// drills/frameworks/<id>.yaml + the drill generators  ->  docs/worksheets/<id>/unit-NN.html
//
// One printable worksheet per unit: a problem for every drilled learning objective, then a
// step-by-step answer key on its own pages. The problems come from the same generators the
// RemNote cards use, so a worksheet is just a fixed set of seeds.
//
//   npx tsx scripts/worksheets.ts [framework=heat-transfer] [--seed 1] [--per 1]
//
// Same framework + seed + per  ->  the same worksheet, every time.
import fs from "fs";
import path from "path";
import yaml from "js-yaml";
import katex from "katex";
import { TEMPLATES, generateTemplate } from "../src/drills/registry";
import type { Problem } from "../src/drills/types";

const args = process.argv.slice(2);
const flag = (name: string, fallback: number) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? Number(args[i + 1]) : fallback;
};
const id = args.find((a, i) => !a.startsWith("--") && !args[i - 1]?.startsWith("--")) ?? "heat-transfer";
const SEED = flag("seed", 1);
const PER = flag("per", 1);

const root = path.resolve(__dirname, "..");
const fw = yaml.load(fs.readFileSync(path.join(root, "drills/frameworks", `${id}.yaml`), "utf8")) as any;
const outDir = path.join(root, "docs/worksheets", id);
fs.mkdirSync(outDir, { recursive: true });

const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

/** text with $...$ inline math -> HTML */
function rich(text: string): string {
  return String(text)
    .split(/(\$[^$]+\$)/g)
    .map((chunk) =>
      chunk.startsWith("$") && chunk.endsWith("$") && chunk.length > 2
        ? katex.renderToString(chunk.slice(1, -1), { throwOnError: false })
        : esc(chunk).replace(/\n/g, "<br>"),
    )
    .join("");
}

const unitOf = (p: { answer: any }) => (p.answer?.kind === "expression" && p.answer.unit ? ` ${esc(p.answer.unit)}` : "");

interface Item { n: number; code: string; lo: string; p: Problem }

function problemHtml(it: Item): string {
  const { p } = it;
  const parts = p.parts?.length
    ? `<ol class="parts">${p.parts
        .map((q) =>
          q.answer.kind === "choice"
            ? `<li>${rich(q.ask)}<ul class="choices">${q.answer.options.map((o) => `<li>${rich(o)}</li>`).join("")}</ul></li>`
            : `<li>${rich(q.ask)} <span class="blank"></span>${unitOf(q)}</li>`,
        )
        .join("")}</ol>`
    : p.answer.kind === "choice"
      ? `<ul class="choices">${p.answer.options.map((o) => `<li>${rich(o)}</li>`).join("")}</ul>`
      : `<p class="single">Answer: <span class="blank wide"></span>${unitOf(p)}</p>`;
  return `<section class="problem">
  <h3><span class="num">${it.n}</span><span class="lo">${it.code}</span></h3>
  <p class="prompt">${rich(p.prompt)}</p>
  ${p.figure ? `<div class="figure">${p.figure}</div>` : ""}
  ${parts}
  <div class="work"></div>
</section>`;
}

function keyHtml(it: Item): string {
  const { p } = it;
  const body = p.parts?.length
    ? `<ol class="parts">${p.parts
        .map((q) => `<li>${rich(q.ask)}: <b>${rich(`$${q.answerTex}$`)}${unitOf(q)}</b>${q.explain ? `<div class="why">${rich(q.explain)}</div>` : ""}</li>`)
        .join("")}</ol>`
    : `<ol class="steps">${p.steps.map((s) => `<li>${rich(s)}</li>`).join("")}</ol>
       <p class="final">Answer: <b>${rich(`$${p.answerTex}$`)}${unitOf(p)}</b></p>`;
  return `<section class="key">
  <h3><span class="num">${it.n}</span><span class="lo">${it.code}</span> <span class="lotext">${esc(it.lo)}</span></h3>
  ${body}
</section>`;
}

const CSS = `
:root { --ink: #1c1c1c; --muted: #666; --rule: #c9c9c9; --accent: #2f5496; }
* { box-sizing: border-box; }
body { font: 11pt/1.45 "Calibri", "Carlito", "Segoe UI", system-ui, sans-serif; color: var(--ink); margin: 0; background: #f3f3f3; }
main { max-width: 8.5in; margin: 0 auto; padding: 0.6in 0.75in; background: #fff; }
header.sheet { border-bottom: 2px solid var(--accent); padding-bottom: 6px; margin-bottom: 14px; }
header.sheet .course { color: var(--accent); font-weight: 700; letter-spacing: 0.02em; }
header.sheet h1 { font-size: 18pt; margin: 2px 0 6px; }
header.sheet .meta { display: flex; gap: 24px; color: var(--muted); font-size: 10pt; }
header.sheet .fill { flex: 1; border-bottom: 1px solid var(--ink); min-width: 1.5in; }
.ideas { color: var(--muted); font-size: 10pt; margin: 0 0 14px; }
h2 { font-size: 12pt; color: var(--accent); border-bottom: 1px solid var(--rule); padding-bottom: 2px; margin: 22px 0 10px; }
.problem, .key { break-inside: avoid; margin: 0 0 16px; }
h3 { font-size: 11pt; margin: 0 0 4px; display: flex; align-items: baseline; gap: 8px; }
.num { display: inline-block; min-width: 1.6em; font-weight: 700; }
.num::after { content: "."; }
.lo { font: 8.5pt ui-monospace, Consolas, monospace; color: var(--muted); border: 1px solid var(--rule); border-radius: 3px; padding: 0 4px; }
.lotext { font-weight: 400; color: var(--muted); font-size: 9.5pt; }
.prompt { margin: 0 0 6px 1.9em; }
.parts, .steps { margin: 0 0 0 1.9em; padding-left: 1.4em; }
.parts { list-style: lower-alpha; }
.parts li, .steps li { margin: 3px 0; }
.single, .final { margin: 6px 0 0 1.9em; }
.choices { list-style: none; margin: 4px 0 0 1.9em; padding: 0; }
.choices li::before { content: "\\25CB"; margin-right: 8px; }
.parts .choices { margin-left: 0; }
.blank { display: inline-block; width: 1.3in; border-bottom: 1px solid var(--ink); margin: 0 4px; }
.blank.wide { width: 3in; }
.work { height: 1.5in; }
.figure { margin: 4px 0 6px 1.9em; }
.figure svg { max-width: 3.4in; height: auto; }
.why { color: #333; font-size: 10pt; margin: 2px 0 6px; }
.keypage { break-before: page; }
footer { color: var(--muted); font-size: 8.5pt; border-top: 1px solid var(--rule); margin-top: 24px; padding-top: 6px; }
.index a { color: var(--accent); }
.index td { padding: 3px 14px 3px 0; vertical-align: top; }
@media print { body { background: #fff; } main { padding: 0; max-width: none; } @page { margin: 0.7in 0.75in; } }
`;

