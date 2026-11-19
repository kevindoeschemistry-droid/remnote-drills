// How long each kind of problem actually takes you. The declared `pace` on a template is a guess
// until there is data; once a template has a few timed first-try answers, the median replaces it.
// Stored in synced storage as template -> the last few times (seconds), so it follows you across
// devices and stays small.
import type { RNPlugin } from "@remnote/plugin-sdk";
import type { Pace } from "./library-path";

export const TIMES_KEY = "drill.times";
export type Times = Record<string, number[]>;

const KEEP = 9; // times kept per template
export const MIN_SAMPLES = 3; // below this the declared pace stands
export const RECALL_MAX = 15; // seconds: at or under this median, an item is recall
export const QUICK_MAX = 60; // seconds: at or under this median, an item is quick
const IGNORE_OVER = 600; // you walked away; not a measurement

export const loadTimes = async (plugin: RNPlugin): Promise<Times> => (await plugin.storage.getSynced<Times>(TIMES_KEY)) ?? {};

/** add one time-to-correct (first try, no hints) for a template; returns the updated record */
export function withTime(times: Times, template: string, seconds: number): Times {
  if (!template || !Number.isFinite(seconds) || seconds <= 0 || seconds > IGNORE_OVER) return times;
  return { ...times, [template]: [...(times[template] ?? []), Math.round(seconds * 10) / 10].slice(-KEEP) };
}

export async function recordTime(plugin: RNPlugin, template: string, seconds: number): Promise<void> {
  const before = await loadTimes(plugin);
  const after = withTime(before, template, seconds);
  if (after !== before) await plugin.storage.setSynced(TIMES_KEY, after);
}

export function median(xs: number[]): number | undefined {
  if (!xs.length) return undefined;
  const s = [...xs].sort((a, b) => a - b), m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
}

/** the pace your own times show for a template, once there are enough of them */
export function measuredPace(times: Times, template: string): Pace | undefined {
  const xs = times[template] ?? [];
  if (xs.length < MIN_SAMPLES) return undefined;
  const m = median(xs)!;
  return m <= RECALL_MAX ? "recall" : m <= QUICK_MAX ? "quick" : "workout";
}

const ORDER: Pace[] = ["recall", "quick", "workout"];
/** an objective is as slow as its slowest drill: measured where every drill has data, declared otherwise */
export function paceOf(times: Times, drills: string[], declared: Pace | undefined): Pace {
  const m = drills.map((d) => measuredPace(times, d));
  if (drills.length && m.every(Boolean)) return ORDER[Math.max(...m.map((p) => ORDER.indexOf(p!)))];
  return declared ?? "workout";
}
