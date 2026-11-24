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


# ═════ Part 3–4: transition elements, f block, organometallic catalysis (ch. 16–22) ═════
T2 = []
TM, FB, OM = "inorg.transition", "inorg.f-block", "inorg.organometallic"


def num_t(name, skill, cases, prompt, ask, explain, verify, tol=0.002):
    return f"""- template: {name}
  skill: {skill}
  pace: quick
  cases:
{cases}
  prompt: {q(prompt)}
  parts:
    - {{ ask: {q(ask)}, label: y, tex: 'n', value: n, tol: {tol}, explain: {q(explain)} }}
  verify: {{ expect: {{ y: "{verify}" }} }}
"""


def rows(fields, data):
    return "\n".join("    - { " + ", ".join(f"{k}: {q(v) if isinstance(v, str) else v}" for k, v in zip(fields, r)) + " }" for r in data)


# ── 16 · survey of the transition elements ──
T2.append(num_t("cw-d-count", TM, rows(["sp", "M", "lg", "ch", "n"], [
    ("[Fe(CN)₆]⁴⁻", "Fe", "CN:6", -4, 6), ("[Fe(CN)₆]³⁻", "Fe", "CN:6", -3, 5), ("[Co(NH₃)₆]³⁺", "Co", "NH3:6", 3, 6),
    ("[Cr(H₂O)₆]³⁺", "Cr", "H2O:6", 3, 3), ("[MnO₄]⁻ written as Mn with four O²⁻", "Mn", "ox:0,F:0", 7, 0),
    ("[Ni(CN)₄]²⁻", "Ni", "CN:4", -2, 8), ("[CuCl₄]²⁻", "Cu", "Cl:4", -2, 9), ("[Ti(H₂O)₆]³⁺", "Ti", "H2O:6", 3, 1),
    ("[V(CO)₆]", "V", "CO:6", 0, 5), ("[PtCl₂(NH₃)₂]", "Pt", "Cl:2,NH3:2", 0, 8)]),
    "What is the dⁿ count of the metal in {{sp}}?", "d electrons",
    "Find the oxidation state by charge balance (neutral ligands 0, halides and CN⁻ −1), then dⁿ = group number − oxidation state.",
    "d_count(M, lg, ch)"))
T2[-1] = T2[-1].replace("    - { sp: '[MnO₄]⁻ written as Mn with four O²⁻', M: 'Mn', lg: 'ox:0,F:0', ch: 7, n: 0 }\n", "")

T2.append(num_t("cw-complex-unpaired", TM, rows(["sp", "M", "lg", "ch", "geo", "spn", "n"], [
    ("[Fe(H₂O)₆]²⁺", "Fe", "H2O:6", 2, "oct", "high", 4), ("[Fe(CN)₆]³⁻", "Fe", "CN:6", -3, "oct", "low", 1),
    ("[CoF₆]³⁻", "Co", "F:6", -3, "oct", "high", 4), ("[Mn(H₂O)₆]²⁺", "Mn", "H2O:6", 2, "oct", "high", 5),
    ("[Cr(H₂O)₆]³⁺", "Cr", "H2O:6", 3, "oct", "high", 3), ("[Cu(H₂O)₆]²⁺", "Cu", "H2O:6", 2, "oct", "high", 1),
    ("[NiCl₄]²⁻ (tetrahedral)", "Ni", "Cl:4", -2, "tet", "high", 2), ("[CoCl₄]²⁻ (tetrahedral)", "Co", "Cl:4", -2, "tet", "high", 3),
    ("[Mn(CN)₆]⁴⁻", "Mn", "CN:6", -4, "oct", "low", 1)]),
    "How many unpaired electrons does {{sp}} have?", "Unpaired electrons",
    "Get dⁿ from the oxidation state, then fill t₂g and e_g (octahedral) or e and t₂ (tetrahedral): weak-field ligands give high spin, CN⁻ low spin, and tetrahedral complexes are always high spin.",
    "unpaired(d_count(M, lg, ch), geo, spn)"))

T2.append(num_t("cw-spin-only-moment", TM, rows(["sp", "d", "spn", "n"], [
    ("an octahedral high-spin d⁵ ion", 5, "high", 35 ** 0.5), ("an octahedral low-spin d⁵ ion", 5, "low", 3 ** 0.5),
    ("an octahedral d³ ion", 3, "high", 15 ** 0.5), ("an octahedral high-spin d⁶ ion", 6, "high", 24 ** 0.5),
    ("an octahedral d⁹ ion", 9, "high", 3 ** 0.5), ("an octahedral d⁸ ion", 8, "high", 8 ** 0.5)]),
    "What is the spin-only magnetic moment of {{sp}}, in Bohr magnetons?", "μ (BM)",
    "μ_so = √(n(n + 2)) with n unpaired electrons: 1.73, 2.83, 3.87, 4.90, 5.92 for n = 1–5. First-row metals come close; orbital contributions push some higher (Co²⁺).",
    "spin_only(d, 'oct', spn)", tol=0.0005))

