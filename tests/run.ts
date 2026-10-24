/* Drill engine tests:  npm test  (runs this, then tests/verify_sympy.py)
 *
 * For every live skill in drills/skills.yaml and every template it names:
 *   1. the reference answer is accepted by the checker
 *   2. negative controls (perturbed answers, wrong IC, wrong option…) are rejected
 *   3. all prompt / step / answer LaTeX renders in KaTeX (what RemNote uses)
 * Plus hand-written student-style answers per answer kind, graph integrity checks,
 * and a dump to tests/out/problems.json for the independent sympy check.
 */
import * as fs from "fs";
import * as katex from "katex";
import { LIVE_SKILLS, ALL_SKILLS, resolveSkill, placesFor, placeText, primaryPlace, SOURCES } from "../src/drills/skills";
import { generate, generateTemplate, TEMPLATES } from "../src/drills/registry";
import { check } from "../src/drills/check";
import type { Answer, Problem } from "../src/drills/types";
import { LAPLACE_FOURIER_CASES } from "./cases/laplace-fourier";

let failures = 0;
const fail = (msg: string) => {
  failures++;
  if (failures < 60) console.log("FAIL:", msg);
};
const SEEDS = Number(process.env.SEEDS ?? 30);

// ── reference / perturbed inputs per answer kind ───────────────────────────
function reference(p: Problem): string | string[] {
  const a = p.answer;
  switch (a.kind) {
    case "ode": return a.ref;
    case "ode2": return `y = ${a.ref}`;
    case "expression": return a.ref;
    case "recurrence": return `a_{n+${a.gap}} = (${a.ref.replace(/m/g, "n")})*a_n`;
    case "roots": return a.ref.join(", ");
    case "indexed": return `${a.label} = ${a.ref}`;
    case "eigenfunctions": return `y_n = ${(p.meta as any).y}`;
    case "choice": return a.correct;
    case "tuple": return a.fields.map((f) => f.ref);
  }
}

function negatives(p: Problem): (string | string[])[] {
  const a = p.answer;
  switch (a.kind) {
    case "ode": return [`${a.ref} + exp(x/3)/7`];
    case "ode2": {
      const out = [`y = ${a.ref} + 0.01*${a.v}`];
      if (a.ic || a.particular) out.push(`y = 1.01*(${a.ref})`);
      if (!a.ic && !a.particular) out.push(`y = ${a.ref.replace(/C2/g, "C1")}`); // dependent constants
      return out;
    }
    case "expression":
      if (a.rel) return [`(${a.ref})*1.03`, `(${a.ref})*10`, `-(${a.ref})`];
      return [(a.vars ?? ["x"]).length ? `${a.ref} + x/7` : `${a.ref} + 0.01`];
    case "recurrence":
      return [
        `a_{n+${a.gap}} = (${a.ref.replace(/m/g, "n")} + 1/(n+5))*a_n`,
        `a_{n+${a.gap + 1}} = (${a.ref.replace(/m/g, "n")})*a_n`,
      ];
    case "roots": return [[a.ref[0] + 1, ...a.ref.slice(1)].join(", ")];
    case "indexed": return [`${a.ref} + 1`, `2*(${a.ref})`];
    case "eigenfunctions": {
      const y = (p.meta as any).y as string;
      return [y.includes("sin") ? y.replace("sin", "cos") : y.replace("cos", "sin"), `${y.replace("x)", "x/2)")}`];
    }
    case "choice": return a.options.filter((o) => o !== a.correct);
    case "tuple":
      return a.proportional
        ? [a.fields.map((f, i) => (i === 0 ? `(${f.ref})*(1 + x)` : f.ref)), a.fields.map((f, i) => (i === 1 ? `${f.ref} + 1` : f.ref))]
        : [a.fields.map((f, i) => (i === 0 ? `${f.ref} + 0.1` : f.ref))];
  }
}

const texChunks = (s: string) => [...s.matchAll(/\$([^$]+)\$/g)].map((x) => x[1]);
function katexOk(where: string, tex: string) {
  try {
    katex.renderToString(tex, { throwOnError: true });
  } catch (e) {
    fail(`${where}: KaTeX error in "${tex}": ${(e as Error).message}`);
  }
}

