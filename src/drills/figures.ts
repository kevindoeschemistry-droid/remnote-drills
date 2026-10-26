// Small SVG diagrams for the exam-style heat transfer problems, drawn from each problem's
// `meta`. Strokes use currentColor so they follow RemNote's light/dark theme.
type M = Record<string, any>;

const W = 460;
const svg = (h: number, body: string, w = W) =>
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="100%" style="max-width:${w}px" font-family="system-ui, sans-serif" font-size="12" fill="none" stroke="currentColor">${body}</svg>`;
const text = (x: number, y: number, s: string, anchor = "middle", extra = "") =>
  `<text x="${x}" y="${y}" text-anchor="${anchor}" fill="currentColor" stroke="none" ${extra}>${s}</text>`;
const arrow = (x1: number, y1: number, x2: number, y2: number, color = "currentColor") => {
  const a = Math.atan2(y2 - y1, x2 - x1);
  const h = 7;
  const p1 = `${x2 - h * Math.cos(a - 0.4)},${y2 - h * Math.sin(a - 0.4)}`;
  const p2 = `${x2 - h * Math.cos(a + 0.4)},${y2 - h * Math.sin(a + 0.4)}`;
  return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="1.5"/><polygon points="${x2},${y2} ${p1} ${p2}" fill="${color}" stroke="none"/>`;
};
const FLUID = "#5aa9e6";
const HOT = "#e0654f";
const SOLID = "rgba(150,150,150,0.18)";

// ── two-layer wall with its (linear) temperature profile ───────────────────
function wall(m: M): string {
  const { T1, T2, T3 } = m;
  const x0 = 90, xm = 230, x1 = 370, top = 20, bot = 150;
  const y = (T: number) => top + 15 + ((T1 - T) / (T1 - T3)) * (bot - top - 30);
  const mark =
    m.mae === "wall-point"
      ? (() => {
          const xa = m.layer === 1 ? x0 : xm;
          const xp = xa + m.f * (xm - x0);
          const yp = y(m.layer === 1 ? T1 + m.f * (T2 - T1) : T2 + m.f * (T3 - T2));
          return `<line x1="${xp}" y1="${top}" x2="${xp}" y2="${bot}" stroke-dasharray="3 3" opacity="0.6"/><circle cx="${xp}" cy="${yp}" r="4" fill="${HOT}" stroke="none"/>${text(xp, bot + 14, "T = ?")}`;
        })()
      : "";
  return svg(
    185,
    `<rect x="${x0}" y="${top}" width="${xm - x0}" height="${bot - top}" fill="${SOLID}"/>
     <rect x="${xm}" y="${top}" width="${x1 - xm}" height="${bot - top}" fill="rgba(90,169,230,0.15)"/>
     ${text((x0 + xm) / 2, top - 6, "material 1")}${text((xm + x1) / 2, top - 6, "material 2")}
     <polyline points="${x0},${y(T1)} ${xm},${y(T2)} ${x1},${y(T3)}" stroke="${HOT}" stroke-width="2"/>
     ${text(x0 - 6, y(T1) + 4, `T₁ = ${T1}`, "end")}${text(xm + 6, y(T2) - 6, `T₂ = ${T2}`, "start")}${text(x1 + 6, y(T3) + 4, `T₃ = ${T3}`, "start")}
     ${arrow(x0 + 10, bot - 12, x1 - 10, bot - 12)}${text((x0 + x1) / 2, bot - 18, "q (1-D, steady)")}
     ${text((x0 + xm) / 2, bot + 30, "L₁")}${text((xm + x1) / 2, bot + 30, "L₂")}${mark}`
  );
}

// ── A | (B over C) | D ──────────────────────────────────────────────────────
function seriesParallel(): string {
  const y0 = 20, h = 140, w = 90, x = [60, 150, 240, 330];
  const block = (xx: number, yy: number, hh: number, label: string, fill: string) =>
    `<rect x="${xx}" y="${yy}" width="${w}" height="${hh}" fill="${fill}"/>${text(xx + w / 2, yy + hh / 2 + 4, label, "middle", 'font-weight="600"')}`;
  return svg(
    210,
    `${block(x[0], y0, h, "A", "rgba(91,124,250,0.25)")}${block(x[1], y0, h / 2, "B", "rgba(240,160,100,0.3)")}${block(x[1], y0 + h / 2, h / 2, "C", "rgba(250,210,90,0.35)")}${block(x[2] + 0, y0, h, "D", "rgba(120,200,120,0.3)")}
     ${arrow(20, y0 + h / 2, x[0] - 4, y0 + h / 2)}${arrow(x[2] + w + 4, y0 + h / 2, x[2] + w + 50, y0 + h / 2)}
     ${text(35, y0 + h / 2 - 8, "q")}${text(x[2] + w + 30, y0 + h / 2 - 8, "q")}
     ${text(x[0] + w / 2, y0 + h + 16, "full height 2h")}${text(x[1] + w / 2, y0 + h + 16, "h each")}${text(x[2] + w / 2, y0 + h + 16, "full height 2h")}
     ${text(W / 2 - 10, y0 + h + 32, "k_A > k_B > k_C > k_D · all blocks same width", "middle", 'font-size="11" opacity="0.8"')}`,
    W - 20
  );
}

