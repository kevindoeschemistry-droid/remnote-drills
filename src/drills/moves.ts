// Movement breaks (Nov 2026): every so many settled problems the panel names a short set to do before the next card.
// The count lives in session storage so it carries from card to card in the queue and starts again with the app.
import type { RNPlugin } from "@remnote/plugin-sdk";

export const MOVE_KEY = "drill.moves.count";
export const MOVE_EVERY = "drill-move-every";
export const MOVE_SET = "drill-move-set";
export type MoveSet = "mixed" | "bodyweight" | "martial" | "holds";

export const MOVES: Record<Exclude<MoveSet, "mixed">, string[]> = {
  bodyweight: ["15 push-ups", "20 squats", "10 burpees", "20 alternating lunges", "30 jumping jacks", "15 sit-ups", "20 mountain climbers each side", "12 squat jumps"],
  martial: ["20 front kicks each leg", "10 roundhouse kicks each leg", "20 straight punches in horse stance", "10 side kicks each leg", "One minute of shadow sparring", "10 crescent kicks each leg", "10 bow-stance to horse-stance transitions each side"],
  holds: ["Horse stance for 60 seconds", "Wall sit for 60 seconds", "Plank for 60 seconds", "Side plank for 30 seconds each side", "Single-leg balance for 45 seconds each leg", "Deep squat hold for 60 seconds"],
};
export const MOVE_SETS: { key: MoveSet; label: string }[] = [
  { key: "mixed", label: "Mixed" },
  { key: "bodyweight", label: "Bodyweight sets" },
  { key: "martial", label: "Kicks and strikes" },
  { key: "holds", label: "Holds (hands and eyes stay free)" },
];

/** a break falls on every `every`-th settled problem; 0 or less turns breaks off */
export const moveDue = (count: number, every: number): boolean => every > 0 && count > 0 && count % every === 0;

/** the nth break's set: walks the list in order, so nothing repeats until the list has been done once */
export function pickMove(set: MoveSet, nth: number): string {
  const order: Exclude<MoveSet, "mixed">[] = ["bodyweight", "martial", "holds"];
  const k = Math.max(0, Math.floor(nth));
  if (set !== "mixed") return MOVES[set][k % MOVES[set].length];
  const list = MOVES[order[k % order.length]];
  return list[Math.floor(k / order.length) % list.length];
}

/** count one settled problem; returns the set to do if this one lands on a break */
export async function tickMove(plugin: RNPlugin): Promise<string | null> {
  const every = Number(await plugin.settings.getSetting<number>(MOVE_EVERY)) || 0;
  if (every <= 0) return null;
  const count = ((await plugin.storage.getSession<number>(MOVE_KEY)) ?? 0) + 1;
  await plugin.storage.setSession(MOVE_KEY, count);
  if (!moveDue(count, every)) return null;
  const raw = (await plugin.settings.getSetting<string>(MOVE_SET)) || "mixed";
  const set: MoveSet = raw === "mixed" || raw in MOVES ? (raw as MoveSet) : "mixed";
  return pickMove(set, count / every - 1);
}
