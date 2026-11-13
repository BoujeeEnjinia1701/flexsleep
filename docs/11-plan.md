---
doc_id: FXS-PLN-001
title: FlexSleep Origami Patient Pod project plan
project: FlexSleep Origami Patient Pod
doc_type: Project plan
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First project plan with the Helpful Engineering process content (STANDARDS 25.7)
---

# FlexSleep Origami Patient Pod project plan

The project is at P3 (TRL 3 on paper). The next step is Amish's decisions D1, D2 and D7 (concept, patient rule, fire case); then, once the portfolio cap allows, a TRL 4 build of one pod for the release and deployment drills and the decision-gate particle test.

Release limitation (STANDARDS 25.5b): no prototype is used in patient care until its stability, fire performance, cleanability and the procedure it embeds are reviewed by qualified IPC and safety staff.

## Purpose

Give patients in crowded emergency wards and shelters visual privacy lying down and a physical boundary against contact and sideways splashes at each bed, in a pod that opens in seconds and supports, never replaces, IPC practice.

## Kill criteria (project stop rules, not a product claim)

As FXS-PRB-001: no measurable particle-exchange effect and no demand for privacy alone; head release over 30 s in a drill; fire case refused (D7); patient pulls and falls not controllable (D2); pods cost more than about 40 % of beds.

## Targets and KPIs

| KPI | Target | Now (paper) |
| --- | --- | --- |
| One-person set-up | under 5 min | 4.2 to 8.3 min estimate |
| Head release | under 30 s | 8 to 20 s estimate |
| Particle exchange to the next bed against an open bed | measured reduction (decision gate) | Unknown (S2) |
| Parts cost | USD 120 (stretch 75) | USD 214.00 |
| Beds per 45 m2 tent | at least 7 | about 6.2 |
| Fire case accepted by a site fire officer | yes | Open (D7) |

## Minimum team

Design lead (Design Molecule Labs); Helpful Engineering CAD volunteer (folds and joints, as the deck asks); airflow or environmental engineer (particle test design); materials and fire engineer (FR reports, bed-and-pod test); clinical adviser (resuscitation and IPC); field partner contact.

## 60 to 90 day plan (on hold beyond TRL 3 until the cap lifts)

| Days | Work | Output |
| --- | --- | --- |
| 0 to 15 | Amish decides D1, D2, D7; buy the platform standards (FXP-PLT-001 D16) | Decisions recorded |
| 15 to 45 | Build one pod to FXS-BLD-001; drills V2 (set-up, release, egress) | TRL 4 test report (planned) |
| 30 to 60 | Particle test V1 with a test partner; thermal V3 | Decision-gate evidence |
| 45 to 90 | FR reports, NFPA 286 or bed-and-pod test plan with the site (D7); user acceptance V4 with a field team | Go or stop on the kill criteria |

## Support needed from Helpful Engineering

CAD designer for the fold and joint details; airflow or environmental engineering support for the particle test; materials selection (halogen-free FR, sealed bags); access to field cot and mattress sizes (MSF, IRC).

## External partners

Field hospital operators (MSF, IRC) for ward configuration and acceptance; an infection control testing partner for particle separation; humanitarian health practitioners for patient feedback; a fire test house for NFPA 701, E84 and NFPA 286; FEMA for viability input (all to engage).

## Stage gates

| Gate | Evidence | Status |
| --- | --- | --- |
| P3 (TRL 3) | This repo: STM, OPT, PRS, CAL, CAD at D3, BOM, BLD, DEC | Reached on paper |
| P4 (TRL 4) | V1 to V4 reports, T1 to T8 platform tests | On hold (cap) |
| P5 (TRL 5 to 6) | Field trial with a partner | On hold |
| P6 | Launch plan with a deployment partner | On hold |

## Next steps and decision request

Amish: D1 (FS3 recommended for the next stage; FS1 carried), D2 (patient rule), D7 (fire benchmark and acceptance), then D3 to D9 and the platform requests in docs/REVIEW.md.

## References

All sources are listed with links and the date checked (2026-11-12) in FXS-STM-001, FXS-REG-001, FXS-MKT-001, FXS-FTO-001, `bom/bom.csv` and FXP-PLT-001.

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