// ── rod midway between two isothermal planes ───────────────────────────────
function rodSlab(m: M): string {
  const cx = 230, cy = 95, r = 26, top = 25, bot = 165;
  return svg(
    195,
    `<rect x="40" y="${top}" width="380" height="${bot - top}" fill="${SOLID}"/>
     <line x1="40" y1="${top}" x2="420" y2="${top}" stroke-width="2.5"/><line x1="40" y1="${bot}" x2="420" y2="${bot}" stroke-width="2.5"/>
     ${text(230, top - 8, "slab face, T_s")}${text(230, bot + 16, "slab face, T_s")}
     <circle cx="${cx}" cy="${cy}" r="${r}" fill="${HOT}" fill-opacity="0.8"/>${text(cx, cy + 4, "rod", "middle", 'font-weight="600"')}
     ${arrow(cx + r + 50, cy, cx + r + 50, top + 2)}${arrow(cx + r + 50, cy, cx + r + 50, bot - 2)}
     <line x1="${cx}" y1="${cy}" x2="${cx + r + 60}" y2="${cy}" stroke-dasharray="3 3" opacity="0.6"/>
     ${text(cx + r + 58, (cy + top) / 2 + 4, "y", "start")}${text(cx + r + 58, (cy + bot) / 2 + 4, "y", "start")}
     ${text(cx - r - 8, cy + 4, `D = ${Math.round(m.D * 1000)} mm`, "end")}
     ${text(70, cy + 4, `k = ${m.k}`, "start")}
     ${text(410, cy + 4, "← ∞ wide →", "end", 'font-size="11" opacity="0.7"')}`
  );
}

// ── two spheres in a large medium ──────────────────────────────────────────
function twoSpheres(m: M): string {
  const Dnm = Math.round(m.D * 1e9);
  const gap = Math.round((m.z * 2 - m.D) * 1e9);
  const scale = 200 / (2 * Dnm + gap);
  const r = (Dnm * scale) / 2;
  const x1 = 130, x2 = x1 + 2 * r + gap * scale, cy = 80;
  const mid = (x1 + x2) / 2;
  return svg(
    170,
    `<rect x="20" y="15" width="420" height="125" rx="10" fill="${SOLID}"/>
     ${text(230, 32, `medium, k = ${m.k} W/m·K`)}
     <circle cx="${x1}" cy="${cy}" r="${r}" fill="${HOT}" fill-opacity="0.8"/><circle cx="${x2}" cy="${cy}" r="${r}" fill="${FLUID}" fill-opacity="0.8"/>
     ${text(x1, cy + r + 16, `T₁ = ${m.T1} K`)}${text(x2, cy + r + 16, `T₂ = ${m.T2} K`)}
     <line x1="${mid}" y1="40" x2="${mid}" y2="135" stroke-dasharray="4 3" opacity="0.7"/>${text(mid, 152, "midplane: isothermal at (T₁+T₂)/2", "middle", 'font-size="11"')}
     ${arrow(x1 + r + 4, cy, mid - 4, cy)}${text((x1 + r + mid) / 2, cy - 8, "q")}
     ${text(x1, cy - r - 6, `D = ${Dnm} nm`, "middle", 'font-size="11"')}${text(mid + (x2 - r - mid) / 2 + 2, cy - 22, `gap ${gap} nm`, "middle", 'font-size="11"')}`
  );
}

// ── pot bottom ─────────────────────────────────────────────────────────────
function pot(m: M): string {
  const top = 70, bot = 110;
  const arrows = [110, 170, 230, 290, 350].map((x) => arrow(x, bot + 40, x, bot + 4, HOT)).join("");
  const bubbles = [130, 200, 260, 330].map((x, i) => `<circle cx="${x}" cy="${40 + (i % 2) * 10}" r="5" stroke="${FLUID}"/>`).join("");
  return svg(
    195,
    `<rect x="60" y="15" width="340" height="${top - 15}" fill="rgba(90,169,230,0.15)" stroke="none"/>${bubbles}
     ${text(70, 32, `boiling water, T∞ = ${m.Tinf} °C${m.h ? `, h = ${m.h} W/m²·K` : ""}`, "start")}
     <rect x="60" y="${top}" width="340" height="${bot - top}" fill="${SOLID}"/>
     ${text(230, (top + bot) / 2 + 4, `pot bottom, k = ${m.k}, L = ${Math.round(m.L * 1000)} mm`)}
     ${text(406, top + 4, m.TL ? `y = L: ${m.TL} °C` : "y = L", "start", 'font-size="11"')}${text(406, bot + 4, "y = 0", "start", 'font-size="11"')}
     ${arrows}${text(230, bot + 58, `q″ = ${m.qf / 1e4} W/cm² from the stove`)}
     ${arrow(30, bot, 30, top - 10)}${text(30, top - 16, "y")}`,
    500
  );
}

