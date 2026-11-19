// The whole curriculum in RemNote, in path order:
//
//   KevinDoesChemistry Library                        (document)
//   ├── 1 · Math                                        (document: a track)
//   │   ├── 1 · Mathematics K–8 (Common Core)           (document: a framework, path #1–258)
//   │   │   ├── Path #1–258 · no prerequisites
//   │   │   ├── Unit 1 · Kindergarten                   (document: practice a unit from the queue)
//   │   │   │   └── 1.1 Counting and cardinality
//   │   │   │       └── #1 · MK-1.1.A · Count to 100 by ones and by tens.
//   │   │   │           ├── K.CC.A.1 · <essential knowledge> · Needs: [[#…]]
//   │   │   │           └── Drill · MK-1.1.A           (card, only where drills exist)
//   │   │   …
//   │   └── 2 · High School Mathematics …
//   ├── 2 · Science …
//
// Ids live in synced storage per framework ("library.map.<id>"), so re-running is cheap and
// idempotent: it only creates what's missing and fixes text that changed in the YAML.
import type { RNPlugin, RichTextInterface } from "@remnote/plugin-sdk";
import lib from "./path.generated.json";
import { BACK, DRILL_POWERUP, DRILL_SLOT, plain } from "./deck";
import { ALL_SKILLS } from "./skills";
import { LO_DRILLS } from "./target";

type Rem = NonNullable<Awaited<ReturnType<RNPlugin["rem"]["findOne"]>>>;

export type Pace = "recall" | "quick" | "workout";
/** `pace`: how long the objective's slowest drill takes (recall ≈ 10 s, quick < 1 min, workout longer) */
export interface PathLo { code: string; pos: number; do: string; ek: string; std: string; needs: string[]; drills: string[]; pace?: Pace }
export interface PathTopic { n: number; title: string; los: PathLo[] }
export interface PathUnit { n: number; title: string; scope: string; topics: PathTopic[] }
export interface PathFramework { id: string; title: string; code: string; track: string; requires: string[]; units: PathUnit[] }

export const LIBRARY = lib as unknown as { tracks: Record<string, string>; frameworks: PathFramework[] };
export const LIBRARY_ROOT = "KevinDoesChemistry Library";
const ROOT_KEY = "library.root";
const mapKey = (fw: string) => `library.map.${fw}`;
const SIG_KEY = "library.signature";

// ── which frameworks get drill cards ──────────────────────────────────────────
// The outline is always built for every framework. Drill cards are flashcards in your queue,
// so they are only created for the frameworks you choose. Unset means "all" (how it worked
// before there was a choice); the Path tab always saves an explicit choice before building.
const CARD_FWS_KEY = "library.cardFrameworks";
const PAUSED_KEY = "library.pausedCourseCards";
const COURSE_CARD_MAP_KEY = "odeDrill.cardMap"; // deck.ts: "skill:i" -> remId
const progressKey = (id: string) => `odeDrill.progress.${id}`;

/** frameworks with at least one drilled objective, and how many cards each would add */
export const DRILLED_FRAMEWORKS: { id: string; title: string; cards: number }[] = (lib as any).frameworks
  .map((fw: PathFramework) => ({ id: fw.id, title: fw.title, cards: fw.units.reduce((n, u) => n + u.topics.reduce((m, t) => m + t.los.filter((l) => l.drills.length).length, 0), 0) }))
  .filter((f: { cards: number }) => f.cards > 0);
/** school maths is in the outline but off for cards until you turn it on */
export const DEFAULT_CARD_FRAMEWORKS: string[] = DRILLED_FRAMEWORKS.filter((f) => f.id !== "math-k8" && f.id !== "math-hs").map((f) => f.id);

/** undefined when no choice has ever been saved (RemNote answers null for a key never set) */
export const getCardFrameworks = async (plugin: RNPlugin): Promise<string[] | undefined> => (await plugin.storage.getSynced<string[] | null>(CARD_FWS_KEY)) ?? undefined;
export const setCardFrameworks = (plugin: RNPlugin, ids: string[]) => plugin.storage.setSynced(CARD_FWS_KEY, ids);

/**
 * A new Library card for an objective whose skill you already cleared in a course starts cleared.
 * Only fills an untouched objective; never overwrites a streak earned on the Library card itself.
 */
