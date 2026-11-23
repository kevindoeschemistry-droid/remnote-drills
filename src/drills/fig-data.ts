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
//                     bonds: [[i, j, order], …] (0-based atom indices; order 1, 2 or 3; 0 = a dashed coordinate or hydrogen bond). A skeletal structure.
//                     arrows: [[from, to, bend], …] curved electron-pushing arrows; an end is an atom index or a pair [i, j]
//                     (the middle of that bond, or of the bond about to form); bend sets the curve's side and depth
//                     notes: [[x, y, text], …] plain captions (residue names)
//   type: cubes       heights: [[…], …] stacks of unit cubes seen from the front right (row 0 at the back, column 0 at the left)
//   type: scheme      panels: [figure, …] stacked top to bottom with an arrow between; a panel may carry `caption`
//   type: views       heights: as for cubes; show: [top, front, end]; outline: true for the silhouette only; mask: 0/1 grid drawn as an outline; labels: false
//                     grids may be packed as 1abcdefghi; options: [grid, …] + view draws lettered candidate views; masks: [grid, …] lettered outlines
//   type: geom        polys: [{ pts | angles: [A, B] | sides3: [a, b, c] | sector: { c, r, from, to }, names, sides, fill }] · segs: [{ a, b | side: [poly, i], label, dash, line, hot, flip }]
//                     angles: [{ corner: [poly, vertex] | at, a1, a2, label, right, hot, arcs }] · ticks / par: [{ side: [poly, i] | a, b, n }]
//                     circles: [{ c, r }] · dots: [{ p, label, dir }] · texts: [{ p, s }] · transversal: { angle, marks: [[0|1, UR|UL|LL|LR, label], …] }   (geom.ts)
//   type: solid       kind: box | cylinder | cone | sphere | hemisphere | pyramid | cone-cylinder | tri-prism · dims · labels · diagonal
//   type: prism       profile: hex 1v1v2… (digit = 4x + z), depth; view 0 top, 1 front, 2 end, 3 isometric (default); options: [profile, …] lettered outlines
// Every number may be an expression in the template's givens and lets. A function (`f`, `field`, a
// `vfield` component) may also be the name of a text field of the drawn case. Strokes use currentColor.
import { math } from "./check";
import { geomSvg, solidSvg, corner, triFromAngles, triFromSides, transversal, sectorPts, type GeomFig, type Pt } from "./geom";

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
  const notes: [number, number, string][] = ((f.notes ?? []) as any[]).map((q) => [n(q[0], scope), n(q[1], scope), String(q[2])]);
  const xs = [...atoms, ...notes].map((a) => a[0]), ys = [...atoms, ...notes].map((a) => a[1]);
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
  for (const [x, y, t] of notes) s += text(X(x), Y(y) + 4, t, "middle", 'font-size="11" opacity="0.7"');
  // curved arrows: a pair of electrons moves from the tail to the head
  for (const a of (f.arrows ?? []) as any[]) {
    const end = (e: any): [number, number] => (Array.isArray(e) ? [(X(atoms[e[0]][0]) + X(atoms[e[1]][0])) / 2, (Y(atoms[e[0]][1]) + Y(atoms[e[1]][1])) / 2] : [X(atoms[e][0]), Y(atoms[e][1])]);
    let [x1, y1] = end(a[0]), [x2, y2] = end(a[1]);
    const bend = Number(a[2] ?? 0.35), len = Math.hypot(x2 - x1, y2 - y1) || 1;
    const cx = (x1 + x2) / 2 - ((y2 - y1) / len) * bend * len, cy = (y1 + y2) / 2 + ((x2 - x1) / len) * bend * len;
    // start and stop a little short of the atoms, along the curve's end tangents
    const t1 = Math.hypot(cx - x1, cy - y1) || 1, t2 = Math.hypot(x2 - cx, y2 - cy) || 1;
    const g1 = Array.isArray(a[0]) ? 2 : 9, g2 = Array.isArray(a[1]) ? 3 : 10;
    x1 += ((cx - x1) / t1) * g1; y1 += ((cy - y1) / t1) * g1; x2 -= ((x2 - cx) / t2) * g2; y2 -= ((y2 - cy) / t2) * g2;
    const ang = Math.atan2(y2 - cy, x2 - cx), hd = 6;
    s += `<path d="M${x1.toFixed(1)},${y1.toFixed(1)} Q${cx.toFixed(1)},${cy.toFixed(1)} ${x2.toFixed(1)},${y2.toFixed(1)}" stroke="${HOT}" stroke-width="1.5"/>`;
    s += `<polygon points="${x2.toFixed(1)},${y2.toFixed(1)} ${(x2 - hd * Math.cos(ang - 0.45)).toFixed(1)},${(y2 - hd * Math.sin(ang - 0.45)).toFixed(1)} ${(x2 - hd * Math.cos(ang + 0.45)).toFixed(1)},${(y2 - hd * Math.sin(ang + 0.45)).toFixed(1)}" fill="${HOT}" stroke="none"/>`;
  }
  return svg(Math.max(w, 120), Math.max(h, 70), s);
}

