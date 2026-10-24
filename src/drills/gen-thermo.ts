// Classical thermodynamics, Level 1 (Dill & Bromberg; Shell 2015).
// Symbolic answers are expressions in the state variables (checked numerically at
// sample points); numeric answers are checked to 1%. Every problem carries its
// inputs in SI in `meta` (with a `th` case name) so tests/verify/thermo.py can
// rebuild the answer from first principles: differentiate the fundamental equation,
// integrate P dV, do the Legendre transform, solve the equilibrium condition.
import { Rng } from "./rng";
import type { Draft } from "./types";
import { m } from "./tex";
import { Q } from "./rational";
import { require_ } from "./reject";
import { fmt } from "./gen-heat";

const R = 8.314;
/** a given value as written in a prompt */
const g = (x: number) => fmt(x, 4);
/** round to what the prompt shows, so answers use exactly the given numbers */
const r4 = (x: number) => Number(x.toPrecision(4));
const r3 = (x: number) => Number(x.toPrecision(3));

const UNITS: Record<string, string> = {
  J: "\\mathrm{J}",
  kJ: "\\mathrm{kJ}",
  "J/mol": "\\mathrm{J/mol}",
  "kJ/mol": "\\mathrm{kJ/mol}",
  "J/K": "\\mathrm{J/K}",
  "J/(mol·K)": "\\mathrm{J/(mol\\cdot K)}",
  K: "\\mathrm{K}",
  Pa: "\\mathrm{Pa}",
  kPa: "\\mathrm{kPa}",
  bar: "\\mathrm{bar}",
  "Pa/K": "\\mathrm{Pa/K}",
  "Pa⁻¹": "\\mathrm{Pa^{-1}}",
  "K⁻¹": "\\mathrm{K^{-1}}",
  "m³": "\\mathrm{m^3}",
  "m³/mol": "\\mathrm{m^3/mol}",
  "m³/(mol·K)": "\\mathrm{m^3/(mol\\cdot K)}",
  L: "\\mathrm{L}",
  mol: "\\mathrm{mol}",
  "": "",
};
const u = (unit: string) => (unit ? `\\,${UNITS[unit] ?? `\\mathrm{${unit}}`}` : "");
const vu = (x: number, unit: string) => `${g(x)}${u(unit)}`;
/** temperatures like 373.15 K keep all their digits */
const gT = (x: number) => fmt(x, 5);

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
    answer: { kind: "expression", ref: `${val}`, vars: [], tol: 0.01, rel: true, label, ...(unit ? { unit } : {}) },
    answerTex: `${labelTex} = ${fmt(val)}${u(unit)}`,
    steps,
    meta,
  };
}

function symbolic(
  ref: string,
  tex: string,
  vars: string[],
  label: string,
  labelTex: string,
  steps: string[],
  meta: Record<string, unknown>,
  prompt: string
): Draft {
  return { prompt, answer: { kind: "expression", ref, vars, label }, answerTex: `${labelTex} = ${tex}`, steps, meta };
}

function choice(options: string[], correct: string, answerTex: string, steps: string[], meta: Record<string, unknown>, prompt: string): Draft {
  return { prompt, answer: { kind: "choice", options, correct }, answerTex, steps, meta };
}

// ── exponents ───────────────────────────────────────────────────────────────
const q = (n: number, d = 1) => new Q(n, d);
/** base^e for display: "" for e = 0, U^{1/3}, V^{-1} */
function pw(base: string, e: Q): string {
  if (e.isZero()) return "";
  if (e.n === 1 && e.d === 1) return base;
  return e.d === 1 ? `${base}^{${e.n}}` : `${base}^{${e.n}/${e.d}}`;
}
const prod = (...fs: string[]) => fs.filter(Boolean).join(" ") || "1";
/** a numeric coefficient in front of a body, LaTeX: 3\,body, \frac{1}{2}\,body, -body */
function coef(c: Q, body: string): string {
  if (c.n === 1 && c.d === 1) return body;
  if (c.n === -1 && c.d === 1) return `-${body}`;
  return `${c.tex()}\\,${body}`;
}
const qs = (e: Q) => (e.d === 1 ? `${e.n}` : `${e.n}/${e.d}`);
const qm = (e: Q) => [e.n, e.d];

// ═══ fundamental equation ═══════════════════════════════════════════════════
/** S = A U^g V^b N^c with g + b + c = 1 (extensive), all positive (a concave model) */
const S_EXPS: [Q, Q][] = [
  [q(1, 3), q(1, 3)], [q(1, 2), q(1, 4)], [q(2, 5), q(2, 5)], [q(1, 4), q(1, 2)],
  [q(1, 2), q(1, 3)], [q(3, 5), q(1, 5)], [q(1, 3), q(1, 2)], [q(1, 4), q(1, 4)],
];
/** U = A S^p V^q N^r with p + q + r = 1, q, r < 0 */
const U_EXPS: [Q, Q, Q][] = [
  [q(3), q(-1), q(-1)], [q(2), q(-1, 2), q(-1, 2)], [q(4), q(-2), q(-1)], [q(4), q(-1), q(-2)],
  [q(5, 2), q(-1), q(-1, 2)], [q(3), q(-3, 2), q(-1, 2)], [q(5, 3), q(-1, 3), q(-1, 3)],
];
const ENTROPY_REP = `In the entropy representation ${m("dS = \\frac{1}{T}dU + \\frac{P}{T}dV - \\frac{\\mu}{T}dN")}, so ${m("\\frac1T = \\left(\\frac{\\partial S}{\\partial U}\\right)_{V,N}")}, ${m("\\frac PT = \\left(\\frac{\\partial S}{\\partial V}\\right)_{U,N}")}, ${m("\\frac{\\mu}{T} = -\\left(\\frac{\\partial S}{\\partial N}\\right)_{U,V}")}.`;
const ENERGY_REP = `In the energy representation ${m("dU = T\\,dS - P\\,dV + \\mu\\,dN")}, so ${m("T = \\left(\\frac{\\partial U}{\\partial S}\\right)_{V,N}")}, ${m("P = -\\left(\\frac{\\partial U}{\\partial V}\\right)_{S,N}")}, ${m("\\mu = \\left(\\frac{\\partial U}{\\partial N}\\right)_{S,V}")}.`;

function feEntropyRep(r: Rng): Draft {
  const [ge, be] = r.pick(S_EXPS);
  const ce = q(1).sub(ge).sub(be);
  const Stex = `S = A\\,${prod(pw("U", ge), pw("V", be), pw("N", ce))}`;
  const Sjs = `A*U^${ge.js()}*V^${be.js()}*N^${ce.js()}`;
  const target = r.pick(["T", "P", "mu"] as const);
  const meta = { th: "fe-S", g: qm(ge), b: qm(be), c: qm(ce), target };
  const prompt = (what: string) =>
    `A model system has the fundamental equation ${m(Stex)} (${m("A")} a positive constant). Find ${what}.`;
  if (target === "T") {
    const tex = coef(q(1).div(ge), `\\frac{${pw("U", q(1).sub(ge))}}{A\\,${prod(pw("V", be), pw("N", ce))}}`);
    return symbolic(`U/(${ge.js()}*${Sjs})`, tex, ["U", "V", "N", "A"], "T", "T", [
      ENTROPY_REP,
      m(`\\frac1T = \\frac{\\partial S}{\\partial U} = ${ge.tex()}\\,A\\,${prod(pw("U", ge.sub(1)), pw("V", be), pw("N", ce))} = ${ge.tex()}\\frac{S}{U}`),
      `Invert: ${m(`T = \\frac{U}{${ge.tex()}S} = ${tex}`)}.`,
    ], meta, prompt(`the temperature ${m("T(U, V, N)")}`));
  }
  if (target === "P") {
    const k = be.div(ge);
    const tex = coef(k, "\\frac{U}{V}");
    return symbolic(`${k.js()}*U/V`, tex, ["U", "V", "N", "A"], "P", "P", [
      ENTROPY_REP,
      `${m(`\\frac1T = ${ge.tex()}\\frac SU`)} and ${m(`\\frac PT = \\frac{\\partial S}{\\partial V} = ${be.tex()}\\frac SV`)}.`,
      `Divide: ${m(`P = \\frac{P/T}{1/T} = \\frac{${be.tex()}\\,S/V}{${ge.tex()}\\,S/U} = ${tex}`)}.`,
    ], meta, prompt(`the pressure ${m("P(U, V, N)")}`));
  }
  const k = ce.div(ge).neg();
  const tex = coef(k, "\\frac{U}{N}");
  return symbolic(`${k.js()}*U/N`, tex, ["U", "V", "N", "A"], "μ", "\\mu", [
    ENTROPY_REP,
    `${m(`\\frac1T = ${ge.tex()}\\frac SU`)} and ${m(`-\\frac{\\mu}{T} = \\frac{\\partial S}{\\partial N} = ${ce.tex()}\\frac SN`)}.`,
    `Divide: ${m(`\\mu = -\\frac{${ce.tex()}\\,S/N}{${ge.tex()}\\,S/U} = ${tex}`)}. Negative, as for any system whose entropy grows with ${m("N")}.`,
  ], meta, prompt(`the chemical potential ${m("\\mu(U, V, N)")}`));
}

function feEnergyRep(r: Rng): Draft {
  const [pe, qe, re] = r.pick(U_EXPS);
  const Utex = `U = A\\,${prod(pw("S", pe), pw("V", qe), pw("N", re))}`;
  const target = r.pick(["T", "P", "mu"] as const);
  const meta = { th: "fe-U", p: qm(pe), q: qm(qe), r: qm(re), target };
  const prompt = (what: string) => `A model system has the fundamental equation ${m(Utex)} (${m("A > 0")}). Find ${what}.`;
  if (target === "T") {
    const tex = coef(pe, `A\\,${prod(pw("S", pe.sub(1)), pw("V", qe), pw("N", re))}`);
    return symbolic(`${pe.js()}*A*S^${pe.sub(1).js()}*V^${qe.js()}*N^${re.js()}`, tex, ["S", "V", "N", "A"], "T", "T", [
      ENERGY_REP,
      `Differentiate at fixed ${m("V, N")}: ${m(`T = \\frac{\\partial U}{\\partial S} = ${tex}`)}.`,
    ], meta, prompt(`the temperature ${m("T(S, V, N)")}`));
  }
  if (target === "P") {
    const c = qe.neg();
    const tex = coef(c, `A\\,${prod(pw("S", pe), pw("V", qe.sub(1)), pw("N", re))}`);
    return symbolic(`${c.js()}*A*S^${pe.js()}*V^${qe.sub(1).js()}*N^${re.js()}`, tex, ["S", "V", "N", "A"], "P", "P", [
      ENERGY_REP,
      m(`\\frac{\\partial U}{\\partial V} = ${coef(qe, `A\\,${prod(pw("S", pe), pw("V", qe.sub(1)), pw("N", re))}`)}`),
      `${m(`P = -\\frac{\\partial U}{\\partial V} = ${tex}`)} — positive, as it must be.`,
    ], meta, prompt(`the pressure ${m("P(S, V, N)")}`));
  }
  const tex = coef(re, `A\\,${prod(pw("S", pe), pw("V", qe), pw("N", re.sub(1)))}`);
  return symbolic(`${re.js()}*A*S^${pe.js()}*V^${qe.js()}*N^${re.sub(1).js()}`, tex, ["S", "V", "N", "A"], "μ", "\\mu", [
    ENERGY_REP,
    `Differentiate at fixed ${m("S, V")}: ${m(`\\mu = \\frac{\\partial U}{\\partial N} = ${tex}`)}.`,
  ], meta, prompt(`the chemical potential ${m("\\mu(S, V, N)")}`));
}

