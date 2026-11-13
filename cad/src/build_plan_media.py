# SPDX-License-Identifier: CERN-OHL-P-2.0
# SPDX-FileCopyrightText: 2026 Design Molecule Labs with Helpful Engineering
"""FlexSleep Origami Patient Pod: prototype build plan pictures (FXS-BLD-001, STANDARDS section 18), option FS1.

Run from the repo root, one picture group per process on a small machine:
    python cad/src/build_plan_media.py overview
    python cad/src/build_plan_media.py sheets [101 102 ...]
    python cad/src/build_plan_media.py joints [1 2 ...]
    python cad/src/build_plan_media.py steps [1 2 ...]
Every picture is drawn from cad/src/model.py (option_fs1 and its part functions), so pictures and model agree:
    docs/05-build-plan/overview.png        one of each component, pulled apart, numbered in build order
    cad/drawings/FXS-DWG-101 to 104        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import functools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from build123d import Compound, Pos, Rot  # noqa: E402
import model as M  # noqa: E402

OUT = ROOT / "docs/05-build-plan"
DWG = ROOT / "cad/drawings"
DATE = "2026-11-12"
PROJECT = "FlexSleep Origami Patient Pod"
P = M.PARAMS


@functools.lru_cache(None)
def raw():
    return M.option_fs1(context=False)


def sel(*keys, exclude=()):
    return [q for q in raw() if any(k in q["name"] for k in keys) and not any(e in q["name"] for e in exclude)]


def grp(name, qs, color=None, bom=None, explode=(0, 0, 0)):
    return Part(name, Compound([q["shape"] for q in qs]), color or qs[0]["color"], bom if bom is not None else qs[0]["bom"], explode)


def near(x, y, r=400, zmax=None, keys=None):
    out = []
    for q in raw():
        if keys and not any(k in q["name"] for k in keys):
            continue
        c = q["shape"].bounding_box().center()
        if abs(c.X - x) < r and abs(c.Y - y) < r and (zmax is None or c.Z < zmax):
            out.append(Part(q["name"], q["shape"], q["color"], q["bom"]))
    return out


def flat_duo():
    return Compound([M.leaf("a"), Pos(P["LEAF"], 0, 0) * M.leaf("b")])


def overview():
    items = [
        ("EPDM pad (4)", M.pad(), "#151617", 6, (-1800, 0, -300)),
        ("Pod foot block (4)", M.foot_block((285.0, 75.0), 180.0), M.C_FOOT, 3, (-1300, 0, -300)),
        ("Outrigger beam (4)", M.outrigger(180.0), M.C_SHEET, 4, (-800, 0, -300)),
        ("Outrigger pin set (4)", M.pin_set(180.0)[0], M.C_PIN, 5, (-400, 0, -300)),
        ("P12 duo panel (4)", flat_duo(), M.C_SHEET, 1, (-1500, 700, 300)),
        ("Angle clip, round core (6)", M.angle_clip(150.0), M.C_CLIP, 2, (600, 0, 600)),
        ("Printed signs and marks (1 set)", M.fx.print_zone(500, 200), M.fx.SAFETY["red"], 8, (1000, 0, 600)),
        ("Edge stiffener channel (2) and bolts", M.edge_channel(), M.C_PIN, 11, (1300, 600, 300)),
        ("Joint cover strip (9)", M.Box(48, 0.3, 780), "#E4F0F2", 13, (900, 600, 300)),
        ("Ballast bag (4), filled on site", M.bag(), M.C_BAG, 7, (1500, 0, -300)),
    ]
    ps = [Part(n, s, c, b, e) for n, s, c, b, e in items]
    return bv.overview(ps, OUT / "overview.png", title=f"{PROJECT}: components of one pod in build order",
                       subtitle="One of each component, pulled apart and numbered in build order, with the count for one pod; plan, not yet built",
                       size=(12, 8), key=True, elev=22, azim=-55)


SHEETS = {
    101: ("duo", "P12 duo panel: making sketch",
          "4 mm flame-retardant PP twinwall (FXP-S4FR), 1,220 x 2,440 mm sheet, flutes along the 2,440 mm length; two per sheet",
          ["Cut a 1,200 x 1,200 mm blank with the flutes running up the panel",
           "Rout a flat-bottomed groove 13.6 mm wide at 600 mm on the back face, down to the front skin",
           "Hot-punch four 8 mm holes 12.5 mm from each side edge at 125, 175, 1,025, 1,075 mm",
           "Hot-punch five 40 mm holes per leaf at 350 mm up, 100 mm apart",
           "Heat-seal every cut edge, both groove shoulders and ends",
           "Print face is the front: it faces the patient; the groove faces the aisle",
           "Check: folds 60 deg toward the front and 30 deg either way without a crack"]),
    102: ("clip", "Angle clip with a round core: making sketch",
          "PETG print, 100 % infill at tongues and pegs, 0.2 mm layers; moulded PP at scale",
          ["Print standing up (the joint line vertical), tongues lying along the layers",
           "Two slots 4.5 mm wide, 40 mm deep, at 150 deg to each other, on a 12 mm round core",
           "Two 7 mm through-pegs per slot at 25 mm either side of the centre",
           "Clear all support from the tongue windows; each tongue springs back freely",
           "Fits: a panel edge slides in until it meets the core; both pegs drop into its holes",
           "Check: a firm hand tug does not pull the panel out; two fingertips on the lips release it"]),
    103: ("block", "Pod foot block: making sketch",
          "PETG print, 4 walls and 25 % infill; one-slot blocks at the free ends, two-slot blocks at the joints",
          ["Print with the slots upward; block 120 x 70 x 40 mm with 4 mm chamfered corners",
           "Slots 4.5 mm wide along each panel direction, floor 10.5 mm up",
           "Triangular spigot 100 mm long on the outside face, 6.5 mm cross hole 60 mm out",
           "Bond a 2 mm EPDM pad under the block",
           "Fits: the panel's bottom edge drops into the slot and sits 12.5 mm above the floor",
           "Check: the block sits flat without rocking"]),
    104: ("rig", "Outrigger beam: making sketch",
          "Offcut of the same FR twinwall, blank 170 x 240 mm, crush scored across the flutes",
          ["Crush-score two lines 50 mm apart across the flutes; fold into a triangle, apex up",
           "Lap the 20 mm tail inside and heat-stake it",
           "Drill 6.5 mm through both sloping walls 59 mm from the block end, 14 mm up",
           "Seal both open ends",
           "Fits: slide over the block's spigot until it touches the block; push in the pin and split pin",
           "Check: the beam does not turn or pull off the spigot by hand"]),
    105: ("chan", "Edge stiffener channel: making sketch",
          "Aluminium channel 7.5 mm outside, 25 mm deep, 1.5 mm wall, cut to 1,160 mm",
          ["Cut the channel to 1,160 mm and deburr both ends and all edges",
           "Drill two 6.6 mm holes through both flanges, 14.6 mm from the web, 79 and 1,029 mm from the bottom end",
           "Fits: slide over the sealed free edge of a side wall from 46 mm above the floor, web against the edge",
           "Bolt through the panel's outer clip holes (125 and 1,075 mm up) with M6 A4 bolts, washers and nuts, hand tight",
           "Check: the free edge stays straight when the leaf is pressed lightly in the middle"]),
}


def _shape(key):
    return {"duo": flat_duo(), "clip": M.angle_clip(150.0), "block": M.foot_block((285.0, 75.0), 180.0), "rig": M.outrigger(180.0), "chan": M.edge_channel()}[key]


def _where(key):
    q = {"duo": sel("P12 duo, left half side"), "clip": sel("Clip-lock angle, left side high"), "block": sel("Pod foot block, left side"),
         "rig": sel("Outrigger beam, left side"), "chan": sel("Edge stiffener channel, left end")}[key]
    return Part(q[0]["name"], q[0]["shape"], q[0]["color"], q[0]["bom"])


def sheets(which=None):
    for no, (key, title, mat, notes) in SHEETS.items():
        if which and str(no) not in which:
            continue
        part = _where(key)
        c = part.shape.bounding_box().center()
        nb = near(c.X, c.Y, r=1300, keys=("P12 duo", "Pod foot", "Outrigger beam"))
        nb = [p for p in nb if p.name != part.name][:10]
        print(bv.component_sheet(part, nb, PROJECT, f"FXS-DWG-{no}", title, mat, notes, DATE, view_shape=_shape(key)))


def joints(which=None):
    l, r = M.pod_chains()
    js = l.joints[1][0]
    le = l.joints[2][0]
    J = {
        4: ("Joint 4: free end, edge stiffener channel bolted over the edge, foot and bag",
            [Part(q["name"], q["shape"], q["color"], q["bom"]) for q in sel("P12 duo, left half side", "Edge stiffener channel, left end",
                                                                             "Pod foot block, left end", "Outrigger beam, left end", "Ballast bag, left end")]
            + [grp("M6 A4 bolt sets (2)", sel("edge stiffener left end"))], 30, 150),
        1: ("Joint 1: head centre, two angle clips and cover strips, no foot (the release joint)", near(0, 0, 320, zmax=1300), 30, 120),
        2: ("Joint 2: side joint, angle clips, foot, outrigger and bag", near(js[0], js[1], 380, zmax=1300), 30, 150),
        3: ("Joint 3: foot block, spigot, outrigger and pin (bag removed)",
            [p for p in near(js[0], js[1], 380, zmax=200) if "Ballast" not in p.name], 25, 200),
    }
    for k, (title, ps, el, az) in J.items():
        if which and str(k) not in which:
            continue
        print(bv.joint(ps, OUT / f"joint-{k:02d}.png", title, subtitle="Close-up from the model; parts named", elev=el, azim=az))


def steps(which=None):
    pads = sel("EPDM pad")
    feet = sel("Pod foot block", "Outrigger", "Split pin")
    lh = sel("P12 duo, left half") + sel("Edge stiffener channel, left", "edge stiffener left") + [q for q in sel("Joint cover strip, left")]
    rh = sel("P12 duo, right half") + sel("Edge stiffener channel, right", "edge stiffener right") + [q for q in sel("Joint cover strip, right")]
    lc = [q for q in sel("Clip-lock") if "left" in q["name"]]
    rc = [q for q in sel("Clip-lock") if "right" in q["name"]]
    cc = [q for q in sel("Clip-lock") if "centre" in q["name"]] + sel("Joint cover strip, centre")
    bags = sel("Ballast bag")
    signs = sel("Print zone")
    G = lambda n, qs, ex=(0, 0, 0): grp(n, qs, explode=ex)
    S = {
        1: ("Step 1: set the four feet with outriggers and pads round the cot", [], [G("Feet, outriggers, pins, pads (4)", feet + pads, (0, 0, 150))]),
        2: ("Step 2: stand the left half's two duos, clip the side joint, bolt on the edge channel", [G("feet", feet + pads)], [G("Left half and its clips", lh + lc, (-500, 0, 0))]),
        3: ("Step 3: stand the right half's two duos, clip the side joint, bolt on the edge channel", [G("feet", feet + pads), G("left", lh + lc)],
            [G("Right half and its clips", rh + rc, (500, 0, 0))]),
        4: ("Step 4: clip the head centre joint (two clips)", [G("feet", feet + pads), G("left", lh + lc), G("right", rh + rc)],
            [G("Head centre clips", cc, (0, -300, 0))]),
        5: ("Step 5: lay the four filled bags on the outriggers; check the signs and marks",
            [G("feet", feet + pads), G("left", lh + lc + signs), G("right", rh + rc), G("centre", cc)], [G("Ballast bags (4)", bags, (0, 0, 400))]),
    }
    for k, (title, done, new) in S.items():
        if which and str(k) not in which:
            continue
        print(bv.step(done, new, OUT / f"step-{k:02d}.png", title, size=(10, 6), elev=34, azim=130, label_done=False))


if __name__ == "__main__":
    cmd, args = (sys.argv[1] if len(sys.argv) > 1 else "all"), sys.argv[2:]
    if cmd in ("overview", "all"):
        print(overview())
    if cmd in ("sheets", "all"):
        sheets(args)
    if cmd in ("joints", "all"):
        joints(args)
    if cmd in ("steps", "all"):
        steps(args)
