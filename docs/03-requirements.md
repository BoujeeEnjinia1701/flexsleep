---
doc_id: FXS-PRS-001
title: FlexSleep Origami Patient Pod product requirements and specifications
project: FlexSleep Origami Patient Pod
doc_type: Product requirements
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First product requirements for the carried option FS1, traced to FXS-URS-001, with targets, verification and status from FXS-CAL-001 and FXS-STM-001
---

# FlexSleep Origami Patient Pod product requirements and specifications

Requirements for the carried option FS1 (origami panel pod); the choice between FS1, FS2 and FS3 is awaiting Amish (FXS-DEC-001 D1). Status "met on paper" means FXS-CAL-001 or a cited figure shows it; nothing is tested at TRL 3. Verification families are in FXS-VER-001 and the platform tests T1 to T8 in FXP-PLT-001.

Release limitation (STANDARDS 25.5b): no prototype is used in patient care until its stability, fire performance, cleanability and the procedure it embeds are reviewed by qualified IPC and safety staff.

Table 1. Product requirements and specifications.

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001 | Deployment and assembly | Deployment time | One untrained person shall set the pod round an empty cot from its bag, tool-free, with filled bags staged, within the target | 5 | maximum | min | Timed trial V2 at TRL 4 | At risk (estimate 4.2 to 8.3) |
| PR-002 | UR-002 | Performance | Cot fit | The inner width at the narrowest point shall leave at least 75 mm a side for a 1,000 mm cot; the side walls shall cover the head and body of a 1.9 to 2.0 m cot | 1,150 | minimum | mm | Analysis (CAL section 2); inspection with three cot types at TRL 4 | Met on paper (1,170) |
| PR-003 | UR-003 | Performance | Visual privacy lying down | Wall top at least 1,200 mm above the floor, so a lying patient's chest is hidden from a standing adult 1 m from the wall | 1,200 | minimum | mm | Analysis (CAL section 4); sightline check V4 at TRL 4 | Met on paper (1,212.5); seated head shows (D3) |
| PR-004 | UR-004 | Usability | Observation | Every patient shall be seen from the open foot end; layout rule: foot ends face the nurse station | 100 | minimum | % of beds | Analysis (CAL section 4); night round V4 | Met by design (foot end); side view limited |
| PR-005 | UR-005 | Performance | Contact and splash boundary | The walls shall intercept straight-line paths from the mouth of a lying patient in the horizontal plane | 80 | minimum | % of directions | Analysis (CAL section 6); splash marks in V1 | Met on paper (84.9) |
| PR-006 | UR-006 | Safety | Head release | Staff shall open the head for resuscitation with no tool, nothing lifted or slid, within the target | 30 | maximum | s | Timed drill V2 at TRL 4 | To verify at TRL 4 (estimate 8 to 20) |
| PR-007 | UR-007 | Safety | Stability against a push | The pod shall not tip under the 178 N BIFMA X5.6 push at the wall top less 102 mm | 178 | minimum | N | Analysis (CAL section 7); T7 at TRL 4 | Not met (free end about 11 N; D5) |
| PR-008 | UR-008 | Safety | Fire | Sheet bought as FXP-S4FR with NFPA 701 TM1 and ASTM E84 Class A reports; pods never touch; no ignition sources in or on a pod; fire case accepted by the site | 0 | none | ignition sources | Inspection of reports; T8; bed-and-pod test to decide (D7) | At risk (201 MJ beside a 144 MJ mattress) |
| PR-009 | UR-009 | Environment and durability | Heat | The top shall stay open over the whole cot so the patient's plume leaves freely | 2.0 | minimum | m2 open top | Analysis (CAL section 5); V3 thermal test | Met on paper (2.42); air movement to verify |
| PR-010 | UR-010 | Maintenance | Cleanable surfaces | All faces toward the patient are print faces with sealed edges and holes; joint slits covered; clips and channels removable for cleaning | 0 | none | open crevices facing the patient | Inspection; FXP-PLT-001 T4 and T6 | Met by design; to verify at TRL 4 |
| PR-011 | UR-011 | Logistics | Pack and carry | Folded panels stack to the target and the kit is carried by one person | 100 | maximum | mm | Analysis (CAL section 3); inspection | Met on paper (40 mm; 7.4 kg) |
| PR-012 | UR-012 | Environment and durability | Deployment cycles | Folds, clips and pins shall keep their function over the target cycles | 50 | minimum | cycles | FXP-PLT-001 T2 and T3 at TRL 4 | To verify at TRL 4 |
| PR-013 | UR-013 | Cost | Parts cost | Parts cost at prototype quantities, reported against the value-engineering target | 120 | target | USD | BOM (CAL section 11) | Over target (USD 214.00) |
| PR-014 | UR-014 | Logistics | Footprint | The pod with its cot and head clearance shall fit a 2.5 m bed pitch | 2,500 | maximum | mm pitch | Analysis (CAL section 10) | Met on paper (2,087 with outriggers); 38 % fewer beds than plain cots |
| PR-015 | UR-015 | Usability | Open pod | Open top and open foot end; a seated patient can see out | 1 | minimum | open sides | Inspection; acceptance V4 | Met by design; acceptance to verify |
| PR-016 | UR-016 | Regulatory | Claims | All documents and on-product wording follow FXS-CLM-001 and STANDARDS 25.5b | 0 | none | banned claims | Inspection (render.py --check) | Met by design |
| PR-017 | UR-017 | Safety | Egress | The open foot end shall be wider than the widest cot in range so the occupied cot can be pulled out | 1,000 | minimum | mm | Analysis (CAL section 2); egress drill V2 | Met on paper (1,170 at the folds) |
| PR-018 | UR-007 | Safety | Not a handhold | Both side walls carry a prohibition sign and words against leaning or pulling, 700 to 900 mm above the floor | 2 | minimum | signs | Inspection; comprehension in V4 | Met by design; does not close the hazard (D2) |
| PR-019 | UR-007 | Safety | Free-edge stiffness | Each free wall edge is held straight by an edge stiffener so the terminal leaf is held on both edges | 2 | minimum | stiffeners | Analysis (CAL section 7); T1 hot at TRL 4 | Met on paper (margin 2.4 hot, load factor 2) |
| PR-020 | UR-006 | Safety | Head clearance | 0.6 m kept clear behind the head wall | 600 | minimum | mm | Inspection of the ward layout | Met by design (layout rule) |

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
