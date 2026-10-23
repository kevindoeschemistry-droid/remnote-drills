// Kuta-style Level 1 ODE problem generators.
//
// Every problem is built BACKWARD from a clean answer (pick the solution, then
// derive the equation), so numbers stay small and integer. Each generator emits
// the LaTeX for display and the mathjs form for the checker side by side.
// tests/ verifies every reference answer against its ODE (JS + independent sympy).

import { Rng } from "./rng";
import type { Draft, SkillId } from "./types";
import { ct, ex, frac, join, signed, xp, m } from "./tex";
import { require_ } from "./reject";

type OdeProblem = Draft;
type WronskianProblem = Draft;

// ── extra LaTeX helpers ─────────────────────────────────────────────────────
/** (n/d) * body with the fraction reduced */
function ctf(n: number, d: number, body: string): string {
  if (d < 0) {
    n = -n;
    d = -d;
  }
  const g = gcdi(n, d);
  n /= g;
  d /= g;
  if (d === 1) return ct(n, body);
  if (n < 0) return `-\\frac{${-n}}{${d}}${body}`;
  return `\\frac{${n}}{${d}}${body}`;
}
function gcdi(a: number, b: number): number {
  a = Math.abs(a);
  b = Math.abs(b);
  while (b) [a, b] = [b, a % b];
  return a || 1;
}
/** k * x^p, using \frac for negative powers */
function xpow(k: number, p: number): string {
  if (p >= 0) return ct(k, xp(p));
  const den = xp(-p);
  if (k < 0) return `-\\frac{${-k}}{${den}}`;
  return `\\frac{${k}}{${den}}`;
}
/** k * body / x */
function fracx(k: number, body: string): string {
  const num = Math.abs(k) === 1 ? body || "1" : `${Math.abs(k)}${body}`;
  return `${k < 0 ? "-" : ""}\\frac{${num}}{x}`;
}
/** t (inner) tail  ->  3\left(x - 1\right)e^{x} */
function ctParen(t: number, inner: string, tail: string): string {
  const lead = t === 1 ? "" : t === -1 ? "-" : `${t}`;
  return `${lead}\\left(${inner}\\right)${tail}`;
}
/** C*body, or the numeric constant times body */
function cterm(c: number | null, body: string): string {
  return c === null ? `C${body}` : ct(c, body);
}
const cjs = (c: number | null) => (c === null ? "C" : `(${c})`);
/** append " - 3x" style tail terms to an expression */
function tail(terms: string[]): string {
  return terms
    .filter((s) => s && s !== "0")
    .map((s) => (s.startsWith("-") ? ` - ${s.slice(1)}` : ` + ${s}`))
    .join("");
}
const trigArg = (k: number) => (k === 1 ? "x" : `${k}x`);

function ode(
  _skill: SkillId,
  template: string,
  eq: string,
  rhs: string,
  answer: string,
  answerTex: string,
  steps: string[],
  ic?: [number, number],
  icTex?: string
): Draft {
  const prompt = ic
    ? `Solve the initial value problem ${m(`${eq},\\quad ${icTex ?? `y(${ic[0]}) = ${ic[1]}`}`)}`
    : `Find the general solution of ${m(eq)}`;
  return { prompt, answer: { kind: "ode", rhs, ic, ref: answer }, answerTex, steps, meta: { variant: template } };
}

const DYDX = "\\frac{dy}{dx} = ";

// ═══════════════════════════════════════════════════════════════════════════
// 1. Separable
// ═══════════════════════════════════════════════════════════════════════════
function sepExpGrowth(r: Rng): OdeProblem {
  // y' = k x^n (y - b)  ->  y = b + (y0 - b) e^{m x^{n+1}}
  const n = r.pick([0, 1, 1, 2, 3]);
  const mm = r.nz(-3, 3);
  const k = mm * (n + 1);
  const b = r.pick([0, 0, 0, 1, 2, -1, 3]);
  const y0 = r.nz(-4, 5, [0, b]);
  const ybar = b === 0 ? "y" : `y${signed(-b)}`;
  const yfac = b === 0 ? "y" : `\\left(${ybar}\\right)`;
  const eq = DYDX + ct(k, xp(n) + yfac);
  const expo = ct(mm, xp(n + 1));
  const solTex = join([ct(y0 - b, `e^{${expo}}`), b === 0 ? "" : `${b}`]);
  return ode(
    "separable",
    "exp-growth",
    eq,
    `(${k})*x^(${n})*(y - (${b}))`,
    `y = (${b}) + (${y0 - b})*exp((${mm})*x^(${n + 1}))`,
    `y = ${solTex}`,
    [
      `Separate: ${m(`\\frac{dy}{${ybar}} = ${ct(k, xp(n))}\\,dx`)}`,
      `Integrate: ${m(`\\ln|${ybar}| = ${expo} + C`)}`,
      `Exponentiate: ${m(`${ybar} = Ce^{${expo}}`)}`,
      `Apply ${m(`y(0) = ${y0}`)}: ${m(`C = ${y0 - b}`)}`,
      m(`y = ${solTex}`),
    ],
    [0, y0]
  );
}

function sepOverY(r: Rng): OdeProblem {
  // y' = a x^n / y  ->  y = sqrt(c x^{n+1} + y0^2)
  const n = r.pick([0, 1, 2, 3]);
  const c = r.pick([1, 2, 3, 4, 6]);
  require_((c * (n + 1)) % 2 === 0);
  const a = (c * (n + 1)) / 2;
  const y0 = r.int(1, 5);
  const inside = `${ct(c, xp(n + 1))} + ${y0 * y0}`;
  return ode(
    "separable",
    "over-y",
    DYDX + `\\frac{${ct(a, xp(n))}}{y}`,
    `(${a})*x^(${n})/y`,
    `y = sqrt((${c})*x^(${n + 1}) + ${y0 * y0})`,
    `y = \\sqrt{${inside}}`,
    [
      `Separate: ${m(`y\\,dy = ${ct(a, xp(n))}\\,dx`)}`,
      `Integrate: ${m(`\\frac{y^2}{2} = ${ctf(c, 2, xp(n + 1))} + C`)}`,
      `Multiply by 2: ${m(`y^2 = ${ct(c, xp(n + 1))} + C`)}`,
      `Apply ${m(`y(0) = ${y0}`)}: ${m(`C = ${y0 * y0}`)}; take the positive root since ${m(`y(0) > 0`)}`,
      m(`y = \\sqrt{${inside}}`),
    ],
    [0, y0]
  );
}

