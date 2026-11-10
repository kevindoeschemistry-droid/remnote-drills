// K–8 mathematics (Common Core K–8), Level 1. Built backward from clean answers:
// whole-number results, exact fractions, terminating decimals, Pythagorean triples.
// Size-specific templates (add within 10 vs within 1000) are separate names so a
// learning objective draws only problems of its own grade.
// Every problem carries meta.mx + inputs for tests/verify/school_k8.py.
import { Rng } from "./rng";
import type { Draft } from "./types";
import { m } from "./tex";
import { Q } from "./rational";
import { require_ } from "./reject";
import { approx, choice, cx, dec, decTex, draft, exact, gcd, int, intTxt, lcm, NAMES, par, poly, polyPy, qpy, qtex, sg, shuffle, tuple } from "./school";

type Gen = (r: Rng) => Draft;
const q = (n: number, d = 1) => new Q(n, d);
const CMP = [">", "<", "="];
const usd = (x: string | number) => m(`\\text{\\textdollar}${x}`);
const piTol = (v: number) => Math.max(5e-4, 0.0051 / v);
const cmpOf = (a: Q, b: Q) => (a.sub(b).isZero() ? "=" : a.sub(b).n > 0 ? ">" : "<");

/** evaluate-this: the answer is the exact value of `py` */
function value(prompt: string, py: string, v: Q | number, steps: string[], tex?: string): Draft {
  const vq = Q.of(v);
  return draft(prompt, exact(vq), tex ?? qtex(vq), steps, { mx: "expr", e: py });
}
/** fill-the-box: the answer replaces ? in `eqPy` */
function box(prompt: string, eqPy: string, v: Q | number, steps: string[]): Draft {
  const vq = Q.of(v);
  return draft(prompt, exact(vq, "?"), `? = ${qtex(vq)}`, steps, { mx: "eq", eq: eqPy });
}
function compare(aTex: string, bTex: string, a: Q, b: Q, why: string, aPy = qpy(a), bPy = qpy(b)): Draft {
  const c = cmpOf(a, b);
  return draft(
    `Which symbol makes this true? ${m(`${aTex} \\;\\square\\; ${bTex}`)}`,
    choice(CMP, c),
    `${aTex} ${c} ${bTex}`,
    [why, `So ${m(`${aTex} ${c} ${bTex}`)}.`],
    { mx: "cmp", a: aPy, b: bPy }
  );
}

// ── counting & place value ──────────────────────────────────────────────────
const countOn = (lo: number, hi: number, kMax: number): Gen => (r) => {
  const n = r.int(lo, hi), k = r.int(1, kMax);
  return draft(
    k === 1 ? `What number comes right after ${m(int(n))}?` : `Start at ${m(int(n))} and count on. What number do you say ${m(`${k}`)} numbers later?`,
    exact(n + k), `${n + k}`,
    [`Count on from ${m(`${n}`)}: ${m(Array.from({ length: k }, (_, i) => n + i + 1).join(",\\ "))}.`],
    { mx: "count-on", n, k }
  );
};
const countBy = (steps: number[], max: number): Gen => (r) => {
  const s = r.pick(steps);
  const start = s === 10 && max <= 100 ? 10 * r.int(1, 5) : s * r.int(1, Math.floor(max / s) - 4) + (s >= 10 && r.chance(0.4) && max > 100 ? r.int(1, 9) * (s / 10) : 0);
  const seq = [0, 1, 2, 3].map((i) => start + i * s);
  require_(seq[3] + s <= max);
  return draft(
    `Skip-count by ${s}s. What comes next? ${m(`${seq.map(int).join(",\\ ")},\\ ?`)}`,
    exact(seq[3] + s), `${seq[3] + s}`,
    [`Each step adds ${s}: ${m(`${int(seq[3])} + ${s} = ${int(seq[3] + s)}`)}.`],
    { mx: "count-by", seq, s }
  );
};
const cmpWhole = (lo: number, hi: number, close: boolean): Gen => (r) => {
  const a = r.int(lo, hi);
  let b: number;
  if (r.chance(0.12)) b = a;
  else if (close) {
    // same leading digits, differ lower down (or swapped digits)
    const s = String(a);
    const sw = s.length >= 2 && r.chance(0.4) ? s.slice(0, -2) + s.slice(-1) + s.slice(-2, -1) : null;
    b = sw && sw !== s && !sw.startsWith("0") ? Number(sw) : a + r.nz(-9, 9) * 10 ** r.int(0, Math.max(0, s.length - 2));
  } else b = r.int(lo, hi);
  require_(b >= lo && b <= hi);
  return compare(int(a), int(b), q(a), q(b), a === b ? "Same digits in every place." : `Compare from the greatest place value down; the first place where the digits differ decides.`);
};
function cmpDec(places: number): Gen {
  return (r) => {
    const sc = 10 ** places;
    const a = r.int(1, 30 * sc) ;
    // trailing-zero traps: 0.4 vs 0.38, 0.45 vs 0.405
    const b = r.chance(0.15) ? a : r.chance(0.5) ? Math.round(a / 10) * 10 + r.nz(-9, 9) : a + r.nz(-5, 5) * 10 ** r.int(0, places);
    require_(b > 0);
    return compare(decTex(a, places), decTex(b, places), q(a, sc), q(b, sc), "Line up the decimal points and compare place by place (write trailing zeros so both have the same number of digits).", dec(a, places), dec(b, places));
  };
}
const cmpFrac = (same: boolean): Gen => (r) => {
  let a: Q, b: Q;
  if (same) {
    if (r.chance(0.5)) {
      const d = r.int(2, 12);
      a = q(r.int(1, d - 1), d); b = q(r.int(1, d - 1), d);
      return compare(`\\frac{${a.n * (d / a.d)}}{${d}}`, `\\frac{${b.n * (d / b.d)}}{${d}}`, a, b, "Same denominator: same-size pieces, so more pieces is more.");
    }
    const n = r.int(1, 5), d1 = r.int(n + 1, 12), d2 = r.int(n + 1, 12);
    return compare(`\\frac{${n}}{${d1}}`, `\\frac{${n}}{${d2}}`, q(n, d1), q(n, d2), "Same numerator: the same number of pieces, and smaller denominators mean bigger pieces.");
  }
  const d1 = r.int(2, 12), d2 = r.int(2, 12);
  const n1 = r.int(1, d1 - 1), n2 = r.chance(0.15) ? (n1 * d2) / d1 : r.int(1, d2 - 1);
  require_(Number.isInteger(n2) && n2 > 0 && d1 !== d2);
  a = q(n1, d1); b = q(n2, d2);
  return compare(`\\frac{${n1}}{${d1}}`, `\\frac{${n2}}{${d2}}`, a, b, `Common denominator ${d1 * d2}: ${m(`\\frac{${n1 * d2}}{${d1 * d2}}`)} vs ${m(`\\frac{${n2 * d1}}{${d1 * d2}}`)}.`);
};
const cmpRational: Gen = (r) => {
  const mk = () => (r.chance(0.5) ? q(r.int(-40, 40), 10) : q(r.nz(-12, 12), r.int(2, 6)));
  const a = mk(), b = r.chance(0.1) ? a.neg() : mk();
  require_(!a.isZero() && !b.isZero() && (a.value() < 0 || b.value() < 0));
  const t = (x: Q) => (x.d === 10 || x.d === 5 || x.d === 2 ? dec(Math.round(x.value() * 10), 1) : x.tex());
  return compare(t(a), t(b), a, b, "On the number line, the number farther right is greater; every negative is less than every positive, and −7 < −3.");
};
const teen: Gen = (r) => {
  const o = r.int(1, 9);
  return r.chance(0.5)
    ? box(`Fill in the box: ${m(`${10 + o} = 10 + \\square`)}`, `${10 + o} == 10 + ?`, o, [`${10 + o} is one ten and ${o} ones.`])
    : value(`${m(`10 + ${o} = \\square`)}`, `10 + ${o}`, 10 + o, [`One ten and ${o} ones make ${10 + o}.`]);
};
const tensOnes: Gen = (r) => {
  const n = r.int(10, 99);
  return draft(
    `How many tens and how many ones are in ${m(`${n}`)}?`,
    tuple([{ label: "tens", tex: "\\text{tens}", ref: Math.floor(n / 10) }, { label: "ones", tex: "\\text{ones}", ref: n % 10 }]),
    `${Math.floor(n / 10)}\\text{ tens}, ${n % 10}\\text{ ones}`,
    [`${m(`${n} = ${Math.floor(n / 10) * 10} + ${n % 10}`)}: the left digit counts tens, the right digit ones.`],
    { mx: "tens-ones", n }
  );
};
const moreLess = (step: number, lo: number, hi: number): Gen => (r) => {
  const n = r.int(lo, hi), up = r.chance(0.5);
  const v = up ? n + step : n - step;
  require_(v >= 0);
  return value(`What is ${step} ${up ? "more" : "less"} than ${m(int(n))}?`, `${n} ${up ? "+" : "-"} ${step}`, v, [`Only the ${step === 10 ? "tens" : "hundreds"} digit changes: ${m(`${int(n)} ${up ? "+" : "-"} ${step} = ${int(v)}`)}.`]);
};
/** expanded form with one missing digit: 4,307 = 4×1000 + ?×100 + 0×10 + 7 */
const expanded = (digits: number, places: number): Gen => (r) => {
  const ds = Array.from({ length: digits }, (_, i) => (i === 0 ? r.int(1, 9) : r.int(0, 9)));
  const hide = r.int(0, digits - 1);
  const pows = ds.map((_, i) => digits - places - 1 - i);
  const val = (p: number) => (p >= 0 ? int(10 ** p) : `\\frac{1}{${int(10 ** -p)}}`);
  const valPy = (p: number) => (p >= 0 ? `${10 ** p}` : `(1/${10 ** -p})`);
  const scaled = Number(ds.join(""));
  const terms = ds.map((d, i) => `${i === hide ? "\\square" : d} \\times ${val(pows[i])}`);
  const eq = `${dec(scaled, places)} == ` + ds.map((d, i) => `${i === hide ? "?" : d}*${valPy(pows[i])}`).join(" + ");
  return box(`Fill in the box: ${m(`${decTex(scaled, places)} = ${terms.join(" + ")}`)}`, eq, ds[hide], [`The digit in the ${val(pows[hide])}s place of ${m(decTex(scaled, places))} is ${ds[hide]}.`]);
};
const digitValue = (digits: number, places: number): Gen => (r) => {
  const ds = Array.from({ length: digits }, (_, i) => (i === 0 ? r.int(1, 9) : r.int(0, 9)));
  const at = r.int(0, digits - 1);
  require_(ds[at] !== 0 && ds.filter((d) => d === ds[at]).length === 1);
  const scaled = Number(ds.join(""));
  const p = digits - places - 1 - at;
  const v = p >= 0 ? q(ds[at] * 10 ** p) : q(ds[at], 10 ** -p);
  return draft(
    `What is the value of the digit ${m(`${ds[at]}`)} in ${m(decTex(scaled, places))}?`,
    exact(v), qtex(v),
    [`It sits in the ${p >= 0 ? int(10 ** p) : `\\frac{1}{${10 ** -p}}`}s place: ${m(`${ds[at]} \\times ${p >= 0 ? int(10 ** p) : `\\frac{1}{${10 ** -p}}`} = ${p >= 0 ? int(v.n) : dec(ds[at], -p)}`)}.`],
    { mx: "digit-value", s: dec(scaled, places), i: at }
  );
};
const tenTimes = (withDecimals: boolean): Gen => (r) => {
  const d = r.int(1, 9);
  const p1 = withDecimals ? r.int(-3, 2) : r.int(0, 4);
  const k = withDecimals ? r.pick([1, -1]) : r.pick([1, 2]);
  const p2 = p1 + k;
  require_(withDecimals ? p2 >= -3 && p2 <= 3 : p2 <= 5);
  const v = (p: number) => (p >= 0 ? q(d * 10 ** p) : q(d, 10 ** -p));
  const t = (p: number) => (p >= 0 ? int(d * 10 ** p) : dec(d, -p));
  const ratio = v(p2).div(v(p1));
  return draft(
    `The ${d} in ${m(t(p2))} is how many times the ${d} in ${m(t(p1))}? (A fraction is fine.)`,
    exact(ratio), qtex(ratio),
    [`Each place is ten times the place to its right, so ${Math.abs(k)} place${Math.abs(k) > 1 ? "s" : ""} ${k > 0 ? "left" : "right"} is ${m(qtex(ratio))} times as much.`],
    { mx: "expr", e: `(${p2 >= 0 ? d * 10 ** p2 : `${d}/${10 ** -p2}`})/(${p1 >= 0 ? d * 10 ** p1 : `${d}/${10 ** -p1}`})` }
  );
};
const roundTo = (digits: [number, number], places: number, targets: number[]): Gen => (r) => {
  const nd = r.int(digits[0], digits[1]);
  const scaled = r.int(10 ** (nd - 1), 10 ** nd - 1);
  const t = r.pick(targets); // power of ten (negative = decimal places)
  require_(10 ** (t + places) < scaled);
  const unit = 10 ** (t + places);
  const down = Math.floor(scaled / unit) * unit;
  const res = scaled - down >= unit / 2 ? down + unit : down;
  const name = t > 0 ? `nearest ${intTxt(10 ** t)}` : t === 0 ? "nearest whole number" : `nearest ${["tenth", "hundredth", "thousandth"][-t - 1]}`;
  return draft(
    `Round ${m(decTex(scaled, places))} to the ${name}.`,
    exact(q(res, 10 ** places)), decTex(res, places),
    [`Look at the digit one place to the right of the ${t === 0 ? "ones" : name.replace("nearest ", "") + "s"} place: 5 or more rounds up, less than 5 rounds down.`, `${m(`${decTex(scaled, places)} \\approx ${decTex(res, places)}`)}.`],
    { mx: "round", s: dec(scaled, places), t }
  );
};
const pow10: Gen = (r) => {
  const scaled = r.int(1, 999), places = r.int(0, 2), k = r.int(1, 3);
  const mul = r.chance(0.5), expo = r.chance(0.4);
  const x = q(scaled, 10 ** places);
  const res = mul ? x.mul(10 ** k) : x.div(10 ** k);
  const f = expo ? `10^{${k}}` : int(10 ** k);
  return value(
    `${m(`${decTex(scaled, places)} ${mul ? "\\times" : "\\div"} ${f} = \\;?`)}`,
    `${dec(scaled, places)} ${mul ? "*" : "/"} 10**${k}`, res,
    [`${mul ? "Multiplying" : "Dividing"} by ${m(f)} moves every digit ${k} place${k > 1 ? "s" : ""} ${mul ? "left" : "right"} (the decimal point ${k} to the ${mul ? "right" : "left"}).`],
    decTexQ(res)
  );
};
function decTexQ(v: Q): string {
  for (let p = 0; p <= 6; p++) if (Number.isInteger(v.value() * 10 ** p) || (10 ** p) % v.d === 0) return decTex(Math.round(v.n * (10 ** p / v.d)), p);
  return v.tex();
}

