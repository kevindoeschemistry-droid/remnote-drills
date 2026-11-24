// Writes the question bank for the `content` branch (CI runs this after a green build of main):
//   <out>/manifest.json      { contract, hash, built, version, coded }   small: fetched on every start
//   <out>/bank-<hash>.json   { hash, graph, lo, path }                    large: fetched once per new hash
// The previous bank file is kept, so a plugin that read the old manifest a moment ago can still fetch it.
// usage: node scripts/publish-content.mjs <out-dir> [previous-dir]
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { describe, FILES } from "./content-meta.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const [out, prev] = process.argv.slice(2);
if (!out) throw new Error("usage: publish-content.mjs <out-dir> [previous-dir]");
fs.mkdirSync(out, { recursive: true });

const texts = FILES.map((f) => fs.readFileSync(path.join(root, "src/drills", f), "utf8"));
const { hash, coded } = describe(texts);
const [graph, lo, pathJson] = texts.map((t) => JSON.parse(t));
const contract = JSON.parse(fs.readFileSync(path.join(root, "src/drills/content-contract.json"), "utf8")).contract;
const version = JSON.parse(fs.readFileSync(path.join(root, "package.json"), "utf8")).version;

fs.writeFileSync(path.join(out, `bank-${hash}.json`), JSON.stringify({ hash, graph, lo, path: pathJson }));
if (prev) {
  try {
    const old = JSON.parse(fs.readFileSync(path.join(prev, "manifest.json"), "utf8"));
    const f = `bank-${old.hash}.json`;
    if (old.hash !== hash && fs.existsSync(path.join(prev, f))) fs.copyFileSync(path.join(prev, f), path.join(out, f));
  } catch {
    /* first publish */
  }
}
const manifest = { contract, hash, built: new Date().toISOString(), version, coded };
fs.writeFileSync(path.join(out, "manifest.json"), JSON.stringify(manifest, null, 1));
fs.writeFileSync(
  path.join(out, "README.md"),
  "Question bank for the KevinDoesChemistry Library RemNote plugin, written by CI from a green build of main.\nDo not edit by hand: see scripts/publish-content.mjs and src/drills/content.ts.\n",
);
console.log(`published question bank ${hash} (contract ${contract}, plugin ${version}, ${coded.length} coded templates)`);