T2.append(num_t("cw-cfse", TM, rows(["sp", "d", "spn", "n"], [
    ("high-spin octahedral d⁴", 4, "high", -0.6), ("low-spin octahedral d⁴", 4, "low", -1.6), ("high-spin octahedral d⁶", 6, "high", -0.4),
    ("low-spin octahedral d⁶", 6, "low", -2.4), ("octahedral d³", 3, "high", -1.2), ("octahedral d⁸", 8, "high", -1.2),
    ("high-spin octahedral d⁷", 7, "high", -0.8)]),
    "What is the crystal-field stabilisation energy of a {{sp}} ion, in units of Δ_o (pairing energy aside)?", "CFSE (Δ_o)",
    "Each t₂g electron counts −0.4Δ_o and each e_g electron +0.6Δ_o. d⁰, high-spin d⁵ and d¹⁰ get nothing, which shows in the double hump of hydration enthalpies across the first row.",
    "cfse(d, 'oct', spn)"))

T2.append(fact_t("cw-spectrochemical", TM, [
    ("spectro:strongest:I,Cl,H2O,NH3,CN", "I⁻, Cl⁻, H₂O, NH₃ and CN⁻", "CN⁻", "I⁻", "H₂O", "NH₃"),
    ("spectro:strongest:F,OH,en,CO", "F⁻, OH⁻, en and CO", "CO", "F⁻", "OH⁻", "en"),
    ("spectro:weakest:I,F,NH3,CN", "I⁻, F⁻, NH₃ and CN⁻ (the weakest field)", "I⁻", "F⁻", "NH₃", "CN⁻"),
], "In the spectrochemical series, which of {{f}} gives the strongest field, unless the weakest is asked?",
    "I⁻ < Br⁻ < Cl⁻ < F⁻ < OH⁻ < H₂O < NH₃ < en < bpy < NO₂⁻ < CN⁻ < CO. π donors (halides) shrink Δ; π acceptors (CN⁻, CO) widen it."))

T2.append("""- template: cw-jahn-teller
  skill: inorg.transition
  pace: recall
  cases:
    - { sp: 'Cu²⁺ (d⁹)', d: 9, spn: 'high', k: 0 }
    - { sp: 'high-spin Cr²⁺ (d⁴)', d: 4, spn: 'high', k: 0 }
    - { sp: 'high-spin Mn³⁺ (d⁴)', d: 4, spn: 'high', k: 0 }
    - { sp: 'low-spin Co²⁺ (d⁷)', d: 7, spn: 'low', k: 0 }
    - { sp: 'Cr³⁺ (d³)', d: 3, spn: 'high', k: 1 }
    - { sp: 'high-spin Mn²⁺ (d⁵)', d: 5, spn: 'high', k: 1 }
    - { sp: 'Ni²⁺ (d⁸)', d: 8, spn: 'high', k: 1 }
    - { sp: 'low-spin Fe²⁺ (d⁶)', d: 6, spn: 'low', k: 1 }
  prompt: 'Does an octahedral complex of {{sp}} show a strong Jahn–Teller distortion?'
  parts:
    - { ask: 'Distortion', label: a, choice: ["Yes: the e_g level is unevenly filled", "No: no strong distortion expected"], correct: k, explain: 'A degenerate, unevenly filled e_g set (one or three electrons) points straight at the ligands and drives a tetragonal elongation: d⁹, high-spin d⁴, low-spin d⁷. Uneven t₂g filling gives only weak effects' }
  verify: { choices: { a: "cw_jahn_teller(d, spn)" } }
""")

T2.append("""- template: cw-labile-inert
  skill: inorg.transition
  pace: recall
  cases:
    - { sp: '[Cr(H₂O)₆]³⁺ (d³)', d: 3, spn: 'high', k: 0 }
    - { sp: '[Co(NH₃)₆]³⁺ (low-spin d⁶)', d: 6, spn: 'low', k: 0 }
    - { sp: '[Fe(H₂O)₆]²⁺ (high-spin d⁶)', d: 6, spn: 'high', k: 1 }
    - { sp: '[Cu(H₂O)₆]²⁺ (d⁹)', d: 9, spn: 'high', k: 1 }
    - { sp: '[Ni(H₂O)₆]²⁺ (d⁸)', d: 8, spn: 'high', k: 1 }
    - { sp: '[Mn(H₂O)₆]²⁺ (high-spin d⁵)', d: 5, spn: 'high', k: 1 }
  prompt: 'Is {{sp}} substitutionally inert or labile?'
  parts:
    - { ask: 'Kinetics', label: a, choice: ["Inert: ligand exchange takes hours or more", "Labile: exchange is fast"], correct: k, explain: 'Taube: d³ and low-spin d⁶ lose the most ligand-field stabilisation on the way to the transition state, so they swap ligands slowly. That is why Werner could separate Co(III) and Cr(III) isomers' }
  verify: { choices: { a: "cw_inert(d, spn)" } }
""")

# ── 17 · first transition series ──
T2.append(fact_t("cw-permanganate-product", TM, [
    ("mn:acid", "in acid", "Mn²⁺", "MnO₂", "MnO₄²⁻", "Mn"),
    ("mn:neutral", "in neutral solution", "MnO₂", "Mn²⁺", "MnO₄²⁻", "Mn"),
    ("mn:base", "in strong base", "MnO₄²⁻", "Mn²⁺", "MnO₂", "Mn"),
], "What does permanganate turn into when it acts as an oxidant {{f}}?",
    "Five electrons in acid (to pale pink Mn²⁺), three near neutral (to brown MnO₂), one in strong base (to green manganate). The same reagent changes its electron count with pH."))

