"""DAT Reading Comprehension at test length (DAT-5.3.A): one passage of several paragraphs with ten questions, to be
worked against a 20-minute clock. Passages and questions are original, written for this Library. Each passage is one
case; question k's options are case fields qk_a (right) … qk_d, so the choice is shuffled per problem.
Writes drills/problems/dat-rc-long.yaml."""
import os
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P1 = """Saliva, the Overlooked Defender

(1) Saliva rarely gets credit for anything. Patients notice it only when there is too much of it during a dental procedure or too little of it on a dry, anxious morning. Yet the roughly half to one and a half litres that the salivary glands secrete each day do more to protect the teeth than any single product sold to clean them. Saliva is not merely water: it is a dilute, carefully regulated solution of ions, proteins and enzymes, and almost every one of its components has a job.

(2) The first job is mechanical. Saliva lubricates the mouth, coats food so that it can be swallowed, and washes sugars and acids away from the teeth. Researchers describe this as salivary clearance, and it can be measured: after a sugary rinse, the sugar concentration in the mouth falls over the following minutes at a rate set largely by how fast saliva flows. A person with a brisk flow clears the sugar quickly; a person with a slow flow keeps it bathing the teeth far longer.

(3) The second job is chemical. When bacteria in dental plaque ferment sugar, they release acids that lower the pH at the tooth surface. Enamel, which is mostly a calcium phosphate mineral, begins to dissolve once the pH falls below a critical value, usually placed near 5.5. Saliva resists this fall. Its bicarbonate acts as a buffer, and the concentration of bicarbonate rises steeply when flow is stimulated, by chewing for example. Saliva is also supersaturated with calcium and phosphate, so that once the pH recovers, minerals can return to the enamel surface. A tooth is therefore not a static object but the site of a daily contest between loss and repair, and saliva is the referee.

(4) The third job belongs to the proteins. Some, such as statherin, keep calcium phosphate dissolved in saliva so that it does not precipitate prematurely as tartar. Others bind to the clean enamel within minutes of brushing and form a thin film, the acquired pellicle, which both protects the surface and serves as the first foothold for bacteria. Still others, including lysozyme and lactoferrin, restrain the growth of microbes directly. The same saliva that feeds the first colonizers of the tooth also limits how far they can spread.

(5) The value of all this becomes obvious when saliva fails. Hundreds of commonly prescribed medicines, radiation therapy to the head and neck, and certain autoimmune diseases reduce salivary flow. Patients with severe dry mouth can develop decay at unusual sites, such as the necks of the teeth near the gums and even the tips of the lower front teeth, places that are normally well protected. Their dentures may fit poorly and their mouths may burn. Saliva substitutes help with comfort, but none reproduces the full set of functions of natural saliva, and most clinicians treat them as a supplement rather than a replacement.

(6) For this reason some researchers argue that saliva deserves a more central place in prevention. Measuring flow and buffering capacity takes only a few minutes and costs little, yet it is seldom done in routine care. Chewing sugar-free gum after meals, which stimulates flow and raises bicarbonate, has modest but consistent support in the research literature. None of this replaces fluoride or brushing; rather, it acknowledges that the mouth already contains a sophisticated protective system, and that much of good dental care consists of not getting in its way."""

Q1 = [
    ("What is the main idea of the passage?", "Saliva protects teeth through several mechanical, chemical and biological functions that deserve more attention", "Saliva substitutes are as effective as natural saliva", "Dental plaque cannot be controlled without fluoride", "Statherin is the most important protein in the mouth"),
    ("According to paragraph 2, what mainly sets how quickly sugar is cleared from the mouth?", "The rate of salivary flow", "The amount of fluoride in toothpaste", "The thickness of the acquired pellicle", "The number of bacteria in plaque"),
    ("At roughly what pH does the passage say enamel begins to dissolve?", "About 5.5", "About 7.0", "About 3.0", "About 8.5"),
    ("As used in paragraph 3, the word 'referee' suggests that saliva", "governs the balance between mineral loss and repair", "prevents all bacteria from reaching the tooth", "decides which foods a person eats", "replaces lost enamel completely"),
    ("Which function does the passage attribute to statherin?", "Keeping calcium phosphate dissolved so that it does not precipitate too early", "Killing bacteria directly", "Buffering acid with bicarbonate", "Lubricating food for swallowing"),
    ("Why does the author say the pellicle is a mixed blessing?", "It protects the enamel but also gives bacteria their first foothold", "It dissolves enamel and also feeds bacteria", "It is removed by brushing and cannot re-form", "It blocks fluoride and saliva alike"),
    ("Decay on the tips of the lower front teeth is mentioned as evidence that", "dry mouth removes protection from normally well-protected sites", "children brush those teeth poorly", "lower teeth have softer enamel", "saliva substitutes cause decay"),
    ("Which statement would the author most likely agree with?", "Chewing sugar-free gum can be a useful addition to fluoride and brushing", "Chewing gum can replace fluoride", "Measuring salivary flow is too expensive for routine care", "Saliva substitutes fully restore natural protection"),
    ("Which can be inferred about a patient whose saliva has low bicarbonate?", "The pH at the tooth surface will recover more slowly after a sugary snack", "The patient cannot develop tartar", "The patient's enamel will not dissolve", "The patient produces more lysozyme"),
    ("What is the author's tone toward saliva's role in dental care?", "Appreciative, arguing it is undervalued", "Dismissive", "Neutral and purely descriptive", "Alarmed and pessimistic"),
]

