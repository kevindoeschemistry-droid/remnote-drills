// drills/frameworks/<id>.yaml  ->  docs/frameworks/<id>.md  (the readable map + coverage per LO)
// Checks: unique ids, practices / big ideas exist, every drill names a real template, and
// which of a course's skills the framework never mentions.
//   node scripts/framework.mjs [heat-transfer]
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import yaml from "js-yaml";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const id = process.argv[2] ?? "heat-transfer";
const fw = yaml.load(fs.readFileSync(path.join(root, "drills/frameworks", `${id}.yaml`), "utf8"));
const graph = JSON.parse(fs.readFileSync(path.join(root, "src/drills/skills.generated.json"), "utf8"));

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
  process.exit(1);
}

// templates of the subject's skills that no LO uses (drills without a home in the map)
const used = new Set(rows.flatMap((r) => [...r.full, ...r.partial]));
const domain = fw.code.toLowerCase();
const orphanTpl = Object.entries(tplSkill).filter(([t, s]) => s.startsWith(`${domain}.`) && !used.has(t)).map(([t]) => t);

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
      md += `- ${mark[r.status]} **${r.code}** ${r.lo.do}\n`;
      for (const e of r.lo.ek ?? []) md += `  - EK: ${e}\n`;
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
