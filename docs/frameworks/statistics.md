# Statistics — curriculum framework (draft 1)

Generated from `drills/frameworks/statistics.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**89 learning objectives** in 12 units (89 core): 89 drilled, 0 partly, 0 with no drills. Core: 89 / 89 drilled.

## Big ideas

- **MAIN · Variation is the subject.** Data vary, samples vary, and statistics is the craft of saying how much of what you see is signal. Every interval and test is a standard error and a multiplier.

## Practices

- **P1 · Compute and interpret.** Carry a statistic to a number and say in a sentence what it does and does not mean.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Exploring one-variable data and collecting data | core | — | 4 | 4 | 0 | 0 |
| 2 · Probability, random variables and distributions | core | — | 4 | 4 | 0 | 0 |
| 3 · Inference for categorical data: proportions | core | — | 3 | 3 | 0 | 0 |
| 4 · Inference for quantitative data: means | core | — | 1 | 1 | 0 | 0 |
| 5 · Regression analysis | core | — | 1 | 1 | 0 | 0 |
| 6 · Probability models | core | — | 19 | 19 | 0 | 0 |
| 7 · Survey sampling | core | — | 5 | 5 | 0 | 0 |
| 8 · Inference for means, proportions and variances | core | — | 16 | 16 | 0 | 0 |
| 9 · Inference in regression and generalised linear models | core | — | 12 | 12 | 0 | 0 |
| 10 · Nonparametric methods | core | — | 8 | 8 | 0 | 0 |
| 11 · Bayesian inference and point estimation | core | — | 9 | 9 | 0 | 0 |
| 12 · Time series | core | — | 7 | 7 | 0 | 0 |

## Unit 1 · Exploring one-variable data and collecting data

Big ideas: MAIN

### 1.1 Describing distributions



- ● **SS-1.1.A** (ap-statistics-2026:1, webwork-opl:ST3.2) Find and compare measures of centre and spread, and flag outliers.
  - EK: Mean and SD are pulled by extremes; median and IQR are not.
  - P1 · drills: stats-center, stats-outlier, mm-mean-focus, mm-median
- ● **SS-1.1.B** (ap-statistics-2026:1, webwork-opl:PB4.3, webwork-opl:PB4.4) Standardise a value and use the normal model.
  - EK: z = (x − μ)/σ; 68-95-99.7.
  - P1 · drills: sx-z-score, sx-empirical-rule, stats-normal

### 1.2 Collecting data



- ● **SS-1.2.A** (ap-statistics-2026:1, webwork-opl:ST2.6, webwork-opl:ST2.8) Identify the source of bias in a sampling method.
  - EK: Undercoverage, voluntary response, nonresponse, convenience, wording.
  - P1 · drills: sx-sampling-bias, hs-study-type
- ● **SS-1.2.B** (ap-statistics-2026:1, webwork-opl:ST1.1) Explain the purpose of random assignment, control, blinding and blocking.
  - EK: Random sampling generalises; random assignment supports cause.
  - P1 · drills: sx-experiment-design, hs-evaluate-report

## Unit 2 · Probability, random variables and distributions

Big ideas: MAIN

### 2.1 Probability rules



- ● **SS-2.1.A** (ap-statistics-2026:2, webwork-opl:PB1.2, webwork-opl:PB1.3, webwork-opl:PB1.4) Apply the addition and multiplication rules, conditional probability and independence.
  - EK: P(A or B) = P(A) + P(B) − P(A and B); P(A and B) = P(A)P(B|A).
  - P1 · drills: stats-addition, stats-mult-rule, stats-conditional, stats-independence, stats-bayes, stats-two-way

### 2.2 Random variables



- ● **SS-2.2.A** (ap-statistics-2026:2, webwork-opl:PB2.1, webwork-opl:PB2.2) Find the mean of a discrete random variable and of a linear transformation, and the spread of a sum.
  - EK: Means add; variances of independent variables add.
  - P1 · drills: stats-expected, stats-insurance, sx-linear-transform, sx-sum-of-independent
- ● **SS-2.2.B** (ap-statistics-2026:2, webwork-opl:PB3.1, webwork-opl:PB3.2, webwork-opl:PB3.4) Use the binomial and geometric distributions.
  - EK: Binomial: mean np, SD √(np(1−p)); geometric wait 1/p.
  - P1 · drills: sx-binomial-probability, sx-binomial-spread, sx-geometric-wait
- ● **SS-2.2.C** (ap-statistics-2026:2, webwork-opl:PB5.3, webwork-opl:ST4.1, webwork-opl:ST4.2) Find the standard deviation of a sample mean and of a sample proportion.
  - EK: σ/√n and √(p(1−p)/n).
  - P1 · drills: sx-standard-error-mean, sx-standard-error-proportion, sx-margin-and-sample-size

## Unit 3 · Inference for categorical data: proportions

Big ideas: MAIN

### 3.1 Intervals and tests for a proportion



- ● **SS-3.1.A** (ap-statistics-2026:3, webwork-opl:ST2.9, webwork-opl:ST5.1, webwork-opl:ST5.4) Build and interpret a confidence interval for a proportion and choose a sample size.
  - EK: p̂ ± z*√(p̂(1−p̂)/n).
  - P1 · drills: sx-proportion-margin, sx-sample-size-needed, sx-confidence-meaning, stats-margin
- ● **SS-3.1.B** (ap-statistics-2026:3, webwork-opl:ST6.1, webwork-opl:ST6.4) Carry out a z test for a proportion and state the conclusion.
  - EK: Use p₀ in the standard error; reject when p < α.
  - P1 · drills: sx-proportion-z-statistic, sx-p-value-decision, sx-error-types
- ● **SS-3.1.C** (ap-statistics-2026:3, webwork-opl:ST6.11, webwork-opl:ST6.12) Compute expected counts and the chi-square statistic for a table.
  - EK: E = row × column / total; χ² = Σ(O − E)²/E.
  - P1 · drills: sx-chi-square-expected, sx-chi-square-term, sx-degrees-of-freedom

## Unit 4 · Inference for quantitative data: means

Big ideas: MAIN

### 4.1 t procedures



- ● **SS-4.1.A** (ap-statistics-2026:4, webwork-opl:ST5.3, webwork-opl:ST6.3) Compute a t statistic and its degrees of freedom.
  - EK: t = (x̄ − μ₀)/(s/√n), df = n − 1.
  - P1 · drills: sx-t-statistic, sx-degrees-of-freedom

## Unit 5 · Regression analysis

Big ideas: MAIN

### 5.1 Least-squares lines



- ● **SS-5.1.A** (ap-statistics-2026:5, webwork-opl:ST7.1, webwork-opl:ST7.2, webwork-opl:ST7.3, webwork-opl:ST7.4) Find and interpret a correlation, a regression line, a residual and r².
  - EK: b = r·s_y/s_x; r² is the share of variation explained.
  - P1 · drills: stats-correlation, stats-regression, stats-residual, sx-r-squared, sx-slope-from-correlation, hs-trend-line

## Unit 6 · Probability models

Big ideas: MAIN

### 6.1 Random variables and their laws



- ● **SS-6.1.A** (webwork-opl:PB1.6) Convert between probability and odds.
  - EK: Odds in favour = p/(1 − p).
  - P1 · drills: st-odds, st-odds-against
- ● **SS-6.1.B** (webwork-opl:PB2.3) Find the median of a continuous distribution.
  - EK: Solve F(m) = 1/2.
  - P1 · drills: st-median-exponential, st-exp-percentile
- ● **SS-6.1.C** (webwork-opl:PB2.5) Use a density to find a probability and the CDF.
  - EK: P(a < X < b) = F(b) − F(a) = ∫ₐᵇ f.
  - P1 · drills: st-pdf-interval, st-normalising-constant
- ● **SS-6.1.D** (webwork-opl:PB2.6) Get a moment from a moment generating function.
  - EK: E[X] = M′(0), E[X²] = M″(0).
  - P1 · drills: st-mgf-mean, st-mgf-variance
- ● **SS-6.1.E** (webwork-opl:PB5.1) Bound a tail probability with Chebyshev's inequality.
  - EK: P(|X − μ| ≥ kσ) ≤ 1/k² for any distribution.
  - P1 · drills: st-chebyshev, st-chebyshev-k
- ● **SS-6.1.F** (webwork-opl:PB5.2) Choose a sample size from the weak law of large numbers.
  - EK: P(|X̄ − μ| ≥ ε) ≤ σ²/(nε²).
  - P1 · drills: st-lln-sample-size, st-lln-bound
- ● **SS-6.1.G** (webwork-opl:PB6.1, webwork-opl:PB6.2) Read joint and marginal probabilities from a table.
  - EK: Marginals are row or column sums; all cells sum to 1.
  - P1 · drills: st-joint-missing, st-conditional-from-table
- ● **SS-6.1.H** (webwork-opl:PB6.3) Compute a covariance from a joint table.
  - EK: Cov(X, Y) = E[XY] − E[X]E[Y].
  - P1 · drills: st-covariance-table, st-correlation-from-cov

### 6.2 Discrete distributions



- ● **SS-6.2.A** (webwork-opl:PB3.3) Approximate a binomial probability with the normal.
  - EK: μ = np, σ = √(np(1−p)), with a continuity correction of ½.
  - P1 · drills: st-normal-approx, st-normal-approx-upper
- ● **SS-6.2.B** (webwork-opl:PB3.5) Use the negative binomial distribution.
  - EK: P(rth success on trial n) = C(n−1, r−1) pʳ (1−p)ⁿ⁻ʳ.
  - P1 · drills: st-negative-binomial, st-negbin-variance
- ● **SS-6.2.C** (webwork-opl:PB3.6) Use the Poisson distribution.
  - EK: P(X = k) = e^{−λ} λᵏ / k!.
  - P1 · drills: st-poisson, st-poisson-rate-from-zero
- ● **SS-6.2.D** (webwork-opl:PB3.7) Use the hypergeometric distribution.
  - EK: Drawing without replacement: C(K,k)C(N−K,n−k)/C(N,n).
  - P1 · drills: st-hypergeometric, st-hypergeom-mean
- ● **SS-6.2.E** (webwork-opl:PB3.8) Use the multinomial distribution.
  - EK: n!/(a!b!c!) p₁ᵃ p₂ᵇ p₃ᶜ.
  - P1 · drills: st-multinomial, st-multinomial-cov
- ● **SS-6.2.F** (webwork-opl:PB7.2) Find the mean wait in an M/M/1 queue.
  - EK: W = 1/(μ − λ), L = λW (Little's law).
  - P1 · drills: st-mm1-wait, st-mm1-number

### 6.3 Continuous distributions



- ● **SS-6.3.A** (webwork-opl:PB4.1) Find the variance of a uniform distribution.
  - EK: Var = (b − a)²/12.
  - P1 · drills: st-uniform-variance, st-uniform-tail
- ● **SS-6.3.B** (webwork-opl:PB4.2) Use the exponential distribution.
  - EK: P(X > t) = e^{−λt}; memoryless.
  - P1 · drills: st-exponential-survival, st-memoryless
- ● **SS-6.3.C** (webwork-opl:PB4.5) Compute a Weibull reliability.
  - EK: R(t) = exp(−(t/η)^β); β < 1, = 1, > 1 for falling, constant, rising hazard.
  - P1 · drills: st-weibull, st-weibull-hazard
- ● **SS-6.3.D** (webwork-opl:PB4.6) Find the mean and variance of a gamma distribution.
  - EK: Gamma(k, θ): mean kθ, variance kθ².
  - P1 · drills: st-gamma-variance, st-gamma-mode
- ● **SS-6.3.E** (webwork-opl:PB4.7) Find the mean of a beta distribution.
  - EK: Beta(a, b) on [0, 1] has mean a/(a + b).
  - P1 · drills: st-beta-mean, st-beta-variance

## Unit 7 · Survey sampling

Big ideas: MAIN

### 7.1 Estimators from samples



- ● **SS-7.1.A** (webwork-opl:ST2.2) Estimate a total with a ratio estimator.
  - EK: Ŷ = (ȳ / x̄) X, using a known total of an auxiliary variable.
  - P1 · drills: st-ratio-estimator, st-ratio-mean
- ● **SS-7.1.B** (webwork-opl:ST2.3) Adjust a sample mean with a regression estimator.
  - EK: ȳ_reg = ȳ + b(X̄ − x̄).
  - P1 · drills: st-regression-estimator, st-regression-slope-back
- ● **SS-7.1.C** (webwork-opl:ST2.4) Combine strata into a stratified estimate.
  - EK: ȳ_st = Σ W_h ȳ_h with W_h = N_h / N.
  - P1 · drills: st-stratified-mean, st-proportional-allocation
- ● **SS-7.1.D** (webwork-opl:ST2.5) Estimate a total from a cluster sample.
  - EK: Ŷ = (N/n) Σ (cluster totals).
  - P1 · drills: st-cluster-total, st-cluster-per-element
- ● **SS-7.1.E** (webwork-opl:ST2.7) Estimate a population size by capture–recapture.
  - EK: N ≈ M C / R (Lincoln–Petersen).
  - P1 · drills: st-capture-recapture, st-recapture-expected

## Unit 8 · Inference for means, proportions and variances

Big ideas: MAIN

### 8.1 Confidence intervals



- ● **SS-8.1.A** (webwork-opl:ST5.2) Build a z interval for a mean.
  - EK: x̄ ± z* σ/√n.
  - P1 · drills: st-z-interval, st-n-for-margin
- ● **SS-8.1.B** (webwork-opl:ST5.5) Build an interval for a difference of proportions.
  - EK: p̂₁ − p̂₂ ± z* √(p̂₁q̂₁/n₁ + p̂₂q̂₂/n₂).
  - P1 · drills: st-two-prop-margin, st-n-two-prop
- ● **SS-8.1.C** (webwork-opl:ST5.6) Build an interval from paired data.
  - EK: Work with the differences: d̄ ± t* s_d/√n.
  - P1 · drills: st-paired-margin, st-sd-from-paired-margin
- ● **SS-8.1.D** (webwork-opl:ST5.7) Build a z interval for a difference of means.
  - EK: (x̄₁ − x̄₂) ± z* √(σ₁²/n₁ + σ₂²/n₂).
  - P1 · drills: st-two-z-margin, st-n-two-means
- ● **SS-8.1.E** (webwork-opl:ST5.8, webwork-opl:ST6.8) Find the standard error for two independent samples.
  - EK: SE = √(s₁²/n₁ + s₂²/n₂) (Welch).
  - P1 · drills: st-welch-t, st-welch-df
- ● **SS-8.1.F** (webwork-opl:ST5.9) Build a confidence interval for a variance.
  - EK: ((n−1)s²/χ²_upper, (n−1)s²/χ²_lower).
  - P1 · drills: st-variance-interval, st-sd-upper-bound

### 8.2 Hypothesis tests



- ● **SS-8.2.A** (webwork-opl:ST6.2) Compute a one-sample z statistic.
  - EK: z = (x̄ − μ₀)/(σ/√n).
  - P1 · drills: st-z-test, st-p-from-z
- ● **SS-8.2.B** (webwork-opl:ST6.5) Compute a two-proportion z statistic.
  - EK: Pool p̂ under H₀: z = (p̂₁ − p̂₂)/√(p̂(1−p̂)(1/n₁ + 1/n₂)).
  - P1 · drills: st-two-prop-z, st-pooled-prop
- ● **SS-8.2.C** (webwork-opl:ST6.6) Compute a paired t statistic.
  - EK: t = d̄/(s_d/√n) with n − 1 df.
  - P1 · drills: st-paired-t, st-paired-dbar-needed
- ● **SS-8.2.D** (webwork-opl:ST6.7) Compute a two-sample z statistic.
  - EK: z = (x̄₁ − x̄₂)/√(σ₁²/n₁ + σ₂²/n₂).
  - P1 · drills: st-two-z, st-diff-for-z
- ● **SS-8.2.E** (webwork-opl:ST6.9) Compute the power of a one-sided z test.
  - EK: Power = Φ(δ√n/σ − z_α) for a true shift δ.
  - P1 · drills: st-power, st-n-for-power
- ● **SS-8.2.F** (webwork-opl:ST6.10) Test a variance with the chi-square statistic.
  - EK: χ² = (n − 1)s²/σ₀².
  - P1 · drills: st-chi-variance, st-s2-for-chi
- ● **SS-8.2.G** (webwork-opl:ST6.13) Find the probability of a 2 × 2 table under Fisher's exact test.
  - EK: With margins fixed, the top-left cell is hypergeometric.
  - P1 · drills: st-fisher-table, st-fisher-mean
- ● **SS-8.2.H** (webwork-opl:ST6.14) Compare two variances with an F statistic.
  - EK: F = s₁²/s₂² with (n₁ − 1, n₂ − 1) df.
  - P1 · drills: st-f-variances, st-sd-ratio-for-f
- ● **SS-8.2.I** (webwork-opl:ST6.15) Compute a one-way ANOVA F statistic.
  - EK: F = MS_between / MS_within.
  - P1 · drills: st-anova-f, st-f-from-ss
- ● **SS-8.2.J** (webwork-opl:ST6.16) Count degrees of freedom in a two-way ANOVA.
  - EK: Factor A: a − 1; B: b − 1; interaction (a − 1)(b − 1); error ab(n − 1).
  - P1 · drills: st-twoway-df, st-twoway-error-df

## Unit 9 · Inference in regression and generalised linear models

Big ideas: MAIN

### 9.1 Simple and multiple regression



- ● **SS-9.1.A** (webwork-opl:ST7.5, webwork-opl:ST12.5) Test a regression slope.
  - EK: t = b/SE_b with n − 2 df.
  - P1 · drills: st-slope-t, st-t-from-r
- ● **SS-9.1.B** (webwork-opl:ST7.6, webwork-opl:ST12.4) Build an interval for a regression coefficient.
  - EK: b ± t* SE_b.
  - P1 · drills: st-slope-interval, st-se-from-interval
- ● **SS-9.1.C** (webwork-opl:ST7.7) Read a residual plot.
  - EK: Residuals should be a patternless band around zero.
  - P1 · drills: st-residual-diagnostics, st-residual-pattern
- ● **SS-9.1.D** (webwork-opl:ST12.1) Fit an exponential model by linearising.
  - EK: y = a e^{bx} ⇔ ln y = ln a + bx.
  - P1 · drills: st-linearised-fit, st-growth-percent
- ● **SS-9.1.E** (webwork-opl:ST12.2) Interpret an indicator variable.
  - EK: A 0/1 dummy shifts the intercept for one group.
  - P1 · drills: st-indicator, st-indicator-predict
- ● **SS-9.1.F** (webwork-opl:ST12.3) Predict from a fitted multiple regression.
  - EK: Plug each predictor into the fitted equation.
  - P1 · drills: st-multiple-predict, st-residual-multiple
- ● **SS-9.1.G** (webwork-opl:ST12.6) Compute an adjusted R².
  - EK: R²_adj = 1 − (1 − R²)(n − 1)/(n − k − 1).
  - P1 · drills: st-adjusted-r2, st-r2-from-adjusted
- ● **SS-9.1.H** (webwork-opl:ST12.7) Compare models with AIC.
  - EK: AIC = n ln(SSE/n) + 2k; smaller is better.
  - P1 · drills: st-aic, st-bic
- ● **SS-9.1.I** (webwork-opl:ST12.5) Compute an overall F statistic from R².
  - EK: F = (R²/k)/((1 − R²)/(n − k − 1)).
  - P1 · drills: st-overall-f, st-r2-from-f

### 9.2 Generalised linear models



- ● **SS-9.2.A** (webwork-opl:ST13.1) Predict a probability from a logistic regression.
  - EK: p = 1/(1 + e^{−(b₀ + b₁x)}); e^{b₁} is the odds ratio per unit x.
  - P1 · drills: st-logistic, st-logistic-odds-ratio
- ● **SS-9.2.B** (webwork-opl:ST13.2) Find an expected count under an independence loglinear model.
  - EK: μ_ij = (row total)(column total)/N.
  - P1 · drills: st-loglinear-expected, st-chi-contribution
- ● **SS-9.2.C** (webwork-opl:ST13.3) Use a proportional-odds (ordinal) model.
  - EK: P(Y ≤ j) = 1/(1 + e^{−(θⱼ − βx)}).
  - P1 · drills: st-ordinal, st-ordinal-middle

## Unit 10 · Nonparametric methods

Big ideas: MAIN

### 10.1 Rank and sign tests



- ● **SS-10.1.A** (webwork-opl:ST8.1) Find a sign-test p-value.
  - EK: Under H₀ the count of + signs is Binomial(n, ½).
  - P1 · drills: st-sign-test, st-sign-z
- ● **SS-10.1.B** (webwork-opl:ST8.2) Find the mean of the Wilcoxon rank-sum statistic.
  - EK: E[W] = n₁(N + 1)/2 under H₀.
  - P1 · drills: st-rank-sum-mean, st-rank-sum-var
- ● **SS-10.1.C** (webwork-opl:ST8.3) Find the mean of the Wilcoxon signed-rank statistic.
  - EK: E[W⁺] = n(n + 1)/4.
  - P1 · drills: st-signed-rank-mean, st-signed-rank-var
- ● **SS-10.1.D** (webwork-opl:ST8.4, webwork-opl:ST10.3) Find the expected number of runs.
  - EK: E[R] = 2n₁n₂/(n₁ + n₂) + 1.
  - P1 · drills: st-runs-mean, st-max-runs
- ● **SS-10.1.E** (webwork-opl:ST8.5) Compute the Kruskal–Wallis statistic.
  - EK: H = 12/(N(N+1)) Σ Rᵢ²/nᵢ − 3(N + 1).
  - P1 · drills: st-kruskal-wallis, st-kw-expected-rank-sum
- ● **SS-10.1.F** (webwork-opl:ST8.6) Compute a Kolmogorov–Smirnov statistic.
  - EK: D = max |F₁(x) − F₂(x)| over the data.
  - P1 · drills: st-ks-statistic, st-ks-critical
- ● **SS-10.1.G** (webwork-opl:ST8.8) Find the coverage of an order-statistic interval for a median.
  - EK: (x₍ₖ₎, x₍ₙ₋ₖ₊₁₎) covers the median with probability 1 − 2P(Bin(n, ½) ≤ k − 1).
  - P1 · drills: st-median-interval, st-median-beyond-max
- ● **SS-10.1.H** (webwork-opl:ST8.9) Know the relative efficiency of rank tests.
  - EK: Against the t test on normal data, the sign test has ARE 2/π ≈ 0.64 and the Wilcoxon 3/π ≈ 0.95.
  - P1 · drills: st-relative-efficiency, st-efficiency-facts

## Unit 11 · Bayesian inference and point estimation

Big ideas: MAIN

### 11.1 Bayesian inference



- ● **SS-11.1.A** (webwork-opl:ST9.1) Choose a conjugate prior.
  - EK: Beta for a binomial p, gamma for a Poisson rate, normal for a normal mean.
  - P1 · drills: st-conjugate-prior, st-conjugate-which
- ● **SS-11.1.B** (webwork-opl:ST9.2) Find a posterior mean under an improper prior.
  - EK: Beta(0, 0) is improper, but with data it gives the posterior Beta(s, n − s).
  - P1 · drills: st-improper-prior, st-flat-poisson-posterior
- ● **SS-11.1.C** (webwork-opl:ST9.3) Update a beta prior with binomial data.
  - EK: Beta(a, b) + s successes in n → Beta(a + s, b + n − s).
  - P1 · drills: st-beta-posterior, st-beta-posterior-mode
- ● **SS-11.1.D** (webwork-opl:ST9.4) Find a normal posterior mean and credible interval.
  - EK: Posterior precision = prior precision + n/σ²; the mean is precision-weighted.
  - P1 · drills: st-normal-posterior, st-normal-posterior-sd
- ● **SS-11.1.E** (webwork-opl:ST9.5) Update odds with a Bayes factor.
  - EK: Posterior odds = prior odds × Bayes factor.
  - P1 · drills: st-bayes-factor, st-bf-from-probs

### 11.2 Point estimation



- ● **SS-11.2.A** (webwork-opl:ST11.1) Find the bias of an estimator.
  - EK: Bias = E[θ̂] − θ; the 1/n variance estimator has bias −σ²/n.
  - P1 · drills: st-variance-bias, st-bias-mean-square
- ● **SS-11.2.B** (webwork-opl:ST11.2) Find the mean squared error of an estimator.
  - EK: MSE = bias² + variance; consistent when both go to 0.
  - P1 · drills: st-mse, st-mse-shrunk
- ● **SS-11.2.C** (webwork-opl:ST11.3) Identify a sufficient statistic.
  - EK: By factorisation, Σxᵢ is sufficient for the Poisson, exponential and Bernoulli families.
  - P1 · drills: st-sufficient, st-sufficient-which
- ● **SS-11.2.D** (webwork-opl:ST11.4) Find a maximum likelihood estimate.
  - EK: Maximise the log-likelihood; for the exponential, λ̂ = 1/x̄.
  - P1 · drills: st-mle-exponential, st-mle-geometric

## Unit 12 · Time series

Big ideas: MAIN

### 12.1 Describing and modelling series



- ● **SS-12.1.A** (webwork-opl:ST10.1) Smooth a series with a moving average.
  - EK: A centred 3-point average replaces each value by the mean of it and its neighbours.
  - P1 · drills: st-moving-average, st-centred-ma
- ● **SS-12.1.B** (webwork-opl:ST10.2) Find the autocorrelation of an AR(1) process.
  - EK: ρₖ = φᵏ.
  - P1 · drills: st-ar1-acf, st-phi-from-acf
- ● **SS-12.1.C** (webwork-opl:ST10.3) Find the variance of the number of runs.
  - EK: Var R = 2n₁n₂(2n₁n₂ − n₁ − n₂)/((n₁ + n₂)²(n₁ + n₂ − 1)).
  - P1 · drills: st-runs-variance, st-runs-var-equal
- ● **SS-12.1.D** (webwork-opl:ST10.4) Compute a seasonal index.
  - EK: Index = season's average / overall average.
  - P1 · drills: st-seasonal-index, st-deseasonalise
- ● **SS-12.1.E** (webwork-opl:ST10.5) Find the variance of an AR(1) process.
  - EK: Var = σₑ²/(1 − φ²).
  - P1 · drills: st-ar1-variance, st-ar1-noise
- ● **SS-12.1.F** (webwork-opl:ST10.6) Forecast with simple exponential smoothing.
  - EK: F_{t+1} = αy_t + (1 − α)F_t.
  - P1 · drills: st-exp-smoothing, st-ses-weight
- ● **SS-12.1.G** (webwork-opl:ST10.7) Convert a frequency to a period.
  - EK: A peak at frequency index k in N samples has period N/k samples.
  - P1 · drills: st-periodogram, st-angular-frequency

## Drills not yet placed on the map

- hs2-outlier-effect (stats.descriptive)
- hs2-causation (stats.descriptive)
- hs2-misleading-report (stats.descriptive)
- k8-scatter-association (stats.bivariate)
- g68-scatter-association (stats.bivariate)
- g68-trend-line-judge (stats.bivariate)
- hs2-two-way-marginal (stats.bivariate)
- hs2-model-type (stats.bivariate)
- hs2-residual-pattern (stats.bivariate)
- hs2-predict-line (stats.bivariate)
- stats-counting (stats.probability)
- mm-subsets (stats.probability)
- mm-two-dice (stats.probability)
- mm-combinations (stats.probability)
- mm-permutations (stats.probability)
- mm-dice-sum-prob (stats.probability)
- g68-simulation-design (stats.probability)
- hs-events-as-sets (stats.probability)
- hs-independence-in-words (stats.probability)
- hs-fair-decision (stats.probability)
- hs-model-consistent (stats.probability)
- hs2-independence-check (stats.probability)
- hs2-conditional-table (stats.probability)
- hs2-conditional-words (stats.probability)
- hs2-without-replacement (stats.probability)
- hs2-fair-decision (stats.probability)
- hs2-positive-predictive (stats.probability)
- k8-simulation-estimate (stats.probability)
- hs-empirical-distribution (stats.expected-value)
- hs2-random-variable (stats.expected-value)
- hs2-empirical-mean (stats.expected-value)
- hs2-raffle-ev (stats.expected-value)
- hs2-strategy-ev (stats.expected-value)
