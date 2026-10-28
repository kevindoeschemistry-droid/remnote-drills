// An endless, interleaved stream of problems from one exam's skills: anything not yet cleared
// comes up 3× as often, never the same skill twice in a row. Chips pin one topic.
import React, { useCallback, useEffect, useState } from "react";
import { usePlugin } from "@remnote/plugin-sdk";
import { DrillPanel } from "./DrillPanel";
import { getProgress, SkillProgress } from "../drills/progress";
import { isLive, resolveSkill } from "../drills/skills";

export function ExamMix({ title, skills: all }: { title: string; skills: string[] }) {
  const plugin = usePlugin();
  const skills = all.filter((s) => isLive(s));
  const [progress, setProgress] = useState<Record<string, SkillProgress>>({});
  const [skill, setSkill] = useState<string | null>(null);
  const [n, setN] = useState(0);
  const [only, setOnly] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    const out: Record<string, SkillProgress> = {};
    for (const s of skills) out[s] = await getProgress(plugin, s);
    setProgress(out);
    return out;
  }, [plugin, skills.join()]);

  const pick = useCallback(async () => {
    const prog = await refresh();
    if (only) return setSkill(only);
    const pool = skills.filter((s) => s !== skill || skills.length === 1).map((s) => ({ s, w: prog[s]?.cleared ? 1 : 3 }));
    let t = Math.random() * pool.reduce((a, x) => a + x.w, 0);
    for (const x of pool) if ((t -= x.w) <= 0) return setSkill(x.s);
    setSkill(pool[pool.length - 1]?.s ?? null);
  }, [refresh, skill, only, skills.join()]);

  useEffect(() => {
    setSkill(null);
    setOnly(null);
    pick();
  }, [skills.join()]);

  const next = useCallback(() => {
    setN((k) => k + 1);
    pick();
  }, [pick]);

  if (!skills.length) return <div className="odd-hint">No live drills for this exam yet.</div>;
  if (!skill) return null;
  const cleared = skills.filter((s) => progress[s]?.cleared).length;
  return (
    <>
      <div className="mm-head">
        <b>{title}</b>
        <span className="odd-hint">
          {" "}
          · {cleared} / {skills.length} skills cleared · problem {n + 1}
        </span>
      </div>
      <div className="mm-chips">
        {skills.map((s) => (
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
    </>
  );
}
