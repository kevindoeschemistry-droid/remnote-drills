// Incropera Ch 5 (transient), 7–9 (convection), 11 (heat exchangers), 13 (radiation), Level 1.
// Same conventions as gen-heat.ts: numeric answers checked to 1%, every problem carries its
// SI inputs in `meta` (with an `ht` case name) so tests/verify/heat2.py can recompute the
// answer from the governing equation on its own. Property values are given in the prompt.
import { Rng } from "./rng";
import type { Draft } from "./types";
import { m } from "./tex";
import { require_ } from "./reject";
import { fmt } from "./gen-heat";

const SIGMA = 5.67e-8;
const PI = Math.PI;
const GRAV = 9.8;

// ── formatting ─────────────────────────────────────────────────────────────
/** a given value as written in a prompt */
const g = (x: number) => fmt(x, 4);
/** round to s significant figures (so a displayed input is exactly the value used) */
const sig = (x: number, s = 2) => Number(x.toPrecision(s));

const UNITS: Record<string, string> = {
  W: "\\mathrm{W}",
  "W/m": "\\mathrm{W/m}",
  "W/m²": "\\mathrm{W/m^2}",
  "W/m²·K": "\\mathrm{W/m^2\\cdot K}",
  "W/m·K": "\\mathrm{W/m\\cdot K}",
  "W/K": "\\mathrm{W/K}",
  "°C": "^\\circ\\mathrm{C}",
  K: "\\mathrm{K}",
  s: "\\mathrm{s}",
  h: "\\mathrm{h}",
  J: "\\mathrm{J}",
  m: "\\mathrm{m}",
  mm: "\\mathrm{mm}",
  "m²": "\\mathrm{m^2}",
  "m²/s": "\\mathrm{m^2/s}",
  "m/s": "\\mathrm{m/s}",
  "kg/s": "\\mathrm{kg/s}",
  "kg/m³": "\\mathrm{kg/m^3}",
  "J/kg·K": "\\mathrm{J/kg\\cdot K}",
  "N·s/m²": "\\mathrm{N\\cdot s/m^2}",
};
const u = (unit: string) => (unit ? `\\,${UNITS[unit] ?? `\\mathrm{${unit}}`}` : "");
const vu = (x: number, unit: string) => `${g(x)}${u(unit)}`;
/** "$sym = value unit$" */
/** "A"/"An" before a spoken number or word ("an 80-mm…", "an 11-m…") */
const an = (next: string) => (/^(8|11-|11 |18-|18 |[aeiouAEIOU])/.test(next) ? "An" : "A");

function numeric(
  val: number,
  label: string,
  labelTex: string,
  unit: string,
  steps: string[],
  meta: Record<string, unknown>,
  prompt: string
): Draft {
  require_(Number.isFinite(val) && val !== 0);
  return {
    prompt,
    answer: { kind: "expression", ref: `${val}`, vars: [], tol: 0.01, rel: true, label, unit },
    answerTex: `${labelTex} = ${fmt(val)}${u(unit)}`,
    steps,
    meta,
  };
}

// ── special functions ──────────────────────────────────────────────────────
/** J_n(x), n = 0 or 1, by its power series (accurate to ~1e-15 for x ≤ 4) */
export function besselJ(n: 0 | 1, x: number): number {
  let term = n === 0 ? 1 : x / 2;
  let s = term;
  const q = (x * x) / 4;
  for (let k = 1; k < 60; k++) {
    term *= -q / (k * (k + n));
    s += term;
    if (Math.abs(term) < 1e-18) break;
  }
  return s;
}

/** erf by its Maclaurin series (|x| ≤ 4: error < 1e-12) */
export function erf(x: number): number {
  if (x < 0) return -erf(-x);
  if (x > 5.5) return 1;
  let term = x;
  let s = x;
  for (let n = 1; n < 400; n++) {
    term *= (-x * x) / n;
    const add = term / (2 * n + 1);
    s += add;
    if (Math.abs(add) < 1e-17 * Math.abs(s)) break;
  }
  return (2 / Math.sqrt(PI)) * s;
}

/** root of f on [lo, hi] (f changes sign), by bisection to machine precision */
function bisect(f: (z: number) => number, lo: number, hi: number): number {
  let flo = f(lo);
  for (let i = 0; i < 200; i++) {
    const mid = (lo + hi) / 2;
    const fm = f(mid);
    if (fm === 0) return mid;
    if (fm < 0 === flo < 0) {
      lo = mid;
      flo = fm;
    } else hi = mid;
  }
  return (lo + hi) / 2;
}

export function erfinv(y: number): number {
  require_(y > 0 && y < 1);
  return bisect((x) => erf(x) - y, 0, 5);
}

// ═══ §5.1–5.3 lumped capacitance ═══════════════════════════════════════════
// Incropera Table A.1 (300 K)
const METALS = [
  { name: "pure copper", k: 401, rho: 8933, c: 385 },
  { name: "pure aluminum", k: 237, rho: 2702, c: 903 },
  { name: "AISI 1010 carbon steel", k: 63.9, rho: 7832, c: 434 },
  { name: "AISI 304 stainless steel", k: 14.9, rho: 7900, c: 477 },
  { name: "cartridge brass", k: 110, rho: 8530, c: 380 },
];
const COOLANTS: [number, string][] = [
  [10, "still air"], [25, "moving air"], [50, "a fan-driven air stream"], [100, "a strong air jet"],
  [250, "an oil bath"], [500, "an agitated oil bath"], [1000, "water"], [3000, "a water quench"],
];

type Shape = "sphere" | "cylinder" | "plate";
interface Body { shape: Shape; D: number; Lc: number; desc: string; LcTex: string }
function lumpBody(r: Rng, shapes: Shape[] = ["sphere", "sphere", "cylinder", "plate"]): Body {
  const shape = r.pick(shapes);
  const Dmm = r.pick([2, 3, 5, 10, 15, 20, 25, 40, 50]);
  const D = Dmm / 1000;
  if (shape === "sphere")
    return { shape, D, Lc: D / 6, desc: `${Dmm}-mm-diameter sphere`, LcTex: `L_c = \\frac{V}{A_s} = \\frac{\\pi D^3/6}{\\pi D^2} = \\frac{D}{6} = ${fmt(D / 6)}\\,\\mathrm{m}` };
  if (shape === "cylinder")
    return { shape, D, Lc: D / 4, desc: `long ${Dmm}-mm-diameter rod`, LcTex: `L_c = \\frac{V}{A_s} = \\frac{\\pi D^2L/4}{\\pi DL} = \\frac{D}{4} = ${fmt(D / 4)}\\,\\mathrm{m}` };
  return { shape, D, Lc: D / 2, desc: `${Dmm}-mm-thick plate (both faces exposed)`, LcTex: `L_c = \\frac{V}{A_s} = \\frac{At}{2A} = \\frac{t}{2} = ${fmt(D / 2)}\\,\\mathrm{m}` };
}
const matTex = (mt: { k: number; rho: number; c: number }) =>
  `${m(`k = ${vu(mt.k, "W/m·K")}`)}, ${m(`\\rho = ${vu(mt.rho, "kg/m³")}`)}, ${m(`c = ${vu(mt.c, "J/kg·K")}`)}`;

interface Lump { mat: (typeof METALS)[number]; b: Body; h: number; how: string; Bi: number; tau: number; Ti: number; Tinf: number }
function lumpSetup(r: Rng, shapes?: Shape[]): Lump {
  const mat = r.pick(METALS);
  const b = lumpBody(r, shapes);
  const [h, how] = r.pick(COOLANTS);
  const Bi = (h * b.Lc) / mat.k;
  require_(Bi < 0.1);
  const tau = (mat.rho * mat.c * b.Lc) / h;
  const Ti = r.pick([150, 200, 300, 400, 500, 600]);
  const Tinf = r.pick([20, 25, 30]);
  return { mat, b, h, how, Bi, tau, Ti, Tinf };
}
const lumpSteps = (L: Lump) => [
  `${m(L.b.LcTex)}; ${m(`Bi = \\frac{hL_c}{k} = \\frac{${L.h}\\times${fmt(L.b.Lc)}}{${g(L.mat.k)}} = ${fmt(L.Bi)} < 0.1`)}, so lumped capacitance is valid.`,
  `Time constant: ${m(`\\tau = \\frac{\\rho c L_c}{h} = \\frac{${L.mat.rho}\\times${L.mat.c}\\times${fmt(L.b.Lc)}}{${L.h}} = ${fmt(L.tau)}${u("s")}`)}.`,
];
const lumpMeta = (L: Lump, extra: Record<string, unknown>) => ({
  ht: "lumped", shape: L.b.shape, D: L.b.D, h: L.h, k: L.mat.k, rho: L.mat.rho, c: L.mat.c, Ti: L.Ti, Tinf: L.Tinf, ...extra,
});
const lumpStem = (L: Lump) =>
  `${an(L.b.desc)} ${L.b.desc} of ${L.mat.name} (${matTex(L.mat)}), initially at ${m(vu(L.Ti, "°C"))}, is suddenly placed in ${L.how} at ${m(vu(L.Tinf, "°C"))} with ${m(`h = ${vu(L.h, "W/m²·K")}`)}.`;

function lumpedBi(r: Rng): Draft {
  const mats = [...METALS, { name: "Pyrex glass", k: 1.4, rho: 2225, c: 835 }, { name: "AISI 316 stainless steel", k: 13.4, rho: 8238, c: 468 }];
  const mat = r.pick(mats);
  const b = lumpBody(r);
  const [h, how] = r.pick(COOLANTS);
  const Bi = (h * b.Lc) / mat.k;
  require_(Bi > 1e-4 && Bi < 5);
  return numeric(Bi, "Bi", "Bi", "", [
    `Characteristic length ${m(b.LcTex)} (not the radius or the full thickness).`,
    m(`Bi = \\frac{hL_c}{k} = \\frac{${h}\\times${fmt(b.Lc)}}{${g(mat.k)}} = ${fmt(Bi)}`),
    Bi < 0.1
      ? `${m("Bi < 0.1")}: the temperature inside stays nearly uniform, so the lumped-capacitance method applies.`
      : `${m("Bi \\ge 0.1")}: internal gradients matter, so lumped capacitance is not valid — use the one-term (Heisler) solution.`,
  ], { ht: "lumped", target: "Bi", shape: b.shape, D: b.D, h, k: mat.k },
  `${an(b.desc)} ${b.desc} of ${mat.name} (${m(`k = ${vu(mat.k, "W/m·K")}`)}) is cooled by ${how} with ${m(`h = ${vu(h, "W/m²·K")}`)}. Find the lumped-capacitance Biot number ${m("Bi = hL_c/k")}.`);
}

function lumpedTime(r: Rng): Draft {
  const L = lumpSetup(r);
  const frac = r.pick([0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75]);
  const T = Math.round(L.Tinf + frac * (L.Ti - L.Tinf));
  require_(T > L.Tinf + 1 && T < L.Ti - 1);
  const t = L.tau * Math.log((L.Ti - L.Tinf) / (T - L.Tinf));
  require_(t > 0.5 && t < 2e5);
  return numeric(t, "t", "t", "s", [
    ...lumpSteps(L),
    `${m("\\frac{T - T_\\infty}{T_i - T_\\infty} = e^{-t/\\tau}")}, so ${m(`t = \\tau\\ln\\frac{T_i - T_\\infty}{T - T_\\infty} = ${fmt(L.tau)}\\ln\\frac{${L.Ti} - ${L.Tinf}}{${T} - ${L.Tinf}} = ${fmt(t)}${u("s")}`)}.`,
  ], lumpMeta(L, { target: "t", T }), `${lumpStem(L)} How long until it reaches ${m(vu(T, "°C"))}? (Answer in seconds.)`);
}

function lumpedTemp(r: Rng): Draft {
  const L = lumpSetup(r);
  const t = sig(L.tau * r.pick([0.2, 0.5, 1, 1.5, 2, 3]), 2);
  require_(t >= 1);
  const T = L.Tinf + (L.Ti - L.Tinf) * Math.exp(-t / L.tau);
  return numeric(T, "T", "T", "°C", [
    ...lumpSteps(L),
    m(`T = T_\\infty + (T_i - T_\\infty)e^{-t/\\tau} = ${L.Tinf} + (${L.Ti} - ${L.Tinf})e^{-${g(t)}/${fmt(L.tau)}} = ${fmt(T)}${u("°C")}`),
  ], lumpMeta(L, { target: "T", t }), `${lumpStem(L)} Find its temperature after ${m(vu(t, "s"))}.`);
}

function lumpedQ(r: Rng): Draft {
  const L = lumpSetup(r, ["sphere"]);
  const t = sig(L.tau * r.pick([0.3, 0.5, 1, 2]), 2);
  require_(t >= 1);
  const V = (PI * L.b.D ** 3) / 6;
  const Q = L.mat.rho * V * L.mat.c * (L.Ti - L.Tinf) * (1 - Math.exp(-t / L.tau));
  return numeric(Q, "Q", "Q", "J", [
    ...lumpSteps(L),
    `Energy given up is the drop in stored energy: ${m("Q = \\rho Vc\\,(T_i - T_\\infty)\\left(1 - e^{-t/\\tau}\\right)")}, with ${m(`V = \\pi D^3/6 = ${fmt(V)}\\,\\mathrm{m^3}`)}.`,
    m(`Q = ${L.mat.rho}\\times${fmt(V)}\\times${L.mat.c}\\times${L.Ti - L.Tinf}\\left(1 - e^{-${g(t)}/${fmt(L.tau)}}\\right) = ${fmt(Q)}${u("J")}`),
  ], lumpMeta(L, { target: "Q", t }), `${lumpStem(L)} How much energy has it transferred to the fluid after ${m(vu(t, "s"))}? (Answer in J.)`);
}