function sepYSquared(r: Rng): OdeProblem {
  // y' = a x^n y^2,  y(0) = 1/c0  ->  y = 1/(c0 - m x^{n+1})
  const n = r.pick([0, 1, 2]);
  const mm = r.nz(-3, 3);
  const a = mm * (n + 1);
  const c0 = r.pick([1, -1, 2, -2, 3]);
  const den = join([`${c0}`, ct(-mm, xp(n + 1))]);
  const y0Tex = frac(1, c0);
  return ode(
    "separable",
    "y-squared",
    DYDX + ct(a, xp(n) + "y^{2}"),
    `(${a})*x^(${n})*y^2`,
    `y = 1/((${c0}) - (${mm})*x^(${n + 1}))`,
    `y = \\frac{1}{${den}}`,
    [
      `Separate: ${m(`\\frac{dy}{y^2} = ${ct(a, xp(n))}\\,dx`)}`,
      `Integrate: ${m(`-\\frac{1}{y} = ${ct(mm, xp(n + 1))} + C`)}`,
      `Apply ${m(`y(0) = ${y0Tex}`)}: ${m(`-${c0 < 0 ? `(${c0})` : c0} = C`)}, so ${m(`C = ${-c0}`)}`,
      `Solve for ${m("y")}: ${m(`y = \\frac{1}{${den}}`)}`,
    ],
    [0, 1 / c0],
    `y(0) = ${y0Tex}`
  );
}

function sepExpSplit(r: Rng): OdeProblem {
  // y' = e^{ax - y}  ->  e^y = e^{ax}/a + C
  const a = r.pick([1, 2, 3, -1]);
  const ea = ex(a);
  const lhsInt = ctf(1, a, ea);
  const eq = DYDX + `e^{${join([ct(a, "x"), "-y"])}}`;
  const rhs = `exp((${a})*x - y)`;
  const steps = [
    `Split: ${m(`\\frac{dy}{dx} = ${ea}\\,e^{-y}`)}`,
    `Separate: ${m(`e^{y}\\,dy = ${ea}\\,dx`)}`,
    `Integrate: ${m(`e^{y} = ${lhsInt} + C`)}`,
  ];
  if (r.chance(0.6)) {
    // y(0) = 0  ->  C = 1 - 1/a
    const cTex = frac(a - 1, a);
    const sol = a === 1 ? "x" : `\\ln\\left(${join([lhsInt, cTex])}\\right)`;
    steps.push(`Apply ${m("y(0) = 0")}: ${m(`1 = ${frac(1, a)} + C`)}, so ${m(`C = ${cTex}`)}`);
    steps.push(m(`y = ${sol}`));
    return ode(
      "separable",
      "exp-split",
      eq,
      rhs,
      `y = log((1/${a})*exp((${a})*x) + (${a - 1})/(${a}))`,
      `y = ${sol}`,
      steps,
      [0, 0]
    );
  }
  const sol = `\\ln\\left(${lhsInt} + C\\right)`;
  steps.push(m(`y = ${sol}`));
  return ode("separable", "exp-split", eq, rhs, `y = log((1/${a})*exp((${a})*x) + C)`, `y = ${sol}`, steps);
}

function sepOverY2(r: Rng): OdeProblem {
  // y' = a x^n / y^2  ->  y^3 = c x^{n+1} + C
  const n = r.pick([0, 1, 2]);
  const c = r.pick([1, 2, 3, 6]);
  require_((c * (n + 1)) % 3 === 0);
  const a = (c * (n + 1)) / 3;
  const inside = `${ct(c, xp(n + 1))} + C`;
  return ode(
    "separable",
    "over-y2",
    DYDX + `\\frac{${ct(a, xp(n))}}{y^{2}}`,
    `(${a})*x^(${n})/y^2`,
    `y^3 = (${c})*x^(${n + 1}) + C`,
    `y = \\sqrt[3]{${inside}}`,
    [
      `Separate: ${m(`y^{2}\\,dy = ${ct(a, xp(n))}\\,dx`)}`,
      `Integrate: ${m(`\\frac{y^3}{3} = ${ctf(c, 3, xp(n + 1))} + C`)}`,
      `Multiply by 3 (absorb into ${m("C")}): ${m(`y^3 = ${inside}`)}`,
      m(`y = \\sqrt[3]{${inside}}`),
    ]
  );
}

// ═══════════════════════════════════════════════════════════════════════════
// 2. Separable via substitution
// ═══════════════════════════════════════════════════════════════════════════
const U_INTRO = `Homogeneous: let ${m("u = y/x")}, so ${m("y = ux")} and ${m("y' = u + xu'")}`;

function subRatio(r: Rng): OdeProblem {
  // y' = y/x + a x/y  ->  y^2 = x^2 (2a ln|x| + C)
  const a = r.nz(-3, 4);
  const sg = a > 0 ? "+" : "-";
  const A = Math.abs(a);
  const solTex = `y^2 = x^2\\left(${ct(2 * a, "\\ln|x|")} + C\\right)`;
  return ode(
    "substitution",
    "ratio",
    DYDX + `\\frac{y}{x} ${sg} \\frac{${ct(A, "x")}}{y}`,
    `y/x + (${a})*x/y`,
    `y^2 = x^2*((${2 * a})*log(abs(x)) + C)`,
    solTex,
    [
      U_INTRO,
      `Substitute: ${m(`u + xu' = u ${sg} \\frac{${A}}{u}`)}, so ${m(`xu' = ${a < 0 ? "-" : ""}\\frac{${A}}{u}`)}`,
      `Separate: ${m(`u\\,du = ${ct(a, "\\frac{dx}{x}")}`)}`,
      `Integrate: ${m(`\\frac{u^2}{2} = ${ct(a, "\\ln|x|")} + C`)}`,
      `Back-substitute ${m("u = y/x")}: ${m(solTex)}`,
    ]
  );
}

