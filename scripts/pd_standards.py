"""Register the NSPE Code of Ethics and the OSHA process-safety-management regulation, add them to the Process Design
basis, and add the three big ideas its new units need. Idempotent. Usage: python3 scripts/pd_standards.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CANONS = [("C1", "Hold the public's safety, health and welfare paramount"),
          ("C2", "Work only in areas of competence"),
          ("C3", "Make public statements objectively and truthfully"),
          ("C4", "Act as a faithful agent or trustee for each employer and client"),
          ("C5", "Avoid deceptive acts"),
          ("C6", "Conduct oneself honourably, lawfully and so as to serve the profession")]
RULES = [("R1", "Rules of practice: public safety — escalate an overridden judgment, approve only conforming documents, keep information confidential, refuse fraudulent ventures, do not aid unlicensed practice, report violations"),
         ("R2", "Rules of practice: competence — accept and seal only work one is qualified for, and only one's own technical segments"),
         ("R3", "Rules of practice: objective statements — complete and honest reports, opinions grounded in fact and expertise, interested parties disclosed"),
         ("R4", "Rules of practice: faithful agency — disclose conflicts of interest, no double compensation without consent, no improper payments, recuse from decisions involving one's own firm"),
         ("R5", "Rules of practice: avoiding deception — no misstated qualifications or responsibility, no improper inducements to win work")]
OBLIG = [("O1", "Professional obligations: integrity — admit errors, warn of likely failure, disclose outside work, treat all fairly"),
         ("O2", "Professional obligations: the public interest — civic involvement, public education, sustainability, continuing development, never seal non-conforming plans"),
         ("O3", "Professional obligations: no public deception — no material misstatement or omission, no false authorship"),
         ("O4", "Professional obligations: confidentiality — client and employer information, and not exploiting project knowledge without consent"),
         ("O5", "Professional obligations: independence — gifts and commissions must not influence a professional decision"),
         ("O6", "Professional obligations: fair competition — no unfair criticism of peers, no compromising contingency arrangements, limits on outside work"),
         ("O7", "Professional obligations: respect for peers — no malicious harm to reputation, report misconduct, review limits in private practice"),
         ("O8", "Professional obligations: accountability — personal responsibility for one's work, registration laws, no concealment behind an entity"),
         ("O9", "Professional obligations: credit and ownership — credit those responsible, respect client-owned designs, settle intellectual-property ownership in advance")]
PSM = [("b", "Application and definitions: which processes are covered"),
       ("c", "Employee participation"), ("d", "Process safety information"),
       ("e", "Process hazard analysis, and the methodologies it may use"),
       ("f", "Operating procedures"), ("g", "Training"), ("h", "Contractors"),
       ("i", "Pre-startup safety review"), ("j", "Mechanical integrity"),
       ("k", "Hot work permit"), ("l", "Management of change"), ("m", "Incident investigation"),
       ("n", "Emergency planning and response"), ("o", "Compliance audits"), ("p", "Trade secrets")]
STDS = [
 {"id": "nspe-ethics", "name": "NSPE Code of Ethics for Engineers (as revised July 2019)",
  "publisher": "National Society of Professional Engineers", "kind": "standard", "read": "full",
  "url": "https://www.nspe.org/career-growth/nspe-code-ethics-engineers",
  "note": "The whole structure read in Nov 2026 from NSPE's own page: six Fundamental Canons, five Rules of Practice, nine Professional Obligations. The Code is NSPE's copyright, so every item title here is our own paraphrase and no card reproduces its wording; cards state the situation and ask which duty governs. The Board of Ethical Review case opinions were not read.",
  "items": [{"code": c, "title": t} for c, t in CANONS + RULES + OBLIG]},
 {"id": "osha-psm", "name": "29 CFR 1910.119, Process safety management of highly hazardous chemicals",
  "publisher": "US Occupational Safety and Health Administration", "kind": "standard", "read": "part",
  "url": "https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119",
  "note": "Paragraph titles (b) to (p) read in Nov 2026, together with the process-hazard-analysis methodology list. The full regulatory text, Appendix A's chemical list and the threshold quantities were not read, so a card that needs a threshold prints it. Items are the paragraph titles, paraphrased.",
  "items": [{"code": c, "title": t} for c, t in PSM]},
]
p = os.path.join(ROOT, "drills/standards.yaml")
t = open(p).read()
for s in STDS:
    if f'"id": "{s["id"]}"' not in t:
        t = t.rstrip("\n") + "\n- " + json.dumps(s, ensure_ascii=False) + "\n"
open(p, "w").write(t)

p = os.path.join(ROOT, "drills/frameworks/process-design.yaml")
t = open(p).read()
if "nspe-ethics" not in t:
    t = t.replace("  also: [pe-chemical]\n", "  also: [pe-chemical, nspe-ethics, osha-psm, turton-5e]\n")
    t = t.replace(
        '  note: "Topics from FE Chemical areas 13, 15, 16 and PE Chemical area 7 (read in full); objectives and their order are ours."',
        '  note: "Topics from FE Chemical areas 11, 13, 14, 15, 16 and 17 and PE Chemical area 7 (read in full); objectives and their order are ours. The professional-practice unit rests on the NSPE Code of Ethics (read in full) and the safety-management unit on 29 CFR 1910.119 (paragraph titles read). Particle technology has no published curriculum of its own, so that unit is a house list on the FE spec items."')
if "id: SOLIDS" not in t:
    t = t.replace("""  - id: DYN
    title: Processes respond with a lag""", """  - id: SOLIDS
    title: A powder is not a fluid
    text: A solid stream is described by a distribution, not a single size, and it flows, grinds and dissolves by its own rules.
  - id: DOCS
    title: A plant is built from documents
    text: What a drawing shows, and what accuracy an estimate claims, decide what can be built and what it will cost.
  - id: DUTY
    title: The duty is to the public first
    text: An engineer's obligations are ordered, and the public's safety outranks the client, the employer and the engineer.
  - id: DYN
    title: Processes respond with a lag""")
# the header's "not here yet" list shrinks
t = t.replace("# Not here yet: equipment sizing and selection, P&IDs, second-order and dead-time dynamics, PID tuning, relief sizing, dispersion modelling, environmental regulation.",
              "# Units 4-9 (Nov 2026) close most of what this header used to list as missing: particle technology, plant\n# documents and estimate classes, relief sizing and loss prevention, professional practice, measurement and\n# uncertainty, and statistics in engineering units. Still not here: second-order and dead-time dynamics, PID\n# tuning, and quantitative dispersion modelling.")
open(p, "w").write(t)
print("ok")