P2 = """How Teeth Learned to Hold On

(1) For most of the twentieth century, a dentist who wanted a filling to stay in a tooth had one reliable tool: geometry. Amalgam and gold do not stick to enamel or dentin, so the cavity was cut into a shape that locked the restoration mechanically, with walls that converged, grooves and undercuts. The rule, taught to generations of students, was to extend the preparation into sound tooth so that the restoration would be retained and future decay prevented. A great deal of healthy tooth was removed in the process, but there seemed to be no alternative.

(2) The alternative began with an observation from industry. In the 1950s a dental researcher, Michael Buonocore, noticed that paints and adhesives held better to metal surfaces that had first been treated with acid. He applied a weak phosphoric acid to enamel and found that resin bonded to the treated surface far more strongly than to untreated enamel. The acid dissolved the enamel selectively, leaving a microscopically rough, porous surface into which liquid resin could flow and harden, forming countless tiny tags. The bond was mechanical, but at a scale no drill could produce.

(3) For a time the discovery had little practical effect. The resins of the day shrank and stained, and they could not withstand the forces of chewing. A second advance was needed, and it came in the early 1960s, when Rafael Bowen developed a new monomer, now known as Bis-GMA, that could be combined with finely ground glass treated to bond chemically with the resin. The result was a composite material that was stronger and more stable than earlier resins. Combined with acid-etched enamel, it allowed a filling to be bonded rather than merely wedged in place.

(4) Dentin proved a much harder problem. Unlike enamel, it is a living, wet tissue riddled with tiny tubules and built around a scaffold of collagen. When acid is applied to dentin, the mineral dissolves and leaves the collagen exposed; if this soft network is dried, it collapses and the resin cannot penetrate it. It took decades of research, much of it in Japan, to show that resin could be made to infiltrate the moist, demineralized collagen and form what came to be called the hybrid layer. Some later systems added molecules that bond chemically to the calcium remaining in the tooth, improving the durability of the joint.

(5) These developments changed the philosophy of the profession as much as its materials. If a restoration could be held by adhesion, the cavity no longer needed to be shaped for retention, and the dentist could remove only the decayed tissue. The term 'minimally invasive dentistry' summarizes the shift. Small lesions could be sealed rather than drilled, and broken front teeth could be rebuilt without crowns.

(6) Adhesive dentistry is not without problems. Bonded restorations are sensitive to technique: contamination with saliva or blood, overdrying of dentin, or an incompletely cured resin can each weaken the bond. Over years in the mouth, the hybrid layer can degrade, and enzymes released from the dentin itself may contribute. Researchers continue to argue about how long bonded restorations last compared with the older materials they replaced. Still, few dentists would return to the era of extension for prevention, when the healthiest tooth structure was often sacrificed to hold a filling in place."""

Q2 = [
    ("What is the passage mainly about?", "How adhesive bonding developed and changed the way teeth are restored", "Why amalgam is the best filling material", "The chemistry of collagen in dentin", "The history of dental schools"),
    ("According to paragraph 1, how were fillings retained before adhesion?", "By cutting the cavity into a shape that locked them mechanically", "By chemical bonds to dentin", "By acid etching of the enamel", "By light-cured resin cements"),
    ("What gave Buonocore the idea of etching enamel?", "Industrial practice of treating metal surfaces with acid before painting or bonding", "A study of tooth decay in children", "The failure of gold restorations", "Research on dentin collagen"),
    ("According to the passage, how does resin hold to etched enamel?", "It flows into a microscopically rough surface and hardens into tiny tags", "It forms a covalent bond with every enamel crystal", "It dissolves the enamel and replaces it", "It is held by suction"),
    ("Why did etching have little practical effect at first?", "The available resins shrank, stained and could not withstand chewing forces", "Dentists refused to use acid", "Phosphoric acid was not yet available", "Enamel could not be etched reliably"),
    ("As used in paragraph 4, 'riddled with' most nearly means", "full of", "puzzled by", "protected from", "free of"),
    ("Why must demineralized dentin not be dried before bonding, according to the passage?", "Its collagen network collapses and the resin cannot penetrate it", "Drying adds bacteria", "Drying strengthens the bond too much", "Dry dentin dissolves faster"),
    ("Which sequence matches the passage?", "Acid etching of enamel → Bis-GMA composites → the hybrid layer in dentin → minimally invasive dentistry", "Hybrid layer → acid etching → Bis-GMA → extension for prevention", "Bis-GMA → amalgam → acid etching → dentin bonding", "Minimally invasive dentistry → acid etching → Bis-GMA → hybrid layer"),
    ("Which statement is NOT supported by the passage?", "Bonded restorations have been proven to last longer than amalgam in every study", "Contamination with saliva can weaken a bond", "The hybrid layer can degrade over time", "Adhesion allowed smaller preparations"),
    ("What is the author's overall attitude toward adhesive dentistry?", "Favourable, while acknowledging its unresolved problems", "Entirely uncritical", "Hostile", "Indifferent"),
]


