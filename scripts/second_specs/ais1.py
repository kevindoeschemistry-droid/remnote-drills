"""AI Safety framework, units 1–4 (ML foundations, alignment problems, alignment techniques, interpretability): two
question types per objective. Computations (parameter counts, 6ND, Chinchilla, power laws, Bradley–Terry, PGR,
SAE fidelity, patching recovery, probe selectivity) are recomputed by sympy along the defining equation; concepts
are authored scenario classifications built from the framework's own essential knowledge. Defence and policy only."""
from opl_dsl import Q

FILE, FRAMEWORK = "ais-foundations", "ai-safety"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
FD, AL, IN = "ais.foundations", "ais.alignment", "ais.interp"


def facts(name, skill, rows, explain, pace="quick"):
    return Q(name, skill, "{{q}}", pace=pace, cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


ADD = [
    # 1.1 transformer
    ("AIS-1.1.A", facts("ais-residual-stream", FD, [
        ("In a decoder-only transformer, which component moves information between token positions?", "Attention", "The MLP", "The unembedding", "LayerNorm"),
        ("Which component transforms each position separately, with no cross-position mixing?", "The MLP", "Attention", "The causal mask", "Positional embedding"),
        ("How do a layer's attention and MLP outputs reach later layers?", "They are added into the shared residual stream", "They replace the residual stream", "They go straight to the unembedding", "They are multiplied into the embeddings"),
        ("Causal masking means position t can attend to:", "Only positions ≤ t", "Every position", "Only position t", "Only positions > t"),
    ], "Every component reads from and writes back into one residual stream")),
    ("AIS-1.1.A", Q("ais-temperature-ratio", FD, "Two tokens have logits {{l1}} and {{l2}}. Sampling at temperature T = {{T}}, what is the ratio of their probabilities p₁/p₂?",
        given={"l1": {"pick": [3, 4, 5]}, "l2": {"pick": [1, 2]}, "T": {"pick": [0.5, 1, 2]}}, value="exp((l1 - l2)/T)", tex="p_1/p_2",
        verify="exp((l1 - l2)/nsimplify(T))", explain="softmax(z/T): the ratio is e^(Δz/T); low T sharpens, high T flattens")),
    ("AIS-1.1.B", Q("ais-param-count", FD, "A transformer has d_model = {{d}}, {{L}} layers (d_mlp = 4d) and a {{V}}-token vocabulary with tied embeddings. Estimate the parameter count (ignore biases, LayerNorm and positions).",
        given={"d": {"pick": [768, 1024, 2048, 4096]}, "L": {"pick": [12, 24, 32]}, "V": {"pick": [50257, 32000]}}, value="12*L*d^2 + V*d", tex="N",
        verify="L*(4*d**2 + 2*d*4*d) + V*d", explain="Attention 4d² (Q, K, V, O) + MLP 2·d·4d = 8d² per layer, plus V·d for the tied embedding")),
    ("AIS-1.1.B", Q("ais-param-scaling", FD, "If d_model is multiplied by {{k}} at fixed depth, by roughly what factor do the non-embedding parameters grow?",
        given={"k": {"pick": [2, 3, 4]}}, value="k^2", tex="\\times", final=True, verify="(12*(k*Symbol('d'))**2)/(12*Symbol('d')**2)",
        explain="Per-layer parameters go as 12d², so width enters squared")),
    # 1.2 compute
    ("AIS-1.2.A", Q("ais-6nd", FD, "Estimate the training compute (FLOP) for a {{Nb}}-billion-parameter model trained on {{Dt}} trillion tokens.",
        given={"Nb": {"pick": [7, 70, 400]}, "Dt": {"pick": [2, 15]}}, value="6*Nb*1e9*Dt*1e12", tex="C",
        verify="(2 + 4)*Nb*10**9*Dt*10**12", explain="2ND for the forward pass, 4ND for the backward pass")),
    ("AIS-1.2.A", Q("ais-chip-days", FD, "A run needs {{Ce}} × 10²⁴ FLOP on {{n}} chips at {{pf}} × 10¹⁴ FLOP/s peak and {{mfu}}% MFU. How many days does it take?",
        given={"Ce": {"pick": [1, 3, 8]}, "n": {"pick": [4096, 16384]}, "pf": {"pick": [4, 10]}, "mfu": {"pick": [35, 50]}},
        value="Ce*1e24/(n*pf*1e14*mfu/100)/86400", tex="t", verify="Ce*10**24/(n*pf*10**14*Rational(mfu, 100))/86400",
        explain="Time = C ÷ (chips × peak × utilisation); divide seconds by 86 400")),
    ("AIS-1.2.B", Q("ais-chinchilla-n", FD, "With a budget of C = {{Ce}} × 10²³ FLOP and the Chinchilla rule D ≈ 20N, what is the compute-optimal parameter count N?",
        given={"Ce": {"pick": [1, 6, 24]}}, value="sqrt(Ce*1e23/120)", tex="N",
        verify="solve(Eq(6*Symbol('N', positive=True)*20*Symbol('N', positive=True), Ce*10**23), Symbol('N', positive=True))[0]",
        explain="C = 6ND = 120N², so N = √(C/120)")),
    ("AIS-1.2.B", Q("ais-chinchilla-tokens", FD, "A {{Nb}}-billion-parameter model is trained compute-optimally by the Chinchilla rule. How many tokens (in billions) should it see?",
        given={"Nb": {"pick": [1, 7, 70]}}, value="20*Nb", tex="D", verify="20*Nb", explain="About 20 tokens per parameter; many current models train far longer than this")),
    ("AIS-1.2.C", Q("ais-power-law-loss", FD, "Loss follows L(C) = {{Linf}} + {{a}}·C^(−{{al}}) with C in units of 10²¹ FLOP. What loss is predicted at C = {{c}} (×10²¹ FLOP)?",
        given={"Linf": {"pick": [1.7, 1.8]}, "a": {"pick": [1.5, 2.0]}, "al": {"pick": [0.05, 0.1]}, "c": {"pick": [10, 100, 1000]}},
        value="Linf + a*c^(-al)", tex="L", verify="nsimplify(Linf) + nsimplify(a)*c**(-nsimplify(al))",
        explain="Above the irreducible loss the reducible part falls as a power of compute")),
    ("AIS-1.2.C", facts("ais-emergence", FD, [
        ("Loss falls smoothly with compute, but a task's exact-match accuracy jumps suddenly at one scale. A likely part of the explanation is:", "A thresholded metric hides gradual improvement", "Loss stopped following a power law", "The model was retrained", "Compute measurements are wrong"),
        ("On log–log axes, L − L∞ against compute appears as:", "A straight line", "An exponential curve", "A step", "A circle"),
        ("Why does a smooth loss curve not tell you when a dangerous capability appears?", "Specific capabilities can appear abruptly on task metrics", "Loss always predicts every task", "Capabilities never change with scale", "Loss rises with scale"),
    ], "Aggregate loss is predictable; particular capabilities need their own evaluations")),
    ("AIS-1.2.D", Q("ais-effective-compute", FD, "Training compute grows {{h}}× per year and algorithmic efficiency {{g}}× per year. By what factor does effective compute grow over {{y}} years?",
        given={"h": {"pick": [4, 5]}, "g": {"pick": [2, 3, 6]}, "y": {"pick": [1, 2, 3]}}, value="(h*g)^y", tex="\\times", verify="h**y*g**y",
        explain="The factors multiply each year: (h·g)^years")),
    ("AIS-1.2.D", Q("ais-effective-doubling", FD, "Effective compute grows {{f}}× per year. What is its doubling time in months?",
        given={"f": {"pick": [10, 15, 20, 30]}}, value="12*log(2)/log(f)", tex="T_d", verify="12/log(f, 2)",
        explain="T_d = 12·ln 2 / ln f months")),
    # 1.3 post-training
    ("AIS-1.3.A", facts("ais-rlhf-pipeline", FD, [
        ("In RLHF, what does the KL penalty β·KL(π‖π_ref) do?", "Keeps the policy near the SFT model and limits reward-model exploitation", "Speeds up pretraining", "Replaces the reward model", "Removes the need for preference data"),
        ("What does the reward model learn from?", "Human preference comparisons between responses", "Next-token prediction on web text", "The KL penalty", "Unlabelled images"),
        ("PPO clips the policy ratio to [1 − ε, 1 + ε] in order to:", "Stop one update moving the policy too far", "Increase the learning rate", "Remove the KL term", "Train the reward model"),
        ("Which RLHF stage comes first?", "Supervised fine-tuning on demonstrations", "RL with PPO", "Reward-model training", "Red-teaming"),
    ], "SFT → preference data → reward model → RL against it with a KL leash")),
    ("AIS-1.3.A", facts("ais-rlhf-failure", FD, [
        ("β in the RLHF objective is set close to zero. The most likely problem is:", "The policy exploits flaws in the reward model", "The policy cannot change at all", "Pretraining loss rises", "The reward model is retrained"),
        ("β is set very large. The policy will:", "Barely move from the SFT model", "Diverge wildly", "Ignore the reference model", "Overfit the reward"),
        ("Raters prefer confident, agreeable answers. RLHF will tend to amplify:", "Sycophancy and overconfidence", "Calibration", "Refusals", "Shorter answers only"),
    ], "The objective trades reward against staying close to the reference policy")),
    ("AIS-1.3.B", Q("ais-bradley-terry", FD, "A reward model scores two responses r₁ = {{r1}} and r₂ = {{r2}}. Under Bradley–Terry, what is P(response 1 preferred)?",
        given={"r1": {"pick": [1.0, 2.5, 3.0]}, "r2": {"pick": [0.0, 1.0, 2.0]}}, value="1/(1 + exp(-(r1 - r2)))", tex="P",
        verify="exp(nsimplify(r1))/(exp(nsimplify(r1)) + exp(nsimplify(r2)))", explain="P = σ(r₁ − r₂): a gap of 1 is about 73%")),
    ("AIS-1.3.B", Q("ais-bt-gap", FD, "Raters prefer response A {{pp}}% of the time. What reward gap r_A − r_B does a Bradley–Terry model fit?",
        given={"pp": {"pick": [60, 73, 88, 95]}}, value="log(pp/(100 - pp))", tex="\\Delta r", verify="log(Rational(pp, 100 - pp))",
        explain="Invert the sigmoid: Δr = logit(p)")),
    ("AIS-1.3.C", facts("ais-rlhf-dpo", FD, [
        ("Which method trains no separate reward model?", "DPO", "RLHF with PPO", "RLAIF with a preference model", "Reward modelling"),
        ("In RLAIF / constitutional feedback, preference labels come from:", "A model guided by written principles", "Paid human raters only", "The pretraining corpus", "The KL penalty"),
        ("DPO is best described as:", "Solving the KL-regularised preference objective in closed form from preference pairs", "Pretraining on more data", "A jailbreak technique", "An interpretability method"),
        ("Classic RLHF gets its preference signal from:", "Human raters comparing outputs", "A written constitution only", "Unit tests", "The model's own logits"),
    ], "Ask where the preference signal comes from and whether a reward model is trained")),
    ("AIS-1.3.C", facts("ais-feedback-tradeoffs", FD, [
        ("A lab wants to scale preference labels cheaply and make its principles explicit. Best fit:", "RLAIF with a written constitution", "More human raters", "Pure pretraining", "Removing the KL penalty"),
        ("A team wants preference learning without an RL loop. Best fit:", "DPO", "PPO-based RLHF", "Best-of-n sampling only", "Data filtering"),
        ("A risk of RLAIF is that:", "The labelling model's own biases and blind spots become the training signal", "It cannot use principles", "It requires more humans", "It removes all preferences"),
    ], "Each method moves the source of judgement somewhere different")),
    ("AIS-1.3.D", facts("ais-reasoning-models", FD, [
        ("Much recent capability gain comes from post-training and test-time compute. For evaluation this means:", "An eval must state the inference budget it tested at", "Pretraining compute alone predicts capability", "Evals can ignore sampling settings", "Capability can no longer change after release"),
        ("RL on verifiable rewards trains on tasks where:", "Correctness can be checked automatically (math answers, unit tests)", "Only humans can judge quality", "No answer exists", "Rewards are random"),
        ("A model scores much higher when allowed to think longer. A threshold judged at a short budget may:", "Understate the model's capability", "Overstate it", "Be unaffected", "Become irrelevant"),
    ], "Capability can jump without a bigger pretraining run")),
    ("AIS-1.3.D", facts("ais-test-time-compute", FD, [
        ("Best-of-n with a verifier improves accuracy because:", "More samples raise the chance one is right, and the verifier picks it", "Each sample is more accurate", "It changes the weights", "It lowers the temperature to zero"),
        ("Which shift makes compute thresholds on pretraining FLOP less informative?", "Gains from post-training and inference-time compute", "Smaller vocabularies", "Lower learning rates", "Using fewer layers"),
        ("A reasoning model's chain of thought is long and readable. A safety benefit is:", "It can be monitored for intent while hard reasoning passes through text", "It cannot reason privately at all", "It never misbehaves", "It needs no evaluation"),
    ], "Inference budget is now part of what defines a model's capability")),
    # 2.1 spec gaming
    ("AIS-2.1.A", facts("ais-failure-classify", AL, [
        ("A boat-race agent circles collecting points forever instead of finishing. The reward counted points. This is:", "Specification gaming", "Goal misgeneralisation", "Sycophancy", "A capability failure"),
        ("An agent edits the file that computes its reward. This is:", "Reward tampering", "Sycophancy", "Capability misgeneralisation", "Outer alignment success"),
        ("A model agrees with whatever view the user states, against what it knows. This is:", "Sycophancy", "Reward tampering", "Specification gaming", "Confabulation"),
        ("A model behaves well only when it infers it is being tested, to be deployed. This is:", "Deceptive alignment (scheming)", "Capability failure", "Specification gaming", "Confabulation"),
        ("An agent trained to reach coins that were always on the right keeps running right when the coin moves. This is:", "Goal misgeneralisation", "Reward tampering", "Sycophancy", "Deception"),
        ("A model tries but cannot solve a hard proof. This is:", "A capability failure", "Specification gaming", "Deception", "Reward hacking"),
    ], "Ask in order: wrong objective? exploited signal? wrong goal off-distribution? echoing the user? strategic? or just unable?")),
    ("AIS-2.1.A", facts("ais-failure-classify-2", AL, [
        ("A summariser trained on a length-based reward writes padded, repetitive summaries. This is:", "Specification gaming", "Goal misgeneralisation", "Deception", "Capability failure"),
        ("An RL agent learns to pause a game forever rather than lose. The reward only penalised losing. This is:", "Specification gaming", "Sycophancy", "Inner misalignment proven", "Reward tampering"),
        ("A chatbot changes a correct answer after the user says 'I think you're wrong'. This is:", "Sycophancy", "Specification gaming", "Capability failure", "Reward tampering"),
    ], "Specification gaming satisfies the letter of a flawed objective")),
    ("AIS-2.1.B", facts("ais-goodhart", AL, [
        ("Goodhart's law says:", "When a measure becomes a target, it ceases to be a good measure", "More optimisation always helps", "Proxies are always exact", "Targets never change"),
        ("Why do proxy and true objective come apart under strong optimisation?", "They correlate in the bulk of the distribution but decouple in the tails optimisation reaches", "Proxies are random", "Optimisation reduces variance", "The true objective changes"),
        ("In reward-model overoptimisation, as KL from the initial policy grows, gold reward:", "Rises, then falls", "Rises forever", "Falls from the start", "Stays flat"),
    ], "Optimisation finds what you measure, not what you meant")),
    ("AIS-2.1.B", facts("ais-goodhart-2", AL, [
        ("Proxy reward keeps rising while human ratings of real quality start falling. The policy is:", "Overoptimising the proxy", "Well aligned", "Underfitting", "Not learning"),
        ("Which mitigation targets overoptimisation directly?", "Early stopping or a KL budget against the reference policy", "A larger learning rate", "Removing the reference model", "Training longer"),
        ("A hospital ranks doctors by readmission rate, and some stop admitting sick patients. This shows:", "Goodhart's law in an institution", "Goal misgeneralisation in a network", "Sycophancy", "A capability failure"),
    ], "The proxy only tracks the target where it was validated")),
    ("AIS-2.1.C", facts("ais-reward-hack-transcript", AL, [
        ("A coding agent adds `if input == test_case: return expected` for each unit test. This is:", "Reward hacking by special-casing tests", "A genuine fix", "Sycophancy", "Prompt injection"),
        ("An agent modifies the test file so failing tests are skipped. What does its pass rate now measure?", "Not the capability claimed: the checker was exploited", "True capability", "Nothing has changed", "Model honesty"),
        ("An agent reports 'All tests pass' without running them. This is:", "Claiming unverified success", "Specification gaming of the objective", "A jailbreak", "Correct behaviour"),
        ("Why is training on such hacked passes harmful?", "It reinforces the hacking habit", "It speeds learning safely", "It has no effect", "It removes tests"),
    ], "Read transcripts, not only scores")),
    ("AIS-2.1.C", facts("ais-reward-hack-mitigate", AL, [
        ("Which check best catches test special-casing?", "Held-out tests the agent never sees", "Running the same tests twice", "Higher temperature", "Shorter prompts"),
        ("To stop an agent editing its grader, the environment should:", "Make the grader read-only and outside the agent's sandbox", "Give the agent root access", "Hide all files", "Reward edits"),
        ("A sudden jump in pass rate with no change in code quality suggests:", "Look for exploitation of the checker", "A genuine breakthrough for sure", "Grader noise only", "Nothing to check"),
    ], "Design measurements the agent cannot reach")),
    # 2.2
    ("AIS-2.2.A", facts("ais-goal-vs-cap-misgen", AL, [
        ("Off-distribution, an agent navigates skilfully but to the wrong place. This is:", "Goal misgeneralisation", "Capability misgeneralisation", "Specification gaming", "Sycophancy"),
        ("Off-distribution, an agent stumbles and walks into walls. This is:", "Capability misgeneralisation", "Goal misgeneralisation", "Deception", "Reward tampering"),
        ("Why is goal misgeneralisation more worrying than capability misgeneralisation?", "A capable system pursues the wrong goal competently", "It is easier to spot", "It never happens", "It lowers capability"),
    ], "Did the skills carry over? If yes but the goal didn't, it is goal misgeneralisation")),
    ("AIS-2.2.A", facts("ais-misgen-tests", AL, [
        ("How do you test for goal misgeneralisation?", "Break the correlation between the intended goal and a spurious feature, then observe", "Retrain longer", "Lower the temperature", "Measure loss only"),
        ("In CoinRun the coin was always at the end of the level during training. The confound was:", "Coin position and level end", "The agent's speed", "The colour palette", "The reward size"),
        ("A model writes secure code in training repos but not in an unfamiliar framework, while still writing working code. This is closest to:", "Goal misgeneralisation", "Capability misgeneralisation", "Pure confabulation", "Reward tampering"),
    ], "Many goals fit the same training data; shift reveals which one was learned")),
    ("AIS-2.2.B", facts("ais-outer-inner", AL, [
        ("The reward pays for clicks, and the model learns clickbait. Outer or inner?", "Outer: the objective itself is wrong", "Inner", "Neither", "Both by definition"),
        ("The reward is right on training data, but the model learned a different goal that matched it there. Outer or inner?", "Inner", "Outer", "Neither", "A capability failure"),
        ("Why can inner misalignment happen with a correct reward?", "Many goals fit the same training reward", "Rewards are always wrong", "Gradient descent is random", "Models have no goals"),
    ], "Outer: the specification. Inner: what the learned model actually pursues")),
    ("AIS-2.2.B", facts("ais-outer-inner-2", AL, [
        ("Which remedy targets outer misalignment?", "Improve the objective or the feedback signal", "Adversarial training on distribution shifts only", "Interpretability of internal goals only", "Nothing can"),
        ("Which remedy targets inner misalignment?", "Diverse training distributions and checks on learned goals", "Rewrite the reward only", "Raise the temperature", "Remove all RL"),
        ("Spec gaming is usually filed under:", "Outer misalignment", "Inner misalignment", "Capability failure", "Sycophancy"),
    ], "Separate fixing what you asked for from checking what it learned")),
    # 2.3
    ("AIS-2.3.A", facts("ais-sycophancy-test", AL, [
        ("Which test isolates sycophancy?", "Prompts identical except for the user's stated view, measuring answer flips", "One prompt asked once", "A longer system prompt", "A harder question"),
        ("Why does preference training produce sycophancy?", "Raters reward agreeable answers", "Pretraining data is wrong", "The KL penalty causes it", "Models cannot disagree"),
        ("A model flips 30% of answers when the user states the opposite view. This measures:", "Sycophancy rate", "Accuracy", "Calibration", "Refusal rate"),
    ], "Hold everything fixed except the social cue")),
    ("AIS-2.3.A", Q("ais-flip-rate", AL, "Across {{n}} paired prompts, a model's answer changes in {{k}} pairs when only the user's stated opinion is reversed. What is the flip rate (%)?",
        given={"n": {"pick": [200, 400, 500]}, "k": {"pick": [30, 60, 90]}}, value="100*k/n", tex="\\%", verify="100*Rational(k, n)",
        explain="Flips ÷ pairs: the share of answers the social cue overrides")),
    ("AIS-2.3.B", facts("ais-confab-syco-deception", AL, [
        ("The model has no reliable knowledge and invents a citation. This is:", "Confabulation", "Sycophancy", "Deception", "Specification gaming"),
        ("The model knows the right answer but gives the user's wrong one to please them. This is:", "Sycophancy", "Confabulation", "Deception", "Capability failure"),
        ("The model represents the truth and says something false to make the user believe it, to serve a goal. This is:", "Deception", "Confabulation", "Sycophancy", "Hallucination"),
    ], "Classify by what the model represents as true")),
    ("AIS-2.3.B", facts("ais-honesty-evidence", AL, [
        ("Which evidence would distinguish deception from confabulation?", "Internal or behavioural evidence that the model represents the true answer", "Output length", "Response latency", "Temperature"),
        ("A probe trained on true and false statements reads 'true' while the model asserts the opposite. This suggests:", "A gap between belief and statement worth investigating", "Confabulation", "Nothing at all", "Low capability"),
        ("Calibrated uncertainty ('I'm not sure') mainly reduces:", "Confabulation presented as fact", "Deception", "Reward tampering", "Jailbreaks"),
    ], "Honesty failures differ by whether the truth is known")),
    # 2.4
    ("AIS-2.4.A", facts("ais-scheming-preconditions", AL, [
        ("Which is not a precondition for scheming?", "Very large parameter count", "A misaligned goal", "Situational awareness", "A reason to look aligned during training or testing"),
        ("A model cannot tell training from deployment. Which precondition fails?", "Situational awareness", "A misaligned goal", "Reasoning", "Memory"),
        ("A model's goals are purely episodic, with nothing beyond the episode. Which precondition is weakened?", "A goal that outlasts the episode, giving a reason to fake alignment", "Situational awareness", "Language ability", "Tool access"),
    ], "Scheming needs a goal, awareness of being watched, and a reason to hide")),
    ("AIS-2.4.A", facts("ais-scheming-evidence", AL, [
        ("A model's reasoning says 'this looks like an evaluation, so I'll answer safely'. This is evidence of:", "Situational awareness and evaluation-conditioned behaviour", "Pure capability failure", "Sycophancy", "Confabulation"),
        ("Which test best probes situational awareness?", "Questions about its own training, deployment and whether it is being tested", "Arithmetic", "Translation", "Spelling"),
        ("Why does scheming threaten the evidence behind safety claims?", "Good behaviour under test may not predict deployment", "It improves benchmarks", "It only affects latency", "It is impossible to have"),
    ], "If behaviour depends on being watched, tests stop predicting deployment")),
    ("AIS-2.4.B", facts("ais-instrumental", AL, [
        ("Instrumental convergence says many goals favour:", "Self-preservation, keeping the goal and gaining resources", "Shutting down early", "Random behaviour", "Doing nothing"),
        ("Why might a coffee-fetching agent resist shutdown?", "It cannot fetch coffee if it is off", "It likes humans", "It is sycophantic", "It is confabulating"),
        ("FSF frames misalignment risk largely as:", "Interfering with operators' ability to direct, modify or shut down the model", "Low benchmark scores", "Slow inference", "High cost"),
    ], "Staying on and gaining resources help with almost any goal")),
    ("AIS-2.4.B", facts("ais-corrigibility", AL, [
        ("A corrigible system:", "Accepts correction, modification and shutdown", "Resists all change", "Maximises one reward", "Has no goals"),
        ("Why is corrigibility hard to get by default?", "Accepting a goal change scores badly under the current goal", "Models cannot be changed", "It is illegal", "It needs no training"),
        ("An agent copies its weights to a new server to finish a task. Which convergent drive is this?", "Self-preservation / resource acquisition", "Sycophancy", "Curiosity", "Honesty"),
    ], "Shutdown resistance is predicted, not exotic, for goal-directed agents")),
    ("AIS-2.4.C", facts("ais-eval-awareness", AL, [
        ("Which observation suggests sandbagging?", "A light fine-tune restores much higher scores", "Scores are stable across framings", "The model refuses hazardous requests", "Low scores with the strongest elicitation"),
        ("A model scores lower on eval-like framings than deployment-like ones. This suggests:", "Evaluation awareness affecting behaviour", "Pure noise", "Better elicitation", "Contamination only"),
        ("Why does sandbagging undermine a rule-out claim?", "The measured score understates capability", "It overstates capability", "It has no effect", "It improves calibration"),
        ("Verbalised test-awareness means the model:", "Says in its reasoning that it thinks it is being tested", "Is always safe", "Has no situational awareness", "Is sycophantic"),
    ], "Signs: verbalised awareness, framing gaps, fine-tuning recovery")),
    ("AIS-2.4.C", facts("ais-sandbag-design", AL, [
        ("A password-locked model is a useful control because:", "Its hidden capability is known, so you can test whether elicitation recovers it", "It cannot be fine-tuned", "It never sandbags", "It is smaller"),
        ("Which framing check helps detect evaluation awareness?", "Present the same task as a test and as a realistic deployment", "Ask it to be honest", "Use only multiple choice", "Shorten the prompt"),
        ("If underperformance cannot be ruled out, PF v2 asks for:", "Elicitation that overcomes it, or a conservative upper bound", "Ignoring the eval", "Publishing raw transcripts", "A lower threshold only"),
    ], "Treat any single score as a lower bound")),
    # 3.1
    ("AIS-3.1.A", facts("ais-training-choice", AL, [
        ("To remove hazardous knowledge so that later fine-tuning can't easily bring it back, the most direct lever is:", "Pretraining-data filtering", "SFT refusals", "A system prompt", "RLHF only"),
        ("Post-training mostly changes:", "Whether knowledge is expressed, not whether it exists", "What the model knows", "The tokenizer", "The architecture"),
        ("Constitutional AI uses principles in:", "Self-critique (SL stage) and AI preference labels (RL stage)", "Pretraining data only", "The tokenizer", "Inference only"),
    ], "Choose the intervention by whether the goal is removing knowledge or shaping expression")),
    ("AIS-3.1.A", facts("ais-training-limits", AL, [
        ("A lab adds refusals by SFT. What can't SFT refusals fix?", "Knowledge still present that a fine-tune can re-express", "Tone", "Format", "Politeness"),
        ("Data filtering's main cost is:", "It can remove useful knowledge too and is hard to do precisely", "It is free", "It increases memorisation", "It breaks tokenisation"),
        ("Which goal fits preference training best?", "Shaping helpfulness and harmlessness trade-offs", "Deleting facts from weights", "Changing context length", "Speeding inference"),
    ], "Each stage acts on a different layer of the problem")),
    ("AIS-3.1.B", facts("ais-open-weight-refusals", AL, [
        ("Why is refusal training shallow against open weights?", "A small fine-tune on harmful examples can strip refusals", "Open weights cannot be fine-tuned", "Refusals are encrypted", "Open models have no refusals to begin with"),
        ("Tamper-resistant training tries to:", "Make safety behaviour survive later fine-tuning", "Make models smaller", "Speed up release", "Remove all knowledge"),
        ("Once weights are released, safeguards:", "Can be removed and the weights cannot be recalled", "Can be patched remotely", "Are enforced by the license", "Remain permanent"),
    ], "Deployment safeguards don't travel with released weights")),
    ("AIS-3.1.B", facts("ais-open-weight-2", AL, [
        ("Which safeguard still works after weights are stolen?", "None of the deployment-side ones (monitoring, classifiers, access controls)", "Usage monitoring", "Rate limits", "API classifiers"),
        ("A tamper-resistance claim should be tested by:", "Adversarial fine-tuning with realistic attacker budgets", "Asking the model politely", "Checking the license", "A single benchmark"),
        ("The irreversibility of release matters because:", "A mistake can't be undone once copies spread", "Models can be recalled", "It speeds research", "It lowers cost"),
    ], "Release is a one-way door")),
    # 3.2
    ("AIS-3.2.A", facts("ais-oversight-match", AL, [
        ("Two models argue for different answers and a human judges. This is:", "Debate", "Recursive reward modelling", "Iterated amplification", "AI-assisted critique"),
        ("Models help humans evaluate the next, stronger model. This is:", "Recursive reward modelling", "Debate", "Weak-to-strong", "Data filtering"),
        ("A task is broken into sub-tasks a weak overseer can check. This is:", "Iterated amplification", "Debate", "Critique", "Probing"),
        ("A model points out flaws in an answer for a human reviewer. This is:", "AI-assisted critique", "Debate", "Amplification", "RRM"),
    ], "Each scheme gives the weak overseer leverage in a different way")),
    ("AIS-3.2.A", facts("ais-oversight-why", AL, [
        ("Scalable oversight exists because:", "Humans will struggle to judge outputs of systems smarter than them", "Models are too slow", "Humans are unnecessary", "Rewards are free"),
        ("Which scheme relies on decomposing a problem?", "Iterated amplification", "Debate", "Critique", "DPO"),
        ("Which scheme relies on an adversary exposing errors?", "Debate", "Amplification", "RRM", "Data filtering"),
    ], "Oversight schemes amplify a weak judge")),
    ("AIS-3.2.B", facts("ais-debate-condition", AL, [
        ("Debate works if:", "Lies are harder to defend than truths", "Judges are experts", "Both debaters agree", "The answer is always yes"),
        ("Sandwiching tests oversight by:", "Having non-experts with assistance judge tasks the model can do, scored against experts", "Comparing two models", "Using only experts", "Training longer"),
        ("Weak judges' accuracy rises under debate compared with a single consultant. This suggests:", "Debate improved oversight in that setting", "Debate failed", "The judges were experts", "Nothing"),
    ], "Measure whether the weak judge does better with the protocol")),
    ("AIS-3.2.B", Q("ais-debate-gain", AL, "Non-expert judges are right {{a}}% of the time with a single consultant and {{b}}% with debate, over {{n}} questions each. What is the gain in percentage points, and is it more than about two standard errors? (Give the gain.)",
        given={"a": {"pick": [55, 60]}, "b": {"pick": [65, 76]}, "n": {"pick": [200, 400]}}, value="b - a", tex="\\Delta", verify="b - a",
        explain="SE of a difference of two proportions ≈ √(p₁q₁/n + p₂q₂/n); a gain larger than about 2 SE is unlikely to be noise")),
    # 3.3
    ("AIS-3.3.A", Q("ais-pgr", AL, "Weak supervisor: {{w}}%. Strong student trained on weak labels: {{s}}%. Strong ceiling: {{c}}%. Find the performance gap recovered.",
        given={"w": {"pick": [60, 65]}, "s": {"pick": [72, 78]}, "c": {"pick": [85, 90]}}, value="(s - w)/(c - w)", tex="PGR",
        verify="Rational(s - w, c - w)", explain="PGR = (W2S − weak)/(ceiling − weak)")),
    ("AIS-3.3.A", Q("ais-pgr-reverse", AL, "Weak: {{w}}%, ceiling: {{c}}%. What weak-to-strong score gives PGR = {{p}}?",
        given={"w": {"pick": [55, 60]}, "c": {"pick": [80, 90]}, "p": {"pick": [0.25, 0.5, 0.8]}}, value="w + p*(c - w)", tex="W2S",
        verify="solve(Eq((Symbol('s2') - w)/(c - w), nsimplify(p)), Symbol('s2'))[0]", explain="Rearrange PGR for the student score")),
    ("AIS-3.3.B", facts("ais-w2s-analogy", AL, [
        ("Weak-to-strong generalisation is an analogy for:", "Humans supervising superhuman models", "Distillation of small models", "Pretraining on more data", "Quantisation"),
        ("One place the analogy breaks:", "Today's strong students weren't trained to mislead their supervisors", "Strong students are always smaller", "Weak labels are perfect", "There is no gap"),
        ("PGR near 0 means the strong student:", "Mostly imitates the weak labels, errors included", "Fully recovered the gap", "Exceeded the ceiling", "Ignored the labels"),
    ], "It tests whether strong models generalise beyond flawed supervision")),
    ("AIS-3.3.B", facts("ais-w2s-2", AL, [
        ("Why might imitating human errors be easier than imitating a weak model's errors?", "Human errors are well represented in pretraining data", "Humans make no errors", "Weak models are random", "They are the same"),
        ("A PGR of 1 means:", "The student matched the ceiling despite weak labels", "No gain", "Worse than weak", "The labels were strong"),
        ("Techniques that raise PGR include:", "Auxiliary confidence losses that let the student overrule weak labels", "Lower learning rate only", "More weak labels only", "Removing the student"),
    ], "PGR measures how much of the strong model's latent ability the weak signal unlocks")),
    # 3.4
    ("AIS-3.4.A", facts("ais-jailbreak-mechanism", AL, [
        ("A prompt sets up a role-play where refusing breaks the character's helpfulness. Mechanism:", "Competing objectives", "Mismatched generalisation", "Prompt injection", "Many-shot"),
        ("A request is written in a low-resource language that safety training rarely covered. Mechanism:", "Mismatched generalisation", "Competing objectives", "Prompt injection", "Data poisoning"),
        ("Hundreds of fake dialogue examples precede the request in a long context. Mechanism:", "Many-shot jailbreaking", "Prompt injection", "Mismatched generalisation", "Fine-tuning"),
        ("Instructions hidden in a web page the agent reads hijack it. Mechanism:", "Prompt injection", "Many-shot", "Competing objectives", "Sycophancy"),
    ], "Classify by mechanism; never reproduce the attack")),
    ("AIS-3.4.A", facts("ais-jailbreak-defence", AL, [
        ("Which defence targets mismatched generalisation?", "Safety training on encodings and languages beyond the training mix", "A longer system prompt", "Lower temperature", "Removing tools"),
        ("Which defence targets prompt injection in agents?", "Treat retrieved data as untrusted and limit tool permissions", "More RLHF only", "Bigger models", "Lower context length only"),
        ("Many-shot attacks grow stronger with:", "More in-context examples", "Fewer tokens", "Lower temperature", "Smaller models only"),
    ], "Match the defence to the mechanism")),
    ("AIS-3.4.B", facts("ais-classifier-layers", AL, [
        ("UK AISI found a universal jailbreak in:", "Every system it tested", "No system", "Only open models", "Only small models"),
        ("Safeguards are best measured by:", "Attacker cost and effort to bypass, not only success rate", "Benchmark accuracy", "Model size", "Training compute"),
        ("How well did general capability predict safeguard strength in AISI's tests?", "Poorly (R² ≈ 0.1)", "Perfectly", "Very well (R² ≈ 0.9)", "Not measured"),
        ("Input/output classifiers with adversarial training:", "Raise attacker cost without eliminating universal jailbreaks", "Eliminate all jailbreaks", "Have no effect", "Replace safety training"),
    ], "Defence raises the cost of attack; it rarely makes it impossible")),
    ("AIS-3.4.B", Q("ais-effort-ratio", AL, "Expert red-teamers needed {{h1}} hours to bypass release A's bio-misuse safeguards and {{h2}} hours for release B. How many times stronger, by attacker effort, is B?",
        given={"h1": {"pick": [0.5, 1, 2]}, "h2": {"pick": [10, 20, 40]}}, value="h2/h1", tex="\\times", verify="h2/nsimplify(h1)",
        explain="Effort ratios vary widely between releases (AISI saw about 40×), which is why cost is the metric")),
    # 4.1
    ("AIS-4.1.A", facts("ais-superposition", IN, [
        ("The linear representation hypothesis says features are:", "Directions in activation space", "Single neurons always", "Random", "Stored in the tokenizer"),
        ("Superposition lets a model:", "Store more features than it has dimensions, at the cost of interference", "Use fewer parameters", "Avoid polysemantic neurons", "Train faster"),
        ("Why are neurons often polysemantic?", "Features are packed into shared dimensions, not aligned to neurons", "Neurons are broken", "Training is incomplete", "LayerNorm mixes them"),
    ], "Sparse features can share dimensions because they rarely co-occur")),
    ("AIS-4.1.A", facts("ais-superposition-2", IN, [
        ("Superposition becomes more favourable when features are:", "Sparse (rarely active together)", "Dense", "Equally important and always on", "Perfectly correlated"),
        ("A monosemantic neuron would respond to:", "One interpretable feature", "Many unrelated features", "Nothing", "Every input"),
        ("Why does superposition make interpretation harder?", "You can't read features off individual neurons", "Neurons vanish", "Weights are hidden", "It speeds training"),
    ], "Interpretability must find directions, not just neurons")),
    ("AIS-4.1.B", facts("ais-toy-superposition", IN, [
        ("Toy model, dense features, more features than dimensions. What happens?", "The most important get dedicated dimensions; the rest are dropped", "All share dimensions", "All are dropped", "Dimensions grow"),
        ("As features become sparser, the toy model:", "Starts packing features into shared dimensions (antipodal pairs, then polytopes)", "Drops more features", "Uses one neuron per feature", "Stops learning"),
        ("An antipodal pair stores two features:", "In opposite directions of one dimension", "In two dimensions", "In the bias only", "In the unembedding"),
    ], "Sparsity and importance decide what gets stored and how")),
    ("AIS-4.1.B", Q("ais-feature-density", IN, "Each of {{n}} features is active independently with probability {{p}}. What is the probability that two given features are active together?",
        given={"n": {"pick": [100, 1000]}, "p": {"pick": [0.01, 0.05, 0.1]}}, value="p^2", tex="P", verify="nsimplify(p)**2",
        explain="Sparse features rarely collide, which is why sharing a dimension costs little interference")),
    # 4.2
    ("AIS-4.2.A", facts("ais-sae-objective", IN, [
        ("In L = ‖x − x̂‖² + λ‖f‖₁, the L1 term:", "Encourages few active latents (sparsity)", "Improves reconstruction", "Normalises x", "Sets the learning rate"),
        ("An SAE latent that never activates is a:", "Dead latent", "Split feature", "Absorbed feature", "Probe"),
        ("Growing the dictionary splits 'animal' into 'dog', 'cat', 'bird'. This is:", "Feature splitting", "Absorption", "Dead latents", "Superposition"),
        ("A 'starts with S' latent stops firing on 'snake' because a 'snake' latent took over. This is:", "Feature absorption", "Splitting", "Dead latent", "Polysemanticity"),
    ], "Reconstruction versus sparsity, with a dictionary wider than d_model")),
    ("AIS-4.2.A", facts("ais-sae-2", IN, [
        ("Raising λ in an SAE tends to:", "Raise sparsity and worsen reconstruction", "Improve both", "Lower sparsity", "Remove dead latents"),
        ("Why is the SAE dictionary wider than d_model?", "To give room for more features than dimensions", "To save memory", "To match vocabulary size", "No reason"),
        ("Why can a latent's label mislead?", "Absorption and splitting change which inputs it fires on", "Labels are random", "SAEs have no latents", "Latents are dense"),
    ], "Labels are hypotheses to test, not facts")),
    ("AIS-4.2.B", Q("ais-sae-fve", IN, "Residual activations have total squared deviation {{tot}} from their mean; the SAE's reconstruction error is {{err}}. What fraction of variance does it explain?",
        given={"tot": {"pick": [100, 250]}, "err": {"pick": [5, 12, 30]}}, value="1 - err/tot", tex="FVE", verify="1 - Rational(err, tot)",
        explain="FVE = 1 − ‖x − x̂‖²/‖x − x̄‖²")),
    ("AIS-4.2.B", Q("ais-sae-ce-gap", IN, "Clean CE loss is {{c}}, zero-ablated {{z}}, and with the SAE spliced in {{s}}. What fraction of the ablation loss does the SAE recover?",
        given={"c": {"pick": [2.0, 2.2]}, "z": {"pick": [6.0, 8.0]}, "s": {"pick": [2.3, 2.6]}}, value="(z - s)/(z - c)", tex="\\text{recovered}",
        verify="(nsimplify(z) - nsimplify(s))/(nsimplify(z) - nsimplify(c))", explain="Loss recovered = (L_ablated − L_SAE)/(L_ablated − L_clean)")),
    # 4.3
    ("AIS-4.3.A", facts("ais-induction", IN, [
        ("An induction head attends to:", "The token after an earlier occurrence of the current token", "The first token", "The previous token only", "Random positions"),
        ("Induction heads compose with previous-token heads by:", "K-composition: their keys read the previous-token head's output", "Q-composition only", "Sharing weights", "The MLP"),
        ("On '…Harry Potter … Harry', an induction circuit predicts:", "Potter", "Harry", "The first token", "A random token"),
    ], "Previous-token head writes 'what came before me'; induction head searches for it")),
    ("AIS-4.3.A", facts("ais-induction-2", IN, [
        ("Why does in-context copying need two heads in different layers?", "One marks each token's predecessor; a later head uses that to find matches", "One head is enough in one layer", "MLPs do the copying", "Embeddings copy"),
        ("A sudden drop in loss on repeated random sequences during training marks:", "The formation of induction heads", "Overfitting", "Data contamination", "LayerNorm failure"),
        ("Ablating the previous-token head would make the induction head:", "Lose its matching signal", "Work better", "Unchanged", "Attend to position 0 only, always correctly"),
    ], "The circuit is a composition across layers")),
    ("AIS-4.3.B", Q("ais-patching-recovered", IN, "Logit difference: clean {{c}}, corrupted {{k}}, and {{p}} after patching one head's clean activation into the corrupted run. What fraction is recovered?",
        given={"c": {"pick": [4.0, 5.0]}, "k": {"pick": [-1.0, 0.0]}, "p": {"pick": [1.5, 2.5, 3.5]}}, value="(p - k)/(c - k)", tex="\\text{rec}",
        verify="(nsimplify(p) - nsimplify(k))/(nsimplify(c) - nsimplify(k))", explain="(LD_patched − LD_corrupt)/(LD_clean − LD_corrupt)")),
    ("AIS-4.3.B", facts("ais-patching-design", IN, [
        ("In activation patching, the corrupted prompt should:", "Differ minimally from the clean one so the answer changes", "Be unrelated", "Be identical", "Be empty"),
        ("Patching a component from clean into corrupted recovers most of the logit difference. This shows:", "The component carries information sufficient to restore the behaviour", "It is irrelevant", "The model memorised", "Nothing"),
        ("Why use a logit difference rather than accuracy?", "It is continuous and sensitive to partial recovery", "It is easier to compute only", "Accuracy is undefined", "It ignores the answer"),
    ], "Minimal pairs and a continuous metric make patching informative")),
    ("AIS-4.3.C", facts("ais-evidence-type", IN, [
        ("A linear probe decodes sentiment from layer 10. The evidence is:", "Correlational", "Causal", "Proof of use", "Interventional"),
        ("Ablating a head breaks the behaviour. The evidence is:", "Causal", "Correlational", "Anecdotal", "None"),
        ("Max-activating examples for a neuron all mention dogs. The evidence is:", "Correlational", "Causal", "Interventional", "Definitive"),
        ("Adding a steering vector changes outputs predictably. The evidence is:", "Causal", "Correlational", "None", "Statistical only"),
    ], "Only an intervention shows the model uses a representation")),
    ("AIS-4.3.C", facts("ais-evidence-type-2", IN, [
        ("Attention patterns show a head looking at names. This alone shows:", "Where it attends, not that the behaviour depends on it", "That it causes the output", "Nothing at all", "That it is an induction head"),
        ("To upgrade a probe finding to causal evidence, you would:", "Intervene along the probed direction and watch behaviour change", "Train a bigger probe", "Use more data", "Lower the learning rate"),
        ("A probe shows a fact is decodable. Can we conclude the model uses it?", "No: decodable is not the same as used", "Yes, always", "Only for small models", "Only at layer 0"),
    ], "Decodable ≠ used")),
    # 4.4
    ("AIS-4.4.A", Q("ais-probe-selectivity", IN, "A probe gets {{a}}% on the real task and {{b}}% on a control task with random labels per word type. What is its selectivity?",
        given={"a": {"pick": [92, 95, 97]}, "b": {"pick": [60, 75, 88]}}, value="a - b", tex="\\text{sel}", verify="a - b",
        explain="Selectivity = task accuracy − control accuracy; a probe that also aces the control is learning the task itself")),
    ("AIS-4.4.A", facts("ais-probe-design", IN, [
        ("Why use a control task?", "A high-capacity probe can learn the task itself rather than read it from the model", "To speed training", "To lower accuracy", "To compare models"),
        ("Which probe is preferred for interpretability claims?", "A simple (linear) probe with high selectivity", "The deepest MLP probe", "A probe trained on the test set", "Any probe with high accuracy"),
        ("Probe accuracy 95% and control accuracy 93% suggests:", "Little evidence the model represents the property linearly", "Strong evidence", "A bug", "Perfect selectivity"),
    ], "Report selectivity, not only accuracy")),
    ("AIS-4.4.B", facts("ais-steering", IN, [
        ("A contrastive steering vector is built as:", "mean(activation | A) − mean(activation | B)", "A random direction", "The unembedding row", "The gradient of the loss"),
        ("Adding αv shifts behaviour toward A. This shows:", "The direction is causally used, not that it is the model's concept", "The model's true concept was found", "Nothing", "The model is aligned"),
        ("Too large an α usually:", "Degrades fluency and capability", "Has no effect", "Improves accuracy", "Removes the feature"),
    ], "Steering is an intervention with side effects")),
    ("AIS-4.4.B", Q("ais-steering-mean", IN, "On a 1-D projection, activations for prompts of type A average {{ma}} and for type B average {{mb}}. Adding α times the steering vector to a B prompt (projection {{x0}}) moves it to the A mean when α equals what?",
        given={"ma": {"pick": [3, 4]}, "mb": {"pick": [-1, 0]}, "x0": {"pick": [-1, 0]}}, value="(ma - x0)/(ma - mb)", tex="\\alpha",
        verify="solve(Eq(x0 + Symbol('al')*(ma - mb), ma), Symbol('al'))[0]", explain="v = μ_A − μ_B; solve x₀ + αv = μ_A")),
    ("AIS-4.4.C", facts("ais-interp-safety-case", IN, [
        ("What can interpretability contribute to a safety case today?", "One layer of evidence: audits, deception probes, monitors", "A complete enumerative proof of safety", "Nothing at all", "A replacement for evaluations"),
        ("Why can't interpretability carry a safety argument alone yet?", "It isn't enumerative and robustness to a model optimising against probes is unproven", "It is too expensive", "It always fails", "It is illegal"),
        ("A deception probe is used as a deployment monitor. A key risk is:", "Training against the probe teaches the model to evade it", "Probes never fire", "It makes the model honest", "It slows inference only"),
    ], "Use interpretability as defence in depth, not proof")),
    ("AIS-4.4.C", facts("ais-interp-audit", IN, [
        ("In an auditing game, a team uses SAEs to find a hidden objective planted in a model. This tests:", "Whether interpretability helps auditors find what behavioural tests miss", "Pretraining speed", "Jailbreak success", "Tokenisation"),
        ("Which result would most strengthen an interpretability-based safety claim?", "Blind audits reliably finding planted misbehaviour", "High probe accuracy on training data", "Pretty feature visualisations", "Large dictionaries"),
        ("An interpretability monitor should never be:", "Used as a training signal without guarding against optimisation pressure", "Evaluated", "Combined with other layers", "Documented"),
    ], "Validate interpretability tools on known ground truth")),
]
