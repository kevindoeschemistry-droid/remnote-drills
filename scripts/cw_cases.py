"""Cotton & Wilkinson, Advanced Inorganic Chemistry 6e → drills/problems/cw-*.yaml (framework inorganic-advanced).

Answers here come from tables typed in this file. tests/verify/cwcalc.py (and incalc's ox_state)
recompute them by rule, or look facts up in CW_FACTS, a second table typed there. Keep the two
separate: a fact entered once in both places is checked by nothing.

    python3 scripts/cw_cases.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "drills/problems"
SHAPES = ["linear", "trigonal planar", "bent", "tetrahedral", "trigonal pyramidal", "trigonal bipyramidal", "seesaw",
          "T-shaped", "octahedral", "square pyramidal", "square planar", "pentagonal bipyramidal", "distorted octahedral"]


def q(s):
    return "'" + str(s).replace("'", "''") + "'"


def shape_cases(rows):
    """rows: (label, centre, ligands, charge, shape, near1, near2, near3)"""
    out = []
    for lab, c, lig, ch, shp, *near in rows:
        assert shp in SHAPES and all(n in SHAPES and n != shp for n in near), lab
        out.append(f"    - {{ sp: {q(lab)}, cen: {q(c)}, lig: {q(lig)}, ch: {ch}, o1: {q(shp)}, o2: {q(near[0])}, o3: {q(near[1])}, o4: {q(near[2])} }}")
    return "\n".join(out)


def fact_cases(rows, extra=""):
    """rows: (key, prompt fill, right, wrong1, wrong2, wrong3)"""
    return "\n".join(f"    - {{ key: {q(k)}, f: {q(f)}, o1: {q(a)}, o2: {q(b)}, o3: {q(c)}, o4: {q(d)} }}" for k, f, a, b, c, d in rows)


def shape_t(name, skill, rows, intro, explain):
    return f"""- template: {name}
  skill: {skill}
  pace: recall
  cases:
{shape_cases(rows)}
  prompt: '{intro}'
  parts:
    - {{ ask: 'Shape', label: a, choice: ["{{{{o1}}}}", "{{{{o2}}}}", "{{{{o3}}}}", "{{{{o4}}}}"], correct: 0, explain: {q(explain)} }}
  verify: {{ choices: {{ a: "cw_shape_pick(cen, lig, ch, o1, o2, o3, o4)" }} }}
"""


def fact_t(name, skill, rows, prompt, explain):
    return f"""- template: {name}
  skill: {skill}
  pace: recall
  cases:
{fact_cases(rows)}
  prompt: {q(prompt)}
  parts:
    - {{ ask: 'Answer', label: a, choice: ["{{{{o1}}}}", "{{{{o2}}}}", "{{{{o3}}}}", "{{{{o4}}}}"], correct: 0, explain: {q(explain)} }}
  verify: {{ choices: {{ a: "cw_fact_pick(key, o1, o2, o3, o4)" }} }}
"""


def ox_t(name, skill, rows, explain):
    """rows: (shown formula, ascii formula, charge, element, answer)"""
    from fractions import Fraction
    cases = "\n".join(f"    - {{ sp: {q(s)}, fm: {q(f)}, ch: {c}, el: {q(e)}, n: {float(Fraction(str(n)))!r} }}" for s, f, c, e, n in rows)
    return f"""- template: {name}
  skill: {skill}
  pace: quick
  cases:
{cases}
  prompt: 'What is the (average) oxidation state of {{{{el}}}} in {{{{sp}}}}?'
  parts:
    - {{ ask: 'Oxidation state', label: y, tex: 'ox', value: n, tol: 0.002, explain: {q(explain)} }}
  verify: {{ expect: {{ y: "ox_state(fm, ch, el)" }} }}
"""


def mo_t(name, skill, rows, what, explain):
    """rows: (shown, atom a, atom b, charge, answer); what = 'bond order' | 'unpaired'"""
    cases = "\n".join(f"    - {{ sp: {q(s)}, A1: {q(a)}, A2: {q(b)}, ch: {c}, n: {n} }}" for s, a, b, c, n in rows)
    fn = "cw_bond_order" if what == "bond order" else "cw_unpaired_mo"
    ask = "Bond order" if what == "bond order" else "Unpaired electrons"
    prompt = ("What is the bond order of {{sp}} from its molecular-orbital diagram?" if what == "bond order"
              else "How many unpaired electrons does {{sp}} have in its ground state (molecular-orbital picture)?")
    return f"""- template: {name}
  skill: {skill}
  pace: quick
  cases:
{cases}
  prompt: {q(prompt)}
  parts:
    - {{ ask: {q(ask)}, label: y, tex: 'n', value: n, tol: 0.002, explain: {q(explain)} }}
  verify: {{ expect: {{ y: "{fn}(A1, A2, ch)" }} }}
