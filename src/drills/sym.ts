// Symbolic parts for problems-as-data: an expression in x (or t, …) with the template's numbers
// folded in, as a checker reference string and as clean LaTeX.
//
//   symbolic("c*x^(n-1) + b", { c: 6, n: 3, b: -4 })  ->  ref "6 * x ^ 2 - 4",  tex "6x^{2} - 4"
//
// Only arithmetic on numbers is folded (and only when the result is an integer or a small
// fraction); the author writes the answer in the form it should be shown in.
import { math } from "./check";

type N = any;
const C = (v: number): N => new (math as any).ConstantNode(v);
const isC = (n: N, v?: number) => n?.isConstantNode && typeof n.value === "number" && (v === undefined || n.value === v);

/** p/q for a "nice" number (|q| ≤ 1000), else null */
function rational(v: number): [number, number] | null {
  if (!Number.isFinite(v)) return null;
  for (let q = 1; q <= 1000; q++) {
    const p = Math.round(v * q);
    if (Math.abs(v * q - p) < 1e-9 * Math.max(1, Math.abs(p))) return [p, q];
  }
  return null;
}

function fold(n: N, scope: Record<string, unknown>): N {
  if (n.isParenthesisNode) return fold(n.content, scope);
  if (n.isSymbolNode) return typeof scope[n.name] === "number" ? C(scope[n.name] as number) : n;
  if (n.isConstantNode) return n;
  if (n.isFunctionNode) {
    const args = n.args.map((a: N) => fold(a, scope));
    const out = new (math as any).FunctionNode(n.fn, args);
    if (args.every((a: N) => isC(a))) {
      const v = Number(out.evaluate());
      if (Number.isInteger(v)) return C(v);
    }
    return out;
  }
  if (n.isOperatorNode) {
    const a = n.args.map((x: N) => fold(x, scope));
    if (a.every((x: N) => isC(x))) {
      const v = Number(new (math as any).OperatorNode(n.op, n.fn, a).evaluate());
      if (rational(v)) return C(v);
    }
    const op = (o: string, fn: string, args: N[]) => new (math as any).OperatorNode(o, fn, args);
    if (n.fn === "unaryMinus") return isC(a[0]) ? C(-a[0].value) : op("-", "unaryMinus", a);
    if (n.fn === "unaryPlus") return a[0];
    const [l, r] = a;
    switch (n.op) {
      case "+": if (isC(l, 0)) return r; if (isC(r, 0)) return l; break;
      case "-": if (isC(r, 0)) return l; if (isC(l, 0)) return op("-", "unaryMinus", [r]); break;
      case "*": {
        // gather the numeric factors of the whole product into one leading coefficient
        const fs: N[] = [];
        let k = 1;
        const walk = (x: N) => {
          if (x.isOperatorNode && x.op === "*" && x.args.length === 2) x.args.forEach(walk);
          else if (x.isOperatorNode && x.fn === "unaryMinus") { k = -k; walk(x.args[0]); }
          else if (isC(x)) k *= x.value;
          else fs.push(x);
        };
        walk(l); walk(r);
        if (k === 0) return C(0);
        if (!fs.length) return C(k);
        const body = fs.reduce((acc: N, f: N) => op("*", "multiply", [acc, f]));
        if (k === 1) return body;
        if (k === -1) return op("-", "unaryMinus", [body]);
        return fs.reduce((acc: N, f: N) => op("*", "multiply", [acc, f]), C(k));
      }
      case "/": if (isC(l, 0)) return C(0); if (isC(r, 1)) return l; break;
      case "^": if (isC(r, 1)) return l; if (isC(r, 0)) return C(1); break;
    }
    return op(n.op, n.fn, a);
  }
  return n;
}

