"""ACS Exams Institute Anchoring Concepts Content Maps for general, organic and inorganic chemistry, read in full from
the supporting information Kevin supplied (Nov 2026):

  general    Holme, Luxford & Murphy, J. Chem. Educ. 2015, 92, 1115 (ed500712k, SI 2: the updated map; it supersedes
             the 2012 map of Holme & Murphy, ed300050q, which was also read)
  organic    Raker, Holme & Murphy, J. Chem. Educ. 2013, 90, 1443 (ed400175w, SI 3)
  inorganic  Marek, Raker, Holme & Murphy, J. Chem. Educ. 2018, 95, 233 (ed7b00498, SI 1)

Each map is ten anchoring concepts → enduring understandings (I.A) → subdisciplinary articulations (I.A.1) → content
details. Items are the articulations, plus any enduring understanding that has none (written as I.F). Labels are our
paraphrases, never the maps' text. CITE_* maps each item to the Library objectives that answer it; an empty list is a
gap. scripts/accm_cite2.py writes the citations onto the objectives (add-only)."""

GEN = [
    ("I.A.1", "Atomic number identifies the element; element symbols"),
    ("I.A.2", "Isotopes: same Z, different mass; weighted average atomic mass"),
    ("I.B.1", "Core and valence electrons in a neutral atom"),
    ("I.B.2", "Orbitals as wavefunctions labelled by quantum numbers"),
    ("I.B.3", "Electron configurations of atoms and ions"),
    ("I.C.1", "Periodic trends in radius, ionisation energy, electron affinity"),
    ("I.C.2", "Effective nuclear charge explains the trends"),
    ("I.C.3", "Periodic trends in the reactivity of elements"),
    ("I.D.1", "Wavelength and frequency of light; which region probes what"),
    ("I.D.2", "Kinetic molecular theory links particles to bulk behaviour"),
    ("I.D.3", "Bulk properties and qualitative trends used to classify matter"),
    ("I.E.1", "The mole and Avogadro's number from the relative mass scale"),
    ("I.E.2", "Mole conversions: mass, amount, number of particles"),
    ("I.E.3", "Atoms are picometre-sized, so N_A is enormous"),
    ("I.F.1", "Mass is conserved because atoms are"),
    ("I.F.2", "Nuclear equations follow changes of identity"),
    ("I.F.3", "Radioactivity measurements identify and quantify isotopes"),
    ("I.G.1", "Anions gain electrons, cations lose them"),
    ("I.G.2", "Ions behave differently from their parent atoms"),
    ("II.A.1", "Ionic bonding as Coulomb attraction"),
    ("II.A.2", "Telling covalent from ionic bonding by the elements"),
    ("II.A.3", "The ionic–polar–nonpolar continuum"),
    ("II.B.1", "Valence-shell electrons form bonds"),
    ("II.B.2", "Covalent bonds as shared electron pairs"),
    ("II.C.1", "A stable bond lowers the energy"),
    ("II.C.2", "Potential energy against internuclear distance"),
    ("II.C.3", "Valence bond theory: overlap of wavefunctions"),
    ("II.D.1", "Bond dissociation energy"),
    ("II.E.1", "Molecular orbitals built from atomic orbitals"),
    ("II.F.1", "Single, double and triple bonds as one, two, three shared pairs"),
    ("II.G.1", "Electron-sea model of metals"),
    ("II.G.2", "Band model of metals"),
    ("III.A.1", "Compounds have fixed atom ratios"),
    ("III.A.2", "Elements that exist as small molecules"),
    ("III.A.3", "Pure substances versus mixtures"),
    ("III.B.1", "Isomers: same formula, different arrangement"),
    ("III.B.2", "Lewis structures for connectivity"),
    ("III.B.3", "VSEPR with Lewis structures predicts shape"),
    ("III.C", "Computed structures of whole molecules"),
    ("III.D", "Symmetry and molecular interactions"),
    ("III.E", "Chirality"),
    ("III.F.1", "Formulas written to show functional groups"),
    ("III.F.2", "Functional groups and acid–base strength"),
    ("III.G.1", "Atom and ion sizes set how solids pack"),
    ("III.H.1", "Metallic, ionic and network solids"),
    ("III.H.2", "Macromolecules understood from their repeat units"),
    ("III.H.3", "Getting an element out of the compounds that hold it"),
    ("IV.A.1", "Weak forces make gases; ideal-gas models"),
    ("IV.A.2", "Properties set by intermolecular forces"),
    ("IV.A.3", "Overcoming only intermolecular forces is a physical change"),
    ("IV.B.1", "Nonbonding forces within one macromolecule"),
    ("IV.C.1", "Dispersion, dipole–dipole and hydrogen bonding"),
    ("IV.C.2", "Permanent dipoles from shape and bond dipoles"),
    ("IV.D.1", "Electrolytes and nonelectrolytes"),
    ("IV.D.2", "Solute–solvent forces govern solutions"),
    ("IV.D.3", "Concentration calculations"),
    ("IV.E.1", "Enthalpy and entropy of solution"),
    ("V.A.1", "Balancing equations"),
    ("V.A.2", "Mass conservation observed in reactions"),
    ("V.A.3", "Stoichiometry from the balanced equation"),
    ("V.B.1", "Structures showing which bonds change"),
    ("V.C.1", "Particle pictures of reactions and limiting reactants"),
    ("V.D.1", "Synthesis, decomposition and double displacement"),
    ("V.D.2", "Redox reactions, including combustion"),
    ("V.D.3", "Acid–base neutralisation and its definitions"),
    ("V.E.1", "Periodic trends in reactions with water and oxygen"),
    ("V.F.1", "Precipitation for qualitative analysis of ions"),
    ("V.F.2", "Limiting reactants and percent yield"),
    ("V.G.1", "Synthesis of modern materials"),
    ("VI.A.1", "Kinetic versus potential energy in reactions"),
    ("VI.A.2", "Energy change as heat and work"),
    ("VI.A.3", "Consistent energy units"),
    ("VI.A.4", "Internal energy versus enthalpy"),
    ("VI.B.1", "Stable until initiated: energy input to start a reaction"),
    ("VI.C.1", "Heat measured through temperature change"),
    ("VI.C.2", "Enthalpy of reaction as heat at constant pressure"),
    ("VI.C.3", "Electrochemistry separates oxidation from reduction"),
    ("VI.D.1", "Bonds broken and formed decide the net energy"),
    ("VI.E.1", "Charge moving through an external circuit"),
    ("VI.F.1", "Pressure–volume work in engines"),
    ("VI.F.2", "Batteries harness chemical change"),
    ("VI.G.1", "State functions"),
    ("VI.G.2", "Hess's law"),
    ("VI.H.1", "Spontaneous change raises the entropy of the universe"),
    ("VI.H.2", "Gibbs energy and spontaneity"),
    ("VI.H.3", "Zero entropy of a perfect crystal at 0 K"),
    ("VI.H.4", "Spontaneous does not mean fast"),
    ("VI.I.1", "Nuclear energy from mass conversion"),
    ("VII.A.1", "A rate defined independently of the species followed"),
    ("VII.A.2", "Rate as change in concentration with time"),
    ("VII.A.3", "Surface area of solids and reaction rate"),
    ("VII.B.1", "Reaction order from the rate law's exponents"),
    ("VII.B.2", "Temperature dependence through the Arrhenius model"),
    ("VII.C.1", "Overall stoichiometry is not the mechanism"),
    ("VII.C.2", "Mechanisms whose steps sum to the overall reaction"),
    ("VII.D.1", "Collision theory: energy and orientation"),
    ("VII.D.2", "Activation energy"),
    ("VII.E.1", "What a catalyst is"),
    ("VII.E.2", "Catalysis through a lower-barrier pathway"),
    ("VII.F.1", "Kinetic versus thermodynamic control"),
    ("VIII.A.1", "Phase changes as reversible, dynamic equilibria"),
    ("VIII.B.1", "Equal forward and reverse rates in phase and chemical equilibria"),
    ("VIII.C.1", "Equilibrium amounts from K and the starting state"),
    ("VIII.C.2", "Solubility equilibria of ionic solids"),
    ("VIII.D.1", "Large or small K and which side is favoured"),
    ("VIII.D.2", "The reverse reaction has 1/K"),
    ("VIII.D.3", "K for a sum of reactions is the product of the K's"),
    ("VIII.E.1", "Le Châtelier's principle"),
    ("VIII.F.1", "K and the Gibbs energy change"),
    ("VIII.F.2", "Cell potential and the Gibbs energy change"),
    ("VIII.G.1", "Acid–base reactions as equilibria"),
    ("VIII.G.2", "How buffers resist pH change"),
    ("VIII.G.3", "Protein–ligand binding as an equilibrium"),
    ("IX.A.1", "Homogeneous and heterogeneous mixtures"),
    ("IX.A.2", "Separating mixtures by distillation and chromatography"),
    ("IX.B.1", "Lab observations read through particle models"),
    ("IX.B.2", "Derived quantities such as density"),
    ("IX.B.3", "Measuring reaction rates in the lab"),
    ("IX.C.1", "Naming compounds by class"),
    ("IX.D.1", "Controlling a reaction through concentration"),
    ("IX.E.1", "Mass measurements and percent yield"),
    ("IX.E.2", "Making a product or releasing energy in the lab"),
    ("IX.E.3", "Line spectra as evidence for the quantum atom"),
    ("IX.E.4", "Mass spectra show isotopes"),
    ("IX.F.1", "Designing procedures that limit measurement error"),
    ("IX.F.2", "Preparing solutions of known concentration"),
    ("IX.G.1", "Accuracy and precision"),
    ("IX.G.2", "Random and systematic error"),
    ("IX.G.3", "Recording observations properly"),
    ("IX.G.4", "Calibration against known samples"),
    ("IX.H.1", "Safety equipment in the laboratory"),
    ("IX.H.2", "Chemical hazards and how to handle them"),
    ("IX.H.3", "Disposing of chemical waste"),
    ("IX.H.4", "Continual awareness of hazard and risk"),
    ("IX.H.5", "Working safely with radioactive material"),
    ("X.A.1", "Kinetic molecular theory as a bridge between scales"),
    ("X.A.2", "Symbolic, macroscopic and particle representations"),
    ("X.B.1", "The mole defined by carbon-12"),
    ("X.C.1", "The Boltzmann distribution as a distribution function"),
    ("X.C.2", "Bulk observables driven by molecular-scale gradients"),
    ("X.D.1", "Energy profiles carry kinetic and thermodynamic information"),
    ("X.D.2", "Linearising data (ln, 1/x) to read a relationship"),
    ("X.E.1", "Rearranging equations to isolate a variable"),
]