T2.append(fact_t("cw-chromate-ph", TM, [
    ("cr:acid", "acid", "Orange Cr₂O₇²⁻", "Yellow CrO₄²⁻", "Green Cr³⁺", "Blue CrO₅"),
    ("cr:base", "base", "Yellow CrO₄²⁻", "Orange Cr₂O₇²⁻", "Green Cr³⁺", "Blue CrO₅"),
], "Chromium(VI) is dissolved in {{f}}. What dominates?",
    "2 CrO₄²⁻ + 2 H⁺ ⇌ Cr₂O₇²⁻ + H₂O: acid pushes right (orange), base left (yellow). Both are Cr(VI); no electrons change hands."))

T2.append(ox_t("cw-first-row-ox", TM, [
    ("VO²⁺ (vanadyl)", "VO", 2, "V", 4), ("FeO₄²⁻ (ferrate)", "FeO4", -2, "Fe", 6), ("Fe₃O₄ (magnetite)", "Fe3O4", 0, "Fe", "8/3"),
    ("Co₃O₄", "Co3O4", 0, "Co", "8/3"), ("NiO(OH)", "NiO2H", 0, "Ni", 3), ("Cu₂O", "Cu2O", 0, "Cu", 1), ("TiO₂", "TiO2", 0, "Ti", 4),
    ("CrO₅ (two peroxides; rule gives the average)", "CrO5", 0, "Cr", 10),
], "Mixed-valence oxides average out: magnetite is Fe²⁺Fe³⁺₂O₄ (+8/3). Charge balance with O = −2 fails for peroxides: CrO₅ is really Cr(VI) with two O₂²⁻ groups, not Cr(+10)."))
T2[-1] = T2[-1].replace("    - { sp: 'CrO₅ (two peroxides; rule gives the average)', fm: 'CrO5', ch: 0, el: 'Cr', n: 10.0 }\n", "")

# ── 18 · second and third series ──
T2.append(num_t("cw-metal-metal-bond", TM, rows(["sp", "d1", "d2", "n"], [
    ("[Re₂Cl₈]²⁻ (two Re(III), d⁴)", 4, 4, 4), ("Mo₂(O₂CCH₃)₄ (two Mo(II), d⁴)", 4, 4, 4), ("Cr₂(O₂CCH₃)₄ (two Cr(II), d⁴)", 4, 4, 4),
    ("Mo₂(NMe₂)₆ (two Mo(III), d³)", 3, 3, 3), ("[Os₂Cl₈]²⁻ (two Os(III), d⁵)", 5, 5, 3), ("Rh₂(O₂CCH₃)₄ (two Rh(II), d⁷)", 7, 7, 1)]),
    "What is the metal–metal bond order in {{sp}}?", "Bond order",
    "d–d overlap gives σ, two π and δ bonding orbitals, then δ*, π* and σ*. Eight d electrons fill σ²π⁴δ²: a quadruple bond, Cotton's [Re₂Cl₈]²⁻ (1964), held eclipsed by the δ bond.",
    "cw_mm_bond(d1, d2)"))

T2.append(fact_t("cw-heavy-tm-facts", TM, [
    ("radii:Zr,Hf", "the radii of Zr and Hf", "Almost the same (lanthanide contraction)", "Hf is much larger", "Zr is much larger", "Hf is larger by the same step as Ti to Zr"),
    ("spin:4d5d", "4d and 5d complexes, as a rule", "Low spin", "High spin", "Always diamagnetic", "Always tetrahedral"),
    ("trans:cisplatin", "the synthesis of cis-[PtCl₂(NH₃)₂]", "Start from PtCl₄²⁻ and add NH₃: Cl⁻ trans-directs the second NH₃ cis", "Start from Pt(NH₃)₄²⁺ and add Cl⁻", "Heat trans-[PtCl₂(NH₃)₂]", "Any order gives the same isomer"),
], "What is true of {{f}}?",
    "The 4f shell fills between La and Hf and shields poorly, so Hf ends up the size of Zr and the two are hard to separate. Larger 4d and 5d orbitals give bigger splittings, so heavy complexes are low spin. Ligands trans to Cl⁻ are labilised more than those trans to NH₃: that trans effect decides cisplatin's geometry."))

# ── 19–20 · lanthanides and actinides ──
T2.append(num_t("cw-f-count", FB, rows(["sp", "Z", "ch", "sr", "n"], [
    ("Ce³⁺", 58, 3, "Ln", 1), ("Nd³⁺", 60, 3, "Ln", 3), ("Gd³⁺", 64, 3, "Ln", 7), ("Eu²⁺", 63, 2, "Ln", 7), ("Yb²⁺", 70, 2, "Ln", 14),
    ("Lu³⁺", 71, 3, "Ln", 14), ("Tb⁴⁺", 65, 4, "Ln", 7), ("U⁴⁺", 92, 4, "An", 2), ("Pu³⁺", 94, 3, "An", 5), ("Am³⁺", 95, 3, "An", 6),
    ("Np in NpO₂⁺ (Np(V))", 93, 5, "An", 2)]),
    "How many f electrons does {{sp}} have?", "f electrons",
    "Ln³⁺ ions are [Xe]4fⁿ with n = Z − 57; An ions are [Rn]5fⁿ. f⁰, f⁷ and f¹⁴ are extra stable, which is why Ce⁴⁺, Eu²⁺, Tb⁴⁺ and Yb²⁺ exist.",
    "cw_f_count(Z, ch, sr)"))

def _gj(S, L, J):
    return 1 + (J * (J + 1) + S * (S + 1) - L * (L + 1)) / (2 * J * (J + 1))

