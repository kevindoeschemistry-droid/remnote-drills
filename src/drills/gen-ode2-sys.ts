// Kreyszig 10e §2.1 (reduction of order), §2.5 (Euler–Cauchy), §2.8 (forced oscillations),
// §2.10 (variation of parameters), Ch 3 (higher-order constant coefficients),
// Ch 4 (2×2 systems y' = Ay by eigenvalues; phase-portrait type).
// Everything is built backward: pick roots / eigenvalues / solution constants first,
// then compute the equation and its data, so every answer is clean.
//
// Answers that aren't constant-coefficient second order use the additive extensions:
//   ode2 + coef   (Σ coef_i(x) y^(n-i) = f: Euler–Cauchy, reduction of order, higher order)
//   tuple + system (components of a solution of y' = Ay)
import { Rng } from "./rng";
import type { Answer, Draft } from "./types";
import { ct, ex, gcd, join, m } from "./tex";
import { Q, qterm } from "./rational";
import { require_ } from "./reject";

const kx = (k: number, v = "x") => (k === 1 ? v : `${k}${v}`); // k > 0
const one = (k: number) => (k === 1 ? "" : `${k}`);
const par = (n: number) => (n < 0 ? `(${n})` : `${n}`);

/** x^q LaTeX ("" for q = 0) */
function xq(q: Q, v = "x"): string {
  if (q.isZero()) return "";
  if (q.n === 1 && q.d === 1) return v;
  return `${v}^{${q.d === 1 ? q.n : `${q.n}/${q.d}`}}`;
}
const xqj = (q: Q, v = "x") => (q.isZero() ? "1" : `${v}^(${q.n}/${q.d})`);
const Qi = (n: number) => new Q(n);
/** k·x for an integer k: x, -x, 3x */
const X = (k: number, v = "x") => (k === 1 ? v : k === -1 ? `-${v}` : `${k}${v}`);
/** e^{qx} for a rational q */
const eQ = (q: Q) => (q.d === 1 ? ex(q.n) : `e^{${q.n < 0 ? "-" : ""}${Math.abs(q.n) === 1 ? "" : Math.abs(q.n)}x/${q.d}}`);
/** (m - q) factor, LaTeX */
const mFactor = (q: Q, v = "m") => (q.isZero() ? v : `(${v} ${q.n < 0 ? "+" : "-"} ${(q.n < 0 ? q.neg() : q).tex()})`);

/** LaTeX for the constant-coefficient operator a y'' + b y' + c y in y */
const lhs2 = (a: number, b: number, c: number) => join([ct(a, "y''"), ct(b, "y'"), ct(c, "y")]);

function ode2(a: number, b: number, c: number, v: string, ref: string, extra: Partial<Extract<Answer, { kind: "ode2" }>> = {}): Answer {
  return { kind: "ode2", a, b, c, v, ref, ...extra };
}
function odeN(coef: string[], ref: string, extra: Partial<Extract<Answer, { kind: "ode2" }>> = {}): Answer {
  return { kind: "ode2", a: 0, b: 0, c: 0, v: "x", coef, ref, ...extra };
}

// ═════════════════════════════════════════════════════════════════════════
// §2.5 Euler–Cauchy  A x² y'' + B x y' + C y = 0,  auxiliary  A m² + (B − A) m + C = 0
// ═════════════════════════════════════════════════════════════════════════
interface EC {
  A: number;
  B: number;
  C: number;
  type: "distinct" | "double" | "complex";
  m1: Q;
  m2: Q;
  mu: number;
  nu: number;
}

function ecReal(m1: Q, m2: Q): EC {
  const A = m1.d * m2.d;
  const B = new Q(A).sub(m1.add(m2).mul(A));
  const C = m1.mul(m2).mul(A);
  require_(B.isInt() && C.isInt() && Math.abs(B.n) <= 30 && Math.abs(C.n) <= 30);
  const [lo, hi] = m1.value() <= m2.value() ? [m1, m2] : [m2, m1];
  return { A, B: B.n, C: C.n, type: lo.value() === hi.value() ? "double" : "distinct", m1: lo, m2: hi, mu: 0, nu: 0 };
}

/** distinct real roots, never 1 (then y = x would solve the equation) */
function ecDistinct(r: Rng, half = true): EC {
  const p = r.int(-3, 4);
  require_(p !== 1);
  if (half && r.chance(0.25)) return ecReal(Qi(p), new Q(r.pick([-3, -1, 1, 3, 5]), 2));
  const q = r.int(-3, 4);
  require_(q !== 1 && q !== p);
  return ecReal(Qi(p), Qi(q));
}
function ecDouble(r: Rng, half = true): EC {
  if (half && r.chance(0.25)) {
    const q = new Q(r.pick([-3, -1, 1, 3]), 2);
    return ecReal(q, q);
  }
  const p = r.int(-3, 3);
  require_(p !== 1);
  return ecReal(Qi(p), Qi(p));
}
function ecComplex(r: Rng): EC {
  const mu = r.int(-2, 2), nu = r.int(1, 3);
  return { A: 1, B: 1 - 2 * mu, C: mu * mu + nu * nu, type: "complex", m1: Qi(0), m2: Qi(0), mu, nu };
}

const ecTex = (E: EC) => `${join([ct(E.A, "x^2y''"), ct(E.B, "xy'"), ct(E.C, "y")])}`;
const ecCoef = (E: EC) => [`${E.A}*x^2`, `${E.B}*x`, `${E.C}`];
const auxTex = (E: EC) => `${join([ct(E.A, "m^2"), ct(E.B - E.A, "m"), E.C ? `${E.C}` : ""])} = 0`;
const nuLn = (nu: number) => (nu === 1 ? "\\ln x" : `${nu}\\ln x`);
const ecRootsTex = (E: EC) =>
  E.type === "distinct"
    ? `m_1 = ${E.m1.tex()},\\ m_2 = ${E.m2.tex()}`
    : E.type === "double"
      ? `m = ${E.m1.tex()}\\ (\\text{double root})`
      : `m = ${E.mu ? `${E.mu} \\pm ${one(E.nu)}i` : `\\pm ${one(E.nu)}i`}`;

function ecGeneral(E: EC): { tex: string; js: string; why: string } {
  if (E.type === "distinct")
    return {
      tex: `y = ${join([`c_1${xq(E.m1)}`, `c_2${xq(E.m2)}`])}`,
      js: `C1*${xqj(E.m1)} + C2*${xqj(E.m2)}`,
      why: `Two distinct real roots: ${m("x^{m_1}")} and ${m("x^{m_2}")} are a basis.`,
    };
  if (E.type === "double") {
    const p = xq(E.m1);
    return {
      tex: p ? `y = (c_1 + c_2\\ln x)${p}` : `y = c_1 + c_2\\ln x`,
      js: `(C1 + C2*log(x))*${xqj(E.m1)}`,
      why: `A double root gives only ${m("x^m")}; reduction of order supplies the second solution ${m("x^m\\ln x")}.`,
    };
  }
  const L = nuLn(E.nu);
  const trig = `c_1\\cos(${L}) + c_2\\sin(${L})`;
  return {
    tex: E.mu ? `y = ${xq(Qi(E.mu))}\\left[${trig}\\right]` : `y = ${trig}`,
    js: `x^(${E.mu})*(C1*cos(${E.nu}*log(x)) + C2*sin(${E.nu}*log(x)))`,
    why: `Complex roots ${m("\\mu \\pm \\nu i")}: ${m("x^{\\mu \\pm \\nu i} = x^\\mu e^{\\pm i\\nu\\ln x}")}, whose real and imaginary parts are ${m("x^\\mu\\cos(\\nu\\ln x)")} and ${m("x^\\mu\\sin(\\nu\\ln x)")}.`,
  };
}

const ecSubst = (E: EC) =>
  `Substitute ${m("y = x^m")}: ${m("x^2y'' = m(m-1)x^m")}, ${m("xy' = mx^m")}, so the auxiliary equation is ${m(`${E.A === 1 ? "" : E.A}m(m-1)${E.B ? ` ${E.B < 0 ? "-" : "+"} ${Math.abs(E.B) === 1 ? "" : Math.abs(E.B)}m` : ""}${E.C ? ` ${E.C < 0 ? "-" : "+"} ${Math.abs(E.C)}` : ""} = 0`)}, i.e. ${m(auxTex(E))}.`;

function ecGeneralDraft(pick: (r: Rng) => EC) {
  return (r: Rng): Draft => {
    const E = pick(r);
    const G = ecGeneral(E);
    return {
      prompt: `Find the general solution of the Euler–Cauchy equation ${m(`${ecTex(E)} = 0`)} for ${m("x > 0")}.`,
      answer: odeN(ecCoef(E), G.js),
      answerTex: G.tex,
      steps: [ecSubst(E), `${m(ecRootsTex(E))}.`, G.why, m(G.tex)],
      meta: { variant: `ec-${E.type}` },
    };
  };
}

