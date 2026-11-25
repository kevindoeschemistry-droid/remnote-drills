# Computational Protein Design — curriculum framework (draft 1)

Generated from `drills/frameworks/protein-design.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**51 learning objectives** in 10 units (42 core): 51 drilled, 0 partly, 0 with no drills. Core: 42 / 42 drilled.

## Big ideas

- **INVERSE · Design is folding run backwards.** Prediction searches conformations for one sequence; design searches sequences for one conformation. The same energy function and the same samplers serve both.
- **ENERGY · A score is a model, not the truth.** Every number is a weighted sum of approximate terms. A design is only as good as what the function leaves out.
- **SEARCH · The space is too big to enumerate.** Rotamers and sequences grow combinatorially, so everything rests on sampling: Monte Carlo, annealing, pruning or a learned prior.
- **TEST · A design is a hypothesis until it is expressed.** Computational scores rank candidates; folding, stability and function are settled in the laboratory.

## Practices

- **P1 · Compute.** Carry the calculation to a number with units, and say what it does not settle.
- **P2 · Decide.** Choose a representation, protocol or method for a stated problem, and name the failure it avoids.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Protein geometry and the rotamer picture | core | — | 4 | 4 | 0 | 0 |
| 2 · How a structure is represented | core | — | 4 | 4 | 0 | 0 |
| 3 · The all-atom energy function | core | — | 6 | 6 | 0 | 0 |
| 4 · Searching conformations | core | — | 4 | 4 | 0 | 0 |
| 5 · Designing sequence | core | — | 6 | 6 | 0 | 0 |
| 6 · Interfaces, docking and ligands | core | — | 4 | 4 | 0 | 0 |
| 7 · De novo design | core | — | 4 | 4 | 0 | 0 |
| 8 · Deep learning for structure and design | core | — | 6 | 6 | 0 | 0 |
| 9 · Validation and the bridge to simulation | core | — | 4 | 4 | 0 | 0 |
| 10 · Specialised modelling and scale | extension | — | 9 | 9 | 0 | 0 |

## Unit 1 · Protein geometry and the rotamer picture

Big ideas: INVERSE

### 1.1 Backbone and side-chain degrees of freedom



- ● **CPD-1.1.A** (pyrosetta-notebooks:2.4, pyrosetta-notebooks:2.5, jhu-545614:T5) Name the backbone and side-chain dihedrals and say which are free, which are nearly fixed, and which regions of the Ramachandran plot the common secondary structures occupy.
  - EK: φ (C−N−Cα−C), ψ (N−Cα−C−N) and ω (nearly planar, about 180° trans); side-chain χ1, χ2…; right-handed α-helix near φ ≈ −60°, ψ ≈ −45°, β-sheet near φ ≈ −120°, ψ ≈ +130°; glycine is permissive and proline restricted.
  - P2 · drills: cpd-dihedrals, cpd-dihedral-which
- ● **CPD-1.1.B** (pyrosetta-notebooks:2.5) Count the conformational degrees of freedom of a chain and show why enumeration is hopeless.
  - EK: Two free backbone dihedrals per residue; discretising each into a few states gives states^(2n) conformations, which is Levinthal's paradox in numbers.
  - P1 · drills: cpd-levinthal, cpd-levinthal-time

### 1.2 Rotamers



- ● **CPD-1.2.A** (pyrosetta-notebooks:6.1, rosetta-ref15:fa_dun) Explain what a rotamer library is and why side-chain conformations are treated as a discrete, backbone-dependent set.
  - EK: Side-chain χ angles cluster in a few favoured combinations; the Dunbrack library gives their probabilities as a function of φ/ψ, and fa_dun scores the chosen rotamer's internal energy.
  - P2 · drills: cpd-rotamer-lib, cpd-rotamer-apply
- ● **CPD-1.2.B** (pyrosetta-notebooks:6.1) Count the rotamer combinations of a set of designable positions and convert a rotamer probability into an energy.
  - EK: Combinations multiply: Π k_i over positions. A probability p maps to an energy −kT ln p, so a rotamer ten times less likely costs about 1.4 kcal/mol at 298 K.
  - P1 · drills: cpd-rotamer-energy, cpd-rotamer-prob

## Unit 2 · How a structure is represented

Big ideas: INVERSE

### 2.1 The Pose and its numbering



- ● **CPD-2.1.A** (pyrosetta-notebooks:2.1, pyrosetta-notebooks:2.2, pyrosetta-notebooks:2) Describe what a Pose holds and how residues are addressed, and distinguish pose numbering from PDB numbering.
  - EK: A Pose carries the sequence, the conformation as internal coordinates, the fold tree and the energies; pose numbering is 1…N over all residues, while PDB numbering carries chains, gaps and insertion codes.
  - P2 · drills: cpd-pose, cpd-pose-apply
- ● **CPD-2.1.B** (pyrosetta-notebooks:2.1) Convert between pose and PDB numbering across chains of known length.
  - EK: Pose index of residue j in chain c is j plus the lengths of the preceding chains, so gaps in PDB numbering do not shift pose indices.
  - P1 · drills: cpd-pose-index, cpd-pose-reverse

### 2.2 Centroid and full atom



- ● **CPD-2.2.A** (pyrosetta-notebooks:4.2, pyrosetta-notebooks:5.1, kuhlman-bradley:3, pyrosetta-notebooks:2) Contrast the centroid and full-atom representations and say which stage of a protocol uses each.
  - EK: Centroid replaces each side chain with one pseudo-atom and a simple score for fast global search; full atom restores every atom for local refinement and final ranking. Multi-resolution modelling is the standard pattern.
  - P2 · drills: cpd-centroid, cpd-resolution-pick
- ● **CPD-2.2.B** (pyrosetta-notebooks:4.2) Compute how many atoms a representation tracks and the speed-up a coarse-grained model buys.
  - EK: Pairwise interaction work scales with the square of the number of interacting centres, so a fourfold cut in centres is about a sixteenfold cut in pair work.
  - P1 · drills: cpd-centroid-speedup, cpd-atom-count

## Unit 3 · The all-atom energy function

Big ideas: ENERGY

### 3.1 Terms and weights



- ● **CPD-3.1.A** (rosetta-ref15:form, rosetta-ref15:table, jhu-545614:T5, pyrosetta-notebooks:3) Name the main energy terms and classify each as physics-based or knowledge-based.
  - EK: Physics-based: fa_atr and fa_rep (Lennard-Jones split at its minimum), fa_sol (Lazaridis–Karplus desolvation), lk_ball_wtd (anisotropic polar solvation), fa_elec (distance-dependent dielectric). Knowledge-based: fa_dun (rotamer), rama_prepro (backbone φ/ψ), p_aa_pp (residue given φ/ψ), the hydrogen-bond and disulfide terms fit to structures.
  - P2 · drills: cpd-terms, cpd-term-diagnose
- ● **CPD-3.1.B** (rosetta-ref15:form, rosetta-ref15:table) Compute a total score as the weighted sum of its terms.
  - EK: Total = Σ w_i E_i. Physics-based terms carry weight 1.0; fa_rep is 0.55, fa_dun 0.7, rama_prepro 0.45, p_aa_pp 0.4, omega 0.6, dslf_fa13 1.25, fa_intra_rep 0.005.
  - P1 · drills: cpd-weighted-score, cpd-weight-change

### 3.2 Reference energies and design



- ● **CPD-3.2.A** (rosetta-ref15:ref) Explain what the reference energy does and why design, not scoring, needs it.
  - EK: ref adds a constant per amino-acid type standing for the unfolded state, fitted to maximise native sequence recovery. For a fixed sequence it is a constant offset; when sequences are compared it removes the composition bias the other terms would impose.
  - P2 · drills: cpd-ref, cpd-ref-apply
- ● **CPD-3.2.B** (rosetta-ref15:ref, rosetta-ref15:units) Compute a stability difference between two candidate sequences including their reference energies.
  - EK: ΔΔG ≈ (E_folded − Σ ref) for one sequence minus the same for the other; a design that scores better only because of composition bias loses that advantage once ref is included.
  - P1 · drills: cpd-ref-compare, cpd-ddg-mutation

### 3.3 Reading an energy



- ● **CPD-3.3.A** (rosetta-ref15:units, rosetta-ref15:guidance) State what the energy's units mean and how far to trust a computed ΔΔG.
  - EK: The current function is parameterised in kcal/mol rather than arbitrary Rosetta Energy Units, but the paper's own worked mutation gave −4.95 kcal/mol against −1.11 kcal/mol measured: the sign and the ranking are more reliable than the magnitude.
  - P2 · drills: cpd-units, cpd-trust-score
- ● **CPD-3.3.B** (rosetta-ref15:guidance) Decompose a score change into terms and name the interaction responsible.
  - EK: Subtract term by term between two states; per-residue and atom-pair tables locate the contact that changed. A buried polar group shows up in solvation, a clash in fa_rep.
  - P1 · drills: cpd-term-decompose, cpd-per-residue

## Unit 4 · Searching conformations

Big ideas: SEARCH

### 4.1 Monte Carlo and annealing



- ● **CPD-4.1.A** (kuhlman-bradley:2, pyrosetta-notebooks:4.1, jhu-545614:T5) State the Metropolis rule and explain why uphill moves are accepted at all.
  - EK: A move raising the score by ΔE is accepted with probability exp(−ΔE/kT); uphill steps let the search leave local minima, which gradient descent cannot do.
  - P2 · drills: cpd-metropolis, cpd-mc-apply
- ● **CPD-4.1.B** (pyrosetta-notebooks:4.1) Compute a Metropolis acceptance probability and show how annealing changes it.
  - EK: P = exp(−ΔE/kT) for ΔE > 0, P = 1 otherwise; lowering the temperature during a run makes the same uphill move far less likely, which is simulated annealing.
  - P1 · drills: cpd-accept-ratio, cpd-metropolis-de

### 4.2 Packing and minimisation



- ● **CPD-4.2.A** (pyrosetta-notebooks:6.2, jhu-545614:T1) Describe what the packer does, and how packing, minimisation and relax differ.
  - EK: The packer runs simulated annealing over discrete rotamers at the positions a task allows; minimisation moves continuous degrees of freedom downhill; relax alternates the two so a structure settles without drifting far.
  - P2 · drills: cpd-packer, cpd-protocol-order
- ● **CPD-4.2.B** (pyrosetta-notebooks:6.2, kuhlman-bradley:5) Count the entries of a rotamer pair-energy table and explain the cost of precomputing it.
  - EK: With n positions and k rotamers each, there are n·k one-body terms and k² entries for each of the n(n−1)/2 position pairs, so the table grows as the square of both.
  - P1 · drills: cpd-pair-table, cpd-pair-table-growth

## Unit 5 · Designing sequence

Big ideas: INVERSE, SEARCH

### 5.1 Specifying what may change



- ● **CPD-5.1.A** (pyrosetta-notebooks:6.3, pyrosetta-notebooks:6.4) Read and write a design specification: which positions repack, which design, and to what alphabet.
  - EK: A resfile or task operation sets per-position behaviour — repack only, design to all residues, or design to a restricted set; everything else stays fixed. Getting this wrong is the usual cause of a nonsense design.
  - P2 · drills: cpd-resfile, cpd-task-scenario
- ● **CPD-5.1.B** (pyrosetta-notebooks:6.3) Count the sequence space a design specification opens.
  - EK: Π a_i over designable positions, where a_i is the alphabet allowed at position i; 20^n for unrestricted design, which is why the space is sampled and never enumerated.
  - P1 · drills: cpd-seq-space, cpd-alphabet-cut

### 5.2 Mutational scans



- ● **CPD-5.2.A** (pyrosetta-notebooks:6.8, rosetta-ref15:guidance) Plan a point-mutation scan and read its output.
  - EK: A saturation scan tries 19 substitutions at each chosen position, scoring each after local repacking; the result is a ranked ΔΔG list, not a verdict.
  - P2 · drills: cpd-scan, cpd-scan-read
- ● **CPD-5.2.B** (pyrosetta-notebooks:6.8) Count the jobs and compute the ΔΔG values a scan produces.
  - EK: 19 substitutions per position times the positions, times the independent trials each is run with; ΔΔG = E_mutant − E_wild-type, with a positive value destabilising.
  - P1 · drills: cpd-scan-jobs, cpd-scan-positions

### 5.3 Judging a design protocol



- ● **CPD-5.3.B** (kuhlman-bradley:5) Match a sequence-optimisation method to its guarantee: dead-end elimination, mean field, annealing, genetic algorithms.
  - EK: Dead-end elimination prunes provably non-optimal rotamers and can return the true optimum; annealing and genetic algorithms are stochastic and return good solutions without a proof.
  - P2 · drills: cpd-search-methods, cpd-method-pick
- ● **CPD-5.3.A** (rosetta-ref15:ref, kuhlman-bradley:5) Use native sequence recovery to judge an energy function or protocol.
  - EK: Redesign a natural protein's positions and count how often the native residue comes back; random choice recovers about 5%, buried positions recover best, and surface positions worst.
  - P1 · drills: cpd-recovery, cpd-recovery-compare

## Unit 6 · Interfaces, docking and ligands

Big ideas: ENERGY

### 6.1 Docking and interface scoring



- ● **CPD-6.1.A** (pyrosetta-notebooks:7.1, pyrosetta-notebooks:7.2, jhu-545614:T1) Describe the two stages of docking and what a funnel plot shows.
  - EK: A global rigid-body search (often Fourier-based) is followed by local high-resolution refinement; plotting score against RMSD to a reference should funnel toward low RMSD if the function discriminates.
  - P2 · drills: cpd-docking, cpd-docking-read
- ● **CPD-6.1.B** (pyrosetta-notebooks:7.2, rosetta-ref15:guidance, pyrosetta-notebooks:8.2) Compute a binding or interface energy from component scores.
  - EK: ΔE_interface = E_complex − E_partner A alone − E_partner B alone, each scored in the same function; near-native models gain in van der Waals, electrostatics and side-chain hydrogen bonds.
  - P1 · drills: cpd-interface-energy, cpd-interface-reverse

### 6.2 Designing a binding site



- ● **CPD-6.2.A** (pyrosetta-notebooks:8.1, kuhlman-bradley:5, jhu-545614:T2) Lay out how a ligand-binding pocket is designed and why designed enzymes fall short of natural ones.
  - EK: Place the ligand, design the shell around it, then repack and minimise. Pocket shape and binding are achievable; transition-state stabilisation, and so catalytic efficiency, is not yet.
  - P2 · drills: cpd-ligand, cpd-pocket-scenario
- ● **CPD-6.2.B** (kuhlman-bradley:5, jhu-545614:T4) Choose one-sided or two-sided interface design for a stated problem and say what makes it hard.
  - EK: Two-sided design redesigns both partners and is easier; a binder against a fixed natural surface is one-sided and much harder, which is also why antibody design remains difficult.
  - P2 · drills: cpd-interface-design, cpd-interface-scenario

## Unit 7 · De novo design

Big ideas: INVERSE, SEARCH

### 7.1 Building a backbone from nothing



- ● **CPD-7.1.A** (pyrosetta-notebooks:6.6, pyrosetta-notebooks:6.7, kuhlman-bradley:5, jhu-545614:T3) Contrast the routes to a de novo backbone: fragment assembly, distance constraints and parametric equations.
  - EK: Fragments splice pieces of known structures; constraints specify the contacts wanted; parametric equations generate ideal folds such as coiled coils and β-barrels from a handful of numbers.
  - P2 · drills: cpd-denovo-backbone, cpd-backbone-pick
- ● **CPD-7.1.B** (pyrosetta-notebooks:6.6) Compute the geometry of a parametric helical bundle from its parameters.
  - EK: A coiled-coil's superhelical radius, pitch and the number of residues per repeat fix the backbone; the rise along the axis per residue follows from the pitch and the residues per turn.
  - P1 · drills: cpd-coiled-coil, cpd-coiled-coil-length

### 7.2 Hard cases



- ● **CPD-7.2.A** (pyrosetta-notebooks:6.5, kuhlman-bradley:5, jhu-545614:T3) Say why buried hydrogen-bond networks are designed before the rest of the sequence.
  - EK: A network of buried polar residues is rare and easily broken by later repacking, so it is found first and then held fixed while the surrounding core is designed.
  - P2 · drills: cpd-hbnet, cpd-hbnet-scenario
- ● **CPD-7.2.B** (kuhlman-bradley:5) Explain negative and multi-state design and compute the energy gap that must be opened.
  - EK: Favour the target state by scoring it against competing states and maximising the gap; a conformational switch is a multi-state design where each state's gap is tuned, and a gap of a few kT sets the population ratio.
  - P1 · drills: cpd-gap-population, cpd-gap-needed

## Unit 8 · Deep learning for structure and design

Big ideas: SEARCH

### 8.1 Structure prediction and its confidence



- ● **CPD-8.1.A** (dl4proteins:WS06) Name the inputs a modern structure predictor takes and read its confidence metrics.
  - EK: Sequence, a multiple-sequence alignment and optional templates go in; pLDDT scores per-residue local confidence (higher is better, with roughly 70 and 90 as useful marks) and PAE scores the expected error between residue pairs, which is what judges domain placement.
  - P2 · drills: cpd-predictor-inputs, cpd-confidence-scenario
- ● **CPD-8.1.B** (kuhlman-bradley:4, dl4proteins:WS06) Explain why alignment depth limits prediction and coevolution-based contacts.
  - EK: Coevolution separates direct couplings from indirect ones only when the alignment is deep; shallow families, including many eukaryote-specific ones, lose that signal, and MSA coverage plots are read for exactly this.
  - P2 · drills: cpd-coevolution, cpd-msa-scenario

### 8.2 Learned representations and generators



- ● **CPD-8.2.A** (dl4proteins:WS04, dl4proteins:WS05, dl4proteins:WS07) Match a representation to its architecture: sequence tokens for language models, residue or atom graphs for message passing.
  - EK: A protein language model is trained on sequences alone and its embeddings transfer to downstream tasks; a graph network passes messages between residues or atoms, where invariance and equivariance to rotation matter.
  - P2 · drills: cpd-representations, cpd-representation-pick
- ● **CPD-8.2.B** (dl4proteins:WS08, dl4proteins:WS09, dl4proteins:WS10) Describe the diffusion design pipeline and what each stage contributes.
  - EK: A diffusion model denoises a backbone (unconditionally, scaffolding a motif, or against a target), an inverse-folding model assigns a sequence to that backbone, and a structure predictor checks that the sequence folds back to it.
  - P2 · drills: cpd-diffusion-pipeline, cpd-pipeline-order

### 8.3 Using a pipeline honestly



- ● **CPD-8.3.B** (dl4proteins:WS09, kuhlman-bradley:6) Say what a self-consistency check does and does not establish.
  - EK: Designing a sequence for a backbone and recovering that backbone from the sequence shows the two models agree; it is not experimental evidence, since both may share the same blind spots.
  - P2 · drills: cpd-self-consistency, cpd-evidence-level
- ● **CPD-8.3.A** (dl4proteins:WS09) Compute the yield of a filtered design funnel.
  - EK: Multiply the pass fractions of the stages: backbones generated, sequences per backbone, and the fraction whose predicted structure falls within the RMSD and confidence cut-offs.
  - P1 · drills: cpd-funnel-yield, cpd-funnel-reverse

## Unit 9 · Validation and the bridge to simulation

Big ideas: TEST, ENERGY

### 9.1 Testing designs



- ● **CPD-9.1.A** (kuhlman-bradley:6) Plan the experiments that test a design and say how many candidates to make.
  - EK: Expression and solubility, then thermal or chemical denaturation for stability, oligomeric state, a high-resolution structure, and a function assay. A stabilisation project may test a handful; a new binder may need thousands, screened by display and sequencing.
  - P2 · drills: cpd-experiments, cpd-experiment-order
- ● **CPD-9.1.B** (kuhlman-bradley:6) Compute the number of designs to order for a target number of successes at an expected hit rate.
  - EK: Expected successes = N × hit rate, so N = target/hit rate; low rates are why display libraries, not individual clones, are used for binders.
  - P1 · drills: cpd-designs-needed, cpd-hit-rate

### 9.2 Where a score is not enough



- ● **CPD-9.2.A** (pyrosetta-notebooks:15.2, rosetta-ref15:guidance) Decide when a score-function ΔΔG is enough and when an alchemical free-energy calculation is warranted.
  - EK: A score-function scan ranks many mutations cheaply and is right about signs more often than magnitudes; when a few candidates must be quantitative, or when a result must survive review, λ dynamics or another alchemical method gives a statistical-mechanics estimate with an error bar.
  - P2 · drills: cpd-score-vs-alchemical, cpd-method-choice-scenario
- ● **CPD-9.2.B** (kuhlman-bradley:7) Name what current energy functions handle worst and relate it to a failed design.
  - EK: Balancing polar against nonpolar energetics, solvation, flexible loops and backbone flexibility are the open problems; a design that expresses but is unstructured usually points at one of them.
  - P2 · drills: cpd-open-problems, cpd-failure-diagnose

## Unit 10 · Specialised modelling and scale (extension)

Big ideas: SEARCH, TEST

### 10.1 Loops, symmetry and density



- ● **CPD-10.1.C** (pyrosetta-notebooks:11) Say what fitting a model into electron density adds to a purely computational score, and what it cannot fix.
  - EK: Density is experimental evidence that restrains the model, scored alongside the energy function; it cannot rescue a region the map does not resolve, where confidence stays low whatever the score says.
  - P2 · drills: cpd-density, cpd-density-2
- ● **CPD-10.1.D** (pyrosetta-notebooks:5.2) Order the stages of a refinement protocol and say what each stage is allowed to move.
  - EK: Refinement alternates small backbone perturbations, side-chain repacking and minimisation under the all-atom function, usually with the repulsive weight ramped, so the structure settles without escaping the starting fold.
  - P2 · drills: cpd-refine-stages, cpd-refine-diagnose
- ● **CPD-10.1.A** (pyrosetta-notebooks:9.1, kuhlman-bradley:5) Say what a loop-closure method must guarantee and why loops are modelled separately from the rest of a structure.
  - EK: A rebuilt loop must still join the fixed flanking residues, so closure is a constraint, not a preference; kinematic closure solves for the dihedrals that close the gap, and loops are irregular and flexible, which is why they are rebuilt rather than threaded.
  - P2 · drills: cpd-loop-closure, cpd-loop-dof
- ● **CPD-10.1.B** (pyrosetta-notebooks:10) Describe what a symmetric model fixes and count the independent degrees of freedom symmetry removes.
  - EK: One asymmetric unit plus a symmetry definition generates the rest, so the energy and the moves apply to the unit and are replicated; n copies of an m-residue chain under exact symmetry leave one chain's degrees of freedom instead of n.
  - P2 · drills: cpd-symmetry, cpd-symmetry-dof

### 10.2 Antibodies and membrane proteins



- ● **CPD-10.2.B** (pyrosetta-notebooks:12.2, kuhlman-bradley:5) Say what antibody design optimises and why it is a one-sided problem.
  - EK: Design chooses CDR sequence and length against a chosen epitope on a target that cannot be changed, so it combines one-sided interface design with flexible-loop modelling: the two hardest cases in the field at once.
  - P2 · drills: cpd-antibody-design, cpd-antibody-design-2
- ● **CPD-10.2.A** (pyrosetta-notebooks:12.1, kuhlman-bradley:5) Describe how an antibody structure is modelled from its framework and loops, and which loop is the hard one.
  - EK: The variable domains' frameworks are conserved enough to graft from templates by canonical class; the six complementarity-determining loops are modelled on top, and CDR H3 is the longest, most variable and least predictable.
  - P2 · drills: cpd-antibody-model, cpd-cdr-count
- ● **CPD-10.2.C** (pyrosetta-notebooks:15.1) Set up a membrane protein in a bilayer and say what the energy function must change.
  - EK: The protein is embedded with its hydrophobic span across the membrane and its orientation and depth fixed relative to the bilayer; the solvation term must treat the membrane interior as nonpolar, so a water-based function would misscore buried polar residues.
  - P2 · drills: cpd-membrane, cpd-tm-span

### 10.3 Running at scale, reproducibly



- ● **CPD-10.3.A** (pyrosetta-notebooks:16) Distinguish the three ways a design campaign is parallelised and match each to its job.
  - EK: Independent decoys of one protocol (embarrassingly parallel), one protocol distributed across workers, and many protocols over many inputs; a scan is the first, a large generative pipeline the third.
  - P2 · drills: cpd-parallel-kind, cpd-parallel-time
- ● **CPD-10.3.B** (pyrosetta-notebooks:16) State what a run must record for a design to be reproducible, and compute the decoy count a campaign needs.
  - EK: The random seed, the protocol version, the input structure and every option, kept with the output; decoys scale as inputs × protocols × decoys per input, and the lowest-scoring decoy of too small a set is just noise.
  - P2 · drills: cpd-decoys, cpd-reproducible
