// "Drills: Link PDF to a textbook" — binds a PDF rem in RemNote to a book in drills/sources.
// The binding lives in RemNote synced storage (rem ids are RemNote's business, not the wiki's).
import React, { useEffect, useState } from "react";
import { renderWidget, usePlugin, useRunAsync, WidgetLocation } from "@remnote/plugin-sdk";
import { SOURCES, sourceLabel } from "../drills/skills";
import { ensureDrillDeck, getBindings, PdfBinding, plain, setBinding } from "../drills/deck";
import "../drills.css";

const stop = (e: React.SyntheticEvent) => e.stopPropagation();

function BookLink() {
  const plugin = usePlugin();
  const ctx = useRunAsync(() => plugin.widget.getWidgetContext<WidgetLocation.Popup>(), []);
  const remId: string | undefined = ctx?.contextData?.remId;
  const rootName: string = ctx?.contextData?.rootName ?? "Wiki Flashcards";
  const remName = useRunAsync(async () => {
    if (!remId) return undefined;
    const rem = await plugin.rem.findOne(remId);
    return rem ? plain(rem.text) || "(untitled)" : undefined;
  }, [remId]);
  const [source, setSource] = useState(SOURCES[0]?.id ?? "");
  const [page1, setPage1] = useState("");
  const [bindings, setBindings] = useState<Record<string, PdfBinding>>({});
  const [busy, setBusy] = useState(false);

  const refresh = async () => setBindings(await getBindings(plugin));
  useEffect(() => {
    refresh();
  }, []);

  const save = async () => {
    if (!remId) return;
    setBusy(true);
    const p = parseInt(page1, 10);
    await setBinding(plugin, source, { remId, name: remName, offset: Number.isFinite(p) ? p - 1 : undefined });
    await ensureDrillDeck(plugin, rootName, true);
    await refresh();
    setBusy(false);
    await plugin.app.toast(`Linked “${remName}” to ${sourceLabel(SOURCES.find((s) => s.id === source)!)}`);
  };

  return (
    <div className="odd-panel" onKeyDown={stop} onKeyUp={stop} onKeyPress={stop}>
      <div className="odd-header">
        <span className="odd-skill">Link a PDF to a textbook</span>
      </div>
      {remId && remName ? (
        <>
          <p className="odd-hint">
            PDF / rem: <b>{remName}</b>
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
              <span className="odd-field-label">p. 1 at</span>
              <input
                className="odd-input"
                placeholder="PDF page showing printed page 1 (optional)"
                value={page1}
                onChange={(e) => setPage1(e.target.value)}
              />
            </label>
          </div>
          <div className="odd-actions">
            <button className="odd-btn primary" disabled={busy} onClick={save}>
              {busy ? "Linking…" : "Link"}
            </button>
          </div>
        </>
      ) : (
        <p className="odd-hint">Open the book's PDF (or click its rem in the sidebar), then run “Drills: Link PDF to a textbook” again.</p>
      )}
      {Object.keys(bindings).length > 0 && (
        <div className="odd-solution">
          <div className="odd-hint">Linked now:</div>
          <ul className="odd-steps">
            {Object.entries(bindings).map(([sid, b]) => {
              const s = SOURCES.find((x) => x.id === sid);
              return (
                <li key={sid}>
                  {s ? sourceLabel(s) : sid} → {b.name ?? b.remId}
                  {b.offset !== undefined ? ` (PDF page = printed + ${b.offset})` : ""}{" "}
                  <button
                    className="odd-btn subtle"
                    onClick={async () => {
                      await setBinding(plugin, sid, null);
                      await ensureDrillDeck(plugin, rootName, true);
                      await refresh();
                    }}
                  >
                    unlink
                  </button>
                </li>
              );
            })}
          </ul>
        </div>
      )}
    </div>
  );
}

renderWidget(BookLink);