function feIdeal(r: Rng): Draft {
  const [c, ctex, what] = r.pick([[1.5, "\\tfrac32", "monatomic"], [2.5, "\\tfrac52", "diatomic"], [3, "3", "polyatomic"]] as [number, string, string][]);
  const N = r.pick([0.5, 1, 1.5, 2, 3]);
  const T0 = r.pick([200, 250, 298, 300, 350, 400, 500, 600]);
  const U = r4(c * N * R * T0);
  const V = r.pick([0.005, 0.01, 0.0224, 0.025, 0.05, 0.1]);
  const target = r.pick(["T", "P"] as const);
  const S = `S = NR\\left[${ctex}\\ln\\frac{U}{N} + \\ln\\frac{V}{N}\\right] + Ns_0`;
  const meta = { th: "fe-ideal", c, N, U, V, target };
  const stem = `The ${what} ideal gas has ${m(S)} (${m("s_0")} a constant). For ${m(`N = ${vu(N, "mol")}`)} with ${m(`U = ${vu(U, "J")}`)} in ${m(`V = ${vu(V, "m³")}`)}`;
  const T = U / (c * N * R);
  if (target === "T")
    return numeric(T, "T", "T", "K", [
      m(`\\frac1T = \\left(\\frac{\\partial S}{\\partial U}\\right)_{V,N} = \\frac{${ctex}NR}{U}`),
      m(`T = \\frac{U}{${ctex}NR} = \\frac{${g(U)}}{${ctex}(${g(N)})(8.314)} = ${fmt(T)}${u("K")}`),
    ], meta, `${stem}, find ${m("T")}.`);
  const P = U / (c * V);
  return numeric(P, "P", "P", "Pa", [
    `${m(`\\frac PT = \\left(\\frac{\\partial S}{\\partial V}\\right)_{U,N} = \\frac{NR}{V}`)} and ${m(`\\frac1T = \\frac{${ctex}NR}{U}`)}.`,
    `Divide: ${m(`P = \\frac{U}{${ctex}V}`)} (equivalently ${m("PV = NRT")}).`,
    m(`P = \\frac{${g(U)}}{${ctex}(${g(V)})} = ${fmt(P)}${u("Pa")}`),
  ], meta, `${stem}, find ${m("P")}.`);
}

function feEuler(r: Rng): Draft {
  const N = r.pick([1, 2, 0.5]);
  const T = r.pick([250, 298, 300, 350, 400]);
  const P = r.pick([1e5, 2e5, 5e4, 1.5e5]);
  const V = r4((N * R * T) / P);
  const S = r4(N * r.pick([120, 135, 150, 160, 175, 190]));
  const mu = -r.pick([28000, 32000, 35000, 38000, 42000, 45000]) - r.int(0, 9) * 100;
  const U = T * S - P * V + mu * N;
  require_(Math.abs(U) > 500);
  const target = r.pick(["U", "mu"] as const);
  const meta = { th: "fe-euler", T, P, V, S, N, mu, U: r4(U), target };
  const euler = `Extensivity: ${m("U(\\lambda S, \\lambda V, \\lambda N) = \\lambda U")}. Differentiate in ${m("\\lambda")} at ${m("\\lambda = 1")}: the Euler relation ${m("U = TS - PV + \\mu N")}.`;
  if (target === "U")
    return numeric(U, "U", "U", "J", [
      euler,
      m(`U = (${T})(${g(S)}) - (${g(P)})(${g(V)}) + (${g(mu)})(${g(N)}) = ${fmt(T * S)} - ${fmt(P * V)} ${mu * N < 0 ? "-" : "+"} ${fmt(Math.abs(mu * N))} = ${fmt(U)}${u("J")}`),
    ], meta,
    `A one-component fluid in equilibrium has ${m(`T = ${vu(T, "K")}`)}, ${m(`P = ${vu(P, "Pa")}`)}, ${m(`V = ${vu(V, "m³")}`)}, ${m(`S = ${vu(S, "J/K")}`)}, ${m(`N = ${vu(N, "mol")}`)} and ${m(`\\mu = ${vu(mu, "J/mol")}`)}. Find its internal energy ${m("U")}.`);
  const Ug = r4(U);
  const muv = (Ug - T * S + P * V) / N;
  return numeric(muv, "μ", "\\mu", "J/mol", [
    euler,
    m(`\\mu = \\frac{U - TS + PV}{N} = \\frac{${g(Ug)} - (${T})(${g(S)}) + (${g(P)})(${g(V)})}{${g(N)}} = ${fmt(muv)}${u("J/mol")}`),
  ], meta,
  `A one-component fluid in equilibrium has ${m(`U = ${vu(Ug, "J")}`)}, ${m(`T = ${vu(T, "K")}`)}, ${m(`P = ${vu(P, "Pa")}`)}, ${m(`V = ${vu(V, "m³")}`)}, ${m(`S = ${vu(S, "J/K")}`)} and ${m(`N = ${vu(N, "mol")}`)}. Use the Euler relation to find ${m("\\mu")}.`);
}

function feGibbsDuhem(r: Rng): Draft {
  const T = r.pick([250, 298, 300, 350, 400, 500]);
  const P1 = r.pick([1, 2, 5, 10]);
  const P2 = r.pick([0.5, 1, 3, 4, 20, 50].filter((x) => x !== P1));
  const dmu = R * T * Math.log(P2 / P1);
  return numeric(dmu, "Δμ", "\\Delta\\mu", "J/mol", [
    `Gibbs–Duhem: ${m("S\\,dT - V\\,dP + N\\,d\\mu = 0")}, so at constant ${m("T")}: ${m("d\\mu = v\\,dP")} with ${m("v = V/N")}.`,
    `Ideal gas: ${m("v = RT/P")}, so ${m(`\\Delta\\mu = \\int_{P_1}^{P_2}\\frac{RT}{P}dP = RT\\ln\\frac{P_2}{P_1}`)}.`,
    m(`\\Delta\\mu = (8.314)(${T})\\ln\\frac{${g(P2)}}{${g(P1)}} = ${fmt(dmu)}${u("J/mol")}`),
  ], { th: "fe-gd", T, P1, P2 },
  `An ideal gas at ${m(`${T}\\,\\mathrm{K}`)} is ${P2 > P1 ? "compressed" : "expanded"} isothermally from ${m(vu(P1, "bar"))} to ${m(vu(P2, "bar"))}. Use the Gibbs–Duhem equation to find the change in its chemical potential ${m("\\Delta\\mu")}.`);
}

// ═══ first law, reversible ideal-gas paths ══════════════════════════════════
const SIGN = `Sign convention: ${m("\\Delta U = q + w")}, with ${m("w")} the work done on the gas, ${m("\\delta w = -P\\,dV")}.`;
const GASES: [string, number, string][] = [
  ["argon (monatomic)", 1.5, "\\tfrac32R"],
  ["helium (monatomic)", 1.5, "\\tfrac32R"],
  ["nitrogen (diatomic)", 2.5, "\\tfrac52R"],
  ["oxygen (diatomic)", 2.5, "\\tfrac52R"],
];

function flIsothermal(r: Rng): Draft {
  const n = r.pick([0.5, 1, 1.5, 2, 3]);
  const T = r.pick([273, 298, 300, 350, 400, 500]);
  const V1 = r.pick([2, 5, 10, 20]);
  const V2 = r.pick([1, 4, 8, 15, 25, 30, 40].filter((v) => v !== V1));
  const w = -n * R * T * Math.log(V2 / V1);
  const target = r.pick(["w", "q"] as const);
  const meta = { th: "fl-iso", n, T, V1: V1 / 1000, V2: V2 / 1000, target };
  const steps = [
    SIGN,
    `Isothermal ideal gas: ${m("P = nRT/V")}, so ${m("w = -\\int_{V_1}^{V_2}\\frac{nRT}{V}dV = -nRT\\ln\\frac{V_2}{V_1}")}.`,
    m(`w = -(${g(n)})(8.314)(${T})\\ln\\frac{${V2}}{${V1}} = ${fmt(w)}${u("J")}`),
  ];
  const stem = `${m(`${g(n)}\\,\\mathrm{mol}`)} of an ideal gas is taken reversibly and isothermally at ${m(`${T}\\,\\mathrm{K}`)} from ${m(vu(V1, "L"))} to ${m(vu(V2, "L"))}.`;
  if (target === "w") return numeric(w, "w", "w", "J", steps, meta, `${stem} Find the work done on the gas, ${m("w")}.`);
  return numeric(-w, "q", "q", "J", [...steps, `Ideal gas at constant ${m("T")}: ${m("\\Delta U = 0")}, so ${m(`q = -w = ${fmt(-w)}${u("J")}`)}.`], meta,
    `${stem} Find the heat absorbed by the gas, ${m("q")}.`);
}

function flAdiabatic(r: Rng): Draft {
  const [gas, c, cvtex] = r.pick(GASES);
  const n = r.pick([0.5, 1, 2]);
  const T1 = r.pick([273, 298, 300, 350, 400, 500]);
  const V1 = r.pick([1, 2, 5, 10, 20]);
  const V2 = r.pick([0.5, 2, 4, 8, 10, 25, 40].filter((v) => v !== V1));
  const T2 = T1 * (V1 / V2) ** (1 / c);
  const target = r.pick(["T2", "w"] as const);
  const meta = { th: "fl-adia", n, c, T1, V1: V1 / 1000, V2: V2 / 1000, target };
  const s0 = [
    SIGN,
    `Reversible adiabatic: ${m("dU = \\delta w")}, i.e. ${m("nC_V\\,dT = -\\frac{nRT}{V}dV")}. Separate and integrate: ${m("T_2 = T_1\\left(\\frac{V_1}{V_2}\\right)^{R/C_V}")}, with ${m(`C_V = ${cvtex}`)}.`,
    m(`T_2 = ${T1}\\left(\\frac{${V1}}{${V2}}\\right)^{1/${c}} = ${fmt(T2)}${u("K")}`),
  ];
  const stem = `${m(`${g(n)}\\,\\mathrm{mol}`)} of ${gas}, treated as an ideal gas, ${V2 > V1 ? "expands" : "is compressed"} reversibly and adiabatically from ${m(vu(V1, "L"))} at ${m(`${T1}\\,\\mathrm{K}`)} to ${m(vu(V2, "L"))}.`;
  if (target === "T2") return numeric(T2, "T₂", "T_2", "K", s0, meta, `${stem} Find the final temperature.`);
  const w = n * c * R * (T2 - T1);
  return numeric(w, "w", "w", "J", [...s0, `${m("q = 0")}, so ${m(`w = \\Delta U = nC_V(T_2 - T_1) = (${g(n)})(${c})(8.314)(${fmt(T2, 4)} - ${T1}) = ${fmt(w)}${u("J")}`)}.`], meta,
    `${stem} Find the work done on the gas, ${m("w")}.`);
}

function flIsobaric(r: Rng): Draft {
  const [gas, c, cvtex] = r.pick(GASES);
  const n = r.pick([0.5, 1, 2, 3]);
  const P = r.pick([1, 2, 5]);
  const T1 = r.pick([273, 298, 300, 350]);
  const T2 = T1 + r.pick([-50, -25, 25, 50, 100, 150, 200]);
  const dT = T2 - T1;
  const target = r.pick(["q", "w", "dU"] as const);
  const meta = { th: "fl-isobaric", n, c, P: P * 1e5, T1, T2, target };
  const stem = `${m(`${g(n)}\\,\\mathrm{mol}`)} of ${gas}, an ideal gas, is ${T2 > T1 ? "heated" : "cooled"} reversibly at a constant ${m(vu(P, "bar"))} from ${m(`${T1}\\,\\mathrm{K}`)} to ${m(`${T2}\\,\\mathrm{K}`)}.`;
  const wv = -n * R * dT, dU = n * c * R * dT, qv = dU - wv;
  const sw = `${m("w = -P\\Delta V = -nR\\Delta T")} (ideal gas at constant ${m("P")}) ${m(`= -(${g(n)})(8.314)(${dT}) = ${fmt(wv)}${u("J")}`)}.`;
  const sU = `${m(`\\Delta U = nC_V\\Delta T`)} with ${m(`C_V = ${cvtex}`)}: ${m(`\\Delta U = ${fmt(dU)}${u("J")}`)}.`;
  if (target === "w") return numeric(wv, "w", "w", "J", [SIGN, sw], meta, `${stem} Find the work done on the gas, ${m("w")}.`);
  if (target === "dU") return numeric(dU, "ΔU", "\\Delta U", "J", [SIGN, `Ideal gas: ${m("U")} depends only on ${m("T")}.`, sU], meta, `${stem} Find ${m("\\Delta U")}.`);
  return numeric(qv, "q", "q", "J", [SIGN, sw, sU, `${m(`q = \\Delta U - w = nC_P\\Delta T = ${fmt(qv)}${u("J")}`)} (${m("C_P = C_V + R")}).`], meta,
    `${stem} Find the heat absorbed, ${m("q")}.`);
}

