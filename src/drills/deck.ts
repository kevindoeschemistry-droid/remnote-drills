// Builds the drill structure in RemNote from the drill graph (drills/*.yaml).
//
//   Wiki Flashcards
//   └── Drills
//       ├── First-order ODEs                         ← one group per domain (book-agnostic)
//       │   └── Separable equations
//       │       ├── ODE drill · Separable equations (1)   ← card: ODE Drill powerup with
//       │       └── …                                       Skill + Sources properties
//       ├── …
//       └── By textbook
//           ├── Kreyszig 10e — Advanced Engineering Mathematics
//           │   ├── PDF: [[the linked PDF rem]]           (Drills: Link PDF to a textbook)
//           │   └── Ch 1 · First-Order ODEs
//           │       └── §1.3 Separable ODEs. Modeling
//           │           ├── [[Separable equations]] · drill   ← reference to the skill's card group
//           │           └── Exact equations · planned
//           └── Incropera 8e — …
//
// Cards have ONE home (their skill), so SRS history never moves when books or
// courses change; books are views. Re-running is idempotent and migrates the
// v0.2 / v0.3 layouts in place (synced id map + aliases keep every card).
import type { RNPlugin, RichTextInterface } from "@remnote/plugin-sdk";
import { liveByDomain, placesFor, placeText, resolveSkill, Section, SOURCES, sourceLabel } from "./skills";

export const DRILL_POWERUP = "odeDrill";
export const DRILL_SLOT = "skill";
export const SOURCES_SLOT = "sources";
const MAP_KEY = "odeDrill.cardMap"; // "skill:i" -> remId
const BINDINGS_KEY = "drills.pdfBindings"; // sourceId -> { remId, offset }
export const DRILL_DOC = "Drills";
const LEGACY_DOCS = ["ODE Drills — Level 1"];
const BY_BOOK = "By textbook";

export interface PdfBinding {
  remId: string;
  name?: string;
  offset?: number; // PDF page = printed page + offset
}

const BACK = "Solve the generated problem below this card and press Check. A new problem appears every review.";

async function rt(plugin: RNPlugin, text: string) {
  return plugin.richText.parseFromMarkdown(text);
}

/** plain text of a rem's name (references count as their id) */
export function plain(text: RichTextInterface | undefined): string {
  return (text ?? [])
    .map((el: any) => (typeof el === "string" ? el : el?.i === "q" ? `@${el._id}` : el?.text ?? ""))
    .join("");
}

export async function findOrCreateDocument(plugin: RNPlugin, name: string, parentId: string | undefined) {
  const nameRT = await rt(plugin, name);
  const existing = await plugin.rem.findByName(nameRT, parentId ?? null);
  if (existing) return existing;
  const rem = await plugin.rem.createRem();
  if (!rem) return undefined;
  await rem.setText(nameRT);
  await rem.setIsDocument(true);
  if (parentId) {
    const parent = await plugin.rem.findOne(parentId);
    if (parent) await plugin.rem.moveRems([rem], parent, 0);
  }
  return rem;
}

async function findOrCreateChild(plugin: RNPlugin, name: string, parentId: string, position: number) {
  const nameRT = await rt(plugin, name);
  const existing = await plugin.rem.findByName(nameRT, parentId);
  if (existing) return existing;
  const rem = await plugin.rem.createRem();
  if (!rem) return undefined;
  await rem.setText(nameRT);
  const parent = await plugin.rem.findOne(parentId);
  if (parent) await plugin.rem.moveRems([rem], parent, position);
  return rem;
}

/** Ensure parent has a child whose text is exactly `text` (references allowed). */
async function ensureLine(plugin: RNPlugin, parentId: string, text: RichTextInterface, position: number) {
  const parent = await plugin.rem.findOne(parentId);
  if (!parent) return;
  const want = plain(text);
  for (const c of await parent.getChildrenRem()) if (plain(c.text) === want) return c;
  const rem = await plugin.rem.createRem();
  if (!rem) return;
  await rem.setText(text);
  await plugin.rem.moveRems([rem], parent, position);
  return rem;
}

