"""Organic Reactions, the intermediate steps (Nov 2026): 26 objectives, two types each. Before this the framework went
from four counting rules straight to "predict the product of…" objectives that each bundle a chapter of Bruice. These
are the single rules those predictions are assembled from: hybridisation, what makes an acid strong, leaving groups and
nucleophiles, intermediate stability, conformations and stereo relationships, then for each functional-group unit the
one-rule-at-a-time questions (regiochemistry, syn or anti, substrate class, reagent class, electrophilicity order,
which derivative converts to which), and a spectroscopy unit the framework lacked. NEEDS puts each ahead of the
prediction objective it feeds. Basis: the ACS organic content map (acs-accm-organic, read in full), Bruice 8e order.

All items here are authored multiple choice or simple arithmetic at sophomore level. pKa values are the rounded
landmarks Bruice uses; strain increments are printed on the card. Kevin checks organic content."""
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "or-steps", "organic-reactions", "P3"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
RS, STR, ALK, AKY, SE, CB, AC, AR, EN, SPEC = ("orgo.reasoning", "orgo.structure", "orgo.alkene-reactions", "orgo.alkyne-reactions", "orgo.substitution-elimination",
                                               "orgo.carbonyl-reactions", "orgo.acyl-reactions", "orgo.aromatic-reactions", "orgo.enolate-reactions", "orgo.spectroscopy")
