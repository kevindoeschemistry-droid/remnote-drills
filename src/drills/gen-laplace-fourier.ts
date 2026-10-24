// Kreyszig 10e Ch 6 (Laplace transforms), §11.1–11.3 (Fourier series), Ch 12 (separation of
// variables), §5.2 / §5.4 (Legendre, Bessel), Level 1.
//
// Everything is built backward from a clean answer: pick f(t) (or y(t), or u(x, t)), then
// compute the transform / the equation / the initial data shown in the prompt.
import { Rng } from "./rng";
import type { Draft } from "./types";
import { ct, join, m } from "./tex";
import { Q, qterm } from "./rational";
import { require_ } from "./reject";

const LT = "\\mathcal{L}";
const fact = (p: number): number => (p <= 1 ? 1 : p * fact(p - 1));

// ── polynomials in s (integer coefficients, index = power) ─────────────────
type Poly = number[];
const trim = (p: Poly) => {
  const q = [...p];
  while (q.length > 1 && q[q.length - 1] === 0) q.pop();
  return q;
};
const padd = (a: Poly, b: Poly): Poly =>
  trim(Array.from({ length: Math.max(a.length, b.length) }, (_, i) => (a[i] ?? 0) + (b[i] ?? 0)));
const pscale = (a: Poly, k: number): Poly => trim(a.map((c) => c * k));
const pmul = (a: Poly, b: Poly): Poly => {
  const out = new Array(a.length + b.length - 1).fill(0);
  a.forEach((x, i) => b.forEach((y, j) => (out[i + j] += x * y)));
  return trim(out);
};
const pval = (p: Poly, v: number) => p.reduce((s, c, i) => s + c * v ** i, 0);
const lin = (k: number): Poly => [-k, 1];
const quad = (k: number, w: number): Poly => padd(pmul(lin(k), lin(k)), [w * w]);

function ptex(p: Poly, v = "s"): string {
  const terms: string[] = [];
  for (let i = p.length - 1; i >= 0; i--) terms.push(i === 0 ? `${p[i]}` : ct(p[i], i === 1 ? v : `${v}^{${i}}`));
  return join(terms);
}
const pjs = (p: Poly, v = "s") => `(${p.map((c, i) => `(${c})*${v}^${i}`).join(" + ")})`;

/** s - k, s + 2, s */
const linTex = (k: number, v = "s") => (k === 0 ? v : k > 0 ? `${v} - ${k}` : `${v} + ${-k}`);
/** factor for a product: s, (s - 2) */
const fac = (k: number) => (k === 0 ? "s" : `(${linTex(k)})`);
/** (s - k)^e, s^e */
const facPow = (k: number, e: number) => (e === 1 ? (k === 0 ? "s" : linTex(k)) : k === 0 ? `s^{${e}}` : `(${linTex(k)})^{${e}}`);
const quadTex = (k: number, w: number) => (k === 0 ? `s^{2} + ${w * w}` : `(${linTex(k)})^{2} + ${w * w}`);

/** true if the LaTeX has a + or - outside all brackets (after the first character) */
function topLevel(s: string): boolean {
  let d = 0;
  for (let i = 0; i < s.length; i++) {
    const ch = s[i];
    if (ch === "(" || ch === "{" || ch === "[") d++;
    else if (ch === ")" || ch === "}" || ch === "]") d--;
    else if ((ch === "+" || ch === "-") && d === 0 && i > 0) return true;
  }
  return false;
}

/** exponent k·(inner) with no redundant parentheses: t - \tau, -(t - \tau), 2(t - \tau) */
const kArg = (k: number, inner: string) => (k === 1 ? inner : ct(k, `(${inner})`));

/** c · num/den as one signed LaTeX fraction term (for join) */
function fr(c: Q, num: string, den: string): string {
  if (c.isZero()) return "0";
  const a = Math.abs(c.n);
  const top = num === "1" ? `${a}` : a === 1 ? num : topLevel(num) ? `${a}(${num})` : `${a}${num}`;
  const bot = c.d === 1 ? den : topLevel(den) ? `${c.d}(${den})` : `${c.d}${den}`;
  return `${c.n < 0 ? "-" : ""}\\frac{${top}}{${bot}}`;
}

/** q · top / bot for Fourier coefficients:  -\frac{4(-1)^{n}}{n^{2}} */
const b0 = (q: Q) => Math.abs(q.n) === 1;
function cf(q: Q, top: string, bot: string): string {
  if (q.isZero()) return "0";
  const a = Math.abs(q.n);
  const wrapped = /^\((.*)\)$/.exec(top);
  const bare = wrapped && !/[()]/.test(wrapped[1].replace(/\(-1\)/g, "")) ? wrapped[1] : top;
  const t = a === 1 && top ? (b0(q) ? bare : top) : `${a}${top}`;
  const b = q.d === 1 ? bot : `${q.d}${bot}`;
  return `${q.n < 0 ? "-" : ""}${b ? `\\frac{${t}}{${b}}` : t}`;
}

// ── time-domain terms and their transforms ─────────────────────────────────
//   exp  e^{kt}            <->  1/(s - k)
//   pow  t^p e^{kt}        <->  p!/(s - k)^{p+1}
//   cos  e^{kt} cos wt     <->  (s - k)/((s - k)^2 + w^2)
//   sin  e^{kt} sin wt     <->  w/((s - k)^2 + w^2)
//   tcos / tsin  t cos wt, t sin wt (time domain only)
interface Term {
  c: Q;
  f: "exp" | "pow" | "cos" | "sin" | "tcos" | "tsin";
  k: number;
  p?: number;
  w?: number;
}
const T = (c: number | Q, f: Term["f"], k = 0, extra: { p?: number; w?: number } = {}): Term => ({ c: Q.of(c), f, k, ...extra });

function tBody(t: Term, a = 0): string {
  const V = a ? `(t - ${a})` : "t";
  const Vin = a ? `t - ${a}` : "t";
  const E = t.k ? `e^{${Math.abs(t.k) === 1 && a ? `${t.k < 0 ? "-" : ""}${t.k < 0 ? V : Vin}` : ct(t.k, V)}}` : "";
  const w = t.w ?? 1;
  const trig = (fn: string) => (a ? `\\${fn}(${w === 1 ? Vin : `${w}${V}`})` : `\\${fn} ${w === 1 ? "" : w}t`);
  switch (t.f) {
    case "exp": return E;
    case "pow": return `${t.p === 1 ? V : `${V}^{${t.p}}`}${E}`;
    case "cos": return `${E}${trig("cos")}`;
    case "sin": return `${E}${trig("sin")}`;
    case "tcos": return `t\\cos ${w === 1 ? "" : w}t`;
    case "tsin": return `t\\sin ${w === 1 ? "" : w}t`;
  }
}
/** time-domain term; shifted by a: g(t - a) u(t - a) */
const tTex = (t: Term, a = 0) => qterm(t.c, `${tBody(t, a)}${a ? `u(t - ${a})` : ""}`);
function tJs(t: Term, a = 0): string {
  const V = a ? `(t-${a})` : "t";
  const E = `exp((${t.k})*${V})`;
  const w = t.w ?? 1;
  const body = {
    exp: E,
    pow: `${V}^${t.p}*${E}`,
    cos: `${E}*cos((${w})*${V})`,
    sin: `${E}*sin((${w})*${V})`,
    tcos: `t*cos((${w})*t)`,
    tsin: `t*sin((${w})*t)`,
  }[t.f];
  return `${t.c.js()}*${body}${a ? `*heaviside(t-${a})` : ""}`;
}
const tSum = (ts: Term[], a = 0) => join(ts.map((t) => tTex(t, a)));
const tSumJs = (ts: Term[], a = 0) => ts.map((t) => tJs(t, a)).join(" + ");

function sTex(t: Term): string {
  const w = t.w ?? 1;
  switch (t.f) {
    case "exp": return fr(t.c, "1", facPow(t.k, 1));
    case "pow": return fr(t.c.mul(fact(t.p!)), "1", facPow(t.k, t.p! + 1));
    case "cos": return fr(t.c, linTex(t.k), quadTex(t.k, w));
    case "sin": return fr(t.c.mul(w), "1", quadTex(t.k, w));
    default: throw new Error("no transform tex for " + t.f);
  }
}
function sJs(t: Term): string {
  const w = t.w ?? 1;
  const sk = `(s-(${t.k}))`;
  switch (t.f) {
    case "exp": return `${t.c.js()}/${sk}`;
    case "pow": return `${t.c.js()}*${fact(t.p!)}/${sk}^${t.p! + 1}`;
    case "cos": return `${t.c.js()}*${sk}/(${sk}^2+${w * w})`;
    case "sin": return `${t.c.js()}*${w}/(${sk}^2+${w * w})`;
    default: throw new Error("no transform js for " + t.f);
  }
}
const sSum = (ts: Term[]) => join(ts.map(sTex));
const sSumJs = (ts: Term[]) => ts.map(sJs).join(" + ");

/** numerator / denominator polynomials of one transform term (integer c) */
function sNumDen(t: Term): { num: Poly; den: Poly; denTex: string } {
  require_(t.c.isInt());
  const c = t.c.n;
  const w = t.w ?? 1;
  switch (t.f) {
    case "exp": return { num: [c], den: lin(t.k), denTex: fac(t.k) };
    case "pow": {
      let den: Poly = [1];
      for (let i = 0; i <= t.p!; i++) den = pmul(den, lin(t.k));
      return { num: [c * fact(t.p!)], den, denTex: facPow(t.k, t.p! + 1) };
    }
    case "cos": return { num: pscale(lin(t.k), c), den: quad(t.k, w), denTex: `(${quadTex(t.k, w)})` };
    case "sin": return { num: [c * w], den: quad(t.k, w), denTex: `(${quadTex(t.k, w)})` };
    default: throw new Error("no transform for " + t.f);
  }
}

/** Σ terms over the product of their (distinct) denominators */
function combine(ts: Term[]): { N: Poly; D: Poly; Dtex: string } {
  const parts = ts.map(sNumDen);
  let D: Poly = [1];
  for (const p of parts) D = pmul(D, p.den);
  let N: Poly = [0];
  parts.forEach((p, i) => {
    let prod = p.num;
    parts.forEach((q, j) => {
      if (j !== i) prod = pmul(prod, q.den);
    });
    N = padd(N, prod);
  });
  return { N, D, Dtex: parts.map((p) => p.denTex).join("") };
}
const ratTex = (N: Poly, Dtex: string) => `\\frac{${ptex(N)}}{${Dtex}}`;
const ratJs = (N: Poly, D: Poly) => `${pjs(N)}/${pjs(D)}`;

const sExpr = (ref: string) => ({ kind: "expression" as const, ref, vars: ["s"], label: "F(s)" });
const tExpr = (ref: string, points?: Record<string, number>[]) => ({ kind: "expression" as const, ref, vars: ["t"], label: "f(t)", ...(points ? { points } : {}) });
/** sample times on both sides of a unit step at t = a */
const stepPoints = (a: number) => [-0.6, -0.25, 0.15, 0.45, 0.8, 1.3, 1.9].map((d) => ({ t: a + d }));

// ══ laplace.table ══════════════════════════════════════════════════════════
const TABLE = `Table: ${m(`${LT}\\{1\\} = \\frac{1}{s}`)}, ${m(`${LT}\\{t^{n}\\} = \\frac{n!}{s^{n+1}}`)}, ${m(`${LT}\\{e^{at}\\} = \\frac{1}{s - a}`)}.`;

function ltLinear(r: Rng): Draft {
  const k = r.nz(-4, 4);
  const ts = [T(r.nz(-6, 6), "exp"), T(r.nz(-5, 5), "pow", 0, { p: 1 }), T(r.nz(-4, 4), "exp", k)];
  return {
    prompt: `Find ${m(`F(s) = ${LT}\\{f(t)\\}`)} for ${m(`f(t) = ${tSum(ts)}`)}.`,
    answer: sExpr(sSumJs(ts)),
    answerTex: `F(s) = ${sSum(ts)}`,
    steps: [
      `Linearity: transform term by term, ${m(`${LT}\\{af + bg\\} = aF + bG`)}.`,
      TABLE,
      m(`F(s) = ${sSum(ts)}`),
    ],
    meta: { f: tSumJs(ts) },
  };
}

function ltTrig(r: Rng): Draft {
  const w = r.int(1, 5);
  const A = r.nz(-5, 5), B = r.nz(-5, 5);
  const ts = [T(A, "cos", 0, { w }), T(B, "sin", 0, { w })];
  const { N } = combine([ts[0]]);
  const num = padd(N, [B * w]);
  const F = `\\frac{${ptex(num)}}{s^{2} + ${w * w}}`;
  return {
    prompt: `Find ${m(`${LT}\\{f(t)\\}`)} for ${m(`f(t) = ${tSum(ts)}`)}.`,
    answer: sExpr(`${pjs(num)}/(s^2+${w * w})`),
    answerTex: `F(s) = ${F}`,
    steps: [
      `Table: ${m(`${LT}\\{\\cos\\omega t\\} = \\frac{s}{s^{2} + \\omega^{2}}`)}, ${m(`${LT}\\{\\sin\\omega t\\} = \\frac{\\omega}{s^{2} + \\omega^{2}}`)}, here ${m(`\\omega = ${w}`)}.`,
      m(`F(s) = ${sSum(ts)}`),
      `Over the common denominator: ${m(`F(s) = ${F}`)}`,
    ],
    meta: { f: tSumJs(ts) },
  };
}

