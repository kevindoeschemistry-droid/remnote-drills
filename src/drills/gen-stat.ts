// Statistical mechanics, Level 1 (Dill & Bromberg 2e; Shell 2015).
// Built backward from clean answers: integer counts and exact fractions where the
// physics allows (counting, Boltzmann factors of 1/2, Langmuir with rational Kp),
// symbolic answers in x = ε/k_BT, and 1%-tolerance numbers with units otherwise.
// Every problem carries its inputs in `meta` (with an `sm` case name) so
// tests/verify/stat.py can recompute the answer from first principles.
import { Rng } from "./rng";
import type { Draft } from "./types";
import { m } from "./tex";
import { Q } from "./rational";
import { require_ } from "./reject";

// ── constants (SI; CODATA exact where defined) ────────────────────────────────
const KB = 1.380649e-23;
const H = 6.62607015e-34;
const NA = 6.02214076e23;
const R = 8.314;
const AMU = 1.6605390666e-27;
const C_CM = 2.99792458e10; // cm/s
const HBAR = H / (2 * Math.PI);

// ── formatting ─────────────────────────────────────────────────────────────
/** a number for display: 3 significant figures, scientific outside [1e-3, 1e6) */
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
/** a given value as written in a prompt */
const g = (x: number) => fmt(x, 4);
/** round to 3 significant figures (data quoted in a prompt) */
const sig3 = (x: number) => Number(x.toPrecision(3));

const UNITS: Record<string, string> = {
  "kJ/mol": "\\mathrm{kJ/mol}",
  "J/mol": "\\mathrm{J/mol}",
  "J/(mol·K)": "\\mathrm{J\\,mol^{-1}K^{-1}}",
  "kJ/(mol·K)": "\\mathrm{kJ\\,mol^{-1}K^{-1}}",
  "J/K": "\\mathrm{J/K}",
  K: "\\mathrm{K}",
  pm: "\\mathrm{pm}",
  "s⁻¹": "\\mathrm{s^{-1}}",
  "cm⁻¹": "\\mathrm{cm^{-1}}",
  "bar⁻¹": "\\mathrm{bar^{-1}}",
  bar: "\\mathrm{bar}",
  "μM": "\\mu\\mathrm{M}",
  "mL/mol": "\\mathrm{mL/mol}",
};
const u = (unit: string) => (unit ? `\\,${UNITS[unit] ?? `\\mathrm{${unit}}`}` : "");
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
  require_(Number.isFinite(val) && val !== 0);
  return {
    prompt,
    answer: { kind: "expression", ref: `${val}`, vars: [], tol: 0.01, rel: true, label, ...(unit ? { unit } : {}) },
    answerTex: `${labelTex} = ${fmt(val)}${u(unit)}`,
    steps,
    meta,
  };
}

/** an exact number: an integer (must be typed exactly) or a fraction (or ≥ 5 decimals) */
function exactQ(q: Q, label: string, labelTex: string, steps: string[], meta: Record<string, unknown>, prompt: string): Draft {
  return {
    prompt,
    answer: { kind: "expression", ref: q.d === 1 ? `${q.n}` : `${q.n}/${q.d}`, vars: [], tol: q.d === 1 ? 1e-9 : 1e-5, label },
    answerTex: `${labelTex} = ${q.tex()}`,
    steps,
    meta,
  };
}

/** an exact symbolic answer in x = ε/k_BT (or an exact closed form with no variables) */
function exactExpr(
  ref: string,
  tex: string,
  label: string,
  labelTex: string,
  steps: string[],
  meta: Record<string, unknown>,
  prompt: string,
  vars: string[] = ["x"]
): Draft {
  return {
    prompt,
    answer: { kind: "expression", ref, vars, tol: vars.length ? 1e-6 : 1e-5, label },
    answerTex: `${labelTex} = ${tex}`,
    steps,
    meta,
  };
}

const fact = (n: number): number => (n <= 1 ? 1 : n * fact(n - 1));
const choose = (n: number, k: number): number => {
  if (k < 0 || k > n) return 0;
  let r = 1;
  for (let i = 1; i <= k; i++) r = (r * (n - k + i)) / i;
  return Math.round(r);
};
/** g·body with g = 1 dropped */
const cf = (k: number, body: string) => (k === 1 ? body : `${k}${body}`);
const X_DEF = `Answer in terms of ${m("x = \\varepsilon/k_BT")} (type x; e.g. exp(-x)).`;

// ═══ stat.probability — D&B Ch 1 ════════════════════════════════════════════
function perm(r: Rng): Draft {
  const n = r.int(5, 9);
  const k = r.int(2, 4);
  const W = fact(n) / fact(n - k);
  const race = r.chance(0.5);
  const prompt = race
    ? `${n} runners finish a race with no ties. In how many ways can the first ${k} places be filled?`
    : `${k} distinguishable molecules (labelled A, B, …) are placed on a lattice of ${n} sites, at most one per site. How many arrangements are there?`;
  const prod = Array.from({ length: k }, (_, i) => n - i).join(" \\cdot ");
  return exactQ(new Q(W), "W", "W", [
    `Order matters (${race ? "gold ≠ silver" : "A on site 1 ≠ B on site 1"}): the first choice has ${n} options, the next ${n - 1}, and so on.`,
    m(`W = \\frac{n!}{(n-k)!} = \\frac{${n}!}{${n - k}!} = ${prod} = ${W}`),
  ], { sm: "perm", n, k }, prompt);
}

function comb(r: Rng): Draft {
  const n = r.int(5, 10);
  const k = r.int(2, n - 2);
  const W = choose(n, k);
  return exactQ(new Q(W), "W", "W", [
    `The ligands are identical, so only WHICH sites are filled matters: count ordered placements, then divide by the ${m(`${k}!`)} orderings of the ligands.`,
    m(`W = \\binom{${n}}{${k}} = \\frac{${n}!}{${k}!\\,${n - k}!} = ${W}`),
  ], { sm: "comb", n, k }, `${k} identical ligand molecules bind to a receptor with ${n} distinguishable sites, at most one per site. How many distinct ways can the ${k} ligands be arranged on the sites?`);
}

const P_OPTS = [
  { a: 1, b: 2, what: "a fair coin lands heads", one: "lands heads" },
  { a: 1, b: 6, what: "a fair die shows a six", one: "shows a six" },
  { a: 1, b: 4, what: "a molecule is in its excited state with probability 1/4", one: "is excited" },
  { a: 1, b: 3, what: "a spin points up with probability 1/3", one: "points up" },
] as const;

function binomProb(r: Rng): Draft {
  const P = r.pick(P_OPTS);
  const n = r.int(4, P.b === 6 ? 6 : P.b === 4 ? 7 : 8);
  const k = r.int(0, n);
  const ways = choose(n, k);
  const q = new Q(ways * P.a ** k * (P.b - P.a) ** (n - k), P.b ** n);
  const p = new Q(P.a, P.b);
  const pc = new Q(P.b - P.a, P.b);
  const items = P.b === 2 ? `${n} tosses` : P.b === 6 ? `${n} rolls` : `${n} independent ${P.b === 4 ? "molecules" : "spins"}`;
  return exactQ(q, "P", "P", [
    `Each outcome with exactly ${k} successes has probability ${m(`p^{${k}}(1-p)^{${n - k}}`)} with ${m(`p = ${p.tex()}`)}; there are ${m(`\\binom{${n}}{${k}} = ${ways}`)} such sequences.`,
    m(`P = \\binom{${n}}{${k}}\\left(${p.tex()}\\right)^{${k}}\\left(${pc.tex()}\\right)^{${n - k}} = ${q.tex()}`),
  ], { sm: "binom", n, k, a: P.a, b: P.b },
  `${P.b === 2 ? "A fair coin is tossed" : P.b === 6 ? "A fair die is rolled" : "Consider"} ${items}${P.b === 4 || P.b === 3 ? `; each ${P.b === 4 ? "molecule is in its excited state with probability 1/4" : "spin points up with probability 1/3"}` : ""}. What is the probability that exactly ${k} ${P.b === 2 ? "land heads" : P.b === 6 ? "show a six" : P.b === 4 ? "are excited" : "point up"}? (Exact fraction.)`);
}

function anagram(r: Rng): Draft {
  const kinds = r.pick([2, 3]);
  const N = r.int(5, 8);
  const counts: number[] = [];
  let left = N;
  for (let i = 0; i < kinds - 1; i++) {
    const c = r.int(1, left - (kinds - 1 - i));
    counts.push(c);
    left -= c;
  }
  counts.push(left);
  require_(counts.every((c) => c >= 1) && counts.some((c) => c >= 2));
  const W = fact(N) / counts.reduce((s, c) => s * fact(c), 1);
  const names = ["A", "B", "C"];
  const desc = counts.map((c, i) => `${c} ${names[i]}`).join(", ");
  return exactQ(new Q(W), "W", "W", [
    `${m(`${N}!`)} orderings if every monomer were distinguishable; swapping identical monomers gives the same sequence, so divide by each ${m("n_i!")}.`,
    m(`W = \\frac{N!}{${counts.map((_, i) => `n_${names[i]}!`).join("\\,")}} = \\frac{${N}!}{${counts.map((c) => `${c}!`).join("\\,")}} = ${W}`),
  ], { sm: "anagram", counts }, `A linear copolymer has ${N} monomers: ${desc}. How many distinct sequences are possible?`);
}

function atLeastOne(r: Rng): Draft {
  const P = r.pick(P_OPTS);
  const n = r.int(2, P.b === 6 ? 4 : 5);
  const q = new Q(P.b ** n - (P.b - P.a) ** n, P.b ** n);
  const pc = new Q(P.b - P.a, P.b);
  const set = P.b === 2 ? `${n} coins are tossed` : P.b === 6 ? `${n} fair dice are rolled` : P.b === 4 ? `${n} independent molecules are each excited with probability 1/4` : `${n} independent spins each point up with probability 1/3`;
  return exactQ(q, "P", "P", [
    `"At least one" is the complement of "none": ${m("P = 1 - P(\\text{none})")}.`,
    `Independent, so ${m(`P(\\text{none}) = \\left(${pc.tex()}\\right)^{${n}}`)}.`,
    m(`P = 1 - \\left(${pc.tex()}\\right)^{${n}} = ${q.tex()}`),
  ], { sm: "atleast", n, a: P.a, b: P.b },
  `${set[0].toUpperCase()}${set.slice(1)}. What is the probability that at least one ${P.b === 2 ? "lands heads" : P.b === 6 ? "shows a six" : P.b === 4 ? "is excited" : "points up"}? (Exact fraction.)`);
}

// ═══ stat.multiplicity — D&B Ch 5; Shell Ch 2, 4 ═══════════════════════════
function twoState(r: Rng): Draft {
  const N = r.int(6, 12);
  const n = r.int(1, N - 1);
  const W = choose(N, n);
  return exactQ(new Q(W), "W", "W", [
    `A microstate says which ${n} of the ${N} spins are up; the spins are distinguishable by position, the up-states are not.`,
    m(`W(N, n) = \\frac{N!}{n!\\,(N-n)!} = \\frac{${N}!}{${n}!\\,${N - n}!} = ${W}`),
  ], { sm: "two-state", N, n }, `A system of ${N} independent two-state spins (each up or down, fixed in place) has exactly ${n} spins up. What is its multiplicity ${m("W")}?`);
}

