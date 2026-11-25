"""General-chemistry objectives for the articulations of the ACS general-chemistry content map (2015) that no
Library objective answered (scripts/accm_maps.py): atom size, getting an element out of an ore, surface area and
rate, protein-ligand binding, and laboratory practice and safety. Safety items are standard practice (OSHA
laboratory standard, GHS pictograms, ALARA); they are authored, and the radiation items are recomputed."""
from opl_dsl import Q

FILE, FRAMEWORK = "ch-accm", "chemistry"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
TOPICS = {"0.6": "Laboratory practice and safety"}


def facts(name, skill, rows, explain, pace="quick"):
    return Q(name, skill, "{{q}}", pace=pace, cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


NA = "6.02214076e23"
OBJS = [
    ("CH-0.5.B", ["acs-accm-general:I.E.3"], "Use the picometre size of atoms to see why a mole is so large.",
     "Atoms are about 100–300 pm across; a millimetre holds millions of them in a row, so a visible sample holds ~10²³."),
    ("CH-4.5.F", ["acs-accm-general:III.H.3"], "Find the mass of an element that can be recovered from an ore or mineral sample.",
     "Mass of element = mass of ore × fraction of mineral × (mass of element in one formula unit ÷ formula mass)."),
    ("CH-5.5.B", ["acs-accm-general:VII.A.3"], "Explain and quantify how dividing a solid raises its surface area and its reaction rate.",
     "Cutting a cube into n³ smaller cubes multiplies the exposed area by n; a surface reaction speeds up in proportion."),
    ("CH-7.5.B", ["acs-accm-general:VIII.G.3"], "Find the fraction of a protein bound to its ligand from the dissociation constant.",
     "P + L ⇌ PL with K_d = [P][L]/[PL]; with ligand in excess, the fraction bound is [L]/(K_d + [L]): half bound when [L] = K_d."),
    ("CH-0.6.A", ["acs-accm-general:IX.F.1", "acs-accm-general:IX.G.2"], "Classify an error as random or systematic, predict its direction, and choose a procedure that limits it.",
     "Systematic errors push every result one way (a mis-zeroed balance, a wet sample); random errors scatter both ways and shrink with replicates; blanks and calibration remove systematic ones."),
    ("CH-0.6.B", ["acs-accm-general:IX.G.3"], "Keep a laboratory record that others can verify.",
     "Write directly in a bound notebook in ink, date every entry, cross out mistakes with one line instead of erasing, and record conditions and raw data."),
    ("CH-0.6.C", ["acs-accm-general:IX.H.1", "acs-accm-general:IX.H.2", "acs-accm-general:IX.H.4"], "Choose the safety equipment and handling for a hazard, reading GHS pictograms and safety data sheets.",
     "Goggles always; fume hood for volatile or toxic substances; know the eyewash, shower and extinguisher; GHS pictograms and SDS sections name the hazard and the response."),
    ("CH-0.6.D", ["acs-accm-general:IX.H.3"], "Dispose of laboratory waste by category.",
     "Separate halogenated from non-halogenated solvents, keep oxidisers apart from organics, neutralise or collect acids and bases, never pour heavy metals or organics down the drain."),
    ("CH-0.6.E", ["acs-accm-general:IX.H.5"], "Reduce radiation dose with time, distance and shielding.",
     "Dose rate falls with the square of the distance from a point source; each half-value layer of shielding halves it; dose = rate × time."),
]

ADD = [
    ("CH-0.5.B", Q("ch-atoms-in-a-line", "gchem.composition", "Atoms {{d}} pm across are lined up touching. How many fit in {{L}} mm?",
        given={"d": {"pick": [100, 150, 250, 300]}, "L": {"pick": [1, 5, 10]}}, value="L*1e-3/(d*1e-12)", tex="N",
        verify="L*Rational(1, 1000)/(d*Rational(1, 10**12))", explain="Convert both lengths to metres and divide: 1 mm ÷ 100 pm = 10⁷ atoms")),
    ("CH-0.5.B", Q("ch-mole-of-marbles", "gchem.composition", "If each atom in a mole were a marble {{dm}} mm across, packed in a cube, how long would the cube's edge be, in km?",
        given={"dm": {"pick": [1, 5, 10]}}, value=f"({NA})^(1/3)*dm*1e-6", tex="L",
        verify=f"c_NA**Rational(1, 3)*dm*Rational(1, 10**6)", explain="Edge = N_A^(1/3) marbles ≈ 8.4 × 10⁷ marbles; a mole of anything visible is enormous")),
    ("CH-4.5.F", Q("ch-metal-from-ore", "gchem.stoichiometry", "An ore is {{w}}% {{mineral}} by mass. What mass of {{el}} (kg) is in {{m}} kg of ore?",
        cases=[{"mineral": "Fe₂O₃", "el": "iron", "nFe": 2, "nO": 3, "w": 60, "m": 1000},
               {"mineral": "Fe₃O₄", "el": "iron", "nFe": 3, "nO": 4, "w": 45, "m": 500},
               {"mineral": "Fe₂O₃", "el": "iron", "nFe": 2, "nO": 3, "w": 80, "m": 250}],
        value="m*w/100*nFe*55.845/(nFe*55.845 + nO*15.999)", tex="m_{Fe}",
        verify="m*Rational(w, 100)*nFe*Rational('55.845')/(nFe*Rational('55.845') + nO*Rational('15.999'))", explain="Mass fraction of Fe in the mineral × mineral mass")),
    ("CH-4.5.F", Q("ch-ore-needed", "gchem.stoichiometry", "How many kg of ore that is {{w}}% CaCO₃ must be mined to supply {{mc}} kg of calcium?",
        given={"w": {"pick": [40, 75, 90]}, "mc": {"pick": [10, 100]}}, value="mc*(40.078 + 12.011 + 3*15.999)/40.078/(w/100)", tex="m",
        verify="mc*(Rational('40.078') + Rational('12.011') + 3*Rational('15.999'))/Rational('40.078')/Rational(w, 100)", explain="Reverse the chain: calcium → CaCO₃ by the mass ratio, then divide by the ore's purity")),
    ("CH-5.5.B", Q("ch-surface-area-cut", "gchem.kinetics", "A cube {{L}} cm on a side is cut into cubes {{l}} cm on a side. By what factor does the total surface area grow?",
        given={"L": {"pick": [1, 2, 4]}, "l": {"pick": [0.1, 0.01]}}, value="L/l", tex="\\times",
        verify="6*(L/nsimplify(l))**3*nsimplify(l)**2/(6*L**2)", explain="(L/l)³ small cubes, each 6l²: total 6L²·(L/l), so the area grows by L/l")),
    ("CH-5.5.B", facts("ch-surface-area-facts", "gchem.kinetics", [
        ("Why does powdered zinc react faster with acid than a single lump of equal mass?", "More atoms are exposed at the surface where acid can collide with them", "Powder has a lower activation energy", "Powder is at a higher temperature", "The equilibrium constant is larger"),
        ("Which change does not speed up a reaction between a gas and a solid catalyst?", "Using larger catalyst pellets of the same total mass", "Grinding the catalyst finer", "Raising the temperature", "Raising the gas pressure"),
        ("Why can flour dust explode in a mill when a sack of flour only burns slowly?", "Fine dust exposes vastly more surface to oxygen", "Dust has a different chemical formula", "Dust contains its own oxidiser", "Dust has a lower heat of combustion"),
    ], "A reaction at a surface goes as fast as collisions with that surface allow")),
    ("CH-7.5.B", Q("ch-fraction-bound", "gchem.equilibrium", "A protein binds its ligand with K_d = {{Kd}} µM. With free ligand at {{L}} µM, what fraction of the protein is bound?",
        given={"Kd": {"pick": [0.5, 2, 10]}, "L": {"pick": [0.5, 2, 20]}}, value="L/(Kd + L)", tex="\\theta",
        verify="solve(Eq(nsimplify(Kd)*Symbol('PL'), (1 - Symbol('PL'))*nsimplify(L)), Symbol('PL'))[0]",
        explain="K_d[PL] = [P][L] with [P] = 1 − [PL] (as fractions): θ = [L]/(K_d + [L])")),
    ("CH-7.5.B", Q("ch-ligand-for-fraction", "gchem.equilibrium", "K_d = {{Kd}} nM. What free ligand concentration (nM) makes the protein {{pct}}% bound?",
        given={"Kd": {"pick": [1, 5, 50]}, "pct": {"pick": [50, 90, 99]}}, value="Kd*(pct/100)/(1 - pct/100)", tex="[L]",
        verify="solve(Eq(Symbol('LL')/(Kd + Symbol('LL')), Rational(pct, 100)), Symbol('LL'))[0]",
        explain="Invert θ = L/(K_d + L): L = K_d θ/(1 − θ); 90% bound needs 9 K_d")),
    ("CH-0.6.A", facts("ch-error-type", "gchem.measurement", [
        ("The balance reads 0.012 g with nothing on it, and nobody zeroed it. What kind of error results?", "Systematic: every mass reads high", "Random: masses scatter both ways", "No error: it cancels in a mass", "A blunder that cannot be detected"),
        ("Readings of a burette at the meniscus vary slightly from trial to trial. What kind of error is that?", "Random", "Systematic, always high", "Systematic, always low", "Gross error"),
        ("A sample being weighed absorbs water from the air. Its calculated purity will be:", "Too low, a systematic error", "Too high, a systematic error", "Unaffected", "Scattered at random"),
        ("Which step removes a systematic error from a reagent's own absorbance?", "Running a reagent blank", "Doing more replicates", "Averaging more readings", "Reporting more significant figures"),
        ("Which step reduces random error in a mean?", "More replicate measurements", "A reagent blank", "Recalibrating once", "Using a different unit"),
    ], "Systematic errors bias every result the same way and need a blank or calibration; random errors average down")),
    ("CH-0.6.A", Q("ch-systematic-direction", "gchem.measurement", "A sample's true mass is {{m}} g, but the balance reads {{off}} g high on every weighing. If the percent of analyte is found as (analyte mass ÷ sample mass) and the analyte mass is measured correctly at {{a}} g, what percent is reported?",
        given={"m": {"pick": [1.000, 2.000]}, "off": {"pick": [0.010, 0.050]}, "a": {"pick": [0.250, 0.400]}}, value="100*a/(m + off)", tex="\\%",
        verify="100*nsimplify(a)/(nsimplify(m) + nsimplify(off))", explain="The inflated denominator biases the percent low, the same way every time")),
    ("CH-0.6.B", facts("ch-notebook", "gchem.measurement", [
        ("You wrote a wrong mass in your notebook. What do you do?", "Draw one line through it, write the correct value beside it, and date or initial", "Erase it", "Tear out the page", "Cover it with correction fluid"),
        ("Where should raw data be written first?", "Straight into the bound notebook", "On a paper towel, copied later", "In memory, written at the end", "Only in the final report"),
        ("Why record the room temperature and instrument settings?", "So the experiment can be repeated and the result checked", "They are never needed", "To fill the page", "Because the instructor will forget"),
        ("A control experiment is run in order to:", "Show the effect comes from the variable tested, not something else", "Make the data look better", "Replace replicates", "Avoid a blank"),
    ], "A record exists so that someone else can verify or repeat the work")),
    ("CH-0.6.B", facts("ch-procedure-design", "gchem.measurement", [
        ("To check that a new titrant concentration is right, you should first:", "Standardise it against a primary standard", "Use it straight away", "Dilute it further", "Heat it"),
        ("Why weigh by difference from a weighing bottle?", "So material left on the bottle does not count as transferred", "It is faster", "To heat the sample", "It removes random error entirely"),
        ("Why bracket an unknown's absorbance with standards?", "So the calibration covers the unknown without extrapolating", "To reduce the volume used", "To avoid a blank", "To raise the absorbance"),
    ], "Good procedures are designed so that the likely errors cannot creep in")),
    ("CH-0.6.C", facts("ch-safety-equipment", "gchem.measurement", [
        ("Concentrated acid splashes into a student's eye. First action?", "Rinse at the eyewash for at least 15 minutes", "Neutralise with base", "Rub the eye dry", "Wait to see whether it hurts"),
        ("You will dispense a volatile, toxic solvent. Where?", "In a working fume hood", "On the open bench near a window", "Over the sink", "Wherever there is space"),
        ("A large chemical spill soaks a person's clothing. Use:", "The safety shower, removing contaminated clothing", "A paper towel", "The eyewash only", "The fire blanket"),
        ("Which eye protection is required when any chemical is in use?", "Splash goggles", "Prescription glasses", "None if careful", "Sunglasses"),
    ], "Know where the eyewash, shower and extinguisher are before work starts")),
    ("CH-0.6.C", facts("ch-ghs-pictograms", "gchem.measurement", [
        ("A GHS label shows a flame over a circle. What hazard?", "Oxidiser", "Flammable", "Explosive", "Corrosive"),
        ("A GHS label shows liquid dripping onto a hand and a surface. What hazard?", "Corrosive", "Flammable", "Toxic", "Environmental"),
        ("A GHS label shows a skull and crossbones. What hazard?", "Acute toxicity", "Corrosive", "Health hazard (chronic)", "Irritant"),
        ("A GHS label shows a person's chest with a star. What hazard?", "Chronic health hazard (carcinogen, mutagen, sensitiser)", "Acute toxicity", "Explosive", "Flammable"),
        ("Which section of a safety data sheet gives first-aid measures?", "Section 4", "Section 1", "Section 9", "Section 14"),
    ], "GHS pictograms are red diamonds; the SDS has 16 sections in a fixed order")),
    ("CH-0.6.D", facts("ch-waste", "gchem.measurement", [
        ("Where does dichloromethane waste go?", "Halogenated organic waste", "Non-halogenated organic waste", "Down the sink with water", "Regular trash"),
        ("Where does acetone used for rinsing go?", "Non-halogenated organic waste", "Halogenated waste", "Aqueous heavy-metal waste", "The sink"),
        ("A solution of lead(II) nitrate is finished with. It goes:", "Into labelled heavy-metal aqueous waste", "Down the sink", "Into organic waste", "Into the trash"),
        ("Why must nitric acid waste be kept out of organic waste?", "Oxidisers and organics can react violently", "It makes the waste too dilute", "It is not hazardous", "Regulations allow mixing"),
        ("Broken glassware goes:", "Into a labelled broken-glass box", "Into paper trash", "Into a sharps container for needles only", "Down the drain"),
    ], "Sort waste so that incompatible chemicals never meet in one container")),
    ("CH-0.6.D", facts("ch-waste-2", "gchem.measurement", [
        ("A waste bottle should be:", "Labelled with its contents and kept closed", "Left open to vent", "Unlabelled to save time", "Filled to the brim"),
        ("Dilute, neutralised aqueous NaCl with no metals or organics may usually:", "Go down the drain with water, where local rules allow", "Go into halogenated waste", "Be evaporated in the hood", "Be mixed with acetone waste"),
        ("Unknown residue in an unlabelled flask should be:", "Reported and handled as hazardous until identified", "Poured into the sink", "Thrown in the trash", "Mixed into any waste bottle"),
    ], "Usual practice; local regulations decide what may go down a drain")),
    ("CH-0.6.E", Q("ch-inverse-square", "gchem.measurement", "A point source gives {{d1}} µSv/h at {{r1}} m. What is the dose rate at {{r2}} m?",
        given={"d1": {"pick": [40, 100, 400]}, "r1": {"pick": [0.5, 1]}, "r2": {"pick": [2, 3, 4]}}, value="d1*(r1/r2)^2", tex="\\dot D",
        verify="d1*(nsimplify(r1)/r2)**2", explain="Intensity spreads over 4πr²: doubling the distance quarters the dose rate")),
    ("CH-0.6.E", Q("ch-half-value-layers", "gchem.measurement", "A source gives {{d0}} µSv/h unshielded. The shield's half-value layer is {{hvl}} cm. What dose do you receive in {{t}} h behind {{x}} cm of it?",
        given={"d0": {"pick": [80, 200]}, "hvl": {"pick": [0.5, 1, 2]}, "t": {"pick": [0.5, 2]}, "x": {"pick": [1, 2, 4]}}, value="d0*0.5^(x/hvl)*t", tex="D",
        verify="d0*Rational(1, 2)**(x/nsimplify(hvl))*nsimplify(t)", explain="Each half-value layer halves the rate; dose = rate × time (time, distance, shielding)")),
]