function ltPower(r: Rng): Draft {
  const p = r.int(2, 4);
  const q = r.int(0, 1);
  const ts = [T(r.nz(-4, 4), "pow", 0, { p }), q === 0 ? T(r.nz(-6, 6), "exp") : T(r.nz(-6, 6), "pow", 0, { p: 1 })];
  return {
    prompt: `Find ${m(`${LT}\\{f(t)\\}`)} for ${m(`f(t) = ${tSum(ts)}`)}.`,
    answer: sExpr(sSumJs(ts)),
    answerTex: `F(s) = ${sSum(ts)}`,
    steps: [
      `${m(`${LT}\\{t^{n}\\} = \\frac{n!}{s^{n+1}}`)}: ${m(`${LT}\\{t^{${p}}\\} = \\frac{${fact(p)}}{s^{${p + 1}}}`)}, ${m(q ? `${LT}\\{t\\} = \\frac{1}{s^{2}}` : `${LT}\\{1\\} = \\frac{1}{s}`)}.`,
      `Multiply by the coefficients (linearity): ${m(`F(s) = ${sSum(ts)}`)}`,
    ],
    meta: { f: tSumJs(ts) },
  };
}

function ltHyperbolic(r: Rng): Draft {
  const k = r.int(1, 4);
  const A = r.nz(-5, 5), B = r.nz(-5, 5);
  const kt = k === 1 ? "t" : `${k}t`;
  const fTex = join([ct(A, `\\cosh ${kt}`), ct(B, `\\sinh ${kt}`)]);
  const num: Poly = [B * k, A];
  const F = `\\frac{${ptex(num)}}{s^{2} - ${k * k}}`;
  return {
    prompt: `Find ${m(`${LT}\\{f(t)\\}`)} for ${m(`f(t) = ${fTex}`)}.`,
    answer: sExpr(`${pjs(num)}/(s^2-${k * k})`),
    answerTex: `F(s) = ${F}`,
    steps: [
      `${m(`\\cosh at = \\tfrac12(e^{at} + e^{-at})`)}, so ${m(`${LT}\\{\\cosh at\\} = \\frac{s}{s^{2} - a^{2}}`)} and ${m(`${LT}\\{\\sinh at\\} = \\frac{a}{s^{2} - a^{2}}`)}.`,
      `With ${m(`a = ${k}`)}: ${m(`F(s) = ${join([fr(new Q(A), "s", `s^{2} - ${k * k}`), fr(new Q(B * k), "1", `s^{2} - ${k * k}`)])}`)}`,
      m(`F(s) = ${F}`),
    ],
    meta: { f: `(${A})*cosh(${k}*t) + (${B})*sinh(${k}*t)` },
  };
}

function ltIdentity(r: Rng): Draft {
  const w = r.int(1, 3);
  const c = r.pick([1, 1, 2, 3, -1, 4]);
  const v = r.int(0, 2);
  const wt = w === 1 ? "t" : `${w}t`;
  const w2 = 2 * w;
  const den = `s(s^{2} + ${4 * w * w})`;
  const denJs = `(s*(s^2+${4 * w * w}))`;
  const cc = ct(c, "");
  const pre = c === 1 ? "" : c === -1 ? "-" : `${c}`;
  if (v === 0) {
    const F = fr(new Q(2 * w * w * c), "1", den);
    return {
      prompt: `Find ${m(`${LT}\\{f(t)\\}`)} for ${m(`f(t) = ${pre}\\sin^{2} ${wt}`)}.`,
      answer: sExpr(`${2 * w * w * c}/${denJs}`),
      answerTex: `F(s) = ${F}`,
      steps: [
        `Not in the table as it stands — use ${m("\\sin^{2}\\theta = \\tfrac12(1 - \\cos 2\\theta)")}: ${m(`f = \\tfrac{${cc}}{2}(1 - \\cos ${w2}t)`)}.`,
        m(`F(s) = \\tfrac{${cc}}{2}\\left(\\frac{1}{s} - \\frac{s}{s^{2} + ${4 * w * w}}\\right)`),
        `Common denominator: ${m(`F(s) = ${F}`)}`,
      ],
      meta: { f: `(${c})*sin(${w}*t)^2` },
    };
  }
  if (v === 1) {
    const num: Poly = pscale([2 * w * w, 0, 1], c);
    const F = `\\frac{${ptex(num)}}{${den}}`;
    return {
      prompt: `Find ${m(`${LT}\\{f(t)\\}`)} for ${m(`f(t) = ${pre}\\cos^{2} ${wt}`)}.`,
      answer: sExpr(`${pjs(num)}/${denJs}`),
      answerTex: `F(s) = ${F}`,
      steps: [
        `Use ${m("\\cos^{2}\\theta = \\tfrac12(1 + \\cos 2\\theta)")}: ${m(`f = \\tfrac{${cc}}{2}(1 + \\cos ${w2}t)`)}.`,
        m(`F(s) = \\tfrac{${cc}}{2}\\left(\\frac{1}{s} + \\frac{s}{s^{2} + ${4 * w * w}}\\right)`),
        `Common denominator: ${m(`F(s) = ${F}`)}`,
      ],
      meta: { f: `(${c})*cos(${w}*t)^2` },
    };
  }
  const F = fr(new Q(c * w), "1", `s^{2} + ${4 * w * w}`);
  return {
    prompt: `Find ${m(`${LT}\\{f(t)\\}`)} for ${m(`f(t) = ${pre}\\sin ${wt}\\cos ${wt}`)}.`,
    answer: sExpr(`${c * w}/(s^2+${4 * w * w})`),
    answerTex: `F(s) = ${F}`,
    steps: [
      `Use ${m("\\sin\\theta\\cos\\theta = \\tfrac12\\sin 2\\theta")}: ${m(`f = \\tfrac{${cc}}{2}\\sin ${w2}t`)}.`,
      m(`F(s) = \\tfrac{${cc}}{2}\\cdot\\frac{${w2}}{s^{2} + ${4 * w * w}} = ${F}`),
    ],
    meta: { f: `(${c})*sin(${w}*t)*cos(${w}*t)` },
  };
}

// ══ laplace.inverse ════════════════════════════════════════════════════════
function iltDistinct(r: Rng): Draft {
  const a = r.int(-4, 4), b = r.int(-4, 4);
  require_(a < b);
  const A = r.nz(-5, 5), B = r.nz(-5, 5);
  const ts = [T(A, "exp", a), T(B, "exp", b)];
  const { N, D, Dtex } = combine(ts);
  const show = r.chance(0.5) ? Dtex : ptex(D);
  return {
    prompt: `Find ${m(`f(t) = ${LT}^{-1}\\left\\{${ratTex(N, show)}\\right\\}`)}.`,
    answer: tExpr(tSumJs(ts)),
    answerTex: `f(t) = ${tSum(ts)}`,
    steps: [
      ...(show === Dtex ? [] : [`Factor the denominator: ${m(`${ptex(D)} = ${Dtex}`)}.`]),
      `Partial fractions ${m(`\\frac{A}{${facPow(a, 1)}} + \\frac{B}{${facPow(b, 1)}}`)}; cover-up: ${m(`A = \\frac{${pval(N, a)}}{${a - b}} = ${A}`)}, ${m(`B = \\frac{${pval(N, b)}}{${b - a}} = ${B}`)}.`,
      `${m(`${LT}^{-1}\\{\\frac{1}{s - a}\\} = e^{at}`)}: ${m(`f(t) = ${tSum(ts)}`)}`,
    ],
    meta: { F: ratJs(N, D) },
  };
}

function iltRepeated(r: Rng): Draft {
  const a = r.nz(-4, 4);
  const A = r.nz(-5, 5), B = r.nz(-4, 4);
  const ts = [T(B, "exp", a), T(A, "pow", a, { p: 1 })];
  const N = padd(pscale(lin(a), B), [A]);
  const D = pmul(lin(a), lin(a));
  const show = r.chance(0.5) ? facPow(a, 2) : ptex(D);
  return {
    prompt: `Find ${m(`f(t) = ${LT}^{-1}\\left\\{${ratTex(N, show)}\\right\\}`)}.`,
    answer: tExpr(tSumJs(ts)),
    answerTex: `f(t) = ${tSum(ts)}`,
    steps: [
      ...(show === facPow(a, 2) ? [] : [`The denominator is a perfect square: ${m(`${ptex(D)} = ${facPow(a, 2)}`)}.`]),
      `Write the numerator in powers of ${m(`(${linTex(a)})`)}: ${m(`${ptex(N)} = ${join([ct(B, `(${linTex(a)})`), `${A}`])}`)}, so ${m(`F = ${sSum(ts)}`)}.`,
      `${m(`${LT}^{-1}\\{\\frac{1}{(s - a)^{2}}\\} = te^{at}`)} (s-shifting of ${m("1/s^{2}")}): ${m(`f(t) = ${tSum(ts)}`)}`,
    ],
    meta: { F: ratJs(N, D) },
  };
}

function iltComplex(r: Rng): Draft {
  const p = r.nz(-3, 3), w = r.int(1, 4);
  const C = r.nz(-4, 4), Dd = r.nz(-4, 4);
  const ts = [T(C, "cos", p, { w }), T(Dd, "sin", p, { w })];
  const N = padd(pscale(lin(p), C), [Dd * w]);
  const Den = quad(p, w);
  return {
    prompt: `Find ${m(`f(t) = ${LT}^{-1}\\left\\{\\frac{${ptex(N)}}{${ptex(Den)}}\\right\\}`)}.`,
    answer: tExpr(tSumJs(ts)),
    answerTex: `f(t) = ${tSum(ts)}`,
    steps: [
      `Complex roots — complete the square: ${m(`${ptex(Den)} = ${quadTex(p, w)}`)}.`,
      `Split the numerator around ${m(linTex(p))}: ${m(`${ptex(N)} = ${join([ct(C, `(${linTex(p)})`), `${Dd * w}`])}`)}, so ${m(`F = ${sSum(ts)}`)}.`,
      `s-shifting: ${m(`${LT}^{-1}\\{\\frac{s - a}{(s - a)^{2} + \\omega^{2}}\\} = e^{at}\\cos\\omega t`)}, ${m(`${LT}^{-1}\\{\\frac{\\omega}{(s - a)^{2} + \\omega^{2}}\\} = e^{at}\\sin\\omega t`)}.`,
      m(`f(t) = ${tSum(ts)}`),
    ],
    meta: { F: ratJs(N, Den) },
  };
}

function iltThree(r: Rng): Draft {
  const a = r.nz(-3, 3), b = r.nz(-3, 3);
  require_(a < b);
  const ts = [T(r.nz(-4, 4), "exp", 0), T(r.nz(-4, 4), "exp", a), T(r.nz(-4, 4), "exp", b)];
  const { N, D, Dtex } = combine(ts);
  require_(N.length >= 2);
  const cover = ts.map((t, i) => {
    const others = ts.filter((_, j) => j !== i).reduce((s, u) => s * (t.k - u.k), 1);
    return `${m(`${["A", "B", "C"][i]} = \\frac{${pval(N, t.k)}}{${others}} = ${t.c.tex()}`)}`;
  });
  return {
    prompt: `Find ${m(`f(t) = ${LT}^{-1}\\left\\{${ratTex(N, Dtex)}\\right\\}`)}.`,
    answer: tExpr(tSumJs(ts)),
    answerTex: `f(t) = ${tSum(ts)}`,
    steps: [
      `Three simple factors: ${m(`F = \\frac{A}{s} + \\frac{B}{${linTex(a)}} + \\frac{C}{${linTex(b)}}`)}.`,
      `Cover-up (evaluate the rest of ${m("F")} at each root): ${cover.join(", ")}.`,
      m(`f(t) = ${tSum(ts)}`),
    ],
    meta: { F: ratJs(N, D) },
  };
}

