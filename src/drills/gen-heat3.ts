// Incropera 8e Ch 6 (boundary layers, analogies), §7.6 (tube banks), Ch 10 (boiling,
// condensation), Ch 12 (radiation properties), Ch 14 + §6.7 (mass transfer).
// Level 1, numeric answers checked to 1%. Every property a student needs is in the
// prompt ("at the film temperature …"), so no table lookup. Each problem carries its
// SI inputs in `meta` (case name under `ht3`) for tests/verify/heat3.py, which
// recomputes the answer from first principles.
import { Rng } from "./rng";
import type { Draft } from "./types";
import { m } from "./tex";
import { require_ } from "./reject";

const SIGMA = 5.67e-8;
const PI = Math.PI;
const G = 9.8; // Incropera's g
const RU = 8.314; // kJ/kmol·K  (p in kPa → C in kmol/m³)
const WIEN = 2898; // µm·K
const C2 = 14388; // µm·K, second radiation constant (Table 12.2 is built on it)

// ── formatting (copied from gen-heat.ts so the two files never conflict) ─────
function fmt(x: number, sig = 3): string {
  if (x === 0) return "0";
  const ax = Math.abs(x);
  if (ax >= 1e6 || ax < 1e-3) {
    const e = Math.floor(Math.log10(ax));
    const mant = Number((x / 10 ** e).toPrecision(sig));
    return `${mant} \\times 10^{${e}}`;
  }
  const v = Number(x.toPrecision(sig));
  const [i, f] = String(Math.abs(v)).split(".");
  const ii = i.length > 4 ? i.replace(/\B(?=(\d{3})+(?!\d))/g, "\\,") : i;
  return `${v < 0 ? "-" : ""}${ii}${f ? `.${f}` : ""}`;
}
const g = (x: number) => fmt(x, 4);
const K = (c: number) => c + 273.15;

const U: Record<string, string> = {
  "": "",
  W: "\\mathrm{W}",
  "W/m": "\\mathrm{W/m}",
  "W/m²": "\\mathrm{W/m^2}",
  "W/m²·K": "\\mathrm{W/m^2\\cdot K}",
  "W/m·K": "\\mathrm{W/m\\cdot K}",
  "°C": "^\\circ\\mathrm{C}",
  K: "\\mathrm{K}",
  m: "\\mathrm{m}",
  mm: "\\mathrm{mm}",
  "m/s": "\\mathrm{m/s}",
  "m²/s": "\\mathrm{m^2/s}",
  "kg/m³": "\\mathrm{kg/m^3}",
  "J/kg·K": "\\mathrm{J/kg\\cdot K}",
  "J/kg": "\\mathrm{J/kg}",
  "N·s/m²": "\\mathrm{N\\cdot s/m^2}",
  "N/m": "\\mathrm{N/m}",
  N: "\\mathrm{N}",
  "µm": "\\mu\\mathrm{m}",
  "kg/s": "\\mathrm{kg/s}",
  "kg/h": "\\mathrm{kg/h}",
  "kg/s·m": "\\mathrm{kg/s\\cdot m}",
  "kg/s·m²": "\\mathrm{kg/s\\cdot m^2}",
  "kmol/s·m²": "\\mathrm{kmol/s\\cdot m^2}",
  "kmol/s": "\\mathrm{kmol/s}",
  "kmol/m³": "\\mathrm{kmol/m^3}",
  "kmol/m³·bar": "\\mathrm{kmol/m^3\\cdot bar}",
  "kg/kmol": "\\mathrm{kg/kmol}",
  "s⁻¹": "\\mathrm{s^{-1}}",
  kPa: "\\mathrm{kPa}",
  bar: "\\mathrm{bar}",
};
const u = (unit: string) => (unit === "" ? "" : `\\,${U[unit] ?? `\\mathrm{${unit}}`}`);
const vu = (x: number, unit: string) => `${g(x)}${u(unit)}`;
const eq = (sym: string, x: number, unit: string) => m(`${sym} = ${vu(x, unit)}`);

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

/** root of f on [lo, hi] by bisection (f(lo), f(hi) of opposite sign) */
function bisect(f: (x: number) => number, lo: number, hi: number): number {
  let flo = f(lo);
  require_(flo * f(hi) < 0);
  for (let i = 0; i < 200; i++) {
    const mid = (lo + hi) / 2;
    const fm = f(mid);
    if (fm * flo > 0) {
      lo = mid;
      flo = fm;
    } else hi = mid;
  }
  return (lo + hi) / 2;
}

/** blackbody band fraction F(0→λT), λT in µm·K (Eq 12.34 series, |error| < 1e-12) */
export function bandFraction(lT: number): number {
  const x = C2 / lT;
  let s = 0;
  for (let n = 1; n < 20000; n++) {
    const t = (Math.exp(-n * x) / n) * (x ** 3 + (3 * x * x) / n + (6 * x) / (n * n) + 6 / n ** 3);
    s += t;
    if (t < 1e-16 * s) break;
  }
  return (15 / PI ** 4) * s;
}

// ── fluids at a film temperature (Incropera Tables A.4–A.6, rounded) ─────────
interface Fluid { name: string; T: number; nu: number; k: number; Pr: number; rho: number; cp: number; alpha: number }
const AIR300: Fluid = { name: "air", T: 300, nu: 15.89e-6, k: 0.0263, Pr: 0.707, rho: 1.1614, cp: 1007, alpha: 22.5e-6 };
const AIR350: Fluid = { name: "air", T: 350, nu: 20.92e-6, k: 0.030, Pr: 0.700, rho: 0.995, cp: 1009, alpha: 29.9e-6 };
const AIR400: Fluid = { name: "air", T: 400, nu: 26.41e-6, k: 0.0338, Pr: 0.690, rho: 0.8711, cp: 1014, alpha: 38.3e-6 };
const WATER300: Fluid = { name: "water", T: 300, nu: 0.858e-6, k: 0.613, Pr: 5.83, rho: 997, cp: 4179, alpha: 0.147e-6 };
const WATER350: Fluid = { name: "water", T: 350, nu: 0.375e-6, k: 0.668, Pr: 2.29, rho: 974, cp: 4195, alpha: 0.164e-6 };
const OIL350: Fluid = { name: "engine oil", T: 350, nu: 41.7e-6, k: 0.138, Pr: 546, rho: 854, cp: 2118, alpha: 0.0765e-6 };
const speeds = (f: Fluid) => (f.name === "air" ? [2, 3, 5, 8, 10, 15, 20, 25] : f.name === "water" ? [0.1, 0.2, 0.3, 0.5, 1, 2] : [0.5, 1, 2, 3, 5]);
const fluidProps = (f: Fluid, keys: (keyof Fluid)[]) => {
  const tex: Record<string, string> = {
    nu: `\\nu = ${vu(f.nu, "m²/s")}`, k: `k = ${vu(f.k, "W/m·K")}`, Pr: `Pr = ${g(f.Pr)}`,
    rho: `\\rho = ${vu(f.rho, "kg/m³")}`, cp: `c_p = ${vu(f.cp, "J/kg·K")}`, alpha: `\\alpha = ${vu(f.alpha, "m²/s")}`,
  };
  return keys.map((k_) => m(tex[k_ as string])).join(", ");
};

// ═══ Ch 6 boundary layers ════════════════════════════════════════════════════
function blTransition(r: Rng): Draft {
  const f = r.pick([AIR300, AIR350, AIR400, WATER300, WATER350, OIL350]);
  const V = r.pick(speeds(f));
  const target = r.pick(["xc", "xc", "ReL"] as const);
  const xc = (5e5 * f.nu) / V;
  const meta = { ht3: "bl-transition", nu: f.nu, V, Rec: 5e5, target };
  if (target === "xc") {
    require_(xc > 0.02 && xc < 30);
    return numeric(xc, "x_c", "x_c", "m", [
      `Transition starts where the local Reynolds number reaches the critical value: ${m("Re_{x_c} = \\frac{u_\\infty x_c}{\\nu} = 5\\times10^5")}.`,
      m(`x_c = \\frac{5\\times10^5\\,\\nu}{u_\\infty} = \\frac{5\\times10^5 \\times ${g(f.nu)}}{${g(V)}} = ${fmt(xc)}${u("m")}`),
    ], meta,
    `${f.name[0].toUpperCase() + f.name.slice(1)} (${fluidProps(f, ["nu"])} at the film temperature) flows at ${eq("u_\\infty", V, "m/s")} parallel to a flat plate. Taking ${m("Re_{x,c} = 5\\times10^5")}, how far from the leading edge does transition to turbulence begin?`);
  }
  const L = r.pick([0.25, 0.5, 1, 2, 3]);
  const ReL = (V * L) / f.nu;
  return numeric(ReL, "Re_L", "Re_L", "", [
    m(`Re_L = \\frac{u_\\infty L}{\\nu} = \\frac{${g(V)} \\times ${g(L)}}{${g(f.nu)}} = ${fmt(ReL)}`),
    `${ReL < 5e5 ? `Below ${m("5\\times10^5")}: laminar over the whole plate.` : `Above ${m("5\\times10^5")}: the boundary layer turns turbulent at ${m(`x_c = ${fmt(xc)}\\,\\mathrm{m}`)}, so the flow is mixed.`}`,
  ], { ...meta, L },
  `${f.name[0].toUpperCase() + f.name.slice(1)} (${fluidProps(f, ["nu"])}) flows at ${eq("u_\\infty", V, "m/s")} over a ${g(L)}-m-long flat plate. Find the Reynolds number at the trailing edge, ${m("Re_L")}.`);
}

function blAverage(r: Rng): Draft {
  const kind = r.pick(["laminar", "turbulent", "trailing", "nusselt"] as const);
  const L = r.pick([0.1, 0.2, 0.25, 0.4, 0.5, 0.8, 1]);
  if (kind === "laminar" || kind === "turbulent") {
    const n = kind === "laminar" ? 0.5 : 0.2;
    const C = kind === "laminar" ? r.pick([3, 4.5, 6, 8, 10, 12]) : r.pick([15, 20, 25, 30, 40]);
    const hbar = (C * L ** -n) / (1 - n);
    const cu = kind === "laminar" ? "\\mathrm{W/m^{1.5}\\cdot K}" : "\\mathrm{W/m^{1.8}\\cdot K}";
    const ex = kind === "laminar" ? "-1/2" : "-1/5";
    return numeric(hbar, "h̄", "\\bar h_L", "W/m²·K", [
      `Average over the plate: ${m("\\bar h_L = \\frac{1}{L}\\int_0^L h_x\\,dx")}.`,
      m(`\\bar h_L = \\frac{C}{L}\\int_0^L x^{${ex}}dx = \\frac{C L^{${ex}}}{1 - ${n === 0.5 ? "1/2" : "1/5"}} = ${n === 0.5 ? "2" : "1.25"}\\,h_x(L)`),
      m(`\\bar h_L = \\frac{${C}\\,(${g(L)})^{${ex}}}{${g(1 - n)}} = ${fmt(hbar)}${u("W/m²·K")}`),
    ], { ht3: "bl-average", kind, C, n, L },
    `For ${kind} flow over a flat plate the local convection coefficient is ${m(`h_x = C x^{${ex}}`)} with ${m(`C = ${C}\\,${cu}`)} (${m("x")} in m). Find the average coefficient ${m("\\bar h_L")} over the first ${m(`L = ${g(L)}\\,\\mathrm{m}`)}.`);
  }
  if (kind === "trailing") {
    const hL = r.pick([5, 8, 12, 20, 35, 50, 120, 300]);
    return numeric(2 * hL, "h̄", "\\bar h_L", "W/m²·K", [
      `${m("h_x = Cx^{-1/2}")} ⇒ ${m("\\bar h_L = \\frac{1}{L}\\int_0^L Cx^{-1/2}dx = 2CL^{-1/2} = 2h_L")}.`,
      m(`\\bar h_L = 2 \\times ${hL} = ${fmt(2 * hL)}${u("W/m²·K")}`),
    ], { ht3: "bl-average", kind, hL, L },
    `In laminar flow over a ${g(L)}-m flat plate, ${m("h_x \\propto x^{-1/2}")}. The local coefficient at the trailing edge is ${eq("h_x(L)", hL, "W/m²·K")}. Find the average coefficient over the whole plate.`);
  }
  const f = r.pick([AIR300, AIR350, AIR400, WATER300, WATER350, OIL350]);
  const V = r.pick(speeds(f));
  const ReL = (V * L) / f.nu;
  require_(ReL < 5e5 && ReL > 500);
  const hL = (f.k / L) * 0.332 * Math.sqrt(ReL) * f.Pr ** (1 / 3);
  const hbar = 2 * hL;
  return numeric(hbar, "h̄", "\\bar h_L", "W/m²·K", [
    m(`Re_L = \\frac{u_\\infty L}{\\nu} = ${fmt(ReL)} < 5\\times10^5`) + ` — laminar throughout.`,
    `${m("h_x = \\frac{k}{x}\\,0.332\\,Re_x^{1/2}Pr^{1/3} \\propto x^{-1/2}")}, so averaging over ${m("0..L")} doubles the trailing-edge value: ${m("\\bar{Nu}_L = 0.664\\,Re_L^{1/2}Pr^{1/3}")}.`,
    m(`\\bar h_L = \\frac{k}{L}\\,0.664\\,Re_L^{1/2}Pr^{1/3} = \\frac{${g(f.k)}}{${g(L)}}(0.664)(${fmt(ReL)})^{1/2}(${g(f.Pr)})^{1/3} = ${fmt(hbar)}${u("W/m²·K")}`),
  ], { ht3: "bl-average", kind, nu: f.nu, k: f.k, Pr: f.Pr, V, L },
  `${f.name[0].toUpperCase() + f.name.slice(1)} flows at ${eq("u_\\infty", V, "m/s")} over a ${g(L)}-m flat plate (${fluidProps(f, ["nu", "k", "Pr"])} at the film temperature). The local Nusselt number is ${m("Nu_x = 0.332\\,Re_x^{1/2}Pr^{1/3}")}. Find the average coefficient ${m("\\bar h_L")}.`);
}

