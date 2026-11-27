#!/usr/bin/env python3
"""Put Swimming on a coach-education curriculum instead of the rulebook alone.

The framework's own note said it: the World Aquatics rules say what is legal, not what to learn in what order. Two
published curricula do say that:

  usas-foc-2007       USA Swimming's Foundations of Coaching (2007), the course every new coach member took. Its
                      table of contents was read in full and chapters 5 (Skills and Mechanics) and 6 (Physical
                      Conditioning) were read through an extraction of each PDF; chapters 1-4 and 7 by title only,
                      and the energy-zone charts' values were not in the text read, so read is 'part'.
  asca-certification  The ASCA schools. Only the session outlines of Levels 1-3 were read, from a course provider's
                      published outline, so read is 'part' and items are session titles in our words.

Idempotent; text edits only (standards.yaml and the framework carry comments and one-line entries a YAML dump
would destroy).
"""
import json, pathlib, re, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
ST = ROOT / "drills" / "standards.yaml"
SK = ROOT / "drills" / "skills.yaml"
FW = ROOT / "drills" / "frameworks" / "swimming.yaml"
SRC = ROOT / "drills" / "sources" / "usas-foundations-of-coaching.yaml"

FOC = {
    "id": "usas-foc-2007",
    "name": "USA Swimming Foundations of Coaching (2007)",
    "publisher": "USA Swimming",
    "kind": "course",
    "read": "part",
    "url": "https://www.gomotionapp.com/efsl/UserFiles/Image/QuickUpload/table-of-contents_000606.pdf",
    "note": ("Read Nov 2026 from copies a member club hosts: the whole table of contents, and chapters 5 (Skills "
             "and Mechanics) and 6 (Physical Conditioning) through an extraction of each PDF. Chapters 1-4 and 7 "
             "were read by title only, and the 4- and 7-zone energy charts' values were not in the text read, so "
             "no card states a zone's heart rate or pace from this source. USA Swimming replaced the course in "
             "2022-23 with its Coaching Certification Program, whose content sits behind member sign-in; this "
             "2007 edition is the last one openly readable. Items are chapter parts, titled in our words."),
    "items": [
        {"code": "1", "title": "Philosophy and ethics (title only)"},
        {"code": "2", "title": "Teaching and communication: learning environment, teaching methods, motivation, goal setting (title only)"},
        {"code": "3", "title": "Organisation and administration: the club, the meet, risk management (title only)"},
        {"code": "4", "title": "Growth and development of young athletes (title only)"},
        {"code": "5.1", "title": "Basic biomechanics: three resistances, reducing them, propulsion, stroke count and stroke rate"},
        {"code": "5.2", "title": "Freestyle: essential skills and teaching progression"},
        {"code": "5.3", "title": "Backstroke: essential skills and teaching progression"},
        {"code": "5.4", "title": "Breaststroke: essential skills and teaching progression"},
        {"code": "5.5", "title": "Butterfly: essential skills and teaching progression"},
        {"code": "5.6", "title": "Starts: forward, backstroke and relay starts, progressions and safety"},
        {"code": "5.7", "title": "Turns: push-offs, flip and open turns, pull-out and breakout"},
        {"code": "6.1", "title": "Basic physiology: the three metabolic pathways, continuous and interval training, DIRT"},
        {"code": "6.2", "title": "Season planning: macro-, meso- and microcycles, taper, principles of training"},
        {"code": "6.3", "title": "Energy zones (chart values not read)"},
        {"code": "6.4", "title": "Planning novice and age-group practices"},
        {"code": "6.5", "title": "Planning senior practices"},
        {"code": "6.6", "title": "Fueling, hydration and drug-free sport"},
        {"code": "7", "title": "Evaluation of athletes, coaches and the club (title only)"},
    ],
}

ASCA_LINE_OLD = '- { id: asca-certification, name: "ASCA coach certification curriculum", publisher: American Swimming Coaches Association, kind: standard, read: none }'
ASCA = {
    "id": "asca-certification",
    "name": "ASCA coach certification schools, Levels 1-3 (session outlines)",
    "publisher": "American Swimming Coaches Association",
    "kind": "course",
    "read": "part",
    "url": "https://www.swimmingcoach.org/certifications-education/certification/",
    "note": ("Read Nov 2026: only the session outlines of the Level 1 (Foundations of Coaching), Level 2 (Stroke "
             "School) and Level 3 (Physiology School) courses, from a course provider's published outline. The "
             "course content itself is paid and was not read. Items are the schools, titled in our words."),
    "items": [
        {"code": "L1", "title": "Level 1, Foundations of Coaching: the coach's role, communication, teaching, motivation, safety, basic biomechanics and physiology, a beginner workout"},
        {"code": "L2", "title": "Level 2, Stroke School: biomechanics, the four strokes, starts, turns and finishes"},
        {"code": "L3", "title": "Level 3, Physiology School: principles of training, energy metabolism, nutrition, macro-, meso- and microcycles, writing and running practices, dryland"},
    ],
}

