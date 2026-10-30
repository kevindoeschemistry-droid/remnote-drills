// Kreyszig 10e §6.2 (transfer function), §6.3 (unit step IVPs), §6.4 (δ, impulse response),
// §6.6 (L{tf} = −F′), §6.7 (systems), §12.1 (classification), §12.4 (d'Alembert),
// §12.6 (Laplace's equation on a rectangle). Level 1.
//
// Built backward as everywhere else: pick the characteristic roots, the switch times and
// clean coefficients, then derive the equation, the forcing and the initial data shown.
import { Rng } from "./rng";
import type { Draft } from "./types";
import { ct, join, m, gcd } from "./tex";
import { Q, qterm } from "./rational";
import { require_ } from "./reject";

const LT = "\\mathcal{L}";
const lcm = (a: number, b: number) => Math.abs(a * b) / gcd(a, b);
const lcmDen = (qs: Q[]) => qs.reduce((l, q) => lcm(l, q.d), 1);

// ── polynomials (integer coefficients, index = power) ──────────────────────
type Poly = number[];
const trim = (p: Poly) => {
  const q = [...p];
  while (q.length > 1 && q[q.length - 1] === 0) q.pop();
  return q;
};
const pmul = (a: Poly, b: Poly): Poly => {
  const out = new Array(a.length + b.length - 1).fill(0);
  a.forEach((x, i) => b.forEach((y, j) => (out[i + j] += x * y)));
  return trim(out);
};
function ptex(p: Poly, v = "s"): string {
  const terms: string[] = [];
  for (let i = p.length - 1; i >= 0; i--) terms.push(i === 0 ? `${p[i]}` : ct(p[i], i === 1 ? v : `${v}^{${i}}`));
  return join(terms);
}
const pjs = (p: Poly, v = "s") => `(${p.map((c, i) => `(${c})*${v}^${i}`).join(" + ")})`;
const linTex = (k: number, v = "s") => (k === 0 ? v : k > 0 ? `${v} - ${k}` : `${v} + ${-k}`);
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
/** c · num/den as one signed LaTeX fraction term (for join) */
function fr(c: Q, num: string, den: string): string {
  if (c.isZero()) return "0";
  const a = Math.abs(c.n);
  const top = num === "1" ? `${a}` : a === 1 ? num : topLevel(num) ? `${a}(${num})` : `${a}${num}`;
  const bot = c.d === 1 ? den : topLevel(den) ? `${c.d}(${den})` : `${c.d}${den}`;
  return `${c.n < 0 ? "-" : ""}\\frac{${top}}{${bot}}`;
}

// ── time-domain terms  c · e^{kt} · {1, t, cos wt, sin wt}, optionally delayed ──
interface Sh { tex: string; js: string; v: number }
const SH = (a: number): Sh => ({ tex: `${a}`, js: `${a}`, v: a });
const SHPI = (k: number): Sh => ({ tex: k === 1 ? "\\pi" : `${k}\\pi`, js: `(${k}*pi)`, v: k * Math.PI });
const eas = (sh: Sh) => `e^{-${sh.tex === "1" ? "" : sh.tex}${sh.tex.endsWith("pi") ? " " : ""}s}`;

type Fn = "exp" | "texp" | "cos" | "sin";
interface Tm { c: Q; f: Fn; k: number; w: number }
const tm = (c: number | Q, f: Fn, k = 0, w = 1): Tm => ({ c: Q.of(c), f, k, w });
const scale = (ts: Tm[], K: number | Q) => ts.map((u) => ({ ...u, c: u.c.mul(K) }));

function body(u: Tm, sh?: Sh): string {
  const V = sh ? `(t - ${sh.tex})` : "t";
  const Vin = sh ? `t - ${sh.tex}` : "t";
  const E = u.k === 0 ? "" : `e^{${u.k === 1 ? Vin : u.k === -1 ? `-${V}` : `${u.k}${V}`}}`;
  const trig = (fn: string) => (sh ? `\\${fn}${u.w === 1 ? `(${Vin})` : ` ${u.w}${V}`}` : `\\${fn} ${u.w === 1 ? "" : u.w}t`);
  switch (u.f) {
    case "exp": return E;
    case "texp": return `${V}${E}`;
    case "cos": return `${E}${trig("cos")}`;
    case "sin": return `${E}${trig("sin")}`;
  }
}
const tTex = (u: Tm, sh?: Sh) => qterm(u.c, body(u, sh));
function tJs(u: Tm, sh?: Sh): string {
  const V = sh ? `(t-${sh.js})` : "t";
  const E = `exp((${u.k})*${V})`;
  const b = { exp: E, texp: `${V}*${E}`, cos: `${E}*cos((${u.w})*${V})`, sin: `${E}*sin((${u.w})*${V})` }[u.f];
  return `${u.c.js()}*${b}`;
}
const sumTex = (ts: Tm[], sh?: Sh) => join(ts.map((u) => tTex(u, sh)));
const sumJs = (ts: Tm[], sh?: Sh) => (ts.length ? ts.map((u) => tJs(u, sh)).join(" + ") : "0");
/** y(0), y'(0) of an undelayed term */
const at0 = (u: Tm): [Q, Q] =>
  u.f === "exp" ? [u.c, u.c.mul(u.k)] : u.f === "texp" ? [new Q(0), u.c] : u.f === "cos" ? [u.c, u.c.mul(u.k)] : [new Q(0), u.c.mul(u.w)];
/** transform of an undelayed term, LaTeX */
function sTex(u: Tm): string {
  switch (u.f) {
    case "exp": return fr(u.c, "1", u.k === 0 ? "s" : linTex(u.k));
    case "texp": return fr(u.c, "1", u.k === 0 ? "s^{2}" : `(${linTex(u.k)})^{2}`);
    case "cos": return fr(u.c, linTex(u.k), quadTex(u.k, u.w));
    case "sin": return fr(u.c.mul(u.w), "1", quadTex(u.k, u.w));
  }
}
const sSum = (ts: Tm[]) => join(ts.map(sTex));

/** a delayed group  [h(t - a)]u(t - a), leading sign pulled out */
function groupTex(ts: Tm[], sh: Sh): string {
  const u = `u(t - ${sh.tex})`;
  if (ts.length === 1) return qterm(ts[0].c, `${body(ts[0], sh)}${u}`);
  const neg = ts[0].c.n < 0;
  const inner = sumTex(neg ? scale(ts, -1) : ts, sh);
  return `${neg ? "-" : ""}\\left[${inner}\\right]${u}`;
}

// ── characteristic polynomial s^2 + bs + c, built from its roots ───────────
interface Char {
  type: "undamped" | "real" | "complex" | "double";
  b: number;
  c: number;
  basis: Tm[]; // homogeneous solutions (coefficient 1)
  g: Tm[]; // impulse response  L^{-1}{1/p(s)}
  h: Tm[]; // unit-step response L^{-1}{1/(s p(s))}
  facTex: string; // p(s) factored
}
function pickChar(r: Rng, types: Char["type"][]): Char {
  const type = r.pick(types);
  if (type === "undamped") {
    const w = r.int(1, 3);
    return {
      type, b: 0, c: w * w,
      basis: [tm(1, "cos", 0, w), tm(1, "sin", 0, w)],
      g: [tm(new Q(1, w), "sin", 0, w)],
      h: [tm(new Q(1, w * w), "exp"), tm(new Q(-1, w * w), "cos", 0, w)],
      facTex: `s^{2} + ${w * w}`,
    };
  }
  if (type === "real") {
    const r1 = r.int(-4, -1), r2 = r.int(-4, -1);
    require_(r1 < r2);
    return {
      type, b: -(r1 + r2), c: r1 * r2,
      basis: [tm(1, "exp", r1), tm(1, "exp", r2)],
      g: [tm(new Q(-1, r2 - r1), "exp", r1), tm(new Q(1, r2 - r1), "exp", r2)],
      h: [tm(new Q(1, r1 * r2), "exp"), tm(new Q(1, r1 * (r1 - r2)), "exp", r1), tm(new Q(1, r2 * (r2 - r1)), "exp", r2)],
      facTex: `(${linTex(r1)})(${linTex(r2)})`,
    };
  }
  if (type === "complex") {
    const p = r.int(-2, -1), w = r.int(1, 3);
    const D = p * p + w * w;
    return {
      type, b: -2 * p, c: D,
      basis: [tm(1, "cos", p, w), tm(1, "sin", p, w)],
      g: [tm(new Q(1, w), "sin", p, w)],
      h: [tm(new Q(1, D), "exp"), tm(new Q(-1, D), "cos", p, w), tm(new Q(p, w * D), "sin", p, w)],
      facTex: quadTex(p, w),
    };
  }
  const k = r.int(-3, -1);
  return {
    type, b: -2 * k, c: k * k,
    basis: [tm(1, "exp", k), tm(1, "texp", k)],
    g: [tm(1, "texp", k)],
    h: [tm(new Q(1, k * k), "exp"), tm(new Q(-1, k * k), "exp", k), tm(new Q(1, k), "texp", k)],
    facTex: `(${linTex(k)})^{2}`,
  };
}
const charEq = (b: number, c: number) => join(["y''", ct(b, "y'"), ct(c, "y")]);
const charPoly = (b: number, c: number) => ptex([c, b, 1]);