async function carryOverProgress(plugin: RNPlugin, code: string): Promise<boolean> {
  const skill = LO_DRILLS[code]?.s;
  if (!skill) return false;
  const mine = await plugin.storage.getSynced<{ attempts?: number; cleared?: boolean }>(progressKey(`lo:${code}`));
  if (mine?.attempts || mine?.cleared) return false;
  const theirs = await plugin.storage.getSynced<{ cleared?: boolean }>(progressKey(skill));
  if (!theirs?.cleared) return false;
  await plugin.storage.setSynced(progressKey(`lo:${code}`), { ...theirs, carriedFrom: skill });
  return true;
}

/**
 * Course cards that the Library now duplicates: a course skill counts as covered when every
 * template it draws from belongs to an objective that has a Library card.
 */
export async function coveredCourseCards(plugin: RNPlugin): Promise<{ skills: string[]; remIds: string[] }> {
  const templates = new Set<string>();
  for (const fw of LIBRARY.frameworks) {
    const map = (await plugin.storage.getSynced<Record<string, string>>(mapKey(fw.id))) ?? {};
    for (const k of Object.keys(map)) if (k.startsWith("card:")) for (const t of LO_DRILLS[k.slice(5)]?.d ?? []) templates.add(t);
  }
  const covered = new Set(
    ALL_SKILLS.filter((s) => {
      const all = Object.values((s as any).levels ?? {}).flat() as string[];
      return all.length > 0 && all.every((t) => templates.has(t));
    }).map((s) => s.id),
  );
  const cardMap = (await plugin.storage.getSynced<Record<string, string>>(COURSE_CARD_MAP_KEY)) ?? {};
  const skills = new Set<string>();
  const remIds: string[] = [];
  for (const [k, id] of Object.entries(cardMap)) {
    const skill = k.slice(0, k.lastIndexOf(":"));
    if (covered.has(skill)) {
      skills.add(skill);
      remIds.push(id);
    }
  }
  return { skills: [...skills], remIds };
}

/** how many course cards this plugin has paused */
export const pausedCourseCards = async (plugin: RNPlugin) => ((await plugin.storage.getSynced<string[]>(PAUSED_KEY)) ?? []).length;

/**
 * Pause the course cards the Library duplicates, so each drill is due once. Nothing is deleted:
 * the cards keep their text and review history, and resumeCourseCards turns them back on.
 */
export async function pauseCoveredCourseCards(plugin: RNPlugin): Promise<number> {
  const { remIds } = await coveredCourseCards(plugin);
  const paused = new Set((await plugin.storage.getSynced<string[]>(PAUSED_KEY)) ?? []);
  let n = 0;
  for (const id of remIds) {
    if (paused.has(id)) continue;
    const rem = await plugin.rem.findOne(id);
    if (!rem) continue;
    await rem.setEnablePractice(false);
    paused.add(id);
    n++;
  }
  await plugin.storage.setSynced(PAUSED_KEY, [...paused]);
  return n;
}

export async function resumeCourseCards(plugin: RNPlugin): Promise<number> {
  const paused = (await plugin.storage.getSynced<string[]>(PAUSED_KEY)) ?? [];
  let n = 0;
  for (const id of paused) {
    const rem = await plugin.rem.findOne(id);
    if (!rem) continue;
    await rem.setEnablePractice(true);
    n++;
  }
  await plugin.storage.setSynced(PAUSED_KEY, []);
  return n;
}

/** every objective in path order */
export const PATH_LOS: (PathLo & { fw: PathFramework; unit: PathUnit; topic: PathTopic })[] = LIBRARY.frameworks
  .flatMap((fw) => fw.units.flatMap((unit) => unit.topics.flatMap((topic) => topic.los.map((lo) => ({ ...lo, fw, unit, topic })))))
  .sort((a, b) => a.pos - b.pos);
export const LO_BY_CODE = new Map(PATH_LOS.map((x) => [x.code, x]));

export const trackOrder = (): string[] => [...new Set(LIBRARY.frameworks.map((f) => f.track))];

