// Kreyszig §2.2 (characteristic equation) and §2.7 (undetermined coefficients), Level 1.
// Variable x, characteristic variable λ (Kreyszig's notation).
// Everything is built backward: pick the roots, then the solution constants or
// the particular-solution coefficients, then compute the equation and its data.
import { Rng } from "./rng";
import type { Draft } from "./types";
import { ct, ex, gcd, join, m } from "./tex";
import { Q } from "./rational";
import { require_ } from "./reject";

const X = (k: number) => (k === 1 ? "x" : k === -1 ? "-x" : `${k}x`);
const kx = (k: number) => (k === 1 ? "x" : `${k}x`); // inside cos/sin, k > 0
const one = (k: number) => (k === 1 ? "" : `${k}`); // coefficient that may be 1

/** a y'' + b y' + c y  (LaTeX) */
function lhs(a: number, b: number, c: number) {
  return join([ct(a, "y''"), ct(b, "y'"), ct(c, "y")]);
}
/** a λ² + b λ + c (LaTeX) */
function charPoly(a: number, b: number, c: number) {
  return join([ct(a, "\\lambda^2"), ct(b, "\\lambda"), c ? `${c}` : "0"]);
}
const cexp = (k: number) => ex(k); // e^{kx}, "" for k = 0

// ── homogeneous: roots ─────────────────────────────────────────────────────
type Roots =
  | { type: "distinct"; a: number; r1: Q; r2: Q }
  | { type: "repeated"; a: number; r: Q }
  | { type: "complex"; a: number; al: number; be: number };

/** a λ² + b λ + c from the roots; a clears denominators. */
function coeffs(R: Roots): [number, number, number] {
  if (R.type === "distinct") {
    const s = R.r1.add(R.r2), p = R.r1.mul(R.r2);
    return [R.a, -s.mul(R.a).n / s.mul(R.a).d, p.mul(R.a).n / p.mul(R.a).d];
  }
  if (R.type === "repeated") {
    const s = R.r.mul(2), p = R.r.mul(R.r);
    return [R.a, -s.mul(R.a).n / s.mul(R.a).d, p.mul(R.a).n / p.mul(R.a).d];
  }
  return [R.a, -2 * R.al * R.a, (R.al * R.al + R.be * R.be) * R.a];
}

function distinctRoots(r: Rng, allowHalf = true): Roots {
  if (allowHalf && r.chance(0.25)) {
    // (λ - p)(2λ - k), k odd
    const p = r.int(-4, 4);
    const k = r.pick([-5, -3, -1, 1, 3, 5]);
    return { type: "distinct", a: 2, r1: new Q(p), r2: new Q(k, 2) };
  }
  const p = r.int(-5, 5);
  const q = r.int(-5, 5);
  require_(p !== q);
  return { type: "distinct", a: 1, r1: new Q(Math.min(p, q)), r2: new Q(Math.max(p, q)) };
}

function repeatedRoot(r: Rng): Roots {
  if (r.chance(0.25)) return { type: "repeated", a: 4, r: new Q(r.pick([-3, -1, 1, 3]), 2) };
  const p = r.int(-4, 4);
  require_(p !== 0);
  return { type: "repeated", a: 1, r: new Q(p) };
}

function complexRoots(r: Rng): Roots {
  return { type: "complex", a: 1, al: r.pick([0, 0, -1, 1, -2, 2, -3, 3]), be: r.int(1, 4) };
}

/** e^{qx} for a rational q, LaTeX and mathjs */
function eq(q: Q): [string, string] {
  if (q.isZero()) return ["", "1"];
  const k = q.d === 1 ? X(q.n) : `${q.n < 0 ? "-" : ""}\\frac{${one(Math.abs(q.n)) || ""}x}{${q.d}}`;
  return [`e^{${k}}`, `exp((${q.n}/${q.d})*x)`];
}

