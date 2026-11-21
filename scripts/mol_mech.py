#!/usr/bin/env python3
"""Mechanisms as a series of drawn states: writes drills/problems/st-mechanisms.yaml.

  python3 scripts/mol_mech.py        (plain Python, no RDKit)

A mechanism is a list of states. Each state is one `type: molecule` figure holding every species
present (enzyme groups, substrate, water), laid out by hand so that atoms stay put from state to
state and only bonds and hydrogens move. Curved arrows on a state show the electron pairs that
move to give the next one. Every state states the same formula and charge, and
tests/verify/molecules.py rebuilds it from the drawn atoms, so a lost atom or charge is caught.

Chymotrypsin follows the textbook serine-protease mechanism as given in Bruice, Organic Chemistry
8e, ch. 22 (catalysis in enzymatic reactions): catalytic triad Asp102-His57-Ser195, two tetrahedral
intermediates held by the oxyanion hole, an acyl-enzyme between them. Residue side chains are cut
down to the reacting group with R for the rest.
"""
import math
from pathlib import Path


class State:
    def __init__(self):
        self.atoms, self.bonds, self.arrows, self.notes, self.ix = [], [], [], [], {}

    def atom(self, key, x, y, label=None):
        self.ix[key] = len(self.atoms)
        self.atoms.append([round(x, 2), round(y, 2)] + ([label] if label else []))

    def bond(self, a, b, order=1):
        self.bonds.append([self.ix[a], self.ix[b]] + ([order] if order != 1 else []))

    def arrow(self, a, b, bend=0.35):
        end = lambda e: [self.ix[e[0]], self.ix[e[1]]] if isinstance(e, tuple) else self.ix[e]  # noqa: E731
        self.arrows.append([end(a), end(b), bend])

    def note(self, x, y, text):
        self.notes.append([x, y, text])

    def yaml(self, indent, formula, arrows=True, caption=None):
        f = lambda a: "[" + ", ".join(f'"{v}"' if isinstance(v, str) else f(v) if isinstance(v, list) else str(v) for v in a) + "]"  # noqa: E731
        out = f"{indent}type: molecule\n{indent}formula: {formula}\n"
        if caption:
            out += f"{indent}caption: '{caption}'\n"
        out += f"{indent}atoms: {f(self.atoms)}\n{indent}bonds: {f(self.bonds)}\n"
        if arrows and self.arrows:
            out += f"{indent}arrows: {f(self.arrows)}\n"
        if self.notes:
            out += f"{indent}notes: {f(self.notes)}\n"
        return out


# ── chymotrypsin ────────────────────────────────────────────────────────────
HIS = (4.0, 2.6)  # centre of the imidazole ring


def triad(s, his_h, ser_h):
    """Asp102 carboxylate, His57 imidazole, Ser195 CH2-O. his_h: N-epsilon carries H (His is protonated)."""
    s.atom("aspR", 0.0, 3.0, "R")
    s.atom("aspC", 1.0, 3.0)
    s.atom("aspO2", 1.5, 3.87, "O")
    s.atom("aspO", 1.87, 2.5, "O-")
    s.bond("aspR", "aspC"); s.bond("aspC", "aspO2", 2); s.bond("aspC", "aspO")
    pt = lambda deg, r=0.85: (HIS[0] + r * math.cos(math.radians(deg)), HIS[1] + r * math.sin(math.radians(deg)))  # noqa: E731
    s.atom("Nd", *pt(198), "N")
    s.atom("Ce", *pt(270))
    s.atom("Ne", *pt(342), "N+" if his_h else "N")
    s.atom("Cd", *pt(54))
    s.atom("Cg", *pt(126))
    s.atom("hisR", pt(126)[0] - 0.3, pt(126)[1] + 0.95, "R")
    s.atom("HNd", pt(198)[0] - 0.75, pt(198)[1] + 0.05, "H")
    s.bond("Nd", "Ce"); s.bond("Ce", "Ne", 2); s.bond("Ne", "Cd"); s.bond("Cd", "Cg", 2); s.bond("Cg", "Nd")
    s.bond("Cg", "hisR"); s.bond("Nd", "HNd"); s.bond("HNd", "aspO", 0)
    s.atom("serO", 6.4, 3.0, "O")
    s.atom("serC", 7.15, 3.7)
    s.atom("serR", 7.15, 4.7, "R")
    s.bond("serO", "serC"); s.bond("serC", "serR")
    s.atom("H", 5.6, 2.72, "H")  # the proton that shuttles between Ser, His and the leaving groups
    if ser_h:
        s.bond("serO", "H")
    if his_h:
        s.bond("Ne", "H")
    s.note(0.9, 4.6, "Asp102")
    s.note(3.6, 4.6, "His57")
    s.note(8.2, 4.0, "Ser195")


