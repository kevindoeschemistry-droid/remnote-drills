// drills/frameworks/*.yaml + docs/frameworks/{path.json,<id>.json}  ->  docs/path/index.html
// One self-contained page: every objective in path order, start to finish.
// Run `node scripts/framework.mjs` first.
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import yaml from "js-yaml";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const P = JSON.parse(fs.readFileSync(path.join(root, "docs/frameworks/path.json"), "utf8"));
const order = new Map(P.objectives.map((c, i) => [c, i + 1]));
const fws = [];
for (const id of P.frameworks) {
  const f = yaml.load(fs.readFileSync(path.join(root, "drills/frameworks", `${id}.yaml`), "utf8"));
  const status = Object.fromEntries(JSON.parse(fs.readFileSync(path.join(root, "docs/frameworks", `${id}.json`), "utf8")).rows.map((r) => [r.code, r.status]));
  const units = f.units.map((u) => ({
    n: u.n, title: u.title, scope: u.scope,
    topics: u.topics.map((t) => ({
      n: t.n, title: t.title,
      los: t.los.map((lo) => {
        const code = `${f.code}-${u.n}.${t.n}.${lo.id}`;
        return [code, order.get(code), lo.do, (lo.ek ?? []).join(" "), [].concat(lo.std ?? []).join(", "), (lo.needs ?? []).join(" "), { ok: 2, partial: 1, gap: 0 }[status[code]] ?? 0];
      }),
    })),
  }));
  fws.push({ id, title: f.title, code: f.code, track: f.track ?? "other", requires: f.requires ?? [], units });
}
const data = JSON.stringify(fws).replace(/</g, "\\u003c");
const html = fs.readFileSync(path.join(root, "scripts/path-page.html"), "utf8").replace("/*DATA*/[]", data);
fs.mkdirSync(path.join(root, "docs/path"), { recursive: true });
fs.writeFileSync(path.join(root, "docs/path/index.html"), html);
console.log(`docs/path/index.html: ${P.objectives.length} objectives, ${(html.length / 1024).toFixed(0)} KB`);
