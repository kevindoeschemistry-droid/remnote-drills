// drills/frameworks/<id>.yaml  ->  docs/frameworks/<id>.md  (the readable map + coverage per LO)
// Checks: unique ids, practices / big ideas exist, every drill names a real template, every
// `needs` prerequisite names a real LO in any framework, and which templates of the
// framework's `domains` no LO uses yet.
//   node scripts/framework.mjs            all frameworks, plus the start-to-finish path
//   node scripts/framework.mjs <id>       one
//
// The path (docs/frameworks/PATH.md, path.json): frameworks in `requires` order (a framework
// comes after every framework it requires), units by n, LOs in file order. Like Khan, it starts
// at the first foundation objective and every later objective's prerequisites come before it;
// a `needs` that points forward along the path is reported as an order error.
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import yaml from "js-yaml";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const fwDir = path.join(root, "drills/frameworks");
const all = Object.fromEntries(
  fs.readdirSync(fwDir).filter((f) => f.endsWith(".yaml")).map((f) => [f.replace(/\.yaml$/, ""), yaml.load(fs.readFileSync(path.join(fwDir, f), "utf8"))])
);
// every LO code in every framework, for cross-framework prerequisites
const allCodes = new Set();
for (const f of Object.values(all)) for (const u of f.units ?? []) for (const t of u.topics ?? []) for (const lo of t.los ?? []) allCodes.add(`${f.code}-${u.n}.${t.n}.${lo.id}`);
const graph = JSON.parse(fs.readFileSync(path.join(root, "src/drills/skills.generated.json"), "utf8"));
let failed = false;
for (const id of process.argv[2] ? [process.argv[2]] : Object.keys(all)) {
const fw = all[id];
if (!fw) { console.error(`no framework ${id}`); process.exit(1); }

// template -> skill, for every live template
const tplSkill = {};
for (const s of graph.skills) for (const ts of Object.values(s.levels ?? {})) for (const t of ts) tplSkill[t] = s.id;

const errors = [];
const practices = new Set(fw.practices.map((p) => p.id));
const ideas = new Set(fw.big_ideas.map((b) => b.id));
const seen = new Set();
const rows = []; // one per LO
for (const u of fw.units) {
  for (const b of u.ideas ?? []) if (!ideas.has(b)) errors.push(`unit ${u.n}: unknown big idea ${b}`);
  for (const t of u.topics) {
    for (const lo of t.los) {
      const code = `${fw.code}-${u.n}.${t.n}.${lo.id}`;
      if (seen.has(code)) errors.push(`duplicate ${code}`);
      seen.add(code);
      for (const p of lo.p ?? []) if (!practices.has(p)) errors.push(`${code}: unknown practice ${p}`);
      for (const n of lo.needs ?? []) if (!allCodes.has(n)) errors.push(`${code}: needs unknown LO ${n}`);
      const full = [], partial = [];
      for (const d of lo.drills ?? []) {
        const name = d.replace(/^~/, "");
        if (!tplSkill[name]) errors.push(`${code}: no template ${name}`);
        (d.startsWith("~") ? partial : full).push(name);
      }
      const status = full.length ? "ok" : partial.length ? "partial" : "gap";
      rows.push({ code, unit: u, topic: t, lo, full, partial, status });
    }
  }
}
if (errors.length) {
  console.error(`${id} framework is invalid:\n  ` + errors.join("\n  "));
  failed = true;
  continue;
}

// templates of the subject's skills that no LO uses (drills without a home in the map)
const used = new Set(rows.flatMap((r) => [...r.full, ...r.partial]));
const domains = fw.domains ?? [fw.code.toLowerCase()];
const orphanTpl = Object.entries(tplSkill).filter(([t, s]) => domains.some((d) => s.startsWith(`${d}.`)) && !used.has(t)).map(([t]) => t);

// ── markdown ──────────────────────────────────────────────────────────────
const count = (rs, st) => rs.filter((r) => r.status === st).length;
const mark = { ok: "●", partial: "◐", gap: "○" };
const core = rows.filter((r) => r.unit.scope === "core");
let md = `# ${fw.title} — curriculum framework (draft ${fw.draft})\n\n`;
md += `Generated from \`drills/frameworks/${id}.yaml\` by \`scripts/framework.mjs\`. ● drilled · ◐ partly · ○ no drills yet.\n\n`;
md += `**${rows.length} learning objectives** in ${fw.units.length} units (${core.length} core): `;
md += `${count(rows, "ok")} drilled, ${count(rows, "partial")} partly, ${count(rows, "gap")} with no drills. `;
md += `Core: ${count(core, "ok")} / ${core.length} drilled.\n\n`;
md += `## Big ideas\n\n` + fw.big_ideas.map((b) => `- **${b.id} · ${b.title}.** ${b.text}`).join("\n") + "\n\n";
md += `## Practices\n\n` + fw.practices.map((p) => `- **${p.id} · ${p.title}.** ${p.text}`).join("\n") + "\n\n";
md += `## Units at a glance\n\n| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |\n|---|---|---|---|---|---|---|\n`;
for (const u of fw.units) {
  const r = rows.filter((x) => x.unit === u);
  md += `| ${u.n} · ${u.title} | ${u.scope} | ${u.weight_est ?? "—"} | ${r.length} | ${count(r, "ok")} | ${count(r, "partial")} | ${count(r, "gap")} |\n`;
}
for (const u of fw.units) {
  md += `\n## Unit ${u.n} · ${u.title}${u.scope === "extension" ? " (extension)" : ""}\n\nBig ideas: ${u.ideas.join(", ")}\n`;
  for (const t of u.topics) {
    const book = Object.entries(t.book ?? {}).map(([b, s]) => `${b} §${s.join(", §")}`).join("; ");
    md += `\n### ${u.n}.${t.n} ${t.title}\n\n${book ? `Book: ${book}` : ""}${t.fe?.length ? ` · FE: ${t.fe.join(", ")}` : ""}\n\n`;
    for (const r of rows.filter((x) => x.topic === t)) {
      md += `- ${mark[r.status]} **${r.code}**${r.lo.std ? ` (${[].concat(r.lo.std).join(", ")})` : ""} ${r.lo.do}\n`;
      for (const e of r.lo.ek ?? []) md += `  - EK: ${e}\n`;
      if (r.lo.needs?.length) md += `  - Needs: ${r.lo.needs.join(", ")}\n`;
      md += `  - ${r.lo.p.join(" · ")}${r.full.length || r.partial.length ? ` · drills: ${[...r.full, ...r.partial.map((x) => `~${x}`)].join(", ")}` : ""}\n`;
    }
  }
}
if (orphanTpl.length) md += `\n## Drills not yet placed on the map\n\n${orphanTpl.map((t) => `- ${t} (${tplSkill[t]})`).join("\n")}\n`;

const outDir = path.join(root, "docs/frameworks");
fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, `${id}.md`), md);
fs.writeFileSync(
  path.join(outDir, `${id}.json`),
  JSON.stringify({ ...fw, rows: rows.map((r) => ({ code: r.code, unit: r.unit.n, topic: r.topic.n, status: r.status, full: r.full, partial: r.partial })), orphanTpl }, null, 1)
);
console.log(`${fw.title}: ${rows.length} LOs (${core.length} core) — ${count(rows, "ok")} drilled, ${count(rows, "partial")} partly, ${count(rows, "gap")} gaps; ${orphanTpl.length} unplaced templates -> docs/frameworks/${id}.md`);
}

