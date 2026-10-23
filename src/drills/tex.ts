// Tiny LaTeX/mathjs string builders for Kuta-style problems.
// Every helper returns a pair-friendly string; generators build the LaTeX and
// the mathjs form side by side so the checker and the display never drift.

export function gcd(a: number, b: number): number {
  a = Math.abs(a);
  b = Math.abs(b);
  while (b) [a, b] = [b, a % b];
  return a || 1;
}

/** LaTeX for the fraction n/d, reduced. */
export function frac(n: number, d: number): string {
  if (d < 0) {
    n = -n;
    d = -d;
  }
  const g = gcd(n, d);
  n /= g;
  d /= g;
  if (d === 1) return `${n}`;
  return n < 0 ? `-\\frac{${-n}}{${d}}` : `\\frac{${n}}{${d}}`;
}

/** mathjs for the fraction n/d */
export function fracJs(n: number, d: number): string {
  return `(${n}/${d})`;
}

/** coefficient * body, LaTeX:  3x^{2}, -x, x, 5 */
export function ct(k: number, body: string): string {
  if (k === 0) return "0"; // join() drops it
  if (body === "") return `${k}`;
  if (k === 1) return body;
  if (k === -1) return `-${body}`;
  return `${k}${body}`;
}

/** coefficient * body, mathjs */
export function cj(k: number, body: string): string {
  return body === "" ? `(${k})` : `(${k})*(${body})`;
}

/** x^n LaTeX ("" for n = 0) */
export function xp(n: number): string {
  if (n === 0) return "";
  if (n === 1) return "x";
  return `x^{${n}}`;
}

/** x^n mathjs */
export function xpj(n: number): string {
  return n === 0 ? "1" : `x^(${n})`;
}

/** e^{kx} LaTeX */
export function ex(k: number, v = "x"): string {
  if (k === 0) return "";
  return `e^{${ct(k, v)}}`;
}

/** e^{kx} mathjs */
export function exj(k: number, v = "x"): string {
  return k === 0 ? "1" : `exp((${k})*${v})`;
}

/** Join LaTeX terms with + / - signs; drops "0" terms. */
export function join(terms: string[]): string {
  const t = terms.filter((s) => s !== "" && s !== "0");
  if (!t.length) return "0";
  let out = t[0];
  for (const s of t.slice(1)) {
    out += s.startsWith("-") ? ` - ${s.slice(1)}` : ` + ${s}`;
  }
  return out;
}

/** "+ 3" / "- 3" suffix for a constant, "" for 0 */
export function signed(k: number): string {
  if (k === 0) return "";
  return k < 0 ? ` - ${-k}` : ` + ${k}`;
}

/** $...$ wrapper */
export const m = (s: string) => `$${s}$`;
