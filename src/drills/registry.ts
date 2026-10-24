// Template name (as written in drills/skills.yaml) -> generator.
import { Rng } from "./rng";
import { Reject } from "./reject";
import type { Draft, Problem } from "./types";
import { resolveSkill, templatesFor } from "./skills";
import { FIRST_ORDER_TEMPLATES } from "./gen-first-order";
import { SERIES_TEMPLATES } from "./gen-series";
import { STURM_TEMPLATES } from "./gen-sturm";
import { SPRING_TEMPLATES } from "./gen-spring";
import { LINEAR2_TEMPLATES } from "./gen-linear2";
import { KINETICS_TEMPLATES } from "./gen-kinetics";
import { HEAT_TEMPLATES } from "./gen-heat";
import { LINALG_TEMPLATES } from "./gen-linalg";
import { HEAT3_TEMPLATES } from "./gen-heat3";

export const TEMPLATES: Record<string, (r: Rng) => Draft> = {
  ...FIRST_ORDER_TEMPLATES,
  ...SERIES_TEMPLATES,
  ...STURM_TEMPLATES,
  ...SPRING_TEMPLATES,
  ...LINEAR2_TEMPLATES,
  ...KINETICS_TEMPLATES,
  ...HEAT_TEMPLATES,
  ...LINALG_TEMPLATES,
  ...HEAT3_TEMPLATES,
};

/** Generate one problem for a skill. Same (skill, seed, level) -> same problem. */
export function generate(skillName: string, seed: number, level = 1): Problem {
  const skill = resolveSkill(skillName);
  if (!skill) throw new Error(`unknown skill ${skillName}`);
  const names = templatesFor(skill, level);
  const r = new Rng(seed);
  for (let i = 0; i < 300; i++) {
    const name = names[Math.floor(r.next() * names.length)];
    const fn = TEMPLATES[name];
    if (!fn) throw new Error(`skills.yaml names template "${name}" but no generator exists`);
    try {
      return { skill: skill.id, template: name, level, ...fn(r) };
    } catch (e) {
      if (!(e instanceof Reject)) throw e;
    }
  }
  throw new Error(`could not generate a ${skill.id} problem`);
}

/** Generate from one named template (tests). */
export function generateTemplate(skillId: string, name: string, seed: number): Problem {
  const r = new Rng(seed);
  for (let i = 0; i < 300; i++) {
    try {
      return { skill: skillId, template: name, level: 1, ...TEMPLATES[name](r) };
    } catch (e) {
      if (!(e instanceof Reject)) throw e;
    }
  }
  throw new Error(`template ${name} keeps rejecting`);
}