LN_TERMS = [("Ce³⁺", "²F₅/₂", 1, 0.5, 3, 2.5), ("Pr³⁺", "³H₄", 2, 1, 5, 4), ("Nd³⁺", "⁴I₉/₂", 3, 1.5, 6, 4.5), ("Sm³⁺", "⁶H₅/₂", 5, 2.5, 5, 2.5),
            ("Gd³⁺", "⁸S₇/₂", 7, 3.5, 0, 3.5), ("Tb³⁺", "⁷F₆", 8, 3, 3, 6), ("Dy³⁺", "⁶H₁₅/₂", 9, 2.5, 5, 7.5), ("Ho³⁺", "⁵I₈", 10, 2, 6, 8),
            ("Er³⁺", "⁴I₁₅/₂", 11, 1.5, 6, 7.5), ("Tm³⁺", "³H₆", 12, 1, 5, 6), ("Yb³⁺", "²F₇/₂", 13, 0.5, 3, 3.5)]
T2.append(num_t("cw-ln-moment", FB, rows(["sp", "term", "f", "n"], [(a, t, f, _gj(S, L, J) * (J * (J + 1)) ** 0.5) for a, t, f, S, L, J in LN_TERMS]),
    "{{sp}} (4f^{{f}}, ground term {{term}}) has its moment from the whole J, since the 4f shell is shielded. What is μ_eff = g_J√(J(J + 1)), in BM?", "μ_eff (BM)",
    "Lanthanide f electrons are buried under 5s and 5p, so ligands barely quench orbital momentum: use J, not the spin-only formula. g_J = 1 + [J(J+1) + S(S+1) − L(L+1)] / 2J(J+1). Dy³⁺ and Ho³⁺ reach about 10.6 BM.",
    "cw_ln_moment(f)", tol=0.0005))

T2.append(fact_t("cw-fblock-ox", FB, [
    ("ln:Ce", "cerium (besides +3)", "+4", "+2", "+5", "+1"), ("ln:Eu", "europium (besides +3)", "+2", "+4", "+5", "+1"),
    ("ln:Yb", "ytterbium (besides +3)", "+2", "+4", "+5", "+1"), ("ln:Tb", "terbium (besides +3)", "+4", "+2", "+5", "+1"),
    ("an:U", "uranium (its highest common state)", "+6", "+3", "+4", "+8"), ("an:Np", "neptunium (its highest state)", "+7", "+3", "+5", "+8"),
    ("an:Th", "thorium (its usual state)", "+4", "+3", "+2", "+6"), ("an:Am", "americium (its usual state in water)", "+3", "+6", "+4", "+2"),
], "Which oxidation state is characteristic of {{f}}?",
    "Lanthanides sit at +3, with +4 or +2 only where it reaches f⁰, f⁷ or f¹⁴. Early actinides behave like transition metals (5f is less shielded): U goes to +6 as uranyl, Np to +7, and only from Am on does +3 take over."))

T2.append(ox_t("cw-actinyl-ox", FB, [
    ("UO₂²⁺ (uranyl)", "UO2", 2, "U", 6), ("NpO₂⁺", "NpO2", 1, "Np", 5), ("PuO₂²⁺", "PuO2", 2, "Pu", 6), ("UF₆", "UF6", 0, "U", 6),
    ("U₃O₈", "U3O8", 0, "U", "16/3"), ("ThO₂", "ThO2", 0, "Th", 4),
], "Actinyl ions O=An=O are linear, with strong multiple bonds; equatorial ligands sit in a ring around them. U₃O₈ is mixed U(V)/U(VI)."))

# ── 21–22 · organometallic reaction steps and catalysis ──
T2.append(num_t("cw-electron-count", OM, rows(["sp", "M", "lg", "ch", "n"], [
    ("Cr(CO)₆", "Cr", "CO:6", 0, 18), ("Fe(CO)₅", "Fe", "CO:5", 0, 18), ("Ni(CO)₄", "Ni", "CO:4", 0, 18), ("ferrocene, FeCp₂", "Fe", "Cp:2", 0, 18),
    ("Cr(η⁶-C₆H₆)₂", "Cr", "C6H6:2", 0, 18), ("V(CO)₆", "V", "CO:6", 0, 17), ("[Mn(CO)₆]⁺", "Mn", "CO:6", 1, 18),
    ("RhCl(PPh₃)₃ (Wilkinson's)", "Rh", "Cl:1,PPh3:3", 0, 16), ("IrCl(CO)(PPh₃)₂ (Vaska's)", "Ir", "Cl:1,CO:1,PPh3:2", 0, 16),
    ("[PtCl₃(η²-C₂H₄)]⁻ (Zeise's anion)", "Pt", "Cl:3,C2H4:1", -1, 16), ("CpMn(CO)₃", "Mn", "Cp:1,CO:3", 0, 18)]),
    "What is the valence electron count of {{sp}}?", "Electrons",
    "Ionic method: dⁿ of the metal plus 2 per ligand pair (Cp⁻ 6, C₆H₆ 6, Cl⁻ 2). Neutral method: group number plus 1 per halide, 5 per Cp, 2 per CO. Both give 18 for stable carbonyls; square-planar d⁸ complexes (Rh(I), Ir(I), Pt(II)) are content with 16.",
    "cw_electron_count(M, lg, ch)"))