// ── addition and subtraction ────────────────────────────────────────────────
const addWithin = (max: number, minTerm = 0): Gen => (r) => {
  const a = r.int(minTerm, max), b = r.int(minTerm, max);
  const add = r.chance(0.5);
  require_(add ? a + b <= max : true);
  const [x, y] = add ? [a, b] : [Math.max(a, b), Math.min(a, b)];
  const v = add ? x + y : x - y;
  return value(`${m(`${int(x)} ${add ? "+" : "-"} ${int(y)} = \\;?`)}`, `${x} ${add ? "+" : "-"} ${y}`, v,
    [max <= 20 ? (add ? `Count on ${y} from ${x}, or make a ten.` : `Think addition: ${y} + ? = ${x}.`) : `Line up place values; ${add ? "regroup 10 ones as a ten (10 tens as a hundred) when a column passes 9" : "break a ten (or hundred) when a column's top digit is smaller"}.`, `${m(`${int(x)} ${add ? "+" : "-"} ${int(y)} = ${int(v)}`)}.`]);
};
const add2d1d: Gen = (r) => {
  const a = r.int(11, 89), b = r.chance(0.5) ? r.int(2, 9) : 10 * r.int(1, 5);
  require_(a + b < 100);
  return value(`${m(`${a} + ${b} = \\;?`)}`, `${a} + ${b}`, a + b, [b % 10 === 0 ? `Add tens to tens: only the tens digit changes.` : `Add ones to ones; if they pass 9, make a new ten.`]);
};
const subTens: Gen = (r) => {
  const a = 10 * r.int(2, 9), b = 10 * r.int(1, a / 10);
  return value(`${m(`${a} - ${b} = \\;?`)}`, `${a} - ${b}`, a - b, [`${a / 10} tens − ${b / 10} tens = ${(a - b) / 10} tens.`]);
};
const addMany = (n: number, lo: number, hi: number, maxSum: number): Gen => (r) => {
  const xs = Array.from({ length: n }, () => r.int(lo, hi));
  const s = xs.reduce((a, b) => a + b, 0);
  require_(s <= maxSum);
  return value(`${m(`${xs.join(" + ")} = \\;?`)}`, xs.join(" + "), s, [`Look for pairs that make a ten (or a round number) first, then add the rest.`]);
};
const makeTen: Gen = (r) => {
  const a = r.int(1, 9);
  return box(`What number makes 10? ${m(`${a} + \\square = 10`)}`, `${a} + ? == 10`, 10 - a, [`${a} and ${10 - a} make 10.`]);
};
const decompose: Gen = (r) => {
  const n = r.int(2, 10), a = r.int(0, n);
  return box(`Fill in the box: ${m(`${n} = ${a} + \\square`)}`, `${n} == ${a} + ?`, n - a, [`${n} take away ${a} leaves ${n - a}.`]);
};
const missingAddend = (max: number): Gen => (r) => {
  const a = r.int(0, max), b = r.int(0, max - a), c = a + b;
  const form = r.int(0, 3);
  const [tex, py, v] = [
    [`${a} + \\square = ${c}`, `${a} + ? == ${c}`, b],
    [`\\square + ${b} = ${c}`, `? + ${b} == ${c}`, a],
    [`${c} - \\square = ${a}`, `${c} - ? == ${a}`, b],
    [`\\square - ${b} = ${a}`, `? - ${b} == ${a}`, c],
  ][form] as [string, string, number];
  return box(`Find the unknown number: ${m(tex)}`, py, v, [`Use the related fact: ${m(`${a} + ${b} = ${c}`)}.`]);
};
const trueFalse: Gen = (r) => {
  const a = r.int(1, 10), b = r.int(0, 10);
  const forms: [string, string, string, string][] = [
    [`${a + b}`, `${a} + ${b}`, `${a + b}`, `${a} + ${b}`],
    [`${a} + ${b}`, `${b} + ${a}`, `${a} + ${b}`, `${b} + ${a}`],
    [`${a}`, `${a + b} - ${b}`, `${a}`, `${a + b} - ${b}`],
    [`${a} + ${b}`, `${a + b + 1}`, `${a} + ${b}`, `${a + b + 1}`],
    [`${a + b} - ${a}`, `${a}`, `${a + b} - ${a}`, `${a}`],
    [`${a}`, `${a}`, `${a}`, `${a}`],
  ];
  const [lt, rt, lp, rp] = r.pick(forms);
  const truth = eval(lp) === eval(rp);
  return draft(`True or false? ${m(`${lt} = ${rt}`)}`, choice(["True", "False"], truth ? "True" : "False"), `\\text{${truth ? "True" : "False"}}`,
    [`The equal sign means both sides name the same number: left ${m(`= ${eval(lp)}`)}, right ${m(`= ${eval(rp)}`)}.`], { mx: "tf", l: lp, r: rp });
};
const evenOdd: Gen = (r) => {
  const n = r.int(1, 20);
  const ev = n % 2 === 0;
  return draft(`Is ${m(`${n}`)} even or odd?`, choice(["Even", "Odd"], ev ? "Even" : "Odd"), `\\text{${ev ? "Even" : "Odd"}}`,
    [ev ? `${n} = ${n / 2} + ${n / 2}: it splits into two equal groups (pairs with none left).` : `Pairing leaves one over: ${n} = ${(n - 1) / 2} + ${(n + 1) / 2}.`], { mx: "even-odd", n });
};

// word problems: the story type and its numbers go to the verifier, which solves the story itself
type Story = { text: string; v: number; type: string; a: number; b: number; why: string };
const THINGS = ["apples", "stickers", "marbles", "books", "shells", "cards", "pencils", "stamps"];
function addStory(r: Rng, max: number): Story {
  const nm = r.pick(NAMES), th = r.pick(THINGS);
  const a = r.int(1, max - 1), b = r.int(1, max - a), c = a + b;
  const t = r.int(0, 6);
  const other = r.pick(NAMES.filter((x) => x !== nm));
  const S: Story[] = [
    { type: "add-result", a, b, v: c, text: `${nm} has ${a} ${th}. ${nm} gets ${b} more. How many ${th} does ${nm} have now?`, why: `${a} + ${b} = ${c}` },
    { type: "add-change", a, b: c, v: b, text: `${nm} had ${a} ${th} and got some more. Now ${nm} has ${c}. How many did ${nm} get?`, why: `${a} + ? = ${c}, so ? = ${c} − ${a} = ${b}` },
    { type: "add-start", a: b, b: c, v: a, text: `${nm} had some ${th}, then got ${b} more. Now there are ${c}. How many did ${nm} start with?`, why: `? + ${b} = ${c}, so ? = ${c} − ${b} = ${a}` },
    { type: "take-result", a: c, b, v: a, text: `There were ${c} ${th}. ${nm} gave away ${b}. How many are left?`, why: `${c} − ${b} = ${a}` },
    { type: "take-change", a: c, b: a, v: b, text: `There were ${c} ${th}. ${nm} gave some away and ${a} are left. How many were given away?`, why: `${c} − ? = ${a}, so ? = ${b}` },
    { type: "compare-diff", a: c, b: a, v: b, text: `${nm} has ${c} ${th}. ${other} has ${a}. How many more does ${nm} have?`, why: `${c} − ${a} = ${b}` },
    { type: "compare-bigger", a, b, v: c, text: `${nm} has ${a} ${th}. ${other} has ${b} more than ${nm}. How many does ${other} have?`, why: `${a} + ${b} = ${c}` },
  ];
  return S[t];
}
const wordAdd = (max: number): Gen => (r) => {
  const s = addStory(r, max);
  return draft(s.text, exact(s.v), `${s.v}`, [`${s.why}.`], { mx: "story", type: s.type, a: s.a, b: s.b });
};
const ITEMS = ["bags", "boxes", "rows", "plates", "teams"];
function multStory(r: Rng): Story {
  const a = r.int(2, 9), b = r.int(2, 9), c = a * b, it = r.pick(ITEMS), th = r.pick(THINGS);
  const S: Story[] = [
    { type: "groups-total", a, b, v: c, text: `There are ${a} ${it} with ${b} ${th} in each. How many ${th} in all?`, why: `${a} × ${b} = ${c}` },
    { type: "share-each", a: c, b: a, v: b, text: `${c} ${th} are shared equally among ${a} ${it}. How many go in each?`, why: `${c} ÷ ${a} = ${b}` },
    { type: "share-groups", a: c, b, v: a, text: `${c} ${th} are packed ${b} to a bag. How many bags are filled?`, why: `${c} ÷ ${b} = ${a}` },
    { type: "groups-total", a, b, v: c, text: `A garden has ${a} rows of ${b} plants. How many plants?`, why: `${a} × ${b} = ${c}` },
  ];
  return r.pick(S);
}
const wordMult: Gen = (r) => {
  const s = multStory(r);
  return draft(s.text, exact(s.v), `${s.v}`, [`${s.why}.`], { mx: "story", type: s.type, a: s.a, b: s.b });
};
const wordTwoStep: Gen = (r) => {
  const nm = r.pick(NAMES), a = r.int(3, 9), b = r.int(3, 9), c = r.int(2, a * b - 1);
  const plus = r.chance(0.5);
  const v = plus ? a * b + c : a * b - c;
  return draft(
    plus ? `${nm} buys ${a} packs of ${b} pencils and already had ${c}. How many pencils now?` : `${nm} buys ${a} packs of ${b} pencils and gives away ${c}. How many are left?`,
    exact(v), `${v}`,
    [`First ${m(`${a} \\times ${b} = ${a * b}`)}, then ${m(`${a * b} ${plus ? "+" : "-"} ${c} = ${v}`)}.`, `Estimate to check: about ${Math.round((a * b) / 10) * 10} ${plus ? "+" : "−"} ${c}.`],
    { mx: "story2", plus, a, b, c }
  );
};
const multCompare: Gen = (r) => {
  const a = r.int(2, 9), b = r.int(2, 12), nm = r.pick(NAMES), nm2 = r.pick(NAMES.filter((x) => x !== nm));
  return r.chance(0.5)
    ? draft(`${nm2} has ${b} stamps. ${nm} has ${a} times as many. How many does ${nm} have?`, exact(a * b), `${a * b}`, [`"${a} times as many" means multiply: ${m(`${a} \\times ${b} = ${a * b}`)}.`], { mx: "story", type: "times", a, b })
    : draft(`${nm} has ${a * b} stamps, which is ${a} times as many as ${nm2}. How many does ${nm2} have?`, exact(b), `${b}`, [`${m(`${a} \\times ? = ${a * b}`)}, so ${m(`? = ${a * b} \\div ${a} = ${b}`)}.`], { mx: "story", type: "times-part", a: a * b, b: a });
};
const remainderWord: Gen = (r) => {
  const per = r.int(4, 30), n = per * r.int(2, 9) + r.int(1, per - 1);
  const t = r.int(0, 2);
  const v = [Math.ceil(n / per), Math.floor(n / per), n % per][t];
  const text = [
    `${n} students go on a trip. Each van holds ${per}. How many vans are needed?`,
    `${n} eggs are packed into cartons of ${per}. How many cartons are filled completely?`,
    `${n} cards are dealt equally into piles of ${per}. How many cards are left over?`,
  ][t];
  return draft(text, exact(v), `${v}`, [`${m(`${n} \\div ${per} = ${Math.floor(n / per)}\\text{ R }${n % per}`)}.`, ["The leftover students still need a van: round up.", "Only full cartons count: drop the remainder.", "The question is the remainder."][t]], { mx: "rem", t, n, per });
};

// ── multiplication and division ─────────────────────────────────────────────
const array: Gen = (r) => {
  const a = r.int(2, 5), b = r.int(2, 5);
  return value(`A rectangle is split into ${m(`${a}`)} rows of ${m(`${b}`)} equal squares. How many squares in all?`, `${a}*${b}`, a * b, [`Add the rows: ${m(Array(a).fill(b).join(" + ") + ` = ${a * b}`)}.`]);
};
const multFacts: Gen = (r) => {
  const a = r.int(2, 10), b = r.int(2, 10);
  return r.chance(0.5)
    ? value(`${m(`${a} \\times ${b} = \\;?`)}`, `${a}*${b}`, a * b, [`${m(`${a} \\times ${b} = ${a * b}`)}.`])
    : value(`${m(`${a * b} \\div ${a} = \\;?`)}`, `${a * b}/${a}`, b, [`Think multiplication: ${m(`${a} \\times ? = ${a * b}`)}.`]);
};
const missingFactor: Gen = (r) => {
  const a = r.int(2, 10), b = r.int(2, 10), c = a * b;
  const form = r.int(0, 2);
  const [tex, py, v] = [[`${a} \\times \\square = ${c}`, `${a}*? == ${c}`, b], [`\\square \\div ${a} = ${b}`, `?/${a} == ${b}`, c], [`${c} \\div \\square = ${b}`, `${c}/? == ${b}`, a]][form] as [string, string, number];
  return box(`Find the unknown number: ${m(tex)}`, py, v, [`Related fact: ${m(`${a} \\times ${b} = ${c}`)}.`]);
};
const multTens: Gen = (r) => {
  const a = r.int(2, 9), b = 10 * r.int(1, 9);
  return value(`${m(`${a} \\times ${b} = \\;?`)}`, `${a}*${b}`, a * b, [`${m(`${a} \\times ${b / 10} = ${(a * b) / 10}`)} ones becomes ${(a * b) / 10} tens.`]);
};
const multMulti = (big: boolean): Gen => (r) => {
  const [a, b] = big ? (r.chance(0.5) ? [r.int(100, 999), r.int(11, 99)] : [r.int(1000, 9999), r.int(11, 99)]) : r.chance(0.5) ? [r.int(1000, 9999), r.int(2, 9)] : [r.int(11, 99), r.int(11, 99)];
  return value(`${m(`${int(a)} \\times ${int(b)} = \\;?`)}`, `${a}*${b}`, a * b, [`Multiply by each place of ${m(int(b))} and add the partial products.`, `${m(`${int(a)} \\times ${int(b)} = ${int(a * b)}`)}.`]);
};
const divRem: Gen = (r) => {
  const d = r.int(3, 9), qt = r.int(100, 1100), rem = r.int(0, d - 1), n = d * qt + rem;
  require_(n < 10000);
  return draft(`Find the quotient and remainder: ${m(`${int(n)} \\div ${d}`)}.`,
    tuple([{ label: "quotient", tex: "q", ref: qt }, { label: "remainder", tex: "r", ref: rem }]),
    `${int(qt)}\\text{ R }${rem}`, [`Check: ${m(`${d} \\times ${int(qt)} + ${rem} = ${int(n)}`)}, and the remainder is less than ${d}.`], { mx: "divmod", n, d });
};
const divExact = (dlo: number, dhi: number, qlo: number, qhi: number): Gen => (r) => {
  const d = r.int(dlo, dhi), qt = r.int(qlo, qhi);
  return value(`${m(`${int(d * qt)} \\div ${d} = \\;?`)}`, `${d * qt}/${d}`, qt, [`Long division (or estimate ${m(`${int(d * qt)} \\div ${Math.round(d / 10) * 10 || d}`)} first), then check: ${m(`${d} \\times ${int(qt)} = ${int(d * qt)}`)}.`]);
};
const factors: Gen = (r) => {
  const n = r.int(2, 100);
  const divs = Array.from({ length: n }, (_, i) => i + 1).filter((k) => n % k === 0);
  if (r.chance(0.5)) {
    const prime = divs.length === 2;
    return draft(`Is ${m(`${n}`)} prime or composite?`, choice(["Prime", "Composite"], prime ? "Prime" : "Composite"), `\\text{${prime ? "Prime" : "Composite"}}`,
      [prime ? `Its only factors are 1 and ${n}.` : `${divs[1]} × ${n / divs[1]} = ${n}, so it has a factor other than 1 and itself.`], { mx: "prime", n });
  }
  return draft(`How many factors (whole-number divisors) does ${m(`${n}`)} have?`, exact(divs.length), `${divs.length}`,
    [`Factor pairs: ${m(divs.filter((k) => k * k <= n).map((k) => `${k}\\times${n / k}`).join(",\\ "))}.`, `Factors: ${divs.join(", ")}.`], { mx: "nfactors", n });
};
const pattern: Gen = (r) => {
  const a = r.int(1, 20), d = r.int(2, 9), k = r.int(5, 10), mul = r.chance(0.25);
  const terms = [a];
  for (let i = 1; i < k; i++) terms.push(mul ? terms[i - 1] * 2 : terms[i - 1] + d);
  return draft(`A pattern starts at ${m(`${a}`)} and the rule is "${mul ? "double" : `add ${d}`}". What is term number ${m(`${k}`)}?`, exact(terms[k - 1]), `${terms[k - 1]}`,
    [`${m(terms.join(",\\ "))}.`], { mx: "pattern", a, d: mul ? 0 : d, mul, k });
};
const twoPatterns: Gen = (r) => {
  const a = r.int(2, 6), f = r.int(2, 4), k = r.int(3, 7);
  return draft(`Pattern A starts at 0 and adds ${a}. Pattern B starts at 0 and adds ${a * f}. Give the ordered pair (A, B) of term number ${k} (counting 0 as term 1).`,
    tuple([{ label: "A", tex: "A", ref: a * (k - 1) }, { label: "B", tex: "B", ref: a * f * (k - 1) }]), `(${a * (k - 1)}, ${a * f * (k - 1)})`,
    [`Term ${k} is after ${k - 1} steps: A = ${a * (k - 1)}, B = ${a * f * (k - 1)} — every B term is ${f} times the A term.`], { mx: "two-patterns", a, b: a * f, k });
};
const orderOps = (exps: boolean): Gen => (r) => {
  const a = r.int(2, 9), b = r.int(2, 9), c = r.int(1, 9), d = r.int(2, 6), e = r.int(1, 5);
  const forms = exps
    ? [[`${a}^{2} + ${b} \\times ${c}`, `${a}**2 + ${b}*${c}`], [`(${a} + ${c})^{2} - ${d}^{2}`, `(${a}+${c})**2 - ${d}**2`], [`${d}^{3} \\div ${d} + ${e}`, `${d}**3/${d} + ${e}`], [`2^{${e + 1}} \\times ${b} - ${c}`, `2**${e + 1}*${b} - ${c}`]]
    : [[`${a} \\times (${b} + ${c}) - ${e}`, `${a}*(${b}+${c}) - ${e}`], [`[${d} \\times (${a} + ${b})] \\div ${d} + ${c}`, `(${d}*(${a}+${b}))/${d} + ${c}`], [`${a} + ${b} \\times ${c} - ${e}`, `${a} + ${b}*${c} - ${e}`], [`\\{${e} + [${a} \\times (${c} + ${d})]\\} - ${b}`, `(${e} + (${a}*(${c}+${d}))) - ${b}`]];
  const [tex, py] = r.pick(forms);
  const v = Function(`return ${py.replace(/\*\*/g, "**")}`)() as number;
  require_(Number.isInteger(v) && v >= 0);
  return value(`Evaluate ${m(tex)}.`, py, v, [`Innermost grouping first, then ${exps ? "exponents, then " : ""}× and ÷ left to right, then + and −.`, `${m(`${tex} = ${v}`)}.`]);
};
const timesAsLarge: Gen = (r) => {
  const k = r.int(2, 9), a = r.int(1000, 99999), b = r.int(100, 9999);
  return draft(`Without calculating: ${m(`${k} \\times (${int(a)} + ${int(b)})`)} is how many times as large as ${m(`${int(a)} + ${int(b)}`)}?`, exact(k), `${k}`,
    [`It is ${k} copies of the same sum, whatever that sum is.`], { mx: "expr", e: `(${k}*(${a}+${b}))/(${a}+${b})` });
};

