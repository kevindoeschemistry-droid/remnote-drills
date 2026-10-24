// Checkers for every answer kind except first-order ODEs (see check.ts).
// Same philosophy throughout: never compare strings — evaluate the student's
// answer numerically and test the property that defines "correct".
import type { Answer, Bc, CheckResult } from "./types";
import { math, normalize, real } from "./check";

const OK: CheckResult = { status: "correct", message: "Correct!" };
const wrong = (message = "Not quite.") => ({ status: "wrong" as const, message });
const syntax = (message: string) => ({ status: "syntax" as const, message });
const EMPTY = syntax("Type your answer first.");

type Scope = Record<string, number>;
interface Compiled {
  f: (scope: Scope) => number;
  symbols: string[];
}

const KNOWN_FUNCS = new Set([
  "sin", "cos", "tan", "sec", "csc", "cot", "asin", "acos", "atan", "arcsin", "arccos", "arctan",
  "sinh", "cosh", "tanh", "sqrt", "cbrt", "exp", "log", "ln", "abs", "atan2", "heaviside",
]);

/** Drop a leading "label =" (W =, y_n =, λ_n =, R =) when there is exactly one "=". */
function rhsOnly(raw: string): string {
  const s = raw.replace(/λ/g, "lambda").replace(/δ/g, "delta").replace(/ω/g, "omega");
  const parts = s.split("=");
  return parts.length === 2 ? parts[1] : s;
}

function compile(expr: string, pre = true): Compiled | null {
  try {
    const node = math.parse(pre ? normalize(expr) : expr);
    const symbols = new Set<string>();
    node.traverse((n: any, _p: string, parent: any) => {
      if (n.isSymbolNode && !(parent?.isFunctionNode && parent.fn === n) && !KNOWN_FUNCS.has(n.name)) symbols.add(n.name);
    });
    symbols.delete("e");
    symbols.delete("pi");
    const code = node.compile();
    return {
      symbols: [...symbols],
      f: (scope) => {
        try {
          const v = real(code.evaluate({ ...scope }));
          return Number.isFinite(v) ? v : NaN;
        } catch {
          return NaN;
        }
      },
    };
  } catch {
    return null;
  }
}

const close = (a: number, b: number, tol: number) => Math.abs(a - b) <= tol * Math.max(1, Math.abs(a), Math.abs(b));
const SAMPLES = [0.23, 0.37, 0.52, 0.66, 0.81, 1.27, 1.93];

// ── expression ──────────────────────────────────────────────────────────────
type ExprAnswer = Extract<Answer, { kind: "expression" }>;
function checkExpression(a: ExprAnswer, raw: string): CheckResult {
  if (!raw.trim()) return EMPTY;
  const vars = a.vars ?? ["x"];
  const mine = compile(a.rel ? plainNumber(rhsOnly(raw)) : rhsOnly(raw));
  const ref = compile(a.ref, false);
  if (!mine || !ref) return syntax("Couldn't read that.");
  const extra = mine.symbols.filter((s) => !vars.includes(s));
  if (extra.length) return syntax(`Unexpected symbol${extra.length > 1 ? "s" : ""}: ${extra.join(", ")}.`);
  const tol = a.tol ?? 1e-6;
  const points: Scope[] = a.points ?? (vars.length ? SAMPLES.map((v) => Object.fromEntries(vars.map((n, i) => [n, v + 0.11 * i]))) : [{}]);
  let ratio: number | null = null;
  let ok = 0;
  for (const pt of points) {
    const r = ref.f(pt);
    if (!Number.isFinite(r)) continue;
    const u = mine.f(pt);
    if (!Number.isFinite(u)) return wrong();
    if (a.upToConstant) {
      if (Math.abs(r) < 1e-12) {
        if (Math.abs(u) > 1e-9) return wrong();
        continue;
      }
      const k = u / r;
      if (ratio === null) ratio = k;
      if (!close(k, ratio, tol) || Math.abs(k) < 1e-12) return wrong();
    } else if (a.rel) {
      if (Math.abs(u - r) > tol * Math.abs(r)) {
        const off = Math.abs(u / r);
        return wrong(
          Math.abs(u + r) <= tol * Math.abs(r)
            ? "Right size, wrong sign — check the direction."
            : Math.abs(off - 1) < 0.05
            ? "Close, but outside 1% — carry more digits through the calculation."
            : [10, 100, 1000, 0.1, 0.01, 0.001].some((f) => Math.abs(off / f - 1) < 0.02)
              ? "Off by a power of ten — check your units (cm, mm, kW)."
              : "Not quite."
        );
      }
    } else if (!close(u, r, tol)) return wrong();
    ok++;
  }
  return ok >= Math.min(3, points.length) ? OK : wrong();
}