/** a 3 x 3 grid given either as nested lists or packed as the ten-digit number 1abcdefghi (rows top to bottom) */
function grid9(g: any, scope: Scope): number[][] {
  if (Array.isArray(g)) return (g as any[][]).map((row) => row.map((v) => Math.round(n(v, scope))));
  const d = String(Math.round(n(g, scope))).slice(1).padStart(9, "0");
  return [0, 1, 2].map((r) => [0, 1, 2].map((c) => Number(d[r * 3 + c])));
}

/** stacked unit cubes in isometric view: heights[r][c] cubes in each column, row 0 at the back, column 0 at the left */
function cubes(f: any, scope: Scope): string {
  const H = grid9(f.heights, scope);
  const R = H.length, C = H[0].length, top = Math.max(1, ...H.flat()), U = 26, cx = Math.cos(Math.PI / 6) * U, cy = Math.sin(Math.PI / 6) * U;
  const ox = R * cx + 10, oy = top * U + 10, wd = (R + C) * cx + 20, ht = top * U + (R + C) * cy + 20;
  // a grid corner (col c, row r, height z) on the page: columns run down-right, rows down-left, height up
  const P = (c: number, r: number, z: number) => `${(ox + (c - r) * cx).toFixed(1)},${(oy + (c + r) * cy - z * U).toFixed(1)}`;
  const face = (pts: string[], fill: string) => `<polygon points="${pts.join(" ")}" fill="${fill}" stroke="#333" stroke-width="1" stroke-linejoin="round"/>`;
  let s = "";
  for (let r = 0; r < R; r++) for (let c = 0; c < C; c++) for (let z = 0; z < H[r][c]; z++) {
    s += face([P(c, r + 1, z), P(c + 1, r + 1, z), P(c + 1, r + 1, z + 1), P(c, r + 1, z + 1)], "#d9d9d9"); // front
    s += face([P(c + 1, r, z), P(c + 1, r + 1, z), P(c + 1, r + 1, z + 1), P(c + 1, r, z + 1)], "#b8b8b8"); // right
    s += face([P(c, r, z + 1), P(c + 1, r, z + 1), P(c + 1, r + 1, z + 1), P(c, r + 1, z + 1)], "#f5f5f5"); // top
  }
  return svg(wd, ht, s);
}

/** one orthographic view of a cube stack as a grid of depth columns: occ[v][u] lists what the eye meets, nearest first */
function viewColumns(H: number[][], which: string): boolean[][][] {
  const R = H.length, C = H[0].length, top = Math.max(1, ...H.flat());
  const at = (r: number, c: number, z: number) => H[r][c] > z;
  if (which === "top") return H.map((row, r) => row.map((_, c) => Array.from({ length: top }, (_, d) => at(r, c, top - 1 - d))));
  if (which === "front") return Array.from({ length: top }, (_, v) => Array.from({ length: C }, (_, c) => Array.from({ length: R }, (_, d) => at(R - 1 - d, c, top - 1 - v))));
  if (which === "end") return Array.from({ length: top }, (_, v) => Array.from({ length: R }, (_, u) => Array.from({ length: C }, (_, d) => at(R - 1 - u, C - 1 - d, top - 1 - v))));
  throw new Error(`unknown view ${which}`);
}

