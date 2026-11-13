---
doc_id: FXS-DEC-001
title: FlexSleep Origami Patient Pod design decisions register
project: FlexSleep Origami Patient Pod
doc_type: Design decisions register
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First register; D1 to D9 proposed, awaiting Amish; F1 to F10 made under the standing instruction of 2026-10-23; C1 to C8 to confirm when bought
---

# FlexSleep Origami Patient Pod design decisions register

Every design decision for this repo, in one place. Nothing below is recorded as Amish's decision unless he made it: the open decisions are **proposed, awaiting Amish**. The STEM fixes F1 to F10 were made under his standing instruction of 2026-10-23 (STANDARDS section 20) and he can reverse them. Decided by Amish: the repo shape (one public repo), licences as Helpful Water, no archive, the credits list, the shared Flex platform for the three Flex repos (2026-11-12) and the standing fix rule (2026-10-23). The platform's own decisions D1 to D18 (FXP-PLT-001) are the proposed baseline awaiting him and are not restated here.

Release limitation (STANDARDS 25.5b): no prototype is used in patient care until its stability, fire performance, cleanability and the procedure it embeds are reviewed by qualified IPC and safety staff.

## Open decisions (proposed, awaiting Amish)

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| D1 | Concept choice | FS1 origami pod (149 of 235); FS2 fabric screen on a pole frame (141); FS3 cot-mounted head-end screen (171) | FS3 as the principle for the next stage (15 % above FS1), with FS1's FR twinwall panels grafted on; FS1 carried now in the drawings, BOM and build plan as the team's concept | Everything | FXS-OPT-001, FXS-DDR-001 |
| D2 | Patients who pull, roll or need help to stand (STM S11, S48) | (a) pod only for patients who stand unaided, with the sign; (b) any patient, with the sign and a staff rule; (c) a cot-mounted grab handle rated as a support, separate from the pod; (d) FS3 principle (cot carries the load) | (a) now, (c) or (d) for the next stage; children and delirious patients by site rule | Signs, patient selection, PR-018 | FXS-CAL-001 section 7 |
| D3 | Wall height and the team's privacy and observation claims (STM S6, S7, X11) | (a) P12, 1.2 m, privacy lying down only, observation from the foot end (as drawn); (b) P18 with a frosted FR film or mesh upper band (6.05 kg of panels from 4 sheets; free-end leaf fails cold without a stiffener; band needs its own fire report); (c) P18 at the head wall only | (a); restate the claims as "privacy lying down" and "observe from the foot end" | PR-003, PR-004, claims | FXS-CAL-001 section 4 |
| D4 | Perforated lower band (team feature, STM S3) | (a) keep (1.2 % of the openings, 40 sealed hole edges, in the cholera splash zone); (b) drop | (b) | Panel making sketch, cleaning | FXS-CAL-001 section 5 |
| D5 | Lateral criterion (STM S10) | (a) state platform limit L1: a boundary that tips if leant on, free ends at about 11 N; (b) more ballast (does not close it, the zigzag is soft in torsion); (c) tie the pod to the cot (FS3 graft) | (a) now, (c) studied with D1 | PR-007, label | FXP-PLT-001 L1, D5 |
| D6 | Routine care access (STM S18, S19) | (a) care from the foot end and by opening the head; (b) cot set off centre, leaving about 345 mm on the working side of a 0.75 m cot; (c) a wider pod (changes the plan and density) | (a) with (b) | Layout rule | FXS-CAL-001 section 2 |
| D7 | Fire benchmark and acceptance (STM S20, S21) | (a) platform minimum (NFPA 701 TM1 and ASTM E84 Class A reports); (b) add NFPA 286 room-corner and a full-scale bed-and-pod test before any patient use; (c) keep FS1 away from sleeping use until (b) passes | (b), with a pod-to-pod wall gap of at least 1.0 m (2.5 m bed pitch) set with the site's fire staff | PR-008, REG, VER | FXP-PLT-001 D18 |
| D8 | Ward layout and density (STM S31, S41, S50) | (a) rows with foot ends to the nurse station, 2.5 m pitch, 1.2 m foot aisle, outriggers and bags marked on the floor; (b) closer pitch (pods do not fit) | (a); accept about 6.2 pods per 45 m2 against 10 beds, or choose FS3 | Layout card, PR-014 | FXS-CAL-001 section 10 |
| D9 | Tent doors and fans (STM S40) | (a) pods at least one pod length from tent doors and never in a fan's jet; (b) two bags at each free end; (c) both | (a) | Layout card, BOM 7 | FXS-CAL-001 section 7 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| C1 | The FR sheet lot's NFPA 701 TM1 and ASTM E84 reports and grammage (at most 700 g/m2) | Fire, mass | PR-008; FXP-PLT-001 F5 |
| C2 | Printed foot block mass at 4 walls and 25 % infill (assumed 45 % of solid) and its strength at the spigot | Mass, outrigger | FXS-CAL-001 A3 |
| C3 | A sealed, wipeable ballast bag cover | Cholera splash, cleaning | STM S35, S45 |
| C4 | EPDM pad friction on wet clinical vinyl and tent groundsheet | Sliding | STM S12 |
| C5 | Cot rail and leg shapes of the cots in use | Fit; FS3 clamps | STM S8, X6 |
| C6 | Aluminium channel 7.5 x 25 x 1.5 mm stock or the nearest size | Edge stiffener | BOM 11 |
| C7 | Clear PP strip film and its heat-staking to FR twinwall | Joint cover strips | BOM 13 |
| C8 | Patent attorney review of US 11,369,208 B2 and US 12,213,925 B2 if FS3 is chosen | FTO | FXS-FTO-001 |