def case(passage, qs):
    c = {"p": passage}
    for k, (q, a, b, cc, d) in enumerate(qs, 1):
        c.update({f"q{k}": q, f"q{k}_a": a, f"q{k}_b": b, f"q{k}_c": cc, f"q{k}_d": d})
    return c


tpl = {
    "template": "dt-rc-full-passage",
    "skill": "dat.reading",
    "pace": "workout",
    "cases": [case(P1, Q1), case(P2, Q2)],
    "prompt": "Set a 20-minute timer and answer all ten questions. Read the passage once for its structure, then go to the questions and back to the paragraph each one points to.\n\n{{p}}",
    "parts": [{"ask": "{{q%d}}" % k, "label": f"a{k}", "choice": [f"{{{{q{k}_{x}}}}}" for x in "abcd"], "correct": 0,
               "explain": "Go back to the paragraph the question points to; the right answer restates it, and the wrong ones are often true of a different paragraph or go further than the text"} for k in range(1, 11)],
    "verify": {"authored": True},
}
R1 = [
    ("What is the function of paragraph 1?", "It introduces saliva as undervalued and previews that its components each have a job", "It describes how bacteria make acid", "It argues that toothpaste is useless", "It lists diseases that cause dry mouth"),
    ("What does paragraph 2 contribute?", "Saliva's mechanical role, with clearance as a measurable example", "A definition of the critical pH", "A history of saliva research", "A recommendation to chew gum"),
    ("How does paragraph 3 relate to paragraph 2?", "It moves from saliva's mechanical job to its chemical one", "It contradicts paragraph 2", "It repeats paragraph 2 with new numbers", "It gives an example of paragraph 2's claim"),
    ("What role does paragraph 5 play in the argument?", "It shows saliva's value by what goes wrong when it fails", "It introduces the passage's main idea for the first time", "It refutes the claims of paragraph 4", "It describes a new saliva substitute"),
    ("What does the final paragraph do?", "Draws a practical conclusion for prevention from the preceding description", "Introduces a new protein", "Summarises the history of dentistry", "Rejects fluoride"),
]
R2 = [
    ("What is the function of paragraph 1?", "It describes the problem adhesion later solved: retention by cutting tooth", "It explains acid etching", "It praises amalgam over composite", "It introduces Bis-GMA"),
    ("How does paragraph 3 relate to paragraph 2?", "It explains why the discovery in paragraph 2 needed a second advance to matter", "It disputes paragraph 2's discovery", "It repeats paragraph 2", "It moves to dentin bonding"),
    ("Why does the author include paragraph 4?", "To show that dentin posed a separate, harder problem than enamel", "To argue that dentin cannot be bonded", "To introduce minimally invasive dentistry", "To describe industrial adhesives"),
    ("What is the role of paragraph 5?", "It states the consequence for the profession's philosophy", "It lists the remaining problems", "It describes Buonocore's experiment", "It explains collagen collapse"),
    ("What does paragraph 6 add to the passage?", "A qualification: adhesion's limits and open questions", "A new discovery", "The passage's thesis for the first time", "A rejection of adhesive dentistry"),
]
tpl2 = {
    "template": "dt-rc-paragraph-roles",
    "skill": "dat.reading",
    "pace": "workout",
    "cases": [dict(case(P1, R1)), dict(case(P2, R2))],
    "prompt": "Skim the passage for its structure (about 5 minutes), then say what each paragraph does in the argument.\n\n{{p}}",
    "parts": [{"ask": "{{q%d}}" % k, "label": f"a{k}", "choice": [f"{{{{q{k}_{x}}}}}" for x in "abcd"], "correct": 0,
               "explain": "Ask what the paragraph does for the whole argument, not what it says: introduce, give an example, contrast, qualify or conclude"} for k in range(1, 6)],
    "verify": {"authored": True},
}

head = "# Generated by scripts/dat_rc_long.py: edit the script, not this file.\n# Full-length DAT reading passages (original), ten questions each, against a 20-minute clock.\n\n"
open(os.path.join(ROOT, "drills/problems/dat-rc-long.yaml"), "w").write(head + yaml.safe_dump([tpl, tpl2], allow_unicode=True, sort_keys=False, width=10000))
print("dat-rc-full-passage: 2 passages x 10 questions")
