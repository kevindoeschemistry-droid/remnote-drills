import { declareIndexPlugin, ReactRNPlugin, RNPlugin, WidgetLocation } from "@remnote/plugin-sdk";
import "../style.css";
import { DRILL_POWERUP, DRILL_SLOT, SOURCES_SLOT, ensureDrillDeck, findOrCreateDocument } from "../drills/deck";
import { SOURCES, sourceLabel } from "../drills/skills";

console.log("[WikiSync] bundle loaded");

// ── Config ─────────────────────────────────────────────────────────────────────

const WIKI_URL = "https://wiki.kevindoeschemistry.com/static/flashcards.json";
const STORAGE_KEY = "wikiCardMap"; // synced: cardId -> remId
const ROOT_NAME = "Wiki Flashcards";

// ── Types ──────────────────────────────────────────────────────────────────────

interface WikiCard {
  id: string;
  question: string;
  answer: string;
}
interface WikiChapter {
  title: string;
  slug: string;
  cards: WikiCard[];
}
interface WikiSection {
  title: string;
  slug: string;
  chapters: WikiChapter[];
}
interface WikiData {
  generated: string;
  version: number;
  sections: WikiSection[];
}

// ── Rich text helper ───────────────────────────────────────────────────────────
// Use parseFromMarkdown so LaTeX ($...$, $$...$$) renders natively in RemNote.

async function rt(plugin: RNPlugin, text: string) {
  return plugin.richText.parseFromMarkdown(text);
}

// ── Sync ───────────────────────────────────────────────────────────────────────

async function syncWikiCards(plugin: RNPlugin) {
  await plugin.app.toast("Fetching wiki flashcards...");

  // 1. Fetch JSON from deployed wiki
  let data: WikiData;
  try {
    const res = await fetch(WIKI_URL);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    data = await res.json();
  } catch (err) {
    await plugin.app.toast(`Sync failed: could not fetch wiki (${err})`);
    return;
  }

  // 2. Load persisted cardId -> remId map (survives across sessions)
  const cardMap: Record<string, string> =
    (await plugin.storage.getSynced(STORAGE_KEY)) ?? {};

  // 3. Find or create root document
  const rootDoc = await findOrCreateDocument(plugin, ROOT_NAME, undefined);
  if (!rootDoc) {
    await plugin.app.toast("Sync failed: could not create root document");
    return;
  }

  let created = 0;
  let updated = 0;
  let failed = 0;

  // 4. Walk sections -> chapters -> cards
  for (const section of data.sections) {
    const sectionRem = await findOrCreateDocument(
      plugin, section.title, rootDoc._id
    );
    if (!sectionRem) { failed++; continue; }

    for (const chapter of section.chapters) {
      const chapterRem = await findOrCreateDocument(
        plugin, chapter.title, sectionRem._id
      );
      if (!chapterRem) { failed++; continue; }

      for (const card of chapter.cards) {
        try {
          const existingRemId = cardMap[card.id];

          if (existingRemId) {
            // Update — preserves RemNote's SRS scheduling data
            const existingRem = await plugin.rem.findOne(existingRemId);
            if (existingRem) {
              await existingRem.setText(await rt(plugin, card.question));
              await existingRem.setBackText(await rt(plugin, card.answer));
              updated++;
              continue;
            }
            // rem was deleted in RemNote — fall through to recreate
          }

          // Create new flashcard rem
          const newRem = await plugin.rem.createRem();
          if (!newRem) { failed++; continue; }

          await newRem.setText(await rt(plugin, card.question));
          await newRem.setBackText(await rt(plugin, card.answer));
          await plugin.rem.moveRems([newRem], chapterRem, 0);

          cardMap[card.id] = newRem._id;
          created++;
        } catch {
          failed++;
        }
      }
    }
  }

  // 5. Persist updated map so future syncs update instead of recreate
  await plugin.storage.setSynced(STORAGE_KEY, cardMap);

  const msg = [
    `Sync complete —`,
    `${created} new,`,
    `${updated} updated`,
    failed ? `, ${failed} failed` : "",
  ].join(" ");
  await plugin.app.toast(msg);

  // 6. Make sure the ODE drill cards exist alongside the synced cards
  await ensureDrillDeck(plugin, ROOT_NAME, true);
}

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
    title: "ODE drills: cards per skill",
    description: "How many drill cards to create for each skill (each review gets a new problem).",
    defaultValue: 3,
  });
  await plugin.settings.registerNumberSetting({
    id: "drill-clear-at",
    title: "ODE drills: correct in a row to clear a skill",
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
  await plugin.app.registerWidget("drill_session", WidgetLocation.Popup, {
    dimensions: { height: "auto", width: 720 },
  });
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
      await plugin.widget.openPopup("drill_session");
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
  console.log("[WikiSync] onActivate called");
  await registerDrills(plugin);
  await plugin.app.registerCommand({
    id: "sync-wiki-cards",
    name: "Sync Wiki Cards",
    action: async () => {
      await syncWikiCards(plugin);
    },
  });
}

async function onDeactivate(_plugin: ReactRNPlugin) {}

declareIndexPlugin(onActivate, onDeactivate);
