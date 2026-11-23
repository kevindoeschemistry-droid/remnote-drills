// Geometry figures for the K-12 drills: polygons with named vertices and labelled sides, angle
// arcs and right-angle boxes, congruence ticks, parallel arrows, circles, and the usual solids.
// Generators pass true coordinates (math axes, y up), so a figure is drawn to scale from the very
// numbers the answer is computed from. Unknowns are labelled "?" or "x"; a label never gives
// the answer away. Strokes use currentColor so the drawing follows the theme.

export type Pt = [number, number];
export interface GeomFig {
  /** closed polygons; names sit outside each vertex, sides[i] labels the side from pts[i] to pts[i+1] */
  polys?: { pts: Pt[]; names?: (string | null | undefined)[]; sides?: (string | null | undefined)[]; fill?: boolean; dash?: boolean }[];
  /** segments; `line: true` extends them a little past both ends with arrowheads */
  segs?: { a: Pt; b: Pt; label?: string | null; dash?: boolean; line?: boolean; hot?: boolean; side?: 1 | -1 }[];
  /** an angle at `at` swept counterclockwise from direction a1 to a2 (degrees) */
  angles?: { at: Pt; a1: number; a2: number; label?: string | null; right?: boolean; hot?: boolean; arcs?: number; thinSide?: 1 | 2 }[];
  /** congruence ticks (n strokes) at the middle of a segment */
  ticks?: { a: Pt; b: Pt; n: number }[];
  /** parallel arrowheads (n chevrons) at the middle of a segment, pointing from a to b */
  par?: { a: Pt; b: Pt; n: number }[];
  circles?: { c: Pt; r: number; dash?: boolean }[];
  dots?: { p: Pt; label?: string | null; dir?: number }[];
  texts?: { p: Pt; s: string }[];
  /** width in px (default 280) and the most height allowed */
  width?: number;
  maxHeight?: number;
}

const ACCENT = "#5b7cfa", HOT = "#e0654f";
const RAD = Math.PI / 180;
const f1 = (v: number) => v.toFixed(1);
const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
/** the SVG, with its box widened to take in every label (text extents are estimated at 7 px a character) */
function svg(w: number, h: number, body: string) {
  let x0 = 0, y0 = 0, x1 = w, y1 = h;
  for (const t of body.matchAll(/<text x="([-\d.]+)" y="([-\d.]+)" text-anchor="(\w+)"[^>]*>([^<]*)<\/text>/g)) {
    const x = +t[1], y = +t[2], len = t[4].replace(/&\w+;/g, "_").length * 7.2, a = t[3];
    const l = a === "start" ? x : a === "end" ? x - len : x - len / 2;
    x0 = Math.min(x0, l - 3); x1 = Math.max(x1, l + len + 3); y0 = Math.min(y0, y - 13); y1 = Math.max(y1, y + 4);
  }
  const W = x1 - x0, H = y1 - y0;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${f1(x0)} ${f1(y0)} ${f1(W)} ${f1(H)}" width="100%" style="max-width:${Math.round(W)}px" font-family="system-ui, sans-serif" font-size="13" fill="none" stroke="currentColor" stroke-linejoin="round">${body}</svg>`;
}
/** text placed so that it sits off (x, y) in direction (ux, uy) */
function label(x: number, y: number, ux: number, uy: number, s: string, gap = 9, extra = "") {
  const L = Math.hypot(ux, uy) || 1;
  ux /= L; uy /= L;
  const tx = x + ux * gap, ty = y + uy * gap;
  const anchor = ux > 0.35 ? "start" : ux < -0.35 ? "end" : "middle";
  const dy = uy > 0.35 ? 11 : uy < -0.35 ? -2 : 4.5;
  return `<text x="${f1(tx)}" y="${f1(ty + dy)}" text-anchor="${anchor}" fill="currentColor" stroke="none" ${extra}>${esc(s)}</text>`;
}
function head(x1: number, y1: number, x2: number, y2: number, color: string, h = 7) {
  const a = Math.atan2(y2 - y1, x2 - x1);
  return `<polygon points="${f1(x2)},${f1(y2)} ${f1(x2 - h * Math.cos(a - 0.4))},${f1(y2 - h * Math.sin(a - 0.4))} ${f1(x2 - h * Math.cos(a + 0.4))},${f1(y2 - h * Math.sin(a + 0.4))}" fill="${color}" stroke="none"/>`;
}