// ── fractions ───────────────────────────────────────────────────────────────
const fracLine: Gen = (r) => {
  const b = r.int(2, 8), a = r.int(1, 2 * b);
  return draft(`The segment from 0 to 1 on a number line is split into ${m(`${b}`)} equal parts. A point is ${m(`${a}`)} of those parts to the right of 0. What number is at the point?`,
    exact(q(a, b)), `\\frac{${a}}{${b}}`, [`Each part has length ${m(`\\frac{1}{${b}}`)}; ${a} of them make ${m(`\\frac{${a}}{${b}}`)}.`], { mx: "expr", e: `${a}*(1/${b})` });
};
const unitShare: Gen = (r) => {
  const b = r.pick([2, 3, 4, 6, 8]), shape = r.pick(["circle", "rectangle", "square"]);
  return draft(`A ${shape} is cut into ${m(`${b}`)} equal parts. What fraction of the whole is one part?`, exact(q(1, b)), `\\frac{1}{${b}}`, [`${b} equal shares: each is ${m(`\\frac{1}{${b}}`)} — more shares make smaller shares.`], { mx: "expr", e: `1/${b}` });
};
const fracEquiv: Gen = (r) => {
  const d = r.int(2, 10), n = r.int(1, d - 1), k = r.int(2, 6);
  const g = gcd(n, d);
  const [nn, dd] = [n / g, d / g];
  return r.chance(0.5)
    ? box(`Fill in the box: ${m(`\\frac{${nn}}{${dd}} = \\frac{\\square}{${dd * k}}`)}`, `${nn}/${dd} == ?/${dd * k}`, nn * k, [`Denominator ×${k}, so numerator ×${k}: ${m(`\\frac{${nn}\\times${k}}{${dd}\\times${k}}`)}.`])
    : box(`Fill in the box: ${m(`\\frac{${nn * k}}{${dd * k}} = \\frac{${nn}}{\\square}`)}`, `${nn * k}/${dd * k} == ${nn}/?`, dd, [`Numerator ÷${k}, so denominator ÷${k}.`]);
};
const fracWhole: Gen = (r) => {
  const w = r.int(1, 8), d = r.int(1, 8);
  return r.chance(0.5)
    ? value(`${m(`\\frac{${w * d}}{${d}} = \\;?`)}`, `${w * d}/${d}`, w, [`${w * d} pieces of size ${m(`\\frac1{${d}}`)} make ${w} wholes.`])
    : box(`Fill in the box: ${m(`${w} = \\frac{\\square}{${d}}`)}`, `${w} == ?/${d}`, w * d, [`Each whole is ${d} pieces of size ${m(`\\frac1{${d}}`)}.`]);
};
const fracAddLike = (mixed: boolean): Gen => (r) => {
  const d = r.int(3, 12);
  let a = q(r.int(1, mixed ? 4 * d : d - 1), d), b = q(r.int(1, mixed ? 3 * d : d - 1), d);
  const add = r.chance(0.6);
  if (!add && a.sub(b).value() < 0) [a, b] = [b, a];
  if (mixed) require_(a.value() > 1 && b.value() > 1 && !a.isInt() && !b.isInt());
  const v = add ? a.add(b) : a.sub(b);
  const t = (x: Q) => (mixed ? qtex(x, true) : `\\frac{${x.n * (d / x.d)}}{${d}}`);
  return value(`${m(`${t(a)} ${add ? "+" : "-"} ${t(b)} = \\;?`)} (a fraction or mixed number written as e.g. 7/3)`, `${a.n}/${a.d} ${add ? "+" : "-"} ${b.n}/${b.d}`, v,
    [`Same denominator: ${add ? "add" : "subtract"} the numerators (${mixed ? "or the wholes and the parts separately, regrouping a whole if needed" : `${d}ths stay ${d}ths`}).`, `${m(`= ${qtex(v, true)}`)}.`]);
};
const fracDecompose: Gen = (r) => {
  const d = r.int(4, 12), n = r.int(3, d + 3), a = r.int(1, n - 2), b = r.int(1, n - a - 1), c = n - a - b;
  return box(`Fill in the box: ${m(`\\frac{${n}}{${d}} = \\frac{${a}}{${d}} + \\frac{${b}}{${d}} + \\frac{\\square}{${d}}`)}`, `${n}/${d} == ${a}/${d} + ${b}/${d} + ?/${d}`, c, [`The numerators must add to ${n}: ${n} − ${a} − ${b} = ${c}.`]);
};
const fracTimesWhole = (word: boolean): Gen => (r) => {
  const n = r.int(2, 9), d = r.int(2, 10), a = r.int(1, d - 1);
  const v = q(n * a, d);
  const text = word ? `${n} people each eat ${m(`\\frac{${a}}{${d}}`)} pound of salad. How many pounds in all? (A fraction like 7/3 is fine.)` : `${m(`${n} \\times \\frac{${a}}{${d}} = \\;?`)}`;
  return value(text, `${n}*(${a}/${d})`, v, [`${m(`${n} \\times \\frac{${a}}{${d}} = \\frac{${n}\\times ${a}}{${d}} = ${qtex(v, true)}`)}.`]);
};
const hundredths: Gen = (r) => {
  const a = r.int(1, 9), b = r.int(1, 99);
  return box(`Fill in the box: ${m(`\\frac{${a}}{10} + \\frac{${b}}{100} = \\frac{\\square}{100}`)}`, `${a}/10 + ${b}/100 == ?/100`, 10 * a + b, [`${m(`\\frac{${a}}{10} = \\frac{${10 * a}}{100}`)}, then add hundredths.`]);
};
const fracToDec: Gen = (r) => {
  const n = r.int(1, 199);
  return box(`Fill in the box: ${m(`${dec(n, 2)} = \\frac{\\square}{100}`)}`, `${dec(n, 2)} == ?/100`, n, [`${dec(n, 2)} is ${n} hundredths.`]);
};
const fracAddUnlike = (word: boolean): Gen => (r) => {
  const d1 = r.int(2, 10), d2 = r.int(2, 12);
  require_(d1 !== d2 && lcm(d1, d2) <= 60);
  const mixed = r.chance(0.3);
  let a = q(r.int(1, mixed ? 3 * d1 : d1 - 1), d1), b = q(r.int(1, d2 - 1), d2);
  const add = r.chance(0.6);
  if (!add && a.sub(b).value() < 0) [a, b] = [b, a];
  require_(!a.isInt() && !b.isInt());
  const v = add ? a.add(b) : a.sub(b);
  const L = lcm(a.d, b.d);
  const nm = r.pick(NAMES);
  const text = word
    ? add ? `${nm} walks ${m(qtex(a, true))} km to the park and ${m(qtex(b, true))} km more to school. How far in all? (e.g. 17/12)` : `A ribbon is ${m(qtex(a, true))} m long. ${nm} cuts off ${m(qtex(b, true))} m. How much is left? (e.g. 5/12)`
    : `${m(`${qtex(a, true)} ${add ? "+" : "-"} ${qtex(b, true)} = \\;?`)} (e.g. 17/12)`;
  return value(text, `${a.n}/${a.d} ${add ? "+" : "-"} ${b.n}/${b.d}`, v,
    [`Common denominator ${L}: ${m(`\\frac{${a.n * (L / a.d)}}{${L}} ${add ? "+" : "-"} \\frac{${b.n * (L / b.d)}}{${L}} = ${v.tex()}`)}.`, `Benchmark check: compare each to ${m("\\tfrac12")} and 1.`]);
};
const fracAsDiv: Gen = (r) => {
  const p = r.int(2, 9), n = r.int(2, 12);
  require_(p % n !== 0);
  const v = q(p, n);
  return value(`${n} friends share ${p} pizzas equally. How much pizza does each get? (e.g. 7/3)`, `${p}/${n}`, v, [`Sharing ${p} among ${n} is ${m(`${p} \\div ${n} = \\frac{${p}}{${n}}`)}${v.value() > 1 ? ` ${m(`= ${qtex(v, true)}`)}` : ""}.`]);
};
const fracMult = (mixed: boolean): Gen => (r) => {
  const a = mixed ? q(r.int(5, 20), r.int(2, 4)) : q(r.int(1, 8), r.int(2, 9)), b = q(r.int(1, 9), r.int(2, 9));
  require_(a.n !== 0 && b.n !== 0 && !a.isInt() && !b.isInt());
  const v = a.mul(b);
  return value(`${m(`${qtex(a, mixed)} \\times ${qtex(b)} = \\;?`)}`, `(${a.n}/${a.d})*(${b.n}/${b.d})`, v,
    [mixed ? `Write the mixed number as ${m(a.tex())} first.` : `Multiply across.`, `${m(`\\frac{${a.n}\\times${b.n}}{${a.d}\\times${b.d}} = ${v.tex()}`)}.`]);
};
const fracArea: Gen = (r) => {
  const a = q(r.int(1, 11), r.int(2, 4)), b = q(r.int(1, 11), r.int(2, 6));
  require_(!a.isInt() || !b.isInt());
  const v = a.mul(b);
  return value(`A rectangle is ${m(qtex(a, true))} m by ${m(qtex(b, true))} m. What is its area in m²? (e.g. 15/8)`, `(${a.n}/${a.d})*(${b.n}/${b.d})`, v,
    [`Tile it with ${m(`\\frac1{${a.d}} \\times \\frac1{${b.d}}`)} squares: ${a.n} × ${b.n} of them, each ${m(`\\frac{1}{${a.d * b.d}}`)} m².`, `Area ${m(`= ${v.tex()}`)} m².`]);
};
const scaling: Gen = (r) => {
  const n = r.int(20, 999), f = r.chance(0.15) ? q(1) : q(r.int(1, 15), r.int(2, 9));
  const c = cmpOf(f.mul(n), q(n));
  const opts = [`greater than ${n}`, `less than ${n}`, `equal to ${n}`];
  const ans = opts[CMP.indexOf(c)];
  const ft = f.isInt() ? "1" : qtex(f);
  return draft(`Without multiplying: is ${m(`${ft} \\times ${n}`)} greater than, less than, or equal to ${m(`${n}`)}?`, choice(opts, ans), `\\text{${ans}}`,
    [`Multiplying by a factor ${f.value() > 1 ? "greater than 1 makes it bigger" : f.value() < 1 ? "less than 1 makes it smaller" : "of 1 leaves it the same"}.`], { mx: "scaling", n, f: `${f.n}/${f.d}` });
};
const unitFracDiv = (word: boolean): Gen => (r) => {
  const b = r.int(2, 9), n = r.int(2, 9), first = r.chance(0.5);
  const v = first ? q(1, b * n) : q(n * b);
  const py = first ? `(1/${b})/${n}` : `${n}/(1/${b})`;
  const text = word
    ? first ? `${m(`\\frac1{${b}}`)} lb of chocolate is shared equally by ${n} people. How much does each get?` : `How many ${m(`\\frac1{${b}}`)}-cup servings are in ${n} cups of raisins?`
    : `${m(first ? `\\frac1{${b}} \\div ${n} = \\;?` : `${n} \\div \\frac1{${b}} = \\;?`)}`;
  return value(text, py, v, [first ? `Check with multiplication: ${m(`\\frac{1}{${b * n}} \\times ${n} = \\frac1{${b}}`)}.` : `Each whole holds ${b} pieces of ${m(`\\frac1{${b}}`)}: ${m(`${n} \\times ${b} = ${n * b}`)}.`]);
};
const fracDiv: Gen = (r) => {
  const a = q(r.nz(1, 9), r.int(2, 9)), b = q(r.int(1, 9), r.int(2, 9));
  require_(!a.isInt() && !b.isInt());
  const v = a.div(b);
  return value(`${m(`${a.tex()} \\div ${b.tex()} = \\;?`)}`, `(${a.n}/${a.d})/(${b.n}/${b.d})`, v, [`Multiply by the reciprocal: ${m(`${a.tex()} \\times \\frac{${b.d}}{${b.n}} = ${v.tex()}`)}.`, `Check: ${m(`${v.tex()} \\times ${b.tex()} = ${a.tex()}`)}.`]);
};

// ── decimals ────────────────────────────────────────────────────────────────
const decOps = (big: boolean): Gen => (r) => {
  const op = r.int(0, 3);
  const pa = big ? r.int(1, 3) : 2, pb = big ? r.int(1, 2) : r.int(1, 2);
  let a = r.int(big ? 100 : 10, big ? 99999 : 999), b = r.int(big ? 10 : 1, big ? 9999 : 99);
  let A = q(a, 10 ** pa), B = q(b, 10 ** pb);
  if (op === 1 && A.sub(B).value() < 0) [A, B] = [B, A];
  if (op === 3) {
    // quotient built backward: terminating with at most 3 decimals
    const qt = q(r.int(2, big ? 9999 : 99), big ? 100 : 10);
    B = q(r.int(2, big ? 99 : 9), r.pick([1, 10]));
    A = qt.mul(B);
    require_([1, 10, 100, 1000, 10000].includes(A.d));
  }
  const v = [A.add(B), A.sub(B), A.mul(B), A.div(B)][op];
  const sym = ["+", "-", "\\times", "\\div"][op];
  const t = (x: Q) => decTexQ(x);
  const py = (x: Q) => decTexQ(x).replace(/\{,\}/g, "");
  return value(`${m(`${t(A)} ${sym} ${t(B)} = \\;?`)}`, `${py(A)} ${["+", "-", "*", "/"][op]} ${py(B)}`, v,
    [[`Line up the decimal points and add.`, `Line up the decimal points and subtract.`, `Multiply as whole numbers, then place the point: the answer has as many decimal places as both factors together.`, `Shift the point in both numbers until the divisor is whole, then divide.`][op], `${m(`= ${decTexQ(v)}`)}.`], decTexQ(v));
};
const decConvert: Gen = (r) => {
  const d = r.pick([3, 6, 7, 9, 11, 12, 13, 15, 8, 16, 20, 25, 40]), n = r.int(1, d - 1);
  require_(gcd(n, d) === 1);
  if (r.chance(0.5)) {
    let dd = d;
    for (const p of [2, 5]) while (dd % p === 0) dd /= p;
    const term = dd === 1;
    return draft(`Does the decimal for ${m(`\\frac{${n}}{${d}}`)} terminate or repeat?`, choice(["Terminates", "Repeats"], term ? "Terminates" : "Repeats"), `\\text{${term ? "Terminates" : "Repeats"}}`,
      [`In lowest terms, a fraction terminates exactly when the denominator has no prime factors other than 2 and 5. ${d} = ${factorTxt(d)}.`], { mx: "terminates", n, d });
  }
  const k = r.int(2, 5);
  let rem = n, digit = 0;
  for (let i = 0; i < k; i++) { rem *= 10; digit = Math.floor(rem / d); rem %= d; }
  return draft(`Use long division: what is digit number ${m(`${k}`)} after the decimal point in ${m(`\\frac{${n}}{${d}}`)}?`, exact(digit), `${digit}`,
    [`${m(`\\frac{${n}}{${d}} = ${(n / d).toFixed(k + 3)}\\ldots`)}`], { mx: "dec-digit", n, d, k });
};
function sciTex(v: number): string {
  const e = Math.floor(Math.log10(Math.abs(v)));
  return `${Number((v / 10 ** e).toPrecision(5))} \\times 10^{${e}}`;
}
function factorTxt(n: number) { const f: number[] = []; for (let p = 2; n > 1; p++) while (n % p === 0) { f.push(p); n /= p; } return f.join(" × "); }
const repeating: Gen = (r) => {
  const d = r.pick([9, 99, 3, 11, 33]), n = r.int(1, d - 1);
  const g = gcd(n, d), v = q(n, d);
  // block of the repeating decimal
  const len = d === 99 || d === 11 || d === 33 ? 2 : 1;
  require_((n * (10 ** len - 1)) % d === 0);
  const block = String((n * (10 ** len - 1)) / d).padStart(len, "0");
  return draft(`Write ${m(`0.\\overline{${block}}`)} as a fraction in lowest terms.`,
    tuple([{ label: "numerator", tex: "\\text{numerator}", ref: v.n }, { label: "denominator", tex: "\\text{denominator}", ref: v.d }]), v.tex(),
    [`Let ${m(`x = 0.\\overline{${block}}`)}; then ${m(`${10 ** len}x - x = ${Number(block)}`)}, so ${m(`x = \\frac{${Number(block)}}{${10 ** len - 1}}`)}${g > 1 || (10 ** len - 1) !== d ? ` ${m(`= ${v.tex()}`)}` : ""}.`], { mx: "repeating", block });
};

