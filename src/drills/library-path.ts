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

type Rem = NonNullable<Awaited<ReturnType<RNPlugin["rem"]["findOne"]>>>;

export interface PathLo { code: string; pos: number; do: string; ek: string; std: string; needs: string[]; drills: string[] }
export interface PathTopic { n: number; title: string; los: PathLo[] }
export interface PathUnit { n: number; title: string; scope: string; topics: PathTopic[] }
export interface PathFramework { id: string; title: string; code: string; track: string; requires: string[]; units: PathUnit[] }

export const LIBRARY = lib as unknown as { tracks: Record<string, string>; frameworks: PathFramework[] };
export const LIBRARY_ROOT = "KevinDoesChemistry Library";
const ROOT_KEY = "library.root";
const mapKey = (fw: string) => `library.map.${fw}`;
const SIG_KEY = "library.signature";

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

export async function libraryRemId(plugin: RNPlugin, code: string): Promise<string | undefined> {
  const lo = LO_BY_CODE.get(code);
  if (!lo) return undefined;
  const map = (await plugin.storage.getSynced<Record<string, string>>(mapKey(lo.fw.id))) ?? {};
  return map[`lo:${code}`];
}

export function librarySignature(): string {
  const text = JSON.stringify(LIBRARY.frameworks.map((f) => [f.id, f.title, f.units.map((u) => [u.title, u.topics.map((t) => [t.title, t.los.map((l) => [l.code, l.pos, l.do, l.ek, l.std, l.needs, l.drills])])])]));
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
  const ensure = async (map: Record<string, string>, key: string, parent: Rem, text: RichTextInterface, pos: number, doc = false) => {
    let rem = map[key] ? await plugin.rem.findOne(map[key]) : undefined;
    if (!rem) {
      rem = await plugin.rem.createRem();
      if (!rem) throw new Error("RemNote refused to create a rem");
      await rem.setText(text);
      if (doc) await rem.setIsDocument(true);
      await plugin.rem.moveRems([rem], parent, pos);
      map[key] = rem._id;
    } else {
      if (plain(rem.text) !== plain(text)) await rem.setText(text);
      if (rem.parent !== parent._id) await plugin.rem.moveRems([rem], parent, pos);
    }
    return rem;
  };

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
    const fwNum = LIBRARY.frameworks.indexOf(fw) + 1;
    const fwRem = await ensure(map, "fw", trackRems[fw.track], [`${fwNum} · ${fw.title}`], k, true);
    frameworkRem[fw.id] = fwRem._id;
    const [a, b] = range(fw);
    const reqs: RichTextInterface = fw.requires.length
      ? [`Path #${a}–${b} · after `, ...fw.requires.flatMap((r, i) => [...(i ? [", "] : []), frameworkRem[r] ? ({ i: "q", _id: frameworkRem[r] } as any) : r])]
      : [`Path #${a}–${b} · no prerequisites`];
    await ensure(map, "meta", fwRem, reqs, 0);

    for (let ui = 0; ui < fw.units.length; ui++) {
      const u = fw.units[ui];
      const unitRem = await ensure(map, `u:${u.n}`, fwRem, [`Unit ${u.n} · ${u.title}${u.scope && u.scope !== "core" ? ` (${u.scope})` : ""}`], ui + 1, true);
      for (let ti = 0; ti < u.topics.length; ti++) {
        const t = u.topics[ti];
        const topicRem = await ensure(map, `t:${u.n}.${t.n}`, unitRem, [`${u.n}.${t.n} ${t.title}`], ti);
        for (let li = 0; li < t.los.length; li++) {
          const lo = t.los[li];
          const loRem = await ensure(map, `lo:${lo.code}`, topicRem, [loTitle(lo)], li);
          if (lo.drills.length) {
            const card = await ensure(map, `card:${lo.code}`, loRem, [`Drill · ${lo.code}`], 1);
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