export async function getBindings(plugin: RNPlugin): Promise<Record<string, PdfBinding>> {
  return (await plugin.storage.getSynced<Record<string, PdfBinding>>(BINDINGS_KEY)) ?? {};
}

export async function setBinding(plugin: RNPlugin, sourceId: string, binding: PdfBinding | null) {
  const all = await getBindings(plugin);
  if (binding) all[sourceId] = binding;
  else delete all[sourceId];
  await plugin.storage.setSynced(BINDINGS_KEY, all);
}

async function drillDoc(plugin: RNPlugin, rootId: string) {
  const name = await rt(plugin, DRILL_DOC);
  let doc = await plugin.rem.findByName(name, rootId);
  if (!doc)
    for (const legacy of LEGACY_DOCS) {
      const old = await plugin.rem.findByName(await rt(plugin, legacy), rootId);
      if (old) {
        await old.setText(name); // rename in place: every card underneath keeps its history
        doc = old;
        break;
      }
    }
  return doc ?? (await findOrCreateDocument(plugin, DRILL_DOC, rootId));
}

/** Find a skill's card group directly under the drills doc or one level down (old layouts). */
async function findSkillGroup(plugin: RNPlugin, docId: string, title: string) {
  const name = await rt(plugin, title);
  const direct = await plugin.rem.findByName(name, docId);
  if (direct) return direct;
  const doc = await plugin.rem.findOne(docId);
  for (const child of (await doc?.getChildrenRem()) ?? []) {
    if (plain(child.text) === BY_BOOK) continue;
    const hit = await plugin.rem.findByName(name, child._id);
    if (hit) return hit;
  }
  return undefined;
}

export async function ensureDrillDeck(plugin: RNPlugin, rootName: string, quiet = false) {
  const perSkill = Math.max(1, Math.min(10, (await plugin.settings.getSetting<number>("drill-cards-per-skill")) || 3));
  const map: Record<string, string> = (await plugin.storage.getSynced<Record<string, string>>(MAP_KEY)) ?? {};

  const root = await findOrCreateDocument(plugin, rootName, undefined);
  if (!root) return void (await plugin.app.toast("Drills: could not create the root document"));
  const doc = await drillDoc(plugin, root._id);
  if (!doc) return void (await plugin.app.toast("Drills: could not create the drills document"));

  // ── cards, homed by domain → skill ─────────────────────────────────────
  let created = 0;
  const groups: Record<string, string> = {}; // skill id -> group rem id
  const domains = liveByDomain();
  for (let d = 0; d < domains.length; d++) {
    const { domain, skills } = domains[d];
    const domainRem = await findOrCreateChild(plugin, domain.title, doc._id, d);
    if (!domainRem) continue;
    for (let s = 0; s < skills.length; s++) {
      const skill = skills[s];
      let group = await plugin.rem.findByName(await rt(plugin, skill.title), domainRem._id);
      if (!group) {
        const old = await findSkillGroup(plugin, doc._id, skill.title);
        if (old) {
          await plugin.rem.moveRems([old], domainRem, s); // keeps SRS history
          group = old;
        } else group = await findOrCreateChild(plugin, skill.title, domainRem._id, s);
      }
      if (!group) continue;
      groups[skill.id] = group._id;
      const sourcesText = placesFor(skill.id).map(placeText).join("; ") || "—";
      for (let i = 1; i <= perSkill; i++) {
        const key = `${skill.id}:${i}`;
        const aliasKey = skill.aliases.map((a) => `${a}:${i}`).find((k) => map[k]);
        if (!map[key] && aliasKey) {
          map[key] = map[aliasKey];
          delete map[aliasKey];
        }
        let rem = map[key] ? await plugin.rem.findOne(map[key]) : undefined;
        if (!rem) {
          rem = await plugin.rem.createRem();
          if (!rem) continue;
          await rem.setText(await rt(plugin, `ODE drill · ${skill.title} (${i})`));
          await rem.setBackText(await rt(plugin, BACK));
          await plugin.rem.moveRems([rem], group, i - 1);
          map[key] = rem._id;
          created++;
        }
        if (!(await rem.hasPowerup(DRILL_POWERUP))) await rem.addPowerup(DRILL_POWERUP);
        if ((await rem.getPowerupProperty(DRILL_POWERUP, DRILL_SLOT))?.trim() !== skill.id)
          await rem.setPowerupProperty(DRILL_POWERUP, DRILL_SLOT, [skill.id]);
        if ((await rem.getPowerupProperty(DRILL_POWERUP, SOURCES_SLOT))?.trim() !== sourcesText)
          await rem.setPowerupProperty(DRILL_POWERUP, SOURCES_SLOT, [sourcesText]);
      }
    }
  }
  await plugin.storage.setSynced(MAP_KEY, map);

  // tidy: v0.3 chapter-unit headers ("Ch 1 · …") left empty by the move
  try {
    for (const child of await doc.getChildrenRem()) {
      if (!/^Ch \d+ · /.test(plain(child.text).trim())) continue;
      if ((await child.getChildrenRem()).length === 0) await child.remove();
    }
  } catch (e) {
    console.error("Drills tidy failed", e);
    await plugin.app.toast(`Drills: tidy step failed — ${String(e)}`);
  }

  // ── books as views ─────────────────────────────────────────────────────
  try {
    await buildTables(plugin, doc._id, groups, domains.length);
  } catch (e) {
    console.error("Drills book contents failed", e);
    await plugin.app.toast(`Drills: book contents failed — ${String(e)}`);
  }

  if (!quiet || created)
    await plugin.app.toast(created ? `Drills: ${created} drill cards created` : "Drills: cards and book contents are up to date");
}

