"""Biochemistry framework (BC, Nov 2026): structure in UNITS (written to drills/frameworks/biochemistry.yaml by
scripts/bc_framework.py) and two question types per objective in ADD. Basis: the ASBMB core concepts (Tansey et al.,
BAMBED 2013, five concepts and their 'students should be able to' statements, numbered T1–T18 by us) and the ASBMB
certification-exam learning objectives (1.1–3.5 read); the AAMC MCAT outline (1A–1D, 5A–5E) and the ACS anchoring
concepts as also. Objectives are a house list in Lehninger's order, pitched for a protein-design PhD: folding and
binding energetics, ΔΔG of mutations, enzyme kinetics, bioenergetics, metabolism, nucleic acids and lab methods.
Every number is recomputed by sympy along the defining equation; facts are standard textbook content."""
from opl_dsl import Q

FILE, FRAMEWORK = "bc-biochemistry", "biochemistry"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
R, F = "8.314462618", "96485.33212"
A, P, B, E, EN, M, MT, NA, SG, LB, EV = ("biochem.acid-base", "biochem.proteins", "biochem.binding", "biochem.enzymes",
    "biochem.bioenergetics", "biochem.membranes", "biochem.metabolism", "biochem.nucleic-acids", "biochem.signalling",
    "biochem.methods", "biochem.evolution")