ORG = [
    ("I.A.1", "Isotopes in MS, NMR and kinetic isotope effects"),
    ("I.B.1", "Electrons and the relative stability of resonance forms"),
    ("I.B.2", "Electrophiles attack electron-rich sites"),
    ("I.B.3", "Nucleophiles attack electron-poor sites"),
    ("I.C.1", "Valence periodicity behind nucleophilicity and pKa trends"),
    ("I.C.2", "Periodic trends in bond strength and length"),
    ("I.D.1", "How organic chemistry's discoveries were made"),
    ("I.D.2", "Structure elucidation by UV, IR, NMR and MS"),
    ("I.E.1", "Molar equivalents, limiting reagents and percent yield"),
    ("I.F", "Atoms keep their identity outside nuclear reactions"),
    ("I.G.1", "Polar metal–carbon bonds as strong bases and nucleophiles"),
    ("II.A.1", "Covalent bonding; primary to quaternary carbons"),
    ("II.A.2", "Bond dipoles from unequal sharing"),
    ("II.B.1", "Bond energy set by the nuclei and electrons shared"),
    ("II.C.1", "Filling low-energy orbitals lowers the energy"),
    ("II.C.2", "Conjugation and aromatic stabilisation"),
    ("II.D.1", "Homolysis and bond dissociation energy"),
    ("II.E.1", "Hybridisation, resonance and MO theory"),
    ("II.E.2", "Orbital symmetry in cycloadditions"),
    ("II.E.3", "Bonding, nonbonding and antibonding MOs; conservation of orbitals"),
    ("II.F.1", "Sigma and pi bonds; lengths and strengths"),
    ("II.F.2", "Free rotation about single bonds, none about double bonds"),
    ("II.G", "Metallic bonding"),
    ("III.A.1", "Functional groups set physical properties"),
    ("III.A.2", "Stereocentres and chirality"),
    ("III.A.3", "Polymers and carbon allotropes"),
    ("III.B.1", "Shape and polarity from VSEPR"),
    ("III.B.2", "Shape and stereochemistry"),
    ("III.C.1", "Molecular modelling programs"),
    ("III.D.1", "Spectroscopy and molecular symmetry"),
    ("III.D.2", "Symmetry-equivalent nuclei in NMR"),
    ("III.E.1", "Enantiomers and diastereomers"),
    ("III.E.2", "Regio- and stereospecific versus selective reactions"),
    ("III.E.3", "Stereochemistry carried from reactant to product"),
    ("III.E.4", "3-D structure decides transition states and isomeric products"),
    ("III.E.5", "Optical activity; separating diastereomers"),
    ("III.F.1", "Reactivity follows functional-group structure"),
    ("III.G", "Extended solid-state structures"),
    ("IV.A.1", "Intermolecular forces in spectra and physical properties"),
    ("IV.A.2", "Forces behind solubility, melting and boiling, solvent effects"),
    ("IV.A.3", "Hydrogen bonding"),
    ("IV.B.1", "Surfactants and micelles"),
    ("IV.B.2", "Forces in polymer, protein and DNA structure"),
    ("IV.C.1", "Intermolecular forces in collisions"),
    ("IV.D.1", "Choosing a solvent by its forces"),
    ("IV.D.2", "Solvent choice and green chemistry"),
    ("IV.E.1", "Solvent choice in organic reactions"),
    ("IV.E.2", "Solvent polarity can switch mechanism and product"),
    ("V.A.1", "Reagents written over the arrow; unbalanced organic equations"),
    ("V.A.2", "Reaction yields"),
    ("V.A.3", "Lab techniques for yield and purity"),
    ("V.A.4", "Multistep synthesis"),
    ("V.B.1", "Bond-making and breaking energetics in synthesis"),
    ("V.C.1", "Visualising molecules reacting"),
    ("V.C.2", "Representations of organic structure"),
    ("V.D.1", "Addition, elimination, rearrangement, substitution, redox"),
    ("V.D.2", "SN1, SN2, E1, E2, electrophilic and nucleophilic aromatic substitution"),
    ("V.D.3", "Radical reactions"),
    ("V.D.4", "Greener reaction conditions"),
    ("V.E.1", "Reactivity organised by functional group"),
    ("V.E.2", "Control by time, temperature, catalyst and solvent"),
    ("V.F.1", "Reagents that control regio- and stereochemistry"),
    ("V.F.2", "Reagents that control regiochemistry"),
    ("VI.A.1", "Thermodynamics of energy change"),
    ("VI.A.2", "Reaction energy diagrams"),
    ("VI.B.1", "Activation energy"),
    ("VI.C.1", "Heat and light as energy sources"),
    ("VI.C.2", "Thermal versus photochemical pericyclic reactions"),
    ("VI.D.1", "Net energy from bonds broken and formed"),
    ("VI.E.1", "Solvation by dipole and induced-dipole forces"),
    ("VI.F.1", "Combustion of hydrocarbons"),
    ("VI.G.1", "Reaction enthalpy from bond energies"),
    ("VI.H", "Entropy and dispersal"),
    ("VI.I", "Nuclear energy scales"),
    ("VII.A.1", "Fast and slow reactions decide the product"),
    ("VII.B.1", "Rate laws as clues to substitution and elimination mechanisms"),
    ("VII.C.1", "Elementary steps behind functional-group reactivity"),
    ("VII.C.2", "Polar and polarisable bonds dictate reactivity"),
    ("VII.C.3", "Curved arrows from nucleophile to electrophile"),
    ("VII.D.1", "Transition-state theory for SN2"),
    ("VII.E.1", "Catalysts lower the activation energy"),
    ("VII.F.1", "Kinetic versus thermodynamic control"),
    ("VII.F.2", "Intermediates, resonance and hyperconjugation in that control"),
    ("VIII.A.1", "Equilibrium position limits product"),
    ("VIII.B.1", "Reversible reactions reach equilibrium"),
    ("VIII.C.1", "Equilibria seen by energy diagram, conformational analysis or instrument"),
    ("VIII.C.2", "pKa as a protonation equilibrium"),
    ("VIII.D.1", "Large K strongly favours products"),
    ("VIII.E.1", "Le Châtelier's principle to drive a reaction"),
    ("VIII.F", "Thermodynamic treatment of equilibrium"),
    ("VIII.G.1", "Protonation equilibria in acid catalysis"),
    ("IX.A.1", "Chemical tests for functional groups"),
    ("IX.A.2", "Instrumental data: X-ray, NMR, IR, MS, EPR"),
    ("IX.A.3", "Wet tests against instrumental methods"),
    ("IX.B.1", "Systematic nomenclature"),
    ("IX.C.1", "Data confirm the intended product"),
    ("IX.C.2", "Measuring stereochemical outcome"),
    ("IX.D", "Measurement by mass, charge or interaction with light"),
    ("IX.E", "Verifiable observations and controls"),
    ("IX.F", "Experimental design for sound inference"),
    ("X.A.1", "Spectroscopic and physical probes in the organic lab"),
    ("X.B.1", "Lab yields explained by molecular models"),
    ("X.C", "Statistics behind macroscopic properties"),
    ("X.D", "Graphical quantitative reasoning"),
]

