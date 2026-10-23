// Consecutive first-order reactions A →(k1) B →(k2) C as a linear system.
//   d/dt [A, B]ᵀ = M [A, B]ᵀ,  M = [[-k1, 0], [k1, -k2]],   C = A0 + B0 + C0 − A − B
// Solved by the eigenvalue method on the 2×2 (A, B) block; C is a conservation leftover.
// Rate constants in min⁻¹, concentrations in mol/L, t in minutes.
import { Rng } from "./rng";
import type { Draft } from "./types";
import { ct, ex, join, m } from "./tex";
import { Q } from "./rational";
import { require_ } from "./reject";

interface Rxn {
  k1: number;
  k2: number;
  A0: number;
  B0: number;
}

function rxn(r: Rng, opts: { equal?: boolean; b0?: boolean } = {}): Rxn {
  const k1 = r.int(1, 5);
  const k2 = opts.equal ? k1 : r.int(1, 5);
  if (!opts.equal) require_(k1 !== k2);
  const A0 = r.pick([1, 2, 3, 4, 5, 6, 10]);
  const B0 = opts.b0 ? r.pick([1, 2, 3]) : 0;
  return { k1, k2, A0, B0 };
}

const scheme = (R: Rxn) =>
  `${m(`A \\xrightarrow{k_1} B \\xrightarrow{k_2} C`)} with ${m(`k_1 = ${R.k1}`)} and ${m(`k_2 = ${R.k2}`)} min⁻¹`;
const init = (R: Rxn) =>
  `${m(`[A]_0 = ${R.A0}`)} mol/L${R.B0 ? `, ${m(`[B]_0 = ${R.B0}`)} mol/L` : ", no B"} and no C at ${m("t = 0")}`;

const rateEqs = (R: Rxn) =>
  `${m(`\\frac{d[A]}{dt} = -${R.k1 === 1 ? "" : R.k1}[A]`)}, ${m(`\\frac{d[B]}{dt} = ${R.k1 === 1 ? "" : R.k1}[A] - ${R.k2 === 1 ? "" : R.k2}[B]`)}, ${m(`\\frac{d[C]}{dt} = ${R.k2 === 1 ? "" : R.k2}[B]`)}`;
const matTex = (R: Rxn) => `M = \\begin{pmatrix} -${R.k1} & 0 \\\\ ${R.k1} & -${R.k2} \\end{pmatrix}`;

/** [B](t): LaTeX, mathjs, and the eigen-method steps */
function bSolution(R: Rxn) {
  const { k1, k2, A0, B0 } = R;
  if (k1 === k2) {
    // double eigenvalue −k: B = (B0 + k A0 t) e^{−kt}
    const k = k1;
    const tex = B0 ? `(${join([`${B0}`, ct(k * A0, "t")])})${ex(-k, "t")}` : ct(k * A0, `t${ex(-k, "t")}`);
    return {
      tex,
      js: `(${B0} + ${k * A0}*t)*exp(-${k}*t)`,
      steps: [
        `${m(matTex(R))} has the double eigenvalue ${m(`-${k}`)} but only one eigenvector ${m("(0, 1)")}, so the two exponentials merge and a ${m(`te^{-${k === 1 ? "" : k}t}`)} term appears — the same repeated-root story as ${m("y'' + 2ky' + k^2y = 0")}.`,
        `${m(`[A] = ${ct(A0, ex(-k, "t"))}`)}; then ${m(`\\frac{d[B]}{dt} + ${k}[B] = ${k * A0}${ex(-k, "t")}`)}. Integrating factor ${m(ex(k, "t"))}: ${m(`(e^{${k === 1 ? "" : k}t}[B])' = ${k * A0}`)}, so ${m(`e^{${k === 1 ? "" : k}t}[B] = ${k * A0}t + ${B0}`)}.`,
      ],
    };
  }
  const d = k2 - k1;
  const c1 = new Q(A0, d); // multiplies (k2 − k1, k1) e^{−k1 t}
  const coef = new Q(k1 * A0, d); // B coefficient on e^{-k1 t}
  const c2 = new Q(B0).sub(coef); // B coefficient on e^{-k2 t}
  const tex = join([qt(coef, ex(-k1, "t")), qt(c2, ex(-k2, "t"))]);
  return {
    tex,
    js: `(${coef.n}/${coef.d})*exp(-${k1}*t) + (${c2.n}/${c2.d})*exp(-${k2}*t)`,
    steps: [
      `${m(matTex(R))} is lower triangular: eigenvalues ${m(`-${k1}`)} and ${m(`-${k2}`)} (the diagonal).`,
      `Eigenvectors: ${m(`\\lambda = -${k1}`)}: ${m(`(k_2 - k_1,\\ k_1) = (${d},\\ ${k1})`)}; ${m(`\\lambda = -${k2}`)}: ${m("(0,\\ 1)")}.`,
      `${m(`\\begin{pmatrix}[A]\\\\ {[B]}\\end{pmatrix} = c_1\\begin{pmatrix}${d}\\\\${k1}\\end{pmatrix}${ex(-k1, "t")} + c_2\\begin{pmatrix}0\\\\1\\end{pmatrix}${ex(-k2, "t")}`)}.`,
      `${m("t = 0")}: ${m(`${d}c_1 = ${A0}`)} and ${m(`${ct(k1, "c_1")} + c_2 = ${B0}`)}, so ${m(`c_1 = ${c1.tex()}`)}, ${m(`c_2 = ${c2.tex()}`)}.`,
    ],
  };
}