"""


MG = "inorg.main-group"
T = []

# ── 1 · cross-cutting topics ─────────────────────────────────────────────
T.append(fact_t("cw-hsab-class", "inorg.cross-cutting", [
    ("hsab:Fe3+", "Fe³⁺", "Hard", "Soft", "Borderline", "Neither: HSAB applies only to bases"),
    ("hsab:Hg2+", "Hg²⁺", "Soft", "Hard", "Borderline", "Neither: HSAB applies only to bases"),
    ("hsab:Ag+", "Ag⁺", "Soft", "Hard", "Borderline", "Neither: HSAB applies only to bases"),
    ("hsab:Cu2+", "Cu²⁺", "Borderline", "Hard", "Soft", "Neither: HSAB applies only to bases"),
    ("hsab:F-", "F⁻", "Hard", "Soft", "Borderline", "Neither: HSAB applies only to acids"),
    ("hsab:I-", "I⁻", "Soft", "Hard", "Borderline", "Neither: HSAB applies only to acids"),
    ("hsab:Mg2+", "Mg²⁺", "Hard", "Soft", "Borderline", "Neither: HSAB applies only to bases"),
], "In Pearson's HSAB scheme, is {{f}} hard, soft or borderline?",
    "Hard: small, highly charged, weakly polarisable (Mg²⁺, Al³⁺, Fe³⁺, F⁻, O donors). Soft: large, polarisable, low charge (Ag⁺, Hg²⁺, Pt²⁺, I⁻, S donors). Hard prefers hard, soft prefers soft: why Hg is found as cinnabar, HgS."))

T.append("""- template: cw-latimer-skip
  skill: inorg.cross-cutting
  pace: quick
  given: { n1: { pick: [1, 2] }, e1: { pick: [0.56, 1.68, 0.77] }, n2: { pick: [1, 2, 3] }, e2: { pick: [2.26, 0.95, -0.44] } }
  prompt: 'A Latimer diagram shows two consecutive steps: ${{n1}}$ electron(s) at $E° = {{e1}}$ V, then ${{n2}}$ electron(s) at $E° = {{e2}}$ V. What is $E°$ for the combined ${{n1 + n2}}$-electron couple, in V?'
  parts:
    - { ask: 'E° (V)', label: y, tex: 'E°', value: (n1*e1 + n2*e2)/(n1 + n2), tol: 0.002, explain: 'Potentials do not add; free energies do. $\\Delta G = -nFE$ for each step, add them, then divide by the total electrons: $E = \\dfrac{n_1E_1 + n_2E_2}{n_1 + n_2}$' }
  verify: { expect: { y: "cw_latimer(n1, e1, n2, e2)" } }
""")

T.append("""- template: cw-disproportionation
  skill: inorg.cross-cutting
  pace: quick
  cases:
    - { sp: 'Cu⁺ (Cu²⁺ 0.15 V Cu⁺ 0.52 V Cu)', left: 0.15, right: 0.52 }
    - { sp: 'MnO₄²⁻ (MnO₄⁻ 0.56 V MnO₄²⁻ 2.26 V MnO₂)', left: 0.56, right: 2.26 }
    - { sp: 'Fe²⁺ (Fe³⁺ 0.77 V Fe²⁺ −0.44 V Fe)', left: 0.77, right: -0.44 }
    - { sp: 'H₂O₂ (O₂ 0.70 V H₂O₂ 1.76 V H₂O)', left: 0.70, right: 1.76 }
    - { sp: 'Hg₂²⁺ (Hg²⁺ 0.91 V Hg₂²⁺ 0.80 V Hg)', left: 0.91, right: 0.80 }
  prompt: 'From the Latimer diagram for {{sp}}, what is $E°$ for the species disproportionating into its neighbours, in V (positive means it disproportionates)?'
  parts:
    - { ask: 'E° (V)', label: y, tex: 'E°', value: right - left, tol: 0.002, explain: 'A species disproportionates when the potential to its right exceeds the one to its left: $E° = E_{right} - E_{left} > 0$. On a Frost diagram it sits above the line joining its neighbours' }
  verify: { expect: { y: "-(left - right)" } }