// ═══ §5.5–5.6 one-term solutions ═══════════════════════════════════════════
type Geo = "wall" | "cyl" | "sph";
/** first eigenvalue: wall ζ tan ζ = Bi; cylinder ζ J₁/J₀ = Bi; sphere 1 − ζ cot ζ = Bi */
export function zeta1(geo: Geo, Bi: number): number {
  if (geo === "wall") return bisect((z) => z * Math.sin(z) - Bi * Math.cos(z), 1e-12, PI / 2);
  if (geo === "cyl") return bisect((z) => z * besselJ(1, z) - Bi * besselJ(0, z), 1e-12, 2.404825557695773);
  return bisect((z) => (1 - Bi) * Math.sin(z) - z * Math.cos(z), 1e-9, PI);
}
export function c1(geo: Geo, z: number): number {
  if (geo === "wall") return (4 * Math.sin(z)) / (2 * z + Math.sin(2 * z));
  if (geo === "cyl") {
    const j0 = besselJ(0, z), j1 = besselJ(1, z);
    return ((2 / z) * j1) / (j0 * j0 + j1 * j1);
  }
  return (4 * (Math.sin(z) - z * Math.cos(z))) / (2 * z - Math.sin(2 * z));
}
const TMATS = [
  { name: "AISI 304 stainless steel", k: 14.9, a: 3.95e-6 },
  { name: "AISI 1010 carbon steel", k: 63.9, a: 18.8e-6 },
  { name: "Pyrex glass", k: 1.4, a: 0.754e-6 },
  { name: "concrete", k: 1.4, a: 0.692e-6 },
  { name: "fireclay brick", k: 1.0, a: 0.54e-6 },
];
const EIGEN_TEX: Record<Geo, string> = {
  wall: "\\zeta_1\\tan\\zeta_1 = Bi",
  cyl: "\\zeta_1\\frac{J_1(\\zeta_1)}{J_0(\\zeta_1)} = Bi",
  sph: "1 - \\zeta_1\\cot\\zeta_1 = Bi",
};
const C1_TEX: Record<Geo, string> = {
  wall: "C_1 = \\frac{4\\sin\\zeta_1}{2\\zeta_1 + \\sin 2\\zeta_1}",
  cyl: "C_1 = \\frac{2}{\\zeta_1}\\frac{J_1(\\zeta_1)}{J_0^2(\\zeta_1) + J_1^2(\\zeta_1)}",
  sph: "C_1 = \\frac{4(\\sin\\zeta_1 - \\zeta_1\\cos\\zeta_1)}{2\\zeta_1 - \\sin 2\\zeta_1}",
};
interface OT { geo: Geo; mat: (typeof TMATS)[number]; L: number; Lmm: number; h: number; Bi: number; z: number; C: number; Ti: number; Tinf: number }
function otSetup(r: Rng, geo: Geo): OT {
  const mat = r.pick(TMATS);
  const Lmm = r.pick([10, 20, 25, 40, 50, 75, 100]);
  const L = Lmm / 1000;
  const h = r.pick([50, 100, 200, 250, 500, 1000, 2000, 5000]);
  const Bi = (h * L) / mat.k;
  require_(Bi >= 0.2 && Bi <= 50);
  const z = zeta1(geo, Bi);
  const C = c1(geo, z);
  const heating = r.chance(0.35);
  const Ti = heating ? r.pick([20, 25]) : r.pick([200, 300, 400, 500, 600]);
  const Tinf = heating ? r.pick([200, 300, 400, 500]) : r.pick([20, 25, 30]);
  return { geo, mat, L, Lmm, h, Bi, z, C, Ti, Tinf };
}
const otNoun = (o: OT) =>
  o.geo === "wall" ? `${2 * o.Lmm}-mm-thick ${o.mat.name} slab (both faces exposed)`
  : o.geo === "cyl" ? `long ${2 * o.Lmm}-mm-diameter ${o.mat.name} rod`
  : `${2 * o.Lmm}-mm-diameter ${o.mat.name} sphere`;
const otStem = (o: OT) =>
  `${an(otNoun(o))} ${otNoun(o)} (${m(`k = ${vu(o.mat.k, "W/m·K")}`)}, ${m(`\\alpha = ${vu(o.mat.a, "m²/s")}`)}), initially at ${m(vu(o.Ti, "°C"))}, is suddenly exposed to fluid at ${m(vu(o.Tinf, "°C"))} with ${m(`h = ${vu(o.h, "W/m²·K")}`)}. For this Biot number Table 5.1 gives ${m(`\\zeta_1 = ${o.z.toFixed(4)}\\,\\mathrm{rad}`)}, ${m(`C_1 = ${o.C.toFixed(4)}`)}.`;
const Lsym = (o: OT) => (o.geo === "wall" ? "L" : "r_o");
const otBiStep = (o: OT) =>
  `${m(`Bi = \\frac{h${Lsym(o)}}{k} = \\frac{${o.h}\\times${g(o.L)}}{${g(o.mat.k)}} = ${fmt(o.Bi)}`)} — with ${m(Lsym(o))} the ${o.geo === "wall" ? "half-thickness" : "outer radius"}, not ${m("V/A_s")}. ${m("Bi > 0.1")}, so lumped capacitance fails.`;
const otEigenStep = (o: OT) =>
  `${m(`\\zeta_1`)} is the first root of ${m(EIGEN_TEX[o.geo])} and ${m(C1_TEX[o.geo])}: ${m(`\\zeta_1 = ${o.z.toFixed(4)}`)}, ${m(`C_1 = ${o.C.toFixed(4)}`)}.`;
const otMeta = (o: OT, extra: Record<string, unknown>) => ({ ht: "one-term", geo: o.geo, L: o.L, k: o.mat.k, alpha: o.mat.a, h: o.h, Ti: o.Ti, Tinf: o.Tinf, ...extra });
function otTime(r: Rng, o: OT): { t: number; Fo: number } {
  const t = sig((r.pick([0.25, 0.3, 0.4, 0.5, 0.75, 1, 1.5, 2]) * o.L * o.L) / o.mat.a, 2);
  const Fo = (o.mat.a * t) / (o.L * o.L);
  require_(Fo > 0.2);
  return { t, Fo };
}
const foStep = (o: OT, t: number, Fo: number) =>
  `${m(`Fo = \\frac{\\alpha t}{${Lsym(o)}^2} = \\frac{${g(o.mat.a)}\\times${g(t)}}{${g(o.L)}^2} = ${fmt(Fo)}`)} ${m("> 0.2")}, so one term of the series is enough.`;

function otCenter(geo: Geo) {
  return (r: Rng): Draft => {
    const o = otSetup(r, geo);
    const { t, Fo } = otTime(r, o);
    const th0 = o.C * Math.exp(-o.z * o.z * Fo);
    require_(th0 > 0.03);
    const T0 = o.Tinf + th0 * (o.Ti - o.Tinf);
    const where = geo === "wall" ? "midplane" : geo === "cyl" ? "centreline" : "centre";
    return numeric(T0, "T₀", "T_0", "°C", [
      otBiStep(o),
      foStep(o, t, Fo),
      otEigenStep(o),
      m(`\\theta_0^* = C_1e^{-\\zeta_1^2Fo} = ${o.C.toFixed(4)}\\,e^{-(${o.z.toFixed(4)})^2(${fmt(Fo)})} = ${fmt(th0)}`),
      m(`T_0 = T_\\infty + \\theta_0^*(T_i - T_\\infty) = ${o.Tinf} + ${fmt(th0)}(${o.Ti} - ${o.Tinf}) = ${fmt(T0)}${u("°C")}`),
    ], otMeta(o, { target: "T0", t }), `${otStem(o)} Using the one-term approximation, find the ${where} temperature after ${m(vu(t, "s"))}.`);
  };
}

function otWallSurface(r: Rng): Draft {
  const o = otSetup(r, "wall");
  const { t, Fo } = otTime(r, o);
  const th0 = o.C * Math.exp(-o.z * o.z * Fo);
  require_(th0 > 0.03);
  const ths = th0 * Math.cos(o.z);
  const Ts = o.Tinf + ths * (o.Ti - o.Tinf);
  return numeric(Ts, "Tₛ", "T_s", "°C", [
    otBiStep(o),
    foStep(o, t, Fo),
    m(`\\theta_0^* = C_1e^{-\\zeta_1^2Fo} = ${o.C.toFixed(4)}\\,e^{-(${o.z.toFixed(4)})^2(${fmt(Fo)})} = ${fmt(th0)}`),
    `At the surface ${m("x^* = x/L = 1")}: ${m(`\\theta^* = \\theta_0^*\\cos\\zeta_1 = ${fmt(th0)}\\cos(${o.z.toFixed(4)}) = ${fmt(ths)}`)} (radians!).`,
    m(`T_s = ${o.Tinf} + ${fmt(ths)}(${o.Ti} - ${o.Tinf}) = ${fmt(Ts)}${u("°C")}`),
  ], otMeta(o, { target: "Ts", t }), `${otStem(o)} Using the one-term approximation, find the surface temperature after ${m(vu(t, "s"))}.`);
}

function otWallTime(r: Rng): Draft {
  const o = otSetup(r, "wall");
  const Fo0 = r.pick([0.3, 0.4, 0.5, 0.75, 1, 1.5]);
  const T0 = Math.round(o.Tinf + o.C * Math.exp(-o.z * o.z * Fo0) * (o.Ti - o.Tinf));
  const th0 = (T0 - o.Tinf) / (o.Ti - o.Tinf);
  require_(th0 > 0.03 && th0 < o.C);
  const Fo = Math.log(o.C / th0) / (o.z * o.z);
  require_(Fo > 0.2);
  const t = (Fo * o.L * o.L) / o.mat.a;
  return numeric(t, "t", "t", "s", [
    otBiStep(o),
    m(`\\theta_0^* = \\frac{T_0 - T_\\infty}{T_i - T_\\infty} = \\frac{${T0} - ${o.Tinf}}{${o.Ti} - ${o.Tinf}} = ${fmt(th0)}`),
    `${m("\\theta_0^* = C_1e^{-\\zeta_1^2Fo}")}, so ${m(`Fo = \\frac{1}{\\zeta_1^2}\\ln\\frac{C_1}{\\theta_0^*} = \\frac{1}{${o.z.toFixed(4)}^2}\\ln\\frac{${o.C.toFixed(4)}}{${fmt(th0)}} = ${fmt(Fo)}`)} ${m("> 0.2")}, so the one-term form was fair to use.`,
    m(`t = \\frac{Fo\\,L^2}{\\alpha} = \\frac{${fmt(Fo)}\\times${g(o.L)}^2}{${g(o.mat.a)}} = ${fmt(t)}${u("s")}`),
  ], otMeta(o, { target: "t", T0 }), `${otStem(o)} Using the one-term approximation, how long until the midplane reaches ${m(vu(T0, "°C"))}? (Answer in seconds.)`);
}

// ═══ §5.7 semi-infinite solid ══════════════════════════════════════════════
const SIMATS = [
  { name: "soil", k: 0.52, rho: 2050, c: 1840 },
  { name: "concrete", k: 1.4, rho: 2300, c: 880 },
  { name: "AISI 1010 carbon steel", k: 63.9, rho: 7832, c: 434 },
  { name: "AISI 304 stainless steel", k: 14.9, rho: 7900, c: 477 },
  { name: "Pyrex glass", k: 1.4, rho: 2225, c: 835 },
  { name: "oak (across the grain)", k: 0.17, rho: 545, c: 2385 },
];
const TIMES: [number, string][] = [
  [10, "10 s"], [30, "30 s"], [60, "1 min"], [300, "5 min"], [600, "10 min"], [1800, "30 min"], [3600, "1 h"],
  [4 * 3600, "4 h"], [12 * 3600, "12 h"], [86400, "1 day"], [3 * 86400, "3 days"], [7 * 86400, "7 days"], [30 * 86400, "30 days"],
];
const DEPTHS_MM = [2, 5, 10, 20, 50, 100, 200, 300, 500, 1000];
const depthText = (mm: number) => (mm >= 100 ? `${g(mm / 1000)} m` : `${mm} mm`);
const alphaOf = (mt: { k: number; rho: number; c: number }) => mt.k / (mt.rho * mt.c);
const siStem = (mt: (typeof SIMATS)[number], Ti: number, Ts: number) =>
  `A thick block of ${mt.name} (${matTex(mt)}), initially at ${m(vu(Ti, "°C"))} throughout, has its surface suddenly brought to and held at ${m(vu(Ts, "°C"))}. Treat it as a semi-infinite solid.`;
const alphaStep = (mt: (typeof SIMATS)[number]) =>
  m(`\\alpha = \\frac{k}{\\rho c} = \\frac{${g(mt.k)}}{${mt.rho}\\times${mt.c}} = ${fmt(alphaOf(mt))}${u("m²/s")}`);
const SURF = [-20, -15, -10, -5, 50, 80, 100, 150, 250];

function erfTemp(r: Rng): Draft {
  const mt = r.pick(SIMATS);
  const a = alphaOf(mt);
  const xmm = r.pick(DEPTHS_MM);
  const [t, tt] = r.pick(TIMES);
  const x = xmm / 1000;
  const eta = x / (2 * Math.sqrt(a * t));
  require_(eta > 0.15 && eta < 2);
  const Ti = r.pick([10, 15, 20, 25]);
  const Ts = r.pick(SURF);
  const T = Ts + (Ti - Ts) * erf(eta);
  return numeric(T, "T", "T", "°C", [
    alphaStep(mt),
    `Constant surface temperature (case 1): ${m("\\frac{T(x,t) - T_s}{T_i - T_s} = \\operatorname{erf}\\frac{x}{2\\sqrt{\\alpha t}}")}.`,
    m(`\\eta = \\frac{x}{2\\sqrt{\\alpha t}} = \\frac{${g(x)}}{2\\sqrt{${fmt(a)}\\times${g(t)}}} = ${fmt(eta)}, \\quad \\operatorname{erf}\\eta = ${erf(eta).toFixed(4)}`),
    m(`T = T_s + (T_i - T_s)\\operatorname{erf}\\eta = ${Ts} + (${Ti} - (${Ts}))(${erf(eta).toFixed(4)}) = ${fmt(T)}${u("°C")}`),
  ], { ht: "semi", target: "T", k: mt.k, rho: mt.rho, c: mt.c, Ti, Ts, x, t },
  `${siStem(mt, Ti, Ts)} Find the temperature ${depthText(xmm)} below the surface after ${tt}.`);
}

