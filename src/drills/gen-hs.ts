// High school mathematics (Common Core HS): algebra & functions, geometry, trigonometry,
// statistics & probability. Level 1, built backward from clean answers: integer or
// rational roots, Pythagorean triples, special angles, least-squares data with planted
// residuals. Answers that need a calculator are checked to a stated tolerance.
// Every problem carries meta.mx + inputs for tests/verify/school_hs.py.
import { Rng } from "./rng";
import type { Draft } from "./types";
import { m } from "./tex";
import { Q } from "./rational";
import { require_ } from "./reject";
import { approx, choice, cx, draft, exact, gcd, int, par, poly, polyJs, polyPy, qpy, qref, qtex, sg, shuffle, tuple } from "./school";

type Gen = (r: Rng) => Draft;
const q = (n: number, d = 1) => new Q(n, d);
const deg = (a: number | string) => m(`${a}^\\circ`);
const RAD = Math.PI / 180;
/** 2-decimal answers: relative tolerance that still admits rounding to 2 places */
const tol2 = (v: number) => Math.max(5e-4, 0.0051 / Math.abs(v));
const r2 = (v: number) => (Math.round(v * 100) / 100).toFixed(2);
const TRIPLES = [[3, 4, 5], [5, 12, 13], [8, 15, 17], [7, 24, 25], [20, 21, 29]];

// ── exact trig values at multiples of 15° ─────────────────────────────────────
// sin of 0..90 by 15: [ref, tex]
const SIN15: [string, string][] = [["0", "0"], ["(sqrt(6)-sqrt(2))/4", "\\frac{\\sqrt6-\\sqrt2}{4}"], ["1/2", "\\frac12"], ["sqrt(2)/2", "\\frac{\\sqrt2}{2}"], ["sqrt(3)/2", "\\frac{\\sqrt3}{2}"], ["(sqrt(6)+sqrt(2))/4", "\\frac{\\sqrt6+\\sqrt2}{4}"], ["1", "1"]];
const TAN15: [string, string][] = [["0", "0"], ["2-sqrt(3)", "2-\\sqrt3"], ["sqrt(3)/3", "\\frac{\\sqrt3}{3}"], ["1", "1"], ["sqrt(3)", "\\sqrt3"], ["2+sqrt(3)", "2+\\sqrt3"]];
const neg = ([r, t]: [string, string]): [string, string] => (r === "0" ? [r, t] : [`-(${r})`, `-${t.startsWith("-") ? `(${t})` : t}`]);
/** exact sin / cos / tan of d degrees (multiple of 15); tan undefined -> null */
function trigExact(fn: "sin" | "cos" | "tan", d: number): [string, string] | null {
  d = ((d % 360) + 360) % 360;
  const k = d / 15;
  const ref = k % 6; // within quadrant
  const quad = Math.floor(k / 6);
  if (fn === "tan") {
    if (d % 180 === 90) return null;
    const base = quad % 2 === 0 ? TAN15[ref] : TAN15[(6 - ref) % 6];
    return quad % 2 === 0 ? base : neg(base);
  }
  // reduce to the reference angle
  const s = [SIN15[ref], SIN15[6 - ref], SIN15[ref], SIN15[6 - ref]][quad];
  const c = [SIN15[6 - ref], SIN15[ref], SIN15[6 - ref], SIN15[ref]][quad];
  const sSign = quad < 2 ? 1 : -1, cSign = quad === 0 || quad === 3 ? 1 : -1;
  return fn === "sin" ? (sSign > 0 ? s : neg(s)) : cSign > 0 ? c : neg(c);
}
const radTex = (d: number) => {
  const f = q(d, 180);
  if (f.isZero()) return "0";
  const num = f.n === 1 ? "\\pi" : f.n === -1 ? "-\\pi" : `${f.n}\\pi`;
  return f.d === 1 ? num : `\\frac{${num}}{${f.d}}`;
};

// ── algebra: equations & inequalities ─────────────────────────────────────────
const linearEq: Gen = (r) => {
  const x = q(r.nz(-12, 12), r.pick([1, 2, 3, 4])), a = q(r.nz(-9, 9), r.pick([1, 1, 2])), c = q(r.nz(-9, 9), r.pick([1, 1, 3])), b = r.int(-15, 15);
  require_(!a.sub(c).isZero());
  const d = a.sub(c).mul(x).add(b);
  return draft(`Solve ${m(`${cx(a, "x")}${sg(b)} = ${cx(c, "x")}${sg(d)}`)}.`, exact(x), `x = ${x.tex()}`,
    [`Collect ${m("x")} on one side: ${m(`${cx(a.sub(c), "x")} = ${d.sub(b).tex()}`)}.`, `${m(`x = ${x.tex()}`)}.`], { mx: "solve", eq: `${qpy(a)}*x + ${b} - (${qpy(c)}*x + ${qpy(d)})` });
};
const FORMULAS: { tex: string; py: string; v: string; sol: string; vars: string[] }[] = [
  { tex: "V = IR", py: "V - I*R", v: "R", sol: "V/I", vars: ["V", "I"] },
  { tex: "A = \\tfrac12 bh", py: "A - b*h/2", v: "h", sol: "2*A/b", vars: ["A", "b"] },
  { tex: "P = 2l + 2w", py: "P - 2*l - 2*w", v: "w", sol: "(P - 2*l)/2", vars: ["P", "l"] },
  { tex: "C = \\tfrac59(F - 32)", py: "C - 5*(F - 32)/9", v: "F", sol: "9*C/5 + 32", vars: ["C"] },
  { tex: "y = mx + b", py: "y - m*x - b", v: "x", sol: "(y - b)/m", vars: ["y", "m", "b"] },
  { tex: "v = u + at", py: "v - u - a*t", v: "t", sol: "(v - u)/a", vars: ["v", "u", "a"] },
  { tex: "PV = nRT", py: "P*V - n*R*T", v: "T", sol: "P*V/(n*R)", vars: ["P", "V", "n", "R"] },
  { tex: "A = P(1 + rt)", py: "A - P*(1 + r*t)", v: "r", sol: "(A - P)/(P*t)", vars: ["A", "P", "t"] },
  { tex: "ax + b = c", py: "a*x + b - c", v: "x", sol: "(c - b)/a", vars: ["a", "b", "c"] },
  { tex: "S = 2\\pi r h", py: "S - 2*pi*r*h", v: "h", sol: "S/(2*pi*r)", vars: ["S", "r"] },
];
const literal: Gen = (r) => {
  const f = r.pick(FORMULAS);
  return draft(`Solve ${m(f.tex)} for ${m(f.v)}.`, { kind: "expression", ref: f.sol, vars: f.vars, label: f.v }, `${f.v} = ${f.sol.replace(/\*/g, "")}`,
    [`Undo the operations around ${m(f.v)} in reverse order, doing the same to both sides.`], { mx: "literal", eq: f.py, v: f.v });
};
const IREL = ["<", "≤", ">", "≥"];
const linearIneq: Gen = (r) => {
  const a = r.nz(-6, 6), c = r.nz(-6, 6), b = r.int(-12, 12), k = q(r.nz(-9, 9), r.pick([1, 1, 2]));
  require_(a !== c);
  const rel = r.pick(IREL);
  const d = k.mul(a - c).add(b);
  const flip = a - c < 0;
  const out = flip ? { "<": ">", "≤": "≥", ">": "<", "≥": "≤" }[rel]! : rel;
  const opts = IREL.map((s) => `x ${s} ${qref(k)}`);
  return draft(`Solve ${m(`${cx(a, "x")}${sg(b)} ${({ "≤": "\\le", "≥": "\\ge" } as any)[rel] ?? rel} ${cx(c, "x")}${sg(d)}`)}.`, choice(opts, `x ${out} ${qref(k)}`), `x ${({ "≤": "\\le", "≥": "\\ge" } as any)[out] ?? out} ${k.tex()}`,
    [`Collect: ${m(`${cx(a - c, "x")}`)} vs ${m(d.sub(b).tex())}; divide by ${a - c}${flip ? " (negative: flip the inequality)" : ""}.`], { mx: "ineq", l: `${a}*x + ${b}`, r: `${c}*x + ${qpy(d)}`, rel });
};
const wordLinear: Gen = (r) => {
  const fixed = r.int(10, 60), rate = q(r.int(5, 40), r.pick([10, 100])), u = r.int(20, 600);
  const tot = rate.mul(u).add(fixed);
  require_([1, 2, 4, 5, 10, 20, 25, 50, 100].includes(tot.d));
  const T = Number(tot.value().toFixed(2));
  return draft(`A phone plan costs a flat ${m(`\\text{\\textdollar}${fixed}`)} plus ${m(`\\text{\\textdollar}${rate.value()}`)} per minute. One month's bill was ${m(`\\text{\\textdollar}${T}`)}. How many minutes were used?`, exact(u), `${u}`,
    [`${m(`${fixed} + ${rate.value()}m = ${T}`)}, so ${m(`m = (${T} - ${fixed}) / ${rate.value()} = ${u}`)}.`], { mx: "solve", eq: `${fixed} + ${qpy(rate)}*x - ${qpy(tot)}` });
};

// ── functions ────────────────────────────────────────────────────────────────
const funcEval: Gen = (r) => {
  const k = r.int(-5, 5);
  if (r.chance(0.6)) {
    const cs = [r.nz(-5, 5), r.int(-9, 9), r.int(-9, 9)];
    const v = cs[0] * k * k + cs[1] * k + cs[2];
    return draft(`${m(`f(x) = ${poly(cs)}`)}. Find ${m(`f(${k})`)}.`, exact(v), `${v}`, [`Substitute ${m(`x = ${k}`)}: ${m(`${cs[0]}(${k})^2 ${sg(cs[1])}(${k})${sg(cs[2])} = ${v}`)}.`], { mx: "eval", f: polyPy(cs), at: k });
  }
  const a = r.nz(-5, 5), b = r.int(-9, 9), c = r.nz(-6, 6);
  require_(k + c !== 0);
  const v = q(a * k + b, k + c);
  return draft(`${m(`f(x) = \\frac{${poly([a, b])}}{${poly([1, c])}}`)}. Find ${m(`f(${k})`)}.`, exact(v), v.tex(), [`${m(`f(${k}) = \\frac{${a * k + b}}{${k + c}} = ${v.tex()}`)}.`], { mx: "eval", f: `(${a}*x + ${b})/(x + ${c})`, at: k });
};
const seqRecursive: Gen = (r) => {
  const a1 = r.int(-5, 9), mul = r.pick([1, 1, 2, 3, -1]), d = r.int(-6, 6), k = r.int(4, 6);
  require_(mul !== 1 || d !== 0);
  const t = [a1];
  for (let i = 1; i < k; i++) t.push(mul * t[i - 1] + d);
  return draft(`${m(`a_1 = ${a1}`)}, ${m(`a_n = ${mul === 1 ? "" : mul === -1 ? "-" : mul}a_{n-1}${sg(d)}`)}. Find ${m(`a_{${k}}`)}.`, exact(t[k - 1]), `${t[k - 1]}`, [`${m(t.map((v, i) => `a_{${i + 1}} = ${v}`).join(",\\ "))}.`], { mx: "recur", a1, mul, d, k });
};
const avgRate: Gen = (r) => {
  const cs = [r.int(-3, 3), r.nz(-4, 4), r.int(-6, 6), r.int(-9, 9)], a = r.int(-3, 2), b = a + r.int(1, 4);
  const f = (x: number) => cs[0] * x ** 3 + cs[1] * x ** 2 + cs[2] * x + cs[3];
  const v = q(f(b) - f(a), b - a);
  return draft(`${m(`f(x) = ${poly(cs)}`)}. Find the average rate of change of ${m("f")} on ${m(`[${a}, ${b}]`)}.`, exact(v), v.tex(), [`${m(`\\frac{f(${b}) - f(${a})}{${b} - ${par(a)}} = \\frac{${f(b)} - ${par(f(a))}}{${b - a}} = ${v.tex()}`)}.`], { mx: "avg-rate", f: polyPy(cs), a, b });
};
const intercepts: Gen = (r) => {
  const A = r.nz(-9, 9), B = r.nz(-9, 9), C = A * B * r.nz(-4, 4);
  return draft(`Find the ${m("x")}- and ${m("y")}-intercepts of ${m(`${cx(A, "x")}${sg(B, "y")} = ${C}`)}.`, tuple([{ label: "x-intercept", tex: "x_0", ref: C / A }, { label: "y-intercept", tex: "y_0", ref: C / B }]), `(${C / A}, 0),\\ (0, ${C / B})`,
    [`Set ${m("y = 0")}: ${m(`x = ${C}/${par(A)} = ${C / A}`)}. Set ${m("x = 0")}: ${m(`y = ${C}/${par(B)} = ${C / B}`)}.`], { mx: "intercepts", e: `${A}*x + ${B}*y - ${C}` });
};
const LE = ["Linear", "Exponential", "Neither"];
const linExp: Gen = (r) => {
  const t = r.int(0, 3);
  if (t === 3) {
    const descs: [string, string][] = [
      [`A savings account grows by ${r.int(2, 9)}% each year.`, "Exponential"], [`A plant grows ${r.int(2, 9)} cm each week.`, "Linear"], [`A car loses ${r.int(10, 25)}% of its value every year.`, "Exponential"],
      [`A pool drains at ${r.int(20, 90)} liters per minute.`, "Linear"], [`A bacteria population doubles every ${r.int(2, 6)} hours.`, "Exponential"], [`A taxi charges a flat fee plus ${m(`\\text{\\textdollar}${r.int(2, 4)}`)} per mile.`, "Linear"],
    ];
    const [txt, ans] = r.pick(descs);
    return draft(`Which model fits? ${txt}`, choice(LE.slice(0, 2), ans), `\\text{${ans}}`, [ans === "Linear" ? `A constant amount per unit of time: linear.` : `A constant percent (factor) per unit of time: exponential.`], { mx: "le-desc", txt });
  }
  const a = r.int(2, 8), d = r.nz(-5, 7), b = r.pick([2, 3]);
  const ys = [0, 1, 2, 3].map((x) => (t === 0 ? a + d * x : t === 1 ? a * b ** x : a + x * x + (x === 3 ? 1 : 0)));
  return draft(`A table: ${m([0, 1, 2, 3].map((x, i) => `(${x}, ${ys[i]})`).join(",\\ "))}. Is the function linear, exponential, or neither?`, choice(LE, LE[t]), `\\text{${LE[t]}}`,
    [`Differences: ${ys.slice(1).map((y, i) => y - ys[i]).join(", ")}; ratios: ${ys.slice(1).map((y, i) => q(y, ys[i]).tex()).map((s) => m(s)).join(", ")}. Equal differences ⇒ linear; equal ratios ⇒ exponential.`], { mx: "le-table", ys });
};
const exp2pts: Gen = (r) => {
  const a = r.nz(-5, 9), b = r.pick([q(2), q(3), q(1, 2), q(3, 2), q(1, 3), q(4)]), x1 = r.int(1, 2), x2 = x1 + r.int(1, 2);
  const y = (x: number) => q(a).mul(Q.of(b.n ** x).div(b.d ** x));
  return draft(`An exponential function ${m("y = a\\cdot b^x")} passes through ${m(`(${x1}, ${y(x1).tex()})`)} and ${m(`(${x2}, ${y(x2).tex()})`)}. Find ${m("a")} and ${m("b")}.`, tuple([{ label: "a", tex: "a", ref: a }, { label: "b", tex: "b", ref: b }]), `y = ${a}\\cdot ${par(b.tex())}^x`,
    [`Divide: ${m(`b^{${x2 - x1}} = ${y(x2).div(y(x1)).tex()}`)}, so ${m(`b = ${b.tex()}`)}; then ${m(`a = y_1 / b^{${x1}} = ${a}`)}.`], { mx: "exp2", p: [x1, qpy(y(x1))], q: [x2, qpy(y(x2))] });
};
const seqExplicit: Gen = (r) => {
  const a1 = r.nz(-9, 12), geo = r.chance(0.5), d = geo ? r.pick([2, 3, -2, 1 / 2]) : r.nz(-7, 7);
  const ref = geo ? `${a1}*(${d})^(n-1)` : `${a1} + (n-1)*(${d})`;
  const terms = [1, 2, 3, 4].map((n) => (geo ? a1 * d ** (n - 1) : a1 + (n - 1) * d));
  return draft(`Write an explicit formula ${m("a_n")} for the ${geo ? "geometric" : "arithmetic"} sequence ${m(`${terms.map((t) => q(Math.round(t * 8), 8).tex()).join(",\\ ")},\\ \\ldots`)} (first term ${m("a_1")}).`,
    { kind: "expression", ref, vars: ["n"], label: "a_n", points: [1, 2, 3, 4, 5, 6, 7].map((n) => ({ n })) }, geo ? `a_n = ${a1}\\cdot ${par(q(Math.round(d * 2), 2).tex())}^{n-1}` : `a_n = ${a1}${sg(d)}(n-1)`,
    [geo ? `Common ratio ${m(`r = ${q(Math.round(d * 2), 2).tex()}`)}: ${m("a_n = a_1 r^{n-1}")}.` : `Common difference ${m(`d = ${d}`)}: ${m("a_n = a_1 + (n-1)d")}.`], { mx: "seq", terms: terms.map((t) => `${t}`), geo });
};
const expParams: Gen = (r) => {
  const t = r.int(0, 2);
  if (t === 0) {
    const p = r.int(1, 30), up = r.chance(0.5), P = r.int(2, 90) * 100;
    const b = q(100 + (up ? p : -p), 100);
    return draft(`${m(`V(t) = ${int(P)}(${b.value()})^t`)}. What is the percent rate of change per unit ${m("t")}? (Use a negative number for decay.)`, exact(up ? p : -p), `${up ? p : -p}\\%`,
      [`Factor ${b.value()} = 1 ${up ? "+" : "−"} ${p / 100}: ${up ? "growth" : "decay"} of ${p}% per period.`], { mx: "pct-rate", b: qpy(b), per: 1 });
  }
  const g = r.pick([10, 15, 20, 25, 50]), k = t === 1 ? r.pick([5, 10]) : 12;
  const b = 1 + g / 100;
  const per = t === 1 ? `y = (${b})^{t/${k}}` : `y = (${b})^t`;
  const v = (b ** (1 / k) - 1) * 100;
  return draft(t === 1 ? `${m(per)} with ${m("t")} in years. What is the equivalent annual percent growth rate? (2 decimals)` : `${m(per)} with ${m("t")} in years. Rewrite as ${m("(b)^{12t}")}: what is the equivalent monthly percent growth rate? (2 decimals)`,
    approx(v, tol2(v)), `${r2(v)}\\%`, [`${m(`${b}^{1/${k}} \\approx ${(b ** (1 / k)).toFixed(5)}`)}, so about ${r2(v)}% per ${t === 1 ? "year" : "month"}.`], { mx: "pct-rate", b: `${b}`, per: k });
};
const rationalExp: Gen = (r) => {
  const t = r.int(0, 1);
  if (t === 0) {
    const base = r.pick([2, 3, 4, 5]), den = r.pick([2, 3, 4]), num = r.nz(-4, 4);
    require_(base ** num <= 1000 && gcd(Math.abs(num), den) === 1 && den !== 1);
    const B = base ** den;
    const v = num >= 0 ? q(base ** num) : q(1, base ** -num);
    return draft(`Evaluate ${m(`${B}^{${q(num, den).tex()}}`)}.`, exact(v), v.tex(), [`${m(`${B}^{1/${den}} = ${base}`)}, then raise to the ${num}: ${m(v.tex())}.`], { mx: "expr", e: `${B}**(${num}/${den})` });
  }
  const p = r.int(1, 7), qd = r.pick([2, 3, 4]), s = r.int(1, 5), sd = r.pick([2, 3, 4]);
  const e = q(p, qd).add(q(s, sd));
  return draft(`Write ${m(`\\sqrt[${qd}]{x^{${p}}}\\cdot x^{${q(s, sd).tex()}}`)} as ${m("x^k")}. What is ${m("k")}?`, exact(e), e.tex(), [`${m(`\\sqrt[${qd}]{x^{${p}}} = x^{${p}/${qd}}`)}; add exponents: ${m(e.tex())}.`], { mx: "exponent", e: `x**(${p}/${qd}) * x**(${s}/${sd})` });
};
const halfPlane: Gen = (r) => {
  const m1 = r.nz(-4, 4), b1 = r.int(-6, 6), a2 = r.nz(-3, 3), c2 = r.int(-8, 8), x = r.int(-5, 5), y = r.int(-6, 6);
  const rel1 = r.pick([">", "≤"]), rel2 = r.pick(["≥", "<"]);
  const ok = (rel1 === ">" ? y > m1 * x + b1 : y <= m1 * x + b1) && (rel2 === "≥" ? x + a2 * y >= c2 : x + a2 * y < c2);
  const tx = (s: string) => ({ "≤": "\\le", "≥": "\\ge" } as any)[s] ?? s;
  return draft(`Is ${m(`(${x}, ${y})`)} a solution of the system ${m(`y ${tx(rel1)} ${poly([m1, b1])},\\quad x${sg(a2, "y")} ${tx(rel2)} ${c2}`)}?`, choice(["Yes", "No"], ok ? "Yes" : "No"), `\\text{${ok ? "Yes" : "No"}}`,
    [`Substitute: ${m(`${y} ${tx(rel1)} ${m1 * x + b1}`)} is ${(rel1 === ">" ? y > m1 * x + b1 : y <= m1 * x + b1) ? "true" : "false"}; ${m(`${x + a2 * y} ${tx(rel2)} ${c2}`)} is ${(rel2 === "≥" ? x + a2 * y >= c2 : x + a2 * y < c2) ? "true" : "false"}. A solution must satisfy both.`], { mx: "half-plane", ineqs: [`y ${rel1 === ">" ? ">" : "<="} ${m1}*x + ${b1}`, `x + ${a2}*y ${rel2 === "≥" ? ">=" : "<"} ${c2}`], x, y });
};