function einsteinW(r: Rng): Draft {
  const N = r.int(3, 5);
  const q = r.int(2, 6);
  const W = choose(q + N - 1, q);
  return exactQ(new Q(W), "W", "W", [
    `Stars and bars: ${q} indistinguishable quanta and ${N - 1} dividers between ${N} oscillators — arrange ${q + N - 1} objects.`,
    m(`W = \\binom{q + N - 1}{q} = \\frac{(${q} + ${N} - 1)!}{${q}!\\,(${N} - 1)!} = ${W}`),
  ], { sm: "einstein", N, q }, `An Einstein solid has ${N} distinguishable oscillators sharing ${m(`q = ${q}`)} indistinguishable energy quanta. How many microstates ${m("W")} are there?`);
}

function dSTwoState(r: Rng): Draft {
  const N = r.int(6, 12);
  const n1 = r.int(0, N);
  const n2 = r.int(0, N);
  const W1 = choose(N, n1);
  const W2 = choose(N, n2);
  require_(W1 !== W2);
  const ratio = new Q(W2, W1);
  const val = Math.log(W2 / W1);
  return exactExpr(`log(${ratio.n}/${ratio.d})`, `\\ln ${ratio.d === 1 ? ratio.n : `\\frac{${ratio.n}}{${ratio.d}}`} \\approx ${fmt(val, 4)}`, "ΔS/k", "\\Delta S/k_B", [
    `Boltzmann: ${m("S = k_B\\ln W")}, so ${m("\\Delta S/k_B = \\ln(W_2/W_1)")}.`,
    `${m(`W_1 = \\binom{${N}}{${n1}} = ${W1}`)}, ${m(`W_2 = \\binom{${N}}{${n2}} = ${W2}`)}.`,
    m(`\\Delta S/k_B = \\ln\\frac{${W2}}{${W1}} \\approx ${fmt(val, 4)}`),
  ], { sm: "dS-two-state", N, n1, n2 }, `${N} two-state spins go from ${n1} up to ${n2} up. Find ${m("\\Delta S/k_B")} (an exact expression like ln(5/2), or a decimal).`, []);
}

function dSVolume(r: Rng): Draft {
  const nmol = r.pick([0.5, 1, 2, 3]);
  const ratio = r.pick([2, 3, 4, 5, 10]);
  const expand = r.chance(0.6);
  const [V1, V2] = expand ? [1, ratio] : [ratio, 1];
  const dS = nmol * R * Math.log(V2 / V1);
  return numeric(dS, "ΔS", "\\Delta S", "J/K", [
    `Lattice model: each of the ${m("N")} molecules independently occupies one of ${m("M \\propto V")} cells, so ${m("W = M^N")} and ${m("\\Delta S = Nk_B\\ln(V_2/V_1)")}.`,
    `${m("Nk_B = nR")}: ${m(`\\Delta S = ${g(nmol)}(8.314)\\ln${expand ? ratio : `\\frac{1}{${ratio}}`} = ${fmt(dS)}\\,\\mathrm{J/K}`)}${expand ? "" : " (negative: fewer places to be)"}.`,
  ], { sm: "dS-volume", nmol, V1, V2 }, `${g(nmol)} mol of an ideal gas is ${expand ? "expanded" : "compressed"} isothermally to ${expand ? `${ratio} times` : `1/${ratio} of`} its volume. Treating each molecule as independently occupying one of ${m("M \\propto V")} lattice cells, find ${m("\\Delta S")} (${m("R = 8.314\\,\\mathrm{J\\,mol^{-1}K^{-1}}")}).`);
}

function einsteinShare(r: Rng): Draft {
  const NA_ = r.int(2, 3);
  const NB_ = r.int(2, 3);
  const q = r.int(3, 6);
  const qA = r.int(0, q);
  const WA = choose(qA + NA_ - 1, qA);
  const WB = choose(q - qA + NB_ - 1, q - qA);
  const Wt = choose(q + NA_ + NB_ - 1, q);
  const P = new Q(WA * WB, Wt);
  return exactQ(P, "P", "P", [
    `All ${m(`W_{tot} = \\binom{${q} + ${NA_ + NB_} - 1}{${q}} = ${Wt}`)} microstates of the combined solid are equally likely.`,
    `Those with ${m(`q_A = ${qA}`)}: ${m(`W_A W_B = \\binom{${qA + NA_ - 1}}{${qA}}\\binom{${q - qA + NB_ - 1}}{${q - qA}} = ${WA}\\cdot${WB} = ${WA * WB}`)}.`,
    m(`P = \\frac{${WA * WB}}{${Wt}} = ${P.tex()}`),
  ], { sm: "einstein-share", NA: NA_, NB: NB_, q, qA },
  `Einstein solids A (${NA_} oscillators) and B (${NB_} oscillators) are in thermal contact and share ${m(`q = ${q}`)} quanta. What is the probability that A holds exactly ${m(`q_A = ${qA}`)} quanta? (Exact fraction.)`);
}

// ═══ stat.boltzmann — D&B Ch 10; Shell Ch 16 ═══════════════════════════════
function bzRatio(r: Rng): Draft {
  const T = r.pick([200, 250, 298, 300, 400, 500, 1000]);
  const g1 = r.int(1, 3);
  const g2 = r.int(1, 3);
  const wav = r.chance(0.4);
  if (wav) {
    const nu = r.pick([50, 100, 200, 300, 500, 1000, 1500, 2000]);
    const x = (H * C_CM * nu) / (KB * T);
    const ratio = (g2 / g1) * Math.exp(-x);
    require_(ratio > 1e-6);
    return numeric(ratio, "N₂/N₁", "N_2/N_1", "", [
      `Boltzmann: ${m("\\frac{N_2}{N_1} = \\frac{g_2}{g_1}e^{-\\Delta E/k_BT}")}, with ${m("\\Delta E = hc\\tilde\\nu")} per molecule.`,
      m(`\\frac{\\Delta E}{k_BT} = \\frac{hc\\tilde\\nu}{k_BT} = \\frac{(6.626\\times10^{-34})(2.998\\times10^{10})(${nu})}{(1.381\\times10^{-23})(${T})} = ${fmt(x, 4)}`),
      m(`\\frac{N_2}{N_1} = \\frac{${g2}}{${g1}}e^{-${fmt(x, 4)}} = ${fmt(ratio)}`),
    ], { sm: "bz-ratio", nu, T, g1, g2 }, `Two energy levels are separated by ${m(vu(nu, "cm⁻¹"))}; the lower has degeneracy ${m(`g_1 = ${g1}`)}, the upper ${m(`g_2 = ${g2}`)}. At ${m(vu(T, "K"))}, find the population ratio ${m("N_2/N_1")}.`);
  }
  const dE = r.pick([1, 2, 2.5, 4, 5, 8, 10, 15, 20]);
  const x = (dE * 1000) / (R * T);
  const ratio = (g2 / g1) * Math.exp(-x);
  require_(ratio > 1e-6);
  return numeric(ratio, "N₂/N₁", "N_2/N_1", "", [
    `Boltzmann: ${m("\\frac{N_2}{N_1} = \\frac{g_2}{g_1}e^{-\\Delta E/RT}")} (molar energy, so ${m("R")}, not ${m("k_B")}).`,
    m(`\\frac{\\Delta E}{RT} = \\frac{${g(dE * 1000)}}{(8.314)(${T})} = ${fmt(x, 4)}`),
    m(`\\frac{N_2}{N_1} = \\frac{${g2}}{${g1}}e^{-${fmt(x, 4)}} = ${fmt(ratio)}`),
  ], { sm: "bz-ratio", dE, T, g1, g2 }, `Two energy levels are ${m(vu(dE, "kJ/mol"))} apart; the lower has degeneracy ${m(`g_1 = ${g1}`)}, the upper ${m(`g_2 = ${g2}`)}. At ${m(vu(T, "K"))}, find the population ratio ${m("N_2/N_1")}.`);
}

function bzFraction(r: Rng): Draft {
  const E1 = r.pick([1, 2, 3, 4, 5]);
  const E2 = E1 + r.pick([1, 2, 3, 5]);
  const gs = [r.int(1, 3), r.int(1, 3), r.int(1, 3)];
  const T = r.pick([200, 300, 400, 500, 800]);
  const Es = [0, E1, E2];
  const w = Es.map((E, i) => gs[i] * Math.exp((-E * 1000) / (R * T)));
  const q = w.reduce((s, v) => s + v, 0);
  const which = r.int(0, 2);
  const f = w[which] / q;
  require_(f > 1e-3);
  const term = (i: number) => (Es[i] === 0 ? `${gs[i]}` : `${cf(gs[i], `e^{-${fmt((Es[i] * 1000) / (R * T), 4)}}`)}`);
  return numeric(f, "p", `p_${which}`, "", [
    `${m("p_i = g_ie^{-E_i/RT}/q")} with ${m("q = \\sum_j g_je^{-E_j/RT}")}.`,
    m(`q = ${[0, 1, 2].map(term).join(" + ")} = ${fmt(q, 4)}`),
    m(`p_${which} = \\frac{${fmt(w[which], 4)}}{${fmt(q, 4)}} = ${fmt(f)}`),
  ], { sm: "bz-fraction", Es, gs, T, which },
  `A molecule has three levels: ${m(`E_0 = 0`)} (${m(`g_0 = ${gs[0]}`)}), ${m(`E_1 = ${vu(E1, "kJ/mol")}`)} (${m(`g_1 = ${gs[1]}`)}), ${m(`E_2 = ${vu(E2, "kJ/mol")}`)} (${m(`g_2 = ${gs[2]}`)}). At ${m(vu(T, "K"))}, what fraction ${m(`p_${which}`)} of molecules is in level ${which}${which ? "" : " (the ground level)"}?`);
}

function bzTemperature(r: Rng): Draft {
  const dE = r.pick([2, 4, 5, 8, 10]);
  const g1 = 1;
  const g2 = r.int(1, 3);
  const ratio = r.pick([0.01, 0.05, 0.1, 0.2, 0.5]);
  require_(ratio < g2 / g1);
  const T = (dE * 1000) / (R * Math.log(g2 / (g1 * ratio)));
  return numeric(T, "T", "T", "K", [
    `Solve ${m(`\\frac{N_2}{N_1} = \\frac{g_2}{g_1}e^{-\\Delta E/RT}`)} for ${m("T")}: ${m("T = \\frac{\\Delta E}{R\\ln\\left(\\frac{g_2}{g_1}\\cdot\\frac{N_1}{N_2}\\right)}")}.`,
    m(`T = \\frac{${g(dE * 1000)}}{8.314\\,\\ln(${g2}/${g(ratio)})} = ${fmt(T)}\\,\\mathrm{K}`),
  ], { sm: "bz-T", dE, g1, g2, ratio }, `An excited level lies ${m(vu(dE, "kJ/mol"))} above a nondegenerate ground level and has degeneracy ${m(`g_2 = ${g2}`)}. At what temperature is ${m(`N_2/N_1 = ${g(ratio)}`)}?`);
}

