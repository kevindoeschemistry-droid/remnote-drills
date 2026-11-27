"""Pharmacology (RX, Nov 2026): principles of pharmacology and the main drug classes. Structure in UNITS (written by
scripts/fw_setup.py), two question types per objective.

Basis: the IUPHAR core concepts of pharmacology (Guilding et al., Br. J. Pharmacol. 2023/24): all 24 concepts and
shortened labels of their 103 sub-concepts were read through an extraction of the open-access copy, so read: part.
They anchor units 1-3. The ASPET Pharmacology Learning Objectives (2026 edition) are the itemised drug-class standard
and could NOT be read (the PDF would not fetch), so they are registered as wanted and units 4-8 are a house list in
the usual textbook order, at the level of class, mechanism and signature adverse effect. Quantitative items are
recomputed; any dose limit a card needs is printed on the card."""
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "px-pharmacology", "pharmacology", "P1"
M = "Symbol('m')"
FW = dict(id="pharmacology", title="Pharmacology", code="RX", domain="pharm", track="health", requires=["anatomy-physiology", "chemistry"], level=4,
          primary="iuphar-core-concepts", also=[], wanted=["aspet-plo-2026"], subject="Human Biology",
          note="Units 1-3 are anchored on the IUPHAR core concepts of pharmacology (24 concepts read through an extraction). Units 4-8, the drug classes, are a house list in textbook order because the ASPET Pharmacology Learning Objectives (2026) could not be fetched; rebase them when that document is read. Class, mechanism and signature adverse effect only: no dosing regimens, and nothing here is clinical advice.",
          header=["What a drug does to the body and what the body does to the drug, then the major drug classes by",
                  "mechanism. The principles units are quantitative (occupancy, half-life, clearance, loading dose);",
                  "the class units are recall. Dental and nursing applications are in INBDE and NCLEX."],
          source=dict(id="pharm-outline", title="Pharmacology by core concept and drug class (course outline)", short="Pharm outline", field="pharmacology",
                      note=["The IUPHAR core concepts and the usual drug-class order written as a source so the pharm.* skills have a home.", "NOT a book. Chapter numbers are ours."]))
_C = ["Drug targets", "Drug-target interaction", "Structure-activity relationship", "Mechanism of drug action", "Dose- and concentration-response relationships", "Drug affinity", "Drug efficacy",
      "Drug potency", "Drug selectivity", "Drug absorption", "Drug bioavailability", "Drug distribution", "Volume of distribution", "Drug metabolism", "First- and zero-order kinetics",
      "Drug elimination", "Elimination half-life", "Drug clearance", "Steady-state concentration", "Drug tolerance", "Adverse drug reaction", "Therapeutic index", "Drug interaction",
      "Individual variation in drug response"]
STDS = [{"id": "iuphar-core-concepts", "name": "Core concepts of pharmacology (IUPHAR Education Section; Guilding et al., British Journal of Pharmacology)", "publisher": "International Union of Basic and Clinical Pharmacology, Education Section", "kind": "standard", "read": "part",
         "url": "https://strathprints.strath.ac.uk/89676/7/Guilding-etal-BJP-2023-Defining-and-unpacking-the-core-concepts-of-pharmacology.pdf",
         "note": "Read Nov 2026 through an extraction of the open-access copy: the 24 core concepts by name and shortened labels for their 103 sub-concepts. The consensus definitions were not read word for word, so read: part. Items are the 24 concepts in the paper's order, coded C1-C24 by us.",
         "items": [{"code": f"C{k + 1}", "title": t} for k, t in enumerate(_C)]},
        {"id": "aspet-plo-2026", "name": "ASPET Pharmacology Learning Objectives (2026 edition; formerly the AMSPC Knowledge Objectives in Medical Pharmacology)", "publisher": "American Society for Pharmacology and Experimental Therapeutics, Division for Pharmacology Education", "kind": "standard", "read": "none",
         "url": "https://www.aspet.org/aspet/education-careers/teaching-resources/pharmacology-learning-objectives",
         "note": "Found Nov 2026: the itemised, drug-class-level standard for health-professions pharmacology. The landing page was read; the PDF itself would not fetch, so nothing in it has been read and no item is registered. Wanted as the basis for Pharmacology units 4-8."}]
SKILLS = [("dynamics", "Targets, agonists and antagonists, dose-response, affinity, efficacy, potency and selectivity", "Pharmacodynamics", []),
          ("kinetics", "Absorption, bioavailability, distribution, metabolism, elimination, half-life, clearance and steady state", "Pharmacokinetics", ["pharm.dynamics"]),
          ("safety", "Therapeutic index, adverse reactions, tolerance, interactions and individual variation", "Safety and variation", ["pharm.kinetics"]),
          ("autonomic", "Cholinergic and adrenergic agonists and antagonists", "Autonomic drugs", ["pharm.dynamics"]),
          ("cardio", "Antihypertensives, diuretics, antithrombotics, lipid drugs and cardiac drugs", "Cardiovascular and renal drugs", ["pharm.autonomic"]),
          ("cns", "Local and general anaesthetics, sedatives, psychiatric drugs, opioids and NSAIDs", "Central nervous system and pain", ["pharm.autonomic"]),
          ("antimicrobial", "Antibacterial, antifungal, antiviral and anticancer drugs", "Chemotherapy", ["pharm.safety"]),
          ("endocrine", "Drugs for diabetes, corticosteroids, thyroid, respiratory and gastrointestinal drugs", "Endocrine and other systems", ["pharm.cardio"])]
IDEAS = [("PD", "What the drug does to the body", "A drug acts by binding a target; how much binds is set by affinity and concentration, and what the binding does is set by efficacy."),
         ("PK", "What the body does to the drug", "Absorption, distribution, metabolism and excretion set the concentration at the target over time; clearance and volume of distribution are the two independent parameters and half-life follows from them."),
         ("CLASS", "Learn the class, then the exception", "Drugs in a class share a mechanism, and most of their uses and adverse effects follow from it.")]