function erfFlux(r: Rng): Draft {
  const mt = r.pick(SIMATS);
  const a = alphaOf(mt);
  const [t, tt] = r.pick(TIMES.slice(0, 10));
  const Ti = r.pick([10, 15, 20, 25]);
  const Ts = r.pick(SURF);
  const q = (mt.k * (Ts - Ti)) / Math.sqrt(PI * a * t);
  return numeric(q, "q″ₛ", "q''_s", "W/m²", [
    alphaStep(mt),
    `Differentiate the erf profile at ${m("x = 0")}: ${m("q''_s = -k\\left.\\frac{\\partial T}{\\partial x}\\right|_{0} = \\frac{k(T_s - T_i)}{\\sqrt{\\pi\\alpha t}}")}.`,
    m(`q''_s = \\frac{${g(mt.k)}(${Ts} - ${Ti})}{\\sqrt{\\pi\\times${fmt(a)}\\times${g(t)}}} = ${fmt(q)}${u("W/m²")}`),
    `${q < 0 ? "Negative: heat leaves the solid through the surface. " : ""}It falls as ${m("t^{-1/2}")} — infinite at ${m("t = 0")}, which is why the model needs ${m("t > 0")}.`,
  ], { ht: "semi", target: "flux", k: mt.k, rho: mt.rho, c: mt.c, Ti, Ts, t },
  `${siStem(mt, Ti, Ts)} Find the surface heat flux into the solid ${m("q''_s")} at ${tt} (positive into the solid).`);
}

function erfDepth(r: Rng): Draft {
  const mt = r.pick(SIMATS);
  const a = alphaOf(mt);
  const [t, tt] = r.pick(TIMES);
  const eta0 = r.pick([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.2, 1.4]);
  const Ti = r.pick([10, 15, 20, 25]);
  const Ts = r.pick(SURF);
  const T = sig(Ts + (Ti - Ts) * erf(eta0), 4);
  const ratio = (T - Ts) / (Ti - Ts);
  require_(ratio > 0.05 && ratio < 0.97);
  const eta = erfinv(ratio);
  const x = 2 * eta * Math.sqrt(a * t);
  require_(x > 1e-3 && x < 5);
  const mm = x < 0.1;
  const val = mm ? x * 1000 : x;
  return numeric(val, "x", "x", mm ? "mm" : "m", [
    alphaStep(mt),
    m(`\\operatorname{erf}\\eta = \\frac{T - T_s}{T_i - T_s} = \\frac{${g(T)} - (${Ts})}{${Ti} - (${Ts})} = ${ratio.toFixed(4)}`),
    `Invert (Table B.2): ${m(`\\eta = ${eta.toFixed(4)}`)}.`,
    m(`x = 2\\eta\\sqrt{\\alpha t} = 2(${eta.toFixed(4)})\\sqrt{${fmt(a)}\\times${g(t)}} = ${fmt(x)}\\,\\mathrm{m}${mm ? ` = ${fmt(val)}${u("mm")}` : ""}`),
  ], { ht: "semi", target: "x", k: mt.k, rho: mt.rho, c: mt.c, Ti, Ts, T, t, unit: mm ? "mm" : "m" },
  `${siStem(mt, Ti, Ts)} After ${tt}, at what depth is the temperature ${m(vu(T, "°C"))}? (Answer in ${mm ? "mm" : "m"}.)`);
}

function erfTime(r: Rng): Draft {
  const mt = r.pick(SIMATS);
  const a = alphaOf(mt);
  const xmm = r.pick(DEPTHS_MM);
  const x = xmm / 1000;
  const frost = mt.name === "soil" && r.chance(0.6);
  const Ti = frost ? r.pick([5, 10, 15, 20]) : r.pick([10, 15, 20, 25]);
  const Ts = frost ? r.pick([-20, -15, -10, -5]) : r.pick(SURF);
  const T = frost ? 0 : Math.round(Ts + (Ti - Ts) * r.pick([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]));
  const ratio = (T - Ts) / (Ti - Ts);
  require_(ratio > 0.05 && ratio < 0.95);
  const eta = erfinv(ratio);
  const t = (x * x) / (4 * eta * eta * a);
  require_(t > 1 && t < 1e8);
  const hours = t >= 3600;
  const val = hours ? t / 3600 : t;
  const ask = frost
    ? `A water main is buried ${depthText(xmm)} deep. How long after the surface freezes does the soil at that depth reach ${m(vu(0, "°C"))}?`
    : `How long until the temperature ${depthText(xmm)} below the surface reaches ${m(vu(T, "°C"))}?`;
  return numeric(val, "t", "t", hours ? "h" : "s", [
    alphaStep(mt),
    m(`\\operatorname{erf}\\eta = \\frac{T - T_s}{T_i - T_s} = \\frac{${T} - (${Ts})}{${Ti} - (${Ts})} = ${ratio.toFixed(4)} \\;\\Rightarrow\\; \\eta = ${eta.toFixed(4)}`),
    `${m("\\eta = x/(2\\sqrt{\\alpha t})")}, so ${m(`t = \\frac{x^2}{4\\eta^2\\alpha} = \\frac{${g(x)}^2}{4(${eta.toFixed(4)})^2(${fmt(a)})} = ${fmt(t)}\\,\\mathrm{s}${hours ? ` = ${fmt(val)}${u("h")}` : ""}`)}.`,
  ], { ht: "semi", target: "t", k: mt.k, rho: mt.rho, c: mt.c, Ti, Ts, T, x, unit: hours ? "h" : "s" },
  `${siStem(mt, Ti, Ts)} ${ask} (Answer in ${hours ? "hours" : "seconds"}.)`);
}

function contactTemp(r: Rng): Draft {
  const pool = [
    { name: "copper", k: 401, rho: 8933, c: 385 },
    { name: "aluminum", k: 237, rho: 2702, c: 903 },
    { name: "stainless steel", k: 14.9, rho: 7900, c: 477 },
    { name: "Pyrex glass", k: 1.4, rho: 2225, c: 835 },
    { name: "oak", k: 0.17, rho: 545, c: 2385 },
    { name: "concrete", k: 1.4, rho: 2300, c: 880 },
  ];
  const A = r.pick(pool);
  const B = r.pick(pool.filter((p) => p.name !== A.name));
  const TA = r.pick([60, 80, 100, 150, 200]);
  const TB = r.pick([0, 10, 20, 25]);
  const eA = Math.sqrt(A.k * A.rho * A.c), eB = Math.sqrt(B.k * B.rho * B.c);
  const Ts = (eA * TA + eB * TB) / (eA + eB);
  return numeric(Ts, "Tₛ", "T_s", "°C", [
    `Both are semi-infinite and the interface flux must match: ${m("\\frac{k_A(T_A - T_s)}{\\sqrt{\\pi\\alpha_At}} = \\frac{k_B(T_s - T_B)}{\\sqrt{\\pi\\alpha_Bt}}")}. Time cancels; since ${m("k/\\sqrt\\alpha = \\sqrt{k\\rho c}")}, ${m("T_s = \\frac{(k\\rho c)_A^{1/2}T_A + (k\\rho c)_B^{1/2}T_B}{(k\\rho c)_A^{1/2} + (k\\rho c)_B^{1/2}}")}.`,
    m(`(k\\rho c)_A^{1/2} = ${fmt(eA)}, \\quad (k\\rho c)_B^{1/2} = ${fmt(eB)}\\ \\mathrm{W\\,s^{1/2}/m^2\\cdot K}`),
    `${m(`T_s = \\frac{${fmt(eA)}(${TA}) + ${fmt(eB)}(${TB})}{${fmt(eA)} + ${fmt(eB)}} = ${fmt(Ts)}${u("°C")}`)} — closer to the material with the larger ${m("\\sqrt{k\\rho c}")}.`,
  ], { ht: "contact-T", kA: A.k, rhoA: A.rho, cA: A.c, kB: B.k, rhoB: B.rho, cB: B.c, TA, TB },
  `A thick block of ${A.name} (${matTex(A)}) at ${m(vu(TA, "°C"))} is pressed against a thick block of ${B.name} (${matTex(B)}) at ${m(vu(TB, "°C"))}. Treating both as semi-infinite solids, find the interface temperature.`);
}

// ═══ Ch 7 external flow ════════════════════════════════════════════════════
// Incropera Table A.4 (air, 1 atm) and A.6 (saturated water)
interface Fluid { name: string; T: number; nu: number; k: number; Pr: number; mu: number; alpha?: number; cp?: number }
const AIR: Fluid[] = [
  { name: "air", T: 250, nu: 11.44e-6, k: 0.0223, Pr: 0.72, mu: 159.6e-7, alpha: 15.9e-6, cp: 1006 },
  { name: "air", T: 300, nu: 15.89e-6, k: 0.0263, Pr: 0.707, mu: 184.6e-7, alpha: 22.5e-6, cp: 1007 },
  { name: "air", T: 350, nu: 20.92e-6, k: 0.03, Pr: 0.7, mu: 208.2e-7, alpha: 29.9e-6, cp: 1009 },
  { name: "air", T: 400, nu: 26.41e-6, k: 0.0338, Pr: 0.69, mu: 230.1e-7, alpha: 38.3e-6, cp: 1014 },
  { name: "air", T: 450, nu: 32.39e-6, k: 0.0373, Pr: 0.686, mu: 250.7e-7, alpha: 47.2e-6, cp: 1021 },
];
const WATER: Fluid[] = [
  { name: "water", T: 300, nu: 0.858e-6, k: 0.613, Pr: 5.83, mu: 855e-6, cp: 4179 },
  { name: "water", T: 320, nu: 0.583e-6, k: 0.64, Pr: 3.77, mu: 577e-6, cp: 4180 },
  { name: "water", T: 340, nu: 0.429e-6, k: 0.66, Pr: 2.66, mu: 420e-6, cp: 4188 },
  { name: "water", T: 360, nu: 0.335e-6, k: 0.674, Pr: 2.02, mu: 324e-6, cp: 4203 },
];
type Prop = "nu" | "k" | "Pr" | "mu" | "alpha" | "cp";
const PROP_TEX: Record<Prop, [string, string]> = {
  nu: ["\\nu", "m²/s"], k: ["k", "W/m·K"], Pr: ["Pr", ""], mu: ["\\mu", "N·s/m²"], alpha: ["\\alpha", "m²/s"], cp: ["c_p", "J/kg·K"],
};
const props = (f: Fluid, which: Prop[]) =>
  which.map((p) => m(`${PROP_TEX[p][0]} = ${vu(f[p] as number, PROP_TEX[p][1])}`)).join(", ");
const fluidAt = (f: Fluid, which: Prop[], at = "") => `${f.name} at ${f.T} K${at} (${props(f, which)})`;
/** free-stream and surface temperatures (K) whose mean is the film temperature */
function filmPair(r: Rng, f: Fluid): [number, number, boolean] {
  const dT = r.pick([10, 20, 30, 40, 50]);
  const hot = r.chance(0.7);
  const Tinf = hot ? f.T - dT / 2 : f.T + dT / 2;
  const Ts = hot ? f.T + dT / 2 : f.T - dT / 2;
  return [Tinf, Ts, hot];
}

function plateLam(r: Rng): Draft {
  const water = r.chance(0.3);
  const f = water ? r.pick(WATER.slice(0, 2)) : r.pick(AIR);
  const U = water ? r.pick([0.05, 0.1, 0.2, 0.3, 0.5]) : r.pick([1, 2, 3, 5, 8, 10]);
  const L = r.pick([0.1, 0.2, 0.25, 0.5, 0.75, 1]);
  const Re = (U * L) / f.nu;
  require_(Re > 1e3 && Re < 5e5);
  const Nu = 0.664 * Math.sqrt(Re) * Math.cbrt(f.Pr);
  const h = (Nu * f.k) / L;
  const [Tinf, Ts] = filmPair(r, f);
  const W = r.pick([0.5, 1, 2]);
  const wantQ = r.chance(0.5);
  const q = h * L * W * (Ts - Tinf);
  const steps = [
    m(`Re_L = \\frac{u_\\infty L}{\\nu} = \\frac{${g(U)}\\times${g(L)}}{${g(f.nu)}} = ${fmt(Re)}`) + ` ${m("< 5\\times10^5")}: laminar over the whole plate.`,
    `Laminar, average (Eq. 7.31): ${m(`\\overline{Nu}_L = 0.664\\,Re_L^{1/2}Pr^{1/3} = 0.664(${fmt(Re)})^{1/2}(${g(f.Pr)})^{1/3} = ${fmt(Nu)}`)}.`,
    m(`\\bar h = \\frac{\\overline{Nu}_L\\,k}{L} = \\frac{${fmt(Nu)}\\times${g(f.k)}}{${g(L)}} = ${fmt(h)}${u("W/m²·K")}`),
  ];
  if (wantQ) steps.push(m(`q = \\bar h\\,(LW)(T_s - T_\\infty) = ${fmt(h)}(${g(L)}\\times${g(W)})(${g(Ts)} - ${g(Tinf)}) = ${fmt(q)}${u("W")}`));
  return numeric(wantQ ? q : h, wantQ ? "q" : "h̄", wantQ ? "q" : "\\bar h", wantQ ? "W" : "W/m²·K", steps,
    { ht: "plate", u: U, L, W, nu: f.nu, k: f.k, Pr: f.Pr, Ts, Tinf, target: wantQ ? "q" : "h" },
    `${f.name === "air" ? "Air" : "Water"} at ${m(vu(Tinf, "K"))} flows at ${m(vu(U, "m/s"))} parallel to a ${g(L)}-m-long, ${g(W)}-m-wide flat plate held at ${m(vu(Ts, "K"))}. Properties at the film temperature ${f.T} K: ${props(f, ["nu", "k", "Pr"])}. Find ${wantQ ? "the heat rate from the plate (one side)" : "the average convection coefficient"}.`);
}

/** A in Nu = (0.037 Re^0.8 − A) Pr^1/3, from Re_x,c = 5e5 (Eq. 7.39) */
const A_MIX = 0.037 * 5e5 ** 0.8 - 0.664 * Math.sqrt(5e5);