function bzExact(r: Rng): Draft {
  const a = r.pick([2, 3, 4]);
  const gs = [r.int(1, 3), r.int(1, 3), r.int(1, 3)];
  const j = r.int(0, 2);
  const ws = gs.map((gi, i) => gi * a ** (2 - i));
  const Z = ws[0] + ws[1] + ws[2];
  const f = new Q(ws[j], Z);
  const fr = (gi: number, i: number) => (i === 0 ? `${gi}` : `${gi}\\cdot\\frac{1}{${a ** i}}`);
  return exactQ(f, "p", `p_${j}`, [
    `At this temperature each step up in energy costs a factor ${m(`e^{-\\varepsilon/k_BT} = 1/${a}`)}.`,
    m(`q = ${gs.map(fr).join(" + ")} = ${new Q(Z, a * a).tex()}`),
    m(`p_${j} = \\frac{${fr(gs[j], j)}}{q} = ${f.tex()}`),
  ], { sm: "bz-exact", a, gs, j },
  `Levels ${m("0, \\varepsilon, 2\\varepsilon")} have degeneracies ${m(`${gs[0]}, ${gs[1]}, ${gs[2]}`)}. At the temperature where ${m(`k_BT = \\varepsilon/\\ln ${a}`)}, what fraction of molecules occupies the level at ${m(j === 0 ? "0" : j === 1 ? "\\varepsilon" : "2\\varepsilon")}? (Exact fraction.)`);
}

// ═══ stat.partition-function — D&B Ch 10; Shell Ch 16 ══════════════════════
function pfQ(r: Rng): Draft {
  const E1 = r.pick([0.5, 1, 2, 3, 4]);
  const E2 = E1 + r.pick([0.5, 1, 2, 4]);
  const gs = [1, r.int(1, 3), r.int(1, 5)];
  const T = r.pick([100, 200, 300, 500]);
  const Es = [0, E1, E2];
  const w = Es.map((E, i) => gs[i] * Math.exp((-E * 1000) / (R * T)));
  const q = w.reduce((s, v) => s + v, 0);
  return numeric(q, "q", "q", "", [
    `Sum over levels: ${m("q = \\sum_i g_ie^{-E_i/RT}")}; the ground level contributes ${m("g_0 = 1")}.`,
    m(`q = 1 + ${cf(gs[1], `e^{-${fmt((E1 * 1000) / (R * T), 4)}}`)} + ${cf(gs[2], `e^{-${fmt((E2 * 1000) / (R * T), 4)}}`)} = ${fmt(q)}`),
    `Read it as "about ${fmt(q, 2)} states are thermally accessible".`,
  ], { sm: "pf-q", Es, gs, T },
  `A molecule's levels are ${m("0")} (nondegenerate), ${m(vu(E1, "kJ/mol"))} (${m(`g = ${gs[1]}`)}) and ${m(vu(E2, "kJ/mol"))} (${m(`g = ${gs[2]}`)}). Find the molecular partition function ${m("q")} at ${m(vu(T, "K"))}.`);
}

function twoLevelTex(g0: number, g1: number) {
  return { qTex: `${g0} + ${cf(g1, "e^{-x}")}`, qJs: `(${g0} + ${g1}*exp(-x))` };
}

function pfU2(r: Rng): Draft {
  const g0 = r.int(1, 3);
  const g1 = r.int(1, 3);
  const { qTex, qJs } = twoLevelTex(g0, g1);
  return exactExpr(`${g1}*exp(-x)/${qJs}`, `\\frac{${cf(g1, "e^{-x}")}}{${qTex}}`, "U/Nε", "\\frac{U}{N\\varepsilon}", [
    `${m(`q = ${g0} + ${cf(g1, "e^{-\\beta\\varepsilon}")}`)}.`,
    `${m("U/N = -\\partial\\ln q/\\partial\\beta = \\varepsilon\\cdot p_1")}: the energy is ${m("\\varepsilon")} times the probability of being up.`,
    m(`\\frac{U}{N\\varepsilon} = \\frac{${cf(g1, "e^{-x}")}}{${qTex}}`),
  ], { sm: "pf-U2", g0, g1 },
  `${m("N")} independent two-level systems: ground level at ${m("0")} (degeneracy ${g0}), excited level at ${m("\\varepsilon")} (degeneracy ${g1}). Find the average energy per particle ${m("U/N\\varepsilon")}. ${X_DEF}`);
}

function pfS2(r: Rng): Draft {
  const g0 = r.int(1, 2);
  const g1 = r.int(1, 3);
  const { qTex, qJs } = twoLevelTex(g0, g1);
  return exactExpr(`log${qJs} + x*${g1}*exp(-x)/${qJs}`, `\\ln\\left(${qTex}\\right) + \\frac{${cf(g1, "xe^{-x}")}}{${qTex}}`, "S/Nk", "\\frac{S}{Nk_B}", [
    `${m("F = -Nk_BT\\ln q")} and ${m("S = (U - F)/T")}, so ${m("\\frac{S}{Nk_B} = \\ln q + \\frac{U}{Nk_BT}")}.`,
    `${m(`\\frac{U}{N\\varepsilon} = \\frac{${cf(g1, "e^{-x}")}}{${qTex}}`)}, and ${m("\\frac{U}{Nk_BT} = x\\frac{U}{N\\varepsilon}")}.`,
    m(`\\frac{S}{Nk_B} = \\ln\\left(${qTex}\\right) + \\frac{${cf(g1, "xe^{-x}")}}{${qTex}}`),
  ], { sm: "pf-S2", g0, g1 },
  `${m("N")} independent two-level systems: ground level ${m("0")} (degeneracy ${g0}), excited level ${m("\\varepsilon")} (degeneracy ${g1}). Find the entropy per particle ${m("S/Nk_B")}. ${X_DEF}`);
}

function pfUho(r: Rng): Draft {
  const zp = r.chance(0.5);
  const ref = zp ? "1/2 + 1/(exp(x) - 1)" : "1/(exp(x) - 1)";
  const tex = zp ? "\\frac{1}{2} + \\frac{1}{e^{x} - 1}" : "\\frac{1}{e^{x} - 1}";
  return exactExpr(ref, tex, "U/Nε", "\\frac{U}{N\\varepsilon}", [
    `${zp ? m("E_v = (v + \\tfrac12)\\varepsilon") : m("E_v = v\\varepsilon")}, ${m("v = 0, 1, 2, \\dots")}: a geometric series, ${m(zp ? "q = \\frac{e^{-x/2}}{1 - e^{-x}}" : "q = \\frac{1}{1 - e^{-x}}")}.`,
    `${m("U/N = -\\partial\\ln q/\\partial\\beta")}: ${m(zp ? "\\ln q = -\\tfrac{\\beta\\varepsilon}{2} - \\ln(1 - e^{-\\beta\\varepsilon})" : "\\ln q = -\\ln(1 - e^{-\\beta\\varepsilon})")}.`,
    m(`\\frac{U}{N\\varepsilon} = ${tex}`),
  ], { sm: "pf-Uho", zp },
  `${m("N")} independent quantum harmonic oscillators have levels ${zp ? m("E_v = (v + \\tfrac12)\\varepsilon") : m("E_v = v\\varepsilon")} (energies measured ${zp ? "from the potential minimum" : "from the ground state"}). Find ${m("U/N\\varepsilon")}. ${X_DEF}`);
}

function pfF(r: Rng): Draft {
  const E1 = r.pick([1, 2, 3, 5]);
  const g0 = r.int(1, 2);
  const g1 = r.int(1, 4);
  const T = r.pick([200, 300, 400, 600]);
  const q = g0 + g1 * Math.exp((-E1 * 1000) / (R * T));
  const F = (-R * T * Math.log(q)) / 1000;
  require_(Math.abs(F) > 0.01);
  return numeric(F, "F", "F_m", "kJ/mol", [
    `Localized (distinguishable) particles: ${m("Q = q^N")}, so ${m("F = -k_BT\\ln Q = -Nk_BT\\ln q")}; per mole ${m("F_m = -RT\\ln q")}.`,
    m(`q = ${g0} + ${cf(g1, `e^{-${fmt((E1 * 1000) / (R * T), 4)}}`)} = ${fmt(q, 4)}`),
    m(`F_m = -(8.314)(${T})\\ln(${fmt(q, 4)}) = ${fmt(F * 1000)}\\,\\mathrm{J/mol} = ${fmt(F)}\\,\\mathrm{kJ/mol}`),
  ], { sm: "pf-F", E1, g0, g1, T },
  `A mole of independent, localized molecules each has a ground level (degeneracy ${g0}) and one excited level ${m(vu(E1, "kJ/mol"))} higher (degeneracy ${g1}). Find the molar Helmholtz free energy ${m("F_m")} (relative to all molecules in one ground state) at ${m(vu(T, "K"))}.`);
}

// ═══ stat.ideal-gas — D&B Ch 11; Shell Ch 9, 18 ═════════════════════════════
const GASES = [
  { name: "He", M: 4.003 }, { name: "Ne", M: 20.18 }, { name: "Ar", M: 39.95 }, { name: "N₂", M: 28.01 },
  { name: "O₂", M: 32.0 }, { name: "CO₂", M: 44.01 }, { name: "Kr", M: 83.8 }, { name: "Xe", M: 131.3 },
];
const lam = (M: number, T: number) => H / Math.sqrt(2 * Math.PI * M * AMU * KB * T);

function igLambda(r: Rng): Draft {
  const gas = r.pick(GASES);
  const T = r.pick([50, 100, 200, 300, 500, 1000]);
  const L = lam(gas.M, T) * 1e12;
  return numeric(L, "Λ", "\\Lambda", "pm", [
    `${m("\\Lambda = \\frac{h}{\\sqrt{2\\pi mk_BT}}")}, with ${m(`m = ${g(gas.M)}\\,\\mathrm{u} \\times 1.661\\times10^{-27} = ${fmt(gas.M * AMU, 4)}\\,\\mathrm{kg}`)}.`,
    m(`\\Lambda = \\frac{6.626\\times10^{-34}}{\\sqrt{2\\pi(${fmt(gas.M * AMU, 4)})(1.381\\times10^{-23})(${T})}} = ${fmt(L * 1e-12)}\\,\\mathrm{m} = ${fmt(L)}\\,\\mathrm{pm}`),
  ], { sm: "ig-lambda", M: gas.M, T },
  `Find the thermal de Broglie wavelength ${m("\\Lambda")} of ${gas.name} (${m(`${g(gas.M)}\\,\\mathrm{g/mol}`)}) at ${m(vu(T, "K"))}, in picometres.`);
}

