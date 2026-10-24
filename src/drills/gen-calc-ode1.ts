// Calculus prerequisites (u-sub, by parts, partial fractions, complex numbers,
// index shifts, partial derivatives) and the rest of Kreyszig Ch 1 (exact
// equations, integrating factors, modeling, "which method?"). Level 1.
//
// Everything is built BACKWARD: pick the antiderivative / potential / roots /
// coefficients first, then derive the question, so answers stay tidy.
// Indefinite integrals use the "ode" answer kind with y' = f(x): the checker
// solves for C at sample points and compares slopes, so any antiderivative
// (any constant) is accepted, a wrong one is rejected, and a missing C is flagged.
import { Rng } from "./rng";
import type { Draft } from "./types";
import { ct, join, m, xp } from "./tex";
import { Q, qterm } from "./rational";
import { require_ } from "./reject";
import { math, real } from "./check";

const q = (n: number, d = 1) => new Q(n, d);

// ═══════════════════════════════════════════════════════════════════════════
// LaTeX / mathjs helpers
// ═══════════════════════════════════════════════════════════════════════════
/** v + off: "x", "x + 2", "k - 1" */
function lin(v: string, off: number): string {
  if (off === 0) return v;
  return off > 0 ? `${v} + ${off}` : `${v} - ${-off}`;
}
const linJs = (v: string, off: number) => `(${v} + (${off}))`;
/** q * num / den as one fraction, sign in front:  -\frac{3x}{2(x - 1)} */
function coefOver(c: Q, num: string, den: string): string {
  const sign = c.n < 0 ? "-" : "";
  const n = Math.abs(c.n);
  const top = num ? (n === 1 ? num : `${n}${num}`) : `${n}`;
  const bot = c.d === 1 ? den : `${c.d}${den}`;
  return `${sign}\\frac{${top}}{${bot}}`;
}
/** coefficient term c·body; tex body may be "" */
interface Tm {
  c: Q;
  tex: string;
  js: string;
}
const tm = (c: Q | number, tex: string, js: string): Tm => ({ c: Q.of(c), tex, js });
const sumTex = (ts: Tm[]) => join(ts.filter((t) => !t.c.isZero()).map((t) => qterm(t.c, t.tex)));
function sumJs(ts: Tm[]): string {
  const s = ts.filter((t) => !t.c.isZero()).map((t) => `${t.c.js()}*(${t.js || "1"})`);
  return s.length ? s.join(" + ") : "0";
}
const P = (s: string) => `\\left(${s}\\right)`;
/** parenthesize a negative factor */
const par = (s: string) => (s.startsWith("-") ? P(s) : s);
/** sin / cos of k·v, LaTeX: \sin x, \sin(3x) */
const trig = (fn: string, k: number, v = "x") => (k === 1 ? `\\${fn} ${v}` : `\\${fn}(${k}${v})`);
const trigJs = (fn: string, k: number, v = "x") => `${fn}((${k})*${v})`;
/** sin^p(kx) */
function trigPow(fn: string, k: number, p: number): string {
  if (p === 1) return trig(fn, k);
  return k === 1 ? `\\${fn}^{${p}} x` : `\\${fn}^{${p}}(${k}x)`;
}
const eTex = (k: number, v = "x") => `e^{${ct(k, v)}}`;
const eJs = (k: number, v = "x") => `exp((${k})*${v})`;
/** the root's linear factor: x, x - 2, x + 3 */
const xr = (root: number) => lin("x", -root);
const xrJs = (root: number) => `(x - (${root}))`;
/** factor in a product: x or (x - 2) */
const xrFac = (root: number) => (root === 0 ? "x" : P(xr(root)));
const lnAbs = (root: number) => `\\ln|${xr(root)}|`;
const lnAbsJs = (root: number) => `log(abs(${xrJs(root)}))`;

// ── small integer polynomials (coefficient i = x^i) ─────────────────────────
type Poly = number[];
function pmul(a: Poly, b: Poly): Poly {
  const out = new Array(a.length + b.length - 1).fill(0);
  a.forEach((ai, i) => b.forEach((bj, j) => (out[i + j] += ai * bj)));
  return out;
}
function padd(...ps: Poly[]): Poly {
  const n = Math.max(...ps.map((p) => p.length));
  const out = new Array(n).fill(0);
  for (const p of ps) p.forEach((c, i) => (out[i] += c));
  while (out.length > 1 && out[out.length - 1] === 0) out.pop();
  return out;
}
const pscale = (p: Poly, k: number) => p.map((c) => c * k);
const root1 = (a: number): Poly => [-a, 1];
const peval = (p: Poly, x: number) => p.reduce((s, c, i) => s + c * x ** i, 0);
function polyTex(p: Poly, v = "x"): string {
  const t: string[] = [];
  for (let i = p.length - 1; i >= 0; i--) if (p[i]) t.push(i === 0 ? `${p[i]}` : ct(p[i], i === 1 ? v : `${v}^{${i}}`));
  return join(t);
}
function polyJs(p: Poly): string {
  const t = p.map((c, i) => (c ? `(${c})*x^${i}` : "")).filter(Boolean);
  return t.length ? t.join(" + ") : "0";
}

function fmtNum(v: number): string {
  if (Math.abs(v - Math.round(v)) < 1e-9) return `${Math.round(v)}`;
  return Number(v.toPrecision(4)).toString();
}

// ── indefinite integral as the "ode" kind y' = integrand ────────────────────
function integral(
  integrand: string,
  integrandJs: string,
  Ftex: string,
  Fjs: string,
  steps: string[],
  variant: string
): Draft {
  return {
    prompt: `Evaluate ${m(`\\int ${integrand}\\,dx`)}`,
    answer: { kind: "ode", rhs: integrandJs, ref: `y = ${Fjs} + C` },
    answerTex: `${Ftex} + C`,
    steps,
    meta: { variant, integrand: integrandJs, F: Fjs },
  };
}

// ═══════════════════════════════════════════════════════════════════════════
// calc.u-sub
// ═══════════════════════════════════════════════════════════════════════════
function usubPoly(r: Rng): Draft {
  // ∫ s x^n (a x^{n+1} + b)^p dx = s/(a(n+1)(p+1)) u^{p+1}
  const n = r.pick([1, 1, 2]);
  const a = r.pick([1, 2, 3, -1]);
  const b = r.pick([1, 2, 3, -1, -2, -3]);
  const p = r.pick([2, 3, -2, -3, 0.5]);
  if (p === 0.5) require_(a > 0 && b > 0);
  const du = a * (n + 1);
  const s = r.chance(0.5) ? du * r.pick([1, 2]) : r.pick([1, 2, 3]);
  const sAbs = Math.abs(s);
  const sg = s < 0 ? "-" : "";
  const u = join([ct(a, xp(n + 1)), `${b}`]);
  const uJs = `((${a})*x^${n + 1} + (${b}))`;
  const xn = ct(sAbs, xp(n));
  let integrand: string, integrandJs: string, Ftex: string, Fjs: string, inner: string, outer: string;
  if (p === 0.5) {
    integrand = `${sg}${xn}\\sqrt{${u}}`;
    integrandJs = `(${s})*x^${n}*sqrt(${uJs})`;
    const K = q(2 * s, 3 * du);
    Ftex = qterm(K, `${P(u)}^{3/2}`);
    Fjs = `${K.js()}*${uJs}^(3/2)`;
    inner = "\\sqrt{u}";
    outer = `\\frac{2}{3}u^{3/2}`;
  } else {
    integrand = p > 0 ? `${sg}${xn}${P(u)}^{${p}}` : `${sg}\\frac{${xn}}{${P(u)}^{${-p}}}`;
    integrandJs = `(${s})*x^${n}*${uJs}^(${p})`;
    const K = q(s, du * (p + 1));
    Ftex = p + 1 === -1 ? coefOver(K, "", P(u)) : p + 1 < 0 ? coefOver(K, "", `${P(u)}^{${-(p + 1)}}`) : qterm(K, `${P(u)}^{${p + 1}}`);
    Fjs = `${K.js()}*${uJs}^(${p + 1})`;
    inner = `u^{${p}}`;
    outer = p + 1 === -1 ? "-u^{-1}" : qterm(q(1, p + 1), `u^{${p + 1}}`);
  }
  const k = q(s, du);
  return integral(
    integrand,
    integrandJs,
    Ftex,
    Fjs,
    [
      `Let ${m(`u = ${u}`)}; then ${m(`du = ${ct(du, xp(n))}\\,dx`)}, so ${m(`${xp(n)}\\,dx = \\frac{du}{${du}}`)}.`,
      `Substitute: ${m(`${qterm(k, `\\int ${inner}\\,du`)}`)}`,
      `Power rule: ${m(`${qterm(k, P(outer))}`)} ${m("+ C")}`,
      `Back-substitute: ${m(`${Ftex} + C`)}`,
    ],
    "usub-poly"
  );
}

function usubExp(r: Rng): Draft {
  const s = r.pick([1, 2, 3, 4, 6]);
  const kind = r.pick(["power", "power", "sqrt", "trig"]);
  if (kind === "power") {
    // ∫ s x^n e^{a x^{n+1}} dx = s/(a(n+1)) e^{a x^{n+1}}
    const n = r.pick([1, 2]);
    const a = n === 1 ? r.pick([1, 2, -1, -2]) : r.pick([1, -1]);
    const ex = `e^{${ct(a, xp(n + 1))}}`;
    const exJs = `exp((${a})*x^${n + 1})`;
    const K = q(s, a * (n + 1));
    return integral(
      `${ct(s, xp(n))}${ex}`,
      `(${s})*x^${n}*${exJs}`,
      qterm(K, ex),
      `${K.js()}*${exJs}`,
      [
        `Let ${m(`u = ${ct(a, xp(n + 1))}`)}; then ${m(`du = ${ct(a * (n + 1), xp(n))}\\,dx`)}.`,
        `Substitute: ${m(qterm(K, "\\int e^{u}\\,du"))}`,
        `${m(`= ${qterm(K, "e^{u}")} + C = ${qterm(K, ex)} + C`)}`,
      ],
      "usub-exp"
    );
  }
  if (kind === "sqrt") {
    // ∫ s e^{k√x}/√x dx = (2s/k) e^{k√x}
    const k = r.pick([1, 2, 3, -1]);
    const ex = `e^{${ct(k, "\\sqrt{x}")}}`;
    const exJs = `exp((${k})*sqrt(x))`;
    const K = q(2 * s, k);
    return integral(
      `\\frac{${ct(s, ex)}}{\\sqrt{x}}`,
      `(${s})*${exJs}/sqrt(x)`,
      qterm(K, ex),
      `${K.js()}*${exJs}`,
      [
        `Let ${m(`u = ${ct(k, "\\sqrt{x}")}`)}; then ${m(`du = \\frac{${k}}{2\\sqrt{x}}\\,dx`)}, so ${m(`\\frac{dx}{\\sqrt{x}} = \\frac{2}{${k}}\\,du`)}.`,
        `Substitute: ${m(qterm(K, "\\int e^{u}\\,du"))}`,
        m(`= ${qterm(K, ex)} + C`),
      ],
      "usub-exp"
    );
  }
  // ∫ s cos x e^{sin x} dx = s e^{sin x};  ∫ s sin x e^{cos x} dx = -s e^{cos x}
  const sinIn = r.chance(0.5);
  const ex = sinIn ? "e^{\\sin x}" : "e^{\\cos x}";
  const exJs = sinIn ? "exp(sin(x))" : "exp(cos(x))";
  const K = q(sinIn ? s : -s);
  return integral(
    `${ct(s, ex)}${sinIn ? "\\cos x" : "\\sin x"}`,
    `(${s})*${exJs}*${sinIn ? "cos(x)" : "sin(x)"}`,
    qterm(K, ex),
    `${K.js()}*${exJs}`,
    [
      `Let ${m(sinIn ? "u = \\sin x" : "u = \\cos x")}; then ${m(sinIn ? "du = \\cos x\\,dx" : "du = -\\sin x\\,dx")}.`,
      `Substitute: ${m(qterm(K, "\\int e^{u}\\,du"))}`,
      m(`= ${qterm(K, ex)} + C`),
    ],
    "usub-exp"
  );
}

function usubTrig(r: Rng): Draft {
  const s = r.pick([1, 2, 3, 4, 6]);
  const kind = r.pick(["sin-cos", "cos-sin", "x-trig", "tan-sec"]);
  if (kind === "x-trig") {
    // ∫ s x cos(a x^2) dx = s/(2a) sin(a x^2);  ∫ s x sin(a x^2) dx = -s/(2a) cos(a x^2)
    const a = r.pick([1, 2, 3]);
    const fn = r.pick(["sin", "cos"]);
    const other = fn === "cos" ? "sin" : "cos";
    const arg = ct(a, "x^{2}");
    const K = q(fn === "cos" ? s : -s, 2 * a);
    return integral(
      `${ct(s, "x")}\\${fn}(${arg})`,
      `(${s})*x*${fn}((${a})*x^2)`,
      qterm(K, `\\${other}(${arg})`),
      `${K.js()}*${other}((${a})*x^2)`,
      [
        `Let ${m(`u = ${arg}`)}; then ${m(`du = ${ct(2 * a, "x")}\\,dx`)}, so ${m(`x\\,dx = \\frac{du}{${2 * a}}`)}.`,
        `Substitute: ${m(qterm(q(s, 2 * a), `\\int \\${fn} u\\,du`))}`,
        m(`= ${qterm(K, `\\${other}(${arg})`)} + C`),
      ],
      "usub-trig"
    );
  }
  const k = r.pick([1, 2, 3]);
  const p = r.pick([1, 2, 3, 4]);
  if (kind === "tan-sec") {
    // ∫ s tan^p(kx) sec^2(kx) dx = s/(k(p+1)) tan^{p+1}(kx)
    const K = q(s, k * (p + 1));
    const kx = k === 1 ? "x" : `${k}x`;
    return integral(
      `${ct(s, trigPow("tan", k, p))}\\sec^{2}${k === 1 ? " x" : `(${kx})`}`,
      `(${s})*tan((${k})*x)^(${p})*sec((${k})*x)^2`,
      qterm(K, trigPow("tan", k, p + 1)),
      `${K.js()}*tan((${k})*x)^(${p + 1})`,
      [
        `Let ${m(`u = ${trig("tan", k)}`)}; then ${m(`du = ${ct(k, `\\sec^{2}${k === 1 ? " x" : `(${kx})`}`)}\\,dx`)}.`,
        `Substitute: ${m(qterm(q(s, k), `\\int ${p === 1 ? "u" : `u^{${p}}`}\\,du`))}`,
        m(`= ${qterm(K, trigPow("tan", k, p + 1))} + C`),
      ],
      "usub-trig"
    );
  }
  // ∫ s sin^p(kx) cos(kx) dx = s/(k(p+1)) sin^{p+1};  ∫ s cos^p sin = -s/(k(p+1)) cos^{p+1}
  const pw = kind === "sin-cos" ? "sin" : "cos";
  const dv = kind === "sin-cos" ? "cos" : "sin";
  const K = q(kind === "sin-cos" ? s : -s, k * (p + 1));
  return integral(
    `${ct(s, trigPow(pw, k, p))}${trig(dv, k)}`,
    `(${s})*${pw}((${k})*x)^(${p})*${dv}((${k})*x)`,
    qterm(K, trigPow(pw, k, p + 1)),
    `${K.js()}*${pw}((${k})*x)^(${p + 1})`,
    [
      `Let ${m(`u = ${trig(pw, k)}`)}; then ${m(`du = ${ct(kind === "sin-cos" ? k : -k, trig(dv, k))}\\,dx`)}.`,
      `Substitute: ${m(qterm(q(kind === "sin-cos" ? s : -s, k), `\\int ${p === 1 ? "u" : `u^{${p}}`}\\,du`))}`,
      m(`= ${qterm(K, trigPow(pw, k, p + 1))} + C`),
    ],
    "usub-trig"
  );
}