/** line segments of a view: an edge is drawn where neighbouring depth columns differ, solid when the nearest surfaces differ, dashed when only something behind does */
function viewLines(occ: boolean[][][], U: number, x0: number, y0: number): string {
  const Hh = occ.length, W = occ[0].length, none: boolean[] = [];
  const col = (v: number, u: number) => (v < 0 || u < 0 || v >= Hh || u >= W ? none : occ[v][u]);
  const kind = (a: boolean[], b: boolean[]) => {
    const n = Math.max(a.length, b.length);
    let differ = false;
    for (let i = 0; i < n; i++) if (!!a[i] !== !!b[i]) differ = true;
    if (!differ) return 0;
    return a.indexOf(true) !== b.indexOf(true) ? 1 : 2;
  };
  let solid = "", dash = "";
  const seg = (k: number, x1: number, y1: number, x2: number, y2: number) => {
    const d = `M${(x0 + x1 * U).toFixed(1)},${(y0 + y1 * U).toFixed(1)} L${(x0 + x2 * U).toFixed(1)},${(y0 + y2 * U).toFixed(1)} `;
    if (k === 1) solid += d; else if (k === 2) dash += d;
  };
  for (let v = 0; v <= Hh; v++) for (let u = 0; u < W; u++) seg(kind(col(v - 1, u), col(v, u)), u, v, u + 1, v);
  for (let v = 0; v < Hh; v++) for (let u = 0; u <= W; u++) seg(kind(col(v, u - 1), col(v, u)), u, v, u, v + 1);
  return (dash ? `<path d="${dash}" stroke="#333" stroke-width="1.2" stroke-dasharray="4 3"/>` : "") + (solid ? `<path d="${solid}" stroke="#333" stroke-width="1.8" stroke-linecap="round"/>` : "");
}

/** orthographic views of a cube stack, laid out as on the DAT: top above front, end to the right of front.
 *  `show` picks the views, `outline` keeps only the silhouette, `mask` draws the outline of a 0/1 grid instead */
function views(f: any, scope: Scope): string {
  const U = 22, PAD = 12, GAP = 26, LBL = f.labels === false ? 0 : 16;
  const lettered = (cells: boolean[][][][]) => {
    // candidate drawings side by side, each with its letter underneath
    let x = PAD, body = "", ht = 0;
    cells.forEach((occ, i) => {
      body += viewLines(occ, U, x, PAD);
      body += text(x + (occ[0].length * U) / 2, PAD + occ.length * U + 15, "ABCDEF"[i], "middle", 'font-size="12" font-weight="600"');
      x += occ[0].length * U + GAP; ht = Math.max(ht, occ.length * U);
    });
    return svg(x - GAP + PAD, ht + 2 * PAD + 18, body);
  };
  const asMask = (g: any) => grid9(g, scope).map((row) => row.map((v) => [v > 0]));
  if (f.masks) return lettered((f.masks as any[]).map(asMask));
  if (f.mask) {
    const M = asMask(f.mask);
    return svg(M[0].length * U + 2 * PAD, M.length * U + 2 * PAD, viewLines(M, U, PAD, PAD));
  }
  if (f.options) {
    const w = ["top", "front", "end"][Math.round(n(f.view, scope))];
    return lettered((f.options as any[]).map((g) => viewColumns(grid9(g, scope), w)));
  }
  const H = grid9(f.heights, scope);
  const show: string[] = f.view !== undefined ? [["top", "front", "end"][Math.round(n(f.view, scope))]] : f.show ?? ["top", "front", "end"];
  const flat = (o: boolean[][][]) => (f.outline ? o.map((row) => row.map((c) => [c.some(Boolean)])) : o);
  const R = H.length, C = H[0].length, top = Math.max(1, ...H.flat());
  const size: Record<string, [number, number]> = { top: [C, R], front: [C, top], end: [R, top] };
  const pos: Record<string, [number, number]> = { top: [0, 0], front: [0, 0], end: [0, 0] };
  const hasTop = show.includes("top"), hasFront = show.includes("front");
  const lowY = hasTop ? R * U + LBL + GAP : 0;
  pos.front = [0, lowY];
  pos.end = [hasFront || hasTop ? C * U + GAP : 0, lowY];
  let s = "", wd = 0, ht = 0;
  for (const w of show) {
    const [x, y] = pos[w], [a, b] = size[w];
    s += viewLines(flat(viewColumns(H, w)), U, PAD + x, PAD + y);
    if (LBL) s += text(PAD + x + (a * U) / 2, PAD + y + b * U + 13, w.toUpperCase(), "middle", 'font-size="10"');
    wd = Math.max(wd, x + a * U); ht = Math.max(ht, y + b * U + LBL);
  }
  return svg(wd + 2 * PAD, ht + 2 * PAD, s);
}

/** a prism profile packed as the hex number 1v1v2…, one digit per corner, digit = 4x + z with x, z in 0..3 */
function profile(code: any, scope: Scope): [number, number][] {
  const d = Math.round(n(code, scope)).toString(16).slice(1);
  return [...d].map((ch) => { const v = parseInt(ch, 16); return [v >> 2, v & 3] as [number, number]; });
}