function plateMixed(r: Rng): Draft {
  const water = r.chance(0.3);
  const f = water ? r.pick(WATER.slice(0, 2)) : r.pick(AIR);
  const U = water ? r.pick([0.5, 1, 1.5, 2]) : r.pick([10, 15, 20, 25, 30, 40, 50]);
  const L = r.pick([1, 1.5, 2, 3, 4, 5]);
  const Re = (U * L) / f.nu;
  require_(Re > 6e5 && Re <= 1e8);
  const Nu = (0.037 * Re ** 0.8 - A_MIX) * Math.cbrt(f.Pr);
  const h = (Nu * f.k) / L;
  const [Tinf, Ts] = filmPair(r, f);
  const W = r.pick([0.5, 1, 2]);
  const wantQ = r.chance(0.4);
  const q = h * L * W * (Ts - Tinf);
  const xc = (5e5 * f.nu) / U;
  const steps = [
    `${m(`Re_L = \\frac{u_\\infty L}{\\nu} = \\frac{${g(U)}\\times${g(L)}}{${g(f.nu)}} = ${fmt(Re)}`)} ${m("> 5\\times10^5")}: laminar up to ${m(`x_c = 5\\times10^5\\nu/u_\\infty = ${fmt(xc)}\\,\\mathrm{m}`)}, turbulent after.`,
    `Mixed boundary layer (Eq. 7.38): ${m("\\overline{Nu}_L = (0.037Re_L^{4/5} - 871)Pr^{1/3}")}, where ${m("871 = 0.037Re_{x,c}^{4/5} - 0.664Re_{x,c}^{1/2}")} comes from averaging the laminar and turbulent local ${m("h_x")}.`,
    m(`\\overline{Nu}_L = (0.037(${fmt(Re)})^{4/5} - 871)(${g(f.Pr)})^{1/3} = ${fmt(Nu)}`),
    m(`\\bar h = \\frac{${fmt(Nu)}\\times${g(f.k)}}{${g(L)}} = ${fmt(h)}${u("W/m²·K")}`),
  ];
  if (wantQ) steps.push(m(`q = \\bar h\\,(LW)(T_s - T_\\infty) = ${fmt(h)}(${g(L * W)})(${g(Ts)} - ${g(Tinf)}) = ${fmt(q)}${u("W")}`));
  return numeric(wantQ ? q : h, wantQ ? "q" : "h̄", wantQ ? "q" : "\\bar h", wantQ ? "W" : "W/m²·K", steps,
    { ht: "plate", u: U, L, W, nu: f.nu, k: f.k, Pr: f.Pr, Ts, Tinf, target: wantQ ? "q" : "h" },
    `${f.name === "air" ? "Air" : "Water"} at ${m(vu(Tinf, "K"))} flows at ${m(vu(U, "m/s"))} parallel to a ${g(L)}-m-long, ${g(W)}-m-wide flat plate held at ${m(vu(Ts, "K"))}. Properties at ${f.T} K: ${props(f, ["nu", "k", "Pr"])}. Transition occurs at ${m("Re_{x,c} = 5\\times10^5")}. Find ${wantQ ? "the heat rate from the plate (one side)" : "the average convection coefficient"}.`);
}

function cylCB(r: Rng): Draft {
  const water = r.chance(0.3);
  const f = water ? r.pick(WATER) : r.pick(AIR);
  const Dmm = r.pick([5, 10, 20, 25, 50, 100]);
  const D = Dmm / 1000;
  const V = water ? r.pick([0.1, 0.25, 0.5, 1]) : r.pick([1, 2, 5, 10, 20, 30]);
  const Re = (V * D) / f.nu;
  require_(Re * f.Pr > 0.2 && Re < 1e7);
  const Nu = 0.3 + ((0.62 * Math.sqrt(Re) * Math.cbrt(f.Pr)) / (1 + (0.4 / f.Pr) ** (2 / 3)) ** 0.25) * (1 + (Re / 282000) ** 0.625) ** 0.8;
  const h = (Nu * f.k) / D;
  const [Tinf, Ts] = filmPair(r, f);
  const wantQ = r.chance(0.4);
  const qp = h * PI * D * (Ts - Tinf);
  const steps = [
    m(`Re_D = \\frac{VD}{\\nu} = \\frac{${g(V)}\\times${g(D)}}{${g(f.nu)}} = ${fmt(Re)}`),
    `Churchill–Bernstein (Eq. 7.54), valid for ${m("Re_DPr > 0.2")}: ${m("\\overline{Nu}_D = 0.3 + \\frac{0.62Re_D^{1/2}Pr^{1/3}}{[1 + (0.4/Pr)^{2/3}]^{1/4}}\\left[1 + \\left(\\frac{Re_D}{282\\,000}\\right)^{5/8}\\right]^{4/5}")}.`,
    m(`\\overline{Nu}_D = ${fmt(Nu)}, \\quad \\bar h = \\frac{\\overline{Nu}_D\\,k}{D} = \\frac{${fmt(Nu)}\\times${g(f.k)}}{${g(D)}} = ${fmt(h)}${u("W/m²·K")}`),
  ];
  if (wantQ) steps.push(m(`q' = \\bar h\\,\\pi D(T_s - T_\\infty) = ${fmt(h)}\\,\\pi(${g(D)})(${g(Ts)} - ${g(Tinf)}) = ${fmt(qp)}${u("W/m")}`));
  return numeric(wantQ ? qp : h, wantQ ? "q′" : "h̄", wantQ ? "q'" : "\\bar h", wantQ ? "W/m" : "W/m²·K", steps,
    { ht: "cyl-cb", V, D, nu: f.nu, k: f.k, Pr: f.Pr, Ts, Tinf, target: wantQ ? "q" : "h" },
    `${f.name === "air" ? "Air" : "Water"} at ${m(vu(Tinf, "K"))} flows at ${m(vu(V, "m/s"))} across a long ${Dmm}-mm-diameter cylinder held at ${m(vu(Ts, "K"))}. Properties at the film temperature ${f.T} K: ${props(f, ["nu", "k", "Pr"])}. Using the Churchill–Bernstein correlation, find ${wantQ ? "the heat rate per metre of cylinder" : "the average convection coefficient"}.`);
}

function sphereWhitaker(r: Rng): Draft {
  const i = r.pick([0, 0, 1]);
  const f = WATER[i];
  const s = WATER[r.pick([1, 2, 3].filter((j) => j > i))];
  const Dmm = r.pick([5, 10, 20, 25, 50]);
  const D = Dmm / 1000;
  const V = r.pick([0.02, 0.05, 0.1, 0.25, 0.5, 1]);
  const Re = (V * D) / f.nu;
  const ratio = f.mu / s.mu;
  require_(Re > 3.5 && Re < 7.6e4 && ratio >= 1 && ratio <= 3.2);
  const Nu = 2 + (0.4 * Math.sqrt(Re) + 0.06 * Re ** (2 / 3)) * f.Pr ** 0.4 * ratio ** 0.25;
  const h = (Nu * f.k) / D;
  const Tinf = f.T, Ts = s.T;
  const wantQ = r.chance(0.4);
  const q = h * PI * D * D * (Ts - Tinf);
  const steps = [
    `Whitaker evaluates properties at ${m("T_\\infty")} (not the film temperature), with ${m("\\mu_s")} at ${m("T_s")}.`,
    m(`Re_D = \\frac{VD}{\\nu} = \\frac{${g(V)}\\times${g(D)}}{${g(f.nu)}} = ${fmt(Re)}, \\quad \\frac{\\mu}{\\mu_s} = \\frac{${g(f.mu)}}{${g(s.mu)}} = ${fmt(ratio)}`),
    `Eq. 7.56: ${m(`\\overline{Nu}_D = 2 + (0.4Re_D^{1/2} + 0.06Re_D^{2/3})Pr^{0.4}(\\mu/\\mu_s)^{1/4} = ${fmt(Nu)}`)}.`,
    m(`\\bar h = \\frac{${fmt(Nu)}\\times${g(f.k)}}{${g(D)}} = ${fmt(h)}${u("W/m²·K")}`),
  ];
  if (wantQ) steps.push(m(`q = \\bar h\\,\\pi D^2(T_s - T_\\infty) = ${fmt(h)}\\,\\pi(${g(D)})^2(${Ts} - ${Tinf}) = ${fmt(q)}${u("W")}`));
  return numeric(wantQ ? q : h, wantQ ? "q" : "h̄", wantQ ? "q" : "\\bar h", wantQ ? "W" : "W/m²·K", steps,
    { ht: "sphere-w", V, D, nu: f.nu, k: f.k, Pr: f.Pr, mu: f.mu, mus: s.mu, Ts, Tinf, target: wantQ ? "q" : "h" },
    `Water at ${m(vu(Tinf, "K"))} flows at ${m(vu(V, "m/s"))} past a ${Dmm}-mm-diameter sphere held at ${m(vu(Ts, "K"))}. Water at ${Tinf} K: ${props(f, ["nu", "k", "Pr", "mu"])}; at ${Ts} K, ${m(`\\mu_s = ${vu(s.mu, "N·s/m²")}`)}. Using the Whitaker correlation, find ${wantQ ? "the heat rate from the sphere" : "the average convection coefficient"}.`);
}

// ═══ Ch 8 internal flow ════════════════════════════════════════════════════
const OIL: Fluid = { name: "engine oil", T: 350, nu: 41.7e-6, k: 0.138, Pr: 546, mu: 3.56e-2, cp: 2118 };
const NU_LAM_FLUX = 48 / 11; // Eq. 8.53, uniform q''_s
const NU_LAM_TS = 3.66; // Eq. 8.55, uniform T_s
const ReTex = (mdot: number, D: number, mu: number, Re: number) =>
  m(`Re_D = \\frac{4\\dot m}{\\pi D\\mu} = \\frac{4\\times${g(mdot)}}{\\pi(${g(D)})(${g(mu)})} = ${fmt(Re)}`);

function intRe(r: Rng): Draft {
  const kind = r.pick(["Re", "Re", "xfdh", "xfdt"] as const);
  const f = kind === "Re" ? r.pick([...WATER.slice(0, 3), AIR[1], OIL]) : r.pick([OIL, WATER[0], WATER[1]]);
  const Dmm = r.pick([5, 10, 15, 20, 25, 50]);
  const D = Dmm / 1000;
  const mdot = f.name === "air" ? r.pick([0.001, 0.005, 0.01, 0.02, 0.05]) : f.name === "water" && kind !== "Re" ? r.pick([0.001, 0.002, 0.005, 0.01]) : r.pick([0.01, 0.02, 0.05, 0.1, 0.25, 0.5]);
  const Re = (4 * mdot) / (PI * D * f.mu);
  const stem = `${f.name === "air" ? "Air" : f.name === "water" ? "Water" : "Engine oil"} flows at ${m(vu(mdot, "kg/s"))} through a ${Dmm}-mm-diameter tube (${f.name} at ${f.T} K: ${props(f, kind === "xfdt" ? ["mu", "Pr"] : ["mu"])}).`;
  const meta = { ht: "int-re", mdot, D, mu: f.mu, Pr: f.Pr, target: kind };
  const reStep = `${ReTex(mdot, D, f.mu, Re)} — from ${m("u_m = \\dot m/(\\rho\\pi D^2/4)")} the density cancels.`;
  if (kind === "Re") {
    require_(Re > 50 && Re < 1e6);
    return numeric(Re, "Re_D", "Re_D", "", [reStep, Re < 2300 ? `${m("Re_D < 2300")}: laminar.` : `${m("Re_D > 2300")}: turbulent${Re < 1e4 ? " (transitional below about 10⁴)" : ""}.`], meta,
      `${stem} Find the Reynolds number.`);
  }
  require_(Re > 20 && Re < 2300);
  const x = kind === "xfdh" ? 0.05 * Re * D : 0.05 * Re * f.Pr * D;
  require_(x < 1e4);
  return numeric(x, kind === "xfdh" ? "x_fd,h" : "x_fd,t", kind === "xfdh" ? "x_{fd,h}" : "x_{fd,t}", "m", [
    reStep,
    `${m("Re_D < 2300")}: laminar, so ${kind === "xfdh" ? m("x_{fd,h} \\approx 0.05Re_DD") + " (Eq. 8.3)" : m("x_{fd,t} \\approx 0.05Re_DPr\\,D") + " (Eq. 8.23)"}.`,
    m(`${kind === "xfdh" ? "x_{fd,h}" : "x_{fd,t}"} = 0.05(${fmt(Re)})${kind === "xfdt" ? `(${g(f.Pr)})` : ""}(${g(D)}) = ${fmt(x)}${u("m")}`),
    ...(kind === "xfdt" && f.Pr > 10 ? [`Large ${m("Pr")}: the thermal entry length dwarfs the hydrodynamic one, so the velocity profile is fully developed long before the temperature profile is.`] : []),
  ], meta, `${stem} Find the ${kind === "xfdh" ? "hydrodynamic" : "thermal"} entry length.`);
}

function tmFlux(r: Rng): Draft {
  const mdot = r.pick([0.01, 0.02, 0.05, 0.1, 0.2]);
  const D = r.pick([10, 20, 25, 40, 50]) / 1000;
  const qs = r.pick([1000, 2000, 5000, 1e4, 2e4]);
  const Tmi = r.pick([10, 15, 20, 25]);
  const cp = 4180;
  const kind = r.pick(["Tmo", "Tmo", "L", "Tso"] as const);
  const stem = `Water (${m(`c_p = ${vu(cp, "J/kg·K")}`)}) enters a ${g(D * 1000)}-mm-diameter tube at ${m(vu(Tmi, "°C"))} and ${m(vu(mdot, "kg/s"))}. The wall supplies a uniform heat flux ${m(`q''_s = ${vu(qs, "W/m²")}`)}.`;
  const meta = { ht: "tm-flux", mdot, D, qs, Tmi, cp, target: kind };
  const bal = `Energy balance on a slice: ${m("\\dot mc_p\\,dT_m = q''_s\\,\\pi D\\,dx")}, so ${m("T_m")} rises linearly: ${m("T_{m,o} = T_{m,i} + \\frac{q''_s\\pi DL}{\\dot mc_p}")}.`;
  if (kind === "L") {
    const Tmo = Tmi + r.pick([10, 20, 25, 30, 40, 50]);
    const L = (mdot * cp * (Tmo - Tmi)) / (qs * PI * D);
    require_(L > 0.2 && L < 200);
    return numeric(L, "L", "L", "m", [bal, m(`L = \\frac{\\dot mc_p(T_{m,o} - T_{m,i})}{q''_s\\pi D} = \\frac{${g(mdot)}\\times${cp}\\times${Tmo - Tmi}}{${g(qs)}\\,\\pi(${g(D)})} = ${fmt(L)}${u("m")}`)],
      { ...meta, Tmo }, `${stem} What tube length heats it to ${m(vu(Tmo, "°C"))}?`);
  }
  const L = r.pick([2, 5, 10, 20]);
  const Tmo = Tmi + (qs * PI * D * L) / (mdot * cp);
  require_(Tmo > Tmi + 1 && Tmo < 95);
  const s = [bal, m(`T_{m,o} = ${Tmi} + \\frac{${g(qs)}\\,\\pi(${g(D)})(${L})}{${g(mdot)}\\times${cp}} = ${fmt(Tmo)}${u("°C")}`)];
  if (kind === "Tmo") return numeric(Tmo, "T_m,o", "T_{m,o}", "°C", s, { ...meta, L }, `${stem} The tube is ${L} m long. Find the outlet mean temperature.`);
  const h = r.pick([500, 1000, 2000, 3000]);
  const Tso = Tmo + qs / h;
  return numeric(Tso, "T_s,o", "T_{s,o}", "°C", [...s, `At the outlet, ${m("q''_s = h(T_s - T_m)")}: ${m(`T_{s,o} = T_{m,o} + \\frac{q''_s}{h} = ${fmt(Tmo, 4)} + \\frac{${g(qs)}}{${h}} = ${fmt(Tso)}${u("°C")}`)}.`],
    { ...meta, L, h }, `${stem} The tube is ${L} m long and the flow is fully developed at the outlet with ${m(`h = ${vu(h, "W/m²·K")}`)}. Find the wall temperature at the outlet.`);
}

