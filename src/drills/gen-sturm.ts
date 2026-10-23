// Kreyszig §11.5 · Sturm–Liouville problems, Level 1.
import { Rng } from "./rng";
import type { Bc, Draft } from "./types";
import { ct, join, m } from "./tex";

type BcType = "DD" | "NN" | "DN" | "ND";

interface Eigen {
  bc: BcType;
  L: number; // numeric
  Ltex: string;
  Ljs: string;
  bcs: Bc[];
  bcTex: string;
  start: number;
  kTex: string; // μ_n
  kJs: string;
  lamTex: string;
  lamJs: string;
  yTex: string;
  yJs: string;
}

function eigen(r: Rng): Eigen {
  const bc = r.pick(["DD", "DD", "NN", "DN", "ND"] as BcType[]);
  const Lc = r.pick([1, 2, 3, "pi"] as const);
  const isPi = Lc === "pi";
  const L = isPi ? Math.PI : Lc;
  const Ltex = isPi ? "\\pi" : `${Lc}`;
  const Ljs = isPi ? "pi" : `${Lc}`;
  const whole = bc === "DD" || bc === "NN";
  let kTex: string;
  if (isPi) kTex = whole ? "n" : "\\frac{2n-1}{2}";
  else {
    const inner = whole ? "n\\pi" : "(2n-1)\\pi";
    const den = whole ? (Lc as number) : 2 * (Lc as number);
    kTex = den === 1 ? inner : `\\frac{${inner}}{${den}}`;
  }
  const kJs = whole ? `(n*pi/${Ljs})` : `((2*n-1)*pi/(2*${Ljs}))`;
  const lamTex = isPi && whole ? "n^{2}" : `\\left(${kTex}\\right)^{2}`;
  const trig = bc === "DD" || bc === "DN" ? "\\sin" : "\\cos";
  const yTex = kTex === "n" ? `${trig} nx` : `${trig}\\left(${kTex} x\\right)`;
  const yJs = `${trig === "\\sin" ? "sin" : "cos"}(${kJs}*x)`;
  const leftY = bc === "DD" || bc === "DN";
  const rightY = bc === "DD" || bc === "ND";
  const bcs: Bc[] = [
    { at: 0, type: leftY ? "y" : "yp" },
    { at: L, type: rightY ? "y" : "yp" },
  ];
  const bcTex = `${leftY ? "y(0)" : "y'(0)"} = 0,\\ ${rightY ? `y(${Ltex})` : `y'(${Ltex})`} = 0`;
  return {
    bc, L, Ltex, Ljs, bcs, bcTex,
    start: bc === "NN" ? 0 : 1,
    kTex, kJs, lamTex, lamJs: `${kJs}^2`, yTex, yJs,
  };
}

function eigenSteps(e: Eigen): string[] {
  const L = e.Ltex;
  const muL = L === "\\pi" ? "\\pi\\mu" : `${L}\\mu`;
  const lam0 =
    e.bc === "NN"
      ? `${m("\\lambda = 0")}: ${m("y = A + Bx")}, ${m("y' = B = 0")}, so ${m("y_0 = 1")} with ${m("\\lambda_0 = 0")} is an eigenpair.`
      : `${m("\\lambda = 0")}: ${m("y = A + Bx")}; the conditions force ${m("A = B = 0")}.`;
  const first =
    e.bc === "DD" || e.bc === "DN" ? `${m("y(0) = 0 \\Rightarrow A = 0")}` : `${m("y'(0) = 0 \\Rightarrow B = 0")}`;
  const second = {
    DD: `${m(`y(${L}) = B\\sin(${muL}) = 0 \\Rightarrow ${muL} = n\\pi`)}`,
    NN: `${m(`y'(${L}) = -A\\mu\\sin(${muL}) = 0 \\Rightarrow ${muL} = n\\pi`)}`,
    DN: `${m(`y'(${L}) = B\\mu\\cos(${muL}) = 0 \\Rightarrow ${muL} = \\frac{(2n-1)\\pi}{2}`)}`,
    ND: `${m(`y(${L}) = A\\cos(${muL}) = 0 \\Rightarrow ${muL} = \\frac{(2n-1)\\pi}{2}`)}`,
  }[e.bc];
  return [
    `${m("\\lambda = -\\mu^2 < 0")}: ${m("y = A\\cosh\\mu x + B\\sinh\\mu x")}; the conditions force ${m("A = B = 0")} (no eigenvalues).`,
    lam0,
    `${m("\\lambda = \\mu^2 > 0")}: ${m("y = A\\cos\\mu x + B\\sin\\mu x")}. ${first}.`,
    `${second}, so ${m(`\\mu_n = ${e.kTex}`)}.`,
  ];
}

