"""ACS Exams Institute Anchoring Concepts Content Map for analytical chemistry (Holme, Bauer, Trate, Reed, Raker &
Murphy, J. Chem. Educ. 2020, ed9b00856; supporting information read in full, Nov 2026, from the PDF Kevin supplied).
Items are its 109 subdisciplinary articulations; titles are our paraphrases, never the map's text. CITE maps each
item to the Library objectives that answer it (no empty lists). Read by scripts/accm_cite2.py."""

ITEMS = [
    ("I.A.1", "Isotopic composition is measurable (ICP-MS)"), ("I.A.2", "Core-level energies scale with nuclear charge (XRF)"),
    ("I.A.3", "Nuclear spin and NMR structure information"), ("I.B.1", "Bond strength and vibrational frequency"),
    ("I.B.2", "Unpaired electrons, paramagnetism and EPR"), ("I.C.1", "Chemically similar elements interfere"),
    ("I.D.1", "Spectroscopy as transitions between quantized levels"), ("I.D.2", "Absorption, emission, scattering and radiationless paths"),
    ("I.D.3", "Beer–Lambert law and its limits"), ("I.D.4", "Spectral regions match kinds of transition; choose λmax"),
    ("I.D.5", "Relaxation routes after excitation; emission ∝ concentration"), ("I.E.1", "Stoichiometry in wet analysis"),
    ("I.E.2", "Units for reporting amount, including ppm and ppb"), ("I.E.3", "Accounting for matter through dilutions"),
    ("I.F.1", "Analysis of radioactive samples"), ("I.G.1", "Conjugate pairs and buffers for pH control"),
    ("I.G.2", "Ion properties in IC, MS, electrophoresis and potentiometry"), ("I.G.3", "Ionic strength and activity coefficients"),
    ("II.A.1", "Solvent ionic strength affects the solute"), ("II.D.1", "Energy to atomize or ionize samples; hard and soft ionization"),
    ("II.E.1", "UV–visible transitions between molecular orbitals"), ("II.F.1", "Bond order and vibrational response"),
    ("III.B.1", "Molecular shape and polarity in analysis"), ("III.D.1", "IR, Raman and NMR selection by structure"),
    ("III.E.1", "Chirality in CD, polarimetry and chiral separations"), ("III.F.1", "Functional groups in spectra and separations"),
    ("III.G.1", "Periodic trends guide method choice"), ("III.H.1", "X-ray diffraction identifies crystals"),
    ("III.H.2", "Microscopy of extended systems"), ("III.H.3", "Thermal analysis (TGA, DSC)"),
    ("IV.A.1", "Intermolecular forces and activity"), ("IV.B.1", "Separation by molecular size"),
    ("IV.C.1", "Intermolecular forces drive extraction and chromatography"), ("IV.C.2", "Normal- versus reverse-phase mechanisms"),
    ("IV.D.1", "Solute–solvent forces and solvatochromic shifts"), ("V.A.1", "Stoichiometric ratios to the analyte and the equivalence point"),
    ("V.A.2", "Mass balance"), ("V.B.1", "Spectroscopy changes states, not species"),
    ("V.B.2", "Reactions that improve detection (tagging)"), ("V.B.3", "Fragmentation in mass spectrometry"),
    ("V.B.4", "Electron transfer at an electrode in voltammetry"), ("V.C.1", "Probes and indicators to follow a titration"),
    ("V.D.1", "Complexation, acid–base, precipitation and redox methods"), ("V.F.1", "Precipitation in qualitative ion analysis"),
    ("V.F.2", "Matching titration conditions and indicator"), ("V.F.3", "Derivatization for GC and detection"),
    ("VI.A.1", "Instruments stimulate and measure a response"), ("VI.B.1", "Energy input matched to the analyte"),
    ("VI.C.1", "Redox cells and electrochemical instruments"), ("VI.D.1", "Calorimetric thermal analysis (DSC)"),
    ("VI.E.1", "Cell potential, standard potentials and Nernst"), ("VI.F.1", "Energy storage devices"),
    ("VII.A.1", "Measurement time scale matched to the process"), ("VII.E.1", "Enzyme and catalytic sensors"),
    ("VIII.A.1", "Tracking equilibria by colour, pH or potential"), ("VIII.B.1", "Dynamic equilibrium"),
    ("VIII.C.1", "Equilibrium calculations and the systematic treatment"), ("VIII.C.2", "Solubility equilibria and complex formation"),
    ("VIII.D.1", "Acid strength, fractional composition and distribution diagrams"), ("VIII.D.2", "Large K for quantitative wet analysis"),
    ("VIII.D.3", "Ksp ranking and the inert-salt effect"), ("VIII.D.4", "Reverse reactions and pK relationships"),
    ("VIII.D.5", "Combining equilibrium constants"), ("VIII.D.6", "Formation and conditional formation constants"),
    ("VIII.E.1", "Le Châtelier reasoning"), ("VIII.E.2", "Common-ion effect"), ("VIII.E.3", "Buffers and Henderson–Hasselbalch"),
    ("VIII.F.1", "Thermodynamics controls equilibrium; Nernst positions"), ("VIII.F.2", "K and ΔG°"),
    ("VIII.F.3", "Temperature dependence of K"), ("VIII.F.4", "Cell potential and ΔG"), ("VIII.F.5", "All equilibria satisfied together"),
    ("VIII.G.1", "Titrations as manipulated equilibria"), ("VIII.G.2", "Partition coefficients in extraction and retention"),
    ("VIII.G.3", "Chromatography as continuous re-equilibration; retention factor"), ("VIII.G.4", "Acid–base equilibria and pH"),
    ("VIII.G.5", "Redox equilibria"), ("IX.A.1", "Detection limit, linear range and sensitivity"),
    ("IX.A.2", "Analyte stability during the method"), ("IX.A.3", "Matrix effects; standard addition and internal standards"),
    ("IX.B.1", "Reading properties from a compound's name"), ("IX.C.1", "Indirect methods: back titration and labelling"),
    ("IX.C.2", "Quantitative conversion and recovery"), ("IX.D.1", "Gravimetric methods"),
    ("IX.D.2", "Spectrometer components and geometries"), ("IX.D.3", "Electroanalytical methods and electrodes"),
    ("IX.D.4", "Mass spectrometry: ionization, analyzers, resolution"), ("IX.D.5", "Choosing and optimizing methods"),
    ("IX.E.1", "Documenting conditions for replication"), ("IX.E.2", "Sample changes in storage"),
    ("IX.E.3", "Representative sampling strategies"), ("IX.F.1", "Traceability, reference materials and primary standards"),
    ("IX.F.2", "Replication and precision"), ("IX.F.3", "Calibration and bracketing standards"),
    ("IX.F.4", "Quality control, error types, glassware tolerance and propagation"), ("IX.F.5", "Statistics: t-tests, regression, outliers"),
    ("IX.G.1", "Waste minimization and cost"), ("IX.G.2", "Laboratory and instrument safety"),
    ("IX.H.1", "Qualitative analysis before quantitative"), ("IX.H.2", "Sample preparation to isolate the analyte"),
    ("IX.H.3", "Interferences, background subtraction and channel selection"), ("IX.H.4", "Specificity can replace separation"),
    ("X.A.1", "Instrument output as particulate information"), ("X.A.2", "Nonlinear fitting (e.g. Michaelis–Menten)"),
    ("X.B.1", "Visualizing how a method encodes molecular information"), ("X.C.1", "Statistical comparison of results"),
    ("X.D.1", "Calibration functions and linear dynamic range"), ("X.D.2", "Reading spectra, chromatograms and voltammograms"),
    ("X.D.3", "Derivative and log plots; removing outliers"),
]


