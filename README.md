# KevinDoesChemistry Library — Kuta-style practice for RemNote

Each drill card generates a fresh problem on every review, checks the typed answer by its
defining property (never by string matching), and shows worked steps, a method box, and the
textbook section it comes from (Kreyszig, Incropera, Lay, Dill & Bromberg, Shell), linked to
your own PDF in RemNote.

## Data & network use

- Everything runs inside RemNote. The plugin makes **no network requests** and sends no data
  anywhere. Progress, PDF links and section anchors live in RemNote's plugin storage.
- Some drill cards show links to public lecture videos (YouTube, LearnChemE); they open in
  your browser only when you click them.

The plugin id stays `wiki-sync` (RemNote keys card maps, streaks and anchors to it); the
display name is **Drills**.

## The drill graph (`drills/`)

Four layers. Each answers one question:

| layer | file | answers |
|---|---|---|
| skills | `drills/skills.yaml` | *what* can be drilled: book-agnostic IDs (`ode1.separable`), domain, prereqs (may cross domains: `ht.lumped → ode1.separable`), templates, `live` / `planned` |
| sources | `drills/sources/*.yaml` | *where a book teaches it*: chapters → sections → skills, optional printed page ranges, wiki paths, notation conventions |
| courses | `drills/courses.yaml` | *which books a course uses* (UCI CBE 200 → Kreyszig, …) |
| PDF bindings | RemNote synced storage `drills.pdfBindings` | *which PDF in RemNote is that book*, plus the printed→PDF page offset. Rem IDs are RemNote's business, so they never live in the repo |

Old IDs (`separable`, `krey-ch01-separable`) remain `aliases`, so cards and
streaks survive renames. `scripts/build-skills.mjs` compiles the four into
`src/drills/skills.generated.json` and fails on any dangling reference.

### In RemNote

```
Wiki Flashcards / Drills
├── First-order ODEs / Separable equations / ODE drill · … (1..3)   ← cards: one home per skill
├── …                                                                  (Sources property: "Kreyszig 10e §1.3")
└── By textbook
    └── Kreyszig 10e — … / PDF: [[book]] / Ch 1 · … / §1.3 … / [[Separable equations]] · drill
```

Cards live under skills, so their review history never moves when books or
courses change. Books are views built from `sources/`. Each card header
shows the place in the book chosen by the *label source* setting, linked to
your copy of the book: **Drills: Anchor this section** (select a section heading
in the PDF first) turns it into a highlight tied to that section, so the drill label
(📖) opens your PDF right there, and the "By textbook" contents get a 📖 link
to it. Anchors and PDF links live in RemNote's synced plugin storage. Without an
anchor the label opens the linked PDF, and without a PDF, the wiki page.
**Drills: Link PDF to a textbook** binds a whole PDF to a book.

Each drill has a **Method** box (formula, when to use it, the usual traps), from
`drills/methods.yaml`. It works offline and on mobile.

Live now (37 skills):

| Domain | Skills |
|---|---|
| First-order ODEs | separable · substitution · integrating factor · IF + by parts · Bernoulli |
| Second-order | characteristic equation (distinct / double / complex roots, IVPs) · undetermined coefficients (polynomial, exponential, trig, modification rule, general solution) · Wronskian · mass–spring undamped (ω₀/T, IVP, amplitude–phase) · mass–spring damped (classify, over/critical/under IVPs) |
| Systems | A → B → C kinetics as a 2×2 system (matrix, eigenvalues, [B](t), [C](t), t_max) |
| Series | classify points · recurrence · first terms · radius of convergence · indicial roots · Frobenius case |
| Linear algebra (Lay 5e) | row reduction · independence · 2×2 inverse · 3×3 determinant · eigenvalues · eigenvectors |
| Heat transfer (Incropera Ch 1–4) | rate equations · energy balances · heat equation (q̇, flux, ∂T/∂t from T(x)) · plane & composite walls, contact resistance · cylinders, spheres, critical radius · generation (wall, rod) · pin fins (m, infinite, adiabatic tip, efficiency, tip temperature) · shape factors · finite-difference nodes |
| BVP | S–L eigenvalues · eigenfunctions · shifted spectrum y″ + (λ + c)y = 0 (eigenvalues, eigenfunctions, how many are negative) · self-adjoint form (p, q, r) · regular/periodic/singular |
| K–12 math (Common Core; OpenStax Prealgebra, Algebra & Trig, Intro Stats) | K–8: counting · place value · add/subtract · multiply/divide · fractions · decimals · measurement & data · ratios & percents · integers · expressions & equations · exponents · linear equations & functions · geometry · data & chance. HS: linear · functions · exponentials & logs · sequences · polynomials · quadratics · rational · complex · vectors & matrices · congruence · similarity · triangle trig · volume · coordinate geometry · circles · unit circle · identities · sinusoids · descriptive stats · bivariate data · probability · expected value. Placed on the LOs of `math-k8.yaml` and `math-hs.yaml`, so every unit has a test-out |

