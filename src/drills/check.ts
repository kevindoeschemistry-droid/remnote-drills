// Answer checking for the ODE drills.
//
// Any answer is read as an equation G(x, y, C) = lhs - rhs = 0 ("y = ..." when
// there is no "=" sign). That covers explicit answers (y = ...) and implicit
// ones (y^2 = ..., 1/y^2 = ..., sqrt(y) = ..., e^y = ...) with one rule:
//
//   General solution: pick points (x, y); solve G = 0 for the constant C there;
//   the curve of that family member has slope -G_x/G_y, which must equal
//   f(x, y). Passing at many points means every member solves the ODE.
//
//   IVP: no constant allowed; G(x0, y0) = 0, then follow the curve away from
//   (x0, y0) and check its slope against f at each step.
//
// Same idea as the wiki's verifyODE (plug the answer back in), extended to
// implicit answers and arbitrary constants.

import { create, all, MathNode } from "mathjs";
import type { Answer, CheckResult, Problem } from "./types";
import { checkOther } from "./check-kinds";

export const math = create(all, {});
// students write ln; mathjs log(x) is already natural log
math.import({ ln: (v: number) => Math.log(v), arctan: Math.atan, arcsin: Math.asin, arccos: Math.acos }, { override: true });

const FUNCS = [
  "arcsin", "arccos", "arctan", "asin", "acos", "atan", "sinh", "cosh", "tanh",
  "sqrt", "cbrt", "sin", "cos", "tan", "sec", "csc", "cot", "exp", "log", "ln", "abs",
];
const RESERVED = new Set(["x", "y", "e", "pi"]);
export { FUNCS, RESERVED };

