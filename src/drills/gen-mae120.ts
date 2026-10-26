// Exam-style heat transfer drills modelled on UCI MAE 120 midterms (2020, 2021, 2026 practice):
// true/false concepts, "is this T(x,y,z) possible?", composite-wall reasoning, the
// finite-difference corner/edge node with Δx ≠ Δy, convection and radiation, and the
// recurring short answers (rod in a slab, two buried spheres, the pot on a stove).
// Numeric answers are checked to 1%; `meta` carries the inputs so tests/verify/mae120.py
// can rebuild each answer on its own.
import { Rng } from "./rng";
import type { Draft } from "./types";
import { m } from "./tex";
import { Reject, require_ } from "./reject";
import { fmt } from "./gen-heat";

const PI = Math.PI;
const g = (x: number) => fmt(x, 4);
const U: Record<string, string> = {
  W: "\\mathrm{W}",
  "W/m": "\\mathrm{W/m}",
  "°C": "^\\circ\\mathrm{C}",
  mm: "\\mathrm{mm}",
  "mm·K/W": "\\mathrm{mm\\cdot K/W}",
  "W/m²·K": "\\mathrm{W/m^2\\cdot K}",
};
const u = (unit: string) => `\\,${U[unit] ?? `\\mathrm{${unit}}`}`;

function numeric(val: number, label: string, labelTex: string, unit: string, steps: string[], meta: Record<string, unknown>, prompt: string): Draft {
  require_(Number.isFinite(val));
  return {
    prompt,
    answer: { kind: "expression", ref: `${val}`, vars: [], tol: 0.01, rel: true, label, unit },
    answerTex: `${labelTex} = ${fmt(val)}${u(unit)}`,
    steps,
    meta,
  };
}

function choice(options: string[], correct: string, steps: string[], meta: Record<string, unknown>, prompt: string): Draft {
  return { prompt, answer: { kind: "choice", options, correct }, answerTex: `\\text{${correct}}`, steps, meta };
}

/** Pick the answer first, then redraw until the inputs give it: keeps two-way questions 50/50. */
function balanced(r: Rng, make: (want: boolean) => Draft): Draft {
  const want = r.chance(0.5);
  for (let i = 0; i < 300; i++) {
    try {
      return make(want);
    } catch (e) {
      if (!(e instanceof Reject)) throw e;
    }
  }
  throw new Reject();
}

const TF = ["True", "False"];

