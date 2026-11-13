---
doc_id: FXS-VER-001
title: FlexSleep Origami Patient Pod verification plan
project: FlexSleep Origami Patient Pod
doc_type: Verification plan
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First verification plan, TRL 4 test families on paper only
---

# FlexSleep Origami Patient Pod verification plan

Planned TRL 4 test families, on paper only; none has been run and no prototype exists. Platform tests T1 to T8 are in FXP-PLT-001 section 14.

Release limitation (STANDARDS 25.5b): no prototype is used in patient care until its stability, fire performance, cleanability and the procedure it embeds are reviewed by qualified IPC and safety staff.

| Test | What it measures | Method | Gate evidence | Closes |
| --- | --- | --- | --- | --- |
| V1 Particle exchange (decision gate) | Particle and tracer transfer from a simulated patient to the next bed, pod against an unshielded baseline; splash marks | Breathing and coughing manikin on a cot, particle counters at the next bed's breathing zone and at the staff position, at two ventilation patterns, repeated | A measured reduction with its uncertainty, or none | S1, S2, S42, PR-005 |
| V2 Drills | One-person set-up; head release; occupied-cot pull-out; egress | Untrained volunteers, timed, gloved, with a resuscitation lead watching | Set-up under 5 min; release under 30 s; cot clears the pod | S17, S19, S24, PR-001, PR-006, PR-017 |
| V3 Thermal | Air temperature and speed at the patient inside and outside the pod, with and without a fan, at 30 to 35 C | Heated manikin of 72 to 108 W | Difference in operative temperature | S4, S44, PR-009 |
| V4 Users | Acceptance, privacy, sign comprehension, night observation | Patients and staff with a field partner | Ratings and misreads | S5 to S7, S11, S33, S34, S50 |
| V5 Pull and push | Wall response to a patient's pull and the BIFMA push, with the edge channels | Force gauge at 700 to 1,100 mm | Tipping force and deflection | S10, S11, S13, PR-007 |
| V6 Fire | Bed-and-pod burn and NFPA 286 (if D7 asks) | Test house | Heat release, spread, drip | S20, S21, PR-008 |

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
