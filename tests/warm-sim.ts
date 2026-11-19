// The warm-up pool and picker against a fake RemNote:
//   nothing warm → empty pool; a cleared skill, a cleared objective and a marked-known objective
//   all join; an objective without a drill never does; a skill already reached through an
//   objective isn't listed twice; the picker never repeats and favours what you haven't done lately.
import { ago, pickWarm, quickOnly, warmPool, warmWeight, MASTERY_KEY, WarmItem } from "../src/drills/warm";
import { PATH_LOS } from "../src/drills/library-path";
import { TIMES_KEY, median, measuredPace, paceOf, recordTime, withTime } from "../src/drills/times";
import { LIVE_SKILLS } from "../src/drills/skills";
import { resolveTarget } from "../src/drills/target";
import { generateFor } from "../src/drills/registry";

const store: Record<string, any> = {};
const plugin: any = { storage: { getSynced: async (k: string) => store[k] ?? null, setSynced: async (k: string, v: any) => void (store[k] = v) } };
const fail = (m: string) => { console.log("FAIL:", m); process.exitCode = 1; };
const DAY = 86400000;

(async () => {
  if ((await warmPool(plugin)).length) fail("pool should be empty before anything is warm");

  const drilled = PATH_LOS.filter((l) => l.drills.length && resolveTarget(`lo:${l.code}`));
  const undrilled = PATH_LOS.find((l) => !l.drills.length)!;
  const [a, b] = drilled;
  const usedSkills = new Set([a, b].map((l) => resolveTarget(`lo:${l.code}`)!.skillId));
  const free = LIVE_SKILLS.find((s) => !usedSkills.has(s.id))!;
  const shared = LIVE_SKILLS.find((s) => s.id === resolveTarget(`lo:${a.code}`)!.skillId)!;

  store[`odeDrill.progress.lo:${a.code}`] = { consecutive: 5, cleared: true, attempts: 9, correct: 8, lastPracticed: Date.now() - 10 * DAY };
  store[MASTERY_KEY] = { [b.code]: "known", [undrilled.code]: "known" };
  store[`odeDrill.progress.${free.id}`] = { consecutive: 0, cleared: true, attempts: 20, correct: 17, lastPracticed: Date.now() };
  store[`odeDrill.progress.${shared.id}`] = { consecutive: 5, cleared: true, attempts: 5, correct: 5 };

  const pool = await warmPool(plugin);
  const targets = pool.map((x) => x.target);
  for (const want of [`lo:${a.code}`, `lo:${b.code}`, free.id]) if (!targets.includes(want)) fail(`pool is missing ${want}`);
  if (targets.includes(`lo:${undrilled.code}`)) fail("an objective with no drill is in the pool");
  if (targets.includes(shared.id)) fail(`${shared.id} is listed as a skill and through ${a.code}`);
  if (pool.length !== 3) fail(`expected 3 warm items, got ${pool.length}: ${targets.join(", ")}`);
  if (pool.find((x) => x.target === free.id)!.reps !== 17) fail("reps should be the correct count");
  if (pool.some((x) => !x.group)) fail("every item needs a group");

  // every pooled target can actually produce a problem
  for (const x of pool) {
    try { if (!generateFor(resolveTarget(x.target)!, 1234).prompt) fail(`${x.target} generated no prompt`); }
    catch (e) { fail(`${x.target} failed to generate: ${e}`); }
  }

  // picker: never the same twice in a row; a miss leaves it warm (cleared is never unset)
  let last: string | null = null;
  const counts: Record<string, number> = {};
  for (let i = 0; i < 3000; i++) {
    const it = pickWarm(pool, last, null)!;
    if (it.target === last) fail("picked the same item twice in a row");
    counts[it.target] = (counts[it.target] ?? 0) + 1;
    last = it.target;
  }
  if (!(counts[`lo:${a.code}`] > counts[free.id])) fail(`something last done 10 days ago should come up more than something done today: ${JSON.stringify(counts)}`);
  const one: WarmItem[] = [pool[0]];
  if (pickWarm(one, one[0].target, null)?.target !== one[0].target) fail("a pool of one must still give that one");
  if (pickWarm(pool, null, pool[0].group)!.group !== pool[0].group) fail("a group filter must stay in the group");
  if (pickWarm([], null, null) !== undefined) fail("an empty pool gives nothing");
  // pace: every drilled objective has one, the mental-math framework has no workouts, and the quick filter drops workouts only
  if (PATH_LOS.some((l) => l.drills.length && !l.pace)) fail("a drilled objective has no pace");
  if (PATH_LOS.some((l) => l.fw.id === "mental-math" && l.pace === "workout")) fail("mental math must stay under a minute");
  if (pool.some((x) => !x.pace)) fail("a warm item has no pace");
  // answer times: a median needs three samples, walks-away are ignored, and measured pace overrides declared
  if (median([9, 3, 30]) !== 9 || median([4, 8]) !== 6 || median([]) !== undefined) fail("median is wrong");
  let ts = withTime({}, "t", 8);
  ts = withTime(ts, "t", 12);
  if (measuredPace(ts, "t") !== undefined) fail("two samples must not decide a pace");
  ts = withTime(ts, "t", 700); // walked away
  if ((ts.t ?? []).length !== 2) fail("a ten-minute answer is not a measurement");
  ts = withTime(ts, "t", 10);
  if (measuredPace(ts, "t") !== "recall") fail("a 10 s median is recall");
  for (let k = 0; k < 20; k++) ts = withTime(ts, "t", 45);
  if (ts.t.length !== 9 || measuredPace(ts, "t") !== "quick") fail("only the last nine times count; a 45 s median is quick");
  if (paceOf(ts, ["t", "u"], "workout") !== "workout") fail("an objective with an untimed drill keeps its declared pace");
  ts = withTime(withTime(withTime(ts, "u", 90), "u", 95), "u", 100);
  if (paceOf(ts, ["t", "u"], "recall") !== "workout") fail("an objective is as slow as its slowest measured drill");
  for (const d of a.drills) for (const sec of [5, 6, 7]) await recordTime(plugin, d, sec);
  if ((store[TIMES_KEY]?.[a.drills[0]] ?? []).length !== 3) fail("recordTime must persist");
  if ((await warmPool(plugin)).find((x) => x.target === `lo:${a.code}`)?.pace !== "recall") fail("measured times must reach the warm pool");
  delete store[TIMES_KEY];
  if (quickOnly(pool).some((x) => x.pace === "workout") || quickOnly(pool).length !== pool.filter((x) => x.pace !== "workout").length) fail("quickOnly must drop the workouts and nothing else");
  if (warmWeight({ target: "x", group: "g", reps: 0 }) !== 3) fail("never-practiced weight");

  const now = Date.UTC(2026, 10, 18);
  const agoCases: [number, string][] = [[0, "today"], [1, "yesterday"], [5, "5 days ago"], [21, "3 weeks ago"], [90, "3 months ago"]];
  for (const [d, want] of agoCases) if (ago(now - d * DAY, now) !== want) fail(`ago(${d} days) = ${ago(now - d * DAY, now)}, want ${want}`);
  if (ago(undefined) !== "") fail("ago(undefined) should be empty");

  console.log(`warm mix: ${pool.length} warm items, picks ${JSON.stringify(Object.values(counts))}`);
  process.exit(process.exitCode ?? 0);
})();