PRACTICES = [("P1", "Compute", "Carry a pharmacodynamic or pharmacokinetic relation to a number."),
             ("P2", "Identify", "Name the mechanism, class or effect from a description.")]
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
PD, PK, SF, AU, CV, CN, AM, EN = ["pharm." + s[0] for s in SKILLS]
U = lambda *s: [f"iuphar-core-concepts:C{x}" for x in s]


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def L(name, skill, prompt, options, rows, explain):
    return Q(name, skill, prompt, pace="recall", cases=[{"q": a, "kc": k} for a, k in rows], choice=options, correct="kc", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", **kw):
    return Q(name, skill, prompt, value=value, tex=tex, verify=verify, explain=explain, **kw)


def C(keys, rows):
    return [dict(zip(keys.split(), r)) for r in rows]


UNITS = {
 1: ("dynamics", "Pharmacodynamics", U(1, 2, 3, 4, 5, 6, 7, 8, 9), ["PD"], {
   1: ("Drugs and targets", [
     ("A", U(1, 2, 4), "Name the classes of drug target and the kinds of drug-target interaction.",
      "Most drugs act on receptors, enzymes, ion channels or transporters. An agonist binds and activates; an antagonist binds without activating and blocks the agonist. Binding may be reversible or irreversible, at the agonist's own (orthosteric) site or at an allosteric site.", "P2", [
       L("px-target-class", PD, "Which class of drug target? {{q}}", ["Receptor", "Enzyme", "Ion channel", "Transporter"], [
           ("A beta blocker binding the beta-1 adrenoceptor", 0), ("An ACE inhibitor", 1), ("A local anaesthetic blocking sodium entry into a nerve", 2), ("An SSRI blocking serotonin reuptake", 3),
           ("Aspirin inhibiting cyclooxygenase", 1), ("A proton pump inhibitor acting on the H+/K+ ATPase", 3), ("Morphine acting at the mu site", 0), ("A statin acting on HMG-CoA reductase", 1)],
         "Ask what kind of protein the drug binds"),
       F("px-interaction-types", PD, [
           ("A drug that binds a receptor and produces no response of its own, but prevents the agonist's effect, is what?", "an antagonist", "a full agonist", "a partial agonist", "an inverse agonist"),
           ("A drug that binds at a site other than the agonist's and changes the receptor's response is what?", "an allosteric modulator", "a competitive antagonist", "a prodrug", "a full agonist"),
           ("A drug that reduces a receptor's activity below its baseline level is what?", "an inverse agonist", "a neutral antagonist", "a partial agonist", "an allosteric activator"),
           ("Aspirin acetylates cyclooxygenase permanently. What kind of inhibition is this?", "irreversible", "competitive reversible", "allosteric reversible", "none: aspirin is an agonist")],
         "Agonists activate, antagonists occupy, inverse agonists switch off constitutive activity")]),
     ("B", U(5, 7, 8), "Read a dose-response curve for potency and efficacy.",
      "Response = Emax × C ÷ (C + EC50) for the simplest case. Potency is how little drug is needed (a lower EC50 is more potent); efficacy is the maximum response the drug can produce. A partial agonist has a lower Emax than a full agonist whatever its potency.", "P1", [
       N("px-fractional-response", PD, "A drug has an EC50 of {{ke}} nM. What percentage of its maximum effect does it produce at a concentration of {{kn}} nM, assuming response = Emax × C / (C + EC50)?", "100*kn/(kn + ke)",
         f"solve(Eq({M}*(kn + ke), 100*kn), {M})[0]", "At the EC50 the response is half of maximum; ten times the EC50 gives about 91%", tex="pct",
         cases=C("ke kn", [(10, 10), (10, 30), (50, 450), (20, 5), (100, 900), (4, 12)])),
       L("px-potency-efficacy", PD, "Drug A: EC50 {{q}}. Which statement is true?", ["A is more potent and more efficacious", "A is more potent; B is more efficacious", "B is more potent; A is more efficacious", "B is more potent and more efficacious"], [
           ("1 nM, Emax 100%. Drug B: EC50 10 nM, Emax 60%", 0), ("1 nM, Emax 50%. Drug B: EC50 10 nM, Emax 100%", 1), ("30 nM, Emax 100%. Drug B: EC50 3 nM, Emax 40%", 2),
           ("200 nM, Emax 70%. Drug B: EC50 20 nM, Emax 100%", 3), ("5 nM, Emax 80%. Drug B: EC50 50 nM, Emax 100%", 1)],
         "Potency is read on the concentration axis, efficacy on the response axis")]),
     ("C", U(6), "Compute receptor occupancy from affinity.",
      "The dissociation constant Kd is the concentration at which half the receptors are occupied; a lower Kd is a higher affinity. Fractional occupancy = [L] ÷ ([L] + Kd).", "P1", [
       N("px-occupancy", PD, "A ligand with Kd = {{kd}} nM is present at {{kl}} nM. What percentage of its receptors are occupied at equilibrium?", "100*kl/(kl + kd)",
         f"solve(Eq({M}/100*(kl + kd), kl), {M})[0]", "Occupancy follows the law of mass action; at [L] = Kd it is 50%", tex="pct",
         cases=C("kd kl", [(2, 2), (5, 15), (1, 9), (20, 5), (8, 72), (50, 150)])),
       N("px-concentration-for-occupancy", PD, "A ligand has Kd = {{kd}} nM. What concentration occupies {{kp}}% of its receptors?", "kd*kp/(100 - kp)",
         f"solve(Eq({M}/({M} + kd), Rational(kp, 100)), {M})[0]", "Rearranged: [L] = Kd × occupancy / (1 − occupancy), so 90% needs nine times Kd", tex="L",
         cases=C("kd kp", [(2, 90), (5, 75), (10, 50), (4, 80), (1, 99), (20, 20)]))]),
     ("D", U(2, 8), "Tell competitive from non-competitive antagonism and compute a dose ratio.",
      "A competitive antagonist shifts the agonist curve to the right without lowering the maximum, and more agonist overcomes it; the dose ratio is 1 + [B] ÷ KB. A non-competitive or irreversible antagonist lowers the maximum response.", "P1", [
       N("px-dose-ratio", PD, "A competitive antagonist with KB = {{kb}} nM is present at {{ka}} nM. By what factor must the agonist concentration be raised to restore the original response?", "1 + ka/kb",
         f"solve(Eq(({M} - 1)*kb, ka), {M})[0]", "The Schild relation: dose ratio = 1 + [B]/KB", tex="DR",
         cases=C("kb ka", [(1, 9), (5, 20), (2, 2), (10, 990), (4, 12)])),
       L("px-antagonist-curve", PD, "What happens to the agonist's concentration-response curve? {{q}}", ["Shifts right, same maximum", "Maximum is reduced", "Shifts left"], [
           ("A reversible competitive antagonist is added", 0), ("An irreversible antagonist inactivates most receptors in a tissue with no spare receptors", 1), ("A non-competitive antagonist is added", 1),
           ("A positive allosteric modulator that increases agonist affinity is added", 2), ("More of a surmountable antagonist is added", 0)],
         "Surmountable antagonism moves the curve; insurmountable antagonism flattens it")]),
     ("E", U(3, 9), "Quantify selectivity and explain why it is lost at high dose.",
      "Selectivity is preferential affinity for one target over another, measured as the ratio of the two Kd or IC50 values. It is relative: at a high enough concentration the second target is occupied too, which is where many adverse effects come from.", "P1", [
       N("px-selectivity-ratio", PD, "A drug has Kd = {{ka}} nM at its intended target and {{kb}} nM at an off-target receptor. How many times more selective is it for the intended target?", "kb/ka",
         f"solve(Eq({M}*ka, kb), {M})[0]", "Ratio of the two dissociation constants; the lower Kd is the preferred target", tex="ratio",
         cases=C("ka kb", [(2, 200), (0.5, 50), (10, 300), (4, 4000), (25, 100)])),
       F("px-selectivity-concepts", PD, [
           ("A beta-1 selective blocker causes bronchospasm at high dose. Why?", "selectivity is relative, and at high concentration it also blocks beta-2 receptors", "it becomes an agonist", "its metabolite is an antihistamine", "beta-1 receptors are in the bronchi"),
           ("What does a structure-activity relationship describe?", "how changes in a molecule's structure change its activity at a target", "how dose relates to plasma concentration", "how fast a drug is cleared", "how two drugs interact"),
           ("Two enantiomers of a drug often differ in potency. Why?", "the target's binding site is itself chiral", "they have different molecular weights", "one is always inactive in every case", "they have different formulas"),
           ("Which term describes a drug that binds many targets with similar affinity?", "non-selective", "highly potent", "a prodrug", "a partial agonist")],
         "No drug is specific; some are selective enough within a dose range")])]),
 }),
 2: ("kinetics", "Pharmacokinetics", U(10, 11, 12, 13, 14, 15, 16, 17, 18, 19), ["PK"], {
   1: ("The fate of a drug", [
     ("A", U(10), "Predict ionisation and absorption from pKa and pH.",
      "The un-ionised form crosses membranes. For a weak acid the un-ionised fraction is 1 ÷ (1 + 10^(pH − pKa)); for a weak base it is 1 ÷ (1 + 10^(pKa − pH)). A drug is trapped on the side of a membrane where it is more ionised: weak acids in alkaline fluid, weak bases in acidic fluid.", "P1", [
       N("px-unionised-acid", PK, "A weak acid has pKa {{ka}}. What percentage of it is un-ionised at pH {{kp}}?", "100/(1 + 10^(kp - ka))",
         "100/(1 + exp((kp - ka)*log(10)))", "Each pH unit above the pKa cuts the un-ionised share of an acid roughly tenfold", tex="pct", tol=0.01,
         cases=C("ka kp", [(3.5, 1.5), (3.5, 7.4), (4.4, 5.4), (7.4, 7.4), (5, 3), (3, 6)])),
       L("px-ion-trapping", PK, "Where does the drug accumulate (become trapped)? {{q}}", ["In the more acidic compartment", "In the more alkaline compartment"], [
           ("A weak acid such as aspirin, between acidic urine and alkalinised urine", 1), ("A weak base such as amphetamine, between plasma and acidic urine", 0),
           ("A weak base, between plasma (pH 7.4) and gastric juice (pH 2)", 0), ("A weak acid, between plasma and urine made alkaline with bicarbonate", 1),
           ("A weak base local anaesthetic, between normal tissue and inflamed acidic tissue outside the nerve", 0)],
         "Drugs are trapped where they are charged: acids in base, bases in acid")]),
     ("B", U(11), "Compute bioavailability and explain first-pass metabolism.",
      "Bioavailability F is the fraction of a dose reaching the systemic circulation unchanged: F = (AUC oral ÷ AUC IV) × (dose IV ÷ dose oral). An intravenous dose has F = 1. Oral drugs pass through the gut wall and liver first, which can remove much of the dose.", "P1", [
       N("px-bioavailability", PK, "An oral dose of {{kd}} mg gives an AUC of {{ka}} mg·h/L; an intravenous dose of {{kv}} mg gives an AUC of {{kb}} mg·h/L. Find the oral bioavailability in percent.", "100*(ka/kd)/(kb/kv)",
         f"solve(Eq({M}/100*kb/kv*kd, ka), {M})[0]", "Compare dose-normalised exposure by the two routes", tex="F",
         cases=C("kd ka kv kb", [(100, 20, 50, 25), (200, 30, 100, 50), (500, 40, 100, 20), (50, 9, 50, 12), (400, 36, 100, 30)])),
       F("px-first-pass", PK, [
           ("Through which organ does an orally absorbed drug pass before reaching the systemic circulation?", "the liver, by the portal vein", "the kidney", "the lung only", "the spleen"),
           ("Which route avoids first-pass metabolism most completely?", "intravenous", "oral", "rectal, high in the rectum", "oral with food"),
           ("Why is glyceryl trinitrate given under the tongue?", "sublingual absorption bypasses the liver, which would otherwise destroy most of the dose", "it tastes better", "it is not absorbed from the mouth", "it needs stomach acid"),
           ("What is the bioavailability of an intravenous bolus?", "100%", "50%", "it depends on the liver", "0%")],
         "First pass is why the oral dose of some drugs is many times the intravenous dose")]),
     ("C", U(12, 13), "Compute and interpret the volume of distribution.",
      "Vd = amount of drug in the body ÷ plasma concentration. It is an apparent volume: a drug held in plasma by protein binding has a Vd near plasma volume, while a lipophilic drug stored in tissue can have a Vd of hundreds of litres.", "P1", [
       N("px-volume-of-distribution", PK, "An intravenous bolus of {{kd}} mg gives an initial plasma concentration of {{kc0}} mg/L (extrapolated to time zero). Find the volume of distribution in litres.", "kd/kc0",
         f"solve(Eq({M}*kc0, kd), {M})[0]", "Dose over initial concentration", tex="V_d",
         cases=C("kd kc0", [(500, 25), (100, 0.5), (300, 60), (1000, 10), (40, 0.1)])),
       L("px-vd-size", PK, "Would you expect a small or a large volume of distribution? {{q}}", ["Small (close to plasma or extracellular volume)", "Large (many times body water)"], [
           ("A drug that is 99% bound to plasma albumin", 0), ("A highly lipophilic drug that accumulates in fat", 1), ("A large, charged molecule such as heparin", 0),
           ("A drug that binds avidly to tissue proteins", 1), ("A small polar drug that does not enter cells", 0)],
         "What stays in plasma has a small Vd; what leaves plasma for tissue has a large one")]),
     ("D", U(14), "Describe drug metabolism and the effect of enzyme induction and inhibition.",
      "Phase I reactions (oxidation, reduction, hydrolysis; mostly cytochrome P450) add or expose a functional group; phase II reactions conjugate (glucuronide, sulfate, acetyl, glutathione) and usually make the drug more water soluble. Inducers raise enzyme levels and lower other drugs' concentrations; inhibitors do the opposite. A prodrug is activated by metabolism.", "P2", [
       L("px-phase", PK, "Phase I or phase II metabolism? {{q}}", ["Phase I", "Phase II"], [
           ("Oxidation by a cytochrome P450", 0), ("Glucuronidation", 1), ("Hydrolysis of an ester", 0), ("Acetylation", 1), ("Conjugation with glutathione", 1), ("N-dealkylation", 0)],
         "Phase I functionalises, phase II conjugates"),
       L("px-induce-inhibit", PK, "What happens to the plasma concentration of a second drug cleared by the same enzyme? {{q}}", ["It falls", "It rises"], [
           ("A P450 inducer such as rifampicin is started", 0), ("A P450 inhibitor such as clarithromycin is started", 1), ("Regular grapefruit juice is added, for a CYP3A4 substrate taken by mouth", 1),
           ("Carbamazepine, an inducer, is started", 0), ("A long-standing inducer is stopped", 1)],
         "More enzyme, less drug; less enzyme, more drug")]),
     ("E", U(15, 16), "Tell first-order from zero-order elimination and compute what remains.",
      "In first-order elimination a constant fraction is removed per unit time, so the half-life is constant and the concentration falls exponentially. In zero-order elimination a constant amount is removed per unit time because the enzymes are saturated (ethanol, high-dose phenytoin and aspirin).", "P1", [
       N("px-first-order-remaining", PK, "A drug with a half-life of {{kh}} hours has a plasma concentration of {{ka}} mg/L. What is the concentration {{kt}} hours later, with first-order elimination and no further dosing?", "ka*0.5^(kt/kh)",
         "ka*exp(-log(2)*kt/kh)", "Halve once for each half-life elapsed", tex="C",
         cases=C("kh ka kt", [(4, 80, 12), (6, 40, 12), (8, 10, 24), (2, 64, 10), (12, 20, 36)])),
       L("px-order", PK, "First-order or zero-order elimination? {{q}}", ["First-order", "Zero-order"], [
           ("A constant fraction of the drug is eliminated each hour", 0), ("A constant amount of the drug is eliminated each hour", 1), ("The half-life is the same at every concentration", 0),
           ("Elimination enzymes are saturated", 1), ("Concentration against time is a straight line on an ordinary (linear) plot", 1), ("Log concentration against time is a straight line", 0)],
         "Fraction against amount; most drugs at therapeutic doses are first-order")]),
     ("F", U(17, 18), "Relate half-life, clearance and volume of distribution.",
      "Clearance is the volume of plasma cleared of drug per unit time: CL = dose ÷ AUC for an intravenous dose. Half-life depends on both independent parameters: t½ = 0.693 × Vd ÷ CL.", "P1", [
       N("px-half-life", PK, "A drug has a volume of distribution of {{kv}} L and a clearance of {{kl}} L/h. Find its half-life in hours, using t½ = 0.693 Vd / CL.", "0.693*kv/kl",
         f"solve(Eq({M}*kl, Rational(693, 1000)*kv), {M})[0]", "A large volume or a low clearance both lengthen the half-life", tex="t",
         cases=C("kv kl", [(40, 4), (200, 10), (15, 6), (500, 35), (70, 7)])),
       N("px-clearance-from-auc", PK, "An intravenous dose of {{kd}} mg gives an AUC of {{ka}} mg·h/L. Find the clearance in L/h.", "kd/ka", f"solve(Eq({M}*ka, kd), {M})[0]",
         "Clearance is dose over total exposure", tex="CL",
         cases=C("kd ka", [(500, 50), (100, 8), (250, 100), (1000, 40), (60, 15)]))]),
     ("G", U(19), "Design a loading and a maintenance dose for a target steady-state concentration.",
      "At steady state the rate in equals the rate out: maintenance dosing rate = CL × Css ÷ F. A loading dose fills the volume at once: loading dose = Vd × Css ÷ F. Without a loading dose, steady state is reached in about four to five half-lives.", "P1", [
       N("px-maintenance-rate", PK, "A drug has a clearance of {{kl}} L/h and an oral bioavailability of {{kf}}%. What oral dosing rate in mg/h keeps the average steady-state concentration at {{ks}} mg/L?", "kl*ks/(kf/100)",
         f"solve(Eq({M}*kf/100, kl*ks), {M})[0]", "Rate in must equal rate out, which is clearance times concentration", tex="rate",
         cases=C("kl kf ks", [(5, 100, 10), (4, 50, 2), (10, 80, 4), (2.5, 25, 8), (6, 60, 15)])),
       N("px-loading-dose", PK, "A drug has a volume of distribution of {{kv}} L and is given intravenously. What loading dose in mg gives a concentration of {{ks}} mg/L at once?", "kv*ks",
         f"solve(Eq({M}/kv, ks), {M})[0]", "The loading dose depends on volume, the maintenance dose on clearance", tex="dose",
         cases=C("kv ks", [(40, 10), (500, 0.0015), (15, 20), (70, 2), (35, 15)]))])]),
 }),
 3: ("safety", "Safety and variation", U(20, 21, 22, 23, 24), ["PD", "PK"], {
   1: ("When the response is not the one intended", [
     ("A", U(22), "Compute a therapeutic index and say what a narrow one requires.",
      "Therapeutic index = TD50 ÷ ED50 (LD50 ÷ ED50 in animal studies). A drug with a low index (warfarin, digoxin, lithium, phenytoin, aminoglycosides) needs careful dosing and often monitoring of plasma levels or effect.", "P1", [
       N("px-therapeutic-index", SF, "A drug's ED50 is {{ka}} mg/kg and its TD50 is {{kb}} mg/kg. Find the therapeutic index.", "kb/ka", f"solve(Eq({M}*ka, kb), {M})[0]",
         "Toxic dose over effective dose: larger is safer", tex="TI",
         cases=C("ka kb", [(5, 500), (2, 6), (10, 40), (0.5, 50), (20, 50)])),
       F("px-narrow-index", SF, [
           ("Which of these drugs has a narrow therapeutic index?", "digoxin", "amoxicillin", "loratadine", "omeprazole"),
           ("What does a narrow therapeutic index usually require in practice?", "individualised dosing and monitoring", "giving the largest dose available", "avoiding all monitoring", "dosing by body surface area only"),
           ("Which of these drugs is commonly monitored with plasma levels because of a narrow index?", "lithium", "paracetamol at ordinary doses", "penicillin V", "cetirizine"),
           ("Drug X has a therapeutic index of 2 and drug Y of 200. Which has the wider margin of safety?", "Y", "X", "they are equal", "it cannot be said without the half-lives")],
         "Warfarin, digoxin, lithium, phenytoin, theophylline, aminoglycosides: the usual narrow-index list")]),
     ("B", U(20, 21), "Classify adverse drug reactions and explain tolerance.",
      "Type A (augmented) reactions are dose-related extensions of the drug's pharmacology and are predictable; type B (bizarre) reactions are unrelated to dose, often immune or genetic, and unpredictable. Tolerance is a reduced response on repeated dosing, from pharmacodynamic change (receptor down-regulation) or pharmacokinetic change (enzyme induction).", "P2", [
       L("px-adr-type", SF, "Type A (dose-related, predictable) or type B (idiosyncratic) reaction? {{q}}", ["Type A", "Type B"], [
           ("Bleeding on warfarin", 0), ("Anaphylaxis to penicillin", 1), ("Hypoglycaemia on insulin", 0), ("Respiratory depression from an opioid", 0),
           ("Haemolysis from a drug in a person with G6PD deficiency", 1), ("Dry mouth from an antimuscarinic drug", 0), ("A severe blistering skin reaction to a first exposure to a drug", 1)],
         "If lowering the dose would fix it, it is type A"),
       F("px-tolerance", SF, [
           ("Regular opioid use leads to a need for larger doses for the same pain relief. What is this called?", "tolerance", "idiosyncrasy", "potentiation", "first-pass effect"),
           ("Which is a pharmacokinetic mechanism of tolerance?", "the drug induces its own metabolising enzymes", "receptors are down-regulated", "second messengers adapt", "the target mutates"),
           ("Tolerance that develops within minutes to hours of repeated doses is called what?", "tachyphylaxis", "anaphylaxis", "synergy", "bioaccumulation"),
           ("Which is a pharmacodynamic mechanism of tolerance?", "receptor down-regulation or desensitisation", "faster renal excretion", "enzyme induction", "reduced absorption")],
         "Tolerance moves the dose-response curve to the right over time")]),
     ("C", U(23), "Classify drug interactions.",
      "Pharmacokinetic interactions change another drug's concentration (absorption, binding, metabolism, excretion). Pharmacodynamic interactions change its effect at the same concentration: additive (the sum), synergistic (more than the sum) or antagonistic (less).", "P2", [
       L("px-combined-effect", SF, "Alone, drug A lowers blood pressure by 10 mmHg and drug B by 8 mmHg. Together they lower it by {{q}} mmHg. What kind of interaction is this?", ["Additive", "Synergistic", "Antagonistic"], [
           ("18", 0), ("30", 1), ("6", 2), ("25", 1), ("11", 2)],
         "Compare the combined effect with the sum of the separate effects"),
       L("px-interaction-kind", SF, "Pharmacokinetic or pharmacodynamic interaction? {{q}}", ["Pharmacokinetic", "Pharmacodynamic"], [
           ("An antacid binds a tetracycline in the gut and reduces its absorption", 0), ("An opioid and a benzodiazepine together depress breathing more than either alone", 1),
           ("An enzyme inhibitor raises the level of a second drug", 0), ("Naloxone reverses the effect of morphine at the receptor", 1), ("Probenecid blocks the renal tubular secretion of penicillin", 0)],
         "Did the concentration change, or the response to the same concentration?")]),
     ("D", U(24), "Adjust for individual variation in drug handling.",
      "Age, body size, organ function, genetics and other drugs change the response to a standard dose. Renal function is estimated by the Cockcroft-Gault equation: creatinine clearance (mL/min) = (140 − age) × weight (kg) ÷ (72 × serum creatinine in mg/dL), multiplied by 0.85 for women.", "P1", [
       N("px-cockcroft-gault", SF, "Estimate the creatinine clearance of a {{ka}}-year-old man weighing {{kw}} kg with a serum creatinine of {{ks}} mg/dL, using (140 − age) × weight / (72 × creatinine).", "(140 - ka)*kw/(72*ks)",
         f"solve(Eq({M}*72*ks, (140 - ka)*kw), {M})[0]", "Clearance falls with age and with a rising creatinine", tex="CL_{cr}",
         cases=C("ka kw ks", [(40, 72, 1), (80, 60, 1.5), (60, 90, 2), (25, 80, 0.8), (70, 54, 1)])),
       F("px-variation", SF, [
           ("A person who is a poor metaboliser at CYP2D6 takes codeine, a prodrug. What is the likely result?", "little pain relief, because less morphine is formed", "toxicity from excess morphine", "no change", "faster elimination"),
           ("A drug is cleared almost entirely by the kidney. What should happen to its dose in renal impairment?", "it should be reduced or given less often", "it should be increased", "no change is needed", "it should be given only intravenously"),
           ("Why are newborns more sensitive to many drugs?", "their metabolising enzymes and renal function are immature", "they have a higher glomerular filtration rate", "they have more plasma protein", "they have less body water"),
           ("What does pharmacogenetics study?", "inherited differences in drug response", "drug prices", "how drugs are synthesised", "placebo effects")],
         "The standard dose is the starting point, not the answer")])]),
 }),
}
H = []   # units 4-8 are a house list: no outside item is cited
UNITS.update({
 4: ("autonomic", "Autonomic drugs", H, ["CLASS"], {
   1: ("Cholinergic and adrenergic drugs", [
     ("A", H, "Predict the effects of muscarinic agonists and antagonists.",
      "Muscarinic activation slows the heart, constricts the pupil and bronchi, increases secretions and gut and bladder motility. Antimuscarinics (atropine and relatives) do the opposite: fast heart, dilated pupils, dry mouth, constipation, urinary retention. Acetylcholinesterase inhibitors raise acetylcholine at both muscarinic and nicotinic synapses.", "P2", [
       L("px-muscarinic-effect", AU, "Is this an effect of a muscarinic agonist or of an antimuscarinic drug? {{q}}", ["Muscarinic agonist", "Antimuscarinic"], [
           ("Dry mouth", 1), ("Constricted pupils", 0), ("Slower heart rate", 0), ("Urinary retention", 1), ("Increased salivation", 0), ("Dilated pupils and blurred near vision", 1), ("Bronchodilation", 1)],
         "Muscarinic effects are rest and digest; blocking them dries, dilates and speeds"),
       F("px-cholinergic-drugs", AU, [
           ("How does neostigmine increase cholinergic transmission?", "it inhibits acetylcholinesterase", "it is a muscarinic agonist", "it blocks nicotinic receptors", "it releases norepinephrine"),
           ("Which drug is a muscarinic antagonist?", "atropine", "pilocarpine", "neostigmine", "nicotine"),
           ("Which drug is used to increase salivary flow in dry mouth because it is a muscarinic agonist?", "pilocarpine", "atropine", "ipratropium", "propranolol"),
           ("Which inhaled drug is an antimuscarinic bronchodilator?", "ipratropium", "salbutamol", "beclometasone", "montelukast")],
         "Agonists mimic acetylcholine, esterase inhibitors preserve it, antagonists block it")]),
     ("B", H, "Match adrenoceptor subtypes to their effects and agonists.",
      "Alpha-1: vasoconstriction, pupil dilation. Alpha-2: reduces central sympathetic outflow. Beta-1: raises heart rate and contractility. Beta-2: bronchodilation and vasodilation in skeletal muscle. Epinephrine acts on all four; phenylephrine is alpha-1 selective, salbutamol beta-2 selective.", "P2", [
       L("px-adrenoceptor", AU, "Which adrenoceptor mainly mediates this? {{q}}", ["Alpha-1", "Alpha-2", "Beta-1", "Beta-2"], [
           ("Vasoconstriction in skin and mucosa", 0), ("Increased heart rate and force", 2), ("Bronchodilation", 3), ("Reduced sympathetic outflow from the brainstem", 1),
           ("Pupil dilation by the radial muscle", 0), ("Relaxation of the uterus", 3), ("Renin release from the kidney", 2)],
         "Alpha-1 squeezes vessels, beta-1 drives the heart, beta-2 opens airways"),
       F("px-adrenergic-agonists", AU, [
           ("Why is epinephrine added to a local anaesthetic?", "alpha-1 vasoconstriction slows absorption, prolonging the block and reducing bleeding", "it blocks sodium channels", "it lowers the pH of the solution", "it relaxes the vessel wall"),
           ("Which drug is a selective beta-2 agonist used for asthma relief?", "salbutamol (albuterol)", "phenylephrine", "atenolol", "clonidine"),
           ("Which drug is an alpha-2 agonist that lowers blood pressure centrally?", "clonidine", "phenylephrine", "dobutamine", "salbutamol"),
           ("Which drug is the first-line treatment for anaphylaxis?", "epinephrine", "atropine", "propranolol", "clonidine")],
         "Learn one prototype per receptor")]),
     ("C", H, "Predict the effects and hazards of adrenoceptor antagonists.",
      "Beta blockers lower heart rate, contractility and renin; non-selective ones can cause bronchospasm and mask the warning signs of hypoglycaemia. Alpha-1 blockers relax vessels and the bladder neck and can cause postural hypotension.", "P2", [
       F("px-beta-blockers", AU, [
           ("Why are non-selective beta blockers avoided in asthma?", "blocking beta-2 receptors can cause bronchospasm", "they raise heart rate", "they cause dry mouth", "they dilate the bronchi too far"),
           ("Which beta blocker is relatively beta-1 selective?", "metoprolol", "propranolol", "carvedilol", "labetalol"),
           ("Which warning sign of hypoglycaemia do beta blockers mask?", "fast heartbeat and tremor", "sweating", "hunger", "confusion"),
           ("What do beta blockers do to cardiac output at rest?", "reduce it by lowering heart rate and contractility", "raise it", "leave it unchanged", "raise it by vasodilation")],
         "Beta-1 for the heart and kidney, beta-2 for the lungs: selectivity decides the hazard"),
       L("px-blocker-effect", AU, "Is this mainly an effect of an alpha-1 blocker or a beta blocker? {{q}}", ["Alpha-1 blocker", "Beta blocker"], [
           ("Dizziness on standing after the first dose", 0), ("Slow heart rate", 1), ("Easier urine flow in prostate enlargement", 0), ("Reduced renin release", 1), ("Cold hands and reduced exercise tolerance", 1)],
         "Alpha-1 block relaxes smooth muscle in vessels and the bladder neck")])]),
 }),
 5: ("cardio", "Cardiovascular and renal drugs", H, ["CLASS"], {
   1: ("Heart, vessels, kidney and blood", [
     ("A", H, "Give the mechanism and signature adverse effect of each antihypertensive class.",
      "ACE inhibitors block angiotensin II formation (cough, high potassium, angioedema); angiotensin receptor blockers block its receptor without the cough; dihydropyridine calcium channel blockers dilate arterioles (ankle swelling, gingival overgrowth); thiazides reduce sodium reabsorption; beta blockers reduce cardiac output and renin.", "P2", [
       F("px-antihypertensive-mechanism", CV, [
           ("How do ACE inhibitors lower blood pressure?", "they reduce formation of angiotensin II", "they block calcium channels", "they block beta receptors", "they block the sodium-chloride transporter"),
           ("How does amlodipine lower blood pressure?", "it blocks L-type calcium channels in arteriolar smooth muscle", "it blocks angiotensin receptors", "it inhibits renin", "it blocks alpha-2 receptors"),
           ("How does losartan act?", "it blocks the angiotensin II type 1 receptor", "it inhibits ACE", "it blocks aldosterone synthesis", "it opens potassium channels"),
           ("Which class is contraindicated in pregnancy because of fetal kidney injury?", "ACE inhibitors and angiotensin receptor blockers", "methyldopa", "labetalol", "nifedipine")],
         "Most antihypertensives act on the renin-angiotensin system, on calcium entry, on sodium or on the sympathetic drive"),
       F("px-antihypertensive-adverse", CV, [
           ("Which class commonly causes a dry cough?", "ACE inhibitors", "angiotensin receptor blockers", "calcium channel blockers", "thiazides"),
           ("Which class can cause gingival overgrowth and ankle swelling?", "dihydropyridine calcium channel blockers", "ACE inhibitors", "beta blockers", "loop diuretics"),
           ("Why do ACE inhibitors cause a cough when angiotensin receptor blockers usually do not?", "ACE also breaks down bradykinin, which accumulates", "they dry the airways", "they block beta-2 receptors", "they raise potassium"),
           ("Which electrolyte tends to rise with ACE inhibitors?", "potassium", "sodium", "calcium", "magnesium")],
         "The cough is bradykinin; the swollen gums are the calcium channel blockers")]),
     ("B", H, "Place each diuretic class on the nephron and predict its electrolyte effects.",
      "Loop diuretics block the Na-K-2Cl carrier in the thick ascending limb (most powerful; lose potassium, calcium). Thiazides block Na-Cl in the distal tubule (lose potassium, retain calcium). Potassium-sparing drugs act in the collecting duct (spironolactone blocks aldosterone; amiloride blocks the sodium channel). Carbonic anhydrase inhibitors act in the proximal tubule; osmotic diuretics throughout.", "P2", [
       L("px-diuretic-site", CV, "Where does it act? {{q}}", ["Proximal tubule", "Thick ascending limb of the loop", "Distal convoluted tubule", "Collecting duct"], [
           ("Furosemide", 1), ("Hydrochlorothiazide", 2), ("Spironolactone", 3), ("Acetazolamide", 0), ("Amiloride", 3), ("Bumetanide", 1)],
         "Proximal, loop, distal, collecting duct: carbonic anhydrase inhibitor, loop, thiazide, potassium-sparing"),
       F("px-diuretic-electrolytes", CV, [
           ("Which diuretic class tends to raise plasma potassium?", "potassium-sparing diuretics", "loop diuretics", "thiazides", "osmotic diuretics"),
           ("Which diuretic class reduces urinary calcium excretion?", "thiazides", "loop diuretics", "carbonic anhydrase inhibitors", "osmotic diuretics"),
           ("Which adverse effect is particular to high-dose loop diuretics?", "hearing damage", "gingival overgrowth", "dry cough", "gynaecomastia"),
           ("Which diuretic can cause gynaecomastia through its antiandrogen action?", "spironolactone", "furosemide", "amiloride", "mannitol")],
         "Loops lose calcium, thiazides keep it; both lose potassium, the collecting-duct drugs keep it")]),
     ("C", H, "Match antithrombotic and lipid-lowering drugs to their mechanisms.",
      "Warfarin blocks vitamin K recycling (factors II, VII, IX, X; monitored by INR; reversed by vitamin K). Heparin potentiates antithrombin (reversed by protamine). Direct oral anticoagulants inhibit factor Xa or thrombin. Aspirin irreversibly inhibits platelet cyclooxygenase; clopidogrel blocks the platelet P2Y12 receptor. Statins inhibit HMG-CoA reductase.", "P2", [
       F("px-antithrombotic-mechanism", CV, [
           ("How does warfarin act?", "it blocks vitamin K epoxide reductase, lowering the vitamin K-dependent clotting factors", "it potentiates antithrombin", "it inhibits platelet cyclooxygenase", "it directly inhibits thrombin"),
           ("How does heparin act?", "it potentiates antithrombin", "it blocks vitamin K recycling", "it blocks the P2Y12 receptor", "it dissolves fibrin"),
           ("How does low-dose aspirin reduce clotting?", "it irreversibly inhibits platelet cyclooxygenase, reducing thromboxane A2", "it inhibits factor Xa", "it blocks the P2Y12 receptor", "it lowers fibrinogen"),
           ("Which drug is a direct factor Xa inhibitor?", "rivaroxaban", "dabigatran", "clopidogrel", "warfarin")],
         "Anticoagulants act on the clotting cascade, antiplatelet drugs on the platelet"),
       F("px-antithrombotic-monitoring", CV, [
           ("Which test monitors warfarin?", "INR (prothrombin time)", "aPTT", "platelet count", "bleeding time"),
           ("What reverses unfractionated heparin?", "protamine sulfate", "vitamin K", "tranexamic acid", "naloxone"),
           ("What reverses warfarin?", "vitamin K (with clotting factor concentrate if urgent)", "protamine", "aspirin", "heparin"),
           ("What is the best-known serious adverse effect of statins?", "muscle injury (myopathy)", "dry cough", "gingival overgrowth", "hearing loss")],
         "Warfarin with INR and vitamin K; heparin with aPTT and protamine")]),
     ("D", H, "Classify cardiac drugs for arrhythmia, angina and heart failure.",
      "Vaughan Williams classes: I sodium channel blockers, II beta blockers, III potassium channel blockers (amiodarone), IV calcium channel blockers (verapamil, diltiazem). Nitrates relieve angina by venodilation through nitric oxide. Digoxin inhibits Na+/K+-ATPase.", "P2", [
       L("px-vaughan-williams", CV, "Which Vaughan Williams class? {{q}}", ["Class I", "Class II", "Class III", "Class IV"], [
           ("Lidocaine", 0), ("Metoprolol", 1), ("Amiodarone", 2), ("Verapamil", 3), ("Flecainide", 0), ("Sotalol, for its potassium channel block", 2), ("Diltiazem", 3)],
         "Sodium, beta, potassium, calcium: I to IV"),
       F("px-cardiac-drugs", CV, [
           ("How does glyceryl trinitrate relieve angina?", "it releases nitric oxide, dilating veins and reducing the heart's workload", "it blocks beta receptors", "it blocks calcium channels", "it inhibits ACE"),
           ("How does digoxin increase the force of contraction?", "it inhibits the Na+/K+-ATPase, raising intracellular calcium", "it stimulates beta-1 receptors", "it blocks potassium channels", "it opens calcium channels directly"),
           ("Which electrolyte disturbance increases the risk of digoxin toxicity?", "low potassium", "high potassium", "high sodium", "low chloride"),
           ("Why must nitrates not be combined with sildenafil?", "both raise cyclic GMP and together can cause severe hypotension", "they antagonise each other", "sildenafil blocks nitrate absorption", "the combination raises blood pressure")],
         "Reduce the heart's work, or change its rhythm, or strengthen its beat")])]),
 }),
 6: ("cns", "Central nervous system and pain", H, ["CLASS"], {
   1: ("Anaesthesia, mood and pain", [
     ("A", H, "Explain how local anaesthetics act and compute the amount in a cartridge.",
      "Local anaesthetics block voltage-gated sodium channels from inside the axon, in their charged form, after crossing the membrane uncharged; small pain fibres are blocked first. Amides (lidocaine, articaine, bupivacaine) are metabolised in the liver, esters by plasma esterases. A 1% solution contains 10 mg/mL.", "P1", [
       N("px-cartridge-mg", CN, "How many milligrams of drug are in a {{kv}} mL cartridge of {{kp}}% local anaesthetic solution?", "kp*10*kv", f"solve(Eq({M}/kv/10, kp), {M})[0]",
         "A 1% solution is 1 g in 100 mL, which is 10 mg per mL", tex="mg",
         cases=C("kv kp", [(1.7, 2), (1.8, 2), (1.7, 4), (1.8, 3), (1.7, 0.5)])),
       F("px-local-anaesthetic", CN, [
           ("Which channel do local anaesthetics block?", "voltage-gated sodium channels", "voltage-gated calcium channels", "GABA-A receptor channels", "potassium leak channels"),
           ("Why do local anaesthetics work poorly in inflamed tissue?", "the acidic tissue keeps more of the drug charged, so less crosses the nerve membrane", "blood flow is reduced", "sodium channels are absent", "the drug is destroyed by bacteria"),
           ("Which of these is an ester local anaesthetic?", "benzocaine", "lidocaine", "articaine", "bupivacaine"),
           ("Which is an early sign of systemic local anaesthetic toxicity?", "numbness around the mouth, ringing in the ears and light-headedness", "high blood pressure only", "gingival overgrowth", "dry cough")],
         "Amides have two letter i's in the name (lidocaine, prilocaine); esters have one")]),
     ("B", H, "Match central nervous system drug classes to their mechanisms.",
      "Benzodiazepines increase the frequency of GABA-A channel opening (reversed by flumazenil). SSRIs block serotonin reuptake. Typical antipsychotics block dopamine D2 receptors (movement disorders). Levodopa replaces dopamine in Parkinson disease. Many antiepileptics block sodium channels (phenytoin, carbamazepine).", "P2", [
       F("px-cns-mechanism", CN, [
           ("How do benzodiazepines act?", "they enhance GABA at the GABA-A receptor", "they block NMDA receptors", "they block dopamine D2 receptors", "they inhibit monoamine oxidase"),
           ("How do SSRIs act?", "they block the serotonin reuptake transporter", "they block serotonin receptors", "they release dopamine", "they inhibit acetylcholinesterase"),
           ("How do typical antipsychotics such as haloperidol act?", "they block dopamine D2 receptors", "they stimulate dopamine receptors", "they enhance GABA", "they block sodium channels"),
           ("How does phenytoin prevent seizures?", "it blocks voltage-gated sodium channels in rapidly firing neurons", "it enhances GABA by opening chloride channels directly", "it blocks dopamine receptors", "it inhibits serotonin reuptake")],
         "GABA up for sedation, dopamine down for psychosis, serotonin up for depression, sodium channels down for seizures"),
       F("px-cns-adverse", CN, [
           ("Which drug reverses benzodiazepine sedation?", "flumazenil", "naloxone", "atropine", "protamine"),
           ("Which antiepileptic is known for causing gingival overgrowth?", "phenytoin", "valproate", "levetiracetam", "lamotrigine"),
           ("Which adverse effects are typical of dopamine D2 blockade?", "movement disorders such as parkinsonism and tardive dyskinesia", "dry cough", "hearing loss", "low potassium"),
           ("Why is levodopa given with carbidopa?", "carbidopa blocks its conversion to dopamine outside the brain", "carbidopa is a dopamine agonist", "carbidopa blocks dopamine receptors", "carbidopa speeds its metabolism")],
         "Three drugs classically enlarge the gums: phenytoin, ciclosporin and the dihydropyridine calcium channel blockers")]),
     ("C", H, "Compare opioids, NSAIDs and paracetamol.",
      "Opioids act on mu receptors (analgesia, respiratory depression, constipation, pinpoint pupils; reversed by naloxone). NSAIDs inhibit cyclooxygenase, reducing prostaglandins (gastric irritation, kidney injury, bleeding). Paracetamol is analgesic and antipyretic with little anti-inflammatory action; overdose injures the liver and is treated with acetylcysteine.", "P2", [
       L("px-analgesic-class", CN, "Which analgesic class does this describe? {{q}}", ["Opioid", "NSAID", "Paracetamol (acetaminophen)"], [
           ("Reversed by naloxone", 0), ("Inhibits cyclooxygenase and can cause gastric ulcers", 1), ("Overdose causes liver injury, treated with acetylcysteine", 2),
           ("Causes constipation and pinpoint pupils", 0), ("Can reduce kidney blood flow and should be used with care in kidney disease", 1), ("Reduces fever with little anti-inflammatory effect", 2)],
         "Each has one signature toxicity: breathing, stomach and kidney, liver"),
       F("px-analgesic-mechanism", CN, [
           ("At which receptor does morphine mainly act for analgesia?", "mu opioid receptor", "kappa opioid receptor only", "NMDA receptor", "GABA-A receptor"),
           ("What is the most dangerous acute effect of an opioid overdose?", "respiratory depression", "constipation", "itching", "pupil constriction"),
           ("Why do NSAIDs irritate the stomach?", "they reduce the prostaglandins that protect the gastric lining", "they are strong acids that burn it directly and only so", "they increase mucus", "they block histamine receptors"),
           ("Which enzyme do selective COX-2 inhibitors spare, reducing gastric injury?", "COX-1", "COX-2", "lipoxygenase", "phospholipase A2")],
         "Prostaglandins hurt at the site of injury and protect in the stomach and kidney")]),
     ("D", H, "Interpret MAC for inhaled anaesthetics and name the intravenous agents.",
      "MAC is the alveolar concentration at which half of patients do not move to a surgical stimulus: a lower MAC means a more potent agent. Solubility in blood sets the speed of onset: a low blood-gas partition coefficient gives fast induction and recovery. Propofol is the usual intravenous induction agent; ketamine blocks NMDA receptors.", "P2", [
       L("px-mac", CN, "Agent A has a MAC of {{q}}. Which is more potent?", ["Agent A", "Agent B"], [
           ("2% and agent B a MAC of 6%", 0), ("105% and agent B a MAC of 1.2%", 1), ("0.75% and agent B a MAC of 2%", 0), ("6% and agent B a MAC of 1.2%", 1)],
         "Potency is the inverse of MAC"),
       F("px-anaesthetic-facts", CN, [
           ("An inhaled anaesthetic has a low blood-gas partition coefficient. What does that mean for induction?", "fast onset and fast recovery", "slow onset and slow recovery", "high potency", "no effect on speed"),
           ("Which intravenous anaesthetic acts mainly by blocking NMDA receptors?", "ketamine", "propofol", "midazolam", "thiopental"),
           ("Which inhaled agent has a MAC above 100% and so cannot produce surgical anaesthesia alone at normal pressure?", "nitrous oxide", "sevoflurane", "isoflurane", "desflurane"),
           ("On which receptor does propofol mainly act?", "GABA-A", "NMDA", "mu opioid", "nicotinic")],
         "Solubility sets speed; MAC sets potency")])]),
 }),
 7: ("antimicrobial", "Chemotherapy", H, ["CLASS"], {
   1: ("Drugs against microbes and tumours", [
     ("A", H, "Give the signature adverse effects and dosing pattern of antibacterial classes.",
      "Penicillins: allergy. Aminoglycosides: kidney and inner-ear toxicity, concentration-dependent killing. Tetracyclines: tooth discolouration in children, chelated by calcium and antacids. Fluoroquinolones: tendon injury. Macrolides: enzyme inhibition, QT prolongation. Beta-lactams kill in a time-dependent way.", "P2", [
       F("px-antibacterial-adverse", AM, [
           ("Which antibacterial class stains developing teeth and is avoided in young children and in pregnancy?", "tetracyclines", "penicillins", "macrolides", "aminoglycosides"),
           ("Which class is toxic to the kidney and the inner ear?", "aminoglycosides", "cephalosporins", "macrolides", "penicillins"),
           ("Which class is associated with tendon rupture?", "fluoroquinolones", "tetracyclines", "penicillins", "sulfonamides"),
           ("Which antibacterial is especially associated with Clostridioides difficile colitis and is used in dentistry for penicillin-allergic patients?", "clindamycin", "gentamicin", "nitrofurantoin", "vancomycin given by mouth")],
         "One signature hazard per class"),
       L("px-kill-pattern", AM, "Which measure best predicts this class's killing? {{q}}", ["Time above the minimum inhibitory concentration", "Peak concentration relative to the minimum inhibitory concentration"], [
           ("Penicillins", 0), ("Aminoglycosides", 1), ("Cephalosporins", 0), ("Fluoroquinolones, which are concentration-dependent", 1)],
         "Beta-lactams need time above the MIC; aminoglycosides need a high peak")]),
     ("B", H, "Match antifungal and antiviral drugs to their targets.",
      "Azoles inhibit ergosterol synthesis; polyenes (amphotericin B, nystatin) bind ergosterol and make pores; echinocandins inhibit cell-wall glucan synthesis. Aciclovir is activated by viral thymidine kinase and inhibits viral DNA polymerase; oseltamivir inhibits influenza neuraminidase.", "P2", [
       F("px-antifungal", AM, [
           ("How do azole antifungals such as fluconazole act?", "they inhibit ergosterol synthesis", "they bind ergosterol and form pores", "they inhibit glucan synthesis", "they inhibit DNA gyrase"),
           ("How does nystatin act?", "it binds ergosterol in the fungal membrane and forms pores", "it inhibits ergosterol synthesis", "it inhibits the fungal ribosome", "it blocks cell-wall chitin synthesis"),
           ("Why do azoles cause many drug interactions?", "they inhibit human cytochrome P450 enzymes", "they induce P450 enzymes", "they bind calcium in the gut", "they block renal secretion"),
           ("Which antifungal class inhibits cell-wall beta-glucan synthesis?", "echinocandins", "azoles", "polyenes", "allylamines")],
         "Ergosterol is the fungal difference that most antifungals exploit"),
       F("px-antiviral", AM, [
           ("Why is aciclovir selective for herpes-infected cells?", "it is activated by the viral thymidine kinase", "it cannot enter uninfected cells", "it binds only viral membranes", "it is destroyed in uninfected cells by acid"),
           ("What does oseltamivir inhibit?", "influenza neuraminidase", "reverse transcriptase", "viral protease", "viral DNA polymerase"),
           ("Which enzyme do nucleoside analogues such as zidovudine inhibit?", "reverse transcriptase", "neuraminidase", "integrase", "viral thymidine kinase"),
           ("Why are antiviral drugs fewer and narrower than antibacterial drugs?", "viruses use the host cell's machinery, leaving few selective targets", "viruses mutate too slowly", "viruses have thick cell walls", "viruses have their own ribosomes")],
         "Each antiviral targets a step the virus must do with its own enzyme")]),
     ("C", H, "State the principles of cancer chemotherapy and its common toxicities.",
      "Cytotoxic drugs kill a constant fraction of cells per dose and hit dividing cells hardest, so bone marrow, gut lining, hair follicles and oral mucosa suffer. Antimetabolites act in S phase, vinca alkaloids and taxanes in M phase; alkylating agents are not phase-specific. Signature toxicities: doxorubicin heart, cisplatin kidney, bleomycin lung, vincristine nerves.", "P2", [
       L("px-chemo-toxicity", AM, "Which organ is the signature site of toxicity? {{q}}", ["Heart", "Kidney", "Lung", "Peripheral nerves"], [
           ("Doxorubicin", 0), ("Cisplatin", 1), ("Bleomycin", 2), ("Vincristine", 3), ("Paclitaxel", 3)],
         "Each classic cytotoxic drug has an organ it is remembered for"),
       F("px-chemo-principles", AM, [
           ("Why do cytotoxic drugs commonly cause mouth ulcers, hair loss and low blood counts?", "these tissues have rapidly dividing cells", "these tissues have poor blood supply", "the drugs are excreted there", "these tissues lack DNA repair entirely"),
           ("How does methotrexate act?", "it inhibits dihydrofolate reductase", "it cross-links DNA", "it stabilises microtubules", "it inhibits topoisomerase II"),
           ("In which phase of the cell cycle do vinca alkaloids act?", "M phase, by preventing microtubule assembly", "S phase", "G1 phase", "G0 phase"),
           ("What does the log-kill hypothesis state?", "each dose kills a constant fraction of tumour cells, not a constant number", "each dose kills a constant number of cells", "tumour cells cannot become resistant", "one dose kills all dividing cells")],
         "Fractional kill is why chemotherapy is given in repeated cycles")])]),
 }),
 8: ("endocrine", "Endocrine and other systems", H, ["CLASS"], {
   1: ("Hormones, airways and gut", [
     ("A", H, "Match drugs for diabetes to their mechanisms and hazards.",
      "Metformin lowers hepatic glucose output (does not cause hypoglycaemia alone; rare lactic acidosis). Sulfonylureas close beta-cell potassium channels to release insulin (hypoglycaemia). SGLT2 inhibitors block renal glucose reabsorption (genital infection). GLP-1 agonists enhance glucose-dependent insulin release and slow gastric emptying. Insulin replaces the hormone.", "P2", [
       F("px-diabetes-mechanism", EN, [
           ("How does metformin lower blood glucose?", "mainly by reducing glucose production in the liver", "by releasing insulin from beta cells", "by blocking glucose reabsorption in the kidney", "by replacing insulin"),
           ("How do sulfonylureas act?", "they close ATP-sensitive potassium channels in beta cells, releasing insulin", "they block SGLT2", "they activate GLP-1 receptors", "they reduce hepatic glucose output"),
           ("How do SGLT2 inhibitors act?", "they block glucose reabsorption in the proximal tubule", "they release insulin", "they slow carbohydrate digestion", "they increase insulin sensitivity in fat"),
           ("How do GLP-1 receptor agonists act?", "they enhance glucose-dependent insulin release and slow gastric emptying", "they block glucagon receptors only", "they inhibit DPP-4", "they block SGLT2")],
         "Less glucose made, more insulin released, more glucose excreted, or insulin itself"),
       L("px-hypoglycaemia-risk", EN, "Used alone, does this drug commonly cause hypoglycaemia? {{q}}", ["Yes", "No"], [
           ("Insulin", 0), ("A sulfonylurea such as glipizide", 0), ("Metformin", 1), ("An SGLT2 inhibitor", 1), ("A DPP-4 inhibitor", 1)],
         "Drugs that add insulin regardless of the glucose level can drive it too low")]),
     ("B", H, "Describe corticosteroid and thyroid drug actions and hazards.",
      "Glucocorticoids suppress inflammation and immunity by changing gene transcription; long courses cause adrenal suppression (taper, never stop abruptly), osteoporosis, high glucose, infection risk and oral candidiasis with inhalers. Levothyroxine replaces T4; thionamides (carbimazole, propylthiouracil) block thyroid hormone synthesis.", "P2", [
       F("px-corticosteroid", EN, [
           ("Why must long-term oral corticosteroids be withdrawn gradually?", "the adrenal axis is suppressed and needs time to recover", "they are stored in fat", "they cause tolerance at the receptor only", "to avoid hypoglycaemia"),
           ("Which is an adverse effect of long-term glucocorticoid treatment?", "osteoporosis", "low blood glucose", "weight loss", "thicker skin"),
           ("What local adverse effect do inhaled corticosteroids cause in the mouth?", "candidiasis (thrush)", "gingival overgrowth", "tooth staining", "numbness"),
           ("Through what kind of receptor do glucocorticoids act?", "an intracellular receptor that alters gene transcription", "a G-protein-coupled membrane receptor", "a ligand-gated ion channel", "a receptor tyrosine kinase")],
         "Steroid courses are tapered because the patient's own cortisol production has been switched off"),
       F("px-thyroid", EN, [
           ("Which drug replaces thyroid hormone in hypothyroidism?", "levothyroxine", "carbimazole", "propranolol", "liothyronine is never used"),
           ("How do thionamides such as carbimazole act?", "they block thyroid hormone synthesis by inhibiting thyroid peroxidase", "they destroy the gland", "they block TSH receptors", "they block thyroid hormone receptors"),
           ("Which rare but serious adverse effect of thionamides must patients be warned about?", "a fall in white cells (agranulocytosis), signalled by sore throat or fever", "hearing loss", "tendon rupture", "gingival overgrowth"),
           ("Which drug class relieves the tremor and fast heart rate of hyperthyroidism while definitive treatment takes effect?", "beta blockers", "ACE inhibitors", "statins", "loop diuretics")],
         "Replace what is missing, or block what is in excess")]),
     ("C", H, "Match respiratory and gastrointestinal drugs to their mechanisms.",
      "Beta-2 agonists and antimuscarinics dilate the bronchi; inhaled corticosteroids control airway inflammation; leukotriene antagonists block one inflammatory pathway. Proton pump inhibitors irreversibly block the H+/K+-ATPase; H2 antagonists block histamine on the parietal cell; antacids neutralise acid already secreted.", "P2", [
       L("px-asthma-role", EN, "Reliever (bronchodilator) or controller (anti-inflammatory)? {{q}}", ["Reliever", "Controller"], [
           ("Salbutamol", 0), ("Inhaled beclometasone", 1), ("Ipratropium", 0), ("Montelukast", 1), ("Inhaled budesonide", 1)],
         "Relievers open the airway now; controllers reduce the inflammation that narrows it"),
       F("px-acid-drugs", EN, [
           ("How does omeprazole reduce gastric acid?", "it irreversibly inhibits the parietal cell's H+/K+-ATPase", "it blocks H2 receptors", "it neutralises acid", "it blocks muscarinic receptors"),
           ("How does famotidine reduce gastric acid?", "it blocks histamine H2 receptors on parietal cells", "it inhibits the proton pump", "it neutralises acid", "it coats the ulcer"),
           ("Which class of acid-reducing drug gives the strongest suppression?", "proton pump inhibitors", "H2 antagonists", "antacids", "alginates"),
           ("Why do antacids reduce the absorption of tetracyclines and fluoroquinolones?", "their metal ions chelate the drug in the gut", "they raise blood flow", "they induce P450 enzymes", "they speed gastric emptying only")],
         "Block the pump, block one of its signals, or mop up what it has made")])]),
 }),
})
ADD = [(f"{FW['code']}-{n}.{tn}.{lo[0]}", qq) for n, u in UNITS.items() for tn, (tt, los) in u[4].items() for lo in los for qq in lo[5]]