function flIsochoric(r: Rng): Draft {
  const [gas, c, cvtex] = r.pick(GASES);
  const n = r.pick([0.5, 1, 2]);
  const V = r.pick([5, 10, 20, 25]);
  const T1 = r.pick([273, 298, 300, 350]);
  const T2 = T1 + r.pick([-50, 25, 50, 100, 150, 200]);
  const target = r.pick(["q", "P2"] as const);
  const meta = { th: "fl-isochoric", n, c, V: V / 1000, T1, T2, target };
  const stem = `${m(`${g(n)}\\,\\mathrm{mol}`)} of ${gas}, an ideal gas, in a rigid ${m(vu(V, "L"))} vessel is taken from ${m(`${T1}\\,\\mathrm{K}`)} to ${m(`${T2}\\,\\mathrm{K}`)}.`;
  if (target === "q") {
    const qv = n * c * R * (T2 - T1);
    return numeric(qv, "q", "q", "J", [
      SIGN,
      `Rigid vessel: ${m("dV = 0")}, so ${m("w = 0")} and ${m("q = \\Delta U = nC_V\\Delta T")}, ${m(`C_V = ${cvtex}`)}.`,
      m(`q = (${g(n)})(${c})(8.314)(${T2 - T1}) = ${fmt(qv)}${u("J")}`),
    ], meta, `${stem} Find the heat absorbed, ${m("q")}.`);
  }
  const P2 = (n * R * T2) / (V / 1000) / 1000;
  return numeric(P2, "P₂", "P_2", "kPa", [
    `At constant volume ${m("P \\propto T")}: ${m("P_2 = nRT_2/V")}, with ${m(`V = ${g(V / 1000)}\\,\\mathrm{m^3}`)}.`,
    m(`P_2 = \\frac{(${g(n)})(8.314)(${T2})}{${g(V / 1000)}} = ${fmt(P2 * 1000)}\\,\\mathrm{Pa} = ${fmt(P2)}${u("kPa")}`),
  ], meta, `${stem} Find the final pressure in kPa.`);
}

// ═══ Legendre transforms ═══════════════════════════════════════════════════
function lgHelmholtz(r: Rng): Draft {
  const [pe, qe, re] = r.pick(U_EXPS);
  const Utex = `U = A\\,${prod(pw("S", pe), pw("V", qe), pw("N", re))}`;
  const inv = q(1).div(pe.sub(1));
  const k = q(1).div(pe).sub(1);
  const inner = `\\frac{T\\,${prod(pw("V", qe.neg()), pw("N", re.neg()))}}{${pe.tex()}A}`;
  const Sstar = `\\left(${inner}\\right)^{${qs(inv)}}`;
  const tex = coef(k, `T${Sstar}`);
  const ref = `${k.js()}*T*(T*V^${qe.neg().js()}*N^${re.neg().js()}/(${pe.js()}*A))^${inv.js()}`;
  return symbolic(ref, tex, ["T", "V", "N", "A"], "F", "F", [
    `${m("F = U - TS")}, written in its natural variables ${m("(T, V, N)")}: eliminate ${m("S")} using ${m("T = \\partial U/\\partial S")}.`,
    `${m(`T = ${coef(pe, `A\\,${prod(pw("S", pe.sub(1)), pw("V", qe), pw("N", re))}`)}`)}, so ${m(`S = ${Sstar}`)}.`,
    `Since ${m(`T = ${pe.tex()}\\,U/S`)}, ${m(`U = \\frac{TS}{${pe.tex()}}`)} and ${m(`F = U - TS = ${coef(k, "TS")}`)}.`,
    `Substitute ${m("S(T, V, N)")}: ${m(`F = ${tex}`)}.`,
  ], { th: "lg-F", p: qm(pe), q: qm(qe), r: qm(re) },
  `A model system has ${m(Utex)} (${m("A > 0")}). Find the Helmholtz free energy ${m("F(T, V, N)")}.`);
}

function lgEnthalpy(r: Rng): Draft {
  const [pe, qe, re] = r.pick(U_EXPS);
  const Utex = `U = A\\,${prod(pw("S", pe), pw("V", qe), pw("N", re))}`;
  const mq = qe.neg();
  const inv = q(1).div(q(1).sub(qe)); // V = (−qA S^p N^r / P)^{1/(1−q)}
  const k = q(1).sub(qe).div(mq);
  const inner = `\\frac{${coef(mq, `A\\,${pw("S", pe)}`)}}{P\\,${pw("N", re.neg())}}`;
  const Vstar = `\\left(${inner}\\right)^{${qs(inv)}}`;
  const tex = coef(k, `P${Vstar}`);
  const ref = `${k.js()}*P*(${mq.js()}*A*S^${pe.js()}/(P*N^${re.neg().js()}))^${inv.js()}`;
  return symbolic(ref, tex, ["S", "P", "N", "A"], "H", "H", [
    `${m("H = U + PV")} in its natural variables ${m("(S, P, N)")}: eliminate ${m("V")} using ${m("P = -\\partial U/\\partial V")}.`,
    `${m(`P = ${coef(mq, `A\\,${prod(pw("S", pe), pw("V", qe.sub(1)), pw("N", re))}`)} = ${coef(mq, "\\frac{U}{V}")}`)}, so ${m(`V = ${Vstar}`)}.`,
    `${m(`U = ${mq.d === 1 && mq.n === 1 ? "" : `\\frac{1}{${mq.tex()}}`}PV`)}, so ${m(`H = U + PV = ${coef(k, "PV")}`)}.`,
    `Substitute ${m("V(S, P, N)")}: ${m(`H = ${tex}`)}.`,
  ], { th: "lg-H", p: qm(pe), q: qm(qe), r: qm(re) },
  `A model system has ${m(Utex)} (${m("A > 0")}). Find the enthalpy ${m("H(S, P, N)")}.`);
}

const NAT_OPTIONS = ["S, V, N", "S, P, N", "T, V, N", "T, P, N", "T, V, μ", "S, V, μ"];
const POTENTIALS: { def: string; name: string; swaps: string[]; ans: number; why: string }[] = [
  { def: "H = U + PV", name: "the enthalpy", swaps: ["V"], ans: 1, why: "dH = T\\,dS + V\\,dP + \\mu\\,dN" },
  { def: "F = U - TS", name: "the Helmholtz free energy", swaps: ["S"], ans: 2, why: "dF = -S\\,dT - P\\,dV + \\mu\\,dN" },
  { def: "G = U - TS + PV", name: "the Gibbs free energy", swaps: ["S", "V"], ans: 3, why: "dG = -S\\,dT + V\\,dP + \\mu\\,dN" },
  { def: "G = H - TS", name: "the Gibbs free energy", swaps: ["S", "V"], ans: 3, why: "dG = -S\\,dT + V\\,dP + \\mu\\,dN" },
  { def: "\\Omega = U - TS - \\mu N", name: "the grand potential", swaps: ["S", "N"], ans: 4, why: "d\\Omega = -S\\,dT - P\\,dV - N\\,d\\mu" },
  { def: "\\Omega = F - \\mu N", name: "the grand potential", swaps: ["S", "N"], ans: 4, why: "d\\Omega = -S\\,dT - P\\,dV - N\\,d\\mu" },
  { def: "L = U - \\mu N", name: "the potential", swaps: ["N"], ans: 5, why: "dL = T\\,dS - P\\,dV - N\\,d\\mu" },
  { def: "U", name: "the internal energy", swaps: [], ans: 0, why: "dU = T\\,dS - P\\,dV + \\mu\\,dN" },
];
function lgNatural(r: Rng): Draft {
  const p = r.pick(POTENTIALS);
  const correct = NAT_OPTIONS[p.ans];
  return choice(NAT_OPTIONS, correct, correct.replace("μ", "\\mu"), [
    `Start from ${m("dU = T\\,dS - P\\,dV + \\mu\\,dN")}: ${m("U")}'s natural variables are ${m("S, V, N")}.`,
    `Each Legendre term swaps one pair: ${m("-TS")} trades ${m("S \\to T")}, ${m("+PV")} trades ${m("V \\to P")}, ${m("-\\mu N")} trades ${m("N \\to \\mu")}.`,
    `${m(p.why)}.`,
  ], { th: "lg-natural", swaps: p.swaps, answer: correct },
  `${p.def === "U" ? "Consider the internal energy U" : `Define ${m(p.def)} (${p.name})`}. What are its natural variables?`);
}

function lgDerive(r: Rng): Draft {
  const [c, ctex] = r.pick([[1.5, "\\tfrac32"], [2.5, "\\tfrac52"]] as [number, string][]);
  const cj = c === 1.5 ? "(3/2)" : "(5/2)";
  const vdw = r.chance(0.5);
  if (vdw) {
    const Ftex = `F = -NRT\\left[\\ln\\frac{V - Nb}{N} + ${ctex}\\ln T + 1\\right] - \\frac{aN^2}{V}`;
    const target = r.pick(["P", "S"] as const);
    const meta = { th: "lg-derive", model: "vdw", c, target };
    const vars = ["b", "N", "a", "R", "T", "V"];
    if (target === "P")
      return symbolic("N*R*T/(V - N*b) - a*N^2/V^2", "\\frac{NRT}{V - Nb} - \\frac{aN^2}{V^2}", vars, "P", "P", [
        `${m("dF = -S\\,dT - P\\,dV + \\mu\\,dN")}, so ${m("P = -(\\partial F/\\partial V)_{T,N}")}.`,
        m(`\\frac{\\partial F}{\\partial V} = -\\frac{NRT}{V - Nb} + \\frac{aN^2}{V^2}`),
        `${m("P = \\frac{NRT}{V - Nb} - \\frac{aN^2}{V^2}")} — the van der Waals equation.`,
      ], meta, `A van der Waals fluid has ${m(Ftex)} (${m("a, b > 0")}). Find ${m("P(T, V, N)")}.`);
    return symbolic(`N*R*(log((V - N*b)/N) + ${cj}*log(T) + 1 + ${cj})`, `NR\\left[\\ln\\frac{V - Nb}{N} + ${ctex}\\ln T + ${c === 1.5 ? "\\tfrac52" : "\\tfrac72"}\\right]`, vars, "S", "S", [
      `${m("S = -(\\partial F/\\partial T)_{V,N}")}.`,
      m(`\\frac{\\partial F}{\\partial T} = -NR\\left[\\ln\\frac{V - Nb}{N} + ${ctex}\\ln T + 1\\right] - NRT\\cdot\\frac{${ctex}}{T}`),
      `${m(`S = NR\\left[\\ln\\frac{V - Nb}{N} + ${ctex}\\ln T + ${c === 1.5 ? "\\tfrac52" : "\\tfrac72"}\\right]`)} — the ${m("a")} term doesn't depend on ${m("T")}, so attraction leaves ${m("S")} alone.`,
    ], meta, `A van der Waals fluid has ${m(Ftex)} (${m("a, b > 0")}). Find the entropy ${m("S(T, V, N)")}.`);
  }
  const Ftex = `F = -NRT\\left[\\ln\\frac{V}{N} + ${ctex}\\ln T + 1\\right]`;
  const target = r.pick(["S", "mu", "P"] as const);
  const meta = { th: "lg-derive", model: "ideal", c, target };
  const vars = ["N", "R", "T", "V"];
  if (target === "P")
    return symbolic("N*R*T/V", "\\frac{NRT}{V}", vars, "P", "P", [
      `${m("P = -(\\partial F/\\partial V)_{T,N}")}.`,
      `Only ${m("\\ln V")} depends on ${m("V")}: ${m("P = NRT\\cdot\\frac1V = \\frac{NRT}{V}")}.`,
    ], meta, `An ideal gas has ${m(Ftex)} (energies from a reference). Find ${m("P(T, V, N)")}.`);
  if (target === "S")
    return symbolic(`N*R*(log(V/N) + ${cj}*log(T) + 1 + ${cj})`, `NR\\left[\\ln\\frac{V}{N} + ${ctex}\\ln T + ${c === 1.5 ? "\\tfrac52" : "\\tfrac72"}\\right]`, vars, "S", "S", [
      `${m("S = -(\\partial F/\\partial T)_{V,N}")} — product rule on ${m("T\\,[\\ldots]")}.`,
      m(`S = NR\\left[\\ln\\frac{V}{N} + ${ctex}\\ln T + 1\\right] + NRT\\cdot\\frac{${ctex}}{T}`),
      m(`S = NR\\left[\\ln\\frac{V}{N} + ${ctex}\\ln T + ${c === 1.5 ? "\\tfrac52" : "\\tfrac72"}\\right]`),
    ], meta, `An ideal gas has ${m(Ftex)} (energies from a reference). Find the entropy ${m("S(T, V, N)")}.`);
  return symbolic(`-R*T*(log(V/N) + ${cj}*log(T))`, `-RT\\left[\\ln\\frac{V}{N} + ${ctex}\\ln T\\right]`, vars, "μ", "\\mu", [
    `${m("\\mu = (\\partial F/\\partial N)_{T,V}")} — ${m("N")} appears twice: in front and inside ${m("\\ln(V/N)")}.`,
    m(`\\mu = -RT\\left[\\ln\\frac VN + ${ctex}\\ln T + 1\\right] - NRT\\cdot\\left(-\\frac1N\\right)`),
    m(`\\mu = -RT\\left[\\ln\\frac{V}{N} + ${ctex}\\ln T\\right]`),
  ], meta, `An ideal gas has ${m(Ftex)} (energies from a reference). Find the chemical potential ${m("\\mu(T, V, N)")}.`);
}

