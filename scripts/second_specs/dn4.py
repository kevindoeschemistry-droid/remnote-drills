"""INBDE on the full Domain of Dentistry (Nov 2026): the July 2018 JCNDE document was read in full (Kevin supplied the
PDF). OBJS give an objective, two types each, to every clinical content area that had none (24 CCs), and lean on the
Foundation Knowledge areas the framework under-served (FK2, FK5, FK7, FK9). Entry-level content only; where practice or
state law varies the item says "usually". Kevin checks dental content."""
from opl_dsl import Q

FILE, FRAMEWORK = "dn-domain", "inbde"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
J = lambda *c: [f"jcnde-domain:{x}" for x in c]


def facts(name, skill, rows, explain, pace="recall"):
    return Q(name, skill, "{{q}}", pace=pace, cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


TOPICS = {"1.4": "Assessment, communication and planning", "2.4": "Patient management beyond the procedure", "3.3": "Practice, team and community", "2.5": "Chemistry of the mouth and host defence"}

OBJS = [
    ("DN-1.4.A", J("CC2", "CC3", "CC11", "FK1"), "Take a chief complaint and history, and run a head-and-neck and intraoral examination in order.",
     "Record the complaint in the patient's words and characterise pain (onset, location, quality, duration, triggers, relief); examine extraorally (asymmetry, nodes, TMJ, glands) before intraorally."),
    ("DN-1.4.B", J("CC6", "CC12"), "Predict a test result from the history and order the phases of a treatment plan.",
     "Plan in phases: systemic, urgent (acute), disease control, definitive (restorative/prosthetic), maintenance."),
    ("DN-1.4.C", J("CC13", "CC14", "CC15", "FK9"), "Communicate options and adapt care to the patient's age, needs and values.",
     "Explain etiology, alternatives (including no treatment), risks and prognosis; use open questions and reflective listening; tell-show-do for children; plan for xerostomia and dexterity in older adults."),
    ("DN-1.4.D", J("CC9", "FK2", "FK6"), "Relate oral disease to systemic disease and convert HbA1c to an estimated average glucose.",
     "Periodontitis and diabetes worsen each other; eAG (mg/dL) = 28.7 × HbA1c − 46.7 (ADAG); A1c ≥ 6.5% is diagnostic for diabetes."),
    ("DN-2.4.A", J("CC25", "FK8"), "Recognise substance use that changes dental care and total an opioid prescription in morphine milligram equivalents.",
     "MME/day = mg per dose × doses per day × conversion factor (codeine 0.15, hydrocodone 1, oxycodone 1.5, CDC 2022); avoid epinephrine within 24 h of cocaine use."),
    ("DN-2.4.B", J("CC36", "CC38", "FK1"), "Use proportion and the supracrestal attachment to plan esthetic and soft-tissue changes.",
     "Seen from the front, central : lateral : canine widths follow roughly 1.618 : 1 : 0.618; keep about 3 mm from the restorative margin to bone (about 2 mm of attached tissue plus the sulcus)."),
    ("DN-2.4.C", J("CC37", "FK10"), "Evaluate treatment outcomes and convert survival over years into an annual failure rate.",
     "AFR = 1 − S^(1/years); recall intervals follow risk (often 3–6 months for high caries or periodontal risk)."),
    ("DN-3.3.A", J("CC42", "CC50", "FK9"), "Recognise the limits of general practice and refer, and assess one's own competence.",
     "Refer when the case exceeds training or equipment; the referring dentist still owes follow-up; continuing education and outcome audit drive self-assessment."),
    ("DN-3.3.B", J("CC43", "CC47", "FK9"), "Read practice finances and meet OSHA and HIPAA duties.",
     "Overhead % = expenses ÷ collections; collection ratio = collected ÷ produced; HIPAA protects health information; OSHA's bloodborne pathogens standard protects staff."),
    ("DN-3.3.C", J("CC48"), "Plan for emergencies and disasters in the practice.",
     "Written plan with roles, evacuation and communication, data backup off site, and drills; dentists may help identify victims through dental records."),
    ("DN-3.3.D", J("CC49", "FK9"), "Delegate to allied dental personnel at the right level of supervision.",
     "Direct supervision: dentist present and checks; general: dentist authorised but need not be present; the allowed duties are set by each state's practice act."),
    ("DN-3.3.E", J("CC53", "CC54", "CC39", "CC40", "FK10"), "Measure a population's caries and choose community programmes.",
     "DMFT = decayed + missing + filled teeth; community water fluoridation at 0.7 mg/L (USPHS 2015); school sealant programmes; teledentistry and silver diamine fluoride widen access."),
    ("DN-3.3.F", J("CC55", "FK7"), "Apply quality assurance: audit, compare against a standard and fix the process.",
     "Plan–Do–Study–Act cycles; weekly biological (spore) testing of sterilisers; a failed spore test means retest, recall loads and repair."),
    ("DN-2.5.A", J("FK2", "CC21"), "Relate plaque pH to enamel and root demineralisation, and fluoride to the critical pH.",
     "Hydroxyapatite dissolves below about pH 5.5, fluorapatite below about 4.5, root dentin near 6.2–6.7; each sugar exposure drops plaque pH for 20–40 minutes (Stephan curve)."),
    ("DN-2.5.B", J("FK2", "FK1"), "Use the bicarbonate buffer to compute salivary pH and explain how flow changes it.",
     "pH = 6.1 + log([HCO₃⁻]/(0.03·P_CO₂)); stimulated saliva carries more bicarbonate and buffers better."),
    ("DN-2.5.C", J("FK5", "CC22"), "Match the host's defences to the stages of gingival and periodontal disease.",
     "Neutrophils dominate the early lesion; T cells, then B and plasma cells, the established and advanced lesions; secretory IgA and lysozyme defend saliva; host enzymes (MMPs) and RANKL drive tissue and bone loss."),
    ("DN-2.5.D", J("FK5", "FK7", "CC51"), "Interpret immunisation and exposure tests for dental personnel.",
     "Anti-HBs ≥ 10 mIU/mL after the hepatitis B series means protection; a non-responder repeats the series once; post-exposure HIV prophylaxis should start within hours (ideally under 2, at most 72)."),
]

DX, MG, PP, PH, MB = "dent.clinical", "dent.clinical", "dent.behavior", "dent.pharm", "dent.biomed"

ADD = [
    ("DN-1.4.A", facts("dn-history-exam", DX, [
        ("A patient says 'my tooth hurts when I drink something cold and stops in a few seconds'. What is this part of the record?", "The chief complaint, in the patient's words", "The diagnosis", "The treatment plan", "The medical history"),
        ("In what order is a comprehensive examination usually done?", "Extraoral head and neck, then intraoral soft tissue, then teeth and periodontium", "Teeth first, then soft tissue", "Radiographs before any history", "Periodontal probing before the medical history"),
        ("A firm, fixed, painless cervical node is found. What is the concern?", "Possible malignancy: it needs follow-up or referral", "Normal reactive node", "Salivary stone", "Nothing; nodes are always benign"),
        ("Where else should a dentist look for information on a patient with a complex history?", "Physician records, prior dental records and the patient's caregiver", "Only the patient's memory", "Online forums", "No other source is allowed"),
    ], "History before examination, extraoral before intraoral, and every source that helps", pace="quick")),
    ("DN-1.4.A", facts("dn-pain-history", DX, [
        ("Pain that wakes the patient at night and lingers after cold points to which pulpal state?", "Symptomatic irreversible pulpitis", "Reversible pulpitis", "Normal pulp", "Pulp necrosis without symptoms"),
        ("Sharp pain only on biting release on one cusp suggests what?", "Cracked tooth", "Pulp necrosis", "Periodontal abscess", "Sinusitis"),
        ("Diffuse pain in several upper molars that worsens on bending over suggests what?", "Maxillary sinusitis", "Irreversible pulpitis of one tooth", "TMJ disc displacement", "Trigeminal neuralgia"),
        ("Brief electric-shock pain triggered by touching the face suggests what?", "Trigeminal neuralgia", "Reversible pulpitis", "Myofascial pain", "Dry socket"),
    ], "The pain's character, trigger and duration point to its source before any test", pace="quick")),
    ("DN-1.4.B", facts("dn-plan-phase", DX, [
        ("A patient has an acute abscess, uncontrolled caries and wants veneers. What comes first?", "Relieve the acute problem", "Place the veneers", "Fabricate a bridge", "Orthodontics"),
        ("After urgent care, which phase comes next?", "Disease control: caries removal, periodontal therapy, oral hygiene", "Definitive prosthetics", "Maintenance recall", "Cosmetic whitening"),
        ("Where does medical consultation for uncontrolled hypertension fit?", "The systemic phase, before elective treatment", "After the crowns", "During maintenance only", "It is not part of the plan"),
        ("Which phase keeps the result over years?", "Maintenance", "Urgent", "Disease control", "Systemic"),
    ], "Systemic → urgent → disease control → definitive → maintenance")),
    ("DN-1.4.B", facts("dn-predict-result", DX, [
        ("A tooth has a deep restoration and a periapical radiolucency, and the patient feels nothing. Cold test result most likely?", "No response (necrotic pulp)", "Lingering pain", "Brief normal response", "Exaggerated response that fades"),
        ("A tooth hurts on percussion after a new high filling, with normal pulp. Cold test result most likely?", "Normal brief response", "No response", "Lingering severe pain", "Pain only to heat"),
        ("A periodontal pocket of 8 mm on one root surface of a vital tooth. Pulp test result most likely?", "Responds normally", "No response", "Lingering pain", "Cannot be tested"),
        ("A child's primary molar has a fistula. Radiograph most likely shows what?", "Furcation radiolucency", "A normal periodontal ligament", "Root canal calcification only", "A supernumerary tooth"),
    ], "Predict before testing: the history usually tells the test result", pace="quick")),
    ("DN-1.4.C", facts("dn-informed-consent", PP, [
        ("What must informed consent include?", "The diagnosis, the proposed treatment, alternatives including no treatment, risks and benefits", "Only the cost", "Only the treatment name", "The dentist's credentials"),
        ("A patient refuses recommended radiographs after an explanation. What is done?", "Document the informed refusal and its risks", "Treat anyway", "Dismiss the patient at once", "Take them without telling"),
        ("A minor needs elective treatment. Who usually gives consent?", "A parent or legal guardian", "The minor alone", "The dental assistant", "No one needs to"),
        ("Which question opens a motivational conversation about flossing?", "'What would make flossing easier for you?'", "'Why don't you floss?'", "'You must floss daily.'", "'Do you floss? Yes or no.'"),
    ], "Consent is a process of explanation; refusal must be informed and recorded", pace="quick")),
    ("DN-1.4.C", facts("dn-patient-adapt", PP, [
        ("A 6-year-old is anxious about a first filling. Which technique fits?", "Tell-show-do", "General anaesthesia at once", "Restraint without consent", "Skipping explanation"),
        ("An 80-year-old on several medications has many root caries. Which factor is most likely?", "Drug-induced xerostomia", "Too much fluoride", "Childhood habits", "Bruxism alone"),
        ("A patient speaks little English. What is best?", "A trained medical interpreter", "A child family member translating", "Proceeding with gestures", "Postponing indefinitely"),
        ("A patient with limited hand dexterity struggles to brush. What helps?", "A power toothbrush or an adapted handle", "Brushing less often", "Stopping flossing", "Only mouthwash"),
    ], "Adapt explanation, technique and home care to the person in the chair", pace="quick")),
    ("DN-1.4.D", Q("dn-eag", DX, "A patient's HbA1c is {{a1c}}%. What is the estimated average glucose, in mg/dL?",
        given={"a1c": {"pick": [6, 7, 8, 9, 10]}}, value="28.7*a1c - 46.7", tex="eAG", verify="Rational(287, 10)*a1c - Rational(467, 10)",
        explain="eAG = 28.7 × A1c − 46.7 (ADAG study); A1c reflects about three months of glucose, and poor control worsens periodontitis and healing")),
    ("DN-1.4.D", facts("dn-oral-systemic", DX, [
        ("How do periodontitis and diabetes interact?", "Each worsens the other; periodontal therapy can modestly lower HbA1c", "Diabetes protects the periodontium", "They are unrelated", "Periodontitis causes type 1 diabetes"),
        ("A patient on a bisphosphonate for cancer needs an extraction. What is the main concern?", "Medication-related osteonecrosis of the jaw", "Excess bleeding", "Allergy to anaesthetic", "Faster healing"),
        ("Which oral sign suggests undiagnosed HIV infection?", "Oral hairy leukoplakia", "Fordyce granules", "Linea alba", "Torus palatinus"),
        ("A pregnant patient has bleeding, swollen gums. Most likely cause?", "Hormone-enhanced plaque-induced gingivitis", "Leukaemia in every case", "Vitamin C excess", "Fluorosis"),
    ], "Oral findings can reveal systemic disease, and systemic disease changes oral treatment", pace="quick")),
    ("DN-2.4.A", Q("dn-mme", PH, "A patient is prescribed {{drug}} {{mg}} mg every {{h}} hours. What is the daily dose in morphine milligram equivalents (CDC 2022 factors)?",
        cases=[{"drug": "hydrocodone", "mg": 5, "h": 6, "f": 1}, {"drug": "oxycodone", "mg": 5, "h": 6, "f": 1.5}, {"drug": "codeine", "mg": 30, "h": 4, "f": 0.15}, {"drug": "hydrocodone", "mg": 10, "h": 4, "f": 1}],
        value="mg*(24/h)*f", tex="MME", verify="mg*Rational(24, h)*nsimplify(f)",
        explain="MME/day = mg per dose × doses per day × factor; most acute dental pain needs no opioid, and NSAIDs with acetaminophen work better")),
    ("DN-2.4.A", facts("dn-substance-use", PH, [
        ("A patient used cocaine this morning. What about local anaesthetic with epinephrine?", "Avoid epinephrine; defer elective care at least 24 hours", "Use double the epinephrine", "It is safe at any dose", "Use felypressin-free only if over 60"),
        ("Rampant smooth-surface caries on buccal surfaces with xerostomia and bruxism suggests what?", "Methamphetamine use", "Fluorosis", "Amelogenesis imperfecta", "Bulimia only"),
        ("A heavy drinker needs pain relief after an extraction. Which drug needs the most caution?", "Acetaminophen (liver toxicity)", "Topical benzocaine", "Chlorhexidine rinse", "Saline rinse"),
        ("A patient in recovery from opioid use disorder needs an extraction. Best analgesic plan?", "Non-opioid: ibuprofen with acetaminophen", "Oxycodone for 7 days", "Codeine syrup", "No analgesia"),
    ], "Ask about substance use; it changes anaesthetic, analgesic and caries plans", pace="quick")),
    ("DN-2.4.B", Q("dn-golden-proportion", DX, "Seen from the front, a maxillary central incisor is {{c}} mm wide. Following the golden proportion (1.618 : 1 : 0.618), how wide should the {{tooth}} appear, in mm?",
        cases=[{"c": 8.5, "tooth": "lateral incisor", "k": 1}, {"c": 8.5, "tooth": "canine", "k": 2}, {"c": 9, "tooth": "lateral incisor", "k": 1}, {"c": 8, "tooth": "canine", "k": 2}],
        value="c/1.618^k", tex="w", verify="nsimplify(c)/Rational(1618, 1000)**k",
        explain="Each tooth appears about 0.618 times as wide as the one in front of it; the ratio is a guide, not a rule")),
    ("DN-2.4.B", facts("dn-esthetic-tissue", DX, [
        ("A crown margin is placed 1 mm from the alveolar crest. What is the risk?", "Violating the supracrestal tissue attachment: chronic inflammation or bone loss", "None", "Faster healing", "Better esthetics"),
        ("A patient has a gummy smile from excess gingiva over short crowns. Which procedure fits?", "Esthetic crown lengthening", "Free gingival graft", "Frenectomy only", "Extraction"),
        ("A thin-biotype patient has recession exposing a root. Which procedure covers it?", "Connective tissue graft", "Gingivectomy", "Scaling only", "Apicoectomy"),
        ("Tetracycline-stained teeth need masking. What usually works best?", "Veneers or crowns", "Over-the-counter whitening strips alone", "Microabrasion", "Fluoride varnish"),
    ], "Keep about 3 mm from margin to bone; match the procedure to the tissue problem", pace="quick")),
    ("DN-2.4.C", Q("dn-afr", DX, "{{surv}}% of restorations of a type survive {{yr}} years. What is the annual failure rate, in %?",
        cases=[{"surv": 90, "yr": 10}, {"surv": 85, "yr": 5}, {"surv": 95, "yr": 5}, {"surv": 70, "yr": 12}],
        value="100*(1 - (surv/100)^(1/yr))", tex="AFR", verify="100*(1 - Rational(surv, 100)**Rational(1, yr))",
        explain="Survival compounds: S = (1 − AFR)^years, so AFR = 1 − S^(1/years); below about 2% a year is good for direct restorations")),
    ("DN-2.4.C", facts("dn-outcome", DX, [
        ("Two years after scaling and root planing, probing depths are back to 6 mm. What does that indicate?", "Disease not controlled: reassess and consider surgery or referral", "Success", "Normal healing", "Need for whitening"),
        ("A patient at high caries risk has new lesions at each visit. Recall interval?", "Shorter, often 3–4 months", "Every 2 years", "Only when in pain", "Never"),
        ("Which outcome measure best tracks periodontal stability over time?", "Clinical attachment level and bleeding on probing", "Tooth shade", "Number of fillings", "Patient age"),
        ("An implant has bleeding, suppuration and bone loss beyond remodelling. Name?", "Peri-implantitis", "Peri-implant mucositis", "Osseointegration", "Normal remodelling"),
    ], "Measure outcomes with the same measures used to diagnose, and set recall by risk", pace="quick")),
    ("DN-3.3.A", facts("dn-referral", PP, [
        ("A general dentist sees a suspicious ulcer that has not healed in 3 weeks. What is required?", "Biopsy or referral for biopsy", "Watch for a year", "Prescribe antibiotics only", "Nothing"),
        ("A case exceeds the dentist's training. What does ethics require?", "Refer to a qualified colleague", "Attempt it anyway", "Refuse care without explanation", "Ask the assistant to do it"),
        ("After a referral, who coordinates the overall care plan?", "The referring general dentist stays involved", "No one", "The patient alone", "Only the specialist forever"),
        ("How does a dentist best judge their own competence in a new procedure?", "Training, audited outcomes and peer review", "Confidence alone", "Patient reviews only", "Years since graduation"),
    ], "Practise within competence; refer and follow up when a case exceeds it", pace="quick")),
    ("DN-3.3.A", facts("dn-scope", PP, [
        ("Which is usually outside a general dentist's scope?", "Prescribing for a patient's unrelated hypertension", "Extracting an erupted tooth", "Placing a composite", "Taking radiographs"),
        ("A patient asks for Botox for forehead wrinkles. What determines whether a dentist may provide it?", "The state dental practice act", "The patient's wishes", "The manufacturer", "Nothing; it is always allowed"),
        ("A complex impacted third molar near the inferior alveolar canal. Usual choice?", "Refer to an oral and maxillofacial surgeon", "Extract with no imaging", "Leave without discussion", "Assign to the hygienist"),
        ("Which continuing-education choice best keeps competence current?", "Courses matched to gaps found in one's own outcomes", "Any course with free food", "None after licensure", "Only sales seminars"),
    ], "Scope is set by training and by state law", pace="quick")),
    ("DN-3.3.B", Q("dn-overhead", PP, "A practice collects {{col}} thousand dollars a year and spends {{ex}} thousand on expenses. Production was {{pr}} thousand. What is the {{what}}, in %?",
        cases=[{"col": 900, "ex": 600, "pr": 950, "what": "overhead", "w": 0}, {"col": 900, "ex": 600, "pr": 950, "what": "collection ratio", "w": 1},
               {"col": 1200, "ex": 720, "pr": 1250, "what": "overhead", "w": 0}, {"col": 760, "ex": 500, "pr": 800, "what": "collection ratio", "w": 1}],
        value="w == 0 ? 100*ex/col : 100*col/pr", tex="\\%", verify="100*[Rational(ex, col), Rational(col, pr)][w]",
        explain="Overhead = expenses ÷ collections; collection ratio = collections ÷ production (aim near 98%)")),
    ("DN-3.3.B", facts("dn-osha-hipaa", PP, [
        ("Which law protects the privacy of patient health information?", "HIPAA", "OSHA", "ADA Title III", "FDA"),
        ("Which agency's standard requires hepatitis B vaccination to be offered to exposed staff?", "OSHA (bloodborne pathogens standard)", "HIPAA", "DEA", "EPA"),
        ("A staff member emails radiographs to a patient's lawyer without authorisation. Problem?", "A HIPAA breach", "An OSHA violation", "Nothing", "A DEA issue"),
        ("Which document must a practice keep for each hazardous chemical?", "A safety data sheet", "A HIPAA notice", "A W-2 form", "A prescription log"),
    ], "HIPAA protects patients' information; OSHA protects workers", pace="quick")),
    ("DN-3.3.C", facts("dn-disaster-plan", PP, [
        ("Which belongs in a dental practice's emergency plan?", "Staff roles, evacuation routes, emergency contacts and off-site data backup", "Only a fire extinguisher", "Only insurance papers", "Nothing written"),
        ("Patient records should survive a flood. What helps most?", "Encrypted off-site or cloud backup", "Paper only in the basement", "A single local hard drive", "No backup"),
        ("How can dentists help after a mass-casualty event?", "Identify victims by comparing dental records", "Prescribing for victims' families", "Running the shelters", "No role"),
        ("How often should staff practise the emergency plan?", "Regularly, with drills at least yearly", "Never", "Only after an emergency", "Every ten years"),
    ], "A plan nobody has practised does not work", pace="quick")),
    ("DN-3.3.C", facts("dn-office-preparedness", PP, [
        ("Which item must every dental office have ready?", "Oxygen and an emergency drug kit, plus an AED where required", "A dental laser", "An intraoral camera", "A panoramic unit"),
        ("A power outage occurs mid-procedure. First priority?", "Patient safety: stop, stabilise and use backup lighting", "Finish the crown", "Leave the office", "Call the lab"),
        ("Who should be trained in basic life support?", "All clinical staff", "Only the dentist", "Only the receptionist", "No one"),
        ("Where should emergency numbers be kept?", "Posted visibly by phones", "Only in the dentist's memory", "In a locked drawer", "Nowhere"),
    ], "Readiness is equipment, training and drills", pace="quick")),
    ("DN-3.3.D", facts("dn-supervision", PP, [
        ("The dentist must be in the office and check the work before the patient leaves. What level of supervision?", "Direct", "General", "Indirect only by phone", "None"),
        ("A hygienist cleans teeth in a nursing home with the dentist's prior authorisation but no dentist present. Level?", "General supervision (where state law allows)", "Direct", "Personal", "Unsupervised"),
        ("Who decides which duties an assistant may legally perform?", "The state dental practice act", "The dentist alone", "The patient", "The manufacturer"),
        ("An assistant is asked to perform a duty not allowed in the state. What is right?", "Decline; the dentist is responsible for illegal delegation", "Do it quietly", "Do it if the patient agrees", "Ask another assistant"),
    ], "Supervision levels and allowed duties are usually defined state by state", pace="quick")),
    ("DN-3.3.D", facts("dn-delegation", PP, [
        ("Which task can only a dentist perform?", "Diagnosis and treatment planning", "Taking radiographs", "Polishing", "Recording a chart"),
        ("An expanded-function assistant places a restoration. Who is responsible for it?", "The supervising dentist", "The assistant alone", "The lab", "The patient"),
        ("A new assistant is unsure how to set up a procedure. Best response?", "Train and verify before delegating", "Let them guess", "Skip the step", "Ask the patient"),
        ("Which team practice reduces errors in a busy office?", "Standard checklists and clear hand-offs", "Verbal orders only", "Skipping time-outs", "Rotating roles without training"),
    ], "Delegate only what the law allows and the person has been trained to do", pace="quick")),
    ("DN-3.3.E", Q("dn-dmft", DX, "In a survey of {{n}} children, the counts were {{d}} decayed, {{m}} missing (due to caries) and {{f}} filled permanent teeth. What is the mean DMFT?",
        given={"n": {"pick": [50, 80, 120]}, "d": {"pick": [60, 90]}, "m": {"pick": [6, 12]}, "f": {"pick": [40, 75]}},
        value="(d + m + f)/n", tex="DMFT", verify="Rational(d + m + f, n)", explain="DMFT counts teeth decayed, missing or filled because of caries; the mean is the total over the number examined")),
    ("DN-3.3.E", facts("dn-community", DX, [
        ("What fluoride level does the U.S. Public Health Service recommend in community water (2015)?", "0.7 mg/L", "1.5 mg/L", "4.0 mg/L", "0.1 mg/L"),
        ("Which school programme prevents most occlusal caries in children?", "Sealants on permanent molars", "Annual radiographs", "Whitening", "Mouthguards"),
        ("Silver diamine fluoride is used for what?", "Arresting cavitated caries without drilling, at the cost of black staining", "Whitening", "Local anaesthesia", "Bonding crowns"),
        ("Which emerging approach widens access in rural areas?", "Teledentistry linked to community hygienists", "More private practices only", "Higher fees", "Closing clinics"),
    ], "Population programmes prevent more disease per dollar than individual treatment", pace="quick")),
    ("DN-3.3.F", Q("dn-spore-rate", PP, "A practice ran {{n}} weekly spore tests last year and {{fails}} failed. What percent passed?",
        given={"n": {"pick": [50, 52]}, "fails": {"pick": [1, 2, 3]}}, value="100*(n - fails)/n", tex="\\%", verify="100*Rational(n - fails, n)",
        explain="Every failure triggers retesting, a review of loads since the last pass and steriliser repair; the audit asks why it failed")),
    ("DN-3.3.F", facts("dn-quality", PP, [
        ("A spore test fails. What comes first?", "Take the steriliser out of service and retest; review loads since the last pass", "Ignore one failure", "Use it until the next week", "Throw away all instruments"),
        ("What is the Plan–Do–Study–Act cycle for?", "Testing a change on a small scale and learning before spreading it", "Billing patients", "Scheduling recalls", "Sterilising instruments"),
        ("An audit finds 20% of charts lack a medical history update. Best next step?", "Change the check-in process and re-audit", "Blame the receptionist", "Stop auditing", "Delete those charts"),
        ("How often should sterilisers usually be tested with biological indicators?", "At least weekly", "Yearly", "Never", "Only after repair"),
    ], "Quality improvement measures, changes the process and measures again", pace="quick")),
    ("DN-2.5.A", facts("dn-critical-ph", MB, [
        ("Below about what plaque pH does enamel hydroxyapatite start to dissolve?", "5.5", "7.0", "4.5", "3.0"),
        ("Why does fluoride protect enamel in an acid attack?", "Fluorapatite forms, which needs a lower pH (about 4.5) to dissolve", "It neutralises all acid", "It kills every bacterium", "It thickens enamel"),
        ("Why are exposed roots more vulnerable than enamel?", "Root dentin and cementum dissolve at a higher pH (about 6.2–6.7)", "They contain more fluoride", "Saliva cannot reach them", "They are harder"),
        ("A patient sips a sweet drink all afternoon. Why is that worse than one quick drink?", "Plaque pH stays below the critical value for hours", "Total sugar is lower", "Saliva flow stops", "pH rises with each sip"),
    ], "Caries is a balance of demineralisation below the critical pH and remineralisation above it")),
    ("DN-2.5.A", Q("dn-ph-hplus", MB, "Plaque pH falls from {{p1}} to {{p2}} after a sugar rinse. By what factor does [H⁺] rise?",
        given={"p1": {"pick": [6.8, 7.0]}, "p2": {"pick": [5.0, 4.5, 5.5]}}, value="10^(p1 - p2)", tex="\\times",
        verify="Integer(10)**(nsimplify(p1) - nsimplify(p2))", explain="pH is −log[H⁺], so each unit is a factor of ten in acidity")),
    ("DN-2.5.B", Q("dn-saliva-ph", MB, "Saliva has [HCO₃⁻] = {{hc}} mM and P_CO₂ = {{pco}} mmHg. Using pH = 6.1 + log([HCO₃⁻]/(0.03·P_CO₂)), what is its pH?",
        cases=[{"hc": 5, "pco": 40, "st": 0}, {"hc": 15, "pco": 40, "st": 1}, {"hc": 30, "pco": 45, "st": 1}, {"hc": 2, "pco": 40, "st": 0}],
        value="6.1 + log10(hc/(0.03*pco))", tex="pH", verify="Rational(61, 10) + log(nsimplify(hc)/(Rational(3, 100)*pco), 10)",
        explain="Henderson–Hasselbalch on the bicarbonate system; stimulated saliva carries more bicarbonate, so its pH and buffering are higher")),
    ("DN-2.5.B", facts("dn-saliva-function", MB, [
        ("Which salivary component is the main buffer?", "Bicarbonate", "Amylase", "Mucin", "Lysozyme"),
        ("Which gland supplies most stimulated saliva?", "Parotid", "Sublingual", "Minor glands", "Lacrimal"),
        ("Which protein in saliva keeps calcium phosphate supersaturated so it does not precipitate?", "Statherin", "Amylase", "Lactoferrin", "IgG"),
        ("Why do patients with xerostomia get rampant caries?", "Less buffering, clearance and remineralisation", "More fluoride", "More bicarbonate", "Faster pellicle loss"),
    ], "Saliva buffers, clears sugar and supplies minerals for repair", pace="quick")),
    ("DN-2.5.C", facts("dn-perio-immune", MB, [
        ("Which cell dominates the initial lesion of gingivitis?", "Neutrophils", "Plasma cells", "Osteoclasts", "Eosinophils"),
        ("Which cell dominates the advanced periodontal lesion?", "Plasma cells (B cells)", "Neutrophils", "Mast cells", "Platelets"),
        ("Which signal drives osteoclasts to resorb alveolar bone?", "RANKL", "IgA", "Lysozyme", "Statherin"),
        ("Which antibody class protects mucosal surfaces in saliva?", "Secretory IgA", "IgE", "IgM", "IgD"),
    ], "Tissue destruction in periodontitis is mostly the host's own response to the biofilm")),
    ("DN-2.5.C", facts("dn-host-modulation", MB, [
        ("Sub-antimicrobial-dose doxycycline is used in periodontitis to do what?", "Inhibit host collagenases (MMPs)", "Kill all bacteria", "Whiten teeth", "Raise IgE"),
        ("A patient with neutrophil defects (e.g. leukocyte adhesion deficiency) shows what?", "Severe early periodontitis", "Fewer caries", "Thicker enamel", "Nothing oral"),
        ("Why does smoking mask gingival bleeding?", "Vasoconstriction and impaired inflammatory response", "Nicotine kills bacteria", "It strengthens the epithelium", "It raises IgA"),
        ("Why does poorly controlled diabetes worsen periodontitis?", "Glycation products amplify inflammation and impair neutrophils", "Glucose kills bacteria", "Insulin dissolves bone", "It raises saliva flow"),
    ], "Host modulation targets the response, not only the bacteria", pace="quick")),
    ("DN-2.5.D", facts("dn-hbv-titer", MB, [
        ("After the hepatitis B series, a dental student's anti-HBs is 50 mIU/mL. Status?", "Protected (at least 10 mIU/mL)", "Not protected", "Infected", "Needs immunoglobulin"),
        ("Anti-HBs is below 10 mIU/mL after a full series. Usual next step?", "Repeat the series once and retest", "No further action", "Assume immunity", "Start antiretrovirals"),
        ("After a needlestick from a source with HIV, when should prophylaxis start?", "As soon as possible, ideally within hours", "After 2 weeks", "Only if symptoms appear", "Never"),
        ("Which virus has the highest transmission risk after a needlestick from an infected source?", "Hepatitis B", "HIV", "Hepatitis C", "Influenza"),
    ], "Know your titre; act on an exposure within hours")),
    ("DN-2.5.D", Q("dn-needlestick-risk", MB, "Rough transmission risks per needlestick are hepatitis B (e-antigen positive) 30%, hepatitis C 1.8% and HIV 0.3%. A clinic records {{n}} needlesticks from {{src}} sources. About how many transmissions are expected without prophylaxis?",
        cases=[{"n": 100, "src": "HIV-positive", "p": 0.003}, {"n": 50, "src": "hepatitis C-positive", "p": 0.018}, {"n": 20, "src": "HBeAg-positive hepatitis B", "p": 0.3}, {"n": 1000, "src": "HIV-positive", "p": 0.003}],
        value="n*p", tex="N", verify="n*nsimplify(p)", explain="Expected cases = exposures × risk per exposure; vaccination makes the hepatitis B risk near zero")),
]