""")

# ── 2 · hydrogen ─────────────────────────────────────────────────────────
T.append(fact_t("cw-hydride-type", MG, [
    ("hydride:NaH", "NaH", "Ionic (saline)", "Covalent (molecular)", "Metallic (interstitial)", "Polymeric (electron-deficient)"),
    ("hydride:CaH2", "CaH₂", "Ionic (saline)", "Covalent (molecular)", "Metallic (interstitial)", "Polymeric (electron-deficient)"),
    ("hydride:CH4", "CH₄", "Covalent (molecular)", "Ionic (saline)", "Metallic (interstitial)", "Polymeric (electron-deficient)"),
    ("hydride:NH3", "NH₃", "Covalent (molecular)", "Ionic (saline)", "Metallic (interstitial)", "Polymeric (electron-deficient)"),
    ("hydride:PdH0.6", "PdH₀.₆", "Metallic (interstitial)", "Ionic (saline)", "Covalent (molecular)", "Polymeric (electron-deficient)"),
    ("hydride:TiH2", "TiH₂", "Metallic (interstitial)", "Ionic (saline)", "Covalent (molecular)", "Polymeric (electron-deficient)"),
], "What kind of hydride is {{f}}?",
    "Electropositive s-block metals give saline hydrides with H⁻ (they react with water to give H₂); p-block elements give molecular hydrides; many d-block metals take up hydrogen into interstices, often non-stoichiometrically."))

T.append("""- template: cw-isotope-shift
  skill: inorg.main-group
  pace: quick
  cases:
    - { b: 'C–H', nu: 2900, mX: 12 }
    - { b: 'O–H', nu: 3600, mX: 16 }
    - { b: 'N–H', nu: 3400, mX: 14 }
    - { b: 'S–H', nu: 2570, mX: 32 }
  prompt: 'A {{b}} stretch appears at ${{nu}}$ cm⁻¹. Treating it as a diatomic oscillator, where does the deuterated bond absorb, in cm⁻¹? (Masses H 1, D 2, X = ${{mX}}$.)'
  parts:
    - { ask: 'Wavenumber (cm⁻¹)', label: y, tex: '\\tilde\\nu_D', value: nu*sqrt((1*mX/(1 + mX))/(2*mX/(2 + mX))), tol: 0.002, explain: 'Same force constant, so $\\tilde\\nu \\propto 1/\\sqrt\\mu$. The ratio is close to $1/\\sqrt2$ because X is much heavier than H: deuteration shifts the band by about 0.73' }
  verify: { expect: { y: "nu*cw_isotope_ratio(1, 2, mX)" } }
