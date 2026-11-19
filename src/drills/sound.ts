// The little "got it" sounds. Synthesised with the Web Audio API, so there is no audio file and
// no network request. A sound only plays in answer to a click or key press (browsers require
// that), and never throws: where audio isn't available it is simply silent.
type Tone = [freq: number, start: number, length: number];

const TUNES: Record<"step" | "correct" | "clear", Tone[]> = {
  step: [[880, 0, 0.09]], // a checked step inside a problem: one soft tick
  correct: [[659.25, 0, 0.12], [987.77, 0.09, 0.22]], // E5 then B5: a rising two-note ding
  clear: [[523.25, 0, 0.12], [659.25, 0.1, 0.12], [783.99, 0.2, 0.12], [1046.5, 0.3, 0.38]], // C–E–G–C: a skill went warm
};

let ctx: AudioContext | undefined;

export function play(which: keyof typeof TUNES, volume = 0.12): void {
  try {
    const AC: typeof AudioContext | undefined = (globalThis as any).AudioContext ?? (globalThis as any).webkitAudioContext;
    if (!AC) return;
    ctx ??= new AC();
    if (ctx.state === "suspended") void ctx.resume();
    const t0 = ctx.currentTime + 0.01;
    for (const [freq, start, length] of TUNES[which]) {
      const osc = ctx.createOscillator(), gain = ctx.createGain();
      osc.type = "sine";
      osc.frequency.value = freq;
      // quick attack, smooth decay: a bell-like ping rather than a beep
      gain.gain.setValueAtTime(0, t0 + start);
      gain.gain.linearRampToValueAtTime(volume, t0 + start + 0.012);
      gain.gain.exponentialRampToValueAtTime(0.0001, t0 + start + length);
      osc.connect(gain).connect(ctx.destination);
      osc.start(t0 + start);
      osc.stop(t0 + start + length + 0.02);
    }
  } catch {
    /* no audio here: stay silent */
  }
}