/** a prism: the profile (in the front plane, x right and z up) pushed straight back by `depth`.
 *  view 3 (default) is the isometric picture, 0/1/2 the top, front and end views; `options` draws lettered outlines */
function prism(f: any, scope: Scope): string {
  const U = 26, PAD = 12, GAP = 26;
  const outline = (P: [number, number][], x0: number, y0: number, zmax: number, xmin: number) =>
    `<polygon points="${P.map(([x, z]) => `${(x0 + (x - xmin) * U).toFixed(1)},${(y0 + (zmax - z) * U).toFixed(1)}`).join(" ")}" stroke="#333" stroke-width="1.8" stroke-linejoin="round"/>`;
  const box = (P: [number, number][]) => ({ x0: Math.min(...P.map((p) => p[0])), x1: Math.max(...P.map((p) => p[0])), z0: Math.min(...P.map((p) => p[1])), z1: Math.max(...P.map((p) => p[1])) });
  if (f.options) {
    let x = PAD, body = "", ht = 0;
    (f.options as any[]).forEach((code, i) => {
      const P = profile(code, scope), b = box(P);
      body += outline(P, x, PAD, b.z1, b.x0);
      body += text(x + ((b.x1 - b.x0) * U) / 2, PAD + 3 * U + 15, "ABCDEF"[i], "middle", 'font-size="12" font-weight="600"');
      x += (b.x1 - b.x0) * U + GAP; ht = 3 * U;
    });
    return svg(x - GAP + PAD, ht + 2 * PAD + 18, body);
  }
  const P = profile(f.profile, scope), D = Math.round(n(f.depth, scope)), view = f.view === undefined ? 3 : Math.round(n(f.view, scope));
  const b = box(P), N = P.length;
  // the highest (axis 1) or rightmost (axis 0) point of the profile on a grid line
  const reach = (axis: number, at: number) => {
    let best = -Infinity;
    for (let i = 0; i < N; i++) {
      const p = P[i], q = P[(i + 1) % N], a = p[1 - axis], c = q[1 - axis];
      if (a === at && c === at) best = Math.max(best, p[axis], q[axis]);
      else if ((a - at) * (c - at) <= 0 && a !== c) best = Math.max(best, p[axis] + ((q[axis] - p[axis]) * (at - a)) / (c - a));
    }
    return best;
  };
  const style = (axis: number, at: number) => (P.some((p) => p[1 - axis] === at && Math.abs(p[axis] - reach(axis, at)) < 1e-9) ? 1 : 2);
  const line = (k: number, x1: number, y1: number, x2: number, y2: number) =>
    `<path d="M${x1.toFixed(1)},${y1.toFixed(1)} L${x2.toFixed(1)},${y2.toFixed(1)}" stroke="#333" ${k === 1 ? 'stroke-width="1.8"' : 'stroke-width="1.2" stroke-dasharray="4 3"'}/>`;
  if (view === 1) return svg((b.x1 - b.x0) * U + 2 * PAD, (b.z1 - b.z0) * U + 2 * PAD, outline(P, PAD, PAD, b.z1, b.x0));
  if (view === 0) {
    const W = (b.x1 - b.x0) * U, Hh = D * U;
    let s = `<rect x="${PAD}" y="${PAD}" width="${W}" height="${Hh}" stroke="#333" stroke-width="1.8"/>`;
    for (const x of new Set(P.map((p) => p[0]))) if (x > b.x0 && x < b.x1) s += line(style(1, x), PAD + (x - b.x0) * U, PAD, PAD + (x - b.x0) * U, PAD + Hh);
    return svg(W + 2 * PAD, Hh + 2 * PAD, s);
  }
  if (view === 2) {
    const W = D * U, Hh = (b.z1 - b.z0) * U;
    let s = `<rect x="${PAD}" y="${PAD}" width="${W}" height="${Hh}" stroke="#333" stroke-width="1.8"/>`;
    for (const z of new Set(P.map((p) => p[1]))) if (z > b.z0 && z < b.z1) s += line(style(0, z), PAD, PAD + (b.z1 - z) * U, PAD + W, PAD + (b.z1 - z) * U);
    return svg(W + 2 * PAD, Hh + 2 * PAD, s);
  }
  // isometric picture, drawn as the cube stacks are: x runs down-right, depth runs up-right, z up
  const cx = Math.cos(Math.PI / 6) * U, cy = Math.sin(Math.PI / 6) * U;
  const ox = D * cx + PAD, oy = b.z1 * U + PAD;
  const Q = (x: number, r: number, z: number) => `${(ox + (x - r) * cx).toFixed(1)},${(oy + (x + r) * cy - z * U).toFixed(1)}`;
  let area = 0;
  for (let i = 0; i < N; i++) area += P[i][0] * P[(i + 1) % N][1] - P[(i + 1) % N][0] * P[i][1];
  const sides: { key: number; svg: string }[] = [];
  for (let i = 0; i < N; i++) {
    const p = P[i], q = P[(i + 1) % N], sgn = area > 0 ? 1 : -1;
    const nx = (q[1] - p[1]) * sgn, nz = -(q[0] - p[0]) * sgn; // outward normal of this side face
    if (nx + nz <= 0) continue; // turned away from the eye
    const fill = nx > 0 && nz > 0 ? "#cdcdcd" : nx > 0 ? "#b8b8b8" : "#f5f5f5";
    sides.push({ key: p[0] + q[0] + p[1] + q[1], svg: `<polygon points="${[Q(p[0], D, p[1]), Q(q[0], D, q[1]), Q(q[0], 0, q[1]), Q(p[0], 0, p[1])].join(" ")}" fill="${fill}" stroke="#333" stroke-width="1" stroke-linejoin="round"/>` });
  }
  sides.sort((u, v) => u.key - v.key);
  const front = `<polygon points="${P.map((p) => Q(p[0], D, p[1])).join(" ")}" fill="#d9d9d9" stroke="#333" stroke-width="1" stroke-linejoin="round"/>`;
  return svg((D + b.x1) * cx + 2 * PAD, b.z1 * U + (D + b.x1) * cy + 2 * PAD, sides.map((q) => q.svg).join("") + front);
}

