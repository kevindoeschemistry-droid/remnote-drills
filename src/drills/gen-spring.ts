// Kreyszig §2.4 · mass–spring free motion, Level 1. Variable t, displacement y(t).
// Built backward from the roots of m r^2 + c r + k = 0 and from integer
// solution constants, so every IVP has clean numbers.
import { Rng } from "./rng";
import type { Draft } from "./types";
import { ct, ex, join, m } from "./tex";
import { Q } from "./rational";
import { require_ } from "./reject";

const DAMP_OPTIONS = ["Overdamped", "Critically damped", "Underdamped"];
const par = (n: number) => (n < 0 ? `(${n})` : `${n}`);
const wt = (w: number) => (w === 1 ? "t" : `${w}t`);

function odeTex(mm: number, c: number, k: number) {
  return `${join([ct(mm, "y''"), c ? ct(c, "y'") : "", ct(k, "y")])} = 0`;
}

// ── undamped ───────────────────────────────────────────────────────────────
function frequency(r: Rng): Draft {
  const us = r.chance(0.5);
  let w: number, setup: string, steps: string[];
  if (us) {
    // weight W lb stretches s ft: k = W/s, m = W/32, ω² = 32/s
    const [s, w0] = r.pick([[2, 4], [new Q(1, 2), 8], [8, 2], [new Q(1, 8), 16]] as [number | Q, number][]);
    const sQ = Q.of(s);
    const W = r.pick([4, 8, 16, 32, 64]);
    w = w0;
    const k = new Q(W).div(sQ);
    const mass = new Q(W, 32);
    setup = `A ${W}-lb weight stretches a spring ${m(sQ.tex())} ft. Use ${m("g = 32")} ft/s².`;
    steps = [
      `Hooke: ${m(`k = \\frac{W}{s} = \\frac{${W}}{${sQ.tex()}} = ${k.tex()}`)} lb/ft; mass ${m(`m = \\frac{W}{g} = ${mass.tex()}`)} slug.`,
      `${m(`\\omega_0 = \\sqrt{k/m} = \\sqrt{${k.div(mass).tex()}} = ${w}`)} rad/s.`,
      `${m(`T = \\frac{2\\pi}{\\omega_0} = ${tPi(w)}`)} s.`,
    ];
  } else {
    w = r.pick([2, 3, 4, 5, 6]);
    const mm = r.pick([1, 2, 4]);
    const k = mm * w * w;
    setup = `A ${mm}-kg mass hangs on a spring with ${m(`k = ${k}`)} N/m (no damping).`;
    steps = [
      `${m(`\\omega_0 = \\sqrt{k/m} = \\sqrt{${k}/${mm}} = ${w}`)} rad/s.`,
      `${m(`T = \\frac{2\\pi}{\\omega_0} = ${tPi(w)}`)} s.`,
    ];
  }
  return {
    prompt: `${setup} Find the natural angular frequency ${m("\\omega_0")} and the period ${m("T")}.`,
    answer: {
      kind: "tuple",
      fields: [
        { label: "ω₀", tex: "\\omega_0", ref: `${w}`, mode: "number" },
        { label: "T", tex: "T", ref: `2*pi/${w}`, mode: "number" },
      ],
      vars: [],
    },
    answerTex: `\\omega_0 = ${w},\\ T = ${tPi(w)}`,
    steps,
    meta: { variant: us ? "us" : "si", w },
  };
}

function tPi(w: number): string {
  const q = new Q(2, w);
  return q.n === 1 ? (q.d === 1 ? "\\pi" : `\\frac{\\pi}{${q.d}}`) : q.d === 1 ? `${q.n}\\pi` : `\\frac{${q.n}\\pi}{${q.d}}`;
}

function undampedIvp(r: Rng): Draft {
  const w = r.pick([1, 2, 3, 4, 5]);
  const mm = r.pick([1, 1, 2, 4]);
  const k = mm * w * w;
  const A = r.int(-3, 4);
  const B = r.int(-3, 3);
  require_(A !== 0 || B !== 0);
  const v0 = B * w;
  const sol = join([ct(A, `\\cos ${wt(w)}`), ct(B, `\\sin ${wt(w)}`)]);
  return {
    prompt: `Undamped mass–spring: solve ${m(`${odeTex(mm, 0, k)},\\quad y(0) = ${A},\\ y'(0) = ${v0}`)}.`,
    answer: { kind: "ode2", a: mm, b: 0, c: k, v: "t", ic: [0, A, v0], ref: `(${A})*cos(${w}*t) + (${B})*sin(${w}*t)` },
    answerTex: `y = ${sol}`,
    steps: [
      `${m(`${mm === 1 ? "" : mm}r^2 + ${k} = 0 \\Rightarrow r = \\pm ${w === 1 ? "" : w}i`)}, so ${m(`\\omega_0 = ${w}`)} and ${m(`y = A\\cos ${wt(w)} + B\\sin ${wt(w)}`)}.`,
      `${m(`y(0) = A = ${A}`)}; ${m(`y'(0) = ${w === 1 ? "" : w}B = ${v0} \\Rightarrow B = ${B}`)}.`,
      m(`y = ${sol}`),
    ],
    meta: { variant: "undamped" },
  };
}

