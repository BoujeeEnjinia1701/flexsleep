# SPDX-License-Identifier: CERN-OHL-P-2.0
# SPDX-FileCopyrightText: 2026 Design Molecule Labs with Helpful Engineering
"""FlexSleep Origami Patient Pod: product appearance model (kit 1.9), TRL 3, option FS1 (carried; choice awaiting Amish).

Built from option_fs1() in cad/src/model.py with every part used as it is, so every main dimension comes from the
model. Only scale context is added: the field cot and a patient lying on it (from model.py) and a standing 1.75 m
mannequin from .kit/context_parts.py at the open foot end, all on the floor (z = 0) the feet stand on; the head-open
state of the same model for the resuscitation render. APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.
Groups: "shell" (panels, prints, strips), "internal" (clips, feet, outriggers, channels, pins, bags), "context" (cot and
people), "open" (the pod with its head opened).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Pos, Rot  # noqa: E402
import model as M  # noqa: E402

TITLE = "FlexSleep Origami Patient Pod: split-head pod of FR twinwall panels round a field cot"
_SHELL = ("P12 duo", "Print zone", "Joint cover strip")

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 26, "az": 130, "args": ["--lens=40"],
     "note": "In a ward, seen from the open foot end, right and above (about 26 deg elevation): a patient on a 0.75 m field cot inside the "
             "1.2 m pod, a 1.75 m nurse at the foot end; walls 1.49 m apart at the joints, 1.91 m long"},
    {"name": "studio", "groups": ["shell", "internal"], "explode": False, "el": 40, "az": 130, "args": [],
     "note": "Studio view from the foot end and above (about 40 deg elevation): two zigzag halves meeting at the head centre, four feet with "
             "outriggers and bags, edge channels on the free ends"},
    {"name": "cutaway", "groups": ["open", "context"], "explode": False, "el": 30, "az": -140, "args": [],
     "note": "Head opened for resuscitation, seen from behind the head and left (about 30 deg elevation): both head leaves swung outward on "
             "their corner folds after the two centre clips are released"},
    {"name": "exploded", "groups": ["shell", "internal"], "explode": True, "el": 30, "az": 130, "args": [],
     "note": "Exploded view from the foot end and above (about 30 deg elevation): halves pulled apart, feet lowered, bags lifted"},
]


def product_parts():
    import context_parts
    out = []
    for q in M.option_fs1(context=True):
        d = dict(q)
        if q["kind"] == "context":
            d["group"] = "context"
        else:
            d["group"] = "shell" if any(k in q["name"] for k in _SHELL) else "internal"
        out.append(d)
    for q in M.option_fs1(context=False, head_open=True):
        d = dict(q)
        d["group"], d["name"] = "open", q["name"] + " (head open)"
        out.append(d)
    man = Pos(0.0, M.P["COT_Y0"] + M.P["COT_L"] + 700.0, 0) * Rot(0, 0, 180) * context_parts.mannequin(1750.0, "stand")
    out.append(dict(name="Nurse at the foot end (scale)", shape=man, material="clay", material_name="skin", color="#9C9C9E", kind="context",
                    bom=None, group="context", explode=(0, 0, 0), note=""))
    return out


if __name__ == "__main__":
    from collections import Counter
    print(Counter(p["group"] for p in product_parts()))