function subSquare(r: Rng): OdeProblem {
  // y' = y/x + a y^2/x^2  ->  y = -x/(a ln|x| + C)
  const a = r.pick([1, 2, 3, -1, -2]);
  const sg = a > 0 ? "+" : "-";
  const solTex = `y = -\\frac{x}{${ct(a, "\\ln|x|")} + C}`;
  return ode(
    "substitution",
    "square",
    DYDX + `\\frac{y}{x} ${sg} \\frac{${ct(Math.abs(a), "y^{2}")}}{x^{2}}`,
    `y/x + (${a})*y^2/x^2`,
    `y = -x/((${a})*log(abs(x)) + C)`,
    solTex,
    [
      U_INTRO,
      `Substitute: ${m(`xu' = ${ct(a, "u^{2}")}`)}`,
      `Separate: ${m(`\\frac{du}{u^{2}} = ${ct(a, "\\frac{dx}{x}")}`)}`,
      `Integrate: ${m(`-\\frac{1}{u} = ${ct(a, "\\ln|x|")} + C`)}`,
      `Back-substitute ${m("u = y/x")}: ${m(solTex)}`,
    ]
  );
}

function subExp(r: Rng): OdeProblem {
  // y' = y/x + a e^{-y/x}  ->  y = x ln(a ln|x| + C)
  const a = r.pick([1, 2, 3]);
  const solTex = `y = x\\ln\\left(${ct(a, "\\ln|x|")} + C\\right)`;
  return ode(
    "substitution",
    "exp",
    DYDX + `\\frac{y}{x} + ${ct(a, "e^{-y/x}")}`,
    `y/x + (${a})*exp(-y/x)`,
    `y = x*log((${a})*log(abs(x)) + C)`,
    solTex,
    [
      U_INTRO,
      `Substitute: ${m(`xu' = ${ct(a, "e^{-u}")}`)}`,
      `Separate: ${m(`e^{u}\\,du = ${ct(a, "\\frac{dx}{x}")}`)}`,
      `Integrate: ${m(`e^{u} = ${ct(a, "\\ln|x|")} + C`)}`,
      `Take ${m("\\ln")}, back-substitute: ${m(solTex)}`,
    ]
  );
}

function subLinearSquare(r: Rng): OdeProblem {
  // y' = (y + ax + b)^2 - a,  v = y + ax + b  ->  v' = v^2
  const a = r.nz(-3, 3);
  const b = r.int(-4, 4);
  const vt = join(["y", ct(a, "x"), b ? `${b}` : ""]);
  const solTex = `y = -\\frac{1}{x + C}${tail([ct(-a, "x"), `${-b}`])}`;
  return ode(
    "substitution",
    "linear-square",
    DYDX + `\\left(${vt}\\right)^{2}${signed(-a)}`,
    `(y + (${a})*x + (${b}))^2 - (${a})`,
    `y = -1/(x + C) - (${a})*x - (${b})`,
    solTex,
    [
      `Let ${m(`v = ${vt}`)}, so ${m(`v' = y'${signed(a)}`)}`,
      `Substitute: ${m("v' = v^{2}")}`,
      `Separate and integrate: ${m("\\frac{dv}{v^2} = dx \\Rightarrow -\\frac{1}{v} = x + C")}`,
      `Back-substitute: ${m(solTex)}`,
    ]
  );
}

function subArctan(r: Rng): OdeProblem {
  // y' = (x + y + b)^2,  v = x + y + b  ->  v' = 1 + v^2
  const b = r.int(-4, 4);
  const vt = join(["x", "y", b ? `${b}` : ""]);
  const solTex = `y = \\tan(x + C) - x${signed(-b)}`;
  return ode(
    "substitution",
    "arctan",
    DYDX + `\\left(${vt}\\right)^{2}`,
    `(x + y + (${b}))^2`,
    `y = tan(x + C) - x - (${b})`,
    solTex,
    [
      `Let ${m(`v = ${vt}`)}, so ${m("v' = 1 + y'")}`,
      `Substitute: ${m("v' = 1 + v^{2}")}`,
      `Separate: ${m("\\frac{dv}{1 + v^{2}} = dx \\Rightarrow \\arctan v = x + C")}`,
      `Back-substitute: ${m(solTex)}`,
    ]
  );
}

// ═══════════════════════════════════════════════════════════════════════════
// 3 & 4. Linear first order:  y' + P(x) y = Q(x)
// ═══════════════════════════════════════════════════════════════════════════
interface Linear {
  template: string;
  Pterm: string; // LaTeX of the P(x)·y term, with its sign
  Pint: string; // LaTeX of P(x) inside ∫
  mu: string;
  Q: string;
  muQ: string;
  integral: string;
  rhs: string; // y' = Q - P y  (mathjs)
  gen: (c: number | null) => string; // LaTeX of y with C or a number
  genJs: (c: number | null) => string; // mathjs of y
  x0?: number; // allowed IC point
  partAt0?: number; // particular part of gen at x0 (homogeneous part is 1 there)
  note?: string; // integration-by-parts line
}

function linExp(r: Rng): Linear {
  const a = r.nz(-3, 4);
  const c = r.nz(-3, 3, [0, -a]);
  const k = r.nz(-3, 3);
  const b = k * (a + c);
  return {
    template: "exp",
    Pterm: ct(a, "y"),
    Pint: `${a}`,
    mu: ex(a),
    Q: ct(b, ex(c)),
    muQ: ct(b, ex(a + c)),
    integral: ct(k, ex(a + c)),
    rhs: `(${b})*exp((${c})*x) - (${a})*y`,
    gen: (C) => join([ct(k, ex(c)), cterm(C, ex(-a))]),
    genJs: (C) => `(${k})*exp((${c})*x) + ${cjs(C)}*exp((${-a})*x)`,
    x0: 0,
    partAt0: k,
  };
}

function linConst(r: Rng): Linear {
  const a = r.nz(-4, 4);
  const k = r.nz(-5, 5);
  return {
    template: "const",
    Pterm: ct(a, "y"),
    Pint: `${a}`,
    mu: ex(a),
    Q: `${k * a}`,
    muQ: ct(k * a, ex(a)),
    integral: ct(k, ex(a)),
    rhs: `(${k * a}) - (${a})*y`,
    gen: (C) => join([`${k}`, cterm(C, ex(-a))]),
    genJs: (C) => `(${k}) + ${cjs(C)}*exp((${-a})*x)`,
    x0: 0,
    partAt0: k,
  };
}