def acyl(s, tetra):
    """the substrate's acyl carbon with its R and its carbonyl oxygen (an oxyanion in a tetrahedral state)"""
    s.atom("C", 6.6, 1.5)
    s.atom("O", 6.6, 0.5, "O-" if tetra else "O")
    s.atom("R", 7.47, 2.0, "R")
    s.bond("C", "R"); s.bond("C", "O", 1 if tetra else 2)
    if tetra:
        s.note(7.9, 0.45, "oxyanion hole")


def states():
    out = []
    # 1. Michaelis complex: peptide in the site, water waiting
    s = State(); triad(s, False, True); acyl(s, False)
    s.atom("N", 5.6, 1.2, "HN"); s.atom("R2", 4.75, 0.65, "R"); s.bond("C", "N"); s.bond("N", "R2")
    s.atom("W", 9.0, 1.7, "H2O")
    s.arrow("Ne", "H", -0.3); s.arrow(("serO", "H"), ("serO", "C"), -0.45); s.arrow(("C", "O"), "O", 0.5)
    out.append(("Enzyme and substrate", "His57, held by Asp102, pulls the proton off Ser195 as the serine oxygen attacks the peptide carbonyl. The carbonyl pi electrons move onto oxygen", s))
    # 2. first tetrahedral intermediate
    s = State(); triad(s, True, False); acyl(s, True)
    s.bond("serO", "C")
    s.atom("N", 5.6, 1.2, "HN"); s.atom("R2", 4.75, 0.65, "R"); s.bond("C", "N"); s.bond("N", "R2")
    s.atom("W", 9.0, 1.7, "H2O")
    s.arrow("O", ("C", "O"), 0.5); s.arrow(("C", "N"), "H", 0.4); s.arrow(("Ne", "H"), "Ne", 0.5)
    out.append(("First tetrahedral intermediate", "The oxyanion re-forms the C=O and the C-N bond breaks, the nitrogen taking the proton from His57-H+: the amine leaves and the acyl group stays on serine", s))
    # 3. acyl-enzyme, amine gone, water in its place
    s = State(); triad(s, False, False); acyl(s, False)
    s.bond("serO", "C")
    s.atom("N", 4.2, 0.1, "H2N"); s.atom("R2", 3.3, -0.3, "R"); s.bond("N", "R2")
    s.atom("W", 5.6, 1.2, "O"); s.atom("Hb", 5.3, 0.45, "H"); s.bond("W", "H"); s.bond("W", "Hb")
    s.arrow("Ne", "H", 0.3); s.arrow(("W", "H"), ("W", "C"), 0.45); s.arrow(("C", "O"), "O", 0.5)
    out.append(("Acyl-enzyme", "The same move again with water where the amine was: His57 takes a proton from water as its oxygen attacks the ester carbonyl", s))
    # 4. second tetrahedral intermediate
    s = State(); triad(s, True, False); acyl(s, True)
    s.bond("serO", "C")
    s.atom("N", 4.2, 0.1, "H2N"); s.atom("R2", 3.3, -0.3, "R"); s.bond("N", "R2")
    s.atom("W", 5.6, 1.2, "O"); s.atom("Hb", 5.3, 0.45, "H"); s.bond("W", "Hb"); s.bond("W", "C")
    s.arrow("O", ("C", "O"), 0.5); s.arrow(("C", "serO"), "H", -0.4); s.arrow(("Ne", "H"), "Ne", -0.5)
    out.append(("Second tetrahedral intermediate", "The oxyanion re-forms the C=O and the bond to serine breaks, the serine oxygen taking its proton back from His57-H+", s))
    # 5. free enzyme and both products
    s = State(); triad(s, False, True); acyl(s, False)
    s.atom("N", 4.2, 0.1, "H2N"); s.atom("R2", 3.3, -0.3, "R"); s.bond("N", "R2")
    s.atom("W", 5.6, 1.2, "O"); s.atom("Hb", 5.3, 0.45, "H"); s.bond("W", "Hb"); s.bond("W", "C")
    out.append(("Enzyme restored, acid and amine released", "", s))
    return out