// ── 0. graph integrity ─────────────────────────────────────────────────────
for (const s of LIVE_SKILLS) {
  for (const t of Object.values(s.levels).flat()) if (!TEMPLATES[t]) fail(`${s.id}: template ${t} has no generator`);
  for (const alias of s.aliases) if (resolveSkill(alias)?.id !== s.id) fail(`alias ${alias} does not resolve`);
}
// every id a RemNote card or streak has ever used must still resolve
const LEGACY: Record<string, string> = {
  separable: "ode1.separable", substitution: "ode1.substitution", linear: "ode1.linear", ibp: "ode1.linear-ibp",
  bernoulli: "ode1.bernoulli", wronskian: "ode2.wronskian",
  "krey-ch01-separable": "ode1.separable", "krey-ch02-wronskian": "ode2.wronskian",
  "krey-ch02-spring-undamped": "ode2.spring-undamped", "krey-ch02-spring-damped": "ode2.spring-damped",
  "krey-ch05-points": "series.points", "krey-ch05-power-series": "series.recurrence", "krey-ch05-series-terms": "series.terms",
  "krey-ch05-radius": "series.radius", "krey-ch05-indicial": "series.indicial", "krey-ch05-frobenius-case": "series.frobenius-case",
  "krey-ch11-sl-eigenvalues": "bvp.sl-eigenvalues", "krey-ch11-sl-eigenfunctions": "bvp.sl-eigenfunctions",
  "krey-ch11-sl-form": "bvp.sl-form", "krey-ch11-sl-classify": "bvp.sl-classify",
};
for (const [old, now] of Object.entries(LEGACY)) if (resolveSkill(old)?.id !== now) fail(`legacy id ${old} should resolve to ${now}`);

// the book layer: every live skill is taught somewhere, and spot-checks of the mapping
for (const s of LIVE_SKILLS) if (!placesFor(s.id).length) fail(`${s.id} is live but no textbook section maps to it`);
const where = (id: string) => placesFor(id).map(placeText).join("; ");
const expectPlace = (id: string, text: string) => { if (!where(id).includes(text)) fail(`${id} should be in ${text} (got ${where(id)})`); };
expectPlace("ode1.separable", "Kreyszig 10e §1.3");
expectPlace("ode2.spring-damped", "Kreyszig 10e §2.4");
expectPlace("ht.fins", "Incropera 8e §3.6");
expectPlace("la.eigenvalues", "Lay 5e §5.2");
expectPlace("ht.finite-difference", "Incropera 8e Ch 4");
expectPlace("bvp.sl-eigenfunctions", "Kreyszig 10e §11.5");
expectPlace("ht.fins", "Incropera 8e §3.6");
expectPlace("ht.transient-one-term", "Incropera 8e §5.5–5.6");
expectPlace("stat.partition-function", "Dill & Bromberg 2e Ch 10");
expectPlace("stat.partition-function", "Shell Ch 16");
if (primaryPlace("stat.partition-function", "shell-2015")?.source.id !== "shell-2015") fail("preferred source not honoured");
if (SOURCES.length !== 5) fail(`expected 5 sources, got ${SOURCES.length}`);

// ── 1–3. every template, many seeds ────────────────────────────────────────
const dump: Problem[] = [];
const counts: Record<string, number> = {};
for (const s of LIVE_SKILLS) {
  for (const t of Object.values(s.levels).flat()) {
    for (let seed = 1; seed <= SEEDS; seed++) {
      const p = generateTemplate(s.id, t, seed * 7919 + t.length);
      dump.push(p);
      const key = `${s.id} / ${t}`;
      counts[key] = (counts[key] ?? 0) + 1;
      const r = check(p, reference(p));
      if (r.status !== "correct") fail(`${key} #${seed}: reference rejected (${r.status}: ${r.message}) ref=${JSON.stringify(reference(p))}`);
      for (const bad of negatives(p)) {
        const rb = check(p, bad);
        if (rb.status === "correct") fail(`${key} #${seed}: wrong answer accepted ${JSON.stringify(bad)}`);
      }
      for (const txt of [p.prompt, ...p.steps]) for (const c of texChunks(txt)) katexOk(key, c);
      katexOk(key, p.answerTex);
    }
  }
  // generate() through the graph works too
  for (let seed = 0; seed < 5; seed++) generate(s.id, seed);
}

