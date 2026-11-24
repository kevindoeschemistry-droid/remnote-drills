// The online question bank (src/drills/content.ts): a published bank that is newer and compatible must
// reach every reader module; an incompatible one, or no network, must leave the compiled bank in place.
// Runs loadContent against a fake fetch; the readers are imported only afterwards, as the entry gates do.
import assert from "assert";
import fs from "fs";
import { applyBank, CONTENT_BASE, CONTENT_CONTRACT, contentStatus, loadContent, refuseReason } from "../src/drills/content";
import meta from "../src/drills/content-meta.generated.json";

const offline = process.argv.includes("--offline");
const graph = JSON.parse(fs.readFileSync("src/drills/skills.generated.json", "utf8"));
const lo = JSON.parse(fs.readFileSync("src/drills/lo-drills.generated.json", "utf8"));
const path = JSON.parse(fs.readFileSync("src/drills/path.generated.json", "utf8"));

// a remote bank with one data template the compiled bank lacks, added to an existing skill
const base = graph.problems.find((p: any) => !p.cases && p.parts?.length === 1 && p.given);
const skill = graph.skills.find((s: any) => Object.values(s.levels ?? {}).some((ts: any) => ts.includes(base.template)));
const NEW = "zz-online-only";
graph.problems.push({ ...base, template: NEW });
for (const ts of Object.values(skill.levels) as string[][]) if (ts.includes(base.template)) ts.push(NEW);
const HASH = "feedfacecafebeef";
const bankText = JSON.stringify({ hash: HASH, graph, lo, path });
const manifest = { contract: CONTENT_CONTRACT, hash: HASH, built: "2026-11-24T00:00:00Z", version: "test", coded: (meta as any).coded };

// pure checks
assert.equal(refuseReason(manifest), undefined);
assert.match(refuseReason({ ...manifest, contract: CONTENT_CONTRACT + 1 })!, /contract/);
assert.match(refuseReason({ ...manifest, coded: [...manifest.coded, "zz-not-compiled"] })!, /generator/);

const served: Record<string, string> = { [`${CONTENT_BASE}/manifest.json`]: JSON.stringify(manifest), [`${CONTENT_BASE}/bank-${HASH}.json`]: bankText };
(globalThis as any).fetch = async (url: string) => {
  if (offline) throw new Error("offline");
  const body = served[url];
  return { ok: !!body, status: body ? 200 : 404, text: async () => body ?? "" };
};

(async () => {
  const s = await loadContent();
  const { DATA } = await import("../src/drills/gen-data");
  const { generateTemplate } = await import("../src/drills/registry");
  const has = DATA.some((t) => t.template === NEW);
  if (offline) {
    assert.equal(s.source, "bundled");
    assert.ok(!has, "offline must keep the compiled bank");
    console.log(`content offline: compiled bank kept (${s.note})`);
  } else {
    assert.equal(s.source, "online");
    assert.equal(contentStatus().hash, HASH);
    assert.ok(has, "the online bank's new template must reach gen-data");
    const p = generateTemplate(skill.id, NEW, 7);
    assert.ok(p.prompt && p.answer, "the online-only template must generate");
    assert.throws(() => applyBank({ graph, lo, path }, s), /already read/);
    console.log(`content online: bank ${s.hash} used; ${NEW} generates under ${skill.id}`);
  }
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