""")

# ── 3–4 · groups 1 and 2 ─────────────────────────────────────────────────
T.append(fact_t("cw-alkali-burn", MG, [
    ("burn:Li", "lithium", "Li₂O", "Li₂O₂", "LiO₂", "Li₃N only"),
    ("burn:Na", "sodium", "Na₂O₂", "Na₂O", "NaO₂", "Na₃N"),
    ("burn:K", "potassium", "KO₂", "K₂O", "K₂O₂", "K₃N"),
    ("burn:Cs", "caesium", "CsO₂", "Cs₂O", "Cs₂O₂", "Cs₃N"),
], "What is the main product when {{f}} burns in excess air?",
    "Large cations stabilise large anions: Li gives the oxide O²⁻, Na the peroxide O₂²⁻, K, Rb and Cs the superoxide O₂⁻. Lithium also forms the nitride, like magnesium (the diagonal relationship)."))

T.append(ox_t("cw-dioxygen-anion-ox", MG, [
    ("KO₂", "KO2", 0, "O", "-1/2"), ("Na₂O₂", "Na2O2", 0, "O", -1), ("Li₂O", "Li2O", 0, "Li", 1), ("BaO₂", "BaO2", 0, "O", -1),
], "Charge balance with the metal fixed by its group: in KO₂ each O carries −½ (superoxide, O₂⁻); in Na₂O₂ each carries −1 (peroxide, O₂²⁻)."))

T.append(fact_t("cw-carbonate-stability", MG, [
    ("carb:Mg,Ca,Ba", "MgCO₃, CaCO₃ and BaCO₃", "BaCO₃", "MgCO₃", "CaCO₃", "All decompose at the same temperature"),
    ("carb:Be,Mg,Sr", "BeCO₃, MgCO₃ and SrCO₃", "SrCO₃", "BeCO₃", "MgCO₃", "All decompose at the same temperature"),
    ("carb:Ca,Sr,Ba", "CaCO₃, SrCO₃ and BaCO₃", "BaCO₃", "CaCO₃", "SrCO₃", "All decompose at the same temperature"),
], "Which of {{f}} needs the highest temperature to decompose to the oxide and CO₂?",
    "Small, highly polarising cations distort the carbonate ion and favour the small oxide ion: thermal stability rises down group 2. BeCO₃ barely exists; BaCO₃ needs about 1300 °C."))

T.append(fact_t("cw-diagonal", MG, [
    ("diag:Li", "lithium", "Mg", "Na", "Be", "Ca"),
    ("diag:Be", "beryllium", "Al", "Mg", "B", "Ca"),
    ("diag:B", "boron", "Si", "Al", "C", "Be"),
], "By the diagonal relationship, which element does {{f}} resemble most?",
    "Moving right raises the charge density and moving down lowers it, so a diagonal step keeps the polarising power similar: Li–Mg (nitrides, carbonate decomposition), Be–Al (amphoteric, covalent chlorides), B–Si (acidic oxides, molecular hydrides)."))

# ── 5–6 · boron and group 13 ─────────────────────────────────────────────
T.append("""- template: cw-wade
  skill: inorg.main-group
  pace: quick
  cases:
    - { sp: 'B₆H₆²⁻', nB: 6, nH: 6, ch: -2, ans: 0 }
    - { sp: 'B₁₂H₁₂²⁻', nB: 12, nH: 12, ch: -2, ans: 0 }
    - { sp: 'B₅H₉', nB: 5, nH: 9, ch: 0, ans: 1 }
    - { sp: 'B₁₀H₁₄', nB: 10, nH: 14, ch: 0, ans: 1 }
    - { sp: 'B₄H₁₀', nB: 4, nH: 10, ch: 0, ans: 2 }
    - { sp: 'B₅H₁₁', nB: 5, nH: 11, ch: 0, ans: 2 }
  prompt: 'Use Wade''s rules: what kind of cluster is {{sp}}?'
  parts:
    - { ask: 'Cluster', label: a, choice: ["closo (n + 1 skeletal pairs)", "nido (n + 2)", "arachno (n + 3)"], correct: ans, explain: 'Each BH unit gives 2 skeletal electrons; every extra H gives 1 and every negative charge 1. Count the pairs and compare with the number of boron atoms n: closo is a closed deltahedron, nido has one vertex missing, arachno two' }
  verify: { choices: { a: "cw_wade(nB, nH, ch)" } }
""")

T.append(fact_t("cw-bx3-acid", MG, [
    ("bx3", "BF₃, BCl₃ and BBr₃", "BBr₃", "BF₃", "BCl₃", "All equal: boron has the same empty p orbital"),
], "Which of {{f}} is the strongest Lewis acid toward NH₃?",
    "The opposite of what electronegativity suggests: in BF₃ the filled F 2p orbitals π-donate into boron's empty 2p, and that π bond must be lost on forming the adduct. The overlap is weaker with Cl and Br, so BBr₃ is the strongest acid."))

T.append(fact_t("cw-inert-pair", MG, [
    ("inert:Tl", "thallium", "+1", "+3", "+2", "0"),
    ("inert:Pb", "lead", "+2", "+4", "+1", "0"),
    ("inert:Bi", "bismuth", "+3", "+5", "+1", "0"),
], "Which oxidation state is the more stable one for {{f}} in its compounds?",
    "Down groups 13–15 the ns² pair holds on: Tl(I), Pb(II) and Bi(III) are the common states, and Tl(III), Pb(IV), Bi(V) are strong oxidants (PbO₂ in car batteries, NaBiO₃ oxidising Mn²⁺)."))

T.append(ox_t("cw-group13-ox", MG, [
    ("GaCl₂ (really Ga⁺[GaCl₄]⁻)", "GaCl2", 0, "Ga", 2), ("TlI₃ (really Tl⁺[I₃]⁻)", "TlI3", 0, "Tl", 3), ("Al₂Cl₆", "Al2Cl6", 0, "Cl", -1),
    ("In₂O₃", "In2O3", 0, "In", 3),
], "Charge balance gives the average, which can hide the real states: GaCl₂ averages +2 but holds Ga(I) and Ga(III); TlI₃ looks like Tl(III) but is Tl⁺ with triiodide."))

# ── 7–8 · carbon and group 14 ────────────────────────────────────────────
T.append(fact_t("cw-carbide-type", MG, [
    ("carbide:CaC2", "CaC₂", "Ionic (acetylide)", "Ionic (methanide)", "Covalent", "Interstitial"),
    ("carbide:Al4C3", "Al₄C₃", "Ionic (methanide)", "Ionic (acetylide)", "Covalent", "Interstitial"),
    ("carbide:SiC", "SiC", "Covalent", "Ionic (acetylide)", "Ionic (methanide)", "Interstitial"),
    ("carbide:WC", "WC", "Interstitial", "Ionic (acetylide)", "Ionic (methanide)", "Covalent"),
], "What kind of carbide is {{f}}?",
    "Saline carbides hydrolyse: acetylides (C₂²⁻) give ethyne, methanides (C⁴⁻) give methane. SiC is a diamond-like network; W, Ti and V carbides put C in the metal's interstices, hard and refractory."))

T.append("""- template: cw-fullerene-rings
  skill: inorg.main-group
  pace: quick
  given: { n: { pick: [60, 70, 76, 84, 240] } }
  prompt: 'A closed fullerene C$_{ {{n}} }$ has only five- and six-membered rings, each carbon in three of them. How many hexagons does it have?'
  parts:
    - { ask: 'Hexagons', label: y, tex: 'h', value: n/2 - 10, tol: 0.002, explain: 'Euler: $V - E + F = 2$ with $E = 3V/2$ forces exactly 12 pentagons for any size, and the rest hexagons: $h = n/2 - 10$. C₆₀ has 20' }
  verify: { expect: { y: "cw_fullerene_hex(n)" } }