INORG = [
    ("I.A.1", "Atomic number identifies the element"),
    ("I.A.2", "Uses of isotopes in inorganic chemistry"),
    ("I.B.1", "Quantum mechanics of electrons in atoms"),
    ("I.B.2", "Quantum numbers give orbital size, shape and orientation"),
    ("I.B.3", "Coulomb terms in configuration energies"),
    ("I.B.4", "Shielding and penetration"),
    ("I.B.5", "Magnetism from electron spin"),
    ("I.B.6", "Oxidation states and their stability"),
    ("I.C.1", "Effective nuclear charge and periodic trends"),
    ("I.C.2", "Group similarities in reactivity, structure and formula"),
    ("I.C.3", "Metal, nonmetal or metalloid behaviour from position"),
    ("I.D.1", "Atomic spectroscopy probes energy levels"),
    ("I.D.2", "X-ray diffraction of powders and single crystals"),
    ("I.E.1", "Stoichiometry, equivalents and percent yield"),
    ("I.F.1", "Kinds of nuclear reaction"),
    ("I.G.1", "Forming cations and anions; which electrons leave"),
    ("I.G.2", "Isoelectronic series"),
    ("II.A.1", "Orbital energies decide the bond type"),
    ("II.A.2", "Crystal field theory"),
    ("II.A.3", "Ionic bonding by electron transfer"),
    ("II.A.4", "Electron-counting rules"),
    ("II.B.1", "Bond order and bond strength"),
    ("II.B.2", "Dative bonds in coordination compounds"),
    ("II.B.3", "Electrostatic cohesion of ionic compounds"),
    ("II.C.1", "Overlap sets bond strength"),
    ("II.C.2", "Lattice energy"),
    ("II.C.3", "Ligand field stabilisation energy"),
    ("II.D.1", "Bond dissociation enthalpy rises with bond order"),
    ("II.D.2", "Vibrational frequency rises with bond order"),
    ("II.E.1", "MOs from orbitals of matching symmetry"),
    ("II.E.2", "Orbital interactions set MO energies"),
    ("II.E.3", "Molecular electron configurations"),
    ("II.E.4", "Symmetry-adapted MOs of polyatomics"),
    ("II.E.5", "Ligand field theory as MO theory of complexes"),
    ("II.F.1", "Lewis structures"),
    ("II.F.2", "Valence bond theory"),
    ("II.F.3", "Bond strength and length against bond order"),
    ("II.G.1", "Electron-sea model"),
    ("II.G.2", "Band theory of conductivity"),
    ("II.G.3", "p–n junctions and their uses"),
    ("II.G.4", "BCS theory of superconductivity"),
    ("III.A.1", "Coordination compounds as Lewis acid–base adducts"),
    ("III.A.2", "Properties set by the coordination environment"),
    ("III.A.3", "Organometallic compounds"),
    ("III.A.4", "Cluster compounds"),
    ("III.A.5", "Chains and layers in Si, P and S chemistry"),
    ("III.B.1", "VSEPR"),
    ("III.B.2", "Wade's rules for clusters"),
    ("III.C.1", "Computed geometries by energy minimisation"),
    ("III.D.1", "Point groups"),
    ("III.D.2", "Space groups"),
    ("III.D.3", "Representations of orbitals and vibrations"),
    ("III.D.4", "Symmetry in interpreting spectra"),
    ("III.D.5", "Properties read from symmetry (polarity, chirality)"),
    ("III.E.1", "Coordination numbers and geometries"),
    ("III.E.2", "Stereoisomers of complexes"),
    ("III.E.3", "Polymorphism"),
    ("III.E.4", "Chiral catalysts"),
    ("III.E.5", "Constitutional isomers of complexes (linkage, ionisation, hydrate, coordination)"),
    ("III.E.6", "Separating and resolving isomers"),
    ("III.F.1", "Classes of ligands"),
    ("III.F.2", "The isolobal analogy"),
    ("III.F.3", "Steric and electronic effects of ligands"),
    ("III.G.1", "Group formulas of oxides, hydrides and halides"),
    ("III.G.2", "The diagonal relationship"),
    ("III.G.3", "The lanthanide contraction"),
    ("III.G.4", "The inert-pair effect"),
    ("III.G.5", "Metal and nonmetal compounds compared"),
    ("III.G.6", "Interhalogen trends"),
    ("III.G.7", "Isoelectronic groups form analogous structures"),
    ("III.H.1", "Packing motifs of extended solids"),
    ("III.H.2", "Ionic structures as filled holes"),
    ("III.H.3", "Defects and interstitials"),
    ("III.H.4", "Nanomaterials of 0 to 3 dimensions"),
    ("III.H.5", "Allotropes of the p-block"),
    ("III.H.6", "Layered solids"),
    ("III.H.7", "Silicate structures"),
    ("III.H.8", "Perovskite-related superconductors"),
    ("IV.A.1", "Dispersion trends in halogen and noble-gas boiling points"),
    ("IV.A.2", "Self-assembly by intermolecular forces"),
    ("IV.B.1", "Hydrogen bonding between metal centres and ligands"),
    ("IV.B.2", "Forces between domains of block copolymers"),
    ("IV.B.3", "Hydrogen bonding in biomolecule structure"),
    ("IV.C.1", "Dispersion, dipole–dipole and hydrogen bonding"),
    ("IV.D.1", "Solid properties from intermolecular forces"),
    ("IV.D.2", "Bulk properties from intermolecular forces"),
    ("IV.D.3", "Phase diagrams"),
    ("IV.E.1", "Intermolecular forces in solution formation"),
    ("IV.E.2", "Forces at surfaces and nanoparticles"),
    ("IV.E.3", "Solvation in reactions"),
    ("V.A.1", "Balancing redox equations in acid, base or neutral solution"),
    ("V.B.1", "Frontier-orbital energies decide whether and how reactions go"),
    ("V.C.1", "Scanning probe microscopy of surface reactions"),
    ("V.D.1", "Acid–base models (Brønsted, Lewis, Lux–Flood, solvent system)"),
    ("V.D.2", "Redox as electron transfer"),
    ("V.D.3", "Organometallic reaction classes by electron count"),
    ("V.D.4", "Metathesis (double displacement)"),
    ("V.D.5", "Heterogeneous reactions at surfaces"),
    ("V.D.6", "Condensation reactions"),
    ("V.E.1", "Periodic trends in reduction potentials"),
    ("V.E.2", "Hydration enthalpies and LFSE"),
    ("V.E.3", "Periodic trends in acid–base properties"),
    ("V.F.1", "Controlling reactions by sterics, pH, solvent, particle size"),
    ("V.F.2", "Metal catalysts, homogeneous and heterogeneous"),
    ("V.F.3", "Metals in biochemistry"),
    ("V.F.4", "Chiral catalysts and stereocontrol"),
    ("V.F.5", "Acid–base behaviour in nonaqueous solvents"),
    ("V.F.6", "Superacids"),
    ("V.F.7", "Fluorine and other strong oxidants in synthesis"),
    ("V.F.8", "The trans effect and trans influence in synthesis"),
    ("V.F.9", "Hard–soft acid–base control of products"),
    ("V.F.10", "Photochemical reactions"),
    ("V.G.1", "Solid-state properties depend on synthesis conditions"),
    ("V.G.2", "Air-, water- and light-sensitive techniques"),
    ("V.G.3", "Coordination chemistry in SAMs and MOFs"),
    ("VI.A.1", "Negative ΔG for spontaneous processes"),
    ("VI.A.2", "Equilibrium between states from their ΔG"),
    ("VI.A.3", "Born–Haber cycles"),
    ("VI.B.1", "Activation energy and rate"),
    ("VI.B.2", "Fluxional molecules"),
    ("VI.B.3", "LFSE and substitution barriers"),
    ("VI.C.1", "Chemical energy converted to other forms"),
    ("VI.C.2", "Measuring or estimating energy differences"),
    ("VI.D.1", "Bond dissociation in Born–Haber cycles"),
    ("VI.D.2", "Bond energies and activation energy"),
    ("VI.D.3", "Proton gain enthalpies and acid–base strength"),
    ("VI.D.4", "Metal and ligand identity in complex energetics"),
    ("VI.E.1", "Cell potential and ΔG"),
    ("VI.E.2", "Electrostatics in complex formation"),
    ("VI.F.1", "Galvanic and electrolytic cells"),
    ("VI.F.2", "Devices converting electrical energy"),
    ("VI.G.1", "Reaction enthalpy from bond energies"),
    ("VI.H.1", "Entropy-driven reactions (chelate effect)"),
    ("VI.H.2", "ΔG = ΔH − TΔS"),
    ("VI.I.1", "Nuclear energy levels, fission and fusion"),
    ("VII.A.1", "Inert and labile complexes"),
    ("VII.A.2", "Fluxionality on different time scales"),
    ("VII.B.1", "Rate measurements under varied conditions"),
    ("VII.C.1", "Activated complexes and transition states"),
    ("VII.C.2", "The steady-state approximation"),
    ("VII.C.3", "Inner- and outer-sphere electron transfer"),
    ("VII.C.4", "Associative, dissociative and interchange substitution"),
    ("VII.C.5", "Mechanisms of fluxional rearrangement (Berry pseudorotation)"),
    ("VII.C.6", "The kinetic chelate effect"),
    ("VII.D.1", "Solvent cages and outer-sphere pre-association"),
    ("VII.E.1", "Catalysts reshape the energy surface"),
    ("VII.E.2", "Heterogeneous catalyst structure and selectivity"),
    ("VII.F.1", "Kinetic versus thermodynamic products"),
    ("VIII.A.1", "Microscopic reversibility"),
    ("VIII.B.1", "Equilibrium as a dynamic steady state"),
    ("VIII.C.1", "Standard equilibrium constants (formation, Ksp, Ka)"),
    ("VIII.D.1", "Equilibrium constants showing periodic trends (Irving–Williams)"),
    ("VIII.D.2", "HSAB and the size of K"),
    ("VIII.E.1", "Le Châtelier in industrial processes"),
    ("VIII.F.1", "K with ΔG, ΔH, ΔS and E°"),
    ("VIII.F.2", "Proton affinity and Brønsted acidity"),
    ("VIII.F.3", "Thermodynamics of complex formation (stepwise and overall β)"),
    ("VIII.G.1", "Equilibrium constants for reactivity"),
    ("VIII.G.2", "The levelling effect"),
    ("VIII.G.3", "Speciation with pH and conditions"),
    ("VIII.G.4", "Chemical sensors from equilibria"),
    ("IX.A.1", "Microscopy from macroscopic to atomic"),
    ("IX.A.2", "Observing fluxional processes spectroscopically"),
    ("IX.A.3", "Structure from bulk measurements"),
    ("IX.A.4", "Fluorescence and phosphorescence time scales"),
    ("IX.B.1", "Naming coordination and organometallic compounds"),
    ("IX.B.2", "Prototype crystal structures and hole filling"),
    ("IX.B.3", "Named catalysts and industrial processes"),
    ("IX.C.1", "Synthesis parameters shape the product"),
    ("IX.C.2", "Analysis for identity and purity"),
    ("IX.D.1", "Formula from combined analyses"),
    ("IX.D.2", "UV–visible spectra of valence transitions"),
    ("IX.D.3", "Multinuclear NMR"),
    ("IX.D.4", "Quantitative redox analysis"),
    ("IX.D.5", "Which radiation probes which transition"),
    ("IX.D.6", "X-ray, electron and neutron diffraction"),
    ("IX.D.7", "Magnetic susceptibility measurements"),
    ("IX.D.8", "Conductivity against temperature"),
    ("IX.E.1", "Purity and comparison with standards"),
    ("IX.E.2", "Conditions affect measured values"),
    ("IX.F.1", "Precision limited by equipment and execution"),
    ("IX.F.2", "Reporting experimental conditions"),
    ("IX.G.1", "Handling light-, air- and moisture-sensitive compounds"),
    ("IX.G.2", "High- and low-pressure hazards"),
    ("IX.G.3", "Cryogen hazards"),
    ("IX.G.4", "Using safety data resources"),
    ("IX.G.5", "Green chemical methods"),
    ("X.A.1", "Bulk properties of nano- and macromaterials from interactions"),
    ("X.A.2", "Band theory as MO theory at the macroscale"),
    ("X.A.3", "Ligand field theory explains what complexes look like"),
    ("X.B.1", "Avogadro's number between grams and amu"),
    ("X.C.1", "Particle size distributions"),
    ("X.D.1", "Plots of periodic trends"),
    ("X.D.2", "MO diagrams"),
    ("X.D.3", "3-D drawings for symmetry"),
    ("X.D.4", "Orbital drawings"),
    ("X.D.5", "Latimer, Pourbaix, Frost and Ellingham diagrams"),
    ("X.D.6", "Phase and distribution (speciation) diagrams"),
    ("X.D.7", "Tanabe–Sugano and Orgel diagrams"),
    ("X.D.8", "Unit-cell and plan drawings"),
    ("X.D.9", "Energy profiles for kinetics"),
]