function tmTs(r: Rng): Draft {
  const mdot = r.pick([0.02, 0.05, 0.1, 0.2, 0.5]);
  const D = r.pick([10, 20, 25, 40, 50]) / 1000;
  const h = r.pick([200, 500, 1000, 2000, 5000]);
  const [Ts, how] = r.pick([[100, "steam condensing on its outside"], [120, "condensing steam"], [5, "an ice-water bath"], [90, "a hot-water jacket"]] as [number, string][]);
  const Tmi = Ts > 50 ? r.pick([10, 15, 20, 25]) : r.pick([40, 50, 60, 80]);
  const cp = 4180;
  const kind = r.pick(["Tmo", "Tmo", "L", "q"] as const);
  const stem = `Water (${m(`c_p = ${vu(cp, "J/kg·K")}`)}) enters a ${g(D * 1000)}-mm-diameter tube at ${m(vu(Tmi, "°C"))} and ${m(vu(mdot, "kg/s"))}. The wall is held at ${m(vu(Ts, "°C"))} by ${how}; the average convection coefficient is ${m(`\\bar h = ${vu(h, "W/m²·K")}`)}.`;
  const meta = { ht: "tm-ts", mdot, D, h, Ts, Tmi, cp, target: kind };
  const law = `Constant ${m("T_s")}: ${m("\\dot mc_p\\,dT_m = h\\pi D(T_s - T_m)\\,dx")} integrates to ${m("\\frac{T_s - T_{m,o}}{T_s - T_{m,i}} = \\exp\\left(-\\frac{\\pi DL\\bar h}{\\dot mc_p}\\right)")} (Eq. 8.42b).`;
  if (kind === "L") {
    const Tmo = Ts > 50 ? Math.round(Tmi + (Ts - Tmi) * r.pick([0.3, 0.5, 0.6, 0.75, 0.9])) : Math.round(Ts + (Tmi - Ts) * r.pick([0.2, 0.4, 0.5, 0.7]));
    const ratio = (Ts - Tmo) / (Ts - Tmi);
    require_(ratio > 0.02 && ratio < 0.98);
    const L = (-(mdot * cp) / (PI * D * h)) * Math.log(ratio);
    require_(L > 0.1 && L < 500);
    return numeric(L, "L", "L", "m", [law, m(`L = -\\frac{\\dot mc_p}{\\pi D\\bar h}\\ln\\frac{T_s - T_{m,o}}{T_s - T_{m,i}} = -\\frac{${g(mdot)}\\times${cp}}{\\pi(${g(D)})(${h})}\\ln\\frac{${Ts} - ${Tmo}}{${Ts} - ${Tmi}} = ${fmt(L)}${u("m")}`)],
      { ...meta, Tmo }, `${stem} What tube length brings the water to ${m(vu(Tmo, "°C"))}?`);
  }
  const L = r.pick([1, 2, 5, 10, 20]);
  const NTU = (PI * D * L * h) / (mdot * cp);
  require_(NTU > 0.05 && NTU < 5);
  const Tmo = Ts - (Ts - Tmi) * Math.exp(-NTU);
  const s = [law, m(`\\frac{\\pi DL\\bar h}{\\dot mc_p} = \\frac{\\pi(${g(D)})(${L})(${h})}{${g(mdot)}\\times${cp}} = ${fmt(NTU)}`), m(`T_{m,o} = T_s - (T_s - T_{m,i})e^{-${fmt(NTU)}} = ${fmt(Tmo)}${u("°C")}`)];
  if (kind === "Tmo") return numeric(Tmo, "T_m,o", "T_{m,o}", "°C", s, { ...meta, L }, `${stem} The tube is ${L} m long. Find the outlet mean temperature.`);
  const q = mdot * cp * (Tmo - Tmi);
  return numeric(q, "q", "q", "W", [...s, `Overall balance: ${m(`q = \\dot mc_p(T_{m,o} - T_{m,i}) = ${g(mdot)}\\times${cp}(${fmt(Tmo, 4)} - ${Tmi}) = ${fmt(q)}${u("W")}`)}${q < 0 ? " (negative: the water is cooled)" : ""}.`],
    { ...meta, L }, `${stem} The tube is ${L} m long. Find the total heat rate to the water${Ts < Tmi ? " (negative if the water loses heat)" : ""}.`);
}

function dittus(r: Rng): Draft {
  const air = r.chance(0.3);
  const f = air ? r.pick(AIR.slice(1, 3)) : r.pick(WATER.slice(0, 3));
  const Dmm = r.pick([10, 20, 25, 40, 50]);
  const D = Dmm / 1000;
  const mdot = air ? r.pick([0.01, 0.02, 0.05, 0.1]) : r.pick([0.1, 0.2, 0.5, 1]);
  const Re = (4 * mdot) / (PI * D * f.mu);
  require_(Re >= 1e4 && Re < 5e6);
  const heating = r.chance(0.5);
  const n = heating ? 0.4 : 0.3;
  const Nu = 0.023 * Re ** 0.8 * f.Pr ** n;
  const h = (Nu * f.k) / D;
  return numeric(h, "h", "h", "W/m²·K", [
    `${ReTex(mdot, D, f.mu, Re)} ${m("\\ge 10^4")}: fully turbulent.`,
    `Dittus–Boelter (Eq. 8.60): ${m("Nu_D = 0.023Re_D^{4/5}Pr^n")}, ${m(`n = ${n}`)} because the fluid is being ${heating ? "heated" : "cooled"} (${m(heating ? "T_s > T_m" : "T_s < T_m")}).`,
    m(`Nu_D = 0.023(${fmt(Re)})^{0.8}(${g(f.Pr)})^{${n}} = ${fmt(Nu)}`),
    m(`h = \\frac{Nu_D\\,k}{D} = \\frac{${fmt(Nu)}\\times${g(f.k)}}{${g(D)}} = ${fmt(h)}${u("W/m²·K")}`),
  ], { ht: "dittus", mdot, D, mu: f.mu, k: f.k, Pr: f.Pr, heating },
  `${air ? "Air" : "Water"} flows at ${m(vu(mdot, "kg/s"))} through a long ${Dmm}-mm-diameter tube whose wall is ${heating ? "hotter" : "colder"} than the fluid. Properties at the mean temperature ${f.T} K: ${props(f, ["mu", "k", "Pr"])}. Find the fully developed convection coefficient.`);
}

function lamFd(r: Rng): Draft {
  const f = r.pick([OIL, OIL, WATER[0], WATER[1]]);
  const Dmm = r.pick([5, 10, 20, 25]);
  const D = Dmm / 1000;
  const mdot = f.name === "water" ? r.pick([0.001, 0.002, 0.005]) : r.pick([0.01, 0.02, 0.05, 0.1]);
  const Re = (4 * mdot) / (PI * D * f.mu);
  require_(Re < 2300);
  const flux = r.chance(0.5);
  const Nu = flux ? NU_LAM_FLUX : NU_LAM_TS;
  const h = (Nu * f.k) / D;
  return numeric(h, "h", "h", "W/m²·K", [
    `${ReTex(mdot, D, f.mu, Re)} ${m("< 2300")}: laminar.`,
    flux
      ? `Fully developed, uniform ${m("q''_s")}: ${m("Nu_D = \\frac{48}{11} = 4.36")} (Eq. 8.53) — no Re or Pr dependence.`
      : `Fully developed, uniform ${m("T_s")}: ${m("Nu_D = 3.66")} (Eq. 8.55) — no Re or Pr dependence.`,
    m(`h = \\frac{Nu_D\\,k}{D} = \\frac{${flux ? "4.364" : "3.66"}\\times${g(f.k)}}{${g(D)}} = ${fmt(h)}${u("W/m²·K")}`),
  ], { ht: "lam-fd", mdot, D, mu: f.mu, k: f.k, bc: flux ? "flux" : "Ts" },
  `${f.name === "water" ? "Water" : "Engine oil"} flows at ${m(vu(mdot, "kg/s"))} through a ${Dmm}-mm-diameter tube with ${flux ? "a uniform wall heat flux" : "a uniform wall temperature"}. Properties at ${f.T} K: ${props(f, ["mu", "k"])}. Find the convection coefficient where the flow is hydrodynamically and thermally fully developed.`);
}

// ═══ Ch 9 free convection ══════════════════════════════════════════════════
interface Free { f: Fluid; Tinf: number; Ts: number; dT: number; beta: number }
function freeSetup(r: Rng, pool: Fluid[] = AIR.slice(1, 4)): Free {
  const f = r.pick(pool);
  const dT = r.pick([10, 20, 30, 40, 60, 80, 100]);
  require_(f.T - dT / 2 >= 250);
  const hot = r.chance(0.75);
  const Tinf = hot ? f.T - dT / 2 : f.T + dT / 2;
  const Ts = hot ? f.T + dT / 2 : f.T - dT / 2;
  return { f, Tinf, Ts, dT, beta: 1 / f.T };
}
const freeProps = (F: Free) => `Air properties at the film temperature ${F.f.T} K: ${props(F.f, ["nu", "alpha", "k", "Pr"])}.`;
const raStep = (F: Free, Lsym: string, L: number, Ra: number) =>
  `Ideal gas: ${m(`\\beta = 1/T_f = 1/${F.f.T}\\,\\mathrm{K^{-1}}`)}. ${m(`Ra_${Lsym} = \\frac{g\\beta(T_s - T_\\infty)${Lsym}^3}{\\nu\\alpha} = \\frac{9.8(1/${F.f.T})(${F.dT})(${g(L)})^3}{(${g(F.f.nu)})(${g(F.f.alpha!)})} = ${fmt(Ra)}`)}.`;
const raOf = (F: Free, L: number) => (GRAV * F.beta * F.dT * L ** 3) / (F.f.nu * F.f.alpha!);
const freeMeta = (F: Free, extra: Record<string, unknown>) => ({ Tf: F.f.T, nu: F.f.nu, alpha: F.f.alpha, k: F.f.k, Pr: F.f.Pr, Ts: F.Ts, Tinf: F.Tinf, ...extra });

function freeRa(r: Rng): Draft {
  const F = freeSetup(r);
  const cyl = r.chance(0.4);
  const L = cyl ? r.pick([10, 25, 50, 100, 200]) / 1000 : r.pick([0.1, 0.25, 0.5, 1, 1.5, 2]);
  const Ra = raOf(F, L);
  return numeric(Ra, cyl ? "Ra_D" : "Ra_L", cyl ? "Ra_D" : "Ra_L", "", [
    raStep(F, cyl ? "D" : "L", L, Ra),
    cyl ? `${m("Ra_D \\le 10^{12}")}, so Churchill–Chu (Eq. 9.34) would apply.` : Ra < 1e9 ? `${m("Ra_L < 10^9")}: the boundary layer is laminar.` : `${m("Ra_L > 10^9")}: the boundary layer becomes turbulent partway up.`,
  ], { ht: "free", geo: cyl ? "hcyl" : "vplate", L, ...freeMeta(F, {}), target: "Ra" },
  `${cyl ? "A" : an(g(L))} ${cyl ? `long horizontal ${g(L * 1000)}-mm-diameter cylinder` : `${g(L)}-m-tall vertical plate`} at ${m(vu(F.Ts, "K"))} is in quiescent air at ${m(vu(F.Tinf, "K"))}. ${freeProps(F)} Find the Rayleigh number ${cyl ? m("Ra_D") : m("Ra_L")}.`);
}

const CC_TEX = "\\overline{Nu}_L = \\left\\{0.825 + \\frac{0.387Ra_L^{1/6}}{[1 + (0.492/Pr)^{9/16}]^{8/27}}\\right\\}^2";
function chuVertical(r: Rng): Draft {
  const F = freeSetup(r);
  const L = r.pick([0.1, 0.25, 0.3, 0.5, 1, 1.5, 2]);
  const Ra = raOf(F, L);
  require_(Ra > 1e4 && Ra < 1e13);
  const Nu = (0.825 + (0.387 * Ra ** (1 / 6)) / (1 + (0.492 / F.f.Pr) ** (9 / 16)) ** (8 / 27)) ** 2;
  const h = (Nu * F.f.k) / L;
  const W = r.pick([0.5, 1, 2]);
  const wantQ = r.chance(0.4);
  const q = h * L * W * (F.Ts - F.Tinf);
  const steps = [
    raStep(F, "L", L, Ra),
    `Churchill–Chu, any ${m("Ra_L")} (Eq. 9.26): ${m(CC_TEX)} ${m(`= ${fmt(Nu)}`)}.`,
    m(`\\bar h = \\frac{\\overline{Nu}_L\\,k}{L} = \\frac{${fmt(Nu)}\\times${g(F.f.k)}}{${g(L)}} = ${fmt(h)}${u("W/m²·K")}`),
  ];
  if (wantQ) steps.push(m(`q = \\bar h\\,(LW)(T_s - T_\\infty) = ${fmt(h)}(${g(L * W)})(${F.Ts} - ${F.Tinf}) = ${fmt(q)}${u("W")}`));
  return numeric(wantQ ? q : h, wantQ ? "q" : "h̄", wantQ ? "q" : "\\bar h", wantQ ? "W" : "W/m²·K", steps,
    { ht: "free", geo: "vplate", L, W, ...freeMeta(F, {}), target: wantQ ? "q" : "h" },
    `${an(g(L))} ${g(L)}-m-tall, ${g(W)}-m-wide vertical plate at ${m(vu(F.Ts, "K"))} is in quiescent air at ${m(vu(F.Tinf, "K"))}. ${freeProps(F)} Using the Churchill–Chu correlation for the full range (Eq. 9.26), find ${wantQ ? "the heat rate from one side" : "the average convection coefficient"}.`);
}

