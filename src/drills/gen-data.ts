// Problems as data: templates written in drills/problems/*.yaml (compiled into
// skills.generated.json by scripts/build-skills.mjs) and turned into Problems here.
//
//   given:    random picks       L: { pick: [0.01, 0.02] }   n: { int: [2, 6] }   Tinf: 25
//   let:      derived values     Ts: Tinf + qdot*L/h            (mathjs, in order)
//   require:  redraw unless      [Tmax < 1200]
//   prompt / ask / explain:      text with $…$ math; {{expr}} prints a value (4 sig figs),
//                                {{expr|3}} with 3, strings as they are
//   parts:    checked steps      { ask, label, tex, value: Ts, unit: "°C" }   the last is the final answer
//                                { ask, label, choice: [opt, opt…], correct: "expr → 0-based index" }
//                                { ask, label, tex, expr: "c*x^(n-1)", vars: [x] }   a symbolic answer: the template's
//                                numbers are folded in and the answer is checked as an expression (sym.ts)
//                                { ask, label, tex, ode: "a*x^n*y", sol: "C*exp(…)", ic: [x0, y0] }   y' = ode(x, y):
//                                an antiderivative (sol ends "+ C") or a solution of a first-order equation, checked
//                                by differentiating what the learner types
//   cases:    one is drawn       [{ f: "…", kind: 0 }, …]   its fields join the givens (text or numbers),
//                                for items whose wording changes with the case
//   figure:   a drawing          { type: plot | numberline | grid | bars | table, … }   see fig-data.ts
//   {{=expr}}                    prints an expression the same way, e.g. $f(x) = {{=a*x^n + b}}$
//   verify:   the independent check (tests/verify/data.py): never reused here
import graph from "./skills.generated.json";
import { math } from "./check";
import { fmt, u } from "./gen-heat";
import { require_ } from "./reject";
import type { Rng } from "./rng";
import type { Answer, Draft, Part } from "./types";
import { symbolic } from "./sym";
import { renderFigure } from "./fig-data";

type Given = number | string | { pick?: (number | string)[]; int?: [number, number] };
interface DataPart {
  ask: string;
  label: string;
  tex?: string;
  value?: string | number;
  expr?: string;
  ode?: string;
  sol?: string;
  ic?: (string | number)[];
  vars?: string[];
  unit?: string;
  tol?: number | string;
  explain?: string;
  choice?: string[];
  correct?: string | number;
  /** self-graded: `draw: true` asks for a sketch or structure on paper; `solution` is the figure to compare with */
  draw?: boolean;
  solution?: Record<string, unknown>;
}
export interface DataTemplate {
  template: string;
  skill: string;
  level?: number;
  given?: Record<string, Given>;
  cases?: Record<string, number | string>[];
  figure?: unknown;
  let?: Record<string, string | number>;
  require?: string[];
  prompt: string;
  parts: DataPart[];
  verify: unknown;
}

export const DATA: DataTemplate[] = ((graph as any).problems ?? []) as DataTemplate[];

type Scope = Record<string, number | string | boolean>;

const evalIn = (expr: string | number, scope: Scope): any => (typeof expr === "number" ? expr : math.evaluate(String(expr), { ...scope }));

function num(expr: string | number, scope: Scope, what: string): number {
  const v = evalIn(expr, scope);
  const x = typeof v === "number" ? v : Number(v?.valueOf?.());
  if (!Number.isFinite(x)) throw new Error(`${what}: ${expr} is not a finite number`);
  return x;
}

/** "{{expr}}" / "{{expr|3}}" -> value; numbers printed for TeX (so put them inside $…$) */
export function fill(text: string, scope: Scope): string {
  return text.replace(/\{\{([^}|]+)(?:\|(\d))?\}\}/g, (_, expr: string, sig?: string) => {
    if (expr.trim().startsWith("=")) return symbolic(expr.trim().slice(1), scope).tex;
    const v = evalIn(expr.trim(), scope);
    if (typeof v === "string") return v;
    if (typeof v === "boolean") return v ? "true" : "false";
    return fmt(Number(v), sig ? Number(sig) : 4);
  });
}

