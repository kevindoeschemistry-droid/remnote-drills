// The warm-up mix: random problems from everything that's already easy for you.
// "Warm" = five in a row at some point (a course skill or a Library objective), or an
// objective you marked known / tested out of on the Path tab. Warm never expires and a miss
// doesn't take it away: the point is to keep doing the easy things, not to finish them.
import type { RNPlugin } from "@remnote/plugin-sdk";
import { DOMAINS, LIVE_SKILLS } from "./skills";
import { PATH_LOS } from "./library-path";
import { getProgress } from "./progress";
import { resolveTarget } from "./target";

export const MASTERY_KEY = "path.mastery"; // code -> "tested" | "known" (PathView)

export interface WarmItem {
  target: string; // what DrillPanel practices: a skill id or "lo:CODE"
  group: string; // framework or subject, for the chips
  reps: number;
  last?: number;
  /** recall ≈ 10 s, quick < 1 min, workout longer; a course skill mixes templates, so it counts as a workout */
  pace: "recall" | "quick" | "workout";
}

export async function warmPool(plugin: RNPlugin): Promise<WarmItem[]> {
  const marks = (await plugin.storage.getSynced<Record<string, string>>(MASTERY_KEY)) ?? {};
  const out: WarmItem[] = [];
  const viaObjective = new Set<string>();
  for (const lo of PATH_LOS) {
    if (!lo.drills.length) continue;
    const t = resolveTarget(`lo:${lo.code}`);
    if (!t) continue;
    const p = await getProgress(plugin, t.key);
    if (!p.cleared && !marks[lo.code]) continue;
    out.push({ target: t.key, group: lo.fw.title, reps: p.correct, last: p.lastPracticed, pace: lo.pace ?? "workout" });
    viaObjective.add(t.skillId);
  }
  // course skills, unless an objective above already draws on the same skill
  for (const s of LIVE_SKILLS) {
    if (viaObjective.has(s.id)) continue;
    const p = await getProgress(plugin, s.id);
    if (!p.cleared) continue;
    out.push({ target: s.id, group: DOMAINS.find((d) => d.id === s.domain)?.title ?? s.domain, reps: p.correct, last: p.lastPracticed, pace: "workout" });
  }
  return out;
}

/** the part of the pool that fits a short sitting: everything but the workouts */
export const quickOnly = (pool: WarmItem[]) => pool.filter((x) => x.pace !== "workout");

const DAY = 86400000;
/** the longer since you last did it, the likelier it comes up (1× today … 3× a week or more ago) */
export const warmWeight = (it: WarmItem, now = Date.now()) => (it.last ? 1 + 2 * Math.min(1, (now - it.last) / (7 * DAY)) : 3);

/** a weighted random item, never the one you just did unless it's the only one */
export function pickWarm(pool: WarmItem[], last: string | null, group: string | null, rand = Math.random, now = Date.now()): WarmItem | undefined {
  const inGroup = group ? pool.filter((x) => x.group === group) : pool;
  const from = inGroup.length > 1 ? inGroup.filter((x) => x.target !== last) : inGroup;
  let t = rand() * from.reduce((a, x) => a + warmWeight(x, now), 0);
  for (const x of from) if ((t -= warmWeight(x, now)) <= 0) return x;
  return from[from.length - 1];
}

/** "today", "yesterday", "5 days ago", "3 weeks ago" */
export function ago(ts: number | undefined, now = Date.now()): string {
  if (!ts) return "";
  const d = Math.floor((now - ts) / DAY);
  if (d <= 0) return "today";
  if (d === 1) return "yesterday";
  if (d < 14) return `${d} days ago`;
  if (d < 60) return `${Math.floor(d / 7)} weeks ago`;
  return `${Math.floor(d / 30)} months ago`;
}
