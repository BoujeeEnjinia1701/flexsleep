# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2026 Design Molecule Labs with Helpful Engineering
"""FlexSleep Origami Patient Pod: STEM check calculations (FXS-STM-001, STANDARDS sections 20 and 25.6a).

Run from the repo root:  python docs/04-calcs/sizing.py      (writes sizing_results.json)
                         python docs/04-calcs/stem_check.py  (writes stem_results.csv, stem_results_options.csv and
                                                              refreshes the two tables in docs/01b-stem-check.md)
Rows S1 onward check the carried option FS1 (the team's origami pod, iteration 2, as made constructable here).
Rows X1 onward check FS2 (fabric screen on a pole frame), FS3 (cot-mounted head-end screen) and the P18 variant.
Platform claims (sheet, clips, folds, disinfection, fire grade) are checked once in FXP-PLT-001 (rows P1 to P40) and
are cited here, not repeated. Sources and dates checked (2026-11-12) are in FXS-STM-001 and FXS-CAL-001.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src")]
from stem_check import Check, WITHIN, PLAUSIBLE, FIX, FAILS  # noqa: E402,F401
import model as M  # noqa: E402

P = M.PARAMS
R = json.loads((ROOT / "docs/04-calcs/sizing_results.json").read_text())
CAL, PLT, REV = "FXS-CAL-001", "FXP-PLT-001", "independent review 2026-11-12"
c = Check(ROOT / "docs/04-calcs/stem_results.csv")
x = Check(ROOT / "docs/04-calcs/stem_results_options.csv")
g, a, th, dg, tp, fi, ac = R["geometry"], R["air"], R["thermal"], R["droplet_geometry"], R["tip"], R["fire"], R["access"]
sg, ms, co, de = R["sight"], R["mass"], R["cost"], R["density"]

# ---- separation, droplets and aerosols ----------------------------------------------------------------------------
c.cited("S1", "A 1.2 m three-sided pod with an open top is a physical boundary against direct contact and against large droplets thrown sideways "
        "from a patient lying on the cot", "Biology", "Epidemiology",
        f"Xie et al. 2007: droplets larger than 60 to 100 um fall before they evaporate over 2 m; exhaled at 1 m/s (breathing) they travel under 1 m, "
        f"at 10 m/s (cough) more than 2 m (for a source about 1.5 m up). Straight-line screen from the mouth ({CAL} section 6; mouth 720 mm up, A2), "
        "rays traced to the walls, the cot plane, the open top and the open foot end",
        f"The side walls stand {dg['side_wall_m']} to {g['inner_w_max_mm'] / 2000:.2f} m from the mouth and the head wall {dg['head_wall_m']} m (perpendicular): "
        f"they stop {dg['horizontal_share_blocked_pct']} % of horizontal directions, where a cough or sneeze goes when the patient turns on their side, and "
        f"{dg['wall']} % of all directions; {dg['top']} % leave through the open top, {dg['foot end']} % through the open foot end and {dg['cot or body']} % "
        f"meet the cot and body. Lying on the back, a cough points up: all of a 30 deg cone round the vertical leaves through the top "
        f"({dg['up_30deg_cone_to_top_pct']} %). The {dg['joint_slit_mm']} mm slit at each angle joint was a direct path 0.45 m behind the head ({REV}: "
        "weak); now covered (F8). A boundary against contact and sideways large droplets only", WITHIN,
        closed_by="FXS-DEC-001 F8; FXS-CLM-001 (may claim); V1 at TRL 4 records splash marks")
c.cited("S2", "The pod gives a measurable reduction in airborne particle exchange with the next bed (team assumption and decision gate)", "Biology",
        "Epidemiology",
        "Rooney et al. 2021 review: 'limited evidence to support the use of 2 metres physical distancing and partition screens within healthcare'; King et "
        "al. predicted halved deposition downstream of a partial partition in one direction only; Gilkeson et al. found partitions may raise exposure near "
        "the source and for simulated health workers; partitions should exceed the breathing zone (30 cm hemisphere in front of the face) of both users. "
        "Ching et al.: full curtains lowered the next-bed bioaerosol from 11,503 to 3,782 cfu/m3. Li et al. 2021: dividers cut face-to-face exposure 99 % "
        "but side by side only 22.6 % (p = 0.49). Closed curtains 'may reduce but not eliminate' transfer (Clinical Infectious Diseases 2022, ACP Hospitalist summary)",
        "Particles under about 60 to 100 um follow the room air. A supine patient's breathing zone points up through the open top, so the pod does not "
        f"exceed it ({REV}: quote corrected, King and Gilkeson added). The effect may be small, zero or negative where ward air runs along the beds; "
        "unproven, not promised. Only the decision-gate test against an unshielded baseline can show it; nothing is claimed until then", PLAUSIBLE,
        closed_by="V1 decision-gate test (FXS-VER-001); FXS-CLM-001 (may claim only after testing)")
c.cited("S3", "Perforated lower band and open top keep passive airflow (team deck)", "Physics", "Fluid mechanics",
        f"Opening areas from the model: open top {a['open_top_m2']} m2, open foot end {a['open_end_m2']} m2, {a['perf_holes']} holes of 40 mm "
        f"({a['perf_m2']} m2) at 350 mm",
        f"The perforations are {a['perf_share_pct']} % of the openings and sit below the cot top, so the top and the foot end do all the work; the band adds "
        "40 sealed hole edges to clean and cuts the leaf where its self-weight load is highest. The airflow claim holds without the band; keeping or "
        "dropping a team feature is Amish's call", FIX, closed_by="Proposed, awaiting Amish: FXS-DEC-001 D4 (recommend drop)")
c.cited("S4", "A person inside does not suffer heat build-up in a warm climate (metabolic heat 72 to 108 W)", "Physics", "Heat transfer",
        "ASHRAE Fundamentals metabolic rates (sleeping 72 W, reclining 81 W, seated 108 W for 1.8 m2, via the EnergyPlus reference); point-source plume "
        f"G = 0.005 Q^(1/3) (y + d)^(5/3) (Kofoed and Nielsen 1988), whole heat taken as convective (A10, overstates the plume temperature), d 0.4 m, rise "
        f"{th['y_rise_m']} m to the wall top",
        f"The plume carries about {th['plume']['sleeping']['m3h']} to {th['plume']['seated quiet']['m3h']} m3/h out of the open top at "
        f"{th['plume']['sleeping']['dT_K']} to {th['plume']['seated quiet']['dT_K']} K above the ward: heat is not trapped under a lid. The point-source "
        f"formula for a lying body is an estimate, and plume flow is entrainment, not a measured exchange of the pod ({REV}: weak). A febrile patient "
        "makes more heat. What the walls take away is sideways air movement (draught or fan) that cools a patient in a hot ward; that is S44", PLAUSIBLE,
        closed_by="V3 thermal comfort test at TRL 4 (FXS-VER-001)")
# ---- privacy, observation, fit ----------------------------------------------------------------------------------
sw, sm = sg["standing"]["woman 5th"], sg["standing"]["man 95th"]
sw, sm = sg["standing"]["woman 5th"], sg["standing"]["man 95th"]
c.cited("S5", "A patient lying in the pod is hidden from people walking past at 0.7 m or more from the wall", "Biology", "Human physiology and biomechanics",
        f"Sightline over a {sg['wall_top_mm']:.0f} mm wall top: hidden depth b = a (h - z)/(e - h); ANSUR II standing eye heights 1,421 to 1,753 mm (NCSU); "
        "chest under bedding at 810 mm, face at 720 mm",
        f"At 1 m from the wall the chest is hidden for {sm['at 1.0 m']['body_m']} to {sw['at 1.0 m']['body_m']} m behind it and the face for "
        f"{sm['at 1.0 m']['face_m']} to {sw['at 1.0 m']['face_m']} m, against {sg['face_from_wall_m']} m to the face. A 95th percentile man sees the face "
        f"from within {sg['tall_sees_face_within_m']} m of the wall, and in the 1.01 m gap between pods at a 2.5 m pitch people pass about 0.5 m from each "
        f"wall, where the face is hidden only {sm['at 0.5 m']['face_m']} m deep ({REV}: weak, restated). Visual privacy only, lying down, from most of the "
        "aisle", WITHIN, closed_by="PR-003; FXS-CLM-001 (restated)")
c.cited("S6", "The pod gives privacy to a patient sitting up on the cot", "Biology", "Human physiology and biomechanics",
        f"Seated eye height above the seat 698 to 860 mm (ANSUR II); seat on the cot canvas about {P['COT_TOP'] - 50:.0f} mm",
        f"Seated eyes are at {sg['seated_eye_mm'][0]:.0f} to {sg['seated_eye_mm'][1]:.0f} mm, {sg['seated_eye_above_top_mm'][0]} to "
        f"+{sg['seated_eye_above_top_mm'][1]} mm about the wall top: a seated patient's head is seen and sees out. The team claim fails as stated and is "
        f"restated as privacy lying down; restating a user-facing claim is Amish's ({REV}: label corrected)", FIX,
        closed_by="Proposed, awaiting Amish: FXS-DEC-001 D3 (height and claim)")
c.cited("S7", "Staff can observe the patient without entering the pod (team deck: semi-transparent upper panels)", "Biology",
        "Human physiology and biomechanics", f"Same sightline at 0.3 m from the wall; face {sg['face_from_wall_m']} m from the wall; P12 has no upper panel",
        f"From the open foot end, everyone sees the patient. From the side, a staff member at 0.3 m from the wall sees the face only if tall: the hidden "
        f"depth is {sm['at 0.3 m']['face_m']} m for a 95th percentile man and {sw['at 0.3 m']['face_m']} m for a 5th percentile woman. The team's "
        "semi-transparent upper panels are not in FS1; observation from the foot end only is a real limit on spotting a patient getting worse, so foot ends "
        f"must face the nurse station (S50) ({REV}: weak, label corrected). Frosted or mesh panels need a P18 wall and their own fire report (X11)", FIX,
        closed_by="Proposed, awaiting Amish: FXS-DEC-001 D3")
c.cited("S8", "The pod fits cots 60 to 100 cm wide (team deck)", "Mathematics", "Units and dimensional analysis",
        "Inner width from the model; MSF field hospital bed 190 to 200 x 75 to 85 cm, lying surface 50 to 55 cm; NATO style camp bed 190 x 64 x 40 cm; "
        "US style military cot 78 x 28 x 18 in; hand and bedding gap 75 mm a side (A9)",
        f"Inner width {g['inner_w_min_mm']:.0f} mm at the folds, {g['inner_w_max_mm']:.0f} mm at the joints: gaps of {g['clear_each_side_mm']['600']:.0f}, "
        f"{g['clear_each_side_mm']['750']:.0f}, {g['clear_each_side_mm']['850']:.0f} and {g['clear_each_side_mm']['1000']:.0f} mm a side for cots of 600, "
        f"750, 850 and 1,000 mm, so the widest cot fits with {g['clear_each_side_mm']['1000']:.0f} mm. The fit is by clearance, not by adjustment; no "
        "staff member can stand inside beside any of them (S21)", WITHIN, closed_by="PR-002")
c.cited("S9", "The pod covers a cot 190 to 200 cm long", "Mathematics", "Units and dimensional analysis",
        f"Side wall {g['side_len_mm']:.0f} mm from the head line; cot head {P['COT_Y0']:.0f} mm from it",
        f"A 1.9 m cot overhangs the open end by {g['cot_overhang_mm']:.0f} mm and a 2.0 m cot by {g['cot_overhang_mm'] + 100:.0f} mm: head and body are inside, "
        "the feet outside", WITHIN, closed_by="PR-002")
# ---- stability -------------------------------------------------------------------------------------------------
c.cited("S10", "The pod does not tip when pushed from the aisle with the 178 N BIFMA X5.6 force", "Physics", "Mechanics and statics",
        f"{PLT} P6, P7 method: rigid-body tipping about the outrigger tips, push at {tp['z_push_mm']:.0f} mm (102 mm below the top); masses from the model "
        f"with four 5 kg bags ({tp['pod_kg']} kg standing)",
        f"As one rigid body the pod would hold {tp['out_side_N']:.0f} N, but it is not one: the zigzag side wall is soft in torsion and a 600 mm leaf bows "
        f"25 mm at {tp['leaf_25mm_N']} N ({PLT} P4). Locally the free end of a side wall tips at about {tp['free_end_out_N']:.0f} N. The bag sits 135 mm "
        f"inside the outrigger tip, so it adds little against outward tipping ({REV}: holds). Proposed fix: state the platform limit L1 (a boundary that "
        "tips if leant on) with a lower lateral criterion; more ballast does not close it", FIX,
        closed_by="Proposed, awaiting Amish: FXS-DEC-001 D5 (with FXP-PLT-001 D5)")
c.cited("S11", "A patient can pull on a panel to sit up or stand, or roll against it, without the pod tipping or folding onto them (fall risk)", "Biology",
        "Human physiology and biomechanics",
        f"Hand load in sit-to-stand with a handle 20 to 41 % of body weight (Bolli et al., one young adult; a frail patient loads the hands more); 70 kg "
        f"patient (A1); ADA 609.8 asks a grab bar for {tp['grab_bar_N']:.0f} N",
        f"Needs {tp['pull_need_N'][0]} to {tp['pull_need_N'][1]} N. A side wall pulled inward tips locally at about {tp['free_end_in_N']:.0f} N "
        f"(a released half at {tp['released_half_in_N']:.0f} N) and a 600 mm leaf bows 25 mm at {tp['leaf_25mm_N']} N, so it gives way and the patient "
        "falls; a patient rolling in rigors or delirium against a wall 0.2 m away does the same, and field cots have no rails, so the wall looks like one "
        f"({REV}: holds; the sign is the weakest control and does not close it). Fixed now: an ISO 3864 prohibition sign with the words 'Do not lean or "
        "pull. Ask staff to help you stand.' on both side walls at 700 to 900 mm (F2). Whether the pod may be used for patients who need support to stand, "
        "are delirious or are children is a scope and safety decision", FIX,
        closed_by="FXS-DEC-001 F2 (standing instruction); Proposed, awaiting Amish: FXS-DEC-001 D2")
c.cited("S12", "The pod does not slide when bumped", "Physics", "Mechanics and statics",
        f"Friction mu W of the standing pod; EPDM pad on wet to dry vinyl or tent floor mu 0.4 to 0.6 (ASSUMED, A4, to measure; wet EPDM on vinyl may be "
        f"lower; {PLT} D17)",
        f"Slides at {tp['slide_N'][0]} to {tp['slide_N'][1]} N as a whole, so the 178 N push may slide it, more so on a wet floor; a half alone tips (about "
        f"{tp['released_half_out_N']:.0f} N) before it slides ({REV}: weak, restated). A pod that slides moves toward the next bed", PLAUSIBLE,
        closed_by="FXS-DEC-001 F4 (pads, standing instruction); T7 at TRL 4")
c.cited("S13", "Clips hold the joints while a patient pulls on a wall", "Engineering and technology", "Joint design",
        f"{PLT} P9: {tp['clip_cap_N']:.0f} N per clip on paper (pull-out of two through-pegs), not bounded by test. A pull at 900 mm shared by the head "
        f"corner fold and the side joint; at the joint the top clip (1,062 mm) takes {tp['top_clip_share'] * 100:.0f} % by lever arm",
        f"About {tp['top_clip_N'][0]} to {tp['top_clip_N'][1]} N on the top clip if the fold takes half, {tp['top_clip_N'][2]} to {tp['top_clip_N'][3]} N "
        f"if the joint takes it all, which passes the paper capacity at the high end; the load is also out of plane (prying) ({REV}: weak, lever arm "
        "added). The wall gives way first (S11)", PLAUSIBLE, closed_by=f"{PLT} T3 and D14")
c.cited("S14", "The platform angle clip takes a panel in both of its slots", "Engineering and technology", "Manufacturing tolerances",
        "Interference check of the model (cad_check.py) with fx.clip('angle') as the platform helper builds it: square 12 mm core, panel edge stopped at "
        "6 mm from the joint line by the hole pattern",
        "As built, the square core stands 6 / cos 30 = 6.93 mm from the axis in the 150 deg slot, 0.93 mm proud of the stop line, so a panel cut to the "
        "platform hole pattern overlapped the core by 147 mm3 and its holes missed the pegs by 0.93 mm against 0.5 mm of clearance (fails as built). "
        "Fixed: the same arms on a 12 mm round core (F1); platform request 1", WITHIN, closed_by="FXS-DEC-001 F1 (standing instruction); REVIEW platform request 1")
ou = R["outrigger"]
c.cited("S15", "Each outrigger carries the tipping load into its foot block", "Engineering and technology", "Joint design",
        f"{PLT} section 5.4 describes the folded outrigger but not how it is held to the block. Inward tipping loads the beam as a cantilever under its "
        f"5 kg bag: M = {ou['M_Nm']} N m; skins-only thin triangle I = a^3 t / 4 = {ou['I_mm4']} mm4 (t = 2 x 0.26 mm)",
        f"A beam that only butts against the block carries no moment, so the outrigger did nothing as drawn. Fixed: a 100 mm triangular spigot on the "
        f"block, the beam slid over it and a 6 mm stainless pin across both (F3). Bending stress about {ou['stress_MPa']} MPa against a raw PP yield of "
        f"{ou['pp_yield_MPa']:.0f} MPa ({PLT}), so a factor of about 2 before local buckling of the 0.26 mm apex skin, which crush scoring weakens; pin "
        f"bearing on two skins unproven ({REV}: weak, numbers added)", PLAUSIBLE,
        closed_by="FXS-DEC-001 F3 (standing instruction); T7 at TRL 4; REVIEW platform request 2")
tl = R["terminal_leaf"]
c.cited("S16", "The terminal leaf at each open end stands under its own weight, cold and hot", "Physics", "Elastic stability",
        f"{PLT} P2 Greenhill flat strip, h_cr 1,441 mm cold and 1,144 mm hot: at 1,200 mm (h_cr / H)^3 = {tl['flat_strip_factor'][0]} cold and "
        f"{tl['flat_strip_factor'][1]} hot. These are raw factors with no load factor (platform_check.py line 143); a leaf with one free edge and no "
        f"twisting stiffness buckles like that strip. With both edges held, {PLT} P3 gives {tl['held_both_edges_margin_LF2'][0]} cold and "
        f"{tl['held_both_edges_margin_LF2'][1]} hot at 1,200 mm, load factor 2 included",
        f"First drawn with a free edge, the leaf would buckle in a hot tent (0.87) and creep toward it over weeks ({REV}: refuted; the author had read 1.73 "
        f"as including a factor of 2). Fixed: an aluminium edge channel bolted over each free edge (F7), so the leaf is held on both edges; with creep "
        f"at 0.3 of the short-term stiffness (reviewer's estimate) the margin is about {tl['held_with_creep_0p3']} with the load factor of 2 still in it", PLAUSIBLE,
        closed_by=f"FXS-DEC-001 F7 (standing instruction); {PLT} T1 hot; REVIEW platform request 3")
# ---- clinical access and egress --------------------------------------------------------------------------------
c.cited("S17", "Staff can open the pod for resuscitation within seconds (team risk; platform first-order check)", "Biology", "Ergonomics",
        "ERC 2021 BLS: 'Start chest compressions as soon as possible' and 'on a firm surface whenever feasible'; ILCOR 2024: firm surface when practical, "
        "moving a patient to the floor judged not worth its risks. Release: two clips at the head centre (two fingertips on two lips each, crouching for "
        "the low one), then both head leaves swing 90 deg outward on their corner folds (A8)",
        f"As first drawn (slide one half 0.8 m) the half, with two 5 kg bags on it, tips at about {tp['released_half_out_N']:.0f} N before it slides at "
        f"about 50 to 75 N, so it fell over instead: 30 to 60 s or a dropped wall ({REV}: refuted). Fixed (F5): no foot at the head centre, so after the "
        f"two clips are released the head leaves swing open on their folds with nothing lifted or slid: about {ac['release_s'][0]:.0f} to "
        f"{ac['release_s'][1]:.0f} s, a {ac['head_open_chord_m']} m opening on each side of the head. It needs {ac['head_clear_behind_m']} m clear "
        "behind the head wall to swing and to reach the clips (F9). For full access the occupied cot is pulled about 1.1 m out of the open foot end "
        f"({g['inner_w_max_mm']:.0f} mm wide). A field cot's canvas is not a firm surface in any case", PLAUSIBLE,
        closed_by="FXS-DEC-001 F5, F9 (standing instruction); V2 timed release at TRL 4")
c.cited("S18", "Staff reach the patient for routine care without moving a panel", "Biology", "Ergonomics",
        f"Side gap {ac['side_clear_closed_mm']:.0f} mm for a 0.75 m cot; wall top {sg['wall_top_mm']:.0f} mm; cot top {P['COT_TOP']:.0f} mm",
        "Fails: nobody stands beside the cot inside the pod, and reaching over a 1.2 m wall to a patient 0.6 m in is poor practice for handling. Routine "
        "care is from the open foot end, or with the head opened (S17), or with the cot set off centre to give one 345 mm working side. Changing the "
        "pod's width changes the plan and the bed spacing", FIX, closed_by="Proposed, awaiting Amish: FXS-DEC-001 D6")
c.cited("S19", "A patient can get out of the pod quickly, including in a fire", "Engineering and technology", "Standards practice",
        f"Open foot end {g['inner_w_max_mm']:.0f} mm wide at the joints and {g['inner_w_min_mm']:.0f} mm at the folds; side gap {ac['side_clear_closed_mm']:.0f} mm; "
        f"{PLT} section 9 keeps the open end clear",
        f"A walking patient sits on the cot's foot end and steps out of the open end, climbing over the cot end rail that stands {g['cot_overhang_mm']:.0f} mm "
        "out; nothing latches. Staff can pull the occupied cot straight out of the open end, which is wider than any cot in range ({REV}: holds, cot "
        "pull added). The narrow side gap makes sitting on the side edge awkward (falls risk); the off-centre cot of D6 helps", PLAUSIBLE,
        closed_by="V2 egress drill at TRL 4; FXS-DEC-001 D6")
# ---- fire --------------------------------------------------------------------------------------------------------
c.cited("S20", "FR twinwall panels round a sleeping patient and bedding are an acceptable fire case", "Chemistry", "Materials and polymer chemistry",
        f"{PLT} P23 and FR1 (27.8 MJ/m2; FR delays ignition, does not reduce fire load); PET 21.4 MJ/kg (UQ) for printed parts and bags; solid foam mattress "
        f"with FR cover 7.3 kg, 19.7 MJ/kg, peak {fi['mattress_peak_kW']:.0f} kW (CBUF item 1:21, NCFS table, an upper value); point-source radiation with "
        "a radiative share of 0.3 (ASSUMED, A5); Heskestad flame height L = 0.235 Q^(2/5) - 1.02 D; PP ignited and burned in the cone at 25 kW/m2 (FSRI)",
        f"The pod adds {fi['total_pod_MJ']:.0f} MJ ({fi['pod_MJ']:.0f} MJ of sheet) beside a {fi['mattress_MJ']:.0f} MJ mattress, {fi['ratio_pod_to_mattress']} "
        f"times the bed's own load. The mattress flame is about {fi['flame_height_m']} m high, so walls 0.2 to 0.4 m away stand in or against it and will "
        "burn, melt and drip whatever their grade; three walls also re-radiate onto the bed and channel the flame. NFPA 701 TM1 (the platform minimum, a "
        f"curtain test) does not show behaviour beside a burning bed ({REV}: holds, stronger by flame height). Rules now: pods never touch (F6), no heat "
        "sources, lamps, candles, coils or chargers in or on a pod. No fix within the principle makes this acceptable on paper: the benchmark, a full-scale "
        "bed-and-pod test and whether the risk is accepted are Amish's, with the site's fire safety staff", FIX,
        closed_by="FXS-DEC-001 F6 (standing instruction); Proposed, awaiting Amish: FXS-DEC-001 D7 (with FXP-PLT-001 D18)")
c.cited("S21", "Pods next to each other do not carry a fire from bed to bed", "Physics", "Heat transfer",
        f"Bed centre spacing 2.5 m in general wards (Bettercare IPC facility design, section 5-5); pod width {g['outer_w_m']} m on its joints; same point-source "
        "screen for the mattress",
        f"At a 2.5 m pitch the neighbour's wall stands {fi['neighbour_wall_from_bed_m']} m from the burning bed's centre line, where the mattress alone gives "
        f"about {fi['q_neighbour_from_mattress_kW_m2']} kW/m2. The larger threat is the burning pod's own 1.9 x 1.2 m walls, {fi['gap_between_pods_at_2p5m_m']} "
        f"m from the neighbour's wall: the reviewer estimates 15 to 25 kW/m2 there (view factor about 0.25, emissive power assumed) ({REV}: weak, distances "
        "corrected). Closer pitches make it worse. Spacing is a site rule set with fire safety staff (D7)", PLAUSIBLE,
        closed_by="FXS-DEC-001 F6; D7; T8 at TRL 4")
o2 = th["oxygen_pct"]
c.cited("S22", "Oxygen given to a patient inside a pod does not raise the fire risk", "Chemistry", "Physical chemistry",
        "Messer safety alert: oxygen-enriched air is more than 23.5 % O2; bedding and clothing enriched with oxygen become 'extremely flammable'. Excess "
        "oxygen at 5 to 15 L/min (ASSUMED, A14), 93 to 100 % purity, mixed into the plume exchange flow of S4, and into half of it",
        f"Bulk pod air reaches {o2['5 L/min, exchange x 1.0'][0]} to {o2['15 L/min, exchange x 1.0'][1]} % with the full exchange and up to "
        f"{o2['15 L/min, exchange x 0.5'][1]} % at 15 L/min with half of it, at the 23.5 % threshold. Oxygen is denser than air and soaks into bedding, so "
        f"local enrichment at low level inside three walls is the real hazard ({REV}: weak, quantified). Rule now: no cylinders or concentrators inside or "
        "fixed to the pod; tubing taken out over the nearest wall top, clear of the head release joint (F6); oxygen patients in a pod only after the site's "
        "fire review", PLAUSIBLE, closed_by="FXS-DEC-001 F6; site fire review (release limitation)")
c.cited("S23", "Smoke from the FR sheet is no worse than other FR plastics in a sleeping space", "Biology", "Toxicology",
        f"{PLT} P37 and D11: brominated FR with antimony trioxide; combustion products include hydrogen bromide and antimony oxides",
        "To assess with the halogen-free FR question; a sleeping patient is the worst case for smoke exposure", PLAUSIBLE, closed_by=f"{PLT} D11")
# ---- deployment, pack, durability, cleaning ---------------------------------------------------------------------
dm = R["deploy_min"]
dm = R["deploy_min"]
c.cited("S24", "One person with no training deploys the pod around a cot in under 5 minutes (team deck)", "Biology", "Ergonomics",
        "Step count from the model (4 feet with pre-pinned outriggers and bonded pads, 4 duos, 6 clips, 4 filled bags, one check) x ASSUMED action times (A7)",
        f"{dm[0]} to {dm[1]} min with the bags already filled and staged and the cot empty: the fast end meets 5 min, the slow end does not. Filling 20 kg of "
        "sand is a separate depot task. Around an occupied cot the cot is pulled about 0.5 m forward and back, a two-person handling task with a line-pull "
        f"risk ({REV}: weak). One person can do the rest because a folded duo stands alone as an L before it is clipped", PLAUSIBLE,
        closed_by="V2 timed deployment at TRL 4")
c.claim("S25", "All panels stack to 10 cm or less for storage (team deck)", "Mathematics", "Units and dimensional analysis",
        f"{PLT} section 11: a folded duo is about 10 mm thick; four duos", R["pack"]["panels_mm"], 100.0, "mm", rule="below",
        closed_by="Feet, outriggers and clips pack in the bag pocket (BOM item 9)")
c.claim("S26", "One person carries the folded pod kit", "Biology", "Ergonomics",
        f"Carried mass from the model with bags empty (A6); NIOSH load constant 23 kg as a ceiling only ({PLT} P16)", ms["carried_kg"], 23.0, "kg",
        rule="below", closed_by=f"PR-011; 25 kg of sand filled on site, never carried ({PLT} B1)")
c.cited("S27", "Panels, clips, feet, pins and channels tolerate 0.5 % hypochlorite and 70 % alcohol wipes", "Chemistry", "Materials and polymer chemistry",
        f"{PLT} P18 to P20 for PP and PETG; EPDM, stainless and aluminium not on those charts",
        f"Pins and bolts changed from A2 to A4 (316) stainless for repeated hypochlorite wipes; PETG tongues under strain may craze with alcohol (stress "
        f"cracking); aluminium channels are rinsed after chlorine ({REV}: weak, A4 adopted). All to the T4 coupons", PLAUSIBLE, closed_by=f"{PLT} T4")
c.cited("S28", "Every surface facing the patient can be wiped", "Biology", "Microbiology",
        f"{PLT} rules E1 to E3; back-face fold grooves; 40 perforation holes; the angle-joint slits",
        "Print faces (no grooves) face the patient in both halves, so every groove faces the aisle (E2); the 11.6 mm joint slits are covered by strips that "
        "come off with the clips for cleaning (F8); hot-punched hole seals cannot be checked by eye, and FDM layer lines and clip interiors are crevices, "
        f"so clips and channels come off for cleaning (E3) ({REV}: weak). Seal integrity under wiping unproven; the perforations add 40 sealed edges (D4)",
        PLAUSIBLE, closed_by=f"FXS-DEC-001 F8; {PLT} T6")
c.cited("S29", "Folds and clips survive 50 deployments", "Engineering and technology", "Fatigue",
        f"{PLT} P13 and P14: the 13.6 mm groove folds to 180 deg (3.4 % skin strain) and 90 deg either way; FS1 folds 60 and 30 deg in use",
        "Inherited; the 60 deg corner fold is inside the platform's range", PLAUSIBLE, closed_by=f"{PLT} T2 and T3")
c.cited("S30", f"The prototype pod's parts cost about USD {co['bom_total']:.0f}, against the USD 120 value-engineering target", "Mathematics",
        "Orders of magnitude", "Priced BOM (bom/bom.csv), cited prices checked 2026-11-12; printed parts at filament cost",
        f"USD {co['bom_total']:.2f}, USD {co['over']:.2f} over the target (a value-engineering target, not a limit, STANDARDS 18); drivers sheet USD "
        f"{co['drivers'][0][1]:.0f}, freight share USD {co['drivers'][1][1]:.0f} and carry bag USD {co['drivers'][2][1]:.0f}. The cash outlay for a "
        f"first prototype is about USD {co['prototype_cash_usd']:.0f} (minimum 10 sheets plus freight), shared across pods ({REV}: holds, cash added). "
        "The USD 75 stretch is not shown", WITHIN, closed_by="FXS-MKT-001; value engineering in FXS-DEC-001")
c.cited("S31", "Pods fit a ward without losing many beds", "Mathematics", "Units and dimensional analysis",
        f"Footprint from the model: outriggers 300 mm out each side, the cot end of a 2.0 m cot and 0.6 m clear behind the head (F9); MSF cholera guideline "
        f"about 4 m2 per bedridden patient and 10 beds plus a nurse station per 45 m2 tent; general ward bed pitch 2.5 m (Bettercare); half a 1.2 m "
        "foot-end aisle per pod (A11)",
        f"Each pod needs {g['footprint_m'][0]} x {g['footprint_m'][1]} m ({g['footprint_m2']} m2), {de['m2_per_pod']} m2 with its aisle share: about "
        f"{de['pods_per_45m2']} pods in a 45 m2 tent against 10 plain beds, about 38 % fewer ({REV}: refuted at 'a quarter'; the cot end had been left "
        f"out). At a 2.5 m pitch the walls fit with {de['floor_gap_between_rigs_at_2p5m_mm']:.0f} mm between outrigger tips at floor level (S41); in "
        "surge wards at a tighter pitch they do not", WITHIN, closed_by="PR-014; FXS-DEC-001 D8")
c.cited("S32", "The pod is for use indoors or inside a tent", "Physics", "Fluid mechanics", f"{PLT} P8 and limit L2", "Inherited", WITHIN,
        closed_by=f"{PLT} D6 (proposed, awaiting Amish)")
c.cited("S33", "Patients accept the pod and do not find it isolating (team risk)", "Biology", "Human physiology and biomechanics",
        "Open top and foot end; seated patients see out (S6); no cited study of partial enclosures in field wards found",
        "To assess with patients and humanitarian health practitioners", PLAUSIBLE, closed_by="V4 user acceptance at TRL 4")
c.cited("S34", "Warning and release marks are read correctly", "Biology", "Human physiology and biomechanics",
        f"{PLT} C1 to C3: colour never the only code; safety colours keep their ISO 3864 meanings; ISO 7010 symbols where registered, ISO 3864-3 for custom ones",
        f"First drawn as a yellow band, but 'Do not lean or pull' is a prohibition, which ISO 3864-1 draws as a red circle and bar ({REV}: refuted). Now a "
        "prohibition sign (red circle and bar on white, custom pictogram to ISO 3864-3) with the words in black on white; release marks are black and "
        "white with words, not red; words in local languages. Comprehension unproven", WITHIN, closed_by=f"FXS-DEC-001 F2; {PLT} T5")
c.cited("S35", "Ballast does not bring wet or soiled bags onto a clinical floor", "Biology", "Microbiology",
        f"{PLT} rule B1; 25 kg of sand per pod", "Bags filled with clean sand off the clinical floor, closed and wiped; a sealed wipeable bag to source (C3)",
        PLAUSIBLE, closed_by="FXS-DEC-001 C3")
c.cited("S36", "Edges, grooves, folds and joints do not cut or pinch hands, including the patient's", "Biology", "Human physiology and biomechanics",
        f"{PLT} P34; slit at a 150 deg angle joint 2 x 6 x sin 75 = {dg['joint_slit_mm']} mm, opening and closing as the wall racks; the reviewer cites "
        "8 to 25 mm as a finger-entrapment band (ISO 13857, EN 1176; not checked here)",
        f"The slits were a finger trap within reach of a patient 0.2 m away ({REV}: weak). Fixed: cover strips on both faces (F8). Sealed edges and folds "
        "as the platform", PLAUSIBLE, closed_by=f"FXS-DEC-001 F8; {PLT} T5")
c.cited("S37", "Static charge on PP panels is acceptable next to oxygen and monitors", "Physics", "Electromagnetism and circuits",
        f"{PLT} P33 (Interprofile antistatic grade 1e9 to 1e12 ohm/sq on request; standard PP highly insulating)",
        f"Standard PP charges in dry tents; a discharge near oxygen-enriched bedding is a low-probability ignition source that is not argued away here "
        f"({REV}: weak). Anti-static FR grade availability to assess", PLAUSIBLE, closed_by=f"{PLT} P33")
c.cited("S38", "The pod supports IPC practice; it makes no claim on airborne transmission", "Biology", "Epidemiology",
        "STANDARDS 25.5b; S1 and S2", "Claims limited to a physical boundary against contact and sideways large droplets, privacy lying down and a "
        "clear bed space (FXS-CLM-001)", WITHIN, closed_by="FXS-CLM-001")

# ---- claims the independent review found missing (2026-11-12) -------------------------------------------------------
de_ = R["density"]
c.cited("S39", "The angle-joint slits do not break privacy or let droplets through", "Mathematics", "Units and dimensional analysis",
        f"Slit 2 x 6 mm x sin 75 deg = {dg['joint_slit_mm']} mm wide between and beyond the 100 mm clips at three joints, about 0.03 m2 in all",
        "A sightline and a droplet path 0.45 m behind the head as drawn first (missed claim). Fixed: flexible clear PP cover strips on both faces in three "
        "lengths per joint, heat-staked to one leaf so the head joint still releases (F8)", WITHIN, closed_by="FXS-DEC-001 F8 (standing instruction)")
c.cited("S40", "The free ends of the side walls stand in a tent with the door open or a fan running", "Physics", "Fluid mechanics",
        f"q = 0.5 rho v^2 on the two 0.6 x 1.2 m leaves of a side duo, rho 1.2 kg/m3; free end tips at about {tp['free_end_out_N']:.0f} N (S10)",
        f"Gusts of 2, 3 and 5 m/s give {tp['gust_on_two_leaves_N']['2.0 m/s']}, {tp['gust_on_two_leaves_N']['3.0 m/s']} and "
        f"{tp['gust_on_two_leaves_N']['5.0 m/s']} N, so a door gust or a pedestal fan aimed at a pod can tip a free end (missed claim). Placing pods away from "
        "tent doors and fans, or more ballast at the free ends, changes the site rules", FIX, closed_by="Proposed, awaiting Amish: FXS-DEC-001 D9")
c.cited("S41", "The aisle between pods stays clear for staff, stretchers and escape", "Engineering and technology", "Standards practice",
        f"At a 2.5 m bed pitch: walls 1.01 m apart, outrigger tips with their bags {de_['floor_gap_between_rigs_at_2p5m_mm']:.0f} mm apart at floor level; "
        "cot overhang into the foot aisle 0.25 to 0.35 m",
        "A 43 mm outrigger and a 70 mm bag at the floor are trip edges for staff carrying patients or buckets, and the clear floor between pods is narrow "
        "(missed claim). Outriggers and bags marked on the floor; side aisles are not escape routes; the foot aisle width is a site rule (D8)", PLAUSIBLE,
        closed_by="FXS-DEC-001 D8; V2 at TRL 4")
c.cited("S42", "Staff working at the open foot end are not exposed more than at an open bed", "Biology", "Epidemiology",
        "Rooney et al. 2021: partitions may raise exposure near the source and for simulated health workers (Gilkeson, Nielsen)",
        "The foot end is where staff stand, in the pod's plume and slower air (missed claim). Unknown sign and size; PPE practice unchanged", PLAUSIBLE,
        closed_by="V1 measures at the staff position at TRL 4")
c.cited("S43", "The pod works with mosquito nets over the cot (malaria settings)", "Biology", "Epidemiology",
        "Treated nets hang over and are tucked under cots; side gap 210 mm for a 0.75 m cot",
        "Hanging and tucking a net inside a 1.2 m wall with a 210 mm gap is awkward, and a net adds fire load beside the bedding (missed claim). To check "
        "with field partners", PLAUSIBLE, closed_by="V4 with field partners at TRL 4")
c.cited("S44", "Patients in a hot ward lose no cooling from fans or draughts", "Physics", "Heat transfer",
        "Walls 0.2 m from a lying patient block sideways air movement; the reviewer quotes about 2 to 3 K of comfort credit for 0.8 m/s air (ASHRAE 55 "
        "practice, not checked here)",
        "The main thermal effect of the pod is lost air movement, not trapped heat (missed claim). A ceiling fan still reaches the open top; a pedestal fan "
        "must blow into the open foot end (and S40 applies)", PLAUSIBLE, closed_by="V3 thermal comfort at TRL 4")
c.cited("S45", "Cholera cots and floor-level splash are compatible with the pod", "Biology", "Microbiology",
        "Cholera beds carry a bucket under the bed (MSF cholera guideline); feet, outriggers, bags and the 350 mm perforated band sit in the splash zone",
        "Daily chlorine mopping goes round four feet and four bags per pod, and bags soak up liquid (missed claim). For cholera use, bags in sealed wipeable "
        "covers (C3) and no perforated band (D4)", PLAUSIBLE, closed_by="FXS-DEC-001 C3, D4")
c.cited("S46", "The pod stands on uneven tent floors", "Physics", "Mechanics and statics",
        "Four rigid feet on a groundsheet over earth; 2 mm pads",
        "A high spot of 10 mm unloads a foot and its bag and the pod rocks; tipping figures fall further (missed claim). Slope and step tolerance to measure",
        PLAUSIBLE, closed_by="T7 on a 1:50 slope at TRL 4")
c.cited("S47", "Panels can be disposed of after an outbreak without harm", "Chemistry", "Environmental and atmospheric chemistry",
        f"About 4 kg of brominated FR PP and 1.3 kg of PETG per pod; {PLT} D11",
        "Contaminated panels are often burned in pits or simple incinerators, which releases hydrogen bromide and may form brominated dioxins and furans "
        "(missed claim). End-of-life route to assess with the halogen-free FR question", PLAUSIBLE, closed_by=f"{PLT} D11")
c.cited("S48", "Carers, children, IV stands and lines fit the pod", "Biology", "Ergonomics",
        "Side gap 210 mm for a 0.75 m cot; walls tip at about 10 N",
        "No room for a carer's mat or an IV stand inside; children will climb walls that tip; lines over a wall snag when the head opens (missed claim). IV "
        "stand outside at the foot end, lines kept off the walls and clear of the release joint; children in pods only by site rule", PLAUSIBLE,
        closed_by="FXS-DEC-001 D2, D6; V4 at TRL 4")
c.cited("S49", "Pests do not live in the flutes", "Biology", "Ecology and agronomy", f"{PLT} E1 seals every cut edge and hole; 4 mm flutes",
        "A failed seal opens a 4 mm channel in which bedbugs and cockroaches can live (missed claim); seals inspected at each turnaround", PLAUSIBLE,
        closed_by=f"{PLT} T6")
c.cited("S50", "Staff see every patient at night", "Biology", "Human physiology and biomechanics",
        "Observation only from the open foot end (S7)", "Layout rule: pods in rows with their foot ends facing the nurse station or a central aisle; lit "
        "foot ends (missed claim)", WITHIN, closed_by="PR-004; FXS-DEC-001 D8")
c.cited("S51", "Privacy is visual only", "Physics", "Acoustics and vibration",
        "A 1.2 m wall with an open top gives almost no sound reduction (a few dB at speech frequencies, reviewer's estimate)",
        "No acoustic privacy is claimed (missed claim)", WITHIN, closed_by="FXS-CLM-001")

# ---- other options and the P18 variant ---------------------------------------------------------------------------
f2, f3, pv = R["FS2"], R["FS3"], R["P12_vs_P18"]
x.cited("X1", "FS2: a 1.75 m fabric screen gives privacy from standing people", "Biology", "Human physiology and biomechanics",
        "ANSUR II standing eye height 1,421 to 1,753 mm", "The fabric top at about 1,550 mm hides the patient from most standing adults, and also hides "
        "the patient from staff except at the foot end", WITHIN)
x.cited("X2", "FS2: the post-and-rail screen stands a 178 N push", "Physics", "Mechanics and statics",
        "One side frame (a third of the screen mass) about a cross-foot tip 124 mm out, push at 1,372 mm; with and without 10 kg of bags on its feet",
        f"About {f2['side_tip_N']} N bare and {f2['side_tip_ballast_N']} N with 10 kg of ballast ({REV}: weak, ballast added for a fair comparison): it tips at "
        "a touch, like FS1's free ends", FIX, closed_by="Option not carried")
x.cited("X3", "FS2: FR fabric meets NFPA 701 and can be wiped", "Chemistry", "Materials and polymer chemistry",
        "Medline 3-panel FR vinyl screen 'meets the standard UL 94' (Staples listing); Still Water privacy panels 'pass the NFPA 701' (Direct Textile Store)",
        f"UL 94 is a plastics test, not a curtain test, so it is no evidence toward NFPA 701 ({REV}: weak); coated fabric with an NFPA 701 report exists; the "
        "lot's report is to source", PLAUSIBLE)
x.cited("X4", "FS2: costs about the USD 120 target", "Mathematics", "Orders of magnitude",
        "Medline FR vinyl 3-panel screen USD 210.79 (Staples); Winco 3130 3-panel screen USD 235.57 (MDMaxx); two screens needed for a U",
        f"About USD {f2['cost_benchmark_usd']:.0f} for two of the cheaper screens at retail; a made FS2 frame of aluminium tube and FR fabric would cost less, "
        f"to assess, so this compares retail with FS1's parts cost ({REV}: weak)", FIX, closed_by="Option not carried")
x.cited("X5", "FS2: one person carries and sets it", "Mathematics", "Orders of magnitude", "Model mass with FR coated fabric at 0.45 kg/m2 (A12)",
        f"{f2['mass_kg']} kg; {f2['posts']} posts, 12 rails and 6 screens to assemble", WITHIN)
x.cited("X6", "FS3: the cot carries a patient's pull on the screen frame", "Physics", "Mechanics and statics",
        "MSF field hospital bed maximum load 120 kg; frame clamped to both side rails with four M6 clamps",
        "The pull goes into the cot, which the patient is lying on, so the frame cannot tip on its own; clamp slip on a round rail and the cot's own "
        "tipping when a patient pulls sideways at 1.2 m are to assess", PLAUSIBLE)
x.cited("X7", "FS3: gives privacy and a contact boundary at the head and upper body", "Biology", "Human physiology and biomechanics",
        f"Screen from the cot rail to {f3['top_mm']:.0f} mm, {f3['side_len_mm']:.0f} mm along each side from the head",
        "Covers the head and chest of a lying patient; legs and the rest of the cot are open. Same sightlines as FS1 for the covered part", WITHIN)
x.cited("X8", "FS3: staff can clear the head for resuscitation", "Biology", "Ergonomics",
        "Four rail clamps with M6 bolts as drawn", "Unbolting four clamps takes a minute or more; a lift-off frame on sockets would be needed to clear it in "
        "seconds (to design if FS3 is chosen)", FIX, closed_by="Option not carried")
x.cited("X9", "FS3: fire case", "Chemistry", "Materials and polymer chemistry",
        "FR coated fabric at the patient's head, about 1.4 m2", "Much less fire load than FS1 (fabric about 0.6 kg against 4 kg of PP sheet), but "
        "fabric hangs within 0.1 m of the pillow; an FR report is needed", PLAUSIBLE)
x.cited("X10", "FS3: free to make (patents)", "Engineering and technology", "Standards practice",
        "US 11,369,208 B2 (active): canopy of U-shaped frames hinged to a bed with a top wall; US 12,213,925 B2 (active): screen clamped to bed side rails",
        "FS3 has no top wall and no rail-clamp bracket with a slider knob as claimed, but sits close to both: an FTO opinion is needed (FXS-FTO-001)", PLAUSIBLE)
x.cited("X11", "FS1 at P18 with a frosted upper band (the team's semi-transparent upper panels)", "Mathematics", "Orders of magnitude",
        f"Same plan with P18 duos ({PLT} module); free-end leaf at 1.8 m ({PLT} P2)",
        f"Panels {pv['P18_pod_kg_panels']} kg from {pv['P18_sheets']} sheets against 4.03 kg from 2; the free-end leaf {pv['P18_free_end_flat_strip']}; a "
        "frosted FR film or mesh band needs its own fire report and staff still see only shapes through it", FIX, closed_by="FXS-DEC-001 D3; not carried")


def table(rows):
    out = ["| # | Claim (number and unit) | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |",
           "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in sorted(rows, key=lambda r: int(r["id"][1:])):
        out.append(f"| {r['id']} | {r['claim']} | {r['field']} | {r['branch']} | {r['law']} | {r['check']} | {r['verdict']} | {r['closed_by'] or 'Open'} |")
    return "\n".join(out)


def inject(doc, tag, text):
    s = doc.read_text(encoding="utf-8")
    a, b = f"<!-- {tag} -->", f"<!-- /{tag} -->"
    if a in s and b in s:
        i, j = s.index(a) + len(a), s.index(b)
        doc.write_text(s[:i] + "\n" + text + "\n" + s[j:], encoding="utf-8")


if __name__ == "__main__":
    state = c.write()
    x.write()
    doc = ROOT / "docs/01b-stem-check.md"
    if doc.exists():
        inject(doc, "STM_TABLE", table(c.rows))
        inject(doc, "STM_OPTIONS", table(x.rows))
        print("refreshed tables in docs/01b-stem-check.md")
    print("FS1 state:", state)
