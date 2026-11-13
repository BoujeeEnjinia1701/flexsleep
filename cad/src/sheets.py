# SPDX-License-Identifier: CERN-OHL-P-2.0
# SPDX-FileCopyrightText: 2026 Design Molecule Labs with Helpful Engineering
"""FlexSleep Origami Patient Pod: drawing set and STL export for option FS1 (carried in the drawing set; choice awaiting Amish).

Run from the repo root, one sheet per process on a small machine:  python cad/src/sheets.py [ga|foot|stl]
    cad/drawings/FXS-DWG-001   general arrangement, split-head pod of four P12 duos round a field cot
    cad/drawings/FXS-DWG-002   foot detail: foot block, spigot, outrigger, pin, pad and ballast bag
    cad/stl/*.stl              one of each printed part (angle clip, foot blocks)
Making sketches for each made part (FXS-DWG-101 onward) are drawn by cad/src/build_plan_media.py.
Sheets are generated from cad/src/model.py and never edited by hand; figures come from FXS-CAL-001.
CONCEPT, NOT FOR FABRICATION.
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src")]
from build123d import Compound, export_stl  # noqa: E402
from drawing import Sheet, project_views  # noqa: E402
import model as M  # noqa: E402

P = M.PARAMS
DATE = "2026-11-12"
DWG = ROOT / "cad/drawings"
R = json.loads((ROOT / "docs/04-calcs/sizing_results.json").read_text())
PROJECT = "FlexSleep Origami Patient Pod"
MAT = "FXP-S4FR 4 mm FR PP twinwall (FXP-PLT-001); PETG printed clips and foot blocks; stainless pins; see bom/bom.csv"
SKIP = ("Print zone", "EPDM pad", "Split pin")


def body(skip=SKIP):
    return [q for q in M.option_fs1(context=False) if not any(s in q["name"] for s in skip)]


def ga():
    parts = body(SKIP + ("Outrigger pin",))
    work = DWG / "_views_ga"
    views = project_views(Compound(children=[q["shape"] for q in parts]), work, center_lines=False)
    s = Sheet(project=PROJECT, title="Split-head patient pod of P12 duo panels (option FS1): general arrangement",
              dwg_no="FXS-DWG-001", rev="P1", author="Amish Chadha", date=DATE, concept=True, scale=None, material=MAT,
              revisions=[("P1", "Preliminary GA from the TRL 3 model (FXS-CAL-001)", DATE, "AC")])
    s.add_ortho(views, ["front", "top", "right"])
    s.add_svg(views["iso"], 276, 32, 140, 70, label="Isometric view", sublabel="Not to scale; seen from the open foot end, right and above")
    g, t = R["geometry"], R["tip"]
    s.add_notes("Key dimensions (mm) and data", [
        f"Pod {g['outer_w_m'] * 1000:.0f} wide x {g['outer_l_m'] * 1000:.0f} long on joint lines; walls {P['H_WALL']:.0f} high on 12.5 mm seats",
        f"Inner width {g['inner_w_min_mm']:.0f} at the folds, {g['inner_w_max_mm']:.0f} at the joints",
        "Head leaves at 15 deg to the head line; 150 deg angle joint at the centre",
        "Head corner fold 60 deg; side joint and side fold 30 deg (zigzag)",
        "4 P12 duos; 6 angle clips (round core) at 162.5 and 1,062.5",
        "4 foot blocks with one pinned outrigger each, 300 from the joint line",
        "4 site-filled 5 kg sand bags; edge channels on the free ends",
        f"Floor needed {g['footprint_m'][0]} x {g['footprint_m'][1]} m with cot and 0.6 m behind the head",
        "Head centre (no foot): release two clips, swing the head leaves open",
        f"Carried {R['mass']['carried_kg']} kg; parts USD {R['cost']['bom_total']:.2f}",
        "Boundary, not a barrier; do not lean or pull; indoor only",
        "PRELIMINARY, NOT FOR FABRICATION",
    ], x=276, y=118, width=140)
    s.save(DWG / "FXS-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print("wrote cad/drawings/FXS-DWG-001.svg, .pdf, .png")


def foot():
    parts = []
    for q in M.option_fs1(context=False):
        if q["name"].endswith(", left side") and not q["name"].startswith("Print"):
            parts.append(q["shape"])
    work = DWG / "_views_foot"
    views = project_views(Compound(children=parts), work, center_lines=False)
    s = Sheet(project=PROJECT, title="Pod foot at the left side joint (option FS1): block, spigot, outrigger, pin, pad and bag",
              dwg_no="FXS-DWG-002", rev="P1", author="Amish Chadha", date=DATE, concept=True, scale=None, material=MAT,
              revisions=[("P1", "Preliminary foot detail from the TRL 3 model", DATE, "AC")])
    s.add_ortho(views, ["front", "top", "right"], dims=True)
    s.add_svg(views["iso"], 276, 32, 140, 70, label="Isometric view", sublabel="Foot at the left side joint; not to scale")
    s.add_notes("Foot hardware", [
        "Block 120 x 70 x 40, two 4.5 mm slots at 150 deg, panels seated 10.5 up",
        "Triangular spigot 100 long on the outside face",
        "Outrigger: folded FR twinwall beam, 50 mm sides, apex up, slid over the spigot",
        "6 mm stainless clevis pin across beam and spigot, split pin on the far side",
        "2 mm EPDM pad bonded under the block",
        "5 kg sealed sand bag laid on the outrigger, filled off the clinical floor",
        "PRELIMINARY, NOT FOR FABRICATION",
    ], x=276, y=118, width=140)
    s.save(DWG / "FXS-DWG-002")
    shutil.rmtree(work, ignore_errors=True)
    print("wrote cad/drawings/FXS-DWG-002.svg, .pdf, .png")


def stl():
    out = ROOT / "cad/stl"
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.stl"):
        old.unlink()
    shapes = {"angle-clip-round-core": M.angle_clip(150.0), "foot-block-two-slot": M.foot_block((285.0, 75.0), 180.0),
              "foot-block-one-slot": M.foot_block((285.0,), 180.0)}
    for nm, sh in shapes.items():
        export_stl(sh, str(out / f"fxs-{nm}.stl"), tolerance=0.05, angular_tolerance=0.2)
    print("wrote", len(list(out.glob("*.stl"))), "STL files to cad/stl/")


if __name__ == "__main__":
    fns = {"ga": ga, "foot": foot, "stl": stl}
    for w in sys.argv[1:] or list(fns):
        fns[w]()
