// "Drills: Mock exam" — a whole paper at once, timed, graded only when you hand it in.
import React, { useEffect, useMemo, useState } from "react";
import { renderWidget, usePlugin } from "@remnote/plugin-sdk";
import { buildExam, drillsFor, WRITTEN } from "../drills/mock-exam";
import { resolveSkill } from "../drills/skills";
import { check } from "../drills/check";
import { MathText, Tex } from "../components/MathText";
import "../drills.css";

const stop = (e: React.SyntheticEvent) => e.stopPropagation();
const newSeed = () => (Date.now() ^ Math.floor(Math.random() * 0xffffffff)) >>> 0;
const mmss = (s: number) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;

function MockExam() {
  const plugin = usePlugin();
  const [seed, setSeed] = useState(newSeed);
  const items = useMemo(() => buildExam(seed), [seed]);
  const [answers, setAnswers] = useState<Record<number, string[]>>({});
  const [submitted, setSubmitted] = useState(false);
  const [start, setStart] = useState(Date.now());
  const [now, setNow] = useState(Date.now());
  const [openSteps, setOpenSteps] = useState<Record<number, boolean>>({});

  useEffect(() => {
    if (submitted) return;
    const t = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(t);
  }, [submitted]);

  const results = useMemo(
    () =>
      submitted
        ? items.map((it) => {
            const a = it.problem.answer;
            const given = answers[it.n] ?? [];
            if (!given.some((x) => x?.trim())) return { ok: false, msg: "No answer." };
            const r = check(it.problem, a.kind === "tuple" ? given : given[0]);
            return { ok: r.status === "correct", msg: r.status === "correct" ? "" : r.message };
          })
        : [],
    [submitted, items, answers]
  );
  const total = items.reduce((s, it) => s + it.points, 0);
  const score = results.reduce((s, r, i) => s + (r.ok ? items[i].points : 0), 0);
  const elapsed = Math.round((now - start) / 1000);
  const todo = useMemo(() => (submitted ? drillsFor(items, results.map((r) => r.ok)) : []), [submitted, items, results]);

  const set = (n: number, i: number, v: string) =>
    setAnswers((all) => {
      const cur = [...(all[n] ?? [])];
      cur[i] = v;
      return { ...all, [n]: cur };
    });

  const restart = () => {
    setSeed(newSeed());
    setAnswers({});
    setSubmitted(false);
    setOpenSteps({});
    setStart(Date.now());
    setNow(Date.now());
  };

  let lastSection = "";
  return (
    <div className="odd-panel mx-exam" onKeyDown={stop} onKeyUp={stop} onKeyPress={stop}>
      <div className="mx-top">
        <span className="odd-skill">Mock exam · MAE 120 format · Incropera Ch 1–5</span>
        <span className="mx-timer">
          {submitted ? `Score ${score} / ${total} · ${mmss(elapsed)}` : `⏱ ${mmss(elapsed)}`}
          {!submitted ? (
            <button className="odd-btn primary mx-handin" onClick={() => setSubmitted(true)}>
              Hand in
            </button>
          ) : (
            <button className="odd-btn primary mx-handin" onClick={restart}>
              New paper
            </button>
          )}
        </span>
      </div>
      {submitted && (
        <div className="mx-todo">
          {todo.length === 0 ? (
            <b>Clean paper. Do another one to be sure.</b>
          ) : (
            <>
              <b>Drill these next</b> <span className="odd-hint">(most points lost first; opens the drill)</span>
              <ol>
                {todo.map((t) => (
                  <li key={t.skill}>
                    <button className="odd-source-btn mx-link" onClick={() => plugin.widget.openPopup("drill_session", { skill: t.skill })}>
                      {resolveSkill(t.skill)?.title ?? t.skill}
                    </button>{" "}
                    <span className="odd-hint">
                      −{t.lost} pts · problem{t.questions.length > 1 ? "s" : ""} {t.questions.join(", ")}
                    </span>
                  </li>
                ))}
              </ol>
              <span className="odd-hint">Opening a drill closes this paper, so look over the solutions below first.</span>
            </>
          )}
        </div>
      )}
      {!submitted && (
        <p className="odd-hint">
          Work it like the real thing: no notes, no checking as you go. Numeric answers count within 1%; round only at the end.
          Hand it in at the bottom.
        </p>
      )}

      {items.map((it, idx) => {
        const a = it.problem.answer;
        const header = it.section !== lastSection ? it.section : null;
        lastSection = it.section;
        const res = results[idx];
        const given = answers[it.n] ?? [];
        return (
          <React.Fragment key={it.n}>
            {header && <div className="mx-section">{header}</div>}
            <div className={"mx-q" + (submitted ? (res?.ok ? " ok" : " bad") : "")}>
              <div className="mx-qhead">
                <b>Problem {it.n}.</b> <span className="odd-hint">({it.points} points)</span>
                {submitted && <span className="mx-mark">{res?.ok ? "✓" : "✗"}</span>}
              </div>
              <div className="odd-prompt">
                <MathText text={it.problem.prompt} />
              </div>
              {it.problem.figure && <div className="odd-figure" dangerouslySetInnerHTML={{ __html: it.problem.figure }} />}
              {a.kind === "choice" ? (
                <div className="odd-choices">
                  {a.options.map((opt) => (
                    <button
                      key={opt}
                      className={
                        "odd-choice" +
                        (given[0] === opt ? " picked" : "") +
                        (submitted && opt === a.correct ? " right" : "") +
                        (submitted && given[0] === opt && opt !== a.correct ? " missed" : "")
                      }
                      disabled={submitted}
                      onClick={() => set(it.n, 0, opt)}
                    >
                      {opt}
                    </button>
                  ))}
                </div>
              ) : a.kind === "tuple" ? (
                <div className="odd-fields">
                  {a.fields.map((f, i) => (
                    <label key={f.label} className="odd-field">
                      <span className="odd-field-label">
                        <Tex tex={f.tex} /> =
                      </span>
                      <input className="odd-input" value={given[i] ?? ""} readOnly={submitted} onChange={(e) => set(it.n, i, e.target.value)} />
                    </label>
                  ))}
                </div>
              ) : (
                <input
                  className="odd-input"
                  value={given[0] ?? ""}
                  readOnly={submitted}
                  placeholder={a.kind === "expression" ? `${a.label ?? "answer"} = …${a.unit ? `   (${a.unit})` : ""}` : "answer"}
                  spellCheck={false}
                  autoComplete="off"
                  onChange={(e) => set(it.n, 0, e.target.value)}
                />
              )}
              {submitted && (
                <div className="mx-answer">
                  {!res?.ok && res?.msg && <div className="odd-hint">{res.msg}</div>}
                  <div>
                    Answer: <Tex tex={it.problem.answerTex} />{" "}
                    <button className="odd-source-btn mx-link" onClick={() => setOpenSteps((o) => ({ ...o, [it.n]: !o[it.n] }))}>
                      {openSteps[it.n] ? "hide solution" : "show solution"}
                    </button>
                  </div>
                  {openSteps[it.n] && (
                    <ol className="odd-steps">
                      {it.problem.steps.map((s, k) => (
                        <li key={k}>
                          <MathText text={s} />
                        </li>
                      ))}
                    </ol>
                  )}
                </div>
              )}
            </div>
          </React.Fragment>
        );
      })}

      <div className="mx-section">Free response — written (check yourself)</div>
      {WRITTEN.map((w, i) => (
        <div key={i} className="mx-q">
          <div className="odd-prompt">
            <MathText text={w.prompt} />
          </div>
          {!submitted ? (
            <p className="odd-hint">Write this one on paper. The model answer appears when you hand in.</p>
          ) : (
            <ul className="odd-steps">
              {w.model.map((line, k) => (
                <li key={k}>
                  <MathText text={line} />
                </li>
              ))}
            </ul>
          )}
        </div>
      ))}

      <div className="odd-actions mx-actions">
        {!submitted ? (
          <button className="odd-btn primary" onClick={() => setSubmitted(true)}>
            Hand in
          </button>
        ) : (
          <>
            <span className="mx-final">
              {score} / {total} ({Math.round((100 * score) / total)}%) in {mmss(elapsed)}
            </span>
            <button className="odd-btn primary" onClick={restart}>
              New paper
            </button>
          </>
        )}
      </div>
    </div>
  );
}

renderWidget(MockExam);
