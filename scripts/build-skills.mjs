// drills/skills.yaml + drills/sources/*.yaml + drills/courses.yaml
//   ->  src/drills/skills.generated.json   (runs before dev / build / test)
// Fails loudly on a broken graph: unknown domain / prereq / skill reference,
// duplicate id or alias, a live skill without templates.
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import yaml from "js-yaml";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../drills");
const out = path.resolve(here, "../src/drills/skills.generated.json");
const load = (f) => yaml.load(fs.readFileSync(f, "utf8"));

const g = load(path.join(root, "skills.yaml"));
const errors = [];
const domains = new Set(g.domains.map((d) => d.id));
const ids = new Set();
const names = new Set();
for (const s of g.skills) {
  for (const n of [s.id, ...(s.aliases ?? [])]) {
    if (names.has(n)) errors.push(`duplicate id/alias: ${n}`);
    names.add(n);
  }
  ids.add(s.id);
  if (!domains.has(s.domain)) errors.push(`${s.id}: unknown domain ${s.domain}`);
  s.kind ??= "solve";
  s.status ??= "planned";
  s.short ??= s.title;
  s.prereqs ??= [];
  s.aliases ??= [];
  s.levels = Object.fromEntries(Object.entries(s.levels ?? {}).map(([k, v]) => [Number(k), v]));
  if (s.status === "live" && !Object.values(s.levels).flat().length) errors.push(`${s.id}: live but no templates`);
}
for (const s of g.skills) {
  for (const p of s.prereqs) if (!ids.has(p)) errors.push(`${s.id}: unknown prereq ${p}`);
  for (const p of s.pool ?? []) if (!ids.has(p)) errors.push(`${s.id}: unknown pool skill ${p}`);
}

// ── sources ───────────────────────────────────────────────────────────────
const sources = fs
  .readdirSync(path.join(root, "sources"))
  .filter((f) => f.endsWith(".yaml"))
  .sort()
  .map((f) => load(path.join(root, "sources", f)));
const sourceIds = new Set();
for (const src of sources) {
  if (sourceIds.has(src.id)) errors.push(`duplicate source ${src.id}`);
  sourceIds.add(src.id);
  src.chapters ??= [];
  for (const ch of src.chapters) {
    ch.skills ??= [];
    ch.sections ??= [];
    for (const sec of ch.sections) sec.skills ??= [];
    for (const sk of [...ch.skills, ...ch.sections.flatMap((s) => s.skills)])
      if (!ids.has(sk)) errors.push(`${src.id} ch ${ch.n}: unknown skill ${sk}`);
  }
}

// ── method notes ──────────────────────────────────────────────────────────
const methodsFile = path.join(root, "methods.yaml");
const methods = fs.existsSync(methodsFile) ? load(methodsFile) ?? {} : {};
for (const [id, lines] of Object.entries(methods)) {
  const sk = g.skills.find((s) => s.id === id);
  if (!sk) errors.push(`methods.yaml: unknown skill ${id}`);
  else if (!Array.isArray(lines) || lines.some((l) => typeof l !== "string")) errors.push(`methods.yaml: ${id} must be a list of strings`);
  else sk.method = lines;
}

// ── courses ───────────────────────────────────────────────────────────────
const coursesFile = path.join(root, "courses.yaml");
const courses = fs.existsSync(coursesFile) ? load(coursesFile).courses ?? [] : [];
for (const c of courses) for (const s of c.sources ?? []) if (!sourceIds.has(s)) errors.push(`course ${c.id}: unknown source ${s}`);

// ── library (where PDFs are filed) ────────────────────────────────────────
const libraryFile = path.join(root, "library.yaml");
const library = fs.existsSync(libraryFile) ? load(libraryFile) : { subjects: [], books: {}, extras: [] };
for (const [sid, subj] of Object.entries(library.books ?? {})) {
  if (!sourceIds.has(sid)) errors.push(`library.yaml: unknown source ${sid}`);
  if (!(library.subjects ?? []).includes(subj)) errors.push(`library.yaml: ${sid} files under unknown subject ${subj}`);
}
for (const x of library.extras ?? []) if (!(library.subjects ?? []).includes(x.subject)) errors.push(`library.yaml: ${x.name} files under unknown subject ${x.subject}`);

if (errors.length) {
  console.error("drills/ is invalid:\n  " + errors.join("\n  "));
  process.exit(1);
}
fs.writeFileSync(out, JSON.stringify({ ...g, sources, courses, library }, null, 1) + "\n");
const live = g.skills.filter((s) => s.status === "live").length;
console.log(`skills: ${g.skills.length} (${live} live), sources: ${sources.length}, courses: ${courses.length} -> ${path.relative(process.cwd(), out)}`);
