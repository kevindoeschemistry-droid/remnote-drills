"""INBDE depth (framework inbde, DN): the Foundation Knowledge areas and the clinical disciplines the first
four units leave open, on the JCNDE Domain of Dentistry (FK1-FK10, CC1-CC56, read Nov 2026 through a
paraphrasing reader). Standard entry-level content only: facts are authored as multiple choice with the
usual wrong answers; doses, risks, statistics and ratios are recomputed by sympy. Where practice varies,
the card says "usual" or names the guideline."""
from opl_dsl import Q, L, U

FW, FILE, IDEA = "DN", "dn-depth", "DX"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
J = lambda *c: [f"jcnde-domain:{x}" for x in c]


def facts(name, skill, prompt, rows, explain):
    """a recall multiple-choice card: rows are (stem field, right, wrong, wrong, wrong)"""
    return Q(name, skill, prompt, pace="recall", cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


UNITS = [
U(5, "dental-anatomy", "Dental anatomy and occlusion (FK1)", [("Tooth morphology and occlusion", [
    L("A", "Recall root and canal numbers of permanent teeth.", "Maxillary first molar 3 roots (MB often 2 canals); mandibular first molar 2 roots; maxillary first premolar usually 2.", [], [
        facts("dn-root-count", "dent.anatomy", "{{q}}", [
            ("How many roots does a maxillary first molar usually have?", "3 (mesiobuccal, distobuccal, palatal)", "2 (mesial, distal)", "1", "4"),
            ("How many roots does a mandibular first molar usually have?", "2 (mesial, distal)", "3 (two buccal, one lingual)", "1", "4"),
            ("How many roots does a maxillary first premolar usually have?", "2 (buccal, palatal)", "1", "3", "It has no consistent pattern"),
            ("Which permanent tooth has the longest root?", "Maxillary canine", "Maxillary central incisor", "Mandibular first molar", "Maxillary first premolar"),
            ("Which root of the maxillary first molar most often has two canals?", "Mesiobuccal (MB2)", "Palatal", "Distobuccal", "None: each root has one"),
            ("How many canals does a mandibular first molar usually have?", "3 (two mesial, one distal), sometimes 4", "2", "1", "5"),
        ], "Canal anatomy drives endodontic access: missed MB2 canals are a leading cause of failed root canal treatment on maxillary molars")], p="P3", std=J("FK1", "CC28")),
    L("B", "Recall cusp and crown features that identify a tooth.", "Mandibular first molar 5 cusps; maxillary first molar 4 plus Carabelli; mandibular second premolar may have 3.", [], [
        facts("dn-crown-features", "dent.anatomy", "{{q}}", [
            ("How many cusps does a mandibular first molar have?", "5 (3 buccal, 2 lingual)", "4", "3", "6"),
            ("Where is the cusp of Carabelli found?", "Mesiolingual cusp of maxillary first molars", "Distobuccal cusp of mandibular first molars", "Lingual of maxillary lateral incisors", "Buccal of mandibular premolars"),
            ("Which is the largest cusp of a maxillary first molar?", "Mesiolingual", "Mesiobuccal", "Distobuccal", "Distolingual"),
            ("Which premolar often has three cusps (a Y-shaped groove pattern)?", "Mandibular second premolar", "Maxillary first premolar", "Mandibular first premolar", "Maxillary second premolar"),
            ("What crosses the occlusal table of a maxillary molar from mesiolingual to distobuccal cusp?", "The oblique ridge", "The transverse ridge", "The central fossa", "The cingulum"),
        ], "Crown features name a tooth from a photo or a radiograph; the oblique ridge is unique to maxillary molars")], p="P3", std=J("FK1")),
    L("C", "Classify occlusion by Angle's molar relationship.", "Class I: MB cusp of the maxillary first molar in the buccal groove of the mandibular first molar; II: distal mandible; III: mesial mandible.", [], [
        facts("dn-angle-class", "dent.anatomy", "{{q}}", [
            ("The mesiobuccal cusp of the maxillary first molar sits in the buccal groove of the mandibular first molar. Which Angle class?", "Class I", "Class II", "Class III", "Class II division 2"),
            ("The mandibular first molar is distal to its Class I position, with flared upper incisors. Which class?", "Class II division 1", "Class II division 2", "Class III", "Class I with crowding"),
            ("The mandibular first molar is distal to its Class I position, with retroclined upper centrals and a deep bite. Which class?", "Class II division 2", "Class II division 1", "Class III", "Class I"),
            ("The mandibular first molar is mesial to its Class I position, often with an anterior crossbite. Which class?", "Class III", "Class II division 1", "Class I", "Class II division 2"),
        ], "Angle classifies the anteroposterior molar relationship only; crowding, crossbites and open bites are described separately")], p="P2", std=J("CC34")),
    L("D", "Judge an abutment by its crown-to-root ratio.", "Ideal 1:2; 2:3 is acceptable; 1:1 is the minimum for an abutment.", [], [
        Q("dn-crown-root-ratio", "dent.anatomy", "On a radiograph a tooth's clinical crown (to the bone crest) measures {{c}} mm and the root in bone {{r}} mm. What is the crown-to-root ratio (as crown/root)? Ratios above 1 rule it out as an abutment.",
          given={"c": {"pick": [6, 8, 10, 12]}, "r": {"pick": [8, 10, 12, 16]}}, value="c/r", tex="C/R", verify="Rational(c, r)",
          explain="Bone loss moves the fulcrum apically, lengthening the clinical crown and shortening the root in bone at the same time")], std=J("CC31")),
])]),
U(6, "head-neck", "Head and neck anatomy (FK1)", [("Nerves, muscles, vessels and glands", [
    L("A", "Name the nerve that supplies a structure.", "Muscles of mastication: V3. Facial expression: VII. Taste anterior two-thirds: VII (chorda tympani); posterior third: IX. Tongue movement: XII.", [], [
        facts("dn-nerve-supply", "dent.anatomy", "{{q}}", [
            ("Which nerve supplies the muscles of mastication?", "Mandibular division of the trigeminal (V3)", "Facial nerve (VII)", "Maxillary division (V2)", "Hypoglossal (XII)"),
            ("Which nerve carries taste from the anterior two-thirds of the tongue?", "Chorda tympani of the facial nerve (VII)", "Lingual nerve's own fibres (V3)", "Glossopharyngeal (IX)", "Hypoglossal (XII)"),
            ("Which nerve carries general sensation from the anterior two-thirds of the tongue?", "Lingual nerve (V3)", "Chorda tympani (VII)", "Glossopharyngeal (IX)", "Vagus (X)"),
            ("Which nerve moves the tongue (all but palatoglossus)?", "Hypoglossal (XII)", "Lingual (V3)", "Glossopharyngeal (IX)", "Facial (VII)"),
            ("Which nerve gives secretomotor fibres to the parotid gland (via the otic ganglion)?", "Glossopharyngeal (IX)", "Facial (VII)", "Vagus (X)", "Trigeminal (V3)"),
            ("Which nerve supplies the palatal gingiva of the maxillary premolars and molars?", "Greater palatine (V2)", "Nasopalatine (V2)", "Posterior superior alveolar (V2)", "Lingual (V3)"),
            ("Which nerve supplies the pulps of the maxillary molars (except often the MB root of the first)?", "Posterior superior alveolar (V2)", "Middle superior alveolar (V2)", "Greater palatine (V2)", "Inferior alveolar (V3)"),
        ], "Sensation of the teeth and gingiva is all trigeminal; taste rides with VII and IX, and motor to the tongue is XII. Anesthetic choice and nerve-injury questions turn on these")], p="P3", std=J("FK1", "CC19")),
    L("B", "Know what each muscle of mastication does.", "Masseter, temporalis, medial pterygoid close; lateral pterygoid opens and protrudes.", [], [
        facts("dn-mastication-muscles", "dent.anatomy", "{{q}}", [
            ("Which muscle of mastication opens the jaw and protrudes the mandible?", "Lateral pterygoid", "Medial pterygoid", "Masseter", "Temporalis"),
            ("Which muscle's posterior fibres retrude the mandible?", "Temporalis", "Masseter", "Lateral pterygoid", "Medial pterygoid"),
            ("Which muscle inserts on the articular disc and condylar neck?", "Lateral pterygoid (superior and inferior heads)", "Masseter", "Medial pterygoid", "Digastric"),
            ("Which muscle forms a sling with the masseter at the angle of the mandible?", "Medial pterygoid", "Lateral pterygoid", "Temporalis", "Buccinator"),
        ], "The lateral pterygoid is the odd one: it opens, protrudes and moves the jaw side to side, and its spasm is a common TMD finding")], p="P3", std=J("FK1", "CC35")),
    L("C", "Locate salivary ducts and the landmarks of nerve blocks.", "Parotid (Stensen) opposite the maxillary second molar; submandibular (Wharton) at the sublingual caruncle.", [], [
        facts("dn-ducts-landmarks", "dent.anatomy", "{{q}}", [
            ("Where does the parotid (Stensen's) duct open?", "Buccal mucosa opposite the maxillary second molar", "Sublingual caruncle", "Along the sublingual fold", "Opposite the mandibular first molar"),
            ("Where does the submandibular (Wharton's) duct open?", "Sublingual caruncle beside the lingual frenum", "Opposite the maxillary second molar", "Soft palate", "Retromolar pad"),
            ("Which gland makes most unstimulated saliva?", "Submandibular", "Parotid", "Sublingual", "Minor salivary glands"),
            ("Through which space does the needle pass for an inferior alveolar nerve block?", "Pterygomandibular space", "Infratemporal fossa above the lateral pterygoid", "Submandibular space", "Parapharyngeal space"),
            ("What does an IANB needle in the parotid gland risk?", "Transient facial nerve paralysis", "Lingual nerve paresthesia", "Hematoma of the pterygoid plexus", "Loss of taste"),
            ("Injury to which vessel causes a hematoma after a posterior superior alveolar block?", "Pterygoid venous plexus", "Facial artery", "Lingual artery", "Inferior alveolar artery"),
        ], "Parotid secretion dominates stimulated flow; the submandibular gland dominates at rest. A needle too far posterior in an IANB reaches the parotid and the facial nerve")], p="P3", std=J("FK1", "CC19")),
    L("D", "Trace the arterial supply and lymph drainage of the mouth.", "Teeth from branches of the maxillary artery; lower lip and floor drain to submental and submandibular nodes.", [], [
        facts("dn-vessels-nodes", "dent.anatomy", "{{q}}", [
            ("Which artery gives rise to the inferior alveolar artery?", "Maxillary artery", "Facial artery", "Lingual artery", "Superficial temporal artery"),
            ("Where does the tip of the tongue drain first?", "Submental nodes", "Deep cervical nodes directly", "Parotid nodes", "Retropharyngeal nodes"),
            ("Where do most maxillary and mandibular teeth drain first (except mandibular incisors)?", "Submandibular nodes", "Submental nodes", "Occipital nodes", "Supraclavicular nodes"),
            ("A spreading infection from a mandibular third molar below the mylohyoid line reaches which space first?", "Submandibular space", "Sublingual space", "Buccal space", "Canine space"),
            ("Why can infection in the danger zone of the face reach the cavernous sinus?", "Facial veins communicate with it through the ophthalmic veins and pterygoid plexus", "The facial artery enters the skull", "Lymph drains directly into the sinus", "The parotid gland contains the sinus"),
        ], "Infection follows fascial planes and veins: the mylohyoid line decides sublingual versus submandibular spread, and bilateral submandibular, sublingual and submental involvement is Ludwig's angina")], p="P3", std=J("FK1", "CC18")),
])]),
U(7, "histology", "Oral histology and development (FK1, FK4)", [("Tooth development, tissues and developmental anomalies", [
    L("A", "Name the cell and germ layer behind each dental tissue.", "Enamel from ameloblasts (ectoderm); dentin, pulp and cementum from ectomesenchyme (neural crest).", [], [
        facts("dn-tissue-origin", "dent.anatomy", "{{q}}", [
            ("Which cells form enamel, and from which origin?", "Ameloblasts, from oral ectoderm", "Odontoblasts, from neural crest", "Cementoblasts, from the dental follicle", "Fibroblasts, from mesoderm"),
            ("Which cells form dentin?", "Odontoblasts (neural-crest ectomesenchyme)", "Ameloblasts", "Cementoblasts", "Osteoclasts"),
            ("What structure shapes the root and induces root dentin?", "Hertwig's epithelial root sheath", "The stellate reticulum", "The enamel knot", "The dental lamina"),
            ("Which tissue is laid down throughout life and can repair itself?", "Secondary and tertiary dentin (and cementum)", "Enamel", "The enamel organ", "Nasmyth's membrane"),
            ("What are the stages of tooth development in order?", "Bud, cap, bell, apposition, maturation", "Cap, bud, bell, maturation, apposition", "Bell, cap, bud, eruption", "Lamina, bell, bud, cap"),
            ("What remnants of Hertwig's root sheath persist in the PDL?", "Epithelial rests of Malassez", "Rests of Serres", "Reduced enamel epithelium", "Bohn's nodules"),
        ], "Enamel is the only dental hard tissue from ectoderm and the only one that cannot be remade once the ameloblasts are lost at eruption. Rests of Malassez give rise to radicular cysts")], p="P3", std=J("FK1")),
    L("B", "Recognise developmental anomalies of teeth.", "Amelogenesis imperfecta: enamel only. Dentinogenesis imperfecta: opalescent teeth, obliterated pulps, linked with osteogenesis imperfecta.", [], [
        facts("dn-tooth-anomalies", "dent.biomed", "{{q}}", [
            ("Opalescent grey-blue teeth with bulbous crowns and obliterated pulp chambers suggest…", "Dentinogenesis imperfecta", "Amelogenesis imperfecta", "Regional odontodysplasia", "Tetracycline staining"),
            ("Thin or soft enamel on all teeth with normal dentin and pulps on radiographs suggests…", "Amelogenesis imperfecta", "Dentinogenesis imperfecta", "Dentin dysplasia", "Fluorosis"),
            ("Teeth that look like ghosts on radiographs (thin enamel and dentin, large pulps) in one quadrant suggest…", "Regional odontodysplasia", "Dentin dysplasia type I", "Taurodontism", "Amelogenesis imperfecta"),
            ("Missing teeth, conical teeth, sparse hair and inability to sweat suggest…", "Hypohidrotic ectodermal dysplasia", "Cleidocranial dysplasia", "Gardner syndrome", "Down syndrome"),
            ("Many supernumerary unerupted teeth and absent clavicles suggest…", "Cleidocranial dysplasia", "Ectodermal dysplasia", "Gardner syndrome", "Treacher Collins syndrome"),
            ("Enlarged pulp chambers that extend apically, with short roots, in molars describe…", "Taurodontism", "Dilaceration", "Concrescence", "Dens invaginatus"),
        ], "Which tissue is affected names the condition: enamel only (AI), dentin with pulp obliteration (DI), or the whole tooth in a region (regional odontodysplasia)")], p="P2", std=J("FK4", "CC5")),
    L("C", "Explain how clefts form.", "Cleft lip: failed fusion of the medial nasal and maxillary processes. Cleft palate: failed fusion of the palatal shelves.", [], [
        facts("dn-clefts", "dent.biomed", "{{q}}", [
            ("Failure of which processes to fuse causes cleft lip?", "Medial nasal and maxillary processes", "Lateral nasal and maxillary processes", "The two palatal shelves", "The mandibular processes"),
            ("Failure of which structures to fuse causes cleft of the secondary palate?", "The lateral palatine shelves", "Medial nasal processes", "Mandibular processes", "Frontonasal and maxillary processes"),
            ("Which tooth is most often missing or malformed next to a cleft of the alveolus?", "Maxillary lateral incisor", "Maxillary central incisor", "Maxillary canine", "Mandibular lateral incisor"),
            ("Which is more common, and more often in males: cleft lip with or without palate, or isolated cleft palate?", "Cleft lip with or without palate", "Isolated cleft palate", "They are equally common", "Neither shows a sex difference"),
        ], "The lip and primary palate form by weeks 6–7, the secondary palate by about week 12; isolated cleft palate is more often female and syndromic")], p="P3", std=J("FK4")),
])]),
U(8, "pharmacology", "Pharmacology (FK8)", [("Analgesics, antibiotics, interactions and dosing", [
    L("A", "Recall analgesic choices and limits for dental pain.", "Ibuprofen 400 mg ± acetaminophen 500–1000 mg beats opioids for most dental pain; acetaminophen ≤ 4 g/day (usual adult maximum).", [], [
        facts("dn-analgesics", "dent.pharm", "{{q}}", [
            ("What is the usual first-line regimen for moderate to severe acute dental pain in a healthy adult (ADA 2024 guideline)?", "Ibuprofen 400 mg with acetaminophen 500–1000 mg", "Hydrocodone with acetaminophen", "Tramadol alone", "Codeine 30 mg"),
            ("What is the usual adult maximum daily dose of acetaminophen?", "4 g (lower, often 3 g, with liver disease or alcohol use)", "1 g", "8 g", "There is no ceiling"),
            ("Why should NSAIDs be avoided in a patient on warfarin?", "They add antiplatelet effect and GI bleeding risk", "They inactivate warfarin", "They cause hypoglycemia", "They block local anesthetics"),
            ("Which analgesic is preferred in the third trimester of pregnancy?", "Acetaminophen", "Ibuprofen", "Aspirin", "Naproxen"),
            ("What reverses opioid respiratory depression?", "Naloxone", "Flumazenil", "Atropine", "Epinephrine"),
            ("What reverses benzodiazepine sedation?", "Flumazenil", "Naloxone", "Physostigmine", "Glucagon"),
        ], "NSAIDs inhibit COX and prostaglandin synthesis at the site of tissue injury, which is why they outperform opioids after extractions; opioids are a last resort for short courses")], p="P3", std=J("FK8", "CC26")),
    L("B", "Choose antibiotics and know their dental side effects.", "Amoxicillin first line; penicillin allergy: azithromycin or doxycycline (clindamycin no longer recommended for prophylaxis, AHA 2021).", [], [
        facts("dn-antibiotics", "dent.pharm", "{{q}}", [
            ("What is the usual first-line antibiotic for a spreading odontogenic infection in a non-allergic adult?", "Amoxicillin (or penicillin VK)", "Ciprofloxacin", "Vancomycin", "Gentamicin"),
            ("For endocarditis prophylaxis in a penicillin-allergic adult, which is now recommended (AHA 2021)?", "Azithromycin 500 mg or doxycycline 100 mg", "Clindamycin 600 mg", "Cephalexin in any allergy", "No antibiotic is ever needed"),
            ("Which antibiotic causes intrinsic tooth staining when given during tooth development?", "Tetracycline (doxycycline, minocycline)", "Amoxicillin", "Metronidazole", "Azithromycin"),
            ("Which antibiotic interacts with alcohol (disulfiram-like reaction) and raises warfarin's effect?", "Metronidazole", "Amoxicillin", "Clindamycin", "Penicillin VK"),
            ("Which antibiotic carries the highest risk of C. difficile colitis among those used in dentistry?", "Clindamycin", "Penicillin VK", "Amoxicillin", "Doxycycline"),
            ("Which antifungal is used as a troche or suspension for oral candidiasis?", "Clotrimazole or nystatin", "Acyclovir", "Metronidazole", "Chlorhexidine alone"),
        ], "Most odontogenic infections are mixed streptococci and anaerobes, which penicillins cover; drainage and removing the source matter more than the drug")], p="P3", std=J("FK8", "CC26", "CC27")),
    L("C", "Recognise drug interactions and complications that change dental care.", "Epinephrine with nonselective β-blockers: hypertension and reflex bradycardia. Antiresorptives: MRONJ. Bisphosphonates and denosumab before extractions.", [], [
        facts("dn-interactions", "dent.pharm", "{{q}}", [
            ("Epinephrine in a patient taking propranolol can cause…", "A sharp rise in blood pressure with reflex bradycardia", "Hypoglycemia", "Prolonged anesthesia only", "Methemoglobinemia"),
            ("A patient on IV zoledronic acid for metastatic cancer needs an extraction. The chief risk is…", "Medication-related osteonecrosis of the jaw", "Uncontrolled bleeding", "Adrenal crisis", "Serotonin syndrome"),
            ("Gingival overgrowth is a known effect of…", "Phenytoin, cyclosporine and nifedipine (calcium channel blockers)", "Metformin", "Amoxicillin", "Levothyroxine"),
            ("Which local anesthetic, in large doses, is most linked to methemoglobinemia?", "Prilocaine", "Lidocaine", "Mepivacaine", "Bupivacaine"),
            ("Which drug class causes xerostomia most often?", "Anticholinergics (and many antidepressants and antihistamines)", "Statins", "Penicillins", "Thyroid hormone"),
            ("A patient on long-term high-dose steroids faces stressful surgery. The concern is…", "Adrenal insufficiency (crisis)", "Hyperthyroidism", "Malignant hyperthermia", "Anaphylaxis to latex"),
        ], "Ask what the drug does to bone, blood, blood pressure or glands, and the dental consequence follows")], p="P3", std=J("FK8", "CC27", "CC8")),
    L("D", "Calculate a weight-based pediatric antibiotic dose.", "Endocarditis prophylaxis: amoxicillin 50 mg/kg, not above the adult 2 g.", [], [
        Q("dn-peds-amoxicillin", "dent.pharm", "A child weighing {{kg}} kg needs endocarditis prophylaxis with amoxicillin (50 mg/kg, not to exceed the adult dose of 2 g). How many mg?",
          given={"kg": {"pick": [12, 18, 25, 32, 45, 60]}}, value="min(50*kg, 2000)", tex="\\text{dose}", final=True, verify="Min(50*kg, 2000)",
          explain="Weight-based until the adult dose is reached; at 40 kg and above the child gets 2 g, 30–60 minutes before the procedure")], std=J("FK8", "CC26")),
    L("E", "Find how much drug remains after a number of half-lives.", "Fraction left = (1/2)^{t/t½}; about 5 half-lives to clear 97%.", [], [
        Q("dn-half-life", "dent.pharm", "A drug has a half-life of {{h}} h. What percentage of a dose remains after {{t}} h?",
          given={"h": {"pick": [2, 4, 6, 8]}, "t": {"pick": [4, 12, 24]}}, value="100*0.5^(t/h)", tex="\\%",
          verify="100*exp(-log(2)/h*t)", explain="First-order elimination: the same fraction leaves in each half-life, whatever the dose")], std=J("FK8")),
])]),
U(9, "micro-immuno", "Microbiology and host defence (FK5, FK7)", [("Oral microbes, infections, immunity and exposure", [
    L("A", "Link oral diseases to their organisms.", "Caries: S. mutans starts, lactobacilli advance. Periodontitis: the red complex (P. gingivalis, T. forsythia, T. denticola).", [], [
        facts("dn-oral-microbes", "dent.biomed", "{{q}}", [
            ("Which organism is most associated with starting smooth-surface caries?", "Streptococcus mutans", "Lactobacillus species", "Porphyromonas gingivalis", "Candida albicans"),
            ("Which organisms are most associated with the progression of dentinal caries?", "Lactobacilli", "Streptococcus sanguinis", "Actinomyces israelii", "Treponema pallidum"),
            ("Which group forms Socransky's red complex?", "P. gingivalis, T. forsythia, T. denticola", "S. mutans, S. sobrinus, lactobacilli", "A. actinomycetemcomitans alone", "Candida, Actinomyces, Veillonella"),
            ("Molar–incisor pattern periodontitis in a teenager (formerly localized aggressive) is classically linked to…", "Aggregatibacter actinomycetemcomitans", "Streptococcus mutans", "Candida albicans", "Lactobacillus casei"),
            ("Draining sinuses with yellow sulfur granules after jaw surgery suggest…", "Actinomycosis", "Candidiasis", "Tuberculosis", "Syphilis"),
            ("Recurrent vesicles on the vermilion border triggered by sun or stress are caused by…", "Herpes simplex virus type 1 (reactivation)", "Varicella-zoster primary infection", "Coxsackievirus A", "Epstein–Barr virus"),
        ], "S. mutans makes acid and glucans from sucrose; P. gingivalis has gingipains that degrade host proteins. Recurrent herpes labialis is reactivation from the trigeminal ganglion")], p="P3", std=J("FK7", "CC21", "CC22")),
    L("B", "Know bloodborne pathogen risk and the response to an exposure.", "Percutaneous transmission risk, unvaccinated source-positive: HBV up to about 30%, HCV about 1.8%, HIV about 0.3%.", [], [
        facts("dn-exposure", "dent.practice", "{{q}}", [
            ("After a needlestick from a source-positive patient, which virus is most likely to be transmitted to an unvaccinated worker?", "Hepatitis B (up to about 30%)", "Hepatitis C (about 1.8%)", "HIV (about 0.3%)", "They carry equal risk"),
            ("When should HIV post-exposure prophylaxis start after a high-risk exposure?", "As soon as possible, ideally within hours (no later than 72 h)", "Only after the source tests positive a week later", "After 6 weeks", "It is never indicated in dentistry"),
            ("What is the first thing to do after a needlestick?", "Wash the wound with soap and water, then report it", "Squeeze and apply bleach", "Finish the procedure, then decide", "Take an antibiotic"),
            ("Which hepatitis vaccine must OSHA's bloodborne pathogens standard offer dental workers at no cost?", "Hepatitis B", "Hepatitis A", "Hepatitis C (there is no vaccine)", "Hepatitis E"),
        ], "Risk scales with viral load in blood: HBV e-antigen-positive blood carries far more virus than HIV-positive blood")], p="P3", std=J("FK7", "CC51")),
    L("C", "Classify hypersensitivity reactions met in dentistry.", "Type I IgE (latex anaphylaxis, penicillin), IV T-cell (contact dermatitis to latex accelerators, nickel, methacrylates).", [], [
        facts("dn-hypersensitivity", "dent.biomed", "{{q}}", [
            ("Hives and wheezing within minutes of latex glove contact are which type of hypersensitivity?", "Type I (IgE-mediated)", "Type IV (delayed, T-cell)", "Type II (cytotoxic)", "Type III (immune complex)"),
            ("A rash on the hands 48 hours after handling uncured methacrylate is which type?", "Type IV (delayed, T-cell)", "Type I", "Type II", "Type III"),
            ("A transfusion reaction from ABO mismatch is which type?", "Type II (antibody against cell surfaces)", "Type I", "Type III", "Type IV"),
            ("Which antibody predominates in saliva?", "Secretory IgA", "IgE", "IgG", "IgM"),
            ("Which cell is the first to arrive in acute gingival inflammation?", "Neutrophil", "Plasma cell", "Eosinophil", "Mast cell degranulation alone"),
        ], "Timing separates them: minutes for type I, days for type IV. Plasma cells dominate established periodontitis lesions, neutrophils the early one")], p="P3", std=J("FK5")),
])]),
U(10, "oral-pathology", "Oral and general pathology (FK6, CC23)", [("Lesions by appearance and site", [
    L("A", "Name a soft-tissue lesion from its description.", "Mucocele: lower lip, after trauma. Ranula: floor of mouth. Fibroma: firm, smooth, on the bite line. Pyogenic granuloma: red, bleeds easily, often in pregnancy.", [], [
        facts("dn-soft-lesions", "dent.biomed", "{{q}}", [
            ("A bluish fluctuant swelling of the lower lip that comes and goes after biting it is most likely…", "Mucocele (mucus extravasation)", "Ranula", "Fibroma", "Hemangioma"),
            ("A firm, smooth, pink nodule on the buccal mucosa along the bite line is most likely…", "Irritation fibroma", "Pyogenic granuloma", "Lipoma", "Squamous cell carcinoma"),
            ("A red, lobulated, easily bleeding gingival mass in a pregnant patient is most likely…", "Pyogenic granuloma (pregnancy tumour)", "Peripheral giant cell granuloma", "Fibroma", "Kaposi sarcoma"),
            ("Bilateral lacy white striae on the buccal mucosa that do not wipe off suggest…", "Lichen planus (Wickham striae)", "Candidiasis", "Leukoedema", "Linea alba"),
            ("A white patch that wipes off leaving a red, raw surface suggests…", "Pseudomembranous candidiasis", "Leukoplakia", "Lichen planus", "Hairy leukoplakia"),
            ("Corrugated white plaques on the lateral tongue in an immunosuppressed patient suggest…", "Oral hairy leukoplakia (EBV)", "Geographic tongue", "Lichen planus", "Frictional keratosis"),
        ], "Site, colour, whether it wipes off and the history narrow the list before biopsy; a white lesion that will not wipe off and has no cause needs a biopsy")], p="P2", std=J("FK6", "CC23", "CC5")),
    L("B", "Rank lesions by malignant risk and know oral cancer's usual sites.", "Erythroplakia carries the highest risk; squamous cell carcinoma is most common on the lateral and ventral tongue and floor of mouth.", [], [
        facts("dn-cancer-risk", "dent.biomed", "{{q}}", [
            ("Which oral lesion has the highest chance of being dysplastic or malignant at biopsy?", "Erythroplakia", "Leukoplakia", "Lichen planus", "Leukoedema"),
            ("What is the most common site of oral squamous cell carcinoma (excluding lip)?", "Lateral and ventral tongue", "Hard palate", "Dorsal tongue", "Attached gingiva"),
            ("HPV-16-related squamous cell carcinoma most often arises in the…", "Oropharynx (tonsils, base of tongue)", "Lower lip", "Buccal mucosa", "Hard palate"),
            ("Lower-lip squamous cell carcinoma is most linked to…", "Chronic sun exposure (actinic cheilitis)", "HPV-16", "Smokeless tobacco alone", "Iron deficiency"),
            ("A non-healing ulcer present for more than two weeks with no cause should be…", "Biopsied", "Watched for six months", "Treated with antibiotics only", "Cauterised"),
        ], "Tobacco and alcohol act together on the floor of mouth and tongue; HPV drives a separate, rising oropharyngeal disease in younger non-smokers")], p="P2", std=J("FK6", "CC23")),
    L("C", "Name a jaw lesion from its radiograph and location.", "Dentigerous cyst around an unerupted crown; periapical cyst at a non-vital apex; ameloblastoma multilocular in the posterior mandible; OKC with Gorlin syndrome.", [], [
        facts("dn-jaw-lesions", "dent.biomed", "{{q}}", [
            ("A unilocular radiolucency around the crown of an impacted third molar, attached at the CEJ, is most likely…", "Dentigerous cyst", "Periapical cyst", "Lateral periodontal cyst", "Stafne defect"),
            ("A radiolucency at the apex of a non-vital tooth is most likely…", "Periapical granuloma or cyst", "Dentigerous cyst", "Ameloblastoma", "Cemento-osseous dysplasia"),
            ("A multilocular 'soap bubble' radiolucency in the posterior mandible of an adult is classically…", "Ameloblastoma", "Periapical cyst", "Stafne defect", "Torus"),
            ("Multiple odontogenic keratocysts with basal cell carcinomas and bifid ribs suggest…", "Nevoid basal cell carcinoma (Gorlin) syndrome", "Gardner syndrome", "Cherubism", "McCune–Albright syndrome"),
            ("A well-defined radiolucency below the mandibular canal near the angle, unchanged for years, is…", "Stafne bone defect (salivary gland depression)", "Ameloblastoma", "Dentigerous cyst", "Osteosarcoma"),
            ("Ground-glass radiopacity that blends with normal bone, in a young patient, suggests…", "Fibrous dysplasia", "Paget disease", "Osteosarcoma", "Condensing osteitis"),
            ("A sunburst periosteal reaction and widened PDL space suggest…", "Osteosarcoma", "Fibrous dysplasia", "Periapical abscess", "Central giant cell granuloma"),
        ], "Location relative to the tooth and the vitality test do most of the work: crown-associated, apex-associated, or unrelated to the teeth")], p="P2", std=J("FK6", "CC7", "CC23")),
    L("D", "Tell the blistering diseases apart.", "Pemphigus vulgaris: intraepithelial split, Nikolsky positive, desmoglein 3. Mucous membrane pemphigoid: subepithelial split, eye scarring risk.", [], [
        facts("dn-vesiculobullous", "dent.biomed", "{{q}}", [
            ("Where is the split in pemphigus vulgaris?", "Within the epithelium (suprabasal acantholysis)", "Below the epithelium (subepithelial)", "In the lamina propria", "There is no split"),
            ("Which antigen do pemphigus vulgaris antibodies target?", "Desmoglein 3 (desmosomes)", "BP180 in hemidesmosomes", "Type VII collagen", "Keratin 14"),
            ("Mucous membrane pemphigoid most needs referral to which specialist, because of scarring risk?", "Ophthalmologist", "Cardiologist", "Nephrologist", "Otologist"),
            ("Target lesions on the skin and crusted lips after a drug or herpes infection suggest…", "Erythema multiforme", "Pemphigus vulgaris", "Lichen planus", "Recurrent aphthous stomatitis"),
            ("Recurrent shallow painful ulcers on non-keratinised mucosa, with no vesicles first, are…", "Recurrent aphthous ulcers", "Recurrent herpes", "Pemphigus", "Squamous cell carcinoma"),
        ], "Intraepithelial blisters break at once and leave ragged erosions; subepithelial ones can stay intact. Recurrent herpes favours keratinised mucosa (palate, gingiva), aphthae the movable mucosa")], p="P2", std=J("FK5", "FK6", "CC23")),
])]),
U(11, "clinical", "Clinical disciplines (CC17–CC38)", [("Periodontics, endodontics, prosthodontics, pediatrics, surgery and orthodontics", [
    L("A", "Classify partially edentulous arches by Kennedy.", "I bilateral distal extension; II unilateral distal extension; III bounded posterior; IV a single bounded anterior space crossing the midline.", [], [
        facts("dn-kennedy", "dent.clinical", "{{q}}", [
            ("Missing teeth on both sides behind the remaining natural teeth: which Kennedy class?", "Class I", "Class II", "Class III", "Class IV"),
            ("A single anterior edentulous space crossing the midline: which Kennedy class?", "Class IV", "Class III", "Class I", "Class II"),
            ("A unilateral posterior space bounded by teeth on both ends: which Kennedy class?", "Class III", "Class II", "Class I", "Class IV"),
            ("A unilateral distal-extension space: which Kennedy class?", "Class II", "Class I", "Class III", "Class IV"),
            ("By Applegate's rules, an edentulous third molar space that will not be replaced is…", "Ignored in classifying", "Always counted", "Class IV", "A modification space"),
            ("Which Kennedy class can have no modification spaces?", "Class IV", "Class I", "Class II", "Class III"),
        ], "The most posterior edentulous area decides the class; other spaces become modifications. Class IV has none because any additional space would be more posterior")], p="P2", std=J("CC29", "CC31")),
    L("B", "Choose pediatric pulp therapy and space maintenance.", "Vital primary pulp exposure with healthy radicular pulp: pulpotomy. Necrotic primary pulp in a restorable tooth: pulpectomy. Early loss of a primary second molar: distal shoe if the first permanent molar has not erupted.", [], [
        facts("dn-pediatric", "dent.clinical", "{{q}}", [
            ("A carious exposure of a vital primary molar with bleeding that stops within minutes after coronal pulp removal: treatment?", "Pulpotomy", "Pulpectomy", "Extraction", "Direct pulp cap"),
            ("A primary second molar is lost before the permanent first molar erupts. Which space maintainer?", "Distal shoe", "Band and loop", "Lower lingual holding arch", "Nance appliance"),
            ("A primary first molar is lost at age 6 with the permanent first molar in occlusion. Usual space maintainer?", "Band and loop", "Distal shoe", "No maintainer is ever needed", "Removable partial denture"),
            ("At what age are all 20 primary teeth usually erupted?", "About 2½–3 years", "About 1 year", "About 5 years", "About 6 years"),
            ("Which behaviour technique introduces a procedure step by step: explain, demonstrate, then do?", "Tell-show-do", "Voice control", "Protective stabilisation", "Nitrous oxide"),
            ("Which primary tooth is usually the first to erupt?", "Mandibular central incisor (about 6 months)", "Maxillary central incisor", "Mandibular first molar", "Maxillary canine"),
        ], "A distal shoe guides the erupting first molar into place; once it is in occlusion a band and loop is enough")], p="P3", std=J("CC20", "CC34", "CC52")),
    L("C", "Know common oral-surgery thresholds and complications.", "Alveolar osteitis appears 2–4 days after extraction; usual INR limit for simple extractions about 3.5 (with local measures); ASA classes I–VI.", [], [
        facts("dn-oral-surgery", "dent.clinical", "{{q}}", [
            ("Severe throbbing pain 2–4 days after a mandibular molar extraction, with an empty socket and bad odour, is…", "Alveolar osteitis (dry socket)", "Osteomyelitis", "Normal healing", "A displaced root tip"),
            ("For a patient on warfarin needing a simple extraction, the usual practice is to check that the INR is…", "Below about 3.5 (and use local hemostatic measures) without stopping warfarin", "Below 1.0", "Normal, by stopping warfarin a week before", "Irrelevant: INR does not affect bleeding"),
            ("A patient with severe systemic disease that is a constant threat to life is ASA class…", "IV", "II", "III", "V"),
            ("A patient with well-controlled hypertension and no other illness is ASA class…", "II", "I", "III", "IV"),
            ("Which nerve is most at risk when removing a mandibular third molar with a lingual flap?", "Lingual nerve", "Mental nerve", "Facial nerve", "Long buccal nerve"),
            ("An oroantral communication after removing a maxillary molar should be managed by…", "Closing it and sinus precautions (no nose blowing), larger ones by flap", "Packing it with gauze for a week", "Irrigating it daily", "Ignoring it: they always close"),
        ], "Dry socket is lost clot, not infection: irrigate and dress it. Stopping anticoagulants for minor surgery usually risks more than it saves")], p="P3", std=J("CC17", "CC32", "CC33", "CC8")),
    L("D", "Diagnose periapical conditions and choose endodontic treatment.", "Symptomatic apical periodontitis: tender to percussion. Acute apical abscess: swelling. Condensing osteitis: radiopacity at the apex of an inflamed pulp.", [], [
        facts("dn-periapical", "dent.clinical", "{{q}}", [
            ("A tooth is sharply tender to percussion and biting, with or without a widened PDL. Periapical diagnosis?", "Symptomatic apical periodontitis", "Asymptomatic apical periodontitis", "Chronic apical abscess", "Normal apical tissues"),
            ("A non-vital tooth has a draining sinus tract and no pain. Periapical diagnosis?", "Chronic apical abscess", "Acute apical abscess", "Symptomatic apical periodontitis", "Condensing osteitis"),
            ("Rapid onset, spontaneous pain and facial swelling from a non-vital tooth. Periapical diagnosis?", "Acute apical abscess", "Chronic apical abscess", "Asymptomatic apical periodontitis", "Reversible pulpitis"),
            ("A diffuse radiopacity at the apex of a tooth with pulpitis is…", "Condensing osteitis", "Cemento-osseous dysplasia", "Hypercementosis", "Idiopathic osteosclerosis"),
            ("What is the usual treatment for a restorable tooth with irreversible pulpitis?", "Root canal treatment (or pulpotomy in selected adult cases)", "Antibiotics alone", "Occlusal adjustment only", "A direct pulp cap"),
            ("Which test gives a false positive in a multirooted tooth with partial necrosis?", "Pulp sensibility tests (cold, EPT) can respond from the vital root", "Percussion", "Palpation", "Bite test"),
        ], "Pulp tests tell vital from non-vital; percussion, palpation, swelling and sinus tracts describe the periapex. The AAE terms keep the two diagnoses separate")], p="P2", std=J("CC20", "CC28")),
])]),
U(12, "systemic", "Systemic disease and medical risk (CC1, CC8, CC16)", [("Vital signs, labs and emergencies", [
    L("A", "Decide whether to treat from blood pressure.", "AHA 2017: stage 2 hypertension from 140/90; elective dental care is usually deferred at 180/110 or above.", [], [
        Q("dn-bp-decision", "dent.management", "A patient's blood pressure is {{s}}/{{d}} mm Hg. By the usual rule (AHA 2017 categories; defer elective care at 180 systolic or 110 diastolic and above), what applies?",
          given={"s": {"pick": [118, 128, 135, 145, 165, 185]}, "d": {"pick": [75, 85, 95, 105, 115]}}, require=["s > d + 20"],
          choice=["Normal or elevated: treat", "Hypertension stage 1 or 2: treat, with fewer epinephrine cartridges and referral", "Defer elective care and refer (severe)"],
          correct="(s >= 180 or d >= 110) ? 2 : ((s >= 130 or d >= 80) ? 1 : 0)",
          verify="2 if (s >= 180 or d >= 110) else (1 if (s >= 130 or d >= 80) else 0)",
          explain="AHA 2017: elevated 120–129 and under 80; stage 1 130–139 or 80–89; stage 2 140/90 and above. The higher category of systolic or diastolic counts")], p="P2", std=J("CC8", "CC1")),
    L("B", "Give the drug, dose and route for office emergencies.", "Anaphylaxis: epinephrine 0.3 mg IM (adult; 0.15 mg child). Angina: nitroglycerin 0.4 mg sublingual every 5 min, up to 3. Hypoglycemia: 15–20 g fast sugar if conscious.", [], [
        facts("dn-emergency-doses", "dent.management", "{{q}}", [
            ("Adult anaphylaxis: first drug and dose?", "Epinephrine 0.3 mg IM (1 mg/mL) in the thigh", "Diphenhydramine 50 mg orally", "Epinephrine 1 mg IV push", "Albuterol, two puffs"),
            ("Chest pain in a known angina patient: first drug and dose?", "Nitroglycerin 0.4 mg sublingual, repeat every 5 min up to 3 doses", "Aspirin 81 mg only", "Epinephrine 0.3 mg IM", "Glucose 15 g"),
            ("Suspected heart attack, no allergy: which drug, besides calling EMS?", "Aspirin 162–325 mg chewed", "Nitroglycerin every minute", "Diphenhydramine", "Midazolam"),
            ("A conscious diabetic patient becomes shaky and sweaty. First action?", "15–20 g of fast-acting oral sugar", "Insulin", "Epinephrine", "Oxygen alone"),
            ("Acute asthma attack: first drug?", "Inhaled albuterol (short-acting β₂ agonist)", "Inhaled corticosteroid", "Epinephrine 1 mg IV", "Aspirin"),
            ("Most common emergency in the dental office, and its first treatment?", "Syncope: lay supine with legs raised", "Anaphylaxis: epinephrine", "Seizure: restrain the patient", "Hyperventilation: give oxygen"),
        ], "Epinephrine is the only first-line drug for anaphylaxis; antihistamines are adjuncts. Nitroglycerin is withheld with low blood pressure or recent PDE-5 inhibitors")], p="P3", std=J("CC16", "FK8")),
    L("C", "Read lab values that change dental treatment.", "INR target 2–3 for most warfarin patients; HbA1c above about 8% means poor control; platelets below about 50,000 need consultation before surgery.", [], [
        facts("dn-lab-values", "dent.management", "{{q}}", [
            ("What does an HbA1c of 9.5% indicate?", "Poorly controlled diabetes over about 3 months", "Well-controlled diabetes", "Today's blood glucose only", "Iron deficiency"),
            ("What is the usual therapeutic INR range for atrial fibrillation on warfarin?", "2–3", "0.8–1.2", "4–5", "6–8"),
            ("Which test monitors warfarin?", "PT/INR", "aPTT", "Bleeding time", "Platelet count"),
            ("Which test monitors unfractionated heparin?", "aPTT", "PT/INR", "HbA1c", "Hematocrit"),
            ("Below about what platelet count is elective oral surgery usually deferred for medical consultation?", "50,000 per μL", "250,000 per μL", "150,000 per μL", "500,000 per μL"),
            ("Why do the direct oral anticoagulants (apixaban, rivaroxaban) need no INR check?", "INR does not reflect their effect; timing of the last dose matters instead", "They have no bleeding risk", "They are vitamin K antagonists", "They are reversed by local anesthetic"),
        ], "Lab values guide timing and local measures; anticoagulants are usually continued for routine dental surgery after discussion with the prescriber")], p="P3", std=J("CC7", "CC8")),
])]),
U(13, "behaviour-research", "Ethics, jurisprudence, behaviour and research (FK9, FK10)", [("Principles, consent, records and evidence", [
    L("A", "Apply the ADA principles of ethics.", "Autonomy, non-maleficence, beneficence, justice and veracity.", [], [
        facts("dn-ethics", "dent.behavior", "{{q}}", [
            ("Involving the patient in treatment decisions and respecting their choice reflects which ADA principle?", "Patient autonomy", "Justice", "Beneficence", "Veracity"),
            ("Referring a patient when a procedure is beyond your skill reflects which principle?", "Non-maleficence", "Justice", "Veracity", "Autonomy"),
            ("Telling a patient about a previous dentist's faulty work, truthfully and without disparagement, reflects…", "Veracity (with justifiable criticism)", "Justice", "Autonomy", "Beneficence alone"),
            ("Refusing a patient because they have HIV violates which principle?", "Justice", "Veracity", "Autonomy", "None: it is allowed"),
            ("Providing pro bono care to the community reflects which principle?", "Beneficence", "Veracity", "Autonomy", "Non-maleficence"),
        ], "The ADA Code names five principles; justice covers fair treatment and access, veracity covers honesty with patients and in advertising")], p="P3", std=J("FK9", "CC45")),
    L("B", "Know the rules for consent, records and reporting.", "Informed consent: diagnosis, proposed treatment, risks, benefits, alternatives including no treatment. Suspected child abuse: report (mandated). Records: never alter; add a dated correction.", [], [
        facts("dn-jurisprudence", "dent.behavior", "{{q}}", [
            ("Which is NOT a required element of informed consent?", "The fee charged by competing offices", "The risks of the proposed treatment", "Reasonable alternatives, including no treatment", "The expected benefits"),
            ("A dentist suspects child abuse from unexplained injuries. In the United States, the dentist must…", "Report to child protective services (mandated reporter)", "Confront the parent first", "Wait for proof", "Only note it in the chart"),
            ("An error is found in a past chart entry. The correct action is…", "Draw a single line through it, add the correction with date and initials", "Erase it and rewrite", "Remove the page", "Leave it as is"),
            ("Under HIPAA, a patient asks for copies of their records. The practice…", "Must provide them (a reasonable copying fee may apply)", "May refuse if a balance is owed", "Must send originals", "Needs a court order"),
            ("A patient leaves mid-treatment and the dentist ends the relationship without notice or referral. This is…", "Patient abandonment", "Informed refusal", "Res ipsa loquitur", "Respondeat superior"),
            ("A dentist is liable for an assistant's negligence during work duties under…", "Respondeat superior", "Res ipsa loquitur", "Informed consent", "Contributory negligence"),
        ], "Records are legal documents: corrections must stay visible. Mandated reporters need suspicion, not proof")], p="P3", std=J("FK9", "CC24", "CC44", "CC46")),
    L("C", "Compute relative risk, odds ratio and number needed to treat.", "RR = [a/(a+b)]/[c/(c+d)]; OR = ad/bc; NNT = 1/ARR.", [], [
        Q("dn-nnt", "dent.behavior", "In a trial, {{e}}% of patients given a sealant develop caries versus {{c}}% given none. How many children must be sealed to prevent one carious tooth (NNT)?",
          given={"e": {"pick": [5, 10, 15]}, "c": {"pick": [25, 30, 40, 50]}}, value="1/((c - e)/100)", tex="NNT", verify="1/(Rational(c, 100) - Rational(e, 100))",
          explain="NNT is the reciprocal of the absolute risk reduction; the relative risk reduction alone overstates benefit when the outcome is rare"),
        Q("dn-odds-ratio", "dent.behavior", "In a case–control study, {{a}} of 100 oral cancer cases and {{b}} of 100 controls used smokeless tobacco. What is the odds ratio?",
          given={"a": {"pick": [20, 30, 45]}, "b": {"pick": [5, 10, 15]}}, value="(a*(100 - b))/((100 - a)*b)", tex="OR",
          verify="(Rational(a, 100 - a))/(Rational(b, 100 - b))", explain="Case–control studies sample on outcome, so only the odds ratio is valid; it approximates relative risk when the disease is rare")], p="P1", std=J("FK10", "CC41")),
    L("D", "Name the study design and the level of evidence.", "Systematic reviews of RCTs at the top; then RCTs, cohort, case–control, case series, expert opinion.", [], [
        facts("dn-study-design", "dent.behavior", "{{q}}", [
            ("Patients with and without a disease are compared for past exposure. Design?", "Case–control", "Cohort", "Randomized controlled trial", "Cross-sectional"),
            ("Exposed and unexposed people are followed forward for new disease. Design?", "Cohort", "Case–control", "Case series", "Cross-sectional"),
            ("Which design gives the strongest evidence for a treatment's effect?", "A systematic review of randomized controlled trials", "A large cohort study", "A case–control study", "Expert opinion"),
            ("Prevalence of gingivitis measured at one time in a population. Design?", "Cross-sectional", "Cohort", "Case–control", "RCT"),
            ("A study rejects a true null hypothesis. Which error?", "Type I (α)", "Type II (β)", "Selection bias", "Recall bias"),
            ("A study fails to detect a real effect because it is too small. Which error?", "Type II (β), from low power", "Type I", "Confounding", "Lead-time bias"),
        ], "Design limits what a study can claim: only randomisation controls unknown confounders")], p="P3", std=J("FK10", "CC41")),
    L("E", "Recommend fluoride supplements by age and water fluoride.", "ADA 2010 schedule: water < 0.3 ppm: 0.25 mg (6 mo–3 y), 0.5 mg (3–6 y), 1.0 mg (6–16 y); 0.3–0.6 ppm: 0, 0.25, 0.5; above 0.6 ppm: none.", [], [
        Q("dn-fluoride-supplement", "dent.management", "A child at high caries risk is {{age}} years old and drinks water with {{w}} ppm fluoride. What daily fluoride supplement (mg F) does the ADA 2010 schedule give?",
          given={"age": {"pick": [1, 2, 4, 5, 8, 12]}, "w": {"pick": [0.1, 0.2, 0.4, 0.5]}}, require=["w < 0.3 or age >= 3"],
          value="w > 0.6 ? 0 : (w >= 0.3 ? (age < 3 ? 0 : (age < 6 ? 0.25 : 0.5)) : (age < 3 ? 0.25 : (age < 6 ? 0.5 : 1)))", tex="\\text{mg F}", final=True,
          verify="0 if w > Rational(6, 10) else ((0 if age < 3 else (Rational(1, 4) if age < 6 else Rational(1, 2))) if w >= Rational(3, 10) else (Rational(1, 4) if age < 3 else (Rational(1, 2) if age < 6 else 1)))",
          explain="Supplements make up for low water fluoride only, and only for children at high risk; more fluoride than this during enamel formation causes fluorosis")], p="P1", std=J("CC21", "CC52")),
])]),
]
