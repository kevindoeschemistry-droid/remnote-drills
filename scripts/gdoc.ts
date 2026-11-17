// One framework unit -> an HTML file that Google Drive converts into an editable Google Doc.
//
//   npx tsx scripts/gdoc.ts heat-transfer 1 [--seed 1]      -> tests/out/gdoc/<id>-unit-NN.html (+ .regions.json)
//   python3 scripts/gdoc_math.py tests/out/gdoc/<id>-unit-NN.html   (renders the fractions to images)
//
// Layout follows Kevin's own worksheets: Name / Date / course line, an italic unit line, a boxed
// method callout, Roman-numeral sections, numbered problems, then the key on a new page.
//
// Every problem, and every key entry, starts with a small grey marker, e.g. ⟦HT-1.1.B·s1⟧ and
// ⟦HT-1.1.B·s1·key⟧. A marker opens a region that runs to the next marker or heading. That is how
// scripts/gdoc-pull.ts finds each line again after the Doc has been edited, and where it files a
// line you added.
//
// Math: anything that is just symbols, subscripts, superscripts and units becomes real Doc text
// (editable). Anything with a fraction or other 2-D layout becomes an image whose alt text is the
// LaTeX; that math is changed in the repo, not in the Doc.
import fs from "fs";
import path from "path";
import yaml from "js-yaml";
import { TEMPLATES, generateTemplate } from "../src/drills/registry";
import type { Problem } from "../src/drills/types";

const args = process.argv.slice(2);
const flag = (name: string, fallback: number) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? Number(args[i + 1]) : fallback;
};
const pos = args.filter((a, i) => !a.startsWith("--") && !args[i - 1]?.startsWith("--"));
const id = pos[0] ?? "heat-transfer";
const unitN = Number(pos[1] ?? 1);
const SEED = flag("seed", 1);

const root = path.resolve(__dirname, "..");
const fw = yaml.load(fs.readFileSync(path.join(root, "drills/frameworks", `${id}.yaml`), "utf8")) as any;
const unit = fw.units.find((u: any) => u.n === unitN);
if (!unit) throw new Error(`${id} has no unit ${unitN}`);

// edits pulled back from the Doc: drills/worksheets/<id>-unit-NN.yaml
//   "<marker>": { lines: { "<line id>": "replacement text, $math$ kept" }, notes: [{ after: "<line id>", text: "…" }] }
const slug = `${id}-unit-${String(unitN).padStart(2, "0")}`;
const overridesFile = path.join(root, "drills/worksheets", `${slug}.yaml`);
interface Override { lines?: Record<string, string>; notes?: { after: string; text: string }[] }
const overrides: Record<string, Override> = fs.existsSync(overridesFile) ? ((yaml.load(fs.readFileSync(overridesFile, "utf8")) as any) ?? {}) : {};

const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

// ── TeX -> Doc text ─────────────────────────────────────────────────────────
class TwoD extends Error {}
const SYM: Record<string, string> = {
  cdot: "·", times: "×", pi: "π", varepsilon: "ε", epsilon: "ε", sigma: "σ", rho: "ρ", alpha: "α", beta: "β", gamma: "γ",
  delta: "δ", Delta: "Δ", theta: "θ", mu: "μ", nu: "ν", tau: "τ", lambda: "λ", zeta: "ζ", eta: "η", phi: "φ", omega: "ω",
  Omega: "Ω", infty: "∞", le: "≤", leq: "≤", ge: "≥", geq: "≥", approx: "≈", neq: "≠", pm: "±", to: "→", rightarrow: "→",
  circ: "°", degree: "°", ln: "ln ", exp: "exp", sin: "sin ", cos: "cos ", tan: "tan ", log: "log ", quad: "  ", ll: "≪", gg: "≫",
  propto: "∝", partial: "∂", nabla: "∇", ell: "ℓ", prime: "′",
};
const ACCENT: Record<string, string> = { dot: "̇", bar: "̄", hat: "̂", overline: "̄", vec: "⃗", ddot: "̈" };