function linPower(r: Rng): Linear {
  const n = r.pick([1, 2, 3, -1, -2]);
  const mm = r.pick([0, 1, 2, 3]);
  require_(mm + n + 1 !== 0);
  const j = r.nz(-3, 3);
  const k = j * (mm + n + 1);
  const Pterm = n > 0 ? `\\frac{${n}}{x}y` : `-\\frac{${-n}}{x}y`;
  const mu = n > 0 ? xp(n) : `\\frac{1}{${xp(-n)}}`;
  const homC = (C: number | null) =>
    C === null ? (n > 0 ? `\\frac{C}{${xp(n)}}` : `C${xp(-n)}`) : xpow(C, -n);
  return {
    template: "power",
    Pterm,
    Pint: `\\frac{${n}}{x}`,
    mu,
    Q: xpow(k, mm),
    muQ: xpow(k, mm + n),
    integral: xpow(j, mm + n + 1),
    rhs: `(${k})*x^(${mm}) - (${n})*y/x`,
    gen: (C) => join([xpow(j, mm + 1), homC(C)]),
    genJs: (C) => `(${j})*x^(${mm + 1}) + ${cjs(C)}*x^(${-n})`,
    x0: 1,
    partAt0: j,
  };
}

function linGauss(r: Rng): Linear {
  const a = r.pick([1, 2, 3, -1]);
  const j = r.nz(-3, 3);
  const b = 2 * a * j;
  const eax2 = `e^{${ct(a, "x^{2}")}}`;
  return {
    template: "gauss",
    Pterm: ct(2 * a, "xy"),
    Pint: ct(2 * a, "x"),
    mu: eax2,
    Q: ct(b, "x"),
    muQ: ct(b, `x${eax2}`),
    integral: ct(j, eax2),
    rhs: `(${b})*x - (${2 * a})*x*y`,
    gen: (C) => join([`${j}`, cterm(C, `e^{${ct(-a, "x^{2}")}}`)]),
    genJs: (C) => `(${j}) + ${cjs(C)}*exp((${-a})*x^2)`,
    x0: 0,
    partAt0: j,
  };
}

function linTrig(r: Rng): Linear {
  const k = r.nz(-4, 4);
  return {
    template: "trig",
    Pterm: "(\\tan x)y",
    Pint: "\\tan x",
    mu: "\\sec x",
    Q: ct(k, "\\cos x"),
    muQ: `${k}`,
    integral: ct(k, "x"),
    rhs: `(${k})*cos(x) - tan(x)*y`,
    gen: (C) => `\\left(${join([ct(k, "x"), C === null ? "C" : `${C}`])}\\right)\\cos x`,
    genJs: (C) => `((${k})*x + ${cjs(C)})*cos(x)`,
    x0: 0,
    partAt0: 0,
  };
}

function linResonant(r: Rng): Linear {
  const a = r.nz(-3, 3);
  const b = r.nz(-5, 5);
  return {
    template: "resonant",
    Pterm: ct(a, "y"),
    Pint: `${a}`,
    mu: ex(a),
    Q: ct(b, ex(-a)),
    muQ: `${b}`,
    integral: ct(b, "x"),
    rhs: `(${b})*exp((${-a})*x) - (${a})*y`,
    gen: (C) => `\\left(${join([ct(b, "x"), C === null ? "C" : `${C}`])}\\right)${ex(-a)}`,
    genJs: (C) => `((${b})*x + ${cjs(C)})*exp((${-a})*x)`,
    x0: 0,
    partAt0: 0,
  };
}

// ── integrating factor + integration by parts ───────────────────────────────
function ibpPoly(r: Rng): Linear {
  const a = r.pick([1, 2, -1, -2, 3]);
  const j = r.nz(-3, 3);
  const b = j * a * a;
  const muQ = ct(b, `x${ex(a)}`);
  const integral = `\\left(${join([ct(j * a, "x"), `${-j}`])}\\right)${ex(a)}`;
  return {
    template: "poly",
    Pterm: ct(a, "y"),
    Pint: `${a}`,
    mu: ex(a),
    Q: ct(b, "x"),
    muQ,
    integral,
    note: `By parts (${m(`u = x,\\ dv = ${ex(a)}\\,dx`)}): ${m(`\\int ${muQ}\\,dx = ${integral}`)}`,
    rhs: `(${b})*x - (${a})*y`,
    gen: (C) => join([ct(j * a, "x"), `${-j}`, cterm(C, ex(-a))]),
    genJs: (C) => `(${j * a})*x - (${j}) + ${cjs(C)}*exp((${-a})*x)`,
    x0: 0,
    partAt0: -j,
  };
}

function ibpOverXTrig(r: Rng): Linear {
  const k = r.nz(-3, 4);
  const isCos = r.chance(0.5);
  const fT = isCos ? "\\cos x" : "\\sin x";
  const muQ = ct(k, `x${fT}`);
  const integral = isCos
    ? join([ct(k, "x\\sin x"), ct(k, "\\cos x")])
    : join([ct(k, "\\sin x"), ct(-k, "x\\cos x")]);
  const Cx = (C: number | null) => (C === null ? "\\frac{C}{x}" : fracx(C, ""));
  return {
    template: isCos ? "over-x-cos" : "over-x-sin",
    Pterm: "\\frac{1}{x}y",
    Pint: "\\frac{1}{x}",
    mu: "x",
    Q: ct(k, fT),
    muQ,
    integral,
    note: `By parts (${m(`u = x,\\ dv = ${fT}\\,dx`)}): ${m(`\\int ${muQ}\\,dx = ${integral}`)}`,
    rhs: isCos ? `(${k})*cos(x) - y/x` : `(${k})*sin(x) - y/x`,
    gen: (C) =>
      isCos
        ? join([ct(k, "\\sin x"), fracx(k, "\\cos x"), Cx(C)])
        : join([fracx(k, "\\sin x"), ct(-k, "\\cos x"), Cx(C)]),
    genJs: (C) =>
      isCos
        ? `(${k})*sin(x) + (${k})*cos(x)/x + ${cjs(C)}/x`
        : `(${k})*sin(x)/x - (${k})*cos(x) + ${cjs(C)}/x`,
  };
}

function ibpOverXExp(r: Rng): Linear {
  const c = r.pick([1, 2, -1]);
  const t = r.nz(-3, 3);
  const k = t * c * c;
  const muQ = ct(k, `x${ex(c)}`);
  const integral = ctParen(t, join([ct(c, "x"), "-1"]), ex(c));
  return {
    template: "over-x-exp",
    Pterm: "\\frac{1}{x}y",
    Pint: "\\frac{1}{x}",
    mu: "x",
    Q: ct(k, ex(c)),
    muQ,
    integral,
    note: `By parts (${m(`u = x,\\ dv = ${ex(c)}\\,dx`)}): ${m(`\\int ${muQ}\\,dx = ${integral}`)}`,
    rhs: `(${k})*exp((${c})*x) - y/x`,
    gen: (C) => join([ct(t * c, ex(c)), fracx(-t, ex(c)), C === null ? "\\frac{C}{x}" : fracx(C, "")]),
    genJs: (C) => `(${t * c})*exp((${c})*x) - (${t})*exp((${c})*x)/x + ${cjs(C)}/x`,
  };
}