def _c(text):
    """'I.A.1: CH-0.4.A PT-1.1.A' lines → {item: [objective codes]}"""
    out = {}
    for line in text.strip().splitlines():
        k, _, v = line.partition(":")
        out[k.strip()] = v.split()
    return out


CITE_GEN = _c("""
I.A.1: CH-0.4.A PT-1.1.A
I.A.2: CH-1.2.A CH-1.2.B
I.B.1: CH-1.5.A CH-1.5.C
I.B.2: CH-1.9.A
I.B.3: CH-1.5.A CH-1.5.B PT-4.1.C
I.C.1: CH-1.7.A
I.C.2: CH-1.5.C CH-1.7.A
I.C.3: CH-1.8.B IN-1.1.B
I.D.1: CH-3.11.A CH-3.12.A
I.D.2: CH-3.5.A
I.D.3: CH-0.1.B CH-0.2.D
I.E.1: CH-0.5.A
I.E.2: CH-1.1.A
I.E.3: CH-0.5.B
I.F.1: CH-4.1.A
I.F.2: CH-1.10.A
I.F.3: CH-1.10.C
I.G.1: CH-1.8.A CH-1.7.D
I.G.2: CH-1.7.D
II.A.1: CH-2.2.B CH-2.3.A
II.A.2: CH-2.1.A
II.A.3: CH-2.1.A
II.B.1: CH-2.5.A
II.B.2: CH-2.5.A
II.C.1: CH-2.2.A
II.C.2: CH-2.2.A
II.C.3: CH-2.7.C
II.D.1: CH-6.7.A
II.E.1: CH-2.8.A
II.F.1: CH-2.7.C CH-2.6.B
II.G.1: CH-2.4.A
II.G.2: PC-6.1.F
III.A.1: CH-1.3.B
III.A.2: CH-6.8.A
III.A.3: CH-0.1.A
III.B.1: DAT-3.5.D
III.B.2: CH-2.5.A
III.B.3: CH-2.7.A
III.C: PC-15.3.B
III.D: PC-17.1.B
III.E: DAT-3.5.C
III.F.1: ST-1.1.A
III.F.2: CH-8.6.A
III.G.1: IN-5.1.E
III.H.1: CH-3.2.A
III.H.2: MT-1.1.C
III.H.3: CH-4.5.F
IV.A.1: CH-3.6.A CH-3.4.A
IV.A.2: CH-3.1.B
IV.A.3: CH-4.4.A
IV.B.1: BI-1.5.A
IV.C.1: CH-3.1.A
IV.C.2: CH-2.7.B
IV.D.1: CH-3.7.C
IV.D.2: CH-3.10.A
IV.D.3: CH-3.7.A CH-3.7.D
IV.E.1: CH-9.6.A
V.A.1: CH-4.1.A
V.A.2: CH-4.5.A
V.A.3: CH-4.5.A
V.B.1: CH-4.3.A DAT-3.1.A
V.C.1: CH-4.3.A CH-4.5.B
V.D.1: CH-4.7.B
V.D.2: CH-4.9.B CH-4.7.A
V.D.3: CH-4.8.A CH-8.6.B
V.E.1: IN-1.1.B IA-3.1.A
V.F.1: IN-4.2.C CH-4.2.A
V.F.2: CH-4.5.C
V.G.1: MT-2.1.B
VI.A.1: CH-6.3.A
VI.A.2: CH-6.10.A
VI.A.3: AQ-3.1.A
VI.A.4: CH-6.10.B
VI.B.1: CH-9.4.A
VI.C.1: CH-6.4.A
VI.C.2: CH-6.4.C
VI.C.3: CH-9.8.A
VI.D.1: CH-6.7.A
VI.E.1: CH-9.11.A
VI.F.1: CH-6.10.A
VI.F.2: CH-9.8.A
VI.G.1: CH-6.9.A
VI.G.2: CH-6.9.A
VI.H.1: CH-9.1.A
VI.H.2: CH-9.3.A CH-9.3.B
VI.H.3: PC-3.2.D PC-20.2.E
VI.H.4: CH-9.4.A
VI.I.1: CH-1.10.D
VII.A.1: CH-5.1.A
VII.A.2: CH-5.1.A
VII.A.3: CH-5.5.B
VII.B.1: CH-5.2.A
VII.B.2: CH-5.6.B
VII.C.1: CH-5.7.A
VII.C.2: CH-5.7.A
VII.D.1: CH-5.5.A
VII.D.2: CH-5.6.A
VII.E.1: CH-5.11.A
VII.E.2: CH-5.11.A
VII.F.1: PC-22.2.D OR-9.1.C
VIII.A.1: CH-7.1.A CH-3.3.B
VIII.B.1: CH-7.1.A
VIII.C.1: CH-7.7.A
VIII.C.2: CH-7.11.A
VIII.D.1: CH-7.5.A
VIII.D.2: CH-7.6.A
VIII.D.3: CH-7.6.A
VIII.E.1: CH-7.9.A
VIII.F.1: CH-9.5.A
VIII.F.2: CH-9.9.B
VIII.G.1: CH-8.3.A
VIII.G.2: CH-8.8.A
VIII.G.3: CH-7.5.B
IX.A.1: CH-0.1.A
IX.A.2: CH-3.9.A
IX.B.1: CH-3.8.A
IX.B.2: CH-0.2.D
IX.B.3: CH-5.2.A
IX.C.1: CH-0.4.C IN-2.2.A
IX.D.1: CH-5.2.C
IX.E.1: CH-4.5.C
IX.E.2: CH-4.7.B
IX.E.3: CH-3.12.B
IX.E.4: CH-1.2.B
IX.F.1: CH-0.6.A
IX.F.2: CH-3.7.B
IX.G.1: CH-0.2.C
IX.G.2: CH-0.6.A
IX.G.3: CH-0.6.B
IX.G.4: CH-3.13.A AN-5.1.C
IX.H.1: CH-0.6.C
IX.H.2: CH-0.6.C
IX.H.3: CH-0.6.D
IX.H.4: CH-0.6.C
IX.H.5: CH-0.6.E
X.A.1: CH-3.5.A
X.A.2: CH-4.3.A CH-3.8.A
X.B.1: CH-0.5.A
X.C.1: CH-3.5.A
X.C.2: CH-6.3.A
X.D.1: CH-5.6.A
X.D.2: CH-5.3.B
X.E.1: CH-3.4.A
""")