// ── input normalisation ─────────────────────────────────────────────────────
export function normalize(raw: string): string {
  let s = raw.trim();
  s = s
    .replace(/[−–—]/g, "-")
    .replace(/[·×⋅]/g, "*")
    .replace(/÷/g, "/")
    .replace(/²/g, "^2")
    .replace(/³/g, "^3")
    .replace(/√\s*([0-9.]+|[a-zA-Z])/g, "sqrt($1)")
    .replace(/√/g, "sqrt")
    .replace(/π/g, "pi")
    .replace(/\\left|\\right/g, "")
    .replace(/\\(ln|sin|cos|tan|sec|exp|sqrt|arctan|pi)/g, "$1")
    .replace(/\\cdot/g, "*")
    .replace(/\\frac\{([^{}]*)\}\{([^{}]*)\}/g, "($1)/($2)")
    .replace(/[{}]/g, (c) => (c === "{" ? "(" : ")"))
    .replace(/\[/g, "(")
    .replace(/\]/g, ")");
  // |u| -> abs(u)   (innermost first)
  for (let i = 0; i < 6 && /\|[^|]*\|/.test(s); i++) s = s.replace(/\|([^|]*)\|/g, "(abs($1))");
  // split glued identifiers: xe -> x*e, xsin -> x*sin, Ce -> C*e, 2xy -> 2x*y
  s = s.replace(/[A-Za-z]+[0-9]*/g, (word) => splitWord(word));
  // a function name followed by a bare argument: sin x -> sin(x), ln x -> ln(x)
  s = s.replace(
    new RegExp(`(?<![a-zA-Z])(${FUNCS.join("|")})\\s+([0-9]*[a-zA-Z](?:\\^[0-9]+)?)`, "g"),
    "$1($2)"
  );
  // x(x+1), C(x+1): a lone symbol before "(" is multiplication, not a call
  s = s.replace(/\b([a-zA-Z][0-9]?)\s*\(/g, "$1*(");
  // everything else (2x, (x+1)(x-1), 3sin(x)) is mathjs implicit multiplication
  return s;
}

function splitWord(word: string): string {
  if (FUNCS.includes(word) || RESERVED.has(word) || /^[A-Z][0-9]$/.test(word)) return word;
  const toks: string[] = [];
  let i = 0;
  while (i < word.length) {
    const fn = FUNCS.filter((f) => word.startsWith(f, i)).sort((a, b) => b.length - a.length)[0];
    if (fn) {
      toks.push(fn);
      i += fn.length;
    } else if (word.startsWith("pi", i)) {
      toks.push("pi");
      i += 2;
    } else if (/[0-9]/.test(word[i]) && toks.length) {
      // trailing digits belong to the previous symbol (C1)
      toks[toks.length - 1] += word[i];
      i++;
    } else {
      toks.push(word[i]);
      i++;
    }
  }
  // sinx -> sin(x), sqrty -> sqrt(y), xsinx -> x*sin(x)
  const out: string[] = [];
  for (let k = 0; k < toks.length; k++) {
    const t = toks[k];
    const nxt = toks[k + 1];
    if (FUNCS.includes(t) && nxt && /^[a-zA-Z][0-9]?$/.test(nxt) && !FUNCS.includes(nxt)) {
      out.push(`${t}(${nxt})`);
      k++;
    } else out.push(t);
  }
  // a trailing function name stays bare so "ln(" / "sin(" keep working
  return out.join("*");
}

// ── compilation ─────────────────────────────────────────────────────────────
interface Eq {
  G: (x: number, y: number, c: Record<string, number>) => number;
  constants: string[];
  lhsNode: MathNode;
  rhsNode: MathNode;
}

function compileEquation(raw: string, defaultLhs = "y"): Eq | null {
  const s = normalize(raw);
  const parts = s.split("=");
  if (parts.length > 2) return null;
  const [lhsS, rhsS] = parts.length === 2 ? parts : [defaultLhs, parts[0]];
  if (!lhsS.trim() || !rhsS.trim()) return null;
  let lhsNode: MathNode, rhsNode: MathNode;
  try {
    lhsNode = math.parse(lhsS);
    rhsNode = math.parse(rhsS);
  } catch {
    return null;
  }
  const constants = new Set<string>();
  for (const node of [lhsNode, rhsNode]) {
    node.traverse((n: any, _path: string, parent: any) => {
      if (n.isSymbolNode && !(parent && parent.isFunctionNode && parent.fn === n)) {
        const name = n.name as string;
        if (!RESERVED.has(name) && !FUNCS.includes(name)) constants.add(name);
      }
    });
  }
  const lhs = lhsNode.compile();
  const rhs = rhsNode.compile();
  const G = (x: number, y: number, c: Record<string, number>) => {
    try {
      const scope = { x, y, ...c };
      const v = real(lhs.evaluate(scope)) - real(rhs.evaluate(scope));
      return Number.isFinite(v) ? v : NaN;
    } catch {
      return NaN;
    }
  };
  return { G, constants: [...constants], lhsNode, rhsNode };
}

export function real(v: any): number {
  if (typeof v === "number") return v;
  if (v && typeof v === "object" && "re" in v) return Math.abs(v.im) < 1e-12 ? v.re : NaN;
  if (typeof v === "boolean") return NaN;
  return NaN;
}

function compileRhs(rhs: string) {
  const c = math.parse(rhs).compile();
  return (x: number, y: number) => {
    try {
      const v = real(c.evaluate({ x, y }));
      return Number.isFinite(v) ? v : NaN;
    } catch {
      return NaN;
    }
  };
}

/** LaTeX preview of what the student typed (best effort). */
export function previewTex(raw: string): string | null {
  if (!raw.trim()) return null;
  try {
    const s = normalize(raw);
    const parts = s.split("=");
    if (parts.length > 2) return null;
    return parts.map((p) => math.parse(p).toTex({ parenthesis: "auto", implicit: "hide" })).join(" = ");
  } catch {
    return null;
  }
}

// ── numerics ────────────────────────────────────────────────────────────────
const rel = (a: number, b: number) => Math.abs(a - b) / Math.max(1, Math.abs(a), Math.abs(b));

/** Find c with g(c) = 0: scan a grid for sign changes, then bisect. */
function solveForC(g: (c: number) => number): number | null {
  const grid: number[] = [];
  for (let k = -60; k <= 60; k++) grid.push(k / 2);
  for (const big of [-500, -100, -40, 40, 100, 500]) grid.push(big);
  grid.sort((a, b) => a - b);
  let prevC = grid[0];
  let prevV = g(prevC);
  for (const c of grid.slice(1)) {
    const v = g(c);
    if (Number.isFinite(v) && Math.abs(v) < 1e-12) return c;
    if (Number.isFinite(v) && Number.isFinite(prevV) && Math.sign(v) !== Math.sign(prevV)) {
      let lo = prevC, hi = c, flo = prevV;
      for (let it = 0; it < 80; it++) {
        const mid = (lo + hi) / 2;
        const fm = g(mid);
        if (!Number.isFinite(fm)) break;
        if (Math.sign(fm) === Math.sign(flo)) {
          lo = mid;
          flo = fm;
        } else hi = mid;
      }
      const root = (lo + hi) / 2;
      const fr = g(root);
      // reject sign changes caused by poles in C
      if (Number.isFinite(fr) && Math.abs(fr) < 1e-7 * Math.max(1, Math.abs(prevV), Math.abs(v))) return root;
    }
    prevC = c;
    prevV = v;
  }
  return null;
}

function slopeOf(G: Eq["G"], x: number, y: number, c: Record<string, number>): number | null {
  const hx = 1e-6 * Math.max(1, Math.abs(x));
  const hy = 1e-6 * Math.max(1, Math.abs(y));
  const Gx = (G(x + hx, y, c) - G(x - hx, y, c)) / (2 * hx);
  const Gy = (G(x, y + hy, c) - G(x, y - hy, c)) / (2 * hy);
  if (!Number.isFinite(Gx) || !Number.isFinite(Gy) || Math.abs(Gy) < 1e-9) return null;
  return -Gx / Gy;
}

const SAMPLE_X = [0.35, 0.6, 0.85, 1.15, 1.45, 1.8, 2.3];
const SAMPLE_Y = [-2.3, -1.1, -0.45, 0.4, 0.9, 1.6, 2.7];

function checkGeneral(eq: Eq, f: (x: number, y: number) => number): CheckResult {
  if (eq.constants.length === 0)
    return { status: "needs-constant", message: "A general solution needs an arbitrary constant — include C." };
  if (eq.constants.length > 1)
    return { status: "syntax", message: `Use a single constant C (found ${eq.constants.join(", ")}).` };
  const name = eq.constants[0];
  let ok = 0;
  for (const x of SAMPLE_X) {
    for (const y of SAMPLE_Y) {
      const fv = f(x, y);
      if (!Number.isFinite(fv)) continue;
      const c = solveForC((cv) => eq.G(x, y, { [name]: cv }));
      if (c === null) continue;
      const s = slopeOf(eq.G, x, y, { [name]: c });
      if (s === null) continue;
      if (rel(s, fv) > 2e-4) return { status: "wrong", message: "Not quite — that family doesn't satisfy the equation." };
      ok++;
    }
  }
  if (ok < 6) {
    return { status: "wrong", message: "Not quite — couldn't match that to the equation at enough points." };
  }
  return { status: "correct", message: "Correct!" };
}

/** Newton solve G(x, y) = 0 for y near guess */
function solveY(G: (y: number) => number, guess: number): number | null {
  let y = guess;
  for (let i = 0; i < 40; i++) {
    const g = G(y);
    if (!Number.isFinite(g)) return null;
    if (Math.abs(g) < 1e-12) return y;
    const h = 1e-7 * Math.max(1, Math.abs(y));
    const d = (G(y + h) - G(y - h)) / (2 * h);
    if (!Number.isFinite(d) || Math.abs(d) < 1e-14) return null;
    const step = g / d;
    y -= step;
    if (Math.abs(step) < 1e-12 * Math.max(1, Math.abs(y))) return y;
  }
  return Math.abs(G(y)) < 1e-8 ? y : null;
}

function checkIvp(eq: Eq, f: (x: number, y: number) => number, ic: [number, number]): CheckResult {
  if (eq.constants.length > 0)
    return {
      status: "has-constant",
      message: `Use the initial condition to find ${eq.constants[0]} — the answer should have no constant left.`,
    };
  const [x0, y0] = ic;
  const g0 = eq.G(x0, y0, {});
  if (!Number.isFinite(g0) || Math.abs(g0) > 1e-7 * Math.max(1, Math.abs(y0)))
    return { status: "wrong", message: `Not quite — your answer doesn't pass through y(${x0}) = ${fmt(y0)}.` };
  let ok = 0;
  for (const dir of [1, -1]) {
    let x = x0, y = y0;
    for (let i = 0; i < 6; i++) {
      const fv = f(x, y);
      if (!Number.isFinite(fv)) break;
      const xn = x + dir * 0.05;
      const yn = solveY((yy) => eq.G(xn, yy, {}), y + dir * 0.05 * fv);
      if (yn === null) break;
      x = xn;
      y = yn;
      const s = slopeOf(eq.G, x, y, {});
      const fn = f(x, y);
      if (s === null || !Number.isFinite(fn)) break;
      if (rel(s, fn) > 2e-4) return { status: "wrong", message: "Not quite — that curve doesn't satisfy the equation." };
      ok++;
    }
  }
  if (ok < 3) return { status: "wrong", message: "Not quite — couldn't confirm that curve near the initial point." };
  return { status: "correct", message: "Correct!" };
}

function fmt(v: number): string {
  const r = Math.round(v * 1e6) / 1e6;
  for (const d of [2, 3, 4, 5, 6]) {
    if (Math.abs(r * d - Math.round(r * d)) < 1e-9 && Math.round(r * d) % d !== 0) return `${Math.round(r * d)}/${d}`;
  }
  return `${r}`;
}

// ── public API ──────────────────────────────────────────────────────────────
type OdeAnswer = Extract<Answer, { kind: "ode" }>;

function checkOde(a: OdeAnswer, raw: string): CheckResult {
  if (!raw.trim()) return { status: "syntax", message: "Type your answer first." };
  const eq = compileEquation(raw);
  if (!eq) return { status: "syntax", message: "Couldn't read that. Try e.g.  y = Ce^(2x) + 3  or  y^2 = x^2 + C" };
  const f = compileRhs(a.rhs);
  return a.ic ? checkIvp(eq, f, a.ic) : checkGeneral(eq, f);
}

/** input is a string, or one string per field for tuple answers */
export function check(p: Problem, input: string | string[]): CheckResult {
  if (p.answer.kind === "ode") return checkOde(p.answer, Array.isArray(input) ? input[0] : input);
  return checkOther(p.answer, input);
}
