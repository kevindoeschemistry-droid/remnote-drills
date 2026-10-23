// Incropera Ch 1–4 (conduction), Level 1 — numeric answers checked to 1%.
// Each problem carries its inputs in SI in `meta` (with a `ht` case name) so the
// sympy verifier can recompute the answer from the governing equation on its own.
import { Rng } from "./rng";
import type { Draft } from "./types";
import { m } from "./tex";
import { require_ } from "./reject";

const SIGMA = 5.67e-8;
const PI = Math.PI;

// ── formatting ─────────────────────────────────────────────────────────────
/** a number for display: 3 significant figures, scientific outside [1e-3, 1e6) */
export function fmt(x: number, sig = 3): string {
  if (x === 0) return "0";
  const ax = Math.abs(x);
  if (ax >= 1e6 || ax < 1e-3) {
    const e = Math.floor(Math.log10(ax));
    const mant = Number((x / 10 ** e).toPrecision(sig));
    return `${mant} \\times 10^{${e}}`;
  }
  const v = Number(x.toPrecision(sig));
  // thin-space thousands for readability, no trailing zeros
  const [i, f] = String(Math.abs(v)).split(".");
  const ii = i.length > 4 ? i.replace(/\B(?=(\d{3})+(?!\d))/g, "\\,") : i;
  return `${v < 0 ? "-" : ""}${ii}${f ? `.${f}` : ""}`;
}
/** a given value as written in a prompt (inputs are already "nice") */
const g = (x: number) => fmt(x, 4);
const K = (c: number) => c + 273.15;

const U: Record<string, string> = {
  W: "\\mathrm{W}",
  "W/m": "\\mathrm{W/m}",
  "W/m²": "\\mathrm{W/m^2}",
  "W/m³": "\\mathrm{W/m^3}",
  "W/m²·K": "\\mathrm{W/m^2\\cdot K}",
  "W/m·K": "\\mathrm{W/m\\cdot K}",
  "°C": "^\\circ\\mathrm{C}",
  K: "\\mathrm{K}",
  "K/s": "\\mathrm{K/s}",
  "m⁻¹": "\\mathrm{m^{-1}}",
  mm: "\\mathrm{mm}",
  "%": "\\%",
  "m²·K/W": "\\mathrm{m^2\\cdot K/W}",
};
const u = (unit: string) => `\\,${U[unit] ?? `\\mathrm{${unit}}`}`;
/** value with unit, in math */
const vu = (x: number, unit: string) => `${g(x)}${u(unit)}`;

function numeric(
  val: number,
  label: string,
  labelTex: string,
  unit: string,
  steps: string[],
  meta: Record<string, unknown>,
  prompt: string
): Draft {
  require_(Number.isFinite(val));
  return {
    prompt,
    answer: { kind: "expression", ref: `${val}`, vars: [], tol: 0.01, rel: true, label, unit },
    answerTex: `${labelTex} = ${fmt(val)}${u(unit)}`,
    steps,
    meta,
  };
}

// ── materials (Incropera Appendix A, rounded) ──────────────────────────────
const SOLIDS = [
  { name: "fireclay brick", k: 1.0 },
  { name: "window glass", k: 1.4 },
  { name: "concrete", k: 1.4 },
  { name: "oak", k: 0.17 },
  { name: "AISI 304 stainless steel", k: 15 },
  { name: "plain carbon steel", k: 60 },
  { name: "aluminum", k: 237 },
  { name: "copper", k: 400 },
  { name: "glass-fiber insulation", k: 0.04 },
];
const INSULATION = [
  { name: "glass-fiber insulation", k: 0.038 },
  { name: "polystyrene foam", k: 0.027 },
  { name: "calcium silicate", k: 0.055 },
  { name: "magnesia (85%)", k: 0.05 },
];

// ═══ §1.2 rate equations ════════════════════════════════════════════════════
function rateCond(r: Rng): Draft {
  const mat = r.pick(SOLIDS);
  const Lcm = r.pick([1, 2, 5, 10, 15, 20]);
  const L = Lcm / 100;
  const T1 = r.pick([40, 60, 80, 100, 150, 200, 300]);
  const T2 = T1 - r.pick([10, 15, 20, 25, 30, 40, 50]);
  const flux = (mat.k * (T1 - T2)) / L;
  const variant = r.pick(["flux", "rate", "k", "T2"] as const);
  const A = r.pick([0.5, 1.2, 2, 4, 10]);
  const base = `A ${Lcm}-cm-thick slab of ${mat.name}`;
  const fourier = `Fourier's law: ${m("q''_x = k\\frac{T_1 - T_2}{L}")}, with ${m(`L = ${g(L)}\\,\\mathrm{m}`)} (not ${Lcm} cm).`;
  const meta = { ht: "cond", k: mat.k, L, T1, T2, A, target: variant };
  if (variant === "flux")
    return numeric(flux, "q″", "q''_x", "W/m²", [
      fourier,
      m(`q''_x = ${g(mat.k)}\\cdot\\frac{${T1} - ${T2}}{${g(L)}} = ${fmt(flux)}${u("W/m²")}`),
    ], meta, `${base} (${m(`k = ${vu(mat.k, "W/m·K")}`)}) has faces at ${m(vu(T1, "°C"))} and ${m(vu(T2, "°C"))}. Find the heat flux ${m("q''_x")}.`);
  if (variant === "rate")
    return numeric(flux * A, "q", "q", "W", [
      fourier,
      m(`q''_x = ${fmt(flux)}${u("W/m²")}`),
      `${m(`q = q''_x A = ${fmt(flux)} \\times ${g(A)} = ${fmt(flux * A)}${u("W")}`)}.`,
    ], meta, `${base} (${m(`k = ${vu(mat.k, "W/m·K")}`)}), ${m(`${g(A)}\\,\\mathrm{m^2}`)} in area, has faces at ${m(vu(T1, "°C"))} and ${m(vu(T2, "°C"))}. Find the heat rate ${m("q")}.`);
  if (variant === "k")
    return numeric(mat.k, "k", "k", "W/m·K", [
      fourier,
      m(`k = \\frac{q''_x L}{T_1 - T_2} = \\frac{${fmt(flux)} \\times ${g(L)}}{${T1 - T2}} = ${fmt(mat.k)}${u("W/m·K")}`),
    ], meta, `A ${Lcm}-cm-thick slab of an unknown material carries a steady heat flux of ${m(vu(Number(flux.toPrecision(4)), "W/m²"))} with faces at ${m(vu(T1, "°C"))} and ${m(vu(T2, "°C"))}. Find its thermal conductivity.`);
  const q4 = Number(flux.toPrecision(4));
  const T2v = T1 - (q4 * L) / mat.k;
  return numeric(T2v, "T₂", "T_2", "°C", [
    fourier,
    m(`T_2 = T_1 - \\frac{q''_x L}{k} = ${T1} - \\frac{${g(q4)} \\times ${g(L)}}{${g(mat.k)}} = ${fmt(T2v)}${u("°C")}`),
  ], { ...meta, flux: q4 }, `${base} (${m(`k = ${vu(mat.k, "W/m·K")}`)}) carries ${m(vu(q4, "W/m²"))}; its hot face is at ${m(vu(T1, "°C"))}. Find the cold-face temperature ${m("T_2")}.`);
}