function ecIvp(r: Rng): Draft {
  const type = r.pick(["distinct", "double", "complex"] as const);
  const E = type === "distinct" ? ecDistinct(r, false) : type === "double" ? ecDouble(r, false) : ecComplex(r);
  const C1 = r.int(-3, 4), C2 = r.int(-3, 4);
  require_(C1 !== 0 || C2 !== 0);
  let y0: number, v0: number, sol: string, js: string, ic: string;
  if (E.type === "distinct") {
    const p = E.m1.n, q = E.m2.n;
    y0 = C1 + C2;
    v0 = p * C1 + q * C2;
    ic = `${m(`y(1) = c_1 + c_2 = ${y0}`)}, ${m(`y'(1) = ${join([ct(p, "c_1"), ct(q, "c_2")])} = ${v0}`)}, so ${m(`c_1 = ${C1},\\ c_2 = ${C2}`)}`;
    const term = (c: number, e: number) => (c === 0 ? "0" : e === 0 ? `${c}` : ct(c, xq(Qi(e))));
    sol = join([term(C1, p), term(C2, q)]);
    js = `(${C1})*x^(${p}) + (${C2})*x^(${q})`;
  } else if (E.type === "double") {
    const p = E.m1.n, P = xq(Qi(p));
    y0 = C1;
    v0 = p * C1 + C2;
    ic = `${m(`y(1) = c_1 = ${y0}`)} (since ${m("\\ln 1 = 0")}); ${m(`y'(1) = ${join([ct(p, "c_1"), "c_2"])} = ${v0}`)}, so ${m(`c_2 = ${C2}`)}`;
    if (C1 && C2) sol = P ? `\\left(${join([`${C1}`, ct(C2, "\\ln x")])}\\right)${P}` : join([`${C1}`, ct(C2, "\\ln x")]);
    else if (C1) sol = P ? ct(C1, P) : `${C1}`;
    else sol = ct(C2, `${P}\\ln x`);
    js = `((${C1}) + (${C2})*log(x))*x^(${p})`;
  } else {
    const { mu, nu } = E;
    const L = nuLn(nu);
    y0 = C1;
    v0 = mu * C1 + nu * C2;
    ic = `${m(`y(1) = c_1 = ${y0}`)}; ${m(`y'(1) = ${join([ct(mu, "c_1"), ct(nu, "c_2")])} = ${v0}`)}, so ${m(`c_2 = ${C2}`)}`;
    const trig = join([ct(C1, `\\cos(${L})`), ct(C2, `\\sin(${L})`)]);
    sol = mu ? `${xq(Qi(mu))}\\left(${trig}\\right)` : trig;
    js = `x^(${mu})*((${C1})*cos(${nu}*log(x)) + (${C2})*sin(${nu}*log(x)))`;
  }
  const G = ecGeneral(E);
  return {
    prompt: `Solve the initial value problem ${m(`${ecTex(E)} = 0,\\quad y(1) = ${y0},\\ y'(1) = ${v0}`)}.`,
    answer: odeN(ecCoef(E), js, { ic: [1, y0, v0] }),
    answerTex: `y = ${sol}`,
    steps: [ecSubst(E), `${m(ecRootsTex(E))}, so ${m(G.tex)}.`, ic + ".", m(`y = ${sol}`)],
    meta: { variant: `ec-ivp-${E.type}` },
  };
}

function ecRoots(r: Rng): Draft {
  const E = r.chance(0.65) ? ecDistinct(r) : ecDouble(r);
  const ref = E.type === "double" ? [E.m1.value(), E.m1.value()] : [E.m1.value(), E.m2.value()];
  return {
    prompt: `Find the roots ${m("m")} of the auxiliary equation of ${m(`${ecTex(E)} = 0`)}.`,
    answer: { kind: "roots", ref, label: "m" },
    answerTex: ecRootsTex(E),
    steps: [
      ecSubst(E),
      `Factor: ${m(`${E.A === 1 ? "" : E.A}${E.type === "double" ? `${mFactor(E.m1)}^2` : `${mFactor(E.m1)}${mFactor(E.m2)}`} = 0`)}.`,
      `${m(ecRootsTex(E))}.`,
    ],
    meta: { variant: "ec-roots", A: E.A, B: E.B, C: E.C },
  };
}

// ═════════════════════════════════════════════════════════════════════════
// §2.1 reduction of order: y2 = u y1, U = u' = e^{-∫p dx}/y1² (standard form y'' + p y' + q y = 0)
// Every equation here is chosen so that y = x is NOT a solution.
// ═════════════════════════════════════════════════════════════════════════
const redPrompt = (eq: string, y1: string) =>
  `${m(`y_1 = ${y1}`)} is a solution of ${m(`${eq} = 0`)}${eq.includes("x") ? ` (${m("x > 0")})` : ""}. Use reduction of order to find a second solution, then give the general solution.`;
const redFormula = `Reduction of order: ${m("y_2 = uy_1")} with ${m("U = u' = \\dfrac{1}{y_1^2}e^{-\\int p\\,dx}")}, where ${m("p")} is the coefficient of ${m("y'")} in standard form.`;

function redEuler(r: Rng): Draft {
  const E = r.chance(0.6) ? ecDistinct(r, false) : ecDouble(r, false);
  // the given solution: a root that isn't 0 (y1 = 1 would be odd to hand out)
  const given = E.type === "double" ? E.m1.n : r.chance(0.5) ? E.m1.n : E.m2.n;
  const other = E.type === "double" ? given : given === E.m1.n ? E.m2.n : E.m1.n;
  require_(given !== 0);
  const y1 = xq(Qi(given));
  const e = -(2 * given + E.B); // exponent in U
  const G = ecGeneral(E);
  let uStep: string, y2: string, js: string, tex: string;
  if (E.type === "double") {
    uStep = `${m(`U = x^{-1}`)}, so ${m("u = \\ln x")} and ${m(`y_2 = ${y1}\\ln x`)}.`;
    y2 = `${y1}\\ln x`;
    js = G.js;
    tex = G.tex;
  } else {
    const d = other - given;
    uStep = `${m(`U = ${xq(Qi(e)) || "1"}`)}, so ${m(`u = ${qterm(new Q(1, d), xq(Qi(d)))}`)} and ${m(`y_2 = uy_1 \\propto ${xq(Qi(other)) || "1"}`)} (constant factors don't matter).`;
    y2 = xq(Qi(other)) || "1";
    js = `C1*x^(${given}) + C2*x^(${other})`;
    tex = `y = ${join([`c_1${y1}`, `c_2${xq(Qi(other))}`])}`;
  }
  return {
    prompt: redPrompt(ecTex(E), y1),
    answer: odeN(ecCoef(E), js),
    answerTex: tex,
    steps: [
      redFormula,
      `Standard form: divide by ${m("x^2")}: ${m(`p = ${E.B === 0 ? "0" : `${E.B < 0 ? "-" : ""}\\frac{${Math.abs(E.B)}}{x}`}`)}, so ${m(`e^{-\\int p\\,dx} = ${xq(Qi(-E.B)) || "1"}`)}; ${m(`y_1^2 = ${xq(Qi(2 * given))}`)}.`,
      uStep,
      `${m(tex)}  (here ${m(`y_2 = ${y2}`)}).`,
    ],
    meta: { variant: `red-euler-${E.type}`, y1: `x^(${given})` },
  };
}

function redTrigOverX(r: Rng): Draft {
  const k = r.int(1, 3);
  const hyp = r.chance(0.35);
  const K = k * k;
  const eq = `xy'' + 2y' ${hyp ? "-" : "+"} ${one(K)}xy`;
  const coef = ["x", "2", `${hyp ? -K : K}*x`];
  let y1: string, y1j: string, uStep: string, tex: string, js: string;
  if (!hyp) {
    const cosFirst = r.chance(0.5);
    const f1 = cosFirst ? "\\cos" : "\\sin";
    y1 = `\\frac{${f1} ${kx(k)}}{x}`;
    y1j = `${cosFirst ? "cos" : "sin"}(${k}*x)/x`;
    uStep = cosFirst
      ? `${m(`U = \\frac{x^2}{\\cos^2 ${kx(k)}}\\cdot x^{-2} = \\sec^2 ${kx(k)}`)}, so ${m(`u = ${k === 1 ? "" : `\\tfrac{1}{${k}}`}\\tan ${kx(k)}`)} and ${m(`y_2 = uy_1 \\propto \\frac{\\sin ${kx(k)}}{x}`)}.`
      : `${m(`U = \\frac{x^2}{\\sin^2 ${kx(k)}}\\cdot x^{-2} = \\csc^2 ${kx(k)}`)}, so ${m(`u = -${k === 1 ? "" : `\\tfrac{1}{${k}}`}\\cot ${kx(k)}`)} and ${m(`y_2 = uy_1 \\propto \\frac{\\cos ${kx(k)}}{x}`)}.`;
    tex = `y = \\frac{c_1\\cos ${kx(k)} + c_2\\sin ${kx(k)}}{x}`;
    js = `(C1*cos(${k}*x) + C2*sin(${k}*x))/x`;
  } else {
    const s = r.pick([1, -1]);
    y1 = `\\frac{e^{${s < 0 ? "-" : ""}${kx(k)}}}{x}`;
    y1j = `exp(${s * k}*x)/x`;
    uStep = `${m(`U = \\frac{x^2}{e^{${s < 0 ? "-" : ""}${kx(2 * k)}}}\\cdot x^{-2} = e^{${s > 0 ? "-" : ""}${kx(2 * k)}}`)}, so ${m(`u = ${s > 0 ? "-" : ""}\\tfrac{1}{${2 * k}}e^{${s > 0 ? "-" : ""}${kx(2 * k)}}`)} and ${m(`y_2 = uy_1 \\propto \\frac{e^{${s > 0 ? "-" : ""}${kx(k)}}}{x}`)}.`;
    tex = `y = \\frac{c_1e^{${kx(k)}} + c_2e^{-${kx(k)}}}{x}`;
    js = `(C1*exp(${k}*x) + C2*exp(${-k}*x))/x`;
  }
  return {
    prompt: redPrompt(eq, y1),
    answer: odeN(coef, js),
    answerTex: tex,
    steps: [
      redFormula,
      `Divide by ${m("x")}: ${m("p = \\frac{2}{x}")}, so ${m("e^{-\\int p\\,dx} = x^{-2}")}.`,
      uStep,
      m(tex),
      `Check: ${m("u = xy")} turns the equation into ${m(`u'' ${hyp ? "-" : "+"} ${one(K)}u = 0`)}.`,
    ],
    meta: { variant: hyp ? "red-hyp" : "red-trig", y1: y1j },
  };
}

function redExpLinear(r: Rng): Draft {
  const k = r.pick([-3, -2, -1, 1, 2, 3]);
  const eq = join(["xy''", k > 0 ? `-(${kx(k)} + 1)y'` : `(${kx(-k)} - 1)y'`, ct(k, "y")]);
  const lin = `${X(k)} + 1`;
  const tex = `y = c_1${ex(k)} + c_2(${lin})`;
  return {
    prompt: redPrompt(eq, ex(k)),
    answer: odeN(["x", `-(${k}*x + 1)`, `${k}`], `C1*exp(${k}*x) + C2*(${k}*x + 1)`),
    answerTex: tex,
    steps: [
      redFormula,
      `Divide by ${m("x")}: ${m(`p = -\\frac{${lin}}{x} = ${-k} - \\frac{1}{x}`)}, so ${m(`e^{-\\int p\\,dx} = x${ex(k)}`)}.`,
      `${m(`U = \\frac{x${ex(k)}}{${ex(2 * k)}} = x${ex(-k)}`)}; integrating by parts, ${m(`u = -${k * k === 1 ? `(${lin})` : `\\frac{${lin}}{${k * k}}`}${ex(-k)}`)}.`,
      `${m(`y_2 = uy_1 = -${k * k === 1 ? `(${lin})` : `\\frac{${lin}}{${k * k}}`}`)}; drop the constant factor: ${m(`y_2 = ${lin}`)}.`,
      m(tex),
    ],
    meta: { variant: "red-exp", y1: `exp(${k}*x)` },
  };
}