const rootsTex = (R: Roots) =>
  R.type === "distinct"
    ? `\\lambda_1 = ${R.r1.tex()},\\ \\lambda_2 = ${R.r2.tex()}`
    : R.type === "repeated"
      ? `\\lambda = ${R.r.tex()}\\ (\\text{double root})`
      : `\\lambda = ${R.al ? `${R.al} \\pm ${one(R.be)}i` : `\\pm ${one(R.be)}i`}`;

/** general solution: LaTeX, mathjs (C1, C2), and the "which case" sentence */
function general(R: Roots): { tex: string; js: string; why: string } {
  if (R.type === "distinct") {
    const [t1, j1] = eq(R.r1), [t2, j2] = eq(R.r2);
    return {
      tex: `y = ${join([t1 ? `c_1${t1}` : "c_1", t2 ? `c_2${t2}` : "c_2"])}`,
      js: `C1*${j1} + C2*${j2}`,
      why: `Two distinct real roots: each gives a solution ${m("e^{\\lambda x}")}.`,
    };
  }
  if (R.type === "repeated") {
    const [t, j] = eq(R.r);
    return {
      tex: `y = (c_1 + c_2x)${t}`,
      js: `(C1 + C2*x)*${j}`,
      why: `A double root gives only one exponential, so the second solution is ${m("xe^{\\lambda x}")}.`,
    };
  }
  const trig = `c_1\\cos ${kx(R.be)} + c_2\\sin ${kx(R.be)}`;
  return {
    tex: R.al ? `y = ${cexp(R.al)}\\left(${trig}\\right)` : `y = ${trig}`,
    js: `exp((${R.al})*x)*(C1*cos(${R.be}*x) + C2*sin(${R.be}*x))`,
    why: `Complex roots ${m("\\alpha \\pm \\beta i")} give ${m("e^{\\alpha x}\\cos\\beta x")} and ${m("e^{\\alpha x}\\sin\\beta x")}.`,
  };
}

function charSteps(R: Roots): string[] {
  const [a, b, c] = coeffs(R);
  const disc = b * b - 4 * a * c;
  return [
    `Characteristic equation: ${m(`${charPoly(a, b, c)} = 0`)}; discriminant ${m(`b^2 - 4ac = ${disc}`)}.`,
    `${m(rootsTex(R))}.`,
  ];
}

function homogeneousGeneral(pick: (r: Rng) => Roots) {
  return (r: Rng): Draft => {
    const R = pick(r);
    const [a, b, c] = coeffs(R);
    const G = general(R);
    return {
      prompt: `Find the general solution of ${m(`${lhs(a, b, c)} = 0`)}.`,
      answer: { kind: "ode2", a, b, c, v: "x", ref: G.js },
      answerTex: G.tex,
      steps: [...charSteps(R), G.why, m(G.tex)],
      meta: { variant: R.type },
    };
  };
}