// ── polynomials & quadratics ─────────────────────────────────────────────────
const mulPoly = (a: number[], b: number[]) => {
  const out = Array(a.length + b.length - 1).fill(0);
  a.forEach((x, i) => b.forEach((y, j) => (out[i + j] += x * y)));
  return out;
};
const polyArith: Gen = (r) => {
  const p = [r.nz(-4, 4), r.int(-6, 6)], qq = r.chance(0.5) ? [r.nz(-3, 3), r.int(-5, 5), r.int(-6, 6)] : [r.nz(-4, 4), r.int(-6, 6)];
  const add = r.chance(0.3);
  let res: number[], tex: string;
  if (add) {
    const a = [r.int(-5, 5), r.nz(-6, 6), r.int(-6, 6), r.int(-9, 9)], b = [r.int(-5, 5), r.int(-6, 6), r.int(-6, 6), r.int(-9, 9)];
    res = a.map((v, i) => v - b[i]);
    require_(res[0] !== 0 || res[1] !== 0);
    tex = `(${poly(a)}) - (${poly(b)})`;
    while (res.length < 4) res.unshift(0);
    return draft(`Simplify ${m(tex)} to ${m("ax^3 + bx^2 + cx + d")}. Give ${m("a, b, c, d")}.`, tuple(["a", "b", "c", "d"].map((l, i) => ({ label: l, tex: l, ref: res[i] }))), poly(res),
      [`Subtract like terms: ${m(poly(res))}.`], { mx: "coeffs", e: `(${polyPy(a)}) - (${polyPy(b)})`, deg: 3 });
  }
  res = mulPoly(p, qq);
  while (res.length < 4) res.unshift(0);
  return draft(`Expand ${m(`(${poly(p)})(${poly(qq)})`)} to ${m("ax^3 + bx^2 + cx + d")}. Give ${m("a, b, c, d")}.`, tuple(["a", "b", "c", "d"].map((l, i) => ({ label: l, tex: l, ref: res[i] }))), poly(res),
    [`Distribute every term of the first factor over the second and combine like terms: ${m(poly(res))}.`], { mx: "coeffs", e: `(${polyPy(p)})*(${polyPy(qq)})`, deg: 3 });
};
const factorZeros: Gen = (r) => {
  const a = r.pick([1, 1, 1, 2, 3]), p = q(r.nz(-9, 9), a === 1 ? 1 : r.pick([1, a])), s = q(r.int(-9, 9));
  const lead = a;
  // a(x - p)(x - s) with a·p integer
  const cs = [lead, -lead * (p.value() + s.value()), lead * p.value() * s.value()];
  require_(cs.every(Number.isInteger) && !p.sub(s).isZero());
  return draft(`Find the zeros of ${m(`f(x) = ${poly(cs)}`)} by factoring. (List them, separated by commas.)`, { kind: "roots", ref: [p.value(), s.value()], label: "x" }, `x = ${p.tex()},\\ ${s.tex()}`,
    [`${m(`${poly(cs)} = ${lead === 1 ? "" : lead}(x ${p.n < 0 ? "+" : "-"} ${Math.abs(p.value())})(x ${s.n < 0 ? "+" : "-"} ${Math.abs(s.value())})`)}.`, `A product is 0 exactly when a factor is.`], { mx: "zeros", e: polyPy(cs) });
};
const completeSquare: Gen = (r) => {
  const h = r.nz(-8, 8), k = r.int(-20, 20), a = r.pick([1, 1, 2, -1, 3]);
  const cs = [a, -2 * a * h, a * h * h + k];
  return draft(`Write ${m(`${poly(cs)}`)} in vertex form ${m(`${a === 1 ? "" : a === -1 ? "-" : a}(x - h)^2 + k`)}. Give ${m("h")} and ${m("k")}.`, tuple([{ label: "h", tex: "h", ref: h }, { label: "k", tex: "k", ref: k }]), `${a === 1 ? "" : a === -1 ? "-" : a}(x ${h < 0 ? "+" : "-"} ${Math.abs(h)})^2${sg(k)}`,
    [`${a !== 1 ? `Factor ${a} from the x-terms, then h` : "H"}alf the x-coefficient is ${m(`${-h}`)}; square it and compensate: ${m(`k = ${k}`)}.`, `The ${a > 0 ? "minimum" : "maximum"} value is ${k}, at ${m(`x = ${h}`)}.`], { mx: "vertex-form", e: polyPy(cs), a });
};
const quadFormula: Gen = (r) => {
  if (r.chance(0.35)) {
    const a = r.nz(-4, 4), b = r.int(-9, 9), c = r.int(-9, 9);
    const D = b * b - 4 * a * c;
    const n = D > 0 ? "2" : D === 0 ? "1" : "0";
    return draft(`How many real solutions does ${m(`${poly([a, b, c])} = 0`)} have?`, choice(["0", "1", "2"], n), n, [`Discriminant ${m(`b^2 - 4ac = ${D}`)}: ${D > 0 ? "positive ⇒ 2" : D === 0 ? "zero ⇒ 1" : "negative ⇒ 0"} real solutions.`], { mx: "nreal", e: polyPy([a, b, c]) });
  }
  const a = r.pick([1, 1, 2, 3]), b = r.int(-9, 9), c = r.int(-9, 9);
  const D = b * b - 4 * a * c;
  const sq = Math.round(Math.sqrt(D));
  require_(D > 0 && sq * sq !== D);
  // simplify sqrt(D) = s√t
  let s = 1, t = D;
  for (let k = 2; k * k <= t; k++) while (t % (k * k) === 0) { t /= k * k; s *= k; }
  const g = gcd(gcd(Math.abs(b), s), 2 * a);
  const ref = [`(${-b} + sqrt(${D}))/(${2 * a})`, `(${-b} - sqrt(${D}))/(${2 * a})`];
  return draft(`Solve ${m(`${poly([a, b, c])} = 0`)} with the quadratic formula. Give both solutions exactly, e.g. (3 + sqrt(5))/2, (3 - sqrt(5))/2.`, { kind: "roots", ref: ref.map((e) => Function("sqrt", `return ${e}`)(Math.sqrt)), label: "x" },
    `x = \\frac{${-b / g === 0 ? "" : -b / g} \\pm ${s / g === 1 ? "" : s / g}\\sqrt{${t}}}{${(2 * a) / g}}`,
    [`${m(`x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a} = \\frac{${-b} \\pm \\sqrt{${D}}}{${2 * a}}`)}.`, `${m(`\\sqrt{${D}} = ${s === 1 ? "" : s}\\sqrt{${t}}`)}.`], { mx: "zeros", e: polyPy([a, b, c]) });
};
const quadWord: Gen = (r) => {
  const T = r.int(2, 8), s = q(r.int(1, 8), r.pick([2, 4]));
  // h(t) = -16(t - T)(t + s) = -16t^2 + 16(T - s)t + 16Ts
  require_(s.value() < T);
  const v = q(16 * T).sub(s.mul(16)), h0 = s.mul(16 * T);
  const tv = q(T).sub(s).div(2), hmax = tv.sub(T).mul(tv.add(s)).mul(-16);
  require_(v.isInt() && h0.isInt());
  const ask = r.int(0, 1);
  return draft(`A ball's height in feet is ${m(`h(t) = -16t^2 + ${v.n}t + ${h0.n}`)} (${m("t")} in seconds). ${ask ? "What is its maximum height in feet?" : "When does it hit the ground?"}`, exact(ask ? hmax : q(T)), ask ? hmax.tex() : `${T}`,
    [ask ? `Vertex at ${m(`t = -b/2a = ${tv.tex()}`)}; ${m(`h(${tv.tex()}) = ${hmax.tex()}`)}.` : `Solve ${m("h(t) = 0")}: ${m(`-16(t - ${T})(t + ${s.tex()}) = 0`)}; reject the negative root.`], { mx: "projectile", e: `-16*x**2 + ${v.n}*x + ${h0.n}`, ask });
};
const linQuad: Gen = (r) => {
  const x1 = r.int(-6, 6), x2 = r.int(-6, 6), mm = r.int(-4, 4), k = r.int(-8, 8);
  require_(x1 !== x2);
  // x^2 + bx + c - (mx + k) = (x - x1)(x - x2)
  const b = -(x1 + x2) + mm, c = x1 * x2 + k;
  return draft(`Find the ${m("x")}-coordinates where ${m(`y = ${poly([1, b, c])}`)} meets ${m(`y = ${poly([mm, k])}`)}.`, { kind: "roots", ref: [x1, x2], label: "x" }, `x = ${x1},\\ ${x2}`,
    [`Set equal: ${m(`${poly([1, b - mm, c - k])} = 0 = (x${sg(-x1)})(x${sg(-x2)})`)}.`], { mx: "lin-quad", f: polyPy([1, b, c]), g: polyPy([mm, k]) });
};
const vertex: Gen = (r) => {
  const a = q(r.nz(-3, 3), r.pick([1, 1, 2])), h = r.int(-6, 6), k = r.int(-10, 10);
  const cs = [a, a.mul(-2 * h), a.mul(h * h).add(k)];
  require_(cs.every((c) => c.isInt()));
  return draft(`Find the vertex of ${m(`y = ${poly(cs)}`)}.`, tuple([{ label: "x", tex: "h", ref: h }, { label: "y", tex: "k", ref: k }]), `(${h}, ${k})`,
    [`${m(`h = -\\frac{b}{2a} = ${h}`)}; ${m(`k = y(${h}) = ${k}`)}. Axis of symmetry ${m(`x = ${h}`)}; ${a.n > 0 ? "minimum" : "maximum"} ${k}.`], { mx: "vertex", e: polyPy(cs) });
};
const transformFn: Gen = (r) => {
  const base = r.pick([["x^2", "x^2", "(X)^2"], ["|x|", "abs(x)", "abs(X)"], ["x^3", "x^3", "(X)^3"]]), h = r.nz(-5, 5), k = r.int(-6, 6), a = r.pick([1, 1, -1, 2, -2]);
  const inner = `(x ${h > 0 ? "-" : "+"} ${Math.abs(h)})`;
  const ref = `${a}*${base[2].replace("X", inner)} + ${k}`;
  return draft(`${m(`f(x) = ${base[0]}`)}. The graph of ${m("g")} is the graph of ${m("f")}${a === -1 ? " reflected across the x-axis, then" : a === 2 ? " stretched vertically by 2, then" : a === -2 ? " stretched vertically by 2 and reflected across the x-axis, then" : ""} shifted ${Math.abs(h)} unit${Math.abs(h) > 1 ? "s" : ""} ${h > 0 ? "right" : "left"}${k ? ` and ${Math.abs(k)} ${k > 0 ? "up" : "down"}` : ""}. Write ${m("g(x)")}.`,
    { kind: "expression", ref, vars: ["x"], label: "g(x)" }, `g(x) = ${a === 1 ? "" : a === -1 ? "-" : a}${base[0].replace("x", inner)}${sg(k)}`,
    [`Right ${m("h")}: replace ${m("x")} by ${m("x - h")}; up ${m("k")}: add ${m("k")}; vertical stretch/reflection: multiply ${m("f")}.`], { mx: "transform-fn", f: base[1].replace("^", "**"), a, h, k });
};
const EOD = ["Even", "Odd", "Neither"];
const evenOdd: Gen = (r) => {
  const t = r.int(0, 2);
  const c = [r.nz(-5, 5), r.nz(-5, 5), r.nz(-5, 5)];
  const forms = [[`${cx(c[0], "x^4")}${sg(c[1], "x^2")}${sg(c[2])}`, `${c[0]}*x**4 + ${c[1]}*x**2 + ${c[2]}`], [`${cx(c[0], "x^5")}${sg(c[1], "x^3")}${sg(c[2], "x")}`, `${c[0]}*x**5 + ${c[1]}*x**3 + ${c[2]}*x`], [`${cx(c[0], "x^3")}${sg(c[1], "x^2")}`, `${c[0]}*x**3 + ${c[1]}*x**2`]];
  const alt = [[`|x|${sg(c[2])}`, `abs(x) + ${c[2]}`], [`x|x|`, `x*abs(x)`], [`(x${sg(c[2])})^2`, `(x + ${c[2]})**2`]];
  const [tex, py] = r.chance(0.3) ? alt[t] : forms[t];
  return draft(`Is ${m(`f(x) = ${tex}`)} even, odd, or neither?`, choice(EOD, EOD[t]), `\\text{${EOD[t]}}`, [`Compute ${m("f(-x)")}: ${["it equals f(x) (symmetric about the y-axis)", "it equals −f(x) (symmetric about the origin)", "it is neither f(x) nor −f(x)"][t]}.`], { mx: "even-odd", e: py });
};
const inverse: Gen = (r) => {
  const t = r.int(0, 2);
  const a = r.nz(-6, 6), b = r.int(-9, 9), c = r.pick([1, 2, 3, 5]);
  if (t === 0) return draft(`Find ${m("f^{-1}(x)")} for ${m(`f(x) = \\frac{${poly([a, b])}}{${c}}`)}.`, { kind: "expression", ref: `(${c}*x - (${b}))/(${a})`, vars: ["x"], label: "f^{-1}(x)" }, `f^{-1}(x) = \\frac{${c}x${sg(-b)}}{${a}}`, [`Swap ${m("x")} and ${m("y")} and solve: ${m(`x = \\frac{${a}y${sg(b)}}{${c}}`)}.`], { mx: "inverse", f: `(${a}*x + ${b})/${c}` });
  if (t === 1) {
    const k = r.int(-9, 0), s = r.pick([1, 2, 4]);
    return draft(`Find ${m("f^{-1}(x)")} for ${m(`f(x) = ${s === 1 ? "" : s}x^3${sg(k)}`)}.`, { kind: "expression", ref: `cbrt((x - (${k}))/${s})`, vars: ["x"], label: "f^{-1}(x)" }, `f^{-1}(x) = \\sqrt[3]{\\frac{x${sg(-k)}}{${s}}}`, [`${m(`y = ${s}x^3${sg(k)} \\Rightarrow x^3 = \\frac{y${sg(-k)}}{${s}}`)}; take the cube root.`], { mx: "inverse", f: `${s}*x**3 + ${k}` });
  }
  const d = r.nz(-5, 5), e = r.nz(-5, 5);
  require_(a * d - b * 1 !== 0 && e !== 0);
  // f(x) = (a x + b)/(x + d)  ->  f^{-1}(x) = (b - d x)/(x - a)
  return draft(`Find ${m("f^{-1}(x)")} for ${m(`f(x) = \\frac{${poly([a, b])}}{${poly([1, d])}}`)}.`, { kind: "expression", ref: `((${b}) - (${d})*x)/(x - (${a}))`, vars: ["x"], label: "f^{-1}(x)" }, `f^{-1}(x) = \\frac{${poly([-d, b])}}{x${sg(-a)}}`,
    [`${m(`y(x${sg(d)}) = ${poly([a, b])}`)} ⇒ ${m(`x(y - ${par(a)}) = ${b} - ${par(d)}y`)}; swap the letters.`], { mx: "inverse", f: `(${a}*x + ${b})/(x + ${d})` });
};
const piecewise: Gen = (r) => {
  const c = r.int(-3, 3), a = r.nz(-4, 4), b = r.int(-5, 5), p = r.int(-4, 4), x = r.pick([c - 2, c - 1, c, c + 1, c + 3]);
  const t = r.int(0, 2);
  if (t === 1) {
    const xv = q(r.int(-40, 40), 10);
    const diff = q(p).sub(xv), v = q(Math.floor(xv.value())).add(diff.n < 0 ? diff.neg() : diff);
    return draft(`Evaluate ${m(`\\lfloor ${xv.value()} \\rfloor + |${p} - ${par(xv.value())}|`)} (floor = greatest integer ≤ the number).`, exact(v), `${v.value()}`,
      [`${m(`\\lfloor ${xv.value()} \\rfloor = ${Math.floor(xv.value())}`)}; ${m(`|${p} - ${par(xv.value())}| = ${Math.abs(p - xv.value()).toFixed(1).replace(/\.0$/, "")}`)}.`], { mx: "expr", e: `floor(${qpy(xv)}) + abs(${p} - (${qpy(xv)}))` });
  }
  const v = x < c ? a * x + b : x * x - p;
  return draft(`${m(`f(x) = \\begin{cases} ${poly([a, b])} & x < ${c} \\\\ x^2 - ${par(p)} & x \\ge ${c} \\end{cases}`)} Find ${m(`f(${x})`)}.`, exact(v), `${v}`, [`${m(`${x} ${x < c ? "<" : "\\ge"} ${c}`)}, so use the ${x < c ? "first" : "second"} piece: ${m(`${v}`)}.`], { mx: "piecewise", a, b, c, p, x });
};
const structure: Gen = (r) => {
  const t = r.int(0, 2);
  if (t === 0) {
    const p = r.int(1, 4), s = r.int(1, 5);
    require_(p !== s);
    const cs = [1, 0, -(p * p + s * s), 0, p * p * s * s];
    return draft(`Find all real zeros of ${m(poly(cs))}. (Treat it as a quadratic in ${m("x^2")}.)`, { kind: "roots", ref: [p, -p, s, -s], label: "x" }, `x = \\pm ${p},\\ \\pm ${s}`, [`${m(`(x^2 - ${p * p})(x^2 - ${s * s}) = 0`)}.`], { mx: "real-zeros", e: polyPy(cs) });
  }
  if (t === 1) {
    const a = r.int(1, 5), b = r.int(1, 3);
    const cs = [b ** 2, 0, 0, 0, -(a ** 4)];
    require_(gcd(a, b) === 1);
    return draft(`Find all real zeros of ${m(poly(cs))}. (Difference of squares, twice.)`, { kind: "roots", ref: [a / Math.sqrt(b), -a / Math.sqrt(b)].map((v) => v), label: "x" }, `x = \\pm\\frac{${a}}{\\sqrt{${b}}}`, [`${m(`(${b === 1 ? "" : b}x^2 - ${a * a})(${b === 1 ? "" : b}x^2 + ${a * a})`)}; the second factor has no real zeros.`], { mx: "real-zeros", e: polyPy(cs) });
  }
  const a = r.int(1, 6), s = r.pick([1, -1]);
  return draft(`Find all real zeros of ${m(`x^3 ${s > 0 ? "-" : "+"} ${a ** 3}`)}. (Sum or difference of cubes.)`, { kind: "roots", ref: [s * a], label: "x" }, `x = ${s * a}`, [`${m(`(x ${s > 0 ? "-" : "+"} ${a})(x^2 ${s > 0 ? "+" : "-"} ${a}x + ${a * a})`)}; the quadratic has negative discriminant.`], { mx: "real-zeros", e: `x**3 - (${s * a ** 3})` });
};
const binom = (n: number, k: number) => { let c = 1; for (let i = 0; i < k; i++) c = (c * (n - i)) / (i + 1); return c; };
const binomial: Gen = (r) => {
  const n = r.int(3, 7), k = r.int(1, n - 1), a = r.nz(-3, 3), b = r.nz(-3, 3);
  const c = binom(n, k) * a ** k * b ** (n - k);
  return draft(`What is the coefficient of ${m(`x^{${k}}`)} in ${m(`(${cx(a, "x")}${sg(b)})^{${n}}`)}?`, exact(c), `${c}`, [`Binomial theorem: ${m(`\\binom{${n}}{${k}}(${a})^{${k}}(${b})^{${n - k}} = ${binom(n, k)} \\cdot ${a ** k} \\cdot ${b ** (n - k)} = ${c}`)}.`], { mx: "binom-coef", e: `(${a}*x + ${b})**${n}`, k });
};
const remainder: Gen = (r) => {
  const cs = [r.nz(-3, 3), r.int(-5, 5), r.int(-6, 6), r.int(-9, 9)], a = r.nz(-3, 3);
  const v = cs[0] * a ** 3 + cs[1] * a ** 2 + cs[2] * a + cs[3];
  return draft(`What is the remainder when ${m(`p(x) = ${poly(cs)}`)} is divided by ${m(`x${sg(-a)}`)}?`, exact(v), `${v}`, [`Remainder theorem: the remainder is ${m(`p(${a}) = ${v}`)}.${v === 0 ? ` So ${m(`x${sg(-a)}`)} is a factor.` : ""}`], { mx: "remainder", e: polyPy(cs), a });
};
const polyZeros: Gen = (r) => {
  const zs = [r.int(-5, 5), r.int(-5, 5), r.int(-5, 5)];
  require_(new Set(zs).size === 3);
  const cs = mulPoly(mulPoly([1, -zs[0]], [1, -zs[1]]), [1, -zs[2]]);
  return draft(`Find all zeros of ${m(`p(x) = ${poly(cs)}`)}. One of them is ${m(`${zs[0]}`)}.`, { kind: "roots", ref: zs, label: "x" }, `x = ${[...new Set(zs)].join(",\\ ")}`,
    [`Divide by ${m(`x${sg(-zs[0])}`)} (synthetic division), then factor the quadratic.`], { mx: "zeros", e: polyPy(cs) });
};
const geomSeries: Gen = (r) => {
  const a = r.nz(-6, 9), rr = r.pick([2, 3, -2, q(1, 2), q(-1, 2), q(1, 3)].map(Q.of)), n = r.int(4, 8);
  const v = q(a).mul(q(1).sub(Q.of(rr.n ** n).div(rr.d ** n))).div(q(1).sub(rr));
  return draft(`Find the sum of the first ${n} terms of the geometric series with first term ${a} and ratio ${m(rr.tex())}.`, exact(v), v.tex(), [`${m(`S_n = a\\frac{1 - r^n}{1 - r} = ${a}\\cdot\\frac{1 - (${rr.tex()})^{${n}}}{1 - ${par(rr.tex())}} = ${v.tex()}`)}.`], { mx: "geo-sum", a, r: qpy(rr), n });
};
const polyDiv: Gen = (r) => {
  const qq = [r.nz(-3, 3), r.int(-6, 6), r.int(-6, 6)].slice(r.chance(0.5) ? 0 : 1), d = r.nz(-4, 4), rem = r.int(-9, 9);
  const num = mulPoly(qq, [1, -d]);
  num[num.length - 1] += rem;
  return draft(`Divide ${m(`(${poly(num)}) \\div (x${sg(-d)})`)}. Give the quotient ${m("q(x)")} and the remainder ${m("r")}.`,
    tuple([{ label: "q(x)", tex: "q(x)", ref: polyJs(qq) }, { label: "r", tex: "r", ref: rem }], ["x"]), `q(x) = ${poly(qq)},\\ r = ${rem}`,
    [`Long or synthetic division by ${m(`x${sg(-d)}`)}; check: ${m(`(x${sg(-d)})(${poly(qq)})${sg(rem)} = ${poly(num)}`)}.`], { mx: "polydiv", num: polyPy(num), d });
};
const rationalAdd: Gen = (r) => {
  const a = r.nz(-6, 6), b = r.nz(-6, 6), p = r.nz(-5, 5), s = r.nz(-5, 5), plus = r.chance(0.6);
  require_(p !== s);
  const sb = plus ? b : -b;
  const P = a + sb, Qc = a * s + sb * p;
  return draft(`Write ${m(`\\frac{${a}}{x${sg(p)}} ${plus ? "+" : "-"} \\frac{${b}}{x${sg(s)}}`)} as ${m(`\\frac{Px + Q}{(x${sg(p)})(x${sg(s)})}`)}. Give ${m("P")} and ${m("Q")}.`, tuple([{ label: "P", tex: "P", ref: P }, { label: "Q", tex: "Q", ref: Qc }]), `\\frac{${poly([P, Qc])}}{(x${sg(p)})(x${sg(s)})}`,
    [`Common denominator: ${m(`${a}(x${sg(s)}) ${plus ? "+" : "-"} ${b}(x${sg(p)}) = ${poly([P, Qc])}`)}.`], { mx: "rat-add", e: `${a}/(x + ${p}) ${plus ? "+" : "-"} ${b}/(x + ${s})`, den: `(x + ${p})*(x + ${s})` });
};
const rationalEq: Gen = (r) => {
  if (r.chance(0.5)) {
    const a = r.nz(-6, 6), k = r.int(-6, 6);
    require_(-a - k !== a);
    return draft(`Solve ${m(`\\frac{x^2 ${sg(k, "x")}}{x${sg(-a)}} = \\frac{${a * a + k * a}}{x${sg(-a)}}`)}. Give only true solutions.`, { kind: "roots", ref: [-a - k], label: "x" }, `x = ${-a - k}`,
      [`Multiply by ${m(`x${sg(-a)}`)}: ${m(`x^2 ${sg(k, "x")} - ${par(a * a + k * a)} = (x${sg(-a)})(x${sg(a + k)}) = 0`)}.`, `${m(`x = ${a}`)} makes the denominator 0: extraneous.`], { mx: "solve-real", eq: `(x**2 + ${k}*x)/(x - (${a})) - (${a * a + k * a})/(x - (${a}))` });
  }
  const qv = r.int(-3, 6), s = r.int(2, 6), x1 = qv + s, x2 = qv + 1 - s, p = qv * qv - x1 * x2;
  return draft(`Solve ${m(`\\sqrt{x${sg(p)}} = x${sg(-qv)}`)}. Give only true solutions.`, { kind: "roots", ref: [x1], label: "x" }, `x = ${x1}`,
    [`Square: ${m(`x${sg(p)} = (x${sg(-qv)})^2`)} ⇒ ${m(`x = ${x1}`)} or ${m(`x = ${x2}`)}.`, `Check: ${m(`x = ${x2}`)} makes the right side negative — extraneous.`], { mx: "solve-real", eq: `sqrt(x + (${p})) - (x - (${qv}))` });
};
const complexArith: Gen = (r) => {
  const a = r.int(-6, 6), b = r.nz(-6, 6), c = r.int(-6, 6), d = r.nz(-6, 6), t = r.int(0, 2);
  const zt = (x: number, y: number) => `${x === 0 ? "" : x}${y < 0 ? "-" : x === 0 ? "" : "+"}${Math.abs(y) === 1 ? "" : Math.abs(y)}i`;
  if (t === 2) {
    const n = r.int(2, 40);
    const [re, im] = [[1, 0], [0, 1], [-1, 0], [0, -1]][n % 4];
    return draft(`Write ${m(`i^{${n}}`)} in the form ${m("a + bi")}.`, tuple([{ label: "a", tex: "a", ref: re }, { label: "b", tex: "b", ref: im }]), re ? `${re}` : `${im === 1 ? "" : "-"}i`, [`Powers of ${m("i")} cycle every 4: ${n} = 4·${Math.floor(n / 4)} + ${n % 4}.`], { mx: "complex", e: `I**${n}` });
  }
  const [re, im] = t === 0 ? [a * c - b * d, a * d + b * c] : [a - c, b - d];
  return draft(`Write ${m(`(${zt(a, b)})${t === 0 ? "" : " - "}(${zt(c, d)})`)} in the form ${m("a + bi")}.`, tuple([{ label: "a", tex: "a", ref: re }, { label: "b", tex: "b", ref: im }]), `${re}${sg(im, "i")}`,
    [t === 0 ? `FOIL, then ${m("i^2 = -1")}: ${m(`(${a * c} - ${par(b * d)}) + (${a * d} + ${par(b * c)})i`)}.` : `Subtract real and imaginary parts separately.`], { mx: "complex", e: t === 0 ? `(${a} + ${b}*I)*(${c} + ${d}*I)` : `(${a} + ${b}*I) - (${c} + ${d}*I)` });
};
const complexRoots: Gen = (r) => {
  const p = r.int(-5, 5), qi = r.int(1, 6);
  const cs = [1, -2 * p, p * p + qi * qi];
  return draft(`${m(`${poly(cs)} = 0`)} has solutions ${m("p \\pm qi")}. Give ${m("p")} and ${m("q > 0")}.`, tuple([{ label: "p", tex: "p", ref: p }, { label: "q", tex: "q", ref: qi }]), `x = ${p}\\pm ${qi}i`,
    [`${m(`x = \\frac{${2 * p} \\pm \\sqrt{${4 * p * p} - ${4 * (p * p + qi * qi)}}}{2} = ${p} \\pm ${qi}i`)}; equivalently ${m(`${poly(cs)} = (x - ${par(p)} - ${qi}i)(x - ${par(p)} + ${qi}i)`)}.`], { mx: "complex-roots", e: polyPy(cs) });
};

