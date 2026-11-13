# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2026 Design Molecule Labs with Helpful Engineering
"""FlexSleep Origami Patient Pod: sizing and first-principles checks (FXS-CAL-001).

Run from the repo root:  python docs/04-calcs/sizing.py   (writes docs/04-calcs/sizing_results.json)
Reads cad/src/model.py (PARAMS and the part lists of FS1, FS2 and FS3) and bom/bom.csv. Platform figures come from
FXP-PLT-001 (docs/platform/flex-platform.md) and are quoted, not recomputed. Every input is cited in FXS-CAL-001
(docs/04-calcs/01-sizing.md) with its source and the date checked (2026-11-12), or marked as an assumption (A1 to A14).
CONCEPT, NOT FOR FABRICATION.
"""
import csv
import json
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src")]
import model as M  # noqa: E402
import flex_parts as fx  # noqa: E402

G = 9.80665
P = M.PARAMS
R = {}

# ---- platform figures (FXP-PLT-001, quoted) ---------------------------------------------------------------------
GSM = P["GSM"] / 1000.0          # 0.70 kg/m2 lot maximum (D1, F5)
HC_PP = 39.7                     # MJ/kg (FSRI via FXP-PLT-001 section 9)
P_PUSH = 178.0                   # N, ANSI/BIFMA X5.6 force stability push (FXP-PLT-001 section 10)
PUSH_25MM = 5.8                  # N that bows a 600 mm leaf by 25 mm (FXP-PLT-001 P4)
CAP_CLIP = 176.0                 # N per clip on paper, two through-pegs (FXP-PLT-001 P9)
RHO_PETG = 1270.0                # kg/m3 (FXP-PLT-001 section 5.3, assumed there)

# ---- cited inputs (FXS-CAL-001 section 1) -------------------------------------------------------------------------
MET = {"sleeping": 72.0, "reclining": 81.0, "seated quiet": 108.0}      # W per person, ASHRAE Fundamentals table via EnergyPlus I/O reference
EYE_STAND = (1421.0, 1753.0)     # mm, women 5th to men 95th, ANSUR II (NCSU summary)
EYE_SIT = (698.0, 860.0)         # mm above the seat, ANSUR II sitting eye height
HC_PET = 21.43                   # MJ/kg gross, PET fibre (UQ fire laboratory INS03)
MATTRESS = dict(kg=7.3, MJkg=19.68, peak_kW=916.7)   # solid polyether foam mattress, FR cotton/polyester cover (CBUF item 1:21, SP test; NCFS table)
PULL_BW = (0.20, 0.41)           # share of body weight on the hands in sit-to-stand with a handle (Bolli et al.)
GRAB_BAR_N = 1112.0              # ADA 609.8 grab bar design force (250 lbf)
MSF_M2_BEDRIDDEN = 4.0           # MSF cholera guideline: about 4 m2 per bedridden patient; 45 m2 tent holds 10 beds + nurse station
WARD_PITCH = 2500.0              # mm, bed centre to bed centre in general wards (Bettercare IPC facility design, section 5-5)
XIE = dict(breath_m=1.0, cough_m=2.0, sneeze_m=6.0, evap_um=(60, 100))   # Xie et al. 2007 (Indoor Air 17: 211-225)

# ---- assumptions (FXS-CAL-001 section 1) --------------------------------------------------------------------------
BODY_KG = 70.0                   # A1 patient mass for the pull case
MOUTH = (0.0, 470.0, 720.0)      # A2 mm, mouth of a patient lying on the cot (head 120 mm from the cot head)
INFILL = 0.45                    # A3 printed foot block mass as a share of solid (4 walls, 25 % infill), to weigh
MU = (0.4, 0.6)                  # A4 EPDM pad on a clinical vinyl or tent floor, wet to dry; to measure (platform D17)
CHI_R = 0.30                     # A5 radiative fraction of a mattress fire (point-source screen)
BAG_EMPTY, CARRY_BAG = 0.10, 0.8 # A6 kg
STEP = {                         # A7 seconds per action for one person, (fast, slow), no training
    "set a foot (pre-pinned outrigger, bonded pad)": (10, 20), "unfold and stand a duo in its feet": (20, 40),
    "push in one clip, holding two panel edges": (10, 20), "lay a filled ballast bag": (10, 20), "check walk round": (30, 60)}