const page = (title: string, body: string) => `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>${esc(title)}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@${katex.version}/dist/katex.min.css">
<style>${CSS}</style></head><body><main>
${body}
</main></body></html>
`;

const sheetHeader = (unit: any, kind: string) => `<header class="sheet">
  <div class="course">${esc(fw.title)} · Unit ${unit.n}</div>
  <h1>${esc(unit.title)}${kind ? ` — ${kind}` : ""}</h1>
  ${kind ? "" : `<div class="meta"><span>Name</span><span class="fill"></span><span>Date</span><span class="fill"></span></div>`}
</header>`;

const index: { n: number; title: string; file: string; problems: number; skipped: string[] }[] = [];
let total = 0;

for (const unit of fw.units) {
  const groups: { topic: any; items: Item[] }[] = [];
  const skipped: string[] = [];
  let n = 0;
  for (const topic of unit.topics) {
    const items: Item[] = [];
    for (const lo of topic.los) {
      const code = `${fw.code}-${unit.n}.${topic.n}.${lo.id}`;
      // "~name" marks a drill that only partly covers the objective; worksheets use full matches only
      const names: string[] = (lo.drills ?? []).filter((d: string) => !d.startsWith("~") && TEMPLATES[d]);
      if (!names.length) {
        skipped.push(code);
        continue;
      }
      for (let k = 0; k < PER; k++) {
        const name = names[(SEED + k) % names.length];
        // a distinct, stable seed per (objective, copy)
        const seed = SEED * 1000 + unit.n * 97 + topic.n * 13 + lo.id.charCodeAt(0) + k * 7919;
        items.push({ n: ++n, code, lo: lo.do, p: generateTemplate("worksheet", name, seed) });
      }
    }
    if (items.length) groups.push({ topic, items });
  }
  if (!n) continue;
  const ideas = (unit.big_ideas ?? unit.ideas ?? []).join(", ");
  const body = [
    sheetHeader(unit, ""),
    ideas ? `<p class="ideas">Big ideas: ${esc(ideas)}</p>` : "",
    ...groups.map((g) => `<h2>${unit.n}.${g.topic.n} ${esc(g.topic.title)}</h2>\n${g.items.map(problemHtml).join("\n")}`),
    `<div class="keypage">`,
    sheetHeader(unit, "Answer key"),
    ...groups.map((g) => `<h2>${unit.n}.${g.topic.n} ${esc(g.topic.title)}</h2>\n${g.items.map(keyHtml).join("\n")}`),
    `</div>`,
    `<footer>${esc(fw.title)} · Unit ${unit.n} · seed ${SEED} · generated by scripts/worksheets.ts from the drill generators${
      skipped.length ? ` · no full drill yet: ${skipped.join(", ")}` : ""
    }</footer>`,
  ].join("\n");
  const file = `unit-${String(unit.n).padStart(2, "0")}.html`;
  fs.writeFileSync(path.join(outDir, file), page(`${fw.title} · Unit ${unit.n} · ${unit.title}`, body));
  index.push({ n: unit.n, title: unit.title, file, problems: n, skipped });
  total += n;
}

fs.writeFileSync(
  path.join(outDir, "index.html"),
  page(
    `${fw.title} worksheets`,
    `<header class="sheet"><div class="course">${esc(fw.title)}</div><h1>Worksheets</h1></header>
<p class="ideas">One worksheet per unit, a problem for every drilled learning objective, with a step-by-step answer key. Print from the browser; the key starts on a new page.</p>
<table class="index">${index
      .map(
        (u) =>
          `<tr><td>Unit ${u.n}</td><td><a href="${u.file}">${esc(u.title)}</a></td><td>${u.problems} problems</td><td>${
            u.skipped.length ? `not yet covered: ${u.skipped.join(", ")}` : ""
          }</td></tr>`,
      )
      .join("")}</table>
<footer>seed ${SEED} · ${PER} per objective · generated by scripts/worksheets.ts</footer>`,
  ),
);
console.log(`docs/worksheets/${id}: ${index.length} worksheets, ${total} problems (seed ${SEED}, ${PER} per objective)`);