const bookTitle = (s: (typeof SOURCES)[number]) => `${sourceLabel(s)} — ${s.title.split(" — ")[1] ?? s.title}`;
const sectionTitle = (s: Section) => `§${s.ref} ${s.title}${s.pages ? ` (pp. ${s.pages[0]}–${s.pages[1]})` : ""}`;

async function buildTables(plugin: RNPlugin, docId: string, groups: Record<string, string>, position: number) {
  const byBook = await findOrCreateChild(plugin, BY_BOOK, docId, position);
  if (!byBook) return;
  const bindings = await getBindings(plugin);
  for (let b = 0; b < SOURCES.length; b++) {
    const src = SOURCES[b];
    const bookRem = await findOrCreateChild(plugin, bookTitle(src), byBook._id, b);
    if (!bookRem) continue;
    const binding = bindings[src.id];
    // replace any stale PDF line, then add the current one
    for (const c of await bookRem.getChildrenRem())
      if (plain(c.text).startsWith("PDF: ") && (!binding || plain(c.text) !== `PDF: @${binding.remId}`)) await c.remove();
    if (binding) await ensureLine(plugin, bookRem._id, ["PDF: ", { i: "q", _id: binding.remId }] as RichTextInterface, 0);
    for (let c = 0; c < src.chapters.length; c++) {
      const ch = src.chapters[c];
      const chRem = await findOrCreateChild(plugin, `Ch ${ch.n} · ${ch.title}`, bookRem._id, c + 1);
      if (!chRem) continue;
      let pos = 0;
      for (const sid of ch.skills) await skillLine(plugin, chRem._id, sid, groups, pos++);
      for (const sec of ch.sections) {
        const secRem = await findOrCreateChild(plugin, sectionTitle(sec), chRem._id, pos++);
        if (!secRem) continue;
        let k = 0;
        for (const sid of sec.skills) await skillLine(plugin, secRem._id, sid, groups, k++);
      }
    }
  }
}

async function skillLine(plugin: RNPlugin, parentId: string, skillId: string, groups: Record<string, string>, pos: number) {
  const skill = resolveSkill(skillId);
  if (!skill) return;
  const groupId = groups[skill.id];
  if (groupId) {
    // a skill that just went live replaces its "planned" line
    const parent = await plugin.rem.findOne(parentId);
    for (const c of (await parent?.getChildrenRem()) ?? [])
      if (plain(c.text) === `${skill.title} · planned`) await c.remove();
    await ensureLine(plugin, parentId, [{ i: "q", _id: groupId }, " · drill"] as RichTextInterface, pos);
  } else await ensureLine(plugin, parentId, [`${skill.title} · planned`], pos);
}