/** figures stacked top to bottom, an arrow between each pair: the states of a mechanism */
function scheme(f: any, scope: Scope): string {
  const parts = (f.panels as any[]).map((p) => {
    const inner = renderFigure(p, scope), m = /viewBox="0 0 ([\d.]+) ([\d.]+)"/.exec(inner)!;
    return { inner, w: Number(m[1]), h: Number(m[2]), caption: p.caption ? str(p.caption, scope) : "" };
  });
  const Wd = Math.max(...parts.map((p) => p.w)), GAP = 30;
  let y = 0, body = "";
  parts.forEach((p, i) => {
    if (p.caption) { body += text(Wd / 2, y + 13, p.caption, "middle", 'font-size="12"'); y += 18; }
    body += p.inner.replace(/^<svg [^>]*>/, `<svg xmlns="http://www.w3.org/2000/svg" x="${((Wd - p.w) / 2).toFixed(1)}" y="${y}" width="${p.w}" height="${p.h}" viewBox="0 0 ${p.w} ${p.h}" font-family="system-ui, sans-serif" font-size="11" fill="none" stroke="currentColor">`);
    y += p.h;
    if (i < parts.length - 1) { if (f.plain) y += 10; else { body += arrowHead(Wd / 2, y + 4, Wd / 2, y + GAP - 6, "currentColor", 6); y += GAP; } }
  });
  return svg(Wd, y, body);
}

/** a code listing in a monospace font, indentation kept: `src` is the code, or the name of a case
 *  field holding it (taken raw, so braces in Java or Python are never read as {{ }} fills) */
function code(f: any, scope: Scope): string {
  const lines = fx(f.src, scope).replace(/\n$/, "").split("\n");
  const esc = (t: string) => t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/ /g, "\u00a0");
  // a long line shrinks the font (down to about 9 px at 63 characters) rather than running off the card
  const PAD = 6, longest = Math.max(...lines.map((l) => l.length));
  const fs = Math.min(11, (W - 2 * PAD) / (longest * 0.61)), CH = fs * 0.61, LH = fs * 1.36;
  const w = Math.min(W, Math.max(120, Math.ceil(longest * CH + 2 * PAD)));
  const h = lines.length * LH + 2 * PAD;
  let s = `<rect x="0.5" y="0.5" width="${w - 1}" height="${h - 1}" rx="4" fill="${ACCENT}" fill-opacity="0.06" stroke-opacity="0.3"/>`;
  lines.forEach((l, i) => { s += `<text x="${PAD}" y="${(PAD + (i + 1) * LH - 4).toFixed(1)}" fill="currentColor" stroke="none" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="${fs.toFixed(2)}" xml:space="preserve">${esc(l)}</text>`; });
  return svg(w, h, s);
}