T2.append(num_t("cw-oxidative-addition", OM, rows(["sp", "M", "lg", "ch", "n"], [
    ("IrCl(CO)(PPh₃)₂ + H₂", "Ir", "Cl:1,CO:1,PPh3:2,H:2", 0, 18), ("IrCl(CO)(PPh₃)₂ + CH₃I", "Ir", "Cl:1,CO:1,PPh3:2,CH3:1,I:1", 0, 18),
    ("RhCl(PPh₃)₃ + H₂", "Rh", "Cl:1,PPh3:3,H:2", 0, 18), ("Pd(PPh₃)₂ + PhBr", "Pd", "PPh3:2,Ph:1,Br:1", 0, 16),
    ("[Rh(CO)₂I₂]⁻ + CH₃I (Monsanto)", "Rh", "CO:2,I:3,CH3:1", -1, 18)]),
    "What is the electron count of the product of the oxidative addition {{sp}}?", "Electrons",
    "Oxidative addition breaks X–Y and adds both to the metal: oxidation state +2, coordination number +2, electron count +2 (16 → 18). Reductive elimination is the reverse and forms the product C–C or C–H bond.",
    "cw_electron_count(M, lg, ch)"))

T2.append(fact_t("cw-reaction-step", OM, [
    ("step:addH2", "M + H₂ → M(H)₂, the metal's oxidation state rising by 2", "Oxidative addition", "Reductive elimination", "Migratory insertion (1,1)", "β-Hydride elimination"),
    ("step:loseHH", "M(H)(R) → M + R–H, the oxidation state falling by 2", "Reductive elimination", "Oxidative addition", "Migratory insertion (1,2)", "β-Hydride elimination"),
    ("step:COins", "M(CH₃)(CO) → M(COCH₃), forming an acyl", "Migratory insertion (1,1)", "Migratory insertion (1,2)", "Oxidative addition", "β-Hydride elimination"),
    ("step:olefinins", "M(H)(CH₂=CH₂) → M(CH₂CH₃)", "Migratory insertion (1,2)", "Migratory insertion (1,1)", "Reductive elimination", "β-Hydride elimination"),
    ("step:betaH", "M(CH₂CH₂R) → M(H)(CH₂=CHR)", "β-Hydride elimination", "Migratory insertion (1,2)", "Oxidative addition", "Reductive elimination"),
], "Name the elementary step: {{f}}.",
    "Catalytic cycles are built from a handful of steps: oxidative addition and reductive elimination change the oxidation state by 2; insertions and β-elimination change it by none, but open or fill a coordination site."))

T2.append(fact_t("cw-beta-hydride", OM, [
    ("betaH:need", "β-hydride elimination from a metal alkyl", "A vacant site cis to the alkyl and a β hydrogen", "An 18-electron metal", "A trans vacant site", "An α hydrogen only"),
], "What does {{f}} need?",
    "The β C–H swings in to the open cis site; without one, or without a β hydrogen (methyl, neopentyl, benzyl), the alkyl is far more stable. Chain growth in polymerisation stops this way."))

T2.append(fact_t("cw-catalytic-process", OM, [
    ("cat:monsanto", "the Monsanto acetic acid process", "Rh with iodide (methanol carbonylation to acetic acid)", "Pd(II) with Cu(II) (ethene to acetaldehyde)", "TiCl₄ with AlEt₃ (alkene polymerisation)", "Ru or Mo alkylidenes (Grubbs, Schrock)"),
    ("cat:wacker", "the Wacker process", "Pd(II) with Cu(II) (ethene to acetaldehyde)", "Rh with iodide (methanol carbonylation to acetic acid)", "Co or Rh carbonyls (alkene + CO + H₂ to aldehyde)", "RhCl(PPh₃)₃ (alkene hydrogenation)"),
    ("cat:ziegler", "Ziegler–Natta polymerisation", "TiCl₄ with AlEt₃ (alkene polymerisation)", "Pd(II) with Cu(II) (ethene to acetaldehyde)", "Ru or Mo alkylidenes (Grubbs, Schrock)", "Co or Rh carbonyls (alkene + CO + H₂ to aldehyde)"),
    ("cat:wilkinson", "homogeneous hydrogenation of alkenes", "RhCl(PPh₃)₃ (alkene hydrogenation)", "TiCl₄ with AlEt₃ (alkene polymerisation)", "Pd(II) with Cu(II) (ethene to acetaldehyde)", "Rh with iodide (methanol carbonylation to acetic acid)"),
    ("cat:hydroform", "hydroformylation (the oxo process)", "Co or Rh carbonyls (alkene + CO + H₂ to aldehyde)", "RhCl(PPh₃)₃ (alkene hydrogenation)", "Ru or Mo alkylidenes (Grubbs, Schrock)", "TiCl₄ with AlEt₃ (alkene polymerisation)"),
    ("cat:metathesis", "olefin metathesis", "Ru or Mo alkylidenes (Grubbs, Schrock)", "Co or Rh carbonyls (alkene + CO + H₂ to aldehyde)", "Pd(II) with Cu(II) (ethene to acetaldehyde)", "TiCl₄ with AlEt₃ (alkene polymerisation)"),
], "What catalyst runs {{f}}?",
    "Each industrial cycle strings together the elementary steps: Monsanto is oxidative addition of CH₃I, CO insertion and reductive elimination of acetyl iodide; Wacker is nucleophilic attack on Pd-bound ethene with Cu reoxidising Pd(0)."))

