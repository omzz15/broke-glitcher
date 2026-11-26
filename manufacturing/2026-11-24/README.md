# Glitch Penguin manufacturing package

Built from the saved `broke-glitcher` KiCad project on 2026-11-24.

Read **ORDERING.md** before submitting the files. The board is **75 × 50 mm, four layers**, with **110 top-side placements** and **37 BOM lines**. All SMA connectors and 2.54 mm headers are excluded.

- `glitch-penguin-gerbers.zip`: upload to JLCPCB for fabrication.
- `assembly/jlcpcb-bom.csv`: upload as the assembly BOM.
- `assembly/jlcpcb-cpl.csv`: upload as the assembly placement file.
- `FABRICATION-NOTES.txt`: engineering notes for stackup, seam, rails and assembly.
- `assembly/assembly-top.pdf`: assembly location / pad-number reference; crossed-out footprints are DNP.
- `assembly/orientation-pad-reference.csv`: physical pad positions for checking polarized parts.
- `assembly/not-assembled.csv`: complete exclusion list, including non-component PCB features.
- `VALIDATION.md`: validation scope, findings and remaining order-preview checks.
- `previews/`: native KiCad reference renders. Colors and missing 3D models are not a calibrated photo or a supplier assembly proof.
- `gerbers/`: unpacked fabrication files.
- `source/`: frozen schematic/project and PCB with zones refilled by native KiCad.
- `export/`: derived PCB used for exports: same design, origin at lower left, DNP paste apertures removed.
- `checks/`: native DRC, BOM/position export, transformation audit and Gerber analysis.
- `SHA256SUMS.txt`: file checksums for this package.

No order was placed. Stock, price, CAM panel/rail acceptance and the JLCPCB placement preview still need to be confirmed at ordering time. The full download ZIP is a bundle; do not upload it in place of the Gerber-only ZIP.