const FN: Record<string, string> = { sin: "\\sin", cos: "\\cos", tan: "\\tan", sec: "\\sec", csc: "\\csc", cot: "\\cot", atan: "\\arctan", asin: "\\arcsin", acos: "\\arccos", log: "\\ln" };
const num = (v: number): string => {
  if (Number.isInteger(v)) return `${v}`;
  const r = rational(v);
  if (r && r[1] <= 100) return `${r[0] < 0 ? "-" : ""}\\frac{${Math.abs(r[0])}}{${r[1]}}`;
  return `${Number(v.toPrecision(6))}`;
};
const isSum = (n: N) => n.isOperatorNode && (n.op === "+" || n.op === "-") && n.args.length === 2;
const isNeg = (n: N) => (n.isOperatorNode && n.fn === "unaryMinus") || (isC(n) && n.value < 0);
const wrap = (s: string) => `\\left(${s}\\right)`;
const mk = (o: string, fn: string, args: N[]) => new (math as any).OperatorNode(o, fn, args);
/** the same thing without its leading minus sign, or null if it has none */
function positive(n: N): N | null {
  if (isC(n)) return n.value < 0 ? C(-n.value) : null;
  if (n.isOperatorNode && n.fn === "unaryMinus") return n.args[0];
  if (n.isOperatorNode && (n.op === "*" || n.op === "/") && n.args.length === 2) {
    const l = positive(n.args[0]);
    if (!l) return null;
    return n.op === "*" && isC(l, 1) ? n.args[1] : mk(n.op, n.fn, [l, n.args[1]]);
  }
  return null;
}

function tex(n: N): string {
  if (isC(n)) return num(n.value);
  if (n.isSymbolNode) return n.name === "pi" ? "\\pi" : n.name;
  if (n.isFunctionNode) {
    const name = n.fn.name ?? String(n.fn);
    const a = n.args[0], t = tex(a);
    if (name === "exp") return `e^{${t}}`;
    if (name === "sqrt") return `\\sqrt{${t}}`;
    if (name === "abs") return `\\left|${t}\\right|`;
    const simple = a.isSymbolNode || (isC(a) && a.value >= 0) || (a.isOperatorNode && a.op === "*" && isC(a.args[0]) && a.args[0].value > 0 && a.args[1].isSymbolNode);
    return `${FN[name] ?? `\\operatorname{${name}}`}${simple ? ` ${t}` : wrap(t)}`;
  }
  if (n.isOperatorNode) {
    if (n.fn === "unaryMinus") return `-${isSum(n.args[0]) ? wrap(tex(n.args[0])) : tex(n.args[0])}`;
    const [l, r] = n.args;
    switch (n.op) {
      case "+": { const q = positive(r); return q ? `${tex(l)} - ${isSum(q) ? wrap(tex(q)) : tex(q)}` : `${tex(l)} + ${tex(r)}`; }
      case "-": { const q = positive(r); return q ? `${tex(l)} + ${isSum(q) ? wrap(tex(q)) : tex(q)}` : `${tex(l)} - ${isSum(r) ? wrap(tex(r)) : tex(r)}`; }
      case "*": {
        const L = isSum(l) ? wrap(tex(l)) : tex(l);
        const R = isSum(r) || isNeg(r) ? wrap(tex(r)) : tex(r);
        if (isC(l) && isC(r)) return `${L} \\cdot ${R}`;
        // a number never follows a letter without a dot: x·3 would read as x3
        return `${L}${/^[\d-]/.test(R) ? " \\cdot " : ""}${R}`;
      }
      case "/": return `\\frac{${tex(l)}}{${tex(r)}}`;
      case "^": {
        const fname = l.isFunctionNode ? l.fn.name ?? "" : "";
        if (FN[fname] && fname !== "log" && isC(r) && r.value > 0) {
          const a = l.args[0];
          return `${FN[fname]}^{${tex(r)}}${a.isSymbolNode ? ` ${tex(a)}` : wrap(tex(a))}`;
        }
        const base = l.isSymbolNode || (isC(l) && l.value >= 0 && Number.isInteger(l.value)) ? tex(l) : wrap(tex(l));
        return `${base}^{${tex(r)}}`;
      }
    }
  }
  return n.toTex();
}

export function symbolic(expr: string, scope: Record<string, unknown>): { ref: string; tex: string } {
  const node = fold(math.parse(expr), scope);
  return { ref: node.toString({ parenthesis: "auto" }), tex: tex(node) };
}