RELEASE = dict(clip=(3.0, 8.0), swing=(2.0, 4.0))   # A8 s per clip released (two fingertips on two lips, crouching for the low clip) and to swing both head leaves open
HEAD_CLEAR = 600.0               # A13 mm kept clear behind the head wall so the head leaves can swing open and the release clips can be reached (F9)
O2_LPM = (5.0, 10.0, 15.0)       # A14 L/min oxygen flows given by mask or concentrator (assumed range), purity 93 to 100 %
HAND_CLEAR = 75.0                # A9 mm minimum gap each side between cot rail and wall for hands and bedding
Q_CONV_SHARE = 1.0               # A10 whole metabolic heat used as convective (conservative for the plume temperature)


def cot_fit_note():
    return f"cot width plus 2 x {HAND_CLEAR:.0f} mm"


# =================================================================================================================
# 1. Geometry of FS1 from the model
# =================================================================================================================
left, right = M.pod_chains()
piv = [d[2][0] for d in left.duos]                       # fold pivots on the interior face: head corner, side fold
jx = abs(left.joints[1][0][0])                           # side joint, mid-plane
inner_min = 2 * min(abs(p[0]) for p in piv)
inner_max = 2 * (jx - M.T / 2)
y_end = left.joints[-1][0][1]
y_corner = piv[0][1]
outer_w = 2 * jx
reach = P["RIG_REACH"]
foot_w = 2 * (jx + reach)
cot_end = P["COT_Y0"] + P["COT_L"]
foot_l = HEAD_CLEAR + max(y_end + P["FOOT_BLOCK"][1] / 2, cot_end + 100.0)     # head clearance to the cot end of a 2.0 m cot
R["geometry"] = dict(inner_w_min_mm=round(inner_min, 1), inner_w_max_mm=round(inner_max, 1), side_len_mm=round(y_end, 1),
                     head_corner_y_mm=round(y_corner, 1), outer_w_m=round(outer_w / 1000, 3), outer_l_m=round(y_end / 1000, 3),
                     footprint_m=(round(foot_w / 1000, 2), round(foot_l / 1000, 2)), footprint_m2=round(foot_w * foot_l / 1e6, 2),
                     cot_max_mm=round(inner_min - 2 * HAND_CLEAR, 0),
                     clear_each_side_mm={f"{w:.0f}": round((inner_min - w) / 2, 0) for w in (600, 750, 850, 1000)},
                     cot_overhang_mm=round(P["COT_Y0"] + P["COT_L"] - y_end, 0))

# plan polygon of the interior (joint mid-plane points of the left half, mirrored) for the open-top area
pts = [(0.0, 0.0)]
pts += [(piv[0][0], piv[0][1]), left.joints[1][0], (piv[1][0], piv[1][1]), left.joints[2][0]]
poly = pts + [(-x, y) for x, y in reversed(pts[1:])]
area = 0.5 * abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly))))
H_TOP = M.Z0 + P["H_WALL"]
open_end = inner_max * P["H_WALL"] / 1e6
n_perf = 8 * 5
perf = n_perf * math.pi * (P["PERF_D"] / 2000) ** 2
R["air"] = dict(open_top_m2=round(area / 1e6, 2), open_end_m2=round(open_end, 2), perf_m2=round(perf, 3), perf_holes=n_perf,
                perf_share_pct=round(100 * perf / (area / 1e6 + open_end + perf), 1), pod_volume_m3=round(area / 1e6 * H_TOP / 1000, 2),
                wall_top_mm=H_TOP)

# =================================================================================================================
# 2. Mass and pack (PR-011)
# =================================================================================================================
parts = M.option_fs1(context=False)
vol = {}
for q in parts:
    key = q["name"].split(",")[0]
    vol.setdefault(key, []).append(q["shape"].volume)