function lgGibbsHelmholtz(r: Rng): Draft {
  const a = -r.int(10, 90) * 100;
  const b = r.pick([-40, -30, -25, -20, 15, 20, 30]);
  const c = r.pick([-6, -5, -4, -3, -2, 2, 3, 4, 5]);
  const logForm = r.chance(0.5);
  const sgn = (k: number, body: string) => (k < 0 ? ` - ${-k}${body}` : ` + ${k}${body}`);
  const Gtex = `G(T) = ${a}${sgn(b, "T")}${sgn(c, logForm ? "T\\ln T" : "T^2")}`;
  const target = r.pick(["H", "S"] as const);
  const meta = { th: "lg-gh", a, b, c, form: logForm ? "TlnT" : "T2", target };
  const prompt = `The molar Gibbs energy of a substance at fixed pressure is ${m(Gtex)} (J/mol, ${m("T")} in K). Find ${target === "H" ? m("H(T)") : m("S(T)")}.`;
  const S0 = `${m("dG = -S\\,dT + V\\,dP")}, so ${m("S = -(\\partial G/\\partial T)_P")}.`;
  if (logForm) {
    const Sref = `${-b - c} - (${c})*log(T)`;
    const Stex = `${-b - c}${c > 0 ? ` - ${c}` : ` + ${-c}`}\\ln T`;
    if (target === "S")
      return symbolic(Sref, Stex, ["T"], "S", "S", [S0, m(`\\frac{\\partial G}{\\partial T} = ${b} + ${c}(\\ln T + 1)`), m(`S = ${Stex}`)], meta, prompt);
    return symbolic(`${a} - (${c})*T`, `${a}${c > 0 ? ` - ${c}T` : ` + ${-c}T`}`, ["T"], "H", "H", [
      S0,
      m(`S = ${Stex}`),
      `${m("H = G + TS")} (Gibbs–Helmholtz): the ${m("bT")} and ${m("T\\ln T")} pieces cancel, leaving ${m(`H = ${a}${c > 0 ? ` - ${c}T` : ` + ${-c}T`}`)}.`,
    ], meta, prompt);
  }
  const Stex = `${-b}${-2 * c > 0 ? ` + ${-2 * c}T` : ` - ${2 * c}T`}`;
  if (target === "S")
    return symbolic(`${-b} - (${2 * c})*T`, Stex, ["T"], "S", "S", [S0, m(`\\frac{\\partial G}{\\partial T} = ${b} + ${2 * c}T`), m(`S = ${Stex}`)], meta, prompt);
  return symbolic(`${a} - (${c})*T^2`, `${a}${c > 0 ? ` - ${c}T^2` : ` + ${-c}T^2`}`, ["T"], "H", "H", [
    S0,
    m(`S = ${Stex}`),
    `${m("H = G + TS")}: ${m(`H = ${a}${c > 0 ? ` - ${c}T^2` : ` + ${-c}T^2`}`)}. (Check: ${m("H = -T^2\\,\\partial(G/T)/\\partial T")}.)`,
  ], meta, prompt);
}

// ═══ Maxwell relations ═════════════════════════════════════════════════════
type Partial = [string, string, string]; // (∂X/∂Y)_Z
const MAXWELL: { a: Partial; b: Partial; sign: 1 | -1; pot: string; dpot: string }[] = [
  { a: ["T", "V", "S"], b: ["P", "S", "V"], sign: -1, pot: "U", dpot: "dU = T\\,dS - P\\,dV" },
  { a: ["T", "P", "S"], b: ["V", "S", "P"], sign: 1, pot: "H", dpot: "dH = T\\,dS + V\\,dP" },
  { a: ["S", "V", "T"], b: ["P", "T", "V"], sign: 1, pot: "F", dpot: "dF = -S\\,dT - P\\,dV" },
  { a: ["S", "P", "T"], b: ["V", "T", "P"], sign: -1, pot: "G", dpot: "dG = -S\\,dT + V\\,dP" },
];
const ptxt = ([X, Y, Z]: Partial, s = 1) => `${s < 0 ? "-" : ""}(∂${X}/∂${Y})_${Z}`;
const ptex = ([X, Y, Z]: Partial, s = 1) => `${s < 0 ? "-" : ""}\\left(\\frac{\\partial ${X}}{\\partial ${Y}}\\right)_{${Z}}`;

function mxPick(r: Rng): Draft {
  const rel = r.pick(MAXWELL);
  const flip = r.chance(0.5);
  const target = flip ? rel.b : rel.a;
  const partner = flip ? rel.a : rel.b;
  const correct = ptxt(partner, rel.sign);
  const others = MAXWELL.filter((x) => x !== rel).flatMap((x) => [x.a, x.b]);
  const d1 = r.pick(others);
  const d2 = r.pick(others.filter((x) => x !== d1));
  const raw: [Partial, number][] = [[partner, rel.sign], [partner, -rel.sign], [d1, r.pick([1, -1])], [d2, r.pick([1, -1])]];
  const k = r.int(0, 3); // rotate so the right answer isn't always first
  const rot = [...raw.slice(k), ...raw.slice(0, k)];
  const options = rot.map(([p, s]) => ptxt(p, s));
  const [X, Y] = [rel.a[2], rel.b[2]]; // the potential's natural variables
  return choice(options, correct, `${ptex(target)} = ${ptex(partner, rel.sign)}`, [
    `${m(ptex(target))} holds ${m(target[2])} fixed and differentiates by ${m(target[1])}: the natural variables are ${m(`(${X}, ${Y})`)}, so use ${m(rel.pot)}.`,
    `${m(rel.dpot)}. Mixed second derivatives of ${m(rel.pot)} are equal.`,
    `${m(`${ptex(rel.a)} = ${ptex(rel.b, rel.sign)}`)}.`,
  ], { th: "mx-pick", target, options: rot, correct: options.indexOf(correct) },
  `Which partial derivative equals ${m(ptex(target))}?`);
}

const LIQUIDS = [
  { name: "liquid water at 298 K", T: 298, alpha: 2.57e-4, kappa: 4.52e-10, V: 1.807e-5, Cp: 75.3 },
  { name: "ethanol at 293 K", T: 293, alpha: 1.12e-3, kappa: 1.11e-9, V: 5.84e-5, Cp: 112.3 },
  { name: "benzene at 298 K", T: 298, alpha: 1.24e-3, kappa: 9.67e-10, V: 8.94e-5, Cp: 136.0 },
  { name: "mercury at 293 K", T: 293, alpha: 1.81e-4, kappa: 4.0e-11, V: 1.48e-5, Cp: 27.98 },
  { name: "copper at 298 K", T: 298, alpha: 4.95e-5, kappa: 7.3e-12, V: 7.11e-6, Cp: 24.4 },
];
const liqStem = (L: (typeof LIQUIDS)[number]) =>
  `For ${L.name} (${m("P = 1\\,\\mathrm{bar}")}): ${m(`\\alpha = ${vu(L.alpha, "K⁻¹")}`)}, ${m(`\\kappa_T = ${vu(L.kappa, "Pa⁻¹")}`)}, molar volume ${m(`v = ${vu(L.V, "m³/mol")}`)}.`;

function mxMeasurable(r: Rng): Draft {
  const L = r.pick(LIQUIDS);
  const target = r.pick(["dSdV", "dSdP", "dUdV", "dHdP", "CpCv"] as const);
  const meta = { th: "mx-meas", T: L.T, P: 1e5, alpha: L.alpha, kappa: L.kappa, V: L.V, Cp: L.Cp, target };
  const defs = `Definitions: ${m("\\alpha = \\frac1v\\left(\\frac{\\partial v}{\\partial T}\\right)_P")}, ${m("\\kappa_T = -\\frac1v\\left(\\frac{\\partial v}{\\partial P}\\right)_T")}; triple product gives ${m("\\left(\\frac{\\partial P}{\\partial T}\\right)_v = \\frac{\\alpha}{\\kappa_T}")}.`;
  const { T, alpha: a, kappa: k, V } = L;
  if (target === "dSdV") {
    const val = a / k;
    return numeric(val, "(∂S/∂V)_T", "\\left(\\frac{\\partial S}{\\partial V}\\right)_T", "Pa/K", [
      `Maxwell (from ${m("F")}): ${m("\\left(\\frac{\\partial S}{\\partial V}\\right)_T = \\left(\\frac{\\partial P}{\\partial T}\\right)_V")}.`,
      defs,
      m(`\\frac{\\alpha}{\\kappa_T} = \\frac{${g(a)}}{${g(k)}} = ${fmt(val)}\\,\\mathrm{J/(K\\cdot m^3)}`),
    ], meta, `${liqStem(L)} Find ${m("\\left(\\partial S/\\partial V\\right)_T")} in J/(K·m³) = Pa/K.`);
  }
  if (target === "dSdP") {
    const val = -V * a;
    return numeric(val, "(∂s/∂P)_T", "\\left(\\frac{\\partial s}{\\partial P}\\right)_T", "m³/(mol·K)", [
      `Maxwell (from ${m("G")}): ${m("\\left(\\frac{\\partial s}{\\partial P}\\right)_T = -\\left(\\frac{\\partial v}{\\partial T}\\right)_P = -v\\alpha")}.`,
      m(`-v\\alpha = -(${g(V)})(${g(a)}) = ${fmt(val)}\\,\\mathrm{J/(mol\\cdot K\\cdot Pa)}`),
    ], meta, `${liqStem(L)} Find the molar ${m("\\left(\\partial s/\\partial P\\right)_T")} (J/(mol·K·Pa) = m³/(mol·K)).`);
  }
  if (target === "dUdV") {
    const val = (T * a) / k - 1e5;
    return numeric(val, "(∂U/∂V)_T", "\\left(\\frac{\\partial U}{\\partial V}\\right)_T", "Pa", [
      `${m("dU = T\\,dS - P\\,dV")} at constant ${m("T")}: ${m("\\left(\\frac{\\partial U}{\\partial V}\\right)_T = T\\left(\\frac{\\partial S}{\\partial V}\\right)_T - P")}.`,
      `Maxwell: ${m("\\left(\\frac{\\partial S}{\\partial V}\\right)_T = \\left(\\frac{\\partial P}{\\partial T}\\right)_V = \\frac{\\alpha}{\\kappa_T}")}.`,
      m(`\\left(\\frac{\\partial U}{\\partial V}\\right)_T = \\frac{(${T})(${g(a)})}{${g(k)}} - 10^5 = ${fmt(val)}${u("Pa")}`),
    ], meta, `${liqStem(L)} Find the internal pressure ${m("\\left(\\partial U/\\partial V\\right)_T")} at ${m(`T = ${T}\\,\\mathrm{K}`)}.`);
  }
  if (target === "dHdP") {
    const val = V * (1 - T * a);
    return numeric(val, "(∂h/∂P)_T", "\\left(\\frac{\\partial h}{\\partial P}\\right)_T", "m³/mol", [
      `${m("dh = T\\,ds + v\\,dP")} at constant ${m("T")}: ${m("\\left(\\frac{\\partial h}{\\partial P}\\right)_T = T\\left(\\frac{\\partial s}{\\partial P}\\right)_T + v")}.`,
      `Maxwell: ${m("\\left(\\frac{\\partial s}{\\partial P}\\right)_T = -v\\alpha")}, so ${m("\\left(\\frac{\\partial h}{\\partial P}\\right)_T = v(1 - T\\alpha)")}.`,
      m(`v(1 - T\\alpha) = ${g(V)}(1 - ${T}\\times${g(a)}) = ${fmt(val)}\\,\\mathrm{J/(mol\\cdot Pa)}`),
    ], meta, `${liqStem(L)} Find the molar ${m("\\left(\\partial h/\\partial P\\right)_T")} at ${m(`T = ${T}\\,\\mathrm{K}`)} (J/(mol·Pa) = m³/mol).`);
  }
  const val = (T * V * a * a) / k;
  return numeric(val, "c_P − c_v", "c_P - c_v", "J/(mol·K)", [
    `${m("c_P - c_v = T\\left(\\frac{\\partial P}{\\partial T}\\right)_v\\left(\\frac{\\partial v}{\\partial T}\\right)_P")} (from ${m("s(T, v)")} and a Maxwell relation).`,
    `${m("\\left(\\frac{\\partial P}{\\partial T}\\right)_v = \\alpha/\\kappa_T")}, ${m("\\left(\\frac{\\partial v}{\\partial T}\\right)_P = v\\alpha")}, so ${m("c_P - c_v = \\frac{Tv\\alpha^2}{\\kappa_T}")}.`,
    m(`\\frac{(${T})(${g(V)})(${g(a)})^2}{${g(k)}} = ${fmt(val)}${u("J/(mol·K)")}`),
  ], meta, `${liqStem(L)} Find ${m("c_P - c_v")} at ${m(`T = ${T}\\,\\mathrm{K}`)}.`);
}