function redGauss(r: Rng): Draft {
  const trig = r.chance(0.5);
  const a = trig ? r.pick([1, 1, 2]) : 1;
  const K = 4 * a * a;
  const eq = `xy'' - y' ${trig ? "+" : "-"} ${K}x^3y`;
  const ax2 = a === 1 ? "x^2" : `${a}x^2`;
  let y1: string, y1j: string, uStep: string, tex: string, js: string;
  if (trig) {
    const cosFirst = r.chance(0.5);
    y1 = `${cosFirst ? "\\cos" : "\\sin"}(${ax2})`;
    y1j = `${cosFirst ? "cos" : "sin"}(${a}*x^2)`;
    uStep = `${m(`U = \\frac{x}{${cosFirst ? "\\cos" : "\\sin"}^2(${ax2})}`)}; substitute ${m(`w = ${ax2}`)}: ${m(`u = ${cosFirst ? "" : "-"}\\tfrac{1}{${2 * a}}${cosFirst ? "\\tan" : "\\cot"}(${ax2})`)}, so ${m(`y_2 \\propto ${cosFirst ? "\\sin" : "\\cos"}(${ax2})`)}.`;
    tex = `y = c_1\\cos(${ax2}) + c_2\\sin(${ax2})`;
    js = `C1*cos(${a}*x^2) + C2*sin(${a}*x^2)`;
  } else {
    const s = r.pick([1, -1]);
    y1 = `e^{${s < 0 ? "-" : ""}x^2}`;
    y1j = `exp(${s}*x^2)`;
    uStep = `${m(`U = xe^{${s > 0 ? "-" : ""}2x^2}`)}, so ${m(`u = ${s > 0 ? "-" : ""}\\tfrac{1}{4}e^{${s > 0 ? "-" : ""}2x^2}`)} and ${m(`y_2 = uy_1 \\propto e^{${s > 0 ? "-" : ""}x^2}`)}.`;
    tex = `y = c_1e^{x^2} + c_2e^{-x^2}`;
    js = `C1*exp(x^2) + C2*exp(-x^2)`;
  }
  return {
    prompt: redPrompt(eq, y1),
    answer: odeN(["x", "-1", `${trig ? K : -K}*x^3`], js),
    answerTex: tex,
    steps: [redFormula, `Divide by ${m("x")}: ${m("p = -\\frac{1}{x}")}, so ${m("e^{-\\int p\\,dx} = x")}.`, uStep, m(tex)],
    meta: { variant: trig ? "red-gauss-trig" : "red-gauss-exp", y1: y1j },
  };
}

function redConst(r: Rng): Draft {
  // a double root k of the characteristic equation; Kreyszig §2.1 Example
  const half = r.chance(0.35);
  const k = half ? new Q(r.pick([-3, -1, 1, 3]), 2) : Qi(r.pick([-3, -2, -1, 1, 2, 3]));
  const a = half ? 4 : 1;
  const b = -2 * k.n * (a / k.d), c = (k.n * k.n * a) / (k.d * k.d);
  const e1 = eQ(k);
  const kj = `(${k.n}/${k.d})`;
  const tex = `y = (c_1 + c_2x)${e1}`;
  return {
    prompt: redPrompt(lhs2(a, b, c), e1),
    answer: ode2(a, b, c, "x", `(C1 + C2*x)*exp(${kj}*x)`),
    answerTex: tex,
    steps: [
      redFormula,
      `Standard form: ${m(`p = ${new Q(b, a).tex()}`)}, so ${m(`e^{-\\int p\\,dx} = ${eQ(k.mul(2))}`)} — exactly ${m("y_1^2")}.`,
      `${m("U = 1")}, so ${m("u = x")} and ${m(`y_2 = x${e1}`)}.`,
      m(tex),
    ],
    meta: { variant: "red-const", y1: `exp(${kj}*x)` },
  };
}

// ═════════════════════════════════════════════════════════════════════════
// §2.8 forced oscillations  m y'' + c y' + k y = F0 cos ωt  (variable t)
// ═════════════════════════════════════════════════════════════════════════
const wt = (w: number) => (w === 1 ? "t" : `${w}t`);

function forcedSteady(r: Rng): Draft {
  const mm = r.pick([1, 1, 2]);
  const w = r.int(1, 3);
  const c = r.int(1, 4);
  const k = r.int(1, 20);
  const P = k - mm * w * w, Qc = c * w;
  const g = gcd(P, Qc);
  const s = r.pick([1, 1, 2]);
  const useCos = r.chance(0.6);
  const A = useCos ? (s * P) / g : (-s * Qc) / g;
  const B = useCos ? (s * Qc) / g : (s * P) / g;
  const F0 = (s * (P * P + Qc * Qc)) / g;
  require_(F0 <= 120);
  const fn = useCos ? "\\cos" : "\\sin";
  const yp = join([ct(A, `\\cos ${wt(w)}`), ct(B, `\\sin ${wt(w)}`)]);
  return {
    prompt: `A damped mass–spring system is driven by ${m(`${F0}${fn} ${wt(w)}`)}: ${m(`${lhs2(mm, c, k)} = ${F0}${fn} ${wt(w)}`)}. Find the steady-state solution ${m("y_p(t)")}.`,
    answer: { kind: "expression", ref: `(${A})*cos(${w}*t) + (${B})*sin(${w}*t)`, vars: ["t"], label: "y_p(t)" },
    answerTex: `y_p = ${yp}`,
    steps: [
      `The transient (homogeneous) part dies out because ${m("c > 0")}; what's left is the response at the driving frequency: try ${m(`y_p = a\\cos ${wt(w)} + b\\sin ${wt(w)}`)}.`,
      `With ${m(`k - m\\omega^2 = ${k} - ${mm * w * w} = ${P}`)} and ${m(`c\\omega = ${Qc}`)}: ${m("\\cos")}: ${m(`${join([ct(P, "a"), ct(Qc, "b")])} = ${useCos ? F0 : 0}`)}; ${m("\\sin")}: ${m(`${join([ct(-Qc, "a"), ct(P, "b")])} = ${useCos ? 0 : F0}`)}.`,
      `${m(`a = ${A},\\ b = ${B}`)}, so ${m(`y_p = ${yp}`)}.`,
    ],
    meta: { variant: "forced-steady", mm, c, k, w, F0, fn: useCos ? "cos" : "sin" },
  };
}

function forcedAmplitude(r: Rng): Draft {
  const [Pa, Qc] = r.pick([[3, 4], [4, 3], [6, 8], [8, 6], [5, 12], [12, 5], [0, 4], [0, 6]] as [number, number][]);
  const w = r.pick([1, 2]);
  require_(Qc % w === 0);
  const c = Qc / w;
  const mm = r.pick([1, 2]);
  const P = Pa * r.pick([1, -1]);
  const k = P + mm * w * w;
  require_(k > 0);
  const R = Math.round(Math.sqrt(P * P + Qc * Qc));
  const amp = r.pick([1, 2, 3]);
  const F0 = amp * R;
  return {
    prompt: `Find the amplitude ${m("C^*")} of the steady-state oscillation of ${m(`${lhs2(mm, c, k)} = ${F0}\\cos ${wt(w)}`)}.`,
    answer: { kind: "expression", ref: `${F0}/sqrt(${P * P + Qc * Qc})`, vars: [], label: "C*" },
    answerTex: `C^* = ${amp}`,
    steps: [
      `Steady state ${m("y_p = a\\cos\\omega t + b\\sin\\omega t")} has amplitude ${m("C^* = \\sqrt{a^2 + b^2} = \\dfrac{F_0}{\\sqrt{(k - m\\omega^2)^2 + c^2\\omega^2}}")}.`,
      `${m(`k - m\\omega^2 = ${k} - ${mm * w * w} = ${P}`)}, ${m(`c\\omega = ${Qc}`)}: ${m(`\\sqrt{${par(P)}^2 + ${Qc}^2} = ${R}`)}.`,
      m(`C^* = \\frac{${F0}}{${R}} = ${amp}`),
    ],
    meta: { variant: "forced-amplitude", mm, c, k, w, F0, fn: "cos" },
  };
}

function forcedResonance(r: Rng): Draft {
  const mm = r.pick([1, 1, 2]);
  const w0 = r.int(1, 4);
  const k = mm * w0 * w0;
  const A = r.pick([1, 2, 3]);
  const F0 = 2 * mm * w0 * A;
  const useCos = r.chance(0.6);
  const ypTex = useCos ? ct(A, `t\\sin ${wt(w0)}`) : ct(-A, `t\\cos ${wt(w0)}`);
  const ypJs = useCos ? `(${A})*t*sin(${w0}*t)` : `(${-A})*t*cos(${w0}*t)`;
  return {
    prompt: `Undamped resonance: find a particular solution of ${m(`${lhs2(mm, 0, k)} = ${F0}${useCos ? "\\cos" : "\\sin"} ${wt(w0)}`)}.`,
    answer: ode2(mm, 0, k, "t", ypJs, { rhs: `${F0}*${useCos ? "cos" : "sin"}(${w0}*t)`, particular: true }),
    answerTex: `y_p = ${ypTex}`,
    steps: [
      `${m(`\\omega_0 = \\sqrt{k/m} = ${w0}`)} equals the driving frequency: ${m(`\\cos ${wt(w0)}`)} and ${m(`\\sin ${wt(w0)}`)} solve the homogeneous equation, so (modification rule) try ${m(`y_p = t(a\\cos ${wt(w0)} + b\\sin ${wt(w0)})`)}.`,
      `Substituting: ${m(`${one(mm)}y_p'' + ${k}y_p = ${2 * mm * w0}(b\\cos ${wt(w0)} - a\\sin ${wt(w0)})`)}.`,
      `${useCos ? m(`${2 * mm * w0}b = ${F0},\\ a = 0`) : m(`-${2 * mm * w0}a = ${F0},\\ b = 0`)}, so ${m(`y_p = ${ypTex}`)} — the amplitude grows like ${m("t")}: resonance.`,
    ],
    meta: { variant: "forced-resonance" },
  };
}

