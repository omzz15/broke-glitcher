# JLCPCB placement review — 2026-11-24

The live JLCPCB preview was compared with the frozen KiCad pad coordinates in
`../2026-11-24/assembly/orientation-pad-reference.csv` and the assembly drawing.
This is an order-preview alignment check, not a new electrical design review.

## Rotation corrections

| Part | Uploaded CPL angle | Reviewed angle | Expected pin 1 in top view |
| --- | ---: | ---: | --- |
| U3 — RT9013-33GB | 180° | 270° | Upper left, three-pin side on left |
| U4 — RP2040 | 90° | 0° | Upper left, on left edge |
| U8 — SGM8051 | 90° | 180° | Upper right, three-pin side on top |

These changes were applied with the JLCPCB placement editor's individual rotate
controls and checked visually. The generic export rotation rules did not match
these three current JLCPCB library models.

`jlcpcb-cpl-reviewed.csv` records the equivalent corrected input angles. It has
the same 110 references, coordinates and top-side assignment as the original;
only the three angles above differ. Prefer it over the original CPL for a new
upload, then check the preview again because supplier library models can change.
The original dated package and ZIP have been retained without modification.

## Preview findings

- U1, U2, U5, U6 and U7 pin-one markers align with their KiCad pad-one positions.
- Q1/Q2 and D1/D6/D7 pin markers and lead patterns align.
- D2–D5 positive markers are on the right; KiCad cathode pads are on the left.
- J1 USB-C lead row and shell anchors visually align; the opening faces outward.
- Y1 pad-one marker is at lower right; SW1/SW2 align with their lands.
- Passive placement alignment was inspected in the board overview.
- SMA connectors and 2.54 mm headers remain unpopulated.

`placements.jpg` shows the corrected placement page. JLCPCB identifies this
preview as a reference; final engineering placement approval remains enabled.
The user approved this placement page and Next was clicked. JLCPCB then showed
an updated autosave timestamp and opened Quote & Order. The current quote is
recorded in `QUOTE.md`. No order has been placed or paid.

## Live order settings differing from the original instructions

The approved quote uses soldermask-plugged vias because tented vias were not
available in the selected configuration. This is not copper-filled/capped vias.
The PCB note specifies plugging the 0.3/0.5 mm vias only and keeping connector
and NPTH holes open. The user approved this choice on the first quote page.

There are 50 complete joined sets with top-side Standard PCBA. JLCPCB-added
rails expand the quote dimensions from 75 × 50 mm to 75 × 70 mm. Both the internal
seam and external rails are to remain attached at delivery. Final production
file and placement confirmations are enabled without automatic approval.

The matched BOM has 37 exact part lines and 110 placements per unit. The live
parts subtotal at BOM approval was $324.34 for the 50-unit run including attrition;
fabrication, assembly and shipping are additional.