function ibpXExp(r: Rng): Linear {
  const a = r.nz(-2, 2);
  const s = r.pick([1, -1, 2, -2]);
  const c = s - a;
  require_(c !== 0);
  const t = r.nz(-2, 2);
  const b = t * s * s;
  const muQ = ct(b, `x${ex(s)}`);
  const lin = join([ct(s, "x"), "-1"]);
  const integral = ctParen(t, lin, ex(s));
  return {
    template: "x-exp",
    Pterm: ct(a, "y"),
    Pint: `${a}`,
    mu: ex(a),
    Q: ct(b, `x${ex(c)}`),
    muQ,
    integral,
    note: `By parts (${m(`u = x,\\ dv = ${ex(s)}\\,dx`)}): ${m(`\\int ${muQ}\\,dx = ${integral}`)}`,
    rhs: `(${b})*x*exp((${c})*x) - (${a})*y`,
    gen: (C) => join([ctParen(t, lin, ex(c)), cterm(C, ex(-a))]),
    genJs: (C) => `(${t})*exp((${c})*x)*((${s})*x - 1) + ${cjs(C)}*exp((${-a})*x)`,
    x0: 0,
    partAt0: -t,
  };
}

function ibpTrigExp(r: Rng): Linear {
  const t = r.nz(-3, 3);
  const k = 2 * t;
  const isSin = r.chance(0.5);
  const fT = isSin ? "\\sin x" : "\\cos x";
  const inner = isSin ? "\\sin x - \\cos x" : "\\sin x + \\cos x";
  const muQ = ct(k, `e^{x}${fT}`);
  const integral = ctParen(t, inner, "e^{x}");
  return {
    template: isSin ? "exp-sin" : "exp-cos",
    Pterm: "y",
    Pint: "1",
    mu: "e^{x}",
    Q: ct(k, fT),
    muQ,
    integral,
    note: `By parts twice; the integral reappears, so solve for it: ${m(`\\int ${muQ}\\,dx = ${integral}`)}`,
    rhs: `(${k})*${isSin ? "sin" : "cos"}(x) - y`,
    gen: (C) => join([ctParen(t, inner, ""), cterm(C, "e^{-x}")]),
    genJs: (C) => `(${t})*(sin(x) ${isSin ? "-" : "+"} cos(x)) + ${cjs(C)}*exp(-x)`,
    x0: 0,
    partAt0: isSin ? -t : t,
  };
}

function ibpPowerExp(r: Rng): Linear {
  // y' - (n/x) y = k x^{n+1} g(x)  ->  (y / x^n)' = k x g(x)
  const n = r.pick([1, 2, 3]);
  const k = r.nz(-3, 3);
  const g = r.pick(["exp", "cos", "sin"] as const);
  const gT = { exp: "e^{x}", cos: "\\cos x", sin: "\\sin x" }[g];
  const gJ = { exp: "exp(x)", cos: "cos(x)", sin: "sin(x)" }[g];
  const muQ = ct(k, `x${gT}`);
  const integral =
    g === "exp"
      ? ctParen(k, "x - 1", "e^{x}")
      : g === "cos"
      ? join([ct(k, "x\\sin x"), ct(k, "\\cos x")])
      : join([ct(k, "\\sin x"), ct(-k, "x\\cos x")]);
  const xn = xp(n);
  const xn1 = xp(n + 1);
  return {
    template: `power-${g}`,
    Pterm: `-\\frac{${n}}{x}y`,
    Pint: `-\\frac{${n}}{x}`,
    mu: `\\frac{1}{${xn}}`,
    Q: ct(k, xn1 + gT),
    muQ,
    integral,
    note: `By parts (${m(`u = x,\\ dv = ${gT}\\,dx`)}): ${m(`\\int ${muQ}\\,dx = ${integral}`)}`,
    rhs: `(${k})*x^(${n + 1})*${gJ} + (${n})*y/x`,
    gen: (C) =>
      g === "exp"
        ? join([ctParen(k, "x - 1", `${xn}e^{x}`), cterm(C, xn)])
        : g === "cos"
        ? join([ct(k, `${xn1}\\sin x`), ct(k, `${xn}\\cos x`), cterm(C, xn)])
        : join([ct(k, `${xn}\\sin x`), ct(-k, `${xn1}\\cos x`), cterm(C, xn)]),
    genJs: (C) =>
      g === "exp"
        ? `(${k})*(x - 1)*x^(${n})*exp(x) + ${cjs(C)}*x^(${n})`
        : g === "cos"
        ? `(${k})*x^(${n + 1})*sin(x) + (${k})*x^(${n})*cos(x) + ${cjs(C)}*x^(${n})`
        : `(${k})*x^(${n})*sin(x) - (${k})*x^(${n + 1})*cos(x) + ${cjs(C)}*x^(${n})`,
  };
}

function makeLinear(skill: SkillId, L: Linear, r: Rng, icChance: number): OdeProblem {
  const eq = `${join(["y'", L.Pterm])} = ${L.Q}`;
  const steps = [
    `Integrating factor: ${m(`\\mu = e^{\\int ${L.Pint}\\,dx} = ${L.mu}`)}`,
    `Multiply through: ${m(`\\left(${L.mu}\\,y\\right)' = ${L.muQ}`)}`,
  ];
  if (L.note) steps.push(L.note);
  steps.push(`Integrate: ${m(`${L.mu}\\,y = ${L.integral} + C`)}`);
  if (L.x0 !== undefined && L.partAt0 !== undefined && r.chance(icChance)) {
    const y0 = r.int(-4, 6);
    const C = y0 - L.partAt0;
    steps.push(`Solve for ${m("y")}: ${m(`y = ${L.gen(null)}`)}`);
    steps.push(`Apply ${m(`y(${L.x0}) = ${y0}`)}: ${m(`C = ${C}`)}`);
    steps.push(m(`y = ${L.gen(C)}`));
    return ode(skill, L.template, eq, L.rhs, `y = ${L.genJs(C)}`, `y = ${L.gen(C)}`, steps, [L.x0, y0]);
  }
  steps.push(m(`y = ${L.gen(null)}`));
  return ode(skill, L.template, eq, L.rhs, `y = ${L.genJs(null)}`, `y = ${L.gen(null)}`, steps);
}