function forcedBeats(r: Rng): Draft {
  const mm = r.pick([1, 1, 2]);
  const w0 = r.int(2, 5), w = r.int(1, 5);
  require_(w !== w0);
  const k = mm * w0 * w0;
  const d = w0 * w0 - w * w;
  const K = Math.sign(d) * r.pick([1, 1, 2, 3]);
  const F0 = mm * d * K;
  require_(F0 > 0 && F0 <= 120);
  const sol = K === 1 ? `\\cos ${wt(w)} - \\cos ${wt(w0)}` : `${K === -1 ? "-" : K}\\left(\\cos ${wt(w)} - \\cos ${wt(w0)}\\right)`;
  return {
    prompt: `An undamped spring starts from rest at equilibrium and is driven off resonance: solve ${m(`${lhs2(mm, 0, k)} = ${F0}\\cos ${wt(w)},\\quad y(0) = 0,\\ y'(0) = 0`)}.`,
    answer: ode2(mm, 0, k, "t", `(${K})*(cos(${w}*t) - cos(${w0}*t))`, { rhs: `${F0}*cos(${w}*t)`, ic: [0, 0, 0] }),
    answerTex: `y = ${sol}`,
    steps: [
      `${m(`\\omega_0 = ${w0} \\ne \\omega = ${w}`)}: try ${m(`y_p = a\\cos ${wt(w)}`)}: ${m(`${one(mm)}(${w0 * w0} - ${w * w})a = ${F0}`)}, so ${m(`a = \\frac{F_0}{m(\\omega_0^2 - \\omega^2)} = ${K}`)}.`,
      `${m(`y = ${join([`A\\cos ${wt(w0)}`, `B\\sin ${wt(w0)}`, ct(K, `\\cos ${wt(w)}`)])}`)}.`,
      `${m(`y(0) = A + ${par(K)} = 0 \\Rightarrow A = ${-K}`)}; ${m(`y'(0) = ${w0}B = 0 \\Rightarrow B = 0`)}.`,
      `${m(`y = ${sol}`)} — the sum of two nearby frequencies: beats, ${m(`y = ${2 * K}\\sin(${qterm(new Q(w0 + w, 2), "t")})\\sin(${qterm(new Q(w0 - w, 2), "t")})`)}.`,
    ],
    meta: { variant: "forced-beats" },
  };
}

function forcedPractical(r: Rng): Draft {
  const mm = r.pick([1, 1, 2]);
  const j = r.int(1, 3);
  const w2 = r.int(1, 12);
  // ω_max² = k/m − c²/(2m²): m = 1, c = 2j → k = w2 + 2j²; m = 2, c = 2j → k = 2·w2 + j²
  const c = 2 * j;
  const k = mm === 1 ? w2 + 2 * j * j : 2 * w2 + j * j;
  require_(c * c < 2 * mm * k);
  const F0 = r.pick([2, 5, 10]);
  const s = Math.round(Math.sqrt(w2));
  const ansTex = s * s === w2 ? `${s}` : `\\sqrt{${w2}}`;
  return {
    prompt: `For ${m(`${lhs2(mm, c, k)} = ${F0}\\cos\\omega t`)}, at what driving frequency ${m("\\omega_{\\max}")} is the steady-state amplitude largest (practical resonance)?`,
    answer: { kind: "expression", ref: `sqrt(${w2})`, vars: [], label: "ω_max" },
    answerTex: `\\omega_{\\max} = ${ansTex}`,
    steps: [
      `${m("C^*(\\omega) = F_0/\\sqrt{D}")} with ${m("D = (k - m\\omega^2)^2 + c^2\\omega^2")}; the amplitude peaks where ${m("D")} is smallest.`,
      `${m("\\frac{dD}{d(\\omega^2)} = -2m(k - m\\omega^2) + c^2 = 0")} gives ${m("\\omega_{\\max}^2 = \\frac{k}{m} - \\frac{c^2}{2m^2}")} (exists since ${m("c^2 < 2mk")}).`,
      `${m(`\\omega_{\\max}^2 = ${new Q(k, mm).tex()} - \\frac{${c * c}}{${2 * mm * mm}} = ${w2}`)}, so ${m(`\\omega_{\\max} = ${ansTex}`)}.`,
    ],
    meta: { variant: "forced-practical", mm, c, k, F0 },
  };
}

// ═════════════════════════════════════════════════════════════════════════
// §2.10 variation of parameters:  y_p = −y1 ∫ y2 r/W dx + y2 ∫ y1 r/W dx
// ═════════════════════════════════════════════════════════════════════════
const vopFormula = `${m("y_p = -y_1\\int\\frac{y_2r}{W}\\,dx + y_2\\int\\frac{y_1r}{W}\\,dx")} (standard form, ${m("r")} the right side).`;

/** double root k:  y'' − 2k y' + k² y = e^{kx} g(x),  y_p = e^{kx} G with G'' = g */
function vopDoubleCore(r: Rng) {
  const k = r.pick([-2, -1, 1, 2, 3]);
  const variant = r.pick(["ln", "xln", "pow", "pow", "sqrt", "atan"] as const);
  const e = ex(k);
  const A = r.pick([1, 2, 3, -1]);
  const frac = (num: number, den: string) => `${num < 0 ? "-" : ""}\\frac{${Math.abs(num) === 1 ? "" : Math.abs(num)}${e}}{${den}}`;
  let rTex: string, rJs: string, yp: string, ypJs: string, ints: string;
  if (variant === "ln") {
    rTex = frac(-A, "x^2");
    rJs = `(${-A})*exp(${k}*x)/x^2`;
    ints = `${m(`\\int\\frac{y_2r}{W}dx = \\int ${ct(-A, "x^{-1}")}\\,dx = ${ct(-A, "\\ln x")}`)}, ${m(`\\int\\frac{y_1r}{W}dx = \\int ${ct(-A, "x^{-2}")}\\,dx = ${ct(A, "x^{-1}")}`)}. So ${m(`y_p = ${ct(A, `${e}\\ln x`)} + ${par(A)}${e}`)}; the last term solves the homogeneous equation — drop it.`;
    yp = ct(A, `${e}\\ln x`);
    ypJs = `(${A})*exp(${k}*x)*log(x)`;
  } else if (variant === "xln") {
    rTex = frac(A, "x");
    rJs = `(${A})*exp(${k}*x)/x`;
    ints = `${m(`\\int\\frac{y_2r}{W}dx = \\int ${A === 1 ? "1" : A === -1 ? "-1" : A}\\,dx = ${ct(A, "x")}`)}, ${m(`\\int\\frac{y_1r}{W}dx = \\int ${ct(A, "x^{-1}")}\\,dx = ${ct(A, "\\ln x")}`)}. So ${m(`y_p = ${ct(-A, `x${e}`)} + ${par(A)}x${e}\\ln x`)}; drop the homogeneous ${m(`x${e}`)} term.`;
    yp = ct(A, `x${e}\\ln x`);
    ypJs = `(${A})*x*exp(${k}*x)*log(x)`;
  } else if (variant === "pow") {
    const p = r.pick([-1, -2, -3]);
    const K = A * p * (p - 1);
    rTex = frac(K, `x^{${2 - p}}`);
    rJs = `(${K})*exp(${k}*x)*x^(${p - 2})`;
    ints = `${m(`\\int\\frac{y_2r}{W}dx = \\int ${ct(K, `x^{${p - 1}}`)}\\,dx = ${qterm(new Q(K, p), `x^{${p}}`)}`)}, ${m(`\\int\\frac{y_1r}{W}dx = \\int ${ct(K, `x^{${p - 2}}`)}\\,dx = ${qterm(new Q(K, p - 1), `x^{${p - 1}}`)}`)}.`;
    yp = ct(A, `x^{${p}}${e}`);
    ypJs = `(${A})*x^(${p})*exp(${k}*x)`;
  } else if (variant === "sqrt") {
    // G = −4j √x, g = j x^{−3/2}
    const jj = r.pick([1, 2, 3]);
    rTex = frac(jj, "x^{3/2}");
    rJs = `(${jj})*exp(${k}*x)*x^(-3/2)`;
    ints = `${m(`\\int\\frac{y_2r}{W}dx = \\int ${ct(jj, "x^{-1/2}")}\\,dx = ${2 * jj}x^{1/2}`)}, ${m(`\\int\\frac{y_1r}{W}dx = \\int ${ct(jj, "x^{-3/2}")}\\,dx = -${2 * jj}x^{-1/2}`)}. So ${m(`y_p = -${2 * jj}x^{1/2}${e} - ${2 * jj}x^{1/2}${e}`)}.`;
    yp = `-${4 * jj}x^{1/2}${e}`;
    ypJs = `(${-4 * jj})*x^(1/2)*exp(${k}*x)`;
  } else {
    rTex = frac(A, "1 + x^2");
    rJs = `(${A})*exp(${k}*x)/(1 + x^2)`;
    ints = `${m(`\\int\\frac{y_2r}{W}dx = \\int\\frac{${A === 1 ? "" : A === -1 ? "-" : A}x}{1 + x^2}dx = ${qterm(new Q(A, 2), "\\ln(1 + x^2)")}`)}, ${m(`\\int\\frac{y_1r}{W}dx = ${ct(A, "\\arctan x")}`)}.`;
    yp = `${A === 1 ? "" : A === -1 ? "-" : A}${e}\\left(x\\arctan x - \\tfrac{1}{2}\\ln(1 + x^2)\\right)`;
    ypJs = `(${A})*exp(${k}*x)*(x*atan(x) - log(1 + x^2)/2)`;
  }
  const b = -2 * k, c = k * k;
  return {
    b, c, k, rTex, rJs, yp, ypJs, variant,
    yh: `(c_1 + c_2x)${e}`,
    yhJs: `(C1 + C2*x)*exp(${k}*x)`,
    steps: [
      `${m(`\\lambda = ${k}`)} is a double root: ${m(`y_1 = ${e},\\ y_2 = x${e}`)}, ${m(`W = y_1y_2' - y_2y_1' = ${ex(2 * k)}`)}.`,
      `${vopFormula} Here ${m(`\\frac{y_1r}{W} = r${ex(-k)}`)} and ${m("\\frac{y_2r}{W} = x\\frac{y_1r}{W}")}.`,
      ints,
    ],
  };
}

function vopDouble(r: Rng): Draft {
  const V = vopDoubleCore(r);
  return {
    prompt: `Use variation of parameters to find a particular solution of ${m(`${lhs2(1, V.b, V.c)} = ${V.rTex}`)} ${m("(x > 0)")}.`,
    answer: ode2(1, V.b, V.c, "x", V.ypJs, { rhs: V.rJs, particular: true }),
    answerTex: `y_p = ${V.yp}`,
    steps: [...V.steps, m(`y_p = ${V.yp}`)],
    meta: { variant: `vop-double-${V.variant}` },
  };
}

