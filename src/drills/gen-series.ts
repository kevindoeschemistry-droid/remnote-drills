// Kreyszig Ch 5 · series solutions, Level 1.
// Built backward: pick the recurrence / indicial roots / singular points first,
// then write the ODE that produces them.
import { Rng } from "./rng";
import type { Draft } from "./types";
import { ct, join, m, signed } from "./tex";
import { Q, qterm } from "./rational";
import { require_ } from "./reject";

const POINT_OPTIONS = ["Ordinary point", "Regular singular point", "Irregular singular point"];
const CASE_OPTIONS = [
  "Distinct roots, not differing by an integer",
  "Double root",
  "Roots differing by a positive integer",
];

/** (x - s) as LaTeX; just "x" when s = 0 */
const lin = (s: number) => (s === 0 ? "x" : `(x${signed(-s)})`);
/** (x - s)^k as LaTeX ("" when k = 0) */
function linPow(s: number, k: number): string {
  if (k === 0) return "";
  if (k === 1) return lin(s);
  return s === 0 ? `x^{${k}}` : `(x${signed(-s)})^{${k}}`;
}
const linPowJs = (s: number, k: number) => (k === 0 ? "1" : `(x - (${s}))^${k}`);

// ── classify a point ───────────────────────────────────────────────────────
function classifyPoint(r: Rng): Draft {
  const x0 = r.int(-2, 2);
  const type = r.int(0, 2); // 0 ordinary, 1 regular, 2 irregular
  const alpha = r.nz(-4, 4);
  const beta = r.nz(-5, 5);
  let P: string, Pjs: string, Qt: string, Qjs: string, Rt: string, Rjs: string;
  const steps: string[] = [];
  const at = m(`x = ${x0}`);
  if (type === 0) {
    const u = r.nz(-3, 3, [x0]);
    const w = r.nz(-3, 3, [x0]);
    P = u === w ? linPow(u, 2) : `${lin(u)}${lin(w)}`;
    Pjs = `(x - (${u}))*(x - (${w}))`;
    Qt = ct(alpha, "x");
    Qjs = `(${alpha})*x`;
    Rt = `${beta}`;
    Rjs = `(${beta})`;
    const Pv = (x0 - u) * (x0 - w);
    steps.push(`Write it as ${m("P(x)y'' + Q(x)y' + R(x)y = 0")} with ${m(`P(x) = ${P}`)}.`);
    steps.push(`${m(`P(${x0}) = ${Pv} \\neq 0`)}, so ${m("Q/P")} and ${m("R/P")} are analytic at ${at}: an ordinary point.`);
  } else {
    // P = (x - x0)^k * g, g = 1 or (x - u)
    const k = type === 1 ? r.pick([1, 2]) : r.pick([2, 3]);
    const useG = r.chance(0.5);
    const u = r.nz(-3, 3, [x0]);
    const g = useG ? lin(u) : "";
    const gJs = useG ? `(x - (${u}))` : "1";
    P = `${linPow(x0, k)}${g}`;
    Pjs = `${linPowJs(x0, k)}*${gJs}`;
    // regular: Q ~ (x-x0)^{k-1}, R ~ (x-x0)^{k-2}; irregular: Q one power too low
    const qPow = type === 1 ? k - 1 : k - 2;
    const rPow = Math.max(0, k - 2);
    Qt = ct(alpha, linPow(x0, qPow));
    Qjs = `(${alpha})*${linPowJs(x0, qPow)}`;
    Rt = ct(beta, linPow(x0, rPow));
    Rjs = `(${beta})*${linPowJs(x0, rPow)}`;
    const gOver = (num: string) => (useG ? `\\frac{${num}}{${g}}` : num);
    steps.push(`${m(`P(x) = ${P}`)} vanishes at ${at}, so it is a singular point. Test ${m(`(x${signed(-x0)})\\frac{Q}{P}`)} and ${m(`(x${signed(-x0)})^2\\frac{R}{P}`)}:`);
    const qLeft = 1 + qPow - k; // power of (x - x0) left after cancelling
    const rLeft = 2 + rPow - k;
    const show = (coef: number, left: number) =>
      left >= 0 ? gOver(ct(coef, linPow(x0, left))) : `\\frac{${coef}}{${linPow(x0, -left)}${g}}`;
    steps.push(
      `${m(`(x${signed(-x0)})\\frac{Q}{P} = ${show(alpha, qLeft)}`)} and ${m(`(x${signed(-x0)})^2\\frac{R}{P} = ${show(beta, rLeft)}`)}`
    );
    steps.push(
      type === 1
        ? `Both are analytic at ${at}: a regular singular point.`
        : `${m(`(x${signed(-x0)})\\frac{Q}{P}`)} still blows up at ${at}: an irregular singular point.`
    );
  }
  const eq = `${join([`${P}y''`, Qt === "0" ? "" : `${Qt}y'`, `${Rt}y`])} = 0`;
  return {
    prompt: `Classify ${m(`x = ${x0}`)} for ${m(eq)}.`,
    answer: { kind: "choice", options: POINT_OPTIONS, correct: POINT_OPTIONS[type] },
    answerTex: `\\text{${POINT_OPTIONS[type]}}`,
    steps,
    meta: { variant: "classify-point", x0, P: Pjs, Q: Qjs, R: Rjs, type },
  };
}