// ═══ concepts: true / false ═════════════════════════════════════════════════
// [id, statement, true?, why]
const CONCEPTS: [string, string, boolean, string][] = [
  ["rad-medium", "Radiation heat transfer requires the presence of a medium to occur.", false, "Radiation is electromagnetic: it crosses a vacuum (sunlight reaches Earth). Conduction and convection need a medium."],
  ["k-direction", "Thermal conductivity $k$ is always independent of the direction of heat transfer in any material.", false, "Anisotropic materials (wood, composites, graphite, crystals) have direction-dependent $k$. Isotropic is an assumption, not a law."],
  ["fin-eff-1", "Adding a fin enhances heat transfer when the fin effectiveness $\\varepsilon_f$ is larger than 1.", true, "$\\varepsilon_f = q_f/(hA_{c,b}\\theta_b)$ compares the fin to the bare base. Above 1 the fin helps; designs usually aim for $\\varepsilon_f \\ge 2$."],
  ["fin-eta", "A fin's efficiency $\\eta_f$ can exceed 1 if the fin is very conductive.", false, "$\\eta_f = q_f/q_{max}$, where $q_{max}$ assumes the whole fin is at the base temperature. It is at most 1."],
  ["fin-linear", "Along a straight fin with convection, the temperature excess decays linearly from base to tip.", false, "Convection off the sides makes $\\theta'' = m^2\\theta$: the profile is $\\cosh/\\sinh$ (exponential-like), not linear."],
  ["wall-linear", "In 1-D steady conduction through a plane wall with constant $k$ and no generation, $T(x)$ is linear.", true, "$d^2T/dx^2 = 0$ gives $T = C_1x + C_2$."],
  ["cyl-linear", "In 1-D steady radial conduction through a cylindrical wall (constant $k$, no generation), $T(r)$ is linear in $r$.", false, "$\\frac{1}{r}\\frac{d}{dr}(r\\,dT/dr) = 0$ gives $T = C_1\\ln r + C_2$: logarithmic."],
  ["q-const-cyl", "In steady radial conduction through a pipe wall without generation, the heat rate $q_r$ is the same at every radius.", true, "Energy conservation: what enters at $r_1$ leaves at $r_2$. The flux $q''_r = q_r/2\\pi rL$ falls with $r$, but $q_r$ is constant."],
  ["flux-const-cyl", "In steady radial conduction through a pipe wall without generation, the heat flux $q''_r$ is the same at every radius.", false, "The rate $q_r$ is constant; the area $2\\pi rL$ grows, so the flux $q''_r$ falls as $1/r$."],
  ["insulation-always", "Adding insulation to a small-diameter wire always reduces its heat loss.", false, "Below the critical radius $r_{cr} = k/h$, added insulation grows the convection area faster than it adds resistance: heat loss goes up."],
  ["tau-large", "In transient conduction, a large thermal time constant $\\tau_t = \\rho Vc/hA_s$ means the temperature difference $\\theta/\\theta_i$ decays slowly.", true, "$\\theta/\\theta_i = e^{-t/\\tau_t}$: a bigger $\\tau_t$ is slower decay."],
  ["bi-small", "The lumped capacitance method is valid when the Biot number is small ($Bi < 0.1$), meaning internal conduction resistance is small compared with surface convection resistance.", true, "$Bi = hL_c/k = R_{cond}/R_{conv}$. Small $Bi$: the solid is nearly isothermal."],
  ["bi-large", "A large Biot number means the solid's temperature is nearly uniform during cooling.", false, "Large $Bi$ means the internal conduction resistance dominates: big gradients inside. Uniform temperature needs small $Bi$."],
  ["lc-sphere", "For a sphere of diameter $D$, the lumped-capacitance characteristic length is $L_c = V/A_s = D/6$.", true, "$V/A_s = (\\pi D^3/6)/(\\pi D^2) = D/6$."],
  ["shape-k", "In a conduction shape-factor problem $q = Sk\\Delta T_{1-2}$, $k$ is the conductivity of the medium between the two surfaces.", true, "The shape factor models conduction through the surrounding medium; the buried objects are isothermal surfaces, their own $k$ does not enter."],
  ["series-same-q", "In 1-D steady conduction through layers in series (no generation), every layer carries the same heat rate.", true, "Nothing is stored or generated, so the same $q$ crosses every layer; the biggest resistance takes the biggest $\\Delta T$."],
  ["biggest-drop", "Across a composite wall in series, the layer with the smallest thermal resistance has the largest temperature drop.", false, "$\\Delta T_i = qR_i$ with the same $q$: the largest resistance has the largest drop."],
  ["steady-zero-storage", "At steady state, the energy stored in a control volume is changing at a constant nonzero rate.", false, "Steady state means $\\dot E_{st} = 0$: in + generated = out."],
  ["laplace-cond", "Steady conduction with constant $k$ and no generation requires $\\nabla^2 T = 0$ everywhere in the solid.", true, "The heat equation reduces to Laplace's equation when $\\partial T/\\partial t = 0$, $\\dot q = 0$, $k$ constant."],
  ["fd-interior", "For an interior node with $\\Delta x = \\Delta y$ and no generation, the finite-difference equation says the node temperature is the average of its four neighbours.", true, "$T_{m+1,n} + T_{m-1,n} + T_{m,n+1} + T_{m,n-1} - 4T_{m,n} = 0$."],
];

function concept(r: Rng): Draft {
  const want = r.chance(0.5);
  const pool = CONCEPTS.filter((c) => c[2] === want);
  const [id, text, truth, why] = r.pick(pool);
  return choice(TF, truth ? "True" : "False", [why], { mae: "concept", id, truth }, `True or false? ${text}`);
}

// ═══ is this temperature field possible? ∇²T = 0 ═══════════════════════════
function poly(terms: [number, string][]): string {
  const parts = terms.filter(([c]) => c !== 0);
  let s = "";
  parts.forEach(([c, body], i) => {
    const a = Math.abs(c);
    const t = `${a === 1 ? "" : a}${body}`;
    s += i === 0 ? (c < 0 ? `-${t}` : t) : c < 0 ? ` - ${t}` : ` + ${t}`;
  });
  return s;
}

