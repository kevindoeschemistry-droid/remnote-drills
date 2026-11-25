"""Free-energy foundations and practice for Molecular Simulation (Nov 2026), on two sources read for this:
alchemistry.org (Main Page, Free Energy Fundamentals, Best Practices, Example Free Energy Calculations; the theory
subpages were not opened) and Mey et al., "Best Practices for Alchemical Free Energy Calculations", LiveCoMS 2 (2020)
18378, now read through §12 (the framework was first built from §1-7). Unit 16 (foundations) sits before unit 8 on the
path and unit 17 (practice) after unit 9, so the ramp runs vocabulary → theory → cycles → practice. Items paraphrase
the sources' recommendations; nothing is copied."""
from opl_dsl import Q

FILE, FRAMEWORK = "md-fe-practice", "molecular-simulation"
PRACTICE = "P5"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
FE, WF, AN = "md.free-energy", "md.workflow", "md.analysis"
W = lambda *s: [f"alchemistry-wiki:{x}" for x in s]
L = lambda *s: [f"livecoms-afe:{x}" for x in s]
RT = "Rational('0.0019872043')*Rational('298.15')"


def mc(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", pace="recall", explain=explain)


UNITS = {"16": ("fe-foundations", "Free-energy foundations and expectations", ["PATH", "ALCH"], W("FUND") + L("1", "3", "4")),
         "17": ("fe-practice", "Free-energy practice: protocol, convergence and reporting", ["SAMPLE", "WORK"], W("BP") + L("7", "8", "12"))}
TOPICS = {"16.1": "Words and ideas", "16.2": "Is the calculation worth running?",
          "17.1": "Protocol choices", "17.2": "Convergence and analysis", "17.3": "Verify and report"}
UNIT_ORDER = ["statmech", "forcefield", "integrate", "thermobaro", "boundaries", "prep", "uncertainty", "fe-foundations", "fe-theory",
              "cycles", "fe-practice", "lambda", "alf", "analysis", "workflow", "lambda-adv", "electronic"]

OBJS = [
    ("MD-16.1.A", W("FUND") + L("1", "3"), "Define the vocabulary of alchemical free energies: end states, λ, decoupling versus annihilation, and phase-space overlap.",
     "Alchemical intermediates are unphysical states that bridge two physical end states; only free-energy differences are defined; neighbouring states must overlap in phase space."),
    ("MD-16.1.B", L("4"), "State the accuracy and reproducibility to expect from alchemical calculations and convert an energy error into a fold error in K.",
     "Favourable cases reach about 1–2 kcal/mol RMS error; 1.36 kcal/mol is a tenfold change in K at 298 K; repeat 2–3 times, ideally from different starting coordinates."),
    ("MD-16.2.A", L("4.5", "4.6"), "Estimate the compute a free-energy campaign needs, and decide when a pilot study or an experiment is the better use of time.",
     "Typical calculations use 20–40 or more λ states per leg; GPU throughput is a few hundred ns/day; run a small pilot before committing."),
    ("MD-16.2.B", L("5.3", "7.1.1"), "Design a perturbation network: star maps, denser networks with cycles, and how many independent cycles a network has.",
     "A star map links each ligand to one hub (N − 1 edges); a connected network with E edges on N ligands has E − N + 1 independent cycles for closure checks."),
    ("MD-17.1.A", W("BP") + L("7.2.3"), "Apply the pathway rules: soft-core for Lennard-Jones, never charges without LJ, fewest insertions, and electrostatics off before LJ.",
     "Use soft-core when LJ is removed (α = 0.5 unless there is a reason not to); remove charges before LJ or soften Coulomb faster; prefer mutating atoms to inserting them."),
    ("MD-17.1.B", L("7.1.1", "12"), "Make the relative-calculation choices: topology, atom mapping, constraints on transformed bonds and perturbation size.",
     "Single, dual or hybrid topology; keep transformations to about 1–5 heavy atoms; don't constrain bonds to transforming atoms (use about a 1 fs step); ring breaking is hard."),
    ("MD-17.1.C", L("7.1.2", "7.2.1", "7.2.2"), "Make the absolute-calculation choices: restraint type, the standard state, weak binders and net charge changes.",
     "Harmonic, flat-bottom (does not restrain rotation) or Boresch (all six rigid-body degrees of freedom); correct to 1 M; net charge changes need co-alchemical ions or corrections."),
    ("MD-17.1.D", W("BP") + L("7.2.4"), "Choose a sampling scheme and equilibrate correctly at every λ.",
     "Independent fixed-λ runs, Hamiltonian replica exchange (recommended), single-replica λ moves, or nonequilibrium switching; equilibrate each λ separately and for equal lengths."),
    ("MD-17.2.A", L("7.2.5", "8.1", "8.2"), "Detect equilibration and decorrelate data: count effectively uncorrelated samples per state.",
     "Discard the early part; N_eff = (T − t₀)/g; aim for at least about 50 per state; if T is not about 20 times t₀, the run is short."),
    ("MD-17.2.B", L("7.2.5"), "Plan what to save: the energies each estimator needs and how often to write them.",
     "TI needs dU/dλ, EXP one-direction ΔU, BAR both neighbours, MBAR every state; write roughly every 50–100 steps; set the target uncertainty before running."),
    ("MD-17.2.C", W("BP") + L("8.3", "8.4", "8.5"), "Choose and cross-check estimators and read the diagnostics: overlap, forward–reverse drift and estimator disagreement.",
     "Prefer TI, BAR or MBAR; EXP is biased; first off-diagonal overlap at least 0.03; estimators disagreeing by more than 1 kcal/mol, or forward–reverse by more than 1 kT, means not converged."),
    ("MD-17.2.D", W("BP") + L("8.4", "8.7"), "Compute an uncertainty from independent repeats and combine the uncertainties of independent legs.",
     "The gold standard is independent copies and their standard error; an estimator's own error assumes uncorrelated data and usually underestimates; independent legs add in quadrature."),
    ("MD-17.3.A", W("BP") + L("8.5", "12"), "Verify a result: alternate cycles, cycle closure, repeat spread against the error bar, and the checklist's red flags.",
     "Results from different cycles should agree; repeats should differ by about what their error bars allow; standard error above 1 kcal/mol or |ΔΔG| above about 15 kcal/mol is suspect."),
    ("MD-17.3.B", L("8.7"), "Report a benchmark the way the field expects: replicates, MUE and RMSE, correlation and ranking statistics, and honest plots.",
     "At least three replicates; RMSE and MUE for relative results (correlation depends on sign convention); bootstrap statistics; equal axes with 1 and 2 kcal/mol bands."),
    ("MD-17.3.C", L("8.6", "7.2.6"), "Diagnose common failures from their symptoms.",
     "Ligand leaving the site, inconsistent estimators, poor replica mixing, slow torsions, rough ΔG(λ), drift, and starting-pose dependence; wrong binding modes are common."),
]

ADD = [
    ("MD-16.1.A", mc("fe-vocab", FE, [
        ("Why are alchemical intermediate states needed?", "Each neighbouring pair must overlap in phase space for the estimators to converge", "They are physical states measured in experiments", "They make the force field more accurate", "They remove the need for a thermodynamic cycle"),
        ("Turning off a molecule's interactions with its surroundings while keeping its internal ones is:", "Decoupling", "Annihilation", "Restraining", "Equilibration"),
        ("Turning off interactions within the molecule as well as with its surroundings is:", "Annihilation", "Decoupling", "Soft-core", "Replica exchange"),
        ("Free-energy calculations give:", "Only differences between states, never an absolute value on their own", "Absolute free energies directly", "Enthalpies only", "Rates of binding"),
        ("The 'alchemical' in alchemical free energy refers to:", "Transforming one chemical species into another along an unphysical path", "Using quantum mechanics", "Running at very high temperature", "Simulating real binding events directly"),
    ], "Intermediates bridge end states; only differences are defined; overlap is what makes estimators work")),
    ("MD-16.1.A", mc("fe-vocab-2", FE, [
        ("Why not just simulate the ligand binding and unbinding directly?", "Unbinding can take microseconds to seconds, far beyond routine MD", "It is less accurate than any alchemical method by definition", "Force fields cannot describe unbound ligands", "It requires quantum mechanics"),
        ("In a relative calculation, λ = 0 and λ = 1 correspond to:", "The two physical end states (ligand A and ligand B)", "Two temperatures", "The bound and unbound poses", "The start and end of the run"),
        ("Because free energy is a state function, the choice of alchemical path changes:", "Efficiency, not the answer (given converged sampling)", "The answer", "Nothing at all", "The force field"),
        ("Absolute and relative binding calculations differ in that absolute ones:", "Remove the ligand from its environment instead of mutating A into B", "Need no thermodynamic cycle", "Are always cheaper", "Need no restraints ever"),
    ], "Alchemy avoids slow physical events by going around them")),
    ("MD-16.1.B", Q("fe-error-fold", FE, "An error of {{d}} kcal/mol in a binding ΔG at 298.15 K corresponds to what fold error in K?",
        given={"d": {"pick": [0.5, 1, 1.5, 2]}}, value="exp(d/(0.0019872043*298.15))", tex="\\times", verify=f"exp(nsimplify(d)/({RT}))",
        explain="K changes by exp(ΔΔG/RT): 1 kcal/mol is about 5.4-fold and 1.36 kcal/mol tenfold at room temperature")),
    ("MD-16.1.B", mc("fe-expect", FE, [
        ("In favourable cases, alchemical binding predictions reach an RMS error of about:", "1–2 kcal/mol", "0.01 kcal/mol", "5–10 kcal/mol", "Exactly zero"),
        ("How many repeats of a protein–ligand calculation are suggested as a minimum?", "Two or three, ideally from different starting coordinates", "One is enough", "Fifty", "None if MBAR reports an error bar"),
        ("Simple hydration free energies are highly repeatable; protein–ligand results usually are:", "Much less repeatable, because slow protein and ligand motions dominate", "Equally repeatable", "Perfectly repeatable", "Impossible to repeat"),
        ("When reporting accuracy, you should state:", "Which error you mean: shifted or unshifted ΔG, or ΔΔG", "Only the best ligand", "Only the correlation", "Nothing; error is obvious"),
    ], "Expect 1–2 kcal/mol at best, and measure repeatability yourself")),
    ("MD-16.2.A", Q("fe-campaign-cost", WF, "A campaign has {{nl}} ligand transformations, each with complex and solvent legs of {{k}} λ states × {{t}} ns, run in {{r}} repeats. At {{rate}} ns/day per GPU, how many GPU-days?",
        given={"nl": {"pick": [10, 20, 40]}, "k": {"pick": [16, 24, 32]}, "t": {"pick": [5, 10]}, "r": {"pick": [3]}, "rate": {"pick": [200, 400]}},
        value="nl*2*k*t*r/rate", tex="GPU\\text{-}days", verify="Rational(nl*2*k*t*r, rate)",
        explain="Cost scales with transformations × legs × λ states × length × repeats; this is why a pilot on a few ligands comes first")),
    ("MD-16.2.A", mc("fe-worth-it", WF, [
        ("Before committing to a large free-energy campaign on a new target, you should:", "Run a short pilot on a few ligands to test feasibility and accuracy", "Run every ligand at once", "Skip benchmarking", "Assume published accuracy applies"),
        ("Typical alchemical calculations use how many λ states per leg?", "About 20–40 or more", "Exactly 2", "About 1000", "1"),
        ("A computed answer is not worth the cost when:", "Measuring the compound would be cheaper and faster", "The target is a protein", "The ligand is charged", "MBAR is available"),
        ("Retrospective testing on known ligands of the same target and series is used to:", "Estimate how well prospective predictions will do", "Replace experiments entirely", "Choose the force field automatically", "Avoid repeats"),
    ], "Weigh compute against experiment and test the setup on known data first")),
    ("MD-16.2.B", Q("fe-network-cycles", FE, "A connected perturbation network joins {{n}} ligands with {{ed}} edges. How many independent closed cycles does it have for cycle-closure checks?",
        given={"n": {"pick": [8, 10, 12]}, "ed": {"pick": [14, 16, 20]}}, value="ed - n + 1", tex="cycles", final=True, verify="ed - n + 1",
        explain="Independent cycles = E − N + 1 (a star map, with E = N − 1, has none, so it cannot be checked by closure)")),
    ("MD-16.2.B", mc("fe-network", FE, [
        ("A star map connects:", "Every ligand to one central reference ligand", "Every ligand to every other", "Ligands in a single chain", "Only ligands with the same charge"),
        ("Star maps suit:", "Large sets, because they use the fewest edges", "Sets where cycle closure is essential", "Absolute calculations only", "Charged ligands only"),
        ("Denser, better-connected networks are favoured because:", "Cycles allow closure checks and errors average out", "They need fewer simulations", "They avoid soft-core", "They need no repeats"),
        ("For N ligands, a star map has how many edges?", "N − 1", "N(N − 1)/2", "2N", "N²"),
    ], "Network shape trades cost for redundancy")),
    ("MD-17.1.A", mc("fe-path-rules", FE, [
        ("A setup removes a ligand's LJ interactions while its partial charges stay on. The problem:", "Unphysically strong electrostatics with no steric repulsion", "Nothing", "Too few λ states for electrostatics", "The barostat fails"),
        ("When removing LJ interactions, you should use:", "A soft-core potential", "A linear path with no soft-core", "A shifted potential that changes with λ", "No intermediate states"),
        ("A safe order for decoupling a molecule is:", "Turn off electrostatics first, then LJ", "Turn off LJ first, then electrostatics", "Both at once linearly", "Change the box size"),
        ("To keep a relative calculation efficient, you should:", "Mutate existing atoms rather than insert or delete many atoms", "Insert as many atoms as possible", "Use one λ state", "Turn off soft-core"),
        ("Electrostatic transformations usually need ___ λ states compared with LJ insertions:", "Fewer", "Many more", "Exactly the same number", "None"),
    ], "The wiki's and LiveCoMS's pathway rules prevent endpoint catastrophes")),
    ("MD-17.1.A", mc("fe-path-rules-2", FE, [
        ("The LiveCoMS paper's default soft-core α, unless there is a reason otherwise, is:", "0.5", "0", "10", "1000"),
        ("A linear λ path is fine when:", "The repulsive cores stay on throughout", "Atoms are being inserted", "Atoms are being deleted", "Never"),
        ("Intramolecular interactions of the changing molecule can usually:", "Stay on, as long as the total potential changes smoothly", "Never stay on", "Be removed first", "Be ignored entirely"),
        ("Restraints between ligand and protein help an intermediate state converge because they:", "Shrink the space the ligand must explore (their free energy must be added back)", "Change the force field", "Remove the need for repeats", "Make the ligand bind tighter in reality"),
    ], "Keep cores on as long as possible and soften what disappears")),
    ("MD-17.1.B", mc("fe-relative-choices", FE, [
        ("Bonds involving atoms being transformed should be:", "Left unconstrained, with a timestep of about 1 fs", "Constrained with SHAKE", "Removed", "Doubled in force constant"),
        ("The checklist suggests relative transformations of about:", "1–5 heavy atoms", "20–30 heavy atoms", "Whole scaffolds", "Zero atoms"),
        ("Which change is particularly hard for relative calculations?", "Breaking or forming a ring", "Changing a methyl to an ethyl", "Changing a partial charge", "Adding a fluorine"),
        ("Single topology uses a ___ maximum common substructure than dual topology:", "More permissive", "Stricter", "Identical", "Irrelevant"),
        ("A software package that handles only one kind of topology means you should:", "Check what it supports before planning the perturbations", "Ignore topology", "Always use dual topology", "Avoid relative calculations"),
    ], "Small, well-mapped changes on unconstrained bonds converge")),
    ("MD-17.1.B", mc("fe-topology-pick", FE, [
        ("Two ligands share a core and differ by a chloro versus methyl group. The best route is:", "A relative calculation mutating the substituent", "Two absolute calculations", "A direct binding simulation", "A docking score"),
        ("A planned edge changes a phenyl into a cyclohexyl and adds six heavy atoms. You should:", "Split it through intermediate ligands into smaller steps", "Run it as one edge", "Use one λ window", "Constrain all bonds"),
        ("A transformation predicts |ΔΔG| = 18 kcal/mol. The checklist says:", "Treat it as likely unreliable and check sampling", "Accept it", "Report it as a strong binder", "Halve it"),
    ], "Plan edges a calculation can actually converge")),
    ("MD-17.1.C", mc("fe-restraints", FE, [
        ("A flat-bottom restraint keeps the ligand near the site but does not restrain:", "Its rotation", "Its position", "Its temperature", "Its charges"),
        ("Boresch restraints restrain:", "All six rigid-body degrees of freedom of the ligand relative to the protein", "Only the distance", "Only the protein backbone", "Nothing"),
        ("Absolute binding free energies are reported relative to a standard state of:", "1 M (1 mol/L)", "1 mM", "Pure ligand", "The simulation box concentration"),
        ("Reference atoms for restraints should be chosen in:", "Well-defined, rigid parts of the ligand and protein", "Floppy loops", "Water molecules", "Ions"),
        ("Restraints can reduce sampling, but they can also:", "Block alternative binding modes", "Change the force field", "Remove the need for a standard-state correction", "Make results exact"),
    ], "Know what each restraint holds and correct for it")),
    ("MD-17.1.C", mc("fe-charge-weak", FE, [
        ("A transformation changes the ligand's net charge. A known option is:", "Co-alchemical ions or an analytical charge correction (best practice is unresolved)", "Ignore it; periodic boxes cancel it", "Remove all ions", "Use a smaller box"),
        ("For a weak binder that may leave the site during decoupling, you can:", "Use flat-bottom or harmonic restraints sized to the site", "Use no restraints and hope", "Raise the temperature", "Delete the protein"),
        ("Charge changes are a problem in periodic simulations because of:", "Finite-size artefacts in electrostatics", "Soft-core", "Thermostats", "Hydrogen mass"),
        ("The 'bound state' must be defined carefully for weak binders because:", "Different assays (ITC, SPR, fluorescence) define binding differently", "Simulations cannot define it", "It is always obvious", "It changes the force field"),
    ], "Charge changes and weak binders are where absolute calculations go wrong")),
    ("MD-17.1.D", mc("fe-sampling-scheme", FE, [
        ("Which sampling scheme does the LiveCoMS paper recommend for most users?", "Hamiltonian replica exchange between λ states", "Nonequilibrium switching only", "A single replica moving through λ", "One long run at λ = 0"),
        ("Independent fixed-λ runs are acceptable when:", "Conformational sampling is fast", "The ligand flips binding modes", "Charges change", "Never"),
        ("For beginners the wiki recommends:", "Equilibrium methods with fixed-λ simulations", "Nonequilibrium pulling", "Expanded ensemble first", "Gibbs sampling"),
        ("Nonequilibrium switching and single-replica λ moves are:", "Promising but less established", "The safest default", "Forbidden", "Identical to TI"),
    ], "Replica exchange is the robust default")),
    ("MD-17.1.D", mc("fe-equilibrate", FE, [
        ("Equilibrating only at λ = 0 and starting all other states from that structure can:", "Leave intermediate states kinetically trapped", "Save time with no risk", "Improve overlap", "Remove the need for repeats"),
        ("Each λ state should be equilibrated:", "Separately, for equal lengths", "Only at the endpoints", "Not at all", "Only if it has charges"),
        ("A shifted potential whose parameters change with λ is risky because:", "Different states get different errors that distort ΔG", "It is too slow", "It needs quantum mechanics", "It always crashes"),
        ("Setup scripts for many calculations should be:", "Automated and kept under version control", "Edited by hand each time", "Deleted after use", "Shared without testing"),
    ], "Equilibrate every state and automate the setup")),
    ("MD-17.2.A", Q("fe-neff", AN, "A λ state ran {{T}} ns. Equilibration was detected at {{t0}} ns and the statistical inefficiency is g = {{g}} ps. How many effectively uncorrelated samples remain?",
        given={"T": {"pick": [5, 10, 20]}, "t0": {"pick": [0.5, 1]}, "g": {"pick": [20, 50, 100]}}, value="(T - t0)*1000/g", tex="N_{\\text{eff}}",
        verify="(nsimplify(T) - nsimplify(t0))*1000/nsimplify(g)", explain="N_eff = (T − t₀)/g; the paper suggests at least about 50 per state for BAR or MBAR")),
    ("MD-17.2.A", mc("fe-equil-detect", AN, [
        ("Automated equilibration detection chooses the cut-off that:", "Maximises the number of effectively uncorrelated samples", "Removes exactly half the data", "Keeps all the data", "Minimises the free energy"),
        ("If the run length is not at least about 20 times the detected equilibration time:", "The data may be too short", "The run is converged", "Use EXP instead", "Lower the temperature"),
        ("Subsampling at the statistical inefficiency g means:", "Keeping roughly one sample every g", "Keeping every sample", "Deleting the last g ps", "Averaging g runs"),
        ("With coupled replica exchange, the statistical inefficiency should be:", "A common value across states", "Different for each state", "Ignored", "Set to 1"),
    ], "Discard the biased start, then thin to independent samples")),
    ("MD-17.2.B", Q("fe-frames", WF, "A {{ns}} ns λ state at a 2 fs timestep writes its energies every {{k}} steps. How many energy frames does it write?",
        given={"ns": {"pick": [5, 10, 20]}, "k": {"pick": [50, 100, 500]}}, value="ns*500000/k", tex="frames", final=True, verify="ns*500000/k",
        explain="Steps = time/timestep = ns × 500 000 at 2 fs; writing every 50–100 steps roughly matches the rate of new uncorrelated information")),
    ("MD-17.2.B", mc("fe-what-to-save", AN, [
        ("TI needs which saved quantity?", "dU/dλ at each state", "ΔU to every state", "Only the trajectory", "Nothing"),
        ("BAR needs:", "ΔU to both neighbouring states", "dU/dλ only", "ΔU to every state", "Only one direction"),
        ("MBAR needs:", "The energy of each sample evaluated at every state", "Only neighbouring states", "dU/dλ only", "Only endpoint energies"),
        ("Before starting production, the paper recommends setting:", "A target statistical uncertainty, such as 0.2 kcal/mol", "A fixed run of one week", "Nothing; run until it looks good", "The final answer"),
    ], "Save the right energies, often enough, toward a stated target")),
    ("MD-17.2.C", Q("fe-overlap-pick", AN, "The first off-diagonal entries of an MBAR overlap matrix, between neighbouring states 0–1, 1–2, 2–3 and 3–4, are {{a}}, {{b}}, {{c}} and {{d}}. Between which neighbouring states should you add a λ state (the paper's threshold is 0.03)?",
        cases=[{"a": 0.12, "b": 0.02, "c": 0.09, "d": 0.15, "k": 1}, {"a": 0.08, "b": 0.11, "c": 0.07, "d": 0.01, "k": 3},
               {"a": 0.005, "b": 0.10, "c": 0.12, "d": 0.06, "k": 0}, {"a": 0.09, "b": 0.06, "c": 0.025, "d": 0.10, "k": 2}],
        choice=["States 0 and 1", "States 1 and 2", "States 2 and 3", "States 3 and 4"], correct="k",
        verify="[a, b, c, d].index(Min(a, b, c, d))", pace="recall", explain="Neighbouring overlap below about 0.03 is unreliable: add or respace states there")),
    ("MD-17.2.C", mc("fe-estimators", AN, [
        ("Which estimator is biased and noisy when energy differences are large?", "EXP (Zwanzig, one-sided)", "BAR", "MBAR", "TI with many states"),
        ("When chaining BAR across states, the uncertainty should be propagated by:", "Bootstrapping", "Simple addition of error bars", "Ignoring correlation", "Taking the largest one"),
        ("For TI, beginners are advised to use:", "The trapezoid rule, adding a few states where dU/dλ curves", "Monte Carlo integration", "One state", "EXP instead"),
        ("WHAM is not the first choice for alchemical data because:", "It introduces binning error", "It is biased like EXP", "It needs dU/dλ", "It cannot use replica exchange"),
        ("Two estimators on the same data disagree by more than 1 kcal/mol. This suggests:", "Poor convergence", "A good result", "A software bug only", "The force field is wrong"),
        ("Forward and reverse estimates differ by more than about 1 kT. This suggests:", "Poor convergence", "Perfect convergence", "Too many λ states", "Nothing"),
    ], "Use robust estimators and treat disagreement as a warning")),
    ("MD-17.2.D", Q("fe-leg-error", AN, "A relative ΔΔG comes from a complex leg with standard error {{s1}} kcal/mol and an independent solvent leg with standard error {{s2}} kcal/mol. What is the standard error of ΔΔG?",
        given={"s1": {"pick": [0.15, 0.3, 0.4]}, "s2": {"pick": [0.05, 0.1, 0.2]}}, value="sqrt(s1^2 + s2^2)", tex="\\sigma",
        verify="sqrt(nsimplify(s1)**2 + nsimplify(s2)**2)", explain="Independent uncertainties add in quadrature; the complex leg usually dominates")),
    ("MD-17.2.D", Q("fe-repeat-se", AN, "Three independent repeats give ΔΔG = {{a}}, {{b}} and {{c}} kcal/mol. What is the standard error of their mean?",
        cases=[{"a": -1.2, "b": -0.8, "c": -1.0}, {"a": 0.4, "b": 0.9, "c": 0.5}, {"a": -2.1, "b": -2.6, "c": -1.9}, {"a": 1.5, "b": 1.1, "c": 1.6}],
        value="std([a, b, c])/sqrt(3)", tex="SE", verify="sqrt(((nsimplify(a)-(nsimplify(a)+nsimplify(b)+nsimplify(c))/3)**2 + (nsimplify(b)-(nsimplify(a)+nsimplify(b)+nsimplify(c))/3)**2 + (nsimplify(c)-(nsimplify(a)+nsimplify(b)+nsimplify(c))/3)**2)/2)/sqrt(3)",
        explain="Sample standard deviation over √n: the error that independent copies reveal, which MBAR's own error bar often understates")),
    ("MD-17.3.A", Q("fe-repeat-consistent", AN, "Two repeats give {{x1}} ± {{s1}} and {{x2}} ± {{s2}} kcal/mol. Is their difference consistent with the stated errors (within 2σ of the difference)?",
        cases=[{"x1": -1.0, "s1": 0.2, "x2": -1.3, "s2": 0.2, "k": 0}, {"x1": -1.0, "s1": 0.1, "x2": -2.0, "s2": 0.1, "k": 1},
               {"x1": 0.5, "s1": 0.3, "x2": 1.4, "s2": 0.3, "k": 1}, {"x1": 2.0, "s1": 0.4, "x2": 2.6, "s2": 0.3, "k": 0}],
        choice=["Consistent", "Not consistent: the error bars are too small"], correct="k",
        verify="0 if Abs(nsimplify(x1) - nsimplify(x2)) <= 2*sqrt(nsimplify(s1)**2 + nsimplify(s2)**2) else 1", pace="quick",
        explain="Differences between repeats bigger than the propagated error mean the error bars underestimate the real uncertainty")),
    ("MD-17.3.A", Q("fe-cycle-closure-3", FE, "Around a three-ligand cycle the edges give ΔΔG(A→B) = {{ab}}, ΔΔG(B→C) = {{bc}} and ΔΔG(C→A) = {{ca}} kcal/mol. What is the cycle-closure error?",
        cases=[{"ab": -1.2, "bc": 0.6, "ca": 0.9}, {"ab": 0.8, "bc": -1.5, "ca": 0.4}, {"ab": 2.1, "bc": -0.7, "ca": -1.1}, {"ab": -0.5, "bc": -0.6, "ca": 1.4}],
        value="ab + bc + ca", tex="kcal/mol", verify="nsimplify(ab) + nsimplify(bc) + nsimplify(ca)",
        explain="A state function sums to zero around a closed cycle; a large residual points to undersampled edges")),
    ("MD-17.3.B", Q("fe-mue", AN, "Predicted versus experimental ΔG (kcal/mol) for four ligands: ({{p1}}, {{e1}}), ({{p2}}, {{e2}}), ({{p3}}, {{e3}}), ({{p4}}, {{e4}}). What is the mean unsigned error?",
        cases=[{"p1": -8.1, "e1": -7.5, "p2": -9.4, "e2": -9.9, "p3": -7.0, "e3": -7.2, "p4": -10.2, "e4": -9.0},
               {"p1": -6.5, "e1": -7.4, "p2": -8.0, "e2": -8.1, "p3": -9.6, "e3": -8.8, "p4": -7.7, "e4": -7.0}],
        value="(abs(p1-e1)+abs(p2-e2)+abs(p3-e3)+abs(p4-e4))/4", tex="MUE",
        verify="(Abs(nsimplify(p1)-nsimplify(e1))+Abs(nsimplify(p2)-nsimplify(e2))+Abs(nsimplify(p3)-nsimplify(e3))+Abs(nsimplify(p4)-nsimplify(e4)))/4",
        explain="MUE and RMSE are the headline errors for relative results; correlation statistics depend on the sign convention")),
    ("MD-17.3.B", mc("fe-reporting", AN, [
        ("For relative free energies, report errors as:", "RMSE and MUE (correlation depends on the sign convention)", "Pearson R only", "The best edge only", "Nothing"),
        ("Correlation and ranking statistics (R², Kendall τ) should be given with:", "Bootstrapped uncertainties", "No uncertainty", "Only the p-value", "Only the slope"),
        ("A scatter plot of predicted against experimental values should have:", "Equal axis ranges, 1:1 aspect ratio and 1 and 2 kcal/mol bands", "Different axis ranges", "Several datasets overlaid", "No error bars"),
        ("A study with fewer than about 10 ligands is better shown as:", "A bar plot", "A scatter plot with R²", "A pie chart", "A single number"),
        ("How many replicates does the reporting section ask for?", "At least three, from uncorrelated starting points", "One", "Two from the same start", "None"),
    ], "Report what lets a reader judge the result")),
    ("MD-17.3.C", mc("fe-diagnose", AN, [
        ("ΔG(λ) is jagged with sudden jumps between neighbouring states. The likely cause:", "Poor overlap or a rare slow event at those states", "Perfect sampling", "Too many repeats", "A correct soft-core"),
        ("In the decoupled state, the ligand drifts out of the pocket. You should:", "Add or tighten a restraint and correct for it", "Ignore it", "Raise the temperature", "Remove the protein"),
        ("Replicas in Hamiltonian replica exchange rarely swap between two states. This shows:", "Poor overlap between those states", "Excellent mixing", "Too many λ states", "Correct convergence"),
        ("Results change with the starting pose. This suggests:", "Slow binding-mode or protein motions are not sampled", "Convergence", "A good force field", "Nothing"),
        ("A torsion in the ligand is rarely visited in some states. This can cause:", "Biased free energies from unsampled conformations", "Faster convergence", "Better overlap", "No effect"),
    ], "Every symptom points at a sampling problem to fix before trusting the number")),
    ("MD-17.3.C", mc("fe-binding-mode", FE, [
        ("Docking is good at producing sterically reasonable poses but poor at:", "Identifying the dominant binding mode", "Producing any pose", "Placing hydrogens", "Running fast"),
        ("In the SAMPL HIV integrase challenge, most submissions:", "Placed more than half the ligands in the wrong site", "Were within 0.1 kcal/mol", "Used no docking", "Matched experiment perfectly"),
        ("A relative calculation can give different answers depending on:", "The starting binding mode", "The random number generator only", "The output format", "Nothing"),
        ("To find stable binding modes before free-energy runs, you can:", "Run short MD from several docked poses and keep the stable ones", "Trust the top docking score", "Pick a pose at random", "Skip this step"),
    ], "A wrong binding mode gives a precise wrong answer")),
]
