---
doc_id: FXS-CAL-001
title: FlexSleep Origami Patient Pod sizing and first-principles checks
project: FlexSleep Origami Patient Pod
doc_type: Calculation note
version: "0.2"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First sizing note for FS1 from the model (geometry, mass, sightlines, plume, droplet screen, stability, fire, times, density, cost) and first figures for FS2 and FS3
  - version: "0.2"
    date: 2026-11-12
    author: Amish Chadha
    change: After the independent review, head swings open with no centre foot (four feet), edge channels, joint strips, footprint with the cot and head clearance, oxygen enrichment, clip lever arm, outrigger bending, tent gusts and the terminal-leaf factor without a load factor
---

# FlexSleep Origami Patient Pod sizing and first-principles checks

Every number here comes from `docs/04-calcs/sizing.py`, which reads the model (`cad/src/model.py`) and the BOM and writes `docs/04-calcs/sizing_results.json`. The pod is an open-top, open-ended boundary of four P12 duos: a 1,487 x 1,913 mm plan on its joint lines, 1,212.5 mm tall, about 7.4 kg to carry and 26.6 kg standing with 20 kg of site-filled sand. These are first-order screens for TRL 3; FXS-VER-001 lists the TRL 4 tests that confirm them. CONCEPT, NOT FOR FABRICATION.

Release limitation (STANDARDS 25.5b): no prototype is used in patient care until its stability, fire performance, cleanability and the procedure it embeds are reviewed by qualified IPC and safety staff.

## 1. Inputs and assumptions

Cited inputs (all checked 2026-11-12; links in FXS-STM-001): FXP-PLT-001 figures (0.70 kg/m2, 39.7 MJ/kg, 178 N BIFMA push, 5.8 N for 25 mm of leaf bow, 176 N per clip, flat-strip h_cr 1,441 mm cold and 1,144 mm hot, leaf margin 3.1 and 1.6 at 1.8 m); metabolic rates 72, 81 and 108 W (ASHRAE Fundamentals via EnergyPlus); ANSUR II eye heights; PET 21.43 MJ/kg (UQ); solid foam mattress 7.3 kg, 19.68 MJ/kg, 917 kW peak (CBUF via NCFS); hand load in sit-to-stand 20 to 41 % of body weight (Bolli et al.); ADA 609.8 grab bar 1,112 N; MSF 4 m2 per bedridden patient; 2.5 m bed pitch (Bettercare); Xie et al. droplet distances; Kofoed and Nielsen plume relation; Messer 23.5 % oxygen threshold.

Assumptions: A1 patient 70 kg; A2 mouth 720 mm above the floor, 470 mm from the head line; A3 printed foot block at 45 % of solid mass; A4 friction 0.4 to 0.6 for EPDM on vinyl or tent floor; A5 radiative share 0.3 of a mattress fire; A6 empty bag 0.10 kg, carry bag 0.8 kg; A7 action times (set a foot 10 to 20 s, stand a duo 20 to 40 s, one clip 10 to 20 s, lay a bag 10 to 20 s, check 30 to 60 s); A8 release 3 to 8 s per clip and 2 to 4 s to swing the head open; A9 75 mm hand gap a side; A10 whole metabolic heat as convective, source diameter 0.4 m; A11 half of a 1.2 m foot aisle per pod; A12 FR coated fabric 0.45 kg/m2; A13 0.6 m clear behind the head; A14 oxygen 5 to 15 L/min at 93 to 100 %.

## 2. Geometry and fit (PR-002, PR-017)

Each half is a P12 duo folded 60 deg at the head corner and a second duo on a 150 deg angle joint; the head leaves meet at the centre at 15 deg to the head line. Inner width is 1,170 mm at the folds and 1,483 mm at the joints; the side walls run 1,913 mm from the head line. Cots of 600, 750, 850 and 1,000 mm leave 285, 210, 160 and 85 mm a side; a 1.9 m cot set 260 mm from the head line overhangs the open end by 247 mm. The open foot end (1,170 mm at the folds) passes every cot in range, so an occupied cot can be pulled straight out (PR-017).

## 3. Mass and pack (PR-011)

Table 1. Mass of one pod (FS1).

| Item | Mass (kg) |
| --- | --- |
| Four P12 duos at 0.70 kg/m2 | 4.03 |
| Six angle clips (PETG, solid) | 0.38 |
| Four foot blocks (printed, 45 % of 0.52 kg solid) | 0.93 |
| Four outriggers, pins, pads | 0.24 |
| Two edge channels, nine joint strips, prints | 0.63 |
| Four empty bags and the carry bag | 1.2 |
| Carried | 7.4 |
| Site-filled sand, four bags | 20.0 |
| Standing | 26.6 |

Folded duos are about 10 mm each (FXP-PLT-001 section 11): 40 mm for four, inside the 100 mm the deck allows; feet, outriggers and clips travel in the bag pocket.

## 4. Sightlines (PR-003, PR-004)

Hidden depth behind a wall of top h for an eye e at distance a: b = a (h - z) / (e - h). With h = 1,212.5 mm, a chest at 810 mm and a face at 720 mm:

Table 2. Depth behind the wall that a standing person cannot see (m).

| Observer | At 0.3 m, chest / face | At 0.5 m | At 1.0 m |
| --- | --- | --- | --- |
| Woman, 5th percentile (eye 1,421 mm) | 0.58 / 0.71 | 0.97 / 1.18 | 1.93 / 2.36 |
| Man, 95th percentile (eye 1,753 mm) | 0.22 / 0.27 | 0.37 / 0.46 | 0.74 / 0.91 |

