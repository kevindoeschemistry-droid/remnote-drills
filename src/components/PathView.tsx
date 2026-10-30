// The Path tab: Khan's three moves over the whole curriculum.
//   Next up    the first objective on your track you haven't mastered, with its drill
//   Test out   a short mixed quiz over a unit's drilled objectives; pass it and the unit is mastered
//   Progress   mastered / total per framework, in path order
import React, { useCallback, useEffect, useMemo, useState } from "react";
import { usePlugin } from "@remnote/plugin-sdk";
import { DrillPanel } from "./DrillPanel";
import { getProgress } from "../drills/progress";
import {
  ensureLibrary, libraryIsBuilt, libraryIsCurrent, libraryRemId, LIBRARY, LO_BY_CODE, PATH_LOS, PathUnit, trackOrder,
} from "../drills/library-path";

const MASTERY_KEY = "path.mastery"; // code -> "tested" (passed a unit test) | "known" (marked by you)
const TRACK_KEY = "path.track";
const PASS = 0.8;
const TEST_SIZE = 8;

type Lo = (typeof PATH_LOS)[number];

export function PathView() {
  const plugin = usePlugin();
  const tracks = useMemo(trackOrder, []);
  const [track, setTrack] = useState<string>(tracks[0]);
  const [marks, setMarks] = useState<Record<string, string>>({});
  const [cleared, setCleared] = useState<Set<string>>(new Set());
  const [built, setBuilt] = useState<boolean | null>(null);
  const [current, setCurrent] = useState(true);
  const [building, setBuilding] = useState<string | null>(null);
  const [test, setTest] = useState<{ unit: PathUnit; los: Lo[]; i: number; right: number } | null>(null);
  const [n, setN] = useState(0);
  const [placing, setPlacing] = useState<string | null>(null);

  const load = useCallback(async () => {
    setMarks((await plugin.storage.getSynced<Record<string, string>>(MASTERY_KEY)) ?? {});
    const done = new Set<string>();
    for (const lo of PATH_LOS) if (lo.drills.length && (await getProgress(plugin, `lo:${lo.code}`)).cleared) done.add(lo.code);
    setCleared(done);
    setBuilt(await libraryIsBuilt(plugin));
    setCurrent(await libraryIsCurrent(plugin));
  }, [plugin]);

  useEffect(() => {
    (async () => {
      try {
        const t = await plugin.storage.getLocal<string>(TRACK_KEY);
        if (t && tracks.includes(t)) setTrack(t);
      } catch {}
      await load();
    })();
  }, []);

  const mastered = (code: string) => !!marks[code] || cleared.has(code);
  const mine = PATH_LOS.filter((lo) => lo.fw.track === track);
  const next = mine.find((lo) => !mastered(lo.code));

  const saveMarks = async (codes: string[], how: string) => {
    const m = { ...marks };
    for (const c of codes) m[c] = how;
    setMarks(m);
    await plugin.storage.setSynced(MASTERY_KEY, m);
  };

  const build = async () => {
    setBuilding("Starting…");
    try {
      await ensureLibrary(plugin, (d, t, label) => setBuilding(`${label} · ${d.toLocaleString()} of ${t.toLocaleString()}`));
      await plugin.app.toast("The Library is in RemNote.");
    } catch (e) {
      await plugin.app.toast(`Building the Library stopped — ${String(e)}. Run it again to pick up where it left off.`);
    }
    setBuilding(null);
    await load();
  };

  const open = async (code: string) => {
    const id = await libraryRemId(plugin, code);
    const rem = id ? await plugin.rem.findOne(id) : undefined;
    if (rem) await plugin.window.openRem(rem);
    else await plugin.app.toast("Build the Library first to open objectives in RemNote.");
  };

  const startTest = (unit: PathUnit) => {
    const drilled = PATH_LOS.filter((lo) => lo.unit === unit && lo.drills.length);
    const pick = [...drilled.filter((lo) => !mastered(lo.code)), ...drilled.filter((lo) => mastered(lo.code))].slice(0, TEST_SIZE);
    setTest({ unit, los: pick, i: 0, right: 0 });
    setN((k) => k + 1);
  };

  // ── test-out in progress ──────────────────────────────────────────────────
  if (test) {
    const finished = test.i >= test.los.length;
    const unitLos = PATH_LOS.filter((lo) => lo.unit === test.unit);
    if (finished) {
      const pass = test.right / test.los.length >= PASS;
      const undrilled = unitLos.filter((lo) => !lo.drills.length && !mastered(lo.code));
      return (
        <div className="path">
          <div className="path-card">
            <b>{pass ? "Passed" : "Not yet"}: Unit {test.unit.n} · {test.unit.title}</b>
            <p>
              {test.right} of {test.los.length} right first time{pass ? "" : ` — you need ${Math.ceil(PASS * test.los.length)}`}.
              {pass ? " Every drilled objective in this unit is now mastered." : " Practice the next-up objectives, then try again."}
            </p>
            {pass && undrilled.length > 0 && (
              <button className="odd-btn" onClick={() => saveMarks(undrilled.map((l) => l.code), "known")}>
                Also mark the {undrilled.length} objective{undrilled.length > 1 ? "s" : ""} without drills as known
              </button>
            )}
            <button className="odd-btn primary" onClick={() => setTest(null)}>Back to the path</button>
          </div>
        </div>
      );
    }
    const lo = test.los[test.i];
    return (
      <div className="path">
        <div className="path-head">
          <b>Test out · Unit {test.unit.n} · {test.unit.title}</b>
          <span className="odd-hint"> · question {test.i + 1} of {test.los.length} · {test.right} right</span>
          <button className="odd-linkbtn" onClick={() => setTest(null)}>stop</button>
        </div>
        <DrillPanel
          key={`${lo.code}:${n}:${test.i}`}
          skill={`lo:${lo.code}`}
          mode="session"
          onResult={async (ok) => {
            if (!ok) return;
            setTest((t) => (t ? { ...t, right: t.right + 1 } : t));
          }}
          onNext={async () => {
            const t = test;
            const right = t.right;
            const last = t.i + 1 >= t.los.length;
            if (last && right / t.los.length >= PASS) await saveMarks(unitLos.filter((l) => l.drills.length).map((l) => l.code), "tested");
            setTest({ ...t, i: t.i + 1 });
          }}
        />
      </div>
    );
  }

  // ── the path ──────────────────────────────────────────────────────────────
  const fwsHere = LIBRARY.frameworks.filter((f) => f.track === track);
  return (
    <div className="path">
      {built === false && (
        <div className="path-card">
          <b>Put the whole curriculum in RemNote</b>
          <p>
            Builds <i>KevinDoesChemistry Library</i>: {LIBRARY.frameworks.length} frameworks and {PATH_LOS.length.toLocaleString()} objectives in path order, with a drill card under every objective that has drills. It takes a while; you can keep working, and if it stops, running it again picks up where it left off.
          </p>
          <button className="odd-btn primary" disabled={!!building} onClick={build}>{building ?? "Build the Library"}</button>
        </div>
      )}
      {built && !current && (
        <div className="path-card subtle">
          The curriculum changed since the Library was built.{" "}
          <button className="odd-btn" disabled={!!building} onClick={build}>{building ?? "Update the Library"}</button>
        </div>
      )}

      <div className="hub-tabs path-tracks">
        {tracks.map((t) => (
          <button key={t} className={"hub-tab" + (t === track ? " on" : "")} onClick={async () => { setTrack(t); try { await plugin.storage.setLocal(TRACK_KEY, t); } catch {} }}>
            {LIBRARY.tracks[t] ?? t}
          </button>
        ))}
      </div>

      {next ? (
        <div className="path-card">
          <div className="odd-hint">
            Next up · #{next.pos} · {next.fw.title} › Unit {next.unit.n} › {next.unit.n}.{next.topic.n} {next.topic.title}
          </div>
          <div className="path-lo"><span className="path-code">{next.code}</span>{next.std && <span className="path-std">{next.std}</span>}</div>
          <div className="path-do">{next.do}</div>
          {next.ek && <div className="odd-hint">{next.ek}</div>}
          {next.needs.length > 0 && (
            <div className="path-needs">
              Needs:{" "}
              {next.needs.map((c) => (
                <button key={c} className={"mm-chip" + (mastered(c) ? " done" : "")} title={LO_BY_CODE.get(c)?.do} onClick={() => open(c)}>
                  {mastered(c) ? "✓ " : ""}{c}
                </button>
              ))}
            </div>
          )}
          <div className="path-row">
            <button className="odd-btn" onClick={() => open(next.code)}>Open in RemNote</button>
            {PATH_LOS.some((l) => l.unit === next.unit && l.drills.length) ? (
              <button className="odd-btn" onClick={() => startTest(next.unit)}>Test out of Unit {next.unit.n}</button>
            ) : (
              <button
                className="odd-btn"
                title="This unit has no drills to test you with yet, so this marks every objective in it known"
                onClick={() => saveMarks(PATH_LOS.filter((l) => l.unit === next.unit).map((l) => l.code), "known")}
              >
                I know Unit {next.unit.n}
              </button>
            )}
            <button className="odd-btn" onClick={() => saveMarks([next.code], "known")}>I know this one</button>
          </div>
          {next.drills.length > 0 ? (
            <DrillPanel key={`${next.code}:${n}`} skill={`lo:${next.code}`} mode="session" onNext={() => { setN((k) => k + 1); load(); }} />
          ) : (
            <div className="odd-hint path-nodrill">No drills for this objective yet. Study it in RemNote, then mark it known, or test out of the unit.</div>
          )}
        </div>
      ) : (
        <div className="path-card">Everything on the {LIBRARY.tracks[track]} track is mastered.</div>
      )}

      <div className="path-progress">
        {fwsHere.map((f) => {
          const los = PATH_LOS.filter((l) => l.fw === f);
          const m = los.filter((l) => mastered(l.code)).length;
          const d = los.filter((l) => l.drills.length).length;
          return (
            <div key={f.id} className="path-fw">
              <div className="path-fw-row">
                <span>{LIBRARY.frameworks.indexOf(f) + 1} · {f.title}</span>
                <span className="odd-hint">{m} / {los.length} mastered · {d} drilled</span>
              </div>
              {placing === f.id ? (
                <div className="path-row odd-hint">
                  Mark all {los.length - m} remaining objectives in {f.title} known?
                  <button className="odd-btn primary" onClick={async () => { await saveMarks(los.filter((l) => !mastered(l.code)).map((l) => l.code), "known"); setPlacing(null); }}>Yes, I know it</button>
                  <button className="odd-btn" onClick={() => setPlacing(null)}>Cancel</button>
                </div>
              ) : (
                m < los.length && <button className="odd-linkbtn path-place" onClick={() => setPlacing(f.id)}>I already know this</button>
              )}
              <div className="path-bar"><i style={{ width: `${(100 * m) / los.length}%` }} /></div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
