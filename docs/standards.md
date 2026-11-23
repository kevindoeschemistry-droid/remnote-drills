# The house standard

The frameworks in `drills/frameworks/` are one standard of our own. Outside standards are how it is
kept honest. This page is the rulebook for both.

## What the house standard is

- **One path.** Every objective has a position from counting to 100 onward, and its prerequisites
  come before it. A framework `requires` other frameworks; an objective `needs` other objectives.
- **Stable codes.** `HT-2.2.A` is framework, unit, topic, objective. A code is never reused for a
  different objective, because drill cards, streaks and worksheets hang off it.
- **One shape.** Big ideas, units, topics, objectives (one testable action each, verb first), the
  knowledge each rests on, and the practices it exercises. Every subject uses the same shape, which
  is what lets a sport, a language skill and thermodynamics sit in one system.
- **Drills answer to objectives**, never to books or outside codes directly.

## What an outside standard is for

An outside standard does three jobs, in this order of strength.

1. **Structure**: the units and their order come from it (AP course descriptions, Common Core).
2. **Coverage check**: its outline is listed item by item in `drills/standards.yaml`, objectives cite
   the items, and the report shows which items nothing answers to (the FE Chemical specification).
3. **Reference**: it is named as a source but nothing cites it item by item.

Kinds are not equal. A curriculum standard or exam specification says what to learn. A rulebook says
what is legal, a rubric how performance is scored, a textbook how one author ordered the material.
A framework resting on the last three has its unit order chosen by us, and the report says so. A reference (CODATA, a regulation's definition of a teaspoon) is the source of truth for a number; it can back a card's value but never says the card belongs in the deck.

## Rules

1. Every framework declares `basis.primary`, and optionally `also` and `wanted`.
2. A standard is `read: full` only if its own text was read. Through someone else's table is
   `crosswalk`; named but unopened is `none`.
3. Cite at the highest level that is true: on the unit if the whole unit answers to the item, else
   the topic, else the objective.
4. Objectives nothing outside asks for are **house only**. That is allowed, and it is where the house
   standard goes beyond its sources (graduate material past an exam specification, for example). It
   should be a decision, not an accident, so the report counts them per framework.
5. When a standard is outlined, its uncovered items are the to-do list for new objectives.

## Moving a framework onto a standard

1. Read the standard's own text. Add it to `drills/standards.yaml` with its outline.
2. Add `std` citations. Do not renumber existing objectives.
3. Read the report. Uncovered items become new objectives at the end of the right topic (new letters,
   so old codes stand). House-only objectives stay, with the note explaining why.
4. Only then set it as `basis.primary`, and move the old basis to `also`.

## Where things stand

See `docs/coverage/standards.md`, rebuilt on every `npm run skills`.

## Quick recall: the basis found, and what it does not cover

Looked for in November 2026, for mental calculation, estimation and anchor quantities.

- **Mental calculation**: the UIL Number Sense sequencing charts (`uil-number-sense`, read in full). An exam specification
  with an itemised topic list at three levels and a published pace: 80 problems in 10 minutes, every tenth an estimate
  accepted within 5 percent. This is the basis to build a mental-math framework on.
- **Estimation**: Common Core already asks for it (`ccss-math`, held only through a crosswalk), and the Science Olympiad
  Fermi rules (`so-fermi`) give a scoring convention: the answer is a power of ten. A rulebook, so it shapes the checker,
  not the content.
- **Pace**: `uil-number-sense` (7.5 s a problem) and the English multiplication tables check (`sta-mtc`, 6 s a fact) are
  the published paces for recall.
- **Anchor quantities**: no published standard lists the magnitudes a chemist should know by heart. Two things were
  found on a second search: the SnapShot "Key Numbers in Biology" sheet (`snapshot-key-numbers`, read in full), a curated
  list for cell biology, and Francl's essay "Take a number" (`francl-take-a-number`, seen second-hand), which argues for
  anchor values in chemistry and names a few. `codata-2022` and `cfr-21-101-9` make each value checkable. The
  `anchor-quantities` framework uses the SnapShot for its biology units; its chemistry units are a house list and are
  labelled as one. The ACS anchoring-concepts content maps have still not been opened.


## Science breadth: school, olympiad, ACS, board and graduate standards (Nov 2026)

Registered in `drills/standards.yaml` and cited at unit level (DAT at topic level): NGSS high school
(`ngss-hs`), IB Chemistry, Physics and Biology for first assessment 2025, USNCO, IChO (Appendices C and
D of the regulations, plus the 12-section syllabus), the ACS Exams anchoring concepts (`acs-accm`), PE
Chemical, the GRE Physics Test and the discontinued GRE Chemistry Test, and the MCAT categories read so
far. Each standard's `read` and `note` say exactly how much of its own text was read; several could
only be read in part (the IB guides are sold to schools, ACS's USNCO page stops after seven topic bands,
the official IChO syllabus PDF was not reachable).

A unit citation measures **breadth**: some objective in that unit answers to the item. It does not
measure depth. AP-level units are cited against USNCO and IChO items, but olympiad problems ask the same
topics much harder; that gap is not visible in the report and is the reason for an olympiad layer.

What nothing answers to yet, grouped by what would have to be built:

1. **Descriptive inorganic chemistry.** IChO Appendix D (s-block, hydrides, oxides of C/N/S, p-block
   oxoacids, halogens, first-row transition-metal ions and colours, amphoterism, permanganate and
   dichromate, iodometry, identifying ions) and c16 (qualitative analysis); IChO syllabus section 5;
   USNCO band 2 is only covered through DAT's laboratory topic; GRE Chemistry inorganic (25%). The
   largest single gap and the one olympiads lean on most.
2. **Analytical chemistry.** GRE Chemistry analytical (15%), IChO syllabus section 12 and a9, MCAT 5C
   (separation and purification). Titration arithmetic exists in AP units; separations,
   gravimetry, complexometry and instrument choice do not.
3. **Polymers and materials.** IChO c22 and a5, IChO syllabus section 10, IB S2.4.
4. **Earth and space science.** 18 NGSS ESS expectations, IB B.2 (greenhouse effect), E.5 (fusion and
   stars) and Biology D4.3 (climate change). Needs a new framework; nothing in the Library touches it.
5. **Physics past AP:** special relativity (IB A.5, GRE 7) and laboratory methods (GRE 8); GRE
   classical mechanics also asks Lagrangian and Hamiltonian mechanics, which no physics unit has.
6. **PE Chemical:** mass-transfer applications (separations: distillation, absorption, extraction),
   and plant design, operation and safety (15–23 questions).
7. **Not drillable as cards:** NGSS design and engineering expectations (PS2-3, PS3-3, PS4-2, PS4-5,
   LS2-7, LS4-6, ETS1), USNCO Part III and IChO's practical skills. These are a house decision to leave
   out; written problems (USNCO Part II) are covered only as far as their single steps are.

Smaller single items: IB R1.3 energy from fuels, R3.3 radical (electron-sharing) reactions, Biology A2.1
origins of cells; ACCM X (visualization) as a concept of its own; IChO c21 (micelles).

### Built since (0.81–0.84, Nov 2026)

Groups 1–6 above now have frameworks: Inorganic Chemistry (IN) and Analytical Chemistry (AN) on IChO
Appendices C–D; Polymers and Materials (MT); Earth and Space Science (ES) on NGSS ESS; physics units 29–30
(special relativity, Lagrangian mechanics); Separations (SP) and Process Design, Economics and Safety
(PD) on FE Chemical 10/13/15/16 and PE Chemical 6.B/7; and a Chemistry Olympiad layer (CO) that asks AP
topics at USNCO-national and IChO depth. Coverage after that: IB Physics 24/24, PE Chemical 16/16, MCAT
(categories read) 14/14, IB Biology 39/40, IChO Appendices 41/42, NGSS 56/71.

Still open: the NGSS design and engineering expectations and USNCO Parts II–III (not drillable as
cards, by decision); NGSS ESS2-5, ESS2-7, ESS3-2, ESS3-4; IB Chemistry R1.3 (fuels) and R3.3 (radical
reactions); IB Biology A2.1 (origins of cells); IChO c21 (micelles); ACCM X (visualization); GRE Physics
laboratory methods; and on FE Chemical the math and statistics items (1.A, 1.F, 2.B–2.F), dynamics and
circuits (3.A–C), materials 4.B–C, the chemistry and biology of area 5, particle technology (11), and
design, ethics and environment items (13.C–D, 14, 16.D–F, 17).
