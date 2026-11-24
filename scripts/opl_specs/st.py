from math import comb
from opl_dsl import Q, L, U

SIGN = [{"n": n, "k": k, "pv": sum(comb(n, j) for j in range(k, n + 1)) / 2**n} for n in range(6, 13) for k in range(n // 2 + 1, n)]
MEDCI = [{"n": n, "k": k, "cov": 1 - 2 * sum(comb(n, j) for j in range(0, k)) / 2**n} for n in range(8, 16) for k in (1, 2, 3)]

FW, FILE, IDEA = "SS", "opl-st", "MAIN"
k_ = "Symbol('k')"


def q(name, skill, prompt, value, verify, explain, tex="x", **kw):
    return Q(name, skill, prompt, value=value, verify=verify, explain=explain, tex=tex, **kw)


UNITS = [
U(6, "probability-models", "Probability models", [
    ("Random variables and their laws", [
        L("A", "Convert between probability and odds.", "Odds in favour = p/(1 − p).", ["PB1.6"], [
            q("st-odds", "stats.probability", "An event has probability ${{p}}$. What are the odds in favour, as a single number $p/(1-p)$?",
              "p/(1 - p)", "solve(Eq(x/(1 + x), nsimplify(p)), x)[0]", "Odds compare the chance it happens with the chance it does not: ${{p}}$ to ${{1 - p}}$. Odds of 3 mean 3 to 1, a probability of 0.75",
              given={"p": {"pick": [0.2, 0.25, 0.4, 0.6, 0.75, 0.8]}}, tex="o", pace="recall")]),
        L("B", "Find the median of a continuous distribution.", "Solve F(m) = 1/2.", ["PB2.3"], [
            q("st-median-exponential", "stats.distributions", "Waiting times are exponential with rate $\\lambda = {{l}}$ per minute. What is the median wait, in minutes?",
              "log(2)/l", "solve(Eq(integrate(nsimplify(l)*exp(-nsimplify(l)*Symbol('s')), (Symbol('s'), 0, x)), Rational(1, 2)), x)[0]",
              "Set $1 - e^{-\\lambda m} = 1/2$: $m = \\ln 2/\\lambda$, shorter than the mean $1/\\lambda$ because the long tail pulls the mean up",
              given={"l": {"pick": [0.1, 0.2, 0.5, 2]}}, tex="m", tol=0.001)]),
        L("C", "Use a density to find a probability and the CDF.", "P(a < X < b) = F(b) − F(a) = ∫ₐᵇ f.", ["PB2.5"], [
            q("st-pdf-interval", "stats.distributions", "$X$ has density $f(x) = 3x^2$ on $[0, 1]$. Find $P({{a}} < X < {{b}})$.",
              "b^3 - a^3", "integrate(3*x**2, (x, nsimplify(a), nsimplify(b)))", "The CDF is $F(x) = x^3$, so the probability is $F({{b}}) - F({{a}})$. For a continuous variable, $<$ and $\\le$ give the same answer",
              given={"a": {"pick": [0, 0.1, 0.2, 0.5]}, "b": {"pick": [0.6, 0.8, 0.9, 1]}}, tex="P")]),
        L("D", "Get a moment from a moment generating function.", "E[X] = M′(0), E[X²] = M″(0).", ["PB2.6"], [
            q("st-mgf-mean", "stats.expected-value", "$X$ has moment generating function $M(t) = (1 - {{p}} + {{p}}e^t)^{ {{n}} }$. Find $E[X]$ from $M'(0)$.",
              "n*p", "diff((1 - nsimplify(p) + nsimplify(p)*exp(x))**n, x).subs(x, 0)", "That is the binomial MGF; $M'(0) = n p$. The MGF of a sum of independent variables is the product of their MGFs",
              given={"p": {"pick": [0.1, 0.25, 0.5, 0.8]}, "n": {"int": [2, 12]}}, tex="E[X]")]),
        L("E", "Bound a tail probability with Chebyshev's inequality.", "P(|X − μ| ≥ kσ) ≤ 1/k² for any distribution.", ["PB5.1"], [
            q("st-chebyshev", "stats.probability", "Whatever the distribution, at most what fraction of values lie {{k}} or more standard deviations from the mean?",
              "1/k^2", "1/nsimplify(k)**2", "Chebyshev: at most $1/k^2$. For a normal distribution the true fraction is far smaller (about 4.6% beyond 2σ against Chebyshev's 25%)",
              given={"k": {"pick": [1.5, 2, 3, 4, 5]}}, tex="P", pace="recall")]),
        L("F", "Choose a sample size from the weak law of large numbers.", "P(|X̄ − μ| ≥ ε) ≤ σ²/(nε²).", ["PB5.2"], [
            q("st-lln-sample-size", "stats.sampling", "A measurement has $\\sigma = {{s}}$. By Chebyshev, how many measurements guarantee $P(|\\bar X - \\mu| \\ge {{e}}) \\le {{d}}$?",
              "s^2/(e^2*d)", "solve(Eq(s**2/(x*nsimplify(e)**2), nsimplify(d)), x)[0]", "Var$(\\bar X) = \\sigma^2/n$; Chebyshev gives $\\sigma^2/(n\\varepsilon^2) \\le \\delta$. This is the weak law of large numbers made quantitative; the normal approximation would need far fewer",
              given={"s": {"pick": [2, 5, 10]}, "e": {"pick": [0.5, 1, 2]}, "d": {"pick": [0.05, 0.1]}}, tex="n")]),
        L("G", "Read joint and marginal probabilities from a table.", "Marginals are row or column sums; all cells sum to 1.", ["PB6.1", "PB6.2"], [
            q("st-joint-missing", "stats.probability", "A joint table for $X, Y \\in \\{0, 1\\}$ has $P(0,0) = {{a/100}}$, $P(0,1) = {{b/100}}$, $P(1,0) = {{c/100}}$. Find $P(X = 1)$.",
              "(100 - a - b)/100", "Rational(c, 100) + (1 - Rational(a + b + c, 100))", "The missing cell is $1 - $ the others, ${{(100 - a - b - c)/100}}$; the marginal $P(X = 1)$ adds the $X = 1$ row: $P(1,0) + P(1,1)$",
              given={"a": {"int": [5, 30]}, "b": {"int": [5, 30]}, "c": {"int": [5, 25]}}, tex="P")]),
        L("H", "Compute a covariance from a joint table.", "Cov(X, Y) = E[XY] − E[X]E[Y].", ["PB6.3"], [
            q("st-covariance-table", "stats.expected-value", "For $X, Y \\in \\{0, 1\\}$: $P(1,1) = {{d/100}}$, $P(X = 1) = {{px/100}}$, $P(Y = 1) = {{py/100}}$. Find $\\operatorname{Cov}(X, Y)$.",
              "d/100 - px*py/10000", "Rational(d, 100)*1*1 - Rational(px, 100)*Rational(py, 100)", "For indicator variables $E[XY] = P(1,1)$ and $E[X] = P(X = 1)$. Zero covariance here means independence; in general it only means no linear association",
              given={"d": {"int": [5, 30]}, "px": {"int": [30, 60]}, "py": {"int": [30, 60]}}, require=["d <= px", "d <= py", "100*d != px*py"], tex="\\operatorname{Cov}")]),
    ]),
    ("Discrete distributions", [
        L("A", "Approximate a binomial probability with the normal.", "μ = np, σ = √(np(1−p)), with a continuity correction of ½.", ["PB3.3"], [
            q("st-normal-approx", "stats.distributions", "$X \\sim \\text{Bin}({{n}}, {{p}})$. Using the normal approximation with continuity correction, what $z$ corresponds to $P(X \\le {{k}})$?",
              "(k + 0.5 - n*p)/sqrt(n*p*(1 - p))", "solve(Eq(nsimplify(k) + Rational(1, 2), n*nsimplify(p) + x*sqrt(n*nsimplify(p)*(1 - nsimplify(p)))), x)[0]",
              "Use $\\mu = np$ and $\\sigma = \\sqrt{np(1 - p)}$, and stretch the integer ${{k}}$ to ${{k}} + 0.5$ so the bar for $X = k$ is included",
              given={"n": {"pick": [50, 100, 200]}, "p": {"pick": [0.3, 0.5, 0.6]}, "k": {"pick": [25, 40, 55, 70]}}, tex="z", tol=0.001)]),
        L("B", "Use the negative binomial distribution.", "P(rth success on trial n) = C(n−1, r−1) pʳ (1−p)ⁿ⁻ʳ.", ["PB3.5"], [
            q("st-negative-binomial", "stats.distributions", "Each trial succeeds with probability ${{p}}$. What is the probability that the {{r}}th success comes on trial {{n}}?",
              "combinations(n - 1, r - 1)*p^r*(1 - p)^(n - r)", "binomial(n - 1, r - 1)*nsimplify(p)**r*(1 - nsimplify(p))**(n - r)",
              "The last trial must be the ${{r}}$th success; the other ${{r - 1}}$ successes fall anywhere in the first ${{n - 1}}$ trials",
              given={"p": {"pick": [0.2, 0.3, 0.5]}, "r": {"int": [2, 4]}, "n": {"int": [5, 9]}}, tex="P", tol=0.0001)]),
        L("C", "Use the Poisson distribution.", "P(X = k) = e^{−λ} λᵏ / k!.", ["PB3.6"], [
            q("st-poisson", "stats.distributions", "Calls arrive at an average of ${{l}}$ per hour, as a Poisson process. What is the probability of exactly {{k}} calls in an hour?",
              "exp(-l)*l^k/factorial(k)", "diff(exp(nsimplify(l)*(x - 1)), x, k).subs(x, 0)/factorial(k)",
              "$P(X = k) = e^{-\\lambda}\\lambda^k/k!$. The Poisson is the binomial with many trials and a small chance each, $np = \\lambda$",
              given={"l": {"pick": [1, 2, 3, 4.5]}, "k": {"int": [0, 5]}}, tex="P", tol=0.0001)]),
        L("D", "Use the hypergeometric distribution.", "Drawing without replacement: C(K,k)C(N−K,n−k)/C(N,n).", ["PB3.7"], [
            q("st-hypergeometric", "stats.distributions", "A lot of {{N}} parts has {{K}} defective. {{n}} are drawn without replacement. What is the probability that exactly {{k}} are defective?",
              "combinations(K, k)*combinations(N - K, n - k)/combinations(N, n)", "binomial(K, k)*binomial(N - K, n - k)/binomial(N, n)",
              "Count the ways to pick ${{k}}$ of the ${{K}}$ bad and ${{n - k}}$ of the good, over all ways to pick ${{n}}$",
              given={"N": {"pick": [20, 25, 30]}, "K": {"pick": [3, 4, 5]}, "n": {"pick": [4, 5, 6]}, "k": {"int": [0, 2]}}, tex="P", tol=0.0001)]),
        L("E", "Use the multinomial distribution.", "n!/(a!b!c!) p₁ᵃ p₂ᵇ p₃ᶜ.", ["PB3.8"], [
            q("st-multinomial", "stats.distributions", "Each roll of a loaded die lands low, middle or high with probabilities 0.5, 0.3, 0.2. In {{a + b + c}} rolls, what is the probability of exactly {{a}} low, {{b}} middle and {{c}} high?",
              "factorial(a + b + c)/(factorial(a)*factorial(b)*factorial(c))*0.5^a*0.3^b*0.2^c",
              "binomial(a + b + c, a)*binomial(b + c, b)*Rational(1, 2)**a*Rational(3, 10)**b*Rational(1, 5)**c",
              "Choose which rolls are low, then which of the rest are middle; multiply by the chance of each pattern",
              given={"a": {"int": [1, 4]}, "b": {"int": [1, 3]}, "c": {"int": [0, 2]}}, tex="P", tol=0.0001)]),
        L("F", "Find the mean wait in an M/M/1 queue.", "W = 1/(μ − λ), L = λW (Little's law).", ["PB7.2"], [
            q("st-mm1-wait", "stats.expected-value", "Customers arrive at {{l}} per hour and one server handles {{m}} per hour (M/M/1). What is the mean time a customer spends in the system, in minutes?",
              "60/(m - l)", "60*(nsimplify(l)/(m - nsimplify(l)))/nsimplify(l)", "$\\rho = \\lambda/\\mu$, $L = \\rho/(1 - \\rho)$ customers, and Little's law $L = \\lambda W$ gives $W = 1/(\\mu - \\lambda)$. As $\\lambda \\to \\mu$ the wait blows up",
              given={"l": {"pick": [4, 6, 8, 9]}, "m": {"pick": [10, 12]}}, tex="W")]),
    ]),
    ("Continuous distributions", [
        L("A", "Find the variance of a uniform distribution.", "Var = (b − a)²/12.", ["PB4.1"], [
            q("st-uniform-variance", "stats.distributions", "$X$ is uniform on $[{{a}}, {{b}}]$. Find $\\operatorname{Var}X$.",
              "(b - a)^2/12", "integrate(x**2/(b - a), (x, a, b)) - integrate(x/(b - a), (x, a, b))**2", "Var $= E[X^2] - (E[X])^2 = (b - a)^2/12$: only the width matters",
              given={"a": {"int": [-3, 3]}, "b": {"int": [4, 10]}}, tex="\\sigma^2")]),
        L("B", "Use the exponential distribution.", "P(X > t) = e^{−λt}; memoryless.", ["PB4.2"], [
            q("st-exponential-survival", "stats.distributions", "A component's life is exponential with mean {{m}} years. What is the probability it lasts more than {{t}} years?",
              "exp(-t/m)", "integrate(exp(-x/m)/m, (x, t, oo))", "$\\lambda = 1/{{m}}$ and $P(X > t) = e^{-t/m}$. Memoryless: a used component that still works is as good as new",
              given={"m": {"pick": [2, 5, 10]}, "t": {"pick": [1, 2, 5, 10]}}, tex="P", tol=0.0001)]),
        L("C", "Compute a Weibull reliability.", "R(t) = exp(−(t/η)^β); β < 1, = 1, > 1 for falling, constant, rising hazard.", ["PB4.5"], [
            q("st-weibull", "stats.distributions", "Lifetimes are Weibull with shape $\\beta = {{bt}}$ and scale $\\eta = {{eta}}$ h. What fraction survive past {{t}} h?",
              "exp(-(t/eta)^bt)", "exp(-integrate(nsimplify(bt)/eta*(x/eta)**(nsimplify(bt) - 1), (x, 0, t)))",
              "Integrate the hazard $h(t) = \\frac\\beta\\eta(t/\\eta)^{\\beta - 1}$ and exponentiate. $\\beta = 1$ is the exponential; $\\beta > 1$ is wear-out",
              given={"bt": {"pick": [0.5, 1, 2, 3]}, "eta": {"pick": [100, 500, 1000]}, "t": {"pick": [50, 100, 200]}}, tex="R", tol=0.0001)]),
        L("D", "Find the mean and variance of a gamma distribution.", "Gamma(k, θ): mean kθ, variance kθ².", ["PB4.6"], [
            q("st-gamma-variance", "stats.distributions", "$X$ has a gamma distribution with shape $k = {{k}}$ and scale $\\theta = {{th}}$. Find $\\operatorname{Var}X$.",
              "k*th^2", f"integrate(x**2*x**(k - 1)*exp(-x/th)/(factorial(k - 1)*th**k), (x, 0, oo)) - integrate(x*x**(k - 1)*exp(-x/th)/(factorial(k - 1)*th**k), (x, 0, oo))**2",
              "A gamma with integer $k$ is the sum of $k$ independent exponentials of mean $\\theta$, so the variances add: $k\\theta^2$",
              given={"k": {"int": [1, 5]}, "th": {"int": [1, 4]}}, tex="\\sigma^2")]),
        L("E", "Find the mean of a beta distribution.", "Beta(a, b) on [0, 1] has mean a/(a + b).", ["PB4.7"], [
            q("st-beta-mean", "stats.distributions", "$X \\sim \\text{Beta}({{a}}, {{b}})$. Find $E[X]$.",
              "a/(a + b)", "integrate(x*x**(a - 1)*(1 - x)**(b - 1), (x, 0, 1))/integrate(x**(a - 1)*(1 - x)**(b - 1), (x, 0, 1))",
              "Beta distributions live on [0, 1] and model proportions; $a$ and $b$ act like counts of successes and failures",
              given={"a": {"int": [1, 6]}, "b": {"int": [1, 6]}}, tex="E[X]")]),
    ]),
]),
U(7, "survey-sampling", "Survey sampling", [
    ("Estimators from samples", [
        L("A", "Estimate a total with a ratio estimator.", "Ŷ = (ȳ / x̄) X, using a known total of an auxiliary variable.", ["ST2.2"], [
            q("st-ratio-estimator", "stats.sampling", "A sample of farms has mean yield {{yb}} t and mean area {{xb}} ha. The whole county has {{X}} ha. Estimate the county's total yield, in t.",
              "yb/xb*X", "solve(Eq(x/X, nsimplify(yb)/nsimplify(xb)), x)[0]", "The ratio estimator assumes yield is proportional to area: $\\hat Y = (\\bar y/\\bar x)X$",
              given={"yb": {"pick": [120, 150, 200]}, "xb": {"pick": [40, 50, 60]}, "X": {"pick": [10000, 25000, 50000]}}, tex="\\hat Y")]),
        L("B", "Adjust a sample mean with a regression estimator.", "ȳ_reg = ȳ + b(X̄ − x̄).", ["ST2.3"], [
            q("st-regression-estimator", "stats.sampling", "A sample has $\\bar y = {{yb}}$, $\\bar x = {{xb}}$ and fitted slope $b = {{b}}$. The population mean of $x$ is ${{XB}}$. What is the regression estimate of the mean of $y$?",
              "yb + b*(XB - xb)", "yb + nsimplify(b)*(XB - xb)", "The sample's $x$ came out ${{xb - XB}}$ off the known mean; shift $\\bar y$ along the fitted line to correct for it",
              given={"yb": {"int": [40, 80]}, "xb": {"int": [20, 30]}, "b": {"pick": [0.5, 1.2, 2]}, "XB": {"int": [22, 32]}}, require=["XB != xb"], tex="\\bar y_{reg}")]),
        L("C", "Combine strata into a stratified estimate.", "ȳ_st = Σ W_h ȳ_h with W_h = N_h / N.", ["ST2.4"], [
            q("st-stratified-mean", "stats.sampling", "A town has {{N1}} houses in stratum A (sample mean {{y1}}) and {{N2}} in stratum B (sample mean {{y2}}). What is the stratified estimate of the mean?",
              "(N1*y1 + N2*y2)/(N1 + N2)", "Rational(N1, N1 + N2)*y1 + Rational(N2, N1 + N2)*y2", "Weight each stratum's mean by its share of the population, not by its share of the sample",
              given={"N1": {"pick": [200, 300, 600]}, "N2": {"pick": [400, 700, 900]}, "y1": {"int": [10, 30]}, "y2": {"int": [30, 60]}}, tex="\\bar y_{st}")]),
        L("D", "Estimate a total from a cluster sample.", "Ŷ = (N/n) Σ (cluster totals).", ["ST2.5"], [
            q("st-cluster-total", "stats.sampling", "{{n}} of {{N}} city blocks are sampled at random and every household in them counted; the sampled blocks hold {{T}} households in total. Estimate the city's households.",
              "N/n*T", "Rational(N, n)*T", "Each sampled block stands for $N/n$ blocks. Cluster sampling is cheap but households in one block are alike, which widens the error",
              given={"n": {"pick": [10, 20, 25]}, "N": {"pick": [400, 500, 1000]}, "T": {"pick": [600, 900, 1500]}}, tex="\\hat Y")]),
        L("E", "Estimate a population size by capture–recapture.", "N ≈ M C / R (Lincoln–Petersen).", ["ST2.7"], [
            q("st-capture-recapture", "stats.sampling", "{{M}} fish are tagged and released. Later {{C}} are caught, of which {{R}} carry tags. Estimate the population.",
              "M*C/R", "solve(Eq(Rational(R, C), M/x), x)[0]", "Tagged fraction in the catch ≈ tagged fraction in the lake: $R/C = M/N$",
              given={"M": {"pick": [50, 100, 200]}, "C": {"pick": [60, 80, 150]}, "R": {"pick": [5, 8, 10, 12]}}, tex="\\hat N")]),
    ]),
]),
U(8, "inference-more", "Inference for means, proportions and variances", [
    ("Confidence intervals", [
        L("A", "Build a z interval for a mean.", "x̄ ± z* σ/√n.", ["ST5.2"], [
            q("st-z-interval", "stats.inference", "$n = {{n}}$, $\\bar x = {{xb}}$, known $\\sigma = {{s}}$. With $z^* = 1.96$, what is the upper end of the 95% interval for $\\mu$?",
              "xb + 1.96*s/sqrt(n)", "xb + Rational(196, 100)*s/sqrt(n)", "Margin $= z^*\\sigma/\\sqrt n$. Quadrupling $n$ halves it",
              given={"n": {"pick": [16, 25, 36, 64, 100]}, "xb": {"int": [40, 80]}, "s": {"pick": [4, 8, 10, 15]}}, tex="U", tol=0.0001)]),
        L("B", "Build an interval for a difference of proportions.", "p̂₁ − p̂₂ ± z* √(p̂₁q̂₁/n₁ + p̂₂q̂₂/n₂).", ["ST5.5"], [
            q("st-two-prop-margin", "stats.inference", "Group 1: {{x1}} of {{n1}}; group 2: {{x2}} of {{n2}}. With $z^* = 1.96$, what is the margin of error for $p_1 - p_2$?",
              "1.96*sqrt((x1/n1)*(1 - x1/n1)/n1 + (x2/n2)*(1 - x2/n2)/n2)", "Rational(196, 100)*sqrt(Rational(x1, n1)*(1 - Rational(x1, n1))/n1 + Rational(x2, n2)*(1 - Rational(x2, n2))/n2)",
              "Variances of independent estimates add; the standard errors do not. For the interval, do not pool",
              given={"x1": {"int": [20, 60]}, "n1": {"pick": [100, 150]}, "x2": {"int": [20, 60]}, "n2": {"pick": [100, 200]}}, tex="ME", tol=0.0001)]),
        L("C", "Build an interval from paired data.", "Work with the differences: d̄ ± t* s_d/√n.", ["ST5.6"], [
            q("st-paired-margin", "stats.inference", "{{n}} subjects are measured before and after; the differences have $\\bar d = {{db}}$ and $s_d = {{sd}}$. With $t^* = {{ts}}$, what is the margin of error?",
              "ts*sd/sqrt(n)", "nsimplify(ts)*nsimplify(sd)/sqrt(n)", "Pairing turns two samples into one sample of differences, which removes the subject-to-subject variation",
              cases=[{"n": 10, "ts": 2.262}, {"n": 15, "ts": 2.145}, {"n": 20, "ts": 2.093}, {"n": 25, "ts": 2.064}],
              given={"db": {"pick": [1.5, 2.4, 3]}, "sd": {"pick": [2, 3.5, 5]}}, tex="ME", tol=0.0001)]),
        L("D", "Build a z interval for a difference of means.", "(x̄₁ − x̄₂) ± z* √(σ₁²/n₁ + σ₂²/n₂).", ["ST5.7"], [
            q("st-two-z-margin", "stats.inference", "Known $\\sigma_1 = {{s1}}$, $\\sigma_2 = {{s2}}$, samples $n_1 = {{n1}}$, $n_2 = {{n2}}$. With $z^* = 1.96$, find the margin of error for $\\mu_1 - \\mu_2$.",
              "1.96*sqrt(s1^2/n1 + s2^2/n2)", "Rational(196, 100)*sqrt(Rational(s1**2, n1) + Rational(s2**2, n2))", "Add the variances of the two means, then take the square root",
              given={"s1": {"pick": [4, 6, 10]}, "s2": {"pick": [5, 8, 12]}, "n1": {"pick": [25, 40, 50]}, "n2": {"pick": [30, 40, 60]}}, tex="ME", tol=0.0001)]),
        L("E", "Find the standard error for two independent samples.", "SE = √(s₁²/n₁ + s₂²/n₂) (Welch).", ["ST5.8", "ST6.8"], [
            q("st-welch-t", "stats.inference", "Sample 1: $\\bar x = {{m1}}$, $s = {{s1}}$, $n = {{n1}}$; sample 2: $\\bar x = {{m2}}$, $s = {{s2}}$, $n = {{n2}}$. Find the Welch $t$ statistic.",
              "(m1 - m2)/sqrt(s1^2/n1 + s2^2/n2)", "(m1 - m2)/sqrt(Rational(s1**2, n1) + Rational(s2**2, n2))", "$t = (\\bar x_1 - \\bar x_2)/\\text{SE}$ with the unpooled SE; Welch's degrees of freedom handle unequal variances",
              given={"m1": {"int": [50, 60]}, "m2": {"int": [44, 52]}, "s1": {"pick": [4, 6, 8]}, "s2": {"pick": [5, 7, 9]}, "n1": {"pick": [12, 20, 30]}, "n2": {"pick": [10, 18, 25]}}, require=["m1 != m2"], tex="t", tol=0.0001)]),
        L("F", "Build a confidence interval for a variance.", "((n−1)s²/χ²_upper, (n−1)s²/χ²_lower).", ["ST5.9"], [
            q("st-variance-interval", "stats.inference", "$n = {{n}}$, $s^2 = {{v}}$. The chi-square critical values with {{n - 1}} df are ${{cl}}$ and ${{cu}}$. What is the lower end of the 95% interval for $\\sigma^2$?",
              "(n - 1)*v/cu", "(n - 1)*nsimplify(v)/nsimplify(cu)", "Divide $(n - 1)s^2$ by the larger critical value for the lower end. The interval is not symmetric about $s^2$",
              cases=[{"n": 10, "cl": 2.700, "cu": 19.023}, {"n": 15, "cl": 5.629, "cu": 26.119}, {"n": 20, "cl": 8.907, "cu": 32.852}, {"n": 25, "cl": 12.401, "cu": 39.364}],
              given={"v": {"pick": [4, 9, 16, 25]}}, tex="L", tol=0.0001)]),
    ]),
    ("Hypothesis tests", [
        L("A", "Compute a one-sample z statistic.", "z = (x̄ − μ₀)/(σ/√n).", ["ST6.2"], [
            q("st-z-test", "stats.inference", "$H_0: \\mu = {{m0}}$. A sample of {{n}} gives $\\bar x = {{xb}}$; $\\sigma = {{s}}$ is known. Find $z$.",
              "(xb - m0)/(s/sqrt(n))", "(xb - m0)*sqrt(n)/s", "Standardise the sample mean with its own standard error $\\sigma/\\sqrt n$",
              given={"m0": {"int": [50, 60]}, "n": {"pick": [16, 25, 36, 49]}, "xb": {"int": [48, 63]}, "s": {"pick": [5, 8, 10]}}, require=["xb != m0"], tex="z", tol=0.0001)]),
        L("B", "Compute a two-proportion z statistic.", "Pool p̂ under H₀: z = (p̂₁ − p̂₂)/√(p̂(1−p̂)(1/n₁ + 1/n₂)).", ["ST6.5"], [
            q("st-two-prop-z", "stats.inference", "Test $p_1 = p_2$: group 1 has {{x1}} of {{n1}}, group 2 has {{x2}} of {{n2}}. Find $z$ (pooled).",
              "(x1/n1 - x2/n2)/sqrt(((x1 + x2)/(n1 + n2))*(1 - (x1 + x2)/(n1 + n2))*(1/n1 + 1/n2))",
              "(Rational(x1, n1) - Rational(x2, n2))/sqrt(Rational(x1 + x2, n1 + n2)*(1 - Rational(x1 + x2, n1 + n2))*(Rational(1, n1) + Rational(1, n2)))",
              "Under $H_0$ the two groups share one $p$, so estimate it from both together. (The interval does not pool; the test does)",
              given={"x1": {"int": [30, 60]}, "n1": {"pick": [100, 120]}, "x2": {"int": [20, 50]}, "n2": {"pick": [100, 150]}}, require=["x1*n2 != x2*n1"], tex="z", tol=0.0001)]),
        L("C", "Compute a paired t statistic.", "t = d̄/(s_d/√n) with n − 1 df.", ["ST6.6"], [
            q("st-paired-t", "stats.inference", "Paired differences from {{n}} subjects have $\\bar d = {{db}}$ and $s_d = {{sd}}$. Find $t$ for $H_0: \\mu_d = 0$.",
              "db/(sd/sqrt(n))", "nsimplify(db)*sqrt(n)/nsimplify(sd)", "It is a one-sample $t$ on the differences, with ${{n - 1}}$ degrees of freedom",
              given={"n": {"pick": [9, 16, 25]}, "db": {"pick": [1.2, 2, 3.5]}, "sd": {"pick": [2, 3, 4.5]}}, tex="t", tol=0.0001)]),
        L("D", "Compute a two-sample z statistic.", "z = (x̄₁ − x̄₂)/√(σ₁²/n₁ + σ₂²/n₂).", ["ST6.7"], [
            q("st-two-z", "stats.inference", "With known $\\sigma_1 = {{s1}}$ and $\\sigma_2 = {{s2}}$: $\\bar x_1 = {{m1}}$ ($n = {{n1}}$), $\\bar x_2 = {{m2}}$ ($n = {{n2}}$). Find $z$ for $H_0: \\mu_1 = \\mu_2$.",
              "(m1 - m2)/sqrt(s1^2/n1 + s2^2/n2)", "(m1 - m2)/sqrt(Rational(s1**2, n1) + Rational(s2**2, n2))", "Same structure as the Welch $t$, with known σ in place of $s$",
              given={"s1": {"pick": [3, 5, 8]}, "s2": {"pick": [4, 6, 9]}, "m1": {"int": [20, 30]}, "m2": {"int": [18, 28]}, "n1": {"pick": [30, 50]}, "n2": {"pick": [40, 60]}}, require=["m1 != m2"], tex="z", tol=0.0001)]),
        L("E", "Compute the power of a one-sided z test.", "Power = Φ(δ√n/σ − z_α) for a true shift δ.", ["ST6.9"], [
            q("st-power", "stats.inference", "A one-sided z test at $\\alpha = 0.05$ ($z_\\alpha = 1.645$) has $\\sigma = {{s}}$ and $n = {{n}}$. If the true mean is {{d}} above $\\mu_0$, what is the power?",
              "0.5*(1 + erf((d*sqrt(n)/s - 1.645)/sqrt(2)))", "Rational(1, 2)*(1 + erf((nsimplify(d)*sqrt(n)/s - Rational(1645, 1000))/sqrt(2)))",
              "Reject when $\\bar x > \\mu_0 + 1.645\\sigma/\\sqrt n$; under the true mean that cut-off sits $1.645 - \\delta\\sqrt n/\\sigma$ standard errors away. Power rises with $n$ and with the effect size",
              given={"s": {"pick": [5, 10]}, "n": {"pick": [16, 25, 36]}, "d": {"pick": [1, 2, 3, 4]}}, tex="1 - \\beta", tol=0.001)]),
        L("F", "Test a variance with the chi-square statistic.", "χ² = (n − 1)s²/σ₀².", ["ST6.10"], [
            q("st-chi-variance", "stats.inference", "$H_0: \\sigma^2 = {{v0}}$. A sample of {{n}} has $s^2 = {{v}}$. Find the test statistic.",
              "(n - 1)*v/v0", "(n - 1)*nsimplify(v)/v0", "Under $H_0$ and normal data, $(n - 1)s^2/\\sigma_0^2$ is chi-square with $n - 1$ df. This test is very sensitive to non-normality",
              given={"v0": {"pick": [4, 9, 16]}, "n": {"pick": [10, 16, 21]}, "v": {"pick": [3, 6.5, 12, 20]}}, tex="\\chi^2", tol=0.0001)]),
        L("G", "Find the probability of a 2 × 2 table under Fisher's exact test.", "With margins fixed, the top-left cell is hypergeometric.", ["ST6.13"], [
            q("st-fisher-table", "stats.inference", "A 2 × 2 table has row totals {{r1}} and {{r2}} and first-column total {{c1}}. With the margins fixed, what is the probability that the top-left cell is {{a}}?",
              "combinations(r1, a)*combinations(r2, c1 - a)/combinations(r1 + r2, c1)", "binomial(r1, a)*binomial(r2, c1 - a)/binomial(r1 + r2, c1)",
              "Fisher's test treats the margins as fixed; the cell count is then hypergeometric. The p-value adds the probabilities of tables as extreme or more",
              given={"r1": {"pick": [5, 6, 8]}, "r2": {"pick": [5, 7, 9]}, "c1": {"pick": [5, 6, 7]}, "a": {"int": [1, 4]}}, require=["c1 - a <= r2", "a <= r1"], tex="P", tol=0.0001)]),
        L("H", "Compare two variances with an F statistic.", "F = s₁²/s₂² with (n₁ − 1, n₂ − 1) df.", ["ST6.14"], [
            q("st-f-variances", "stats.inference", "Sample 1 ($n = {{n1}}$) has $s = {{s1}}$; sample 2 ($n = {{n2}}$) has $s = {{s2}}$. Find $F = s_1^2/s_2^2$.",
              "s1^2/s2^2", "(nsimplify(s1)/nsimplify(s2))**2", "Square the standard deviations first. Under $H_0$ this is F with ({{n1 - 1}}, {{n2 - 1}}) df",
              given={"n1": {"pick": [10, 15]}, "n2": {"pick": [12, 20]}, "s1": {"pick": [2.5, 4, 6]}, "s2": {"pick": [2, 3, 5]}}, tex="F", tol=0.0001)]),
        L("I", "Compute a one-way ANOVA F statistic.", "F = MS_between / MS_within.", ["ST6.15"], [
            q("st-anova-f", "stats.inference", "Three groups of {{n}} have means {{a}}, {{b}}, {{c}}, and the pooled within-group variance is {{w}}. Find $F$.",
              "(n*((a - (a + b + c)/3)^2 + (b - (a + b + c)/3)^2 + (c - (a + b + c)/3)^2)/2)/w",
              "(n*(Matrix([a, b, c]) - Matrix([1, 1, 1])*(a + b + c)/3).dot(Matrix([a, b, c]) - Matrix([1, 1, 1])*(a + b + c)/3)/2)/nsimplify(w)",
              "SS between $= n\\sum(\\bar x_i - \\bar x)^2$ with $k - 1 = 2$ df; MS within is the pooled variance. A large F means the means differ more than the noise inside groups explains",
              given={"n": {"pick": [5, 8, 10]}, "a": {"int": [10, 14]}, "b": {"int": [12, 16]}, "c": {"int": [14, 19]}, "w": {"pick": [4, 6.5, 9]}}, require=["a != c"], tex="F", tol=0.0001)]),
        L("J", "Count degrees of freedom in a two-way ANOVA.", "Factor A: a − 1; B: b − 1; interaction (a − 1)(b − 1); error ab(n − 1).", ["ST6.16"], [
            q("st-twoway-df", "stats.inference", "A two-way ANOVA has factor A at {{a}} levels, factor B at {{b}} levels and {{n}} replicates per cell. How many degrees of freedom does the {{what}} have?",
              "k == 0 ? (a - 1)*(b - 1) : a*b*(n - 1)", "(a - 1)*(b - 1) if k == 0 else a*b*n - 1 - (a - 1) - (b - 1) - (a - 1)*(b - 1)",
              "Total $abn - 1$ splits into $A$, $B$, $A\\times B$ and error. Without replication there is no error term left to test the interaction",
              given={"a": {"int": [2, 4]}, "b": {"int": [2, 5]}, "n": {"int": [2, 4]}}, cases=[{"what": "interaction", "k": 0}, {"what": "error term", "k": 1}], tex="df", pace="recall")]),
    ]),
]),
U(9, "regression-more", "Inference in regression and generalised linear models", [
    ("Simple and multiple regression", [
        L("A", "Test a regression slope.", "t = b/SE_b with n − 2 df.", ["ST7.5", "ST12.5"], [
            q("st-slope-t", "stats.inference", "A regression on {{n}} points has slope $b = {{b}}$ with standard error ${{se}}$. Find $t$ for $H_0: \\beta = 0$.",
              "b/se", "nsimplify(b)/nsimplify(se)", "$t = b/\\text{SE}_b$ with $n - 2 = {{n - 2}}$ df in simple regression; in multiple regression the same ratio tests each coefficient",
              given={"n": {"pick": [12, 20, 30]}, "b": {"pick": [0.8, 1.5, -2.2, 3.4]}, "se": {"pick": [0.3, 0.5, 0.9]}}, tex="t", tol=0.0001)]),
        L("B", "Build an interval for a regression coefficient.", "b ± t* SE_b.", ["ST7.6", "ST12.4"], [
            q("st-slope-interval", "stats.inference", "A coefficient is estimated as {{b}} with SE {{se}}; $t^* = {{ts}}$. What is the lower end of its confidence interval?",
              "b - ts*se", "nsimplify(b) - nsimplify(ts)*nsimplify(se)", "If the interval excludes 0, the test of $\\beta = 0$ rejects at the matching level",
              given={"b": {"pick": [1.2, 2.5, -0.8, 4]}, "se": {"pick": [0.2, 0.4, 0.7]}, "ts": {"pick": [2.048, 2.101, 2.228]}}, tex="L", tol=0.0001)]),
        L("C", "Read a residual plot.", "Residuals should be a patternless band around zero.", ["ST7.7"], [
            Q("st-residual-diagnostics", "stats.bivariate", "A residual plot shows {{q}}. What does it suggest?", pace="recall",
              cases=[{"q": "a U-shaped curve", "ans": 0}, {"q": "a fan that widens to the right", "ans": 1}, {"q": "a random band of even width around 0", "ans": 2}, {"q": "one point far from all the others", "ans": 3}],
              choice=["The relationship is curved: transform or add a term", "Unequal variance: transform y or weight the fit", "The linear model is adequate", "An outlier or influential point: check it"],
              correct="ans", verify="authored", explain="Residuals carry what the line missed. Curvature, changing spread and lone points are the three things to look for")]),
        L("D", "Fit an exponential model by linearising.", "y = a e^{bx} ⇔ ln y = ln a + bx.", ["ST12.1"], [
            q("st-linearised-fit", "stats.bivariate", "A straight-line fit of $\\ln y$ against $x$ gives $\\ln y = {{c}} + {{d}}x$. What is $a$ in $y = ae^{bx}$?",
              "exp(c)", "solve(Eq(log(x), nsimplify(c)), x)[0]", "The intercept of the log fit is $\\ln a$ and the slope is $b$. Least squares on $\\ln y$ weights small $y$ values more than a direct nonlinear fit would",
              given={"c": {"pick": [0.5, 1.2, 2, 3.1]}, "d": {"pick": [-0.3, 0.2, 0.45]}}, tex="a", tol=0.0001)]),
        L("E", "Interpret an indicator variable.", "A 0/1 dummy shifts the intercept for one group.", ["ST12.2"], [
            q("st-indicator", "stats.bivariate", "$\\hat y = {{b0}} + {{b1}}x + {{b2}}D$ with $D = 1$ for the treated group. Predict $y$ for a treated unit with $x = {{x0}}$.",
              "b0 + b1*x0 + b2", "nsimplify(b0) + nsimplify(b1)*x0 + nsimplify(b2)*1", "The dummy's coefficient is the gap between groups at the same $x$: here ${{b2}}$",
              given={"b0": {"pick": [10, 12.5, 20]}, "b1": {"pick": [0.8, 1.5, 2]}, "b2": {"pick": [-3, 2.5, 4]}, "x0": {"int": [2, 10]}}, tex="\\hat y", tol=0.0001)]),
        L("F", "Predict from a fitted multiple regression.", "Plug each predictor into the fitted equation.", ["ST12.3"], [
            q("st-multiple-predict", "stats.bivariate", "$\\hat y = {{b0}} + {{b1}}x_1 + ({{b2}})x_2$. Predict $y$ at $x_1 = {{u}}$, $x_2 = {{w}}$.",
              "b0 + b1*u + b2*w", "Matrix([1, u, w]).dot(Matrix([nsimplify(b0), nsimplify(b1), nsimplify(b2)]))", "Each coefficient is the change in $\\hat y$ per unit of its predictor with the others held fixed",
              given={"b0": {"pick": [5, 8.5, 12]}, "b1": {"pick": [1.2, 2, 3]}, "b2": {"pick": [-1.5, -0.5, 0.75]}, "u": {"int": [1, 6]}, "w": {"int": [1, 8]}}, tex="\\hat y", tol=0.0001)]),
        L("G", "Compute an adjusted R².", "R²_adj = 1 − (1 − R²)(n − 1)/(n − k − 1).", ["ST12.6"], [
            q("st-adjusted-r2", "stats.bivariate", "A model with {{k}} predictors on {{n}} observations has $R^2 = {{r2}}$. Find the adjusted $R^2$.",
              "1 - (1 - r2)*(n - 1)/(n - k - 1)", "1 - (1 - nsimplify(r2))*(n - 1)/(n - k - 1)", "Adjusted $R^2$ charges for each predictor; it can fall when a useless variable is added",
              given={"k": {"int": [2, 6]}, "n": {"pick": [20, 30, 50]}, "r2": {"pick": [0.6, 0.75, 0.9]}}, tex="R^2_{adj}", tol=0.0001)]),
        L("H", "Compare models with AIC.", "AIC = n ln(SSE/n) + 2k; smaller is better.", ["ST12.7"], [
            q("st-aic", "stats.bivariate", "A least-squares model with {{k}} parameters on {{n}} points has SSE = {{sse}}. Compute AIC $= n\\ln(\\text{SSE}/n) + 2k$.",
              "n*log(sse/n) + 2*k", "n*log(nsimplify(sse)/n) + 2*k", "Between models fitted to the same data, the lower AIC wins; the $2k$ term is the penalty for each parameter",
              given={"k": {"int": [2, 5]}, "n": {"pick": [20, 40, 100]}, "sse": {"pick": [12, 35, 80, 150]}}, tex="AIC", tol=0.0001)]),
        L("I", "Compute an overall F statistic from R².", "F = (R²/k)/((1 − R²)/(n − k − 1)).", ["ST12.5"], [
            q("st-overall-f", "stats.inference", "A regression with {{k}} predictors on {{n}} observations has $R^2 = {{r2}}$. Find the overall $F$.",
              "(r2/k)/((1 - r2)/(n - k - 1))", "(nsimplify(r2)/k)/((1 - nsimplify(r2))/(n - k - 1))", "The overall F tests whether any predictor helps; it compares explained to unexplained variation per degree of freedom",
              given={"k": {"int": [2, 5]}, "n": {"pick": [25, 40, 60]}, "r2": {"pick": [0.3, 0.5, 0.7]}}, tex="F", tol=0.0001)]),
    ]),
    ("Generalised linear models", [
        L("A", "Predict a probability from a logistic regression.", "p = 1/(1 + e^{−(b₀ + b₁x)}); e^{b₁} is the odds ratio per unit x.", ["ST13.1"], [
            q("st-logistic", "stats.bivariate", "A logistic model has $\\ln\\frac{p}{1 - p} = {{b0}} + {{b1}}x$. Find $p$ at $x = {{x0}}$.",
              "1/(1 + exp(-(b0 + b1*x0)))", "solve(Eq(log(x/(1 - x)), nsimplify(b0) + nsimplify(b1)*x0), x)[0]", "Compute the log-odds, then invert: $p = 1/(1 + e^{-\\eta})$",
              given={"b0": {"pick": [-3, -2, -1.5]}, "b1": {"pick": [0.4, 0.8, 1.2]}, "x0": {"int": [0, 6]}}, tex="p", tol=0.0001)]),
        L("B", "Find an expected count under an independence loglinear model.", "μ_ij = (row total)(column total)/N.", ["ST13.2"], [
            q("st-loglinear-expected", "stats.inference", "In a contingency table with $N = {{N}}$, row $i$ totals {{r}} and column $j$ totals {{c}}. Under the independence loglinear model, what is the expected count in cell $(i, j)$?",
              "r*c/N", "exp(log(r) + log(c) - log(N))", "$\\log\\mu_{ij} = \\lambda + \\lambda_i^R + \\lambda_j^C$ with no interaction term, which is independence; the fitted counts are the familiar row × column / total",
              given={"N": {"pick": [200, 400, 500]}, "r": {"pick": [60, 80, 120]}, "c": {"pick": [50, 90, 150]}}, tex="\\mu", tol=0.0001)]),
        L("C", "Use a proportional-odds (ordinal) model.", "P(Y ≤ j) = 1/(1 + e^{−(θⱼ − βx)}).", ["ST13.3"], [
            q("st-ordinal", "stats.bivariate", "A proportional-odds model has $\\operatorname{logit} P(Y \\le 1) = {{t1}} - {{b}}x$. Find $P(Y \\le 1)$ at $x = {{x0}}$.",
              "1/(1 + exp(-(t1 - b*x0)))", "solve(Eq(log(x/(1 - x)), nsimplify(t1) - nsimplify(b)*x0), x)[0]", "Each cut-point has its own $\\theta_j$ but every cumulative logit shares the slope; that sharing is the proportional-odds assumption",
              given={"t1": {"pick": [-1, 0.5, 1.5]}, "b": {"pick": [0.3, 0.6, 1]}, "x0": {"int": [0, 5]}}, tex="P", tol=0.0001)]),
    ]),
]),
U(10, "nonparametric", "Nonparametric methods", [
    ("Rank and sign tests", [
        L("A", "Find a sign-test p-value.", "Under H₀ the count of + signs is Binomial(n, ½).", ["ST8.1"], [
            q("st-sign-test", "stats.inference", "Of {{n}} paired differences (no ties), {{k}} are positive. What is the one-sided sign-test p-value $P(X \\ge {{k}})$?",
              "pv", f"summation(binomial(n, {k_}), ({k_}, k, n))/2**n",
              "Count tables at least this extreme: $\\sum_{j \\ge k}\\binom nj/2^n$. The sign test uses only directions, so it works for any continuous distribution",
              cases=SIGN, tex="p", tol=0.0001)]),
        L("B", "Find the mean of the Wilcoxon rank-sum statistic.", "E[W] = n₁(N + 1)/2 under H₀.", ["ST8.2"], [
            q("st-rank-sum-mean", "stats.inference", "Two samples of sizes {{n1}} and {{n2}} are ranked together. Under $H_0$, what is the expected rank sum of the first sample?",
              "n1*(n1 + n2 + 1)/2", f"n1*summation({k_}, ({k_}, 1, n1 + n2))/(n1 + n2)", "Every rank is equally likely to land in either sample, so each of the $n_1$ ranks averages $(N + 1)/2$",
              given={"n1": {"int": [4, 12]}, "n2": {"int": [4, 12]}}, tex="E[W]", pace="recall")]),
        L("C", "Find the mean of the Wilcoxon signed-rank statistic.", "E[W⁺] = n(n + 1)/4.", ["ST8.3"], [
            q("st-signed-rank-mean", "stats.inference", "For {{n}} nonzero differences, what is the expected sum of the positive ranks $W^+$ under $H_0$?",
              "n*(n + 1)/4", f"summation({k_}, ({k_}, 1, n))/2", "Each rank $1..n$ is positive with probability ½: half of $n(n + 1)/2$",
              given={"n": {"int": [5, 20]}}, tex="E[W^+]", pace="recall")]),
        L("D", "Find the expected number of runs.", "E[R] = 2n₁n₂/(n₁ + n₂) + 1.", ["ST8.4", "ST10.3"], [
            q("st-runs-mean", "stats.inference", "A sequence has {{n1}} of one symbol and {{n2}} of the other in random order. What is the expected number of runs?",
              "2*n1*n2/(n1 + n2) + 1", f"1 + (n1 + n2 - 1)*2*Rational(n1, n1 + n2)*Rational(n2, n1 + n2 - 1)",
              "Each of the $N - 1$ adjacent pairs starts a new run when the symbols differ, with probability $2n_1n_2/(N(N - 1))$. Too few runs suggests clustering, too many suggests alternation",
              given={"n1": {"int": [5, 15]}, "n2": {"int": [5, 15]}}, tex="E[R]")]),
        L("E", "Compute the Kruskal–Wallis statistic.", "H = 12/(N(N+1)) Σ Rᵢ²/nᵢ − 3(N + 1).", ["ST8.5"], [
            q("st-kruskal-wallis", "stats.inference", "Three groups of {{n}} are ranked together ($N = {{3*n}}$). Their rank sums are {{r1}}, {{r2}} and {{3*n*(3*n + 1)/2 - r1 - r2}}. Find $H$.",
              "12/(3*n*(3*n + 1))*(r1^2 + r2^2 + (3*n*(3*n + 1)/2 - r1 - r2)^2)/n - 3*(3*n + 1)",
              "Rational(12, 3*n*(3*n + 1))*Matrix([r1, r2, Rational(3*n*(3*n + 1), 2) - r1 - r2]).dot(Matrix([r1, r2, Rational(3*n*(3*n + 1), 2) - r1 - r2]))/n - 3*(3*n + 1)",
              "It is a one-way ANOVA on ranks. The three rank sums must add to $N(N + 1)/2$, which is a quick check",
              given={"n": {"pick": [4, 5, 6]}, "r1": {"int": [15, 30]}, "r2": {"int": [20, 40]}}, require=["3*n*(3*n + 1)/2 - r1 - r2 > 0"], tex="H", tol=0.0001)]),
        L("F", "Compute a Kolmogorov–Smirnov statistic.", "D = max |F₁(x) − F₂(x)| over the data.", ["ST8.6"], [
            q("st-ks-statistic", "stats.inference", "Two empirical CDFs at four points are $F_1 = ({{a1}}, {{a2}}, {{a3}}, 1)$ and $F_2 = ({{b1}}, {{b2}}, {{b3}}, 1)$. Find $D = \\max|F_1 - F_2|$.",
              "max(abs(a1 - b1), abs(a2 - b2), abs(a3 - b3))", "Max(Abs(nsimplify(a1) - nsimplify(b1)), Abs(nsimplify(a2) - nsimplify(b2)), Abs(nsimplify(a3) - nsimplify(b3)))",
              "The KS statistic is the largest vertical gap between the two step functions. It is sensitive to differences in location, spread and shape at once",
              given={"a1": {"pick": [0.1, 0.2, 0.3]}, "a2": {"pick": [0.4, 0.5, 0.6]}, "a3": {"pick": [0.7, 0.8, 0.9]}, "b1": {"pick": [0.0, 0.05, 0.2]}, "b2": {"pick": [0.2, 0.35, 0.45]}, "b3": {"pick": [0.5, 0.65, 0.75]}}, tex="D", tol=0.0001)]),
        L("G", "Find the coverage of an order-statistic interval for a median.", "(x₍ₖ₎, x₍ₙ₋ₖ₊₁₎) covers the median with probability 1 − 2P(Bin(n, ½) ≤ k − 1).", ["ST8.8"], [
            q("st-median-interval", "stats.inference", "From {{n}} observations, the interval from the {{k}}th smallest to the {{k}}th largest is used for the median. What is its exact coverage?",
              "cov", f"1 - 2*summation(binomial(n, {k_}), ({k_}, 0, k - 1))/2**n",
              "The interval misses the median only if fewer than $k$ observations fall on one side. No distribution assumptions needed",
              cases=MEDCI, tex="C", tol=0.0001)]),
        L("H", "Know the relative efficiency of rank tests.", "Against the t test on normal data, the sign test has ARE 2/π ≈ 0.64 and the Wilcoxon 3/π ≈ 0.95.", ["ST8.9"], [
            q("st-relative-efficiency", "stats.inference", "On normal data, roughly how many observations does the {{t}} need to match a $t$ test on 100? (Use the asymptotic relative efficiency.)",
              "100/are", "100/are", "ARE is the ratio of sample sizes for equal power. The Wilcoxon loses almost nothing on normal data and can win heavily on heavy-tailed data",
              cases=[{"t": "sign test", "are": 0.6366197723675814}, {"t": "Wilcoxon signed-rank test", "are": 0.954929658551372}], tex="n", tol=0.01, pace="recall")]),
    ]),
]),
U(11, "bayes-estimation", "Bayesian inference and point estimation", [
    ("Bayesian inference", [
        L("A", "Choose a conjugate prior.", "Beta for a binomial p, gamma for a Poisson rate, normal for a normal mean.", ["ST9.1"], [
            Q("st-conjugate-prior", "stats.probability", "Which prior is conjugate for {{q}}?", pace="recall",
              cases=[{"q": "a binomial success probability", "ans": 0}, {"q": "a Poisson rate", "ans": 1}, {"q": "a normal mean with known variance", "ans": 2}, {"q": "an exponential rate", "ans": 1}],
              choice=["Beta", "Gamma", "Normal"], correct="ans", verify="authored",
              explain="A conjugate prior gives a posterior of the same family, so updating is arithmetic on its parameters")]),
        L("B", "Find a posterior mean under an improper prior.", "Beta(0, 0) is improper, but with data it gives the posterior Beta(s, n − s).", ["ST9.2"], [
            q("st-improper-prior", "stats.probability", "With the improper prior $\\pi(p) \\propto 1/(p(1 - p))$ and {{s}} successes in {{n}} trials, what is the posterior mean of $p$?",
              "s/n", "integrate(x**s*(1 - x)**(n - s - 1), (x, 0, 1))/integrate(x**(s - 1)*(1 - x)**(n - s - 1), (x, 0, 1))",
              "The posterior is Beta$(s, n - s)$, proper once there is at least one success and one failure; its mean is the sample proportion",
              given={"s": {"int": [2, 8]}, "n": {"int": [10, 20]}}, tex="E[p\\mid x]")]),
        L("C", "Update a beta prior with binomial data.", "Beta(a, b) + s successes in n → Beta(a + s, b + n − s).", ["ST9.3"], [
            q("st-beta-posterior", "stats.probability", "Prior $p \\sim \\text{Beta}({{a}}, {{b}})$; then {{s}} successes in {{n}} trials. What is the posterior mean?",
              "(a + s)/(a + b + n)", "integrate(x**(a + s)*(1 - x)**(b + n - s - 1), (x, 0, 1))/integrate(x**(a + s - 1)*(1 - x)**(b + n - s - 1), (x, 0, 1))",
              "Add successes to $a$ and failures to $b$. The posterior mean sits between the prior mean $a/(a + b)$ and the data $s/n$, pulled toward the data as $n$ grows",
              given={"a": {"int": [1, 5]}, "b": {"int": [1, 5]}, "s": {"int": [0, 8]}, "n": {"int": [8, 15]}}, require=["s <= n"], tex="E[p\\mid x]")]),
        L("D", "Find a normal posterior mean and credible interval.", "Posterior precision = prior precision + n/σ²; the mean is precision-weighted.", ["ST9.4"], [
            q("st-normal-posterior", "stats.probability", "Prior $\\mu \\sim N({{m0}}, {{t}}^2)$; data: {{n}} observations with mean {{xb}} and known $\\sigma = {{s}}$. What is the posterior mean of $\\mu$?",
              "(m0/t^2 + n*xb/s^2)/(1/t^2 + n/s^2)", "solve(Eq(x*(1/Integer(t)**2 + n/Integer(s)**2), m0/Integer(t)**2 + n*xb/Integer(s)**2), x)[0]",
              "Weight each source by its precision. A 95% credible interval is the posterior mean ± 1.96 posterior SDs, and it really is a probability statement about μ",
              given={"m0": {"int": [40, 60]}, "t": {"pick": [2, 5, 10]}, "n": {"pick": [4, 9, 25]}, "xb": {"int": [45, 70]}, "s": {"pick": [5, 10]}}, tex="\\mu_{post}", tol=0.0001)]),
        L("E", "Update odds with a Bayes factor.", "Posterior odds = prior odds × Bayes factor.", ["ST9.5"], [
            q("st-bayes-factor", "stats.probability", "Before the data, $P(H_1) = {{p}}$. The data give a Bayes factor of {{B}} for $H_1$ over $H_0$. What is $P(H_1 \\mid \\text{data})$?",
              "p/(1 - p)*B/(1 + p/(1 - p)*B)", "solve(Eq(x/(1 - x), nsimplify(p)/(1 - nsimplify(p))*B), x)[0]",
              "Turn the prior into odds, multiply by the Bayes factor, turn back into a probability. A Bayes factor of 10 is strong evidence but cannot rescue a very unlikely hypothesis",
              given={"p": {"pick": [0.1, 0.2, 0.5]}, "B": {"pick": [3, 10, 20]}}, tex="P", tol=0.0001)]),
    ]),
    ("Point estimation", [
        L("A", "Find the bias of an estimator.", "Bias = E[θ̂] − θ; the 1/n variance estimator has bias −σ²/n.", ["ST11.1"], [
            q("st-variance-bias", "stats.expected-value", "With $n = {{n}}$ and true variance {{v}}, what is the bias of $\\frac1n\\sum (x_i - \\bar x)^2$ as an estimator of $\\sigma^2$?",
              "-v/n", "(n - 1)*Rational(v, n) - v", "$E\\left[\\frac1n\\sum(x_i - \\bar x)^2\\right] = \\frac{n - 1}{n}\\sigma^2$, which is why $s^2$ divides by $n - 1$",
              given={"n": {"int": [4, 20]}, "v": {"pick": [4, 9, 16, 25]}}, tex="b")]),
        L("B", "Find the mean squared error of an estimator.", "MSE = bias² + variance; consistent when both go to 0.", ["ST11.2"], [
            q("st-mse", "stats.expected-value", "An estimator has $E[\\hat\\theta] = \\theta + {{c}}/n$ and $\\operatorname{Var}\\hat\\theta = {{v}}/n$. Find its MSE at $n = {{n}}$.",
              "(c/n)^2 + v/n", "(Rational(c, n))**2 + Rational(v, n)", "Both the bias and the variance shrink to 0 as $n$ grows, so the estimator is consistent even though it is biased",
              given={"c": {"int": [1, 5]}, "v": {"int": [2, 10]}, "n": {"pick": [5, 10, 20]}}, tex="MSE")]),
        L("C", "Identify a sufficient statistic.", "By factorisation, Σxᵢ is sufficient for the Poisson, exponential and Bernoulli families.", ["ST11.3"], [
            Q("st-sufficient", "stats.expected-value", "For an i.i.d. sample from {{q}}, which statistic is sufficient for the parameter?", pace="recall",
              cases=[{"q": "a Poisson(λ)", "ans": 0}, {"q": "a Bernoulli(p)", "ans": 0}, {"q": "a uniform on [0, θ]", "ans": 1}, {"q": "an exponential(λ)", "ans": 0}],
              choice=["The sum of the observations", "The largest observation", "The sample median"], correct="ans", verify="authored",
              explain="Write the likelihood and see what it depends on. For the uniform on [0, θ] it is $\\theta^{-n}$ when $\\theta \\ge \\max x_i$, so only the maximum matters")]),
        L("D", "Find a maximum likelihood estimate.", "Maximise the log-likelihood; for the exponential, λ̂ = 1/x̄.", ["ST11.4"], [
            q("st-mle-exponential", "stats.expected-value", "{{n}} lifetimes from an exponential distribution sum to {{S}} h. What is the MLE of the rate $\\lambda$, per hour?",
              "n/S", "solve(diff(n*log(x) - x*S, x), x)[0]", "$\\ell(\\lambda) = n\\ln\\lambda - \\lambda\\sum x_i$; $\\ell' = 0$ gives $\\hat\\lambda = n/\\sum x_i = 1/\\bar x$",
              given={"n": {"int": [5, 20]}, "S": {"pick": [100, 250, 500]}}, tex="\\hat\\lambda", tol=0.0001)]),
    ]),
]),
U(12, "time-series", "Time series", [
    ("Describing and modelling series", [
        L("A", "Smooth a series with a moving average.", "A centred 3-point average replaces each value by the mean of it and its neighbours.", ["ST10.1"], [
            q("st-moving-average", "stats.descriptive", "A series reads {{a}}, {{b}}, {{c}} at times 4, 5, 6. What is the centred 3-point moving average at time 5?",
              "(a + b + c)/3", "Rational(a + b + c, 3)", "Averaging over a window removes short wiggles; a window equal to the season length removes the seasonal pattern",
              given={"a": {"int": [10, 30]}, "b": {"int": [10, 30]}, "c": {"int": [10, 30]}}, tex="m_5")]),
        L("B", "Find the autocorrelation of an AR(1) process.", "ρₖ = φᵏ.", ["ST10.2"], [
            q("st-ar1-acf", "stats.descriptive", "A stationary AR(1) process $y_t = {{phi}}y_{t-1} + e_t$. What is its lag-{{k}} autocorrelation?",
              "phi^k", "nsimplify(phi)**k", "Each step multiplies the memory by φ, so correlation decays geometrically. A slowly decaying ACF hints at non-stationarity",
              given={"phi": {"pick": [-0.5, 0.3, 0.6, 0.8]}, "k": {"int": [1, 4]}}, tex="\\rho_k", tol=0.0001)]),
        L("C", "Find the variance of the number of runs.", "Var R = 2n₁n₂(2n₁n₂ − n₁ − n₂)/((n₁ + n₂)²(n₁ + n₂ − 1)).", ["ST10.3"], [
            q("st-runs-variance", "stats.descriptive", "Values above and below the median form a sequence with {{n1}} above and {{n2}} below. What is the variance of the number of runs?",
              "2*n1*n2*(2*n1*n2 - n1 - n2)/((n1 + n2)^2*(n1 + n2 - 1))", "Rational(2*n1*n2*(2*n1*n2 - n1 - n2), (n1 + n2)**2*(n1 + n2 - 1))",
              "Divide (runs − mean) by the square root of this for a z statistic; trends make too few runs",
              given={"n1": {"int": [6, 15]}, "n2": {"int": [6, 15]}}, tex="\\operatorname{Var}R")]),
        L("D", "Compute a seasonal index.", "Index = season's average / overall average.", ["ST10.4"], [
            q("st-seasonal-index", "stats.descriptive", "Quarterly sales average {{q1}}, {{q2}}, {{q3}} and {{q4}}. What is the seasonal index for Q{{j}}?",
              "j == 1 ? q1/((q1 + q2 + q3 + q4)/4) : (j == 2 ? q2/((q1 + q2 + q3 + q4)/4) : (j == 3 ? q3/((q1 + q2 + q3 + q4)/4) : q4/((q1 + q2 + q3 + q4)/4)))",
              "Matrix([q1, q2, q3, q4])[j - 1]*4/(q1 + q2 + q3 + q4)", "An index of 1.2 means that quarter runs 20% above average; deseasonalise by dividing by it",
              given={"q1": {"int": [80, 120]}, "q2": {"int": [90, 140]}, "q3": {"int": [100, 160]}, "q4": {"int": [70, 130]}, "j": {"int": [1, 4]}}, tex="S_j", tol=0.0001)]),
        L("E", "Find the variance of an AR(1) process.", "Var = σₑ²/(1 − φ²).", ["ST10.5"], [
            q("st-ar1-variance", "stats.descriptive", "$y_t = {{phi}}y_{t-1} + e_t$ with white noise of variance {{v}}. What is the stationary variance of $y_t$?",
              "v/(1 - phi^2)", f"v*summation(nsimplify(phi)**(2*{k_}), ({k_}, 0, oo))", "Write $y_t = \\sum \\phi^ke_{t-k}$ and add the variances: a geometric series in $\\phi^2$. It blows up as $|\\phi| \\to 1$",
              given={"phi": {"pick": [-0.5, 0.3, 0.6, 0.8]}, "v": {"pick": [1, 2, 4]}}, tex="\\gamma_0", tol=0.0001)]),
        L("F", "Forecast with simple exponential smoothing.", "F_{t+1} = αy_t + (1 − α)F_t.", ["ST10.6"], [
            q("st-exp-smoothing", "stats.descriptive", "With $\\alpha = {{a}}$, last forecast {{F}} and actual value {{y}}, what is the next forecast?",
              "a*y + (1 - a)*F", "F + nsimplify(a)*(y - F)", "The forecast moves a fraction α of the way toward the latest value: large α reacts fast, small α smooths more",
              given={"a": {"pick": [0.1, 0.2, 0.3, 0.5]}, "F": {"int": [80, 120]}, "y": {"int": [70, 130]}}, require=["y != F"], tex="F_{t+1}", tol=0.0001)]),
        L("G", "Convert a frequency to a period.", "A peak at frequency index k in N samples has period N/k samples.", ["ST10.7"], [
            q("st-periodogram", "stats.descriptive", "A periodogram of {{N}} monthly values peaks at frequency index $k = {{k}}$. What period does that cycle have, in months?",
              "N/k", "solve(Eq(x*k, N), x)[0]", "Frequency $k$ means $k$ full cycles across the record, so each lasts $N/k$ samples. Monthly data with a peak at $N/12$ cycles is the annual season",
              given={"N": {"pick": [120, 240, 360]}, "k": {"pick": [10, 20, 30, 40]}}, tex="T", pace="recall")]),
    ]),
]),
]
