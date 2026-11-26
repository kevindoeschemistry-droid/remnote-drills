"""Create the Speaking drill skills, their domain, the library subject and a source file. Idempotent.
Usage: python3 scripts/speak_skills.py"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
q = lambda s: '"' + s + '"'
SK = [("speak.voice", "Breath, voice and diction", "Breath support, volume, articulation and writing for the ear", []),
      ("speak.pace", "Pace, pauses and fillers", "Words per minute, deliberate pauses, filler rates and how to cut them", ["speak.voice"]),
      ("speak.presence", "Vocal variety and presence", "Intonation, stress, eye contact, stance and cutting hedges", ["speak.pace"]),
      ("speak.structure", "Structure", "Answer first, PREP and SCQA, signposting and endings", ["speak.pace"]),
      ("speak.impromptu", "Impromptu speaking", "Table topics, question handling, STAR answers and introductions", ["speak.structure"]),
      ("speak.explain", "Explaining technical ideas", "Audience modelling, concrete to abstract, analogies, checks, numbers and figures", ["speak.structure"]),
      ("speak.persuade", "Persuasion and storytelling", "Motivated sequence, objections, the ask, and story shape", ["speak.structure"]),
      ("speak.listen", "Listening and conversation", "Paraphrase, follow-ups, short contributions and disagreeing well", ["speak.presence"]),
      ("speak.review", "Feedback and self-review", "Measuring a recording, competency scoring, targets and evaluations", ["speak.pace"]),
      ("speak.longform", "Long-form talks", "Segmenting a lecture, keyword outlines and fitting a time slot", ["speak.structure"]),
      ("speak.mediated", "Remote and recorded speaking", "Camera and microphone setup, and handling lag", ["speak.presence"])]
p = os.path.join(ROOT, "drills/skills.yaml")
L = open(p).read().split("\n")
if not any("id: speak," in ln for ln in L):
    i = next(k for k, ln in enumerate(L) if "id: is," in ln)
    L.insert(i + 1, '  - { id: speak, title: "Speaking" }')
if not any("id: speak.voice," in ln for ln in L):
    i = max(k for k, ln in enumerate(L) if "domain: is," in ln)
    L[i + 1:i + 1] = [f'  - {{ id: {a}, domain: speak, title: {q(b)}, short: {q(c)}'
                      + (f', prereqs: [{", ".join(pr)}]' if pr else "") + " }" for a, b, c, pr in SK]
open(p, "w").write("\n".join(L))

p = os.path.join(ROOT, "drills/library.yaml")
L = open(p).read().split("\n")
if not any(ln.strip() == '- "Speaking"' for ln in L):
    i = next(k for k, ln in enumerate(L) if ln.strip() == '- "Information Systems"')
    L.insert(i + 1, '  - "Speaking"')
if not any(ln.startswith("  speak:") for ln in L):
    i = next(k for k, ln in enumerate(L) if ln.startswith("  is:"))
    L.insert(i + 1, '  speak: "Speaking"')
open(p, "w").write("\n".join(L))

p = os.path.join(ROOT, "drills/sources/speaking-units.yaml")
if not os.path.exists(p):
    CH = [(1, "Breath, voice and diction", "speak.voice"), (2, "Pace, pauses and filler words", "speak.pace"),
          (3, "Vocal variety and presence", "speak.presence"), (4, "Structure", "speak.structure"),
          (5, "Impromptu speaking", "speak.impromptu"), (6, "Explaining technical ideas", "speak.explain"),
          (7, "Persuasion and storytelling", "speak.persuade"), (8, "Listening and conversation", "speak.listen"),
          (9, "Feedback and self-review", "speak.review"), (10, "Lecturing and long-form talks", "speak.longform"),
          (11, "Remote, recorded and microphone speaking", "speak.mediated")]
    out = ["# The Speaking framework's own units, written as a source so its skills have a home. This is not a book: the",
           "# NCA Competent Speaker scoring rubric and the Toastmasters competency list are the framework's basis, and the",
           "# unit order is ours. No textbook was read for these.",
           "id: speaking-units", 'title: "Speaking and Articulation units"', 'short: "Speaking units"',
           "year: 2026", "field: communication", "chapters:"]
    out += [f'  - {{ n: {n}, title: {q(t)}, skills: [{s}] }}' for n, t, s in CH]
    open(p, "w").write("\n".join(out) + "\n")
print("ok")