const EOS = [
  { id: "vdw", name: "van der Waals", P: "\\frac{RT}{V - b} - \\frac{a}{V^2}", dSdV: ["R/(V - b)", "\\frac{R}{V - b}"], dUdV: ["a/V^2", "\\frac{a}{V^2}"], dPdT: "\\frac{R}{V - b}" },
  { id: "berthelot", name: "Berthelot", P: "\\frac{RT}{V - b} - \\frac{a}{TV^2}", dSdV: ["R/(V - b) + a/(T^2*V^2)", "\\frac{R}{V - b} + \\frac{a}{T^2V^2}"], dUdV: ["2*a/(T*V^2)", "\\frac{2a}{TV^2}"], dPdT: "\\frac{R}{V - b} + \\frac{a}{T^2V^2}" },
  { id: "virial", name: "truncated virial", P: "\\frac{RT}{V} + \\frac{bRT - a}{V^2}", dSdV: ["R/V + b*R/V^2", "\\frac{R}{V} + \\frac{bR}{V^2}"], dUdV: ["a/V^2", "\\frac{a}{V^2}"], dPdT: "\\frac{R}{V} + \\frac{bR}{V^2}" },
  { id: "rk", name: "Redlich–Kwong", P: "\\frac{RT}{V - b} - \\frac{a}{\\sqrt{T}\\,V(V + b)}", dSdV: ["R/(V - b) + a/(2*T^(3/2)*V*(V + b))", "\\frac{R}{V - b} + \\frac{a}{2T^{3/2}V(V + b)}"], dUdV: ["3*a/(2*sqrt(T)*V*(V + b))", "\\frac{3a}{2\\sqrt{T}\\,V(V + b)}"], dPdT: "\\frac{R}{V - b} + \\frac{a}{2T^{3/2}V(V + b)}" },
];
function mxEos(r: Rng): Draft {
  const e = r.pick(EOS);
  const target = r.pick(["dSdV", "dUdV"] as const);
  const meta = { th: "mx-eos", eos: e.id, target };
  const vars = ["b", "a", "R", "T", "V"];
  const prompt = (what: string) => `One mole of a ${e.name} gas obeys ${m(`P = ${e.P}`)} (${m("V")} the molar volume, ${m("a, b > 0")}). Find ${what}.`;
  const mx = `Maxwell (from ${m("dF = -S\\,dT - P\\,dV")}): ${m("\\left(\\frac{\\partial S}{\\partial V}\\right)_T = \\left(\\frac{\\partial P}{\\partial T}\\right)_V")}.`;
  if (target === "dSdV")
    return symbolic(e.dSdV[0], e.dSdV[1], vars, "(∂S/∂V)_T", "\\left(\\frac{\\partial S}{\\partial V}\\right)_T", [
      mx,
      `Differentiate the equation of state at fixed ${m("V")}: ${m(`\\left(\\frac{\\partial P}{\\partial T}\\right)_V = ${e.dPdT}`)}.`,
    ], meta, prompt(m("\\left(\\partial S/\\partial V\\right)_T")));
  return symbolic(e.dUdV[0], e.dUdV[1], vars, "(∂U/∂V)_T", "\\left(\\frac{\\partial U}{\\partial V}\\right)_T", [
    `${m("dU = T\\,dS - P\\,dV")}, so ${m("\\left(\\frac{\\partial U}{\\partial V}\\right)_T = T\\left(\\frac{\\partial S}{\\partial V}\\right)_T - P")}.`,
    mx,
    m(`T\\left(\\frac{\\partial P}{\\partial T}\\right)_V - P = T\\left(${e.dPdT}\\right) - \\left(${e.P}\\right) = ${e.dUdV[1]}`),
  ], meta, prompt(`${m("\\left(\\partial U/\\partial V\\right)_T")} (the internal pressure)`));
}

function mxTriple(r: Rng): Draft {
  const L = r.pick(LIQUIDS);
  const dT = r.pick([1, 2, 5, 10]);
  const slope = L.alpha / L.kappa;
  const dP = (slope * dT) / 1e5;
  return numeric(dP, "ΔP", "\\Delta P", "bar", [
    `Triple product rule: ${m("\\left(\\frac{\\partial P}{\\partial T}\\right)_V\\left(\\frac{\\partial T}{\\partial V}\\right)_P\\left(\\frac{\\partial V}{\\partial P}\\right)_T = -1")}.`,
    `So ${m("\\left(\\frac{\\partial P}{\\partial T}\\right)_V = -\\frac{(\\partial V/\\partial T)_P}{(\\partial V/\\partial P)_T} = \\frac{\\alpha}{\\kappa_T} = \\frac{" + g(L.alpha) + "}{" + g(L.kappa) + "}")} ${m(`= ${fmt(slope)}${u("Pa/K")}`)}.`,
    m(`\\Delta P \\approx \\frac{\\alpha}{\\kappa_T}\\Delta T = ${fmt(slope)} \\times ${dT} = ${fmt(dP * 1e5)}\\,\\mathrm{Pa} = ${fmt(dP)}${u("bar")}`),
  ], { th: "mx-triple", alpha: L.alpha, kappa: L.kappa, V: L.V, T: L.T, Cp: L.Cp, dT },
  `A rigid, completely full sealed container holds ${L.name.replace(/ at \d+ K/, "")} (${m(`\\alpha = ${vu(L.alpha, "K⁻¹")}`)}, ${m(`\\kappa_T = ${vu(L.kappa, "Pa⁻¹")}`)}). It is warmed by ${m(`${dT}\\,\\mathrm{K}`)}. Treating ${m("\\alpha, \\kappa_T")} as constant, estimate the pressure rise in bar.`);
}

// ═══ stability ═════════════════════════════════════════════════════════════
const STAB_OPTIONS = ["Stable", "Unstable"];
const STAB_CASES: [Q, Q][] = [
  ...S_EXPS.slice(0, 6),
  [q(3, 2), q(-1, 2)], [q(2, 3), q(2, 3)], [q(2), q(-1, 2)], [q(1, 2), q(-1, 2)], [q(3, 4), q(1, 2)], [q(1, 3), q(4, 3)],
];
function stConcavity(r: Rng): Draft {
  const [ge, be] = r.pick(STAB_CASES);
  const ce = q(1).sub(ge).sub(be);
  const Suu = ge.mul(ge.sub(1));
  const Svv = be.mul(be.sub(1));
  const det = ge.mul(be).mul(ce); // det / (S²/U²V²)
  const stable = Suu.value() < 0 && det.value() > 0;
  const fail = Suu.value() >= 0 ? "S_UU" : Svv.value() >= 0 ? "S_VV" : "det";
  const Stex = `S = A\\,${prod(pw("U", ge), pw("V", be), pw("N", ce))}`;
  const correct = STAB_OPTIONS[stable ? 0 : 1];
  return choice(STAB_OPTIONS, correct, `\\text{${correct}}`, [
    `Stability at fixed ${m("N")} needs ${m("S(U, V)")} concave: ${m("S_{UU} < 0")} (so ${m("C_V > 0")}), ${m("S_{VV} < 0")}, and ${m("S_{UU}S_{VV} - S_{UV}^2 > 0")}.`,
    `${m(`S_{UU} = ${Suu.tex()}\\,\\frac{S}{U^2}`)}, ${m(`S_{VV} = ${Svv.tex()}\\,\\frac{S}{V^2}`)}, ${m(`S_{UV} = ${ge.mul(be).tex()}\\,\\frac{S}{UV}`)}.`,
    `${m(`S_{UU}S_{VV} - S_{UV}^2 = ${det.tex()}\\,\\frac{S^2}{U^2V^2}`)}.`,
    stable ? "All three hold: stable." : `Fails: ${fail === "S_UU" ? m("S_{UU} \\ge 0") + " (negative heat capacity)" : fail === "S_VV" ? m("S_{VV} \\ge 0") : "the Hessian determinant is negative"} — unstable.`,
  ], { th: "st-concave", g: qm(ge), b: qm(be), c: qm(ce), stable },
  `Is a system with fundamental equation ${m(Stex)} (${m("A > 0")}) thermodynamically stable for all ${m("U, V > 0")}?`);
}

function stCv(r: Rng): Draft {
  const [ge, be] = r.pick(S_EXPS);
  const ce = q(1).sub(ge).sub(be);
  const Stex = `S = A\\,${prod(pw("U", ge), pw("V", be), pw("N", ce))}`;
  const inv = q(1).div(q(1).sub(ge));
  const Utex = `\\left(${ge.tex()}A\\,${prod("T", pw("V", be), pw("N", ce))}\\right)^{${qs(inv)}}`;
  const kk = inv; // C_V = U / ((1−g) T)
  const tex = `${kk.tex()}\\,\\frac{${Utex}}{T}`;
  const ref = `${kk.js()}*(${ge.js()}*A*T*V^${be.js()}*N^${ce.js()})^${inv.js()}/T`;
  return symbolic(ref, tex, ["T", "V", "N", "A"], "C_V", "C_V", [
    `${m(`\\frac1T = \\frac{\\partial S}{\\partial U} = ${ge.tex()}\\frac SU`)}, so ${m(`${pw("U", q(1).sub(ge))} = ${ge.tex()}A\\,${prod("T", pw("V", be), pw("N", ce))}`)} and ${m(`U = ${Utex}`)}.`,
    `${m("C_V = (\\partial U/\\partial T)_{V,N}")}: ${m("U \\propto T^{" + qs(inv) + "}")}, so ${m(`C_V = ${inv.tex()}\\,\\frac UT`)}.`,
    `${m(`C_V = ${tex}`)} > 0 ✓ — consistent with ${m("S_{UU} < 0")}.`,
  ], { th: "st-cv", g: qm(ge), b: qm(be), c: qm(ce) },
  `A model system has ${m(Stex)} (${m("A > 0")}). Find its heat capacity ${m("C_V(T, V, N)")}.`);
}

const VDW = [
  { name: "CO₂", tex: "\\mathrm{CO_2}", a: 0.364, b: 4.267e-5 },
  { name: "N₂", tex: "\\mathrm{N_2}", a: 0.137, b: 3.87e-5 },
  { name: "Ar", tex: "\\mathrm{Ar}", a: 0.1355, b: 3.2e-5 },
  { name: "CH₄", tex: "\\mathrm{CH_4}", a: 0.2283, b: 4.278e-5 },
  { name: "H₂O", tex: "\\mathrm{H_2O}", a: 0.5536, b: 3.049e-5 },
  { name: "NH₃", tex: "\\mathrm{NH_3}", a: 0.4225, b: 3.707e-5 },
];
const vdwGiven = (G: (typeof VDW)[number]) =>
  `${m(`a = ${g(G.a)}\\,\\mathrm{Pa\\,m^6/mol^2}`)}, ${m(`b = ${vu(G.b, "m³/mol")}`)}`;
const dPdVvdw = (a: number, b: number, T: number, V: number) => -(R * T) / (V - b) ** 2 + (2 * a) / V ** 3;
const STAB2 = ["Stable (κ_T > 0)", "Unstable (κ_T < 0)"];

