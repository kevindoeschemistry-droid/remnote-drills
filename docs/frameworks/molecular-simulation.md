# Molecular Simulation — curriculum framework (draft 1)

Generated from `drills/frameworks/molecular-simulation.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**102 learning objectives** in 14 units (96 core): 0 drilled, 0 partly, 102 with no drills. Core: 0 / 96 drilled.

## Big ideas

- **BOLTZ · Probabilities are free energies.** Every observable is a Boltzmann-weighted average, and every free-energy difference is a log of a population or partition-function ratio. Turning counts into kcal/mol and back is the core move of the field.
- **MODEL · The answer is only as good as the model.** A force field, water model, protonation state, box and cutoff scheme define the Hamiltonian being sampled. They are one package; change one piece and the results belong to a different model.
- **DYN · Dynamics is a sampling engine.** Integrators, constraints, thermostats and barostats exist to generate the right ensemble stably and efficiently. Their parameters trade accuracy, speed and fidelity of the dynamics.
- **SAMPLE · Finite, correlated sampling sets the error bar.** Trajectories are correlated time series of finite length. The number of independent samples, not the number of frames, sets the uncertainty, and unvisited states produce error no error bar shows.
- **PATH · Free energy is a state function.** Because ΔG depends only on endpoints, non-physical alchemical paths and thermodynamic cycles give physical answers. Good paths keep neighbouring states overlapping.
- **ALCH · Alchemical space can be sampled like real space.** λ dynamics treats λ as a coordinate with its own dynamics; with implicit constraints and flattened biases, one simulation visits many chemical end states, and their populations give the free energies.
- **WORK · Simulation is a reproducible pipeline.** Results come from scripts run on shared clusters. Correct scheduling, engine choice, bookkeeping and documentation decide whether a number can be trusted, repeated and published.

## Practices

- **P1 · Define the system and ensemble.** State what physical question is asked, which ensemble and endpoints answer it, and which states (folded/unfolded, bound/unbound) must be simulated.
- **P2 · Build the model.** Choose force field, water, protonation and tautomer states, termini, ions, box shape and size, and write them down.
- **P3 · Choose the method and its parameters.** Pick integrator, timestep, constraints, thermostat, barostat, electrostatics, estimator, λ schedule or ALF options to fit the goal, and check each against its validity conditions.
- **P4 · Compute with units.** kcal/mol and k_BT, Å and nm, fs/ps/ns, steps vs time, molar vs per-molecule; never mix them silently.
- **P5 · Check and quantify.** Sanity-check limits and magnitudes, test equilibration and convergence, estimate uncertainty from independent samples, and close cycles.
- **P6 · Run, script and document.** Write and debug engine scripts and job files, run them on the cluster, and keep every input needed to reproduce the result.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Statistical mechanics for simulation | core | — | 6 | 0 | 0 | 6 |
| 2 · Force fields | core | — | 7 | 0 | 0 | 7 |
| 3 · Integration and MD algorithms | core | — | 6 | 0 | 0 | 6 |
| 4 · Thermostats and barostats | core | — | 5 | 0 | 0 | 5 |
| 5 · Periodic boundaries and long-range electrostatics | core | — | 6 | 0 | 0 | 6 |
| 6 · System preparation and equilibration | core | — | 7 | 0 | 0 | 7 |
| 7 · Sampling, convergence and uncertainty | core | — | 7 | 0 | 0 | 7 |
| 8 · Free-energy theory and estimators | core | — | 11 | 0 | 0 | 11 |
| 9 · Thermodynamic cycles, binding and stability | core | — | 8 | 0 | 0 | 8 |
| 10 · λ dynamics and multisite λ dynamics | core | — | 9 | 0 | 0 | 9 |
| 11 · Adaptive Landscape Flattening in practice | core | — | 9 | 0 | 0 | 9 |
| 12 · Trajectory analysis | core | — | 6 | 0 | 0 | 6 |
| 13 · HPC, engines and reproducible workflow | core | — | 9 | 0 | 0 | 9 |
| 14 · Advanced λ dynamics | extension | — | 6 | 0 | 0 | 6 |

## Unit 1 · Statistical mechanics for simulation

Big ideas: BOLTZ, SAMPLE

### 1.1 Ensembles, ergodicity and temperature

Book: livecoms-md-basics §3.3; frenkel-smit §Ch 2; tuckerman §Ch 3, §Ch 4, §Ch 5; allen-tildesley §Ch 2

- ○ **MD-1.1.A** Choose the ensemble (NVE, NVT, NPT, μVT) that matches a described experiment or simulation goal — choice rep.
  - EK: Bench conditions (fixed T and P) ⇒ NPT, whose free energy is G; NVT gives A; NVE conserves H and is used to test integrators and measure unperturbed dynamics.
  - P1
- ○ **MD-1.1.B** State the ergodic hypothesis and identify features of a system that break it on simulation timescales.
  - EK: Time average = ensemble average only if the trajectory visits all relevant states; barriers of many k_BT (slow rotamers, buried waters, unfolding) make runs quasi-nonergodic.
  - P5
- ○ **MD-1.1.C** Calculate the instantaneous temperature from kinetic energy and the count of degrees of freedom — numeric rep.
  - EK: ⟨K⟩ = (N_df/2) k_B T; N_df = 3N − N_constraints − 3 when centre-of-mass motion is removed.
  - P4

### 1.2 Boltzmann weights and free energy

Book: livecoms-md-basics §3.2, §3.3; frenkel-smit §Ch 2; tuckerman §Ch 4, §Ch 5

- ○ **MD-1.2.A** Calculate the population ratio of two states from their energy difference at a given temperature — numeric rep.
  - EK: p_i/p_j = exp[−(E_i − E_j)/k_BT]; k_BT = 0.593 kcal/mol at 298.15 K, so 1.36 kcal/mol is a factor of 10.
  - P4
- ○ **MD-1.2.B** Convert between a population (or probability) ratio and a free-energy difference — numeric rep.
  - EK: ΔG_A→B = −k_BT ln(P_B/P_A); a free energy counts every microstate of a state, so it includes entropy, not just the lowest energy.
  - Needs: MD-1.2.A
  - P4
- ○ **MD-1.2.C** Distinguish Helmholtz and Gibbs free energy and the potential of mean force along a coordinate, and state which one a given simulation yields.
  - EK: A = −k_BT ln Q (NVT), G = −k_BT ln Δ (NPT); W(ξ) = −k_BT ln P(ξ) + const. Absolute Q is intractable, but ratios of Q are ensemble averages.
  - P1

## Unit 2 · Force fields

Big ideas: MODEL

### 2.1 The CHARMM functional form

Book: livecoms-md-basics §3.5, §4.1; allen-tildesley §Ch 1; molssi-mmtools §Introduction

- ○ **MD-2.1.A** Write the CHARMM potential energy function term by term and name each parameter and the pairs each term excludes.
  - EK: Bonds K_b(b − b₀)², angles K_θ(θ − θ₀)², Urey–Bradley, dihedrals K_φ[1 + cos(nφ − δ)], impropers, CMAP, LJ ε[(R_min/r)¹² − 2(R_min/r)⁶], Coulomb; 1-2 and 1-3 pairs excluded, 1-4 pairs use special LJ parameters.
  - P2
- ○ **MD-2.1.B** Calculate a Lennard-Jones or Coulomb pair energy from CHARMM parameters using the combining rules — numeric rep.
  - EK: ε_ij = √(ε_i ε_j), R_min,ij = R_min,i/2 + R_min,j/2; Coulomb = 332.06 q_i q_j / r kcal/mol with r in Å and q in e.
  - P4

### 2.2 Topology, parameter and structure files

Book: orientation §Tutorial 2, §Tutorial 4.3

- ○ **MD-2.2.A** Explain what RTF, PRM, PSF, CRD and toppar.str files each contain and which ones CHARMM reads in what order.
  - EK: RTF: atoms, types, charges, connectivity and patches per residue (which terms exist); PRM: the constants in those terms; PSF: the generated list of atoms, bonds, angles, dihedrals of this system; CRD: coordinates; toppar.str streams the RTF/PRM set.
  - P2 · P6
- ○ **MD-2.2.B** Map a residue's chemical state to its CHARMM36 name or patch: ASPP, GLUP, HSD/HSE/HSP, LSN, NTER/CTER, ACE/CT3 — choice rep.
  - EK: ASP, GLU deprotonated and LYS protonated by default; HIS must always be specified; charged termini for a whole protein, neutral ACE/CT3 caps for a peptide cut from a chain.
  - P2

### 2.3 Parameterization

Book: livecoms-md-basics §4.1; orientation §Installation

- ○ **MD-2.3.A** Describe how CHARMM36/CGenFF charges, dihedrals and LJ parameters are fitted, and why water model, cutoffs, constraints and 1-4 treatment belong to the parameter set.
  - EK: Charges fit to QM interaction energies with TIP3P water; dihedrals to QM scans; LJ to liquid densities and heats of vaporization. Constraint and cutoff settings are part of the force field definition — match the parameterizing work.
  - P2
- ○ **MD-2.3.B** Judge a CGenFF (ParamChem) parameter assignment from its penalty scores and decide whether to validate or reoptimize — choice rep.
  - EK: Penalty < 10 ≈ fine; 10–50 validate; > 50 reparameterize against QM.
  - P2 · P5

### 2.4 Water models

Book: livecoms-md-basics §4.1; orientation §Tutorial 2

- ○ **MD-2.4.A** Compare TIP3P (CHARMM variant), SPC/E and TIP4P-type models by geometry, rigidity and known property errors, and name the model CHARMM36 assumes.
  - EK: TIP3P: rigid 3-site; the CHARMM variant adds LJ on H; diffuses ~2× too fast but CHARMM36 is fitted with it. TIP4P models add a virtual M site carrying the negative charge.
  - P2

## Unit 3 · Integration and MD algorithms

Big ideas: DYN

### 3.1 Verlet-family integrators

Book: livecoms-md-basics §3.1, §4.3; frenkel-smit §Ch 4, §App H; allen-tildesley §Ch 3; tuckerman §Ch 3

- ○ **MD-3.1.A** Write one step of velocity Verlet and of leapfrog and explain why their time reversibility and symplecticity give bounded energy error.
  - EK: Leapfrog: v(t + ½Δt) = v(t − ½Δt) + a(t)Δt, x(t + Δt) = x(t) + v(t + ½Δt)Δt. Symplectic integrators conserve a shadow Hamiltonian, so NVE energy fluctuates without drift; drift signals a bad Δt or cutoff artifacts.
  - P3
- ○ **MD-3.1.B** Advance positions and velocities through one or two integration steps for a given 1-D force — numeric rep.
  - EK: Velocity Verlet: x₁ = x₀ + v₀Δt + ½a₀Δt²; v₁ = v₀ + ½(a₀ + a₁)Δt.
  - P4

### 3.2 Timestep and constraints

Book: livecoms-md-basics §4.3; livecoms-afe §7.1.1; hayes2021-blade §2; allen-tildesley §Ch 3

- ○ **MD-3.2.A** Calculate the period of the fastest vibration from its wavenumber and pick the largest stable timestep with and without hydrogen-bond constraints — numeric rep.
  - EK: T = 1/(c ν̃); X–H stretches at 3000–3600 cm⁻¹ have T ≈ 9–11 fs; with Δt ≲ T/10 that is ~1 fs unconstrained, ~2 fs with X–H constrained (rigid water roughly doubles Δt).
  - P3 · P4
- ○ **MD-3.2.B** Explain how SHAKE, RATTLE and SETTLE impose holonomic constraints and count the degrees of freedom they remove.
  - EK: Lagrange multipliers iteratively restore bond lengths each step; SETTLE solves rigid 3-site water analytically; each constraint removes one degree of freedom (enters N_df).
  - Needs: MD-1.1.C
  - P3
- ○ **MD-3.2.C** Decide when to use hydrogen mass repartitioning at 4 fs, or drop constraints and use 1 fs, including for bonds to alchemical atoms — choice rep.
  - EK: HMR moves mass from heavy atoms to their H, conserving total mass and thermodynamics but altering kinetics. Constraints on bonds that change length between alchemical states bias single-topology results; 1 fs without them is the general fix.
  - P3
- ○ **MD-3.2.D** Diagnose an unstable timestep or bad starting structure from run symptoms (SHAKE failures, energy blow-up, temperature spikes).
  - EK: Early crashes usually mean unrelaxed contacts (minimize) or too large a Δt; steady NVE drift means Δt, constraint tolerance or cutoff treatment is too loose.
  - P5

## Unit 4 · Thermostats and barostats

Big ideas: DYN, MODEL

### 4.1 Thermostats

Book: livecoms-md-basics §4.4; frenkel-smit §Ch 7; tuckerman §Ch 4, §Ch 15; hayes2021-blade §2

- ○ **MD-4.1.A** Choose a thermostat for a stated goal — fast equilibration, canonical production, or dynamical properties — and justify it — choice rep.
  - EK: Bussi: general purpose; Nosé–Hoover chains: canonical, better ergodicity in small systems; Langevin: canonical, robust, damps dynamics; Berendsen and simple velocity rescaling give the wrong ensemble (flying ice cube).
  - P3
- ○ **MD-4.1.B** Write the Langevin equation and explain how the friction coefficient (CHARMM fbeta, ps⁻¹) trades temperature control against dynamical fidelity.
  - EK: m dv/dt = F − γmv + R(t), ⟨R(t)R(t′)⟩ = 2γm k_BT δ(t − t′). BLaDE uses a g-BAOAB Langevin integrator; the tutorial's fbeta 0.1 ps⁻¹ is weak coupling.
  - P3

### 4.2 Barostats and density

Book: livecoms-md-basics §4.5; frenkel-smit §Ch 6, §Ch 7; hayes2021-blade §2; blade-doc §BLaDE

- ○ **MD-4.2.A** Choose a barostat for equilibration vs production and for isotropic vs anisotropic cells — choice rep.
  - EK: Berendsen only for early equilibration; Monte Carlo barostat, Langevin piston and Parrinello–Rahman sample NPT; anisotropic or semi-isotropic coupling for membranes and crystals.
  - P3
- ○ **MD-4.2.B** Explain how a Monte Carlo barostat accepts a volume move and set its BLaDE parameters (prmc, iprs, pref, prdv).
  - EK: Accept with min{1, exp[−β(ΔU + PΔV) + N ln(V′/V)]}; BLaDE's N counts heavy atoms. iprs = steps between attempts (default 50), pref = pressure in atm (1), prdv = σ of ΔV in Å³ (100).
  - P3 · P6
- ○ **MD-4.2.C** Calculate a system's density from its box dimensions and total mass and check it against the expected value — numeric rep.
  - EK: ρ = M/(N_A V); 1 g/cm³ = 0.6022 amu/Å³. Pure TIP3P at 298 K should sit near 0.98–1.0 g/cm³.
  - P4 · P5

## Unit 5 · Periodic boundaries and long-range electrostatics

Big ideas: MODEL, DYN

### 5.1 Periodic boundary conditions and box choice

Book: livecoms-md-basics §4.2; orientation §Tutorial 1.2, §Tutorial 2; allen-tildesley §Ch 1; frenkel-smit §Ch 4

- ○ **MD-5.1.A** Apply the minimum-image convention to find the distance between two atoms in a periodic box — numeric rep.
  - EK: Δx ← Δx − L·round(Δx/L) per axis; valid only when the nonbonded cutoff is below L/2.
  - P4
- ○ **MD-5.1.B** Size a solvent box from the solute's extent and edge distance and compare atom counts for cubic, truncated-octahedral and rhombic-dodecahedral cells — numeric rep.
  - EK: Cube side = d_max + 2 × edge (10 Å is standard; more for highly charged solutes like RNA). For the same image distance d: V_cube = d³, V_oct ≈ 0.770 d³ (23% fewer atoms), V_RD ≈ 0.707 d³ (29% fewer). Water ≈ 0.0334 molecules/Å³.
  - P2 · P4
- ○ **MD-5.1.C** Explain why periodic artifacts are smaller than vacuum-interface artifacts and name the cases where they are not.
  - EK: A droplet's surface distorts the solute; images avoid it. Artifacts grow with net charge, small boxes, and solutes that expand (unfolded chains need a fixed, larger box, e.g. 40 Å for the pentapeptides).
  - P2 · P5

### 5.2 Cutoffs and particle-mesh Ewald

Book: livecoms-md-basics §3.4, §4.2; frenkel-smit §Ch 11; allen-tildesley §Ch 6; hayes2021-blade §2; orientation §Tutorial 1.2, §Tutorial 4.3

- ○ **MD-5.2.A** Explain why truncating Coulomb interactions fails in condensed phases and how Ewald splitting into real- and reciprocal-space sums fixes it.
  - EK: 1/r decays slower than the number of neighbours grows (∝ r²). Ewald: erfc(κr)/r is short-ranged in real space; the smooth remainder is summed on a reciprocal grid (PME, O(N log N)); a uniform neutralizing background handles net charge.
  - P3
- ○ **MD-5.2.B** Choose PME parameters (real-space cutoff, κ, grid spacing, interpolation order) consistent with a target accuracy — choice rep.
  - EK: Typical CHARMM36 setup: 12 Å cutoff, κ ≈ 0.34 Å⁻¹, grid spacing ≤ 1 Å, order 4–6 (BLaDE supports 4, 6, 8). Larger κ shifts work to reciprocal space.
  - P3
- ○ **MD-5.2.C** Distinguish switched, shifted and force-switched LJ cutoffs and pick the CHARMM36 standard, including neighbour-list buffer.
  - EK: CHARMM36: vfswitch from 10 to 12 Å, pair list to 14–16 Å; BLaDE requires PME or VSWITCH for electrostatics and VFSWITCH or VSHIFT for LJ. Apply long-range dispersion corrections only if the force field was fitted with them.
  - P3

## Unit 6 · System preparation and equilibration

Big ideas: MODEL, SAMPLE

### 6.1 Building the system

Book: orientation §Tutorial 1.2; livecoms-md-basics §4.3.1; livecoms-afe §5.1, §5.2

- ○ **MD-6.1.A** Assign protonation states from propka pKa predictions at the experimental pH, using predicted pKa for the folded state and model pKa for an unfolded peptide — numeric rep.
  - EK: pH < pKa ⇒ protonated; fraction protonated = 1/(1 + 10^(pH − pKa)). Check ASP, GLU, HIS, LYS; ARG, TYR, CYS rarely titrate. Record the states — they go in the methods section.
  - P2 · P4
- ○ **MD-6.1.B** Choose a histidine tautomer (HSD, HSE, HSP) from its pKa and hydrogen-bond environment — choice rep.
  - EK: Protonated ⇒ HSP; otherwise put H on the δ or ε N according to nearby donors/acceptors; HSE when exposed or unclear (marginally more stable in the unfolded state).
  - Needs: MD-6.1.A
  - P2
- ○ **MD-6.1.C** Calculate the number of counterions and salt ion pairs needed to neutralize a box and reach a target concentration — numeric rep.
  - EK: N_pairs ≈ c(M) × V(Å³) × 6.022 × 10⁻⁴; neutralize the net solute charge first. Mimic the experiment; otherwise ~150 mM (Na⁺ extracellular, K⁺ intracellular).
  - P2 · P4
- ○ **MD-6.1.D** Build a solvated, ionized protein box in CHARMM-GUI Solution Builder at the experimental temperature, pH and salt, deciding which crystallographic components and termini to keep.
  - EK: Keep crystallographic waters for the folded protein (pockets refill slowly); drop BME/Cl⁻ additives unless relevant; set temperature to the experiment (often 298.15 K, not the 303.15 K default).
  - P2 · P6

### 6.2 Minimization, heating and equilibration

Book: livecoms-md-basics §4.3.2, §4.3.3, §4.3.4, §4.3.5; livecoms-uq §4.1, §5; orientation §Tutorial 1.2

- ○ **MD-6.2.A** Order the preparation stages — minimize, assign velocities, restrained NVT, NPT, production — and justify each stage.
  - EK: Minimize to remove clashes; relax solvent at constant volume with solute restrained; then relax volume at constant pressure; NVT production at a set density needs NPT equilibration first.
  - P1 · P3
- ○ **MD-6.2.B** Calculate the per-component velocity spread or RMS speed of an atom drawn from a Maxwell–Boltzmann distribution — numeric rep.
  - EK: σ_v = √(k_BT/m) per Cartesian component; v_rms = √(3k_BT/m).
  - P4
- ○ **MD-6.2.C** Decide when equilibration is complete from time series of energy, temperature, pressure, density and RMSD, and discard the burn-in.
  - EK: No drift and fluctuation about a stable mean in several observables; if unsure, extend. Analyse only the production portion, applying the cut uniformly.
  - P5

## Unit 7 · Sampling, convergence and uncertainty

Big ideas: SAMPLE

### 7.1 Correlation in time series

Book: livecoms-uq §6.1, §7.3.1; frenkel-smit §App G; allen-tildesley §Ch 8; livecoms-md-basics §4.3.5

- ○ **MD-7.1.A** Compute a normalized autocorrelation function and integrated correlation time from a short time series — numeric rep.
  - EK: C_j = ⟨δx_k δx_{k+j}⟩ / s²; τ_int = Σ_j C_j, summed until it converges but before it integrates noise.
  - P4
- ○ **MD-7.1.B** Calculate the statistical inefficiency and effective number of independent samples, and from them the standard error of a mean — numeric rep.
  - EK: g = 1 + 2Σ_{j≥1} C_j (in frames); N_ind = N/g; s(x̄) = s(x)/√N_ind. Saving frames more often than τ adds disk, not information.
  - Needs: MD-7.1.A
  - P4 · P5

### 7.2 Error bars

Book: livecoms-uq §6.2, §7.2, §7.3.2, §7.4, §7.5, §7.6

- ○ **MD-7.2.A** Compute a standard error from block averages and identify the block size at which the estimate plateaus — numeric rep.
  - EK: Split N frames into M equal blocks of n; s(x̄) = s(block means)/√M; increase n until s(x̄) stops growing.
  - P4 · P5
- ○ **MD-7.2.B** Compute a standard error and 95% confidence interval from n independent trials using the Student t factor — numeric rep.
  - EK: SE = s/√n with s over trial means; CI = x̄ ± t·SE, t(0.975, n − 1) = 2.78 for n = 5, 2.57 for n = 6. Starting structures must be independent for this to hold.
  - P4 · P5
- ○ **MD-7.2.C** Propagate uncertainty through sums, differences and nonlinear functions, e.g. σ(ΔΔG) from two legs — numeric rep.
  - EK: Independent legs: σ²(a − b) = σ²_a + σ²_b; nonlinear F: σ²_F ≈ Σ(∂F/∂x_i)² σ²_i, valid when noise-to-signal is small.
  - P4
- ○ **MD-7.2.D** Bootstrap a confidence interval for a derived quantity from correlated data, and report it with significant figures that match the uncertainty.
  - EK: Resample blocks or independent trials, not raw frames; 95% CI = 2.5th–97.5th percentile. Report the confidence level and only meaningful digits.
  - P5

### 7.3 Sampling quality

Book: livecoms-uq §2, §3, §4.2, §4.4, §7.7; livecoms-afe §4.2

- ○ **MD-7.3.A** Distinguish statistical uncertainty from sampling error that no error bar reveals, and detect insufficient sampling from drift, rare transitions and disagreement between independent runs.
  - EK: Checks can rule out good sampling but never prove it. Independent runs from diverse starts that disagree beyond their error bars signal unvisited states ('dark uncertainty').
  - P5

## Unit 8 · Free-energy theory and estimators

Big ideas: BOLTZ, PATH, SAMPLE

### 8.1 Free-energy perturbation

Book: livecoms-afe §1, §3.2; frenkel-smit §Ch 8; tuckerman §Ch 8

- ○ **MD-8.1.A** Calculate ΔA from given ⟨exp(−βΔU)⟩ or a list of ΔU samples with the Zwanzig relation, forward and reverse — numeric rep.
  - EK: ΔA_0→1 = −k_BT ln⟨exp(−βΔU)⟩_0, ΔU = U₁ − U₀ evaluated on state-0 samples; exact in the limit, derived from Q₁/Q₀.
  - Needs: MD-1.2.B
  - P4
- ○ **MD-8.1.B** Estimate ΔA from the mean and variance of ΔU with the second-order cumulant expansion — numeric rep.
  - EK: ΔA ≈ ⟨ΔU⟩₀ − βσ²_ΔU/2; exact for Gaussian ΔU.
  - P4
- ○ **MD-8.1.C** Judge whether an FEP estimate is reliable from the ΔU distribution width and forward–reverse hysteresis.
  - EK: The exponential average is biased and dominated by rare low-ΔU samples; reliable only when σ_ΔU ≲ 1–2 k_BT, i.e. neighbouring states overlap. Large forward–reverse disagreement means too few windows.
  - P5

### 8.2 Thermodynamic integration

Book: livecoms-afe §1, §3.2; frenkel-smit §Ch 8; tuckerman §Ch 8

- ○ **MD-8.2.A** Calculate ΔA by integrating ⟨∂U/∂λ⟩ over λ windows with the trapezoid or Simpson rule — numeric rep.
  - EK: ΔA = ∫₀¹ ⟨∂U/∂λ⟩_λ dλ; trapezoid needs evenly or explicitly weighted windows; Simpson needs an odd number of evenly spaced points.
  - P4
- ○ **MD-8.2.B** Derive ∂U/∂λ for a linear mixing potential and explain why curvature near the endpoints demands more windows or soft-core.
  - EK: U = (1 − λ)U₀ + λU₁ ⇒ ∂U/∂λ = U₁ − U₀; for appearing atoms ⟨∂U/∂λ⟩ diverges as λ → 0 under linear LJ scaling.
  - P3

### 8.3 BAR, MBAR and overlap

Book: livecoms-afe §1, §3.2, §7.2.3; frenkel-smit §Ch 8

- ○ **MD-8.3.A** Explain how BAR combines forward and reverse ΔU samples and why it beats one-sided exponential averaging.
  - EK: BAR solves a self-consistent equation for ΔA using both directions; it is the minimum-variance two-state estimator and much less biased than Zwanzig.
  - P3
- ○ **MD-8.3.B** Explain MBAR as reweighting all samples to all states, and relate it to BAR and WHAM.
  - EK: MBAR solves for every state's free energy simultaneously from all samples; with two states it reduces to BAR; binned, it is WHAM (used in ALF flattening).
  - P3
- ○ **MD-8.3.C** Read an MBAR overlap matrix and decide where to add λ states — choice rep.
  - EK: Each state should share substantial overlap with its neighbours (off-diagonal elements not near zero); a weak link between two neighbours is where to insert a state. 20–40 states are typical.
  - Needs: MD-8.3.B
  - P5

### 8.4 Alchemical pathways and soft-core

Book: livecoms-afe §7.1.1, §7.2.3; hayes2017-alf §Methods

- ○ **MD-8.4.A** Design an alchemical λ schedule for inserting or deleting atoms: order of electrostatic and LJ changes, soft-core, and number of states.
  - EK: Remove charges while LJ cores are on, then transform LJ with soft-core, then restore charges on inserted atoms; never change both at once on linear paths when sites appear or vanish.
  - P3
- ○ **MD-8.4.B** Explain the endpoint catastrophe and how soft-core potentials remove it.
  - EK: As an atom's LJ is scaled to zero, other atoms can overlap it and r⁻¹² diverges; soft-core remaps short distances so the energy stays finite (in MSλD, distances inside a λ-dependent cutoff, r₀ = 2 Å).
  - P3
- ○ **MD-8.4.C** Distinguish single, dual and multiple topology and decoupling vs annihilation, and identify the topology MSλD uses — choice rep.
  - EK: MSλD uses a shared core plus one complete substituent group per alternative; substituents at the same site never interact with each other; decoupling turns off only intermolecular terms.
  - P2 · P3

## Unit 9 · Thermodynamic cycles, binding and stability

Big ideas: PATH, BOLTZ

### 9.1 Relative free energies

Book: livecoms-afe §3.2, §7.1; orientation §Tutorial 1, §Tutorial 3.2; alf-readme §Best Practices

- ○ **MD-9.1.A** Close a thermodynamic cycle to compute a relative binding ΔΔG from alchemical legs in complex and solvent — numeric rep.
  - EK: ΔΔG_bind = ΔG_bind(B) − ΔG_bind(A) = ΔG_complex(A→B) − ΔG_solvent(A→B); the physical binding legs are never simulated.
  - Needs: MD-1.2.B
  - P1 · P4
- ○ **MD-9.1.B** Compute a mutational folding ΔΔG from alchemical legs in the folded protein and an unfolded-state peptide model, and state its sign convention — numeric rep.
  - EK: ΔΔG_fold = ΔG_alch(folded) − ΔG_alch(unfolded); positive = destabilizing. The capped pentapeptide (mutating residue ± 2) models a locally solvated unfolded state and ignores nonlocal contacts.
  - P1 · P4
- ○ **MD-9.1.C** Compute cycle-closure errors in a perturbation network and use them to flag unreliable edges — numeric rep.
  - EK: ΔG summed around any closed loop should be 0; nonzero closure measures error. Star maps are cheap; redundant, connected maps allow error analysis.
  - P5

### 9.2 Absolute binding

Book: livecoms-afe §3.2, §6.1, §7.1.2

- ○ **MD-9.2.A** Lay out the double-decoupling cycle with restraints and identify every term in ΔG°_bind, including the standard-state correction.
  - EK: Decouple the ligand in solvent and in the restrained site; add the restraint free energy (analytic for Boresch's six-DOF restraints) and the standard-state term; remove charges before LJ.
  - P1
- ○ **MD-9.2.B** Calculate the standard-state correction for confining a ligand to a given restraint volume — numeric rep.
  - EK: ΔG = −k_BT ln(V_site/V°), V° = 1661 Å³ per molecule at 1 M.
  - P4
- ○ **MD-9.2.C** Choose a relative or absolute calculation for a described project — choice rep.
  - EK: Relative: congeneric series with a shared core and a reliable bound pose. Absolute: no common substructure, uncertain site, or comparing sites or poses.
  - P1 · P3

### 9.3 Comparing to experiment

Book: livecoms-afe §4.1, §4.3, §5.1, §5.4

- ○ **MD-9.3.A** Convert between K_d and ΔG° and between fold-changes and ΔΔG, and judge a prediction against expected accuracy — numeric rep.
  - EK: ΔG° = RT ln(K_d/1 M); a 10× change in K_d is 1.36 kcal/mol at 298 K; ~1–2 kcal/mol RMS error is typical in favourable cases.
  - P4 · P5
- ○ **MD-9.3.B** Match simulation conditions (pH, salt, temperature, construct, protonation) to the experiment being reproduced.
  - EK: The T4 lysozyme sites were measured at pH 3.0 (L99, M106, F153) and 5.4 (V149), so two folded-state setups are needed.
  - P1 · P2

## Unit 10 · λ dynamics and multisite λ dynamics

Big ideas: ALCH, PATH, BOLTZ

### 10.1 λ as a dynamic variable

Book: hayes2017-alf §Methods; hayes2021-blade §2; orientation §Tutorial 2, §Literature

- ○ **MD-10.1.A** Write the λ-dynamics extended Hamiltonian and explain how treating λ as a particle samples several alchemical states in one simulation.
  - EK: H = K(x) + ½ m_λ λ̇² + U(x, λ); λ moves under −∂U/∂λ with a fictitious mass, so its population over time reflects relative free energies.
  - P3
- ○ **MD-10.1.B** Write the MSλD potential for several sites and substituents and identify which terms scale with λ.
  - EK: U = U₀ + Σ_s Σ_i λ_si U_si + Σ λ_si λ_tj U_si,tj (s ≠ t); Σ_i λ_si = 1 and λ_si ≥ 0 at each site; the environment U₀ is unscaled; substituents at one site don't see each other.
  - Needs: MD-10.1.A
  - P3
- ○ **MD-10.1.C** Calculate the number of λ variables and chemical end states for a multisite system from its nsubs list — numeric rep.
  - EK: nsubs counts native + each mutant per site (V149 with 5 mutants ⇒ 6); nblocks = Σ nsubs; end states = Π nsubs (15 sites × 2 ⇒ 32 768).
  - P4

### 10.2 Implicit constraints

Book: hayes2017-alf §Methods; orientation §Tutorial 2, §Literature

- ○ **MD-10.2.A** Compute λ values from θ coordinates with the fnex implicit constraint and verify they sum to one — numeric rep.
  - EK: λ_i = exp(c sin θ_i) / Σ_j exp(c sin θ_j), c = 5.5 (fnex); θ is unbounded, λ stays in (0, 1) and sums to 1 automatically.
  - P4
- ○ **MD-10.2.B** Calculate the λ bounds an fnex constraint can reach for a given number of substituents and explain the endpoint error it causes — numeric rep.
  - EK: Bounds = [1 + (N − 1)e^{±2c}]⁻¹, so exact endpoints are never sampled (≈ 0.1–0.2 kcal/mol error) and sampling weakens past 8–9 substituents; piecewise constraints (fnpwise2026) reach the exact endpoints.
  - Needs: MD-10.2.A
  - P4 · P5

### 10.3 Biasing potentials

Book: hayes2017-alf §Methods; alf-readme §Best Practices; orientation §Tutorial 2

- ○ **MD-10.3.A** Identify the role of each ALF bias term — fixed φ (b), quadratic ψ (c), endpoint χ (x) and ω (s), and the newer t and u terms — on the alchemical landscape.
  - EK: φ offsets each substituent's free energy (≈ −ΔG) so all endpoints are equally populated; ψ_ij/4 changes the barrier between substituents; χ/ω shape the region near endpoints; bcxstu2026 adds t and u terms for many substituents.
  - P3
- ○ **MD-10.3.B** Calculate the number of pairwise bias potentials a block setup must allocate for a given nblocks and bias scheme — numeric rep.
  - EK: Pairs = nblocks(nblocks − 1)/2; bcxs2018 uses 5 potentials per pair, bcxstu2026 uses 9 (ldbi count).
  - Needs: MD-10.1.C
  - P4 · P6

### 10.4 Free energies from λ trajectories

Book: hayes2017-alf §Methods; alf-readme §Best Practices; orientation §Tutorial 3.2, §Tutorial 3.3

- ○ **MD-10.4.A** Calculate the free-energy difference between two substituents from their end-state populations (λ > 0.99) and fixed biases — numeric rep.
  - EK: ΔG_i→j = −k_BT ln(P_j/P_i) − (φ_j − φ_i), with P counted only where λ > λ_c (0.99 in production; 0.8 in older work).
  - Needs: MD-1.2.B, MD-10.3.A
  - P4
- ○ **MD-10.4.B** Interpret nan or very noisy entries in Result.txt as unsampled substituents and decide whether to refine biases before extending production.
  - EK: A histogram estimator needs every end state visited; unvisited substituents mean biases are not yet converged — run another production of the same length first.
  - P5

## Unit 11 · Adaptive Landscape Flattening in practice

Big ideas: ALCH, SAMPLE, WORK

### 11.1 The flattening algorithm

Book: alf-readme §Algorithms; hayes2017-alf §Methods; orientation §Tutorial 3

- ○ **MD-11.1.A** Describe one ALF cycle — run MD, reweight recent runs, compute 1-D and 2-D free-energy profiles, fit bias changes, write the next variables file — and why changes are capped.
  - EK: WHAM/MBAR combine several recent runs at different biases; a linear model of profile response feeds a quadratic penalty on deviations from flat. Only the bottom few kcal/mol of a basin is sampled, so updates are limited to a few kcal/mol.
  - P3
- ○ **MD-11.1.B** Judge from PlotFreeEnergy5 profiles whether flattening has converged enough to start production.
  - EK: Sampling should extend across every profile with no large unsampled gaps; perfect flatness isn't required, thermodynamic accessibility is.
  - P5

### 11.2 Running ALF

Book: alf-readme §Best Practices, §Input Specification; orientation §Tutorial 3.2, §Tutorial 3.3

- ○ **MD-11.2.A** Plan the flattening schedule and convert it to step counts at a given timestep — numeric rep.
  - EK: initialize; ~100 runflat cycles of 100 ps (200 for arginine), equilibration = ¼ of each run (25 ps + 75 ps, so the sampling-steps argument is 3× the equilibration one); then ~10 cycles of 1 ns. At 2 fs, 25 ps = 12 500 steps.
  - P3 · P4
- ○ **MD-11.2.B** Plan a production ramp of independent trials extended by factors of 4–5 to a target length, and total its simulation time — numeric rep.
  - EK: 5 trials (a–e) each round, e.g. 5 → 20 → 100 ns. Typical totals: solvation 10–20 ns; well-behaved protein point mutations 40 ns; hard or multiple mutations 100 ns; massive spaces 400 ns.
  - P3 · P4
- ○ **MD-11.2.C** Write alf_info.py for a system: name, nsubs, nblocks, temp, enginepath, nreps, and optional q, loss, bias and impcons keys.
  - EK: name must match prep/name.inp; nblocks = Σ nsubs; nreps = 1 without replica exchange; q lists each substituent's net charge.
  - Needs: MD-10.1.C
  - P6
- ○ **MD-11.2.D** Choose loss function, bias scheme and implicit constraint for a described system — choice rep.
  - EK: Defaults linear2018 / bcxs2018 / fnex2011 are no longer best practice: use nonlinear2024 loss and fnpwise2026; bcxs2018 for ~2 substituents, bcxstu2026 for ~20 (with matching blocksetup.inp edits).
  - P3
- ○ **MD-11.2.E** Compute ΔΔG_fold with its uncertainty from Result.txt values in the folded and unfolded ensembles — numeric rep.
  - EK: ΔΔG = dG(folded) − dG(unfolded) per mutant relative to native; combine the two legs' errors in quadrature.
  - Needs: MD-9.1.B, MD-7.2.C
  - P4 · P5

### 11.3 Building the alchemical system in CHARMM

Book: orientation §Tutorial 2

- ○ **MD-11.3.A** Edit alchemical_definitions.inp for a mutation set: site resids, substituent sequence codes, segids and terminal variables.
  - EK: s1seq1 = 0 is the native residue; further entries are one-letter codes (h/b/j = HSD/HSE/HSP); nterres/cterres = first and last resid of the chain (1–162 folded, site ± 2 unfolded).
  - P2 · P6
- ○ **MD-11.3.B** Assemble a prep directory — system.inp adapted from step5_production.inp, toppar soft link, aa_stream patch/select/delete/blocksetup streams, nbond.str, alf_info.py — and test it with RunSetup.
  - EK: DIMENS must be in the first script CHARMM reads, so it is removed from system.inp; patchloop adds alchemical atoms, selectloop names them, deleteloop removes spurious angles/dihedrals, blocksetup applies λ scaling and biases.
  - Needs: MD-11.3.A
  - P6

## Unit 12 · Trajectory analysis

Big ideas: SAMPLE, BOLTZ

### 12.1 Structural deviation and fluctuation

Book: livecoms-uq §4.2; livecoms-afe §5.4; molssi-mmtools §MD Simulation of a Protein

- ○ **MD-12.1.A** Compute the RMSD between two small coordinate sets after optimal superposition, and use RMSD vs time to judge stability before free-energy runs — numeric rep.
  - EK: RMSD = √[(1/N) Σ |r_i − r_i^ref|²] after Kabsch alignment on a chosen atom set (Cα or backbone); a plateau, not a small number, is the stability signal.
  - P4 · P5
- ○ **MD-12.1.B** Compute per-residue RMSF and convert it to a crystallographic B-factor for comparison with experiment — numeric rep.
  - EK: RMSF_i = √⟨|r_i − ⟨r_i⟩|²⟩ after alignment; B = (8π²/3) RMSF².
  - P4

### 12.2 Interactions, clustering and distributions

Book: livecoms-uq §4.2, §4.4; frenkel-smit §Ch 5

- ○ **MD-12.2.A** Classify a contact as a hydrogen bond from donor–acceptor distance and angle under a stated criterion — choice rep.
  - EK: Common criterion: D···A ≤ 3.5 Å and D–H···A angle ≥ 120–150°; report occupancy as fraction of frames, and state the criterion used.
  - P4
- ○ **MD-12.2.B** Cluster conformations by RMSD and report cluster populations and representative structures.
  - EK: Cutoff-based or hierarchical clustering on pairwise RMSD; combined clustering of independent runs tests whether they sample the same states.
  - P5
- ○ **MD-12.2.C** Compute a potential of mean force from a histogram of a coordinate — numeric rep.
  - EK: W(ξ) = −k_BT ln P(ξ) + const; bins with no counts carry no information.
  - Needs: MD-1.2.B
  - P4

### 12.3 Visualization and trajectory handling

Book: orientation §Tutorial 1.2, §Installation; molssi-mmtools §MD Simulation of a Protein

- ○ **MD-12.3.A** Load a trajectory correctly (PSF before DCD in VMD) and re-centre or unwrap periodic coordinates before measuring.
  - EK: A DCD holds only coordinates; the PSF supplies atom identities. Molecules split across box faces corrupt RMSD and distances until imaged.
  - P6

## Unit 13 · HPC, engines and reproducible workflow

Big ideas: WORK, DYN

### 13.1 The cluster and SLURM

Book: orientation §Cluster SLURM, §Tutorial 1.1, §Tutorial 3.2

- ○ **MD-13.1.A** Write a SLURM script for a GPU CHARMM job with partition, account, time limit, GPU request and memory, and submit or debug it without using the login node.
  - EK: -p free-gpu or gpu; -A rhayes1_lab_gpu on paid partitions only; --time in minutes; --gres=gpu:1 (a GPU partition alone gives no GPU); --mem only after an OOM; srun --pty for interactive debugging; --array=1-4%1 runs chained segments one at a time.
  - P6
- ○ **MD-13.1.B** Estimate GPU-hours and cost for a simulation campaign from throughput in ns/day, and choose free vs paid partitions — numeric rep.
  - EK: GPU-h = 24 × total ns / (ns/day); paid gpu is $0.32 per GPU-hour; free-gpu costs nothing but jobs are preempted (ALF tolerates restarts).
  - P4 · P6

### 13.2 MD engines

Book: orientation §Tutorial 4.2; hayes2021-blade §2, §3; blade-doc §BLaDE

- ○ **MD-13.2.A** Choose an engine — CHARMM standard, DOMDEC, BLaDE, OpenMM — for a described job — choice rep.
  - EK: Standard CHARMM is CPU and slow; DOMDEC GPU is ~5× slower than BLaDE; BLaDE runs MSλD 5–8× faster than DOMDEC; OpenMM is fast for plain MD but does not run λ dynamics within CHARMM.
  - P3 · P6
- ○ **MD-13.2.B** Write BLaDE NVT and NPT dynamics commands and state BLaDE's restrictions.
  - EK: Add 'blade' to ENER/MINI/DYNA; NPT adds 'prmc iprs 100 pref 1 prdv 100'; set friction with 'scalar fbeta set 0.1 sele all end'. Langevin or NVE only, MC barostat only, H-bond constraints only, one GPU per OpenMP thread, no MPI.
  - Needs: MD-4.2.B
  - P6
- ○ **MD-13.2.C** Run an equivalent plain-MD simulation through OpenMM's Python API from CHARMM files.
  - EK: Load PSF + parameter set, build the System with PME and H-bond constraints, LangevinMiddleIntegrator at T, MonteCarloBarostat at 1 bar; CHARMM-GUI can emit OpenMM inputs directly.
  - P6

### 13.3 CHARMM scripting

Book: orientation §Tutorial 1.1, §Tutorial 4.1, §Tutorial 4.3

- ○ **MD-13.3.A** Read and write CHARMM scripts using titles, set/calc, @ and @@ variables, ? system values, stream, if/goto loops, bomlev and stop, and find the right documentation section.
  - EK: Titles start with * and end at a lone *; ! starts comments; CHARMM is case-insensitive but file paths aren't (quote them). Key docs: BLOCK, CONSTRAINTS (SHAKE, restraints), Ewald, nonbonded, CRYSTAL and IMAGE.
  - P6

### 13.4 Reproducibility and data management

Book: livecoms-uq §2; orientation §Tutorial 1.2, §Tutorial 3.4; molssi-mmtools §Git and GitHub

- ○ **MD-13.4.A** Record everything needed to reproduce a run: force-field and engine versions, protonation states, box and ions, seeds, all scripts under version control, and unprocessed data.
  - EK: A result without its inputs and analysis scripts can't be checked; document the full uncertainty procedure too.
  - P6
- ○ **MD-13.4.B** Estimate trajectory storage from atom count, save interval and simulation length — numeric rep.
  - EK: DCD stores single-precision x, y, z: 12 bytes per atom per frame; frames = steps / nsavc.
  - P4 · P6
- ○ **MD-13.4.C** Clean up a finished ALF project, separating disposable intermediates from data that must be kept.
  - EK: run*/output, analysis*/data, Energy, Lambda and slurm logs are disposable; keep alchemical trajectories (run*/res) of published work; spatial DCDs may go after publication.
  - P6

## Unit 14 · Advanced λ dynamics (extension)

Big ideas: ALCH, SAMPLE

### 14.1 Large chemical spaces

Book: alf-readme §Best Practices; orientation §Literature

- ○ **MD-14.1.A** Decide whether intersite coupling biases are needed and set ntersite for flattening and postprocessing.
  - EK: Default [0,0] ignores coupling; with significant coupling use [0,1] in short runflat cycles and [2,1] in postprocess (adjusting only c intersite biases).
  - P3
- ○ **MD-14.1.B** Choose between the histogram estimator and the Potts-model estimator (likelihood vs pseudolikelihood) for a given chemical-space size — choice rep.
  - EK: Histograms need every end state visited (~100–500 states max); Potts keeps one- and two-site terms only; LM below ~10⁶ end states, PLM above.
  - Needs: MD-10.1.C
  - P3
- ○ **MD-14.1.C** Partition a mutation set across sites and systems to respect substituent-per-site limits — choice rep.
  - EK: The ALF README advises ≤ 6 substituents per site (9 the tested ceiling); split larger sets across systems sharing a reference substituent. Newer constraints and biases (2024–2026) extend this to dozens.
  - P1 · P3

### 14.2 Hard perturbations

Book: alf-readme §Best Practices; orientation §Tutorial 1, §Tutorial 3.3, §Literature; livecoms-afe §7.2.2

- ○ **MD-14.2.A** Correct a charge-changing perturbation: explain its PME finite-size errors and apply ALF's discrete solvent correction with the q key.
  - EK: Net-charge changes in a neutral PME box introduce artifacts; the discrete solvent correction is the largest computable term; alternatives include co-alchemical ions.
  - P3 · P5
- ○ **MD-14.2.B** Explain when a site needs replica exchange (e.g. A42, A98, M102 in T4 lysozyme) and how biasing-potential replica exchange helps.
  - EK: Some sites have slow coupled conformational and alchemical barriers; replicas with offset biases exchange to cross them. Replica runs need nreps > 1 and working MPI on the cluster.
  - P3
- ○ **MD-14.2.C** Explain why proline and glycine mutations need a dedicated alchemical strategy.
  - EK: Proline bonds its side chain back to the backbone N and glycine lacks Cβ, so backbone terms (CMAP, ring closure) differ between substituents; Hayes & Brooks 2021 give the workaround.
  - P2
