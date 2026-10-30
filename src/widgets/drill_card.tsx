// Renders under any flashcard tagged with the "ODE Drill" powerup:
// a fresh problem every time the card comes up, checked as you type.
import React from "react";
import { renderWidget, usePlugin, useRunAsync, WidgetLocation } from "@remnote/plugin-sdk";
import { DrillPanel } from "../components/DrillPanel";
import { isDrillable } from "../drills/target";
import { DRILL_POWERUP, DRILL_SLOT } from "../drills/deck";
import "../drills.css";

function DrillCard() {
  const plugin = usePlugin();
  const ctx = useRunAsync(() => plugin.widget.getWidgetContext<WidgetLocation.FlashcardUnder>(), []);
  const skill = useRunAsync(async () => {
    if (!ctx?.remId) return undefined;
    const rem = await plugin.rem.findOne(ctx.remId);
    if (!rem) return undefined;
    return (await rem.getPowerupProperty(DRILL_POWERUP, DRILL_SLOT))?.trim();
  }, [ctx?.remId]);

  if (!ctx?.remId) return null;
  if (skill === undefined) return null;
  if (!isDrillable(skill)) return <div className="odd-panel">Unknown drill skill “{skill}”.</div>;
  // key on the card so a new card always starts a new problem
  return <DrillPanel key={ctx.cardId ?? ctx.remId} skill={skill} mode="card" />;
}

renderWidget(DrillCard);