CITE_ORG = _c("""
I.A.1: PC-13.1.E
I.B.1: DAT-3.1.C
I.B.2: OR-2.1.A DAT-3.1.E OR-8.1.E
I.B.3: OR-1.2.C DAT-3.1.F OR-8.1.E
I.C.1: DAT-3.3.B
I.C.2: DAT-3.5.G
I.D.1: OR-9.2.E
I.D.2: DAT-3.4.C DAT-3.4.D PC-10.1.E
I.E.1: OR-9.2.B CH-4.5.C
I.F: CH-1.10.A
I.G.1: OR-10.1.A OR-4.1.A
II.A.1: ST-1.1.A
II.A.2: CH-2.7.B
II.B.1: DAT-3.5.G
II.C.1: CH-2.2.A
II.C.2: OR-1.2.B DAT-3.5.F
II.D.1: OR-9.1.E
II.E.1: CH-2.7.C DAT-3.5.G
II.E.2: OR-9.1.G OR-7.1.A
II.E.3: CH-2.8.A
II.F.1: DAT-3.5.G
II.F.2: DAT-3.5.E
II.G: CH-2.4.A
III.A.1: DAT-3.4.A ST-1.1.A
III.A.2: DAT-3.5.C OR-1.1.B
III.A.3: MT-1.1.C IA-5.1.A
III.B.1: CH-2.7.A
III.B.2: DAT-3.5.D
III.C.1: PC-15.3.B
III.D.1: PC-17.1.E
III.D.2: DAT-3.4.E CO-14.1.D
III.E.1: DAT-3.5.D
III.E.2: OR-9.1.B
III.E.3: DAT-3.2.A DAT-3.1.G
III.E.4: OR-3.1.B
III.E.5: PC-17.1.F
III.F.1: DAT-3.2.J
III.G: CH-3.2.A
IV.A.1: DAT-3.4.A
IV.A.2: DAT-3.4.A DAT-3.1.F
IV.A.3: CH-3.1.A
IV.B.1: BI-2.4.A
IV.B.2: BI-1.5.A
IV.C.1: CH-5.5.A
IV.D.1: DAT-3.1.F
IV.D.2: OR-9.2.A
IV.E.1: DAT-3.1.F
IV.E.2: DAT-3.1.F OR-1.2.C
V.A.1: DAT-3.2.I
V.A.2: OR-9.2.B CH-4.5.C
V.A.3: DAT-3.4.B
V.A.4: DAT-3.2.I
V.B.1: CH-6.7.A
V.C.1: DAT-3.1.A
V.C.2: ST-2.2.A DAT-3.5.E
V.D.1: OR-9.2.F OR-8.1.G
V.D.2: OR-1.2.C OR-6.1.A OR-6.1.D
V.D.3: DAT-3.1.D OR-9.1.E
V.D.4: OR-9.2.A
V.E.1: OR-3.1.A OR-4.1.A OR-5.1.A
V.E.2: PC-22.2.D DAT-3.1.F
V.F.1: OR-2.1.B DAT-3.2.B
V.F.2: OR-2.1.A
VI.A.1: CH-6.8.B
VI.A.2: DAT-3.1.H
VI.B.1: CH-5.6.A
VI.C.1: DAT-3.1.D
VI.C.2: OR-9.1.G
VI.D.1: CH-6.7.A
VI.E.1: CH-3.10.A
VI.F.1: CH-4.7.B
VI.G.1: CH-6.7.A
VI.H: CH-9.1.A
VI.I: CH-1.10.D
VII.A.1: OR-9.1.C
VII.B.1: OR-9.1.D
VII.C.1: DAT-3.1.H OR-8.1.F
VII.C.2: DAT-3.2.J
VII.C.3: DAT-3.1.B OR-8.1.A OR-8.1.E
VII.D.1: OR-8.1.A
VII.E.1: CH-5.11.A
VII.F.1: OR-9.1.C PC-22.2.D
VII.F.2: DAT-3.5.H OR-9.1.C OR-8.1.G
VIII.A.1: CH-7.5.A OR-9.2.C
VIII.B.1: CH-7.1.A
VIII.C.1: OR-9.1.A DAT-3.5.E
VIII.C.2: DAT-3.3.A OR-1.2.A
VIII.D.1: OR-1.2.A
VIII.E.1: OR-9.2.C
VIII.F: CH-9.5.A
VIII.G.1: DAT-3.3.C OR-8.1.F
IX.A.1: OR-9.2.D
IX.A.2: DAT-3.4.F
IX.A.3: OR-9.2.D
IX.B.1: DAT-3.5.A
IX.C.1: DAT-3.4.F
IX.C.2: PC-17.1.F
IX.D: CH-1.2.B
IX.E: CH-0.6.B
IX.F: CH-0.6.A
X.A.1: DAT-3.4.B DAT-3.4.F
X.B.1: CH-4.5.C
X.C: CH-3.5.A
X.D: CH-5.3.B
""")