// ── exponentials & logarithms ────────────────────────────────────────────────
const expSolve: Gen = (r) => {
  const a = r.int(2, 9), b = r.pick([2, 3, 10, Math.E]), c = r.pick([1, 2, 0.5, 3]), d = a * r.int(2, 30);
  const t = Math.log(d / a) / (c * Math.log(b));
  const bt = b === Math.E ? "e" : `${b}`;
  return draft(`Solve ${m(`${a}\\cdot ${bt}^{${c === 1 ? "" : c}t} = ${d}`)} for ${m("t")}. (Exact, e.g. ln(5)/ln(2), or 3 decimals.)`, approx(t, Math.max(3e-4, 0.0006 / Math.abs(t))), `t = \\frac{\\ln(${d / a})}{${c === 1 ? "" : c}\\ln ${bt}} \\approx ${t.toFixed(3)}`,
    [`Divide by ${a}: ${m(`${bt}^{${c}t} = ${d / a}`)}; take logs: ${m(`${c}t\\ln ${bt} = \\ln ${d / a}`)}.`], { mx: "exp-solve", a, b: b === Math.E ? "E" : `${b}`, c: `${c}`, d });
};
const expLogGraph = (kind: "exp" | "log"): Gen => (r) => {
  if (kind === "exp") {
    const a = r.nz(-5, 5), b = r.pick([2, 3, q(1, 2)].map(Q.of)), k = r.int(-6, 6);
    return draft(`For ${m(`y = ${a}\\cdot ${par(b.tex())}^x${sg(k)}`)}, give the ${m("y")}-intercept and the horizontal asymptote ${m("y = c")}.`, tuple([{ label: "y-intercept", tex: "y_0", ref: a + k }, { label: "asymptote c", tex: "c", ref: k }]), `y_0 = ${a + k},\\ y = ${k}`,
      [`At ${m("x = 0")}: ${m(`${a} + ${k}`)}. As ${b.value() > 1 ? "x \\to -\\infty" : "x \\to \\infty"} the exponential term → 0, leaving ${m(`y = ${k}`)}.`], { mx: "exp-graph", e: `${a}*(${qpy(b)})**x + ${k}`, grow: b.value() > 1 });
  }
  const b = r.pick([2, 3, 10]), h = r.int(-6, 6), k = r.int(-3, 3);
  const xi = h + b ** -k;
  require_(Number.isInteger(xi * 1000));
  return draft(`For ${m(`y = \\log_{${b}}(x${sg(-h)})${sg(k)}`)}, give the vertical asymptote ${m("x = c")} and the ${m("x")}-intercept.`, tuple([{ label: "asymptote c", tex: "c", ref: h }, { label: "x-intercept", tex: "x_0", ref: q(h).add(Q.of(k <= 0 ? b ** -k : 1).div(k > 0 ? b ** k : 1)) }]), `x = ${h},\\ x_0 = ${xi}`,
    [`The argument must be positive: asymptote ${m(`x = ${h}`)}. ${m("y = 0")}: ${m(`\\log_{${b}}(x${sg(-h)}) = ${-k}`)}, ${m(`x = ${h} + ${b}^{${-k}}`)}.`], { mx: "log-graph", b, h, k });
};
const cooling: Gen = (r) => {
  const Ta = r.int(15, 25), T0 = r.int(70, 95), k = r.pick([0.05, 0.08, 0.1, 0.12, 0.2]), tt = r.int(3, 30);
  const ask = r.int(0, 1);
  if (ask === 0) {
    const v = Ta + (T0 - Ta) * Math.exp(-k * tt);
    return draft(`Coffee cools as ${m(`T(t) = ${Ta} + ${T0 - Ta}e^{-${k}t}`)} (°C, minutes). What is its temperature after ${tt} minutes? (2 decimals)`, approx(v, tol2(v)), `${r2(v)}`, [`${m(`T(${tt}) = ${Ta} + ${T0 - Ta}e^{-${(k * tt).toFixed(2)}} \\approx ${r2(v)}`)}.`], { mx: "cool", Ta, D: T0 - Ta, k: `${k}`, t: tt });
  }
  const T1 = r.int(Ta + 5, T0 - 5);
  const v = -Math.log((T1 - Ta) / (T0 - Ta)) / k;
  return draft(`Coffee cools as ${m(`T(t) = ${Ta} + ${T0 - Ta}e^{-${k}t}`)} (°C, minutes). When does it reach ${T1} °C? (2 decimals)`, approx(v, tol2(v)), `${r2(v)}`, [`${m(`e^{-${k}t} = \\frac{${T1 - Ta}}{${T0 - Ta}}`)}, so ${m(`t = -\\frac{1}{${k}}\\ln\\frac{${T1 - Ta}}{${T0 - Ta}}`)}.`], { mx: "cool-time", Ta, D: T0 - Ta, k: `${k}`, T1 });
};
const compose: Gen = (r) => {
  const a = r.nz(-4, 4), b = r.int(-6, 6), c = r.nz(-3, 3), d = r.int(-5, 5);
  if (r.chance(0.5)) {
    const x = r.int(-4, 4), g = a * x + b, v = c * g * g + d;
    return draft(`${m(`f(x) = ${poly([c, 0, d])}`)}, ${m(`g(x) = ${poly([a, b])}`)}. Find ${m(`f(g(${x}))`)}.`, exact(v), `${v}`, [`${m(`g(${x}) = ${g}`)}, then ${m(`f(${g}) = ${v}`)}.`], { mx: "compose-at", f: `${c}*x**2 + ${d}`, g: `${a}*x + ${b}`, at: x });
  }
  return draft(`${m(`f(x) = ${poly([c, 0, d])}`)}, ${m(`g(x) = ${poly([a, b])}`)}. Find ${m("f(g(x))")}.`, { kind: "expression", ref: `${c}*(${a}*x + ${b})^2 + ${d}`, vars: ["x"], label: "f(g(x))" }, `${c}(${poly([a, b])})^2${sg(d)}`,
    [`Replace every ${m("x")} in ${m("f")} by ${m("g(x)")}.`], { mx: "compose", f: `${c}*x**2 + ${d}`, g: `${a}*x + ${b}` });
};
const logRules: Gen = (r) => {
  const t = r.int(0, 2), b = r.pick([2, 3, 5]);
  if (t === 0) {
    const m1 = r.int(-2, 5), m2 = r.int(-3, 4);
    const show = (e: number) => (e >= 0 ? int(b ** e) : `\\frac{1}{${b ** -e}}`);
    return draft(`Evaluate ${m(`\\log_{${b}} ${show(m1)} + \\log_{${b}} ${show(m2)}`)}.`, exact(m1 + m2), `${m1 + m2}`, [`${m(`\\log_{${b}} ${b}^k = k`)}: ${m(`${m1} + ${par(m2)} = ${m1 + m2}`)}.`], { mx: "expr", e: `log(${b}**(${m1}), ${b}) + log(${b}**(${m2}), ${b})` });
  }
  if (t === 1) {
    const b = r.pick([5, 7, 10]), p = r.int(0, 3), s = r.int(0, 2), k = r.int(-1, 1);
    require_(p + s > 0);
    const N = q(2 ** p * 3 ** s * (k > 0 ? b : 1), k < 0 ? b : 1);
    const ref = `${p}*u + ${s}*v + ${k}`;
    return draft(`Let ${m("u = \\log_{b} 2")} and ${m("v = \\log_{b} 3")} with ${m(`b = ${b}`)}. Write ${m(`\\log_{${b}} ${N.tex()}`)} in terms of ${m("u")} and ${m("v")}.`, { kind: "expression", ref, vars: ["u", "v"], label: "log" },
      `${p ? `${p === 1 ? "" : p}u` : ""}${s ? ` + ${s === 1 ? "" : s}v` : ""}${k ? (k > 0 ? " + 1" : " - 1") : ""}`, [`${m(`${N.tex()} = 2^{${p}}\\cdot 3^{${s}}\\cdot ${b}^{${k}}`)}; product and power rules.`], { mx: "log-uv", N: qpy(N), b, p, s, k });
  }
  const B = r.pick([4, 8, 9, 27, 16]), base = B === 9 || B === 27 ? 3 : 2, e1 = Math.round(Math.log(B) / Math.log(base)), e2 = r.int(1, 6);
  const v = q(e2, e1);
  return draft(`Evaluate ${m(`\\log_{${B}} ${base ** e2}`)} exactly (change of base).`, exact(v), v.tex(), [`${m(`\\frac{\\log_{${base}} ${base ** e2}}{\\log_{${base}} ${B}} = \\frac{${e2}}{${e1}}`)}.`], { mx: "expr", e: `log(${base ** e2}, ${B})` });
};
const logEq: Gen = (r) => {
  const b = r.pick([2, 3]), a = r.int(1, 6), k = r.int(1, 5);
  // x(x - a) = b^k with an integer root
  const D = a * a + 4 * b ** k, s = Math.round(Math.sqrt(D));
  require_(s * s === D && (a + s) % 2 === 0);
  const x1 = (a + s) / 2, x2 = (a - s) / 2;
  return draft(`Solve ${m(`\\log_{${b}} x + \\log_{${b}}(x - ${a}) = ${k}`)}. Give only true solutions.`, { kind: "roots", ref: [x1], label: "x" }, `x = ${x1}`,
    [`Product rule: ${m(`x(x - ${a}) = ${b}^{${k}} = ${b ** k}`)} ⇒ ${m(`x = ${x1}`)} or ${m(`x = ${x2}`)}.`, `${m(`x = ${x2}`)} is not in the domain (log of a negative).`], { mx: "log-eq", b, a, k });
};
const rationalGraph: Gen = (r) => {
  const a = r.int(-5, 5), b = r.int(-5, 5), c = r.int(-5, 5), L = r.nz(-3, 3);
  require_(new Set([a, b, c]).size === 3);
  const num = mulPoly([L, -L * a], [1, -b]), den = mulPoly([1, -a], [1, -c]);
  return draft(`For ${m(`f(x) = \\frac{${poly(num)}}{${poly(den)}}`)}, give the ${m("x")}-coordinate of the hole, the vertical asymptote ${m("x = v")}, and the horizontal asymptote ${m("y = h")}.`,
    tuple([{ label: "hole x", tex: "x_{hole}", ref: a }, { label: "v", tex: "v", ref: c }, { label: "h", tex: "h", ref: L }]), `\\text{hole at } x = ${a},\\ x = ${c},\\ y = ${L}`,
    [`${m(`f(x) = \\frac{${L === 1 ? "" : L === -1 ? "-" : L}(x${sg(-a)})(x${sg(-b)})}{(x${sg(-a)})(x${sg(-c)})}`)}: the common factor is a hole; ${m(`x${sg(-c)}`)} remains below; equal degrees ⇒ ratio of leading coefficients.`], { mx: "rat-graph", num: polyPy(num), den: polyPy(den) });
};
const complexConj: Gen = (r) => {
  if (r.chance(0.4)) {
    const [a, b] = r.pick(TRIPLES), k = r.int(1, 3), s1 = r.pick([1, -1]), s2 = r.pick([1, -1]);
    return draft(`Find ${m(`|${s1 * a * k} ${s2 > 0 ? "+" : "-"} ${b * k}i|`)}.`, exact(Math.hypot(a * k, b * k)), `${Math.hypot(a * k, b * k)}`, [`${m(`|a + bi| = \\sqrt{a^2 + b^2} = \\sqrt{(z)(\\bar z)}`)}.`], { mx: "complex", e: `Abs(${s1 * a * k} + ${s2 * b * k}*I)` });
  }
  const re = q(r.int(-6, 6), r.pick([1, 2, 5])), im = q(r.int(-6, 6), r.pick([1, 2, 5])), c = r.int(-4, 4), d = r.nz(-4, 4);
  const num = [re.mul(c).sub(im.mul(d)), re.mul(d).add(im.mul(c))];
  require_(num.every((x) => x.isInt()));
  return draft(`Write ${m(`\\frac{${num[0].n}${num[1].n < 0 ? "-" : "+"}${Math.abs(num[1].n)}i}{${c}${d < 0 ? "-" : "+"}${Math.abs(d)}i}`)} in the form ${m("a + bi")}.`, tuple([{ label: "a", tex: "a", ref: re }, { label: "b", tex: "b", ref: im }]), `${re.tex()}${sg(im, "i")}`,
    [`Multiply top and bottom by the conjugate ${m(`${c}${d < 0 ? "+" : "-"}${Math.abs(d)}i`)}; the denominator becomes ${m(`${c * c + d * d}`)}.`], { mx: "complex", e: `(${num[0].n} + ${num[1].n}*I)/(${c} + ${d}*I)` });
};
const complexDist: Gen = (r) => {
  const [a, b] = r.pick(TRIPLES), x1 = r.int(-6, 6), y1 = r.int(-6, 6), s = r.pick([1, -1]);
  const x2 = x1 + 2 * a * s, y2 = y1 + 2 * b * r.pick([1, -1]);
  return draft(`For ${m(`z_1 = ${x1}${y1 < 0 ? "-" : "+"}${Math.abs(y1)}i`)} and ${m(`z_2 = ${x2}${y2 < 0 ? "-" : "+"}${Math.abs(y2)}i`)}, find the distance ${m("|z_1 - z_2|")} and the midpoint ${m("a + bi")}.`,
    tuple([{ label: "distance", tex: "d", ref: 2 * Math.hypot(a, b) }, { label: "a", tex: "a", ref: (x1 + x2) / 2 }, { label: "b", tex: "b", ref: (y1 + y2) / 2 }]), `d = ${2 * Math.hypot(a, b)},\\ ${(x1 + x2) / 2}${sg((y1 + y2) / 2, "i")}`,
    [`Distance = modulus of the difference; midpoint = average of the endpoints.`], { mx: "complex-dist", z1: [x1, y1], z2: [x2, y2] });
};

