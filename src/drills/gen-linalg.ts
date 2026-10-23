// Linear algebra, Level 1 (Lay ch 1, 2, 3, 5). Built backward from clean answers:
// integer solutions, determinants that make clean inverses, integer eigenvalues.
import { Rng } from "./rng";
import type { Draft } from "./types";
import { m } from "./tex";
import { Q } from "./rational";
import { require_ } from "./reject";

type M = number[][];

const det2 = (a: M) => a[0][0] * a[1][1] - a[0][1] * a[1][0];
const det3 = (a: M) =>
  a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1]) -
  a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0]) +
  a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]);

const pmat = (rows: (string | number)[][], aug = false) => {
  const n = rows[0].length;
  const spec = aug ? `{${"r".repeat(n - 1)}|r}` : "";
  const body = rows.map((r) => r.join(" & ")).join(" \\\\ ");
  return aug ? `\\left[\\begin{array}${spec} ${body} \\end{array}\\right]` : `\\begin{bmatrix} ${body} \\end{bmatrix}`;
};
const vec = (v: (string | number)[]) => `\\begin{bmatrix} ${v.join(" \\\\ ")} \\end{bmatrix}`;
const par = (n: number) => (n < 0 ? `(${n})` : `${n}`);

function intMatrix(r: Rng, n: number, lo = -4, hi = 4): M {
  return Array.from({ length: n }, () => Array.from({ length: n }, () => r.int(lo, hi)));
}

// ── §1.1–1.2 row reduction ────────────────────────────────────────────────────
function system(r: Rng): Draft {
  const A = intMatrix(r, 3, -3, 4);
  require_(det3(A) !== 0 && A.flat().filter((x) => x === 0).length <= 2 && A[0][0] !== 0);
  const x = [r.int(-4, 5), r.int(-4, 5), r.int(-4, 5)];
  const b = A.map((row) => row.reduce((s, a, j) => s + a * x[j], 0));
  require_(b.every((v) => Math.abs(v) <= 30));
  // forward elimination with exact fractions, recording the row operations
  const R: Q[][] = A.map((row, i) => [...row.map((v) => new Q(v)), new Q(b[i])]);
  const ops: string[] = [];
  for (let c = 0; c < 3; c++) {
    let p = c;
    while (p < 3 && R[p][c].isZero()) p++;
    if (p !== c) {
      [R[p], R[c]] = [R[c], R[p]];
      ops.push(`R_${c + 1} \\leftrightarrow R_${p + 1}`);
    }
    for (let i = c + 1; i < 3; i++) {
      if (R[i][c].isZero()) continue;
      const f = R[i][c].div(R[c][c]);
      R[i] = R[i].map((v, j) => v.sub(f.mul(R[c][j])));
      ops.push(`R_${i + 1} \\leftarrow R_${i + 1} ${f.n < 0 ? "+" : "-"} ${absTex(f)}R_${c + 1}`);
    }
  }
  const varTex = ["x_1", "x_2", "x_3"];
  const eqTex = A.map((row, i) => `${terms(row, varTex)} = ${b[i]}`).join(" \\\\ ");
  return {
    prompt: `Solve by row reduction: ${m(`\\begin{aligned} ${eqTex} \\end{aligned}`)}`,
    answer: {
      kind: "tuple",
      fields: varTex.map((v, i) => ({ label: `x${"₁₂₃"[i]}`, tex: v, ref: `${x[i]}`, mode: "number" as const })),
      vars: [],
    },
    answerTex: `(x_1, x_2, x_3) = (${x.join(", ")})`,
    steps: [
      `Augmented matrix: ${m(pmat(A.map((row, i) => [...row, b[i]]), true))}.`,
      `Row operations to echelon form: ${m(ops.join(",\\quad "))}.`,
      `Echelon form: ${m(pmat(R.map((row) => row.map((q) => q.tex())), true))}.`,
      `Back-substitute from the bottom row up: ${m(`x_3 = ${x[2]},\\ x_2 = ${x[1]},\\ x_1 = ${x[0]}`)}.`,
      `Check in row 1: ${m(`${A[0].map((a, j) => `${par(a)}(${x[j]})`).join(" + ")} = ${b[0]}`)} ✓`,
    ],
    meta: { variant: "system", A, b },
  };
}

