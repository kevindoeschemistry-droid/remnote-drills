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

## Using it in RemNote

Three commands: **Drills: Open** (the sidebar: Practice in course order with the gaps
shown, Exam mix for the course's next exam, Courses to build one and the setup tools),
**Drills: Anchor this section** and **Drills: Link PDF to a textbook** (both need a PDF open).

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