function homogeneousIvp(r: Rng): Draft {
  const type = r.pick(["distinct", "repeated", "complex"] as const);
  const R =
    type === "distinct"
      ? distinctRoots(r, false)
      : type === "repeated"
        ? repeatedRoot(r)
        : complexRoots(r);
  require_(R.type !== "repeated" || R.r.d === 1);
  const [a, b, c] = coeffs(R);
  const C1 = r.int(-3, 4);
  const C2 = r.int(-3, 4);
  require_(C1 !== 0 || C2 !== 0);
  let y0: number, v0: number, sol: string, js: string, ic: string;
  if (R.type === "distinct") {
    const p = R.r1.n, q = R.r2.n;
    y0 = C1 + C2;
    v0 = p * C1 + q * C2;
    ic = `${m(`c_1 + c_2 = ${y0}`)} and ${m(`${join([ct(p, "c_1"), ct(q, "c_2")])} = ${v0}`)}, so ${m(`c_1 = ${C1},\\ c_2 = ${C2}`)}`;
    sol = join([C1 ? (p ? ct(C1, cexp(p)) : `${C1}`) : "0", C2 ? (q ? ct(C2, cexp(q)) : `${C2}`) : "0"]);
    js = `(${C1})*exp(${p}*x) + (${C2})*exp(${q}*x)`;
  } else if (R.type === "repeated") {
    const p = R.r.n;
    y0 = C1;
    v0 = p * C1 + C2;
    ic = `${m(`y(0) = c_1 = ${y0}`)}; ${m(`y'(0) = ${join([ct(p, "c_1"), "c_2"])} = ${v0}`)}, so ${m(`c_2 = ${C2}`)}`;
    sol = C1 && C2 ? `\\left(${join([`${C1}`, ct(C2, "x")])}\\right)${cexp(p)}` : C1 ? ct(C1, cexp(p)) : ct(C2, `x${cexp(p)}`);
    js = `((${C1}) + (${C2})*x)*exp(${p}*x)`;
  } else {
    const { al, be } = R;
    y0 = C1;
    v0 = al * C1 + be * C2;
    ic = `${m(`y(0) = c_1 = ${y0}`)}; ${m(`y'(0) = ${join([ct(al, "c_1"), ct(be, "c_2")])} = ${v0}`)}, so ${m(`c_2 = ${C2}`)}`;
    const trig = join([ct(C1, `\\cos ${kx(be)}`), ct(C2, `\\sin ${kx(be)}`)]);
    sol = al ? (C1 && C2 ? `${cexp(al)}\\left(${trig}\\right)` : `${trig}${cexp(al)}`) : trig;
    js = `exp((${al})*x)*((${C1})*cos(${be}*x) + (${C2})*sin(${be}*x))`;
  }
  const G = general(R);
  return {
    prompt: `Solve the initial value problem ${m(`${lhs(a, b, c)} = 0,\\quad y(0) = ${y0},\\ y'(0) = ${v0}`)}.`,
    answer: { kind: "ode2", a, b, c, v: "x", ic: [0, y0, v0], ref: js },
    answerTex: `y = ${sol}`,
    steps: [...charSteps(R), `General solution ${m(G.tex)}.`, ic + ".", m(`y = ${sol}`)],
    meta: { variant: `ivp-${R.type}` },
  };
}

// ── undetermined coefficients ──────────────────────────────────────────────
// Monic equations y'' + b y' + c y = f(x) with integer or complex roots.
interface Monic {
  b: number;
  c: number;
  roots: number[]; // real roots (with multiplicity); empty when complex
  R: Roots;
}
function monic(r: Rng, kind: "any" | "nonzero" = "any"): Monic {
  const t = r.int(0, 2);
  let R: Roots;
  if (t === 0) {
    const p = r.int(-3, 3), q = r.int(-3, 3);
    require_(p < q);
    R = { type: "distinct", a: 1, r1: new Q(p), r2: new Q(q) };
  } else if (t === 1) {
    const p = r.int(-3, 3);
    require_(p !== 0);
    R = { type: "repeated", a: 1, r: new Q(p) };
  } else R = { type: "complex", a: 1, al: r.int(-2, 2), be: r.int(1, 3) };
  const [, b, c] = coeffs(R);
  const roots = R.type === "distinct" ? [R.r1.n, R.r2.n] : R.type === "repeated" ? [R.r.n, R.r.n] : [];
  if (kind === "nonzero") require_(c !== 0);
  return { b, c, roots, R };
}
const P = (M: Monic, k: number) => k * k + M.b * k + M.c;

/** polynomial with integer coefficients (high → low) in x: LaTeX, mathjs */
function poly(cs: number[]): [string, string] {
  const deg = cs.length - 1;
  const tex = join(cs.map((k, i) => ct(k, deg - i === 0 ? "" : deg - i === 1 ? "x" : `x^{${deg - i}}`)));
  const js = cs.map((k, i) => `(${k})*x^${deg - i}`).join(" + ");
  return [tex, js];
}