// ── vectors & matrices ──────────────────────────────────────────────────────
const vectorOps: Gen = (r) => {
  const t = r.int(0, 3), u = [r.int(-8, 8), r.int(-8, 8)], v = [r.int(-8, 8), r.int(-8, 8)], k = r.nz(-4, 4);
  if (t === 0) {
    const P = [r.int(-9, 9), r.int(-9, 9)];
    return draft(`A vector starts at ${m(`(${P.join(", ")})`)} and ends at ${m(`(${P[0] + u[0]}, ${P[1] + u[1]})`)}. Find its components.`, tuple([{ label: "x", tex: "v_x", ref: u[0] }, { label: "y", tex: "v_y", ref: u[1] }]), `\\langle ${u.join(", ")}\\rangle`, [`Terminal minus initial.`], { mx: "vec", op: "comp", P, Qp: [P[0] + u[0], P[1] + u[1]] });
  }
  if (t === 3) {
    const [a, b] = r.pick(TRIPLES);
    return draft(`${m(`\\mathbf v = \\langle ${a}, ${-b}\\rangle`)}. Find ${m(`\\|${k}\\mathbf v\\|`)}.`, exact(Math.abs(k) * Math.hypot(a, b)), `${Math.abs(k) * Math.hypot(a, b)}`, [`${m(`\\|c\\mathbf v\\| = |c|\\,\\|\\mathbf v\\| = ${Math.abs(k)} \\cdot ${Math.hypot(a, b)}`)}.`], { mx: "vec", op: "norm", u: [a, -b], k });
  }
  const res = t === 1 ? [u[0] + k * v[0], u[1] + k * v[1]] : [k * u[0] - v[0], k * u[1] - v[1]];
  return draft(`${m(`\\mathbf u = \\langle ${u.join(", ")}\\rangle,\\ \\mathbf v = \\langle ${v.join(", ")}\\rangle`)}. Find ${m(t === 1 ? `\\mathbf u ${k < 0 ? "-" : "+"} ${Math.abs(k) === 1 ? "" : Math.abs(k)}\\mathbf v` : `${k === 1 ? "" : k === -1 ? "-" : k}\\mathbf u - \\mathbf v`)}.`, tuple([{ label: "x", tex: "x", ref: res[0] }, { label: "y", tex: "y", ref: res[1] }]), `\\langle ${res.join(", ")}\\rangle`, [`Componentwise.`], { mx: "vec", op: t === 1 ? "u+kv" : "ku-v", u, v, k });
};
const vectorPolar: Gen = (r) => {
  const m1 = r.int(5, 20), m2 = r.int(5, 20), a1 = r.int(0, 35) * 10, a2 = r.int(0, 35) * 10;
  const x = m1 * Math.cos(a1 * RAD) + m2 * Math.cos(a2 * RAD), y = m1 * Math.sin(a1 * RAD) + m2 * Math.sin(a2 * RAD);
  const mag = Math.hypot(x, y);
  let dir = (Math.atan2(y, x) / RAD + 360) % 360;
  require_(mag > 2 && dir > 5 && dir < 355);
  return draft(`Add ${m(`\\mathbf u`)} (magnitude ${m1}, direction ${deg(a1)}) and ${m(`\\mathbf v`)} (magnitude ${m2}, direction ${deg(a2)}); directions are measured counterclockwise from the positive x-axis. Give the magnitude and direction (0–360°) of the sum, to 2 decimals.`,
    tuple([{ label: "magnitude", tex: "\\|\\mathbf u + \\mathbf v\\|", ref: mag, mode: "number" }, { label: "direction°", tex: "\\theta", ref: dir, mode: "number" }]), `${r2(mag)},\\ ${r2(dir)}^\\circ`,
    [`Components: ${m(`(${x.toFixed(3)}, ${y.toFixed(3)})`)}; magnitude ${m("\\sqrt{x^2 + y^2}")}, direction from ${m("\\operatorname{atan2}(y, x)")}.`], { mx: "vec-polar", m1, a1, m2, a2 });
};
const matrixOps: Gen = (r) => {
  const A = [[r.int(-5, 5), r.int(-5, 5)], [r.int(-5, 5), r.int(-5, 5)]], B = [[r.int(-5, 5), r.int(-5, 5)], [r.int(-5, 5), r.int(-5, 5)]], k = r.nz(-4, 4), t = r.int(0, 2);
  const pm = (M: number[][]) => `\\begin{bmatrix} ${M.map((row) => row.join(" & ")).join(" \\\\ ")} \\end{bmatrix}`;
  if (t === 2) {
    const v = [r.int(-5, 5), r.int(-5, 5)];
    const res = A.map((row) => row[0] * v[0] + row[1] * v[1]);
    return draft(`Compute ${m(`${pm(A)}${pm([[v[0]], [v[1]]])}`)}.`, tuple(res.map((x, i) => ({ label: `entry ${i + 1}`, tex: `y_${i + 1}`, ref: x }))), pm([[res[0]], [res[1]]]), [`Row · column for each entry.`], { mx: "mat", op: "Av", A, v });
  }
  const res = t === 0 ? [0, 1].map((i) => [0, 1].map((j) => A[i][0] * B[0][j] + A[i][1] * B[1][j])) : A.map((row, i) => row.map((x, j) => k * x + B[i][j]));
  return draft(`Compute ${m(t === 0 ? `${pm(A)}${pm(B)}` : `${k}${pm(A)} + ${pm(B)}`)}. Give the entries row by row.`, tuple(res.flat().map((x, i) => ({ label: `a${[11, 12, 21, 22][i]}`, tex: `a_{${[11, 12, 21, 22][i]}}`, ref: x }))), pm(res),
    [t === 0 ? `Entry (i, j) = row i of the first · column j of the second.` : `Scale every entry by ${k}, then add entrywise.`], { mx: "mat", op: t === 0 ? "AB" : "kA+B", A, B, k });
};
const matrixDet: Gen = (r) => {
  const A = [[r.int(-6, 6), r.int(-6, 6)], [r.int(-6, 6), r.int(-6, 6)]];
  const D = A[0][0] * A[1][1] - A[0][1] * A[1][0];
  const pm = `\\begin{bmatrix} ${A.map((row) => row.join(" & ")).join(" \\\\ ")} \\end{bmatrix}`;
  if (r.chance(0.5)) {
    const area = r.int(1, 9);
    return draft(`The transformation ${m(`T(\\mathbf x) = ${pm}\\mathbf x`)} is applied to a region of area ${area}. What is the area of the image?`, exact(Math.abs(D) * area), `${Math.abs(D) * area}`, [`Areas scale by ${m(`|\\det A| = ${Math.abs(D)}`)}.`], { mx: "mat", op: "area", A, area });
  }
  return draft(`Is ${m(`${pm}`)} invertible?`, choice(["Invertible", "Not invertible"], D !== 0 ? "Invertible" : "Not invertible"), `\\det = ${D}`, [`${m(`\\det = ${D}`)}: invertible exactly when nonzero.`], { mx: "mat", op: "inv?", A });
};

