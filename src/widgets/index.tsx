import { BuiltInPowerupCodes, declareIndexPlugin, ReactRNPlugin, RNPlugin, WidgetLocation } from "@remnote/plugin-sdk";
type RemObject = NonNullable<Awaited<ReturnType<RNPlugin["rem"]["findOne"]>>>;
import "../style.css";
import { DRILL_POWERUP, DRILL_SLOT, SOURCES_SLOT, ensureDrillDeck, findOrCreateDocument } from "../drills/deck";
import { SOURCES, sourceLabel } from "../drills/skills";
import { latestHighlight, pdfOf } from "../drills/anchors";
import { organizeLibrary } from "../drills/library";
import { coursesWithUnits, ensureCourse } from "../drills/course";

console.log("[Drills] bundle loaded");

// Legacy home of the drill cards (v0.2–v0.14); ensureDrillDeck migrates out of it.
const ROOT_NAME = "Wiki Flashcards";

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
  // Unlimited practice: popup + right sidebar tab
  await plugin.app.registerWidget("drill_session", WidgetLocation.RightSidebar, {
    dimensions: { height: "auto", width: "100%" },
    widgetTabTitle: "ODE Drills",
  });
  // Link a PDF in RemNote to a textbook in drills/sources
  await plugin.app.registerWidget("book_link", WidgetLocation.Popup, {
    dimensions: { height: "auto", width: 560 },
  });

  await plugin.app.registerCommand({
    id: "ode-drills-practice",
    name: "Drills: Practice",
    action: async () => {
      await plugin.window.openWidgetInRightSidebar("drill_session");
    },
  });
  await plugin.app.registerCommand({
    id: "ode-drills-create-cards",
    name: "Drills: Create drill cards & book contents",
    action: async () => {
      await plugin.app.toast("Drills: building cards and book contents…");
      try {
        await ensureDrillDeck(plugin, ROOT_NAME);
      } catch (e) {
        console.error("Drills failed", e);
        await plugin.app.toast(`Drills failed — ${String(e)}`);
      }
    },
  });
  await plugin.app.registerWidget("midterm_mix", WidgetLocation.RightSidebar, {
    dimensions: { height: "auto", width: "100%" },
    widgetTabTitle: "Midterm mix",
  });
  await plugin.app.registerCommand({
    id: "drills-midterm-mix",
    name: "Drills: Midterm mix (heat transfer, Ch 1–5 only)",
    action: async () => {
      await plugin.window.openWidgetInRightSidebar("midterm_mix");
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
    id: "drills-organize-library",
    name: "Drills: Organize textbook PDFs (subject documents, rename)",
    action: async () => {
      await plugin.app.toast("Filing textbook PDFs…");
      try {
        const log = await organizeLibrary(plugin);
        await plugin.app.toast(log.length ? `Filed ${log.length} PDF${log.length > 1 ? "s" : ""}: ${log.join(" · ")}` : "Subject documents ready; no recognised PDFs to file yet.");
      } catch (e) {
        await plugin.app.toast(`Organizing failed — ${String(e)}`);
      }
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
  // one command per full course: builds Course › Unit › Lesson › drill cards
  for (const c of coursesWithUnits())
    await plugin.app.registerCommand({
      id: `drills-course-${c.id}`,
      name: `Drills: Build course · ${c.title}`,
      action: async () => {
        await plugin.app.toast(`Building ${c.title}…`);
        try {
          await ensureCourse(plugin, c.id);
        } catch (e) {
          await plugin.app.toast(`Building ${c.title} failed — ${String(e)}`);
        }
      },
    });
}

async function onDeactivate(_plugin: ReactRNPlugin) {}

declareIndexPlugin(onActivate, onDeactivate);
