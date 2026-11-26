# Process Design, Economics and Safety — curriculum framework (draft 1)

Generated from `drills/frameworks/process-design.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**62 learning objectives** in 10 units (9 core): 62 drilled, 0 partly, 0 with no drills. Core: 9 / 9 drilled.

## Big ideas

- **MONEY · Money has a time value.** A dollar later is worth less than a dollar now; every economic comparison discounts to one date.
- **LAYERS · Safety is layers.** Keep fuel out of its flammable range, exposures under their limits, and find deviations before they happen.
- **SOLIDS · A powder is not a fluid.** A solid stream is described by a distribution, not a single size, and it flows, grinds and dissolves by its own rules.
- **DOCS · A plant is built from documents.** What a drawing shows, and what accuracy an estimate claims, decide what can be built and what it will cost.
- **DUTY · The duty is to the public first.** An engineer's obligations are ordered, and the public's safety outranks the client, the employer and the engineer.
- **DYN · Processes respond with a lag.** A first-order process reaches 63% of a step change in one time constant; control design starts there.

## Practices

- **P1 · Compute.** Carry the calculation to a number.
- **P2 · Judge.** Decide whether a design or exposure is acceptable.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Engineering economics | core | — | 5 | 5 | 0 | 0 |
| 2 · Process safety | core | — | 3 | 3 | 0 | 0 |
| 3 · Process dynamics | core | — | 1 | 1 | 0 | 0 |
| 4 · Particle technology | extension | — | 11 | 11 | 0 | 0 |
| 5 · Plant documents and design practice | extension | — | 7 | 7 | 0 | 0 |
| 6 · Pressure relief and loss prevention | extension | — | 9 | 9 | 0 | 0 |
| 7 · Professional practice | extension | — | 7 | 7 | 0 | 0 |
| 8 · Measurement, uncertainty and project selection | extension | — | 6 | 6 | 0 | 0 |
| 9 · Statistics in engineering units | extension | — | 7 | 7 | 0 | 0 |
| 10 · Control strategies and hardware | extension | — | 6 | 6 | 0 | 0 |

## Unit 1 · Engineering economics

Big ideas: MONEY

### 1.1 Time value of money



- ● **PD-1.1.A** Convert a nominal rate to an effective annual rate.
  - EK: (1 + r/m)^m − 1.
  - P1 · drills: pd-effective-rate, pd-nominal-from-effective
- ● **PD-1.1.B** (icheme-level-f:A2.7) Compute a project's net present value.
  - EK: NPV = −I + A(P/A,i,n) + S(1+i)⁻ⁿ.
  - Needs: PD-1.1.A
  - P1 · drills: pd-npv, pd-capital-recovery
- ● **PD-1.1.C** Compute a simple payback period.
  - EK: Cumulative cash flow covers the investment.
  - P1 · drills: pd-payback, pd-roi

### 1.2 Costs



- ● **PD-1.2.A** Scale an equipment cost by capacity and cost index.
  - EK: C₂ = C₁(S₂/S₁)^0.6 × I₂/I₁.
  - P1 · drills: pd-cost-scaling, pd-capacity-from-budget
- ● **PD-1.2.B** Compute book value under straight-line or declining-balance depreciation.
  - EK: SL (P − S)/n; DDB 2/n of book value.
  - P1 · drills: pd-depreciation, pd-soyd

## Unit 2 · Process safety

Big ideas: LAYERS

### 2.1 Hazards



- ● **PD-2.1.C** (fe-chemical:16.C, icheme-level-f:A2.6) State what a HAZOP guide word means.
  - EK: NO, MORE, LESS, REVERSE, AS WELL AS, PART OF, OTHER THAN.
  - P2 · drills: pd-hazop, pd-hazop-word
- ● **PD-2.1.A** (fe-chemical:16.A, aiche-bok:X.SAFE) Compute the lower flammable limit of a fuel mixture.
  - EK: Le Chatelier: 1/Σ(yᵢ/LFLᵢ).
  - P1 · drills: pd-lfl-mixture, pd-flammable-check
- ● **PD-2.1.B** (fe-chemical:16.B, aiche-bok:X.SAFE) Judge a mixed exposure against its limits.
  - EK: Σ Cᵢ/TLVᵢ ≤ 1.
  - P2 · drills: pd-tlv-mixture, pd-tlv-allowance

## Unit 3 · Process dynamics

Big ideas: DYN

### 3.1 First-order systems



- ● **PD-3.1.A** Compute the step response of a first-order process.
  - EK: y = KΔu(1 − e^(−t/τ)).
  - P1 · drills: pd-first-order, pd-time-constant-from-data

## Unit 4 · Particle technology (extension)

Big ideas: SOLIDS

### 4.1 Describing a powder



- ● **PD-4.1.A** (fe-chemical:11.A) State what a particle-size distribution is and which mean a stated application needs
  - EK: A powder has a distribution of sizes, so a single number is always a particular kind of average: the arithmetic mean, the volume or mass mean, and the Sauter (surface-volume) mean answer different questions, and the Sauter mean is the one that carries surface area per unit volume.
  - P2 · drills: pd-which-mean, pd-mass-fraction-cut
- ● **PD-4.1.B** (fe-chemical:11.A) Compute the Sauter mean diameter of a stated size distribution
  - EK: The Sauter mean is the diameter of the uniform sphere set with the same surface area per unit volume as the real powder: the sum of n_i d_i cubed over the sum of n_i d_i squared.
  - P1 · drills: pd-sauter, pd-arith-vs-sauter
- ● **PD-4.1.C** (fe-chemical:11.A) Compute voidage and bulk density from particle density and the other of the two
  - EK: Bulk density is the particle density times one minus the voidage, so measuring two of the three gives the third; a powder's bulk density is not a material property because it depends on how it was poured and settled.
  - P1 · drills: pd-voidage, pd-bulk-from-voidage
- ● **PD-4.1.D** (fe-chemical:11.A) Convert between a sieve mesh number and an aperture, and state which fraction a stated cut holds
  - EK: A sieve stack reports mass fractions between successive apertures; a mesh number counts wires per inch, so a larger mesh number is a smaller aperture and the two run in opposite directions.
  - P1 · drills: pd-mesh-direction, pd-cut-between

### 4.2 Size reduction and crystallization



- ● **PD-4.2.A** (fe-chemical:11.B) Compute the size-reduction energy from Rittinger's, Kick's or Bond's law
  - EK: The three laws differ in what they take the energy to be proportional to: new surface created (Rittinger, fine grinding), size ratio (Kick, coarse crushing), or the Bond work index with the reciprocal square roots of the sizes (intermediate, the one used for mills).
  - P1 · drills: pd-bond-energy, pd-grind-finer
- ● **PD-4.2.B** (fe-chemical:11.B) State which size-reduction law fits a stated duty and what the work index means
  - EK: The Bond work index is the energy in kilowatt-hours per ton to take a very large feed to eighty per cent passing 100 micrometres, so it is a measured property of the material that makes mill duties comparable.
  - P2 · drills: pd-which-law, pd-work-index-back
- ● **PD-4.2.C** (fe-chemical:11.B) Compute a crystallization yield from solubilities, cooling and evaporation
  - EK: The yield is what the solution can no longer hold: solute in minus solute still dissolved in the mother liquor at the final temperature, with water removed by evaporation reducing the amount the liquor can hold, and with the hydrate's water of crystallization counted in the crystal mass.
  - P1 · drills: pd-crystal-yield, pd-crystal-evap
- ● **PD-4.2.D** (fe-chemical:11.B) State what supersaturation controls in a crystallizer and what the crystal-size trade-off is
  - EK: Supersaturation drives both nucleation and growth, and nucleation rises faster with it, so a high supersaturation gives many small crystals and a low one, held steady, gives fewer large ones: product size is a control decision, not a material constant.
  - P2 · drills: pd-supersaturation, pd-nucleation-ratio

### 4.3 Handling and storage



- ● **PD-4.3.A** (fe-chemical:11.C) Compute the capacity of a belt or screw conveyor from its loading and speed
  - EK: A conveyor's capacity is the cross-section it carries times belt speed times bulk density, which is why a bulk density change at the same volumetric setting changes the mass rate.
  - P1 · drills: pd-conveyor-capacity, pd-conveyor-density-change
- ● **PD-4.3.B** (fe-chemical:11.C) State what the angle of repose and a mass-flow versus funnel-flow hopper mean for storage
  - EK: The angle of repose is the slope a poured heap stands at; a hopper steeper than the material's flow requirement runs in mass flow, where all the contents move, while a shallower one runs in funnel flow, where a central channel empties and the rest stays and can cake or arch.
  - P2 · drills: pd-hopper-flow, pd-repose-height
- ● **PD-4.3.C** (fe-chemical:11.C) Compute the dust-explosion and dilution-air quantities a stated solids handling duty needs
  - EK: A combustible dust cloud between its minimum explosible concentration and its upper limit will propagate given an ignition source and confinement, so a dust duty is designed by keeping the cloud out of that band and by relieving or suppressing what cannot be kept out.
  - P1 · drills: pd-dust-concentration, pd-dilution-air

## Unit 5 · Plant documents and design practice (extension)

Big ideas: DOCS

### 5.1 Drawings and documents



- ● **PD-5.1.A** (fe-chemical:14.A, cheme-grad-core:PS.3, aiche-bok:T.DES) State what a block flow diagram, a process flow diagram and a P&ID each show
  - EK: A block flow diagram shows the blocks and the streams between them; a process flow diagram adds the major equipment, its tags and a stream table of flows, compositions and conditions; a P&ID adds every line with its size and material, every valve and instrument, and the interlocks, and it is the document the plant is built and operated from.
  - P2 · drills: pd-which-drawing, pd-drawing-detail-count
- ● **PD-5.1.B** (fe-chemical:14.A, cheme-grad-core:PS.3, aiche-bok:T.BAL) Read a stream table and compute the missing entry from the balance
  - EK: A stream table is a material balance written out, so a missing flow or composition follows from closing the balance round the unit it belongs to; an entry that does not close is an error in the table, not a property of the process.
  - P1 · drills: pd-stream-close, pd-stream-composition
- ● **PD-5.1.C** (fe-chemical:14.A, aiche-bok:T.INST) State what an instrument tag's letters mean and what a control loop on a P&ID consists of
  - EK: An instrument tag's first letter is the measured variable and the following letters are the function, so FIC is a flow indicating controller and LT a level transmitter; a loop on the drawing is a transmitter, a controller and a final control element sharing one tag number.
  - P2 · drills: pd-instrument-tag, pd-loop-count

### 5.2 Sizing, scale-up and standards



- ● **PD-5.2.A** (fe-chemical:14.B, aiche-bok:T.DES, aiche-bok:T.SU) Scale an equipment cost with the six-tenths rule and a cost index
  - EK: Capacity scaling uses an exponent near 0.6 because cost follows surface and capacity follows volume, and a cost from another year is brought forward by the ratio of cost indices; the two corrections are independent and both are needed.
  - P1 · drills: pd-six-tenths, pd-cost-index
- ● **PD-5.2.B** (fe-chemical:14.B, aiche-bok:T.DES) Compute an installed cost from a bare-module or Lang factor and state what it covers
  - EK: A factor multiplies purchased equipment cost to cover installation, piping, instruments, electrical, structures and indirect costs, so a quoted equipment price is a fraction of the capital a plant needs; the factor depends on whether the plant handles fluids, solids or both.
  - P1 · drills: pd-bare-module, pd-factor-from-total
- ● **PD-5.2.C** (fe-chemical:14.D, icheme-level-f:A2.7) State what an estimate class claims and compute a contingency from a stated accuracy band
  - EK: An estimate's class states both the design definition behind it and the accuracy range it claims, which widens as definition falls; contingency is money for what is known to be missing at that definition, not for scope that has not been decided.
  - P1 · drills: pd-contingency, pd-estimate-class
- ● **PD-5.2.D** (fe-chemical:14.E, aiche-bok:X.SAFE) State what a design standard or code fixes and who is bound by it
  - EK: A code such as the pressure-vessel code is adopted into law by a jurisdiction and fixes minimum requirements for design, fabrication, inspection and stamping, so a vessel's thickness is not purely the designer's choice; a standard such as a pump or flange standard fixes dimensions so that parts from different makers interchange.
  - P2 · drills: pd-code-vs-standard, pd-thickness-code

## Unit 6 · Pressure relief and loss prevention (extension)

Big ideas: LAYERS

### 6.1 Relief device sizing



- ● **PD-6.1.A** (fe-chemical:16.D, icheme-level-f:A2.6, aiche-bok:X.SAFE) State the accumulation a relief device may allow above the maximum allowable working pressure
  - EK: A single relief device is set at or below the maximum allowable working pressure and the accumulated pressure may reach 110 per cent of it for a non-fire case, 116 per cent where multiple devices are installed and 121 per cent for the fire case; those are the numbers that separate a protected vessel from a burst one.
  - P1 · drills: pd-accumulation, pd-accumulation-which
- ● **PD-6.1.B** (fe-chemical:16.D) Size a vapour relief area from the printed sizing equation and the stated coefficients
  - EK: The required area rises with the relieving rate and the square root of temperature over molecular weight, and falls with the relieving pressure: a relief valve sized for one fluid and set pressure is not transferable to another.
  - P1 · drills: pd-relief-area, pd-relief-area-scale
- ● **PD-6.1.C** (fe-chemical:16.D) Compute the fire-case relief duty from the printed wetted-area correlation
  - EK: The fire case takes heat input from the wetted area of the vessel, so the relief load is the heat absorbed divided by the latent heat of the contents: a vessel's worst relief case is often a fire outside it rather than any process upset.
  - P1 · drills: pd-fire-relief, pd-fire-insulation-credit
- ● **PD-6.1.D** (fe-chemical:16.D, icheme-level-f:A2.6) Choose between a relief valve, a rupture disc and both in series for a stated duty
  - EK: A relief valve recloses and can be tested, a rupture disc opens fully, does not reclose and tolerates corrosive or polymerising service, and the two in series protect the valve while still relieving; a disc's burst pressure carries a manufacturing tolerance that the set pressure must allow for.
  - P2 · drills: pd-valve-or-disc, pd-disc-tolerance

### 6.2 Underpressure and containment



- ● **PD-6.2.A** (fe-chemical:16.D) Compute the external-pressure condition a vessel must withstand and when full vacuum is specified
  - EK: A vessel emptied against a closed vent, or steamed out and cooled, pulls a vacuum, and a vessel designed only for internal pressure buckles well below one atmosphere of external pressure, so the usual answer is to design for full vacuum or to fit a vacuum breaker.
  - P1 · drills: pd-vacuum-cooling, pd-underpressure
- ● **PD-6.2.B** (fe-chemical:16.E) State where a relieved stream may be discharged and what the containment choice depends on
  - EK: What leaves a relief device still has to go somewhere: to atmosphere only where the discharge is safe at grade and in the plume, otherwise to a flare, a scrubber or a knockout drum and catch tank, chosen on the stream's toxicity, flammability and whether it is two-phase.
  - P2 · drills: pd-relief-destination, pd-knockout-liquid

### 6.3 Reactivity and waste



- ● **PD-6.3.A** (fe-chemical:16.F, icheme-level-f:A2.6) Compute the adiabatic temperature rise of a runaway and the time to maximum rate
  - EK: The adiabatic temperature rise is the heat of reaction over the heat capacity, and it is a property of the charge rather than of the vessel, so a reaction whose adiabatic rise exceeds the margin to the vessel's limit cannot be made safe by cooling alone.
  - P1 · drills: pd-adiabatic-rise, pd-margin-to-limit
- ● **PD-6.3.B** (fe-chemical:16.F, icheme-level-f:A2.6) State which reactivity hazards a stated material pairing creates
  - EK: Incompatible pairings generate heat, gas or a toxic product on mixing, so segregation, bunding and separate transfer lines are design decisions, and a compatibility chart is consulted before a drain or a vent is shared.
  - P2 · drills: pd-incompatible, pd-segregation-pairs
- ● **PD-6.3.C** (fe-chemical:16.E, icheme-level-f:A2.7) Compute a waste-minimisation or treatment duty from a stated discharge limit
  - EK: A discharge limit is a concentration or a load, so meeting it is either removing material or reducing the volume it is carried in; the cheapest route is almost always not generating it, since every treated stream is paid for twice.
  - P1 · drills: pd-waste-dilution-limit, pd-waste-load-reduction

## Unit 7 · Professional practice (extension)

Big ideas: DUTY

### 7.1 The ordered duties



- ● **PD-7.1.A** (nspe-ethics:C1, nspe-ethics:R1, icheme-level-f:A2.7) State which duty governs when a stated situation puts the public's safety against another obligation
  - EK: The canons are ordered: the public's safety, health and welfare is held paramount, so where loyalty to an employer, a contract or the engineer's own interest conflicts with it, the public's interest wins and the route is to escalate rather than to go along.
  - P2 · drills: pd-paramount, pd-report-violation
- ● **PD-7.1.C** (nspe-ethics:C4, nspe-ethics:R4, nspe-ethics:O5) Identify the conflict of interest in a stated arrangement and what disclosure it requires
  - EK: A conflict of interest is disclosed to all affected parties rather than privately managed, double compensation for the same work needs everyone's consent, and gifts or commissions from suppliers are refused because the test is influence, not whether the decision in fact changed.
  - P2 · drills: pd-coi, pd-coi-scenario
- ● **PD-7.1.D** (nspe-ethics:O4, nspe-ethics:R1) Decide what a stated piece of client or employer information may be used for
  - EK: Confidential information is not disclosed without consent and is not used to win other work or to act against the former client, which binds an engineer after leaving as well as while employed.
  - P2 · drills: pd-confidential-use, pd-confidential-scenario
- ● **PD-7.1.B** (nspe-ethics:C2, nspe-ethics:R2) Decide whether a stated assignment or signature is within an engineer's competence
  - EK: An engineer accepts and seals only work in their own field of competence, and on a large project seals only the technical segments they prepared or directly supervised, which is why a stamp is a professional claim and not a formality.
  - P2 · drills: pd-competence-scope, pd-seal-segments

### 7.2 Agreements and intellectual property



- ● **PD-7.2.C** (nspe-ethics:O9) Decide who owns a stated design or work product and who must be credited
  - EK: Work produced in employment generally belongs to the employer and a client's designs stay the client's, so ownership is settled in advance in writing; credit is a separate duty from ownership and is given to whoever did the work.
  - P2 · drills: pd-ownership, pd-ownership-scenario
- ● **PD-7.2.A** (fe-chemical:17.B, icheme-level-f:A2.7) State what makes an agreement binding and which term in a stated contract carries the risk
  - EK: An agreement needs an offer, acceptance and consideration between parties competent to contract for a lawful purpose; the terms that carry the engineering risk are scope, the standard of care, indemnity and limitation of liability, and a signed scope decides what extra work is a change order.
  - P2 · drills: pd-contract-basics, pd-change-order
- ● **PD-7.2.B** (fe-chemical:17.D) Choose the intellectual-property protection a stated creation needs and state its term
  - EK: A utility patent protects an invention for twenty years from filing in exchange for publishing it, a copyright protects an expression without registration, a trademark protects a mark in use indefinitely while it is used, and a trade secret lasts only while it is kept secret, which is why publishing destroys it.
  - P2 · drills: pd-ip-kind, pd-patent-expiry

## Unit 8 · Measurement, uncertainty and project selection (extension)

Big ideas: DOCS

### 8.1 Significant figures and propagation



- ● **PD-8.1.A** (fe-chemical:1.F) Report a computed result to the right number of significant figures
  - EK: A product or quotient carries the significant figures of its least precise factor and a sum carries the decimal place of its least precise term, so a calculator's digits are not a claim about precision; rounding is done once, at the end.
  - P1 · drills: pd-sigfig-product, pd-sigfig-sum
- ● **PD-8.1.B** (fe-chemical:1.F) Propagate stated uncertainties through a sum and a product
  - EK: Absolute uncertainties add in quadrature through a sum and relative ones through a product, so the largest contributor dominates and measuring the other quantities better buys almost nothing.
  - P1 · drills: pd-uncert-sum, pd-uncert-product
- ● **PD-8.1.C** (fe-chemical:1.F) Distinguish accuracy from precision for a stated set of measurements
  - EK: Precision is the spread of repeated measurements and accuracy is how close they sit to the truth, so a tight set can be badly wrong: precision is improved by repeating, accuracy only by calibrating.
  - P2 · drills: pd-accuracy-precision, pd-calibration-offset

### 8.2 Uncertainty in an economic decision



- ● **PD-8.2.A** (fe-chemical:13.C, cheme-grad-core:PS.3) Compute the expected monetary value of a stated decision under uncertainty
  - EK: The expected value weights each outcome by its probability, which ranks decisions but says nothing about the spread, so a decision whose downside cannot be survived is not chosen on expected value alone.
  - P1 · drills: pd-expected-value, pd-breakeven-probability
- ● **PD-8.2.B** (fe-chemical:13.C) Compute how far a stated economic conclusion moves when one input is varied
  - EK: A sensitivity analysis varies one input at a time to find which assumption the answer rests on, which is usually the price or the capacity rather than the capital cost.
  - P1 · drills: pd-sensitivity, pd-sensitivity-breakeven
- ● **PD-8.2.C** (fe-chemical:13.D, cheme-grad-core:PS.3, aiche-bok:T.OPT) Rank stated projects by net present value, payback and rate of return, and say where the rankings differ
  - EK: Net present value ranks by money created at the firm's own discount rate, payback ignores everything after it and prefers quick small projects, and rate of return is dimensionless and so ignores size; where they disagree, net present value is the one that answers the firm's question.
  - P2 · drills: pd-ranking-criteria, pd-payback-vs-npv

## Unit 9 · Statistics in engineering units (extension)

Big ideas: DOCS

### 9.1 Describing and testing data



- ● **PD-9.1.A** (fe-chemical:2.D) Compute the mean, median, sample standard deviation and range of a stated data set
  - EK: The median resists an outlier that moves the mean, and the sample standard deviation divides by one less than the count because the mean was estimated from the same data; reporting a mean without a spread says almost nothing.
  - P1 · drills: pd-mean-median, pd-sample-sd
- ● **PD-9.1.B** (fe-chemical:2.C) Test a stated engineering claim about a mean and state what the result does and does not show
  - EK: A hypothesis test asks how surprising the data would be if the claim were true, so failing to reject is not evidence that the claim holds, and a significant difference may still be too small to matter in the plant.
  - P2 · drills: pd-t-statistic, pd-test-meaning
- ● **PD-9.1.C** (fe-chemical:2.E) Fit a straight line to stated data and interpret its slope and coefficient of determination
  - EK: The least-squares slope is the covariance over the variance of the predictor, and the coefficient of determination is the fraction of variation the line accounts for, which says nothing about whether the relationship is causal or whether a straight line was the right shape.
  - P1 · drills: pd-regress-slope, pd-r-squared-meaning
- ● **PD-9.1.D** (fe-chemical:2.B) Compute the expected value of a stated engineering outcome and use it to choose
  - EK: An expected value over a discrete outcome set is the probability-weighted sum, and it is the right basis for a decision repeated many times; for a one-off with a ruinous branch it is not.
  - P1 · drills: pd-discrete-expectation, pd-inspection-worth

### 9.2 Capability and control charts



- ● **PD-9.2.A** (fe-chemical:2.F) Compute the control limits of an X-bar chart and decide whether a stated point is out of control
  - EK: Control limits sit three standard errors from the centre line, so they narrow with the square root of the subgroup size and are not the specification limits: a process can be in control and still make scrap.
  - P1 · drills: pd-control-limits, pd-subgroup-effect
- ● **PD-9.2.B** (fe-chemical:2.F) Compute the capability indices of a stated process and say what they mean
  - EK: Capability compares the specification width with six standard deviations, and the centred index also charges the process for being off target, so a capable but off-centre process has a high capability index and a low centred one.
  - P1 · drills: pd-cp-cpk, pd-cp-only
- ● **PD-9.2.C** (fe-chemical:2.F) Decide what a stated pattern on a control chart indicates
  - EK: A run on one side of the centre line, a steady trend or a point beyond three sigma each signal that something changed, and the point of the rules is to catch a shift before the product goes out of specification rather than after.
  - P2 · drills: pd-chart-pattern, pd-run-probability

## Unit 10 · Control strategies and hardware (extension)

Big ideas: DYN

### 10.1 Choosing a strategy



- ● **PD-10.1.A** (fe-chemical:15.B, aiche-bok:T.OPT) Choose feedback, feedforward, cascade or ratio control for a stated problem
  - EK: Feedback acts on the error and so always acts late; feedforward acts on a measured disturbance before the output moves but needs a model and leaves no correction for what it did not measure; cascade puts a fast inner loop inside a slow outer one; ratio holds one flow proportional to another.
  - P2 · drills: fe-strategy-pick, fe-cascade-speed
- ● **PD-10.1.B** (fe-chemical:15.B) State what each of the three controller actions contributes and what it costs
  - EK: Proportional action is immediate but leaves an offset, integral action removes the offset but adds lag and can wind up, and derivative action anticipates but amplifies measurement noise; a noisy flow loop is therefore usually proportional-integral rather than three-term.
  - P2 · drills: fe-pid-terms, fe-reset-time
- ● **PD-10.1.C** (fe-chemical:15.B, aiche-bok:T.OPT) Compute the offset a stated proportional-only loop leaves, and the gain that would halve it
  - EK: Proportional-only offset is the load change divided by one plus the loop gain, so halving the offset means doubling one plus the gain: the offset can be made small but never zero without integral action.
  - P1 · drills: fe-p-offset, fe-gain-for-offset

### 10.2 Loop design and hardware



- ● **PD-10.2.A** (fe-chemical:15.C, aiche-bok:T.INST) Compute a control valve's flow coefficient for a stated duty
  - EK: A valve's coefficient relates flow to the square root of its pressure drop over specific gravity, so a valve is sized at the flow it must pass with the drop actually available, and a valve taking too little of the system's drop loses authority over the flow.
  - P1 · drills: fe-valve-cv, fe-valve-authority
- ● **PD-10.2.B** (fe-chemical:15.C, aiche-bok:T.INST) Choose a valve characteristic and a failure position for a stated service
  - EK: A linear characteristic suits a loop where most of the drop is across the valve and an equal-percentage one where the line takes most of it, so the installed characteristic is what matters; the failure position is chosen from what is safe on air loss, which is why a fuel valve fails closed and a cooling-water valve fails open.
  - P2 · drills: fe-valve-characteristic, fe-installed-gain
- ● **PD-10.2.C** (fe-chemical:15.C, aiche-bok:T.INST) Convert between a stated transmitter range, its signal and the engineering value
  - EK: A transmitter maps its calibrated range linearly onto its output span, so a reading is converted by the fraction of span; getting the range wrong is the commonest reason a loop controls to the wrong value while looking healthy.
  - P1 · drills: fe-transmitter-span, fe-transmitter-signal

## Drills not yet placed on the map

- gc-first-order-time (design.control)
- gc-ramp-lag (design.control)
- gc-overshoot (design.control)
- gc-zeta-from-overshoot (design.control)
- gc-p-offset (design.control)
- gc-kc-for-offset (design.control)
- gc-ultimate-gain (design.control)
- gc-stability-check (design.control)
- gc-ultimate-period (design.control)
- gc-zn-reset (design.control)
- gc-amplitude-ratio (design.control)
- gc-phase-lag (design.control)
- gc-fopdt-crossover (design.control)
- gc-fopdt-ultimate-gain (design.control)
- cpd-dihedrals (design.structure)
- cpd-levinthal (design.structure)
- cpd-rotamer-lib (design.structure)
- cpd-rotamer-energy (design.structure)
- cpd-dihedral-which (design.structure)
- cpd-levinthal-time (design.structure)
- cpd-rotamer-apply (design.structure)
- cpd-rotamer-prob (design.structure)
- cpd-pose (design.representation)
- cpd-pose-index (design.representation)
- cpd-centroid (design.representation)
- cpd-centroid-speedup (design.representation)
- cpd-pose-apply (design.representation)
- cpd-pose-reverse (design.representation)
- cpd-resolution-pick (design.representation)
- cpd-atom-count (design.representation)
- cpd-symmetry (design.representation)
- cpd-symmetry-dof (design.representation)
- cpd-density (design.representation)
- cpd-membrane (design.representation)
- cpd-density-2 (design.representation)
- cpd-tm-span (design.representation)
- cpd-terms (design.energy)
- cpd-weighted-score (design.energy)
- cpd-ref (design.energy)
- cpd-ref-compare (design.energy)
- cpd-units (design.energy)
- cpd-term-decompose (design.energy)
- cpd-term-diagnose (design.energy)
- cpd-weight-change (design.energy)
- cpd-ref-apply (design.energy)
- cpd-ddg-mutation (design.energy)
- cpd-trust-score (design.energy)
- cpd-per-residue (design.energy)
- cpd-metropolis (design.sampling)
- cpd-accept-ratio (design.sampling)
- cpd-packer (design.sampling)
- cpd-pair-table (design.sampling)
- cpd-mc-apply (design.sampling)
- cpd-metropolis-de (design.sampling)
- cpd-protocol-order (design.sampling)
- cpd-pair-table-growth (design.sampling)
- cpd-loop-closure (design.sampling)
- cpd-loop-dof (design.sampling)
- cpd-refine-stages (design.sampling)
- cpd-refine-diagnose (design.sampling)
- cpd-resfile (design.sequence)
- cpd-seq-space (design.sequence)
- cpd-scan (design.sequence)
- cpd-scan-jobs (design.sequence)
- cpd-recovery (design.sequence)
- cpd-search-methods (design.sequence)
- cpd-task-scenario (design.sequence)
- cpd-alphabet-cut (design.sequence)
- cpd-scan-read (design.sequence)
- cpd-scan-positions (design.sequence)
- cpd-recovery-compare (design.sequence)
- cpd-method-pick (design.sequence)
- cpd-docking (design.interfaces)
- cpd-interface-energy (design.interfaces)
- cpd-ligand (design.interfaces)
- cpd-interface-design (design.interfaces)
- cpd-docking-read (design.interfaces)
- cpd-interface-reverse (design.interfaces)
- cpd-pocket-scenario (design.interfaces)
- cpd-interface-scenario (design.interfaces)
- cpd-antibody-model (design.interfaces)
- cpd-antibody-design (design.interfaces)
- cpd-cdr-count (design.interfaces)
- cpd-antibody-design-2 (design.interfaces)
- cpd-denovo-backbone (design.denovo)
- cpd-coiled-coil (design.denovo)
- cpd-hbnet (design.denovo)
- cpd-gap-population (design.denovo)
- cpd-backbone-pick (design.denovo)
- cpd-coiled-coil-length (design.denovo)
- cpd-hbnet-scenario (design.denovo)
- cpd-gap-needed (design.denovo)
- cpd-predictor-inputs (design.ml)
- cpd-coevolution (design.ml)
- cpd-representations (design.ml)
- cpd-diffusion-pipeline (design.ml)
- cpd-funnel-yield (design.ml)
- cpd-self-consistency (design.ml)
- cpd-confidence-scenario (design.ml)
- cpd-msa-scenario (design.ml)
- cpd-representation-pick (design.ml)
- cpd-pipeline-order (design.ml)
- cpd-funnel-reverse (design.ml)
- cpd-evidence-level (design.ml)
- cpd-experiments (design.validation)
- cpd-designs-needed (design.validation)
- cpd-score-vs-alchemical (design.validation)
- cpd-open-problems (design.validation)
- cpd-experiment-order (design.validation)
- cpd-hit-rate (design.validation)
- cpd-method-choice-scenario (design.validation)
- cpd-failure-diagnose (design.validation)
- cpd-parallel-kind (design.validation)
- cpd-decoys (design.validation)
- cpd-reproducible (design.validation)
- cpd-parallel-time (design.validation)