""")

T.append(mo_t("cw-isoelectronic-bond-order", MG, [
    ("CO", "C", "O", 0, 3), ("CN⁻", "C", "N", -1, 3), ("NO⁺", "N", "O", 1, 3), ("C₂²⁻ (acetylide)", "C", "C", -2, 3),
    ("C₂", "C", "C", 0, 2), ("NO", "N", "O", 0, 2.5), ("CN", "C", "N", 0, 2.5),
], "bond order", "Count valence electrons and fill σ2s, σ*2s, then (for up to ten valence electrons) π2p before σ2p. CO, CN⁻, NO⁺ and C₂²⁻ are all isoelectronic with N₂: bond order 3."))

T.append("""- template: cw-silicate-ratio
  skill: inorg.main-group
  pace: quick
  cases:
    - { sp: 'an orthosilicate (isolated tetrahedra, as in olivine)', s: 0, f: 4 }
    - { sp: 'a pyrosilicate (pairs sharing one corner, Si₂O₇⁶⁻)', s: 1, f: 3.5 }
    - { sp: 'a chain or ring silicate (pyroxene, two corners shared)', s: 2, f: 3 }
    - { sp: 'a sheet silicate (mica, talc: three corners shared)', s: 3, f: 2.5 }
    - { sp: 'a framework (quartz, all four corners shared)', s: 4, f: 2 }
  prompt: 'In {{sp}}, each SiO₄ tetrahedron shares ${{s}}$ corner(s). How many oxygen atoms are there per silicon?'
  parts:
    - { ask: 'O per Si', label: y, tex: 'O/Si', value: f, tol: 0.002, explain: 'A shared O counts half to each Si: O/Si = (4 − s) + s/2. That gives SiO₄⁴⁻, Si₂O₇⁶⁻, (SiO₃²⁻)ₙ, (Si₂O₅²⁻)ₙ and SiO₂' }
  verify: { expect: { y: "cw_silicate_ratio(s)" } }
