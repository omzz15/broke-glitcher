# Glitch Penguin — JLCPCB ordering guide

Prepared 2026-11-24 from the saved KiCad 10.0.3 project. Nothing has been uploaded or ordered.

## Files to upload

| JLCPCB step | File |
|---|---|
| PCB fabrication / Gerber upload | `glitch-penguin-gerbers.zip` |
| Assembly BOM | `assembly/jlcpcb-bom.csv` |
| Assembly CPL / placement | `assembly/jlcpcb-cpl.csv` |
| Engineering reference, if requested | `assembly/assembly-top.pdf`, `assembly/orientation-pad-reference.csv`, and `FABRICATION-NOTES.txt` |

The outer `glitch-penguin-manufacturing-package-2026-11-24.zip` is a download bundle, **not** the Gerber upload. Extract it first. Upload the Gerber-only ZIP above.

The BOM has **37 lines and 110 placed components per complete controller-and-target set**, all on the top side. Quantities in the BOM are for ONE set; do not multiply them by 25 or 50. JLCPCB applies the assembly quantity and its own component attrition allowance. The CPL contains exactly those same 110 designators.

All six SMA connectors and all six 2.54 mm headers already have DNP flags in the schematic and PCB:

| Omitted hardware | References |
|---|---|
| SMA connectors | J4, J6, J7, J8, J9, J11 |
| SWD header | J2 |
| Controller/target link headers | J5, J10 |
| External target headers | J12, J13 |
| Glitch selector header | JP2 |

The USB-C connector J1 **is included**. All resistors, capacitors, ICs, LEDs, switches, MOSFETs, clamp diodes, crystal and fuse are included. Bare test pads, mounting holes, the mouse-bite footprint and copper solder jumpers are PCB features, not purchased components; they are excluded from the assembly tables. `assembly/not-assembled.csv` lists every omission. JP1/JP5/JP6/JP7 retain their etched copper bridges; JP3/JP4 stay open. Do not ask the factory to add jumper shunts or solder bridges.

## PCB order selections

| Option | Selection / instruction |
|---|---|
| Base material | FR-4 |
| Layers | 4 |
| Finished board thickness | **1.6 mm nominal** |
| Board dimensions | **75 × 50 mm** for one joined controller/target set, before any added manufacturing rails |
| Copper | 1 oz outer, 0.5 oz inner; retain the specified stackup |
| Specify stackup | **Yes — JLC04161H-3313 / JLC3313, 4-layer 1.6 mm**. Match 0.0994 mm 3313 prepregs and 1.265 mm core; do not substitute 7628 or 3313A. Confirm the actual stack drawing if the order page changes its naming. |
| Impedance control | Specify the stackup above. No additional certified impedance coupon/test is requested by this package. If the form puts stackup selection under “Impedance Control,” enable that selection, but do not invent a 50 Ω requirement for every trace. |
| PCB solder-mask color | **White** |
| Silkscreen color | **Black**, both sides |
| Surface finish | **HASL with lead**, matching the saved `HAL SnPb` stackup and the latest HASL preference. If you want a lead-free build, select LeadFree HASL instead; the Gerbers are unchanged. |
| Via covering | **Tented, both sides**; preserve the supplied mask openings for component and connector pads |
| Via filling / capping | No epoxy filling/capping requested; do not select paid filled-and-capped vias as a substitute for tenting |
| Different designs | **2** — controller and detachable target |
| Delivery format | **Panel by Customer** for the already joined two-section design. One uploaded 75 × 50 mm unit is one complete set. See the rail instructions below. |
| Quantity | **25 or 50 complete joined sets**, according to your chosen run. This is 25/50 controller boards plus 25/50 targets. Confirm the quote counts sets, rather than counting the two sections separately. |
| Routing / separation | Routed slots and 50 × 0.5 mm NPTH mouse-bite holes as supplied. **No V-score. Keep the internal seam intact.** |
| Castellated holes / edge plating / gold fingers | No |
| Electrical test | Retain JLCPCB's normal bare-board electrical test |
| Mark on PCB | Remove order number, if offered. If marking is mandatory, put it on an added rail or obtain approval for a location; do not overwrite the pin tables or logos. |
| Other special processing | No countersinking, beveling, blind/buried vias, special edge finish or extra surface treatment requested |
| Production-file confirmation | Request/enable confirmation of engineering files before manufacture, particularly the seam and added rails |

The saved KiCad thickness is 1.62516 mm because its layer sum includes solder mask; this is the intended **nominal 1.6 mm** construction, not an order for a custom 1.625 mm thickness. The Gerber job's 75.05 × 50.05 mm bounding box includes the 0.05 mm outline stroke; the actual routing centerline outline is **75 × 50 mm**.

