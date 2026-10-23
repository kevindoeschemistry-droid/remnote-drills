// Section anchors: a PDF highlight (in RemNote) marking where a textbook section
// starts in *your* copy of the book. Drill labels and the "By textbook" contents
// jump there. Stored in synced plugin storage — highlight ids are RemNote's,
// never the repo's.
import type { RNPlugin } from "@remnote/plugin-sdk";
import type { Place, Source } from "./skills";
import { getBindings } from "./deck";

const ANCHORS_KEY = "drills.anchors"; // "<sourceId>|<ref>" -> highlight rem id

/** "3.6" for a section, "ch4" for a chapter */
export const anchorKey = (sourceId: string, ref: string) => `${sourceId}|${ref}`;
export const sectionRef = (p: Pick<Place, "chapter" | "section">) => (p.section ? p.section.ref : `ch${p.chapter.n}`);

export async function getAnchors(plugin: RNPlugin): Promise<Record<string, string>> {
  return (await plugin.storage.getSynced<Record<string, string>>(ANCHORS_KEY)) ?? {};
}

export async function setAnchor(plugin: RNPlugin, sourceId: string, ref: string, highlightId: string | null) {
  const all = await getAnchors(plugin);
  if (highlightId) all[anchorKey(sourceId, ref)] = highlightId;
  else delete all[anchorKey(sourceId, ref)];
  await plugin.storage.setSynced(ANCHORS_KEY, all);
}

/** The anchor for a place: its section, else its chapter. */
export async function anchorFor(plugin: RNPlugin, p: Place): Promise<string | undefined> {
  const all = await getAnchors(plugin);
  return all[anchorKey(p.source.id, sectionRef(p))] ?? all[anchorKey(p.source.id, `ch${p.chapter.n}`)];
}

/** Every anchorable target in a book, in reading order. */
export function targets(src: Source): { ref: string; label: string }[] {
  const out: { ref: string; label: string }[] = [];
  for (const ch of src.chapters) {
    out.push({ ref: `ch${ch.n}`, label: `Ch ${ch.n} · ${ch.title}` });
    for (const s of ch.sections) out.push({ ref: s.ref, label: `§${s.ref} ${s.title}` });
  }
  return out;
}

/**
 * Open the book at a place. Returns what happened so the caller can fall back to the wiki.
 *   "anchor": jumped to the section's highlight in the PDF
 *   "pdf":    no anchor yet, opened the linked PDF
 *   "none":   no PDF linked for this book
 */
export async function openPlace(plugin: RNPlugin, p: Place): Promise<"anchor" | "pdf" | "none"> {
  const hlId = await anchorFor(plugin, p);
  const hl = hlId ? await plugin.rem.findOne(hlId) : undefined;
  const binding = (await getBindings(plugin))[p.source.id];
  const pdfId = binding?.remId ?? hl?.parent ?? undefined;
  const pdf = pdfId ? await plugin.rem.findOne(pdfId) : undefined;
  if (hl) {
    if (pdf) await plugin.window.openRem(pdf);
    // the reader needs a moment to mount before it can scroll
    for (const wait of [400, 900, 1600]) {
      await new Promise((r) => setTimeout(r, wait));
      try {
        await hl.scrollToReaderHighlight();
        return "anchor";
      } catch {
        /* reader not ready yet */
      }
    }
    await hl.openRemInContext();
    return "anchor";
  }
  if (pdf) {
    await plugin.window.openRem(pdf);
    return "pdf";
  }
  return "none";
}

/** Guess the section a highlight marks from its text: "3.6 Heat Transfer from…" or "Chapter 4". */
export function guessRef(src: Source, text: string): string | undefined {
  const t = text.replace(/\s+/g, " ").trim();
  const sec = /^(?:§\s*)?(\d+\.\d+)\b/.exec(t);
  if (sec) {
    const hit = src.chapters.flatMap((c) => c.sections).find((s) => s.ref === sec[1] || s.ref.startsWith(sec[1] + "–"));
    if (hit) return hit.ref;
  }
  const ch = /^(?:chapter|ch\.?)\s*(\d+)\b/i.exec(t);
  if (ch && src.chapters.some((c) => c.n === Number(ch[1]))) return `ch${ch[1]}`;
  const lower = t.toLowerCase();
  for (const c of src.chapters) {
    for (const s of c.sections) if (lower.includes(s.title.toLowerCase())) return s.ref;
    if (lower.includes(c.title.toLowerCase())) return `ch${c.n}`;
  }
  return undefined;
}