def facts(name, skill, rows, explain, pace="quick"):
    return Q(name, skill, "{{q}}", pace=pace, cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


T = lambda *n: [f"asbmb-core-2013:T{x}" for x in n]
C = lambda *n: [f"asbmb-cert:{x}" for x in n]
MC_ = lambda *n: [f"aamc-mcat-outline:{x}" for x in n]

# unit n: (id, title, std, ideas, {topic n: (title, [(letter, std, do, ek, practice)])})
UNITS = {
 1: ("acid-base", "Water, pH and ionisable groups", MC_("5A"), ["ENERGY"], {
   1: ("Buffers and protonation", [
     ("A", [], "Compute buffer pH or the base:acid ratio of a biological buffer with the Henderson–Hasselbalch equation.", "pH = pKa + log([A⁻]/[HA]); phosphate (pKa 6.86) and bicarbonate (6.1) buffer cells and blood.", "P1"),
     ("B", [], "Compute the fraction of an ionisable side chain protonated at a given pH.", "f(HA) = 1/(1 + 10^(pH − pKa)); His (pKa ≈ 6.0) switches near physiological pH.", "P1")]),
   2: ("Amino-acid and peptide charge", [
     ("A", MC_("1A"), "Find the isoelectric point of an amino acid from its pKa values.", "pI = average of the two pKa values flanking the neutral species.", "P1"),
     ("B", MC_("1A"), "Compute the net charge of a peptide at a given pH from its ionisable groups.", "Sum fractional charges: +1/(1 + 10^(pH − pKa)) for basic groups, −1/(1 + 10^(pKa − pH)) for acidic ones.", "P1")])}),
 2: ("proteins", "Protein structure and folding", T(15, 16) + C("2.1", "2.3", "1.3") + MC_("1A"), ["STRUCTURE", "ENERGY"], {
   1: ("Levels of structure", [
     ("A", C("2.1"), "Relate secondary-structure geometry to length: residues per turn and rise per residue.", "α-helix: 3.6 residues/turn, 1.5 Å rise per residue (5.4 Å pitch); β-strand: about 3.3–3.5 Å per residue.", "P1"),
     ("B", C("2.3"), "Identify the interactions that stabilise a structure and predict the effect of a substitution.", "Hydrophobic burial, hydrogen bonds, salt bridges, disulfides; Pro breaks helices, Gly adds flexibility.", "P2")]),
   2: ("Folding thermodynamics", [
     ("A", T(16) + C("1.3"), "Compute ΔG of folding, the melting temperature and the fraction folded for a two-state protein.", "ΔG_unf = ΔH(1 − T/Tm) (ΔCp neglected); K_fold = e^(−ΔG_fold/RT); f_folded = K/(1 + K).", "P1"),
     ("B", T(16) + C("2.3"), "Convert a mutation's ΔΔG into a change in stability, folding equilibrium constant or fraction unfolded.", "ΔΔG > 0 destabilises; each 5.7 kJ/mol at 298 K is a factor of 10 in K.", "P1"),
     ("C", C("1.3"), "Explain the hydrophobic effect and why folding is not a random search.", "Burying nonpolar groups releases ordered water (entropy gain); Levinthal: a random search would take astronomically long, so folding follows a funnel.", "P2")])}),
 3: ("binding", "Binding, cooperativity and allostery", T(17, 18) + C("2.2") + MC_("1A"), ["STRUCTURE"], {
   1: ("Affinity", [
     ("A", T(17), "Compute fractional saturation and the binding free energy from K_d.", "θ = [L]/(K_d + [L]); ΔG°_bind = RT ln K_d (with K_d in M).", "P1"),
     ("B", T(17), "Compute the ΔΔG of binding between two variants from their K_d values.", "ΔΔG = RT ln(K_d,mut/K_d,wt); a 10-fold loss is +5.7 kJ/mol at 298 K.", "P1")]),
   2: ("Cooperativity and allostery", [
     ("A", T(18), "Use the Hill equation and read cooperativity from n_H.", "θ = Lⁿ/(K₀.₅ⁿ + Lⁿ); going from 10% to 90% saturation needs an 81^(1/n)-fold change in [L].", "P1"),
     ("B", T(18) + C("1.1"), "Explain haemoglobin's cooperativity and its regulation by H⁺, CO₂ and 2,3-BPG.", "T and R states; the Bohr effect and BPG stabilise T, lowering affinity to unload O₂ in tissues; myoglobin binds hyperbolically.", "P2")])}),
 4: ("enzymes", "Enzymes", T(5) + C("1.5", "2.4") + MC_("5E"), ["ENERGY"], {
   1: ("Michaelis–Menten kinetics", [
     ("A", T(5) + C("2.4"), "Compute an initial rate from V_max, K_M and [S].", "v = V_max[S]/(K_M + [S]); v = V_max/2 at [S] = K_M.", "P1"),
     ("B", T(5), "Compute k_cat and catalytic efficiency and compare with the diffusion limit.", "k_cat = V_max/[E]_T; k_cat/K_M approaches 10⁸–10⁹ M⁻¹ s⁻¹ for diffusion-limited enzymes.", "P1"),
     ("C", T(5) + C("2.4"), "Read K_M and V_max from a Lineweaver–Burk plot.", "1/v = (K_M/V_max)(1/[S]) + 1/V_max: y-intercept 1/V_max, x-intercept −1/K_M.", "P1")]),
   2: ("Inhibition", [
     ("A", C("2.4"), "Compute apparent K_M and V_max for competitive, uncompetitive and mixed inhibition.", "α = 1 + [I]/K_I: competitive K_M,app = αK_M; uncompetitive divides both K_M and V_max by α′; mixed scales both.", "P1"),
     ("B", C("2.4"), "Convert an IC₅₀ to K_I for a competitive inhibitor and classify inhibition from data.", "Cheng–Prusoff: K_I = IC₅₀/(1 + [S]/K_M).", "P1")]),
   3: ("Catalytic mechanisms", [
     ("A", C("1.5"), "Relate transition-state stabilisation to rate enhancement, separating it from ΔG of the reaction.", "Enzymes lower ΔG‡, not ΔG; rate enhancement = e^(ΔΔG‡/RT).", "P1"),
     ("B", C("2.4"), "Identify catalytic strategies (acid–base, covalent, metal ion, proximity) in a described mechanism.", "Serine proteases: Ser–His–Asp triad, covalent acyl-enzyme, oxyanion hole stabilises the tetrahedral intermediate.", "P2")])}),
 5: ("bioenergetics", "Bioenergetics", T(6, 7) + C("1.4") + MC_("1D"), ["ENERGY"], {
   1: ("Free energy in the cell", [
     ("A", T(6), "Compute ΔG of ATP hydrolysis at cellular concentrations from ΔG°′ and the mass-action ratio.", "ΔG = ΔG°′ + RT ln([ADP][Pi]/[ATP]); ΔG°′ = −30.5 kJ/mol, cellular ΔG about −50 to −60.", "P1"),
     ("B", T(7) + C("1.4"), "Find the overall ΔG°′ and K′ of a coupled reaction.", "ΔG°′ values add; K′ = e^(−ΔG°′/RT) multiplies.", "P1")]),
   2: ("Redox and chemiosmosis", [
     ("A", T(6), "Compute ΔG°′ of an electron transfer from standard reduction potentials.", "ΔG°′ = −nFΔE°′; NADH → O₂ (ΔE°′ = 1.14 V) releases about 220 kJ/mol.", "P1"),
     ("B", T(8), "Compute the proton-motive force and the free energy per proton moved into the matrix.", "Δp = Δψ − (2.303RT/F)ΔpH (pH_in − pH_out); ΔG per H⁺ = −FΔp.", "P1")])}),
 6: ("membranes", "Membranes and transport", C("2.1") + MC_("5A"), ["ENERGY", "STRUCTURE"], {
   1: ("Transport energetics", [
     ("A", [], "Compute the Nernst equilibrium potential of an ion.", "E = (RT/zF) ln([out]/[in]); about 61.5/z mV per decade at 37 °C.", "P1"),
     ("B", T(8), "Compute the free energy of moving a charged solute across a membrane.", "ΔG = RT ln(c_in/c_out) + zFΔψ (Δψ = ψ_in − ψ_out).", "P1"),
     ("C", C("2.1"), "Distinguish channels, carriers and pumps, and predict how lipid composition changes fluidity.", "Unsaturated and shorter chains raise fluidity; cholesterol buffers it; pumps use ATP, secondary transporters use gradients.", "P2")])}),
 7: ("metabolism", "Metabolism", T(6, 9) + C("1.1", "1.2") + MC_("1D"), ["ENERGY", "REGULATION"], {
   1: ("Glycolysis and gluconeogenesis", [
     ("A", C("1.1"), "Account for the ATP and NADH of glycolysis and name its control points.", "Net 2 ATP and 2 NADH per glucose; hexokinase, PFK-1 (the committed step) and pyruvate kinase are irreversible and regulated.", "P1"),
     ("B", C("1.1", "1.2"), "Explain how gluconeogenesis bypasses glycolysis's irreversible steps and what it costs.", "Pyruvate carboxylase + PEPCK, fructose-1,6-bisphosphatase, glucose-6-phosphatase; 4 ATP + 2 GTP + 2 NADH per glucose.", "P2")]),
   2: ("Oxidative metabolism", [
     ("A", T(6), "Compute the ATP yield of complete glucose oxidation from P/O ratios.", "10 NADH and 2 FADH₂ per glucose (with the shuttle); 2.5 ATP/NADH and 1.5 ATP/FADH₂ give about 30–32 ATP.", "P1"),
     ("B", C("1.2"), "Compute the ATP yield of β-oxidation of a saturated fatty acid.", "C_n: n/2 − 1 rounds (each FADH₂ + NADH), n/2 acetyl-CoA (10 ATP each), minus 2 for activation; palmitate gives 106.", "P1")]),
   3: ("Regulation and nitrogen", [
     ("A", T(9) + C("1.1"), "Predict how insulin, glucagon and allosteric effectors regulate fuel metabolism.", "Insulin: storage (glycogen synthesis, glycolysis); glucagon: mobilisation via cAMP/PKA; F2,6BP couples hormone state to PFK-1.", "P2"),
     ("B", [], "Account for the cost and logic of nitrogen disposal through the urea cycle.", "Urea carries two N (one from NH₄⁺ via carbamoyl phosphate, one from aspartate); 4 high-energy phosphate bonds per urea.", "P2")])}),
 8: ("nucleic-acids", "Nucleic acids and information flow", T(11, 12, 13, 14) + C("3.1", "3.2", "3.3") + MC_("1B", "1C"), ["INFORMATION"], {
   1: ("DNA structure", [
     ("A", T(12), "Use Chargaff's rules to find base composition.", "In double-stranded DNA, A = T and G = C, so %G = (100 − 2·%A)/2.", "P1"),
     ("B", T(12), "Estimate a short duplex's melting temperature and say why GC content raises it.", "Wallace rule for short oligos: Tm ≈ 2(A + T) + 4(G + C) °C; GC pairs stack more strongly (and have three H-bonds).", "P1")]),
   2: ("Mutation and fidelity", [
     ("A", C("3.1") + T(4), "Predict a mutation's effect on the protein: silent, missense, nonsense or frameshift.", "An insertion or deletion that is not a multiple of 3 shifts the reading frame downstream.", "P2"),
     ("B", T(14), "Compute the expected number of replication errors per genome from the error rate.", "Errors = genome length × error rate per base; proofreading and mismatch repair bring E. coli to ~10⁻¹⁰ per base.", "P1")]),
   3: ("Expression and its measurement", [
     ("A", C("3.2", "3.3"), "Predict gene-expression changes from regulatory logic (lac operon, activators, repressors).", "lac is expressed when lactose is present (repressor off) and glucose is low (cAMP–CAP on).", "P2"),
     ("B", [], "Compute PCR amplification and a qPCR fold change by the ΔΔCt method.", "Copies = N₀·2ⁿ at full efficiency; fold change = 2^(−ΔΔCt).", "P1")])}),
 9: ("signalling", "Signalling and regulation", C("3.5") + T(9), ["REGULATION"], {
   1: ("Signal transduction", [
     ("A", C("3.5"), "Compute the amplification of a signalling cascade.", "Gains multiply: each enzyme in a cascade activates many of the next.", "P1"),
     ("B", C("3.5"), "Match a receptor class to its second messenger and downstream kinase.", "GPCR–Gs → adenylyl cyclase → cAMP → PKA; Gq → PLC → IP₃ (Ca²⁺) and DAG (PKC); RTKs autophosphorylate and recruit SH2 proteins.", "P2")])}),
 10: ("methods", "Methods in biochemistry", MC_("5C"), ["MEASURE"], {
   1: ("Quantitation and size", [
     ("A", [], "Compute protein concentration from A₂₈₀ with the Beer–Lambert law.", "A = εcl; ε₂₈₀ ≈ 5500·nW + 1490·nY + 125·(cystines) M⁻¹ cm⁻¹.", "P1"),
     ("B", [], "Estimate a protein's molar mass from SDS-PAGE mobility against standards.", "log M is linear in relative mobility over the gel's range.", "P1")]),
   2: ("Purification", [
     ("A", [], "Compute specific activity, fold purification and yield from a purification table.", "Specific activity = units/mg; fold = SA/SA_crude; yield = units/units_crude.", "P1"),
     ("B", [], "Choose a separation (ion exchange, gel filtration, affinity) from a protein's pI, size or binding.", "Below its pI a protein is positive and binds a cation exchanger; gel filtration elutes large proteins first.", "P2")])}),
 11: ("evolution", "Evolution and homeostasis", T(1, 2, 3, 4, 8, 10) + C("2.5", "3.4", "1.6"), ["INFORMATION", "REGULATION"], {
   1: ("Molecular evolution", [
     ("A", T(2, 3), "Estimate divergence time from sequence differences with a molecular clock.", "t = d/(2r): differences accumulate along both lineages.", "P1"),
     ("B", C("2.5") + T(4), "Judge homology from sequence identity and explain conserved function with changed sequence.", "Above ~30–40% identity over a full domain, proteins are very likely homologous; active-site residues are conserved more than surface ones.", "P2")]),
   2: ("Steady state and control", [
     ("A", T(8, 10), "Use the mass-action ratio to tell near-equilibrium steps from regulated, far-from-equilibrium ones.", "Q/K′ ≈ 1 means near equilibrium (not a control point); Q/K′ ≪ 1 means large negative ΔG, a likely control point.", "P1")])}),
}

IDEAS = [("ENERGY", "Energy is required and transformed", "Free energy, coupling and catalysis decide which processes run and how fast."),
         ("STRUCTURE", "Structure determines function", "Folding and binding energetics set what a macromolecule does."),
         ("INFORMATION", "Information is stored and flows", "Sequence encodes structure; replication, transcription and translation move it."),
         ("REGULATION", "Homeostasis is regulated and far from equilibrium", "Control points, signals and steady states keep cells running."),
         ("MEASURE", "Discovery requires measurement", "Quantitative methods turn molecules into numbers.")]

ADD = [
    # 1.1
    ("BC-1.1.A", Q("bc-hh-ph", A, "A phosphate buffer has [HPO₄²⁻] = {{b}} mM and [H₂PO₄⁻] = {{a}} mM (pKa 6.86). What is the pH?",
        given={"b": {"pick": [10, 20, 40]}, "a": {"pick": [10, 20, 50]}}, value="6.86 + log10(b/a)", tex="pH", verify="Rational(686, 100) + log(Rational(b, a), 10)",
        explain="Henderson–Hasselbalch")),
    ("BC-1.1.A", Q("bc-blood-ratio", A, "Blood pH is {{pH}} and the bicarbonate system's pKa is 6.1. What is the [HCO₃⁻]/[CO₂] ratio?",
        given={"pH": {"pick": [7.4, 7.2, 7.5]}}, value="10^(pH - 6.1)", tex="ratio", verify="10**(nsimplify(pH) - Rational(61, 10))",
        explain="At 7.4 the ratio is 20:1: the buffer works far from its pKa because CO₂ is exhaled and HCO₃⁻ is renal-regulated")),
    ("BC-1.1.B", Q("bc-fraction-protonated", A, "A histidine side chain has pKa {{pKa}}. What fraction is protonated at pH {{pH}}?",
        given={"pKa": {"pick": [6.0, 6.5]}, "pH": {"pick": [5.5, 6.0, 7.4]}}, value="1/(1 + 10^(pH - pKa))", tex="f",
        verify="10**(nsimplify(pKa) - nsimplify(pH))/(1 + 10**(nsimplify(pKa) - nsimplify(pH)))", explain="f = [HA]/([HA] + [A⁻])")),
    ("BC-1.1.B", Q("bc-shifted-pka", A, "An active-site Lys normally has pKa 10.5, but buried in a hydrophobic pocket its pKa falls to {{pk}}. What fraction is neutral at pH {{pH}}?",
        given={"pk": {"pick": [6.0, 7.0, 8.0]}, "pH": {"pick": [7.0, 7.4]}}, value="1/(1 + 10^(pk - pH))", tex="f",
        verify="1 - 1/(1 + 10**(nsimplify(pH) - nsimplify(pk)))", explain="Environment shifts pKa: burial disfavours charge, making the neutral amine a nucleophile")),
    # 1.2
    ("BC-1.2.A", Q("bc-pi", A, "Find the pI of {{aa}} (pKa values {{k1}}, {{k2}}, {{k3}}; the neutral form lies between {{lo}} and {{hi}}).",
        cases=[{"aa": "aspartate", "k1": 1.99, "k2": 3.90, "k3": 9.90, "lo": 1.99, "hi": 3.90}, {"aa": "lysine", "k1": 2.16, "k2": 9.06, "k3": 10.54, "lo": 9.06, "hi": 10.54},
               {"aa": "glutamate", "k1": 2.10, "k2": 4.07, "k3": 9.47, "lo": 2.10, "hi": 4.07}, {"aa": "histidine", "k1": 1.82, "k2": 6.04, "k3": 9.33, "lo": 6.04, "hi": 9.33}],
        value="(lo + hi)/2", tex="pI", verify="(nsimplify(lo) + nsimplify(hi))/2", explain="Average the two pKa values on either side of the zero-charge species")),
    ("BC-1.2.A", Q("bc-pi-glycine", A, "A neutral amino acid has α-carboxyl pKa {{k1}} and α-amino pKa {{k2}}. What is its pI?",
        given={"k1": {"pick": [2.34, 2.0, 2.2]}, "k2": {"pick": [9.6, 9.1, 9.7]}}, value="(k1 + k2)/2", tex="pI",
        verify="solve(Eq(Symbol('ph') - nsimplify(k1), nsimplify(k2) - Symbol('ph')), Symbol('ph'))[0]",
        explain="At the pI the fractional + and − charges cancel, so 10^(pI − pKa₁) = 10^(pKa₂ − pI): the average")),
    ("BC-1.2.B", Q("bc-peptide-charge", A, "A peptide has an N-terminus (pKa 9.0), a C-terminus (pKa 2.0), one Lys (10.5) and {{nd}} Asp (3.9). What is its net charge at pH {{pH}}?",
        given={"nd": {"pick": [1, 2]}, "pH": {"pick": [3.0, 7.0, 11.0]}},
        value="1/(1 + 10^(pH - 9.0)) + 1/(1 + 10^(pH - 10.5)) - 1/(1 + 10^(2.0 - pH)) - nd/(1 + 10^(3.9 - pH))", tex="q",
        verify="1/(1 + 10**(nsimplify(pH) - 9)) + 1/(1 + 10**(nsimplify(pH) - Rational(21, 2))) - 1/(1 + 10**(2 - nsimplify(pH))) - nd/(1 + 10**(Rational(39, 10) - nsimplify(pH)))",
        explain="Sum each group's fractional charge")),
    ("BC-1.2.B", facts("bc-charge-direction", A, [
        ("A protein with pI 5.0 is placed in buffer at pH 7.4. Its net charge is:", "Negative", "Positive", "Zero", "Undefined"),
        ("In electrophoresis at pH 8.6, a protein with pI 9.5 moves toward:", "The cathode (−)", "The anode (+)", "Neither", "The top of the gel"),
        ("Which amino acid side chain is positively charged at pH 7?", "Arginine", "Glutamate", "Serine", "Phenylalanine"),
        ("Which change makes a protein more soluble near its pI?", "Moving the pH away from the pI", "Moving to the pI", "Removing all salt", "Raising the protein concentration"),
    ], "Below the pI a protein is positive, above it negative")),
    # 2.1
    ("BC-2.1.A", Q("bc-helix-length", P, "An α-helix of {{n}} residues: how long is it in Å, and how many turns? (Give the length.)",
        given={"n": {"pick": [12, 18, 24, 36]}}, value="1.5*n", tex="L", verify="Rational(3, 2)*n", explain="1.5 Å rise per residue; turns = n/3.6")),
    ("BC-2.1.A", Q("bc-helix-turns", P, "A transmembrane α-helix must span a {{d}} Å hydrophobic core. About how many residues does it need?",
        given={"d": {"pick": [30, 36, 45]}}, value="d/1.5", tex="n", verify="Rational(d*2, 3)", explain="About 20 residues span the ~30 Å core: a hydrophobic stretch of ~20 flags a TM helix")),
    ("BC-2.1.B", facts("bc-interactions", P, [
        ("Lys and Glu side chains 3 Å apart on a protein surface form a:", "Salt bridge", "Disulfide", "Peptide bond", "Glycosidic bond"),
        ("Which interaction is covalent?", "Disulfide bond", "Hydrogen bond", "Salt bridge", "Hydrophobic interaction"),
        ("Replacing a buried Leu with Asp most likely:", "Destabilises the fold by burying a charge", "Stabilises it", "Has no effect", "Forms a disulfide"),
        ("Pro in the middle of an α-helix tends to:", "Break or kink the helix", "Strengthen it", "Form a disulfide", "Add a charge"),
        ("Replacing Gly in a tight turn with a large residue often:", "Destabilises the turn (Gly allows unusual φ/ψ)", "Has no effect", "Strengthens the turn", "Creates a disulfide"),
    ], "Classify by chemistry; predict substitutions by what they bury, break or add")),
    ("BC-2.1.B", facts("bc-structure-levels", P, [
        ("Hydrogen bonds between backbone C=O and N–H four residues apart define:", "The α-helix", "The β-sheet", "Tertiary structure", "Quaternary structure"),
        ("The arrangement of subunits in haemoglobin is its:", "Quaternary structure", "Primary structure", "Secondary structure", "Tertiary structure"),
        ("The peptide bond is planar because:", "Partial double-bond character from resonance", "Steric clash", "Disulfides", "Hydrophobic effect"),
        ("Which angles describe backbone conformation on a Ramachandran plot?", "φ and ψ", "χ₁ and χ₂", "ω only", "θ and φ"),
    ], "Primary → secondary → tertiary → quaternary")),
    # 2.2
    ("BC-2.2.A", Q("bc-fold-fraction", P, "A two-state protein has ΔH_unf = {{dH}} kJ/mol and Tm = {{Tm}} K (ΔCp ignored). What fraction is folded at {{T}} K?",
        given={"dH": {"pick": [300, 400, 500]}, "Tm": {"pick": [330, 340, 350]}, "T": {"pick": [310, 320, 325]}},
        value=f"1/(1 + exp(-dH*1000*(1 - T/Tm)/({R}*T)))", tex="f",
        verify=f"1/(1 + exp(-(dH*1000 - T*dH*1000/Tm)/(Rational('{R}')*T)))", explain="ΔG_unf = ΔH − TΔS with ΔS = ΔH/Tm; f_folded = 1/(1 + K_unf)")),
    ("BC-2.2.A", Q("bc-fold-dg", P, "ΔH_unf = {{dH}} kJ/mol, Tm = {{Tm}} K. What is ΔG_unf (kJ/mol) at {{T}} K (ΔCp ignored)?",
        given={"dH": {"pick": [300, 400]}, "Tm": {"pick": [330, 350]}, "T": {"pick": [298, 310]}}, value="dH*(1 - T/Tm)", tex="\\Delta G",
        verify="dH - T*Rational(dH, Tm)", explain="Marginal stability: tens of kJ/mol from large, opposing ΔH and TΔS")),
    ("BC-2.2.B", Q("bc-ddg-fraction", P, "A protein is stable by ΔG_unf = {{dg}} kJ/mol at 298 K. A mutation destabilises it by ΔΔG = {{dd}} kJ/mol. What fraction of the mutant is unfolded?",
        given={"dg": {"pick": [20, 25, 30]}, "dd": {"pick": [5, 10, 15, 18]}}, value=f"1/(1 + exp((dg - dd)*1000/({R}*298)))", tex="f_U",
        verify=f"exp(-(dg - dd)*1000/(Rational('{R}')*298))/(1 + exp(-(dg - dd)*1000/(Rational('{R}')*298)))",
        explain="Stability left = ΔG − ΔΔG; K_unf = e^(−ΔG/RT)")),
    ("BC-2.2.B", Q("bc-ddg-k-factor", P, "By what factor does a ΔΔG of {{dd}} kJ/mol change the folding equilibrium constant at 298 K?",
        given={"dd": {"pick": [2, 5.7, 10, 15]}}, value=f"exp(dd*1000/({R}*298))", tex="\\times", verify=f"exp(nsimplify(dd)*1000/(Rational('{R}')*298))",
        explain="Each ~5.7 kJ/mol is a factor of 10")),
    ("BC-2.2.C", facts("bc-hydrophobic", P, [
        ("The hydrophobic effect is driven mainly by:", "The entropy gained when ordered water around nonpolar groups is released", "Strong attraction between nonpolar groups", "Covalent bonding", "Electrostatic repulsion of water"),
        ("Cold denaturation happens because:", "The hydrophobic effect weakens at low temperature", "Proteins freeze solid", "Disulfides break", "pH changes"),
        ("Levinthal's paradox shows that folding:", "Cannot be a random search of all conformations", "Is random", "Takes years", "Needs no energy"),
        ("A folding 'funnel' means:", "Many paths lead downhill in free energy to the native state", "One fixed path", "A flat landscape", "Folding requires ATP always"),
    ], "Folding is guided downhill, largely by burying nonpolar surface")),
    ("BC-2.2.C", Q("bc-levinthal", P, "If each of {{n}} residues could adopt 3 conformations and the chain sampled 10¹³ per second, how many years would a random search take? (Give log₁₀ of the years.)",
        given={"n": {"pick": [100, 150]}}, value="n*log10(3) - 13 - log10(3.156e7)", tex="\\log_{10} t",
        verify="log(3**n/(10**13*Rational('3.156e7')), 10)", explain="3¹⁰⁰ ≈ 5 × 10⁴⁷: far longer than the universe's age, yet proteins fold in ms")),
    # 3.1
    ("BC-3.1.A", Q("bc-theta", B, "K_d = {{Kd}} nM. What fraction of the protein is bound at free ligand {{L}} nM?",
        given={"Kd": {"pick": [1, 10, 100]}, "L": {"pick": [1, 10, 50, 500]}}, value="L/(Kd + L)", tex="\\theta",
        verify="solve(Eq(Kd*Symbol('th'), (1 - Symbol('th'))*L), Symbol('th'))[0]", explain="θ = [L]/(K_d + [L])")),
    ("BC-3.1.A", Q("bc-dg-bind", B, "A ligand binds with K_d = {{m}} × 10^−{{ex}} M at 298 K. What is ΔG°_bind (kJ/mol)?",
        given={"m": {"pick": [1, 2, 5]}, "ex": {"pick": [6, 9, 12]}}, value=f"{R}*298*log(m*10^(-ex))/1000", tex="\\Delta G",
        verify=f"-Rational('{R}')*298*log(1/(m*Rational(1, 10**ex)))/1000", explain="ΔG° = RT ln K_d (= −RT ln K_a): nM binders are about −50 kJ/mol")),
    ("BC-3.1.B", Q("bc-ddg-bind", B, "A mutation raises K_d from {{k1}} nM to {{k2}} nM. What is ΔΔG_bind at 298 K (kJ/mol)?",
        given={"k1": {"pick": [1, 5, 10]}, "k2": {"pick": [50, 100, 1000]}}, value=f"{R}*298*log(k2/k1)/1000", tex="\\Delta\\Delta G",
        verify=f"Rational('{R}')*298*log(Rational(k2, k1))/1000", explain="ΔΔG = RT ln(K_d,mut/K_d,wt)")),
    ("BC-3.1.B", Q("bc-kd-from-ddg", B, "A designed variant improves binding by ΔΔG = −{{dd}} kJ/mol at 298 K. The parent's K_d is {{kd}} µM. What is the variant's K_d (µM)?",
        given={"dd": {"pick": [3, 5.7, 8, 11.4]}, "kd": {"pick": [1, 10, 100]}}, value=f"kd*exp(-dd*1000/({R}*298))", tex="K_d",
        verify=f"kd/exp(nsimplify(dd)*1000/(Rational('{R}')*298))", explain="Each 5.7 kJ/mol is a tenfold gain in affinity")),
    # 3.2
    ("BC-3.2.A", Q("bc-hill-theta", B, "A protein binds with K₀.₅ = {{K}} and Hill coefficient n = {{n}}. What fraction is bound at [L] = {{L}} (same units)?",
        given={"K": {"pick": [26, 10]}, "n": {"pick": [1, 2.8]}, "L": {"pick": [5, 26, 100]}}, value="L^n/(K^n + L^n)", tex="\\theta",
        verify="1/(1 + (Rational(K, L))**nsimplify(n))", explain="Haemoglobin: n ≈ 2.8, P₅₀ ≈ 26 torr")),
    ("BC-3.2.A", Q("bc-hill-range", B, "With Hill coefficient n = {{n}}, by what factor must [L] rise to go from 10% to 90% saturation?",
        given={"n": {"pick": [1, 2, 2.8, 4]}}, value="81^(1/n)", tex="\\times", verify="Integer(9)**(2/nsimplify(n))",
        explain="81-fold for a non-cooperative binder; cooperativity sharpens the switch")),
    ("BC-3.2.B", facts("bc-hemoglobin", B, [
        ("In exercising muscle, lower pH and higher CO₂ make haemoglobin:", "Release O₂ more readily (Bohr effect)", "Bind O₂ more tightly", "Unchanged", "Lose its haem"),
        ("2,3-BPG binds haemoglobin in:", "The central cavity of the T state, lowering O₂ affinity", "The haem pocket", "The R state only", "Myoglobin"),
        ("Fetal haemoglobin binds O₂ more tightly than adult haemoglobin because it:", "Binds 2,3-BPG more weakly", "Has more haem", "Has no Bohr effect", "Is monomeric"),
        ("Myoglobin's O₂-binding curve is hyperbolic because:", "It has one binding site, so no cooperativity", "It has four sites", "It binds BPG", "It is allosteric"),
        ("CO is toxic partly because it:", "Binds haem far more tightly than O₂ and shifts remaining sites toward R", "Lowers pH", "Binds BPG", "Is a gas"),
    ], "T ⇌ R: effectors that stabilise T lower affinity")),
    ("BC-3.2.B", facts("bc-allostery-models", B, [
        ("In the concerted (MWC) model, subunits:", "Switch between T and R together", "Change one at a time", "Never change", "Are independent"),
        ("In the sequential (KNF) model, binding to one subunit:", "Changes neighbours' conformation and affinity", "Switches all at once", "Has no effect", "Releases ligand"),
        ("A Hill coefficient below 1 suggests:", "Negative cooperativity or site heterogeneity", "Strong positive cooperativity", "No binding", "Covalent binding"),
    ], "Models differ in how conformational change spreads")),
    # 4.1
    ("BC-4.1.A", Q("bc-mm-rate", E, "V_max = {{V}} µM/s, K_M = {{Km}} µM. What is v at [S] = {{S}} µM?",
        given={"V": {"pick": [10, 50, 100]}, "Km": {"pick": [5, 20, 100]}, "S": {"pick": [5, 20, 200]}}, value="V*S/(Km + S)", tex="v",
        verify="V/(1 + Rational(Km, S))", explain="Half V_max at [S] = K_M")),
    ("BC-4.1.A", Q("bc-mm-s-for-v", E, "K_M = {{Km}} µM. What [S] gives v = {{f}}% of V_max?",
        given={"Km": {"pick": [10, 50]}, "f": {"pick": [50, 80, 90, 99]}}, value="Km*(f/100)/(1 - f/100)", tex="[S]",
        verify="solve(Eq(Symbol('ss')/(Km + Symbol('ss')), Rational(f, 100)), Symbol('ss'))[0]", explain="90% of V_max needs 9 K_M; 99% needs 99 K_M")),
    ("BC-4.1.B", Q("bc-kcat", E, "V_max = {{V}} µM/s with [E]_T = {{Et}} nM. What is k_cat (s⁻¹)?",
        given={"V": {"pick": [10, 50, 120]}, "Et": {"pick": [10, 50, 100]}}, value="V*1000/Et", tex="k_{cat}", verify="Rational(V*1000, Et)",
        explain="k_cat = V_max/[E]_T; convert µM to nM")),
    ("BC-4.1.B", Q("bc-efficiency", E, "An enzyme has k_cat = {{kc}} s⁻¹ and K_M = {{Km}} µM. What is k_cat/K_M (M⁻¹ s⁻¹)?",
        given={"kc": {"pick": [100, 4000, 10000]}, "Km": {"pick": [10, 25, 100]}}, value="kc/(Km*1e-6)", tex="k_{cat}/K_M",
        verify="kc/(Km*Rational(1, 10**6))", explain="Near 10⁸–10⁹ M⁻¹ s⁻¹ the enzyme is diffusion-limited (catalase, triose phosphate isomerase)")),
    ("BC-4.1.C", Q("bc-lb-km", E, "A Lineweaver–Burk plot has slope {{s}} s and y-intercept {{b}} s/µM (1/v in s/µM, 1/[S] in µM⁻¹). What is K_M (µM)?",
        given={"s": {"pick": [0.5, 2, 5]}, "b": {"pick": [0.01, 0.02, 0.05]}}, value="s/b", tex="K_M",
        verify="nsimplify(s)/nsimplify(b)", explain="Slope = K_M/V_max, intercept = 1/V_max, so K_M = slope/intercept")),
    ("BC-4.1.C", Q("bc-lb-vmax", E, "The y-intercept of a Lineweaver–Burk plot is {{b}} s/µM. What is V_max (µM/s)?",
        given={"b": {"pick": [0.01, 0.02, 0.05, 0.1]}}, value="1/b", tex="V_{max}", verify="1/nsimplify(b)",
        explain="The y-intercept is 1/V_max; the x-intercept is −1/K_M")),
    # 4.2
    ("BC-4.2.A", Q("bc-competitive", E, "K_M = {{Km}} µM. A competitive inhibitor (K_I = {{Ki}} µM) is present at {{I}} µM. What is the apparent K_M?",
        given={"Km": {"pick": [10, 50]}, "Ki": {"pick": [2, 5, 20]}, "I": {"pick": [5, 10, 40]}}, value="Km*(1 + I/Ki)", tex="K_M^{app}",
        verify="Km + Km*Rational(I, Ki)", explain="Competitive: K_M rises by α = 1 + [I]/K_I; V_max is unchanged")),
    ("BC-4.2.A", Q("bc-uncompetitive", E, "V_max = {{V}}. An uncompetitive inhibitor with K_I′ = {{Ki}} µM is at {{I}} µM. What is the apparent V_max?",
        given={"V": {"pick": [100, 60]}, "Ki": {"pick": [5, 10]}, "I": {"pick": [5, 10, 20]}}, value="V/(1 + I/Ki)", tex="V_{max}^{app}",
        verify="V*Ki/(Ki + I)", explain="Uncompetitive divides both V_max and K_M by α′, leaving their ratio unchanged")),
    ("BC-4.2.B", Q("bc-cheng-prusoff", E, "A competitive inhibitor has IC₅₀ = {{ic}} nM in an assay with [S] = {{S}} µM and K_M = {{Km}} µM. What is K_I (nM)?",
        given={"ic": {"pick": [100, 500]}, "S": {"pick": [10, 50]}, "Km": {"pick": [5, 10, 50]}}, value="ic/(1 + S/Km)", tex="K_I",
        verify="solve(Eq(ic, Symbol('ki')*(1 + Rational(S, Km))), Symbol('ki'))[0]", explain="IC₅₀ depends on [S]; K_I does not")),
    ("BC-4.2.B", facts("bc-inhibition-pattern", E, [
        ("Lineweaver–Burk lines cross on the y-axis. Inhibition type?", "Competitive", "Uncompetitive", "Noncompetitive (pure)", "Irreversible"),
        ("The lines are parallel. Type?", "Uncompetitive", "Competitive", "Mixed", "None"),
        ("The lines cross on the x-axis (K_M unchanged, V_max lowered). Type?", "Pure noncompetitive", "Competitive", "Uncompetitive", "Substrate inhibition"),
        ("Adding more substrate fully overcomes inhibition. Type?", "Competitive", "Uncompetitive", "Noncompetitive", "Irreversible"),
        ("Activity doesn't recover after dialysis. The inhibitor is likely:", "Irreversible (covalent)", "Competitive", "Uncompetitive", "Mixed reversible"),
    ], "Read the type from where the lines meet")),
    # 4.3
    ("BC-4.3.A", Q("bc-rate-enhancement", E, "An enzyme lowers ΔG‡ by {{dd}} kJ/mol at 298 K. By what factor does it speed the reaction?",
        given={"dd": {"pick": [20, 40, 60, 80]}}, value=f"exp(dd*1000/({R}*298))", tex="\\times", verify=f"exp(dd*1000/(Rational('{R}')*298))",
        explain="Rate ∝ e^(−ΔG‡/RT); ΔG of the reaction and the equilibrium are untouched")),
    ("BC-4.3.A", facts("bc-catalysis-thermo", E, [
        ("An enzyme changes which of these?", "ΔG‡ (the activation barrier)", "ΔG of the reaction", "The equilibrium constant", "The final ratio of products to reactants"),
        ("Enzymes bind most tightly to:", "The transition state", "The substrate", "The product", "Water"),
        ("Why are transition-state analogues potent inhibitors?", "The enzyme binds the transition state more tightly than the substrate", "They are covalent", "They are large", "They change ΔG"),
        ("An enzyme speeds the forward reaction 10⁶-fold. The reverse reaction is sped:", "10⁶-fold too", "Not at all", "10³-fold", "It is slowed"),
    ], "Catalysts lower barriers in both directions")),
    ("BC-4.3.B", facts("bc-catalytic-strategies", E, [
        ("In chymotrypsin, Ser195 attacks the substrate to form an acyl-enzyme. Strategy:", "Covalent catalysis", "Metal-ion catalysis", "Proximity only", "Electrostatic repulsion"),
        ("His57 shuttles a proton in the catalytic triad. Strategy:", "General acid–base catalysis", "Covalent catalysis", "Metal-ion catalysis", "Conformational selection"),
        ("Zn²⁺ in carbonic anhydrase lowers water's pKa to make OH⁻. Strategy:", "Metal-ion catalysis", "Covalent catalysis", "Proximity", "Allostery"),
        ("The oxyanion hole stabilises:", "The tetrahedral intermediate's negative charge", "The substrate", "The product", "The Zn²⁺"),
        ("Binding two substrates side by side in the right orientation is:", "Proximity and orientation effects", "Covalent catalysis", "Metal catalysis", "Inhibition"),
    ], "Name the strategy from what each residue or cofactor does")),
    ("BC-4.3.B", facts("bc-catalytic-strategies-2", E, [
        ("Mutating the triad's Asp102 in trypsin mostly:", "Lowers activity by weakening His as a base", "Has no effect", "Raises activity", "Changes specificity only"),
        ("Chymotrypsin cuts after large hydrophobic residues because:", "Its S1 pocket is deep and hydrophobic", "Its triad differs", "It uses Zn²⁺", "It is allosteric"),
        ("Lysozyme strains the substrate toward the transition state. This illustrates:", "Transition-state stabilisation by distortion", "Covalent catalysis only", "Metal catalysis", "Allostery"),
    ], "Specificity and catalysis come from different parts of the active site")),
    # 5.1
    ("BC-5.1.A", Q("bc-atp-dg", EN, "In a cell, [ATP] = {{atp}} mM, [ADP] = {{adp}} mM, [Pi] = {{pi}} mM at 310 K. ΔG°′ = −30.5 kJ/mol. What is ΔG of ATP hydrolysis (kJ/mol)?",
        given={"atp": {"pick": [3, 5, 8]}, "adp": {"pick": [0.25, 0.5, 1]}, "pi": {"pick": [1, 3, 8]}}, value=f"-30.5 + {R}*310*log((adp/1000)*(pi/1000)/(atp/1000))/1000", tex="\\Delta G",
        verify=f"Rational(-61, 2) + Rational('{R}')*310*log(nsimplify(adp)*nsimplify(pi)/(atp*1000))/1000", explain="ΔG = ΔG°′ + RT ln Q with concentrations in M: far more negative than −30.5")),
    ("BC-5.1.A", Q("bc-atp-ratio-needed", EN, "For ATP hydrolysis to release {{dg}} kJ/mol at 310 K (ΔG°′ = −30.5), what mass-action ratio [ADP][Pi]/[ATP] (in M) is needed?",
        given={"dg": {"pick": [50, 55, 60]}}, value=f"exp((-dg + 30.5)*1000/({R}*310))", tex="Q",
        verify=f"exp((Rational(61, 2) - dg)*1000/(Rational('{R}')*310))", explain="The cell holds ATP far from equilibrium")),
    ("BC-5.1.B", Q("bc-coupled-dg", EN, "Glucose + Pi → glucose-6-P has ΔG°′ = +13.8 kJ/mol; ATP hydrolysis −30.5. What is ΔG°′ for glucose + ATP → G6P + ADP? And its K′ at 298 K? (Give K′.)",
        given={"z": {"pick": [1]}}, value=f"z*exp(16.7*1000/({R}*298))", tex="K'", verify=f"z*exp(-(Rational(138, 10) - Rational(305, 10))*1000/(Rational('{R}')*298))",
        explain="ΔG°′ = 13.8 − 30.5 = −16.7 kJ/mol; K′ = e^(16 700/RT) ≈ 850")),
    ("BC-5.1.B", Q("bc-coupling-k", EN, "Reaction A has K′ = {{ka}} and reaction B has K′ = {{kb}}. What is K′ for A + B?",
        given={"ka": {"pick": [0.001, 0.01]}, "kb": {"pick": [1e5, 2e5]}}, value="ka*kb", tex="K'",
        verify=f"exp(-(-Rational('{R}')*298*log(nsimplify(ka)) - Rational('{R}')*298*log(nsimplify(kb)))/(Rational('{R}')*298))",
        explain="ΔG°′ add, so K′ multiply")),
    # 5.2
    ("BC-5.2.A", Q("bc-redox-dg", EN, "Electrons pass from {{don}} (E°′ = {{e1}} V) to {{acc}} (E°′ = {{e2}} V), n = 2. What is ΔG°′ (kJ/mol)?",
        cases=[{"don": "NADH", "e1": -0.32, "acc": "O₂", "e2": 0.816}, {"don": "succinate (FADH₂)", "e1": 0.031, "acc": "O₂", "e2": 0.816},
               {"don": "NADH", "e1": -0.32, "acc": "ubiquinone", "e2": 0.045}, {"don": "NADH", "e1": -0.32, "acc": "pyruvate → lactate", "e2": -0.185}],
        value=f"-2*{F}*(e2 - e1)/1000", tex="\\Delta G", verify=f"-2*Rational('{F}')*(nsimplify(e2) - nsimplify(e1))/1000",
        explain="ΔG°′ = −nFΔE°′: NADH → O₂ releases about 220 kJ/mol")),
    ("BC-5.2.A", Q("bc-redox-atp", EN, "If the {{dg}} kJ/mol released by NADH → O₂ drives ATP synthesis needing about 50 kJ/mol under cell conditions, what is the maximum ATP per NADH?",
        given={"dg": {"pick": [220]}}, value="floor(dg/50)", tex="n", final=True, verify="floor(Rational(dg, 50))",
        explain="Up to 4 thermodynamically; the measured P/O of 2.5 reflects proton stoichiometry, not energy alone")),
    ("BC-5.2.B", Q("bc-pmf", EN, "A mitochondrion has Δψ = {{psi}} mV (matrix negative) and pH_in − pH_out = {{dph}} at 310 K. What is the proton-motive force magnitude (mV)?",
        given={"psi": {"pick": [140, 160, 180]}, "dph": {"pick": [0.5, 0.75, 1.0]}}, value=f"psi + 2.302585093*{R}*310/{F}*1000*dph", tex="\\Delta p",
        verify=f"psi + log(10)*Rational('{R}')*310/Rational('{F}')*1000*nsimplify(dph)", explain="Both the electrical and the pH terms push H⁺ inward; about 61.5 mV per pH unit at 37 °C")),
    ("BC-5.2.B", Q("bc-pmf-dg", EN, "Δp = {{dp}} mV. What free energy (kJ/mol) is released per mole of H⁺ flowing back into the matrix?",
        given={"dp": {"pick": [180, 200, 220]}}, value=f"{F}*dp/1e6", tex="\\Delta G", verify=f"Rational('{F}')*dp/10**6",
        explain="ΔG = −FΔp: about 20 kJ/mol per proton, so ATP synthesis needs several protons")),
    # 6.1
    ("BC-6.1.A", Q("bc-nernst", M, "At 310 K, [{{ion}}]_out = {{co}} mM and [{{ion}}]_in = {{ci}} mM (z = {{z}}). What is its Nernst potential (mV)?",
        cases=[{"ion": "K⁺", "co": 5, "ci": 140, "z": 1}, {"ion": "Na⁺", "co": 145, "ci": 12, "z": 1}, {"ion": "Ca²⁺", "co": 2, "ci": 0.0001, "z": 2}, {"ion": "Cl⁻", "co": 110, "ci": 10, "z": -1}],
        value=f"1000*{R}*310/(z*{F})*log(co/ci)", tex="E", verify=f"1000*Rational('{R}')*310/(z*Rational('{F}'))*log(nsimplify(co)/nsimplify(ci))",
        explain="E = (RT/zF) ln(out/in): K⁺ about −89 mV, Na⁺ about +67 mV")),
    ("BC-6.1.A", Q("bc-nernst-ratio", M, "What concentration ratio out/in gives a Nernst potential of {{E}} mV for a monovalent cation at 310 K?",
        given={"E": {"pick": [-90, -60, 60]}}, value=f"exp(E/1000*{F}/({R}*310))", tex="ratio", verify=f"exp(Rational(E, 1000)*Rational('{F}')/(Rational('{R}')*310))",
        explain="Each 61.5 mV is a tenfold gradient at 37 °C")),
    ("BC-6.1.B", Q("bc-transport-dg", M, "What is ΔG (kJ/mol) to move Na⁺ out of a cell ([in] = {{ci}} mM, [out] = {{co}} mM) against a membrane potential of {{psi}} mV (inside negative) at 310 K?",
        given={"ci": {"pick": [10, 15]}, "co": {"pick": [140, 145]}, "psi": {"pick": [-60, -70]}}, value=f"({R}*310*log(co/ci) - {F}*psi/1000)/1000", tex="\\Delta G",
        verify=f"(Rational('{R}')*310*log(Rational(co, ci)) + 1*Rational('{F}')*(0 - Rational(psi, 1000)))/1000",
        explain="Chemical term RT ln(c_out/c_in) plus electrical term zF(ψ_out − ψ_in): both uphill, hence the Na⁺/K⁺ pump")),
    ("BC-6.1.B", Q("bc-glucose-gradient", M, "SGLT1 couples 2 Na⁺ entering (each releasing {{gna}} kJ/mol) to glucose entry. What maximum glucose gradient in/out can it build at 310 K?",
        given={"gna": {"pick": [10, 12, 15]}}, value=f"exp(2*gna*1000/({R}*310))", tex="ratio", verify=f"exp(2*gna*1000/(Rational('{R}')*310))",
        explain="Secondary active transport: the Na⁺ gradient pays for the glucose gradient")),
    ("BC-6.1.C", facts("bc-membranes", M, [
        ("Which change increases membrane fluidity?", "More unsaturated (cis) fatty acid chains", "Longer saturated chains", "Lower temperature", "Fewer double bonds"),
        ("Cholesterol in membranes:", "Buffers fluidity: less fluid when warm, more fluid when cold", "Always increases fluidity", "Always decreases fluidity", "Has no effect"),
        ("A transporter that moves glucose down its gradient without ATP is:", "Facilitated diffusion (a uniporter, GLUT)", "A primary pump", "A channel for ions only", "Simple diffusion"),
        ("The Na⁺/K⁺-ATPase moves per ATP:", "3 Na⁺ out and 2 K⁺ in", "2 Na⁺ out and 3 K⁺ in", "1 Na⁺ out", "No ions"),
        ("Channels differ from carriers in that channels:", "Open a pore and move ions much faster, without binding-and-flipping", "Need ATP", "Saturate at low concentration", "Move glucose"),
    ], "Composition sets fluidity; energy source sets the transport class")),
    ("BC-6.1.C", facts("bc-membranes-2", M, [
        ("Which lipid forms the bilayer's two leaflets?", "Phospholipids with polar heads outward and tails inward", "Triglycerides", "Free fatty acids only", "Cholesterol only"),
        ("A protein spans the bilayer with a ~20-residue hydrophobic helix. It is:", "An integral membrane protein", "A peripheral protein", "A soluble enzyme", "A lipid"),
        ("Ouabain blocks the Na⁺/K⁺-ATPase. A direct effect is:", "The Na⁺ gradient runs down, slowing Na⁺-coupled transport", "Faster glucose uptake", "Higher membrane potential", "No effect"),
    ], "Membranes are fluid mosaics with gradients maintained by pumps")),
    # 7.1
    ("BC-7.1.A", Q("bc-glycolysis-atp", MT, "Under anaerobic conditions, how many net ATP does a cell gain from {{n}} glucose molecules through glycolysis and lactate fermentation?",
        given={"n": {"pick": [1, 5, 10]}}, value="2*n", tex="ATP", final=True, verify="n*(4 - 2)", explain="4 made, 2 invested; NADH is reoxidised making lactate, so no extra ATP")),
    ("BC-7.1.A", facts("bc-glycolysis-control", MT, [
        ("The committed step of glycolysis is catalysed by:", "Phosphofructokinase-1", "Hexokinase", "Aldolase", "Enolase"),
        ("High ATP and citrate signal:", "Inhibition of PFK-1", "Activation of PFK-1", "No change", "Activation of pyruvate kinase"),
        ("Fructose-2,6-bisphosphate:", "Activates PFK-1 and inhibits fructose-1,6-bisphosphatase", "Inhibits PFK-1", "Is a glycolytic intermediate", "Is made in mitochondria"),
        ("Which glycolytic step produces NADH?", "Glyceraldehyde-3-phosphate dehydrogenase", "Hexokinase", "PFK-1", "Pyruvate kinase"),
        ("Why must NAD⁺ be regenerated in anaerobic cells?", "Glycolysis stops at GAPDH without it", "To make ATP directly", "To make glucose", "To make O₂"),
    ], "Regulation sits at the irreversible steps")),
    ("BC-7.1.B", facts("bc-gluconeogenesis", MT, [
        ("Which enzyme pair bypasses pyruvate kinase?", "Pyruvate carboxylase and PEP carboxykinase", "Hexokinase and glucokinase", "PFK-1 and aldolase", "Enolase and GAPDH"),
        ("Glucose-6-phosphatase is absent from muscle, so muscle:", "Cannot release free glucose into blood", "Makes extra glucose", "Has no glycogen", "Cannot do glycolysis"),
        ("Acetyl-CoA activates pyruvate carboxylase. This links:", "Abundant fat-derived acetyl-CoA to making glucose", "Glycolysis to fermentation", "Urea to TCA", "Nothing"),
        ("Why can't animals make net glucose from even-chain fatty acids?", "Acetyl-CoA can't be converted to pyruvate or net oxaloacetate", "They lack enzymes for fat breakdown", "Fatty acids are toxic", "They can"),
    ], "Gluconeogenesis reverses glycolysis except at three irreversible steps")),
    ("BC-7.1.B", Q("bc-gng-cost", MT, "Making one glucose from 2 pyruvate costs 4 ATP and 2 GTP. How many high-energy phosphate bonds for {{n}} glucose?",
        given={"n": {"pick": [1, 3, 10]}}, value="6*n", tex="n", final=True, verify="n*(4 + 2)",
        explain="Versus 2 ATP gained by glycolysis: running both at once would waste energy, hence reciprocal regulation")),
    ("BC-7.2.A", Q("bc-glucose-atp", MT, "Per glucose, oxidation yields 10 NADH and 2 FADH₂ plus 4 ATP/GTP by substrate-level phosphorylation. With P/O = {{pn}} for NADH and {{pf}} for FADH₂, what is the total ATP?",
        given={"pn": {"pick": [2.5, 3]}, "pf": {"pick": [1.5, 2]}}, value="10*pn + 2*pf + 4", tex="ATP", verify="10*nsimplify(pn) + 2*nsimplify(pf) + 4",
        explain="With 2.5 and 1.5: 32 (30 if cytosolic NADH enters via the glycerol-3-phosphate shuttle)")),
    ("BC-7.2.A", facts("bc-tca", MT, [
        ("Per acetyl-CoA, the citric acid cycle yields:", "3 NADH, 1 FADH₂, 1 GTP and 2 CO₂", "2 NADH and 2 ATP", "1 NADH only", "No reduced carriers"),
        ("Which TCA enzyme is part of the electron transport chain?", "Succinate dehydrogenase (Complex II)", "Citrate synthase", "Aconitase", "Fumarase"),
        ("Oxygen's role in oxidative phosphorylation is:", "Final electron acceptor at Complex IV", "Proton pump", "ATP synthase subunit", "A TCA substrate"),
        ("Uncouplers such as DNP:", "Dissipate the proton gradient, so O₂ use continues without ATP synthesis", "Block Complex IV", "Inhibit ATP synthase directly", "Make more ATP"),
        ("Oligomycin blocks ATP synthase. Electron transport then:", "Slows, because the proton gradient builds up", "Speeds up", "Is unaffected", "Reverses"),
    ], "The cycle makes carriers; the chain turns them into a gradient")),
    ("BC-7.2.B", Q("bc-beta-ox", MT, "Net ATP from complete oxidation of a saturated C{{n}} fatty acid (P/O 2.5 and 1.5; 10 ATP per acetyl-CoA; 2 ATP for activation)?",
        given={"n": {"pick": [12, 14, 16, 18]}}, value="(n/2 - 1)*(1.5 + 2.5) + (n/2)*10 - 2", tex="ATP", final=True,
        verify="(Rational(n, 2) - 1)*4 + Rational(n, 2)*10 - 2", explain="Palmitate (C16): 7 rounds × 4 + 8 × 10 − 2 = 106")),
    ("BC-7.2.B", Q("bc-beta-rounds", MT, "How many rounds of β-oxidation and how many acetyl-CoA come from a saturated C{{n}} fatty acid? (Give the rounds.)",
        given={"n": {"pick": [10, 16, 20, 24]}}, value="n/2 - 1", tex="n", final=True, verify="Rational(n, 2) - 1",
        explain="Each round removes 2 carbons; the last round yields two acetyl-CoA, so n/2 acetyl-CoA from n/2 − 1 rounds")),
    ("BC-7.3.A", facts("bc-hormones", MT, [
        ("High insulin promotes:", "Glycogen synthesis and glycolysis", "Glycogen breakdown", "Gluconeogenesis", "Lipolysis"),
        ("Glucagon acts on liver through:", "cAMP and protein kinase A", "Insulin receptor tyrosine kinase", "Ca²⁺ only", "Nuclear receptors"),
        ("PKA phosphorylates glycogen phosphorylase kinase, leading to:", "Glycogen breakdown", "Glycogen synthesis", "Glycolysis only", "Fat synthesis"),
        ("In the fasted state the liver mainly:", "Releases glucose from glycogen and gluconeogenesis", "Stores glucose", "Makes fat", "Burns glucose only"),
        ("Malonyl-CoA inhibits carnitine acyltransferase I. Its effect:", "Fatty acids are not oxidised while they are being made", "Fat oxidation rises", "Nothing", "Glycolysis stops"),
    ], "Hormones switch the same pathways between storage and mobilisation")),
    ("BC-7.3.A", facts("bc-regulation-levels", MT, [
        ("ATP inhibiting PFK-1 by binding a site other than the active site is:", "Allosteric regulation", "Covalent modification", "Gene regulation", "Compartmentation"),
        ("Phosphorylation switching glycogen synthase off is:", "Covalent modification", "Allosteric regulation", "Proteolysis", "Compartmentation"),
        ("Fatty acid synthesis in cytosol and oxidation in mitochondria is:", "Compartmentation", "Allostery", "Proteolytic activation", "Substrate availability"),
        ("Pepsinogen becoming pepsin is:", "Proteolytic cleavage (zymogen activation)", "Allostery", "Gene regulation", "Phosphorylation"),
    ], "Levels of control differ in speed and permanence")),
    ("BC-7.3.B", Q("bc-urea-cost", MT, "Each urea costs 4 high-energy phosphate bonds and disposes of 2 N. How many high-energy bonds to dispose of {{n}} mol of N?",
        given={"n": {"pick": [2, 10, 30]}}, value="2*n", tex="n", final=True, verify="Rational(4, 2)*n", explain="3 ATP, one of them cleaved to AMP + PPi: 4 phosphate bonds per urea")),
    ("BC-7.3.B", facts("bc-urea", MT, [
        ("The two nitrogens of urea come from:", "NH₄⁺ (via carbamoyl phosphate) and aspartate", "Two glutamates", "Two ammonias", "Arginine side chain only"),
        ("The urea cycle's first steps occur in:", "Mitochondria", "Cytosol only", "Nucleus", "Lysosome"),
        ("A urea-cycle enzyme deficiency causes:", "Hyperammonaemia", "Hypoglycaemia only", "Low ammonia", "Nothing"),
        ("Fumarate from the urea cycle links it to:", "The citric acid cycle", "Glycolysis", "Fatty acid synthesis", "The pentose phosphate pathway"),
    ], "Nitrogen leaves as urea, linked to the TCA cycle by fumarate")),
    # 8.1
    ("BC-8.1.A", Q("bc-chargaff", NA, "Double-stranded DNA is {{a}}% adenine. What percent is guanine?",
        given={"a": {"pick": [20, 22, 30, 35]}}, value="(100 - 2*a)/2", tex="\\%G", verify="solve(Eq(2*a + 2*Symbol('gg'), 100), Symbol('gg'))[0]",
        explain="A = T and G = C, so A + G = 50%")),
    ("BC-8.1.A", Q("bc-gc-content", NA, "A genome region is {{at}}% A + T. What is its GC content (%) and its %C? (Give %C.)",
        given={"at": {"pick": [40, 50, 60, 70]}}, value="(100 - at)/2", tex="\\%C", verify="Rational(100 - at, 2)", explain="G = C, each half of the GC fraction")),
    ("BC-8.1.B", Q("bc-wallace", NA, "Estimate the Tm (°C) of a short oligonucleotide with {{at}} A/T and {{gc}} G/C bases (Wallace rule).",
        given={"at": {"pick": [8, 10, 12]}, "gc": {"pick": [6, 8, 10]}}, value="2*at + 4*gc", tex="T_m", final=True, verify="2*at + 4*gc",
        explain="Tm ≈ 2(A + T) + 4(G + C): rough, for primers under about 20 nt")),
    ("BC-8.1.B", facts("bc-dna-tm", NA, [
        ("Why does higher GC content raise DNA's Tm?", "GC pairs stack more strongly (and have three H-bonds)", "GC is heavier", "AT pairs are covalent", "GC is charged"),
        ("Adding salt to DNA solution raises Tm because cations:", "Screen the backbone phosphates' repulsion", "Break H-bonds", "Remove water", "Denature DNA"),
        ("Melting DNA raises A₂₆₀ (hyperchromicity) because:", "Unstacked bases absorb more", "Strands get heavier", "Phosphates absorb", "Sugars break"),
    ], "Stacking and electrostatics set duplex stability")),
    ("BC-8.2.A", Q("bc-frameshift", NA, "An insertion of {{k}} nucleotides into a coding exon: does it shift the reading frame? (1 = yes, 0 = no)",
        given={"k": {"pick": [1, 2, 3, 4, 6, 7]}}, value="mod(k, 3) == 0 ? 0 : 1", tex="\\text{shift}", final=True, verify="0 if k % 3 == 0 else 1",
        explain="Only indels that are not multiples of 3 shift the frame")),
    ("BC-8.2.A", facts("bc-mutation-type", NA, [
        ("A codon changes from GAA (Glu) to GAG (Glu). Type:", "Silent", "Missense", "Nonsense", "Frameshift"),
        ("GAA (Glu) to GUA (Val), as in sickle-cell haemoglobin. Type:", "Missense", "Silent", "Nonsense", "Frameshift"),
        ("CAG (Gln) to UAG. Type:", "Nonsense (stop)", "Missense", "Silent", "Frameshift"),
        ("A single base deleted early in the coding sequence. Type:", "Frameshift", "Silent", "Missense", "Nonsense only"),
        ("Why are third-position changes often silent?", "The code is degenerate at the wobble position", "Ribosomes skip them", "They are never read", "They change the tRNA"),
    ], "Read the codon table")),
    ("BC-8.2.B", Q("bc-replication-errors", NA, "A {{g}} × 10⁶ bp genome is copied with an overall error rate of 10^−{{ex}} per base. How many errors per replication are expected?",
        given={"g": {"pick": [4.6, 3200]}, "ex": {"pick": [8, 9, 10]}}, value="g*1e6*10^(-ex)", tex="n",
        verify="nsimplify(g)*10**6*Rational(1, 10**ex)", explain="Errors = length × rate; human cells copy 3.2 × 10⁹ bp, so even 10⁻¹⁰ leaves a few mutations")),
    ("BC-8.2.B", facts("bc-fidelity", NA, [
        ("DNA polymerase's 3′→5′ exonuclease:", "Proofreads, removing a mismatched nucleotide just added", "Builds RNA primers", "Joins fragments", "Unwinds DNA"),
        ("Mismatch repair in E. coli tells the new strand from the old by:", "Hemimethylated GATC sites", "Strand length", "Colour", "Uracil"),
        ("Fidelity improves roughly 10² from proofreading and 10²–10³ from:", "Mismatch repair", "Ligase", "Primase", "Topoisomerase"),
        ("UV light mainly causes:", "Pyrimidine dimers, removed by nucleotide-excision repair", "Deamination only", "Double-strand breaks only", "Methylation"),
    ], "Selection, proofreading and repair multiply fidelity")),
    ("BC-8.3.A", facts("bc-lac-operon", NA, [
        ("Lactose present, glucose absent. lac expression is:", "High (repressor off, CAP–cAMP on)", "Low", "Off", "Constitutive always"),
        ("Lactose absent. lac expression is:", "Off (repressor bound)", "High", "Induced", "Maximal"),
        ("Lactose and glucose both present. Expression is:", "Low (catabolite repression: little cAMP)", "Maximal", "Off entirely", "Unregulated"),
        ("A lacI⁻ mutant (no functional repressor) expresses lac:", "Constitutively, even without lactose", "Never", "Only with glucose", "Only at high temperature"),
        ("The inducer that binds the lac repressor is:", "Allolactose", "Glucose", "cAMP", "Lactose directly"),
    ], "Repressor reads lactose; CAP reads glucose")),
    ("BC-8.3.A", facts("bc-eukaryote-expression", NA, [
        ("Histone acetylation generally:", "Opens chromatin and raises transcription", "Silences genes", "Removes histones", "Has no effect"),
        ("A 5′ cap and poly(A) tail on eukaryotic mRNA help:", "Stability and translation", "Splicing only", "DNA replication", "Degradation"),
        ("Alternative splicing allows:", "Several proteins from one gene", "Faster replication", "No introns", "Prokaryotic expression"),
        ("Enhancers act:", "At a distance, by looping to the promoter through bound activators", "Only next to the start codon", "On mRNA", "On proteins"),
    ], "Eukaryotic expression is regulated at chromatin, transcription, RNA processing and translation")),
    ("BC-8.3.B", Q("bc-pcr", NA, "PCR starts from {{n0}} template copies. After {{c}} cycles at {{eff}}% efficiency, how many copies are there?",
        given={"n0": {"pick": [10, 100, 1000]}, "c": {"pick": [20, 25, 30]}, "eff": {"pick": [100, 90]}}, value="n0*(1 + eff/100)^c", tex="N",
        verify="n0*(1 + Rational(eff, 100))**c", explain="Each cycle multiplies by (1 + efficiency)")),
    ("BC-8.3.B", Q("bc-ddct", NA, "qPCR: target Ct {{t1}} vs reference {{r1}} in treated; target {{t0}} vs reference {{r0}} in control. What is the fold change (2^−ΔΔCt)?",
        given={"t1": {"pick": [22, 24]}, "r1": {"pick": [18]}, "t0": {"pick": [25, 26]}, "r0": {"pick": [18, 19]}}, value="2^(-((t1 - r1) - (t0 - r0)))", tex="FC",
        verify="2**((t0 - r0) - (t1 - r1))", explain="Each cycle earlier means twice the starting template")),
    # 9.1
    ("BC-9.1.A", Q("bc-cascade", SG, "One hormone-bound receptor activates {{a}} G proteins; each activated adenylyl cyclase makes {{b}} cAMP; each PKA phosphorylates {{c}} targets. Assuming each G protein activates one cyclase and 4 cAMP activate one PKA, how many targets are phosphorylated?",
        given={"a": {"pick": [10, 20]}, "b": {"pick": [100, 200]}, "c": {"pick": [10, 50]}}, value="a*b/4*c", tex="n", verify="a*Rational(b, 4)*c",
        explain="Gains multiply down a cascade")),
    ("BC-9.1.A", facts("bc-signal-termination", SG, [
        ("How is a Gs signal switched off?", "The Gα subunit hydrolyses its GTP to GDP", "Receptor degradation only", "Adding more hormone", "ATP synthesis"),
        ("Cholera toxin keeps Gs active by:", "Blocking its GTPase (ADP-ribosylation)", "Activating phosphodiesterase", "Blocking adenylyl cyclase", "Binding cAMP"),
        ("Phosphodiesterase ends cAMP signals by:", "Hydrolysing cAMP to AMP", "Making cAMP", "Phosphorylating PKA", "Binding the receptor"),
        ("Caffeine prolongs cAMP signals by:", "Inhibiting phosphodiesterase", "Activating the receptor", "Making ATP", "Blocking PKA"),
    ], "Amplification is matched by fast switches to turn signals off")),
    ("BC-9.1.B", facts("bc-receptor-classes", SG, [
        ("A Gq-coupled receptor activates phospholipase C, producing:", "IP₃ (Ca²⁺ release) and DAG (PKC)", "cAMP", "cGMP", "NO"),
        ("Insulin's receptor is a:", "Receptor tyrosine kinase", "GPCR", "Ligand-gated ion channel", "Nuclear receptor"),
        ("Steroid hormones mostly act through:", "Intracellular (nuclear) receptors that regulate transcription", "GPCRs", "RTKs", "Ion channels"),
        ("SH2 domains bind:", "Phosphotyrosine motifs", "cAMP", "GTP", "DNA"),
        ("The β-adrenergic receptor couples to:", "Gs → adenylyl cyclase → cAMP", "Gq → PLC", "RTK", "A nuclear receptor"),
    ], "Match receptor, transducer and second messenger")),
    ("BC-9.1.B", facts("bc-receptor-classes-2", SG, [
        ("Nitric oxide signals through:", "Soluble guanylyl cyclase making cGMP", "cAMP", "IP₃", "RTKs"),
        ("Ras is activated when it binds:", "GTP (via a GEF such as SOS)", "GDP", "cAMP", "Ca²⁺"),
        ("Calmodulin is a sensor for:", "Ca²⁺", "cAMP", "DAG", "GTP"),
    ], "Second messengers are small, fast and amplifying")),
    # 10.1
    ("BC-10.1.A", Q("bc-a280", LB, "A protein with {{w}} Trp and {{y}} Tyr (no cystines) reads A₂₈₀ = {{A}} in a 1 cm cuvette. What is its concentration (µM)?",
        given={"w": {"pick": [2, 4, 6]}, "y": {"pick": [5, 10, 15]}, "A": {"pick": [0.3, 0.5, 1.0]}}, value="A/(5500*w + 1490*y)*1e6", tex="c",
        verify="nsimplify(A)/(5500*w + 1490*y)*10**6", explain="ε₂₈₀ from Trp and Tyr content; c = A/(εl)")),
    ("BC-10.1.A", Q("bc-a280-mg", LB, "A protein (M = {{M}} kDa, ε₂₈₀ = {{eps}} M⁻¹ cm⁻¹) gives A₂₈₀ = {{A}} (1 cm). What is its concentration in mg/mL?",
        given={"M": {"pick": [25, 50, 66]}, "eps": {"pick": [30000, 45000]}, "A": {"pick": [0.4, 0.8]}}, value="A/eps*M*1000", tex="c",
        verify="nsimplify(A)/eps*M*1000", explain="Molar concentration × molar mass (g/mol = mg/mmol)")),
    ("BC-10.1.B", Q("bc-sds-mw", LB, "SDS-PAGE standards fit log₁₀(M/kDa) = {{a}} − {{b}}·R_f. A band runs at R_f = {{rf}}. Estimate its mass (kDa).",
        given={"a": {"pick": [2.4, 2.3]}, "b": {"pick": [1.2, 1.5]}, "rf": {"pick": [0.3, 0.5, 0.7]}}, value="10^(a - b*rf)", tex="M",
        verify="10**(nsimplify(a) - nsimplify(b)*nsimplify(rf))", explain="log M is linear in mobility within the gel's range")),
    ("BC-10.1.B", facts("bc-sds-facts", LB, [
        ("SDS-PAGE separates proteins by:", "Size (SDS gives uniform charge per mass)", "Charge", "pI", "Hydrophobicity"),
        ("A protein runs at 50 kDa under reducing SDS-PAGE and 100 kDa without reductant. It is likely:", "A disulfide-linked dimer", "A monomer of 150 kDa", "Degraded", "Glycosylated only"),
        ("Native gel filtration gives 200 kDa but SDS-PAGE gives 50 kDa. The protein is likely:", "A tetramer of non-covalently bound subunits", "A monomer", "Degraded", "Aggregated by disulfides"),
    ], "Compare reducing and non-reducing, denaturing and native measurements")),
    ("BC-10.2.A", Q("bc-purification", LB, "Crude extract: {{u0}} units in {{p0}} mg. After affinity chromatography: {{u1}} units in {{p1}} mg. What is the fold purification?",
        given={"u0": {"pick": [10000, 20000]}, "p0": {"pick": [500, 1000]}, "u1": {"pick": [4000, 6000]}, "p1": {"pick": [2, 5]}}, value="(u1/p1)/(u0/p0)", tex="\\times",
        verify="Rational(u1, p1)/Rational(u0, p0)", explain="Ratio of specific activities (units/mg)")),
    ("BC-10.2.A", Q("bc-yield", LB, "Starting with {{u0}} enzyme units, {{u1}} units remain after purification. What is the yield (%)?",
        given={"u0": {"pick": [10000, 20000]}, "u1": {"pick": [2000, 4000, 6000]}}, value="100*u1/u0", tex="\\%", verify="100*Rational(u1, u0)",
        explain="Yield tracks activity, not protein; a good step raises fold purification while keeping yield")),
    ("BC-10.2.B", facts("bc-separation-choice", LB, [
        ("A protein with pI 9 at pH 7 binds which column?", "Cation exchanger (e.g. CM-cellulose)", "Anion exchanger", "Neither", "Gel filtration only"),
        ("In gel filtration, which elutes first?", "The largest protein", "The smallest", "The most charged", "The most hydrophobic"),
        ("A His-tagged protein is captured on:", "Ni²⁺-NTA affinity resin", "Size exclusion", "An anion exchanger always", "Silica"),
        ("Bound protein is eluted from an ion exchanger by:", "Raising salt (or shifting pH)", "Adding SDS", "Lowering temperature", "Adding DNA"),
        ("To remove a small contaminant from a large protein quickly:", "Dialysis or desalting (size)", "Ion exchange only", "Mass spectrometry", "SDS-PAGE"),
    ], "Choose by the property that differs most between target and contaminants")),
    ("BC-10.2.B", facts("bc-separation-choice-2", LB, [
        ("A protein with pI 4.5 at pH 7.5 binds:", "An anion exchanger (e.g. DEAE)", "A cation exchanger", "Neither", "Ni-NTA"),
        ("Ammonium sulfate precipitation separates proteins by:", "Solubility at high salt (salting out)", "Size", "pI only", "Affinity"),
        ("Why put an affinity step early in a purification?", "It gives the largest fold purification in one step", "It is cheapest", "It removes salt", "It measures mass"),
    ], "Order steps from high capacity to high resolution")),
    # 11.1
    ("BC-11.1.A", Q("bc-mol-clock", EV, "Two species' orthologous gene differs at {{d}}% of sites, and substitutions accumulate at {{r}} × 10⁻⁹ per site per year in each lineage. How long ago (millions of years) did they diverge?",
        given={"d": {"pick": [2, 6, 10]}, "r": {"pick": [1, 2]}}, value="(d/100)/(2*r*1e-9)/1e6", tex="t",
        verify="Rational(d, 100)/(2*r*Rational(1, 10**9))/10**6", explain="t = d/(2r): both lineages accumulate changes")),
    ("BC-11.1.A", facts("bc-mol-clock-2", EV, [
        ("Why divide by 2 in t = d/(2r)?", "Substitutions accumulate along both lineages since the split", "To convert units", "It's an error", "Because DNA is double-stranded"),
        ("Which genes evolve slowest?", "Those under strong functional constraint (e.g. histones)", "Pseudogenes", "Introns", "Noncoding repeats"),
        ("Saturation of substitutions at large distances makes raw percent difference:", "Underestimate true divergence", "Overestimate it", "Exact", "Irrelevant"),
    ], "Clocks need calibration and saturation corrections")),
    ("BC-11.1.B", Q("bc-identity", EV, "Two aligned sequences of {{L}} residues share {{m}} identical positions. What is their percent identity?",
        given={"L": {"pick": [200, 300]}, "m": {"pick": [60, 120, 150]}}, value="100*m/L", tex="\\%", verify="100*Rational(m, L)",
        explain="Above ~30–40% over a full domain, homology is very likely")),
    ("BC-11.1.B", facts("bc-homology", EV, [
        ("Homologous proteins share:", "A common ancestor", "Only similar function", "Identical sequences", "The same organism"),
        ("Two enzymes have 15% identity but the same fold and catalytic residues. They are probably:", "Distant homologues", "Unrelated", "Identical", "Pseudogenes"),
        ("Paralogues arise by:", "Gene duplication within a lineage", "Speciation", "Horizontal transfer only", "Translation errors"),
        ("Which residues are usually most conserved?", "Active-site and structural-core residues", "Surface loop residues", "Signal peptides", "Tags"),
    ], "Structure is conserved longer than sequence")),
    ("BC-11.2.A", Q("bc-mass-action", EV, "For a pathway step, K′ = {{K}} and the measured mass-action ratio Q = {{Qv}} at 310 K. What is ΔG (kJ/mol)?",
        given={"K": {"pick": [1000, 0.1, 10]}, "Qv": {"pick": [0.01, 1, 100]}}, value=f"{R}*310*log(Qv/K)/1000", tex="\\Delta G",
        verify=f"Rational('{R}')*310*(log(nsimplify(Qv)) - log(nsimplify(K)))/1000", explain="ΔG = RT ln(Q/K′): a step far from equilibrium is a likely control point")),
    ("BC-11.2.A", facts("bc-steady-state", EV, [
        ("A pathway intermediate's concentration is constant while flux passes through. This is:", "A steady state, not equilibrium", "Equilibrium", "Death", "A closed system"),
        ("Which step is most likely to be regulated?", "The one with Q/K′ far below 1 (large negative ΔG)", "The one with Q/K′ ≈ 1", "Any reversible step", "The last step always"),
        ("Living cells are:", "Open systems held far from equilibrium by energy input", "At equilibrium", "Closed systems", "Isolated"),
    ], "Homeostasis is a regulated steady state")),
]