function usubLog(r: Rng): Draft {
  const s = r.pick([1, 2, 3, 4, 6]);
  const kind = r.pick(["power", "power", "loglog", "inverse"]);
  const intro = `Let ${m("u = \\ln x")}; then ${m("du = \\frac{dx}{x}")}.`;
  if (kind === "loglog") {
    return integral(
      `\\frac{${s}}{x\\ln x}`,
      `(${s})/(x*log(x))`,
      ct(s, "\\ln|\\ln x|"),
      `(${s})*log(abs(log(x)))`,
      [intro, `Substitute: ${m(`${ct(s, "\\int \\frac{du}{u}")} = ${ct(s, "\\ln|u|")} + C`)}`, m(`= ${ct(s, "\\ln|\\ln x|")} + C`)],
      "usub-log"
    );
  }
  if (kind === "inverse") {
    // ∫ s / (x (ln x)^p) dx = -s/((p-1)(ln x)^{p-1})
    const p = r.pick([2, 3]);
    const K = q(-s, p - 1);
    const Ftex = coefOver(K, "", p - 1 === 1 ? "\\ln x" : `(\\ln x)^{${p - 1}}`);
    return integral(
      `\\frac{${s}}{x(\\ln x)^{${p}}}`,
      `(${s})/(x*log(x)^${p})`,
      Ftex,
      `${K.js()}/log(x)^${p - 1}`,
      [intro, `Substitute: ${m(`${ct(s, `\\int u^{-${p}}\\,du`)} = ${coefOver(K, "", p - 1 === 1 ? "u" : `u^{${p - 1}}`)} + C`)}`, m(`= ${Ftex} + C`)],
      "usub-log"
    );
  }
  const p = r.pick([1, 2, 3]);
  const K = q(s, p + 1);
  const lnp = p === 1 ? "\\ln x" : `(\\ln x)^{${p}}`;
  return integral(
    `\\frac{${ct(s, lnp)}}{x}`,
    `(${s})*log(x)^${p}/x`,
    qterm(K, `(\\ln x)^{${p + 1}}`),
    `${K.js()}*log(x)^${p + 1}`,
    [intro, `Substitute: ${m(`${ct(s, `\\int ${p === 1 ? "u" : `u^{${p}}`}\\,du`)} = ${qterm(K, `u^{${p + 1}}`)} + C`)}`, m(`= ${qterm(K, `(\\ln x)^{${p + 1}}`)} + C`)],
    "usub-log"
  );
}

function usubRatio(r: Rng): Draft {
  const s = r.pick([1, 2, 3, 4, 6]);
  const kind = r.pick(["log", "log", "sqrt", "trig"]);
  if (kind === "sqrt") {
    // ∫ s x / sqrt(x^2 + c) dx = s sqrt(x^2 + c)
    const c = r.pick([1, 4, 9, 2, 5]);
    const inside = `x^{2} + ${c}`;
    return integral(
      `\\frac{${ct(s, "x")}}{\\sqrt{${inside}}}`,
      `(${s})*x/sqrt(x^2 + ${c})`,
      ct(s, `\\sqrt{${inside}}`),
      `(${s})*sqrt(x^2 + ${c})`,
      [
        `Let ${m(`u = ${inside}`)}; then ${m("du = 2x\\,dx")}.`,
        `Substitute: ${m(`${qterm(q(s, 2), "\\int u^{-1/2}\\,du")} = ${ct(s, "u^{1/2}")} + C`)}`,
        m(`= ${ct(s, `\\sqrt{${inside}}`)} + C`),
      ],
      "usub-ratio"
    );
  }
  if (kind === "trig") {
    const c = r.pick([2, 3, 4]);
    const sinBottom = r.chance(0.5);
    const den = sinBottom ? `\\sin x + ${c}` : `\\cos x + ${c}`;
    const denJs = sinBottom ? `(sin(x) + ${c})` : `(cos(x) + ${c})`;
    const K = q(sinBottom ? s : -s);
    return integral(
      `\\frac{${ct(s, sinBottom ? "\\cos x" : "\\sin x")}}{${den}}`,
      `(${s})*${sinBottom ? "cos(x)" : "sin(x)"}/${denJs}`,
      qterm(K, `\\ln(${den})`),
      `${K.js()}*log(${denJs})`,
      [
        `The numerator is ${sinBottom ? "" : "minus "}the derivative of the denominator: let ${m(`u = ${den}`)}, ${m(`du = ${sinBottom ? "\\cos x" : "-\\sin x"}\\,dx`)}.`,
        `Substitute: ${m(`${qterm(K, "\\int \\frac{du}{u}")} = ${qterm(K, "\\ln|u|")} + C`)}`,
        `${m(`u > 0`)} always, so ${m(`${qterm(K, `\\ln(${den})`)} + C`)}`,
      ],
      "usub-ratio"
    );
  }
  // ∫ s x^n / (x^{n+1} + c) dx = s/(n+1) ln|x^{n+1} + c|
  const n = r.pick([1, 2]);
  const c = r.nz(-5, 6);
  const den = `${xp(n + 1)}${c < 0 ? ` - ${-c}` : ` + ${c}`}`;
  const denJs = `(x^${n + 1} + (${c}))`;
  const K = q(s, n + 1);
  return integral(
    `\\frac{${ct(s, xp(n))}}{${den}}`,
    `(${s})*x^${n}/${denJs}`,
    qterm(K, `\\ln|${den}|`),
    `${K.js()}*log(abs(${denJs}))`,
    [
      `Let ${m(`u = ${den}`)}; then ${m(`du = ${ct(n + 1, xp(n))}\\,dx`)}.`,
      `Substitute: ${m(`${qterm(K, "\\int \\frac{du}{u}")} = ${qterm(K, "\\ln|u|")} + C`)}`,
      m(`= ${qterm(K, `\\ln|${den}|`)} + C`),
    ],
    "usub-ratio"
  );
}

function usubLinear(r: Rng): Draft {
  const a = r.pick([2, 3, 4, -2, -3]);
  const b = r.nz(-3, 3);
  require_(Math.abs(0.35 * a + b) < 3); // keep the integrand moderate where the checker samples
  const u = join([ct(a, "x"), `${b}`]);
  const uJs = `((${a})*x + (${b}))`;
  const s = r.chance(0.5) ? Math.abs(a) * r.pick([1, 2]) : r.pick([1, 2, 3]);
  const kind = r.pick(["power", "power", "cos", "recip"]);
  const intro = `Let ${m(`u = ${u}`)}; then ${m(`du = ${a}\\,dx`)}, so ${m(`dx = \\frac{du}{${a}}`)}.`;
  if (kind === "cos") {
    const fn = r.pick(["sin", "cos"]);
    const other = fn === "cos" ? "sin" : "cos";
    const K = q(fn === "cos" ? s : -s, a);
    return integral(
      `${ct(s, `\\${fn}(${u})`)}`,
      `(${s})*${fn}(${uJs})`,
      qterm(K, `\\${other}(${u})`),
      `${K.js()}*${other}(${uJs})`,
      [intro, `Substitute: ${m(qterm(q(s, a), `\\int \\${fn} u\\,du`))}`, m(`= ${qterm(K, `\\${other}(${u})`)} + C`)],
      "usub-linear"
    );
  }
  if (kind === "recip") {
    const K = q(s, a);
    return integral(
      `\\frac{${s}}{${u}}`,
      `(${s})/${uJs}`,
      qterm(K, `\\ln|${u}|`),
      `${K.js()}*log(abs(${uJs}))`,
      [intro, `Substitute: ${m(`${qterm(K, "\\int \\frac{du}{u}")} = ${qterm(K, "\\ln|u|")} + C`)}`, m(`= ${qterm(K, `\\ln|${u}|`)} + C`)],
      "usub-linear"
    );
  }
  const p = r.pick([2, 3, -2, -3]);
  const K = q(s, a * (p + 1));
  const Ftex = p + 1 === -1 ? coefOver(K, "", P(u)) : p + 1 < 0 ? coefOver(K, "", `${P(u)}^{${-(p + 1)}}`) : qterm(K, `${P(u)}^{${p + 1}}`);
  return integral(
    p > 0 ? `${ct(s, `${P(u)}^{${p}}`)}` : `\\frac{${s}}{${P(u)}^{${-p}}}`,
    `(${s})*${uJs}^(${p})`,
    Ftex,
    `${K.js()}*${uJs}^(${p + 1})`,
    [intro, `Substitute: ${m(qterm(q(s, a), `\\int u^{${p}}\\,du`))}`, `Power rule and back-substitute: ${m(`${Ftex} + C`)}`],
    "usub-linear"
  );
}

// ═══════════════════════════════════════════════════════════════════════════
// calc.by-parts
// ═══════════════════════════════════════════════════════════════════════════
const PARTS = `Parts: ${m("\\int u\\,dv = uv - \\int v\\,du")}`;

function partsXExp(r: Rng): Draft {
  // ∫ (cx + d) e^{ax} dx = e^{ax} [ (c/a) x + d/a - c/a^2 ]
  const a = r.pick([1, 2, 3, -1, -2]);
  const c = r.nz(-3, 4);
  const d = r.chance(0.4) ? 0 : r.nz(-4, 4);
  const poly = join([ct(c, "x"), d ? `${d}` : ""]);
  const polyJ = `((${c})*x + (${d}))`;
  const q1 = q(c, a);
  const q0 = q(d, a).sub(q(c, a * a));
  const inner = sumTex([tm(q1, "x", "x"), tm(q0, "", "")]);
  const ea = eTex(a);
  const Ftex = q0.isZero() ? qterm(q1, `x${ea}`) : `${P(inner)}${ea}`;
  const Fjs = `${eJs(a)}*(${q1.js()}*x + ${q0.js()})`;
  return integral(
    d === 0 ? `${ct(c, "x")}${ea}` : `${P(poly)}${ea}`,
    `${polyJ}*${eJs(a)}`,
    Ftex,
    Fjs,
    [
      `${PARTS} with ${m(`u = ${poly}`)}, ${m(`dv = ${ea}\\,dx`)}: ${m(`du = ${c}\\,dx`)}, ${m(`v = ${qterm(q(1, a), ea)}`)}.`,
      m(`\\int = ${qterm(q(1, a), `${P(poly)}${ea}`)} - ${P(qterm(q(c, a), `\\int ${ea}\\,dx`))}`),
      `${m(`\\int ${ea}\\,dx = ${qterm(q(1, a), ea)}`)}, so ${m(`\\int = ${Ftex} + C`)}`,
    ],
    "parts-x-exp"
  );
}

function partsXTrig(r: Rng): Draft {
  const k = r.pick([1, 2, 3, 4]);
  const c = r.nz(-3, 3);
  const d = r.chance(0.5) ? 0 : r.nz(-3, 3);
  const fn = r.pick(["sin", "cos"]);
  const poly = join([ct(c, "x"), d ? `${d}` : ""]);
  const polyJ = `((${c})*x + (${d}))`;
  // sin: -(cx+d)cos(kx)/k + c sin(kx)/k^2 ;  cos: (cx+d) sin(kx)/k + c cos(kx)/k^2
  const other = fn === "sin" ? "cos" : "sin";
  const s1 = fn === "sin" ? -1 : 1;
  const first: Tm = d === 0 ? tm(q(s1 * c, k), `x${trig(other, k)}`, `x*${trigJs(other, k)}`) : tm(q(s1, k), `${P(poly)}${trig(other, k)}`, `${polyJ}*${trigJs(other, k)}`);
  const second = tm(q(c, k * k), trig(fn, k), trigJs(fn, k));
  const F = [first, second];
  const vTex = qterm(q(s1, k), trig(other, k));
  return integral(
    d === 0 ? `${ct(c, "x")}${trig(fn, k)}` : `${P(poly)}${trig(fn, k)}`,
    `${polyJ}*${trigJs(fn, k)}`,
    sumTex(F),
    sumJs(F),
    [
      `${PARTS} with ${m(`u = ${poly}`)}, ${m(`dv = ${trig(fn, k)}\\,dx`)}: ${m(`du = ${c}\\,dx`)}, ${m(`v = ${vTex}`)}.`,
      m(`\\int = ${sumTex([first])} - ${P(qterm(q(s1 * c, k), `\\int ${trig(other, k)}\\,dx`))}`),
      `Integrate the rest: ${m(`\\int = ${sumTex(F)} + C`)}`,
    ],
    "parts-x-trig"
  );
}

/** q·x^p·tail with negative powers moved into a denominator */
function xpowTerm(c: Q, p: number, tail: string): string {
  if (p >= 0) {
    const body = xp(p) + tail;
    return body ? qterm(c, body) : c.tex();
  }
  return coefOver(c, tail, xp(-p));
}

function partsLog(r: Rng): Draft {
  // ∫ c x^n ln x dx = c x^{n+1}/(n+1) ln x - c x^{n+1}/(n+1)^2
  const n = r.pick([0, 1, 2, 3, -2, -3]);
  const c = r.chance(0.5) ? Math.abs(n + 1) * r.pick([1, 2]) : r.pick([1, 2, 3]);
  const a = q(c, n + 1);
  const b = q(-c, (n + 1) * (n + 1));
  const Ftex = join([xpowTerm(a, n + 1, "\\ln x"), xpowTerm(b, n + 1, "")]);
  const Fjs = `${a.js()}*x^(${n + 1})*log(x) + ${b.js()}*x^(${n + 1})`;
  const integrand = n >= 0 ? ct(c, `${xp(n)}\\ln x`) : `\\frac{${ct(c, "\\ln x")}}{${xp(-n)}}`;
  const v = xpowTerm(q(1, n + 1), n + 1, "");
  return integral(
    integrand,
    `(${c})*x^(${n})*log(x)`,
    Ftex,
    Fjs,
    [
      `${PARTS} with ${m("u = \\ln x")} (it simplifies when differentiated), ${m(`dv = ${n === 0 ? "" : n > 0 ? xp(n) : `x^{${n}}`}\\,dx`)}: ${m("du = \\frac{dx}{x}")}, ${m(`v = ${v}`)}.`,
      m(`\\int = ${join([xpowTerm(a, n + 1, "\\ln x"), qterm(a.neg(), `\\int ${n === 0 ? "1" : n > 0 ? xp(n) : `x^{${n}}`}\\,dx`)])}`),
      m(`= ${Ftex} + C`),
    ],
    "parts-x-log"
  );
}

