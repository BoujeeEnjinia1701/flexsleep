---
doc_id: FXS-RSK-001
title: FlexSleep Origami Patient Pod risk register, hazard analysis and design FMEA
project: FlexSleep Origami Patient Pod
doc_type: Risk register
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First project risk register, preliminary hazard analysis and first-pass design FMEA for FS1
---

# FlexSleep Origami Patient Pod risk register, hazard analysis and design FMEA

The highest risks are a patient pulling a wall over and falling (H1), a bed fire involving the panels (H2) and a delayed resuscitation (H3). All three are first-order checks of the platform for FlexSleep; H1 and H2 are not closed by design and go to Amish (FXS-DEC-001 D2, D7).

Release limitation (STANDARDS 25.5b): no prototype is used in patient care until its stability, fire performance, cleanability and the procedure it embeds are reviewed by qualified IPC and safety staff.

## Project risks

| Risk | Cause | Effect | Likelihood (1 to 5) | Impact (1 to 5) | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- |
| The airborne hypothesis is not supported | Weak and mixed evidence for partitions (S2) | Decision gate fails | 4 | 3 | Project lead | Keep claims to contact and splash; test V1 early |
| Fire acceptance refused | Panels beside bedding (S20) | Pod unusable round sleeping patients | 3 | 5 | Project lead | D7; pursue FS3 (D1) |
| Density cost too high | 38 % fewer beds (S31) | Operators decline | 3 | 4 | Field partner | D8; FS3 |
| Cost over target | Sheet and freight (S30) | Funding case weaker | 4 | 2 | Value engineering | Bulk sheet, shared freight, moulding |
| Field partner not engaged | No MSF or IRC contact yet | No validation | 3 | 4 | Helpful Engineering | PLN partner list |

## Preliminary hazard analysis

| # | Hazard | Cause | Harm | Severity (1 to 5) | Likelihood (1 to 5) | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Wall gives way under a patient | Patient pulls, leans or rolls; wall tips at about 10 N, needs 137 to 281 N (S11) | Fall, fracture | 4 | 4 | Prohibition sign (F2); patient rule (D2); FS3 principle | High until D2 |
| H2 | Panels burn in a bed fire | Mattress fire, candle, coil, charger, oxygen (S20, S22) | Burns, smoke, spread to neighbours | 5 | 2 | FR grade with reports; no ignition sources; pods apart (F6); D7 test | High until D7 |
| H3 | Delayed resuscitation | Head enclosed; 210 mm side gaps (S17) | Death or harm | 5 | 2 | Split head swings open (F5); 0.6 m behind head (F9); cot pull-out; drill V2 | Medium |
| H4 | Pod tips into the aisle or the next bed | Bump, door gust, fan (S10, S40) | Minor injury, trip | 2 | 4 | Layout rules (D9); limit L1 | Medium |
| H5 | Trip over outriggers and bags | 43 mm beams, 70 mm bags at floor level (S41) | Fall of staff carrying patients | 3 | 3 | Floor marking; layout (D8) | Medium |
| H6 | Fingers trapped | Joint slits 11.6 mm (S36) | Minor injury | 2 | 2 | Cover strips (F8) | Low |
| H7 | Missed deterioration | Side view limited (S7, S50) | Delayed care | 4 | 2 | Foot ends to the nurse station (D8) | Medium |
| H8 | Contamination retained | Unsealed edges, slits, clip crevices (S28) | Cross-contamination | 3 | 2 | E1 to E3; strips; clips removed for cleaning | Medium |
| H9 | Oxygen enrichment | O2 tubing inside three walls (S22) | Fire intensity | 5 | 2 | No equipment in the pod; site review | Medium |
| H10 | False sense of protection | Pod read as an isolation measure | Lapses in IPC practice | 3 | 3 | Claims register (FXS-CLM-001); labels | Medium |

## Design FMEA (first pass)

| Item | Function | Failure mode | Effect | Cause | Severity | Occurrence | Detection | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Side wall | Boundary | Tips or folds inward | Patient falls (H1) | Pull or lean beyond about 10 N | 8 | 6 | 4 | 192 | D2; FS3 graft; sign |
| Panel sheet | Fire behaviour | Ignites and drips | Burns (H2) | Bed fire | 10 | 3 | 5 | 150 | D7 test; reports C1 |
| Head clips | Release | Slow or stuck release | Delayed CPR (H3) | Gloves, crouch, worn tongue | 9 | 3 | 4 | 108 | Drill V2; release marks |
| Free-edge leaf | Stand | Buckles hot | Wall collapse | 50 C tent, creep | 5 | 2 | 4 | 40 | Edge channel F7; T1 hot |
| Outrigger | Widen base | Folds at the spigot | Pod tips | Bag load, crush score | 5 | 3 | 5 | 75 | Pinned spigot F3; T7 |
| Clip | Hold joint | Peg pulls out | Wall separates | Pull up to 231 N on one clip | 6 | 3 | 5 | 90 | FXP-PLT-001 T3 |
| Cover strip | Close slit | Peels | Gap reopens | Heat-staking fails, wiping | 3 | 4 | 3 | 36 | C7; T6 |
| Foot pad | Grip | Slides | Pod moves to next bed | Wet floor | 4 | 4 | 4 | 64 | C4; T7 |
| Ballast bag | Ballast | Leaks or soaks | Splash, contamination | Cholera floor (S45) | 4 | 3 | 3 | 36 | C3 sealed cover |
| Print | Sign | Unreadable | Pull hazard not flagged | Wipes, language | 5 | 3 | 4 | 60 | FXP-PLT-001 T4, T5 |

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