function stVdwStable(r: Rng): Draft {
  const G = r.pick(VDW);
  const Tc = (8 * G.a) / (27 * R * G.b);
  const T = Math.round(Tc * r.pick([0.8, 0.85, 0.9, 0.95, 1.1]));
  const V = r3(3 * G.b * r.pick([0.5, 0.6, 0.8, 1.0, 1.2, 1.5, 2.5, 4, 8]));
  const d = dPdVvdw(G.a, G.b, T, V);
  const scale = (R * T) / (V - G.b) ** 2;
  require_(V > 1.2 * G.b && Math.abs(d) > 0.05 * scale);
  const stable = d < 0;
  const correct = STAB2[stable ? 0 : 1];
  return choice(STAB2, correct, `\\text{${stable ? "Stable" : "Unstable"}}`, [
    `Mechanical stability: ${m("\\kappa_T = -\\frac1V\\left(\\frac{\\partial V}{\\partial P}\\right)_T > 0")}, i.e. ${m("\\left(\\frac{\\partial P}{\\partial V}\\right)_T < 0")}.`,
    `van der Waals, molar: ${m("\\left(\\frac{\\partial P}{\\partial V}\\right)_T = -\\frac{RT}{(V - b)^2} + \\frac{2a}{V^3}")}.`,
    m(`= -\\frac{(8.314)(${T})}{(${g(V)} - ${g(G.b)})^2} + \\frac{2(${g(G.a)})}{(${g(V)})^3} = ${fmt(d)}\\,\\mathrm{Pa\\,mol/m^3}`),
    stable ? "Negative: stable." : "Positive: the fluid would expand when squeezed — inside the spinodal, unstable (it splits into liquid + vapor).",
  ], { th: "st-vdw", a: G.a, b: G.b, T, V, stable },
  `Model ${G.name} as a van der Waals fluid (${vdwGiven(G)}). Is a homogeneous state at ${m(`T = ${T}\\,\\mathrm{K}`)} with molar volume ${m(`V = ${vu(V, "m³/mol")}`)} mechanically stable?`);
}

function stVdwTc(r: Rng): Draft {
  const G = r.pick(VDW);
  const Tc = (8 * G.a) / (27 * R * G.b);
  return numeric(Tc, "T_c", "T_c", "K", [
    `The stability limit ${m("(\\partial P/\\partial V)_T = 0")} first appears at the critical point, where also ${m("(\\partial^2 P/\\partial V^2)_T = 0")}.`,
    `${m("-\\frac{RT}{(V-b)^2} + \\frac{2a}{V^3} = 0")} and ${m("\\frac{2RT}{(V-b)^3} - \\frac{6a}{V^4} = 0")}. Divide: ${m("V_c = 3b")}; back-substitute: ${m("T_c = \\frac{8a}{27Rb}")}.`,
    m(`T_c = \\frac{8(${g(G.a)})}{27(8.314)(${g(G.b)})} = ${fmt(Tc)}${u("K")}`),
  ], { th: "st-tc", a: G.a, b: G.b },
  `Model ${G.name} as a van der Waals fluid (${vdwGiven(G)}). Find the temperature above which every homogeneous state is mechanically stable (the critical temperature).`);
}

function stVdwKappa(r: Rng): Draft {
  const G = r.pick(VDW);
  const Tc = (8 * G.a) / (27 * R * G.b);
  const T = Math.round(Tc * r.pick([1.1, 1.3, 1.5, 2]));
  const V = r3(3 * G.b * r.pick([2, 4, 8, 20, 50]));
  const d = dPdVvdw(G.a, G.b, T, V);
  const kappa = -1 / (V * d);
  require_(kappa > 0);
  return numeric(kappa, "κ_T", "\\kappa_T", "Pa⁻¹", [
    `${m("\\kappa_T = -\\frac1V\\left(\\frac{\\partial V}{\\partial P}\\right)_T = -\\frac{1}{V\\,(\\partial P/\\partial V)_T}")}.`,
    m(`\\left(\\frac{\\partial P}{\\partial V}\\right)_T = -\\frac{RT}{(V - b)^2} + \\frac{2a}{V^3} = ${fmt(d)}\\,\\mathrm{Pa\\,mol/m^3}`),
    m(`\\kappa_T = -\\frac{1}{(${g(V)})(${fmt(d)})} = ${fmt(kappa)}${u("Pa⁻¹")}`),
  ], { th: "st-kappa", a: G.a, b: G.b, T, V },
  `Model ${G.name} as a van der Waals fluid (${vdwGiven(G)}). Find the isothermal compressibility ${m("\\kappa_T")} at ${m(`T = ${T}\\,\\mathrm{K}`)} and molar volume ${m(`V = ${vu(V, "m³/mol")}`)}.`);
}

// ═══ phase equilibrium ═════════════════════════════════════════════════════
const LIQ_VAP = [
  { name: "water", dH: 40660, Tb: 373.15 },
  { name: "ethanol", dH: 38560, Tb: 351.4 },
  { name: "benzene", dH: 30720, Tb: 353.2 },
  { name: "acetone", dH: 29100, Tb: 329.2 },
  { name: "methanol", dH: 35210, Tb: 337.8 },
  { name: "diethyl ether", dH: 26520, Tb: 307.6 },
  { name: "n-hexane", dH: 28850, Tb: 341.9 },
];
const CC = `Clausius–Clapeyron (vapor ideal, liquid volume neglected, ${m("\\Delta H_{vap}")} constant): ${m("\\frac{d\\ln P}{dT} = \\frac{\\Delta H_{vap}}{RT^2}")}, so ${m("\\ln\\frac{P_2}{P_1} = -\\frac{\\Delta H_{vap}}{R}\\left(\\frac{1}{T_2} - \\frac{1}{T_1}\\right)")}.`;

function peCCPressure(r: Rng): Draft {
  const L = r.pick(LIQ_VAP);
  const T2 = r4(L.Tb - r.pick([10, 20, 25, 30, 40, 50]));
  const P2 = 101.325 * Math.exp((-L.dH / R) * (1 / T2 - 1 / L.Tb));
  return numeric(P2, "P", "P", "kPa", [
    CC,
    m(`\\ln\\frac{P_2}{101.325} = -\\frac{${L.dH}}{8.314}\\left(\\frac{1}{${g(T2)}} - \\frac{1}{${gT(L.Tb)}}\\right) = ${fmt(Math.log(P2 / 101.325), 4)}`),
    m(`P_2 = 101.325\\,e^{${fmt(Math.log(P2 / 101.325), 4)}} = ${fmt(P2)}${u("kPa")}`),
  ], { th: "pe-P", dH: L.dH, T1: L.Tb, P1: 101325, T2 },
  `${L.name[0].toUpperCase() + L.name.slice(1)} boils at ${m(`${gT(L.Tb)}${u("K")}`)} at ${m("1\\,\\mathrm{atm} = 101.325\\,\\mathrm{kPa}")}, with ${m(`\\Delta H_{vap} = ${vu(L.dH, "J/mol")}`)}. Estimate its vapor pressure at ${m(vu(T2, "K"))}.`);
}

function peCCEnthalpy(r: Rng): Draft {
  const L = r.pick(LIQ_VAP);
  const T1 = r4(L.Tb - r.pick([30, 40, 50]));
  const T2 = r4(L.Tb - r.pick([0, 5, 10]));
  const p = (T: number) => r4(101.325 * Math.exp((-L.dH / R) * (1 / T - 1 / L.Tb)));
  const P1 = p(T1), P2 = p(T2);
  const dH = (R * Math.log(P2 / P1)) / (1 / T1 - 1 / T2) / 1000;
  return numeric(dH, "ΔH_vap", "\\Delta H_{vap}", "kJ/mol", [
    CC,
    `Solve for ${m("\\Delta H_{vap}")}: ${m("\\Delta H_{vap} = \\frac{R\\ln(P_2/P_1)}{1/T_1 - 1/T_2}")}.`,
    m(`\\Delta H_{vap} = \\frac{8.314\\ln(${g(P2)}/${g(P1)})}{1/${g(T1)} - 1/${g(T2)}} = ${fmt(dH * 1000)}\\,\\mathrm{J/mol} = ${fmt(dH)}${u("kJ/mol")}`),
  ], { th: "pe-dH", T1, P1: P1 * 1000, T2, P2: P2 * 1000 },
  `The vapor pressure of ${L.name} is ${m(vu(P1, "kPa"))} at ${m(vu(T1, "K"))} and ${m(vu(P2, "kPa"))} at ${m(vu(T2, "K"))}. Estimate ${m("\\Delta H_{vap}")} in kJ/mol.`);
}

function peCCTemperature(r: Rng): Draft {
  const L = r.pick(LIQ_VAP);
  const P2 = r.pick([50, 60, 70, 80, 90, 150, 200]);
  const T2 = 1 / (1 / L.Tb - (R * Math.log(P2 / 101.325)) / L.dH);
  return numeric(T2, "T_b", "T_b", "K", [
    CC,
    `Solve for ${m("T_2")}: ${m("\\frac{1}{T_2} = \\frac{1}{T_1} - \\frac{R}{\\Delta H_{vap}}\\ln\\frac{P_2}{P_1}")}.`,
    m(`\\frac{1}{T_2} = \\frac{1}{${gT(L.Tb)}} - \\frac{8.314}{${L.dH}}\\ln\\frac{${P2}}{101.325} = ${fmt(1 / T2, 5)}\\,\\mathrm{K^{-1}} \\Rightarrow T_2 = ${fmt(T2)}${u("K")}`),
  ], { th: "pe-T", dH: L.dH, T1: L.Tb, P1: 101325, P2: P2 * 1000 },
  `${L.name[0].toUpperCase() + L.name.slice(1)} boils at ${m(`${gT(L.Tb)}${u("K")}`)} at ${m("101.325\\,\\mathrm{kPa}")} (${m(`\\Delta H_{vap} = ${vu(L.dH, "J/mol")}`)}). At what temperature does it boil when the pressure is ${m(vu(P2, "kPa"))}?`);
}

const MELT = [
  { name: "ice → water", dH: 6010, T: 273.15, dV: -1.634e-6 },
  { name: "solid → liquid benzene", dH: 9870, T: 278.7, dV: 1.08e-5 },
  { name: "solid → liquid mercury", dH: 2290, T: 234.3, dV: 5.17e-7 },
  { name: "solid → liquid gallium", dH: 5590, T: 302.9, dV: -4.0e-7 },
];
function peClapeyron(r: Rng): Draft {
  const variant = r.pick(["melt-slope", "melt-shift", "vap-slope"] as const);
  if (variant === "vap-slope") {
    const L = r.pick(LIQ_VAP);
    const slope = (L.dH * 101325) / (R * L.Tb ** 2);
    return numeric(slope, "dP/dT", "\\frac{dP}{dT}", "Pa/K", [
      `Clapeyron: ${m("\\frac{dP}{dT} = \\frac{\\Delta H}{T\\Delta V}")} (from ${m("d\\mu_l = d\\mu_g")} along the coexistence line).`,
      `Vapor ideal, liquid volume negligible: ${m("\\Delta V \\approx RT/P")}, so ${m("\\frac{dP}{dT} = \\frac{\\Delta H_{vap}P}{RT^2}")}.`,
      m(`\\frac{dP}{dT} = \\frac{(${L.dH})(101\\,325)}{(8.314)(${gT(L.Tb)})^2} = ${fmt(slope)}${u("Pa/K")}`),
    ], { th: "pe-slope", phase: "vap", dH: L.dH, T: L.Tb, P: 101325 },
    `Find the slope ${m("dP/dT")} of the vapor-pressure curve of ${L.name} at its normal boiling point ${m(`${gT(L.Tb)}${u("K")}`)} (${m(`\\Delta H_{vap} = ${vu(L.dH, "J/mol")}`)}).`);
  }
  const M = r.pick(MELT);
  const slope = M.dH / (M.T * M.dV);
  const clap = `Clapeyron: ${m("\\frac{dP}{dT} = \\frac{\\Delta S}{\\Delta V} = \\frac{\\Delta H}{T\\Delta V}")} (from ${m("d\\mu_s = d\\mu_l")}: ${m("-s_s\\,dT + v_s\\,dP = -s_l\\,dT + v_l\\,dP")}).`;
  const given = `For ${M.name} at ${m(`${gT(M.T)}${u("K")}`)} and 1 bar: ${m(`\\Delta H_{fus} = ${vu(M.dH, "J/mol")}`)}, ${m(`\\Delta V_{fus} = ${vu(M.dV, "m³/mol")}`)}.`;
  if (variant === "melt-slope")
    return numeric(slope, "dP/dT", "\\frac{dP}{dT}", "Pa/K", [
      clap,
      m(`\\frac{dP}{dT} = \\frac{${M.dH}}{(${gT(M.T)})(${g(M.dV)})} = ${fmt(slope)}${u("Pa/K")}`),
      M.dV < 0 ? "Negative: squeezing it lowers the melting point (the liquid is denser)." : "Positive: pressure raises the melting point.",
    ], { th: "pe-slope", phase: "melt", dH: M.dH, T: M.T, dV: M.dV }, `${given} Find the slope ${m("dP/dT")} of the melting curve.`);
  const dPbar = r.pick([50, 100, 200, 500]);
  const dTm = (dPbar * 1e5) / slope;
  return numeric(dTm, "ΔT_m", "\\Delta T_m", "K", [
    clap,
    m(`\\frac{dP}{dT} = \\frac{${M.dH}}{(${gT(M.T)})(${g(M.dV)})} = ${fmt(slope)}${u("Pa/K")}`),
    m(`\\Delta T_m \\approx \\frac{\\Delta P}{dP/dT} = \\frac{${dPbar}\\times10^5}{${fmt(slope)}} = ${fmt(dTm)}${u("K")}`),
  ], { th: "pe-shift", dH: M.dH, T: M.T, dV: M.dV, dP: dPbar * 1e5 },
  `${given} By how much does the melting temperature change if the pressure is raised by ${m(vu(dPbar, "bar"))}? (Give the signed change.)`);
}