function eigenvalues(r: Rng): Draft {
  const e = eigen(r);
  const nTex = `n = ${e.start}, ${e.start + 1}, ${e.start + 2}, \\dots`;
  return {
    prompt: `Find the eigenvalues ${m("\\lambda_n")} of ${m(`y'' + \\lambda y = 0,\\ ${e.bcTex}`)}.`,
    answer: { kind: "indexed", ref: e.lamJs, start: e.start, label: "λ_n" },
    answerTex: `\\lambda_n = ${e.lamTex},\\quad ${nTex}`,
    steps: [...eigenSteps(e), m(`\\lambda_n = \\mu_n^2 = ${e.lamTex},\\quad ${nTex}`)],
    meta: { variant: e.bc, L: e.Ljs, y: e.yJs, lam: e.lamJs, start: e.start },
  };
}

function eigenfunctions(r: Rng): Draft {
  const e = eigen(r);
  const nTex = `n = ${e.start}, ${e.start + 1}, \\dots`;
  return {
    prompt: `Find the eigenfunctions ${m("y_n(x)")} of ${m(`y'' + \\lambda y = 0,\\ ${e.bcTex}`)}.`,
    answer: { kind: "eigenfunctions", bcs: e.bcs, L: e.L, refLambda: e.lamJs, start: e.start },
    answerTex: `y_n = ${e.yTex},\\quad ${nTex}` + (e.bc === "NN" ? "\\ (y_0 = 1)" : ""),
    steps: [...eigenSteps(e), m(`y_n = ${e.yTex}`) + " (any nonzero multiple works)."],
    meta: { variant: e.bc, L: e.Ljs, y: e.yJs, lam: e.lamJs, start: e.start },
  };
}

// ── self-adjoint form ──────────────────────────────────────────────────────
interface Form {
  eq: string;
  aTex: string;
  bTex: string;
  ratioTex: string; // b/a
  intTex: string; // ∫ b/a dx
  p: [string, string];
  q: [string, string];
  r: [string, string];
  a: string; b: string; c: string; d: string; // mathjs, for tests
}