function blThickness(r: Rng): Draft {
  const f = r.pick([AIR300, AIR350, AIR400, WATER300, WATER350, OIL350]);
  const V = r.pick(speeds(f));
  const xcm = r.pick([2, 5, 10, 20, 30, 50]);
  const x = xcm / 100;
  const Re = (V * x) / f.nu;
  require_(Re < 5e5 && Re > 1000);
  const d = (5 * x) / Math.sqrt(Re);
  const target = r.pick(["delta", "deltat", "deltat"] as const);
  const dt = d / f.Pr ** (1 / 3);
  const meta = { ht3: "bl-thickness", nu: f.nu, Pr: f.Pr, V, x, target };
  const s1 = m(`Re_x = \\frac{u_\\infty x}{\\nu} = \\frac{${g(V)} \\times ${g(x)}}{${g(f.nu)}} = ${fmt(Re)}`) + " (laminar).";
  const s2 = m(`\\delta = \\frac{5x}{Re_x^{1/2}} = \\frac{5(${g(x)})}{(${fmt(Re)})^{1/2}} = ${fmt(d, 4)}\\,\\mathrm{m} = ${fmt(d * 1000)}\\,\\mathrm{mm}`);
  const stem = `${f.name[0].toUpperCase() + f.name.slice(1)} (${fluidProps(f, ["nu", "Pr"])}) flows at ${eq("u_\\infty", V, "m/s")} over a flat plate.`;
  if (target === "delta")
    return numeric(d * 1000, "δ", "\\delta", "mm", [s1, s2], meta,
      `${stem} Find the velocity boundary-layer thickness ${m("\\delta")} at ${m(`x = ${xcm}\\,\\mathrm{cm}`)}, in mm.`);
  return numeric(dt * 1000, "δ_t", "\\delta_t", "mm", [
    s1, s2,
    `${m("\\delta/\\delta_t \\approx Pr^{1/3}")}: ${m(`\\delta_t = \\frac{${fmt(d * 1000)}}{(${g(f.Pr)})^{1/3}} = ${fmt(dt * 1000)}\\,\\mathrm{mm}`)}${f.Pr > 1 ? " — thinner than δ, since Pr > 1." : " — slightly thicker than δ (Pr < 1)."}`,
  ], meta, `${stem} Find the thermal boundary-layer thickness ${m("\\delta_t")} at ${m(`x = ${xcm}\\,\\mathrm{cm}`)}, in mm.`);
}

function blColburn(r: Rng): Draft {
  const f = r.pick([AIR300, AIR350, AIR400, WATER300, WATER350]);
  const V = r.pick(speeds(f));
  const L = r.pick([0.2, 0.3, 0.5, 0.8, 1]);
  const W = r.pick([0.5, 1, 1.5, 2]);
  const ReL = (V * L) / f.nu;
  require_(ReL < 5e5 && ReL > 2000);
  const F = Number(((1.328 / Math.sqrt(ReL)) * 0.5 * f.rho * V * V * L * W).toPrecision(3));
  require_(F > 1e-3);
  const tau = F / (L * W);
  const Cf = tau / (0.5 * f.rho * V * V);
  const hbar = (Cf / 2) * f.rho * f.cp * V * f.Pr ** (-2 / 3);
  return numeric(hbar, "h̄", "\\bar h", "W/m²·K", [
    m(`\\bar\\tau_s = \\frac{F_D}{LW} = \\frac{${g(F)}}{${g(L)}\\times${g(W)}} = ${fmt(tau)}\\,\\mathrm{N/m^2}, \\quad \\bar C_f = \\frac{\\bar\\tau_s}{\\rho u_\\infty^2/2} = ${fmt(Cf)}`),
    `Chilton–Colburn: ${m("\\frac{C_f}{2} = St\\,Pr^{2/3}")} with ${m("St = \\frac{h}{\\rho c_p u_\\infty}")}, valid for ${m("0.6 < Pr < 60")}.`,
    m(`\\bar h = \\frac{\\bar C_f}{2}\\,\\rho c_p u_\\infty Pr^{-2/3} = ${fmt(Cf / 2)}(${g(f.rho)})(${g(f.cp)})(${g(V)})(${g(f.Pr)})^{-2/3} = ${fmt(hbar)}${u("W/m²·K")}`),
  ], { ht3: "bl-colburn", F, L, W, V, rho: f.rho, cp: f.cp, Pr: f.Pr },
  `${f.name[0].toUpperCase() + f.name.slice(1)} at ${eq("u_\\infty", V, "m/s")} flows over one face of a ${g(L)}-m-long, ${g(W)}-m-wide plate; the measured drag force on that face is ${eq("F_D", F, "N")}. With ${fluidProps(f, ["rho", "cp", "Pr"])}, use the Chilton–Colburn analogy to find the average heat-transfer coefficient.`);
}

function blGroups(r: Rng): Draft {
  const v = r.pick(["Nu", "h", "Pr"] as const);
  const f = r.pick([AIR300, AIR350, AIR400, WATER300, WATER350, OIL350]);
  if (v === "Nu") {
    const h = r.pick(f.name === "air" ? [10, 25, 40, 60, 100] : [200, 500, 1000, 2500]);
    const L = r.pick([0.05, 0.1, 0.25, 0.5, 1]);
    const ks = r.pick([15, 60, 237, 400]);
    const Nu = (h * L) / f.k;
    return numeric(Nu, "Nu", "\\bar{Nu}_L", "", [
      `The Nusselt number uses the ${m("k")} of the fluid, not of the solid: ${m("\\bar{Nu}_L = \\frac{\\bar h L}{k_f}")}. (Using the solid's ${m("k")} would give a Biot number.)`,
      m(`\\bar{Nu}_L = \\frac{${h} \\times ${g(L)}}{${g(f.k)}} = ${fmt(Nu)}`),
    ], { ht3: "bl-groups", v, h, L, k: f.k },
    `A ${g(L)}-m plate (${m(`k_s = ${vu(ks, "W/m·K")}`)}) is cooled by ${f.name} (${m(`k_f = ${vu(f.k, "W/m·K")}`)}) with ${m(`\\bar h = ${vu(h, "W/m²·K")}`)}. Find the average Nusselt number ${m("\\bar{Nu}_L")}.`);
  }
  if (v === "h") {
    const Nu = r.pick([8, 15, 30, 55, 120, 250]);
    const Dmm = r.pick([5, 10, 20, 25, 50]);
    const D = Dmm / 1000;
    const h = (Nu * f.k) / D;
    return numeric(h, "h̄", "\\bar h", "W/m²·K", [
      m("\\bar h = \\frac{\\bar{Nu}_D\\,k}{D}"),
      m(`\\bar h = \\frac{${Nu} \\times ${g(f.k)}}{${g(D)}} = ${fmt(h)}${u("W/m²·K")}`),
    ], { ht3: "bl-groups", v, Nu, D, k: f.k },
    `For ${f.name} (${m(`k = ${vu(f.k, "W/m·K")}`)}) in cross flow over a ${Dmm}-mm-diameter cylinder, a correlation gives ${m(`\\bar{Nu}_D = ${Nu}`)}. Find ${m("\\bar h")}.`);
  }
  const mu = Number((f.nu * f.rho).toPrecision(4)); // as printed in the prompt
  const Pr = (mu * f.cp) / f.k;
  return numeric(Pr, "Pr", "Pr", "", [
    m("Pr = \\frac{\\nu}{\\alpha} = \\frac{\\mu c_p}{k}"),
    m(`Pr = \\frac{${fmt(mu, 4)} \\times ${g(f.cp)}}{${g(f.k)}} = ${fmt(Pr)}`),
  ], { ht3: "bl-groups", v, mu, cp: f.cp, k: f.k },
  `For ${f.name} at ${f.T} K: ${m(`\\mu = ${vu(mu, "N·s/m²")}`)}, ${m(`c_p = ${vu(f.cp, "J/kg·K")}`)}, ${m(`k = ${vu(f.k, "W/m·K")}`)}. Find the Prandtl number.`);
}

// ═══ §7.6 tube banks ════════════════════════════════════════════════════════
interface Bank { aligned: boolean; D: number; ST: number; SL: number; SD: number; Vmax: number; diag: boolean }
function bank(r: Rng, V: number): Bank {
  const aligned = r.chance(0.5);
  const Dmm = r.pick([10, 12.7, 16, 20, 25]);
  const D = Dmm / 1000;
  const ST = r.pick([1.25, 1.5, 2, 2.5, 3]) * D;
  const SL = r.pick([1, 1.25, 1.5, 2, 2.5]) * D;
  require_(aligned ? SL > D * 1.1 : true);
  const SD = Math.sqrt(SL * SL + (ST / 2) ** 2);
  require_(SD > D * 1.05);
  const diag = !aligned && 2 * (SD - D) < ST - D;
  const Vmax = diag ? (ST * V) / (2 * (SD - D)) : (ST * V) / (ST - D);
  return { aligned, D, ST, SL, SD, Vmax, diag };
}
const mmTex = (x: number) => `${g(x * 1000)}\\,\\mathrm{mm}`;
const bankStem = (b: Bank) =>
  `a${b.aligned ? "n aligned" : " staggered"} bank of ${m(mmTex(b.D))}-diameter tubes with ${m(`S_T = ${mmTex(b.ST)}`)} and ${m(`S_L = ${mmTex(b.SL)}`)}`;
function vmaxSteps(b: Bank, V: number): string[] {
  if (b.aligned)
    return [`Aligned: the smallest flow area is the transverse gap ${m("S_T - D")}, so ${m(`V_{max} = \\frac{S_T}{S_T - D}V = \\frac{${g(b.ST * 1000)}}{${g((b.ST - b.D) * 1000)}}(${g(V)}) = ${fmt(b.Vmax)}\\,\\mathrm{m/s}`)}.`];
  return [
    `Staggered: ${m(`S_D = \\sqrt{S_L^2 + (S_T/2)^2} = ${fmt(b.SD * 1000, 4)}\\,\\mathrm{mm}`)}. Compare the two gaps: ${m(`2(S_D - D) = ${fmt(2 * (b.SD - b.D) * 1000, 4)}`)} vs ${m(`S_T - D = ${fmt((b.ST - b.D) * 1000, 4)}`)} (mm).`,
    b.diag
      ? `The diagonal plane is narrower (${m("S_D < (S_T + D)/2")}), so ${m(`V_{max} = \\frac{S_T}{2(S_D - D)}V = ${fmt(b.Vmax)}\\,\\mathrm{m/s}`)}.`
      : `The transverse plane is narrower, so ${m(`V_{max} = \\frac{S_T}{S_T - D}V = ${fmt(b.Vmax)}\\,\\mathrm{m/s}`)}.`,
  ];
}