duo_kg = 2 * P["LEAF"] * P["H_WALL"] * 1e-6 * GSM
clip_kg = sum(vol["Clip-lock angle"]) * 1e-9 * RHO_PETG
block_kg_solid = sum(vol["Pod foot block"]) * 1e-9 * RHO_PETG
block_kg = block_kg_solid * INFILL
NF = len(vol["Pod foot block"])
rig_kg = NF * (170 * 240e-6) * GSM
chan_kg = sum(vol["Edge stiffener channel"]) * 1e-9 * 2700
strip_kg = sum(vol["Joint cover strip"]) * 1e-9 * 900
pin_kg = sum(vol["Outrigger pin 6 mm (ISO 2341 B)"]) * 1e-9 * 7950 + sum(vol["Split pin (ISO 1234)"]) * 1e-9 * 7950
pad_kg = sum(vol["EPDM pad"]) * 1e-9 * 1150
prints_kg = 0.05
carried = 4 * duo_kg + clip_kg + block_kg + rig_kg + pin_kg + pad_kg + prints_kg + chan_kg + strip_kg + NF * BAG_EMPTY + CARRY_BAG
R["mass"] = dict(duo_kg=round(duo_kg, 3), panels_kg=round(4 * duo_kg, 2), clips_kg=round(clip_kg, 2), clip_each_g=round(clip_kg / 6 * 1000, 0),
                 blocks_kg=round(block_kg, 2), block_each_solid_kg=round(block_kg_solid / NF, 3), outriggers_kg=round(rig_kg, 2), feet=NF,
                 pins_kg=round(pin_kg, 3), pads_kg=round(pad_kg, 3), channels_kg=round(chan_kg, 2), strips_kg=round(strip_kg, 3),
                 carried_kg=round(carried, 1), ballast_kg=NF * P["BAG_KG"], standing_kg=round(carried - CARRY_BAG + NF * P["BAG_KG"], 1))
R["pack"] = dict(panels_mm=4 * 10.0, panels_folded_mm=(600, 1200), note="platform: a duo folds to about 10 mm (FXP-PLT-001 section 11)")

# =================================================================================================================
# 3. Sightlines (PR-003, PR-004)
# =================================================================================================================
def hidden(e, a, z, h=None):
    """Depth behind a wall of top h, hidden to an eye e at a metres from the wall, for points at height z (mm)."""
    h = H_TOP if h is None else h
    return a * (h - z) / (e - h) if e > h else float("inf")


Z_BODY, Z_FACE = P["COT_TOP"] + 60 + 250, MOUTH[2]        # top of the chest under bedding, and the face
sight = {}
for nm, e in (("woman 5th", EYE_STAND[0]), ("man 95th", EYE_STAND[1])):
    sight[nm] = {f"at {a} m": dict(body_m=round(hidden(e, a * 1000, Z_BODY) / 1000, 2), face_m=round(hidden(e, a * 1000, Z_FACE) / 1000, 2))
                 for a in (0.3, 0.5, 1.0)}
face_wall = inner_min / 2
seat = P["COT_TOP"] - 50                    # sitting on the cot's canvas edge
R["sight"] = dict(standing=sight, wall_top_mm=H_TOP, face_from_wall_m=round(face_wall / 1000, 2),
                  tall_sees_face_within_m=round(face_wall * (EYE_STAND[1] - H_TOP) / (H_TOP - Z_FACE) / 1000, 2),
                  seated_eye_mm=(seat + EYE_SIT[0], seat + EYE_SIT[1]), lying_eye_mm=Z_FACE,
                  seated_eye_above_top_mm=(round(seat + EYE_SIT[0] - H_TOP), round(seat + EYE_SIT[1] - H_TOP)))

# =================================================================================================================
# 4. Air, plume, heat and oxygen (PR-009)
# =================================================================================================================
body_top = Z_BODY
d_src = 0.40                                # m, source diameter for the Baturin and Schmidt relation (a lying torso, assumed in A10)
y_rise = (H_TOP - body_top) / 1000
plume = {}
for nm, q in MET.items():
    Gv = 0.005 * (q * Q_CONV_SHARE) ** (1 / 3) * (y_rise + d_src) ** (5 / 3)
    plume[nm] = dict(m3h=round(Gv * 3600, 1), dT_K=round(q / (1.2 * 1005 * Gv), 1))
