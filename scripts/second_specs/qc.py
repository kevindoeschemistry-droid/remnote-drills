"""Electronic Structure framework (QC, Nov 2026): structure in UNITS (written to
drills/frameworks/electronic-structure.yaml by scripts/qc_framework.py) and two question types per objective in ADD.

The gap this fills: Hartree-Fock, basis sets and DFT existed only as a handful of items inside Molecular Simulation
(MD unit 15), which is wrong for a computational-chemistry MS. This framework is the method side; MD keeps the
classical-dynamics and free-energy side, and the two are linked by `requires`.

Sources read for this (Nov 2026):
  psi4numpy-tutorials  The Psi4NumPy tutorial modules, whose numbering and titles were confirmed from the project
                       README, a port's progress list and a documentation wiki: 01 basics, 03 Hartree-Fock (a-d),
                       04 density functional theory (a-e), 05 Moller-Plesset (a-b), 06 molecular properties,
                       07 SAPT, 08 CEPA0 and CCD, 11 integrals. The notebooks themselves were not run, so the
                       objectives under each module are ours.
  molssi-qm-tools      MolSSI's "Quantum Mechanics Tools" lesson: all seven episodes read from the lesson page
                       (geometry optimisation, intramolecular and intermolecular potential energy surfaces, basis-set
                       convergence of geometry and frequencies, standard redox potentials, and two version-control
                       episodes, which are out of scope here).
  szabo-ostlund        Szabo & Ostlund, Modern Quantum Chemistry: chapter structure from memory, so it is a textbook
                       crosswalk and not a curriculum.

Scaling exponents are the standard formal ones and are asked as scaling ratios, which is how the repo checks every
other scaling item: the answer is a ratio of the same law before and after, never recalled from a table."""
from opl_dsl import Q

FILE, FRAMEWORK = "qc-electronic", "electronic-structure"
PRACTICE = "P1"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
OB, HF, BS, CR, DF, PR = ("qchem.orbitals", "qchem.hartree-fock", "qchem.basis", "qchem.correlation",
                          "qchem.dft", "qchem.properties")
PN = lambda *s: [f"psi4numpy-tutorials:{x}" for x in s]
QT = lambda *s: [f"molssi-qm-tools:{x}" for x in s]

IDEAS = [("APPROX", "Every method is an approximation with a name",
          "A calculation is a Hamiltonian, a wavefunction model and a basis. Quoting a result without all three says nothing."),
         ("SCALE", "Cost decides what is possible",
          "Formal cost grows as a power of system size, and the exponent is the first thing that rules a method in or out."),
         ("CONVERGE", "Two limits, not one",
          "A result converges in the basis and in the treatment of correlation. Improving one while the other lags is wasted effort.")]