function amplitudePhase(r: Rng): Draft {
  const w = r.pick([1, 2, 3, 4]);
  const [A0, B0] = r.pick([[3, 4], [4, 3], [5, 12], [1, 1], [6, 8], [8, 15]] as [number, number][]);
  const A = A0 * r.pick([1, -1]);
  const B = B0 * r.pick([1, -1]);
  const R2 = A * A + B * B;
  const Rt = Math.round(Math.sqrt(R2)) ** 2 === R2 ? `${Math.round(Math.sqrt(R2))}` : `\\sqrt{${R2}}`;
  let delta = Math.atan2(B, A);
  if (delta < 0) delta += 2 * Math.PI;
  const base = Math.abs(A) === Math.abs(B) ? "\\frac{\\pi}{4}" : `\\arctan\\frac{${Math.abs(B)}}{${Math.abs(A)}}`;
  const quad = A > 0 ? (B > 0 ? 1 : 4) : B > 0 ? 2 : 3;
  const dTex =
    Math.abs(A) === Math.abs(B)
      ? ["", "\\frac{\\pi}{4}", "\\frac{3\\pi}{4}", "\\frac{5\\pi}{4}", "\\frac{7\\pi}{4}"][quad]
      : ["", base, `\\pi - ${base}`, `\\pi + ${base}`, `2\\pi - ${base}`][quad];
  const y = join([ct(A, `\\cos ${wt(w)}`), ct(B, `\\sin ${wt(w)}`)]);
  return {
    prompt: `Write ${m(`y = ${y}`)} as ${m(`R\\cos(${wt(w)} - \\delta)`)} with ${m("R > 0,\\ 0 \\le \\delta < 2\\pi")}.`,
    answer: {
      kind: "tuple",
      fields: [
        { label: "R", tex: "R", ref: `sqrt(${R2})`, mode: "number" },
        { label: "δ", tex: "\\delta", ref: `${delta}`, mode: "angle" },
      ],
      vars: [],
    },
    answerTex: `R = ${Rt},\\ \\delta = ${dTex} \\approx ${delta.toFixed(4)}`,
    steps: [
      `${m("R\\cos(\\omega t - \\delta) = R\\cos\\delta\\cos\\omega t + R\\sin\\delta\\sin\\omega t")}, so ${m(`R\\cos\\delta = ${A}`)}, ${m(`R\\sin\\delta = ${B}`)}.`,
      `${m(`R = \\sqrt{${par(A)}^2 + ${par(B)}^2} = ${Rt}`)}.`,
      `${m(`\\tan\\delta = \\frac{${B}}{${A}}`)}, and ${m(`(\\cos\\delta, \\sin\\delta)`)} has the signs of ${m(`(${A}, ${B})`)}: quadrant ${quad}, so ${m(`\\delta = ${dTex} \\approx ${delta.toFixed(4)}`)}.`,
    ],
    meta: { variant: "amplitude-phase", A, B, w },
  };
}

// ── damped ─────────────────────────────────────────────────────────────────
interface Damped {
  type: 0 | 1 | 2; // over, critical, under
  mm: number;
  c: number;
  k: number;
  rootsTex: string;
  p?: number;
  q?: number;
  al?: number;
  be?: number;
}

function damped(r: Rng, type: 0 | 1 | 2): Damped {
  const mm = r.pick([1, 1, 2]);
  if (type === 0) {
    const p = r.int(1, 4);
    const q = r.int(p + 1, 6);
    return { type, mm, c: mm * (p + q), k: mm * p * q, rootsTex: `r = -${p},\\ -${q}`, p, q };
  }
  if (type === 1) {
    const p = r.int(1, 4);
    return { type, mm, c: 2 * mm * p, k: mm * p * p, rootsTex: `r = -${p}\\ (\\text{double})`, p };
  }
  const al = r.int(1, 3);
  const be = r.int(1, 4);
  return {
    type, mm, c: 2 * mm * al, k: mm * (al * al + be * be),
    rootsTex: `r = -${al} \\pm ${be === 1 ? "" : be}i`, al, be,
  };
}