/** rational coefficient times body */
function qt(q: Q, body: string): string {
  if (q.isZero()) return "0";
  if (q.d === 1) return ct(q.n, body);
  const f = `\\frac{${Math.abs(q.n)}}{${q.d}}`;
  return `${q.n < 0 ? "-" : ""}${f}${body}`;
}

function kinMatrix(r: Rng): Draft {
  const R = rxn(r);
  return {
    prompt: `For ${scheme(R)}, write the rate equations for ${m("[A]")} and ${m("[B]")} as ${m("\\frac{d}{dt}\\begin{pmatrix}[A]\\\\ {[B]}\\end{pmatrix} = M\\begin{pmatrix}[A]\\\\ {[B]}\\end{pmatrix}")}. Enter the entries of ${m("M")}.`,
    answer: {
      kind: "tuple",
      fields: [
        { label: "M₁₁", tex: "M_{11}", ref: `${-R.k1}`, mode: "number" },
        { label: "M₁₂", tex: "M_{12}", ref: "0", mode: "number" },
        { label: "M₂₁", tex: "M_{21}", ref: `${R.k1}`, mode: "number" },
        { label: "M₂₂", tex: "M_{22}", ref: `${-R.k2}`, mode: "number" },
      ],
      vars: [],
    },
    answerTex: matTex(R),
    steps: [
      `Each step is first order: A is used up at ${m("k_1[A]")}; B is made at ${m("k_1[A]")} and used up at ${m("k_2[B]")}.`,
      `${rateEqs(R)}.`,
      `[C] doesn't feed back into A or B, so the system closes on the ${m("2\\times2")} block: ${m(matTex(R))}.`,
    ],
    meta: { variant: "matrix", ...R },
  };
}

function kinEigen(r: Rng): Draft {
  const R = rxn(r, { equal: r.chance(0.15) });
  const ev = R.k1 === R.k2 ? [-R.k1, -R.k1] : [-R.k1, -R.k2];
  return {
    prompt: `For ${scheme(R)}, find the eigenvalues of the ${m("2\\times2")} matrix ${m("M")} in ${m("\\frac{d}{dt}\\begin{pmatrix}[A]\\\\ {[B]}\\end{pmatrix} = M\\begin{pmatrix}[A]\\\\ {[B]}\\end{pmatrix}")}.`,
    answer: { kind: "roots", ref: ev, label: "λ" },
    answerTex: R.k1 === R.k2 ? `\\lambda = -${R.k1}\\ (\\text{double})` : `\\lambda = -${R.k1},\\ -${R.k2}`,
    steps: [
      `${m(matTex(R))}.`,
      `${m(`\\det(M - \\lambda I) = (-${R.k1} - \\lambda)(-${R.k2} - \\lambda) = 0`)} — a triangular matrix's eigenvalues are its diagonal entries.`,
      `${m(R.k1 === R.k2 ? `\\lambda = -${R.k1}` : `\\lambda = -${R.k1},\\ -${R.k2}`)}${R.k1 === R.k2 ? " (double)" : ""}: each is minus a rate constant, so every term decays.`,
    ],
    meta: { variant: "eigen", ...R },
  };
}

function kinB(r: Rng): Draft {
  const R = rxn(r, { equal: r.chance(0.2), b0: r.chance(0.3) });
  const B = bSolution(R);
  return {
    prompt: `For ${scheme(R)}, ${init(R)}: find ${m("[B](t)")}.`,
    answer: { kind: "expression", ref: B.js, vars: ["t"], label: "[B](t)" },
    answerTex: `[B](t) = ${B.tex}`,
    steps: [
      `${rateEqs(R)}.`,
      ...B.steps,
      m(`[B](t) = ${B.tex}`),
      `Check: ${m(`[B](0) = ${R.B0}`)} and ${m("[B] \\to 0")} as ${m("t \\to \\infty")} (it all ends up as C).`,
    ],
    meta: { variant: "B", ...R },
  };
}