function iltQuadratic(r: Rng): Draft {
  const w = r.int(1, 4);
  const A = r.nz(-4, 4);
  const classic = r.chance(0.5);
  const B = classic ? -A : r.int(-4, 4);
  const C = classic ? 0 : r.nz(-3, 3);
  const ts = [T(A, "exp", 0), T(B, "cos", 0, { w }), T(C, "sin", 0, { w })].filter((t) => !t.c.isZero());
  const N: Poly = trim([A * w * w, C * w, A + B]);
  const D: Poly = [0, w * w, 0, 1];
  const Dtex = `s(s^{2} + ${w * w})`;
  return {
    prompt: `Find ${m(`f(t) = ${LT}^{-1}\\left\\{${ratTex(N, Dtex)}\\right\\}`)}.`,
    answer: tExpr(tSumJs(ts)),
    answerTex: `f(t) = ${tSum(ts)}`,
    steps: [
      `Partial fractions with an irreducible quadratic: ${m(`F = \\frac{A}{s} + \\frac{Bs + C'}{s^{2} + ${w * w}}`)}.`,
      `${m(`A = \\frac{${pval(N, 0)}}{${w * w}} = ${A}`)}; matching ${m("s^{2}")} and ${m("s")} coefficients: ${m(`A + B = ${A + B}`)}, ${m(`C' = ${C * w}`)}, so ${m(`B = ${B}`)}.`,
      m(`F = ${join([fr(new Q(A), "1", "s"), fr(new Q(1), ptex(trim([C * w, B])), `s^{2} + ${w * w}`)])}`),
      m(`f(t) = ${tSum(ts)}`),
    ],
    meta: { F: ratJs(N, D) },
  };
}

// ══ laplace.shifting ═══════════════════════════════════════════════════════
const S_SHIFT = `First shifting theorem: ${m(`${LT}\\{e^{at}f(t)\\} = F(s - a)`)}.`;
const T_SHIFT = `Second shifting theorem: ${m(`${LT}\\{f(t - a)u(t - a)\\} = e^{-as}F(s)`)}.`;

function shiftSFwd(r: Rng): Draft {
  const k = r.nz(-4, 4);
  if (r.chance(0.5)) {
    const p = r.int(1, 3);
    const t = T(r.nz(-4, 4), "pow", k, { p });
    return {
      prompt: `Find ${m(`${LT}\\{f(t)\\}`)} for ${m(`f(t) = ${tTex(t)}`)}.`,
      answer: sExpr(sJs(t)),
      answerTex: `F(s) = ${sTex(t)}`,
      steps: [
        S_SHIFT,
        `${m(`${LT}\\{${tTex(T(t.c, "pow", 0, { p }))}\\} = ${sTex(T(t.c, "pow", 0, { p }))}`)}; replace ${m("s")} by ${m(linTex(k))}.`,
        m(`F(s) = ${sTex(t)}`),
      ],
      meta: { f: tJs(t) },
    };
  }
  const w = r.int(1, 4);
  const ts = [T(r.nz(-4, 4), "cos", k, { w }), T(r.nz(-4, 4), "sin", k, { w })];
  const num = padd(pscale(lin(k), ts[0].c.n), [ts[1].c.n * w]);
  const F = `\\frac{${ptex(num)}}{${quadTex(k, w)}}`;
  const ek = `e^{${ct(k, "t")}}`;
  const inner = join([ct(ts[0].c.n, `\\cos ${w === 1 ? "" : w}t`), ct(ts[1].c.n, `\\sin ${w === 1 ? "" : w}t`)]);
  return {
    prompt: `Find ${m(`${LT}\\{f(t)\\}`)} for ${m(`f(t) = ${ek}(${inner})`)}.`,
    answer: sExpr(sSumJs(ts)),
    answerTex: `F(s) = ${F}`,
    steps: [
      S_SHIFT,
      `Without the exponential: ${m(`${LT}\\{${inner}\\} = \\frac{${ptex(padd(pscale(lin(0), ts[0].c.n), [ts[1].c.n * w]))}}{s^{2} + ${w * w}}`)}.`,
      `Replace ${m("s")} by ${m(linTex(k))}: ${m(`F(s) = ${sSum(ts)} = ${F}`)}`,
    ],
    meta: { f: tSumJs(ts) },
  };
}

function shiftSInv(r: Rng): Draft {
  const k = r.nz(-4, 4);
  const v = r.int(0, 2);
  let ts: Term[];
  let Ftex: string, Fjs: string, base: string;
  if (v === 0) {
    const p = r.int(1, 3);
    ts = [T(r.nz(-3, 3), "pow", k, { p })];
    Ftex = sTex(ts[0]);
    Fjs = sJs(ts[0]);
    base = `${m(`${LT}^{-1}\\{\\frac{${fact(p)}}{s^{${p + 1}}}\\} = t^{${p}}`)}`;
  } else if (v === 1) {
    const w = r.int(1, 4);
    ts = [T(r.nz(-4, 4), "sin", k, { w })];
    Ftex = sTex(ts[0]);
    Fjs = sJs(ts[0]);
    base = `${m(`${LT}^{-1}\\{\\frac{\\omega}{s^{2} + \\omega^{2}}\\} = \\sin\\omega t`)}, ${m(`\\omega = ${w}`)}`;
  } else {
    const w = r.int(1, 4);
    ts = [T(r.nz(-4, 4), "cos", k, { w }), T(r.nz(-4, 4), "sin", k, { w })];
    const num = padd(pscale(lin(k), ts[0].c.n), [ts[1].c.n * w]);
    Ftex = `\\frac{${ptex(num)}}{${quadTex(k, w)}}`;
    Fjs = sSumJs(ts);
    base = `split the numerator: ${m(`${ptex(num)} = ${join([ct(ts[0].c.n, `(${linTex(k)})`), `${ts[1].c.n * w}`])}`)}, then cosine and sine entries with ${m(`\\omega = ${w}`)}`;
  }
  return {
    prompt: `Find ${m(`f(t) = ${LT}^{-1}\\left\\{${Ftex}\\right\\}`)}.`,
    answer: tExpr(tSumJs(ts)),
    answerTex: `f(t) = ${tSum(ts)}`,
    steps: [
      `${S_SHIFT} Read ${m(linTex(k))} as a shifted ${m("s")}: the answer carries ${m(`e^{${ct(k, "t")}}`)}.`,
      `Unshifted: ${base}.`,
      m(`f(t) = ${tSum(ts)}`),
    ],
    meta: { F: Fjs },
  };
}

function shiftTFwd(r: Rng): Draft {
  const a = r.int(1, 3);
  const v = r.int(0, 4);
  const E = `e^{-${a === 1 ? "" : a}s}`;
  const Ejs = `exp(-${a}*s)`;
  if (v === 4) {
    // t u(t - a) = [(t - a) + a] u(t - a)
    const c = r.nz(-3, 3);
    const F = `${E}\\left(${join([fr(new Q(c), "1", "s^{2}"), fr(new Q(c * a), "1", "s")])}\\right)`;
    return {
      prompt: `Find ${m(`${LT}\\{f(t)\\}`)} for ${m(`f(t) = ${ct(c, "t")}\\,u(t - ${a})`)}.`,
      answer: sExpr(`${Ejs}*((${c})/s^2 + (${c * a})/s)`),
      answerTex: `F(s) = ${F}`,
      steps: [
        `${T_SHIFT} The factor multiplying ${m(`u(t - ${a})`)} must be written in ${m(`t - ${a}`)}.`,
        `${m(`t = (t - ${a}) + ${a}`)}, so ${m(`f = ${c === 1 ? "" : c === -1 ? "-" : c}\\big[(t - ${a}) + ${a}\\big]u(t - ${a})`)}.`,
        `Shift ${m(`${LT}\\{t + ${a}\\} = \\frac{1}{s^{2}} + \\frac{${a}}{s}`)}: ${m(`F(s) = ${F}`)}`,
      ],
      meta: { f: `(${c})*t*heaviside(t-${a})` },
    };
  }
  const t =
    v === 0 ? T(r.nz(-5, 5), "exp", 0)
    : v === 1 ? T(r.nz(-3, 3), "pow", 0, { p: r.int(1, 2) })
    : v === 2 ? T(r.nz(-4, 4), "exp", r.nz(-3, 3))
    : T(r.nz(-4, 4), r.pick(["sin", "cos"] as const), 0, { w: r.int(1, 4) });
  const F = `${sTex(t)}\\,${E}`;
  return {
    prompt: `Find ${m(`${LT}\\{f(t)\\}`)} for ${m(`f(t) = ${tTex(t, a)}`)}.`,
    answer: sExpr(`${Ejs}*(${sJs(t)})`),
    answerTex: `F(s) = ${F}`,
    steps: [
      T_SHIFT,
      `Here ${m(`f(t) = g(t - ${a})u(t - ${a})`)} with ${m(`g(t) = ${tTex(t)}`)}, ${m(`G(s) = ${sTex(t)}`)}.`,
      m(`F(s) = ${F}`),
    ],
    meta: { f: tJs(t, a) },
  };
}

function shiftTInv(r: Rng): Draft {
  const a = r.int(1, 3);
  const v = r.int(0, 3);
  const t =
    v === 0 ? T(r.nz(-5, 5), "exp", 0)
    : v === 1 ? T(r.nz(-3, 3), "pow", 0, { p: r.int(1, 2) })
    : v === 2 ? T(r.nz(-4, 4), "exp", r.nz(-3, 3))
    : T(r.nz(-4, 4), r.pick(["sin", "cos"] as const), 0, { w: r.int(1, 3) });
  const E = `e^{-${a === 1 ? "" : a}s}`;
  return {
    prompt: `Find ${m(`f(t) = ${LT}^{-1}\\left\\{${sTex(t)}\\,${E}\\right\\}`)}. Write the unit step as ${m(`u(t - a)`)}.`,
    answer: tExpr(tJs(t, a), stepPoints(a)),
    answerTex: `f(t) = ${tTex(t, a)}`,
    steps: [
      `${T_SHIFT} The factor ${m(E)} means: invert the rest, then shift by ${m(`${a}`)} and switch on at ${m(`t = ${a}`)}.`,
      `${m(`${LT}^{-1}\\left\\{${sTex(t)}\\right\\} = ${tTex(t)}`)}.`,
      `Replace ${m("t")} by ${m(`t - ${a}`)} and multiply by ${m(`u(t - ${a})`)}: ${m(`f(t) = ${tTex(t, a)}`)}`,
    ],
    meta: { F: `exp(-${a}*s)*(${sJs(t)})` },
  };
}

function shiftBox(r: Rng): Draft {
  const v = r.int(0, 2);
  if (v === 0) {
    const a = r.int(0, 2), b = a + r.int(1, 3);
    const K = r.nz(-5, 5);
    const Ea = a ? `e^{-${a === 1 ? "" : a}s}` : "1";
    const Eb = `e^{-${b === 1 ? "" : b}s}`;
    const F = fr(new Q(K), `${Ea} - ${Eb}`, "s");
    return {
      prompt: `Find ${m(`${LT}\\{f(t)\\}`)} for ${m(`f(t) = \\begin{cases} ${K} & ${a} < t < ${b} \\\\ 0 & \\text{otherwise} \\end{cases}`)}.`,
      answer: sExpr(`(${K})*(exp(-${a}*s) - exp(-${b}*s))/s`),
      answerTex: `F(s) = ${F}`,
      steps: [
        `Switch on at ${m(`t = ${a}`)}, off at ${m(`t = ${b}`)}: ${m(`f = ${K}\\big[${a ? `u(t - ${a})` : "1"} - u(t - ${b})\\big]`)}.`,
        `${m(`${LT}\\{u(t - a)\\} = \\frac{e^{-as}}{s}`)}.`,
        m(`F(s) = ${F}`),
      ],
      meta: { f: `(${K})*(heaviside(t-${a}) - heaviside(t-${b}))` },
    };
  }
  const a = r.int(1, 3);
  const E = `e^{-${a === 1 ? "" : a}s}`;
  if (v === 1) {
    const K = r.nz(-5, 5), M = r.nz(-5, 5, [0, K]);
    const F = join([fr(new Q(K), "1", "s"), fr(new Q(M - K), E, "s")]);
    return {
      prompt: `Find ${m(`${LT}\\{f(t)\\}`)} for ${m(`f(t) = \\begin{cases} ${K} & 0 < t < ${a} \\\\ ${M} & t > ${a} \\end{cases}`)}.`,
      answer: sExpr(`(${K})/s + (${M - K})*exp(-${a}*s)/s`),
      answerTex: `F(s) = ${F}`,
      steps: [
        `Start at ${m(`${K}`)} and jump by ${m(`${M - K}`)} at ${m(`t = ${a}`)}: ${m(`f = ${K} ${M - K < 0 ? "-" : "+"} ${Math.abs(M - K)}u(t - ${a})`)}.`,
        `${m(`${LT}\\{u(t - a)\\} = \\frac{e^{-as}}{s}`)}.`,
        m(`F(s) = ${F}`),
      ],
      meta: { f: `(${K}) + (${M - K})*heaviside(t-${a})` },
    };
  }
  const c = r.nz(-3, 3);
  const F = `${fr(new Q(c), "1", "s^{2}")} - ${E}\\left(${join([fr(new Q(c), "1", "s^{2}"), fr(new Q(c * a), "1", "s")])}\\right)`;
  const ct_ = c === 1 ? "" : c === -1 ? "-" : `${c}`;
  return {
    prompt: `Find ${m(`${LT}\\{f(t)\\}`)} for ${m(`f(t) = \\begin{cases} ${ct_}t & 0 < t < ${a} \\\\ 0 & t > ${a} \\end{cases}`)}.`,
    answer: sExpr(`(${c})/s^2 - exp(-${a}*s)*((${c})/s^2 + (${c * a})/s)`),
    answerTex: `F(s) = ${F}`,
    steps: [
      `Switch the ramp off at ${m(`t = ${a}`)}: ${m(`f = ${ct_}t\\big[1 - u(t - ${a})\\big]`)}.`,
      `Write the switched-off part in ${m(`t - ${a}`)}: ${m(`t\\,u(t - ${a}) = \\big[(t - ${a}) + ${a}\\big]u(t - ${a})`)}, whose transform is ${m(`${E}\\left(\\frac{1}{s^{2}} + \\frac{${a}}{s}\\right)`)}.`,
      m(`F(s) = ${F}`),
    ],
    meta: { f: `(${c})*t*(1 - heaviside(t-${a}))` },
  };
}

// ══ laplace.ivp ════════════════════════════════════════════════════════════
interface Ivp {
  b: number;
  c: number;
  rhsTex: string;
  rhsJs?: string;
  ts: Term[]; // y(t)
  N: Poly;
  Dtex: string;
  rhsS: string; // transform of the right side, LaTeX ("" if 0)
}

function ivpDraft(I: Ivp): Draft {
  const y = (t: number) => I.ts.reduce((s, u) => s + u.c.value() * yVal(u, t), 0);
  const h = 1e-6;
  const y0 = Math.round(y(0));
  const y1 = Math.round((y(h) - y(-h)) / (2 * h));
  const eq = `${join(["y''", ct(I.b, "y'"), ct(I.c, "y")])} = ${I.rhsTex}`;
  const sub = `(${ptex([I.c, I.b, 1])})Y = ${join([ptex([I.b * y0 + y1, y0]), I.rhsS])}`;
  return {
    prompt: `Solve by the Laplace transform: ${m(eq)}, ${m(`y(0) = ${y0},\\ y'(0) = ${y1}`)}.`,
    answer: { kind: "ode2", a: 1, b: I.b, c: I.c, v: "t", ...(I.rhsJs ? { rhs: I.rhsJs } : {}), ic: [0, y0, y1], ref: tSumJs(I.ts) },
    answerTex: `y = ${tSum(I.ts)}`,
    steps: [
      `Transform: ${m(`${LT}\\{y''\\} = s^{2}Y - sy(0) - y'(0)`)}, ${m(`${LT}\\{y'\\} = sY - y(0)`)}. Subsidiary equation: ${m(sub)}.`,
      m(`Y = ${ratTex(I.N, I.Dtex)}`),
      `Partial fractions: ${m(`Y = ${sSum(I.ts)}`)}.`,
      m(`y(t) = ${tSum(I.ts)}`),
    ],
    meta: { b: I.b, c: I.c, rhs: I.rhsJs ?? "0", y0, y1 },
  };
}
function yVal(u: Term, t: number): number {
  const w = u.w ?? 1;
  const E = Math.exp(u.k * t);
  return u.f === "exp" ? E : u.f === "pow" ? t ** u.p! * E : u.f === "cos" ? E * Math.cos(w * t) : E * Math.sin(w * t);
}
/** numerator ((s + b)y0 + y1)·extra + forcing */
function ivpNum(b: number, y0: number, y1: number): Poly {
  return [b * y0 + y1, y0];
}

