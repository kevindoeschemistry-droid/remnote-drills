// Exact fractions for hand-sized arithmetic (series coefficients, roots).
import { gcd } from "./tex";

export class Q {
  readonly n: number;
  readonly d: number;
  constructor(n: number, d = 1) {
    if (d === 0) throw new Error("zero denominator");
    if (d < 0) {
      n = -n;
      d = -d;
    }
    const g = gcd(n, d);
    this.n = n / g;
    this.d = d / g;
  }
  static of(x: number | Q): Q {
    return x instanceof Q ? x : new Q(x);
  }
  add(o: number | Q) {
    const b = Q.of(o);
    return new Q(this.n * b.d + b.n * this.d, this.d * b.d);
  }
  sub(o: number | Q) {
    return this.add(Q.of(o).neg());
  }
  mul(o: number | Q) {
    const b = Q.of(o);
    return new Q(this.n * b.n, this.d * b.d);
  }
  div(o: number | Q) {
    const b = Q.of(o);
    return new Q(this.n * b.d, this.d * b.n);
  }
  neg() {
    return new Q(-this.n, this.d);
  }
  isZero() {
    return this.n === 0;
  }
  isInt() {
    return this.d === 1;
  }
  value() {
    return this.n / this.d;
  }
  /** LaTeX, e.g. -\frac{1}{2} */
  tex(): string {
    if (this.d === 1) return `${this.n}`;
    return `${this.n < 0 ? "-" : ""}\\frac{${Math.abs(this.n)}}{${this.d}}`;
  }
  /** mathjs */
  js(): string {
    return this.d === 1 ? `(${this.n})` : `(${this.n}/${this.d})`;
  }
}

/** q * body as a LaTeX term:  \frac{1}{2}x^{2}, -x, 3 */
export function qterm(q: Q, body: string): string {
  if (q.isZero()) return "0";
  if (body === "") return q.tex();
  if (q.n === 1 && q.d === 1) return body;
  if (q.n === -1 && q.d === 1) return `-${body}`;
  if (q.d === 1) return `${q.n}${body}`;
  return `${q.n < 0 ? "-" : ""}\\frac{${Math.abs(q.n)}}{${q.d}}${body}`;
}