// ═══ solutions ═════════════════════════════════════════════════════════════
function soMixEntropy(r: Rng): Draft {
  const nA = r.pick([0.5, 1, 1.5, 2, 3]);
  const nB = r.pick([0.5, 1, 2, 2.5, 4]);
  const n = nA + nB, xA = nA / n, xB = nB / n;
  const dS = -R * (nA * Math.log(xA) + nB * Math.log(xB));
  return numeric(dS, "ΔS_mix", "\\Delta S_{mix}", "J/K", [
    `Ideal mixing: ${m("\\Delta S_{mix} = -R\\sum_i n_i\\ln x_i")} (each component spreads into the whole volume).`,
    `${m(`x_A = ${fmt(xA, 4)}`)}, ${m(`x_B = ${fmt(xB, 4)}`)}.`,
    m(`\\Delta S_{mix} = -8.314\\left[${g(nA)}\\ln ${fmt(xA, 4)} + ${g(nB)}\\ln ${fmt(xB, 4)}\\right] = ${fmt(dS)}${u("J/K")}`),
  ], { th: "so-dS", nA, nB },
  `${m(vu(nA, "mol"))} of liquid A and ${m(vu(nB, "mol"))} of liquid B form an ideal solution. Find ${m("\\Delta S_{mix}")}.`);
}

function soMixGibbs(r: Rng): Draft {
  const nA = r.pick([0.5, 1, 2, 3]);
  const nB = r.pick([1, 1.5, 2, 4]);
  const T = r.pick([298, 300, 310, 350]);
  const n = nA + nB, xA = nA / n, xB = nB / n;
  const dG = R * T * (nA * Math.log(xA) + nB * Math.log(xB));
  return numeric(dG, "ΔG_mix", "\\Delta G_{mix}", "J", [
    `Ideal solution: ${m("\\mu_i = \\mu_i^* + RT\\ln x_i")}, so ${m("\\Delta G_{mix} = \\sum_i n_i(\\mu_i - \\mu_i^*) = RT\\sum_i n_i\\ln x_i")}.`,
    `${m(`x_A = ${fmt(xA, 4)}`)}, ${m(`x_B = ${fmt(xB, 4)}`)}.`,
    m(`\\Delta G_{mix} = (8.314)(${T})\\left[${g(nA)}\\ln ${fmt(xA, 4)} + ${g(nB)}\\ln ${fmt(xB, 4)}\\right] = ${fmt(dG)}${u("J")}`),
  ], { th: "so-dG", nA, nB, T },
  `${m(vu(nA, "mol"))} of A and ${m(vu(nB, "mol"))} of B mix to form an ideal solution at ${m(`${T}\\,\\mathrm{K}`)}. Find ${m("\\Delta G_{mix}")}.`);
}

const PAIRS = [
  { A: "benzene", B: "toluene", PA: 12.7, PB: 3.79 },
  { A: "n-hexane", B: "n-heptane", PA: 20.2, PB: 6.09 },
  { A: "methanol", B: "ethanol", PA: 16.9, PB: 7.87 },
  { A: "acetone", B: "chloroform", PA: 30.8, PB: 26.2 },
];
function soRaoult(r: Rng): Draft {
  const p = r.pick(PAIRS);
  const xA = r.pick([0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8]);
  const pA = xA * p.PA, pB = (1 - xA) * p.PB, P = pA + pB;
  const target = r.pick(["P", "y"] as const);
  const meta = { th: "so-raoult", xA, PA: p.PA * 1000, PB: p.PB * 1000, target };
  const stem = `A liquid mixture of ${p.A} (${m(`x_A = ${xA}`)}) and ${p.B} behaves ideally at 298 K, where ${m(`P_A^* = ${vu(p.PA, "kPa")}`)} and ${m(`P_B^* = ${vu(p.PB, "kPa")}`)}.`;
  const s1 = `Raoult: ${m("p_i = x_iP_i^*")} (from ${m("\\mu_i^{liq} = \\mu_i^* + RT\\ln x_i = \\mu_i^{vap}")}).`;
  const s2 = m(`p_A = ${xA}(${p.PA}) = ${fmt(pA, 4)},\\quad p_B = ${fmt(1 - xA, 3)}(${p.PB}) = ${fmt(pB, 4)}\\,\\mathrm{kPa}`);
  if (target === "P")
    return numeric(P, "P", "P", "kPa", [s1, s2, m(`P = p_A + p_B = ${fmt(P)}${u("kPa")}`)], meta, `${stem} Find the total vapor pressure.`);
  return numeric(pA / P, "y_A", "y_A", "", [s1, s2, `Dalton: ${m(`y_A = p_A/P = ${fmt(pA, 4)}/${fmt(P, 4)} = ${fmt(pA / P)}`)} — the vapor is richer in the more volatile component.`], meta,
    `${stem} Find the mole fraction ${m("y_A")} of ${p.A} in the vapor.`);
}

const HENRY = [
  { gas: "O₂", tex: "\\mathrm{O_2}", K: 4.34e4 },
  { gas: "N₂", tex: "\\mathrm{N_2}", K: 8.65e4 },
  { gas: "CO₂", tex: "\\mathrm{CO_2}", K: 1.65e3 },
  { gas: "CH₄", tex: "\\mathrm{CH_4}", K: 4.13e4 },
  { gas: "He", tex: "\\mathrm{He}", K: 1.45e5 },
];
function soHenry(r: Rng): Draft {
  const H = r.pick(HENRY);
  const target = r.pick(["x", "p"] as const);
  const s0 = `Henry's law for a dilute solute: ${m("p_i = K_H x_i")} (the solute's ${m("\\mu_i")} in solution is ${m("\\mu_i^\\dagger + RT\\ln x_i")}, referenced to infinite dilution).`;
  if (target === "x") {
    const p = r.pick([0.21, 0.5, 0.79, 1, 2, 5]);
    const x = p / H.K;
    return numeric(x, "x", `x_{${H.tex}}`, "", [s0, m(`x = \\frac{p}{K_H} = \\frac{${p}}{${g(H.K)}} = ${fmt(x)}`)], { th: "so-henry", K: H.K * 1e5, p: p * 1e5, target },
      `The Henry's-law constant of ${H.gas} in water at 298 K is ${m(`K_H = ${vu(H.K, "bar")}`)} (mole-fraction basis). Find the mole fraction of dissolved ${H.gas} at a partial pressure of ${m(vu(p, "bar"))}.`);
  }
  const x = r.pick([1e-5, 2e-5, 5e-5, 1e-4, 2.5e-4]);
  const p = H.K * x;
  return numeric(p, "p", `p_{${H.tex}}`, "bar", [s0, m(`p = K_H x = (${g(H.K)})(${g(x)}) = ${fmt(p)}${u("bar")}`)], { th: "so-henry", K: H.K * 1e5, x, target },
    `The Henry's-law constant of ${H.gas} in water at 298 K is ${m(`K_H = ${vu(H.K, "bar")}`)} (mole-fraction basis). What partial pressure of ${H.gas} gives a dissolved mole fraction of ${m(g(x))}?`);
}

function soActivity(r: Rng): Draft {
  const variant = r.pick(["measured", "margules"] as const);
  if (variant === "measured") {
    const p = r.pick(PAIRS);
    const xA = r.pick([0.2, 0.3, 0.4, 0.5, 0.6]);
    const gam = r.pick([0.6, 0.75, 0.85, 1.2, 1.4, 1.8, 2.3]);
    const pA = r4(gam * xA * p.PA);
    const gv = pA / (xA * p.PA);
    return numeric(gv, "γ_A", "\\gamma_A", "", [
      `Nonideal liquid: ${m("\\mu_A = \\mu_A^* + RT\\ln a_A")}, ${m("a_A = \\gamma_Ax_A")}; equating with the ideal vapor gives ${m("p_A = \\gamma_Ax_AP_A^*")}.`,
      m(`\\gamma_A = \\frac{p_A}{x_AP_A^*} = \\frac{${g(pA)}}{(${xA})(${p.PA})} = ${fmt(gv)}`),
      gv > 1 ? "γ > 1: positive deviation from Raoult (A–B attractions weaker than A–A, B–B)." : "γ < 1: negative deviation from Raoult (A–B attractions stronger).",
    ], { th: "so-gamma", xA, PA: p.PA * 1000, pA: pA * 1000 },
    `In a mixture with ${p.B} at 298 K, ${p.A} has ${m(`x_A = ${xA}`)} and partial vapor pressure ${m(vu(pA, "kPa"))}. Its pure vapor pressure is ${m(vu(p.PA, "kPa"))}. Find the activity coefficient ${m("\\gamma_A")}.`);
  }
  const W = r.pick([-3000, -2000, -1000, 1000, 1500, 2500, 4000]);
  const T = r.pick([298, 300, 320, 350]);
  const xA = r.pick([0.1, 0.2, 0.3, 0.5, 0.7, 0.8]);
  const gam = Math.exp((W * (1 - xA) ** 2) / (R * T));
  return numeric(gam, "γ_A", "\\gamma_A", "", [
    `Regular (two-suffix Margules) solution: ${m("G^{ex} = W\\,n\\,x_Ax_B")} with ${m("n = n_A + n_B")}.`,
    `${m("RT\\ln\\gamma_A = \\left(\\frac{\\partial G^{ex}}{\\partial n_A}\\right)_{T,P,n_B} = Wx_B^2")}.`,
    m(`\\gamma_A = \\exp\\frac{(${W})(${fmt(1 - xA, 3)})^2}{(8.314)(${T})} = ${fmt(gam)}`),
  ], { th: "so-margules", W, T, xA },
  `A binary liquid follows the regular-solution model ${m("G^{ex}/n = W x_Ax_B")} with ${m(`W = ${vu(W, "J/mol")}`)}. Find ${m("\\gamma_A")} at ${m(`x_A = ${xA}`)} and ${m(`${T}\\,\\mathrm{K}`)}.`);
}

// ═══ chemical equilibrium ══════════════════════════════════════════════════
const KDG = `${m("\\Delta G^\\circ = -RT\\ln K")} (at equilibrium ${m("\\Delta G = \\Delta G^\\circ + RT\\ln Q = 0")} with ${m("Q = K")}).`;
function ceK(r: Rng): Draft {
  const dG = r.pick([-30, -20, -15, -10, -8, -5, -2, 3, 5, 8, 12, 20, 25]);
  const T = r.pick([298, 300, 350, 400, 500]);
  const K = Math.exp((-dG * 1000) / (R * T));
  return numeric(K, "K", "K", "", [
    KDG,
    m(`K = \\exp\\left(-\\frac{\\Delta G^\\circ}{RT}\\right) = \\exp\\left(-\\frac{${dG * 1000}}{(8.314)(${T})}\\right) = ${fmt(K)}`),
  ], { th: "ce-K", dG: dG * 1000, T },
  `A gas-phase reaction has ${m(`\\Delta G^\\circ = ${vu(dG, "kJ/mol")}`)} at ${m(`${T}\\,\\mathrm{K}`)}. Find its equilibrium constant ${m("K")}.`);
}