function form(rg: Rng): Form {
  const which = rg.int(0, 6);
  if (which === 0) {
    const k = rg.nz(-3, 3);
    const c = rg.pick([0, 0, 1, -2, 3]);
    const ek = `e^{${ct(k, "x")}}`;
    const ekJs = `exp((${k})*x)`;
    return {
      eq: `${join(["y''", ct(k, "y'")])} + ${c ? `(${c} + \\lambda)` : "\\lambda "}y = 0`,
      aTex: "1", bTex: `${k}`, ratioTex: `${k}`, intTex: ct(k, "x"),
      p: [ek, ekJs], q: [c ? ct(c, ek) : "0", c ? `(${c})*${ekJs}` : "0"], r: [ek, ekJs],
      a: "1", b: `${k}`, c: `${c}`, d: "1",
    };
  }
  if (which === 1) {
    const k = rg.pick([0, 1, 2, 3]);
    const c = rg.pick([0, 0, -1, 4]);
    // c * x^p, with \frac for negative powers
    const xc = (cc: number, pw: number) => {
      if (pw >= 0) return ct(cc, pw === 0 ? "" : pw === 1 ? "x" : `x^{${pw}}`);
      const den = pw === -1 ? "x" : `x^{${-pw}}`;
      return `${cc < 0 ? "-" : ""}\\frac{${Math.abs(cc)}}{${den}}`;
    };
    return {
      eq: `${join(["x^{2}y''", ct(k, "xy'")])} + ${c ? `(${c} + \\lambda)` : "\\lambda "}y = 0,\\ x > 0`,
      aTex: "x^{2}", bTex: ct(k, "x"), ratioTex: k ? `\\frac{${k}}{x}` : "0", intTex: k ? ct(k, "\\ln x") : "0",
      p: [xc(1, k), `x^(${k})`],
      q: [c ? xc(c, k - 2) : "0", c ? `(${c})*x^(${k - 2})` : "0"],
      r: [xc(1, k - 2), `x^(${k - 2})`],
      a: "x^2", b: `(${k})*x`, c: `${c}`, d: "1",
    };
  }
  if (which === 2) {
    const k = rg.pick([2, -2, 4, -4]);
    const half = k / 2;
    const e = `e^{${ct(half, "x^{2}")}}`;
    const eJs = `exp((${half})*x^2)`;
    return {
      eq: `${join(["y''", ct(k, "xy'")])} + \\lambda y = 0`,
      aTex: "1", bTex: ct(k, "x"), ratioTex: ct(k, "x"), intTex: ct(half, "x^{2}"),
      p: [e, eJs], q: ["0", "0"], r: [e, eJs],
      a: "1", b: `(${k})*x`, c: "0", d: "1",
    };
  }
  if (which === 3)
    return {
      eq: "xy'' + (1 - x)y' + \\lambda y = 0,\\ x > 0",
      aTex: "x", bTex: "1 - x", ratioTex: "\\frac{1}{x} - 1", intTex: "\\ln x - x",
      p: ["xe^{-x}", "x*exp(-x)"], q: ["0", "0"], r: ["e^{-x}", "exp(-x)"],
      a: "x", b: "1 - x", c: "0", d: "1",
    };
  if (which === 4)
    return {
      eq: "(1 - x^{2})y'' - xy' + \\lambda y = 0,\\ |x| < 1",
      aTex: "1 - x^{2}", bTex: "-x", ratioTex: "\\frac{-x}{1 - x^{2}}", intTex: "\\tfrac12\\ln(1 - x^{2})",
      p: ["\\sqrt{1 - x^{2}}", "sqrt(1 - x^2)"], q: ["0", "0"], r: ["\\frac{1}{\\sqrt{1 - x^{2}}}", "1/sqrt(1 - x^2)"],
      a: "1 - x^2", b: "-x", c: "0", d: "1",
    };
  if (which === 5)
    return {
      eq: "(1 - x^{2})y'' - 2xy' + \\lambda y = 0,\\ |x| < 1",
      aTex: "1 - x^{2}", bTex: "-2x", ratioTex: "\\frac{-2x}{1 - x^{2}}", intTex: "\\ln(1 - x^{2})",
      p: ["1 - x^{2}", "1 - x^2"], q: ["0", "0"], r: ["1", "1"],
      a: "1 - x^2", b: "-2*x", c: "0", d: "1",
    };
  const nu = rg.int(1, 3);
  return {
    eq: `x^{2}y'' + xy' + (\\lambda x^{2} - ${nu * nu})y = 0,\\ x > 0`,
    aTex: "x^{2}", bTex: "x", ratioTex: "\\frac{1}{x}", intTex: "\\ln x",
    p: ["x", "x"], q: [`-\\frac{${nu * nu}}{x}`, `-(${nu * nu})/x`], r: ["x", "x"],
    a: "x^2", b: "x", c: `-(${nu * nu})`, d: "x^2",
  };
}

function slForm(r: Rng): Draft {
  const f = form(r);
  const pqr = `p = ${f.p[0]},\\ q = ${f.q[0]},\\ r = ${f.r[0]}`;
  return {
    prompt: `Put ${m(f.eq)} in Sturm–Liouville form ${m("(py')' + (q + \\lambda r)y = 0")}. Give ${m("p, q, r")}.`,
    answer: {
      kind: "tuple",
      fields: [
        { label: "p", tex: "p(x)", ref: f.p[1], mode: "expr" },
        { label: "q", tex: "q(x)", ref: f.q[1], mode: "expr" },
        { label: "r", tex: "r(x)", ref: f.r[1], mode: "expr" },
      ],
      vars: ["x"],
      proportional: true,
    },
    answerTex: pqr,
    steps: [
      `Read off ${m(`a = ${f.aTex}`)} (on ${m("y''")}) and ${m(`b = ${f.bTex}`)} (on ${m("y'")}).`,
      `${m(`p = e^{\\int b/a\\,dx} = e^{\\int ${f.ratioTex}\\,dx} = e^{${f.intTex}} = ${f.p[0]}`)}.`,
      `Multiply the equation by ${m("p/a")}: then ${m("q = c\\,p/a")} and ${m("r = d\\,p/a")} for the ${m("y")} and ${m("\\lambda y")} coefficients.`,
      m(pqr) + " (any common constant multiple also works).",
    ],
    meta: { variant: "form", a: f.a, b: f.b, c: f.c, d: f.d, p: f.p[1], q: f.q[1], r: f.r[1] },
  };
}