function livpReal(r: Rng): Draft {
  const r1 = r.int(-4, 4), r2 = r.int(-4, 4);
  require_(r1 < r2);
  const ts = [T(r.nz(-4, 4), "exp", r1), T(r.nz(-4, 4), "exp", r2)];
  const b = -(r1 + r2), c = r1 * r2;
  const y0 = ts[0].c.n + ts[1].c.n, y1 = ts[0].c.n * r1 + ts[1].c.n * r2;
  return ivpDraft({ b, c, rhsTex: "0", ts, N: ivpNum(b, y0, y1), Dtex: `${fac(r1)}${fac(r2)}`, rhsS: "" });
}

function livpComplex(r: Rng): Draft {
  const p = r.int(-3, 3), w = r.int(1, 4);
  const C = r.nz(-4, 4), D = r.int(-4, 4);
  const ts = [T(C, "cos", p, { w }), T(D, "sin", p, { w })].filter((t) => !t.c.isZero());
  const b = -2 * p, c = p * p + w * w;
  const y0 = C, y1 = p * C + w * D;
  return ivpDraft({ b, c, rhsTex: "0", ts, N: ivpNum(b, y0, y1), Dtex: quadTex(p, w), rhsS: "" });
}

function livpDouble(r: Rng): Draft {
  const k = r.nz(-3, 3);
  const A = r.nz(-4, 4), B = r.nz(-4, 4);
  const ts = [T(A, "exp", k), T(B, "pow", k, { p: 1 })];
  const b = -2 * k, c = k * k;
  return ivpDraft({ b, c, rhsTex: "0", ts, N: ivpNum(b, A, A * k + B), Dtex: facPow(k, 2), rhsS: "" });
}

function livpExp(r: Rng): Draft {
  const r1 = r.int(-3, 3), r2 = r.int(-3, 3), k = r.int(-3, 3);
  require_(r1 < r2 && k !== r1 && k !== r2);
  const b = -(r1 + r2), c = r1 * r2;
  const P = r.nz(-3, 3);
  const K = P * (k * k + b * k + c);
  const ts = [T(r.int(-3, 3), "exp", r1), T(r.int(-3, 3), "exp", r2), T(P, "exp", k)].filter((t) => !t.c.isZero());
  const y0 = ts.reduce((s, t) => s + t.c.n, 0), y1 = ts.reduce((s, t) => s + t.c.n * t.k, 0);
  const N = padd(pmul(ivpNum(b, y0, y1), lin(k)), [K]);
  const rhsTex = k === 0 ? `${K}` : ct(K, `e^{${ct(k, "t")}}`);
  return ivpDraft({
    b, c, rhsTex, rhsJs: `(${K})*exp((${k})*t)`, ts, N,
    Dtex: `${fac(r1)}${fac(r2)}${fac(k)}`, rhsS: fr(new Q(K), "1", facPow(k, 1)),
  });
}

function livpConst(r: Rng): Draft {
  const w = r.int(1, 4);
  const P = r.nz(-3, 3);
  const K = P * w * w;
  const ts = [T(P, "exp", 0), T(r.int(-3, 3), "cos", 0, { w }), T(r.int(-3, 3), "sin", 0, { w })].filter((t) => !t.c.isZero());
  require_(ts.length >= 2);
  const y0 = ts.filter((t) => t.f !== "sin").reduce((s, t) => s + t.c.n, 0);
  const y1 = ts.filter((t) => t.f === "sin").reduce((s, t) => s + t.c.n * w, 0);
  const N = padd(pmul(ivpNum(0, y0, y1), lin(0)), [K]);
  return ivpDraft({ b: 0, c: w * w, rhsTex: `${K}`, rhsJs: `${K}`, ts, N, Dtex: `s(s^{2} + ${w * w})`, rhsS: fr(new Q(K), "1", "s") });
}

// ══ laplace.convolution ════════════════════════════════════════════════════
interface Fn {
  tex: (v: string) => string; // f(v): v is "t", "\\tau" or "(t - \\tau)"
  js: string; // in t
  term: Term; // its transform as a table term
}
function basicFn(r: Rng): Fn {
  const v = r.int(0, 4);
  if (v === 0) return { tex: () => "1", js: "1", term: T(1, "exp", 0) };
  if (v === 1) return { tex: (x) => (x.startsWith("(") ? x : x), js: "t", term: T(1, "pow", 0, { p: 1 }) };
  if (v === 2) {
    const k = r.nz(-3, 3);
    return { tex: (x) => `e^{${x.startsWith("(") ? kArg(k, x.slice(1, -1)) : ct(k, x)}}`, js: `exp((${k})*t)`, term: T(1, "exp", k) };
  }
  const w = r.int(1, 3);
  const fn = v === 3 ? "sin" : "cos";
  return {
    tex: (x) => `\\${fn}${x.startsWith("(") ? `\\left(${w === 1 ? x.slice(1, -1) : `${w}${x}`}\\right)` : ` ${w === 1 ? "" : w}${x}`}`,
    js: `${fn}((${w})*t)`,
    term: T(1, fn as "sin" | "cos", 0, { w }),
  };
}

function convCompute(r: Rng): Draft {
  const v = r.int(0, 5);
  const c = r.pick([1, 1, 2, 3, -1, -2]);
  const a = r.nz(-3, 3), b = r.nz(-3, 3, [0, a]);
  const w = r.int(1, 3);
  const wt = w === 1 ? "t" : `${w}t`;
  const ea = `e^{${ct(a, "t")}}`;
  const pairs: [string, string, string, string, Term[]][] = [
    // f tex, g tex, f js, g js, result (before × c)
    ["1", ea, "1", `exp((${a})*t)`, [T(new Q(1, a), "exp", a), T(new Q(-1, a), "exp", 0)]],
    [ea, `e^{${ct(b, "t")}}`, `exp((${a})*t)`, `exp((${b})*t)`, [T(new Q(1, a - b), "exp", a), T(new Q(-1, a - b), "exp", b)]],
    ["t", "1", "t", "1", [T(new Q(1, 2), "pow", 0, { p: 2 })]],
    ["1", `\\sin ${wt}`, "1", `sin(${w}*t)`, [T(new Q(1, w), "exp", 0), T(new Q(-1, w), "cos", 0, { w })]],
    ["1", `\\cos ${wt}`, "1", `cos(${w}*t)`, [T(new Q(1, w), "sin", 0, { w })]],
    ["t", ea, "t", `exp((${a})*t)`, [T(new Q(1, a * a), "exp", a), T(new Q(-1, a * a), "exp", 0), T(new Q(-1, a), "pow", 0, { p: 1 })]],
  ];
  const [fT, gT, fJ, gJ, res0] = pairs[v];
  const res = res0.map((t) => ({ ...t, c: t.c.mul(c) }));
  const fTex = c === 1 ? fT : fT === "1" ? `${c}` : `${c === -1 ? "-" : c}${fT}`;
  const FG = {
    0: `\\frac{${c}}{s(${linTex(a)})}`,
    1: `\\frac{${c}}{(${linTex(a)})(${linTex(b)})}`,
    2: `\\frac{${c}}{s^{3}}`,
    3: `\\frac{${c * w}}{s(s^{2} + ${w * w})}`,
    4: `\\frac{${c}}{s^{2} + ${w * w}}`,
    5: `\\frac{${c}}{s^{2}(${linTex(a)})}`,
  }[v];
  return {
    prompt: `Find the convolution ${m("(f * g)(t) = \\int_0^t f(\\tau)\\,g(t - \\tau)\\,d\\tau")} for ${m(`f(t) = ${fTex}`)}, ${m(`g(t) = ${gT}`)}.`,
    answer: tExpr(tSumJs(res)),
    answerTex: `(f * g)(t) = ${tSum(res)}`,
    steps: [
      `Convolution theorem: ${m(`${LT}\\{f * g\\} = F(s)G(s) = ${FG}`)} (or integrate directly).`,
      `Partial fractions: ${m(`F(s)G(s) = ${sSum(res)}`)}.`,
      m(`(f * g)(t) = ${tSum(res)}`),
    ],
    meta: { f: `(${c})*${fJ}`, g: gJ },
  };
}

function convInverse(r: Rng): Draft {
  const v = r.int(0, 4);
  const c = r.pick([1, 1, 2, 3, -1, 4]);
  const a = r.nz(-3, 3), b = r.nz(-3, 3, [0, a]);
  const w = r.int(1, 3);
  const C = new Q(c);
  let Ftex: string, Fjs: string, res: Term[], split: string;
  const wt = w === 1 ? "t" : `${w}t`;
  if (v === 0) {
    Ftex = `\\frac{${c}}{(${linTex(a)})(${linTex(b)})}`;
    Fjs = `${c}/((s-(${a}))*(s-(${b})))`;
    res = [T(C.div(a - b), "exp", a), T(C.div(b - a), "exp", b)];
    split = `${m(`\\frac{1}{${linTex(a)}}\\cdot\\frac{${c}}{${linTex(b)}}`)}: ${m(`f = e^{${ct(a, "t")}} * ${ct(c, `e^{${ct(b, "t")}}`)} = ${c === 1 ? "" : c === -1 ? "-" : c}\\int_0^t e^{${ct(a, "\\tau")}}e^{${kArg(b, "t - \\tau")}}\\,d\\tau`)}`;
  } else if (v === 1) {
    Ftex = `\\frac{${c}}{s(${linTex(a)})}`;
    Fjs = `${c}/(s*(s-(${a})))`;
    res = [T(C.div(a), "exp", a), T(C.div(-a), "exp", 0)];
    split = `${m(`\\frac{${c}}{s}\\cdot\\frac{1}{${linTex(a)}}`)}: ${m(`f = ${c} * e^{${ct(a, "t")}} = ${c === 1 ? "" : c === -1 ? "-" : c}\\int_0^t e^{${ct(a, "\\tau")}}\\,d\\tau`)}`;
  } else if (v === 2) {
    Ftex = `\\frac{${c}}{(s^{2} + ${w * w})^{2}}`;
    Fjs = `${c}/(s^2+${w * w})^2`;
    res = [T(C.div(2 * w ** 3), "sin", 0, { w }), T(C.div(-2 * w * w), "tcos", 0, { w })];
    split = `${m(`\\frac{${c}}{${w * w}}\\cdot\\frac{${w}}{s^{2} + ${w * w}}\\cdot\\frac{${w}}{s^{2} + ${w * w}}`)}: ${m(`f = \\frac{${c}}{${w * w}}\\int_0^t \\sin ${w === 1 ? "" : w}\\tau\\,\\sin\\left(${w === 1 ? "" : w}(t - \\tau)\\right)d\\tau`)}`;
  } else if (v === 3) {
    Ftex = `\\frac{${c}s}{(s^{2} + ${w * w})^{2}}`.replace("{1s}", "{s}");
    Fjs = `${c}*s/(s^2+${w * w})^2`;
    res = [T(C.div(2 * w), "tsin", 0, { w })];
    split = `${m(`\\frac{${c}}{${w}}\\cdot\\frac{s}{s^{2} + ${w * w}}\\cdot\\frac{${w}}{s^{2} + ${w * w}}`)}: ${m(`f = \\frac{${c}}{${w}}\\int_0^t \\cos ${w === 1 ? "" : w}\\tau\\,\\sin\\left(${w === 1 ? "" : w}(t - \\tau)\\right)d\\tau`)}`;
  } else {
    Ftex = `\\frac{${c}}{s^{2}(${linTex(a)})}`;
    Fjs = `${c}/(s^2*(s-(${a})))`;
    res = [T(C.div(a * a), "exp", a), T(C.div(-a * a), "exp", 0), T(C.div(-a), "pow", 0, { p: 1 })];
    split = `${m(`\\frac{${c}}{s^{2}}\\cdot\\frac{1}{${linTex(a)}}`)}: ${m(`f = ${ct(c, "t")} * e^{${ct(a, "t")}} = ${c === 1 ? "" : c === -1 ? "-" : c}\\int_0^t \\tau\\,e^{${kArg(a, "t - \\tau")}}\\,d\\tau`)}`;
  }
  Ftex = Ftex.replace("\\frac{1s}", "\\frac{s}").replace("\\frac{-1s}", "\\frac{-s}");
  return {
    prompt: `Use the convolution theorem to find ${m(`f(t) = ${LT}^{-1}\\left\\{${Ftex}\\right\\}`)}.`,
    answer: tExpr(tSumJs(res)),
    answerTex: `f(t) = ${tSum(res)}`,
    steps: [
      `Convolution theorem: ${m(`${LT}^{-1}\\{F G\\} = f * g`)}. Split ${split}.`,
      `Evaluate the integral (it is ${m("\\tau")}-integration; ${m("t")} is a constant inside).`,
      m(`f(t) = ${tSum(res)}`),
    ],
    meta: { F: Fjs },
  };
}