// ── measurement & data ──────────────────────────────────────────────────────
const SHAPES: [string, string, number][] = [
  ["triangle", "sides", 3], ["square", "corners (vertices)", 4], ["rectangle", "sides", 4], ["pentagon", "sides", 5], ["hexagon", "vertices", 6],
  ["octagon", "sides", 8], ["cube", "faces", 6], ["cube", "edges", 12], ["cube", "vertices", 8], ["triangle", "vertices", 3], ["quadrilateral", "sides", 4], ["rectangular prism", "faces", 6],
];
const shapeAttr: Gen = (r) => {
  const [s, what, n] = r.pick(SHAPES);
  return draft(`How many ${what} does a ${s} have?`, exact(n), `${n}`, [`A ${s} has ${n} ${what}.`], { mx: "shape", s, what: what.split(" ")[0] });
};
const fmtTime = (h: number, mm: number) => `${((h + 11) % 12) + 1}:${String(mm).padStart(2, "0")}`;
const elapsed: Gen = (r) => {
  const h1 = r.int(7, 15), m1 = r.int(0, 59), dur = r.int(15, 200);
  const t2 = h1 * 60 + m1 + dur;
  require_(t2 < 22 * 60);
  const ap = (h: number) => (h < 12 ? "a.m." : "p.m.");
  return draft(`A movie starts at ${fmtTime(h1, m1)} ${ap(h1)} and ends at ${fmtTime(Math.floor(t2 / 60), t2 % 60)} ${ap(Math.floor(t2 / 60))} How many minutes long is it?`, exact(dur), `${dur}`,
    [`Count up to the next hour, then whole hours, then the leftover minutes: ${dur} minutes.`], { mx: "elapsed", h1, m1, h2: Math.floor(t2 / 60), m2: t2 % 60 });
};
const timeAfter = (stepMin: number): Gen => (r) => {
  const h = r.int(1, 11), mm = stepMin * r.int(0, 60 / stepMin - 1), add = stepMin * r.int(1, 120 / stepMin);
  const t = h * 60 + mm + add;
  const H = ((Math.floor(t / 60) + 11) % 12) + 1, M = t % 60;
  return draft(`It is ${fmtTime(h, mm)}. What time will it be in ${add} minutes? Give the hour (1–12) and the minutes.`,
    tuple([{ label: "hour", tex: "\\text{hour}", ref: H }, { label: "minutes", tex: "\\text{minutes}", ref: M }]), `${H}:${String(M).padStart(2, "0")}`,
    [`${add} minutes = ${Math.floor(add / 60)} h ${add % 60} min after ${fmtTime(h, mm)}.`], { mx: "time-after", h, mm, add });
};
const COINS: [string, number][] = [["quarters", 25], ["dimes", 10], ["nickels", 5], ["pennies", 1]];
const money: Gen = (r) => {
  const cnt = COINS.map(() => r.int(0, 4));
  const dollars = r.int(0, 2);
  require_(cnt.some((c) => c > 0));
  const txt = [dollars ? `${dollars} one-dollar bill${dollars > 1 ? "s" : ""}` : "", ...COINS.map(([nm], i) => (cnt[i] ? `${cnt[i]} ${cnt[i] === 1 ? nm.replace(/ies$/, "y").replace(/s$/, "") : nm}` : ""))].filter(Boolean).join(", ");
  const v = dollars * 100 + cnt.reduce((s, c, i) => s + c * COINS[i][1], 0);
  return draft(`How many cents is ${txt}?`, exact(v), `${v}\\text{ cents}`, [COINS.map(([nm, val], i) => (cnt[i] ? `${cnt[i]}×${val}¢` : "")).filter(Boolean).join(" + ") + (dollars ? ` + ${dollars * 100}¢` : "") + ` = ${v}¢.`], { mx: "money", cnt, dollars });
};
const UNITS: [string, string, number][] = [
  ["km", "m", 1000], ["m", "cm", 100], ["cm", "mm", 10], ["kg", "g", 1000], ["L", "mL", 1000], ["ft", "in", 12], ["yd", "ft", 3], ["lb", "oz", 16], ["h", "min", 60], ["min", "s", 60], ["gal", "qt", 4],
];
const convert = (downOnly: boolean): Gen => (r) => {
  const [big, small, f] = r.pick(UNITS);
  const down = downOnly || r.chance(0.5);
  if (down) {
    const x = downOnly ? q(r.int(2, 12)) : q(r.int(5, 95), r.pick([2, 4, 10]));
    require_(x.mul(f).isInt());
    return draft(`${m(`${decTexQ(x)}\\ \\text{${big}} = \\;?\\ \\text{${small}}`)}`, exact(x.mul(f)), `${decTexQ(x.mul(f))}\\ \\text{${small}}`, [`1 ${big} = ${f} ${small}, so multiply by ${f}.`], { mx: "convert", x: `${x.n}/${x.d}`, from: big, to: small });
  }
  const y = r.int(1, 40) * (f % 10 === 0 ? f / r.pick([2, 4, 10, 1]) : f / r.pick([1, 2]));
  require_(Number.isInteger(y) && y > 0);
  const v = q(y, f);
  return draft(`${m(`${int(y)}\\ \\text{${small}} = \\;?\\ \\text{${big}}`)} (a decimal or fraction)`, exact(v), `${decTexQ(v)}\\ \\text{${big}}`, [`${f} ${small} = 1 ${big}, so divide by ${f}.`], { mx: "convert", x: `${y}`, from: small, to: big });
};
const rectArea: Gen = (r) => {
  const l = r.int(2, 15), w = r.int(2, 12);
  return r.chance(0.6)
    ? draft(`A rectangle is ${l} cm long and ${w} cm wide. What is its area in cm²?`, exact(l * w), `${l * w}\\ \\text{cm}^2`, [`Rows of unit squares: ${m(`${l} \\times ${w} = ${l * w}`)}.`], { mx: "rect", l, w, ask: "area" })
    : draft(`A rectangle has area ${l * w} m² and length ${l} m. What is its width in m?`, exact(w), `${w}\\ \\text{m}`, [`${m(`${l} \\times w = ${l * w}`)}, so ${m(`w = ${w}`)}.`], { mx: "rect", l, A: l * w, ask: "width" });
};
const areaDistributive: Gen = (r) => {
  const a = r.int(2, 9), b = r.int(2, 9), c = r.int(2, 9);
  return box(`A rectangle ${a} by ${b + c} is split into a ${a} × ${b} piece and another piece. Fill in the box: ${m(`${a} \\times ${b + c} = ${a} \\times ${b} + ${a} \\times \\square`)}`, `${a}*${b + c} == ${a}*${b} + ${a}*?`, c, [`The other piece is ${a} by ${b + c} − ${b} = ${c}.`]);
};
const rectilinear: Gen = (r) => {
  const W = r.int(6, 14), H = r.int(5, 12), w = r.int(2, W - 2), h = r.int(2, H - 2);
  return draft(`An L-shaped room is a ${W} m by ${H} m rectangle with a ${w} m by ${h} m rectangle cut out of one corner. What is its area in m²?`, exact(W * H - w * h), `${W * H - w * h}\\ \\text{m}^2`,
    [`Whole rectangle minus the missing corner: ${m(`${W}\\times${H} - ${w}\\times${h} = ${W * H} - ${w * h} = ${W * H - w * h}`)}.`, `Or split it into two rectangles and add.`], { mx: "lshape", W, H, w, h });
};
const perimeter: Gen = (r) => {
  const l = r.int(2, 20), w = r.int(2, 15);
  return r.chance(0.5)
    ? draft(`What is the perimeter of a ${l} ft by ${w} ft rectangle?`, exact(2 * (l + w)), `${2 * (l + w)}\\ \\text{ft}`, [`Add all four sides: ${m(`${l} + ${w} + ${l} + ${w} = ${2 * (l + w)}`)}.`], { mx: "eq", eq: `? == ${l} + ${w} + ${l} + ${w}` })
    : box(`A rectangle has perimeter ${2 * (l + w)} ft and length ${l} ft. What is its width?`, `2*${l} + 2*? == ${2 * (l + w)}`, w, [`Two lengths use ${2 * l} ft; the two widths share ${2 * w} ft.`]);
};
const angleTurn: Gen = (r) => {
  const d = r.pick([2, 3, 4, 5, 6, 8, 9, 10, 12, 36]), n = r.int(1, d - 1);
  const v = q(360 * n, d);
  require_(v.isInt());
  return draft(`An angle turns through ${m(`\\frac{${n}}{${d}}`)} of a full circle. How many degrees is it?`, exact(v), `${v.n}^\\circ`, [`A full turn is 360°: ${m(`\\frac{${n}}{${d}} \\times 360 = ${v.n}`)}.`], { mx: "expr", e: `${n}*360/${d}` });
};
const angleAdd: Gen = (r) => {
  const whole = r.int(40, 175), a = r.int(10, whole - 10);
  return box(`Angle ${m("ABC")} measures ${whole}°. Ray ${m("BD")} splits it into ${m("\\angle ABD")} = ${a}° and ${m("\\angle DBC")}. Find ${m("\\angle DBC")} in degrees.`, `${a} + ? == ${whole}`, whole - a, [`Angle measure is additive: ${m(`${whole} - ${a} = ${whole - a}`)}.`]);
};
const angleType: Gen = (r) => {
  const a = r.chance(0.2) ? r.pick([90, 180]) : r.int(1, 179);
  const t = a < 90 ? "Acute" : a === 90 ? "Right" : a < 180 ? "Obtuse" : "Straight";
  return draft(`Classify an angle of ${a}°.`, choice(["Acute", "Right", "Obtuse", "Straight"], t), `\\text{${t}}`, [`Acute < 90° = right < obtuse < 180° = straight.`], { mx: "angle-type", a });
};
const SYM: [string, number][] = [["square", 4], ["rectangle (not a square)", 2], ["equilateral triangle", 3], ["isosceles triangle (not equilateral)", 1], ["regular pentagon", 5], ["regular hexagon", 6], ["parallelogram (not a rectangle or rhombus)", 0], ["rhombus (not a square)", 2], ["regular octagon", 8], ["scalene triangle", 0]];
const symmetryLines: Gen = (r) => {
  const [s, n] = r.pick(SYM);
  return draft(`How many lines of symmetry does a ${s} have?`, exact(n), `${n}`, [`Fold lines that match the two halves exactly: ${n}.`], { mx: "sym-lines", s });
};
const HIER: [string, string, boolean][] = [
  ["square", "rectangle", true], ["square", "rhombus", true], ["rectangle", "square", false], ["rhombus", "parallelogram", true], ["parallelogram", "rectangle", false],
  ["rectangle", "parallelogram", true], ["trapezoid (exactly one pair of parallel sides)", "parallelogram", false], ["square", "quadrilateral", true], ["rhombus", "square", false], ["equilateral triangle", "isosceles triangle", true], ["isosceles triangle", "equilateral triangle", false],
];
const hierarchy: Gen = (r) => {
  const [a, b, t] = r.pick(HIER);
  return draft(`True or false: every ${a} is a ${b.replace(/ \(.*\)/, "")}.`, choice(["True", "False"], t ? "True" : "False"), `\\text{${t ? "True" : "False"}}`, [`A ${a} ${t ? "has every defining property" : "need not have all the properties"} of a ${b.replace(/ \(.*\)/, "")}.`], { mx: "hier", a, b });
};
const volumePrism = (frac: boolean): Gen => (r) => {
  const l = frac ? q(r.int(1, 9), 2) : q(r.int(2, 12)), w = frac ? q(r.int(1, 9), r.pick([2, 4])) : q(r.int(2, 10)), h = frac ? q(r.int(1, 7), r.pick([2, 3])) : q(r.int(2, 10));
  require_(!frac || !(l.isInt() && w.isInt() && h.isInt()));
  const v = l.mul(w).mul(h);
  const t = (x: Q) => qtex(x, true);
  return draft(`A box (right rectangular prism) is ${m(t(l))} by ${m(t(w))} by ${m(t(h))} inches. What is its volume in cubic inches?${frac ? " (e.g. 45/8)" : ""}`, exact(v), `${v.tex()}\\ \\text{in}^3`,
    [`${m("V = lwh")}${frac ? `: pack it with ${m(`\\frac1{${lcm(lcm(l.d, w.d), h.d)}}`)}-inch cubes and count` : ""}: ${m(`${t(l)} \\times ${t(w)} \\times ${t(h)} = ${v.tex()}`)}.`], { mx: "box", dims: [l, w, h].map((x) => `${x.n}/${x.d}`) });
};
const volumeComposite: Gen = (r) => {
  const a = [r.int(2, 9), r.int(2, 9), r.int(2, 9)], b = [r.int(2, 9), r.int(2, 9), r.int(2, 9)];
  const v = a[0] * a[1] * a[2] + b[0] * b[1] * b[2];
  return draft(`A solid is made of two non-overlapping boxes, ${a.join(" × ")} cm and ${b.join(" × ")} cm. What is its volume in cm³?`, exact(v), `${v}\\ \\text{cm}^3`,
    [`Volume is additive: ${m(`${a[0] * a[1] * a[2]} + ${b[0] * b[1] * b[2]} = ${v}`)}.`], { mx: "two-boxes", a, b });
};
const dataGraph = (scaled: boolean): Gen => (r) => {
  const cats = shuffle(["red", "blue", "green", "yellow"], () => r.next()).slice(0, 3);
  const per = scaled ? r.pick([2, 5, 10]) : 1;
  const counts = cats.map(() => per * r.int(1, scaled ? 9 : 10));
  const ask = r.int(0, 1);
  const [i, j] = [0, 1].map(() => r.int(0, 2));
  require_(ask === 0 || i !== j);
  const desc = scaled ? `In a picture graph each ★ stands for ${per} votes: ${cats.map((c, k) => `${c} has ${counts[k] / per} ★`).join(", ")}.` : `Favourite colours: ${cats.map((c, k) => `${c} ${counts[k]}`).join(", ")}.`;
  const v = ask === 0 ? counts.reduce((a, b) => a + b, 0) : Math.abs(counts[i] - counts[j]);
  const qtxt = ask === 0 ? "How many votes in all?" : `How many more votes did ${counts[i] >= counts[j] ? cats[i] : cats[j]} get than ${counts[i] >= counts[j] ? cats[j] : cats[i]}?`;
  return draft(`${desc} ${qtxt}`, exact(v), `${v}`, [scaled ? `Votes = stars × ${per}: ${counts.join(", ")}.` : `Read each count.`, ask === 0 ? `${counts.join(" + ")} = ${v}.` : `Difference: ${v}.`], { mx: "graph", counts, ask, i, j });
};
const linePlot = (redistribute: boolean): Gen => (r) => {
  const d = r.pick([2, 4, 8]);
  const xs = Array.from({ length: r.int(5, 8) }, () => q(r.int(1, 2 * d), d)).sort((a, b) => a.value() - b.value());
  const tot = xs.reduce((s, x) => s.add(x), q(0));
  const v = redistribute ? tot.div(xs.length) : xs[xs.length - 1].sub(xs[0]);
  require_(!v.isZero());
  return draft(`A line plot shows these lengths in inches: ${m(xs.map((x) => qtex(x, true)).join(",\\ "))}. ${redistribute ? "If the total length were shared equally among the pieces, how long would each be?" : "How much longer is the longest than the shortest?"} (e.g. 5/8)`,
    exact(v), v.tex(), [redistribute ? `Total ${m(tot.tex())}, divided by ${xs.length}: ${m(v.tex())}.` : `${m(`${qtex(xs[xs.length - 1], true)} - ${qtex(xs[0], true)} = ${v.tex()}`)}.`], { mx: "lineplot", xs: xs.map((x) => `${x.n}/${x.d}`), redistribute });
};