function freeHoriz(r: Rng): Draft {
  const F = freeSetup(r, AIR.slice(0, 3));
  const a = r.pick([0.1, 0.2, 0.25, 0.3, 0.5, 1]);
  const b = r.pick([0.1, 0.2, 0.25, 0.5, 1, 2]);
  const hotSurface = F.Ts > F.Tinf;
  const up = r.chance(0.5); // the plate's exposed face points up
  // hot face up or cold face down → buoyant plume rises freely (Eqs. 9.30–9.31); otherwise Eq. 9.32
  const rising = up === hotSurface;
  const L = (a * b) / (2 * (a + b));
  const Ra = raOf(F, L);
  let Nu: number, corr: string;
  if (rising) {
    require_(Ra >= 1e4 && Ra <= 1e11);
    if (Ra <= 1e7) { Nu = 0.54 * Ra ** 0.25; corr = "\\overline{Nu}_L = 0.54Ra_L^{1/4}\\ (10^4 \\le Ra_L \\le 10^7,\\ \\text{Eq. 9.30})"; }
    else { Nu = 0.15 * Math.cbrt(Ra); corr = "\\overline{Nu}_L = 0.15Ra_L^{1/3}\\ (10^7 \\le Ra_L \\le 10^{11},\\ \\text{Eq. 9.31})"; }
  } else {
    require_(Ra >= 1e4 && Ra <= 1e9);
    Nu = 0.52 * Ra ** 0.2;
    corr = "\\overline{Nu}_L = 0.52Ra_L^{1/5}\\ (10^4 \\le Ra_L \\le 10^9,\\ \\text{Eq. 9.32})";
  }
  const h = (Nu * F.f.k) / L;
  const wantQ = r.chance(0.5);
  const q = h * a * b * (F.Ts - F.Tinf);
  const face = `${hotSurface ? "hot" : "cold"} face ${up ? "up" : "down"}`;
  const steps = [
    `Characteristic length ${m(`L = \\frac{A_s}{P} = \\frac{${g(a)}\\times${g(b)}}{2(${g(a)} + ${g(b)})} = ${fmt(L)}\\,\\mathrm{m}`)}.`,
    raStep(F, "L", L, Ra).replace("(T_s - T_\\infty)", "|T_s - T_\\infty|"),
    `${face[0].toUpperCase()}${face.slice(1)}: ${rising ? "the plume leaves the surface freely" : "the fluid has to spill around the edges"}, so ${m(corr)}: ${m(`\\overline{Nu}_L = ${fmt(Nu)}`)}.`,
    m(`\\bar h = \\frac{${fmt(Nu)}\\times${g(F.f.k)}}{${fmt(L)}} = ${fmt(h)}${u("W/m²·K")}`),
  ];
  if (wantQ) steps.push(m(`q = \\bar hA_s(T_s - T_\\infty) = ${fmt(h)}(${g(a * b)})(${F.Ts} - ${F.Tinf}) = ${fmt(q)}${u("W")}`));
  return numeric(wantQ ? q : h, wantQ ? "q" : "h̄", wantQ ? "q" : "\\bar h", wantQ ? "W" : "W/m²·K", steps,
    { ht: "free", geo: "hplate", a, b, up, ...freeMeta(F, {}), target: wantQ ? "q" : "h" },
    `A horizontal ${g(a)} m × ${g(b)} m plate at ${m(vu(F.Ts, "K"))} exchanges heat by free convection from its ${up ? "upper" : "lower"} face (the other face is insulated) with quiescent air at ${m(vu(F.Tinf, "K"))}. ${freeProps(F)} Find ${wantQ ? `the heat rate${hotSurface ? "" : " (negative: heat flows into the plate)"}` : "the average convection coefficient"}.`);
}

function freeCyl(r: Rng): Draft {
  const F = freeSetup(r);
  const Dmm = r.pick([10, 25, 50, 100, 200]);
  const D = Dmm / 1000;
  const Ra = raOf(F, D);
  require_(Ra <= 1e12 && Ra > 1);
  const Nu = (0.6 + (0.387 * Ra ** (1 / 6)) / (1 + (0.559 / F.f.Pr) ** (9 / 16)) ** (8 / 27)) ** 2;
  const h = (Nu * F.f.k) / D;
  const wantQ = r.chance(0.5);
  const qp = h * PI * D * (F.Ts - F.Tinf);
  const steps = [
    raStep(F, "D", D, Ra),
    `Churchill–Chu, horizontal cylinder (Eq. 9.34): ${m("\\overline{Nu}_D = \\left\\{0.60 + \\frac{0.387Ra_D^{1/6}}{[1 + (0.559/Pr)^{9/16}]^{8/27}}\\right\\}^2")} ${m(`= ${fmt(Nu)}`)}.`,
    m(`\\bar h = \\frac{${fmt(Nu)}\\times${g(F.f.k)}}{${g(D)}} = ${fmt(h)}${u("W/m²·K")}`),
  ];
  if (wantQ) steps.push(m(`q' = \\bar h\\,\\pi D(T_s - T_\\infty) = ${fmt(h)}\\,\\pi(${g(D)})(${F.Ts} - ${F.Tinf}) = ${fmt(qp)}${u("W/m")}`));
  return numeric(wantQ ? qp : h, wantQ ? "q′" : "h̄", wantQ ? "q'" : "\\bar h", wantQ ? "W/m" : "W/m²·K", steps,
    { ht: "free", geo: "hcyl", L: D, ...freeMeta(F, {}), target: wantQ ? "q" : "h" },
    `A long horizontal ${Dmm}-mm-diameter pipe at ${m(vu(F.Ts, "K"))} is in quiescent air at ${m(vu(F.Tinf, "K"))}. ${freeProps(F)} Find ${wantQ ? "the heat rate per metre of pipe" : "the average convection coefficient"}.`);
}

// ═══ Ch 11 heat exchangers ═════════════════════════════════════════════════
const HOT: [string, number][] = [["engine oil", 2131], ["hot water", 4190], ["ethylene glycol", 2650]];
const COLD: [string, number][] = [["water", 4178], ["water", 4180]];
interface HX { hot: string; cph: number; cpc: number; mh: number; mc: number; Ch: number; Cc: number }
function hxFlows(r: Rng): HX {
  const [hot, cph] = r.pick(HOT);
  const [, cpc] = r.pick(COLD);
  const mh = r.pick([0.1, 0.2, 0.3, 0.5, 1, 1.2, 2]);
  const mc = r.pick([0.1, 0.2, 0.25, 0.4, 0.5, 1, 1.5]);
  return { hot, cph, cpc, mh, mc, Ch: mh * cph, Cc: mc * cpc };
}
const hxStreams = (x: HX) =>
  `${x.hot[0].toUpperCase()}${x.hot.slice(1)} (${m(`c_p = ${vu(x.cph, "J/kg·K")}`)}) at ${m(vu(x.mh, "kg/s"))} heats water (${m(`c_p = ${vu(x.cpc, "J/kg·K")}`)}) at ${m(vu(x.mc, "kg/s"))}`;
const hxMeta = (x: HX, extra: Record<string, unknown>) => ({ mh: x.mh, cph: x.cph, mc: x.mc, cpc: x.cpc, ...extra });

function lmtd(counter: boolean) {
  return (r: Rng): Draft => {
    const x = hxFlows(r);
    const Thi = r.pick([80, 90, 100, 120, 150, 180, 200]);
    const Tho = Thi - r.pick([10, 20, 30, 40, 50, 60, 80]);
    const Tci = r.pick([10, 15, 20, 25, 30]);
    const q = x.Ch * (Thi - Tho);
    const Tco = Tci + q / x.Cc;
    const dT1 = counter ? Thi - Tco : Thi - Tci;
    const dT2 = counter ? Tho - Tci : Tho - Tco;
    require_(dT1 > 3 && dT2 > 3 && Math.abs(dT1 - dT2) > 1 && Tco < 100);
    const lm = (dT1 - dT2) / Math.log(dT1 / dT2);
    const U = r.pick([100, 250, 500, 800, 1000, 1500, 2000]);
    const A = q / (U * lm);
    const tube = r.chance(0.4);
    const Dmm = r.pick([20, 25, 50, 100]);
    const L = A / (PI * (Dmm / 1000));
    require_(A > 0.05 && A < 500 && (!tube || (L > 0.5 && L < 2000)));
    const ends = counter
      ? m(`\\Delta T_1 = T_{h,i} - T_{c,o} = ${dT1 % 1 ? fmt(dT1, 4) : dT1}, \\quad \\Delta T_2 = T_{h,o} - T_{c,i} = ${dT2 % 1 ? fmt(dT2, 4) : dT2}`)
      : m(`\\Delta T_1 = T_{h,i} - T_{c,i} = ${dT1 % 1 ? fmt(dT1, 4) : dT1}, \\quad \\Delta T_2 = T_{h,o} - T_{c,o} = ${dT2 % 1 ? fmt(dT2, 4) : dT2}`);
    const steps = [
      `Hot side: ${m(`q = \\dot m_hc_{p,h}(T_{h,i} - T_{h,o}) = ${g(x.mh)}\\times${x.cph}\\times${Thi - Tho} = ${fmt(q)}${u("W")}`)}; cold side: ${m(`T_{c,o} = T_{c,i} + \\frac{q}{\\dot m_cc_{p,c}} = ${fmt(Tco)}${u("°C")}`)}.`,
      `${counter ? "Counterflow" : "Parallel flow"} — the end temperature differences: ${ends}.`,
      m(`\\Delta T_{lm} = \\frac{\\Delta T_1 - \\Delta T_2}{\\ln(\\Delta T_1/\\Delta T_2)} = ${fmt(lm)}${u("K")}`),
      m(`A = \\frac{q}{U\\Delta T_{lm}} = \\frac{${fmt(q)}}{${U}\\times${fmt(lm)}} = ${fmt(A)}${u("m²")}`),
    ];
    if (tube) steps.push(m(`L = \\frac{A}{\\pi D} = \\frac{${fmt(A)}}{\\pi(${g(Dmm / 1000)})} = ${fmt(L)}${u("m")}`));
    const stem = `${hxStreams(x)} in a ${counter ? "counterflow" : "parallel-flow"} ${tube ? `double-pipe exchanger (inner tube ${Dmm} mm in diameter)` : "heat exchanger"} with ${m(`U = ${vu(U, "W/m²·K")}`)}. The ${x.hot} cools from ${m(vu(Thi, "°C"))} to ${m(vu(Tho, "°C"))}; the water enters at ${m(vu(Tci, "°C"))}.`;
    return numeric(tube ? L : A, tube ? "L" : "A", tube ? "L" : "A", tube ? "m" : "m²", steps,
      { ht: "lmtd", flow: counter ? "counter" : "parallel", ...hxMeta(x, { Thi, Tho, Tci, U, D: Dmm / 1000, target: tube ? "L" : "A" }) },
      `${stem} Find the required ${tube ? "tube length" : "heat transfer area"}.`);
  };
}

type Flow = "parallel" | "counter" | "shell2";
export function effectiveness(flow: Flow, NTU: number, Cr: number): number {
  if (flow === "parallel") return (1 - Math.exp(-NTU * (1 + Cr))) / (1 + Cr);
  if (flow === "counter") {
    const e = Math.exp(-NTU * (1 - Cr));
    return (1 - e) / (1 - Cr * e);
  }
  const s = Math.sqrt(1 + Cr * Cr);
  const e = Math.exp(-NTU * s);
  return 2 / (1 + Cr + (s * (1 + e)) / (1 - e));
}
const EPS_TEX: Record<Flow, string> = {
  parallel: "\\varepsilon = \\frac{1 - \\exp[-NTU(1 + C_r)]}{1 + C_r}\\ \\text{(Eq. 11.28a)}",
  counter: "\\varepsilon = \\frac{1 - \\exp[-NTU(1 - C_r)]}{1 - C_r\\exp[-NTU(1 - C_r)]}\\ \\text{(Eq. 11.29a)}",
  shell2: "\\varepsilon = 2\\left\\{1 + C_r + \\sqrt{1 + C_r^2}\\,\\frac{1 + e^{-NTU\\sqrt{1 + C_r^2}}}{1 - e^{-NTU\\sqrt{1 + C_r^2}}}\\right\\}^{-1}\\ \\text{(Eq. 11.30a)}",
};
const FLOW_NAME: Record<Flow, string> = { parallel: "parallel-flow", counter: "counterflow", shell2: "shell-and-tube (one shell pass, two tube passes)" };
interface NTUCase { x: HX; flow: Flow; U: number; A: number; Cmin: number; Cmax: number; Cr: number; NTU: number; eps: number; Thi: number; Tci: number }
function ntuSetup(r: Rng, flows: Flow[]): NTUCase {
  const x = hxFlows(r);
  const flow = r.pick(flows);
  const U = r.pick([200, 500, 800, 1000, 1500, 2000]);
  const A = r.pick([0.5, 1, 2, 3, 5, 8, 10, 20]);
  const Cmin = Math.min(x.Ch, x.Cc), Cmax = Math.max(x.Ch, x.Cc);
  const Cr = Cmin / Cmax;
  const NTU = (U * A) / Cmin;
  require_(NTU > 0.2 && NTU < 5 && Cr < 0.95);
  const eps = effectiveness(flow, NTU, Cr);
  const Thi = r.pick([80, 90, 100, 120, 150]);
  const Tci = r.pick([10, 15, 20, 25]);
  return { x, flow, U, A, Cmin, Cmax, Cr, NTU, eps, Thi, Tci };
}
const ntuSteps = (c: NTUCase) => [
  `${m(`C_h = ${fmt(c.x.Ch, 4)}`)}, ${m(`C_c = ${fmt(c.x.Cc, 4)}\\ \\mathrm{W/K}`)}: ${m(`C_{min} = ${fmt(c.Cmin, 4)}`)} (the ${c.Cmin === c.x.Ch ? c.x.hot : "water"}), ${m(`C_r = ${fmt(c.Cr, 4)}`)}.`,
  m(`NTU = \\frac{UA}{C_{min}} = \\frac{${c.U}\\times${g(c.A)}}{${fmt(c.Cmin, 4)}} = ${fmt(c.NTU)}`),
  `${m(EPS_TEX[c.flow])}: ${m(`\\varepsilon = ${fmt(c.eps)}`)}.`,
];
const ntuStem = (c: NTUCase) =>
  `${hxStreams(c.x)} in a ${FLOW_NAME[c.flow]} heat exchanger with ${m(`U = ${vu(c.U, "W/m²·K")}`)} and ${m(`A = ${vu(c.A, "m²")}`)}. The ${c.x.hot} enters at ${m(vu(c.Thi, "°C"))}, the water at ${m(vu(c.Tci, "°C"))}.`;