def _c(s):
    out = {}
    for ln in s.strip().split("\n"):
        k, v = ln.split(":", 1)
        out[k.strip()] = v.split()
    return out


CITE = _c("""
I.A.1: CH-1.2.B AN-6.2.C
I.A.2: AN-6.1.D
I.A.3: CO-4.1.C CO-14.1.D IA-15.4.C
I.B.1: PC-13.1.E CO-14.1.C
I.B.2: CH-1.5.B AN-6.1.C
I.C.1: AN-6.1.D
I.D.1: AQ-3.2.A CH-3.13.A
I.D.2: AN-6.1.A AN-6.1.B
I.D.3: CH-3.13.A AN-5.1.A PC-16.1.B BC-10.1.A AN-6.1.B
I.D.4: AQ-3.2.A AN-6.1.D
I.D.5: AN-6.1.A
I.E.1: CH-4.6.A AN-2.1.A
I.E.2: CH-3.7.D
I.E.3: CH-3.7.B
I.F.1: CH-1.10.A NU-7.1.B
I.G.1: CH-8.9.A
I.G.2: AN-6.3.B IA-15.4.D PC-10.1.E
I.G.3: PC-8.1.A PC-8.1.C
II.A.1: PC-8.1.C AN-6.5.C
II.D.1: AN-6.2.B
II.E.1: PC-16.1.B AN-6.1.A
II.F.1: PC-13.1.E CO-14.1.C
III.B.1: CH-2.7.A
III.D.1: AN-6.1.C CO-14.1.D
III.E.1: PC-17.1.F
III.F.1: CO-14.1.C AN-6.3.C
III.G.1: AN-6.1.D
III.H.1: IN-5.2.A PC-6.1.F
III.H.2: IA-15.4.D
III.H.3: AN-6.4.A
IV.A.1: PC-8.1.C
IV.B.1: BC-10.2.B
IV.C.1: CH-3.9.A AN-4.1.B AN-6.3.A
IV.C.2: AN-6.3.A
IV.D.1: CH-3.10.A
V.A.1: CH-4.6.A AN-1.1.A
V.A.2: AN-3.1.B AN-6.5.D
V.B.1: PC-16.1.B
V.B.2: AN-6.3.C
V.B.3: AN-6.2.A
V.B.4: AN-6.4.B
V.C.1: AN-1.2.B CH-8.5.B
V.D.1: AN-1.1.A AN-1.1.B AN-1.1.C AN-1.1.D
V.F.1: CH-4.2.A CH-7.11.C
V.F.2: AN-1.2.B
V.F.3: AN-6.3.C
VI.A.1: AN-5.2.C
VI.B.1: AN-5.2.C AN-6.2.B
VI.C.1: CH-9.8.A
VI.D.1: AN-6.4.A
VI.E.1: CH-9.9.A CO-11.1.C CH-9.11.A
VI.F.1: CH-9.10.A
VII.A.1: CH-9.11.A AN-6.1.A
VII.E.1: BC-4.1.A AN-6.4.B
VIII.A.1: AN-1.2.B CH-8.5.B
VIII.B.1: CH-7.1.A
VIII.C.1: CH-7.4.B AN-6.5.D
VIII.C.2: AN-3.1.A AN-3.1.B
VIII.D.1: CH-8.3.A AN-6.5.A
VIII.D.2: AN-1.1.A AN-6.5.B
VIII.D.3: CH-7.11.B AN-6.5.C
VIII.D.4: CH-7.6.A CH-8.3.D
VIII.D.5: CH-7.6.A
VIII.D.6: IA-15.3.F AN-6.5.B
VIII.E.1: CH-7.9.A
VIII.E.2: AN-3.1.A
VIII.E.3: CH-8.9.A CH-8.8.A
VIII.F.1: CO-11.1.D
VIII.F.2: CH-9.9.B
VIII.F.3: CH-9.12.A
VIII.F.4: CH-9.9.B
VIII.F.5: AN-6.5.D CO-1.1.A
VIII.G.1: AN-1.2.A
VIII.G.2: AN-4.1.A
VIII.G.3: AN-4.1.B
VIII.G.4: CH-8.3.A
VIII.G.5: CO-11.1.D
IX.A.1: AN-6.6.A
IX.A.2: AN-6.6.G
IX.A.3: AN-5.1.B AN-6.6.B
IX.B.1: CH-0.4.C IN-2.2.A
IX.C.1: AN-1.1.A AN-6.3.C
IX.C.2: AN-6.6.C
IX.D.1: AN-2.1.A
IX.D.2: AN-6.1.D
IX.D.3: IA-15.4.D AN-6.4.B
IX.D.4: PC-10.1.E AN-6.2.A
IX.D.5: AN-5.2.C
IX.E.1: CH-0.6.B
IX.E.2: AN-6.6.G
IX.E.3: AN-6.6.D
IX.F.1: AN-6.6.F
IX.F.2: AN-5.2.A AN-5.2.B
IX.F.3: AN-5.1.C
IX.F.4: AN-5.2.B AN-6.6.G
IX.F.5: AN-5.2.A AN-6.6.E
IX.G.1: CH-0.6.D
IX.G.2: CH-0.6.C
IX.H.1: CH-4.2.A
IX.H.2: AN-4.1.A
IX.H.3: AN-6.1.D
IX.H.4: AN-5.2.C
X.A.1: AN-5.2.C
X.A.2: PC-22.3.G BC-4.1.C
X.B.1: AN-5.2.C
X.C.1: AN-6.6.E
X.D.1: AN-5.1.C AN-5.1.B AN-6.6.A
X.D.2: AN-4.1.B CH-8.5.B
X.D.3: AN-6.6.H
""")
assert set(CITE) == {c for c, _ in ITEMS}, set(CITE) ^ {c for c, _ in ITEMS}
