// A course in RemNote:  Course (document) › Unit (document) › Lesson › skill group › drill cards.
// Practicing any level with RemNote's queue gives exactly that slice. Each course has its own
// cards (RemNote only queues cards inside a document), keyed "<course>|<skill>:<i>"; mastery
// streaks stay per skill, shared across courses.
import type { RNPlugin, RichTextInterface } from "@remnote/plugin-sdk";
import { BACK, bookLine, DRILL_POWERUP, DRILL_SLOT, ensureLine, findOrCreateChild, findOrCreateDocument, plain, rt, SOURCES_SLOT, videoLines } from "./deck";
import { anchorFor } from "./anchors";
import { COURSES, Course, placesFor, placeText, resolveSkill } from "./skills";

const COURSE_MAP_KEY = "drills.courseCardMap"; // "<course>|<skill>:<i>" -> remId

export const coursesWithUnits = (): Course[] => COURSES.filter((c) => c.units?.length);

export async function ensureCourse(plugin: RNPlugin, courseId: string, quiet = false) {
  const course = COURSES.find((c) => c.id === courseId);
  if (!course?.units?.length) return void (await plugin.app.toast(`Drills: no course ${courseId}`));
  const perSkill = Math.max(1, Math.min(10, (await plugin.settings.getSetting<number>("drill-cards-per-skill")) || 3));
  const map: Record<string, string> = (await plugin.storage.getSynced<Record<string, string>>(COURSE_MAP_KEY)) ?? {};
  const root = await findOrCreateDocument(plugin, course.title, undefined);
  if (!root) return void (await plugin.app.toast("Drills: could not create the course document"));

  // milestones at the top: "Final · 2026-12-08 · Units 1–6"
  let top = 0;
  for (const m of course.milestones ?? []) {
    const unitNums = m.units.map((u) => course.units!.findIndex((x) => x.id === u) + 1).filter((n) => n > 0);
    await ensureLine(plugin, root._id, [`🗓 ${m.name} · ${m.date} · Units ${unitNums.join(", ")}`] as RichTextInterface, top++);
  }

  const groups: Record<string, string> = {}; // skill -> its group in this course (first lesson that teaches it)
  let created = 0;
  for (let u = 0; u < course.units.length; u++) {
    const unit = course.units[u];
    const unitDoc = await findOrCreateChild(plugin, unit.title, root._id, top + u);
    if (!unitDoc) continue;
    if (!(await unitDoc.isDocument())) await unitDoc.setIsDocument(true);
    for (let l = 0; l < unit.lessons.length; l++) {
      const lesson = unit.lessons[l];
      const lessonRem = await findOrCreateChild(plugin, lessonTitle(lesson.ref, lesson.title), unitDoc._id, l);
      if (!lessonRem) continue;
      let pos = 0;
      // the book: anchor (📖) and videos for the lesson's first skill in this course's textbook
      const place = lesson.skills
        .flatMap((s) => placesFor(s))
        .find((p) => course.sources.includes(p.source.id));
      if (place) {
        if (await bookLine(plugin, lessonRem._id, await anchorFor(plugin, place))) pos++;
        pos += await videoLines(plugin, lessonRem._id, place.section?.videos ?? place.chapter.videos, pos);
      }
      if (!lesson.skills.length) {
        await ensureLine(plugin, lessonRem._id, ["⚠ No drills yet for this section"] as RichTextInterface, pos++);
        continue;
      }
      for (const sid of lesson.skills) {
        const skill = resolveSkill(sid);
        if (!skill) continue;
        if (groups[skill.id]) {
          // taught again later in the course: link back instead of duplicating cards
          await ensureLine(plugin, lessonRem._id, ["↺ ", { i: "q", _id: groups[skill.id] }] as RichTextInterface, pos++);
          continue;
        }
        const group = await findOrCreateChild(plugin, skill.title, lessonRem._id, pos++);
        if (!group) continue;
        groups[skill.id] = group._id;
        const sourcesText = placesFor(skill.id).filter((p) => course.sources.includes(p.source.id)).map(placeText).join("; ") || "—";
        for (let i = 1; i <= perSkill; i++) {
          const key = `${course.id}|${skill.id}:${i}`;
          let rem = map[key] ? await plugin.rem.findOne(map[key]) : undefined;
          if (!rem) {
            rem = await plugin.rem.createRem();
            if (!rem) continue;
            await rem.setText(await rt(plugin, `Drill · ${skill.title} (${i})`));
            await rem.setBackText(await rt(plugin, BACK));
            await plugin.rem.moveRems([rem], group, i - 1);
            map[key] = rem._id;
            created++;
          }
          if (!(await rem.hasPowerup(DRILL_POWERUP))) await rem.addPowerup(DRILL_POWERUP);
          if ((await rem.getPowerupProperty(DRILL_POWERUP, DRILL_SLOT))?.trim() !== skill.id)
            await rem.setPowerupProperty(DRILL_POWERUP, DRILL_SLOT, [skill.id]);
          if ((await rem.getPowerupProperty(DRILL_POWERUP, SOURCES_SLOT))?.trim() !== sourcesText)
            await rem.setPowerupProperty(DRILL_POWERUP, SOURCES_SLOT, [sourcesText]);
        }
      }
      // a lesson that just got drills drops its "no drills yet" line
      for (const c of await lessonRem.getChildrenRem()) if (plain(c.text).startsWith("⚠ No drills yet") && lesson.skills.length) await c.remove();
    }
  }
  await plugin.storage.setSynced(COURSE_MAP_KEY, map);
  if (!quiet || created)
    await plugin.app.toast(created ? `${course.title}: ${created} drill cards created` : `${course.title} is up to date`);
}

const lessonTitle = (ref: string, title: string) => (/^\d/.test(ref) ? `§${ref} ${title}` : title);
