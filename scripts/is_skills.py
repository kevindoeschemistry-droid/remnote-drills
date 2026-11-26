"""Create the Information Systems drill skills, their domain, the library subject and a source file, so the IS
framework's objectives can carry drills. Idempotent. Usage: python3 scripts/is_skills.py"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
q = lambda s: '"' + s + '"'
SK = [("is.strategy", "IS strategy and governance", "Strategic role, investment appraisal, decision rights and frameworks", []),
      ("is.architecture", "Enterprise architecture", "Domains and method, application portfolio, integration styles, cloud migration", ["is.strategy"]),
      ("is.development", "Systems analysis and delivery", "Process and requirements modelling, scheduling, earned value, deployment", ["is.strategy"]),
      ("is.data", "Data and analytics management", "Data quality and stewardship, star schemas, ingestion, analytics for decisions", ["is.architecture"]),
      ("is.infrastructure", "Infrastructure and service operations", "Sizing and sourcing, service management, SLAs, vendor selection", ["is.architecture"]),
      ("is.assurance", "Risk, continuity and assurance", "Risk scoring and treatment, ALE and ROSI, RTO and RPO, controls and audit", ["is.infrastructure"]),
      ("is.innovation", "Innovation and digital business", "Adoption models, change models, diffusion, business models, unit economics", ["is.strategy"]),
      ("is.ethics", "Ethics, privacy and sustainability", "Which regime applies, impact assessments, ethical reasoning, lifetime carbon", ["is.data"])]
p = os.path.join(ROOT, "drills/skills.yaml")
L = open(p).read().split("\n")
if not any("id: is," in ln for ln in L):
    i = next(k for k, ln in enumerate(L) if "id: qchem," in ln)
    L.insert(i + 1, '  - { id: is, title: "Information systems" }')
if not any("id: is.strategy," in ln for ln in L):
    i = max(k for k, ln in enumerate(L) if "domain: qchem," in ln)
    L[i + 1:i + 1] = [f'  - {{ id: {a}, domain: is, title: {q(b)}, short: {q(c)}'
                      + (f', prereqs: [{", ".join(pr)}]' if pr else "") + " }" for a, b, c, pr in SK]
open(p, "w").write("\n".join(L))

p = os.path.join(ROOT, "drills/library.yaml")
L = open(p).read().split("\n")
if not any(ln.strip() == '- "Information Systems"' for ln in L):
    i = next(k for k, ln in enumerate(L) if ln.strip() == '- "Electronic Structure"')
    L.insert(i + 1, '  - "Information Systems"')
if not any(ln.startswith("  is:") for ln in L):
    i = next(k for k, ln in enumerate(L) if ln.startswith("  qchem:"))
    L.insert(i + 1, '  is: "Information Systems"')
open(p, "w").write("\n".join(L))

p = os.path.join(ROOT, "drills/sources/msis-areas.yaml")
if not os.path.exists(p):
    CH = [(1, "IS strategy, governance and investment", "is.strategy"),
          (2, "Enterprise architecture and integration", "is.architecture"),
          (3, "Systems analysis, development and project delivery", "is.development"),
          (4, "Data, information and analytics management", "is.data"),
          (5, "IT infrastructure and service operations", "is.infrastructure"),
          (6, "Business continuity, risk and information assurance", "is.assurance"),
          (7, "Innovation, change and digital business models", "is.innovation"),
          (8, "Ethics, impacts and sustainability", "is.ethics")]
    out = ["# The competency areas of the MSIS 2016 graduate curriculum model, written as a source so the is.* skills have a",
           "# home. This is not a book: the curriculum model itself is the framework's basis, and these \"chapters\" are the",
           "# areas its units follow. No textbook was read for these.",
           "id: msis-areas", 'title: "MSIS 2016 competency areas"', 'short: "MSIS areas"',
           "year: 2016", "field: information systems", "chapters:"]
    out += [f'  - {{ n: {n}, title: {q(t)}, skills: [{s}] }}' for n, t, s in CH]
    open(p, "w").write("\n".join(out) + "\n")
print("ok")