function ucPoly(r: Rng): Draft {
  const M = monic(r, "nonzero");
  const deg = r.pick([1, 2, 2]);
  const A = deg === 2 ? [r.pick([1, -1, 2, -2, 3]), r.int(-3, 3), r.int(-3, 3)] : [r.pick([1, -1, 2, -2, 3]), r.int(-4, 4)];
  const [A2, A1, A0] = deg === 2 ? A : [0, A[0], A[1]];
  const f = deg === 2 ? [M.c * A2, 2 * M.b * A2 + M.c * A1, 2 * A2 + M.b * A1 + M.c * A0] : [M.c * A1, M.b * A1 + M.c * A0];
  require_(f.every((k) => Math.abs(k) <= 40));
  const [ft, fj] = poly(f);
  const [yt, yj] = poly(deg === 2 ? [A2, A1, A0] : [A1, A0]);
  const trial = deg === 2 ? "y_p = Kx^2 + Mx + N" : "y_p = Kx + M";
  const eqs =
    deg === 2
      ? `${m("x^2")}: ${m(`${ct(M.c, "K")} = ${f[0]}`)}; ${m("x")}: ${m(`${join([ct(2 * M.b, "K"), ct(M.c, "M")])} = ${f[1]}`)}; ${m("1")}: ${m(`${join(["2K", ct(M.b, "M"), ct(M.c, "N")])} = ${f[2]}`)}`
      : `${m("x")}: ${m(`${ct(M.c, "K")} = ${f[0]}`)}; ${m("1")}: ${m(`${join([ct(M.b, "K"), ct(M.c, "M")])} = ${f[1]}`)}`;
  return {
    prompt: `Find a particular solution of ${m(`${lhs(1, M.b, M.c)} = ${ft}`)}.`,
    answer: { kind: "ode2", a: 1, b: M.b, c: M.c, v: "x", rhs: fj, particular: true, ref: yj },
    answerTex: `y_p = ${yt}`,
    steps: [
      `The right side is a degree-${deg} polynomial and ${m("\\lambda = 0")} is not a root, so try ${m(trial)}.`,
      `Substitute and match coefficients — ${eqs}.`,
      m(`y_p = ${yt}`),
    ],
    meta: { variant: "poly", f },
  };
}

function ucExp(r: Rng): Draft {
  const M = monic(r);
  const k = r.pick([-3, -2, -1, 1, 2, 3]);
  const Pk = P(M, k);
  require_(Pk !== 0 && Math.abs(Pk) <= 20);
  const A = r.pick([1, -1, 2, -2, 3, 1]);
  const K = A * Pk;
  const fTex = ct(K, ex(k));
  return {
    prompt: `Find a particular solution of ${m(`${lhs(1, M.b, M.c)} = ${fTex}`)}.`,
    answer: { kind: "ode2", a: 1, b: M.b, c: M.c, v: "x", rhs: `(${K})*exp(${k}*x)`, particular: true, ref: `(${A})*exp(${k}*x)` },
    answerTex: `y_p = ${ct(A, ex(k))}`,
    steps: [
      `${m(`\\lambda = ${k}`)} is not a root of ${m(`${charPoly(1, M.b, M.c)}`)}, so try ${m(`y_p = K${ex(k)}`)}.`,
      `Substituting: ${m(`\\left(${join([`${k * k}`, `${M.b * k}`, `${M.c}`])}\\right)K${ex(k)} = ${ct(Pk, "K")}${ex(k)}`)}.`,
      `${m(`${ct(Pk, "K")} = ${K} \\Rightarrow K = ${A}`)}, so ${m(`y_p = ${ct(A, ex(k))}`)}.`,
    ],
    meta: { variant: "exp" },
  };
}