function vopTrigCore(r: Rng) {
  const A = r.pick([1, 2, 3, -1]);
  const cot = r.chance(0.5);
  const fn = cot ? "\\cot x" : "\\csc x";
  const rTex = ct(A, fn);
  const rJs = cot ? `(${A})*cos(x)/sin(x)` : `(${A})/sin(x)`;
  const yp = cot
    ? ct(A, "\\sin x\\,\\ln\\left(\\tan\\tfrac{x}{2}\\right)")
    : A === 1
      ? "-x\\cos x + \\sin x\\,\\ln(\\sin x)"
      : `${A}\\left(-x\\cos x + \\sin x\\,\\ln(\\sin x)\\right)`;
  const ypJs = cot ? `(${A})*sin(x)*log(tan(x/2))` : `(${A})*(-x*cos(x) + sin(x)*log(sin(x)))`;
  const ints = cot
    ? `${m(`\\int y_2r\\,dx = \\int ${ct(A, "\\cos x")}\\,dx = ${ct(A, "\\sin x")}`)}; ${m(`\\int y_1r\\,dx = ${A === 1 ? "" : A === -1 ? "-" : A}\\int\\frac{\\cos^2x}{\\sin x}dx = ${A === 1 ? "" : A === -1 ? "-" : A}\\int(\\csc x - \\sin x)\\,dx = ${A === 1 ? "" : A === -1 ? "-" : A}\\left(\\ln\\tan\\tfrac{x}{2} + \\cos x\\right)`)}.`
    : `${m(`\\int y_2r\\,dx = \\int ${A === 1 ? "1" : A === -1 ? "-1" : A}\\,dx = ${ct(A, "x")}`)}; ${m(`\\int y_1r\\,dx = \\int ${ct(A, "\\cot x")}\\,dx = ${ct(A, "\\ln(\\sin x)")}`)}.`;
  return {
    rTex, rJs, yp, ypJs, cot,
    steps: [
      `${m("y_1 = \\cos x,\\ y_2 = \\sin x")}, ${m("W = 1")}. Undetermined coefficients can't handle ${m(fn)} — variation of parameters can. Work on ${m("0 < x < \\pi")}.`,
      vopFormula,
      ints,
      cot ? `${m(`y_p = ${ct(-A, "\\sin x\\cos x")} + ${par(A)}\\sin x\\left(\\ln\\tan\\tfrac{x}{2} + \\cos x\\right)`)}: the ${m("\\sin x\\cos x")} terms cancel.` : `${m(A > 0 ? `y_p = -\\cos x\\cdot ${ct(A, "x")} + \\sin x\\cdot ${ct(A, "\\ln(\\sin x)")}` : `y_p = -\\cos x\\cdot(${ct(A, "x")}) + \\sin x\\cdot(${ct(A, "\\ln(\\sin x)")})`)}.`,
    ],
  };
}

function vopTrig(r: Rng): Draft {
  const V = vopTrigCore(r);
  return {
    prompt: `Use variation of parameters to find a particular solution of ${m(`y'' + y = ${V.rTex}`)} on ${m("0 < x < \\pi")}.`,
    answer: ode2(1, 0, 1, "x", V.ypJs, { rhs: V.rJs, particular: true }),
    answerTex: `y_p = ${V.yp}`,
    steps: [...V.steps, m(`y_p = ${V.yp}`)],
    meta: { variant: V.cot ? "vop-cot" : "vop-csc" },
  };
}

/** Euler–Cauchy with forcing:  x² y'' + B x y' + C y = r(x) */
function vopEuler(r: Rng): Draft {
  const E = ecDistinct(r, false);
  const m1 = E.m1.n, m2 = E.m2.n;
  const resonant = r.chance(0.35);
  const p = resonant ? r.pick([m1, m2]) : r.int(-3, 4);
  require_(resonant || (p !== m1 && p !== m2));
  const Kp = r.pick([1, -1, 2, 3]);
  const coefR = resonant ? Kp * (2 * p + E.B - 1) : Kp * ((p - m1) * (p - m2));
  require_(coefR !== 0 && Math.abs(coefR) <= 60);
  const xp_ = xq(Qi(p));
  const rTex = xp_ ? ct(coefR, xp_) : `${coefR}`;
  const rJs = `(${coefR})*x^(${p})`;
  const yp = resonant ? ct(Kp, `${xp_}\\ln x`) : xp_ ? ct(Kp, xp_) : `${Kp}`;
  const ypJs = resonant ? `(${Kp})*x^(${p})*log(x)` : `(${Kp})*x^(${p})`;
  const c12 = new Q(coefR, m2 - m1);
  const integ = (e: number) => (e === -1 ? qterm(c12, "\\ln x") : qterm(c12.div(e + 1), xq(Qi(e + 1)) || ""));
  const e1 = p - m1 - 1, e2 = p - m2 - 1;
  return {
    prompt: `Use variation of parameters to find a particular solution of ${m(`${ecTex(E)} = ${rTex}`)} ${m("(x > 0)")}.`,
    answer: odeN(ecCoef(E), ypJs, { rhs: rJs, particular: true }),
    answerTex: `y_p = ${yp}`,
    steps: [
      `Homogeneous: ${m(auxTex(E))} gives ${m(`m = ${m1},\\ ${m2}`)}, so ${m(`y_1 = ${xq(Qi(m1)) || "1"},\\ y_2 = ${xq(Qi(m2)) || "1"}`)}, ${m(`W = ${ct(m2 - m1, xq(Qi(m1 + m2 - 1)))}`)}.`,
      `Standard form first — divide by ${m("x^2")}: ${m(`r = ${xq(Qi(p - 2)) ? ct(coefR, xq(Qi(p - 2))) : coefR}`)}. Then ${vopFormula}`,
      `${m(`\\frac{y_2r}{W} = ${qterm(c12, xq(Qi(e1)) || "")}`)}, ${m(`\\int = ${integ(e1)}`)}; ${m(`\\frac{y_1r}{W} = ${qterm(c12, xq(Qi(e2)) || "")}`)}, ${m(`\\int = ${integ(e2)}`)}.`,
      `${m(`y_p = -y_1(${integ(e1)}) + y_2(${integ(e2)})`)}${resonant ? `; drop the multiple of ${m(xp_ || "1")}, which solves the homogeneous equation` : ""}.`,
      m(`y_p = ${yp}`),
    ],
    meta: { variant: resonant ? "vop-euler-resonant" : "vop-euler" },
  };
}

function vopGeneral(r: Rng): Draft {
  if (r.chance(0.5)) {
    const V = vopTrigCore(r);
    const tex = `y = c_1\\cos x + c_2\\sin x ${V.yp.startsWith("-") ? "- " + V.yp.slice(1) : "+ " + V.yp}`;
    return {
      prompt: `Find the general solution of ${m(`y'' + y = ${V.rTex}`)} on ${m("0 < x < \\pi")}.`,
      answer: ode2(1, 0, 1, "x", `C1*cos(x) + C2*sin(x) + ${V.ypJs}`, { rhs: V.rJs }),
      answerTex: tex,
      steps: [...V.steps, `${m(tex)}.`],
      meta: { variant: "vop-general-trig" },
    };
  }
  const V = vopDoubleCore(r);
  const tex = `y = ${V.yh} ${V.yp.startsWith("-") ? "- " + V.yp.slice(1) : "+ " + V.yp}`;
  return {
    prompt: `Find the general solution of ${m(`${lhs2(1, V.b, V.c)} = ${V.rTex}`)} ${m("(x > 0)")}.`,
    answer: ode2(1, V.b, V.c, "x", `${V.yhJs} + ${V.ypJs}`, { rhs: V.rJs }),
    answerTex: tex,
    steps: [...V.steps, `${m(tex)}.`],
    meta: { variant: "vop-general-double" },
  };
}

// ═════════════════════════════════════════════════════════════════════════
// Ch 3: higher-order constant coefficients
// ═════════════════════════════════════════════════════════════════════════
type Factor = { kind: "real"; r: number; mult: number } | { kind: "pair"; al: number; be: number };

function polyMul(a: number[], b: number[]): number[] {
  const out = new Array(a.length + b.length - 1).fill(0);
  a.forEach((x, i) => b.forEach((y, j) => (out[i + j] += x * y)));
  return out;
}
function charCoeffs(fs: Factor[]): number[] {
  let p = [1];
  for (const f of fs) {
    if (f.kind === "real") for (let i = 0; i < f.mult; i++) p = polyMul(p, [1, -f.r]);
    else p = polyMul(p, [1, -2 * f.al, f.al * f.al + f.be * f.be]);
  }
  return p;
}
const DER = ["y", "y'", "y''", "y'''", "y^{(4)}"];
function hiEqTex(cs: number[]) {
  const n = cs.length - 1;
  return join(cs.map((c, i) => ct(c, DER[n - i])));
}
function hiCharTex(cs: number[]) {
  const n = cs.length - 1;
  return join(cs.map((c, i) => (n - i === 0 ? (c ? `${c}` : "0") : ct(c, n - i === 1 ? "\\lambda" : `\\lambda^${n - i}`))));
}
function factorTex(fs: Factor[]): string {
  return fs
    .map((f) => {
      if (f.kind === "pair") return `(${hiCharTex([1, -2 * f.al, f.al * f.al + f.be * f.be])})`;
      const base = f.r === 0 ? "\\lambda" : `(\\lambda ${f.r > 0 ? "-" : "+"} ${Math.abs(f.r)})`;
      return f.mult > 1 ? `${base}^${f.mult}` : base;
    })
    .join("");
}
function basis(fs: Factor[]): { tex: string; js: string }[] {
  const out: { tex: string; js: string }[] = [];
  for (const f of fs) {
    if (f.kind === "real")
      for (let j = 0; j < f.mult; j++) out.push({ tex: `${j === 0 ? "" : j === 1 ? "x" : `x^${j}`}${ex(f.r)}`, js: `x^${j}*exp(${f.r}*x)` });
    else {
      const e = ex(f.al);
      out.push({ tex: `${e}\\cos ${kx(f.be)}`, js: `exp(${f.al}*x)*cos(${f.be}*x)` });
      out.push({ tex: `${e}\\sin ${kx(f.be)}`, js: `exp(${f.al}*x)*sin(${f.be}*x)` });
    }
  }
  return out;
}
const rootsList = (fs: Factor[]) =>
  fs
    .map((f) =>
      f.kind === "real"
        ? `${f.r}${f.mult > 1 ? `\\ (\\text{${f.mult === 2 ? "double" : "triple"}})` : ""}`
        : `${f.al ? `${f.al} \\pm ${one(f.be)}i` : `\\pm ${one(f.be)}i`}`
    )
    .join(",\\ ");