function ceDG(r: Rng): Draft {
  const K = r.pick([1.5e-4, 3.2e-3, 0.045, 0.25, 4.7, 18, 360, 2.4e4, 6.1e5]);
  const T = r.pick([298, 300, 350, 400, 500, 700]);
  const dG = (-R * T * Math.log(K)) / 1000;
  return numeric(dG, "ΔG°", "\\Delta G^\\circ", "kJ/mol", [
    KDG,
    m(`\\Delta G^\\circ = -(8.314)(${T})\\ln(${g(K)}) = ${fmt(dG * 1000)}\\,\\mathrm{J/mol} = ${fmt(dG)}${u("kJ/mol")}`),
    K > 1 ? `${m("K > 1")} so ${m("\\Delta G^\\circ < 0")}: products favored at standard state.` : `${m("K < 1")} so ${m("\\Delta G^\\circ > 0")}.`,
  ], { th: "ce-dG", K, T },
  `A reaction has ${m(`K = ${g(K)}`)} at ${m(`${T}\\,\\mathrm{K}`)}. Find ${m("\\Delta G^\\circ")} in kJ/mol.`);
}

function ceVantHoff(r: Rng): Draft {
  const dH = r.pick([-120, -92.2, -57.2, -41.2, -20, 30, 58, 90, 131.3, 178]);
  const T1 = r.pick([298, 300, 400]);
  const T2 = T1 + r.pick([-25, 25, 50, 100, 200]);
  const K1 = r.pick([0.015, 0.12, 0.5, 2.5, 14, 85, 1.6e3]);
  const target = r.pick(["K2", "dH"] as const);
  const vh = `van 't Hoff: ${m("\\frac{d\\ln K}{dT} = \\frac{\\Delta H^\\circ}{RT^2}")} (Gibbs–Helmholtz on ${m("-\\Delta G^\\circ/RT")}); for constant ${m("\\Delta H^\\circ")}, ${m("\\ln\\frac{K_2}{K_1} = -\\frac{\\Delta H^\\circ}{R}\\left(\\frac{1}{T_2} - \\frac{1}{T_1}\\right)")}.`;
  const K2 = K1 * Math.exp((-dH * 1000 / R) * (1 / T2 - 1 / T1));
  if (target === "K2")
    return numeric(K2, "K₂", "K_2", "", [
      vh,
      m(`\\ln\\frac{K_2}{${g(K1)}} = -\\frac{${dH * 1000}}{8.314}\\left(\\frac{1}{${T2}} - \\frac{1}{${T1}}\\right) = ${fmt(Math.log(K2 / K1), 4)}`),
      m(`K_2 = ${g(K1)}\\,e^{${fmt(Math.log(K2 / K1), 4)}} = ${fmt(K2)}`),
    ], { th: "ce-vh", dH: dH * 1000, T1, T2, K1, target },
    `A reaction has ${m(`K = ${g(K1)}`)} at ${m(`${T1}\\,\\mathrm{K}`)} and ${m(`\\Delta H^\\circ = ${vu(dH, "kJ/mol")}`)}, roughly constant. Find ${m("K")} at ${m(`${T2}\\,\\mathrm{K}`)}.`);
  const K2g = r3(K2);
  require_(Math.abs(Math.log(K2g / K1)) > 0.05);
  const dHv = (-R * Math.log(K2g / K1)) / (1 / T2 - 1 / T1) / 1000;
  return numeric(dHv, "ΔH°", "\\Delta H^\\circ", "kJ/mol", [
    vh,
    m(`\\Delta H^\\circ = -\\frac{R\\ln(K_2/K_1)}{1/T_2 - 1/T_1} = -\\frac{8.314\\ln(${g(K2g)}/${g(K1)})}{1/${T2} - 1/${T1}} = ${fmt(dHv)}${u("kJ/mol")}`),
  ], { th: "ce-vh", T1, T2, K1, K2: K2g, target },
  `An equilibrium constant is ${m(g(K1))} at ${m(`${T1}\\,\\mathrm{K}`)} and ${m(g(K2g))} at ${m(`${T2}\\,\\mathrm{K}`)}. Assuming constant ${m("\\Delta H^\\circ")}, find it in kJ/mol.`);
}

const RXNS = [
  { id: "A=2B", tex: "\\mathrm{N_2O_4(g) \\rightleftharpoons 2\\,NO_2(g)}", start: "N₂O₄", Kexpr: "K = \\frac{(2\\xi)^2}{(n_0 - \\xi)(n_0 + \\xi)}\\frac{P}{P^\\circ}" },
  { id: "A=B+C", tex: "\\mathrm{PCl_5(g) \\rightleftharpoons PCl_3(g) + Cl_2(g)}", start: "PCl₅", Kexpr: "K = \\frac{\\xi^2}{(n_0 - \\xi)(n_0 + \\xi)}\\frac{P}{P^\\circ}" },
  { id: "A+B=2C", tex: "\\mathrm{H_2(g) + I_2(g) \\rightleftharpoons 2\\,HI(g)}", start: "H₂ and I₂", Kexpr: "K = \\frac{(2\\xi)^2}{(n_0 - \\xi)^2}" },
];
function ceExtent(r: Rng): Draft {
  const rx = r.pick(RXNS);
  const n0 = r.pick([1, 2, 0.5]);
  const f = r.pick([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]);
  const P = rx.id === "A+B=2C" ? 1 : r.pick([0.5, 1, 2, 5]);
  const Kexact = rx.id === "A=2B" ? (4 * f * f * P) / (1 - f * f) : rx.id === "A=B+C" ? (f * f * P) / (1 - f * f) : (4 * f * f) / ((1 - f) * (1 - f));
  const K = r3(Kexact);
  const xi = rx.id === "A=2B" ? n0 * Math.sqrt(K / (K + 4 * P)) : rx.id === "A=B+C" ? n0 * Math.sqrt(K / (K + P)) : (n0 * Math.sqrt(K)) / (2 + Math.sqrt(K));
  const solve = rx.id === "A=2B" ? `\\xi = n_0\\sqrt{\\frac{K}{K + 4P/P^\\circ}}` : rx.id === "A=B+C" ? `\\xi = n_0\\sqrt{\\frac{K}{K + P/P^\\circ}}` : `\\frac{2\\xi}{n_0 - \\xi} = \\sqrt K \\Rightarrow \\xi = \\frac{n_0\\sqrt K}{2 + \\sqrt K}`;
  const table = rx.id === "A+B=2C" ? `${m("n_{H_2} = n_{I_2} = n_0 - \\xi")}, ${m("n_{HI} = 2\\xi")}; total stays ${m("2n_0")}, so ${m("P")} cancels.` : `Moles: reactant ${m("n_0 - \\xi")}, products ${rx.id === "A=2B" ? m("2\\xi") : m("\\xi,\\ \\xi")}; total ${m("n_0 + \\xi")}; ${m("p_i = (n_i/n)P")}.`;
  return numeric(xi, "ξ", "\\xi", "mol", [
    `Equilibrium: ${m("\\sum_i\\nu_i\\mu_i = 0")} with ${m("\\mu_i = \\mu_i^\\circ + RT\\ln(p_i/P^\\circ)")} gives ${m("K = \\prod_i(p_i/P^\\circ)^{\\nu_i}")}.`,
    table,
    m(rx.Kexpr),
    `Solve: ${m(solve)} ${m(`= ${fmt(xi)}\\,\\mathrm{mol}`)}.`,
  ], { th: "ce-extent", rx: rx.id, n0, P, K },
  `For ${m(rx.tex)}, ${m(`K = ${g(K)}`)} (standard state ${m("P^\\circ = 1\\,\\mathrm{bar}")}). Starting from ${m(vu(n0, "mol"))} ${rx.id === "A+B=2C" ? "each" : "of"} ${rx.start} only, at a total pressure of ${m(vu(P, "bar"))}, find the equilibrium extent of reaction ${m("\\xi")}.`);
}

const DIR = ["Forward (toward products)", "Reverse (toward reactants)", "Already at equilibrium"];
function ceDirection(r: Rng): Draft {
  const dG = r.pick([-6, -4, -2, 2, 4, 5, 8]);
  const T = r.pick([298, 350, 400]);
  const pA = r.pick([0.1, 0.25, 0.5, 1, 2]);
  const pB = r.pick([0.05, 0.1, 0.3, 0.5, 1, 1.5]);
  const K = Math.exp((-dG * 1000) / (R * T));
  const Qv = (pB * pB) / pA;
  const lnr = Math.log(Qv / K);
  require_(Math.abs(lnr) > 0.3);
  const dGr = dG * 1000 + R * T * Math.log(Qv);
  const correct = DIR[Qv < K ? 0 : 1];
  return choice(DIR, correct, `\\text{${Qv < K ? "Forward" : "Reverse"}}`, [
    `${m("\\Delta G = \\Delta G^\\circ + RT\\ln Q")}; the reaction runs in the direction that lowers ${m("G")}: forward if ${m("\\Delta G < 0")} (${m("Q < K")}).`,
    `${m(`Q = \\frac{(p_B/P^\\circ)^2}{p_A/P^\\circ} = \\frac{${pB}^2}{${pA}} = ${fmt(Qv)}`)}, ${m(`K = e^{-\\Delta G^\\circ/RT} = ${fmt(K)}`)}.`,
    `${m(`\\Delta G = ${dG * 1000} + (8.314)(${T})\\ln ${fmt(Qv)} = ${fmt(dGr)}\\,\\mathrm{J/mol}`)}: ${dGr < 0 ? "negative, runs forward" : "positive, runs in reverse"}.`,
  ], { th: "ce-dir", dG: dG * 1000, T, pA, pB, forward: Qv < K },
  `For ${m("\\mathrm{A(g) \\rightleftharpoons 2\\,B(g)}")}, ${m(`\\Delta G^\\circ = ${vu(dG, "kJ/mol")}`)} at ${m(`${T}\\,\\mathrm{K}`)}. A mixture has ${m(`p_A = ${vu(pA, "bar")}`)} and ${m(`p_B = ${vu(pB, "bar")}`)}. Which way does the reaction proceed?`);
}

export const THERMO_TEMPLATES: Record<string, (r: Rng) => Draft> = {
  "th-fe-entropy-rep": feEntropyRep,
  "th-fe-energy-rep": feEnergyRep,
  "th-fe-ideal": feIdeal,
  "th-fe-euler": feEuler,
  "th-fe-gibbs-duhem": feGibbsDuhem,
  "th-fl-isothermal": flIsothermal,
  "th-fl-adiabatic": flAdiabatic,
  "th-fl-isobaric": flIsobaric,
  "th-fl-isochoric": flIsochoric,
  "th-lg-helmholtz": lgHelmholtz,
  "th-lg-enthalpy": lgEnthalpy,
  "th-lg-natural": lgNatural,
  "th-lg-derive": lgDerive,
  "th-lg-gibbs-helmholtz": lgGibbsHelmholtz,
  "th-mx-pick": mxPick,
  "th-mx-measurable": mxMeasurable,
  "th-mx-eos": mxEos,
  "th-mx-triple": mxTriple,
  "th-st-concavity": stConcavity,
  "th-st-cv": stCv,
  "th-st-vdw-stable": stVdwStable,
  "th-st-vdw-tc": stVdwTc,
  "th-st-vdw-kappa": stVdwKappa,
  "th-pe-cc-pressure": peCCPressure,
  "th-pe-cc-enthalpy": peCCEnthalpy,
  "th-pe-cc-temperature": peCCTemperature,
  "th-pe-clapeyron": peClapeyron,
  "th-so-mix-entropy": soMixEntropy,
  "th-so-mix-gibbs": soMixGibbs,
  "th-so-raoult": soRaoult,
  "th-so-henry": soHenry,
  "th-so-activity": soActivity,
  "th-ce-k": ceK,
  "th-ce-dg": ceDG,
  "th-ce-vant-hoff": ceVantHoff,
  "th-ce-extent": ceExtent,
  "th-ce-direction": ceDirection,
};