function tbVmax(r: Rng): Draft {
  const f = r.pick([AIR300, AIR350, WATER300]);
  const V = r.pick(f.name === "air" ? [2, 4, 5, 6, 8, 10, 12] : [0.2, 0.3, 0.5, 1]);
  const b = bank(r, V);
  const target = r.pick(["Vmax", "Vmax", "Re"] as const);
  const meta = { ht3: "tb-vmax", aligned: b.aligned, D: b.D, ST: b.ST, SL: b.SL, V, nu: f.nu, target };
  if (target === "Vmax")
    return numeric(b.Vmax, "V_max", "V_{max}", "m/s", vmaxSteps(b, V), meta,
      `${f.name[0].toUpperCase() + f.name.slice(1)} approaches ${bankStem(b)} at ${eq("V", V, "m/s")}. Find the maximum velocity ${m("V_{max}")} in the bank.`);
  const Re = (b.Vmax * b.D) / f.nu;
  return numeric(Re, "Re_D,max", "Re_{D,max}", "", [
    ...vmaxSteps(b, V),
    m(`Re_{D,max} = \\frac{V_{max}D}{\\nu} = \\frac{${fmt(b.Vmax, 4)} \\times ${g(b.D)}}{${g(f.nu)}} = ${fmt(Re)}`),
  ], meta, `${f.name[0].toUpperCase() + f.name.slice(1)} (${fluidProps(f, ["nu"])}) approaches ${bankStem(b)} at ${eq("V", V, "m/s")}. Find ${m("Re_{D,max}")}, the Reynolds number the Zukauskas correlation uses.`);
}

const C2_TABLE: Record<number, [number, number]> = { 3: [0.86, 0.84], 4: [0.9, 0.89], 5: [0.92, 0.92], 7: [0.95, 0.95], 10: [0.97, 0.97], 13: [0.98, 0.98], 16: [0.99, 0.99] };
function tbZukauskas(r: Rng): Draft {
  const water = r.chance(0.3);
  const f = water ? WATER300 : AIR300;
  const Prs = water ? r.pick([2.29, 3.0, 4.16]) : r.pick([0.700, 0.690]);
  const V = r.pick(water ? [0.1, 0.2, 0.3, 0.5] : [2, 4, 5, 6, 8, 10, 12]);
  const b = bank(r, V);
  const Re = (b.Vmax * b.D) / f.nu;
  require_(Re > 1000 && Re < 2e5);
  const NL = r.pick([3, 5, 7, 10, 16, 20, 25]);
  const C2c = NL >= 20 ? 1 : C2_TABLE[NL][b.aligned ? 0 : 1];
  let C: number, mm: number, cNote: string;
  if (b.aligned) [C, mm, cNote] = [0.27, 0.63, "aligned, 10³–2×10⁵"];
  else if (b.ST / b.SL < 2) {
    C = Number((0.35 * (b.ST / b.SL) ** 0.2).toFixed(3));
    mm = 0.6;
    cNote = `staggered, ${m("S_T/S_L < 2")}: ${m(`C = 0.35(S_T/S_L)^{1/5} = ${C}`)}`;
  } else [C, mm, cNote] = [0.4, 0.6, "staggered, S_T/S_L > 2"];
  const Nu = C2c * C * Re ** mm * f.Pr ** 0.36 * (f.Pr / Prs) ** 0.25;
  const h = (Nu * f.k) / b.D;
  return numeric(h, "h̄", "\\bar h", "W/m²·K", [
    ...vmaxSteps(b, V),
    m(`Re_{D,max} = \\frac{V_{max}D}{\\nu} = ${fmt(Re)}`),
    `Zukauskas (Eq 7.58, Table 7.5 ${cNote}): ${m(`\\bar{Nu}_D = C_2\\,C\\,Re_{D,max}^{m}Pr^{0.36}(Pr/Pr_s)^{1/4} = ${C2c}(${C})(${fmt(Re)})^{${mm}}(${g(f.Pr)})^{0.36}(${g(f.Pr)}/${g(Prs)})^{1/4} = ${fmt(Nu)}`)}.`,
    m(`\\bar h = \\frac{\\bar{Nu}_D\\,k}{D} = \\frac{${fmt(Nu)} \\times ${g(f.k)}}{${g(b.D)}} = ${fmt(h)}${u("W/m²·K")}`),
  ], { ht3: "tb-zukauskas", aligned: b.aligned, D: b.D, ST: b.ST, SL: b.SL, V, nu: f.nu, k: f.k, Pr: f.Pr, Prs, C, m: mm, C2: C2c },
  `${f.name[0].toUpperCase() + f.name.slice(1)} at ${eq("V", V, "m/s")} flows across ${bankStem(b)}, ${m(`N_L = ${NL}`)} rows deep. Properties: ${fluidProps(f, ["nu", "k", "Pr"])}, and ${m(`Pr_s = ${g(Prs)}`)} at the tube surface. Use ${m(`\\bar{Nu}_D = C_2\\,C\\,Re_{D,max}^{m}Pr^{0.36}(Pr/Pr_s)^{1/4}`)} with ${m(`C = ${C}`)}, ${m(`m = ${mm}`)}, ${m(`C_2 = ${C2c}`)}. Find the average convection coefficient.`);
}

function tbOutlet(r: Rng): Draft {
  const f = r.pick([AIR300, AIR350]);
  const V = r.pick([2, 4, 5, 6, 8, 10]);
  const b = bank(r, V);
  const h = r.pick([60, 80, 100, 135, 160, 200, 250]);
  const NT = r.pick([8, 10, 12, 15, 20]);
  const NL = r.pick([4, 6, 8, 10, 12, 16]);
  const N = NT * NL;
  const Ti = r.pick([15, 20, 25]);
  const Ts = r.pick([70, 90, 100, 120]);
  const expo = (PI * b.D * N * h) / (f.rho * V * NT * b.ST * f.cp);
  const To = Ts - (Ts - Ti) * Math.exp(-expo);
  const target = r.pick(["To", "q"] as const);
  const meta = { ht3: "tb-outlet", D: b.D, ST: b.ST, V, h, NT, NL, rho: f.rho, cp: f.cp, Ti, Ts, target };
  require_(Ts - To > 1);
  const dTlm = ((Ts - Ti) - (Ts - To)) / Math.log((Ts - Ti) / (Ts - To));
  const q = N * h * PI * b.D * dTlm;
  const stem = `Air (${fluidProps(f, ["rho", "cp"])}) enters a bank of ${m(mmTex(b.D))} tubes (${m(`S_T = ${mmTex(b.ST)}`)}, ${m(`N_T = ${NT}`)} tubes per row, ${m(`N_L = ${NL}`)} rows) at ${eq("V", V, "m/s")} and ${m(vu(Ti, "°C"))}. The tube walls are at ${m(vu(Ts, "°C"))} and ${m(`\\bar h = ${vu(h, "W/m²·K")}`)}.`;
  const s1 = `Energy balance on the air (Eq 7.62): ${m("\\frac{T_s - T_o}{T_s - T_i} = \\exp\\left(-\\frac{\\pi D N \\bar h}{\\rho V N_T S_T c_p}\\right)")}, ${m(`N = N_TN_L = ${N}`)}.`;
  const s2 = m(`\\frac{\\pi D N\\bar h}{\\rho V N_T S_T c_p} = \\frac{\\pi(${g(b.D)})(${N})(${h})}{(${g(f.rho)})(${g(V)})(${NT})(${g(b.ST)})(${g(f.cp)})} = ${fmt(expo, 4)}`);
  const s3 = m(`T_o = ${Ts} - (${Ts} - ${Ti})e^{-${fmt(expo, 4)}} = ${fmt(To, 4)}${u("°C")}`);
  if (target === "To") return numeric(To, "T_o", "T_o", "°C", [s1, s2, s3], meta, `${stem} Find the outlet air temperature ${m("T_o")}.`);
  return numeric(q, "q′", "q'", "W/m", [
    s1, s2, s3,
    m(`\\Delta T_{lm} = \\frac{(T_s - T_i) - (T_s - T_o)}{\\ln[(T_s - T_i)/(T_s - T_o)]} = ${fmt(dTlm, 4)}\\,\\mathrm{K}`),
    m(`q' = N\\bar h\\pi D\\,\\Delta T_{lm} = ${N}(${h})\\pi(${g(b.D)})(${fmt(dTlm, 4)}) = ${fmt(q)}${u("W/m")}`),
  ], meta, `${stem} Find the heat rate per unit length of tubes, ${m("q'")}.`);
}

// ═══ Ch 10 boiling ══════════════════════════════════════════════════════════
const WSAT = { rl: 957.9, rv: 0.5955, hfg: 2257e3, cpl: 4217, mul: 279e-6, Prl: 1.76, sig: 58.9e-3 };
const satProps = `${m(`\\rho_l = ${vu(WSAT.rl, "kg/m³")}`)}, ${m(`\\rho_v = ${vu(WSAT.rv, "kg/m³")}`)}, ${m(`h_{fg} = ${vu(WSAT.hfg, "J/kg")}`)}, ${m(`c_{p,l} = ${vu(WSAT.cpl, "J/kg·K")}`)}, ${m(`\\mu_l = ${vu(WSAT.mul, "N·s/m²")}`)}, ${m(`Pr_l = ${WSAT.Prl}`)}, ${m(`\\sigma = ${vu(WSAT.sig, "N/m")}`)}`;
const SURF = [
  { name: "polished copper", Csf: 0.0128 }, { name: "scored copper", Csf: 0.0068 },
  { name: "chemically etched stainless steel", Csf: 0.013 }, { name: "mechanically polished stainless steel", Csf: 0.013 },
  { name: "ground and polished stainless steel", Csf: 0.006 }, { name: "brass", Csf: 0.006 },
  { name: "nickel", Csf: 0.006 }, { name: "platinum", Csf: 0.013 },
];
const rohsenow = (dT: number, Csf: number) => {
  const W = WSAT;
  return W.mul * W.hfg * Math.sqrt((G * (W.rl - W.rv)) / W.sig) * ((W.cpl * dT) / (Csf * W.hfg * W.Prl)) ** 3;
};
const zuber = (S: { rl: number; rv: number; hfg: number; sig: number }, gg = G) =>
  0.149 * S.hfg * S.rv * ((S.sig * gg * (S.rl - S.rv)) / (S.rv * S.rv)) ** 0.25;

function boilRohsenow(r: Rng): Draft {
  const s = r.pick(SURF);
  const target = r.pick(["flux", "rate", "Ts"] as const);
  const qmax = zuber(WSAT);
  const meta0 = { ht3: "rohsenow", ...WSAT, Csf: s.Csf, n: 1, target };
  const pre = `Saturated water at 1 atm (${m("T_{sat} = 100^\\circ\\mathrm{C}")}; ${satProps}) boils on a ${s.name} surface (${m(`C_{s,f} = ${s.Csf}`)}, ${m("n = 1.0")}).`;
  const rohTex = "q''_s = \\mu_l h_{fg}\\left[\\frac{g(\\rho_l - \\rho_v)}{\\sigma}\\right]^{1/2}\\left(\\frac{c_{p,l}\\Delta T_e}{C_{s,f}h_{fg}Pr_l^n}\\right)^3";
  const grav = Math.sqrt((G * (WSAT.rl - WSAT.rv)) / WSAT.sig);
  if (target === "Ts") {
    const qs = r.pick([5e4, 1e5, 2e5, 3e5, 5e5, 8e5]);
    const dT = ((s.Csf * WSAT.hfg * WSAT.Prl) / WSAT.cpl) * (qs / (WSAT.mul * WSAT.hfg * grav)) ** (1 / 3);
    require_(dT > 5 && dT < 30 && qs < 0.9 * qmax);
    return numeric(100 + dT, "T_s", "T_s", "°C", [
      `Rohsenow (Eq 10.5): ${m(rohTex)}. Solve for ${m("\\Delta T_e = T_s - T_{sat}")}.`,
      m(`\\mu_l h_{fg}\\left[\\frac{g(\\rho_l - \\rho_v)}{\\sigma}\\right]^{1/2} = ${fmt(WSAT.mul * WSAT.hfg * grav, 4)}\\,\\mathrm{W/m^2}`),
      m(`\\Delta T_e = \\frac{C_{s,f}h_{fg}Pr_l}{c_{p,l}}\\left(\\frac{q''_s}{${fmt(WSAT.mul * WSAT.hfg * grav, 4)}}\\right)^{1/3} = ${fmt(dT, 4)}\\,\\mathrm{K}`),
      m(`T_s = 100 + ${fmt(dT, 4)} = ${fmt(100 + dT, 4)}${u("°C")}`),
    ], { ...meta0, qs },
    `${pre} What surface temperature gives a nucleate-boiling heat flux of ${m(`q''_s = ${vu(qs, "W/m²")}`)}? (${m(`g = ${G}\\,\\mathrm{m/s^2}`)})`);
  }
  const dT = r.pick([5, 6, 8, 10, 12, 15, 18, 20, 25]);
  const qs = rohsenow(dT, s.Csf);
  require_(qs < 0.9 * qmax);
  const steps = [
    `Excess temperature ${m(`\\Delta T_e = T_s - T_{sat} = ${100 + dT} - 100 = ${dT}\\,\\mathrm{K}`)} — between about 5 and 30 K: nucleate boiling, so Rohsenow (Eq 10.5) applies.`,
    m(rohTex),
    m(`q''_s = ${fmt(WSAT.mul * WSAT.hfg * grav, 4)}\\left(\\frac{${WSAT.cpl}(${dT})}{${s.Csf}(${g(WSAT.hfg)})(${WSAT.Prl})}\\right)^3 = ${fmt(qs)}${u("W/m²")}`),
  ];
  const stemT = `The surface is at ${m(vu(100 + dT, "°C"))}; ${m(`g = ${G}\\,\\mathrm{m/s^2}`)}.`;
  if (target === "flux") return numeric(qs, "q″_s", "q''_s", "W/m²", steps, { ...meta0, dT }, `${pre} ${stemT} Find the boiling heat flux.`);
  const geo = r.pick(["disk", "rod"] as const);
  const A = geo === "disk" ? (() => { const D = r.pick([0.1, 0.15, 0.2, 0.3]); return { A: (PI * D * D) / 4, tex: `${g(D)}-m-diameter horizontal disk (top face)`, s: `A = \\pi D^2/4 = ${fmt((PI * D * D) / 4, 4)}\\,\\mathrm{m^2}` }; })()
    : (() => { const D = r.pick([0.005, 0.01, 0.02]); const L = r.pick([0.2, 0.3, 0.5]); return { A: PI * D * L, tex: `${g(D * 1000)}-mm-diameter, ${g(L)}-m-long horizontal heater rod`, s: `A = \\pi DL = ${fmt(PI * D * L, 4)}\\,\\mathrm{m^2}` }; })();
  return numeric(qs * A.A, "q", "q", "W", [...steps, m(`${A.s}, \\quad q = q''_sA = ${fmt(qs * A.A)}${u("W")}`)], { ...meta0, dT, A: A.A },
    `${pre} The heater is a ${A.tex}. ${stemT} Find the power needed to hold this temperature.`);
}