const order = (fs: Factor[]) => fs.reduce((s, f) => s + (f.kind === "real" ? f.mult : 2), 0);
/** y = x would solve the equation iff 0 is a root of multiplicity ≥ 2 */
const okZero = (fs: Factor[]) => fs.every((f) => f.kind !== "real" || f.r !== 0 || f.mult === 1);

function hiGeneralDraft(pick: (r: Rng) => Factor[], variant: string) {
  return (r: Rng): Draft => {
    const fs = pick(r);
    require_(okZero(fs));
    const cs = charCoeffs(fs);
    require_(cs.every((c) => Math.abs(c) <= 60));
    const n = order(fs);
    const B = basis(fs);
    const tex = `y = ${join(B.map((b, i) => `c_${i + 1}${b.tex}`))}`;
    const js = B.map((b, i) => `C${i + 1}*${b.js}`).join(" + ");
    const cn = Array.from({ length: n }, (_, i) => `C${i + 1}`).join(", ");
    return {
      prompt: `Find the general solution of ${m(`${hiEqTex(cs)} = 0`)} (use ${cn}).`,
      answer: odeN(cs.map(String), js),
      answerTex: tex,
      steps: [
        `Characteristic equation: ${m(`${hiCharTex(cs)} = 0`)}.`,
        `Factor (test divisors of the constant term for integer roots): ${m(`${factorTex(fs)} = 0`)}, so ${m(`\\lambda = ${rootsList(fs)}`)}.`,
        `Each simple real root gives ${m("e^{\\lambda x}")}; a root of multiplicity ${m("k")} gives ${m("e^{\\lambda x}, xe^{\\lambda x}, \\dots, x^{k-1}e^{\\lambda x}")}; a pair ${m("\\alpha \\pm \\beta i")} gives ${m("e^{\\alpha x}\\cos\\beta x,\\ e^{\\alpha x}\\sin\\beta x")} — ${n} solutions in all.`,
        m(tex),
      ],
      meta: { variant },
    };
  };
}

function distinctInts(r: Rng, k: number, lo = -3, hi = 3): number[] {
  const out: number[] = [];
  while (out.length < k) {
    const v = r.int(lo, hi);
    if (!out.includes(v)) out.push(v);
  }
  return out.sort((a, b) => a - b);
}
const pickDistinct = (r: Rng): Factor[] => distinctInts(r, r.chance(0.3) ? 4 : 3).map((v) => ({ kind: "real", r: v, mult: 1 }));
function pickRepeated(r: Rng): Factor[] {
  const pat = r.pick(["2+1", "2+1", "3", "2+2", "2+1+1"] as const);
  if (pat === "3") return [{ kind: "real", r: r.pick([-2, -1, 1, 2]), mult: 3 }];
  const [a, b, c] = distinctInts(r, 3);
  if (pat === "2+1") return [{ kind: "real", r: a, mult: 2 }, { kind: "real", r: b, mult: 1 }];
  if (pat === "2+2") return [{ kind: "real", r: a, mult: 2 }, { kind: "real", r: b, mult: 2 }];
  return [{ kind: "real", r: b, mult: 2 }, { kind: "real", r: a, mult: 1 }, { kind: "real", r: c, mult: 1 }];
}
function pickComplex(r: Rng): Factor[] {
  const pat = r.pick(["1+pair", "1+pair", "pair+pair", "2real+pair"] as const);
  const pair = (): Factor => ({ kind: "pair", al: r.pick([-1, 0, 0, 1, 2]), be: r.int(1, 3) });
  if (pat === "1+pair") return [{ kind: "real", r: r.int(-3, 3), mult: 1 }, pair()];
  if (pat === "pair+pair") {
    const a = r.int(1, 3), b = r.int(1, 3);
    require_(a < b);
    return [{ kind: "pair", al: 0, be: a }, { kind: "pair", al: 0, be: b }];
  }
  const a = r.int(1, 3);
  return [{ kind: "real", r: -a, mult: 1 }, { kind: "real", r: a, mult: 1 }, { kind: "pair", al: 0, be: r.int(1, 3) }];
}

function hiRoots(r: Rng): Draft {
  const fs = r.chance(0.5) ? pickDistinct(r) : pickRepeated(r);
  const cs = charCoeffs(fs);
  require_(cs.every((c) => Math.abs(c) <= 60));
  // largest first (the roots kind compares sets; order is irrelevant to the student)
  const roots = fs.flatMap((f) => (f.kind === "real" ? Array(f.mult).fill(f.r) : [])).sort((a, b) => b - a);
  return {
    prompt: `Find the roots of the characteristic equation of ${m(`${hiEqTex(cs)} = 0`)}.`,
    answer: { kind: "roots", ref: roots, label: "λ" },
    answerTex: `\\lambda = ${rootsList(fs)}`,
    steps: [
      `${m("y = e^{\\lambda x}")} gives ${m(`${hiCharTex(cs)} = 0`)}.`,
      `Integer roots divide the constant term ${m(`${cs[cs.length - 1]}`)}; test them (synthetic division) and factor: ${m(`${factorTex(fs)} = 0`)}.`,
      m(`\\lambda = ${rootsList(fs)}`),
    ],
    meta: { variant: "hi-roots", coef: cs },
  };
}

function hiIvp(r: Rng): Draft {
  const rs = distinctInts(r, 3, -2, 3);
  const Cs = [r.int(-2, 3), r.int(-2, 3), r.int(-2, 3)];
  require_(Cs.filter((c) => c !== 0).length >= 2);
  const fs: Factor[] = rs.map((v) => ({ kind: "real", r: v, mult: 1 }));
  const cs = charCoeffs(fs);
  const ic = [0, 1, 2].map((j) => Cs.reduce((s, c, i) => s + c * rs[i] ** j, 0));
  const sol = join(Cs.map((c, i) => (c === 0 ? "0" : rs[i] === 0 ? `${c}` : ct(c, ex(rs[i])))));
  const js = Cs.map((c, i) => `(${c})*exp(${rs[i]}*x)`).join(" + ");
  return {
    prompt: `Solve ${m(`${hiEqTex(cs)} = 0,\\quad y(0) = ${ic[0]},\\ y'(0) = ${ic[1]},\\ y''(0) = ${ic[2]}`)}.`,
    answer: odeN(cs.map(String), js, { ic: [0, ic[0], ic[1], ic[2]] }),
    answerTex: `y = ${sol}`,
    steps: [
      `${m(`${hiCharTex(cs)} = ${factorTex(fs)} = 0`)}: ${m(`\\lambda = ${rs.join(",\\ ")}`)}, so ${m(`y = ${join(rs.map((v, i) => `c_${i + 1}${ex(v)}`))}`)}.`,
      `${m("y^{(j)}(0) = \\sum_i c_i\\lambda_i^{\\,j}")}: ${m(`c_1 + c_2 + c_3 = ${ic[0]}`)}, ${m(`${join(rs.map((v, i) => ct(v, `c_${i + 1}`)))} = ${ic[1]}`)}, ${m(`${join(rs.map((v, i) => ct(v * v, `c_${i + 1}`)))} = ${ic[2]}`)}.`,
      `Solve (a Vandermonde system): ${m(Cs.map((c, i) => `c_${i + 1} = ${c}`).join(",\\ "))}.`,
      m(`y = ${sol}`),
    ],
    meta: { variant: "hi-ivp" },
  };
}

// ═════════════════════════════════════════════════════════════════════════
// Ch 4: y' = Ay, 2×2.  A = P M P⁻¹ with det P = ±1 keeps every entry an integer.
// ═════════════════════════════════════════════════════════════════════════
type M2 = number[][];
const PS: M2[] = [
  [[1, 1], [0, 1]], [[1, 0], [1, 1]], [[2, 1], [1, 1]], [[1, 1], [1, 2]], [[1, 2], [1, 3]], [[3, 1], [2, 1]],
  [[1, -1], [1, 0]], [[2, 3], [1, 2]], [[1, 1], [2, 3]], [[1, 0], [2, 1]], [[1, -1], [0, 1]], [[1, 0], [-1, 1]],
];
const mul = (X: M2, Y: M2) => [0, 1].map((i) => [0, 1].map((j) => X[i][0] * Y[0][j] + X[i][1] * Y[1][j]));
function conj(P: M2, Mx: M2): M2 {
  const d = P[0][0] * P[1][1] - P[0][1] * P[1][0];
  const Pi = [[P[1][1] / d, -P[0][1] / d], [-P[1][0] / d, P[0][0] / d]];
  return mul(mul(P, Mx), Pi);
}
const pmat = (A: M2) => `\\begin{pmatrix} ${A.map((r) => r.join(" & ")).join(" \\\\ ")} \\end{pmatrix}`;
const vec = (v: (number | string)[]) => `\\begin{pmatrix} ${v.join(" \\\\ ")} \\end{pmatrix}`;
const okA = (A: M2, diagOk = false) =>
  A.flat().every((x) => Number.isInteger(x) && Math.abs(x) <= 12) && (diagOk || A[0][1] !== 0 || A[1][0] !== 0);

function realSystem(r: Rng) {
  const P = r.pick(PS);
  const l1 = r.int(-4, 4), l2 = r.int(-4, 4);
  require_(l1 !== l2);
  const A = conj(P, [[l1, 0], [0, l2]]);
  require_(okA(A) && (A[0][0] !== 0 || A[1][0] !== 0));
  return { A, l1, l2, v1: [P[0][0], P[1][0]], v2: [P[0][1], P[1][1]] };
}
const yPrompt = (A: M2) => `${m(`\\mathbf y' = A\\mathbf y,\\quad A = ${pmat(A)}`)}`;
const sysFields = (refs: string[]) =>
  refs.map((ref, i) => ({ label: `y${"₁₂"[i]}(t)`, tex: `y_${i + 1}(t)`, ref, mode: "expr" as const }));
