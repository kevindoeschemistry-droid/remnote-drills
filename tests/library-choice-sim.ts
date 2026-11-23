// Library drill cards by framework, progress carried over from courses, and pausing the course
// cards the Library duplicates. Runs against an in-memory stand-in for RemNote.
import {
  coveredCourseCards, DEFAULT_CARD_FRAMEWORKS, DRILLED_FRAMEWORKS, ensureLibrary, getCardFrameworks, LIBRARY, libraryIsCurrent, PATH_LOS, pauseCoveredCourseCards, pausedCourseCards, resumeCourseCards, setCardFrameworks,
} from "../src/drills/library-path";
import { ALL_SKILLS } from "../src/drills/skills";
import { LO_DRILLS } from "../src/drills/target";

let nextId = 0;
const rems = new Map<string, any>();
const store: Record<string, any> = {};
function mk() {
  const r: any = { _id: `r${nextId++}`, text: [], parent: undefined, children: [] as string[], doc: false, practice: true, powerups: {} as Record<string, any> };
  r.setText = async (t: any) => void (r.text = t);
  r.setBackText = async () => {};
  r.setIsDocument = async (d: boolean) => void (r.doc = d);
  r.setEnablePractice = async (on: boolean) => void (r.practice = on);
  r.hasPowerup = async (p: string) => p in r.powerups;
  r.addPowerup = async (p: string) => void (r.powerups[p] ??= {});
  r.getPowerupProperty = async (p: string, s: string) => r.powerups[p]?.[s];
  r.setPowerupProperty = async (p: string, s: string, v: string[]) => void ((r.powerups[p] ??= {})[s] = v.join(""));
  rems.set(r._id, r);
  return r;
}
const plugin: any = {
  rem: {
    createRem: async () => mk(),
    findOne: async (id: string) => rems.get(id),
    moveRems: async ([r]: any[], parent: any, pos: number) => {
      if (r.parent) { const p = rems.get(r.parent); p.children = p.children.filter((c: string) => c !== r._id); }
      r.parent = parent._id;
      parent.children.splice(Math.min(pos, parent.children.length), 0, r._id);
    },
  },
  storage: { getSynced: async (k: string) => store[k] ?? null, setSynced: async (k: string, v: any) => void (store[k] = JSON.parse(JSON.stringify(v))) },
};
const fail = (m: string) => { console.log("FAIL:", m); process.exitCode = 1; };
const cardsIn = (fw: string) => Object.keys(store[`library.map.${fw}`] ?? {}).filter((k) => k.startsWith("card:")).length;
const want = (fw: string) => DRILLED_FRAMEWORKS.find((f) => f.id === fw)?.cards ?? 0;
const allCards = () => LIBRARY.frameworks.reduce((n, f) => n + cardsIn(f.id), 0);