/** Engineering-number input: "25,000", "2.5 x 10^4", "25000 W/m^2" -> mathjs-friendly */
function plainNumber(s: string): string {
  return s
    .replace(/(\d),(?=\d{3}\b)/g, "$1")
    .replace(/(\d)\s*[xX×·]\s*10\s*\^/g, "$1*10^")
    .replace(/\s*(°\s*C|°C|K|W|kW|W\/m|W\/m\^?2|W\/m²|W\/m\^?3|W\/m³|W\/m·K|m\^?-1|1\/m|mm|cm|m|%|K\/s|°C\/s|m²·K\/W|m\^2K\/W)\s*$/u, "");
}

// ── second-order constant-coefficient ODE  a y'' + b y' + c y = f ────────────
type Ode2Answer = Extract<Answer, { kind: "ode2" }>;
function checkOde2(a: Ode2Answer, raw: string): CheckResult {
  if (!raw.trim()) return EMPTY;
  if (a.coef) return checkOdeN(a, raw);
  const parts = raw.split("=");
  if (parts.length > 2) return syntax(`Write it as  y = …  in terms of ${a.v}.`);
  const mine = compile(parts.length === 2 ? parts[1] : parts[0]);
  if (!mine) return syntax("Couldn't read that.");
  const forcing = a.rhs ? compile(a.rhs, false) : null;
  const f = (tt: number) => (forcing ? forcing.f({ [a.v]: tt }) : 0);
  const consts = mine.symbols.filter((s) => s !== a.v);
  const h = 1e-4;
  const at = (t: number, c: Scope) => {
    const g = (tt: number) => mine.f({ ...c, [a.v]: tt });
    const y0 = g(t), yp = g(t + h), ym = g(t - h);
    return { y: y0, d1: (yp - ym) / (2 * h), d2: (yp - 2 * y0 + ym) / (h * h) };
  };
  const residualOk = (c: Scope) => {
    for (const t of [0.3, 0.7, 1.1, 1.6, 2.2]) {
      const { y, d1, d2 } = at(t, c);
      if (![y, d1, d2].every(Number.isFinite)) return false;
      const ft = f(t);
      const res = a.a * d2 + a.b * d1 + a.c * y - ft;
      const scale = Math.max(Math.abs(a.a * d2), Math.abs(a.b * d1), Math.abs(a.c * y), Math.abs(ft), 1e-3);
      if (Math.abs(res) > 2e-5 * scale) return false;
    }
    return true;
  };
  const notIt = a.rhs ? "Not quite — that doesn't satisfy the equation (check the right-hand side)." : "Not quite — that doesn't satisfy the equation.";
  if (a.ic) {
    if (consts.length) return { status: "has-constant", message: `Use the initial conditions to find ${consts.join(", ")}.` };
    if (!residualOk({})) return wrong(notIt);
    const [t0, y0, v0] = a.ic;
    const { y, d1 } = at(t0, {});
    if (!close(y, y0, 1e-6) || !close(d1, v0, 1e-5))
      return wrong(`Not quite — check y(${t0}) = ${y0} and y'(${t0}) = ${v0}.`);
    return OK;
  }
  if (a.particular) {
    if (consts.length) return { status: "has-constant", message: "A particular solution has no arbitrary constants — solve for the coefficients." };
    return residualOk({}) ? OK : wrong(notIt);
  }
  if (consts.length < 2) return { status: "needs-constant", message: "A general solution needs two arbitrary constants." };
  const base = (vals: number[]) => Object.fromEntries(consts.map((n, i) => [n, vals[i % 2] + 0.3 * Math.floor(i / 2)]));
  for (const vals of [[0.7, -1.3], [1.9, 0.4], [-0.6, 2.2]]) if (!residualOk(base(vals))) return wrong(notIt);
  // the constants must multiply two independent solutions: C1 e^{2x} + C2 e^{2x} is one solution
  const c0 = base([0.7, -1.3]);
  const ts = [0.2, 0.6, 1.0, 1.5, 2.1];
  const grads = consts.map((n) =>
    ts.map((t) => (mine.f({ ...c0, [n]: c0[n] + h, [a.v]: t }) - mine.f({ ...c0, [n]: c0[n] - h, [a.v]: t })) / (2 * h))
  );
  const dot = (u: number[], v: number[]) => u.reduce((s, ui, i) => s + ui * v[i], 0);
  let independent = false;
  for (let i = 0; i < grads.length && !independent; i++)
    for (let j = i + 1; j < grads.length && !independent; j++) {
      const uu = dot(grads[i], grads[i]), vv = dot(grads[j], grads[j]), uv = dot(grads[i], grads[j]);
      if (uu > 1e-12 && vv > 1e-12 && (uu * vv - uv * uv) / (uu * vv) > 1e-7) independent = true;
    }
  if (!independent)
    return wrong("Your constants multiply the same solution — you need two independent ones (for a double root λ: e^{λx} and x·e^{λx}).");
  return OK;
}

