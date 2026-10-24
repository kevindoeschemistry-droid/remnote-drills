// The drill graph (drills/*.yaml, compiled to JSON at build time).
//
//   skills   — what can be drilled (book-agnostic; cards + streaks hang off these)
//   sources  — textbooks: chapters/sections and the skills each one teaches
//   courses  — which sources a course uses
import graph from "./skills.generated.json";

export interface Domain {
  id: string;
  title: string;
}

export interface Skill {
  id: string;
  domain: string;
  title: string;
  short: string;
  kind: "solve" | "classify";
  status: "live" | "planned";
  aliases: string[];
  prereqs: string[];
  levels: Record<number, string[]>;
  pool?: string[];
  /** "Method" notes: one line each, $…$ math */
  method?: string[];
}

export interface Section {
  ref: string;
  title: string;
  skills: string[];
  wiki?: string;
  pages?: [number, number];
  videos?: Video[];
}

/** A lecture or screencast that teaches this section (opened in the browser). */
export interface Video {
  title: string;
  url: string;
}

export interface Chapter {
  n: number;
  title: string;
  skills: string[];
  sections: Section[];
  wiki?: string;
  pages?: [number, number];
  videos?: Video[];
}

export interface Source {
  id: string;
  title: string;
  short: string;
  edition?: number;
  year?: number;
  field?: string;
  wiki?: string;
  conventions?: Record<string, string>;
  chapters: Chapter[];
}

export interface Course {
  id: string;
  title: string;
  sources: string[];
}

export const DOMAINS: Domain[] = (graph as any).domains;
export const ALL_SKILLS: Skill[] = (graph as any).skills;
export const LIVE_SKILLS: Skill[] = ALL_SKILLS.filter((s) => s.status === "live");
export const SOURCES: Source[] = (graph as any).sources;
export const COURSES: Course[] = (graph as any).courses;

export const WIKI_BASE = "https://wiki.kevindoeschemistry.com/";

const byName = new Map<string, Skill>();
for (const s of ALL_SKILLS) {
  byName.set(s.id, s);
  for (const a of s.aliases) byName.set(a, s);
}

/** Look up a skill by id or by an old alias ("separable", "krey-ch01-separable" -> ode1.separable). */
export function resolveSkill(name: string | undefined | null): Skill | undefined {
  return name ? byName.get(name.trim()) : undefined;
}

export function isLive(name: string | undefined | null): boolean {
  return resolveSkill(name)?.status === "live";
}

/** Live skills grouped by domain, in graph order. */
export function liveByDomain(): { domain: Domain; skills: Skill[] }[] {
  return DOMAINS.map((domain) => ({ domain, skills: LIVE_SKILLS.filter((s) => s.domain === domain.id) })).filter(
    (g) => g.skills.length
  );
}

export function templatesFor(skill: Skill, level = 1): string[] {
  const levels = Object.keys(skill.levels).map(Number).sort((a, b) => a - b);
  const pick = levels.filter((l) => l <= level).pop() ?? levels[0];
  return skill.levels[pick] ?? [];
}

export const sourceById = (id: string) => SOURCES.find((s) => s.id === id);
export const sourceLabel = (s: Source) => `${s.short}${s.edition && s.edition > 1 ? ` ${s.edition}e` : ""}`;

/** Every place a skill is taught: section-level first, chapter-level if the chapter maps it directly. */
export interface Place {
  source: Source;
  chapter: Chapter;
  section?: Section;
  ref: string; // "§1.3" or "Ch 7"
  wiki?: string;
}

/** Videos for a place: its section's, else its chapter's. */
export const videosFor = (p: Place | undefined): Video[] => (p ? p.section?.videos ?? p.chapter.videos ?? [] : []);

export function placesFor(skillId: string): Place[] {
  const out: Place[] = [];
  for (const source of SOURCES)
    for (const chapter of source.chapters) {
      for (const section of chapter.sections)
        if (section.skills.includes(skillId))
          out.push({ source, chapter, section, ref: `§${section.ref}`, wiki: section.wiki ?? chapter.wiki ?? source.wiki });
      if (chapter.skills.includes(skillId))
        out.push({ source, chapter, ref: `Ch ${chapter.n}`, wiki: chapter.wiki ?? source.wiki });
    }
  return out;
}

/** The place to show on a card: the preferred source if it teaches the skill, else the first. */
export function primaryPlace(skillId: string, preferredSource?: string): Place | undefined {
  const all = placesFor(skillId);
  return all.find((p) => p.source.id === preferredSource) ?? all[0];
}

export const placeText = (p: Place) => `${sourceLabel(p.source)} ${p.ref}`;
