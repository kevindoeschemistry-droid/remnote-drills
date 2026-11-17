// One framework unit -> an HTML file that Google Drive converts into an editable Google Doc.
//
//   npx tsx scripts/gdoc.ts heat-transfer 1 [--seed 1]      -> tests/out/gdoc/<id>-unit-NN.html (+ .regions.json)
//   python3 scripts/gdoc_math.py tests/out/gdoc/<id>-unit-NN.html   (renders the fractions to images)
//
// Layout follows Kevin's own worksheets: Name / Date / course line, an italic unit line, a boxed
// method callout, Roman-numeral sections, numbered problems, then the key on a new page.
//
// Every generated problem starts with a small grey marker, e.g. ⟦HT-1.1.B·s1⟧. The marker is how
// scripts/gdoc-pull.ts finds the region again after the Doc has been edited. Text outside the
// markers (headings, the callout, instructions) is never touched by a regeneration.
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

// overrides pulled back from the Doc: drills/worksheets/<id>-unit-NN.yaml  { "<marker>": "replacement prompt text" }
const slug = `${id}-unit-${String(unitN).padStart(2, "0")}`;
const overridesFile = path.join(root, "drills/worksheets", `${slug}.yaml`);
const overrides: Record<string, string> = fs.existsSync(overridesFile) ? ((yaml.load(fs.readFileSync(overridesFile, "utf8")) as any) ?? {}) : {};

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
/** text with $...$ -> inline HTML */
const rich = (text: string) =>
  String(text)
    .split(/(\$[^$]+\$)/g)
    .map((c) => (c.startsWith("$") && c.endsWith("$") && c.length > 2 ? math(c.slice(1, -1)) : esc(c)))
    .join("");

const unitOf = (p: { answer: any }) => (p.answer?.kind === "expression" && p.answer.unit ? ` ${esc(p.answer.unit)}` : "");

// ── content ─────────────────────────────────────────────────────────────────
const ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"];
const F = `font-family:Calibri,Arial,sans-serif;font-size:11pt;`;
const mark = (m: string) => `<span style="color:#999999;font-size:8pt;">⟦${m}⟧</span>`;
const BLANK = `<p style="${F}margin:0;">&nbsp;</p>`;

/** what a piece of inline HTML reads as once Google hands the Doc back as text */
const plain = (h: string) =>
  h.replace(/<img[^>]*>/g, "[image]").replace(/<[^>]+>/g, "").replace(/&nbsp;/g, " ").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&").replace(/\s+/g, " ").trim();
interface Segment { kind: "text" | "math"; src: string; plain: string }
/** the prompt cut into text and $math$ pieces, each with its plain reading, so gdoc-pull.ts can tell which piece an edit touched */
const segments = (text: string): Segment[] =>
  String(text)
    .split(/(\$[^$]+\$)/g)
    .filter((c) => c !== "")
    .map((c) => (c.startsWith("$") && c.endsWith("$") && c.length > 2 ? { kind: "math" as const, src: c, plain: plain(math(c.slice(1, -1))) } : { kind: "text" as const, src: c, plain: c.replace(/\s+/g, " ") }));
interface Region { marker: string; code: string; template: string; seed: number; prompt: string; overridden: boolean; segments: Segment[] }
const regions: Region[] = [];
const sheet: string[] = [];
const key: string[] = [];
let n = 0;
let section = 0;