""")

T.append(shape_t("cw-group14-shape", MG, [
    ("SnCl₂ (gas)", "Sn", "Cl2", 0, "bent", "linear", "trigonal planar", "T-shaped"),
    ("SnCl₃⁻", "Sn", "Cl3", -1, "trigonal pyramidal", "trigonal planar", "tetrahedral", "T-shaped"),
    ("SiF₆²⁻", "Si", "F6", -2, "octahedral", "trigonal bipyramidal", "square planar", "tetrahedral"),
    ("CO₂", "C", "O2", 0, "linear", "bent", "trigonal planar", "T-shaped"),
    ("CO₃²⁻", "C", "O3", -2, "trigonal planar", "trigonal pyramidal", "T-shaped", "tetrahedral"),
], "What is the shape of {{sp}}?", "VSEPR: count the centre's valence electrons, subtract one per single-bonded ligand and two per double-bonded O, adjust for charge, halve what is left for lone pairs. Sn(II) keeps a stereoactive lone pair: SnCl₂ is bent and SnCl₃⁻ pyramidal."))

# ── 9–10 · nitrogen and group 15 ─────────────────────────────────────────
T.append(ox_t("cw-nitrogen-ox", MG, [
    ("N₂O", "N2O", 0, "N", 1), ("NO", "NO", 0, "N", 2), ("N₂O₃", "N2O3", 0, "N", 3), ("NO₂", "NO2", 0, "N", 4),
    ("N₂O₅", "N2O5", 0, "N", 5), ("N₂H₄", "N2H4", 0, "N", -2), ("NH₂OH", "NH3O", 0, "N", -1), ("HN₃", "HN3", 0, "N", "-1/3"),
], "Nitrogen spans −3 (NH₃) to +5 (N₂O₅, HNO₃), and has a well-known compound at nearly every step: hydrazine −2, hydroxylamine −1, N₂ 0, N₂O +1, NO +2, N₂O₃ +3, NO₂ +4."))

T.append(mo_t("cw-no-family", MG, [
    ("NO⁺", "N", "O", 1, 3), ("NO", "N", "O", 0, 2.5), ("NO⁻", "N", "O", -1, 2), ("N₂⁺", "N", "N", 1, 2.5),
], "bond order", "NO has one electron in π*: removing it (NO⁺, isoelectronic with N₂ and CO) raises the bond order to 3 and shortens the bond; adding one (NO⁻) lowers it to 2."))

T.append(fact_t("cw-p-oxoacid", MG, [
    ("basic:H3PO2", "phosphinic acid, H₃PO₂", "1", "2", "3", "0"),
    ("basic:H3PO3", "phosphonic acid, H₃PO₃", "2", "1", "3", "0"),
    ("basic:H3PO4", "phosphoric acid, H₃PO₄", "3", "1", "2", "4"),
    ("basic:H4P2O7", "diphosphoric acid, H₄P₂O₇", "4", "2", "3", "1"),
], "How many protons can {{f}} give up in water?",
    "Only O–H hydrogens are acidic. H₃PO₃ is HPO(OH)₂ with one P–H; H₃PO₂ is H₂PO(OH) with two. So basicity is 1, 2, 3 for H₃PO₂, H₃PO₃, H₃PO₄."))

T.append(shape_t("cw-group15-shape", MG, [
    ("PF₅", "P", "F5", 0, "trigonal bipyramidal", "square pyramidal", "octahedral", "seesaw"),
    ("PCl₄⁺", "P", "Cl4", 1, "tetrahedral", "square planar", "seesaw", "trigonal pyramidal"),
    ("PCl₆⁻", "P", "Cl6", -1, "octahedral", "trigonal bipyramidal", "square planar", "pentagonal bipyramidal"),
    ("SbF₅²⁻", "Sb", "F5", -2, "square pyramidal", "trigonal bipyramidal", "octahedral", "seesaw"),
    ("NH₃", "N", "H3", 0, "trigonal pyramidal", "trigonal planar", "tetrahedral", "T-shaped"),
    ("SbCl₃", "Sb", "Cl3", 0, "trigonal pyramidal", "trigonal planar", "T-shaped", "tetrahedral"),
], "What is the shape of {{sp}}?", "Solid PCl₅ is [PCl₄]⁺[PCl₆]⁻: the same atoms, two shapes. A lone pair on the centre (NH₃, SbCl₃, SbF₅²⁻) takes a position of its own and pushes the ligands into the next shape down."))

# ── 11–12 · oxygen and group 16 ──────────────────────────────────────────
T.append(mo_t("cw-dioxygen-bond-order", MG, [
    ("O₂⁺", "O", "O", 1, 2.5), ("O₂", "O", "O", 0, 2), ("O₂⁻ (superoxide)", "O", "O", -1, 1.5), ("O₂²⁻ (peroxide)", "O", "O", -2, 1),
    ("F₂", "F", "F", 0, 1), ("N₂", "N", "N", 0, 3),
], "bond order", "Each electron added to π* lowers the bond order by ½: O₂⁺ 2.5, O₂ 2, superoxide 1.5, peroxide 1. Bond lengths follow: 112, 121, 133 and 149 pm."))

T.append(mo_t("cw-dioxygen-unpaired", MG, [
    ("O₂", "O", "O", 0, 2), ("O₂⁻", "O", "O", -1, 1), ("O₂⁺", "O", "O", 1, 1), ("B₂", "B", "B", 0, 2), ("C₂", "C", "C", 0, 0),
    ("O₂²⁻", "O", "O", -2, 0),
], "unpaired", "Two degenerate π* (or π) orbitals fill one electron each before pairing (Hund): O₂ has two unpaired electrons, which is why liquid oxygen sticks to a magnet and the Lewis structure cannot show it. B₂ is paramagnetic only because π lies below σ2p there."))

T.append(shape_t("cw-group16-shape", MG, [
    ("SF₄", "S", "F4", 0, "seesaw", "tetrahedral", "square planar", "trigonal pyramidal"),
    ("SF₆", "S", "F6", 0, "octahedral", "trigonal bipyramidal", "square planar", "pentagonal bipyramidal"),
    ("SO₂", "S", "O2", 0, "bent", "linear", "trigonal planar", "T-shaped"),
    ("SO₃", "S", "O3", 0, "trigonal planar", "trigonal pyramidal", "T-shaped", "tetrahedral"),
    ("SOCl₂", "S", "OCl2", 0, "trigonal pyramidal", "trigonal planar", "tetrahedral", "T-shaped"),
    ("O₃", "O", "O2", 0, "bent", "linear", "trigonal planar", "T-shaped"),
    ("TeCl₄", "Te", "Cl4", 0, "seesaw", "tetrahedral", "square planar", "trigonal pyramidal"),
], "What is the shape of {{sp}}?", "In a trigonal bipyramid the lone pair takes an equatorial site, where it has fewer 90° neighbours: SF₄ is a seesaw, not a distorted tetrahedron."))

T.append(ox_t("cw-sulfur-ox", MG, [
    ("S₂O₃²⁻ (thiosulfate)", "S2O3", -2, "S", 2), ("S₄O₆²⁻ (tetrathionate)", "S4O6", -2, "S", "5/2"),
    ("S₂O₄²⁻ (dithionite)", "S2O4", -2, "S", 3), ("S₂O₆²⁻ (dithionate)", "S2O6", -2, "S", 5),
    ("SO₃²⁻", "SO3", -2, "S", 4), ("H₂S", "H2S", 0, "S", -2),
], "Charge balance gives the average over the sulfur atoms. In thiosulfate the two S are not alike (one central S(VI)-like, one terminal S(−II)-like); averages of +2 and +2.5 are why iodometry's 2 S₂O₃²⁻ → S₄O₆²⁻ moves one electron per thiosulfate."))

# ── 13–14 · halogens and noble gases ─────────────────────────────────────
T.append(shape_t("cw-interhalogen-shape", MG, [
    ("ClF₃", "Cl", "F3", 0, "T-shaped", "trigonal planar", "trigonal pyramidal", "seesaw"),
    ("BrF₅", "Br", "F5", 0, "square pyramidal", "trigonal bipyramidal", "octahedral", "seesaw"),
    ("IF₇", "I", "F7", 0, "pentagonal bipyramidal", "octahedral", "distorted octahedral", "square pyramidal"),
    ("I₃⁻", "I", "I2", -1, "linear", "bent", "T-shaped", "trigonal planar"),
    ("ICl₄⁻", "I", "Cl4", -1, "square planar", "tetrahedral", "seesaw", "square pyramidal"),
    ("ClO₃⁻", "Cl", "O3", -1, "trigonal pyramidal", "trigonal planar", "T-shaped", "tetrahedral"),
], "What is the shape of {{sp}}?", "Interhalogens put the heavier halogen in the centre with an odd number of F around it. Lone pairs go where they have most room: equatorial in a trigonal bipyramid (ClF₃ T-shaped, I₃⁻ linear), trans in an octahedron (ICl₄⁻ square planar)."))

T.append(ox_t("cw-halogen-ox", MG, [
    ("ClO⁻", "ClO", -1, "Cl", 1), ("ClO₂⁻", "ClO2", -1, "Cl", 3), ("ClO₃⁻", "ClO3", -1, "Cl", 5), ("ClO₄⁻", "ClO4", -1, "Cl", 7),
    ("IO₆⁵⁻ (orthoperiodate)", "IO6", -5, "I", 7), ("BrO₃⁻", "BrO3", -1, "Br", 5), ("ClO₂", "ClO2", 0, "Cl", 4),
], "Each added O raises the state by 2 in the oxoanions; ClO₂, a radical with Cl(+4), is the odd one out. Fluorine is always −1."))

T.append(fact_t("cw-oxoacid-strength", MG, [
    ("oxo:Cl", "HOCl, HClO₂, HClO₃ and HClO₄", "HClO₄", "HOCl", "HClO₂", "HClO₃"),
], "Which of {{f}} is the strongest acid?",
    "More oxo groups pull electron density from O–H and spread the anion's charge: pKa runs 7.5, 2.0, about −1 and about −10. Pauling's rule: pKa ≈ 8 − 5p for (HO)ₘXOₚ."))

T.append(shape_t("cw-xenon-shape", MG, [
    ("XeF₂", "Xe", "F2", 0, "linear", "bent", "T-shaped", "trigonal planar"),
    ("XeF₄", "Xe", "F4", 0, "square planar", "tetrahedral", "seesaw", "square pyramidal"),
    ("XeF₆", "Xe", "F6", 0, "distorted octahedral", "octahedral", "pentagonal bipyramidal", "trigonal bipyramidal"),
    ("XeO₃", "Xe", "O3", 0, "trigonal pyramidal", "trigonal planar", "T-shaped", "tetrahedral"),
    ("XeO₄", "Xe", "O4", 0, "tetrahedral", "square planar", "seesaw", "trigonal pyramidal"),
    ("XeOF₄", "Xe", "OF4", 0, "square pyramidal", "trigonal bipyramidal", "octahedral", "seesaw"),
], "What is the shape of {{sp}}?", "Xenon brings 8 valence electrons. XeF₂ has three lone pairs (linear), XeF₄ two (square planar), XeF₆ one, stereoactive, which distorts the octahedron (it fluxes in the gas)."))

T.append(ox_t("cw-xenon-ox", MG, [
    ("XeF₂", "XeF2", 0, "Xe", 2), ("XeF₄", "XeF4", 0, "Xe", 4), ("XeO₃", "XeO3", 0, "Xe", 6), ("XeO₄", "XeO4", 0, "Xe", 8),
    ("XeO₆⁴⁻ (perxenate)", "XeO6", -4, "Xe", 8), ("XeOF₄", "XeOF4", 0, "Xe", 6),
], "Xenon compounds come in even oxidation states, +2 to +8, because the 5p and 5s electrons are promoted in pairs as bonds form. Only F and O are electronegative enough to oxidise it."))

# ── 15 · group 12 ────────────────────────────────────────────────────────
T.append(fact_t("cw-group12-facts", MG, [
    ("hg1", "mercury(I) in water", "Hg₂²⁺, with an Hg–Hg bond", "Hg⁺, a simple monatomic ion", "HgOH⁺", "It does not exist"),
    ("zno", "the oxide of zinc", "Amphoteric", "Basic only", "Acidic only", "Neutral"),
    ("d10colour", "the colour of most Zn²⁺ and Cd²⁺ compounds", "Colourless: a full d shell has no d–d transitions", "Blue, like Cu²⁺", "Pink, like Co²⁺", "Green, like Ni²⁺"),
], "What is true of {{f}}?",
    "Group 12 keeps a full d¹⁰ shell, so it behaves as a main-group metal: no d–d colour, mostly +2. Mercury is the exception with Hg₂²⁺, the first metal–metal bonded ion recognised."))

T.append(ox_t("cw-mercury-ox", MG, [
    ("Hg₂Cl₂ (calomel)", "Hg2Cl2", 0, "Hg", 1), ("HgCl₂", "HgCl2", 0, "Hg", 2), ("HgO", "HgO", 0, "Hg", 2),
    ("Hg₃²⁺", "Hg3", 2, "Hg", "2/3"), ("ZnO₂²⁻ as Zn(OH)₄²⁻", "ZnO4H4", -2, "Zn", 2),
], "Calomel is Hg(I) as the Hg₂²⁺ dimer; the formula HgCl would hide the Hg–Hg bond. Polymercury cations like Hg₃²⁺ carry fractional average states."))

if __name__ == "__main__":
    head = ("# Cotton & Wilkinson, Advanced Inorganic Chemistry 6e, chapters 1–15 (framework inorganic-advanced).\n"
            "# Generated by scripts/cw_cases.py: edit the script, not this file. Checked by tests/verify/cwcalc.py\n"
            "# (VSEPR, MO ladders, Wade, Euler, Latimer, CW_FACTS) and incalc's ox_state.\n\n")
    (ROOT / "cw-main-group.yaml").write_text(head + "\n".join(T))
    print(f"wrote {len(T)} templates")