function convTransform(r: Rng): Draft {
  const f = basicFn(r), g = basicFn(r);
  require_(f.js !== g.js || f.js === "1");
  require_(!(f.js === "1" && g.js === "1"));
  const c = r.pick([1, 1, 2, 3, -2]);
  const ft = { ...f.term, c: new Q(c) };
  const pf = sNumDen(ft), pg = sNumDen(g.term);
  const N = pmul(pf.num, pg.num);
  const D = pmul(pf.den, pg.den);
  const sPow = (t: string) => (t === "s" ? 1 : /^s\^\{(\d+)\}$/.test(t) ? Number(t.slice(3, -1)) : 0);
  const [ef, eg] = [sPow(pf.denTex), sPow(pg.denTex)];
  const dtex =
    ef && eg ? `s^{${ef + eg}}`
    : pf.denTex === pg.denTex ? `${pf.denTex}^{2}`
    : eg && !ef ? `${pg.denTex}${pf.denTex}`
    : `${pf.denTex}${pg.denTex}`;
  const F = ratTex(N, dtex);
  const ftex = f.js === "1" ? (c === 1 ? "" : `${c}`) : c === 1 ? f.tex("\\tau") : `${c === -1 ? "-" : c}${f.tex("\\tau")}`;
  const gtex = g.js === "1" ? "" : g.tex("(t - \\tau)");
  return {
    prompt: `Find ${m(`${LT}\\left\\{\\int_0^t ${[ftex, gtex].filter(Boolean).join("\\,")}\\,d\\tau\\right\\}`)} without evaluating the integral.`,
    answer: sExpr(ratJs(N, D)),
    answerTex: `${F}`,
    steps: [
      `The integral is the convolution ${m("f * g")} with ${m(`f(t) = ${(ftex || "1").replace(/\\tau/g, "t")}`)}, ${m(`g(t) = ${g.js === "1" ? "1" : g.tex("t")}`)}.`,
      `${m(`${LT}\\{f * g\\} = F(s)G(s)`)}: ${m(`F = ${sTex(ft)}`)}, ${m(`G = ${sTex(g.term)}`)}.`,
      `Multiply: ${m(F)}`,
    ],
    meta: { f: `(${c})*${f.js}`, g: g.js },
  };
}

function convVolterra(r: Rng): Draft {
  const v = r.int(0, 3);
  let eq: string, res: Term[], steps: string[], lam: number, K: string, rhs: string;
  if (v === 0) {
    const k = r.nz(-3, 3), c = r.nz(-4, 4);
    eq = `y(t) ${k > 0 ? "-" : "+"} ${Math.abs(k) === 1 ? "" : Math.abs(k)}\\int_0^t y(\\tau)\\,d\\tau = ${c}`;
    res = [T(c, "exp", k)];
    lam = -k; K = "1"; rhs = `${c}`;
    steps = [
      `The integral is ${m("1 * y")}, with transform ${m("Y/s")}: ${m(`Y ${k > 0 ? "-" : "+"} ${Math.abs(k) === 1 ? "" : Math.abs(k)}\\frac{Y}{s} = \\frac{${c}}{s}`)}.`,
      `Multiply by ${m("s")}: ${m(`(${linTex(k)})Y = ${c}`)}, ${m(`Y = \\frac{${c}}{${linTex(k)}}`)}.`,
    ];
  } else if (v === 1) {
    const w = r.int(1, 4), c = r.nz(-4, 4);
    eq = `y(t) + ${w === 1 ? "" : w * w}\\int_0^t (t - \\tau)\\,y(\\tau)\\,d\\tau = ${c}`;
    res = [T(c, "cos", 0, { w })];
    lam = w * w; K = "x"; rhs = `${c}`;
    steps = [
      `The integral is ${m("t * y")}, with transform ${m("Y/s^{2}")}: ${m(`Y\\left(1 + \\frac{${w * w}}{s^{2}}\\right) = \\frac{${c}}{s}`)}.`,
      m(`Y = \\frac{${ct(c, "s")}}{s^{2} + ${w * w}}`),
    ];
  } else if (v === 2) {
    const c = r.nz(-4, 4);
    eq = `y(t) - \\int_0^t y(\\tau)\\sin(t - \\tau)\\,d\\tau = ${ct(c, "t")}`;
    res = [T(c, "pow", 0, { p: 1 }), T(new Q(c, 6), "pow", 0, { p: 3 })];
    lam = -1; K = "sin(x)"; rhs = `(${c})*t`;
    steps = [
      `The integral is ${m("y * \\sin t")}: ${m(`Y - \\frac{Y}{s^{2} + 1} = \\frac{${c}}{s^{2}}`)}, i.e. ${m(`Y\\frac{s^{2}}{s^{2} + 1} = \\frac{${c}}{s^{2}}`)}.`,
      m(`Y = \\frac{${ct(c, "(s^{2} + 1)")}}{s^{4}} = ${join([fr(new Q(c), "1", "s^{2}"), fr(new Q(c), "1", "s^{4}")])}`),
    ];
  } else {
    const a = r.nz(-2, 2), k = r.nz(-3, 3);
    const g = a + k;
    require_(g !== 0);
    const c = g * r.nz(-2, 2);
    const ea = `e^{${kArg(a, "t - \\tau")}}`;
    eq = `y(t) ${k > 0 ? "-" : "+"} ${Math.abs(k) === 1 ? "" : Math.abs(k)}\\int_0^t ${ea}\\,y(\\tau)\\,d\\tau = ${c}`;
    res = [T(new Q(c * a, g), "exp", 0), T(new Q(c * k, g), "exp", g)];
    lam = -k; K = `exp((${a})*x)`; rhs = `${c}`;
    steps = [
      `The integral is ${m(`e^{${ct(a, "t")}} * y`)}: ${m(`Y ${k > 0 ? "-" : "+"} \\frac{${Math.abs(k) === 1 ? "" : Math.abs(k)}Y}{${linTex(a)}} = ${fr(new Q(c), "1", "s")}`)}.`,
      `${m(`Y\\frac{${linTex(g)}}{${linTex(a)}} = ${fr(new Q(c), "1", "s")}`)}, so ${m(`Y = ${fr(new Q(c), linTex(a), `s(${linTex(g)})`)} = ${sSum(res)}`)}.`,
    ];
  }
  return {
    prompt: `Solve the integral equation ${m(eq)} for ${m("y(t)")}.`,
    answer: { kind: "expression", ref: tSumJs(res), vars: ["t"], label: "y(t)" },
    answerTex: `y(t) = ${tSum(res)}`,
    steps: [...steps, m(`y(t) = ${tSum(res)}`)],
    meta: { lam, K, rhs },
  };
}

// ══ bvp.fourier-series ═════════════════════════════════════════════════════
// Kreyszig's convention: f(x) = a_0 + Σ (a_n cos(nπx/L) + b_n sin(nπx/L)), a_0 the mean value.
const N_POINTS = [1, 2, 3, 4, 5, 6, 7].map((n) => ({ n }));
interface Coef { label: string; tex: string; ref: string; shown: string }
const A0 = (shown: string, ref: string): Coef => ({ label: "a_0", tex: "a_0", ref, shown });
const AN = (shown: string, ref: string): Coef => ({ label: "a_n", tex: "a_n", ref, shown });
const BN = (shown: string, ref: string): Coef => ({ label: "b_n", tex: "b_n", ref, shown });

function fsDraft(prompt: string, coefs: Coef[], steps: string[], meta: Record<string, unknown>): Draft {
  const all = coefs.map((c) => `${c.tex} = ${c.shown}`).join(",\\quad ");
  return {
    prompt,
    answer: { kind: "tuple", fields: coefs.map((c) => ({ label: c.label, tex: c.tex, ref: c.ref, mode: "expr" as const })), vars: ["n"], points: N_POINTS },
    answerTex: all,
    steps: [...steps, m(all)],
    meta,
  };
}
const FULL = (L: string) =>
  L === "\\pi"
    ? `with ${m("f(x) = a_0 + \\sum_{n\\ge1}(a_n\\cos nx + b_n\\sin nx)")} (period ${m("2\\pi")})`
    : `with ${m(`f(x) = a_0 + \\sum_{n\\ge1}\\left(a_n\\cos\\frac{n\\pi x}{${L}} + b_n\\sin\\frac{n\\pi x}{${L}}\\right)`)} (period ${m(`2L = ${2 * Number(L)}`)})`;
const alt = (g: number) => `(${g})*(1-(-1)^n)`;

function fsStep(r: Rng): Draft {
  const c = r.int(-4, 4), d = r.int(-4, 4);
  require_(c !== d);
  const g = c - d;
  return fsDraft(
    `Find the Fourier coefficients of ${m(`f(x) = \\begin{cases} ${d} & -\\pi < x < 0 \\\\ ${c} & 0 < x < \\pi \\end{cases}`)}, ${FULL("\\pi")}.`,
    [A0(new Q(c + d, 2).tex(), `(${c + d})/2`), AN("0", "0"), BN(cf(new Q(g), "(1 - (-1)^{n})", "n\\pi"), `${alt(g)}/(n*pi)`)],
    [
      `${m("a_0 = \\frac{1}{2\\pi}\\int_{-\\pi}^{\\pi} f\\,dx")} is the mean: ${m(new Q(c + d, 2).tex())}.`,
      `${m("a_n = \\frac{1}{\\pi}\\int f\\cos nx\\,dx = 0")}: ${m("\\cos nx")} integrates to 0 over each half.`,
      `With ${m(`f = d = ${d}`)} on the left and ${m(`f = c = ${c}`)} on the right: ${m(`b_n = \\frac{1}{\\pi}\\left[d\\int_{-\\pi}^{0}\\sin nx\\,dx + c\\int_{0}^{\\pi}\\sin nx\\,dx\\right] = \\frac{c - d}{n\\pi}(1 - \\cos n\\pi)`)}, ${m(`c - d = ${g}`)}, and ${m("\\cos n\\pi = (-1)^n")} (so ${m("b_n = 0")} for even ${m("n")}).`,
    ],
    { L: "pi", kind: "full", pieces: [[`${d}`, "-pi", "0"], [`${c}`, "0", "pi"]] }
  );
}

function fsSaw(r: Rng): Draft {
  const k = r.nz(-3, 3), c = r.int(-3, 3);
  return fsDraft(
    `Find the Fourier coefficients of ${m(`f(x) = ${join([ct(k, "x"), `${c}`])}`)} on ${m("-\\pi < x < \\pi")}, ${FULL("\\pi")}.`,
    [A0(`${c}`, `${c}`), AN("0", "0"), BN(cf(new Q(2 * k), "(-1)^{n+1}", "n"), `(${2 * k})*(-1)^(n+1)/n`)],
    [
      `${m("a_0")} = mean value = ${m(`${c}`)} (the ${m("x")} part averages to 0).`,
      `${m(ct(k, "x"))} is odd, so its cosine coefficients vanish: ${m("a_n = 0")}.`,
      `By parts: ${m(`\\frac{1}{\\pi}\\int_{-\\pi}^{\\pi} x\\sin nx\\,dx = -\\frac{2\\cos n\\pi}{n} = \\frac{2(-1)^{n+1}}{n}`)}; times ${m(`${k}`)}.`,
    ],
    { L: "pi", kind: "full", pieces: [[`(${k})*x + (${c})`, "-pi", "pi"]] }
  );
}