vol_m3 = R["air"]["pod_volume_m3"]
o2 = {}
for f in O2_LPM:
    for share in (1.0, 0.5):
        Vx = plume["sleeping"]["m3h"] * share / 60 * 1000          # L/min of exchange air
        o2[f"{f:.0f} L/min, exchange x {share}"] = (round(100 * (0.209 * Vx + 0.93 * f) / (Vx + f), 1), round(100 * (0.209 * Vx + 1.0 * f) / (Vx + f), 1))
R["thermal"] = dict(plume=plume, plume_m3h_at_top=plume["seated quiet"]["m3h"], plume_dT_K=plume["seated quiet"]["dT_K"],
                    pod_volume_changes_per_h=round(plume["sleeping"]["m3h"] / vol_m3, 1), y_rise_m=round(y_rise, 2),
                    oxygen_pct=o2, oxygen_threshold_pct=23.5)

# =================================================================================================================
# 5. Straight-line directions from the mouth: walls, open top, open foot end, cot (PR-005, a geometric screen)
# =================================================================================================================
js = [j[0] for j in left.joints]
lp = [js[0], piv[0], js[1], piv[1], js[2]]
rp = [(-x, y) for x, y in lp]
segs = [(a_, b_) for chain in (lp, rp) for a_, b_ in zip(chain[:-1], chain[1:])]
COT = (-P["COT_W"] / 2, P["COT_W"] / 2, P["COT_Y0"], P["COT_Y0"] + P["COT_L"], P["COT_TOP"])


def ray(o, d):
    best, kind = None, None
    for (ax, ay), (bx, by) in segs:
        ex, ey = bx - ax, by - ay
        den = d[0] * ey - d[1] * ex
        if abs(den) < 1e-12:
            continue
        t = ((ax - o[0]) * ey - (ay - o[1]) * ex) / den
        u = ((ax - o[0]) * d[1] - (ay - o[1]) * d[0]) / den
        if t > 1e-6 and 0 <= u <= 1:
            z = o[2] + t * d[2]
            if M.Z0 <= z <= H_TOP and (best is None or t < best):
                best, kind = t, "wall"
    if d[2] < 0:                                   # the cot plane below the mouth
        t = (COT[4] - o[2]) / d[2]
        x_, y_ = o[0] + t * d[0], o[1] + t * d[1]
        if COT[0] <= x_ <= COT[1] and COT[2] <= y_ <= COT[3] and (best is None or t < best):
            best, kind = t, "cot or body"
    if kind is None:
        if d[2] > 0:
            t_top = (H_TOP - o[2]) / d[2]
            y_at = o[1] + t_top * d[1]
            kind = "top" if y_at <= y_end else "foot end"
        else:
            kind = "foot end or floor"
    return kind


random.seed(1)
cnt = {}
N = 40000
for _ in range(N):
    zc = random.uniform(-1, 1)
    ph = random.uniform(0, 2 * math.pi)
    sx = math.sqrt(1 - zc * zc)
    k = ray(MOUTH, (sx * math.cos(ph), sx * math.sin(ph), zc))
    cnt[k] = cnt.get(k, 0) + 1
R["droplet_geometry"] = {k: round(100 * v / N, 1) for k, v in cnt.items()}
hb = sum(ray(MOUTH, (math.cos(2 * math.pi * k / 3600), math.sin(2 * math.pi * k / 3600), 0.0)) == "wall" for k in range(3600))
up_cone = sum(ray(MOUTH, (math.sin(math.radians(30)) * math.cos(2 * math.pi * k / 360), math.sin(math.radians(30)) * math.sin(2 * math.pi * k / 360),
                          math.cos(math.radians(30)))) == "top" for k in range(360))