// ── ratios, rates, percents ─────────────────────────────────────────────────
const ratioTable: Gen = (r) => {
  const a = r.int(2, 9), b = r.int(2, 9), k = r.int(2, 9);
  require_(a !== b);
  return draft(`A recipe uses ${a} cups of flour for every ${b} cups of sugar. How many cups of sugar go with ${a * k} cups of flour?`, exact(b * k), `${b * k}`,
    [`${a * k} is ${k} times ${a}, so scale the ratio ${a}:${b} by ${k}: ${a * k}:${b * k}.`], { mx: "ratio", a, b, x: a * k });
};
const unitRate: Gen = (r) => {
  const n = r.int(2, 12), per = q(r.int(25, 900), 100);
  const tot = per.mul(n);
  require_([1, 2, 4, 5, 10, 20, 25, 50, 100].includes(tot.d));
  return r.chance(0.5)
    ? draft(`${n} notebooks cost ${usd(decTexQ(tot))}. What is the price per notebook in dollars?`, exact(per), `\\text{\\textdollar}${decTexQ(per)}`, [`Unit rate: ${m(`${decTexQ(tot)} \\div ${n} = ${decTexQ(per)}`)} dollars per notebook.`], { mx: "expr", e: `${decTexQ(tot)}/${n}` })
    : draft(`A car travels ${int(60 * n)} km in ${n} hours at a constant speed. How far does it go in ${n + 3} hours?`, exact(60 * (n + 3)), `${60 * (n + 3)}\\ \\text{km}`, [`Speed ${m(`${60 * n} \\div ${n} = 60`)} km/h, so ${m(`60 \\times ${n + 3}`)}.`], { mx: "expr", e: `${60 * n}/${n}*${n + 3}` });
};
const percentOf: Gen = (r) => {
  const p = r.pick([5, 10, 12, 15, 20, 25, 30, 40, 45, 50, 60, 75, 80, 120]), w = r.int(2, 40) * 20;
  const part = (p * w) / 100;
  require_(Number.isInteger(part));
  return r.chance(0.5)
    ? draft(`What is ${p}% of ${w}?`, exact(part), `${part}`, [`${m(`\\frac{${p}}{100} \\times ${w} = ${part}`)}.`], { mx: "expr", e: `${p}/100*${w}` })
    : draft(`${part} is ${p}% of what number?`, exact(w), `${w}`, [`${m(`\\frac{${p}}{100}\\,w = ${part}`)}, so ${m(`w = ${part} \\times \\frac{100}{${p}} = ${w}`)}.`], { mx: "eq", eq: `${p}/100*? == ${part}` });
};
const unitRateFrac: Gen = (r) => {
  const a = q(r.int(1, 5), r.int(2, 4)), b = q(1, r.int(2, 8));
  const v = a.div(b);
  return draft(`Someone walks ${m(a.tex())} mile in ${m(b.tex())} hour. What is the speed in miles per hour?`, exact(v), `${qtex(v)}`, [`${m(`${a.tex()} \\div ${b.tex()} = ${a.tex()} \\times ${b.d} = ${qtex(v)}`)}.`], { mx: "expr", e: `(${a.n}/${a.d})/(${b.n}/${b.d})` });
};
const propTest: Gen = (r) => {
  const k = q(r.int(1, 12), r.pick([1, 2])), xs = [r.int(1, 4), r.int(5, 8), r.int(9, 12)];
  const prop = r.chance(0.5);
  const ys = xs.map((x) => k.mul(x));
  if (!prop) ys[r.int(0, 2)] = ys[r.int(0, 2)].add(r.nz(-3, 3));
  require_(ys.every((y) => y.value() > 0) && (prop || !ys.every((y, i) => y.div(xs[i]).sub(ys[0].div(xs[0])).isZero())));
  const isP = ys.every((y, i) => y.div(xs[i]).sub(ys[0].div(xs[0])).isZero());
  return draft(`Is ${m("y")} proportional to ${m("x")}? ${m(xs.map((x, i) => `(${x}, ${qtex(ys[i])})`).join(",\\ "))}`, choice(["Proportional", "Not proportional"], isP ? "Proportional" : "Not proportional"), `\\text{${isP ? "Proportional" : "Not proportional"}}`,
    [`Ratios ${m("y/x")}: ${m(xs.map((x, i) => qtex(ys[i].div(x))).join(",\\ "))} — ${isP ? "all equal" : "not all equal"}.`], { mx: "prop", xs, ys: ys.map((y) => `${y.n}/${y.d}`) });
};
const propK: Gen = (r) => {
  const k = q(r.int(1, 20), r.pick([1, 2, 4])), x1 = r.int(2, 9);
  return r.chance(0.5)
    ? draft(`${m("y")} is proportional to ${m("x")}, and ${m(`y = ${qtex(k.mul(x1))}`)} when ${m(`x = ${x1}`)}. What is the constant of proportionality ${m("k")} in ${m("y = kx")}?`, exact(k), qtex(k), [`${m(`k = y/x = ${qtex(k.mul(x1))} / ${x1} = ${qtex(k)}`)}.`], { mx: "eq", eq: `? * ${x1} == ${qpy(k.mul(x1))}` })
    : draft(`Pens cost the same each: ${x1} pens cost ${usd(decTexQ(k.mul(x1)))}. Write ${m("t = pn")}; what is ${m("t")} for ${m(`n = ${x1 + 5}`)}?`, exact(k.mul(x1 + 5)), decTexQ(k.mul(x1 + 5)), [`${m(`p = ${decTexQ(k)}`)}, so ${m(`t = ${decTexQ(k)} \\times ${x1 + 5}`)}.`], { mx: "expr", e: `${qpy(k.mul(x1))}/${x1}*${x1 + 5}` });
};
const percentChange: Gen = (r) => {
  const t = r.int(0, 4), p = r.pick([5, 10, 15, 20, 25, 30, 40, 50]), base = 20 * r.int(1, 30);
  const nm = ["sales tax", "tip", "discount", "markup", "change"][t];
  if (t === 4) {
    const b2 = base * (100 + (r.chance(0.5) ? p : -p)) / 100;
    const ch = q(100 * (b2 - base), base);
    return draft(`A price changes from ${usd(base)} to ${usd(b2)}. What is the percent change? (negative for a decrease)`, exact(ch), `${qtex(ch)}\\%`, [`${m(`\\frac{${b2} - ${base}}{${base}} \\times 100 = ${qtex(ch)}\\%`)}.`], { mx: "expr", e: `(${b2}-${base})/${base}*100` });
  }
  const up = t !== 2;
  const v = q(base * (100 + (up ? p : -p)), 100);
  return draft(`An item costs ${usd(base)}. With a ${p}% ${nm}, what is the final amount in dollars?`, exact(v), `\\text{\\textdollar}${decTexQ(v)}`, [`${up ? "Add" : "Subtract"} ${p}%: ${m(`${base} \\times ${up ? 1 + p / 100 : 1 - p / 100} = ${decTexQ(v)}`)}.`], { mx: "expr", e: `${base}*(1 ${up ? "+" : "-"} ${p}/100)` });
};
const scaleDrawing: Gen = (r) => {
  const s = r.pick([2, 4, 5, 10, 20, 50]), l = q(r.int(5, 60), 2), w = q(r.int(4, 40), 2);
  const area = r.chance(0.4);
  return area
    ? draft(`On a scale drawing 1 cm represents ${s} m. A room is ${decTexQ(l)} cm by ${decTexQ(w)} cm on the drawing. What is its actual area in m²?`, exact(l.mul(s).mul(w.mul(s))), decTexQ(l.mul(w).mul(s * s)), [`Actual sides: ${decTexQ(l.mul(s))} m and ${decTexQ(w.mul(s))} m; area scales by ${s}² = ${s * s}.`], { mx: "expr", e: `(${qpy(l)}*${s})*(${qpy(w)}*${s})` })
    : draft(`On a scale drawing 1 cm represents ${s} m. A wall is ${decTexQ(l)} cm long on the drawing. How long is it in meters?`, exact(l.mul(s)), decTexQ(l.mul(s)), [`${m(`${decTexQ(l)} \\times ${s} = ${decTexQ(l.mul(s))}`)} m.`], { mx: "expr", e: `${qpy(l)}*${s}` });
};

// ── integers & rational numbers ─────────────────────────────────────────────
const opposite: Gen = (r) => {
  const a = r.nz(-30, 30), k = r.int(1, 3);
  const v = k % 2 ? -a : a;
  const tex = `${"-(".repeat(k)}${a}${")".repeat(k)}`;
  return value(`Simplify ${m(tex)}.`, `${"-(".repeat(k)}${a}${")".repeat(k)}`, v, [`Each minus sign takes the opposite (reflects across 0); ${k} of them ${k % 2 ? "flip" : "cancel"}.`]);
};
const absVal: Gen = (r) => {
  const a = r.nz(-40, 40), b = r.nz(-40, 40), t = r.int(0, 1);
  return t === 0
    ? value(`${m(`|${a}| - |${b}| = \\;?`)}`, `abs(${a}) - abs(${b})`, Math.abs(a) - Math.abs(b), [`Absolute value is distance from 0: ${Math.abs(a)} and ${Math.abs(b)}.`])
    : draft(`How far apart are ${m(`${a}`)} and ${m(`${b}`)} on the number line?`, exact(Math.abs(a - b)), `${Math.abs(a - b)}`, [`Distance ${m(`= |${a} - ${par(b)}| = ${Math.abs(a - b)}`)}.`], { mx: "expr", e: `abs(${a} - (${b}))` });
};
const QUAD = ["I", "II", "III", "IV"];
const quadrant: Gen = (r) => {
  const x = r.nz(-9, 9), y = r.nz(-9, 9);
  if (r.chance(0.5)) {
    const qd = x > 0 ? (y > 0 ? "I" : "IV") : y > 0 ? "II" : "III";
    return draft(`Which quadrant contains the point ${m(`(${x}, ${y})`)}?`, choice(QUAD, qd), `\\text{${qd}}`, [`Signs (${x > 0 ? "+" : "−"}, ${y > 0 ? "+" : "−"}): quadrant ${qd} (I is (+, +), counting counterclockwise).`], { mx: "quadrant", x, y });
  }
  const ax = r.pick(["x", "y"]);
  const [X, Y] = ax === "x" ? [x, -y] : [-x, y];
  return draft(`Reflect ${m(`(${x}, ${y})`)} across the ${ax}-axis. What are the coordinates of the image?`, tuple([{ label: "x", tex: "x", ref: X }, { label: "y", tex: "y", ref: Y }]), `(${X}, ${Y})`, [`Reflecting across the ${ax}-axis flips the sign of the ${ax === "x" ? "y" : "x"}-coordinate.`], { mx: "reflect", x, y, ax });
};
const plotQ1: Gen = (r) => {
  const x = r.int(0, 10), y = r.int(0, 10);
  return draft(`Start at the origin, move ${x} units right and ${y} units up. What ordered pair names the point?`, tuple([{ label: "x", tex: "x", ref: x }, { label: "y", tex: "y", ref: y }]), `(${x}, ${y})`, [`The first coordinate is the distance along the x-axis, the second along the y-axis.`], { mx: "exprs", es: [`${x}`, `${y}`] });
};
const coordDist: Gen = (r) => {
  const a = r.nz(-9, 9), b = r.nz(-9, 9), c = r.nz(-9, 9);
  require_(a !== b);
  const same = r.chance(0.5);
  const [P1, P2] = same ? [`(${a}, ${c})`, `(${b}, ${c})`] : [`(${c}, ${a})`, `(${c}, ${b})`];
  return draft(`What is the distance between ${m(P1)} and ${m(P2)}?`, exact(Math.abs(a - b)), `${Math.abs(a - b)}`, [`They share a coordinate, so the distance is ${m(`|${a} - ${par(b)}| = ${Math.abs(a - b)}`)}.`], { mx: "dist", p: same ? [a, c] : [c, a], q: same ? [b, c] : [c, b] });
};
const intOps = (ops: number[]): Gen => (r) => {
  const op = r.pick(ops);
  let a = r.nz(-20, 20), b = r.nz(-20, 20);
  if (op === 3) { b = r.nz(-9, 9); a = b * r.nz(-12, 12); }
  require_(a < 0 || b < 0);
  const v = [a + b, a - b, a * b, a / b][op];
  const sym = ["+", "-", "\\times", "\\div"][op];
  return value(`${m(`${a} ${sym} ${par(b)} = \\;?`)}`, `(${a}) ${["+", "-", "*", "/"][op]} (${b})`, v,
    [[`Different signs: subtract the absolute values and keep the sign of the larger; same signs: add and keep the sign.`, `Subtracting is adding the opposite: ${m(`${a} + ${par(-b)}`)}.`, `Same signs give a positive product, different signs a negative one.`, `Same signs give a positive quotient, different signs a negative one.`][op]]);
};
const rationalOps: Gen = (r) => {
  const mk = () => (r.chance(0.5) ? q(r.nz(-50, 50), 10) : q(r.nz(-9, 9), r.int(2, 6)));
  const a = mk(), b = mk(), c = mk();
  const op = r.int(0, 2);
  const t = (x: Q) => (x.d === 10 || x.d === 5 || x.d === 2 ? dec(Math.round(x.value() * 10), 1) : x.tex());
  const forms: [string, string, Q][] = [
    [`${t(a)} - ${par(t(b))} + ${par(t(c))}`, `(${qpy(a)}) - (${qpy(b)}) + (${qpy(c)})`, a.sub(b).add(c)],
    [`${t(a)} \\times ${par(t(b))}`, `(${qpy(a)})*(${qpy(b)})`, a.mul(b)],
    [`(${t(a)} + ${par(t(b))}) \\div ${par(t(c))}`, `((${qpy(a)}) + (${qpy(b)}))/(${qpy(c)})`, c.isZero() ? q(0) : a.add(b).div(c)],
  ];
  const [tex, py, v] = forms[op];
  require_(!c.isZero() && v.d <= 100);
  return value(`${m(`${tex} = \\;?`)} (a fraction or decimal)`, py, v, [`Convert to one form (fractions are safest), apply the sign rules, simplify.`, `${m(`= ${qtex(v)}`)}.`]);
};
const gcfLcm: Gen = (r) => {
  const t = r.int(0, 2);
  if (t === 1) {
    const a = r.int(2, 12), b = r.int(2, 12);
    require_(a !== b);
    return draft(`What is the least common multiple of ${a} and ${b}?`, exact(lcm(a, b)), `${lcm(a, b)}`, [`Multiples of ${Math.max(a, b)} until one is a multiple of ${Math.min(a, b)}: ${lcm(a, b)}.`], { mx: "lcm", a, b });
  }
  const g = r.int(2, 12), x = r.int(1, 9), y = r.int(1, 9);
  require_(gcd(x, y) === 1 && x !== y && g * Math.max(x, y) <= 100);
  if (t === 0) return draft(`What is the greatest common factor of ${g * x} and ${g * y}?`, exact(g), `${g}`, [`${g * x} = ${g} × ${x} and ${g * y} = ${g} × ${y}, and ${x}, ${y} share no factor.`], { mx: "gcf", a: g * x, b: g * y });
  return box(`Factor out the greatest common factor: ${m(`${g * x} + ${g * y} = \\square\\,(${x} + ${y})`)}`, `${g * x} + ${g * y} == ?*(${x} + ${y})`, g, [`GCF(${g * x}, ${g * y}) = ${g}.`]);
};