CITE_INORG = _c("""
I.A.1: PT-1.1.A CH-0.4.A
I.A.2: IA-2.1.B PC-13.1.E
I.B.1: CH-1.9.A PC-12.1.B
I.B.2: CH-1.9.A
I.B.3: CH-1.5.C IA-15.1.A
I.B.4: IA-15.1.A CH-1.5.C
I.B.5: CH-1.5.B IN-3.1.B IA-15.4.B
I.B.6: IN-2.1.A PT-2.2.A
I.C.1: CH-1.7.A IA-15.1.A
I.C.2: CH-1.8.B
I.C.3: IN-2.2.B CH-0.4.C
I.D.1: CH-3.12.B
I.D.2: IN-5.2.A
I.E.1: CH-4.5.C
I.F.1: CH-1.10.A
I.G.1: CH-1.5.A
I.G.2: CH-1.7.D IA-5.1.B
II.A.1: CH-2.1.A
II.A.2: IN-3.1.C
II.A.3: CH-2.3.A
II.A.4: IA-14.1.A IA-4.1.A
II.B.1: CH-2.8.A IA-7.1.A
II.B.2: CH-8.6.B
II.B.3: CH-2.2.B
II.C.1: CH-2.7.C
II.C.2: CH-2.2.B IA-15.2.A
II.C.3: IN-3.1.C IA-10.1.B IA-15.3.I
II.D.1: IA-5.1.B
II.D.2: PC-13.1.F
II.E.1: CH-2.8.A
II.E.2: CH-2.8.A
II.E.3: IA-7.1.A
II.E.4: PC-17.1.E
II.E.5: IA-10.1.C
II.F.1: CH-2.5.B
II.F.2: CH-2.7.C
II.F.3: IA-5.1.B
II.G.1: CH-2.4.A
II.G.2: PC-6.1.F MT-2.1.B IA-15.2.C
II.G.3: IA-15.2.C
II.G.4: IA-15.2.D
III.A.1: CH-8.6.B
III.A.2: IN-3.2.B IN-3.1.D
III.A.3: IA-14.1.A
III.A.4: IA-4.1.A
III.A.5: IA-5.1.C
III.B.1: CH-2.7.A IA-8.1.A
III.B.2: IA-4.1.A
III.C.1: PC-15.3.B
III.D.1: PC-17.1.B IA-15.1.B
III.D.2: IA-15.2.D
III.D.3: PC-17.1.E
III.D.4: PC-17.1.E
III.D.5: IA-15.1.B
III.E.1: IA-15.1.E IN-5.1.B
III.E.2: IN-3.2.A
III.E.3: IA-15.2.D
III.E.4: IA-15.3.H
III.E.5: IA-15.1.E
III.E.6: IA-15.1.E
III.F.1: IA-14.1.A IN-3.1.D IA-15.1.D
III.F.2: IA-15.1.C
III.F.3: IA-15.1.D
III.G.1: IA-3.1.A CH-1.8.B
III.G.2: IA-3.1.C
III.G.3: IA-12.1.B
III.G.4: IA-4.1.C
III.G.5: IN-2.2.B IA-2.1.A
III.G.6: IA-8.1.A
III.G.7: IA-5.1.B
III.H.1: IN-5.1.C
III.H.2: IN-5.1.E
III.H.3: IA-15.2.B
III.H.4: PC-6.1.G IA-15.2.E
III.H.5: IA-5.1.A
III.H.6: IA-15.2.D
III.H.7: IA-5.1.C
III.H.8: IA-15.2.D
IV.A.1: CH-3.1.B
IV.A.2: IA-15.2.E
IV.B.1: CH-3.1.A
IV.B.2: MT-1.1.C
IV.B.3: BI-1.5.A
IV.C.1: CH-3.1.A
IV.D.1: CH-3.2.A
IV.D.2: CH-3.1.B
IV.D.3: CH-3.3.C
IV.E.1: CH-3.10.A
IV.E.2: MT-3.1.A
IV.E.3: CH-9.6.A
V.A.1: CH-4.9.C IN-4.1.A
V.B.1: IA-14.1.B OR-9.1.G
V.C.1: IA-15.4.D
V.D.1: CH-8.6.B IA-1.1.A IA-15.3.G
V.D.2: CH-4.9.B IA-15.3.B
V.D.3: IA-14.1.B
V.D.4: CH-4.2.B
V.D.5: PC-22.3.I
V.D.6: IA-11.1.A
V.E.1: CH-9.9.A
V.E.2: IA-15.3.I
V.E.3: IN-2.2.B IA-8.1.B
V.F.1: IA-15.2.E
V.F.2: IA-14.2.A
V.F.3: IA-11.2.E IA-11.2.F
V.F.4: IA-15.3.H
V.F.5: IA-15.3.G
V.F.6: IA-15.3.G
V.F.7: IA-8.1.C
V.F.8: IA-15.3.C IA-12.1.B
V.F.9: IA-1.1.A
V.F.10: PC-16.1.E
V.G.1: IA-15.2.E
V.G.2: IA-15.5.A
V.G.3: IA-15.2.E
VI.A.1: CH-9.3.B
VI.A.2: CH-9.5.A
VI.A.3: IA-15.2.A
VI.B.1: CH-5.6.B
VI.B.2: IA-15.3.E
VI.B.3: IA-10.1.D IA-15.3.A
VI.C.1: CH-9.8.A
VI.C.2: CH-6.4.C
VI.D.1: IA-15.2.A
VI.D.2: CH-6.7.A
VI.D.3: CH-8.6.A
VI.D.4: IA-10.1.D
VI.E.1: CH-9.9.B
VI.E.2: CH-2.2.B
VI.F.1: CH-9.8.B
VI.F.2: CH-9.11.A
VI.G.1: CH-6.7.A
VI.H.1: IA-15.3.D
VI.H.2: CH-9.3.A
VI.I.1: CH-1.10.D
VII.A.1: IA-10.1.D
VII.A.2: IA-15.3.E
VII.B.1: CH-5.2.A
VII.C.1: CH-5.6.A
VII.C.2: PC-22.3.D
VII.C.3: IA-15.3.B
VII.C.4: IA-15.3.A
VII.C.5: IA-15.3.E
VII.C.6: IA-15.3.D
VII.D.1: IA-15.3.A
VII.E.1: CH-5.11.A
VII.E.2: PC-22.3.I
VII.F.1: PC-22.2.D
VIII.A.1: IA-14.1.B
VIII.B.1: CH-7.1.A
VIII.C.1: CH-7.11.A AN-3.1.B IA-15.3.F
VIII.D.1: IA-15.3.F
VIII.D.2: IA-1.1.A
VIII.E.1: CH-7.9.A
VIII.F.1: CH-9.9.B
VIII.F.2: CH-8.6.A
VIII.F.3: IA-15.3.F IA-15.3.D
VIII.G.1: CH-7.5.A
VIII.G.2: IA-15.3.G
VIII.G.3: CH-8.7.A
VIII.G.4: IA-15.4.D
IX.A.1: IA-15.4.D
IX.A.2: IA-15.3.E
IX.A.3: IN-5.2.A
IX.A.4: IA-15.4.D
IX.B.1: IA-15.1.F
IX.B.2: IN-5.1.B
IX.B.3: IA-14.2.A
IX.C.1: IA-15.2.E
IX.C.2: AN-5.2.C
IX.D.1: CH-1.3.D
IX.D.2: IN-3.2.B IA-15.4.A
IX.D.3: IA-15.4.C
IX.D.4: IN-4.1.B
IX.D.5: CH-3.11.A
IX.D.6: IN-5.2.A
IX.D.7: IN-3.1.B IA-15.4.B
IX.D.8: IA-15.2.C
IX.E.1: CH-0.2.C
IX.E.2: AN-5.2.C
IX.F.1: AN-5.2.B
IX.F.2: CH-0.6.B
IX.G.1: IA-15.5.A
IX.G.2: IA-15.5.A
IX.G.3: IA-15.5.A
IX.G.4: CH-0.6.C
IX.G.5: OR-9.2.A
X.A.1: PC-6.1.G
X.A.2: PC-6.1.F
X.A.3: IN-3.2.B IA-15.4.A
X.B.1: CH-1.1.A
X.C.1: MT-1.1.A
X.D.1: CH-1.7.A
X.D.2: CH-2.8.A
X.D.3: PC-17.1.A
X.D.4: PC-12.1.B
X.D.5: IA-1.1.B IA-1.1.C
X.D.6: CH-3.3.C CH-8.7.A
X.D.7: IA-15.4.A
X.D.8: IN-5.1.A
X.D.9: CH-5.10.A
""")

MAPS = {"acs-accm-general": (GEN, CITE_GEN), "acs-accm-organic": (ORG, CITE_ORG), "acs-accm-inorganic": (INORG, CITE_INORG)}