function fsParabola(r: Rng): Draft {
  const k = r.nz(-3, 3), c = r.int(-3, 3);
  const a0 = join([qterm(new Q(k, 3), "\\pi^{2}"), `${c}`]);
  return fsDraft(
    `Find the Fourier coefficients of ${m(`f(x) = ${join([ct(k, "x^{2}"), `${c}`])}`)} on ${m("-\\pi < x < \\pi")}, ${FULL("\\pi")}.`,
    [A0(a0, `(${k})*pi^2/3 + (${c})`), AN(cf(new Q(4 * k), "(-1)^{n}", "n^{2}"), `(${4 * k})*(-1)^n/n^2`), BN("0", "0")],
    [
      `Even function: ${m("b_n = 0")}. ${m("a_0 = \\frac{1}{2\\pi}\\int_{-\\pi}^{\\pi} f\\,dx")}: ${m(`\\frac{1}{2\\pi}\\int_{-\\pi}^{\\pi} x^{2}dx = \\frac{\\pi^{2}}{3}`)}.`,
      `By parts twice: ${m("\\frac{1}{\\pi}\\int_{-\\pi}^{\\pi} x^{2}\\cos nx\\,dx = \\frac{4\\cos n\\pi}{n^{2}} = \\frac{4(-1)^{n}}{n^{2}}")}; the constant contributes nothing to ${m("a_n")}.`,
    ],
    { L: "pi", kind: "full", pieces: [[`(${k})*x^2 + (${c})`, "-pi", "pi"]] }
  );
}

function fsAbs(r: Rng): Draft {
  const k = r.nz(-3, 3), c = r.int(-3, 3);
  const a0 = join([qterm(new Q(k, 2), "\\pi"), `${c}`]);
  return fsDraft(
    `Find the Fourier coefficients of ${m(`f(x) = ${join([ct(k, "|x|"), `${c}`])}`)} on ${m("-\\pi < x < \\pi")}, ${FULL("\\pi")}.`,
    [A0(a0, `(${k})*pi/2 + (${c})`), AN(cf(new Q(2 * k), "((-1)^{n} - 1)", "n^{2}\\pi"), `(${2 * k})*((-1)^n - 1)/(n^2*pi)`), BN("0", "0")],
    [
      `Even function: ${m("b_n = 0")}, and the integrals are twice those over ${m("[0, \\pi]")}.`,
      `${m("a_0")}: the mean of ${m("|x|")} on ${m("[0, \\pi]")} is ${m("\\pi/2")}.`,
      `${m("a_n = \\frac{2}{\\pi}\\int_0^{\\pi} x\\cos nx\\,dx = \\frac{2(\\cos n\\pi - 1)}{n^{2}\\pi}")}: zero for even ${m("n")}, ${m("-\\frac{4}{n^{2}\\pi}")} for odd; times ${m(`${k}`)}.`,
    ],
    { L: "pi", kind: "full", pieces: [[`(${-k})*x + (${c})`, "-pi", "0"], [`(${k})*x + (${c})`, "0", "pi"]] } // |x| = -x, x
  );
}

function fsPeriod2L(r: Rng): Draft {
  const L = r.int(1, 4);
  if (r.chance(0.5)) {
    const k = r.nz(-3, 3);
    return fsDraft(
      `Find the Fourier coefficients of ${m(`f(x) = ${ct(k, "x")}`)} on ${m(`-${L} < x < ${L}`)}, ${FULL(`${L}`)}.`,
      [A0("0", "0"), AN("0", "0"), BN(cf(new Q(2 * k * L), "(-1)^{n+1}", "n\\pi"), `(${2 * k * L})*(-1)^(n+1)/(n*pi)`)],
      [
        `Odd function: ${m("a_0 = a_n = 0")}.`,
        `${m(`b_n = \\frac{1}{L}\\int_{-L}^{L} f\\sin\\frac{n\\pi x}{L}dx`)}; by parts ${m("\\frac{1}{L}\\int_{-L}^{L} x\\sin\\frac{n\\pi x}{L}dx = \\frac{2L(-1)^{n+1}}{n\\pi}")}.`,
        `With ${m(`L = ${L}`)} and the factor ${m(`${k}`)}: ${m(`b_n = ${cf(new Q(2 * k * L), "(-1)^{n+1}", "n\\pi")}`)}.`,
      ],
      { L: `${L}`, kind: "full", pieces: [[`(${k})*x`, `-${L}`, `${L}`]] }
    );
  }
  const c = r.nz(-4, 4);
  return fsDraft(
    `Find the Fourier coefficients of ${m(`f(x) = \\begin{cases} 0 & -${L} < x < 0 \\\\ ${c} & 0 < x < ${L} \\end{cases}`)}, ${FULL(`${L}`)}.`,
    [A0(new Q(c, 2).tex(), `(${c})/2`), AN("0", "0"), BN(cf(new Q(c), "(1 - (-1)^{n})", "n\\pi"), `${alt(c)}/(n*pi)`)],
    [
      `${m("a_0")} = mean = ${m(new Q(c, 2).tex())}.`,
      `${m(`a_n = \\frac{1}{${L}}\\int_0^{${L}} ${ct(c, `\\cos\\frac{n\\pi x}{${L}}`)}dx = 0`)}.`,
      `${m(`b_n = \\frac{1}{${L}}\\int_0^{${L}} ${ct(c, `\\sin\\frac{n\\pi x}{${L}}`)}dx = \\frac{${c}}{n\\pi}(1 - \\cos n\\pi)`)} — the ${m("L")} cancels.`,
    ],
    { L: `${L}`, kind: "full", pieces: [["0", `-${L}`, "0"], [`${c}`, "0", `${L}`]] }
  );
}

function fsHalfRange(r: Rng): Draft {
  const isPi = r.chance(0.35);
  const L = isPi ? 0 : r.int(1, 3);
  const Lt = isPi ? "\\pi" : `${L}`;
  const Lj = isPi ? "pi" : `${L}`;
  const arg = isPi ? "nx" : `\\frac{n\\pi x}{${L}}`;
  const v = r.int(0, 2);
  const range = `on ${m(`0 < x < ${Lt}`)}`;
  if (v === 0) {
    const c = r.nz(-4, 4);
    return fsDraft(
      `Find the coefficients ${m("b_n")} of the half-range sine series ${m(`f(x) = \\sum b_n\\sin ${arg}`)} of ${m(`f(x) = ${c}`)} ${range}.`,
      [BN(cf(new Q(2 * c), "(1 - (-1)^{n})", "n\\pi"), `${alt(2 * c)}/(n*pi)`)],
      [
        `Sine series = Fourier series of the odd extension: ${m(`b_n = \\frac{2}{L}\\int_0^{L} f\\sin\\frac{n\\pi x}{L}dx`)}.`,
        `${m(`\\frac{2}{L}\\int_0^{L} ${ct(c, "\\sin\\frac{n\\pi x}{L}")}dx = \\frac{${2 * c}}{n\\pi}(1 - \\cos n\\pi)`)} (any ${m("L")}).`,
      ],
      { L: Lj, kind: "sine", pieces: [[`${c}`, "0", Lj]] }
    );
  }
  const k = r.nz(-3, 3);
  if (v === 1) {
    const q = isPi ? new Q(2 * k) : new Q(2 * k * L);
    const bot = isPi ? "n" : "n\\pi";
    return fsDraft(
      `Find the coefficients ${m("b_n")} of the half-range sine series ${m(`f(x) = \\sum b_n\\sin ${arg}`)} of ${m(`f(x) = ${ct(k, "x")}`)} ${range}.`,
      [BN(cf(q, "(-1)^{n+1}", bot), `(${2 * k})*(${Lj})*(-1)^(n+1)/(n*pi)`)],
      [
        `Odd extension: ${m(`b_n = \\frac{2}{L}\\int_0^{L} ${ct(k, "x")}\\sin\\frac{n\\pi x}{L}dx`)}.`,
        `By parts: ${m("\\frac{2}{L}\\int_0^{L} x\\sin\\frac{n\\pi x}{L}dx = \\frac{2L(-1)^{n+1}}{n\\pi}")}; ${m(`L = ${Lt}`)}.`,
      ],
      { L: Lj, kind: "sine", pieces: [[`(${k})*x`, "0", Lj]] }
    );
  }
  const a0q = isPi ? new Q(k, 2) : new Q(k * L, 2);
  const a0 = isPi ? qterm(a0q, "\\pi") : a0q.tex();
  const anq = isPi ? new Q(2 * k) : new Q(2 * k * L);
  const anBot = isPi ? "n^{2}\\pi" : "n^{2}\\pi^{2}";
  return fsDraft(
    `Find ${m("a_0")} and ${m("a_n")} of the half-range cosine series ${m(`f(x) = a_0 + \\sum a_n\\cos ${arg}`)} of ${m(`f(x) = ${ct(k, "x")}`)} ${range}.`,
    [A0(a0, `(${k})*(${Lj})/2`), AN(cf(anq, "((-1)^{n} - 1)", anBot), `(${2 * k})*(${Lj})*((-1)^n - 1)/(n^2*pi^2)`)],
    [
      `Cosine series = Fourier series of the even extension: ${m("a_0 = \\frac{1}{L}\\int_0^{L} f\\,dx")}, ${m("a_n = \\frac{2}{L}\\int_0^{L} f\\cos\\frac{n\\pi x}{L}dx")}.`,
      `${m(`a_0 = \\frac{1}{L}\\int_0^{L} ${ct(k, "x")}\\,dx = ${qterm(new Q(k, 2), "L")}`)}.`,
      `By parts: ${m("\\frac{2}{L}\\int_0^{L} x\\cos\\frac{n\\pi x}{L}dx = \\frac{2L((-1)^{n} - 1)}{n^{2}\\pi^{2}}")}; ${m(`L = ${Lt}`)}.`,
    ],
    { L: Lj, kind: "cosine", pieces: [[`(${k})*x`, "0", Lj]] }
  );
}

// ══ pde.separation ═════════════════════════════════════════════════════════
interface Dom { L: number; Lt: string; Lj: string }
function dom(r: Rng, allowPi = true): Dom {
  const c = allowPi ? r.pick(["pi", "pi", 1, 2] as const) : r.pick([1, 2] as const);
  return c === "pi" ? { L: Math.PI, Lt: "\\pi", Lj: "pi" } : { L: c, Lt: `${c}`, Lj: `${c}` };
}
/** sin(mπx/L) / cos(...) LaTeX and mathjs */
function mode(d: Dom, mm: number, fn: "sin" | "cos"): [string, string] {
  const tex =
    d.Lt === "\\pi" ? `\\${fn} ${mm === 1 ? "" : mm}x`
    : d.Lt === "1" ? `\\${fn} ${mm === 1 ? "" : mm}\\pi x`
    : `\\${fn}\\frac{${mm === 1 ? "" : mm}\\pi x}{${d.Lt}}`;
  return [tex, `${fn}(${mm}*pi*x/(${d.Lj}))`];
}
/** decay rate c²(mπ/L)² as LaTeX coefficient of t, mathjs, number */
function rate(d: Dom, c2: number, mm: number): [string, string, number] {
  const k = c2 * mm * mm;
  const tex = d.Lt === "\\pi" ? `${k}` : qterm(new Q(k, d.L * d.L), "\\pi^{2}");
  return [tex, `(${c2})*(${mm}*pi/(${d.Lj}))^2`, (c2 * (mm * Math.PI) ** 2) / d.L ** 2];
}
/** nπx/L and nπ/L for the domain, simplified for L = π and L = 1 */
const npx = (d: Dom) => (d.Lt === "\\pi" ? "nx" : d.Lt === "1" ? "n\\pi x" : `\\frac{n\\pi x}{${d.Lt}}`);
const npL = (d: Dom) => (d.Lt === "\\pi" ? "n" : d.Lt === "1" ? "n\\pi" : `\\frac{n\\pi}{${d.Lt}}`);
const xPts = [0.13, 0.29, 0.41, 0.58, 0.77, 0.88, 0.36];
const heatPts = (d: Dom, maxRate: number) => [0.05, 0.15, 0.3, 0.5, 0.8, 1.1, 1.5].map((tau, i) => ({ x: xPts[i] * d.L, t: tau / maxRate }));
const wavePts = (d: Dom) => [0.2, 0.45, 0.7, 1.0, 1.3, 1.6, 1.9].map((t, i) => ({ x: xPts[i] * d.L, t }));
const uExpr = (ref: string, points: Record<string, number>[]) => ({ kind: "expression" as const, ref, vars: ["x", "t"], label: "u(x,t)", points });
const heatEq = (c2: number) => `u_t = ${c2 === 1 ? "" : c2}u_{xx}`;
const expT = (rt: string) => `e^{-${rt === "1" ? "" : rt}t}`;

function twoModes(r: Rng): [number, number] {
  const a = r.int(1, 4), b = r.int(1, 4);
  require_(a < b);
  return [a, b];
}

