# Routable mousebite seam for Broke Glitcher

This footprint replaces the entire existing central mousebite assembly: **all fourteen stock half-footprints, using one footprint**. It retains the 2 mm controller-to-target gap, all header positions, and aligns with 2.5 mm corner radii on the 50 mm-tall boards. The five remaining tabs follow the existing signal groups.

The working PCB and schematics have not been changed. A separate fitted example based on commit `6d9a196` uses 2.5 mm radii on all eight board corners. The working board still has its original 2.25 mm radii.

![Dimensioned seam overview](/Users/asritha/broke-glitcher/docs/mousebite-seam/seam-overview.svg)

## Files and placement

- Footprint library: [BrokeGlitcher_Mechanical.pretty](/Users/asritha/broke-glitcher/footprints/BrokeGlitcher_Mechanical.pretty)
- Footprint: [MouseBite_Seam_2x45mm_5Tabs5mm_D0.5_Route.kicad_mod](/Users/asritha/broke-glitcher/footprints/BrokeGlitcher_Mechanical.pretty/MouseBite_Seam_2x45mm_5Tabs5mm_D0.5_Route.kicad_mod)
- Project library registration: [fp-lib-table](/Users/asritha/broke-glitcher/fp-lib-table)
- Dimensioned drawing: [seam-overview.svg](/Users/asritha/broke-glitcher/docs/mousebite-seam/seam-overview.svg)
- Local fitted example: [broke-glitcher.kicad_pcb](</Users/asritha/Documents/ChatGPT/Low Cost Glitching Board/mousebite-design/validation/broke-glitcher.kicad_pcb>)
- Native four-layer plots: [fitted-copper.pdf](</Users/asritha/Documents/ChatGPT/Low Cost Glitching Board/mousebite-design/validation/fitted-copper.pdf>)
- [Validation summary](/Users/asritha/broke-glitcher/docs/mousebite-seam/validation-summary.json)

The library entry uses `${KIPRJMOD}/footprints/BrokeGlitcher_Mechanical.pretty`, so the library remains portable with the repository. The absolute links above point to this workstation's files.

Place `BrokeGlitcher_Mechanical:MouseBite_Seam_2x45mm_5Tabs5mm_D0.5_Route` at **X = 66.000 mm, Y = 40.000 mm, rotation = 0°**, on the front side. It is a board-only mechanical footprint; no schematic symbol, component order, paste or silkscreen is required. It is excluded from BOM and placement output.

## Dimensions and manufacturing basis

| Feature | Design |
|---|---:|
| Existing board-edge gap | 2.0 mm |
| Overall replacement seam height | 45 mm |
| Matching board corner radius | 2.5 mm |
| Number of tabs | 5 |
| Minimum tab neck | 5.0 mm |
| Tab centre pitch | 6.6 mm |
| Internal routed slots | 2.0 × 1.6 mm, 0.8 mm corner radius |
| Mousebite holes | 50 × Ø0.5 mm NPTH |
| Hole rows | X = 65.25 and 66.75 mm |
| Ordinary adjacent-hole pitch | 0.8 mm, leaving 0.3 mm material |
| Wider intentional routing gaps | 1.8 mm between hole centres |
| Hole-edge-to-copper design clearance | 0.25 mm |
| Usable routing window between holes | 0.8 mm, after both clearances |
| Routing windows | Two per tab, available on all four layers |
| Fracture-strip via keepout | X = 64.8–67.2, Y = 23.6–56.4 mm |

JLC currently specifies a 5 mm minimum mousebite tab, recommends Ø0.5–0.8 mm holes, and gives 0.2 mm NPTH-to-track and routed-edge-to-copper clearances. Its minimum non-plated routed slot is 1.0 mm. This design uses a 1.6 mm minimum opening and 0.25 mm hole-to-copper clearance. The 0.3 mm ordinary hole webs are within the published 0.2–0.3 mm recommendation. [JLCPCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities/)

The intentionally larger spaces between selected holes carry the electrical connections; this is not a uniformly perforated mechanical tab. The pattern follows the routable-tab principle of the previous stock footprint. Its dimensions have been checked, but JLC has not approved this custom electrically connected seam and its break force has not been measured.

The new upper/lower notches remove the two former end tabs, which had no signal traces crossing them. Ground pours change during refill, so review the resulting header thermals as described below.

## Routing allocation

The bounds below are **available copper extents**, not trace-centre limits. Keep half the trace width inside each end of the interval. For example, a 0.5 mm trace in a 0.8 mm window has 0.3 mm of positioning freedom.

| Tab centre Y | Window Y bounds, mm | F.Cu crossing | B.Cu crossing |
|---:|---|---|---|
| 26.8 | 25.5–26.3 | Spare | Sense P and Sense N, 0.2 mm each |
| 26.8 | 27.3–28.1 | Always-on +3V3, 0.5 mm | Switched TARGET_VDD, 0.5 mm |
| 33.4 | 32.1–32.9 | GP29 / SWCLK | GP28 / SWDIO |
| 33.4 | 33.9–34.7 | GP26 / reset | GP27 / BSL |
| 40.0 | 38.7–39.5 | GP25 / LF clock | Spare |
| 40.0 | 40.5–41.3 | GP23 / HF clock | GP24 / trigger |
| 46.6 | 45.3–46.1 | GP22 / SPI CS | GP21 / controller UART RX |
| 46.6 | 47.1–47.9 | GP20 / controller UART TX | GP19 / controller SPI TX |
| 53.2 | 51.9–52.7 | GP16 / controller SPI RX | GP18 / SPI clock |
| 53.2 | 53.7–54.5 | Spare | TARGET_GLITCH_OUT, 0.5 mm |