const laplaceCheck = (r: Rng) =>
  balanced(r, (possible) => {
    const coord = r.chance(0.65) ? "cart" : "cyl";
    if (coord === "cart") {
      const a = r.nz(-9, 9), b = r.nz(-9, 9);
      let c = -(a + b);
      if (!possible) c += r.pick([-4, -3, -2, -1, 1, 2, 3, 4]);
      require_(c !== 0);
      const cross = ([[r.int(-8, 8), "xy"], [r.int(-8, 8), "yz"], [r.int(-8, 8), "xz"]] as [number, string][]).filter(() => r.chance(0.6));
      const lap = 2 * (a + b + c);
      const T = poly([[a, "x^2"], [b, "y^2"], [c, "z^2"], ...cross]);
      return choice(["Possible", "Not possible"], lap === 0 ? "Possible" : "Not possible", [
        `Steady, no generation, constant ${m("k")}: the field must satisfy ${m("\\nabla^2 T = \\partial^2T/\\partial x^2 + \\partial^2T/\\partial y^2 + \\partial^2T/\\partial z^2 = 0")}.`,
        `Cross terms like ${m("xy")} have zero second derivatives. Only the squares count: ${m(`2(${a}) + 2(${b}) + 2(${c}) = ${lap}`)}.`,
        lap === 0 ? "Zero: possible." : `${lap} ≠ 0: not possible.`,
      ], { mae: "laplace", coord, a, b, c, cross },
      `Assuming steady conduction with no internal heat generation and constant properties, is this temperature field in an infinite solid physically possible? ${m(`T(x,y,z) = ${T}`)}`);
    }
    // cylindrical: T = A r² + B z² + C rz + D ln r ;  ∇²(r²) = 4, ∇²(z²) = 2, ∇²(rz) = z/r, ∇²(ln r) = 0
    const A = r.nz(-9, 9);
    let B = -2 * A;
    let C = 0;
    if (!possible) {
      if (r.chance(0.5)) C = r.nz(-9, 9);
      else B += r.pick([-3, -2, -1, 1, 2, 3]);
    }
    require_(B !== 0);
    const D = r.chance(0.5) ? r.nz(-5, 5) : 0;
    const lapConst = 4 * A + 2 * B;
    const ok = lapConst === 0 && C === 0;
    const T = poly([[A, "r^2"], [B, "z^2"], [C, "rz"], [D, "\\ln r"]]);
    return choice(["Possible", "Not possible"], ok ? "Possible" : "Not possible", [
      `Cylindrical Laplacian: ${m("\\nabla^2T = \\frac{1}{r}\\frac{\\partial}{\\partial r}\\left(r\\frac{\\partial T}{\\partial r}\\right) + \\frac{1}{r^2}\\frac{\\partial^2T}{\\partial\\phi^2} + \\frac{\\partial^2T}{\\partial z^2}")}.`,
      `Term by term: ${m("\\nabla^2(r^2) = 4")}, ${m("\\nabla^2(z^2) = 2")}, ${m("\\nabla^2(rz) = z/r")}, ${m("\\nabla^2(\\ln r) = 0")}.`,
      `${m(`\\nabla^2 T = 4(${A}) + 2(${B})${C ? ` + ${C}\\,z/r` : ""} = ${lapConst}${C ? ` + ${C}z/r` : ""}`)}: ${ok ? "zero everywhere, possible." : "not zero everywhere, not possible."}`,
    ], { mae: "laplace", coord, A, B, C, D },
    `Assuming steady conduction with no internal heat generation and constant properties, is this temperature field physically possible? ${m(`T(r,\\phi,z) = ${T}`)}`);
  });

// ═══ composite walls: reasoning ═════════════════════════════════════════════
const wallCompare = (r: Rng) =>
  balanced(r, (truth) => {
    const T1 = r.pick([200, 180, 150, 120, 100]);
    const d1 = r.pick([10, 20, 30, 40, 50, 60]);
    const d2 = r.pick([10, 20, 30, 40, 50, 60]);
    require_(d1 !== d2);
    const T2 = T1 - d1, T3 = T2 - d2;
    const claim = r.pick(["R1>R2", "R1<R2", "k1>k2", "k1<k2"] as const);
    // same q, ΔT = qR  ⇒ R1/R2 = d1/d2 ; equal L and A ⇒ R ∝ 1/k
    const holds = { "R1>R2": d1 > d2, "R1<R2": d1 < d2, "k1>k2": d1 < d2, "k1<k2": d1 > d2 }[claim];
    require_(holds === truth);
    const claimTex = { "R1>R2": "R_{t,1} > R_{t,2}", "R1<R2": "R_{t,1} < R_{t,2}", "k1>k2": "k_1 > k_2", "k1<k2": "k_1 < k_2" }[claim];
    return choice(TF, truth ? "True" : "False", [
      `1-D steady, no generation: the same ${m("q")} crosses both layers, so ${m("\\Delta T_i = qR_{t,i}")}.`,
      `${m(`\\Delta T_1 = ${d1}`)}, ${m(`\\Delta T_2 = ${d2}`)}, so ${m(d1 > d2 ? "R_{t,1} > R_{t,2}" : "R_{t,1} < R_{t,2}")}.`,
      `Equal thickness and area: ${m("R_t = L/kA")}, so the larger resistance has the smaller ${m("k")}: ${m(d1 > d2 ? "k_1 < k_2" : "k_1 > k_2")}.`,
    ], { mae: "wall-compare", d1, d2, claim },
    `A composite wall of materials 1 and 2 (${m("L_1 = L_2")}, same area) carries 1-D steady conduction. The outer faces and the interface are at ${m(`T_1 = ${T1}`)}, ${m(`T_2 = ${T2}`)}, ${m(`T_3 = ${T3}\\,^\\circ\\mathrm{C}`)}. True or false: ${m(claimTex)}.`);
  });