// ── 4. student-style answers per kind ──────────────────────────────────────
function mk(answer: Answer, extra: Partial<Problem> = {}): Problem {
  return { skill: "t", template: "t", level: 1, prompt: "", answerTex: "", steps: [], answer, ...extra };
}
const cases: [string, Problem, (string | string[])[], (string | string[])[]][] = [
  // ── ode2 + coef (variable coefficients / higher order) and tuple + system ──
  [
    "Euler–Cauchy double root x²y'' - 3xy' + 4y = 0",
    mk({ kind: "ode2", a: 0, b: 0, c: 0, v: "x", coef: ["x^2", "-3*x", "4"], ref: "" }),
    ["y = (C1 + C2 ln x) x^2", "c1 x^2 + c2 x^2 ln|x|", "A x^2 + B x^2 log(x)"],
    ["y = C1 x^2 + C2 x^2", "C1 x^2 + C2 x ln x", "(C1 + C2 x)e^(2x)", "C1 x^2"],
  ],
  [
    "Euler–Cauchy IVP x²y'' - 2y = 0, y(1) = 1, y'(1) = 5",
    mk({ kind: "ode2", a: 0, b: 0, c: 0, v: "x", coef: ["x^2", "0", "-2"], ic: [1, 1, 5], ref: "" }),
    ["y = 2x^2 - 1/x", "2x² - x^(-1)"],
    ["2x^2 + 1/x", "C1 x^2 + C2/x", "2x^2 - 1/x + x"],
  ],
  [
    "reduction of order xy'' + 2y' + xy = 0",
    mk({ kind: "ode2", a: 0, b: 0, c: 0, v: "x", coef: ["x", "2", "x"], ref: "" }),
    ["y = (C1 cos x + C2 sin x)/x", "A cos(x)/x + B sin(x)/x"],
    ["C1 cos(x)/x + C2 cos(x)/x", "C1 cos x + C2 sin x"],
  ],
  [
    "third order y''' - y' = 0",
    mk({ kind: "ode2", a: 0, b: 0, c: 0, v: "x", coef: ["1", "0", "-1", "0"], ref: "" }),
    ["y = C1 + C2 e^x + C3 e^(-x)", "A + B cosh(x) + C sinh(x)"],
    ["C1 + C2 e^x", "C1 + C2 e^x + C3 e^x", "C1 + C2 x + C3 e^x"],
  ],
  [
    "triple root y''' - 3y'' + 3y' - y = 0",
    mk({ kind: "ode2", a: 0, b: 0, c: 0, v: "x", coef: ["1", "-3", "3", "-1"], ref: "" }),
    ["y = (C1 + C2 x + C3 x^2) e^x", "c1 e^x + c2 x e^x + c3 x^2 e^x"],
    ["(C1 + C2 x + C3 x^3)e^x", "(C1 + C2 x)e^x + C3 e^x"],
  ],
  [
    "third-order IVP y''' - y' = 0, y(0) = 2, y'(0) = 0, y''(0) = 2",
    mk({ kind: "ode2", a: 0, b: 0, c: 0, v: "x", coef: ["1", "0", "-1", "0"], ic: [0, 2, 0, 2], ref: "" }),
    ["y = e^x + e^(-x)", "2cosh(x)"],
    ["e^x + e^(-x) + 1", "2e^x", "C1 + e^x + e^(-x)"],
  ],
  [
    "variation of parameters y'' + y = csc x",
    mk({ kind: "ode2", a: 1, b: 0, c: 1, v: "x", rhs: "1/sin(x)", particular: true, ref: "" }),
    ["y_p = -x cos x + sin x ln(sin x)", "sin(x) ln|sin x| - x cos(x) + 3 sin x"],
    ["sin x ln(sin x)", "-x cos x", "-x cos x + sin x ln(sin x) + C1 cos x"],
  ],
  [
    "system y' = [[1,2],[2,1]] y, general",
    mk({ kind: "tuple", fields: [{ label: "y₁", tex: "y_1", ref: "", mode: "expr" }, { label: "y₂", tex: "y_2", ref: "", mode: "expr" }], system: { A: [[1, 2], [2, 1]], v: "t" } }),
    [["C1 e^(3t) + C2 e^(-t)", "C1 e^(3t) - C2 e^(-t)"], ["2A e^{3t} + B e^{-t}", "2A e^{3t} - B e^{-t}"], ["y1 = c1 e^(3t) + c2 e^(-t)", "y2 = c1 e^(3t) - c2 e^(-t)"]],
    [["C1 e^(3t)", "C1 e^(3t)"], ["C1 e^(3t) + C2 e^(-t)", "C1 e^(3t) + C2 e^(-t)"], ["C1 e^(3t) + C2 e^(3t)", "C1 e^(3t) + C2 e^(3t)"]],
  ],
  [
    "system IVP y(0) = (2, 0)",
    mk({ kind: "tuple", fields: [{ label: "y₁", tex: "y_1", ref: "", mode: "expr" }, { label: "y₂", tex: "y_2", ref: "", mode: "expr" }], system: { A: [[1, 2], [2, 1]], v: "t", ic: [0, 2, 0] } }),
    [["e^(3t) + e^(-t)", "e^(3t) - e^(-t)"], ["y1 = e^{3t} + e^{-t}", "y2 = e^{3t} - e^{-t}"]],
    [["e^(3t) - e^(-t)", "e^(3t) + e^(-t)"], ["2e^(3t)", "0"], ["C1 e^(3t) + e^(-t)", "e^(3t) - e^(-t)"]],
  ],
  [
    "first-order (from v0.2)",
    mk({ kind: "ode", rhs: "x^4*exp(x) + 3*y/x", ref: "" }),
    ["y = x^3(x-1)e^x + Cx^3", "y = x^4e^x - x^3e^x + Cx^3"],
    ["y = x^4e^x + Cx^3"],
  ],
  [
    "recurrence y'' + xy' + y = 0 (a_{n+2} = -a_n/(n+2))",
    mk({ kind: "recurrence", gap: 2, ref: "-1/(m+2)", from: 0 }),
    [
      "a_{n+2} = -a_n/(n+2)",
      "a_(n+2) = -a_n/(n+2)",
      "a_{k+2} = -a_k/(k+2)",
      "(n+2)a_{n+2} = -a_n",
      "a_n = -a_{n-2}/n",
      "a_{n+2} = -(n+1)a_n/((n+2)(n+1))",
      "(n+2)(n+1)a_{n+2} = -(n+1) a_n",
      "a_{n+2}(n+2) + a_n = 0",
      "(n+2)a_{n+2} + a_n = 0",
    ],
    ["a_{n+2} = a_n/(n+2)", "a_{n+2} = -a_n/(n+1)", "a_{n+1} = -a_n/(n+2)"],
  ],
  [
    "recurrence Airy y'' - xy = 0",
    mk({ kind: "recurrence", gap: 3, ref: "1/((m+3)*(m+2))", from: 0 }),
    ["a_{n+3} = a_n/((n+3)(n+2))", "a_{n+2} = a_{n-1}/((n+2)(n+1))", "(n+3)(n+2)a_{n+3} = a_n"],
    ["a_{n+2} = a_{n-1}/((n+3)(n+2))"],
  ],
  [
    "roots",
    mk({ kind: "roots", ref: [0.5, -1] }),
    ["1/2, -1", "r = -1, 0.5", "-1 and 1/2", "r1 = 1/2, r2 = -1"],
    ["1/2", "1/2, 1", "-1/2, 1"],
  ],
  [
    "double root",
    mk({ kind: "roots", ref: [0.5, 0.5] }),
    ["1/2", "1/2, 1/2"],
    ["1/2, 0"],
  ],
  [
    "eigenvalues DD on [0,2]",
    mk({ kind: "indexed", ref: "(n*pi/2)^2", start: 1, label: "λ_n" }),
    ["λ_n = (n pi/2)^2", "n^2 pi^2/4", "lambda_n = ((n+1)pi/2)^2"],
    ["(n pi)^2", "(n pi/2)"],
  ],
  [
    "eigenfunctions DN on [0,pi]",
    mk({ kind: "eigenfunctions", bcs: [{ at: 0, type: "y" }, { at: Math.PI, type: "yp" }], L: Math.PI, refLambda: "((2*n-1)*pi/(2*pi))^2", start: 1 }),
    ["y_n = sin((2n-1)x/2)", "sin((2n+1)x/2)", "3sin((2n-1)x/2)", "B sin((n - 1/2)x)"],
    ["sin(nx)", "cos((2n-1)x/2)", "sin((2n-1)x/2) + 1"],
  ],
  [
    "S–L form, Bessel-type",
    mk({ kind: "tuple", fields: [{ label: "p", tex: "p", ref: "x", mode: "expr" }, { label: "q", tex: "q", ref: "-4/x", mode: "expr" }, { label: "r", tex: "r", ref: "x", mode: "expr" }], vars: ["x"], proportional: true }),
    [["x", "-4/x", "x"], ["2x", "-8/x", "2x"], ["p = x", "q = -4/x", "r = x"]],
    [["x", "4/x", "x"], ["x", "-4/x", "1"]],
  ],
  [
    "amplitude–phase",
    mk({ kind: "tuple", fields: [{ label: "R", tex: "R", ref: "5", mode: "number" }, { label: "δ", tex: "d", ref: `${Math.atan2(4, -3)}`, mode: "angle" }], vars: [] }),
    [["5", "pi - atan(4/3)"], ["5", "2.2143"], ["sqrt(25)", "2.214297"]],
    [["5", "atan(4/3)"], ["5", "-atan(4/3)"], ["7", "pi - atan(4/3)"]],
  ],
  [
    "damped IVP",
    mk({ kind: "ode2", a: 1, b: 4, c: 13, v: "t", ic: [0, 2, -1], ref: "" }),
    ["y = e^(-2t)(2cos(3t) + sin(3t))", "y(t)=2e^(-2t)cos(3t)+e^(-2t)sin(3t)", "e^{-2t}(2\\cos 3t + \\sin 3t)"],
    ["y = e^(-2t)(2cos(3t) - sin(3t))", "y = e^(-2t)(C1 cos(3t) + C2 sin(3t))", "y = 2cos(3t) + sin(3t)"],
  ],
  [
    "general second order",
    mk({ kind: "ode2", a: 1, b: 0, c: 4, v: "t", ref: "" }),
    ["y = C1 cos(2t) + C2 sin(2t)", "y = A cos 2t + B sin 2t"],
    ["y = C1 cos(2t)", "y = C1 cos(4t) + C2 sin(4t)"],
  ],
  [
    "repeated root general",
    mk({ kind: "ode2", a: 1, b: -4, c: 4, v: "x", ref: "" }),
    ["y = (C1 + C2 x)e^(2x)", "y = c1 e^{2x} + c2 x e^{2x}", "A e^(2x) + B x e^(2x)"],
    ["y = C1 e^(2x) + C2 e^(2x)", "y = (C1 + C2)e^(2x)", "y = C1 e^(2x) + C2 e^(-2x)", "y = C1 x e^(2x)"],
  ],
  [
    "complex general in x",
    mk({ kind: "ode2", a: 1, b: 2, c: 5, v: "x", ref: "" }),
    ["y = e^(-x)(C1 cos(2x) + C2 sin(2x))", "y = e^{-x}(A\\cos 2x + B\\sin 2x)"],
    ["y = e^(-x)(C1 cos(2x) + C2 cos(2x))", "y = e^(x)(C1 cos(2x) + C2 sin(2x))", "y = C1 e^(-x) + C2 e^(2x)"],
  ],
  [
    "particular, polynomial forcing",
    mk({ kind: "ode2", a: 1, b: 3, c: 2, v: "x", rhs: "4*x^2", particular: true, ref: "" }),
    ["y_p = 2x^2 - 6x + 7", "2x^2-6x+7", "y = 2x^2 - 6x + 7 + e^(-x)"],
    ["y_p = 2x^2", "y = 2x^2 - 6x + 7 + C1 e^(-x)", "2x^2 - 6x"],
  ],
  [
    "particular, resonance",
    mk({ kind: "ode2", a: 1, b: 0, c: 9, v: "x", rhs: "12*cos(3*x)", particular: true, ref: "" }),
    ["y_p = 2x sin(3x)", "2x\\sin 3x"],
    ["y_p = 2 sin(3x)", "y_p = 2x cos(3x)", "y_p = (2/3) cos(3x)"],
  ],
  [
    "general with forcing",
    mk({ kind: "ode2", a: 1, b: -1, c: -2, v: "x", rhs: "6*exp(x)", ref: "" }),
    ["y = C1 e^(-x) + C2 e^(2x) - 3e^x"],
    ["y = C1 e^(-x) + C2 e^(2x)", "y = -3e^x", "y = C1 e^(-x) + C2 e^(2x) + 3e^x"],
  ],
  [
    "radius as a number",
    mk({ kind: "expression", ref: "sqrt(5)", vars: [], label: "R" }),
    ["sqrt(5)", "R = √5", "2.2360679775"],
    ["2", "5"],
  ],
];
for (const [name, p, good, bad] of [...cases, ...LAPLACE_FOURIER_CASES]) {
  for (const g of good) {
    const r = check(p, g);
    if (r.status !== "correct") fail(`${name}: should accept ${JSON.stringify(g)} (${r.status}: ${r.message})`);
  }
  for (const b of bad) {
    const r = check(p, b);
    if (r.status === "correct") fail(`${name}: should reject ${JSON.stringify(b)}`);
  }
}

// method notes render
let methodLines = 0;
for (const sk of ALL_SKILLS)
  for (const line of sk.method ?? []) {
    methodLines++;
    for (const c of texChunks(line)) katexOk(`method ${sk.id}`, c);
  }
console.log(`method notes: ${methodLines} lines rendered`);

fs.mkdirSync("tests/out", { recursive: true });
fs.writeFileSync("tests/out/problems.json", JSON.stringify(dump));
console.log(Object.entries(counts).map(([k, v]) => `${k}: ${v}`).join("\n"));
console.log(`\n${LIVE_SKILLS.length} live skills of ${ALL_SKILLS.length}; ${dump.length} problems generated; failures: ${failures}`);
process.exit(failures ? 1 : 0);
