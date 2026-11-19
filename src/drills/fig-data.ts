// Figures for problems-as-data: a `figure:` block in a drills/problems/*.yaml template is drawn
// here as SVG from the template's numbers, so the picture and the answer can never disagree.
//
//   type: plot        x, y: [min, max] · curves: [{ f, from, to, dash }] · points: [{ at, open, label }]
//                     vlines: [x…] · hlines: [y…] · segments / arrows: [{ from, to }] · shade: { f, from, to }
//                     field: "x - y" (slope field of dy/dx) · vfield: ["-y", "x"] · labels: [{ at, text }]
//                     scatter: { x: [...], y: [...] } · tick (or xtick, ytick): grid spacing (default: about eight lines)
//                     xunit: pi (label x in multiples of π)
//                     circles: [{ at, r, dash }] · arcs: [{ at, r, from, to }] (degrees) · bare: true (a geometry sketch: no grid or axes, one scale both ways)
//   type: numberline  range: [a, b] · step · labelEvery (label only multiples of it) · points: [{ at, open, label }]
//                     dots: [values] (a dot plot)
//                     box: { min, q1, med, q3, max } · interval: { from, to, openFrom, openTo }
//   type: grid        cols, rows · shaded (first n cells) · dots: true (objects to count, not squares) · count (first n dots)
//   type: bars        labels: [...] · values: [...]
//   type: table       head: [...] · rows: [[...], …]   or   xs: [...] + f: "expression in x" (a table of values)
//   type: molecule    atoms: [[x, y, label], …] (no label = a carbon vertex; "OH", "NH2", "H2N", "O", "S" …)
//                     bonds: [[i, j, order], …] (0-based atom indices; order 1, 2 or 3; 0 = a dashed coordinate bond). A skeletal structure.
// Every number may be an expression in the template's givens and lets. A function (`f`, `field`, a
// `vfield` component) may also be the name of a text field of the drawn case. Strokes use currentColor.
import { math } from "./check";

type Scope = Record<string, unknown>;
const ACCENT = "#5b7cfa", HOT = "#e0654f";
const W = 360;

const ev = (e: unknown, scope: Scope): any => (typeof e === "number" ? e : typeof e === "string" ? math.evaluate(e, { ...scope }) : e);
const n = (e: unknown, scope: Scope): number => Number(ev(e, scope)?.valueOf?.() ?? ev(e, scope));
const arr = (e: unknown, scope: Scope): number[] => {
  if (Array.isArray(e)) return e.map((q) => n(q, scope));
  const v = ev(e, scope);
  return (v?.toArray ? v.toArray() : v).map(Number);
};
/** a function to draw: an expression, or the name of a case's text field holding one */
const fx = (e: unknown, scope: Scope): string => (typeof e === "string" && typeof scope[e] === "string" ? String(scope[e]) : String(e));
const str = (e: unknown, scope: Scope): string => String(e).replace(/\{\{([^}]+)\}\}/g, (_, q) => { const v = ev(q.trim(), scope); return typeof v === "number" ? String(Number(v.toPrecision(6))) : String(v); });
const svg = (w: number, h: number, body: string) =>
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="100%" style="max-width:${w}px" font-family="system-ui, sans-serif" font-size="11" fill="none" stroke="currentColor">${body}</svg>`;
const text = (x: number, y: number, s: string, anchor = "middle", extra = "") => `<text x="${x.toFixed(1)}" y="${y.toFixed(1)}" text-anchor="${anchor}" fill="currentColor" stroke="none" ${extra}>${s}</text>`;
const tickStep = (span: number) => { const raw = span / 8, p = 10 ** Math.floor(Math.log10(raw)); return [1, 2, 5, 10].map((k) => k * p).find((s) => s >= raw)!; };
const nice = (v: number) => String(Number(v.toPrecision(6)));
/** an x value as a multiple of π: π/2, π, 3π/2 … (xunit: pi) */
function piLabel(v: number): string {
  for (const d of [1, 2, 3, 4, 6, 8, 12]) {
    const k = (v / Math.PI) * d;
    if (Math.abs(k - Math.round(k)) < 1e-6) { const m = Math.round(k), a = Math.abs(m); return `${m < 0 ? "−" : ""}${a === 1 ? "" : a}π${d === 1 ? "" : `/${d}`}`; }
  }
  return nice(v);
}
function arrowHead(x1: number, y1: number, x2: number, y2: number, color: string, h = 6) {
  const a = Math.atan2(y2 - y1, x2 - x1);
  return `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" stroke="${color}" stroke-width="1.4"/><polygon points="${x2.toFixed(1)},${y2.toFixed(1)} ${(x2 - h * Math.cos(a - 0.4)).toFixed(1)},${(y2 - h * Math.sin(a - 0.4)).toFixed(1)} ${(x2 - h * Math.cos(a + 0.4)).toFixed(1)},${(y2 - h * Math.sin(a + 0.4)).toFixed(1)}" fill="${color}" stroke="none"/>`;
}