/** a geometry figure (geom.ts) from a template: numbers may be expressions, labels may hold {{fills}};
 *  a polygon may be built from `angles: [A, B]` or `sides3: [a, b, c]` (a triangle), and an angle mark,
 *  tick or segment may name a corner or side as `corner: [polygon, vertex]` / `side: [polygon, i]` */
function geomData(f: any, scope: Scope): string {
  const L = (v: unknown) => (v == null ? null : str(v, scope));
  const P = (p: unknown): Pt => arr(p, scope) as Pt;
  const base: GeomFig = f.transversal ? transversal(n(f.transversal.angle, scope), f.transversal.marks.map((m: any[]) => [m[0], m[1], str(m[2], scope)]), f.transversal.parallel !== false) : {};
  const polys = (f.polys ?? []).map((pg: any) => {
    const pts: Pt[] = pg.angles ? triFromAngles(n(pg.angles[0], scope), n(pg.angles[1], scope)) : pg.sides3 ? triFromSides(...(arr(pg.sides3, scope) as [number, number, number]))
      : pg.sector ? sectorPts(P(pg.sector.c), n(pg.sector.r, scope), n(pg.sector.from, scope), n(pg.sector.to, scope)) : pg.pts.map(P);
    return { pts, names: pg.names?.map(L), sides: pg.sides?.map(L), fill: !!pg.fill, dash: !!pg.dash };
  });
  const side = (ref: unknown[]): [Pt, Pt] => { const q = polys[n(ref[0], scope)].pts, i = n(ref[1], scope); return [q[i], q[(i + 1) % q.length]]; };
  const ends = (x: any): [Pt, Pt] => (x.side ? side(x.side) : [P(x.a), P(x.b)]);
  return geomSvg({
    ...base,
    polys: [...(base.polys ?? []), ...polys],
    segs: [...(base.segs ?? []), ...(f.segs ?? []).map((g: any) => { const [a, b] = ends(g); return { a, b, label: L(g.label), dash: !!g.dash, line: !!g.line, hot: !!g.hot, side: g.flip ? -1 : 1 }; })],
    angles: [...(base.angles ?? []), ...(f.angles ?? []).map((a: any) => ({ ...(a.corner ? corner(polys[n(a.corner[0], scope)].pts, n(a.corner[1], scope)) : { at: P(a.at), a1: n(a.a1, scope), a2: n(a.a2, scope) }), label: L(a.label), right: typeof a.right === "string" ? !!n(a.right, scope) : !!a.right, hot: !!a.hot, arcs: a.arcs }))],
    ticks: (f.ticks ?? []).map((t: any) => { const [a, b] = ends(t); return { a, b, n: t.n ?? 1 }; }),
    par: [...(base.par ?? []), ...(f.par ?? []).map((t: any) => { const [a, b] = ends(t); return { a, b, n: t.n ?? 1 }; })],
    circles: (f.circles ?? []).map((c: any) => ({ c: P(c.c), r: n(c.r, scope), dash: !!c.dash })),
    dots: (f.dots ?? []).map((d: any) => ({ p: P(d.p), label: L(d.label), dir: d.dir == null ? undefined : n(d.dir, scope) })),
    texts: (f.texts ?? []).map((t: any) => ({ p: P(t.p), s: str(t.s, scope) })),
    width: base.width,
  });
}

export function renderFigure(f: any, scope: Scope): string {
  switch (f?.type) {
    case "plot": return plot(f, scope);
    case "numberline": return numberline(f, scope);
    case "grid": return grid(f, scope);
    case "bars": return bars(f, scope);
    case "table": return table(f, scope);
    case "molecule": return molecule(f, scope);
    case "scheme": return scheme(f, scope);
    case "cubes": return cubes(f, scope);
    case "views": return views(f, scope);
    case "prism": return prism(f, scope);
    case "code": return code(f, scope);
    case "geom": return geomData(f, scope);
    case "solid": return solidSvg({ kind: f.kind, dims: arr(f.dims, scope), labels: (f.labels ?? []).map((l: unknown) => (l == null ? null : str(l, scope))), diagonal: !!f.diagonal, units: !!f.units });
    default: throw new Error(`unknown figure type ${f?.type}`);
  }
}