function boilCHF(r: Rng): Draft {
  const set = r.pick([
    { label: "saturated water at 1 atm", rl: 957.9, rv: 0.5955, hfg: 2257e3, sig: 58.9e-3 },
    { label: "saturated water at 4.85 bar", rl: 915, rv: 2.55, hfg: 2114e3, sig: 48.8e-3 },
    { label: "saturated water at 2 bar", rl: 942, rv: 1.13, hfg: 2202e3, sig: 54.9e-3 },
  ]);
  const place = r.pick([
    { where: "on Earth", g: 9.8 }, { where: "on Earth", g: 9.8 }, { where: "on the Moon", g: 1.62 }, { where: "on Mars", g: 3.71 },
  ]);
  const target = r.pick(["flux", "flux", "power"] as const);
  const q = zuber(set, place.g);
  const props = `${m(`\\rho_l = ${vu(set.rl, "kg/m³")}`)}, ${m(`\\rho_v = ${vu(set.rv, "kg/m³")}`)}, ${m(`h_{fg} = ${vu(set.hfg, "J/kg")}`)}, ${m(`\\sigma = ${vu(set.sig, "N/m")}`)}`;
  const steps = [
    `Critical heat flux, Zuber/Lienhard (Eq 10.6) with ${m("C = 0.149")} for a large horizontal surface: ${m("q''_{max} = C h_{fg}\\rho_v\\left[\\frac{\\sigma g(\\rho_l - \\rho_v)}{\\rho_v^2}\\right]^{1/4}")}.`,
    m(`q''_{max} = 0.149(${g(set.hfg)})(${g(set.rv)})\\left[\\frac{${g(set.sig)}(${place.g})(${g(set.rl - set.rv)})}{${g(set.rv)}^2}\\right]^{1/4} = ${fmt(q)}${u("W/m²")}`),
  ];
  const meta = { ht3: "chf", rl: set.rl, rv: set.rv, hfg: set.hfg, sig: set.sig, g: place.g, C: 0.149, target };
  const pre = `A large horizontal heater boils ${set.label} ${place.where} (${m(`g = ${place.g}\\,\\mathrm{m/s^2}`)}). Properties: ${props}.`;
  if (target === "flux") return numeric(q, "q″_max", "q''_{max}", "W/m²", steps, meta, `${pre} Find the critical heat flux.`);
  const A = r.pick([0.01, 0.02, 0.05, 0.1]);
  return numeric(q * A, "q_max", "q_{max}", "W", [...steps, m(`q_{max} = q''_{max}A = ${fmt(q)}\\times${g(A)} = ${fmt(q * A)}${u("W")}`)], { ...meta, A },
    `${pre} The heater area is ${m(`${g(A)}\\,\\mathrm{m^2}`)}. What is the largest power it can dissipate in nucleate boiling before burnout risk?`);
}

const REGIMES = ["Free convection boiling", "Nucleate boiling", "Transition boiling", "Film boiling"];
function boilRegime(r: Rng): Draft {
  const k = r.int(0, 3);
  const dT = r.pick([[1, 2, 3, 4], [8, 10, 12, 15, 18, 22, 25], [40, 50, 60, 75, 90, 100], [150, 200, 300, 400, 500, 600]][k]);
  const inK = r.chance(0.3);
  const Ts = 100 + dT;
  return {
    prompt: `A surface at ${inK ? m(`${K(Ts).toFixed(2)}\\,\\mathrm{K}`) : m(vu(Ts, "°C"))} is submerged in saturated water at 1 atm (${m("T_{sat} = 100^\\circ\\mathrm{C}")}), with the surface temperature controlled. Which boiling regime is it in (boiling curve, Fig 10.4)?`,
    answer: { kind: "choice", options: REGIMES, correct: REGIMES[k] },
    answerTex: `\\text{${REGIMES[k]}}`,
    steps: [
      `Excess temperature ${m(`\\Delta T_e = T_s - T_{sat} = ${dT}\\,\\mathrm{K}`)}${inK ? ` (${m(`${K(Ts).toFixed(2)} - 373.15`)})` : ""}.`,
      `Water at 1 atm: free convection for ${m("\\Delta T_e \\lesssim 5\\,\\mathrm{K}")}; nucleate ${m("5 \\text{–} 30\\,\\mathrm{K}")} (up to the critical flux); transition ${m("30 \\text{–} 120\\,\\mathrm{K}")} (to the Leidenfrost point); film beyond ${m("120\\,\\mathrm{K}")}.`,
      `So: ${REGIMES[k].toLowerCase()}.`,
    ],
    meta: { ht3: "regime", dT, k },
  };
}

// ═══ Ch 10 condensation ═════════════════════════════════════════════════════
const COND_PROPS = [
  { Tf: 370, rl: 960.6, cpl: 4214, mul: 289e-6, kl: 0.679, Ts: [92, 94, 95, 96, 97, 98] },
  { Tf: 360, rl: 967.1, cpl: 4203, mul: 324e-6, kl: 0.674, Ts: [80, 82, 85, 88] },
];
const RV = 0.5955, HFG = 2257e3;
function condProps(P: (typeof COND_PROPS)[number]) {
  return `${m(`\\rho_l = ${vu(P.rl, "kg/m³")}`)}, ${m(`c_{p,l} = ${vu(P.cpl, "J/kg·K")}`)}, ${m(`\\mu_l = ${vu(P.mul, "N·s/m²")}`)}, ${m(`k_l = ${vu(P.kl, "W/m·K")}`)} (liquid, at ${m(`T_f \\approx ${P.Tf}\\,\\mathrm{K}`)}); ${m(`\\rho_v = ${RV}\\,\\mathrm{kg/m^3}`)}, ${m(`h_{fg} = ${vu(HFG, "J/kg")}`)} (at ${m("T_{sat}")}); ${m(`g = ${G}\\,\\mathrm{m/s^2}`)}`;
}