T2.append(num_t("cw-monsanto-count", OM, rows(["sp", "M", "lg", "ch", "n"], [
    ("[Rh(CO)₂I₂]⁻, the resting catalyst", "Rh", "CO:2,I:2", -1, 16), ("[CH₃Rh(CO)₂I₃]⁻, after oxidative addition", "Rh", "CO:2,I:3,CH3:1", -1, 18),
    ("[Rh(COCH₃)(CO)I₃]⁻, after CO insertion", "Rh", "CO:1,I:3,acyl:1", -1, 16), ("[Rh(COCH₃)(CO)₂I₃]⁻, after CO binds", "Rh", "CO:2,I:3,acyl:1", -1, 18)]),
    "In the Monsanto cycle, what is the electron count of {{sp}}?", "Electrons",
    "The cycle alternates 16 and 18 electrons (Tolman's rule): oxidative addition 16 → 18, migratory insertion 18 → 16, CO uptake 16 → 18, reductive elimination of CH₃COI 18 → 16.",
    "cw_electron_count(M, lg, ch)"))


# ═════ chapters 17–18 metal by metal ═════
# Facts entered once: the verifier's CW_FACTS copy of these keys was generated from this table, so it
# checks only that the shuffled answer lands on the right option, not the fact itself.
# (metal group label, skill unit, [(key, question, right, w1, w2, w3), ...])
ELEM = [
 ("ti", "Titanium", [
  ("ti:kroll", "How is titanium metal made industrially (the Kroll process)?", "Reduce TiCl₄ with Mg", "Reduce TiO₂ with carbon", "Electrolyse aqueous TiCl₃", "Roast TiS₂ in air"),
  ("ti:pigment", "Which titanium compound is the world's main white pigment?", "TiO₂", "TiCl₄", "Ti₂O₃", "TiN"),
  ("ti:aq3", "What colour is [Ti(H₂O)₆]³⁺, and why?", "Violet: one d–d transition of its single d electron", "Colourless: d⁰", "Yellow: charge transfer", "Green: two d–d bands"),
 ]),
 ("v", "Vanadium", [
  ("v:contact", "Which vanadium compound catalyses SO₂ → SO₃ in the contact process?", "V₂O₅", "VCl₄", "VO", "V(CO)₆"),
  ("v:VO2+", "What colour is the vanadyl ion VO²⁺ in water?", "Blue", "Yellow", "Violet", "Green"),
  ("v:V2+", "What colour is V²⁺ in water?", "Violet", "Blue", "Yellow", "Green"),
  ("v:VO2plus", "What colour is the dioxovanadium(V) ion VO₂⁺ in water?", "Yellow", "Blue", "Violet", "Green"),
 ]),
 ("cr", "Chromium", [
  ("cr:acetate", "What is unusual about chromium(II) acetate, Cr₂(O₂CCH₃)₄(H₂O)₂?", "A Cr–Cr quadruple bond makes it red and nearly diamagnetic", "It is a Cr(VI) peroxide", "It is tetrahedral and blue", "It is a liquid at room temperature"),
  ("cr:chromyl", "Heating a chloride with K₂Cr₂O₇ and conc. H₂SO₄ gives red-brown vapour. What is it?", "CrO₂Cl₂ (chromyl chloride)", "Cl₂", "CrCl₃", "HCl"),
  ("cr:aq3", "What is the colour and lability of [Cr(H₂O)₆]³⁺?", "Violet and substitution-inert (d³)", "Green and labile", "Orange and labile", "Colourless and inert"),
 ]),
 ("mn", "Manganese", [
  ("mn:pink", "Why is [Mn(H₂O)₆]²⁺ only very pale pink?", "High-spin d⁵: every d–d transition is spin-forbidden", "d⁰: no d electrons", "It absorbs only in the infrared", "It is a strong charge-transfer absorber"),
  ("mn:psii", "Which manganese cluster oxidises water in photosynthesis?", "The Mn₄CaO₅ cluster of photosystem II", "MnO₄⁻ in the chloroplast", "Mn(CO)₅ in photosystem I", "MnO₂ in the thylakoid membrane"),
  ("mn:battery", "Which manganese compound is the cathode of an ordinary alkaline battery?", "MnO₂", "KMnO₄", "MnCl₂", "Mn₂O₇"),
 ]),
 ("fe", "Iron", [
  ("fe:haber", "What is the catalyst of the Haber–Bosch ammonia synthesis?", "Iron (promoted with K₂O and Al₂O₃)", "Platinum gauze", "V₂O₅", "Nickel"),
  ("fe:prussian", "What is Prussian blue?", "Fe(III) hexacyanoferrate(II), Fe₄[Fe(CN)₆]₃", "Fe(CN)₂", "FeSCN²⁺", "Fe₃O₄"),
  ("fe:heme", "In which oxidation state does heme iron bind O₂ in haemoglobin?", "Fe(II)", "Fe(III)", "Fe(IV)", "Fe(0)"),
  ("fe:aq3", "Why are solutions of Fe³⁺ salts acidic?", "Small, highly charged Fe³⁺ polarises bound water: [Fe(H₂O)₆]³⁺ is a weak acid", "Fe³⁺ releases H₂", "The anion is always an acid", "Fe³⁺ oxidises water to H⁺ and O₂"),
 ]),
 ("co", "Cobalt", [
  ("co:b12", "Which vitamin contains cobalt?", "B₁₂ (cobalamin)", "B₁ (thiamine)", "C (ascorbic acid)", "D (calciferol)"),
  ("co:humidity", "Why does blue cobalt chloride paper turn pink in damp air?", "Tetrahedral [CoCl₄]²⁻ (blue) becomes octahedral [Co(H₂O)₆]²⁺ (pink)", "Co(II) is oxidised to Co(III)", "The paper bleaches", "Co(III) is reduced to Co(II)"),
  ("co:battery", "Which cobalt compound is the classic lithium-ion battery cathode?", "LiCoO₂", "CoCl₂", "Co(CO)₄", "CoSO₄"),
 ]),
 ("ni", "Nickel", [
  ("ni:mond", "How does the Mond process purify nickel?", "Ni + 4 CO forms volatile Ni(CO)₄, which decomposes on heating", "Electrolysis of NiSO₄", "Reduction of NiO with H₂", "Zone refining"),
  ("ni:dmg", "What does dimethylglyoxime give with Ni²⁺ in ammonia?", "A red precipitate of square-planar Ni(dmgH)₂", "A blue solution", "A green precipitate of Ni(OH)₂", "No reaction"),
  ("ni:raney", "What is Raney nickel used for?", "Catalytic hydrogenation", "Electroplating", "Pigment", "Coinage"),
 ]),
 ("cu", "Copper", [
  ("cu:disprop", "What happens to Cu⁺ in water?", "It disproportionates to Cu and Cu²⁺", "It is stable indefinitely", "It is oxidised by water to Cu²⁺ and H₂", "It forms Cu₂²⁺ dimers"),
  ("cu:ammine", "What forms when excess ammonia is added to aqueous Cu²⁺?", "Deep-blue [Cu(NH₃)₄(H₂O)₂]²⁺", "A pale green precipitate that stays", "Colourless [Cu(NH₃)₂]⁺", "Black CuO"),
  ("cu:fehling", "What red solid forms in a positive Fehling's test?", "Cu₂O", "CuO", "Cu(OH)₂", "CuS"),
  ("cu:hemocyanin", "Which O₂ carrier in molluscs and arthropods uses copper?", "Haemocyanin", "Haemoglobin", "Myoglobin", "Hemerythrin"),
 ]),
 ("zrhf", "Zirconium and hafnium", [
  ("zr:clad", "Why is zirconium alloy used for nuclear fuel cladding?", "It absorbs very few neutrons and resists corrosion", "It absorbs neutrons strongly", "It is radioactive", "It is cheap and soft"),
  ("hf:rods", "Why is hafnium used in reactor control rods?", "It absorbs neutrons strongly", "It reflects neutrons", "It moderates neutrons", "It is a fuel"),
  ("zr:zirconia", "What stabilises cubic zirconia at room temperature?", "Adding Y₂O₃ or CaO", "Adding carbon", "Quenching in water", "Adding HfO₂"),
 ]),
 ("nbta", "Niobium and tantalum", [
  ("ta:capacitor", "Why is tantalum used in small capacitors?", "Its anodised Ta₂O₅ film is a thin, stable dielectric", "It is a superconductor at room temperature", "It is magnetic", "It is a liquid metal"),
  ("nb:magnet", "Which niobium alloy winds most MRI superconducting magnets?", "Nb–Ti", "Nb–Fe", "Nb₂O₅", "Nb–Cu"),
  ("nbta:twins", "Why are Nb and Ta so hard to separate?", "The lanthanide contraction makes them almost the same size", "They form the same alloy", "Ta is radioactive", "They are not found together"),
 ]),
 ("mow", "Molybdenum and tungsten", [
  ("mo:nitrogenase", "Which metal besides iron is in the usual cofactor of nitrogenase?", "Molybdenum", "Tungsten", "Copper", "Cobalt"),
  ("mo:mos2", "Why is MoS₂ a dry lubricant?", "Layers held by van der Waals forces slide over each other", "It melts at low temperature", "It is a liquid crystal", "It absorbs oil"),
  ("w:melting", "Which metal has the highest melting point?", "Tungsten", "Molybdenum", "Rhenium", "Osmium"),
  ("w:keggin", "What is [PW₁₂O₄₀]³⁻?", "A Keggin polyoxometalate", "A tungsten carbonyl", "A tungsten cluster hydride", "A tungsten bronze"),
 ]),
 ("tcre", "Technetium and rhenium", [
  ("tc:99m", "Why is ⁹⁹ᵐTc the workhorse of nuclear-medicine imaging?", "A 6-hour half-life and a clean 140 keV gamma ray", "It emits alpha particles", "It is stable", "It decays in seconds"),
  ("re:perrhenate", "How does ReO₄⁻ compare with MnO₄⁻ as an oxidant?", "Much weaker: high oxidation states are more stable down a group", "Much stronger", "About the same", "ReO₄⁻ does not exist"),
  ("re:reforming", "Where is rhenium used industrially?", "With Pt in petroleum-reforming catalysts", "In steel pigments", "As a neutron absorber", "In fertiliser"),
 ]),
 ("ruos", "Ruthenium and osmium", [
  ("os:oso4", "What does OsO₄ do to an alkene?", "Adds two OH groups on the same face (cis-dihydroxylation)", "Cleaves it to carboxylic acids", "Hydrogenates it", "Polymerises it"),
  ("ru:photoredox", "What makes [Ru(bpy)₃]²⁺ useful in photoredox chemistry?", "A long-lived MLCT excited state that both oxidises and reduces", "It is colourless", "It is paramagnetic", "It is a strong acid"),
  ("os:max", "What is the highest oxidation state of osmium, seen in OsO₄?", "+8", "+6", "+4", "+10"),
 ]),
 ("rhir", "Rhodium and iridium", [
  ("rh:converter", "What does rhodium do in a car's three-way catalytic converter?", "Reduces NOₓ to N₂", "Oxidises CO only", "Removes sulfur", "Stores oxygen"),
  ("ir:cativa", "Which process makes acetic acid with an iridium catalyst?", "The Cativa process", "The Wacker process", "The Mond process", "The Kroll process"),
  ("rhir:vaska", "What is Vaska's complex known for?", "Reversible oxidative addition of O₂, H₂ and CH₃I to Ir(I)", "Being an 18-electron Ir(III) hydride", "Catalysing olefin metathesis", "Being tetrahedral"),
 ]),
 ("pdpt", "Palladium and platinum", [
  ("pd:h2", "What is unusual about palladium and hydrogen?", "Pd absorbs hundreds of times its volume of H₂ and lets it diffuse through", "Pd does not react with hydrogen at all", "Pd forms ionic PdH₂", "Pd burns in hydrogen"),
  ("pd:coupling", "Which reactions are catalysed by Pd(0)/Pd(II) cycles and won the 2010 Nobel Prize?", "Cross-couplings (Heck, Suzuki, Negishi)", "Olefin metathesis", "Ziegler–Natta polymerisation", "Hydroformylation"),
  ("pt:ostwald", "Which process oxidises ammonia over Pt–Rh gauze?", "The Ostwald process (nitric acid)", "The Haber process", "The contact process", "The Solvay process"),
  ("pt:cisplatin", "Why is cisplatin an anticancer drug?", "It binds adjacent guanines in DNA and kinks it", "It oxidises tumour cells", "It blocks iron uptake", "It releases chlorine"),
 ]),
 ("agau", "Silver and gold", [
  ("au:cyanide", "How is gold extracted from low-grade ore?", "Leached as [Au(CN)₂]⁻ with cyanide and air", "Dissolved in nitric acid", "Smelted with carbon", "Electrolysed from AuCl"),
  ("au:aquaregia", "What does aqua regia turn gold into?", "[AuCl₄]⁻", "Au(NO₃)₃", "AuCl", "Au₂O₃"),
  ("ag:photo", "What role did silver bromide play in film photography?", "Light reduces AgBr grains, seeding a developable silver image", "It is the dye", "It fixes the image", "It is the plastic base"),
  ("au:linear", "What geometry does gold(I) usually take?", "Linear, two-coordinate", "Tetrahedral", "Octahedral", "Square planar"),
 ]),
]