// A | (B over C) | D, identical blocks; A and D span the full height, B and C half each
const SP_CLAIMS: [string, string][] = [
  ["fA>fB", "q''_A > q''_B"],
  ["fB>fA", "q''_B > q''_A"],
  ["qB>qC", "q_B > q_C"],
  ["qC>qB", "q_C > q_B"],
  ["fC>fD", "q''_C > q''_D"],
  ["fD>fC", "q''_D > q''_C"],
  ["qA>qD", "q_A > q_D"],
  ["qA=qD", "q_A = q_D"],
  ["fB>fD", "q''_B > q''_D"],
  ["fA=fD", "q''_A = q''_D"],
];
// truth for kA > kB > kC > kD (fluxes: A and D span 2h, B and C span h; q_A = q_D = q_B + q_C, q_B > q_C)
const SP_TRUTH: Record<string, boolean> = {
  "fA>fB": false, "fB>fA": true, "qB>qC": true, "qC>qB": false, "fC>fD": false, "fD>fC": true,
  "qA>qD": false, "qA=qD": true, "fB>fD": true, "fA=fD": true,
};
const seriesParallel = (r: Rng) =>
  balanced(r, (truth) => {
    const [id, tex] = r.pick(SP_CLAIMS);
    require_(SP_TRUTH[id] === truth);
    return choice(TF, truth ? "True" : "False", [
      `A and D are in series with the parallel pair B ∥ C, so all the heat through A goes through D: ${m("q_A = q_B + q_C = q_D")}.`,
      `B and C see the same ${m("\\Delta T")} with the same size; ${m("k_B > k_C")} gives ${m("q_B > q_C")}.`,
      `Fluxes: A and D span the full height ${m("2h")}, B and C span ${m("h")}. ${m("q''_A = q''_D = (q_B + q_C)/2h")}, which lies between ${m("q''_C = q_C/h")} and ${m("q''_B = q_B/h")}.`,
    ], { mae: "series-parallel", id },
    `A composite wall: block A, then blocks B (top) and C (bottom) side by side, then block D. All four blocks are identical in size; A and D each span the full height, B and C each span half of it. With 1-D steady conduction, no generation or contact resistance, and ${m("k_A > k_B > k_C > k_D")}: true or false, ${m(tex)}? (${m("q_X")} is the rate through X, ${m("q''_X")} the flux through it.)`);
  });

// ═══ temperature at a point in a layer ═════════════════════════════════════
function wallPoint(r: Rng): Draft {
  const T1 = r.pick([150, 200, 250, 300, 400]);
  const T2 = T1 - r.pick([20, 40, 50, 60, 80, 100]);
  const T3 = T2 - r.pick([20, 30, 50, 70, 90]);
  const layer = r.pick([1, 2]);
  const f = r.pick([1 / 4, 1 / 2, 3 / 4, 1 / 3, 2 / 3]);
  const fTex = { 0.25: "1/4", 0.5: "1/2", 0.75: "3/4" }[f] ?? (f < 0.5 ? "1/3" : "2/3");
  const [Ta, Tb] = layer === 1 ? [T1, T2] : [T2, T3];
  const T = Ta + f * (Tb - Ta);
  return numeric(T, "T", "T", "°C", [
    `1-D steady, no generation, constant ${m("k")}: within each layer ${m("T(x)")} is a straight line between that layer's face temperatures.`,
    m(`T = T_${layer === 1 ? 1 : 2} + \\tfrac{x'}{L_${layer}}(T_${layer === 1 ? 2 : 3} - T_${layer === 1 ? 1 : 2}) = ${Ta} + ${fTex}(${Tb} - ${Ta}) = ${fmt(T)}${u("°C")}`),
  ], { mae: "wall-point", Ta, Tb, f },
  `A two-layer wall (material 1 then 2) has its outer faces at ${m(`T_1 = ${T1}`)} and ${m(`T_3 = ${T3}\\,^\\circ\\mathrm{C}`)} and its interface at ${m(`T_2 = ${T2}\\,^\\circ\\mathrm{C}`)} (1-D steady, no generation). Find the temperature ${m(`${fTex}`)} of the way through layer ${layer}, measured from ${layer === 1 ? "the outer face at " + m("T_1") : "the interface"}.`);
}