function condPlate(r: Rng): Draft {
  const P = COND_PROPS[0];
  const Ts = r.pick(P.Ts);
  const dT = 100 - Ts;
  const L = r.pick([0.02, 0.03, 0.04, 0.05, 0.08, 0.1]);
  const b = r.pick([0.1, 0.2, 0.3, 0.5, 1]);
  const hfgp = HFG + 0.68 * P.cpl * dT;
  const brk = (G * P.rl * (P.rl - RV) * P.kl ** 3 * hfgp) / (P.mul * L * dT);
  const h = 0.943 * brk ** 0.25;
  const q = h * L * b * dT;
  const md = q / hfgp;
  const Re = (4 * md) / (P.mul * b);
  require_(Re < 30);
  const target = r.pick(["h", "q", "mdot", "Re"] as const);
  const steps = [
    `Modified latent heat (film subcooling): ${m(`h'_{fg} = h_{fg} + 0.68c_{p,l}(T_{sat} - T_s) = ${g(HFG)} + 0.68(${P.cpl})(${dT}) = ${fmt(hfgp, 5)}\\,\\mathrm{J/kg}`)}.`,
    `Nusselt laminar film (Eq 10.30): ${m(`\\bar h_L = 0.943\\left[\\frac{g\\rho_l(\\rho_l - \\rho_v)k_l^3h'_{fg}}{\\mu_l(T_{sat} - T_s)L}\\right]^{1/4} = 0.943(${fmt(brk, 4)})^{1/4} = ${fmt(h, 4)}\\,\\mathrm{W/m^2\\cdot K}`)}.`,
  ];
  const q_ = m(`q = \\bar h_L(bL)(T_{sat} - T_s) = ${fmt(h, 4)}(${g(b)}\\times${g(L)})(${dT}) = ${fmt(q, 4)}\\,\\mathrm{W}`);
  const md_ = m(`\\dot m = \\frac{q}{h'_{fg}} = ${fmt(md, 4)}\\,\\mathrm{kg/s}`);
  const re_ = `${m(`Re_\\delta = \\frac{4\\dot m}{\\mu_l b} = \\frac{4(${fmt(md, 4)})}{(${g(P.mul)})(${g(b)})} = ${fmt(Re)}`)} ${m("\\le 30")}: laminar, wave-free — the Nusselt result holds.`;
  const meta = { ht3: "cond-plate", rl: P.rl, rv: RV, cpl: P.cpl, mul: P.mul, kl: P.kl, hfg: HFG, g: G, Tsat: 100, Ts, L, b, target };
  const pre = `Saturated steam at 1 atm (${m("T_{sat} = 100^\\circ\\mathrm{C}")}) condenses on a vertical plate ${g(L * 100)} cm high and ${g(b)} m wide held at ${m(vu(Ts, "°C"))}. Properties: ${condProps(P)}. Assume a laminar film.`;
  if (target === "h") return numeric(h, "h̄_L", "\\bar h_L", "W/m²·K", steps, meta, `${pre} Find the average condensation coefficient ${m("\\bar h_L")}.`);
  if (target === "q") return numeric(q, "q", "q", "W", [...steps, q_], meta, `${pre} Find the heat rate to the plate.`);
  if (target === "mdot") return numeric(md, "ṁ", "\\dot m", "kg/s", [...steps, q_, md_], meta, `${pre} Find the condensation rate ${m("\\dot m")}.`);
  return numeric(Re, "Re_δ", "Re_\\delta", "", [...steps, q_, md_, re_], meta, `${pre} Find the film Reynolds number ${m("Re_\\delta = 4\\dot m/(\\mu_l b)")} at the bottom of the plate and check the laminar assumption.`);
}

function condTube(r: Rng): Draft {
  const P = r.pick(COND_PROPS);
  const Ts = r.pick(P.Ts);
  const dT = 100 - Ts;
  const Dmm = r.pick([10, 12.7, 16, 19, 25, 38, 50]);
  const D = Dmm / 1000;
  const hfgp = HFG + 0.68 * P.cpl * dT;
  const brk = (G * P.rl * (P.rl - RV) * P.kl ** 3 * hfgp) / (P.mul * dT * D);
  const h = 0.729 * brk ** 0.25;
  const qp = h * PI * D * dT;
  const mp = qp / hfgp;
  const target = r.pick(["h", "mdot", "mdotL"] as const);
  const Lt = r.pick([1, 2, 3, 5]);
  const steps = [
    m(`h'_{fg} = h_{fg} + 0.68c_{p,l}\\Delta T = ${g(HFG)} + 0.68(${P.cpl})(${dT}) = ${fmt(hfgp, 5)}\\,\\mathrm{J/kg}`),
    `Single horizontal tube (Eq 10.46, ${m("C = 0.729")}): ${m(`\\bar h_D = 0.729\\left[\\frac{g\\rho_l(\\rho_l - \\rho_v)k_l^3h'_{fg}}{\\mu_l(T_{sat} - T_s)D}\\right]^{1/4} = 0.729(${fmt(brk, 4)})^{1/4} = ${fmt(h, 4)}\\,\\mathrm{W/m^2\\cdot K}`)}.`,
  ];
  const md_ = m(`\\dot m' = \\frac{\\bar h_D\\pi D(T_{sat} - T_s)}{h'_{fg}} = \\frac{${fmt(h, 4)}\\pi(${g(D)})(${dT})}{${fmt(hfgp, 5)}} = ${fmt(mp, 4)}\\,\\mathrm{kg/s\\cdot m}`);
  const meta = { ht3: "cond-tube", rl: P.rl, rv: RV, cpl: P.cpl, mul: P.mul, kl: P.kl, hfg: HFG, g: G, Tsat: 100, Ts, D, Lt, target };
  const pre = `Saturated steam at 1 atm (${m("T_{sat} = 100^\\circ\\mathrm{C}")}) condenses on the outside of a horizontal ${Dmm}-mm-diameter tube whose surface is at ${m(vu(Ts, "°C"))}. Properties: ${condProps(P)}.`;
  if (target === "h") return numeric(h, "h̄_D", "\\bar h_D", "W/m²·K", steps, meta, `${pre} Find the average condensation coefficient.`);
  if (target === "mdot") return numeric(mp, "ṁ′", "\\dot m'", "kg/s·m", [...steps, md_], meta, `${pre} Find the condensation rate per unit tube length ${m("\\dot m'")}.`);
  return numeric(mp * Lt * 3600, "ṁ", "\\dot m", "kg/h", [...steps, md_, m(`\\dot m = \\dot m'L \\times 3600 = ${fmt(mp, 4)}(${Lt})(3600) = ${fmt(mp * Lt * 3600)}\\,\\mathrm{kg/h}`)], meta,
    `${pre} The tube is ${Lt} m long. How much condensate does it collect per hour (kg/h)?`);
}

// ═══ Ch 12 radiation properties ═════════════════════════════════════════════
const BODIES = [
  { what: "the sun (an effective blackbody at 5800 K)", T: 5800 },
  { what: "a tungsten filament at 2800 K", T: 2800 },
  { what: "a tungsten filament at 3000 K", T: 3000 },
  { what: "a furnace wall at 1200 K", T: 1200 },
  { what: "a red-hot steel ingot at 1000 K", T: 1000 },
  { what: "human skin at 305 K", T: 305 },
  { what: "a 2000 K flame (as a blackbody)", T: 2000 },
  { what: "the earth's surface at 288 K", T: 288 },
];

function radWien(r: Rng): Draft {
  const target = r.pick(["lam", "lam", "T"] as const);
  if (target === "lam") {
    const B = r.pick(BODIES);
    const lam = WIEN / B.T;
    return numeric(lam, "λ_max", "\\lambda_{max}", "µm", [
      `Wien's displacement law (Eq 12.30): ${m("\\lambda_{max}T = C_3 = 2898\\,\\mu\\mathrm{m\\cdot K}")}, with ${m("T")} in kelvin.`,
      m(`\\lambda_{max} = \\frac{2898}{${B.T}} = ${fmt(lam)}\\,\\mu\\mathrm{m}`),
    ], { ht3: "wien", T: B.T, target },
    `At what wavelength (in µm) is the spectral emissive power of ${B.what} a maximum?`);
  }
  const lam = r.pick([0.4, 0.45, 0.5, 0.55, 0.65, 0.8, 1.2, 2, 3, 4.5, 9.5, 10]);
  const T = WIEN / lam;
  return numeric(T, "T", "T", "K", [
    m("\\lambda_{max}T = 2898\\,\\mu\\mathrm{m\\cdot K}"),
    m(`T = \\frac{2898}{${g(lam)}} = ${fmt(T)}\\,\\mathrm{K}`),
  ], { ht3: "wien", lam, target },
  `The emission spectrum of a source that behaves like a blackbody peaks at ${m(`\\lambda = ${g(lam)}\\,\\mu\\mathrm{m}`)}. Estimate its temperature.`);
}

function radStefan(r: Rng): Draft {
  const target = r.pick(["Eb", "power", "T"] as const);
  if (target === "Eb") {
    const Tc = r.pick([27, 100, 200, 327, 500, 727, 1000, 1227]);
    const Eb = SIGMA * K(Tc) ** 4;
    return numeric(Eb, "E_b", "E_b", "W/m²", [
      `Kelvin first: ${m(`T = ${Tc} + 273.15 = ${g(K(Tc))}\\,\\mathrm{K}`)} (using ${m(`${Tc}^4`)} instead is the classic slip).`,
      m(`E_b = \\sigma T^4 = (5.67\\times10^{-8})(${g(K(Tc))})^4 = ${fmt(Eb)}${u("W/m²")}`),
    ], { ht3: "stefan", T: K(Tc), eps: 1, target },
    `Find the total emissive power of a blackbody at ${m(vu(Tc, "°C"))}.`);
  }
  if (target === "power") {
    const T = r.pick([2500, 2800, 3000]);
    const eps = r.pick([0.3, 0.35, 0.4, 0.45]);
    const Dmm = r.pick([0.05, 0.08, 0.1, 0.2]);
    const Lmm = r.pick([10, 20, 30, 50]);
    const A = PI * (Dmm / 1000) * (Lmm / 1000);
    const q = eps * SIGMA * T ** 4 * A;
    return numeric(q, "q", "q", "W", [
      m(`A = \\pi DL = \\pi(${g(Dmm / 1000)})(${g(Lmm / 1000)}) = ${fmt(A, 4)}\\,\\mathrm{m^2}`),
      m(`q = \\varepsilon\\sigma T^4A = ${eps}(5.67\\times10^{-8})(${T})^4(${fmt(A, 4)}) = ${fmt(q)}${u("W")}`),
    ], { ht3: "stefan", T, eps, A, target },
    `A tungsten filament ${Dmm} mm in diameter and ${Lmm} mm long runs at ${m(`${T}\\,\\mathrm{K}`)} with total emissivity ${m(`\\varepsilon = ${eps}`)}. How much power does it emit (ignore the ends and any irradiation)?`);
  }
  const eps = r.pick([0.5, 0.7, 0.8, 0.9, 1]);
  const E = r.pick([500, 1000, 2500, 5000, 1e4, 5e4, 1e5]);
  const T = (E / (eps * SIGMA)) ** 0.25;
  return numeric(T, "T", "T", "K", [
    m("E = \\varepsilon\\sigma T^4 \\;\\Rightarrow\\; T = \\left(\\frac{E}{\\varepsilon\\sigma}\\right)^{1/4}"),
    m(`T = \\left(\\frac{${g(E)}}{${eps}(5.67\\times10^{-8})}\\right)^{1/4} = ${fmt(T)}\\,\\mathrm{K}`),
  ], { ht3: "stefan", E, eps, target },
  `A diffuse surface with total emissivity ${m(`${eps}`)} emits ${m(`E = ${vu(E, "W/m²")}`)}. Find its temperature in kelvin.`);
}

const BANDS = [
  { what: "the visible band", l1: 0.4, l2: 0.7 }, { what: "the visible band", l1: 0.38, l2: 0.78 },
  { what: "the near infrared", l1: 0.7, l2: 3 }, { what: "the band", l1: 1, l2: 5 }, { what: "the band", l1: 2, l2: 8 },
  { what: "the band", l1: 3, l2: 10 }, { what: "the ultraviolet band", l1: 0.2, l2: 0.4 },
];
function radBand(r: Rng): Draft {
  const B = r.pick(BODIES.filter((b) => b.T >= 1000));
  const target = r.pick(["band", "below", "above", "power"] as const);
  if (target === "band" || target === "power") {
    const bd = r.pick(BANDS);
    const F1 = bandFraction(bd.l1 * B.T), F2 = bandFraction(bd.l2 * B.T);
    const dF = F2 - F1;
    require_(dF > 0.005);
    const steps = [
      `Band fraction from Table 12.2 (Eq 12.34), using ${m("\\lambda T")}: ${m(`\\lambda_1T = ${g(bd.l1 * B.T)}`)}, ${m(`\\lambda_2T = ${g(bd.l2 * B.T)}\\,\\mu\\mathrm{m\\cdot K}`)}.`,
      m(`F_{(0\\to\\lambda_1)} = ${fmt(F1, 4)}, \\quad F_{(0\\to\\lambda_2)} = ${fmt(F2, 4)}`),
      m(`F_{(\\lambda_1\\to\\lambda_2)} = ${fmt(F2, 4)} - ${fmt(F1, 4)} = ${fmt(dF, 4)}`),
    ];
    const meta = { ht3: "band", T: B.T, l1: bd.l1, l2: bd.l2, target };
    if (target === "band")
      return numeric(dF, "F", "F_{(\\lambda_1\\to\\lambda_2)}", "", steps, meta,
        `What fraction of the total emission of ${B.what} lies in ${bd.what} ${m(`${bd.l1}\\text{–}${bd.l2}\\,\\mu\\mathrm{m}`)}?`);
    const Eb = SIGMA * B.T ** 4;
    return numeric(dF * Eb, "E_b,Δλ", "E_{b,\\Delta\\lambda}", "W/m²", [...steps, m(`E_{b,\\Delta\\lambda} = F\\,\\sigma T^4 = ${fmt(dF, 4)}(5.67\\times10^{-8})(${B.T})^4 = ${fmt(dF * Eb)}${u("W/m²")}`)], meta,
      `Treat ${B.what} as a blackbody. How much emissive power (W/m²) does it emit between ${m(`${bd.l1}`)} and ${m(`${bd.l2}\\,\\mu\\mathrm{m}`)}?`);
  }
  const lam = r.pick([0.5, 0.7, 1, 1.5, 2, 3, 4, 5]);
  const F = bandFraction(lam * B.T);
  const val = target === "below" ? F : 1 - F;
  require_(val > 0.005 && val < 0.995);
  return numeric(val, "F", target === "below" ? "F_{(0\\to\\lambda)}" : "F_{(\\lambda\\to\\infty)}", "", [
    m(`\\lambda T = ${g(lam)}\\times${B.T} = ${g(lam * B.T)}\\,\\mu\\mathrm{m\\cdot K}`),
    m(`F_{(0\\to\\lambda)} = ${fmt(F, 4)}`) + ` (Table 12.2).`,
    ...(target === "above" ? [m(`F_{(\\lambda\\to\\infty)} = 1 - F_{(0\\to\\lambda)} = ${fmt(val, 4)}`)] : []),
  ], { ht3: "band", T: B.T, l1: target === "below" ? 0 : lam, l2: target === "below" ? lam : -1 /* ∞ */, target },
  `What fraction of the emission of ${B.what} is at wavelengths ${target === "below" ? "shorter" : "longer"} than ${m(`${lam}\\,\\mu\\mathrm{m}`)}?`);
}

function radSpectral(r: Rng): Draft {
  const target = r.pick(["eps", "E", "alphaS"] as const);
  const lc = r.pick([1, 1.5, 2, 3, 4, 5]);
  const a1 = r.pick([0.1, 0.2, 0.4, 0.6, 0.8, 0.9]);
  let a2 = r.pick([0.1, 0.2, 0.4, 0.6, 0.8, 0.9]);
  require_(a1 !== a2);
  if (target === "alphaS") {
    const Ts = 5800;
    const F = bandFraction(lc * Ts);
    const al = a1 * F + a2 * (1 - F);
    return numeric(al, "α_S", "\\alpha_S", "", [
      `Solar irradiation is proportional to a 5800 K blackbody spectrum, so ${m("\\alpha_S = \\alpha_1F_{(0\\to\\lambda_c)} + \\alpha_2[1 - F_{(0\\to\\lambda_c)}]")} with ${m("T = 5800\\,\\mathrm{K}")}, not the surface temperature.`,
      m(`\\lambda_cT = ${lc}\\times5800 = ${lc * 5800}\\,\\mu\\mathrm{m\\cdot K}: \\; F_{(0\\to\\lambda_c)} = ${fmt(F, 4)}`),
      m(`\\alpha_S = ${a1}(${fmt(F, 4)}) + ${a2}(${fmt(1 - F, 4)}) = ${fmt(al)}`),
    ], { ht3: "spectral", T: Ts, lc, a1, a2, target },
    `An opaque, diffuse surface has spectral absorptivity ${m(`\\alpha_\\lambda = ${a1}`)} for ${m(`\\lambda < ${lc}\\,\\mu\\mathrm{m}`)} and ${m(`\\alpha_\\lambda = ${a2}`)} beyond. Find its solar absorptivity ${m("\\alpha_S")} (sun as a 5800 K blackbody).`);
  }
  const T = r.pick([400, 500, 800, 1000, 1200, 1500, 2000]);
  const F = bandFraction(lc * T);
  require_(F > 0.003);
  const eps = a1 * F + a2 * (1 - F);
  const steps = [
    `Total emissivity weights ${m("\\varepsilon_\\lambda")} by the blackbody spectrum at the surface temperature: ${m("\\varepsilon = \\varepsilon_1F_{(0\\to\\lambda_c)} + \\varepsilon_2[1 - F_{(0\\to\\lambda_c)}]")}.`,
    m(`\\lambda_cT = ${lc}\\times${T} = ${lc * T}\\,\\mu\\mathrm{m\\cdot K}: \\; F_{(0\\to\\lambda_c)} = ${fmt(F, 4)}`),
    m(`\\varepsilon = ${a1}(${fmt(F, 4)}) + ${a2}(${fmt(1 - F, 4)}) = ${fmt(eps, 4)}`),
  ];
  const meta = { ht3: "spectral", T, lc, a1, a2, target };
  const pre = `A diffuse surface at ${m(`${T}\\,\\mathrm{K}`)} has spectral emissivity ${m(`\\varepsilon_\\lambda = ${a1}`)} for ${m(`\\lambda < ${lc}\\,\\mu\\mathrm{m}`)} and ${m(`\\varepsilon_\\lambda = ${a2}`)} for ${m(`\\lambda > ${lc}\\,\\mu\\mathrm{m}`)}.`;
  if (target === "eps") return numeric(eps, "ε", "\\varepsilon", "", steps, meta, `${pre} Find its total hemispherical emissivity.`);
  const E = eps * SIGMA * T ** 4;
  return numeric(E, "E", "E", "W/m²", [...steps, m(`E = \\varepsilon\\sigma T^4 = ${fmt(eps, 4)}(5.67\\times10^{-8})(${T})^4 = ${fmt(E)}${u("W/m²")}`)], meta,
    `${pre} Find its total emissive power ${m("E")}.`);
}

function radBalance(r: Rng): Draft {
  const target = r.pick(["J", "net", "Teq", "solar"] as const);
  if (target === "solar") {
    const coat = r.pick([
      { name: "white paint", aS: 0.21, eps: 0.93 }, { name: "black paint", aS: 0.97, eps: 0.97 },
      { name: "polished aluminum", aS: 0.09, eps: 0.03 }, { name: "anodized aluminum", aS: 0.14, eps: 0.84 },
      { name: "a selective black-chrome coating", aS: 0.9, eps: 0.1 },
    ]);
    const GS = r.pick([600, 700, 800, 900, 1000]);
    const h = r.pick([5, 10, 15, 20, 25]);
    const Tinf = r.pick([290, 295, 300]);
    const Tsky = r.pick([250, 260, 270]);
    const f = (T: number) => coat.aS * GS + coat.eps * SIGMA * Tsky ** 4 - coat.eps * SIGMA * T ** 4 - h * (T - Tinf);
    const T = bisect(f, 150, 1000);
    return numeric(T, "T_s", "T_s", "K", [
      `Surface energy balance (opaque, back insulated). Absorbed solar uses ${m("\\alpha_S")}; the long-wave sky irradiation ${m("G_{sky} = \\sigma T_{sky}^4")} is absorbed with ${m("\\alpha = \\varepsilon")} (Kirchhoff, gray in the infrared): ${m("\\alpha_SG_S + \\varepsilon\\sigma T_{sky}^4 = \\varepsilon\\sigma T_s^4 + h(T_s - T_\\infty)")}.`,
      m(`${coat.aS}(${GS}) + ${coat.eps}(5.67\\times10^{-8})(${Tsky})^4 = ${coat.eps}(5.67\\times10^{-8})T_s^4 + ${h}(T_s - ${Tinf})`),
      `Solve by iteration: ${m(`T_s = ${fmt(T, 4)}\\,\\mathrm{K}`)} (${m(`${fmt(T - 273.15, 3)}^\\circ\\mathrm{C}`)}).`,
    ], { ht3: "rad-balance", aS: coat.aS, eps: coat.eps, GS, h, Tinf, Tsky, target },
    `A horizontal roof coated with ${coat.name} (${m(`\\alpha_S = ${coat.aS}`)}, ${m(`\\varepsilon = ${coat.eps}`)}) receives ${m(`G_S = ${vu(GS, "W/m²")}`)} of sunlight; the sky behaves as a blackbody at ${m(`${Tsky}\\,\\mathrm{K}`)}, and air at ${m(`${Tinf}\\,\\mathrm{K}`)} gives ${m(`h = ${vu(h, "W/m²·K")}`)}. The underside is insulated. Find the steady roof temperature in kelvin.`);
  }
  const eps = r.pick([0.2, 0.4, 0.6, 0.75, 0.8, 0.9]);
  const Gi = r.pick([500, 1000, 2000, 3000, 5000, 1e4]);
  if (target === "Teq") {
    const T = (Gi / SIGMA) ** 0.25;
    return numeric(T, "T", "T", "K", [
      `No convection, back insulated: absorbed = emitted, ${m("\\alpha G = \\varepsilon\\sigma T^4")}.`,
      `Gray and diffuse ⇒ ${m("\\alpha = \\varepsilon")} (Kirchhoff), so ${m("\\varepsilon")} cancels: ${m(`T = (G/\\sigma)^{1/4} = (${g(Gi)}/5.67\\times10^{-8})^{1/4} = ${fmt(T)}\\,\\mathrm{K}`)}.`,
    ], { ht3: "rad-balance", eps, G: Gi, target },
    `An opaque, diffuse, gray plate (${m(`\\varepsilon = ${eps}`)}) in vacuum is insulated on its back and receives irradiation ${m(`G = ${vu(Gi, "W/m²")}`)} on its front. Find its steady temperature in kelvin.`);
  }
  const T = r.pick([300, 350, 400, 500, 600, 800]);
  const E = eps * SIGMA * T ** 4;
  const J = E + (1 - eps) * Gi;
  const net = E - eps * Gi;
  require_(Math.abs(net) > 5);
  const steps = [
    `Opaque, diffuse, gray: ${m(`\\alpha = \\varepsilon = ${eps}`)}, ${m(`\\rho = 1 - \\alpha = ${g(1 - eps)}`)}.`,
    m(`E = \\varepsilon\\sigma T^4 = ${eps}(5.67\\times10^{-8})(${T})^4 = ${fmt(E, 4)}\\,\\mathrm{W/m^2}`),
  ];
  const meta = { ht3: "rad-balance", eps, G: Gi, T, target };
  const pre = `An opaque, diffuse, gray surface (${m(`\\varepsilon = ${eps}`)}) at ${m(`${T}\\,\\mathrm{K}`)} receives irradiation ${m(`G = ${vu(Gi, "W/m²")}`)}.`;
  if (target === "J")
    return numeric(J, "J", "J", "W/m²", [...steps, m(`J = E + \\rho G = ${fmt(E, 4)} + ${g(1 - eps)}(${g(Gi)}) = ${fmt(J)}${u("W/m²")}`)], meta, `${pre} Find its radiosity ${m("J")}.`);
  return numeric(net, "q″_rad", "q''_{rad}", "W/m²", [
    ...steps,
    m(`q''_{rad} = E - \\alpha G = ${fmt(E, 4)} - ${eps}(${g(Gi)}) = ${fmt(net)}${u("W/m²")}`) + (net < 0 ? " — negative: the surface gains radiant energy." : "."),
  ], meta, `${pre} Find the net radiative flux leaving the surface, ${m("q''_{rad} = J - G")}.`);
}

// ═══ Ch 14 diffusion mass transfer ══════════════════════════════════════════
function mdFick(r: Rng): Draft {
  const kind = r.pick(["solid", "gas", "gas-mass"] as const);
  if (kind === "solid") {
    const D = r.pick([1.2e-12, 1e-11, 2.6e-13]);
    const T = D === 1.2e-12 ? 358 : D === 1e-11 ? 438 : 293;
    const metal = D === 2.6e-13 ? "iron" : "nickel";
    const C1 = r.pick([0.01, 0.02, 0.03, 0.05]);
    const C2_ = r.pick([0, 0.001, 0.002, 0.005]);
    const Lmm = r.pick([0.5, 1, 2, 3, 5]);
    const L = Lmm / 1000;
    const N = (D * (C1 - C2_)) / L;
    const mass = r.chance(0.5);
    const meta = { ht3: "fick", kind, D, C1, C2: C2_, L, M: 2.016, mass };
    const steps = [
      `Stationary medium (the metal does not move), steady, 1-D, no reaction: ${m("C_A")} is linear and ${m("N''_A = J^*_A = D_{AB}\\frac{C_{A,1} - C_{A,2}}{L}")}.`,
      m(`N''_A = ${g(D)}\\cdot\\frac{${C1} - ${C2_}}{${g(L)}} = ${fmt(N)}${u("kmol/s·m²")}`),
    ];
    const pre = `Hydrogen diffuses through a ${Lmm}-mm ${metal} plate at ${T} K (${m(`D_{AB} = ${vu(D, "m²/s")}`)}). The molar concentrations of H₂ in the metal at its two faces are ${m(`${C1}`)} and ${m(`${C2_}\\,\\mathrm{kmol/m^3}`)}.`;
    if (!mass) return numeric(N, "N″_A", "N''_A", "kmol/s·m²", steps, meta, `${pre} Find the molar flux of hydrogen.`);
    return numeric(N * 2.016, "n″_A", "n''_A", "kg/s·m²", [...steps, `Mass flux: multiply by ${m("\\mathcal M_A = 2.016\\,\\mathrm{kg/kmol}")}: ${m(`n''_A = ${fmt(N * 2.016)}\\,\\mathrm{kg/s\\cdot m^2}`)}.`], meta,
      `${pre} Find the mass flux of hydrogen (kg/s·m²; ${m("\\mathcal M_{H_2} = 2.016\\,\\mathrm{kg/kmol}")}).`);
  }
  const pair = r.pick([
    { A: "CO₂", B: "N₂", D: 0.16e-4, M: 44.01 }, { A: "H₂", B: "air", D: 0.41e-4, M: 2.016 },
    { A: "NH₃", B: "air", D: 0.28e-4, M: 17.03 }, { A: "O₂", B: "N₂", D: 0.18e-4, M: 32 },
  ]);
  const T = 298;
  const p = 101.325;
  const C = p / (RU * T);
  const x1 = r.pick([0.2, 0.3, 0.5, 0.6, 0.8]);
  const x2 = r.pick([0, 0.05, 0.1]);
  const L = r.pick([0.1, 0.2, 0.25, 0.5, 1]);
  const Dmm = r.pick([10, 20, 25, 50]);
  const A = (PI * (Dmm / 1000) ** 2) / 4;
  const N = (C * pair.D * (x1 - x2)) / L;
  const steps = [
    m(`C = \\frac{p}{\\mathcal R T} = \\frac{${p}}{8.314 \\times ${T}} = ${fmt(C, 4)}\\,\\mathrm{kmol/m^3}`),
    `Equimolar counterdiffusion (${m("N_A = -N_B")}): no net molar flow, so ${m("N''_A = J^*_A = CD_{AB}\\frac{x_{A,1} - x_{A,2}}{L}")}.`,
    m(`N''_A = ${fmt(C, 4)}(${g(pair.D)})\\frac{${x1} - ${x2}}{${g(L)}} = ${fmt(N, 4)}\\,\\mathrm{kmol/s\\cdot m^2}`),
    m(`N_A = N''_A\\frac{\\pi D^2}{4} = ${fmt(N, 4)}(${fmt(A, 4)}) = ${fmt(N * A, 4)}\\,\\mathrm{kmol/s}`),
  ];
  const meta = { ht3: "fick", kind, D: pair.D, x1, x2, L, p, T, A, M: pair.M };
  const pre = `Two large tanks of ${pair.A}–${pair.B} gas at 1 atm (${m(`p = ${p}\\,\\mathrm{kPa}`)}) and ${T} K are joined by a ${g(L)}-m tube of ${Dmm}-mm diameter. The mole fraction of ${pair.A} is ${m(`${x1}`)} in one tank and ${m(`${x2}`)} in the other; ${m(`D_{AB} = ${vu(pair.D, "m²/s")}`)}, ${m(`\\mathcal R = 8.314\\,\\mathrm{kJ/kmol\\cdot K}`)}. Assume equimolar counterdiffusion.`;
  if (kind === "gas") return numeric(N * A, "N_A", "N_A", "kmol/s", steps, meta, `${pre} Find the molar transfer rate of ${pair.A} (kmol/s).`);
  return numeric(N * A * pair.M, "n_A", "n_A", "kg/s", [...steps, `To mass: ${m(`n_A = \\mathcal M_AN_A = ${pair.M}(${fmt(N * A, 4)}) = ${fmt(N * A * pair.M)}\\,\\mathrm{kg/s}`)} — kmol × kg/kmol, not kmol alone.`], meta,
    `${pre} Find the mass transfer rate of ${pair.A} in kg/s (${m(`\\mathcal M_A = ${pair.M}\\,\\mathrm{kg/kmol}`)}).`);
}

const WATER_EVAP = [
  { T: 298, psat: 3.169, D: 0.26e-4 }, { T: 320, psat: 10.53, D: 0.29e-4 }, { T: 340, psat: 27.18, D: 0.32e-4 },
];
function mdStefan(r: Rng): Draft {
  const W = r.pick(WATER_EVAP);
  const p = 101.325;
  const C = p / (RU * W.T);
  const xA0 = W.psat / p;
  const phi = r.pick([0, 0, 0.2, 0.5]);
  const xAL = Number(((phi * 3.169) / p).toPrecision(4)); // air at the tube mouth is room air at 298 K
  const L = r.pick([0.05, 0.1, 0.15, 0.2, 0.3]);
  const Dmm = r.pick([10, 20, 25, 50]);
  const A = (PI * (Dmm / 1000) ** 2) / 4;
  const N = ((C * W.D) / L) * Math.log((1 - xAL) / (1 - xA0));
  const target = r.pick(["N", "rate"] as const);
  const steps = [
    `Stagnant air (${m("N_B = 0")}), so water vapor carries bulk motion with it (Stefan flow): ${m("N''_A = -CD_{AB}\\frac{dx_A}{dx} + x_AN''_A")}. Integrating with constant ${m("N''_A")}: ${m("N''_A = \\frac{CD_{AB}}{L}\\ln\\frac{1 - x_{A,L}}{1 - x_{A,0}}")}.`,
    `${m(`C = \\frac{p}{\\mathcal RT} = \\frac{${p}}{8.314(${W.T})} = ${fmt(C, 4)}\\,\\mathrm{kmol/m^3}`)}; at the liquid surface ${m(`x_{A,0} = p_{sat}/p = ${g(W.psat)}/${p} = ${fmt(xA0, 4)}`)}; at the top ${m(`x_{A,L} = ${fmt(xAL, 4)}`)}.`,
    m(`N''_A = \\frac{${fmt(C, 4)}(${g(W.D)})}{${g(L)}}\\ln\\frac{1 - ${fmt(xAL, 4)}}{1 - ${fmt(xA0, 4)}} = ${fmt(N, 4)}\\,\\mathrm{kmol/s\\cdot m^2}`),
  ];
  const meta = { ht3: "stefan-flow", T: W.T, p, D: W.D, xA0, xAL, L, A, M: 18.02, target };
  const pre = `Water at ${W.T} K sits at the bottom of a ${Dmm}-mm-diameter tube; the liquid surface is ${g(L * 100)} cm below the open top. Air at 1 atm (${m(`p = ${p}\\,\\mathrm{kPa}`)}) flows across the top ${phi === 0 ? "and is dry" : `with a water-vapor mole fraction of ${m(fmt(xAL, 4))}`}. Take ${m(`p_{sat} = ${vu(W.psat, "kPa")}`)}, ${m(`D_{AB} = ${vu(W.D, "m²/s")}`)}, ${m("\\mathcal R = 8.314\\,\\mathrm{kJ/kmol\\cdot K}")}, and the column isothermal at ${W.T} K.`;
  if (target === "N") return numeric(N, "N″_A", "N''_A", "kmol/s·m²", steps, meta, `${pre} Find the molar evaporation flux ${m("N''_A")}, including bulk motion.`);
  const rate = N * A * 18.02 * 3600;
  return numeric(rate, "ṁ", "\\dot m", "kg/h", [...steps, m(`\\dot m = N''_A\\,\\frac{\\pi D^2}{4}\\,\\mathcal M_A\\,(3600) = ${fmt(N, 4)}(${fmt(A, 4)})(18.02)(3600) = ${fmt(rate)}\\,\\mathrm{kg/h}`)], meta,
    `${pre} Find the evaporation rate in kg/h (${m("\\mathcal M_{H_2O} = 18.02\\,\\mathrm{kg/kmol}")}).`);
}

const MEMBRANES = [
  { gas: "H₂", S: 0.04, D: 0.85e-9, M: 2.016 }, { gas: "O₂", S: 0.07, D: 0.21e-9, M: 32 },
  { gas: "N₂", S: 0.035, D: 0.15e-9, M: 28.01 }, { gas: "CO₂", S: 0.9, D: 0.11e-9, M: 44.01 },
];
function mdMembrane(r: Rng): Draft {
  const mb = r.pick(MEMBRANES);
  const p1 = r.pick([2, 3, 5, 10]);
  const p2 = r.pick([0, 0.2, 1]);
  const Lmm = r.pick([0.5, 1, 2, 5]);
  const L = Lmm / 1000;
  const A = r.pick([0.01, 0.05, 0.1, 0.5]);
  const target = r.pick(["Cs", "N", "mass"] as const);
  const Cs = mb.S * p1;
  const N = (mb.D * mb.S * (p1 - p2)) / L;
  const meta = { ht3: "membrane", S: mb.S, D: mb.D, p1, p2, L, A, M: mb.M, target };
  const pre = `${mb.gas} at ${p1} bar is held behind a vulcanized-rubber membrane ${Lmm} mm thick; the gas pressure on the other side is ${p2} bar. Solubility ${m(`S = ${vu(mb.S, "kmol/m³·bar")}`)}, ${m(`D_{AB} = ${vu(mb.D, "m²/s")}`)}.`;
  const s1 = `Gas–solid interface: ${m("C_{A,s} = S\\,p_A")}, so ${m(`C_{A,1} = ${mb.S}(${p1}) = ${fmt(Cs, 4)}`)} and ${m(`C_{A,2} = ${mb.S}(${p2}) = ${fmt(mb.S * p2, 4)}\\,\\mathrm{kmol/m^3}`)}.`;
  if (target === "Cs") return numeric(Cs, "C_A,s", "C_{A,s}", "kmol/m³", [s1], meta, `${pre} Find the molar concentration of ${mb.gas} in the rubber at the high-pressure face.`);
  const s2 = m(`N''_A = D_{AB}\\frac{C_{A,1} - C_{A,2}}{L} = \\frac{D_{AB}S(p_1 - p_2)}{L} = ${fmt(N)}\\,\\mathrm{kmol/s\\cdot m^2}`);
  if (target === "N") return numeric(N, "N″_A", "N''_A", "kmol/s·m²", [s1, s2], meta, `${pre} Find the molar diffusion flux of ${mb.gas} through the membrane.`);
  const rate = N * A * mb.M;
  return numeric(rate, "n_A", "n_A", "kg/s", [s1, s2, m(`n_A = \\mathcal M_AN''_AA = ${mb.M}(${fmt(N)})(${g(A)}) = ${fmt(rate)}\\,\\mathrm{kg/s}`)], meta,
    `${pre} The membrane area is ${m(`${g(A)}\\,\\mathrm{m^2}`)}. Find the mass leak rate of ${mb.gas} (${m(`\\mathcal M_A = ${mb.M}\\,\\mathrm{kg/kmol}`)}).`);
}

function mdReaction(r: Rng): Draft {
  const D = r.pick([1.5e-9, 2e-9, 2.6e-9]);
  const k1 = r.pick([1e-3, 2e-3, 5e-3, 0.01, 0.02, 0.05]);
  const Lmm = r.pick([0.5, 1, 2, 3, 5]);
  const L = Lmm / 1000;
  const mm = Math.sqrt(k1 / D);
  const mL = mm * L;
  require_(mL > 0.3 && mL < 6);
  const C0 = r.pick([0.01, 0.02, 0.03, 0.05]);
  const target = r.pick(["flux", "CL"] as const);
  const meta = { ht3: "reaction", D, k1, L, C0, target };
  const steps = [
    `Steady diffusion with first-order consumption ${m("\\dot N_A = -k_1C_A")}: ${m("D_{AB}\\frac{d^2C_A}{dx^2} - k_1C_A = 0")}, with ${m("C_A(0) = C_{A,0}")} and ${m("dC_A/dx = 0")} at the impermeable bottom ${m("x = L")}.`,
    `${m("C_A(x) = C_{A,0}\\frac{\\cosh m(L - x)}{\\cosh mL}")}, ${m(`m = \\sqrt{k_1/D_{AB}} = \\sqrt{${g(k1)}/${g(D)}} = ${fmt(mm, 4)}\\,\\mathrm{m^{-1}}`)}, ${m(`mL = ${fmt(mL, 4)}`)}.`,
  ];
  const pre = `Gas A dissolves at the surface of a stagnant liquid layer ${Lmm} mm deep (surface concentration ${m(`C_{A,0} = ${vu(C0, "kmol/m³")}`)}) and is consumed in the liquid by a first-order reaction, ${m(`k_1 = ${vu(k1, "s⁻¹")}`)}; ${m(`D_{AB} = ${vu(D, "m²/s")}`)}. The bottom of the layer is impermeable.`;
  if (target === "CL") {
    const CL = C0 / Math.cosh(mL);
    return numeric(CL, "C_A(L)", "C_A(L)", "kmol/m³", [...steps, m(`C_A(L) = \\frac{C_{A,0}}{\\cosh mL} = \\frac{${C0}}{\\cosh ${fmt(mL, 4)}} = ${fmt(CL)}\\,\\mathrm{kmol/m^3}`)], meta,
      `${pre} Find the concentration of A at the bottom of the layer.`);
  }
  const N = D * C0 * mm * Math.tanh(mL);
  return numeric(N, "N″_A", "N''_A", "kmol/s·m²", [...steps, m(`N''_A(0) = -D_{AB}\\frac{dC_A}{dx}\\Big|_0 = D_{AB}C_{A,0}m\\tanh mL = ${fmt(N)}\\,\\mathrm{kmol/s\\cdot m^2}`)], meta,
    `${pre} Find the molar flux of A into the liquid at its surface.`);
}

// ═══ §6.7–6.8, Ch 7 convective mass transfer ════════════════════════════════
const SPECIES = [
  { name: "water vapor", D: 0.26e-4 }, { name: "naphthalene vapor", D: 0.62e-5 }, { name: "ammonia", D: 0.28e-4 },
];
function mcAnalogy(r: Rng): Draft {
  const sp = r.pick(SPECIES);
  const f = AIR300;
  const reverse = r.chance(0.35);
  const Le = f.alpha / sp.D;
  const fac = f.k / (sp.D * Le ** (1 / 3)); // Eq 6.92 with n = 1/3 (≈ ρc_pLe^{2/3})
  const steps = (h: number, hm: number) => [
    `Same geometry and flow, so the dimensionless correlations match: ${m("\\frac{\\bar{Nu}}{Pr^{n}} = \\frac{\\bar{Sh}}{Sc^{n}}")}, ${m("n = 1/3")}. Hence (Eq 6.92) ${m("\\frac{\\bar h}{\\bar h_m} = \\frac{k}{D_{AB}Le^{1-n}} \\approx \\rho c_pLe^{2/3}")}.`,
    m(`Le = \\frac{\\alpha}{D_{AB}} = \\frac{${g(f.alpha)}}{${g(sp.D)}} = ${fmt(Le, 4)}, \\quad \\frac{k}{D_{AB}Le^{1/3}} = \\frac{${g(f.k)}}{${g(sp.D)}(${fmt(Le, 4)})^{1/3}} = ${fmt(fac, 4)}\\,\\mathrm{J/m^3\\cdot K}`),
    reverse
      ? m(`\\bar h = \\bar h_m\\,\\frac{k}{D_{AB}Le^{1/3}} = ${g(hm)}(${fmt(fac, 4)}) = ${fmt(h)}\\,\\mathrm{W/m^2\\cdot K}`)
      : m(`\\bar h_m = \\bar h\\,\\frac{D_{AB}Le^{1/3}}{k} = \\frac{${g(h)}}{${fmt(fac, 4)}} = ${fmt(hm)}\\,\\mathrm{m/s}`),
  ];
  const props = `air at 300 K: ${fluidProps(f, ["k", "alpha"])}; ${sp.name}–air ${m(`D_{AB} = ${vu(sp.D, "m²/s")}`)}`;
  if (!reverse) {
    const h = r.pick([10, 20, 35, 50, 80, 120]);
    const hm = h / fac;
    return numeric(hm, "h̄_m", "\\bar h_m", "m/s", steps(h, hm), { ht3: "analogy", h, k: f.k, alpha: f.alpha, D: sp.D, reverse },
      `Heat-transfer tests on a model in an air stream give ${m(`\\bar h = ${vu(h, "W/m²·K")}`)}. Use the heat–mass analogy to find the average mass-transfer coefficient for ${sp.name} from an identically shaped surface in the same flow (${props}).`);
  }
  const hm = r.pick([0.005, 0.01, 0.02, 0.03, 0.05]);
  const h = hm * fac;
  return numeric(h, "h̄", "\\bar h", "W/m²·K", steps(h, hm), { ht3: "analogy", hm, k: f.k, alpha: f.alpha, D: sp.D, reverse },
    `Sublimation/evaporation tests in an air stream give ${m(`\\bar h_m = ${vu(hm, "m/s")}`)} for ${sp.name} from a model. Use the heat–mass analogy to find the convection heat-transfer coefficient for the same shape and flow (${props}).`);
}

const RHO_SAT = [
  { T: 290, rho: 0.01435 }, { T: 298, rho: 0.02306 }, { T: 300, rho: 0.02556 }, { T: 310, rho: 0.04361 }, { T: 320, rho: 0.07153 },
];
function mcEvap(r: Rng): Draft {
  const target = r.pick(["rate", "q", "Tinf"] as const);
  if (target === "Tinf") {
    const S = r.pick(RHO_SAT.slice(0, 3));
    const f = AIR300;
    const D = 0.26e-4;
    const hfg = 2.44e6;
    const Le = f.alpha / D;
    const dT = (hfg * S.rho * D * Le ** (1 / 3)) / f.k;
    return numeric(S.T + dT, "T_∞", "T_\\infty", "K", [
      `Steady wetted surface: convection in = evaporation out, ${m("\\bar h(T_\\infty - T_s) = \\bar h_mh_{fg}(\\rho_{A,s} - \\rho_{A,\\infty})")}, with ${m("\\rho_{A,\\infty} = 0")} for dry air.`,
      `Analogy (Eq 6.92, ${m("n = 1/3")}): ${m("\\bar h/\\bar h_m = k/(D_{AB}Le^{1/3}) \\approx \\rho c_pLe^{2/3}")}, ${m(`Le = ${g(f.alpha)}/${g(D)} = ${fmt(Le, 4)}`)}.`,
      m(`T_\\infty - T_s = \\frac{h_{fg}\\rho_{A,sat}(T_s)\\,D_{AB}Le^{1/3}}{k} = \\frac{${g(hfg)}(${g(S.rho)})(${g(D)})(${fmt(Le, 4)})^{1/3}}{${g(f.k)}} = ${fmt(dT, 4)}\\,\\mathrm{K}`),
      m(`T_\\infty = ${S.T} + ${fmt(dT, 4)} = ${fmt(S.T + dT, 4)}\\,\\mathrm{K}`),
    ], { ht3: "evap-cool", Ts: S.T, rhoAs: S.rho, alpha: f.alpha, k: f.k, D, hfg },
    `A wetted wick (wet-bulb thermometer) in a stream of dry air reads ${m(`T_s = ${S.T}\\,\\mathrm{K}`)} at steady state. Neglecting radiation, find the air temperature ${m("T_\\infty")}. Take ${m(`\\rho_{A,sat}(T_s) = ${vu(S.rho, "kg/m³")}`)}, ${m(`h_{fg} = ${vu(hfg, "J/kg")}`)}, ${m(`D_{AB} = ${vu(D, "m²/s")}`)}, and air ${fluidProps(f, ["k", "alpha"])}.`);
  }
  const Ss = r.pick(RHO_SAT.slice(1));
  const Sinf = r.pick(RHO_SAT.filter((s) => s.T <= Ss.T));
  const phi = r.pick([0, 0.3, 0.5, 0.6, 0.8]);
  const hm = r.pick([0.005, 0.01, 0.015, 0.02, 0.03]);
  const A = r.pick([0.05, 0.1, 0.25, 0.5, 1, 2]);
  const nA = hm * A * (Ss.rho - phi * Sinf.rho);
  require_(nA > 0);
  const hfg = Ss.T >= 310 ? 2.41e6 : 2.44e6;
  const steps = [
    `${m("n_A = \\bar h_mA(\\rho_{A,s} - \\rho_{A,\\infty})")}: the surface vapor is saturated at ${m("T_s")}; the free stream holds ${m(`\\rho_{A,\\infty} = \\phi_\\infty\\rho_{A,sat}(T_\\infty) = ${phi}(${g(Sinf.rho)}) = ${fmt(phi * Sinf.rho, 4)}\\,\\mathrm{kg/m^3}`)}.`,
    m(`n_A = ${g(hm)}(${g(A)})(${g(Ss.rho)} - ${fmt(phi * Sinf.rho, 4)}) = ${fmt(nA, 4)}\\,\\mathrm{kg/s}`),
  ];
  const meta = { ht3: "evap", hm, A, rhoAs: Ss.rho, rhoAinf: Sinf.rho, phi, hfg, target };
  const pre = `A water surface of area ${m(`${g(A)}\\,\\mathrm{m^2}`)} at ${m(`${Ss.T}\\,\\mathrm{K}`)} is exposed to air at ${m(`${Sinf.T}\\,\\mathrm{K}`)} with relative humidity ${m(`${Math.round(phi * 100)}\\%`)}, and ${m(`\\bar h_m = ${vu(hm, "m/s")}`)}. Saturated vapor densities: ${m(`\\rho_{A,sat}(${Ss.T}\\,\\mathrm{K}) = ${g(Ss.rho)}`)}${Sinf.T !== Ss.T ? `, ${m(`\\rho_{A,sat}(${Sinf.T}\\,\\mathrm{K}) = ${g(Sinf.rho)}`)}` : ""} ${m("\\mathrm{kg/m^3}")}.`;
  if (target === "rate") return numeric(nA * 3600, "n_A", "n_A", "kg/h", [...steps, m(`n_A = ${fmt(nA, 4)} \\times 3600 = ${fmt(nA * 3600)}\\,\\mathrm{kg/h}`)], meta, `${pre} Find the evaporation rate in kg/h.`);
  return numeric(nA * hfg, "q_evap", "q_{evap}", "W", [...steps, m(`q_{evap} = n_Ah_{fg} = ${fmt(nA, 4)}(${g(hfg)}) = ${fmt(nA * hfg)}\\,\\mathrm{W}`)], meta,
    `${pre} With ${m(`h_{fg} = ${vu(hfg, "J/kg")}`)}, find the rate of heat loss by evaporation.`);
}

function mcSherwood(r: Rng): Draft {
  const geo = r.pick(["plate", "plate-rate", "sphere"] as const);
  const f = AIR300;
  if (geo === "sphere") {
    const Dmm = r.pick([0.5, 1, 2, 3]);
    const D = Dmm / 1000;
    const V = r.pick([0.5, 1, 2, 5]);
    const DAB = 0.26e-4;
    const Re = (V * D) / f.nu;
    const Sc = f.nu / DAB;
    const Sh = 2 + 0.6 * Math.sqrt(Re) * Sc ** (1 / 3);
    const hm = (Sh * DAB) / D;
    return numeric(hm, "h̄_m", "\\bar h_m", "m/s", [
      m(`Re_D = \\frac{VD}{\\nu} = ${fmt(Re, 4)}, \\quad Sc = \\frac{\\nu}{D_{AB}} = ${fmt(Sc, 4)}`),
      `Ranz–Marshall for a sphere (mass-transfer form of Eq 7.57): ${m(`\\bar{Sh}_D = 2 + 0.6Re_D^{1/2}Sc^{1/3} = ${fmt(Sh, 4)}`)}.`,
      m(`\\bar h_m = \\frac{\\bar{Sh}_DD_{AB}}{D} = \\frac{${fmt(Sh, 4)}(${g(DAB)})}{${g(D)}} = ${fmt(hm)}\\,\\mathrm{m/s}`),
    ], { ht3: "sherwood", geo, D, V, nu: f.nu, DAB },
    `A ${Dmm}-mm water droplet falls at ${eq("V", V, "m/s")} relative to air at 300 K (${fluidProps(f, ["nu"])}; water vapor–air ${m(`D_{AB} = ${vu(DAB, "m²/s")}`)}). Using ${m("\\bar{Sh}_D = 2 + 0.6Re_D^{1/2}Sc^{1/3}")}, find the average mass-transfer coefficient.`);
  }
  const sp = r.pick(SPECIES.slice(0, 2));
  const rhoAs = sp.name === "water vapor" ? 0.02556 : 6.7e-4;
  const V = r.pick([1, 2, 3, 5, 8, 10]);
  const L = r.pick([0.05, 0.1, 0.2, 0.3, 0.5]);
  const Re = (V * L) / f.nu;
  require_(Re < 5e5);
  const Sc = f.nu / sp.D;
  const Sh = 0.664 * Math.sqrt(Re) * Sc ** (1 / 3);
  const hm = (Sh * sp.D) / L;
  const steps = [
    m(`Re_L = \\frac{u_\\infty L}{\\nu} = ${fmt(Re, 4)} < 5\\times10^5, \\quad Sc = \\frac{\\nu}{D_{AB}} = \\frac{${g(f.nu)}}{${g(sp.D)}} = ${fmt(Sc, 4)}`),
    `Laminar plate, mass-transfer form: ${m(`\\bar{Sh}_L = 0.664Re_L^{1/2}Sc^{1/3} = ${fmt(Sh, 4)}`)}.`,
    m(`\\bar h_m = \\frac{\\bar{Sh}_LD_{AB}}{L} = ${fmt(hm, 4)}\\,\\mathrm{m/s}`),
  ];
  const W = r.pick([0.1, 0.2, 0.5]);
  const meta = { ht3: "sherwood", geo, L, V, nu: f.nu, DAB: sp.D, rhoAs, W };
  const pre = `Air at 300 K (${fluidProps(f, ["nu"])}) flows at ${eq("u_\\infty", V, "m/s")} over a ${g(L)}-m-long ${sp.name === "water vapor" ? "wetted plate at 300 K" : "plate coated with naphthalene at 300 K"} (${sp.name}–air ${m(`D_{AB} = ${vu(sp.D, "m²/s")}`)}).`;
  if (geo === "plate") return numeric(hm, "h̄_m", "\\bar h_m", "m/s", steps, meta, `${pre} Find the average mass-transfer coefficient ${m("\\bar h_m")}.`);
  const nA = hm * L * W * rhoAs;
  return numeric(nA, "n_A", "n_A", "kg/s", [...steps, m(`n_A = \\bar h_m(LW)(\\rho_{A,s} - 0) = ${fmt(hm, 4)}(${g(L)}\\times${g(W)})(${g(rhoAs)}) = ${fmt(nA)}\\,\\mathrm{kg/s}`)], meta,
    `${pre} The plate is ${g(W)} m wide, ${m(`\\rho_{A,sat} = ${vu(rhoAs, "kg/m³")}`)} at the surface, and the free stream carries none of the vapor. Find the ${sp.name === "water vapor" ? "evaporation" : "sublimation"} rate.`);
}

export const HEAT3_TEMPLATES: Record<string, (r: Rng) => Draft> = {
  "ht3-bl-transition": blTransition,
  "ht3-bl-average": blAverage,
  "ht3-bl-thickness": blThickness,
  "ht3-bl-colburn": blColburn,
  "ht3-bl-groups": blGroups,
  "ht3-tb-vmax": tbVmax,
  "ht3-tb-zukauskas": tbZukauskas,
  "ht3-tb-outlet": tbOutlet,
  "ht3-rohsenow": boilRohsenow,
  "ht3-chf": boilCHF,
  "ht3-boil-regime": boilRegime,
  "ht3-cond-plate": condPlate,
  "ht3-cond-tube": condTube,
  "ht3-wien": radWien,
  "ht3-stefan": radStefan,
  "ht3-band": radBand,
  "ht3-spectral": radSpectral,
  "ht3-rad-balance": radBalance,
  "ht3-fick": mdFick,
  "ht3-stefan-flow": mdStefan,
  "ht3-membrane": mdMembrane,
  "ht3-reaction": mdReaction,
  "ht3-mc-analogy": mcAnalogy,
  "ht3-mc-evap": mcEvap,
  "ht3-mc-sherwood": mcSherwood,
};