T3 = []
for g, name, rows3 in ELEM:
    T3.append(fact_t(f"cw-{g}-chemistry", TM, rows3, "{{f}}",
        f"{name}: the chemistry Cotton & Wilkinson single out — industrial use, characteristic compounds and colours, and where the metal turns up in biology."))

T3.append(ox_t("cw-heavy-metal-ox", TM, [
    ("RuO₄", "RuO4", 0, "Ru", 8), ("OsO₄", "OsO4", 0, "Os", 8), ("ReO₄⁻", "ReO4", -1, "Re", 7), ("TcO₄⁻", "TcO4", -1, "Tc", 7),
    ("MoO₃", "MoO3", 0, "Mo", 6), ("WO₄²⁻", "WO4", -2, "W", 6), ("Nb₂O₅", "Nb2O5", 0, "Nb", 5), ("IrF₆", "IrF6", 0, "Ir", 6),
    ("PtF₆", "PtF6", 0, "Pt", 6), ("[AuCl₄]⁻", "AuCl4", -1, "Au", 3), ("AgF₂", "AgF2", 0, "Ag", 2), ("[PdCl₄]²⁻", "PdCl4", -2, "Pd", 2),
], "Down a group, high oxidation states become more stable: Fe never reaches +8 but Ru and Os do; MnO₄⁻ is a fierce oxidant and ReO₄⁻ a mild one. PtF₆ is strong enough to oxidise O₂ and Xe."))