## Answer kinds (how answers are checked)

Never by string matching — the answer is evaluated and the defining property tested.

| kind | checked by |
|---|---|
| `ode` | plug into y′ = f(x, y); explicit or implicit; general needs C, IVP must not have one |
| `ode2` | plug into a y″ + b y′ + c y = f; initial conditions; a particular solution has no constants; a general one needs two constants on independent solutions (C₁e^{2x} + C₂e^{2x} is rejected) |
| `expression` | numeric equality (optionally up to a constant factor); engineering numbers use `rel` (within 1%), accept 2.5e4 / 25,000 / 2.5 x 10^4 / trailing units, and diagnose power-of-ten and sign slips |
| `recurrence` | any equivalent form or index shift, e.g. `(n+2)(n+1)a_{n+2} = 2n a_n`, `a_n = a_{n-2}/n` |
| `roots` | as a set |
| `indexed` | λₙ for 5 values of n (start index may be off by one) |
| `eigenfunctions` | −y″/y constant and matching an eigenvalue, both BCs hold, any constant multiple |
| `choice` | option match |
| `tuple` | per field; `proportional` allows one common factor (S–L p, q, r); `angle` compares mod 2π |

## Adding a skill

**As data (preferred for numeric, multi-step problems).** Write a template in
`drills/problems/<area>.yaml` — no TypeScript. It goes live on its skill by itself:

```yaml
- template: ht-gen-wall-conv
  skill: ht.generation
  given: { L: { pick: [0.01, 0.02] }, qdot: { pick: [1.0e+5, 1.0e+6] }, k: { pick: [5, 15] }, h: { pick: [100, 500] }, Tinf: 25 }
  let: { Ts: Tinf + qdot*L/h, Tmax: Ts + qdot*L^2/(2*k) }       # mathjs, in order
  require: [Tmax < 1200]                                          # redraw otherwise
  prompt: "A wall … $\dot q = {{qdot}}\,\mathrm{W/m^3}$ …"         # {{expr}} prints a value (4 sig figs)
  parts:                                                          # checked steps; the last is the final answer
    - { ask: "Surface temperature", label: Ts, tex: T_s, value: Ts, unit: "°C", explain: "…" }
    - { ask: "Maximum temperature", label: Tmax, tex: "T_{max}", value: Tmax, unit: "°C", explain: "…" }
  verify:                                                         # the independent check (tests/verify/data.py)
    var: x
    ode: "k*diff(T(x), x, 2) + qdot"                              # sympy solves the governing equation
    bcs: ["dT(0) = 0", "-k*dT(L) = h*(T(L) - Tinf)"]
    expect: { Ts: "T(L)", Tmax: "T(0)" }                          # or residuals: [balances that must vanish]
```

The build refuses a template whose parts aren't all covered by `verify`. In
RemNote the parts are asked one at a time (each checked, with **Show this step**)
until the skill has 3 in a row; after that only the final answer is asked, and a
miss walks back through the steps to find the one that broke.

**As code** (symbolic answers, odd shapes): write generators in `src/drills/gen-*.ts`,
register them in `registry.ts`, list them under the skill's levels in `skills.yaml`,
and add a first-principles case to `tests/verify/`.

Then `npm test`. Courses you've built in RemNote pick up new skills on their own.

### Symbolic answers in problems-as-data

A part of a `drills/problems/*.yaml` template can be an expression instead of a number: `expr: "n*a*(a*x + b)^(n - 1)"`
(with `vars: [x, h]` if it has more than `x`). The template's numbers are folded in (`src/drills/sym.ts`), the learner's
answer is checked as an expression, and `{{=expr}}` prints any expression the same way in a prompt or explanation.
`verify.expect` then recomputes it in sympy from the givens (`diff(...)`, `limit(...)`, `solve(...)`), and
`verify.choices` does the same for multiple-choice parts. The calculus templates (`ca-*.yaml`) are written this way.

