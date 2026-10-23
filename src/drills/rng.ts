// Small seeded RNG so any problem can be regenerated from its seed.

export class Rng {
  private s: number;
  constructor(seed: number) {
    this.s = seed >>> 0 || 0x9e3779b9;
  }
  /** mulberry32 */
  next(): number {
    let t = (this.s += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  }
  int(lo: number, hi: number): number {
    return lo + Math.floor(this.next() * (hi - lo + 1));
  }
  /** random int in [lo, hi] not in `exclude` (default excludes 0) */
  nz(lo: number, hi: number, exclude: number[] = [0]): number {
    for (;;) {
      const k = this.int(lo, hi);
      if (!exclude.includes(k)) return k;
    }
  }
  pick<T>(xs: readonly T[]): T {
    return xs[Math.floor(this.next() * xs.length)];
  }
  chance(p: number): boolean {
    return this.next() < p;
  }
}