function pdeHeat(r: Rng): Draft {
  const d = dom(r);
  const c2 = d.Lt === "\\pi" ? r.int(1, 3) : r.pick([1, 2]);
  const [m1, m2] = twoModes(r);
  const A = r.nz(-5, 5), B = r.nz(-5, 5);
  const [s1, s1j] = mode(d, m1, "sin"), [s2, s2j] = mode(d, m2, "sin");
  const [r1, r1j] = rate(d, c2, m1), [r2, r2j, r2n] = rate(d, c2, m2);
  const u = join([ct(A, `${s1}\\,${expT(r1)}`), ct(B, `${s2}\\,${expT(r2)}`)]);
  const uj = `(${A})*${s1j}*exp(-${r1j}*t) + (${B})*${s2j}*exp(-${r2j}*t)`;
  return {
    prompt: `Solve ${m(heatEq(c2))} on ${m(`0 < x < ${d.Lt}`)} with ${m(`u(0,t) = u(${d.Lt},t) = 0`)} and ${m(`u(x,0) = ${join([ct(A, s1), ct(B, s2)])}`)}.`,
    answer: uExpr(uj, heatPts(d, r2n)),
    answerTex: `u(x,t) = ${u}`,
    steps: [
      `Separate ${m("u = F(x)G(t)")}: ${m(`F'' + p^{2}F = 0`)} with ${m(`F(0) = F(${d.Lt}) = 0`)} gives ${m(`F_n = \\sin ${npx(d)}`)}; ${m(`G_n = e^{-\\lambda_n^{2}t}`)}, ${m(`\\lambda_n^{2} = ${c2 === 1 ? "" : c2}\\left(${npL(d)}\\right)^{2}`)}.`,
      `${m("u = \\sum B_n\\sin\\frac{n\\pi x}{L}e^{-\\lambda_n^{2}t}")}; the initial condition is already a sine sum, so ${m(`B_{${m1}} = ${A}`)}, ${m(`B_{${m2}} = ${B}`)}, all others 0.`,
      `Decay rates ${m(`\\lambda_{${m1}}^{2} = ${r1}`)}, ${m(`\\lambda_{${m2}}^{2} = ${r2}`)}.`,
      m(`u(x,t) = ${u}`),
    ],
    meta: { pde: "heat", c2, L: d.Lj, bc: "DD", u0: `(${A})*${s1j} + (${B})*${s2j}` },
  };
}

function pdeNeumann(r: Rng): Draft {
  const d = dom(r);
  const c2 = d.Lt === "\\pi" ? r.int(1, 3) : r.pick([1, 2]);
  const a0 = r.int(-5, 5), mm = r.int(1, 4), B = r.nz(-5, 5);
  const [cs, csj] = mode(d, mm, "cos");
  const [rt, rtj, rtn] = rate(d, c2, mm);
  const u = join([`${a0}`, ct(B, `${cs}\\,${expT(rt)}`)]);
  return {
    prompt: `Solve ${m(heatEq(c2))} on ${m(`0 < x < ${d.Lt}`)} with insulated ends ${m(`u_x(0,t) = u_x(${d.Lt},t) = 0`)} and ${m(`u(x,0) = ${join([`${a0}`, ct(B, cs)])}`)}.`,
    answer: uExpr(`(${a0}) + (${B})*${csj}*exp(-${rtj}*t)`, heatPts(d, rtn)),
    answerTex: `u(x,t) = ${u}`,
    steps: [
      `Separate: ${m("F'' + p^{2}F = 0")}, ${m(`F'(0) = F'(${d.Lt}) = 0`)} gives ${m(`F_n = \\cos ${npx(d)}`)}, ${m("n = 0, 1, 2, \\dots")} — including the constant ${m("F_0 = 1")}.`,
      `${m("u = A_0 + \\sum A_n\\cos\\frac{n\\pi x}{L}e^{-\\lambda_n^{2}t}")}; match the initial condition: ${m(`A_0 = ${a0}`)}, ${m(`A_{${mm}} = ${B}`)}.`,
      `The constant mode never decays (insulated: heat cannot leave); ${m(`\\lambda_{${mm}}^{2} = ${rt}`)}.`,
      m(`u(x,t) = ${u}`),
    ],
    meta: { pde: "heat", c2, L: d.Lj, bc: "NN", u0: `(${a0}) + (${B})*${csj}` },
  };
}

function pdeSteady(r: Rng): Draft {
  const d = dom(r, false);
  const c2 = r.pick([1, 2]);
  const T1 = r.int(-5, 10);
  const slope = r.nz(-5, 5);
  const T2 = T1 + slope * d.L;
  const mm = r.int(1, 3), A = r.nz(-5, 5);
  const [sn, snj] = mode(d, mm, "sin");
  const [rt, rtj, rtn] = rate(d, c2, mm);
  const steady = join([`${T1}`, ct(slope, "x")]);
  const u = join([`${T1}`, ct(slope, "x"), ct(A, `${sn}\\,${expT(rt)}`)]);
  return {
    prompt: `Solve ${m(heatEq(c2))} on ${m(`0 < x < ${d.Lt}`)} with ${m(`u(0,t) = ${T1}`)}, ${m(`u(${d.Lt},t) = ${T2}`)} and ${m(`u(x,0) = ${join([`${T1}`, ct(slope, "x"), ct(A, sn)])}`)}.`,
    answer: uExpr(`(${T1}) + (${slope})*x + (${A})*${snj}*exp(-${rtj}*t)`, heatPts(d, rtn)),
    answerTex: `u(x,t) = ${u}`,
    steps: [
      `Nonzero end temperatures: split ${m("u = U(x) + v(x,t)")} with the steady state ${m("U'' = 0")}, ${m(`U(0) = ${T1}`)}, ${m(`U(${d.Lt}) = ${T2}`)}: ${m(`U = ${steady}`)}.`,
      `${m("v")} solves the same equation with zero end values and ${m(`v(x,0) = u(x,0) - U = ${ct(A, sn)}`)}.`,
      `One mode: ${m(`v = ${ct(A, `${sn}\\,${expT(rt)}`)}`)}.`,
      m(`u(x,t) = ${u}`),
    ],
    meta: { pde: "heat", c2, L: d.Lj, bc: "fixed", T1, T2, u0: `(${T1}) + (${slope})*x + (${A})*${snj}` },
  };
}

function pdeWave(r: Rng): Draft {
  const d: Dom = { L: Math.PI, Lt: "\\pi", Lj: "pi" };
  const c = r.int(1, 3);
  const v = r.int(0, 2);
  const eq = `u_{tt} = ${c === 1 ? "" : c * c}u_{xx}`;
  const ct_ = (k: number, fn: string) => `\\${fn} ${k === 1 ? "" : k}t`;
  let u: string, uj: string, f0: string, f0j: string, g0: string, g0j: string, coefStep: string;
  if (v === 0) {
    const [m1, m2] = twoModes(r);
    const A = r.nz(-4, 4), B = r.nz(-4, 4);
    const [s1, s1j] = mode(d, m1, "sin"), [s2, s2j] = mode(d, m2, "sin");
    u = join([ct(A, `${s1}${ct_(c * m1, "cos")}`), ct(B, `${s2}${ct_(c * m2, "cos")}`)]);
    uj = `(${A})*${s1j}*cos(${c * m1}*t) + (${B})*${s2j}*cos(${c * m2}*t)`;
    f0 = join([ct(A, s1), ct(B, s2)]); f0j = `(${A})*${s1j} + (${B})*${s2j}`;
    g0 = "0"; g0j = "0";
    coefStep = `Zero initial velocity: ${m("B_n^{*} = 0")}. Read off ${m(`B_{${m1}} = ${A}`)}, ${m(`B_{${m2}} = ${B}`)} from ${m("u(x,0)")}.`;
  } else {
    const m1 = r.int(1, 4), G = r.nz(-4, 4) * c * m1;
    const [s1, s1j] = mode(d, m1, "sin");
    const amp = new Q(G, c * m1);
    const A = v === 2 ? r.nz(-4, 4) : 0;
    const m2 = v === 2 ? r.nz(1, 4, [m1]) : 0;
    const [s2, s2j] = v === 2 ? mode(d, m2, "sin") : ["", ""];
    u = join([qterm(amp, `${s1}${ct_(c * m1, "sin")}`), A ? ct(A, `${s2}${ct_(c * m2, "cos")}`) : "0"]);
    uj = `${amp.js()}*${s1j}*sin(${c * m1}*t)` + (A ? ` + (${A})*${s2j}*cos(${c * m2}*t)` : "");
    f0 = A ? ct(A, s2) : "0"; f0j = A ? `(${A})*${s2j}` : "0";
    g0 = ct(G, s1); g0j = `(${G})*${s1j}`;
    coefStep = `${m("u_t(x,0) = \\sum B_n^{*}\\lambda_n\\sin nx")}: ${m(`B_{${m1}}^{*}\\cdot${c * m1} = ${G}`)}, so ${m(`B_{${m1}}^{*} = ${amp.tex()}`)}${A ? `; from ${m("u(x,0)")}: ${m(`B_{${m2}} = ${A}`)}` : ""}.`;
  }
  return {
    prompt: `Solve ${m(eq)} on ${m("0 < x < \\pi")} with ${m("u(0,t) = u(\\pi,t) = 0")}, ${m(`u(x,0) = ${f0}`)}, ${m(`u_t(x,0) = ${g0}`)}.`,
    answer: uExpr(uj, wavePts(d)),
    answerTex: `u(x,t) = ${u}`,
    steps: [
      `Separate: ${m("F_n = \\sin nx")}, ${m(`G_n = B_n\\cos\\lambda_n t + B_n^{*}\\sin\\lambda_n t`)} with ${m(`\\lambda_n = cn = ${c === 1 ? "" : c}n`)}.`,
      coefStep,
      m(`u(x,t) = ${u}`),
    ],
    meta: { pde: "wave", c2: c * c, L: "pi", bc: "DD", u0: f0j, ut0: g0j },
  };
}

function pdeRates(r: Rng): Draft {
  const d = dom(r);
  const v = r.int(0, 2);
  const nTex = (start: number) => `n = ${start}, ${start + 1}, ${start + 2}, \\dots`;
  if (v === 2) {
    const c = r.int(1, 3);
    const ref = `(${c})*n*pi/(${d.Lj})`;
    const tex = d.Lt === "\\pi" ? ct(c, "n") : d.Lt === "1" ? `${ct(c, "n")}\\pi` : `\\frac{${ct(c, "n")}\\pi}{${d.Lt}}`;
    return {
      prompt: `Separating ${m("u = F(x)G(t)")} in ${m(`u_{tt} = ${c === 1 ? "" : c * c}u_{xx}`)}, ${m(`0 < x < ${d.Lt}`)}, ${m(`u(0,t) = u(${d.Lt},t) = 0`)} gives ${m("G_n = B_n\\cos\\lambda_n t + B_n^{*}\\sin\\lambda_n t")}. Find ${m("\\lambda_n")}.`,
      answer: { kind: "indexed", ref, start: 1, label: "λ_n" },
      answerTex: `\\lambda_n = ${tex},\\quad ${nTex(1)}`,
      steps: [
        `${m("F'' + p^{2}F = 0")}, ${m(`F(0) = F(${d.Lt}) = 0`)}: ${m(`p = ${npL(d)}`)}, ${m(`F_n = \\sin ${npx(d)}`)}.`,
        `${m("\\ddot G + c^{2}p^{2}G = 0")} with ${m(`c = ${c}`)}: ${m(`\\lambda_n = cp = ${tex}`)}.`,
      ],
      meta: { pde: "wave", c2: c * c, L: d.Lj, bc: "DD", start: 1, lam: ref },
    };
  }
  const c2 = r.int(1, 4);
  const bc = v === 0 ? "DD" : "NN";
  const start = bc === "DD" ? 1 : 0;
  const ref = `(${c2})*(n*pi/(${d.Lj}))^2`;
  const tex = d.Lt === "\\pi" ? ct(c2, "n^{2}") : qterm(new Q(c2, d.L * d.L), "n^{2}\\pi^{2}");
  const bcTex = bc === "DD" ? `u(0,t) = u(${d.Lt},t) = 0` : `u_x(0,t) = u_x(${d.Lt},t) = 0`;
  return {
    prompt: `Separating ${m("u = F(x)G(t)")} in ${m(heatEq(c2))}, ${m(`0 < x < ${d.Lt}`)}, ${m(bcTex)} gives product solutions ${m("F_n(x)e^{-\\kappa_n t}")}. Find ${m("\\kappa_n")}.`,
    answer: { kind: "indexed", ref, start, label: "κ_n" },
    answerTex: `\\kappa_n = ${tex},\\quad ${nTex(start)}`,
    steps: [
      `${m("F'' + p^{2}F = 0")}, ${m(bc === "DD" ? `F(0) = F(${d.Lt}) = 0` : `F'(0) = F'(${d.Lt}) = 0`)}: ${m(`p = ${npL(d)}`)}, ${m(`F_n = \\${bc === "DD" ? "sin" : "cos"} ${npx(d)}`)}${bc === "NN" ? ` (with ${m("n = 0")}: a constant)` : ""}.`,
      `${m("\\dot G = -c^{2}p^{2}G")}: ${m(`\\kappa_n = c^{2}p^{2} = ${tex}`)}.`,
    ],
    meta: { pde: "heat", c2, L: d.Lj, bc, start, lam: ref },
  };
}

