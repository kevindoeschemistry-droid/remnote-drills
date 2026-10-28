// The Drills sidebar ("Drills: Open"): everything that isn't a card in the queue.
//   Practice   pick a skill (in course order, gaps shown) and drill until it clears
//   Exam mix   interleaved problems from the next exam's units
//   Courses    build / update a course, plus the one-off setup tools
import React, { useEffect, useMemo, useState } from "react";
import { renderWidget, usePlugin } from "@remnote/plugin-sdk";
import { DrillPanel } from "../components/DrillPanel";
import { ExamMix } from "../components/ExamMix";
import { COURSES, isLive, liveByDomain, resolveSkill } from "../drills/skills";
import { getProgress, SkillProgress } from "../drills/progress";
import { builtCourses, coursesWithUnits, ensureCourse, nextMilestone } from "../drills/course";
import { ensureDrillDeck, LEGACY_ROOT } from "../drills/deck";
import { organizeLibrary } from "../drills/library";
import "../drills.css";

const LAST_KEY = "odeDrill.lastSkill";
const COURSE_KEY = "drills.hubCourse";
const TAB_KEY = "drills.hubTab";
type Tab = "practice" | "exam" | "courses";

const lessonLabel = (ref: string, title: string) => (/^\d/.test(ref) ? `§${ref} ${title}` : title);

async function local<T>(plugin: ReturnType<typeof usePlugin>, key: string): Promise<T | undefined> {
  try {
    return (await plugin.storage.getLocal<T>(key)) ?? undefined;
  } catch {
    return undefined;
  }
}