T3.append(ox_t("cw-first-row-ox-2", TM, [
    ("K₂FeO₄", "K2FeO4", 0, "Fe", 6), ("CoF₃", "CoF3", 0, "Co", 3), ("K₃[CuF₆]", "K3CuF6", 0, "Cu", 3), ("Mn₂O₇", "Mn2O7", 0, "Mn", 7),
    ("CrO₃", "CrO3", 0, "Cr", 6), ("V₂O₅", "V2O5", 0, "V", 5), ("TiCl₄", "TiCl4", 0, "Ti", 4), ("NiF₆²⁻", "NiF6", -2, "Ni", 4),
], "The highest states of the first series fall after Mn: +4 for Ti, +5 V, +6 Cr, +7 Mn, +6 Fe (ferrate), +3 to +4 for Co, Ni and Cu, and only with F or O."))

if __name__ == "__main__":
    head = ("# Cotton & Wilkinson, Advanced Inorganic Chemistry 6e, chapters 1–15 (framework inorganic-advanced).\n"
            "# Generated by scripts/cw_cases.py: edit the script, not this file. Checked by tests/verify/cwcalc.py\n"
            "# (VSEPR, MO ladders, Wade, Euler, Latimer, CW_FACTS) and incalc's ox_state.\n\n")
    (ROOT / "cw-main-group.yaml").write_text(head + "\n".join(T))
    head2 = head.replace("chapters 1–15", "chapters 16–22")
    (ROOT / "cw-transition.yaml").write_text(head2 + "\n".join(T2))
    (ROOT / "cw-elements.yaml").write_text(head2.replace("chapters 16–22", "chapters 17–18, metal by metal") + "\n".join(T3))
    print(f"wrote {len(T)} + {len(T2)} + {len(T3)} templates")
