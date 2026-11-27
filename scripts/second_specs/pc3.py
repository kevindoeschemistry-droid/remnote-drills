"""Second question types for the six Physical Chemistry objectives that listed one drill (Nov 2026)."""
FILE, FRAMEWORK = "pc-second-types-2", "physical-chemistry"
from opl_dsl import Q

M = "Symbol('m')"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
ADD = []


def N(code, name, skill, prompt, value, verify, explain, tex="answer", **kw):
    ADD.append((code, Q(name, skill, prompt, value=value, tex=tex, verify=verify, explain=explain, **kw)))


def L(code, name, skill, prompt, options, rows, explain):
    ADD.append((code, Q(name, skill, prompt, pace="recall", cases=[{"q": a, "kc": k} for a, k in rows], choice=options, correct="kc", verify="authored", explain=explain)))


def F(code, name, skill, rows, explain):
    ADD.append((code, Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows], choice=MC, correct="0", verify="authored", explain=explain)))


def C(keys, rows):
    return [dict(zip(keys.split(), r)) for r in rows]


B, SY, SP = "quantum.bonding", "quantum.symmetry", "quantum.spectroscopy"
N("PC-15.2.A", "pc-hybrid-p-character", B, "A central atom has {{kb}} bonded atoms and {{kl}} lone pair(s), all in equivalent hybrids. What percent p character do the hybrids have?", "(kb + kl - 1)/(kb + kl)*100",
  "100 - 100*Rational(1, kb + kl)", "n domains mix one s orbital with n − 1 p orbitals, so each hybrid is 1/n s: 50% p for sp, 66.7% for sp², 75% for sp³", tex="\\%p",
  cases=C("kb kl", [(2, 0), (3, 0), (2, 1), (4, 0), (3, 1), (2, 2)]))
L("PC-15.2.B", "pc-walsh-ah2-shape", B, "By Walsh's rules, the AH₂ species {{q}} is:", ["Linear", "Bent"], [
  ("BeH₂ (4 valence electrons)", 0), ("BH₂ (5)", 1), ("CH₂ (6)", 1), ("NH₂ (7)", 1), ("H₂O (8)", 1), ("BH₂⁺ (4)", 0)],
  "With four valence electrons only the two bonding orbitals are filled and they favour 180°. From the fifth electron on, the orbital that drops sharply on bending is occupied")
N("PC-15.3.A", "pc-singlet-triplet-gap", B, "Two electrons occupy different orbitals with Coulomb integral J = {{kj}} eV and exchange integral K = {{kk}} eV. How far does the open-shell singlet lie above the triplet, in eV?",
  "2*kk", "(nsimplify(kj) + nsimplify(kk)) - (nsimplify(kj) - nsimplify(kk))", "E = h₁ + h₂ + J ± K: plus for the singlet, minus for the triplet, so the gap is 2K and the triplet is lower (Hund)", tex="\\Delta E",
  cases=C("kj kk", [(10.5, 1.2), (8.0, 0.4), (12.0, 2.5), (9.3, 0.8)]))
L("PC-17.1.E", "pc-ir-raman-activity", SY, "The {{q}} is:", ["IR active only", "Raman active only", "Both IR and Raman active"], [
  ("symmetric stretch of CO₂", 1), ("antisymmetric stretch of CO₂", 0), ("bend of CO₂", 0), ("symmetric stretch of H₂O", 2), ("stretch of N₂", 1), ("stretch of HCl", 2)],
  "IR needs a changing dipole, Raman a changing polarisability. In a molecule with a centre of symmetry no mode is both (mutual exclusion)")
N("PC-18.1.C", "pc-chemical-shift-ppm", SP, "On a {{km}} MHz spectrometer a proton resonates {{kh}} Hz downfield of TMS. What is its chemical shift in ppm?", "kh/km", "Rational(kh, km*10**6)*10**6",
  "δ = (ν − ν_ref)/ν₀ × 10⁶, which is why the ppm scale does not depend on the magnet", tex="\\delta", cases=C("km kh", [(300, 2160), (400, 2880), (500, 1250), (60, 432), (600, 4380)]))
L("PC-18.1.E", "pc-karplus-size", SP, "By the Karplus relation, the three-bond H–H coupling for {{q}} is:", ["Large (about 8–13 Hz)", "Small (about 0–5 Hz)"], [
  ("an anti arrangement (dihedral 180°)", 0), ("a gauche arrangement (60°)", 1), ("two axial hydrogens on adjacent carbons of a chair", 0), ("an axial and an equatorial hydrogen on adjacent carbons", 1),
  ("two equatorial hydrogens on adjacent carbons", 1), ("a dihedral angle of 90°", 1)],
  "J is largest near 0° and 180° and passes through a minimum near 90°. Axial–axial is 180°; the other chair pairs are about 60°")
assert len(ADD) == 6