# unit n: (id, title, std, ideas, {topic n: (title, [(letter, std, do, ek, practice)])})
UNITS = {
 1: ("orbitals", "Orbitals, determinants and notation", PN("01"), ["APPROX"], {
   1: ("Counting the problem", [
     ("A", PN("01"), "Count electrons, occupied and virtual orbitals, and determinants for a closed-shell molecule in a given basis.",
      "A closed-shell molecule with N electrons fills N/2 spatial orbitals; a basis of K functions gives K spatial orbitals, so K - N/2 are virtual. Excitation counts come from choosing occupied and virtual pairs.", "P1"),
     ("B", PN("01"), "Read a method and basis label and say what each part fixes.",
      "A label such as CCSD(T)/cc-pVTZ names the correlation treatment and the basis separately; neither alone defines the calculation, and the geometry it was run at is a third choice.", "P2")]),
   2: ("Spin and reference", [
     ("A", PN("03"), "Distinguish restricted, unrestricted and restricted open-shell references and say when each is used.",
      "RHF pairs spatial orbitals for closed shells; UHF lets alpha and beta differ, which allows spin contamination; ROHF keeps a pure spin state at the cost of flexibility.", "P2"),
     ("B", PN("03"), "Compute the expected value of S squared for a given multiplicity and judge spin contamination from a reported value.",
      "For a pure state, S squared equals S(S+1) with S = (multiplicity - 1)/2: 0 for a singlet, 0.75 for a doublet, 2 for a triplet. A UHF value well above that is contaminated.", "P1")]),
 }),
 2: ("hartree-fock", "The Hartree-Fock method", PN("03", "11"), ["APPROX", "CONVERGE"], {
   1: ("The SCF procedure", [
     ("A", PN("03"), "Put the steps of an SCF cycle in order and say what makes it self-consistent.",
      "Build the core Hamiltonian and overlap, guess a density, build the Fock matrix from it, solve the generalised eigenvalue problem, form a new density, repeat until the density and energy stop changing.", "P2"),
     ("B", PN("03"), "Compute the Hartree-Fock energy from its one- and two-electron pieces and the nuclear repulsion.",
      "The electronic energy is a trace over the density with the core and Fock matrices; the total adds the nuclear repulsion, which is a pure geometry term.", "P1")]),
   2: ("What Hartree-Fock misses", [
     ("A", PN("03", "05"), "Define correlation energy and say which correlation Hartree-Fock already includes.",
      "Correlation energy is the exact non-relativistic energy minus the Hartree-Fock energy, always negative. Hartree-Fock includes exchange, and so same-spin (Fermi) correlation, but no opposite-spin (Coulomb) correlation.", "P2"),
     ("B", PN("03"), "Compute a correlation energy or a percentage recovered from reported total energies.",
      "E_corr = E_method - E_HF; the fraction recovered compares a method's correlation energy with a reference such as a complete-basis coupled-cluster value.", "P1")]),
   3: ("Convergence in practice", [
     ("A", PN("03"), "Diagnose an SCF that will not converge and name the usual remedies.",
      "Oscillation points at near-degenerate orbitals or a poor guess: DIIS acceleration, level shifting, damping, a better initial guess, or converging a simpler basis or method first.", "P2"),
     ("B", PN("11"), "Count the two-electron integrals a basis implies and say why screening and density fitting matter.",
      "There are about K^4/8 unique two-electron integrals for K basis functions once permutational symmetry is used; screening discards negligible ones and density fitting replaces the four-index set with a smaller three-index one.", "P1")]),
 }),
 3: ("basis", "Basis sets", QT("4"), ["CONVERGE", "SCALE"], {
   1: ("Reading a basis-set name", [
     ("A", QT("4"), "Read a basis-set name and say what it adds: split valence, polarisation, diffuse functions, and the correlation-consistent series.",
      "A split-valence set gives valence orbitals more than one function; polarisation functions add higher angular momentum for bonding flexibility; diffuse functions matter for anions and weak interactions; cc-pVXZ is a series designed to converge smoothly.", "P2"),
     ("B", QT("4"), "Count basis functions for a molecule in a stated basis.",
      "Count per atom and sum: a minimal basis gives one function per occupied atomic orbital, and each added shell contributes its own degeneracy (3 for p, 5 or 6 for d).", "P1")]),
   2: ("Converging and correcting", [
     ("A", QT("4"), "Judge from a series of results whether a property has converged in the basis.",
      "A property is converged when successive members of a systematic series change by less than the accuracy wanted; geometries converge faster than energies, and interaction energies slowest.", "P1"),
     ("B", QT("4"), "Compute a counterpoise-corrected interaction energy and explain basis-set superposition error.",
      "In a small basis each monomer borrows functions from its partner, over-binding the complex; the counterpoise correction recomputes each monomer in the full dimer basis and subtracts the difference.", "P1")]),
 }),
 4: ("correlation", "Correlation methods", PN("05", "08", "07"), ["APPROX", "SCALE"], {
   1: ("Perturbation theory", [
     ("A", PN("05"), "State what MP2 adds and when perturbation theory is the wrong tool.",
      "MP2 adds the leading double-excitation correction from the Hartree-Fock reference. It fails where the reference is poor: small gaps, bond breaking, diradicals, and transition metals.", "P2"),
     ("B", PN("05"), "Compute an MP2 correlation contribution from given orbital energies and integrals for one excitation.",
      "Each doubly-excited amplitude contributes a term whose numerator is the integral squared and whose denominator is the sum of occupied minus virtual orbital energies, so small gaps make large contributions.", "P1")]),
   2: ("Coupled cluster and configuration interaction", [
     ("A", PN("08"), "Order the common correlation methods by cost and accuracy, and say what CCSD(T) means.",
      "MP2, then CCSD, then CCSD(T), which adds a perturbative triples correction and is the usual accuracy reference for single-reference molecules.", "P2"),
     ("B", PN("08"), "Compute how much longer a calculation takes when the system grows, from a method's formal scaling.",
      "Formal cost scales as a power of basis size: about the fourth power for Hartree-Fock, the fifth for MP2, the sixth for CCSD and the seventh for CCSD(T). The ratio of two sizes raised to that power is the slowdown.", "P1")]),
   3: ("Interactions", [
     ("A", PN("07"), "Say what a symmetry-adapted perturbation theory decomposition gives that a total interaction energy does not.",
      "It splits the interaction into electrostatics, exchange, induction and dispersion, so two complexes with the same binding energy can be told apart by what binds them.", "P2"),
     ("B", PN("07"), "Attribute a described interaction to the dominant SAPT component.",
      "A hydrogen bond is electrostatics-dominated; two nonpolar rings stacking is dispersion-dominated; a polar molecule beside a polarisable one gains induction.", "P2")]),
 }),
 5: ("dft", "Density functional theory", PN("04"), ["APPROX", "SCALE"], {
   1: ("What a functional is", [
     ("A", PN("04"), "Place a functional on the rungs from local density through generalised gradient to hybrid and double hybrid, and say what each rung adds.",
      "LDA uses the density; GGA adds its gradient; meta-GGA adds the kinetic-energy density; a hybrid mixes in exact exchange; a double hybrid adds perturbative correlation.", "P2"),
     ("B", PN("04"), "Compute the exchange mixture a hybrid applies from its stated fraction of exact exchange.",
      "A hybrid replaces a stated fraction of the functional's exchange with Hartree-Fock exchange; range-separated hybrids make that fraction depend on distance.", "P1")]),
   2: ("Practice and pitfalls", [
     ("A", PN("04"), "Name what DFT handles poorly and the correction usually applied.",
      "Plain functionals miss long-range dispersion, so an empirical correction is added; self-interaction error distorts charge-transfer states and barriers, which range-separated hybrids reduce.", "P2"),
     ("B", PN("04"), "Compute an integration-grid or a dispersion-corrected energy from stated components.",
      "The total is the functional's energy plus the dispersion correction, which is a sum of damped pairwise terms; a grid too coarse adds noise that looks like a real energy difference.", "P1")]),
 }),
 6: ("properties", "Geometry, frequencies and properties", QT("1", "2", "3", "5") + PN("06"), ["CONVERGE"], {
   1: ("Geometry optimisation", [
     ("A", QT("1"), "State what an optimiser converges on and how a minimum is told from a saddle point.",
      "The gradient goes to zero at any stationary point; the Hessian's eigenvalues decide which it is, and a frequency calculation reports one imaginary frequency for a transition state.", "P2"),
     ("B", QT("2", "3"), "Read a potential energy surface scan for a bond length, angle or intermolecular distance and extract the minimum and the well depth.",
      "Scanning one coordinate while relaxing or fixing the rest gives a curve whose minimum is the equilibrium value and whose depth below the separated limit is the binding energy.", "P1")]),
   2: ("Frequencies and thermochemistry", [
     ("A", PN("06"), "Compute a zero-point vibrational energy from a set of harmonic frequencies.",
      "ZPE is half the sum of h times each harmonic frequency; a nonlinear molecule of n atoms has 3n - 6 modes and a linear one 3n - 5.", "P1"),
     ("B", QT("5") + PN("06"), "Compute a reaction energy or a standard potential from computed energies and say what corrections it needs.",
      "A reaction energy is the sum of products minus reactants, corrected for zero-point energy and thermal terms; an electrode potential divides the free-energy change by minus the electrons times the Faraday constant and needs a reference.", "P1")]),
   3: ("Choosing and reporting", [
     ("A", PN("04", "08") + QT("4"), "Choose a method and basis for a stated problem and defend both choices.",
      "Match the treatment to the chemistry and the basis to the property: geometries tolerate small bases, interaction energies do not; a multireference problem rules out single-reference methods whatever the basis.", "P2"),
     ("B", PN("01"), "State what a reported result must include to be reproducible.",
      "Method, basis, geometry (or that it was optimised at the same level), any dispersion correction and solvation model, the program and its version, and for a transition state the imaginary frequency.", "P2")]),
 }),
}