/** Convert TeX that needs no 2-D layout into inline HTML; throws TwoD otherwise. */
function texToHtml(tex: string): string {
  let i = 0;
  const group = (): string => {
    // one argument: {…} or a single token
    while (tex[i] === " ") i++;
    if (tex[i] === "{") {
      let depth = 0;
      const start = i + 1;
      for (; i < tex.length; i++) {
        if (tex[i] === "{") depth++;
        else if (tex[i] === "}" && --depth === 0) break;
      }
      const inner = tex.slice(start, i);
      i++;
      return inner;
    }
    if (tex[i] === "\\") {
      const m = /^\\([A-Za-z]+|.)/.exec(tex.slice(i))!;
      i += m[0].length;
      return m[0];
    }
    return tex[i++];
  };
  const run = (upright: boolean): string => {
    let out = "";
    while (i < tex.length) {
      const ch = tex[i];
      if (ch === "\\") {
        const m = /^\\([A-Za-z]+|.)/.exec(tex.slice(i))!;
        i += m[0].length;
        const name = m[1];
        if (name === "," || name === ";" || name === ":" || name === " ") out += " ";
        else if (name === "!") out += "";
        else if (name === "mathrm" || name === "text" || name === "mathit" || name === "textbf" || name === "mathbf") out += sub(group(), name !== "mathit");
        else if (name === "left" || name === "right" || name === "displaystyle" || name === "big" || name === "Big") out += "";
        else if (ACCENT[name]) out += sub(group(), upright) + ACCENT[name];
        else if (SYM[name] !== undefined) out += SYM[name];
        else if (name === "%" || name === "$" || name === "{" || name === "}" || name === "&" || name === "#" || name === "_") out += esc(name);
        else throw new TwoD(name);
      } else if (ch === "^" || ch === "_") {
        i++;
        const inner = sub(group(), upright);
        out += inner === "°" && ch === "^" ? "°" : ch === "^" ? `<sup>${inner}</sup>` : `<sub>${inner}</sub>`;
      } else if (ch === "{") {
        out += sub(group(), upright);
      } else if (ch === "}" ) {
        i++;
      } else if (ch === "'") {
        out += "′";
        i++;
      } else if (ch === "-") {
        out += "−";
        i++;
      } else if (ch === " ") {
        i++;
      } else if (/[A-Za-z]/.test(ch)) {
        out += upright ? esc(ch) : `<i>${esc(ch)}</i>`;
        i++;
      } else if (ch === "=" || ch === "+" || ch === "<" || ch === ">") {
        out += ` ${esc(ch)} `;
        i++;
      } else {
        out += esc(ch);
        i++;
      }
    }
    return out;
  };
  const sub = (inner: string, upright: boolean): string => {
    const save = [tex, i] as const;
    tex = inner;
    i = 0;
    const r = run(upright);
    [tex, i] = [save[0], save[1]];
    return r;
  };
  return run(false).replace(/<\/i><i>/g, "").replace(/−<\/sup>/g, "−</sup>").replace(/ {2,}/g, " ").replace(/^ (=|\+)/, "$1");
}

let images = 0;
function math(tex: string): string {
  try {
    return texToHtml(tex);
  } catch (e) {
    if (!(e instanceof TwoD)) throw e;
    images++;
    return `<img src="TEX:${Buffer.from(tex, "utf8").toString("base64")}" alt="${esc(tex).replace(/"/g, "&quot;")}">`;
  }
}
/** what a piece of inline HTML reads as once Google hands the Doc back as text */
const plain = (h: string) =>
  h.replace(/<img[^>]*>/g, "[image]").replace(/<[^>]+>/g, "").replace(/&nbsp;/g, " ").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&").replace(/\s+/g, " ").trim();

// A line's source is text with $math$; **$math$** is a bold answer.
const PIECE = /(\*\*\$[^$]+\$\*\*|\$[^$]+\$)/g;
const isMath = (c: string) => /^(\*\*)?\$[^$]+\$(\*\*)?$/.test(c) && c.length > 2;
const lineHtml = (src: string) =>
  String(src)
    .split(PIECE)
    .map((c) => (!isMath(c) ? esc(c) : c.startsWith("**") ? `<b>${math(c.slice(3, -3))}</b>` : math(c.slice(1, -1))))
    .join("");
