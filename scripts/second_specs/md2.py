"""Second question types for the Molecular Simulation objectives md.py left single, written from the Hayes group's own
orientation repository (RyanHayes-Lab/Orientation, all nine files read Nov 2026) and its lambda-dynamics-examples
templates. These are the tool- and project-specific objectives md.py deferred: CHARMM file formats and scripting,
ALF and BLaDE settings, the T4 lysozyme setup, and the hpc3 cluster and SLURM.

Every number a card states comes from the orientation text or the example run files, and the arithmetic is recomputed
by the verifier from the givens. A verify expression must not contain a comprehension or a generator: inside one,
neither the case fields nor the verifier's own names (Rational, nsimplify) are visible, so unroll the terms. Lab-internal paths, accounts and people are not drilled. MD-15.1.A reuses an
Electronic Structure template, since that framework now owns basis-set counting.
"""
from opl_dsl import Q

FILE, FRAMEWORK = "md-hayes", "molecular-simulation"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
FF, PREP, FE, LAM, ALF, ANA, WF, ADV = ("md.forcefields", "md.prep", "md.free-energy", "md.lambda",
                                        "md.lambda", "md.analysis", "md.workflow", "md.lambda")
UNC, BND = "md.analysis", "md.boundaries"


def facts(name, skill, rows, explain, skillq="{{q}}"):
    return Q(name, skill, skillq, pace="recall",
             cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


ADD = [
    # ── unit 2 force fields ──────────────────────────────────────────────
    ("MD-2.2.A", facts("mdh-which-file", FF, [
        ("Which file says that a residue's CB-CG bond has an equilibrium length of 1.53 angstrom?", "The parameter file (.prm)", "The topology file (.rtf)", "The structure file (.psf)", "The coordinate file (.crd)"),
        ("Which file says which atoms exist in a residue and how they are connected?", "The topology file (.rtf)", "The parameter file (.prm)", "The coordinate file (.crd)", "The stream file (.str)"),
        ("Which file holds the whole system's atom, bond, angle and dihedral list after patching?", "The structure file (.psf)", "The topology file (.rtf)", "The parameter file (.prm)", "The coordinate file (.crd)"),
        ("Which file is preferred over a PDB for coordinates in CHARMM, because PDB has an atom-count limit?", "The coordinate file (.crd)", "The structure file (.psf)", "The parameter file (.prm)", "The topology file (.rtf)"),
        ("What does toppar.str do?", "Streams the list of topology and parameter files to read", "Holds the coordinates", "Holds the box size", "Runs the dynamics"),
    ], "Roughly: the RTF says which terms are in the energy function, the PRM says what the constants in them are, and the PSF is the assembled system")),
    ("MD-2.3.A", facts("mdh-param-origin", FF, [
        ("A protein force field's partial charges are usually fitted to what?", "Quantum interaction energies with water, and condensed-phase properties", "Crystal structures alone", "Vibrational frequencies alone", "Nothing: they are formal charges"),
        ("Why can a water model not be swapped freely between force fields?", "The protein parameters were fitted alongside one water model, so the balance is lost", "Water models are proprietary", "They have different numbers of atoms, which CHARMM forbids", "They use different units"),
        ("Torsion parameters are generally fitted last because they:", "Absorb the residual error once nonbonded and bonded terms are set", "Are the least important", "Cannot be computed", "Are taken from experiment"),
        ("A force field's accuracy for a property it was never fitted to is:", "An extrapolation that has to be tested, not assumed", "Guaranteed by transferability", "Exact", "Irrelevant"),
    ], "A force field is a fitted, balanced set: the parameters are not independently meaningful, which is why mixing sources is risky")),
    ("MD-2.3.B", Q("mdh-penalty-decide", FF, "A CGenFF assignment reports a charge penalty of {{cp}} and a parameter penalty of {{pp}}. On the usual reading (under 10 fine, 10-50 worth checking, over 50 needs reparameterisation), how many of the two exceed 50?",
        given={"cp": {"pick": [3, 12, 45, 120, 260]}, "pp": {"pick": [0, 8, 55, 90]}},
        value="(cp > 50 ? 1 : 0) + (pp > 50 ? 1 : 0)", tex="count", final=True,
        verify="(1 if cp > 50 else 0) + (1 if pp > 50 else 0)",
        explain="The penalties are the program's own confidence, not an error bar: a high one means the analogy it used was poor and the parameter needs quantum validation")),
    # ── unit 5 boundaries ────────────────────────────────────────────────
    ("MD-5.1.C", facts("mdh-pbc-artifacts", BND, [
        ("Why are periodic boundaries preferred to a droplet of water?", "A droplet has a surface, and surface water distorts the solute", "Periodic boundaries have no artifacts", "Droplets are more expensive", "Droplets cannot be simulated"),
        ("Which case needs more padding than the usual 10 angstrom?", "A strongly charged molecule such as RNA", "A small neutral peptide", "A rigid protein", "A lipid tail"),
        ("A periodic artifact that remains however large the box is made:", "None: they shrink with box size, which is how you test for them", "Self-interaction of the net charge", "Surface tension", "The Jacobian"),
        ("The standard test for a periodic artifact is to:", "Repeat the calculation in a larger box and see whether the answer moves", "Change the force field", "Lower the temperature", "Remove the ions"),
    ], "Both choices have artifacts; periodic ones are smaller and, unlike a surface, they can be tested by changing the box")),
    # ── unit 6 preparation ───────────────────────────────────────────────
    ("MD-6.1.D", Q("mdh-box-edge", PREP, "A protein's longest extent is {{ext}} angstrom. With an edge distance of {{pad}} angstrom of water on each side, what cubic box edge is needed (angstrom)?",
        given={"ext": {"pick": [34, 42, 55, 61]}, "pad": {"pick": [10, 12, 15]}},
        value="ext + 2*pad", tex="L", final=True, verify="ext + 2*pad",
        explain="Ten angstrom each side is the usual choice, which puts 20 angstrom between periodic images of the solute; the unfolded pentapeptide boxes are instead fixed (40 angstrom) because the peptide's extent fluctuates")),
    ("MD-6.2.A", facts("mdh-stage-purpose", PREP, [
        ("Why is the first equilibration run at constant volume rather than constant pressure?", "The added water has to relax before the box size means anything", "Constant pressure is slower", "The barostat is unavailable", "The temperature is wrong at constant pressure"),
        ("What is relaxed in the second, constant-pressure stage?", "The box volume, and so the density", "The protonation states", "The force field", "The timestep"),
        ("Restraints on the solute during early equilibration are there to:", "Let solvent relax without the solute drifting from the starting structure", "Speed up the integrator", "Fix the temperature", "Remove the need for minimisation"),
        ("Minimisation before dynamics is needed because:", "A bad contact in the starting structure would give a huge force and crash the integrator", "It equilibrates the temperature", "It sets the density", "It assigns velocities"),
    ], "Each stage relaxes one thing that the next stage assumes: contacts, then solvent, then volume")),
    ("MD-6.2.C", facts("mdh-equil-signal", PREP, [
        ("The density is still drifting upward at the end of the constant-pressure run. The reading:", "Equilibration is not finished; extend it before production", "It is converged, since the temperature is stable", "The barostat is broken", "The force field is wrong"),
        ("Which observable is slowest to equilibrate in a solvated protein?", "Water in buried pockets and side-chain packing", "The instantaneous temperature", "The total energy", "The box angles"),
        ("Equilibration should be judged on:", "The property the study will report, not just energy and temperature", "The total energy alone", "The temperature alone", "Wall-clock time"),
        ("Crystallographic waters are often kept because:", "Buried water relaxes slowly, so added water may take a long time to fill those pockets", "They are cheaper than added water", "CHARMM-GUI requires them", "They set the density"),
    ], "A flat energy trace is necessary, not sufficient: the slow coordinate is usually the one the study cares about")),
    # ── unit 7 uncertainty ───────────────────────────────────────────────
    ("MD-7.2.D", Q("mdh-bootstrap-width", UNC, "A bootstrap over {{nb}} resamples gives a derived quantity whose resampled values have a standard deviation of {{sd}} kcal/mol. What is the width of the symmetric 95 percent interval (kcal/mol), using 1.96 standard deviations?",
        given={"nb": {"pick": [200, 1000, 5000]}, "sd": {"pick": [0.12, 0.3, 0.45, 0.8]}},
        value="2*1.96*sd", tex="width", verify="2*Rational(196, 100)*nsimplify(sd)",
        explain="The resample count sets how finely the percentiles are resolved, not the width; the width comes from the spread, and for correlated data the resampling must be done on blocks")),
    ("MD-7.3.A", facts("mdh-hidden-error", UNC, [
        ("Five independent runs agree to 0.05 kcal/mol but disagree with experiment by 3 kcal/mol. The likely cause:", "A systematic error — force field, protonation or construct — that no error bar reveals", "Too few samples", "A bad random seed", "The estimator"),
        ("A tight error bar from one long run can still be wrong because:", "The run may never have left one basin, so its average is of that basin", "Error bars are always wrong", "Long runs drift", "The integrator loses energy"),
        ("The cheapest check for a trapped run is:", "Independent runs from different starting structures", "A longer run from the same start", "A smaller timestep", "A larger box"),
        ("Statistical uncertainty tells you:", "How much the answer would move if you sampled more of the same ensemble", "How close the answer is to the truth", "Whether the force field is right", "Whether the protonation is right"),
    ], "The error bar measures the sampling, not the model; only a different starting point or a different model exposes the rest")),
    # ── unit 8 estimators and pathways ───────────────────────────────────
    ("MD-8.3.A", Q("mdh-bar-shift", FE, "In BAR's self-consistent condition, the forward and reverse Fermi-weighted counts are equal. With {{nf}} forward and {{nr}} reverse samples, what offset (in kT) does the equal-sample-count term contribute, as ln of the ratio of reverse to forward counts?",
        given={"nf": {"pick": [200, 500, 1000]}, "nr": {"pick": [200, 800, 2000]}},
        value="log(nr/nf)", tex="\\ln(n_r/n_f)", verify="log(Rational(nr, nf))",
        explain="BAR carries the sample-count ratio explicitly, which is part of why it is the maximum-likelihood estimator for two states while a one-sided exponential average is not")),
    ("MD-8.3.B", facts("mdh-mbar-relations", FE, [
        ("MBAR applied to exactly two states reduces to:", "BAR", "WHAM", "Thermodynamic integration", "The Zwanzig relation"),
        ("WHAM is recovered from MBAR when:", "The energies are binned into a histogram along a coordinate", "There are two states", "The samples are uncorrelated", "The states are equally spaced"),
        ("MBAR's inputs are:", "The energy of every sample evaluated in every state", "Only each sample's own state energy", "The free energies", "The overlap matrix"),
        ("MBAR needs uncorrelated samples because:", "Its uncertainty estimate assumes independence, so correlated input understates the error", "It cannot run otherwise", "Correlated samples bias the free energy badly", "It is a histogram method"),
    ], "One estimator, read three ways: two states give BAR, binning gives WHAM, and the general case reweights every sample to every state")),
    ("MD-8.3.C", Q("mdh-overlap-worst", FE, "An MBAR overlap matrix has nearest-neighbour overlaps {{v1}}, {{v2}}, {{v3}} and {{v4}} between consecutive lambda states. How many of the four fall below the usual 0.03 threshold?",
        cases=[{"v1": 0.21, "v2": 0.02, "v3": 0.18, "v4": 0.004},
               {"v1": 0.09, "v2": 0.11, "v3": 0.07, "v4": 0.14},
               {"v1": 0.3, "v2": 0.015, "v3": 0.26, "v4": 0.22},
               {"v1": 0.012, "v2": 0.008, "v3": 0.02, "v4": 0.05}],
        value="(v1 < 0.03 ? 1 : 0) + (v2 < 0.03 ? 1 : 0) + (v3 < 0.03 ? 1 : 0) + (v4 < 0.03 ? 1 : 0)",
        tex="count", final=True,
        verify="(1 if nsimplify(v1) < Rational(3, 100) else 0) + (1 if nsimplify(v2) < Rational(3, 100) else 0)"
               " + (1 if nsimplify(v3) < Rational(3, 100) else 0) + (1 if nsimplify(v4) < Rational(3, 100) else 0)",
        explain="Each gap below the threshold is where a lambda state has to be inserted; the rest of the schedule is already dense enough")),
    ("MD-8.4.A", facts("mdh-schedule-order", FE, [
        ("When deleting an atom, which interaction is switched off first?", "The charges, while the Lennard-Jones is still on", "The Lennard-Jones, while the charges are still on", "Both together", "The bonded terms"),
        ("Turning off charges before Lennard-Jones avoids:", "A bare charge with no repulsive core, which collapses solvent onto it", "An endpoint catastrophe in the bonded terms", "A barostat failure", "A SHAKE failure"),
        ("The fewest-atoms rule says to:", "Transform the smallest set of atoms that connects the two end states", "Transform everything for symmetry", "Insert rather than delete", "Always use dual topology"),
        ("A transformation that both inserts and deletes atoms is handled by:", "Soft-core Lennard-Jones on both sets, with charges inside the LJ window", "Separate simulations with no soft core", "A smaller timestep", "A larger cutoff"),
    ], "Charges never without LJ, soft-core for LJ, and as few atoms as the end states allow")),
    ("MD-8.4.B", Q("mdh-softcore-finite", FE, "A soft-core potential replaces r by (alpha*sigma^6*(1-lam)^p + r^6)^(1/6). At r = 0 with alpha = {{al}}, sigma = {{sig}} angstrom, p = 1 and lam = {{lam}}, what effective separation (angstrom) does a vanishing atom see?",
        given={"al": {"pick": [0.5, 1.0]}, "sig": {"pick": [3.0, 3.4, 3.8]}, "lam": {"pick": [0.1, 0.5, 0.9]}},
        value="(al*sig^6*(1 - lam))^(1/6)", tex="r_{eff}",
        verify="(nsimplify(al)*nsimplify(sig)**6*(1 - nsimplify(lam)))**Rational(1, 6)",
        explain="The effective separation stays finite as lambda leaves 1, so the energy and its lambda derivative stay finite: that is exactly what removes the endpoint catastrophe")),
    ("MD-8.4.C", facts("mdh-topology-kinds", FE, [
        ("Single topology transforms a methyl to a chloro by:", "Changing the atom types and charges of shared atoms, with dummies for the mismatch", "Keeping both groups present and scaling them in and out", "Deleting the whole ligand", "Using separate simulations"),
        ("Dual topology keeps both end states present at once, which means:", "The two groups must not interact with each other", "The ligand has twice the mass", "No soft core is needed", "The charges cancel"),
        ("Decoupling a ligand switches off:", "Its interactions with the environment, leaving its internal terms on", "All of its interactions, internal ones included", "Only its charges", "Only its Lennard-Jones"),
        ("Annihilation differs from decoupling by also:", "Switching off the ligand's internal nonbonded interactions", "Keeping the environment on", "Using a larger box", "Requiring replica exchange"),
        ("Multisite lambda dynamics is closest to which topology?", "Multiple topology: several substituents present at one site, each scaled by its own lambda", "Single topology", "Dual topology with two states", "No topology"),
    ], "The distinction decides what the end states mean, and a standard-state correction is needed only for the one that removes the ligand from the box")),
    # ── unit 9 cycles ────────────────────────────────────────────────────
    ("MD-9.2.A", facts("mdh-double-decoupling-terms", FE, [
        ("In double decoupling with restraints, which term is often forgotten?", "The free energy of releasing the restraint, with its standard-state correction", "The solvation leg", "The complex leg", "The nuclear repulsion"),
        ("The restraint in the complex leg is there to:", "Keep the ligand in the site while its interactions vanish, so the end state is well defined", "Speed up the calculation", "Fix the protonation", "Set the density"),
        ("Why is a restraint needed at all when a ligand is decoupled in the site?", "A noninteracting ligand would wander out of the site and sample the whole box", "The barostat would fail", "SHAKE would fail", "The charges would not cancel"),
        ("The absolute binding free energy is referenced to:", "A standard state, usually 1 molar, which enters as a volume correction", "The box volume", "The simulation length", "The number of lambda windows"),
    ], "A double-decoupling cycle is only closed once the restraint-release and standard-state terms are in it")),
    ("MD-9.2.C", facts("mdh-relative-or-absolute", FE, [
        ("Ranking twenty close analogues of one scaffold is best done:", "Relative, as a perturbation network among the analogues", "Absolute, one ligand at a time", "With a single long MD run", "By docking alone"),
        ("Comparing two chemically unrelated ligands calls for:", "Absolute calculations, since no sensible atom mapping exists", "Relative, with a dummy-heavy map", "A longer relative run", "A larger box"),
        ("A charge-changing modification within a series argues for:", "Extra care: a finite-size correction either way, and relative only if the correction is applied", "Nothing special", "Absolute always, with no correction", "Dropping the ligand"),
        ("Relative calculations are usually cheaper because:", "The shared scaffold's error cancels, so less of the molecule has to be transformed", "They use fewer lambda windows by definition", "They need no equilibration", "They avoid soft cores"),
    ], "Chemical similarity is what decides: a mapping that cancels most of the system is the whole advantage of a relative calculation")),
    ("MD-9.3.B", Q("mdh-protonation-count", PREP, "propka predicts pKa values {{p1}}, {{p2}}, {{p3}} and {{p4}} for four acidic residues. At an experimental pH of {{ph}}, how many are protonated?",
        cases=[{"p1": 3.48, "p2": 3.95, "p3": 2.72, "p4": 3.99, "ph": 3.0},
               {"p1": 3.48, "p2": 3.95, "p3": 2.72, "p4": 3.99, "ph": 5.4},
               {"p1": 4.6, "p2": 2.1, "p3": 5.8, "p4": 3.3, "ph": 3.0},
               {"p1": 4.6, "p2": 2.1, "p3": 5.8, "p4": 3.3, "ph": 5.4},
               {"p1": 6.2, "p2": 4.4, "p3": 3.1, "p4": 7.0, "ph": 7.0}],
        value="(p1 > ph ? 1 : 0) + (p2 > ph ? 1 : 0) + (p3 > ph ? 1 : 0) + (p4 > ph ? 1 : 0)",
        tex="count", final=True,
        verify="(1 if nsimplify(p1) > nsimplify(ph) else 0) + (1 if nsimplify(p2) > nsimplify(ph) else 0)"
               " + (1 if nsimplify(p3) > nsimplify(ph) else 0) + (1 if nsimplify(p4) > nsimplify(ph) else 0)",
        explain="Below its pKa a residue is protonated, above it deprotonated. The T4 lysozyme sites are run at the paper's two experimental pH values, and the states chosen here are what goes in the methods section")),
    # ── unit 10 lambda dynamics ──────────────────────────────────────────
    ("MD-10.1.A", facts("mdh-lambda-extended", LAM, [
        ("In lambda dynamics, lambda is:", "An extra dynamical variable with its own mass and momentum, propagated with the atoms", "A fixed parameter set once per window", "A Monte Carlo move", "A bias"),
        ("The advantage over fixed-lambda windows is that:", "One simulation samples the whole alchemical space, so several end states are compared at once", "No biases are needed", "It needs no equilibration", "It is exact"),
        ("A lambda particle given too small a mass will:", "Move so fast that the spatial coordinates cannot follow it adiabatically", "Freeze at an end state", "Break SHAKE", "Change the free energy"),
        ("Free energies come out of a lambda-dynamics run from:", "The relative populations of the end states", "The work done on lambda", "The trajectory length", "The bias values alone"),
    ], "Making lambda dynamical turns a set of separate windows into one trajectory whose populations carry the answer")),
    ("MD-10.1.B", facts("mdh-msld-scaling", LAM, [
        ("In the MSλD potential, which terms are scaled by a single substituent's lambda?", "That substituent's own bonded and nonbonded terms with the environment", "The whole system's energy", "The water-water interactions", "The nuclear repulsion"),
        ("Which terms carry a product of two lambdas?", "Interactions between substituents at two different sites", "Substituent-environment interactions", "Environment-environment interactions", "Bonded terms within the common core"),
        ("Substituents at the same site do not interact because:", "They occupy the same space, so their mutual interactions are excluded", "Their lambdas are equal", "They are far apart", "Their charges cancel"),
        ("The common core's self-interaction is:", "Unscaled, since it is present in every end state", "Scaled by the sum of lambdas", "Scaled by the product of lambdas", "Omitted"),
    ], "Which power of lambda multiplies a term follows from how many alchemical groups the term involves")),
    ("MD-10.3.A", facts("mdh-bias-roles", LAM, [
        ("Which ALF bias term is a fixed offset that equalises the end-state free energies?", "The fixed term, applied per substituent", "The quadratic term", "The endpoint term", "The intersite term"),
        ("What does the endpoint bias term do?", "Pushes population into the physical end states, where lambda is near 0 or 1", "Flattens the middle of the profile", "Couples two sites", "Sets the temperature"),
        ("Why is any bias needed at all?", "Barriers between substituents make transitions rare, so the run would not interconvert them", "To correct the force field", "To conserve energy", "To set the standard state"),
        ("The biases affect the final free energies how?", "Not at all: they are subtracted out, they only change how fast it converges", "They shift every answer", "They scale the answer by lambda", "They set the error bar"),
    ], "Each term flattens a different feature of the landscape; the answer is bias-independent, the convergence is not")),
    ("MD-10.3.B", Q("mdh-bias-count-scheme", LAM, "A block setup has {{nb}} blocks. How many more pairwise bias potentials must be allocated under the newer nine-per-pair scheme than under the older five-per-pair scheme?",
        given={"nb": {"pick": [4, 6, 12, 28]}},
        value="(9 - 5)*nb*(nb - 1)/2", tex="extra", final=True,
        verify="4*Rational(nb*(nb - 1), 2)",
        explain="Both schemes allocate a fixed number of potentials per ordered pair of blocks, so the count grows as nblocks squared; the newer scheme's extra terms are what let it handle around twenty substituents")),
    ("MD-10.4.B", facts("mdh-nan-result", LAM, [
        ("A Result.txt entry is nan. The reading:", "That substituent was never sampled, so no free energy could be estimated", "The simulation crashed", "The free energy is zero", "The estimator failed on good data"),
        ("The usual first response to a nan in the penultimate production run is:", "Repeat a production of that length, since it suggests the biases have not converged", "Extend straight to the final length", "Change the force field", "Reduce the number of substituents to one"),
        ("Very noisy but finite entries suggest:", "Marginal sampling of that substituent: more flattening or longer production", "A bug in the estimator", "A charge error", "A box that is too large"),
        ("Extending a long production from poor biases gives:", "Poor results: refine the biases on shorter runs first", "Good results, since length fixes everything", "The same result faster", "A smaller error bar only"),
    ], "A nan is a sampling report, not a crash: it says the bias schedule, not the run length, is what needs work")),
    # ── unit 11 ALF in practice ──────────────────────────────────────────
    ("MD-11.1.A", facts("mdh-alf-cycle", ALF, [
        ("What does one ALF cycle consist of?", "A short simulation, reweighting of recent cycles, profiles fitted, and the biases updated", "A full production run and a final analysis", "One lambda window", "One postprocessing pass only"),
        ("Why does a cycle reweight several recent runs rather than only the last?", "To use more data while still discarding biases that are now stale", "To save disk", "Because the last run is always wrong", "To avoid reweighting altogether"),
        ("If a cycle fails with an error, runflat:", "Retries that cycle until it succeeds", "Stops the whole schedule", "Skips to production", "Reports nan and continues"),
        ("Relaunching runflat after a crash:", "Checks how far it got and resumes at the first incomplete cycle", "Starts over from cycle 1", "Requires manual editing", "Is not supported"),
    ], "The cycle is short-run, reweight, fit, update; the fault tolerance is what makes a hundred-cycle schedule practical on a preemptable queue")),
    ("MD-11.1.B", facts("mdh-flat-converged", ALF, [
        ("A flattened 1-D profile along one substituent's lambda should look like:", "Roughly flat, with population reaching both end states", "A deep well at lambda = 0.5", "A single sharp peak", "A straight line with large slope"),
        ("A profile with a deep minimum in the middle means:", "The run is trapped between end states and the biases need more work", "Flattening has converged", "The substituent is unphysical", "The temperature is too low"),
        ("Biases that are still moving between cycles indicate:", "More flattening cycles are needed before production", "Production can start", "The loss function is wrong", "The engine is wrong"),
        ("Starting production from unconverged biases costs:", "A long run that samples some substituents badly, giving nan or noisy entries", "Nothing, since biases cancel", "Only disk space", "A systematic shift in every answer"),
    ], "Flattening is judged on the profiles and on whether the biases have stopped moving, not on cycle count alone")),
    ("MD-11.2.A", Q("mdh-flat-steps", ALF, "A flattening cycle is to run {{ps}} ps at a {{dt}} fs timestep, discarding the first quarter. How many sampling steps does that make?",
        given={"ps": {"pick": [100, 104, 200, 1000]}, "dt": {"pick": [2.0]}},
        value="0.75*ps*1000/dt", tex="steps", final=True,
        verify="Rational(3, 4)*nsimplify(ps)*1000/nsimplify(dt)",
        explain="Numerical experiments found discarding the first quarter optimal, so the sampling argument is three times the equilibration argument; the example run files use 13000 and 39000 steps for a cycle of about 104 ps and 125000 and 375000 for 1 ns")),
    ("MD-11.2.C", Q("mdh-nblocks-from-mutations", ALF, "A system mutates site 1 to {{m1}} alternatives and site 2 to {{m2}} alternatives, each site also keeping its native residue. What value of nblocks does alf_info.py compute?",
        given={"m1": {"pick": [3, 5, 11, 15]}, "m2": {"pick": [1, 2, 7, 11]}},
        value="(m1 + 1) + (m2 + 1)", tex="nblocks", final=True, verify="m1 + 1 + m2 + 1",
        explain="nsubs counts the native plus each mutation at a site, and nblocks is the sum over sites, which is what alf_info.py prints; the p38 example has nsubs 16 and 12 and so nblocks 28")),
    ("MD-11.2.D", facts("mdh-alf-options", ALF, [
        ("For a site-saturation system with about twenty substituents, the recommended bias scheme is:", "The newer nine-term scheme, which was designed for that many", "The older five-term scheme", "No bias", "Only the fixed term"),
        ("For a two-substituent perturbation, the recommended bias scheme is:", "The older five-term scheme, which is best for two", "The newer nine-term scheme", "No bias", "Intersite biases"),
        ("Current best practice for the loss function is:", "The nonlinear loss, not the older linearized one", "The older linearized loss", "No loss function", "Either, since they agree"),
        ("Current best practice for implicit constraints is:", "The piecewise constraint, which samples the exact endpoints", "The oldest exponential constraint", "No constraint", "A harmonic restraint on lambda"),
        ("Linearized ALF should not be used beyond about:", "Eight or nine substituents", "Two substituents", "Fifty substituents", "Any number: it always works"),
    ], "The defaults in the software are the oldest options; best practice has moved, and the right bias scheme depends on how many substituents the site has")),
    ("MD-11.2.E", Q("mdh-ddg-uncertainty", ALF, "Result.txt gives {{gf}} kcal/mol in the folded ensemble with uncertainty {{sf}}, and {{gu}} with uncertainty {{su}} in the unfolded ensemble. What is the uncertainty of the folding ΔΔG (kcal/mol)?",
        cases=[{"gf": 2.4, "sf": 0.18, "gu": 0.9, "su": 0.11},
               {"gf": -1.6, "sf": 0.25, "gu": 0.4, "su": 0.3},
               {"gf": 3.9, "sf": 0.4, "gu": 1.2, "su": 0.15},
               {"gf": 0.7, "sf": 0.09, "gu": -0.5, "su": 0.12}],
        value="sqrt(sf^2 + su^2)", tex="\\sigma_{\\Delta\\Delta G}",
        verify="sqrt(nsimplify(sf)**2 + nsimplify(su)**2)",
        explain="The folding ΔΔG subtracts the unfolded ensemble's value from the folded one, and the two legs are independent runs, so their uncertainties add in quadrature")),
    ("MD-11.3.A", facts("mdh-alchemical-definitions", ALF, [
        ("In alchemical_definitions.inp, the first substituent at a site is written as:", "0, standing for the native residue already in the non-alchemical structure file", "The native residue's one-letter code", "1", "Blank"),
        ("Subsequent substituents at a site are written as:", "One-letter amino acid codes", "Three-letter residue names", "Atom numbers", "The site resid"),
        ("Histidine substituents need special codes because:", "The three protonation states are separate substituents and need separate codes", "Histidine cannot be mutated", "Histidine has two sites", "Its charge changes"),
        ("The terminal variables in that file usually have no effect unless:", "The mutation site is near a chain terminus", "The protein is large", "The site has many substituents", "The box is small"),
        ("Mutating several sites in one simulation means:", "Listing a second site resid and its own substituent sequence", "Running separate simulations always", "Editing the parameter file", "Nothing: only one site is supported"),
    ], "The file is the mutation set in machine-readable form; the native residue is always substituent zero, which is why nsubs is one more than the number of mutations")),
    ("MD-11.3.B", facts("mdh-prep-assembly", ALF, [
        ("system.inp is adapted from the production script by:", "Stripping out the dynamics commands and adding the alchemical setup streams", "Adding more dynamics commands", "Removing the topology files", "Changing the force field"),
        ("Why must the array-dimension line be removed from system.inp?", "It only works in the first script CHARMM reads, and system.inp is streamed by another script", "It is obsolete", "It conflicts with BLaDE", "It sets the box size"),
        ("A soft link to the topology directory is created because:", "Everything must live under prep for ALF, but the stream file refers to the original names", "Links are faster", "CHARMM cannot read directories", "It saves disk space"),
        ("Of the three alchemical streams, which adds the extra atoms and their bonded terms?", "The patch stream", "The select stream", "The delete stream", "The block setup stream"),
        ("What does the delete stream remove?", "Angles and dihedrals the patching added by accident", "The native residue", "The water", "The biases"),
        ("Which stream applies the lambda scaling to the right atom selections?", "The block setup stream", "The patch stream", "The select stream", "The delete stream"),
    ], "The prep directory is a non-alchemical system plus four streams: patch, select, delete, then block setup")),
    # ── unit 12 analysis ─────────────────────────────────────────────────
    ("MD-12.2.B", Q("mdh-cluster-population", ANA, "Clustering {{nf}} frames at a {{cut}} angstrom RMSD cutoff puts {{n1}} frames in the largest cluster. What percentage of the trajectory does it hold?",
        given={"nf": {"pick": [2000, 5000, 10000]}, "cut": {"pick": [1.5, 2.0, 2.5]}, "n1": {"pick": [412, 1850, 6300]}},
        require=["n1 < nf"], value="100*n1/nf", tex="\\%", verify="100*Rational(n1, nf)",
        explain="A cutoff that puts nearly everything in one cluster is too loose and one that makes every frame its own cluster is too tight; the representative structure is the member nearest the cluster centre, not the lowest-energy frame")),
    ("MD-12.3.A", facts("mdh-traj-handling", ANA, [
        ("Why must the structure file be loaded before the trajectory?", "The trajectory holds only numbers; without the structure file nothing says which atom each is", "The viewer sorts files alphabetically", "The trajectory holds the topology", "It does not matter"),
        ("A molecule appears split across the box edge. The cause:", "Periodic wrapping: it must be unwrapped or re-centred before measuring", "A broken bond", "A bad timestep", "A failed barostat"),
        ("Measuring an RMSD without first superposing gives:", "A value dominated by overall translation and rotation", "The correct RMSD", "Zero", "The RMSF"),
        ("A distance measured across a periodic boundary without the minimum image convention is:", "Too large, because it uses the far copy", "Too small", "Correct", "Undefined"),
    ], "Most trajectory analysis mistakes are bookkeeping: what the numbers mean, and which periodic copy they refer to")),
    # ── unit 13 cluster, engines, scripting, reproducibility ─────────────
    ("MD-13.1.A", Q("mdh-slurm-time", WF, "A SLURM time limit is given as a single number, which slurm reads as minutes. How many minutes should be requested for a job expected to take {{hr}} hours, with a {{saf}}x safety factor?",
        given={"hr": {"pick": [2, 6, 24, 36]}, "saf": {"pick": [1.5, 2]}},
        value="hr*60*saf", tex="minutes", final=True, verify="nsimplify(hr)*60*nsimplify(saf)",
        explain="A bare number in the time option is minutes, so a full day is 1440; slurm uses the limit to schedule, and the lab is billed for the time actually used, not the limit")),
    ("MD-13.1.B", Q("mdh-gpu-cost", WF, "A campaign needs {{ns}} ns of simulation and the system runs at {{rate}} ns/day on one GPU. At the paid GPU rate of 0.32 dollars per GPU-hour, what does it cost (dollars)?",
        given={"ns": {"pick": [100, 500, 2000]}, "rate": {"pick": [15, 40, 80]}},
        value="ns/rate*24*0.32", tex="dollars", verify="Rational(ns, rate)*24*Rational(32, 100)",
        explain="GPU-hours are the simulation length divided by the throughput; the free GPU partition costs nothing but a job there is killed when a paid job needs the node, so the usual plan is free for production and paid for debugging")),
    ("MD-13.2.A", facts("mdh-engine-choice", WF, [
        ("Which engine runs lambda dynamics fastest inside CHARMM?", "BLaDE, on a GPU", "The standard Fortran engine on CPUs", "The CPU-GPU domain-decomposition engine", "OpenMM called from CHARMM"),
        ("Why can OpenMM not be used for the lambda-dynamics runs here, even though it is fast?", "It does not yet run lambda dynamics from within CHARMM", "It is slower than the standard engine", "It cannot read CHARMM files", "It has no GPU support"),
        ("The GPU domain-decomposition engine compares to BLaDE how?", "Several times slower for these systems", "Faster", "Identical", "It cannot use a GPU"),
        ("A quick energy evaluation of a small system is fine on:", "The standard engine, since the setup cost dominates anyway", "BLaDE only", "A GPU partition only", "OpenMM only"),
        ("CHARMM is preferred in this group over faster engines because:", "Multisite lambda dynamics was developed in it and its features are there", "It is the fastest", "It is the only one with a scripting language", "It is the newest"),
    ], "The engine choice is a speed decision except for lambda dynamics, where only some engines support it at all")),
    ("MD-13.2.B", facts("mdh-blade-commands", WF, [
        ("What distinguishes a constant-pressure BLaDE dynamics command from a constant-volume one?", "The pressure-coupling keywords: the Monte Carlo barostat and its interval, reference pressure and volume move", "The friction coefficient", "The timestep", "Nothing"),
        ("Before the dynamics command, the friction coefficient is set by:", "A scalar assignment over the selected atoms", "A keyword in the dynamics command", "The topology file", "The barostat"),
        ("The equilibration and production steps here differ in timestep by:", "A factor of two: 1 fs for equilibration, 2 fs for production", "Nothing", "A factor of ten", "A factor of four"),
        ("BLaDE is invoked for an energy or minimisation by:", "Adding its keyword to that command", "Recompiling CHARMM", "A separate executable", "An environment variable"),
    ], "The same keyword switches engine for energy, minimisation and dynamics; constant pressure only adds the barostat keywords")),
    ("MD-13.2.C", facts("mdh-openmm-equivalent", WF, [
        ("Reproducing a CHARMM run in OpenMM from the same files requires matching:", "The cutoff scheme, long-range method, constraints and thermostat parameters", "Only the force field files", "Only the timestep", "Only the temperature"),
        ("The commonest cause of a mismatch between two engines on the same system is:", "Different nonbonded cutoff and switching conventions", "Different random seeds", "Different integrators", "Different file formats"),
        ("An engine comparison should be checked on:", "The single-point energy of one configuration, before any dynamics", "The free energy only", "The wall-clock time", "The trajectory length"),
        ("Matching single-point energies between engines to within a small tolerance shows:", "The system was set up the same way in both, which is what a cross-check is for", "That both are correct physics", "That the sampling agrees", "That the free energies will agree"),
    ], "A cross-engine check is a setup check: agree on one configuration's energy first, and only then compare dynamics")),
    ("MD-13.3.A", facts("mdh-charmm-script-syntax", WF, [
        ("In a CHARMM script, how is a title ended?", "A line containing only an asterisk", "A blank line", "An exclamation point", "The stop command"),
        ("Which character begins a comment?", "An exclamation point", "An asterisk", "A hash", "A double slash"),
        ("How is the value of a script variable used?", "With an at sign before its name", "With a question mark", "With a dollar sign", "With braces"),
        ("What does a doubled at sign do?", "Builds a variable name from another variable's value, giving array-like access", "Escapes the at sign", "Prints the variable", "Doubles the value"),
        ("How is a value that CHARMM itself computed, such as the atom count, referenced?", "With a question mark before its name", "With an at sign", "With a doubled at sign", "With a colon"),
        ("How are loops written in the CHARMM scripting language?", "With a label, a counter, and an if test that jumps back to the label", "With a for keyword", "With a while keyword", "Loops are not possible"),
        ("Why must a file path with capital letters be quoted?", "CHARMM is case-insensitive but linux is not, so quoting preserves the case", "Quotes are always required", "To allow spaces", "To make it a stream file"),
    ], "The language is small: titles, set and calc, at and doubled-at for variables, question mark for CHARMM's own values, stream, and if with goto for control flow")),
    ("MD-13.4.A", facts("mdh-reproducibility-record", WF, [
        ("Which of these is most often left out of a methods section and most often needed to reproduce a run?", "The protonation states assigned to every titratable residue", "The temperature", "The force field name", "The simulation length"),
        ("Recording the engine version matters because:", "Defaults and algorithms change between versions, so the same input can give different runs", "Versions are needed for citation only", "It identifies the author", "It sets the seed"),
        ("For an alchemical run, the record must also include:", "The bias scheme, loss function and implicit constraint used, since the defaults are not best practice", "Only the lambda count", "Only the estimator", "Nothing extra"),
        ("The box and ion composition belong in the record because:", "They set the salt concentration and net charge the result depends on", "They are needed for the figures", "They set the timestep", "They are not needed"),
    ], "A run is reproducible when someone else could rebuild the same system: the model, the states you chose, and the options that are not defaults")),
    ("MD-13.4.B", Q("mdh-traj-storage", WF, "A system has {{na}} atoms. Single-precision coordinates are written every {{iv}} steps of a {{ns}} ns run at a 2 fs timestep. How many gigabytes of trajectory is that, counting 12 bytes per atom per frame and 1 GB as 10^9 bytes?",
        given={"na": {"pick": [25000, 48000, 95000]}, "iv": {"pick": [5000, 50000]}, "ns": {"pick": [20, 100, 500]}},
        value="na*12*(ns*1e6/2/iv)/1e9", tex="GB",
        verify="nsimplify(na)*12*(nsimplify(ns)*10**6/2/nsimplify(iv))/10**9",
        explain="A nanosecond is 500000 steps at 2 fs, so the frame count is the step count over the save interval; raising the save interval is the lever that keeps a long production from filling the group's quota")),
    ("MD-13.4.C", facts("mdh-alf-cleanup", WF, [
        ("After a finished ALF project, which is safe to delete?", "The per-cycle run directories and the intermediate analysis data", "The alchemical trajectories of published work", "The prep directory", "Result.txt"),
        ("Which should essentially never be deleted for published work?", "The alchemical trajectories, which are the data behind the numbers", "The slurm log files", "The per-cycle output files", "The intermediate energy files"),
        ("The spatial trajectories of a published project:", "Can be deleted if space is desperate, after publication", "Must be kept forever", "Are never written", "Are the smallest files"),
        ("The cheapest way to generate less trajectory data in the first place is:", "Raise the save interval on the production command", "Shorten the run", "Use fewer substituents", "Delete afterwards"),
    ], "The intermediates exist for debugging; what carries the result is the prep directory, the alchemical trajectories and the analysis output")),
    # ── unit 14 advanced ─────────────────────────────────────────────────
    ("MD-14.1.A", facts("mdh-intersite-coupling", ADV, [
        ("Intersite coupling biases are needed when:", "Substituents at different sites interact, so one site's landscape depends on the other's state", "There is only one site", "The substituents are identical", "The box is small"),
        ("Without intersite flattening, a multi-site run tends to:", "Sample some combinations of substituents and never others", "Crash", "Give a systematic shift in every answer", "Run slower"),
        ("The intersite setting is given:", "Per site pair, as part of the flattening and postprocessing calls", "Once for the whole system", "In the topology file", "By the engine"),
        ("Two sites far apart in the structure:", "Usually need no intersite biases, since they barely interact", "Always need intersite biases", "Cannot be run together", "Need replica exchange"),
    ], "Coupling is a property of the structure: sites that touch need their joint landscape flattened, sites that do not can be treated independently")),
    ("MD-14.1.B", facts("mdh-potts-estimator", ADV, [
        ("The Potts-model estimator is preferred to counting end-state populations when:", "The combinatorial space is too large for every combination to be visited", "There are two substituents", "The run is short", "The biases are converged"),
        ("The histogram estimator fails in a large space because:", "Most combinations have zero counts, so their free energies are undefined", "It is biased", "It is slow", "It needs the biases"),
        ("The Potts model assumes the free energy is:", "A sum of per-site terms plus pairwise couplings", "Exactly additive with no couplings", "A single global constant", "Independent of the sites"),
        ("Pseudolikelihood is used instead of full likelihood because:", "The full likelihood's normalisation is intractable for many sites", "It is more accurate", "It needs fewer samples", "It avoids the couplings"),
    ], "A model estimator buys coverage of unvisited combinations at the price of its own assumption, so the assumption has to be checked")),
    ("MD-14.1.C", Q("mdh-partition-sites", ADV, "A design needs {{tot}} substituents at one site, and a single simulation is held to at most {{cap}} substituents there. How many simulations does the site need, if one substituent must be the shared native in every one?",
        given={"tot": {"pick": [12, 20, 25, 40]}, "cap": {"pick": [8, 12, 20]}},
        require=["tot > cap"], value="ceil((tot - 1)/(cap - 1))", tex="runs", final=True,
        verify="ceiling(Rational(tot - 1, cap - 1))",
        explain="The native has to appear in every batch so the batches can be referenced to each other, so each batch adds only cap minus one new substituents; the per-site cap depends on the bias scheme and implicit constraint chosen")),
    ("MD-14.2.A", facts("mdh-charge-change", ADV, [
        ("A charge-changing perturbation in a periodic box suffers from:", "A finite-size error, because the neutralising background interacts with the solute", "No special error", "A barostat failure", "A SHAKE failure"),
        ("The software's correction for this is applied by:", "Declaring each substituent's charge so the discrete solvent correction can be computed", "Adding a counterion by hand", "Enlarging the box only", "Nothing: it cancels"),
        ("The finite-size error shrinks with box size as:", "Roughly the inverse of the box length, which is why it is slow to converge away", "Exponentially", "Not at all", "The inverse square of the atom count"),
        ("A relative calculation between two ligands of equal net charge:", "Avoids the correction entirely, which is a reason to pair perturbations that way", "Still needs it", "Needs a larger correction", "Cannot be run"),
    ], "The correction is cheap and the box-size route is not, so declare the charges; better still, design the network so net charge does not change")),
    ("MD-14.2.B", facts("mdh-when-rex", ADV, [
        ("Which sites in the T4 lysozyme exercise needed replica exchange for converged free energies?", "A42, A98 and M102", "L99, M106, V149 and F153", "All seven", "None"),
        ("Biasing-potential replica exchange helps by:", "Letting a replica stuck behind a spatial barrier swap into a differently biased landscape", "Running longer", "Removing the biases", "Adding substituents"),
        ("A site needs replica exchange when the slow coordinate is:", "Spatial — the surrounding structure has to rearrange — rather than alchemical", "Always alchemical", "The timestep", "The box volume"),
        ("A symptom that flattening alone will not fix the sampling is:", "Biases that converge but end-state populations that still depend on the starting structure", "A nan in the first cycle", "A slow queue", "A large box"),
    ], "Flattening handles alchemical barriers; a spatial barrier needs exchange, which is why four of the seven T4 lysozyme sites were enough for the exercise and three were not")),
    ("MD-14.2.C", facts("mdh-pro-gly", ADV, [
        ("Why do proline mutations need a dedicated alchemical strategy?", "Proline's ring closes the backbone, so the mutation changes backbone connectivity, not just a side chain", "Proline is charged", "Proline is too large", "Proline has no side chain"),
        ("Why is glycine a special case?", "It removes the side chain entirely, including atoms the common core would otherwise share", "It is the smallest residue", "It is achiral", "It cannot be mutated"),
        ("A standard side-chain-only perturbation scheme assumes:", "A shared backbone that every substituent keeps unchanged", "A shared side chain", "Equal net charge", "A single site"),
        ("The T4 lysozyme exercise is described as side-chain only, which means:", "Proline and glycine substituents are outside its scope", "No backbone atoms exist", "Only one site is mutated", "The protein is rigid"),
    ], "The common core is the backbone; proline and glycine break that assumption in opposite directions, so each needs its own treatment")),
]

# MD-15.1.A: Electronic Structure now owns basis-set counting, so its second type is that framework's template.
# MD-15.1.A takes qc-shell-functions as its second drill, written straight into the framework line
# (the pattern pc.py used), since a template may not be listed in two spec files.
