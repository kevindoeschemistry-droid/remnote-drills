# Wiki Sync — drills for RemNote

Kuta-style drill-and-kill practice inside RemNote: each drill card generates a
fresh problem on every review, checks the typed answer by its defining property
(never by string matching), and shows worked steps labelled with the textbook
section (Kreyszig, Incropera, Dill & Bromberg, Shell).

## Data & network use

- **Drills** run entirely inside RemNote. No network access; nothing leaves your
  knowledge base. Streaks and PDF links live in RemNote's plugin storage.
- **Sync Wiki Cards** (only when you run it) downloads one public file,
  `https://wiki.kevindoeschemistry.com/flashcards.json`, and creates flashcards
  from it. No user data is sent anywhere.
- Card headers link to pages on `wiki.kevindoeschemistry.com` (ordinary links).


The plugin does two jobs:

1. **Sync Wiki Cards** — pulls `flashcards.json` from the deployed wiki into
   `Wiki Flashcards → Textbook → Chapter` (published by the wiki).
2. **Drills** — Kuta-style drill-and-kill inside RemNote. Every review card
   generates a new problem and checks the typed answer.

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

1. Add it to `drills/skills.yaml` (status `planned` first is fine) and list it under the sections that teach it in `drills/sources/*.yaml`.
2. Write generators in `src/drills/gen-*.ts` — build each problem backward from a clean answer — and register them by name in `registry.ts`.
3. Flip the skill to `live` with its template names, run `npm test`, then *Drills: Create drill cards & book contents* in RemNote.

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
