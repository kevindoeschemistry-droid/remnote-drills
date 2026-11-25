"""AI Safety framework, units 8–12 (frontier safety frameworks and safety cases, regulation and coordination,
strategy and forecasting, deeper mechanistic interpretability, agentic risk): two question types per objective.
Computations (EU AI Act compute thresholds, cluster compute, threshold drift, Brier scores, forecasts, direct logit
attribution) are recomputed along another route; framework facts follow the framework's essential knowledge, read
from the RSP, Preparedness Framework v2, FSF v3, the EU AI Act GPAI provisions, NIST AI RMF and IASR 2026. Dated
facts (policy versions, dates) need rechecking when they age."""
from opl_dsl import Q

FILE, FRAMEWORK = "ais-governance", "ai-safety"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
FW, GV, SG, IN, AG = "ais.frameworks", "ais.governance", "ais.strategy", "ais.interp", "ais.agentic"


def facts(name, skill, rows, explain, pace="quick"):
    return Q(name, skill, "{{q}}", pace=pace, cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


ADD = [
    # 8.1
    ("AIS-8.1.A", facts("ais-framework-compare", FW, [
        ("'Critical Capability Levels' with alert thresholds belong to:", "Google DeepMind's Frontier Safety Framework", "OpenAI's Preparedness Framework", "Anthropic's RSP", "The EU AI Act"),
        ("'High' and 'Critical' thresholds with a Safety Advisory Group belong to:", "OpenAI's Preparedness Framework", "Anthropic's RSP", "Google DeepMind's FSF", "NIST AI RMF"),
        ("Risk Reports reviewed with the Long-Term Benefit Trust belong to:", "Anthropic's RSP", "OpenAI's Preparedness Framework", "Google DeepMind's FSF", "The Seoul commitments"),
        ("The common 'if-then' structure of these frameworks is:", "A capability threshold, early-warning evals, the safeguards it requires, and a no-deploy condition", "Revenue targets", "Model size limits", "Publication rules only"),
    ], "Same if-then skeleton, different names and governance")),
    ("AIS-8.1.A", facts("ais-framework-compare-2", FW, [
        ("In PF v2, who makes the final call on a threshold?", "Leadership, advised by the SAG", "The SAG alone", "An external regulator", "Users"),
        ("Which framework adds a harmful-manipulation CCL in its v3?", "Google DeepMind's FSF", "OpenAI's PF", "Anthropic's RSP", "NIST RMF"),
        ("Which framework's tracked categories are Bio/Chem, Cyber and AI Self-improvement?", "OpenAI's Preparedness Framework v2", "Anthropic's RSP", "Google DeepMind's FSF", "EU AI Act"),
    ], "Learn each framework's vocabulary and decision-maker")),
    ("AIS-8.1.B", facts("ais-framework-evaluate", FW, [
        ("A common weakness of company frameworks (IASR 2026):", "They are voluntary and revisable by the company", "They are legally binding", "They have no thresholds", "They ban all deployment"),
        ("Which feature most improves a framework's credibility?", "External verification of threshold calls", "Longer documents", "More marketing", "Secret thresholds"),
        ("PF v2's SAG can:", "Advise but not block leadership", "Veto any launch", "Fire the CEO", "Set law"),
        ("Threshold specificity matters because:", "Vague thresholds let the company decide case by case", "Specific thresholds are illegal", "It doesn't", "Vague ones are stricter"),
    ], "Judge frameworks on specificity, verification, enforceability and amendment")),
    ("AIS-8.1.B", facts("ais-framework-evaluate-2", FW, [
        ("A framework can be amended by the company at any time without notice. The main concern:", "Commitments can be weakened when they bind", "It becomes too strict", "Regulators must approve", "Nothing"),
        ("Triggers across companies' frameworks:", "Vary widely", "Are identical", "Are set by law", "Don't exist"),
        ("Which would make a framework enforceable?", "Embedding its commitments in law, contracts or binding agreements", "Publishing it", "Translating it", "Shortening it"),
    ], "Voluntary commitments are only as strong as what makes them stick")),
    # 8.2
    ("AIS-8.2.A", facts("ais-rsp-trigger", FW, [
        ("Under the RSP, crossing the AI R&D-4 threshold requires:", "An affirmative case naming the most immediate misalignment risks and mitigations", "Immediate open release", "No change", "A lower price"),
        ("RSP v2 tied which standards to capability thresholds?", "ASL-3 deployment and security standards", "Pricing standards", "Hiring standards", "Marketing standards"),
        ("RSP v3 (Feb 2026) rewrote the policy around:", "Risk Reports and Frontier Safety Roadmaps", "Model sizes", "Benchmarks only", "Advertising"),
        ("Models clearly beyond Opus 4.5 get:", "Sabotage risk reports", "No evaluation", "Automatic release", "A smaller context"),
    ], "Map a result to the RSP obligation it triggers")),
    ("AIS-8.2.A", facts("ais-rsp-trigger-2", FW, [
        ("An eval shows a model could substantially automate frontier AI research. Which RSP domain is this?", "AI R&D", "CBRN", "Cyber only", "Persuasion"),
        ("An eval shows significant uplift toward a defined CBRN actor tier. Which RSP domain?", "CBRN", "AI R&D", "Autonomy only", "None"),
        ("Why do AI R&D thresholds get special treatment?", "AI-accelerated AI research could compound risks quickly", "They are easier to test", "They are unrelated to safety", "They are cheaper"),
    ], "Thresholds are organised by risk domain")),
    ("AIS-8.2.B", facts("ais-rsp-accountability", FW, [
        ("RSP v3.4 shares unredacted Risk Reports with:", "At least 200 staff", "Nobody", "The public only", "One executive"),
        ("RSP Risk Reports carry:", "Coverage dates and marked redactions", "No dates", "Only marketing", "Raw weights"),
        ("External review of a Risk Report may:", "Be split among several reviewers if all sections are covered", "Be skipped", "Be done by the model", "Be secret from the board"),
    ], "Accountability comes from documentation, review and internal visibility")),
    ("AIS-8.2.B", facts("ais-rsp-accountability-2", FW, [
        ("Why give many staff access to unredacted reports?", "More people can notice and raise problems", "For marketing", "To leak them", "It is required by the EU"),
        ("The Long-Term Benefit Trust's role in the RSP relates to:", "External review and governance oversight", "Pricing", "Hardware purchasing", "Recruiting"),
        ("A coverage date on a Risk Report tells you:", "Which period and models its evidence covers", "When it will expire legally", "Nothing", "Its author"),
    ], "Read reports for what they cover and who checked them")),
    # 8.3
    ("AIS-8.3.A", facts("ais-pf-level", FW, [
        ("Under PF v2, reaching High in a tracked category requires:", "Safeguards that sufficiently minimise risk before deployment", "Halting all work", "Nothing", "Open release"),
        ("Reaching Critical additionally requires safeguards:", "During development, not only deployment", "Only after release", "Only for open models", "None"),
        ("PF v2's scalable evals carry:", "Indicative thresholds; the final call is holistic", "Binding automatic thresholds", "No thresholds", "Legal thresholds"),
    ], "High constrains deployment; Critical constrains development too")),
    ("AIS-8.3.A", facts("ais-pf-level-2", FW, [
        ("A cyber eval approaches the High threshold but is not clearly over it. The PF process:", "Makes a holistic judgement from all evidence, documented in reports", "Ignores it", "Automatically halts training", "Releases immediately"),
        ("Which reports accompany a PF decision?", "Capabilities and Safeguards Reports", "Only a press release", "Financial statements", "None"),
        ("Why are PF thresholds 'holistic calls'?", "No single eval fully captures the risk", "They are random", "Law requires it", "To avoid evaluation"),
    ], "Judgement sits on top of the evidence")),
    ("AIS-8.3.B", facts("ais-safeguard-map", FW, [
        ("Usage monitoring answers which threat?", "A benign model with a hostile user (misuse)", "A scheming model", "Hardware failure", "Contamination"),
        ("Trust-based access tiers answer:", "Misuse by unknown users", "Model misalignment", "Data contamination", "Latency"),
        ("Control protocols and monitoring of the model's own actions answer:", "A model that may act against you (misalignment)", "Misuse only", "Price competition", "Contamination"),
        ("Robustness training answers:", "Attackers trying to bypass refusals", "Hardware theft", "Model size", "Scheming"),
    ], "Misuse safeguards assume a benign model; misalignment safeguards don't")),
    ("AIS-8.3.B", facts("ais-safeguard-map-2", FW, [
        ("Weight security answers:", "Theft that would bypass every deployment safeguard", "Sycophancy", "Prompt injection only", "Bias"),
        ("Which safeguard is useless against a scheming model that controls its own monitor?", "Untrusted self-monitoring", "Human audits", "Trusted monitoring", "Sandboxing"),
        ("A safeguard report should state:", "Which threat each safeguard addresses and how it was tested", "Only that safeguards exist", "The price", "Nothing"),
    ], "Map each safeguard to an explicit threat")),
    ("AIS-8.3.C", facts("ais-marginal-risk", FW, [
        ("PF v2's marginal-risk clause lets OpenAI relax safeguards if:", "Another developer released similar capability without them, risk doesn't meaningfully rise, it's acknowledged publicly, and OpenAI stays more protective", "Revenue falls", "Users ask", "Regulators approve"),
        ("A worry about the clause is that it:", "Can feed a race to the bottom as each lab points to the others", "Makes safeguards stricter", "Is illegal", "Has no effect"),
        ("Which condition limits the clause most?", "OpenAI must remain more protective than the other developer", "Revenue", "Size", "None"),
    ], "Relative safety clauses can weaken absolute floors")),
    ("AIS-8.3.C", facts("ais-marginal-risk-2", FW, [
        ("The best argument for a marginal-risk clause:", "Holding back gives little safety if equivalent capability is already available", "It is always safer", "It raises prices", "It ends competition"),
        ("The best argument against:", "It ties one lab's floor to the least careful competitor", "It is too strict", "It slows research", "It is unclear"),
        ("Public acknowledgement in the clause helps by:", "Letting outsiders scrutinise the relaxation", "Hiding it", "Ending the clause", "Reducing risk directly"),
    ], "Weigh counterfactual impact against race dynamics")),
    # 8.4
    ("AIS-8.4.A", facts("ais-fsf-ccl", FW, [
        ("In the FSF, alert thresholds:", "Fire on early-warning evals before a CCL is reached", "Mark a CCL reached", "Are legal limits", "Are prices"),
        ("Reaching a CCL requires:", "A safety case review before external launch", "Nothing", "Open release", "Deletion"),
        ("For advanced ML R&D CCLs, review also covers:", "Large internal deployments", "Marketing", "Only external launches", "Hardware"),
        ("FSF v3's Tracked Capability Levels (TCLs):", "Flag lesser risks sooner", "Replace CCLs", "Are legal thresholds", "Are prices"),
    ], "Alert threshold → response plan → safety case review")),
    ("AIS-8.4.A", facts("ais-fsf-ccl-2", FW, [
        ("A model approaches an ML R&D CCL but is only used internally. Under FSF v3:", "Large internal deployment can still require review", "No review is ever needed internally", "It must be open-sourced", "It is deleted"),
        ("Which CCL did FSF v3 add?", "Harmful manipulation", "Translation", "Coding speed", "Image generation"),
        ("FSF frames misalignment CCLs around:", "Instrumental reasoning that undermines human control", "Benchmark scores", "Model size", "Revenue"),
    ], "Know which capability approaches which level and what follows")),
    # 8.5
    ("AIS-8.5.A", facts("ais-safety-case-type", FW, [
        ("'The model cannot do X even with strong elicitation.' Argument type:", "Inability", "Control", "Trustworthiness", "Deference"),
        ("'Even if the model tries, the monitoring protocol prevents harm.' Argument type:", "Control", "Inability", "Trustworthiness", "None"),
        ("'The model won't try to cause harm.' Argument type:", "Trustworthiness", "Control", "Inability", "Deference"),
        ("A safety case is structured as:", "Claims, arguments and evidence", "A press release", "A model card only", "A benchmark score"),
    ], "Inability, control or trustworthiness")),
    ("AIS-8.5.A", facts("ais-safety-case-type-2", FW, [
        ("As models grow more capable, inability arguments:", "Get harder to sustain", "Get easier", "Stay the same", "Become unnecessary"),
        ("Which evidence supports a control argument?", "Red-team results against the protocol", "Benchmarks of helpfulness", "User ratings", "Pretraining loss"),
        ("Which evidence would a trustworthiness argument need?", "Evidence about the model's goals and honesty that we mostly don't have yet", "A benchmark score", "Compute logs", "A licence"),
    ], "Each argument type rests on a different kind of evidence")),
    ("AIS-8.5.B", facts("ais-safety-case-flaw", FW, [
        ("An inability case rests on one benchmark run with default prompting. Weakest premise:", "Adequate elicitation", "The threat model", "Statistics", "Model size"),
        ("A control case was red-teamed only by the developer's own monitor team with a week's effort. Weakest premise:", "Red-team strength", "Elicitation", "Data quality", "Pricing"),
        ("A trustworthiness case cites the model saying it is aligned. Weakest premise:", "Self-report as evidence of goals", "Elicitation", "Compute", "Benchmarks"),
    ], "A case is only as strong as its least-supported premise")),
    ("AIS-8.5.B", facts("ais-safety-case-flaw-2", FW, [
        ("A control case assumes the trusted monitor never colludes with the policy model, but both are copies of the same model. Weakest premise:", "Monitor independence", "Elicitation", "Audit budget", "Threat model"),
        ("An inability case was tested at a small inference budget while deployment allows long reasoning. Weakest premise:", "Test conditions match deployment", "Red-team strength", "Honesty", "Licensing"),
        ("A case argues safety from interpretability probes that were also used in training. Weakest premise:", "The probe wasn't optimised against", "Elicitation", "Statistics", "Data"),
    ], "Find the premise the conclusion most depends on")),
    # 9.1
    ("AIS-9.1.A", Q("ais-eu-gpai-class", GV, "A language model was trained with {{m}} × 10^{{ex}} FLOP. Under the EU AI Act, is it presumed a GPAI model with systemic risk?",
        cases=[{"m": 3, "ex": 25, "sr": 1}, {"m": 8, "ex": 24, "sr": 0}, {"m": 2, "ex": 26, "sr": 1}, {"m": 5, "ex": 23, "sr": 0}, {"m": 1, "ex": 24, "sr": 0}],
        choice=["Yes, systemic risk is presumed", "No: GPAI but below the presumption"], correct="sr == 1 ? 0 : 1",
        verify="0 if m*10**ex > 10**25 else 1", explain="Above 10²⁵ FLOP systemic risk is presumed (the threshold is under review); the Commission can also designate")),
    ("AIS-9.1.A", Q("ais-eu-margin", GV, "A run used {{m}} × 10^{{ex}} FLOP. By what factor is it above (or below, if < 1) the EU 10²⁵ FLOP systemic-risk presumption?",
        cases=[{"m": 3, "ex": 25}, {"m": 8, "ex": 24}, {"m": 2, "ex": 26}, {"m": 5, "ex": 24}], value="m*10^ex/1e25", tex="\\times",
        verify="Rational(m*10**ex, 10**25)", explain="Compare the run's compute with 10²⁵ FLOP")),
    ("AIS-9.1.B", facts("ais-gpai-duty", GV, [
        ("Which duty applies to all GPAI providers?", "A public summary of training content", "Adversarial testing", "Serious-incident reporting", "Commission notification of systemic risk"),
        ("Which duty applies only to systemic-risk GPAI providers?", "Evaluations including adversarial testing", "Technical documentation", "A copyright policy", "Information for downstream providers"),
        ("A systemic-risk provider never told the Commission its model crossed the threshold. Missed duty:", "Notification", "Copyright policy", "Training summary", "Downstream information"),
        ("A provider gave downstream deployers no documentation of capabilities and limits. Missed duty (all providers):", "Information for downstream providers", "Adversarial testing", "Incident reporting", "Cybersecurity"),
    ], "Separate all-provider duties from systemic-risk duties")),
    ("AIS-9.1.B", facts("ais-gpai-duty-2", GV, [
        ("Serious-incident reporting applies to:", "Systemic-risk GPAI providers", "All providers", "Only deployers", "No one"),
        ("A copyright policy is required of:", "All GPAI providers", "Only systemic-risk ones", "Only open models", "No one"),
        ("Ensuring cybersecurity of the model is required of:", "Systemic-risk GPAI providers", "Every app developer", "Only open models", "No one"),
    ], "The systemic-risk tier adds evaluation, mitigation, incident and security duties")),
    ("AIS-9.1.C", facts("ais-gpai-timeline", GV, [
        ("GPAI obligations under the EU AI Act apply from:", "2 August 2025", "1 January 2024", "2 August 2027", "They never apply"),
        ("Commission enforcement powers over GPAI start:", "2 August 2026", "2 August 2025", "2025 Q1", "2030"),
        ("Models placed on the market before 2 August 2025 must comply by:", "2 August 2027", "Immediately", "Never", "2026 Q1"),
        ("The GPAI Code of Practice is:", "A voluntary route to show compliance (Transparency, Copyright, Safety & Security)", "Binding law", "A ban", "A tax"),
    ], "Dated facts: recheck when they age")),
    ("AIS-9.1.C", facts("ais-gpai-open-source", GV, [
        ("Free, open-source GPAI models skip some documentation duties unless:", "They carry systemic risk", "They are small", "They are popular", "They are multilingual"),
        ("Signing the Code of Practice:", "Is voluntary but helps demonstrate compliance", "Is mandatory", "Exempts from the Act", "Is a criminal matter"),
        ("The Code's three chapters are:", "Transparency, Copyright, Safety & Security", "Price, Speed, Size", "Training, Testing, Shipping", "None of these"),
    ], "Open-source relief stops at systemic risk")),
    # 9.2
    ("AIS-9.2.A", facts("ais-rmf-functions", GV, [
        ("Setting roles, policies and a risk culture across the organisation:", "Govern", "Map", "Measure", "Manage"),
        ("Describing a use's context and the risks it may raise:", "Map", "Govern", "Measure", "Manage"),
        ("Running evaluations and tracking risk metrics:", "Measure", "Map", "Manage", "Govern"),
        ("Prioritising risks, acting on them and monitoring over time:", "Manage", "Measure", "Govern", "Map"),
    ], "Govern cuts across Map, Measure and Manage")),
    ("AIS-9.2.A", facts("ais-rmf-functions-2", GV, [
        ("Writing an incident-response plan for a deployed model:", "Manage", "Map", "Measure", "Govern"),
        ("Training staff on AI risk policy:", "Govern", "Measure", "Map", "Manage"),
        ("Red-teaming a model before release:", "Measure", "Govern", "Map", "Manage"),
    ], "Sort activities by what they do in the risk cycle")),
    ("AIS-9.2.B", facts("ais-gai-profile", GV, [
        ("NIST AI 600-1 (Generative AI Profile) lists how many GAI risks?", "12", "4", "100", "3"),
        ("'CBRN information or capabilities' in AI 600-1 is mapped to actions under:", "The four RMF functions", "Copyright law", "A tax code", "The EU Act only"),
        ("How do NIST standards typically bind?", "Through procurement, contracts and voluntary adoption", "Criminal law", "They always bind directly", "Never"),
        ("In the EU, harmonised standards give:", "A presumption of conformity", "An exemption from law", "A fine", "Nothing"),
    ], "Standards bind indirectly unless law adopts them")),
    ("AIS-9.2.B", facts("ais-gai-profile-2", GV, [
        ("Confabulation in AI 600-1 maps most directly to which control?", "Measuring and disclosing reliability and grounding", "Weight security", "Export control", "Copyright review"),
        ("Information integrity risk concerns:", "Generated content undermining trust in information", "Hardware", "Latency", "Pricing"),
        ("Why map a risk to all four functions?", "Each function contributes different actions to managing it", "To fill a template", "Only Measure matters", "Only Govern matters"),
    ], "Each risk gets actions across the whole cycle")),
    # 9.3
    ("AIS-9.3.A", facts("ais-compute-lever", GV, [
        ("Which property makes compute governable?", "Detectable, excludable and quantifiable, with a concentrated supply chain", "It is free", "It is invisible", "It is unlimited"),
        ("Where is the supply chain most concentrated?", "Fabrication, lithography and leading chips", "Electricity", "Software", "Data"),
        ("Frontier runs are visible to:", "The cloud providers that host the clusters", "Nobody", "Only users", "Only the press"),
    ], "Chokepoints make compute a lever")),
    ("AIS-9.3.A", facts("ais-compute-lever-2", GV, [
        ("Which policy uses compute as a lever?", "Reporting requirements for very large training runs", "Copyright filters", "Content labels", "Age verification"),
        ("Why is data a weaker lever than compute?", "It is copyable and hard to exclude", "It is rare", "It is expensive", "It is regulated"),
        ("Export controls on advanced chips act at:", "The hardware supply chain", "Model outputs", "User prompts", "Inference prices"),
    ], "Physical goods are easier to govern than information")),
    ("AIS-9.3.B", Q("ais-cluster-compute", GV, "{{n}} chips at {{f}} × 10¹⁵ FLOP/s, {{mfu}}% utilisation, for {{d}} days. Estimate the training compute (FLOP).",
        given={"n": {"pick": [10000, 25000, 100000]}, "f": {"pick": [1, 2]}, "mfu": {"pick": [30, 40]}, "d": {"pick": [60, 90]}},
        value="n*f*1e15*mfu/100*d*86400", tex="C", verify="n*f*10**15*Rational(mfu, 100)*d*24*3600",
        explain="C = chips × FLOP/s × utilisation × seconds; 10⁴ × 10¹⁵ × 0.4 × 90 days ≈ 3 × 10²⁵")),
    ("AIS-9.3.B", Q("ais-days-to-threshold", GV, "A cluster of {{n}} chips at {{f}} × 10¹⁵ FLOP/s and {{mfu}}% utilisation trains continuously. After how many days does it pass 10²⁵ FLOP?",
        given={"n": {"pick": [5000, 10000, 20000]}, "f": {"pick": [1, 2]}, "mfu": {"pick": [30, 40]}}, value="1e25/(n*f*1e15*mfu/100)/86400", tex="t",
        verify="solve(Eq(n*f*10**15*Rational(mfu, 100)*Symbol('tt')*86400, 10**25), Symbol('tt'))[0]", explain="Invert C = rate × time")),
    ("AIS-9.3.C", Q("ais-threshold-drift", GV, "Algorithmic efficiency improves {{g}}× per year. A capability first needing 10²⁵ FLOP will need how much compute (×10²⁵) after {{y}} years?",
        given={"g": {"pick": [2, 3, 6]}, "y": {"pick": [1, 2, 3]}}, value="1/g^y", tex="C", verify="Rational(1, g**y)",
        explain="A fixed FLOP line falls behind: the same capability arrives below it")),
    ("AIS-9.3.C", facts("ais-threshold-weakness", GV, [
        ("Why do fixed compute thresholds age badly?", "Algorithmic efficiency lets the same capability be reached with less compute", "Compute gets more expensive", "Chips get slower", "Laws change"),
        ("Which gain does a pretraining-FLOP threshold miss?", "Post-training and inference-time compute", "Model size", "Training tokens", "Chip count"),
        ("A remedy for threshold drift:", "Combine compute with capability-based triggers and update thresholds", "Raise the threshold every year", "Remove thresholds", "Count parameters instead"),
    ], "Compute is a proxy for capability, and the proxy drifts")),
    # 9.4
    ("AIS-9.4.A", facts("ais-coordination-problem", GV, [
        ("Two labs each cut safety testing to ship first. Coordination problem:", "Race to the bottom", "Verification gap", "Free-riding", "Collective action success"),
        ("Two countries would pause together but can't check each other's compliance. Problem:", "Verification gap", "Race to the bottom", "Free-riding", "None"),
        ("One lab benefits from others' safety research without contributing. Problem:", "Free-riding", "Verification gap", "Race to the bottom", "Monopoly"),
    ], "Without verification, mutual restraint is unstable")),
    ("AIS-9.4.A", facts("ais-coordination-2", GV, [
        ("Which mechanism addresses a verification gap?", "Compute monitoring or third-party audits", "Press releases", "Higher prices", "More benchmarks"),
        ("Why is mutual restraint unstable without verification?", "Each side fears the other defects", "Both want to restrain", "It is illegal", "Restraint is free"),
        ("A shared safety standard backed by procurement rules mainly counters:", "A race to the bottom", "Free-riding on research", "Verification", "Nothing"),
    ], "Name the problem before choosing the fix")),
    ("AIS-9.4.B", facts("ais-summit-track", GV, [
        ("At the Seoul summit (2024), companies committed to:", "Publish safety frameworks", "Stop all training", "Open-source models", "Pay a levy"),
        ("The first AI safety summit was held at:", "Bletchley Park, 2023", "Paris, 2025", "Seoul, 2024", "Geneva, 2022"),
        ("AI Safety Institutes test models pre-deployment under:", "Voluntary agreements, without power to block release", "Binding law with veto power", "No agreements", "Court orders"),
        ("Which institute publishes more of its findings?", "UK AISI (more than CAISI)", "Neither publishes", "Both equally", "CAISI more"),
    ], "Dated facts: recheck when they age")),
    ("AIS-9.4.B", facts("ais-summit-track-2", GV, [
        ("Which came after Seoul?", "Paris, 2025", "Bletchley, 2023", "Both before", "None"),
        ("India hosted a summit in the series in:", "2026", "2023", "2024", "2025"),
        ("A limit of the institute model is that institutes:", "Can't block release and publish findings unevenly", "Have veto power", "Train the models", "Set prices"),
    ], "Bletchley 2023 → Seoul 2024 → Paris 2025 → India 2026")),
    ("AIS-9.4.C", facts("ais-evidence-dilemma", GV, [
        ("The evidence dilemma (IASR 2026) is:", "Evidence about risk arrives slower than capability, so acting early risks bad policy and waiting risks exposure", "There is too much evidence", "Evidence is always clear", "Policy is always fast"),
        ("If-then commitments respond by:", "Committing now to act later when evidence crosses a threshold", "Acting on no evidence", "Waiting indefinitely", "Banning research"),
        ("Transparency requirements help by:", "Producing the evidence decision-makers need", "Hiding results", "Slowing release only", "Replacing evaluation"),
    ], "Pre-commit to evidence-triggered action")),
    ("AIS-9.4.C", facts("ais-evidence-dilemma-2", GV, [
        ("A regulator waits for proof of harm before acting. The risk:", "Exposure to harms that arrive before proof", "Bad policy from acting early", "None", "Too much evidence"),
        ("A regulator acts on speculation alone. The risk:", "Poorly targeted policy", "Exposure", "Nothing", "Too slow"),
        ("Which tool combines early commitment with later evidence?", "If-then commitments", "Immediate bans", "Waiting", "Self-certification"),
    ], "Both acting early and waiting carry costs")),
    # 9.5
    ("AIS-9.5.A", facts("ais-who-can-act", GV, [
        ("Who controls the chip chokepoint?", "A handful of chip designers, fabs and lithography suppliers, plus export-control authorities", "Users", "App stores", "Universities"),
        ("Who can most directly see a frontier training run?", "The compute provider hosting it", "Users", "Journalists", "Standards bodies"),
        ("Which actor can block market access in a jurisdiction?", "Governments and regulators", "Benchmark authors", "Individual researchers", "Users"),
    ], "Leverage sits at chokepoints: chips, cloud, capital, talent, market access")),
    ("AIS-9.5.A", facts("ais-who-can-act-2", GV, [
        ("A policy window opens when:", "One of the chokepoints shifts (a shortage, a crisis, a new law)", "Nothing changes", "Models get smaller", "Prices fall only"),
        ("Talent is a lever because:", "Frontier work depends on a small pool of researchers", "It is unlimited", "It is regulated", "It doesn't matter"),
        ("Investors act on frontier labs through:", "Capital and governance rights", "Benchmarks", "Chips", "Publications"),
    ], "Map who can act before choosing whom to persuade")),
    ("AIS-9.5.B", facts("ais-open-weights", GV, [
        ("Open models trail the closed frontier by about:", "Under a year (IASR) / 4–8 months (AISI)", "Five years", "They lead", "Ten years"),
        ("The strongest argument for open weights:", "Benefits to research, access and scrutiny", "Safeguards are stronger", "They can be recalled", "They are always safer"),
        ("The strongest argument against open weights at the frontier:", "Safeguards are removable and release is irreversible", "They are slower", "They are less accurate", "They cost more"),
        ("Marginal risk asks:", "How much a release adds beyond what is already available", "Total risk of AI", "Only benefits", "Price"),
    ], "Weigh marginal risk, irreversibility and the frontier gap")),
    ("AIS-9.5.B", facts("ais-open-weights-2", GV, [
        ("If open models trail the frontier by months, releasing a model at today's open level:", "Adds less marginal risk than releasing at the frontier", "Adds more", "Is irreversible only for closed models", "Is never safe"),
        ("Why does irreversibility weigh heavily?", "A release can't be undone if a hazard is found later", "It can always be recalled", "Laws require it", "It doesn't"),
        ("A staged approach to open release would:", "Release once evaluations show no dangerous capability at that level", "Never release", "Release everything immediately", "Release only weights without code"),
    ], "Argue both sides with the same criteria")),
    # 10.1
    ("AIS-10.1.A", Q("ais-benchmark-trend", SG, "A benchmark score (logit scale) rises linearly: logit {{l0}} now, +{{s}} per year. When does it reach 90% (logit ≈ 2.197)? Give years from now.",
        given={"l0": {"pick": [-2, -1, 0]}, "s": {"pick": [0.5, 1, 1.5]}}, value="(log(9) - l0)/s", tex="t", verify="(log(9) - l0)/nsimplify(s)",
        explain="Extrapolating on the logit scale avoids pretending a percentage can grow forever; logit(0.9) = ln 9")),
    ("AIS-10.1.A", facts("ais-timeline-bottlenecks", SG, [
        ("Which is not one of IASR 2026's named bottlenecks to scaling?", "Lack of interest", "Data", "Chips", "Energy"),
        ("'Jagged' capability means:", "Strong on some hard tasks, weak on some easy ones", "Uniformly improving", "Random", "Declining"),
        ("Why does one trend line rarely mean 'AGI'?", "Capability is jagged and benchmarks are narrow", "Trends never continue", "Compute stops", "Benchmarks are perfect"),
    ], "Forecasts should show their bottlenecks")),
    ("AIS-10.1.B", Q("ais-brier", SG, "You forecast {{p1}}, {{p2}} and {{p3}} for three events; outcomes were yes, no, yes. What is your Brier score?",
        given={"p1": {"pick": [0.7, 0.9]}, "p2": {"pick": [0.2, 0.4]}, "p3": {"pick": [0.6, 0.8]}},
        value="((p1 - 1)^2 + p2^2 + (p3 - 1)^2)/3", tex="B", verify="((nsimplify(p1) - 1)**2 + nsimplify(p2)**2 + (nsimplify(p3) - 1)**2)/3",
        explain="Mean squared error of probabilities; 0 is perfect, 0.25 is always saying 50%")),
    ("AIS-10.1.B", Q("ais-brier-constant", SG, "Always forecasting {{p}} on events that happen {{f}}% of the time gives what expected Brier score?",
        given={"p": {"pick": [0.5, 0.3, 0.7]}, "f": {"pick": [20, 50, 70]}}, value="(f/100)*(1 - p)^2 + (1 - f/100)*p^2", tex="B",
        verify="Rational(f, 100)*(1 - nsimplify(p))**2 + (1 - Rational(f, 100))*nsimplify(p)**2", explain="The best constant forecast is the base rate")),
    # 10.2
    ("AIS-10.2.A", facts("ais-takeoff", SG, [
        ("The AI-R&D feedback loop means:", "AI multiplies research output, so progress compounds", "AI stops research", "Research gets slower", "Hardware improves alone"),
        ("A key limit on a software intelligence explosion is:", "Compute for experiments", "Lack of ideas", "Too few benchmarks", "Too many researchers"),
        ("Why do frameworks give AI R&D thresholds special weight?", "Crossing them could speed every other risk", "They are easy to measure", "They concern marketing", "They are legal requirements"),
        ("PF v2's Critical AI self-improvement level involves:", "Generational gains in a fifth of the 2024 time", "Any coding ability", "Writing emails", "Answering trivia"),
    ], "Compounding progress could shrink the time to react")),
    ("AIS-10.2.A", Q("ais-rd-multiplier", SG, "If AI raises research speed {{m}}× and a model generation took {{T}} months, how long would the next generation take, other things equal?",
        given={"m": {"pick": [2, 3, 5]}, "T": {"pick": [12, 18]}}, value="T/m", tex="t", verify="Rational(T, m)",
        explain="A 5× speed-up turns 18 months into about 3.6; experiments limited by compute cap the multiplier")),
    # 10.3
    ("AIS-10.3.A", facts("ais-risk-taxonomy", SG, [
        ("A group uses a model to plan a cyberattack. IASR category:", "Malicious use", "Malfunction", "Systemic risk", "None"),
        ("A model pursues an unintended goal and resists correction. IASR category:", "Malfunction (loss of control)", "Malicious use", "Systemic", "None"),
        ("Automation displaces large parts of the labour market. IASR category:", "Systemic risk", "Malicious use", "Malfunction", "None"),
        ("A model gives a confidently wrong medical dose. IASR category:", "Malfunction (reliability)", "Malicious use", "Systemic", "None"),
    ], "Misuse, malfunction, systemic")),
    ("AIS-10.3.A", facts("ais-risk-taxonomy-2", SG, [
        ("An influence operation floods social media with generated content. Category and lever?", "Malicious use; provenance and platform policy", "Malfunction; retraining", "Systemic; labour policy", "None"),
        ("Many firms delegate decisions to AI and humans lose oversight capacity. Category?", "Systemic (autonomy)", "Misuse", "Malfunction only", "None"),
        ("Which lever fits malfunction risk?", "Alignment, testing and control", "Export controls only", "Copyright law", "Advertising"),
    ], "Name the category, then the lever that fits it")),
    ("AIS-10.3.B", facts("ais-threat-model-compare", SG, [
        ("Misuse risk is driven mainly by:", "Access and uplift", "Misalignment", "Labour markets", "Model honesty"),
        ("Loss-of-control risk is driven mainly by:", "Misalignment plus autonomy", "Access", "Prices", "Copyright"),
        ("Power-concentration risk arises when:", "AI replaces the cooperation that checks power", "Models are small", "Benchmarks saturate", "Open models lead"),
        ("The main levers for misuse are:", "Safeguards and security", "Alignment research only", "Distribution of benefits", "None"),
    ], "Different drivers, different levers")),
    ("AIS-10.3.B", facts("ais-threat-model-compare-2", SG, [
        ("Which lever addresses power concentration?", "Governance and wide distribution of benefits", "Classifiers", "Weight security alone", "RLHF"),
        ("Which lever addresses loss of control?", "Alignment and control", "Export controls only", "Content labels", "Pricing"),
        ("An intervention that strongly cuts misuse but speeds autonomy could:", "Raise loss-of-control risk", "Lower every risk", "Have no trade-off", "End power concentration"),
    ], "Interventions trade off across threat models")),
    ("AIS-10.3.C", facts("ais-transition-strategy", SG, [
        ("A coordinated pause bets most on:", "Verification and enforcement", "A safe lead", "Defence outpacing offence", "Nothing"),
        ("Safe-lead racing bets on:", "A responsible actor staying ahead and using the lead well", "Verification", "A global pause", "Open release"),
        ("Defensive acceleration bets on:", "Defence technologies outpacing offence", "Pausing", "Racing", "Doing nothing"),
        ("Gradual institutional adaptation bets on:", "Institutions keeping pace with capability", "A lead", "Verification", "A pause"),
    ], "Every strategy bets on something")),
    ("AIS-10.3.C", facts("ais-transition-strategy-2", SG, [
        ("Which observation would most weaken the case for safe-lead racing?", "The lead is thin and safety work is cut to keep it", "Verification improves", "Defence is cheap", "Institutions adapt"),
        ("Which observation would most strengthen the case for a coordinated pause?", "Reliable compute verification becomes available", "Labs disagree", "Chips get cheaper", "Open models lead"),
        ("A crux in strategy debates is:", "A belief whose change would flip the preferred strategy", "A fact everyone agrees on", "A benchmark", "A press release"),
    ], "Find the crux behind each strategy")),
    ("AIS-10.3.D", Q("ais-itn-score", SG, "Score an intervention on importance {{imp}}, tractability {{tr}} and neglectedness {{ng}} (each 1–10), multiplying them. A second scores {{i2}}, {{t2}}, {{n2}}. What is the ratio of the first to the second?",
        given={"imp": {"pick": [8, 9]}, "tr": {"pick": [3, 5]}, "ng": {"pick": [6, 8]}, "i2": {"pick": [9, 10]}, "t2": {"pick": [6, 7]}, "n2": {"pick": [2, 3]}},
        value="(imp*tr*ng)/(i2*t2*n2)", tex="ratio", verify="Rational(imp*tr*ng, i2*t2*n2)",
        explain="The factors multiply, so a very neglected but moderately important area can beat a crowded important one")),
    ("AIS-10.3.D", facts("ais-theory-of-change", SG, [
        ("A theory of change links:", "Action → intermediate outcome → risk reduction", "Effort → salary", "Topic → paper", "Model → benchmark"),
        ("Comparative advantage asks:", "Where your skills make the most difference relative to others", "What is most famous", "What pays most", "What is easiest"),
        ("Which is the weakest theory of change?", "Writing about a topic with no path to anyone acting on it", "Building an eval a lab adopts", "Training red-teamers", "Advising a regulator"),
    ], "Prioritise by impact, tractability, neglect and your fit")),
    # 11.1
    ("AIS-11.1.A", facts("ais-qk-ov", IN, [
        ("The QK circuit (W_Qᵀ W_K) decides:", "Where a head attends", "What it writes", "The vocabulary", "The layer count"),
        ("The OV circuit (W_V W_O) decides:", "What information gets moved", "Where to attend", "The learning rate", "The tokenizer"),
        ("A copying head's OV circuit tends to map a token to:", "Raising that same token's logit", "A random token", "The previous position", "Nothing"),
    ], "QK chooses the source; OV chooses the message")),
    ("AIS-11.1.A", facts("ais-qk-ov-2", IN, [
        ("Two heads attend to the same positions but write different things. They differ in their:", "OV circuits", "QK circuits", "Embeddings", "LayerNorms"),
        ("A previous-token head's QK circuit attends:", "From each position to the one before it", "To the first token", "To itself", "Randomly"),
        ("Why analyse QK and OV separately?", "Attention pattern and moved content are independent decisions", "They are the same", "Only OV matters", "Only QK matters"),
    ], "Separate where from what")),
    ("AIS-11.1.B", Q("ais-dla", IN, "A head's output (after the final LayerNorm scale) is h = ({{h1}}, {{h2}}). The unembedding columns are u_correct = ({{c1}}, {{c2}}) and u_wrong = ({{w1}}, {{w2}}). Compute its direct logit attribution.",
        given={"h1": {"pick": [1, 2, -1]}, "h2": {"pick": [0.5, 1, 2]}, "c1": {"pick": [1, 2]}, "c2": {"pick": [0, 1]}, "w1": {"pick": [0, -1]}, "w2": {"pick": [1, 2]}},
        value="h1*(c1 - w1) + h2*(c2 - w2)", tex="DLA",
        verify="(Matrix([[h1, nsimplify(h2)]])*(Matrix([c1, c2]) - Matrix([w1, w2])))[0]", explain="DLA = h · (u_correct − u_wrong)")),
    ("AIS-11.1.B", facts("ais-dla-limits", IN, [
        ("Direct logit attribution ignores:", "Effects that pass through later layers", "The unembedding", "The final LayerNorm", "The correct token"),
        ("A head with large positive DLA for the correct token:", "Directly pushes the model toward the correct answer", "Is irrelevant", "Hurts the answer", "Moves no information"),
        ("Why use a correct-minus-wrong logit difference?", "It cancels shifts that raise all logits together", "It is easier to type", "It ignores the answer", "It is required by PyTorch"),
    ], "DLA measures the direct path only")),
    # 12.1
    ("AIS-12.1.A", facts("ais-agent-injection", AG, [
        ("An email assistant reads incoming mail containing hidden instructions. The injection pathway is:", "Untrusted data in the context acting as instructions", "The user's prompt", "The weights", "The tokenizer"),
        ("Which control limits damage from a hijacked agent?", "Least-privilege tools, permissions and egress limits", "A longer system prompt", "Higher temperature", "More tools"),
        ("A browsing agent can send email and read the web. The most dangerous combination is:", "Reading untrusted pages and sending data out", "Reading only", "Writing drafts only", "Searching only"),
        ("Requiring user confirmation before irreversible actions:", "Breaks the chain at the step that causes harm", "Has no effect", "Increases risk", "Replaces monitoring"),
    ], "Untrusted data is an instruction channel; limit what a hijacked agent can do")),
    ("AIS-12.1.A", facts("ais-agent-injection-2", AG, [
        ("Why can't a system prompt alone stop prompt injection?", "The model can't reliably tell instructions in data from instructions from the user", "System prompts are ignored", "Injection only uses images", "It can"),
        ("A coding agent installs packages named in a README it fetched. The injection risk is:", "A malicious README directing it to install attacker code", "None", "Slow builds", "Sycophancy"),
        ("Which design separates trusted from untrusted content?", "Quarantining untrusted data in a tool with no side-effect permissions", "Merging all inputs", "Removing logs", "Raising temperature"),
    ], "Design so that a hijack has little to work with")),
    ("AIS-12.1.B", facts("ais-distributed-attack", AG, [
        ("Why can per-instance monitors miss distributed attacks?", "Each instance's actions look benign; the harm lies in the combination", "Monitors are off", "Instances can't act", "Attacks are always obvious"),
        ("What monitoring design catches distributed attacks?", "Aggregating actions across instances", "Per-message filters only", "Higher temperature", "Shorter contexts"),
        ("Many agent instances each copy a small piece of a sensitive dataset. A per-instance monitor sees:", "Small, harmless-looking reads", "The full exfiltration", "Nothing at all", "An alert every time"),
    ], "Monitor the fleet, not just each instance")),
    ("AIS-12.1.B", Q("ais-split-threshold", AG, "A monitor flags any instance that reads more than {{t}} records. An attacker splits a {{Nr}}-record exfiltration across instances, each just under the limit. How many instances does it need?",
        given={"t": {"pick": [50, 100, 200]}, "Nr": {"pick": [10000, 50000]}}, value="ceil(Nr/(t - 1))", tex="n", final=True,
        verify="ceiling(Rational(Nr, t - 1))", explain="Per-instance limits are easy to stay under; aggregate counts across instances")),
]
