# Electric Circuits and Signals — curriculum framework (draft 1)

Generated from `drills/frameworks/electric-circuits.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**24 learning objectives** in 7 units (24 core): 24 drilled, 0 partly, 0 with no drills. Core: 24 / 24 drilled.

## Big ideas

- **CONS · Charge and energy are conserved.** Currents into a node sum to zero and voltages round a loop sum to zero; every circuit method is bookkeeping on those two facts.
- **PHASOR · Sinusoids become complex numbers.** At one frequency a capacitor and an inductor behave as imaginary resistances, so AC analysis is DC analysis with complex arithmetic.
- **POLE · Poles tell the story.** Where a system's poles lie fixes how fast it responds, whether it rings and whether it is stable.

## Practices

- **P1 · Compute.** Carry a circuit or system relation to a number with its unit.
- **P2 · Classify.** Name the behaviour, the filter or the stability from a description.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · DC circuits | core | — | 4 | 4 | 0 | 0 |
| 2 · AC steady state | core | — | 4 | 4 | 0 | 0 |
| 3 · Transients and linear systems | core | — | 4 | 4 | 0 | 0 |
| 4 · Signal processing | core | — | 3 | 3 | 0 | 0 |
| 5 · Electronics | core | — | 3 | 3 | 0 | 0 |
| 6 · Power systems | core | — | 3 | 3 | 0 | 0 |
| 7 · Control systems | core | — | 3 | 3 | 0 | 0 |

## Unit 1 · DC circuits

Big ideas: CONS

### 1.1 Resistive circuits



- ● **EE-1.1.A** (fe-electrical:6A) Apply Kirchhoff's current and voltage laws.
  - EK: KCL: the currents entering a node equal the currents leaving it. KVL: the voltage rises and drops round any closed loop sum to zero.
  - Needs: PH-11.7.B
  - P1 · drills: ee-kcl-node, ee-kvl-loop
- ● **EE-1.1.B** (fe-electrical:6B) Reduce series and parallel resistors and use the divider rules.
  - EK: Series resistances add. For two in parallel, R = R1 R2 ÷ (R1 + R2). A voltage divider gives V2 = V × R2 ÷ (R1 + R2); a current divider sends the larger current through the smaller resistance.
  - Needs: EE-1.1.A
  - P1 · drills: ee-parallel, ee-voltage-divider
- ● **EE-1.1.C** (fe-electrical:6C) Find a Thevenin equivalent and the maximum power it can deliver.
  - EK: Any linear two-terminal network is equivalent to a source Vth (the open-circuit voltage) in series with Rth (the resistance seen with sources switched off). A load draws maximum power when it equals Rth, and that power is Vth² ÷ (4 Rth).
  - Needs: EE-1.1.B
  - P1 · drills: ee-thevenin-resistance, ee-max-power
- ● **EE-1.1.D** (fe-electrical:6D) Solve a single-node circuit by node analysis and by superposition.
  - EK: Write KCL at the unknown node with each branch current as a voltage difference over a resistance. With several sources, superposition gives the same answer: find the response to each source with the others switched off, then add.
  - Needs: EE-1.1.C
  - P1 · drills: ee-node-voltage, ee-superposition

## Unit 2 · AC steady state

Big ideas: PHASOR

### 2.1 Sinusoids and impedance



- ● **EE-2.1.A** (fe-electrical:6E) Convert between peak, RMS, frequency and period.
  - EK: For a sinusoid the RMS value is the peak divided by √2; it is the DC value that would heat a resistor equally. Frequency is the reciprocal of the period, and angular frequency is 2πf.
  - Needs: EE-1.1.D, EM-1.2.C
  - P1 · drills: ee-rms, ee-angular-frequency
- ● **EE-2.1.B** (fe-electrical:6G) Compute the reactance of an inductor and a capacitor.
  - EK: An inductor's reactance is ωL and rises with frequency; a capacitor's is 1 ÷ (ωC) and falls with frequency. As impedances they are jωL and 1 ÷ (jωC): current lags voltage in an inductor and leads it in a capacitor.
  - Needs: EE-2.1.A
  - P1 · drills: ee-inductive-reactance, ee-capacitive-reactance
- ● **EE-2.1.C** (fe-electrical:6F, fe-electrical:6G) Combine resistance and reactance into an impedance magnitude and phase.
  - EK: In a series circuit Z = R + j(X_L − X_C), so |Z| = √(R² + X²) and the phase angle is arctan(X ÷ R): positive (current lags) when the circuit is inductive.
  - Needs: EE-2.1.B
  - P1 · drills: ee-impedance-magnitude, ee-phase-angle
- ● **EE-2.1.D** (fe-electrical:10A) Compute real, reactive and apparent power and the power factor.
  - EK: Apparent power S = V_rms I_rms (VA). Real power P = S cos φ (W); reactive power Q = S sin φ (var); S² = P² + Q². The power factor is cos φ = P ÷ S.
  - Needs: EE-2.1.C
  - P1 · drills: ee-real-power, ee-reactive-power

## Unit 3 · Transients and linear systems

Big ideas: POLE

### 3.1 Response in time and frequency



- ● **EE-3.1.A** (fe-electrical:7A) Find a first-order time constant and the response at a given time.
  - EK: An RC circuit has time constant τ = RC and an RL circuit τ = L ÷ R. A step response rises as V(1 − e^(−t/τ)): 63% after one time constant, effectively complete after five.
  - Needs: EE-2.1.D, EM-7.3.B, PH-11.8.B
  - P1 · drills: ee-time-constant, ee-step-response
- ● **EE-3.1.B** (fe-electrical:7B) Find the resonant frequency and quality factor of an RLC circuit.
  - EK: Resonance is where the inductive and capacitive reactances are equal: ω0 = 1 ÷ √(LC). For a series RLC circuit Q = ω0 L ÷ R, and the bandwidth is the resonant frequency divided by Q.
  - Needs: EE-3.1.A
  - P1 · drills: ee-resonant-frequency, ee-quality-factor
- ● **EE-3.1.C** (fe-electrical:7C, fe-electrical:7D) Read a transfer function for DC gain, time constant and stability.
  - EK: For H(s) = K ÷ (s + a) the pole is at s = −a, the time constant is 1 ÷ a and the DC gain is H(0) = K ÷ a. A system is stable when every pole has a negative real part.
  - Needs: EE-3.1.B
  - P1 · drills: ee-dc-gain, ee-pole-stability
- ● **EE-3.1.D** (fe-electrical:7A, fe-electrical:7D) Find a first-order cutoff frequency and express a gain in decibels.
  - EK: An RC low-pass filter has H = 1 ÷ (1 + jωRC), cutoff frequency fc = 1 ÷ (2πRC) and gain 1/√2 (−3 dB) there. A voltage gain in decibels is 20 log10 of the ratio.
  - Needs: EE-3.1.C
  - P1 · drills: ee-cutoff-frequency, ee-decibels

## Unit 4 · Signal processing

Big ideas: POLE

### 4.1 Sampling and filtering



- ● **EE-4.1.A** (fe-electrical:8A) Apply the Nyquist criterion and find an alias frequency.
  - EK: A signal must be sampled at more than twice its highest frequency. A component above half the sampling rate appears at the distance to the nearest multiple of the sampling rate: f_alias = |f − k fs|.
  - Needs: EE-3.1.D
  - P1 · drills: ee-nyquist-rate, ee-alias-frequency
- ● **EE-4.1.B** (fe-electrical:8B) Name filter types and compute a first-order filter's gain.
  - EK: Low-pass, high-pass, band-pass and band-stop filters are named for what they let through. A first-order low-pass filter has gain 1 ÷ √(1 + (f/fc)²) and rolls off at 20 dB per decade above cutoff.
  - Needs: EE-4.1.A
  - P1 · drills: ee-filter-type, ee-first-order-gain
- ● **EE-4.1.C** (fe-electrical:8C) Run a difference equation and find a digital filter's DC gain.
  - EK: A digital filter computes each output from present and past samples. FIR filters use inputs only; IIR filters also feed back past outputs. The DC gain is the transfer function H(z) at z = 1.
  - Needs: EE-4.1.B
  - P1 · drills: ee-difference-equation, ee-digital-dc-gain

## Unit 5 · Electronics

Big ideas: CONS

### 5.1 Devices and amplifiers



- ● **EE-5.1.A** (fe-electrical:9A, fe-electrical:9B) Use the constant-drop diode model and the transistor current gain.
  - EK: A forward-biased silicon diode is modelled as a 0.7 V drop; reverse-biased, it is an open circuit. In the active region a bipolar transistor's collector current is β times its base current.
  - Needs: EE-1.1.D
  - P1 · drills: ee-diode-current, ee-bjt-collector
- ● **EE-5.1.B** (fe-electrical:9C) Find the gain of ideal op-amp circuits.
  - EK: An ideal op-amp with negative feedback holds its two inputs at the same voltage and draws no input current. Inverting amplifier: gain −Rf ÷ Rin. Non-inverting amplifier: gain 1 + Rf ÷ R1.
  - Needs: EE-5.1.A
  - P1 · drills: ee-inverting-output, ee-noninverting-gain
- ● **EE-5.1.C** (fe-electrical:9D, fe-electrical:9E) Compute converter resolution and a rectifier's average output.
  - EK: An n-bit converter divides its range into 2^n steps, so one step is the range ÷ 2^n. The average (DC) value of an ideal full-wave rectified sine is 2Vp ÷ π; half-wave gives Vp ÷ π.
  - Needs: EE-5.1.B
  - P1 · drills: ee-adc-resolution, ee-rectifier-average

## Unit 6 · Power systems

Big ideas: PHASOR

### 6.1 Three-phase, transformers and machines



- ● **EE-6.1.A** (fe-electrical:10A, fe-electrical:10B) Relate line and phase quantities and compute three-phase power.
  - EK: In a balanced wye connection the line voltage is √3 times the phase voltage and line current equals phase current; in delta the roles swap. Total real power is √3 × V_line × I_line × power factor.
  - Needs: EE-2.1.D
  - P1 · drills: ee-line-voltage, ee-three-phase-power
- ● **EE-6.1.B** (fe-electrical:10C) Use the turns ratio of an ideal transformer.
  - EK: For an ideal transformer V1 ÷ V2 = N1 ÷ N2 and I1 ÷ I2 = N2 ÷ N1, so power is conserved. A load Z on the secondary looks like (N1 ÷ N2)² Z from the primary.
  - Needs: EE-6.1.A
  - P1 · drills: ee-transformer-voltage, ee-reflected-impedance
- ● **EE-6.1.C** (fe-electrical:10D) Compute synchronous speed and slip.
  - EK: Synchronous speed in rev/min is 120 f ÷ P for P poles. An induction motor runs slightly slower; slip = (synchronous speed − rotor speed) ÷ synchronous speed.
  - Needs: EE-6.1.B
  - P1 · drills: ee-synchronous-speed, ee-slip

## Unit 7 · Control systems

Big ideas: POLE

### 7.1 Feedback



- ● **EE-7.1.A** (fe-electrical:12A, fe-electrical:12D) Reduce a feedback loop and find its steady-state error.
  - EK: With forward gain G and feedback gain H, negative feedback gives a closed-loop gain of G ÷ (1 + GH). For unity feedback and a step input, a system with DC loop gain K has a steady-state error of 1 ÷ (1 + K); an integrator in the loop makes it zero.
  - Needs: EE-3.1.D
  - P1 · drills: ee-closed-loop-gain, ee-steady-state-error
- ● **EE-7.1.B** (fe-electrical:12C, fe-electrical:12D) Predict overshoot, settling time and damping type from ζ and ωn.
  - EK: A second-order system is underdamped for ζ < 1, critically damped at ζ = 1 and overdamped above. For ζ < 1 the percent overshoot is 100 e^(−πζ/√(1−ζ²)), and the 2% settling time is about 4 ÷ (ζ ωn).
  - Needs: EE-7.1.A
  - P1 · drills: ee-overshoot, ee-settling-time
- ● **EE-7.1.C** (fe-electrical:12B, fe-electrical:12C) Read Bode slopes and judge stability from margins.
  - EK: Each pole adds −20 dB per decade above its corner frequency and each zero adds +20 dB per decade. A closed loop is stable when the open loop has positive gain and phase margins; phase margin is 180° plus the open-loop phase at the gain-crossover frequency.
  - Needs: EE-7.1.B
  - P1 · drills: ee-bode-slope, ee-phase-margin
