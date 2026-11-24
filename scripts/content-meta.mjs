// Describes the question bank compiled into this build (runs at the end of `npm run skills`):
//   src/drills/content-meta.generated.json  { hash, coded }
// hash   sha-256 over the three generated JSON files, so a published bank can be compared with the bundled one
// coded  template names the bank uses that no data template supplies: they must come from compiled generators,
//        so a published bank that needs a coded name this build lacks is refused (the plugin must be updated)
import fs from "fs";
import path from "path";
import crypto from "crypto";
import { fileURLToPath } from "url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const gen = (f) => path.join(root, "src/drills", f);
export const FILES = ["skills.generated.json", "lo-drills.generated.json", "path.generated.json"];

export function describe(texts) {
  const hash = crypto.createHash("sha256");
  for (const t of texts) hash.update(t).update("\0");
  const [graph, lo] = texts.map((t) => JSON.parse(t));
  const data = new Set((graph.problems ?? []).map((p) => p.template));
  const used = new Set();
  for (const s of graph.skills ?? []) for (const ts of Object.values(s.levels ?? {})) for (const t of ts) used.add(t);
  for (const d of Object.values(lo ?? {})) for (const t of d.d ?? []) used.add(t);
  const coded = [...used].filter((t) => !data.has(t)).sort();
  return { hash: hash.digest("hex").slice(0, 16), coded };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const texts = FILES.map((f) => fs.readFileSync(gen(f), "utf8"));
  const meta = describe(texts);
  fs.writeFileSync(gen("content-meta.generated.json"), JSON.stringify(meta));
  console.log(`question bank ${meta.hash}: ${meta.coded.length} coded templates in use`);
}