### Cases, figures and authored keys

Three more things a `drills/problems/*.yaml` template can carry (see `mx-gaps.yaml`, `mx-judgment.yaml`, `mx-figures.yaml`):

- `cases:` a list of objects; one is drawn per problem and its fields join the givens. A field can be text (a formula
  to print, a sentence, a function to draw) or a list (a data set), which is how judgment items ("which technique?",
  "what kind of study?") and read-the-data items are written.
- `figure:` a picture drawn as SVG by `src/drills/fig-data.ts` from the same numbers the key uses: `plot` (curves,
  points, segments, slope fields, vector fields, scatter), `numberline` (points, dot plots, box plots, rulers), `grid`
  (unit squares, dots to count), `bars`, `table`. Numeric answers are checked with a relative tolerance, so a value
  part can never be 0: choose givens that keep read-off answers away from it.
- `verify: { authored: true }` for a key that is a matter of definition and cannot be recomputed. It is a statement
  that a person wrote the key and nothing checks it, so use it only when `verify.choices` cannot do the job, and say so
  when reporting coverage. Choice options are plain text (no TeX, no `^`).

## Standards

The frameworks are a house standard: our own objective codes, written to fit together along one path. Outside standards
(Common Core, AP course descriptions, the FE exam specifications, CS2023 and so on) are what it is checked against.
`drills/standards.yaml` lists them with their kind and how fully each was read; every framework declares a `basis`; and
units, topics or objectives cite outside items with `std`. `docs/coverage/standards.md` (rebuilt by `npm run skills`)
shows the basis of every framework, how many objectives are anchored outside, and which items of an outlined standard
nothing answers to yet. `docs/standards.md` has the rules for adding a standard or moving a framework onto one.

## The path and the Library

`drills/frameworks/*.yaml` are curriculum maps (AP/IB style: units → topics → learning objectives,
with essential knowledge, practices, official standard codes and prerequisites). Each declares the
frameworks it `requires`; `node scripts/framework.mjs` orders all of them into one start-to-finish
path (K.CC.A.1 "count to 100" is #1), checks every prerequisite comes first, and writes
`docs/frameworks/PATH.md` and the data the plugin bundles. `scripts/path-page.mjs` builds the
browsable page `docs/path/index.html`.

In RemNote, the sidebar's **Path** tab builds *KevinDoesChemistry Library* (Track › Framework ›
Unit › Topic › Objective, in path order, each objective with its standard, essential knowledge and
linked prerequisites, and a drill card wherever drills exist), shows the next objective you haven't
mastered on each track, runs unit test-outs (80% to pass), and lets you mark what you already know.

## Using it in RemNote