function plot(f: any, scope: Scope): string {
  const [x0, x1] = arr(f.x ?? [-5, 5], scope), [y0, y1] = arr(f.y ?? [-5, 5], scope);
  const bare = !!f.bare;
  // a bare sketch keeps one scale on both axes, so circles are round and angles are true
  const L = bare ? 12 : 30, R = 12, T = 12, B = bare ? 12 : 24, H = bare ? T + B + ((W - L - R) * (y1 - y0)) / (x1 - x0) : 260;
  const X = (x: number) => L + ((x - x0) / (x1 - x0)) * (W - L - R), Y = (y: number) => H - B - ((y - y0) / (y1 - y0)) * (H - T - B);
  let s = "";
  const sx = n(f.xtick ?? f.tick ?? tickStep(x1 - x0), scope), sy = n(f.ytick ?? f.tick ?? tickStep(y1 - y0), scope);
  const xname = f.xunit === "pi" ? piLabel : nice;
  for (let x = Math.ceil(x0 / sx) * sx; !bare && x <= x1 + 1e-9; x += sx) {
    s += `<line x1="${X(x).toFixed(1)}" y1="${Y(y0)}" x2="${X(x).toFixed(1)}" y2="${Y(y1)}" opacity="0.13"/>`;
    if (Math.abs(x) > 1e-9) s += text(X(x), Math.min(H - B + 13, Math.max(T + 10, Y(0) + 13)), xname(x), "middle", 'opacity="0.75"');
  }
  for (let y = Math.ceil(y0 / sy) * sy; !bare && y <= y1 + 1e-9; y += sy) {
    s += `<line x1="${X(x0)}" y1="${Y(y).toFixed(1)}" x2="${X(x1)}" y2="${Y(y).toFixed(1)}" opacity="0.13"/>`;
    if (Math.abs(y) > 1e-9) s += text(Math.max(L - 4, Math.min(W - R - 4, X(0) - 4)), Y(y) + 4, nice(y), "end", 'opacity="0.75"');
  }
  if (!bare && y0 <= 0 && y1 >= 0) s += `<line x1="${X(x0)}" y1="${Y(0)}" x2="${X(x1)}" y2="${Y(0)}" stroke-width="1.2"/>` + text(X(x1) - 2, Y(0) - 5, f.xlabel ?? "x", "end");
  if (!bare && x0 <= 0 && x1 >= 0) s += `<line x1="${X(0)}" y1="${Y(y0)}" x2="${X(0)}" y2="${Y(y1)}" stroke-width="1.2"/>` + text(X(0) + 5, Y(y1) + 9, f.ylabel ?? "y", "start");
  const clip = `<clipPath id="c"><rect x="${L}" y="${T}" width="${W - L - R}" height="${H - T - B}"/></clipPath>`;
  let inner = "";
  if (f.shade) {
    const a = n(f.shade.from, scope), b = n(f.shade.to, scope), g = math.compile(fx(f.shade.f, scope));
    const pts = Array.from({ length: 61 }, (_, i) => a + ((b - a) * i) / 60).map((x) => `${X(x).toFixed(1)},${Y(Number(g.evaluate({ ...scope, x }))).toFixed(1)}`);
    inner += `<polygon points="${X(a).toFixed(1)},${Y(0)} ${pts.join(" ")} ${X(b).toFixed(1)},${Y(0)}" fill="${ACCENT}" fill-opacity="0.22" stroke="none"/>`;
  }
  if (f.field) {
    const g = math.compile(fx(f.field, scope)), nx = 11, ny = 9;
    for (let i = 0; i < nx; i++) for (let j = 0; j < ny; j++) {
      const x = x0 + ((x1 - x0) * (i + 0.5)) / nx, y = y0 + ((y1 - y0) * (j + 0.5)) / ny;
      const m = Number(g.evaluate({ ...scope, x, y }));
      if (!Number.isFinite(m)) continue;
      const ang = Math.atan2(-m * ((H - T - B) / (y1 - y0)), (W - L - R) / (x1 - x0)), r = 8;
      inner += `<line x1="${(X(x) - r * Math.cos(ang)).toFixed(1)}" y1="${(Y(y) - r * Math.sin(ang)).toFixed(1)}" x2="${(X(x) + r * Math.cos(ang)).toFixed(1)}" y2="${(Y(y) + r * Math.sin(ang)).toFixed(1)}" stroke="${ACCENT}" stroke-width="1.3"/>`;
    }
  }
  if (f.vfield) {
    const gx = math.compile(fx(f.vfield[0], scope)), gy = math.compile(fx(f.vfield[1], scope)), nx = 9, ny = 7;
    const cells: [number, number, number, number][] = [];
    for (let i = 0; i < nx; i++) for (let j = 0; j < ny; j++) {
      const x = x0 + ((x1 - x0) * (i + 0.5)) / nx, y = y0 + ((y1 - y0) * (j + 0.5)) / ny;
      cells.push([x, y, Number(gx.evaluate({ ...scope, x, y })), Number(gy.evaluate({ ...scope, x, y }))]);
    }
    const big = Math.max(...cells.map((c) => Math.hypot(c[2], c[3])), 1e-9);
    for (const [x, y, u, v] of cells) {
      const k = 15 / big, dx = u * k, dy = -v * k;
      if (Math.hypot(dx, dy) < 1.5) continue;
      inner += arrowHead(X(x) - dx / 2, Y(y) - dy / 2, X(x) + dx / 2, Y(y) + dy / 2, ACCENT, 4);
    }
  }
  for (const c of f.curves ?? []) {
    const a = n(c.from ?? x0, scope), b = n(c.to ?? x1, scope), g = math.compile(fx(c.f, scope));
    let d = "", pen = false;
    for (let i = 0; i <= 240; i++) {
      const x = a + ((b - a) * i) / 240, y = Number(g.evaluate({ ...scope, x }));
      if (!Number.isFinite(y) || y < y0 - (y1 - y0) || y > y1 + (y1 - y0)) { pen = false; continue; }
      d += `${pen ? "L" : "M"}${X(x).toFixed(1)} ${Y(y).toFixed(1)} `;
      pen = true;
    }
    inner += `<path d="${d}" stroke="${c.color === "hot" ? HOT : ACCENT}" stroke-width="2" ${c.dash ? 'stroke-dasharray="5 4"' : ""}/>`;
  }
  for (const v of f.vlines ?? []) inner += `<line x1="${X(n(v, scope)).toFixed(1)}" y1="${Y(y0)}" x2="${X(n(v, scope)).toFixed(1)}" y2="${Y(y1)}" stroke-dasharray="4 4" opacity="0.7"/>`;
  for (const v of f.hlines ?? []) inner += `<line x1="${X(x0)}" y1="${Y(n(v, scope)).toFixed(1)}" x2="${X(x1)}" y2="${Y(n(v, scope)).toFixed(1)}" stroke-dasharray="4 4" opacity="0.7"/>`;
  for (const g of f.segments ?? []) { const p = arr(g.from, scope), q = arr(g.to, scope); inner += `<line x1="${X(p[0]).toFixed(1)}" y1="${Y(p[1]).toFixed(1)}" x2="${X(q[0]).toFixed(1)}" y2="${Y(q[1]).toFixed(1)}" stroke="${ACCENT}" stroke-width="2" ${g.dash ? 'stroke-dasharray="5 4"' : ""}/>`; }
  for (const c of f.circles ?? []) {
    const [cx, cy] = arr(c.at, scope), r = n(c.r, scope);
    inner += `<ellipse cx="${X(cx).toFixed(1)}" cy="${Y(cy).toFixed(1)}" rx="${Math.abs(X(r) - X(0)).toFixed(1)}" ry="${Math.abs(Y(r) - Y(0)).toFixed(1)}" stroke="${ACCENT}" stroke-width="1.4" ${c.dash ? 'stroke-dasharray="4 4"' : ""}/>`;
  }
  for (const c of f.arcs ?? []) {
    const [cx, cy] = arr(c.at, scope), r = n(c.r, scope), a0 = n(c.from, scope), a1 = n(c.to, scope);
    let d = "";
    for (let k = 0; k <= 40; k++) { const t = ((a0 + ((a1 - a0) * k) / 40) * Math.PI) / 180; d += `${k ? "L" : "M"}${X(cx + r * Math.cos(t)).toFixed(1)},${Y(cy + r * Math.sin(t)).toFixed(1)}`; }
    inner += `<path d="${d}" stroke="${ACCENT}" stroke-width="1.4" ${c.dash ? 'stroke-dasharray="4 4"' : ""}/>`;
  }
  for (const g of f.arrows ?? []) { const p = arr(g.from, scope), q = arr(g.to, scope); inner += arrowHead(X(p[0]), Y(p[1]), X(q[0]), Y(q[1]), g.color === "hot" ? HOT : ACCENT, 7); }
  let top = "";
  for (const p of f.points ?? []) {
    const [px, py] = arr(p.at, scope);
    top += `<circle cx="${X(px).toFixed(1)}" cy="${Y(py).toFixed(1)}" r="4" fill="${p.open ? "var(--odd-bg, #fff)" : ACCENT}" stroke="${ACCENT}" stroke-width="1.6"/>`;
    if (p.label) top += text(X(px) + 7, Y(py) - 7, str(p.label, scope), "start");
  }
  if (f.scatter) {
    const xs = arr(f.scatter.x, scope), ys = arr(f.scatter.y, scope);
    xs.forEach((px, i) => { top += `<circle cx="${X(px).toFixed(1)}" cy="${Y(ys[i]).toFixed(1)}" r="3.4" fill="${ACCENT}" stroke="none"/>`; });
  }
  for (const l of f.labels ?? []) { const [lx, ly] = arr(l.at, scope); top += text(X(lx), Y(ly), str(l.text, scope)); }
  return svg(W, H, `${clip}${s}<g clip-path="url(#c)">${inner}</g>${top}`);
}

