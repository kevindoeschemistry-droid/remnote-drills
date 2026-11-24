"""Biosecurity framework (BS) items: two question types per objective, written together here (the framework is new, so
these are its first and second types). Policy and defence level only: epidemic arithmetic, surveillance, biosafety,
treaties, screening, oversight, clean air, PPE, countermeasures and governance. No item may help anyone make, enhance or
deploy a pathogen. Arithmetic is recomputed by sympy along another route; facts are authored and dated."""
from opl_dsl import Q

FILE, FRAMEWORK = "bs-biosecurity", "biosecurity"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
n = lambda v: f"nsimplify({v})"


def facts(name, skill, rows, explain, pace="recall"):
    return Q(name, skill, "{{q}}", pace=pace, cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


ADD = [
    # ── 1 pandemic-proof world ───────────────────────────────────────────
    ("BS-1.1.A", Q("bs-doubling-time", "biosec.epidemiology", "An outbreak has R = {{R}} and a generation interval of {{Tg}} days (treat it as fixed). What is the doubling time, in days?",
        given={"R": {"pick": [1.3, 1.5, 2, 2.5, 3]}, "Tg": {"pick": [3, 5, 7]}}, value="log(2)/(log(R)/Tg)", tex="T_d",
        verify=f"Tg*log(2)/log({n('R')})", explain="r = ln R / T_g, then T_d = ln 2 / r: the same R doubles faster with a shorter generation interval")),
    ("BS-1.1.A", Q("bs-r-from-doubling", "biosec.epidemiology", "Cases double every {{Td}} days and the generation interval is {{Tg}} days (fixed). What is R?",
        given={"Td": {"pick": [2.5, 3, 4, 7]}, "Tg": {"pick": [3, 5, 6]}}, value="exp(log(2)/Td*Tg)", tex="R",
        verify=f"2**({n('Tg')}/{n('Td')})", explain="R = e^{rT_g} with r = ln 2 / T_d, which is 2^{T_g/T_d}: R doublings per generation")),
    ("BS-1.1.B", Q("bs-herd-threshold", "biosec.epidemiology", "A pathogen has R₀ = {{R0}}. What fraction of the population must be immune for herd protection, in %?",
        given={"R0": {"pick": [1.5, 2, 3, 4, 6, 12]}}, value="100*(1 - 1/R0)", tex="\\%", verify=f"solve(Eq({n('R0')}*(1 - x/100), 1), x)[0]",
        explain="Spread stops once each case infects fewer than one: R₀(1 − p) < 1")),
    ("BS-1.1.B", Q("bs-r0-from-threshold", "biosec.epidemiology", "Herd protection against a pathogen needs {{h}}% of the population immune. What R₀ does that imply?",
        given={"h": {"pick": [50, 60, 75, 80, 90, 95]}}, value="1/(1 - h/100)", tex="R_0", verify=f"solve(Eq(1 - 1/x, Rational(h, 100)), x)[0]",
        explain="p = 1 − 1/R₀, so R₀ = 1/(1 − p): measles-like thresholds (~95%) mean R₀ near 20")),
    ("BS-1.1.C", Q("bs-ifr-from-cfr", "biosec.epidemiology", "{{d}} deaths follow {{c}} confirmed cases, but only {{a}}% of infections were confirmed. What is the infection fatality ratio, in %?",
        given={"d": {"pick": [12, 30, 75]}, "c": {"pick": [1000, 2500, 5000]}, "a": {"pick": [10, 20, 40]}}, value="100*d/(c/(a/100))", tex="\\mathrm{IFR}",
        verify="100*d/c*Rational(a, 100)", explain="IFR = CFR × ascertainment: counting only the sick inflates apparent lethality")),
    ("BS-1.1.C", facts("bs-fatality-bias", "biosec.epidemiology", [
        ("Early in an outbreak, mild infections are rarely tested. How does that bias the case fatality ratio?", "Upward: the denominator misses mild infections", "Downward", "Not at all", "It makes it zero"),
        ("Deaths lag cases by weeks. Dividing deaths to date by cases to date during rapid growth biases the CFR how?", "Downward: recent cases have not yet had time to die", "Upward", "Not at all", "It doubles it"),
        ("Which ratio uses all infections, including those never tested, as its denominator?", "The infection fatality ratio", "The case fatality ratio", "The attack rate", "R₀"),
    ], "Ascertainment inflates the CFR; reporting lag deflates it during growth")),
    ("BS-1.2.A", facts("bs-history-facts", "biosec.landscape", [
        ("In which year did the WHO certify the eradication of smallpox?", "1980", "1967", "1977", "1995"),
        ("The 1979 anthrax outbreak at Sverdlovsk was later traced to what?", "An accidental release from a military facility", "Contaminated meat only", "A natural animal outbreak", "A terrorist attack"),
        ("In which year was the Biological Weapons Convention opened for signature?", "1972", "1925", "1993", "2001"),
        ("The 1925 Geneva Protocol did what?", "Banned the use (not the development or stockpiling) of chemical and biological weapons in war", "Banned all biological research", "Created the WHO", "Set up verification inspections"),
    ], "Use was banned in 1925; development and stockpiling only in 1972, and without verification")),
    ("BS-1.2.A", facts("bs-history-order", "biosec.landscape", [
        ("Which came first?", "The Geneva Protocol", "The BWC", "Smallpox eradication", "The 2001 anthrax letters"),
        ("Which came last?", "The WHO Pandemic Agreement's adoption", "The IHR (2005)", "The BWC entering into force", "UNSCR 1540"),
        ("Which happened between the BWC's entry into force (1975) and smallpox eradication (1980)?", "The Sverdlovsk anthrax release (1979)", "The 1918 influenza pandemic", "The Geneva Protocol", "The 2001 anthrax letters"),
    ], "1925 Geneva Protocol · 1972/1975 BWC · 1979 Sverdlovsk · 1980 smallpox · 2001 letters · 2004 UNSCR 1540 · 2005 IHR · 2025 Pandemic Agreement")),
    ("BS-1.2.B", facts("bs-risk-source", "biosec.landscape", [
        ("A virus jumps from bats to people through an intermediate animal at a market. Which kind of risk is this?", "Natural (zoonotic spillover)", "Accidental", "Deliberate", "None"),
        ("A researcher is infected through a needle-stick and carries an agent out of the lab. Which kind?", "Accidental (laboratory-acquired)", "Natural", "Deliberate", "Agricultural"),
        ("A group seeks to cause harm by releasing an agent. Which kind?", "Deliberate", "Natural", "Accidental", "Environmental"),
    ], "Natural, accidental and deliberate risks need different layers: surveillance and One Health, biosafety, and nonproliferation")),
    ("BS-1.2.B", facts("bs-gcbr-features", "biosec.landscape", [
        ("Which combination most raises a biological event toward global catastrophe?", "High transmissibility, high severity and poor countermeasures", "Low transmissibility but high severity", "A slow-growing local outbreak", "A well-understood pathogen with a vaccine stockpile"),
        ("Why do biosecurity planners worry about 'stealth' spread?", "Long presymptomatic spread defeats symptom-based detection", "It makes vaccines unnecessary", "It is always mild", "It needs no surveillance"),
        ("Which factor most improves society's ability to respond?", "Time between detection and wide spread", "A shorter doubling time", "Fewer diagnostic tests", "Less international reporting"),
    ], "Scale depends on the pathogen and on our response: detection time and countermeasures are levers")),
    # ── 2 prevent ────────────────────────────────────────────────────────
    ("BS-2.1.A", facts("bs-bwc-facts", "biosec.prevent", [
        ("What does the BWC lack that the Chemical Weapons Convention has?", "A verification body with inspections", "A ban on development", "Review conferences", "States Parties"),
        ("Which BWC article contains the core prohibition on developing, producing and stockpiling?", "Article I", "Article X", "Article XII", "Article VII"),
        ("What are the BWC's confidence-building measures?", "Annual voluntary declarations of relevant facilities and activities", "Surprise inspections", "Sanctions", "Export licences"),
        ("Roughly how many States Parties does the BWC have (2026)?", "About 189", "About 60", "About 120", "Every UN member"),
    ], "The BWC rests on national implementation, consultation and transparency, not inspection")),
    ("BS-2.1.A", facts("bs-bwc-scenario", "biosec.prevent", [
        ("A State Party suspects another of breaching the Convention. Which route does the BWC itself provide?", "Consult bilaterally, then lodge a complaint with the UN Security Council (Article VI)", "Ask the OPCW to inspect", "Refer it to the WHO", "Impose sanctions itself under Article I"),
        ("A State Party wants to share vaccine technology for peaceful purposes. Which article supports this?", "Article X (peaceful cooperation)", "Article I", "Article III", "Article VI"),
        ("A State Party passes laws making BWC violations crimes for individuals. Which obligation is it meeting?", "Article IV (national implementation)", "Article XII", "Article X", "Article VII"),
    ], "Articles I–IV are obligations; V–VI consultation and complaint; VII assistance; X peaceful use; XII review")),
    ("BS-2.1.B", facts("bs-export-controls", "biosec.prevent", [
        ("What is the Australia Group?", "An informal forum that harmonises national export controls on chemical and biological items", "A treaty with inspections", "A WHO committee", "A vaccine alliance"),
        ("What does UN Security Council Resolution 1540 (2004) require of every state?", "Laws and controls keeping WMD and related materials from non-state actors", "Destroying all pathogens", "Joining the Australia Group", "Reporting every outbreak to the WHO"),
        ("Export controls on dual-use equipment chiefly aim to…", "Make it harder for proliferators to acquire it while allowing legitimate trade", "Stop all trade in lab equipment", "Fund vaccine research", "Classify research papers"),
    ], "Supply-side controls work through national licensing, coordinated lists and catch-all clauses")),
    ("BS-2.1.B", facts("bs-regime-match", "biosec.prevent", [
        ("Which instrument binds every UN member state, party or not?", "UNSCR 1540", "The BWC", "The Australia Group", "The IHR (2005)"),
        ("Which instrument is a political arrangement, not a treaty?", "The Australia Group", "The BWC", "The Geneva Protocol", "The IHR (2005)"),
        ("Which instrument obliges states to notify the WHO of potential public health emergencies?", "The IHR (2005)", "The BWC", "UNSCR 1540", "The Australia Group"),
    ], "Treaties bind parties; Security Council resolutions bind all members; the Australia Group coordinates")),
    ("BS-2.2.A", facts("bs-synthesis-screening", "biosec.prevent", [
        ("Gene synthesis screening checks which two things?", "The ordered sequence against sequences of concern, and the customer's legitimacy", "Only the price", "Only the shipping address", "The customer's publication record only"),
        ("Why do screening frameworks worry about benchtop DNA synthesisers?", "They move synthesis outside the provider's central screening", "They are too slow", "They only make RNA", "They are illegal everywhere"),
        ("Why screen short sequence windows, not just whole genes?", "Orders can be split into fragments that are assembled later", "Short sequences are always dangerous", "Whole genes cannot be screened", "To lower costs"),
    ], "Screening is a chokepoint: sequence, customer and fragment-splitting all have to be covered")),
    ("BS-2.2.A", facts("bs-screening-scenario", "biosec.prevent", [
        ("An order matches a regulated sequence and the customer is an unverified individual. What does good practice do?", "Hold the order and escalate for customer verification and review", "Ship it with a warning", "Delete the record", "Ship half of it"),
        ("An order matches a sequence of concern but comes from a verified vaccine lab with a legitimate need. What happens?", "It can proceed after review, with records kept", "It is always refused", "It is shipped without records", "The lab is reported to police automatically"),
        ("A flagged sequence turns out to be a harmless housekeeping gene that shares a short motif. What is that?", "A false positive, which review should clear", "A true positive", "A screening failure that must ship", "A reason to stop all screening"),
    ], "Screening flags; trained people decide, and both false negatives and false positives have costs")),
    ("BS-2.2.B", facts("bs-durc-facts", "biosec.prevent", [
        ("What is dual-use research of concern?", "Life-science research reasonably expected to yield knowledge or products that could be directly misapplied to cause significant harm", "Any research with two funders", "Research on two pathogens at once", "Research that is classified"),
        ("When are dual-use risks best weighed?", "Before funding and before publication, not only after", "Only after publication", "Never: science must be open", "Only by journals"),
        ("What is an information hazard?", "True information whose spread could enable harm", "False information", "Information in a hazard log", "A leaked password"),
    ], "Oversight works at proposal, conduct and communication stages")),
    ("BS-2.2.B", facts("bs-durc-scenario", "biosec.prevent", [
        ("A paper's defensive findings are valuable, but one methods paragraph would lower the barrier to misuse. A common response is…", "Publish the findings and restrict the sensitive methodological detail", "Retract the whole paper", "Publish everything at once", "Post the methods on social media"),
        ("A student proposes an experiment whose main output would be a more dangerous agent. What should happen first?", "Institutional dual-use review before any work begins", "Run it and decide later", "Publish the plan for feedback", "Hide it from review"),
        ("Which question best separates acceptable from concerning work?", "Does the benefit require creating or disclosing the dangerous capability?", "Is the lab well funded?", "Is the result surprising?", "Is the journal prestigious?"),
    ], "Seek the defensive benefit by routes that do not create or spread the dangerous capability")),
    ("BS-2.2.C", Q("bs-layered-miss", "biosec.prevent", "A misuse request must pass {{k}} independent safeguard layers, each missing {{m}}% of such requests. What percentage gets through all of them?",
        given={"k": {"int": [2, 4]}, "m": {"pick": [5, 10, 20, 30]}}, value="100*(m/100)^k", tex="\\%", verify="100*Rational(m, 100)**k",
        explain="Independent misses multiply; correlated failures (one jailbreak beats all layers) break this, which is why layers should differ")),
    ("BS-2.2.C", facts("bs-ai-safeguards", "biosec.prevent", [
        ("Which safeguard checks a model's inputs and outputs at deployment, separate from the model's own training?", "A classifier on prompts and completions", "Pretraining data filtering", "A model card", "Rate limits only"),
        ("What does a dangerous-capability evaluation measure?", "Whether a model meaningfully raises a user's ability to cause harm, relative to existing resources", "How fluent the model is", "Its training cost", "Whether it can browse"),
        ("Why give vetted researchers different access from the public?", "Access controls let legitimate defensive work proceed while limiting anonymous misuse", "To charge more", "Because the public cannot use APIs", "It is required by the BWC"),
    ], "Model safeguards stack: training, classifiers, evaluations, access and monitoring")),
    ("BS-2.3.A", facts("bs-lbm4-levels", "biosec.biosafety", [
        ("In the WHO Laboratory Biosafety Manual (4th ed.), what decides which controls a lab needs?", "A local risk assessment of the agent and the work", "The agent's risk group alone", "The building's age", "The country's income"),
        ("What are 'core requirements' in the 4th edition?", "The minimum controls, including good microbiological practice, that apply to all work", "Controls for the most dangerous agents only", "Optional guidance", "Rules for transport only"),
        ("What is residual risk?", "The risk that remains after control measures are applied", "The risk before any controls", "Risk from waste only", "Zero, once controls are in place"),
    ], "LBM4 replaced fixed levels with a risk-based ladder: core requirements → heightened control → maximum containment")),
    ("BS-2.3.A", facts("bs-lbm4-scenario", "biosec.biosafety", [
        ("A risk assessment finds the inherent risk is low for routine diagnostic work. What applies?", "Core requirements", "Maximum containment", "No controls at all", "Heightened control measures only"),
        ("An assessment finds a significant risk of airborne exposure that core requirements cannot bring to an acceptable level. What next?", "Add heightened control measures", "Stop all risk assessment", "Use core requirements anyway", "Move to the field"),
        ("Which step closes the WHO risk assessment cycle?", "Review the risks and the control measures", "Gather information", "Buy equipment", "Publish the results"),
    ], "Gather information → evaluate risks → develop a control strategy → select and implement controls → review")),
    ("BS-2.3.B", facts("bs-bsc-class", "biosec.biosafety", [
        ("Which biosafety cabinet protects the worker and the environment but not the sample?", "Class I", "Class II", "Class III", "A clean bench"),
        ("Which cabinet is the usual choice when the worker, the sample and the environment all need protection?", "Class II", "Class I", "A clean bench", "A fume hood"),
        ("Which is a gas-tight glove box used under the most stringent containment?", "Class III", "Class I", "Class II", "A laminar-flow clean bench"),
        ("Why is a laminar-flow clean bench not a biosafety cabinet?", "It blows filtered air toward the worker and protects only the sample", "It has no filter", "It is too small", "It is gas-tight"),
    ], "Inflow protects the worker, downflow through HEPA protects the sample, HEPA exhaust protects the environment")),
    ("BS-2.3.B", Q("bs-hepa-series", "biosec.biosafety", "A HEPA filter lets through {{p}}% of particles at its most penetrating size. Exhaust passes through {{k}} such filters in series. What fraction gets through?",
        given={"p": {"pick": [0.03, 0.01, 0.005]}, "k": {"int": [1, 3]}}, value="(p/100)^k", tex="P", verify=f"({n('p')}/100)**k",
        explain="A HEPA filter removes at least 99.97% at the most penetrating particle size (~0.3 µm); filters in series multiply their penetrations")),
    # ── 3 detect ─────────────────────────────────────────────────────────
    ("BS-3.1.A", facts("bs-surveillance-match", "biosec.detect", [
        ("Which system can pick up an infection in a community before anyone seeks care?", "Wastewater surveillance", "Hospital death records", "Insurance claims", "Annual surveys"),
        ("Which system can find a pathogen nobody is looking for?", "Untargeted metagenomic sequencing", "A PCR test for a known agent", "A rapid antigen test", "Syndromic counts of one disease"),
        ("Which system counts symptoms such as fever visits before a diagnosis is made?", "Syndromic surveillance", "Metagenomics", "Serology", "Genome sequencing of isolates"),
    ], "Each system trades speed, specificity and coverage; layering them shortens time to detection")),
    ("BS-3.1.A", facts("bs-ihr-facts", "biosec.detect", [
        ("Under the IHR (2005), who declares a Public Health Emergency of International Concern?", "The WHO Director-General, after advice from an Emergency Committee", "The UN Security Council", "The World Health Assembly by vote", "Any affected country"),
        ("What did the 2024 IHR amendments add (in force since September 2025)?", "A 'pandemic emergency' alert level above a PHEIC", "A ban on travel restrictions", "Inspections of laboratories", "A new treaty on weapons"),
        ("What must a State Party do under the IHR when an event may constitute a PHEIC?", "Notify the WHO within 24 hours of assessment", "Close its borders", "Inform the BWC ISU", "Wait for confirmation by sequencing"),
    ], "The IHR are legally binding on 196 States Parties and set the notification and alert rules")),
    ("BS-3.1.B", Q("bs-detection-delay", "biosec.detect", "Infections double every {{Td}} days. Detection comes {{dt}} days later than it could have. By what factor are infections larger at detection?",
        given={"Td": {"pick": [2.5, 3, 4, 7]}, "dt": {"pick": [7, 10, 14, 21]}}, value="2^(dt/Td)", tex="f", verify=f"exp(log(2)*{n('dt')}/{n('Td')})",
        explain="Each doubling time of delay doubles the problem: two weeks at three-day doubling is about 25×")),
    ("BS-3.1.B", Q("bs-days-to-threshold", "biosec.detect", "An outbreak starts from {{I0}} infections and doubles every {{Td}} days. A system reliably detects it at {{Nd}} infections. How many days after the start is it detected?",
        given={"I0": {"pick": [1, 10]}, "Td": {"pick": [3, 4, 5]}, "Nd": {"pick": [1000, 10000, 100000]}}, value="Td*log(Nd/I0)/log(2)", tex="t",
        verify=f"solve(Eq(x*log(2)/{n('Td')}, log(Rational(Nd, I0))), x)[0]", explain="t = T_d log₂(N/I₀): each tenfold drop in the threshold saves about 3.3 doubling times")),
    ("BS-3.1.C", Q("bs-reads-needed", "biosec.detect", "A target makes up {{ra}} of the reads in a wastewater sample. How many reads, in millions, must be sequenced to expect {{k}} target reads?",
        cases=[{"ra": "1 in 10 million", "f": 1e-7}, {"ra": "1 in 100 million", "f": 1e-8}, {"ra": "1 in a billion", "f": 1e-9}], given={"k": {"pick": [1, 5, 10]}},
        value="k/f/1e6", tex="N", verify=f"solve(Eq(x*10**6*{n('f')}, k), x)[0]", explain="Expected target reads = depth × relative abundance; early detection needs very deep sequencing")),
    ("BS-3.1.C", Q("bs-abundance-growth", "biosec.detect", "A target's relative abundance in wastewater doubles every {{Td}} days. At {{dep}} million reads per sample, sequencing first expects one target read when abundance reaches 1/{{dep}} million. If abundance today is 1 in {{now}} million, how many days until then?",
        given={"Td": {"pick": [3, 4, 5]}, "dep": {"pick": [100, 500, 1000]}, "now": {"pick": [10000, 100000]}}, value="Td*log(now/dep)/log(2)", tex="t",
        verify=f"{n('Td')}*log(Rational(now, dep), 2)", explain="Deeper sequencing lowers the threshold, and each halving of it buys one doubling time")),
    ("BS-3.2.A", Q("bs-ppv", "biosec.detect", "A test has sensitivity {{se}}% and specificity {{sp}}%. Prevalence is {{pr}}%. What is the positive predictive value, in %?",
        given={"se": {"pick": [80, 90, 95]}, "sp": {"pick": [95, 98, 99.5]}, "pr": {"pick": [0.5, 1, 5, 20]}}, value="100*se*pr/(se*pr + (100 - sp)*(100 - pr))", tex="\\mathrm{PPV}",
        verify=f"100*{n('se')}/100*{n('pr')}/100/({n('se')}/100*{n('pr')}/100 + (1 - {n('sp')}/100)*(1 - {n('pr')}/100))",
        explain="At low prevalence even a specific test gives mostly false positives: confirm with a second test")),
    ("BS-3.2.A", Q("bs-ppv-two-tests", "biosec.detect", "Two independent tests, each with sensitivity {{se}}% and specificity {{sp}}%, are both positive. Prevalence is {{pr}}%. What is the probability of infection, in %?",
        given={"se": {"pick": [85, 90, 95]}, "sp": {"pick": [95, 98]}, "pr": {"pick": [0.5, 1, 2]}}, value="100*se^2*pr/(se^2*pr + (100 - sp)^2*(100 - pr))", tex="P",
        verify=f"100/(1 + ((1 - {n('sp')}/100)/({n('se')}/100))**2*(1 - {n('pr')}/100)/({n('pr')}/100))",
        explain="Each positive multiplies the odds by the likelihood ratio se/(1 − sp)")),
    # ── 4 withstand ──────────────────────────────────────────────────────
    ("BS-4.1.A", Q("bs-wells-riley", "biosec.withstand", "Wells–Riley: {{Ni}} infectious person(s) emit {{q}} quanta/h in a room ventilated at {{Qv}} m³/h. A susceptible person breathing {{p}} m³/h stays {{t}} h. What is their infection probability, in %?",
        given={"Ni": {"pick": [1, 2]}, "q": {"pick": [10, 25, 50]}, "Qv": {"pick": [300, 600, 1200]}, "p": {"pick": [0.5, 0.6]}, "t": {"pick": [1, 2, 4]}},
        value="100*(1 - exp(-Ni*q*p*t/Qv))", tex="P", verify=f"100*(1 - exp(-Ni*q*{n('p')}*t/Qv))",
        explain="Risk scales with the inhaled dose I·q·p·t/Q: doubling clean airflow halves the dose")),
    ("BS-4.1.A", Q("bs-each-sum", "biosec.withstand", "A room has {{v}} outdoor air changes per hour. A portable HEPA unit delivers {{cadr}} m³/h of clean air in a {{V}} m³ room. What is the equivalent total air changes per hour?",
        given={"v": {"pick": [1, 2, 3]}, "cadr": {"pick": [300, 450, 600]}, "V": {"pick": [100, 150, 200]}}, value="v + cadr/V", tex="\\mathrm{eACH}",
        verify="solve(Eq(x*V, v*V + cadr), x)[0]", explain="Clean-air rates add: CADR ÷ room volume gives the cleaner's equivalent air changes")),
    ("BS-4.1.B", Q("bs-clearance-time", "biosec.withstand", "A well-mixed room has {{ach}} equivalent air changes per hour. How many minutes until {{pc}}% of an airborne contaminant is removed (no new emission)?",
        given={"ach": {"pick": [2, 4, 6, 12]}, "pc": {"pick": [90, 99, 99.9]}}, value="60*log(1/(1 - pc/100))/ach", tex="t",
        verify=f"-60*log(1 - {n('pc')}/100)/ach", explain="Concentration decays as e^{−ACH·t}: 99% takes ln 100 ≈ 4.6 air changes")),
    ("BS-4.1.B", facts("bs-far-uvc", "biosec.withstand", [
        ("Why can far-UVC (about 222 nm) be used in occupied rooms when conventional 254 nm germicidal UV generally cannot?", "It is absorbed in the outer dead layer of skin and the tear film", "It does not kill microbes", "It is visible light", "It needs no power"),
        ("Which is a known side effect to manage with far-UVC lamps?", "Ozone generation", "Radioactivity", "Magnetic fields", "Noise"),
        ("Upper-room germicidal UV protects occupants by…", "Disinfecting air in the upper part of the room while people stay below the beam", "Shining on people directly", "Filtering water", "Heating the room"),
    ], "Germicidal light adds equivalent air changes without moving air; dose, ozone and placement are the design questions")),
    ("BS-4.2.A", facts("bs-respirator-facts", "biosec.withstand", [
        ("An N95 respirator filters at least what fraction of the test aerosol?", "95%", "50%", "99.97%", "80%"),
        ("Under OSHA, what is the assigned protection factor of a half-mask respirator (including N95s) when fit-tested?", "10", "2", "50", "1000"),
        ("Why does a fit test matter more than the filter rating?", "Air leaking around the seal bypasses the filter", "Filters fail without fit tests", "It sizes the filter", "It is a legal formality only"),
        ("Which offers a higher assigned protection factor than a half-mask?", "A full-facepiece respirator (APF 50)", "A surgical mask", "A cloth mask", "A face shield alone"),
    ], "Protection = filtration × fit: elastomerics and PAPRs are reusable stockpile options")),
    ("BS-4.2.A", Q("bs-mask-reff", "biosec.withstand", "R = {{R}}. A fraction {{c}}% of people wear masks that cut their onward transmission by {{e}}%. What is the new R (ignore protection of the wearer)?",
        given={"R": {"pick": [1.5, 2, 3]}, "c": {"pick": [40, 60, 80]}, "e": {"pick": [30, 50, 80]}}, value="R*(1 - c/100*e/100)", tex="R_{eff}",
        verify=f"{n('R')}*(1 - {n('c')}/100) + {n('R')}*{n('c')}/100*(1 - {n('e')}/100)", explain="Average over wearers and non-wearers: coverage × effect is what reduces R")),
    ("BS-4.2.B", Q("bs-isolation-reff", "biosec.withstand", "R = {{R}}. Testing and isolation prevent {{f}}% of each case's onward transmission. What is the new R, and is it below 1? (Give R.)",
        given={"R": {"pick": [1.4, 1.8, 2.5]}, "f": {"pick": [30, 45, 60]}}, value="R*(1 - f/100)", tex="R_{eff}", verify=f"solve(Eq(x/{n('R')}, 1 - {n('f')}/100), x)[0]",
        explain="Isolation removes the transmission that would have happened after it starts; presymptomatic spread limits f")),
    ("BS-4.2.B", facts("bs-npi-match", "biosec.withstand", [
        ("Which measure best addresses airborne spread in a crowded indoor space?", "More clean air (ventilation, filtration, germicidal UV) and respirators", "Hand sanitiser alone", "Disinfecting surfaces daily", "Temperature screening"),
        ("Which measure most directly limits spread by people who feel well but are infectious?", "Testing and quarantine of contacts", "Symptom screening at doors", "Isolation of symptomatic cases only", "Closing parks"),
        ("Which measure reduces importation early in an outbreak but buys only time?", "Travel testing and quarantine", "Vaccination", "Better hospital beds", "Antivirals"),
    ], "Match the measure to the route and the stage; most NPIs buy time for countermeasures")),
    # ── 5 combat ─────────────────────────────────────────────────────────
    ("BS-5.1.A", Q("bs-vaccine-coverage", "biosec.combat", "R₀ = {{R0}} and the vaccine prevents {{eff}}% of transmission. What fraction of the population must be vaccinated for herd protection, in %? (Over 100 means it cannot be reached by vaccination alone.)",
        given={"R0": {"pick": [1.5, 2, 3, 4]}, "eff": {"pick": [60, 75, 90, 95]}}, value="100*(1 - 1/R0)/(eff/100)", tex="V_c",
        verify=f"solve(Eq({n('R0')}*(1 - x/100*{n('eff')}/100), 1), x)[0]", explain="Vaccinating V with efficacy E removes V·E of susceptibles: R₀(1 − VE) < 1")),
    ("BS-5.1.A", Q("bs-efficacy-needed", "biosec.combat", "R₀ = {{R0}} and at most {{vmax}}% of people can be vaccinated. What minimum efficacy against transmission, in %, gives herd protection?",
        given={"R0": {"pick": [1.5, 2, 2.5]}, "vmax": {"pick": [70, 80, 90]}}, value="100*(1 - 1/R0)/(vmax/100)", tex="E",
        verify=f"solve(Eq({n('R0')}*(1 - {n('vmax')}/100*x/100), 1), x)[0]", explain="Coverage and efficacy trade off: their product must reach 1 − 1/R₀")),
    ("BS-5.1.B", Q("bs-ve-trial", "biosec.combat", "In a trial, {{cv}} of {{nv}} vaccinated and {{cu}} of {{nu}} placebo participants became cases. What is the vaccine efficacy, in %?",
        given={"cv": {"pick": [8, 11, 20]}, "nv": {"pick": [15000, 20000]}, "cu": {"pick": [90, 150, 185]}, "nu": {"pick": [15000, 20000]}}, value="100*(1 - (cv/nv)/(cu/nu))", tex="VE",
        verify="100*(Rational(cu, nu) - Rational(cv, nv))/Rational(cu, nu)", explain="VE = 1 − attack rate in vaccinated ÷ attack rate in unvaccinated")),
    ("BS-5.1.B", Q("bs-ve-expected-cases", "biosec.combat", "A vaccine is {{VE}}% efficacious. In a group of {{nn}} vaccinated people with an unvaccinated attack rate of {{ar}}%, how many cases are expected?",
        given={"VE": {"pick": [50, 70, 90, 95]}, "nn": {"pick": [1000, 10000]}, "ar": {"pick": [2, 5, 10]}}, value="nn*ar/100*(1 - VE/100)", tex="N",
        verify="solve(Eq(1 - (x/nn)/Rational(ar, 100), Rational(VE, 100)), x)[0]", explain="Efficacy scales the attack rate, it does not make cases impossible")),
    ("BS-5.1.C", facts("bs-mcm-facts", "biosec.combat", [
        ("What is CEPI's 100 Days Mission?", "Safe, effective vaccines ready within 100 days of a pandemic threat being identified", "Ending all pandemics in 100 days", "A 100-day lockdown plan", "A 100-dose stockpile"),
        ("Why do platform technologies (mRNA, viral vectors) speed vaccines?", "The process is reused; only the antigen sequence changes", "They need no trials", "They are cheaper to store", "They replace diagnostics"),
        ("What does an advance market commitment do?", "Guarantees purchase of a product if it succeeds, so firms invest before demand appears", "Bans exports", "Funds only basic research", "Fixes prices after a pandemic"),
    ], "Speed comes from platforms, prepared trials, money committed in advance and manufacturing ready to switch")),
    ("BS-5.1.C", facts("bs-mcm-scenario", "biosec.combat", [
        ("A new pathogen emerges and no vaccine exists. Which preparation shortens the time to first doses most?", "Prototype vaccines and trial networks prepared in advance for related virus families", "Waiting for the sequence to be published in a journal", "Building new factories after the outbreak", "Stockpiling unrelated vaccines"),
        ("Phase 3 trials stall because cases fall. Which design helps?", "Adaptive or platform trials across many sites with shared protocols", "Cancelling the trial", "Enrolling fewer people", "Ignoring the control group"),
        ("Low-income countries got vaccines late in 2021. Which fix targets that?", "Regional manufacturing and pre-agreed equitable allocation", "Higher prices", "Fewer manufacturers", "Export bans"),
    ], "Countermeasures fail at R&D, trials, financing or delivery; each has its own fix")),
    ("BS-5.2.A", Q("bs-doses-per-day", "biosec.combat", "{{P}} million people need {{d}} doses each within {{days}} days. How many million doses per day must be made and delivered?",
        given={"P": {"pick": [8000, 330, 50]}, "d": {"pick": [1, 2]}, "days": {"pick": [100, 180, 365]}}, value="P*d/days", tex="\\dot N",
        verify="solve(Eq(x*days, P*d), x)[0]", explain="Total doses ÷ days: the world needs tens of millions per day for a 100-day campaign")),
    ("BS-5.2.A", Q("bs-campaign-days", "biosec.combat", "Capacity is {{r}} million doses per day. How many days does it take to give {{d}} dose(s) to {{P}} million people?",
        given={"r": {"pick": [10, 40, 80]}, "d": {"pick": [1, 2]}, "P": {"pick": [8000, 330, 1400]}}, value="P*d/r", tex="t",
        verify="solve(Eq(r*x, P*d), x)[0]", explain="Time = doses ÷ rate: scale-up is usually the binding constraint once a vaccine works")),
    ("BS-5.2.B", facts("bs-governance-facts", "biosec.combat", [
        ("In which year did the World Health Assembly adopt the WHO Pandemic Agreement?", "2025", "2005", "2019", "2022"),
        ("Which instrument sets the rules for notifying and responding to public health emergencies?", "The International Health Regulations (2005)", "The BWC", "UNSCR 1540", "The Geneva Protocol"),
        ("Who advises the WHO Director-General before a PHEIC is declared?", "An IHR Emergency Committee of experts", "The UN Security Council", "The BWC Review Conference", "National ministers by vote"),
    ], "Health security runs through WHO instruments; weapons through the BWC and the Security Council")),
    ("BS-5.2.B", facts("bs-who-decides", "biosec.combat", [
        ("An unusual outbreak may be deliberate. Which body can the UN Secretary-General draw on to investigate alleged use of biological weapons?", "The Secretary-General's Mechanism, with its roster of experts and labs", "The WHO Emergency Committee", "The Australia Group", "CEPI"),
        ("Who decides on travel and trade measures under the IHR?", "States, which should follow WHO recommendations and justify additional measures", "The WHO, with binding orders", "The BWC ISU", "Airlines"),
        ("A vaccine needs emergency use. Who grants it in a country?", "The national regulator (WHO Emergency Use Listing helps others rely on it)", "CEPI", "The manufacturer", "The World Bank"),
    ], "Know which body can act: WHO advises, states decide, the Secretary-General investigates alleged use")),
    # ── 6 contributing ───────────────────────────────────────────────────
    ("BS-6.1.A", facts("bs-infohazard", "biosec.practice", [
        ("In a biosecurity discussion group, which is good practice?", "Discuss defences and policy, not specific ways to cause harm", "Brainstorm new attack ideas to test defences", "Share technical details freely", "Post sensitive material publicly"),
        ("You realise a public post would spread a specific route to misuse. What do you do?", "Don't publish it; raise it privately with an appropriate expert or authority", "Publish it to warn people", "Post it with a disclaimer", "Send it to a journalist"),
        ("Why can even true, defensive-minded detail be hazardous?", "It can lower the barrier for someone with harmful intent", "It is always false", "It is copyrighted", "It is boring"),
    ], "Talk about the shape of risks and defences; keep operational detail out")),
    ("BS-6.1.A", facts("bs-infohazard-scenario", "biosec.practice", [
        ("A participant starts describing how a specific pathogen could be made worse. As facilitator, you…", "Redirect to defences and remind the group of the info-hazard norms", "Let them finish for completeness", "Ask the group to improve the idea", "Record it for the notes"),
        ("A journalist asks you to explain how an AI model could help with a bioweapon, step by step. A responsible answer…", "Explains the risk at a high level and what safeguards exist, without steps", "Walks through the steps", "Refuses to discuss biosecurity at all", "Points them to technical papers"),
        ("Where should a credible concern about a specific vulnerability go?", "To people who can fix it, through a responsible-disclosure route", "A public forum", "Social media", "Nowhere"),
    ], "Facilitators protect the room: redirect, restate norms, escalate privately when needed")),
    ("BS-6.1.B", Q("bs-defence-layers", "biosec.practice", "Prevention stops {{p1}}% of threats, detection catches {{p2}}% of the rest in time, and withstand-plus-combat contains {{p3}}% of those still left. If the layers are independent, what percentage become catastrophes?",
        given={"p1": {"pick": [50, 70, 90]}, "p2": {"pick": [50, 80]}, "p3": {"pick": [60, 90]}}, value="100*(1 - p1/100)*(1 - p2/100)*(1 - p3/100)", tex="\\%",
        verify="100*Rational(100 - p1, 100)*Rational(100 - p2, 100)*Rational(100 - p3, 100)", explain="Independent layers multiply their failure rates; no single layer needs to be perfect")),
    ("BS-6.1.B", facts("bs-layer-match", "biosec.practice", [
        ("DNA synthesis screening belongs to which layer?", "Prevent", "Detect", "Withstand", "Combat"),
        ("Metagenomic wastewater sequencing belongs to which layer?", "Detect", "Prevent", "Withstand", "Combat"),
        ("Stockpiling elastomeric respirators belongs to which layer?", "Withstand", "Prevent", "Detect", "Combat"),
        ("A vaccine platform ready for any virus family belongs to which layer?", "Combat", "Prevent", "Detect", "Withstand"),
    ], "Prevent · Detect · Withstand · Combat: place an idea, then ask which layer is thinnest")),
]