const ntuMeta = (c: NTUCase, target: string) => ({ ht: "ntu", flow: c.flow, ...hxMeta(c.x, { U: c.U, A: c.A, Thi: c.Thi, Tci: c.Tci, target }) });

function ntuEff(r: Rng): Draft {
  const c = ntuSetup(r, ["parallel", "counter"]);
  return numeric(c.eps, "ε", "\\varepsilon", "", ntuSteps(c), ntuMeta(c, "eps"),
    `${ntuStem(c)} Find the effectiveness ${m("\\varepsilon")} (as a fraction).`);
}

function ntuOutlet(r: Rng): Draft {
  const c = ntuSetup(r, ["parallel", "counter"]);
  const q = c.eps * c.Cmin * (c.Thi - c.Tci);
  const cold = r.chance(0.5);
  const T = cold ? c.Tci + q / c.x.Cc : c.Thi - q / c.x.Ch;
  return numeric(T, cold ? "T_c,o" : "T_h,o", cold ? "T_{c,o}" : "T_{h,o}", "°C", [
    ...ntuSteps(c),
    m(`q = \\varepsilon C_{min}(T_{h,i} - T_{c,i}) = ${fmt(c.eps)}\\times${fmt(c.Cmin, 4)}\\times${c.Thi - c.Tci} = ${fmt(q)}${u("W")}`),
    cold ? m(`T_{c,o} = T_{c,i} + \\frac{q}{C_c} = ${c.Tci} + \\frac{${fmt(q)}}{${fmt(c.x.Cc, 4)}} = ${fmt(T)}${u("°C")}`)
      : m(`T_{h,o} = T_{h,i} - \\frac{q}{C_h} = ${c.Thi} - \\frac{${fmt(q)}}{${fmt(c.x.Ch, 4)}} = ${fmt(T)}${u("°C")}`),
  ], ntuMeta(c, cold ? "Tco" : "Tho"), `${ntuStem(c)} Find the outlet temperature of the ${cold ? "water" : c.x.hot}.`);
}

function shellTube(r: Rng): Draft {
  const c = ntuSetup(r, ["shell2"]);
  const q = c.eps * c.Cmin * (c.Thi - c.Tci);
  const kind = r.pick(["q", "Tco", "eps"] as const);
  const steps = ntuSteps(c);
  if (kind === "eps") return numeric(c.eps, "ε", "\\varepsilon", "", steps, ntuMeta(c, "eps"), `${ntuStem(c)} Find the effectiveness ${m("\\varepsilon")} (as a fraction).`);
  steps.push(m(`q = \\varepsilon C_{min}(T_{h,i} - T_{c,i}) = ${fmt(c.eps)}\\times${fmt(c.Cmin, 4)}\\times${c.Thi - c.Tci} = ${fmt(q)}${u("W")}`));
  if (kind === "q") return numeric(q, "q", "q", "W", steps, ntuMeta(c, "q"), `${ntuStem(c)} Find the heat transfer rate.`);
  const T = c.Tci + q / c.x.Cc;
  steps.push(m(`T_{c,o} = ${c.Tci} + \\frac{${fmt(q)}}{${fmt(c.x.Cc, 4)}} = ${fmt(T)}${u("°C")}`));
  return numeric(T, "T_c,o", "T_{c,o}", "°C", steps, ntuMeta(c, "Tco"), `${ntuStem(c)} Find the water outlet temperature.`);
}

// ═══ Ch 13 view factors ════════════════════════════════════════════════════
function vfReciprocity(r: Rng): Draft {
  const A1 = r.pick([0.5, 1, 1.5, 2, 2.5, 4]);
  const A2 = r.pick([1, 2, 3, 4, 5, 6, 8]);
  const F12 = r.pick([0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6]);
  if (r.chance(0.5)) {
    const F21 = (A1 * F12) / A2;
    require_(F21 < 1 && A1 !== A2);
    return numeric(F21, "F₂₁", "F_{21}", "", [
      `Reciprocity: ${m("A_1F_{12} = A_2F_{21}")}.`,
      m(`F_{21} = \\frac{A_1F_{12}}{A_2} = \\frac{${g(A1)}\\times${g(F12)}}{${g(A2)}} = ${fmt(F21)}`),
    ], { ht: "vf", case: "recip", A1, A2, F12 },
    `Surface 1 (${m(`A_1 = ${vu(A1, "m²")}`)}) and surface 2 (${m(`A_2 = ${vu(A2, "m²")}`)}) have ${m(`F_{12} = ${g(F12)}`)}. Find ${m("F_{21}")}.`);
  }
  const A3 = r.pick([1, 2, 3, 4, 5, 6]);
  const F31 = (A1 * (1 - F12)) / A3;
  require_(F31 < 1);
  return numeric(F31, "F₃₁", "F_{31}", "", [
    `Surface 1 is flat, so ${m("F_{11} = 0")}; summation: ${m(`F_{13} = 1 - F_{11} - F_{12} = 1 - ${g(F12)} = ${g(1 - F12)}`)}.`,
    `Reciprocity: ${m(`F_{31} = \\frac{A_1F_{13}}{A_3} = \\frac{${g(A1)}\\times${g(1 - F12)}}{${g(A3)}} = ${fmt(F31)}`)}.`,
  ], { ht: "vf", case: "sum-recip", A1, A3, F12 },
  `A flat surface 1 (${m(`A_1 = ${vu(A1, "m²")}`)}) sees only surfaces 2 and 3; ${m(`F_{12} = ${g(F12)}`)}. Surface 3 has ${m(`A_3 = ${vu(A3, "m²")}`)}. Find ${m("F_{31}")}.`);
}

function vfConcentric(r: Rng): Draft {
  const sphere = r.chance(0.5);
  const D1 = r.pick([0.1, 0.2, 0.25, 0.3, 0.5]);
  const D2 = D1 + r.pick([0.05, 0.1, 0.2, 0.25, 0.5]);
  const ratio = sphere ? (D1 / D2) ** 2 : D1 / D2;
  const self = r.chance(0.5);
  const val = self ? 1 - ratio : ratio;
  return numeric(val, self ? "F₂₂" : "F₂₁", self ? "F_{22}" : "F_{21}", "", [
    `The inner surface is convex and fully enclosed: ${m("F_{11} = 0")}, ${m("F_{12} = 1")}.`,
    `Reciprocity: ${m(`F_{21} = \\frac{A_1}{A_2}F_{12} = ${sphere ? "\\left(\\frac{D_1}{D_2}\\right)^2" : "\\frac{D_1}{D_2}"} = ${sphere ? `\\left(\\frac{${g(D1)}}{${g(D2)}}\\right)^2` : `\\frac{${g(D1)}}{${g(D2)}}`} = ${fmt(ratio)}`)}.`,
    ...(self ? [`Summation on the concave outer surface, which sees itself: ${m(`F_{22} = 1 - F_{21} = ${fmt(val)}`)}.`] : []),
  ], { ht: "vf", case: "concentric", sphere, D1, D2, target: self ? "F22" : "F21" },
  `${sphere ? "A sphere" : "A long cylinder"} of diameter ${m(vu(D1, "m"))} (surface 1) sits concentrically inside a ${sphere ? "spherical shell" : "long cylindrical shell"} of inner diameter ${m(vu(D2, "m"))} (surface 2). Find ${m(self ? "F_{22}" : "F_{21}")}.`);
}

const TRIANGLES = [[3, 4, 5], [1, 1, 1], [2, 3, 4], [5, 5, 8], [1, 2, 2], [4, 5, 6], [5, 6, 8]];
function vfDuct(r: Rng): Draft {
  const s = r.pick([0.1, 0.2, 0.5]);
  const base = r.pick(TRIANGLES);
  const order = r.pick([[0, 1, 2], [1, 2, 0], [2, 0, 1], [0, 2, 1]]);
  const w = order.map((i) => sig(base[i] * s, 3));
  const i = r.int(0, 2);
  const j = r.pick([0, 1, 2].filter((x) => x !== i));
  const k = 3 - i - j;
  const F = (w[i] + w[j] - w[k]) / (2 * w[i]);
  return numeric(F, `F${i + 1}${j + 1}`, `F_{${i + 1}${j + 1}}`, "", [
    `Each flat side sees only the other two: ${m(`F_{${i + 1}${j + 1}} + F_{${i + 1}${k + 1}} = 1`)}, and likewise for the other sides; reciprocity per unit length: ${m("w_iF_{ij} = w_jF_{ji}")}.`,
    `Solving the three summation and three reciprocity equations: ${m(`F_{ij} = \\frac{w_i + w_j - w_k}{2w_i}`)}.`,
    m(`F_{${i + 1}${j + 1}} = \\frac{${g(w[i])} + ${g(w[j])} - ${g(w[k])}}{2(${g(w[i])})} = ${fmt(F)}`),
  ], { ht: "vf", case: "duct", w, i, j },
  `A long duct has a triangular cross-section with flat sides of widths ${m(`w_1 = ${vu(w[0], "m")}`)}, ${m(`w_2 = ${vu(w[1], "m")}`)} and ${m(`w_3 = ${vu(w[2], "m")}`)}. Using only reciprocity and summation, find ${m(`F_{${i + 1}${j + 1}}`)}.`);
}

/** coaxial parallel disks, Table 13.2: from disk i (radius ri) to disk j (radius rj), gap L */
export function fDisks(ri: number, rj: number, L: number): number {
  const Ri = ri / L, Rj = rj / L;
  const S = 1 + (1 + Rj * Rj) / (Ri * Ri);
  return 0.5 * (S - Math.sqrt(S * S - 4 * (rj / ri) ** 2));
}
const DISK_TEX = "F_{ij} = \\tfrac12\\left\\{S - \\left[S^2 - 4(r_j/r_i)^2\\right]^{1/2}\\right\\},\\ S = 1 + \\frac{1 + R_j^2}{R_i^2},\\ R = r/L";

function vfCavity(r: Rng): Draft {
  const rr = r.pick([0.05, 0.1, 0.2, 0.25]);
  const H = r.pick([0.05, 0.1, 0.2, 0.3, 0.5]);
  const F12 = fDisks(rr, rr, H);
  const F13 = 1 - F12;
  const F31 = (rr * F13) / (2 * H); // A1/A3 = πr²/(2πrH)
  const kind = r.pick(["F13", "F31", "F33"] as const);
  const val = kind === "F13" ? F13 : kind === "F31" ? F31 : 1 - 2 * F31;
  const steps = [
    `Close the cavity with an imaginary disk 2 across the opening. The base (1) and opening (2) are coaxial disks, ${m(`R_1 = R_2 = r/H = ${fmt(rr / H, 4)}`)}: ${m(`S = 2 + 1/R^2 = ${fmt(2 + (H / rr) ** 2, 4)}`)}, ${m(`F_{12} = ${fmt(F12, 4)}`)}.`,
    `The base is flat: ${m(`F_{13} = 1 - F_{12} = ${fmt(F13, 4)}`)}.`,
  ];
  if (kind !== "F13") steps.push(`Reciprocity, ${m("A_1 = \\pi r^2")}, ${m("A_3 = 2\\pi rH")}: ${m(`F_{31} = \\frac{A_1F_{13}}{A_3} = \\frac{r}{2H}F_{13} = ${fmt(F31, 4)}`)}.`);
  if (kind === "F33") steps.push(`By symmetry ${m("F_{32} = F_{31}")}; summation: ${m(`F_{33} = 1 - 2F_{31} = ${fmt(val, 4)}`)}.`);
  const want = kind === "F13" ? "from the base to the side wall, F_{13}" : kind === "F31" ? "from the side wall to the base, F_{31}" : "of the side wall to itself, F_{33}";
  return numeric(val, kind.replace("F", "F_"), `F_{${kind.slice(1)}}`, "", steps, { ht: "vf", case: "cavity", r: rr, H, target: kind },
    `A cylindrical cavity has radius ${m(vu(rr, "m"))} and depth ${m(vu(H, "m"))}: base (1), opening (2), side wall (3). For coaxial parallel disks (Table 13.2), ${m(DISK_TEX)}. Find the view factor ${want.replace(/F_\{(\d+)\}/, (s) => m(s))}.`);
}

// ═══ Ch 13 enclosures ══════════════════════════════════════════════════════
const EPS = [0.1, 0.2, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9];
const EB = (T: number) => SIGMA * T ** 4;

