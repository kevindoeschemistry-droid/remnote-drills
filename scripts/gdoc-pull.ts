// Pull edits made in the Google Doc back into the repo.
//
//   npx tsx scripts/gdoc-pull.ts tests/out/gdoc/heat-transfer-unit-01.regions.json <doc-text-file> [--write]
//
// <doc-text-file> is the Doc read back as text (Drive's Markdown reading). A ⟦marker⟧ opens a
// region that runs to the next marker or heading; problems and answer-key entries each have one.
// Every line in a region is compared with what scripts/gdoc.ts wrote:
//
//   same       nothing to do
//   wording    the new wording is saved, keeping every $math$ piece exactly as the repo has it
//   note       a line you added: saved as a note after the line above it, and put back there on
//              the next gdoc.ts run
//   math       a number or symbol changed. Reported, never saved: the Doc can't hand math back
//              reliably, so that change belongs in the generator
//   removed    a generated line (or an earlier note) is gone from the Doc. Reported; a removed
//              note is dropped from the file with --write, a removed generated line is not
//   missing    the marker itself is gone. Reported
//
// Saved edits go to drills/worksheets/<slug>.yaml. Without --write it only reports.
import fs from "fs";
import path from "path";
import yaml from "js-yaml";

const [regionsFile, docFile] = process.argv.slice(2).filter((a) => !a.startsWith("--"));
const WRITE = process.argv.includes("--write");
const root = path.resolve(__dirname, "..");
const meta = JSON.parse(fs.readFileSync(regionsFile, "utf8"));

