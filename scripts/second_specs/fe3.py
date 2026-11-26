"""The last five FE Chemical items nothing in the Library answered: material types and compatibility (4.B), corrosion
mechanisms and control (4.C), bioprocessing (5.E), control strategies (15.B) and loop design and hardware (15.C).

Corrosion and materials go to Materials as unit 4, bioprocessing to Reaction Engineering as unit 9, and the control
strategies to Process Design unit 10 beside its first-order dynamics. Two question types per objective, every number
recomputed by the verifier. Where a table was not read (galvanic series positions, standard valve coefficients) the
card prints the values it needs.
"""
from opl_dsl import Q

FILE, PRACTICE = "fe-last", "P1"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
CORR, BIO, CTRL = "materials.corrosion", "cre.bioprocess", "design.control"


def facts(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall",
             cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


# ── Materials unit 4 ────────────────────────────────────────────────────
MT_UNITS = {"4": ("corrosion", "Material selection and corrosion", ["PROPS"],
                  ["fe-chemical:4.A", "fe-chemical:4.B", "fe-chemical:4.C"])}
MT_TOPICS = {"4.1": "Choosing a material", "4.2": "Corrosion mechanisms", "4.3": "Corrosion control"}
MT_OBJS = [
 ("MT-4.1.A", ["fe-chemical:4.B"], "Choose a material class for a stated service from its temperature, pressure and chemistry",
  "Carbon steel is the default and everything else is justified against it: stainless for oxidising and mildly corrosive service, nickel alloys for hot chlorides and strong acids, titanium for seawater and wet chlorine, and polymers or linings where metals fail but temperature allows.", "P2"),
 ("MT-4.1.B", ["fe-chemical:4.B"], "Compute the wall thickness a stated corrosion allowance adds and the life it buys",
  "A corrosion allowance is thickness added beyond the pressure requirement, so the life it buys is the allowance over the corrosion rate; doubling the allowance doubles the life only if the rate stays constant, which is exactly what localised attack does not do.", "P1"),
 ("MT-4.1.C", ["fe-chemical:4.B"], "Decide whether a stated material pairing is compatible in service",
  "Compatibility is not just whether the metal dissolves: it covers embrittlement, stress-corrosion cracking, catalytic decomposition of the fluid and contamination of the product, and a compatibility chart is read for the fluid at the service temperature, not at room temperature.", "P2"),
 ("MT-4.2.A", ["fe-chemical:4.C"], "Compute a corrosion rate from a mass-loss or thickness measurement",
  "A uniform rate in millimetres a year follows from mass loss over area, density and time, and it is the one corrosion mode a wall thickness can be designed against.", "P1"),
 ("MT-4.2.B", ["fe-chemical:4.C"], "Identify the corrosion mechanism a stated failure describes",
  "Uniform attack thins the wall evenly; pitting and crevice attack concentrate it where the electrolyte is stagnant; galvanic attack puts the anode next to a more noble metal; stress-corrosion cracking needs tensile stress, a susceptible alloy and a specific environment together; and erosion-corrosion follows high velocity and solids.", "P2"),
 ("MT-4.2.C", ["fe-chemical:4.C"], "Predict which metal corrodes in a stated galvanic couple and how the area ratio changes the rate",
  "The less noble metal is the anode and corrodes, and the current it must carry is set by the cathode area, so a small anode next to a large cathode corrodes fast: a steel bolt in a stainless plate fails, while a stainless bolt in a steel plate does not.", "P2"),
 ("MT-4.3.A", ["fe-chemical:4.C"], "Compute a cathodic protection current from the area to be protected and a stated current density",
  "Cathodic protection makes the whole structure the cathode, either with a sacrificial anode of a less noble metal or with an impressed current, and the duty is the protected area times the current density the environment needs.", "P1"),
 ("MT-4.3.B", ["fe-chemical:4.C"], "State what a coating, an inhibitor and a passive film each do and how each fails",
  "A coating is a barrier that fails locally at a holiday, where attack then concentrates; an inhibitor changes the solution so the reaction slows, and fails when its concentration drops; a passive film is grown by the metal itself, and fails where chloride breaks it down or where oxygen cannot reach to repair it.", "P2"),
]
# ── Reaction Engineering unit 9 ─────────────────────────────────────────
RE_UNITS = {"9": ("bioprocess", "Bioprocessing", ["TIME"], ["fe-chemical:5.E"])}
RE_TOPICS = {"9.1": "Growth and product formation", "9.2": "Bioreactor operation"}
RE_OBJS = [
 ("RE-9.1.A", ["fe-chemical:5.E"], "Compute a specific growth rate from the Monod equation and the doubling time it gives",
  "Monod kinetics is Michaelis-Menten applied to a whole organism: growth saturates at a maximum specific rate, and the doubling time is the natural logarithm of two over that rate.", "P1"),
 ("RE-9.1.B", ["fe-chemical:5.E"], "Compute a yield coefficient and the substrate a stated batch needs",
  "A yield coefficient is cells or product per unit substrate consumed, so the substrate charge follows from the target titre; what the coefficient leaves out is maintenance, which is why a slow fermentation uses more substrate per gram of product than a fast one.", "P1"),
 ("RE-9.1.C", ["fe-chemical:5.E"], "Compute the dilution rate at which a chemostat washes out and the productivity near it",
  "At steady state in a chemostat the specific growth rate equals the dilution rate, so raising the feed rate raises productivity until the dilution rate reaches the maximum growth rate, at which point the culture washes out.", "P1"),
 ("RE-9.2.A", ["fe-chemical:5.E"], "Compute the oxygen transfer a stated aerobic fermentation needs and compare it with the supply",
  "An aerobic culture's oxygen demand is its oxygen uptake rate, and the supply is the transfer coefficient times the driving force to the dissolved concentration; because oxygen is barely soluble, the driving force is small and transfer is usually what limits scale-up rather than kinetics.", "P1"),
 ("RE-9.2.B", ["fe-chemical:5.E"], "State which mode of bioreactor operation a stated objective calls for",
  "Batch is simplest and gives a defined lot, fed-batch avoids substrate inhibition and catabolite repression and is what most industrial fermentations use, continuous gives the highest productivity but risks contamination and strain drift over long runs, and perfusion keeps cells while removing product.", "P2"),
 ("RE-9.2.C", ["fe-chemical:5.E"], "Compute the sterilisation hold a stated thermal death requirement needs",
  "Thermal death is first order in viable count, so the hold time is the number of log reductions times the decimal reduction time at that temperature; the design basis is the probability of one survivor in the whole batch, not an average.", "P1"),
]
# ── Process Design unit 10 ──────────────────────────────────────────────
PD_UNITS = {"10": ("control-strategy", "Control strategies and hardware", ["DYN"],
                   ["fe-chemical:15.B", "fe-chemical:15.C"])}
PD_TOPICS = {"10.1": "Choosing a strategy", "10.2": "Loop design and hardware"}
PD_OBJS = [
 ("PD-10.1.A", ["fe-chemical:15.B"], "Choose feedback, feedforward, cascade or ratio control for a stated problem",
  "Feedback acts on the error and so always acts late; feedforward acts on a measured disturbance before the output moves but needs a model and leaves no correction for what it did not measure; cascade puts a fast inner loop inside a slow outer one; ratio holds one flow proportional to another.", "P2"),
 ("PD-10.1.B", ["fe-chemical:15.B"], "State what each of the three controller actions contributes and what it costs",
  "Proportional action is immediate but leaves an offset, integral action removes the offset but adds lag and can wind up, and derivative action anticipates but amplifies measurement noise; a noisy flow loop is therefore usually proportional-integral rather than three-term.", "P2"),
 ("PD-10.1.C", ["fe-chemical:15.B"], "Compute the offset a stated proportional-only loop leaves, and the gain that would halve it",
  "Proportional-only offset is the load change divided by one plus the loop gain, so halving the offset means doubling one plus the gain: the offset can be made small but never zero without integral action.", "P1"),
 ("PD-10.2.A", ["fe-chemical:15.C"], "Compute a control valve's flow coefficient for a stated duty",
  "A valve's coefficient relates flow to the square root of its pressure drop over specific gravity, so a valve is sized at the flow it must pass with the drop actually available, and a valve taking too little of the system's drop loses authority over the flow.", "P1"),
 ("PD-10.2.B", ["fe-chemical:15.C"], "Choose a valve characteristic and a failure position for a stated service",
  "A linear characteristic suits a loop where most of the drop is across the valve and an equal-percentage one where the line takes most of it, so the installed characteristic is what matters; the failure position is chosen from what is safe on air loss, which is why a fuel valve fails closed and a cooling-water valve fails open.", "P2"),
 ("PD-10.2.C", ["fe-chemical:15.C"], "Convert between a stated transmitter range, its signal and the engineering value",
  "A transmitter maps its calibrated range linearly onto its output span, so a reading is converted by the fraction of span; getting the range wrong is the commonest reason a loop controls to the wrong value while looking healthy.", "P1"),
]
OBJS = MT_OBJS + RE_OBJS + PD_OBJS
UNITS = {}
TOPICS = {**MT_TOPICS, **RE_TOPICS, **PD_TOPICS}

ADD = [
 # ── materials: selection ───────────────────────────────────────────
 ("MT-4.1.A", facts("fe-material-pick", CORR, [
     ("Hot concentrated chloride solution at 150 degrees Celsius calls for:", "A nickel alloy, since stainless steels crack in hot chlorides", "304 stainless steel", "Carbon steel", "Aluminium"),
     ("Seawater service at ambient temperature calls for:", "Titanium or a suitable copper-nickel alloy", "Carbon steel with no allowance", "Mild steel galvanised", "Cast iron"),
     ("The default material against which others are justified is:", "Carbon steel", "316 stainless steel", "Titanium", "A fluoropolymer lining"),
     ("Dilute sulphuric acid at ambient temperature in a small vessel often argues for:", "A lined or polymer vessel, since the metals that resist it are expensive", "Carbon steel", "Aluminium", "Galvanised steel"),
     ("A material that resists the fluid but fails the service may still be wrong because of:", "Temperature, stress, or contamination of the product", "Price alone", "Colour", "Availability alone"),
 ], "Carbon steel first, and every upgrade justified by what specifically attacks it at the service conditions")),
 ("MT-4.1.B", Q("fe-corrosion-life", CORR, "A vessel carries a corrosion allowance of {{al}} mm at a measured rate of {{rt}} mm a year. What life does the allowance buy (years)?",
     given={"al": {"pick": [1.5, 3.0, 6.0]}, "rt": {"pick": [0.05, 0.1, 0.25, 0.5]}},
     value="al/rt", tex="years", verify="nsimplify(al)/nsimplify(rt)",
     explain="A design life follows from allowance over rate, which works only for uniform attack: pitting goes through a wall while the average thickness barely moves, so an allowance is no defence against it")),
 ("MT-4.1.B", Q("fe-allowance-needed", CORR, "A {{yr}}-year life at a corrosion rate of {{rt}} mm a year needs what allowance (mm)?",
     given={"yr": {"pick": [10, 20, 25]}, "rt": {"pick": [0.05, 0.1, 0.25, 0.5]}},
     value="yr*rt", tex="mm", verify="nsimplify(yr)*nsimplify(rt)",
     explain="The reverse: at half a millimetre a year a twenty-five year life needs more than a centimetre of extra steel, which is usually the point at which a better material is cheaper than the thickness")),
 ("MT-4.1.C", facts("fe-compatibility", CORR, [
     ("Austenitic stainless steel under tensile stress in a hot chloride solution is at risk of:", "Stress-corrosion cracking, which needs stress, a susceptible alloy and that environment together", "Uniform thinning only", "Galvanic attack", "No attack"),
     ("Hydrogen service at high temperature and pressure threatens steel through:", "Hydrogen attack and embrittlement, which the alloy is selected against", "Pitting", "Crevice attack", "Erosion"),
     ("Copper is excluded from some service not because it corrodes but because it:", "Catalyses decomposition of the fluid or contaminates the product", "Is expensive", "Is soft", "Is non-magnetic"),
     ("A compatibility chart must be read at:", "The service temperature, since ratings change with it", "Room temperature", "The boiling point", "Any temperature: ratings are fixed"),
 ], "Compatibility covers cracking, embrittlement, catalysis and contamination, not just dissolution")),
 # ── materials: mechanisms ──────────────────────────────────────────
 ("MT-4.2.A", Q("fe-corrosion-rate", CORR, "A coupon of area {{ar}} cm2 loses {{ml}} mg over {{dy}} days. With a density of {{dn}} g/cm3, what is the corrosion rate (mm/year)?",
     cases=[{"ar": 20, "ml": 45, "dy": 30, "dn": 7.86}, {"ar": 50, "ml": 180, "dy": 90, "dn": 7.86},
            {"ar": 10, "ml": 12, "dy": 60, "dn": 8.9}, {"ar": 25, "ml": 300, "dy": 14, "dn": 2.7}],
     value="ml/1000/dn/ar*10*365/dy", tex="mm/year",
     verify="nsimplify(ml)/1000/nsimplify(dn)/nsimplify(ar)*10*365/nsimplify(dy)",
     explain="Mass loss becomes a thickness by dividing by density and area, and a rate by dividing by time; a coupon measures the uniform rate only, so pitting has to be looked for separately")),
 ("MT-4.2.A", Q("fe-rate-from-thickness", CORR, "An inspection finds {{th}} mm of wall lost after {{yr}} years. What rate is that (mm/year), and how long until a further {{rm}} mm goes?",
     given={"th": {"pick": [0.8, 2.0, 4.5]}, "yr": {"pick": [4, 8, 15]}, "rm": {"pick": [1.0, 3.0]}},
     value="rm/(th/yr)", tex="years", verify="nsimplify(rm)/(nsimplify(th)/nsimplify(yr))",
     explain="Extrapolating a measured rate is how an inspection interval is set, and it assumes the mechanism and the conditions have not changed since the wall was new")),
 ("MT-4.2.B", facts("fe-mechanism-id", CORR, [
     ("Deep isolated holes in an otherwise sound stainless wall indicate:", "Pitting, usually initiated by chloride on the passive film", "Uniform attack", "Galvanic attack", "Erosion-corrosion"),
     ("Attack concentrated under a gasket and nowhere else indicates:", "Crevice corrosion, where the trapped solution cannot be replenished with oxygen", "Uniform attack", "Stress-corrosion cracking", "Pitting on the open surface"),
     ("Branching cracks in a stressed component with no general thinning indicate:", "Stress-corrosion cracking", "Pitting", "Uniform attack", "Erosion"),
     ("Thinning concentrated just downstream of an elbow indicates:", "Erosion-corrosion, from high velocity and entrained solids", "Uniform attack", "Crevice corrosion", "Galvanic attack"),
     ("Attack confined to where two different metals are bolted together indicates:", "Galvanic corrosion", "Pitting", "Stress-corrosion cracking", "Uniform attack"),
 ], "Each mechanism leaves its own geometry, which is why a failure is diagnosed from where the metal went rather than from how much")),
 ("MT-4.2.C", Q("fe-area-ratio", CORR, "A galvanic couple has a cathode of {{ac}} cm2 and an anode of {{aa}} cm2. By what factor is the anode's current density raised over an equal-area couple?",
     given={"ac": {"pick": [50, 200, 1000]}, "aa": {"pick": [1, 5, 25]}},
     require=["ac > aa"], value="ac/aa", tex="\\times", verify="Rational(ac, aa)",
     explain="The cathode sets the total current and the anode carries it over its own area, so a small anode next to a large cathode corrodes fast: a steel bolt in a stainless plate fails, the reverse pairing does not")),
 ("MT-4.2.C", facts("fe-galvanic-which", CORR, [
     ("In a couple of carbon steel and 316 stainless in seawater, which corrodes?", "The carbon steel, as the less noble member", "The stainless steel", "Neither", "Both equally"),
     ("In a couple of zinc and steel, which corrodes?", "The zinc, which is why it is used as a sacrificial anode", "The steel", "Neither", "Both equally"),
     ("Galvanic attack needs:", "Two different metals, an electrolyte and an electrical connection", "Only two different metals", "Only an electrolyte", "Tensile stress"),
     ("Breaking the electrical connection with an insulating gasket:", "Stops the galvanic current and so the attack", "Has no effect", "Accelerates attack", "Changes which metal is the anode"),
 ], "Less noble corrodes, and the couple needs all three of metals, electrolyte and connection, so removing any one stops it")),
 # ── materials: control ────────────────────────────────────────────
 ("MT-4.3.A", Q("fe-cp-current", CORR, "A structure of {{ar}} m2 needs a protection current density of {{cd}} mA/m2. What total current is that (A)?",
     given={"ar": {"pick": [40, 350, 2500]}, "cd": {"pick": [10, 20, 55, 110]}},
     value="ar*cd/1000", tex="A", verify="nsimplify(ar)*Rational(cd, 1000)",
     explain="The duty scales with the exposed area, so coating the structure first and protecting cathodically only the coating holidays is what makes the anode or rectifier small")),
 ("MT-4.3.A", Q("fe-anode-life", CORR, "A sacrificial anode of {{ms}} kg delivers {{cap}} A-hours per kg at a current of {{cu}} A. How many years does it last?",
     given={"ms": {"pick": [10, 25, 60]}, "cap": {"pick": [780, 1230, 2600]}, "cu": {"pick": [0.5, 2, 8]}},
     value="ms*cap/cu/8766", tex="years", verify="nsimplify(ms)*nsimplify(cap)/nsimplify(cu)/8766",
     explain="An anode's life is its charge capacity over the current drawn, so the replacement interval and the protection duty are the same calculation read two ways")),
 ("MT-4.3.B", facts("fe-protection-fails", CORR, [
     ("A coating with a small holiday is worse than no coating in one respect:", "Attack concentrates at the holiday, since the small bare area carries all the current", "It is always better", "It changes the anode", "It raises the pH"),
     ("A corrosion inhibitor fails when:", "Its concentration falls below what is needed, which can be worse than none if it leaves partial coverage", "The temperature falls", "The flow stops", "The pH rises"),
     ("A passive film on stainless steel is broken down by:", "Chloride, especially where oxygen cannot reach to repair the film", "Nitrogen", "Oxygen", "Water alone"),
     ("A passive film repairs itself only where:", "Oxygen can reach the surface, which is why crevices and deposits are dangerous", "The metal is stressed", "Chloride is present", "The flow is high"),
     ("Cathodic protection makes the protected structure:", "The cathode of the cell, so it no longer dissolves", "The anode", "Electrically isolated", "Non-conducting"),
 ], "Each control measure has its own failure mode, and a partly failed barrier concentrates attack rather than halving it")),
 # ── bioprocessing ─────────────────────────────────────────────────
 ("RE-9.1.A", Q("fe-monod-rate", BIO, "With a maximum specific growth rate of {{mx}} per hour and a half-saturation constant of {{ks}} g/L, what specific growth rate does a substrate concentration of {{ss}} g/L give (per hour)?",
     given={"mx": {"pick": [0.25, 0.4, 0.9]}, "ks": {"pick": [0.1, 0.5, 2.0]}, "ss": {"pick": [0.05, 1.0, 5.0, 20]}},
     value="mx*ss/(ks + ss)", tex="h^{-1}",
     verify="nsimplify(mx)*nsimplify(ss)/(nsimplify(ks) + nsimplify(ss))",
     explain="Monod kinetics is Michaelis-Menten for a whole organism: well above the half-saturation constant growth is at its maximum and substrate concentration no longer matters, which is the regime a batch spends most of its time in")),
 ("RE-9.1.A", Q("fe-doubling-time", BIO, "A culture grows at a specific rate of {{mu}} per hour. What is its doubling time (hours)?",
     given={"mu": {"pick": [0.08, 0.25, 0.4, 1.2]}}, value="log(2)/mu", tex="h",
     verify="log(2)/nsimplify(mu)",
     explain="Doubling time is the natural logarithm of two over the specific rate, so a culture at 0.4 per hour doubles in under two hours while one at 0.08 takes nearly nine")),
 ("RE-9.1.B", Q("fe-yield-substrate", BIO, "A target of {{tt}} g/L of cells at a yield of {{yx}} g cells per g substrate needs how much substrate (g/L), if {{s0}} g/L must be left at the end?",
     given={"tt": {"pick": [8, 25, 60]}, "yx": {"pick": [0.3, 0.45, 0.5]}, "s0": {"pick": [0, 1, 5]}},
     value="tt/yx + s0", tex="g/L", verify="nsimplify(tt)/nsimplify(yx) + nsimplify(s0)",
     explain="The yield coefficient converts the target titre into a substrate charge; it leaves out maintenance, so a slow fermentation uses more substrate per gram of product than the coefficient predicts")),
 ("RE-9.1.B", Q("fe-yield-from-batch", BIO, "A batch consumed {{ds}} g/L of substrate and produced {{dx}} g/L of cells. What yield coefficient is that (g/g)?",
     given={"ds": {"pick": [20, 55, 120]}, "dx": {"pick": [6, 25, 48]}},
     require=["dx < ds"], value="dx/ds", tex="g/g", verify="Rational(dx, ds)",
     explain="Measuring the yield from the batch rather than assuming it is how maintenance and by-product formation show up, as a yield below the theoretical value")),
 ("RE-9.1.C", Q("fe-washout", BIO, "A chemostat of volume {{vv}} L runs on a feed of {{qq}} L/h. What is its dilution rate (per hour), and does it exceed a maximum growth rate of {{mx}} per hour? Give the dilution rate.",
     given={"vv": {"pick": [50, 200, 1000]}, "qq": {"pick": [5, 40, 150]}, "mx": {"pick": [0.25, 0.4, 0.9]}},
     value="qq/vv", tex="h^{-1}", verify="Rational(qq, vv)",
     explain="At steady state the specific growth rate equals the dilution rate, so a dilution rate above the maximum growth rate washes the culture out: the highest usable feed rate sits just below it")),
 ("RE-9.1.C", Q("fe-chemostat-feed", BIO, "What feed rate (L/h) sets a dilution rate of {{fr}} times the maximum growth rate of {{mx}} per hour in a {{vv}} L vessel?",
     given={"fr": {"pick": [0.5, 0.8, 0.95]}, "mx": {"pick": [0.25, 0.4, 0.9]}, "vv": {"pick": [50, 200, 1000]}},
     value="fr*mx*vv", tex="L/h", verify="nsimplify(fr)*nsimplify(mx)*nsimplify(vv)",
     explain="Running near the washout point maximises productivity and minimises the margin for upset, which is why continuous culture is run at a fraction of the maximum rather than at it")),
 ("RE-9.2.A", Q("fe-oxygen-demand", BIO, "A culture of {{xx}} g/L has a specific oxygen uptake of {{qo}} mmol per g per hour in {{vv}} L. What is the oxygen demand (mmol/h)?",
     given={"xx": {"pick": [5, 20, 45]}, "qo": {"pick": [2, 8, 15]}, "vv": {"pick": [50, 200, 1000]}},
     value="xx*qo*vv", tex="mmol/h", verify="nsimplify(xx)*nsimplify(qo)*nsimplify(vv)",
     explain="Demand scales with cell mass, so the oxygen a fermentation needs rises through the batch and peaks late: the transfer system is sized for the peak, not the average")),
 ("RE-9.2.A", Q("fe-kla-needed", BIO, "To meet an oxygen demand of {{dm}} mmol/(L h) with a saturation of {{cs}} mmol/L and a dissolved concentration held at {{cl}} mmol/L, what transfer coefficient is needed (per hour)?",
     given={"dm": {"pick": [20, 90, 250]}, "cs": {"pick": [0.21, 0.25]}, "cl": {"pick": [0.02, 0.05, 0.1]}},
     require=["cl < cs"], value="dm/(cs - cl)", tex="h^{-1}",
     verify="nsimplify(dm)/(nsimplify(cs) - nsimplify(cl))",
     explain="Because oxygen's saturation concentration is tiny, the driving force is tiny and the required coefficient is large: oxygen transfer, not kinetics, is usually what limits a fermentation's scale-up")),
 ("RE-9.2.B", facts("fe-reactor-mode", BIO, [
     ("A substrate that inhibits growth at high concentration argues for:", "Fed-batch, feeding it at the rate the culture consumes it", "Batch with the whole charge at the start", "Continuous at high dilution", "Perfusion"),
     ("The highest volumetric productivity, accepting the risks, comes from:", "Continuous culture near the washout point", "Batch", "Fed-batch", "A sequence of batches"),
     ("The main risks of a long continuous run are:", "Contamination and genetic drift of the strain", "Oxygen limitation only", "Substrate inhibition", "Foaming"),
     ("A defined, traceable lot for a regulated product argues for:", "Batch or fed-batch operation", "Continuous culture", "Perfusion with recycle", "Whichever is cheapest"),
     ("Perfusion differs from simple continuous culture by:", "Retaining the cells while product is removed", "Removing cells with the product", "Running without feed", "Operating above washout"),
 ], "The mode follows the constraint: inhibition, productivity, contamination risk or lot definition")),
 ("RE-9.2.C", Q("fe-sterilisation-hold", BIO, "A sterilisation must achieve {{nl}} log reductions with a decimal reduction time of {{dv}} minutes. What hold time is needed (minutes)?",
     given={"nl": {"pick": [6, 9, 12]}, "dv": {"pick": [0.3, 1.1, 2.5]}},
     value="nl*dv", tex="min", verify="nsimplify(nl)*nsimplify(dv)",
     explain="Thermal death is first order in viable count, so each decimal reduction time removes a factor of ten and the hold is simply the product; the basis is the probability of a single survivor in the batch")),
 ("RE-9.2.C", Q("fe-sterilisation-logs", BIO, "A starting load of {{n0}} organisms must be brought to a survival probability of 1 in {{pp}}. How many log reductions is that?",
     given={"n0": {"pick": [1000000, 100000000]}, "pp": {"pick": [1000, 1000000]}},
     value="log10(n0) + log10(pp)", tex="logs", verify="log(nsimplify(n0), 10) + log(nsimplify(pp), 10)",
     explain="The reductions needed span from the starting load down past one to the accepted survival probability, which is why a pharmaceutical basis asks for twelve logs rather than six")),
 # ── control strategies ────────────────────────────────────────────
 ("PD-10.1.A", facts("fe-strategy-pick", CTRL, [
     ("A measurable inlet disturbance that moves the output before feedback can react argues for:", "Feedforward on that disturbance, trimmed by feedback", "Feedback alone with a higher gain", "Ratio control", "Manual operation"),
     ("A slow temperature loop whose valve is upset by changing steam pressure argues for:", "Cascade, with a fast inner pressure or flow loop inside the temperature loop", "Feedforward on temperature", "A larger valve", "Derivative action"),
     ("Holding one reagent flow proportional to another is:", "Ratio control", "Cascade control", "Feedforward control", "Override control"),
     ("Feedforward alone is risky because:", "It corrects only for what it measures and models, and never checks the result", "It is slower than feedback", "It needs no model", "It cannot be combined with feedback"),
     ("Feedback's inherent limitation is that:", "It acts only once the output has already moved", "It needs a process model", "It cannot remove offset", "It requires a fast inner loop"),
 ], "Each strategy answers a different question: when the disturbance is known, when the valve is unreliable, and when two streams must track")),
 ("PD-10.1.B", facts("fe-pid-terms", CTRL, [
     ("Which action leaves a steady offset after a load change?", "Proportional alone", "Integral", "Derivative", "None of them"),
     ("Which action removes the offset but can wind up when the valve saturates?", "Integral", "Proportional", "Derivative", "Feedforward"),
     ("Which action anticipates but amplifies measurement noise?", "Derivative", "Integral", "Proportional", "Ratio"),
     ("A noisy flow loop is usually tuned as:", "Proportional-integral, leaving derivative out", "Three-term with high derivative", "Proportional only", "Integral only"),
     ("Reset windup is prevented by:", "Limiting or freezing the integral while the output is saturated", "Raising the gain", "Adding derivative", "Narrowing the proportional band"),
 ], "Three actions with three costs, and the loop's noise and speed decide which are used")),
 ("PD-10.1.C", Q("fe-p-offset", CTRL, "A proportional-only loop has a loop gain of {{kg}}. What fraction of an unmeasured load change remains as offset?",
     given={"kg": {"pick": [1, 4, 9, 19]}}, value="1/(1 + kg)", tex="fraction",
     verify="Rational(1, 1 + kg)",
     explain="Offset is the load change over one plus the loop gain, so it falls with gain but never reaches zero; integral action is what removes it, at the cost of lag")),
 ("PD-10.1.C", Q("fe-gain-for-offset", CTRL, "What loop gain reduces a proportional-only offset from {{f1}} to {{f2}} of the load change?",
     cases=[{"f1": 0.5, "f2": 0.1}, {"f1": 0.2, "f2": 0.05}, {"f1": 0.25, "f2": 0.02}, {"f1": 0.1, "f2": 0.01}],
     value="1/f2 - 1", tex="K", verify="1/nsimplify(f2) - 1",
     explain="Cutting the offset by a factor of five means raising one plus the gain by five, which is also five times the sensitivity to noise: the trade is why integral action exists")),
 ("PD-10.2.A", Q("fe-valve-cv", CTRL, "A valve must pass {{qq}} US gallons per minute of a liquid of specific gravity {{sg}} with {{dp}} psi across it. What flow coefficient is needed, using Cv = Q*sqrt(SG/dP)?",
     given={"qq": {"pick": [40, 150, 600]}, "sg": {"pick": [0.8, 1.0, 1.25]}, "dp": {"pick": [5, 15, 40]}},
     value="qq*sqrt(sg/dp)", tex="C_v",
     verify="nsimplify(qq)*sqrt(nsimplify(sg)/nsimplify(dp))",
     explain="The coefficient is printed as its defining equation because valve-standard tables were not read. Flow goes as the square root of the drop, so a valve given only a small share of the system's drop has little authority over the flow")),
 ("PD-10.2.A", Q("fe-valve-authority", CTRL, "A valve takes {{dv}} psi of a system whose total drop is {{dt}} psi. What percentage of the drop is across the valve?",
     given={"dv": {"pick": [5, 15, 40]}, "dt": {"pick": [25, 60, 120]}},
     require=["dv < dt"], value="100*dv/dt", tex="\\%", verify="100*Rational(dv, dt)",
     explain="Valve authority is its share of the total drop; below about a quarter the installed characteristic distorts badly and the loop becomes hard to tune at any gain")),
 ("PD-10.2.B", facts("fe-valve-characteristic", CTRL, [
     ("A valve taking most of the system's pressure drop suits:", "A linear characteristic", "An equal-percentage characteristic", "A quick-opening characteristic", "Any characteristic"),
     ("A valve in a line that takes most of the drop suits:", "An equal-percentage characteristic, so the installed behaviour comes out closer to linear", "A linear characteristic", "A quick-opening characteristic", "No valve"),
     ("A fuel gas valve is usually specified to:", "Fail closed on loss of air", "Fail open", "Fail in place", "Fail to its last position"),
     ("A cooling water valve on an exothermic reactor is usually specified to:", "Fail open on loss of air", "Fail closed", "Fail in place", "Fail to minimum flow"),
     ("The installed characteristic differs from the inherent one because:", "The pressure drop across the valve changes as it opens and the line takes more", "The actuator is nonlinear", "The positioner distorts it", "The trim wears"),
 ], "The characteristic is chosen for the installed behaviour, and the failure position is chosen from what is safe on air loss")),
 ("PD-10.2.C", Q("fe-transmitter-span", CTRL, "A transmitter is ranged {{lo}} to {{hi}} degrees Celsius on a 4 to 20 mA output. What does {{ma}} mA mean (degrees Celsius)?",
     given={"lo": {"pick": [0, 50, 100]}, "hi": {"pick": [200, 300, 400]}, "ma": {"pick": [8, 12, 17.6]}},
     require=["hi > lo"], value="lo + (ma - 4)/16*(hi - lo)", tex="^\\circ C",
     verify="nsimplify(lo) + (nsimplify(ma) - 4)/16*(nsimplify(hi) - nsimplify(lo))",
     explain="The signal maps linearly onto the calibrated range, so a wrong range makes a loop control to the wrong value while every indication looks healthy")),
 ("PD-10.2.C", Q("fe-transmitter-signal", CTRL, "The same transmitter, ranged {{lo}} to {{hi}} degrees Celsius, reads {{tv}} degrees. What current does it send (mA)?",
     given={"lo": {"pick": [0, 50, 100]}, "hi": {"pick": [200, 300, 400]}, "tv": {"pick": [120, 180, 260]}},
     require=["tv > lo", "tv < hi"], value="4 + (tv - lo)/(hi - lo)*16", tex="mA",
     verify="4 + (nsimplify(tv) - nsimplify(lo))/(nsimplify(hi) - nsimplify(lo))*16",
     explain="The reverse conversion, and the reason the zero is at 4 mA rather than 0: a broken wire reads 0 and is distinguishable from a genuine bottom-of-range reading")),
]

# Second types for the facts-only objectives above, each a different question form.
ADD += [
 ("MT-4.1.A", Q("fe-upgrade-cost", CORR, "Carbon steel for a vessel costs {{k1}} dollars; the alloy that resists the service costs {{fm}} times as much in material. If material is {{mf}} per cent of the installed cost, what does the upgrade add to the installed cost (per cent)?",
     given={"k1": {"pick": [40000, 120000]}, "fm": {"pick": [2.5, 4, 8]}, "mf": {"pick": [25, 40, 60]}},
     value="(fm - 1)*mf", tex="\\%", verify="(nsimplify(fm) - 1)*nsimplify(mf)",
     explain="The alloy premium only applies to the material fraction, so a four-fold material price rise on a vessel that is 40 per cent material adds 120 per cent, not 300: that arithmetic is what decides upgrade against allowance against lining")),
 ("MT-4.1.C", Q("fe-stress-threshold", CORR, "A component is stressed to {{sv}} MPa against a stress-corrosion threshold of {{th}} MPa in this environment. What percentage of the threshold is that?",
     given={"sv": {"pick": [60, 140, 310]}, "th": {"pick": [100, 200, 350]}},
     value="100*sv/th", tex="\\%", verify="100*Rational(sv, th)",
     explain="Stress-corrosion cracking needs stress above a threshold in that specific environment, so a stress-relief heat treatment or a lower design stress removes the risk without changing the alloy")),
 ("MT-4.2.B", Q("fe-pit-penetration", CORR, "Uniform attack runs at {{ur}} mm a year while pits grow {{pf}} times faster. A wall of {{wt}} mm fails by pitting in how many years?",
     given={"ur": {"pick": [0.05, 0.1, 0.2]}, "pf": {"pick": [10, 25, 60]}, "wt": {"pick": [6, 10, 16]}},
     value="wt/(ur*pf)", tex="years", verify="nsimplify(wt)/(nsimplify(ur)*nsimplify(pf))",
     explain="The number is why an allowance is no defence against pitting: at twenty-five times the uniform rate a wall is through long before the average thickness has moved, and only inspection for pits catches it")),
 ("MT-4.3.B", Q("fe-coating-holiday", CORR, "A coating covers all but {{hp}} per cent of a surface. By what factor is the current density on the bare metal raised, compared with the whole surface being bare?",
     given={"hp": {"pick": [0.1, 0.5, 2, 5]}}, value="100/hp", tex="\\times",
     verify="100/nsimplify(hp)",
     explain="A nearly perfect coating concentrates the whole cell's current into the holidays, which is why a coated pipeline still needs cathodic protection and why a small defect perforates fast")),
 ("RE-9.2.B", Q("fe-fedbatch-feed", BIO, "A fed-batch holds substrate at the consumption rate. With {{xx}} g/L of cells in {{vv}} L at a specific consumption of {{qs}} g per g per hour, what feed of a {{cf}} g/L solution is needed (L/h)?",
     given={"xx": {"pick": [10, 30, 60]}, "vv": {"pick": [100, 500, 2000]}, "qs": {"pick": [0.05, 0.12, 0.3]}, "cf": {"pick": [200, 500, 700]}},
     value="xx*vv*qs/cf", tex="L/h",
     verify="nsimplify(xx)*nsimplify(vv)*nsimplify(qs)/nsimplify(cf)",
     explain="Feeding at the consumption rate is what keeps substrate low enough to avoid inhibition and repression; because cell mass grows, the feed has to rise with it, which is why fed-batch profiles are exponential")),
 ("PD-10.1.A", Q("fe-cascade-speed", CTRL, "An outer loop has a time constant of {{to}} minutes and the inner loop {{ti}} minutes. By what factor is the inner loop faster, and is the usual rule of at least three times met? Give the factor.",
     given={"to": {"pick": [8, 20, 45]}, "ti": {"pick": [0.5, 2, 6]}},
     value="to/ti", tex="\\times", verify="nsimplify(to)/nsimplify(ti)",
     explain="Cascade works only when the inner loop settles well inside the outer loop's response, usually a factor of three or more; below that the two loops interact and tuning either one upsets the other")),
 ("PD-10.1.B", Q("fe-reset-time", CTRL, "A controller's integral action is set as a reset time of {{tr}} minutes per repeat. What is the reset rate in repeats per minute?",
     given={"tr": {"pick": [0.4, 2.5, 8, 20]}}, value="1/tr", tex="repeats/min",
     verify="1/nsimplify(tr)",
     explain="The same integral setting is quoted both ways by different makers, and confusing them turns a sluggish loop into an oscillating one: more repeats per minute is more integral action, more minutes per repeat is less")),
 ("PD-10.2.B", Q("fe-installed-gain", CTRL, "An equal-percentage valve has an inherent rangeability of {{rg}}. What fraction of maximum flow does it pass at {{op}} per cent open, if flow goes as R to the power of (opening minus one)?",
     cases=[{"rg": 50, "op": 50}, {"rg": 50, "op": 25}, {"rg": 30, "op": 75}, {"rg": 100, "op": 50}],
     value="rg^(op/100 - 1)", tex="fraction",
     verify="nsimplify(rg)**(Rational(op, 100) - 1)",
     explain="An equal-percentage valve passes a small fraction of full flow at half open, which is what compensates a line whose own drop rises with flow: the installed characteristic is the product of the two")),
]