export function geomSvg(f: GeomFig): string {
  const W = f.width ?? 280, maxH = f.maxHeight ?? 230, pad = 30;
  const all: Pt[] = [];
  for (const p of f.polys ?? []) all.push(...p.pts);
  for (const s of f.segs ?? []) all.push(s.a, s.b);
  for (const c of f.circles ?? []) all.push([c.c[0] - c.r, c.c[1] - c.r], [c.c[0] + c.r, c.c[1] + c.r]);
  for (const d of f.dots ?? []) all.push(d.p);
  for (const a of f.angles ?? []) all.push(a.at);
  const xs = all.map((p) => p[0]), ys = all.map((p) => p[1]);
  const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
  const bw = Math.max(x1 - x0, 1e-9), bh = Math.max(y1 - y0, 1e-9);
  const k = Math.min((W - 2 * pad) / bw, (maxH - 2 * pad) / bh);
  const w = Math.max(bw * k + 2 * pad, 120), h = bh * k + 2 * pad;
  const ox = (w - bw * k) / 2;
  const X = (p: Pt) => ox + (p[0] - x0) * k, Y = (p: Pt) => pad + (y1 - p[1]) * k;
  const P = (p: Pt): Pt => [X(p), Y(p)];
  let s = "";
  // fills first, then lines, then marks, then text on top
  for (const pg of f.polys ?? []) {
    const pts = pg.pts.map(P);
    s += `<polygon points="${pts.map((q) => `${f1(q[0])},${f1(q[1])}`).join(" ")}" ${pg.fill ? `fill="${ACCENT}" fill-opacity="0.12"` : ""} stroke-width="1.8" ${pg.dash ? 'stroke-dasharray="5 4"' : ""}/>`;
  }
  for (const c of f.circles ?? []) s += `<circle cx="${f1(X(c.c))}" cy="${f1(Y(c.c))}" r="${f1(c.r * k)}" stroke-width="1.8" ${c.dash ? 'stroke-dasharray="5 4"' : ""}/>`;
  for (const sg of f.segs ?? []) {
    let [a, b] = [P(sg.a), P(sg.b)];
    const color = sg.hot ? HOT : "currentColor";
    if (sg.line) {
      const L = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1, ux = (b[0] - a[0]) / L, uy = (b[1] - a[1]) / L, e = 14;
      a = [a[0] - ux * e, a[1] - uy * e]; b = [b[0] + ux * e, b[1] + uy * e];
      s += head(b[0] - ux, b[1] - uy, b[0], b[1], color) + head(a[0] + ux, a[1] + uy, a[0], a[1], color);
    }
    s += `<line x1="${f1(a[0])}" y1="${f1(a[1])}" x2="${f1(b[0])}" y2="${f1(b[1])}" stroke="${color}" stroke-width="${sg.dash ? 1.3 : 1.8}" ${sg.dash ? 'stroke-dasharray="5 4"' : ""}/>`;
  }
  for (const t of f.ticks ?? []) {
    const a = P(t.a), b = P(t.b), mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, L = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1;
    const ux = (b[0] - a[0]) / L, uy = (b[1] - a[1]) / L;
    for (let i = 0; i < t.n; i++) {
      const o = (i - (t.n - 1) / 2) * 4.5, cx = mx + ux * o, cy = my + uy * o;
      s += `<line x1="${f1(cx - uy * 5)}" y1="${f1(cy + ux * 5)}" x2="${f1(cx + uy * 5)}" y2="${f1(cy - ux * 5)}" stroke-width="1.5"/>`;
    }
  }
  for (const t of f.par ?? []) {
    const a = P(t.a), b = P(t.b), mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, L = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1;
    const ux = (b[0] - a[0]) / L, uy = (b[1] - a[1]) / L;
    for (let i = 0; i < t.n; i++) {
      const o = (i - (t.n - 1) / 2) * 6 + 3, cx = mx + ux * o, cy = my + uy * o;
      s += `<polyline points="${f1(cx - ux * 6 - uy * 4.5)},${f1(cy - uy * 6 + ux * 4.5)} ${f1(cx)},${f1(cy)} ${f1(cx - ux * 6 + uy * 4.5)},${f1(cy - uy * 6 - ux * 4.5)}" stroke-width="1.5"/>`;
    }
  }
  for (const an of f.angles ?? []) {
    const [cx, cy] = P(an.at), color = an.hot ? HOT : ACCENT;
    // screen y points down: a math angle t is the direction (cos t, −sin t)
    const dir = (t: number): Pt => [Math.cos(t * RAD), -Math.sin(t * RAD)];
    let sweep = (((an.a2 - an.a1) % 360) + 360) % 360;
    if (sweep === 0) sweep = 360;
    if (an.right) {
      const u = dir(an.a1), v = dir(an.a2), r = 10;
      s += `<polyline points="${f1(cx + u[0] * r)},${f1(cy + u[1] * r)} ${f1(cx + (u[0] + v[0]) * r)},${f1(cy + (u[1] + v[1]) * r)} ${f1(cx + v[0] * r)},${f1(cy + v[1] * r)}" stroke="${color}" stroke-width="1.5"/>`;
    } else {
      const n = an.arcs ?? 1;
      for (let i = 0; i < n; i++) {
        const r = (sweep > 120 ? 14 : sweep < 35 ? 26 : 18) + i * 4;
        const u = dir(an.a1), v = dir(an.a1 + sweep);
        s += `<path d="M ${f1(cx + u[0] * r)} ${f1(cy + u[1] * r)} A ${r} ${r} 0 ${sweep > 180 ? 1 : 0} 0 ${f1(cx + v[0] * r)} ${f1(cy + v[1] * r)}" stroke="${color}" stroke-width="1.5"/>`;
      }
    }
    if (an.label) {
      // a thin angle has no room inside: its label goes just outside the first ray
      const thin = !an.right && (sweep < 40 || (!!an.thinSide && sweep < an.label.length * 4.5));
      const mid = dir(thin ? (an.thinSide === 2 ? an.a1 + sweep + 28 : an.a1 - 28) : an.a1 + sweep / 2), r = an.right ? 16 : thin ? 30 : (sweep > 120 ? 14 : sweep < 35 ? 26 : 18) + 4 * ((an.arcs ?? 1) - 1) + 3;
      s += label(cx + mid[0] * r, cy + mid[1] * r, mid[0], mid[1], an.label, 3, `fill="${color}"`).replace('fill="currentColor" ', "");
    }
  }
  for (const d of f.dots ?? []) {
    const [x, y] = P(d.p);
    s += `<circle cx="${f1(x)}" cy="${f1(y)}" r="3" fill="currentColor" stroke="none"/>`;
    if (d.label) { const t = (d.dir ?? 45) * RAD; s += label(x, y, Math.cos(t), -Math.sin(t), d.label, 7, 'font-style="italic"'); }
  }
  // side labels sit outside the polygon, vertex names beyond each corner
  for (const pg of f.polys ?? []) {
    const pts = pg.pts.map(P), n = pts.length;
    const cx = pts.reduce((a, q) => a + q[0], 0) / n, cy = pts.reduce((a, q) => a + q[1], 0) / n;
    pg.sides?.forEach((lab, i) => {
      if (!lab) return;
      const a = pts[i], b = pts[(i + 1) % n], mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2;
      let nx = -(b[1] - a[1]), ny = b[0] - a[0];
      if (nx * (mx - cx) + ny * (my - cy) < 0) { nx = -nx; ny = -ny; }
      s += label(mx, my, nx, ny, lab, 6);
    });
    pg.names?.forEach((nm, i) => {
      if (!nm) return;
      const q = pts[i], prev = pts[(i + n - 1) % n], next = pts[(i + 1) % n];
      // the outward bisector of the corner
      const u = [prev[0] - q[0], prev[1] - q[1]], v = [next[0] - q[0], next[1] - q[1]];
      const lu = Math.hypot(u[0], u[1]) || 1, lv = Math.hypot(v[0], v[1]) || 1;
      let bx = -(u[0] / lu + v[0] / lv), by = -(u[1] / lu + v[1] / lv);
      if (Math.hypot(bx, by) < 1e-6) { bx = q[0] - cx; by = q[1] - cy; }
      s += label(q[0], q[1], bx, by, nm, 5, 'font-style="italic"');
    });
  }
  for (const sg of f.segs ?? []) {
    if (!sg.label) continue;
    const a = P(sg.a), b = P(sg.b), side = sg.side ?? 1;
    s += label((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (b[1] - a[1]) * side, -(b[0] - a[0]) * side, sg.label, 6);
  }
  for (const t of f.texts ?? []) { const [x, y] = P(t.p); s += `<text x="${f1(x)}" y="${f1(y + 4.5)}" text-anchor="middle" fill="currentColor" stroke="none">${esc(t.s)}</text>`; }
  return svg(w, h, s);
}

// ── solids, drawn in oblique projection with the hidden edges dashed ──────────
export type SolidKind = "box" | "cylinder" | "cone" | "sphere" | "hemisphere" | "pyramid" | "cone-cylinder" | "tri-prism";
export interface SolidFig {
  kind: SolidKind;
  /** box: [l, w, h] · cylinder, cone, cone-cylinder: [r, h] · sphere, hemisphere: [r] · pyramid: [s, h] · tri-prism: [b, h, L] */
  dims: number[];
  /** the labels for the same dimensions, in the same order ("" or null for none) */
  labels: (string | null | undefined)[];
  /** box: draw the space diagonal */
  diagonal?: boolean;
  /** box: draw the unit cubes on the three faces in view */
  units?: boolean;
}

export function solidSvg(f: SolidFig): string {
  const d = f.dims.map((v) => Math.max(v, 1e-6)), L = f.labels;
  const dash = 'stroke-dasharray="4 4" stroke-width="1.2"';
  const ln = (a: Pt, b: Pt, extra = 'stroke-width="1.8"') => `<line x1="${f1(a[0])}" y1="${f1(a[1])}" x2="${f1(b[0])}" y2="${f1(b[1])}" ${extra}/>`;
  const lab = (a: Pt, b: Pt, ux: number, uy: number, s?: string | null) => (s ? label((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, ux, uy, s, 6) : "");
  const ell = (cx: number, cy: number, rx: number, ry: number, half: "front" | "back" | "all", extra = 'stroke-width="1.8"') =>
    half === "all" ? `<ellipse cx="${f1(cx)}" cy="${f1(cy)}" rx="${f1(rx)}" ry="${f1(ry)}" ${extra}/>`
      : `<path d="M ${f1(cx - rx)} ${f1(cy)} A ${f1(rx)} ${f1(ry)} 0 0 ${half === "front" ? 0 : 1} ${f1(cx + rx)} ${f1(cy)}" ${extra}/>`;
  const pad = 34;
  if (f.kind === "box" || f.kind === "tri-prism") {
    // front face in the plane of the page; depth runs up and to the right at 35°, foreshortened by half
    const [a, b, c] = f.kind === "box" ? d : [d[0], d[1], d[2]];
    const depth = f.kind === "box" ? b : c, wide = a, tall = f.kind === "box" ? c : b;
    const dx = Math.cos(35 * RAD) * 0.5 * depth, dy = Math.sin(35 * RAD) * 0.5 * depth;
    const k = Math.min(200 / (wide + dx), 150 / (tall + dy));
    const W = (wide + dx) * k + 2 * pad, H = (tall + dy) * k + 2 * pad;
    const o: Pt = [pad, H - pad], ex = dx * k, ey = dy * k, sw = wide * k, sh = tall * k;
    const p = (x: number, y: number, z: number): Pt => [o[0] + x * sw + z * ex, o[1] - y * sh - z * ey];
    let s = "";
    if (f.kind === "box") {
      const A = p(0, 0, 0), B = p(1, 0, 0), C = p(1, 1, 0), D = p(0, 1, 0), A2 = p(0, 0, 1), B2 = p(1, 0, 1), C2 = p(1, 1, 1), D2 = p(0, 1, 1);
      s += `<polygon points="${[A, B, C, D].map((q) => q.map(f1).join(",")).join(" ")}" fill="${ACCENT}" fill-opacity="0.1" stroke-width="1.8"/>`;
      s += ln(B, B2) + ln(C, C2) + ln(D, D2) + ln(B2, C2) + ln(C2, D2) + ln(A, A2, dash) + ln(A2, B2, dash) + ln(A2, D2, dash);
      if (f.units) {
        const thin = 'stroke-width="0.8" opacity="0.7"';
        for (let i = 1; i < a; i++) s += ln(p(i / a, 0, 0), p(i / a, 1, 0), thin) + ln(p(i / a, 1, 0), p(i / a, 1, 1), thin);
        for (let j = 1; j < c; j++) s += ln(p(0, j / c, 0), p(1, j / c, 0), thin) + ln(p(1, j / c, 0), p(1, j / c, 1), thin);
        for (let k2 = 1; k2 < b; k2++) s += ln(p(0, 1, k2 / b), p(1, 1, k2 / b), thin) + ln(p(1, 0, k2 / b), p(1, 1, k2 / b), thin);
      }
      if (f.diagonal) s += ln(A, C2, `stroke="${HOT}" stroke-width="1.8"`);
      s += lab(A, B, 0, 1, L[0]) + lab(B, B2, 1, -0.3, L[1]) + lab(B2, C2, 1, 0, L[2]);
    } else {
      // triangular prism: the triangle (base b, height h, apex centred) is the front face
      const A = p(0, 0, 0), B = p(1, 0, 0), T = p(0.5, 1, 0), A2 = p(0, 0, 1), B2 = p(1, 0, 1), T2 = p(0.5, 1, 1), F = p(0.5, 0, 0);
      s += `<polygon points="${[A, B, T].map((q) => q.map(f1).join(",")).join(" ")}" fill="${ACCENT}" fill-opacity="0.1" stroke-width="1.8"/>`;
      s += ln(B, B2) + ln(T, T2) + ln(B2, T2) + ln(A, A2, dash) + ln(A2, B2, dash) + ln(A2, T2, dash) + ln(T, F, dash);
      s += lab(A, B, 0, 1, L[0]) + lab(F, T, -1, 0, L[1]) + lab(B, B2, 1, -0.3, L[2]);
    }
    return svg(W, H, s);
  }
  if (f.kind === "pyramid") {
    const [sd, h] = d, dx = Math.cos(35 * RAD) * 0.5 * sd, dy = Math.sin(35 * RAD) * 0.5 * sd;
    const k = Math.min(200 / (sd + dx), 160 / (h + dy));
    const W = (sd + dx) * k + 2 * pad, H = Math.max(h * k, dy * k) + dy * k / 2 + 2 * pad;
    const p = (x: number, z: number, y = 0): Pt => [pad + x * sd * k + z * dx * k, H - pad - z * dy * k - y * k];
    const A = p(0, 0), B = p(1, 0), C = p(1, 1), D = p(0, 1), M = p(0.5, 0.5), T = p(0.5, 0.5, h);
    let s = ln(A, B) + ln(B, C) + ln(C, D, dash) + ln(D, A, dash) + ln(T, A) + ln(T, B) + ln(T, C) + ln(T, D, dash) + ln(T, M, dash);
    s += lab(A, B, 0, 1, L[0]) + lab(M, T, 1, 0, L[1]);
    return svg(W, H, s);
  }
  // round solids: one scale, ellipses squashed to 0.3
  const r = d[0], h = f.kind === "sphere" ? 2 * r : f.kind === "hemisphere" ? r : f.kind === "cone-cylinder" ? 2 * d[1] : d[1];
  const k = Math.min(100 / r, 190 / (h + 0.6 * r));
  const rx = r * k, ry = 0.3 * r * k, W = 2 * rx + 2 * pad + 40, cx = pad + rx;
  let s = "", H: number;
  if (f.kind === "sphere") {
    H = 2 * rx + 2 * pad;
    const cy = pad + rx;
    s += `<circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(rx)}" stroke-width="1.8"/>` + ell(cx, cy, rx, ry, "front") + ell(cx, cy, rx, ry, "back", dash);
    s += ln([cx, cy], [cx + rx, cy], `stroke="${HOT}" stroke-width="1.6"`) + `<circle cx="${f1(cx)}" cy="${f1(cy)}" r="2.5" fill="currentColor" stroke="none"/>` + lab([cx, cy], [cx + rx, cy], 0, -1, L[0]);
    return svg(W, H, s);
  }
  if (f.kind === "hemisphere") {
    H = rx + ry + 2 * pad;
    const cy = pad + rx;
    s += `<path d="M ${f1(cx - rx)} ${f1(cy)} A ${f1(rx)} ${f1(rx)} 0 0 1 ${f1(cx + rx)} ${f1(cy)}" stroke-width="1.8"/>` + ell(cx, cy, rx, ry, "all");
    s += ln([cx, cy], [cx + rx, cy], `stroke="${HOT}" stroke-width="1.6"`) + lab([cx, cy], [cx + rx, cy], 0, 1, L[0]);
    return svg(W, H, s);
  }
  const hk = d[1] * k;
  if (f.kind === "cylinder") {
    H = hk + 2 * ry + 2 * pad;
    const top = pad + ry, bot = top + hk;
    s += ell(cx, top, rx, ry, "all") + ln([cx - rx, top], [cx - rx, bot]) + ln([cx + rx, top], [cx + rx, bot]) + ell(cx, bot, rx, ry, "front") + ell(cx, bot, rx, ry, "back", dash);
    s += ln([cx, top], [cx + rx, top], `stroke="${HOT}" stroke-width="1.6"`) + lab([cx, top], [cx + rx, top], 0, -1, L[0]) + lab([cx + rx, top], [cx + rx, bot], 1, 0, L[1]);
    return svg(W, H, s);
  }
  if (f.kind === "cone") {
    H = hk + ry + 2 * pad;
    const bot = pad + hk, apex: Pt = [cx, pad];
    s += ln(apex, [cx - rx, bot]) + ln(apex, [cx + rx, bot]) + ell(cx, bot, rx, ry, "front") + ell(cx, bot, rx, ry, "back", dash) + ln(apex, [cx, bot], dash);
    s += ln([cx, bot], [cx + rx, bot], `stroke="${HOT}" stroke-width="1.6"`) + lab([cx, bot], [cx + rx, bot], 0, 1, L[0]) + (L[1] ? ln([cx - rx - 14, pad], [cx - rx - 14, bot], 'stroke-width="1" stroke-dasharray="2 3"') + label(cx - rx - 14, (pad + bot) / 2, -1, 0, L[1], 4) : "");
    return svg(W, H, s);
  }
  // cone-cylinder: a cone of height h on a cylinder of the same radius and height
  H = 2 * hk + ry + 2 * pad;
  const apex: Pt = [cx, pad], mid = pad + hk, bot = mid + hk;
  s += ln(apex, [cx - rx, mid]) + ln(apex, [cx + rx, mid]) + ln(apex, [cx, mid], dash) + ell(cx, mid, rx, ry, "front") + ell(cx, mid, rx, ry, "back", dash);
  s += ln([cx - rx, mid], [cx - rx, bot]) + ln([cx + rx, mid], [cx + rx, bot]) + ell(cx, bot, rx, ry, "front") + ell(cx, bot, rx, ry, "back", dash);
  s += ln([cx, mid], [cx + rx, mid], `stroke="${HOT}" stroke-width="1.6"`) + lab([cx, mid], [cx + rx, mid], 0, 1, L[0]) + (L[1] ? ln([cx - rx - 14, pad], [cx - rx - 14, mid], 'stroke-width="1" stroke-dasharray="2 3"') + label(cx - rx - 14, (pad + mid) / 2, -1, 0, L[1], 4) : "") + lab([cx + rx, mid], [cx + rx, bot], 1, 0, L[1]);
  return svg(W, H, s);
}

/** points of a triangle with sides a = BC, b = CA, c = AB: A at the origin, B along the x-axis */
export function triFromSides(a: number, b: number, c: number): [Pt, Pt, Pt] {
  const x = (b * b + c * c - a * a) / (2 * c), y = Math.sqrt(Math.max(b * b - x * x, 0));
  return [[0, 0], [c, 0], [x, y]];
}
/** the direction from p to q, in degrees */
export const dirDeg = (p: Pt, q: Pt) => Math.atan2(q[1] - p[1], q[0] - p[0]) / RAD;

/** the interior angle at corner i of a polygon, as { a1, a2 } for an angle mark */
export function corner(pts: Pt[], i: number): { at: Pt; a1: number; a2: number } {
  const n = pts.length, q = pts[i], prev = pts[(i + n - 1) % n], next = pts[(i + 1) % n];
  let area = 0;
  for (let j = 0; j < n; j++) area += pts[j][0] * pts[(j + 1) % n][1] - pts[(j + 1) % n][0] * pts[j][1];
  return area > 0 ? { at: q, a1: dirDeg(q, next), a2: dirDeg(q, prev) } : { at: q, a1: dirDeg(q, prev), a2: dirDeg(q, next) };
}
/** a triangle with angles A at (0, 0) and B at (c, 0), apex C above */
export function triFromAngles(A: number, B: number, c = 10): [Pt, Pt, Pt] {
  const C = 180 - A - B, b = (c * Math.sin(B * RAD)) / Math.sin(C * RAD);
  return [[0, 0], [c, 0], [b * Math.cos(A * RAD), b * Math.sin(A * RAD)]];
}
export type Spot = "UR" | "UL" | "LL" | "LR";
/** two horizontal parallel lines cut by a transversal at angle th; marks[i] = [line 0 (bottom) or 1 (top), spot, label] */
export function transversal(angle: number, marks: [0 | 1, Spot, string][], parallel = true): GeomFig {
  // drawn no shallower than 35° so the marks stay apart; the labels carry the measures
  const th = Math.min(Math.max(angle, 35), 145);
  const H = 9, dx = H / Math.tan(th * RAD), P0: Pt = [0, 0], P1: Pt = [dx, H];
  const xs = [0, dx], lo = Math.min(...xs) - 6, hi = Math.max(...xs) + 6;
  const t = 4 / Math.sin(th * RAD);
  const u: Pt = [Math.cos(th * RAD), Math.sin(th * RAD)];
  const range: Record<Spot, [number, number]> = { UR: [0, th], UL: [th, 180], LL: [180, 180 + th], LR: [180 + th, 360] };
  return {
    segs: [
      { a: [lo, 0], b: [hi, 0], line: true }, { a: [lo, H], b: [hi, H], line: true },
      { a: [P0[0] - u[0] * t * 0.6, P0[1] - u[1] * t * 0.6], b: [P1[0] + u[0] * t * 0.6, P1[1] + u[1] * t * 0.6], line: true },
    ],
    par: parallel ? [{ a: [lo, 0], b: [lo + 3, 0], n: 1 }, { a: [lo, H], b: [lo + 3, H], n: 1 }] : [],
    angles: marks.map(([l, sp, lab], i) => ({ at: l ? P1 : P0, a1: range[sp][0], a2: range[sp][1], label: lab, hot: i > 0 })),
    width: 300,
  };
}
/** a filled sector as a polygon, angles in degrees */
export function sectorPts(c: Pt, r: number, from: number, to: number): Pt[] {
  const n = Math.max(6, Math.ceil(Math.abs(to - from) / 5)), out: Pt[] = [c];
  for (let i = 0; i <= n; i++) { const t = (from + ((to - from) * i) / n) * RAD; out.push([c[0] + r * Math.cos(t), c[1] + r * Math.sin(t)]); }
  return out;
}
export const onCirc = (c: Pt, r: number, t: number): Pt => [c[0] + r * Math.cos(t * RAD), c[1] + r * Math.sin(t * RAD)];
/** attach a figure to a generator's draft */
export const withFig = <T extends object>(d: T, figure: string): T & { figure: string } => ({ ...d, figure });
/** "(3x + 5)°" from a coefficient and constant */
export const angExpr = (a: number, b: number) => `(${a === 1 ? "" : a}x${b === 0 ? "" : b > 0 ? ` + ${b}` : ` − ${-b}`})°`;