function numberline(f: any, scope: Scope): string {
  const [a, b] = arr(f.range, scope), step = f.step ? n(f.step, scope) : tickStep(b - a);
  const dots = f.dots ? arr(f.dots, scope) : [], le = f.labelEvery ? n(f.labelEvery, scope) : 0;
  const counts = new Map<number, number>();
  for (const d of dots) counts.set(d, (counts.get(d) ?? 0) + 1);
  const tall = Math.max(0, ...counts.values());
  const H = 54 + tall * 11 + (f.box ? 34 : 0), L = 18, yAxis = H - 26;
  const X = (x: number) => L + ((x - a) / (b - a)) * (W - 2 * L);
  let s = arrowHead(L - 8, yAxis, W - L + 8, yAxis, "currentColor", 5) + arrowHead(W - L + 8, yAxis, L - 8, yAxis, "currentColor", 5);
  for (let x = a; x <= b + 1e-9; x += step) s += `<line x1="${X(x).toFixed(1)}" y1="${yAxis - 4}" x2="${X(x).toFixed(1)}" y2="${yAxis + 4}"/>` + (f.hideLabels || (le && Math.abs(x / le - Math.round(x / le)) > 1e-6) ? "" : text(X(x), yAxis + 17, nice(x)));
  for (const [v, c] of counts) for (let i = 0; i < c; i++) s += `<circle cx="${X(v).toFixed(1)}" cy="${yAxis - 11 - i * 11}" r="4.2" fill="${ACCENT}" stroke="none"/>`;
  if (f.box) {
    const q = (k: string) => X(n(f.box[k], scope)), y = yAxis - 22 - tall * 11, h = 20;
    s += `<line x1="${q("min")}" y1="${y}" x2="${q("q1")}" y2="${y}"/><line x1="${q("q3")}" y1="${y}" x2="${q("max")}" y2="${y}"/><rect x="${q("q1")}" y="${y - h / 2}" width="${q("q3") - q("q1")}" height="${h}" fill="${ACCENT}" fill-opacity="0.2" stroke="${ACCENT}"/><line x1="${q("med")}" y1="${y - h / 2}" x2="${q("med")}" y2="${y + h / 2}" stroke="${ACCENT}" stroke-width="2"/><line x1="${q("min")}" y1="${y - 6}" x2="${q("min")}" y2="${y + 6}"/><line x1="${q("max")}" y1="${y - 6}" x2="${q("max")}" y2="${y + 6}"/>`;
  }
  if (f.interval) {
    const p = X(n(f.interval.from, scope)), q = X(n(f.interval.to, scope));
    s += `<line x1="${p}" y1="${yAxis}" x2="${q}" y2="${yAxis}" stroke="${ACCENT}" stroke-width="4"/>`;
  }
  for (const p of f.points ?? []) {
    const px = X(n(p.at, scope));
    s += `<circle cx="${px.toFixed(1)}" cy="${yAxis}" r="4.5" fill="${p.open ? "var(--odd-bg, #fff)" : ACCENT}" stroke="${ACCENT}" stroke-width="1.6"/>`;
    if (p.label) s += text(px, yAxis - 10, str(p.label, scope));
  }
  return svg(W, H, s);
}