const tr = (A: M2) => A[0][0] + A[1][1];
const det = (A: M2) => A[0][0] * A[1][1] - A[0][1] * A[1][0];
const charSys = (A: M2) => {
  const p = tr(A), q = det(A);
  return `\\lambda^2${p ? ` ${p > 0 ? "-" : "+"} ${Math.abs(p) === 1 ? "" : Math.abs(p)}\\lambda` : ""}${q ? ` ${q > 0 ? "+" : "-"} ${Math.abs(q)}` : ""} = 0`;
};
const eigStep = (A: M2, roots: string) =>
  `${m("\\det(A - \\lambda I) = \\lambda^2 - (\\operatorname{tr}A)\\lambda + \\det A")}: ${m(`\\operatorname{tr}A = ${tr(A)},\\ \\det A = ${det(A)}`)}, so ${m(charSys(A))} and ${m(roots)}.`;

function sysEigen(r: Rng): Draft {
  const S = realSystem(r);
  return {
    prompt: `Find the eigenvalues of the coefficient matrix of ${yPrompt(S.A)}.`,
    answer: { kind: "roots", ref: [S.l1, S.l2], label: "λ" },
    answerTex: `\\lambda = ${Math.min(S.l1, S.l2)},\\ ${Math.max(S.l1, S.l2)}`,
    steps: [
      `Try ${m("\\mathbf y = \\mathbf x e^{\\lambda t}")}: ${m("A\\mathbf x = \\lambda\\mathbf x")}, an eigenvalue problem.`,
      eigStep(S.A, `\\lambda = ${S.l1},\\ ${S.l2}`),
      `Check: they sum to the trace ${m(`${tr(S.A)}`)} and multiply to the determinant ${m(`${det(S.A)}`)}.`,
    ],
    meta: { variant: "sys-eigen", A: S.A },
  };
}

function sysGeneral(r: Rng): Draft {
  const S = realSystem(r);
  const { A, l1, l2, v1, v2 } = S;
  const tex = `\\mathbf y = c_1${vec(v1)}${ex(l1, "t")} + c_2${vec(v2)}${ex(l2, "t")}`;
  const refs = [0, 1].map((i) => `C1*(${v1[i]})*exp(${l1}*t) + C2*(${v2[i]})*exp(${l2}*t)`);
  return {
    prompt: `Find the general solution of ${yPrompt(A)}. Enter ${m("y_1(t)")} and ${m("y_2(t)")} using C1, C2.`,
    answer: { kind: "tuple", fields: sysFields(refs), vars: ["t"], system: { A, v: "t" } },
    answerTex: tex,
    steps: [
      eigStep(A, `\\lambda_1 = ${l1},\\ \\lambda_2 = ${l2}`),
      `Eigenvectors from ${m("(A - \\lambda I)\\mathbf x = \\mathbf 0")}: ${m(`\\lambda_1 = ${l1}:\\ \\mathbf x^{(1)} = ${vec(v1)}`)}; ${m(`\\lambda_2 = ${l2}:\\ \\mathbf x^{(2)} = ${vec(v2)}`)} (any nonzero multiples).`,
      `${m(tex)}, i.e. ${m(`y_1 = ${join([ct(v1[0], `c_1${ex(l1, "t")}`), ct(v2[0], `c_2${ex(l2, "t")}`)])},\\ y_2 = ${join([ct(v1[1], `c_1${ex(l1, "t")}`), ct(v2[1], `c_2${ex(l2, "t")}`)])}`)}.`,
    ],
    meta: { variant: "sys-general", A },
  };
}

function sysIvp(r: Rng): Draft {
  const S = realSystem(r);
  const { A, l1, l2, v1, v2 } = S;
  const C1 = r.int(-3, 3), C2 = r.int(-3, 3);
  require_(C1 !== 0 && C2 !== 0);
  const y0 = [0, 1].map((i) => C1 * v1[i] + C2 * v2[i]);
  const term = (c: number, l: number) => (c === 0 ? "0" : l === 0 ? `${c}` : ct(c, ex(l, "t")));
  const comp = (i: number) => join([term(C1 * v1[i], l1), term(C2 * v2[i], l2)]);
  const refs = [0, 1].map((i) => `(${C1 * v1[i]})*exp(${l1}*t) + (${C2 * v2[i]})*exp(${l2}*t)`);
  const tex = `y_1 = ${comp(0)},\\quad y_2 = ${comp(1)}`;
  return {
    prompt: `Solve ${yPrompt(A)} with ${m(`y_1(0) = ${y0[0]},\\ y_2(0) = ${y0[1]}`)}.`,
    answer: { kind: "tuple", fields: sysFields(refs), vars: ["t"], system: { A, v: "t", ic: [0, y0[0], y0[1]] } },
    answerTex: tex,
    steps: [
      eigStep(A, `\\lambda_1 = ${l1},\\ \\lambda_2 = ${l2}`),
      `Eigenvectors ${m(`${vec(v1)}`)} and ${m(`${vec(v2)}`)}: ${m(`\\mathbf y = c_1${vec(v1)}${ex(l1, "t")} + c_2${vec(v2)}${ex(l2, "t")}`)}.`,
      `${m("t = 0")}: ${m(`c_1${vec(v1)} + c_2${vec(v2)} = ${vec(y0)}`)}, so ${m(`c_1 = ${C1},\\ c_2 = ${C2}`)}.`,
      m(tex),
    ],
    meta: { variant: "sys-ivp", A },
  };
}

/** A = P [[α, β], [−β, α]] P⁻¹: z = e^{αt}(c1 (cos, −sin) + c2 (sin, cos)), y = P z */
function complexSystem(r: Rng) {
  const P = r.pick(PS);
  const al = r.pick([-2, -1, 0, 1, 2]), be = r.int(1, 3);
  const A = conj(P, [[al, be], [-be, al]]);
  require_(okA(A));
  return { A, P, al, be };
}
/** y_i = e^{αt}[(P_i0 c1 + P_i1 c2) cos βt + (P_i0 c2 − P_i1 c1) sin βt]  (mathjs) */
function complexComp(P: M2, al: number, be: number, i: number) {
  const a = P[i][0], b = P[i][1];
  return `exp(${al}*t)*(((${a})*C1 + (${b})*C2)*cos(${be}*t) + ((${a})*C2 - (${b})*C1)*sin(${be}*t))`;
}
/** a + bi, LaTeX */
const cx = (a: number, b: number) => (b === 0 ? `${a}` : a === 0 ? `${ct(b, "i")}` : `${a} ${b < 0 ? "-" : "+"} ${Math.abs(b) === 1 ? "" : Math.abs(b)}i`);

function sysComplex(r: Rng): Draft {
  const { A, P, al, be } = complexSystem(r);
  const refs = [0, 1].map((i) => complexComp(P, al, be, i));
  const e = ex(al, "t");
  const lin = (x: number, y: number, n1: string, n2: string) => {
    const s = join([ct(x, n1), ct(y, n2)]);
    return s.includes(" ") ? `(${s})` : s === "0" ? "" : s;
  };
  const comp = (i: number) => {
    const [a, b] = [P[i][0], P[i][1]];
    const cosC = lin(a, b, "c_1", "c_2"), sinC = lin(-b, a, "c_1", "c_2");
    const inner = join([cosC ? `${cosC}\\cos ${wt(be)}` : "0", sinC ? `${sinC}\\sin ${wt(be)}` : "0"]);
    return e ? `${e}\\left[${inner}\\right]` : inner;
  };
  const tex = `y_1 = ${comp(0)},\\quad y_2 = ${comp(1)}`;
  return {
    prompt: `Find the general (real) solution of ${yPrompt(A)}. Enter ${m("y_1(t)")} and ${m("y_2(t)")} using C1, C2.`,
    answer: { kind: "tuple", fields: sysFields(refs), vars: ["t"], system: { A, v: "t" } },
    answerTex: tex,
    steps: [
      eigStep(A, `\\lambda = ${al ? `${al} \\pm ${one(be)}i` : `\\pm ${one(be)}i`}`),
      `Complex eigenvalues ${m("\\alpha \\pm \\beta i")}: take one complex eigenvector ${m("\\mathbf x")}; the real and imaginary parts of ${m("\\mathbf x e^{(\\alpha + i\\beta)t}")} are two real solutions, each ${e ? `${m(e)} times ` : ""}a combination of ${m(`\\cos ${wt(be)}`)} and ${m(`\\sin ${wt(be)}`)}.`,
      `Here ${m(`\\mathbf x = ${vec([cx(P[0][0], P[0][1]), cx(P[1][0], P[1][1])])}`)} for ${m(`\\lambda = ${cx(al, be)}`)}: the real part of ${m("\\mathbf x e^{\\lambda t}")} goes with ${m("c_1")}, the imaginary part with ${m("c_2")}.`,
      m(tex),
    ],
    meta: { variant: "sys-complex", A },
  };
}

function sysComplexIvp(r: Rng): Draft {
  const { A, P, al, be } = complexSystem(r);
  const c1 = r.int(-2, 3), c2 = r.int(-2, 3);
  require_(c1 !== 0 || c2 !== 0);
  const y0 = [0, 1].map((i) => P[i][0] * c1 + P[i][1] * c2);
  const coefs = [0, 1].map((i) => [P[i][0] * c1 + P[i][1] * c2, P[i][0] * c2 - P[i][1] * c1]);
  const refs = coefs.map(([a, b]) => `exp(${al}*t)*((${a})*cos(${be}*t) + (${b})*sin(${be}*t))`);
  const e = ex(al, "t");
  const comp = (i: number) => {
    const inner = join([ct(coefs[i][0], `\\cos ${wt(be)}`), ct(coefs[i][1], `\\sin ${wt(be)}`)]);
    return e && inner !== "0" ? `${e}\\left(${inner}\\right)` : inner;
  };
  const tex = `y_1 = ${comp(0)},\\quad y_2 = ${comp(1)}`;
  return {
    prompt: `Solve ${yPrompt(A)} with ${m(`y_1(0) = ${y0[0]},\\ y_2(0) = ${y0[1]}`)}.`,
    answer: { kind: "tuple", fields: sysFields(refs), vars: ["t"], system: { A, v: "t", ic: [0, y0[0], y0[1]] } },
    answerTex: tex,
    steps: [
      eigStep(A, `\\lambda = ${al ? `${al} \\pm ${one(be)}i` : `\\pm ${one(be)}i`}`),
      `Each component is ${m(`${e}(a\\cos ${wt(be)} + b\\sin ${wt(be)})`)}. The initial values fix the cosine coefficients: ${m(`a_1 = ${y0[0]},\\ a_2 = ${y0[1]}`)}.`,
      `The sine coefficients come from ${m("\\mathbf y'(0) = A\\mathbf y(0)")}: ${m(`\\mathbf y'(0) = ${vec([A[0][0] * y0[0] + A[0][1] * y0[1], A[1][0] * y0[0] + A[1][1] * y0[1]])}`)}, and ${m(`y_i'(0) = ${al === 0 ? "" : `${al}a_i + `}${one(be)}b_i`)} gives ${m(`b_1 = ${coefs[0][1]},\\ b_2 = ${coefs[1][1]}`)}.`,
      m(tex),
    ],
    meta: { variant: "sys-complex-ivp", A },
  };
}

