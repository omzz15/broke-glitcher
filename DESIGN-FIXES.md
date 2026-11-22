# Controller design fixes — 2026-11-22

These changes address the confirmed schematic/check failures and the practical layout corrections
from the controller review. The PCB remains a 50 × 50 mm, four-layer controller using the existing
JLC04161H-3313 stackup. The target GPIO assignment is unchanged. No parts were purchased.

## Changes

| Area | Change |
|---|---|
| Crowbar | Relocated Q1, U2, R3–R7, C5, C7 and TP4; rerouted the gate drive and local power/ground connections. The routed Q1–R8–J11 drain path is now approximately **8.52 mm**, down from **13.51 mm**. Its main tracks are 0.8 mm wide instead of 0.5 mm. R8 and J11 stayed in place to respect the SMA courtyard. |
| ADC input | Moved C43 to the ADC's AIN lead. The connection from C43 to U7 pin 27 is approximately **1.78 mm** of track. C29 was relocated to make room, and the reference connection was rerouted. R54 stays at the amplifier output. |
| BOOTSEL | Moved R19 near the flash, leaving approximately **2.10 mm** between its flash-side pad and U5 CS. The long button route is now behind the resistor. TP15 moved slightly for clearance. |
| Routing cleanup | Removed the four original dangling USB/VBUS stubs. Refilling and DRC found no remaining unrouted connections. Ground stitching outside the edited region was preserved. Five stitching vias now retain their explicit GND assignment instead of being automatically reassigned during refill. |
| Silkscreen | Trimmed footprint silkscreen to the existing 0.15 mm pad-clearance rule; retained too-small fragments on fabrication layers. Moved clashing subsystem outlines to User.Drawings, adjusted test-point circles, and clipped the USB outline at the board edge. Added back-side SMA, SWD and target-power labels. |
| Schematic | Removed the isolated LINK_GPIO28 label. Separated the legacy target bus from LINK_GPIO[17..29] and connected it to its own interface sheet pin. Added a power flag after the target shunt. Corrected F1's footprint filter to accept its existing 1206 fuse footprint. |
| Controller-only scope | Marked the 29 target-only components excluded from this PCB and BOM. The target schematic, values, MPNs, LCSC codes and DNP flags remain available. These exclusions prevent a PCB update from reintroducing the target. |
| Library portability | Recovered the already embedded BrokeGlitcher symbols into `BrokeGlitcher.kicad_sym` and restored `sym-lib-table`. No new symbol pinouts or custom footprint libraries were designed. |

Moved PCB footprints: **Q1, U2, R3, R4, R5, R6, R7, R19, C5, C7, C29, C43, TP4, TP15**.
Exact before/after coordinates are in [preservation.json](review/2026-11-22/preservation.json).
The physical controller BOM has no added or substituted components.

## Verification and exclusions

KiCad 10.0.3 validation after zone refill:

- **ERC: 0 violations.**
- **DRC: 0 active violations; 0 unconnected items.**
- **Schematic/PCB parity: 0 mismatches.**
- All **118 PCB footprints** preserve their references, footprint identities, component fields,
  pad geometry and pad nets. This was checked independently of the DRC exclusions.
- Native XML netlists confirm the controller's connectivity and net names are identical to the
  starting design. All schematic value/footprint/datasheet/MPN/LCSC fields were preserved.
- Top/bottom PCB renders and the changed schematic pages were inspected.
- Existing manual project settings were preserved outside the documented DRC exclusion entries.

The DRC result includes **118 individually documented exclusions**: the **15 pre-existing SMA
edge-clearance exclusions**, plus **103 footprint-library comparison notices**, including the
pre-existing U4 notice. The latter are accepted because the local graphics intentionally differ
after the silkscreen cleanup and every pad and component field was checked against the original.
The original U4 pad definitions were also checked against the standard footprint in the preceding
review. No copper-clearance, unrouted-net or silkscreen violation was newly excluded, and no rule
severity or fabrication clearance was relaxed. Updating these footprints from the library can
restore the original silkscreen clashes; rerun DRC after doing so.

KiCad documents disabling automatic net updates for stitching vias in its
[PCB Editor manual](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html#_routing_tracks_and_vias).
The five affected UUIDs are recorded in
[ground-net-retention.json](review/2026-11-22/ground-net-retention.json).

Evidence: [ERC](review/2026-11-22/erc-final.json),
[DRC and parity](review/2026-11-22/parity-final.json),
[pad/field preservation](review/2026-11-22/preservation.json),
[netlist preservation](review/2026-11-22/netlist-preservation.json).

The target-only exclusions and their original flags are recorded in
[target-exclusions.json](review/2026-11-22/target-exclusions.json). Restore those flags when creating
a target PCB/BOM; the current controller header still exposes raw GPIO and does not assign those
pins to the target peripherals.

## Remaining operating and assembly checks

These edits do not establish measured glitch timing or ADC performance. The earlier review's
unmeasured operating-envelope concerns remain:

- Validate D7/D8 input-clamp transients against U8's input limits with the intended target.
- Measure U3 temperature and determine the combined controller/target continuous-current budget.
- Check the post-fuse USB supply against U2's 4.5 V minimum recommended operating voltage.
- Agree the RP2040 exposed-pad via/paste treatment with the assembler; its existing vias were
  retained. Tenting is not filled/capped via-in-pad.
- Confirm the exact hand-fitted SMA geometry and J2 assembly choice before preparing an order.

Confidence is **high** for connectivity, preserved attributes, measured file geometry and native
check results. Performance improvements are engineering expectations requiring bench verification.

The complete starting snapshot and intermediate reports are retained outside the Git repository at
`~/Documents/ChatGPT/Low Cost Glitching Board/reviews/2026-11-22-fixes/`.
Changes are saved locally; no commit, push, purchase or fabrication order was made.