Three commands: **Drills: Open** (the sidebar: Path, Practice in course order with the gaps
shown, Exam mix for the course's next exam, Courses to build one and the setup tools),
**Drills: Anchor this section** and **Drills: Link PDF to a textbook** (both need a PDF open).

### Warm-up mix

**Practice → Warm-up mix** serves random problems from everything that is already easy: any skill or objective you once
got five in a row on, plus objectives marked known or tested out of on the Path tab. It never ends and nothing in it can
be finished. Something you haven't done for a week comes up three times as often as something done today, and a miss
never takes an item out. Chips narrow the mix to one subject.

A skill that reached five in a row is shown as **Warm ✓** with its rep count and when you last did it. In storage the
field is still `cleared`, and course skills still get the RemNote tag `Cleared ✓`, because Study Companions counts that
tag for badges.

The Path tab only shows objectives that have a drill, and only the tracks that have any. **Show the N objectives without
drills** at the bottom brings back the whole map. In the Library itself, a unit or framework with nothing to practice
has "· no drills yet" in its title.

### The Library

**Path → Build the Library** puts every framework in RemNote in path order (track → framework → unit → topic → objective).
Every framework gets its outline. Drill cards are flashcards in your queue, so they are made only for the frameworks ticked
before building; school maths (K–8 and high school) starts unticked. Change the ticks later under **Drill cards** and press
**Update the Library**: ticking adds cards, unticking stops new ones and keeps the cards already made.

- A new Library card for an objective whose skill you already cleared in a course starts cleared.
- If a course card drills a skill the Library now covers in full, the Path tab offers to pause the course cards so each
  drill is due once. Pausing deletes nothing and **Resume them** turns them back on.

## Develop

```bash
npm install
npm run dev     # http://localhost:3005 (RemNote → Plugins → Build → Develop from localhost)
npm test        # every template × 30 seeds: JS checker + negative controls + KaTeX, then sympy cross-check
npm run build   # dist/ + PluginZip.zip
```

`npm run skills` compiles `drills/` (skill graph, textbooks, courses) into
`src/drills/skills.generated.json`; it runs automatically before dev/build/test
and fails on any dangling reference.

## Release

Every push and pull request runs `.github/workflows/build.yml`: version check, type check, `npm test`, `npm run build`.
The run keeps `PluginZip.zip` as an artifact, so no build has to happen on your own machine.

1. Bump the version in `package.json` (both places) and `public/manifest.json`. `node scripts/check-version.mjs` confirms they agree.
2. Merge to `main`.
3. `git tag v0.28.0 && git push origin v0.28.0`. The tag build publishes a GitHub Release with `PluginZip.zip` attached.
4. Download the zip and upload it in RemNote → Plugins → Build → Upload plugin. RemNote has no upload API, so this step stays manual.

## Worksheets

`npm run worksheets -- heat-transfer` writes one printable worksheet per unit to `docs/worksheets/heat-transfer/`:
a problem for every drilled learning objective, then a step-by-step answer key on its own pages. The problems come from
the same generators as the RemNote cards, so a worksheet is a fixed set of seeds.

- `--seed 2` gives a different version of every problem; the same seed always gives the same worksheet.
- `--per 3` gives three problems per objective.
- Any framework id in `drills/frameworks/` works in place of `heat-transfer`.
- Objectives with no full drill are listed in the worksheet footer and on the index page.

Open a unit in a browser and print it (or save as PDF).

### Google Docs

`scripts/gdoc.ts` writes a unit as HTML that Google Drive converts into an editable Doc, in the layout of the
hand-made worksheets (name and date line, italic unit line, boxed method callout, Roman-numeral sections).

```bash
npx tsx scripts/gdoc.ts heat-transfer 1                       # tests/out/gdoc/heat-transfer-unit-01.html + .regions.json
python3 scripts/gdoc_math.py tests/out/gdoc/heat-transfer-unit-01.html \
  docs/worksheets/heat-transfer/gdoc/img <public base URL of that folder>
```

- Symbols, subscripts, superscripts and units become real Doc text. Fractions and other 2-D math become images whose
  alt text is the LaTeX; Google fetches them by URL at conversion, so the image folder has to be pushed first.
- Every problem and every answer-key entry starts with a grey marker such as `⟦HT-1.1.B·s1⟧`. Leave the markers in place.
- `docs/worksheets/<framework>/gdoc/docs.json` records which Doc belongs to which unit.

**Pulling edits back.** Read the Doc back as text, save it to a file, then:

```bash
npx tsx scripts/gdoc-pull.ts tests/out/gdoc/heat-transfer-unit-01.regions.json doc.txt --write
```

Each line under a marker is compared with what was written:

- **Reworded line**: saved with every `$math$` piece kept as the repo has it.
- **Added line**: saved as a note after the line above it, and put back there on the next `gdoc.ts` run.
- **Changed number or symbol**: reported and not saved. Change that in the generator.
- **Removed line**: reported and not saved.

Edits are stored in `drills/worksheets/<slug>.yaml`. Headings, the header lines and the callout box are not tracked.

## Wiki links

Sources point at wiki pages with `wiki:` (book, chapter or section). `node scripts/check-wiki.mjs` checks every one
against `drills/wiki-pages.json`, a snapshot of the wiki's textbook folders, and fails on a dead link. It runs as part
of `npm run skills`, so `npm test` and the build catch a broken link too.

- After adding, renaming or removing wiki pages: `node scripts/check-wiki.mjs --wiki <path to the wiki repo>` refreshes the snapshot.
- `docs/coverage/wiki-links.md` lists, per source, the sections that teach a skill but have no wiki page, and the wiki
  drill pages no section points at.

