// "📌 Anchor section" inside the PDF reader: on the toolbar that appears when you select
// text (turns the selection into a highlight) and in the popup of an existing highlight.
import React, { useState } from "react";
import { renderWidget, usePlugin, useRunAsync, WidgetLocation } from "@remnote/plugin-sdk";
import { pdfOf } from "../drills/anchors";
import "../drills.css";

function AnchorButton() {
  const plugin = usePlugin();
  const ctx = useRunAsync(() => plugin.widget.getWidgetContext<WidgetLocation.PDFHighlightPopupLocation>(), []);
  const [busy, setBusy] = useState(false);
  const go = async () => {
    setBusy(true);
    try {
      let hl = ctx?.remId ? await plugin.rem.findOne(ctx.remId) : undefined;
      if (!hl) hl = await plugin.reader.addHighlight();
      if (!hl) return void (await plugin.app.toast("Select the section heading's text first (or use an area highlight)."));
      await plugin.widget.openPopup("anchor", { highlightId: hl._id, pdfId: await pdfOf(plugin, hl), rootName: "Wiki Flashcards" });
    } finally {
      setBusy(false);
    }
  };
  return (
    <button className="odd-btn odd-anchor-btn" onClick={go} disabled={busy} title="Tie this heading to a textbook section so drills open your PDF here">
      📌 Anchor section
    </button>
  );
}

renderWidget(AnchorButton);
