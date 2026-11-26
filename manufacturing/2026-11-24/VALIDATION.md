# Manufacturing export validation

Date: 2026-11-24. Tool: KiCad 10.0.3.

This pass generated and checked manufacturing files. It is not a new full electrical, thermal or signal-integrity review, nor a factory DFM approval.

## Results

| Check | Result |
|---|---|
| Saved source versus archived PCB | Same parsed board items; native save/refill reordered some zone records only |
| Source schematics versus snapshot | Exact byte matches |
| Export-only adjustments | Lower-left auxiliary origin at KiCad (15,65) mm; paste removed from 30 DNP SMA pads |
| Copper, tracks, vias, pads, mask, drills, outline and artwork | Preserved from source; no electrical design changes |
| Native DRC unconnected items | **0** |
| Native schematic parity issues | **0** |
| Gerber completeness/alignment analyzer | Complete, aligned; **0 findings** |
| Fabrication layers | 4 copper, 2 mask, 2 silk, front paste, one outline |
| Drill files | Separate PTH and NPTH, metric decimal, shared export origin |
| Plated drill operations | 414 total, including 4 USB shell slots |
| Non-plated holes | 52: 50 mouse-bite holes, 2 USB locating holes |
| BOM/CPL | Exact designator-set match; no duplicate references |
| Assembly count | 110 top-side components, 37 BOM rows |
| Part numbers | Every included component has an LCSC number and MPN matching its schematic/PCB fields |
| Exclusions | All 12 DNP connectors/headers excluded; J1 USB-C included |
| Board size | Outline centerline 75 × 50 mm; bounding box including outline stroke 75.05 × 50.05 mm |
| Via tenting | Board setup enables front/back tenting; all 319 track-vias inherit it |
| Native visual check | Front/back renders and assembly reference inspected |

`checks/package-validation.json` records the structural checks. Native exports and analyzer outputs are retained in `checks/`. The frozen export board is retained in `export/`.

## Existing DRC findings retained

The configured DRC reports **504 findings: 48 errors and 456 warnings**. It is not a clean DRC report. The following categorization describes the actual output; it does not globally waive manufacturing requirements.

| Type | Count | Interpretation for this export |
|---|---:|---|
| NPTH inside courtyard | 45 | MB1 mouse-bite holes intersect J5/J10/JP2 courtyards; these headers are DNP. No corresponding drill-to-copper clearance violation was reported. Factory seam/rail acceptance remains necessary. |
| Courtyards overlap | 3 | MB1 with J5, J10 and JP2; same unpopulated-header situation |
| Silkscreen over mask openings | 199 | Mostly footprint markings near exposed pads. Export uses solder-mask subtraction; some printed strokes will be clipped. |
| Silkscreen overlap | 128 | Existing text/graphics intersections; no artwork redesign performed |
| Text height | 79 | Existing text below the project's 1.0 mm rule, including 0.8 mm labels |
| Text stroke thickness | 32 | Existing TrueType glyph strokes below the configured check; small lettering still needs CAM review |
| Library footprint differs | 9 | Existing placed-footprint edits; current board footprints were exported as-is |
| Dangling track ends | 7 | Existing stubs; separate unconnected-items count is zero |
| Silk at board edge | 2 | J1 footprint silk at the upper edge |

Full evidence, coordinates and UUIDs: `checks/drc.json`. No errors were hidden by modifying severities, clearing warnings or changing project rules. This pass used the user's existing rule configuration.

## Placement conventions and limits

The JLC CPL uses the pad-bounding-box centre convention and common package rotations from Fabrication Toolkit's pinned transformation data:

https://github.com/bennymeg/Fabrication-Toolkit/blob/7f627b6be76081b962161b9eb9fe3a326a18c915/plugins/transformations.csv

The data is retained in `checks/jlc-footprint-transforms.csv`. `checks/placement-transforms.csv` records each applied correction. Corrections are package-based conventions, **not verification against JLCPCB's specific part models**. No downloaded third-party plugin code was run.

The USB-C centre changes by 1.46 mm relative to the KiCad footprint anchor. Twelve parts receive generic angle offsets. U6's `Texas_RHB0032E_VQFN...` name does not match the transformation table, so no angle correction was guessed for U6. Check its physical pad 1 in JLCPCB's preview, along with all other ICs, LEDs, diodes, MOSFETs and the USB-C connector. The orientation CSV and assembly PDF provide the intended board-side pad locations.

## Remaining ordering checks

- No JLCPCB upload or placement preview was performed; do not treat the CPL as an approved assembly proof.
- Stock, live Basic/Extended classification, prices, attrition and substitutions are not verified by this export.
- The 75 × 50 mm design needs external rails or a factory carrier/panel for Standard PCBA's published 70 × 70 mm minimum. Those rails are not in these Gerbers; coordinate their addition with JLCPCB and preserve the internal seam.
- White mask, black silk and HASL follow the saved design. Native 3D colors and absent 3D connector models do not predict the exact manufactured appearance.
- No firmware programming or functional test is provided. Bare-board net testing and assembly inspection do not replace bring-up testing.

Ordering selections and factory notes are in `ORDERING.md` and `FABRICATION-NOTES.txt`.