// ── (1 + a x^2) y'' + b x y' + d y = 0 ─────────────────────────────────────
interface Gen2 {
  a: number;
  b: number;
  d: number;
  eq: string;
  poly: (n: number) => number;
  polyTex: string; // a n^2 + (b - a) n + d
  recTex: string; // a_{n+2} = ...
  refJs: string; // f(m)
}

function pickGen2(r: Rng): Gen2 {
  const a = r.pick([0, 0, 1, -1]);
  const b = r.int(-2, 2);
  const d = r.int(-4, 4);
  require_(b !== 0 || d !== 0);
  const lead = a === 0 ? "y''" : a === 1 ? "(1 + x^{2})y''" : "(1 - x^{2})y''";
  const eq = `${join([lead, ct(b, "xy'"), d ? ct(d, "y") : ""])} = 0`;
  const poly = (n: number) => a * n * n + (b - a) * n + d;
  const polyTex = join([ct(a, "n^{2}"), ct(b - a, "n"), d ? `${d}` : ""]);
  // present the recurrence with a positive-looking numerator when we can
  const leadNeg = (a !== 0 ? a : b - a !== 0 ? b - a : d) < 0;
  const negTex = join([ct(-a, "n^{2}"), ct(a - b, "n"), d ? `${-d}` : ""]);
  const recTex = leadNeg
    ? `a_{n+2} = \\frac{${negTex}}{(n+2)(n+1)}\\,a_n`
    : `a_{n+2} = -\\frac{${polyTex}}{(n+2)(n+1)}\\,a_n`;
  const refJs = `-((${a})*m^2 + (${b - a})*m + (${d}))/((m+2)*(m+1))`;
  return { a, b, d, eq, poly, polyTex, recTex, refJs };
}

function gen2Steps(g: Gen2): string[] {
  const parts: string[] = ["(n+2)(n+1)a_{n+2}"];
  if (g.a) parts.push(`${g.a === 1 ? "" : "-"}n(n-1)a_n`);
  if (g.b) parts.push(ct(g.b, "na_n"));
  if (g.d) parts.push(ct(g.d, "a_n"));
  return [
    `Substitute ${m("y = \\sum a_n x^n")}: ${m("y' = \\sum n a_n x^{n-1}")}, ${m("y'' = \\sum n(n-1) a_n x^{n-2}")}.`,
    `Shift the ${m("y''")} sum so every term has ${m("x^n")}: ${m("\\sum (n+2)(n+1)a_{n+2}x^n")}` +
      (g.a ? `; the ${m(`${g.a === 1 ? "" : "-"}x^2y''`)} part is already ${m("\\sum n(n-1)a_n x^n")}.` : "."),
    `Coefficient of ${m("x^n")}: ${m(`${join(parts)} = 0`)}, i.e. ${m(`(n+2)(n+1)a_{n+2} + (${g.polyTex})a_n = 0`)}.`,
    m(g.recTex),
  ];
}

function recurrence(r: Rng): Draft {
  const g = pickGen2(r);
  return {
    prompt: `Substitute ${m("y = \\sum_{n\\ge 0} a_n x^n")} into ${m(g.eq)} and find the recurrence relation.`,
    answer: { kind: "recurrence", gap: 2, ref: g.refJs, from: 0 },
    answerTex: g.recTex,
    steps: gen2Steps(g),
    meta: { variant: "general", ode: { P: `1 + (${g.a})*x^2`, Q: `(${g.b})*x`, R: `(${g.d})` } },
  };
}