function grid(f: any, scope: Scope): string {
  const cols = n(f.cols, scope), rows = n(f.rows, scope), shaded = f.shaded === undefined ? 0 : n(f.shaded, scope);
  const count = f.count === undefined ? cols * rows : n(f.count, scope);
  const cell = Math.min(30, Math.floor((W - 20) / cols)), H = rows * cell + 20, x0 = (W - cols * cell) / 2;
  let s = "";
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
    const i = r * cols + c, x = x0 + c * cell, y = 10 + r * cell;
    if (f.dots) { if (i < count) s += `<circle cx="${x + cell / 2}" cy="${y + cell / 2}" r="${cell * 0.3}" fill="${ACCENT}" stroke="none"/>`; }
    else s += `<rect x="${x}" y="${y}" width="${cell}" height="${cell}" ${i < shaded ? `fill="${ACCENT}" fill-opacity="0.35"` : ""}/>`;
  }
  return svg(W, H, s);
}

function bars(f: any, scope: Scope): string {
  const vals = arr(f.values, scope), labels: string[] = f.labels.map((l: unknown) => str(l, scope));
  const H = 190, B = 26, L = 30, top = Math.max(...vals), step = tickStep(top), max = Math.ceil(top / step) * step;
  const bw = (W - L - 12) / vals.length;
  let s = `<line x1="${L}" y1="${H - B}" x2="${W - 8}" y2="${H - B}"/>`;
  for (let v = 0; v <= max + 1e-9; v += step) { const y = H - B - (v / max) * (H - B - 12); s += `<line x1="${L}" y1="${y}" x2="${W - 8}" y2="${y}" opacity="0.13"/>` + text(L - 4, y + 4, nice(v), "end"); }
  vals.forEach((v, i) => { const h = (v / max) * (H - B - 12); s += `<rect x="${L + i * bw + bw * 0.15}" y="${H - B - h}" width="${bw * 0.7}" height="${h}" fill="${ACCENT}" fill-opacity="0.45" stroke="${ACCENT}"/>` + text(L + i * bw + bw / 2, H - B + 15, labels[i]); });
  return svg(W, H, s);
}