head_line = math.radians(P["HEAD_TILT"])
R["droplet_geometry"].update(side_wall_m=round(inner_min / 2000, 2), head_wall_m=round(MOUTH[1] * math.cos(head_line) / 1000, 2),
                             horizontal_share_blocked_pct=round(100 * hb / 3600, 1), up_30deg_cone_to_top_pct=round(100 * up_cone / 360, 1),
                             joint_slit_mm=round(2 * fx.CORE / 2 * math.sin(math.radians(75)), 1))

# =================================================================================================================
# 6. Stability: push from the aisle, patient pull, released half, tent gusts (PR-007)
# =================================================================================================================
def masses(ps):
    out = []
    for q in ps:
        nm = q["name"]
        c = q["shape"].bounding_box().center()
        if nm.startswith("P12 duo"):
            m = duo_kg
            c = q["shape"].center()
        elif nm.startswith("Ballast bag"):
            m = P["BAG_KG"]
        elif nm.startswith("Pod foot block"):
            m = q["shape"].volume * 1e-9 * RHO_PETG * INFILL
        elif nm.startswith(("Clip", "Edge stiffener channel")):
            m = q["shape"].volume * 1e-9 * (RHO_PETG if nm.startswith("Clip") else 2700)
        elif nm.startswith("Outrigger beam"):
            m = 170 * 240e-6 * GSM
        else:
            m = 0.0
        out.append((nm, m, c.X, c.Y))
    return out


ms = masses(parts)
W = sum(m for _, m, _, _ in ms) * G
z_push = min(1372.0, H_TOP - 102.0) / 1000          # BIFMA height: 1,372 mm or 102 mm below the top, whichever is lower


def tip_force(items, axis_x, side, z):
    """Force at height z (m) that tips the items about a line x = axis_x (mm) parallel to y; side +1 tips toward +x."""
    return sum(m * G * (side * (axis_x - x)) / 1000 for _, m, x, _ in items) / z


x_tip_out = -(jx + reach)
x_in_edge = -(jx - P["FOOT_BLOCK"][1] / 2)
pod_out = tip_force(ms, x_tip_out, -1, z_push)
half = [i for i in ms if i[2] < -1.0]
half_out = tip_force(half, x_tip_out, -1, z_push)
half_in = tip_force(half, x_in_edge, +1, z_push)
endp = [i for i in ms if ("left end" in i[0]) or i[0] == "P12 duo, left half side"]
end_out = tip_force(endp, x_tip_out, -1, z_push)
end_in = tip_force(endp, x_in_edge, +1, z_push)
pull_need = (PULL_BW[0] * BODY_KG * G, PULL_BW[1] * BODY_KG * G)
slide = (MU[0] * W, MU[1] * W)
z_pull = 900.0
top_share = (z_pull - ZC0) / (ZC1 - ZC0) if (ZC1 := M.ZC[1]) and (ZC0 := M.ZC[0]) else 0.0
gust = {f"{v} m/s": round(0.5 * 1.2 * v * v * 2 * P["LEAF"] * P["H_WALL"] * 1e-6, 1) for v in (2.0, 3.0, 5.0)}
R["tip"] = dict(z_push_mm=z_push * 1000, pod_kg=round(W / G, 1), out_side_N=round(pod_out, 0), released_half_out_N=round(half_out, 0),
                released_half_in_N=round(half_in, 0), free_end_out_N=round(end_out, 0), free_end_in_N=round(end_in, 0),
                pull_in_N=round(min(half_in, end_in), 0), pull_need_N=(round(pull_need[0]), round(pull_need[1])),
                grab_bar_N=GRAB_BAR_N, slide_N=(round(slide[0]), round(slide[1])), push_N=P_PUSH,
                leaf_25mm_N=PUSH_25MM, clip_cap_N=CAP_CLIP, top_clip_share=round(top_share, 2),
                top_clip_N=(round(top_share * pull_need[0] / 2), round(top_share * pull_need[1] / 2), round(top_share * pull_need[0]), round(top_share * pull_need[1])),
                gust_on_two_leaves_N=gust)