function ucTrig(r: Rng): Draft {
  const M = monic(r);
  const w = r.int(1, 3);
  const p = M.c - w * w, q = M.b * w;
  require_(p !== 0 || q !== 0);
  const g = gcd(p, q);
  const s = r.pick([1, -1, 2]);
  const useCos = r.chance(0.5);
  // A cos + B sin with (A, B) ∝ (p, q) gives a pure cosine; ∝ (-q, p) a pure sine
  const A = useCos ? (s * p) / g : (-s * q) / g;
  const B = useCos ? (s * q) / g : (s * p) / g;
  const K = (s * (p * p + q * q)) / g;
  require_(Math.abs(K) <= 60);
  const fn = useCos ? "\\cos" : "\\sin";
  const fTex = ct(K, `${fn} ${kx(w)}`);
  const yp = join([ct(A, `\\cos ${kx(w)}`), ct(B, `\\sin ${kx(w)}`)]);
  return {
    prompt: `Find a particular solution of ${m(`${lhs(1, M.b, M.c)} = ${fTex}`)}.`,
    answer: {
      kind: "ode2", a: 1, b: M.b, c: M.c, v: "x", particular: true,
      rhs: `(${K})*${useCos ? "cos" : "sin"}(${w}*x)`, ref: `(${A})*cos(${w}*x) + (${B})*sin(${w}*x)`,
    },
    answerTex: `y_p = ${yp}`,
    steps: [
      `${m(`\\pm ${one(w)}i`)} are not roots, so try ${m(`y_p = K\\cos ${kx(w)} + M\\sin ${kx(w)}`)} (both terms, even though the right side has one).`,
      `Substituting: ${m("\\cos")}: ${m(`${join([ct(p, "K"), ct(q, "M")])} = ${useCos ? K : 0}`)}; ${m("\\sin")}: ${m(`${join([ct(-q, "K"), ct(p, "M")])} = ${useCos ? 0 : K}`)}.`,
      `${m(`K = ${A},\\ M = ${B}`)}, so ${m(`y_p = ${yp}`)}.`,
    ],
    meta: { variant: "trig" },
  };
}

function ucResonance(r: Rng): Draft {
  const variant = r.pick(["simple", "double", "trig"] as const);
  const A = r.pick([1, -1, 2, -2, 3]);
  if (variant === "trig") {
    const w = r.int(1, 4);
    const useCos = r.chance(0.5);
    // L[x sin wx] = 2w cos wx, L[x cos wx] = -2w sin wx
    const K = useCos ? 2 * w * A : -2 * w * A;
    const fTex = ct(K, `${useCos ? "\\cos" : "\\sin"} ${kx(w)}`);
    const ypTex = ct(A, `x${useCos ? "\\sin" : "\\cos"} ${kx(w)}`);
    return {
      prompt: `Find a particular solution of ${m(`y'' + ${w * w}y = ${fTex}`)}.`,
      answer: {
        kind: "ode2", a: 1, b: 0, c: w * w, v: "x", particular: true,
        rhs: `(${K})*${useCos ? "cos" : "sin"}(${w}*x)`, ref: `(${A})*x*${useCos ? "sin" : "cos"}(${w}*x)`,
      },
      answerTex: `y_p = ${ypTex}`,
      steps: [
        `${m(`\\lambda = \\pm ${one(w)}i`)} are roots, so ${m(`\\cos ${kx(w)}`)} and ${m(`\\sin ${kx(w)}`)} already solve the homogeneous equation. Modification rule: multiply by ${m("x")}.`,
        `Try ${m(`y_p = x(K\\cos ${kx(w)} + M\\sin ${kx(w)})`)}: ${m(`y_p'' + ${w * w}y_p = ${2 * w}(M\\cos ${kx(w)} - K\\sin ${kx(w)})`)}.`,
        `${useCos ? m(`${2 * w}M = ${K},\\ K = 0`) : m(`-${2 * w}K = ${K},\\ M = 0`)}, so ${m(`y_p = ${ypTex}`)}.`,
      ],
      meta: { variant: "resonance-trig" },
    };
  }
  let b: number, c: number, k: number, K: number, ypTex: string, ypJs: string, steps: string[];
  if (variant === "simple") {
    const p = r.int(-3, 3), q = r.int(-3, 3);
    require_(p !== q);
    b = -(p + q);
    c = p * q;
    k = p;
    K = A * (p - q); // L[x e^{px}] = P'(p) e^{px} = (2p + b) e^{px} = (p - q) e^{px}
    ypTex = ct(A, `x${ex(p)}`);
    ypJs = `(${A})*x*exp(${p}*x)`;
    steps = [
      `Roots ${m(`\\lambda = ${p},\\ ${q}`)}: ${m(`${ex(p) || "1"}`)} already solves the homogeneous equation (simple root). Modification rule: try ${m(`y_p = Kx${ex(p)}`)}.`,
      `Substituting, the ${m(`x${ex(p)}`)} terms cancel and ${m(`${ct(p - q, "K")}${ex(p)}`)} remains.`,
      `${m(`${ct(p - q, "K")} = ${K} \\Rightarrow K = ${A}`)}, so ${m(`y_p = ${ypTex}`)}.`,
    ];
  } else {
    const p = r.pick([-3, -2, -1, 1, 2, 3]);
    b = -2 * p;
    c = p * p;
    k = p;
    K = 2 * A; // L[x² e^{px}] = 2 e^{px} for a double root p
    ypTex = ct(A, `x^2${ex(p)}`);
    ypJs = `(${A})*x^2*exp(${p}*x)`;
    steps = [
      `${m(`\\lambda = ${p}`)} is a double root: both ${m(ex(p))} and ${m(`x${ex(p)}`)} solve the homogeneous equation. Modification rule (double root): try ${m(`y_p = Kx^2${ex(p)}`)}.`,
      `Substituting, everything cancels except ${m(`2K${ex(p)}`)}.`,
      `${m(`2K = ${K} \\Rightarrow K = ${A}`)}, so ${m(`y_p = ${ypTex}`)}.`,
    ];
  }
  require_(K !== 0);
  return {
    prompt: `Find a particular solution of ${m(`${lhs(1, b, c)} = ${ct(K, ex(k))}`)}.`,
    answer: { kind: "ode2", a: 1, b, c, v: "x", particular: true, rhs: `(${K})*exp(${k}*x)`, ref: ypJs },
    answerTex: `y_p = ${ypTex}`,
    steps,
    meta: { variant: `resonance-${variant}` },
  };
}

