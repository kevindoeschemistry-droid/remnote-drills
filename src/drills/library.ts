// "Drills: Organize textbook PDFs": create subject documents and file each recognised
// PDF inside its subject as "Author — Title (Ne)". Moves and renames only; never deletes.
// Anchors and PDF links are keyed by rem id, so they survive the move and rename.
import { BuiltInPowerupCodes, RNPlugin } from "@remnote/plugin-sdk";
import graph from "./skills.generated.json";
import { SOURCES, Source } from "./skills";
import { findOrCreateDocument, getBindings, plain, setBinding } from "./deck";
import { findPdfFor } from "./anchors";

interface Library {
  subjects: string[];
  books: Record<string, string>;
  extras: { match: string[]; name: string; subject: string }[];
}
const LIB: Library = (graph as any).library ?? { subjects: [], books: {}, extras: [] };

export const pdfName = (s: Source) => `${s.title}${s.edition && s.edition > 1 ? ` (${s.edition}e)` : ""}`;
type AnyRem = NonNullable<Awaited<ReturnType<RNPlugin["rem"]["findOne"]>>>;

async function fileInto(plugin: RNPlugin, pdf: AnyRem, name: string, subject: AnyRem, log: string[]) {
  const before = plain(pdf.text);
  if (before !== name) await pdf.setText(await plugin.richText.parseFromMarkdown(name));
  if (pdf.parent !== subject._id) await plugin.rem.moveRems([pdf], subject, 0);
  log.push(`${before === name ? name : `“${before}” → “${name}”`} in ${plain(subject.text)}`);
}

async function findExtra(plugin: RNPlugin, words: string[]): Promise<AnyRem | undefined> {
  const hits: any[] = await plugin.search.search([words.join(" ")], undefined, { numResults: 25 }).catch(() => []);
  for (const rem of hits) {
    if (!rem || !(await rem.hasPowerup(BuiltInPowerupCodes.UploadedFile))) continue;
    const name = plain(rem.text).toLowerCase();
    if (words.every((w) => name.includes(w.toLowerCase()))) return rem;
  }
  return undefined;
}

export async function organizeLibrary(plugin: RNPlugin): Promise<string[]> {
  const log: string[] = [];
  const subjects: Record<string, AnyRem> = {};
  for (const name of LIB.subjects) {
    const doc = await findOrCreateDocument(plugin, name, undefined);
    if (doc) subjects[name] = doc;
  }
  const bindings = await getBindings(plugin);
  for (const [sid, subj] of Object.entries(LIB.books)) {
    const src = SOURCES.find((s) => s.id === sid);
    if (!src || !subjects[subj]) continue;
    const bound = bindings[sid]?.remId ? await plugin.rem.findOne(bindings[sid].remId) : undefined;
    const pdf = bound ?? (await findPdfFor(plugin, src));
    if (!pdf) continue;
    await fileInto(plugin, pdf, pdfName(src), subjects[subj], log);
    if (!bound) await setBinding(plugin, sid, { remId: pdf._id, name: pdfName(src) });
  }
  for (const x of LIB.extras) {
    if (!subjects[x.subject]) continue;
    const pdf = await findExtra(plugin, x.match);
    if (pdf) await fileInto(plugin, pdf, x.name, subjects[x.subject], log);
  }
  return log;
}