def facts(name, skill, rows, explain, pace="recall"):
    return Q(name, skill, "{{q}}", pace=pace, cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


ADD = [
    ("QC-1.1.A", Q("qc-orbital-count", OB, "A closed-shell molecule has {{ne}} electrons and is run in a basis of {{kk}} functions. How many virtual spatial orbitals are there?",
        given={"ne": {"pick": [10, 14, 20, 42]}, "kk": {"pick": [25, 48, 115]}}, value="kk - ne/2", tex="virtuals", final=True,
        verify="kk - Rational(ne, 2)", explain="N/2 spatial orbitals are occupied in a closed shell, so the rest of the K are virtual: the occupied-virtual product is what every correlation method sums over")),
    ("QC-1.1.A", Q("qc-double-excitations", OB, "With {{no}} occupied and {{nv}} virtual spatial orbitals, how many distinct pairs of (occupied, virtual) single excitations are there?",
        given={"no": {"pick": [5, 7, 10]}, "nv": {"pick": [20, 41, 105]}}, value="no*nv", tex="excitations", final=True,
        verify="no*nv", explain="The single-excitation space is the product; the double space goes as its square, which is where the cost of correlation methods comes from")),
    ("QC-1.1.B", facts("qc-label-parts", OB, [
        ("In CCSD(T)/cc-pVTZ, the part before the slash fixes:", "The correlation treatment", "The basis set", "The geometry", "The program"),
        ("In CCSD(T)/cc-pVTZ, the part after the slash fixes:", "The basis set", "The correlation treatment", "The solvent", "The temperature"),
        ("A result quoted as CCSD(T)/cc-pVTZ//B3LYP/6-31G* means:", "The energy is CCSD(T)/cc-pVTZ at a geometry optimised with B3LYP/6-31G*", "Two energies were averaged", "Two basis sets were combined", "The calculation failed and was retried"),
        ("A total energy quoted with no basis set is:", "Uninterpretable, because the basis changes the number", "Fine, since totals are absolute", "Fine if the method is given", "Only a problem for DFT"),
    ], "Method, basis and geometry are three separate choices, and all three belong in the report")),
    ("QC-1.1.B", facts("qc-label-read", OB, [
        ("B3LYP/6-31G(d) describes:", "A hybrid functional with a split-valence polarised basis", "A coupled-cluster method", "A perturbation treatment", "A semi-empirical method"),
        ("MP2/aug-cc-pVDZ differs from MP2/cc-pVDZ by:", "Added diffuse functions", "A different correlation treatment", "A different geometry", "Nothing"),
        ("HF/STO-3G is a:", "Minimal-basis Hartree-Fock calculation, the cheapest meaningful level", "Correlated calculation", "DFT calculation", "Complete-basis result"),
    ], "Each name decomposes into what it says about treatment and basis")),
    ("QC-1.2.A", facts("qc-reference-pick", HF, [
        ("A closed-shell organic molecule at its equilibrium geometry is best started from:", "A restricted (RHF) reference", "An unrestricted reference, necessarily", "A multireference wavefunction", "No reference"),
        ("A radical with one unpaired electron is usually treated with:", "An unrestricted or restricted open-shell reference", "A closed-shell restricted reference", "No reference", "A minimal basis only"),
        ("The cost of letting alpha and beta orbitals differ is:", "Spin contamination: the wavefunction is no longer a pure spin state", "Higher symmetry", "Fewer integrals", "Nothing"),
        ("ROHF keeps a pure spin state but:", "Is less flexible, so its energy is above the UHF energy", "Is always more accurate", "Is cheaper than RHF", "Cannot describe radicals"),
    ], "Pick the reference from the spin state, then watch for contamination if you used UHF")),
    ("QC-1.2.B", Q("qc-s-squared", HF, "What is the expected value of S squared for a pure state of multiplicity {{mult}}?",
        given={"mult": {"pick": [1, 2, 3, 4, 5]}}, value="((mult - 1)/2)*((mult - 1)/2 + 1)", tex="\\langle S^2\\rangle",
        verify="Rational(mult - 1, 2)*(Rational(mult - 1, 2) + 1)",
        explain="S = (multiplicity - 1)/2 and the expectation is S(S+1): 0, 0.75, 2, 3.75, 6. A UHF value well above this is contaminated")),
    ("QC-2.1.A", facts("qc-scf-order", HF, [
        ("Which comes first in an SCF cycle?", "Build the one-electron (core) Hamiltonian and overlap matrices, which do not change", "Form the density from the orbitals", "Diagonalise the Fock matrix", "Check convergence"),
        ("The Fock matrix depends on the density, which depends on the orbitals, which come from the Fock matrix. This is why:", "The procedure must be iterated to self-consistency", "The method is exact", "No guess is needed", "The energy is variational only at the start"),
        ("SCF convergence is judged on:", "The change in the density and the energy between cycles", "The number of basis functions", "The nuclear repulsion", "The molecular symmetry"),
        ("The nuclear repulsion energy during an SCF at fixed geometry:", "Stays constant, because it depends only on the nuclei", "Changes each cycle", "Is zero", "Is iterated like the density"),
    ], "Fixed integrals, then guess, build, diagonalise, rebuild, until nothing moves")),
    ("QC-2.1.B", Q("qc-total-energy", HF, "An SCF gives an electronic energy of {{ee}} hartree and the nuclear repulsion is {{nr}} hartree. What is the total energy (hartree)?",
        given={"ee": {"pick": [-85.2156, -112.4408, -198.7731]}, "nr": {"pick": [9.1681, 23.5894, 70.1123]}},
        value="ee + nr", tex="E_h", verify="nsimplify(ee) + nsimplify(nr)",
        explain="The total is electronic plus nuclear repulsion; only the total is comparable between geometries")),
    ("QC-2.2.A", facts("qc-correlation-def", HF, [
        ("Correlation energy is defined as:", "The exact non-relativistic energy minus the Hartree-Fock energy, in the same basis", "The Hartree-Fock energy itself", "The nuclear repulsion", "The zero-point energy"),
        ("The sign of the correlation energy is:", "Negative: correlation always lowers the energy", "Positive", "Either", "Zero"),
        ("Hartree-Fock already includes which correlation?", "Same-spin (Fermi) correlation, through exchange antisymmetry", "Opposite-spin correlation", "All correlation", "None at all"),
        ("Two electrons of opposite spin in Hartree-Fock:", "See only each other's average field, so their instantaneous repulsion is missed", "Are fully correlated", "Cannot occupy the same orbital", "Do not interact"),
    ], "Exchange gives same-spin correlation for free; the missing piece is opposite-spin")),
    ("QC-2.2.B", Q("qc-corr-fraction", HF, "A method gives {{em}} hartree where Hartree-Fock gives {{eh}} and the reference correlated value is {{er}}. What percentage of the correlation energy is recovered?",
        cases=[{"em": -76.3105, "eh": -76.0266, "er": -76.3421}, {"em": -40.3892, "eh": -40.1985, "er": -40.4102},
               {"em": -154.7210, "eh": -154.0856, "er": -154.7905}, {"em": -109.2755, "eh": -108.9543, "er": -109.3380}],
        value="100*(em - eh)/(er - eh)", tex="\\%",
        verify="100*(nsimplify(em) - nsimplify(eh))/(nsimplify(er) - nsimplify(eh))",
        explain="The fraction recovered is the method's correlation energy over the reference's: MP2 typically recovers most of it, CCSD(T) nearly all")),
    ("QC-2.3.A", facts("qc-scf-fail", HF, [
        ("An SCF oscillates between two densities without converging. The first remedy:", "DIIS acceleration, or damping and level shifting if it persists", "A larger basis", "A different molecule", "More cycles at the same settings"),
        ("SCF convergence is hardest when:", "The HOMO-LUMO gap is small, so orbitals swap between cycles", "The molecule is closed-shell and rigid", "The basis is minimal", "The geometry is optimised"),
        ("A useful practical trick for a stubborn SCF is:", "Converge a smaller basis or simpler method first and use those orbitals as the guess", "Turn off the two-electron integrals", "Reduce the nuclear charges", "Skip convergence checking"),
        ("Level shifting works by:", "Raising the virtual orbital energies artificially to widen the gap during convergence", "Reducing the number of electrons", "Changing the geometry", "Adding diffuse functions"),
    ], "Near-degenerate orbitals are the usual cause; DIIS, damping, shifting and a better guess are the usual cures")),
    ("QC-2.3.B", Q("qc-integral-count", HF, "A basis has {{kk}} functions. Roughly how many unique two-electron integrals are there, using permutational symmetry (K^4/8)?",
        given={"kk": {"pick": [25, 48, 115, 200]}}, value="kk^4/8", tex="integrals", final=True, verify="Rational(kk**4, 8)",
        explain="The four-index set grows as the fourth power, which is why screening and density fitting exist")),
    ("QC-3.1.A", facts("qc-basis-name", BS, [
        ("The 'd' in 6-31G(d) adds:", "Polarisation functions on heavy atoms", "Diffuse functions", "More core functions", "A dispersion correction"),
        ("A '+' in 6-31+G(d) adds:", "Diffuse functions on heavy atoms", "Polarisation functions", "Core correlation", "Relativistic terms"),
        ("Diffuse functions matter most for:", "Anions, lone pairs and weak interactions", "Core ionisation", "Bond lengths of neutral hydrocarbons", "Nothing in practice"),
        ("The cc-pVXZ series was designed so that:", "Results converge smoothly toward the complete-basis limit as X increases", "Each member is cheaper than the last", "Polarisation is unnecessary", "No diffuse functions are ever needed"),
        ("A minimal basis such as STO-3G gives:", "One function per occupied atomic orbital, so no flexibility to polarise", "Two functions per valence orbital", "Polarisation functions", "The complete-basis limit"),
    ], "A basis-set name is a recipe: split valence, polarisation, diffuse, and which series it belongs to")),
    ("QC-3.1.B", Q("qc-basis-functions", BS, "In a minimal basis, hydrogen contributes 1 function and a first-row atom (Li to Ne) contributes 5 (1s, 2s, three 2p). How many basis functions does a molecule with {{nh}} hydrogens and {{nc}} first-row atoms have?",
        given={"nh": {"pick": [2, 4, 6, 12]}, "nc": {"pick": [1, 2, 6]}}, value="nh + 5*nc", tex="functions", final=True,
        verify="nh + 5*nc", explain="Counting functions is how a job's cost is estimated before it is submitted")),
    ("QC-3.2.A", Q("qc-basis-converge", BS, "A property is computed as {{v1}}, {{v2}} and {{v3}} in successive members of a basis series. Has it converged to within {{tolv}} (the change between the last two)?",
        cases=[{"v1": 1.102, "v2": 1.088, "v3": 1.085, "tolv": 0.005, "kd": 0}, {"v1": -4.8, "v2": -6.2, "v3": -7.1, "tolv": 0.5, "kd": 1},
               {"v1": 112.4, "v2": 110.9, "v3": 110.8, "tolv": 0.2, "kd": 0}, {"v1": 2.51, "v2": 2.33, "v3": 2.20, "tolv": 0.05, "kd": 1}],
        choice=["Converged within the tolerance", "Not converged: still drifting"], correct="kd", pace="quick",
        verify="0 if Abs(nsimplify(v3) - nsimplify(v2)) <= nsimplify(tolv) else 1",
        explain="Convergence is judged on the change between successive members, not on agreement with experiment")),
    ("QC-3.2.B", Q("qc-counterpoise", BS, "A dimer scores {{ed}} hartree; the monomers in their own bases give {{m1}} and {{m2}}, and in the full dimer basis {{g1}} and {{g2}}. What is the counterpoise-corrected interaction energy, in kcal/mol (1 hartree = 627.5094740631 kcal/mol)?",
        cases=[{"ed": -152.6080, "m1": -76.3010, "m2": -76.3010, "g1": -76.3025, "g2": -76.3024},
               {"ed": -80.7900, "m1": -40.3930, "m2": -40.3930, "g1": -40.3942, "g2": -40.3941}],
        value="(ed - g1 - g2)*627.5094740631", tex="kcal/mol",
        verify="(nsimplify(ed) - nsimplify(g1) - nsimplify(g2))*Rational('627.5094740631')",
        explain="The corrected interaction uses the monomers computed in the dimer basis, which removes the artificial stabilisation from borrowed functions")),
    ("QC-4.1.A", facts("qc-mp2-limits", CR, [
        ("MP2 adds:", "The leading double-excitation correction to the Hartree-Fock reference", "All correlation exactly", "An exchange correction", "A relativistic correction"),
        ("MP2 is least trustworthy when:", "The HOMO-LUMO gap is small, because the perturbation denominators become small", "The molecule is a closed-shell hydrocarbon", "The basis is large", "The geometry is optimised"),
        ("A stretched bond approaching dissociation is a problem for MP2 because:", "A single reference no longer describes the wavefunction well", "The basis is too large", "The integrals vanish", "Exchange disappears"),
        ("For a system where MP2 fails for reference reasons, a larger basis will:", "Not fix it: the problem is the reference, not the basis", "Fix it", "Make it worse only", "Have no effect at all"),
    ], "Perturbation theory assumes a good reference; where that fails, basis size cannot save it")),
    ("QC-4.1.B", Q("qc-mp2-term", CR, "For one double excitation the contribution is the integral squared over the orbital-energy denominator. With integral {{itg}} hartree and occupied energies {{ei}}, {{ej}} and virtual energies {{ea}}, {{eb}}, what is the denominator (hartree)?",
        cases=[{"itg": 0.04, "ei": -0.63, "ej": -0.51, "ea": 0.18, "eb": 0.25},
               {"itg": 0.07, "ei": -0.95, "ej": -0.72, "ea": 0.11, "eb": 0.33},
               {"itg": 0.02, "ei": -0.40, "ej": -0.38, "ea": 0.05, "eb": 0.09}],
        value="ei + ej - ea - eb", tex="E_h", verify="nsimplify(ei) + nsimplify(ej) - nsimplify(ea) - nsimplify(eb)",
        explain="The denominator is occupied minus virtual, so it is negative and small when the gap is small: that is exactly when MP2 blows up")),
    ("QC-4.2.A", facts("qc-cc-order", CR, [
        ("Which ordering by increasing cost is right?", "Hartree-Fock, MP2, CCSD, CCSD(T)", "CCSD(T), CCSD, MP2, Hartree-Fock", "MP2, Hartree-Fock, CCSD(T), CCSD", "They all cost the same"),
        ("The (T) in CCSD(T) is:", "A perturbative triples correction added after the CCSD equations are solved", "A full triples treatment", "A basis-set correction", "A relativistic term"),
        ("CCSD(T) is often called the gold standard because:", "For single-reference molecules in a good basis it reaches chemical accuracy", "It is the cheapest method", "It is exact", "It needs no basis set"),
        ("For a genuinely multireference problem, CCSD(T):", "Can fail, because it is still built on one reference", "Is still exact", "Becomes cheaper", "Needs no correction"),
    ], "Cost and accuracy rise together, and all of it rests on the reference being good")),
    ("QC-4.2.B", Q("qc-scaling-ratio", CR, "A calculation scales as the {{pw}} power of basis size. The basis grows from {{k1}} to {{k2}} functions. By what factor does the cost rise?",
        given={"pw": {"pick": [4, 5, 6, 7]}, "k1": {"pick": [50, 100]}, "k2": {"pick": [100, 200, 300]}},
        value="(k2/k1)^pw", tex="\\times", verify="Rational(k2, k1)**pw",
        explain="Doubling the basis costs 16 times more at N^4 and 128 times more at N^7: the exponent is what rules a method in or out")),
    ("QC-4.3.A", facts("qc-sapt-why", CR, [
        ("A SAPT decomposition gives, beyond the total interaction energy:", "How much comes from electrostatics, exchange, induction and dispersion", "A better total", "A cheaper calculation", "The geometry"),
        ("Two complexes bind with the same total energy but different SAPT profiles. This tells you:", "They are held together by different physics, which may respond differently to a change", "Nothing", "One calculation is wrong", "They are the same complex"),
        ("A decomposition is useful in design because:", "It says which interaction to strengthen rather than just that binding is weak", "It lowers the energy", "It avoids basis sets", "It replaces experiment"),
    ], "A total says whether it binds; a decomposition says why")),
    ("QC-4.3.B", facts("qc-sapt-attribute", CR, [
        ("A water dimer's interaction is dominated by:", "Electrostatics", "Dispersion", "Induction", "Exchange repulsion"),
        ("Two stacked benzene rings are held together mainly by:", "Dispersion", "Electrostatics", "Induction", "Covalent bonding"),
        ("A cation beside a large polarisable molecule gains a large:", "Induction term", "Dispersion term only", "Exchange term", "Nothing"),
        ("At very short range the term that rises steeply and opposes binding is:", "Exchange repulsion", "Dispersion", "Electrostatics", "Induction"),
    ], "Match the chemistry to the component: polar means electrostatics, nonpolar and large means dispersion")),
    ("QC-5.1.A", facts("qc-functional-rungs", DF, [
        ("A local density approximation functional uses:", "The density alone", "The density and its gradient", "Exact exchange", "Perturbative correlation"),
        ("A generalised gradient approximation adds:", "The density's gradient", "Exact exchange", "The kinetic-energy density", "Nothing"),
        ("A meta-GGA adds, beyond the gradient:", "The kinetic-energy density", "Exact exchange", "Perturbative correlation", "A dispersion term"),
        ("A hybrid functional mixes in:", "A fraction of exact (Hartree-Fock) exchange", "Perturbative correlation only", "Relativistic terms", "A larger basis"),
        ("A double hybrid adds, beyond exact exchange:", "Perturbative correlation", "The density gradient", "The kinetic-energy density", "An empirical dispersion term"),
    ], "Each rung adds one more ingredient, and cost rises with it")),
    ("QC-5.1.B", Q("qc-hybrid-mix", DF, "A hybrid uses {{frac}} per cent exact exchange. For an exchange energy of {{ex}} hartree from the functional and {{hfx}} hartree from Hartree-Fock exchange, what is the mixed exchange energy (hartree)?",
        given={"frac": {"pick": [20, 25, 50]}, "ex": {"pick": [-8.42, -12.95]}, "hfx": {"pick": [-8.10, -12.40]}},
        value="(1 - frac/100)*ex + frac/100*hfx", tex="E_h",
        verify="(1 - Rational(frac,100))*nsimplify(ex) + Rational(frac,100)*nsimplify(hfx)",
        explain="A hybrid is a weighted blend: B3LYP uses 20 per cent exact exchange, PBE0 25 per cent")),
    ("QC-5.2.A", facts("qc-dft-pitfalls", DF, [
        ("Plain (non-dispersion-corrected) functionals miss:", "Long-range dispersion, so stacked and van der Waals complexes are under-bound", "Exchange", "Electrostatics", "The nuclear repulsion"),
        ("Self-interaction error in DFT shows up most in:", "Charge-transfer states and reaction barriers", "Bond lengths of small molecules", "Nuclear repulsion", "Zero-point energies"),
        ("A range-separated hybrid helps because it:", "Makes the fraction of exact exchange depend on distance, improving long-range behaviour", "Removes the basis set", "Adds dispersion", "Lowers the cost"),
        ("The usual fix for missing dispersion is:", "An added empirical pairwise correction", "A larger basis", "Tighter SCF convergence", "A finer grid"),
        ("A DFT result that changes noticeably with the integration grid means:", "The grid was too coarse: refine it before trusting the difference", "The functional is wrong", "The basis is too large", "The geometry is a transition state"),
    ], "Dispersion, self-interaction and the grid are the three places DFT quietly misleads")),
    ("QC-5.2.B", Q("qc-dispersion-total", DF, "A functional gives {{efun}} hartree and the dispersion correction is {{edisp}} hartree. What is the corrected energy, and what is the correction in kcal/mol (1 hartree = 627.5094740631 kcal/mol)? Give the correction.",
        given={"efun": {"pick": [-232.1540, -461.8812]}, "edisp": {"pick": [-0.0121, -0.0305, -0.0068]}},
        value="edisp*627.5094740631", tex="kcal/mol", verify="nsimplify(edisp)*Rational('627.5094740631')",
        explain="Dispersion corrections are small in hartree and decisive in kcal/mol, which is why they change conclusions about stacking")),
    ("QC-6.1.A", facts("qc-stationary-points", PR, [
        ("An optimiser converges when:", "The gradient of the energy with respect to the coordinates is essentially zero", "The energy is negative", "The SCF converges", "The basis is complete"),
        ("A minimum and a transition state are told apart by:", "The Hessian: a transition state has exactly one negative eigenvalue", "The energy alone", "The basis set", "The gradient, which differs"),
        ("A frequency calculation on a true minimum gives:", "All real frequencies", "One imaginary frequency", "Several imaginary frequencies", "No frequencies"),
        ("A frequency calculation reporting one imaginary frequency means:", "A first-order saddle point, that is a transition state", "A minimum", "A failed SCF", "A basis-set error"),
        ("Frequencies must be computed at:", "The same level and basis the geometry was optimised with", "Any level", "A smaller basis always", "The complete-basis limit"),
    ], "The gradient finds a stationary point; only the Hessian says which kind it is")),
    ("QC-6.1.B", Q("qc-well-depth", PR, "A scan gives a minimum energy of {{emin}} hartree and a separated-fragment limit of {{esep}} hartree. What is the well depth in kcal/mol (1 hartree = 627.5094740631 kcal/mol)?",
        cases=[{"emin": -152.6080, "esep": -152.6020}, {"emin": -80.7900, "esep": -80.7846},
               {"emin": -234.1255, "esep": -234.1102}, {"emin": -110.4433, "esep": -110.4401}],
        value="(esep - emin)*627.5094740631", tex="kcal/mol",
        verify="(nsimplify(esep) - nsimplify(emin))*Rational('627.5094740631')",
        explain="The depth below the separated limit is the binding energy; a counterpoise correction belongs on it if the basis is small")),
    ("QC-6.2.A", Q("qc-zpe", PR, "A nonlinear molecule has harmonic frequencies summing to {{sumf}} cm-1. What is the zero-point energy in kcal/mol (1 cm-1 = 0.0028591214 kcal/mol)?",
        given={"sumf": {"pick": [4500, 8800, 13200]}}, value="0.5*sumf*0.0028591214", tex="kcal/mol",
        verify="Rational(1,2)*sumf*Rational('0.0028591214')",
        explain="ZPE is half the sum of the harmonic frequencies; it rarely cancels between reactants and products, so it belongs in any reaction energy")),
    ("QC-6.2.A", Q("qc-mode-count", PR, "How many vibrational modes does a nonlinear molecule of {{na}} atoms have?",
        given={"na": {"pick": [3, 5, 6, 12]}}, value="3*na - 6", tex="modes", final=True, verify="3*na - 6",
        explain="3n - 6 for nonlinear and 3n - 5 for linear: the count a frequency output should match, and a quick check that the job did what you meant")),
    ("QC-6.2.B", Q("qc-reaction-energy", PR, "A reaction A + B to C has energies {{ea}}, {{eb}} and {{ec}} hartree. What is the reaction energy in kcal/mol (1 hartree = 627.5094740631 kcal/mol)?",
        cases=[{"ea": -76.3010, "eb": -40.3930, "ec": -116.7120}, {"ea": -154.0856, "eb": -76.3010, "ec": -230.4010},
               {"ea": -110.4433, "eb": -40.3930, "ec": -150.8255}],
        value="(ec - ea - eb)*627.5094740631", tex="kcal/mol",
        verify="(nsimplify(ec) - nsimplify(ea) - nsimplify(eb))*Rational('627.5094740631')",
        explain="Products minus reactants, converted; zero-point and thermal corrections come next, and they rarely cancel")),
    ("QC-6.3.A", facts("qc-method-choice", PR, [
        ("A geometry optimisation of a medium closed-shell organic molecule, for a later single point, is well served by:", "A hybrid functional with a modest polarised basis", "CCSD(T) with a large basis", "Minimal-basis Hartree-Fock", "A multireference method"),
        ("An interaction energy between two stacked aromatic rings needs:", "A dispersion-corrected or correlated method with a diffuse, polarised basis", "Hartree-Fock in a minimal basis", "A functional with no dispersion correction", "Geometry optimisation only"),
        ("A bond being broken homolytically needs:", "A multireference treatment, because one determinant no longer suffices", "MP2 with a large basis", "A hybrid functional with a small basis", "Hartree-Fock"),
        ("A barrier height for a charge-transfer reaction is best not computed with:", "A plain GGA functional, because of self-interaction error", "A range-separated hybrid", "CCSD(T)", "A double hybrid"),
    ], "Match the treatment to the chemistry and the basis to the property")),
    ("QC-6.3.B", facts("qc-report-reproducible", PR, [
        ("A reported computed energy must state, at minimum:", "The method, the basis and the geometry it was computed at", "Only the method", "Only the basis", "Only the program"),
        ("A transition state should additionally be reported with:", "Its single imaginary frequency", "Its dipole moment", "Its charge only", "Nothing extra"),
        ("A DFT result should state:", "The functional, any dispersion correction and the grid if non-default", "Only that DFT was used", "Only the basis", "Only the total energy"),
        ("A solvated result should state:", "The solvation model and solvent, since the number is meaningless without them", "Only the solvent", "Nothing: solvation is standard", "Only the dielectric constant"),
    ], "A number nobody can regenerate is not a result: this is the same standard the design pipeline items apply")),
]

# Second types, so every objective has two (the design rule).
ADD += [
    ("QC-1.2.A", Q("qc-unpaired", HF, "A species of multiplicity {{mult}} has how many unpaired electrons?",
        given={"mult": {"pick": [1, 2, 3, 4, 5]}}, value="mult - 1", tex="unpaired", final=True, verify="mult - 1",
        explain="Multiplicity is 2S + 1, so unpaired electrons = multiplicity - 1: the number that decides whether a restricted reference is even possible")),
    ("QC-1.2.B", facts("qc-contamination-read", HF, [
        ("A UHF doublet reports S squared = 1.10 against an expected 0.75. The reading:", "Noticeable spin contamination: higher-spin states are mixing in", "A pure doublet", "An error in the basis", "A converged triplet"),
        ("Spin contamination matters because it:", "Makes the energy and properties belong to no single spin state", "Speeds the SCF", "Changes the nuclear repulsion", "Improves the geometry"),
        ("A contaminated UHF reference passed to MP2 usually gives:", "An unreliable correlation energy, since the reference itself is wrong", "An exact answer", "The same answer as ROHF", "No answer"),
    ], "Compare the reported value with S(S+1) and treat a large excess as a warning about the reference")),
    ("QC-2.1.A", facts("qc-scf-pieces", HF, [
        ("Which matrix does not change during an SCF at fixed geometry and basis?", "The overlap matrix", "The density matrix", "The Fock matrix", "The orbital coefficients"),
        ("The generalised eigenvalue problem is solved rather than a plain one because:", "The basis functions are not orthogonal, so the overlap matrix appears", "The Fock matrix is not symmetric", "The density is complex", "The energy is variational"),
        ("The Hartree-Fock energy is variational, which means:", "It is an upper bound to the exact energy in that basis", "It is exact", "It is a lower bound", "It is unbounded"),
        ("A converged SCF gives orbitals that:", "Reproduce the density that generated the Fock matrix they came from", "Diagonalise the overlap matrix", "Minimise the nuclear repulsion", "Are exact"),
    ], "Fixed integrals, a non-orthogonal basis, and a variational upper bound")),
    ("QC-2.1.B", Q("qc-electronic-from-total", HF, "A total energy of {{tot}} hartree includes a nuclear repulsion of {{nr}} hartree. What is the electronic energy (hartree)?",
        given={"tot": {"pick": [-76.0266, -40.1985, -154.0856]}, "nr": {"pick": [9.1681, 13.4394, 70.1123]}},
        value="tot - nr", tex="E_h", verify="nsimplify(tot) - nsimplify(nr)",
        explain="The reverse split, and the check that two programs reporting different totals are not just splitting them differently")),
    ("QC-2.2.A", facts("qc-correlation-kinds", HF, [
        ("Dynamic correlation is:", "The short-range avoidance of electrons that a single determinant misses", "The mixing of several important determinants", "An exchange effect", "A relativistic effect"),
        ("Static (non-dynamic) correlation appears when:", "Several determinants are needed to describe the state at all", "Electrons avoid each other at short range", "The basis is too small", "The grid is coarse"),
        ("A stretched single bond at dissociation has mainly:", "Static correlation, which single-reference methods handle badly", "Dynamic correlation only", "No correlation", "Exchange only"),
        ("MP2 and CCSD(T) are designed for:", "Dynamic correlation on top of a good single reference", "Static correlation", "Relativistic effects", "Basis-set incompleteness"),
    ], "Two kinds of correlation, and single-reference methods only handle one of them well")),
    ("QC-2.2.B", Q("qc-corr-energy", HF, "Hartree-Fock gives {{eh}} hartree and a correlated method gives {{em}}. What is the correlation energy in kcal/mol (1 hartree = 627.5094740631 kcal/mol)?",
        cases=[{"eh": -76.0266, "em": -76.3105}, {"eh": -40.1985, "em": -40.3892},
               {"eh": -154.0856, "em": -154.7210}, {"eh": -108.9543, "em": -109.2755}],
        value="(em - eh)*627.5094740631", tex="kcal/mol",
        verify="(nsimplify(em) - nsimplify(eh))*Rational('627.5094740631')",
        explain="Correlation energy is large in absolute terms, which is why it has to be treated consistently on both sides of a reaction")),
    ("QC-2.3.A", facts("qc-guess-matters", HF, [
        ("A poor initial guess mainly costs:", "Cycles, and in hard cases convergence to the wrong solution", "Accuracy at convergence, always", "Nuclear repulsion", "Basis functions"),
        ("Two different SCF solutions can exist for one system. This means:", "A converged SCF is not automatically the lowest one: a stability check may be needed", "The method is broken", "The basis is too small", "The energy is not variational"),
        ("Converging a difficult SCF is often easiest by:", "Starting from the orbitals of a converged nearby calculation", "Doubling the basis", "Removing symmetry", "Raising the temperature"),
    ], "The guess decides which solution you land on, not just how fast")),
    ("QC-2.3.B", Q("qc-integral-growth", HF, "By what factor does the two-electron integral count grow when the basis goes from {{k1}} to {{k2}} functions?",
        given={"k1": {"pick": [50, 100]}, "k2": {"pick": [100, 150, 200]}}, value="(k2/k1)^4", tex="\\times",
        verify="Rational(k2, k1)**4",
        explain="The fourth-power growth of the integral list is why density fitting and screening are standard, not optional")),
    ("QC-3.1.A", facts("qc-basis-pick", BS, [
        ("Computing the electron affinity of a halide, the basis must include:", "Diffuse functions, because the extra electron is loosely held", "Only core functions", "No polarisation", "A minimal basis"),
        ("Optimising the geometry of a neutral hydrocarbon tolerates:", "A modest polarised basis such as a split-valence set with d functions", "Only the complete-basis limit", "A minimal basis with no polarisation", "Diffuse functions on every atom"),
        ("Computing a dispersion-bound dimer's interaction energy needs:", "Polarisation and diffuse functions, and ideally a counterpoise correction", "A minimal basis", "No polarisation", "Only the monomer basis"),
        ("A property computed in a minimal basis should be treated as:", "Qualitative at best", "Converged", "Chemically accurate", "Basis-independent"),
    ], "Match the basis to the property: loose electrons need diffuse functions, weak binding needs both")),
    ("QC-3.1.B", Q("qc-shell-functions", BS, "A shell of angular momentum l has 2l+1 pure functions. How many functions does a basis with {{ns}} s, {{np}} p and {{nd}} d shells on one atom have?",
        given={"ns": {"pick": [3, 4, 5]}, "np": {"pick": [2, 3, 4]}, "nd": {"pick": [1, 2]}},
        value="ns + 3*np + 5*nd", tex="functions", final=True, verify="ns + 3*np + 5*nd",
        explain="Each p shell adds 3 and each d shell 5 (pure) functions: this is how a basis-set table becomes a function count")),
    ("QC-3.2.A", Q("qc-extrapolate-change", BS, "Successive basis members give {{v2}} and {{v3}} for a property. What is the change between them, as a percentage of the larger-basis value?",
        cases=[{"v2": -8.21, "v3": -8.65}, {"v2": 1.088, "v3": 1.085}, {"v2": -6.2, "v3": -7.1}, {"v2": 110.9, "v3": 110.8}],
        value="abs((v3 - v2)/v3)*100", tex="\\%",
        verify="Abs((nsimplify(v3) - nsimplify(v2))/nsimplify(v3))*100",
        explain="A change of a per cent or less between successive members is the usual sign of basis convergence for that property")),
    ("QC-3.2.B", facts("qc-bsse-why", BS, [
        ("Basis-set superposition error makes an interaction energy:", "Too negative, because each monomer borrows the other's functions", "Too positive", "Unchanged", "Zero"),
        ("BSSE shrinks as:", "The basis grows toward completeness", "The basis shrinks", "The temperature rises", "The geometry relaxes"),
        ("The counterpoise correction computes each monomer:", "In the full dimer basis, with the partner's functions present but no nuclei or electrons", "In its own basis only", "At the dimer geometry only", "With twice the electrons"),
        ("A large counterpoise correction tells you:", "The basis is too small for this interaction energy", "The interaction is strong", "The geometry is wrong", "The method is wrong"),
    ], "A small basis fakes stabilisation; counterpoise measures how much")),
    ("QC-4.1.A", facts("qc-mp2-scaling-use", CR, [
        ("MP2 is popular because it:", "Recovers most dynamic correlation at a cost one power above Hartree-Fock", "Is exact", "Needs no basis set", "Handles multireference cases"),
        ("Spin-component-scaled MP2 variants exist because:", "Scaling the same- and opposite-spin contributions differently corrects known MP2 biases", "MP2 is too cheap", "They remove the basis-set dependence", "They add exact exchange"),
        ("MP2 systematically overbinds dispersion complexes in large bases. The usual response:", "Use a scaled variant or a coupled-cluster reference", "Shrink the basis to compensate", "Ignore it", "Add diffuse functions only"),
    ], "A cheap, useful method with known, documented biases")),
    ("QC-4.1.B", Q("qc-mp2-contribution", CR, "For a double excitation the contribution is the integral squared over the denominator. With integral {{itg}} hartree and a denominator of {{den}} hartree, what is the contribution (hartree)?",
        given={"itg": {"pick": [0.02, 0.04, 0.07]}, "den": {"pick": [-0.71, -1.23, -0.35]}},
        value="itg^2/den", tex="E_h", verify="nsimplify(itg)**2/nsimplify(den)",
        explain="Negative and largest when the denominator is small: a small gap makes a single excitation dominate, which is the warning sign")),
    ("QC-4.2.A", facts("qc-method-ladder", CR, [
        ("Adding a perturbative triples correction to CCSD gives:", "CCSD(T)", "CCSD", "MP2", "CISD"),
        ("Truncated configuration interaction such as CISD is less used than CCSD because it:", "Is not size-extensive, so errors grow with system size", "Is more expensive than CCSD(T)", "Needs no reference", "Is exact"),
        ("Full configuration interaction in a given basis is:", "Exact in that basis, but affordable only for very small systems", "Cheap", "An approximation to Hartree-Fock", "Basis-independent"),
        ("Chemical accuracy is usually taken to mean about:", "1 kcal/mol", "10 kcal/mol", "0.001 kcal/mol", "100 kcal/mol"),
    ], "The ladder runs to exactness and the cost runs with it; size-extensivity is why coupled cluster won")),
    ("QC-4.2.B", Q("qc-basis-for-cost", CR, "A method scales as the {{pw}} power of basis size. If the cost budget allows a {{fac}}-fold increase, by what factor can the basis grow?",
        given={"pw": {"pick": [4, 5, 6, 7]}, "fac": {"pick": [16, 64, 128]}}, value="fac^(1/pw)", tex="\\times",
        verify="Rational(fac)**Rational(1, pw)",
        explain="Inverting the scaling: at N^7 a 128-fold budget buys barely twice the basis, which is why CCSD(T) lives in small bases")),
    ("QC-4.3.A", facts("qc-sapt-levels", CR, [
        ("SAPT0 differs from higher-order SAPT by:", "Truncating the perturbation series earlier, so it is cheaper and less accurate", "Using a different basis", "Including no dispersion", "Being exact"),
        ("A SAPT decomposition requires:", "Two identifiable monomers, so it does not apply to a single molecule's internal energy", "Only one molecule", "A transition state", "A periodic system"),
        ("The exchange terms in SAPT are:", "Repulsive, arising from antisymmetry between monomers", "Attractive", "Zero", "The same as dispersion"),
    ], "Pick the SAPT order for the accuracy you need, and remember it needs two monomers")),
    ("QC-4.3.B", Q("qc-sapt-total", CR, "A SAPT decomposition gives electrostatics {{el}}, exchange {{ex}}, induction {{ind}} and dispersion {{dsp}} kcal/mol. What is the total interaction energy?",
        cases=[{"el": -8.4, "ex": 7.1, "ind": -1.9, "dsp": -2.6}, {"el": -0.6, "ex": 2.4, "ind": -0.3, "dsp": -3.9},
               {"el": -12.2, "ex": 9.8, "ind": -3.4, "dsp": -1.8}, {"el": -2.0, "ex": 3.3, "ind": -0.7, "dsp": -3.1}],
        value="el + ex + ind + dsp", tex="kcal/mol",
        verify="nsimplify(el) + nsimplify(ex) + nsimplify(ind) + nsimplify(dsp)",
        explain="The components sum to the total; which one dominates is what the decomposition is for")),
    ("QC-5.1.A", facts("qc-functional-pick", DF, [
        ("A functional with no exact exchange will tend to:", "Underestimate reaction barriers", "Overestimate barriers", "Give exact barriers", "Not converge"),
        ("For a main-group thermochemistry screen, a reasonable default is:", "A well-tested hybrid with a dispersion correction", "LDA", "Hartree-Fock", "Full CI"),
        ("Double hybrids cost more than hybrids because they:", "Add a perturbative correlation term, which scales like MP2", "Use larger grids", "Need diffuse functions", "Add exact exchange twice"),
        ("A functional's performance is established by:", "Benchmarking against reference data for the property in question", "Its rung alone", "Its age", "Its cost"),
    ], "Rung guides the choice; benchmarks decide it")),
    ("QC-5.1.B", Q("qc-exchange-fraction", DF, "A hybrid's mixed exchange is {{mix}} hartree, built from {{ex}} hartree of functional exchange and {{hfx}} hartree of exact exchange. What fraction of exact exchange (per cent) does it use?",
        cases=[{"mix": -8.356, "ex": -8.42, "hfx": -8.10}, {"mix": -12.8125, "ex": -12.95, "hfx": -12.40},
               {"mix": -8.26, "ex": -8.42, "hfx": -8.10}],
        value="(mix - ex)/(hfx - ex)*100", tex="\\%",
        verify="(nsimplify(mix) - nsimplify(ex))/(nsimplify(hfx) - nsimplify(ex))*100",
        explain="Inverting the blend recovers the mixing fraction, which is the single number that most distinguishes one hybrid from another")),
    ("QC-5.2.A", Q("qc-dispersion-share", DF, "An interaction energy is {{tot}} kcal/mol, of which the dispersion correction supplies {{dsp}}. What percentage of the binding comes from the correction?",
        cases=[{"tot": -12.4, "dsp": -7.6}, {"tot": -3.1, "dsp": -2.8}, {"tot": -24.0, "dsp": -4.2}, {"tot": -8.8, "dsp": -5.9}],
        value="100*dsp/tot", tex="\\%", verify="100*nsimplify(dsp)/nsimplify(tot)",
        explain="When most of the binding comes from the empirical correction, the result rests on that correction's parameters rather than on the functional")),
    ("QC-5.2.B", facts("qc-grid-and-noise", DF, [
        ("A numerical integration grid is needed in DFT because:", "The exchange-correlation functional cannot be integrated analytically", "The basis is non-orthogonal", "The density is complex", "The nuclei move"),
        ("A grid that is too coarse shows up as:", "Energy differences and gradients that change when the grid is refined", "A failed SCF only", "A wrong nuclear repulsion", "A basis-set error"),
        ("Grid quality matters most for:", "Small energy differences, such as conformer gaps and weak interactions", "Total energies only", "Bond lengths only", "Nothing"),
        ("Before reporting a small DFT energy difference you should:", "Repeat it on a finer grid to confirm it is not numerical noise", "Report it as is", "Shrink the basis", "Loosen SCF convergence"),
    ], "Grid noise looks exactly like a real small energy difference, so check it")),
    ("QC-6.1.A", facts("qc-opt-practice", PR, [
        ("A geometry optimisation that converges to a structure with one imaginary frequency has found:", "A transition state, not a minimum", "A minimum", "A failed calculation", "A complete-basis result"),
        ("A frequency calculation at a geometry that was not fully optimised gives:", "Spurious small imaginary frequencies that are artefacts", "Exact frequencies", "No frequencies", "The correct ZPE"),
        ("To confirm a transition state connects the intended reactant and product you:", "Follow the imaginary mode downhill in both directions", "Check the energy only", "Compute the dipole", "Enlarge the basis"),
        ("Optimising in a small basis then computing the energy in a large one is:", "A standard and defensible compromise, as long as both levels are reported", "Never acceptable", "Equivalent to optimising in the large basis", "Cheaper but meaningless"),
    ], "The Hessian and the imaginary mode are what turn a stationary point into a claim")),
    ("QC-6.1.B", Q("qc-equilibrium-scan", PR, "A bond scan gives energies {{e1}}, {{e2}}, {{e3}}, {{e4}} hartree at {{r1}}, {{r2}}, {{r3}}, {{r4}} angstrom. At which distance is the minimum?",
        cases=[{"e1": -76.0201, "e2": -76.0266, "e3": -76.0240, "e4": -76.0180, "r1": 0.90, "r2": 0.96, "r3": 1.02, "r4": 1.10, "kd": 1},
               {"e1": -40.1902, "e2": -40.1960, "e3": -40.1985, "e4": -40.1950, "r1": 1.00, "r2": 1.06, "r3": 1.09, "r4": 1.15, "kd": 2},
               {"e1": -110.4433, "e2": -110.4401, "e3": -110.4350, "e4": -110.4300, "r1": 1.10, "r2": 1.16, "r3": 1.22, "r4": 1.28, "kd": 0}],
        choice=["{{r1}}", "{{r2}}", "{{r3}}", "{{r4}}"], correct="kd", pace="quick",
        verify="[nsimplify(e1), nsimplify(e2), nsimplify(e3), nsimplify(e4)].index(Min(nsimplify(e1), nsimplify(e2), nsimplify(e3), nsimplify(e4)))",
        explain="The lowest energy on the scan is the equilibrium value; a minimum at the edge of the scan means the range was too narrow")),
    ("QC-6.2.B", Q("qc-potential-from-dg", PR, "A reaction with {{nel}} electrons has a free-energy change of {{dg}} kJ/mol. What is the standard potential (V), using F = 96485.33212 C/mol?",
        given={"nel": {"pick": [1, 2, 4]}, "dg": {"pick": [-237.1, -474.2, -131.3]}},
        value="-dg*1000/(nel*96485.33212)", tex="V", verify="-nsimplify(dg)*1000/(nel*Rational('96485.33212'))",
        explain="E = -dG/(nF); a computed potential also needs a reference electrode to be comparable with experiment")),
    ("QC-6.3.A", Q("qc-cost-decision", PR, "A CCSD(T) job on a {{k1}}-function basis took {{hr}} hours. Scaling as the seventh power, how many hours would a {{k2}}-function basis take?",
        given={"k1": {"pick": [100, 120]}, "hr": {"pick": [2, 6, 12]}, "k2": {"pick": [150, 200, 240]}},
        value="hr*(k2/k1)^7", tex="hours", verify="hr*Rational(k2, k1)**7",
        explain="The arithmetic that decides a project: at N^7 a modest basis increase turns hours into weeks")),
    ("QC-6.3.B", facts("qc-report-missing", PR, [
        ("A paper reports 'DFT energies' with no functional named. The result is:", "Not reproducible: the functional is the method", "Fine, since DFT is standard", "Fine if the basis is given", "Only a problem for weak interactions"),
        ("A reported interaction energy with no mention of counterpoise or basis is:", "Hard to compare with anything, because BSSE could account for much of it", "Fully comparable", "Exact", "Unaffected by basis"),
        ("Two papers disagree on a barrier height by 5 kcal/mol. The first thing to compare:", "The functional, basis and geometry each used", "The authors", "The journals", "The year"),
        ("Reporting a geometry as 'optimised' without the level is a problem because:", "The energy was computed at a geometry nobody else can reproduce", "Geometries do not matter", "Only the basis matters", "It is never a problem"),
    ], "The same standard as the design pipeline: a number nobody can regenerate is not a result")),
]
