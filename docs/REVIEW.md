# FlexSleep Origami Patient Pod review note

**Media completed, 2026-11-12.** The Blender Cycles renders queued by this session were rendered on Amish's Mac: `media/options.png`, `media/render-hero.png`, `render-studio.png`, `render-cutaway.png` and `render-exploded.png` were composed and captioned, `media/card.png` and `media/social-preview.png` were made with `cards.py`, and `image_qc.py` passes. `render.py --check` passes. `release_gate.py` fails only on `stem_check: open` (Plausible rows wait on TRL 4 evidence; design decisions await Amish). Amish approved the repo as public on 2026-11-12.

## Session 2026-11-12: P0 to P3 (TRL 3) under kit 1.9.1-he

### What was done

- STEM check first ([docs/01b-stem-check.md](01b-stem-check.md), `docs/04-calcs/stem_check.py`, `stem_results.csv`, `stem_results_options.csv`) with the structure checks of STANDARDS 25.6a and the brief's questions (particles, heat, sightlines, cot sizes, patient pull, fire, resuscitation), built on FXP-PLT-001 v0.2 (cited, not edited); then an independent review by a separate `claude -p` process given only the results tables, `stem_check.py`, `sizing.py`, its results, `model.py`, the BOM and the cited sources (not `docs/platform/`).
- Three options at D3 in `cad/src/model.py` (FS1 68 parts, FS2 91, FS3 34; `cad/fidelity.json` passes D3, no interference); FS1 built from `cad/src/flex_parts.py`; per-part STEP for FS1 in `cad/step/FS1/`, assembly STEP per option.
- Pipeline documents: PRB, STM, PRC, OPT, URS, PRS, RTM (generated), CAL with `sizing.py`, BLD with pictures, DEC with DDR 0001 to 0003, REG, FEA, RSK (PHA and design FMEA), MKT, PLN (HE process content), CLM, VER, FTO.
- Drawings FXS-DWG-001 (GA) and 002 (foot); making sketches FXS-DWG-101 to 105; 3 STL files; concept media (hero, cutaway with the head opened, exploded, flow, viewer, blueprint).
- `cad/src/product_model.py`; render queue in `/home/claude/he5/renderq/flexsleep` (option scenes, `flexsleep__options_jobs.json`) and `/home/claude/he5/renderq/flexsleep/views` (`flexsleep__jobs.json`: hero, studio, cutaway, exploded).
- `project.yaml` to P3, TRL 3, `stem_check: open`, `design_state: constructable`; README with all sections.

### Key results (FXS-CAL-001)

- Plan 1,487 x 1,913 mm on joint lines; inner width 1,170 to 1,483 mm (cots of 600 to 1,000 mm leave 285 to 85 mm a side); wall top 1,212.5 mm.
- Mass 7.4 kg carried, 26.6 kg standing with 20 kg of sand; panels stack to 40 mm.
- Particles: walls take 84.9 % of horizontal directions from the mouth and 47.7 % of all directions; a supine cough leaves through the top; no airborne figure claimed.
- Heat: plume 52 to 59 m3/h at 4.1 to 5.4 K out of a 2.42 m2 open top; perforated band 1.2 % of the openings.
- Sightlines: lying patient hidden from most of the aisle, seen by a tall person within 0.64 m; seated eyes -64 to +98 mm about the top.
- Stability: free end tips at about 11 N outward and 9 N inward; a patient's pull to stand needs 137 to 281 N; rigid-pod bound 239 N; sliding 102 to 153 N; a 5 m/s gust gives 21.6 N on a side duo.
- Fire: 201 MJ per pod against a 144 MJ foam mattress; mattress flame about 2.2 m high; 25 kW/m2 out to 0.94 m.
- Access: head release 8 to 20 s (estimate); set-up 4.2 to 8.3 min (estimate); footprint 2.09 x 2.86 m with cot and head clearance, about 6.2 pods per 45 m2 tent against 10 beds.
- Value-engineering target USD 120; estimated cost of the constructable design USD 214.00 (USD 94.00 over); USD 4.28 a deployment over 50; first-prototype cash about USD 600.

### Requirements not met or at risk

- PR-007 stability against the 178 N push: **not met** (about 11 N at a free end); D5.
- PR-018 not a handhold: sign fitted, **hazard not closed** (D2).
- PR-008 fire: **at risk** (D7).
- PR-013 cost: **over target** (USD 214.00 against 120).
- PR-001 set-up under 5 min: at risk (4.2 to 8.3 min).
- PR-003 privacy: met lying down only; PR-004 observation: from the foot end only (D3).
- PR-006, PR-009, PR-012: to verify at TRL 4.

### STEM check

FS1 (S1 to S51): 15 within, 28 plausible, 8 fail with a fix that goes to Amish (S3 perforated band, S6 seated privacy, S7 observation panels, S10 push, S11 patient pull, S18 routine access, S20 fire, S40 tent gusts); none fails outright. Options (X1 to X11): 3 within, 4 plausible, 4 fail with a fix (FS2 tipping and cost, FS3 release, P18 variant). Fixes under the standing instruction of 2026-10-23: F1 round-core angle clip, F2 prohibition sign, F3 pinned outriggers, F4 pads, F5 head that swings open, F6 spacing and ignition rules, F7 edge channels, F8 joint strips, F9 head clearance, F10 A4 stainless.