FORMULA = "C6H9N3O5R5-"  # every state: the same atoms and one negative charge (Asp102)

HEAD = """# Mechanisms as drawn states with curved arrows.
# GENERATED by scripts/mol_mech.py: edit there, not here.
#
# Basis: the serine-protease mechanism as taught in Bruice, Organic Chemistry 8e, ch. 22 (standards.yaml:
# bruice-8e). Side chains are cut down to the reacting group, with R for the rest. Self-graded: draw the
# arrows and the next state, reveal, compare. Every state carries the same formula and charge, which
# tests/verify/molecules.py rebuilds from the drawn atoms.
"""


# ── the four mechanisms every other one is built from ───────────────────────
def small_mechanisms():
    """(slug, name, skill, formula, [(state title, why this step happens, State)])"""
    out = []

    # SN2: hydroxide on bromoethane
    def sn2(done):
        s = State()
        s.atom("O", 0.0, 0.0, "HO" if done else "HO-")
        s.atom("C1", 2.0, 0.0); s.atom("C2", 2.0, 1.0)
        s.atom("Br", 3.4, 0.0, "Br-" if done else "Br")
        s.bond("C1", "C2")
        s.bond("O", "C1") if done else s.bond("C1", "Br")
        return s
    a = sn2(False); a.arrow("O", "C1", -0.3); a.arrow(("C1", "Br"), "Br", -0.5)
    out.append(("sn2", "the SN2 reaction of hydroxide with bromoethane", "orgo.substitution-elimination", "C2H6BrO-", [
        ("Hydroxide and bromoethane", "One step. The nucleophile attacks the carbon from the side opposite the leaving group while the C–Br bond breaks: two arrows, no intermediate, and the configuration at carbon inverts", a),
        ("Ethanol and bromide", "", sn2(True))]))

    # E2: an alkoxide on bromoethane
    def e2(done):
        s = State()
        s.atom("R", -0.2, 1.6, "R"); s.atom("O", 0.8, 1.6, "O" if done else "O-")
        s.atom("H", 1.6, 0.8, "H"); s.atom("Cb", 2.3, 0.0); s.atom("Ca", 3.3, 0.0)
        s.atom("Br", 3.9, -0.9, "Br-" if done else "Br")
        s.bond("R", "O")
        if done:
            s.bond("O", "H"); s.bond("Cb", "Ca", 2)
        else:
            s.bond("H", "Cb"); s.bond("Cb", "Ca"); s.bond("Ca", "Br")
        return s
    a = e2(False); a.arrow("O", "H", -0.3); a.arrow(("H", "Cb"), ("Cb", "Ca"), -0.4); a.arrow(("Ca", "Br"), "Br", -0.5)
    out.append(("e2", "the E2 elimination of bromoethane by an alkoxide", "orgo.substitution-elimination", "C2H5BrOR-", [
        ("An alkoxide and bromoethane", "One step, three arrows in a row: the base takes the β-hydrogen, the C–H electrons become the π bond, and the leaving group departs. The H and the leaving group must be anti to each other", a),
        ("An alcohol, ethene and bromide", "", e2(True))]))

    # electrophilic addition: HBr to 2-methylpropene
    def add(stage):
        s = State()
        s.atom("C1", 0.0, 0.0); s.atom("C2", 1.0, 0.0, "C+" if stage == 1 else None)
        s.atom("C3", 1.5, -0.87); s.atom("C4", 2.0, 0.0)
        s.atom("H", -0.3, 1.2, "H"); s.atom("Br", 0.9, 1.9, "Br-" if stage == 1 else "Br")
        s.bond("C2", "C3"); s.bond("C2", "C4")
        if stage == 0:
            s.bond("C1", "C2", 2); s.bond("H", "Br")
        else:
            s.bond("C1", "C2"); s.bond("C1", "H")
        if stage == 2:
            s.bond("C2", "Br")
        return s
    a = add(0); a.arrow(("C1", "C2"), "H", 0.4); a.arrow(("H", "Br"), "Br", 0.5)
    b = add(1); b.arrow("Br", "C2", 0.3)
    out.append(("hbr-addition", "the addition of HBr to 2-methylpropene", "orgo.alkene-reactions", "C4H9Br", [
        ("2-Methylpropene and HBr", "The π bond is the nucleophile. It takes the proton onto the carbon with more hydrogens, because that leaves the positive charge on the more substituted carbon: a tertiary carbocation", a),
        ("Carbocation and bromide", "The halide attacks the carbocation. The first step decided the product; this one is fast", b),
        ("2-Bromo-2-methylpropane", "", add(2))]))

    # nucleophilic acyl substitution: hydroxide on an ester
    def acyl_sub(stage):
        s = State()
        s.atom("Rc", 1.13, -0.5, "R"); s.atom("C", 2.0, 0.0)
        s.atom("O1", 2.0, 1.0, "O-" if stage == 1 else "O")
        s.atom("O2", 2.87, -0.5, "O-" if stage == 2 else "O"); s.atom("R2", 3.74, 0.0, "R")
        s.atom("O3", 0.5, 0.9, "HO-" if stage == 0 else "HO")
        s.bond("Rc", "C"); s.bond("C", "O1", 1 if stage == 1 else 2); s.bond("O2", "R2")
        if stage < 2:
            s.bond("C", "O2")
        if stage > 0:
            s.bond("O3", "C")
        return s
    a = acyl_sub(0); a.arrow("O3", "C", -0.3); a.arrow(("C", "O1"), "O1", 0.5)
    b = acyl_sub(1); b.arrow("O1", ("C", "O1"), 0.5); b.arrow(("C", "O2"), "O2", -0.5)
    out.append(("acyl-substitution", "the attack of hydroxide on an ester (nucleophilic acyl substitution)", "orgo.acyl-reactions", "CHO3R2-", [
        ("An ester and hydroxide", "Addition: the nucleophile attacks the carbonyl carbon and the π electrons move up onto oxygen. The carbon becomes tetrahedral", a),
        ("The tetrahedral intermediate", "Elimination: the oxyanion pushes back down, re-forming C=O, and the best leaving group is expelled. Every acyl substitution is these two steps", b),
        ("A carboxylic acid and an alkoxide", "", acyl_sub(2))]))
    return out