function absTex(q: Q) {
  const a = q.n < 0 ? q.neg() : q;
  return a.n === a.d ? "" : a.d === 1 ? `${a.n}` : `\\tfrac{${a.n}}{${a.d}}`;
}

function terms(row: number[], vars: string[]) {
  const out: string[] = [];
  row.forEach((a, j) => {
    if (!a) return;
    const body = Math.abs(a) === 1 ? vars[j] : `${Math.abs(a)}${vars[j]}`;
    out.push(out.length ? `${a < 0 ? "-" : "+"} ${body}` : `${a < 0 ? "-" : ""}${body}`);
  });
  return out.join(" ") || "0";
}

// ── §1.7 linear independence ─────────────────────────────────────────────────
const IND = ["Linearly independent", "Linearly dependent"];
function independence(r: Rng): Draft {
  const dependent = r.chance(0.5);
  const v1 = [r.int(-3, 3), r.int(-3, 3), r.int(-3, 3)];
  const v2 = [r.int(-3, 3), r.int(-3, 3), r.int(-3, 3)];
  let v3: number[], rel = "";
  if (dependent) {
    const a = r.pick([1, -1, 2, -2, 3]);
    const b = r.pick([1, -1, 2, -2]);
    v3 = v1.map((x, i) => a * x + b * v2[i]);
    rel = `${m(`\\mathbf v_3 = ${a === 1 ? "" : a === -1 ? "-" : a}\\mathbf v_1 ${b < 0 ? "-" : "+"} ${Math.abs(b) === 1 ? "" : Math.abs(b)}\\mathbf v_2`)}`;
  } else v3 = [r.int(-3, 3), r.int(-3, 3), r.int(-3, 3)];
  const A = [0, 1, 2].map((i) => [v1[i], v2[i], v3[i]]);
  const D = det3(A);
  require_(dependent ? D === 0 : D !== 0);
  // no zero vectors, no obvious multiples
  require_([v1, v2, v3].every((v) => v.some((x) => x !== 0)) && det2([[v1[0], v2[0]], [v1[1], v2[1]]]) !== 0);
  return {
    prompt: `Are ${m(`\\mathbf v_1 = ${vec(v1)},\\ \\mathbf v_2 = ${vec(v2)},\\ \\mathbf v_3 = ${vec(v3)}`)} linearly independent?`,
    answer: { kind: "choice", options: IND, correct: IND[dependent ? 1 : 0] },
    answerTex: `\\text{${IND[dependent ? 1 : 0]}}`,
    steps: [
      `Three vectors in ${m("\\mathbb R^3")}: put them in the columns of ${m("A")}; they're independent exactly when ${m("A\\mathbf x = \\mathbf 0")} has only the trivial solution, i.e. ${m("\\det A \\ne 0")}.`,
      `${m(`\\det ${pmat(A)} = ${D}`)}.`,
      dependent ? `Zero, so dependent: ${rel}.` : `Nonzero, so the only solution is ${m("\\mathbf x = \\mathbf 0")}: independent.`,
    ],
    meta: { variant: "independence", A, dependent },
  };
}