const range = (fw: PathFramework) => {
  const ps = fw.units.flatMap((u) => u.topics.flatMap((t) => t.los.map((l) => l.pos)));
  return [Math.min(...ps), Math.max(...ps)];
};
const loTitle = (lo: PathLo) => `#${lo.pos} · ${lo.code} · ${lo.do}`;
// units and frameworks you can't practice yet say so in their title, so an empty one reads as
// "not written yet" rather than "broken"
const NO_DRILLS = " · no drills yet";
const unitDrilled = (u: PathUnit) => u.topics.some((t) => t.los.some((l) => l.drills.length));
const unitTitle = (u: PathUnit) => `Unit ${u.n} · ${u.title}${u.scope && u.scope !== "core" ? ` (${u.scope})` : ""}${unitDrilled(u) ? "" : NO_DRILLS}`;
const fwTitle = (fw: PathFramework) => `${LIBRARY.frameworks.indexOf(fw) + 1} · ${fw.title}${fw.units.some(unitDrilled) ? "" : NO_DRILLS}`;

export async function libraryRemId(plugin: RNPlugin, code: string): Promise<string | undefined> {
  const lo = LO_BY_CODE.get(code);
  if (!lo) return undefined;
  const map = (await plugin.storage.getSynced<Record<string, string>>(mapKey(lo.fw.id))) ?? {};
  return map[`lo:${code}`];
}

export function librarySignature(): string {
  const text = JSON.stringify(LIBRARY.frameworks.map((f) => [f.id, fwTitle(f), f.units.map(unitTitle), f.units.map((u) => [u.title, u.topics.map((t) => [t.title, t.los.map((l) => [l.code, l.pos, l.do, l.ek, l.std, l.needs, l.drills])])])]));
  let h = 2166136261;
  for (let i = 0; i < text.length; i++) h = Math.imul(h ^ text.charCodeAt(i), 16777619);
  return (h >>> 0).toString(36);
}

export async function libraryIsBuilt(plugin: RNPlugin) {
  return !!(await plugin.storage.getSynced<string>(ROOT_KEY));
}
export async function libraryIsCurrent(plugin: RNPlugin) {
  return (await plugin.storage.getSynced<string>(SIG_KEY)) === librarySignature();
}

/**
 * Build (or bring up to date) the whole library. onProgress gets (done, total, label) after each
 * framework. Safe to stop and re-run: ids are saved after every framework.
 */