function rateConv(r: Rng): Draft {
  const [h, how] = r.pick([
    [5, "free convection in air"], [10, "free convection in air"], [25, "forced air"], [50, "forced air"],
    [100, "forced air"], [250, "forced air"], [500, "water"], [1000, "water"],
  ] as [number, string][]);
  const Ts = r.pick([40, 60, 80, 100, 150, 200]);
  const Tinf = r.pick([15, 20, 25, 27, 30]);
  const variant = r.pick(["plate", "cyl", "h", "Ts"] as const);
  if (variant === "cyl") {
    const Dmm = r.pick([1, 2, 5, 10, 25, 50]);
    const L = r.pick([0.2, 0.5, 1, 2]);
    const A = PI * (Dmm / 1000) * L;
    const q = h * A * (Ts - Tinf);
    return numeric(q, "q", "q", "W", [
      `Newton's law of cooling: ${m("q = hA(T_s - T_\\infty)")}. The area is the lateral surface of the cylinder: ${m(`A = \\pi DL = \\pi(${g(Dmm / 1000)})(${g(L)}) = ${fmt(A)}\\,\\mathrm{m^2}`)}.`,
      m(`q = ${h}\\times${fmt(A)}\\times(${Ts} - ${Tinf}) = ${fmt(q)}${u("W")}`),
    ], { ht: "conv", h, A, Ts, Tinf, target: "q" },
    `A ${Dmm}-mm-diameter, ${g(L)}-m-long rod at ${m(vu(Ts, "°C"))} is cooled by ${how} at ${m(vu(Tinf, "°C"))} with ${m(`h = ${vu(h, "W/m²·K")}`)}. Find the heat rate from its lateral surface.`);
  }
  const A = r.pick([0.25, 0.5, 1, 1.5, 2]);
  const q = h * A * (Ts - Tinf);
  const meta = { ht: "conv", h, A, Ts, Tinf, target: variant === "plate" ? "q" : variant };
  if (variant === "plate")
    return numeric(q, "q", "q", "W", [
      m("q = hA(T_s - T_\\infty)"),
      m(`q = ${h}\\times${g(A)}\\times(${Ts} - ${Tinf}) = ${fmt(q)}${u("W")}`),
    ], meta, `A ${m(`${g(A)}\\,\\mathrm{m^2}`)} plate at ${m(vu(Ts, "°C"))} is cooled by ${how} at ${m(vu(Tinf, "°C"))}, ${m(`h = ${vu(h, "W/m²·K")}`)}. Find the convection heat rate.`);
  if (variant === "h")
    return numeric(h, "h", "h", "W/m²·K", [
      m("h = \\frac{q}{A(T_s - T_\\infty)}"),
      m(`h = \\frac{${g(q)}}{${g(A)}\\times(${Ts} - ${Tinf})} = ${fmt(h)}${u("W/m²·K")}`),
    ], meta, `A heater keeps a ${m(`${g(A)}\\,\\mathrm{m^2}`)} plate at ${m(vu(Ts, "°C"))} in fluid at ${m(vu(Tinf, "°C"))} using ${m(vu(q, "W"))} (all lost by convection). Find the convection coefficient ${m("h")}.`);
  return numeric(Ts, "Tₛ", "T_s", "°C", [
    m("T_s = T_\\infty + \\frac{q}{hA}"),
    m(`T_s = ${Tinf} + \\frac{${g(q)}}{${h}\\times${g(A)}} = ${fmt(Ts)}${u("°C")}`),
  ], meta, `A ${m(`${g(A)}\\,\\mathrm{m^2}`)} plate dissipates ${m(vu(q, "W"))} by convection to fluid at ${m(vu(Tinf, "°C"))} with ${m(`h = ${vu(h, "W/m²·K")}`)}. Find the plate temperature.`);
}

function rateRad(r: Rng): Draft {
  const eps = r.pick([0.2, 0.5, 0.7, 0.8, 0.9, 0.95]);
  const Ts = r.pick([100, 150, 200, 250, 300, 400, 500]);
  const Tsur = r.pick([0, 15, 20, 25, 30]);
  const variant = r.pick(["flux", "flux", "hr"] as const);
  const Tk = K(Ts), Tsk = K(Tsur);
  if (variant === "hr") {
    const hr = eps * SIGMA * (Tk + Tsk) * (Tk * Tk + Tsk * Tsk);
    return numeric(hr, "h_r", "h_r", "W/m²·K", [
      `Temperatures in kelvin: ${m(`T_s = ${g(Tk)}\\,\\mathrm{K}`)}, ${m(`T_{sur} = ${g(Tsk)}\\,\\mathrm{K}`)}.`,
      m(`h_r = \\varepsilon\\sigma(T_s + T_{sur})(T_s^2 + T_{sur}^2) = ${eps}(5.67\\times10^{-8})(${g(Tk + Tsk)})(${fmt(Tk * Tk + Tsk * Tsk, 4)}) = ${fmt(hr)}${u("W/m²·K")}`),
    ], { ht: "hr", eps, Ts: Tk, Tsur: Tsk },
    `A surface with ${m(`\\varepsilon = ${eps}`)} at ${m(vu(Ts, "°C"))} sees large surroundings at ${m(vu(Tsur, "°C"))}. Find the radiation heat transfer coefficient ${m("h_r")}.`);
  }
  const q = eps * SIGMA * (Tk ** 4 - Tsk ** 4);
  return numeric(q, "q″_rad", "q''_{rad}", "W/m²", [
    `Kelvin, always, for radiation: ${m(`T_s = ${g(Tk)}\\,\\mathrm{K}`)}, ${m(`T_{sur} = ${g(Tsk)}\\,\\mathrm{K}`)}.`,
    m(`q''_{rad} = \\varepsilon\\sigma(T_s^4 - T_{sur}^4) = ${eps}(5.67\\times10^{-8})(${fmt(Tk ** 4)} - ${fmt(Tsk ** 4)}) = ${fmt(q)}${u("W/m²")}`),
  ], { ht: "rad", eps, Ts: Tk, Tsur: Tsk },
  `A surface with emissivity ${m(`${eps}`)} is at ${m(vu(Ts, "°C"))} in large surroundings at ${m(vu(Tsur, "°C"))}. Find the net radiation heat flux from the surface.`);
}

// ═══ §1.3 energy balances ═══════════════════════════════════════════════════
function ebSurface(r: Rng): Draft {
  const mat = r.pick(SOLIDS.filter((s) => s.k >= 0.15 && s.k <= 2));
  const Lcm = r.pick([10, 15, 20, 25]);
  const L = Lcm / 100;
  const T1 = r.pick([100, 150, 200, 300, 400]);
  const T2 = r.pick([40, 50, 60, 80]);
  const Tinf = r.pick([20, 25]);
  const eps = r.pick([0.8, 0.85, 0.9]);
  const cond = (mat.k * (T1 - T2)) / L;
  const rad = eps * SIGMA * (K(T2) ** 4 - K(Tinf) ** 4);
  const h = (cond - rad) / (T2 - Tinf);
  require_(h > 2 && h < 300);
  return numeric(h, "h", "h", "W/m²·K", [
    `Surface energy balance at the outer face (no storage, no generation): ${m("q''_{cond} = q''_{conv} + q''_{rad}")}.`,
    m(`q''_{cond} = k\\frac{T_1 - T_2}{L} = ${g(mat.k)}\\cdot\\frac{${T1} - ${T2}}{${g(L)}} = ${fmt(cond)}${u("W/m²")}`),
    m(`q''_{rad} = \\varepsilon\\sigma(T_2^4 - T_{sur}^4) = ${eps}(5.67\\times10^{-8})(${g(K(T2))}^4 - ${g(K(Tinf))}^4) = ${fmt(rad)}${u("W/m²")}`),
    m(`h = \\frac{q''_{cond} - q''_{rad}}{T_2 - T_\\infty} = \\frac{${fmt(cond)} - ${fmt(rad)}}{${T2 - Tinf}} = ${fmt(h)}${u("W/m²·K")}`),
  ], { ht: "eb-surface", k: mat.k, L, T1, T2, Tinf, eps },
  `The inner face of a ${Lcm}-cm ${mat.name} wall (${m(`k = ${vu(mat.k, "W/m·K")}`)}) is at ${m(vu(T1, "°C"))}; the outer face is at ${m(vu(T2, "°C"))} (${m(`\\varepsilon = ${eps}`)}), exposed to air and surroundings both at ${m(vu(Tinf, "°C"))}. Find the outside convection coefficient ${m("h")}.`);
}