// ══ laplace.step-ivp / laplace.delta: one engine ═════════════════════════════
interface Force { sh: Sh; K: number; delta: boolean }

function switchedDraft(r: Rng, ch: Char, forces: Force[], rTex: string): Draft {
  const hc = r.chance(0.5) ? [0, 0] : [r.int(-3, 3), r.int(-3, 3)];
  const hom = ch.basis.map((u, i) => ({ ...u, c: new Q(hc[i]) })).filter((u) => !u.c.isZero());
  const y0 = hom.reduce((s, u) => s.add(at0(u)[0]), new Q(0)).n;
  const y1 = hom.reduce((s, u) => s.add(at0(u)[1]), new Q(0)).n;
  const groups = forces.map((f) => ({ f, ts: scale(f.delta ? ch.g : ch.h, f.K) }));
  const yTex = join([sumTex(hom), ...groups.map((g) => groupTex(g.ts, g.f.sh))]);
  const yJs = [sumJs(hom), ...groups.map((g) => `(${sumJs(g.ts, g.f.sh)})*heaviside(t-${g.f.sh.js})`)].join(" + ");
  const steps = forces.filter((f) => !f.delta);
  const rhsJs = steps.length ? steps.map((f) => `(${f.K})*heaviside(t-${f.sh.js})`).join(" + ") : undefined;
  const icTex = join([ct(y0, "s"), `${ch.b * y0 + y1}`]);
  const forcingS = join(forces.map((f) => (f.delta ? ct(f.K, eas(f.sh)) : fr(new Q(f.K), eas(f.sh), "s"))));
  const anyStep = forces.some((f) => !f.delta), anyDelta = forces.some((f) => f.delta);
  const unit = anyStep ? h0Tex(ch) : "";
  const sub = `(${charPoly(ch.b, ch.c)})Y = ${join([icTex === "0" ? "" : icTex, forcingS])}`;
  return {
    prompt: `Solve by the Laplace transform: ${m(`${charEq(ch.b, ch.c)} = ${rTex}`)}, ${m(`y(0) = ${y0},\\ y'(0) = ${y1}`)}. Write unit steps as ${m("u(t - a)")}.`,
    answer: {
      kind: "ode2", a: 1, b: ch.b, c: ch.c, v: "t", ...(rhsJs ? { rhs: rhsJs } : {}), ic: [0, y0, y1], ref: yJs,
      switches: forces.map((f) => ({ at: f.sh.v, kick: f.delta ? f.K : 0 })),
    },
    answerTex: `y = ${yTex}`,
    steps: [
      `Transform: ${anyStep ? m(`${LT}\\{u(t - a)\\} = \\frac{e^{-as}}{s}`) : ""}${anyStep && anyDelta ? ", " : ""}${anyDelta ? m(`${LT}\\{\\delta(t - a)\\} = e^{-as}`) : ""}, ${m(`${LT}\\{y''\\} = s^{2}Y - sy(0) - y'(0)`)}. Subsidiary equation: ${m(sub)}.`,
      ...(hom.length ? [`Initial-condition part: ${m(`\\frac{${icTex}}{${ch.facTex}} = ${sSum(hom)}`)}, which inverts to ${m(sumTex(hom))}.`] : [`Zero initial conditions: only the forcing contributes.`]),
      ...(anyStep ? [`Partial fractions: ${m(`\\frac{1}{s(${ch.facTex})} = ${sSum(ch.h)}`)}, so ${m(`h(t) = ${LT}^{-1}\\left\\{\\frac{1}{s(${ch.facTex})}\\right\\} = ${unit}`)}.`] : []),
      ...(anyDelta ? [`${m(`g(t) = ${LT}^{-1}\\left\\{\\frac{1}{${ch.facTex}}\\right\\} = ${sumTex(ch.g)}`)}.`] : []),
      `t-shifting: ${m(`e^{-as}F(s) \\to f(t - a)u(t - a)`)}, one delayed copy per switch.${anyDelta ? ` (y stays continuous; ${m("y'")} jumps by the impulse strength at each ${m("\\delta")}.)` : ` (y and ${m("y'")} stay continuous at the switches.)`}`,
      m(`y = ${yTex}`),
    ],
    meta: { b: ch.b, c: ch.c, y0, y1, forcing: forces.map((f) => ({ type: f.delta ? "delta" : "step", at: f.sh.js, K: f.K })) },
  };
}
const h0Tex = (ch: Char) => sumTex(ch.h);

function stepOn(r: Rng): Draft {
  const ch = pickChar(r, ["undamped", "real", "complex", "double"]);
  const sh = ch.type === "undamped" && r.chance(0.4) ? SHPI(1) : SH(r.int(1, 3));
  const K = lcmDen(ch.h.map((u) => u.c)) * r.nz(-2, 2);
  require_(Math.abs(K) <= 20);
  const d = switchedDraft(r, ch, [{ sh, K, delta: false }], ct(K, `u(t - ${sh.tex})`));
  return fixCases(d, r.chance(0.5), `r(t) = \\begin{cases} 0 & 0 < t < ${sh.tex} \\\\ ${K} & t > ${sh.tex} \\end{cases}`);
}

/** present the forcing as cases in the prompt; the steps then rewrite it with unit steps */
function fixCases(d: Draft, cases: boolean, casesTex: string): Draft {
  if (!cases) return d;
  const eq = /\$(y'' [^$]*?) = ([^$]*)\$/.exec(d.prompt)!;
  return {
    ...d,
    prompt: d.prompt.replace(eq[0], `$${eq[1]} = r(t)$`).replace(/\. Write unit steps/, `, where $${casesTex}$. Write unit steps`),
    steps: [`Write the forcing with unit steps: ${m(`r(t) = ${eq[2]}`)}.`, ...d.steps],
  };
}

function stepPulse(r: Rng): Draft {
  const ch = pickChar(r, ["undamped", "undamped", "real", "complex", "double"]);
  let a: Sh, b: Sh;
  if (ch.type === "undamped" && r.chance(0.5)) [a, b] = [SHPI(1), SHPI(2)];
  else {
    const p = r.int(1, 3), q = p + r.int(1, 2);
    [a, b] = [SH(p), SH(q)];
  }
  const K = lcmDen(ch.h.map((u) => u.c)) * r.nz(-2, 2);
  require_(Math.abs(K) <= 20);
  const casesTex = `r(t) = \\begin{cases} ${K} & ${a.tex} < t < ${b.tex} \\\\ 0 & \\text{otherwise} \\end{cases}`;
  const kTex = K === 1 ? "" : K === -1 ? "-" : `${K}`;
  // RNG draws inside switchedDraft (initial conditions) come after every choice above
  const d = switchedDraft(r, ch, [{ sh: a, K, delta: false }, { sh: b, K: -K, delta: false }], `${kTex}\\big[u(t - ${a.tex}) - u(t - ${b.tex})\\big]`);
  return fixCases(d, r.chance(0.5), casesTex);
}

