# Statistics — curriculum framework (draft 1)

Generated from `drills/frameworks/statistics.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**13 learning objectives** in 5 units (13 core): 13 drilled, 0 partly, 0 with no drills. Core: 13 / 13 drilled.

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
