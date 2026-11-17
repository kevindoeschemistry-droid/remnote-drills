// Writes the other half of the wiki links: each wiki page a source points at gets a
// `remnote:` line in its frontmatter listing the RemNote skills drilled from it.
//
//   node scripts/wiki-backlinks.mjs --wiki <path to the wiki repo>            write
//   node scripts/wiki-backlinks.mjs --wiki <path to the wiki repo> --check    report only; exit 1 if anything is out of date
//
// A section page lists that section's skills. A chapter page lists every skill taught in the
// chapter. Only frontmatter changes; page bodies are left alone (the wiki's drill pages allow no
// links back in the body). Run it again after `wiki:` links or section skills change.
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import yaml from "js-yaml";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);
const wikiDir = args.includes("--wiki") ? args[args.indexOf("--wiki") + 1] : null;
const CHECK = args.includes("--check");
if (!wikiDir || !fs.existsSync(path.join(wikiDir, "content"))) {
  console.error("usage: node scripts/wiki-backlinks.mjs --wiki <path to the wiki repo> [--check]");
  process.exit(1);
}

// wiki page -> skills, in the order the book teaches them
const want = new Map();
const add = (page, skills) => {
  if (!page || !skills.length) return;
  const have = want.get(page) ?? [];
  for (const s of skills) if (!have.includes(s)) have.push(s);
  want.set(page, have);
};
for (const f of fs.readdirSync(path.join(root, "drills/sources")).filter((f) => f.endsWith(".yaml")).sort()) {
  const s = yaml.load(fs.readFileSync(path.join(root, "drills/sources", f), "utf8"));
  for (const ch of s.chapters ?? []) {
    const all = [];
    for (const sec of ch.sections ?? []) {
      all.push(...(sec.skills ?? []));
      add(sec.wiki, sec.skills ?? []);
    }
    add(ch.wiki, [...(ch.skills ?? []), ...all]);
  }
}

let changed = 0;
let missing = 0;
for (const [page, skills] of want) {
  const file = [path.join(wikiDir, "content", `${page}.md`), path.join(wikiDir, "content", page, "index.md")].find((p) => fs.existsSync(p));
  if (!file) {
    console.error(`no such wiki page: ${page}`);
    missing++;
    continue;
  }
  const text = fs.readFileSync(file, "utf8");
  const m = /^---\r?\n([\s\S]*?)\r?\n---/.exec(text);
  if (!m) {
    console.error(`no frontmatter: ${page}`);
    missing++;
    continue;
  }
  const line = `remnote: [${skills.join(", ")}]`;
  const lines = m[1].split(/\r?\n/).filter((l) => !/^remnote:/.test(l));
  lines.push(line);
  const next = `---\n${lines.join("\n")}\n---` + text.slice(m[0].length);
  if (next === text) continue;
  changed++;
  if (CHECK) console.log(`out of date: ${page}`);
  else fs.writeFileSync(file, next);
}
console.log(`${want.size} wiki pages carry RemNote skills; ${changed} ${CHECK ? "out of date" : "updated"}, ${missing} missing`);
if (missing || (CHECK && changed)) process.exit(1);