The face lies 0.58 m from the wall: hidden from most of the aisle, seen by a tall person within 0.64 m. Seated on the cot, eyes are at 1,148 to 1,310 mm, -64 to +98 mm about the top: a seated patient's head shows (PR-003 holds for lying only). Staff observe from the open foot end (PR-004).

## 5. Air, plume and oxygen (PR-009)

Openings: top 2.42 m2, foot end 1.78 m2, perforated band 0.05 m2 (40 holes of 40 mm), so the band is 1.2 % of the openings. Plume G = 0.005 Q^(1/3) (y + d)^(5/3), y = 0.40 m to the wall top: 51.9 m3/h at 4.1 K (sleeping), 54.0 m3/h at 4.5 K (reclining), 59.4 m3/h at 5.4 K (seated). Excess oxygen mixed into that flow gives 21.3 to 22.2 % at 5 to 15 L/min and up to 23.6 % at 15 L/min with half the exchange, at the 23.5 % threshold; local enrichment in bedding is higher.

## 6. Droplet screen (PR-005)

Straight lines from the mouth, traced against the walls (12.5 to 1,212.5 mm), the cot plane, the open top and the open foot end, over a sphere of directions: walls 47.7 %, cot and body 26.4 %, open top 22.4 %, foot end 3.5 %. In the horizontal plane the walls take 84.9 %. A 30 deg cone round the vertical leaves through the top in full. Side walls 0.58 to 0.74 m from the mouth, head wall 0.45 m. The 11.6 mm slit at each angle joint is covered (F8). This is geometry, not aerosol transport.

## 7. Stability (PR-007, PR-018, PR-019)

Rigid-body tipping about the outrigger tips (FXP-PLT-001 P6 and P7 method), push at 1,110.5 mm:

Table 3. Tipping and pull figures.

| Case | Force (N) |
| --- | --- |
| Whole pod as one rigid body, outward | 239 |
| Free end of a side wall, outward / inward | 11 / 9 |
| A half alone, outward / inward | 22 / 16 |
| Sliding of the whole pod, mu 0.4 to 0.6 | 102 to 153 |
| Patient pull to stand, 20 to 41 % of 70 kg | 137 to 281 |
| Top clip at a side joint, half to all of that pull | 56 to 231 |
| Gust on a side duo at 2, 3, 5 m/s | 3.5, 7.8, 21.6 |

The zigzag is soft in torsion, so the local figures govern; the platform push and a patient's pull both fail (PR-007 not met). The outrigger under its bag carries 6.4 N m: 11.3 MPa in its skins against 24 MPa yield. The free-edged terminal leaf has a raw self-weight factor of 1.73 cold and 0.87 hot; held by its edge channel the leaf margin is 4.7 cold and 2.4 hot with the load factor of 2, about 1.4 with creep at 0.3 (PR-019).

## 8. Fire (PR-008)

Sheet 5.92 m2 at 27.8 MJ/m2: 165 MJ; PETG 28 MJ; bags 9 MJ; 201 MJ per pod against 144 MJ for a solid foam mattress (1.4 times). Point-source flux 25 kW/m2 out to 0.94 m and 10 kW/m2 to 1.48 m from a 917 kW mattress; flame height about 2.2 m. At a 2.5 m pitch the neighbour's wall is 1.76 m from the bed centre (about 7.1 kW/m2 from the mattress) and 1.01 m from the burning pod's wall.

## 9. Deployment and access (PR-001, PR-006, PR-020)

One person, empty cot, bags pre-filled: 4.2 to 8.3 min. Head release: two clips and the swing, 8 to 20 s; each head leaf opens a 0.85 m chord; 0.6 m clear behind the head. For full access the occupied cot is pulled about 1.1 m out of the open end.

## 10. Density (PR-014)

Footprint 2.09 x 2.86 m with outriggers, a 2.0 m cot and the head clearance (5.97 m2), 7.22 m2 with half an aisle: about 6.2 pods in a 45 m2 tent against 10 plain beds. At a 2.5 m pitch the outrigger tips stand 413 mm apart at floor level.

## 11. Cost (PR-013)

Value-engineering target: USD 120. Estimated cost of the constructable design: USD 214.00 at prototype quantities (USD 94.00 over the target), USD 4.28 a deployment over 50. Drivers: sheet USD 90, freight share USD 25, carry bag USD 20, foot blocks USD 18.60. The cash outlay for a first prototype is about USD 600 (ten sheets minimum plus freight), shared across pods.

## 12. Other options

FS2: 11.9 kg, seven posts, 1.75 m, a side frame tips at 3.5 N bare and 12.4 N with 10 kg of bags; two retail screens USD 421.58. FS3: 2.4 kg, screen to 1,200 mm and 700 mm along each side. P18 variant: panels 6.05 kg from four sheets; a free-edged P18 leaf fails cold.

## 13. Requirements met by design, not by calculation

- PR-010 cleanable surfaces: print faces toward the patient by the build direction of both halves; grooves face the aisle; joint strips and clips removable (FXS-STM-001 S28).
- PR-012 deployment cycles: folds of 60 and 30 deg are inside the platform's 90 deg range; cycles to FXP-PLT-001 T2 and T3.
- PR-015 open pod: open top 2.42 m2 and foot end 1.78 m2 (section 5).
- PR-016 claims: wording follows FXS-CLM-001; `render.py --check` enforces the infection claims rule.

## Where the numbers come from

`docs/04-calcs/sizing.py`, `docs/04-calcs/sizing_results.json`, `cad/src/model.py`, `bom/bom.csv`, FXP-PLT-001.

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