function twoSurface(r: Rng): Draft {
  const geo = r.pick(["plates", "cyl", "sph"] as const);
  const e1 = r.pick(EPS), e2 = r.pick(EPS);
  const T1 = r.pick([400, 500, 600, 700, 800, 1000]);
  const T2 = r.pick([77, 250, 300, 350]);
  const D1 = r.pick([0.02, 0.05, 0.1, 0.2]);
  const D2 = sig(D1 * r.pick([1.25, 1.5, 2, 3, 5]), 3);
  let q: number, A1: number, A2: number, label: string, unit: string, desc: string;
  if (geo === "plates") { A1 = 1; A2 = 1; unit = "W/m²"; label = "q″₁₂"; desc = `Two large parallel plates face each other: plate 1 at ${m(vu(T1, "K"))} (${m(`\\varepsilon_1 = ${e1}`)}), plate 2 at ${m(vu(T2, "K"))} (${m(`\\varepsilon_2 = ${e2}`)}). Find the net radiation flux from 1 to 2.`; }
  else if (geo === "cyl") { A1 = PI * D1; A2 = PI * D2; unit = "W/m"; label = "q′₁₂"; desc = `A long tube of diameter ${m(vu(D1, "m"))} at ${m(vu(T1, "K"))} (${m(`\\varepsilon_1 = ${e1}`)}) runs concentrically inside a long tube of inner diameter ${m(vu(D2, "m"))} at ${m(vu(T2, "K"))} (${m(`\\varepsilon_2 = ${e2}`)}); the gap is evacuated. Find the net radiation per metre of length from the inner tube to the outer.`; }
  else { A1 = PI * D1 * D1; A2 = PI * D2 * D2; unit = "W"; label = "q₁₂"; desc = `A sphere of diameter ${m(vu(D1, "m"))} at ${m(vu(T1, "K"))} (${m(`\\varepsilon_1 = ${e1}`)}) sits concentrically inside a spherical shell of inner diameter ${m(vu(D2, "m"))} at ${m(vu(T2, "K"))} (${m(`\\varepsilon_2 = ${e2}`)}); the gap is evacuated. Find the net radiation exchange.`; }
  const R1 = (1 - e1) / (e1 * A1), R12 = 1 / A1, R2 = (1 - e2) / (e2 * A2);
  q = (EB(T1) - EB(T2)) / (R1 + R12 + R2);
  const tex = geo === "plates" ? "q''_{12}" : geo === "cyl" ? "q'_{12}" : "q_{12}";
  const steps = [
    `Two-surface enclosure, ${m("F_{12} = 1")}: three resistances in series, ${m("q_{12} = \\frac{\\sigma(T_1^4 - T_2^4)}{\\frac{1 - \\varepsilon_1}{\\varepsilon_1A_1} + \\frac{1}{A_1F_{12}} + \\frac{1 - \\varepsilon_2}{\\varepsilon_2A_2}}")} (Eq. 13.23).`,
    geo === "plates"
      ? `Per unit area (${m("A_1 = A_2")}): ${m("q''_{12} = \\frac{\\sigma(T_1^4 - T_2^4)}{1/\\varepsilon_1 + 1/\\varepsilon_2 - 1}")}.`
      : `${geo === "cyl" ? "Per metre" : "Areas"}: ${m(`A_1 = ${fmt(A1, 4)}, \\ A_2 = ${fmt(A2, 4)}`)}, so the resistances are ${m(`${fmt(R1, 4)} + ${fmt(R12, 4)} + ${fmt(R2, 4)}`)}.`,
    m(`${tex} = \\frac{5.67\\times10^{-8}(${T1}^4 - ${T2}^4)}{${fmt(R1 + R12 + R2, 4)}} = ${fmt(q)}${u(unit)}`),
  ];
  return numeric(q, label, tex, unit, steps, { ht: "encl", case: "two", geo, e1, e2, T1, T2, D1, D2 }, desc);
}

function shield(r: Rng): Draft {
  const e1 = r.pick(EPS), e2 = r.pick(EPS);
  const ea = r.pick([0.02, 0.05, 0.1, 0.2]);
  const eb = r.chance(0.5) ? ea : r.pick([0.02, 0.05, 0.1, 0.2, 0.5]);
  const T1 = r.pick([400, 500, 600, 800, 1000]);
  const T2 = r.pick([77, 300, 350]);
  const Ra = 1 / e1 + 1 / ea - 1, Rb = 1 / eb + 1 / e2 - 1;
  const q = (EB(T1) - EB(T2)) / (Ra + Rb);
  const wantT = r.chance(0.4);
  const T3 = ((EB(T1) - q * Ra) / SIGMA) ** 0.25;
  const steps = [
    `Shield in series between two large plates (Eq. 13.24–13.25), per unit area: ${m("q''_{12} = \\frac{\\sigma(T_1^4 - T_2^4)}{\\left(\\frac{1}{\\varepsilon_1} + \\frac{1}{\\varepsilon_{3,1}} - 1\\right) + \\left(\\frac{1}{\\varepsilon_{3,2}} + \\frac{1}{\\varepsilon_2} - 1\\right)}")}.`,
    m(`\\left(\\frac{1}{${e1}} + \\frac{1}{${ea}} - 1\\right) + \\left(\\frac{1}{${eb}} + \\frac{1}{${e2}} - 1\\right) = ${fmt(Ra, 4)} + ${fmt(Rb, 4)} = ${fmt(Ra + Rb, 4)}`),
    m(`q''_{12} = \\frac{5.67\\times10^{-8}(${T1}^4 - ${T2}^4)}{${fmt(Ra + Rb, 4)}} = ${fmt(q)}${u("W/m²")}`),
  ];
  if (wantT) steps.push(`The same flux crosses each gap: ${m(`\\sigma T_3^4 = \\sigma T_1^4 - q''_{12}\\left(\\frac{1}{\\varepsilon_1} + \\frac{1}{\\varepsilon_{3,1}} - 1\\right)`)}, so ${m(`T_3 = ${fmt(T3)}${u("K")}`)}.`);
  const sides = ea === eb ? `${m(`\\varepsilon_3 = ${ea}`)} on both sides` : `${m(`\\varepsilon_{3,1} = ${ea}`)} on the side facing plate 1 and ${m(`\\varepsilon_{3,2} = ${eb}`)} facing plate 2`;
  return numeric(wantT ? T3 : q, wantT ? "T₃" : "q″₁₂", wantT ? "T_3" : "q''_{12}", wantT ? "K" : "W/m²", steps,
    { ht: "encl", case: "shield", e1, e2, ea, eb, T1, T2, target: wantT ? "T3" : "q" },
    `Two large parallel plates at ${m(vu(T1, "K"))} (${m(`\\varepsilon_1 = ${e1}`)}) and ${m(vu(T2, "K"))} (${m(`\\varepsilon_2 = ${e2}`)}) are separated by a thin radiation shield with ${sides}. Find ${wantT ? "the shield temperature" : "the net radiation flux between the plates"}.`);
}

function blackDisks(r: Rng): Draft {
  const r1 = r.pick([0.05, 0.1, 0.2, 0.25]);
  const r2 = r.pick([0.05, 0.1, 0.2, 0.25, 0.5]);
  const L = r.pick([0.05, 0.1, 0.2, 0.25, 0.5]);
  const T1 = r.pick([500, 600, 800, 1000, 1200]);
  const T2 = r.pick([300, 350, 400]);
  const F12 = fDisks(r1, r2, L);
  const A1 = PI * r1 * r1;
  const q = A1 * F12 * (EB(T1) - EB(T2));
  return numeric(q, "q₁₂", "q_{12}", "W", [
    m(`R_1 = r_1/L = ${fmt(r1 / L, 4)}, \\quad R_2 = r_2/L = ${fmt(r2 / L, 4)}, \\quad S = 1 + \\frac{1 + R_2^2}{R_1^2} = ${fmt(1 + (1 + (r2 / L) ** 2) / (r1 / L) ** 2, 4)}`),
    m(`F_{12} = \\tfrac12\\left\\{S - \\sqrt{S^2 - 4(r_2/r_1)^2}\\right\\} = ${fmt(F12, 4)}`),
    `Black surfaces: ${m("q_{12} = A_1F_{12}\\sigma(T_1^4 - T_2^4)")} = ${m(`\\pi(${g(r1)})^2(${fmt(F12, 4)})(5.67\\times10^{-8})(${T1}^4 - ${T2}^4) = ${fmt(q)}${u("W")}`)}.`,
  ], { ht: "encl", case: "black-disks", r1, r2, L, T1, T2 },
  `Two black coaxial parallel disks face each other ${m(vu(L, "m"))} apart: disk 1 (radius ${m(vu(r1, "m"))}) at ${m(vu(T1, "K"))} and disk 2 (radius ${m(vu(r2, "m"))}) at ${m(vu(T2, "K"))}. For coaxial disks (Table 13.2), ${m(DISK_TEX)}. Find the net radiation exchange from disk 1 to disk 2.`);
}

function reradiating(r: Rng): Draft {
  const s = r.pick([0.2, 0.5, 1]);
  const base = r.pick(TRIANGLES);
  const w = base.map((x) => sig(x * s, 3)); // sides 1, 2, R
  const F = (i: number, j: number) => (w[i] + w[j] - w[3 - i - j]) / (2 * w[i]);
  const e1 = r.pick(EPS), e2 = r.pick(EPS);
  const T1 = r.pick([800, 1000, 1200, 1500]);
  const T2 = r.pick([400, 500, 600]);
  const [A1, A2] = [w[0], w[1]];
  const R1 = (1 - e1) / (e1 * A1), R2 = (1 - e2) / (e2 * A2);
  const Rmid = 1 / (A1 * F(0, 1) + 1 / (1 / (A1 * F(0, 2)) + 1 / (A2 * F(1, 2))));
  const q = (EB(T1) - EB(T2)) / (R1 + Rmid + R2);
  const wantT = r.chance(0.35);
  const J1 = EB(T1) - q * R1, J2 = EB(T2) + q * R2;
  const a = A1 * F(0, 2), b = A2 * F(1, 2);
  const JR = (a * J1 + b * J2) / (a + b);
  const TR = (JR / SIGMA) ** 0.25;
  const steps = [
    `View factors from the triangle rule ${m("F_{ij} = (w_i + w_j - w_k)/(2w_i)")}: ${m(`F_{12} = ${fmt(F(0, 1), 4)}, \\ F_{1R} = ${fmt(F(0, 2), 4)}, \\ F_{2R} = ${fmt(F(1, 2), 4)}`)}.`,
    `Reradiating surface (Eq. 13.30), per metre: ${m("q_1 = \\frac{E_{b1} - E_{b2}}{\\frac{1 - \\varepsilon_1}{\\varepsilon_1A_1} + \\left[A_1F_{12} + \\left(\\frac{1}{A_1F_{1R}} + \\frac{1}{A_2F_{2R}}\\right)^{-1}\\right]^{-1} + \\frac{1 - \\varepsilon_2}{\\varepsilon_2A_2}}")}.`,
    m(`q'_1 = \\frac{5.67\\times10^{-8}(${T1}^4 - ${T2}^4)}{${fmt(R1, 4)} + ${fmt(Rmid, 4)} + ${fmt(R2, 4)}} = ${fmt(q)}${u("W/m")}`),
  ];
  if (wantT) steps.push(`${m(`J_1 = E_{b1} - q_1\\frac{1 - \\varepsilon_1}{\\varepsilon_1A_1} = ${fmt(J1, 4)}`)}, ${m(`J_2 = E_{b2} + q_1\\frac{1 - \\varepsilon_2}{\\varepsilon_2A_2} = ${fmt(J2, 4)}`)}; the reradiating node has no net flow, ${m(`J_R = \\frac{A_1F_{1R}J_1 + A_2F_{2R}J_2}{A_1F_{1R} + A_2F_{2R}} = ${fmt(JR, 4)} = \\sigma T_R^4`)}, ${m(`T_R = ${fmt(TR)}${u("K")}`)}.`);
  return numeric(wantT ? TR : q, wantT ? "T_R" : "q′₁", wantT ? "T_R" : "q'_1", wantT ? "K" : "W/m", steps,
    { ht: "encl", case: "rerad", w, e1, e2, T1, T2, target: wantT ? "TR" : "q" },
    `A long furnace duct has a triangular cross-section. Side 1 (width ${m(vu(w[0], "m"))}) is a heater at ${m(vu(T1, "K"))}, ${m(`\\varepsilon_1 = ${e1}`)}; side 2 (${m(vu(w[1], "m"))}) is the load at ${m(vu(T2, "K"))}, ${m(`\\varepsilon_2 = ${e2}`)}; side R (${m(vu(w[2], "m"))}) is insulated and reradiating. Find ${wantT ? "the temperature of the reradiating wall" : "the net radiation per metre of duct from the heater"}.`);
}

export const HEAT2_TEMPLATES: Record<string, (r: Rng) => Draft> = {
  "ht-bi": lumpedBi,
  "ht-lumped-time": lumpedTime,
  "ht-lumped-temp": lumpedTemp,
  "ht-lumped-energy": lumpedQ,
  "ht-ot-wall-center": otCenter("wall"),
  "ht-ot-wall-surface": otWallSurface,
  "ht-ot-wall-time": otWallTime,
  "ht-ot-cyl-center": otCenter("cyl"),
  "ht-ot-sphere-center": otCenter("sph"),
  "ht-erf-temp": erfTemp,
  "ht-erf-flux": erfFlux,
  "ht-erf-depth": erfDepth,
  "ht-erf-time": erfTime,
  "ht-erf-contact": contactTemp,
  "ht-plate-lam": plateLam,
  "ht-plate-mixed": plateMixed,
  "ht-cyl-cb": cylCB,
  "ht-sphere-whitaker": sphereWhitaker,
  "ht-int-re": intRe,
  "ht-tm-flux": tmFlux,
  "ht-tm-ts": tmTs,
  "ht-dittus": dittus,
  "ht-lam-fd": lamFd,
  "ht-ra": freeRa,
  "ht-chu-vertical": chuVertical,
  "ht-free-horiz": freeHoriz,
  "ht-free-cyl": freeCyl,
  "ht-lmtd-counter": lmtd(true),
  "ht-lmtd-parallel": lmtd(false),
  "ht-ntu-eff": ntuEff,
  "ht-ntu-outlet": ntuOutlet,
  "ht-shell-tube": shellTube,
  "ht-vf-reciprocity": vfReciprocity,
  "ht-vf-concentric": vfConcentric,
  "ht-vf-duct": vfDuct,
  "ht-vf-cavity": vfCavity,
  "ht-two-surface": twoSurface,
  "ht-shield": shield,
  "ht-black-disks": blackDisks,
  "ht-reradiating": reradiating,
};