const VOLS = [
  { V: 1e-6, tex: "1\\,\\mathrm{cm^3}" },
  { V: 1e-3, tex: "1\\,\\mathrm{L}" },
  { V: 0.0248, tex: "24.8\\,\\mathrm{L}" },
  { V: 1, tex: "1\\,\\mathrm{m^3}" },
];
function igQtrans(r: Rng): Draft {
  const gas = r.pick(GASES);
  const T = r.pick([100, 300, 500, 1000]);
  const V = r.pick(VOLS);
  const L = lam(gas.M, T);
  const q = V.V / L ** 3;
  return numeric(q, "q", "q_{trans}", "", [
    `${m("q_{trans} = V/\\Lambda^3")} — the number of thermal-wavelength cubes that fit in the box.`,
    m(`\\Lambda = \\frac{h}{\\sqrt{2\\pi mk_BT}} = ${fmt(L, 4)}\\,\\mathrm{m}`),
    m(`q_{trans} = \\frac{${fmt(V.V)}}{(${fmt(L, 4)})^3} = ${fmt(q)}`),
  ], { sm: "ig-qtrans", M: gas.M, T, V: V.V },
  `Find the translational partition function ${m("q_{trans}")} of one ${gas.name} molecule (${m(`${g(gas.M)}\\,\\mathrm{g/mol}`)}) in a ${m(V.tex)} box at ${m(vu(T, "K"))}.`);
}

const BONDS = [
  { name: "H₂", m1: 1.008, m2: 1.008, r: 74.14 },
  { name: "N₂", m1: 14.003, m2: 14.003, r: 109.8 },
  { name: "O₂", m1: 15.995, m2: 15.995, r: 120.7 },
  { name: "CO", m1: 12.0, m2: 15.995, r: 112.8 },
  { name: "H³⁵Cl", m1: 1.008, m2: 34.969, r: 127.5 },
  { name: "HF", m1: 1.008, m2: 18.998, r: 91.7 },
  { name: "NO", m1: 14.003, m2: 15.995, r: 115.1 },
  { name: "³⁵Cl₂", m1: 34.969, m2: 34.969, r: 198.8 },
];
function igThetaRot(r: Rng): Draft {
  const b = r.pick(BONDS);
  const mu = ((b.m1 * b.m2) / (b.m1 + b.m2)) * AMU;
  const I = mu * (b.r * 1e-12) ** 2;
  const th = HBAR ** 2 / (2 * I * KB);
  return numeric(th, "θ_rot", "\\theta_{rot}", "K", [
    `Rigid rotor: ${m("E_J = J(J+1)\\frac{\\hbar^2}{2I}")}, ${m("\\theta_{rot} = \\frac{\\hbar^2}{2Ik_B}")}, ${m("I = \\mu r^2")}.`,
    m(`\\mu = \\frac{(${b.m1})(${b.m2})}{${g(b.m1 + b.m2)}}\\,\\mathrm{u} = ${fmt(mu, 4)}\\,\\mathrm{kg},\\quad I = ${fmt(I, 4)}\\,\\mathrm{kg\\,m^2}`),
    m(`\\theta_{rot} = \\frac{(1.0546\\times10^{-34})^2}{2(${fmt(I, 4)})(1.381\\times10^{-23})} = ${fmt(th)}\\,\\mathrm{K}`),
  ], { sm: "ig-theta-rot", m1: b.m1, m2: b.m2, r: b.r },
  `${b.name} has atomic masses ${m(`${b.m1}`)} and ${m(`${b.m2}\\,\\mathrm{u}`)} and bond length ${m(`${b.r}\\,\\mathrm{pm}`)}. Find its rotational temperature ${m("\\theta_{rot} = \\hbar^2/(2Ik_B)")}.`);
}

const ROTORS = [
  { name: "H₂", th: 87.6, s: 2 }, { name: "N₂", th: 2.88, s: 2 }, { name: "O₂", th: 2.08, s: 2 },
  { name: "CO", th: 2.78, s: 1 }, { name: "HCl", th: 15.2, s: 1 }, { name: "Cl₂", th: 0.351, s: 2 },
  { name: "I₂", th: 0.0537, s: 2 }, { name: "NO", th: 2.45, s: 1 }, { name: "HF", th: 30.1, s: 1 },
];
function igQrot(r: Rng): Draft {
  const mol = r.pick(ROTORS);
  const T = r.pick([300, 500, 1000]);
  require_(T / mol.th >= 10);
  const q = T / (mol.s * mol.th);
  return numeric(q, "q_rot", "q_{rot}", "", [
    `${m(`T/\\theta_{rot} = ${fmt(T / mol.th)} \\gg 1`)}, so the sum over ${m("J")} becomes an integral: ${m("q_{rot} = \\frac{T}{\\sigma\\theta_{rot}}")}.`,
    `${mol.s === 2 ? "Homonuclear" : "Heteronuclear"}: ${m(`\\sigma = ${mol.s}`)}${mol.s === 2 ? " (a half-turn gives the same molecule)" : ""}.`,
    m(`q_{rot} = \\frac{${T}}{${mol.s === 1 ? "" : `${mol.s}\\times`}${g(mol.th)}} = ${fmt(q)}`),
  ], { sm: "ig-qrot", th: mol.th, s: mol.s, T },
  `${mol.name} has ${m(`\\theta_{rot} = ${vu(mol.th, "K")}`)}. Find its rotational partition function at ${m(vu(T, "K"))} (high-temperature limit; include the symmetry number).`);
}

const VIBS = [
  { name: "N₂", nu: 2359 }, { name: "O₂", nu: 1580 }, { name: "CO", nu: 2170 }, { name: "HCl", nu: 2991 },
  { name: "Cl₂", nu: 560 }, { name: "Br₂", nu: 325 }, { name: "I₂", nu: 214.5 }, { name: "F₂", nu: 917 },
];
function igQvib(r: Rng): Draft {
  const mol = r.pick(VIBS);
  const T = r.pick([300, 500, 1000, 2000]);
  const th = (H * C_CM * mol.nu) / KB;
  const x = th / T;
  const variant = r.pick(["theta", "q", "excited"] as const);
  const thStep = m(`\\theta_{vib} = \\frac{hc\\tilde\\nu}{k_B} = \\frac{(6.626\\times10^{-34})(2.998\\times10^{10})(${mol.nu})}{1.381\\times10^{-23}} = ${fmt(th, 4)}\\,\\mathrm{K}`);
  const meta = { sm: "ig-qvib", nu: mol.nu, T, variant };
  const given = `${mol.name} has ${m(`\\tilde\\nu = ${vu(mol.nu, "cm⁻¹")}`)}`;
  if (variant === "theta")
    return numeric(th, "θ_vib", "\\theta_{vib}", "K", [
      `${m("\\theta_{vib}")} is the vibrational quantum in kelvin: ${m("k_B\\theta_{vib} = h\\nu = hc\\tilde\\nu")} (with ${m("c")} in cm/s).`,
      thStep,
    ], meta, `${given}. Find its vibrational temperature ${m("\\theta_{vib}")}.`);
  if (variant === "q") {
    require_(x <= 3);
    const q = 1 / (1 - Math.exp(-x));
    return numeric(q, "q_vib", "q_{vib}", "", [
      thStep,
      `Energies from the ground state, ${m("E_v = vk_B\\theta_{vib}")}: geometric series ${m("q_{vib} = \\frac{1}{1 - e^{-\\theta_{vib}/T}}")}.`,
      m(`q_{vib} = \\frac{1}{1 - e^{-${fmt(x, 4)}}} = ${fmt(q)}`),
    ], meta, `${given}. Find its vibrational partition function ${m("q_{vib}")} at ${m(vu(T, "K"))}, with energies measured from the ground vibrational state.`);
  }
  const f = Math.exp(-x);
  require_(f >= 1e-4);
  return numeric(f, "fraction", "1 - p_0", "", [
    thStep,
    `${m("p_0 = 1/q_{vib} = 1 - e^{-\\theta_{vib}/T}")}, so the excited fraction is ${m("1 - p_0 = e^{-\\theta_{vib}/T}")}.`,
    m(`e^{-${fmt(x, 4)}} = ${fmt(f)}`),
  ], meta, `${given}. At ${m(vu(T, "K"))}, what fraction of molecules is in an excited vibrational state (${m("v \\ge 1")})?`);
}

// ═══ stat.heat-capacity — D&B Ch 12 ═════════════════════════════════════════
const MOLS = [
  { name: "Ar", atoms: 1, linear: false }, { name: "He", atoms: 1, linear: false },
  { name: "N₂", atoms: 2, linear: true }, { name: "HCl", atoms: 2, linear: true },
  { name: "CO₂", atoms: 3, linear: true }, { name: "HCN", atoms: 3, linear: true },
  { name: "H₂O", atoms: 3, linear: false }, { name: "NH₃", atoms: 4, linear: false },
  { name: "C₂H₂ (acetylene)", atoms: 4, linear: true }, { name: "CH₄", atoms: 5, linear: false },
];
function cvEquipartition(r: Rng): Draft {
  const mol = r.pick(MOLS);
  const high = mol.atoms > 1 && r.chance(0.5);
  const rot = mol.atoms === 1 ? 0 : mol.linear ? 2 : 3;
  const vib = 3 * mol.atoms - 3 - rot;
  const half = 3 + rot + (high ? 2 * vib : 0); // quadratic terms
  const cv = new Q(half, 2);
  return exactQ(cv, "Cv/R", "C_{V,m}/R", [
    `Equipartition: each quadratic term in the energy gives ${m("\\tfrac12 R")} per mole.`,
    `Translation: 3 terms. Rotation: ${rot === 0 ? "none (an atom)" : `${rot} (${mol.linear ? "linear" : "nonlinear"})`}.${mol.atoms > 1 ? ` Vibration: ${m(`3N - ${mol.linear ? 5 : 6} = ${vib}`)} modes, ${high ? `each 2 terms (kinetic + potential) = ${2 * vib}` : "frozen out (θ_vib ≫ T)"}.` : ""}`,
    m(`C_{V,m} = \\frac{${half}}{2}R = ${cv.tex()}R`),
  ], { sm: "cv-equip", atoms: mol.atoms, linear: mol.linear, high },
  `Use equipartition to find ${m("C_{V,m}/R")} for ${mol.name} gas ${high ? "at a temperature high enough that every vibration is fully (classically) active" : "near room temperature, where rotations are fully active and vibrations are frozen out"}.`);
}

