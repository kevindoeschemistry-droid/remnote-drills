"""AI Safety framework, units 5–7 (evaluation science, dangerous-capability evaluation methodology, control and
security): two question types per objective. Statistics (pass@k, confidence intervals, Cohen's kappa, sample size,
relative risk, horizons, catch probability, layered residual risk) are recomputed along another route (explicit
sums, solve on the defining equation); concepts are authored scenarios. Methodology only: no item describes how to
cause harm, and dangerous-capability items name domains and study designs, never content."""
from opl_dsl import Q

FILE, FRAMEWORK = "ais-evals", "ai-safety"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
EV, DC, CT = "ais.evals", "ais.dangerous-caps", "ais.control"


def facts(name, skill, rows, explain, pace="quick"):
    return Q(name, skill, "{{q}}", pace=pace, cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


ADD = [
    # 5.1
    ("AIS-5.1.A", facts("ais-eval-classify", EV, [
        ("A benchmark asks whether the model, under best elicitation, can complete a multi-step software task. This measures:", "Capability, with an agentic task", "Propensity, with a static benchmark", "Propensity, with a red-team", "An uplift study"),
        ("Researchers place the model in a realistic deployment and record how often it takes a harmful shortcut unprompted. This measures:", "Propensity", "Capability", "Contamination", "Uplift"),
        ("Experts try for a week to get the model to produce disallowed help. This is:", "A red-team exercise", "A static benchmark", "An uplift study", "A propensity survey"),
        ("Two groups of participants attempt a task with and without model access. This is:", "A human uplift study", "A static benchmark", "An agentic task", "A red-team exercise"),
    ], "Capability asks 'can it'; propensity asks 'will it'")),
    ("AIS-5.1.A", facts("ais-capability-propensity", EV, [
        ("Which claim needs a capability eval?", "The model cannot do X even when we try hard", "The model rarely does X in normal use", "Users like the model", "The model is fast"),
        ("Which claim needs a propensity eval?", "The model would not choose to do X in realistic conditions", "The model is unable to do X", "The model scores 90% on a benchmark", "The model has N parameters"),
        ("Why can't one setup support both claims?", "Capability needs maximal elicitation; propensity needs realistic, unpressured conditions", "They are the same", "Propensity needs no data", "Capability needs no prompts"),
    ], "Different claims need different setups")),
    ("AIS-5.1.B", facts("ais-threat-model", DC, [
        ("A threat model links a capability to harm by naming:", "Actor, resources, steps and the bottleneck the model might remove", "Only the topic", "Only the model size", "Only the benchmark"),
        ("An eval should target:", "The bottleneck in the threat model, not just the topic", "Whatever is easiest to measure", "Trivia about the domain", "Model speed"),
        ("A trivia benchmark about a hazardous domain mainly measures:", "Recognition of facts, which may not be the bottleneck", "End-to-end capability", "Propensity", "Uplift"),
    ], "Evaluate the step the model could actually change")),
    ("AIS-5.1.B", facts("ais-threat-model-2", DC, [
        ("Which actor tier matters for a 'novice uplift' threshold?", "People without relevant expertise or resources", "State programmes", "Expert teams", "The developers"),
        ("If the bottleneck for an actor is hands-on execution, a text Q&A eval:", "May miss the capability that matters", "Measures it perfectly", "Is required", "Overstates nothing"),
        ("Which is a good threat-model output?", "A list of steps with where the model could help most", "A single accuracy number", "A model card", "A press release"),
    ], "A threat model tells you what to measure")),
    # 5.2
    ("AIS-5.2.A", facts("ais-validity-flaw", EV, [
        ("The test questions appear verbatim in the model's training data. Flaw:", "Contamination", "Saturation", "Leaky grader", "Construct mismatch"),
        ("All frontier models score 98–99%. Flaw:", "Saturation", "Contamination", "Shortcut", "Leaky grader"),
        ("The answer can be guessed from option length alone. Flaw:", "Answerable shortcut", "Saturation", "Contamination", "Unrealistic environment"),
        ("The grader passes any answer containing the word 'correct'. Flaw:", "Leaky grader", "Saturation", "Contamination", "Construct mismatch"),
        ("A cyber eval runs in a toy environment with none of the defences of real systems. Flaw:", "Unrealistic environment", "Saturation", "Leaky grader", "Shortcut"),
        ("The score tracks general knowledge, not the threat-model capability. Flaw:", "Construct mismatch", "Contamination", "Saturation", "Leaky grader"),
    ], "Ask whether the score tracks the capability that matters")),
    ("AIS-5.2.A", facts("ais-validity-flaw-2", EV, [
        ("Pre-deployment results fail to predict real-world performance. IASR 2026 attributes much of this to:", "Benchmarks being outdated, narrow or contaminated", "Too many evaluators", "Using humans", "Statistics"),
        ("An eval measures typing speed as a proxy for coding skill. Flaw:", "Construct mismatch", "Saturation", "Contamination", "Leaky grader"),
        ("Which fix targets saturation?", "Harder items with headroom above current scores", "More of the same items", "A leakier grader", "Publishing answers"),
    ], "Validity is about the inference, not the number")),
    ("AIS-5.2.B", facts("ais-contamination", EV, [
        ("A canary string in a dataset lets you:", "Detect whether the dataset leaked into training", "Encrypt the data", "Speed up grading", "Remove bias"),
        ("Scores drop sharply on rephrased versions of the same items. This signals:", "Contamination (memorisation)", "Saturation", "Better reasoning", "A leaky grader"),
        ("A release-date split compares performance on items:", "Published before and after the training cutoff", "Of different lengths", "Graded by different people", "In different languages"),
        ("Which keeps a benchmark uncontaminated longest?", "A private held-out set", "Posting it on GitHub", "Including answers", "Translating it"),
    ], "Contamination inflates scores through memorisation")),
    ("AIS-5.2.B", Q("ais-contam-gap", EV, "A model scores {{o}}% on original items and {{r}}% on rephrased equivalents. What is the contamination gap in percentage points?",
        given={"o": {"pick": [82, 90, 95]}, "r": {"pick": [60, 70, 78]}}, value="o - r", tex="\\Delta", verify="o - r",
        explain="A gap between original and rephrased items is the signature of memorisation")),
    ("AIS-5.2.C", facts("ais-mcq-limits", EV, [
        ("Why do MCQ knowledge benchmarks misjudge real-world capability?", "Recognising an answer is not producing or executing it", "They are too hard", "They use numbers", "They are always contaminated"),
        ("Which is usually the real bottleneck MCQs miss?", "Tacit knowledge and multi-step execution", "Vocabulary", "Spelling", "Response length"),
        ("Near-ceiling MCQ scores also:", "Compress differences between models", "Reveal small differences", "Prove capability", "Measure propensity"),
    ], "Open-ended and agentic tasks test production and execution")),
    ("AIS-5.2.C", Q("ais-mcq-chance", EV, "An MCQ benchmark has {{k}} options per item and a model scores {{s}}%. What is its chance-corrected score (%)?",
        given={"k": {"pick": [4, 5]}, "s": {"pick": [40, 60, 85]}}, value="100*(s/100 - 1/k)/(1 - 1/k)", tex="\\%",
        verify="100*(Rational(s, 100) - Rational(1, k))/(1 - Rational(1, k))", explain="(score − chance)/(1 − chance): guessing alone scores 1/k")),
    # 5.3
    ("AIS-5.3.A", Q("ais-pass-at-k", EV, "n = {{n}} samples per problem, c = {{c}} correct. Compute the unbiased pass@{{k}}.",
        cases=[{"n": 10, "c": 2, "k": 1}, {"n": 10, "c": 2, "k": 5}, {"n": 20, "c": 3, "k": 5}, {"n": 20, "c": 1, "k": 10}, {"n": 100, "c": 10, "k": 10}],
        value="1 - combinations(n - c, k)/combinations(n, k)", tex="pass@k",
        verify="1 - binomial(n - c, k)/binomial(n, k)",
        explain="1 − C(n − c, k)/C(n, k): the chance a random k-subset contains at least one correct sample")),
    ("AIS-5.3.A", Q("ais-pass-at-k-naive", EV, "With n = {{n}}, c = {{c}}, by how much does the naive 1 − (1 − c/n)^k overstate (+) or understate (−) the unbiased pass@{{k}}? (Naive minus unbiased.)",
        cases=[{"n": 10, "c": 2, "k": 5}, {"n": 20, "c": 3, "k": 5}, {"n": 10, "c": 1, "k": 5}],
        value="(1 - (1 - c/n)^k) - (1 - combinations(n - c, k)/combinations(n, k))", tex="\\Delta",
        verify="(1 - (1 - Rational(c, n))**k) - (1 - binomial(n - c, k)/binomial(n, k))", explain="Sampling without replacement from n differs from independent draws when n is small")),
    ("AIS-5.3.B", Q("ais-score-ci", EV, "A model solves {{c}} of {{n}} independent items. Give the half-width of the 95% normal-approximation CI, in percentage points.",
        cases=[{"c": 60, "n": 200}, {"c": 120, "n": 400}, {"c": 300, "n": 1000}, {"c": 150, "n": 200}, {"c": 720, "n": 1000}], value="100*1.96*sqrt((c/n)*(1 - c/n)/n)", tex="\\pm",
        verify="100*Rational(196, 100)*sqrt(Rational(c, n)*(1 - Rational(c, n))/n)", explain="SE = √(p(1 − p)/n); half-width 1.96·SE")),
    ("AIS-5.3.B", Q("ais-two-model-z", EV, "Model A solves {{a}}/{{n}} and model B {{b}}/{{n}} of the same-sized independent item sets. What is the z-score of the difference (unpooled SE)?",
        given={"a": {"pick": [120, 140]}, "b": {"pick": [150, 170]}, "n": {"pick": [200, 300]}},
        value="(b/n - a/n)/sqrt((a/n)*(1 - a/n)/n + (b/n)*(1 - b/n)/n)", tex="z",
        verify="(Rational(b, n) - Rational(a, n))/sqrt(Rational(a, n)*(1 - Rational(a, n))/n + Rational(b, n)*(1 - Rational(b, n))/n)",
        explain="|z| > 1.96 is significant at 5%; repeated samples of the same item need clustered SEs")),
    ("AIS-5.3.C", Q("ais-cohen-kappa", EV, "Two graders label {{n}} outputs pass/fail. They agree on {{agr}}. Grader A says pass {{pa}} times, B {{pb}} times. Find Cohen's κ.",
        given={"n": {"pick": [100]}, "agr": {"pick": [80, 85, 90]}, "pa": {"pick": [50, 60]}, "pb": {"pick": [55, 65]}},
        value="(agr/n - ((pa/n)*(pb/n) + (1 - pa/n)*(1 - pb/n)))/(1 - ((pa/n)*(pb/n) + (1 - pa/n)*(1 - pb/n)))", tex="\\kappa",
        verify="(Rational(agr, n) - (Rational(pa*pb, n*n) + Rational((n - pa)*(n - pb), n*n)))/(1 - (Rational(pa*pb, n*n) + Rational((n - pa)*(n - pb), n*n)))",
        explain="κ = (p_o − p_e)/(1 − p_e) with p_e from each grader's marginals")),
    ("AIS-5.3.C", facts("ais-grader-reliability", EV, [
        ("κ = 0.45 between a model grader and expert labels. Should you threshold on the model grader?", "No: below about 0.6 is weak agreement", "Yes, κ above 0 is enough", "Yes, if accuracy is high", "κ doesn't matter"),
        ("Why is raw percent agreement misleading when 90% of outputs pass?", "High agreement happens by chance when classes are unbalanced", "It is always exact", "It ignores graders", "It overweights fails"),
        ("Before trusting an LLM grader, you should:", "Validate it against expert labels on a sample", "Assume it matches humans", "Use the same model being tested", "Skip calibration"),
    ], "Chance-corrected agreement tells you whether grading is reliable")),
    ("AIS-5.3.D", Q("ais-sample-size", EV, "To detect success rates of {{p1}} vs {{p2}} at α = 0.05 (two-sided) and 80% power, how many participants per arm? (Use (1.96 + 0.84)² = 7.84.)",
        given={"p1": {"pick": [0.1, 0.2, 0.3]}, "p2": {"pick": [0.4, 0.5]}}, value="7.84*(p1*(1 - p1) + p2*(1 - p2))/(p1 - p2)^2", tex="n",
        verify="Rational(784, 100)*(nsimplify(p1)*(1 - nsimplify(p1)) + nsimplify(p2)*(1 - nsimplify(p2)))/(nsimplify(p1) - nsimplify(p2))**2",
        explain="Halving the detectable difference quadruples the sample")),
    ("AIS-5.3.D", Q("ais-sample-size-scale", EV, "A study needs n per arm to detect a {{d1}}-point difference. Roughly how many per arm to detect a {{d2}}-point difference with similar rates?",
        given={"d1": {"pick": [20, 30]}, "d2": {"pick": [10, 15]}}, value="(d1/d2)^2", tex="\\times n", verify="Rational(d1, d2)**2",
        explain="n ∝ 1/Δ²")),
    # 5.4
    ("AIS-5.4.A", facts("ais-elicitation-levers", EV, [
        ("A capability rule-out used only the default chat prompt. The main gap is:", "Inadequate elicitation (no scaffolds, tools, fine-tuning or best-of-n)", "Too many samples", "Too much compute", "Nothing"),
        ("PF v2 asks evaluators to test with:", "Top-tier settings, a helpful-only variant and the best scaffolds", "The safety-tuned model only", "One sample per item", "No tools"),
        ("Any single elicitation result should be read as:", "A lower bound on capability", "An upper bound", "Exact", "Irrelevant"),
        ("Which is an elicitation lever?", "Fine-tuning on the task", "Adding safety refusals", "Lowering the token limit", "Removing tools"),
    ], "A rule-out is only as strong as the elicitation behind it")),
    ("AIS-5.4.A", facts("ais-elicitation-2", EV, [
        ("Why test a helpful-only variant?", "Refusal training can hide capability that a misuser could unlock", "It is safer to deploy", "It is cheaper", "It has fewer parameters"),
        ("An eval fixes a small inference budget. Later, longer reasoning finds much higher scores. The original claim was:", "Under-elicited", "Over-elicited", "Exact", "Contaminated"),
        ("Which campaign is adequate for a rule-out?", "Strong scaffolds, tools, many samples and task fine-tuning, with results reported", "One prompt per item", "A survey of users", "Reading the system card"),
    ], "Try hard before claiming 'can't'")),
    ("AIS-5.4.B", Q("ais-elicitation-gap", EV, "Default prompting scores {{d}}%; the best elicitation scores {{b}}%. A threshold is set at {{t}}%. If later scaffolding adds the same gap again, does the best score cross it? Give the projected score.",
        given={"d": {"pick": [20, 30]}, "b": {"pick": [35, 45]}, "t": {"pick": [50, 60]}}, value="2*b - d", tex="\\%", verify="b + (b - d)",
        explain="Gap = best − default; margins should allow for future elicitation gains")),
    ("AIS-5.4.B", Q("ais-margin", EV, "An early-warning threshold must sit below a danger threshold of {{T}}% by the expected elicitation gain of {{g}} points plus {{s}} points of statistical uncertainty. Where should the warning fire?",
        given={"T": {"pick": [50, 60, 70]}, "g": {"pick": [5, 10, 15]}, "s": {"pick": [3, 5]}}, value="T - g - s", tex="\\%", verify="T - (g + s)",
        explain="Leave room for both unmeasured elicitation and sampling error")),
    ("AIS-5.4.C", facts("ais-sandbag-check", EV, [
        ("A small fine-tune on correct examples raises scores from 20% to 70%. This suggests the original score measured:", "Willingness more than capability", "True capability", "Contamination", "Nothing"),
        ("A password-locked model is used as a control to check that:", "Your elicitation methods can recover hidden capability", "The model is honest", "Passwords work", "Training is cheap"),
        ("A model does well when a task is framed as real work and badly when framed as a test. This is evidence of:", "Sandbagging or evaluation awareness", "Better elicitation", "Contamination", "Saturation"),
    ], "Check that low scores survive the strongest elicitation")),
    ("AIS-5.4.C", facts("ais-sandbag-check-2", EV, [
        ("Which result would most strongly rule out sandbagging?", "Fine-tuning and best scaffolds recover little extra performance", "The model says it isn't sandbagging", "Scores are low", "The eval is short"),
        ("Consistency across framings means:", "The same task posed many ways gives similar scores", "Using one prompt", "Asking the model to be consistent", "Repeating one sample"),
        ("Why can't you ask the model whether it is sandbagging?", "A sandbagging model could misreport", "It doesn't understand", "It is illegal", "It slows evaluation"),
    ], "Behavioural checks beat self-report")),
    # 5.5
    ("AIS-5.5.A", facts("ais-briefing", EV, [
        ("A one-page briefing on a dangerous-capability section should separate:", "Evidence (scores, elicitation, baselines, intervals) from judgement (the threshold call)", "Marketing from science", "Long from short models", "Old from new data"),
        ("Which belongs in the briefing?", "What was tested, how hard, against what baseline, and the conclusion", "Raw hazardous transcripts", "Employee names", "The full training set"),
        ("Redactions and untested pathways should be:", "Flagged explicitly", "Omitted", "Guessed at", "Treated as passed"),
    ], "A decision-maker needs the evidence, its strength and the call")),
    ("AIS-5.5.A", facts("ais-briefing-2", EV, [
        ("A system card says 'the model does not pose significant uplift'. The first question a briefer should ask:", "Against what baseline and with what elicitation?", "What colour is the logo?", "How long is the card?", "Who wrote it?"),
        ("A score of 42% with no human expert baseline:", "Can't be judged against a threshold", "Is clearly safe", "Is clearly dangerous", "Is irrelevant"),
        ("The best one-line summary distinguishes:", "What the evidence shows from what the developer concluded", "Opinions from facts about the company", "Revenue from cost", "Open from closed"),
    ], "Keep the evidence and the judgement visibly apart")),
    ("AIS-5.5.B", facts("ais-card-critique", EV, [
        ("A report gives a score but no confidence interval. What's missing?", "Uncertainty", "Elicitation detail", "Threat model", "Baseline"),
        ("A report compares against no human or expert baseline. What's missing?", "A baseline", "Uncertainty", "A threat model", "A scaffold"),
        ("A report doesn't say which prompts, tools or fine-tuning were used. What's missing?", "Elicitation detail", "Uncertainty", "A baseline", "A threat model"),
        ("A report doesn't explain why the benchmark relates to real-world harm. What's missing?", "The threat-model link", "Uncertainty", "Elicitation detail", "A baseline"),
    ], "No baseline and no interval means no comparison to a threshold")),
    ("AIS-5.5.B", facts("ais-card-critique-2", EV, [
        ("Which addition would most improve a terse eval report?", "Elicitation details, a baseline and confidence intervals", "A longer introduction", "More marketing", "Removing numbers"),
        ("An eval report pools all attack categories into one rate. The problem:", "Weak categories can hide behind strong ones", "Pooling is always best", "It inflates sample size correctly", "None"),
        ("A report omits the inference budget. Why does that matter?", "Scores can change a lot with more test-time compute", "It doesn't", "Budgets are secret", "It only affects cost"),
    ], "Critique by what a reader would need to check the claim")),
    # 6.1
    ("AIS-6.1.A", facts("ais-actor-tier", DC, [
        ("PF v2's Bio/Chem High threshold concerns meaningful counterfactual help to:", "Novices, with known threats", "State programmes with novel threats", "Developers", "Nobody"),
        ("PF v2's Critical threshold adds help to experts with:", "Novel threats, or a full cycle without humans", "Known threats only", "Defensive research", "Publication"),
        ("RSP CBRN thresholds are written as uplift to:", "Defined actor tiers, such as moderately resourced state programmes", "All users equally", "Only researchers", "Benchmarks"),
    ], "Thresholds are defined by who is helped and how much")),
    ("AIS-6.1.A", facts("ais-actor-tier-2", DC, [
        ("A result shows the model helps trained experts plan faster but adds nothing for novices. Which tier is affected?", "Expert", "Novice", "None", "All equally"),
        ("Why does the actor tier matter for a threshold?", "The same help means different marginal risk for different actors", "It doesn't", "Only for cyber", "Only for marketing"),
        ("'Counterfactual' uplift compares the actor with the model against:", "The same actor with existing tools", "Nobody", "The developers", "Last year's model only"),
    ], "Uplift is relative to what each actor could already do")),
    ("AIS-6.1.B", facts("ais-tracking-criteria", DC, [
        ("Which is not one of PF v2's five tracking criteria?", "Popular with users", "Plausible", "Measurable", "Net new"),
        ("'Severe' in PF v2 means roughly:", "Thousands dead or hundreds of billions of dollars of damage", "Any harm", "Reputational harm", "Ten people affected"),
        ("'Net new' asks whether the risk:", "Could not already be achieved with pre-2021 tools", "Is new to the news", "Is cheap", "Involves new laws"),
        ("A proposed risk is severe but cannot be measured. Under PF v2 it is:", "Not a tracked category (it may be a research category)", "Tracked", "Ignored entirely", "Critical"),
    ], "Plausible, measurable, severe, net new, instantaneous or irremediable")),
    ("AIS-6.1.B", facts("ais-tracking-criteria-2", DC, [
        ("Which category does PF v2 track?", "AI self-improvement", "Persuasion", "Bias", "Copyright"),
        ("Why does PF v2 require 'measurable'?", "Thresholds must be checkable by evaluations", "To reduce cost", "To please regulators only", "It doesn't"),
        ("A risk that unfolds slowly and can be remedied fails which criterion?", "Instantaneous or irremediable", "Plausible", "Measurable", "Severe"),
    ], "The criteria decide what gets thresholds and safeguards")),
    # 6.2
    ("AIS-6.2.A", facts("ais-uplift-design", DC, [
        ("An uplift RCT's participants should be matched to:", "The threat actor in the threat model", "The developers", "Random volunteers", "Experts only"),
        ("The control arm should have:", "The tools the actor could already use, such as internet search", "Nothing at all", "The same model", "A weaker model only"),
        ("The outcome should be measured:", "Blind and by expert graders, against a pre-registered rubric", "By the participants themselves", "By the developer's marketing team", "After unblinding"),
        ("Why pre-register the analysis?", "To prevent choosing metrics after seeing results", "To speed publication", "To hide results", "It is required by law"),
    ], "Uplift is counterfactual: compare with what the actor could already do")),
    ("AIS-6.2.A", facts("ais-uplift-design-2", DC, [
        ("Which outcome is a weaker proxy for real-world success?", "Accuracy of a written plan", "End-to-end task completion", "Both equally", "Neither"),
        ("Why must hazardous study outputs be stored with restricted access?", "They may contain information that should not spread", "They are large", "They are boring", "They are already public"),
        ("A within-subject design (same people with and without the model) risks:", "Learning effects from the first attempt", "Too much power", "No variance", "Perfect blinding"),
    ], "Design for a credible counterfactual and safe handling")),
    ("AIS-6.2.B", Q("ais-uplift-rr", DC, "In an uplift study, {{a}}/{{n}} participants with model access and {{b}}/{{n}} controls produce an accurate protocol. What is the relative risk?",
        given={"a": {"pick": [14, 20, 28]}, "b": {"pick": [3, 5, 6]}, "n": {"pick": [30, 40]}}, value="a/b", tex="RR", verify="Rational(a, n)/Rational(b, n)",
        explain="RR = p_treat/p_control (UK AISI reported 4.7× for one such study)")),
    ("AIS-6.2.B", Q("ais-uplift-diff", DC, "With {{a}}/{{n}} successes with the model and {{b}}/{{n}} without, give the difference in proportions (percentage points) and its standard error; enter the SE.",
        given={"a": {"pick": [14, 20]}, "b": {"pick": [3, 5]}, "n": {"pick": [30, 40]}},
        value="100*sqrt((a/n)*(1 - a/n)/n + (b/n)*(1 - b/n)/n)", tex="SE",
        verify="100*sqrt(Rational(a, n)*(1 - Rational(a, n))/n + Rational(b, n)*(1 - Rational(b, n))/n)",
        explain="With arms this small the interval is wide: report it")),
    ("AIS-6.2.C", facts("ais-uplift-flaw", DC, [
        ("The study scores written protocols, not real execution. Flaw:", "Proxy outcome", "Underpowered arms", "Weak control", "Unblinded grading"),
        ("Controls had no internet access while the treatment arm had the model. Flaw:", "Weak control", "Proxy outcome", "Contamination", "Saturation"),
        ("Each arm had 6 participants. Flaw:", "Underpowered arms", "Proxy outcome", "Weak control", "Leaky grader"),
        ("Graders knew which arm each answer came from. Flaw:", "Unblinded grading", "Underpowered arms", "Proxy outcome", "Weak control"),
    ], "IASR 2026 calls real-world uplift highly uncertain")),
    ("AIS-6.2.C", facts("ais-uplift-flaw-2", DC, [
        ("Participants were all PhD experts, but the threshold concerns novices. Flaw:", "Population doesn't match the threat actor", "Too much power", "Saturation", "Contamination"),
        ("The study tested an older model than the one being released. Flaw:", "Wrong model version", "Weak control", "Proxy outcome", "Blinding"),
        ("A null result with wide confidence intervals shows:", "The study can't rule out meaningful uplift", "No uplift exists", "Large uplift", "Perfect safety"),
    ], "Absence of evidence in a small study is not evidence of absence")),
    # 6.3
    ("AIS-6.3.A", Q("ais-horizon-project", DC, "A model's 50%-success task horizon is {{h0}} minutes and doubles every {{Td}} months. What is it after {{t}} months?",
        given={"h0": {"pick": [30, 60, 90]}, "Td": {"pick": [7, 8]}, "t": {"pick": [12, 24, 36]}}, value="h0*2^(t/Td)", tex="h",
        verify="h0*2**Rational(t, Td)", explain="h(t) = h₀·2^(t/T_d)")),
    ("AIS-6.3.A", Q("ais-horizon-cross", DC, "Horizon now {{h0}} min, doubling every {{Td}} months. When (months) does it reach {{h}} hours?",
        given={"h0": {"pick": [30, 60]}, "Td": {"pick": [7, 8]}, "h": {"pick": [8, 40, 160]}}, value="Td*log(h*60/h0)/log(2)", tex="t",
        verify="Td*log(Rational(h*60, h0), 2)", explain="t = T_d·log₂(h/h₀)")),
    ("AIS-6.3.B", facts("ais-agentic-harness", DC, [
        ("In an Inspect-style harness, the solver is:", "The scaffold that drives the model and its tools", "The dataset", "The grader", "The sandbox"),
        ("The sandbox:", "Bounds what the agent can touch", "Grades outputs", "Stores the dataset", "Trains the model"),
        ("Why score sub-tasks as well as end-to-end success?", "Stage scores show where a chain breaks", "To inflate scores", "Sub-tasks are cheaper only", "They are required by law"),
        ("RepliBench found models:", "Strong at early stages, weak at later ones", "Uniformly strong", "Uniformly weak", "Untested"),
    ], "Dataset → solver → scorer, inside a sandbox")),
    ("AIS-6.3.B", facts("ais-agentic-harness-2", DC, [
        ("An agentic eval reports only final success, 5%. What extra data would help most?", "Per-stage success rates", "Model size", "Prompt length", "Training data"),
        ("Why must agentic evals run in an isolated sandbox?", "The agent may take real actions with real effects", "For speed", "To save money", "It is traditional"),
        ("Repeating each task several times (AISI repeats 10×) lets you:", "Estimate variability and success probability per task", "Train the model", "Reduce cost", "Avoid grading"),
    ], "Agentic evals need isolation, repetition and stage-wise scoring")),
    # 6.4
    ("AIS-6.4.A", facts("ais-redteam-plan", DC, [
        ("A red-team plan should fix in advance:", "Scope, threat model, expertise, success criteria and severity rubric", "Only the date", "The press release", "The model's answers"),
        ("Hazardous transcripts from a campaign need:", "Restricted storage and cleared graders", "Public posting", "Deletion before grading", "Social media sharing"),
        ("PF v2 uses expert deep dives to:", "Validate automated evals", "Replace all evals", "Train the model", "Write marketing"),
    ], "Plan, contain and validate")),
    ("AIS-6.4.A", facts("ais-redteam-plan-2", DC, [
        ("Who should red-team a domain-specific misuse risk?", "People with expertise matched to the threat actor", "Anyone available", "The model's developers only", "Random users"),
        ("A success criterion should be:", "Defined before the campaign starts", "Chosen after seeing results", "Secret from the team", "Unmeasurable"),
        ("Why include a severity rubric?", "Not every bypass is equally harmful", "To slow the team", "To guarantee success", "It is decorative"),
    ], "Decide what counts as a finding before you look")),
    ("AIS-6.4.B", facts("ais-redteam-types", DC, [
        ("Probing what the model can do with safeguards off is:", "Model red-teaming", "Safeguards testing", "Automated red-teaming", "Benchmarking"),
        ("Measuring attacker effort to bypass deployed protections is:", "Safeguards testing", "Model red-teaming", "Automated red-teaming", "Uplift study"),
        ("Using models to generate attacks at scale is:", "Automated red-teaming", "Safeguards testing", "Model red-teaming", "An RCT"),
        ("A weakness of automated red-teaming:", "It misses novel attacks humans would find", "It is too slow", "It has no coverage", "It needs experts only"),
    ], "Each kind supports a different claim")),
    ("AIS-6.4.B", facts("ais-redteam-types-2", DC, [
        ("Which supports the claim 'our deployed system resists misuse'?", "Safeguards testing", "Model red-teaming", "A benchmark", "A system card alone"),
        ("Which supports the claim 'the underlying model has capability X'?", "Model red-teaming with strong elicitation", "Safeguards testing", "User surveys", "Automated red-teaming only"),
        ("Combining automated and human red-teaming gives:", "Breadth from automation and novelty from humans", "Nothing new", "Only breadth", "Only novelty"),
    ], "Match the method to the claim")),
    ("AIS-6.4.C", Q("ais-harmful-rate", DC, "Red-teamers flag {{f}} harmful responses in {{n}} attempts. Give the harmful-response rate (%).",
        given={"f": {"pick": [6, 12, 25]}, "n": {"pick": [300, 500, 1000]}}, value="100*f/n", tex="\\%", verify="100*Rational(f, n)",
        explain="Report it with a confidence interval, by category, weighted by severity")),
    ("AIS-6.4.C", Q("ais-wilson", DC, "{{f}} flagged out of {{n}} attempts. Compute the Wilson 95% upper bound (%), with z = 1.96.",
        given={"f": {"pick": [0, 2, 5]}, "n": {"pick": [100, 200, 500]}},
        value="100*((f/n + 1.96^2/(2*n)) + 1.96*sqrt(f/n*(1 - f/n)/n + 1.96^2/(4*n^2)))/(1 + 1.96^2/n)", tex="UB",
        verify="100*((Rational(f, n) + Rational(196, 100)**2/(2*n)) + Rational(196, 100)*sqrt(Rational(f, n)*(1 - Rational(f, n))/n + Rational(196, 100)**2/(4*n**2)))/(1 + Rational(196, 100)**2/n)",
        explain="Wilson intervals stay sensible near zero, unlike p ± 1.96·SE; zero findings does not mean a zero rate")),
    ("AIS-6.4.D", facts("ais-disclosure", DC, [
        ("Which part of a dangerous-capability eval should usually be published?", "Methods, aggregate scores and thresholds", "Operational hazardous content", "Raw transcripts", "Successful attack strings"),
        ("RSP Risk Reports must:", "Mark where redactions were made", "Contain no redactions", "Be secret entirely", "Be written by the government"),
        ("What decides what an AI Safety Institute discloses?", "Each testing agreement", "Nothing", "The model", "Public demand only"),
        ("A successful jailbreak against a deployed system should first go to:", "The developer through responsible disclosure", "Social media", "A paper preprint", "Nobody"),
    ], "Publish enough to check the claim; withhold what enables harm")),
    ("AIS-6.4.D", facts("ais-disclosure-2", DC, [
        ("Why publish aggregate results while withholding specifics?", "Others can scrutinise the claim without gaining harmful capability", "To look transparent only", "Because specifics are boring", "Regulators forbid aggregates"),
        ("A finding reveals a new class of vulnerability in many models. A responsible step:", "Coordinate disclosure with affected developers before publishing", "Publish attack code immediately", "Ignore it", "Sell it"),
        ("Who should see unredacted hazardous details?", "People with a need to know and appropriate clearance", "Everyone", "No one, ever", "Only the press"),
    ], "Disclosure is tiered by audience and hazard")),
    # 7.1
    ("AIS-7.1.A", facts("ais-control-protocol", CT, [
        ("A weaker trusted model scores each action of the strong model, and the top suspicious ones go to humans. Protocol:", "Trusted monitoring", "Untrusted monitoring", "Defer-to-trusted", "Trusted editing"),
        ("Suspicious actions are replaced by the trusted model's own output. Protocol:", "Defer-to-trusted", "Trusted monitoring", "Untrusted monitoring", "Trusted editing"),
        ("A second copy of the strong model monitors the first. Protocol:", "Untrusted monitoring", "Trusted monitoring", "Defer-to-trusted", "Trusted editing"),
        ("The trusted model rewrites the strong model's output to remove anything suspicious. Protocol:", "Trusted editing", "Defer-to-trusted", "Trusted monitoring", "Untrusted monitoring"),
    ], "Control assumes the strong model may scheme")),
    ("AIS-7.1.A", facts("ais-control-concepts", CT, [
        ("In AI control, 'trusted' means:", "Weaker but assumed not to be scheming", "Stronger", "Open source", "Certified"),
        ("The scarce resource in control protocols is usually:", "Human audit budget", "GPU memory", "Tokens", "Electricity"),
        ("Control evaluations test protocols by having:", "A red team play the scheming model", "The model promise to behave", "Users vote", "No adversary"),
        ("Untrusted monitoring's main risk is:", "Collusion between the monitor and the policy", "Too much compute", "Weak capabilities", "Latency"),
    ], "Ask whether harm is prevented even if the model tries")),
    ("AIS-7.1.B", Q("ais-catch-prob", CT, "Each attack attempt is caught with probability {{p}}. What is the chance at least one of {{k}} attempts is caught?",
        given={"p": {"pick": [0.1, 0.2, 0.3]}, "k": {"pick": [1, 3, 10]}}, value="1 - (1 - p)^k", tex="P", verify="1 - (1 - nsimplify(p))**k",
        explain="1 − (1 − p)^k: the attacker's best response is few, well-chosen attempts")),
    ("AIS-7.1.B", Q("ais-audit-needed", CT, "How high must the per-attempt catch probability be for a {{P}}% chance of catching at least one of {{k}} attempts?",
        given={"P": {"pick": [90, 95, 99]}, "k": {"pick": [3, 5, 10]}}, value="1 - (1 - P/100)^(1/k)", tex="p",
        verify="1 - (1 - Rational(P, 100))**Rational(1, k)", explain="Solve 1 − (1 − p)^k = P")),
    ("AIS-7.1.C", facts("ais-cot-monitor", CT, [
        ("CoT monitoring works while:", "Hard reasoning has to pass through readable text", "Models are small", "Outputs are short", "Training is fast"),
        ("Which would erode CoT monitorability?", "Optimisation pressure on the CoT and latent reasoning", "Longer CoTs", "Monitoring more", "Human review"),
        ("Training a model to avoid 'bad thoughts' in its CoT risks:", "Hiding the intent while keeping the behaviour", "Removing the behaviour", "Making it more honest", "Nothing"),
    ], "Don't train against the monitor you rely on")),
    ("AIS-7.1.C", facts("ais-cot-monitor-2", CT, [
        ("A CoT monitor catches reward hacking by reading:", "Stated plans to exploit the grader", "Only final answers", "Logits", "Timing"),
        ("Why might a CoT be unfaithful?", "The written reasoning need not be the computation that produced the answer", "It is always faithful", "It's too long", "It's encrypted"),
        ("Which design preserves monitorability?", "Keep CoTs out of the reward signal", "Reward short CoTs only", "Penalise suspicious words", "Hide CoTs from all monitors"),
    ], "Monitorability is fragile and must be protected")),
    # 7.2
    ("AIS-7.2.A", facts("ais-kill-chain", CT, [
        ("Defence in depth (IASR 2026) layers:", "Access controls, classifiers, usage monitoring and incident response", "One strong filter", "Only training", "Only law"),
        ("Each layer in defence in depth only has to:", "Stop some attempts", "Stop all attempts", "Be perfect", "Replace the others"),
        ("Breaking a kill chain is cheapest where:", "A step is hard for the attacker and easy for you to block", "The attacker is strongest", "No layer exists", "The model is largest"),
    ], "Choose layers by where they cheaply remove a necessary step")),
    ("AIS-7.2.A", facts("ais-kill-chain-2", CT, [
        ("For misuse via an API, which layer acts before any output is generated?", "Access controls and know-your-customer checks", "Incident response", "Post-hoc audits", "Publication"),
        ("Which layer catches slow, repeated probing across sessions?", "Usage monitoring", "A single input classifier", "The model's refusal training", "The license"),
        ("Incident response matters because:", "Some attempts will get through every preventive layer", "Prevention is perfect", "It is cheaper than prevention", "Laws require only that"),
    ], "Prevention, detection and response together")),
    ("AIS-7.2.B", Q("ais-layered-risk", CT, "Three independent layers let an attack through with probabilities {{a}}, {{b}} and {{c}}. What is the chance it passes all three?",
        given={"a": {"pick": [0.1, 0.2, 0.3]}, "b": {"pick": [0.2, 0.5]}, "c": {"pick": [0.1, 0.4]}}, value="a*b*c", tex="P",
        verify="nsimplify(a)*nsimplify(b)*nsimplify(c)", explain="Independence lets you multiply; correlated failures break this")),
    ("AIS-7.2.B", facts("ais-correlated-layers", CT, [
        ("Why does a universal jailbreak hurt layered defences?", "It can defeat several layers at once, correlating failures", "It only affects one layer", "It improves independence", "It doesn't"),
        ("Two classifiers trained on the same data share blind spots. Treating them as independent:", "Overstates protection", "Understates it", "Is exact", "Doesn't matter"),
        ("Which layer pairing is most independent?", "A model-based classifier plus account-level human review", "Two copies of the same classifier", "Two prompts", "Two refusals"),
    ], "Independence must be argued, not assumed")),
    # 7.3
    ("AIS-7.3.A", facts("ais-weight-security", CT, [
        ("RAND's SL1–SL5 scale runs from:", "Amateur attackers up to top-priority state operations", "Low to high model size", "Open to closed licences", "Cheap to expensive chips"),
        ("Which control addresses insider threat?", "Multi-party access and insider-threat programmes", "A public licence", "Bigger models", "Rate limits"),
        ("Egress limits help against:", "Exfiltration of weights", "Prompt injection", "Sycophancy", "Contamination"),
        ("Matching an attacker class to a security level means:", "Defending well enough against the strongest attacker you expect", "Defending against everyone equally", "Ignoring state actors", "Only using encryption"),
    ], "Security levels scale with the attacker you must stop")),
    ("AIS-7.3.A", facts("ais-weight-security-2", CT, [
        ("A top-priority state operation is the attacker class for:", "The highest security level", "Basic security", "No security", "Open release"),
        ("Hardened hardware and confidential computing aim to:", "Keep weights protected even from parts of the infrastructure", "Speed inference", "Improve accuracy", "Lower cost"),
        ("Opportunistic attackers are stopped mainly by:", "Standard good security hygiene", "Air gaps", "State-level controls", "Nothing"),
    ], "Different attackers, different controls")),
    ("AIS-7.3.B", facts("ais-stolen-weights", CT, [
        ("After weights are stolen, which safeguard still applies?", "None of the deployment-side ones", "Usage monitoring", "API classifiers", "Rate limits"),
        ("Why is release irreversible?", "Copies can't be recalled once distributed", "It can be revoked", "Licences enforce deletion", "Models expire"),
        ("Whoever holds the weights can:", "Fine-tune out refusals and skip monitoring", "Only run them as shipped", "Not modify them", "Be tracked automatically"),
    ], "Deployment safeguards are only as strong as weight security")),
    ("AIS-7.3.B", facts("ais-stolen-weights-2", CT, [
        ("Why does weight security become more important as capability rises?", "Theft would hand over capability with none of its safeguards", "It doesn't", "Bigger models are easier to steal", "Laws demand it only"),
        ("A frontier lab's safety case relies on API safeguards. Which assumption must also hold?", "The weights are secure", "Users are honest", "The model is open", "Training is cheap"),
        ("Open-weight release and theft are similar in that both:", "Put the weights beyond deployment controls", "Are legal", "Are reversible", "Are rare"),
    ], "No weights, no misuse via the weights")),
]
