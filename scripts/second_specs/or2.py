"""Second question types for Organic Reactions (OR) objectives that had one: stereocentres in reverse, oxidation level
by functional group, directing-group strength, and what the SN2 and E2 mechanisms require. OR-1.1.A, 1.2.B and 1.2.C
reuse co-h-from-dou, dat-pi-electron-count and dat-rate-doubling (written into the framework line)."""
from opl_dsl import Q

FILE, FRAMEWORK = "or-second-types", "organic-reactions"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]


def facts(name, rows, explain, pace="recall"):
    return Q(name, "orgo.reasoning", "{{q}}", pace=pace, cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


ADD = [
    ("OR-1.1.B", Q("or-centres-from-max", "orgo.reasoning", "A molecule with no internal mirror plane has at most {{2^k}} stereoisomers. How many stereocentres does it have?", pace="recall",
        given={"k": {"int": [1, 6]}}, value="k", tex="n", final=True, verify="log(Integer(2)**k, 2)",
        explain="2ⁿ stereoisomers for n stereocentres; a meso form (internal mirror) lowers the count")),
    ("OR-1.1.C", Q("or-carbon-ox-group", "orgo.reasoning", "What is the oxidation state of the carbon in {{c}}?", pace="recall",
        cases=[{"c": "the CH₂OH carbon of ethanol", "h": 2, "o": 1}, {"c": "the carbonyl carbon of acetone", "h": 0, "o": 2}, {"c": "the carboxyl carbon of acetic acid", "h": 0, "o": 3},
               {"c": "the carbonyl carbon of acetaldehyde", "h": 1, "o": 2}, {"c": "carbon dioxide", "h": 0, "o": 4}, {"c": "the methyl carbon of ethane", "h": 3, "o": 0}],
        value="o - h", tex="", final=True, verify="o - h",
        explain="Count +1 for each bond to O (a C=O counts twice), −1 for each H, 0 for each C: alcohol −1 → aldehyde +1 → acid +3")),
    ("OR-1.2.D", Q("or-activator-rank", "orgo.reasoning", "Which substituent makes benzene react fastest with an electrophile?", pace="recall",
        cases=[{"o1": "–NH₂", "o2": "–CH₃", "o3": "–Cl", "o4": "–NO₂"}, {"o1": "–OH", "o2": "–Br", "o3": "–CO₂CH₃", "o4": "–CF₃"},
               {"o1": "–OCH₃", "o2": "–H", "o3": "–CHO", "o4": "–SO₃H"}, {"o1": "–CH₃", "o2": "–Cl", "o3": "–CN", "o4": "–NO₂"}],
        choice=MC, correct="0", verify="authored",
        explain="Lone-pair donors (NH₂, OH, OR) activate strongly; alkyls weakly; halogens deactivate yet direct ortho/para; C=O, CN, NO₂, CF₃ deactivate and direct meta")),
    ("OR-8.1.A", facts("or-sn2-requirements", [
        ("(R)-2-bromobutane reacts with hydroxide by SN2. What is the configuration of the product?", "(S)-butan-2-ol: inversion", "(R)-butan-2-ol: retention", "A racemic mixture", "No stereocentre remains"),
        ("Which substrate reacts fastest by SN2?", "Methyl bromide", "tert-Butyl bromide", "Neopentyl bromide", "2-Bromo-2-methylbutane"),
        ("Which solvent speeds an SN2 reaction with an anionic nucleophile?", "A polar aprotic solvent such as DMSO", "Water", "Methanol", "Hexane"),
    ], "One step, backside attack, inversion; crowding at carbon slows it and polar aprotic solvents leave the nucleophile bare")),
    ("OR-8.1.B", facts("or-e2-requirements", [
        ("What geometry does E2 require between the leaving group and the hydrogen removed?", "Anti-periplanar (180°)", "Syn-periplanar (0°)", "Gauche (60°)", "Any geometry"),
        ("On a cyclohexane ring, where must the leaving group be for E2?", "Axial, anti to an axial hydrogen", "Equatorial", "Either position", "In the plane of the ring"),
        ("With tert-butoxide as the base, which alkene is the major E2 product of 2-bromo-2-methylbutane?", "The less substituted (Hofmann) alkene", "The more substituted (Zaitsev) alkene", "An equal mixture", "No alkene"),
    ], "E2 is concerted: the C–H and C–LG bonds must be anti-periplanar; bulky bases take the more reachable hydrogen")),
]