// ── variable-coefficient / higher-order linear ODE  Σ coef_i(v) y^(n-i) = f ───
/** number of linearly independent vectors (Gram–Schmidt on normalised copies) */
function rank(vecs: number[][]): number {
  const basis: number[][] = [];
  for (const v0 of vecs) {
    const nrm = Math.sqrt(v0.reduce((s, x) => s + x * x, 0));
    if (!(nrm > 1e-9)) continue;
    let v = v0.map((x) => x / nrm);
    for (const b of basis) {
      const d = v.reduce((s, x, i) => s + x * b[i], 0);
      v = v.map((x, i) => x - d * b[i]);
    }
    const r2 = v.reduce((s, x) => s + x * x, 0);
    if (r2 > 1e-7) basis.push(v.map((x) => x / Math.sqrt(r2)));
  }
  return basis.length;
}

const SYMBOLIC_NAMES: Record<string, string> = { ln: "log", arctan: "atan", arcsin: "asin", arccos: "acos" };

function checkOdeN(a: Ode2Answer, raw: string): CheckResult {
  const coef = a.coef!;
  const n = coef.length - 1;
  const parts = raw.split("=");
  if (parts.length > 2) return syntax(`Write it as  y = …  in terms of ${a.v}.`);
  const body = normalize(parts.length === 2 ? parts[1] : parts[0]);
  const mine = compile(body, false);
  if (!mine) return syntax("Couldn't read that.");
  const cs = coef.map((s) => compile(s, false)!);
  const forcing = a.rhs ? compile(a.rhs, false) : null;
  const f = (tt: number) => (forcing ? forcing.f({ [a.v]: tt }) : 0);
  const consts = mine.symbols.filter((s) => s !== a.v);
  // derivatives y, y', …, y^(n): central differences up to order 2 (as checkOde2), exact above that
  let derivs: (t: number, c: Scope) => number[];
  if (n <= 2) {
    const h = 1e-4;
    derivs = (t, c) => {
      const g = (tt: number) => mine.f({ ...c, [a.v]: tt });
      const y0 = g(t), yp = g(t + h), ym = g(t - h);
      return [y0, (yp - ym) / (2 * h), (yp - 2 * y0 + ym) / (h * h)].slice(0, n + 1);
    };
  } else {
    let fs: ((s: Scope) => number)[];
    try {
      let node: any = math.parse(body).transform((nd: any) =>
        nd.isFunctionNode && SYMBOLIC_NAMES[nd.fn.name] ? new (math as any).FunctionNode(SYMBOLIC_NAMES[nd.fn.name], nd.args) : nd
      );
      const nodes = [node];
      for (let k = 1; k <= n; k++) nodes.push((node = math.derivative(node, a.v, { simplify: false })));
      fs = nodes.map((nd) => {
        const code = nd.compile();
        return (s: Scope) => {
          try {
            const v = real(code.evaluate({ ...s }));
            return Number.isFinite(v) ? v : NaN;
          } catch {
            return NaN;
          }
        };
      });
    } catch {
      return syntax("Couldn't differentiate that — check the functions you used.");
    }
    derivs = (t, c) => fs.map((g) => g({ ...c, [a.v]: t }));
  }
  const residualOk = (c: Scope) => {
    for (const t of [0.3, 0.7, 1.1, 1.6, 2.2]) {
      const d = derivs(t, c);
      if (!d.every(Number.isFinite)) return false;
      const terms = cs.map((k, i) => k.f({ [a.v]: t }) * d[n - i]);
      const ft = f(t);
      const res = terms.reduce((s, x) => s + x, 0) - ft;
      const scale = Math.max(...terms.map(Math.abs), Math.abs(ft), 1e-3);
      if (!Number.isFinite(res) || Math.abs(res) > 2e-5 * scale) return false;
    }
    return true;
  };
  const notIt = a.rhs ? "Not quite — that doesn't satisfy the equation (check the right-hand side)." : "Not quite — that doesn't satisfy the equation.";
  if (a.ic) {
    if (consts.length) return { status: "has-constant", message: `Use the initial conditions to find ${consts.join(", ")}.` };
    if (!residualOk({})) return wrong(notIt);
    const [t0, ...vals] = a.ic;
    const d = derivs(t0, {});
    const names = ["y", "y'", "y''", "y'''"];
    for (let j = 0; j < Math.min(n, vals.length); j++)
      if (!close(d[j], vals[j], j === 0 ? 1e-6 : 1e-5)) return wrong(`Not quite — check ${names[j] ?? `y^(${j})`}(${t0}) = ${vals[j]}.`);
    return OK;
  }
  if (a.particular) {
    if (consts.length) return { status: "has-constant", message: "A particular solution has no arbitrary constants — solve for the coefficients." };
    return residualOk({}) ? OK : wrong(notIt);
  }
  if (consts.length < n) return { status: "needs-constant", message: `A general solution of this order-${n} equation needs ${n} arbitrary constants.` };
  const base = (vals: number[]) => Object.fromEntries(consts.map((nm, i) => [nm, vals[i % vals.length] + 0.3 * Math.floor(i / vals.length)]));
  for (const vals of [[0.7, -1.3, 0.45, 1.1], [1.9, 0.4, -0.8, 0.25], [-0.6, 2.2, 1.3, -1.7]]) if (!residualOk(base(vals))) return wrong(notIt);
  const c0 = base([0.7, -1.3, 0.45, 1.1]);
  const ts = [0.2, 0.45, 0.7, 1.0, 1.3, 1.6, 2.1];
  const h = 1e-4;
  const grads = consts.map((nm) =>
    ts.map((t) => (mine.f({ ...c0, [nm]: c0[nm] + h, [a.v]: t }) - mine.f({ ...c0, [nm]: c0[nm] - h, [a.v]: t })) / (2 * h))
  );
  if (rank(grads) < n) return wrong(`Your constants don't multiply ${n} independent solutions — for a repeated root λ use e^{λx}, x·e^{λx}, x²e^{λx}, ….`);
  return OK;
}

