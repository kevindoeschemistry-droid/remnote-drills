// A full mock exam in the format of the UCI MAE 120 practice midterms: true/false, multiple
// choice, short answers (no partial credit), then free-response problems. Each paper is built
// from one seed, so "New paper" gives fresh numbers and the same seed rebuilds the same paper.
import { generateTemplate } from "./registry";
import { Rng } from "./rng";
import type { Problem } from "./types";

export interface ExamItem {
  n: number;
  section: string;
  points: number;
  problem: Problem;
}

// which drill teaches each true/false statement
const CONCEPT_SKILL: Record<string, string> = {
  "rad-medium": "ht.rate-equations", "k-direction": "ht.rate-equations",
  "fin-eff-1": "ht.fins", "fin-eta": "ht.fins", "fin-linear": "ht.fins",
  "wall-linear": "ht.resistance-plane", "series-same-q": "ht.resistance-plane", "biggest-drop": "ht.resistance-plane",
  "cyl-linear": "ht.resistance-radial", "q-const-cyl": "ht.resistance-radial", "flux-const-cyl": "ht.resistance-radial",
  "insulation-always": "ht.resistance-radial",
  "tau-large": "ht.lumped", "bi-small": "ht.lumped", "bi-large": "ht.lumped", "lc-sphere": "ht.lumped",
  "shape-k": "ht.shape-factors", "steady-zero-storage": "ht.energy-balance", "laplace-cond": "ht.heat-equation",
  "fd-interior": "ht.finite-difference",
};
const TEMPLATE_SKILLS: Record<string, string[]> = {
  "mae-wall-compare": ["ht.resistance-plane", "ht.exam-concepts"],
  "mae-series-parallel": ["ht.resistance-plane", "ht.exam-concepts"],
  "mae-wall-point": ["ht.resistance-plane", "ht.exam-short"],
  "mae-laplace": ["ht.heat-equation", "ht.exam-concepts"],
  "mae-two-spheres": ["ht.shape-factors", "ht.exam-short"],
  "mae-rod-slab": ["ht.shape-factors", "ht.exam-short"],
  "mae-fd": ["ht.exam-fd", "ht.finite-difference"],
  "mae-pot": ["ht.exam-short", "ht.heat-equation"],
  "ht-bi": ["ht.lumped"],
  "ht-lumped-temp": ["ht.lumped"],
};

/** The drills to do next, from the questions missed: most points lost first. */
export function drillsFor(items: ExamItem[], ok: boolean[]): { skill: string; lost: number; questions: number[] }[] {
  const tally = new Map<string, { lost: number; questions: number[] }>();
  items.forEach((it, i) => {
    if (ok[i]) return;
    const t = it.problem.template;
    const skills = t === "mae-concept"
      ? [CONCEPT_SKILL[(it.problem.meta as any)?.id] ?? "ht.exam-concepts", "ht.exam-concepts"]
      : TEMPLATE_SKILLS[t] ?? [it.problem.skill];
    for (const s of new Set(skills)) {
      const cur = tally.get(s) ?? { lost: 0, questions: [] };
      cur.lost += it.points;
      cur.questions.push(it.n);
      tally.set(s, cur);
    }
  });
  return [...tally.entries()].map(([skill, v]) => ({ skill, ...v })).sort((a, b) => b.lost - a.lost);
}

/** Written parts that can't be auto-graded: prompt + what a full-credit answer contains. */
export const WRITTEN = [
  {
    prompt:
      "Pot on a stove (heat flux $q''$ in at $y = 0$, boiling water at $T_\\infty$ above): write the 1-D steady equation and both boundary conditions, then sketch $T(y)$. How does the sketch change if $q''$ increases while the water stays at $T_\\infty$?",
    model: [
      "$d^2T/dy^2 = 0$ (steady, 1-D, no generation, constant $k$).",
      "BCs: $-k\\,dT/dy|_{y=0} = q''$ (flux in); $-k\\,dT/dy|_{y=L} = h[T(L) - T_\\infty]$ (convection out).",
      "$T(y) = T_\\infty + q''/h + (q''/k)(L - y)$: a straight line, slope $-q''/k$, with $T(L) = T_\\infty + q''/h$ and $T(0) = T_\\infty + q''(L/k + 1/h)$.",
      "Larger $q''$: the line gets steeper, and both $T(0)$ and $T(L)$ rise; $T_\\infty$ stays put. Label the intercepts.",
    ],
  },
  {
    prompt:
      "The pot handle: your boss says the temperature along it falls linearly. Agree? How would you redesign the handle so you can hold it closer to the pot? Give two ways.",
    model: [
      "Disagree: the handle is a fin. Convection off its sides gives $d^2\\theta/dx^2 - m^2\\theta = 0$, so $\\theta$ decays exponentially ($\\cosh/\\sinh$ profile), not linearly. Linear would need no heat loss from the sides.",
      "Lower the handle's $k$ (wood, phenolic, plastic) so $m = \\sqrt{hP/kA_c}$ grows and the temperature drops off faster.",
      "Insulate the base or add a low-$k$ break where the handle joins the pot (more resistance in series).",
      "Make the handle longer or thinner, or add fins / holes to raise $hP$ and shed heat before your hand.",
    ],
  },
];

// Section plan modelled on the 2026 practice midterm (2 points per part).
const PLAN: { section: string; points: number; skill: string; template: string }[] = [
  { section: "True or false", points: 2, skill: "ht.exam-concepts", template: "mae-concept" },
  { section: "True or false", points: 2, skill: "ht.exam-concepts", template: "mae-wall-compare" },
  { section: "True or false", points: 2, skill: "ht.exam-concepts", template: "mae-concept" },
  { section: "True or false", points: 2, skill: "ht.exam-concepts", template: "mae-concept" },
  { section: "Multiple choice (quick calculations)", points: 2, skill: "ht.exam-short", template: "mae-wall-point" },
  { section: "Multiple choice (quick calculations)", points: 2, skill: "ht.exam-concepts", template: "mae-laplace" },
  { section: "Multiple choice (quick calculations)", points: 2, skill: "ht.exam-short", template: "mae-two-spheres" },
  { section: "Multiple choice (quick calculations)", points: 2, skill: "ht.exam-concepts", template: "mae-series-parallel" },
  { section: "Short answer (no partial credit)", points: 2, skill: "ht.exam-short", template: "mae-rod-slab" },
  { section: "Short answer (no partial credit)", points: 2, skill: "ht.exam-short", template: "mae-rod-slab" },
  { section: "Free response", points: 2, skill: "ht.exam-fd", template: "mae-fd" },
  { section: "Free response", points: 2, skill: "ht.exam-fd", template: "mae-fd" },
  { section: "Free response", points: 2, skill: "ht.exam-short", template: "mae-pot" },
  { section: "Free response", points: 2, skill: "ht.lumped", template: "ht-bi" },
  { section: "Free response", points: 2, skill: "ht.lumped", template: "ht-lumped-temp" },
];

export function buildExam(seed: number): ExamItem[] {
  const r = new Rng(seed);
  const used = new Set<string>();
  const out: ExamItem[] = [];
  PLAN.forEach((p, i) => {
    // avoid the same question twice on one paper (e.g. two identical true/false statements)
    let problem = generateTemplate(p.skill, p.template, Math.floor(r.next() * 2 ** 31));
    for (let k = 0; k < 20 && used.has(problem.prompt); k++)
      problem = generateTemplate(p.skill, p.template, Math.floor(r.next() * 2 ** 31));
    used.add(problem.prompt);
    out.push({ n: i + 1, section: p.section, points: p.points, problem });
  });
  return out;
}
