import React from "react";
import katex from "katex";

const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

/** Text with $...$ inline math, rendered with KaTeX. */
export function MathText({ text, className }: { text: string; className?: string }) {
  const html = text
    .split(/\$([^$]+)\$/)
    .map((part, i) =>
      i % 2 ? katex.renderToString(part, { throwOnError: false, displayMode: false }) : esc(part)
    )
    .join("");
  return <span className={className} dangerouslySetInnerHTML={{ __html: html }} />;
}

/** A single LaTeX expression. */
export function Tex({ tex, display = false }: { tex: string; display?: boolean }) {
  const html = katex.renderToString(tex, { throwOnError: false, displayMode: display });
  return <span dangerouslySetInnerHTML={{ __html: html }} />;
}
