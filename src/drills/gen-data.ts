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
//   verify:   the independent check (tests/verify/data.py): never reused here
import graph from "./skills.generated.json";
import { math } from "./check";
import { fmt, u } from "./gen-heat";
import { require_ } from "./reject";
import type { Rng } from "./rng";
import type { Answer, Draft, Part } from "./types";

type Given = number | string | { pick?: (number | string)[]; int?: [number, number] };
interface DataPart {
  ask: string;
  label: string;
  tex?: string;
  value?: string | number;
  unit?: string;
  tol?: number;
  explain?: string;
  choice?: string[];
  correct?: string | number;
}
export interface DataTemplate {
  template: string;
  skill: string;
  level?: number;
  given?: Record<string, Given>;
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
  const scope: Scope = { ...given };
  for (const [k, e] of Object.entries(t.let ?? {})) {
    const v = evalIn(e, scope);
    scope[k] = typeof v === "number" || typeof v === "string" || typeof v === "boolean" ? v : Number(v);
  }
  for (const c of t.require ?? []) require_(Boolean(evalIn(c, scope)));

  const values: Record<string, number> = {};
  const parts: Part[] = t.parts.map((p) => {
    const ask = fill(p.ask, scope);
    const explain = p.explain ? fill(p.explain, scope) : undefined;
    if (p.choice) {
      const options = p.choice.map((o) => fill(o, scope));
      const idx = num(p.correct ?? 0, scope, `${t.template} › ${p.label}`);
      require_(idx >= 0 && idx < options.length && new Set(options).size === options.length);
      const correct = options[idx];
      values[p.label] = idx;
      return { ask, answer: { kind: "choice", options, correct } as Answer, answerTex: `\\text{${correct.replace(/[{}$\\]/g, "")}}`, explain };
    }
    const v = num(p.value!, scope, `${t.template} › ${p.label}`);
    require_(v !== 0);
    values[p.label] = v;
    scope[p.label] = v;
    const answer: Answer = { kind: "expression", ref: `${v}`, vars: [], tol: p.tol ?? 0.01, rel: true, label: p.label, unit: p.unit };
    return { ask, answer, answerTex: `${p.tex ?? p.label} = ${fmt(v)}${p.unit ? u(p.unit) : ""}`, explain };
  });
  const last = parts[parts.length - 1];
  return {
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
