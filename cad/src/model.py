# SPDX-License-Identifier: CERN-OHL-P-2.0
# SPDX-FileCopyrightText: 2026 Design Molecule Labs with Helpful Engineering
"""FlexSleep Origami Patient Pod. Parametric model (kit 1.9 interface, STANDARDS section 24), detail level D3.

Run from the repo root:  python .kit/cad_check.py --export
Every main dimension is in PARAMS; docs/04-calcs/sizing.py (FXS-CAL-001) and stem_check.py (FXS-STM-001) read it.
FS1 is built from the shared Flex platform parts in cad/src/flex_parts.py (FXP-PLT-001); that file is not edited here.

Units mm. Z up, floor at z = 0. x runs across the cot (centre line x = 0), y along it: the head wall is at y = 0 and
the open foot end at +y. CONCEPT, NOT FOR FABRICATION.

Options (FXS-OPT-001; the recommendation is proposed, awaiting Amish):
  FS1  Origami panel pod (team concept, iteration 2, made constructable on the platform): four FXP-S4FR P12 duos,
       1.2 m high, in two mirror halves that meet at the head centre on one angle joint. Each half is a duo folded
       60 deg at the head corner and a second duo joined on a 30 deg angle clip, so each side wall is a zigzag
       (platform rule S1). The halves stand alone as L shapes (rule S3): releasing the two clips of the head joint
       lets staff slide one half away to reach the head and side for resuscitation. Five feet with one outside
       outrigger each, pinned, with a site-filled 5 kg bag. Perforated band at 350 mm; open top and open foot end.
  FS2  Fabric privacy screen on a light pole frame: the same U plan drawn with flame-retardant (FR) coated fabric
       laced into aluminium post-and-rail frames 1.75 m high on cross feet.
  FS3  Cot-mounted head-end screen: an aluminium tube frame clamped to the cot's side rails carries an FR fabric
       screen round the head and upper body, 1.2 m above the floor; the cot and the patient's weight carry it.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from build123d import Axis, Box, Compound, Cylinder, Location, Polygon, Pos, Rot, chamfer, extrude

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]
import cad_parts as cp  # noqa: E402
from cad_parts import part  # noqa: E402
import flex_parts as fx  # noqa: E402

TITLE = "FlexSleep Origami Patient Pod"
OPTIONS = {"FS1": "Origami panel pod (FR twinwall, split head)", "FS2": "Fabric privacy screen on a pole frame",
           "FS3": "Cot-mounted head-end screen"}
PRINCIPLES = {
    "FS1": "Pre-scored FR polypropylene duo panels fold into two zigzag L halves round the cot; plan shape, feet and "
           "site-filled ballast give stability; the halves part at the head for resuscitation access.",
    "FS2": "FR coated fabric is laced into light aluminium post-and-rail frames standing on cross feet round the cot; "
           "the light fabric allows a 1.75 m screen at the cost of more parts and a frame that tips easily.",
    "FS3": "An aluminium frame clamped to the cot's own rails carries an FR fabric screen round the head and upper "
           "body; the cot and patient carry every load, so nothing stands on the floor and nothing tips on its own.",
}
CHOSEN = "FS1"   # carried to the drawing, BOM and build plan. Proposed, awaiting Amish (FXS-DEC-001 D1); not decided
OPTION_VIEWS = {
    "FS1": dict(el=30, az=130, scale="person", keep_context=True, ground_z=0.0),
    "FS2": dict(el=30, az=130, scale="person", keep_context=True, ground_z=0.0),
    "FS3": dict(el=30, az=130, scale="person", keep_context=True, ground_z=0.0),
}
ALLOWED_CONTACTS = [("Split pin", "Outrigger pin")]   # the split pin passes through the pin's cross hole by design

T = fx.SHEET[fx.GRADE]["t"]                    # 4 mm FXP-S4FR
TS = fx.SKIN                                   # 0.26 mm skin
GW = fx._groove_w()                            # 13.6 mm fold groove
PARAMS = {
    # platform (FXP-PLT-001), read, not changed
    "GRADE": fx.GRADE, "SHEET_T": T, "GSM": fx.SHEET[fx.GRADE]["gsm"], "LEAF": fx.LEAF, "DUO_W": 2 * fx.LEAF,
    "CORE": fx.CORE, "CLIP_H": fx.CLIP_H, "FOOT_SEAT": fx.FOOT_SEAT, "GROOVE_W": GW,
    "PAD": 2.0,                                 # EPDM non-slip pad under every foot block (FXS-DEC-001 F4)
    # FS1 pod
    "H_WALL": 1200.0,                           # P12 duo; P18 with a translucent band is FXS-DEC-001 D3
    "HEAD_TILT": 15.0,                          # head leaves at 15 deg to the head line (angle joint of 150 deg at the centre)
    "CORNER_TURN": -60.0,                       # fold at the head corner (turn, deg): head leaf 165 deg -> side leaf 105 deg
    "ZIG": 30.0,                                # zigzag turn at the side joint and the side fold (rule S1)
    "FOOT_BLOCK": (120.0, 70.0, 40.0),          # platform foot block size, long axis across the outrigger
    "RIG_REACH": 300.0,                         # outrigger tip from the joint line (FXP-PLT-001 section 5.4)
    "SPIGOT_L": 100.0,                          # triangular spigot on the block that the hollow outrigger slides over (F3)
    "PIN_D": 6.0,
    "PERF_D": 40.0, "PERF_Z": 350.0, "PERF_PITCH": 100.0,   # perforated band, team feature (FXS-DEC-001 D4)
    "BAG": (250.0, 200.0, 70.0), "BAG_KG": 5.0,
    # cot (context) and the fit range of the team deck
    "COT_L": 1900.0, "COT_W": 750.0, "COT_TOP": 500.0, "COT_Y0": 260.0,   # MSF field hospital bed 190 to 200 x 75 to 85 cm, 50 to 55 cm
    "COT_FIT": (600.0, 1000.0),                 # deck: cots 60 to 100 cm wide
    # FS2: fabric screens on post-and-rail frames
    "FS2_H": 1750.0, "FS2_POST": (25.0, 1.5), "FS2_FOOT": (350.0, 40.0, 5.0), "FS2_FABRIC_T": 0.6,
    "FS2_HALF_W": 700.0, "FS2_Y0": -60.0, "FS2_L": 2000.0,
    # FS3: cot-mounted head-end screen
    "FS3_TOP": 1200.0, "FS3_TUBE": (22.0, 1.5), "FS3_SIDE_L": 700.0, "FS3_FABRIC_T": 0.6,
}
P = PARAMS
H = P["H_WALL"]
Z0 = fx.FOOT_SEAT + P["PAD"]                    # panel bottom edge, seated in a foot on its 2 mm pad
ZC = [Z0 + z for z in fx.clip_heights(H)]       # clip centres: 162.5 and 1062.5

C_SHEET, C_CLIP, C_FOOT, C_PIN, C_BAG = "#ECEDE8", "#2E3A40", "#2E3A40", "#C9CDD1", "#B8AD8F"
C_INK = fx.SAFETY["black"]


def _p(name, shape, mat, kind="made", bom=None, explode=(0, 0, 0), color=None, group="shell", note=""):
    return part(name, shape, mat, kind=kind, bom=bom, group=group, explode=explode, color=color, note=note)


_CACHE = {}


def _once(key, fn):
    if key not in _CACHE:
        _CACHE[key] = fn()
    return _CACHE[key]


def _rot2(v, deg):
    a = math.radians(deg)
    return (v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a))


def _add(a, b):
    return (a[0] + b[0], a[1] + b[1])


# ---------------------------------------------------------------------------------------------------------
# FS1 pieces
# ---------------------------------------------------------------------------------------------------------
def leaf(side):
    """One 600 mm leaf of a P12 duo in panel coordinates (x 0..600, print face at y = 0, back face at y = T).
    side 'a': clip holes on its left edge, half the fold groove on its right edge; side 'b' the mirror. The
    perforated band (team feature) is a row of hot-punched 40 mm holes at 350 mm, 100 mm apart, at least 50 mm
    from the fold, the edges and the clip holes (FXP-PLT-001 section 13)."""
    def f():
        L = P["LEAF"]
        body = fx.panel(L, H, hole_edges=("left",) if side == "a" else ("right",))
        g = GW / 2
        x0 = L - g if side == "a" else 0.0
        body = body - Pos(x0 + g / 2, TS + (T - TS + 0.5) / 2, H / 2) * Box(g, T - TS + 0.5, H + 2)
        r = P["PERF_D"] / 2
        for x in (100.0, 200.0, 300.0, 400.0, 500.0):
            body = body - Pos(x, T / 2, P["PERF_Z"]) * Rot(90, 0, 0) * Cylinder(r, T + 2)
        return body
    return _once(f"leaf{side}", f)


class Chain:
    """Walks a wall along the floor: joints, leaves and folds. Interior on the right of travel (print face)."""

    def __init__(self, xy, heading):
        self.xy, self.h = xy, heading
        self.joints = [(xy, None, heading)]     # (point, heading in, heading out)
        self.duos = []                          # list of [(location, side), (location, side)]

    def duo(self, fold_turn, zig_after=None):
        h1 = self.h
        loc_a = Pos(self.xy[0], self.xy[1], Z0) * Rot(0, 0, h1) * Pos(fx.CORE / 2, -T / 2, 0)
        pivot = _add(self.xy, _rot2((fx.CORE / 2 + P["LEAF"], -T / 2), h1))
        h2 = h1 + fold_turn
        loc_b = Pos(pivot[0], pivot[1], Z0) * Rot(0, 0, h2)
        self.duos.append([(loc_a, "a"), (loc_b, "b"), (pivot, h1, h2)])
        self.xy = _add(pivot, _rot2((P["LEAF"] + fx.CORE / 2, T / 2), h2))
        self.h = h2
        return self

    def joint(self, turn):
        hin = self.h
        self.h = hin + turn
        self.joints.append((self.xy, hin, self.h))
        return self

    def end(self):
        self.joints.append((self.xy, self.h, None))
        return self


def pod_chains():
    """Left half from the head centre out; right half from its free end in (interior always on the right)."""
    ht, ct, z = P["HEAD_TILT"], P["CORNER_TURN"], P["ZIG"]
    left = Chain((0.0, 0.0), 180.0 - ht).duo(ct).joint(-z).duo(+z).end()
    fe = left.joints[-1][0]
    hl = left.joints[-1][1]
    right = Chain((-fe[0], fe[1]), (180.0 - hl) + 180.0).duo(+z).joint(-z).duo(ct).end()
    return left, right


def angle_clip(ang, detail="full"):
    """The FXP-PLT-001 angle clip (two standard slot arms from fx._arm, slots at 0 and `ang` deg) on a 12 mm ROUND
    core. The platform helper's square core stands 0.93 mm proud of the 6 mm stop line in the 150 deg slot
    (6 / cos 30 = 6.93 mm), so a panel cut to the platform hole pattern cannot reach its pegs there (found by the
    interference check; FXS-DEC-001 F1, platform request 1). Slots, pegs, tongues and clip grid are unchanged."""
    def f():
        core = Cylinder(fx.CORE / 2, fx.CLIP_H)
        body = core
        for a in (0.0, ang):
            body = body + Rot(0, 0, a) * fx._arm(T, detail)
        return body
    return _once(f"aclip_{round(ang, 1)}_{detail}", f)


def _clip_at(xy, hin, hout, z, detail="full"):
    d1 = (hin + 180.0) % 360
    ang = (hout - d1) % 360
    return Pos(xy[0], xy[1], z) * Rot(0, 0, d1) * angle_clip(ang, detail)


def foot_block(slot_dirs, rig_dir):
    """Pod foot block in its own frame (joint axis on Z, floor contact at z = 0): the FXP-PLT-001 foot block
    (120 x 70 x 40 mm, slots 4.5 mm wide, panel seated 10.5 mm up) with its long axis across the outrigger, slots
    along each panel direction, and a triangular spigot 100 mm long on the outrigger side that the hollow
    outrigger beam slides over and is pinned to (FXS-DEC-001 F3). A 6.5 mm cross hole takes the pin."""
    key = f"blk_{tuple(round(a, 1) for a in slot_dirs)}_{round(rig_dir, 1)}"

    def f():
        bx, by, bz = P["FOOT_BLOCK"]
        gap = T + fx.CLEAR
        blk = Pos(0, 0, bz / 2) * Box(by, bx, bz)        # long axis along local y, outrigger along local +x
        try:
            blk = chamfer(blk.edges().filter_by(Axis.Z), 4.0)
        except Exception:
            pass
        blk = Rot(0, 0, rig_dir) * blk
        for a in slot_dirs:
            L = 72.0
            blk = blk - Rot(0, 0, a) * Pos(L / 2 - gap / 2, 0, fx.FOOT_SEAT + 15) * Box(L + gap, gap, 30)
        side = 50.0
        tri_h = side * math.sqrt(3) / 2
        sp = extrude(Polygon((-side / 2 + 2.6, 1.6), (side / 2 - 2.6, 1.6), (0, tri_h - 2.9), align=None), P["SPIGOT_L"])
        sp = Rot(0, 90, 0) * Rot(0, 0, 90) * sp           # profile in the local YZ plane, along +x
        sp = sp - Pos(P["SPIGOT_L"] - 40.0, 0, 14.0) * Rot(90, 0, 0) * Cylinder(3.25, 60)
        sp = Pos(by / 2 - 1.0, 0, 0) * sp
        return blk.fuse(Rot(0, 0, rig_dir) * sp)
    return _once(key, f)


def outrigger(rig_dir):
    """Folded FR twinwall outrigger beam (equilateral triangle, 50 mm sides, apex up), from the block face to
    300 mm from the joint line, with the 6.5 mm pin hole through both sloping walls."""
    def f():
        side = 50.0
        tri_h = side * math.sqrt(3) / 2
        r0 = P["FOOT_BLOCK"][1] / 2
        L = P["RIG_REACH"] - r0
        outer = extrude(Polygon((-side / 2, 0), (side / 2, 0), (0, tri_h), align=None), L)
        inner = Pos(0, 0, -1) * extrude(Polygon((-side / 2 + 1.5, 0.9), (side / 2 - 1.5, 0.9), (0, tri_h - 1.7), align=None), L + 2)
        beam = outer - inner
        beam = Rot(0, 90, 0) * Rot(0, 0, 90) * beam
        beam = beam - Pos(P["SPIGOT_L"] - 40.0 - 1.0, 0, 14.0) * Rot(90, 0, 0) * Cylinder(3.25, 60)
        return Rot(0, 0, rig_dir) * Pos(r0, 0, 0) * beam
    return _once(f"rig_{round(rig_dir, 1)}", f)


def pin_set(rig_dir):
    """6 mm ISO 2341 B clevis pin across the outrigger and spigot, with its ISO 1234 split pin."""
    r = P["FOOT_BLOCK"][1] / 2 - 1.0 + P["SPIGOT_L"] - 40.0
    w = 50.0 - 2 * 14.0 / math.tan(math.radians(60))   # beam width at the pin height
    grip = w + 7.0                                      # clear of the sloping walls above and below the pin line
    y0 = -(w / 2 + 3.5)                                 # head face on the -y side, pin runs toward +y
    pin = Pos(r, y0, 14.0) * Rot(90, 0, 0) * cp.clevis_pin(P["PIN_D"], grip)
    sp = Pos(r, y0 + grip + P["PIN_D"], 14.0) * Rot(0, 0, 90) * cp.split_pin(P["PIN_D"])
    return Rot(0, 0, rig_dir) * pin, Rot(0, 0, rig_dir) * sp


def bag():
    def f():
        bx, by, bz = P["BAG"]
        return cp.break_edges(Pos(0, 0, bz / 2) * Box(bx, by, bz), 14.0)
    return _once("bag", f)


def pad():
    return _once("pad", lambda: cp.sheet(P["FOOT_BLOCK"][1] - 2, P["FOOT_BLOCK"][0] - 2, P["PAD"], r_corner=3.0, edge=0.3))


def cot_context():
    """Field cot of the MSF field hospital bed class (context only): two side rails, end bars, legs, canvas bed."""
    L, W, top, y0 = P["COT_L"], P["COT_W"], P["COT_TOP"], P["COT_Y0"]
    rails = []
    for sx in (-1, 1):
        rails.append(Pos(sx * (W / 2 - 15), y0, top - 15) * Rot(-90, 0, 0) * cp.round_tube(30, 1.5, L))
        for yy in (y0 + 80, y0 + L / 2, y0 + L - 80):
            rails.append(Pos(sx * (W / 2 - 15), yy, 0) * cp.round_tube(25, 1.5, top - 30))
    for yy in (y0 + 15, y0 + L - 15):
        rails.append(Pos(-W / 2 + 15, yy, top - 15) * Rot(0, 90, 0) * cp.round_tube(25, 1.5, W - 30))
    bed = Pos(0, y0 + L / 2, top - 2) * cp.sheet(W - 30, L - 40, 2.0, r_corner=10)
    return Compound(rails + [bed])


def patient_context():
    import context_parts
    man = context_parts.mannequin(1750.0, "stand")
    lying = Rot(0, 0, 180) * Rot(-90, 0, 0) * man   # face up, head toward -y, back on the cot
    bb = lying.bounding_box()
    return Pos(-bb.center().X, P["COT_Y0"] + 120 - bb.min.Y, P["COT_TOP"] + 60 - bb.min.Z) * lying


def _ctx(name, shape, color="#9C9C9E", material="skin"):
    return dict(name=name, shape=shape, material="clay", material_name=material, color=color, kind="context",
                bom=None, group="context", explode=(0, 0, 0), note="")


CH_Z0, CH_L = 46.0, 1160.0                      # edge stiffener: bottom just above the foot block (42 mm), top 6.5 mm under the wall top


def edge_channel():
    """Free-end edge stiffener (FXS-DEC-001 F7): aluminium channel 7.5 x 25 x 1.5 mm, 1,170 mm long, slipped over the
    sealed free edge of each side wall and bolted through the two outer clip holes (125 and 1,075 mm up). It holds the
    terminal leaf's free edge straight, so the leaf buckles as a plate held on both vertical edges, not as a flat strip."""
    def f():
        h, b, tf = T + fx.CLEAR + 3.0, 25.0, 1.5
        ch = cp.channel(h, b, tf, CH_L, tf=tf)
        for z in (Z0 + 125.0 - CH_Z0, Z0 + 1075.0 - CH_Z0):
            ch = ch - Pos(fx.HOLE_E + tf + 0.3, 0, z) * Rot(90, 0, 0) * Cylinder(3.3, h + 4)
        return cp.break_edges(ch, 0.3) if False else ch
    return _once("edge_channel", f)