function Hub() {
  const plugin = usePlugin();
  const courses = coursesWithUnits();
  const [tab, setTab] = useState<Tab>("practice");
  const [courseId, setCourseId] = useState<string>("all");
  const [skill, setSkill] = useState<string | null>(null);
  const [progress, setProgress] = useState<Record<string, SkillProgress>>({});
  const [built, setBuilt] = useState<string[]>([]);
  const [busy, setBusy] = useState<string | null>(null);
  const course = COURSES.find((c) => c.id === courseId);

  useEffect(() => {
    (async () => {
      const b = await builtCourses(plugin);
      setBuilt(b);
      const c = (await local<string>(plugin, COURSE_KEY)) ?? b[0] ?? "all";
      setCourseId(c);
      setTab((await local<Tab>(plugin, TAB_KEY)) ?? "practice");
      const last = await local<string>(plugin, LAST_KEY);
      setSkill(isLive(last) ? resolveSkill(last)!.id : liveByDomain()[0].skills[0].id);
    })();
  }, []);

  // the skill list: the course's lessons in order (gaps shown, disabled), or every live skill by domain
  const groups = useMemo(() => {
    if (!course?.units) return liveByDomain().map((g) => ({ title: g.domain.title, items: g.skills.map((s) => ({ id: s.id, label: s.title, gap: false })) }));
    return course.units.map((u, i) => ({
      title: `Unit ${i + 1} · ${u.title}`,
      items: u.lessons.flatMap((l) =>
        l.skills.length
          ? l.skills.map((s) => ({ id: s, label: `${lessonLabel(l.ref, l.title)} · ${resolveSkill(s)?.short ?? s}`, gap: !isLive(s) }))
          : [{ id: `gap:${u.id}:${l.ref}`, label: `${lessonLabel(l.ref, l.title)} · no drills yet`, gap: true }]
      ),
    }));
  }, [courseId]);

  useEffect(() => {
    (async () => {
      const all: Record<string, SkillProgress> = {};
      for (const g of groups) for (const it of g.items) if (!it.gap) all[it.id] = await getProgress(plugin, it.id);
      setProgress(all);
    })();
  }, [groups, skill]);

  const pickTab = async (t: Tab) => {
    setTab(t);
    await plugin.storage.setLocal(TAB_KEY, t);
  };
  const pickCourse = async (c: string) => {
    setCourseId(c);
    await plugin.storage.setLocal(COURSE_KEY, c);
  };
  const run = async (label: string, f: () => Promise<unknown>) => {
    setBusy(label);
    try {
      await f();
    } catch (e) {
      await plugin.app.toast(`${label} failed — ${String(e)}`);
    }
    setBusy(null);
    setBuilt(await builtCourses(plugin));
  };

  const exam = course ? nextMilestone(course) : undefined;
  if (!skill) return null;
  return (
    <div className="odd-session mm-scroll">
      <div className="hub-top">
        <select className="odd-select hub-course" value={courseId} onChange={(e) => pickCourse(e.target.value)}>
          {courses.map((c) => (
            <option key={c.id} value={c.id}>
              {c.title}
            </option>
          ))}
          <option value="all">All skills</option>
        </select>
        <div className="hub-tabs">
          {(["practice", "exam", "courses"] as Tab[]).map((t) => (
            <button key={t} className={"hub-tab" + (tab === t ? " on" : "")} onClick={() => pickTab(t)}>
              {t === "practice" ? "Practice" : t === "exam" ? "Exam mix" : "Courses"}
            </button>
          ))}
        </div>
      </div>

      {tab === "practice" && (
        <>
          <select
            className="odd-select"
            value={skill}
            onChange={async (e) => {
              setSkill(e.target.value);
              await plugin.storage.setLocal(LAST_KEY, e.target.value);
            }}
          >
            {!groups.some((g) => g.items.some((it) => it.id === skill)) && <option value={skill}>{resolveSkill(skill)?.title}</option>}
            {groups.map((g) => (
              <optgroup key={g.title} label={g.title}>
                {g.items.map((it, i) => (
                  <option key={`${it.id}:${i}`} value={it.id} disabled={it.gap}>
                    {it.gap ? "⚠ " : progress[it.id]?.cleared ? "✓ " : ""}
                    {it.label}
                  </option>
                ))}
              </optgroup>
            ))}
          </select>
          <DrillPanel key={skill} skill={skill} mode="session" />
        </>
      )}

      {tab === "exam" &&
        (exam ? (
          <ExamMix
            key={`${courseId}:${exam.name}`}
            title={`${exam.name} · ${exam.date}${exam.days >= 0 ? ` · ${exam.days} day${exam.days === 1 ? "" : "s"}` : ""}`}
            skills={exam.skills}
          />
        ) : (
          <div className="odd-hint">Pick a course with exam dates to get an exam mix.</div>
        ))}

      {tab === "courses" && (
        <div className="hub-courses">
          {courses.map((c) => {
            const lessons = (c.units ?? []).flatMap((u) => u.lessons);
            const gaps = lessons.filter((l) => !l.skills.some((s) => isLive(s))).length;
            const isBuilt = built.includes(c.id);
            return (
              <div key={c.id} className="hub-course-row">
                <div>
                  <b>{c.title}</b>
                  <div className="odd-hint">
                    {c.units!.length} units · {lessons.length} lessons · {gaps ? `${gaps} with no drills yet` : "every lesson has drills"}
                    {isBuilt ? " · in RemNote, updates itself" : ""}
                  </div>
                </div>
                <button className="odd-btn primary" disabled={!!busy} onClick={() => run(c.title, () => ensureCourse(plugin, c.id))}>
                  {busy === c.title ? "Building…" : isBuilt ? "Update now" : "Build in RemNote"}
                </button>
              </div>
            );
          })}
          <div className="hub-tools">
            <div className="odd-hint">Setup</div>
            <button className="odd-btn" disabled={!!busy} onClick={() => run("Drill cards", () => ensureDrillDeck(plugin, LEGACY_ROOT))}>
              {busy === "Drill cards" ? "Building…" : "Drill cards by subject + book contents"}
            </button>
            <button
              className="odd-btn"
              disabled={!!busy}
              onClick={() =>
                run("Organizing PDFs", async () => {
                  const log = await organizeLibrary(plugin);
                  await plugin.app.toast(log.length ? `Filed ${log.length} PDF${log.length > 1 ? "s" : ""}: ${log.join(" · ")}` : "No recognised PDFs to file.");
                })
              }
            >
              {busy === "Organizing PDFs" ? "Filing…" : "File textbook PDFs into subjects"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

renderWidget(Hub);