interface Segment { kind: "text" | "math"; src: string; plain: string }
/** a line cut into text and math pieces, each with its plain reading, so gdoc-pull.ts can tell which piece an edit touched */
const segments = (src: string): Segment[] =>
  String(src)
    .split(PIECE)
    .filter((c) => c !== "")
    .map((c) => (isMath(c) ? { kind: "math" as const, src: c, plain: plain(lineHtml(c)) } : { kind: "text" as const, src: c, plain: c.replace(/\s+/g, " ") }));

const unitOf = (p: { answer: any }) => (p.answer?.kind === "expression" && p.answer.unit ? ` ${p.answer.unit}` : "");

// ── content ─────────────────────────────────────────────────────────────────
const ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"];
const F = `font-family:Calibri,Arial,sans-serif;font-size:11pt;`;
const mark = (m: string) => `<span style="color:#999999;font-size:8pt;">⟦${m}⟧</span>`;
const BLANK = `<p style="${F}margin:0;">&nbsp;</p>`;
const letter = (k: number) => String.fromCharCode(97 + k);

interface Line { id: string; src: string; indent: number; note?: boolean; edited?: boolean; segments?: Segment[] }
interface Region { marker: string; code: string; template: string; seed: number; lines: Line[] }
const regions: Region[] = [];
const structure: string[] = []; // plain text of headings and header lines: a region never runs past one of these

/** apply pulled-back wording and notes to a region's generated lines */
function withEdits(marker: string, generated: { src: string; indent: number }[]): Line[] {
  const o = overrides[marker] ?? {};
  const out: Line[] = [];
  const notesAfter = (id: string, indent: number) =>
    (o.notes ?? []).forEach((n, k) => n.after === id && out.push({ id: `n${k}`, src: n.text, indent, note: true }));
  generated.forEach((g, k) => {
    const id = `g${k}`;
    const src = o.lines?.[id] ?? g.src;
    out.push({ id, src, indent: g.indent, edited: o.lines?.[id] !== undefined });
    notesAfter(id, Math.max(g.indent, 36));
  });
  return out;
}
/** the marker paragraph carries line g0; the rest follow as their own paragraphs */
function regionHtml(n: number, r: Region): string {
  const [first, ...rest] = r.lines;
  return (
    `<p style="${F}margin:8pt 0 2pt 18pt;">${n}.  ${mark(r.marker)}${first.src ? ` ${lineHtml(first.src)}` : ""}</p>` +
    rest.map((l) => `<p style="${F}margin:2pt 0 2pt ${l.indent}pt;">${lineHtml(l.src)}</p>`).join("")
  );
}

const sheet: string[] = [];
const key: string[] = [];
let n = 0;
let section = 0;
let edits = 0;

for (const topic of unit.topics) {
  const items: { p: Problem; q: Region; k: Region }[] = [];
  for (const lo of topic.los) {
    const code = `${fw.code}-${unit.n}.${topic.n}.${lo.id}`;
    const names: string[] = (lo.drills ?? []).filter((d: string) => !d.startsWith("~") && TEMPLATES[d]);
    if (!names.length) continue;
    const name = names[SEED % names.length];
    const seed = SEED * 1000 + unit.n * 97 + topic.n * 13 + lo.id.charCodeAt(0);
    const p = generateTemplate("worksheet", name, seed);
    const marker = `${code}·s${SEED}`;
    // worksheet side: the prompt, then one line per part or choice
    const qLines = [{ src: p.prompt, indent: 18 }];
    if (p.parts?.length) p.parts.forEach((q, k) => qLines.push({ src: `${letter(k)}. ${q.ask}  ____________${unitOf(q)}`, indent: 36 }));
    else if (p.answer.kind === "choice") p.answer.options.forEach((o, k) => qLines.push({ src: `${letter(k)}. ${o}`, indent: 36 }));
    // key side: an empty first line (the marker stands alone), then the worked steps
    const kLines = [{ src: "", indent: 18 }];
    if (p.parts?.length)
      p.parts.forEach((q, k) => {
        kLines.push({ src: `${letter(k)}. ${q.ask}: **$${q.answerTex}$**`, indent: 36 });
        if (q.explain) kLines.push({ src: q.explain, indent: 54 });
      });
    else {
      p.steps.forEach((s) => kLines.push({ src: s, indent: 36 }));
      kLines.push({ src: `**$${p.answerTex}$**`, indent: 36 });
    }
    const q: Region = { marker, code, template: name, seed, lines: withEdits(marker, qLines) };
    const k: Region = { marker: `${marker}·key`, code, template: name, seed, lines: withEdits(`${marker}·key`, kLines) };
    regions.push(q, k);
    items.push({ p, q, k });
  }
  if (!items.length) continue;
  const title = `${ROMAN[section++]}. ${topic.title}`;
  structure.push(title);
  const head = `<p style="${F}margin:14pt 0 4pt 0;"><b>${esc(title)}</b></p>`;
  sheet.push(head);
  key.push(head);
  for (const it of items) {
    n++;
    sheet.push(regionHtml(n, it.q) + BLANK.repeat(it.p.parts?.length ? 5 : 6));
    key.push(regionHtml(n, it.k));
  }
}

