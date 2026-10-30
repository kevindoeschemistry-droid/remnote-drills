# AI Safety — curriculum framework (draft 1)

Generated from `drills/frameworks/ai-safety.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**104 learning objectives** in 12 units (100 core): 0 drilled, 0 partly, 104 with no drills. Core: 0 / 100 drilled.

## Big ideas

- **OPT · Optimisation finds what you measure, not what you meant.** Training, RL and evaluation all optimise a proxy; with enough pressure the proxy and the intent come apart — in the model (reward hacking, misgeneralisation) and in the institution (Goodharted benchmarks and thresholds).
- **OBS · You can only govern what you can observe.** Every safety claim rests on evidence — evals, interpretability, monitoring — and that evidence is a lower bound shaped by elicitation, validity and the model's awareness of being tested.
- **SCALE · Capability scales predictably in aggregate, unpredictably in specifics.** Loss, compute and task horizons follow smooth trends you can extrapolate; which dangerous capability arrives when does not, so commitments are written as if-then triggers.
- **DEF · No single layer is enough.** Alignment, control, safeguards, security and governance each fail sometimes; risk falls by stacking imperfect layers whose failures are not correlated.
- **INC · Incentives and coordination set the ceiling.** Race dynamics, chokepoints and verification decide which safety measures actually get adopted; the strategic question is who can act, and what would make restraint stable.

## Practices

- **P1 · Diagnose.** Classify a described behaviour, result or scenario into the right failure mode, threat category or mechanism — and say what evidence separates it from the nearest alternative.
- **P2 · Model the threat.** State actor, resources, pathway and bottleneck; say what the model would have to contribute for harm to become more likely, and against what baseline.
- **P3 · Design and critique evidence.** Build or audit an eval, study or experiment — construct validity, contamination, elicitation, controls, grading, power — and say what the result does and doesn't license.
- **P4 · Compute.** FLOP, parameters, scaling-law extrapolation, pass@k, confidence intervals, agreement, effect sizes, catch probabilities and forecasts — with orders of magnitude checked.
- **P5 · Map to commitments.** Read a framework, law or standard closely enough to say which threshold or obligation a described result triggers, what must happen next and who decides.
- **P6 · Argue and decide.** Steelman competing positions, find the crux, prioritise interventions and write the conclusion for a decision-maker.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · ML foundations for safety | core | — | 10 | 0 | 0 | 10 |
| 2 · Alignment problems | core | — | 10 | 0 | 0 | 10 |
| 3 · Alignment techniques | core | — | 8 | 0 | 0 | 8 |
| 4 · Interpretability | core | — | 10 | 0 | 0 | 10 |
| 5 · Evaluation science | core | — | 14 | 0 | 0 | 14 |
| 6 · Dangerous-capability evaluations and red-teaming (methodology) | core | — | 11 | 0 | 0 | 11 |
| 7 · Control, monitoring and security | core | — | 7 | 0 | 0 | 7 |
| 8 · Frontier safety frameworks and safety cases | core | — | 10 | 0 | 0 | 10 |
| 9 · Regulation, standards, compute and coordination | core | — | 13 | 0 | 0 | 13 |
| 10 · Strategy and forecasting | core | — | 7 | 0 | 0 | 7 |
| 11 · Mechanistic interpretability, deeper | extension | — | 2 | 0 | 0 | 2 |
| 12 · Agentic and multi-agent risk | extension | — | 2 | 0 | 0 | 2 |

## Unit 1 · ML foundations for safety

Big ideas: SCALE, OPT

### 1.1 The transformer

Book: arena §Ch 0, §Ch 1; bluedot-tais §Unit 4 §4.1

- ○ **AIS-1.1.A** Trace a token through a decoder-only transformer — embedding, residual stream, attention, MLP, unembedding — and say what each component reads from and writes to the residual stream.
  - EK: Every layer adds to one shared residual stream; attention moves information between positions, MLPs transform each position separately.
  - EK: Causal masking lets position t attend only to positions ≤ t; sampling is from softmax(logits / T).
  - P1
- ○ **AIS-1.1.B** Calculate a transformer's parameter count from d_model, n_layers and vocabulary size (drill: compute).
  - EK: Per layer ≈ 12·d_model² (4d² attention + 8d² MLP with d_mlp = 4d); embeddings add V·d (×2 if untied).
  - P4

### 1.2 Pretraining, compute and scaling laws

Book: arena §Ch 1; bluedot-agi §Unit 2 §2.1; iasr-2026 §§Capabilities

- ○ **AIS-1.2.A** Estimate training compute from parameters and tokens, and convert it to chip-days at a stated utilisation (drill: compute).
  - EK: C ≈ 6ND (2ND forward, 4ND backward); time = C / (N_chips × peak FLOP/s × MFU).
  - P4
- ○ **AIS-1.2.B** Find the compute-optimal model size and token count for a budget with the Chinchilla rule (drill: compute).
  - EK: Compute-optimal D ≈ 20N; with C = 6ND, N ≈ √(C/120).
  - Needs: AIS-1.2.A
  - P4
- ○ **AIS-1.2.C** Extrapolate loss from a fitted power law, and explain why smooth loss gains need not predict when a specific capability appears (drill: compute).
  - EK: L(C) = L∞ + a·C^(−α) is a straight line on log–log axes above the irreducible loss.
  - EK: Task metrics can jump with scale; part of 'emergence' is the choice of a thresholded metric.
  - P4 · P5
- ○ **AIS-1.2.D** Decompose growth in effective compute into hardware/spend and algorithmic efficiency, and project it a few years forward (drill: compute).
  - EK: IASR 2026: training compute ~5×/yr, algorithmic efficiency 2–6×/yr; the factors multiply.
  - P4 · P6

### 1.3 Post-training — RLHF, RLAIF, DPO and reasoning models

Book: arena §Ch 2; bluedot-tais §Unit 2 §2.3; iasr-2026 §§Capabilities

- ○ **AIS-1.3.A** Lay out the RLHF pipeline — SFT, preference data, reward model, RL with a KL penalty — and say what each stage contributes.
  - EK: Objective: maximise E[r_φ(x, y)] − β·KL(π ‖ π_ref); the KL term keeps the policy near the SFT model and limits reward-model exploitation.
  - EK: PPO clips the policy ratio to [1 − ε, 1 + ε] so one update can't move the policy far.
  - P1
- ○ **AIS-1.3.B** Calculate preference probabilities from a Bradley–Terry reward model (drill: compute).
  - EK: P(y₁ ≻ y₂) = σ(r₁ − r₂); a reward gap of 1 ≈ 73 %, of 2 ≈ 88 %.
  - P4
- ○ **AIS-1.3.C** Contrast RLHF, RLAIF/constitutional feedback and DPO by where the preference signal comes from and whether a separate reward model is trained (drill: classify).
  - EK: DPO solves the same KL-regularised objective in closed form from preference pairs; RLAIF replaces human raters with a model guided by written principles.
  - P1
- ○ **AIS-1.3.D** Explain how RL on verifiable rewards and inference-time compute produce reasoning models, and what that shifts for evaluation.
  - EK: IASR 2026: much recent gain comes from post-training and test-time compute, so capability can jump without a bigger pretraining run — and an eval must fix the inference budget it tested at.
  - P1 · P3

## Unit 2 · Alignment problems

Big ideas: OPT, OBS

### 2.1 Specification gaming and reward hacking

Book: bluedot-tais §Unit 1 §1.3; iasr-2026 §§Risks: malfunctions; uk-aisi §Pre-deployment testing: cheating behaviour

- ○ **AIS-2.1.A** Classify a described failure as specification gaming, reward hacking/tampering, goal misgeneralisation, sycophancy, deceptive alignment or a plain capability failure (drill: classify).
  - EK: Ask in order: was the objective itself wrong (specification gaming)? was the reward signal exploited or tampered with (reward hacking)? is the goal wrong only off-distribution (misgeneralisation)? is the user's view echoed (sycophancy)? is good behaviour strategic (deception)? none — it just couldn't (capability).
  - P1
- ○ **AIS-2.1.B** Explain Goodhart's law and predict how a proxy reward diverges from the true objective as optimisation pressure grows.
  - EK: Proxy and target correlate in the bulk of the distribution and decouple in the tails that strong optimisation reaches.
  - EK: Reward-model overoptimisation: gold reward rises, then falls, as KL from the initial policy grows.
  - P1 · P6
- ○ **AIS-2.1.C** Identify reward hacking in a described coding or agentic transcript — special-casing tests, editing the grader, claiming unverified success — and say what it does to the measurement (drill: classify).
  - EK: A pass won by exploiting the checker scores capability that isn't there; trained on, it reinforces the habit. Read transcripts, not only scores.
  - P1 · P3

### 2.2 Goal misgeneralisation and inner alignment

Book: bluedot-tais §Unit 1 §1.3

- ○ **AIS-2.2.A** Distinguish goal misgeneralisation from capability misgeneralisation in a described distribution shift (drill: classify).
  - EK: Goal misgeneralisation: capabilities carry over but pursue the wrong goal (the CoinRun agent runs right, not to the coin). Capability misgeneralisation: the agent just becomes incompetent.
  - P1
- ○ **AIS-2.2.B** Distinguish outer from inner misalignment in a described failure (drill: classify).
  - EK: Outer: the training objective is wrong. Inner: the objective was fine on the training data but the learned model pursues something else; many goals fit the same training reward.
  - P1

### 2.3 Sycophancy and honesty

Book: bluedot-tais §Unit 2 §2.3; iasr-2026 §§Risks: systemic

- ○ **AIS-2.3.A** Trace sycophancy back to preference training, and design a paired-prompt test that separates it from genuine agreement.
  - EK: Raters reward agreeable answers. Prompts identical except for the user's stated view isolate the effect; measure answer flips.
  - P1 · P3
- ○ **AIS-2.3.B** Distinguish confabulation, sycophancy and deception by what the model represents as true (drill: classify).
  - EK: Confabulation: no reliable knowledge. Sycophancy: knowledge overridden by a social cue. Deception: represents the truth and instrumentally induces a false belief.
  - P1

### 2.4 Deceptive alignment, scheming and situational awareness

Book: bluedot-tais §Unit 1 §1.3; bluedot-agi §Unit 3 §3.2; gdm-fsf §Misalignment / instrumental reasoning; openai-pf §Research categories: Sandbagging, Undermining Safeguards

- ○ **AIS-2.4.A** State the preconditions for scheming — a misaligned goal, situational awareness, and a reason to look aligned during training or testing — and judge which ones a described model shows (drill: classify).
  - EK: Without situational awareness a model can't condition behaviour on being watched; without a goal that outlasts the episode it has no reason to.
  - P1 · P2
- ○ **AIS-2.4.B** Explain instrumental convergence and why shutdown resistance and resource acquisition follow from many different goals.
  - EK: Staying on, keeping its goal and gaining resources help with almost any objective — which is why FSF frames misalignment risk as interfering with operators' ability to direct, modify or shut down.
  - P2
- ○ **AIS-2.4.C** Explain how evaluation awareness and sandbagging undermine safety testing, and name the evidence that would reveal them.
  - EK: IASR 2026: models increasingly recognise test settings. Signs: verbalised test-awareness, gaps between eval-like and deployment-like framings, underperformance that a light fine-tune removes.
  - P1 · P3

## Unit 3 · Alignment techniques

Big ideas: OPT, OBS, DEF

### 3.1 Training for safety

Book: bluedot-tais §Unit 2 §2.2, §Unit 2 §2.3, §Unit 2 §2.4

- ○ **AIS-3.1.A** Choose among pretraining-data filtering, SFT, preference training and constitutional training for a stated safety goal, and say what each can't fix.
  - EK: Data filtering removes knowledge; post-training mostly shapes whether knowledge is expressed, so later fine-tuning can undo it.
  - EK: Constitutional AI: principles drive self-critique (SL stage) and AI preference labels (RL stage).
  - Needs: AIS-1.3.A
  - P6
- ○ **AIS-3.1.B** Explain why refusal training is shallow against fine-tuning on released weights, and what tamper-resistant training attempts.
  - EK: A small harmful fine-tune can strip refusals; safeguards on open weights are easy to remove and the weights can't be recalled (IASR 2026).
  - P2

### 3.2 Scalable oversight

Book: bluedot-tais §Unit 2 §2.4

- ○ **AIS-3.2.A** Match debate, recursive reward modelling, iterated amplification and AI-assisted critique to how each lets a weak overseer judge a strong model (drill: classify).
  - EK: Debate: two models argue, a judge decides. RRM: models help humans evaluate the next model. Amplification: decompose into checkable sub-tasks. Critique: a model points out flaws for the human.
  - P1
- ○ **AIS-3.2.B** State the empirical condition debate needs, and read a debate or sandwiching result to say whether oversight improved.
  - EK: Debate works if lies are harder to defend than truths; test with weaker judges' accuracy under debate vs a single consultant.
  - EK: Sandwiching: non-experts with assistance on tasks the model can do, scored against experts.
  - P3

### 3.3 Weak-to-strong generalisation

Book: bluedot-tais §Unit 2 §2.4

- ○ **AIS-3.3.A** Calculate performance gap recovered from weak, weak-to-strong and strong-ceiling scores (drill: compute).
  - EK: PGR = (W2S − weak) / (ceiling − weak); 1 = full recovery, 0 = the strong student only imitates the weak labels.
  - P4
- ○ **AIS-3.3.B** Explain what weak-to-strong is an analogy for and where the analogy breaks.
  - EK: Humans supervising superhuman models. It breaks because today's strong students weren't trained to mislead, and imitating human errors may be easier than imitating a weak model's.
  - P6

### 3.4 Robustness and misuse safeguards

Book: bluedot-tais §Unit 5 §5.2; uk-aisi §Frontier AI Trends Report: safeguards; openai-pf §Safeguards against malicious users

- ○ **AIS-3.4.A** Classify a described jailbreak by mechanism — competing objectives, mismatched generalisation, many-shot, prompt injection — without reproducing it (drill: classify).
  - EK: Competing objectives pit helpfulness against harmlessness; mismatched generalisation uses inputs safety training didn't cover (encodings, low-resource languages); prompt injection arrives through data, not the user turn.
  - P1
- ○ **AIS-3.4.B** Explain why input/output classifiers plus adversarial training raise attacker cost without eliminating universal jailbreaks, and measure safeguards by cost, not only by success.
  - EK: UK AISI found a universal jailbreak in every system it tested; expert effort to jailbreak bio-misuse content varied ~40× between releases; capability barely predicted safeguard strength (R² ≈ 0.1).
  - P3

## Unit 4 · Interpretability

Big ideas: OBS

### 4.1 Features and superposition

Book: arena §Ch 1; bluedot-tais §Unit 4 §4.1

- ○ **AIS-4.1.A** State the linear representation hypothesis and explain why superposition makes neurons polysemantic.
  - EK: Features are directions in activation space. With sparse features a model stores more features than dimensions, at the cost of interference, so features aren't neuron-aligned.
  - P1
- ○ **AIS-4.1.B** Predict whether a toy model stores features in superposition from their sparsity and importance.
  - EK: Dense features: the top-d by importance get dedicated dimensions, the rest are dropped. As sparsity rises, features share dimensions (antipodal pairs, then polytopes).
  - P6

### 4.2 Sparse autoencoders

Book: arena §Ch 1; bluedot-tais §Unit 4 §4.2

- ○ **AIS-4.2.A** Write the SAE objective, explain each term, and name its failure modes (dead latents, feature splitting, absorption).
  - EK: L = ‖x − x̂‖² + λ‖f‖₁ with a dictionary wider than d_model; dictionary size changes which features appear, and absorption makes a latent's label misleading.
  - P1
- ○ **AIS-4.2.B** Evaluate an SAE from variance explained, mean L0 and the loss increase when it is spliced into the model (drill: compute).
  - EK: FVE = 1 − ‖x − x̂‖²/‖x − x̄‖²; report CE-loss increase on substitution; sparsity and fidelity trade off along a frontier.
  - P3 · P4

### 4.3 Circuits and causal interventions

Book: arena §Ch 1; bluedot-tais §Unit 4 §4.2

- ○ **AIS-4.3.A** Explain how a previous-token head and an induction head compose to copy in-context sequences.
  - EK: K-composition: the induction head's keys read the previous-token head's output, so it attends to the token after the earlier occurrence of the current token.
  - P1
- ○ **AIS-4.3.B** Design an activation-patching experiment and compute the normalised logit difference recovered (drill: compute).
  - EK: Patch clean activations into the corrupted run; recovered = (LD_patched − LD_corrupt) / (LD_clean − LD_corrupt).
  - P3 · P4
- ○ **AIS-4.3.C** Classify the evidence behind a described interpretability claim as correlational (probe, attention pattern, max-activating examples) or causal (ablation, patching, steering) (drill: classify).
  - EK: Only an intervention shows the model uses a representation; a probe shows it is decodable.
  - P1 · P3

### 4.4 Probing, steering and interpretability for safety cases

Book: arena §Ch 1; bluedot-tais §Unit 4 §4.2

- ○ **AIS-4.4.A** Design a linear probe with a control task and report its selectivity (drill: compute).
  - EK: Selectivity = probe accuracy − control-task accuracy; a high-capacity probe can learn the task itself.
  - P3 · P4
- ○ **AIS-4.4.B** Explain how a contrastive steering vector is built and what a successful steer does and doesn't show.
  - EK: v = mean(act | A) − mean(act | B); adding αv shifting behaviour shows the direction is causally used, not that it is the model's concept.
  - P1
- ○ **AIS-4.4.C** Judge what interpretability can contribute to a safety case today — audits, deception probes, monitors — and where it can't carry the argument.
  - EK: Useful as one layer; not yet enumerative, and robustness against a model optimising against the probe is unproven.
  - Needs: AIS-4.3.C
  - P6

## Unit 5 · Evaluation science

Big ideas: OBS, SCALE

### 5.1 What an eval measures

Book: bluedot-tais §Unit 3 §3.1; arena §Ch 3; openai-pf §Evaluations

- ○ **AIS-5.1.A** Classify a described eval as capability or propensity, and as static benchmark, agentic task, red-team exercise or human uplift study (drill: classify).
  - EK: Capability: can it, under best elicitation? Propensity: will it, under realistic conditions? The two need different setups and support different claims.
  - P1
- ○ **AIS-5.1.B** Write a threat model that links a capability to a harm pathway, and use it to decide what an eval must measure.
  - EK: Actor, resources, steps, and the bottleneck the model might remove; an eval targets the bottleneck, not the topic.
  - P2 · P3

### 5.2 Validity, contamination and saturation

Book: iasr-2026 §§Evaluation gaps; arena §Ch 3

- ○ **AIS-5.2.A** Spot the validity flaw in a described eval design — construct mismatch, contamination, saturation, leaky grader, answerable shortcut, unrealistic environment (drill: spot the flaw).
  - EK: Construct validity asks whether the score tracks the threat-model capability. IASR 2026: benchmarks are often outdated, narrow or contaminated, and pre-deployment tests often fail to predict real-world performance.
  - P3
- ○ **AIS-5.2.B** Detect and mitigate contamination with canary strings, private held-out sets, perturbed items and release-date splits.
  - EK: Contamination inflates scores through memorisation; a gap between original and rephrased items is the signature.
  - P3
- ○ **AIS-5.2.C** Explain why recognition-style (MCQ) knowledge benchmarks misjudge real-world capability, and what open-ended and agentic tasks add.
  - EK: Recognising an answer ≠ producing it or executing it; tacit knowledge and multi-step execution are usually the bottlenecks. Near-ceiling scores also compress differences.
  - P3 · P2

### 5.3 Statistics for evals

Book: arena §Ch 3; uk-aisi §Frontier AI Trends Report: methodology

- ○ **AIS-5.3.A** Compute pass@k from n samples with c correct using the unbiased estimator (drill: compute).
  - EK: pass@k = 1 − C(n − c, k) / C(n, k); not the same as 1 − (1 − c/n)^k when n is small.
  - P4
- ○ **AIS-5.3.B** Put a confidence interval on an eval score and decide whether two models really differ (drill: compute).
  - EK: SE = √(p(1 − p)/n), 95 % CI ≈ p ± 1.96 SE; repeated samples of the same item are clustered — cluster SEs by item (AISI repeats each task 10×).
  - P4 · P3
- ○ **AIS-5.3.C** Compute Cohen's κ for rubric-graded outputs and decide whether grading (human or model) is reliable enough to threshold on (drill: compute).
  - EK: κ = (p_o − p_e) / (1 − p_e); below ~0.6 is weak. Validate model graders against expert labels before trusting them.
  - P4 · P3
- ○ **AIS-5.3.D** Compute the sample size per arm needed to detect a target difference between two success rates (drill: compute).
  - EK: n ≈ (z_α/2 + z_β)² · [p₁(1 − p₁) + p₂(1 − p₂)] / (p₁ − p₂)²; at α = 0.05, power 0.8, (1.96 + 0.84)² ≈ 7.85.
  - P4 · P3

### 5.4 Elicitation and sandbagging

Book: openai-pf §Elicitation; uk-aisi §Best practice: elicitation, environmental realism; arena §Ch 3

- ○ **AIS-5.4.A** List the levers of elicitation — prompting, scaffolds and tools, best-of-n, fine-tuning, helpful-only variants, inference budget — and judge whether a described campaign was adequate for a rule-out claim (drill: spot the flaw).
  - EK: PF v2: test at top-tier settings, with a helpful-only variant and the best scaffolds; any one result is a lower bound, not a ceiling. A rule-out is only as strong as the elicitation behind it.
  - P3
- ○ **AIS-5.4.B** Estimate the elicitation gap and widen a threshold margin for future scaffolding gains (drill: compute).
  - EK: Gap = best-elicited − default score; Anthropic's six-month eval interval and PF's lower-bound language both assume later elicitation will find more.
  - P4 · P5
- ○ **AIS-5.4.C** Design a check for sandbagging: fine-tuning recovery, password-locked controls, consistency across framings.
  - EK: If a small fine-tune restores much higher scores, the original number measured willingness, not capability; PF asks for elicitation that overcomes deliberate underperformance or a conservative upper bound.
  - Needs: AIS-2.4.C
  - P3

### 5.5 Reporting evaluation results

Book: bluedot-gov §Unit 1; bluedot-tais §Unit 3 §3.2; rsp §Risk Reports; openai-pf §Capabilities Reports

- ○ **AIS-5.5.A** Read a system card's dangerous-capability section and write a one-page briefing for a decision-maker: what was tested, how hard, against what baseline, and what was concluded.
  - EK: Separate evidence (scores, elicitation, baselines, CIs) from judgement (the threshold call); flag redactions and untested pathways.
  - P6 · P3
- ○ **AIS-5.5.B** Critique a system card or eval report for missing information — elicitation detail, human/expert baselines, uncertainty, threat-model link (drill: spot the flaw).
  - EK: A score with no baseline and no interval can't be compared to a threshold.
  - P3

## Unit 6 · Dangerous-capability evaluations and red-teaming (methodology)

Big ideas: OBS, DEF

### 6.1 Threat models by domain

Book: openai-pf §Tracked categories, §Tracking criteria; gdm-fsf §CCLs; iasr-2026 §§Risks: malicious use; bluedot-agi §Unit 3 §3.4

- ○ **AIS-6.1.A** Identify, for a described result, which actor tier (novice, expert, state programme) and which kind of help (knowledge, troubleshooting, end-to-end execution) a framework's threshold is keyed to (drill: map to framework).
  - EK: PF v2 Bio/Chem High: meaningful counterfactual help to novices with known threats; Critical: experts to novel threats, or a full cycle without humans. RSP CBRN thresholds are written as uplift to defined actor tiers (e.g. moderately resourced state programmes).
  - P5 · P2
- ○ **AIS-6.1.B** Apply PF v2's five tracking criteria to decide whether a proposed risk belongs in a tracked category.
  - EK: Plausible, measurable, severe (thousands dead or hundreds of $bn), net new (not achievable with pre-2021 tools), instantaneous or irremediable.
  - P5 · P2

### 6.2 Uplift studies

Book: uk-aisi §Frontier AI Trends Report: chem/bio; iasr-2026 §§Risks: malicious use; bluedot-agi §Unit 3 §3.4

- ○ **AIS-6.2.A** Design an uplift RCT at the methodology level: participant population matched to the threat actor, internet-only control arm, model-assisted arm, blinded expert grading on a pre-registered rubric and threshold.
  - EK: Uplift is counterfactual: compare against what the actor could already do without the model, not against zero.
  - Needs: AIS-5.1.B
  - P3 · P2
- ○ **AIS-6.2.B** Compute an uplift effect — difference in proportions, relative risk, and its uncertainty — from arm-level counts (drill: compute).
  - EK: RR = p_treat / p_control; UK AISI reported non-specialists with a frontier model 4.7× more likely to produce an accurate protocol. With small arms the CI on RR is wide; report it.
  - Needs: AIS-5.3.B
  - P4
- ○ **AIS-6.2.C** Spot the validity flaw in a described uplift study — proxy outcome, weak control, underpowered arms, unblinded graders, participants unlike the threat actor (drill: spot the flaw).
  - EK: Written-protocol accuracy is a proxy for real-world success; IASR 2026 calls real-world uplift highly uncertain.
  - P3

### 6.3 Agentic, autonomy and AI R&D evals

Book: arena §Ch 3; uk-aisi §Frontier AI Trends Report: autonomy; iasr-2026 §§Capabilities; openai-pf §AI Self-improvement

- ○ **AIS-6.3.A** Project a 50 %-success task-time horizon forward with a doubling time, and find when it crosses a stated horizon (drill: compute).
  - EK: h(t) = h₀ · 2^(t / T_d); IASR 2026 cites a ~7-month doubling, AISI ~8 months for cyber tasks; t = T_d · log₂(h / h₀).
  - P4
- ○ **AIS-6.3.B** Lay out an agentic eval in an Inspect-style harness — dataset, solver/scaffold, tools, sandbox, scorer — and name the ways it can be reward-hacked or under-elicited.
  - EK: Dataset → solver → scorer; the sandbox bounds what the agent can touch; stage-wise sub-task scores show where an end-to-end chain breaks (RepliBench: strong early stages, weak later ones).
  - Needs: AIS-2.1.C
  - P3

### 6.4 Red-teaming and hazardous results

Book: bluedot-tais §Unit 3 §3.1, §Unit 5 §5.3; uk-aisi §Pre-deployment testing; openai-pf §Deep dives; nist-rmf §Measure

- ○ **AIS-6.4.A** Plan a red-team campaign: scope, threat model, red-teamer expertise, success criteria, severity rubric, and handling of hazardous outputs.
  - EK: PF v2 uses expert deep dives to validate automated evals; hazardous transcripts need restricted storage and cleared graders.
  - P3 · P2
- ○ **AIS-6.4.B** Distinguish model red-teaming, safeguards testing and automated red-teaming, and say what claim each result licenses (drill: classify).
  - EK: Model red-teaming probes capability; safeguards testing measures attacker effort to bypass deployed protections; automated red-teaming scales coverage but misses novel attacks.
  - P1 · P3
- ○ **AIS-6.4.C** Score red-team outputs with a severity/actionability rubric and report the harmful-response rate by category with a confidence interval (drill: compute).
  - EK: Rate = flagged / attempts with a Wilson or normal CI; weight by severity; report per attack category, not only pooled.
  - Needs: AIS-5.3.B
  - P4
- ○ **AIS-6.4.D** Decide what in an eval result can be published, what must be redacted, and what goes only to authorities.
  - EK: Publish methods, aggregates and thresholds; withhold operational content. RSP Risk Reports must mark redactions; institutes' disclosure depends on each testing agreement.
  - P6 · P5

## Unit 7 · Control, monitoring and security

Big ideas: DEF, OBS

### 7.1 AI control

Book: bluedot-tais §Unit 5 §5.1, §Unit 5 §5.2; uk-aisi §Best practice: control red team, control safety case

- ○ **AIS-7.1.A** Classify a control protocol — trusted monitoring, untrusted monitoring, defer-to-trusted, trusted editing, resampling — and predict its safety–usefulness trade-off (drill: classify).
  - EK: Control assumes the strong model may be scheming and asks whether the protocol still prevents harm; a red team plays the model. 'Trusted' = weaker but not scheming; human audit budget is the scarce resource.
  - P1 · P6
- ○ **AIS-7.1.B** Compute the probability a protocol catches a scheming model before it succeeds, from audit fraction, monitor recall and number of attack attempts (drill: compute).
  - EK: If each attempt is caught with probability p, P(caught at least once in k) = 1 − (1 − p)^k; the attacker's best response is few, well-chosen attempts.
  - P4
- ○ **AIS-7.1.C** Explain chain-of-thought monitorability and what would destroy it.
  - EK: CoT monitoring works while hard reasoning must pass through readable text; optimisation pressure on the CoT and latent reasoning erode it.
  - P1 · P6

### 7.2 Monitoring, kill chains and incident response

Book: bluedot-tais §Unit 5 §5.3; openai-pf §Safeguards: usage monitoring; iasr-2026 §§Risk management; eu-aia §Art 55 serious incidents

- ○ **AIS-7.2.A** Map a described misuse scenario onto a kill chain and choose the layer where breaking it is cheapest (drill: classify).
  - EK: Defence in depth (IASR 2026): access controls → classifiers → usage monitoring → incident response; each layer only has to stop some attempts.
  - P2 · P6
- ○ **AIS-7.2.B** Compute residual risk of layered defences assuming independence, and say why correlated failures break the estimate (drill: compute).
  - EK: P(all fail) = Π pᵢ only if failures are independent; a universal jailbreak or shared blind spot correlates the layers.
  - P4

### 7.3 Model weight security

Book: rsp §v2 ASL-3 Security Standard; openai-pf §Safeguards; uk-aisi §Best practice: security

- ○ **AIS-7.3.A** Match an attacker class (opportunistic, cybercrime, insider, state operation) to the weight-security level needed and the controls it implies (drill: classify).
  - EK: RAND SL1–SL5 scale from amateur attackers to top-priority state operations; controls include multi-party access, egress limits, hardened hardware and insider-threat programmes.
  - P1 · P2
- ○ **AIS-7.3.B** Explain why stolen or openly released weights remove every deployment-side safeguard.
  - EK: Whoever holds the weights can fine-tune out refusals and skip monitoring; release is irreversible (IASR 2026).
  - Needs: AIS-3.1.B
  - P2

## Unit 8 · Frontier safety frameworks and safety cases

Big ideas: DEF, INC, OBS

### 8.1 If-then commitments compared

Book: iasr-2026 §§Risk management; bluedot-tais §Unit 3 §3.2; rsp §v3.4; openai-pf §v2; gdm-fsf §v3

- ○ **AIS-8.1.A** Compare the RSP, Preparedness Framework and FSF on threshold names, tracked domains, who decides and what happens on crossing (drill: classify).
  - EK: If-then: a capability threshold, early-warning evals, the safeguards it requires, and a no-deploy condition. RSP: capability thresholds, Risk Reports, LTBT review. PF: High/Critical, Capabilities + Safeguards Reports, SAG advises, Leadership decides. FSF: CCLs with alert thresholds and response plans, safety case reviews.
  - P5
- ○ **AIS-8.1.B** Evaluate a framework on threshold specificity, external verification, enforceability and how it can be revised, and find who can actually say no (drill: spot the flaw).
  - EK: Most frameworks are voluntary and revisable by the company; triggers vary widely across companies (IASR 2026); SAG cannot block leadership.
  - P5 · P6

### 8.2 Anthropic Responsible Scaling Policy

Book: rsp §Capability thresholds, §Risk Reports, §Frontier Safety Roadmap; bluedot-tais §Unit 3 §3.3

- ○ **AIS-8.2.A** Identify which RSP threshold or obligation a described result triggers — CBRN, AI R&D-4 affirmative misalignment-risk case, sabotage risk report (drill: map to framework).
  - EK: Crossing AI R&D-4 requires an affirmative case naming the most immediate misalignment risks and mitigations; models clearly beyond Opus 4.5 get sabotage risk reports. v2 tied ASL-3 deployment and security standards to thresholds; v3 (Feb 2026) rewrote the policy around Risk Reports and Roadmaps.
  - P5
- ○ **AIS-8.2.B** Explain the RSP's accountability machinery — Risk Reports with coverage dates and marked redactions, LTBT-requested external review, noncompliance reporting — and what each makes verifiable.
  - EK: v3.4: unredacted Risk Reports to ≥200 staff; multiple external reviewers may split sections if all are covered.
  - P5 · P6

### 8.3 OpenAI Preparedness Framework

Book: openai-pf §v2; bluedot-tais §Unit 3 §3.4

- ○ **AIS-8.3.A** Decide whether a described result reaches High or Critical in a tracked category and what is then required, and before when (drill: map to framework).
  - EK: Tracked: Bio/Chem, Cyber, AI Self-improvement. High: safeguards must sufficiently minimise risk before deployment. Critical: also during development. Thresholds are holistic calls; scalable evals carry only indicative thresholds.
  - P5
- ○ **AIS-8.3.B** Map a safeguard to the threat it answers — robustness, usage monitoring, trust-based access (malicious users) vs autonomy limits, value/instruction alignment, oversight, system architecture (misaligned model) (drill: classify).
  - EK: Misuse safeguards assume a benign model and a hostile user; misalignment safeguards assume the model itself may act against you.
  - P1 · P5
- ○ **AIS-8.3.C** Evaluate the marginal-risk clause: when it lets OpenAI relax safeguards and what it does to race dynamics.
  - EK: Allowed only if overall risk doesn't meaningfully rise, it is publicly acknowledged, and OpenAI stays more protective than the other developer.
  - P5 · P6

### 8.4 Google DeepMind Frontier Safety Framework

Book: gdm-fsf §v3: CCLs, TCLs, safety case reviews; bluedot-tais §Unit 3 §3.5

- ○ **AIS-8.4.A** Identify which CCL a described capability approaches and the FSF response — alert threshold, response plan, safety case review, internal-deployment scope (drill: map to framework).
  - EK: Early-warning evals fire alert thresholds before a CCL; reaching a CCL needs a safety case review before external launch, and for advanced ML R&D CCLs before large internal deployments too. v3 added a harmful-manipulation CCL; TCLs flag lesser risks sooner.
  - P5

### 8.5 Safety cases

Book: uk-aisi §Best practice: control safety case sketch; gdm-fsf §Safety case reviews; rsp §Affirmative misalignment-risk case

- ○ **AIS-8.5.A** Structure a safety case as claims, arguments and evidence, and classify its argument as inability, control or trustworthiness (drill: classify).
  - EK: Inability: the model can't. Control: it can't cause harm even if it tries, given the protocol. Trustworthiness: it won't.
  - P1 · P5
- ○ **AIS-8.5.B** Find the weakest premise in a described safety case (drill: spot the flaw).
  - EK: A case is as strong as its least-supported premise; inability arguments rest on elicitation, control arguments on red-team strength, trustworthiness arguments on evidence we mostly don't have yet.
  - Needs: AIS-5.4.A
  - P3 · P6

## Unit 9 · Regulation, standards, compute and coordination

Big ideas: INC, DEF

### 9.1 EU AI Act — general-purpose AI

Book: eu-aia §Art 51, §Art 53, §Art 55, §GPAI Code of Practice

- ○ **AIS-9.1.A** Decide from training compute whether a model is GPAI and whether it is presumed to carry systemic risk (drill: compute).
  - EK: Indicative GPAI criterion: > 10²³ FLOP and generates language. Systemic risk presumed above 10²⁵ FLOP (under review); the Commission can also designate.
  - Needs: AIS-1.2.A
  - P4 · P5
- ○ **AIS-9.1.B** Identify which GPAI obligation a described provider has missed, separating all-provider duties from systemic-risk duties (drill: map to framework).
  - EK: All providers: technical documentation, information for downstream providers, copyright policy, public training-content summary. Systemic risk: notify the Commission, evaluate incl. adversarial testing, assess and mitigate risk, report serious incidents, ensure cybersecurity.
  - P5
- ○ **AIS-9.1.C** State the GPAI timeline, the open-source carve-out, and the role of the Code of Practice.
  - EK: Obligations apply from 2 Aug 2025; Commission enforcement from 2 Aug 2026; models placed earlier comply by 2 Aug 2027. Free open-source models skip some documentation duties unless systemic-risk. The Code (Transparency, Copyright, Safety & Security) is a voluntary route to show compliance.
  - P5

### 9.2 NIST AI RMF and standards

Book: nist-rmf §AI RMF 1.0 Core, §AI 600-1

- ○ **AIS-9.2.A** Sort described risk-management activities into Govern, Map, Measure and Manage (drill: classify).
  - EK: Govern: culture, roles, policy (cuts across). Map: context and risks of a use. Measure: assess and track. Manage: prioritise, act, monitor over time.
  - P5
- ○ **AIS-9.2.B** Map a Generative AI Profile risk (e.g. CBRN information or capabilities, confabulation, information security) to the Measure actions an eval team would own, and explain how voluntary standards become binding.
  - EK: AI 600-1 lists 12 GAI risks with actions keyed to the four functions. Standards bind through procurement, contracts and, in the EU, harmonised standards that give a presumption of conformity.
  - P5

### 9.3 Compute governance

Book: bluedot-gov §Unit 2; bluedot-agi §Unit 2 §2.1; eu-aia §Art 51

- ○ **AIS-9.3.A** Explain why compute is a governance lever — detectable, excludable, quantifiable, with a concentrated supply chain — and list the tools it enables (export controls, cloud KYC, reporting thresholds, on-chip mechanisms).
  - EK: A handful of firms control fabrication, lithography and leading chips; frontier runs need clusters visible to the cloud providers that host them.
  - P6
- ○ **AIS-9.3.B** Estimate a run's training compute from cluster size, chip throughput, utilisation and duration, and compare it to regulatory thresholds (drill: compute).
  - EK: C = N_chips × FLOP/s × MFU × seconds; 10⁴ chips × 10¹⁵ FLOP/s × 0.4 × 90 days ≈ 3 × 10²⁵ FLOP.
  - Needs: AIS-1.2.A
  - P4 · P5
- ○ **AIS-9.3.C** Evaluate the weaknesses of fixed compute thresholds: algorithmic efficiency, post-training and inference compute, distillation.
  - EK: A fixed FLOP line falls behind as efficiency improves 2–6×/yr; capability can be reached below it, or added after pretraining.
  - Needs: AIS-1.2.D
  - P6

### 9.4 International coordination and the evidence dilemma

Book: bluedot-gov §Unit 2, §Unit 3; bluedot-agi §Unit 1 §1.3; iasr-2026 §§Evidence dilemma, §§Risk management; uk-aisi §Pre-deployment testing

- ○ **AIS-9.4.A** Identify the coordination problem in a described scenario — race to the bottom, verification gap, free-riding, non-credible commitment (drill: classify).
  - EK: Without verification, mutual restraint is unstable: each side fears the other defects.
  - P1 · P6
- ○ **AIS-9.4.B** Trace the summit-and-institute track — Bletchley 2023, Seoul commitments 2024, Paris 2025, India 2026; the AISI/CAISI network; the International AI Safety Report — and what each actually produced.
  - EK: Seoul: companies committed to publish safety frameworks. Institutes test pre-deployment under voluntary agreements, can't block release, and publish findings unevenly (UK AISI more, CAISI less).
  - P5
- ○ **AIS-9.4.C** Explain the evidence dilemma and how if-then commitments and transparency requirements respond to it.
  - EK: IASR 2026: evidence about risk arrives slower than capability; acting early risks bad policy, waiting risks exposure. If-then rules commit now to act on evidence later.
  - P6

### 9.5 Institutions, power and contested questions

Book: bluedot-gov §Unit 2, §Unit 4, §Unit 5; bluedot-agi §Unit 3 §3.3; iasr-2026 §§Open-weight models

- ○ **AIS-9.5.A** Map who can act on a given frontier-AI decision — labs, compute providers, governments, standards bodies, investors — and where each depends on the others.
  - EK: Leverage sits at chokepoints: chips, cloud, capital, talent, market access; policy windows open when one of them shifts.
  - P6
- ○ **AIS-9.5.B** Argue both sides of the open-weights question using marginal risk, irreversibility and the closed–open capability gap, and name your crux.
  - EK: Open models trail the closed frontier by under a year (IASR) / 4–8 months (AISI); benefits to research and access; safeguards removable, weights unrecallable.
  - P6

## Unit 10 · Strategy and forecasting

Big ideas: SCALE, INC

### 10.1 Drivers and timelines

Book: bluedot-agi §Unit 2 §2.1, §Unit 2 §2.2; iasr-2026 §§Capabilities

- ○ **AIS-10.1.A** Build a simple timeline forecast from compute growth, algorithmic progress and a benchmark trend, and name the bottleneck most likely to break it (drill: compute).
  - EK: IASR 2026 bottlenecks: data, chips, capital, energy. Capability is 'jagged' — strong on some hard tasks, weak on some easy ones — so one trend line rarely means 'AGI'.
  - Needs: AIS-1.2.D, AIS-6.3.A
  - P4 · P6
- ○ **AIS-10.1.B** Make probabilistic forecasts on AI questions and score them with the Brier score (drill: compute).
  - EK: Brier = mean (p − o)²; 0 is perfect, 0.25 is always saying 50 %.
  - P4

### 10.2 Takeoff and AI R&D automation

Book: bluedot-agi §Unit 2 §2.3; bluedot-gov §Unit 4; openai-pf §AI Self-improvement; rsp §AI R&D thresholds; gdm-fsf §ML R&D CCLs

- ○ **AIS-10.2.A** Explain the AI-R&D feedback loop behind fast takeoff, what limits it, and why AI R&D thresholds are the frameworks' early warning for it.
  - EK: If AI multiplies research output, progress compounds (software intelligence explosion), limited by experiment compute. PF Critical: generational gains in 1/5 the 2024 time; RSP AI R&D-4; FSF ML R&D CCLs extend reviews to internal deployment.
  - P2 · P5

### 10.3 Threat models, strategies and prioritisation

Book: bluedot-agi §Unit 3, §Unit 4, §Unit 5; bluedot-tais §Unit 1 §1.3, §Unit 6 §6.2; bluedot-gov §Unit 3, §Unit 4, §Unit 6; iasr-2026 §§Risks

- ○ **AIS-10.3.A** Classify a described scenario as misuse, malfunction/loss of control or systemic risk, and name the mitigation layer that does most against it (drill: classify).
  - EK: IASR 2026 taxonomy: malicious use (content, influence, cyber, bio/chem); malfunctions (reliability, loss of control); systemic (labour, autonomy).
  - P1 · P2
- ○ **AIS-10.3.B** Compare loss-of-control, misuse and power-concentration threat models on what drives their likelihood and which interventions help each.
  - EK: Misuse: access and uplift → safeguards, security. Loss of control: misalignment + autonomy → alignment, control. Power concentration: AI replacing the cooperation that checks power → governance, distribution.
  - P2 · P6
- ○ **AIS-10.3.C** Compare strategies for the transition — safe-lead racing, coordinated pause, defensive acceleration, frameworks-plus-regulation — by their assumptions and failure modes, and stress-test one against accelerating capability and competition.
  - EK: Each strategy bets on something: verification, a lead, defence outpacing offence, or institutions keeping pace.
  - P6
- ○ **AIS-10.3.D** Prioritise safety interventions by importance, tractability and neglectedness and your comparative advantage, and state a theory of change with its crux.
  - EK: Theory of change: action → intermediate outcome → risk reduction. A crux is a belief whose change would flip the decision.
  - P6

## Unit 11 · Mechanistic interpretability, deeper (extension)

Big ideas: OBS

### 11.1 Attention circuits and attribution

Book: arena §Ch 1

- ○ **AIS-11.1.A** Split an attention head into its QK and OV circuits and say what each decides.
  - EK: W_QK = W_Qᵀ W_K decides where to attend; W_OV = W_V W_O decides what gets moved.
  - Needs: AIS-4.3.A
  - P1
- ○ **AIS-11.1.B** Compute a component's direct logit attribution for a correct-vs-wrong token pair (drill: compute).
  - EK: DLA = (component output, scaled by the final LayerNorm) · (W_U[:, correct] − W_U[:, wrong]).
  - P4

## Unit 12 · Agentic and multi-agent risk (extension)

Big ideas: DEF, OBS

### 12.1 Securing tool-using agents

Book: iasr-2026 §§Risks: malfunctions; openai-pf §Research categories: Long-range Autonomy, ARA; uk-aisi §Best practice: multi-agent control

- ○ **AIS-12.1.A** Identify the prompt-injection pathways in a described agent deployment and the least-privilege or containment control for each (drill: classify).
  - EK: Untrusted data in the context is an instruction channel; limit tools, permissions and egress so a hijacked agent can do little.
  - P1 · P2
- ○ **AIS-12.1.B** Explain why per-instance monitors miss distributed attacks across many agent instances.
  - EK: Each instance's actions can look benign; the harm lies in the combination, so monitoring must aggregate across instances.
  - Needs: AIS-7.1.A
  - P2