Independent review (2026-11-12): of 49 rows, **28 held, 17 weak, 4 refuted** (S16 terminal leaf, S17 release time, S31 footprint, S34 sign colour), and **22 missed claims**, added as S39 to S51 or folded into rows. Each was checked with numbers before acting: the refuted rows led to F5, F7, F9, the corrected footprint and the prohibition sign; the weak rows were restated with the reviewer's corrections where verified. The reviewer's ISO 13857 finger band, ASHRAE comfort credit and burning-wall flux are recorded as its estimates, not verified here. Full record in FXS-STM-001.

### Decisions proposed and awaiting Amish (FXS-DEC-001)

- D1 concept: FS3 171, FS1 149, FS2 141 of 235; FS3 leads by 15 %, so the choice is Amish's. Recommendation: FS3 as the principle for the next stage with FS1's panels grafted on; FS1 carried now as the team concept.
- D2 patients who pull, roll or need help to stand. D3 wall height and restated privacy and observation claims. D4 drop the perforated band. D5 stated limit L1 for lateral loads. D6 routine care access (off-centre cot). D7 fire benchmark and acceptance (NFPA 286 and a bed-and-pod test; 1.0 m between pods). D8 ward layout and density. D9 tent doors and fans.
- On-product wording in FXS-CLM-001.
- To confirm when bought: C1 to C8.

### Platform requests (FXP-PLT-001; not edited here)

1. **Angle clip core.** `flex_parts.clip("angle")` puts the arms on a 12 mm square core, which stands 6 / cos 30 = 6.93 mm from the axis in the 150 deg slot, 0.93 mm proud of the 6 mm stop line: a panel cut to the platform hole pattern overlaps the core (147 mm3 in the interference check) and its holes miss the pegs by 0.93 mm against 0.5 mm of clearance. FlexSleep builds the same arms on a 12 mm round core in its model (F1). Proposed: a round core for the angle clip in the platform.
2. **Outrigger fixing.** Section 5.4 and `foot()` give the folded outrigger but no connection to the block; as drawn it butts the block and carries no moment, so it does nothing for tipping. FlexSleep adds a 100 mm triangular spigot on the block and a 6 mm stainless pin (F3). Proposed: adopt a spigot and pin in the platform foot.
3. **Rule S1 and free wall ends; the P2 factor.** S1 asks every vertical edge of a panel over 600 mm to be supported, which no open-ended plan (including the platform's own U bay) can meet at its free ends. The platform text calls the flat P12 figures "load margins" of 1.73 cold and 0.87 hot, but `platform_check.py` computes (h_cr / H)^3 with no load factor, so a free-edged P12 leaf buckles hot. FlexSleep bolts an aluminium channel over each free edge (F7). Proposed: state the free-end rule (edge stiffener or a turn of at least 30 deg within 600 mm) and correct the P2 wording.
4. **Angle foot.** The foot family has no kind for a 150 deg angle joint; FlexSleep builds a 120 x 70 x 40 mm block with slots on the two panel directions and one outside outrigger. Proposed: add an angle foot kind, and a one-outrigger option, to `foot()`.
5. **Joint slits.** Between and beyond the 100 mm clips, a 150 deg joint leaves an 11.6 mm slit the full height: a sightline, a droplet path and a finger gap. FlexSleep covers it with clear PP strips (F8). Proposed: a platform rule for joint slits near care zones.

### Build plan findings (design for construction, FXS-DDR-002)

Four duos in two halves rather than three panels; zigzag sides; no foot at the head centre so the head swings; pinned outriggers; edge channels on the free ends; joint strips; every made part has a making sketch and the printed parts an STL.

### Safety concerns

A patient pulling a wall over and falling (H1, FMEA RPN 192, the top item); panels in a bed fire (H2, RPN 150); delayed resuscitation if the release is slow or the head is against a wall (H3, RPN 108); tipping into the aisle from gusts or bumps; trip edges of outriggers and bags; oxygen enrichment inside three walls; false sense of protection (claims register). Release limitation in every document.

### Appearance model

`product_model.py` uses the FS1 parts as modelled, the cot and lying patient from `model.py`, a standing nurse from `context_parts.mannequin()`, and the head-open state of the same model for the cutaway render. No appearance deviations from `model.py`. Proposed, awaiting Amish: none.

### Checks that do not pass, and kit notes

- `python .kit/render.py --check` fails only on `media/options.png`, which needs the Blender renders of the exported option scenes; the storefront warning lists `media/render-hero.png`, `media/render-studio.png`, `media/render-exploded.png`, `media/card.png` and `media/social-preview.png`, also Blender-dependent. After the Mac renders: `python .kit/options.py --compose=<dir>`, caption the views with `.kit/photo_caption.py`, then `python .kit/cards.py .` and `python .kit/image_qc.py`.
- Twinwall is modelled as solid 4 mm sheet; masses in FXS-CAL-001 use the platform's 0.70 kg/m2 (the mass in `cad/fidelity.json` uses solid densities).
- The independent reviewer could not open the ACP Hospitalist and Staples pages (HTTP 403) or the NCFS table (TLS); the author read them on 2026-11-12.
- The cplast.net FR sheet price and the MatterHackers and Walmart prices are taken from the FlexTriage BOM of the same date, not re-fetched here.
- No git command that writes was run; committing and pushing are left to Amish.

### Recommended next step

Amish decides D1, D2 and D7, and the platform requests. On paper FS1 is ready for TRL 4 drills (set-up, head release, cot pull-out) and the decision-gate particle test, but not for use round sleeping patients until D2 and D7 are settled; if FS3 is chosen, it is modelled to P3 in a new session.