// ── §2.2 2×2 inverse ──────────────────────────────────────────────────────────
function inverse(r: Rng): Draft {
  const A = intMatrix(r, 2, -5, 6);
  const D = det2(A);
  require_(D !== 0 && Math.abs(D) <= 6 && A.flat().filter((x) => x === 0).length <= 1);
  const [[a, b], [c, d]] = A;
  const inv = [new Q(d, D), new Q(-b, D), new Q(-c, D), new Q(a, D)];
  const labels = ["(A⁻¹)₁₁", "(A⁻¹)₁₂", "(A⁻¹)₂₁", "(A⁻¹)₂₂"];
  const texs = ["(A^{-1})_{11}", "(A^{-1})_{12}", "(A^{-1})_{21}", "(A^{-1})_{22}"];
  return {
    prompt: `Find ${m("A^{-1}")} for ${m(`A = ${pmat(A)}`)}.`,
    answer: {
      kind: "tuple",
      fields: inv.map((q, i) => ({ label: labels[i], tex: texs[i], ref: `${q.n}/${q.d}`, mode: "number" as const })),
      vars: [],
    },
    answerTex: `A^{-1} = ${pmat([[inv[0].tex(), inv[1].tex()], [inv[2].tex(), inv[3].tex()]])}`,
    steps: [
      `${m(`\\det A = ad - bc = (${a})(${d}) - (${b})(${c}) = ${D}`)} ${m("\\ne 0")}, so ${m("A")} is invertible.`,
      `Swap the diagonal, negate the off-diagonal, divide by the determinant: ${m(`A^{-1} = \\frac{1}{${D}}${pmat([[d, -b], [-c, a]])}`)}.`,
      `${m(`A^{-1} = ${pmat([[inv[0].tex(), inv[1].tex()], [inv[2].tex(), inv[3].tex()]])}`)}. Check: ${m("AA^{-1} = I")}.`,
    ],
    meta: { variant: "inverse", A },
  };
}

// ── §3.1–3.2 3×3 determinant ─────────────────────────────────────────────────
function determinant(r: Rng): Draft {
  const A = intMatrix(r, 3, -4, 5);
  // a zero or two makes cofactor expansion the obvious move
  const zr = r.int(0, 2);
  A[zr][r.int(0, 2)] = 0;
  const D = det3(A);
  require_(D !== 0 && Math.abs(D) <= 150);
  // expand along the row with the most zeros
  const row = [0, 1, 2].reduce((best, i) => (A[i].filter((x) => !x).length > A[best].filter((x) => !x).length ? i : best), 0);
  const minor = (i: number, j: number) => A.filter((_, k) => k !== i).map((rr) => rr.filter((_, l) => l !== j));
  const parts = [0, 1, 2].map((j) => {
    const sgn = (row + j) % 2 ? -1 : 1;
    const Mij = minor(row, j);
    return { j, sgn, a: A[row][j], Mij, d: det2(Mij) };
  });
  const expansion = parts
    .filter((p) => p.a !== 0)
    .map((p, k) => `${k === 0 ? (p.sgn * p.a < 0 ? "-" : "") : p.sgn * p.a < 0 ? " - " : " + "}${Math.abs(p.a)}\\begin{vmatrix} ${p.Mij.map((rr) => rr.join(" & ")).join(" \\\\ ")} \\end{vmatrix}`)
    .join("");
  const numbers = parts
    .filter((p) => p.a !== 0)
    .map((p, k) => `${k === 0 ? (p.sgn * p.a < 0 ? "-" : "") : p.sgn * p.a < 0 ? " - " : " + "}${Math.abs(p.a)}(${p.d})`)
    .join("");
  return {
    prompt: `Compute ${m(`\\det ${pmat(A)}`)}.`,
    answer: { kind: "expression", ref: `${D}`, vars: [], label: "det A" },
    answerTex: `\\det A = ${D}`,
    steps: [
      `Cofactor expansion along row ${row + 1} (the one with the most zeros), signs ${m(row % 2 ? "- + -" : "+ - +")}.`,
      m(`\\det A = ${expansion}`),
      m(`= ${numbers} = ${D}`),
    ],
    meta: { variant: "det", A },
  };
}

// ── §5.1–5.2 eigenvalues / eigenvectors (2×2) ──────────────────────────────────
function eigenMatrix(r: Rng) {
  // A = P diag(l1, l2) P^{-1} with det P = ±1 keeps every entry an integer
  const P = r.pick([
    [[1, 1], [0, 1]], [[1, 0], [1, 1]], [[2, 1], [1, 1]], [[1, 1], [1, 2]], [[1, 2], [1, 3]],
    [[3, 1], [2, 1]], [[1, -1], [1, 0]], [[2, 3], [1, 2]], [[1, 1], [2, 3]],
  ]);
  const l1 = r.int(-4, 5);
  const l2 = r.int(-4, 5);
  require_(l1 !== l2);
  const dP = det2(P);
  const Pinv = [[P[1][1] / dP, -P[0][1] / dP], [-P[1][0] / dP, P[0][0] / dP]];
  const PD = [[P[0][0] * l1, P[0][1] * l2], [P[1][0] * l1, P[1][1] * l2]];
  const A = [0, 1].map((i) => [0, 1].map((j) => PD[i][0] * Pinv[0][j] + PD[i][1] * Pinv[1][j]));
  require_(A.flat().every((x) => Number.isInteger(x) && Math.abs(x) <= 12) && (A[0][1] !== 0 || A[1][0] !== 0));
  return { A, l1, l2, v1: [P[0][0], P[1][0]], v2: [P[0][1], P[1][1]] };
}