function partsTabular(r: Rng): Draft {
  // x^2 times e^{ax}, cos(kx) or sin(kx): integrate by parts twice
  const c = r.pick([1, 1, 2, 3, -1]);
  const kind = r.pick(["exp", "exp", "sin", "cos"]);
  if (kind === "exp") {
    const a = r.pick([1, -1, 2, -2]);
    const ea = eTex(a);
    const F = [tm(q(c, a), "x^{2}", "x^2"), tm(q(-2 * c, a * a), "x", "x"), tm(q(2 * c, a * a * a), "", "")];
    const Ftex = `${P(sumTex(F))}${ea}`;
    return integral(
      `${ct(c, "x^{2}")}${ea}`,
      `(${c})*x^2*${eJs(a)}`,
      Ftex,
      `${eJs(a)}*(${sumJs(F)})`,
      [
        `${PARTS} twice (tabular): differentiate ${m(ct(c, "x^{2}"))} ${m(`\\to ${2 * c}x \\to ${2 * c} \\to 0`)}; integrate ${m(ea)} three times.`,
        `Alternate signs ${m("+, -, +")}: ${m(`${ct(c, "x^{2}")}\\cdot ${par(qterm(q(1, a), ea))} - ${par(`${2 * c}x`)}\\cdot ${par(qterm(q(1, a * a), ea))} + ${par(`${2 * c}`)}\\cdot ${par(qterm(q(1, a * a * a), ea))}`)}`,
        `Factor ${m(ea)}: ${m(`${Ftex} + C`)}`,
      ],
      "parts-tabular"
    );
  }
  const k = r.pick([1, 2, 3]);
  // cos: x^2 sin/k + 2x cos/k^2 - 2 sin/k^3 ;  sin: -x^2 cos/k + 2x sin/k^2 + 2 cos/k^3
  const F =
    kind === "cos"
      ? [
          tm(q(c, k), `x^{2}${trig("sin", k)}`, `x^2*${trigJs("sin", k)}`),
          tm(q(2 * c, k * k), `x${trig("cos", k)}`, `x*${trigJs("cos", k)}`),
          tm(q(-2 * c, k * k * k), trig("sin", k), trigJs("sin", k)),
        ]
      : [
          tm(q(-c, k), `x^{2}${trig("cos", k)}`, `x^2*${trigJs("cos", k)}`),
          tm(q(2 * c, k * k), `x${trig("sin", k)}`, `x*${trigJs("sin", k)}`),
          tm(q(2 * c, k * k * k), trig("cos", k), trigJs("cos", k)),
        ];
  return integral(
    `${ct(c, "x^{2}")}${trig(kind, k)}`,
    `(${c})*x^2*${trigJs(kind, k)}`,
    sumTex(F),
    sumJs(F),
    [
      `${PARTS} twice (tabular): differentiate ${m(ct(c, "x^{2}"))} down to ${m("0")}, integrate ${m(trig(kind, k))} three times.`,
      `Antiderivatives of ${m(trig(kind, k))}: ${m(kind === "cos" ? `${qterm(q(1, k), trig("sin", k))},\\ ${qterm(q(-1, k * k), trig("cos", k))},\\ ${qterm(q(-1, k * k * k), trig("sin", k))}` : `${qterm(q(-1, k), trig("cos", k))},\\ ${qterm(q(-1, k * k), trig("sin", k))},\\ ${qterm(q(1, k * k * k), trig("cos", k))}`)}`,
      `Multiply diagonally with signs ${m("+, -, +")}: ${m(`${sumTex(F)} + C`)}`,
    ],
    "parts-tabular"
  );
}

function partsExpTrig(r: Rng): Draft {
  // ∫ e^{ax} sin(bx) = e^{ax}(a sin bx - b cos bx)/(a^2+b^2); cos: e^{ax}(a cos bx + b sin bx)/(a^2+b^2)
  const a = r.pick([1, 2, 3, -1, -2]);
  const b = r.pick([1, 2, 3]);
  const fn = r.pick(["sin", "cos"]);
  const D = a * a + b * b;
  const s = r.chance(0.5) ? D : 1;
  const K = q(s, D);
  const inner =
    fn === "sin" ? join([ct(a, trig("sin", b)), ct(-b, trig("cos", b))]) : join([ct(a, trig("cos", b)), ct(b, trig("sin", b))]);
  const innerJs =
    fn === "sin" ? `(${a})*${trigJs("sin", b)} - (${b})*${trigJs("cos", b)}` : `(${a})*${trigJs("cos", b)} + (${b})*${trigJs("sin", b)}`;
  const ea = eTex(a);
  const Ftex = qterm(K, `${ea}${P(inner)}`);
  return integral(
    `${ct(s, ea)}${trig(fn, b)}`,
    `(${s})*${eJs(a)}*${trigJs(fn, b)}`,
    Ftex,
    `${K.js()}*${eJs(a)}*(${innerJs})`,
    [
      `Call the integral ${m("I")}. ${PARTS} twice, both times with ${m(`u = `)}the trig factor and ${m(`dv = ${ea}\\,dx`)}.`,
      `The second round gives back ${m("I")}: ${m(`I = ${join([
        qterm(q(1, a), `${ea}${trig(fn, b)}`),
        qterm(q(fn === "sin" ? -b : b, a * a), `${ea}${trig(fn === "sin" ? "cos" : "sin", b)}`),
        qterm(q(-b * b, a * a), "I"),
      ])}`)}`,
      `Solve for ${m("I")}: multiply by ${m(`\\frac{${a * a}}{${D}}`)}, so ${m(`\\int ${ea}${trig(fn, b)}\\,dx = ${qterm(q(1, D), `${ea}${P(inner)}`)}`)}`,
      ...(s === 1 ? [] : [`Times ${m(`${s}`)}: ${m(`${Ftex} + C`)}`]),
    ],
    "parts-exp-trig"
  );
}

function partsInverse(r: Rng): Draft {
  if (r.chance(0.3)) {
    // ∫ arcsin x dx = x arcsin x + sqrt(1 - x^2)
    const c = r.pick([1, 2, 3]);
    const F = [tm(c, "x\\arcsin x", "x*asin(x)"), tm(c, "\\sqrt{1 - x^{2}}", "sqrt(1 - x^2)")];
    return integral(
      ct(c, "\\arcsin x"),
      `(${c})*asin(x)`,
      sumTex(F),
      sumJs(F),
      [
        `${PARTS} with ${m("u = \\arcsin x")}, ${m("dv = dx")}: ${m("du = \\frac{dx}{\\sqrt{1 - x^2}}")}, ${m("v = x")}.`,
        m(`\\int \\arcsin x\\,dx = x\\arcsin x - \\int \\frac{x}{\\sqrt{1 - x^2}}\\,dx`),
        `Substitute ${m("w = 1 - x^2")}: ${m("\\int \\frac{x\\,dx}{\\sqrt{1 - x^2}} = -\\sqrt{1 - x^2}")}, so ${m(`${ct(c, "")}\\int = ${sumTex(F)} + C`.replace(/^1\\int/, "\\int"))}`,
      ],
      "parts-inverse"
    );
  }
  // ∫ c arctan(kx) dx = c x arctan(kx) - c ln(1 + k^2x^2)/(2k)
  const k = r.pick([1, 2, 3]);
  const c = r.pick([1, 2, 3, 4]);
  const at = k === 1 ? "\\arctan x" : `\\arctan(${k}x)`;
  const atJs = `atan((${k})*x)`;
  const inside = k === 1 ? "1 + x^{2}" : `1 + ${k * k}x^{2}`;
  const F = [tm(c, `x${at}`, `x*${atJs}`), tm(q(-c, 2 * k), `\\ln(${inside})`, `log(1 + ${k * k}*x^2)`)];
  return integral(
    ct(c, at),
    `(${c})*${atJs}`,
    sumTex(F),
    sumJs(F),
    [
      `${PARTS} with ${m(`u = ${at}`)}, ${m("dv = dx")}: ${m(`du = \\frac{${k}}{${inside}}\\,dx`)}, ${m("v = x")}.`,
      m(`\\int ${at}\\,dx = x${at} - \\int \\frac{${ct(k, "x")}}{${inside}}\\,dx`),
      `u-substitute ${m(`w = ${inside}`)}: ${m(`\\int \\frac{${ct(k, "x")}}{${inside}}\\,dx = ${qterm(q(1, 2 * k), `\\ln(${inside})`)}`)}`,
      `Times ${m(`${c}`)}: ${m(`${sumTex(F)} + C`)}`,
    ],
    "parts-inverse"
  );
}

// ═══════════════════════════════════════════════════════════════════════════
// calc.partial-fractions
// ═══════════════════════════════════════════════════════════════════════════
function rationalTex(num: Poly, den: string) {
  return `\\frac{${polyTex(num)}}{${den}}`;
}

function pfDistinct(r: Rng): Draft {
  const a = r.int(-4, 4);
  const b = r.int(-4, 4);
  require_(a < b);
  const A = r.nz(-4, 4);
  const B = r.nz(-4, 4);
  const num = padd(pscale(root1(b), A), pscale(root1(a), B));
  const den = pmul(root1(a), root1(b));
  const F = [tm(A, lnAbs(a), lnAbsJs(a)), tm(B, lnAbs(b), lnAbsJs(b))];
  return integral(
    rationalTex(num, polyTex(den)),
    `(${polyJs(num)})/(${polyJs(den)})`,
    sumTex(F),
    sumJs(F),
    [
      `Factor: ${m(`${polyTex(den)} = ${xrFac(a)}${xrFac(b)}`)}, so write ${m(`\\frac{A}{${xr(a)}} + \\frac{B}{${xr(b)}}`)}.`,
      `Cover-up: ${m(`A = \\frac{${peval(num, a)}}{${a - b}} = ${A}`)} (at ${m(`x = ${a}`)}), ${m(`B = \\frac{${peval(num, b)}}{${b - a}} = ${B}`)} (at ${m(`x = ${b}`)}).`,
      `Each piece integrates to a log: ${m(`${sumTex(F)} + C`)}`,
    ],
    "pf-distinct"
  );
}

function pfRepeated(r: Rng): Draft {
  // A/(x-a) + B/(x-a)^2 + D/(x-b)
  const a = r.int(-3, 3);
  const b = r.int(-3, 3);
  require_(a !== b);
  const A = r.int(-3, 3);
  const B = r.nz(-4, 4);
  const D = r.nz(-3, 3);
  const num = padd(pscale(pmul(root1(a), root1(b)), A), pscale(root1(b), B), pscale(pmul(root1(a), root1(a)), D));
  const sq = a === 0 ? "x^{2}" : `${P(xr(a))}^{2}`;
  const den = a === 0 ? `x^{2}${xrFac(b)}` : b === 0 ? `x${sq}` : `${sq}${xrFac(b)}`;
  const denJs = `${xrJs(a)}^2*${xrJs(b)}`;
  const F = [tm(A, lnAbs(a), lnAbsJs(a)), tm(D, lnAbs(b), lnAbsJs(b))];
  const recip = coefOver(q(-B), "", xr(a));
  const Ftex = join([sumTex([F[0]]) === "0" ? "" : sumTex([F[0]]), recip, sumTex([F[1]])]);
  const Fjs = `${sumJs(F)} + (${-B})/${xrJs(a)}`;
  return integral(
    rationalTex(num, den),
    `(${polyJs(num)})/(${denJs})`,
    Ftex,
    Fjs,
    [
      `Repeated factor: ${m(`\\frac{A}{${xr(a)}} + \\frac{B}{${P(xr(a))}^{2}} + \\frac{D}{${xr(b)}}`)}.`,
      `Cover-up at ${m(`x = ${a}`)}: ${m(`B = \\frac{${peval(num, a)}}{${a - b}} = ${B}`)}; at ${m(`x = ${b}`)}: ${m(`D = \\frac{${peval(num, b)}}{${(b - a) ** 2}} = ${D}`)}.`,
      `Compare ${m("x^2")} coefficients: ${m(`A + D = ${num[2] ?? 0}`)}, so ${m(`A = ${A}`)}.`,
      `Integrate (${m(`\\int \\frac{dx}{(x - a)^2} = -\\frac{1}{x - a}`)}): ${m(`${Ftex} + C`)}`,
    ],
    "pf-repeated"
  );
}

function pfThree(r: Rng): Draft {
  const roots = [r.int(-3, 3), r.int(-3, 3), r.int(-3, 3)].sort((u, v) => u - v);
  require_(roots[0] < roots[1] && roots[1] < roots[2]);
  const [a, b, c] = roots;
  const co = [r.nz(-3, 3), r.nz(-3, 3), r.nz(-3, 3)];
  const num = padd(pscale(pmul(root1(b), root1(c)), co[0]), pscale(pmul(root1(a), root1(c)), co[1]), pscale(pmul(root1(a), root1(b)), co[2]));
  const den = roots.map(xrFac).join("");
  const denJs = roots.map(xrJs).join("*");
  const F = roots.map((rt, i) => tm(co[i], lnAbs(rt), lnAbsJs(rt)));
  const cover = roots.map((rt, i) => {
    const others = roots.filter((_, j) => j !== i);
    const d = (rt - others[0]) * (rt - others[1]);
    return m(`${"ABD"[i]} = \\frac{${peval(num, rt)}}{${d}} = ${co[i]}`);
  });
  return integral(
    rationalTex(num, den),
    `(${polyJs(num)})/(${denJs})`,
    sumTex(F),
    sumJs(F),
    [
      `Three distinct linear factors: ${m(`\\frac{A}{${xr(a)}} + \\frac{B}{${xr(b)}} + \\frac{D}{${xr(c)}}`)}.`,
      `Cover-up at ${m(`x = ${a}, ${b}, ${c}`)}: ${cover.join(", ")}.`,
      `Integrate: ${m(`${sumTex(F)} + C`)}`,
    ],
    "pf-three"
  );
}

function pfIrreducible(r: Rng): Draft {
  // A/(x-a) + (Bx + D)/(x^2 + k^2)
  const a = r.int(-3, 3);
  const k = r.pick([1, 2, 3]);
  const A = r.nz(-3, 3);
  const B = r.pick([-4, -2, 2, 4, 1, -1, 0]);
  const D = k * r.int(-2, 2);
  require_(B !== 0 || D !== 0);
  const quad: Poly = [k * k, 0, 1];
  const num = padd(pscale(quad, A), pmul([D, B], root1(a)));
  const qt = `x^{2} + ${k * k}`;
  const den = `${xrFac(a)}(${qt})`;
  const atan = k === 1 ? "\\arctan x" : `\\arctan\\frac{x}{${k}}`;
  const F = [
    tm(A, lnAbs(a), lnAbsJs(a)),
    tm(q(B, 2), `\\ln(${qt})`, `log(x^2 + ${k * k})`),
    tm(q(D, k), atan, `atan(x/${k})`),
  ];
  return integral(
    rationalTex(num, den),
    `(${polyJs(num)})/(${xrJs(a)}*(x^2 + ${k * k}))`,
    sumTex(F),
    sumJs(F),
    [
      `Irreducible quadratic gets a linear numerator: ${m(`\\frac{A}{${xr(a)}} + \\frac{Bx + D}{${qt}}`)}.`,
      `Cover-up at ${m(`x = ${a}`)}: ${m(`A = \\frac{${peval(num, a)}}{${a * a + k * k}} = ${A}`)}. Compare ${m("x^2")} and constant terms: ${m(`B = ${B}`)}, ${m(`D = ${D}`)}.`,
      `${m(`\\int \\frac{x}{${qt}}dx = \\frac{1}{2}\\ln(${qt})`)}, ${m(`\\int \\frac{dx}{${qt}} = ${qterm(q(1, k), atan)}`)}.`,
      m(`${sumTex(F)} + C`),
    ],
    "pf-irreducible"
  );
}

function pfImproper(r: Rng): Draft {
  // s(x-a)(x-b) + A(x-b) + B(x-a) over (x-a)(x-b) = s + A/(x-a) + B/(x-b)
  const a = r.int(-4, 4);
  const b = r.int(-4, 4);
  require_(a < b);
  const s = r.pick([1, 1, 2, 3]);
  const A = r.nz(-4, 4);
  const B = r.nz(-4, 4);
  const den = pmul(root1(a), root1(b));
  const num = padd(pscale(den, s), pscale(root1(b), A), pscale(root1(a), B));
  const F = [tm(s, "x", "x"), tm(A, lnAbs(a), lnAbsJs(a)), tm(B, lnAbs(b), lnAbsJs(b))];
  const rem = padd(num, pscale(den, -s));
  return integral(
    rationalTex(num, polyTex(den)),
    `(${polyJs(num)})/(${polyJs(den)})`,
    sumTex(F),
    sumJs(F),
    [
      `Degree on top = degree below: divide first. ${m(`\\frac{${polyTex(num)}}{${polyTex(den)}} = ${s} + \\frac{${polyTex(rem)}}{${polyTex(den)}}`)}`,
      `Split the remainder over ${m(`${xrFac(a)}${xrFac(b)}`)}: ${m(`A = ${A}`)}, ${m(`B = ${B}`)} (cover-up).`,
      `Integrate: ${m(`${sumTex(F)} + C`)}`,
    ],
    "pf-improper"
  );
}