def option_fs1(context=True, head_open=False):
    """FS1 parts. head_open=True swings both head leaves 90 deg outward about their corner folds, as staff would open
    the head for resuscitation after releasing the two centre clips (FXS-DEC-001 F5); used for the cutaway picture."""
    out = []
    left, right = pod_chains()
    halves = (("left", left), ("right", right))
    names = {("left", 0): "head and side", ("left", 1): "side", ("right", 0): "side", ("right", 1): "head and side"}
    head_tf = {}
    for hn, ch in halves:
        for k, (la, lb, (pivot, h1, h2)) in enumerate(ch.duos):
            sw_a = sw_b = Location()
            if head_open and (hn, k) == ("left", 0):
                sw_a = Pos(pivot[0], pivot[1], 0) * Rot(0, 0, -90) * Pos(-pivot[0], -pivot[1], 0)
            if head_open and (hn, k) == ("right", 1):
                sw_b = Pos(pivot[0], pivot[1], 0) * Rot(0, 0, 90) * Pos(-pivot[0], -pivot[1], 0)
            if (hn, k) == ("left", 0):
                head_tf["left"] = sw_a * la[0]
            if (hn, k) == ("right", 1):
                head_tf["right"] = sw_b * lb[0]
            shape = Compound([sw_a * la[0] * leaf("a"), sw_b * lb[0] * leaf("b")])
            ex = (-260, 0, 0) if hn == "left" else (260, 0, 0)
            out.append(_p(f"P12 duo, {hn} half {names[(hn, k)]}", shape, "hdpe_natural", "made", 1, ex, C_SHEET,
                          note=f"FXP-S4FR, 1,200 x 1,200 mm, folded {abs(h2 - h1):.0f} deg at its groove, flutes vertical"))
    lj, rj = left.joints, right.joints
    joints = [("centre", lj[0][0], (rj[-1][1] + 180) % 360, lj[0][2]),        # (name, xy, slot dir A, slot dir B)
              ("left side", lj[1][0], (lj[1][1] + 180) % 360, lj[1][2]),
              ("right side", rj[1][0], (rj[1][1] + 180) % 360, rj[1][2]),
              ("left end", lj[2][0], (lj[2][1] + 180) % 360, None),
              ("right end", rj[0][0], None, rj[0][2])]
    # clips at the side joints and the head centre (the release joint); none at the centre when the head is open
    for nm, xy, da, db in joints[:3]:
        if head_open and nm == "centre":
            continue
        hin = (da - 180) % 360
        for n, zc in enumerate(ZC):
            out.append(_p(f"Clip-lock angle, {nm} {'low' if n == 0 else 'high'}", _clip_at(xy, hin, db, zc), "hdpe_black", "made", 2,
                          (0, 0, 0), C_CLIP, note="FXP-PLT-001 angle clip arms on a round core (F1), PETG print"))
        # joint cover strips on both faces between and beyond the clips (F8): 11.6 mm slit at a 150 deg joint
        if head_open and nm == "centre":
            continue
        bx = math.cos(math.radians(da)) + math.cos(math.radians(db))
        by = math.sin(math.radians(da)) + math.sin(math.radians(db))
        segs = [(P["PAD"] + P["FOOT_BLOCK"][2] + 3.0, ZC[0] - 50.0 - 3.0), (ZC[0] + 50.0 + 3.0, ZC[1] - 50.0 - 3.0), (ZC[1] + 50.0 + 3.0, Z0 + H - 3.0)]
        for si, (z0, z1) in enumerate(segs):
            pieces = []
            for d in (da, db):
                n_ = (-math.sin(math.radians(d)), math.cos(math.radians(d)))
                sgn = 1.0 if n_[0] * bx + n_[1] * by > 0 else -1.0
                for face in (1.0, -1.0):
                    off = face * sgn * (T / 2 + 0.25)
                    pieces.append(Pos(xy[0], xy[1], 0) * Rot(0, 0, d) * Pos(12.0, off, (z0 + z1) / 2) * Box(24.0, 0.3, z1 - z0))
            out.append(_p(f"Joint cover strip, {nm} {('low', 'mid', 'top')[si]}", Compound(pieces), "polycarbonate", "bought", 13, (0, 0, 0),
                          "#E4F0F2", note="flexible clear PP strip 24 mm each side of the slit, both faces, heat-staked to one leaf (F8)"))
    # feet at the side joints and free ends (none at the head centre, so the head leaves can swing open, F5)
    tri_h = 50.0 * math.sqrt(3) / 2
    for nm, xy, da, db in joints[1:]:
        dirs = [d for d in (da, db) if d is not None]
        if len(dirs) == 2:
            bis = math.degrees(math.atan2(math.sin(math.radians(dirs[0])) + math.sin(math.radians(dirs[1])),
                                          math.cos(math.radians(dirs[0])) + math.cos(math.radians(dirs[1]))))
            rig = (bis + 180.0) % 360                 # convex side of the joint: outside the pod
        else:
            rig = 180.0 if xy[0] < 0 else 0.0         # free ends: straight out sideways
        loc = Pos(xy[0], xy[1], 0)
        out.append(_p(f"EPDM pad, {nm}", loc * Rot(0, 0, rig) * pad(), "epdm", "bought", 6, (0, 0, -160), "#151617"))
        out.append(_p(f"Pod foot block, {nm}", loc * Pos(0, 0, P["PAD"]) * foot_block(tuple(dirs), rig), "hdpe_black", "made", 3,
                      (0, 0, -120), C_FOOT, note="platform foot block with one outside spigot, PETG print (F3)"))
        out.append(_p(f"Outrigger beam, {nm}", loc * Pos(0, 0, P["PAD"]) * outrigger(rig), "hdpe_natural", "made", 4, (0, 0, -120), C_SHEET,
                      note="folded from FXP-S4FR offcut, blank 170 x 240 mm, crush scored across the flutes"))
        pn, sp = pin_set(rig)
        out.append(_p(f"Outrigger pin 6 mm (ISO 2341 B), {nm}", loc * Pos(0, 0, P["PAD"]) * pn, "stainless", "fastener", 5))
        out.append(_p(f"Split pin (ISO 1234), {nm}", loc * Pos(0, 0, P["PAD"]) * sp, "stainless", "fastener", 5))
        r = P["FOOT_BLOCK"][1] / 2 + P["BAG"][0] / 2 + 5.0
        bxy = _add(xy, _rot2((r, 0.0), rig))
        out.append(_p(f"Ballast bag, {nm}", Pos(bxy[0], bxy[1], P["PAD"] + tri_h + 0.4) * Rot(0, 0, rig) * bag(), "canvas", "bought", 7,
                      (0, 0, 120), C_BAG))
    # free-end edge stiffeners (F7), bolted through the two outer clip holes
    for nm, xy, da, db in joints[3:]:
        hd = da if da is not None else db                       # direction from the end joint back along the panel
        edge = _add(xy, _rot2((fx.CORE / 2, 0.0), hd))
        loc = Pos(edge[0], edge[1], CH_Z0) * Rot(0, 0, hd) * Pos(-1.8, 0, 0)
        out.append(_p(f"Edge stiffener channel, {nm}", loc * edge_channel(), "aluminium", "made", 11, (0, 0, 0), C_PIN))
        hh = T + fx.CLEAR + 3.0
        for z in (Z0 + 125.0 - CH_Z0, Z0 + 1075.0 - CH_Z0):
            for n_, s_ in cp.hex_bolt_set(6, hh):
                out.append(_p(f"{n_}, edge stiffener {nm} at {z + CH_Z0 - Z0:.0f}", loc * Pos(fx.HOLE_E + 1.8, hh / 2, z) * Rot(-90, 0, 0) * s_,
                              "stainless", "fastener", 12))
    # printed zones on the print (interior) faces: prohibition sign and words, bed card, release marks (F2, FXP-PLT-001 C2, C5)
    for hn, ch in halves:
        k = 0 if hn == "left" else 1
        la, lb, _ = ch.duos[k]
        side_loc = lb[0] if hn == "left" else la[0]
        head_loc = head_tf[hn]
        out.append(_p(f"Print zone, do-not-pull words, {hn}", side_loc * fx.print_zone(330, 200, (220 if hn == "left" else 50), 700 - Z0), "label",
                      "made", 8, (0, 0, 0), C_INK))
        out.append(_p(f"Print zone, prohibition sign, {hn}", side_loc * fx.print_zone(150, 150, (50 if hn == "left" else 400), 725 - Z0), "label",
                      "made", 8, (0, 0, 0), fx.SAFETY["red"]))
        if hn == "left":
            out.append(_p("Print zone, bed card", head_loc * fx.print_zone(300, 200, 150, 800 - Z0), "label", "made", 8, (0, 0, 0), C_INK))
        out.append(_p(f"Print zone, release mark, {hn} head", head_loc * fx.print_zone(60, 900, (500 if hn == "left" else 40), 150), "label",
                      "made", 8, (0, 0, 0), C_INK))
    if context:
        out.append(_ctx("Field cot (context)", cot_context(), "#5E6B5A", "canvas"))
        out.append(_ctx("Patient lying (scale)", patient_context()))
    return out