function recurrenceAiry(r: Rng): Draft {
  const c = r.nz(-3, 3);
  const eq = `${join(["y''", ct(c, "xy")])} = 0`;
  const neg = -c;
  const num = Math.abs(neg) === 1 ? "a_n" : `${Math.abs(neg)}a_n`;
  const recTex = `a_{n+3} = ${neg < 0 ? "-" : ""}\\frac{${num}}{(n+3)(n+2)}`;
  return {
    prompt: `Substitute ${m("y = \\sum_{n\\ge 0} a_n x^n")} into ${m(eq)} and find the recurrence relation.`,
    answer: { kind: "recurrence", gap: 3, ref: `(${neg})/((m+3)*(m+2))`, from: 0 },
    answerTex: recTex,
    steps: [
      `${m("y'' = \\sum (n+2)(n+1)a_{n+2}x^n")} and ${m(`${ct(c, "xy")} = ${ct(c, "\\sum a_{n-1}x^n")}`)} (starts at ${m("n = 1")}).`,
      `${m("x^0")}: ${m("2a_2 = 0")}, so ${m("a_2 = 0")}.`,
      `${m("x^n,\\ n\\ge1")}: ${m(`${join(["(n+2)(n+1)a_{n+2}", ct(c, "a_{n-1}")])} = 0`)}.`,
      `Shift ${m("n \\to n+1")}: ${m(recTex)} (every third coefficient is linked).`,
    ],
    meta: { variant: "airy", ode: { P: "1", Q: "0", R: `(${c})*x` } },
  };
}

// ── first terms ────────────────────────────────────────────────────────────
function polyTex(cs: Q[]): string {
  return join(cs.map((c, k) => qterm(c, k === 0 ? "" : k === 1 ? "x" : `x^{${k}}`)));
}
const polyJs = (cs: Q[]) => cs.map((c, k) => `${c.js()}*x^${k}`).join(" + ");

function initial(r: Rng): [number, number] {
  const A = r.int(-2, 3);
  const B = r.int(-2, 3);
  require_(A !== 0 || B !== 0);
  return [A, B];
}

function seriesTerms(r: Rng): Draft {
  const g = pickGen2(r);
  const [A, B] = initial(r);
  const a: Q[] = [new Q(A), new Q(B)];
  for (let n = 0; n <= 3; n++) a.push(a[n].mul(new Q(-g.poly(n), (n + 2) * (n + 1))));
  require_(a.slice(2).filter((c) => !c.isZero()).length >= 2);
  const ans = polyTex(a);
  return {
    prompt: `Find the power-series solution of ${m(g.eq)} with ${m(`y(0) = ${A},\\ y'(0) = ${B}`)}, through the ${m("x^5")} term.`,
    answer: { kind: "expression", ref: polyJs(a), vars: ["x"], label: "y" },
    answerTex: `y = ${ans} + \\cdots`,
    steps: [
      `Recurrence: ${m(g.recTex)}.`,
      `${m(`a_0 = y(0) = ${A}`)}, ${m(`a_1 = y'(0) = ${B}`)}.`,
      ...[2, 3, 4, 5].map((k) => `${m(`a_{${k}} = ${a[k].tex()}`)}`),
      m(`y = ${ans} + \\cdots`),
    ],
    meta: { variant: "general", coeffs: a.map((c) => [c.n, c.d]), ode: { P: `1 + (${g.a})*x^2`, Q: `(${g.b})*x`, R: `(${g.d})` }, A, B },
  };
}

function seriesTermsAiry(r: Rng): Draft {
  const c = r.nz(-3, 3);
  const [A, B] = initial(r);
  const a: Q[] = [new Q(A), new Q(B), new Q(0)];
  for (let n = 0; n <= 2; n++) a.push(a[n].mul(new Q(-c, (n + 3) * (n + 2))));
  require_(a.slice(2).filter((q) => !q.isZero()).length >= 1);
  const eq = `${join(["y''", ct(c, "xy")])} = 0`;
  const ans = polyTex(a);
  return {
    prompt: `Find the power-series solution of ${m(eq)} with ${m(`y(0) = ${A},\\ y'(0) = ${B}`)}, through the ${m("x^5")} term.`,
    answer: { kind: "expression", ref: polyJs(a), vars: ["x"], label: "y" },
    answerTex: `y = ${ans} + \\cdots`,
    steps: [
      `Recurrence: ${m("a_2 = 0")} and ${m(`a_{n+3} = \\frac{${-c}\\,a_n}{(n+3)(n+2)}`)}.`,
      `${m(`a_0 = ${A}`)}, ${m(`a_1 = ${B}`)}, ${m("a_2 = 0")}.`,
      ...[3, 4, 5].map((k) => `${m(`a_{${k}} = ${a[k].tex()}`)}`),
      m(`y = ${ans} + \\cdots`),
    ],
    meta: { variant: "airy", coeffs: a.map((q) => [q.n, q.d]), ode: { P: "1", Q: "0", R: `(${c})*x` }, A, B },
  };
}