// ── geometry ─────────────────────────────────────────────────────────────────
const TR = ["reflect over the x-axis", "reflect over the y-axis", "reflect over the line y = x", "rotate 90° counterclockwise about the origin", "rotate 180° about the origin", "rotate 270° counterclockwise about the origin", "translate"];
const geoTransform: Gen = (r) => {
  const x = r.nz(-7, 7), y = r.nz(-7, 7), t1 = r.int(0, 6), t2 = r.int(0, 5), dx = r.nz(-5, 5), dy = r.nz(-5, 5);
  const ap = (t: number, [a, b]: number[]) => [[a, -b], [-a, b], [b, a], [-b, a], [-a, -b], [b, -a], [a + dx, b + dy]][t];
  const img = ap(t2, ap(t1, [x, y]));
  const nm = (t: number) => (t === 6 ? `translate by ${m(`\\langle ${dx}, ${dy}\\rangle`)}` : TR[t]);
  return draft(`Point ${m(`(${x}, ${y})`)}: first ${nm(t1)}, then ${nm(t2)}. Where does it end up?`, tuple([{ label: "x", tex: "x'", ref: img[0] }, { label: "y", tex: "y'", ref: img[1] }]), `(${img.join(", ")})`,
    [`After the first: ${m(`(${ap(t1, [x, y]).join(", ")})`)}; after the second: ${m(`(${img.join(", ")})`)}.`], { mx: "geo-transform", x, y, ts: [t1, t2], dx, dy });
};
const symmetry: Gen = (r) => {
  const n = r.int(3, 12);
  return r.chance(0.5)
    ? draft(`What is the smallest positive rotation (in degrees) that carries a regular ${n}-gon onto itself?`, exact(q(360, n)), `${q(360, n).tex()}^\\circ`, [`${n} equal central angles: ${m(`360/${n}`)}.`], { mx: "rot-sym", n, ask: "angle" })
    : draft(`How many lines of reflection symmetry does a regular ${n}-gon have?`, exact(n), `${n}`, [`${n % 2 ? "Each line passes through a vertex and the midpoint of the opposite side" : "Half pass through opposite vertices, half through midpoints of opposite sides"}: ${n}.`], { mx: "rot-sym", n, ask: "lines" });
};
const CRIT = ["SSS", "SAS", "ASA", "AAS", "Not enough information"];
const congruence: Gen = (r) => {
  // facts among sides AB, BC, CA and angles A, B, C (3 facts)
  const facts = shuffle(["AB", "BC", "CA", "A", "B", "C"], () => r.next()).slice(0, 3).sort();
  const sides = facts.filter((f) => f.length === 2), angs = facts.filter((f) => f.length === 1);
  let ans = "Not enough information";
  if (sides.length === 3) ans = "SSS";
  else if (sides.length === 2) ans = angs[0] && sides.every((s) => s.includes(angs[0])) ? "SAS" : "Not enough information";
  else if (sides.length === 1) ans = angs.every((a) => sides[0].includes(a)) ? "ASA" : "AAS";
  const map: Record<string, string> = { A: "D", B: "E", C: "F" };
  const tx = (f: string) => (f.length === 2 ? `\\overline{${f}} \\cong \\overline{${f.split("").map((c) => map[c]).join("")}}` : `\\angle ${f} \\cong \\angle ${map[f]}`);
  return draft(`In triangles ${m("ABC")} and ${m("DEF")}: ${facts.map((f) => m(tx(f))).join(", ")}. Which criterion proves ${m("\\triangle ABC \\cong \\triangle DEF")}?`, choice(CRIT, ans), `\\text{${ans}}`,
    [ans === "Not enough information" ? `${sides.length === 2 ? "The angle is not between the two sides (SSA)" : "Three angles fix only the shape (AAA)"}: not a congruence criterion.` : `The given parts form ${ans}.`], { mx: "congruence", facts });
};
const PAIRS: [string, boolean][] = [["corresponding", true], ["alternate interior", true], ["alternate exterior", true], ["same-side interior", false], ["vertical", true], ["a linear pair", false]];
const anglesLines: Gen = (r) => {
  const [nm, eq] = r.pick(PAIRS), x = r.int(5, 30), a = r.int(2, 6), b = r.int(-20, 30), c = r.int(1, 5);
  const A = a * x + b;
  require_(A > 10 && A < 170 && a !== c);
  const B = eq ? A : 180 - A, d = B - c * x;
  return draft(`${nm === "vertical" || nm === "a linear pair" ? "Two angles" : "Parallel lines are cut by a transversal; two angles"} are ${nm}${nm.startsWith("a ") ? "" : " angles"}: ${m(`(${cx(a, "x")}${sg(b)})^\\circ`)} and ${m(`(${cx(c, "x")}${sg(d)})^\\circ`)}. Find ${m("x")}.`, exact(x), `x = ${x}`,
    [`${nm[0].toUpperCase() + nm.slice(1)} angles are ${eq ? "congruent" : "supplementary"}: ${m(eq ? `${cx(a, "x")}${sg(b)} = ${cx(c, "x")}${sg(d)}` : `${cx(a + c, "x")}${sg(b + d)} = 180`)}.`], { mx: "angle-pair", pair: nm, e1: `${a}*x + ${b}`, e2: `${c}*x + ${d}` });
};
const triangleThm: Gen = (r) => {
  const t = r.int(0, 2);
  if (t === 0) {
    const v = 2 * r.int(10, 80);
    return draft(`An isosceles triangle has vertex angle ${deg(v)}. What is each base angle in degrees?`, exact((180 - v) / 2), `${(180 - v) / 2}^\\circ`, [`Base angles are congruent and the three add to 180°.`], { mx: "iso-base", v });
  }
  if (t === 1) {
    const s = r.int(4, 30), x = r.int(-5, 5), y = r.int(2, 9);
    return draft(`In triangle ${m("ABC")}, ${m("M")} and ${m("N")} are the midpoints of ${m("\\overline{AB}")} and ${m("\\overline{AC}")}, and ${m(`BC = ${s}`)}. Find ${m("MN")}.`, exact(q(s, 2)), q(s, 2).tex(), [`Midsegment theorem: ${m("MN \\parallel BC")} and ${m("MN = \\tfrac12 BC")}.`], { mx: "midsegment", s, apex: [x, y] });
  }
  const a = r.int(2, 5), b = r.int(-10, 20), c = r.int(1, 4), d = r.int(0, 30), x = r.int(5, 20);
  const third = 180 - (a * x + b) - (c * x + d);
  require_(a * x + b > 5 && c * x + d > 5 && third > 5);
  return draft(`A triangle has angles ${m(`(${cx(a, "x")}${sg(b)})^\\circ`)}, ${m(`(${cx(c, "x")}${sg(d)})^\\circ`)} and ${deg(third)}. Find ${m("x")}.`, exact(x), `x = ${x}`, [`Angle sum: ${m(`${cx(a + c, "x")}${sg(b + d + third)} = 180`)}.`], { mx: "solve", eq: `${a}*x + ${b} + ${c}*x + ${d} + ${third} - 180` });
};
const parallelogram: Gen = (r) => {
  const x = r.int(2, 15);
  if (r.chance(0.5)) {
    const a = r.int(2, 8), b = r.int(-10, 20), A = a * x + b;
    require_(A > 20 && A < 160);
    return draft(`In parallelogram ${m("ABCD")}, ${m(`\\angle A = (${cx(a, "x")}${sg(b)})^\\circ`)} and ${m(`\\angle B = ${180 - A}^\\circ`)}. Find ${m("x")}.`, exact(x), `x = ${x}`, [`Consecutive angles are supplementary.`], { mx: "angle-pair", pair: "consecutive (parallelogram)", e1: `${a}*x + ${b}`, e2: `${180 - A}` });
  }
  const a = r.int(2, 6), b = r.int(-5, 10), c = r.int(1, 5), d = (a - c) * x + b;
  require_(a !== c && a * x + b > 0);
  return draft(`The diagonals of parallelogram ${m("ABCD")} meet at ${m("E")}, with ${m(`AE = ${cx(a, "x")}${sg(b)}`)} and ${m(`EC = ${cx(c, "x")}${sg(d)}`)}. Find ${m("AC")}.`, exact(2 * (a * x + b)), `${2 * (a * x + b)}`, [`Diagonals bisect each other: ${m(`${cx(a, "x")}${sg(b)} = ${cx(c, "x")}${sg(d)}`)} ⇒ ${m(`x = ${x}`)}; ${m(`AC = 2\\,AE`)}.`], { mx: "diag-bisect", e1: `${a}*x + ${b}`, e2: `${c}*x + ${d}` });
};
const dilation: Gen = (r) => {
  const cx_ = r.int(-4, 4), cy = r.int(-4, 4), k = r.pick([2, 3, q(1, 2), q(3, 2), -1].map(Q.of)), dx = r.int(-6, 6) * 2, dy = r.int(-6, 6) * 2;
  if (r.chance(0.3)) {
    const L = r.int(2, 20);
    return draft(`A segment of length ${L} is dilated by scale factor ${m(k.tex())}. How long is the image?`, exact(Q.of(L).mul(k.n < 0 ? k.neg() : k)), Q.of(L).mul(k.n < 0 ? k.neg() : k).tex(), [`A dilation multiplies every length by ${m(`|k|`)}.`], { mx: "dil-len", L, k: qpy(k) });
  }
  const img = [k.mul(dx).add(cx_), k.mul(dy).add(cy)];
  return draft(`Dilate ${m(`(${cx_ + dx}, ${cy + dy})`)} by scale factor ${m(k.tex())} centered at ${m(`(${cx_}, ${cy})`)}.`, tuple([{ label: "x", tex: "x'", ref: img[0] }, { label: "y", tex: "y'", ref: img[1] }]), `(${img[0].tex()}, ${img[1].tex()})`,
    [`From the center: ${m(`\\langle ${dx}, ${dy}\\rangle \\to ${k.tex()}\\langle ${dx}, ${dy}\\rangle`)}, then add the center back.`], { mx: "dilate", P: [cx_ + dx, cy + dy], C: [cx_, cy], k: qpy(k) });
};
const similar: Gen = (r) => {
  const s = [r.int(3, 15), r.int(3, 15), r.int(3, 15)], k = q(r.int(2, 9), r.pick([1, 2, 3]));
  require_(s[0] + s[1] > s[2] && s[1] + s[2] > s[0] && s[0] + s[2] > s[1] && k.value() !== 1);
  const t = s.map((x) => k.mul(x));
  return draft(`${m("\\triangle ABC \\sim \\triangle DEF")} with ${m(`AB = ${s[0]},\\ BC = ${s[1]},\\ CA = ${s[2]}`)} and ${m(`DE = ${t[0].tex()}`)}. Find ${m("EF")}.`, exact(t[1]), t[1].tex(), [`Scale factor ${m(`DE/AB = ${k.tex()}`)}; ${m(`EF = ${k.tex()} \\cdot ${s[1]}`)}.`], { mx: "similar", s, DE: qpy(t[0]) });
};
const sideSplitter: Gen = (r) => {
  const ad = r.int(2, 12), db = r.int(2, 12), ae = r.int(2, 15);
  return draft(`In ${m("\\triangle ABC")}, ${m("D")} is on ${m("\\overline{AB}")} and ${m("E")} on ${m("\\overline{AC}")} with ${m("\\overline{DE} \\parallel \\overline{BC}")}. ${m(`AD = ${ad},\\ DB = ${db},\\ AE = ${ae}`)}. Find ${m("EC")}.`, exact(q(ae * db, ad)), q(ae * db, ad).tex(), [`Side-splitter theorem: ${m("\\frac{AD}{DB} = \\frac{AE}{EC}")}, so ${m(`EC = \\frac{${ae}\\cdot ${db}}{${ad}}`)}.`], { mx: "splitter", ad, db, ae });
};
const rightTrig: Gen = (r) => {
  const t = r.int(0, 1), A = r.int(15, 75), h = r.int(5, 40);
  if (t === 0) {
    const fn = r.pick(["opp", "adj"]);
    const v = fn === "opp" ? h * Math.sin(A * RAD) : h * Math.cos(A * RAD);
    return draft(`A right triangle has hypotenuse ${h} and an acute angle of ${deg(A)}. Find the side ${fn === "opp" ? "opposite" : "adjacent to"} that angle (2 decimals).`, approx(v, tol2(v)), r2(v), [`${m(`${fn === "opp" ? "\\sin" : "\\cos"} ${A}^\\circ = \\frac{${fn === "opp" ? "\\text{opp}" : "\\text{adj}"}}{${h}}`)}.`], { mx: "right-side", h, A, fn });
  }
  const a = r.int(3, 20), b = r.int(3, 20);
  const v = Math.atan(a / b) / RAD;
  return draft(`A ramp rises ${a} ft over a horizontal run of ${b} ft. What angle does it make with the ground, in degrees (2 decimals)?`, approx(v, tol2(v)), r2(v), [`${m(`\\tan\\theta = \\frac{${a}}{${b}}`)}, ${m(`\\theta = \\tan^{-1}(${a}/${b})`)}.`], { mx: "right-angle", a, b });
};
const trigRatio: Gen = (r) => {
  const [a, b, c] = r.pick(TRIPLES), fn = r.pick(["sin", "cos", "tan"]);
  if (r.chance(0.35)) {
    const th = r.int(5, 85);
    return draft(`In a right triangle, ${m(`\\sin ${th}^\\circ = \\cos x^\\circ`)} with ${m("0 < x < 90")}. Find ${m("x")}.`, exact(90 - th), `${90 - th}`, [`The acute angles of a right triangle are complementary, and the sine of one is the cosine of the other.`], { mx: "cofunction", th });
  }
  const v = fn === "sin" ? q(a, c) : fn === "cos" ? q(b, c) : q(a, b);
  return draft(`A right triangle has legs ${a} and ${b} and hypotenuse ${c}. Angle ${m("\\theta")} is opposite the leg of length ${a}. Find ${m(`\\${fn}\\theta`)} as a fraction.`, exact(v), v.tex(), [`SOH-CAH-TOA: ${m(`\\${fn}\\theta = ${v.tex()}`)}.`], { mx: "trig-ratio", legs: [a, b], fn });
};
const density: Gen = (r) => {
  if (r.chance(0.5)) {
    const pop = r.int(20, 900) * 100, area = r.pick([4, 5, 8, 10, 20, 25, 40, 50]);
    return draft(`A county of ${area} square miles has ${pop.toLocaleString("en-US")} people. What is its population density in people per square mile?`, exact(q(pop, area)), q(pop, area).tex(), [`Density = people ÷ area.`], { mx: "expr", e: `${pop}/${area}` });
  }
  const rad = r.int(1, 6), h = r.int(2, 20), rho = r.pick([q(1), q(5, 2), q(27, 10), q(79, 10)]);
  const v = rho.mul(rad * rad * h).value() * Math.PI;
  return draft(`A solid cylinder (radius ${rad} cm, height ${h} cm) has density ${m(`${rho.value()}\\ \\text{g/cm}^3`)}. What is its mass in grams? (exact with π, or 2 decimals)`, approx(`${rho.value() * rad * rad * h}*pi`, tol2(v)), `${r2(v)}\\ \\text{g}`, [`Mass = density × volume = ${m(`${rho.value()} \\cdot \\pi (${rad})^2 (${h})`)}.`], { mx: "cyl-mass", rad, h, rho: qpy(rho) });
};
const areaSin: Gen = (r) => {
  const a = r.int(3, 20), b = r.int(3, 20), C = r.pick([30, 45, 60, 90, 120, 135, 150, r.int(20, 160)]);
  const v = 0.5 * a * b * Math.sin(C * RAD);
  return draft(`Find the area of a triangle with sides ${a} and ${b} and included angle ${deg(C)} (exact or 2 decimals).`, approx(v, tol2(v)), r2(v), [`${m(`A = \\tfrac12 ab\\sin C = \\tfrac12(${a})(${b})\\sin ${C}^\\circ`)}.`], { mx: "area-sas", a, b, C });
};
const lawSines: Gen = (r) => {
  const A = r.int(25, 80), B = r.int(25, 80), a = r.int(5, 30);
  require_(A + B < 160);
  const b = (a * Math.sin(B * RAD)) / Math.sin(A * RAD);
  return draft(`In ${m("\\triangle ABC")}, ${m(`A = ${A}^\\circ,\\ B = ${B}^\\circ,\\ a = ${a}`)}. Find ${m("b")} (2 decimals).`, approx(b, tol2(b)), r2(b), [`${m(`\\frac{a}{\\sin A} = \\frac{b}{\\sin B}`)} ⇒ ${m(`b = \\frac{${a}\\sin ${B}^\\circ}{\\sin ${A}^\\circ}`)}.`], { mx: "law-sines", A, B, a });
};
const lawCosines: Gen = (r) => {
  const b = r.int(3, 25), c = r.int(3, 25), A = r.int(20, 150);
  const a = Math.sqrt(b * b + c * c - 2 * b * c * Math.cos(A * RAD));
  return draft(`In ${m("\\triangle ABC")}, ${m(`b = ${b},\\ c = ${c},\\ A = ${A}^\\circ`)}. Find ${m("a")} (2 decimals).`, approx(a, tol2(a)), r2(a), [`${m(`a^2 = b^2 + c^2 - 2bc\\cos A`)}.`], { mx: "law-cosines", b, c, A });
};
const SOLIDS = ["cylinder", "cone", "sphere", "hemisphere", "square pyramid", "cone on a cylinder"];
const volume: Gen = (r) => {
  const t = r.int(0, 5), rad = r.int(1, 9), h = r.int(1, 12), s = r.int(2, 12);
  const v = [q(rad * rad * h), q(rad * rad * h, 3), q(4 * rad ** 3, 3), q(2 * rad ** 3, 3), q(s * s * h, 3), q(rad * rad * h).add(q(rad * rad * h, 3))][t];
  const isPi = t !== 4;
  const desc = [`a cylinder with radius ${rad} and height ${h}`, `a cone with radius ${rad} and height ${h}`, `a sphere of radius ${rad}`, `a hemisphere of radius ${rad}`, `a square pyramid with base edge ${s} and height ${h}`, `a cone (radius ${rad}, height ${h}) sitting on a cylinder of the same radius and height`][t];
  const val = v.value() * (isPi ? Math.PI : 1);
  return draft(`Find the volume of ${desc}${isPi ? " — exact in terms of π (e.g. 12pi) or 2 decimals" : ""}.`, isPi ? approx(`(${qref(v)})*pi`, tol2(val)) : exact(v), isPi ? `${qtex(v)}\\pi` : qtex(v),
    [[`${m("V = \\pi r^2 h")}`, `${m("V = \\tfrac13\\pi r^2 h")}`, `${m("V = \\tfrac43\\pi r^3")}`, `Half a sphere: ${m("\\tfrac23\\pi r^3")}`, `${m("V = \\tfrac13 Bh")}`, `Add: ${m("\\pi r^2 h + \\tfrac13\\pi r^2 h")}`][t] + `.`], { mx: "volume", t: SOLIDS[t], rad, h, s });
};
const CROSS: [string, string, string][] = [
  ["a cylinder", "perpendicular to its axis", "Circle"], ["a cylinder", "parallel to its axis (through the axis)", "Rectangle"], ["a cone", "perpendicular to its axis", "Circle"], ["a cone", "through its apex, along the axis", "Triangle"],
  ["a cube", "parallel to a face", "Square"], ["a square pyramid", "parallel to the base", "Square"], ["a square pyramid", "perpendicular to the base through the apex", "Triangle"], ["a sphere", "through any plane that cuts it", "Circle"],
];
const crossSection: Gen = (r) => {
  if (r.chance(0.35)) {
    const [shape, axis, solid] = r.pick([["rectangle", "one of its sides", "Cylinder"], ["right triangle", "one of its legs", "Cone"], ["semicircle", "its diameter", "Sphere"]]);
    return draft(`Rotating a ${shape} about ${axis} generates which solid?`, choice(["Cylinder", "Cone", "Sphere", "Prism"], solid), `\\text{${solid}}`, [`Each point traces a circle around the axis.`], { mx: "rotate-solid", shape });
  }
  const [solid, cut, ans] = r.pick(CROSS);
  return draft(`What shape is the cross-section of ${solid} cut ${cut}?`, choice(["Circle", "Rectangle", "Triangle", "Square"], ans), `\\text{${ans}}`, [`Picture the cut face.`], { mx: "cross", solid, cut });
};
const parallelPerp: Gen = (r) => {
  const m1 = q(r.nz(-5, 5), r.pick([1, 2, 3])), b1 = r.int(-6, 6), x0 = r.int(-6, 6) * m1.d, y0 = r.int(-8, 8), perp = r.chance(0.5);
  const mm = perp ? q(-m1.d, m1.n) : m1;
  const b = q(y0).sub(mm.mul(x0));
  require_(b.isInt() || b.d <= 3);
  return draft(`Find the line through ${m(`(${x0}, ${y0})`)} ${perp ? "perpendicular" : "parallel"} to ${m(`y = ${poly([m1, b1])}`)}. Give ${m("m")} and ${m("b")} in ${m("y = mx + b")}.`, tuple([{ label: "m", tex: "m", ref: mm }, { label: "b", tex: "b", ref: b }]), `y = ${poly([mm, b])}`,
    [`${perp ? `Perpendicular slopes multiply to −1: ${m(`m = ${mm.tex()}`)}` : `Parallel lines share the slope ${m(mm.tex())}`}; ${m(`b = y_0 - m x_0 = ${b.tex()}`)}.`], { mx: "par-perp", m1: qpy(m1), b1, P: [x0, y0], perp });
};
const partition: Gen = (r) => {
  const A = [r.int(-8, 8), r.int(-8, 8)], a = r.int(1, 4), b = r.int(1, 4), d = [r.int(-4, 4) * (a + b), r.int(-4, 4) * (a + b)];
  require_(d[0] !== 0 || d[1] !== 0);
  const P = [A[0] + (d[0] * a) / (a + b), A[1] + (d[1] * a) / (a + b)];
  return draft(`Find the point ${m("P")} on ${m("\\overline{AB}")} with ${m(`A(${A.join(", ")})`)} and ${m(`B(${A[0] + d[0]}, ${A[1] + d[1]})`)} such that ${m(`AP : PB = ${a} : ${b}`)}.`, tuple([{ label: "x", tex: "x", ref: P[0] }, { label: "y", tex: "y", ref: P[1] }]), `(${P.join(", ")})`,
    [`${m(`P = A + \\frac{${a}}{${a + b}}(B - A)`)}.`], { mx: "partition", A, B: [A[0] + d[0], A[1] + d[1]], a, b });
};
const coordPerim: Gen = (r) => {
  const [a, b] = r.pick(TRIPLES), x0 = r.int(-5, 5), y0 = r.int(-5, 5), k = r.int(1, 2), sx = r.pick([1, -1]), sy = r.pick([1, -1]);
  // legs along grid lines, so every side is a whole number
  const V = [[x0, y0], [x0 + sx * a * k, y0], [x0, y0 + sy * b * k]];
  const per = a * k + b * k + Math.hypot(a * k, b * k);
  const ask = r.chance(0.5);
  return draft(`Triangle with vertices ${m(V.map((p) => `(${p.join(", ")})`).join(",\\ "))}: find its ${ask ? "perimeter" : "area"}.`, exact(ask ? per : q(a * b * k * k, 2)), ask ? `${per}` : q(a * b * k * k, 2).tex(), [ask ? `Two legs along grid lines; hypotenuse by the distance formula: ${Math.hypot(a * k, b * k)}.` : `Right triangle: ${m("\\tfrac12 \\cdot \\text{leg} \\cdot \\text{leg}")}.`], { mx: "polygon", V, ask: ask ? "perimeter" : "area" });
};
const QUADS = ["Rectangle", "Parallelogram (not a rectangle)", "Not a parallelogram"];
const coordProof: Gen = (r) => {
  const A = [r.int(-5, 5), r.int(-5, 5)], u = [r.nz(-4, 4), r.int(-4, 4)], t = r.int(0, 2);
  const sc = r.pick([1, 2]), v = t === 0 ? [-u[1] * sc, u[0] * sc] : [r.int(-4, 4), r.nz(-4, 4)];
  require_(u[0] * v[1] - u[1] * v[0] !== 0 && (t === 0 || u[0] * v[0] + u[1] * v[1] !== 0));
  const B = [A[0] + u[0], A[1] + u[1]], D = [A[0] + v[0], A[1] + v[1]];
  const C = t === 2 ? [B[0] + v[0] + r.nz(-2, 2), B[1] + v[1]] : [B[0] + v[0], B[1] + v[1]];
  return draft(`Classify quadrilateral ${m("ABCD")} with ${m(`A(${A}),\\ B(${B}),\\ C(${C}),\\ D(${D})`.replace(/,(?=-?\d)/g, ", "))}.`, choice(QUADS, QUADS[t]), `\\text{${QUADS[t]}}`,
    [`Parallelogram ⇔ the diagonals share a midpoint; a parallelogram is a rectangle ⇔ its diagonals are equal (or adjacent sides have slopes with product −1).`], { mx: "quad-class", V: [A, B, C, D] });
};
const parabola: Gen = (r) => {
  const h = r.int(-5, 5), k = r.int(-5, 5), p = r.pick([q(1, 4), q(1, 2), q(1), q(2), q(-1, 4), q(-1), q(3, 4)].map(Q.of));
  const a = q(1).div(p.mul(4));
  return draft(`A parabola has focus ${m(`(${h}, ${q(k).add(p).tex()})`)} and directrix ${m(`y = ${q(k).sub(p).tex()}`)}. Write it as ${m("y = a(x - h)^2 + k")}: give ${m("a, h, k")}.`, tuple([{ label: "a", tex: "a", ref: a }, { label: "h", tex: "h", ref: h }, { label: "k", tex: "k", ref: k }]), `y = ${a.tex()}(x${sg(-h)})^2${sg(k)}`,
    [`The vertex is halfway between focus and directrix; ${m(`p = ${p.tex()}`)} (focus above ⇒ opens up), ${m("a = \\frac{1}{4p}")}.`], { mx: "parabola", F: [h, qpy(q(k).add(p))], dy: qpy(q(k).sub(p)) });
};
const inscribed: Gen = (r) => {
  const t = r.int(0, 2), arc = 2 * r.int(10, 170);
  if (t === 0) return draft(`An inscribed angle intercepts an arc of ${deg(arc)}. What is the angle's measure?`, exact(arc / 2), `${arc / 2}^\\circ`, [`Inscribed angle = half the intercepted arc.`], { mx: "inscribed", arc, ask: "inscribed" });
  if (t === 1) return draft(`A central angle measures ${deg(arc / 2)}. What does an inscribed angle intercepting the same arc measure?`, exact(arc / 4), `${arc / 4}^\\circ`, [`The central angle equals the arc; the inscribed angle is half of it.`], { mx: "inscribed", arc: arc / 2, ask: "inscribed" });
  const k = r.int(20, 80);
  return draft(`${m("\\overline{AB}")} is a diameter and ${m("C")} is on the circle with ${m(`\\angle CAB = ${k}^\\circ`)}. Find ${m("\\angle CBA")}.`, exact(90 - k), `${90 - k}^\\circ`, [`An angle inscribed in a semicircle is a right angle (${m("\\angle ACB = 90^\\circ")}).`], { mx: "thales", k });
};
const cyclicQuad: Gen = (r) => {
  const A = r.int(40, 140), B = r.int(40, 140);
  return draft(`Quadrilateral ${m("ABCD")} is inscribed in a circle with ${m(`\\angle A = ${A}^\\circ`)} and ${m(`\\angle B = ${B}^\\circ`)}. Find ${m("\\angle C")}.`, exact(180 - A), `${180 - A}^\\circ`, [`Opposite angles of an inscribed quadrilateral are supplementary.`], { mx: "cyclic", A, B });
};
const arcSector: Gen = (r) => {
  const rad = r.int(2, 15), d = r.pick([30, 45, 60, 72, 90, 120, 135, 150, 210, 240, 270, 300]), sector = r.chance(0.5), inRad = r.chance(0.4);
  const v = sector ? q(d * rad * rad, 360) : q(2 * d * rad, 360);
  return draft(`A circle has radius ${rad}. Find the ${sector ? "area of the sector" : "length of the arc"} cut off by a central angle of ${inRad ? m(radTex(d)) : deg(d)} — exact in terms of π, or 2 decimals.`, approx(`(${qref(v)})*pi`, tol2(v.value() * Math.PI)), `${qtex(v)}\\pi`,
    [`${sector ? m("A = \\frac{\\theta}{360^\\circ}\\pi r^2 = \\tfrac12 r^2\\theta_{rad}") : m("s = \\frac{\\theta}{360^\\circ}2\\pi r = r\\theta_{rad}")}.`], { mx: "arc", rad, d, sector });
};
const circleEq: Gen = (r) => {
  const h = r.int(-8, 8), k = r.int(-8, 8), rad = r.int(1, 9);
  const D = -2 * h, E = -2 * k, F = h * h + k * k - rad * rad;
  return draft(`Find the center and radius of ${m(`x^2 + y^2${sg(D, "x")}${sg(E, "y")}${sg(F)} = 0`)}.`, tuple([{ label: "h", tex: "h", ref: h }, { label: "k", tex: "k", ref: k }, { label: "r", tex: "r", ref: rad }]), `(${h}, ${k}),\\ r = ${rad}`,
    [`Complete the square in x and y: ${m(`(x${sg(-h)})^2 + (y${sg(-k)})^2 = ${rad * rad}`)}.`], { mx: "circle-eq", D, E, F });
};
const onCircle: Gen = (r) => {
  const [a, b, c] = r.pick(TRIPLES), h = r.int(-5, 5), k = r.int(-5, 5), t = r.int(0, 2);
  const Q2 = t === 0 ? [h + b, k - a] : [h + b + (t === 1 ? -1 : 1), k - a];
  const ans = ["On the circle", "Inside", "Outside"][t];
  return draft(`A circle centered at ${m(`(${h}, ${k})`)} passes through ${m(`(${h + a}, ${k + b})`)}. Where is the point ${m(`(${Q2.join(", ")})`)}?`, choice(["On the circle", "Inside", "Outside"], (() => { const d2 = (Q2[0] - h) ** 2 + (Q2[1] - k) ** 2; return d2 === c * c ? "On the circle" : d2 < c * c ? "Inside" : "Outside"; })()), `\\text{${ans}}`,
    [`Radius ${c}; compare the point's distance from the center with ${c}.`], { mx: "on-circle", C: [h, k], P: [h + a, k + b], Q: Q2 });
};
const conic: Gen = (r) => {
  const [a, b, c] = r.pick(TRIPLES);
  const ell = r.chance(0.5);
  // ellipse: foci (±a', 0) with a'^2 = A^2 - B^2; hyperbola: c^2 = A^2 + B^2
  const [A, B, F] = ell ? [c, b, a] : [a, b, c];
  return draft(ell ? `An ellipse has foci ${m(`(\\pm ${F}, 0)`)} and the sum of distances to the foci is ${2 * A}. Write it as ${m("\\frac{x^2}{p} + \\frac{y^2}{q} = 1")}: give ${m("p, q")}.` : `A hyperbola has foci ${m(`(\\pm ${F}, 0)`)} and the difference of distances to the foci is ${2 * A}. Write it as ${m("\\frac{x^2}{p} - \\frac{y^2}{q} = 1")}: give ${m("p, q")}.`,
    tuple([{ label: "p", tex: "p", ref: A * A }, { label: "q", tex: "q", ref: B * B }]), `\\frac{x^2}{${A * A}} ${ell ? "+" : "-"} \\frac{y^2}{${B * B}} = 1`,
    [`${m(`a = ${A}`)}, ${m(`c = ${F}`)}; ${ell ? m(`b^2 = a^2 - c^2 = ${B * B}`) : m(`b^2 = c^2 - a^2 = ${B * B}`)}.`], { mx: "conic", ell, F, s: 2 * A });
};