const einsteinCvOf = (x: number) => (3 * R * x * x * Math.exp(x)) / (Math.exp(x) - 1) ** 2;
function cvEinstein(r: Rng): Draft {
  const thE = r.pick([90, 150, 240, 300, 500, 1320]);
  const T = r.pick([50, 100, 200, 300, 500, 1000]);
  const x = thE / T;
  require_(x <= 12 && x >= 0.05);
  const cv = einsteinCvOf(x);
  return numeric(cv, "Cv", "C_{V,m}", "J/(mol·K)", [
    `Einstein solid: ${m("3N_A")} independent oscillators, ${m("C_{V,m} = 3R\\frac{x^2e^{x}}{(e^{x} - 1)^2}")} with ${m("x = \\theta_E/T")}.`,
    m(`x = \\frac{${thE}}{${T}} = ${fmt(x, 4)}`),
    m(`C_{V,m} = 3(8.314)\\frac{(${fmt(x, 4)})^2e^{${fmt(x, 4)}}}{(e^{${fmt(x, 4)}} - 1)^2} = ${fmt(cv)}\\,\\mathrm{J\\,mol^{-1}K^{-1}}`),
    `Check: ${m("x \\to 0")} gives Dulong–Petit ${m("3R = 24.9")}.`,
  ], { sm: "cv-einstein", thE, T },
  `A crystal has Einstein temperature ${m(`\\theta_E = ${vu(thE, "K")}`)}. Find its molar heat capacity ${m("C_{V,m}")} at ${m(vu(T, "K"))}.`);
}

function cvTwoLevel(r: Rng): Draft {
  const g0 = r.int(1, 3);
  const g1 = r.int(1, 3);
  const { qTex, qJs } = twoLevelTex(g0, g1);
  return exactExpr(`${g0 * g1}*x^2*exp(-x)/${qJs}^2`, `\\frac{${cf(g0 * g1, "x^2e^{-x}")}}{\\left(${qTex}\\right)^2}`, "Cv/Nk", "\\frac{C_V}{Nk_B}", [
    `${m(`\\frac{U}{N\\varepsilon} = \\frac{${cf(g1, "e^{-x}")}}{${qTex}}`)}.`,
    `${m("C_V = \\partial U/\\partial T")} and ${m("\\partial x/\\partial T = -x/T")}, so ${m("\\frac{C_V}{Nk_B} = -x^2\\frac{d(U/N\\varepsilon)}{dx}")}.`,
    m(`\\frac{C_V}{Nk_B} = \\frac{${cf(g0 * g1, "x^2e^{-x}")}}{\\left(${qTex}\\right)^2}`),
    `This is the Schottky peak: zero at both ${m("T \\to 0")} and ${m("T \\to \\infty")}.`,
  ], { sm: "cv-two", g0, g1 },
  `${m("N")} independent two-level systems: ground level ${m("0")} (degeneracy ${g0}), excited level ${m("\\varepsilon")} (degeneracy ${g1}). Find the heat capacity ${m("C_V/Nk_B")}. ${X_DEF}`);
}

function cvOscillator(r: Rng): Draft {
  const n3 = r.chance(0.5);
  const k = n3 ? 3 : 1;
  return exactExpr(`${k}*x^2*exp(x)/(exp(x) - 1)^2`, `\\frac{${cf(k, "x^2e^{x}")}}{(e^{x} - 1)^2}`, "Cv/Nk", "\\frac{C_V}{Nk_B}", [
    `One oscillator: ${m("\\frac{U}{\\varepsilon} = \\frac{1}{2} + \\frac{1}{e^{x} - 1}")} (the zero-point term does not depend on ${m("T")}).`,
    `${m("\\frac{C}{k_B} = -x^2\\frac{d(U/\\varepsilon)}{dx} = \\frac{x^2e^{x}}{(e^{x} - 1)^2}")}${n3 ? `; three independent directions per atom triple it` : ""}.`,
    m(`\\frac{C_V}{Nk_B} = \\frac{${cf(k, "x^2e^{x}")}}{(e^{x} - 1)^2}`),
  ], { sm: "cv-ho", k },
  n3
    ? `An Einstein solid of ${m("N")} atoms, each vibrating independently in 3 directions with quantum ${m("\\varepsilon = h\\nu")}. Find ${m("C_V/Nk_B")}. ${X_DEF}`
    : `${m("N")} independent 1-D quantum harmonic oscillators with quantum ${m("\\varepsilon = h\\nu")}. Find ${m("C_V/Nk_B")}. ${X_DEF}`);
}

const DIATOMIC_VIB = [
  { name: "N₂", th: 3374 }, { name: "O₂", th: 2256 }, { name: "CO", th: 3122 }, { name: "HCl", th: 4303 },
  { name: "Cl₂", th: 805 }, { name: "Br₂", th: 463 }, { name: "I₂", th: 308 }, { name: "F₂", th: 1320 },
];
function cvDiatomicGas(r: Rng): Draft {
  const mol = r.pick(DIATOMIC_VIB);
  const T = r.pick([300, 500, 1000, 1500, 2000]);
  const x = mol.th / T;
  const vib = (R * x * x * Math.exp(x)) / (Math.exp(x) - 1) ** 2;
  const cv = 2.5 * R + vib;
  return numeric(cv, "Cv", "C_{V,m}", "J/(mol·K)", [
    `Translation ${m("\\tfrac32R")} + rotation ${m("R")} (fully active, ${m("T \\gg \\theta_{rot}")}) + one vibration (quantum, Einstein function).`,
    m(`x = \\frac{\\theta_{vib}}{T} = ${fmt(x, 4)},\\quad C_{vib} = R\\frac{x^2e^{x}}{(e^{x}-1)^2} = ${fmt(vib, 4)}\\,\\mathrm{J\\,mol^{-1}K^{-1}}`),
    m(`C_{V,m} = \\tfrac52(8.314) + ${fmt(vib, 4)} = ${fmt(cv)}\\,\\mathrm{J\\,mol^{-1}K^{-1}}`),
  ], { sm: "cv-gas", th: mol.th, T },
  `${mol.name} gas has ${m(`\\theta_{vib} = ${vu(mol.th, "K")}`)}. Find its molar heat capacity ${m("C_{V,m}")} at ${m(vu(T, "K"))} (ideal gas; translation and rotation classical, vibration quantum).`);
}

// ═══ stat.fluctuations — Shell Ch 17 ═══════════════════════════════════════
function flTwoLevel(r: Rng): Draft {
  const g0 = r.int(1, 3);
  const g1 = r.int(1, 3);
  const { qTex, qJs } = twoLevelTex(g0, g1);
  return exactExpr(`${g0 * g1}*exp(-x)/${qJs}^2`, `\\frac{${cf(g0 * g1, "e^{-x}")}}{\\left(${qTex}\\right)^2}`, "σ²/ε²", "\\frac{\\langle E^2\\rangle - \\langle E\\rangle^2}{\\varepsilon^2}", [
    `With ${m(`p_1 = \\frac{${cf(g1, "e^{-x}")}}{${qTex}}`)}: ${m("\\langle E\\rangle = \\varepsilon p_1")} and ${m("\\langle E^2\\rangle = \\varepsilon^2p_1")}.`,
    `${m("\\sigma_E^2 = \\varepsilon^2p_1(1 - p_1)")}, with ${m(`1 - p_1 = \\frac{${g0}}{${qTex}}`)}.`,
    m(`\\frac{\\sigma_E^2}{\\varepsilon^2} = \\frac{${cf(g0 * g1, "e^{-x}")}}{\\left(${qTex}\\right)^2}`),
  ], { sm: "fl-two", g0, g1 },
  `One two-level system (ground ${m("0")}, degeneracy ${g0}; excited ${m("\\varepsilon")}, degeneracy ${g1}) is in contact with a bath at ${m("T")}. Find the energy variance ${m("(\\langle E^2\\rangle - \\langle E\\rangle^2)/\\varepsilon^2")}. ${X_DEF}`);
}

function flExact(r: Rng): Draft {
  const a = r.pick([2, 3, 4]);
  const gs = [r.int(1, 3), r.int(1, 3), r.int(1, 3)];
  const ws = gs.map((gi, i) => gi * a ** (2 - i));
  const Z = ws[0] + ws[1] + ws[2];
  const s1 = ws[1] + 2 * ws[2];
  const s2 = ws[1] + 4 * ws[2];
  const mean = new Q(s1, Z);
  const sq = new Q(s2, Z);
  const v = sq.sub(mean.mul(mean));
  return exactQ(v, "σ²/ε²", "\\sigma_E^2/\\varepsilon^2", [
    `Each step up costs ${m(`e^{-\\varepsilon/k_BT} = 1/${a}`)}; weights ${m(`\\propto ${ws.join(" : ")}`)} for ${m("0, \\varepsilon, 2\\varepsilon")} (multiply through by ${a * a}).`,
    m(`\\frac{\\langle E\\rangle}{\\varepsilon} = \\frac{${ws[1]} + 2(${ws[2]})}{${Z}} = ${mean.tex()},\\quad \\frac{\\langle E^2\\rangle}{\\varepsilon^2} = \\frac{${ws[1]} + 4(${ws[2]})}{${Z}} = ${sq.tex()}`),
    m(`\\frac{\\sigma_E^2}{\\varepsilon^2} = ${sq.tex()} - \\left(${mean.tex()}\\right)^2 = ${v.tex()}`),
  ], { sm: "fl-exact", a, gs },
  `A molecule has levels ${m("0, \\varepsilon, 2\\varepsilon")} with degeneracies ${m(`${gs[0]}, ${gs[1]}, ${gs[2]}`)}. At the temperature where ${m(`k_BT = \\varepsilon/\\ln ${a}`)}, find ${m("(\\langle E^2\\rangle - \\langle E\\rangle^2)/\\varepsilon^2")} for one molecule. (Exact fraction.)`);
}

const NS = [
  { N: 6, tex: "6" }, { N: 24, tex: "24" }, { N: 150, tex: "150" }, { N: 600, tex: "600" },
  { N: 1e6, tex: "10^{6}" }, { N: 1e12, tex: "10^{12}" }, { N: 1e20, tex: "10^{20}" }, { N: NA, tex: "6.022\\times10^{23}" },
];
function flRelative(r: Rng): Draft {
  const { N, tex } = r.pick(NS);
  const rel = Math.sqrt(2 / (3 * N));
  return numeric(rel, "σ/⟨E⟩", "\\sigma_E/\\langle E\\rangle", "", [
    `${m("\\sigma_E^2 = k_BT^2C_V")}. Monatomic ideal gas: ${m("\\langle E\\rangle = \\tfrac32Nk_BT")}, ${m("C_V = \\tfrac32Nk_B")}.`,
    m(`\\frac{\\sigma_E}{\\langle E\\rangle} = \\frac{\\sqrt{\\tfrac32Nk_B^2T^2}}{\\tfrac32Nk_BT} = \\sqrt{\\frac{2}{3N}}`),
    m(`\\sqrt{\\frac{2}{3(${tex})}} = ${fmt(rel)}`),
  ], { sm: "fl-rel", N }, `A monatomic ideal gas of ${m(`N = ${tex}`)} atoms is held at fixed ${m("T")} and ${m("V")}. Find the relative energy fluctuation ${m("\\sigma_E/\\langle E\\rangle")}.`);
}