const fac = (l: number) => (l === 0 ? "\\lambda" : `(\\lambda ${l > 0 ? "-" : "+"} ${Math.abs(l)})`);

function eigenvalues(r: Rng): Draft {
  const E = eigenMatrix(r);
  const { A } = E;
  const tr = A[0][0] + A[1][1], D = det2(A);
  const lin = tr === 0 ? "" : ` ${tr > 0 ? "-" : "+"} ${Math.abs(tr) === 1 ? "" : Math.abs(tr)}\\lambda`;
  const poly = `\\lambda^2${lin}${D === 0 ? "" : ` ${D > 0 ? "+" : "-"} ${Math.abs(D)}`}`;
  return {
    prompt: `Find the eigenvalues of ${m(`A = ${pmat(A)}`)}.`,
    answer: { kind: "roots", ref: [E.l1, E.l2], label: "λ" },
    answerTex: `\\lambda = ${Math.min(E.l1, E.l2)},\\ ${Math.max(E.l1, E.l2)}`,
    steps: [
      `${m("\\det(A - \\lambda I) = 0")}. For a ${m("2\\times2")}: ${m("\\lambda^2 - (\\operatorname{tr}A)\\lambda + \\det A = 0")}.`,
      `${m(`\\operatorname{tr}A = ${tr}`)}, ${m(`\\det A = ${D}`)}: ${m(`${poly} = 0`)}.`,
      `${m(`${fac(E.l1)}${fac(E.l2)} = 0`)}, so ${m(`\\lambda = ${E.l1},\\ ${E.l2}`)}. Check: they sum to the trace and multiply to the determinant.`,
    ],
    meta: { variant: "eigenvalues", A },
  };
}

function eigenvector(r: Rng): Draft {
  const E = eigenMatrix(r);
  const { A } = E;
  const lam = E.l1, v = E.v1;
  const B = [[A[0][0] - lam, A[0][1]], [A[1][0], A[1][1] - lam]];
  const row = B[0].some((x) => x !== 0) ? B[0] : B[1];
  return {
    prompt: `${m(`A = ${pmat(A)}`)} has eigenvalue ${m(`\\lambda = ${lam}`)}. Find a corresponding eigenvector.`,
    answer: {
      kind: "tuple",
      fields: [
        { label: "v₁", tex: "v_1", ref: `${v[0]}`, mode: "number" },
        { label: "v₂", tex: "v_2", ref: `${v[1]}`, mode: "number" },
      ],
      vars: [],
      proportional: true,
    },
    answerTex: `\\mathbf v = ${vec(v)}\\ (\\text{any nonzero multiple})`,
    steps: [
      `Solve ${m(`(A - ${par(lam)}I)\\mathbf v = \\mathbf 0`)}: ${m(`A - ${par(lam)}I = ${pmat(B)}`)} — singular, so its rows are proportional.`,
      `One row is enough: ${m(`${terms(row, ["v_1", "v_2"])} = 0`)}.`,
      `${m(`\\mathbf v = ${vec(v)}`)}, or any nonzero multiple. Check: ${m(`A\\mathbf v = ${vec([A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1]])} = ${par(lam)}\\mathbf v`)} ✓`,
    ],
    meta: { variant: "eigenvector", A, lam },
  };
}

export const LINALG_TEMPLATES: Record<string, (r: Rng) => Draft> = {
  "la-system": system,
  "la-independence": independence,
  "la-inverse": inverse,
  "la-det": determinant,
  "la-eigenvalues": eigenvalues,
  "la-eigenvector": eigenvector,
};