JLCPCB's [stackup table](https://cart.jlcpcb.com/client/template/placeOrder/impedance.html) lists the 3313/core/copper dimensions used here. Its [ordering guide](https://jlcpcb.com/help/article/instructions-for-ordering) describes black silkscreen on white solder mask. Its [different-design policy](https://jlcpcb.com/help/article/different-design-in-your-pcb-files) counts separable, different boards as different designs even when traces connect them.

## Assembly selections and rails

Select **Standard PCBA, top-side assembly**, to retain this white four-layer board and specified stackup. Economic PCBA has restricted combinations of color, layer stackup and quantity; do not assume changing only the finish makes this white four-layer configuration eligible. If saving assembly cost is more important than color, separately quote a green version while keeping the 3313 stackup. Do not change the current order's color or construction implicitly.

Standard PCBA's published minimum panel size is 70 × 70 mm and it requires process rails/fiducials. The supplied unit is 75 × 50 mm, so **ask JLCPCB to add external process rails to reach at least 75 × 70 mm**. A starting request is **10 mm rails on the top and bottom**, with tooling holes and fiducials in those rails. Let their CAM engineer confirm the rail/tab geometry around the protruding USB-C connector. Ordinary 5 mm top/bottom rails would only reach 60 mm and would not meet the published 70 mm minimum.

These external rails are **not drawn in the supplied Gerbers**. If the quote page cannot add them to a customer-panel order, request an engineering-assisted rail/panel quote using `FABRICATION-NOTES.txt`. Do not misstate the original Gerber size as 75 × 70 mm, and do not upload the original CPL against a separately panelized file unless JLCPCB applies the same coordinate transformation to both. The internal controller/target seam must remain exactly as supplied.

| Assembly option | Selection |
|---|---|
| Service | Standard PCBA |
| Assembly side | Top only |
| Assembly quantity | Same number of complete sets as desired: 25 or 50 |
| Parts | Match the exact LCSC numbers in the BOM; check package and MPN before accepting substitutions |
| Procurement | JLCPCB-sourced parts; no customer-supplied parts specified |
| Through-hole hand/wave assembly | No pin headers or SMAs. Retain normal assembly of J1, including its four shell-anchor slots. |
| Depaneling | Do not separate the target from the controller. Keep external rails for shipping if this is the simpler option. |
| Inspection | Retain normal assembly inspection and required QFN X-ray. RP2040 and MSPM0 have hidden exposed-pad joints. |
| Programming / functional testing | Not included; no firmware image or factory test procedure is supplied |
| Conformal coating / potting | None |
| Separate stencil purchase | Not needed solely for JLCPCB's assembly service; its production stencil is handled in assembly |

See JLCPCB's [assembly capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities) for service restrictions, minimum panel size, rails, and inspection. Fees and parts stock must be checked in the actual quote; the project’s Basic/Extended fields are historical and are not a live price or stock check.

## Placement preview before payment

The CPL uses millimetres, with its origin at the joined board's lower-left corner: original KiCad coordinate **(15, 65) mm**. X increases right and Y increases up when looking at the top. Gerbers, drills and CPL share this origin.

Common footprint rotation corrections from the [Fabrication Toolkit](https://github.com/bennymeg/Fabrication-Toolkit/tree/7f627b6be76081b962161b9eb9fe3a326a18c915) were applied, along with its pad-bounding-box centre convention. This shifts J1's placement centre 1.46 mm down from its KiCad anchor. The correction audit is `checks/placement-transforms.csv`; the unmodified KiCad placement export is `checks/kicad-positions.csv`. No third-party plugin code was installed or executed.

**These are upload files, not a JLCPCB-approved placement proof.** Package-based rotations cannot establish every library part's orientation. In the JLCPCB preview, check all IC pin-1 marks, MOSFET/diode pins, LED cathodes, the crystal and USB-C position. **U6's manufacturer-named Texas RHB footprint has no matching automatic rotation rule**; explicitly align its pad 1 rather than assuming 0° is accepted. LEDs, crystal, switches and USB-C also retain their native angle unless the preview requires correction. Match physical pads, not just the rotation number.

`assembly/assembly-top.pdf` and `assembly/orientation-pad-reference.csv` provide board-side reference positions. Check the BOM preview shows **110 fitted components per set** and none of the twelve DNP connectors/headers. J1 must be present. JLCPCB's [BOM/CPL preparation guide](https://jlcpcb.com/help/article/advice-for-bom-and-cpl-files-preparation) requires matching reference designators and consistent coordinate units.

## What was checked

`VALIDATION.md` records the export checks and remaining KiCad findings. This is a manufacturing export pass, not a new full electrical design review. The Gerber set is complete and aligned; there are zero unconnected items and zero schematic parity findings. Existing mouse-bite/courtyard and silkscreen warnings were retained and recorded, rather than silently changing the finished design. Have JLCPCB review the internal breakaway geometry and the final silkscreen proof, including small text, before payment.