// ── trigonometry ─────────────────────────────────────────────────────────────
const degRad: Gen = (r) => {
  const d = r.pick([15, 30, 36, 45, 60, 72, 90, 120, 135, 150, 210, 225, 240, 270, 300, 315, 330, 405, -60, -135]);
  return r.chance(0.5)
    ? draft(`Convert ${deg(d)} to radians (in terms of π, e.g. 3pi/4).`, { kind: "expression", ref: `${qref(q(d, 180))}*pi`, vars: [], label: "radians", tol: 1e-9 }, radTex(d), [`Multiply by ${m("\\frac{\\pi}{180}")}: ${m(radTex(d))}.`], { mx: "to-rad", d })
    : draft(`Convert ${m(radTex(d))} radians to degrees.`, exact(d), `${d}^\\circ`, [`Multiply by ${m("\\frac{180}{\\pi}")}.`], { mx: "to-deg", rad: qpy(q(d, 180)) });
};
const trigExactQ: Gen = (r) => {
  const d = 15 * r.int(-8, 32), d2 = d % 30 === 0 || d % 45 === 0 ? d : 45 * r.int(0, 7);
  const fn = r.pick(["sin", "cos", "tan"] as const);
  const v = trigExact(fn, d2);
  require_(v !== null);
  const inRad = r.chance(0.5);
  return draft(`Find the exact value of ${m(`\\${fn}\\left(${inRad ? radTex(d2) : `${d2}^\\circ`}\\right)`)} (e.g. sqrt(3)/2).`, { kind: "expression", ref: v![0], vars: [], label: fn, tol: 1e-9 }, v![1],
    [`Reference angle ${deg(((d2 % 180) + 180) % 180 > 90 ? 180 - (((d2 % 180) + 180) % 180) : ((d2 % 180) + 180) % 180)}; the sign comes from the quadrant (All Students Take Calculus).`], { mx: "trig-exact", fn, d: d2 });
};
const pythId: Gen = (r) => {
  const [a, b, c] = r.pick(TRIPLES), quad = r.int(1, 4), given = r.pick(["sin", "cos"] as const), want = r.pick(["cos", "tan", "sin"].filter((f) => f !== given));
  const sx = quad === 1 || quad === 4 ? 1 : -1, sy = quad <= 2 ? 1 : -1;
  const S = q(sy * a, c), C = q(sx * b, c), T = q(sy * a, sx * b);
  const gv = given === "sin" ? S : C, wv = want === "sin" ? S : want === "cos" ? C : T;
  return draft(`${m(`\\${given}\\theta = ${gv.tex()}`)} and ${m("\\theta")} is in quadrant ${["I", "II", "III", "IV"][quad - 1]}. Find ${m(`\\${want}\\theta`)}.`, exact(wv), wv.tex(),
    [`${m("\\sin^2\\theta + \\cos^2\\theta = 1")}: the other one has size ${m(`\\frac{${given === "sin" ? b : a}}{${c}}`)}; its sign comes from the quadrant.`], { mx: "pyth-id", given, gv: qpy(gv), quad, want });
};
const sinusoid: Gen = (r) => {
  const A = r.int(1, 9), B = r.pick([1, 2, 3, 4, q(1, 2), q(1, 3), q(1, 12)].map(Q.of)), h = r.int(-3, 3), k = r.int(-9, 9), fn = r.pick(["sin", "cos"]);
  if (r.chance(0.35)) {
    const lo = r.int(30, 60), hi = lo + 2 * r.int(5, 20), P = r.pick([12, 24, 365]);
    return draft(`A temperature oscillates between ${lo} and ${hi} with period ${P}. Model it as ${m("y = A\\sin(Bx) + k")} with ${m("A, B > 0")}: give ${m("A, B, k")} (B exact, e.g. pi/12).`,
      tuple([{ label: "A", tex: "A", ref: (hi - lo) / 2 }, { label: "B", tex: "B", ref: `2*pi/${P}` }, { label: "k", tex: "k", ref: (hi + lo) / 2 }]), `A = ${(hi - lo) / 2},\\ B = \\frac{2\\pi}{${P}},\\ k = ${(hi + lo) / 2}`,
      [`Amplitude = half the range; midline = the average; ${m("B = 2\\pi/\\text{period}")}.`], { mx: "sin-model", lo, hi, P });
  }
  return draft(`For ${m(`y = ${A === 1 ? "" : A}\\${fn}\\left(${B.isInt() && B.n === 1 ? "" : B.tex()}(x${sg(-h)})\\right)${sg(k)}`)}, give the amplitude, period (exact, e.g. pi), and midline ${m("y = c")}.`,
    tuple([{ label: "amplitude", tex: "A", ref: A }, { label: "period", tex: "T", ref: `2*pi/(${qref(B)})` }, { label: "midline c", tex: "c", ref: k }]), `${A},\\ ${q(2 * B.d, B.n).tex()}\\pi,\\ y = ${k}`,
    [`Amplitude ${m(`|A| = ${A}`)}, period ${m(`2\\pi / ${B.tex()}`)}, midline ${m(`y = ${k}`)} (the shift ${h} moves it sideways only).`], { mx: "sinusoid", e: `${A}*${fn}((${qpy(B)})*(x - (${h}))) + ${k}`, B: qpy(B) });
};
const trigSym: Gen = (r) => {
  const v = q(r.nz(-9, 9), 10), t = r.int(0, 4);
  const forms: [string, string, Q][] = [["\\sin(-\\theta)", "sin", v.neg()], ["\\sin(\\pi - \\theta)", "sin", v], ["\\sin(\\theta + 2\\pi)", "sin", v], ["\\cos(-\\theta)", "cos", v], ["\\cos(\\pi + \\theta)", "cos", v.neg()]];
  const [tex, given, ans] = forms[t];
  return draft(`If ${m(`\\${given}\\theta = ${v.value()}`)}, find ${m(tex)}.`, exact(ans), `${ans.value()}`, [[`Sine is odd.`, `Reflection across the y-axis keeps sine.`, `Period 2π.`, `Cosine is even.`, `A half turn negates cosine.`][t]], { mx: "trig-sym", given, v: qpy(v), expr: ["sin(-t)", "sin(pi - t)", "sin(t + 2*pi)", "cos(-t)", "cos(pi + t)"][t] });
};
const trigSolve: Gen = (r) => {
  const fn = r.pick(["sin", "cos"] as const);
  const special = r.chance(0.6);
  if (special) {
    const vals: [string, string, number[]][] = fn === "sin"
      ? [["1/2", "\\frac12", [30, 150]], ["-1/2", "-\\frac12", [210, 330]], ["sqrt(2)/2", "\\frac{\\sqrt2}{2}", [45, 135]], ["sqrt(3)/2", "\\frac{\\sqrt3}{2}", [60, 120]], ["-sqrt(3)/2", "-\\frac{\\sqrt3}{2}", [240, 300]], ["0", "0", [0, 180]]]
      : [["1/2", "\\frac12", [60, 300]], ["-1/2", "-\\frac12", [120, 240]], ["sqrt(2)/2", "\\frac{\\sqrt2}{2}", [45, 315]], ["-sqrt(2)/2", "-\\frac{\\sqrt2}{2}", [135, 225]], ["0", "0", [90, 270]], ["-sqrt(3)/2", "-\\frac{\\sqrt3}{2}", [150, 210]]];
    const [ref, tex, ds] = r.pick(vals);
    return draft(`Solve ${m(`\\${fn} x = ${tex}`)} for ${m("0 \\le x < 2\\pi")}. List all solutions (e.g. pi/6, 5pi/6).`, { kind: "roots", ref: ds.map((d) => (d * Math.PI) / 180), label: "x" }, ds.map(radTex).join(",\\ "),
      [`Reference angle from the unit circle; ${fn === "sin" ? "sine" : "cosine"} has this sign in two quadrants.`], { mx: "trig-solve", fn, v: ref });
  }
  const v = q(r.nz(-9, 9), 10);
  const a = fn === "sin" ? Math.asin(v.value()) : Math.acos(v.value());
  const sols = fn === "sin" ? [a < 0 ? a + 2 * Math.PI : a, Math.PI - a] : [a, 2 * Math.PI - a];
  return draft(`Solve ${m(`\\${fn} x = ${v.value()}`)} for ${m("0 \\le x < 2\\pi")}. Give both solutions exactly with ${fn === "sin" ? "asin" : "acos"} (e.g. ${fn === "sin" ? "asin(0.3), pi - asin(0.3)" : "acos(0.3), 2pi - acos(0.3)"}).`, { kind: "roots", ref: sols, label: "x" }, sols.map((s) => s.toFixed(4)).join(",\\ "),
    [fn === "sin" ? `${m("x = \\sin^{-1} v")} or ${m("\\pi - \\sin^{-1} v")}, shifted into ${m("[0, 2\\pi)")}.` : `${m("x = \\cos^{-1} v")} or ${m("2\\pi - \\cos^{-1} v")}.`], { mx: "trig-solve", fn, v: qpy(v) });
};
const addition: Gen = (r) => {
  if (r.chance(0.5)) {
    const d = r.pick([15, 75, 105, 165, 195, 255, 285, 345]), fn = r.pick(["sin", "cos"] as const);
    const v = trigExact(fn, d)!;
    return draft(`Use a sum or difference formula to find the exact value of ${m(`\\${fn} ${d}^\\circ`)} (e.g. (sqrt(6)-sqrt(2))/4).`, { kind: "expression", ref: v[0], vars: [], label: fn, tol: 1e-9 }, v[1],
      [`Write ${d}° as a sum or difference of 30°, 45°, 60°, 90°, 180° angles and expand.`], { mx: "trig-exact", fn, d });
  }
  const [a1, b1, c1] = r.pick(TRIPLES), [a2, b2, c2] = r.pick(TRIPLES), t = r.int(0, 2);
  const sa = q(a1, c1), ca = q(b1, c1), sb = q(a2, c2), cb = q(b2, c2);
  const [tex, v] = [["\\sin(\\alpha + \\beta)", sa.mul(cb).add(ca.mul(sb))], ["\\cos(\\alpha - \\beta)", ca.mul(cb).add(sa.mul(sb))], ["\\sin 2\\alpha", sa.mul(ca).mul(2)]][t] as [string, Q];
  return draft(`${m(`\\sin\\alpha = ${sa.tex()}`)} and ${m(`\\cos\\beta = ${cb.tex()}`)}, both angles acute. Find ${m(tex)}.`, exact(v), v.tex(),
    [`First ${m(`\\cos\\alpha = ${ca.tex()}`)}, ${m(`\\sin\\beta = ${sb.tex()}`)}; then expand.`], { mx: "sum-formula", sa: qpy(sa), cb: qpy(cb), which: ["sin(a+b)", "cos(a-b)", "sin(2a)"][t] });
};