// ═══════════════════════════════════════════════════════════════════════════
// 5. Bernoulli:  y' + P y = Q y^n,  v = y^{1-n}
// ═══════════════════════════════════════════════════════════════════════════
const YPOW: Record<string, string> = { "2": "y^{2}", "3": "y^{3}", "0.5": "\\sqrt{y}" };
const VDEF: Record<string, string> = {
  "2": "v = y^{-1} = \\frac{1}{y}",
  "3": "v = y^{-2} = \\frac{1}{y^{2}}",
  "0.5": "v = y^{1/2} = \\sqrt{y}",
};
const PTEX: Record<string, string> = { "2": "-1", "3": "-2", "0.5": "\\frac{1}{2}" };

function bernIntro(n: number): string[] {
  const key = `${n}`;
  return [
    `Bernoulli with ${m(`n = ${n === 0.5 ? "\\frac{1}{2}" : n}`)}: let ${m(VDEF[key])}`,
    `Divide by ${m(YPOW[key])} and multiply by ${m(`1 - n = ${PTEX[key]}`)} to get a linear equation in ${m("v")}:`,
  ];
}

function bernConst(r: Rng): OdeProblem {
  // y' + a y = b y^n
  const n = r.pick([2, 2, 3, 0.5]);
  const a = r.pick([1, 2, 3, -1, -2]);
  const k = r.nz(-3, 3);
  const b = k * a;
  const key = `${n}`;
  // p = 1 - n as a fraction pn/pd
  const [pn, pd] = n === 0.5 ? [1, 2] : [1 - n, 1];
  const vlhs = join(["v'", ctf(pn * a, pd, "v")]);
  const vrhs = ctf(pn * b, pd, "");
  const mu = `e^{${ctf(pn * a, pd, "x")}}`;
  const muQ = ctf(pn * b, pd, mu);
  const decay = `e^{${ctf(-pn * a, pd, "x")}}`;
  const vsol = `C${decay}${signed(k)}`;
  const ypowJs = n === 0.5 ? "sqrt(y)" : `y^${n}`;
  const decayJs = `exp((${-pn * a}/${pd})*x)`;
  let answer: string, answerTex: string;
  if (n === 2) {
    answer = `y = 1/(C*${decayJs} + (${k}))`;
    answerTex = `y = \\frac{1}{${vsol}}`;
  } else if (n === 3) {
    answer = `1/y^2 = C*${decayJs} + (${k})`;
    answerTex = `\\frac{1}{y^{2}} = ${vsol}`;
  } else {
    answer = `sqrt(y) = C*${decayJs} + (${k})`;
    answerTex = `\\sqrt{y} = ${vsol}`;
  }
  return ode(
    "bernoulli",
    `const-n${key}`,
    `${join(["y'", ct(a, "y")])} = ${ct(b, YPOW[key])}`,
    `(${b})*${ypowJs} - (${a})*y`,
    answer,
    answerTex,
    [
      ...bernIntro(n),
      m(`${vlhs} = ${vrhs}`),
      `Integrating factor ${m(`\\mu = ${mu}`)}: ${m(`\\left(${mu}\\,v\\right)' = ${muQ}`)}`,
      `Integrate and divide by ${m("\\mu")}: ${m(`v = ${vsol}`)}`,
      `Back-substitute: ${m(answerTex)}`,
    ]
  );
}

function bernPower(r: Rng): OdeProblem {
  // y' + (a/x) y = b x^m y^n
  const n = r.pick([2, 2, 3]);
  const p = 1 - n;
  const a = r.pick([1, 2, -1, -2, 3]);
  const mm = r.pick([0, 1, 2]);
  const s = p * a;
  require_(mm + s + 1 !== 0);
  const j = r.nz(-3, 3);
  const bNum = j * (mm + s + 1);
  require_(bNum % p === 0);
  const b = bNum / p;
  const key = `${n}`;
  const Pterm = a > 0 ? `\\frac{${a}}{x}y` : `-\\frac{${-a}}{x}y`;
  const sv = s > 0 ? `\\frac{${s}}{x}v` : `-\\frac{${-s}}{x}v`;
  const mu = s > 0 ? xp(s) : `\\frac{1}{${xp(-s)}}`;
  const vsol = join([xpow(j, mm + 1), s > 0 ? `\\frac{C}{${xp(s)}}` : `C${xp(-s)}`]);
  const vJs = `(${j})*x^(${mm + 1}) + C*x^(${-s})`;
  const answer = n === 2 ? `y = 1/(${vJs})` : `1/y^2 = ${vJs}`;
  const answerTex = n === 2 ? `y = \\frac{1}{${vsol}}` : `\\frac{1}{y^{2}} = ${vsol}`;
  return ode(
    "bernoulli",
    `power-n${n}`,
    `${join(["y'", Pterm])} = ${ct(b, xp(mm) + YPOW[key])}`,
    `(${b})*x^(${mm})*y^${n} - (${a})*y/x`,
    answer,
    answerTex,
    [
      ...bernIntro(n),
      m(`${join(["v'", sv])} = ${xpow(p * b, mm)}`),
      `Integrating factor ${m(`\\mu = ${mu}`)}: ${m(`\\left(${mu}\\,v\\right)' = ${xpow(p * b, mm + s)}`)}`,
      `Integrate and divide by ${m("\\mu")}: ${m(`v = ${vsol}`)}`,
      `Back-substitute: ${m(answerTex)}`,
    ]
  );
}

function bernExp(r: Rng): OdeProblem {
  // y' + a y = b e^{cx} y^2
  const a = r.pick([1, 2, -1, -2]);
  const c = r.nz(-2, 3, [0, a]);
  const j = r.nz(-2, 2);
  const b = -j * (c - a);
  const vsol = join([ct(j, ex(c)), `C${ex(a)}`]);
  const answerTex = `y = \\frac{1}{${vsol}}`;
  return ode(
    "bernoulli",
    "exp-n2",
    `${join(["y'", ct(a, "y")])} = ${ct(b, ex(c) + "y^{2}")}`,
    `(${b})*exp((${c})*x)*y^2 - (${a})*y`,
    `y = 1/((${j})*exp((${c})*x) + C*exp((${a})*x))`,
    answerTex,
    [
      ...bernIntro(2),
      m(`${join(["v'", ct(-a, "v")])} = ${ct(-b, ex(c))}`),
      `Integrating factor ${m(`\\mu = ${ex(-a)}`)}: ${m(`\\left(${ex(-a)}\\,v\\right)' = ${ct(-b, ex(c - a))}`)}`,
      `Integrate and divide by ${m("\\mu")}: ${m(`v = ${vsol}`)}`,
      `Back-substitute: ${m(answerTex)}`,
    ]
  );
}