// ── linear system  y' = A y  (tuple of components) ─────────────────────────
type TupleAns = Extract<Answer, { kind: "tuple" }>;
function checkSystem(a: TupleAns, inputs: string[]): CheckResult {
  const S = a.system!;
  const k = S.A.length;
  if (inputs.length !== k || inputs.some((s) => !s?.trim())) return syntax("Fill in every component.");
  const comps: Compiled[] = [];
  for (let i = 0; i < k; i++) {
    const c = compile(rhsOnly(inputs[i]));
    if (!c) return syntax(`Couldn't read ${a.fields[i].label}.`);
    comps.push(c);
  }
  const consts = [...new Set(comps.flatMap((c) => c.symbols))].filter((s) => s !== S.v);
  const h = 1e-4;
  const residualOk = (c: Scope) => {
    for (const t of [0.15, 0.4, 0.7, 1.0, 1.35]) {
      const y = comps.map((g) => g.f({ ...c, [S.v]: t }));
      const d = comps.map((g) => (g.f({ ...c, [S.v]: t + h }) - g.f({ ...c, [S.v]: t - h })) / (2 * h));
      if (![...y, ...d].every(Number.isFinite)) return false;
      for (let i = 0; i < k; i++) {
        const terms = S.A[i].map((aij, j) => aij * y[j]);
        const res = d[i] - terms.reduce((s, x) => s + x, 0);
        const scale = Math.max(Math.abs(d[i]), ...terms.map(Math.abs), ...y.map(Math.abs), 1e-3);
        if (Math.abs(res) > 2e-5 * scale) return false;
      }
    }
    return true;
  };
  const notIt = "Not quite — that doesn't satisfy y' = Ay.";
  if (S.ic) {
    if (consts.length) return { status: "has-constant", message: `Use the initial conditions to find ${consts.join(", ")}.` };
    if (!residualOk({})) return wrong(notIt);
    const [t0, ...vals] = S.ic;
    const bad = comps.map((g, i) => (close(g.f({ [S.v]: t0 }), vals[i], 1e-6) ? "" : a.fields[i].label)).filter(Boolean);
    return bad.length ? wrong(`Not quite — check the initial value of ${bad.join(", ")}.`) : OK;
  }
  if (consts.length < k) return { status: "needs-constant", message: `A general solution needs ${k} arbitrary constants (C1, C2).` };
  const base = (vals: number[]) => Object.fromEntries(consts.map((nm, i) => [nm, vals[i % 2] + 0.3 * Math.floor(i / 2)]));
  for (const vals of [[0.7, -1.3], [1.9, 0.4], [-0.6, 2.2]]) if (!residualOk(base(vals))) return wrong(notIt);
  const c0 = base([0.7, -1.3]);
  const ts = [0.1, 0.35, 0.6, 0.9, 1.2];
  const grads = consts.map((nm) =>
    ts.flatMap((t) => comps.map((g) => (g.f({ ...c0, [nm]: c0[nm] + h, [S.v]: t }) - g.f({ ...c0, [nm]: c0[nm] - h, [S.v]: t })) / (2 * h)))
  );
  if (rank(grads) < k) return wrong("Your constants multiply the same solution — you need two independent ones (one per eigenvector).");
  return OK;
}

