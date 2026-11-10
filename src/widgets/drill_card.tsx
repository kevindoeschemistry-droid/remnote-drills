// Renders under any flashcard tagged with the "ODE Drill" powerup:
// a fresh problem every time the card comes up, checked as you type.
import React from "react";
import { renderWidget, usePlugin, useRunAsync, WidgetLocation } from "@remnote/plugin-sdk";
import { DrillPanel } from "../components/DrillPanel";
import { isDrillable } from "../drills/target";
import { DRILL_POWERUP, DRILL_SLOT } from "../drills/deck";
import { SEED_SLOT } from "../drills/static-card";
import "../drills.css";

function DrillCard() {
  const plugin = usePlugin();
  const ctx = useRunAsync(() => plugin.widget.getWidgetContext<WidgetLocation.FlashcardUnder>(), []);
  const skill = useRunAsync(async () => {
    if (!ctx?.remId) return undefined;
    const rem = await plugin.rem.findOne(ctx.remId);
    if (!rem) return undefined;
    const skill = (await rem.getPowerupProperty(DRILL_POWERUP, DRILL_SLOT))?.trim();
    const seed = Number((await rem.getPowerupProperty(DRILL_POWERUP, SEED_SLOT))?.trim());
    return { skill, seed: Number.isFinite(seed) && seed > 0 ? seed : undefined };
  }, [ctx?.remId]);

  if (!ctx?.remId) return null;
  if (skill === undefined) return null;
  if (!isDrillable(skill.skill)) return <div className="odd-panel">Unknown drill skill “{skill.skill}”.</div>;
  // the card's own text shows the problem; check that same problem (seed), without repeating it
  return <DrillPanel key={`${ctx.cardId ?? ctx.remId}:${skill.seed}`} skill={skill.skill!} mode="card" seed={skill.seed} hidePrompt={!!skill.seed} />;
}

renderWidget(DrillCard);