function table(f: any, scope: Scope): string {
  const cell = (c: unknown) => (typeof c === "number" ? nice(c) : str(c, scope));
  const g = f.f ? math.compile(fx(f.f, scope)) : null;
  const head: string[] = f.head.map(cell);
  const rows: string[][] = g ? arr(f.xs, scope).map((x) => [nice(x), nice(Number(g.evaluate({ ...scope, x })))]) : f.rows.map((r: unknown[]) => r.map(cell));
  const cw = Math.min(70, (W - 10) / head.length), rh = 22, w = cw * head.length + 2, H = rh * (rows.length + 1) + 4;
  let s = `<rect x="1" y="1" width="${w - 2}" height="${rh}" fill="${ACCENT}" fill-opacity="0.15" stroke="none"/>`;
  [head, ...rows].forEach((r, i) => { r.forEach((c, j) => { s += text(1 + j * cw + cw / 2, 1 + i * rh + 15, c, "middle", i === 0 ? 'font-weight="600"' : ""); }); s += `<line x1="1" y1="${1 + (i + 1) * rh}" x2="${w - 1}" y2="${1 + (i + 1) * rh}" opacity="0.35"/>`; });
  for (let j = 0; j <= head.length; j++) s += `<line x1="${1 + j * cw}" y1="1" x2="${1 + j * cw}" y2="${H - 3}" opacity="0.35"/>`;
  return svg(w, H, s);
}