// ═══════════════════════════════════════════════════════════════════════════
// 6. Wronskian
// ═══════════════════════════════════════════════════════════════════════════
interface WSpec {
  template: string;
  f: string[]; // LaTeX of each function
  js: string[]; // mathjs of each function
  rows: string[][]; // LaTeX matrix rows (function, first derivative, ...)
  W: string;
  Wjs: string;
}

function wronskian(spec: WSpec): WronskianProblem {
  const independent = spec.Wjs.trim() !== "0";
  const fl = spec.f.join(",\\ ");
  const matrix = `W = \\begin{vmatrix} ${spec.rows.map((r) => r.join(" & ")).join(" \\\\ ")} \\end{vmatrix}`;
  const P = (s: string) => `\\left(${s}\\right)`;
  const steps = [m(matrix)];
  if (spec.f.length === 2) {
    steps.push(m(`W = ${P(spec.rows[0][0])}${P(spec.rows[1][1])} - ${P(spec.rows[0][1])}${P(spec.rows[1][0])}`));
  } else {
    steps.push("Expand the 3×3 determinant (cofactor expansion along a row or column with zeros).");
  }
  steps.push(m(`W = ${spec.W}`));
  steps.push(
    independent
      ? `${m("W \\neq 0")}, so the functions are linearly independent.`
      : `${m("W \\equiv 0")}, so the functions are linearly dependent (one is a multiple or combination of the others).`
  );
  return {
    prompt: `Find the Wronskian ${m(spec.f.length === 2 ? "W(f, g)" : "W(f, g, h)")} of ${m(fl)}.`,
    answer: { kind: "expression", ref: spec.Wjs, vars: ["x"], label: "W" },
    answerTex: `W = ${spec.W}`,
    steps,
    meta: { variant: spec.template, funcs: spec.js, independent },
  };
}

function wrExps(r: Rng): WronskianProblem {
  const a = r.int(-3, 3);
  const b = r.nz(-4, 4, [a]);
  const F = (k: number) => (k === 0 ? "1" : ex(k));
  const D = (k: number) => (k === 0 ? "0" : ct(k, ex(k)));
  return wronskian({
    template: "exps",
    f: [F(a), F(b)],
    js: [`exp((${a})*x)`, `exp((${b})*x)`],
    rows: [
      [F(a), F(b)],
      [D(a), D(b)],
    ],
    W: ct(b - a, ex(a + b)),
    Wjs: `(${b - a})*exp((${a + b})*x)`,
  });
}

function wrRepeated(r: Rng): WronskianProblem {
  const a = r.nz(-3, 3);
  return wronskian({
    template: "repeated",
    f: [ex(a), `x${ex(a)}`],
    js: [`exp((${a})*x)`, `x*exp((${a})*x)`],
    rows: [
      [ex(a), `x${ex(a)}`],
      [ct(a, ex(a)), join([ct(a, `x${ex(a)}`), ex(a)])],
    ],
    W: ex(2 * a),
    Wjs: `exp((${2 * a})*x)`,
  });
}

function wrTrig(r: Rng): WronskianProblem {
  const k = r.int(1, 5);
  const t = trigArg(k);
  return wronskian({
    template: "trig",
    f: [`\\cos ${t}`, `\\sin ${t}`],
    js: [`cos(${k}*x)`, `sin(${k}*x)`],
    rows: [
      [`\\cos ${t}`, `\\sin ${t}`],
      [ct(-k, `\\sin ${t}`), ct(k, `\\cos ${t}`)],
    ],
    W: `${k}`,
    Wjs: `${k}`,
  });
}

function wrDamped(r: Rng): WronskianProblem {
  const a = r.nz(-2, 2);
  const b = r.int(1, 4);
  const t = trigArg(b);
  const E = ex(a);
  return wronskian({
    template: "damped",
    f: [`${E}\\cos ${t}`, `${E}\\sin ${t}`],
    js: [`exp((${a})*x)*cos(${b}*x)`, `exp((${a})*x)*sin(${b}*x)`],
    rows: [
      [`${E}\\cos ${t}`, `${E}\\sin ${t}`],
      [
        `${E}\\left(${join([ct(a, `\\cos ${t}`), ct(-b, `\\sin ${t}`)])}\\right)`,
        `${E}\\left(${join([ct(a, `\\sin ${t}`), ct(b, `\\cos ${t}`)])}\\right)`,
      ],
    ],
    W: ct(b, ex(2 * a)),
    Wjs: `(${b})*exp((${2 * a})*x)`,
  });
}

function wrPowers(r: Rng): WronskianProblem {
  const p = r.int(1, 4);
  const q = r.nz(-2, 5, [0, p]);
  return wronskian({
    template: "powers",
    f: [xpow(1, p), xpow(1, q)],
    js: [`x^(${p})`, `x^(${q})`],
    rows: [
      [xpow(1, p), xpow(1, q)],
      [xpow(p, p - 1), xpow(q, q - 1)],
    ],
    W: xpow(q - p, p + q - 1),
    Wjs: `(${q - p})*x^(${p + q - 1})`,
  });
}

function wrLog(r: Rng): WronskianProblem {
  const p = r.pick([1, 2, -1]);
  const spec: Record<number, WSpec> = {
    1: {
      template: "log",
      f: ["x", "x\\ln x"],
      js: ["x", "x*log(x)"],
      rows: [
        ["x", "x\\ln x"],
        ["1", "\\ln x + 1"],
      ],
      W: "x",
      Wjs: "x",
    },
    2: {
      template: "log",
      f: ["x^{2}", "x^{2}\\ln x"],
      js: ["x^2", "x^2*log(x)"],
      rows: [
        ["x^{2}", "x^{2}\\ln x"],
        ["2x", "2x\\ln x + x"],
      ],
      W: "x^{3}",
      Wjs: "x^3",
    },
    [-1]: {
      template: "log",
      f: ["\\frac{1}{x}", "\\frac{\\ln x}{x}"],
      js: ["1/x", "log(x)/x"],
      rows: [
        ["\\frac{1}{x}", "\\frac{\\ln x}{x}"],
        ["-\\frac{1}{x^{2}}", "\\frac{1 - \\ln x}{x^{2}}"],
      ],
      W: "\\frac{1}{x^{3}}",
      Wjs: "x^(-3)",
    },
  };
  return wronskian(spec[p]);
}