// ═══ short answers that keep coming back ═══════════════════════════════════
// rod centred between two isothermal planes (Table 4.1 case 5): S' = 2π / ln(8z/πD)
function rodSlab(r: Rng): Draft {
  const Dmm = r.pick([20, 25, 40, 50, 60, 80, 100]);
  const D = Dmm / 1000;
  const k = r.pick([0.2, 0.5, 1, 1.5, 2]);
  const variant = r.pick(["R", "q", "y"] as const);
  const Ts = r.pick([15, 20, 25]);
  const Trod = Ts + r.pick([40, 50, 65, 80, 100]);
  if (variant === "y") {
    // build backward: pick y, find q̇, round q̇, recompute y
    const y0 = r.pick([0.1, 0.15, 0.2, 0.3, 0.5, 0.8, 1]);
    const R0 = Math.log((8 * y0) / (PI * D)) / (2 * PI * k);
    const qdot = Number((((Trod - Ts) / R0) / ((PI * D * D) / 4)).toPrecision(2));
    const qp = (qdot * PI * D * D) / 4;
    const R = (Trod - Ts) / qp;
    const y = (Math.exp(2 * PI * k * R) * PI * D) / 8;
    require_(y > 2 * D);
    return numeric(y * 1000, "y", "y", "mm", [
      `All the heat generated in the rod leaves through the slab: ${m(`q' = \\dot q\\,\\pi D^2/4 = ${fmt(qdot)}\\times\\pi(${g(D)})^2/4 = ${fmt(qp)}\\,\\mathrm{W/m}`)}.`,
      `Required resistance per length: ${m(`R'_t = \\Delta T/q' = ${Trod - Ts}/${fmt(qp)} = ${fmt(R, 4)}\\,\\mathrm{m\\cdot K/W}`)}.`,
      `Table 4.1 case 5 (cylinder midway between parallel planes, ${m("z = y")}): ${m("R'_t = \\frac{\\ln(8z/\\pi D)}{2\\pi k}")}, so ${m(`y = \\frac{\\pi D}{8}e^{2\\pi kR'_t} = ${fmt(y * 1000)}${u("mm")}`)}.`,
    ], { mae: "rod-slab", variant, D, k, qdot, dT: Trod - Ts },
    `A long rod, ${m(`D = ${Dmm}\\,\\mathrm{mm}`)}, with uniform generation ${m(`\\dot q = ${fmt(qdot)}\\,\\mathrm{W/m^3}`)}, is centred in a very wide slab (${m(`k = ${k}\\,\\mathrm{W/m\\cdot K}`)}) whose two faces are each a distance ${m("y")} from the rod's axis and held at ${m(`${Ts}\\,^\\circ\\mathrm{C}`)}. The rod surface stays at ${m(`${Trod}\\,^\\circ\\mathrm{C}`)} at steady state. Find ${m("y")} in mm.`);
  }
  const y = r.pick([0.1, 0.2, 0.25, 0.5, 1, 2]);
  require_(y > 2 * D);
  const R = Math.log((8 * y) / (PI * D)) / (2 * PI * k);
  const sTex = `R'_t = \\frac{\\ln(8z/\\pi D)}{2\\pi k} = \\frac{\\ln(8(${g(y)})/\\pi(${g(D)}))}{2\\pi(${k})} = ${fmt(R, 4)}\\,\\mathrm{m\\cdot K/W}`;
  const setup = `A long rod, ${m(`D = ${Dmm}\\,\\mathrm{mm}`)}, is centred in a very wide slab (${m(`k = ${k}\\,\\mathrm{W/m\\cdot K}`)}) whose two faces are each ${m(`y = ${g(y)}\\,\\mathrm{m}`)} from the rod's axis.`;
  if (variant === "R")
    return numeric(R * 1000, "R′", "R'_t", "mm·K/W", [
      `Table 4.1 case 5, cylinder midway between parallel planes, ${m("z = y")}: ${m("S' = 2\\pi/\\ln(8z/\\pi D)")} per unit length, and ${m("R'_t = 1/(S'k)")}.`,
      m(sTex),
      `In the units asked: ${m(`${fmt(R * 1000)}${u("mm·K/W")}`)} (multiply m by 1000).`,
    ], { mae: "rod-slab", variant, D, k, y }, `${setup} Find the conduction resistance per unit length between the rod surface and the slab faces, in mm·K/W.`);
  const q = (Trod - Ts) / R;
  return numeric(q, "q′", "q'", "W/m", [
    `Table 4.1 case 5: ${m(sTex)}.`,
    m(`q' = \\frac{T_{rod} - T_s}{R'_t} = \\frac{${Trod} - ${Ts}}{${fmt(R, 4)}} = ${fmt(q)}${u("W/m")}`),
  ], { mae: "rod-slab", variant, D, k, y, dT: Trod - Ts },
  `${setup} The rod surface is at ${m(`${Trod}\\,^\\circ\\mathrm{C}`)} and the slab faces at ${m(`${Ts}\\,^\\circ\\mathrm{C}`)}. Find the heat loss per unit length of rod.`);
}

// two isothermal spheres in a large medium: by symmetry the midplane is isothermal at the mean,
// so each sphere is "Case 1, sphere buried in a semi-infinite medium" with z = centre-to-midplane
function twoSpheres(r: Rng): Draft {
  const Dnm = r.pick([100, 200, 300, 400, 500]);
  const gapNm = r.pick([1, 1.5, 2, 3]) * Dnm;
  const k = r.pick([50, 100, 200, 500, 1000]);
  const T1 = r.pick([400, 500, 600]);
  const T2 = r.pick([100, 200, 300]);
  const D = Dnm * 1e-9;
  const z = D / 2 + (gapNm * 1e-9) / 2;
  const S = (2 * PI * D) / (1 - D / (4 * z));
  const Tm = (T1 + T2) / 2;
  const q = S * k * (T1 - Tm);
  return numeric(q, "q", "q", "W", [
    `Symmetry: the plane halfway between the spheres is isothermal at ${m(`(T_1 + T_2)/2 = ${Tm}\\,\\mathrm{K}`)}. Each sphere then looks like Table 4.1 case 1, a sphere buried a depth ${m("z")} below an isothermal surface.`,
    `${m("z")} is centre to midplane: ${m(`z = D/2 + \\text{gap}/2 = ${Dnm / 2} + ${gapNm / 2} = ${Dnm / 2 + gapNm / 2}\\,\\mathrm{nm}`)}.`,
    m(`S = \\frac{2\\pi D}{1 - D/4z} = \\frac{2\\pi(${g(D)})}{1 - ${Dnm}/${4 * (Dnm / 2 + gapNm / 2)}} = ${fmt(S)}\\,\\mathrm{m}`),
    `${m(`q = Sk(T_1 - T_{mid}) = ${fmt(S)}\\times${k}\\times${T1 - Tm} = ${fmt(q)}${u("W")}`)}. Use the medium's ${m("k")}, not the particles'. (Equivalently, two equal resistances ${m("1/Sk")} in series across the full ${m("T_1 - T_2")}.)`,
  ], { mae: "two-spheres", D, z, k, T1, T2 },
  `Two spherical nanoparticles, ${m(`D = ${Dnm}\\,\\mathrm{nm}`)}, sit in a very large solid of conductivity ${m(`${k}\\,\\mathrm{W/m\\cdot K}`)} with a ${m(`${gapNm}\\,\\mathrm{nm}`)} gap between their surfaces. Their surfaces are held at ${m(`${T1}\\,\\mathrm{K}`)} and ${m(`${T2}\\,\\mathrm{K}`)}. Ignoring convection and radiation, find the heat rate between them.`);
}

// the pot: flux q'' in at y = 0, convection to boiling water at y = L
function pot(r: Rng): Draft {
  const qcm = r.pick([5, 10, 20, 50, 100]); // W/cm²
  const qf = qcm * 1e4;
  const Lmm = r.pick([2, 3, 4, 5, 6]);
  const L = Lmm / 1000;
  const k = r.pick([15, 60, 180, 240, 400]);
  const Tinf = 100;
  const variant = r.pick(["T0", "TL", "T0fromTL", "h"] as const);
  if (variant === "T0fromTL" || variant === "h") {
    const TL = Tinf + r.pick([2, 3, 5, 8, 10]);
    const T0 = TL + (qf * L) / k;
    if (variant === "h") {
      const h = qf / (TL - Tinf);
      return numeric(h, "h", "h", "W/m²·K", [
        `Steady, so the flux entering at the bottom leaves into the water: ${m("q'' = h[T(L) - T_\\infty]")}.`,
        m(`h = \\frac{q''}{T(L) - T_\\infty} = \\frac{${fmt(qf)}}{${TL} - ${Tinf}} = ${fmt(h)}\\,\\mathrm{W/m^2\\cdot K}`),
      ], { mae: "pot", variant, qf, L, k, TL, Tinf }, `A pot bottom (${m(`L = ${Lmm}\\,\\mathrm{mm}`)}, ${m(`k = ${k}\\,\\mathrm{W/m\\cdot K}`)}) is heated from below with ${m(`q'' = ${qcm}\\,\\mathrm{W/cm^2}`)}. Water boils above it at ${m(`T_\\infty = ${Tinf}\\,^\\circ\\mathrm{C}`)}, and the inner surface is at ${m(`T(L) = ${TL}\\,^\\circ\\mathrm{C}`)} at steady state. Find the boiling heat transfer coefficient ${m("h")}.`);
    }
    return numeric(T0, "T(0)", "T(0)", "°C", [
      `1-D steady, no generation: ${m("d^2T/dy^2 = 0")}, so ${m("T")} is linear. BCs: ${m("-k\\,dT/dy|_0 = q''")} and ${m(`T(L) = ${TL}`)}.`,
      `So ${m("dT/dy = -q''/k")} everywhere and ${m("T(y) = T(L) + \\frac{q''}{k}(L - y)")}.`,
      m(`T(0) = ${TL} + \\frac{${fmt(qf)}\\times${g(L)}}{${k}} = ${fmt(T0)}${u("°C")}`),
    ], { mae: "pot", variant, qf, L, k, TL, Tinf }, `A pot bottom (${m(`L = ${Lmm}\\,\\mathrm{mm}`)}, ${m(`k = ${k}\\,\\mathrm{W/m\\cdot K}`)}) is heated from below with ${m(`q'' = ${qcm}\\,\\mathrm{W/cm^2}`)} (convert to W/m²). At steady boiling the surface touching the water is at ${m(`T(L) = ${TL}\\,^\\circ\\mathrm{C}`)}. Find the temperature of the bottom face, ${m("T(0)")}.`);
  }
  const h = r.pick([5000, 10000, 20000, 50000]);
  const TL = Tinf + qf / h;
  require_(TL - Tinf < 60);
  const T0 = TL + (qf * L) / k;
  const ask0 = variant === "T0";
  return numeric(ask0 ? T0 : TL, ask0 ? "T(0)" : "T(L)", ask0 ? "T(0)" : "T(L)", "°C", [
    `BCs: ${m("-k\\,dT/dy|_0 = q''")} (flux in) and ${m("-k\\,dT/dy|_L = h[T(L) - T_\\infty]")} (convection out). Steady and 1-D: the same ${m("q''")} crosses the whole layer.`,
    `${m(`T(y) = T_\\infty + \\frac{q''}{h} + \\frac{q''}{k}(L - y)`)}, a straight line with slope ${m("-q''/k")}.`,
    m(`T(L) = ${Tinf} + \\frac{${fmt(qf)}}{${fmt(h)}} = ${fmt(TL)}${u("°C")}`),
    ...(ask0 ? [m(`T(0) = T(L) + \\frac{q''L}{k} = ${fmt(TL)} + \\frac{${fmt(qf)}\\times${g(L)}}{${k}} = ${fmt(T0)}${u("°C")}`)] : []),
  ], { mae: "pot", variant, qf, L, k, h, Tinf },
  `A pot bottom (${m(`L = ${Lmm}\\,\\mathrm{mm}`)}, ${m(`k = ${k}\\,\\mathrm{W/m\\cdot K}`)}) is heated from below with ${m(`q'' = ${qcm}\\,\\mathrm{W/cm^2}`)}. Boiling water above it is at ${m(`T_\\infty = ${Tinf}\\,^\\circ\\mathrm{C}`)} with ${m(`h = ${fmt(h)}\\,\\mathrm{W/m^2\\cdot K}`)}. At steady state, find ${ask0 ? "the bottom-face temperature " + m("T(0)") : "the inner-surface temperature " + m("T(L)")}.`);
}

// ═══ finite-difference nodes like the exam: Δx = aΔy, convection, radiation, insulation ═══
type Face = { kind: "cond"; T: number; len: number; dist: number } | { kind: "conv"; len: number } | { kind: "ins" };

function fdExam(r: Rng): Draft {
  const a = r.pick([1, 2, 4, 4, 0.5]); // Δx = a Δy
  const dyCm = r.pick([1, 2]);
  const dy = dyCm / 100;
  const dx = a * dy;
  const k = r.pick([5, 15, 25, 50]);
  const h = r.pick([25, 50, 100, 200]);
  const Tinf = r.pick([20, 25, 30]);
  const rad = r.chance(0.5);
  const hr = rad ? r.pick([5, 8, 10, 15]) : 0;
  const Tsur = rad ? r.pick([20, 40, 60]) : 0;
  const type = r.pick(["corner", "top", "side", "corner-ins"] as const);
  const T = () => r.pick([60, 70, 80, 90, 100, 110, 120, 140]);
  // per unit depth: conduction conductance = k·(face length)/(centre distance); exposed: (h + hr)·length
  let faces: { name: string; f: Face }[];
  let where: string;
  if (type === "corner") {
    where = "an external corner: exposed to the fluid on its top face and its right face";
    faces = [
      { name: "left", f: { kind: "cond", T: T(), len: dy / 2, dist: dx } },
      { name: "below", f: { kind: "cond", T: T(), len: dx / 2, dist: dy } },
      { name: "top", f: { kind: "conv", len: dx / 2 } },
      { name: "right", f: { kind: "conv", len: dy / 2 } },
    ];
  } else if (type === "corner-ins") {
    where = "a corner whose top face is insulated and whose right face is exposed to the fluid";
    faces = [
      { name: "left", f: { kind: "cond", T: T(), len: dy / 2, dist: dx } },
      { name: "below", f: { kind: "cond", T: T(), len: dx / 2, dist: dy } },
      { name: "top", f: { kind: "ins" } },
      { name: "right", f: { kind: "conv", len: dy / 2 } },
    ];
  } else if (type === "top") {
    where = "the top surface (a horizontal boundary) exposed to the fluid";
    faces = [
      { name: "left", f: { kind: "cond", T: T(), len: dy / 2, dist: dx } },
      { name: "right", f: { kind: "cond", T: T(), len: dy / 2, dist: dx } },
      { name: "below", f: { kind: "cond", T: T(), len: dx, dist: dy } },
      { name: "top", f: { kind: "conv", len: dx } },
    ];
  } else {
    where = "the right surface (a vertical boundary) exposed to the fluid";
    faces = [
      { name: "left", f: { kind: "cond", T: T(), len: dy, dist: dx } },
      { name: "above", f: { kind: "cond", T: T(), len: dx / 2, dist: dy } },
      { name: "below", f: { kind: "cond", T: T(), len: dx / 2, dist: dy } },
      { name: "right", f: { kind: "conv", len: dy } },
    ];
  }
  let G = 0, GT = 0;
  for (const { f } of faces) {
    if (f.kind === "cond") {
      const c = (k * f.len) / f.dist;
      G += c;
      GT += c * f.T;
    } else if (f.kind === "conv") {
      G += (h + hr) * f.len;
      GT += h * f.len * Tinf + hr * f.len * Tsur;
    }
  }
  const Tn = GT / G;
  const aTex = a === 1 ? "\\Delta x = \\Delta y" : a === 0.5 ? "\\Delta y = 2\\Delta x" : `\\Delta x = ${a}\\Delta y`;
  const nb = faces.filter((x) => x.f.kind === "cond").map((x) => `${x.name} ${m(`${(x.f as any).T}\\,^\\circ\\mathrm{C}`)}`).join(", ");
  const termTex = faces
    .map(({ name, f }) => {
      if (f.kind === "cond") {
        const lenTex = f.len === dx ? "\\Delta x" : f.len === dy ? "\\Delta y" : f.len === dx / 2 ? "\\frac{\\Delta x}{2}" : "\\frac{\\Delta y}{2}";
        const distTex = f.dist === dx ? "\\Delta x" : "\\Delta y";
        return `k\\,${lenTex}\\,\\frac{T_{${name}} - T_n}{${distTex}}`;
      }
      if (f.kind === "conv") {
        const lenTex = f.len === dx ? "\\Delta x" : f.len === dy ? "\\Delta y" : f.len === dx / 2 ? "\\frac{\\Delta x}{2}" : "\\frac{\\Delta y}{2}";
        return `h\\,${lenTex}(T_\\infty - T_n)${rad ? ` + h_r\\,${lenTex}(T_{sur} - T_n)` : ""}`;
      }
      return "";
    })
    .filter(Boolean)
    .join(" + ");
  return numeric(Tn, "T_n", "T_n", "°C", [
    `Draw the node's control volume: ${type.startsWith("corner") ? "a quarter cell" : "a half cell"}, ${m(`${type === "side" ? "\\Delta x/2 \\times \\Delta y" : type === "top" ? "\\Delta x \\times \\Delta y/2" : "\\Delta x/2 \\times \\Delta y/2"}`)}. Each conduction path's area is the face it crosses (per unit depth); its length is the distance to that neighbour.`,
    `Energy balance, all heat flows assumed into the node: ${m(`${termTex} = 0`)}${type === "corner-ins" ? " (the insulated top contributes nothing)" : ""}.`,
    `With ${m(`${aTex}`)}, ${m(`\\Delta y = ${g(dy)}`)}, ${m(`\\Delta x = ${g(dx)}\\,\\mathrm{m}`)}: each term is a conductance times a temperature difference. ${m(`T_n = \\frac{\\sum G_iT_i}{\\sum G_i} = \\frac{${fmt(GT, 4)}}{${fmt(G, 4)}} = ${fmt(Tn)}${u("°C")}`)}.`,
  ], { mae: "fd", faces: faces.map(({ f }) => f), k, h, Tinf, hr, Tsur },
  `A 2-D steady finite-difference node (no generation, ${m(`k = ${k}\\,\\mathrm{W/m\\cdot K}`)}, grid ${m(aTex)} with ${m(`\\Delta y = ${dyCm}\\,\\mathrm{cm}`)}) sits on ${where}. The fluid is at ${m(`T_\\infty = ${Tinf}\\,^\\circ\\mathrm{C}`)}, ${m(`h = ${h}\\,\\mathrm{W/m^2\\cdot K}`)}${rad ? `; radiation to surroundings at ${m(`T_{sur} = ${Tsur}\\,^\\circ\\mathrm{C}`)} is linearised with ${m(`h_r = ${hr}\\,\\mathrm{W/m^2\\cdot K}`)}` : "; neglect radiation"}. Neighbouring nodes: ${nb}. Find the node temperature ${m("T_n")}.`);
}

export const MAE120_TEMPLATES: Record<string, (r: Rng) => Draft> = {
  "mae-concept": concept,
  "mae-laplace": laplaceCheck,
  "mae-wall-compare": wallCompare,
  "mae-series-parallel": seriesParallel,
  "mae-wall-point": wallPoint,
  "mae-rod-slab": rodSlab,
  "mae-two-spheres": twoSpheres,
  "mae-pot": pot,
  "mae-fd": fdExam,
};
