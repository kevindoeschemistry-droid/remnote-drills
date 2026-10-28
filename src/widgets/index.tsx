import { BuiltInPowerupCodes, declareIndexPlugin, ReactRNPlugin, RNPlugin, WidgetLocation } from "@remnote/plugin-sdk";
type RemObject = NonNullable<Awaited<ReturnType<RNPlugin["rem"]["findOne"]>>>;
import "../style.css";
import { DRILL_POWERUP, DRILL_SLOT, LEGACY_ROOT, SOURCES_SLOT } from "../drills/deck";
import { SOURCES, sourceLabel } from "../drills/skills";
import { latestHighlight, pdfOf } from "../drills/anchors";
import { syncCourses } from "../drills/course";

console.log("[Drills] bundle loaded");

const ROOT_NAME = LEGACY_ROOT;

// ── Plugin lifecycle ───────────────────────────────────────────────────────────

async function registerDrills(plugin: ReactRNPlugin) {
  await plugin.app.registerPowerup({
    name: "ODE Drill",
    code: DRILL_POWERUP,
    description: "Generates a fresh Kuta-style ODE problem under this flashcard every review.",
    options: {
      slots: [
        { code: DRILL_SLOT, name: "Skill", onlyProgrammaticModifying: true, hidden: true },
        // visible on the card: where this skill is taught ("Kreyszig 10e §1.3; …")
        { code: SOURCES_SLOT, name: "Sources", onlyProgrammaticModifying: true },
      ],
    },
  });

  await plugin.settings.registerNumberSetting({
    id: "drill-cards-per-skill",
    title: "Drills: cards per skill",
    description: "How many drill cards to create for each skill (each review gets a new problem).",
    defaultValue: 3,
  });
  await plugin.settings.registerNumberSetting({
    id: "drill-clear-at",
    title: "Drills: correct in a row to clear a skill",
    defaultValue: 5,
  });
  await plugin.settings.registerDropdownSetting({
    id: "drill-label-source",
    title: "Drills: label cards with this textbook",
    description: "When a skill is taught in several books, the card header shows this one.",
    defaultValue: SOURCES[0]?.id,
    options: SOURCES.map((s) => ({ key: s.id, label: `${sourceLabel(s)} — ${s.title}`, value: s.id })),
  });

  // Under every card tagged ODE Drill: the generated problem + answer box
  await plugin.app.registerWidget("drill_card", WidgetLocation.FlashcardUnder, {
    powerupFilter: DRILL_POWERUP,
    dimensions: { height: "auto", width: "100%" },
  });
  // The sidebar: practice, exam mix, courses + setup
  await plugin.app.registerWidget("drill_session", WidgetLocation.RightSidebar, {
    dimensions: { height: "auto", width: "100%" },
    widgetTabTitle: "Drills",
  });
  // Link a PDF in RemNote to a textbook in drills/sources
  await plugin.app.registerWidget("book_link", WidgetLocation.Popup, {
    dimensions: { height: "auto", width: 560 },
  });

  // Three commands: open the sidebar, and the two that need a PDF in front of you.
  await plugin.app.registerCommand({
    id: "ode-drills-practice",
    name: "Drills: Open (practice, exam mix, courses)",
    action: async () => {
      await plugin.window.openWidgetInRightSidebar("drill_session");
    },
  });
  await plugin.app.registerWidget("anchor", WidgetLocation.Popup, {
    dimensions: { height: "auto", width: 600 },
  });
  // 📌 button inside the PDF reader: on the selection toolbar and in a highlight's popup
  await plugin.app.registerWidget("anchor_button", WidgetLocation.PDFHighlightToolbarLocation, {
    dimensions: { height: 34, width: 150 },
  });
  await plugin.app.registerWidget("anchor_button", WidgetLocation.PDFHighlightPopupLocation, {
    dimensions: { height: 34, width: 150 },
  });
  await plugin.app.registerCommand({
    id: "drills-anchor-section",
    name: "Drills: Anchor this section (highlight the heading in your PDF first)",
    action: async () => {
      // 1) the text selected in the PDF reader becomes a highlight
      let hl = await plugin.reader.addHighlight().catch(() => undefined);
      // 2) or an existing highlight you clicked on
      if (!hl) {
        const f = await plugin.focus.getFocusedRem();
        if (f && (await f.hasPowerup(BuiltInPowerupCodes.PDFHighlight))) hl = f;
      }
      // 3) or the newest highlight in the PDF that's open: highlight the heading, then run this
      if (!hl) hl = await latestHighlight(plugin);
      if (!hl) {
        await plugin.app.toast("Open the book's PDF, highlight the section heading (Highlight button), then run this again.");
        return;
      }
      await plugin.widget.openPopup("anchor", { highlightId: hl._id, pdfId: await pdfOf(plugin, hl), rootName: ROOT_NAME });
    },
  });
  await plugin.app.registerCommand({
    id: "drills-link-pdf",
    name: "Drills: Link PDF to a textbook",
    action: async () => {
      // the PDF that's open (or the rem you're on) is the candidate
      let remId = (await plugin.focus.getFocusedRem())?._id;
      if (!remId) remId = await plugin.window.getOpenPaneRemId(await plugin.window.getFocusedPaneId());
      await plugin.widget.openPopup("book_link", { remId, rootName: ROOT_NAME });
    },
  });
}

async function onActivate(plugin: ReactRNPlugin) {
  await registerDrills(plugin);
  // courses you've built follow their definition: new lessons and skills arrive on their own
  setTimeout(() => syncCourses(plugin).catch((e) => console.error("[Drills] course sync failed", e)), 4000);
}

async function onDeactivate(_plugin: ReactRNPlugin) {}

declareIndexPlugin(onActivate, onDeactivate);
