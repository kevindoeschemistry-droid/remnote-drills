# Financial Accounting (CPA FAR) — curriculum framework (draft 1)

Generated from `drills/frameworks/accounting-far.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**26 learning objectives** in 3 units (26 core): 26 drilled, 0 partly, 0 with no drills. Core: 26 / 26 drilled.

## Big ideas

- **ACCR · Accrual accounting matches effects to periods.** Revenue when earned, expenses when incurred, estimates revised prospectively, errors restated.
- **MEAS · Each item has a measurement basis.** Cost, amortized cost, fair value, net realizable value or present value, and the choice decides where changes are reported.
- **PRES · Presentation tells users where to look.** Which statement, which section, which class of net assets or fund an item lands in is itself information.

## Practices

- **P1 · Compute.** Carry an accounting measurement to a number.
- **P2 · Classify.** Put an item in the right statement, section, class, level or treatment.
- **P3 · Apply the rule.** State what GAAP requires in a situation.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Financial reporting | core | — | 9 | 9 | 0 | 0 |
| 2 · Select balance sheet accounts | core | — | 10 | 10 | 0 | 0 |
| 3 · Select transactions | core | — | 7 | 7 | 0 | 0 |

## Unit 1 · Financial reporting

Big ideas: PRES, ACCR

### 1.1 For-profit financial statements



- ● **FA-1.1.A** (cpa-far:I.A) Place an item in the statement where it is reported.
  - EK: A short list of unrealized items goes to OCI; owner transactions to the statement of changes in equity.
  - P2 · drills: fa-statement-home
- ● **FA-1.1.B** (cpa-far:I.A) Classify cash flows and compute operating cash flow by the indirect method and cash collected from customers.
  - EK: Interest paid and dividends received are operating under US GAAP.
  - Needs: FA-1.1.A
  - P1 · P2 · drills: fa-cf-class, fa-cfo-indirect, fa-cash-collected
- ● **FA-1.1.C** (cpa-far:I.A) Compute goodwill, the noncontrolling interest's share of income, and intercompany profit to eliminate in consolidation.
  - EK: Goodwill = consideration + NCI fair value − net identifiable assets.
  - Needs: FA-1.1.B
  - P1 · drills: fa-goodwill, fa-nci-income, fa-intercompany-profit

### 1.2 Not-for-profit entities



- ● **FA-1.2.A** (cpa-far:I.B) Classify contributions and releases between net assets with and without donor restrictions.
  - EK: Only donors restrict; board designations do not.
  - Needs: FA-1.1.C
  - P2 · drills: fa-nfp-net-assets

### 1.3 State and local government



- ● **FA-1.3.A** (cpa-far:I.C) Give the measurement focus and basis for each fund type and the government-wide statements, and pick the fund for an activity.
  - EK: Governmental funds: current financial resources, modified accrual.
  - Needs: FA-1.2.A
  - P2 · drills: fa-gov-basis, fa-fund-purpose

### 1.4 Public companies and special purpose frameworks



- ● **FA-1.4.A** (cpa-far:I.D) Name SEC filings and the segment reporting thresholds.
  - EK: 10-K, 10-Q, 8-K; 10% tests, 75% coverage.
  - Needs: FA-1.3.A
  - P3 · drills: fa-public-reporting
- ● **FA-1.4.B** (cpa-far:I.E) Apply the cash, modified cash and tax bases.
  - EK: Describe the basis and its differences from GAAP.
  - Needs: FA-1.4.A
  - P3 · drills: fa-special-framework

### 1.5 Ratios and performance metrics



- ● **FA-1.5.A** (cpa-far:I.F) Compute liquidity and activity ratios: current, quick, days in receivables and days in inventory.
  - EK: Turnover uses averages; days = 365 ÷ turnover.
  - Needs: FA-1.4.B
  - P1 · drills: fa-current-ratio, fa-quick-ratio, fa-ar-turnover, fa-inventory-days
- ● **FA-1.5.B** (cpa-far:I.F, cpa-far:I.A) Compute weighted-average shares and basic EPS.
  - EK: Subtract preferred dividends; weight shares by time outstanding.
  - Needs: FA-1.5.A
  - P1 · drills: fa-eps, fa-weighted-shares

## Unit 2 · Select balance sheet accounts

Big ideas: MEAS

### 2.1 Cash and receivables



- ● **FA-2.1.A** (cpa-far:II.A) Decide what counts as a cash equivalent and reconcile a bank balance.
  - EK: Original maturity of three months or less.
  - Needs: FA-1.5.B
  - P1 · P2 · drills: fa-cash-equivalent, fa-bank-rec
- ● **FA-2.1.B** (cpa-far:II.B) Estimate the allowance for credit losses and bad debt expense.
  - EK: The expense brings the allowance to its required balance.
  - Needs: FA-2.1.A
  - P1 · drills: fa-allowance, fa-aging

### 2.2 Inventory



- ● **FA-2.2.A** (cpa-far:II.C) Cost ending inventory by FIFO, LIFO and weighted average, apply lower of cost and NRV, and estimate it by the gross profit method.
  - EK: Rising prices: FIFO gives the highest ending inventory.
  - Needs: FA-2.1.B
  - P1 · drills: fa-inventory-flow, fa-lcnrv, fa-gross-profit-method

### 2.3 Property, plant and equipment



- ● **FA-2.3.A** (cpa-far:II.D) Compute straight-line, double-declining-balance and sum-of-the-years'-digits depreciation, a disposal gain or loss, and depreciation after a change in estimate.
  - EK: Estimates change prospectively.
  - Needs: FA-2.2.A
  - P1 · drills: fa-dep-sl, fa-dep-ddb, fa-dep-syd, fa-disposal, fa-change-estimate
- ● **FA-2.3.B** (cpa-far:II.D) Compute interest capitalized during construction.
  - EK: Avoidable interest, capped at actual.
  - Needs: FA-2.3.A
  - P1 · drills: fa-capitalized-interest

### 2.4 Investments



- ● **FA-2.4.A** (cpa-far:II.E) Choose the measurement for a debt or equity investment and apply the equity method.
  - EK: Trading FV-NI, AFS FV-OCI, HTM amortized cost; 20–50% equity method.
  - Needs: FA-2.3.B
  - P1 · P2 · drills: fa-investment-class, fa-equity-method

### 2.5 Intangible assets



- ● **FA-2.5.A** (cpa-far:II.F) Measure a goodwill impairment.
  - EK: Carrying amount over fair value, capped at goodwill.
  - Needs: FA-2.4.A
  - P1 · drills: fa-goodwill-impairment

### 2.6 Payables and debt



- ● **FA-2.6.A** (cpa-far:II.G) Accrue interest on a note payable.
  - EK: Principal × rate × time.
  - Needs: FA-2.5.A
  - P1 · drills: fa-accrued-interest
- ● **FA-2.6.B** (cpa-far:II.H) Price a bond and amortize its discount or premium by the effective interest method.
  - EK: Expense at the market rate on carrying amount; cash at the coupon rate on face.
  - Needs: FA-2.6.A
  - P1 · drills: fa-bond-price, fa-bond-amortization

### 2.7 Equity



- ● **FA-2.7.A** (cpa-far:II.I) Record a stock dividend and roll retained earnings forward, including a prior-period adjustment.
  - EK: Small stock dividends at fair value; error corrections adjust opening retained earnings.
  - Needs: FA-2.6.B
  - P1 · drills: fa-stock-dividend, fa-retained-earnings

## Unit 3 · Select transactions

Big ideas: ACCR, MEAS

### 3.1 Changes, contingencies and subsequent events



- ● **FA-3.1.A** (cpa-far:III.A) Tell a change in principle, a change in estimate and an error correction apart, and say how each is reported.
  - EK: Retrospective, prospective, restatement.
  - Needs: FA-2.7.A
  - P2 · drills: fa-accounting-change
- ● **FA-3.1.B** (cpa-far:III.B) Decide whether to accrue, disclose or ignore a contingency.
  - EK: Probable and estimable → accrue; a range → best estimate or minimum.
  - Needs: FA-3.1.A
  - P3 · drills: fa-contingency
- ● **FA-3.1.C** (cpa-far:III.G) Decide whether a subsequent event is recognized or only disclosed.
  - EK: Conditions existing at the balance-sheet date are recognized.
  - Needs: FA-3.1.B
  - P2 · drills: fa-subsequent-event

### 3.2 Revenue recognition



- ● **FA-3.2.A** (cpa-far:III.C) Order the five steps, allocate a price by standalone selling prices, estimate variable consideration, and recognize revenue over time.
  - EK: Cost-to-cost: cumulative revenue minus what earlier years recognized.
  - Needs: FA-3.1.C
  - P1 · P3 · drills: fa-revenue-steps, fa-ssp-allocation, fa-expected-value, fa-over-time

### 3.3 Income taxes



- ● **FA-3.3.A** (cpa-far:III.D) Classify temporary and permanent differences and measure a deferred tax liability at the enacted rate.
  - EK: Use the rate enacted for the reversal years.
  - Needs: FA-3.2.A
  - P1 · P2 · drills: fa-temp-perm, fa-deferred-tax

### 3.4 Fair value



- ● **FA-3.4.A** (cpa-far:III.E) Place a valuation input in the fair value hierarchy.
  - EK: Level 1 quoted identical, Level 2 observable, Level 3 unobservable.
  - Needs: FA-3.3.A
  - P2 · drills: fa-fair-value-level

### 3.5 Lessee accounting



- ● **FA-3.5.A** (cpa-far:III.F) Classify a lease as finance or operating and measure the lease liability.
  - EK: Five tests; liability = PV of remaining payments.
  - Needs: FA-3.4.A
  - P1 · P2 · drills: fa-lease-class, fa-lease-liability