// ── expressions & equations ─────────────────────────────────────────────────
const evaluate: Gen = (r) => {
  const x = r.nz(-5, 6), y = r.nz(-4, 5), a = r.nz(-6, 6), b = r.nz(-9, 9), c = r.int(1, 9);
  const forms: [string, string][] = [
    [`${cx(a, "x^2")}${sg(b, "y")}${sg(c)}`, `${a}*x**2 + ${b}*y + ${c}`],
    [`\\frac{${c}x + ${Math.abs(y)}}{2} - ${par(a)}y`, `(${c}*x + ${Math.abs(y)})/2 - (${a})*y`],
    [`6s^2 \\text{ for } s = ${Math.abs(x)}`, `6*${Math.abs(x)}**2`],
    [`${c}(x - y)^2`, `${c}*(x - y)**2`],
  ];
  const k = r.int(0, 3);
  const [tex, py] = forms[k];
  const v = Function("x", "y", `return ${py}`)(x, y) as number;
  require_(Number.isInteger(v * 2));
  return draft(k === 2 ? `The surface area of a cube is ${m("A = 6s^2")}. Find ${m("A")} for ${m(`s = ${Math.abs(x)}`)}.` : `Evaluate ${m(tex)} for ${m(`x = ${x},\\ y = ${y}`)}.`,
    exact(q(v * 2, 2)), qtex(q(v * 2, 2)), [`Substitute, then follow the order of operations (exponents before multiplication).`], { mx: "expr", e: py.replace(/\bx\b/g, `(${x})`).replace(/\by\b/g, `(${y})`) });
};
const equivForm = (rational: boolean): Gen => (r) => {
  const mk = () => (rational ? q(r.nz(-9, 9), r.pick([1, 2, 4])) : q(r.nz(-6, 9)));
  const a = mk(), b = mk(), c = mk(), d = mk();
  // a(bx + c) + dx  ->  (ab + d)x + ac
  const A = a.mul(b).add(d), B = a.mul(c);
  require_(!A.isZero());
  const t = (x: Q) => (rational && x.d !== 1 ? (x.d === 2 || x.d === 4 ? decTexQ(x) : x.tex()) : x.tex());
  return draft(`Write ${m(`${t(a)}(${cx(b, "x")}${sg(c)})${sg(d, "x")}`)} in the form ${m("ax + b")}. Give ${m("a")} and ${m("b")}.`,
    tuple([{ label: "a", tex: "a", ref: A }, { label: "b", tex: "b", ref: B }]), `${poly([A, B])}`,
    [`Distribute: ${m(`${cx(a.mul(b), "x")}${sg(a.mul(c))}${sg(d, "x")}`)}; combine like terms: ${m(poly([A, B]))}.`], { mx: "lin-form", e: `(${qpy(a)})*((${qpy(b)})*x + (${qpy(c)})) + (${qpy(d)})*x` });
};
const equivCheck: Gen = (r) => {
  const a = r.int(2, 6), b = r.int(1, 9), c = r.int(1, 4);
  const pairs: [string, string, string, string][] = [
    [`${a}(x + ${b})`, `${a}x + ${a * b}`, `${a}*(x + ${b})`, `${a}*x + ${a * b}`],
    [`${a}(x + ${b})`, `${a}x + ${b}`, `${a}*(x + ${b})`, `${a}*x + ${b}`],
    [`x + x + x`, `3x`, `x + x + x`, `3*x`],
    [`${c}x + ${b}x`, `${c + b}x^2`, `${c}*x + ${b}*x`, `${c + b}*x**2`],
    [`${a * c}x + ${a * b}`, `${a}(${c}x + ${b})`, `${a * c}*x + ${a * b}`, `${a}*(${c}*x + ${b})`],
    [`(x + ${b})^2`, `x^2 + ${b * b}`, `(x + ${b})**2`, `x**2 + ${b * b}`],
  ];
  const [l, rr, lp, rp] = r.pick(pairs);
  const same = [1, 2, 3, 4, 5, 6].every((x) => Function("x", `return (${lp}) - (${rp})`)(x) === 0);
  return draft(`Are ${m(l)} and ${m(rr)} equivalent expressions?`, choice(["Equivalent", "Not equivalent"], same ? "Equivalent" : "Not equivalent"), `\\text{${same ? "Equivalent" : "Not equivalent"}}`,
    [same ? `They agree for every value of ${m("x")} (properties of operations turn one into the other).` : `Try ${m("x = 1")}: they give different numbers.`], { mx: "equiv", l: lp, r: rp });
};
const coefficient: Gen = (r) => {
  const cs = [r.nz(-9, 9), r.nz(-9, 9), r.int(-9, 9)];
  const t = r.int(0, 2);
  const what = ["the coefficient of " + "$x^2$", "the coefficient of $x$", "the constant term"][t];
  return draft(`In ${m(poly(cs))}, what is ${what}?`, exact(cs[t]), `${cs[t]}`, [`Read the number multiplying each power (with its sign).`], { mx: "coef", e: polyPy(cs), p: 2 - t });
};
const percentExpr: Gen = (r) => {
  const p = r.int(1, 40), up = r.chance(0.5);
  const v = q(100 + (up ? p : -p), 100);
  return box(`${up ? "Increasing" : "Decreasing"} a quantity ${m("a")} by ${p}% gives ${m(`a ${up ? "+" : "-"} ${dec(p, 2)}a`)}. Fill in the box: ${m(`a ${up ? "+" : "-"} ${dec(p, 2)}a = \\square\\,a`)}`, `7 ${up ? "+" : "-"} ${dec(p, 2)}*7 == ?*7`, v, [`Factor out ${m("a")}: ${m(`(1 ${up ? "+" : "-"} ${dec(p, 2)})a = ${decTexQ(v)}a`)}.`]);
};
const oneStep: Gen = (r) => {
  const x = q(r.int(1, 60), r.pick([1, 1, 2, 4, 10])), p = q(r.int(1, 40), r.pick([1, 2, 4, 10]));
  const add = r.chance(0.5);
  const t = (z: Q) => (z.isInt() ? z.tex() : decTexQ(z));
  return add
    ? draft(`Solve ${m(`x + ${t(p)} = ${t(x.add(p))}`)}.`, exact(x), `x = ${t(x)}`, [`Subtract ${t(p)} from both sides.`], { mx: "solve", eq: `x + ${qpy(p)} - (${qpy(x.add(p))})` })
    : draft(`Solve ${m(`${t(p)}x = ${t(x.mul(p))}`)}.`, exact(x), `x = ${t(x)}`, [`Divide both sides by ${t(p)}.`], { mx: "solve", eq: `${qpy(p)}*x - (${qpy(x.mul(p))})` });
};
const solutionCheck: Gen = (r) => {
  const x = r.int(1, 9), a = r.int(2, 7), b = r.int(1, 15);
  const opts = shuffle([x, x + 1, x - 1, x + 2].filter((v) => v >= 0), () => r.next()).map(String);
  require_(opts.length === 4);
  return draft(`Which value of ${m("x")} makes ${m(`${a}x + ${b} = ${a * x + b}`)} true?`, choice(opts, `${x}`), `x = ${x}`, [`Substitute each: ${m(`${a}(${x}) + ${b} = ${a * x + b}`)} ✓.`], { mx: "which-solves", eq: `${a}*x + ${b} - ${a * x + b}` });
};
const PHRASES: [string, string][] = [["at least", "≥"], ["at most", "≤"], ["more than", ">"], ["fewer than", "<"], ["no more than", "≤"], ["no fewer than", "≥"]];
const ineqPhrase: Gen = (r) => {
  const [ph, rel] = r.pick(PHRASES), c = r.int(3, 90);
  const opts = ["≥", "≤", ">", "<"].map((s) => `x ${s} ${c}`);
  return draft(`A ride needs ${ph} ${c} people (${m("x")} people). Which inequality says that?`, choice(opts, `x ${rel} ${c}`), `x ${rel === "≥" ? "\\ge" : rel === "≤" ? "\\le" : rel} ${c}`,
    [`"${ph}" ${rel === "≥" || rel === "≤" ? "includes" : "excludes"} ${c} itself.`], { mx: "phrase", ph, c });
};
const twoStep: Gen = (r) => {
  const x = q(r.nz(-12, 12), r.pick([1, 1, 2, 3])), p = q(r.nz(-9, 9), r.pick([1, 1, 2, 4])), qq = r.nz(-15, 15);
  const paren = r.chance(0.4);
  const rhs = paren ? p.mul(x.add(qq)) : p.mul(x).add(qq);
  const t = (z: Q) => z.tex();
  const tex = paren ? `${t(p)}(x ${qq < 0 ? "-" : "+"} ${Math.abs(qq)}) = ${t(rhs)}` : `${cx(p, "x")}${sg(qq)} = ${t(rhs)}`;
  return draft(`Solve ${m(tex)}. (A fraction is fine.)`, exact(x), `x = ${t(x)}`, [paren ? `Divide by ${m(t(p))}, then subtract ${qq}.` : `Subtract ${qq}, then divide by ${m(t(p))}.`, `${m(`x = ${t(x)}`)}.`], { mx: "solve", eq: paren ? `(${qpy(p)})*(x + (${qq})) - (${qpy(rhs)})` : `(${qpy(p)})*x + (${qq}) - (${qpy(rhs)})` });
};
const twoStepIneq: Gen = (r) => {
  const p = r.nz(-6, 6), qq = r.nz(-12, 12), b = r.nz(-10, 10), gt = r.chance(0.5);
  const rhs = p * b + qq;
  const flip = p < 0;
  const relX = gt !== flip ? ">" : "<";
  const opts = [`x > ${b}`, `x < ${b}`, `x > ${-b}`, `x < ${-b}`];
  return draft(`Solve ${m(`${cx(p, "x")}${sg(qq)} ${gt ? ">" : "<"} ${rhs}`)}.`, choice(opts, `x ${relX} ${b}`), `x ${relX} ${b}`,
    [`Subtract ${qq}: ${m(`${cx(p, "x")} ${gt ? ">" : "<"} ${rhs - qq}`)}.`, `Divide by ${p}${flip ? " — negative, so the inequality flips" : ""}: ${m(`x ${relX} ${b}`)}.`], { mx: "ineq", e: `${p}*x + ${qq}`, rel: gt ? ">" : "<", rhs });
};
const dependent: Gen = (r) => {
  const k = r.int(20, 80), t = q(r.int(1, 20), 2);
  return draft(`A train's distance is ${m(`d = ${k}t`)} (miles, hours). How far does it go in ${m(`t = ${decTexQ(t)}`)} hours?`, exact(t.mul(k)), decTexQ(t.mul(k)), [`${m(`d = ${k} \\times ${decTexQ(t)} = ${decTexQ(t.mul(k))}`)}.`], { mx: "expr", e: `${k}*${qpy(t)}` });
};

// ── grade 8 ─────────────────────────────────────────────────────────────────
const intExponents: Gen = (r) => {
  const b = r.pick([2, 3, 5, 10]), m1 = r.int(-5, 5), m2 = r.int(-5, 5), k = r.int(2, 3);
  const t = r.int(0, 2);
  const [tex, py, e] = [
    [`${b}^{${m1}} \\times ${b}^{${m2}}`, `${b}**(${m1}) * ${b}**(${m2})`, m1 + m2],
    [`\\frac{${b}^{${m1}}}{${b}^{${m2}}}`, `${b}**(${m1}) / ${b}**(${m2})`, m1 - m2],
    [`(${b}^{${m1}})^{${k}}`, `(${b}**(${m1}))**${k}`, m1 * k],
  ][t] as [string, string, number];
  require_(Math.abs(e) <= 4 && (b !== 10 || Math.abs(e) <= 3) && b ** Math.abs(e) <= 1000);
  const v = e >= 0 ? q(b ** e) : q(1, b ** -e);
  return value(`${m(`${tex} = \\;?`)} (as a whole number or fraction)`, py, v, [`${["Same base: add exponents", "Same base: subtract exponents", "Power of a power: multiply exponents"][t]}: ${m(`${b}^{${e}} = ${qtex(v)}`)}.`]);
};
const roots: Gen = (r) => {
  const t = r.int(0, 3), n = r.int(2, 15), c = r.int(1, 6) * r.pick([1, -1]);
  const [tex, py, v] = [
    [`\\sqrt{${n * n}}`, `sqrt(${n * n})`, n],
    [`\\sqrt[3]{${c * c * c}}`, `cbrt(${c * c * c})`, c],
    [`x^2 = ${n * n},\\ x > 0`, `sqrt(${n * n})`, n],
    [`x^3 = ${c * c * c}`, `${c}`, c],
  ][t] as [string, string, number];
  return draft(t >= 2 ? `Solve ${m(tex)}.` : `Evaluate ${m(tex)}.`, exact(v), `${v}`, [`${t % 2 ? `${c}^3 = ${c * c * c}` : `${n}^2 = ${n * n}`}.`], t === 1 || t === 3 ? { mx: "eq", eq: `?**3 == ${c * c * c}` } : { mx: "eq", eq: `?**2 == ${n * n} and ? > 0` });
};
const sqrtBetween: Gen = (r) => {
  const n = r.int(2, 200);
  const s = Math.floor(Math.sqrt(n));
  require_(s * s !== n);
  return draft(`${m(`\\sqrt{${n}}`)} lies between two consecutive whole numbers. What is the smaller one?`, exact(s), `${s}`, [`${m(`${s}^2 = ${s * s} < ${n} < ${(s + 1) ** 2} = ${s + 1}^2`)}.`], { mx: "isqrt", n });
};
const sciNotation: Gen = (r) => {
  const a = r.int(11, 99) / 10, b = r.int(11, 99) / 10, e1 = r.int(-9, 9), e2 = r.int(-9, 9);
  const t = r.int(0, 2);
  const v = t === 0 ? a * b * 10 ** (e1 + e2) : (a / b) * 10 ** (e1 - e2);
  if (t === 2) {
    const k = r.int(2, 9), e = r.int(2, 8);
    return draft(`About how many times as large is ${m(`${k * 2} \\times 10^{${e + 3}}`)} as ${m(`2 \\times 10^{${e}}`)}?`, approx(k * 1000, 1e-6), `${int(k * 1000)}`, [`${m(`\\frac{${2 * k}}{2} \\times 10^{${e + 3} - ${e}} = ${k} \\times 10^3`)}.`], { mx: "expr", e: `(${2 * k}*10**${e + 3})/(2*10**${e})` });
  }
  return draft(`${m(`(${a} \\times 10^{${e1}}) ${t === 0 ? "\\times" : "\\div"} (${b} \\times 10^{${e2}}) = \\;?`)} (e.g. 3.6e-4 or 3.6 x 10^-4)`, approx(v, 1e-6), sciTex(v),
    [`${t === 0 ? "Multiply" : "Divide"} the numbers and ${t === 0 ? "add" : "subtract"} the exponents, then renormalise to one digit before the point.`], { mx: "expr", e: `(${a}*10**(${e1})) ${t === 0 ? "*" : "/"} (${b}*10**(${e2}))` });
};
const linearEq: Gen = (r) => {
  const x = q(r.nz(-10, 10), r.pick([1, 1, 2, 3])), a = r.nz(-6, 6), b = r.nz(-9, 9), c = r.nz(-5, 5), d = r.nz(-6, 6);
  require_(a + c !== d);
  // a(x + b) + c x = d x + e
  const e = x.mul(a + c - d).add(a * b);
  return draft(`Solve ${m(`${a}(x ${b < 0 ? "-" : "+"} ${Math.abs(b)})${sg(c, "x")} = ${cx(d, "x")}${sg(e)}`)}. (A fraction is fine.)`, exact(x), `x = ${x.tex()}`,
    [`Distribute and collect: ${m(`${cx(a + c, "x")}${sg(a * b)} = ${cx(d, "x")}${sg(e)}`)}.`, `${m(`${cx(a + c - d, "x")} = ${e.sub(a * b).tex()}`)}, so ${m(`x = ${x.tex()}`)}.`], { mx: "solve", eq: `(${a})*(x + (${b})) + (${c})*x - ((${d})*x + (${qpy(e)}))` });
};
const SOLN = ["One solution", "No solution", "Infinitely many solutions"];
const eqCount: Gen = (r) => {
  const a = r.nz(-6, 6), b = r.nz(-9, 9), k = r.int(0, 2);
  const c = k === 0 ? a + r.nz(-3, 3) : a, d = k === 2 ? b : b + r.nz(-5, 5);
  const ans = c !== a ? SOLN[0] : d === b ? SOLN[2] : SOLN[1];
  return draft(`How many solutions does ${m(`${cx(a, "x")}${sg(b)} = ${cx(c, "x")}${sg(d)}`)} have?`, choice(SOLN, ans), `\\text{${ans}}`,
    [c !== a ? `The ${m("x")}-terms differ, so it reduces to ${m("x = a")}.` : d === b ? `Both sides are identical: ${m("a = a")}.` : `The ${m("x")}-terms cancel and leave ${m(`${b} = ${d}`)}, false.`], { mx: "nsol", l: `${a}*x + ${b}`, r: `${c}*x + ${d}` });
};
const system = (word: boolean): Gen => (r) => {
  if (word) {
    const pa = r.int(6, 15), pc = r.int(2, pa - 2), A = r.int(5, 60), C = r.int(5, 60);
    return draft(`A show sold ${A + C} tickets for ${usd(pa * A + pc * C)}. Adult tickets cost ${usd(pa)} and child tickets ${usd(pc)}. How many of each were sold?`,
      tuple([{ label: "adults", tex: "a", ref: A }, { label: "children", tex: "c", ref: C }]), `a = ${A},\\ c = ${C}`,
      [`${m(`a + c = ${A + C}`)} and ${m(`${pa}a + ${pc}c = ${pa * A + pc * C}`)}.`, `Substitute ${m(`c = ${A + C} - a`)}: ${m(`${pa - pc}a = ${pa * A + pc * C - pc * (A + C)}`)}, so ${m(`a = ${A}`)}.`], { mx: "tickets", n: A + C, total: pa * A + pc * C, pa, pc });
  }
  const x = r.int(-8, 8), y = r.int(-8, 8), a = r.nz(-5, 5), b = r.nz(-5, 5), c = r.nz(-5, 5), d = r.nz(-5, 5);
  require_(a * d - b * c !== 0);
  return draft(`Solve the system ${m(`\\begin{aligned} ${cx(a, "x")}${sg(b, "y")} &= ${a * x + b * y} \\\\ ${cx(c, "x")}${sg(d, "y")} &= ${c * x + d * y} \\end{aligned}`)}`,
    tuple([{ label: "x", tex: "x", ref: x }, { label: "y", tex: "y", ref: y }]), `(${x}, ${y})`,
    [`Eliminate one variable (multiply to match coefficients, then add or subtract), solve, back-substitute.`, `Check in both: ${m(`(${x}, ${y})`)} is where the lines cross.`], { mx: "system", rows: [[a, b, a * x + b * y], [c, d, c * x + d * y]] });
};
const slope = (withIntercept: boolean): Gen => (r) => {
  const mm = q(r.nz(-6, 6), r.pick([1, 1, 2, 3])), b = r.int(-9, 9), x1 = r.int(-6, 6), dx = r.nz(-5, 5) * mm.d;
  const x2 = x1 + dx, y1 = mm.mul(x1).add(b), y2 = mm.mul(x2).add(b);
  require_(y1.isInt() && y2.isInt());
  return withIntercept
    ? draft(`A linear function passes through ${m(`(${x1}, ${y1.n})`)} and ${m(`(${x2}, ${y2.n})`)}. Find its rate of change ${m("m")} and initial value ${m("b")} in ${m("y = mx + b")}.`,
      tuple([{ label: "m", tex: "m", ref: mm }, { label: "b", tex: "b", ref: b }]), `y = ${poly([mm, b])}`, [`${m(`m = \\frac{${y2.n} - ${par(y1.n)}}{${x2} - ${par(x1)}} = ${mm.tex()}`)}; ${m(`b = y_1 - m x_1 = ${b}`)}.`], { mx: "line", p: [x1, y1.n], q: [x2, y2.n] })
    : draft(`What is the slope of the line through ${m(`(${x1}, ${y1.n})`)} and ${m(`(${x2}, ${y2.n})`)}?`, exact(mm), mm.tex(), [`${m(`m = \\frac{\\Delta y}{\\Delta x} = \\frac{${y2.n - y1.n}}{${dx}} = ${mm.tex()}`)}.`], { mx: "slope", p: [x1, y1.n], q: [x2, y2.n] });
};
const isFunction: Gen = (r) => {
  const xs = shuffle([1, 2, 3, 4, 5, 6, 7], () => r.next()).slice(0, 4);
  const fn = r.chance(0.5);
  if (!fn) xs[3] = xs[r.int(0, 2)];
  const pairs = xs.map((x) => [x, r.int(-5, 9)]);
  require_(fn || pairs[3][1] !== pairs[xs.indexOf(xs[3])][1]);
  return draft(`Is the relation ${m(`\\{${pairs.map(([x, y]) => `(${x}, ${y})`).join(",\\ ")}\\}`)} a function of ${m("x")}?`, choice(["Function", "Not a function"], fn ? "Function" : "Not a function"), `\\text{${fn ? "Function" : "Not a function"}}`,
    [fn ? `Every input appears once, so each has exactly one output.` : `The input ${xs[3]} has two different outputs.`], { mx: "is-fn", pairs });
};
const linearOrNot: Gen = (r) => {
  const a = r.nz(-5, 5), b = r.int(-9, 9);
  const forms: [string, string, boolean][] = [[`y = ${cx(a, "x")}${sg(b)}`, `${a}*x + ${b}`, true], [`y = ${cx(a, "x^2")}${sg(b)}`, `${a}*x**2 + ${b}`, false], [`y = \\frac{${a}}{x}`, `${a}/x`, false], [`y = ${b}`, `${b}`, true], [`A = s^2`, `x**2`, false], [`y = ${a}(x${sg(b)})`, `${a}*(x + ${b})`, true]];
  const [tex, py, lin] = r.pick(forms);
  return draft(`Is ${m(tex)} a linear function?`, choice(["Linear", "Not linear"], lin ? "Linear" : "Not linear"), `\\text{${lin ? "Linear" : "Not linear"}}`,
    [lin ? `It has the form ${m("y = mx + b")}: equal steps in x give equal steps in y.` : `Equal steps in the input don't give equal steps in the output.`], { mx: "linear", e: py });
};
const compareFns: Gen = (r) => {
  const m1 = r.nz(-6, 6), b1 = r.int(-5, 5), m2 = r.nz(-6, 6), b2 = r.int(-5, 9);
  const xs = [0, 1, 2, 3];
  return draft(`${m(`f(x) = ${poly([m1, b1])}`)}. A table for the linear function ${m("g")}: ${m(xs.map((x) => `(${x}, ${m2 * x + b2})`).join(",\\ "))}. Which has the greater rate of change?`,
    choice(["f", "g", "Same"], m1 === m2 ? "Same" : m1 > m2 ? "f" : "g"), `\\text{${m1 === m2 ? "Same" : m1 > m2 ? "f" : "g"}}`,
    [`f has slope ${m1}; g rises ${m2} per step in x.`], { mx: "cmp-rate", f: m1, pts: xs.map((x) => [x, m2 * x + b2]) });
};

