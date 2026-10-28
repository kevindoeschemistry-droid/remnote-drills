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
// drills/live/*.yaml: per-area overlays that switch planned skills live ({ id: { short, kind, levels, … } })
const liveDir = path.join(root, "live");
if (fs.existsSync(liveDir))
  for (const f of fs.readdirSync(liveDir).filter((f) => f.endsWith(".yaml")).sort())
    for (const [id, patch] of Object.entries(load(path.join(liveDir, f)) ?? {})) {
      const sk = g.skills.find((s) => s.id === id);
      if (!sk) errors.push(`live/${f}: unknown skill ${id}`);
      else Object.assign(sk, { status: "live" }, patch);
    }
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
    for (const v of [...(ch.videos ?? []), ...ch.sections.flatMap((s) => s.videos ?? [])])
      if (typeof v?.title !== "string" || !/^https:\/\//.test(v?.url ?? "")) errors.push(`${src.id} ch ${ch.n}: a video needs a title and an https url`);
    for (const sk of [...ch.skills, ...ch.sections.flatMap((s) => s.skills)])
      if (!ids.has(sk)) errors.push(`${src.id} ch ${ch.n}: unknown skill ${sk}`);
  }
}

// ── method notes ──────────────────────────────────────────────────────────
const methodsFile = path.join(root, "methods.yaml");
const methods = fs.existsSync(methodsFile) ? load(methodsFile) ?? {} : {};
// drills/methods/*.yaml: per-area method notes
const methodsDir = path.join(root, "methods");
if (fs.existsSync(methodsDir))
  for (const f of fs.readdirSync(methodsDir).filter((f) => f.endsWith(".yaml")).sort())
    for (const [id, lines] of Object.entries(load(path.join(methodsDir, f)) ?? {})) {
      if (methods[id]) errors.push(`methods/${f}: ${id} already has method notes`);
      methods[id] = lines;
    }
for (const [id, lines] of Object.entries(methods)) {
  const sk = g.skills.find((s) => s.id === id);
  if (!sk) errors.push(`methods.yaml: unknown skill ${id}`);
  else if (!Array.isArray(lines) || lines.some((l) => typeof l !== "string")) errors.push(`methods.yaml: ${id} must be a list of strings`);
  else sk.method = lines;
}

// ── courses ───────────────────────────────────────────────────────────────
const coursesFile = path.join(root, "courses.yaml");
const courses = fs.existsSync(coursesFile) ? load(coursesFile).courses ?? [] : [];
// drills/courses/*.yaml: full courses (units → lessons → skills, milestones); replace the stub with the same id
const coursesDir = path.join(root, "courses");
if (fs.existsSync(coursesDir))
  for (const f of fs.readdirSync(coursesDir).filter((f) => f.endsWith(".yaml")).sort()) {
    const c = load(path.join(coursesDir, f));
    const i = courses.findIndex((x) => x.id === c.id);
    if (i >= 0) courses[i] = c;
    else courses.push(c);
  }
for (const c of courses) {
  for (const s of c.sources ?? []) if (!sourceIds.has(s)) errors.push(`course ${c.id}: unknown source ${s}`);
  const unitIds = new Set();
  for (const u of c.units ?? []) {
    if (unitIds.has(u.id)) errors.push(`course ${c.id}: duplicate unit ${u.id}`);
    unitIds.add(u.id);
    for (const l of u.lessons ?? []) {
      l.skills ??= [];
      for (const sk of l.skills) if (!ids.has(sk)) errors.push(`course ${c.id} › ${u.id} › ${l.ref}: unknown skill ${sk}`);
    }
  }
  for (const m of c.milestones ?? []) {
    m.date = String(m.date instanceof Date ? m.date.toISOString().slice(0, 10) : m.date);
    for (const u of m.units ?? []) if (!unitIds.has(u)) errors.push(`course ${c.id}: milestone ${m.name} names unknown unit ${u}`);
  }
}

