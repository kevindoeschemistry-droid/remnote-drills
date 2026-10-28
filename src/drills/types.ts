// Shared types for the drill engine.
//
// A Problem is never stored — only its address (skill, template, level, seed)
// is, and generators rebuild it. Its `answer` says HOW to check, by kind.

export type SkillId = string;

/** Boundary condition for y'' + λy = 0 on [0, L]: y(at) = 0 or y'(at) = 0 */
export interface Bc {
  at: number;
  type: "y" | "yp";
}

export type Answer =
  /** first order, y(x): explicit or implicit, general (needs C) or IVP */
  | { kind: "ode"; rhs: string; ic?: [number, number]; ref: string }
  /** a y'' + b y' + c y = 0 in variable `v`; IVP if ic = [t0, y0, y0'] */
  /** a y'' + b y' + c y = rhs(v) (rhs default 0). particular: one solution, no constants;
   *  ic: the IVP solution; otherwise the general solution (two independent constants) */
  | { kind: "ode2"; a: number; b: number; c: number; v: string; rhs?: string; particular?: boolean; ic?: [number, number, number, ...number[]]; ref: string;
      /** variable coefficients and/or higher order: coef[i] multiplies y^(n-i), highest derivative first
       *  (mathjs in v; n = coef.length - 1). When present a, b, c are ignored and ic = [t0, y, y', …, y^(n-1)]. */
      coef?: string[] }
  /** an expression in `vars` (default x); optionally only up to a constant factor */
  | { kind: "expression"; ref: string; vars?: string[]; upToConstant?: boolean; label?: string; tol?: number;
      /** tol is a fraction of the reference value (engineering numbers: 0.01 = within 1%) */
      rel?: boolean; unit?: string;
      /** sample scopes to check at, instead of the default grid (integer n, both sides of a step, small t) */
      points?: Record<string, number>[] }
  /** two-term recurrence a_{m+gap} = f(m) a_m ; ref is f in the variable m */
  | { kind: "recurrence"; gap: number; ref: string; from: number }
  /** a list of numbers, order ignored (indicial roots, characteristic roots) */
  | { kind: "roots"; ref: number[]; label?: string }
  /** a sequence in n, e.g. eigenvalues λ_n; ref in variable n, valid from n = start */
  | { kind: "indexed"; ref: string; start: number; label: string }
  /** eigenfunctions y_n(x) of y'' + λy = 0 with these BCs; refLambda in n from start */
  | { kind: "eigenfunctions"; bcs: Bc[]; L: number; refLambda: string; start: number }
  /** pick one option */
  | { kind: "choice"; options: string[]; correct: string }
  /** several labelled fields; `proportional` = all fields may share one constant factor */
  | {
      kind: "tuple";
      fields: { label: string; tex: string; ref: string; mode: "expr" | "number" | "angle" }[];
      vars?: string[];
      proportional?: boolean;
      /** fields are the components of a solution of y' = A y in variable v: with ic = [t0, y1(t0), …]
       *  the IVP solution, otherwise the general solution (n independent constants) */
      system?: { A: number[][]; v: string; ic?: number[] };
      /** sample scopes to check at, instead of the default grid (e.g. integer n for Fourier coefficients) */
      points?: Record<string, number>[];
    };

export interface Problem {
  skill: SkillId;
  template: string;
  level: number;
  /** card front: text with $...$ inline math */
  prompt: string;
  answer: Answer;
  /** reference answer, LaTeX */
  answerTex: string;
  /** worked steps, text with $...$ */
  steps: string[];
  /** template-specific extras used by tests (never by the UI) */
  meta?: Record<string, unknown>;
  /** optional diagram: a self-contained SVG string built by the generator */
  figure?: string;
  /** checked steps, in order; the last one is the final answer (== answer). The panel walks
   *  through them one at a time until the skill has a streak, then asks only the final answer. */
  parts?: Part[];
}

export interface Part {
  /** what this step asks for: text with $...$ */
  ask: string;
  answer: Answer;
  answerTex: string;
  /** shown once the step is answered or revealed: why, with the numbers */
  explain?: string;
}

/** What a generator returns; the registry stamps skill / template / level. */
export type Draft = Omit<Problem, "skill" | "template" | "level">;

export interface CheckResult {
  status: "correct" | "wrong" | "syntax" | "needs-constant" | "has-constant";
  message: string;
}