// ── geometry ────────────────────────────────────────────────────────────────
const areaPoly: Gen = (r) => {
  const t = r.int(0, 3), b = r.int(2, 20), h = r.int(2, 15), b2 = r.int(1, 15), s = r.int(-5, 8);
  // vertices for the verifier (shoelace); the prompt gives base and height
  const shapes: [string, number[][], Q][] = [
    [`a triangle with base ${b} cm and height ${h} cm`, [[0, 0], [b, 0], [s, h]], q(b * h, 2)],
    [`a right triangle with legs ${b} cm and ${h} cm`, [[0, 0], [b, 0], [0, h]], q(b * h, 2)],
    [`a parallelogram with base ${b} cm and height ${h} cm`, [[0, 0], [b, 0], [b + s, h], [s, h]], q(b * h)],
    [`a trapezoid with parallel sides ${b} cm and ${b2} cm and height ${h} cm`, [[0, 0], [b, 0], [s + b2, h], [s, h]], q((b + b2) * h, 2)],
  ];
  const [txt, verts, v] = shapes[t];
  return draft(`Find the area of ${txt}, in cm².`, exact(v), `${qtex(v)}\\ \\text{cm}^2`, [[`Half the rectangle on the same base and height: ${m(`\\tfrac12 bh`)}.`, `${m(`\\tfrac12 \\times ${b} \\times ${h}`)}.`, `Cut off a triangle and slide it over: a ${b} × ${h} rectangle.`, `Two copies make a parallelogram with base ${b + b2}: ${m(`\\tfrac12(b_1 + b_2)h`)}.`][t], `${m(`= ${qtex(v)}`)}.`], { mx: "shoelace", verts });
};
const surfaceArea: Gen = (r) => {
  const l = r.int(1, 10), w = r.int(1, 10), h = r.int(1, 10);
  return draft(`A net folds into a ${l} × ${w} × ${h} box. What is the surface area?`, exact(2 * (l * w + l * h + w * h)), `${2 * (l * w + l * h + w * h)}`, [`Six rectangles, in pairs: ${m(`2(${l * w} + ${l * h} + ${w * h})`)}.`], { mx: "box-sa", l, w, h });
};
const circle: Gen = (r) => {
  const rad = r.int(1, 15), useD = r.chance(0.4), area = r.chance(0.5);
  const v = area ? rad * rad : 2 * rad;
  return draft(`A circle has ${useD ? `diameter ${2 * rad}` : `radius ${rad}`} cm. Find its ${area ? "area (cm²)" : "circumference (cm)"} — exact in terms of π (e.g. ${area ? "25pi" : "10pi"}) or to 2 decimals.`,
    approx(`${v}*pi`, piTol(v * Math.PI)), `${v}\\pi`, [area ? `${m(`A = \\pi r^2 = \\pi(${rad})^2`)}.` : `${m(`C = 2\\pi r = \\pi d = ${2 * rad}\\pi`)}.`], { mx: "circle", rad, area });
};
const anglePairs: Gen = (r) => {
  const t = r.int(0, 2), tot = [90, 180, 0][t];
  const x = r.int(5, 30), a = r.int(2, 5), b = r.int(-20, 20);
  const A = a * x + b;
  require_(A > 5 && (t === 2 || A < tot - 5));
  const other = t === 2 ? A : tot - A;
  const name = ["complementary", "supplementary", "vertical"][t];
  return draft(`Two angles are ${name}. One measures ${m(`(${cx(a, "x")}${sg(b)})^\\circ`)} and the other ${other}°. Find ${m("x")}.`, exact(x), `x = ${x}`,
    [t === 2 ? `Vertical angles are equal: ${m(`${cx(a, "x")}${sg(b)} = ${other}`)}.` : `They add to ${tot}°: ${m(`${cx(a, "x")}${sg(b)} + ${other} = ${tot}`)}.`], { mx: "solve", eq: t === 2 ? `${a}*x + ${b} - ${other}` : `${a}*x + ${b} + ${other} - ${tot}` });
};
const prismWord: Gen = (r) => {
  const b = r.int(2, 12), h = r.int(2, 10), L = r.int(3, 20);
  require_((b * h) % 2 === 0);
  return draft(`A tent is a triangular prism: the triangle has base ${b} ft and height ${h} ft, and the tent is ${L} ft long. What is its volume in ft³?`, exact((b * h * L) / 2), `${(b * h * L) / 2}`, [`Base area ${m(`\\tfrac12(${b})(${h}) = ${(b * h) / 2}`)}, times length ${L}.`], { mx: "tri-prism", tri: [[0, 0], [b, 0], [b / 2, h]], L });
};
const triangleAngles: Gen = (r) => {
  const t = r.int(0, 2), a = r.int(20, 100), b = r.int(20, 150 - a);
  if (t === 0) return box(`A triangle has angles ${a}° and ${b}°. What is the third angle?`, `${a} + ${b} + ? == 180`, 180 - a - b, [`Angles of a triangle add to 180°.`]);
  if (t === 1) return box(`A triangle has interior angles ${a}° and ${b}°. What is the exterior angle at the third vertex?`, `? + (180 - ${a} - ${b}) == 180`, a + b, [`An exterior angle equals the sum of the two remote interior angles: ${a + b}°.`]);
  const ang = r.int(30, 150), x = r.int(5, 25), k = r.int(2, 5), c = ang - k * x;
  return draft(`Parallel lines are cut by a transversal. Corresponding angles measure ${ang}° and ${m(`(${cx(k, "x")}${sg(c)})^\\circ`)}. Find ${m("x")}.`, exact(x), `x = ${x}`, [`Corresponding angles are equal: ${m(`${cx(k, "x")}${sg(c)} = ${ang}`)}.`], { mx: "solve", eq: `${k}*x + ${c} - ${ang}` });
};
const TRANS = ["translate", "reflect-x", "reflect-y", "rot90", "rot180", "dilate"];
const transform: Gen = (r) => {
  const x = r.nz(-8, 8), y = r.nz(-8, 8), t = r.pick(TRANS), dx = r.nz(-6, 6), dy = r.nz(-6, 6), k = r.pick([2, 3, q(1, 2)].map(Q.of));
  require_(t !== "dilate" || k.mul(x).isInt() && k.mul(y).isInt());
  const img: [Q, Q] = t === "translate" ? [q(x + dx), q(y + dy)] : t === "reflect-x" ? [q(x), q(-y)] : t === "reflect-y" ? [q(-x), q(y)] : t === "rot90" ? [q(-y), q(x)] : t === "rot180" ? [q(-x), q(-y)] : [k.mul(x), k.mul(y)];
  const desc = { translate: `translated ${dx} units horizontally and ${dy} units vertically`, "reflect-x": `reflected across the x-axis`, "reflect-y": `reflected across the y-axis`, rot90: `rotated 90° counterclockwise about the origin`, rot180: `rotated 180° about the origin`, dilate: `dilated by scale factor ${m(k.tex())} centered at the origin` }[t];
  return draft(`The point ${m(`(${x}, ${y})`)} is ${desc}. What are the image's coordinates?`, tuple([{ label: "x", tex: "x'", ref: img[0] }, { label: "y", tex: "y'", ref: img[1] }]), `(${img[0].tex()}, ${img[1].tex()})`,
    [{ translate: `${m(`(x + ${par(dx)},\\ y + ${par(dy)})`)}`, "reflect-x": `${m("(x, y) \\to (x, -y)")}`, "reflect-y": `${m("(x, y) \\to (-x, y)")}`, rot90: `${m("(x, y) \\to (-y, x)")}`, rot180: `${m("(x, y) \\to (-x, -y)")}`, dilate: `${m(`(x, y) \\to (${k.tex()}x, ${k.tex()}y)`)}` }[t] + "."], { mx: "transform", x, y, t, dx, dy, k: `${k.n}/${k.d}` });
};
const TRIPLES = [[3, 4, 5], [5, 12, 13], [8, 15, 17], [7, 24, 25], [20, 21, 29], [9, 40, 41]];
const pythag: Gen = (r) => {
  const [a, b, c] = r.pick(TRIPLES), k = r.int(1, 4), t = r.int(0, 2);
  if (t === 2) {
    const [p, qq, s] = [r.int(1, 8), r.int(1, 8), r.int(1, 8)];
    const d2 = p * p + qq * qq + s * s;
    return draft(`A box is ${p} by ${qq} by ${s} inches. How long is the diagonal from one corner to the opposite corner? (exact, e.g. sqrt(29), or 2 decimals)`, approx(`sqrt(${d2})`, piTol(Math.sqrt(d2))), `\\sqrt{${d2}}`,
      [`Floor diagonal² = ${p}² + ${qq}²; then add height²: ${m(`d = \\sqrt{${p}^2 + ${qq}^2 + ${s}^2} = \\sqrt{${d2}}`)}.`], { mx: "diag3", dims: [p, qq, s] });
  }
  return t === 0
    ? draft(`A right triangle has legs ${a * k} and ${b * k}. How long is the hypotenuse?`, exact(c * k), `${c * k}`, [`${m(`c = \\sqrt{${a * k}^2 + ${b * k}^2} = ${c * k}`)}.`], { mx: "eq", eq: `?**2 == ${a * k}**2 + ${b * k}**2 and ? > 0` })
    : draft(`A right triangle has hypotenuse ${c * k} and one leg ${a * k}. How long is the other leg?`, exact(b * k), `${b * k}`, [`${m(`b = \\sqrt{${c * k}^2 - ${a * k}^2} = ${b * k}`)}.`], { mx: "eq", eq: `${a * k}**2 + ?**2 == ${c * k}**2 and ? > 0` });
};
const pythagConverse: Gen = (r) => {
  const [a, b, c] = r.pick(TRIPLES), k = r.int(1, 3), right = r.chance(0.5);
  const sides = right ? [a * k, b * k, c * k] : [a * k, b * k, c * k + r.nz(-2, 2)];
  return draft(`A triangle has sides ${sides.join(", ")}. Is it a right triangle?`, choice(["Right triangle", "Not a right triangle"], right ? "Right triangle" : "Not a right triangle"), `\\text{${right ? "Right" : "Not right"}}`,
    [`Converse of Pythagoras: right exactly when ${m(`${sides[0]}^2 + ${sides[1]}^2 = ${sides[2]}^2`)} (${sides[0] ** 2 + sides[1] ** 2} vs ${sides[2] ** 2}).`], { mx: "is-right", sides });
};
const distance: Gen = (r) => {
  const [a, b] = r.pick(TRIPLES), k = r.int(1, 2), x1 = r.int(-9, 9), y1 = r.int(-9, 9), sx = r.pick([1, -1]), sy = r.pick([1, -1]);
  const flip = r.chance(0.5);
  const [dx, dy] = flip ? [b * k, a * k] : [a * k, b * k];
  const x2 = x1 + sx * dx, y2 = y1 + sy * dy;
  const c = Math.sqrt(dx * dx + dy * dy);
  return draft(`What is the distance between ${m(`(${x1}, ${y1})`)} and ${m(`(${x2}, ${y2})`)}?`, exact(c), `${c}`, [`Legs ${dx} and ${dy}: ${m(`\\sqrt{${dx}^2 + ${dy}^2} = ${c}`)}.`], { mx: "dist", p: [x1, y1], q: [x2, y2] });
};
const volumeRound: Gen = (r) => {
  const t = r.int(0, 2), rad = r.int(1, 9), h = r.int(1, 12);
  const v = [q(rad * rad * h), q(rad * rad * h, 3), q(4 * rad ** 3, 3)][t];
  const nm = ["cylinder", "cone", "sphere"][t];
  return draft(`Find the volume of a ${nm} with radius ${rad}${t < 2 ? ` and height ${h}` : ""} — exact in terms of π (e.g. ${t === 1 ? "12pi" : "36pi"}) or to 2 decimals.`, approx(`(${v.n}/${v.d})*pi`, piTol(v.value() * Math.PI)), `${qtex(v)}\\pi`,
    [[`${m("V = \\pi r^2 h")}`, `${m("V = \\tfrac13 \\pi r^2 h")}`, `${m("V = \\tfrac43 \\pi r^3")}`][t] + ` ${m(`= ${qtex(v)}\\pi`)}.`], { mx: "solid", t: nm, rad, h });
};

