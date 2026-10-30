// What a drill card or panel practices: a skill ("ode1.separable") or a learning objective
// ("lo:CA-6.9.A"), which draws only from the templates the curriculum map lists for it.
import loDrills from "./lo-drills.generated.json";
import { isLive, resolveSkill } from "./skills";

export interface LoDrill {
  t: string; // the objective
  f: string; // framework title
  d: string[]; // templates
  s: string; // skill of the first template (method notes, book place)
}
export const LO_DRILLS = loDrills as Record<string, LoDrill>;

export interface Target {
  key: string; // progress key and card slot value
  skillId: string;
  title: string;
  templates?: string[];
  code?: string;
}

export function resolveTarget(name: string | undefined | null): Target | undefined {
  if (!name) return undefined;
  if (name.startsWith("lo:")) {
    const code = name.slice(3);
    const x = LO_DRILLS[code];
    return x ? { key: name, skillId: x.s, title: `${code} · ${x.t}`, templates: x.d, code } : undefined;
  }
  const s = resolveSkill(name);
  return s ? { key: s.id, skillId: s.id, title: s.title } : undefined;
}

export const isDrillable = (name: string | undefined | null) => (name?.startsWith("lo:") ? !!resolveTarget(name) : isLive(name));