// ── classify ───────────────────────────────────────────────────────────────
const SL_OPTIONS = ["Regular", "Periodic", "Singular"];
const SL_CASES: [number, string, string][] = [
  [0, "y'' + \\lambda y = 0,\\ y(0) = 0,\\ y'(2) = 0", "On a finite interval with p = 1 > 0, r = 1 > 0 and one separated condition at each end: regular."],
  [0, "(xy')' + \\frac{\\lambda}{x}y = 0,\\ y(1) = 0,\\ y(e) = 0", "p = x and r = 1/x are positive and continuous on [1, e], separated conditions at both ends: regular."],
  [0, "(e^{2x}y')' + \\lambda e^{2x}y = 0,\\ y(0) = 0,\\ y(1) = 0", "p = r = e^{2x} > 0 on [0, 1] with separated conditions: regular."],
  [0, "y'' + \\lambda y = 0,\\ y(0) + y'(0) = 0,\\ y(1) = 0", "Mixed (Robin) conditions are still separated, one at each end: regular."],
  [1, "y'' + \\lambda y = 0,\\ y(-\\pi) = y(\\pi),\\ y'(-\\pi) = y'(\\pi)", "Conditions tie the two endpoints together and p(−π) = p(π): periodic."],
  [1, "y'' + \\lambda y = 0,\\ y(-1) = y(1),\\ y'(-1) = y'(1)", "Endpoint values are matched to each other, not set separately: periodic."],
  [1, "y'' + \\lambda y = 0,\\ y(0) = y(2\\pi),\\ y'(0) = y'(2\\pi)", "Values and slopes are matched across the interval: periodic."],
  [2, "((1 - x^{2})y')' + \\lambda y = 0 \\text{ on } [-1, 1],\\ y \\text{ bounded}", "p = 1 − x² vanishes at both endpoints, so only boundedness is imposed there: singular (Legendre)."],
  [2, "(xy')' + \\left(\\lambda x - \\frac{4}{x}\\right)y = 0 \\text{ on } [0, 1],\\ y(1) = 0", "p = x vanishes at x = 0 (and q blows up there): singular (Bessel)."],
  [2, "(xe^{-x}y')' + \\lambda e^{-x}y = 0 \\text{ on } [0, \\infty)", "Infinite interval and p = xe^{−x} vanishes at 0: singular (Laguerre)."],
  [2, "(\\sqrt{1 - x^{2}}\\,y')' + \\frac{\\lambda}{\\sqrt{1 - x^{2}}}y = 0 \\text{ on } [-1, 1]", "p vanishes and r blows up at ±1: singular (Chebyshev)."],
];

function slClassify(r: Rng): Draft {
  const kind = r.int(0, 2);
  const [k, tex, why] = r.pick(SL_CASES.filter((c) => c[0] === kind));
  return {
    prompt: `Is this Sturm–Liouville problem regular, periodic, or singular? ${m(tex)}`,
    answer: { kind: "choice", options: SL_OPTIONS, correct: SL_OPTIONS[k] },
    answerTex: `\\text{${SL_OPTIONS[k]}}`,
    steps: [
      `Regular: finite interval, ${m("p, p', q, r")} continuous with ${m("p, r > 0")}, one separated condition at each end. Periodic: ${m("p(a) = p(b)")} with ${m("y(a)=y(b),\\ y'(a)=y'(b)")}. Singular: ${m("p")} vanishes at an endpoint or the interval is infinite.`,
      why,
    ],
    meta: { variant: "classify" },
  };
}

// ── shifted spectrum: y'' + (λ + c)y = 0 ───────────────────────────────────
// Substitute ω = λ + c: the boundary-value problem for ω is the plain one, so
// ω_n = μ_n² and λ_n = μ_n² − c. Eigenfunctions don't change; eigenvalues can go
// negative (or hit zero), which is the point of the drill.
interface Shifted {
  e: Eigen;
  c: number;
  eqTex: string;
  lamTex: string;
  lamJs: string;
  nTex: string;
}

function shifted(r: Rng): Shifted {
  const e = eigen(r);
  const c = r.pick([1, 2, 3, 4, 4, 4, 9, 9, -1, -2, -4]);
  const lamTex = `${e.lamTex} ${c > 0 ? "-" : "+"} ${Math.abs(c)}`;
  return {
    e, c,
    eqTex: `y'' + (\\lambda ${c > 0 ? "+" : "-"} ${Math.abs(c)})y = 0,\\ ${e.bcTex}`,
    lamTex,
    lamJs: `${e.lamJs} - (${c})`,
    nTex: `n = ${e.start}, ${e.start + 1}, ${e.start + 2}, \\dots`,
  };
}