function flCv(r: Rng): Draft {
  const Cv = r.pick([5, 10, 20, 30, 50]);
  const T = r.pick([280, 300, 310, 330, 350]);
  const sigma = Math.sqrt(R * T * T * Cv * 1000) / 1000;
  return numeric(sigma, "σ_E", "\\sigma_E", "kJ/mol", [
    `${m("\\langle E^2\\rangle - \\langle E\\rangle^2 = k_BT^2C_V")} per molecule. Per mole of molecules (each fluctuating on its own): ${m("\\sigma_{E,m} = \\sqrt{RT^2C_{V,m}}")}.`,
    `${m(`C_{V,m} = ${g(Cv * 1000)}\\,\\mathrm{J\\,mol^{-1}K^{-1}}`)} — convert kJ to J first.`,
    m(`\\sigma_E = \\sqrt{(8.314)(${T})^2(${g(Cv * 1000)})} = ${fmt(sigma * 1000)}\\,\\mathrm{J/mol} = ${fmt(sigma)}\\,\\mathrm{kJ/mol}`),
  ], { sm: "fl-cv", Cv, T },
  `A protein has heat capacity ${m(`C_{V,m} = ${vu(Cv, "kJ/(mol·K)")}`)} at ${m(vu(T, "K"))}. Find the rms fluctuation of one molecule's energy, ${m("\\sigma_E")}, in kJ/mol.`);
}

function flOscillator(r: Rng): Draft {
  const zp = r.chance(0.5);
  return exactExpr("exp(x)/(exp(x) - 1)^2", "\\frac{e^{x}}{(e^{x} - 1)^2}", "σ²/ε²", "\\frac{\\sigma_E^2}{\\varepsilon^2}", [
    `${m("\\sigma_E^2 = \\partial^2\\ln q/\\partial\\beta^2 = -\\partial\\langle E\\rangle/\\partial\\beta")}${zp ? " — the zero-point shift moves every level equally, so it drops out" : ""}.`,
    `${m(`\\langle E\\rangle = \\frac{\\varepsilon}{e^{\\beta\\varepsilon} - 1}${zp ? " + \\tfrac{\\varepsilon}{2}" : ""}`)}, and ${m("-\\frac{\\partial}{\\partial\\beta}\\frac{\\varepsilon}{e^{\\beta\\varepsilon} - 1} = \\frac{\\varepsilon^2e^{\\beta\\varepsilon}}{(e^{\\beta\\varepsilon} - 1)^2}")}.`,
    m("\\frac{\\sigma_E^2}{\\varepsilon^2} = \\frac{e^{x}}{(e^{x} - 1)^2}"),
  ], { sm: "fl-ho", zp },
  `One quantum harmonic oscillator, levels ${zp ? m("E_v = (v + \\tfrac12)\\varepsilon") : m("E_v = v\\varepsilon")}, is in contact with a bath at ${m("T")}. Find ${m("(\\langle E^2\\rangle - \\langle E\\rangle^2)/\\varepsilon^2")}. ${X_DEF}`);
}

// ═══ stat.ensembles — Shell Ch 19 ══════════════════════════════════════════
function ensSite(r: Rng): Draft {
  const eps = r.pick([5, 10, 15, 20]);
  const mu = r.pick([-5, -10, -15, -20, -25]);
  const T = r.pick([280, 300, 350]);
  const y = Math.exp(((mu + eps) * 1000) / (R * T));
  const occ = y / (1 + y);
  const empty = r.chance(0.3);
  const val = empty ? 1 - occ : occ;
  require_(val > 1e-3 && val < 0.999);
  return numeric(val, empty ? "P(empty)" : "⟨n⟩", empty ? "P_0" : "\\langle n\\rangle", "", [
    `Grand canonical, one site: ${m("\\Xi = \\sum_n e^{-\\beta(E_n - \\mu n)} = 1 + e^{\\beta(\\mu + \\varepsilon)}")} (occupied energy ${m("-\\varepsilon")}).`,
    m(`\\beta(\\mu + \\varepsilon) = \\frac{(${mu} + ${eps})\\times10^{3}}{(8.314)(${T})} = ${fmt(((mu + eps) * 1000) / (R * T), 4)},\\quad e^{\\beta(\\mu+\\varepsilon)} = ${fmt(y, 4)}`),
    empty ? m(`P_0 = \\frac{1}{\\Xi} = \\frac{1}{1 + ${fmt(y, 4)}} = ${fmt(val)}`) : m(`\\langle n\\rangle = \\frac{${fmt(y, 4)}}{1 + ${fmt(y, 4)}} = ${fmt(val)}`),
  ], { sm: "ens-site", eps, mu, T, empty },
  `A surface site holds at most one molecule; an adsorbed molecule has energy ${m(`-\\varepsilon = ${vu(-eps, "kJ/mol")}`)}. The site exchanges molecules with a gas at chemical potential ${m(`\\mu = ${vu(mu, "kJ/mol")}`)} and ${m(vu(T, "K"))}. Find ${empty ? "the probability that the site is empty" : `the average occupancy ${m("\\langle n\\rangle")}`}.`);
}

const Z_OPTS = [2, 3, 4, 5, 10];
const F_OPTS = [2, 3, 4, 5, 6, 10];
function ensLattice(r: Rng): Draft {
  const M = r.int(2, 6);
  const zd = r.pick(Z_OPTS);
  const f = r.pick(F_OPTS);
  require_(f !== zd);
  const y = new Q(f, zd);
  const N = y.mul(M).div(y.add(1));
  return exactQ(N, "⟨N⟩", "\\langle N\\rangle", [
    `Independent sites: ${m("\\Xi = (1 + \\lambda e^{\\beta\\varepsilon})^M")} with ${m(`\\lambda e^{\\beta\\varepsilon} = \\frac{1}{${zd}}\\cdot${f} = ${y.tex()}`)}.`,
    `${m("\\langle N\\rangle = \\lambda\\frac{\\partial\\ln\\Xi}{\\partial\\lambda} = M\\frac{\\lambda e^{\\beta\\varepsilon}}{1 + \\lambda e^{\\beta\\varepsilon}}")}.`,
    m(`\\langle N\\rangle = ${M}\\cdot\\frac{${y.tex()}}{1 + ${y.tex()}} = ${N.tex()}`),
  ], { sm: "ens-lattice", M, zd, f },
  `A molecule has ${M} independent binding sites, each empty or singly occupied with energy ${m("-\\varepsilon")}. It is in contact with a reservoir where ${m(`\\lambda = e^{\\beta\\mu} = 1/${zd}`)}, and ${m(`e^{\\beta\\varepsilon} = ${f}`)}. Find the average number bound, ${m("\\langle N\\rangle")}. (Exact fraction.)`);
}

function ensNFluct(r: Rng): Draft {
  const M = r.int(2, 6);
  const zd = r.pick(Z_OPTS);
  const f = r.pick(F_OPTS);
  require_(f !== zd);
  const y = new Q(f, zd);
  const v = y.mul(M).div(y.add(1).mul(y.add(1)));
  return exactQ(v, "σ_N²", "\\langle N^2\\rangle - \\langle N\\rangle^2", [
    `${m("\\sigma_N^2 = \\lambda\\frac{\\partial\\langle N\\rangle}{\\partial\\lambda}")}; independent sites each contribute ${m("\\theta(1 - \\theta)")}, ${m("\\theta = \\frac{y}{1 + y}")}, ${m(`y = \\lambda e^{\\beta\\varepsilon} = ${y.tex()}`)}.`,
    m(`\\theta = ${y.div(y.add(1)).tex()},\\quad \\sigma_N^2 = ${M}\\cdot${y.div(y.add(1)).tex()}\\cdot${new Q(1).div(y.add(1)).tex()} = ${v.tex()}`),
  ], { sm: "ens-nfluct", M, zd, f },
  `${M} independent sites, each empty or singly occupied with energy ${m("-\\varepsilon")}, exchange molecules with a reservoir at ${m(`\\lambda = e^{\\beta\\mu} = 1/${zd}`)}; ${m(`e^{\\beta\\varepsilon} = ${f}`)}. Find the particle-number variance ${m("\\langle N^2\\rangle - \\langle N\\rangle^2")}. (Exact fraction.)`);
}

const Y_OPTS = [new Q(1, 2), new Q(1), new Q(2), new Q(3), new Q(1, 3)];
const W_OPTS = [new Q(1, 4), new Q(1, 2), new Q(2), new Q(4), new Q(3)];
function ensPair(r: Rng): Draft {
  const y = r.pick(Y_OPTS);
  const w = r.pick(W_OPTS);
  const Xi = new Q(1).add(y.mul(2)).add(y.mul(y).mul(w));
  const num = y.mul(2).add(y.mul(y).mul(w).mul(2));
  const N = num.div(Xi);
  return exactQ(N, "⟨N⟩", "\\langle N\\rangle", [
    `States: empty (weight 1), one ligand in either pocket (2 states, ${m(`y = ${y.tex()}`)} each), both pockets (${m(`y^2w = ${y.mul(y).mul(w).tex()}`)}).`,
    m(`\\Xi = 1 + 2(${y.tex()}) + ${y.mul(y).mul(w).tex()} = ${Xi.tex()}`),
    m(`\\langle N\\rangle = \\frac{1\\cdot 2y + 2\\cdot y^2w}{\\Xi} = \\frac{${num.tex()}}{${Xi.tex()}} = ${N.tex()}`),
  ], { sm: "ens-pair", y: [y.n, y.d], w: [w.n, w.d] },
  `A protein has two identical binding pockets. Each bound ligand contributes a factor ${m(`y = \\lambda e^{-\\beta\\varepsilon_b} = ${y.tex()}`)}, and when both are filled an interaction multiplies the weight by ${m(`w = e^{-\\beta J} = ${w.tex()}`)}. Find the average number of ligands bound, ${m("\\langle N\\rangle")}. (Exact fraction.)`);
}

function ensIsobaric(r: Rng): Draft {
  const dE = r.pick([2, 5, 10, 15]);
  const dV = r.pick([-100, -50, -30, -20, 20, 50]);
  const p = r.pick([1, 1000, 2000, 3000, 5000]);
  const T = r.pick([298, 300, 310]);
  const pV = p * 1e5 * dV * 1e-6; // J/mol
  const ratio = Math.exp(-(dE * 1000 + pV) / (R * T));
  require_(ratio > 1e-6 && ratio < 1e6);
  return numeric(ratio, "P_B/P_A", "P_B/P_A", "", [
    `Isothermal–isobaric ensemble: each state weighs ${m("e^{-\\beta(E + pV)}")}, so ${m("\\frac{P_B}{P_A} = e^{-(\\Delta E + p\\Delta V)/RT}")}.`,
    m(`p\\Delta V = (${g(p * 1e5)}\\,\\mathrm{Pa})(${g(dV * 1e-6)}\\,\\mathrm{m^3/mol}) = ${fmt(pV)}\\,\\mathrm{J/mol}`),
    m(`\\frac{P_B}{P_A} = \\exp\\left(-\\frac{${g(dE * 1000)} + (${fmt(pV)})}{(8.314)(${T})}\\right) = ${fmt(ratio)}`),
  ], { sm: "ens-isobaric", dE, dV, p, T },
  `A protein switches between conformations A and B; B is ${m(vu(dE, "kJ/mol"))} higher in energy and its molar volume differs by ${m(`\\Delta V = V_B - V_A = ${vu(dV, "mL/mol")}`)}. At ${m(`${g(p)}\\,\\mathrm{bar}`)} and ${m(vu(T, "K"))}, find ${m("P_B/P_A")}.`);
}

