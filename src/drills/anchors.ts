// Section anchors: a PDF highlight (in RemNote) marking where a textbook section
// starts in *your* copy of the book. Drill labels and the "By textbook" contents
// jump there. Stored in synced plugin storage — highlight ids are RemNote's,
// never the repo's.
import type { RNPlugin } from "@remnote/plugin-sdk";
import type { Place, Source } from "./skills";
import { getBindings, plain, setBinding } from "./deck";
import { BuiltInPowerupCodes } from "@remnote/plugin-sdk";

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
  // nothing linked yet: look for a PDF that matches the book and link it
  const found = await findPdfFor(plugin, p.source);
  if (found) {
    await setBinding(plugin, p.source.id, { remId: found._id, name: plain(found.text) || undefined });
    await plugin.app.toast(`Linked “${plain(found.text)}” as ${p.source.short}. Anchor sections to jump straight to them.`);
    await plugin.window.openRem(found);
    return "pdf";
  }
  return "none";
}

const words = (s: string) =>
  s
    .toLowerCase()
    .replace(/[^a-z0-9 ]+/g, " ")
    .split(/\s+/)
    .filter((w) => w.length > 2 && !["the", "and", "with", "its", "for", "edition"].includes(w));

/** A PDF in RemNote whose name matches the book (author + title words), or undefined. */
export async function findPdfFor(plugin: RNPlugin, src: Source) {
  const title = src.title.split(" — ")[1] ?? src.title;
  const want = new Set([...words(src.short), ...words(title)]);
  const seen = new Set<string>();
  let best: { rem: any; score: number } | undefined;
  for (const q of [`${src.short} ${title}`, title, src.short]) {
    let hits: any[] = [];
    try {
      hits = await plugin.search.search([q], undefined, { numResults: 20 });
    } catch {
      continue;
    }
    for (const rem of hits) {
      if (!rem || seen.has(rem._id)) continue;
      seen.add(rem._id);
      if (!(await rem.hasPowerup(BuiltInPowerupCodes.UploadedFile))) continue;
      const have = new Set(words(plain(rem.text)));
      const score = [...want].filter((w) => have.has(w)).length;
      // author name + at least one title word
      if (have.has(src.short.toLowerCase().split(" ")[0]) && score >= 2 && (!best || score > best.score)) best = { rem, score };
    }
  }
  return best?.rem;
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

type AnyRem = NonNullable<Awaited<ReturnType<RNPlugin["rem"]["findOne"]>>>;

/** The PDF a highlight belongs to: its PdfId slot, else the nearest uploaded-file ancestor. */
export async function pdfOf(plugin: RNPlugin, hl: AnyRem): Promise<string | undefined> {
  try {
    const viaSlot = await hl.getPowerupPropertyAsRem(BuiltInPowerupCodes.PDFHighlight, "PdfId");
    if (viaSlot) return viaSlot._id;
  } catch {
    /* slot not readable */
  }
  let cur: AnyRem | undefined = hl;
  for (let i = 0; i < 6 && cur?.parent; i++) {
    cur = await plugin.rem.findOne(cur.parent);
    if (cur && (await cur.hasPowerup(BuiltInPowerupCodes.UploadedFile))) return cur._id;
  }
  return hl.parent ?? undefined;
}

/** The newest highlight in the PDF that's open (or that contains the focused rem). */
export async function latestHighlight(plugin: RNPlugin): Promise<AnyRem | undefined> {
  const paneRemId = await plugin.window.getOpenPaneRemId(await plugin.window.getFocusedPaneId());
  let pdf: AnyRem | undefined = paneRemId ? await plugin.rem.findOne(paneRemId) : undefined;
  // walk up to the uploaded PDF if the pane is showing something inside it
  for (let i = 0; i < 6 && pdf && !(await pdf.hasPowerup(BuiltInPowerupCodes.UploadedFile)); i++)
    pdf = pdf.parent ? await plugin.rem.findOne(pdf.parent) : undefined;
  if (!pdf) return undefined;
  let best: AnyRem | undefined;
  for (const r of await pdf.getDescendants())
    if ((!best || r.createdAt > best.createdAt) && (await r.hasPowerup(BuiltInPowerupCodes.PDFHighlight))) best = r;
  return best;
}

/** Which book a PDF is, from its name: author surname + title words (e.g. "David Lay, Linear Algebra…" → Lay 5e). */
export function guessSourceForPdf(pdfName: string, sources: Source[]): Source | undefined {
  const have = new Set(words(pdfName));
  let best: { src: Source; score: number } | undefined;
  for (const src of sources) {
    const title = src.title.split(" — ")[1] ?? src.title;
    const author = words(src.short)[0];
    if (!author || !have.has(author)) continue;
    const score = 2 + words(title).filter((w) => have.has(w)).length;
    if (!best || score > best.score) best = { src, score };
  }
  return best?.src;
}