A = lambda *s: [f"acs-accm-organic:{x}" for x in s]


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def L(name, skill, prompt, options, rows, explain):
    """a fixed list of options (kept in order); rows are (text, index of the right option)"""
    return Q(name, skill, prompt, pace="recall", cases=[{"q": a, "kc": k} for a, k in rows], choice=options, correct="kc", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", final=False, **kw):
    return Q(name, skill, prompt, value=value, tex=tex, final=final, verify=verify, explain=explain, **kw)


ARIO = ["Resonance: the conjugate base's charge is delocalised", "Atom: the charge sits on a more electronegative or larger atom",
        "Induction: nearby electronegative atoms withdraw electron density", "Orbital: the lone pair is in an orbital with more s character"]

UNITS = {"11": ("spectroscopy", "Spectroscopy for structure", ["RULES"], A("I.D.2", "IX.A.2"))}
TOPICS = {"1.3": "What makes a site reactive", "1.4": "Shape and stereochemistry", "2.3": "Additions, one rule at a time", "3.2": "Reading the substrate and the reagent",
          "4.2": "Carbonyl reasoning", "5.2": "Acyl reasoning", "6.2": "Aromatic reasoning", "7.2": "Carbon–carbon bond reasoning", "11.1": "Reading IR, NMR and mass spectra"}
OBJS = [
 ("OR-1.3.A", A("II.E.1", "II.F.1", "III.B.1"), "Assign the hybridisation and geometry of an atom and count σ and π bonds.", "Count the groups around the atom (σ bonds plus lone pairs): four is sp³, three sp², two sp. A lone pair next to a π bond is delocalised, so that atom is sp². Every bond has one σ; a double bond adds one π, a triple bond two."),
 ("OR-1.3.B", A("I.C.1", "VIII.C.2", "I.B.1"), "Explain an acidity difference by atom, resonance, induction or orbital, and recall landmark pKa values.", "The more stable the conjugate base, the stronger the acid. Landmarks: carboxylic acid about 5, phenol and ammonium about 10, water and alcohols about 16, terminal alkyne about 25, amine N–H about 36, alkene 44, alkane above 50."),
 ("OR-1.3.C", A("I.B.2", "I.B.3", "IV.E.2"), "Rank leaving groups and nucleophiles.", "Good leaving groups are weak bases: I⁻ > Br⁻ > Cl⁻ ≫ F⁻, and sulfonates such as tosylate; HO⁻, RO⁻ and H₂N⁻ do not leave. Nucleophilicity follows basicity in polar aprotic solvents; in protic solvents larger, more polarisable anions are better because small ones are held by hydrogen bonds."),
 ("OR-1.3.D", A("VII.F.2", "II.D.1"), "Rank carbocations, radicals and carbanions by stability.", "Carbocations and radicals: 3° > 2° > 1° > methyl, by hyperconjugation; allylic and benzylic ones are stabilised by resonance; vinyl and aryl cations are very unstable. Alkyl carbanions run the other way; a carbanion next to C=O is stabilised by resonance."),
 ("OR-1.4.A", A("II.F.2", "VIII.C.1"), "Compare conformations: staggered and eclipsed, gauche and anti, axial and equatorial.", "Staggered beats eclipsed and anti beats gauche. In a chair, a substituent is more stable equatorial because an axial one suffers 1,3-diaxial interactions; the chair with the larger group equatorial wins."),
 ("OR-1.4.B", A("III.E.1", "III.A.2"), "Classify two structures as identical, constitutional isomers, enantiomers or diastereomers, and count stereoisomers when a meso form exists.", "Enantiomers are non-superimposable mirror images: every stereocentre inverted. Diastereomers differ at some but not all stereocentres, and include cis–trans isomers. A meso compound has stereocentres and an internal mirror plane, so it removes one from the 2ⁿ count."),
 ("OR-1.4.C", A("III.E.5", "IX.C.2"), "Compute enantiomeric excess from optical rotation and the composition from the excess.", "ee = observed specific rotation / rotation of the pure enantiomer × 100. A sample with ee per cent excess contains (100 + ee)/2 per cent of the major enantiomer. A racemic mixture has ee 0 and does not rotate light."),
 ("OR-1.4.D", A("III.B.2", "IX.B.1"), "Assign E or Z to an alkene and rank alkenes by stability.", "On each alkene carbon, rank the two groups by atomic number at the first point of difference. High-priority groups on the same side is Z, opposite is E. More substituted alkenes are more stable, and trans beats cis."),
 ("OR-2.3.A", A("V.F.1", "V.F.2", "III.E.3"), "State the regiochemistry and the stereochemistry each alkene addition gives.", "Through a carbocation (HX, H₃O⁺): Markovnikov, no stereocontrol. Radical HBr and hydroboration: anti-Markovnikov, hydroboration syn. Br₂ and halohydrins: anti, through a bromonium ion. H₂/Pd, OsO₄ and peroxyacids: syn."),
 ("OR-2.3.B", A("VII.F.2", "V.D.1"), "Find the carbocation an addition goes through and decide whether it rearranges; recall the alkyne counterparts.", "The proton adds to give the more stable cation; a 1,2-hydride or methyl shift follows whenever it gives a more stable one. Alkynes: Lindlar gives cis, Na/NH₃ trans; Hg²⁺ hydration gives a methyl ketone, hydroboration an aldehyde."),
 ("OR-3.2.A", A("V.D.2", "III.E.4"), "Classify an alkyl halide and say which mechanisms it allows.", "Methyl and 1°: SN2 (E2 only with a bulky base). 2°: all four, decided by the reagent. 3°: no SN2; E2 with a strong base, SN1/E1 with a weak one. Allylic and benzylic react fast by either. Vinyl and aryl: neither SN1 nor SN2."),
 ("OR-3.2.B", A("IV.E.1", "IV.E.2", "I.C.1"), "Classify a reagent as strong or weak base and nucleophile, and a solvent as protic or aprotic.", "Strong base, strong nucleophile: HO⁻, RO⁻. Strong bulky base: tert-butoxide, LDA, DBU. Good nucleophile, weak base: I⁻, Br⁻, HS⁻, RS⁻, N₃⁻, NC⁻. Weak both: H₂O, ROH. Polar aprotic solvents (DMSO, DMF, acetone, acetonitrile) speed SN2; protic solvents favour SN1 and E1."),
 ("OR-3.2.C", A("III.E.3", "III.E.4"), "State the stereochemical outcome of SN2, SN1 and E2.", "SN2: back-side attack, inversion. SN1: planar carbocation, racemisation (often slightly more inversion). E2: H and leaving group anti-periplanar, which in a cyclohexane means both axial; the reaction is stereospecific."),
 ("OR-3.2.D", A("V.E.1", "V.D.1"), "Predict how far an alcohol is oxidised and how its OH is turned into a leaving group.", "PCC, Swern and Dess–Martin stop a 1° alcohol at the aldehyde; aqueous chromic acid takes it to the carboxylic acid. 2° alcohols give ketones; 3° alcohols are not oxidised. TsCl keeps the configuration; PBr₃ and SOCl₂/pyridine invert; HX on a 3° alcohol is SN1."),
 ("OR-4.2.A", A("III.F.1", "VII.C.2"), "Rank carbonyl compounds by electrophilicity and say which hydride reduces which.", "Acyl chloride > anhydride > aldehyde > ketone > ester ≈ acid > amide > carboxylate. NaBH₄ reduces aldehydes and ketones; LiAlH₄ also reduces esters, acids and amides (amides to amines); DIBAL-H at −78 °C stops an ester at the aldehyde."),
 ("OR-4.2.B", A("VII.C.1", "V.E.1"), "Decide between addition and substitution at a carbonyl, and recognise hemiacetals and acetals.", "Both begin with a tetrahedral alkoxide. If the carbonyl carbon carries a leaving group it is expelled (substitution); aldehydes and ketones have none (addition). Acetals form with acid and removal of water, survive base and nucleophiles, and so protect a carbonyl."),
 ("OR-4.2.C", A("VIII.C.2", "VII.F.1"), "Recall α-hydrogen pKa values and choose conditions for the kinetic or thermodynamic enolate.", "α-H of a ketone about 20, an ester about 25, a β-diketone about 9. LDA (its amine has pKa about 36) at −78 °C removes the less hindered proton completely: the kinetic enolate. Alkoxide at room temperature equilibrates to the more substituted, thermodynamic enolate."),
 ("OR-5.2.A", A("VIII.A.1", "V.E.1"), "Decide whether an acyl substitution goes forward and what hydrolysis needs.", "An acyl derivative converts only into a less reactive one: chloride → anhydride → ester → amide, never back without activation. Saponification is irreversible because the acid ends as carboxylate; acid-catalysed hydrolysis is the reverse of Fischer esterification."),
 ("OR-5.2.B", A("III.A.1", "IX.B.1"), "Recognise the carboxylic acid derivatives, including cyclic ones, and give their hydrolysis products.", "Ester RCO₂R′, amide RCONR₂, anhydride (RCO)₂O, acyl chloride RCOCl, nitrile RCN; a cyclic ester is a lactone, a cyclic amide a lactam. Hydrolysis returns the carboxylic acid plus the alcohol, amine, second acid or ammonia."),
 ("OR-6.2.A", A("I.B.2", "V.D.2"), "Name the electrophile each aromatic substitution uses and the limits of the Friedel–Crafts reactions.", "Br₂/FeBr₃ gives a polarised bromine, HNO₃/H₂SO₄ gives NO₂⁺, RCl/AlCl₃ a carbocation, RCOCl/AlCl₃ an acylium ion. Alkylation rearranges and over-alkylates; acylation does neither. Neither works on strongly deactivated rings."),
 ("OR-6.2.B", A("V.A.4", "V.F.2"), "Choose the order of two aromatic substitutions and explain why a group directs where it does.", "Install first the group whose directing effect puts the second where you want it. Lone-pair donors direct ortho/para by resonance; halogens also do, though they deactivate by induction; groups with a positive or partial positive atom on the ring direct meta."),
 ("OR-7.2.A", A("I.B.3", "V.E.1"), "Name the product type of an aldol, Claisen, Michael and Robinson reaction and the conditions each needs.", "Aldol: β-hydroxy carbonyl, dehydrating on heating to the enone. Claisen: β-keto ester, needing a full equivalent of alkoxide. Michael: 1,5-dicarbonyl. Robinson: Michael then intramolecular aldol. A crossed aldol is clean when one partner has no α-hydrogen."),
 ("OR-7.2.B", A("II.E.2", "III.E.3"), "State what a Diels–Alder reaction needs and what it preserves.", "An s-cis diene (best electron-rich) and a dienophile (best electron-poor) join in one concerted step, six π electrons making two σ bonds and a cyclohexene. Dienophile stereochemistry is retained; cyclic dienes favour the endo product."),
 ("OR-11.1.A", A("I.D.2", "IX.A.2"), "Read functional groups from landmark IR bands.", "O–H broad 3200–3600, acid O–H very broad 2500–3300, N–H 3300–3500 (two bands for NH₂), ≡C–H 3300 sharp, sp² C–H just above 3000 and sp³ just below, C≡N 2250, C≡C 2100–2260, C=O about 1700 cm⁻¹ (ester higher, amide and conjugated lower)."),
 ("OR-11.1.B", A("III.D.2", "I.D.2"), "Use splitting, integration and landmark shifts in a ¹H NMR spectrum.", "n equivalent neighbours split a signal into n + 1 peaks. Landmarks in ppm: alkyl 0.9–1.5, next to C=O 2–2.5, next to O 3.3–4, vinyl 4.5–6.5, aromatic 6.5–8, aldehyde 9–10, carboxylic acid 10–12."),
 ("OR-11.1.C", A("I.A.1", "I.D.2"), "Read a mass spectrum: isotope patterns, the nitrogen rule and common losses.", "One Br gives M and M + 2 about 1:1; one Cl about 3:1. An odd molecular mass means an odd number of nitrogens. Common losses: 15 CH₃, 18 H₂O, 29 C₂H₅ or CHO; common ions: 43 acylium or propyl, 77 phenyl, 91 benzyl (tropylium)."),
]
ADD = [
 ("OR-1.3.A", F("or-hybridisation", STR, [
    ("The carbonyl carbon of acetone is:", "sp², trigonal planar", "sp³, tetrahedral", "sp, linear", "sp³, trigonal pyramidal"),
    ("Each carbon of acetylene is:", "sp, linear", "sp², trigonal planar", "sp³, tetrahedral", "sp², bent"),
    ("The nitrogen of trimethylamine is:", "sp³, trigonal pyramidal", "sp², trigonal planar", "sp, linear", "sp², bent"),
    ("The central carbon of allene, CH₂=C=CH₂, is:", "sp", "sp²", "sp³", "Not hybridised"),
    ("The nitrogen of an amide, whose lone pair is delocalised into the C=O, is best described as:", "sp², planar", "sp³, pyramidal", "sp, linear", "sp³, tetrahedral")],
    "Count σ bonds plus lone pairs on the atom; a lone pair that is part of a resonance system does not count as a separate group")),
 ("OR-1.3.A", N("or-sigma-count", STR, "{{nm}} has {{kpi}} π bond(s). How many σ bonds does it have?", "(4*kc + kh + 2*ko + 3*kn)/2 - kpi", "(kc + kh + ko + kn) - 1 + kr",
    "Total bonds = half the sum of valences (C 4, H 1, O 2, N 3); subtract the π bonds. Check: an acyclic molecule of N atoms has N − 1 σ bonds, and each ring adds one", tex="\\sigma", final=True,
    cases=[{"nm": "Ethene, C₂H₄,", "kc": 2, "kh": 4, "ko": 0, "kn": 0, "kpi": 1, "kr": 0}, {"nm": "Propyne, C₃H₄,", "kc": 3, "kh": 4, "ko": 0, "kn": 0, "kpi": 2, "kr": 0},
           {"nm": "Benzene, C₆H₆,", "kc": 6, "kh": 6, "ko": 0, "kn": 0, "kpi": 3, "kr": 1}, {"nm": "Acetone, C₃H₆O,", "kc": 3, "kh": 6, "ko": 1, "kn": 0, "kpi": 1, "kr": 0},
           {"nm": "Acetonitrile, C₂H₃N,", "kc": 2, "kh": 3, "ko": 0, "kn": 1, "kpi": 2, "kr": 0}, {"nm": "Cyclohexene, C₆H₁₀,", "kc": 6, "kh": 10, "ko": 0, "kn": 0, "kpi": 1, "kr": 1}])),
 ("OR-1.3.B", L("or-acidity-factor", RS, "{{q}}", ARIO, [
    ("Acetic acid (pKa about 5) is far more acidic than ethanol (about 16). The main reason:", 0),
    ("A thiol (pKa about 10) is more acidic than an alcohol (about 16). The main reason:", 1),
    ("2,2,2-Trifluoroethanol is more acidic than ethanol. The main reason:", 2),
    ("A terminal alkyne (pKa about 25) is more acidic than an alkene (about 44). The main reason:", 3),
    ("Water is more acidic than ammonia. The main reason:", 1),
    ("Phenol (pKa about 10) is more acidic than cyclohexanol (about 16). The main reason:", 0),
    ("Chloroacetic acid is more acidic than acetic acid. The main reason:", 2)],
    "Ask what stabilises the conjugate base. Check the atom bearing the charge first, then resonance, then induction, then the orbital")),
 ("OR-1.3.B", F("or-pka-six", RS, [
    ("Approximate pKa of a carboxylic acid such as acetic acid:", "About 5", "About 10", "About 16", "About 25"),
    ("Approximate pKa of phenol:", "About 10", "About 5", "About 16", "About 25"),
    ("Approximate pKa of an alcohol such as ethanol:", "About 16", "About 5", "About 10", "About 36"),
    ("Approximate pKa of a terminal alkyne C–H:", "About 25", "About 16", "About 44", "About 5"),
    ("Approximate pKa of an alkylammonium ion, RNH₃⁺:", "About 10", "About 5", "About 25", "About 36"),
    ("Approximate pKa of an amine N–H (for example ammonia acting as an acid):", "About 36", "About 10", "About 16", "About 25")],
    "Six numbers that settle most acid–base questions in the course: 5, 10, 10, 16, 25, 36")),
 ("OR-1.3.C", F("or-leaving-group", RS, [
    ("Which is the best leaving group?", "I⁻", "F⁻", "HO⁻", "H₂N⁻"),
    ("Which is the best leaving group?", "Tosylate, TsO⁻", "HO⁻", "CH₃O⁻", "H⁻"),
    ("Good leaving groups are:", "Weak bases (conjugate bases of strong acids)", "Strong bases", "Always small and highly charged", "Always strong nucleophiles"),
    ("In acid, the OH of an alcohol can leave because it departs as:", "Water", "Hydroxide", "Hydride", "Oxide"),
    ("Which halide is the poorest leaving group?", "F⁻", "Cl⁻", "Br⁻", "I⁻")],
    "The weaker the base, the better it leaves; hydroxide and alkoxide must be converted first (protonated, or made into a sulfonate)")),
 ("OR-1.3.C", F("or-nucleophile-rank", RS, [
    ("In a polar protic solvent such as methanol, which halide is the best nucleophile?", "I⁻", "F⁻", "Cl⁻", "Br⁻"),
    ("In a polar aprotic solvent such as DMSO, which halide is the best nucleophile?", "F⁻", "I⁻", "Br⁻", "Cl⁻"),
    ("Which is the strongest nucleophile?", "CH₃O⁻", "CH₃OH", "H₂O", "CH₃CO₂H"),
    ("tert-Butoxide is a poor nucleophile mainly because it is:", "Sterically hindered", "A weak base", "Uncharged", "Too polarisable"),
    ("Which is the better nucleophile in a protic solvent?", "HS⁻", "HO⁻", "H₂O", "F⁻")],
    "A charged species beats its neutral conjugate acid. Down a group, protic solvents make the larger anion the better nucleophile because the small one is tied up by hydrogen bonds")),
 ("OR-1.3.D", F("or-carbocation-rank", RS, [
    ("Which carbocation is most stable?", "tert-Butyl (3°)", "Isopropyl (2°)", "Ethyl (1°)", "Methyl"),
    ("Which carbocation is most stable?", "Benzyl", "Ethyl (1°)", "Methyl", "Vinyl"),
    ("Alkyl groups stabilise a carbocation by:", "Hyperconjugation and induction", "Donating a lone pair", "Hydrogen bonding", "Withdrawing electrons"),
    ("An allyl cation is more stable than a propyl cation because of:", "Resonance", "Greater s character", "Steric relief", "A stronger C–H bond"),
    ("Which carbocation is least stable?", "Vinyl", "Isopropyl (2°)", "Allyl", "tert-Butyl (3°)")],
    "More alkyl groups, or a neighbouring π system, spread the positive charge. A cation on an sp² or sp carbon cannot be stabilised this way")),
 ("OR-1.3.D", F("or-intermediate-facts", RS, [
    ("Alkyl radical stability follows:", "3° > 2° > 1° > methyl", "methyl > 1° > 2° > 3°", "1° > 3° > 2° > methyl", "All are equal"),
    ("Simple alkyl carbanion stability follows:", "methyl > 1° > 2° > 3°", "3° > 2° > 1° > methyl", "2° > 3° > 1° > methyl", "All are equal"),
    ("Which carbanion is most stable?", "One next to a C=O (an enolate)", "A 3° alkyl carbanion", "A 2° alkyl carbanion", "A 1° alkyl carbanion"),
    ("The charged carbon of a carbocation is:", "sp², with an empty p orbital", "sp³, with a lone pair", "sp³, with an empty sp³ orbital", "sp, with a lone pair"),
    ("A 1,2-hydride shift happens when it produces:", "A more stable carbocation", "A less stable carbocation", "A radical", "A carbanion")],
    "Radicals follow cations (electron-poor centres are helped by alkyl groups); carbanions are the reverse and need resonance or an electronegative neighbour")),
 ("OR-1.4.A", N("or-eclipsing-strain", STR, "Looking down one C–C bond, an eclipsed conformation has {{kh}} H/H, {{km}} CH₃/H and {{kq}} CH₃/CH₃ eclipsing interactions. Taking these as 1.0, 1.4 and 2.6 kcal/mol each, find its strain above the staggered form.", "kh*1.0 + km*1.4 + kq*2.6", "kh + km*Rational(14, 10) + kq*Rational(26, 10)",
    "Add the three eclipsing pairs. Propane's barrier (two H/H and one CH₃/H) comes out at 3.4 kcal/mol", tex="E",
    cases=[{"kh": 3, "km": 0, "kq": 0}, {"kh": 2, "km": 1, "kq": 0}, {"kh": 1, "km": 2, "kq": 0}, {"kh": 2, "km": 0, "kq": 1}, {"kh": 0, "km": 2, "kq": 1}])),
 ("OR-1.4.A", F("or-chair-preference", STR, [
    ("In the more stable chair of methylcyclohexane the methyl group is:", "Equatorial", "Axial", "Equally axial and equatorial", "In the plane of the ring"),
    ("An axial substituent is destabilised mainly by:", "1,3-Diaxial interactions", "Angle strain", "Loss of resonance", "Eclipsing with the ring oxygen"),
    ("In either chair of cis-1,2-dimethylcyclohexane the two methyls are:", "One axial, one equatorial", "Both equatorial", "Both axial", "Both in the ring plane"),
    ("trans-1,2-Dimethylcyclohexane prefers the chair with:", "Both methyls equatorial", "Both methyls axial", "One axial, one equatorial", "No preference"),
    ("cis-1,3-Dimethylcyclohexane prefers the chair with:", "Both methyls equatorial", "Both methyls axial", "One axial, one equatorial", "No preference"),
    ("In tert-butylcyclohexane the tert-butyl group is essentially always:", "Equatorial", "Axial", "Half axial, half equatorial", "Out of the chair entirely")],
    "Draw the chair and its ring flip; every axial group becomes equatorial and the reverse. The flip that puts the most (or largest) groups equatorial wins")),
 ("OR-1.4.B", F("or-isomer-pair", STR, [
    ("(2R,3R)-2,3-Dibromopentane and (2S,3S)-2,3-dibromopentane are:", "Enantiomers", "Diastereomers", "Identical", "Constitutional isomers"),
    ("(2R,3R)-2,3-Dibromopentane and (2R,3S)-2,3-dibromopentane are:", "Diastereomers", "Enantiomers", "Identical", "Constitutional isomers"),
    ("cis-2-Butene and trans-2-butene are:", "Diastereomers", "Enantiomers", "Constitutional isomers", "Identical"),
    ("Butane and 2-methylpropane are:", "Constitutional isomers", "Diastereomers", "Enantiomers", "Identical"),
    ("(2R,3S)-2,3-Dibromobutane and (2S,3R)-2,3-dibromobutane are:", "Identical (one meso compound)", "Enantiomers", "Diastereomers", "Constitutional isomers")],
    "Same connectivity? If not, constitutional. If so: all stereocentres inverted means enantiomers (unless the molecule is meso), some inverted means diastereomers")),
 ("OR-1.4.B", L("or-stereoisomer-count", STR, "How many stereoisomers does {{q}} have?", ["2", "3", "4", "8"], [
    ("tartaric acid, HO₂C–CH(OH)–CH(OH)–CO₂H,", 1), ("2,3-dibromopentane", 2), ("2,3-dibromobutane", 1), ("1,2-dimethylcyclohexane", 1),
    ("1,4-dimethylcyclohexane", 0), ("2-bromo-3-chlorobutane", 2), ("1,3-dimethylcyclohexane", 1)],
    "Two stereocentres give at most four. When the two ends are identical, one of the four pairs up as a single meso compound, leaving three. 1,4-Dimethylcyclohexane has no stereocentres, only cis and trans")),
 ("OR-1.4.C", N("or-ee-from-rotation", STR, "A sample has specific rotation {{ko}}°; the pure enantiomer has {{kp}}°. Find the enantiomeric excess in per cent.", "ko/kp*100", "solve(Eq(Symbol('m')/100*nsimplify(kp), nsimplify(ko)), Symbol('m'))[0]",
    "ee = observed/pure × 100", tex="ee",
    cases=[{"ko": 6.0, "kp": 12.0}, {"ko": 9.0, "kp": 12.0}, {"ko": 4.6, "kp": 23.0}, {"ko": 21.0, "kp": 28.0}, {"ko": 3.3, "kp": 66.0}])),
 ("OR-1.4.C", N("or-major-from-ee", STR, "A mixture of two enantiomers has an enantiomeric excess of {{ke}}%. What per cent of the mixture is the major enantiomer?", "(100 + ke)/2", "solve(Eq(Symbol('m') - (100 - Symbol('m')), ke), Symbol('m'))[0]",
    "The racemic part, 100 − ee, is split evenly; the major enantiomer is the excess plus half of the rest", tex="major", final=True,
    given={"ke": {"pick": [10, 20, 50, 80, 90, 98]}})),
 ("OR-1.4.D", L("or-e-z", STR, "{{q}} The alkene is:", ["E", "Z", "Neither: it has no E/Z isomers"], [
    ("One alkene carbon carries Cl and H, the other Br and CH₃; Cl and Br are on the same side.", 1),
    ("One alkene carbon carries CH₃ and H, the other CH₂CH₃ and CH₃; the first carbon's CH₃ is on the same side as the ethyl.", 1),
    ("One alkene carbon carries F and Cl, the other Br and I; Cl and Br are on the same side.", 0),
    ("One alkene carbon carries two Cl, the other H and CH₃.", 2),
    ("One alkene carbon carries OH and CH₃, the other CHO and CH₂OH; OH and CHO are on the same side.", 1),
    ("One alkene carbon carries CH₃ and H, the other CH₃ and H; the two CH₃ groups are on opposite sides.", 0)],
    "Rank the two groups on each carbon by atomic number (go outward at a tie: CHO counts as O, O, H and beats CH₂OH with O, H, H). Higher-priority groups together is Z")),
 ("OR-1.4.D", F("or-alkene-stability", STR, [
    ("Which alkene is most stable?", "2,3-Dimethyl-2-butene (tetrasubstituted)", "2-Methyl-2-butene (trisubstituted)", "trans-2-Butene", "1-Butene"),
    ("Which is more stable?", "trans-2-Butene, because its methyls are farther apart", "cis-2-Butene, because its methyls are closer", "They are equal", "Neither can be isolated"),
    ("A smaller heat of hydrogenation means the alkene is:", "More stable", "Less stable", "Less substituted", "More strained"),
    ("Zaitsev's rule says elimination favours:", "The more substituted alkene", "The less substituted alkene", "The cis alkene", "The terminal alkene")],
    "Each alkyl group on the double bond stabilises it; the heat released on hydrogenation measures how far above the alkane the alkene sits")),
 ("OR-2.3.A", F("or-addition-regio", ALK, [
    ("HBr adds to 1-butene. The Br ends up on:", "C2, the more substituted carbon (Markovnikov)", "C1, the less substituted carbon", "C1 and C2 equally", "C3"),
    ("HBr with peroxides adds to 1-butene. The Br ends up on:", "C1, the less substituted carbon (anti-Markovnikov)", "C2, the more substituted carbon", "C1 and C2 equally", "C3"),
    ("BH₃·THF, then H₂O₂ and NaOH, on 1-butene puts the OH on:", "C1, the less substituted carbon", "C2, the more substituted carbon", "Both C1 and C2", "C3"),
    ("H₂O with H₂SO₄ on 1-butene puts the OH on:", "C2, the more substituted carbon", "C1, the less substituted carbon", "Both C1 and C2", "C4"),
    ("Oxymercuration–reduction is chosen over acid-catalysed hydration because it:", "Gives the Markovnikov alcohol without carbocation rearrangement", "Gives the anti-Markovnikov alcohol", "Adds two OH groups", "Cleaves the double bond")],
    "Ask what the first species to add is and where it goes: H⁺ goes to the carbon with more hydrogens; Br• and boron go to the less hindered carbon")),
 ("OR-2.3.A", L("or-addition-stereo", ALK, "{{q}} The two new groups add:", ["Syn (same face)", "Anti (opposite faces)", "With no control: a planar carbocation is attacked from both faces"], [
    ("H₂ with Pd/C on an alkene.", 0), ("Br₂ in CH₂Cl₂ on an alkene.", 1), ("BH₃·THF, then H₂O₂ and NaOH.", 0), ("OsO₄, then NaHSO₃ and water.", 0),
    ("A peroxyacid (mCPBA) forming an epoxide.", 0), ("HBr on an alkene.", 2), ("Br₂ in water (halohydrin formation).", 1), ("Epoxidation, then aqueous acid, giving a diol.", 1)],
    "One-step or surface additions deliver both groups to one face. A three-membered ring intermediate (bromonium, epoxide) is opened from the back, giving anti")),
 ("OR-2.3.B", F("or-cation-and-shift", ALK, [
    ("HCl adds to 2-methylpropene. The intermediate carbocation is:", "Tertiary", "Primary", "Secondary", "Vinylic"),
    ("HBr adds to 3-methyl-1-butene. The major product forms after:", "A 1,2-hydride shift from the secondary to a tertiary cation", "No rearrangement", "A 1,2-methyl shift to a primary cation", "A radical chain"),
    ("HBr adds to 3,3-dimethyl-1-butene. The major product forms after:", "A 1,2-methyl shift from the secondary to a tertiary cation", "A 1,2-hydride shift", "No rearrangement", "A radical chain"),
    ("Markovnikov's rule holds because the proton adds so as to give:", "The more stable carbocation", "The less hindered carbocation", "The stronger C–H bond", "The more stable radical")],
    "Protonate to the more stable cation, then look one carbon over: if moving an H or CH₃ with its electrons makes a more stable cation, it moves")),
 ("OR-2.3.B", F("or-alkyne-rules", AKY, [
    ("H₂ with Lindlar's catalyst converts an internal alkyne to:", "A cis alkene", "A trans alkene", "An alkane", "A ketone"),
    ("Na in liquid NH₃ converts an internal alkyne to:", "A trans alkene", "A cis alkene", "An alkane", "An enol"),
    ("H₂O, H₂SO₄ and HgSO₄ convert a terminal alkyne to:", "A methyl ketone", "An aldehyde", "A diol", "A carboxylic acid"),
    ("A hindered borane, then H₂O₂ and NaOH, converts a terminal alkyne to:", "An aldehyde", "A methyl ketone", "A primary alcohol", "A cis alkene"),
    ("NaNH₂ removes a terminal alkyne's proton because ammonia (pKa about 36) is:", "A much weaker acid than the alkyne (pKa about 25)", "A stronger acid than the alkyne", "A good leaving group", "A radical initiator")],
    "Hydration gives an enol that tautomerises: Markovnikov OH becomes a ketone, anti-Markovnikov OH becomes an aldehyde")),
 ("OR-3.2.A", F("or-substrate-class", SE, [
    ("Which alkyl halides react fastest by SN2?", "Methyl and primary", "Tertiary", "Vinyl and aryl", "Neopentyl"),
    ("A tertiary alkyl halide does not react by SN2 because:", "The back side of the carbon is blocked", "Its carbocation is unstable", "Its leaving group is poor", "It has no β-hydrogens"),
    ("Under ordinary conditions vinyl and aryl halides undergo:", "Neither SN1 nor SN2", "SN2 readily", "SN1 readily", "Both SN1 and SN2"),
    ("A primary benzylic or allylic halide can react by SN1 because:", "Its carbocation is resonance-stabilised", "It is unhindered", "It has no β-hydrogens", "Its C–X bond is unusually strong"),
    ("Neopentyl bromide, (CH₃)₃CCH₂Br, is primary yet very slow in SN2 because of:", "Steric hindrance from the neighbouring quaternary carbon", "A poor leaving group", "Resonance in the substrate", "An unusually strong C–Br bond")],
    "SN2 needs room at the back of the carbon; SN1 needs a cation that can exist. Classify the carbon first, then ask which of the two is possible")),
 ("OR-3.2.A", F("or-mechanism-rate-rank", SE, [
    ("Rank SN2 reactivity, fastest first:", "CH₃Br > CH₃CH₂Br > (CH₃)₂CHBr > (CH₃)₃CBr", "(CH₃)₃CBr > (CH₃)₂CHBr > CH₃CH₂Br > CH₃Br", "(CH₃)₂CHBr > CH₃Br > (CH₃)₃CBr > CH₃CH₂Br", "All react at the same rate"),
    ("Rank SN1 reactivity, fastest first:", "(CH₃)₃CBr > (CH₃)₂CHBr > CH₃CH₂Br", "CH₃CH₂Br > (CH₃)₂CHBr > (CH₃)₃CBr", "(CH₃)₂CHBr > (CH₃)₃CBr > CH₃CH₂Br", "All react at the same rate"),
    ("For one alkyl group, which halide reacts fastest in substitution and elimination alike?", "R–I", "R–F", "R–Cl", "R–Br"),
    ("E2 reactivity of alkyl halides follows:", "3° > 2° > 1°", "1° > 2° > 3°", "Methyl > 1° > 2°", "All react at the same rate")],
    "SN2 falls with crowding; SN1 and E1 rise with cation stability; E2 rises with substitution because the alkene formed is more stable")),
 ("OR-3.2.B", F("or-reagent-class", SE, [
    ("Potassium tert-butoxide is best described as:", "A strong, bulky base and a poor nucleophile", "A good nucleophile and a weak base", "A weak base and a weak nucleophile", "An acid"),
    ("NaCN, NaN₃ and NaSH are:", "Good nucleophiles but weak bases", "Strong bulky bases", "Weak nucleophiles and weak bases", "Acids"),
    ("Water and alcohols on their own are:", "Weak nucleophiles and weak bases", "Strong bases", "Strong nucleophiles", "Bulky bases"),
    ("Sodium ethoxide is:", "Both a strong base and a strong nucleophile", "A weak base", "A bulky, non-nucleophilic base", "A weak nucleophile and a weak base"),
    ("With tert-butoxide, E2 of 2-bromo-2-methylbutane gives mainly:", "The less substituted (Hofmann) alkene", "The more substituted (Zaitsev) alkene", "The substitution product", "No reaction")],
    "Sort the reagent into one of four boxes before looking at the substrate: strong base and nucleophile, bulky strong base, nucleophile only, or weak in both")),
 ("OR-3.2.B", F("or-solvent-class", SE, [
    ("Which solvent most speeds an SN2 reaction of an anionic nucleophile?", "DMSO (polar aprotic)", "Methanol (polar protic)", "Water", "Hexane"),
    ("Polar protic solvents favour SN1 because they:", "Stabilise the carbocation and the leaving group", "Strengthen the nucleophile", "Block the back side of the carbon", "Remove β-hydrogens"),
    ("Which is a polar aprotic solvent?", "Acetone", "Ethanol", "Water", "Acetic acid"),
    ("Protic solvents weaken small anionic nucleophiles by:", "Hydrogen-bonding to them", "Oxidising them", "Protonating the substrate", "Lowering the temperature")],
    "Protic means an O–H or N–H that can hydrogen-bond. Aprotic polar solvents dissolve the salt but leave the anion bare and reactive")),
 ("OR-3.2.C", F("or-stereo-outcome", SE, [
    ("SN2 at a stereocentre gives:", "Inversion of configuration", "Retention", "Racemisation", "Loss of the stereocentre"),
    ("SN1 at a stereocentre gives:", "A nearly racemic mixture", "Clean inversion", "Clean retention", "A single diastereomer"),
    ("E2 needs the β-hydrogen and the leaving group to be:", "Anti-periplanar", "Gauche", "Perpendicular", "On the same carbon"),
    ("In a cyclohexane, E2 needs the leaving group and the β-hydrogen to be:", "Both axial (trans-diaxial)", "Both equatorial", "One axial and one equatorial", "Cis to each other")],
    "Back-side attack inverts; a planar cation forgets its configuration; E2 needs the breaking C–H and C–X bonds lined up anti")),
 ("OR-3.2.C", F("or-stereo-consequences", SE, [
    ("(R)-2-Bromobutane with NaCN in DMSO gives a nitrile whose stereocentre has:", "The opposite spatial arrangement (inversion)", "The same arrangement (retention)", "Both arrangements equally", "Disappeared"),
    ("Converting an alcohol to its tosylate (TsCl, pyridine) at a stereocentre:", "Retains configuration, because the C–O bond is not broken", "Inverts configuration", "Racemises it", "Destroys the stereocentre"),
    ("Tosylation followed by SN2 with a nucleophile gives overall:", "One inversion", "Two inversions (net retention)", "Racemisation", "Retention"),
    ("E2 is called stereospecific because:", "Each diastereomer of the substrate gives its own alkene isomer", "It always gives the trans alkene", "It goes through a carbocation", "It needs a chiral base")],
    "Track each step: only a step that breaks a bond to the stereocentre can change it")),
 ("OR-3.2.D", L("or-alcohol-oxidation", SE, "{{q}} The product is:", ["An aldehyde", "A carboxylic acid", "A ketone", "No reaction"], [
    ("A primary alcohol with PCC in CH₂Cl₂.", 0), ("A primary alcohol with Na₂Cr₂O₇ in aqueous H₂SO₄.", 1), ("A secondary alcohol with PCC.", 2), ("A secondary alcohol with Na₂Cr₂O₇ in aqueous H₂SO₄.", 2),
    ("A tertiary alcohol with Na₂Cr₂O₇ in aqueous H₂SO₄.", 3), ("A primary alcohol under Swern conditions.", 0), ("A primary alcohol with Dess–Martin periodinane.", 0)],
    "Oxidation removes an H from the carbinol carbon: a tertiary alcohol has none. Water lets the aldehyde hydrate and oxidise again, so only anhydrous reagents stop at the aldehyde")),
 ("OR-3.2.D", F("or-oh-to-leaving-group", SE, [
    ("PBr₃ converts a primary or secondary alcohol to the bromide by:", "SN2, with inversion", "SN1, with racemisation", "A radical chain", "E2"),
    ("SOCl₂ with pyridine converts a secondary alcohol to the chloride with:", "Inversion", "Retention", "Racemisation", "Rearrangement"),
    ("A tertiary alcohol reacts with HBr by:", "SN1", "SN2", "E2 only", "No reaction"),
    ("Concentrated H₂SO₄ and heat convert an alcohol to:", "An alkene (dehydration)", "An alkane", "A ketone", "An ether only"),
    ("Hydroxide itself is not displaced in SN2 because it is:", "A strong base and so a poor leaving group", "Too large", "Not nucleophilic", "Uncharged")],
    "Every method first turns OH into something that can leave: a protonated oxygen, a phosphite or chlorosulfite ester, or a sulfonate")),
 ("OR-4.2.A", F("or-carbonyl-electrophilicity", CB, [
    ("Which is most reactive toward nucleophiles?", "An acyl chloride", "An ester", "An amide", "A carboxylate ion"),
    ("Why is an aldehyde more electrophilic than a ketone?", "One fewer electron-donating alkyl group and less crowding", "It has more alkyl groups", "Its C=O is not polar", "It has a leaving group"),
    ("Amides are the least reactive neutral acid derivatives because:", "The nitrogen lone pair donates strongly into the C=O", "Nitrogen is a good leaving group", "They have no C=O", "They are always hindered"),
    ("Which order of reactivity in nucleophilic acyl substitution is correct?", "Acyl chloride > anhydride > ester > amide", "Amide > ester > anhydride > acyl chloride", "Ester > acyl chloride > amide > anhydride", "All are equal")],
    "The better the group on the carbonyl donates by resonance (N > O > Cl), the less electrophilic the carbon, and the worse that group is at leaving")),
 ("OR-4.2.A", F("or-hydride-scope", CB, [
    ("NaBH₄ in methanol reduces:", "Aldehydes and ketones, but not esters or amides", "Esters and amides only", "Carboxylic acids", "Isolated alkenes"),
    ("Which reagent reduces a carboxylic acid to a primary alcohol?", "LiAlH₄", "NaBH₄", "H₂ with Lindlar's catalyst", "PCC"),
    ("DIBAL-H at −78 °C, then water, converts an ester to:", "An aldehyde", "A primary alcohol", "A carboxylic acid", "A ketone"),
    ("LiAlH₄ reduces an amide to:", "An amine", "An alcohol", "An aldehyde", "A nitrile"),
    ("LiAlH₄ must be used in dry ether or THF because with water or alcohols it:", "Reacts violently, giving H₂", "Is unreactive", "Forms an acetal", "Becomes NaBH₄")],
    "NaBH₄ is the mild one (aldehydes and ketones); LiAlH₄ reduces everything with a C=O; DIBAL-H in the cold delivers one hydride to an ester")),
 ("OR-4.2.B", F("or-add-or-substitute", CB, [
    ("A nucleophile adds to a ketone and the C=O does not re-form because:", "The carbonyl carbon carries no leaving group", "Ketones are too hindered", "The nucleophile is too weak", "The C=O is not polar"),
    ("An ester reacts with a nucleophile by substitution because:", "The tetrahedral intermediate can expel alkoxide and re-form the C=O", "Esters have no C=O", "Esters are more electrophilic than aldehydes", "Alkoxide is a weak base"),
    ("The intermediate common to carbonyl addition and acyl substitution is:", "A tetrahedral alkoxide", "A carbocation", "A radical", "An enol"),
    ("Which gives a tertiary alcohol with one equivalent of CH₃MgBr, then aqueous acid?", "A ketone", "An aldehyde other than formaldehyde", "Formaldehyde", "CO₂")],
    "Draw the tetrahedral intermediate and ask whether anything on that carbon can leave as a base weaker than the nucleophile that came in")),
 ("OR-4.2.B", F("or-acetal-facts", CB, [
    ("An aldehyde with one equivalent of an alcohol (acid catalyst) gives:", "A hemiacetal", "An acetal", "An ester", "An ether"),
    ("An acetal is stable to:", "Bases and nucleophiles", "Aqueous acid", "Both aqueous acid and base", "Neither acid nor base"),
    ("Acetal formation is driven to completion by:", "Removing water", "Adding water", "Adding base", "Cooling"),
    ("A ketone is protected as a cyclic acetal with ethylene glycol so that:", "A Grignard or hydride reagent can react elsewhere in the molecule", "It becomes more electrophilic", "It can be oxidised", "It becomes acidic")],
    "An acetal is two ether-like C–O bonds on one carbon: no C=O for a nucleophile to attack, and removed again with aqueous acid")),
 ("OR-4.2.C", F("or-alpha-pka", EN, [
    ("Approximate pKa of the α-hydrogen of a ketone:", "About 20", "About 5", "About 36", "About 50"),
    ("Approximate pKa of the α-hydrogen of an ester:", "About 25", "About 10", "About 16", "About 44"),
    ("Approximate pKa of the central CH₂ of a β-diketone:", "About 9", "About 20", "About 25", "About 36"),
    ("α-Hydrogens are acidic because the conjugate base:", "Is an enolate, with the charge delocalised onto oxygen", "Has an sp-hybridised carbon", "Loses the carbonyl group", "Is stabilised by alkyl induction")],
    "One carbonyl makes a C–H about as acidic as an alkyne-plus; two flanking carbonyls bring it down near phenol")),
 ("OR-4.2.C", F("or-enolate-choice", EN, [
    ("LDA in THF at −78 °C removes which α-hydrogen of 2-methylcyclohexanone?", "The less hindered one, giving the kinetic enolate", "The more substituted one, giving the thermodynamic enolate", "Both equally", "Neither"),
    ("Sodium ethoxide in ethanol at room temperature gives mainly, from 2-methylcyclohexanone:", "The more substituted (thermodynamic) enolate, by equilibration", "The kinetic enolate only", "No enolate at all", "An enamine"),
    ("LDA converts a ketone to its enolate essentially completely because diisopropylamine's pKa is about:", "36, far above the ketone's 20", "10, below the ketone's 20", "20, the same as the ketone's", "5"),
    ("Ethoxide gives only a small equilibrium amount of a ketone's enolate because ethanol's pKa is about:", "16, below the ketone's 20", "36", "50", "25")],
    "Strong, bulky, cold and irreversible gives the kinetic enolate; weaker base, warm and reversible lets the more stable enolate win")),
 ("OR-5.2.A", L("or-acyl-forward", AC, "{{q}} Without further activation, this:", ["Goes forward", "Does not go forward"], [
    ("An acyl chloride and ammonia, to give an amide.", 0), ("An amide and chloride ion, to give an acyl chloride.", 1), ("An anhydride and ethanol, to give an ester.", 0), ("An ester and chloride ion, to give an acyl chloride.", 1),
    ("An ester and ammonia, to give an amide.", 0), ("An amide and ethanol alone, to give an ester.", 1), ("An acyl chloride and water, to give a carboxylic acid.", 0), ("A carboxylate ion and ethanol, to give an ester.", 1)],
    "Downhill only: acyl chloride → anhydride → ester → amide. The group expelled must be a weaker base than the nucleophile that attacked")),
 ("OR-5.2.A", F("or-hydrolysis-conditions", AC, [
    ("Base-promoted ester hydrolysis (saponification) is irreversible because:", "The carboxylic acid formed is deprotonated to a carboxylate", "Alkoxide is an excellent leaving group", "Water is removed", "The ester is volatile"),
    ("Acid-catalysed ester hydrolysis is:", "Reversible: the reverse of Fischer esterification", "Irreversible", "A radical reaction", "Impossible"),
    ("Which derivative needs the harshest conditions to hydrolyse?", "An amide", "An acyl chloride", "An anhydride", "An ester"),
    ("A carboxylic acid is converted to an acyl chloride with:", "SOCl₂", "NaCl", "Aqueous HCl", "Cl₂ and light")],
    "To go uphill (acid to acyl chloride) you need a reagent that makes OH a leaving group; to hydrolyse the least reactive derivative you need heat and strong acid or base")),
 ("OR-5.2.B", F("or-derivative-names", AC, [
    ("RCO–O–COR is:", "An anhydride", "An ester", "A ketone", "A peroxide"),
    ("A cyclic ester is called:", "A lactone", "A lactam", "An epoxide", "An acetal"),
    ("A cyclic amide is called:", "A lactam", "A lactone", "An imine", "An enamine"),
    ("R–C≡N is:", "A nitrile", "An isocyanate", "An imine", "An amide"),
    ("RCO–NR′₂ is:", "A tertiary amide", "A tertiary amine", "An imide", "An enamine")],
    "Find the C=O, then name what else is on that carbon: OR′ ester, N amide, O–C=O anhydride, Cl acyl chloride")),
 ("OR-5.2.B", F("or-hydrolysis-products", AC, [
    ("Hydrolysis of ethyl acetate gives:", "Acetic acid and ethanol", "Acetic anhydride and ethane", "Acetaldehyde and ethanol", "Ethane and CO₂"),
    ("Hydrolysis of N-methylacetamide gives:", "Acetic acid and methylamine", "Acetone and ammonia", "Methanol and acetamide", "Acetaldehyde and methylamine"),
    ("Hydrolysis of acetic anhydride gives:", "Two molecules of acetic acid", "Acetic acid and ethanol", "Acetone and CO₂", "Ethyl acetate"),
    ("Complete acidic hydrolysis of a nitrile gives:", "A carboxylic acid and ammonium ion", "An aldehyde", "A primary amine", "A ketone")],
    "Break the bond between the C=O carbon and the heteroatom; put OH on the carbon and H on the piece that left")),
 ("OR-6.2.A", F("or-eas-electrophile", AR, [
    ("HNO₃ with H₂SO₄ generates the electrophile:", "NO₂⁺ (nitronium)", "NO⁺", "NO₃⁻", "H₃O⁺"),
    ("CH₃COCl with AlCl₃ generates:", "An acylium ion, CH₃C≡O⁺", "A methyl cation", "A chlorine radical", "Chloride as the electrophile"),
    ("Br₂ needs FeBr₃ to brominate benzene because:", "Benzene is too unreactive for Br₂ alone; the Lewis acid polarises Br–Br", "FeBr₃ is the nucleophile", "FeBr₃ reduces the ring", "Br₂ is a base"),
    ("The intermediate of electrophilic aromatic substitution is:", "A resonance-stabilised carbocation (arenium ion)", "A carbanion", "A benzyne", "A radical"),
    ("Benzene substitutes rather than adds because losing H⁺ from the intermediate:", "Restores aromaticity", "Forms a stronger C–H bond", "Releases a radical", "Breaks the ring")],
    "Every aromatic substitution is the same two steps: the ring attacks a strong electrophile, then a base removes H⁺ to restore the aromatic ring")),
 ("OR-6.2.A", F("or-friedel-crafts-limits", AR, [
    ("Friedel–Crafts alkylation of benzene with 1-chloropropane gives mostly isopropylbenzene because:", "The incipient primary cation rearranges by a hydride shift", "Chloride attacks the ring", "Benzene rearranges", "AlCl₃ is bulky"),
    ("To make propylbenzene cleanly, use:", "Friedel–Crafts acylation, then reduce the C=O to CH₂", "Friedel–Crafts alkylation with 1-chloropropane", "Nitration, then reduction", "Bromination, then water"),
    ("Friedel–Crafts reactions fail on:", "Nitrobenzene and other strongly deactivated rings", "Toluene", "Anisole", "Benzene"),
    ("Alkylation tends to go on to polyalkylation because the product is:", "More activated than the starting ring", "Less activated than the starting ring", "Insoluble", "Antiaromatic")],
    "Acylium ions do not rearrange and the acyl product is deactivated, so acylation then reduction avoids both problems of alkylation")),
 ("OR-6.2.B", L("or-eas-order", AR, "To make {{q}}:", ["Do the first-named step first", "Do the second-named step first", "Either order gives the same product"], [
    ("m-bromonitrobenzene from benzene by nitration and bromination", 0), ("p-bromonitrobenzene from benzene by nitration and bromination", 1),
    ("m-chloroacetophenone from benzene by acylation and chlorination", 0), ("p-chloroacetophenone from benzene by acylation and chlorination", 1),
    ("p-nitrobenzoic acid from toluene by nitration and side-chain oxidation", 0), ("m-nitrobenzoic acid from toluene by nitration and side-chain oxidation", 1)],
    "The group already on the ring decides where the next goes. Put on the meta director first for a meta product, the ortho/para director first for a para product; CH₃ directs para but CO₂H directs meta")),
 ("OR-6.2.B", F("or-directing-why", AR, [
    ("Halogens deactivate the ring yet direct ortho/para because they:", "Withdraw by induction but donate a lone pair by resonance to the ortho/para intermediate", "Donate by induction", "Have no lone pairs", "Are bulky"),
    ("A nitro group directs meta because ortho or para attack would put the positive charge:", "On the carbon bearing the electron-withdrawing group", "On an oxygen", "Outside the ring", "On the meta carbon"),
    ("–OH and –NH₂ are strong activators because they:", "Donate a lone pair into the ring by resonance", "Withdraw by induction only", "Are bulky", "Are acidic"),
    ("When an activator and a deactivator on the ring disagree, the position is set by:", "The activator", "The deactivator", "Whichever is larger", "Neither; no reaction occurs")],
    "Draw the arenium ion for ortho, meta and para attack and look for the resonance form that puts + on the substituted carbon: a donor makes that form good, a withdrawer makes it bad")),
 ("OR-7.2.A", F("or-condensation-product-type", EN, [
    ("An aldol addition, without heating, gives:", "A β-hydroxy aldehyde or ketone", "An α,β-unsaturated carbonyl", "A β-keto ester", "A 1,5-dicarbonyl"),
    ("A Claisen condensation of two esters gives:", "A β-keto ester", "A β-hydroxy ester", "A 1,5-diester", "An α,β-unsaturated ester"),
    ("A Michael addition of an enolate to an α,β-unsaturated ketone gives:", "A 1,5-dicarbonyl compound", "A β-hydroxy ketone", "A β-keto ester", "A 1,2-diol"),
    ("A Robinson annulation is:", "A Michael addition followed by an intramolecular aldol condensation", "Two Claisen condensations", "A Diels–Alder reaction", "An aldol followed by a Wittig reaction"),
    ("In an aldol reaction the nucleophilic atom is:", "The α-carbon of an enolate", "The carbonyl oxygen", "The carbonyl carbon", "The oxygen of hydroxide")],
    "Number from one carbonyl to the other in the product: 1,3 (β-hydroxy or β-keto) means aldol or Claisen; 1,5 means Michael")),
 ("OR-7.2.A", F("or-condensation-conditions", EN, [
    ("A crossed aldol gives one main product when one partner:", "Has no α-hydrogens (for example benzaldehyde)", "Is a ketone", "Is chiral", "Is used in less than one equivalent"),
    ("A Claisen condensation needs a full equivalent of base because:", "The β-keto ester product is deprotonated, which pulls the equilibrium forward", "The base is consumed as a nucleophile", "Esters are strong acids", "Alkoxide escapes as a gas"),
    ("An intramolecular Claisen condensation is called:", "A Dieckmann condensation", "A Robinson annulation", "A Michael addition", "A Cannizzaro reaction"),
    ("Ethoxide is the base for a Claisen condensation of ethyl esters so that:", "Transesterification gives back the same ester", "The base is bulky", "No enolate forms", "The ester is hydrolysed")],
    "The Claisen equilibrium is unfavourable until the product, with a pKa near 11, gives up its proton to alkoxide")),
 ("OR-7.2.B", F("or-diels-alder-needs", EN, [
    ("A Diels–Alder diene must be able to adopt:", "The s-cis conformation", "The s-trans conformation only", "A chair", "An anti-periplanar geometry"),
    ("The fastest Diels–Alder reactions pair an electron-rich diene with:", "An electron-poor dienophile", "An electron-rich dienophile", "A radical", "A carbocation"),
    ("A Diels–Alder reaction forms:", "Two new σ bonds and a cyclohexene ring", "One σ bond and a cyclobutane", "Two new π bonds", "A cyclopentane"),
    ("Cyclopentadiene is an especially reactive diene because it is:", "Locked s-cis", "Aromatic", "Locked s-trans", "Electron-poor")],
    "Four carbons of the diene and two of the dienophile close a six-membered ring; the diene's ends must both reach the dienophile, which needs s-cis")),
 ("OR-7.2.B", F("or-diels-alder-outcome", EN, [
    ("A cis-disubstituted dienophile gives a product in which those two substituents are:", "Cis", "Trans", "A 1:1 mixture of cis and trans", "Lost"),
    ("With a cyclic diene the kinetically favoured product is usually:", "Endo", "Exo", "Meso", "The trans-fused one"),
    ("The Diels–Alder reaction is:", "Concerted: all bonds change in one step", "Stepwise through a carbocation", "Stepwise through a radical pair", "An SN2 reaction"),
    ("How many π electrons take part in the Diels–Alder transition state?", "6", "4", "2", "8")],
    "One step, no intermediate, so nothing can rotate: whatever was cis on the dienophile stays cis in the ring")),
 ("OR-11.1.A", F("or-ir-landmarks", SPEC, [
    ("A strong, sharp IR band near 1700 cm⁻¹ indicates:", "C=O", "O–H", "C≡N", "C–O"),
    ("A broad IR band at 3200–3600 cm⁻¹ indicates:", "The O–H of an alcohol", "C=O", "sp³ C–H", "C≡C"),
    ("A sharp IR band near 2250 cm⁻¹ indicates:", "C≡N", "C=O", "N–H", "C=C"),
    ("A very broad band from 2500 to 3300 cm⁻¹ with another near 1710 cm⁻¹ indicates:", "A carboxylic acid", "An ester", "A ketone", "An amine"),
    ("C–H stretches just above 3000 cm⁻¹ come from hydrogens on:", "sp² carbons", "sp³ carbons", "Oxygen", "Nitrogen")],
    "Read left to right: the X–H region above 2800, triple bonds near 2200, C=O near 1700")),
 ("OR-11.1.A", F("or-ir-distinguish", SPEC, [
    ("Which IR feature tells 1-hexyne from 2-hexyne?", "A sharp ≡C–H band near 3300 cm⁻¹", "A C=O band near 1700 cm⁻¹", "sp³ C–H bands below 3000 cm⁻¹", "A broad O–H band"),
    ("Which IR feature tells an alcohol from an ether?", "A broad O–H band at 3200–3600 cm⁻¹", "A C–O band near 1100 cm⁻¹", "sp³ C–H bands", "A band near 1700 cm⁻¹"),
    ("A primary amine, RNH₂, shows how many N–H stretching bands?", "Two", "One", "None", "Three"),
    ("An amide C=O absorbs at lower wavenumber than an ester C=O because the amide C=O:", "Has more single-bond character from nitrogen's resonance donation", "Is attached to a heavier atom only", "Is not polar", "Is hydrogen-bonded to carbon"),
    ("Conjugating a C=O with a C=C moves its band:", "To lower wavenumber", "To higher wavenumber", "Not at all", "Out of the infrared")],
    "A weaker (more single-bond-like) C=O vibrates at lower frequency; resonance donation and conjugation both weaken it")),
 ("OR-11.1.B", N("or-nmr-splitting", SPEC, "A proton has {{kn}} equivalent neighbouring protons (and no others). Into how many peaks is its signal split?", "kn + 1", "summation(1, (nn, 0, kn))",
    "The n + 1 rule: each neighbour can be spin up or down, giving n + 1 distinguishable combinations", tex="peaks", final=True,
    given={"kn": {"pick": [1, 2, 3, 4, 6, 9]}})),
 ("OR-11.1.B", F("or-nmr-shift-landmarks", SPEC, [
    ("A ¹H signal at 9–10 ppm is:", "An aldehyde H", "An alkyl CH₃", "A vinyl H", "An O–CH₃"),
    ("¹H signals at 6.5–8 ppm are:", "Aromatic H", "Alkyl H", "Aldehyde H", "Carboxylic acid H"),
    ("A 3H singlet near 3.7 ppm is most likely:", "O–CH₃", "C–CH₃ of an alkane", "An aldehyde H", "An aromatic H"),
    ("A 3H singlet near 2.1 ppm is most likely:", "CH₃ next to a C=O", "O–CH₃", "An aromatic H", "CH₃ of an alkane chain"),
    ("A broad 1H signal at 10–12 ppm is:", "A carboxylic acid O–H", "An alkyne C–H", "A vinyl H", "An alkyl C–H"),
    ("A 3H triplet near 1.2 ppm with a 2H quartet near 4.1 ppm indicates:", "An ethyl group on oxygen, –OCH₂CH₃", "An isopropyl group", "A tert-butyl group", "An ethyl group on a C=O")],
    "The closer a hydrogen is to an electronegative atom or a π system, the further downfield it appears")),
 ("OR-11.1.C", F("or-ms-patterns", SPEC, [
    ("M and M + 2 peaks of about equal height indicate one:", "Bromine", "Chlorine", "Sulfur", "Nitrogen"),
    ("M and M + 2 peaks in about a 3:1 ratio indicate one:", "Chlorine", "Bromine", "Fluorine", "Oxygen"),
    ("For a compound of C, H, N and O, an odd molecular-ion mass indicates:", "An odd number of nitrogens", "No nitrogen", "An even number of nitrogens", "A ring"),
    ("The base peak of a mass spectrum is:", "The most intense peak, set to 100%", "Always the molecular ion", "The peak of highest m/z", "The peak of lowest m/z")],
    "⁷⁹Br and ⁸¹Br are nearly 1:1; ³⁵Cl and ³⁷Cl are about 3:1. Nitrogen has an even mass but an odd valence, which is where the nitrogen rule comes from")),
 ("OR-11.1.C", F("or-ms-fragments", SPEC, [
    ("A peak at M − 15 corresponds to loss of:", "CH₃", "H₂O", "C₂H₅", "CO"),
    ("A peak at M − 18 from an alcohol corresponds to loss of:", "H₂O", "CH₃", "OH", "NH₃"),
    ("A strong peak at m/z 43 from a methyl ketone is:", "The acylium ion CH₃CO⁺", "The molecular ion", "CO₂⁺", "The tropylium ion"),
    ("A strong peak at m/z 91 suggests:", "A benzyl group (tropylium ion)", "A phenol", "A tert-butyl group", "A bromine atom"),
    ("A peak at m/z 77 suggests:", "A phenyl group", "A benzyl group", "An acetyl group", "A propyl group")],
    "Fragments that are stable cations dominate: acylium, benzylic/tropylium, tertiary")),
]
NEEDS = {
 "OR-1.3.A": ["CH-2.7.B"], "OR-1.3.B": ["OR-1.3.A", "CH-8.7.A"], "OR-1.2.A": ["OR-1.3.B"], "OR-1.3.C": ["OR-1.3.B"], "OR-1.3.D": ["OR-1.3.A"],
 "OR-1.4.A": ["OR-1.3.A"], "OR-9.1.A": ["OR-1.4.A"], "OR-1.4.B": ["OR-1.1.B"], "OR-1.4.C": ["OR-1.4.B"], "OR-1.4.D": ["OR-1.4.B"],
 "OR-2.3.A": ["OR-1.3.D", "OR-1.4.D"], "OR-2.3.B": ["OR-2.3.A"], "OR-2.1.A": ["OR-2.3.B"], "OR-2.1.B": ["OR-2.3.A"], "OR-2.2.A": ["OR-2.3.B"],
 "OR-3.2.A": ["OR-1.3.C", "OR-1.3.D"], "OR-3.2.B": ["OR-3.2.A"], "OR-1.2.C": ["OR-3.2.B"], "OR-3.2.C": ["OR-3.2.B", "OR-1.4.B"], "OR-3.2.D": ["OR-1.1.C", "OR-1.3.C"],
 "OR-3.1.A": ["OR-3.2.D", "OR-3.2.C"], "OR-3.1.B": ["OR-3.2.C", "OR-1.2.C"],
 "OR-4.2.A": ["OR-1.3.C"], "OR-4.2.B": ["OR-4.2.A"], "OR-4.1.A": ["OR-4.2.A"], "OR-4.1.B": ["OR-4.2.B"], "OR-4.2.C": ["OR-1.3.B", "OR-4.2.A"], "OR-4.1.C": ["OR-4.2.C"],
 "OR-5.2.B": ["OR-4.2.A"], "OR-5.2.A": ["OR-5.2.B", "OR-4.2.B"], "OR-5.1.A": ["OR-5.2.A"], "OR-5.1.B": ["OR-5.2.A"],
 "OR-6.2.A": ["OR-1.2.B", "OR-1.3.D"], "OR-6.1.A": ["OR-6.2.A"], "OR-6.2.B": ["OR-1.2.D", "OR-6.2.A"], "OR-6.1.B": ["OR-6.2.B"],
 "OR-7.2.A": ["OR-4.2.C"], "OR-7.2.B": ["OR-1.2.B", "OR-1.4.D"], "OR-7.1.A": ["OR-7.2.A", "OR-7.2.B"],
 "OR-11.1.A": ["OR-1.3.A"], "OR-11.1.B": ["OR-11.1.A"], "OR-11.1.C": ["OR-1.1.A"],
}