for (const topic of unit.topics) {
  const items: { code: string; marker: string; p: Problem; prompt: string }[] = [];
  for (const lo of topic.los) {
    const code = `${fw.code}-${unit.n}.${topic.n}.${lo.id}`;
    const names: string[] = (lo.drills ?? []).filter((d: string) => !d.startsWith("~") && TEMPLATES[d]);
    if (!names.length) continue;
    const name = names[SEED % names.length];
    const seed = SEED * 1000 + unit.n * 97 + topic.n * 13 + lo.id.charCodeAt(0);
    const p = generateTemplate("worksheet", name, seed);
    const marker = `${code}·s${SEED}`;
    const prompt = overrides[marker] ?? p.prompt;
    const before = images;
    regions.push({ marker, code, template: name, seed, prompt, overridden: marker in overrides, segments: segments(prompt) });
    images = before; // segments() renders the math a second time; don't count it twice
    items.push({ code, marker, p, prompt });
  }
  if (!items.length) continue;
  const head = `<p style="${F}margin:14pt 0 4pt 0;"><b>${ROMAN[section++]}. ${esc(topic.title)}</b></p>`;
  sheet.push(head);
  key.push(head);
  for (const it of items) {
    n++;
    const { p } = it;
    const asks = p.parts?.length
      ? p.parts
          .map((q, k) => `<p style="${F}margin:2pt 0 2pt 36pt;">${String.fromCharCode(97 + k)}. ${rich(q.ask)}  ____________${unitOf(q)}</p>`)
          .join("")
      : p.answer.kind === "choice"
        ? p.answer.options.map((o, k) => `<p style="${F}margin:2pt 0 2pt 36pt;">${String.fromCharCode(97 + k)}. ${rich(o)}</p>`).join("")
        : "";
    sheet.push(`<p style="${F}margin:8pt 0 2pt 18pt;">${n}.  ${mark(it.marker)} ${rich(it.prompt)}</p>${asks}${BLANK.repeat(p.parts?.length ? 5 : 6)}`);
    const worked = p.parts?.length
      ? p.parts
          .map(
            (q, k) =>
              `<p style="${F}margin:2pt 0 2pt 36pt;">${String.fromCharCode(97 + k)}. ${rich(q.ask)}: <b>${math(q.answerTex)}</b></p>` +
              (q.explain ? `<p style="${F}margin:0 0 4pt 54pt;">${rich(q.explain)}</p>` : ""),
          )
          .join("")
      : p.steps.map((s) => `<p style="${F}margin:2pt 0 2pt 36pt;">${rich(s)}</p>`).join("") +
        `<p style="${F}margin:4pt 0 2pt 36pt;"><b>${math(p.answerTex)}</b></p>`;
    key.push(`<p style="${F}margin:8pt 0 2pt 18pt;">${n}.  ${mark(`${it.marker}·key`)}</p>${worked}`);
  }
}

// "incropera-8e": ["1.1", "1.2"] across the unit's topics -> "Incropera 8e §1.1–1.3"
const bySource: Record<string, string[]> = {};
for (const t of unit.topics) for (const [b, secs] of Object.entries(t.book ?? {})) (bySource[b] ??= []).push(...[].concat(secs as any).map(String));
const sourceName = (slug: string) => {
  const f = path.join(root, "drills/sources", `${slug}.yaml`);
  const src = fs.existsSync(f) ? (yaml.load(fs.readFileSync(f, "utf8")) as any) : null;
  return src?.short ?? slug.replace(/-/g, " ").replace(/^\w/, (c) => c.toUpperCase());
};
const books = Object.entries(bySource).map(([b, secs]) => `${sourceName(b)} §${secs.length > 1 ? `${secs[0]}–${secs[secs.length - 1]}` : secs[0]}`);
const practices: any[] = fw.practices ?? [];
const header = (suffix: string) => `
<p style="${F}margin:0;">Name: ______________________________&nbsp;&nbsp;Date: ________________&nbsp;&nbsp;&nbsp;&nbsp;<b>${esc(String(fw.title).toUpperCase())}</b></p>
<p style="${F}margin:6pt 0 8pt 0;"><i>Unit ${unit.n} – ${esc(unit.title)}${suffix}${books.length ? ` (${esc(books.join("; "))})` : ""}</i></p>`;
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

const outDir = path.join(root, "tests/out/gdoc");
fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, `${slug}.html`), html);
fs.writeFileSync(path.join(outDir, `${slug}.regions.json`), JSON.stringify({ framework: id, unit: unitN, seed: SEED, overridesFile: path.relative(root, overridesFile), regions }, null, 1) + "\n");
console.log(`tests/out/gdoc/${slug}.html: ${n} problems, ${images} formulas need images, ${Object.keys(overrides).length} overrides applied`);