# outrigger beam bending under its bag (inward tipping), skins only: I = a^3 t / 4 for a thin equilateral triangle
a_, t_ = 50.0, 2 * fx.SKIN
I_ = a_ ** 3 * t_ / 4
c_ = 2 / 3 * a_ * math.sqrt(3) / 2
Mb = P["BAG_KG"] * G * (P["FOOT_BLOCK"][1] / 2 + P["BAG"][0] / 2 + 5.0 - P["FOOT_BLOCK"][1] / 2) / 1000
R["outrigger"] = dict(M_Nm=round(Mb, 1), I_mm4=round(I_), stress_MPa=round(Mb * 1000 * c_ / I_, 1), pp_yield_MPa=24.0)
# free-end leaf buckling: platform raw factor (h_cr / H)^3 with no load factor; with the edge stiffener the leaf is held on both edges
R["terminal_leaf"] = dict(flat_strip_factor=(round((1441 / 1200) ** 3, 2), round((1144 / 1200) ** 3, 2)),
                          held_both_edges_margin_LF2=(round(3.1 * 1800 / 1200, 1), round(1.6 * 1800 / 1200, 1)),
                          held_with_creep_0p3=round(3.1 * 1800 / 1200 * 0.3, 1))

# =================================================================================================================
# 7. Fire (PR-008)
# =================================================================================================================
sheet_m2 = 4 * 2 * P["LEAF"] * P["H_WALL"] * 1e-6 + NF * 170 * 240e-6
pod_MJ = sheet_m2 * GSM * HC_PP
petg_MJ = (clip_kg + block_kg) * HC_PET
bags_MJ = NF * BAG_EMPTY * HC_PET
matt_MJ = MATTRESS["kg"] * MATTRESS["MJkg"]
r_25 = math.sqrt(CHI_R * MATTRESS["peak_kW"] / (4 * math.pi * 25.0))
r_10 = math.sqrt(CHI_R * MATTRESS["peak_kW"] / (4 * math.pi * 10.0))
gap_pods = (WARD_PITCH - outer_w) / 1000
d_neigh = (WARD_PITCH - outer_w / 2) / 1000
R["fire"] = dict(sheet_m2=round(sheet_m2, 2), pod_MJ=round(pod_MJ, 0), petg_MJ=round(petg_MJ, 1), bags_MJ=round(bags_MJ, 1),
                 total_pod_MJ=round(pod_MJ + petg_MJ + bags_MJ, 0), mattress_MJ=round(matt_MJ, 0), mattress_peak_kW=MATTRESS["peak_kW"],
                 ratio_pod_to_mattress=round((pod_MJ + petg_MJ + bags_MJ) / matt_MJ, 2), r_25kW_m=round(r_25, 2), r_10kW_m=round(r_10, 2),
                 flame_height_m=round(0.235 * MATTRESS["peak_kW"] ** 0.4 - 1.02 * math.sqrt(4 * 1.9 * 0.75 / math.pi), 1),
                 gap_between_pods_at_2p5m_m=round(gap_pods, 2), neighbour_wall_from_bed_m=round(d_neigh, 2),
                 q_neighbour_from_mattress_kW_m2=round(CHI_R * MATTRESS["peak_kW"] / (4 * math.pi * d_neigh ** 2), 1))

# =================================================================================================================
# 8. Deployment and access times (PR-001, PR-006)
# =================================================================================================================
n = {"set a foot (pre-pinned outrigger, bonded pad)": NF, "unfold and stand a duo in its feet": 4,
     "push in one clip, holding two panel edges": 6, "lay a filled ballast bag": NF, "check walk round": 1}
fast = sum(STEP[k][0] * v for k, v in n.items()) / 60
slow = sum(STEP[k][1] * v for k, v in n.items()) / 60
rel = (2 * RELEASE["clip"][0] + RELEASE["swing"][0], 2 * RELEASE["clip"][1] + RELEASE["swing"][1])
R["deploy_min"] = (round(fast, 1), round(slow, 1))
R["access"] = dict(release_s=rel, clips_to_release=2, head_open_chord_m=round(2 * P["LEAF"] * math.sin(math.radians(45)) / 1000, 2),
                   head_clear_behind_m=HEAD_CLEAR / 1000, side_clear_closed_mm=R["geometry"]["clear_each_side_mm"]["750"],
                   cot_pull_out_m=round((MOUTH[1] + 600 - P["COT_Y0"] + 300) / 1000, 1))

