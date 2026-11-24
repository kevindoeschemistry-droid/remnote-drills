"""AP Statistics 2026-27 depth (Nov 2026): the course framework's 150 learning objectives were read (CED effective fall
2026) and registered as items of `ap-statistics-2026`. EXISTING adds those codes to the objectives that already answer
them; OBJS are new objectives (written into statistics.yaml by scripts/insert_objs.py) for the rest, two types each.
Conceptual items (choose a procedure, check conditions, interpret) are authored; numbers are recomputed by sympy."""
from opl_dsl import Q

FILE, FRAMEWORK = "st-ap-depth", "statistics"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
A = lambda *c: [f"ap-statistics-2026:{x}" for x in c]


def facts(name, skill, rows, explain, pace="recall"):
    return Q(name, skill, "{{q}}", pace=pace, cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


EXISTING = {
    "SS-1.1.A": A("1.7.A", "1.7.B", "1.7.D", "1.7.E", "1.8.A"),
    "SS-1.1.B": A("1.9.D", "1.9.E", "2.11.C", "2.11.D", "2.11.E", "2.11.F"),
    "SS-1.2.A": A("1.12.A"),
    "SS-1.2.B": A("1.13.A", "1.13.B"),
    "SS-2.1.A": A("2.4.A", "2.5.A", "2.6.A", "2.7.A"),
    "SS-2.2.A": A("2.9.A"),
    "SS-2.2.B": A("2.10.B", "2.10.E"),
    "SS-2.2.C": A("3.2.A", "4.1.A"),
    "SS-3.1.A": A("3.3.C", "3.3.D", "3.4.C"),
    "SS-3.1.B": A("3.7.A", "3.7.B"),
    "SS-3.1.C": A("3.15.A", "3.15.B"),
    "SS-4.1.A": A("4.5.A"),
    "SS-5.1.A": A("5.2.A", "5.3.A", "5.4.A", "5.5.A", "5.5.B"),
}

OBJS = [
    ("SS-1.1.C", A("1.5.A", "1.6.A", "1.6.B", "1.7.F", "1.8.B", "1.9.A", "1.9.B", "1.9.C"),
     "Describe a distribution's shape and pick the centre and spread that suit it.", "Skewed right: mean > median; skewed or with outliers, report median and IQR; symmetric, mean and SD."),
    ("SS-1.1.D", A("1.7.C"), "Find summary statistics after a change of units.", "For y = a + bx: centre and position become a + b·(value); spread (SD, IQR, range) becomes |b|·(value)."),
    ("SS-1.1.E", A("1.2.A", "1.2.B", "1.2.C", "1.1.A"), "Classify variables and tell parameters from statistics.", "Categorical vs quantitative (discrete counts, continuous measures); a parameter describes a population, a statistic a sample."),
    ("SS-1.1.F", A("1.3.A", "1.3.B", "1.4.A", "1.4.B", "1.4.C"), "Summarise one categorical variable with relative frequencies and the right graph.", "Relative frequency = count ÷ total; bar charts compare categories; pie charts need parts of one whole."),
    ("SS-1.2.C", A("1.1.B", "1.10.A", "1.10.B", "1.10.C", "1.10.D", "1.10.E", "1.13.C", "1.13.D"), "Classify a study and state the scope of its conclusions.", "Random sampling lets results generalise to the population; random assignment lets them show cause; an observational study shows association only."),
    ("SS-1.2.D", A("1.11.A", "1.11.B"), "Identify a sampling method and judge when it fits.", "SRS, stratified (sample within groups), cluster (take whole groups), systematic (every kth), convenience."),
    ("SS-2.1.B", A("2.1.A", "2.1.B", "2.2.A", "2.2.B", "2.2.C"), "Read joint, marginal and conditional percentages from a two-way table and judge association.", "Conditional % = cell ÷ its row (or column) total; variables are associated when the conditional distributions differ."),
    ("SS-2.1.C", A("2.3.A", "2.10.D", "2.12.A"), "Estimate a probability from a simulation and design one.", "Estimated probability = successes ÷ trials; assign random digits in proportion to each outcome's probability."),
    ("SS-2.2.D", A("2.8.A", "2.9.B"), "Build a discrete probability distribution and interpret its mean.", "Probabilities lie in [0, 1] and sum to 1; the mean is the long-run average outcome."),
    ("SS-2.2.E", A("2.10.A", "2.10.C"), "Decide whether a setting is binomial and find P(at least one).", "Binary outcomes, independent trials, fixed n, same p; P(X ≥ 1) = 1 − (1 − p)ⁿ."),
    ("SS-2.2.F", A("3.2.B", "3.2.C", "4.1.B", "4.1.C", "3.9.B", "3.9.C", "4.6.B", "4.6.C"), "Check the conditions for a sampling distribution and describe its shape.", "10% condition (n ≤ N/10); large counts np, n(1 − p) ≥ 10; for means, normal population or n ≥ 30 (CLT)."),
    ("SS-2.2.G", A("3.1.A", "3.1.B"), "Tell biased from unbiased estimators and compute a point estimate.", "An estimator is unbiased when its sampling distribution is centred on the parameter; p̂ and x̄ are unbiased."),
    ("SS-2.2.H", A("2.11.A", "2.11.B"), "Describe a normal distribution and recover its mean and SD from facts about it.", "Symmetric, unimodal, mean = median; the inflection points sit one SD from the mean."),
    ("SS-3.1.D", A("3.3.A", "3.5.A", "3.10.A", "3.12.A", "3.14.B", "4.2.B", "4.4.A", "4.7.A", "4.9.A"), "Choose the inference procedure for a study.", "One or two groups; proportion or mean; paired or independent; one categorical variable vs two (goodness of fit, homogeneity, independence)."),
    ("SS-3.1.E", A("3.3.B", "3.5.B", "3.5.C", "3.10.B", "3.12.B", "3.12.C", "3.14.C", "3.14.D", "4.2.C", "4.4.B", "4.4.C", "4.7.B", "4.9.B", "4.9.C"), "State hypotheses about a parameter and check the conditions for the procedure.", "H₀ names a parameter value (or no difference); conditions are random, 10%, and large counts or normal/large sample."),
    ("SS-3.1.F", A("3.4.A", "3.4.B", "3.6.A", "3.11.A", "3.11.B", "3.13.B", "3.13.C", "3.15.C", "3.15.D", "4.3.A", "4.3.B", "4.5.B", "4.5.C", "4.8.A", "4.8.B", "4.10.B", "4.10.C"), "Interpret a p-value or a confidence interval and draw the conclusion.", "The p-value is the chance of a result this extreme if H₀ is true; reject H₀ when p < α; a value outside the interval is implausible."),
    ("SS-3.1.G", A("3.8.A", "3.8.B", "3.8.C", "3.8.D"), "Identify Type I and Type II errors and their probabilities.", "Type I rejects a true H₀ (probability α); Type II fails to reject a false H₀ (probability β = 1 − power)."),
    ("SS-3.1.H", A("3.9.A", "3.10.C", "3.10.D", "3.13.A"), "Find the standard error and interval for a difference of two proportions.", "SE = √(p̂₁(1 − p̂₁)/n₁ + p̂₂(1 − p̂₂)/n₂); interval = (p̂₁ − p̂₂) ± z*·SE."),
    ("SS-3.1.I", A("3.14.A"), "Find chi-square degrees of freedom and describe the distribution.", "Goodness of fit: k − 1; two-way table: (r − 1)(c − 1); chi-square is right-skewed, mean = df."),
    ("SS-4.1.B", A("4.2.A", "4.2.D", "4.2.E", "4.3.C"), "Compute a t interval's margin of error and see how n changes it.", "ME = t*·s/√n with df = n − 1; quadrupling n halves the margin."),
    ("SS-4.1.C", A("4.6.A", "4.7.C", "4.7.D", "4.10.A"), "Compute the standard error and t statistic for two independent means.", "SE = √(s₁²/n₁ + s₂²/n₂); t = (x̄₁ − x̄₂)/SE; conservative df = min(n₁, n₂) − 1."),
    ("SS-5.1.B", A("5.1.A", "5.1.B", "5.1.C", "5.4.B", "5.4.C"), "Describe a scatterplot and read residuals and residual plots.", "Direction, form, strength, unusual points; residual = y − ŷ; a curved residual plot says a line is the wrong model."),
]

DESC, SAMP, PROB, DIST, EV, INF, BIV = ("stats.descriptive", "stats.sampling", "stats.probability", "stats.distributions",
                                       "stats.expected-value", "stats.inference", "stats.bivariate")

ADD = [
    # 1.1.C shape and choice of summary
    ("SS-1.1.C", facts("st-shape-from-summary", DESC, [
        ("A distribution has mean 52 and median 41. What shape is most likely?", "Skewed right", "Skewed left", "Symmetric", "Uniform"),
        ("A distribution has mean 18 and median 23. What shape is most likely?", "Skewed left", "Skewed right", "Symmetric", "Bimodal"),
        ("Household incomes in a town are strongly skewed right. Which pair best describes centre and spread?", "Median and IQR", "Mean and SD", "Mean and range", "Mode and SD"),
        ("Test scores are roughly symmetric with no outliers. Which pair best describes centre and spread?", "Mean and SD", "Median and range", "Mode and IQR", "Maximum and minimum"),
    ], "The mean is pulled toward the long tail; resistant summaries (median, IQR) suit skewed data")),
    ("SS-1.1.C", Q("st-add-outlier", DESC, "A data set of {{n}} values has mean {{m}}. A value of {{big}} is added. What is the new mean?",
        given={"n": {"pick": [9, 19, 24]}, "m": {"pick": [40, 50, 62]}, "big": {"pick": [150, 300, 500]}}, value="(n*m + big)/(n + 1)", tex="\\bar x",
        verify="solve(Eq(x*(n + 1), n*m + big), x)[0]", explain="New mean = (old total + new value)/(n + 1); the median would barely move: the mean is not resistant")),
    # 1.1.D units
    ("SS-1.1.D", Q("st-units-mean", DESC, "Temperatures in °C have mean {{m}} and SD {{s}}. Converted to °F (F = 32 + 1.8C), what is the new {{what}}?",
        cases=[{"m": 20, "s": 5, "what": "mean", "w": 0}, {"m": 20, "s": 5, "what": "standard deviation", "w": 1}, {"m": 35, "s": 2.5, "what": "mean", "w": 0}, {"m": 12, "s": 4, "what": "standard deviation", "w": 1}],
        value="w == 0 ? 32 + 1.8*m : 1.8*s", tex="y", verify="[32 + Rational(9, 5)*nsimplify(m), Rational(9, 5)*nsimplify(s)][w]",
        explain="Adding a constant shifts centre but not spread; multiplying scales both")),
    ("SS-1.1.D", Q("st-units-iqr", DESC, "Lengths in inches have IQR {{q}} and median {{med}}. In centimetres (1 in = 2.54 cm), what is the new {{what}}?",
        cases=[{"q": 4, "med": 30, "what": "IQR", "w": 0}, {"q": 4, "med": 30, "what": "median", "w": 1}, {"q": 1.5, "med": 12, "what": "IQR", "w": 0}, {"q": 10, "med": 64, "what": "median", "w": 1}],
        value="w == 0 ? 2.54*q : 2.54*med", tex="y", verify="Rational(254, 100)*[nsimplify(q), nsimplify(med)][w]",
        explain="A change of units multiplies every value, so every measure of position and spread scales by the same factor")),
    # 1.1.E variables
    ("SS-1.1.E", facts("st-variable-type", DESC, [
        ("A survey records each student's blood type. What kind of variable?", "Categorical", "Quantitative discrete", "Quantitative continuous", "A parameter"),
        ("A study records the number of siblings each person has. What kind of variable?", "Quantitative discrete", "Quantitative continuous", "Categorical", "Ordinal only"),
        ("A study records each runner's 5 km time in seconds. What kind of variable?", "Quantitative continuous", "Quantitative discrete", "Categorical", "Identifier"),
        ("Zip codes are recorded for each customer. What kind of variable?", "Categorical (numbers used as labels)", "Quantitative continuous", "Quantitative discrete", "A statistic"),
    ], "Ask whether arithmetic on the values makes sense: if not, the variable is categorical")),
    ("SS-1.1.E", facts("st-param-statistic", SAMP, [
        ("A poll of 1 000 voters finds 46% support a measure. The 46% is a …", "Statistic", "Parameter", "Population", "Observational unit"),
        ("The mean height of all players registered in a league is 178 cm. That mean is a …", "Parameter", "Statistic", "Sample", "Variable"),
        ("In a study of 50 dogs' weights, what are the observational units?", "The dogs", "The weights", "The mean weight", "The 50"),
        ("Which symbol names a population proportion?", "p", "p̂", "x̄", "s"),
    ], "Parameters (μ, σ, p) describe populations; statistics (x̄, s, p̂) are computed from samples")),
    # 1.1.F categorical summary
    ("SS-1.1.F", Q("st-relative-frequency", DESC, "In a survey, {{a}} chose bus, {{b}} chose car and {{c}} chose bike. What percent chose {{which}}?",
        cases=[{"a": 45, "b": 90, "c": 15, "which": "bus", "k": 0}, {"a": 30, "b": 120, "c": 50, "which": "car", "k": 1}, {"a": 12, "b": 28, "c": 40, "which": "bike", "k": 2}, {"a": 60, "b": 75, "c": 15, "which": "bus", "k": 0}],
        value="100*(k == 0 ? a : (k == 1 ? b : c))/(a + b + c)", tex="\\%", verify="100*[a, b, c][k]/(a + b + c)",
        explain="Relative frequency = category count ÷ total; it lets groups of different sizes be compared")),
    ("SS-1.1.F", facts("st-categorical-graph", DESC, [
        ("Students pick their favourite of five sports and may pick only one. Which graph shows the parts of the whole?", "Pie chart or bar chart of relative frequencies", "Histogram", "Boxplot", "Scatterplot"),
        ("Respondents may tick several streaming services each. Why is a pie chart wrong?", "The percentages do not form one whole; they can exceed 100% in total", "Pie charts need numbers", "There are too few categories", "Bar charts cannot show percents"),
        ("Two schools of different sizes are compared on favourite subject. What should the bars show?", "Relative frequencies (percents) in each school", "Raw counts only", "Means", "Cumulative counts"),
        ("A bar chart's vertical axis starts at 40% instead of 0. What is the risk?", "Differences between bars look larger than they are", "Bars become wider", "The mode changes", "Nothing"),
    ], "Compare categories with relative frequencies; graph honestly from zero", pace="quick")),
    # 1.2.C study type and scope
    ("SS-1.2.C", facts("st-study-classify", SAMP, [
        ("Researchers randomly assign 200 volunteers to a new or old diet and compare weight loss. What is it?", "An experiment", "An observational study", "A census", "A sample survey"),
        ("A school records the GPA of every one of its students. What is it?", "A census", "A sample survey", "An experiment", "A simulation"),
        ("Records of 5 000 smokers and non-smokers are compared for lung disease. What is it?", "An observational study", "An experiment", "A census", "A randomized trial"),
        ("A random sample of 1 200 adults is asked how often they exercise. What is it?", "A sample survey (observational)", "An experiment", "A census", "A matched-pairs design"),
    ], "An experiment imposes a treatment; an observational study only records")),
    ("SS-1.2.C", facts("st-scope-inference", SAMP, [
        ("Volunteers are randomly assigned to two treatments. To whom do the results apply, and can they show cause?", "Only to people like the volunteers; yes, cause", "To the whole population; yes, cause", "To the whole population; no cause", "To no one"),
        ("A random sample of residents is surveyed, with no treatment imposed. What can be concluded?", "Generalise to the population; association only", "Cause and effect for everyone", "Cause for the sample only", "Nothing at all"),
        ("A random sample is drawn and then randomly assigned to treatments. What can be concluded?", "Cause and effect, generalised to the population", "Association only", "Cause for the sample only", "Nothing beyond the sample"),
        ("A convenience sample with no random assignment shows coffee drinkers sleep less. What can be concluded?", "Association in this sample only", "Coffee causes poor sleep", "All adults sleep less with coffee", "Sleep causes coffee drinking"),
    ], "Random selection buys generalisation; random assignment buys causation", pace="quick")),
    # 1.2.D sampling methods
    ("SS-1.2.D", facts("st-sampling-method", SAMP, [
        ("A principal randomly picks 20 students from each grade. Which method?", "Stratified random sample", "Cluster sample", "Systematic sample", "Simple random sample"),
        ("A district randomly picks 5 schools and surveys every teacher in them. Which method?", "Cluster sample", "Stratified random sample", "Convenience sample", "Systematic sample"),
        ("A store surveys every 25th customer after a random start. Which method?", "Systematic sample", "Cluster sample", "Stratified sample", "Voluntary response"),
        ("Why stratify by grade instead of taking an SRS?", "Estimates are more precise when the strata differ in the response", "It removes all bias", "It is always cheaper", "It avoids random selection"),
    ], "Strata: sample within every group; clusters: take whole randomly chosen groups")),
    ("SS-1.2.D", Q("st-systematic-interval", SAMP, "A list holds {{N}} names and a systematic sample of {{n}} is wanted. What sampling interval k should be used, and with a random start of {{st}}, what is the {{j}}th name chosen? Give the position of that name.",
        given={"N": {"pick": [1200, 2000, 5000]}, "n": {"pick": [50, 100]}, "st": {"pick": [3, 7, 11]}, "j": {"pick": [2, 5, 10]}},
        value="st + (j - 1)*N/n", tex="\\text{position}", final=True, verify="nsimplify(st) + (j - 1)*Rational(N, n)",
        explain="k = N/n; the chosen positions are start, start + k, start + 2k, …")),
    # 2.1.B two-way tables
    ("SS-2.1.B", Q("st-conditional-pct", PROB, "Of {{a}} seniors, {{b}} drive to school; of {{c}} juniors, {{d}} drive. What percent of {{who}} drive?",
        cases=[{"a": 120, "b": 72, "c": 150, "d": 45, "who": "seniors", "k": 0}, {"a": 120, "b": 72, "c": 150, "d": 45, "who": "juniors", "k": 1}, {"a": 80, "b": 20, "c": 200, "d": 30, "who": "juniors", "k": 1}, {"a": 250, "b": 100, "c": 100, "d": 60, "who": "all students", "k": 2}],
        value="k == 0 ? 100*b/a : (k == 1 ? 100*d/c : 100*(b + d)/(a + c))", tex="\\%", verify="100*[Rational(b, a), Rational(d, c), Rational(b + d, a + c)][k]",
        explain="A conditional percent divides by its own group's total; the marginal percent divides by the grand total")),
    ("SS-2.1.B", facts("st-association", PROB, [
        ("60% of seniors and 30% of juniors drive to school. Is driving associated with grade?", "Yes: the conditional distributions differ", "No: both groups have drivers", "Only if the sample is a census", "Cannot say without the means"),
        ("45% of men and 45% of women prefer tea. Are drink and sex associated in this table?", "No: the conditional distributions match", "Yes, strongly", "Yes, weakly", "Cannot tell from percents"),
        ("Which graph best compares conditional distributions of two categorical variables?", "Segmented (stacked) bar chart of percents", "Histogram", "Scatterplot", "Boxplot"),
        ("A table shows 900 urban and 100 rural respondents. Why compare percents, not counts?", "The groups have very different sizes", "Counts are always wrong", "Percents remove all bias", "Percents add to more than 100"),
    ], "Association means knowing one variable changes the distribution of the other", pace="quick")),
    # 2.1.C simulation
    ("SS-2.1.C", Q("st-sim-estimate", PROB, "In {{tr}} simulated trials, the event happened {{hits}} times. What is the estimated probability, as a decimal?",
        given={"tr": {"pick": [50, 100, 200, 500]}, "hits": {"pick": [7, 13, 21, 42]}}, value="hits/tr", tex="\\hat P", verify="Rational(hits, tr)",
        explain="The estimate is the relative frequency of the event across trials; more trials give a steadier estimate")),
    ("SS-2.1.C", facts("st-sim-design", PROB, [
        ("A player makes 70% of free throws. Which digit assignment simulates one shot?", "Digits 0–6 = make, 7–9 = miss", "Digits 0–7 = make, 8–9 = miss", "Even = make, odd = miss", "0 = make, 1–9 = miss"),
        ("To simulate a 25% chance with pairs of digits 00–99, which assignment works?", "00–24 = success, 25–99 = failure", "00–25 = success", "Pairs ending in 5 = success", "00–04 = success"),
        ("When simulating draws without replacement from 10 people using digits 0–9, what must you do with repeats?", "Skip a digit already chosen", "Count it again", "Stop the trial", "Add 10 to it"),
        ("Why run many simulated trials, not a few?", "The estimate's variability shrinks as trials increase", "Each trial becomes more accurate", "It removes bias in the model", "It changes the true probability"),
    ], "A simulation must model the right probabilities and repeat enough to settle down", pace="quick")),
    # 2.2.D distributions
    ("SS-2.2.D", Q("st-missing-prob", EV, "X takes values 0, 1, 2, 3 with P(0) = {{p0}}, P(1) = {{p1}}, P(2) = {{p2}} and P(3) unknown. What is E(X)?",
        cases=[{"p0": 0.1, "p1": 0.3, "p2": 0.4}, {"p0": 0.25, "p1": 0.25, "p2": 0.25}, {"p0": 0.5, "p1": 0.2, "p2": 0.2}, {"p0": 0.05, "p1": 0.15, "p2": 0.5}],
        value="p1 + 2*p2 + 3*(1 - p0 - p1 - p2)", tex="E(X)",
        verify="nsimplify(p1) + 2*nsimplify(p2) + 3*(1 - nsimplify(p0) - nsimplify(p1) - nsimplify(p2))",
        explain="First P(3) = 1 − (sum of the others), then E(X) = Σ x·P(x)")),
    ("SS-2.2.D", facts("st-ev-interpret", EV, [
        ("A raffle ticket has E(winnings) = −0.40 dollars. What does that mean?", "Over many tickets, a buyer loses 40 cents per ticket on average", "Every ticket loses 40 cents", "40% of tickets lose", "The raffle is fair"),
        ("Which list is a valid probability distribution?", "0.2, 0.5, 0.3", "0.4, 0.4, 0.4", "0.6, −0.1, 0.5", "0.3, 0.3, 0.3"),
        ("A random variable has SD 0. What does that say?", "It always takes the same value", "Its mean is 0", "It is binomial", "It is normal"),
        ("A game's expected net gain is 0. What is it called?", "Fair", "Biased", "Unbiased estimator", "Independent"),
    ], "The mean of a random variable is a long-run average, not a typical single outcome", pace="quick")),
    # 2.2.E binomial setting
    ("SS-2.2.E", facts("st-binomial-check", DIST, [
        ("Draw 5 cards without replacement from a standard deck and count hearts. Why is it not binomial?", "Draws are not independent; p changes", "Outcomes are not binary", "n is not fixed", "There are too few trials"),
        ("Roll a die until a 6 appears and count rolls. Why is it not binomial?", "The number of trials is not fixed (it is geometric)", "p changes", "Outcomes are not binary", "Rolls are dependent"),
        ("Survey 20 people from a city of 2 million and count those who own a car. Binomial?", "Approximately: the sample is under 10% of the population", "No: without replacement always breaks it", "No: car ownership is not binary", "Only if p = 0.5"),
        ("Count heads in 10 tosses of a fair coin. Which conditions hold?", "All four: binary, independent, fixed n, same p", "Only binary and fixed n", "Only independence", "None"),
    ], "BINS: Binary, Independent, Number fixed, Same probability")),
    ("SS-2.2.E", Q("st-at-least-one", DIST, "Each of {{n}} independent parts fails with probability {{p}}. What is the probability that at least one fails?",
        given={"n": {"pick": [5, 10, 20]}, "p": {"pick": [0.02, 0.05, 0.1]}}, value="1 - (1 - p)^n", tex="P", verify="1 - (1 - nsimplify(p))**n",
        explain="P(at least one) = 1 − P(none) = 1 − (1 − p)ⁿ: easier than adding every case")),
    # 2.2.F sampling-distribution conditions
    ("SS-2.2.F", Q("st-ten-percent", SAMP, "Sampling without replacement from a population of {{N}}, what is the largest sample size that meets the 10% condition?",
        given={"N": {"pick": [800, 1500, 4200, 25000]}}, value="floor(N/10)", tex="n", final=True, verify="floor(Rational(N, 10))",
        explain="n ≤ N/10 keeps draws nearly independent, so the usual standard-deviation formulas hold")),
    ("SS-2.2.F", facts("st-clt-conditions", SAMP, [
        ("A population is strongly skewed. When is the sampling distribution of x̄ approximately normal?", "When n is large, about 30 or more (CLT)", "Never", "Only when n < 10", "Only for proportions"),
        ("n = 50 and p = 0.04. Is the sampling distribution of p̂ approximately normal?", "No: np = 2 is below 10", "Yes: n ≥ 30", "Yes: p is small", "Only if the population is normal"),
        ("A population is normal. How large must n be for x̄ to be normal?", "Any n", "At least 30", "At least 100", "n must equal 10% of N"),
        ("What happens to the SD of x̄ when n is multiplied by 4?", "It halves", "It doubles", "It quarters", "It does not change"),
    ], "Large counts for proportions, the CLT for means, and σ/√n for spread", pace="quick")),
    # 2.2.G estimators
    ("SS-2.2.G", facts("st-unbiased", SAMP, [
        ("An estimator's sampling distribution is centred on the true parameter. It is …", "Unbiased", "Precise", "Consistent with any n", "Resistant"),
        ("Simulated sample maxima average 47 when the true population maximum is 50. The sample maximum is …", "Biased (low) as an estimator of the population maximum", "Unbiased", "Exact", "Too variable but unbiased"),
        ("How does a larger sample size change an unbiased estimator?", "Less variability, same centre", "Less bias", "More bias", "No change at all"),
        ("Which statistic is an unbiased estimator of p?", "p̂", "The sample maximum", "The sample range", "The sample median of a skewed variable"),
    ], "Bias is about the centre of the sampling distribution, variability about its spread")),
    ("SS-2.2.G", Q("st-point-estimate", SAMP, "A random sample of {{n}} gives {{k}} successes. What is the point estimate of p, as a decimal?",
        given={"n": {"pick": [80, 150, 400]}, "k": {"pick": [12, 36, 60]}}, value="k/n", tex="\\hat p", verify="Rational(k, n)",
        explain="p̂ = successes ÷ n is the unbiased point estimate of the population proportion")),
    # 2.2.H normal
    ("SS-2.2.H", Q("st-normal-from-facts", DIST, "A normal distribution has {{f1}} and {{f2}}. What is its standard deviation?",
        cases=[{"f1": "2.5% of values above 130", "f2": "mean 100", "s": 15}, {"f1": "16% of values below 62", "f2": "mean 70", "s": 8}, {"f1": "inflection points at 40 and 60", "f2": "a symmetric shape", "s": 10}, {"f1": "the middle 95% from 18 to 42", "f2": "a symmetric shape", "s": 6}],
        value="s", tex="\\sigma", final=True, verify="[Rational(130 - 100, 2), Rational(70 - 62, 1), Rational(60 - 40, 2), Rational(42 - 18, 4)][[15, 8, 10, 6].index(s)]",
        explain="Use 68-95-99.7: 2.5% in one tail is 2σ out, 16% is 1σ out, and the inflection points are ±1σ")),
    ("SS-2.2.H", facts("st-normal-describe", DIST, [
        ("In a normal distribution, how do mean and median compare?", "They are equal", "The mean is larger", "The median is larger", "It depends on σ"),
        ("Where are the inflection points of a normal curve?", "One SD either side of the mean", "Two SDs either side", "At the mean", "At the quartiles"),
        ("Two normal curves have the same mean; one has a larger SD. How does it look?", "Lower and wider", "Taller and narrower", "Shifted right", "Skewed"),
        ("What total area lies under a normal density curve?", "1", "0.5", "100", "Depends on σ"),
    ], "A normal curve is fixed by its mean (centre) and SD (spread)")),
    # 3.1.D choose the procedure
    ("SS-3.1.D", facts("st-choose-procedure", INF, [
        ("Is the proportion of defective parts below 5%? One random sample of parts.", "One-sample z test for a proportion", "Two-sample t test", "Chi-square test for independence", "Paired t interval"),
        ("Do two random samples of patients differ in mean recovery time?", "Two-sample t procedure for a difference of means", "One-proportion z test", "Paired t test", "Chi-square goodness of fit"),
        ("Each subject's blood pressure is measured before and after a drug. Did it fall on average?", "Paired t test on the differences", "Two-sample t test", "Two-proportion z test", "Chi-square homogeneity"),
        ("One random sample is classified by two categorical variables. Are they related?", "Chi-square test for independence", "Chi-square test for homogeneity", "Two-sample t test", "One-sample t test"),
        ("Independent random samples from three regions are compared on favourite brand. Same distribution?", "Chi-square test for homogeneity", "Chi-square independence", "Paired t test", "One-proportion z interval"),
    ], "Ask: categorical or quantitative response? One sample, two independent samples or paired? Estimate or test?", pace="quick")),
    ("SS-3.1.D", facts("st-parameter-name", INF, [
        ("A study estimates the average daily screen time of all teens in a state. What is the parameter?", "μ, the mean screen time of all teens in the state", "x̄, the sample mean", "p, a proportion", "μ₁ − μ₂"),
        ("A test asks whether more men than women support a law. What is the parameter?", "p₁ − p₂, the difference in population proportions", "p̂₁ − p̂₂", "μ_d", "χ²"),
        ("Twins are paired; one gets a tutoring program. What is the parameter?", "μ_d, the mean of the within-pair differences", "μ₁ − μ₂ for independent groups", "p", "σ"),
        ("A study estimates the fraction of a city's trees that are diseased. What is the parameter?", "p, the proportion of all the city's trees that are diseased", "p̂", "μ", "n"),
    ], "Name the parameter in words and symbols, about the population, never the sample", pace="quick")),
    # 3.1.E hypotheses and conditions
    ("SS-3.1.E", facts("st-hypotheses", INF, [
        ("A company claims 90% of orders ship on time; a manager suspects fewer do. Hypotheses?", "H₀: p = 0.90, Hₐ: p < 0.90", "H₀: p̂ = 0.90, Hₐ: p̂ < 0.90", "H₀: p < 0.90, Hₐ: p = 0.90", "H₀: p = 0.90, Hₐ: p is not 0.90"),
        ("Does a new fertiliser change mean yield from 40 bushels? Hypotheses?", "H₀: μ = 40, Hₐ: μ is not 40", "H₀: μ is not 40, Hₐ: μ = 40", "H₀: x̄ = 40, Hₐ: x̄ is not 40", "H₀: μ > 40, Hₐ: μ = 40"),
        ("Is a drug's cure rate higher than placebo's? Hypotheses?", "H₀: p₁ − p₂ = 0, Hₐ: p₁ − p₂ > 0", "H₀: p₁ − p₂ > 0, Hₐ: = 0", "H₀: p̂₁ = p̂₂", "H₀: μ₁ = μ₂"),
        ("In a chi-square test for independence, what is H₀?", "The two variables are independent in the population", "The variables are associated", "All counts are equal", "The sample is random"),
    ], "Hypotheses are about parameters; H₀ holds the equality, Hₐ what the study suspects")),
    ("SS-3.1.E", Q("st-large-counts", INF, "A test of H₀: p = {{p0}} uses n = {{n}}. What is the smaller of n·p₀ and n(1 − p₀)? (The condition needs it to be at least 10.)",
        given={"p0": {"pick": [0.05, 0.1, 0.2, 0.6]}, "n": {"pick": [80, 150, 400]}}, value="min(n*p0, n*(1 - p0))", tex="\\min",
        verify="Min(n*nsimplify(p0), n*(1 - nsimplify(p0)))", explain="For a test, the large-counts check uses p₀ (the null value); for an interval it uses p̂")),
    # 3.1.F interpret
    ("SS-3.1.F", facts("st-pvalue-interpret", INF, [
        ("A test of H₀: p = 0.5 gives p-value 0.03. What does 0.03 mean?", "If p = 0.5, a result this extreme would happen about 3% of the time", "There is a 3% chance H₀ is true", "There is a 97% chance Hₐ is true", "The sample proportion is 0.03"),
        ("p-value = 0.12 at α = 0.05. Conclusion?", "Fail to reject H₀: not convincing evidence for Hₐ", "Accept H₀ as proven", "Reject H₀", "Reject Hₐ"),
        ("A 95% interval for p is (0.41, 0.49). Is p = 0.5 plausible?", "No: 0.5 lies outside the interval", "Yes: it is close", "Yes: intervals contain every value", "Cannot tell"),
        ("What does '95% confident' mean?", "95% of intervals built this way capture the true parameter", "P(parameter in this interval) = 0.95", "95% of the data lie in the interval", "The sample mean is 95% accurate"),
        ("A 95% interval for μ₁ − μ₂ is (−2.1, 4.3). Is there convincing evidence of a difference?", "No: 0 lies in the interval", "Yes: the interval is wide", "Yes: it has positive values", "Cannot tell without the p-value"),
    ], "The p-value is computed assuming H₀; confidence is about the method, not one interval", pace="quick")),
    ("SS-3.1.F", Q("st-ci-midpoint", INF, "A confidence interval for p is ({{lo}}, {{hi}}). What was the margin of error?",
        given={"lo": {"pick": [0.32, 0.41, 0.55]}, "hi": {"pick": [0.38, 0.47, 0.63]}}, value="(hi - lo)/2", tex="ME",
        verify="(nsimplify(hi) - nsimplify(lo))/2", explain="The interval is estimate ± ME, so ME is half its width and the estimate its midpoint")),
    # 3.1.G errors
    ("SS-3.1.G", facts("st-error-type", INF, [
        ("H₀: a patient does not have the disease. A test says the patient has it, but they don't. Which error?", "Type I", "Type II", "Neither", "Sampling error"),
        ("H₀: a batch is safe. The test passes a batch that is actually contaminated. Which error?", "Type II", "Type I", "Neither", "Response bias"),
        ("How can β be reduced without raising α?", "Increase the sample size", "Lower α", "Use a two-sided test", "Reduce the effect size"),
        ("A study uses α = 0.01 instead of 0.05. What happens?", "Type I errors become rarer, Type II errors more likely", "Both become rarer", "Power increases", "Nothing changes"),
    ], "Type I: false alarm; Type II: missed effect; more data lowers β")),
    ("SS-3.1.G", Q("st-error-prob", INF, "A test uses α = {{al}} and has power {{pw}} against a specific alternative. What is the probability of {{what}}?",
        cases=[{"al": 0.05, "pw": 0.8, "what": "a Type I error when H₀ is true", "w": 0}, {"al": 0.05, "pw": 0.8, "what": "a Type II error at that alternative", "w": 1}, {"al": 0.01, "pw": 0.65, "what": "a Type II error at that alternative", "w": 1}, {"al": 0.1, "pw": 0.9, "what": "a Type I error when H₀ is true", "w": 0}],
        value="w == 0 ? al : 1 - pw", tex="P", verify="[nsimplify(al), 1 - nsimplify(pw)][w]",
        explain="P(Type I) = α; P(Type II) = β = 1 − power")),
    # 3.1.H two proportions
    ("SS-3.1.H", Q("st-two-prop-se", INF, "Sample 1: p̂₁ = {{p1}} with n₁ = {{n1}}. Sample 2: p̂₂ = {{p2}} with n₂ = {{n2}}. What is the standard error of p̂₁ − p̂₂?",
        given={"p1": {"pick": [0.4, 0.55, 0.7]}, "p2": {"pick": [0.3, 0.45]}, "n1": {"pick": [100, 200]}, "n2": {"pick": [150, 250]}},
        value="sqrt(p1*(1 - p1)/n1 + p2*(1 - p2)/n2)", tex="SE",
        verify="sqrt(nsimplify(p1)*(1 - nsimplify(p1))/n1 + nsimplify(p2)*(1 - nsimplify(p2))/n2)",
        explain="Variances of independent estimates add, so the SEs add in quadrature")),
    ("SS-3.1.H", Q("st-two-prop-ci", INF, "p̂₁ = {{p1}}, p̂₂ = {{p2}}, and the standard error of the difference is {{se}}. With z* = 1.96, what is the {{side}} endpoint of the 95% interval for p₁ − p₂?",
        cases=[{"p1": 0.62, "p2": 0.5, "se": 0.04, "side": "lower", "sg": -1}, {"p1": 0.62, "p2": 0.5, "se": 0.04, "side": "upper", "sg": 1}, {"p1": 0.35, "p2": 0.41, "se": 0.03, "side": "upper", "sg": 1}, {"p1": 0.8, "p2": 0.7, "se": 0.05, "side": "lower", "sg": -1}],
        value="p1 - p2 + sg*1.96*se", tex="\\text{endpoint}", verify="nsimplify(p1) - nsimplify(p2) + sg*Rational(196, 100)*nsimplify(se)",
        explain="(p̂₁ − p̂₂) ± z*·SE; check whether 0 falls inside")),
    # 3.1.I chi-square df
    ("SS-3.1.I", Q("st-chisq-df", INF, "A chi-square test uses {{desc}}. How many degrees of freedom?",
        cases=[{"desc": "a 3 × 4 two-way table", "r": 3, "c": 4}, {"desc": "a 2 × 5 two-way table", "r": 2, "c": 5}, {"desc": "a goodness-of-fit test with 6 categories", "r": 6, "c": 2}, {"desc": "a 4 × 4 two-way table", "r": 4, "c": 4}],
        value="(r - 1)*(c - 1)", tex="df", final=True, verify="(r - 1)*(c - 1)",
        explain="Two-way: (rows − 1)(columns − 1); goodness of fit with k categories: k − 1")),
    ("SS-3.1.I", facts("st-chisq-shape", INF, [
        ("What is the shape of a chi-square distribution with few degrees of freedom?", "Strongly skewed right", "Symmetric", "Skewed left", "Uniform"),
        ("What is the mean of a chi-square distribution with df = 8?", "8", "0", "16", "√8"),
        ("As df grows, how does the chi-square distribution change?", "It becomes more symmetric and shifts right", "It becomes more skewed", "It shifts left", "It stays the same"),
        ("Why is a chi-square test always one-sided (upper tail)?", "Large χ² means observed counts are far from expected in any direction", "χ² can be negative", "The lower tail is undefined", "Convention only"),
    ], "χ² is a sum of squared standardised deviations: never negative, mean = df")),
    # 4.1.B t margin
    ("SS-4.1.B", Q("st-t-margin", INF, "A sample of n = {{n}} has s = {{s}}. Using t* = {{ts}}, what is the margin of error of the confidence interval for μ?",
        cases=[{"n": 16, "s": 8, "ts": 2.131}, {"n": 25, "s": 10, "ts": 2.064}, {"n": 36, "s": 12, "ts": 2.030}, {"n": 9, "s": 6, "ts": 2.306}],
        value="ts*s/sqrt(n)", tex="ME", verify="nsimplify(ts)*s/sqrt(n)", explain="ME = t*·s/√n with df = n − 1 (t* is read from the table for that df)")),
    ("SS-4.1.B", Q("st-t-resize", INF, "A t interval from n = {{n}} has margin of error {{me}}. Roughly what sample size gives margin {{me2}} at the same confidence and s?",
        cases=[{"n": 25, "me": 4, "me2": 2}, {"n": 30, "me": 6, "me2": 3}, {"n": 50, "me": 3, "me2": 1}, {"n": 40, "me": 5, "me2": 2.5}],
        value="n*(me/me2)^2", tex="n", verify="n*(nsimplify(me)/nsimplify(me2))**2", explain="ME ∝ 1/√n, so dividing ME by k multiplies n by k²")),
    # 4.1.C two means
    ("SS-4.1.C", Q("st-two-sample-t", INF, "Group 1: x̄₁ = {{m1}}, s₁ = {{s1}}, n₁ = {{n1}}. Group 2: x̄₂ = {{m2}}, s₂ = {{s2}}, n₂ = {{n2}}. What is the two-sample t statistic?",
        cases=[{"m1": 52, "s1": 8, "n1": 32, "m2": 48, "s2": 6, "n2": 30}, {"m1": 7.4, "s1": 1.2, "n1": 25, "m2": 6.8, "s2": 1.5, "n2": 25}, {"m1": 110, "s1": 15, "n1": 40, "m2": 102, "s2": 12, "n2": 36}],
        value="(m1 - m2)/sqrt(s1^2/n1 + s2^2/n2)", tex="t",
        verify="(nsimplify(m1) - nsimplify(m2))/sqrt(nsimplify(s1)**2/n1 + nsimplify(s2)**2/n2)",
        explain="t = (x̄₁ − x̄₂)/√(s₁²/n₁ + s₂²/n₂), with H₀: μ₁ − μ₂ = 0")),
    ("SS-4.1.C", Q("st-conservative-df", INF, "A two-sample t procedure has n₁ = {{n1}} and n₂ = {{n2}}. What is the conservative degrees of freedom?",
        given={"n1": {"pick": [12, 20, 35]}, "n2": {"pick": [15, 18, 41]}}, value="min(n1, n2) - 1", tex="df", final=True, verify="Min(n1, n2) - 1",
        explain="The conservative choice is the smaller sample size minus 1; software's Welch df is larger")),
    # 5.1.B scatterplots and residuals
    ("SS-5.1.B", facts("st-scatter-describe", BIV, [
        ("As study hours rise, scores rise in a straight-line pattern with little scatter. Description?", "Strong, positive, linear", "Weak, negative, curved", "Strong, negative, linear", "No association"),
        ("A residual plot shows a clear U shape. What does it say?", "A linear model is not appropriate; the relationship is curved", "The line fits well", "There is no relationship", "Residuals are all positive"),
        ("A point far to the right of the others in x pulls the line toward it. What is it?", "An influential point (high leverage)", "A residual of zero", "An outlier only in y", "A lurking variable"),
        ("A residual plot shows random scatter with a fan shape widening to the right. What does it say?", "Variability of y grows with x", "The model is perfect", "The relationship is curved", "There is no association"),
    ], "Describe direction, form, strength and unusual points; read the residual plot for form")),
    ("SS-5.1.B", Q("st-residual", BIV, "The least-squares line is ŷ = {{b0}} + {{b1}}x. An observation has x = {{xv}} and y = {{yv}}. What is its residual?",
        cases=[{"b0": 12, "b1": 2.5, "xv": 10, "yv": 41}, {"b0": 3.2, "b1": 0.8, "xv": 15, "yv": 14}, {"b0": 50, "b1": -1.5, "xv": 12, "yv": 30}, {"b0": -4, "b1": 3, "xv": 7, "yv": 19}],
        value="yv - (b0 + b1*xv)", tex="e", verify="nsimplify(yv) - (nsimplify(b0) + nsimplify(b1)*xv)",
        explain="Residual = observed − predicted; positive means the point lies above the line")),
]
