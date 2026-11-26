# Biochemistry — curriculum framework (draft 1)

Generated from `drills/frameworks/biochemistry.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**49 learning objectives** in 11 units (49 core): 49 drilled, 0 partly, 0 with no drills. Core: 49 / 49 drilled.

## Big ideas

- **ENERGY · Energy is required and transformed.** Free energy, coupling and catalysis decide which processes run and how fast.
- **STRUCTURE · Structure determines function.** Folding and binding energetics set what a macromolecule does.
- **INFORMATION · Information is stored and flows.** Sequence encodes structure; replication, transcription and translation move it.
- **REGULATION · Homeostasis is regulated and far from equilibrium.** Control points, signals and steady states keep cells running.
- **MEASURE · Discovery requires measurement.** Quantitative methods turn molecules into numbers.

## Practices

- **P1 · Compute.** Carry the calculation to a number with units.
- **P2 · Reason.** Predict or explain an outcome from structure, energetics or regulation.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Water, pH and ionisable groups | core | — | 4 | 4 | 0 | 0 |
| 2 · Protein structure and folding | core | — | 6 | 6 | 0 | 0 |
| 3 · Binding, cooperativity and allostery | core | — | 4 | 4 | 0 | 0 |
| 4 · Enzymes | core | — | 7 | 7 | 0 | 0 |
| 5 · Bioenergetics | core | — | 4 | 4 | 0 | 0 |
| 6 · Membranes and transport | core | — | 3 | 3 | 0 | 0 |
| 7 · Metabolism | core | — | 6 | 6 | 0 | 0 |
| 8 · Nucleic acids and information flow | core | — | 6 | 6 | 0 | 0 |
| 9 · Signalling and regulation | core | — | 2 | 2 | 0 | 0 |
| 10 · Methods in biochemistry | core | — | 4 | 4 | 0 | 0 |
| 11 · Evolution and homeostasis | core | — | 3 | 3 | 0 | 0 |

## Unit 1 · Water, pH and ionisable groups

Big ideas: ENERGY

### 1.1 Buffers and protonation



- ● **BC-1.1.A** (asbmb-core-2013:3.1, asbmb-core-2013:3.3, fe-chemical:5.D) Compute buffer pH or the base:acid ratio of a biological buffer with the Henderson–Hasselbalch equation.
  - EK: pH = pKa + log([A⁻]/[HA]); phosphate (pKa 6.86) and bicarbonate (6.1) buffer cells and blood.
  - P1 · drills: bc-hh-ph, bc-blood-ratio
- ● **BC-1.1.B** (asbmb-core-2013:3.1) Compute the fraction of an ionisable side chain protonated at a given pH.
  - EK: f(HA) = 1/(1 + 10^(pH − pKa)); His (pKa ≈ 6.0) switches near physiological pH.
  - P1 · drills: bc-fraction-protonated, bc-shifted-pka

### 1.2 Amino-acid and peptide charge



- ● **BC-1.2.A** (aamc-mcat-outline:1A) Find the isoelectric point of an amino acid from its pKa values.
  - EK: pI = average of the two pKa values flanking the neutral species.
  - P1 · drills: bc-pi, bc-pi-glycine
- ● **BC-1.2.B** (aamc-mcat-outline:1A, asbmb-core-2013:5.2) Compute the net charge of a peptide at a given pH from its ionisable groups.
  - EK: Sum fractional charges: +1/(1 + 10^(pH − pKa)) for basic groups, −1/(1 + 10^(pKa − pH)) for acidic ones.
  - P1 · drills: bc-peptide-charge, bc-charge-direction

## Unit 2 · Protein structure and folding

Big ideas: STRUCTURE, ENERGY

### 2.1 Levels of structure



- ● **BC-2.1.A** (asbmb-cert:2.1, asbmb-core-2013:5.1) Relate secondary-structure geometry to length: residues per turn and rise per residue.
  - EK: α-helix: 3.6 residues/turn, 1.5 Å rise per residue (5.4 Å pitch); β-strand: about 3.3–3.5 Å per residue.
  - P1 · drills: bc-helix-length, bc-helix-turns
- ● **BC-2.1.B** (asbmb-cert:2.3, asbmb-core-2013:5.2) Identify the interactions that stabilise a structure and predict the effect of a substitution.
  - EK: Hydrophobic burial, hydrogen bonds, salt bridges, disulfides; Pro breaks helices, Gly adds flexibility.
  - P2 · drills: bc-interactions, bc-structure-levels

### 2.2 Folding thermodynamics



- ● **BC-2.2.A** (asbmb-core-2013:5.2, asbmb-cert:1.3, asbmb-core-2013:5.5) Compute ΔG of folding, the melting temperature and the fraction folded for a two-state protein.
  - EK: ΔG_unf = ΔH(1 − T/Tm) (ΔCp neglected); K_fold = e^(−ΔG_fold/RT); f_folded = K/(1 + K).
  - P1 · drills: bc-fold-fraction, bc-fold-dg
- ● **BC-2.2.B** (asbmb-core-2013:5.2, asbmb-cert:2.3) Convert a mutation's ΔΔG into a change in stability, folding equilibrium constant or fraction unfolded.
  - EK: ΔΔG > 0 destabilises; each 5.7 kJ/mol at 298 K is a factor of 10 in K.
  - P1 · drills: bc-ddg-fraction, bc-ddg-k-factor
- ● **BC-2.2.C** (asbmb-cert:1.3, asbmb-core-2013:5.2, asbmb-core-2013:5.5) Explain the hydrophobic effect and why folding is not a random search.
  - EK: Burying nonpolar groups releases ordered water (entropy gain); Levinthal: a random search would take astronomically long, so folding follows a funnel.
  - P2 · drills: bc-hydrophobic, bc-levinthal
- ● **BC-2.2.D** (asbmb-core-2013:5.6) Recognise intrinsically disordered proteins from their composition and say how they still function.
  - EK: Few hydrophobic residues and high net charge keep a chain unfolded; disordered regions bind by folding on contact, often to many partners, and are common in signalling.
  - P1 · drills: bc-idp-facts, bc-idp-charge

## Unit 3 · Binding, cooperativity and allostery

Big ideas: STRUCTURE

### 3.1 Affinity



- ● **BC-3.1.A** (asbmb-core-2013:5.3, asbmb-core-2013:5.4) Compute fractional saturation and the binding free energy from K_d.
  - EK: θ = [L]/(K_d + [L]); ΔG°_bind = RT ln K_d (with K_d in M).
  - P1 · drills: bc-theta, bc-dg-bind
- ● **BC-3.1.B** (asbmb-core-2013:5.3, asbmb-core-2013:5.4) Compute the ΔΔG of binding between two variants from their K_d values.
  - EK: ΔΔG = RT ln(K_d,mut/K_d,wt); a 10-fold loss is +5.7 kJ/mol at 298 K.
  - P1 · drills: bc-ddg-bind, bc-kd-from-ddg

### 3.2 Cooperativity and allostery



- ● **BC-3.2.A** (asbmb-core-2013:5.7, asbmb-core-2013:5.4) Use the Hill equation and read cooperativity from n_H.
  - EK: θ = Lⁿ/(K₀.₅ⁿ + Lⁿ); going from 10% to 90% saturation needs an 81^(1/n)-fold change in [L].
  - P1 · drills: bc-hill-theta, bc-hill-range
- ● **BC-3.2.B** (asbmb-core-2013:5.7, asbmb-cert:1.1) Explain haemoglobin's cooperativity and its regulation by H⁺, CO₂ and 2,3-BPG.
  - EK: T and R states; the Bohr effect and BPG stabilise T, lowering affinity to unload O₂ in tissues; myoglobin binds hyperbolically.
  - P2 · drills: bc-hemoglobin, bc-allostery-models

## Unit 4 · Enzymes

Big ideas: ENERGY

### 4.1 Michaelis–Menten kinetics



- ● **BC-4.1.A** (asbmb-core-2013:2.2, asbmb-cert:2.4, acs-accm-analytical:VII.E.1, fe-chemical:5.D) Compute an initial rate from V_max, K_M and [S].
  - EK: v = V_max[S]/(K_M + [S]); v = V_max/2 at [S] = K_M.
  - P1 · drills: bc-mm-rate, bc-mm-s-for-v
- ● **BC-4.1.B** (asbmb-core-2013:2.2) Compute k_cat and catalytic efficiency and compare with the diffusion limit.
  - EK: k_cat = V_max/[E]_T; k_cat/K_M approaches 10⁸–10⁹ M⁻¹ s⁻¹ for diffusion-limited enzymes.
  - P1 · drills: bc-kcat, bc-efficiency
- ● **BC-4.1.C** (asbmb-core-2013:2.2, asbmb-cert:2.4, acs-accm-analytical:X.A.2) Read K_M and V_max from a Lineweaver–Burk plot.
  - EK: 1/v = (K_M/V_max)(1/[S]) + 1/V_max: y-intercept 1/V_max, x-intercept −1/K_M.
  - P1 · drills: bc-lb-km, bc-lb-vmax

### 4.2 Inhibition



- ● **BC-4.2.A** (asbmb-cert:2.4) Compute apparent K_M and V_max for competitive, uncompetitive and mixed inhibition.
  - EK: α = 1 + [I]/K_I: competitive K_M,app = αK_M; uncompetitive divides both K_M and V_max by α′; mixed scales both.
  - P1 · drills: bc-competitive, bc-uncompetitive
- ● **BC-4.2.B** (asbmb-cert:2.4) Convert an IC₅₀ to K_I for a competitive inhibitor and classify inhibition from data.
  - EK: Cheng–Prusoff: K_I = IC₅₀/(1 + [S]/K_M).
  - P1 · drills: bc-cheng-prusoff, bc-inhibition-pattern

### 4.3 Catalytic mechanisms



- ● **BC-4.3.A** (asbmb-cert:1.5) Relate transition-state stabilisation to rate enhancement, separating it from ΔG of the reaction.
  - EK: Enzymes lower ΔG‡, not ΔG; rate enhancement = e^(ΔΔG‡/RT).
  - P1 · drills: bc-rate-enhancement, bc-catalysis-thermo
- ● **BC-4.3.B** (asbmb-cert:2.4) Identify catalytic strategies (acid–base, covalent, metal ion, proximity) in a described mechanism.
  - EK: Serine proteases: Ser–His–Asp triad, covalent acyl-enzyme, oxyanion hole stabilises the tetrahedral intermediate.
  - P2 · drills: bc-catalytic-strategies, bc-catalytic-strategies-2

## Unit 5 · Bioenergetics

Big ideas: ENERGY

### 5.1 Free energy in the cell



- ● **BC-5.1.A** (asbmb-core-2013:2.3) Compute ΔG of ATP hydrolysis at cellular concentrations from ΔG°′ and the mass-action ratio.
  - EK: ΔG = ΔG°′ + RT ln([ADP][Pi]/[ATP]); ΔG°′ = −30.5 kJ/mol, cellular ΔG about −50 to −60.
  - P1 · drills: bc-atp-dg, bc-atp-ratio-needed
- ● **BC-5.1.B** (asbmb-core-2013:2.4, asbmb-cert:1.4) Find the overall ΔG°′ and K′ of a coupled reaction.
  - EK: ΔG°′ values add; K′ = e^(−ΔG°′/RT) multiplies.
  - P1 · drills: bc-coupled-dg, bc-coupling-k

### 5.2 Redox and chemiosmosis



- ● **BC-5.2.A** (asbmb-core-2013:2.3, asbmb-core-2013:2.1) Compute ΔG°′ of an electron transfer from standard reduction potentials.
  - EK: ΔG°′ = −nFΔE°′; NADH → O₂ (ΔE°′ = 1.14 V) releases about 220 kJ/mol.
  - P1 · drills: bc-redox-dg, bc-redox-atp
- ● **BC-5.2.B** (asbmb-core-2013:3.2, asbmb-core-2013:2.1) Compute the proton-motive force and the free energy per proton moved into the matrix.
  - EK: Δp = Δψ − (2.303RT/F)ΔpH (pH_in − pH_out); ΔG per H⁺ = −FΔp.
  - P1 · drills: bc-pmf, bc-pmf-dg

## Unit 6 · Membranes and transport

Big ideas: ENERGY, STRUCTURE

### 6.1 Transport energetics



- ● **BC-6.1.A** (asbmb-core-2013:2.1, fe-chemical:5.D) Compute the Nernst equilibrium potential of an ion.
  - EK: E = (RT/zF) ln([out]/[in]); about 61.5/z mV per decade at 37 °C.
  - P1 · drills: bc-nernst, bc-nernst-ratio
- ● **BC-6.1.B** (asbmb-core-2013:3.2, asbmb-core-2013:2.1) Compute the free energy of moving a charged solute across a membrane.
  - EK: ΔG = RT ln(c_in/c_out) + zFΔψ (Δψ = ψ_in − ψ_out).
  - P1 · drills: bc-transport-dg, bc-glucose-gradient
- ● **BC-6.1.C** (asbmb-cert:2.1) Distinguish channels, carriers and pumps, and predict how lipid composition changes fluidity.
  - EK: Unsaturated and shorter chains raise fluidity; cholesterol buffers it; pumps use ATP, secondary transporters use gradients.
  - P2 · drills: bc-membranes, bc-membranes-2

## Unit 7 · Metabolism

Big ideas: ENERGY, REGULATION

### 7.1 Glycolysis and gluconeogenesis



- ● **BC-7.1.A** (asbmb-cert:1.1, asbmb-core-2013:3.4) Account for the ATP and NADH of glycolysis and name its control points.
  - EK: Net 2 ATP and 2 NADH per glucose; hexokinase, PFK-1 (the committed step) and pyruvate kinase are irreversible and regulated.
  - P1 · drills: bc-glycolysis-atp, bc-glycolysis-control
- ● **BC-7.1.B** (asbmb-cert:1.1, asbmb-cert:1.2, asbmb-core-2013:3.4) Explain how gluconeogenesis bypasses glycolysis's irreversible steps and what it costs.
  - EK: Pyruvate carboxylase + PEPCK, fructose-1,6-bisphosphatase, glucose-6-phosphatase; 4 ATP + 2 GTP + 2 NADH per glucose.
  - P2 · drills: bc-gluconeogenesis, bc-gng-cost

### 7.2 Oxidative metabolism



- ● **BC-7.2.A** (asbmb-core-2013:2.3) Compute the ATP yield of complete glucose oxidation from P/O ratios.
  - EK: 10 NADH and 2 FADH₂ per glucose (with the shuttle); 2.5 ATP/NADH and 1.5 ATP/FADH₂ give about 30–32 ATP.
  - P1 · drills: bc-glucose-atp, bc-tca
- ● **BC-7.2.B** (asbmb-cert:1.2) Compute the ATP yield of β-oxidation of a saturated fatty acid.
  - EK: C_n: n/2 − 1 rounds (each FADH₂ + NADH), n/2 acetyl-CoA (10 ATP each), minus 2 for activation; palmitate gives 106.
  - P1 · drills: bc-beta-ox, bc-beta-rounds

### 7.3 Regulation and nitrogen



- ● **BC-7.3.A** (asbmb-core-2013:3.5, asbmb-cert:1.1, asbmb-core-2013:3.6) Predict how insulin, glucagon and allosteric effectors regulate fuel metabolism.
  - EK: Insulin: storage (glycogen synthesis, glycolysis); glucagon: mobilisation via cAMP/PKA; F2,6BP couples hormone state to PFK-1.
  - P2 · drills: bc-hormones, bc-regulation-levels
- ● **BC-7.3.B** (asbmb-core-2013:3.4) Account for the cost and logic of nitrogen disposal through the urea cycle.
  - EK: Urea carries two N (one from NH₄⁺ via carbamoyl phosphate, one from aspartate); 4 high-energy phosphate bonds per urea.
  - P2 · drills: bc-urea-cost, bc-urea

## Unit 8 · Nucleic acids and information flow

Big ideas: INFORMATION

### 8.1 DNA structure



- ● **BC-8.1.A** (asbmb-core-2013:4.2, asbmb-core-2013:4.1) Use Chargaff's rules to find base composition.
  - EK: In double-stranded DNA, A = T and G = C, so %G = (100 − 2·%A)/2.
  - P1 · drills: bc-chargaff, bc-gc-content
- ● **BC-8.1.B** (asbmb-core-2013:4.2) Estimate a short duplex's melting temperature and say why GC content raises it.
  - EK: Wallace rule for short oligos: Tm ≈ 2(A + T) + 4(G + C) °C; GC pairs stack more strongly (and have three H-bonds).
  - P1 · drills: bc-wallace, bc-dna-tm

### 8.2 Mutation and fidelity



- ● **BC-8.2.A** (asbmb-cert:3.1, asbmb-core-2013:1.5) Predict a mutation's effect on the protein: silent, missense, nonsense or frameshift.
  - EK: An insertion or deletion that is not a multiple of 3 shifts the reading frame downstream.
  - P2 · drills: bc-frameshift, bc-mutation-type
- ● **BC-8.2.B** (asbmb-core-2013:4.4) Compute the expected number of replication errors per genome from the error rate.
  - EK: Errors = genome length × error rate per base; proofreading and mismatch repair bring E. coli to ~10⁻¹⁰ per base.
  - P1 · drills: bc-replication-errors, bc-fidelity

### 8.3 Expression and its measurement



- ● **BC-8.3.A** (asbmb-cert:3.2, asbmb-cert:3.3, asbmb-core-2013:4.2) Predict gene-expression changes from regulatory logic (lac operon, activators, repressors).
  - EK: lac is expressed when lactose is present (repressor off) and glucose is low (cAMP–CAP on).
  - P2 · drills: bc-lac-operon, bc-eukaryote-expression
- ● **BC-8.3.B** (asbmb-core-2013:4.3) Compute PCR amplification and a qPCR fold change by the ΔΔCt method.
  - EK: Copies = N₀·2ⁿ at full efficiency; fold change = 2^(−ΔΔCt).
  - P1 · drills: bc-pcr, bc-ddct

## Unit 9 · Signalling and regulation

Big ideas: REGULATION

### 9.1 Signal transduction



- ● **BC-9.1.A** (asbmb-cert:3.5) Compute the amplification of a signalling cascade.
  - EK: Gains multiply: each enzyme in a cascade activates many of the next.
  - P1 · drills: bc-cascade, bc-signal-termination
- ● **BC-9.1.B** (asbmb-cert:3.5) Match a receptor class to its second messenger and downstream kinase.
  - EK: GPCR–Gs → adenylyl cyclase → cAMP → PKA; Gq → PLC → IP₃ (Ca²⁺) and DAG (PKC); RTKs autophosphorylate and recruit SH2 proteins.
  - P2 · drills: bc-receptor-classes, bc-receptor-classes-2

## Unit 10 · Methods in biochemistry

Big ideas: MEASURE

### 10.1 Quantitation and size



- ● **BC-10.1.A** (acs-accm-analytical:I.D.3) Compute protein concentration from A₂₈₀ with the Beer–Lambert law.
  - EK: A = εcl; ε₂₈₀ ≈ 5500·nW + 1490·nY + 125·(cystines) M⁻¹ cm⁻¹.
  - P1 · drills: bc-a280, bc-a280-mg
- ● **BC-10.1.B** () Estimate a protein's molar mass from SDS-PAGE mobility against standards.
  - EK: log M is linear in relative mobility over the gel's range.
  - P1 · drills: bc-sds-mw, bc-sds-facts

### 10.2 Purification



- ● **BC-10.2.A** () Compute specific activity, fold purification and yield from a purification table.
  - EK: Specific activity = units/mg; fold = SA/SA_crude; yield = units/units_crude.
  - P1 · drills: bc-purification, bc-yield
- ● **BC-10.2.B** (acs-accm-analytical:IV.B.1) Choose a separation (ion exchange, gel filtration, affinity) from a protein's pI, size or binding.
  - EK: Below its pI a protein is positive and binds a cation exchanger; gel filtration elutes large proteins first.
  - P2 · drills: bc-separation-choice, bc-separation-choice-2

## Unit 11 · Evolution and homeostasis

Big ideas: INFORMATION, REGULATION

### 11.1 Molecular evolution



- ● **BC-11.1.A** (asbmb-core-2013:1.3, asbmb-core-2013:1.4, asbmb-core-2013:1.2) Estimate divergence time from sequence differences with a molecular clock.
  - EK: t = d/(2r): differences accumulate along both lineages.
  - P1 · drills: bc-mol-clock, bc-mol-clock-2
- ● **BC-11.1.B** (asbmb-cert:2.5, asbmb-core-2013:1.5, asbmb-core-2013:1.2) Judge homology from sequence identity and explain conserved function with changed sequence.
  - EK: Above ~30–40% identity over a full domain, proteins are very likely homologous; active-site residues are conserved more than surface ones.
  - P2 · drills: bc-identity, bc-homology

### 11.2 Steady state and control



- ● **BC-11.2.A** (asbmb-core-2013:3.2, asbmb-core-2013:3.6, asbmb-core-2013:3.3) Use the mass-action ratio to tell near-equilibrium steps from regulated, far-from-equilibrium ones.
  - EK: Q/K′ ≈ 1 means near equilibrium (not a control point); Q/K′ ≪ 1 means large negative ΔG, a likely control point.
  - P1 · drills: bc-mass-action, bc-steady-state

## Drills not yet placed on the map

- aa-draw-gly (biochem.amino-acids)
- aa-name-gly (biochem.amino-acids)
- aa-draw-ala (biochem.amino-acids)
- aa-name-ala (biochem.amino-acids)
- aa-draw-val (biochem.amino-acids)
- aa-name-val (biochem.amino-acids)
- aa-draw-leu (biochem.amino-acids)
- aa-name-leu (biochem.amino-acids)
- aa-draw-ile (biochem.amino-acids)
- aa-name-ile (biochem.amino-acids)
- aa-draw-ser (biochem.amino-acids)
- aa-name-ser (biochem.amino-acids)
- aa-draw-thr (biochem.amino-acids)
- aa-name-thr (biochem.amino-acids)
- aa-draw-cys (biochem.amino-acids)
- aa-name-cys (biochem.amino-acids)
- aa-draw-met (biochem.amino-acids)
- aa-name-met (biochem.amino-acids)
- aa-draw-asp (biochem.amino-acids)
- aa-name-asp (biochem.amino-acids)
- aa-draw-glu (biochem.amino-acids)
- aa-name-glu (biochem.amino-acids)
- aa-draw-asn (biochem.amino-acids)
- aa-name-asn (biochem.amino-acids)
- aa-draw-gln (biochem.amino-acids)
- aa-name-gln (biochem.amino-acids)
- aa-draw-lys (biochem.amino-acids)
- aa-name-lys (biochem.amino-acids)
- aa-draw-arg (biochem.amino-acids)
- aa-name-arg (biochem.amino-acids)
- aa-draw-his (biochem.amino-acids)
- aa-name-his (biochem.amino-acids)
- aa-draw-phe (biochem.amino-acids)
- aa-name-phe (biochem.amino-acids)
- aa-draw-tyr (biochem.amino-acids)
- aa-name-tyr (biochem.amino-acids)
- aa-draw-trp (biochem.amino-acids)
- aa-name-trp (biochem.amino-acids)
- aa-draw-pro (biochem.amino-acids)
- aa-name-pro (biochem.amino-acids)
- st-draw-adenine (biochem.nucleotides)
- st-name-adenine (biochem.nucleotides)
- st-draw-guanine (biochem.nucleotides)
- st-name-guanine (biochem.nucleotides)
- st-draw-cytosine (biochem.nucleotides)
- st-name-cytosine (biochem.nucleotides)
- st-draw-thymine (biochem.nucleotides)
- st-name-thymine (biochem.nucleotides)
- st-draw-uracil (biochem.nucleotides)
- st-name-uracil (biochem.nucleotides)
- st-draw-adenosine (biochem.nucleotides)
- st-name-adenosine (biochem.nucleotides)
- st-draw-atp (biochem.nucleotides)
- st-name-atp (biochem.nucleotides)
- st-draw-d-glyceraldehyde (biochem.sugars)
- st-name-d-glyceraldehyde (biochem.sugars)
- st-draw-d-ribose (biochem.sugars)
- st-name-d-ribose (biochem.sugars)
- st-draw-2-deoxy-d-ribose (biochem.sugars)
- st-name-2-deoxy-d-ribose (biochem.sugars)
- st-draw-d-glucose (biochem.sugars)
- st-name-d-glucose (biochem.sugars)
- st-draw-d-galactose (biochem.sugars)
- st-name-d-galactose (biochem.sugars)
- st-draw-d-mannose (biochem.sugars)
- st-name-d-mannose (biochem.sugars)
- st-draw-d-fructose (biochem.sugars)
- st-name-d-fructose (biochem.sugars)
- st-draw-alpha-d-glucopyranose (biochem.sugars)
- st-name-alpha-d-glucopyranose (biochem.sugars)
- st-draw-beta-d-glucopyranose (biochem.sugars)
- st-name-beta-d-glucopyranose (biochem.sugars)
- st-draw-beta-d-galactopyranose (biochem.sugars)
- st-name-beta-d-galactopyranose (biochem.sugars)
- st-draw-beta-d-ribofuranose (biochem.sugars)
- st-name-beta-d-ribofuranose (biochem.sugars)
- st-draw-2-deoxy-beta-d-ribofuranose (biochem.sugars)
- st-name-2-deoxy-beta-d-ribofuranose (biochem.sugars)
- st-draw-pyruvic-acid (biochem.metabolites)
- st-name-pyruvic-acid (biochem.metabolites)
- st-draw-lactic-acid (biochem.metabolites)
- st-name-lactic-acid (biochem.metabolites)
- st-draw-glycerol (biochem.metabolites)
- st-name-glycerol (biochem.metabolites)
- st-draw-glyceraldehyde-3-phosphate (biochem.metabolites)
- st-name-glyceraldehyde-3-phosphate (biochem.metabolites)
- st-draw-dihydroxyacetone-phosphate (biochem.metabolites)
- st-name-dihydroxyacetone-phosphate (biochem.metabolites)
- st-draw-phosphoenolpyruvic-acid (biochem.metabolites)
- st-name-phosphoenolpyruvic-acid (biochem.metabolites)
- st-draw-oxaloacetic-acid (biochem.metabolites)
- st-name-oxaloacetic-acid (biochem.metabolites)
- st-draw-citric-acid (biochem.metabolites)
- st-name-citric-acid (biochem.metabolites)
- st-draw-alpha-ketoglutaric-acid (biochem.metabolites)
- st-name-alpha-ketoglutaric-acid (biochem.metabolites)
- st-draw-succinic-acid (biochem.metabolites)
- st-name-succinic-acid (biochem.metabolites)
- st-draw-fumaric-acid (biochem.metabolites)
- st-name-fumaric-acid (biochem.metabolites)
- st-draw-malic-acid (biochem.metabolites)
- st-name-malic-acid (biochem.metabolites)
- st-draw-a-peptide-bond (biochem.peptides)
- st-name-a-peptide-bond (biochem.peptides)
- st-draw-glycylalanine (biochem.peptides)
- st-name-glycylalanine (biochem.peptides)
- st-draw-alanylglycine (biochem.peptides)
- st-name-alanylglycine (biochem.peptides)
- st-draw-glutathione (biochem.peptides)
- st-name-glutathione (biochem.peptides)
- st-draw-cystine (biochem.peptides)
- st-name-cystine (biochem.peptides)
- st-mech-chymotrypsin-1 (biochem.mechanisms)
- st-mech-chymotrypsin-2 (biochem.mechanisms)
- st-mech-chymotrypsin-3 (biochem.mechanisms)
- st-mech-chymotrypsin-4 (biochem.mechanisms)
- st-mech-chymotrypsin-whole (biochem.mechanisms)
- st-mech-chymotrypsin-roles (biochem.mechanisms)
- st-draw-nad (biochem.coenzymes)
- st-name-nad (biochem.coenzymes)
- st-draw-nadh (biochem.coenzymes)
- st-name-nadh (biochem.coenzymes)
- st-draw-fad (biochem.coenzymes)
- st-name-fad (biochem.coenzymes)
- st-draw-coenzyme-a (biochem.coenzymes)
- st-name-coenzyme-a (biochem.coenzymes)
- st-draw-acetyl-coa (biochem.coenzymes)
- st-name-acetyl-coa (biochem.coenzymes)
- st-draw-thiamine-pyrophosphate (biochem.coenzymes)
- st-name-thiamine-pyrophosphate (biochem.coenzymes)
- st-draw-protoporphyrin-ix (biochem.coenzymes)
- st-name-protoporphyrin-ix (biochem.coenzymes)
- st-draw-heme-b (biochem.coenzymes)
- st-name-heme-b (biochem.coenzymes)
- st-draw-palmitic-acid (biochem.lipids-coenzymes)
- st-name-palmitic-acid (biochem.lipids-coenzymes)
- st-draw-stearic-acid (biochem.lipids-coenzymes)
- st-name-stearic-acid (biochem.lipids-coenzymes)
- st-draw-oleic-acid (biochem.lipids-coenzymes)
- st-name-oleic-acid (biochem.lipids-coenzymes)
- st-draw-cholesterol (biochem.lipids-coenzymes)
- st-name-cholesterol (biochem.lipids-coenzymes)
- st-draw-nicotinamide (biochem.lipids-coenzymes)
- st-name-nicotinamide (biochem.lipids-coenzymes)
- st-draw-pyridoxal-phosphate (biochem.lipids-coenzymes)
- st-name-pyridoxal-phosphate (biochem.lipids-coenzymes)
- st-draw-biotin (biochem.lipids-coenzymes)
- st-name-biotin (biochem.lipids-coenzymes)
- st-draw-lipoic-acid (biochem.lipids-coenzymes)
- st-name-lipoic-acid (biochem.lipids-coenzymes)