# ---------------------------------------------------------------------------------------------------------
# FS2: FR fabric screens on aluminium post-and-rail frames (same U plan)
# ---------------------------------------------------------------------------------------------------------
def option_fs2(context=True):
    out = []
    od, t = P["FS2_POST"]
    hh, hw, y0, L = P["FS2_H"], P["FS2_HALF_W"], P["FS2_Y0"], P["FS2_L"]
    fl, fw, ft = P["FS2_FOOT"]
    posts = [(-hw, y0), (0.0, y0), (hw, y0), (-hw, y0 + L / 2), (hw, y0 + L / 2), (-hw, y0 + L), (hw, y0 + L)]
    for k, (x, y) in enumerate(posts):
        post = cp.round_tube(od, t, hh - 40) - Pos(0, 0, 10) * Rot(0, 90, 0) * Cylinder(4.25, od + 20)
        out.append(_p(f"Aluminium post {k + 1}, {od:.0f} x {t} mm", Pos(x, y, ft + 30) * post, "aluminium", "bought", 21))
        bars = []
        for a in (45, 135):
            bars.append(Rot(0, 0, a) * Pos(0, 0, ft / 2) * cp.break_edges(Box(fl, fw, ft), 1.0))
        out.append(_p(f"Cross foot {k + 1}, aluminium flat bar", Pos(x, y, 0) * Compound(bars), "aluminium", "made", 22, (0, 0, -100)))
        sock = cp.round_tube(od + 6, 2.0, 60) - Pos(0, 0, 40) * Rot(0, 90, 0) * Cylinder(4.25, od + 20)
        out.append(_p(f"Post socket {k + 1}", Pos(x, y, ft) * sock, "aluminium", "made", 22, (0, 0, -100)))
        for n, s in cp.hex_bolt_set(8, od + 6):
            out.append(_p(f"{n}, post {k + 1}", Pos(x, y, ft + 40) * Rot(0, 90, 0) * Pos(0, 0, (od + 6) / 2) * s, "zinc_plated", "fastener"))
    spans = [(0, 1), (1, 2), (0, 3), (3, 5), (2, 4), (4, 6)]
    for k, (a, b) in enumerate(spans):
        (x0, y_0), (x1, y1) = posts[a], posts[b]
        Ls = math.hypot(x1 - x0, y1 - y0 if False else y1 - y_0)
        ang = math.degrees(math.atan2(y1 - y_0, x1 - x0))
        loc = Pos(x0, y_0, 0) * Rot(0, 0, ang)
        for zr, nm in ((hh - 20, "top"), (180.0, "bottom")):
            out.append(_p(f"{nm.capitalize()} rail {k + 1}", loc * Pos(od / 2 + 8, 0, zr) * Rot(0, 90, 0) * cp.round_tube(20, 1.2, Ls - od - 16),
                          "aluminium", "bought", 23))
            for e, xe in (("a", od / 2 + 9), ("b", Ls - od / 2 - 9)):
                ring = Rot(0, 90, 0) * (Cylinder(14, 8) - Cylinder(10.3, 10))
                out.append(_p(f"Rail end clamp {k + 1}{nm[0]}{e}", loc * Pos(xe, 0, zr) * ring, "hdpe_black", "made", 24))
        scr = cp.sheet(Ls - od - 60, hh - 260, P["FS2_FABRIC_T"],
                       holes=[(-(Ls - od - 60) / 2 + 30 + j * 250, (hh - 260) / 2 - 20, 10) for j in range(int((Ls - od - 120) // 250) + 1)],
                       r_corner=20, edge=0.2)
        out.append(_p(f"FR coated fabric screen {k + 1}", loc * Pos(Ls / 2, 12, 200 + (hh - 260) / 2) * Rot(90, 0, 0) * scr, "canvas", "bought", 25,
                      color="#DCE7EA"))
    if context:
        out.append(_ctx("Field cot (context)", cot_context(), "#5E6B5A", "canvas"))
        out.append(_ctx("Patient lying (scale)", patient_context()))
    return out


# ---------------------------------------------------------------------------------------------------------
# FS3: cot-mounted head-end screen
# ---------------------------------------------------------------------------------------------------------
def option_fs3(context=True):
    out = []
    od, t = P["FS3_TUBE"]
    W, top, y0 = P["COT_W"], P["COT_TOP"], P["COT_Y0"]
    xr = W / 2 - 15                                 # cot rail centre line
    xo = xr + 45.0                                  # upright line, outboard of the rail
    zt = P["FS3_TOP"]
    ys = [y0 + 120.0, y0 + 120.0 + P["FS3_SIDE_L"]]
    for sx in (-1, 1):
        for j, y in enumerate(ys):
            nm = f"{'left' if sx < 0 else 'right'} {'head' if j == 0 else 'rear'}"
            out.append(_p(f"Upright, {nm}", Pos(sx * xo, y, top - 60) * cp.round_tube(od, t, zt - top + 60 - 15), "aluminium", "bought", 31))
            # rail clamp: two printed halves round the cot rail and a bracket round the upright, one M6 bolt set
            blk = (cp.break_edges(Box(70, 40, 50), 3.0) - Pos(-22.5, 0, 0) * Rot(90, 0, 0) * Cylinder(15.4, 50)
                   - Pos(22.5, 0, 0) * Cylinder(od / 2 + 0.4, 60) - Pos(0, 0, 0) * Rot(90, 0, 0) * Cylinder(3.3, 60))
            out.append(_p(f"Rail clamp, {nm}", Pos(sx * (xr + 22.5), y, top - 15) * Rot(0, 0, 0 if sx > 0 else 180) * blk, "hdpe_black", "made", 32))
            for n, s in cp.hex_bolt_set(6, 40):
                out.append(_p(f"{n}, clamp {nm}", Pos(sx * (xr + 22.5), y + 20, top - 15 + 0) * Rot(-90, 0, 0) * Pos(0, 0, 0) * s, "zinc_plated", "fastener"))
            if False:
                pass
        # side top tube along the cot, between the head and rear uprights
        out.append(_p(f"Side top tube, {'left' if sx < 0 else 'right'}", Pos(sx * xo, ys[0] + 16, zt) * Rot(-90, 0, 0) * cp.round_tube(od, t, P["FS3_SIDE_L"] - 32),
                      "aluminium", "bought", 33))
        for j, y in enumerate(ys):
            el = cp.break_edges(Box(32, 32, 32), 3.0) - Cylinder(od / 2 + 0.3, 40) - Rot(90, 0, 0) * Cylinder(od / 2 + 0.3, 40)
            out.append(_p(f"Corner fitting, {'left' if sx < 0 else 'right'} {'head' if j == 0 else 'rear'}", Pos(sx * xo, y, zt) * el, "hdpe_black", "made", 34))
    out.append(_p("Head top tube", Pos(-xo + 16, ys[0], zt) * Rot(0, 90, 0) * cp.round_tube(od, t, 2 * xo - 32), "aluminium", "bought", 33))
    # fabric: head panel across and two side panels, hung from the top tubes on ties, to the cot rail level
    hf = zt - top - 40
    head = cp.sheet(2 * xo - 40, hf, P["FS3_FABRIC_T"], holes=[(-(2 * xo - 40) / 2 + 30 + j * 200, hf / 2 - 20, 8) for j in range(5)], r_corner=15, edge=0.2)
    out.append(_p("FR fabric head panel", Pos(0, ys[0] - 20, top + 20 + hf / 2) * Rot(90, 0, 0) * head, "canvas", "bought", 35, color="#DCE7EA"))
    for sx in (-1, 1):
        sp = cp.sheet(P["FS3_SIDE_L"] - 40, hf, P["FS3_FABRIC_T"], holes=[(-(P["FS3_SIDE_L"] - 40) / 2 + 30 + j * 200, hf / 2 - 20, 8) for j in range(4)],
                      r_corner=15, edge=0.2)
        out.append(_p(f"FR fabric side panel, {'left' if sx < 0 else 'right'}", Pos(sx * (xo + 20), ys[0] + P["FS3_SIDE_L"] / 2, top + 20 + hf / 2) * Rot(0, 0, 90) * Rot(90, 0, 0) * sp,
                      "canvas", "bought", 35, color="#DCE7EA"))
    if context:
        out.append(_ctx("Field cot (context)", cot_context(), "#5E6B5A", "canvas"))
        out.append(_ctx("Patient lying (scale)", patient_context()))
    return out


def components(option="FS1"):
    return {"FS1": option_fs1, "FS2": option_fs2, "FS3": option_fs3}[option]()


if __name__ == "__main__":
    from collections import Counter
    l, r = pod_chains()
    print("left joints", [(tuple(round(v, 1) for v in j[0]), j[1], j[2]) for j in l.joints])
    print("right joints", [(tuple(round(v, 1) for v in j[0]), j[1], j[2]) for j in r.joints])
    for k in OPTIONS:
        ps = components(k)
        real = [q for q in ps if q["kind"] != "context"]
        print(k, len(real), "parts", Counter(q["kind"] for q in real))
