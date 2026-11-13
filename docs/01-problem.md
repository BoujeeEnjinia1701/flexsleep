---
doc_id: FXS-PRB-001
title: FlexSleep Origami Patient Pod problem statement
project: FlexSleep Origami Patient Pod
doc_type: Problem statement
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First problem statement from the Helpful Engineering project update (iteration 2), with cited burning platform, users, personas, constraints and kill criteria
---

# FlexSleep Origami Patient Pod problem statement

Overcrowded emergency care puts patients in open, shared sleeping space with no privacy and open contact and large-droplet paths between beds. Field hospital operators, shelter managers and humanitarian health teams need a light, foldable micro-boundary round a cot that gives a patient visual privacy and a physical boundary against direct contact and sideways splashes, keeps the patient in sight of staff, opens in seconds for resuscitation and adds as little fire risk as possible beside bedding. This statement draws on the Helpful Engineering project update for the FlexSleep Origami Patient Pod (concept iteration 2) and is a proposal for review with a co-design partner. CONCEPT, NOT FOR FABRICATION.

Release limitation (STANDARDS 25.5b): no prototype is used in patient care until its stability, fire performance, cleanability and the procedure it embeds are reviewed by qualified infection prevention and control (IPC) and safety staff.

## Burning platform

- Surge wards run at a density where privacy infrastructure does not exist. MSF's cholera guideline plans "approximately 30 m2 per patient" for a whole centre but about 4 m2 of ward space per bedridden patient, and "a 45 m2 tent can hold 10 beds + one nurse station" ([MSF medical guidelines, cholera treatment centres](https://medicalguidelines.msf.org/en/viewport/CHOL/english/6-1-cholera-treatment-centres-ctc-25296944.html), checked 2026-11-12).
- General ward guidance asks for "at least 2.5 metres, measured from the centre of one bed to the centre of the next bed" and beds "separated by curtains (both for privacy and for infection control during cough-generating procedures)" ([Bettercare, IPC considerations for healthcare facility design, section 5-5](https://bettercare.co.za/infection-prevention-and-control/05.html), checked 2026-11-12). Field wards rarely have either.
- Large respiratory droplets fall within short distances: the largest droplets that evaporate before falling 2 m are 60 to 100 um; larger ones exhaled at 1 m/s travel under 1 m and at 10 m/s (coughing) more than 2 m (Xie et al. 2007, *Indoor Air* 17: 211-225, abstract checked 2026-11-12 on [SciSpace](https://scispace.com/papers/how-far-droplets-can-move-in-indoor-environments-revisiting-47zol844og)). A boundary close to the bed intercepts sideways splashes; it does not stop aerosols.
- The evidence for partitions against airborne spread between beds is weak and mixed: a 2021 review found "limited evidence to support the use of 2 metres physical distancing and partition screens within healthcare" and studies where partitions raised exposure near the source ([Rooney et al. 2021](https://eprints.whiterose.ac.uk/181044/1/Evidence%20review%20of%20physical%20distancing%20and%20partition%20screens%20to%20reduce%20healthcare%20acquired%20SARS-CoV-2.pdf), checked 2026-11-12). The team's decision gate (a measured reduction in airborne particle exchange) is therefore an open question, not a premise.
- Commercial answers cost more than the team's target: a 3-panel FR vinyl privacy screen on casters is USD 210.79 ([Staples, Medline MDS80450](https://www.staples.com/medline-foldable-flame-retardant-vinyl-privacy-screen-with-casters-3-panel-69-x-87in-mds80450/product_829862)) and a 3-panel steel frame screen USD 235.57 ([MDMaxx, Winco 3130](https://mdmaxx.com/products/winco-3130-privess-basic-3-panel-steel-frame-folding-screen-with-standard-white-vinyl)), both checked 2026-11-12, and one screen covers only one side of a bed.

## Users and context

Table 1. Users and needs.

| User | Context | Need | Persona |
| --- | --- | --- | --- |
| Field hospital operator | Surge or outbreak ward in a tent or hall, rows of field cots | Privacy and order between beds without losing beds or blocking care | P1 |
| Ward nurse | Night and day rounds, gloved, many patients | Sees every patient from the aisle; reaches the patient; opens the pod at once in an arrest | P2 |
| Shelter manager | Displacement shelter, mixed families, mats and cots | Dignity and a defined personal space, low cost, packs away | P3 |
| Patient | Febrile, frail or frightened; may be delirious; may need help to stand | Privacy lying down, not shut in, nothing that falls on them or looks like a handhold | P4 |
| Logistician | Ships and stores kits with other relief items | Flat pack, known mass, few loose parts | P5 |
| Volunteer setting up | No training, alone, ward already occupied | Pictures, parts that only fit one way, one-person set-up | P6 |

### Personas

- **P1 Dr. Mensah, field hospital operator.** Runs a 40-bed respiratory surge tent; wants privacy without losing a quarter of the beds.
- **P2 Ana, ward nurse.** Does night rounds with a torch; must see chests rising from the aisle and start CPR in seconds.
- **P3 Karim, shelter manager.** Runs a school-hall shelter of 120 people; families ask for privacy for a sick relative.
- **P4 Mr. Osei, patient.** 72 years old, febrile, needs a hand to stand; pulls on whatever is beside the bed.
- **P5 Joy, logistician.** Counts kilograms and cubic metres per bed; stores pods with tents and cots.
- **P6 Sam, volunteer.** Sets pods round cots in a ward that is already full.

### Stakeholders

Table 2. Stakeholders.

| Stakeholder | Interest | How they shape the design |
| --- | --- | --- |
| Helpful Engineering (project team) | Open, low-cost hardware for crisis settings | Source deck, decision gate, volunteer support |
| Design Molecule Labs | Constructable open design at TRL 3 | Kit standards, shared Flex platform (FXP-PLT-001) |
| Field hospital operators (MSF, IRC, named in the deck as partners to explore) | Ward layout, acceptance | Validate fit, density and procedure (to engage) |
| FEMA (named in the deck) | Viability input | Review of deployment cases (to engage) |
| Site fire safety officer | Fire load beside bedding, oxygen, exits | Placement rules and fire benchmark (FXS-REG-001) |
| IPC lead at the receiving site | Cleaning, touch surfaces, claims | Procedure review before any patient use |
| Resuscitation lead | Access to the head and chest in an arrest | Release procedure and drill (FXS-VER-001 V2) |
| Infection control testing partner (named in the deck) | Particle exchange against a baseline | Decision-gate test (V1) |
| Funders (the deck cites the US rural health fund) | Cost per pod and per patient night | Value-engineering target |

## Constraints

- Shared Flex platform (Amish, 2026-11-12): FXP-S4FR 4 mm FR polypropylene twinwall, the clip-lock family, feet, print and colour rules and the structural rules S1 to S4, L1 and L2 (FXP-PLT-001).
- Indoor or in-tent use only (FXP-PLT-001 L2, proposed).
- Value-engineering target USD 120 per pod; stretch under USD 75 at volume (team deck).
- Team targets: three pre-scored panels (head, left, right) round a cot or mattress 60 to 100 cm wide; perforated lower band and open top for passive airflow; semi-transparent upper panels for observation; snap connectors; one-person deployment in under 5 minutes; all panels stack to 10 cm; compatible with standard disinfection and repeated deployment.
- Field cots in range: MSF field hospital bed 190 to 200 x 75 to 85 cm, lying surface 50 to 55 cm high ([MSF UniCat 12947](https://unicat.msf.org/cat/product/12947)); NATO style camp bed 190 x 64 x 40 cm ([SP Services](https://www.spservices.co.uk/Equipment/Treatment-Room/Furniture/Emergency-Foldable-Camp-Bed---NATO-Style/p/CH4689)); military style folding cot 78 x 28 x 18 in, about 1,981 x 711 x 457 mm ([School Health](https://www.schoolhealth.com/military-style-folding-cot)); all checked 2026-11-12.
- No medical device claim; claims follow STANDARDS 25.5b (FXS-CLM-001).

## Out of scope

- Airborne barriers or filtration: panels are boundaries, not barriers (FXP-PLT-001 L1); the iteration 1 HEPA unit is not carried (the CleanAir project covers air).
- Any support function: the pod is not a bed rail, grab rail or handhold.
- Outdoor use without a tent (FXP-PLT-001 L2).
- Acoustic privacy.

## Prior work

- Team iteration 1: aluminium pole frame with rigid polycarbonate panels, four sides with a zipped entry and a HEPA unit on the frame, dropped on weight, bulk and the complexity of a bespoke filter.
- Commercial: hospital cubicle curtains on ceiling tracks, mobile FR vinyl privacy screens, disposable privacy curtains with an NFPA 701 pass (FXS-MKT-001).
- Patents on portable bed enclosures, bed canopies and rail-clamped privacy screens (FXS-FTO-001).

## Kill criteria (project stop rules, not a product claim)

The project stops or changes course if any of these holds at TRL 4:

- The decision-gate test shows no measurable reduction in particle exchange against an unshielded baseline and field partners do not want the pod for privacy alone.
- Staff cannot open the head for resuscitation in under 30 s in a drill.
- A bed-and-pod fire test or the site fire review judges FR twinwall round bedding unacceptable (FXS-DEC-001 D7).
- Patients pull on walls or fall in user trials despite the signs, and no layout or patient rule controls it (D2).
- Pods cost more than about 40 % of a ward's beds at the operator's density.

## User research and co-design

Every target here is a proposal until tested with a field hospital team and patients: cot fit, wall height, who may use a pod, how it is opened, how it is cleaned and how close pods may stand.

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
