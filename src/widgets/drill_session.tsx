// Unlimited Kuta-style practice: pick a skill, drill until it clears.
// Opens as a popup ("ODE Drills: Practice") and as a right-sidebar tab.
import React, { useEffect, useState } from "react";
import { renderWidget, usePlugin, useRunAsync, WidgetLocation } from "@remnote/plugin-sdk";
import { DrillPanel } from "../components/DrillPanel";
import { isLive, liveByDomain, resolveSkill } from "../drills/skills";
import { getProgress, SkillProgress } from "../drills/progress";
import "../drills.css";

const LAST_KEY = "odeDrill.lastSkill";

function DrillSession() {
  const plugin = usePlugin();
  const ctx = useRunAsync(async () => {
    try {
      return await plugin.widget.getWidgetContext<WidgetLocation.Popup>();
    } catch {
      return undefined;
    }
  }, []);
  const [skill, setSkill] = useState<string | null>(null);
  const [progress, setProgress] = useState<Record<string, SkillProgress>>({});
  const groups = liveByDomain();

  useEffect(() => {
    (async () => {
      const fromCtx = ctx?.contextData?.skill;
      const last = await plugin.storage.getLocal<string>(LAST_KEY);
      const pick = [fromCtx, last].find((s) => isLive(s));
      setSkill(pick ? resolveSkill(pick)!.id : groups[0].skills[0].id);
    })();
  }, [ctx]);

  useEffect(() => {
    (async () => {
      const all: Record<string, SkillProgress> = {};
      for (const g of groups) for (const s of g.skills) all[s.id] = await getProgress(plugin, s.id);
      setProgress(all);
    })();
  }, [skill]);

  if (!skill) return null;
  return (
    <div className="odd-session mm-scroll">
      <select
        className="odd-select"
        value={skill}
        onChange={async (e) => {
          setSkill(e.target.value);
          await plugin.storage.setLocal(LAST_KEY, e.target.value);
        }}
      >
        {groups.map((g) => (
          <optgroup key={g.domain.id} label={g.domain.title}>
            {g.skills.map((s) => (
              <option key={s.id} value={s.id}>
                {progress[s.id]?.cleared ? "✓ " : ""}
                {s.title}
              </option>
            ))}
          </optgroup>
        ))}
      </select>
      <DrillPanel key={skill} skill={skill} mode="session" />
    </div>
  );
}

renderWidget(DrillSession);