// ═══ stat.binding — D&B Ch 26–28 ═══════════════════════════════════════════
const K_OPTS = [new Q(1, 2), new Q(2), new Q(3), new Q(4), new Q(5), new Q(10)];
const P_PRESS = [new Q(1, 4), new Q(1, 2), new Q(1), new Q(2), new Q(3)];
const dec = (q: Q) => `${q.value()}`;
function bindTheta(r: Rng): Draft {
  if (r.chance(0.5)) {
    const K = r.pick(K_OPTS);
    const p = r.pick(P_PRESS);
    const Kp = K.mul(p);
    const th = Kp.div(Kp.add(1));
    return exactQ(th, "θ", "\\theta", [
      `Each site: empty (weight 1) or occupied (weight ${m("Kp")}). Site partition function ${m("q = 1 + Kp")}, so ${m("\\theta = \\frac{Kp}{1 + Kp}")}.`,
      m(`Kp = (${dec(K)})(${dec(p)}) = ${Kp.tex()},\\quad \\theta = \\frac{${Kp.tex()}}{1 + ${Kp.tex()}} = ${th.tex()}`),
    ], { sm: "bind-theta", K: [K.n, K.d], x: [p.n, p.d], mode: "gas" },
    `A gas adsorbs on a surface following the Langmuir isotherm with ${m(`K = ${dec(K)}\\,\\mathrm{bar^{-1}}`)}. What fraction ${m("\\theta")} of sites is covered at ${m(`p = ${dec(p)}\\,\\mathrm{bar}`)}? (Exact fraction.)`);
  }
  const Kd = r.pick([1, 2, 5, 10, 20, 50]);
  const c = r.pick([1, 2, 5, 10, 20, 50, 100]);
  const th = new Q(c, Kd + c);
  return exactQ(th, "θ", "\\theta", [
    `One site in solution: weights 1 (empty) and ${m("c/K_d")} (bound), so ${m("\\theta = \\frac{c/K_d}{1 + c/K_d} = \\frac{c}{K_d + c}")}.`,
    m(`\\theta = \\frac{${c}}{${Kd} + ${c}} = ${th.tex()}`),
  ], { sm: "bind-theta", K: [1, Kd], x: [c, 1], mode: "solution" },
  `A receptor binds a ligand at a single site with ${m(`K_d = ${vu(Kd, "μM")}`)}. What fraction of receptors is bound at free ligand concentration ${m(vu(c, "μM"))}? (Exact fraction.)`);
}

function bindPressure(r: Rng): Draft {
  const K = r.pick([0.1, 0.5, 2, 4, 5, 10]);
  const th = r.pick([0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]);
  const p = th / (K * (1 - th));
  return numeric(p, "p", "p", "bar", [
    `Langmuir: ${m("\\theta = \\frac{Kp}{1 + Kp}")}. Solve for ${m("p")}: ${m("Kp = \\frac{\\theta}{1 - \\theta}")}.`,
    m(`p = \\frac{\\theta}{K(1 - \\theta)} = \\frac{${th}}{${K}(1 - ${th})} = ${fmt(p)}\\,\\mathrm{bar}`),
    th === 0.5 ? `At half coverage ${m("p = 1/K")}.` : `Note how much more pressure the last few percent of coverage costs.`,
  ], { sm: "bind-p", K, th }, `A gas adsorbs on a surface following the Langmuir isotherm with ${m(`K = ${vu(K, "bar⁻¹")}`)}. What pressure gives fractional coverage ${m(`\\theta = ${th}`)}?`);
}

const RATIOS = [new Q(1, 2), new Q(3, 2), new Q(2), new Q(3)];
function bindHill(r: Rng): Draft {
  const n = r.int(2, 4);
  const ratio = r.pick(RATIOS);
  require_(!(n === 4 && ratio.n === 3));
  const K = r.pick([2, 4, 6, 10, 20]);
  const c = ratio.mul(K);
  const rn = new Q(ratio.n ** n, ratio.d ** n);
  const th = rn.div(rn.add(1));
  return exactQ(th, "θ", "\\theta", [
    `Hill: ${m("\\theta = \\frac{(c/K_{1/2})^{n_H}}{1 + (c/K_{1/2})^{n_H}}")} — the all-or-none limit, where ${m("n_H")} ligands bind together.`,
    m(`\\frac{c}{K_{1/2}} = \\frac{${dec(c)}}{${K}} = ${ratio.tex()},\\quad \\left(${ratio.tex()}\\right)^{${n}} = ${rn.tex()}`),
    m(`\\theta = \\frac{${rn.tex()}}{1 + ${rn.tex()}} = ${th.tex()}`),
  ], { sm: "bind-hill", n, K, c: [c.n, c.d] },
  `A protein binds ligand cooperatively with Hill coefficient ${m(`n_H = ${n}`)} and half-saturation concentration ${m(`K_{1/2} = ${vu(K, "μM")}`)}. Find the fractional saturation ${m("\\theta")} at ${m(`c = ${dec(c)}\\,\\mu\\mathrm{M}`)}. (Exact fraction.)`);
}

function bindHillN(r: Rng): Draft {
  const n = r.pick([1.5, 2, 2.5, 2.8, 3, 3.5]);
  const K = r.pick([5, 10, 26]);
  const c1 = Number((K * r.pick([0.4, 0.5, 0.6, 0.8])).toPrecision(3));
  const c2 = Number((K * r.pick([1.25, 1.5, 2])).toPrecision(3));
  const hill = (c: number) => c ** n / (K ** n + c ** n);
  const t1 = sig3(hill(c1));
  const t2 = sig3(hill(c2));
  require_(t1 > 0.005 && t2 < 0.995);
  const lo = (t: number) => Math.log(t / (1 - t));
  const nH = (lo(t2) - lo(t1)) / Math.log(c2 / c1);
  const unitTex = K === 26 ? "\\mathrm{Torr}" : "\\mu\\mathrm{M}";
  return numeric(nH, "n_H", "n_H", "", [
    `Hill plot: ${m("\\ln\\frac{\\theta}{1 - \\theta} = n_H\\ln c - n_H\\ln K_{1/2}")} — a straight line with slope ${m("n_H")}.`,
    m(`\\ln\\frac{${t1}}{${sig3(1 - t1)}} = ${fmt(lo(t1), 4)},\\quad \\ln\\frac{${t2}}{${sig3(1 - t2)}} = ${fmt(lo(t2), 4)}`),
    m(`n_H = \\frac{${fmt(lo(t2), 4)} - (${fmt(lo(t1), 4)})}{\\ln(${c2}/${c1})} = ${fmt(nH)}`),
  ], { sm: "bind-nh", c1, c2, t1, t2 },
  `${K === 26 ? "Hemoglobin" : "A cooperative receptor"} is ${m(`\\theta = ${t1}`)} saturated at ${m(`${c1}\\,${unitTex}`)} ${K === 26 ? "O₂ pressure" : "ligand"} and ${m(`\\theta = ${t2}`)} at ${m(`${c2}\\,${unitTex}`)}. Assuming the Hill equation holds between these points, find the Hill coefficient ${m("n_H")}.`);
}

const KDS = [
  { Kd: 1e-8, tex: "10\\,\\mathrm{nM}" }, { Kd: 5e-8, tex: "50\\,\\mathrm{nM}" }, { Kd: 1e-6, tex: "1\\,\\mu\\mathrm{M}" },
  { Kd: 5e-6, tex: "5\\,\\mu\\mathrm{M}" }, { Kd: 1e-4, tex: "100\\,\\mu\\mathrm{M}" },
];
const CONCS = [
  { c: 1e-6, tex: "1\\,\\mu\\mathrm{M}" }, { c: 1e-5, tex: "10\\,\\mu\\mathrm{M}" }, { c: 1e-4, tex: "100\\,\\mu\\mathrm{M}" }, { c: 1e-3, tex: "1\\,\\mathrm{mM}" },
];
function bindDG(r: Rng): Draft {
  const T = r.pick([298, 310]);
  if (r.chance(0.5)) {
    const { Kd, tex } = r.pick(KDS);
    const dG = (R * T * Math.log(Kd)) / 1000;
    return numeric(dG, "ΔG°", "\\Delta G^\\circ_{bind}", "kJ/mol", [
      `Binding constant ${m("K_a = 1/K_d")} (standard state 1 M): ${m("\\Delta G^\\circ = -RT\\ln K_a = RT\\ln(K_d/1\\,\\mathrm{M})")}.`,
      m(`\\Delta G^\\circ = (8.314)(${T})\\ln(${fmt(Kd)}) = ${fmt(dG * 1000)}\\,\\mathrm{J/mol} = ${fmt(dG)}\\,\\mathrm{kJ/mol}`),
    ], { sm: "bind-dg", Kd, T, variant: "dG" }, `A ligand binds its receptor with ${m(`K_d = ${tex}`)} at ${m(vu(T, "K"))}. Find the standard binding free energy ${m("\\Delta G^\\circ_{bind}")} (1 M standard state).`);
  }
  const dG = r.pick([-20, -25, -30, -35, -40]);
  const { c, tex } = r.pick(CONCS);
  const Kd = Math.exp((dG * 1000) / (R * T));
  const th = c / (Kd + c);
  require_(th > 0.01 && th < 0.99);
  return numeric(th, "θ", "\\theta", "", [
    `${m("K_d = e^{\\Delta G^\\circ/RT}")} in M: ${m(`K_d = \\exp\\frac{${dG * 1000}}{(8.314)(${T})} = ${fmt(Kd, 4)}\\,\\mathrm{M}`)}.`,
    `Single site: ${m("\\theta = \\frac{c}{K_d + c}")}.`,
    m(`\\theta = \\frac{${fmt(c)}}{${fmt(Kd, 4)} + ${fmt(c)}} = ${fmt(th)}`),
  ], { sm: "bind-dg", dG, T, c, variant: "theta" },
  `A drug binds a single site on its target with ${m(`\\Delta G^\\circ_{bind} = ${vu(dG, "kJ/mol")}`)} (1 M standard state) at ${m(vu(T, "K"))}. What fraction of targets is bound at a free drug concentration of ${m(tex)}?`);
}

// ═══ stat.rates — D&B Ch 19; Shell Ch 21 ═══════════════════════════════════
const EAS = [40, 50, 60, 75, 80, 100, 120];
const arr = (A: number, Ea: number, T: number) => A * Math.exp((-Ea * 1000) / (R * T));

