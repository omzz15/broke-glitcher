"""Build JLC assembly tables and audit every included and excluded footprint."""
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

import wx

app = wx.App(False)
wx.Image.CleanUpHandlers()
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]


def write_csv(path, fields, rows):
    """Write an explicit, stable CSV schema."""
    with path.open('w', newline='') as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def ref_key(ref):
    match = re.fullmatch(r'([A-Za-z]+)(\d+)', ref)
    if match is None:
        raise ValueError(f'Unexpected reference designator: {ref}')
    return match[1], int(match[2])


inventory = json.loads((ROOT / 'checks/inventory.json').read_text())
physical = {x['ref']: x for x in inventory if x['props'].get('LCSC Part #')}
assert len(physical) == 110
assert all('dnp' not in x['attr'] and x['layer'] == 'F.Cu' for x in physical.values())
with (ROOT / 'checks/kicad-bom.csv').open() as source:
    schematic = {row['Designator']: row for row in csv.DictReader(source)}
groups = defaultdict(list)
for ref, item in physical.items():
    symbol = schematic[ref]
    assert symbol['LCSC Part #'] == item['props']['LCSC Part #']
    assert symbol['MPN'] == item['props']['MPN']
    assert symbol['Footprint'] == item['footprint']
    assert symbol['Comment'] == item['value']
    groups[(symbol['LCSC Part #'], symbol['MPN'], symbol['Footprint'])].append(ref)
bom = []
for (lcsc, mpn, footprint), refs in groups.items():
    refs.sort(key=ref_key)
    values = sorted({physical[ref]['value'] for ref in refs})
    bom.append({'Comment': ' / '.join(values), 'Designator': ','.join(refs),
                'Footprint': footprint.split(':')[-1], 'LCSC Part #': lcsc,
                'Quantity': len(refs), 'Manufacturer Part Number': mpn})
bom.sort(key=lambda row: ref_key(row['Designator'].split(',')[0]))
write_csv(ROOT / 'assembly/jlcpcb-bom.csv', list(bom[0]), bom)

board = p.LoadBoard(str(ROOT / 'export/broke-glitcher.kicad_pcb'))
with (ROOT / 'checks/jlc-footprint-transforms.csv').open() as source:
    transforms = list(csv.DictReader(source))
positions = []
audit = []
orientation = []
for footprint in board.GetFootprints():
    ref = footprint.GetReference()
    if ref not in physical:
        continue
    angle = footprint.GetOrientation().AsDegrees()
    assert angle % 90 == 0 and not footprint.IsFlipped()
    pads = list(footprint.Pads())
    box = pads[0].GetBoundingBox()
    for pad in pads[1:]:
        box.Merge(pad.GetBoundingBox())
    center = box.GetCenter()
    origin = board.GetDesignSettings().GetAuxOrigin()
    x, y = p.ToMM(center.x - origin.x), p.ToMM(origin.y - center.y)
    name = str(footprint.GetFPID().GetLibItemName())
    rule = next((r for r in transforms if re.search(r['Regex To Match'], name)), None)
    correction = float(rule['Rotation']) if rule else 0
    rotation = (angle + correction) % 360
    positions.append({'Designator': ref, 'Mid X': f'{x:.6f}mm', 'Mid Y': f'{y:.6f}mm',
                      'Rotation': f'{rotation:.6f}', 'Layer': 'Top'})
    anchor = footprint.GetPosition()
    audit.append({'Designator': ref, 'KiCad rotation': angle, 'Correction': correction,
                  'CPL rotation': rotation, 'Rule': rule['Regex To Match'] if rule else '',
                  'Center minus anchor X mm': p.ToMM(center.x - anchor.x),
                  'Center minus anchor Y mm': p.ToMM(center.y - anchor.y)})
    if ref.startswith(('U', 'D', 'Q', 'J', 'Y')):
        for pad in pads:
            if pad.GetNumber() not in {'1', '2', '3', 'A1', 'B1'}:
                continue
            point = pad.GetPosition()
            orientation.append({'Designator': ref, 'Pad': pad.GetNumber(),
                                'X mm': p.ToMM(point.x - origin.x),
                                'Y mm': p.ToMM(origin.y - point.y),
                                'Net': pad.GetNetname()})
positions.sort(key=lambda row: ref_key(row['Designator']))
audit.sort(key=lambda row: ref_key(row['Designator']))
assert {row['Designator'] for row in positions} == set(physical)
assert sum(row['Quantity'] for row in bom) == len(positions) == 110
assert all(0 < float(row['Mid X'][:-2]) < 75 for row in positions)
assert all(0 < float(row['Mid Y'][:-2]) < 50 for row in positions)
write_csv(ROOT / 'assembly/jlcpcb-cpl.csv', list(positions[0]), positions)
write_csv(ROOT / 'checks/placement-transforms.csv', list(audit[0]), audit)
write_csv(ROOT / 'assembly/orientation-pad-reference.csv', list(orientation[0]), orientation)
excluded = []
for item in sorted(inventory, key=lambda item: ref_key(item['ref'])):
    if item['ref'] in physical:
        continue
    reason = 'DNP connector/header' if item['ref'].startswith('J') and 'dnp' in item['attr'] else 'PCB feature; no purchased component'
    excluded.append({'Designator': item['ref'], 'Value': item['value'],
                     'Footprint': item['footprint'], 'Reason': reason})
write_csv(ROOT / 'assembly/not-assembled.csv', list(excluded[0]), excluded)
print(f'{len(bom)} BOM rows, {len(positions)} placements, {len(excluded)} omitted features')
print('Rotation corrections:', [(r['Designator'], r['Correction']) for r in audit if r['Correction']])
print('Center corrections:', [r for r in audit if abs(r['Center minus anchor X mm']) > .001 or abs(r['Center minus anchor Y mm']) > .001])
app.Destroy()