function pfCoeffs(r: Rng): Draft {
  const a = r.int(-5, 5);
  const b = r.int(-5, 5);
  require_(a < b);
  const A = r.nz(-5, 5);
  const B = r.nz(-5, 5);
  const num = padd(pscale(root1(b), A), pscale(root1(a), B));
  const den = pmul(root1(a), root1(b));
  return {
    prompt: `Find ${m("A")} and ${m("B")}: ${m(`\\frac{${polyTex(num)}}{${polyTex(den)}} = \\frac{A}{${xr(a)}} + \\frac{B}{${xr(b)}}`)}`,
    answer: {
      kind: "tuple",
      fields: [
        { label: "A", tex: "A", ref: `${A}`, mode: "number" },
        { label: "B", tex: "B", ref: `${B}`, mode: "number" },
      ],
      vars: [],
    },
    answerTex: `A = ${A},\\quad B = ${B}`,
    steps: [
      `Multiply through by ${m(`${xrFac(a)}${xrFac(b)}`)}: ${m(`${polyTex(num)} = A${xrFac(b)} + B${xrFac(a)}`)}.`,
      `${m(`x = ${a}`)}: ${m(`${peval(num, a)} = ${a - b}A`)}, so ${m(`A = ${A}`)}.`,
      `${m(`x = ${b}`)}: ${m(`${peval(num, b)} = ${b - a}B`)}, so ${m(`B = ${B}`)}.`,
    ],
    meta: { variant: "pf-coeffs", num, a, b },
  };
}

// ═══════════════════════════════════════════════════════════════════════════
// calc.complex-euler   (Kreyszig §2.2: complex roots, e^{iθ} = cos θ + i sin θ)
// ═══════════════════════════════════════════════════════════════════════════
/** exact cos of t·π/12, t integer:  value = c·√rad */
function cos12(t: number): [Q, number] {
  t = ((t % 24) + 24) % 24;
  if (t > 12) t = 24 - t;
  const T: Record<number, [Q, number]> = {
    0: [q(1), 1], 2: [q(1, 2), 3], 3: [q(1, 2), 2], 4: [q(1, 2), 1], 6: [q(0), 1],
    8: [q(-1, 2), 1], 9: [q(-1, 2), 2], 10: [q(-1, 2), 3], 12: [q(-1), 1],
  };
  return T[t];
}
const sin12 = (t: number) => cos12(6 - t);
const surd = (c: Q, rad: number) => (rad === 1 ? c.tex() : qterm(c, `\\sqrt{${rad}}`));
const surdJs = (c: Q, rad: number) => (rad === 1 ? c.js() : `${c.js()}*sqrt(${rad})`);
/** a + bi, LaTeX, with b = c·√rad */
function complexTex(re: Q, reRad: number, im: Q, imRad: number): string {
  const imBody = imRad === 1 ? "i" : `\\sqrt{${imRad}}\\,i`;
  return join([re.isZero() ? "" : surd(re, reRad), im.isZero() ? "" : qterm(im, imBody)]);
}
/** angle t·π/12 as LaTeX, e.g. \frac{2\pi}{3} */
function angTex(t: number): string {
  const a = q(t, 12);
  if (a.isZero()) return "0";
  const n = Math.abs(a.n);
  const sign = a.n < 0 ? "-" : "";
  const top = n === 1 ? "\\pi" : `${n}\\pi`;
  return a.d === 1 ? `${sign}${top}` : `${sign}\\frac{${top}}{${a.d}}`;
}
/** exponent i·t·π/12, e.g. 2\pi i/3 */
function iAngTex(t: number): string {
  const a = q(t, 12);
  const n = Math.abs(a.n);
  const sign = a.n < 0 ? "-" : "";
  return `${sign}${n === 1 ? "" : n}\\pi i${a.d === 1 ? "" : `/${a.d}`}`;
}
const NICE_T = [2, 3, 4, 6, 8, 9, 10, 12, -2, -3, -4, -6, -8, -9, -10];

function complexRect(r: Rng): Draft {
  const t = r.pick(NICE_T);
  const den = q(t, 12).d;
  const R = den <= 2 ? r.pick([1, 2, 3, 5]) : r.pick([2, 4, 6]);
  const [cc, cr] = cos12(t);
  const [sc, sr] = sin12(t);
  const re = cc.mul(R), im = sc.mul(R);
  const z = complexTex(re, cr, im, sr) || "0";
  return {
    prompt: `Write ${m(`${R === 1 ? "" : R}e^{${iAngTex(t)}}`)} in the form ${m("a + bi")}.`,
    answer: {
      kind: "tuple",
      fields: [
        { label: "a", tex: "a", ref: surdJs(re, cr), mode: "number" },
        { label: "b", tex: "b", ref: surdJs(im, sr), mode: "number" },
      ],
      vars: [],
    },
    answerTex: z,
    steps: [
      `Euler: ${m("re^{i\\theta} = r(\\cos\\theta + i\\sin\\theta)")} with ${m(`r = ${R}`)}, ${m(`\\theta = ${angTex(t)}`)}.`,
      `${m(`\\cos ${par(angTex(t))} = ${surd(cc, cr)}`)}, ${m(`\\sin ${par(angTex(t))} = ${surd(sc, sr)}`)}.`,
      `Multiply by ${m(`${R}`)}: ${m(`${z}`)}, so ${m(`a = ${surd(re, cr)},\\ b = ${surd(im, sr)}`)}.`,
    ],
    meta: { variant: "euler-rect", R, t },
  };
}

function complexPolar(r: Rng): Draft {
  const t = r.pick(NICE_T);
  const den = q(t, 12).d;
  const R = den <= 2 ? r.pick([1, 2, 3, 5]) : r.pick([2, 4, 6]);
  const [cc, cr] = cos12(t);
  const [sc, sr] = sin12(t);
  const re = cc.mul(R), im = sc.mul(R);
  const z = complexTex(re, cr, im, sr);
  const ang = q(t, 12);
  return {
    prompt: `Write ${m(`z = ${z}`)} in polar form ${m("z = re^{i\\theta}")}: give ${m("r = |z|")} and an argument ${m("\\theta")}.`,
    answer: {
      kind: "tuple",
      fields: [
        { label: "r", tex: "r", ref: `${R}`, mode: "number" },
        { label: "θ", tex: "\\theta", ref: `(${ang.n})*pi/${ang.d}`, mode: "angle" },
      ],
      vars: [],
    },
    answerTex: `r = ${R},\\quad \\theta = ${angTex(t)}`,
    steps: [
      `${m(`r = \\sqrt{a^2 + b^2} = \\sqrt{${re.mul(re).mul(cr).tex()} + ${im.mul(im).mul(sr).tex()}} = ${R}`)}.`,
      `${m(`\\cos\\theta = a/r = ${surd(cc, cr)}`)}, ${m(`\\sin\\theta = b/r = ${surd(sc, sr)}`)}: read the quadrant from the signs of ${m("a")} and ${m("b")}, not from ${m("\\arctan(b/a)")} alone.`,
      `${m(`\\theta = ${angTex(t)}`)} (any ${m("\\theta + 2\\pi k")} is the same point), so ${m(`z = ${R === 1 ? "" : R}e^{${iAngTex(t)}}`)}.`,
    ],
    meta: { variant: "euler-polar", R, t, re: surdJs(re, cr), im: surdJs(im, sr) },
  };
}

function complexDeMoivre(r: Rng): Draft {
  // z = a + b√s i with a, b = ±1, s ∈ {1, 3};  z^n by De Moivre
  const s = r.pick([1, 3]);
  const a0 = r.pick([1, -1]);
  const b0 = r.pick([1, -1]);
  const n = s === 1 ? r.int(2, 6) : r.int(2, 4);
  let [a, b] = [a0, b0];
  for (let i = 1; i < n; i++) [a, b] = [a * a0 - s * b * b0, a * b0 + b * a0];
  // argument in units of π/12
  const base = s === 1 ? 3 : 4; // π/4 or π/3
  const tq = a0 > 0 ? base : 12 - base;
  const t0 = b0 > 0 ? tq : -tq;
  const mod = s === 1 ? "\\sqrt{2}" : "2";
  const modN = s === 1 ? (n % 2 === 0 ? `${2 ** (n / 2)}` : `${2 ** ((n - 1) / 2) === 1 ? "" : 2 ** ((n - 1) / 2)}\\sqrt{2}`) : `${2 ** n}`;
  let tn = (t0 * n) % 24;
  if (tn > 12) tn -= 24;
  if (tn <= -12) tn += 24;
  const zTex = complexTex(q(a0), 1, q(b0), s);
  const res = complexTex(q(a), 1, q(b), s) || "0";
  return {
    prompt: `Use De Moivre's formula to write ${m(`${P(zTex)}^{${n}}`)} in the form ${m("a + bi")}.`,
    answer: {
      kind: "tuple",
      fields: [
        { label: "a", tex: "a", ref: `${a}`, mode: "number" },
        { label: "b", tex: "b", ref: s === 1 ? `${b}` : `${b}*sqrt(3)`, mode: "number" },
      ],
      vars: [],
    },
    answerTex: res,
    steps: [
      `Polar form: ${m(`|z| = ${mod}`)}, ${m(`\\arg z = ${angTex(t0)}`)}, so ${m(`z = ${mod}\\,e^{${iAngTex(t0)}}`)}.`,
      `De Moivre: ${m(`z^{${n}} = ${P(mod)}^{${n}} e^{${iAngTex(t0 * n)}} = ${modN}\\,e^{${tn === 0 ? "0" : iAngTex(tn)}}`)}.`,
      `Euler: ${m(`${modN}\\left(\\cos ${P(angTex(tn))} + i\\sin ${P(angTex(tn))}\\right) = ${res}`)}.`,
    ],
    meta: { variant: "euler-demoivre", a0, b0, s, n },
  };
}

function complexQuadRoots(r: Rng): Draft {
  // λ² + Bλ + C = 0 with roots α ± βi
  const al = r.int(-4, 4);
  const be = r.int(1, 5);
  const B = -2 * al, C = al * al + be * be;
  const eq = join(["\\lambda^{2}", ct(B, "\\lambda"), `${C}`]) + " = 0";
  return {
    prompt: `Solve ${m(eq)}. Its roots are ${m("\\lambda = \\alpha \\pm \\beta i")} with ${m("\\beta > 0")}: give ${m("\\alpha")} and ${m("\\beta")}.`,
    answer: {
      kind: "tuple",
      fields: [
        { label: "α", tex: "\\alpha", ref: `${al}`, mode: "number" },
        { label: "β", tex: "\\beta", ref: `${be}`, mode: "number" },
      ],
      vars: [],
    },
    answerTex: `\\lambda = ${al === 0 ? "" : al} \\pm ${be === 1 ? "" : be}i`,
    steps: [
      `Quadratic formula: ${m(`\\lambda = \\frac{${-B} \\pm \\sqrt{${B * B} - ${4 * C}}}{2}`)}`,
      `${m(`${B * B - 4 * C} < 0`)}: ${m(`\\sqrt{${B * B - 4 * C}} = ${2 * be}i`)} (since ${m(`\\sqrt{-k} = i\\sqrt{k}`)}).`,
      m(`\\lambda = ${al} \\pm ${be}i`),
    ],
    meta: { variant: "euler-quad", B, C, al, be },
  };
}

function complexReIm(r: Rng): Draft {
  const al = r.int(-3, 3);
  const be = r.int(1, 4);
  const eAl = al === 0 ? "" : eTex(al);
  const eAlJs = al === 0 ? "1" : eJs(al);
  const bx = be === 1 ? "x" : `${be}x`;
  const expo = al === 0 ? (be === 1 ? "ix" : `${be}ix`) : `(${al} ${"+"} ${be === 1 ? "" : be}i)x`;
  if (r.chance(0.5)) {
    return {
      prompt: `Write ${m(`e^{${expo}}`)} as ${m("u(x) + i\\,v(x)")} with ${m("u, v")} real.`,
      answer: {
        kind: "tuple",
        fields: [
          { label: "u", tex: "u(x)", ref: `${eAlJs}*cos((${be})*x)`, mode: "expr" },
          { label: "v", tex: "v(x)", ref: `${eAlJs}*sin((${be})*x)`, mode: "expr" },
        ],
        vars: ["x"],
      },
      answerTex: `${eAl}\\cos ${bx} + i\\,${eAl}\\sin ${bx}`,
      steps: [
        ...(al === 0 ? [] : [`Split the exponent: ${m(`e^{${expo}} = ${eAl}\\,e^{${be === 1 ? "" : be}ix}`)}.`]),
        `Euler: ${m(`e^{${be === 1 ? "" : be}ix} = \\cos ${bx} + i\\sin ${bx}`)}.`,
        `${m(`u = ${eAl}\\cos ${bx}`)}, ${m(`v = ${eAl}\\sin ${bx}`)}: these are the two real solutions for the roots ${m(`${al} \\pm ${be === 1 ? "" : be}i`)}.`,
      ],
      meta: { variant: "euler-reim", al, be },
    };
  }
  // (e^{(α+βi)x} ± e^{(α-βi)x}) / 2  or / 2i
  const plus = r.chance(0.5);
  const conj = al === 0 ? (be === 1 ? "-ix" : `-${be}ix`) : `(${al} - ${be === 1 ? "" : be}i)x`;
  return {
    prompt: `Simplify to a real function: ${m(`\\frac{e^{${expo}} ${plus ? "+" : "-"} e^{${conj}}}{${plus ? "2" : "2i"}}`)}`,
    answer: { kind: "expression", ref: `${eAlJs}*${plus ? "cos" : "sin"}((${be})*x)`, vars: ["x"] },
    answerTex: `${eAl}\\${plus ? "cos" : "sin"} ${bx}`,
    steps: [
      `Euler on both: ${m(`e^{\\pm ${be === 1 ? "" : be}ix} = \\cos ${bx} \\pm i\\sin ${bx}`)}${al === 0 ? "" : `, each times ${m(eAl)}`}.`,
      plus ? `Add: the ${m("\\sin")} terms cancel, leaving ${m(`2${eAl}\\cos ${bx}`)}.` : `Subtract: the ${m("\\cos")} terms cancel, leaving ${m(`2i${eAl}\\sin ${bx}`)}.`,
      `Divide by ${m(plus ? "2" : "2i")}: ${m(`${eAl}\\${plus ? "cos" : "sin"} ${bx}`)}`,
    ],
    meta: { variant: "euler-combine", al, be, plus },
  };
}

// ═══════════════════════════════════════════════════════════════════════════
// calc.sigma-shift   (Kreyszig §5.1: shifting summation indices)
// ═══════════════════════════════════════════════════════════════════════════
/** coefficient families b(index), index = v + off; tex as numerator/denominator */
interface BFam {
  num: (v: string, off: number) => string;
  den: (v: string, off: number) => string;
  js: (v: string, off: number) => string;
}
const B_FAMS: BFam[] = [
  { num: (v, o) => `2^{${lin(v, o)}}`, den: () => "", js: (v, o) => `2^${linJs(v, o)}` },
  { num: (v, o) => `3^{${lin(v, o)}}`, den: () => "", js: (v, o) => `3^${linJs(v, o)}` },
  { num: () => "", den: (v, o) => lin(v, o + 1), js: (v, o) => `1/${linJs(v, o + 1)}` },
  { num: () => "", den: (v, o) => lin(v, o + 2), js: (v, o) => `1/${linJs(v, o + 2)}` },
  { num: () => "", den: (v, o) => `2^{${lin(v, o)}}`, js: (v, o) => `1/2^${linJs(v, o)}` },
];
/** polynomial factor ∏ (index + o_i) */
const pfac = (v: string, off: number, fs: number[]) =>
  fs.map((o) => lin(v, off + o)).map((s) => (s === v ? s : P(s))).join("");
