# What each framework is based on, and where the holes are

Snapshot of 2026-11-18 (plugin 0.30.0). Regenerate the counts with `npm run skills`.

## Basis and drill coverage

"Opened" means the standard's own text was read while drafting. "Crosswalk" means it was read
through someone else's correlation table because the original could not be fetched.

| Framework | Built from | How firmly | Objectives | With a drill |
|---|---|---|---|---|
| Mathematics K–8 | Common Core State Standards | Crosswalk (NC DPI reprint; corestandards.org was blocked) | 258 | 195 |
| High School Mathematics | Common Core Appendix A, traditional pathway | Opened | 200 | 130 |
| Calculus | AP Calculus AB/BC Course and Exam Description | Opened, plus Larson correlation for LO codes | 173 | 13 |
| Applied Engineering Mathematics | UCI CBE 200 catalogue line + Kreyszig 10e | Course has no public syllabus; shaped by the book | 118 | 93 |
| Chemistry | AP Chemistry CED (Fall 2024) | Partly opened (text extraction truncated; LOs for Units 1–2 only) | 179 | 7 |
| Physics | AP Physics 1, 2, C CEDs | Partly opened (topic lists; LO codes for a few units) | 201 | 4 |
| Biology | AP Biology CED (2019) | Crosswalk (Mader correlation; College Board blocked) | 178 | 0 |
| **Physical Chemistry** | Engel & Reid 3e, via the wiki's 141 drill pages | **Textbook-shaped. The ACS content map and CPT supplement were not opened** | 141 | 61 |
| Programming Foundations | AP Computer Science A CED (Fall 2025) | Opened | 140 | 0 |
| Computer Science | ACM/IEEE CS2023 Body of Knowledge | Opened | 140 | 0 |
| Information Systems | ACM/AIS MSIS 2016 | Opened | 53 | 0 |
| Heat Transfer | NCEES FE Mechanical and Chemical specs + UCI MAE 120 + Incropera 8e | Opened | 98 | 92 |
| Thermodynamics and Statistical Mechanics | UCI CBE 240 catalogue line, UCSB ChE 210A, Dill & Bromberg, Shell | Course has no public syllabus; shaped by the books | 124 | 81 |
| Molecular Simulation | No standard exists; LiveCoMS best-practice papers + Hayes group tutorial | Triangulated | 102 | 0 |
| Dental Admission Test | ADA DAT 2026 Candidate Guide | Opened | 183 | 0 |
| AI Safety | BlueDot Technical AI Safety course + lab frameworks | Opened | 104 | 0 |
| Speaking and Articulation | NCA Competent Speaker form + research | Opened | 69 | 0 |
| Basketball | USA Basketball Player Development Curriculum | Partly opened | 88 | 0 |
| Swimming | World Aquatics rules + coaching literature | Opened | 88 | 0 |
| Wushu | IWUF 2024 competition rules | Opened (mirror) | 88 | 0 |

Total: 20 frameworks, 2,725 objectives, 676 with a drill.

## Hole 1: standards that were never read directly

- **Physical Chemistry**: ACS Exams Institute Anchoring Concepts Content Map IV (J. Chem. Educ. 2018, 95, 238) and the ACS CPT Physical Chemistry Supplement. Until one is read, the unit order is Engel & Reid's.
- **Chemistry, Physics**: only part of each AP CED was extracted. Later units have topic titles but paraphrased objectives.
- **Biology, K–8**: read through a third party's correlation table.
- **Engineering Mathematics, Thermodynamics**: the UCI courses publish no syllabus, so the textbook is doing the standard's job. A syllabus from the instructor would fix this.

## Hole 2: frameworks with no drills at all

Biology, Programming, Computer Science, Information Systems, Molecular Simulation, DAT, AI Safety,
Speaking, Basketball, Swimming, Wushu. Eleven of twenty. Some of these (speaking, the three
sports) are observable skills that a typed-answer drill does not fit; they need a different kind
of item, not more generators.

## Hole 3: drilled thinly

Calculus 13 of 173, Chemistry 7 of 179, Physics 4 of 201. These sit under everything else on the
path, so they matter more than their size suggests.

## Hole 4: wiki subjects with no framework

The wiki has 121 textbooks; 97 have drill pages. Subjects there with no framework to hang a
generator on:

| Wiki subject | Books | Books with wiki drills | Framework |
|---|---|---|---|
| Linear Algebra | 6 | 6 | none (drills exist under Engineering Mathematics for Lay only) |
| Physics (upper division: quantum, E&M, classical, solid state) | 6 | 6 | none above AP level |
| Computational Chemistry & Physics | 6 | 6 | Molecular Simulation covers MD only |
| Inorganic & Electrochemistry | 3 | 3 | none |
| Organic and Medicinal Chemistry | 3 | 3 | none |
| Chemical Engineering (transport, reaction engineering, separations) | 4 | 4 | Heat Transfer only |
| Materials Science & Biomaterials | 5 | 5 | none |
| Biochemistry & Cell Biology | 9 | 9 | none above AP Biology |
| Machine Learning & AI | 4 | 4 | none |
| Quantitative Finance, Factor Investing, Trading, Stat Arb, Options | 23 | 23 | none |
| Cybersecurity, Crypto, Cyber Policy | 8 | 8 | none |
| CBRN, Forecasting | 4 | 4 | none |
| Civil Engineering | 18 | 0 | none |
| Linguistics | 6 | 0 | none |

## Hole 5: inside Physical Chemistry

61 of 141 objectives have a generator, 14 are partly covered, 66 have none. The 66 are mostly the
ones that are not a single number: operators and eigenfunctions, term symbols, point groups and
character tables, MO diagrams, mechanisms. Those need symbolic or multiple-choice items.

## Hole 6: books RemNote drills from that the wiki doesn't have

Incropera, Shell, and the three OpenStax texts have no wiki pages, so their sections link nowhere.