// ── statistics ───────────────────────────────────────────────────────────────
function halves(xs: number[]) {
  const s = [...xs].sort((a, b) => a - b), n = s.length;
  const med = (a: number[]) => (a.length % 2 ? q(a[(a.length - 1) / 2]) : q(a[a.length / 2 - 1] + a[a.length / 2], 2));
  return { q1: med(s.slice(0, Math.floor(n / 2))), md: med(s), q3: med(s.slice(Math.ceil(n / 2))), s };
}
const center: Gen = (r) => {
  const n = r.int(6, 10), xs = Array.from({ length: n }, () => r.int(10, 60)), t = r.pick(["mean", "median", "IQR", "SD"]);
  const { q1, md, q3, s } = halves(xs);
  const mean = xs.reduce((a, b) => a + b, 0) / n;
  const sd = Math.sqrt(xs.reduce((a, x) => a + (x - mean) ** 2, 0) / n);
  if (t === "SD") return draft(`Data: ${m(xs.join(",\\ "))}. Find the population standard deviation (2 decimals).`, approx(sd, tol2(sd)), r2(sd), [`Mean ${mean.toFixed(3)}; average the squared deviations, then take the square root.`], { mx: "center", xs, t });
  const v = t === "mean" ? q(xs.reduce((a, b) => a + b, 0), n) : t === "median" ? md : q3.sub(q1);
  return draft(`Data: ${m(xs.join(",\\ "))}. Find the ${t === "IQR" ? "interquartile range (quartiles = medians of the lower and upper halves)" : t}.`, exact(v), v.tex(), [`Sorted: ${m(s.join(",\\ "))}${t === "IQR" ? `; ${m(`Q_1 = ${q1.tex()},\\ Q_3 = ${q3.tex()}`)}` : ""}.`], { mx: "center", xs, t });
};
const outlier: Gen = (r) => {
  const n = r.int(7, 11), xs = Array.from({ length: n }, () => r.int(20, 50));
  const { q1, q3 } = halves(xs);
  const iqr = q3.sub(q1), hi = q3.add(iqr.mul(q(3, 2)));
  if (r.chance(0.5)) return draft(`Data: ${m(xs.join(",\\ "))}. Using the 1.5 × IQR rule, what is the upper fence ${m("Q_3 + 1.5\\,\\text{IQR}")}?`, exact(hi), hi.tex(), [`${m(`Q_1 = ${q1.tex()},\\ Q_3 = ${q3.tex()},\\ \\text{IQR} = ${iqr.tex()}`)}.`], { mx: "fence", xs });
  const cand = r.chance(0.5) ? Math.ceil(hi.value()) + r.int(0, 10) : Math.floor(hi.value()) - r.int(1, 5);
  const out = q(cand).sub(hi).value() > 0;
  return draft(`Data: ${m(xs.join(",\\ "))}. By the 1.5 × IQR rule for this data, would a value of ${cand} be an outlier?`, choice(["Outlier", "Not an outlier"], out ? "Outlier" : "Not an outlier"), `\\text{${out ? "Outlier" : "Not an outlier"}}`,
    [`Upper fence ${m(hi.tex())}; ${cand} is ${out ? "above" : "not above"} it.`], { mx: "is-outlier", xs, v: cand });
};
const twoWayHS: Gen = (r) => {
  const t = [[r.int(5, 60), r.int(5, 60)], [r.int(5, 60), r.int(5, 60)]], kind = r.int(0, 2), i = r.int(0, 1), j = r.int(0, 1);
  const tot = t.flat().reduce((a, b) => a + b, 0), row = t[i][0] + t[i][1], col = t[0][j] + t[1][j];
  const rows = ["juniors", "seniors"], cols = ["drive to school", "don't drive"];
  const [txt, v] = [[`What fraction of all students are ${rows[i]} who ${cols[j]}?`, q(t[i][j], tot)], [`What fraction of all students ${cols[j]}?`, q(col, tot)], [`What fraction of ${rows[i]} ${cols[j]}?`, q(t[i][j], row)]][kind] as [string, Q];
  return draft(`Juniors: ${t[0][0]} drive to school, ${t[0][1]} don't. Seniors: ${t[1][0]} drive, ${t[1][1]} don't. ${txt}`, exact(v), v.tex(), [[`Joint relative frequency: cell ÷ grand total.`, `Marginal: column total ÷ grand total.`, `Conditional: cell ÷ row total.`][kind]], { mx: "two-way-hs", t, kind, i, j });
};
const regression: Gen = (r) => {
  const mm = q(r.nz(-6, 6), r.pick([1, 2])), b = r.int(-10, 20), c1 = r.int(-3, 3), c2 = r.int(-3, 3);
  const xs = [1, 2, 3, 4, 5];
  const e = [0, 1, 2, 3, 4].map((i) => c1 * [1, -2, 0, 2, -1][i] + c2 * [2, -1, -2, -1, 2][i]);
  const ys = xs.map((x, i) => mm.mul(x).add(b).add(e[i]));
  require_(ys.every((y) => y.isInt()) && (c1 !== 0 || c2 !== 0));
  if (r.chance(0.4)) {
    const x0 = r.int(6, 12);
    return draft(`Fit the least-squares line to ${m(xs.map((x, i) => `(${x}, ${ys[i].n})`).join(",\\ "))} and use it to predict ${m("y")} at ${m(`x = ${x0}`)}.`, exact(mm.mul(x0).add(b)), mm.mul(x0).add(b).tex(), [`Least squares: ${m(`\\hat y = ${poly([mm, b])}`)} (slope ${m("\\frac{\\sum (x-\\bar x)(y - \\bar y)}{\\sum (x - \\bar x)^2}")}).`], { mx: "lsq-pred", xs, ys: ys.map((y) => y.n), x0 });
  }
  return draft(`Find the least-squares regression line ${m("\\hat y = mx + b")} for ${m(xs.map((x, i) => `(${x}, ${ys[i].n})`).join(",\\ "))}.`, tuple([{ label: "m", tex: "m", ref: mm }, { label: "b", tex: "b", ref: b }]), `\\hat y = ${poly([mm, b])}`,
    [`${m("\\bar x = 3")}, ${m(`\\bar y = ${ys.reduce((a, y) => a.add(y), q(0)).div(5).tex()}`)}; ${m("m = \\frac{\\sum (x-\\bar x)(y-\\bar y)}{\\sum (x-\\bar x)^2}")}, ${m("b = \\bar y - m\\bar x")}.`], { mx: "lsq", xs, ys: ys.map((y) => y.n) });
};
const residual: Gen = (r) => {
  const mm = q(r.int(-50, 50), 10), b = r.int(-20, 40), x = r.int(1, 30), y = r.int(-20, 120);
  const v = q(y).sub(mm.mul(x).add(b));
  return draft(`The fitted line is ${m(`\\hat y = ${mm.value()}x${sg(b)}`)}. For the data point ${m(`(${x}, ${y})`)}, what is the residual?`, exact(v), `${v.value()}`, [`Residual = observed − predicted = ${m(`${y} - ${mm.mul(x).add(b).value()}`)}.`], { mx: "residual", m: qpy(mm), b, x, y });
};
const correlation: Gen = (r) => {
  const n = 5, xs = shuffle([1, 2, 3, 4, 5, 6, 7, 8], () => r.next()).slice(0, n).sort((a, b) => a - b), s = r.pick([1, -1]);
  const ys = xs.map((x) => s * 2 * x + r.int(-3, 3) + 10);
  const mx = xs.reduce((a, b) => a + b) / n, my = ys.reduce((a, b) => a + b) / n;
  const sxy = xs.reduce((a, x, i) => a + (x - mx) * (ys[i] - my), 0), sxx = xs.reduce((a, x) => a + (x - mx) ** 2, 0), syy = ys.reduce((a, y) => a + (y - my) ** 2, 0);
  const rr = sxy / Math.sqrt(sxx * syy);
  require_(Math.abs(rr) > 0.4 && Math.abs(rr) < 0.999);
  return draft(`Compute the correlation coefficient ${m("r")} for ${m(xs.map((x, i) => `(${x}, ${ys[i]})`).join(",\\ "))} (3 decimals).`, approx(rr, 0.0015), rr.toFixed(3), [`${m("r = \\frac{\\sum(x-\\bar x)(y-\\bar y)}{\\sqrt{\\sum(x-\\bar x)^2\\sum(y-\\bar y)^2}}")}.`], { mx: "corr", xs, ys });
};
const normal: Gen = (r) => {
  const mu = r.int(50, 150), sd = r.int(2, 15), t = r.int(0, 3);
  if (t === 3) {
    const z = q(r.int(-30, 30), 10), x = z.mul(sd).add(mu);
    return draft(`A normal distribution has mean ${mu} and standard deviation ${sd}. What is the z-score of ${x.value()}?`, exact(z), `${z.value()}`, [`${m(`z = \\frac{x - \\mu}{\\sigma} = \\frac{${x.value()} - ${mu}}{${sd}}`)}.`], { mx: "zscore", mu, sd, x: qpy(x) });
  }
  const k = r.int(1, 3);
  const [txt, v] = [[`between ${mu - k * sd} and ${mu + k * sd}`, [68, 95, 99.7][k - 1]], [`above ${mu + k * sd}`, [16, 2.5, 0.15][k - 1]], [`between ${mu - sd} and ${mu + 2 * sd}`, 81.5]][t] as [string, number];
  return draft(`A normal distribution has mean ${mu} and standard deviation ${sd}. By the empirical rule (68–95–99.7), about what percent of values lie ${txt}?`, approx(v, 1e-6), `${v}\\%`, [`68% within 1σ, 95% within 2σ, 99.7% within 3σ; the rest splits evenly into the two tails.`], { mx: "empirical", mu, sd, lo: t === 1 ? mu + k * sd : t === 2 ? mu - sd : mu - k * sd, hi: t === 1 ? null : t === 2 ? mu + 2 * sd : mu + k * sd });
};
const margin: Gen = (r) => {
  const n = r.pick([100, 200, 400, 500, 1000]), k = r.int(Math.round(n * 0.2), Math.round(n * 0.8));
  const p = k / n, me = 2 * Math.sqrt((p * (1 - p)) / n) * 100;
  return draft(`In a random sample of ${n}, ${k} say yes. Estimate the margin of error (≈ 2 standard errors of the sample proportion), in percentage points, 2 decimals.`, approx(me, tol2(me)), r2(me), [`${m(`\\hat p = ${p}`)}, ${m(`SE = \\sqrt{\\hat p(1-\\hat p)/n}`)}; margin ≈ ${m("2\\,SE")} = ${r2(me)} points.`], { mx: "margin", n, k });
};

