// Every drill target (skills and objectives) can be written out as a card: front and back are
// RemNote rich text, LaTeX segments are balanced, and no raw $ is left in plain text.
import { LIVE_SKILLS } from "../src/drills/skills";
import { LO_DRILLS, resolveTarget } from "../src/drills/target";
import { generateFor } from "../src/drills/registry";
import { backOf, frontOf } from "../src/drills/static-card";
import katex from "katex";
let n = 0, bad = 0;
const targets = [...LIVE_SKILLS.map((s) => s.id), ...Object.keys(LO_DRILLS).map((c) => `lo:${c}`)];
for (const name of targets) for (let s = 1; s <= 4; s++) {
  const t = resolveTarget(name)!;
  const p = generateFor(t, s * 7919);
  for (const rt of [frontOf(p, "Drill"), backOf(p)]) {
    n++;
    for (const el of rt as any[]) {
      if (typeof el === "string") { if (el.includes("$")) { bad++; if (bad < 6) console.log("raw $ in", name, JSON.stringify(el).slice(0, 120)); } }
      else if (el.i === "x") { try { katex.renderToString(el.text, { throwOnError: true }); } catch (e) { bad++; if (bad < 6) console.log("bad latex", name, el.text.slice(0, 80)); } }
    }
  }
}
console.log(`${targets.length} drill targets, ${n} card faces, ${bad} problems`);
process.exit(bad ? 1 : 0);