def small_items():
    out = ["\n# ── core organic mechanisms: SN2, E2, electrophilic addition, acyl substitution ──\n"]
    for slug, name, skill, formula, steps in small_mechanisms():
        for k in range(len(steps) - 1):
            title, why, s = steps[k]
            nxt_title, _, nxt = steps[k + 1]
            n_of = f", step {k + 1} of {len(steps) - 1}" if len(steps) > 2 else ""
            out.append(f"""
- template: st-mech-{slug}-{k + 1}
  skill: {skill}
  pace: quick
  prompt: 'Mechanism: {name}{n_of}. Starting from {title[0].lower() + title[1:]}, draw the curved arrows and what they lead to.'
  figure:
{s.yaml("    ", formula, arrows=False)}  parts:
    - ask: 'Draw the arrows and the next state, then compare'
      label: a
      draw: true
      solution:
        type: scheme
        panels:
{item(s.yaml("            ", formula))}{item(nxt.yaml("            ", formula, arrows=False, caption=nxt_title))}      explain: '{why}'
""")
    return "".join(out)


def item(block):
    """a figure block as one entry of a YAML list"""
    return "          - " + block[12:]


def main():
    st = states()
    out = [HEAD]
    for k in range(4):
        title, why, s = st[k]
        nxt_title, _, nxt = st[k + 1]
        out.append(f"""
- template: st-mech-chymotrypsin-{k + 1}
  skill: biochem.mechanisms
  pace: quick
  prompt: 'Chymotrypsin, step {k + 1} of 4, starting from: {title.lower()}. Draw the curved arrows and the state they lead to.'
  figure:
{s.yaml("    ", FORMULA, arrows=False)}  parts:
    - ask: 'Draw the arrows and the next state, then compare'
      label: a
      draw: true
      solution:
        type: scheme
        panels:
{item(s.yaml("            ", FORMULA))}{item(nxt.yaml("            ", FORMULA, arrows=False, caption=nxt_title))}      explain: '{why}'
""")
    panels = "".join(item(s.yaml("            ", FORMULA, caption=f"{i + 1}. {t}")) for i, (t, _, s) in enumerate(st))
    out.append(f"""
- template: st-mech-chymotrypsin-whole
  skill: biochem.mechanisms
  pace: workout
  prompt: 'Draw the whole chymotrypsin mechanism for hydrolysis of a peptide bond: the catalytic triad, both tetrahedral intermediates, the acyl-enzyme, and every curved arrow.'
  parts:
    - ask: 'Draw all five states on paper, then compare'
      label: a
      draw: true
      solution:
        type: scheme
        panels:
{panels}      explain: 'Two halves with the same three arrows each. Acylation: serine attacks (His57 as base), the tetrahedral intermediate collapses and the amine leaves (His57-H+ as acid). Deacylation: water attacks (His57 as base), the second intermediate collapses and serine leaves (His57-H+ as acid). Asp102 holds His57 in place and steadies its positive charge; the oxyanion hole steadies both intermediates'

- template: st-mech-chymotrypsin-roles
  skill: biochem.mechanisms
  pace: recall
  cases:
    - {{ q: 'Which residue is the nucleophile that attacks the peptide carbonyl?', ans: 2 }}
    - {{ q: 'Which residue acts as the general base and then the general acid?', ans: 1 }}
    - {{ q: 'Which residue orients the imidazole ring and steadies its positive charge?', ans: 0 }}
    - {{ q: 'What stabilises the negative charge on the tetrahedral intermediates?', ans: 3 }}
  prompt: 'Chymotrypsin. {{{{q}}}}'
  parts:
    - ask: 'Answer'
      label: a
      choice: ["Asp102", "His57", "Ser195", "The oxyanion hole (backbone N-H groups)"]
      correct: ans
      explain: 'The triad: Asp102 holds His57, His57 shuttles the proton, Ser195 attacks. The oxyanion hole, two backbone N-H groups, hydrogen-bonds the oxyanion'
  verify: {{ authored: true }}
""")
    out.append(small_items())
    path = Path(__file__).resolve().parents[1] / "drills/problems/st-mechanisms.yaml"
    path.write_text("".join(out), encoding="utf8")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