// ── the start-to-finish path ─────────────────────────────────────────────────
if (!process.argv[2] && !failed) {
  const ids = Object.keys(all);
  const missing = [];
  for (const id of ids) for (const r of all[id].requires ?? []) if (!all[r]) missing.push(`${id} requires ${r}, which isn't written yet`);
  // Kahn's algorithm; ties broken by track order, then the order frameworks were listed in TRACKS
  const TRACKS = ["math", "science", "computing", "engineering", "health", "safety", "communication", "athletics"];
  const rank = (id) => [TRACKS.indexOf(all[id].track ?? "zz") === -1 ? 99 : TRACKS.indexOf(all[id].track), all[id].level ?? 0, id];
  const cmp = (a, b) => { const x = rank(a), y = rank(b); return x[0] - y[0] || x[1] - y[1] || String(x[2]).localeCompare(String(y[2])); };
  const indeg = Object.fromEntries(ids.map((id) => [id, (all[id].requires ?? []).filter((r) => all[r]).length]));
  const order = [];
  let ready = ids.filter((id) => indeg[id] === 0).sort(cmp);
  while (ready.length) {
    const id = ready.shift();
    order.push(id);
    for (const j of ids) if ((all[j].requires ?? []).includes(id) && --indeg[j] === 0) ready = [...ready, j].sort(cmp);
  }
  const cyclic = ids.filter((id) => !order.includes(id));
  const pos = new Map();
  const seq = [];
  let pulled = 0;
  for (const id of order) {
    // file order, except that an objective's prerequisites inside the same framework are pulled
    // in just ahead of it (stable topological sort, earliest file position first)
    const mine = [];
    for (const u of all[id].units) for (const t of u.topics) for (const lo of t.los)
      mine.push({ code: `${all[id].code}-${u.n}.${t.n}.${lo.id}`, fw: id, unit: u.n, scope: u.scope, needs: lo.needs ?? [] });
    const idx = new Map(mine.map((x, i) => [x.code, i]));
    const local = (x) => x.needs.filter((n) => idx.has(n));
    const left = new Map(mine.map((x) => [x.code, local(x).length]));
    const users = new Map(mine.map((x) => [x.code, []]));
    for (const x of mine) for (const n of local(x)) users.get(n).push(x);
    const ready = mine.filter((x) => left.get(x.code) === 0);
    const out = [];
    while (ready.length) {
      ready.sort((a, b) => idx.get(a.code) - idx.get(b.code));
      const x = ready.shift();
      out.push(x);
      for (const y of users.get(x.code)) if (left.set(y.code, left.get(y.code) - 1).get(y.code) === 0) ready.push(y);
    }
    for (const x of mine) if (!out.includes(x)) out.push(x); // a cycle: keep file order for the rest
    out.forEach((x, i) => { if (i < idx.get(x.code)) pulled++; });
    for (const x of out) { pos.set(x.code, seq.length); seq.push(x); }
  }
  const forward = seq.filter((x) => x.needs.some((n) => pos.has(n) && pos.get(n) > pos.get(x.code))).map((x) => `${x.code} needs ${x.needs.filter((n) => pos.get(n) > pos.get(x.code)).join(", ")}, which comes later`);
  let md = `# The path — start to finish\n\nEvery framework in \`requires\` order; inside each, units and objectives in order, except that ${pulled} objectives move up to sit just after the prerequisites they need. ${seq.length} objectives in ${order.length} frameworks.\n\n`;
  md += `| # | Framework | Track | Requires | LOs | Path position |\n|---|---|---|---|---|---|\n`;
  order.forEach((id, i) => {
    const mine = seq.filter((x) => x.fw === id);
    md += `| ${i + 1} | ${all[id].title} | ${all[id].track ?? "—"} | ${(all[id].requires ?? []).join(", ") || "—"} | ${mine.length} | ${pos.get(mine[0].code) + 1}–${pos.get(mine[mine.length - 1].code) + 1} |\n`;
  });
  if (missing.length) md += `\n## Not written yet\n\n${missing.map((m) => `- ${m}`).join("\n")}\n`;
  if (cyclic.length) md += `\n## Cycle in requires\n\n${cyclic.join(", ")}\n`;
  if (forward.length) md += `\n## Order problems (a prerequisite comes after the objective)\n\n${forward.map((m) => `- ${m}`).join("\n")}\n`;
  fs.writeFileSync(path.join(root, "docs/frameworks/PATH.md"), md);
  fs.writeFileSync(path.join(root, "docs/frameworks/path.json"), JSON.stringify({ frameworks: order, objectives: seq.map((x) => x.code) }));

  // for the plugin: the whole library (Library builder, Path tab) and a small LO → drills map (cards)
  const TRACK_TITLES = { math: "Math", science: "Science", computing: "Computing", engineering: "Engineering", health: "Health", safety: "AI Safety", communication: "Communication", athletics: "Athletics" };
  const tplSkill = {};
  for (const s of graph.skills) for (const ts of Object.values(s.levels ?? {})) for (const t of ts) tplSkill[t] = s.id;
  const lib = {
    tracks: TRACK_TITLES,
    frameworks: order.map((id) => {
      const f = all[id];
      return {
        id, title: f.title, code: f.code, track: f.track ?? "other", requires: f.requires ?? [],
        units: f.units.map((u) => ({
          n: u.n, title: u.title, scope: u.scope ?? "core",
          topics: u.topics.map((t) => ({
            n: t.n, title: t.title,
            los: t.los.map((lo) => {
              const code = `${f.code}-${u.n}.${t.n}.${lo.id}`;
              return { code, pos: pos.get(code) + 1, do: lo.do, ek: (lo.ek ?? []).join(" "), std: [].concat(lo.std ?? []).join(", "), needs: lo.needs ?? [], drills: (lo.drills ?? []).filter((d) => !d.startsWith("~")) };
            }),
          })),
        })),
      };
    }),
  };
  const loDrills = {};
  for (const f of lib.frameworks) for (const u of f.units) for (const t of u.topics) for (const lo of t.los)
    if (lo.drills.length) loDrills[lo.code] = { t: lo.do, f: f.title, d: lo.drills, s: tplSkill[lo.drills[0]] };
  fs.writeFileSync(path.join(root, "src/drills/path.generated.json"), JSON.stringify(lib));
  fs.writeFileSync(path.join(root, "src/drills/lo-drills.generated.json"), JSON.stringify(loDrills));
  console.log(`path: ${seq.length} objectives in ${order.length} frameworks; ${pulled} moved ahead to sit after their prerequisites; ${missing.length} missing requires, ${cyclic.length} in cycles, ${forward.length} order problems -> docs/frameworks/PATH.md`);
}
if (failed) process.exit(1);