This accommodates all **13 GPIO signals, two power feeds, two physical sense traces and the glitch output**. Sense P shares the TARGET_VDD net name but is a separate thin Kelvin branch. Ground remains supplied through the copper reference layers; the five GND header contacts are one net, not five additional independent signal traces.

A 0.8 mm window can accommodate three 0.15 mm signals at 0.15 mm spacing, or one 0.5 mm power trace. The actual fit retains the 0.150876 mm GPIO widths. Do not fill both inner layers with extra signal routing: keep an adjacent GND reference beneath the top/bottom crossings.

The footprint includes 0.25 mm local NPTH clearance and a no-via rule area. It does not forbid ground pours; these should refill around the holes. Teal rectangles on Dwgs.User show the usable routing windows and do not appear in copper or silkscreen fabrication output.

## Replacement procedure

If the earlier 45.5 mm custom seam is already placed, change its footprint assignment to the new 45 mm version at the same position and rotation. Only the end extensions are shorter; no further trace shifts are needed. Update the board corners as described in step 2.

1. Save your current board. Delete only the fourteen footprints named `Panelization:MouseBite-Part_2.0x4.5mm_outset_D0.5mm_P0.85mm_5h_Trace`. Do not delete the headers or the board-level corner arcs.
2. Add the new footprint at **(66,40), 0°**. The four seam endpoints are at X=65/67, Y=17.5/62.5 mm. Set the adjoining board corners to radius 2.5 mm and extend/trim the adjacent straight edges to their new tangent points. The fitted example updates all eight outer corners. No extra straight connector segments are needed.
3. Make the four local trace adjustments below. The fitted example shows the exact result. GPIO crossings and the main switched-power feed can remain where they are.
4. Refill zones, inspect both outer layers and both ground references, and run native DRC. Do not remove the no-via rule or reduce hole clearance to force a route through.
5. Re-export the board outline and drill files. Ensure all fifty mousebite holes are non-plated and the internal slots are routed from Edge.Cuts.

| Crossing | Existing centre Y | Fitted centre Y | Shift |
|---|---:|---:|---:|
| +3V3, F.Cu, 0.5 mm | 28.00 | 27.70 | −0.30 mm |
| Sense P / TARGET_VDD **0.2 mm branch**, B.Cu | 25.96 | 25.80 | −0.16 mm |
| Sense N / TARGET_VDD_SENSE, B.Cu | 26.25 | 26.15 | −0.10 mm |
| TARGET_GLITCH_OUT, B.Cu, 0.5 mm | 53.70 | 54.10 | +0.40 mm |

The thin sense branches start only 0.09 mm apart at their copper edges. Stagger their approach bends so the upper trace moves away first; bending both simultaneously can reduce perpendicular spacing below that limit. In the fitted example, Sense P tapers over X=64.05–64.75 and 67.25–67.95; Sense N tapers over X=64.35–65 and 67–67.65. The other adjusted crossings taper over X=64.25–65 and 67–67.75. Keep the main 0.5 mm TARGET_VDD feed at Y=27.75.

## Validation and remaining layout work

Validation used native KiCad 10.0.3 footprint loading, zone refill, DRC, PDF plotting, Gerber export and separate PTH/NPTH drill export, plus an independent raw-file clearance calculation.

- The footprint loads with 50 NPTH pads, a no-via rule area and its routed outline.
- All **485 numbered pad/net identities remain unchanged** in the fitted board.
- **Zero unconnected items**, zero copper-clearance violations, and no open-outline or hole-clearance errors in the fitted copy.
- Minimum calculated new-hole-edge-to-track clearance: **0.274562 mm**, at the GP18 crossing.
- Native drill export contains **50 new Ø0.5 mm non-plated holes**; the two existing Ø0.65 mm USB locator holes are separate.
- The fitted example uses 2.5 mm board-corner radii; only the footprint end extensions change, so tab positions, holes and routing windows stay the same.
- The source schematics, PCB, project settings and custom rules remain unchanged.

This is a validated footprint fit, **not a clean DRC signoff for the whole board**. The fitted copy retains earlier review issues. Header courtyard/NPTH reports decrease from 14/54 to 3/45, but the near-edge header arrangement remains. Starved thermal messages change from 11 to 13: additional local islands are flagged at **J5.2 on F.Cu** and **J13.2 on B.Cu**. They remain electrically connected through other layers; improve their local ground connections during final layout cleanup. The signal-width rule also counts more split glitch segments after the reroute; retain the wide copper and correct the rule's scope.

The mechanical courtyard warnings involve optional header bodies near the fracture region. They are not copper shorts, but should not be blanket-ignored if headers will be populated before separation. Five tabs with copper crossings can still take substantial force to separate. Prefer cutting/supporting the tabs over twisting the assembled boards, and test on a prototype.

Suggested fabrication note:

> Functional breakaway target section. Keep controller and target attached through assembly and delivery. Do not replace this seam with V-score or depanel it at the factory. Mousebite holes are NPTH; intervening windows intentionally carry copper. Customer separates after testing.

The manufacturing exports in the local validation folder are diagnostic files, not a complete production release.

