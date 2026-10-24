import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { usePlugin, QueueInteractionScore } from "@remnote/plugin-sdk";
import { generate } from "../drills/registry";
import { placeText, primaryPlace, resolveSkill, videosFor, WIKI_BASE } from "../drills/skills";
import { anchorFor, openPlace } from "../drills/anchors";
import { getBindings } from "../drills/deck";
import { check, previewTex } from "../drills/check";
import { recurrencePreview } from "../drills/check-kinds";
import { getProgress, recordAttempt, resetProgress, SkillProgress, EMPTY } from "../drills/progress";
import type { Answer, CheckResult, Problem } from "../drills/types";
import { MathText, Tex } from "./MathText";

type Phase = "answering" | "correct" | "wrong" | "revealed";

const newSeed = () => (Date.now() ^ Math.floor(Math.random() * 0xffffffff)) >>> 0;

/** Keep typing inside the drill from triggering RemNote's queue shortcuts. */
const stop = (e: React.SyntheticEvent) => e.stopPropagation();

function inputHelp(a: Answer): { placeholder: string; hint: string } {
  switch (a.kind) {
    case "ode":
      return {
        placeholder: a.ic ? "y = …" : "y = …   (use C for the constant)",
        hint: "Type math like 2x, e^(3x), ln|x|, sqrt(x), sin(x). Implicit answers (y^2 = …) are fine.",
      };
    case "ode2":
      return {
        placeholder: a.ic || a.particular ? `y${a.particular ? "_p" : ""} = …   (in terms of ${a.v})` : "y = …   (use C1, C2)",
        hint: `Type math like 3cos(2${a.v}) - sin(2${a.v}), (C1 + C2 ${a.v})e^(-${a.v}) or ${a.v}^2 e^(3${a.v}).`,
      };
    case "expression":
      return {
        placeholder: `${a.label ?? "answer"} = …${a.unit ? `   (${a.unit})` : ""}`,
        hint: a.rel
          ? `A number${a.unit ? ` in ${a.unit}` : ""} — within 1% counts. 2.5e4 and 25000 both work.`
          : a.vars?.length === 0 ? "A number: 2, sqrt(5), 3/2 …" : "Type math like 2e^(3x), 1 + x - x^3/6.",
      };
    case "recurrence":
      return {
        placeholder: "a_{n+k} = …   (k as the recurrence needs)",
        hint: "Write coefficients as a_{n+2}, a_(n+2) or a_n; any index letter (n, k, m) works.",
      };
    case "roots":
      return { placeholder: `${a.label ?? "r"} = …, …`, hint: "Separate roots with commas, e.g. 1/2, -1." };
    case "indexed":
      return { placeholder: `${a.label} = …   (in terms of n)`, hint: "Use n, e.g. (n pi/2)^2 or n^2." };
    case "eigenfunctions":
      return { placeholder: "y_n = …   (in terms of n and x)", hint: "Use n and x, e.g. sin(n pi x/3). Any constant multiple is fine." };
    default:
      return { placeholder: "", hint: "" };
  }
}