// ── radius of convergence ──────────────────────────────────────────────────
function radius(r: Rng): Draft {
  const complex = r.chance(0.5);
  const x0 = r.int(-2, 3);
  let Ptex: string, Pjs: string, rootsTex: string, R2: number, dists: string;
  if (complex) {
    const al = r.int(-2, 2);
    const be = r.int(1, 3);
    Ptex = join(["x^{2}", ct(-2 * al, "x"), `${al * al + be * be}`]);
    Pjs = `x^2 - (${2 * al})*x + (${al * al + be * be})`;
    rootsTex = `x = ${al === 0 ? "" : al} \\pm ${be === 1 ? "" : be}i`;
    R2 = (x0 - al) ** 2 + be * be;
    dists = `\\sqrt{(${x0}${signed(-al)})^2 + ${be}^2} = ${rootTex(R2)}`;
  } else {
    const u = r.nz(-3, 3, [x0]);
    const w = r.nz(-3, 4, [x0, u]);
    Ptex = join(["x^{2}", ct(-(u + w), "x"), u * w ? `${u * w}` : ""]);
    Pjs = `(x - (${u}))*(x - (${w}))`;
    rootsTex = `x = ${u},\\ ${w}`;
    R2 = Math.min(Math.abs(x0 - u), Math.abs(x0 - w)) ** 2;
    dists = `|${x0} - (${u})| = ${Math.abs(x0 - u)},\\ |${x0} - (${w})| = ${Math.abs(x0 - w)}`;
  }
  const q = r.nz(-3, 3);
  const c = r.nz(-4, 4);
  const eqClean = `${join([`(${Ptex})y''`, ct(q, "xy'"), ct(c, "y")])} = 0`;
  return {
    prompt: `Without solving, find the minimum radius of convergence of a power-series solution of ${m(eqClean)} about ${m(`x_0 = ${x0}`)}.`,
    answer: { kind: "expression", ref: `sqrt(${R2})`, vars: [], label: "R" },
    answerTex: `R = ${rootTex(R2)}`,
    steps: [
      `Singular points are where the ${m("y''")} coefficient vanishes: ${m(`${Ptex} = 0 \\Rightarrow ${rootsTex}`)}.`,
      `Distances from ${m(`x_0 = ${x0}`)}: ${m(dists)}.`,
      `The series converges at least out to the nearest one: ${m(`R = ${rootTex(R2)}`)}.`,
    ],
    meta: { variant: complex ? "complex" : "real", P: Pjs, x0, R2 },
  };
}

function rootTex(n: number): string {
  const s = Math.round(Math.sqrt(n));
  return s * s === n ? `${s}` : `\\sqrt{${n}}`;
}

// ── Frobenius: indicial roots / case ───────────────────────────────────────
const CASES: [Q, Q][][] = [
  // non-integer difference
  [[new Q(1, 2), new Q(0)], [new Q(1, 2), new Q(-1)], [new Q(1, 3), new Q(0)], [new Q(3, 2), new Q(0)], [new Q(1, 2), new Q(1)], [new Q(2, 3), new Q(0)], [new Q(-1, 2), new Q(1)]],
  // double root
  [[new Q(1, 2), new Q(1, 2)], [new Q(0), new Q(0)], [new Q(1), new Q(1)], [new Q(-1), new Q(-1)], [new Q(2), new Q(2)], [new Q(1, 3), new Q(1, 3)]],
  // integer difference
  [[new Q(1), new Q(0)], [new Q(2), new Q(0)], [new Q(1), new Q(-1)], [new Q(1, 2), new Q(-1, 2)], [new Q(3, 2), new Q(-1, 2)], [new Q(2), new Q(-1)], [new Q(0), new Q(-2)]],
];

