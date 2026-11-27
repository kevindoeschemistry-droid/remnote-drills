# Electronic Structure — curriculum framework (draft 1)

Generated from `drills/frameworks/electronic-structure.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**30 learning objectives** in 6 units (30 core): 30 drilled, 0 partly, 0 with no drills. Core: 30 / 30 drilled.

## Big ideas

- **APPROX · Every method is an approximation with a name.** A calculation is a Hamiltonian, a wavefunction model and a basis. Quoting a result without all three says nothing.
- **SCALE · Cost decides what is possible.** Formal cost grows as a power of system size, and the exponent is the first thing that rules a method in or out.
- **CONVERGE · Two limits, not one.** A result converges in the basis and in the treatment of correlation. Improving one while the other lags is wasted effort.

## Practices

- **P1 · Compute.** Carry the calculation to a number with units, and say what it does not settle.
- **P2 · Decide.** Choose a method, basis or protocol for a stated problem, and name the failure it avoids.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Orbitals, determinants and notation | core | — | 4 | 4 | 0 | 0 |
| 2 · The Hartree-Fock method | core | — | 6 | 6 | 0 | 0 |
| 3 · Basis sets | core | — | 4 | 4 | 0 | 0 |
| 4 · Correlation methods | core | — | 6 | 6 | 0 | 0 |
| 5 · Density functional theory | core | — | 4 | 4 | 0 | 0 |
| 6 · Geometry, frequencies and properties | core | — | 6 | 6 | 0 | 0 |

## Unit 1 · Orbitals, determinants and notation

Big ideas: APPROX

### 1.1 Counting the problem



- ● **QC-1.1.B** (psi4numpy-tutorials:01) Read a method and basis label and say what each part fixes.
  - EK: A label such as CCSD(T)/cc-pVTZ names the correlation treatment and the basis separately; neither alone defines the calculation, and the geometry it was run at is a third choice.
  - Needs: CH-1.9.A, CH-2.8.A
  - P2 · drills: qc-label-parts, qc-label-read
- ● **QC-1.1.A** (psi4numpy-tutorials:01) Count electrons, occupied and virtual orbitals, and determinants for a closed-shell molecule in a given basis.
  - EK: A closed-shell molecule with N electrons fills N/2 spatial orbitals; a basis of K functions gives K spatial orbitals, so K - N/2 are virtual. Excitation counts come from choosing occupied and virtual pairs.
  - Needs: QC-1.1.B
  - P1 · drills: qc-orbital-count, qc-double-excitations

### 1.2 Spin and reference



- ● **QC-1.2.A** (psi4numpy-tutorials:03, psi4numpy-tutorials:03c, psi4numpy-tutorials:03d) Distinguish restricted, unrestricted and restricted open-shell references and say when each is used.
  - EK: RHF pairs spatial orbitals for closed shells; UHF lets alpha and beta differ, which allows spin contamination; ROHF keeps a pure spin state at the cost of flexibility.
  - Needs: QC-1.1.A
  - P2 · drills: qc-reference-pick, qc-unpaired
- ● **QC-1.2.B** (psi4numpy-tutorials:03, psi4numpy-tutorials:03c) Compute the expected value of S squared for a given multiplicity and judge spin contamination from a reported value.
  - EK: For a pure state, S squared equals S(S+1) with S = (multiplicity - 1)/2: 0 for a singlet, 0.75 for a doublet, 2 for a triplet. A UHF value well above that is contaminated.
  - Needs: QC-1.2.A
  - P1 · drills: qc-s-squared, qc-contamination-read

## Unit 2 · The Hartree-Fock method

Big ideas: APPROX, CONVERGE

### 2.1 The SCF procedure



- ● **QC-2.1.A** (psi4numpy-tutorials:03, psi4numpy-tutorials:03a) Put the steps of an SCF cycle in order and say what makes it self-consistent.
  - EK: Build the core Hamiltonian and overlap, guess a density, build the Fock matrix from it, solve the generalised eigenvalue problem, form a new density, repeat until the density and energy stop changing.
  - Needs: QC-1.2.B
  - P2 · drills: qc-scf-order, qc-scf-pieces
- ● **QC-2.1.B** (psi4numpy-tutorials:03, psi4numpy-tutorials:03a) Compute the Hartree-Fock energy from its one- and two-electron pieces and the nuclear repulsion.
  - EK: The electronic energy is a trace over the density with the core and Fock matrices; the total adds the nuclear repulsion, which is a pure geometry term.
  - Needs: QC-2.1.A
  - P1 · drills: qc-total-energy, qc-electronic-from-total

### 2.2 What Hartree-Fock misses



- ● **QC-2.2.A** (psi4numpy-tutorials:03, psi4numpy-tutorials:05) Define correlation energy and say which correlation Hartree-Fock already includes.
  - EK: Correlation energy is the exact non-relativistic energy minus the Hartree-Fock energy, always negative. Hartree-Fock includes exchange, and so same-spin (Fermi) correlation, but no opposite-spin (Coulomb) correlation.
  - Needs: QC-2.1.B
  - P2 · drills: qc-correlation-def, qc-correlation-kinds
- ● **QC-2.2.B** (psi4numpy-tutorials:03) Compute a correlation energy or a percentage recovered from reported total energies.
  - EK: E_corr = E_method - E_HF; the fraction recovered compares a method's correlation energy with a reference such as a complete-basis coupled-cluster value.
  - Needs: QC-2.2.A
  - P1 · drills: qc-corr-fraction, qc-corr-energy

### 2.3 Convergence in practice



- ● **QC-2.3.A** (psi4numpy-tutorials:03, psi4numpy-tutorials:03b) Diagnose an SCF that will not converge and name the usual remedies.
  - EK: Oscillation points at near-degenerate orbitals or a poor guess: DIIS acceleration, level shifting, damping, a better initial guess, or converging a simpler basis or method first.
  - Needs: QC-2.2.B
  - P2 · drills: qc-scf-fail, qc-guess-matters
- ● **QC-2.3.B** (psi4numpy-tutorials:11, psi4numpy-tutorials:03b) Count the two-electron integrals a basis implies and say why screening and density fitting matter.
  - EK: There are about K^4/8 unique two-electron integrals for K basis functions once permutational symmetry is used; screening discards negligible ones and density fitting replaces the four-index set with a smaller three-index one.
  - Needs: QC-2.3.A
  - P1 · drills: qc-integral-count, qc-integral-growth

## Unit 3 · Basis sets

Big ideas: CONVERGE, SCALE

### 3.1 Reading a basis-set name



- ● **QC-3.1.A** (molssi-qm-tools:4) Read a basis-set name and say what it adds: split valence, polarisation, diffuse functions, and the correlation-consistent series.
  - EK: A split-valence set gives valence orbitals more than one function; polarisation functions add higher angular momentum for bonding flexibility; diffuse functions matter for anions and weak interactions; cc-pVXZ is a series designed to converge smoothly.
  - Needs: QC-2.3.B
  - P2 · drills: qc-basis-name, qc-basis-pick
- ● **QC-3.1.B** (molssi-qm-tools:4) Count basis functions for a molecule in a stated basis.
  - EK: Count per atom and sum: a minimal basis gives one function per occupied atomic orbital, and each added shell contributes its own degeneracy (3 for p, 5 or 6 for d).
  - Needs: QC-3.1.A
  - P1 · drills: qc-basis-functions, qc-shell-functions

### 3.2 Converging and correcting



- ● **QC-3.2.A** (molssi-qm-tools:4) Judge from a series of results whether a property has converged in the basis.
  - EK: A property is converged when successive members of a systematic series change by less than the accuracy wanted; geometries converge faster than energies, and interaction energies slowest.
  - Needs: QC-3.1.B
  - P1 · drills: qc-basis-converge, qc-extrapolate-change
- ● **QC-3.2.B** (molssi-qm-tools:4) Compute a counterpoise-corrected interaction energy and explain basis-set superposition error.
  - EK: In a small basis each monomer borrows functions from its partner, over-binding the complex; the counterpoise correction recomputes each monomer in the full dimer basis and subtracts the difference.
  - Needs: QC-3.2.A
  - P1 · drills: qc-counterpoise, qc-bsse-why

## Unit 4 · Correlation methods

Big ideas: APPROX, SCALE

### 4.1 Perturbation theory



- ● **QC-4.1.A** (psi4numpy-tutorials:05, psi4numpy-tutorials:05a, psi4numpy-tutorials:05b) State what MP2 adds and when perturbation theory is the wrong tool.
  - EK: MP2 adds the leading double-excitation correction from the Hartree-Fock reference. It fails where the reference is poor: small gaps, bond breaking, diradicals, and transition metals.
  - Needs: QC-2.3.B, QC-3.2.B
  - P2 · drills: qc-mp2-limits, qc-mp2-scaling-use
- ● **QC-4.1.B** (psi4numpy-tutorials:05, psi4numpy-tutorials:05a) Compute an MP2 correlation contribution from given orbital energies and integrals for one excitation.
  - EK: Each doubly-excited amplitude contributes a term whose numerator is the integral squared and whose denominator is the sum of occupied minus virtual orbital energies, so small gaps make large contributions.
  - Needs: QC-4.1.A
  - P1 · drills: qc-mp2-term, qc-mp2-contribution

### 4.2 Coupled cluster and configuration interaction



- ● **QC-4.2.A** (psi4numpy-tutorials:08) Order the common correlation methods by cost and accuracy, and say what CCSD(T) means.
  - EK: MP2, then CCSD, then CCSD(T), which adds a perturbative triples correction and is the usual accuracy reference for single-reference molecules.
  - Needs: QC-4.1.B
  - P2 · drills: qc-cc-order, qc-method-ladder
- ● **QC-4.2.B** (psi4numpy-tutorials:08) Compute how much longer a calculation takes when the system grows, from a method's formal scaling.
  - EK: Formal cost scales as a power of basis size: about the fourth power for Hartree-Fock, the fifth for MP2, the sixth for CCSD and the seventh for CCSD(T). The ratio of two sizes raised to that power is the slowdown.
  - Needs: QC-4.2.A
  - P1 · drills: qc-scaling-ratio, qc-basis-for-cost

### 4.3 Interactions



- ● **QC-4.3.A** (psi4numpy-tutorials:07) Say what a symmetry-adapted perturbation theory decomposition gives that a total interaction energy does not.
  - EK: It splits the interaction into electrostatics, exchange, induction and dispersion, so two complexes with the same binding energy can be told apart by what binds them.
  - Needs: QC-4.2.B
  - P2 · drills: qc-sapt-why, qc-sapt-levels
- ● **QC-4.3.B** (psi4numpy-tutorials:07) Attribute a described interaction to the dominant SAPT component.
  - EK: A hydrogen bond is electrostatics-dominated; two nonpolar rings stacking is dispersion-dominated; a polar molecule beside a polarisable one gains induction.
  - Needs: QC-4.3.A
  - P2 · drills: qc-sapt-attribute, qc-sapt-total

## Unit 5 · Density functional theory

Big ideas: APPROX, SCALE

### 5.1 What a functional is



- ● **QC-5.1.A** (psi4numpy-tutorials:04, psi4numpy-tutorials:04b, psi4numpy-tutorials:04c) Place a functional on the rungs from local density through generalised gradient to hybrid and double hybrid, and say what each rung adds.
  - EK: LDA uses the density; GGA adds its gradient; meta-GGA adds the kinetic-energy density; a hybrid mixes in exact exchange; a double hybrid adds perturbative correlation.
  - Needs: QC-2.3.B
  - P2 · drills: qc-functional-rungs, qc-functional-pick
- ● **QC-5.1.B** (psi4numpy-tutorials:04, psi4numpy-tutorials:04e) Compute the exchange mixture a hybrid applies from its stated fraction of exact exchange.
  - EK: A hybrid replaces a stated fraction of the functional's exchange with Hartree-Fock exchange; range-separated hybrids make that fraction depend on distance.
  - Needs: QC-5.1.A
  - P1 · drills: qc-hybrid-mix, qc-exchange-fraction

### 5.2 Practice and pitfalls



- ● **QC-5.2.A** (psi4numpy-tutorials:04, psi4numpy-tutorials:04d) Name what DFT handles poorly and the correction usually applied.
  - EK: Plain functionals miss long-range dispersion, so an empirical correction is added; self-interaction error distorts charge-transfer states and barriers, which range-separated hybrids reduce.
  - Needs: QC-5.1.B
  - P2 · drills: qc-dft-pitfalls, qc-dispersion-share
- ● **QC-5.2.B** (psi4numpy-tutorials:04, psi4numpy-tutorials:04a) Compute an integration-grid or a dispersion-corrected energy from stated components.
  - EK: The total is the functional's energy plus the dispersion correction, which is a sum of damped pairwise terms; a grid too coarse adds noise that looks like a real energy difference.
  - Needs: QC-5.2.A
  - P1 · drills: qc-dispersion-total, qc-grid-and-noise

## Unit 6 · Geometry, frequencies and properties

Big ideas: CONVERGE

### 6.1 Geometry optimisation



- ● **QC-6.1.A** (molssi-qm-tools:1) State what an optimiser converges on and how a minimum is told from a saddle point.
  - EK: The gradient goes to zero at any stationary point; the Hessian's eigenvalues decide which it is, and a frequency calculation reports one imaginary frequency for a transition state.
  - Needs: QC-2.3.B, QC-3.2.B
  - P2 · drills: qc-stationary-points, qc-opt-practice
- ● **QC-6.1.B** (molssi-qm-tools:2, molssi-qm-tools:3) Read a potential energy surface scan for a bond length, angle or intermolecular distance and extract the minimum and the well depth.
  - EK: Scanning one coordinate while relaxing or fixing the rest gives a curve whose minimum is the equilibrium value and whose depth below the separated limit is the binding energy.
  - Needs: QC-6.1.A
  - P1 · drills: qc-well-depth, qc-equilibrium-scan

### 6.2 Frequencies and thermochemistry



- ● **QC-6.2.A** (psi4numpy-tutorials:06) Compute a zero-point vibrational energy from a set of harmonic frequencies.
  - EK: ZPE is half the sum of h times each harmonic frequency; a nonlinear molecule of n atoms has 3n - 6 modes and a linear one 3n - 5.
  - Needs: QC-6.1.B
  - P1 · drills: qc-zpe, qc-mode-count
- ● **QC-6.2.B** (molssi-qm-tools:5, psi4numpy-tutorials:06) Compute a reaction energy or a standard potential from computed energies and say what corrections it needs.
  - EK: A reaction energy is the sum of products minus reactants, corrected for zero-point energy and thermal terms; an electrode potential divides the free-energy change by minus the electrons times the Faraday constant and needs a reference.
  - Needs: QC-6.2.A
  - P1 · drills: qc-reaction-energy, qc-potential-from-dg

### 6.3 Choosing and reporting



- ● **QC-6.3.B** (psi4numpy-tutorials:01) State what a reported result must include to be reproducible.
  - EK: Method, basis, geometry (or that it was optimised at the same level), any dispersion correction and solvation model, the program and its version, and for a transition state the imaginary frequency.
  - Needs: QC-6.2.B
  - P2 · drills: qc-report-reproducible, qc-report-missing
- ● **QC-6.3.A** (psi4numpy-tutorials:04, psi4numpy-tutorials:08, molssi-qm-tools:4) Choose a method and basis for a stated problem and defend both choices.
  - EK: Match the treatment to the chemistry and the basis to the property: geometries tolerate small bases, interaction energies do not; a multireference problem rules out single-reference methods whatever the basis.
  - Needs: QC-6.3.B
  - P2 · drills: qc-method-choice, qc-cost-decision