export async function ensureLibrary(plugin: RNPlugin, onProgress?: (done: number, total: number, label: string) => void) {
  const ensure = async (map: Record<string, string>, key: string, parent: Rem, text: RichTextInterface, pos: number, doc = false, keepText = false) => {
    let rem = map[key] ? await plugin.rem.findOne(map[key]) : undefined;
    if (!rem) {
      rem = await plugin.rem.createRem();
      if (!rem) throw new Error("RemNote refused to create a rem");
      await rem.setText(text);
      if (doc) await rem.setIsDocument(true);
      await plugin.rem.moveRems([rem], parent, pos);
      map[key] = rem._id;
    } else {
      if (!keepText && plain(rem.text) !== plain(text)) await rem.setText(text);
      if (rem.parent !== parent._id) await plugin.rem.moveRems([rem], parent, pos);
    }
    return rem;
  };

  const chosen = await getCardFrameworks(plugin);
  const cardsOn = (fw: string) => chosen === undefined || chosen.includes(fw);

  // root
  const rootMap: Record<string, string> = {};
  const rootId = await plugin.storage.getSynced<string>(ROOT_KEY);
  let root = rootId ? await plugin.rem.findOne(rootId) : undefined;
  if (!root) {
    root = await plugin.rem.createRem();
    if (!root) throw new Error("RemNote refused to create the library");
    await root.setText([LIBRARY_ROOT]);
    await root.setIsDocument(true);
    await plugin.storage.setSynced(ROOT_KEY, root._id);
  }
  const trackMap = (await plugin.storage.getSynced<Record<string, string>>("library.tracks")) ?? rootMap;
  const tracks = trackOrder();
  const trackRems: Record<string, Rem> = {};
  for (let i = 0; i < tracks.length; i++)
    trackRems[tracks[i]] = await ensure(trackMap, tracks[i], root, [`${i + 1} · ${LIBRARY.tracks[tracks[i]] ?? tracks[i]}`], i, true);
  await plugin.storage.setSynced("library.tracks", trackMap);

  const total = PATH_LOS.length;
  let done = 0;
  const fwIndexInTrack: Record<string, number> = {};
  const frameworkRem: Record<string, string> = {};
  for (const fw of LIBRARY.frameworks) {
    const map = (await plugin.storage.getSynced<Record<string, string>>(mapKey(fw.id))) ?? {};
    const k = (fwIndexInTrack[fw.track] = (fwIndexInTrack[fw.track] ?? -1) + 1);
    const fwRem = await ensure(map, "fw", trackRems[fw.track], [fwTitle(fw)], k, true);
    frameworkRem[fw.id] = fwRem._id;
    const [a, b] = range(fw);
    const reqs: RichTextInterface = fw.requires.length
      ? [`Path #${a}–${b} · after `, ...fw.requires.flatMap((r, i) => [...(i ? [", "] : []), frameworkRem[r] ? ({ i: "q", _id: frameworkRem[r] } as any) : r])]
      : [`Path #${a}–${b} · no prerequisites`];
    await ensure(map, "meta", fwRem, reqs, 0);

    for (let ui = 0; ui < fw.units.length; ui++) {
      const u = fw.units[ui];
      const unitRem = await ensure(map, `u:${u.n}`, fwRem, [unitTitle(u)], ui + 1, true);
      for (let ti = 0; ti < u.topics.length; ti++) {
        const t = u.topics[ti];
        const topicRem = await ensure(map, `t:${u.n}.${t.n}`, unitRem, [`${u.n}.${t.n} ${t.title}`], ti);
        for (let li = 0; li < t.los.length; li++) {
          const lo = t.los[li];
          const loRem = await ensure(map, `lo:${lo.code}`, topicRem, [loTitle(lo)], li);
          // cards only for the frameworks you chose; a card that already exists is kept either way
          if (lo.drills.length && (cardsOn(fw.id) || map[`card:${lo.code}`])) {
            const isNew = !map[`card:${lo.code}`];
            // a card's text is its current written-out problem (static-card.ts), so it's never reset here
            const card = await ensure(map, `card:${lo.code}`, loRem, [`Drill · ${lo.code}`], 1, false, true);
            if (isNew) await carryOverProgress(plugin, lo.code);
            if (!(await card.hasPowerup(DRILL_POWERUP))) {
              await card.setBackText([BACK]);
              await card.addPowerup(DRILL_POWERUP);
            }
            if ((await card.getPowerupProperty(DRILL_POWERUP, DRILL_SLOT))?.trim() !== `lo:${lo.code}`)
              await card.setPowerupProperty(DRILL_POWERUP, DRILL_SLOT, [`lo:${lo.code}`]);
          }
        }
      }
    }
    await plugin.storage.setSynced(mapKey(fw.id), map);
    done += fw.units.reduce((s, u) => s + u.topics.reduce((x, t) => x + t.los.length, 0), 0);
    onProgress?.(done, total, fw.title);
  }

  // second pass: detail lines, now that every objective has a rem to link to
  const ids = new Map<string, string>();
  const maps: Record<string, Record<string, string>> = {};
  for (const fw of LIBRARY.frameworks) {
    maps[fw.id] = (await plugin.storage.getSynced<Record<string, string>>(mapKey(fw.id))) ?? {};
    for (const [k, v] of Object.entries(maps[fw.id])) if (k.startsWith("lo:")) ids.set(k.slice(3), v);
  }
  done = 0;
  for (const fw of LIBRARY.frameworks) {
    const map = maps[fw.id];
    for (const u of fw.units)
      for (const t of u.topics)
        for (const lo of t.los) {
          const loRem = await plugin.rem.findOne(map[`lo:${lo.code}`]);
          if (!loRem) continue;
          const text: RichTextInterface = [[lo.std, lo.ek].filter(Boolean).join(" · ") || "—"];
          if (lo.needs.length) {
            text.push(" · Needs: ");
            lo.needs.forEach((n, i) => {
              if (i) text.push(" ");
              const id = ids.get(n);
              text.push(id ? ({ i: "q", _id: id } as any) : n);
            });
          }
          await ensure(map, `d:${lo.code}`, loRem, text, 0);
        }
    await plugin.storage.setSynced(mapKey(fw.id), map);
    done += fw.units.reduce((s, u) => s + u.topics.reduce((x, t) => x + t.los.length, 0), 0);
    onProgress?.(done, total, `${fw.title} · links`);
  }
  await plugin.storage.setSynced(SIG_KEY, librarySignature());
}