// ── probability ─────────────────────────────────────────────────────────────
const SUITS = ["hearts", "diamonds", "clubs", "spades"];
const addRule: Gen = (r) => {
  if (r.chance(0.5)) {
    const s = r.pick(SUITS), face = r.chance(0.5);
    const v = face ? q(13 + 12 - 3, 52) : q(13 + 4 - 1, 52);
    const rank = r.pick(["king", "queen", "ace", "seven"]);
    return draft(`One card is drawn from a standard 52-card deck. What is the probability it is a ${s.slice(0, -1)} or ${face ? "a face card (J, Q, K)" : `a ${rank}`}?`, exact(v), v.tex(), [`${m("P(A \\cup B) = P(A) + P(B) - P(A \\cap B)")}: ${m(`\\frac{13}{52} + \\frac{${face ? 12 : 4}}{52} - \\frac{${face ? 3 : 1}}{52}`)}.`], { mx: "cards-or", suit: s, other: face ? "face" : rank });
  }
  const k = r.int(2, 5);
  return draft(`A fair die is rolled. What is the probability of an even number or a number greater than ${k}?`, exact(q([2, 4, 6].filter((x) => x <= k).length + (6 - k), 6)), q([2, 4, 6].filter((x) => x <= k).length + (6 - k), 6).tex(), [`Count the outcomes in the union directly, or use the addition rule.`], { mx: "die-or", k });
};
const conditional: Gen = (r) => {
  const s = r.int(4, 10), cond = r.pick(["the first die is even", "at least one die shows a 3", "the first die is less than 4", "the dice match"]);
  const outs: [number, number][] = [];
  for (let a = 1; a <= 6; a++) for (let b = 1; b <= 6; b++) outs.push([a, b]);
  const B = outs.filter(([a, b]) => (cond.includes("even") ? a % 2 === 0 : cond.includes("3") ? a === 3 || b === 3 : cond.includes("less") ? a < 4 : a === b));
  const AB = B.filter(([a, b]) => a + b === s);
  return draft(`Two fair dice are rolled. Given that ${cond}, what is the probability the sum is ${s}?`, exact(q(AB.length, B.length)), q(AB.length, B.length).tex(), [`Restrict to the ${B.length} outcomes where ${cond}; ${AB.length} of them sum to ${s}.`], { mx: "dice-cond", s, cond });
};
const independence: Gen = (r) => {
  const pa = q(r.int(1, 9), 10), pb = q(r.int(1, 9), 10), ind = r.chance(0.5);
  const pab = ind ? pa.mul(pb) : pa.mul(pb).add(q(r.nz(-5, 5), 100));
  require_(pab.value() > 0 && pab.value() <= Math.min(pa.value(), pb.value()));
  if (r.chance(0.4)) {
    const v = pab.div(pb);
    return draft(`${m(`P(A) = ${pa.value()},\\ P(B) = ${pb.value()},\\ P(A \\cap B) = ${pab.value()}`)}. Find ${m("P(A \\mid B)")}.`, exact(v), v.tex(), [`${m("P(A\\mid B) = \\frac{P(A \\cap B)}{P(B)}")}.`], { mx: "cond-prob", pab: qpy(pab), pb: qpy(pb) });
  }
  return draft(`${m(`P(A) = ${pa.value()},\\ P(B) = ${pb.value()},\\ P(A \\cap B) = ${pab.value()}`)}. Are ${m("A")} and ${m("B")} independent?`, choice(["Independent", "Not independent"], ind ? "Independent" : "Not independent"), `\\text{${ind ? "Independent" : "Not independent"}}`, [`Independent ⇔ ${m("P(A\\cap B) = P(A)P(B)")} = ${pa.mul(pb).value()}.`], { mx: "independent", pa: qpy(pa), pb: qpy(pb), pab: qpy(pab) });
};
const multRule: Gen = (r) => {
  const red = r.int(2, 8), blue = r.int(2, 8), k = r.int(2, 3), with_ = r.chance(0.3);
  const v = with_ ? q(red, red + blue).mul(Q.of(red ** (k - 1)).div((red + blue) ** (k - 1))) : Array.from({ length: k }, (_, i) => q(red - i, red + blue - i)).reduce((a, b) => a.mul(b));
  require_(red >= k);
  return draft(`A bag has ${red} red and ${blue} blue marbles. ${k} are drawn ${with_ ? "with" : "without"} replacement. What is the probability all are red?`, exact(v), v.tex(), [`${m("P(A \\cap B) = P(A)P(B\\mid A)")}: ${m(Array.from({ length: k }, (_, i) => `\\frac{${with_ ? red : red - i}}{${with_ ? red + blue : red + blue - i}}`).join(" \\cdot "))}.`], { mx: "draw-all-red", red, blue, k, with: with_ });
};
const countingProb: Gen = (r) => {
  const n = r.int(6, 10), k = r.int(2, 4), w = r.int(k, n - 1);
  const C = (a: number, b: number) => binom(a, b);
  const v = q(C(w, k), C(n, k));
  return draft(`A committee of ${k} is chosen at random from ${n} people, ${w} of whom are women. What is the probability all ${k} are women?`, exact(v), v.tex(), [`${m(`\\frac{\\binom{${w}}{${k}}}{\\binom{${n}}{${k}}} = \\frac{${C(w, k)}}{${C(n, k)}}`)}.`], { mx: "committee", n, k, w });
};
const bayes: Gen = (r) => {
  const prev = q(r.pick([1, 2, 5, 10]), 100), sens = q(r.pick([90, 95, 98, 99]), 100), spec = q(r.pick([90, 95, 98, 99]), 100);
  const tp = prev.mul(sens), fp = q(1).sub(prev).mul(q(1).sub(spec));
  const v = tp.div(tp.add(fp));
  return draft(`A disease affects ${prev.mul(100).tex()}% of people. A test catches ${sens.mul(100).tex()}% of cases and correctly clears ${spec.mul(100).tex()}% of healthy people. If someone tests positive, what is the probability they have the disease? (fraction)`, exact(v), v.tex(),
    [`Out of 10,000 people: ${tp.mul(10000).tex()} true positives, ${fp.mul(10000).tex()} false positives; ${m(`P = \\frac{${tp.mul(10000).tex()}}{${tp.add(fp).mul(10000).tex()}}`)}.`], { mx: "bayes", prev: qpy(prev), sens: qpy(sens), spec: qpy(spec) });
};
const expected: Gen = (r) => {
  const t = r.int(0, 2);
  if (t === 0) {
    const xs = [0, 1, 2, 3], ps = [r.int(1, 5), r.int(1, 5), r.int(1, 5), r.int(1, 5)];
    const tot = ps.reduce((a, b) => a + b, 0);
    const v = q(xs.reduce((a, x, i) => a + x * ps[i], 0), tot);
    return draft(`A random variable takes values 0, 1, 2, 3 with probabilities ${m(ps.map((p) => q(p, tot).tex()).join(",\\ "))}. Find its expected value.`, exact(v), v.tex(), [`${m("E[X] = \\sum x\\,P(x)")}.`], { mx: "ev", xs, ps: ps.map((p) => qpy(q(p, tot))) });
  }
  if (t === 1) {
    const n = r.int(10, 40), k = r.pick([2, 4, 5]);
    return draft(`A student guesses on all ${n} questions of a multiple-choice test with ${k} choices each. What is the expected number of correct answers?`, exact(q(n, k)), q(n, k).tex(), [`Each question is right with probability ${m(`\\frac1{${k}}`)}; expectations add: ${m(`${n}\\cdot\\frac1{${k}}`)}.`], { mx: "guess", n, k });
  }
  const cost = r.int(1, 5), prize = r.int(5, 50), win = q(1, r.pick([5, 6, 8, 10, 20]));
  const v = win.mul(prize).sub(cost);
  return draft(`A game costs ${m(`\\text{\\textdollar}${cost}`)} to play and pays ${m(`\\text{\\textdollar}${prize}`)} with probability ${m(win.tex())} (nothing otherwise). What is the expected net gain per game in dollars?`, exact(v), v.tex(), [`${m(`E = ${win.tex()}\\cdot ${prize} - ${cost}`)}.`], { mx: "game", cost, prize, win: qpy(win) });
};
const insurance: Gen = (r) => {
  const pA = r.int(5, 20) * 100, dA = r.int(5, 20) * 100, pB = pA + r.int(2, 10) * 100, dB = r.int(1, 4) * 100, pr = q(r.int(5, 40), 100);
  const eA = pr.mul(dA).add(pA), eB = pr.mul(dB).add(pB);
  require_(!eA.sub(eB).isZero());
  const best = eA.value() < eB.value() ? "Plan A" : "Plan B";
  return draft(`Plan A: premium ${m(`\\text{\\textdollar}${pA}`)}, deductible ${m(`\\text{\\textdollar}${dA}`)}. Plan B: premium ${m(`\\text{\\textdollar}${pB}`)}, deductible ${m(`\\text{\\textdollar}${dB}`)}. You expect one claim a year with probability ${pr.value()} (paying the deductible), none otherwise. Which plan has the lower expected yearly cost?`, choice(["Plan A", "Plan B"], best), `\\text{${best}}`,
    [`Expected cost = premium + P(claim)·deductible: A ${eA.value()}, B ${eB.value()}.`], { mx: "insurance", pA, dA, pB, dB, pr: qpy(pr) });
};

export const HS_TEMPLATES: Record<string, Gen> = {
  // algebra & functions
  "alg-linear-eq": linearEq,
  "alg-literal": literal,
  "alg-linear-ineq": linearIneq,
  "alg-word-linear": wordLinear,
  "alg-func-eval": funcEval,
  "alg-seq-recursive": seqRecursive,
  "alg-avg-rate": avgRate,
  "alg-intercepts": intercepts,
  "alg-lin-exp": linExp,
  "alg-exp-2pts": exp2pts,
  "alg-seq-explicit": seqExplicit,
  "alg-exp-params": expParams,
  "alg-rational-exp": rationalExp,
  "alg-half-plane": halfPlane,
  "alg-poly-arith": polyArith,
  "alg-factor-zeros": factorZeros,
  "alg-complete-square": completeSquare,
  "alg-quad-formula": quadFormula,
  "alg-quad-word": quadWord,
  "alg-lin-quad": linQuad,
  "alg-vertex": vertex,
  "alg-transform": transformFn,
  "alg-even-odd": evenOdd,
  "alg-inverse": inverse,
  "alg-piecewise": piecewise,
  "alg-structure": structure,
  "alg-binomial": binomial,
  "alg-remainder": remainder,
  "alg-poly-zeros": polyZeros,
  "alg-geom-series": geomSeries,
  "alg-poly-div": polyDiv,
  "alg-rational-add": rationalAdd,
  "alg-rational-eq": rationalEq,
  "alg-complex-arith": complexArith,
  "alg-complex-roots": complexRoots,
  "alg-exp-solve": expSolve,
  "alg-exp-graph": expLogGraph("exp"),
  "alg-log-graph": expLogGraph("log"),
  "alg-cooling": cooling,
  "alg-compose": compose,
  "alg-log-rules": logRules,
  "alg-log-eq": logEq,
  "alg-rational-graph": rationalGraph,
  "alg-complex-conj": complexConj,
  "alg-complex-dist": complexDist,
  "alg-vector": vectorOps,
  "alg-vector-polar": vectorPolar,
  "alg-matrix-ops": matrixOps,
  "alg-matrix-det": matrixDet,
  // geometry
  "geo-transform": geoTransform,
  "geo-symmetry": symmetry,
  "geo-congruence": congruence,
  "geo-angles-lines": anglesLines,
  "geo-triangle-thm": triangleThm,
  "geo-parallelogram": parallelogram,
  "geo-dilation": dilation,
  "geo-similar": similar,
  "geo-side-splitter": sideSplitter,
  "geo-right-trig": rightTrig,
  "geo-trig-ratio": trigRatio,
  "geo-density": density,
  "geo-area-sin": areaSin,
  "geo-law-sines": lawSines,
  "geo-law-cosines": lawCosines,
  "geo-volume": volume,
  "geo-cross-section": crossSection,
  "geo-parallel-perp": parallelPerp,
  "geo-partition": partition,
  "geo-coord-perimeter": coordPerim,
  "geo-coord-proof": coordProof,
  "geo-parabola": parabola,
  "geo-inscribed": inscribed,
  "geo-cyclic-quad": cyclicQuad,
  "geo-arc-sector": arcSector,
  "geo-circle-eq": circleEq,
  "geo-on-circle": onCircle,
  "geo-conic": conic,
  // trigonometry
  "trig-deg-rad": degRad,
  "trig-exact": trigExactQ,
  "trig-pyth": pythId,
  "trig-sinusoid": sinusoid,
  "trig-symmetry": trigSym,
  "trig-solve": trigSolve,
  "trig-addition": addition,
  // statistics & probability
  "stats-center": center,
  "stats-outlier": outlier,
  "stats-two-way": twoWayHS,
  "stats-regression": regression,
  "stats-residual": residual,
  "stats-correlation": correlation,
  "stats-normal": normal,
  "stats-margin": margin,
  "stats-addition": addRule,
  "stats-conditional": conditional,
  "stats-independence": independence,
  "stats-mult-rule": multRule,
  "stats-counting": countingProb,
  "stats-bayes": bayes,
  "stats-expected": expected,
  "stats-insurance": insurance,
};