// ── finite-difference node ─────────────────────────────────────────────────
function fdNode(m: M): string {
  const dy = 60;
  const dx = Math.max(30, Math.min(170, m.a * dy));
  const faces: M[] = m.faces;
  const has = (n: string) => faces.find((f) => f.name === n);
  const exposedTop = has("top")?.kind === "conv";
  const exposedRight = has("right")?.kind === "conv";
  const insulatedTop = has("top")?.kind === "ins";
  const cx = 260, cy = exposedTop || insulatedTop ? 80 : 110;
  // solid region: everything not exposed
  const sx0 = cx - dx - 30, sx1 = exposedRight ? cx : cx + dx + 30;
  const sy0 = exposedTop || insulatedTop ? cy : cy - dy - 30, sy1 = cy + dy + 30;
  let body = `<rect x="${sx0}" y="${sy0}" width="${sx1 - sx0}" height="${sy1 - sy0}" fill="${SOLID}" stroke="none"/>`;
  if (exposedTop) body += `<rect x="${sx0}" y="${cy - 45}" width="${(exposedRight ? cx + 60 : sx1) - sx0}" height="45" fill="rgba(90,169,230,0.18)" stroke="none"/>`;
  if (exposedRight) body += `<rect x="${cx}" y="${exposedTop ? cy - 45 : sy0}" width="70" height="${sy1 - (exposedTop ? cy - 45 : sy0)}" fill="rgba(90,169,230,0.18)" stroke="none"/>`;
  if (insulatedTop)
    body += `<line x1="${sx0}" y1="${cy}" x2="${sx1}" y2="${cy}" stroke-width="3"/>` +
      Array.from({ length: 12 }, (_, i) => `<line x1="${sx0 + i * ((sx1 - sx0) / 12)}" y1="${cy}" x2="${sx0 + i * ((sx1 - sx0) / 12) + 8}" y2="${cy - 8}"/>`).join("") +
      text(sx1 - 4, cy - 12, "insulated", "end", 'font-size="11"');
  // grid lines + neighbours
  const pos: Record<string, [number, number]> = { left: [cx - dx, cy], right: [cx + dx, cy], above: [cx, cy - dy], below: [cx, cy + dy] };
  for (const f of faces) {
    if (f.kind !== "cond") continue;
    const [x, y] = pos[f.name];
    body += `<line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}" opacity="0.5"/><circle cx="${x}" cy="${y}" r="5" fill="#3aa76d" stroke="none"/>${text(x + (f.name === "left" ? -8 : 8), y + (f.name === "left" ? 18 : -8), `${f.T} °C`, f.name === "left" ? "end" : "start")}`;
  }
  // the node's control volume (dashed)
  const hx0 = cx - dx / 2, hx1 = exposedRight ? cx : cx + dx / 2;
  const hy0 = exposedTop || insulatedTop ? cy : cy - dy / 2, hy1 = cy + dy / 2;
  body += `<rect x="${hx0}" y="${hy0}" width="${hx1 - hx0}" height="${hy1 - hy0}" stroke="${HOT}" stroke-dasharray="5 3" stroke-width="1.5"/>`;
  body += `<circle cx="${cx}" cy="${cy}" r="7" fill="${HOT}" stroke="none"/>${text(cx + 10, cy + 18, "Tₙ", "start", 'font-weight="600"')}`;
  // spacing labels
  body += arrow(cx - dx, sy1 - 10, cx, sy1 - 10) + text(cx - dx / 2, sy1 - 14, m.a === 1 ? "Δx = Δy" : m.a === 0.5 ? "Δx = Δy/2" : `Δx = ${m.a}Δy`);
  body += text(sx0 + 4, cy + dy / 2 + 4, "Δy", "start", 'font-size="11"') + `<line x1="${sx0 + 22}" y1="${cy}" x2="${sx0 + 22}" y2="${cy + dy}" opacity="0.7"/>`;
  const fluid = `fluid: T∞ = ${m.Tinf} °C, h = ${m.h}${m.hr ? `; h_r = ${m.hr} to T_sur = ${m.Tsur} °C` : ""}`;
  body += text(260, 16, exposedTop || exposedRight ? fluid : "", "middle", 'font-size="11"');
  return svg(Math.max(sy1 + 15, 200), body, 520);
}

/** The SVG for a problem, or undefined if it has none. */
export function figureFor(meta: M | undefined): string | undefined {
  switch (meta?.mae) {
    case "wall-compare":
    case "wall-point":
      return wall(meta);
    case "series-parallel":
      return seriesParallel();
    case "rod-slab":
      return rodSlab(meta);
    case "two-spheres":
      return twoSpheres(meta);
    case "pot":
      return pot(meta);
    case "fd":
      return fdNode(meta);
  }
  return undefined;
}
