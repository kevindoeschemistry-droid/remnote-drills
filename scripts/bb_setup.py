"""Create the Basketball drill skills, domain, library subject and source, and register the rules standard.
Idempotent. Usage: python3 scripts/bb_setup.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
q = lambda s: '"' + s + '"'
SK = [("bb.offense", "Offensive principles", "Spacing, advantage creation, drive-and-kick, screens, transition", []),
      ("bb.pnr-offense", "Ball-screen offense", "Screen types, set-up, reads against each coverage, screener actions", ["bb.offense"]),
      ("bb.defense", "Defensive principles", "Positioning, help and rotation, closeouts, rebounding, transition defence", []),
      ("bb.pnr-defense", "Ball-screen defence", "Coverages, what each concedes, routes and weak-side help", ["bb.defense"]),
      ("bb.zone-press", "Zone, man and press", "Zone shapes and weak spots, zone attack, press shapes and outlets", ["bb.defense"]),
      ("bb.situational", "Situational basketball", "Clock and score, fouling decisions, timeouts, out-of-bounds sets", ["bb.offense"]),
      ("bb.rules", "Rules and officiating", "Shot clock, violations, free throws, block/charge, mechanics", []),
      ("bb.analytics", "Analytics", "Possessions and ratings, shooting efficiency, four factors, shot value, samples", []),
      ("bb.scouting", "Scouting and film study", "Player and team keys, coverage identification, self-scouting", ["bb.defense"]),
      ("bb.development", "Practice design and development", "Levels, progression, drill design, cues, evaluation", [])]
p = os.path.join(ROOT, "drills/skills.yaml")
L = open(p).read().split("\n")
if not any("id: bb," in ln for ln in L):
    i = next(k for k, ln in enumerate(L) if "id: speak," in ln)
    L.insert(i + 1, '  - { id: bb, title: "Basketball" }')
if not any("id: bb.offense," in ln for ln in L):
    i = max(k for k, ln in enumerate(L) if "domain: speak," in ln)
    L[i + 1:i + 1] = [f'  - {{ id: {a}, domain: bb, title: {q(b)}, short: {q(c)}'
                      + (f', prereqs: [{", ".join(pr)}]' if pr else "") + " }" for a, b, c, pr in SK]
open(p, "w").write("\n".join(L))

p = os.path.join(ROOT, "drills/library.yaml")
L = open(p).read().split("\n")
if not any(ln.strip() == '- "Basketball"' for ln in L):
    i = next(k for k, ln in enumerate(L) if ln.strip() == '- "Speaking"')
    L.insert(i + 1, '  - "Basketball"')
if not any(ln.startswith("  bb:") for ln in L):
    i = next(k for k, ln in enumerate(L) if ln.startswith("  speak:"))
    L.insert(i + 1, '  bb: "Basketball"')
open(p, "w").write("\n".join(L))

p = os.path.join(ROOT, "drills/sources/usab-units.yaml")
if not os.path.exists(p):
    CH = [(1, "Offensive principles", "bb.offense"), (2, "Ball-screen offense", "bb.pnr-offense"),
          (3, "Defensive principles", "bb.defense"), (4, "Ball-screen defence", "bb.pnr-defense"),
          (5, "Zone, man and press", "bb.zone-press"), (6, "Situational basketball", "bb.situational"),
          (7, "Rules and officiating", "bb.rules"), (8, "Analytics", "bb.analytics"),
          (9, "Scouting and film study", "bb.scouting"), (10, "Practice design and player development", "bb.development")]
    out = ["# The Basketball framework's own units, written as a source so its skills have a home. This is not a book: the",
           "# USA Basketball player development curriculum is the framework's basis and the unit order is ours.",
           "id: usab-units", 'title: "Basketball framework units"', 'short: "Basketball units"',
           "year: 2026", "field: athletics", "chapters:"]
    out += [f'  - {{ n: {n}, title: {q(t)}, skills: [{s}] }}' for n, t, s in CH]
    open(p, "w").write("\n".join(out) + "\n")

STD = {"id": "ncaa-mbb-rules", "name": "NCAA Men's Basketball Rules (2025-26 rules book and the approved rules changes)",
       "publisher": "National Collegiate Athletic Association", "kind": "rulebook", "read": "part",
       "url": "https://ncaaorg.s3.amazonaws.com/championships/sports/basketball/rules/men/2025-26PRMBB_RulesChanges.pdf",
       "note": "The 2025-26 and 2026-27 rules-changes document and the rules book's table of contents were read in Nov 2026, together with the NCAA's own announcement of the 2025-26 changes (coach's challenge needing a timeout in hand, foul continuation, Flagrant 1 for groin contact giving two shots and the ball, one working shot clock permitted). The rules articles themselves were not read, so a card that needs a number prints it or names the level, and FIBA and NBA figures here are from general knowledge and need rechecking. As of the 2025-26 season NCAA men's is the only level above high school still using halves and a seven-foul one-and-one bonus.",
       "items": [{"code": "CH", "title": "Rules changes for 2025-26: coach's challenge, foul continuation, Flagrant 1, shot-clock operation"},
                 {"code": "TOC", "title": "Rules book structure: the articles on the clock, violations, fouls, penalties and officiating mechanics"}]}
p = os.path.join(ROOT, "drills/standards.yaml")
t = open(p).read()
if '"id": "ncaa-mbb-rules"' not in t:
    open(p, "w").write(t.rstrip("\n") + "\n- " + json.dumps(STD, ensure_ascii=False) + "\n")
p = os.path.join(ROOT, "drills/frameworks/basketball.yaml")
t = open(p).read()
t = t.replace("domains: []", "domains: [bb]")
if "ncaa-mbb-rules" not in t:
    t = t.replace("""basis:
  primary: usab-pdc
  note:""", """basis:
  primary: usab-pdc
  also: [ncaa-mbb-rules]
  note:""")
open(p, "w").write(t)
print("ok")