SKILLS = [
    ("swim.hydro", "Hydrodynamics: resistance, streamline and propulsion", "Swim hydrodynamics"),
    ("swim.technique", "Stroke technique: phases, timing and fault diagnosis", "Stroke technique"),
    ("swim.walls", "Starts, turns, underwaters and breakouts", "Starts and turns"),
    ("swim.physiology", "Energy systems, thresholds and adaptation", "Swim physiology"),
    ("swim.video", "Video analysis and before/after testing", "Video analysis"),
    ("swim.practice", "Practice design: sessions, sets, send-offs and drills", "Practice design"),
    ("swim.coaching", "Coaching others: progressions, cues and group management", "Coaching swimmers"),
]

SOURCE = """# USA Swimming's Foundations of Coaching (2007), as the chapters the newer swim.* skills map to. Chapters 5 and 6
# were read (see drills/standards.yaml, usas-foc-2007); the video-analysis row has no chapter of its own in the
# course and names the quantity, as the pacing rows of the rulebook source do.
id: usas-foundations-of-coaching
title: "USA Swimming Foundations of Coaching"
short: "Foundations of Coaching"
year: 2007
field: swimming
chapters:
  - { n: 2, title: "Teaching and communication", skills: [swim.coaching] }
  - { n: 5, title: "Skills and mechanics: biomechanics", skills: [swim.hydro] }
  - { n: 5, title: "Skills and mechanics: the four strokes", skills: [swim.technique] }
  - { n: 5, title: "Skills and mechanics: starts and turns", skills: [swim.walls] }
  - { n: 6, title: "Physical conditioning: physiology and energy zones", skills: [swim.physiology] }
  - { n: 6, title: "Physical conditioning: planning practices", skills: [swim.practice] }
  - { n: 7, title: "Evaluation: measuring stroke count, rate and change", skills: [swim.video] }
"""

# unit -> citations added to every objective of that unit that has no std yet
UNIT_STD = {
    1: ["usas-foc-2007:5.1", "asca-certification:L2"],
    2: ["usas-foc-2007:5.2", "usas-foc-2007:5.3", "asca-certification:L2"],
    3: ["usas-foc-2007:5.5", "asca-certification:L2"],
    4: ["usas-foc-2007:5.4", "asca-certification:L2"],
    5: ["usas-foc-2007:5.6", "usas-foc-2007:5.7", "asca-certification:L2"],
    8: ["usas-foc-2007:6.1", "usas-foc-2007:6.3", "asca-certification:L3"],
    9: ["usas-foc-2007:6.2", "asca-certification:L3"],
    10: ["usas-foc-2007:7"],
    11: ["usas-foc-2007:6.4", "usas-foc-2007:6.5", "asca-certification:L3"],
    12: ["usas-foc-2007:2", "usas-foc-2007:4", "asca-certification:L1"],
}


def main():
    t = ST.read_text()
    if '"id": "usas-foc-2007"' not in t:
        t = t.rstrip("\n") + "\n- " + json.dumps(FOC, ensure_ascii=False) + "\n"
        print("  added usas-foc-2007")
    if ASCA_LINE_OLD in t:
        t = t.replace(ASCA_LINE_OLD, "- " + json.dumps(ASCA, ensure_ascii=False))
        print("  asca-certification: read none -> part, 3 items")
    ST.write_text(t)
    ids = {s["id"]: s for s in yaml.safe_load(ST.read_text())}
    assert ids["usas-foc-2007"]["read"] == "part" and len(ids["asca-certification"].get("items", [])) == 3

    t = SK.read_text()
    if "id: swim.hydro" not in t:
        t = t.rstrip("\n") + "\n" + "".join(
            f'  - {{ id: {i}, domain: swim, title: "{ti}", short: "{sh}" }}\n' for i, ti, sh in SKILLS)
        SK.write_text(t)
        print(f"  skills: {len(SKILLS)} swim.* skills")
    if not SRC.exists():
        SRC.write_text(SOURCE)
        print(f"  source: {SRC.name}")

    t = FW.read_text()
    old = "basis:\n  primary: world-aquatics-rules\n  wanted: [asca-certification]\n"
    if old in t:
        i = t.index(old)
        j = t.index("\n", t.index("  note:", i)) + 1
        t = t[:i] + ("basis:\n  primary: world-aquatics-rules\n  also: [usas-foc-2007, asca-certification]\n"
                     "  note: \"The World Aquatics rules (read in full) say what is legal. What to learn, and in what order, "
                     "now rests on USA Swimming's Foundations of Coaching (2007; chapters 5 and 6 read, the rest by title) "
                     "and the ASCA Level 1-3 school outlines (titles only). Research papers named in an objective's own "
                     "essential knowledge are its source for that claim. Unit order is ours.\"\n") + t[j:]
        print("  swimming basis: also usas-foc-2007, asca-certification")
    out, unit, n = [], None, 0
    for line in t.split("\n"):
        m = re.match(r"^    n: (\d+)", line)
        if m:
            unit = int(m.group(1))
        m = re.match(r"^(          - \{ id: [A-Z]+, )(.*)$", line)
        if m and unit in UNIT_STD and "std:" not in line:
            line = m.group(1) + "std: [" + ", ".join(f'"{s}"' for s in UNIT_STD[unit]) + "], " + m.group(2)
            n += 1
        out.append(line)
    FW.write_text("\n".join(out))
    assert yaml.safe_load(FW.read_text())["basis"]["also"] == ["usas-foc-2007", "asca-certification"]
    print(f"  cited on {n} objectives")


if __name__ == "__main__":
    main()