function draw(g: Given, r: Rng): number | string {
  if (typeof g === "number" || typeof g === "string") return g;
  if (g.pick) return r.pick(g.pick);
  if (g.int) return r.int(g.int[0], g.int[1]);
  throw new Error("a given needs pick, int or a value");
}

export function buildData(t: DataTemplate, r: Rng): Draft {
  const given: Scope = {};
  for (const [k, g] of Object.entries(t.given ?? {})) given[k] = draw(g, r);
  if (t.cases?.length) Object.assign(given, r.pick(t.cases as any));
  const scope: Scope = { ...given };
  for (const [k, e] of Object.entries(t.let ?? {})) {
    const v = evalIn(e, scope);
    scope[k] = typeof v === "number" || typeof v === "string" || typeof v === "boolean" ? v : Number(v);
  }
  for (const c of t.require ?? []) require_(Boolean(evalIn(c, scope)));

  const values: Record<string, number> = {};
  const parts: Part[] = t.parts.map((p) => {
    const ask = fill(p.ask, scope);
    const tex = p.tex ? fill(p.tex, scope) : p.label;
    const explain = p.explain ? fill(p.explain, scope) : undefined;
    if (p.draw) {
      const answer: Answer = { kind: "self", figure: p.solution ? renderFigure(p.solution as any, scope) : undefined, note: explain };
      return { ask, answer, answerTex: "\\text{compare with the drawing}", explain };
    }
    if (p.choice) {
      const options = p.choice.map((o) => fill(o, scope));
      const idx = num(p.correct ?? 0, scope, `${t.template} › ${p.label}`);
      require_(idx >= 0 && idx < options.length && new Set(options).size === options.length);
      const correct = options[idx];
      values[p.label] = idx;
      return { ask, answer: { kind: "choice", options, correct } as Answer, answerTex: `\\text{${correct.replace(/[{}$\\]/g, "")}}`, explain };
    }
    if (p.ode && p.sol) {
      const rhs = symbolic(p.ode, scope), sol = symbolic(p.sol, scope);
      const ic = p.ic ? ([num(p.ic[0], scope, "ic"), num(p.ic[1], scope, "ic")] as [number, number]) : undefined;
      const answer: Answer = { kind: "ode", rhs: rhs.ref, ref: `y = ${sol.ref}`, ...(ic ? { ic } : {}) };
      return { ask, answer, answerTex: `${tex} = ${sol.tex}`, explain };
    }
    if (p.expr) {
      const s = symbolic(p.expr, scope);
      const answer: Answer = { kind: "expression", ref: s.ref, vars: p.vars ?? ["x"], label: p.label, tol: 1e-9 };
      return { ask, answer, answerTex: `${tex} = ${s.tex}`, explain };
    }
    const v = num(p.value!, scope, `${t.template} › ${p.label}`);
    require_(v !== 0);
    values[p.label] = v;
    scope[p.label] = v;
    // the tolerance may be an expression, so a drawn case can carry its own band (an anchor known as a range)
    const tol = p.tol === undefined ? 0.01 : num(p.tol, scope, `${t.template} › ${p.label} tol`);
    const answer: Answer = { kind: "expression", ref: `${v}`, vars: [], tol, rel: true, label: p.label, unit: p.unit };
    return { ask, answer, answerTex: `${tex} = ${fmt(v, tol < 0.01 ? 6 : 3)}${p.unit ? u(p.unit) : ""}`, explain };
  });
  const last = parts[parts.length - 1];
  return {
    ...(t.figure ? { figure: renderFigure(t.figure, scope) } : {}),
    prompt: fill(t.prompt, scope),
    answer: last.answer,
    answerTex: last.answerTex,
    steps: parts.map((p) => `${p.ask} — $${p.answerTex}$${p.explain ? `. ${p.explain}` : ""}`),
    parts,
    meta: { data: t.template, given, values },
  };
}

export const DATA_TEMPLATES: Record<string, (r: Rng) => Draft> = Object.fromEntries(
  DATA.map((t) => [t.template, (r: Rng) => buildData(t, r)])
);