function wrThree(r: Rng): WronskianProblem {
  const specs: WSpec[] = [
    {
      template: "three-poly",
      f: ["1", "x", "x^{2}"],
      js: ["1", "x", "x^2"],
      rows: [
        ["1", "x", "x^{2}"],
        ["0", "1", "2x"],
        ["0", "0", "2"],
      ],
      W: "2",
      Wjs: "2",
    },
    {
      template: "three-exp",
      f: ["e^{x}", "e^{-x}", "e^{2x}"],
      js: ["exp(x)", "exp(-x)", "exp(2*x)"],
      rows: [
        ["e^{x}", "e^{-x}", "e^{2x}"],
        ["e^{x}", "-e^{-x}", "2e^{2x}"],
        ["e^{x}", "e^{-x}", "4e^{2x}"],
      ],
      W: "-6e^{2x}",
      Wjs: "-6*exp(2*x)",
    },
    {
      template: "three-trig",
      f: ["1", "\\cos x", "\\sin x"],
      js: ["1", "cos(x)", "sin(x)"],
      rows: [
        ["1", "\\cos x", "\\sin x"],
        ["0", "-\\sin x", "\\cos x"],
        ["0", "-\\cos x", "-\\sin x"],
      ],
      W: "1",
      Wjs: "1",
    },
    {
      template: "three-exp2",
      f: ["1", "e^{x}", "e^{2x}"],
      js: ["1", "exp(x)", "exp(2*x)"],
      rows: [
        ["1", "e^{x}", "e^{2x}"],
        ["0", "e^{x}", "2e^{2x}"],
        ["0", "e^{x}", "4e^{2x}"],
      ],
      W: "2e^{3x}",
      Wjs: "2*exp(3*x)",
    },
    {
      template: "three-mono",
      f: ["x", "x^{2}", "x^{3}"],
      js: ["x", "x^2", "x^3"],
      rows: [
        ["x", "x^{2}", "x^{3}"],
        ["1", "2x", "3x^{2}"],
        ["0", "2", "6x"],
      ],
      W: "2x^{3}",
      Wjs: "2*x^3",
    },
  ];
  return wronskian(r.pick(specs));
}

function wrDependent(r: Rng): WronskianProblem {
  const k = r.pick([2, 3, -2, 5]);
  const a = r.nz(-3, 3);
  const specs: WSpec[] = [
    {
      template: "dep-multiple",
      f: [ex(a), ct(k, ex(a))],
      js: [`exp((${a})*x)`, `(${k})*exp((${a})*x)`],
      rows: [
        [ex(a), ct(k, ex(a))],
        [ct(a, ex(a)), ct(k * a, ex(a))],
      ],
      W: "0",
      Wjs: "0",
    },
    {
      template: "dep-double-angle",
      f: ["\\sin 2x", "\\sin x\\cos x"],
      js: ["sin(2*x)", "sin(x)*cos(x)"],
      rows: [
        ["\\sin 2x", "\\sin x\\cos x"],
        ["2\\cos 2x", "\\cos^{2}x - \\sin^{2}x"],
      ],
      W: "0",
      Wjs: "0",
    },
    {
      template: "dep-pythagorean",
      f: ["1", "\\sin^{2}x", "\\cos^{2}x"],
      js: ["1", "sin(x)^2", "cos(x)^2"],
      rows: [
        ["1", "\\sin^{2}x", "\\cos^{2}x"],
        ["0", "2\\sin x\\cos x", "-2\\sin x\\cos x"],
        ["0", "2\\cos 2x", "-2\\cos 2x"],
      ],
      W: "0",
      Wjs: "0",
    },
    {
      template: "dep-linear",
      f: ["x", ct(k, "x")],
      js: ["x", `(${k})*x`],
      rows: [
        ["x", ct(k, "x")],
        ["1", `${k}`],
      ],
      W: "0",
      Wjs: "0",
    },
  ];
  return wronskian(r.pick(specs));
}

// ═══════════════════════════════════════════════════════════════════════════
// Named templates (referenced from drills/skills.yaml)
// ═══════════════════════════════════════════════════════════════════════════
const LIN_IC = 0.4;
const IBP_IC = 0.3;
const lin = (b: (r: Rng) => Linear) => (r: Rng) => makeLinear("linear", b(r), r, LIN_IC);
const ibp = (b: (r: Rng) => Linear) => (r: Rng) => makeLinear("ibp", b(r), r, IBP_IC);

export const FIRST_ORDER_TEMPLATES: Record<string, (r: Rng) => Draft> = {
  "sep-exp-growth": sepExpGrowth,
  "sep-over-y": sepOverY,
  "sep-y-squared": sepYSquared,
  "sep-exp-split": sepExpSplit,
  "sep-over-y2": sepOverY2,
  "sub-ratio": subRatio,
  "sub-square": subSquare,
  "sub-exp": subExp,
  "sub-linear-square": subLinearSquare,
  "sub-arctan": subArctan,
  "lin-exp": lin(linExp),
  "lin-const": lin(linConst),
  "lin-power": lin(linPower),
  "lin-gauss": lin(linGauss),
  "lin-trig": lin(linTrig),
  "lin-resonant": lin(linResonant),
  "ibp-poly": ibp(ibpPoly),
  "ibp-over-x-trig": ibp(ibpOverXTrig),
  "ibp-over-x-exp": ibp(ibpOverXExp),
  "ibp-x-exp": ibp(ibpXExp),
  "ibp-trig-exp": ibp(ibpTrigExp),
  "ibp-power-exp": ibp(ibpPowerExp),
  "bern-const": bernConst,
  "bern-power": bernPower,
  "bern-exp": bernExp,
  "wr-exps": wrExps,
  "wr-repeated": wrRepeated,
  "wr-trig": wrTrig,
  "wr-damped": wrDamped,
  "wr-powers": wrPowers,
  "wr-log": wrLog,
  "wr-three": wrThree,
  "wr-dependent": wrDependent,
};