function shiftSteps(S: Shifted): string[] {
  const { c } = S;
  return [
    `Let ${m(`\\omega = \\lambda ${c > 0 ? "+" : "-"} ${Math.abs(c)}`)}: the equation becomes ${m("y'' + \\omega y = 0")} with the same boundary conditions.`,
    ...eigenSteps(S.e).map((t) => t.replace(/\\lambda/g, "\\omega")),
    `Undo the substitution: ${m(`\\lambda_n = \\omega_n ${c > 0 ? "-" : "+"} ${Math.abs(c)} = ${S.lamTex}`)}.`,
  ];
}

function shiftEigenvalues(r: Rng): Draft {
  const S = shifted(r);
  return {
    prompt: `Find the eigenvalues ${m("\\lambda_n")} of ${m(S.eqTex)}.`,
    answer: { kind: "indexed", ref: S.lamJs, start: S.e.start, label: "λ_n" },
    answerTex: `\\lambda_n = ${S.lamTex},\\quad ${S.nTex}`,
    steps: [...shiftSteps(S), m(`\\lambda_n = ${S.lamTex},\\quad ${S.nTex}`)],
    meta: { variant: S.e.bc, L: S.e.Ljs, y: S.e.yJs, lam: S.e.lamJs, start: S.e.start, shift: S.c },
  };
}

function shiftEigenfunctions(r: Rng): Draft {
  const S = shifted(r);
  const e = S.e;
  return {
    prompt: `Find the eigenfunctions ${m("y_n(x)")} of ${m(S.eqTex)}.`,
    answer: { kind: "eigenfunctions", bcs: e.bcs, L: e.L, refLambda: e.lamJs, start: e.start },
    answerTex: `y_n = ${e.yTex},\\quad n = ${e.start}, ${e.start + 1}, \\dots` + (e.bc === "NN" ? "\\ (y_0 = 1)" : ""),
    steps: [
      ...shiftSteps(S).slice(0, -1),
      `The shift moves the eigenvalues, not the eigenfunctions: ${m(`y_n = ${e.yTex}`)} (any nonzero multiple), with ${m(`\\lambda_n = ${S.lamTex}`)}.`,
    ],
    meta: { variant: e.bc, L: e.Ljs, y: e.yJs, lam: e.lamJs, start: e.start, shift: S.c },
  };
}

function shiftNegative(r: Rng): Draft {
  const S = shifted(r);
  const e = S.e;
  const lam = (n: number) => {
    const k = e.bc === "DD" || e.bc === "NN" ? (n * Math.PI) / e.L : ((2 * n - 1) * Math.PI) / (2 * e.L);
    return k * k - S.c;
  };
  const vals = Array.from({ length: 40 }, (_, i) => lam(e.start + i));
  const neg = vals.filter((v) => v < -1e-9).length;
  const zero = vals.some((v) => Math.abs(v) < 1e-9);
  const listed = vals.slice(0, Math.max(neg + 1, 2)).map((v, i) => {
    const n = e.start + i;
    return `\\lambda_{${n}} ${Math.abs(v - Math.round(v)) < 1e-9 ? `= ${Math.round(v)}` : `\\approx ${v.toFixed(2)}`}`;
  });
  return {
    prompt: `How many negative eigenvalues does ${m(S.eqTex)} have?`,
    answer: { kind: "expression", ref: `${neg}`, vars: [], label: "count" },
    answerTex: `${neg}`,
    steps: [
      `From ${m("\\omega = \\lambda " + (S.c > 0 ? "+" : "-") + " " + Math.abs(S.c))}: ${m(`\\lambda_n = ${S.lamTex}`)}, ${m(S.nTex)}.`,
      `${m(listed.join(",\\ "))}${vals.length > listed.length ? ", and they only grow from there" : ""}.`,
      `${neg} negative${zero ? `; one eigenvalue is exactly ${m("0")}, which is not negative` : ""}. ${S.c < 0 ? "A negative shift only pushes the eigenvalues up." : ""}`.trim(),
    ],
    meta: { variant: "negative-count", bc: e.bc, L: e.Ljs, lam: e.lamJs, start: e.start, shift: S.c },
  };
}

export const STURM_TEMPLATES: Record<string, (r: Rng) => Draft> = {
  "sl-eigenvalues": eigenvalues,
  "sl-eigenfunctions": eigenfunctions,
  "sl-form": slForm,
  "sl-classify": slClassify,
  "sl-shift-eigenvalues": shiftEigenvalues,
  "sl-shift-eigenfunctions": shiftEigenfunctions,
  "sl-shift-negative": shiftNegative,
};
