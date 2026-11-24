"""Second question types for INBDE (DN). Recall objectives get a second angle (scenario, treatment choice or a
different view of the same fact); calculation objectives get a reverse or related calculation. Entry-level content only;
Kevin checks dental content."""
from opl_dsl import Q

FILE, FRAMEWORK = "dn-second-types", "inbde"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]


def facts(name, skill, rows, explain, prompt="{{q}}"):
    return Q(name, skill, prompt, pace="recall", cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


DX, MG, PR, MAT, AN, BM, PH, CL, BH = ("dent.diagnosis", "dent.management", "dent.practice", "dent.materials", "dent.anatomy",
                                         "dent.biomed", "dent.pharm", "dent.clinical", "dent.behavior")

ADD = [
    ("DN-1.1.B", facts("dn-dentition-counts", DX, [
        ("How many permanent teeth replace primary teeth (succedaneous teeth)?", "20", "32", "12", "28"),
        ("Which permanent teeth have no primary predecessor?", "The molars", "The premolars", "The canines", "The incisors"),
        ("A child of 8 typically has which dentition?", "Mixed: permanent first molars and incisors with primary canines and molars", "Primary only", "Permanent only", "No erupted teeth"),
    ], "Permanent premolars replace primary molars; permanent molars erupt behind the primary dentition")),
    ("DN-1.2.A", facts("dn-black-class-more", DX, [
        ("A lesion in the buccal pit of a mandibular molar is which class?", "Class I", "Class II", "Class V", "Class VI"),
        ("A lesion in the gingival third of the facial surface of a premolar is which class?", "Class V", "Class I", "Class III", "Class VI"),
        ("A lesion on the cusp tip of a canine is which class?", "Class VI", "Class IV", "Class III", "Class I"),
    ], "Class I pits and fissures (including buccal and lingual pits); V gingival third; VI incisal edges and cusp tips")),
    ("DN-1.2.B", facts("dn-pulp-treatment", DX, [
        ("Which treatment fits reversible pulpitis?", "Remove the cause (caries) and restore", "Root canal treatment", "Extraction", "Antibiotics alone"),
        ("Which treatment fits symptomatic irreversible pulpitis in a restorable tooth?", "Root canal treatment (pulpectomy)", "A sedative filling and nothing more", "Antibiotics alone", "No treatment"),
        ("Which treatment fits pulp necrosis in a restorable tooth?", "Root canal treatment", "Pulp capping", "Desensitising toothpaste", "Observation only"),
    ], "The diagnosis decides whether the pulp can be kept: reversible, keep; irreversible or necrotic, remove")),
    ("DN-1.3.A", facts("dn-slob-scenario", DX, [
        ("The tube is shifted mesially and the object moves distally relative to the teeth. Where is it?", "Buccal", "Lingual", "In the pulp", "Cannot be told"),
        ("The tube is shifted distally and the object also moves distally. Where is it?", "Lingual", "Buccal", "Apical", "Coronal"),
        ("Teeth appear foreshortened on a periapical. What is the error?", "Too much vertical angulation", "Too little vertical angulation", "Wrong horizontal angulation", "Cone cut"),
    ], "Same Lingual, Opposite Buccal; elongation means too little vertical angulation, foreshortening too much")),
    ("DN-2.1.A", facts("dn-emergency-more", MG, [
        ("A patient with known angina has chest pain in the chair. What is the first drug?", "Nitroglycerin 0.4 mg sublingual", "Epinephrine IM", "Glucose", "Albuterol"),
        ("An asthmatic patient is wheezing. What is the first drug?", "Inhaled albuterol (short-acting β₂ agonist)", "Nitroglycerin", "Diphenhydramine", "Aspirin"),
        ("Chest pain not relieved by nitroglycerin suggests a heart attack. Which drug do you give while calling for help?", "Aspirin 162–325 mg, chewed (if not allergic)", "More local anesthetic", "Glucose", "Albuterol"),
        ("An unconscious diabetic patient cannot swallow. What is given for suspected hypoglycemia?", "Glucagon 1 mg IM (or IV dextrose)", "Oral glucose", "Insulin", "Nitroglycerin"),
    ], "Match the emergency, then give the first drug while activating emergency services")),
    ("DN-2.1.B", facts("dn-prophylaxis-regimen", MG, [
        ("What is the usual adult oral regimen for endocarditis prophylaxis (AHA 2021)?", "Amoxicillin 2 g, 30–60 min before the procedure", "Amoxicillin 500 mg for 7 days", "Penicillin VK 250 mg after the procedure", "Clindamycin 600 mg (now the first choice)"),
        ("Which dental procedures call for prophylaxis in a high-risk patient?", "Those manipulating gingiva or the periapical region, or perforating mucosa", "Only extractions", "Radiographs", "Routine anesthetic injections through healthy tissue"),
        ("If the dose was not given before the procedure, when may it still be given?", "Up to 2 hours after the procedure", "Never", "The next day", "Only intravenously before"),
    ], "AHA 2021 removed clindamycin from the list; amoxicillin 2 g remains the standard")),
    ("DN-2.2.B", Q("dn-lidocaine-cartridges", MG, "Using a maximum dose of 7 mg/kg (not over 500 mg) for 2% lidocaine with epinephrine, how many full 1.8 mL cartridges may a {{kg}} kg patient receive?",
        given={"kg": {"pick": [20, 30, 50, 70, 90]}}, value="floor(min(7*kg, 500)/36)", tex="N", final=True,
        verify="floor(Min(7*kg, 500)/(Rational(2, 100)*1000*Rational(18, 10)))", explain="2% is 20 mg/mL, so a 1.8 mL cartridge holds 36 mg; children reach the limit after very few")),
    ("DN-3.2.A", Q("dn-ppv-prevalence", PR, "A test has sensitivity {{se}}% and specificity {{sp}}%. In a population where {{p}}% have the disease, what is the positive predictive value, in %?",
        given={"se": {"pick": [80, 90, 95]}, "sp": {"pick": [85, 90, 99]}, "p": {"pick": [1, 10, 30]}}, value="100*se*p/(se*p + (100 - sp)*(100 - p))", tex="PPV",
        verify="100*(Rational(se, 100)*Rational(p, 100))/(Rational(se, 100)*Rational(p, 100) + (1 - Rational(sp, 100))*(1 - Rational(p, 100)))",
        explain="Bayes' rule: the same test has a much lower PPV when the disease is rare")),
    ("DN-4.1.B", Q("dn-flexural-load", MAT, "A composite bar ({{b}} mm wide, {{h}} mm high) is tested in three-point bending over a {{L}} mm span. At what load, in N, will it fracture if its flexural strength is {{s}} MPa?",
        given={"b": {"pick": [2]}, "h": {"pick": [2]}, "L": {"pick": [20]}, "s": {"pick": [80, 120, 150]}}, value="2*s*b*h^2/(3*L)", tex="F",
        verify="solve(Eq(3*x*L/(2*b*h**2), s), x)[0]", explain="σ = 3FL/2bh²: double the height and the bar carries four times the load")),
    ("DN-4.2.B", facts("dn-composite-choice", MAT, [
        ("Raising filler content in a composite does what to polymerisation shrinkage?", "Lowers it (less resin to shrink)", "Raises it", "No change", "Eliminates it"),
        ("Why is a flowable composite used as a liner in a deep box?", "Its low viscosity adapts to the cavity floor", "It is the strongest", "It shrinks least", "It needs no light"),
        ("Which property rises with filler content?", "Elastic modulus and wear resistance", "Shrinkage", "Water sorption", "Thermal expansion"),
    ], "Filler replaces resin, so it stiffens the material and cuts shrinkage, expansion and water uptake")),
    ("DN-4.3.A", Q("dn-temperature-for-gap", MAT, "Tooth expands 11.4 ppm/°C and {{mat}} {{a1}} ppm/°C. Across a {{L}} mm restoration, what temperature change opens a {{g}} μm mismatch?",
        cases=[{"mat": "amalgam", "a1": 25}, {"mat": "a composite", "a1": 35}, {"mat": "an unfilled resin", "a1": 80}], given={"L": {"pick": [4, 8]}, "g": {"pick": [2, 5]}},
        value="g/((a1 - 11.4)*1e-6*L*1000)", tex="\\Delta T", verify="solve(Eq((nsimplify(a1) - Rational(114, 10))/10**6*L*1000*x, g), x)[0]",
        explain="Hot and cold drinks swing 50 °C or more; a large expansion mismatch pumps fluid along the margin (percolation)")),
    ("DN-4.4.A", facts("dn-cement-choice", MAT, [
        ("Which material releases fluoride and bonds chemically to tooth, suiting a high-caries cervical lesion?", "Glass ionomer", "Amalgam", "Zinc phosphate", "ZOE"),
        ("Why must a ZOE base not go under a composite?", "Eugenol inhibits resin polymerisation", "It is too acidic", "It is radiolucent", "It sets too fast"),
        ("Why is zinc phosphate mixed slowly on a cool slab?", "To control its heat of reaction and give working time", "To raise its pH faster", "To add fluoride", "To make it adhesive"),
    ], "Choose by what the site needs: fluoride and adhesion, sedation, or strength")),
    ("DN-4.4.B", facts("dn-ceramic-why", MAT, [
        ("Why does hydrofluoric acid etch lithium disilicate but not zirconia?", "HF dissolves the glass phase, and zirconia has none", "Zirconia is too soft", "HF damages zirconia", "Zirconia is a metal"),
        ("What does a silane coupling agent do on etched glass ceramic?", "Bonds chemically to the silica and to the resin cement", "Etches the surface", "Seals the dentin", "Hardens the ceramic"),
        ("Which primer chemistry bonds resin cement to zirconia?", "MDP (phosphate monomer)", "Silane alone", "Phosphoric acid", "Hydrofluoric acid"),
    ], "Glass ceramics: HF then silane; zirconia: air abrasion then an MDP primer")),
    ("DN-4.5.A", Q("dn-noble-total", MAT, "An alloy contains {{comp}}. What is its total noble-metal content (Au + Pt-group metals), in %?",
        cases=[{"comp": "Au 75%, Pd 3%, Ag 10%, Cu 12%", "au": 75, "pd": 3, "pt": 0}, {"comp": "Pd 60%, Ag 30%, Sn and others 10%", "au": 0, "pd": 60, "pt": 0},
               {"comp": "Au 50%, Pd 30%, Ag 10%, others 10%", "au": 50, "pd": 30, "pt": 0}, {"comp": "Au 40%, Pt 5%, Pd 20%, Ag 25%, Cu 10%", "au": 40, "pd": 20, "pt": 5}],
        value="au + pd + pt", tex="\\%_{noble}", verify="100 - (100 - au - pd - pt)",
        explain="Silver is not a noble metal in the ADA scheme: high noble ≥ 60% noble with ≥ 40% gold; noble ≥ 25%; predominantly base below 25%")),
    ("DN-5.1.A", facts("dn-canal-counts", AN, [
        ("How many canals does a mandibular first molar most often have?", "3 (mesiobuccal, mesiolingual, distal), sometimes 4", "1", "2", "5"),
        ("Which root of the maxillary first molar often hides a second canal (MB2)?", "Mesiobuccal", "Distobuccal", "Palatal", "None"),
        ("Which tooth usually has two canals in one or two roots?", "Maxillary first premolar", "Maxillary central incisor", "Maxillary canine", "Mandibular second premolar"),
    ], "Missed canals (MB2, a second distal or a second mandibular incisor canal) are a common cause of failure")),
    ("DN-5.1.B", facts("dn-identify-tooth", AN, [
        ("A premolar crown has a mesial concavity and a mesial marginal groove. Which tooth?", "Maxillary first premolar", "Mandibular first premolar", "Maxillary second premolar", "Mandibular second premolar"),
        ("A premolar has a large buccal cusp, a tiny lingual cusp and a mesiolingual groove. Which tooth?", "Mandibular first premolar", "Maxillary first premolar", "Mandibular second premolar", "Maxillary second premolar"),
        ("Which tooth most often has a lingual pit and may be peg-shaped?", "Maxillary lateral incisor", "Mandibular central incisor", "Maxillary canine", "Mandibular lateral incisor"),
    ], "Small features (grooves, concavities, cusp proportions) separate teeth that look alike")),
    ("DN-5.1.C", facts("dn-canine-relation", AN, [
        ("In Class I canine relation, where does the maxillary canine sit?", "In the embrasure between the mandibular canine and first premolar", "Directly over the mandibular canine", "Between the mandibular premolars", "Lingual to the mandibular canine"),
        ("The maxillary canine sits mesial to that embrasure. What canine relation is that?", "Class II", "Class I", "Class III", "Normal"),
        ("Which Angle class often comes with an anterior crossbite?", "Class III", "Class I", "Class II division 1", "Class II division 2"),
    ], "Canine relation is read alongside the molar relation, the basis of Angle's classes")),
    ("DN-5.1.D", Q("dn-root-needed", AN, "An abutment's clinical crown measures {{c}} mm. How much root, in mm, must remain in bone for a crown-to-root ratio of 1:{{r}}?",
        given={"c": {"pick": [8, 10, 12]}, "r": {"pick": [1, 1.5, 2]}}, value="c*r", tex="L_{root}", verify="solve(Eq(c/x, 1/nsimplify(r)), x)[0]",
        explain="1:1.5 is a good ratio, 1:1 the usual minimum for an abutment; bone loss lengthens the crown and shortens the root")),
    ("DN-6.1.A", facts("dn-block-coverage", AN, [
        ("Which block anaesthetises the palatal tissue from the canine forward?", "Nasopalatine", "Greater palatine", "PSA", "Infraorbital"),
        ("Which block anaesthetises palatal tissue posterior to the canine on one side?", "Greater palatine", "Nasopalatine", "Mental", "Buccal"),
        ("The IANB does not anaesthetise the buccal gingiva of mandibular molars. Which nerve needs its own block?", "Long buccal nerve", "Lingual nerve", "Mental nerve", "Mylohyoid nerve"),
    ], "Know which nerve carries each area to know which block covers it")),
    ("DN-6.1.B", facts("dn-muscle-movement", AN, [
        ("Which three muscles close the jaw?", "Masseter, temporalis and medial pterygoid", "Lateral pterygoid, digastric and mylohyoid", "Buccinator, orbicularis oris and mentalis", "Digastric and geniohyoid only"),
        ("The mandible deviates to the left on protrusion. Which lateral pterygoid is weak or not working?", "The left (the right pulls the jaw toward the left)", "The right", "Both", "Neither: the masseter is at fault"),
        ("Which muscle pulls the condyle forward when the mouth opens wide?", "Lateral pterygoid", "Masseter", "Temporalis", "Medial pterygoid"),
    ], "Elevators close; the lateral pterygoids protrude and open; one side contracting swings the jaw to the other")),
    ("DN-6.1.C", facts("dn-landmark-locate", AN, [
        ("Where is the mental foramen usually found?", "Below the apices of the mandibular premolars", "Below the first molar's distal root", "At the midline", "Behind the third molar"),
        ("Which landmark covers the nasopalatine (incisive) foramen?", "The incisive papilla", "The palatine raphe only", "The fovea palatini", "The hamular notch"),
        ("Where is the infraorbital foramen in relation to the eye?", "About 1 cm below the infraorbital rim", "Above the eyebrow", "At the angle of the mandible", "Beside the nose tip"),
    ], "Foramina mark where nerves emerge and where blocks are given")),
    ("DN-6.1.D", facts("dn-vessel-risk", AN, [
        ("A PSA injection given too deep causes a rapid swelling. Which vessels are usually hit?", "The pterygoid venous plexus", "The facial artery", "The lingual artery", "The carotid"),
        ("Which artery supplies the hard palate posterior to the canine?", "Greater palatine (from the maxillary artery)", "Lingual", "Facial", "Superior labial"),
        ("Why can dental infections spread to the cavernous sinus?", "Valveless facial and pterygoid veins connect to it", "Arteries carry pus upward", "Lymph drains there", "They cannot"),
    ], "Venous connections without valves are why upper-face infections can spread intracranially")),
    ("DN-7.1.A", facts("dn-supporting-origin", AN, [
        ("Which structure gives rise to cementum, PDL and alveolar bone lining the socket?", "The dental follicle (sac)", "The enamel organ", "The dental papilla", "The oral epithelium"),
        ("Which structure becomes the pulp?", "The dental papilla", "The dental follicle", "The enamel organ", "Hertwig's root sheath"),
        ("Remnants of Hertwig's root sheath in the PDL are called what?", "Rests of Malassez", "Rests of Serres", "Reduced enamel epithelium", "Odontoblasts"),
    ], "Enamel organ → enamel; papilla → dentin and pulp; follicle → cementum, PDL and bone")),
    ("DN-7.1.B", facts("dn-anomaly-shape", AN, [
        ("Two teeth joined by cementum only, after root formation. What is it?", "Concrescence", "Fusion", "Gemination", "Dilaceration"),
        ("A tooth with an enlarged pulp chamber and short roots (bull-like). What is it?", "Taurodontism", "Dens in dente", "Dilaceration", "Concrescence"),
        ("An invagination of enamel into the crown, most often in maxillary lateral incisors. What is it?", "Dens invaginatus (dens in dente)", "Dens evaginatus", "Taurodontism", "Enamel pearl"),
    ], "Fusion joins two tooth germs (count drops); gemination splits one (count normal)")),
    ("DN-7.1.C", facts("dn-cleft-timing", AN, [
        ("When in development does the lip normally fuse?", "Around weeks 4–7", "Around weeks 12–16", "After birth", "In the first week"),
        ("When do the palatal shelves normally fuse?", "Around weeks 8–12", "Around weeks 4–5", "In the third trimester", "After birth"),
        ("Which drug taken in early pregnancy is linked to orofacial clefts?", "Phenytoin (and some other anticonvulsants)", "Acetaminophen", "Penicillin", "Folic acid"),
    ], "Clefts reflect failed fusion during these windows; folic acid lowers the risk")),
    ("DN-8.1.A", Q("dn-acetaminophen-tablets", PH, "A patient's acetaminophen ceiling is {{lim}} g a day. How many {{mg}} mg tablets is that at most?",
        given={"lim": {"pick": [3, 4]}, "mg": {"pick": [325, 500]}}, value="floor(lim*1000/mg)", tex="N", final=True,
        verify="floor(Rational(lim*1000, mg))", explain="Count acetaminophen in combination products too; 3 g is the usual lower ceiling with liver disease or alcohol use")),
    ("DN-8.1.B", facts("dn-antibiotic-risks", PH, [
        ("Which antibiotic most raises the risk of C. difficile colitis?", "Clindamycin", "Amoxicillin", "Penicillin VK", "Metronidazole"),
        ("Why is amoxicillin–clavulanate chosen over amoxicillin?", "Clavulanate blocks β-lactamases of resistant bacteria", "It is stronger against viruses", "It is cheaper", "It has no side effects"),
        ("Below what age are tetracyclines usually avoided?", "8 years", "18 years", "2 years", "65 years"),
    ], "Choose for the organism and the patient: allergy, age, gut flora")),
    ("DN-8.1.C", facts("dn-interaction-scenarios", PH, [
        ("A patient on warfarin is prescribed metronidazole. What happens to the INR?", "It rises: bleeding risk increases", "It falls", "No change", "Warfarin stops working"),
        ("Why limit epinephrine in a patient on a tricyclic antidepressant?", "The pressor effect is enhanced", "Tricyclics block local anaesthetics", "Epinephrine stops the antidepressant", "There is no reason"),
        ("A patient on oral bisphosphonates for osteoporosis for 2 years needs an extraction. What is the usual stance?", "Proceed with care: the MRONJ risk is low but should be discussed", "Never extract", "Stop the drug for a year first", "No consent needed"),
    ], "Interactions change dosing, timing or consent, rarely whether to treat at all")),
    ("DN-8.1.D", Q("dn-suspension-volume", PH, "A child of {{kg}} kg needs amoxicillin 50 mg/kg (not over 2 g) as suspension containing {{c}} mg/5 mL. What volume, in mL?",
        given={"kg": {"pick": [10, 15, 20, 45]}, "c": {"pick": [250, 400]}}, value="min(50*kg, 2000)/c*5", tex="V",
        verify="Min(50*kg, 2000)*5/nsimplify(c)", explain="Dose first, capped at the adult dose; then convert with the concentration")),
    ("DN-8.1.E", Q("dn-time-to-fraction", PH, "A drug has a half-life of {{h}} h. How long until only {{f}}% of a dose remains, in h?",
        given={"h": {"pick": [2, 4, 6]}, "f": {"pick": [50, 25, 12.5, 6.25]}}, value="h*log(100/f)/log(2)", tex="t",
        verify="nsimplify(h)*log(100/nsimplify(f), 2)", explain="About 4–5 half-lives clear most of a drug and set the time to steady state")),
    ("DN-9.1.A", facts("dn-organism-lesion", BM, [
        ("Recurrent cold sores on the lip are usually caused by what?", "Herpes simplex virus 1", "Coxsackievirus A16", "Candida albicans", "Varicella-zoster virus"),
        ("White plaques that wipe off to leave a red base suggest which organism?", "Candida albicans", "Streptococcus mutans", "HPV", "Treponema pallidum"),
        ("Hand, foot and mouth disease is caused by what?", "Coxsackievirus A16 (enteroviruses)", "HSV-1", "Epstein–Barr virus", "Candida"),
    ], "Many oral lesions point to one organism")),
    ("DN-9.1.B", Q("dn-exposure-expected", PR, "Average per-exposure transmission risks after a needlestick from a positive source are about {{r}}% for {{v}}. In {{n}} such exposures, how many infections are expected?",
        cases=[{"v": "HBV (HBeAg-positive, unvaccinated worker)", "r": 30}, {"v": "HCV", "r": 1.8}, {"v": "HIV", "r": 0.3}], given={"n": {"pick": [100, 1000]}},
        value="n*r/100", tex="E", verify="n*nsimplify(r)/100", explain="Risk ranks HBV ≫ HCV > HIV, which is why the HBV vaccine matters most")),
    ("DN-9.1.C", facts("dn-hypersensitivity-more", BM, [
        ("Autoantibodies against desmosomes in pemphigus vulgaris are which hypersensitivity type?", "Type II (antibody against tissue)", "Type I", "Type III", "Type IV"),
        ("Immune complexes depositing in vessel walls cause which type?", "Type III", "Type I", "Type II", "Type IV"),
        ("A nickel allergy rash under an orthodontic appliance is which type?", "Type IV (delayed, T-cell)", "Type I", "Type II", "Type III"),
    ], "I IgE; II antibody to cells or tissue; III immune complexes; IV T cells")),
    ("DN-10.1.A", facts("dn-lesion-site", BM, [
        ("A painless, smooth, firm nodule on the buccal mucosa along the bite line. What is it most likely?", "Irritation fibroma", "Mucocele", "Ranula", "Pyogenic granuloma"),
        ("A bluish, fluctuant swelling on the lower lip after biting it. What is it?", "Mucocele", "Fibroma", "Hemangioma only", "Ranula"),
        ("A red, bleeding gingival growth in a pregnant patient. What is it?", "Pyogenic granuloma", "Fibroma", "Mucocele", "Squamous cell carcinoma"),
    ], "Site, colour and history narrow a soft-tissue lesion quickly")),
    ("DN-10.1.B", facts("dn-cancer-site-risk", BM, [
        ("Which red lesion carries the highest risk of dysplasia or carcinoma?", "Erythroplakia", "Leukoplakia", "Linea alba", "Fordyce granules"),
        ("Which site is a high-risk location for oral squamous cell carcinoma?", "Ventrolateral tongue and floor of mouth", "Hard palate", "Dorsal tongue", "Attached gingiva of incisors"),
        ("A white lesion that does not wipe off and has no clear cause. What is the next step?", "Biopsy", "Reassure and discharge", "Antifungals only", "Wait five years"),
    ], "Red is riskier than white; unexplained persistent lesions get a biopsy")),
    ("DN-10.1.C", facts("dn-jaw-lesion-more", BM, [
        ("A multilocular radiolucency in the posterior mandible of an adult. Which lesion is classic?", "Ameloblastoma", "Periapical granuloma", "Torus", "Condensing osteitis"),
        ("Periapical radiolucencies at vital mandibular incisors in a middle-aged woman. What is likely?", "Cemento-osseous dysplasia", "Periapical abscess", "Ameloblastoma", "Osteosarcoma"),
        ("A radiolucency around the crown of an unerupted tooth, attached at the CEJ. What is likely?", "Dentigerous cyst", "Radicular cyst", "Lateral periodontal cyst", "Stafne defect"),
    ], "Test pulp vitality before treating a periapical radiolucency")),
    ("DN-10.1.D", facts("dn-blister-test", BM, [
        ("Gentle rubbing of normal mucosa produces a blister (positive Nikolsky). Which disease is likely?", "Pemphigus vulgaris", "Lichen planus", "Aphthous ulcer", "Candidiasis"),
        ("Where does the split occur in mucous membrane pemphigoid?", "Below the epithelium (subepithelial)", "Within the epithelium", "In the dermis only", "In bone"),
        ("Target lesions on the skin with crusted lips after a drug or herpes infection suggest what?", "Erythema multiforme", "Pemphigus", "Pemphigoid", "Lichen planus"),
    ], "Intraepithelial split: pemphigus; subepithelial: pemphigoid; targets: erythema multiforme")),
    ("DN-11.1.A", facts("dn-kennedy-more", CL, [
        ("A mandibular arch is missing all posterior teeth on both sides, plus one incisor. Which Kennedy class?", "Class I, modification 1", "Class IV", "Class II", "Class III, modification 1"),
        ("One side has a free-end posterior space; the other side is intact. Which class?", "Class II", "Class I", "Class III", "Class IV"),
        ("A single bounded space crossing the midline, all posterior teeth present. Which class?", "Class IV", "Class III", "Class I", "Class II"),
        ("A single bounded posterior space with teeth on both ends. Which class?", "Class III", "Class II", "Class IV", "Class I"),
    ], "The most posterior edentulous area sets the class; others are modifications; Class IV has none")),
    ("DN-11.1.B", facts("dn-space-maintainer", CL, [
        ("A primary first molar is lost early on one side. Which space maintainer fits?", "Band and loop", "Distal shoe", "Lower lingual holding arch", "None ever"),
        ("A primary second molar is lost before the permanent first molar erupts. Which appliance guides the molar?", "Distal shoe", "Band and loop", "Nance appliance", "Retainer"),
        ("Primary molars are lost on both sides of the mandible after the permanent incisors erupt. Which appliance?", "Lower lingual holding arch", "Band and loop on each side", "Distal shoe", "Complete denture"),
    ], "Choose by which tooth is lost, how many, and whether the guiding teeth have erupted")),
    ("DN-11.1.C", facts("dn-surgery-complication", CL, [
        ("Severe throbbing pain 2–4 days after a mandibular molar extraction, with an empty socket. What is it?", "Alveolar osteitis (dry socket)", "Infection always needing antibiotics", "Normal healing", "Nerve injury"),
        ("How is a dry socket usually managed?", "Gentle irrigation and a medicated dressing, with analgesics", "Re-extraction", "Antibiotics alone", "Suturing the socket shut"),
        ("Numbness of the lower lip after a third molar extraction suggests injury to which nerve?", "Inferior alveolar", "Lingual", "Facial", "Buccal"),
    ], "Dry socket is a clot problem, not usually an infection")),
    ("DN-11.1.D", facts("dn-periapical-findings", CL, [
        ("A sinus tract draining near a nonvital tooth, with little pain. Which diagnosis?", "Chronic apical abscess", "Symptomatic apical periodontitis", "Acute apical abscess", "Normal apical tissues"),
        ("A diffuse radiopacity around the apex of a tooth with chronic pulpitis. Which diagnosis?", "Condensing osteitis", "Ameloblastoma", "Periapical cyst", "Acute apical abscess"),
        ("Rapid-onset swelling and pain over a necrotic tooth. Which diagnosis?", "Acute apical abscess", "Chronic apical abscess", "Asymptomatic apical periodontitis", "Reversible pulpitis"),
    ], "Pain, swelling, sinus tracts and radiographic change separate the apical diagnoses")),
    ("DN-12.1.A", Q("dn-bp-category", CL, "A patient's blood pressure is {{s}}/{{d}} mmHg. Which AHA (2017) category is it?",
        given={"s": {"pick": [115, 125, 135, 150, 185]}, "d": {"pick": [75, 85, 95, 125]}},
        choice=["Normal", "Elevated", "Stage 1 hypertension", "Stage 2 hypertension", "Hypertensive crisis"],
        correct="(s > 180 or d > 120) ? 4 : ((s >= 140 or d >= 90) ? 3 : ((s >= 130 or d >= 80) ? 2 : (s >= 120 ? 1 : 0)))",
        verify="4 if (s > 180 or d > 120) else (3 if (s >= 140 or d >= 90) else (2 if (s >= 130 or d >= 80) else (1 if s >= 120 else 0)))",
        explain="The higher of the two numbers decides the category; a crisis needs immediate medical referral")),
    ("DN-12.1.B", Q("dn-epi-child-dose", CL, "Anaphylaxis in a child of {{kg}} kg: epinephrine 0.01 mg/kg IM, not over 0.3 mg, from a 1 mg/mL ampule. What volume, in mL?",
        given={"kg": {"pick": [10, 15, 20, 25, 40]}}, value="min(0.01*kg, 0.3)", tex="V", verify="Min(kg*Rational(1, 100), Rational(3, 10))/1",
        explain="Children get 0.01 mg/kg up to the 0.3 mg adult auto-injector dose; 1 mg/mL means mg and mL are equal")),
    ("DN-12.1.C", Q("dn-anc", CL, "A patient's white count is {{w}} × 10³/μL with {{n}}% neutrophils and {{b}}% bands. What is the absolute neutrophil count, per μL?",
        given={"w": {"pick": [2.5, 4, 7]}, "n": {"pick": [20, 40, 60]}, "b": {"pick": [0, 3, 5]}}, value="w*1000*(n + b)/100", tex="ANC",
        verify="nsimplify(w)*1000*Rational(n, 100) + nsimplify(w)*1000*Rational(b, 100)", explain="Below about 1000/μL, elective surgery is usually deferred because of infection risk")),
    ("DN-13.1.A", facts("dn-ethics-principle", BH, [
        ("A dentist explains all treatment options, including no treatment, and lets the patient choose. Which principle?", "Patient autonomy", "Justice", "Veracity", "Nonmaleficence"),
        ("A dentist refers a case beyond their skill. Which principle?", "Nonmaleficence (do no harm)", "Justice", "Autonomy", "Veracity"),
        ("A dentist does not refuse a patient because of HIV status. Which principle?", "Justice", "Beneficence", "Veracity", "Autonomy"),
        ("A dentist tells a patient about a broken file left in a canal. Which principle?", "Veracity", "Justice", "Autonomy", "Beneficence"),
    ], "The ADA Code rests on autonomy, nonmaleficence, beneficence, justice and veracity")),
    ("DN-13.1.B", facts("dn-consent-scenario", BH, [
        ("Which is required for informed consent?", "Diagnosis, proposed treatment, risks, benefits and alternatives (including none)", "Only the patient's signature", "Only the fee", "Only the risks"),
        ("Who consents for treatment of a 10-year-old (not emancipated)?", "A parent or legal guardian", "The child alone", "The dentist", "The school nurse"),
        ("A dentist suspects child abuse. What must they do?", "Report it to the authorities, as a mandated reporter", "Wait for proof", "Tell the parents only", "Nothing without consent"),
    ], "Consent needs information and capacity; abuse reporting is required by law")),
    ("DN-13.1.D", Q("dn-nnt-sealant", PR, "A sealant programme lowers the risk of a carious lesion over three years from {{c}}% to {{t}}%. How many children must be treated to prevent one lesion (NNT)?",
        given={"c": {"pick": [40, 30, 20]}, "t": {"pick": [10, 5]}}, value="ceil(100/(c - t))", tex="NNT", final=True,
        verify="ceiling(1/(Rational(c, 100) - Rational(t, 100)))", explain="NNT = 1/ARR, rounded up; a big relative reduction can still mean a large NNT when the event is rare")),
    ("DN-13.1.E", Q("dn-naf-fluoride", PR, "How many mg of fluoride ion does a {{m}} mg sodium fluoride tablet deliver? (Na 22.99, F 19.00)",
        given={"m": {"pick": [0.55, 1.1, 2.2]}}, value="m*19.00/(22.99 + 19.00)", tex="m_F",
        verify="nsimplify(m)*Rational(1900, 100)/(Rational(2299, 100) + Rational(1900, 100))", explain="Fluoride is about 45% of NaF by mass: a 2.2 mg tablet gives 1.0 mg F⁻, the supplement dose for ages 6–16 in low-fluoride areas")),
]