function kinC(r: Rng): Draft {
  const R = rxn(r, { equal: r.chance(0.15) });
  const B = bSolution(R);
  const A = ct(R.A0, ex(-R.k1, "t"));
  const cJs = `${R.A0} - ${R.A0}*exp(-${R.k1}*t) - (${B.js})`;
  // C = A0 − A − B, simplified for display
  let cTex: string;
  if (R.k1 === R.k2) cTex = `${R.A0} - ${R.A0}${ex(-R.k1, "t")} - ${B.tex}`;
  else {
    const d = R.k2 - R.k1;
    const onK1 = new Q(-R.A0).sub(new Q(R.k1 * R.A0, d)); // −A0 − k1A0/(k2−k1) = −k2A0/(k2−k1)
    const onK2 = new Q(R.k1 * R.A0, d);
    cTex = join([`${R.A0}`, qt(onK1, ex(-R.k1, "t")), qt(onK2, ex(-R.k2, "t"))]);
  }
  return {
    prompt: `For ${scheme(R)}, ${init(R)}: find ${m("[C](t)")}.`,
    answer: { kind: "expression", ref: cJs, vars: ["t"], label: "[C](t)" },
    answerTex: `[C](t) = ${cTex}`,
    steps: [
      `Mass balance: ${m(`[A] + [B] + [C] = ${R.A0}`)} for all ${m("t")}, so ${m(`[C] = ${R.A0} - [A] - [B]`)} — no third ODE needed.`,
      `${m(`[A] = ${A}`)} (first equation on its own).`,
      `${m(`[B] = ${B.tex}`)} (eigen-solution of the ${m("2\\times2")} block).`,
      m(`[C](t) = ${cTex}`),
      `Check: ${m("[C](0) = 0")} and ${m(`[C] \\to ${R.A0}`)} as ${m("t \\to \\infty")}.`,
    ],
    meta: { variant: "C", ...R },
  };
}

function kinTmax(r: Rng): Draft {
  const R = rxn(r, { equal: r.chance(0.2) });
  const { k1, k2 } = R;
  let ref: string, tex: string, steps: string[];
  if (k1 === k2) {
    ref = `1/${k1}`;
    tex = new Q(1, k1).tex();
    steps = [
      `${m(`[B] = ${ct(k1 * R.A0, `t${ex(-k1, "t")}`)}`)} (equal rate constants).`,
      `${m(`\\frac{d[B]}{dt} = ${k1 * R.A0}${ex(-k1, "t")}(1 - ${k1 === 1 ? "" : k1}t) = 0`)}`,
      m(`t_{\\max} = \\frac{1}{k} = ${tex}`) + " min.",
    ];
  } else {
    ref = `log(${k1}/${k2})/(${k1} - ${k2})`;
    // write it with positive numbers: ln(big/small)/(big − small)
    const [hi, lo] = k1 > k2 ? [k1, k2] : [k2, k1];
    const ln = lo === 1 ? `\\ln ${hi}` : `\\ln\\frac{${hi}}{${lo}}`;
    tex = hi - lo === 1 ? ln : `\\frac{1}{${hi - lo}}${ln}`;
    const val = Math.log(k1 / k2) / (k1 - k2);
    steps = [
      `${m(`[B] = \\frac{k_1[A]_0}{k_2 - k_1}\\left(e^{-k_1t} - e^{-k_2t}\\right)`)}.`,
      `${m("\\frac{d[B]}{dt} = 0")}: ${m("k_1e^{-k_1t} = k_2e^{-k_2t}")}, so ${m("e^{(k_1-k_2)t} = k_1/k_2")}.`,
      `${m(`t_{\\max} = \\frac{\\ln(k_1/k_2)}{k_1 - k_2} = ${tex} \\approx ${val.toFixed(4)}`)} min — it doesn't depend on ${m("[A]_0")}.`,
    ];
  }
  return {
    prompt: `For ${scheme(R)}, starting from pure A: at what time ${m("t_{\\max}")} is ${m("[B]")} largest?`,
    answer: { kind: "expression", ref, vars: [], label: "t_max", tol: 1e-4 },
    answerTex: `t_{\\max} = ${tex}`,
    steps,
    meta: { variant: "tmax", ...R },
  };
}

export const KINETICS_TEMPLATES: Record<string, (r: Rng) => Draft> = {
  "kin-matrix": kinMatrix,
  "kin-eigen": kinEigen,
  "kin-B": kinB,
  "kin-C": kinC,
  "kin-tmax": kinTmax,
};