// ── statistics & probability ────────────────────────────────────────────────
function quartiles(xs: number[]): [number, number, number] {
  const s = [...xs].sort((a, b) => a - b);
  const med = (a: number[]) => (a.length % 2 ? a[(a.length - 1) / 2] : (a[a.length / 2 - 1] + a[a.length / 2]) / 2);
  const h = Math.floor(s.length / 2);
  return [med(s.slice(0, h)), med(s), med(s.slice(s.length - h))];
}
const centerSpread: Gen = (r) => {
  const n = r.int(5, 9);
  const xs = Array.from({ length: n }, () => r.int(1, 30));
  const t = r.pick(["mean", "median", "range", "IQR", "MAD"]);
  const mean = q(xs.reduce((a, b) => a + b, 0), n);
  const [q1, md, q3] = quartiles(xs);
  if (t === "MAD") require_(mean.isInt());
  const v = t === "mean" ? mean : t === "median" ? q(md * 2, 2) : t === "range" ? q(Math.max(...xs) - Math.min(...xs)) : t === "IQR" ? q((q3 - q1) * 2, 2) : xs.reduce((s, x) => s.add(Math.abs(x - mean.n)), q(0)).div(n);
  const sorted = [...xs].sort((a, b) => a - b);
  return draft(`Data: ${m(xs.join(",\\ "))}. Find the ${{ mean: "mean", median: "median", range: "range", IQR: "interquartile range (median of each half, leaving out the middle value when the count is odd)", MAD: "mean absolute deviation" }[t]}.`,
    exact(v), qtex(v), [`Sorted: ${m(sorted.join(",\\ "))}.`, { mean: `Sum ${xs.reduce((a, b) => a + b, 0)} ÷ ${n}.`, median: `Middle value${n % 2 ? "" : "s averaged"}.`, range: `Max − min.`, IQR: `Q1 = ${q1}, Q3 = ${q3}.`, MAD: `Mean ${mean.n}; average the distances from it.` }[t]], { mx: "stat", xs, t });
};
const bag = (r: Rng) => {
  const cols = ["red", "blue", "green", "yellow"].slice(0, r.int(2, 4));
  return { cols, cnt: cols.map(() => r.int(0, 9)) };
};
const probSimple: Gen = (r) => {
  const { cols, cnt } = bag(r);
  const tot = cnt.reduce((a, b) => a + b, 0), i = r.int(0, cols.length - 1);
  require_(tot > 0);
  return draft(`A bag has ${cols.map((c, k) => `${cnt[k]} ${c}`).join(", ")} marbles. One is drawn at random. What is the probability it is ${cols[i]}?`, exact(q(cnt[i], tot)), q(cnt[i], tot).tex(), [`Favorable ÷ total: ${m(`\\frac{${cnt[i]}}{${tot}}`)}.`], { mx: "bag", cnt, i });
};
const LIKELY = ["Impossible", "Unlikely", "Equally likely as not", "Likely", "Certain"];
const probLikely: Gen = (r) => {
  const tot = r.int(4, 20), k = r.chance(0.15) ? r.pick([0, tot]) : r.chance(0.15) ? tot / 2 : r.int(1, tot - 1);
  require_(Number.isInteger(k));
  const p = k / tot;
  const ans = p === 0 ? LIKELY[0] : p === 1 ? LIKELY[4] : p === 0.5 ? LIKELY[2] : p < 0.5 ? LIKELY[1] : LIKELY[3];
  return draft(`A spinner has ${tot} equal sections, ${k} of them blue. Landing on blue is…`, choice(LIKELY, ans), `\\text{${ans}}`, [`${m(`P = \\frac{${k}}{${tot}}`)}: 0 impossible, below ½ unlikely, ½ even, above ½ likely, 1 certain.`], { mx: "likely", k, tot });
};
const probPredict: Gen = (r) => {
  const sides = r.pick([4, 6, 8, 10]), n = sides * r.int(5, 50);
  return draft(`A fair ${sides}-sided die is rolled ${n} times. About how many times do you expect a 1?`, exact(n / sides), `${n / sides}`, [`${m(`P(1) = \\frac1{${sides}}`)}, so about ${m(`\\frac{${n}}{${sides}} = ${n / sides}`)}.`], { mx: "predict", sides, n });
};
const probCompound: Gen = (r) => {
  const t = r.int(0, 2);
  if (t === 0) {
    const s = r.int(2, 12);
    const ways = [1, 2, 3, 4, 5, 6].flatMap((a) => [1, 2, 3, 4, 5, 6].map((b) => a + b)).filter((x) => x === s).length;
    return draft(`Two fair dice are rolled. What is the probability the sum is ${s}?`, exact(q(ways, 36)), q(ways, 36).tex(), [`${ways} of the 36 equally likely outcomes give ${s}.`], { mx: "dice-sum", s });
  }
  if (t === 1) {
    const n = r.int(2, 4), k = r.int(0, n);
    const c = [1, 1, 2, 6, 24][n] / ([1, 1, 2, 6, 24][k] * [1, 1, 2, 6, 24][n - k]);
    return draft(`${n} fair coins are tossed. What is the probability of exactly ${k} heads?`, exact(q(c, 2 ** n)), q(c, 2 ** n).tex(), [`List the ${2 ** n} outcomes; ${c} have exactly ${k} heads.`], { mx: "coins", n, k });
  }
  const d = r.int(1, 6);
  return draft(`A coin is tossed and a die is rolled. What is the probability of heads and a number greater than ${d - 1}?`, exact(q(7 - d, 12)), q(7 - d, 12).tex(), [`12 outcomes; heads with ${d}–6 is ${7 - d} of them.`], { mx: "coin-die", d });
};
const sampleInfer: Gen = (r) => {
  const n = r.pick([20, 25, 40, 50]), k = r.int(1, n - 1), N = n * r.int(5, 40);
  return draft(`In a random sample of ${n} students, ${k} prefer soccer. Estimate how many of the school's ${intTxt(N)} students prefer soccer.`, exact(q(k * N, n)), `${(k * N) / n}`, [`Same proportion: ${m(`\\frac{${k}}{${n}} \\times ${int(N)} = ${(k * N) / n}`)}.`], { mx: "sample", n, k, N });
};
const linePredict: Gen = (r) => {
  const mm = q(r.int(1, 40), r.pick([1, 2, 4])), b = r.int(0, 50), x = r.int(1, 20);
  return draft(`A line of best fit for study hours ${m("x")} and test score ${m("y")} is ${m(`y = ${decTexQ(mm)}x + ${b}`)}. Predict the score for ${x} hours.`, exact(mm.mul(x).add(b)), decTexQ(mm.mul(x).add(b)), [`Each extra hour adds ${decTexQ(mm)} points to the predicted score; start from ${b} at 0 hours.`], { mx: "expr", e: `${qpy(mm)}*${x} + ${b}` });
};
const twoWay: Gen = (r) => {
  const t = [[r.int(5, 40), r.int(5, 40)], [r.int(5, 40), r.int(5, 40)]];
  const row = r.int(0, 1), col = r.int(0, 1);
  const rowTot = t[row][0] + t[row][1];
  return draft(`Survey: of students with a curfew, ${t[0][0]} do chores and ${t[0][1]} don't; of students without a curfew, ${t[1][0]} do chores and ${t[1][1]} don't. Among students ${row ? "without" : "with"} a curfew, what fraction ${col ? "don't do" : "do"} chores?`,
    exact(q(t[row][col], rowTot)), q(t[row][col], rowTot).tex(), [`Row relative frequency: ${m(`\\frac{${t[row][col]}}{${rowTot}}`)}.`], { mx: "two-way", t, row, col });
};

export const K8_TEMPLATES: Record<string, Gen> = {
  // counting & cardinality, place value
  "k8-count-on": countOn(1, 95, 3),
  "k8-count-120": countOn(90, 116, 4),
  "k8-count-tens": countBy([10], 100),
  "k8-skip-count": countBy([5, 10, 100], 1000),
  "k8-cmp-10": cmpWhole(1, 10, false),
  "k8-cmp-2d": cmpWhole(10, 99, true),
  "k8-cmp-3d": cmpWhole(100, 999, true),
  "k8-cmp-multi": cmpWhole(1000, 999999, true),
  "k8-cmp-dec2": cmpDec(2),
  "k8-cmp-dec3": cmpDec(3),
  "k8-cmp-frac-same": cmpFrac(true),
  "k8-cmp-frac": cmpFrac(false),
  "k8-cmp-rational": cmpRational,
  "k8-teen": teen,
  "k8-tens-ones": tensOnes,
  "k8-ten-more": moreLess(10, 10, 89),
  "k8-hundred-more": moreLess(100, 100, 900),
  "k8-expanded": expanded(3, 0),
  "k8-expanded-big": expanded(6, 0),
  "k8-expanded-dec": expanded(6, 3),
  "k8-digit-value": digitValue(6, 0),
  "k8-digit-value-dec": digitValue(5, 3),
  "k8-ten-times": tenTimes(false),
  "k8-ten-times-dec": tenTimes(true),
  "k8-round-10-100": roundTo([2, 3], 0, [1, 2]),
  "k8-round-any": roundTo([4, 7], 0, [1, 2, 3, 4, 5]),
  "k8-round-dec": roundTo([3, 5], 3, [-1, -2, 0]),
  "k8-pow10": pow10,
  // addition & subtraction
  "k8-add5": addWithin(5),
  "k8-add10": addWithin(10),
  "k8-add20": addWithin(20),
  "k8-add100": addWithin(100, 10),
  "k8-add1000": addWithin(1000, 100),
  "k8-add-multi": addWithin(999999, 1000),
  "k8-add2d1d": add2d1d,
  "k8-sub-tens": subTens,
  "k8-add3": addMany(3, 1, 9, 20),
  "k8-add4x2d": addMany(4, 10, 99, 400),
  "k8-make-ten": makeTen,
  "k8-decompose10": decompose,
  "k8-missing-addend": missingAddend(20),
  "k8-true-false": trueFalse,
  "k8-even-odd": evenOdd,
  "k8-word-add10": wordAdd(10),
  "k8-word-add20": wordAdd(20),
  "k8-word-add100": wordAdd(100),
  // multiplication & division
  "k8-array": array,
  "k8-mult-facts": multFacts,
  "k8-missing-factor": missingFactor,
  "k8-mult-tens": multTens,
  "k8-word-mult": wordMult,
  "k8-word-2step": wordTwoStep,
  "k8-mult-compare": multCompare,
  "k8-remainder-word": remainderWord,
  "k8-factors": factors,
  "k8-pattern": pattern,
  "k8-two-patterns": twoPatterns,
  "k8-mult-multi": multMulti(false),
  "k8-mult-std": multMulti(true),
  "k8-div-rem": divRem,
  "k8-div-2d": divExact(11, 99, 12, 99),
  "k8-long-div": divExact(12, 250, 101, 999),
  "k8-order-ops": orderOps(false),
  "k8-exponents": orderOps(true),
  "k8-times-as-large": timesAsLarge,
  // fractions
  "k8-frac-line": fracLine,
  "k8-unit-share": unitShare,
  "k8-frac-equiv": fracEquiv,
  "k8-frac-whole": fracWhole,
  "k8-frac-add-like": fracAddLike(false),
  "k8-frac-mixed-like": fracAddLike(true),
  "k8-frac-decompose": fracDecompose,
  "k8-frac-times-whole": fracTimesWhole(false),
  "k8-frac-times-word": fracTimesWhole(true),
  "k8-frac-hundredths": hundredths,
  "k8-frac-to-dec": fracToDec,
  "k8-frac-add": fracAddUnlike(false),
  "k8-frac-add-word": fracAddUnlike(true),
  "k8-frac-as-div": fracAsDiv,
  "k8-frac-mult": fracMult(false),
  "k8-frac-mult-mixed": fracMult(true),
  "k8-frac-area": fracArea,
  "k8-frac-scaling": scaling,
  "k8-frac-unit-div": unitFracDiv(false),
  "k8-frac-unit-div-word": unitFracDiv(true),
  "k8-frac-div": fracDiv,
  // decimals
  "k8-dec-ops": decOps(false),
  "k8-dec-std": decOps(true),
  "k8-dec-convert": decConvert,
  "k8-repeating": repeating,
  // measurement & data
  "k8-shape-attr": shapeAttr,
  "k8-time-half": timeAfter(30),
  "k8-time-five": timeAfter(5),
  "k8-elapsed": elapsed,
  "k8-money": money,
  "k8-convert-down": convert(true),
  "k8-convert": convert(false),
  "k8-rect-area": rectArea,
  "k8-area-distributive": areaDistributive,
  "k8-rectilinear": rectilinear,
  "k8-perimeter": perimeter,
  "k8-angle-turn": angleTurn,
  "k8-angle-add": angleAdd,
  "k8-angle-type": angleType,
  "k8-symmetry-lines": symmetryLines,
  "k8-shape-hierarchy": hierarchy,
  "k8-volume-prism": volumePrism(false),
  "k8-volume-frac": volumePrism(true),
  "k8-volume-composite": volumeComposite,
  "k8-data-graph": dataGraph(false),
  "k8-data-scaled": dataGraph(true),
  "k8-line-plot": linePlot(false),
  "k8-line-plot-share": linePlot(true),
  // ratios & percents
  "k8-ratio-table": ratioTable,
  "k8-unit-rate": unitRate,
  "k8-percent": percentOf,
  "k8-unit-rate-frac": unitRateFrac,
  "k8-prop-test": propTest,
  "k8-prop-k": propK,
  "k8-percent-change": percentChange,
  "k8-scale-drawing": scaleDrawing,
  // integers & rationals
  "k8-opposite": opposite,
  "k8-abs": absVal,
  "k8-quadrant": quadrant,
  "k8-plot-q1": plotQ1,
  "k8-coord-dist": coordDist,
  "k8-int-add-sub": intOps([0, 1]),
  "k8-int-mul-div": intOps([2, 3]),
  "k8-rational-ops": rationalOps,
  "k8-gcf-lcm": gcfLcm,
  // expressions & equations
  "k8-evaluate": evaluate,
  "k8-equiv-form": equivForm(false),
  "k8-equiv-form-rational": equivForm(true),
  "k8-equiv-check": equivCheck,
  "k8-coefficient": coefficient,
  "k8-percent-expr": percentExpr,
  "k8-one-step": oneStep,
  "k8-solution-check": solutionCheck,
  "k8-ineq-phrase": ineqPhrase,
  "k8-two-step": twoStep,
  "k8-two-step-ineq": twoStepIneq,
  "k8-dependent": dependent,
  // grade 8
  "k8-int-exponents": intExponents,
  "k8-roots": roots,
  "k8-sqrt-between": sqrtBetween,
  "k8-sci-notation": sciNotation,
  "k8-linear-eq": linearEq,
  "k8-eq-count": eqCount,
  "k8-system": system(false),
  "k8-system-word": system(true),
  "k8-slope": slope(false),
  "k8-rate-initial": slope(true),
  "k8-is-function": isFunction,
  "k8-linear-or-not": linearOrNot,
  "k8-compare-fns": compareFns,
  // geometry
  "k8-area-poly": areaPoly,
  "k8-surface-area": surfaceArea,
  "k8-circle": circle,
  "k8-angle-pairs": anglePairs,
  "k8-prism-word": prismWord,
  "k8-triangle-angles": triangleAngles,
  "k8-transform": transform,
  "k8-pythag": pythag,
  "k8-pythag-converse": pythagConverse,
  "k8-distance": distance,
  "k8-volume-round": volumeRound,
  // statistics & probability
  "k8-center-spread": centerSpread,
  "k8-prob-simple": probSimple,
  "k8-prob-likely": probLikely,
  "k8-prob-predict": probPredict,
  "k8-prob-compound": probCompound,
  "k8-sample-infer": sampleInfer,
  "k8-line-predict": linePredict,
  "k8-two-way": twoWay,
};