/** A = P [[λ, 1], [0, λ]] P⁻¹: y = c1 x e^{λt} + c2 (x t + u) e^{λt}, x = P col 0, u = P col 1 */
function sysRepeated(r: Rng): Draft {
  const P = r.pick(PS);
  const l = r.pick([-3, -2, -1, 1, 2, 3]);
  const A = conj(P, [[l, 1], [0, l]]);
  require_(okA(A));
  const xv = [P[0][0], P[1][0]], u = [P[0][1], P[1][1]];
  const e = ex(l, "t");
  const refs = [0, 1].map((i) => `exp(${l}*t)*((${xv[i]})*C1 + (${u[i]})*C2 + (${xv[i]})*C2*t)`);
  const tex = `\\mathbf y = c_1${vec(xv)}${e} + c_2\\left(${vec(xv)}t + ${vec(u)}\\right)${e}`;
  return {
    prompt: `Find the general solution of ${yPrompt(A)}. Enter ${m("y_1(t)")} and ${m("y_2(t)")} using C1, C2.`,
    answer: { kind: "tuple", fields: sysFields(refs), vars: ["t"], system: { A, v: "t" } },
    answerTex: tex,
    steps: [
      eigStep(A, `\\lambda = ${l}\\ (\\text{double})`),
      `${m(`A - ${par(l)}I = ${pmat([[A[0][0] - l, A[0][1]], [A[1][0], A[1][1] - l]])}`)} has rank 1: only one eigenvector ${m(`\\mathbf x = ${vec(xv)}`)}.`,
      `Second solution ${m(`(\\mathbf x t + \\mathbf u)${e}`)} with ${m(`(A - ${par(l)}I)\\mathbf u = \\mathbf x`)}: ${m(`\\mathbf u = ${vec(u)}`)} (any solution; adding a multiple of ${m("\\mathbf x")} is fine).`,
      m(tex),
    ],
    meta: { variant: "sys-repeated", A },
  };
}

// ═════════════════════════════════════════════════════════════════════════
// Ch 4.3–4.4 phase portrait type (Kreyszig Table 4.1 / 4.2)
// ═════════════════════════════════════════════════════════════════════════
export const PHASE_OPTIONS = [
  "Node (asymptotically stable)",
  "Node (unstable)",
  "Saddle point (unstable)",
  "Center (stable, not attractive)",
  "Spiral point (asymptotically stable)",
  "Spiral point (unstable)",
];
const STABILITY_OPTIONS = ["Asymptotically stable", "Stable, not attractive", "Unstable"];
const stabilityOf = (type: number) => (type === 0 || type === 4 ? 0 : type === 3 ? 1 : 2);

/** eigen-structure for a type: real roots (r1, r2) or a complex pair (al, be) */
function phaseRoots(r: Rng, type: number): { k: "real"; r1: number; r2: number } | { k: "cx"; al: number; be: number } {
  if (type === 0 || type === 1) {
    const s = type === 0 ? -1 : 1;
    const a = r.int(1, 4), b = r.int(1, 4);
    return { k: "real", r1: s * a, r2: s * b };
  }
  if (type === 2) return { k: "real", r1: -r.int(1, 4), r2: r.int(1, 4) };
  const be = r.int(1, 3);
  if (type === 3) return { k: "cx", al: 0, be };
  return { k: "cx", al: (type === 4 ? -1 : 1) * r.int(1, 2), be };
}

function phaseMatrix(r: Rng, type: number): M2 {
  const R = phaseRoots(r, type);
  const P = r.pick(PS);
  let A: M2;
  if (R.k === "real") A = conj(P, R.r1 === R.r2 && r.chance(0.5) ? [[R.r1, 1], [0, R.r1]] : [[R.r1, 0], [0, R.r2]]);
  else A = conj(P, [[R.al, R.be], [-R.be, R.al]]);
  require_(okA(A));
  return A;
}

function phaseSteps(A: M2): string[] {
  const p = tr(A), q = det(A), D = p * p - 4 * q;
  return [
    `${m(`p = \\operatorname{tr}A = ${p}`)}, ${m(`q = \\det A = ${q}`)}, ${m(`\\Delta = p^2 - 4q = ${D}`)}.`,
    `Kreyszig's criteria: ${m("q < 0")} saddle; ${m("q > 0,\\ \\Delta \\ge 0")} node; ${m("q > 0,\\ \\Delta < 0")}: center if ${m("p = 0")}, spiral otherwise. Stable and attractive when ${m("p < 0,\\ q > 0")}; a center (${m("p = 0")}) is stable but not attractive.`,
  ];
}
const verdict = (A: M2, label: string) => `Eigenvalues: roots of ${m(charSys(A))}. So: ${label.toLowerCase()}.`;

function phaseFromMatrix(r: Rng): Draft {
  const type = r.int(0, 5);
  const A = phaseMatrix(r, type);
  return {
    prompt: `Classify the critical point ${m("\\mathbf y = \\mathbf 0")} of ${yPrompt(A)} (type and stability).`,
    answer: { kind: "choice", options: PHASE_OPTIONS, correct: PHASE_OPTIONS[type] },
    answerTex: `\\text{${PHASE_OPTIONS[type]}}`,
    steps: [...phaseSteps(A), verdict(A, PHASE_OPTIONS[type])],
    meta: { variant: "phase-matrix", A, type },
  };
}

function phaseFromEquations(r: Rng): Draft {
  const type = r.int(0, 5);
  const A = phaseMatrix(r, type);
  const row = (i: number) => join([ct(A[i][0], "y_1"), ct(A[i][1], "y_2")]);
  return {
    prompt: `Classify the critical point at the origin of ${m(`y_1' = ${row(0)},\\quad y_2' = ${row(1)}`)}.`,
    answer: { kind: "choice", options: PHASE_OPTIONS, correct: PHASE_OPTIONS[type] },
    answerTex: `\\text{${PHASE_OPTIONS[type]}}`,
    steps: [`Read off ${m(`A = ${pmat(A)}`)}.`, ...phaseSteps(A), verdict(A, PHASE_OPTIONS[type])],
    meta: { variant: "phase-equations", A, type },
  };
}

function phaseFromOde2(r: Rng): Draft {
  const type = r.int(0, 5);
  const R = phaseRoots(r, type);
  // y'' + b y' + c y = 0 with characteristic roots R
  const [b, c] = R.k === "real" ? [-(R.r1 + R.r2), R.r1 * R.r2] : [-2 * R.al, R.al * R.al + R.be * R.be];
  const A = [[0, 1], [-c, -b]];
  return {
    prompt: `Write ${m(`${lhs2(1, b, c)} = 0`)} as a system (${m("y_1 = y,\\ y_2 = y'")}) and classify its critical point at the origin.`,
    answer: { kind: "choice", options: PHASE_OPTIONS, correct: PHASE_OPTIONS[type] },
    answerTex: `\\text{${PHASE_OPTIONS[type]}}`,
    steps: [
      `${m(`y_1' = y_2`)}, ${m(`y_2' = ${join([ct(-c, "y_1"), ct(-b, "y_2")])}`)}: ${m(`A = ${pmat(A)}`)}.`,
      ...phaseSteps(A),
      verdict(A, PHASE_OPTIONS[type]),
    ],
    meta: { variant: "phase-ode2", A, type },
  };
}

function phaseStability(r: Rng): Draft {
  const type = r.int(0, 5);
  const A = phaseMatrix(r, type);
  const s = stabilityOf(type);
  return {
    prompt: `Is the critical point ${m("\\mathbf y = \\mathbf 0")} of ${yPrompt(A)} stable?`,
    answer: { kind: "choice", options: STABILITY_OPTIONS, correct: STABILITY_OPTIONS[s] },
    answerTex: `\\text{${STABILITY_OPTIONS[s]}}`,
    steps: [...phaseSteps(A), `It is a ${PHASE_OPTIONS[type].toLowerCase()}.`],
    meta: { variant: "phase-stability", A, type, stability: s },
  };
}

export const ODE2_SYS_TEMPLATES: Record<string, (r: Rng) => Draft> = {
  "red-euler": redEuler,
  "red-trig": redTrigOverX,
  "red-exp": redExpLinear,
  "red-gauss": redGauss,
  "red-const": redConst,
  "ec-distinct": ecGeneralDraft((r) => ecDistinct(r)),
  "ec-double": ecGeneralDraft((r) => ecDouble(r)),
  "ec-complex": ecGeneralDraft(ecComplex),
  "ec-ivp": ecIvp,
  "ec-roots": ecRoots,
  "forced-steady": forcedSteady,
  "forced-amplitude": forcedAmplitude,
  "forced-resonance": forcedResonance,
  "forced-beats": forcedBeats,
  "forced-practical": forcedPractical,
  "vop-double": vopDouble,
  "vop-trig": vopTrig,
  "vop-euler": vopEuler,
  "vop-general": vopGeneral,
  "hi-distinct": hiGeneralDraft(pickDistinct, "hi-distinct"),
  "hi-repeated": hiGeneralDraft(pickRepeated, "hi-repeated"),
  "hi-complex": hiGeneralDraft(pickComplex, "hi-complex"),
  "hi-roots": hiRoots,
  "hi-ivp": hiIvp,
  "sys-eigen": sysEigen,
  "sys-general": sysGeneral,
  "sys-ivp": sysIvp,
  "sys-complex": sysComplex,
  "sys-complex-ivp": sysComplexIvp,
  "sys-repeated": sysRepeated,
  "phase-matrix": phaseFromMatrix,
  "phase-equations": phaseFromEquations,
  "phase-ode2": phaseFromOde2,
  "phase-stability": phaseStability,
};
