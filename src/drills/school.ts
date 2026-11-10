// Shared helpers for the K–12 mathematics drills (gen-k8.ts, gen-hs.ts).
//
// Every school problem carries `meta.mx` (a case name) plus the raw inputs, so
// tests/verify/school_k8.py and school_hs.py can recompute the answer from the
// problem statement with exact arithmetic, enumeration or sympy — never from the
// generator's own formula. Generic cases:
//   { mx: "expr", e }        the answer is the exact value of the Python expression e
//   { mx: "exprs", es }      tuple: field i is the exact value of es[i]
//   { mx: "eq", eq }         the answer, put in place of "?", makes the equation eq true
//   { mx: "cmp", a, b }      choice of >, <, = between two exact numbers
// Answers that are a different *form* of the prompt (a fraction as a decimal, an
// expanded form) ask for one missing piece instead, so retyping the prompt can't pass.
import type { Answer, Draft } from "./types";
import { Q } from "./rational";
import { gcd } from "./tex";

export { gcd };
export const lcm = (a: number, b: number) => Math.abs(a * b) / gcd(a, b);

/** mathjs / sympy reference for a rational */
export const qref = (q: Q) => (q.d === 1 ? `${q.n}` : `${q.n}/${q.d}`);
/** Python source for a rational (exact under sympify(rational=True)) */
export const qpy = (q: Q) => (q.d === 1 ? `${q.n}` : `(${q.n})/(${q.d})`);

/** an exact number: integer or fraction, checked to 1e-6 */
export function exact(v: number | Q, label = "answer"): Answer {
  // tight tolerance: 999,999 + 0.01 must still be wrong
  return { kind: "expression", ref: typeof v === "number" ? `${v}` : qref(v), vars: [], label, tol: 1e-10 };
}
/** a rounded number (decimals, π answers): within `tol` (fraction of the value) */
export function approx(v: number | string, tol = 0.002, label = "answer"): Answer {
  return { kind: "expression", ref: `${v}`, vars: [], rel: true, tol, label };
}
export function choice(options: string[], correct: string): Answer {
  if (!options.includes(correct) || new Set(options).size !== options.length) throw new Error(`bad choice ${correct} in ${options}`);
  return { kind: "choice", options, correct };
}
export interface F {
  label: string;
  tex: string;
  ref: string | number | Q;
  mode?: "expr" | "number" | "angle";
}
export function tuple(fields: F[], vars: string[] = [], points?: Record<string, number>[]): Answer {
  return {
    kind: "tuple",
    fields: fields.map((f) => ({ label: f.label, tex: f.tex, ref: typeof f.ref === "object" ? qref(f.ref) : `${f.ref}`, mode: f.mode ?? "expr" })),
    vars,
    ...(points ? { points } : {}),
  };
}
export function draft(prompt: string, answer: Answer, answerTex: string, steps: string[], meta: Record<string, unknown>): Draft {
  return { prompt, answer, answerTex, steps, meta };
}

// ── number formatting ─────────────────────────────────────────────────────────
/** integer for LaTeX, thousands grouped with {,} (4{,}357) */
export function int(n: number): string {
  const s = String(Math.abs(n)).replace(/\B(?=(\d{3})+(?!\d))/g, "{,}");
  return n < 0 ? `-${s}` : s;
}
/** plain-text integer with commas (choice options, word problems) */
export const intTxt = (n: number) => n.toLocaleString("en-US");
/** exact decimal string from a scaled integer: dec(3472, 3) = "3.472" */
export function dec(scaled: number, places: number): string {
  if (places === 0) return `${scaled}`;
  const neg = scaled < 0;
  const s = String(Math.abs(scaled)).padStart(places + 1, "0");
  let out = `${s.slice(0, -places)}.${s.slice(-places)}`.replace(/0+$/, "").replace(/\.$/, "");
  return neg ? `-${out}` : out;
}
/** decimal for LaTeX (grouped integer part) */
export function decTex(scaled: number, places: number): string {
  const s = dec(scaled, places);
  const [i, f] = s.replace("-", "").split(".");
  return `${s.startsWith("-") ? "-" : ""}${int(Number(i))}${f ? `.${f}` : ""}`;
}
/** a rational as LaTeX; mixed number when asked (2\tfrac{1}{3}) */
export function qtex(q: Q, mixed = false): string {
  if (!mixed || q.d === 1 || Math.abs(q.n) < q.d) return q.tex();
  const w = Math.trunc(q.n / q.d);
  const rem = Math.abs(q.n) - Math.abs(w) * q.d;
  return `${w}\\tfrac{${rem}}{${q.d}}`;
}
/** wrap a negative in parentheses */
export const par = (s: string | number) => (String(s).startsWith("-") ? `(${s})` : `${s}`);
/** coefficient times variable, LaTeX: 3x, -x, x */
export function cx(k: number | Q, v: string): string {
  const q = Q.of(k);
  if (q.n === q.d) return v;
  if (q.n === -q.d) return `-${v}`;
  return `${q.tex()}${v}`;
}
/** signed term for joining: " + 3x", " - 5" */
export function sg(k: number | Q, v = ""): string {
  const q = Q.of(k);
  if (q.isZero()) return "";
  const a = q.n < 0 ? q.neg() : q;
  const body = v ? (a.n === a.d ? v : `${a.tex()}${v}`) : a.tex();
  return q.n < 0 ? ` - ${body}` : ` + ${body}`;
}
/** a x^2 + b x + c (or any descending polynomial), LaTeX */
export function poly(coefs: (number | Q)[], v = "x"): string {
  const n = coefs.length - 1;
  let out = "";
  coefs.forEach((c, i) => {
    const p = n - i;
    const body = p === 0 ? "" : p === 1 ? v : `${v}^{${p}}`;
    const q = Q.of(c);
    if (q.isZero()) return;
    if (!out) out = body ? cx(q, body) : q.tex();
    else out += sg(q, body);
  });
  return out || "0";
}
/** same polynomial in Python / mathjs syntax */
export function polyPy(coefs: (number | Q)[], v = "x"): string {
  const n = coefs.length - 1;
  return coefs.map((c, i) => `(${qpy(Q.of(c))})*${v}**${n - i}`).join(" + ") || "0";
}
export const polyJs = (coefs: (number | Q)[], v = "x") => polyPy(coefs, v).replace(/\*\*/g, "^");

export const NAMES = ["Ana", "Ben", "Chen", "Dara", "Eli", "Fatima", "Gus", "Hana", "Ivan", "Jada", "Kofi", "Lena", "Mateo", "Nia", "Omar", "Priya"];
export const shuffle = <T>(xs: T[], next: () => number) => {
  const a = [...xs];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(next() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
};