function classifyDamping(r: Rng): Draft {
  const d = damped(r, r.int(0, 2) as 0 | 1 | 2);
  const disc = d.c * d.c - 4 * d.mm * d.k;
  return {
    prompt: `Classify the motion of ${m(odeTex(d.mm, d.c, d.k))}.`,
    answer: { kind: "choice", options: DAMP_OPTIONS, correct: DAMP_OPTIONS[d.type] },
    answerTex: `\\text{${DAMP_OPTIONS[d.type]}}`,
    steps: [
      `Compare ${m("c^2")} with ${m("4mk")}: ${m(`c^2 - 4mk = ${d.c * d.c} - ${4 * d.mm * d.k} = ${disc}`)}.`,
      `${m(disc > 0 ? "> 0" : disc === 0 ? "= 0" : "< 0")}: ${DAMP_OPTIONS[d.type].toLowerCase()} (${m(d.rootsTex)}).`,
    ],
    meta: { variant: "classify", ...d },
  };
}

function dampedIvp(type: 0 | 1 | 2) {
  return (r: Rng): Draft => {
    const d = damped(r, type);
    const C1 = r.int(-3, 4);
    const C2 = r.int(-3, 4);
    require_(C1 !== 0 || C2 !== 0);
    let sol: string, js: string, y0: number, v0: number, form: string, icStep: string;
    if (type === 0) {
      const { p, q } = d as Required<Damped>;
      y0 = C1 + C2;
      v0 = -p * C1 - q * C2;
      form = `y = C_1e^{-${p === 1 ? "" : p}t} + C_2e^{-${q}t}`;
      icStep = `${m(`C_1 + C_2 = ${y0}`)}, ${m(`-${p === 1 ? "" : p}C_1 - ${q}C_2 = ${v0}`)} ${m("\\Rightarrow")} ${m(`C_1 = ${C1},\\ C_2 = ${C2}`)}`;
      sol = join([ct(C1, ex(-p, "t")), ct(C2, ex(-q, "t"))]);
      js = `(${C1})*exp(-${p}*t) + (${C2})*exp(-${q}*t)`;
    } else if (type === 1) {
      const { p } = d as Required<Damped>;
      y0 = C1;
      v0 = C2 - p * C1;
      form = `y = (C_1 + C_2t)e^{-${p === 1 ? "" : p}t}`;
      icStep = `${m(`C_1 = ${y0}`)}, ${m(`C_2 - ${p === 1 ? "" : p}C_1 = ${v0} \\Rightarrow C_2 = ${C2}`)}`;
      // (C1 + C2 t)e^{-pt}; no parentheses around a single term
      sol = C1 && C2 ? `\\left(${join([`${C1}`, ct(C2, "t")])}\\right)${ex(-p, "t")}` : C1 ? ct(C1, ex(-p, "t")) : ct(C2, `t${ex(-p, "t")}`);
      js = `((${C1}) + (${C2})*t)*exp(-${p}*t)`;
    } else {
      const { al, be } = d as Required<Damped>;
      y0 = C1;
      v0 = -al * C1 + be * C2;
      form = `y = e^{-${al === 1 ? "" : al}t}(C_1\\cos ${wt(be)} + C_2\\sin ${wt(be)})`;
      icStep = `${m(`C_1 = ${y0}`)}, ${m(`-${al === 1 ? "" : al}C_1 + ${be === 1 ? "" : be}C_2 = ${v0} \\Rightarrow C_2 = ${C2}`)}`;
      sol = `${ex(-al, "t")}\\left(${join([ct(C1, `\\cos ${wt(be)}`), ct(C2, `\\sin ${wt(be)}`)])}\\right)`;
      js = `exp(-${al}*t)*((${C1})*cos(${be}*t) + (${C2})*sin(${be}*t))`;
    }
    return {
      prompt: `Damped mass–spring: solve ${m(`${odeTex(d.mm, d.c, d.k)},\\quad y(0) = ${y0},\\ y'(0) = ${v0}`)}.`,
      answer: { kind: "ode2", a: d.mm, b: d.c, c: d.k, v: "t", ic: [0, y0, v0], ref: js },
      answerTex: `y = ${sol}`,
      steps: [
        `Characteristic equation ${m(`${d.mm === 1 ? "" : d.mm}r^2 + ${d.c}r + ${d.k} = 0`)}: ${m(d.rootsTex)} (${DAMP_OPTIONS[type].toLowerCase()}).`,
        `${m(form)}.`,
        icStep + ".",
        m(`y = ${sol}`),
      ],
      meta: { variant: ["over", "critical", "under"][type] },
    };
  };
}

export const SPRING_TEMPLATES: Record<string, (r: Rng) => Draft> = {
  "spring-frequency": frequency,
  "spring-undamped-ivp": undampedIvp,
  "spring-amplitude-phase": amplitudePhase,
  "spring-classify": classifyDamping,
  "spring-over-ivp": dampedIvp(0),
  "spring-critical-ivp": dampedIvp(1),
  "spring-under-ivp": dampedIvp(2),
};