(async () => {
  // a course the user already worked through: one skill the Library will cover, cleared, and one it won't
  const htLos = PATH_LOS.filter((l) => l.fw.id === "heat-transfer" && l.drills.length);
  // a skill whose every template sits under a heat-transfer objective (ht.rate-equations is not one: ht-rad is only a partial match)
  const htTemplates = new Set(htLos.flatMap((l) => LO_DRILLS[l.code].d));
  const whole = (id: string) => { const all = Object.values((ALL_SKILLS.find((s) => s.id === id) as any)?.levels ?? {}).flat() as string[]; return all.length > 0 && all.every((t) => htTemplates.has(t)); };
  const clearedSkill = LO_DRILLS[htLos.find((l) => whole(LO_DRILLS[l.code].s))!.code].s;
  const partSkill = "ht.rate-equations";
  const sameSkill = htLos.filter((l) => LO_DRILLS[l.code].s === clearedSkill).map((l) => l.code);
  const otherLo = htLos.find((l) => LO_DRILLS[l.code].s !== clearedSkill)!;
  store[`odeDrill.progress.${clearedSkill}`] = { consecutive: 5, cleared: true, attempts: 9, correct: 8 };
  const k8Skill = ALL_SKILLS.find((s) => s.status === "live" && PATH_LOS.some((l) => l.fw.id === "math-k8" && LO_DRILLS[l.code]?.s === s.id))!;
  const courseCards = { [`${clearedSkill}:0`]: mk()._id, [`${clearedSkill}:1`]: mk()._id, [`${k8Skill.id}:0`]: mk()._id, [`${partSkill}:0`]: mk()._id };
  store["odeDrill.cardMap"] = courseCards;

  // 1. only the chosen framework gets cards; the outline is complete
  await setCardFrameworks(plugin, ["heat-transfer"]);
  await ensureLibrary(plugin);
  if (cardsIn("heat-transfer") !== want("heat-transfer")) fail(`heat-transfer has ${cardsIn("heat-transfer")} cards, expected ${want("heat-transfer")}`);
  if (allCards() !== want("heat-transfer")) fail(`${allCards()} cards in total, expected only heat-transfer's ${want("heat-transfer")}`);
  const los = LIBRARY.frameworks.reduce((n, f) => n + Object.keys(store[`library.map.${f.id}`]).filter((k) => k.startsWith("lo:")).length, 0);
  if (los !== PATH_LOS.length) fail(`${los} objectives in the outline, expected ${PATH_LOS.length}`);

  // 2. progress carried over for the cleared skill's objectives, and only those
  for (const code of sameSkill) {
    const p = store[`odeDrill.progress.lo:${code}`];
    if (!p?.cleared || p.carriedFrom !== clearedSkill) fail(`${code} did not inherit cleared from ${clearedSkill}`);
  }
  if (store[`odeDrill.progress.lo:${otherLo.code}`]) fail(`${otherLo.code} has progress it never earned`);

  // 3. a streak earned on the Library card is never overwritten by a later build
  store[`odeDrill.progress.lo:${sameSkill[0]}`] = { consecutive: 0, cleared: false, attempts: 3, correct: 1 };
  await ensureLibrary(plugin);
  if (store[`odeDrill.progress.lo:${sameSkill[0]}`].attempts !== 3) fail("a rebuild overwrote progress earned on a Library card");

  // 4. adding a framework adds its cards; removing one keeps the cards already made
  await setCardFrameworks(plugin, ["thermodynamics"]);
  await ensureLibrary(plugin);
  if (cardsIn("thermodynamics") !== want("thermodynamics")) fail(`thermodynamics has ${cardsIn("thermodynamics")} cards, expected ${want("thermodynamics")}`);
  if (cardsIn("heat-transfer") !== want("heat-transfer")) fail("unticking heat-transfer removed its cards");
  if (cardsIn("math-k8") !== 0) fail("math-k8 got cards without being chosen");

  // 5. duplicates: the covered skill's course cards are found, paused, and resumed; the uncovered one is left alone
  const dup = await coveredCourseCards(plugin);
  if (!dup.skills.includes(clearedSkill)) fail(`${clearedSkill} should count as covered by the Library`);
  if (dup.skills.includes(partSkill)) fail(`${partSkill} is only partly covered (ht-rad has no full objective) and must stay on`);
  if (dup.skills.includes(k8Skill.id)) fail(`${k8Skill.id} has no Library cards and should not count as covered`);
  const n = await pauseCoveredCourseCards(plugin);
  const again = await pauseCoveredCourseCards(plugin);
  const off = Object.entries(courseCards).filter(([, id]) => !rems.get(id).practice).map(([k]) => k);
  if (n !== dup.remIds.length || again !== 0) fail(`paused ${n} then ${again}, expected ${dup.remIds.length} then 0`);
  if (off.some((k) => k.startsWith(`${k8Skill.id}:`) || k.startsWith(`${partSkill}:`))) fail("paused a course card the Library does not cover");
  if (!off.includes(`${clearedSkill}:0`) || !off.includes(`${clearedSkill}:1`)) fail("did not pause the covered skill's cards");
  if ((await pausedCourseCards(plugin)) !== n) fail("paused count is wrong");
  const back = await resumeCourseCards(plugin);
  if (back !== n || Object.values(courseCards).some((id) => !rems.get(id).practice)) fail("resume did not turn every paused card back on");

  // 6. a framework that got its first drills after the choice was saved gets cards anyway
  //    (Kevin's DAT and structures, Nov 2026): first a choice saved before the plugin recorded what
  //    was on offer, then one saved since, with a framework that was not on offer at the time
  store["library.cardFrameworks"] = DEFAULT_CARD_FRAMEWORKS.filter((id) => id !== "dat");
  delete store["library.cardFrameworksSeen"];
  const legacy = (await getCardFrameworks(plugin))!;
  if (!legacy.includes("dat")) fail("an old choice without dat did not turn dat on");
  if (legacy.includes("math-k8") || legacy.includes("math-hs")) fail("an old choice turned school maths on");
  if (await libraryIsCurrent(plugin)) fail("a changed card choice should make the Library out of date");
  await ensureLibrary(plugin);
  if (cardsIn("dat") !== want("dat")) fail(`dat has ${cardsIn("dat")} cards, expected ${want("dat")}`);
  if (!(await libraryIsCurrent(plugin))) fail("the Library is not current after the update");
  await setCardFrameworks(plugin, ["chemistry"]);
  store["library.cardFrameworksSeen"] = store["library.cardFrameworksSeen"].filter((id: string) => id !== "structures");
  const later = (await getCardFrameworks(plugin))!;
  if (!later.includes("structures") || later.includes("physics")) fail(`a framework new since the choice should be on and an unticked one off: ${later.join(", ")}`);

  console.log(`library choice: ${want("heat-transfer")} + ${want("thermodynamics")} cards for two frameworks, ${sameSkill.length} objectives inherited "${clearedSkill}", ${dup.remIds.length} course cards found as duplicates (${n} paused and resumed)`);
  process.exit(process.exitCode ?? 0);
})();
