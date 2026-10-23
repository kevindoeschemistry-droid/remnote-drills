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
  | { kind: "ode2"; a: number; b: number; c: number; v: string; rhs?: string; particular?: boolean; ic?: [number, number, number]; ref: string }
  /** an expression in `vars` (default x); optionally only up to a constant factor */
  | { kind: "expression"; ref: string; vars?: string[]; upToConstant?: boolean; label?: string; tol?: number;
      /** tol is a fraction of the reference value (engineering numbers: 0.01 = within 1%) */
      rel?: boolean; unit?: string }
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
}

/** What a generator returns; the registry stamps skill / template / level. */
export type Draft = Omit<Problem, "skill" | "template" | "level">;

export interface CheckResult {
  status: "correct" | "wrong" | "syntax" | "needs-constant" | "has-constant";
  message: string;
}