/** Drive's Markdown reading -> the same plain text gdoc.ts predicts */
const norm = (s: string) =>
  s
    .replace(/\\([\\`*_{}\[\]()#+\-.!|<>~])/g, "$1") // Markdown escapes
    .replace(/\*+/g, "") // emphasis markers
    .replace(/[   ]/g, " ")
    .replace(/\s+/g, " ")
    .trim();

interface Segment { kind: "text" | "math"; src: string; plain: string }
interface Line { id: string; src: string; note?: boolean; segments: Segment[] }
const plainOf = (l: Line) => norm(l.segments.map((s) => s.plain).join(""));

// ── cut the Doc into regions ────────────────────────────────────────────────
const structure = new Set<string>((meta.structure as string[]).map(norm));
const isBoundary = (t: string) => structure.has(t) || /^Name: _+/.test(t);
const docRegions: Record<string, string[]> = {};
let open: string[] | null = null;
for (const raw of fs.readFileSync(docFile, "utf8").split("\n")) {
  const m = /⟦([^⟧]+)⟧(.*)$/.exec(raw);
  if (m) {
    open = docRegions[m[1]] = [];
    const first = norm(m[2]);
    open.push(first); // may be "", the key's marker stands alone
    continue;
  }
  const t = norm(raw);
  if (!t) continue;
  if (isBoundary(t)) open = null;
  else open?.push(t);
}

// ── compare ─────────────────────────────────────────────────────────────────
const words = (s: string) => new Set(s.toLowerCase().split(/[^\p{L}\p{N}.]+/u).filter(Boolean));
const similar = (a: string, b: string) => {
  const [x, y] = [words(a), words(b)];
  let both = 0;
  for (const w of x) if (y.has(w)) both++;
  return both / Math.max(1, x.size + y.size - both);
};

/** new wording for a line, with its math pieces carried over from the repo; null if a math piece was changed */
function rebuild(line: Line, got: string): { src: string } | { broken: string } {
  let cursor = 0;
  let src = "";
  for (const seg of line.segments) {
    if (seg.kind !== "math") continue;
    const m = norm(seg.plain);
    const at = got.indexOf(m, cursor);
    if (at < 0) return { broken: seg.src };
    src += got.slice(cursor, at) + seg.src;
    cursor = at + m.length;
  }
  return { src: src + got.slice(cursor) };
}

const overridesPath = path.join(root, meta.overridesFile);
type Override = { lines?: Record<string, string>; notes?: { after: string; text: string }[] };
const before: Record<string, Override> = fs.existsSync(overridesPath) ? ((yaml.load(fs.readFileSync(overridesPath, "utf8")) as any) ?? {}) : {};
const after: Record<string, Override> = {};
const count = { same: 0, wording: 0, note: 0, math: 0, removed: 0, missing: 0 };
const say = (kind: keyof typeof count, where: string, text: string) => {
  count[kind]++;
  if (kind !== "same") console.log(`${kind.padEnd(8)} ${where}: ${text}`);
};

for (const r of meta.regions as { marker: string; template: string; lines: Line[] }[]) {
  const doc = docRegions[r.marker];
  if (!doc) {
    say("missing", r.marker, "the marker is not in the Doc any more");
    if (before[r.marker]) after[r.marker] = before[r.marker]; // keep what was saved; nothing new can be learned
    continue;
  }
  const lines = r.lines.filter((l, k) => !(k === 0 && plainOf(l) === "")); // the key's empty first line
  const D = doc.filter((t, k) => !(k === 0 && t === ""));
  const o: Override = { lines: { ...(before[r.marker]?.lines ?? {}) }, notes: [] };

  // 1. exact matches, in order, anchor everything else
  const matchOfLine = new Array<number>(lines.length).fill(-1);
  const takenD = new Array<boolean>(D.length).fill(false);
  let from = 0;
  lines.forEach((l, i) => {
    const at = D.indexOf(plainOf(l), from);
    if (at >= 0) {
      matchOfLine[i] = at;
      takenD[at] = true;
      from = at + 1;
    }
  });
  // 2. between anchors, pair a leftover Doc line with a leftover generated line when they read alike
  const edited = new Map<number, number>(); // line index -> Doc index
  for (let d = 0; d < D.length; d++) {
    if (takenD[d]) continue;
    const prev = Math.max(-1, ...matchOfLine.map((at, i) => (at >= 0 && at < d ? i : -1)), ...[...edited].filter(([, at]) => at < d).map(([i]) => i));
    const nextIdx = matchOfLine.findIndex((at, i) => i > prev && at > d);
    const end = nextIdx < 0 ? lines.length : nextIdx;
    let best = -1;
    let bestScore = 0.35;
    for (let i = prev + 1; i < end; i++) {
      if (matchOfLine[i] >= 0 || edited.has(i)) continue;
      const s = similar(plainOf(lines[i]), D[d]);
      if (s > bestScore) [best, bestScore] = [i, s];
    }
    if (best >= 0) {
      edited.set(best, d);
      takenD[d] = true;
    }
  }
  // 3. report each generated line and earlier note
  const keptNotes: Record<string, string> = {}; // old note id -> its current text
  lines.forEach((l, i) => {
    const where = `${r.marker} ${l.note ? "note" : `line ${l.id}`}`;
    if (matchOfLine[i] >= 0) {
      say("same", where, "");
      if (l.note) keptNotes[l.id] = l.src;
    } else if (edited.has(i)) {
      const got = D[edited.get(i)!];
      const res = rebuild(l, got);
      if ("broken" in res) {
        say("math", where, `${res.broken} no longer appears as written. Change numbers and math in the generator (${r.template}), not in the Doc.\n         Doc now reads: ${got}`);
        if (l.note) keptNotes[l.id] = l.src;
      } else {
        say("wording", where, `\n   repo: ${norm(l.src)}\n   doc:  ${res.src}`);
        if (l.note) keptNotes[l.id] = res.src;
        else o.lines![l.id] = res.src;
      }
    } else say("removed", where, `"${plainOf(l).slice(0, 80)}" is not in the Doc`);
  });
  // 4. rebuild the notes list: earlier notes that survive keep their anchor, leftover Doc lines become new notes
  const prior = before[r.marker]?.notes ?? [];
  prior.forEach((nt, k) => keptNotes[`n${k}`] !== undefined && o.notes!.push({ after: nt.after, text: keptNotes[`n${k}`] }));
  for (let d = 0; d < D.length; d++) {
    if (takenD[d]) continue;
    // attach to the last generated line that sits above it in the Doc
    let anchor = lines.find((l) => !l.note)?.id ?? "g0";
    lines.forEach((l, i) => {
      const at = matchOfLine[i] >= 0 ? matchOfLine[i] : (edited.get(i) ?? -1);
      if (!l.note && at >= 0 && at < d) anchor = l.id;
    });
    o.notes!.push({ after: anchor, text: D[d] });
    say("note", r.marker, `"${D[d]}" added after line ${anchor}`);
  }
  if (!Object.keys(o.lines!).length) delete o.lines;
  if (!o.notes!.length) delete o.notes;
  if (o.lines || o.notes) after[r.marker] = o;
}

const changed = JSON.stringify(after) !== JSON.stringify(before);
if (WRITE && changed) {
  fs.mkdirSync(path.dirname(overridesPath), { recursive: true });
  const head =
    `# Edits pulled back from the Google Doc by scripts/gdoc-pull.ts, one entry per marker.\n` +
    `# lines: wording that replaces a generated line.  notes: lines you added, put back after the line named.\n` +
    `# scripts/gdoc.ts applies these. Delete an entry to go back to what the generator writes.\n`;
  if (Object.keys(after).length) fs.writeFileSync(overridesPath, head + yaml.dump(after, { lineWidth: 220 }));
  else if (fs.existsSync(overridesPath)) fs.unlinkSync(overridesPath);
  console.log(`\nsaved to ${meta.overridesFile}`);
} else if (changed) console.log(`\nnot saved; run again with --write`);
console.log(
  `${count.same} lines unchanged, ${count.wording} reworded, ${count.note} added, ${count.math} math edits, ${count.removed} removed, ${count.missing} markers missing`,
);
