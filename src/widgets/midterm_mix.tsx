// "Drills: Midterm mix" — an endless stream of problems from the midterm's skills only,
// weighted toward the exam-style sets and anything not yet cleared. No spaced repetition.
import React, { useCallback, useEffect, useState } from "react";
import { renderWidget, usePlugin } from "@remnote/plugin-sdk";
import { DrillPanel } from "../components/DrillPanel";
import { MIDTERM_SKILLS } from "../drills/mock-exam";
import { getProgress, SkillProgress } from "../drills/progress";
import { resolveSkill } from "../drills/skills";
import "../drills.css";

function MidtermMix() {
  const plugin = usePlugin();
  const [progress, setProgress] = useState<Record<string, SkillProgress>>({});
  const [skill, setSkill] = useState<string | null>(null);
  const [n, setN] = useState(0);
  const [only, setOnly] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    const all: Record<string, SkillProgress> = {};
    for (const { skill: s } of MIDTERM_SKILLS) all[s] = await getProgress(plugin, s);
    setProgress(all);
    return all;
  }, [plugin]);

  const pick = useCallback(async () => {
    const all = await refresh();
    if (only) return setSkill(only);
    // not cleared counts 3x; never the same skill twice in a row when there's a choice
    const pool = MIDTERM_SKILLS.filter((x) => x.skill !== skill || MIDTERM_SKILLS.length === 1).map((x) => ({
      ...x,
      w: x.weight * (all[x.skill]?.cleared ? 1 : 3),
    }));
    let t = Math.random() * pool.reduce((s, x) => s + x.w, 0);
    for (const x of pool) if ((t -= x.w) <= 0) return setSkill(x.skill);
    setSkill(pool[pool.length - 1].skill);
  }, [refresh, skill, only]);

  useEffect(() => {
    pick();
  }, []);

  const next = useCallback(() => {
    setN((k) => k + 1);
    pick();
  }, [pick]);

  const cleared = MIDTERM_SKILLS.filter((x) => progress[x.skill]?.cleared).length;
  if (!skill) return null;
  return (
    <div className="odd-session">
      <div className="mm-head">
        <b>Midterm mix</b>
        <span className="odd-hint">
          {" "}
          · {cleared} / {MIDTERM_SKILLS.length} topics cleared · problem {n + 1}
        </span>
      </div>
      <div className="mm-chips">
        {MIDTERM_SKILLS.map(({ skill: s }) => (
          <button
            key={s}
            className={"mm-chip" + (progress[s]?.cleared ? " done" : "") + (only === s ? " on" : "") + (skill === s ? " now" : "")}
            title={only === s ? "Back to the mix" : "Stay on this topic"}
            onClick={() => {
              const o = only === s ? null : s;
              setOnly(o);
              if (o) {
                setSkill(o);
                setN((k) => k + 1);
              }
            }}
          >
            {progress[s]?.cleared ? "✓ " : ""}
            {resolveSkill(s)?.short ?? s}
          </button>
        ))}
      </div>
      <DrillPanel key={`${skill}:${n}`} skill={skill} mode="session" onNext={next} />
    </div>
  );
}

renderWidget(MidtermMix);
