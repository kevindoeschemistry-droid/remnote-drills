// Pull edits made in the Google Doc back into the repo.
//
//   npx tsx scripts/gdoc-pull.ts tests/out/gdoc/heat-transfer-unit-01.regions.json <doc-text-file> [--write]
//
// <doc-text-file> is the Doc read back as text (Drive's Markdown reading). For every ⟦marker⟧ the
// problem paragraph in the Doc is compared with what scripts/gdoc.ts wrote:
//
//   same            nothing to do
//   wording edited  the new wording is saved to drills/worksheets/<slug>.yaml, keeping every $math$
//                   piece exactly as it is in the repo; the next gdoc.ts run uses it
//   math edited     reported, never saved: a number or symbol changed, and the Doc can't hand math
//                   back reliably, so that change belongs in the generator
//   missing         the marker is gone from the Doc; reported
//
// Without --write it only reports.
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

const doc = fs.readFileSync(docFile, "utf8");
const found: Record<string, string> = {};
const re = /⟦([^⟧]+)⟧([^\n]*)/g;
for (let m; (m = re.exec(doc)); ) found[m[1]] = norm(m[2]);

const overridesPath = path.join(root, meta.overridesFile);
const overrides: Record<string, string> = fs.existsSync(overridesPath) ? ((yaml.load(fs.readFileSync(overridesPath, "utf8")) as any) ?? {}) : {};
let changed = 0;
let problems = 0;

for (const r of meta.regions as any[]) {
  const got = found[r.marker];
  if (got === undefined) {
    console.log(`missing    ${r.marker}: the marker is not in the Doc any more`);
    problems++;
    continue;
  }
  const want = norm(r.segments.map((s: any) => s.plain).join(""));
  if (got === want) {
    console.log(`same       ${r.marker}`);
    continue;
  }
  // find every math piece, in order, in the Doc's paragraph; what lies between them is the new wording
  let cursor = 0;
  let rebuilt = "";
  let mathEdited: string | null = null;
  const segs: any[] = r.segments;
  for (let k = 0; k < segs.length; k++) {
    if (segs[k].kind !== "math") continue;
    const m = norm(segs[k].plain);
    const at = got.indexOf(m, cursor);
    if (at < 0) {
      mathEdited = segs[k].src;
      break;
    }
    const between = got.slice(cursor, at);
    // keep the spacing convention of the source: text pieces own the spaces around math
    rebuilt += between + segs[k].src;
    cursor = at + m.length;
  }
  if (mathEdited) {
    console.log(`math       ${r.marker}: ${mathEdited} no longer appears as written. Change numbers and math in the generator (${r.template}), not in the Doc.`);
    console.log(`           Doc now reads: ${got}`);
    problems++;
    continue;
  }
  rebuilt += got.slice(cursor);
  console.log(`wording    ${r.marker}`);
  console.log(`   repo: ${norm(r.prompt)}`);
  console.log(`   doc:  ${rebuilt}`);
  overrides[r.marker] = rebuilt;
  changed++;
}

if (WRITE && changed) {
  fs.mkdirSync(path.dirname(overridesPath), { recursive: true });
  const head = `# Wording pulled back from the Google Doc by scripts/gdoc-pull.ts. One entry per problem marker.\n# scripts/gdoc.ts uses these in place of the generator's prompt. Delete an entry to go back to the generator's wording.\n`;
  fs.writeFileSync(overridesPath, head + yaml.dump(overrides, { lineWidth: 200 }));
  console.log(`\nwrote ${changed} override(s) to ${meta.overridesFile}`);
} else if (changed) console.log(`\n${changed} wording edit(s) found; run again with --write to save them`);
console.log(`${meta.regions.length} regions checked, ${changed} wording edits, ${problems} needing attention`);