const pfacJs = (v: string, off: number, fs: number[]) => fs.map((o) => linJs(v, off + o)).join("*") || "1";
/** c · P(index) · b(index) as LaTeX */
function coefTex(c: number, fs: number[], b: BFam, v: string, off: number): string {
  const den = b.den(v, off);
  const bare = den && fs.length === 1 && Math.abs(c) === 1;
  const p = bare ? lin(v, off + fs[0]) : pfac(v, off, fs);
  const num = `${p}${b.num(v, off)}`;
  if (den) return coefOver(q(c), num, den);
  if (!num) return `${c}`;
  return /^\d/.test(num) && Math.abs(c) !== 1 ? `${c}\\cdot ${num}` : ct(c, num);
}
const coefJs = (c: number, fs: number[], b: BFam, v: string, off: number) => `(${c})*${pfacJs(v, off, fs)}*${b.js(v, off)}`;
const xpow = (v: string, off: number) => (lin(v, off) === "0" ? "" : `x^{${lin(v, off)}}`);
const sumOf = (n0: number, body: string) => `\\sum_{n=${n0}}^{\\infty} ${body}`;

/** Σ_{n=n0} c P(n) b(n) x^{n + j} (times x^pre)  ->  Σ_{k=k0} c_k x^k */
function sigmaReindex(r: Rng, kind: "down" | "up" | "pre"): Draft {
  const b = r.pick(B_FAMS);
  const c = r.pick([1, 1, 2, 3, -1]);
  let fs: number[], n0: number, j: number, pre = 0;
  if (kind === "down") {
    j = -r.pick([1, 2]);
    fs = j === -1 ? r.pick([[0], [1]]) : r.pick([[0, -1], [0]]);
    n0 = -j + r.pick([0, 0, 1]);
  } else if (kind === "up") {
    j = r.pick([1, 2]);
    fs = r.pick([[], [0], [1]]);
    n0 = r.pick([0, 1]);
  } else {
    pre = r.pick([1, 2]);
    j = -r.pick([1, 2]);
    fs = j === -1 ? [0] : [0, -1];
    n0 = -j;
  }
  // the first term must not vanish, and no factor may cancel the 1/(n + c) of b
  require_(fs.every((o) => n0 + o !== 0) && !fs.some((o) => b.den("n", 0) === lin("n", o)));
  const shift = j + pre; // x^{n + shift} overall, so k = n + shift
  const k0 = n0 + shift;
  const body = `${coefTex(c, fs, b, "n", 0)}\\,${xpow("n", j)}`;
  const series = `${pre ? (pre === 1 ? "x" : `x^{${pre}}`) : ""}${sumOf(n0, body)}`;
  const ck = coefTex(c, fs, b, "k", -shift);
  const ckJs = coefJs(c, fs, b, "k", -shift);
  const what = pre ? `Bring ${m(pre === 1 ? "x" : `x^{${pre}}`)} inside: the power becomes ${m(`x^{${lin("n", shift)}}`)}.` : `The power is ${m(`x^{${lin("n", j)}}`)}.`;
  return {
    prompt: `Rewrite ${m(series)} as ${m("\\sum_{k=k_0}^{\\infty} c_k x^k")}: give ${m("k_0")} and ${m("c_k")}.`,
    answer: {
      kind: "tuple",
      fields: [
        { label: "k₀", tex: "k_0", ref: `${k0}`, mode: "number" },
        { label: "c_k", tex: "c_k", ref: ckJs, mode: "expr" },
      ],
      vars: ["k"],
    },
    answerTex: `\\sum_{k=${k0}}^{\\infty} ${coefTex(c, fs, b, "k", -shift)}\\,x^{k}`,
    steps: [
      `${what} Set ${m(`k = ${lin("n", shift)}`)}, i.e. ${m(`n = ${lin("k", -shift)}`)}.`,
      `Lower limit: ${m(`n = ${n0}`)} gives ${m(`k = ${k0}`)}.`,
      `Replace every ${m("n")} by ${m(lin("k", -shift))}: ${m(`c_k = ${ck}`)}.`,
    ],
    meta: { variant: "sigma-reindex", k0, sums: [{ coef: coefJs(c, fs, b, "n", 0), pow: shift, n0 }] },
  };
}

function sigmaDerivative(r: Rng): Draft {
  const b = r.pick(B_FAMS);
  const order = r.pick([1, 2]);
  const yTex = sumOf(0, `${coefTex(1, [], b, "n", 0)}\\,x^{n}`);
  const fs = order === 1 ? [0] : [0, -1];
  const ckJs = coefJs(1, fs, b, "k", order);
  const ck = coefTex(1, fs, b, "k", order);
  const d = order === 1 ? "y'" : "y''";
  return {
    prompt: `${m(`y = ${yTex}`)}. Write ${m(`${d} = \\sum_{k=0}^{\\infty} c_k x^k`)}: find ${m("c_k")}.`,
    answer: { kind: "expression", ref: ckJs, vars: ["k"], label: "c_k" },
    answerTex: `c_k = ${ck}`,
    steps: [
      `Differentiate term by term: ${m(`${d} = ${sumOf(order, `${coefTex(1, fs, b, "n", 0)}\\,${xpow("n", -order)}`)}`)} (the first ${order === 1 ? "term drops" : "two terms drop"} out).`,
      `Shift: ${m(`k = ${lin("n", -order)}`)}, so ${m(`n = ${lin("k", order)}`)} and the sum starts at ${m("k = 0")}.`,
      m(`c_k = ${ck}`),
    ],
    meta: { variant: "sigma-derivative", b: b.js("n", 0), order },
  };
}

function sigmaCombine(r: Rng): Draft {
  // Σ_{n=2} n(n-1) b_n x^{n-2}  - μ x Σ_{n=1} n b_n x^{n-1}  + λ Σ_{n=0} b_n x^n
  const b = r.pick(B_FAMS);
  const lam = r.nz(-4, 4);
  const mu = r.chance(0.5) ? r.nz(-3, 3) : 0;
  const s1 = sumOf(2, `${coefTex(1, [0, -1], b, "n", 0)}\\,x^{n-2}`);
  const s2 = sumOf(1, `${coefTex(1, [0], b, "n", 0)}\\,x^{n-1}`);
  const s3 = sumOf(0, `${coefTex(1, [], b, "n", 0)}\\,x^{n}`);
  const muPart = mu === 0 ? "" : `${mu > 0 ? " - " : " + "}${Math.abs(mu) === 1 ? "" : Math.abs(mu)}x${s2}`;
  const lamPart = `${lam > 0 ? " + " : " - "}${Math.abs(lam) === 1 ? "" : Math.abs(lam)}${s3}`;
  const expr = `${s1}${muPart}${lamPart}`;
  const t1 = coefTex(1, [0, -1], b, "k", 2);
  const t2 = mu === 0 ? "" : coefTex(-mu, [0], b, "k", 0);
  const t3 = coefTex(lam, [], b, "k", 0);
  const ck = join([t1, t2, t3]);
  const ckJs = [coefJs(1, [0, -1], b, "k", 2), mu ? coefJs(-mu, [0], b, "k", 0) : "", coefJs(lam, [], b, "k", 0)].filter(Boolean).join(" + ");
  return {
    prompt: `Find the coefficient ${m("c_k")} of ${m("x^k")} (${m("k \\ge 0")}) in ${m(expr)}`,
    answer: { kind: "expression", ref: ckJs, vars: ["k"], label: "c_k" },
    answerTex: `c_k = ${ck}`,
    steps: [
      `First sum: ${m("k = n - 2")}, so ${m("n = k + 2")}: coefficient ${m(t1)}, starting at ${m("k = 0")}.`,
      ...(mu === 0 ? [] : [`Middle: ${m("x\\cdot x^{n-1} = x^n")}, so ${m("k = n")}: ${m(t2)} (at ${m("k = 0")} it is ${m("0")}, so starting at 1 or 0 doesn't matter).`]),
      `Last sum is already in ${m("x^k")}: ${m(t3)}.`,
      `All start at ${m("k = 0")}; add: ${m(`c_k = ${ck}`)}`,
    ],
    meta: {
      variant: "sigma-combine",
      k0: 0,
      sums: [
        { coef: coefJs(1, [0, -1], b, "n", 0), pow: -2, n0: 2 },
        ...(mu ? [{ coef: coefJs(-mu, [0], b, "n", 0), pow: 0, n0: 1 }] : []),
        { coef: coefJs(lam, [], b, "n", 0), pow: 0, n0: 0 },
      ],
    },
  };
}

// ═══════════════════════════════════════════════════════════════════════════
// A tiny CAS for products of x^a, y^b, e^{kx}, sin, cos, ln, e^{kxy}
// (calc.multivariable, ode1.exact, ode1.exact-if)
// ═══════════════════════════════════════════════════════════════════════════
type Var = "x" | "y";
type Fac =
  | { t: "pow" | "exp" | "sin" | "cos"; v: Var; k: number }
  | { t: "ln"; v: Var; k: 1 }
  | { t: "exy"; v: "xy"; k: number };
interface Term {
  c: Q;
  f: Fac[];
}
type Ex = Term[];
const ORDER = ["pow", "exp", "exy", "ln", "sin", "cos"];
const facKey = (f: Fac) => `${ORDER.indexOf(f.t)}${f.v}${f.t === "pow" || f.t === "exp" || f.t === "exy" ? "" : f.k}`;

function norm(t: Term): Term {
  const merged = new Map<string, Fac>();
  for (const f of t.f) {
    const key = facKey(f);
    const prev = merged.get(key);
    if (prev && (f.t === "pow" || f.t === "exp" || f.t === "exy")) merged.set(key, { ...prev, k: prev.k + f.k } as Fac);
    else if (prev) throw new Error("repeated transcendental factor");
    else merged.set(key, f);
  }
  const f = [...merged.values()].filter((g) => !((g.t === "pow" || g.t === "exp" || g.t === "exy") && g.k === 0));
  f.sort((a, b) => (facKey(a) < facKey(b) ? -1 : 1));
  return { c: t.c, f };
}
const termKey = (t: Term) => t.f.map((f) => `${f.t}${f.v}${f.k}`).join("|");
function combine(ex: Ex): Ex {
  const out = new Map<string, Term>();
  for (const t0 of ex) {
    const t = norm(t0);
    const k = termKey(t);
    const prev = out.get(k);
    out.set(k, prev ? { c: prev.c.add(t.c), f: t.f } : t);
  }
  return [...out.values()].filter((t) => !t.c.isZero());
}
const dependsOn = (f: Fac, v: Var) => f.v === v || f.t === "exy";
function dFac(f: Fac, v: Var): [number, Fac[]] | null {
  switch (f.t) {
    case "pow":
      return f.k === 0 ? null : [f.k, [{ t: "pow", v: f.v, k: f.k - 1 }]];
    case "exp":
      return [f.k, [f]];
    case "sin":
      return [f.k, [{ t: "cos", v: f.v, k: f.k }]];
    case "cos":
      return [-f.k, [{ t: "sin", v: f.v, k: f.k }]];
    case "ln":
      return [1, [{ t: "pow", v: f.v, k: -1 }]];
    case "exy":
      return [f.k, [{ t: "pow", v: v === "x" ? "y" : "x", k: 1 }, f]];
  }
}
function diff(ex: Ex, v: Var): Ex {
  const out: Ex = [];
  for (const t of ex)
    t.f.forEach((f, i) => {
      if (!dependsOn(f, v)) return;
      const d = dFac(f, v);
      if (!d) return;
      out.push({ c: t.c.mul(d[0]), f: [...t.f.slice(0, i), ...t.f.slice(i + 1), ...d[1]] });
    });
  return combine(out);
}
const mulFac = (ex: Ex, f: Fac): Ex => combine(ex.map((t) => ({ c: t.c, f: [...t.f, f] })));
const exAdd = (...xs: Ex[]): Ex => combine(xs.flat());
const exScale = (ex: Ex, k: number | Q): Ex => combine(ex.map((t) => ({ c: t.c.mul(k), f: t.f })));
const exDepends = (ex: Ex, v: Var) => ex.some((t) => t.f.some((f) => dependsOn(f, v)));
const termDepends = (t: Term, v: Var) => t.f.some((f) => dependsOn(f, v));

function facTex(f: Fac): string {
  switch (f.t) {
    case "pow":
      return f.k === 1 ? f.v : `${f.v}^{${f.k}}`;
    case "exp":
      return eTex(f.k, f.v);
    case "exy":
      return `e^{${ct(f.k, "xy")}}`;
    case "ln":
      return `\\ln ${f.v}`;
    default:
      return f.k === 1 ? `\\${f.t} ${f.v}` : `\\${f.t}(${f.k}${f.v})`;
  }
}
function facJs(f: Fac): string {
  switch (f.t) {
    case "pow":
      return `${f.v}^(${f.k})`;
    case "exp":
      return eJs(f.k, f.v);
    case "exy":
      return `exp((${f.k})*x*y)`;
    case "ln":
      return `log(${f.v})`;
    default:
      return `${f.t}((${f.k})*${f.v})`;
  }
}
function termTex(t: Term): string {
  const num = t.f.filter((f) => !(f.t === "pow" && f.k < 0)).map(facTex).join("");
  const den = t.f.filter((f) => f.t === "pow" && f.k < 0).map((f) => facTex({ ...f, k: -f.k } as Fac)).join("");
  if (den) return coefOver(t.c, num, den);
  return num ? qterm(t.c, num) : t.c.tex();
}
const exTex = (ex: Ex) => join(ex.map(termTex));
const termJs = (t: Term) => `${t.c.js()}*${t.f.map(facJs).join("*") || "1"}`;
const exJs = (ex: Ex) => (ex.length ? ex.map(termJs).join(" + ") : "0");

// atoms
const pw = (v: Var, k: number): Fac => ({ t: "pow", v, k });
const mono = (c: number, a: number, b: number): Term => norm({ c: q(c), f: [pw("x", a), pw("y", b)] });
const atom = (c: number, ...f: Fac[]): Term => norm({ c: q(c), f });
const coefNz = (r: Rng) => r.pick([1, 1, 2, 3, -1, -2, 4]);