export function DrillPanel({ skill, mode }: { skill: string; mode: "card" | "session" }) {
  const plugin = usePlugin();
  const meta = resolveSkill(skill)!;
  const [seed, setSeed] = useState(newSeed);
  const problem: Problem = useMemo(() => generate(meta.id, seed), [meta.id, seed]);
  const a = problem.answer;
  const nFields = a.kind === "tuple" ? a.fields.length : 1;
  const [inputs, setInputs] = useState<string[]>([""]);
  const [chosen, setChosen] = useState<string | null>(null);
  const [phase, setPhase] = useState<Phase>("answering");
  const [result, setResult] = useState<CheckResult | null>(null);
  const [progress, setProgress] = useState<SkillProgress>(EMPTY);
  const [clearAt, setClearAt] = useState(5);
  const [prefSource, setPrefSource] = useState<string | undefined>();
  const [missedOnce, setMissedOnce] = useState(false);
  const [showMethod, setShowMethod] = useState(false);
  const firstRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    let live = true;
    (async () => {
      const ca = (await plugin.settings.getSetting<number>("drill-clear-at")) || 5;
      const pref = (await plugin.settings.getSetting<string>("drill-label-source")) || undefined;
      const p = await getProgress(plugin, meta.id);
      if (live) {
        setClearAt(ca);
        setPrefSource(pref);
        setProgress(p);
      }
    })();
    return () => {
      live = false;
    };
  }, [plugin, meta.id]);

  useEffect(() => {
    setInputs(Array(nFields).fill(""));
    setChosen(null);
    setPhase("answering");
    setResult(null);
    setMissedOnce(false);
    firstRef.current?.focus();
  }, [problem, nFields]);

  const done = phase === "correct" || phase === "revealed";

  const submit = useCallback(
    async (answer: string | string[]) => {
      if (done) return;
      const r = check(problem, answer);
      setResult(r);
      if (r.status === "syntax" || r.status === "needs-constant" || r.status === "has-constant") return;
      if (r.status === "correct") {
        setPhase("correct");
        // a miss earlier on this problem already broke the streak
        if (!missedOnce) setProgress(await recordAttempt(plugin, meta.id, "correct", clearAt));
      } else {
        setPhase(a.kind === "choice" ? "revealed" : "wrong");
        if (!missedOnce) {
          setMissedOnce(true);
          setProgress(await recordAttempt(plugin, meta.id, "wrong", clearAt));
        }
      }
    },
    [done, problem, missedOnce, plugin, meta.id, clearAt, a.kind]
  );

  const doCheck = useCallback(() => submit(a.kind === "tuple" ? inputs : inputs[0]), [submit, inputs, a.kind]);

  const reveal = useCallback(async () => {
    setPhase("revealed");
    if (!missedOnce) {
      setMissedOnce(true);
      setProgress(await recordAttempt(plugin, meta.id, "revealed", clearAt));
    }
  }, [missedOnce, plugin, meta.id, clearAt]);

  const next = useCallback(() => setSeed(newSeed()), []);

  const rate = useCallback(
    async (score: QueueInteractionScore) => {
      try {
        await plugin.queue.rateCurrentCard(score);
      } catch {
        await plugin.app.toast("Use the queue's rating buttons for this card.");
      }
    },
    [plugin]
  );

  const onKey = (e: React.KeyboardEvent, i: number) => {
    e.stopPropagation();
    if (e.key !== "Enter") return;
    e.preventDefault();
    if (done) return next();
    if (a.kind === "tuple" && i < nFields - 1 && !inputs[i + 1]) {
      (e.currentTarget.parentElement?.parentElement?.querySelectorAll("input")[i + 1] as HTMLInputElement)?.focus();
      return;
    }
    doCheck();
  };

  const setInput = (i: number, v: string) => {
    setInputs((xs) => xs.map((x, k) => (k === i ? v : x)));
    if (phase === "wrong") setPhase("answering");
  };

  const help = inputHelp(a);
  const place = primaryPlace(meta.id, prefSource);
  // where the label goes: "anchor" (your PDF at the section), "pdf" (your PDF), or the wiki
  const [bookTarget, setBookTarget] = useState<"anchor" | "pdf" | "wiki">("wiki");
  useEffect(() => {
    let live = true;
    (async () => {
      if (!place) return;
      const t = (await anchorFor(plugin, place)) ? "anchor" : (await getBindings(plugin))[place.source.id] ? "pdf" : "wiki";
      if (live) setBookTarget(t);
    })();
    return () => {
      live = false;
    };
  }, [plugin, place?.source.id, place?.ref]);
  const videos = videosFor(place);
  const [showVideos, setShowVideos] = useState(false);
  const openBook = async () => {
    if (!place) return;
    const r = await openPlace(plugin, place);
    if (r !== "none") return setBookTarget((t) => (t === "wiki" ? "pdf" : t));
    if (place.wiki) window.open(WIKI_BASE + place.wiki, "_blank", "noopener");
    else
      await plugin.app.toast(
        `No ${place.source.short} PDF found in RemNote. Upload it, or open it and run “Drills: Anchor this section”.`
      );
  };
  const preview = useMemo(() => {
    const s = inputs[0] ?? "";
    if (!s.trim()) return null;
    return a.kind === "recurrence" ? recurrencePreview(s) : previewTex(s);
  }, [inputs, a.kind]);

  return (
    <div className="odd-panel" onKeyDown={stop} onKeyUp={stop} onKeyPress={stop}>
      <div className="odd-header">
        <span className="odd-skill">
          {place && (
            <>
              {bookTarget !== "wiki" ? (
                <button
                  className="odd-source odd-source-btn"
                  onClick={openBook}
                  title={bookTarget === "anchor" ? "Open your PDF at this section" : "Open your PDF (anchor this section to jump straight to it)"}
                >
                  📖 {placeText(place)}
                </button>
              ) : (
                <button className="odd-source odd-source-btn" onClick={openBook} title="Open this section in your PDF (finds and links the book's PDF if it's in RemNote)">
                  {placeText(place)}
                </button>
              )}
              {videos.length > 0 && " "}
              {videos.length > 0 && (
                <button
                  className="odd-source odd-source-btn"
                  onClick={() => setShowVideos((v) => !v)}
                  title="Videos that teach this section"
                >
                  🎬{videos.length > 1 ? ` ${videos.length}` : ""}
                </button>
              )}
              {" · "}
            </>
          )}
          {meta.title}
        </span>
        <span className="odd-pips" title={`${progress.consecutive} in a row`}>
          {Array.from({ length: clearAt }, (_, i) => (
            <span key={i} className={"odd-pip" + (i < Math.min(progress.consecutive, clearAt) ? " on" : "")} />
          ))}
        </span>
        <span className="odd-count">
          {progress.cleared ? "Cleared ✓ · " : ""}
          {Math.min(progress.consecutive, clearAt)} / {clearAt}
        </span>
      </div>

      {showVideos && videos.length > 0 && (
        <div className="odd-videos">
          {videos.map((v) => (
            <a key={v.url} className="odd-video" href={v.url} target="_blank" rel="noopener noreferrer">
              🎬 {v.title}
            </a>
          ))}
        </div>
      )}

      <div className="odd-prompt">
        <MathText text={problem.prompt} />
      </div>

      {a.kind === "choice" ? (
        <div className="odd-choices">
          {a.options.map((opt) => {
            const cls =
              "odd-choice" +
              (done && opt === a.correct ? " right" : "") +
              (done && chosen === opt && opt !== a.correct ? " missed" : "");
            return (
              <button
                key={opt}
                className={cls}
                disabled={done}
                onClick={() => {
                  setChosen(opt);
                  submit(opt);
                }}
              >
                {opt}
              </button>
            );
          })}
        </div>
      ) : a.kind === "tuple" ? (
        <div className="odd-fields">
          {a.fields.map((f, i) => (
            <label key={f.label} className="odd-field">
              <span className="odd-field-label">
                <Tex tex={f.tex} /> =
              </span>
              <input
                ref={i === 0 ? firstRef : undefined}
                className="odd-input"
                value={inputs[i] ?? ""}
                spellCheck={false}
                autoCapitalize="off"
                autoComplete="off"
                onChange={(e) => setInput(i, e.target.value)}
                onKeyDown={(e) => onKey(e, i)}
                readOnly={done}
              />
              <span className="odd-field-preview">
                {inputs[i]?.trim() && previewTex(inputs[i]) ? <Tex tex={previewTex(inputs[i])!} /> : null}
              </span>
            </label>
          ))}
          {!done && (
            <button className="odd-btn primary odd-fields-check" onClick={doCheck}>
              Check
            </button>
          )}
        </div>
      ) : (
        <>
          <div className="odd-row">
            <input
              ref={firstRef}
              className="odd-input"
              value={inputs[0] ?? ""}
              placeholder={help.placeholder}
              spellCheck={false}
              autoCapitalize="off"
              autoComplete="off"
              onChange={(e) => setInput(0, e.target.value)}
              onKeyDown={(e) => onKey(e, 0)}
              readOnly={done}
            />
            {!done && (
              <button className="odd-btn primary" onClick={doCheck}>
                Check
              </button>
            )}
          </div>
          <div className="odd-preview">
            {preview ? (
              <>
                reads as <Tex tex={preview} />
              </>
            ) : (
              <span className="odd-hint">{help.hint}</span>
            )}
          </div>
        </>
      )}

      {result && (
        <div className={"odd-result " + (phase === "correct" ? "ok" : result.status === "wrong" ? "bad" : "warn")}>
          {result.message}
        </div>
      )}

      {done && (
        <div className="odd-solution">
          <div className="odd-answer">
            <Tex tex={problem.answerTex} />
          </div>
          <ol className="odd-steps">
            {problem.steps.map((s, i) => (
              <li key={i}>
                <MathText text={s} />
              </li>
            ))}
          </ol>
        </div>
      )}

      {showMethod && meta.method && (
        <div className="odd-method">
          <div className="odd-method-title">Method · {meta.short}</div>
          <ul>
            {meta.method.map((line, i) => (
              <li key={i}>
                <MathText text={line} />
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="odd-actions">
        {!done && (
          <button className="odd-btn" onClick={reveal}>
            Show solution
          </button>
        )}
        {meta.method && (
          <button
            className={"odd-btn" + (phase === "wrong" && !showMethod ? " nudge" : "")}
            onClick={() => setShowMethod((v) => !v)}
            title="Formulas, when to use them, and the usual traps"
          >
            {showMethod ? "Hide method" : "Method"}
          </button>
        )}
        {done && (
          <button className="odd-btn primary" onClick={next}>
            Next problem ↵
          </button>
        )}
        {mode === "card" && done && (
          <>
            {phase === "correct" && !missedOnce ? (
              <button className="odd-btn good" onClick={() => rate(QueueInteractionScore.GOOD)}>
                Rate Good → next card
              </button>
            ) : (
              <button className="odd-btn again" onClick={() => rate(QueueInteractionScore.AGAIN)}>
                Rate Again → next card
              </button>
            )}
          </>
        )}
        {mode === "session" && (
          <button
            className="odd-btn subtle"
            onClick={async () => {
              await resetProgress(plugin, meta.id);
              setProgress(await getProgress(plugin, meta.id));
            }}
          >
            reset streak
          </button>
        )}
      </div>
    </div>
  );
}
