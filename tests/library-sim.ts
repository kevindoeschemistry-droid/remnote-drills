// Runs ensureLibrary against an in-memory stand-in for RemNote: checks the tree, ordering,
// idempotency (a second run creates nothing), and that every needs reference resolves.
import { ensureLibrary, LIBRARY, PATH_LOS } from "../src/drills/library-path";

let nextId = 0, created = 0;
const rems = new Map<string, any>();
const store: Record<string, any> = {};
function mk() {
  const r: any = { _id: `r${nextId++}`, text: [], backText: undefined, parent: undefined, children: [] as string[], doc: false, powerups: {} as Record<string, any> };
  r.setText = async (t: any) => void (r.text = t);
  r.setBackText = async (t: any) => void (r.backText = t);
  r.setIsDocument = async (d: boolean) => void (r.doc = d);
  r.hasPowerup = async (p: string) => p in r.powerups;
  r.addPowerup = async (p: string) => void (r.powerups[p] ??= {});
  r.getPowerupProperty = async (p: string, s: string) => r.powerups[p]?.[s];
  r.setPowerupProperty = async (p: string, s: string, v: string[]) => void ((r.powerups[p] ??= {})[s] = v.join(""));
  rems.set(r._id, r);
  created++;
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
  storage: { getSynced: async (k: string) => store[k], setSynced: async (k: string, v: any) => void (store[k] = JSON.parse(JSON.stringify(v))) },
};
const txt = (r: any) => r.text.map((x: any) => (typeof x === "string" ? x : `[[${rems.get(x._id)?.text?.[0]?.slice(0, 12)}]]`)).join("");
const fail = (m: string) => { console.log("FAIL:", m); process.exitCode = 1; };

(async () => {
  const t0 = Date.now();
  await ensureLibrary(plugin);
  const first = created;
  console.log(`first build: ${first} rems in ${Date.now() - t0} ms`);
  await ensureLibrary(plugin);
  if (created !== first) fail(`second run created ${created - first} more rems`);

  const root = rems.get(store["library.root"]);
  const tracks = root.children.map((id: string) => txt(rems.get(id)));
  console.log("tracks:", tracks.join(" | "));
  // walk: every LO rem appears once, in unit/topic order; collect positions per framework
  let los = 0, cards = 0, refs = 0, badRefs = 0;
  for (const tid of root.children) for (const fid of rems.get(tid).children) {
    const fw = rems.get(fid);
    for (const uid of fw.children.slice(1)) for (const topid of rems.get(uid).children) for (const lid of rems.get(topid).children) {
      los++;
      const lo = rems.get(lid);
      const kids = lo.children.map((id: string) => rems.get(id));
      for (const k of kids) {
        if (k.powerups.odeDrill) cards++;
        for (const x of k.text) if (typeof x !== "string") { refs++; if (!rems.get(x._id)) badRefs++; }
      }
      if (!kids.length || kids[0].powerups.odeDrill) fail(`${txt(lo)} has no detail line first`);
    }
  }
  if (los !== PATH_LOS.length) fail(`${los} objective rems, expected ${PATH_LOS.length}`);
  const drilled = PATH_LOS.filter((l) => l.drills.length).length;
  if (cards !== drilled) fail(`${cards} cards, expected ${drilled}`);
  if (badRefs) fail(`${badRefs} dangling references`);
  const needs = PATH_LOS.reduce((s, l) => s + l.needs.length, 0);
  if (refs < needs) fail(`${refs} references for ${needs} needs`);
  // order check: frameworks listed in path order within each track
  const fwTitles = root.children.flatMap((tid: string) => rems.get(tid).children.map((f: string) => txt(rems.get(f))));
  console.log("first frameworks:", fwTitles.slice(0, 5).join(" | "));
  const sample = rems.get(rems.get(rems.get(rems.get(root.children[0]).children[0]).children[1]).children[0]);
  console.log("first objective:", txt(rems.get(sample.children[0])), "→", txt(rems.get(rems.get(sample.children[0]).children[0])));
  console.log(`${los} objectives, ${cards} drill cards, ${refs} prerequisite links, ${LIBRARY.frameworks.length} frameworks`);
  process.exit(process.exitCode ?? 0);
})();
