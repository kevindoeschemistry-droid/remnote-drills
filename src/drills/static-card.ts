// Phone-ready drill cards. RemNote's mobile app doesn't run plugins, so a drill card can't be an
// empty shell that the plugin fills in. Instead every drill card carries one real generated
// problem as ordinary card text (front: the problem; back: the answer and the worked solution),
// plus the seed that made it. On the phone you review it like any flashcard; on desktop the
// widget rebuilds the very same problem from the seed and checks your answer.
//
// After you review a card it gets a new problem: right away on desktop (queue event), or at the
// next desktop start for reviews done on the phone (the card's review count went up).
import type { RNPlugin, RichTextInterface } from "@remnote/plugin-sdk";
import { DRILL_POWERUP, DRILL_SLOT } from "./deck";
import { generateFor } from "./registry";
import { resolveTarget, Target } from "./target";
import type { Problem } from "./types";

export const SEED_SLOT = "seed";
const REPS_KEY = "drills.staticReps"; // remId -> review count when its problem was written

export const newSeed = () => (Date.now() ^ Math.floor(Math.random() * 0xffffffff)) >>> 0;

/** "$x^2$ and $$\int$$" -> RemNote rich text with LaTeX elements */
export function richFromMd(text: string): RichTextInterface {
  const out: any[] = [];
  const re = /\$\$([\s\S]+?)\$\$|\$([^$]+?)\$/g;
  let last = 0;
  let m: RegExpExecArray | null;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(text.slice(last, m.index));
    out.push(m[1] !== undefined ? { i: "x", text: m[1].trim(), block: true } : { i: "x", text: m[2].trim() });
    last = re.lastIndex;
  }
  if (last < text.length) out.push(text.slice(last));
  return out;
}

const tex = (t: string): any => ({ i: "x", text: t });
const LETTERS = "ABCDEFGH";

function answerRich(a: Problem["answer"], answerTex: string): any[] {
  if (a.kind === "choice") return [`${a.correct}`];
  return [tex(answerTex)];
}

/** card front: the problem as you'd see it on paper */
export function frontOf(p: Problem, header: string): RichTextInterface {
  const out: any[] = [`${header} · `, ...richFromMd(p.prompt.replace(/\s*\n+\s*/g, " "))];
  if (p.figure) out.push({ i: "i", url: `data:image/svg+xml;base64,${toBase64(p.figure)}`, percent: 50 });
  if (p.parts?.length) p.parts.forEach((pt, i) => out.push(`  (${i + 1}) `, ...richFromMd(pt.ask)));
  else if (p.answer.kind === "choice") p.answer.options.forEach((o, i) => out.push(`  (${LETTERS[i]}) `, ...richFromMd(o)));
  else if (p.answer.kind === "tuple") out.push("  Give ", ...p.answer.fields.flatMap((f, i) => [...(i ? [", "] : []), tex(f.tex || f.label)]), ".");
  return out;
}

/** card back: the answer, then the worked solution */
export function backOf(p: Problem): RichTextInterface {
  const out: any[] = [];
  if (p.parts?.length)
    p.parts.forEach((pt, i) => {
      out.push(`${i ? "  " : ""}(${i + 1}) `, ...answerRich(pt.answer, pt.answerTex));
      if (pt.explain) out.push(" — ", ...richFromMd(pt.explain));
    });
  else {
    out.push(...answerRich(p.answer, p.answerTex));
    if (p.steps.length) out.push("  ·  Solution: ", ...p.steps.flatMap((s, i) => [...(i ? [" → "] : []), ...richFromMd(s)]));
  }
  return out;
}

function toBase64(s: string): string {
  const bytes = new TextEncoder().encode(s);
  let bin = "";
  bytes.forEach((b) => (bin += String.fromCharCode(b)));
  return btoa(bin);
}

const headerFor = (t: Target) => (t.code ? `Drill ${t.code}` : `Drill · ${t.title}`);

async function reviewCount(rem: any): Promise<number> {
  try {
    const cards = await rem.getCards();
    return cards.reduce((n: number, c: any) => n + (c.repetitionHistory?.length ?? 0), 0);
  } catch {
    return 0;
  }
}

/** Put a new problem on the card. */
export async function writeProblem(plugin: RNPlugin, rem: any, targetName: string, reps?: Record<string, number>) {
  const target = resolveTarget(targetName);
  if (!target) return false;
  const seed = newSeed();
  const p = generateFor(target, seed);
  await rem.setText(frontOf(p, headerFor(target)));
  await rem.setBackText(backOf(p));
  await rem.setPowerupProperty(DRILL_POWERUP, SEED_SLOT, [String(seed)]);
  if (reps) reps[rem._id] = await reviewCount(rem);
  return true;
}

/**
 * Give every drill card a written-out problem, and a fresh one to any card reviewed since its
 * problem was written. Returns how many cards changed.
 */
export async function refreshStaticCards(plugin: RNPlugin): Promise<number> {
  const pu = await plugin.powerup.getPowerupByCode(DRILL_POWERUP);
  const rems = (await pu?.taggedRem()) ?? [];
  const reps = (await plugin.storage.getSynced<Record<string, number>>(REPS_KEY)) ?? {};
  let changed = 0;
  for (const rem of rems) {
    const target = (await rem.getPowerupProperty(DRILL_POWERUP, DRILL_SLOT))?.trim();
    if (!target || !resolveTarget(target)) continue;
    const seed = (await rem.getPowerupProperty(DRILL_POWERUP, SEED_SLOT))?.trim();
    const n = await reviewCount(rem);
    if (seed && reps[rem._id] !== undefined && n <= reps[rem._id]) continue;
    try {
      if (await writeProblem(plugin, rem, target, reps)) changed++;
    } catch (e) {
      console.error("[Drills] could not write a problem for", target, e);
    }
    if (changed % 25 === 0) await plugin.storage.setSynced(REPS_KEY, reps);
  }
  await plugin.storage.setSynced(REPS_KEY, reps);
  return changed;
}

/** After a review on desktop: the card gets its next problem right away. */
export async function reseedAfterReview(plugin: RNPlugin, cardId: string | undefined) {
  if (!cardId) return;
  const card = await plugin.card.findOne(cardId);
  const rem = card ? await plugin.rem.findOne(card.remId) : undefined;
  if (!rem || !(await rem.hasPowerup(DRILL_POWERUP))) return;
  const target = (await rem.getPowerupProperty(DRILL_POWERUP, DRILL_SLOT))?.trim();
  if (!target) return;
  const reps = (await plugin.storage.getSynced<Record<string, number>>(REPS_KEY)) ?? {};
  await writeProblem(plugin, rem, target, reps);
  await plugin.storage.setSynced(REPS_KEY, reps);
}
