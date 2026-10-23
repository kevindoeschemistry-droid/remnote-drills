// "Drills: Anchor this section" — ties a PDF highlight (usually a section heading)
// to a textbook section, so drill labels open your PDF right there.
import React, { useEffect, useMemo, useState } from "react";
import { renderWidget, usePlugin, useRunAsync, WidgetLocation } from "@remnote/plugin-sdk";
import { SOURCES, sourceLabel } from "../drills/skills";
import { ensureDrillDeck, getBindings, plain, setBinding } from "../drills/deck";
import { getAnchors, anchorKey, guessRef, guessSourceForPdf, setAnchor, targets } from "../drills/anchors";
import "../drills.css";

const stop = (e: React.SyntheticEvent) => e.stopPropagation();

function Anchor() {
  const plugin = usePlugin();
  const ctx = useRunAsync(() => plugin.widget.getWidgetContext<WidgetLocation.Popup>(), []);
  const hlId: string | undefined = ctx?.contextData?.highlightId;
  const pdfId: string | undefined = ctx?.contextData?.pdfId;
  const rootName: string = ctx?.contextData?.rootName ?? "Wiki Flashcards";
  const hlText = useRunAsync(async () => {
    if (!hlId) return "";
    const rem = await plugin.rem.findOne(hlId);
    return plain(rem?.text).trim();
  }, [hlId]);
  const [bindings, setBindingsState] = useState<Record<string, { remId: string }>>({});
  const [anchors, setAnchors] = useState<Record<string, string>>({});
  const [source, setSource] = useState<string>("");
  const [ref, setRef] = useState<string>("");
  const [saved, setSaved] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      setBindingsState(await getBindings(plugin));
      setAnchors(await getAnchors(plugin));
    })();
  }, []);

  const pdfName = useRunAsync(async () => (pdfId ? plain((await plugin.rem.findOne(pdfId))?.text) : ""), [pdfId]);
  // default book: the one linked to this PDF, else the one its name matches, else the first
  useEffect(() => {
    if (source || pdfName === undefined) return;
    const linked = Object.entries(bindings).find(([, b]) => b.remId === pdfId)?.[0];
    setSource(linked ?? guessSourceForPdf(pdfName, SOURCES)?.id ?? SOURCES[0]?.id ?? "");
  }, [bindings, pdfId, pdfName]);

  const src = SOURCES.find((s) => s.id === source);
  const opts = useMemo(() => (src ? targets(src) : []), [src]);

  // default section: guessed from the highlighted text, else the first one not yet anchored
  useEffect(() => {
    if (!src) return;
    const g = hlText ? guessRef(src, hlText) : undefined;
    setRef(g ?? opts.find((o) => !anchors[anchorKey(src.id, o.ref)])?.ref ?? opts[0]?.ref ?? "");
  }, [src, hlText, anchors]);

  const save = async () => {
    if (!hlId || !src || !ref) return;
    await setAnchor(plugin, src.id, ref, hlId);
    if (pdfId && !bindings[src.id]) {
      const pdf = await plugin.rem.findOne(pdfId);
      await setBinding(plugin, src.id, { remId: pdfId, name: plain(pdf?.text) || undefined });
    }
    const label = opts.find((o) => o.ref === ref)?.label ?? ref;
    setSaved(`${sourceLabel(src)} ${label}`);
    setAnchors(await getAnchors(plugin));
    await ensureDrillDeck(plugin, rootName, true);
  };

  if (!hlId)
    return (
      <div className="odd-panel" onKeyDown={stop}>
        <p className="odd-hint">
          In your PDF, select a section heading (e.g. “3.6 Heat Transfer from Extended Surfaces”), then run “Drills: Anchor this
          section”.
        </p>
      </div>
    );

  const done = src ? opts.filter((o) => anchors[anchorKey(src.id, o.ref)]).length : 0;

  return (
    <div className="odd-panel" onKeyDown={stop} onKeyUp={stop} onKeyPress={stop}>
      <div className="odd-header">
        <span className="odd-skill">Anchor a textbook section</span>
        {src && (
          <span className="odd-count">
            {done} / {opts.length} anchored
          </span>
        )}
      </div>
      <p className="odd-hint">
        Anchoring your highlight: <b>{hlText || "(area highlight, no text)"}</b>. Wrong one? Close this, highlight the heading, and run it again.
      </p>
      <div className="odd-fields">
        <label className="odd-field">
          <span className="odd-field-label">Book</span>
          <select className="odd-select" value={source} onChange={(e) => setSource(e.target.value)}>
            {SOURCES.map((s) => (
              <option key={s.id} value={s.id}>
                {sourceLabel(s)} — {s.title}
              </option>
            ))}
          </select>
        </label>
        <label className="odd-field">
          <span className="odd-field-label">Section</span>
          <select className="odd-select" value={ref} onChange={(e) => setRef(e.target.value)}>
            {opts.map((o) => (
              <option key={o.ref} value={o.ref}>
                {src && anchors[anchorKey(src.id, o.ref)] ? "✓ " : ""}
                {o.label}
              </option>
            ))}
          </select>
        </label>
      </div>
      <div className="odd-actions">
        <button className="odd-btn primary" onClick={save}>
          Anchor
        </button>
      </div>
      {saved && (
        <div className="odd-result ok">
          Anchored {saved}. Drills for this section now open your PDF here. Select the next heading and run the command again.
        </div>
      )}
    </div>
  );
}

renderWidget(Anchor);