function ebWire(r: Rng): Draft {
  const Dmm = r.pick([1, 2, 3, 5]);
  const D = Dmm / 1000;
  const I = r.pick([5, 10, 15, 20, 25]);
  const Re = r.pick([0.01, 0.02, 0.05, 0.1, 0.2]); // Ω/m
  const Tinf = r.pick([20, 25]);
  const gen = I * I * Re; // W/m
  const withRad = r.chance(0.4);
  if (!withRad) {
    const h = r.pick([10, 25, 50, 100, 250]);
    const Ts = Tinf + gen / (h * PI * D);
    require_(Ts < 600 && Ts - Tinf > 3);
    return numeric(Ts, "Tₛ", "T_s", "°C", [
      `Per unit length, steady state: electrical dissipation = convection, ${m("I^2R'_e = h\\pi D(T_s - T_\\infty)")}.`,
      m(`I^2R'_e = ${I}^2 \\times ${g(Re)} = ${fmt(gen)}${u("W/m")}`),
      m(`T_s = T_\\infty + \\frac{I^2R'_e}{h\\pi D} = ${Tinf} + \\frac{${fmt(gen)}}{${h}\\pi(${g(D)})} = ${fmt(Ts)}${u("°C")}`),
    ], { ht: "eb-wire", I, Re, D, h, Tinf, target: "Ts" },
    `A ${Dmm}-mm-diameter wire with electrical resistance ${m(`${g(Re)}\\,\\Omega/\\mathrm{m}`)} carries ${m(`${I}\\,\\mathrm{A}`)} in air at ${m(vu(Tinf, "°C"))} with ${m(`h = ${vu(h, "W/m²·K")}`)}. Neglecting radiation, find the steady wire temperature.`);
  }
  const Ts = r.pick([60, 80, 100, 150, 200]);
  const eps = r.pick([0.6, 0.8, 0.9]);
  const radPerL = eps * SIGMA * PI * D * (K(Ts) ** 4 - K(Tinf) ** 4);
  const h = (gen - radPerL) / (PI * D * (Ts - Tinf));
  require_(h > 3 && h < 2000);
  return numeric(h, "h", "h", "W/m²·K", [
    `Per unit length: ${m("I^2R'_e = h\\pi D(T_s - T_\\infty) + \\varepsilon\\sigma\\pi D(T_s^4 - T_{sur}^4)")}.`,
    `${m(`I^2R'_e = ${fmt(gen)}${u("W/m")}`)}; radiation ${m(`= ${eps}(5.67\\times10^{-8})\\pi(${g(D)})(${g(K(Ts))}^4 - ${g(K(Tinf))}^4) = ${fmt(radPerL)}${u("W/m")}`)}.`,
    m(`h = \\frac{${fmt(gen)} - ${fmt(radPerL)}}{\\pi(${g(D)})(${Ts} - ${Tinf})} = ${fmt(h)}${u("W/m²·K")}`),
  ], { ht: "eb-wire", I, Re, D, Ts, Tinf, eps, target: "h" },
  `A ${Dmm}-mm wire (${m(`R'_e = ${g(Re)}\\,\\Omega/\\mathrm{m}`)}, ${m(`\\varepsilon = ${eps}`)}) carries ${m(`${I}\\,\\mathrm{A}`)} and runs at ${m(vu(Ts, "°C"))} in air and surroundings at ${m(vu(Tinf, "°C"))}. Find the convection coefficient.`);
}

// ═══ Ch 2 heat diffusion equation ═══════════════════════════════════════════
interface Profile { a: number; b: number; c: number; L: number; k: number; tex: string }
function profile(r: Rng): Profile {
  const a = r.pick([100, 150, 200, 250, 300]);
  const b = r.pick([-200, -150, -100, -50, 0, 50, 100, 200]);
  const c = r.pick([-2000, -1500, -1000, -800, -500, -200, 200, 500]);
  const L = r.pick([0.05, 0.1, 0.2, 0.25]);
  const k = r.pick([1.5, 5, 15, 25, 40, 60]);
  const tex = `T(x) = ${a}${b ? (b > 0 ? ` + ${b}x` : ` - ${-b}x`) : ""}${c > 0 ? ` + ${c}x^2` : ` - ${-c}x^2`}`;
  return { a, b, c, L, k, tex };
}
const profStem = (P: Profile) =>
  `At some instant the temperature in a ${g(P.L)}-m-thick plane wall (${m(`k = ${vu(P.k, "W/m·K")}`)}) is ${m(P.tex)} (${m("^\\circ\\mathrm{C}")}, ${m("x")} in m, ${m(`0 \\le x \\le ${g(P.L)}`)}).`;

function heGeneration(r: Rng): Draft {
  const P = profile(r);
  const qdot = -2 * P.k * P.c;
  return numeric(qdot, "q̇", "\\dot q", "W/m³", [
    `Steady, 1-D, constant ${m("k")}: ${m("\\frac{d^2T}{dx^2} + \\frac{\\dot q}{k} = 0")}, so ${m("\\dot q = -k\\frac{d^2T}{dx^2}")}.`,
    m(`\\frac{d^2T}{dx^2} = 2(${P.c}) = ${2 * P.c}\\,\\mathrm{K/m^2}`),
    `${m(`\\dot q = -${g(P.k)}\\times(${2 * P.c}) = ${fmt(qdot)}${u("W/m³")}`)}${qdot < 0 ? " — negative: the wall is a heat sink (e.g. an endothermic reaction)." : "."}`,
  ], { ht: "he-gen", ...P },
  `${profStem(P).replace("At some instant the", "The steady")} Find the volumetric generation rate ${m("\\dot q")}.`);
}

function heFlux(r: Rng): Draft {
  const P = profile(r);
  const atL = r.chance(0.5);
  const x = atL ? P.L : 0;
  const dTdx = P.b + 2 * P.c * x;
  const q = -P.k * dTdx;
  require_(Math.abs(q) > 1);
  return numeric(q, "q″ₓ", "q''_x", "W/m²", [
    `Fourier: ${m("q''_x = -k\\frac{dT}{dx}")}, positive in ${m("+x")}.`,
    m(`\\frac{dT}{dx} = ${P.b} + 2(${P.c})x \\;\\Rightarrow\\; \\left.\\frac{dT}{dx}\\right|_{x=${g(x)}} = ${fmt(dTdx)}\\,\\mathrm{K/m}`),
    `${m(`q''_x = -${g(P.k)}\\times(${fmt(dTdx)}) = ${fmt(q)}${u("W/m²")}`)}${q < 0 ? ` — negative, so heat flows in the ${m("-x")} direction there.` : "."}`,
  ], { ht: "he-flux", ...P, x },
  `${profStem(P)} Find the heat flux ${m("q''_x")} at ${m(`x = ${atL ? "L" : "0"}`)} (positive in ${m("+x")}).`);
}

function heDTdt(r: Rng): Draft {
  const P = profile(r);
  const qdot = r.pick([1e4, 5e4, 1e5, 2e5, 5e5]);
  const [rho, cp, name, kMat] = r.pick([[7900, 477, "stainless steel", 15], [7850, 434, "carbon steel", 60], [2300, 880, "concrete", 1.4]] as [number, number, string, number][]);
  P.k = kMat;
  const num = P.k * 2 * P.c + qdot;
  require_(Math.abs(num) > 0.1 * Math.max(Math.abs(P.k * 2 * P.c), qdot));
  const rate = num / (rho * cp);
  return numeric(rate, "∂T/∂t", "\\partial T/\\partial t", "K/s", [
    `Heat equation: ${m("\\rho c_p\\frac{\\partial T}{\\partial t} = k\\frac{\\partial^2T}{\\partial x^2} + \\dot q")}.`,
    m(`k\\frac{\\partial^2T}{\\partial x^2} = ${g(P.k)}\\times${2 * P.c} = ${fmt(P.k * 2 * P.c)}${u("W/m³")}`),
    m(`\\frac{\\partial T}{\\partial t} = \\frac{${fmt(P.k * 2 * P.c)} + ${fmt(qdot)}}{${rho}\\times${cp}} = ${fmt(rate)}${u("K/s")}`),
    `Same at every ${m("x")}, because ${m("\\partial^2T/\\partial x^2")} is constant for a quadratic profile.`,
  ], { ht: "he-dTdt", ...P, qdot, rho, cp },
  `${profStem(P).replace("plane wall", `${name} plane wall`)} It generates ${m(`\\dot q = ${vu(qdot, "W/m³")}`)}; ${m(`\\rho = ${rho}\\,\\mathrm{kg/m^3}`)}, ${m(`c_p = ${cp}\\,\\mathrm{J/kg\\cdot K}`)}. Find ${m("\\partial T/\\partial t")} at that instant.`);
}

// ═══ §3.1 plane & composite walls ═══════════════════════════════════════════
interface Layer { name: string; k: number; L: number }
function layers(r: Rng, n: number): Layer[] {
  const opts = [
    { name: "plaster", k: 0.17, L: [1, 2] },
    { name: "glass-fiber insulation", k: 0.038, L: [5, 8, 10] },
    { name: "brick", k: 0.72, L: [10, 15, 20] },
    { name: "plywood", k: 0.12, L: [1, 2] },
    { name: "concrete", k: 1.4, L: [10, 15, 20] },
    { name: "steel", k: 50, L: [0.5, 1] },
  ];
  const picks: Layer[] = [];
  while (picks.length < n) {
    const o = r.pick(opts);
    if (picks.some((p) => p.name === o.name)) continue;
    picks.push({ name: o.name, k: o.k, L: r.pick(o.L) / 100 });
  }
  return picks;
}

function wall(r: Rng): Draft {
  const Ls = layers(r, r.pick([2, 3]));
  const hi = r.pick([5, 8, 10]);
  const ho = r.pick([20, 25, 40]);
  const Ti = r.pick([20, 22, 25]);
  const To = r.pick([-15, -10, -5, 0]);
  const Rs = [1 / hi, ...Ls.map((l) => l.L / l.k), 1 / ho];
  const Rtot = Rs.reduce((s, x) => s + x, 0);
  const flux = (Ti - To) / Rtot;
  const target = r.pick(["flux", "flux", "U", "Tsi", "T12"] as const);
  const desc = Ls.map((l, i) => `${i ? (i === Ls.length - 1 ? ", and " : ", ") : ""}${g(l.L * 100)} cm of ${l.name} (${m(`k = ${g(l.k)}`)})`).join("");
  const prompt = (ask: string) =>
    `A wall is, from inside to outside, ${desc} (W/m·K). Inside air ${m(vu(Ti, "°C"))} with ${m(`h_i = ${hi}`)}; outside air ${m(vu(To, "°C"))} with ${m(`h_o = ${ho}`)} (${m("\\mathrm{W/m^2\\cdot K}")}). ${ask}`;
  const network = [
    `Series resistances per unit area: ${m(`R''_{tot} = \\frac{1}{h_i} + ${Ls.map((_, i) => `\\frac{L_${i + 1}}{k_${i + 1}}`).join(" + ")} + \\frac{1}{h_o}`)}.`,
    m(`R''_{tot} = ${Rs.map((x) => fmt(x, 3)).join(" + ")} = ${fmt(Rtot, 4)}${u("m²·K/W")}`),
  ];
  const meta = { ht: "wall", layers: Ls.map((l) => [l.k, l.L]), hi, ho, Ti, To, target };
  if (target === "U")
    return numeric(1 / Rtot, "U", "U", "W/m²·K", [...network, m(`U = \\frac{1}{R''_{tot}} = ${fmt(1 / Rtot)}${u("W/m²·K")}`)], meta,
      prompt(`Find the overall heat transfer coefficient ${m("U")}.`));
  const fluxSteps = [...network, m(`q'' = \\frac{T_{\\infty,i} - T_{\\infty,o}}{R''_{tot}} = \\frac{${Ti} - (${To})}{${fmt(Rtot, 4)}} = ${fmt(flux)}${u("W/m²")}`)];
  if (target === "flux") return numeric(flux, "q″", "q''", "W/m²", fluxSteps, meta, prompt("Find the heat loss per unit area."));
  const Tsi = Ti - flux / hi;
  if (target === "Tsi")
    return numeric(Tsi, "T_s,i", "T_{s,i}", "°C", [...fluxSteps, `Same ${m("q''")} through every resistance: ${m(`T_{s,i} = T_{\\infty,i} - \\frac{q''}{h_i} = ${Ti} - \\frac{${fmt(flux)}}{${hi}} = ${fmt(Tsi)}${u("°C")}`)}.`], meta,
      prompt("Find the inside surface temperature."));
  const T12 = Tsi - (flux * Ls[0].L) / Ls[0].k;
  return numeric(T12, "T₁₂", "T_{12}", "°C", [
    ...fluxSteps,
    m(`T_{s,i} = ${Ti} - \\frac{${fmt(flux)}}{${hi}} = ${fmt(Tsi)}${u("°C")}`),
    m(`T_{12} = T_{s,i} - q''\\frac{L_1}{k_1} = ${fmt(Tsi, 4)} - ${fmt(flux)}\\times${fmt(Ls[0].L / Ls[0].k, 3)} = ${fmt(T12)}${u("°C")}`),
  ], meta, prompt(`Find the temperature at the ${Ls[0].name}–${Ls[1].name} interface.`));
}

function wallContact(r: Rng): Draft {
  const [m1, m2] = r.pick([
    [{ name: "aluminum", k: 237 }, { name: "aluminum", k: 237 }],
    [{ name: "copper", k: 400 }, { name: "aluminum", k: 237 }],
    [{ name: "stainless steel", k: 15 }, { name: "stainless steel", k: 15 }],
    [{ name: "stainless steel", k: 15 }, { name: "aluminum", k: 237 }],
  ]);
  const L1 = r.pick([5, 10, 20]) / 1000;
  const L2 = r.pick([5, 10, 20]) / 1000;
  const Rtc = r.pick([0.5e-4, 1e-4, 2e-4, 3e-4, 5e-4]);
  const T1 = r.pick([100, 150, 200]);
  const T3 = r.pick([20, 25, 30, 40]);
  const Rtot = L1 / m1.k + Rtc + L2 / m2.k;
  const flux = (T1 - T3) / Rtot;
  const dropTarget = r.chance(0.5);
  const steps = [
    `Series: ${m("R''_{tot} = \\frac{L_1}{k_1} + R''_{t,c} + \\frac{L_2}{k_2}")}.`,
    m(`R''_{tot} = ${fmt(L1 / m1.k, 3)} + ${fmt(Rtc, 3)} + ${fmt(L2 / m2.k, 3)} = ${fmt(Rtot, 4)}${u("m²·K/W")}`),
    m(`q'' = \\frac{${T1} - ${T3}}{${fmt(Rtot, 4)}} = ${fmt(flux)}${u("W/m²")}`),
  ];
  const prompt = `Two plates are pressed together: ${m(`${L1 * 1000}`)}-mm ${m1.name} (${m(`k = ${m1.k}`)}) and ${m(`${L2 * 1000}`)}-mm ${m2.name} (${m(`k = ${m2.k}`)}, W/m·K), with contact resistance ${m(`R''_{t,c} = ${fmt(Rtc)}${u("m²·K/W")}`)}. The outer faces are at ${m(vu(T1, "°C"))} and ${m(vu(T3, "°C"))}.`;
  const meta = { ht: "contact", k1: m1.k, k2: m2.k, L1, L2, Rtc, T1, T3, target: dropTarget ? "drop" : "flux" };
  if (!dropTarget) return numeric(flux, "q″", "q''", "W/m²", steps, meta, `${prompt} Find the heat flux.`);
  const drop = flux * Rtc;
  return numeric(drop, "ΔT_c", "\\Delta T_c", "K", [...steps, `${m(`\\Delta T_c = q''R''_{t,c} = ${fmt(flux)}\\times${fmt(Rtc)} = ${fmt(drop)}${u("K")}`)} — with metals this thin, the contact is often the biggest resistance.`],
    meta, `${prompt} Find the temperature drop across the contact.`);
}

// ═══ §3.3 radial systems ════════════════════════════════════════════════════
function cylInsulated(r: Rng): Draft {
  const ins = r.pick(INSULATION);
  const r1 = r.pick([10, 15, 25, 50]) / 1000; // pipe outer radius
  const t = r.pick([10, 20, 25, 50]) / 1000;
  const r2 = r1 + t;
  const Ts = r.pick([100, 150, 200, 250]);
  const Tinf = r.pick([20, 25]);
  const h = r.pick([5, 10, 15, 25]);
  const Rcond = Math.log(r2 / r1) / (2 * PI * ins.k);
  const Rconv = 1 / (2 * PI * r2 * h);
  const qp = (Ts - Tinf) / (Rcond + Rconv);
  const outer = r.chance(0.4);
  const steps = [
    `Per unit length: ${m("R'_{cond} = \\frac{\\ln(r_2/r_1)}{2\\pi k}")}, ${m("R'_{conv} = \\frac{1}{2\\pi r_2 h}")} — radii in metres, ${m("r_2 = r_1 + t")}.`,
    m(`R'_{cond} = \\frac{\\ln(${g(r2)}/${g(r1)})}{2\\pi(${ins.k})} = ${fmt(Rcond)}, \\quad R'_{conv} = \\frac{1}{2\\pi(${g(r2)})(${h})} = ${fmt(Rconv)}\\ \\mathrm{m\\cdot K/W}`),
    m(`q' = \\frac{${Ts} - ${Tinf}}{${fmt(Rcond)} + ${fmt(Rconv)}} = ${fmt(qp)}${u("W/m")}`),
  ];
  const prompt = `A pipe with outer radius ${m(`${r1 * 1000}\\,\\mathrm{mm}`)} and surface temperature ${m(vu(Ts, "°C"))} is covered with ${m(`${t * 1000}\\,\\mathrm{mm}`)} of ${ins.name} (${m(`k = ${vu(ins.k, "W/m·K")}`)}). Ambient air is at ${m(vu(Tinf, "°C"))} with ${m(`h = ${vu(h, "W/m²·K")}`)}.`;
  const meta = { ht: "cyl", k: ins.k, r1, r2, Ts, Tinf, h, target: outer ? "T2" : "q" };
  if (!outer) return numeric(qp, "q′", "q'", "W/m", steps, meta, `${prompt} Find the heat loss per metre of pipe.`);
  const T2 = Tinf + qp * Rconv;
  return numeric(T2, "T₂", "T_2", "°C", [...steps, m(`T_2 = T_\\infty + q'R'_{conv} = ${Tinf} + ${fmt(qp)}\\times${fmt(Rconv)} = ${fmt(T2)}${u("°C")}`)],
    meta, `${prompt} Find the outer surface temperature of the insulation.`);
}

function sphereTank(r: Rng): Draft {
  const ins = r.pick(INSULATION);
  const r1 = r.pick([0.25, 0.4, 0.5, 1]);
  const t = r.pick([25, 50, 100]) / 1000;
  const r2 = r1 + t;
  const Ts1 = r.pick([-196, -150, -100, -40]);
  const Tinf = r.pick([20, 25, 30]);
  const h = r.pick([5, 10, 20]);
  const Rcond = (1 / r1 - 1 / r2) / (4 * PI * ins.k);
  const Rconv = 1 / (4 * PI * r2 * r2 * h);
  const q = (Tinf - Ts1) / (Rcond + Rconv);
  return numeric(q, "q", "q", "W", [
    `Sphere: ${m("R_{cond} = \\frac{1}{4\\pi k}\\left(\\frac{1}{r_1} - \\frac{1}{r_2}\\right)")}, ${m("R_{conv} = \\frac{1}{4\\pi r_2^2h}")}.`,
    m(`R_{cond} = \\frac{1}{4\\pi(${ins.k})}\\left(\\frac{1}{${g(r1)}} - \\frac{1}{${g(r2)}}\\right) = ${fmt(Rcond)}, \\quad R_{conv} = ${fmt(Rconv)}\\ \\mathrm{K/W}`),
    m(`q = \\frac{${Tinf} - (${Ts1})}{${fmt(Rcond)} + ${fmt(Rconv)}} = ${fmt(q)}${u("W")}`),
  ], { ht: "sphere", k: ins.k, r1, r2, Ts1, Tinf, h },
  `A spherical tank of radius ${m(`${g(r1)}\\,\\mathrm{m}`)} holds a cold liquid that keeps its wall at ${m(vu(Ts1, "°C"))}. It has ${m(`${t * 1000}\\,\\mathrm{mm}`)} of ${ins.name} (${m(`k = ${vu(ins.k, "W/m·K")}`)}); outside air is at ${m(vu(Tinf, "°C"))}, ${m(`h = ${vu(h, "W/m²·K")}`)}. Find the heat gain.`);
}

function criticalRadius(r: Rng): Draft {
  const k = r.pick([0.04, 0.05, 0.1, 0.15, 0.2]);
  const h = r.pick([2, 4, 5, 10, 20]);
  const sphere = r.chance(0.3);
  const rc = ((sphere ? 2 : 1) * k) / h;
  return numeric(rc * 1000, "r_cr", "r_{cr}", "mm", [
    `Total resistance ${sphere ? m("\\frac{1}{4\\pi k}\\left(\\frac{1}{r_i} - \\frac{1}{r}\\right) + \\frac{1}{4\\pi r^2h}") : m("\\frac{\\ln(r/r_i)}{2\\pi kL} + \\frac{1}{2\\pi rLh}")} is smallest where ${m("dR/dr = 0")}.`,
    m(`r_{cr} = ${sphere ? "\\frac{2k}{h}" : "\\frac{k}{h}"} = \\frac{${sphere ? `2(${k})` : k}}{${h}} = ${g(rc)}\\,\\mathrm{m} = ${fmt(rc * 1000)}${u("mm")}`),
    `Below ${m("r_{cr}")}, adding insulation increases the heat loss (more convection area than added conduction resistance).`,
  ], { ht: "rcrit", k, h, sphere },
  `Find the critical insulation radius for a ${sphere ? "sphere" : "cylinder (wire or pipe)"} insulated with a material of ${m(`k = ${vu(k, "W/m·K")}`)} in air with ${m(`h = ${vu(h, "W/m²·K")}`)}. Give it in mm.`);
}

// ═══ §3.5 generation ════════════════════════════════════════════════════════
function genWall(r: Rng): Draft {
  const half = r.pick([10, 20, 25, 50]) / 1000; // half-thickness (or full, one side insulated)
  const insulated = r.chance(0.35);
  const qdot = r.pick([1e5, 2e5, 5e5, 1e6, 2e6]);
  const k = r.pick([2, 5, 15, 25, 40]);
  const h = r.pick([50, 100, 250, 500, 1000]);
  const Tinf = r.pick([20, 25, 30]);
  const Ts = Tinf + (qdot * half) / h;
  const Tmax = Ts + (qdot * half * half) / (2 * k);
  require_(Tmax < 1200);
  const want = r.chance(0.5) ? "Tmax" : "Ts";
  const geom = insulated
    ? `A ${g(half * 1000)}-mm plane wall, insulated on one face and cooled on the other,`
    : `A ${g(2 * half * 1000)}-mm plane wall cooled on both faces`;
  const Lnote = insulated
    ? `With one face insulated, the wall is half of a symmetric wall: ${m(`L = ${g(half)}\\,\\mathrm{m}`)} is the full thickness here, and ${m("T_{max}")} sits on the insulated face.`
    : `Symmetric: ${m(`L = ${g(half)}\\,\\mathrm{m}`)} is the half-thickness, and ${m("T_{max}")} is at the midplane.`;
  const steps = [
    Lnote,
    `Energy balance on the cooled face: everything generated leaves by convection, ${m("\\dot qL = h(T_s - T_\\infty)")}, so ${m(`T_s = ${Tinf} + \\frac{${fmt(qdot)}\\times${g(half)}}{${h}} = ${fmt(Ts)}${u("°C")}`)}.`,
  ];
  if (want === "Tmax") steps.push(m(`T_{max} = T_s + \\frac{\\dot qL^2}{2k} = ${fmt(Ts, 4)} + \\frac{${fmt(qdot)}\\times${g(half)}^2}{2(${k})} = ${fmt(Tmax)}${u("°C")}`));
  return numeric(want === "Tmax" ? Tmax : Ts, want === "Tmax" ? "T_max" : "Tₛ", want === "Tmax" ? "T_{max}" : "T_s", "°C", steps,
    { ht: "gen-wall", L: half, qdot, k, h, Tinf, target: want },
    `${geom}, generates ${m(`\\dot q = ${vu(qdot, "W/m³")}`)} uniformly (${m(`k = ${vu(k, "W/m·K")}`)}). The coolant is at ${m(vu(Tinf, "°C"))} with ${m(`h = ${vu(h, "W/m²·K")}`)}. Find ${want === "Tmax" ? "the maximum temperature in the wall" : "the cooled surface temperature"}.`);
}

function genCyl(r: Rng): Draft {
  const romm = r.pick([2, 5, 10, 15, 25]);
  const ro = romm / 1000;
  const qdot = r.pick([1e6, 5e6, 1e7, 2e7, 5e7]);
  const k = r.pick([2, 15, 25, 50]);
  const h = r.pick([500, 1000, 2000, 5000]);
  const Tinf = r.pick([20, 25, 50]);
  const Ts = Tinf + (qdot * ro) / (2 * h);
  const T0 = Ts + (qdot * ro * ro) / (4 * k);
  require_(T0 < 1500 && T0 - Tinf > 5);
  return numeric(T0, "T₀", "T_0", "°C", [
    `Surface energy balance per length: ${m("\\dot q\\pi r_o^2 = h2\\pi r_o(T_s - T_\\infty)")}, so ${m("T_s = T_\\infty + \\frac{\\dot qr_o}{2h}")}.`,
    m(`T_s = ${Tinf} + \\frac{${fmt(qdot)}\\times${g(ro)}}{2(${h})} = ${fmt(Ts)}${u("°C")}`),
    `Radial conduction with generation: ${m("T(r) = T_s + \\frac{\\dot qr_o^2}{4k}\\left(1 - \\frac{r^2}{r_o^2}\\right)")}, largest at the centre.`,
    m(`T_0 = ${fmt(Ts, 4)} + \\frac{${fmt(qdot)}\\times${g(ro)}^2}{4(${k})} = ${fmt(T0)}${u("°C")}`),
  ], { ht: "gen-cyl", ro, qdot, k, h, Tinf },
  `A long ${2 * romm}-mm-diameter rod (${m(`k = ${vu(k, "W/m·K")}`)}) generates ${m(`\\dot q = ${vu(qdot, "W/m³")}`)} and is cooled by fluid at ${m(vu(Tinf, "°C"))} with ${m(`h = ${vu(h, "W/m²·K")}`)}. Find the centreline temperature.`);
}

// ═══ §3.6 fins ══════════════════════════════════════════════════════════════
interface Pin { name: string; k: number; D: number; Lf: number; h: number; Tb: number; Tinf: number; m: number; M: number }
function pin(r: Rng): Pin {
  const mat = r.pick([{ name: "copper", k: 400 }, { name: "aluminum", k: 237 }, { name: "aluminum alloy 2024", k: 177 }, { name: "carbon steel", k: 60 }, { name: "stainless steel", k: 15 }]);
  const D = r.pick([2, 3, 5, 10, 20]) / 1000;
  const Lf = r.pick([20, 50, 75, 100, 150]) / 1000;
  const h = r.pick([10, 25, 50, 100]);
  const Tb = r.pick([60, 80, 100, 150, 200]);
  const Tinf = r.pick([20, 25]);
  const P = PI * D, Ac = (PI * D * D) / 4;
  const mm = Math.sqrt((h * P) / (mat.k * Ac));
  const M = Math.sqrt(h * P * mat.k * Ac) * (Tb - Tinf);
  return { name: mat.name, k: mat.k, D, Lf, h, Tb, Tinf, m: mm, M };
}
const pinStem = (p: Pin, len = true) =>
  `A ${g(p.D * 1000)}-mm-diameter ${p.name} pin fin (${m(`k = ${vu(p.k, "W/m·K")}`)})${len ? `, ${g(p.Lf * 1000)} mm long,` : ""} has its base at ${m(vu(p.Tb, "°C"))} in fluid at ${m(vu(p.Tinf, "°C"))} with ${m(`h = ${vu(p.h, "W/m²·K")}`)}.`;
const mStep = (p: Pin) =>
  `Pin: ${m("P = \\pi D")}, ${m("A_c = \\pi D^2/4")}, so ${m(`m = \\sqrt{\\frac{hP}{kA_c}} = \\sqrt{\\frac{4h}{kD}} = \\sqrt{\\frac{4(${p.h})}{${p.k}(${g(p.D)})}} = ${fmt(p.m)}${u("m⁻¹")}`)}.`;
const pinMeta = (p: Pin, target: string) => ({ ht: "fin", k: p.k, D: p.D, Lf: p.Lf, h: p.h, Tb: p.Tb, Tinf: p.Tinf, target });

function finM(r: Rng): Draft {
  const p = pin(r);
  return numeric(p.m, "m", "m", "m⁻¹", [mStep(p).replace("so ", "")], pinMeta(p, "m"), `${pinStem(p, false)} Find the fin parameter ${m("m")}.`);
}

function finInfinite(r: Rng): Draft {
  const p = pin(r);
  const M = p.M;
  return numeric(M, "q_f", "q_f", "W", [
    `Infinitely long fin: ${m("q_f = \\sqrt{hPkA_c}\\,\\theta_b")}, ${m("\\theta_b = T_b - T_\\infty")}.`,
    m(`hPkA_c = (${p.h})(\\pi\\cdot${g(p.D)})(${p.k})(\\pi\\cdot${g(p.D)}^2/4) = ${fmt(p.h * PI * p.D * p.k * (PI * p.D * p.D) / 4)}`),
    m(`q_f = \\sqrt{${fmt(p.h * PI * p.D * p.k * (PI * p.D * p.D) / 4)}}\\times(${p.Tb} - ${p.Tinf}) = ${fmt(M)}${u("W")}`),
  ], pinMeta(p, "infinite"), `${pinStem(p, false)} Treating it as infinitely long, find the fin heat rate.`);
}

function finAdiabatic(r: Rng): Draft {
  const p = pin(r);
  const mL = p.m * p.Lf;
  const q = p.M * Math.tanh(mL);
  return numeric(q, "q_f", "q_f", "W", [
    mStep(p),
    `${m(`mL = ${fmt(p.m)}\\times${g(p.Lf)} = ${fmt(mL)}`)}${mL > 2.65 ? ` (> 2.65, so it is effectively infinite: ${m("\\tanh mL \\approx 1")})` : ""}.`,
    `Adiabatic tip: ${m("q_f = M\\tanh mL")}, ${m(`M = \\sqrt{hPkA_c}\\,\\theta_b = ${fmt(p.M)}${u("W")}`)}.`,
    m(`q_f = ${fmt(p.M)}\\times\\tanh(${fmt(mL)}) = ${fmt(q)}${u("W")}`),
  ], pinMeta(p, "adiabatic"), `${pinStem(p)} Assuming an adiabatic tip, find the fin heat rate.`);
}

function finEfficiency(r: Rng): Draft {
  const p = pin(r);
  const Lc = p.Lf + p.D / 4;
  const mLc = p.m * Lc;
  const eta = Math.tanh(mLc) / mLc;
  require_(eta < 0.97 && eta > 0.2);
  return numeric(eta * 100, "η_f", "\\eta_f", "%", [
    `Corrected length for a convecting tip: ${m(`L_c = L + D/4 = ${g(p.Lf)} + ${g(p.D / 4)} = ${fmt(Lc, 4)}\\,\\mathrm{m}`)}.`,
    mStep(p),
    m(`\\eta_f = \\frac{\\tanh mL_c}{mL_c} = \\frac{\\tanh(${fmt(mLc)})}{${fmt(mLc)}} = ${fmt(eta, 3)} = ${fmt(eta * 100)}\\%`),
  ], pinMeta(p, "efficiency"), `${pinStem(p)} Using the corrected length, find the fin efficiency (in %).`);
}

function finTip(r: Rng): Draft {
  const p = pin(r);
  const mL = p.m * p.Lf;
  require_(mL < 4);
  const TL = p.Tinf + (p.Tb - p.Tinf) / Math.cosh(mL);
  return numeric(TL, "T(L)", "T(L)", "°C", [
    mStep(p),
    `Adiabatic tip: ${m("\\frac{\\theta}{\\theta_b} = \\frac{\\cosh m(L-x)}{\\cosh mL}")}, so at ${m("x = L")}: ${m("\\theta(L) = \\frac{\\theta_b}{\\cosh mL}")}.`,
    m(`T(L) = ${p.Tinf} + \\frac{${p.Tb - p.Tinf}}{\\cosh(${fmt(mL)})} = ${fmt(TL)}${u("°C")}`),
  ], pinMeta(p, "tip"), `${pinStem(p)} Assuming an adiabatic tip, find the tip temperature.`);
}

// ═══ Ch 4 two-dimensional conduction ════════════════════════════════════════
function shapeFactor(r: Rng): Draft {
  const kind = r.pick(["buried-cyl", "buried-sphere", "cyl-square"] as const);
  const k = r.pick([0.5, 0.8, 1.0, 1.2, 1.5]);
  const T1 = r.pick([60, 80, 100, 120, 150]);
  const T2 = r.pick([0, 5, 10, 15]);
  let S: number, sTex: string, setup: string, meta: Record<string, unknown>;
  if (kind === "buried-cyl") {
    const D = r.pick([0.1, 0.2, 0.3, 0.5]);
    const z = r.pick([0.5, 1, 1.5, 2]);
    const L = r.pick([10, 20, 50, 100]);
    S = (2 * PI * L) / Math.acosh((2 * z) / D);
    sTex = `S = \\frac{2\\pi L}{\\cosh^{-1}(2z/D)} = \\frac{2\\pi(${L})}{\\cosh^{-1}(${g((2 * z) / D)})} = ${fmt(S)}\\,\\mathrm{m}`;
    setup = `A ${L}-m length of pipe, ${m(`D = ${g(D)}\\,\\mathrm{m}`)}, is buried with its centreline ${m(`z = ${g(z)}\\,\\mathrm{m}`)} below the ground surface`;
    meta = { ht: "sf", kind, D, z, L };
  } else if (kind === "buried-sphere") {
    const D = r.pick([0.5, 1, 1.5, 2]);
    const z = r.pick([1, 2, 3, 5]);
    require_(z > D);
    S = (2 * PI * D) / (1 - D / (4 * z));
    sTex = `S = \\frac{2\\pi D}{1 - D/4z} = \\frac{2\\pi(${g(D)})}{1 - ${g(D)}/${g(4 * z)}} = ${fmt(S)}\\,\\mathrm{m}`;
    setup = `A spherical tank, ${m(`D = ${g(D)}\\,\\mathrm{m}`)}, is buried with its centre ${m(`z = ${g(z)}\\,\\mathrm{m}`)} below the ground surface`;
    meta = { ht: "sf", kind, D, z };
  } else {
    const D = r.pick([0.05, 0.1, 0.15]);
    const w = r.pick([0.2, 0.3, 0.5]);
    const L = r.pick([1, 2, 5]);
    S = (2 * PI * L) / Math.log((1.08 * w) / D);
    sTex = `S = \\frac{2\\pi L}{\\ln(1.08w/D)} = \\frac{2\\pi(${L})}{\\ln(${g((1.08 * w) / D)})} = ${fmt(S)}\\,\\mathrm{m}`;
    setup = `A ${m(`D = ${g(D)}\\,\\mathrm{m}`)} pipe, ${L} m long, runs along the centre of a square ${m(`w = ${g(w)}\\,\\mathrm{m}`)} casing whose outer faces are held at a uniform temperature`;
    meta = { ht: "sf", kind, D, w, L };
  }
  const q = S * k * (T1 - T2);
  return numeric(q, "q", "q", "W", [
    `Table 4.1 — ${kind === "buried-cyl" ? "horizontal isothermal cylinder buried in a semi-infinite medium" : kind === "buried-sphere" ? "isothermal sphere buried in a semi-infinite medium" : "circular cylinder centred in a square solid of equal length"}: ${m(sTex)}.`,
    m(`q = Sk(T_1 - T_2) = ${fmt(S)}\\times${k}\\times(${T1} - ${T2}) = ${fmt(q)}${u("W")}`),
  ], { ...meta, k, T1, T2 },
  `${setup}. Its surface is at ${m(vu(T1, "°C"))}, the ${kind === "cyl-square" ? "outer faces" : "ground surface"} at ${m(vu(T2, "°C"))}; ${m(`k = ${vu(k, "W/m·K")}`)}. Using the conduction shape factor, find the heat rate.`);
}

function fdNode(r: Rng): Draft {
  const kind = r.pick(["interior", "interior-gen", "surface-conv", "corner-conv"] as const);
  const T = () => r.pick([40, 50, 60, 70, 80, 90, 100, 120, 150]);
  const dx = r.pick([0.01, 0.02, 0.025, 0.05]);
  const k = r.pick([1, 5, 15, 25, 50]);
  if (kind === "interior" || kind === "interior-gen") {
    const [a, b, c, d] = [T(), T(), T(), T()];
    const qdot = kind === "interior-gen" ? r.pick([1e5, 5e5, 1e6, 5e6]) : 0;
    const gen = (qdot * dx * dx) / k;
    require_(gen < 150);
    const Tm = (a + b + c + d + gen) / 4;
    return numeric(Tm, "T_m,n", "T_{m,n}", "°C", [
      `Interior node, ${m("\\Delta x = \\Delta y")}: the energy balance gives ${m("T_{m+1,n} + T_{m-1,n} + T_{m,n+1} + T_{m,n-1}" + (qdot ? " + \\frac{\\dot q\\Delta x^2}{k}" : "") + " - 4T_{m,n} = 0")}.`,
      ...(qdot ? [m(`\\frac{\\dot q\\Delta x^2}{k} = \\frac{${fmt(qdot)}\\times${g(dx)}^2}{${k}} = ${fmt(gen)}`)] : []),
      m(`T_{m,n} = \\frac{${a} + ${b} + ${c} + ${d}${qdot ? ` + ${fmt(gen)}` : ""}}{4} = ${fmt(Tm)}${u("°C")}`),
    ], { ht: "fd", kind, nb: [a, b, c, d], qdot, dx, k },
    `In a 2-D steady finite-difference grid (${m(`\\Delta x = \\Delta y = ${g(dx)}\\,\\mathrm{m}`)}, ${m(`k = ${vu(k, "W/m·K")}`)}${qdot ? `, ${m(`\\dot q = ${vu(qdot, "W/m³")}`)}` : ", no generation"}), an interior node's neighbours are at ${m(`${a}, ${b}, ${c}`)} and ${m(`${d}\\,^\\circ\\mathrm{C}`)}. Find the node temperature.`);
  }
  const h = r.pick([10, 25, 50, 100, 250]);
  const Tinf = r.pick([20, 25, 30]);
  const Bi = (h * dx) / k;
  if (kind === "surface-conv") {
    const [left, up, down] = [T(), T(), T()];
    const Tm = (2 * left + up + down + 2 * Bi * Tinf) / (2 * (Bi + 2));
    return numeric(Tm, "T_m,n", "T_{m,n}", "°C", [
      `Node on a plane surface with convection (Table 4.2, case 3): half-cells above and below, a full cell inward, and convection over ${m("\\Delta y")}.`,
      m("2T_{m-1,n} + T_{m,n+1} + T_{m,n-1} + \\frac{2h\\Delta x}{k}T_\\infty - 2\\left(\\frac{h\\Delta x}{k} + 2\\right)T_{m,n} = 0"),
      m(`\\frac{h\\Delta x}{k} = \\frac{${h}\\times${g(dx)}}{${k}} = ${fmt(Bi, 4)}`),
      m(`T_{m,n} = \\frac{2(${left}) + ${up} + ${down} + 2(${fmt(Bi, 4)})(${Tinf})}{2(${fmt(Bi, 4)} + 2)} = ${fmt(Tm)}${u("°C")}`),
    ], { ht: "fd", kind, inward: left, up, down, h, Tinf, dx, k },
    `A node sits on a plane surface exposed to fluid at ${m(vu(Tinf, "°C"))}, ${m(`h = ${vu(h, "W/m²·K")}`)} (${m(`\\Delta x = \\Delta y = ${g(dx)}\\,\\mathrm{m}`)}, ${m(`k = ${vu(k, "W/m·K")}`)}). The interior neighbour is at ${m(vu(left, "°C"))}; the neighbours along the surface are at ${m(`${up}`)} and ${m(vu(down, "°C"))}. Find the node temperature.`);
  }
  const [left, down] = [T(), T()];
  const Tm = (left + down + 2 * Bi * Tinf) / (2 * (Bi + 1));
  return numeric(Tm, "T_m,n", "T_{m,n}", "°C", [
    `External corner with convection (Table 4.2, case 4): a quarter-cell, two half-faces conducting inward, convection on both outer faces.`,
    m("T_{m-1,n} + T_{m,n-1} + \\frac{2h\\Delta x}{k}T_\\infty - 2\\left(\\frac{h\\Delta x}{k} + 1\\right)T_{m,n} = 0"),
    m(`\\frac{h\\Delta x}{k} = ${fmt(Bi, 4)}`),
    m(`T_{m,n} = \\frac{${left} + ${down} + 2(${fmt(Bi, 4)})(${Tinf})}{2(${fmt(Bi, 4)} + 1)} = ${fmt(Tm)}${u("°C")}`),
  ], { ht: "fd", kind, a: left, b: down, h, Tinf, dx, k },
  `An external-corner node is exposed on both outer faces to fluid at ${m(vu(Tinf, "°C"))}, ${m(`h = ${vu(h, "W/m²·K")}`)} (${m(`\\Delta x = \\Delta y = ${g(dx)}\\,\\mathrm{m}`)}, ${m(`k = ${vu(k, "W/m·K")}`)}). Its two neighbours are at ${m(`${left}`)} and ${m(vu(down, "°C"))}. Find the corner temperature.`);
}

export const HEAT_TEMPLATES: Record<string, (r: Rng) => Draft> = {
  "ht-cond": rateCond,
  "ht-conv": rateConv,
  "ht-rad": rateRad,
  "ht-eb-surface": ebSurface,
  "ht-eb-wire": ebWire,
  "ht-he-gen": heGeneration,
  "ht-he-flux": heFlux,
  "ht-he-dTdt": heDTdt,
  "ht-wall": wall,
  "ht-contact": wallContact,
  "ht-cyl": cylInsulated,
  "ht-sphere": sphereTank,
  "ht-rcrit": criticalRadius,
  "ht-gen-wall": genWall,
  "ht-gen-cyl": genCyl,
  "ht-fin-m": finM,
  "ht-fin-infinite": finInfinite,
  "ht-fin-adiabatic": finAdiabatic,
  "ht-fin-efficiency": finEfficiency,
  "ht-fin-tip": finTip,
  "ht-shape": shapeFactor,
  "ht-fd": fdNode,
};
