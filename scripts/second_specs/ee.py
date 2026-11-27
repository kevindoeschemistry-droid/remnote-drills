"""Electric Circuits and Signals (EE, Nov 2026): the circuits, signals, electronics, power and control core of an
electrical engineering degree. Structure in UNITS (written by scripts/fw_setup.py), two question types per objective.

Basis: the NCEES FE Electrical and Computer CBT exam specifications (effective July 2020): sections 6 (circuit
analysis), 7 (linear systems), 8 (signal processing), 9 (electronics), 10 (power), 11 (electromagnetics) and 12
(control systems) were read to their lettered lines through an extraction, so read: part; the other sections were
not read. Cards compute by the usual formula; verify expressions solve the governing relation for the unknown."""
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "ee-circuits", "electric-circuits", "P1"
M = "Symbol('m')"
FW = dict(id="electric-circuits", title="Electric Circuits and Signals", code="EE", domain="ee", track="engineering", requires=["physics", "engineering-math"], level=3,
          primary="fe-electrical", also=[], subject="Electrical Engineering",
          note="Anchored on the NCEES FE Electrical and Computer specification, sections 6-10 and 12, read to their lettered lines. Electromagnetics (section 11) is left to Physics and is not cited; communications, networks, digital and computer systems and software are in Computer Science or not built. Circuits are described in words because no schematic figure type exists yet.",
          header=["Circuit analysis from Ohm's law to phasors, then what circuits do to signals (transients, resonance,",
                  "filters, sampling), the standard electronic building blocks, three-phase power and machines, and",
                  "feedback control. Every circuit is described in words, so each card is one relation and one number."],
          source=dict(id="fe-electrical-outline", title="Circuits and signals by FE Electrical section (course outline)", short="FE Electrical outline", field="electrical engineering",
                      note=["The FE Electrical and Computer sections written as a source so the ee.* skills have a home.", "NOT a book: only the specification was read. Chapter numbers are ours."]))
_I = [("6A", "KCL and KVL"), ("6B", "Series and parallel equivalent circuits"), ("6C", "Thevenin and Norton theorems"), ("6D", "Node and loop analysis"),
      ("6E", "Waveform analysis: RMS, average, frequency, phase"), ("6F", "Phasors"), ("6G", "Impedance"),
      ("7A", "Frequency and transient response"), ("7B", "Resonance"), ("7C", "Laplace transforms"), ("7D", "Transfer functions"),
      ("8A", "Sampling: aliasing and the Nyquist theorem"), ("8B", "Analog filters"), ("8C", "Digital filters: difference equations and z-transforms"),
      ("9A", "Discrete devices: diodes, transistors, thyristors"), ("9B", "Amplifiers"), ("9C", "Operational amplifiers"), ("9D", "Instrumentation and data acquisition"), ("9E", "Power electronics"),
      ("10A", "Power theory: power factor, single and three phase"), ("10B", "Transmission and distribution"), ("10C", "Transformers"), ("10D", "Motors and generators"),
      ("11A", "Electrostatics and magnetostatics"), ("11B", "Electrodynamics"), ("11C", "Transmission lines"),
      ("12A", "Block diagrams"), ("12B", "Bode plots"), ("12C", "Closed-loop and open-loop response and stability"), ("12D", "Controller performance")]
STDS = [{"id": "fe-electrical", "name": "NCEES FE Electrical and Computer CBT Exam Specifications (effective July 2020)", "publisher": "NCEES", "kind": "exam-spec", "read": "part",
         "url": "https://ncees.org/wp-content/uploads/2022/09/FE-Electrical-and-Computer-CBT-specs.pdf",
         "note": "Read Nov 2026 through an extraction of the NCEES PDF: sections 6-12 with their question ranges and lettered lines. Sections 1-5 (mathematics, statistics, ethics, economics, materials, engineering sciences) and 13-17 (communications, networks, digital systems, computer systems, software) were not read, so read: part. Items are the lettered lines of sections 6-12, titled in our words.",
         "items": [{"code": c, "title": t} for c, t in _I]}]
SKILLS = [("dc", "Kirchhoff's laws, equivalent resistance, dividers, Thevenin equivalents and node analysis", "DC circuits", []),
          ("ac", "RMS values, reactance, impedance, phase and AC power", "AC steady state", ["ee.dc"]),
          ("systems", "Time constants, resonance, transfer functions and frequency response", "Transients and linear systems", ["ee.ac"]),
          ("signals", "Sampling and aliasing, analog filters, difference equations", "Signal processing", ["ee.systems"]),
          ("electronics", "Diodes, transistors, operational amplifiers, rectifiers and converters", "Electronics", ["ee.dc"]),
          ("power", "Three-phase power, transformers and machines", "Power systems", ["ee.ac"]),
          ("control", "Feedback, second-order response, stability and Bode slopes", "Control systems", ["ee.systems"])]