function ucGeneral(r: Rng): Draft {
  const sub = r.chance(0.5) ? ucPoly(r) : ucExp(r);
  const a = sub.answer as Extract<Draft["answer"], { kind: "ode2" }>;
  const R = rootsFor(a.b, a.c);
  const G = general(R);
  const yh = G.tex.replace(/^y = /, "");
  const yp = sub.answerTex.replace(/^y_p = /, "");
  const tex = `y = ${yh} + ${yp}`.replace("+ -", "- ");
  return {
    prompt: sub.prompt.replace("Find a particular solution of", "Find the general solution of"),
    answer: { ...a, particular: undefined, ref: `${G.js} + ${a.ref}` },
    answerTex: tex,
    steps: [
      `Homogeneous part: ${m(rootsTex(R))}, so ${m(`y_h = ${yh}`)}.`,
      ...sub.steps.slice(0, -1),
      `${m(`y = y_h + y_p = ${yh} + ${yp}`.replace("+ -", "- "))}.`,
    ],
    meta: { variant: `general-${(sub.meta as any).variant}` },
  };
}

/** roots of λ² + bλ + c for the monic equations above */
function rootsFor(b: number, c: number): Roots {
  const disc = b * b - 4 * c;
  if (disc > 0) {
    const s = Math.round(Math.sqrt(disc));
    return { type: "distinct", a: 1, r1: new Q(-b - s, 2), r2: new Q(-b + s, 2) };
  }
  if (disc === 0) return { type: "repeated", a: 1, r: new Q(-b, 2) };
  return { type: "complex", a: 1, al: -b / 2, be: Math.round(Math.sqrt(-disc) / 2) };
}

export const LINEAR2_TEMPLATES: Record<string, (r: Rng) => Draft> = {
  "char-distinct": homogeneousGeneral((r) => distinctRoots(r)),
  "char-repeated": homogeneousGeneral(repeatedRoot),
  "char-complex": homogeneousGeneral(complexRoots),
  "char-ivp": homogeneousIvp,
  "uc-poly": ucPoly,
  "uc-exp": ucExp,
  "uc-trig": ucTrig,
  "uc-resonance": ucResonance,
  "uc-general": ucGeneral,
};