/** a transcendental atom that depends on both x and y */
function mixedTranscendental(r: Rng, allowLn: boolean, allowYTrans = true): Term {
  const c = coefNz(r);
  const k = r.pick([1, 1, 2, 3]);
  const kinds = ["yexp", "ytrig", "exy", ...(allowYTrans ? ["xexp", "xtrig"] : []), ...(allowLn ? ["yln"] : [])];
  const kind = r.pick(kinds);
  const b = r.pick([1, 1, 2]);
  switch (kind) {
    case "yexp":
      return atom(c, pw("y", b), { t: "exp", v: "x", k: r.pick([1, 2, -1]) });
    case "xexp":
      return atom(c, pw("x", b), { t: "exp", v: "y", k: r.pick([1, 2, -1]) });
    case "ytrig":
      return atom(c, pw("y", b), { t: r.pick(["sin", "cos"]) as "sin", v: "x", k });
    case "xtrig":
      return atom(c, pw("x", b), { t: r.pick(["sin", "cos"]) as "sin", v: "y", k });
    case "yln":
      return atom(c, pw("y", b), { t: "ln", v: "x", k: 1 });
    default:
      return atom(c, { t: "exy", v: "xy", k: r.pick([1, 2, -1]) });
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// calc.multivariable
// ═══════════════════════════════════════════════════════════════════════════
function mvFunction(r: Rng, allowLn = true): Ex {
  const terms: Term[] = [mono(coefNz(r), r.int(1, 3), r.int(1, 3))];
  if (r.chance(0.7)) terms.push(mixedTranscendental(r, allowLn));
  if (r.chance(0.5) || terms.length === 1) terms.push(r.chance(0.5) ? mono(coefNz(r), r.int(1, 4), 0) : mono(coefNz(r), 0, r.int(1, 4)));
  const F = combine(terms);
  require_(F.length >= 2);
  return F;
}

function mvPartial(r: Rng): Draft {
  const F = mvFunction(r);
  const v: Var = r.pick(["x", "y"]);
  const other = v === "x" ? "y" : "x";
  const D = diff(F, v);
  require_(D.length > 0);
  return {
    prompt: `${m(`f(x, y) = ${exTex(F)}`)}. Find ${m(`\\frac{\\partial f}{\\partial ${v}}`)}.`,
    answer: { kind: "expression", ref: exJs(D), vars: ["x", "y"], label: `f_${v}` },
    answerTex: `f_${v} = ${exTex(D)}`,
    steps: [
      `Differentiate in ${m(v)} and treat ${m(other)} as a constant.`,
      `Term by term: ${F.map((t) => m(`${termTex(t)} \\to ${exTex(diff([t], v)) || "0"}`)).join(", ")}.`,
      m(`f_${v} = ${exTex(D)}`),
    ],
    meta: { variant: "mv-partial", F: exJs(F), wrt: v },
  };
}

function mvMixed(r: Rng): Draft {
  const F = mvFunction(r);
  const Fx = diff(F, "x");
  const Fxy = diff(Fx, "y");
  require_(Fxy.length > 0);
  const Fy = diff(F, "y");
  return {
    prompt: `${m(`f(x, y) = ${exTex(F)}`)}. Find the mixed partial ${m("f_{xy} = \\frac{\\partial^2 f}{\\partial y\\,\\partial x}")}.`,
    answer: { kind: "expression", ref: exJs(Fxy), vars: ["x", "y"], label: "f_xy" },
    answerTex: `f_{xy} = ${exTex(Fxy)}`,
    steps: [
      m(`f_x = ${exTex(Fx)}`),
      `Differentiate that in ${m("y")}: ${m(`f_{xy} = ${exTex(Fxy)}`)}`,
      `Check the other order: ${m(`f_y = ${exTex(Fy)}`)}, and ${m(`f_{yx} = ${exTex(diff(Fy, "x"))}`)} — the same (Clairaut).`,
    ],
    meta: { variant: "mv-mixed", F: exJs(F) },
  };
}

function mvImplicit(r: Rng): Draft {
  const F = mvFunction(r);
  const Fx = diff(F, "x"), Fy = diff(F, "y");
  require_(Fx.length > 0 && Fy.length > 0);
  const ans = `-\\frac{${exTex(Fx)}}{${exTex(Fy)}}`;
  return {
    prompt: `The curve ${m(`${exTex(F)} = c`)} defines ${m("y(x)")} implicitly. Find ${m("\\frac{dy}{dx}")}.`,
    answer: { kind: "expression", ref: `-(${exJs(Fx)})/(${exJs(Fy)})`, vars: ["x", "y"], label: "dy/dx" },
    answerTex: `\\frac{dy}{dx} = ${ans}`,
    steps: [
      `Along the curve ${m("du = u_x\\,dx + u_y\\,dy = 0")}, so ${m("\\frac{dy}{dx} = -\\frac{u_x}{u_y}")}.`,
      `${m(`u_x = ${exTex(Fx)}`)}, ${m(`u_y = ${exTex(Fy)}`)}.`,
      m(`\\frac{dy}{dx} = ${ans}`),
    ],
    meta: { variant: "mv-implicit", F: exJs(F) },
  };
}

const EXACT_OPTIONS = ["Exact", "Not exact"];
function mvExactTest(r: Rng): Draft {
  const F = mvFunction(r, false);
  let M = diff(F, "x"), N = diff(F, "y");
  require_(M.length > 0 && N.length > 0 && diff(M, "y").length > 0);
  const exact = r.chance(0.5);
  if (!exact) {
    if (r.chance(0.5)) N = exScale(N, -1);
    else {
      const i = N.findIndex((t) => termDepends(t, "x"));
      require_(i >= 0);
      N = combine(N.map((t, j) => (j === i ? { c: t.c.mul(2), f: t.f } : t)));
    }
  }
  const My = diff(M, "y"), Nx = diff(N, "x");
  const isExact = exAdd(My, exScale(Nx, -1)).length === 0;
  require_(isExact === exact);
  return {
    prompt: `Is ${m(`${P(exTex(M))}\\,dx + ${P(exTex(N))}\\,dy`)} an exact differential?`,
    answer: { kind: "choice", options: EXACT_OPTIONS, correct: EXACT_OPTIONS[exact ? 0 : 1] },
    answerTex: `\\text{${EXACT_OPTIONS[exact ? 0 : 1]}}`,
    steps: [
      `Exact means ${m("M\\,dx + N\\,dy = du")} for some ${m("u")}; then ${m("M_y = u_{xy} = N_x")}. Test that.`,
      `${m(`M_y = ${exTex(My) || "0"}`)}, ${m(`N_x = ${exTex(Nx) || "0"}`)}.`,
      exact ? `Equal, so exact (here ${m(`u = ${exTex(F)}`)}).` : `Not equal, so not exact.`,
    ],
    meta: { variant: "mv-exact-test", M: exJs(M), N: exJs(N), exact },
  };
}

// ═══════════════════════════════════════════════════════════════════════════
// ode1.exact   (Kreyszig §1.4: M dx + N dy = 0, M_y = N_x, solution u(x, y) = c)
// ═══════════════════════════════════════════════════════════════════════════
function exactPotential(r: Rng, kind: string, ivp: boolean): Ex {
  const terms: Term[] = [mono(coefNz(r), r.int(1, 3), r.int(1, 3))];
  if (kind === "trans") terms.push(mixedTranscendental(r, false, !ivp));
  else if (r.chance(0.5)) terms.push(mono(coefNz(r), r.int(1, 3), r.int(1, 3)));
  if (r.chance(0.6)) terms.push(mono(coefNz(r), r.int(1, 3), 0));
  if (r.chance(0.5)) terms.push(mono(coefNz(r), 0, r.int(1, 3)));
  const F = combine(terms);
  require_(F.length >= 2);
  return F;
}

function exactDraft(F: Ex, ic: [number, number] | null, variant: string): Draft {
  const M = diff(F, "x"), N = diff(F, "y");
  require_(M.length > 0 && N.length > 0);
  const My = diff(M, "y");
  const xPart = F.filter((t) => termDepends(t, "x"));
  const kPart = F.filter((t) => !termDepends(t, "x"));
  const eq = `${P(exTex(M))}\\,dx + ${P(exTex(N))}\\,dy = 0`;
  const rhs = `-(${exJs(M)})/(${exJs(N)})`;
  const uy = diff(xPart, "y");
  const kp = diff(kPart, "y");
  const steps = [
    `Exactness: ${m(`M_y = ${exTex(My)} = N_x`)}.`,
    `Integrate ${m("M")} in ${m("x")}: ${m(`u = ${exTex(xPart)} + k(y)`)}.`,
    `${m("u_y = N")}: ${m(`${exTex(uy) || "0"} + k'(y) = ${exTex(N)}`)}, so ${m(`k'(y) = ${exTex(kp) || "0"}`)}${kPart.length ? `, ${m(`k = ${exTex(kPart)}`)}` : ""}.`,
  ];
  if (!ic) {
    steps.push(`Solution: ${m(`${exTex(F)} = C`)}`);
    return {
      prompt: `Solve the exact equation ${m(eq)}`,
      answer: { kind: "ode", rhs, ref: `${exJs(F)} = C` },
      answerTex: `${exTex(F)} = C`,
      steps,
      meta: { variant, M: exJs(M), N: exJs(N) },
    };
  }
  const [x0, y0] = ic;
  // u(0, y0): x-powers vanish, e^{kx}, cos(kx), e^{kxy} -> 1, sin(kx) -> 0
  let val = 0;
  for (const t of F) {
    let v = t.c.value();
    for (const f of t.f) {
      if (f.t === "pow") v *= f.v === "x" ? (f.k === 0 ? 1 : 0) : y0 ** f.k;
      else if (f.v === "x" && f.t === "exp") v *= 1;
      else if (f.v === "x" && f.t === "cos") v *= 1;
      else if (f.v === "x" && f.t === "sin") v *= 0;
      else if (f.t === "exy") v *= 1;
      else throw new Error("non-integer u(0, y0)");
    }
    val += v;
  }
  require_(Number.isInteger(val) && x0 === 0);
  const nAt = real(math.evaluate(exJs(N), { x: x0, y: y0 }));
  require_(Math.abs(nAt) > 1e-9);
  steps.push(`${m("u(x, y) = c")} with ${m(`y(0) = ${y0}`)}: ${m(`c = u(0, ${y0}) = ${val}`)}, so ${m(`${exTex(F)} = ${val}`)}`);
  return {
    prompt: `Solve the initial value problem ${m(`${eq},\\quad y(0) = ${y0}`)}`,
    answer: { kind: "ode", rhs, ic: [0, y0], ref: `${exJs(F)} = ${val}` },
    answerTex: `${exTex(F)} = ${val}`,
    steps,
    meta: { variant, M: exJs(M), N: exJs(N) },
  };
}

const exactPoly = (r: Rng) => exactDraft(exactPotential(r, "poly", false), null, "exact-poly");
const exactTrans = (r: Rng) => exactDraft(exactPotential(r, "trans", false), null, "exact-trans");
function exactExy(r: Rng): Draft {
  const F = combine([atom(coefNz(r), { t: "exy", v: "xy", k: r.pick([1, 2, -1]) }), mono(coefNz(r), r.int(1, 3), r.int(0, 2)), ...(r.chance(0.5) ? [mono(coefNz(r), 0, r.int(1, 3))] : [])]);
  return exactDraft(F, null, "exact-exy");
}
function exactIvp(r: Rng): Draft {
  const F = exactPotential(r, r.pick(["poly", "trans"]), true);
  return exactDraft(F, [0, r.pick([1, 2, -1, -2, 3])], "exact-ivp");
}

// ═══════════════════════════════════════════════════════════════════════════
// ode1.exact-if   (Kreyszig §1.4: P dx + Q dy = 0, integrating factor F(x) or F*(y))
// ═══════════════════════════════════════════════════════════════════════════
interface IfSpec {
  Pe: Ex;
  Qe: Ex;
  U: Ex; // potential of F·P dx + F·Q dy
  v: Var; // the IF depends on v only
  mu: { tex: string; js: string };
  R: string; // LaTeX of R or R*
}

function ifSpec(r: Rng, v: Var, type: "exp" | "pow", kPow?: number): IfSpec {
  const o: Var = v === "x" ? "y" : "x";
  if (type === "exp") {
    // U = e^{a v} G,  G polynomial;  divide U_x, U_y by e^{a v}
    const a = r.pick([1, 2, -1, -2, 3]);
    const mixed = mono(coefNz(r), r.int(1, 2), r.int(1, 2));
    const G = combine([mixed, ...(r.chance(0.6) ? [v === "x" ? mono(coefNz(r), 0, r.int(1, 3)) : mono(coefNz(r), r.int(1, 3), 0)] : []), ...(r.chance(0.4) ? [mono(coefNz(r), r.int(0, 2), r.int(0, 2))] : [])]);
    require_(exDepends(G, o));
    const U = mulFac(G, { t: "exp", v, k: a });
    const inv: Fac = { t: "exp", v, k: -a };
    return {
      Pe: mulFac(diff(U, "x"), inv),
      Qe: mulFac(diff(U, "y"), inv),
      U,
      v,
      mu: { tex: eTex(a, v), js: eJs(a, v) },
      R: `${a}`,
    };
  }
  // U = Σ monomials with v-power ≥ k+1;  divide U_x, U_y by v^k
  const k = kPow ?? r.pick([1, 2]);
  const terms = [
    v === "x" ? mono(coefNz(r), k + r.int(1, 2), r.int(1, 2)) : mono(coefNz(r), r.int(1, 2), k + r.int(1, 2)),
    ...(r.chance(0.6) ? [v === "x" ? mono(coefNz(r), k + r.int(1, 2), r.int(0, 3)) : mono(coefNz(r), r.int(0, 3), k + r.int(1, 2))] : []),
  ];
  const U = combine(terms);
  require_(U.length >= 1 && exDepends(U, o));
  const inv = pw(v, -k);
  const Pe = mulFac(diff(U, "x"), inv), Qe = mulFac(diff(U, "y"), inv);
  require_([...Pe, ...Qe].every((t) => t.f.every((f) => !(f.t === "pow" && f.k < 0))));
  return { Pe, Qe, U, v, mu: { tex: k === 1 ? v : `${v}^{${k}}`, js: `${v}^${k}` }, R: `\\frac{${k}}{${v}}` };
}

/** does the mathjs expression change when only `v` changes? (sampled numerically) */
function varies(js: string, v: Var): boolean {
  const o = v === "x" ? "y" : "x";
  const c = math.compile(js);
  for (const w of [0.7, 1.3, 2.1])
    for (const [u1, u2] of [[0.6, 1.4], [0.9, 1.9]]) {
      const a = real(c.evaluate({ [o]: w, [v]: u1 })), b = real(c.evaluate({ [o]: w, [v]: u2 }));
      if (Number.isFinite(a) && Number.isFinite(b) && Math.abs(a - b) > 1e-9 * Math.max(1, Math.abs(a))) return true;
    }
  return false;
}

function ifCommon(s: IfSpec) {
  const Py = diff(s.Pe, "y"), Qx = diff(s.Qe, "x");
  require_(exAdd(Py, exScale(Qx, -1)).length > 0 && s.Pe.length > 0 && s.Qe.length > 0);
  // only one of Kreyszig's two tests may succeed: R* (or R) for the other variable must fail
  const dif = `(${exJs(Py)}) - (${exJs(Qx)})`;
  require_(s.v === "x" ? varies(`(${dif})/(${exJs(s.Pe)})`, "x") : varies(`(${dif})/(${exJs(s.Qe)})`, "y"));
  const eq = `${P(exTex(s.Pe))}\\,dx + ${P(exTex(s.Qe))}\\,dy = 0`;
  const test =
    s.v === "x"
      ? `${m("R = \\frac{1}{Q}\\left(\\frac{\\partial P}{\\partial y} - \\frac{\\partial Q}{\\partial x}\\right)")} with ${m(`P_y = ${exTex(Py) || "0"}`)}, ${m(`Q_x = ${exTex(Qx) || "0"}`)}: ${m(`R = ${s.R}`)}, a function of ${m("x")} only.`
      : `${m("R^* = \\frac{1}{P}\\left(\\frac{\\partial Q}{\\partial x} - \\frac{\\partial P}{\\partial y}\\right)")} with ${m(`P_y = ${exTex(Py) || "0"}`)}, ${m(`Q_x = ${exTex(Qx) || "0"}`)}: ${m(`R^* = ${s.R}`)}, a function of ${m("y")} only.`;
  const fname = s.v === "x" ? "F(x)" : "F^*(y)";
  const integ = `${m(`${fname} = \\exp\\int ${s.R}\\,d${s.v} = ${s.mu.tex}`)}`;
  return { eq, test, fname, integ, Py, Qx };
}

function ifFactor(r: Rng, v: Var): Draft {
  // F = x^2 rather than x: a constant-multiple answer check can't tell x from x + x/7
  const s = ifSpec(r, v, r.pick(["exp", "pow"]), 2);
  const c = ifCommon(s);
  return {
    prompt: `${m(c.eq)} is not exact. Find an integrating factor ${m(c.fname)} that makes it exact.`,
    answer: { kind: "expression", ref: s.mu.js, vars: [v], upToConstant: true, label: v === "x" ? "F(x)" : "F*(y)" },
    answerTex: `${c.fname} = ${s.mu.tex}`,
    steps: [
      `Not exact: ${m(`P_y = ${exTex(c.Py) || "0"} \\ne ${exTex(c.Qx) || "0"} = Q_x`)}.`,
      c.test,
      `${c.integ} (any constant multiple works).`,
      `Check: ${m(`${s.mu.tex}\\cdot`)}the equation has ${m(`M_y = N_x`)}.`,
    ],
    meta: { variant: "if-factor", P: exJs(s.Pe), Q: exJs(s.Qe), v, mu: s.mu.js },
  };
}

function ifSolve(r: Rng): Draft {
  const s = ifSpec(r, r.pick(["x", "y"]), r.pick(["exp", "pow"]));
  const c = ifCommon(s);
  return {
    prompt: `Find an integrating factor and solve ${m(c.eq)}`,
    answer: { kind: "ode", rhs: `-(${exJs(s.Pe)})/(${exJs(s.Qe)})`, ref: `${exJs(s.U)} = C` },
    answerTex: `${exTex(s.U)} = C`,
    steps: [
      `Not exact: ${m(`P_y = ${exTex(c.Py) || "0"} \\ne ${exTex(c.Qx) || "0"} = Q_x`)}.`,
      c.test,
      c.integ,
      `Multiply through: ${m(`${P(exTex(diff(s.U, "x")))}\\,dx + ${P(exTex(diff(s.U, "y")))}\\,dy = 0`)} is exact.`,
      `Integrate as in an exact equation: ${m(`${exTex(s.U)} = C`)}`,
    ],
    meta: { variant: "if-solve", P: exJs(s.Pe), Q: exJs(s.Qe), v: s.v, mu: s.mu.js },
  };
}

const IF_OPTIONS = ["Integrating factor F(x)", "Integrating factor F*(y)"];
function ifTest(r: Rng): Draft {
  const v: Var = r.pick(["x", "y"]);
  const s = ifSpec(r, v, r.pick(["exp", "pow"]));
  const c = ifCommon(s);
  const ix = v === "x" ? 0 : 1;
  return {
    prompt: `${m(c.eq)} is not exact. Which integrating factor does Kreyszig's test give: one depending only on ${m("x")}, or only on ${m("y")}?`,
    answer: { kind: "choice", options: IF_OPTIONS, correct: IF_OPTIONS[ix] },
    answerTex: `\\text{${IF_OPTIONS[ix]}} = ${s.mu.tex}`,
    steps: [
      `${m(`P_y = ${exTex(c.Py) || "0"}`)}, ${m(`Q_x = ${exTex(c.Qx) || "0"}`)}.`,
      c.test,
      c.integ,
    ],
    meta: { variant: "if-test", P: exJs(s.Pe), Q: exJs(s.Qe), v },
  };
}

// ═══════════════════════════════════════════════════════════════════════════
// ode1.modeling   (Kreyszig §1.3 mixing & Newton cooling, §1.1/1.3 decay, §1.5 logistic)
// ═══════════════════════════════════════════════════════════════════════════
function modelMixing(r: Rng): Draft {
  const tau = r.pick([10, 20, 25, 50, 100]);
  const V = r.pick([100, 200, 500, 1000]);
  const rate = V / tau;
  require_(Number.isInteger(rate));
  const c = r.pick([0, 0.1, 0.2, 0.5, 1]);
  const yinf = Math.round(c * V);
  const y0 = r.pick([0, 10, 20, 50, 100, 200]);
  require_(y0 !== yinf);
  const D = y0 - yinf;
  const yTex = join([yinf ? `${yinf}` : "", ct(D, `e^{-t/${tau}}`)]);
  const yJs = `${yinf} + (${D})*exp(-t/${tau})`;
  const setup = [
    `Salt balance: ${m("y' = \\text{in} - \\text{out}")} ${m(`= ${rate}\\cdot${c} - ${rate}\\cdot\\frac{y}{${V}}`)}, i.e. ${m(`y' = -\\frac{1}{${tau}}(y - ${yinf})`)}.`,
    `Separate (or linear): ${m(`y = ${yinf} + Ce^{-t/${tau}}`)}; ${m(`y(0) = ${y0}`)} gives ${m(`C = ${D}`)}.`,
  ];
  const story = `A tank holds ${m(`${V}`)} L of ${y0 ? `brine containing ${m(`${y0}`)} kg of salt` : "pure water"}. ${c ? `Brine with ${m(`${c}`)} kg/L` : "Pure water"} flows in at ${m(`${rate}`)} L/min; the well-stirred mixture flows out at the same rate.`;
  const target = r.pick(["fn", "at", "time"]);
  const meta = { variant: "model-mixing", V, rate, c, y0, target } as Record<string, unknown>;
  if (target === "fn") {
    return {
      prompt: `${story} Find the amount of salt ${m("y(t)")} (kg) at time ${m("t")} (min).`,
      answer: { kind: "expression", ref: yJs, vars: ["t"], label: "y(t)" },
      answerTex: `y(t) = ${yTex}`,
      steps: [...setup, m(`y(t) = ${yTex}`)],
      meta,
    };
  }
  if (target === "at") {
    const T = r.pick([5, 10, 15, 30, 60]);
    const val = yinf + D * Math.exp(-T / tau);
    meta.T = T;
    return {
      prompt: `${story} How much salt is in the tank after ${m(`${T}`)} min?`,
      answer: { kind: "expression", ref: `${yinf} + (${D})*exp(-${T}/${tau})`, vars: [], rel: true, tol: 0.01, label: "y", unit: "kg" },
      answerTex: `y(${T}) \\approx ${fmtNum(val)}\\ \\text{kg}`,
      steps: [...setup, `${m(`y(${T}) = ${yinf} + (${D})e^{-${T}/${tau}} \\approx ${fmtNum(val)}`)} kg.`],
      meta,
    };
  }
  // time to get halfway from y0 to the limit: e^{-t/τ} = 1/2
  const half = (y0 + yinf) / 2;
  meta.yT = half;
  return {
    prompt: `${story} When does the tank hold ${m(`${half}`)} kg of salt?`,
    answer: { kind: "expression", ref: `${tau}*log(2)`, vars: [], rel: true, tol: 0.01, label: "t", unit: "min" },
    answerTex: `t = ${tau}\\ln 2 \\approx ${fmtNum(tau * Math.log(2))}\\ \\text{min}`,
    steps: [...setup, `${m(`${half} = ${yinf} + (${D})e^{-t/${tau}}`)}: ${m("e^{-t/" + tau + "} = \\frac{1}{2}")}, so ${m(`t = ${tau}\\ln 2 \\approx ${fmtNum(tau * Math.log(2))}`)} min.`],
    meta,
  };
}

function modelCooling(r: Rng): Draft {
  const TA = r.pick([20, 22, 25, 15]);
  const D0 = r.pick([40, 60, 64, 80, 100]);
  const qr = r.pick([q(1, 2), q(3, 4), q(1, 4)]);
  const t1 = r.pick([5, 10, 15, 20]);
  const T0 = TA + D0;
  const T1 = TA + D0 * qr.value();
  require_(Number.isInteger(T1 * 2));
  const what = r.pick(["object", "coffee", "casting"]);
  const story = `A${what === "object" ? "n object" : what === "coffee" ? " cup of coffee" : " metal casting"} at ${m(`${T0}^\\circ\\text{C}`)} is placed in a room at ${m(`${TA}^\\circ\\text{C}`)}. After ${m(`${t1}`)} min it is at ${m(`${fmtNum(T1)}^\\circ\\text{C}`)}.`;
  const kTex = `k = \\frac{\\ln ${qr.n === 1 ? qr.d : `(${qr.d}/${qr.n})`}}{${t1}}`;
  const setup = [
    `Newton: ${m(`T' = -k(T - ${TA})`)}, so ${m(`T = ${TA} + ${D0}e^{-kt}`)}.`,
    `${m(`T(${t1}) = ${fmtNum(T1)}`)}: ${m(`e^{-${t1}k} = ${qr.tex()}`)}, ${m(kTex)}.`,
  ];
  const target = r.pick(["at", "time", "k"]);
  const meta = { variant: "model-cooling", TA, T0, t1, T1, target } as Record<string, unknown>;
  if (target === "k") {
    const kv = Math.log(qr.d / qr.n) / t1;
    return {
      prompt: `${story} Find the cooling constant ${m("k")} in ${m(`T' = -k(T - T_A)`)} (per minute).`,
      answer: { kind: "expression", ref: `log(${qr.d}/${qr.n})/${t1}`, vars: [], rel: true, tol: 0.01, label: "k" },
      answerTex: `${kTex} \\approx ${fmtNum(kv)}\\ \\text{min}^{-1}`,
      steps: [...setup, m(`k \\approx ${fmtNum(kv)}`)],
      meta,
    };
  }
  const nmul = r.pick([2, 3]);
  if (target === "at") {
    const t2 = nmul * t1;
    const val = TA + D0 * qr.value() ** nmul;
    meta.t2 = t2;
    return {
      prompt: `${story} What is its temperature after ${m(`${t2}`)} min?`,
      answer: { kind: "expression", ref: `${TA} + ${D0}*(${qr.n}/${qr.d})^${nmul}`, vars: [], rel: true, tol: 0.01, label: "T", unit: "°C" },
      answerTex: `T(${t2}) = ${fmtNum(val)}^\\circ\\text{C}`,
      steps: [...setup, `${m(`e^{-${t2}k} = (e^{-${t1}k})^{${nmul}} = ${P(qr.tex())}^{${nmul}}`)}, so ${m(`T(${t2}) = ${TA} + ${D0}\\cdot${P(qr.tex())}^{${nmul}} = ${fmtNum(val)}`)}.`],
      meta,
    };
  }
  const Tt = TA + D0 * qr.value() ** nmul;
  require_(Math.abs(Tt * 100 - Math.round(Tt * 100)) < 1e-9);
  meta.Tt = Tt;
  return {
    prompt: `${story} When does it reach ${m(`${fmtNum(Tt)}^\\circ\\text{C}`)}?`,
    answer: { kind: "expression", ref: `${nmul * t1}`, vars: [], rel: true, tol: 0.01, label: "t", unit: "min" },
    answerTex: `t = ${nmul * t1}\\ \\text{min}`,
    steps: [...setup, `${m(`${fmtNum(Tt)} = ${TA} + ${D0}e^{-kt}`)}: ${m(`e^{-kt} = ${P(qr.tex())}^{${nmul}}`)}, so ${m(`t = ${nmul}\\cdot${t1} = ${nmul * t1}`)} min.`],
    meta,
  };
}

function modelDecay(r: Rng): Draft {
  const kind = r.pick(["halflife", "carbon", "doubling"]);
  if (kind === "carbon") {
    // Kreyszig §1.3 Example 4: half-life of C-14 is 5715 years
    const pct = r.pick([20, 25, 40, 50, 52.5, 60, 70, 80]);
    const t = (5715 * Math.log(100 / pct)) / Math.log(2);
    return {
      prompt: `A fossil contains ${m(`${pct}\\%`)} of the original ${m("{}^{14}\\text{C}")}. Taking the half-life as 5715 years, estimate its age (years).`,
      answer: { kind: "expression", ref: `5715*log(100/${pct})/log(2)`, vars: [], rel: true, tol: 0.01, label: "t", unit: "yr" },
      answerTex: `t \\approx ${Math.round(t)}\\ \\text{yr}`,
      steps: [
        `Decay ${m("y' = -ky")}: ${m("y = y_0e^{-kt}")}, and the half-life gives ${m("k = \\ln 2/5715")}.`,
        `${m(`e^{-kt} = ${pct / 100}`)}: ${m(`t = \\frac{\\ln(1/${pct / 100})}{k} = \\frac{5715\\ln(1/${pct / 100})}{\\ln 2}`)}`,
        m(`t \\approx ${Math.round(t)}\\ \\text{yr}`),
      ],
      meta: { variant: "model-decay", H: 5715, frac: pct / 100, target: "time" },
    };
  }
  const H = r.pick([2, 3, 5, 8, 10, 20]);
  const y0 = r.pick([10, 50, 80, 100, 200]);
  const T = r.pick([3, 4, 6, 7, 12, 15, 25]);
  require_(T % H !== 0);
  if (kind === "doubling") {
    const val = y0 * 2 ** (T / H);
    return {
      prompt: `A bacteria culture grows at a rate proportional to its size (${m("y' = ky")}) and doubles every ${m(`${H}`)} h. Starting from ${m(`${y0}`)} mg, how much is there after ${m(`${T}`)} h?`,
      answer: { kind: "expression", ref: `${y0}*2^(${T}/${H})`, vars: [], rel: true, tol: 0.01, label: "y", unit: "mg" },
      answerTex: `y(${T}) = ${y0}\\cdot 2^{${T}/${H}} \\approx ${fmtNum(val)}\\ \\text{mg}`,
      steps: [
        `${m(`y = ${y0}e^{kt}`)}; doubling: ${m(`e^{${H}k} = 2`)}, ${m(`k = \\ln 2/${H}`)}.`,
        `So ${m(`y = ${y0}\\cdot 2^{t/${H}}`)}.`,
        m(`y(${T}) = ${y0}\\cdot 2^{${T}/${H}} \\approx ${fmtNum(val)}`),
      ],
      meta: { variant: "model-decay", H, y0, T, growth: true, target: "at" },
    };
  }
  const val = y0 * 2 ** (-T / H);
  return {
    prompt: `A radioactive sample decays by ${m("y' = -ky")} with half-life ${m(`${H}`)} days. Starting from ${m(`${y0}`)} mg, how much remains after ${m(`${T}`)} days?`,
    answer: { kind: "expression", ref: `${y0}*2^(-${T}/${H})`, vars: [], rel: true, tol: 0.01, label: "y", unit: "mg" },
    answerTex: `y(${T}) = ${y0}\\cdot 2^{-${T}/${H}} \\approx ${fmtNum(val)}\\ \\text{mg}`,
    steps: [
      `${m(`y = ${y0}e^{-kt}`)}; half-life: ${m(`e^{-${H}k} = \\frac{1}{2}`)}, ${m(`k = \\ln 2/${H}`)}.`,
      `So ${m(`y = ${y0}\\cdot 2^{-t/${H}}`)}.`,
      m(`y(${T}) = ${y0}\\cdot 2^{-${T}/${H}} \\approx ${fmtNum(val)}`),
    ],
    meta: { variant: "model-decay", H, y0, T, growth: false, target: "at" },
  };
}

function modelLogistic(r: Rng): Draft {
  // y' = A y - B y^2, carrying capacity K = A/B;  y = K / (1 + (K/y0 - 1) e^{-At})
  const A = r.pick([1, 2, 3]);
  const K = r.pick([2, 4, 5, 10, 20]);
  const B = q(A, K);
  const y0 = r.pick([1, 1, 2, K * 2]);
  require_(y0 !== K);
  const Cq = q(K, y0).sub(1);
  const eq = `y' = ${ct(A, "y")} - ${qterm(B, "y^{2}")}`;
  const yTex = `\\frac{${K}}{1 ${Cq.n < 0 ? "-" : "+"} ${qterm(q(Math.abs(Cq.n), Cq.d), `e^{${ct(-A, "t")}}`)}}`;
  return {
    prompt: `Logistic growth: solve ${m(`${eq},\\quad y(0) = ${y0}`)}`,
    answer: { kind: "expression", ref: `${K}/(1 + ${Cq.js()}*exp(-${A}*t))`, vars: ["t"], label: "y(t)" },
    answerTex: `y(t) = ${yTex}`,
    steps: [
      `Bernoulli (or separable): ${m("u = 1/y")} gives ${m(`u' + ${A}u = ${B.tex()}`)}, so ${m(`u = \\frac{1}{${K}} + Ce^{${ct(-A, "t")}}`)}.`,
      `Equivalently ${m(`y = \\frac{${K}}{1 + Ce^{${ct(-A, "t")}}}`)} with carrying capacity ${m(`A/B = ${K}`)}.`,
      `${m(`y(0) = ${y0}`)}: ${m(`1 + C = ${q(K, y0).tex()}`)}, ${m(`C = ${Cq.tex()}`)}.`,
      m(`y(t) = ${yTex}`),
    ],
    meta: { variant: "model-logistic", A, B: [B.n, B.d], y0 },
  };
}

// ═══════════════════════════════════════════════════════════════════════════
// ode1.recognize   (which Ch 1 method?)
// ═══════════════════════════════════════════════════════════════════════════
const RECOG = ["Separable", "Substitution u = y/x or v = ax + by", "Linear", "Bernoulli", "Exact"];
interface Rec {
  tex: string;
  f: string;
  form: "explicit" | "diff";
  M?: string;
  N?: string;
  why: string[];
}
function recogDraft(cls: number, rec: Rec): Draft {
  return {
    prompt: `Which method solves ${m(rec.tex)} most directly?`,
    answer: { kind: "choice", options: RECOG, correct: RECOG[cls] },
    answerTex: `\\text{${RECOG[cls]}}`,
    steps: [
      `Check in order: separable ${m("g(x)h(y)")}? linear in ${m("y")}? ${m("y^n")} term (Bernoulli)? a function of ${m("y/x")} or ${m("ax + by")}? ${m("M\\,dx + N\\,dy")} with ${m("M_y = N_x")}?`,
      ...rec.why,
    ],
    meta: { variant: "recognize", cls, f: rec.f, form: rec.form, M: rec.M, N: rec.N },
  };
}

const G_X = [
  { tex: "x", js: "x" },
  { tex: "x^{2}", js: "x^2" },
  { tex: "e^{x}", js: "exp(x)" },
  { tex: "\\cos x", js: "cos(x)" },
  { tex: "x^{3}", js: "x^3" },
];
function recogSeparable(r: Rng): Draft {
  const g = r.pick(G_X);
  const h = r.pick([
    { tex: "(1 + y^{2})", js: "(1 + y^2)", expand: true },
    { tex: "e^{-y}", js: "exp(-y)", expand: false },
    { tex: "e^{y}", js: "exp(y)", expand: false },
    { tex: "\\cos y", js: "cos(y)", expand: false },
    { tex: "(y^{2} + 4)", js: "(y^2 + 4)", expand: true },
  ]);
  require_(!(g.js === "exp(x)" && h.js.startsWith("exp")));
  const c = r.pick([1, 2, 3, -1]);
  const hidden = h.expand && g.tex !== "\\cos x" && r.chance(0.5);
  const k = h.js === "(1 + y^2)" ? 1 : 4;
  const rhs = hidden ? join([ct(c, `${g.tex}y^{2}`), ct(c * k, g.tex)]) : g.tex === "\\cos x" ? ct(c, `${h.tex}\\cos x`) : ct(c, `${g.tex}${h.tex}`);
  return recogDraft(0, {
    tex: `y' = ${rhs}`,
    f: `(${c})*${g.js}*${h.js}`,
    form: "explicit",
    why: [`It factors as ${m(`(${ct(c, g.tex)})\\cdot ${h.tex}`)}: a function of ${m("x")} times a function of ${m("y")}.`, `Separate: ${m(`\\frac{dy}{${h.tex}} = ${ct(c, g.tex)}\\,dx`)} and integrate.`],
  });
}

function recogLinear(r: Rng): Draft {
  const pk = r.pick(["const", "overx", "x"]);
  const k = r.pick([1, 2, 3, -1, -2]);
  const rr = r.pick([
    { tex: "x^{2}", js: "x^2" },
    { tex: "e^{x}", js: "exp(x)" },
    { tex: "\\sin x", js: "sin(x)" },
    { tex: "x^{3}", js: "x^3" },
    { tex: "e^{-x}", js: "exp(-x)" },
  ]);
  const p = pk === "const" ? { tex: `${k}`, js: `${k}` } : pk === "overx" ? { tex: coefOver(q(k), "", "x"), js: `${k}/x` } : { tex: ct(k, "x"), js: `${k}*x` };
  // avoid p and r proportional (that is separable): e^{-x}·const never matches p; x^2 vs kx no
  let tex: string;
  if (pk === "overx" && rr.js.startsWith("x^") && r.chance(0.5)) {
    const pow = Number(rr.js.slice(2));
    tex = `xy' ${k < 0 ? "-" : "+"} ${ct(Math.abs(k), "y")} = x^{${pow + 1}}`;
  } else if (r.chance(0.3)) {
    tex = `y' = ${rr.tex} ${k < 0 ? "+" : "-"} ${ct(Math.abs(k), pk === "const" ? "y" : pk === "overx" ? "\\frac{y}{x}" : "xy")}`;
  } else {
    tex = `y' ${k < 0 ? "-" : "+"} ${pk === "const" ? ct(Math.abs(k), "y") : pk === "overx" ? `\\frac{${Math.abs(k)}}{x}y` : ct(Math.abs(k), "xy")} = ${rr.tex}`;
  }
  return recogDraft(2, {
    tex,
    f: `${rr.js} - (${p.js})*y`,
    form: "explicit",
    why: [`It has the form ${m("y' + p(x)y = r(x)")} with ${m(`p = ${p.tex}`)}, ${m(`r = ${rr.tex}`)}: ${m("y")} and ${m("y'")} appear only to the first power.`, `Integrating factor ${m("e^{\\int p\\,dx}")}.`],
  });
}

function recogBernoulli(r: Rng): Draft {
  const n = r.pick([2, 3, 2]);
  const pk = r.pick(["const", "overx"]);
  const k = r.pick([1, 2, 3, -1]);
  const g = r.pick([
    { tex: "x", js: "x" },
    { tex: "x^{2}", js: "x^2" },
    { tex: "e^{x}", js: "exp(x)" },
    { tex: "x^{3}", js: "x^3" },
  ]);
  const yn = `y^{${n}}`;
  const pTex = pk === "const" ? ct(Math.abs(k), "y") : `\\frac{${Math.abs(k)}}{x}y`;
  const pJs = pk === "const" ? `${k}` : `${k}/x`;
  const tex = `y' ${k < 0 ? "-" : "+"} ${pTex} = ${g.tex}${yn}`;
  return recogDraft(3, {
    tex,
    f: `${g.js}*y^${n} - (${pJs})*y`,
    form: "explicit",
    why: [`Linear except for the ${m(yn)} on the right: ${m("y' + p(x)y = g(x)y^n")} with ${m(`n = ${n}`)}.`, `Set ${m(`u = y^{1-n} = y^{${1 - n}}`)} to make it linear.`],
  });
}

function recogSubstitution(r: Rng): Draft {
  const kind = r.pick(["ratio", "ratio", "exp", "square", "lin-ratio"]);
  if (kind === "ratio") {
    // y' = (ax + by)/(cx + dy), not exact as (ax+by)dx - (cx+dy)dy, not degenerate
    const a = r.nz(-3, 3), b = r.nz(-3, 3), c = r.nz(-3, 3), d = r.nz(-3, 3);
    require_(b !== -c && a * d !== b * c);
    const num = join([ct(a, "x"), ct(b, "y")]);
    const den = join([ct(c, "x"), ct(d, "y")]);
    const diffForm = r.chance(0.4);
    const negDen = join([ct(-c, "x"), ct(-d, "y")]);
    return recogDraft(1, {
      tex: diffForm ? `(${num})\\,dx + (${negDen})\\,dy = 0` : `y' = \\frac{${num}}{${den}}`,
      f: `((${a})*x + (${b})*y)/((${c})*x + (${d})*y)`,
      form: diffForm ? "diff" : "explicit",
      M: diffForm ? `(${a})*x + (${b})*y` : undefined,
      N: diffForm ? `(${-c})*x + (${-d})*y` : undefined,
      why: [
        ...(diffForm ? [`Not exact: ${m(`M_y = ${b} \\ne ${-c} = N_x`)}.`] : []),
        `Divide top and bottom by ${m("x")}: ${m("y'")} is a function of ${m("y/x")} alone (homogeneous).`,
        `Set ${m("y = ux")}: ${m("u + xu' = f(u)")} is separable.`,
      ],
    });
  }
  if (kind === "exp") {
    const k = r.pick([1, 2, 3]);
    return recogDraft(1, {
      tex: `y' = \\frac{y}{x} + ${ct(k, "e^{-y/x}")}`,
      f: `y/x + (${k})*exp(-y/x)`,
      form: "explicit",
      why: [`Everything is a function of ${m("y/x")}.`, `${m("y = ux")} gives ${m(`xu' = ${ct(k, "e^{-u}")}`)}, separable.`],
    });
  }
  const a = r.pick([1, 2, -1, -2]);
  const b = r.int(-3, 3);
  const v = join([ct(a, "x"), "y", b ? `${b}` : ""]);
  if (kind === "square") {
    return recogDraft(1, {
      tex: `y' = (${v})^{2}`,
      f: `((${a})*x + y + (${b}))^2`,
      form: "explicit",
      why: [`The right side depends only on ${m(`v = ${v}`)}.`, `${m(`v' = ${a} + y' = ${a} + v^2`)}: separable in ${m("v")}.`],
    });
  }
  const c2 = r.int(-3, 3);
  require_(c2 !== b);
  const v2 = join([ct(a, "x"), "y", c2 ? `${c2}` : ""]);
  return recogDraft(1, {
    tex: `y' = \\frac{${v}}{${v2}}`,
    f: `((${a})*x + y + (${b}))/((${a})*x + y + (${c2}))`,
    form: "explicit",
    why: [`Top and bottom both contain ${m(`${ct(a, "x")} + y`)}: set ${m(`v = ${ct(a, "x")} + y`)}.`, `${m(`v' = ${a} + y'`)} is a function of ${m("v")} alone: separable.`],
  });
}

/** numeric guard: does y' = f(x, y) also fit separable / linear / homogeneous / f(ax + by)? */
function fitsOtherClass(fJs: string): boolean {
  const c = math.compile(fJs);
  const f = (x: number, y: number) => real(c.evaluate({ x, y }));
  const h = 1e-4;
  const flags = { sep: true, lin: true, hom: true, arg: true };
  let ratio0: number | null = null;
  let n = 0;
  for (const [x, y] of [[0.7, 1.3], [1.4, 0.6], [0.9, 2.2], [1.9, 1.1], [1.2, 1.7]]) {
    const f0 = f(x, y);
    const fx = (f(x + h, y) - f(x - h, y)) / (2 * h);
    const fy = (f(x, y + h) - f(x, y - h)) / (2 * h);
    const fyy = (f(x, y + h) - 2 * f0 + f(x, y - h)) / (h * h);
    const fxy = (f(x + h, y + h) - f(x + h, y - h) - f(x - h, y + h) + f(x - h, y - h)) / (4 * h * h);
    if (![f0, fx, fy, fyy, fxy].every(Number.isFinite) || Math.abs(fy) < 1e-9) continue;
    n++;
    const rel = (a: number, b: number) => Math.abs(a - b) / Math.max(Math.abs(a), Math.abs(b), 1e-9);
    if (rel(f0 * fxy, fx * fy) > 1e-4) flags.sep = false;
    if (Math.abs(fyy) > 1e-4 * Math.max(Math.abs(f0), Math.abs(fy), 1)) flags.lin = false;
    if (Math.abs(x * fx + y * fy) > 1e-5 * Math.max(Math.abs(x * fx), Math.abs(y * fy), 1e-9)) flags.hom = false;
    const ratio = fx / fy;
    if (ratio0 === null) ratio0 = ratio;
    else if (rel(ratio, ratio0) > 1e-5) flags.arg = false;
  }
  return n < 3 || flags.sep || flags.lin || flags.hom || flags.arg;
}

function recogExact(r: Rng): Draft {
  const F = combine([mono(coefNz(r), r.int(1, 3), r.int(2, 3)), mixedTranscendental(r, false), ...(r.chance(0.5) ? [mono(coefNz(r), r.int(1, 3), 0)] : [])]);
  const M = diff(F, "x"), N = diff(F, "y");
  require_(M.length > 0 && N.length > 0 && !fitsOtherClass(`-(${exJs(M)})/(${exJs(N)})`));
  return recogDraft(4, {
    tex: `${P(exTex(M))}\\,dx + ${P(exTex(N))}\\,dy = 0`,
    f: `-(${exJs(M)})/(${exJs(N)})`,
    form: "diff",
    M: exJs(M),
    N: exJs(N),
    why: [`${m(`M_y = ${exTex(diff(M, "y"))} = N_x`)}: exact (and it is neither separable nor linear in ${m("y")}).`, `Solve by ${m("u = \\int M\\,dx + k(y)")}: here ${m(`u = ${exTex(F)}`)}.`],
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// Named templates (referenced from drills/live/calc-ode1.yaml)
// ═══════════════════════════════════════════════════════════════════════════
export const CALC_ODE1_TEMPLATES: Record<string, (r: Rng) => Draft> = {
  "usub-poly": usubPoly,
  "usub-exp": usubExp,
  "usub-trig": usubTrig,
  "usub-log": usubLog,
  "usub-ratio": usubRatio,
  "usub-linear": usubLinear,
  "parts-x-exp": partsXExp,
  "parts-x-trig": partsXTrig,
  "parts-x-log": partsLog,
  "parts-tabular": partsTabular,
  "parts-exp-trig": partsExpTrig,
  "parts-inverse": partsInverse,
  "pf-distinct": pfDistinct,
  "pf-repeated": pfRepeated,
  "pf-three": pfThree,
  "pf-irreducible": pfIrreducible,
  "pf-improper": pfImproper,
  "pf-coeffs": pfCoeffs,
  "euler-rect": complexRect,
  "euler-polar": complexPolar,
  "euler-demoivre": complexDeMoivre,
  "euler-quad-roots": complexQuadRoots,
  "euler-re-im": complexReIm,
  "sigma-shift-down": (r) => sigmaReindex(r, "down"),
  "sigma-shift-up": (r) => sigmaReindex(r, "up"),
  "sigma-prefactor": (r) => sigmaReindex(r, "pre"),
  "sigma-derivative": sigmaDerivative,
  "sigma-combine": sigmaCombine,
  "mv-partial": mvPartial,
  "mv-mixed": mvMixed,
  "mv-implicit": mvImplicit,
  "mv-exact-test": mvExactTest,
  "exact-poly": exactPoly,
  "exact-trans": exactTrans,
  "exact-exy": exactExy,
  "exact-ivp": exactIvp,
  "if-factor-x": (r) => ifFactor(r, "x"),
  "if-factor-y": (r) => ifFactor(r, "y"),
  "if-solve": ifSolve,
  "if-test": ifTest,
  "model-mixing": modelMixing,
  "model-cooling": modelCooling,
  "model-decay": modelDecay,
  "model-logistic": modelLogistic,
  "recog-separable": recogSeparable,
  "recog-substitution": recogSubstitution,
  "recog-linear": recogLinear,
  "recog-bernoulli": recogBernoulli,
  "recog-exact": recogExact,
};
