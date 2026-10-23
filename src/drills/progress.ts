// Per-skill streaks, stored in RemNote synced storage so they follow you across devices.
// Same rule as the wiki's drill zones: N correct in a row clears the skill;
// a wrong answer or "show solution" resets the streak.
// Keys use the canonical skill id; a streak saved under an old alias is read once and migrated.
import type { RNPlugin } from "@remnote/plugin-sdk";
import { resolveSkill } from "./skills";

export interface SkillProgress {
  consecutive: number;
  cleared: boolean;
  attempts: number;
  correct: number;
  lastPracticed?: number;
}

const key = (id: string) => `odeDrill.progress.${id}`;
export const EMPTY: SkillProgress = { consecutive: 0, cleared: false, attempts: 0, correct: 0 };

export async function getProgress(plugin: RNPlugin, name: string): Promise<SkillProgress> {
  const skill = resolveSkill(name);
  if (!skill) return { ...EMPTY };
  let saved = await plugin.storage.getSynced<SkillProgress>(key(skill.id));
  if (!saved) {
    for (const alias of skill.aliases) {
      saved = await plugin.storage.getSynced<SkillProgress>(key(alias));
      if (saved) {
        await plugin.storage.setSynced(key(skill.id), saved);
        break;
      }
    }
  }
  return { ...EMPTY, ...(saved ?? {}) };
}

export async function recordAttempt(
  plugin: RNPlugin,
  name: string,
  outcome: "correct" | "wrong" | "revealed",
  clearAt: number
): Promise<SkillProgress> {
  const skill = resolveSkill(name)!;
  const p = await getProgress(plugin, skill.id);
  p.attempts += outcome === "revealed" ? 0 : 1;
  if (outcome === "correct") {
    p.correct += 1;
    p.consecutive += 1;
    if (p.consecutive >= clearAt) p.cleared = true;
  } else {
    p.consecutive = 0;
  }
  p.lastPracticed = Date.now();
  await plugin.storage.setSynced(key(skill.id), p);
  return p;
}

export async function resetProgress(plugin: RNPlugin, name: string): Promise<void> {
  const skill = resolveSkill(name)!;
  await plugin.storage.setSynced(key(skill.id), { ...EMPTY });
}