function deltaIvp(r: Rng): Draft {
  const ch = pickChar(r, ["undamped", "real", "real", "complex", "double"]);
  const sh = ch.type === "undamped" && r.chance(0.4) ? SHPI(1) : SH(r.int(1, 3));
  const K = lcmDen(ch.g.map((u) => u.c)) * r.nz(-2, 2);
  require_(Math.abs(K) <= 12);
  const forces: Force[] = [{ sh, K, delta: true }];
  let rTex = ct(K, `\\delta(t - ${sh.tex})`);
  if (ch.type === "undamped" && r.chance(0.35)) {
    // a second kick (Kreyszig's hammer blows)
    const sh2 = sh.js.includes("pi") ? SHPI(2) : SH(sh.v + r.int(1, 2));
    const K2 = lcmDen(ch.g.map((u) => u.c)) * r.nz(-2, 2);
    forces.push({ sh: sh2, K: K2, delta: true });
    rTex = join([rTex, ct(K2, `\\delta(t - ${sh2.tex})`)]);
  }
  const d = switchedDraft(r, ch, forces, rTex);
  return { ...d, prompt: d.prompt.replace(" Write unit steps as $u(t - a)$.", " Write the answer with unit steps $u(t - a)$.") };
}

function deltaResponse(r: Rng): Draft {
  const ch = pickChar(r, ["undamped", "real", "complex", "double"]);
  const A = r.pick([1, 1, 1, 2]);
  const g = scale(ch.g, new Q(1, A));
  const eq = join([ct(A, "y''"), ct(A * ch.b, "y'"), ct(A * ch.c, "y")]);
  const Gs = A === 1 ? `\\frac{1}{${charPoly(ch.b, ch.c)}}` : `\\frac{1}{${A}(${charPoly(ch.b, ch.c)})}`;
  const kick = new Q(1, A);
  return {
    prompt: `Find the impulse response ${m("g(t)")} (for ${m("t > 0")}) of ${m(`${eq} = \\delta(t)`)}, starting from rest: ${m("y(0^-) = y'(0^-) = 0")}.`,
    answer: { kind: "ode2", a: A, b: A * ch.b, c: A * ch.c, v: "t", ic: [0, 0, kick.value()], ref: sumJs(g) },
    answerTex: `g(t) = ${sumTex(g)}`,
    steps: [
      `${m(`${LT}\\{\\delta(t)\\} = 1`)} and the initial state is zero, so ${m(`${A === 1 ? "" : A}(${charPoly(ch.b, ch.c)})Y = 1`)}: ${m(`G(s) = ${Gs}`)}, the transfer function.`,
      `${m(`${charPoly(ch.b, ch.c)} = ${ch.facTex}`)}; ${m(`\\frac{1}{${ch.facTex}} = ${sSum(ch.g)}`)}.`,
      `Invert: ${m(`g(t) = ${sumTex(g)}`)}. Check: ${m("g(0) = 0")} and ${m(`g'(0^+) = ${kick.tex()}`)} — the impulse makes ${m("y'")} jump by ${m("1/a")}, ${m("a")} the leading coefficient.`,
    ],
    meta: { b: A * ch.b, c: A * ch.c, a: A, y0: 0, y1: 0, forcing: [{ type: "delta", at: "0", K: 1 }] },
  };
}

// ══ laplace.systems ═════════════════════════════════════════════════════════
function eigenSystem(r: Rng) {
  for (let tries = 0; tries < 400; tries++) {
    const a11 = r.int(-4, 4), a12 = r.nz(-4, 4), a21 = r.nz(-4, 4), a22 = r.int(-4, 4);
    const T = a11 + a22, D = a11 * a22 - a12 * a21;
    const disc = T * T - 4 * D;
    const sq = Math.round(Math.sqrt(Math.max(disc, 0)));
    if (disc <= 0 || sq * sq !== disc || (T + sq) % 2) continue;
    const l1 = (T - sq) / 2, l2 = (T + sq) / 2;
    if (l1 === 0 || l2 === 0 || Math.abs(l1) > 5 || Math.abs(l2) > 5) continue;
    const vec = (l: number): [number, number] => {
      let v: [number, number] = [a12, l - a11];
      const g = gcd(v[0], v[1]);
      v = [v[0] / g, v[1] / g];
      return v[0] < 0 || (v[0] === 0 && v[1] < 0) ? [-v[0], -v[1]] : v;
    };
    return { A: [[a11, a12], [a21, a22]], l1, l2, v1: vec(l1), v2: vec(l2) };
  }
  require_(false);
  throw new Error("unreachable");
}