# =================================================================================================================
# 9. Ward density (PR-014)
# =================================================================================================================
aisle = 1200.0                                     # mm, shared aisle at the foot end (A11: half counted per pod)
per_pod = foot_w / 1000 * (foot_l + aisle / 2) / 1000
R["density"] = dict(m2_per_pod=round(per_pod, 2), msf_m2_per_bed=MSF_M2_BEDRIDDEN, beds_per_45m2_plain=10,
                    pods_per_45m2=round(45 / per_pod, 1), fits_2p5m_pitch=foot_w <= WARD_PITCH,
                    pitch_needed_mm=round(foot_w, 0), pitch_needed_walls_mm=round(outer_w, 0),
                    floor_gap_between_rigs_at_2p5m_mm=round(WARD_PITCH - foot_w, 0), bags_reach_mm=round(reach + 0, 0))

# =================================================================================================================
# 10. Cost from the BOM (PR-013)
# =================================================================================================================
rows = list(csv.DictReader((ROOT / "bom/bom.csv").open()))
lines = [(r["item"], float(r["qty"]) * float(r["unit_cost_usd"])) for r in rows]
tot = sum(v for _, v in lines)
R["cost"] = dict(bom_total=round(tot, 2), target=120.0, stretch=75.0, over=round(tot - 120.0, 2),
                 drivers=sorted([(k, round(v, 2)) for k, v in lines], key=lambda x: -x[1])[:4],
                 per_use_50=round(tot / 50, 2), per_use_100=round(tot / 100, 2), prototype_cash_usd=round(10 * 44.99 + 150, 2))

# =================================================================================================================
# 11. Other options (FS2, FS3), first-order figures from their models
# =================================================================================================================
def opt_mass(opt):
    import cad_parts
    tot = 0.0
    for q in M.components(opt):
        if q["kind"] == "context":
            continue
        if "fabric" in q["name"].lower():
            tot += q["shape"].volume / P["FS2_FABRIC_T"] * 1e-6 * 0.45     # A12 FR PVC-coated polyester 0.45 kg/m2
        else:
            tot += cad_parts.mass_kg(q)
    return round(tot, 1)


fs2 = M.option_fs2(False)
post = [q for q in fs2 if q["name"].startswith("Aluminium post")]
R["FS2"] = dict(mass_kg=opt_mass("FS2"), posts=len(post), height_mm=P["FS2_H"], cost_benchmark_usd=round(2 * 210.79, 2),
                note="two Medline 3-panel FR vinyl screens would screen the U")
fs2_side_kg = R["FS2"]["mass_kg"] / 3
lev = P["FS2_FOOT"][0] / 2 * math.cos(math.radians(45)) / 1000
R["FS2"]["side_tip_N"] = round(fs2_side_kg * G * lev / 1.372, 1)
R["FS2"]["side_tip_ballast_N"] = round((fs2_side_kg + 10.0) * G * lev / 1.372, 1)
R["FS3"] = dict(mass_kg=opt_mass("FS3"), top_mm=P["FS3_TOP"], side_len_mm=P["FS3_SIDE_L"])
R["P12_vs_P18"] = dict(P18_duo_kg=round(2 * P["LEAF"] * 1800e-6 * GSM, 3), P18_pod_kg_panels=round(4 * 2 * P["LEAF"] * 1800e-6 * GSM, 2),
                       P18_sheets=4, P12_sheets=2, P18_free_end_flat_strip="fails cold (FXP-PLT-001 P2: flat h_cr 1,441 mm < 1,800 mm)")

(ROOT / "docs/04-calcs/sizing_results.json").write_text(json.dumps(R, indent=1))
if __name__ == "__main__":
    for k, v in R.items():
        print(k, v)