## Decisions made

| Date | Decision | Words or authority | Record |
| --- | --- | --- | --- |
| 2026-11-12 | Shared Flex platform for FlexClean, FlexSleep and FlexTriage | Amish | FXP-PLT-001 |
| 2026-10-23 | Standing STEM fix rule | Amish | STANDARDS section 20 |
| 2026-11-12 | F1 Angle clip arms on a 12 mm round core (the platform square core stands 0.93 mm proud in the 150 deg slot) | Standing instruction | FXS-DDR-003 |
| 2026-11-12 | F2 Prohibition sign and words on both side walls, ISO 3864 prohibition form | Standing instruction | FXS-DDR-003 |
| 2026-11-12 | F3 Outrigger slid over a 100 mm spigot on the block and pinned | Standing instruction | FXS-DDR-002 |
| 2026-11-12 | F4 EPDM pads under every foot block | Standing instruction | FXS-DDR-003 |
| 2026-11-12 | F5 Split head that swings open on the corner folds; no foot at the head centre | Standing instruction | FXS-DDR-003 |
| 2026-11-12 | F6 Pods never touch; no ignition sources or oxygen equipment in or on a pod; tubing over the nearest wall top | Standing instruction | FXS-DDR-003 |
| 2026-11-12 | F7 Aluminium edge stiffener channels on the free ends | Standing instruction | FXS-DDR-003 |
| 2026-11-12 | F8 Joint cover strips on both faces of every angle joint | Standing instruction | FXS-DDR-003 |
| 2026-11-12 | F9 0.6 m clear behind the head wall | Standing instruction | FXS-DDR-003 |
| 2026-11-12 | F10 Pins and bolts in A4 (316) stainless | Standing instruction | FXS-DDR-003 |

## Value engineering

Value-engineering target: USD 120 per pod (stretch under USD 75 at volume). Estimated cost of the constructable design: USD 214.00 at prototype quantities (USD 94.00 over the target). Drivers: two FR sheets USD 90.00, freight share USD 25.00, carry bag USD 20.00, foot blocks USD 18.60, ballast bags USD 15.00, edge channels USD 12.00. Savings worth trying: FR sheet by the pallet; freight shared across a ward's pods; a cheaper sleeve bag; moulded cored feet and clips at volume (FXP-PLT-001 D4); dropping the perforated band saves punching time, not material. The stretch target is not shown on paper.

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