function systemDraft(r: Rng, forced: boolean): Draft {
  const { A, l1, l2, v1, v2 } = eigenSystem(r);
  const al = r.nz(-3, 3), be = r.nz(-3, 3);
  const p: [number, number] = forced ? [r.int(-3, 3), r.int(-3, 3)] : [0, 0];
  require_(!forced || p[0] !== 0 || p[1] !== 0);
  const g = forced ? [-(A[0][0] * p[0] + A[0][1] * p[1]), -(A[1][0] * p[0] + A[1][1] * p[1])] : [0, 0];
  const ic = [p[0] + al * v1[0] + be * v2[0], p[1] + al * v1[1] + be * v2[1]];
  require_(Math.abs(ic[0]) <= 12 && Math.abs(ic[1]) <= 12);
  const comp = (i: 0 | 1): Tm[] =>
    [tm(p[i], "exp"), tm(al * v1[i], "exp", l1), tm(be * v2[i], "exp", l2)].filter((u) => !u.c.isZero());
  const ys = [comp(0), comp(1)];
  const rowTex = (i: 0 | 1) => `y_${i + 1}' = ${join([ct(A[i][0], "y_1"), ct(A[i][1], "y_2"), `${g[i]}`])}`;
  const sub = (i: 0 | 1) => {
    const own = i === 0 ? `(${linTex(A[0][0])})Y_1` : `(${linTex(A[1][1])})Y_2`;
    const other = i === 0 ? ct(-A[0][1], "Y_2") : ct(-A[1][0], "Y_1");
    const rhs = join([`${ic[i]}`, g[i] ? fr(new Q(g[i]), "1", "s") : "0"]);
    return i === 0 ? `${join([own, other])} = ${rhs}` : `${join([other, own])} = ${rhs}`;
  };
  const Dtex = `(${linTex(l1)})(${linTex(l2)})`;
  const ans = ys.map((ts) => sumTex(ts));
  return {
    prompt: `Solve by the Laplace transform: ${m(rowTex(0))}, ${m(rowTex(1))}, ${m(`y_1(0) = ${ic[0]},\\ y_2(0) = ${ic[1]}`)}.`,
    answer: {
      kind: "tuple",
      fields: [
        { label: "y₁(t)", tex: "y_1", ref: sumJs(ys[0]), mode: "expr" },
        { label: "y₂(t)", tex: "y_2", ref: sumJs(ys[1]), mode: "expr" },
      ],
      vars: ["t"],
      system: { A, v: "t", ic: [0, ic[0], ic[1]], ...(forced ? { g: g.map((x) => `${x}`) } : {}) },
    },
    answerTex: `y_1 = ${ans[0]},\\quad y_2 = ${ans[1]}`,
    steps: [
      `Transform each equation (${m(`${LT}\\{y_j'\\} = sY_j - y_j(0)`)}${forced ? `, ${m(`${LT}\\{k\\} = k/s`)}` : ""}): ${m(sub(0))}, ${m(sub(1))}.`,
      `Coefficient determinant: ${m(`(${linTex(A[0][0])})(${linTex(A[1][1])}) - (${A[0][1]})(${A[1][0]}) = ${ptex([l1 * l2, -(l1 + l2), 1])} = ${Dtex}`)}; solve by Cramer's rule (or elimination).`,
      `Partial fractions: ${m(`Y_1 = ${sSum(ys[0])}`)}, ${m(`Y_2 = ${sSum(ys[1])}`)}.`,
      m(`y_1 = ${ans[0]},\\quad y_2 = ${ans[1]}`),
    ],
    meta: { A, g, y0: ic },
  };
}
const lsysIvp = (r: Rng) => systemDraft(r, false);
const lsysForced = (r: Rng) => systemDraft(r, true);

// ══ laplace.transfer ════════════════════════════════════════════════════════
function transferG(r: Rng): Draft {
  const v = r.int(0, 2);
  if (v === 2) {
    const tau = r.int(2, 6), K = r.nz(-5, 5);
    return {
      prompt: `A first-order element obeys ${m(`${tau}y' + y = ${ct(K, "r(t)")}`)}. With ${m("y(0) = 0")}, find its transfer function ${m("G(s) = Y(s)/R(s)")}.`,
      answer: { kind: "expression", ref: `(${K})/(${tau}*s+1)`, vars: ["s"], label: "G(s)" },
      answerTex: `G(s) = ${fr(new Q(K), "1", `${tau}s + 1`)}`,
      steps: [
        `Transform with zero initial value: ${m(`${tau}sY + Y = ${ct(K, "R")}`)}.`,
        `${m(`G = \\frac{Y}{R} = ${fr(new Q(K), "1", `${tau}s + 1`)}`)} (gain ${m(`${K}`)}, time constant ${m(`${tau}`)}).`,
      ],
      meta: { den: [1, tau], num: [K] },
    };
  }
  const a = r.pick([1, 1, 2, 3]), b = r.int(0, 6), c = r.int(1, 10);
  const den: Poly = [c, b, a];
  const d = r.int(1, 5);
  const num: Poly = v === 0 ? [1] : [d, 1];
  const lhs = join([ct(a, "y''"), ct(b, "y'"), ct(c, "y")]);
  const rhs = v === 0 ? "r(t)" : `r'(t) + ${d}r(t)`;
  const G = `\\frac{${ptex(num)}}{${ptex(den)}}`;
  return {
    prompt: `For ${m(`${lhs} = ${rhs}`)} with all initial values zero, find the transfer function ${m("G(s) = Y(s)/R(s)")}.`,
    answer: { kind: "expression", ref: `${pjs(num)}/${pjs(den)}`, vars: ["s"], label: "G(s)" },
    answerTex: `G(s) = ${G}`,
    steps: [
      `Zero initial values: ${m("\\mathcal{L}\\{y'\\} = sY")}, ${m("\\mathcal{L}\\{y''\\} = s^{2}Y")}${v ? `, ${m("\\mathcal{L}\\{r'\\} = sR")}` : ""}.`,
      `${m(`(${ptex(den)})Y = ${v ? `(${ptex(num)})R` : "R"}`)}.`,
      m(`G(s) = \\frac{Y}{R} = ${G}`),
    ],
    meta: { den, num },
  };
}

function transferPoles(r: Rng): Draft {
  const p1 = r.int(-5, 3), p2 = r.int(-5, 3);
  require_(p1 < p2);
  const den = pmul([-p1, 1], [-p2, 1]);
  const z = r.int(-5, 5);
  require_(z !== -p1 && z !== -p2);
  const K = r.nz(-4, 4);
  const num: Poly = r.chance(0.5) ? [K] : [K * z, K];
  const asOde = r.chance(0.4) && num.length === 1;
  const prompt = asOde
    ? `Find the poles of the transfer function of ${m(`${charEq(den[1], den[0])} = ${ct(K, "r(t)")}`)}.`
    : `Find the poles of ${m(`G(s) = \\frac{${ptex(num)}}{${ptex(den)}}`)}.`;
  const stable = p2 < 0;
  return {
    prompt,
    answer: { kind: "roots", ref: [p1, p2], label: "poles" },
    answerTex: `s = ${p1},\\ ${p2}`,
    steps: [
      ...(asOde ? [`Zero initial values: ${m(`G(s) = \\frac{${K}}{${ptex(den)}}`)}.`] : []),
      `Poles are the roots of the denominator: ${m(`${ptex(den)} = (${linTex(p1)})(${linTex(p2)}) = 0`)}${num.length > 1 ? ` (the zero ${m(`s = ${-z}`)} does not cancel either)` : ""}.`,
      `${m(`s = ${p1},\\ ${p2}`)} — ${stable ? "both in the left half-plane, so the system is stable." : "one is not in the left half-plane, so the system is not stable."}`,
    ],
    meta: { den, num },
  };
}

const STAB = [
  "Stable — every pole has negative real part",
  "Marginally stable — simple poles on the imaginary axis, none to the right",
  "Unstable — a pole with positive real part, or a repeated pole on the imaginary axis",
];
function transferStable(r: Rng): Draft {
  // factors: [poly, tex, poles (re, multiplicity 1)]
  type F = { p: Poly; tex: string; re: number[]; im0: boolean[] };
  const fac = (): F => {
    const v = r.int(0, 5);
    const a = r.int(1, 4), w = r.int(1, 3);
    switch (v) {
      case 0: return { p: [a, 1], tex: `(s + ${a})`, re: [-a], im0: [true] };
      case 1: return { p: [-a, 1], tex: `(s - ${a})`, re: [a], im0: [true] };
      case 2: return { p: [0, 1], tex: "s", re: [0], im0: [true] };
      case 3: return { p: [w * w, 0, 1], tex: `(s^{2} + ${w * w})`, re: [0, 0], im0: [false, false] };
      case 4: return { p: [a * a + w * w, 2 * a, 1], tex: `(${quadTex(-a, w)})`, re: [-a, -a], im0: [false, false] };
      default: return { p: [a * a + w * w, -2 * a, 1], tex: `(${quadTex(a, w)})`, re: [a, a], im0: [false, false] };
    }
  };
  const [f1, f2] = [fac(), fac()].sort((p, q) => (p.tex === "s" ? -1 : q.tex === "s" ? 1 : 0));
  const den = pmul(f1.p, f2.p);
  const sameImag = f1.tex === f2.tex && f1.re.every((x) => x === 0);
  const res = [...f1.re, ...f2.re];
  const type = res.some((x) => x > 0) || sameImag ? 2 : res.some((x) => x === 0) ? 1 : 0;
  const K = r.nz(1, 6);
  const Dtex = f1.tex === f2.tex ? `${f1.tex}^{2}` : `${f1.tex}${f2.tex}`;
  return {
    prompt: `Classify the stability of the system with transfer function ${m(`G(s) = \\frac{${K}}{${Dtex}}`)}.`,
    answer: { kind: "choice", options: STAB, correct: STAB[type] },
    answerTex: `\\text{${["Stable", "Marginally stable", "Unstable"][type]}}`,
    steps: [
      `Poles = roots of the denominator: ${[f1, f2].map((f) => m(`${f.tex.replace(/^\(|\)$/g, "")} = 0`)).join(", ")}.`,
      `Real parts: ${m(res.join(",\\ "))}${sameImag ? ` — the imaginary-axis pair is repeated` : ""}.`,
      [
        "All in the open left half-plane: every mode decays.",
        "Simple poles on the imaginary axis (and none to the right): bounded, non-decaying modes.",
        sameImag ? "A repeated pole on the imaginary axis gives a growing t·cos/t·sin (or t) mode." : "A pole in the right half-plane gives a growing mode.",
      ][type],
    ],
    meta: { den, type },
  };
}

// ══ laplace.t-multiply  (L{t f} = −F′) ═══════════════════════════════════════
function tmulForward(r: Rng): Draft {
  const v = r.int(0, 3), A = r.pick([1, 1, 2, 3, -1, -2]);
  const w = r.int(1, 4), k = r.nz(-3, 3);
  const pre = A === 1 ? "" : A === -1 ? "-" : `${A}`;
  let fTex: string, fJs: string, F0: string, Ftex: string, Fjs: string;
  if (v === 0) {
    fTex = `${pre}t\\sin ${w === 1 ? "" : w}t`; fJs = `(${A})*t*sin(${w}*t)`;
    F0 = `\\frac{${w}}{s^{2} + ${w * w}}`;
    Ftex = fr(new Q(2 * w * A), "s", `(s^{2} + ${w * w})^{2}`); Fjs = `(${2 * w * A})*s/(s^2+${w * w})^2`;
  } else if (v === 1) {
    fTex = `${pre}t\\cos ${w === 1 ? "" : w}t`; fJs = `(${A})*t*cos(${w}*t)`;
    F0 = `\\frac{s}{s^{2} + ${w * w}}`;
    Ftex = fr(new Q(A), `s^{2} - ${w * w}`, `(s^{2} + ${w * w})^{2}`); Fjs = `(${A})*(s^2-${w * w})/(s^2+${w * w})^2`;
  } else if (v === 2) {
    fTex = `${pre}te^{${ct(k, "t")}}\\sin ${w === 1 ? "" : w}t`; fJs = `(${A})*t*exp((${k})*t)*sin(${w}*t)`;
    F0 = `\\frac{${w}}{${quadTex(k, w)}}`;
    Ftex = fr(new Q(2 * w * A), linTex(k), `\\left[${quadTex(k, w)}\\right]^{2}`);
    Fjs = `(${2 * w * A})*(s-(${k}))/((s-(${k}))^2+${w * w})^2`;
  } else {
    const a = r.int(1, 3);
    fTex = `${pre}t\\sinh ${a === 1 ? "" : a}t`; fJs = `(${A})*t*sinh(${a}*t)`;
    F0 = `\\frac{${a}}{s^{2} - ${a * a}}`;
    Ftex = fr(new Q(2 * a * A), "s", `(s^{2} - ${a * a})^{2}`); Fjs = `(${2 * a * A})*s/(s^2-${a * a})^2`;
  }
  return {
    prompt: `Use ${m(`${LT}\\{tf(t)\\} = -F'(s)`)} to find ${m(`${LT}\\{${fTex}\\}`)}.`,
    answer: { kind: "expression", ref: Fjs, vars: ["s"], label: "F(s)" },
    answerTex: `${LT}\\{${fTex}\\} = ${Ftex}`,
    steps: [
      `Without the factor ${m("t")}: ${m(`F(s) = ${A === 1 ? "" : A === -1 ? "-" : A}${F0}`)}.`,
      `Differentiate in ${m("s")} (quotient rule) and change the sign: ${m(`-F'(s) = ${Ftex}`)}.`,
    ],
    meta: { f: fJs },
  };
}

function tmulInverse(r: Rng): Draft {
  const v = r.int(0, 3);
  let Ftex: string, Fjs: string, fTex: string, fJs: string, dF: string;
  if (v === 0) {
    const a = r.int(-3, 3), b = r.int(-3, 3);
    require_(a !== b);
    Ftex = `\\ln\\frac{${linTex(a)}}{${linTex(b)}}`;
    Fjs = `log((s-(${a}))/(s-(${b})))`;
    dF = `-F'(s) = ${fr(new Q(1), "1", linTex(b))} - ${fr(new Q(1), "1", linTex(a))}`;
    const ea = a === 0 ? "1" : `e^{${ct(a, "t")}}`, eb = b === 0 ? "1" : `e^{${ct(b, "t")}}`;
    fTex = `\\frac{${eb} - ${ea}}{t}`;
    fJs = `(exp((${b})*t) - exp((${a})*t))/t`;
  } else if (v === 1) {
    const w = r.int(1, 4);
    Ftex = `\\arctan\\frac{${w}}{s}`;
    Fjs = `atan(${w}/s)`;
    dF = `-F'(s) = \\frac{${w}}{s^{2} + ${w * w}}`;
    fTex = `\\frac{\\sin ${w === 1 ? "" : w}t}{t}`;
    fJs = `sin(${w}*t)/t`;
  } else if (v === 2) {
    const w = r.int(1, 4);
    Ftex = `\\ln\\left(1 + \\frac{${w * w}}{s^{2}}\\right)`;
    Fjs = `log(1 + ${w * w}/s^2)`;
    dF = `-F'(s) = \\frac{2}{s} - \\frac{2s}{s^{2} + ${w * w}}`;
    fTex = `\\frac{2(1 - \\cos ${w === 1 ? "" : w}t)}{t}`;
    fJs = `2*(1 - cos(${w}*t))/t`;
  } else {
    const a = r.int(1, 4), b = r.int(1, 4);
    require_(a !== b);
    Ftex = `\\ln\\frac{s^{2} + ${a * a}}{s^{2} + ${b * b}}`;
    Fjs = `log((s^2+${a * a})/(s^2+${b * b}))`;
    dF = `-F'(s) = \\frac{2s}{s^{2} + ${b * b}} - \\frac{2s}{s^{2} + ${a * a}}`;
    fTex = `\\frac{2(\\cos ${b === 1 ? "" : b}t - \\cos ${a === 1 ? "" : a}t)}{t}`;
    fJs = `2*(cos(${b}*t) - cos(${a}*t))/t`;
  }
  return {
    prompt: `Find ${m(`f(t) = ${LT}^{-1}\\left\\{${Ftex}\\right\\}`)}. (Differentiate first: ${m(`${LT}\\{tf(t)\\} = -F'(s)`)}.)`,
    answer: { kind: "expression", ref: fJs, vars: ["t"], label: "f(t)", points: [0.23, 0.61, 0.97, 1.34, 1.71, 2.28, 2.63].map((t) => ({ t })) },
    answerTex: `f(t) = ${fTex}`,
    steps: [
      `${m("F")} itself is not in the table, but its derivative is rational: ${m(dF)}.`,
      `So ${m(`t\\,f(t) = ${LT}^{-1}\\{-F'\\} = ${fTex.replace(/^\\frac\{(.*)\}\{t\}$/, "$1")}`)}.`,
      `Divide by ${m("t")}: ${m(`f(t) = ${fTex}`)}.`,
    ],
    meta: { F: Fjs },
  };
}

// ══ pde.classify ════════════════════════════════════════════════════════════
const TYPES = ["Elliptic", "Parabolic", "Hyperbolic"];
function pdeClassify(r: Rng): Draft {
  const v = r.int(0, 3);
  if (v === 3) {
    // Tricomi-type: y u_xx + u_yy = 0 (type depends on the half-plane)
    const neg = r.chance(0.5);
    const k = r.pick([1, 1, 2, 3]);
    const which = r.chance(0.5) ? "x" : "y";
    const eq = which === "y" ? `${ct(k, "y")}u_{xx} + u_{yy} = 0` : `u_{xx} + ${ct(k, "x")}u_{yy} = 0`;
    const type = neg ? 2 : 0;
    return {
      prompt: `Classify ${m(eq)} in the half-plane ${m(`${which} ${neg ? "<" : ">"} 0`)}.`,
      answer: { kind: "choice", options: TYPES, correct: TYPES[type] },
      answerTex: `\\text{${TYPES[type]}}`,
      steps: [
        `Kreyszig: ${m("Au_{xx} + 2Bu_{xy} + Cu_{yy} = F")} is elliptic if ${m("AC - B^{2} > 0")}, parabolic if ${m("= 0")}, hyperbolic if ${m("< 0")}. The coefficients may depend on position.`,
        `Here ${m(which === "y" ? `A = ${ct(k, "y")},\\ B = 0,\\ C = 1` : `A = 1,\\ B = 0,\\ C = ${ct(k, "x")}`)}: ${m(`AC - B^{2} = ${ct(k, which)}`)}, which is ${neg ? "negative" : "positive"} for ${m(`${which} ${neg ? "<" : ">"} 0`)}.`,
        `${TYPES[type]}.`,
      ],
      meta: { A: which === "y" ? `${k}*y` : "1", Bxy: "0", C: which === "y" ? "1" : `${k}*x`, pt: which === "y" ? { x: 0.5, y: neg ? -1 : 1 } : { x: neg ? -1 : 1, y: 0.5 }, type },
    };
  }
  const xv = r.chance(0.3) ? "t" : "y";
  let A: number, Bxy: number, C: number;
  if (v === 1) {
    const p = r.int(1, 3), q = r.int(1, 3);
    A = p * p; C = q * q; Bxy = 2 * p * q * r.pick([1, -1]);
  } else {
    A = r.nz(-4, 4); C = r.nz(-4, 4); Bxy = r.int(-6, 6);
    require_(Bxy * Bxy !== 4 * A * C);
  }
  const disc = Bxy * Bxy - 4 * A * C;
  const type = disc > 0 ? 2 : disc === 0 ? 1 : 0;
  const lower = r.chance(0.5) ? [ct(r.int(-3, 3), "u_x"), ct(r.int(-3, 3), `u_${xv}`), ct(r.int(-3, 3), "u")] : [];
  const eq = `${join([ct(A, "u_{xx}"), ct(Bxy, `u_{x${xv}}`), ct(C, `u_{${xv}${xv}}`), ...lower])} = 0`;
  const B = new Q(Bxy, 2);
  const AC = new Q(A * C).sub(B.mul(B));
  return {
    prompt: `Classify the PDE ${m(eq)}.`,
    answer: { kind: "choice", options: TYPES, correct: TYPES[type] },
    answerTex: `\\text{${TYPES[type]}}`,
    steps: [
      `Compare with ${m(`Au_{xx} + 2Bu_{x${xv}} + Cu_{${xv}${xv}} = F`)} (lower-order terms don't matter): ${m(`A = ${A},\\ 2B = ${Bxy},\\ C = ${C}`)}, so ${m(`B = ${B.tex()}`)}.`,
      `${m(`AC - B^{2} = ${A * C} - ${B.mul(B).tex()} = ${AC.tex()}`)}: ${["positive", "zero", "negative"][type]}.`,
      `${TYPES[type]} (${m(["AC - B^{2} > 0", "AC - B^{2} = 0", "AC - B^{2} < 0"][type])}).`,
    ],
    meta: { A: `${A}`, Bxy: `${Bxy}`, C: `${C}`, pt: {}, type },
  };
}

function pdeVerify(r: Rng): Draft {
  const v = r.int(0, 4);
  const sinT = (k: number, x: string) => `\\sin ${k === 1 ? "" : k}${x}`;
  const cosT = (k: number, x: string) => `\\cos ${k === 1 ? "" : k}${x}`;
  let prompt: string, ref: string, ansTex: string, steps: string[], meta: Record<string, unknown>;
  if (v === 0) {
    const c2 = r.int(1, 4), mm = r.int(1, 3), A = r.nz(-4, 4);
    const k = c2 * mm * mm;
    const fn = r.pick(["sin", "cos"]);
    const uTex = `${ct(A, `e^{-${k === 1 ? "" : k}t}`)}${fn === "sin" ? sinT(mm, "x") : cosT(mm, "x")}`;
    prompt = `For which constant ${m("c^{2}")} does ${m(`u = ${uTex}`)} solve the heat equation ${m("u_t = c^{2}u_{xx}")}?`;
    ref = `${c2}`; ansTex = `c^{2} = ${c2}`;
    steps = [`${m(`u_t = ${-k}u`)} and ${m(`u_{xx} = ${-mm * mm}u`)}.`, `${m(`${-k}u = c^{2}(${-mm * mm}u)`)}, so ${m(`c^{2} = ${k}/${mm * mm} = ${c2}`)}.`];
    meta = { u: `(${A})*exp(-${k}*t)*${fn}(${mm}*x)`, op: "heat", c2: "K", vars: ["x", "t"] };
  } else if (v === 1) {
    const c2 = r.int(1, 4), mm = r.int(1, 3), A = r.nz(-4, 4);
    const k = c2 * mm * mm;
    prompt = `For which decay rate ${m("k")} does ${m(`u = ${ct(A, "e^{-kt}")}${sinT(mm, "x")}`)} solve ${m(`u_t = ${c2 === 1 ? "" : c2}u_{xx}`)}?`;
    ref = `${k}`; ansTex = `k = ${k}`;
    steps = [`${m("u_t = -ku")}, ${m(`u_{xx} = ${-mm * mm}u`)}.`, `${m(`-k = ${c2}\\cdot(${-mm * mm})`)}: ${m(`k = ${k}`)}.`];
    meta = { u: `(${A})*exp(-K*t)*sin(${mm}*x)`, op: "heat", c2: `${c2}`, vars: ["x", "t"] };
  } else if (v === 2) {
    const c = r.int(1, 4), mm = r.int(1, 3);
    const w = c * mm;
    if (r.chance(0.5)) {
      prompt = `For which ${m("c^{2}")} does ${m(`u = ${sinT(mm, "x")}${cosT(w, "t")}`)} solve the wave equation ${m("u_{tt} = c^{2}u_{xx}")}?`;
      steps = [`${m(`u_{tt} = ${-w * w}u`)}, ${m(`u_{xx} = ${-mm * mm}u`)}.`, `${m(`c^{2} = ${w * w}/${mm * mm} = ${c * c}`)}.`];
      meta = { u: `sin(${mm}*x)*cos(${w}*t)`, op: "wave", c2: "K", vars: ["x", "t"] };
    } else {
      const p = r.int(2, 3);
      const sgn = r.pick(["-", "+"]);
      prompt = `For which ${m("c^{2}")} does ${m(`u = (x ${sgn} ${c === 1 ? "" : c}t)^{${p}}`)} solve ${m("u_{tt} = c^{2}u_{xx}")}?`;
      steps = [`Any ${m(`f(x ${sgn} vt)`)} gives ${m("u_{tt} = v^{2}f''")}, ${m("u_{xx} = f''")}: a wave moving at speed ${m("v")}.`, `${m(`v = ${c}`)}, so ${m(`c^{2} = ${c * c}`)}.`];
      meta = { u: `(x ${sgn} ${c}*t)^${p}`, op: "wave", c2: "K", vars: ["x", "t"] };
    }
    ref = `${c * c}`; ansTex = `c^{2} = ${c * c}`;
  } else if (v === 3) {
    const a = r.nz(-3, 3);
    if (r.chance(0.5)) {
      prompt = `For which ${m("k")} is ${m(`u = ${ct(a, "x^{3}")} + kxy^{2}`)} harmonic (${m("u_{xx} + u_{yy} = 0")})?`;
      ref = `${-3 * a}`; ansTex = `k = ${-3 * a}`;
      steps = [`${m(`u_{xx} = ${6 * a}x`)}, ${m("u_{yy} = 2kx")}.`, `${m(`${6 * a}x + 2kx = 0`)}: ${m(`k = ${-3 * a}`)}.`];
      meta = { u: `(${a})*x^3 + K*x*y^2`, op: "laplace", vars: ["x", "y"] };
    } else {
      const A3 = 3 * a;
      prompt = `For which ${m("k")} is ${m(`u = ${ct(A3, "x^{2}y")} + ky^{3}`)} harmonic (${m("u_{xx} + u_{yy} = 0")})?`;
      ref = `${-a}`; ansTex = `k = ${-a}`;
      steps = [`${m(`u_{xx} = ${2 * A3}y`)}, ${m("u_{yy} = 6ky")}.`, `${m(`${2 * A3}y + 6ky = 0`)}: ${m(`k = ${-a}`)}.`];
      meta = { u: `(${A3})*x^2*y + K*y^3`, op: "laplace", vars: ["x", "y"] };
    }
  } else {
    const mm = r.int(1, 4);
    const fn = r.pick(["sin", "cos"]);
    prompt = `For which ${m("k > 0")} is ${m(`u = e^{${mm === 1 ? "" : mm}x}\\${fn} ky`)} harmonic (${m("u_{xx} + u_{yy} = 0")})?`;
    ref = `${mm}`; ansTex = `k = ${mm}`;
    steps = [`${m(`u_{xx} = ${mm * mm}u`)}, ${m("u_{yy} = -k^{2}u")}.`, `${m(`${mm * mm} - k^{2} = 0`)}, ${m(`k = ${mm}`)} (the positive root).`];
    meta = { u: `exp(${mm}*x)*${fn}(K*y)`, op: "laplace", vars: ["x", "y"], positive: true };
  }
  return {
    prompt,
    answer: { kind: "expression", ref, vars: [], label: ansTex.split(" =")[0] },
    answerTex: ansTex,
    steps: [...steps, "Substitute back to check: the residual vanishes identically."],
    meta,
  };
}

// ══ pde.dalembert ═══════════════════════════════════════════════════════════
/** q as a leading factor: "" for 1, "-" for -1 */
const pre = (q: Q) => (q.n === q.d ? "" : q.n === -q.d ? "-" : q.tex());
interface Wave { tex: string; js: string; u: string; uJs: string; explain: string }
/** displacement f(x) = A·shape and its half-sum ½[f(x+ct) + f(x−ct)] */
function dispShape(r: Rng, c: number): Wave {
  const v = r.int(0, 4), A = r.pick([1, 2, 3, -1, 4]), k = r.int(1, 3);
  const P = `(x+${c}*t)`, M = `(x-${c}*t)`;
  const ctx = `${c === 1 ? "" : c}t`;
  const kx = `${k === 1 ? "" : k}x`;
  if (v === 0) return { tex: ct(A, `\\sin ${kx}`), js: `(${A})*sin(${k}*x)`, u: ct(A, `\\sin ${kx}\\cos ${k * c === 1 ? "" : k * c}t`), uJs: `(${A})/2*(sin(${k}*${P}) + sin(${k}*${M}))`, explain: `${m("\\sin\\alpha + \\sin\\beta = 2\\sin\\frac{\\alpha+\\beta}{2}\\cos\\frac{\\alpha-\\beta}{2}")}` };
  if (v === 1) return { tex: ct(A, `\\cos ${kx}`), js: `(${A})*cos(${k}*x)`, u: ct(A, `\\cos ${kx}\\cos ${k * c === 1 ? "" : k * c}t`), uJs: `(${A})/2*(cos(${k}*${P}) + cos(${k}*${M}))`, explain: `${m("\\cos\\alpha + \\cos\\beta = 2\\cos\\frac{\\alpha+\\beta}{2}\\cos\\frac{\\alpha-\\beta}{2}")}` };
  if (v === 2) return { tex: ct(A, "x^{2}"), js: `(${A})*x^2`, u: A === 1 ? `x^{2} + ${c * c}t^{2}` : `${pre(new Q(A))}(x^{2} + ${c * c}t^{2})`, uJs: `(${A})/2*(${P}^2 + ${M}^2)`, explain: `${m(`\\tfrac12[(x + ${ctx})^{2} + (x - ${ctx})^{2}] = x^{2} + ${c * c}t^{2}`)}` };
  if (v === 3) return { tex: ct(A, "e^{-x^{2}}"), js: `(${A})*exp(-x^2)`, u: `${pre(new Q(A, 2))}\\left[e^{-(x + ${ctx})^{2}} + e^{-(x - ${ctx})^{2}}\\right]`, uJs: `(${A})/2*(exp(-${P}^2) + exp(-${M}^2))`, explain: "two Gaussian bumps of half height, moving apart" };
  return { tex: `\\frac{${A}}{1 + x^{2}}`, js: `(${A})/(1+x^2)`, u: `${pre(new Q(A, 2))}\\left[\\frac{1}{1 + (x + ${ctx})^{2}} + \\frac{1}{1 + (x - ${ctx})^{2}}\\right]`, uJs: `(${A})/2*(1/(1+${P}^2) + 1/(1+${M}^2))`, explain: "two half-height bumps, one moving left and one right" };
}
/** velocity g(x) = B·shape and its term (1/2c)∫_{x−ct}^{x+ct} g */
function velShape(r: Rng, c: number): Wave {
  const v = r.int(0, 4), B = r.pick([1, 2, 3, -1, -2, 4]), k = r.int(1, 3);
  const P = `(x+${c}*t)`, M = `(x-${c}*t)`;
  const kx = `${k === 1 ? "" : k}x`;
  const kct = `${k * c === 1 ? "" : k * c}t`;
  const amp = new Q(B, c * k);
  if (v === 0) return { tex: ct(B, `\\cos ${kx}`), js: `(${B})*cos(${k}*x)`, u: qterm(amp, `\\cos ${kx}\\sin ${kct}`), uJs: `(${B})/(2*${c}*${k})*(sin(${k}*${P}) - sin(${k}*${M}))`, explain: `${m(`\\int\\cos ${kx}\\,dx = \\frac{\\sin ${kx}}{${k}}`)}, and ${m("\\sin\\alpha - \\sin\\beta = 2\\cos\\frac{\\alpha+\\beta}{2}\\sin\\frac{\\alpha-\\beta}{2}")}` };
  if (v === 1) return { tex: ct(B, `\\sin ${kx}`), js: `(${B})*sin(${k}*x)`, u: qterm(amp, `\\sin ${kx}\\sin ${kct}`), uJs: `(${B})/(2*${c}*${k})*(cos(${k}*${M}) - cos(${k}*${P}))`, explain: `${m(`\\int\\sin ${kx}\\,dx = -\\frac{\\cos ${kx}}{${k}}`)}, and ${m("\\cos\\beta - \\cos\\alpha = 2\\sin\\frac{\\alpha+\\beta}{2}\\sin\\frac{\\alpha-\\beta}{2}")}` };
  if (v === 2) return { tex: `${B}`, js: `${B}`, u: ct(B, "t"), uJs: `(${B})*t`, explain: `${m(`\\frac{1}{${2 * c}}\\int_{x - ${c === 1 ? "" : c}t}^{x + ${c === 1 ? "" : c}t} ${B}\\,ds = ${ct(B, "t")}`)}: the whole string moves rigidly` };
  if (v === 3) return { tex: ct(B, "x"), js: `(${B})*x`, u: ct(B, "xt"), uJs: `(${B})/(4*${c})*(${P}^2 - ${M}^2)`, explain: `${m(`\\frac{1}{${2 * c}}\\cdot\\frac{${B}}{2}\\left[(x + ${c === 1 ? "" : c}t)^{2} - (x - ${c === 1 ? "" : c}t)^{2}\\right] = ${ct(B, "xt")}`)}` };
  return { tex: ct(B, "xe^{-x^{2}}"), js: `(${B})*x*exp(-x^2)`, u: `${pre(new Q(B, 4 * c))}\\left[e^{-(x - ${c === 1 ? "" : c}t)^{2}} - e^{-(x + ${c === 1 ? "" : c}t)^{2}}\\right]`, uJs: `(${B})/(4*${c})*(exp(-${M}^2) - exp(-${P}^2))`, explain: `${m("\\int xe^{-x^{2}}dx = -\\tfrac12e^{-x^{2}}")}` };
}
const dalPts = [0.2, 0.45, 0.7, 0.95, 1.2, 1.45, 1.7].map((t, i) => ({ x: -1.3 + 0.55 * i, t: t * 0.8 }));

function dalembert(r: Rng, velocity: boolean): Draft {
  const c = r.int(1, 3);
  const withF = !velocity || r.chance(0.4);
  const f = withF ? dispShape(r, c) : null;
  const g = velocity ? velShape(r, c) : null;
  const u = join([f ? f.u : "0", g ? g.u : "0"]);
  const uJs = [f ? f.uJs : "", g ? g.uJs : ""].filter(Boolean).join(" + ");
  const eq = `u_{tt} = ${c === 1 ? "" : c * c}u_{xx}`;
  return {
    prompt: `Solve ${m(eq)} on ${m("-\\infty < x < \\infty")} with ${m(`u(x,0) = ${f ? f.tex : "0"}`)} and ${m(`u_t(x,0) = ${g ? g.tex : "0"}`)}.`,
    answer: { kind: "expression", ref: uJs, vars: ["x", "t"], label: "u(x,t)", points: dalPts },
    answerTex: `u(x,t) = ${u}`,
    steps: [
      `d'Alembert (${m(`c = ${c}`)}): ${m("u = \\tfrac12[f(x + ct) + f(x - ct)] + \\frac{1}{2c}\\int_{x - ct}^{x + ct} g(s)\\,ds")}.`,
      ...(f ? [`Displacement part: ${m(`\\tfrac12[f(x + ${c === 1 ? "" : c}t) + f(x - ${c === 1 ? "" : c}t)]`)} — ${f.explain}: ${m(f.u)}.`] : []),
      ...(g ? [`Velocity part: ${g.explain}: ${m(g.u)}.`] : [`${m("g = 0")}: no integral term.`]),
      m(`u(x,t) = ${u}`),
    ],
    meta: { c2: c * c, f: f ? f.js : "0", g: g ? g.js : "0" },
  };
}
const dalDisp = (r: Rng) => dalembert(r, false);
const dalVel = (r: Rng) => dalembert(r, true);

// ══ pde.laplace-rect ════════════════════════════════════════════════════════
interface Len { v: number; tex: string; js: string; pi: boolean; n: number }
const lenPick = (r: Rng, opts: (number | "pi")[]): Len => {
  const c = r.pick(opts);
  return c === "pi" ? { v: Math.PI, tex: "\\pi", js: "pi", pi: true, n: 1 } : { v: c, tex: `${c}`, js: `${c}`, pi: false, n: c };
};
/** k·π·X/L as LaTeX, X a variable ("x", "(2 - y)") or a length; k = "n" or a mode number */
function arg(k: number | "n", X: string | Len, L: Len): string {
  const q = typeof X === "string" ? new Q(typeof k === "number" ? k : 1, L.n) : new Q((typeof k === "number" ? k : 1) * X.n, L.n);
  const pis = 1 + (typeof X !== "string" && X.pi ? 1 : 0) - (L.pi ? 1 : 0);
  const piS = pis === 0 ? "" : pis === 1 ? "\\pi" : "\\pi^{2}";
  const v = `${k === "n" ? "n" : ""}${piS}${typeof X === "string" ? (piS ? ` ${X}` : X) : ""}`;
  if (q.d === 1) return v ? qterm(q, v) : `${q.n}`;
  return `\\frac{${qterm(new Q(q.n), v || "1")}}{${q.d}}`;
}
const argJs = (k: number | string, X: string, L: Len) => `(${k})*pi*(${X})/(${L.js})`;

function laplaceModes(r: Rng): Draft {
  const a = lenPick(r, ["pi", 1, 2]), b = lenPick(r, ["pi", 1, 2]);
  const edge = r.pick(["top", "top", "right", "bottom"] as const);
  const m1 = r.int(1, 3), m2 = r.int(1, 4);
  require_(m1 < m2);
  const A1 = r.nz(-5, 5), A2 = r.chance(0.6) ? r.nz(-5, 5) : 0;
  const modes = ([[m1, A1], [m2, A2]] as [number, number][]).filter(([, A]) => A !== 0);
  // along: the variable of the data side (its eigenfunctions); across: the sinh direction
  const along = edge === "right" ? { v: "y", L: b } : { v: "x", L: a };
  const span = edge === "right" ? a : b;
  const across = edge === "right" ? "x" : edge === "top" ? "y" : `(${b.tex} - y)`;
  const acrossJs = edge === "right" ? "x" : edge === "top" ? "y" : `(${b.js} - y)`;
  const sinT = (k: number | "n") => `\\sin ${arg(k, along.v, along.L)}`;
  const dataTex = join(modes.map(([k, A]) => ct(A, sinT(k))));
  const term = (k: number, A: number) => `${ct(A, `\\frac{\\sinh ${arg(k, across, along.L)}}{\\sinh ${arg(k, span, along.L)}}`)}\\,${sinT(k)}`;
  const uTex = join(modes.map(([k, A]) => term(k, A)));
  const uJs = modes.map(([k, A]) => `(${A})*sin(${argJs(k, along.v, along.L)})*sinh(${argJs(k, acrossJs, along.L)})/sinh(${argJs(k, span.js, along.L)})`).join(" + ");
  const zero = { top: `x = 0,\\ x = ${a.tex},\\ y = 0`, right: `x = 0,\\ y = 0,\\ y = ${b.tex}`, bottom: `x = 0,\\ x = ${a.tex},\\ y = ${b.tex}` }[edge];
  const dataEq = { top: `u(x, ${b.tex})`, right: `u(${a.tex}, y)`, bottom: "u(x, 0)" }[edge];
  const third = { top: "y = 0", right: "x = 0", bottom: `y = ${b.tex}` }[edge];
  const pts = [[0.21, 0.33], [0.37, 0.71], [0.52, 0.48], [0.66, 0.19], [0.79, 0.86], [0.44, 0.92], [0.88, 0.57]].map(([fx, fy]) => ({ x: fx * a.v, y: fy * b.v }));
  const other = along.v === "x" ? "y" : "x";
  return {
    prompt: `Solve ${m("u_{xx} + u_{yy} = 0")} in the rectangle ${m(`0 < x < ${a.tex},\\ 0 < y < ${b.tex}`)} with ${m("u = 0")} on ${m(zero)} and ${m(`${dataEq} = ${dataTex}`)}.`,
    answer: { kind: "expression", ref: uJs, vars: ["x", "y"], label: "u(x,y)", points: pts },
    answerTex: `u(x,y) = ${uTex}`,
    steps: [
      `Separate ${m(`u = F(${along.v})G(${other})`)}: the zero sides ${m(`${along.v} = 0`)} and ${m(`${along.v} = ${along.L.tex}`)} make ${m("F'' + kF = 0")} a sine problem, ${m(`F_n = ${sinT("n")}`)}, and then ${m(`G_n'' = \\left(${arg("n", "", along.L) || "n"}\\right)^{2}G_n`)}.`,
      `The zero side ${m(third)} picks ${m(`G_n = \\sinh ${arg("n", across, along.L)}`)} (it vanishes there).`,
      `On the data side the series must equal a sine sum already given: each mode keeps its coefficient, divided by the value of its ${m("\\sinh")} there.`,
      m(`u(x,y) = ${uTex}`),
    ],
    meta: { a: a.js, b: b.js, edge, edgeData: modes.map(([k, A]) => `(${A})*sin(${argJs(k, along.v, along.L)})`).join(" + ") },
  };
}

function laplaceCoef(r: Rng): Draft {
  const a = lenPick(r, ["pi", 1, 2]);
  const b = a.pi ? lenPick(r, ["pi", 1]) : lenPick(r, [1, a.n]);
  const v = r.int(0, 1);
  const U = r.nz(-6, 6), k = r.nz(-3, 3);
  const fTex = v === 0 ? `${U}` : ct(k, "x");
  const fJs = v === 0 ? `${U}` : `(${k})*x`;
  const nx = arg("n", "x", a);
  const sinhB = `\\sinh ${arg("n", b, a)}`;
  const ref = v === 0
    ? `2*(${U})*(1-(-1)^n)/(n*pi*sinh(n*pi*(${b.js})/(${a.js})))`
    : `2*(${k})*(${a.js})*(-1)^(n+1)/(n*pi*sinh(n*pi*(${b.js})/(${a.js})))`;
  // (2/a)∫_0^a f sin(nπx/a) dx
  const C = v === 0 ? 2 * U : 2 * k * (a.pi ? 1 : a.n);
  const shape = v === 0 ? "(1 - (-1)^{n})" : "(-1)^{n+1}";
  const den = v === 1 && a.pi ? "n" : "n\\pi";
  const sgn = C < 0 ? "-" : "";
  const integral = `${sgn}\\frac{${Math.abs(C)}${shape}}{${den}}`;
  const ansTex = `A_n^{*} = ${sgn}\\frac{${Math.abs(C)}${shape}}{${den}\\,${sinhB}}`;
  return {
    prompt: `${m("u_{xx} + u_{yy} = 0")} in ${m(`0 < x < ${a.tex},\\ 0 < y < ${b.tex}`)}, ${m("u = 0")} on ${m(`x = 0,\\ x = ${a.tex},\\ y = 0`)}, and ${m(`u(x, ${b.tex}) = ${fTex}`)}. Separation gives ${m(`u = \\sum_{n\\ge1} A_n^{*}\\sin ${nx}\\,\\sinh ${arg("n", "y", a)}`)}. Find ${m("A_n^{*}")}.`,
    answer: { kind: "expression", ref, vars: ["n"], label: "A_n*", points: [1, 2, 3, 4, 5, 6].map((n) => ({ n })) },
    answerTex: ansTex,
    steps: [
      `At ${m(`y = ${b.tex}`)}: ${m(`\\sum_n \\big(A_n^{*}\\,${sinhB}\\big)\\sin ${nx} = ${fTex}`)} — a Fourier sine series of ${m("f")} on ${m(`(0, ${a.tex})`)}.`,
      `${m(`A_n^{*}\\,${sinhB} = \\frac{2}{${a.tex}}\\int_0^{${a.tex}} ${fTex}\\,\\sin ${nx}\\,dx = ${integral}`)}${v === 1 ? " (by parts)" : ""}.`,
      m(ansTex),
    ],
    meta: { a: a.js, b: b.js, f: fJs },
  };
}

export const LAPLACE2_TEMPLATES: Record<string, (r: Rng) => Draft> = {
  "step-ivp-on": stepOn,
  "step-ivp-pulse": stepPulse,
  "delta-ivp": deltaIvp,
  "delta-response": deltaResponse,
  "lsys-ivp": lsysIvp,
  "lsys-forced": lsysForced,
  "transfer-g": transferG,
  "transfer-poles": transferPoles,
  "transfer-stable": transferStable,
  "tmul-forward": tmulForward,
  "tmul-inverse": tmulInverse,
  "pde-classify": pdeClassify,
  "pde-verify": pdeVerify,
  "dalembert-displacement": dalDisp,
  "dalembert-velocity": dalVel,
  "laplace-rect-modes": laplaceModes,
  "laplace-rect-coef": laplaceCoef,
};