// ── problems as data: drills/problems/*.yaml ─────────────────────────────
// Each entry is a template (givens, derived values, prompt, checked parts, verify block).
// It joins its skill's levels by itself, so writing the file is all it takes to go live.
const problems = [];
const problemsDir = path.join(root, "problems");
const tplNames = new Set();
if (fs.existsSync(problemsDir))
  for (const f of fs.readdirSync(problemsDir).filter((f) => f.endsWith(".yaml")).sort())
    for (const t of load(path.join(problemsDir, f)) ?? []) {
      const where = `problems/${f} › ${t.template ?? "?"}`;
      if (!t.template) errors.push(`${where}: needs a template name`);
      if (tplNames.has(t.template)) errors.push(`${where}: duplicate template`);
      tplNames.add(t.template);
      const sk = g.skills.find((s) => s.id === t.skill);
      if (!sk) { errors.push(`${where}: unknown skill ${t.skill}`); continue; }
      if (!t.prompt) errors.push(`${where}: needs a prompt`);
      if (!Array.isArray(t.parts) || !t.parts.length) errors.push(`${where}: needs at least one part`);
      for (const p of t.parts ?? []) {
        if (!p.ask || !p.label) errors.push(`${where}: every part needs ask and label`);
        if (p.value === undefined && !p.choice) errors.push(`${where} › ${p.label}: needs value (a number) or choice`);
      }
      // an answer nobody checked independently doesn't ship
      const v = t.verify ?? {};
      if (!v.ode && !v.residuals && !v.truth) errors.push(`${where}: needs a verify block (ode, residuals or truth)`);
      for (const p of t.parts ?? [])
        if (p.value !== undefined && !(v.expect ?? {})[p.label] && !new RegExp(`\\b${p.label}\\b`).test(JSON.stringify([v.ode, v.bcs, v.residuals])))
          errors.push(`${where} › ${p.label}: verify must check this part (verify.expect.${p.label}, or use it in ode / bcs / residuals)`);
      for (const k of Object.keys(t.given ?? {})) if (!/^[A-Za-z][A-Za-z0-9_]*$/.test(k)) errors.push(`${where}: bad given name ${k}`);
      const lvl = Number(t.level ?? 1);
      sk.levels[lvl] = [...(sk.levels[lvl] ?? []).filter((x) => x !== t.template), t.template];
      sk.status = "live";
      problems.push(t);
    }

// ── library (where PDFs are filed) ────────────────────────────────────────
const libraryFile = path.join(root, "library.yaml");
const library = fs.existsSync(libraryFile) ? load(libraryFile) : { subjects: [], books: {}, extras: [] };
for (const [sid, subj] of Object.entries(library.books ?? {})) {
  if (!sourceIds.has(sid)) errors.push(`library.yaml: unknown source ${sid}`);
  if (!(library.subjects ?? []).includes(subj)) errors.push(`library.yaml: ${sid} files under unknown subject ${subj}`);
}
for (const d of g.domains) if (!library.domains?.[d.id]) errors.push(`library.yaml: domain ${d.id} has no subject`);
for (const [d, subj] of Object.entries(library.domains ?? {})) {
  if (!domains.has(d)) errors.push(`library.yaml: unknown domain ${d}`);
  if (!(library.subjects ?? []).includes(subj)) errors.push(`library.yaml: domain ${d} files under unknown subject ${subj}`);
}
for (const x of library.extras ?? []) if (!(library.subjects ?? []).includes(x.subject)) errors.push(`library.yaml: ${x.name} files under unknown subject ${x.subject}`);

if (errors.length) {
  console.error("drills/ is invalid:\n  " + errors.join("\n  "));
  process.exit(1);
}
fs.writeFileSync(out, JSON.stringify({ ...g, sources, courses, library, problems }, null, 1) + "\n");
const live = g.skills.filter((s) => s.status === "live").length;
console.log(`skills: ${g.skills.length} (${live} live), sources: ${sources.length}, courses: ${courses.length} -> ${path.relative(process.cwd(), out)}`);