function lcm(a: number, b: number) {
  let x = a, y = b;
  while (y) [x, y] = [y, x % y];
  return (a * b) / x;
}

function frobeniusEq(r: Rng, kase: number) {
  const [r1, r2] = r.pick(CASES[kase]);
  const p0 = new Q(1).sub(r1.add(r2));
  const q0 = r1.mul(r2);
  const D = lcm(p0.d, q0.d);
  const A = D, B = p0.n * (D / p0.d), C = q0.n * (D / q0.d);
  const E = r.nz(-2, 2);
  const yTerm = C ? `(${join([`${C}`, ct(E, "x")])})y` : ct(E, "xy");
  const eq = `${join([ct(A, "x^{2}y''"), ct(B, "xy'"), yTerm])} = 0`;
  const steps = [
    `Divide by ${m(ct(A, "x^{2}"))}: ${m(`p_0 = \\lim_{x\\to0} x\\cdot\\frac{${ct(B, "x")}}{${ct(A, "x^{2}")}} = ${p0.tex()}`)}, ${m(`q_0 = \\lim_{x\\to0} x^2\\cdot\\frac{${join([C ? `${C}` : "0", ct(E, "x")])}}{${ct(A, "x^{2}")}} = ${q0.tex()}`)}.`,
    `Indicial equation ${m("r(r-1) + p_0 r + q_0 = 0")}: ${m(`${indicialTex(p0.sub(1), q0)} = 0`)}.`,
    `Roots: ${m(`r_1 = ${r1.tex()},\\ r_2 = ${r2.tex()}`)}.`,
  ];
  return { r1, r2, eq, steps, A, B, C, E };
}

function signedQ(q: Q): string {
  if (q.isZero()) return "+ 0";
  return q.n < 0 ? `- ${q.neg().tex()}` : `+ ${q.tex()}`;
}

function indicial(r: Rng): Draft {
  const f = frobeniusEq(r, r.int(0, 2));
  return {
    prompt: `${m("x = 0")} is a regular singular point of ${m(f.eq)}. Find the roots of the indicial equation.`,
    answer: { kind: "roots", ref: [f.r1.value(), f.r2.value()], label: "r" },
    answerTex: `r = ${f.r1.tex()},\\ ${f.r2.tex()}`,
    steps: f.steps,
    meta: { variant: "indicial", A: f.A, B: f.B, C: f.C, E: f.E },
  };
}

function frobeniusCase(r: Rng): Draft {
  const kase = r.int(0, 2);
  const f = frobeniusEq(r, kase);
  const diff = f.r1.sub(f.r2);
  const why = [
    `${m(`r_1 - r_2 = ${diff.tex()}`)} is not an integer: two Frobenius series ${m("x^{r_1}\\sum a_n x^n")} and ${m("x^{r_2}\\sum b_n x^n")}.`,
    `Double root: ${m("y_2 = y_1 \\ln x + x^{r}\\sum b_n x^n")} (a log term always appears).`,
    `${m(`r_1 - r_2 = ${diff.tex()}`)} is a positive integer: ${m("y_2 = k\\,y_1\\ln x + x^{r_2}\\sum b_n x^n")} (the log term may vanish).`,
  ][kase];
  return {
    prompt: `For ${m(f.eq)} about the regular singular point ${m("x = 0")}, which Frobenius case applies?`,
    answer: { kind: "choice", options: CASE_OPTIONS, correct: CASE_OPTIONS[kase] },
    answerTex: `\\text{${CASE_OPTIONS[kase]}}`,
    steps: [...f.steps, why],
    meta: { variant: "case", A: f.A, B: f.B, C: f.C, E: f.E, kase },
  };
}

export const SERIES_TEMPLATES: Record<string, (r: Rng) => Draft> = {
  "series-classify-point": classifyPoint,
  "series-recurrence": recurrence,
  "series-recurrence-airy": recurrenceAiry,
  "series-terms": seriesTerms,
  "series-terms-airy": seriesTermsAiry,
  "series-radius": radius,
  "frobenius-indicial": indicial,
  "frobenius-case": frobeniusCase,
};

/** r^2 + b r + c with rational b, c — drops zero terms and unit coefficients */
function indicialTex(b: Q, c: Q): string {
  const lin = b.isZero() ? "" : b.n === b.d ? " + r" : b.n === -b.d ? " - r" : ` ${signedQ(b)}r`;
  return `r^2${lin}${c.isZero() ? "" : ` ${signedQ(c)}`}`;
}
