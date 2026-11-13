# SPDX-License-Identifier: CERN-OHL-P-2.0
# SPDX-FileCopyrightText: 2026 Design Molecule Labs with Helpful Engineering
"""FlexSleep Origami Patient Pod: concept media from the TRL 3 model (option FS1, carried; proposed, awaiting Amish).

Run from the repo root:  python cad/src/concept_media.py [hero|cutaway|exploded|flow|web|blueprint ...]
With no argument it draws everything; on a small machine run one picture per process. Geometry comes from
cad/src/model.py; figures come from FXS-CAL-001 (docs/04-calcs/sizing_results.json). Uses the pieces of
.kit/concept.py render_all one at a time, with a 1.75 m person for scale. CONCEPT, NOT FOR FABRICATION.
"""
import csv
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src")]
import concept as K  # noqa: E402
from concept import Part  # noqa: E402
import model as M  # noqa: E402

PROJECT, TITLE, DWG, DATE = "FlexSleep Origami Patient Pod", "Split-head patient pod of FR twinwall panels (option FS1, proposed)", "FXS-DWG-010", "2026-11-12"
MD = ROOT / "media"
RES = ROOT / "docs/04-calcs/sizing_results.json"
SMALL = ("pin", "Split", "pad")


def parts(small=False, context=True, keep=None, head_open=False):
    out = []
    for q in M.option_fs1(context=context, head_open=head_open):
        if not small and any(s in q["name"] for s in SMALL):
            continue
        if keep and not keep(q):
            continue
        out.append(Part(q["name"], q["shape"], q["color"], q["bom"], tuple(q["explode"])))
    return out


def hero():
    ps = K.with_scale_figure(parts())
    return K._render(ps, MD / "hero.png", title=PROJECT, size=(10, 6.5), elev=30, azim=130,
                     note="Option FS1 (carried; choice proposed, awaiting Amish). Seen from the open foot end, right and above, 30 deg elevation; "
                          "grey figure 1.75 m; patient on a 0.75 m field cot. Walls 1.2 m, open top and open foot end; the two halves "
                          "part at the head centre. CONCEPT, NOT FOR FABRICATION")


def cutaway():
    ps = parts(head_open=True)
    return K._render(ps, MD / "cutaway.png", azim=-140, elev=32, size=(9, 7), title=f"{PROJECT}: head opened for resuscitation",
                     note="Both head leaves swung 90 deg outward on their corner folds after the two centre clips are released; seen from behind "
                          "the head and left, 32 deg elevation. Nothing is lifted or slid; 0.6 m is kept clear behind the head. CONCEPT, NOT FOR FABRICATION")


def bom_names():
    out = {}
    for r in csv.DictReader((ROOT / "bom/bom.csv").open()):
        n, _, rest = r["item"].partition(" ")
        out[int(n)] = rest.split(",")[0]
    return out


def exploded():
    names = bom_names()
    ps = []
    for p in parts(small=True, context=False):
        if p.bom is None:
            continue
        ps.append(Part(names.get(p.bom, p.name), p.shape, p.color, p.bom, p.explode))
    return K._render(ps, MD / "exploded.png", offsets=True, labels=True, size=(11, 8), elev=30, azim=-40,
                     title=f"{PROJECT}: exploded view",
                     note="Seen from the open foot end, right and above, 30 deg elevation; numbers match bom/bom.csv. Halves pulled apart, "
                          "feet lowered, bags lifted")


def flow():
    r = json.loads(RES.read_text())
    a, th = r["air"], r["thermal"]
    stages = [("Ward air in", f"foot end {a['open_end_m2']} m2"),
              ("Perforated band", f"{a['perf_share_pct']} % of openings"),
              ("Patient, 72 to 108 W", "sleeping to seated"),
              ("Warm plume rises", f"{th['plume_m3h_at_top']:.0f} m3/h at wall top"),
              ("Out of the open top", f"{a['open_top_m2']} m2"),
              ("Back to the ward", f"{th['plume_dT_K']:.1f} K warmer")]
    return K.flow_diagram(stages, MD / "flow.png",
                          f"{PROJECT}: how air leaves the pod (estimates, FXS-CAL-001); the walls stop direct contact and sideways "
                          "large droplets, not aerosols", "")


def web():
    return K.export_web_model(parts(context=False), "media", title=f"{PROJECT}: {TITLE}")


def blueprint():
    from build123d import Compound
    from drawing import Sheet, project_views
    r = json.loads(RES.read_text())
    ps = parts(context=False)
    shown = K.with_scale_figure(parts())
    views = project_views(Compound(children=[p.shape for p in ps]), MD / "_views", center_lines=False)
    views["iso"] = project_views(Compound(children=[p.shape for p in shown]), MD / "_views_fig", center_lines=False)["iso"]
    g = r["geometry"]
    s = Sheet(project=PROJECT, title=TITLE, dwg_no=DWG, rev="P1", author="Amish Chadha", date=DATE, theme="blueprint",
              material="Detailed TRL 3 model for concept communication",
              revisions=[("P1", "Concept sheet from the TRL 3 model", DATE, "AC")])
    s.add_ortho(views)
    s.add_svg(views["iso"], 276, 32, 140, 118, label="Isometric view", sublabel="Not to scale; grey is a 1.75 m person")
    s.add_notes("Key figures (estimates, FXS-CAL-001)", [
        f"Pod {g['outer_w_m']:.2f} x {g['outer_l_m']:.2f} m on joint lines; walls 1.2 m, open top and foot end",
        f"Inner width {g['inner_w_min_mm']:.0f} to {g['inner_w_max_mm']:.0f} mm; fits cots up to {g['cot_max_mm']:.0f} mm",
        f"4 P12 duos from 2 FR sheets; 6 clips; 4 feet with bags; 2 edge channels",
        f"Carried mass {r['mass']['carried_kg']} kg; folded panels {r['pack']['panels_mm']:.0f} mm thick",
        f"Free end tips at about {r['tip']['free_end_out_N']:.0f} N: a boundary, not a support (pull to stand needs {r['tip']['pull_need_N'][0]} N or more)",
        f"Head release about {r['access']['release_s'][0]:.0f} to {r['access']['release_s'][1]:.0f} s (estimate)",
        f"Fire load: pod {r['fire']['pod_MJ']:.0f} MJ beside a {r['fire']['mattress_MJ']:.0f} MJ foam mattress",
        f"Parts USD {r['cost']['bom_total']:.0f} (target USD 120); indoor or in-tent only"], x=276, y=168, width=140)
    s.save(MD / "concept-blueprint")
    shutil.rmtree(MD / "_views", ignore_errors=True)
    shutil.rmtree(MD / "_views_fig", ignore_errors=True)
    return MD / "concept-blueprint.png"


if __name__ == "__main__":
    fns = {"hero": hero, "cutaway": cutaway, "exploded": exploded, "flow": flow, "web": web, "blueprint": blueprint}
    for w_ in sys.argv[1:] or list(fns):
        print(w_, "->", fns[w_]())
