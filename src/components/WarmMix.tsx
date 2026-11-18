// Warm-up mix: an endless stream of problems from everything already easy for you.
// Chips narrow it to one subject. Nothing here can be finished; that's the point.
import React, { useCallback, useEffect, useState } from "react";
import { usePlugin } from "@remnote/plugin-sdk";
import { DrillPanel } from "./DrillPanel";
import { pickWarm, warmPool, WarmItem } from "../drills/warm";

export function WarmMix() {
  const plugin = usePlugin();
  const [pool, setPool] = useState<WarmItem[] | null>(null);
  const [now, setNow] = useState<WarmItem | null>(null);
  const [group, setGroup] = useState<string | null>(null);
  const [n, setN] = useState(0);
  const [done, setDone] = useState(0);

  useEffect(() => {
    (async () => {
      const p = await warmPool(plugin);
      setPool(p);
      setNow(pickWarm(p, null, null) ?? null);
    })();
  }, []);

  const next = useCallback(
    (g: string | null = group) => {
      if (!pool) return;
      setNow(pickWarm(pool, now?.target ?? null, g) ?? null);
      setN((k) => k + 1);
    },
    [pool, now, group],
  );

  if (!pool) return <div className="odd-hint">Gathering what's warm…</div>;
  if (!pool.length || !now)
    return (
      <div className="path-card">
        <b>Nothing is warm yet</b>
        <p>
          A skill joins the warm-up mix once you get five in a row on it. Objectives you mark as known on the Path tab join straight away, so "I already know this" on a framework fills the mix
          in one click.
        </p>
      </div>
    );
  const groups = [...new Set(pool.map((x) => x.group))];
  return (
    <>
      <div className="mm-head">
        <b>Warm-up mix</b>
        <span className="odd-hint">
          {" "}
          · {pool.length} warm · {done} done this session
        </span>
      </div>
      {groups.length > 1 && (
        <div className="mm-chips">
          {groups.map((g) => (
            <button
              key={g}
              className={"mm-chip" + (group === g ? " on" : "")}
              title={group === g ? "Back to everything" : "Only this subject"}
              onClick={() => {
                const to = group === g ? null : g;
                setGroup(to);
                next(to);
              }}
            >
              {g} · {pool.filter((x) => x.group === g).length}
            </button>
          ))}
        </div>
      )}
      <DrillPanel key={`${now.target}:${n}`} skill={now.target} mode="session" onResult={() => setDone((k) => k + 1)} onNext={() => next()} />
    </>
  );
}