// ══ series.special-functions ═══════════════════════════════════════════════
const EQ_OPTIONS = ["Legendre equation", "Bessel equation", "Euler–Cauchy equation", "Hermite equation"];
const SUB = "₀₁₂₃₄₅₆₇₈₉";
const sub = (k: number) => `${k}`.split("").map((ch) => SUB[Number(ch)]).join("");

function specIdentify(r: Rng): Draft {
  const type = r.int(0, 3);
  let eq: string, P: string, Qs: string, R: string, why: string;
  if (type === 0) {
    const n = r.int(1, 5), f = r.pick([1, 1, -1, 2]);
    const k = n * (n + 1);
    const lead = f === 1 ? "(1 - x^{2})" : f === -1 ? "(x^{2} - 1)" : `${f}(1 - x^{2})`;
    eq = `${lead}y'' ${f > 0 ? "-" : "+"} ${Math.abs(2 * f)}xy' ${f > 0 ? "+" : "-"} ${Math.abs(f * k)}y = 0`;
    P = `(${f})*(1-x^2)`; Qs = `(${-2 * f})*x`; R = `${f * k}`;
    why = `Divide by ${m(`${f}`)}: ${m(`(1 - x^{2})y'' - 2xy' + n(n+1)y = 0`)} with ${m(`n(n+1) = ${k}`)}, ${m(`n = ${n}`)}: Legendre's equation.`;
  } else if (type === 1) {
    const nu2 = r.pick([new Q(1, 4), new Q(9, 4), new Q(1), new Q(4), new Q(9), new Q(1, 9), new Q(0)]);
    if (r.chance(0.5)) {
      eq = `x^{2}y'' + xy' + (x^{2}${nu2.isZero() ? "" : ` - ${nu2.tex()}`})y = 0`;
      P = "x^2"; Qs = "x"; R = `x^2 - ${nu2.js()}`;
      why = `${m("x^{2}y'' + xy' + (x^{2} - \\nu^{2})y = 0")} with ${m(`\\nu^{2} = ${nu2.tex()}`)}: Bessel's equation.`;
    } else {
      eq = nu2.isZero() ? `xy'' + y' + xy = 0` : `xy'' + y' + \\left(x - \\frac{${nu2.n}}{${nu2.d === 1 ? "" : nu2.d}x}\\right)y = 0`;
      P = "x"; Qs = "1"; R = `x - ${nu2.js()}/x`;
      why = `Multiply by ${m("x")}: ${m(`x^{2}y'' + xy' + ${nu2.isZero() ? "x^{2}" : `(x^{2} - ${nu2.tex()})`}y = 0`)}, Bessel's equation with ${m(`\\nu^{2} = ${nu2.tex()}`)}.`;
    }
  } else if (type === 2) {
    const a = r.pick([1, 1, -1, 2, 3, -2]), b = r.nz(-6, 6);
    eq = `x^{2}y'' ${a < 0 ? "-" : "+"} ${Math.abs(a) === 1 ? "" : Math.abs(a)}xy' ${b < 0 ? "-" : "+"} ${Math.abs(b) === 1 ? "" : Math.abs(b)}y = 0`;
    P = "x^2"; Qs = `(${a})*x`; R = `${b}`;
    why = `Coefficients ${m("x^{2}, x, 1")} times constants: Euler–Cauchy (try ${m("y = x^{m}")}).${a === 1 ? ` It is not Bessel: there is no ${m("x^{2}y")} term.` : ""}`;
  } else {
    const n = r.int(1, 5), f = r.pick([1, 1, -1, 2]);
    eq = `${f === 1 ? "" : f === -1 ? "-" : f}y'' ${f > 0 ? "-" : "+"} ${Math.abs(2 * f)}xy' ${f > 0 ? "+" : "-"} ${Math.abs(2 * n * f)}y = 0`;
    P = `${f}`; Qs = `(${-2 * f})*x`; R = `${2 * n * f}`;
    why = `Divide by ${m(`${f}`)}: ${m(`y'' - 2xy' + 2ny = 0`)} with ${m(`n = ${n}`)}: Hermite's equation (constant leading coefficient, so it is not Legendre).`;
  }
  return {
    prompt: `Which classical equation is ${m(eq)}?`,
    answer: { kind: "choice", options: EQ_OPTIONS, correct: EQ_OPTIONS[type] },
    answerTex: `\\text{${EQ_OPTIONS[type].replace("–", "--")}}`,
    steps: [
      `Compare with the standard forms: Legendre ${m("(1 - x^{2})y'' - 2xy' + n(n+1)y = 0")}; Bessel ${m("x^{2}y'' + xy' + (x^{2} - \\nu^{2})y = 0")}; Euler–Cauchy ${m("x^{2}y'' + axy' + by = 0")}; Hermite ${m("y'' - 2xy' + 2ny = 0")}.`,
      why,
    ],
    meta: { variant: "identify", P, Q: Qs, R, type },
  };
}

function specLegendreN(r: Rng): Draft {
  const n = r.int(1, 6), f = r.pick([1, 1, -1, 2, 3]);
  const k = n * (n + 1);
  const lead = f === 1 ? "(1 - x^{2})" : f === -1 ? "(x^{2} - 1)" : `${f}(1 - x^{2})`;
  const eq = `${lead}y'' ${f > 0 ? "-" : "+"} ${Math.abs(2 * f)}xy' ${f > 0 ? "+" : "-"} ${Math.abs(f * k)}y = 0`;
  return {
    prompt: `${m(eq)} is Legendre's equation. For which ${m("n \\ge 0")} is it? (Its polynomial solution is ${m("P_n")}.)`,
    answer: { kind: "expression", ref: `${n}`, vars: [], label: "n" },
    answerTex: `n = ${n}`,
    steps: [
      `Divide by ${m(`${f}`)} to reach ${m("(1 - x^{2})y'' - 2xy' + n(n+1)y = 0")}: ${m(`n(n+1) = ${k}`)}.`,
      `${m(`n^{2} + n - ${k} = (n - ${n})(n + ${n + 1}) = 0`)}; take the root ${m("n \\ge 0")}: ${m(`n = ${n}`)}.`,
    ],
    meta: { variant: "legendre-n", P: `(${f})*(1-x^2)`, Q: `(${-2 * f})*x`, R: `${f * k}` },
  };
}

function specBesselOrder(r: Rng): Draft {
  const nu = r.pick([new Q(1, 2), new Q(3, 2), new Q(5, 2), new Q(1, 3), new Q(2, 3), new Q(1), new Q(2), new Q(3), new Q(4)]);
  const nu2 = nu.mul(nu);
  const k = r.pick([1, 1, 2, 3]);
  const k2 = k * k;
  const eq = `x^{2}y'' + xy' + (${k2 === 1 ? "" : k2}x^{2} - ${nu2.tex()})y = 0`;
  return {
    prompt: `${m(eq)} has solutions ${m(`J_{\\nu}(${k === 1 ? "" : k}x)`)}. Find the order ${m("\\nu \\ge 0")}.`,
    answer: { kind: "expression", ref: nu.js(), vars: [], label: "ν" },
    answerTex: `\\nu = ${nu.tex()}`,
    steps: [
      `Bessel form ${m("x^{2}y'' + xy' + (k^{2}x^{2} - \\nu^{2})y = 0")}, solved by ${m("J_\\nu(kx)")}${k === 1 ? "" : ` (here ${m(`k = ${k}`)})`}.`,
      `${m(`\\nu^{2} = ${nu2.tex()}`)}, so ${m(`\\nu = ${nu.tex()}`)}.`,
    ],
    meta: { variant: "bessel-order", P: "x^2", Q: "x", R: `${k2}*x^2 - ${nu2.js()}`, k },
  };
}

function specBesselScaled(r: Rng): Draft {
  const nu = r.int(0, 3), k = r.int(2, 4);
  const opts: [string, number, string][] = [
    [`J${sub(nu)}(${k}x)`, nu, `${k}`],
    [`J${sub(nu)}(${k * k}x)`, nu, `${k * k}`],
    [`J${sub(nu)}(x/${k})`, nu, `1/${k}`],
    [`J${sub(nu + 1)}(${k}x)`, nu + 1, `${k}`],
  ];
  const order = [0, 1, 2, 3].sort(() => r.next() - 0.5);
  const options = order.map((i) => opts[i][0]);
  const eq = `x^{2}y'' + xy' + ${nu ? `(${k * k}x^{2} - ${nu * nu})` : `${k * k}x^{2}`}y = 0`;
  return {
    prompt: `Which function solves ${m(eq)}?`,
    answer: { kind: "choice", options, correct: opts[0][0] },
    answerTex: `J_{${nu}}(${k}x)`,
    steps: [
      `Substitute ${m(`z = ${k}x`)}: ${m("x\\frac{d}{dx} = z\\frac{d}{dz}")}, and ${m(`${k * k}x^{2} = z^{2}`)}, so the equation becomes Bessel's ${m(`z^{2}y'' + zy' + ${nu ? `(z^{2} - ${nu * nu})` : "z^{2}"}y = 0`)}.`,
      `${m(`\\nu^{2} = ${nu * nu}`)} gives ${m(`\\nu = ${nu}`)}, and ${m(`y = J_{${nu}}(z) = J_{${nu}}(${k}x)`)} — the scale is ${m(`k = \\sqrt{${k * k}} = ${k}`)}.`,
    ],
    meta: { variant: "bessel-scaled", nu, k, options: order.map((i) => [opts[i][1], opts[i][2]]), correctIndex: order.indexOf(0) },
  };
}

const IND_OPTIONS = ["Yes — J_ν and J_−ν are independent", "No — use Y_ν for the second solution"];
function specBesselIndependent(r: Rng): Draft {
  const nu = r.pick([new Q(1, 2), new Q(3, 2), new Q(1, 3), new Q(2, 3), new Q(5, 2), new Q(1, 4), new Q(1), new Q(2), new Q(3), new Q(4)]);
  const integer = nu.isInt();
  const nu2 = nu.mul(nu);
  return {
    prompt: `For Bessel's equation ${m(`x^{2}y'' + xy' + (x^{2} - ${nu2.tex()})y = 0`)}, is ${m(`y = c_1J_{${nu.tex()}}(x) + c_2J_{-${nu.tex()}}(x)`)} a general solution?`,
    answer: { kind: "choice", options: IND_OPTIONS, correct: IND_OPTIONS[integer ? 1 : 0] },
    answerTex: integer ? `\\text{No: } J_{-${nu.tex()}} = (-1)^{${nu.tex()}}J_{${nu.tex()}},\\ y = c_1J_{${nu.tex()}} + c_2Y_{${nu.tex()}}` : `\\text{Yes: } \\nu = ${nu.tex()} \\notin \\mathbb{Z}`,
    steps: [
      `${m(`\\nu = ${nu.tex()}`)} (the equation fixes ${m(`\\nu^{2} = ${nu2.tex()}`)}).`,
      integer
        ? `Integer order: ${m("J_{-n}(x) = (-1)^{n}J_n(x)")}, the two are dependent; the second solution is ${m("Y_n")} (Bessel function of the second kind).`
        : `Non-integer order: ${m("J_\\nu")} starts like ${m("x^{\\nu}")} and ${m("J_{-\\nu}")} like ${m("x^{-\\nu}")} — independent, so ${m("c_1J_\\nu + c_2J_{-\\nu}")} is general.`,
    ],
    meta: { variant: "bessel-independent", nu: nu.value(), integer },
  };
}

export const LAPLACE_FOURIER_TEMPLATES: Record<string, (r: Rng) => Draft> = {
  "lt-linear": ltLinear,
  "lt-trig": ltTrig,
  "lt-power": ltPower,
  "lt-hyperbolic": ltHyperbolic,
  "lt-identity": ltIdentity,
  "ilt-distinct": iltDistinct,
  "ilt-repeated": iltRepeated,
  "ilt-complex": iltComplex,
  "ilt-three": iltThree,
  "ilt-quadratic": iltQuadratic,
  "shift-s-forward": shiftSFwd,
  "shift-s-inverse": shiftSInv,
  "shift-t-forward": shiftTFwd,
  "shift-t-inverse": shiftTInv,
  "shift-piecewise": shiftBox,
  "livp-real": livpReal,
  "livp-complex": livpComplex,
  "livp-double": livpDouble,
  "livp-exp": livpExp,
  "livp-const": livpConst,
  "conv-compute": convCompute,
  "conv-inverse": convInverse,
  "conv-transform": convTransform,
  "conv-volterra": convVolterra,
  "fs-step": fsStep,
  "fs-sawtooth": fsSaw,
  "fs-parabola": fsParabola,
  "fs-abs": fsAbs,
  "fs-period-2l": fsPeriod2L,
  "fs-half-range": fsHalfRange,
  "pde-heat": pdeHeat,
  "pde-neumann": pdeNeumann,
  "pde-steady": pdeSteady,
  "pde-wave": pdeWave,
  "pde-rates": pdeRates,
  "spec-identify": specIdentify,
  "spec-legendre-n": specLegendreN,
  "spec-bessel-order": specBesselOrder,
  "spec-bessel-scaled": specBesselScaled,
  "spec-bessel-independent": specBesselIndependent,
};