// "incropera-8e": ["1.1", "1.2"] across the unit's topics -> "Incropera §1.1–1.3"
const bySource: Record<string, string[]> = {};
for (const t of unit.topics) for (const [b, secs] of Object.entries(t.book ?? {})) (bySource[b] ??= []).push(...[].concat(secs as any).map(String));
const sourceName = (slug: string) => {
  const f = path.join(root, "drills/sources", `${slug}.yaml`);
  const src = fs.existsSync(f) ? (yaml.load(fs.readFileSync(f, "utf8")) as any) : null;
  return src?.short ?? slug.replace(/-/g, " ").replace(/^\w/, (c) => c.toUpperCase());
};
const books = Object.entries(bySource).map(([b, secs]) => `${sourceName(b)} §${secs.length > 1 ? `${secs[0]}–${secs[secs.length - 1]}` : secs[0]}`);
const practices: any[] = fw.practices ?? [];
const header = (suffix: string) => {
  const unitLine = `Unit ${unit.n} – ${unit.title}${suffix}${books.length ? ` (${books.join("; ")})` : ""}`;
  structure.push(unitLine);
  return `
<p style="${F}margin:0;">Name: ______________________________&nbsp;&nbsp;Date: ________________&nbsp;&nbsp;&nbsp;&nbsp;<b>${esc(String(fw.title).toUpperCase())}</b></p>
<p style="${F}margin:6pt 0 8pt 0;"><i>${esc(unitLine)}</i></p>`;
};
const callout = practices.length
  ? `<table style="border-collapse:collapse;margin:6pt auto;width:85%;"><tr><td style="border:1pt solid #000000;padding:6pt 10pt;${F}text-align:center;">
<p style="${F}margin:0 0 3pt 0;"><i>Methodology for ${esc(fw.title)} Problems</i></p>
${practices.slice(0, 5).map((p, k) => `<p style="${F}margin:0;"><i>${k + 1}. ${esc(p.title)}</i></p>`).join("\n")}
</td></tr></table>`
  : "";

const html = `<!doctype html><html><head><meta charset="utf-8"><title>${esc(fw.title)} · Unit ${unit.n} · ${esc(unit.title)}</title></head>
<body style="${F}">
${header("")}
${callout}
${sheet.join("\n")}
<p style="${F}page-break-before:always;margin:0;">&nbsp;</p>
${header(" — Answer Key")}
${key.join("\n")}
</body></html>
`;

// the manifest gdoc-pull.ts compares the Doc against (segments are computed last so their math isn't counted twice)
const shown = images;
for (const r of regions) for (const l of r.lines) { l.segments = segments(l.src); if (l.edited || l.note) edits++; }
images = shown;

const outDir = path.join(root, "tests/out/gdoc");
fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, `${slug}.html`), html);
fs.writeFileSync(
  path.join(outDir, `${slug}.regions.json`),
  JSON.stringify({ framework: id, unit: unitN, seed: SEED, overridesFile: path.relative(root, overridesFile), structure, regions }, null, 1) + "\n",
);
console.log(`tests/out/gdoc/${slug}.html: ${n} problems, ${images} formulas need images, ${edits} pulled-back edits applied`);