// ── recurrence  a_{m+gap} = f(m) a_m ───────────────────────────────────────
type RecAnswer = Extract<Answer, { kind: "recurrence" }>;
const COEF = /a(?:_\s*\{([^}]*)\}|_\s*\(([^)]*)\)|\[([^\]]*)\]|_\s*([nkmj])(?![a-zA-Z(]))/g;

export function parseRecurrence(raw: string) {
  const tokens: { offset: number; idx: string }[] = [];
  let bad = false;
  const s = raw.replace(COEF, (_m, g1, g2, g3, g4) => {
    const inner = (g1 ?? g2 ?? g3 ?? g4 ?? "").trim();
    const mm = /^([nkmj])\s*(?:([+-])\s*(\d+))?$/.exec(inner);
    if (!mm) {
      bad = true;
      return "0";
    }
    const offset = mm[2] ? (mm[2] === "-" ? -1 : 1) * Number(mm[3]) : 0;
    tokens.push({ offset, idx: mm[1] });
    return ` @${offset + 50}@ `;
  });
  if (bad || !tokens.length) return null;
  const idx = tokens[0].idx;
  if (tokens.some((t) => t.idx !== idx)) return null;
  // bare symbols so implicit multiplication works on both sides ("n a_n", "a_n (n+1)");
  // a placeholder followed by "(" gets an explicit * so it isn't read as a function call
  const norm = normalize(s)
    .replace(/@(\d+)@\s*\(/g, (_m, k) => ` acoef_${k}*(`)
    .replace(/@(\d+)@/g, (_m, k) => ` acoef_${k} `);
  return { norm, idx, offsets: [...new Set(tokens.map((t) => t.offset))].sort((x, y) => x - y) };
}

function checkRecurrence(a: RecAnswer, raw: string): CheckResult {
  if (!raw.trim()) return EMPTY;
  const parsed = parseRecurrence(raw);
  if (!parsed) return syntax("Write it like  a_{n+2} = -a_n/((n+2)(n+1))");
  const sides = parsed.norm.split("=");
  if (sides.length !== 2) return syntax("Write it as an equation:  a_{n+2} = …");
  if (parsed.offsets.length !== 2) return wrong("A two-term recurrence links exactly two coefficients.");
  const [q, p] = parsed.offsets;
  if (p - q !== a.gap)
    return wrong(`Not quite — this recurrence links coefficients ${a.gap} apart (a_{n+${a.gap}} and a_n).`);
  const F = compile(`(${sides[0]}) - (${sides[1]})`, false);
  if (!F) return syntax("Couldn't read that.");
  const names = [parsed.idx, `acoef_${p + 50}`, `acoef_${q + 50}`];
  const extra = F.symbols.filter((s) => !names.includes(s));
  if (extra.length) return syntax(`Unexpected symbol: ${extra.join(", ")}`);
  const ref = compile(a.ref, false)!;
  let ok = 0;
  for (let mIdx = a.from; mIdx < a.from + 8; mIdx++) {
    const fm = ref.f({ m: mIdx });
    if (!Number.isFinite(fm)) continue;
    const n = mIdx - q; // the student's index value at which their a_{n+q} is a_m
    const sc = (Ap: number, Aq: number) => F.f({ [parsed.idx]: n, [names[1]]: Ap, [names[2]]: Aq });
    const alpha = sc(1, 0);
    const beta = sc(0, 1);
    if (!Number.isFinite(alpha) || !Number.isFinite(beta) || Math.abs(alpha) < 1e-12) continue;
    if (!close(-beta / alpha, fm, 1e-9)) return wrong();
    ok++;
  }
  return ok >= 5 ? OK : wrong();
}

// ── roots ───────────────────────────────────────────────────────────────────
type RootsAnswer = Extract<Answer, { kind: "roots" }>;
function checkRoots(a: RootsAnswer, raw: string): CheckResult {
  if (!raw.trim()) return EMPTY;
  const items = raw
    .split(/,|;|\band\b|\bor\b/)
    .map((x) => x.trim())
    .filter(Boolean)
    .map((x) => rhsOnly(x));
  const vals: number[] = [];
  for (const it of items) {
    const c = compile(it);
    if (!c || c.symbols.length) return syntax("List the roots as numbers, e.g.  1/2, -1");
    const v = c.f({});
    if (!Number.isFinite(v)) return syntax("List the roots as numbers, e.g.  1/2, -1");
    vals.push(v);
  }
  const uniq = (xs: number[]) => xs.filter((v, i) => xs.findIndex((w) => close(v, w, 1e-9)) === i);
  const mine = uniq(vals);
  const ref = uniq(a.ref);
  if (mine.length !== ref.length || !ref.every((r) => mine.some((v) => close(v, r, 1e-9)))) return wrong();
  return OK;
}

// ── indexed sequence λ_n ───────────────────────────────────────────────────
type IndexedAnswer = Extract<Answer, { kind: "indexed" }>;
function checkIndexed(a: IndexedAnswer, raw: string): CheckResult {
  if (!raw.trim()) return EMPTY;
  const mine = compile(rhsOnly(raw));
  const ref = compile(a.ref, false);
  if (!mine || !ref) return syntax("Couldn't read that.");
  const extra = mine.symbols.filter((s) => s !== "n");
  if (extra.length) return syntax(`Write it in terms of n only (found ${extra.join(", ")}).`);
  // allow the student to start counting one off from us
  for (const shift of [0, -1, 1]) {
    let good = true;
    for (let n = a.start; n < a.start + 5; n++) {
      const r = ref.f({ n });
      const u = mine.f({ n: n + shift });
      if (!Number.isFinite(r) || !Number.isFinite(u) || !close(u, r, 1e-9)) {
        good = false;
        break;
      }
    }
    if (good) return OK;
  }
  return wrong();
}

// ── eigenfunctions of y'' + λy = 0 ─────────────────────────────────────────
type EigAnswer = Extract<Answer, { kind: "eigenfunctions" }>;
function checkEigenfunctions(a: EigAnswer, raw: string): CheckResult {
  if (!raw.trim()) return EMPTY;
  const mine = compile(rhsOnly(raw));
  if (!mine) return syntax("Couldn't read that.");
  const consts = mine.symbols.filter((s) => s !== "x" && s !== "n");
  if (consts.length > 1) return syntax("Write y_n in terms of x and n (one constant multiple is fine).");
  const ref = compile(a.refLambda, false)!;
  const refLams: number[] = [];
  for (let n = a.start; n < a.start + 15; n++) refLams.push(ref.f({ n }));
  const c: Scope = consts.length ? { [consts[0]]: 1.7 } : {};
  const L = a.L;
  const grid = [0.13, 0.29, 0.41, 0.58, 0.77].map((t) => t * L);
  const h = 1e-4 * Math.max(1, L);
  const found: number[] = [];
  for (let n = 0; n <= 6; n++) {
    const f = (x: number) => mine.f({ ...c, n, x });
    const vals = grid.map(f);
    if (!vals.every(Number.isFinite)) return wrong();
    const big = Math.max(...vals.map(Math.abs), Math.abs(f(0)), Math.abs(f(L)));
    if (big < 1e-8) continue; // trivial (e.g. sin(0·x))
    // -y''/y must be one constant λ
    const lams: number[] = [];
    for (const x of grid) {
      const y = f(x);
      if (Math.abs(y) < 0.05 * big) continue;
      lams.push(-(f(x + h) - 2 * y + f(x - h)) / (h * h) / y);
    }
    if (lams.length < 2 || !lams.every((l) => Math.abs(l - lams[0]) <= 1e-4 * Math.max(1, Math.abs(lams[0]))))
      return wrong("Not quite — that's not a solution of the equation.");
    const lam = lams.reduce((s, v) => s + v, 0) / lams.length;
    if (!refLams.some((r) => Math.abs(r - lam) <= 1e-4 * Math.max(1, Math.abs(r))))
      return wrong("Not quite — that solves the equation but misses the boundary conditions.");
    for (const bc of a.bcs as Bc[]) {
      const v = bc.type === "y" ? f(bc.at) : (f(bc.at + h) - f(bc.at - h)) / (2 * h);
      if (Math.abs(v) > 1e-5 * big * Math.max(1, Math.sqrt(Math.abs(lam))))
        return wrong(`Not quite — check the condition at x = ${bc.at === 0 ? 0 : "L"}.`);
    }
    if (!found.some((l) => Math.abs(l - lam) <= 1e-6 * Math.max(1, l))) found.push(lam);
  }
  return found.length >= 3 ? OK : wrong("Not quite — give the whole family in terms of n.");
}

// ── tuple ───────────────────────────────────────────────────────────────────
type TupleAnswer = Extract<Answer, { kind: "tuple" }>;
function checkTuple(a: TupleAnswer, inputs: string[]): CheckResult {
  if (a.system) return checkSystem(a, inputs);
  if (inputs.length !== a.fields.length || inputs.some((s) => !s?.trim())) return syntax("Fill in every field.");
  const vars = a.vars ?? [];
  const comps: Compiled[] = [];
  for (let i = 0; i < inputs.length; i++) {
    const c = compile(rhsOnly(inputs[i]));
    if (!c) return syntax(`Couldn't read ${a.fields[i].label}.`);
    const extra = c.symbols.filter((s) => !vars.includes(s));
    if (extra.length) return syntax(`${a.fields[i].label}: unexpected symbol ${extra.join(", ")}.`);
    comps.push(c);
  }
  const refs = a.fields.map((f) => compile(f.ref, false)!);
  const points: Scope[] = a.points ?? (vars.length ? SAMPLES.slice(0, 5).map((v) => ({ [vars[0]]: v })) : [{}]);
  let ratio: number | null = null;
  const bad: string[] = [];
  a.fields.forEach((field, i) => {
    for (const pt of points) {
      const r = refs[i].f(pt);
      const u = comps[i].f(pt);
      if (!Number.isFinite(r)) continue;
      if (!Number.isFinite(u)) return void bad.push(field.label);
      if (a.proportional) {
        if (Math.abs(r) < 1e-12) {
          if (Math.abs(u) > 1e-9) return void bad.push(field.label);
          continue;
        }
        const k = u / r;
        if (ratio === null) ratio = k;
        if (Math.abs(k) < 1e-12 || !close(k, ratio, 1e-6)) return void bad.push(field.label);
      } else if (field.mode === "angle") {
        const d = (((u - r) % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI);
        if (Math.min(d, 2 * Math.PI - d) > 2e-3) return void bad.push(field.label);
      } else if (!close(u, r, field.mode === "number" ? 1e-3 : 1e-6)) return void bad.push(field.label);
    }
  });
  if (bad.length) return wrong(`Not quite — check ${[...new Set(bad)].join(", ")}.`);
  return OK;
}

// ── dispatch ────────────────────────────────────────────────────────────────
export function checkOther(a: Answer, input: string | string[]): CheckResult {
  const one = Array.isArray(input) ? input[0] ?? "" : input;
  switch (a.kind) {
    case "expression":
      return checkExpression(a, one);
    case "ode2":
      return checkOde2(a, one);
    case "recurrence":
      return checkRecurrence(a, one);
    case "roots":
      return checkRoots(a, one);
    case "indexed":
      return checkIndexed(a, one);
    case "eigenfunctions":
      return checkEigenfunctions(a, one);
    case "choice":
      return one === a.correct ? OK : wrong(`Not quite — it's ${a.correct.toLowerCase()}.`);
    case "tuple":
      return checkTuple(a, Array.isArray(input) ? input : [input]);
    default:
      return syntax("Unsupported answer type.");
  }
}

/** Preview helper for recurrences: a_{n+2} survives as a_{n+2} in the LaTeX. */
export function recurrencePreview(raw: string): string | null {
  const parsed = parseRecurrence(raw);
  if (!parsed) return null;
  try {
    return parsed.norm
      .split("=")
      .map((side) => math.parse(side).toTex({ parenthesis: "auto", implicit: "hide" }))
      .join(" = ")
      .replace(/acoef\\?_(\d+)|acoef_\{(\d+)\}/g, (_m, k1, k2) => {
        const off = Number(k1 ?? k2) - 50;
        return `a_{${parsed.idx}${off === 0 ? "" : off > 0 ? `+${off}` : off}}`;
      });
  } catch {
    return null;
  }
}