function rateEa(r: Rng): Draft {
  const Ea = r.pick(EAS);
  const A = r.pick([1e10, 1e12, 1e13]);
  const T1 = r.pick([280, 290, 298, 300, 310]);
  const T2 = T1 + r.pick([10, 20, 30, 50]);
  const k1 = sig3(arr(A, Ea, T1));
  const k2 = sig3(arr(A, Ea, T2));
  const val = (R * Math.log(k2 / k1)) / (1 / T1 - 1 / T2) / 1000;
  return numeric(val, "Ea", "E_a", "kJ/mol", [
    `Divide the two Arrhenius equations; ${m("A")} cancels: ${m("\\ln\\frac{k_2}{k_1} = \\frac{E_a}{R}\\left(\\frac{1}{T_1} - \\frac{1}{T_2}\\right)")}.`,
    m(`\\ln\\frac{${fmt(k2)}}{${fmt(k1)}} = ${fmt(Math.log(k2 / k1), 4)},\\quad \\frac{1}{${T1}} - \\frac{1}{${T2}} = ${fmt(1 / T1 - 1 / T2, 4)}\\,\\mathrm{K^{-1}}`),
    m(`E_a = \\frac{(8.314)(${fmt(Math.log(k2 / k1), 4)})}{${fmt(1 / T1 - 1 / T2, 4)}} = ${fmt(val * 1000)}\\,\\mathrm{J/mol} = ${fmt(val)}\\,\\mathrm{kJ/mol}`),
  ], { sm: "rate-ea", k1, k2, T1, T2 },
  `A first-order reaction has ${m(`k = ${fmt(k1)}\\,\\mathrm{s^{-1}}`)} at ${m(vu(T1, "K"))} and ${m(`k = ${fmt(k2)}\\,\\mathrm{s^{-1}}`)} at ${m(vu(T2, "K"))}. Find the activation energy ${m("E_a")}.`);
}

function rateK2(r: Rng): Draft {
  const Ea = r.pick(EAS);
  const T1 = r.pick([290, 298, 300, 310]);
  const T2 = T1 + r.pick([-20, -10, 10, 25, 40, 60]);
  const k1 = sig3(arr(1e12, Ea, T1));
  const k2 = k1 * Math.exp(((-Ea * 1000) / R) * (1 / T2 - 1 / T1));
  return numeric(k2, "k₂", "k_2", "s⁻¹", [
    m("\\ln\\frac{k_2}{k_1} = -\\frac{E_a}{R}\\left(\\frac{1}{T_2} - \\frac{1}{T_1}\\right)"),
    m(`-\\frac{${Ea * 1000}}{8.314}\\left(\\frac{1}{${T2}} - \\frac{1}{${T1}}\\right) = ${fmt(Math.log(k2 / k1), 4)}`),
    m(`k_2 = (${fmt(k1)})e^{${fmt(Math.log(k2 / k1), 4)}} = ${fmt(k2)}\\,\\mathrm{s^{-1}}`),
  ], { sm: "rate-k2", Ea, k1, T1, T2 },
  `A reaction with ${m(`E_a = ${vu(Ea, "kJ/mol")}`)} has ${m(`k = ${fmt(k1)}\\,\\mathrm{s^{-1}}`)} at ${m(vu(T1, "K"))}. Find ${m("k")} at ${m(vu(T2, "K"))}.`);
}

function rateFactor(r: Rng): Draft {
  const T1c = r.pick([0, 10, 20, 25, 37]);
  const dT = r.pick([10, 20, 30]);
  const T1 = T1c + 273.15;
  const T2 = T1 + dT;
  if (r.chance(0.5)) {
    const Ea = r.pick(EAS);
    const f = Math.exp(((Ea * 1000) / R) * (1 / T1 - 1 / T2));
    return numeric(f, "k₂/k₁", "k_2/k_1", "", [
      `${m("A")} cancels in the ratio: ${m("\\frac{k_2}{k_1} = \\exp\\left[\\frac{E_a}{R}\\left(\\frac{1}{T_1} - \\frac{1}{T_2}\\right)\\right]")}, temperatures in kelvin.`,
      m(`T_1 = ${g(T1)}\\,\\mathrm{K},\\ T_2 = ${g(T2)}\\,\\mathrm{K}:\\quad \\frac{k_2}{k_1} = \\exp\\left[\\frac{${Ea * 1000}}{8.314}(${fmt(1 / T1 - 1 / T2, 4)})\\right] = ${fmt(f)}`),
    ], { sm: "rate-factor", Ea, T1, T2, variant: "factor" },
    `A reaction has ${m(`E_a = ${vu(Ea, "kJ/mol")}`)}. By what factor does its rate constant increase from ${m(`${T1c}^\\circ\\mathrm{C}`)} to ${m(`${T1c + dT}^\\circ\\mathrm{C}`)}?`);
  }
  const fac = r.pick([2, 3, 10]);
  const Ea = (R * Math.log(fac)) / (1 / T1 - 1 / T2) / 1000;
  return numeric(Ea, "Ea", "E_a", "kJ/mol", [
    m(`\\ln ${fac} = \\frac{E_a}{R}\\left(\\frac{1}{T_1} - \\frac{1}{T_2}\\right),\\quad T \\text{ in kelvin}`),
    m(`E_a = \\frac{(8.314)\\ln ${fac}}{1/${g(T1)} - 1/${g(T2)}} = ${fmt(Ea * 1000)}\\,\\mathrm{J/mol} = ${fmt(Ea)}\\,\\mathrm{kJ/mol}`),
  ], { sm: "rate-factor", fac, T1, T2, variant: "Ea" },
  `What activation energy makes a rate constant ${fac === 2 ? "double" : fac === 3 ? "triple" : "increase tenfold"} between ${m(`${T1c}^\\circ\\mathrm{C}`)} and ${m(`${T1c + dT}^\\circ\\mathrm{C}`)}?`);
}

function rateEyring(r: Rng): Draft {
  const dH = r.pick([50, 60, 70, 80, 90]);
  const dS = r.pick([-50, -20, 0, 10, 30]);
  const T = r.pick([298, 300, 310, 350]);
  const pre = (KB * T) / H;
  const dG = dH * 1000 - T * dS;
  const k = pre * Math.exp(-dG / (R * T));
  return numeric(k, "k", "k", "s⁻¹", [
    `Eyring: ${m("k = \\frac{k_BT}{h}e^{-\\Delta G^\\ddagger/RT}")}, with ${m("\\Delta G^\\ddagger = \\Delta H^\\ddagger - T\\Delta S^\\ddagger")} (ΔS‡ in J, ΔH‡ in kJ — match units).`,
    m(`\\frac{k_BT}{h} = ${fmt(pre, 4)}\\,\\mathrm{s^{-1}},\\quad \\Delta G^\\ddagger = ${dH * 1000} - (${T})(${dS}) = ${fmt(dG, 4)}\\,\\mathrm{J/mol}`),
    m(`k = (${fmt(pre, 4)})\\exp\\left(-\\frac{${fmt(dG, 4)}}{(8.314)(${T})}\\right) = ${fmt(k)}\\,\\mathrm{s^{-1}}`),
  ], { sm: "rate-eyring", dH, dS, T },
  `A unimolecular reaction has ${m(`\\Delta H^\\ddagger = ${vu(dH, "kJ/mol")}`)} and ${m(`\\Delta S^\\ddagger = ${vu(dS, "J/(mol·K)")}`)}. Use transition-state theory to find ${m("k")} at ${m(vu(T, "K"))}.`);
}

function rateDG(r: Rng): Draft {
  const dGtrue = r.pick([55, 60, 65, 70, 75, 80, 90, 100]);
  const T = r.pick([298, 300, 310, 350]);
  const pre = (KB * T) / H;
  const k = sig3(pre * Math.exp((-dGtrue * 1000) / (R * T)));
  const dG = (R * T * Math.log(pre / k)) / 1000;
  return numeric(dG, "ΔG‡", "\\Delta G^\\ddagger", "kJ/mol", [
    `Invert Eyring: ${m("\\Delta G^\\ddagger = RT\\ln\\frac{k_BT}{hk}")}.`,
    m(`\\frac{k_BT}{h} = ${fmt(pre, 4)}\\,\\mathrm{s^{-1}},\\quad \\ln\\frac{${fmt(pre, 4)}}{${fmt(k)}} = ${fmt(Math.log(pre / k), 4)}`),
    m(`\\Delta G^\\ddagger = (8.314)(${T})(${fmt(Math.log(pre / k), 4)}) = ${fmt(dG)}\\,\\mathrm{kJ/mol}`),
  ], { sm: "rate-dg", k, T },
  `An enzyme-catalysed step has ${m(`k = ${fmt(k)}\\,\\mathrm{s^{-1}}`)} at ${m(vu(T, "K"))}. Use the Eyring equation to find ${m("\\Delta G^\\ddagger")}.`);
}

export const STAT_TEMPLATES: Record<string, (r: Rng) => Draft> = {
  "sm-perm": perm,
  "sm-comb": comb,
  "sm-binom": binomProb,
  "sm-anagram": anagram,
  "sm-atleast": atLeastOne,
  "sm-two-state": twoState,
  "sm-einstein-w": einsteinW,
  "sm-ds-two-state": dSTwoState,
  "sm-ds-volume": dSVolume,
  "sm-einstein-share": einsteinShare,
  "sm-bz-ratio": bzRatio,
  "sm-bz-fraction": bzFraction,
  "sm-bz-temperature": bzTemperature,
  "sm-bz-exact": bzExact,
  "sm-pf-q": pfQ,
  "sm-pf-u-two-level": pfU2,
  "sm-pf-s-two-level": pfS2,
  "sm-pf-u-oscillator": pfUho,
  "sm-pf-f": pfF,
  "sm-ig-lambda": igLambda,
  "sm-ig-qtrans": igQtrans,
  "sm-ig-theta-rot": igThetaRot,
  "sm-ig-qrot": igQrot,
  "sm-ig-qvib": igQvib,
  "sm-cv-equipartition": cvEquipartition,
  "sm-cv-einstein": cvEinstein,
  "sm-cv-two-level": cvTwoLevel,
  "sm-cv-oscillator": cvOscillator,
  "sm-cv-diatomic": cvDiatomicGas,
  "sm-fl-two-level": flTwoLevel,
  "sm-fl-exact": flExact,
  "sm-fl-relative": flRelative,
  "sm-fl-cv": flCv,
  "sm-fl-oscillator": flOscillator,
  "sm-ens-site": ensSite,
  "sm-ens-lattice": ensLattice,
  "sm-ens-n-fluct": ensNFluct,
  "sm-ens-pair": ensPair,
  "sm-ens-isobaric": ensIsobaric,
  "sm-bind-langmuir": bindTheta,
  "sm-bind-pressure": bindPressure,
  "sm-bind-hill": bindHill,
  "sm-bind-hill-n": bindHillN,
  "sm-bind-dg": bindDG,
  "sm-rate-ea": rateEa,
  "sm-rate-k2": rateK2,
  "sm-rate-factor": rateFactor,
  "sm-rate-eyring": rateEyring,
  "sm-rate-dg": rateDG,
};