IDEAS = [("CONS", "Charge and energy are conserved", "Currents into a node sum to zero and voltages round a loop sum to zero; every circuit method is bookkeeping on those two facts."),
         ("PHASOR", "Sinusoids become complex numbers", "At one frequency a capacitor and an inductor behave as imaginary resistances, so AC analysis is DC analysis with complex arithmetic."),
         ("POLE", "Poles tell the story", "Where a system's poles lie fixes how fast it responds, whether it rings and whether it is stable.")]
PRACTICES = [("P1", "Compute", "Carry a circuit or system relation to a number with its unit."),
             ("P2", "Classify", "Name the behaviour, the filter or the stability from a description.")]
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
DC, AC, SY, SG, EL, PW, CT = ["ee." + s[0] for s in SKILLS]
E_ = lambda *s: [f"fe-electrical:{x}" for x in s]


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def L(name, skill, prompt, options, rows, explain):
    return Q(name, skill, prompt, pace="recall", cases=[{"q": a, "kc": k} for a, k in rows], choice=options, correct="kc", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", **kw):
    return Q(name, skill, prompt, value=value, tex=tex, verify=verify, explain=explain, **kw)


def C(keys, rows):
    return [dict(zip(keys.split(), r)) for r in rows]


UNITS = {
 1: ("dc", "DC circuits", E_("6A", "6B", "6C", "6D"), ["CONS"], {
   1: ("Resistive circuits", [
     ("A", E_("6A"), "Apply Kirchhoff's current and voltage laws.",
      "KCL: the currents entering a node equal the currents leaving it. KVL: the voltage rises and drops round any closed loop sum to zero.", "P1", [
       N("ee-kcl-node", DC, "Currents of {{ka}} A and {{kb}} A flow into a node and {{kd}} A flows out through one branch. What current flows out through the only other branch?", "ka + kb - kd",
         f"solve(Eq(ka + kb, kd + {M}), {M})[0]", "What goes in must come out", tex="I", final=True,
         cases=C("ka kb kd", [(3, 5, 2), (1.5, 2.5, 3), (10, 4, 9), (0.8, 0.7, 0.5), (6, 6, 7)])),
       N("ee-kvl-loop", DC, "A {{kv}} V source drives two resistors in series. The voltage across the first resistor is {{ka}} V. What is the voltage across the second?", "kv - ka",
         f"solve(Eq(kv - ka - {M}, 0), {M})[0]", "Rises equal drops round the loop", tex="V", final=True,
         cases=C("kv ka", [(12, 4.5), (9, 6.2), (24, 15), (5, 1.8), (120, 45)]))]),
     ("B", E_("6B"), "Reduce series and parallel resistors and use the divider rules.",
      "Series resistances add. For two in parallel, R = R1 R2 ÷ (R1 + R2). A voltage divider gives V2 = V × R2 ÷ (R1 + R2); a current divider sends the larger current through the smaller resistance.", "P1", [
       N("ee-parallel", DC, "Resistors of {{ka}} Ω and {{kb}} Ω are connected in parallel. Find the equivalent resistance in ohms.", "ka*kb/(ka + kb)",
         f"solve(Eq(1/{M}, 1/Rational(ka) + 1/Rational(kb)), {M})[0]", "Product over sum; the result is always less than the smaller resistor", tex="R",
         cases=C("ka kb", [(6, 3), (10, 15), (100, 400), (12, 4), (30, 60)])),
       N("ee-voltage-divider", DC, "A {{kv}} V source drives {{ka}} Ω in series with {{kb}} Ω. Find the voltage across the {{kb}} Ω resistor.", "kv*kb/(ka + kb)",
         f"solve(Eq({M}/kb, kv/Rational(ka + kb)), {M})[0]", "The same current flows through both, so voltage splits in proportion to resistance", tex="V",
         cases=C("kv ka kb", [(12, 2, 4), (9, 1, 2), (10, 3, 7), (24, 5, 3), (5, 10, 15)]))]),
     ("C", E_("6C"), "Find a Thevenin equivalent and the maximum power it can deliver.",
      "Any linear two-terminal network is equivalent to a source Vth (the open-circuit voltage) in series with Rth (the resistance seen with sources switched off). A load draws maximum power when it equals Rth, and that power is Vth² ÷ (4 Rth).", "P1", [
       N("ee-thevenin-resistance", DC, "A {{kv}} V source drives {{ka}} Ω in series with {{kb}} Ω, and the output is taken across the {{kb}} Ω resistor. Find the Thevenin resistance seen at the output.", "ka*kb/(ka + kb)",
         f"(kv*kb/Rational(ka + kb))/(kv/Rational(ka))", "Short the source: the two resistors are then in parallel. The check divides open-circuit voltage by short-circuit current", tex="R_{th}",
         cases=C("kv ka kb", [(12, 6, 3), (10, 10, 15), (9, 4, 12), (24, 20, 30), (5, 1, 4)])),
       N("ee-max-power", DC, "A source has a Thevenin voltage of {{kv}} V and a Thevenin resistance of {{kr}} Ω. What is the maximum power it can deliver to a load?", "kv^2/(4*kr)",
         f"(kv/Rational(2*kr))**2*kr", "The matched load takes half the voltage, so P = (Vth/2)²/Rth", tex="P",
         cases=C("kv kr", [(12, 6), (10, 5), (24, 8), (9, 3), (5, 50)]))]),
     ("D", E_("6D"), "Solve a single-node circuit by node analysis and by superposition.",
      "Write KCL at the unknown node with each branch current as a voltage difference over a resistance. With several sources, superposition gives the same answer: find the response to each source with the others switched off, then add.", "P1", [
       N("ee-node-voltage", DC, "A node is connected to a {{ka}} V source through {{kp}} Ω, to a {{kb}} V source through {{kq}} Ω, and to ground through {{kr}} Ω. Find the node voltage.", "(ka/kp + kb/kq)/(1/kp + 1/kq + 1/kr)",
         f"solve(Eq((ka - {M})/kp + (kb - {M})/kq, {M}/kr), {M})[0]", "Sum of currents into the node from the two sources equals the current to ground", tex="V",
         cases=C("ka kp kb kq kr", [(12, 2, 6, 2, 2), (10, 5, 20, 10, 10), (9, 3, 3, 6, 6), (24, 4, 12, 4, 2)])),
       N("ee-superposition", DC, "A node is fed by a {{ka}} V source through {{kp}} Ω and by a second source through {{kq}} Ω, with {{kr}} Ω from the node to ground. With the second source switched off (replaced by a short), what node voltage does the first source alone produce?", "ka*(kq*kr/(kq + kr))/(kp + kq*kr/(kq + kr))",
         f"solve(Eq((ka - {M})/kp, {M}/kq + {M}/kr), {M})[0]", "With the other source shorted, its resistor is in parallel with the one to ground, and the first source sees a divider", tex="V",
         cases=C("ka kp kq kr", [(12, 2, 2, 2), (10, 5, 10, 10), (9, 3, 6, 6), (24, 4, 4, 2)]))])]),
 }),
 2: ("ac", "AC steady state", E_("6E", "6F", "6G", "10A"), ["PHASOR"], {
   1: ("Sinusoids and impedance", [
     ("A", E_("6E"), "Convert between peak, RMS, frequency and period.",
      "For a sinusoid the RMS value is the peak divided by √2; it is the DC value that would heat a resistor equally. Frequency is the reciprocal of the period, and angular frequency is 2πf.", "P1", [
       N("ee-rms", AC, "A sinusoidal voltage has a peak value of {{kp}} V. Find its RMS value.", "kp/sqrt(2)", f"sqrt(integrate((kp*sin(Y))**2, (Y, 0, 2*pi))/(2*pi))",
         "Root of the mean of the square over one cycle, which for a sine is peak over root two", tex="V_{rms}",
         cases=C("kp", [(170,), (10,), (325,), (5,), (48,)])),
       N("ee-angular-frequency", AC, "A sinusoid has a period of {{kt}} ms. Find its angular frequency in rad/s.", "2*pi/(kt/1000)", f"solve(Eq({M}*kt/1000, 2*pi), {M})[0]",
         "One cycle is 2π radians, covered in one period", tex="\\omega",
         cases=C("kt", [(20,), (1,), (16.667,), (2.5,), (0.5,)]))]),
     ("B", E_("6G"), "Compute the reactance of an inductor and a capacitor.",
      "An inductor's reactance is ωL and rises with frequency; a capacitor's is 1 ÷ (ωC) and falls with frequency. As impedances they are jωL and 1 ÷ (jωC): current lags voltage in an inductor and leads it in a capacitor.", "P1", [
       N("ee-inductive-reactance", AC, "Find the reactance in ohms of a {{kl}} mH inductor at {{kf}} Hz.", "2*pi*kf*kl/1000", f"solve(Eq({M}*1000, 2*pi*kf*kl), {M})[0]",
         "X_L = 2πfL, with L in henries", tex="X_L",
         cases=C("kl kf", [(10, 1000), (50, 60), (2, 5000), (100, 50), (0.5, 100000)])),
       N("ee-capacitive-reactance", AC, "Find the reactance in ohms of a {{kc0}} μF capacitor at {{kf}} Hz.", "1/(2*pi*kf*kc0*1e-6)", f"solve(Eq({M}*2*pi*kf*kc0, 10**6), {M})[0]",
         "X_C = 1/(2πfC), with C in farads", tex="X_C",
         cases=C("kc0 kf", [(10, 60), (1, 1000), (100, 50), (0.1, 10000), (47, 120)]))]),
     ("C", E_("6F", "6G"), "Combine resistance and reactance into an impedance magnitude and phase.",
      "In a series circuit Z = R + j(X_L − X_C), so |Z| = √(R² + X²) and the phase angle is arctan(X ÷ R): positive (current lags) when the circuit is inductive.", "P1", [
       N("ee-impedance-magnitude", AC, "A series circuit has a resistance of {{kr}} Ω, an inductive reactance of {{ka}} Ω and a capacitive reactance of {{kb}} Ω. Find the magnitude of its impedance.", "sqrt(kr^2 + (ka - kb)^2)",
         f"Abs(kr + I*ka - I*kb)", "Reactances subtract, then combine with resistance at right angles", tex="|Z|",
         cases=C("kr ka kb", [(3, 8, 4), (5, 20, 8), (8, 4, 10), (12, 25, 9), (40, 10, 40)])),
       N("ee-phase-angle", AC, "A series circuit has a resistance of {{kr}} Ω and a net reactance of {{kq}} Ω (positive means inductive). Find the phase angle of the impedance in degrees.", "atan(kq/kr)*180/pi",
         f"atan2(kq, kr)*180/pi", "tan φ = X/R; a positive angle means the current lags the voltage", tex="\\phi",
         cases=C("kr kq", [(3, 4), (10, 10), (8, -6), (5, 12), (20, -20)]))]),
     ("D", E_("10A"), "Compute real, reactive and apparent power and the power factor.",
      "Apparent power S = V_rms I_rms (VA). Real power P = S cos φ (W); reactive power Q = S sin φ (var); S² = P² + Q². The power factor is cos φ = P ÷ S.", "P1", [
       N("ee-real-power", AC, "A load draws {{ki0}} A RMS from a {{kv}} V RMS supply at a power factor of {{kf}}. Find the real power in watts.", "kv*ki0*kf", f"solve(Eq({M}/(kv*ki0), kf), {M})[0]",
         "Only the in-phase part of the current delivers energy", tex="P",
         cases=C("kv ki0 kf", [(120, 10, 0.8), (240, 5, 0.9), (230, 13, 0.6), (480, 20, 0.85), (120, 2, 0.5)])),
       N("ee-reactive-power", AC, "A load takes {{kp}} W of real power at an apparent power of {{ks}} VA. Find the reactive power in var.", "sqrt(ks^2 - kp^2)",
         f"Max(*solve(Eq({M}**2 + kp**2, ks**2), {M}))", "The power triangle: S is the hypotenuse of P and Q", tex="Q",
         cases=C("kp ks", [(800, 1000), (300, 500), (1200, 1300), (600, 1000), (2400, 2500)]))])]),
 }),
 3: ("systems", "Transients and linear systems", E_("7A", "7B", "7C", "7D"), ["POLE"], {
   1: ("Response in time and frequency", [
     ("A", E_("7A"), "Find a first-order time constant and the response at a given time.",
      "An RC circuit has time constant τ = RC and an RL circuit τ = L ÷ R. A step response rises as V(1 − e^(−t/τ)): 63% after one time constant, effectively complete after five.", "P1", [
       N("ee-time-constant", SY, "Find the time constant in milliseconds of a {{kr}} kΩ resistor in series with a {{kc0}} μF capacitor.", "kr*kc0", f"solve(Eq({M}/1000, kr*1000*kc0/10**6), {M})[0]",
         "τ = RC; kilohms times microfarads gives milliseconds", tex="\\tau",
         cases=C("kr kc0", [(10, 1), (4.7, 10), (100, 0.1), (2.2, 47), (1, 100)])),
       N("ee-step-response", SY, "A capacitor charges from zero toward {{kv}} V through a resistor with time constant {{kt}} ms. Find its voltage after {{ka}} ms.", "kv*(1 - exp(-ka/kt))",
         f"kv - kv*exp(-Rational(ka)/kt)", "v = V(1 − e^(−t/τ))", tex="v",
         cases=C("kv kt ka", [(10, 2, 2), (5, 10, 20), (12, 1, 3), (9, 4, 2), (24, 5, 5)]))]),
     ("B", E_("7B"), "Find the resonant frequency and quality factor of an RLC circuit.",
      "Resonance is where the inductive and capacitive reactances are equal: ω0 = 1 ÷ √(LC). For a series RLC circuit Q = ω0 L ÷ R, and the bandwidth is the resonant frequency divided by Q.", "P1", [
       N("ee-resonant-frequency", SY, "Find the resonant frequency in Hz of a {{kl}} mH inductor with a {{kc0}} μF capacitor.", "1/(2*pi*sqrt(kl*1e-3*kc0*1e-6))",
         f"Max(*solve(Eq(2*pi*{M}*kl/1000, 10**6/(2*pi*{M}*kc0)), {M}))", "The frequency at which X_L equals X_C", tex="f_0", tol=0.01,
         cases=C("kl kc0", [(10, 1), (1, 0.1), (100, 10), (25, 4), (2, 0.5)])),
       N("ee-quality-factor", SY, "A series RLC circuit resonates at {{kw}} rad/s with L = {{kl}} mH and R = {{kr}} Ω. Find its quality factor.", "kw*kl/1000/kr",
         f"solve(Eq({M}*kr*1000, kw*kl), {M})[0]", "Q = ω0 L / R: reactance at resonance over resistance", tex="Q",
         cases=C("kw kl kr", [(10000, 10, 5), (5000, 20, 10), (100000, 1, 2), (2000, 50, 4), (40000, 5, 8)]))]),
     ("C", E_("7C", "7D"), "Read a transfer function for DC gain, time constant and stability.",
      "For H(s) = K ÷ (s + a) the pole is at s = −a, the time constant is 1 ÷ a and the DC gain is H(0) = K ÷ a. A system is stable when every pole has a negative real part.", "P1", [
       N("ee-dc-gain", SY, "A system has transfer function H(s) = {{kk}} / (s + {{ka}}). Find its DC gain.", "kk/ka", f"limit(kk/(Z + ka), Z, 0)",
         "Set s = 0: the response to a constant input once transients have died", tex="H(0)",
         cases=C("kk ka", [(10, 2), (5, 20), (100, 4), (3, 12), (50, 5)])),
       L("ee-pole-stability", SY, "A system's poles are at {{q}}. Is it stable?", ["Stable", "Unstable", "Marginally stable"], [
           ("s = −2 and s = −5", 0), ("s = −1 ± 3j", 0), ("s = +1 and s = −4", 1), ("s = ±2j", 2), ("s = 0.5 ± 2j", 1), ("s = −3 only", 0)],
         "Left half-plane poles decay, right half-plane poles grow, poles on the imaginary axis neither")]),
     ("D", E_("7A", "7D"), "Find a first-order cutoff frequency and express a gain in decibels.",
      "An RC low-pass filter has H = 1 ÷ (1 + jωRC), cutoff frequency fc = 1 ÷ (2πRC) and gain 1/√2 (−3 dB) there. A voltage gain in decibels is 20 log10 of the ratio.", "P1", [
       N("ee-cutoff-frequency", SY, "Find the cutoff frequency in Hz of an RC low-pass filter with R = {{kr}} kΩ and C = {{kc0}} nF.", "1/(2*pi*kr*1e3*kc0*1e-9)",
         f"solve(Eq(2*pi*{M}*kr*kc0, 10**6), {M})[0]", "Where the capacitor's reactance equals the resistance", tex="f_c", tol=0.01,
         cases=C("kr kc0", [(1, 100), (10, 10), (4.7, 33), (100, 1), (2.2, 470)])),
       N("ee-decibels", SY, "An amplifier's output voltage is {{kg}} times its input voltage. Express the gain in decibels.", "20*log10(kg)", f"20*log(kg)/log(10)",
         "20 log10 for voltage ratios: a factor of 10 is 20 dB, a factor of 2 about 6 dB", tex="dB", tol=0.01,
         cases=C("kg", [(10,), (100,), (2,), (0.5,), (50,), (0.1,)]))])]),
 }),
 4: ("signals", "Signal processing", E_("8A", "8B", "8C"), ["POLE"], {
   1: ("Sampling and filtering", [
     ("A", E_("8A"), "Apply the Nyquist criterion and find an alias frequency.",
      "A signal must be sampled at more than twice its highest frequency. A component above half the sampling rate appears at the distance to the nearest multiple of the sampling rate: f_alias = |f − k fs|.", "P1", [
       N("ee-nyquist-rate", SG, "A signal's highest frequency component is {{kf}} kHz. What is the minimum sampling rate in kHz that avoids aliasing (the Nyquist rate)?", "2*kf", f"solve(Eq({M}/2, kf), {M})[0]",
         "Twice the highest frequency present", tex="f_s", final=True,
         cases=C("kf", [(20,), (4,), (3.4,), (15,), (0.5,)])),
       N("ee-alias-frequency", SG, "A {{kf}} Hz tone is sampled at {{ks}} Hz. At what frequency does it appear after sampling?", "abs(kf - round(kf/ks)*ks)",
         "Min(Abs(kf - floor(kf/Rational(ks))*ks), Abs(kf - (floor(kf/Rational(ks)) + 1)*ks))", "Fold about the nearest multiple of the sampling rate", tex="f",
         cases=C("kf ks", [(700, 1000), (1300, 1000), (4500, 8000), (9000, 8000), (60, 100)]))]),
     ("B", E_("8B"), "Name filter types and compute a first-order filter's gain.",
      "Low-pass, high-pass, band-pass and band-stop filters are named for what they let through. A first-order low-pass filter has gain 1 ÷ √(1 + (f/fc)²) and rolls off at 20 dB per decade above cutoff.", "P1", [
       L("ee-filter-type", SG, "Which filter? {{q}}", ["Low-pass", "High-pass", "Band-pass", "Band-stop (notch)"], [
           ("Removes 60 Hz hum and leaves frequencies above and below it", 3), ("Removes high-frequency noise from a slowly varying sensor signal", 0), ("Blocks DC and passes audio", 1),
           ("Selects one radio station from many", 2), ("An anti-aliasing filter placed before a sampler", 0), ("A series capacitor feeding a resistor to ground, output across the resistor", 1)],
         "Named for the band it passes"),
       N("ee-first-order-gain", SG, "A first-order low-pass filter has a cutoff frequency of {{kc0}} Hz. Find its gain (output amplitude over input amplitude) at {{kf}} Hz.", "1/sqrt(1 + (kf/kc0)^2)",
         f"Abs(1/(1 + I*Rational(kf)/kc0))", "|H| = 1/√(1 + (f/fc)²): 0.707 at cutoff, about a tenth one decade above", tex="|H|",
         cases=C("kc0 kf", [(100, 100), (1000, 3000), (50, 500), (200, 150), (10, 20)]))]),
     ("C", E_("8C"), "Run a difference equation and find a digital filter's DC gain.",
      "A digital filter computes each output from present and past samples. FIR filters use inputs only; IIR filters also feed back past outputs. The DC gain is the transfer function H(z) at z = 1.", "P1", [
       N("ee-difference-equation", SG, "A filter obeys y[n] = {{ka}} y[n−1] + x[n] with y[−1] = 0. The input is 1 for every n ≥ 0. Find y[2].", "1 + ka + ka^2",
         f"ka*(ka*(ka*0 + 1) + 1) + 1", "Step through: y[0] = 1, y[1] = a + 1, y[2] = a(a + 1) + 1", tex="y[2]",
         cases=C("ka", [(0.5,), (0.9,), (0.25,), (-0.5,), (0.8,)])),
       N("ee-digital-dc-gain", SG, "A filter obeys y[n] = {{ka}} y[n−1] + {{kb}} x[n]. Find its DC gain.", "kb/(1 - ka)", f"solve(Eq({M}, ka*{M} + kb), {M})[0]",
         "At DC the output stops changing, so set y[n] = y[n−1] with x = 1; equivalently H(z) at z = 1", tex="H(1)",
         cases=C("ka kb", [(0.5, 1), (0.9, 0.1), (0.75, 0.5), (-0.5, 3), (0.2, 4)]))])]),
 }),
 5: ("electronics", "Electronics", E_("9A", "9B", "9C", "9D", "9E"), ["CONS"], {
   1: ("Devices and amplifiers", [
     ("A", E_("9A", "9B"), "Use the constant-drop diode model and the transistor current gain.",
      "A forward-biased silicon diode is modelled as a 0.7 V drop; reverse-biased, it is an open circuit. In the active region a bipolar transistor's collector current is β times its base current.", "P1", [
       N("ee-diode-current", EL, "A {{kv}} V source drives a silicon diode (0.7 V drop when conducting) in series with a {{kr}} Ω resistor, forward biased. Find the current in mA.", "1000*(kv - 0.7)/kr",
         f"solve(Eq(kv - Rational(7, 10) - {M}*kr/1000, 0), {M})[0]", "KVL with the diode as a fixed 0.7 V drop", tex="I",
         cases=C("kv kr", [(5, 430), (12, 1000), (3.3, 260), (9, 2200), (1.5, 100)])),
       N("ee-bjt-collector", EL, "A transistor with β = {{kb}} has a base current of {{ka}} μA and is in the active region. Find the collector current in mA.", "kb*ka/1000",
         f"solve(Eq({M}*1000/kb, ka), {M})[0]", "I_C = β I_B", tex="I_C",
         cases=C("kb ka", [(100, 20), (200, 15), (150, 40), (80, 50), (250, 8)]))]),
     ("B", E_("9C"), "Find the gain of ideal op-amp circuits.",
      "An ideal op-amp with negative feedback holds its two inputs at the same voltage and draws no input current. Inverting amplifier: gain −Rf ÷ Rin. Non-inverting amplifier: gain 1 + Rf ÷ R1.", "P1", [
       N("ee-inverting-output", EL, "An inverting amplifier has a feedback resistor of {{kf}} kΩ and an input resistor of {{kn}} kΩ. Find the output voltage for an input of {{kv}} V.", "-kf/kn*kv",
         f"solve(Eq(kv/kn + {M}/kf, 0), {M})[0]", "KCL at the virtual ground: input current plus feedback current is zero", tex="V_o",
         cases=C("kf kn kv", [(10, 1, 0.5), (47, 10, 1), (100, 20, -0.2), (22, 2.2, 0.3), (5, 10, 4)])),
       N("ee-noninverting-gain", EL, "A non-inverting amplifier has a feedback resistor of {{kf}} kΩ and a resistor of {{kn}} kΩ from the inverting input to ground. Find its voltage gain.", "1 + kf/kn",
         f"solve(Eq(1/{M}, kn/Rational(kf + kn)), {M})[0]", "The feedback divider returns a fraction R1/(R1 + Rf) of the output, and the gain is its reciprocal", tex="A",
         cases=C("kf kn", [(9, 1), (10, 10), (47, 4.7), (100, 1), (2, 8)]))]),
     ("C", E_("9D", "9E"), "Compute converter resolution and a rectifier's average output.",
      "An n-bit converter divides its range into 2^n steps, so one step is the range ÷ 2^n. The average (DC) value of an ideal full-wave rectified sine is 2Vp ÷ π; half-wave gives Vp ÷ π.", "P1", [
       N("ee-adc-resolution", EL, "A {{kn}}-bit analog-to-digital converter has a full-scale range of {{kv}} V. Find the size of one step in millivolts.", "1000*kv/2^kn",
         f"solve(Eq({M}*2**kn/1000, kv), {M})[0]", "Range divided by the number of codes", tex="LSB",
         cases=C("kn kv", [(8, 5), (10, 3.3), (12, 5), (16, 10), (4, 2)])),
       N("ee-rectifier-average", EL, "An ideal full-wave rectifier is fed a sine wave of peak {{kp}} V. Find the average value of its output.", "2*kp/pi",
         f"integrate(kp*sin(Y), (Y, 0, pi))/pi", "Average of a half-sine over its half-period", tex="V_{avg}",
         cases=C("kp", [(10,), (170,), (17,), (5,), (34,)]))])]),
 }),
 6: ("power", "Power systems", E_("10A", "10B", "10C", "10D"), ["PHASOR"], {
   1: ("Three-phase, transformers and machines", [
     ("A", E_("10A", "10B"), "Relate line and phase quantities and compute three-phase power.",
      "In a balanced wye connection the line voltage is √3 times the phase voltage and line current equals phase current; in delta the roles swap. Total real power is √3 × V_line × I_line × power factor.", "P1", [
       N("ee-line-voltage", PW, "A balanced wye-connected source has a phase voltage of {{kv}} V. Find the line-to-line voltage.", "sqrt(3)*kv", "sqrt((kv - kv*cos(2*pi/3))**2 + (kv*sin(2*pi/3))**2)",
         "The difference of two phasors 120° apart is √3 times either", tex="V_L",
         cases=C("kv", [(120,), (277,), (230,), (2400,), (7200,)])),
       N("ee-three-phase-power", PW, "A balanced three-phase load draws {{ki0}} A per line at {{kv}} V line-to-line with a power factor of {{kf}}. Find the total real power in kW.", "sqrt(3)*kv*ki0*kf/1000",
         f"3*(kv/sqrt(3))*ki0*kf/1000", "√3 V_L I_L cos φ, the same as three times the per-phase power", tex="P",
         cases=C("kv ki0 kf", [(480, 20, 0.85), (208, 30, 0.9), (400, 10, 0.8), (4160, 50, 0.95), (240, 15, 0.7)]))]),
     ("B", E_("10C"), "Use the turns ratio of an ideal transformer.",
      "For an ideal transformer V1 ÷ V2 = N1 ÷ N2 and I1 ÷ I2 = N2 ÷ N1, so power is conserved. A load Z on the secondary looks like (N1 ÷ N2)² Z from the primary.", "P1", [
       N("ee-transformer-voltage", PW, "An ideal transformer has {{ka}} primary turns and {{kb}} secondary turns. The primary voltage is {{kv}} V. Find the secondary voltage.", "kv*kb/ka",
         f"solve(Eq(kv/{M}, Rational(ka)/kb), {M})[0]", "Voltage follows the turns", tex="V_2",
         cases=C("ka kb kv", [(1000, 100, 2400), (500, 50, 120), (200, 800, 120), (4000, 200, 7200), (120, 12, 240)])),
       N("ee-reflected-impedance", PW, "An ideal transformer with a turns ratio of {{ka}}:1 (primary to secondary) feeds a {{kz}} Ω load. What impedance does the source see?", "ka^2*kz",
         f"(ka*{M})/({M}/ka/kz)", "Voltage is multiplied by the ratio and current divided by it, so impedance goes as the ratio squared", tex="Z",
         cases=C("ka kz", [(10, 8), (2, 50), (5, 4), (20, 0.5), (4, 16)]))]),
     ("C", E_("10D"), "Compute synchronous speed and slip.",
      "Synchronous speed in rev/min is 120 f ÷ P for P poles. An induction motor runs slightly slower; slip = (synchronous speed − rotor speed) ÷ synchronous speed.", "P1", [
       N("ee-synchronous-speed", PW, "Find the synchronous speed in rev/min of a {{kp}}-pole machine on a {{kf}} Hz supply.", "120*kf/kp", f"solve(Eq({M}/60*kp/2, kf), {M})[0]",
         "Each pole pair gives one electrical cycle per revolution", tex="n_s", final=True,
         cases=C("kp kf", [(4, 60), (2, 50), (6, 60), (8, 50), (12, 60)])),
       N("ee-slip", PW, "A {{kp}}-pole, {{kf}} Hz induction motor runs at {{kn}} rev/min. Find its slip in percent.", "100*(120*kf/kp - kn)/(120*kf/kp)",
         f"solve(Eq(kn, (1 - {M}/100)*120*kf/kp), {M})[0]", "How far the rotor falls behind the rotating field, as a fraction of synchronous speed", tex="s",
         cases=C("kp kf kn", [(4, 60, 1746), (2, 50, 2910), (6, 60, 1140), (8, 50, 720), (4, 50, 1440)]))])]),
 }),
 7: ("control", "Control systems", E_("12A", "12B", "12C", "12D"), ["POLE"], {
   1: ("Feedback", [
     ("A", E_("12A", "12D"), "Reduce a feedback loop and find its steady-state error.",
      "With forward gain G and feedback gain H, negative feedback gives a closed-loop gain of G ÷ (1 + GH). For unity feedback and a step input, a system with DC loop gain K has a steady-state error of 1 ÷ (1 + K); an integrator in the loop makes it zero.", "P1", [
       N("ee-closed-loop-gain", CT, "A negative-feedback loop has a forward gain of {{kg}} and a feedback gain of {{kh}}. Find the closed-loop gain.", "kg/(1 + kg*kh)",
         f"solve(Eq({M}, kg*(1 - kh*{M})), {M})[0]", "Output = G × (input − H × output)", tex="T",
         cases=C("kg kh", [(100, 0.1), (10, 1), (1000, 0.01), (50, 0.5), (4, 0.25)])),
       N("ee-steady-state-error", CT, "A unity-feedback system with no integrator has a DC loop gain of {{kk}}. Find the steady-state error to a unit step, in percent.", "100/(1 + kk)",
         f"100*(1 - solve(Eq({M}, kk*(1 - {M})), {M})[0])", "The output settles at K/(1 + K), leaving 1/(1 + K) uncorrected", tex="e_{ss}",
         cases=C("kk", [(9,), (99,), (4,), (19,), (1,)]))]),
     ("B", E_("12C", "12D"), "Predict overshoot, settling time and damping type from ζ and ωn.",
      "A second-order system is underdamped for ζ < 1, critically damped at ζ = 1 and overdamped above. For ζ < 1 the percent overshoot is 100 e^(−πζ/√(1−ζ²)), and the 2% settling time is about 4 ÷ (ζ ωn).", "P1", [
       N("ee-overshoot", CT, "A second-order system has a damping ratio of {{kz}}. Find its percent overshoot to a step.", "100*exp(-pi*kz/sqrt(1 - kz^2))",
         f"100*exp(-pi/tan(acos(Rational(kz))))", "Overshoot depends on damping ratio alone", tex="OS", tol=0.01,
         cases=C("kz", [(0.5,), (0.7,), (0.2,), (0.3,), (0.6,)])),
       N("ee-settling-time", CT, "A second-order system has ζ = {{kz}} and ωn = {{kw}} rad/s. Estimate its 2% settling time in seconds from 4 / (ζ ωn).", "4/(kz*kw)",
         f"solve(Eq({M}*kz*kw, 4), {M})[0]", "Four time constants of the decaying envelope e^(−ζωn t)", tex="t_s",
         cases=C("kz kw", [(0.5, 4), (0.7, 10), (0.2, 5), (0.4, 20), (0.8, 2)]))]),
     ("C", E_("12B", "12C"), "Read Bode slopes and judge stability from margins.",
      "Each pole adds −20 dB per decade above its corner frequency and each zero adds +20 dB per decade. A closed loop is stable when the open loop has positive gain and phase margins; phase margin is 180° plus the open-loop phase at the gain-crossover frequency.", "P1", [
       N("ee-bode-slope", CT, "An open-loop transfer function has {{kp}} poles and {{kq}} zeros, all at frequencies well below the frequency of interest. Find the slope of its magnitude plot there, in dB per decade.", "-20*(kp - kq)",
         f"20*kq - 20*kp", "Minus 20 dB per decade for each pole, plus 20 for each zero", tex="slope", final=True,
         cases=C("kp kq", [(2, 0), (3, 1), (1, 0), (4, 1), (3, 0)])),
       N("ee-phase-margin", CT, "At the frequency where its gain is 0 dB, an open-loop system has a phase of {{ka}}°. Find the phase margin in degrees.", "180 + ka",
         f"solve(Eq(ka - {M}, -180), {M})[0]", "How much more lag the loop could take before reaching −180°", tex="PM", final=True,
         cases=C("ka", [(-135,), (-120,), (-150,), (-170,), (-100,)]))])]),
 }),
}
ADD = [(f"{FW['code']}-{n}.{tn}.{lo[0]}", qq) for n, u in UNITS.items() for tn, (tt, los) in u[4].items() for lo in los for qq in lo[5]]
