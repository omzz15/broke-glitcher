"""Prepare a fabrication copy, preserving the editable project's layout."""
import json
from pathlib import Path
import wx

app = wx.App(False)
wx.Image.CleanUpHandlers()
import pcbnew as p

root = Path(__file__).resolve().parents[1]
board = p.LoadBoard(str(root / 'source/broke-glitcher.kicad_pcb'))
board.GetDesignSettings().SetAuxOrigin(p.VECTOR2I(p.FromMM(15), p.FromMM(65)))
removed = []
for footprint in board.GetFootprints():
    if not footprint.IsDNP():
        continue
    for pad in footprint.Pads():
        layers = pad.GetLayerSet()
        paste = [layer for layer in (p.F_Paste, p.B_Paste) if pad.IsOnLayer(layer)]
        for layer in paste:
            layers.removeLayer(layer)
        if paste:
            pad.SetLayerSet(layers)
            removed.append({'ref': footprint.GetReference(), 'pad': pad.GetNumber(),
                            'layers': [p.LayerName(layer) for layer in paste]})
p.SaveBoard(str(root / 'export/broke-glitcher.kicad_pcb'), board)
(root / 'checks/export-adjustments.json').write_text(json.dumps({
    'origin_mm': [15, 65], 'dnp_paste_apertures_removed': removed,
    'note': 'Export copy only. No changes to copper, solder mask, drills or silkscreen.'
}, indent=2) + '\n')
print('Export origin: bottom-left (15,65) mm; removed paste from', len(removed), 'DNP pads')
app.Destroy()