/** a skeletal structure: unlabelled vertices are carbons, hydrogens on carbon are implied.
 *  A label that starts with H ("H2N", "HO") is right-aligned so its heavy atom sits on the vertex. */
function molecule(f: any, scope: Scope): string {
  const atoms: [number, number, string][] = (f.atoms as any[]).map((a) => [n(a[0], scope), n(a[1], scope), String(a[2] ?? "")]);
  const xs = atoms.map((a) => a[0]), ys = atoms.map((a) => a[1]);
  const S = 38, MX = 40, MY = 24, minX = Math.min(...xs), maxY = Math.max(...ys);
  const w = (Math.max(...xs) - minX) * S + 2 * MX, h = (maxY - Math.min(...ys)) * S + 2 * MY;
  const X = (x: number) => MX + (x - minX) * S, Y = (y: number) => MY + (maxY - y) * S;
  let s = "";
  for (const b of f.bonds as number[][]) {
    const [i, j, order = 1, side = 0] = b, A = atoms[i], B = atoms[j];
    let x1 = X(A[0]), y1 = Y(A[1]), x2 = X(B[0]), y2 = Y(B[1]);
    const len = Math.hypot(x2 - x1, y2 - y1), ux = (x2 - x1) / len, uy = (y2 - y1) / len;
    // stop short of a label so the line does not run through the letters
    // … and further when it leaves on the side the label's hydrogens are written on
    const gap = (lab: string, dx: number) => (lab ? 9 + Math.max(0, (/^H\d?[A-Z]/.test(lab) ? -1 : 1) * dx) * 7 * (lab.length - 1) : 0);
    const ga = gap(A[2], ux), gb = gap(B[2], -ux);
    x1 += ux * ga; y1 += uy * ga; x2 -= ux * gb; y2 -= uy * gb;
    const line = (o: number, trim: number) => `<line x1="${(x1 - uy * o + ux * trim).toFixed(1)}" y1="${(y1 + ux * o + uy * trim).toFixed(1)}" x2="${(x2 - uy * o - ux * trim).toFixed(1)}" y2="${(y2 + ux * o - uy * trim).toFixed(1)}" stroke-width="1.6"/>`;
    // a ring double bond keeps its main line on the ring and puts the second, shorter one inside (side = ±1)
    if (order === 2 && side) s += line(0, 0) + line(4.6 * side, 5);
    // order 0: a coordinate (dative) bond to a metal, drawn dashed
    else if (order === 0) s += line(0, 0).replace("/>", ' stroke-dasharray="3 3"/>');
    else for (const o of order === 2 ? [-2.3, 2.3] : order === 3 ? [-3.8, 0, 3.8] : [0]) s += line(o, 0);
  }
  for (const [x, y, lab] of atoms) {
    if (!lab) continue;
    // letters on the baseline, digits dropped, a trailing charge raised
    let level = 0;
    const sub = (lab.match(/[A-Za-z]+|\d+|[+-]/g) ?? []).map((tok) => {
      const want = /\d/.test(tok) ? 3 : /[+-]/.test(tok) ? -5 : 0, dy = want - level;
      level = want;
      return `<tspan dy="${dy}" font-size="${want ? 9 : 13}">${tok === "-" ? "−" : tok}</tspan>`;
    }).join("");
    const hFirst = /^H\d?[A-Z]/.test(lab);
    s += /^[A-Z][a-z]?[+-]?$/.test(lab) ? text(X(x), Y(y) + 4.5, sub, "middle", 'font-size="13"')
      : hFirst ? text(X(x) + 5, Y(y) + 4.5, sub, "end", 'font-size="13"')
      : text(X(x) - 5, Y(y) + 4.5, sub, "start", 'font-size="13"');
  }
  return svg(Math.max(w, 120), Math.max(h, 70), s);
}

export function renderFigure(f: any, scope: Scope): string {
  switch (f?.type) {
    case "plot": return plot(f, scope);
    case "numberline": return numberline(f, scope);
    case "grid": return grid(f, scope);
    case "bars": return bars(f, scope);
    case "table": return table(f, scope);
    case "molecule": return molecule(f, scope);
    default: throw new Error(`unknown figure type ${f?.type}`);
  }
}
