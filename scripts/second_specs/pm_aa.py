"""Abstract Algebra (AA, Nov 2026): groups, permutations, actions, quotients and a first look at rings. Structure in
UNITS (written by scripts/pm_setup.py), two question types per objective.

Basis: the Cambridge Part IA Groups and Part IB Groups, Rings and Modules schedules (read through an extraction of
the 2026-27 Schedules booklet). Cards answer by the theorem; tests/verify/pmcalc.py applies the permutations, counts
the residues and enumerates the colourings."""
from math import factorial, gcd
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "aa-algebra", "abstract-algebra", "P1"
FW = dict(id="abstract-algebra", title="Abstract Algebra", code="AA", domain="aa", requires=["number-theory", "linear-algebra"], level=4,
          primary="cambridge-ia-groups", also=["cambridge-ib-grm"],
          note="Anchored on the Cambridge Groups and Groups, Rings and Modules schedules (read through an extraction). Group theory is the weight, since it is what chemistry uses; rings stop at unique factorisation, and modules appear only as the classification of finite abelian groups. Fields and Galois theory are not built.",
          header=["Groups first, because symmetry is where chemistry meets algebra: point groups, permutations of identical",
                  "nuclei and counting distinct structures all sit on units 1-3. Advanced Inorganic drills point-group symbols;",
                  "this framework is what the symbols mean. Proofs are drilled as the counts they force."])
SKILLS = [("groups", "Group axioms, orders of elements, subgroups and Lagrange's theorem", "Groups and subgroups", []),
          ("perms", "Cycle notation, sign and conjugacy in symmetric groups", "Permutations", ["aa.groups"]),
          ("actions", "Orbits, stabilisers, Burnside counting and the class equation", "Group actions", ["aa.perms"]),
          ("quotients", "Normal subgroups, homomorphisms, abelian groups and the Sylow theorems", "Quotients and structure", ["aa.actions"]),
          ("rings", "Units and zero divisors, ideals, fields and unique factorisation", "Rings", ["aa.quotients"])]
IDEAS = [("SYM", "A group is the symmetries of something", "Every group acts, and counting orbits and stabilisers is how its structure is read off."),
         ("DIV", "Orders divide", "Lagrange's theorem and its relatives turn structural questions into arithmetic on the order of the group.")]
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
GP, PM, AC, QT, RG = "aa.groups", "aa.perms", "aa.actions", "aa.quotients", "aa.rings"
G = lambda *s: [f"cambridge-ia-groups:{x}" for x in s]
R = lambda *s: [f"cambridge-ib-grm:{x}" for x in s]


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", **kw):
    return Q(name, skill, prompt, value=value, tex=tex, final=True, verify=verify, explain=explain, **kw)


def lcm(*xs):
    r = 1
    for x in xs: r = r * x // gcd(r, x)
    return r


def cyc(s):  # '123|45' -> '(1 2 3)(4 5)'
    return "".join("(" + " ".join(c) + ")" for c in s.split("|"))


def phi(n):
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)


def necklaces(n, k):
    return sum(k ** gcd(n, r) for r in range(n)) // n


def class_size(t):
    n, d = sum(t), 1
    for ln in set(t): d *= ln ** t.count(ln) * factorial(t.count(ln))
    return factorial(n) // d


def sylow(order, p):
    m = order
    while m % p == 0: m //= p
    return sum(1 for d in range(1, m + 1) if m % d == 0 and d % p == 1)


UNITS = {
 1: ("groups", "Groups and subgroups", G("G1", "G2"), ["SYM", "DIV"], {
   1: ("Axioms, orders and Lagrange", [
     ("A", G("G1"), "Decide whether a set with an operation is a group and name the axiom that fails.",
      "A group needs closure, associativity, an identity and an inverse for every element. Commutativity is not required.", "P2", [
       Q("aa-is-it-a-group", GP, "Is this a group: {{st}}?", pace="recall", cases=[
           {"st": "the integers under addition", "kc": 0}, {"st": "the integers under multiplication", "kc": 1}, {"st": "the non-zero rationals under multiplication", "kc": 0},
           {"st": "the natural numbers under addition", "kc": 1}, {"st": "invertible 2×2 real matrices under multiplication", "kc": 0}, {"st": "all 2×2 real matrices under multiplication", "kc": 1},
           {"st": "{1, −1, i, −i} under multiplication", "kc": 0}, {"st": "the odd integers under addition", "kc": 1}, {"st": "the non-zero residues modulo 6 under multiplication", "kc": 1},
           {"st": "the non-zero residues modulo 7 under multiplication", "kc": 0}],
         choice=["Yes", "No"], correct="kc", verify="authored",
         explain="Look for what is missing: integers lack multiplicative inverses, odd integers are not closed under addition, and modulo 6 the product 2 · 3 is 0, which is not in the set"),
       F("aa-failed-axiom", GP, [
           ("The integers under subtraction are not a group because subtraction is not:", "Associative", "Closed", "Defined for negatives", "Invertible"),
           ("The natural numbers 1, 2, 3, … under addition fail to be a group for want of:", "An identity and inverses", "Closure", "Associativity", "Commutativity"),
           ("All 2×2 real matrices under multiplication fail to be a group because:", "Singular matrices have no inverse", "Multiplication is not associative", "There is no identity", "The set is not closed"),
           ("Which property is NOT required of a group?", "Commutativity", "Associativity", "An identity", "Inverses")],
         "Test the axioms in order. Many natural examples fail only on inverses, and restricting to the invertible elements repairs them")]),
     ("B", G("G1", "G2"), "Find the order of an element of a cyclic group and count elements of a given order.",
      "In Z_n the element a has order n/gcd(a, n). A cyclic group of order n has φ(d) elements of order d for each divisor d, and none of any other order.", "P1", [
       N("aa-order-in-zn", GP, "What is the order of {{ka}} in the additive group Z_{{kn}}?", "kn/gcd(ka, kn)", "lcm(ka, kn)/ka",
         "Adding a to itself first returns to 0 at the least common multiple of a and n, which is n/gcd(a, n) additions", tex="order",
         given={"ka": {"pick": [4, 6, 8, 9, 10]}, "kn": {"pick": [12, 18, 20, 30]}}),
       N("aa-count-order-d", GP, "How many elements of order {{kd}} are there in the cyclic group Z_{{kn}}?", "kans", "pm_zn_count_order(kn, kd)",
         "A cyclic group has exactly one subgroup of each order dividing n, and that subgroup has φ(d) generators", tex="elements",
         cases=[{"kn": n, "kd": d, "kans": phi(d)} for n, d in [(12, 4), (12, 6), (20, 5), (30, 6), (18, 9), (24, 8), (30, 15)]])]),
     ("C", G("G2"), "Use Lagrange's theorem to limit subgroup orders and count cosets.",
      "The order of a subgroup divides the order of the group, and the index |G|/|H| is the number of cosets. A group of prime order is cyclic.", "P1", [
       N("aa-coset-count", GP, "A group of order {{kg}} has a subgroup of order {{kh}}. How many left cosets does the subgroup have?", "kg/kh", "solve(Eq(Symbol('m')*kh, kg), Symbol('m'))[0]",
         "The cosets partition the group into pieces of equal size, so there are |G|/|H| of them", tex="cosets",
         cases=[{"kg": g, "kh": h} for g, h in [(24, 6), (60, 12), (48, 8), (120, 24), (36, 4), (100, 20)]]),
       F("aa-lagrange-facts", GP, [
           ("A group of order 35 cannot have a subgroup of order:", "10", "5", "7", "1"),
           ("Every group of prime order is:", "Cyclic", "Non-abelian", "Trivial", "A symmetric group"),
           ("The order of an element of a finite group always:", "Divides the order of the group", "Equals the order of the group", "Is prime", "Is even"),
           ("The alternating group A₄ has order 12 but no subgroup of order 6. This shows that:", "The converse of Lagrange's theorem is false", "Lagrange's theorem is false", "A₄ is cyclic", "A₄ is abelian"),
           ("Fermat's little theorem follows from Lagrange applied to:", "The units modulo p, a group of order p − 1", "The integers modulo p under addition", "The symmetric group S_p", "The cyclic group of order p")],
         "Lagrange says which orders are possible, not which occur. A₄ is the standard example of a divisor with no subgroup")]),
     ("D", G("G2"), "Find the order of the group of units modulo n and decide whether it is cyclic.",
      "The units modulo n form a group of order φ(n). It is cyclic exactly for n = 1, 2, 4, p^k and 2p^k with p an odd prime.", "P1", [
       N("aa-unit-group-order", GP, "How many elements has the group of units modulo {{kn}}?", "kans", "pm_phi(kn)",
         "A residue is a unit exactly when it is coprime to n, so the order is φ(n)", tex="order",
         cases=[{"kn": n, "kans": phi(n)} for n in (8, 9, 12, 15, 16, 20, 24)]),
       Q("aa-unit-group-cyclic", GP, "Is the group of units modulo {{kn}} cyclic?", pace="recall", cases=[
           {"kn": 5, "kc": 0}, {"kn": 8, "kc": 1}, {"kn": 9, "kc": 0}, {"kn": 10, "kc": 0}, {"kn": 12, "kc": 1}, {"kn": 14, "kc": 0}, {"kn": 15, "kc": 1}, {"kn": 16, "kc": 1}],
         choice=["Yes", "No"], correct="kc", verify="authored",
         explain="Cyclic only for 1, 2, 4, odd prime powers and twice odd prime powers. Modulo 8 every unit squares to 1, so no element has order 4")])]),
 }),
 2: ("perms", "Permutations", G("G6"), ["SYM"], {
   1: ("Cycles, sign and conjugacy", [
     ("A", G("G6"), "Compose permutations in cycle notation and find the order of a permutation.",
      "Disjoint cycles commute and the order of a permutation is the least common multiple of its cycle lengths. Products are applied right to left.", "P1", [
       N("aa-perm-order", PM, "What is the order of the permutation {{sh}}?", "kans", "pm_perm_order(cy)",
         "Each cycle returns to the identity after its own length, so the whole permutation does after the least common multiple", tex="order",
         cases=[{"cy": c, "sh": cyc(c), "kans": lcm(*[len(x) for x in c.split("|")])} for c in ("123|45", "1234|56", "123|4567", "12|345|6789", "12345|67", "123|456")]),
       N("aa-perm-compose", PM, "Let σ = {{s1}} and τ = {{s2}}. Where does στ (apply τ first, then σ) send {{kx}}?", "kans", "pm_perm_image(c1, c2, kx)",
         "Follow the point through the right-hand permutation first, then through the left-hand one", tex="image",
         cases=[{"c1": a, "c2": b, "s1": cyc(a), "s2": cyc(b), "kx": x, "kans": y} for a, b, x, y in [
             ("123", "12", 1, 3), ("123", "12", 2, 2), ("12", "123", 1, 1), ("1234", "13", 3, 2), ("13|24", "123", 2, 1), ("1234", "243", 4, 4)]])]),
     ("B", G("G6"), "Find the sign of a permutation and work with the alternating group.",
      "A cycle of length k is a product of k − 1 transpositions, so it is even when k is odd. The even permutations form A_n, of order n!/2.", "P1", [
       N("aa-perm-sign", PM, "What is the sign of the permutation {{sh}}? Answer 1 for even, −1 for odd.", "kans", "pm_perm_sign(cy)",
         "Add up (length − 1) over the cycles: an even total is an even permutation", tex="sign",
         cases=[{"cy": c, "sh": cyc(c), "kans": (-1) ** sum(len(x) - 1 for x in c.split("|"))} for c in ("123|45", "1234", "12|34", "12345", "123|4567", "12|34|56")]),
       N("aa-alternating-order", PM, "How many elements has the alternating group A_{{kn}}?", "factorial(kn)/2", "solve(Eq(2*Symbol('m'), factorial(kn)), Symbol('m'))[0]",
         "Multiplying by a fixed transposition pairs each even permutation with an odd one, so exactly half are even", tex="order",
         given={"kn": {"pick": [4, 5, 6, 7]}})]),
     ("C", G("G6", "G3"), "Count conjugacy classes in a symmetric group and the size of a class.",
      "Two permutations are conjugate in S_n exactly when they have the same cycle type, so the classes are the partitions of n. A class with m_k cycles of length k has n!/Π(k^m_k · m_k!) elements.", "P1", [
       N("aa-sn-class-count", PM, "How many conjugacy classes has the symmetric group S_{{kn}}?", "kans", "pm_partitions(kn)",
         "One class per cycle type, so count the partitions of n. For n = 4: 4, 3+1, 2+2, 2+1+1, 1+1+1+1", tex="classes",
         cases=[{"kn": 3, "kans": 3}, {"kn": 4, "kans": 5}, {"kn": 5, "kans": 7}, {"kn": 6, "kans": 11}, {"kn": 7, "kans": 15}]),
       N("aa-sn-class-size", PM, "How many permutations in S_{{kn}} have cycle type {{sh}}?", "kans", "pm_sn_class_size(ty)",
         "Divide n! by the length of each cycle (rotating a cycle changes nothing) and by m! for each set of m equal cycles (reordering them changes nothing)", tex="permutations",
         cases=[{"kn": sum(t), "sh": " + ".join(map(str, t)), "ty": ",".join(map(str, t)), "kans": class_size(t)} for t in ([2, 1, 1], [2, 2], [3, 1], [3, 2], [2, 2, 1], [4, 1], [3, 3], [2, 2, 2])])])]),
 }),
 3: ("actions", "Group actions", G("G3", "G5"), ["SYM", "DIV"], {
   1: ("Orbits, stabilisers and counting", [
     ("A", G("G3", "G5"), "Use the orbit-stabiliser theorem to find the order of a symmetry group.",
      "|G| = |orbit| × |stabiliser|. The rotations of a cube move a face to any of 6 faces and 4 rotations fix a face, so there are 24.", "P1", [
       N("aa-orbit-stabiliser", AC, "The rotation group of a regular {{nm}} acts on its {{kf}} faces, all in one orbit, and {{ks}} rotations fix a given face. How many rotations are there?", "kf*ks", "solve(Eq(Symbol('m')/ks, kf), Symbol('m'))[0]",
         "The group's order is the size of an orbit times the size of a stabiliser. The same count works on vertices or edges and must agree", tex="|G|",
         cases=[{"nm": "tetrahedron", "kf": 4, "ks": 3}, {"nm": "cube", "kf": 6, "ks": 4}, {"nm": "octahedron", "kf": 8, "ks": 3}, {"nm": "dodecahedron", "kf": 12, "ks": 5}, {"nm": "icosahedron", "kf": 20, "ks": 3}]),
       N("aa-stabiliser-size", AC, "A group of order {{kg}} acts on a set, and one point has an orbit of size {{ko}}. How many group elements fix that point?", "kg/ko", "solve(Eq(Symbol('m')*ko, kg), Symbol('m'))[0]",
         "Orbit size times stabiliser size is the group order, so orbit sizes always divide the order of the group", tex="|\\mathrm{Stab}|",
         cases=[{"kg": g, "ko": o} for g, o in [(24, 8), (60, 12), (48, 6), (120, 20), (24, 12), (60, 30)]])]),
     ("B", G("G3"), "Count orbits with Burnside's lemma.",
      "The number of orbits is the average number of fixed points: (1/|G|) Σ |Fix(g)|. A rotation by r places of an n-bead ring fixes k^gcd(n, r) colourings.", "P1", [
       N("aa-necklaces", AC, "How many different rings of {{kn}} beads can be made with {{kk}} colours, if rings that differ by a rotation count as the same?", "kans", "pm_necklaces(kn, kk)",
         "Average k^gcd(n, r) over the n rotations. For a prime n this is (k^n + (n − 1)k)/n", tex="rings",
         cases=[{"kn": n, "kk": k, "kans": necklaces(n, k)} for n, k in [(3, 2), (4, 2), (5, 2), (6, 2), (4, 3), (5, 3), (3, 3)]]),
       N("aa-burnside-average", AC, "A group of order {{kg}} acts on a set. Its elements fix {{kl}} points in total (summing the fixed points of every element). How many orbits are there?", "kl/kg", "solve(Eq(Symbol('m')*kg, kl), Symbol('m'))[0]",
         "Burnside: the number of orbits is the total number of fixed points divided by the order of the group", tex="orbits",
         cases=[{"kg": 4, "kl": 24}, {"kg": 6, "kl": 48}, {"kg": 12, "kl": 36}, {"kg": 24, "kl": 240}, {"kg": 8, "kl": 48}])]),
     ("C", G("G3") + R("GR"), "Use centralisers, the class equation and Cauchy's theorem.",
      "The size of a conjugacy class is |G| divided by the size of the centraliser. The class equation forces a non-trivial centre in a p-group, and Cauchy: if a prime p divides |G| there is an element of order p.", "P1", [
       N("aa-centraliser-size", AC, "In S_{{kn}}, how many permutations commute with a given permutation of cycle type {{sh}}?", "kans", "factorial(kn)/pm_sn_class_size(ty)",
         "The class of that cycle type has n!/|centraliser| elements, and the centraliser is generated by rotating each cycle and swapping equal ones", tex="|C(g)|",
         cases=[{"kn": sum(t), "sh": " + ".join(map(str, t)), "ty": ",".join(map(str, t)), "kans": factorial(sum(t)) // class_size(t)} for t in ([2, 1, 1], [2, 2], [3, 1], [3, 2], [4, 1], [2, 2, 1])]),
       F("aa-class-equation-facts", AC, [
           ("The class equation of S₃ (sizes of its conjugacy classes) is:", "1 + 2 + 3", "1 + 1 + 4", "2 + 2 + 2", "1 + 5"),
           ("A group of order p², p prime, must be:", "Abelian", "Cyclic", "Simple", "Non-abelian"),
           ("The centre of a non-trivial group of prime-power order is always:", "Non-trivial", "Trivial", "The whole group", "Of order p exactly"),
           ("Cauchy's theorem: a group of order 30 must contain an element of order:", "5", "6", "10", "15"),
           ("An element lies in the centre exactly when its conjugacy class has size:", "1", "2", "|G|", "p")],
         "Class sizes divide |G| and sum to |G|. In a p-group every non-central class has size divisible by p, so the centre cannot be just the identity")])]),
 }),
 4: ("quotients", "Quotients and structure", G("G4") + R("GR", "MO"), ["DIV"], {
   1: ("Homomorphisms, abelian groups and Sylow", [
     ("A", G("G4") + R("GR"), "Apply the first isomorphism theorem and count homomorphisms between cyclic groups.",
      "The image of a homomorphism is isomorphic to G/ker, so |image| = |G|/|kernel|. A homomorphism from Z_m to Z_n is fixed by where 1 goes, and there are gcd(m, n) of them.", "P1", [
       N("aa-image-size", QT, "A homomorphism from a group of order {{kg}} has a kernel of order {{kk}}. How many elements has its image?", "kg/kk", "solve(Eq(Symbol('m')*kk, kg), Symbol('m'))[0]",
         "The image is the quotient by the kernel: each element of the image is hit by exactly |kernel| elements", tex="|\\mathrm{im}|",
         cases=[{"kg": g, "kk": k} for g, k in [(24, 4), (60, 5), (36, 12), (120, 60), (48, 16), (30, 6)]]),
       N("aa-hom-count", QT, "How many group homomorphisms are there from Z_{{km}} to Z_{{kn}}?", "gcd(km, kn)", "pm_hom_count(km, kn)",
         "The image a of 1 must satisfy m·a = 0 in Z_n, and exactly gcd(m, n) residues do", tex="homomorphisms",
         given={"km": {"pick": [4, 6, 8, 10, 12]}, "kn": {"pick": [6, 9, 12, 15, 20]}})]),
     ("B", R("MO"), "Classify finite abelian groups of a given order and decide when a product is cyclic.",
      "Every finite abelian group is a product of cyclic groups of prime-power order. For n = Π p^a the number of abelian groups is Π (number of partitions of a). Z_m × Z_n is cyclic exactly when gcd(m, n) = 1.", "P1", [
       N("aa-abelian-count", QT, "How many abelian groups of order {{kn}} = 2^{{ka}} · 3^{{kb}} are there, up to isomorphism?", "kans", "pm_partitions(ka)*pm_partitions(kb)",
         "Split each prime power separately: 2^a can be broken up in as many ways as a has partitions, and likewise 3^b", tex="groups",
         cases=[{"kn": 2 ** a * 3 ** b, "ka": a, "kb": b, "kans": [1, 1, 2, 3, 5][a] * [1, 1, 2, 3][b]} for a, b in [(2, 1), (3, 1), (2, 2), (3, 2), (4, 1), (4, 2), (1, 3)]]),
       N("aa-product-max-order", QT, "What is the largest order of an element of Z_{{km}} × Z_{{kn}}?", "lcm(km, kn)", "km*kn/gcd(km, kn)",
         "The order of (a, b) is the least common multiple of the two orders, so the maximum is lcm(m, n); the product is cyclic only when that equals mn", tex="order",
         given={"km": {"pick": [4, 6, 9, 10]}, "kn": {"pick": [6, 8, 12, 15]}})]),
     ("C", R("GR"), "Use the Sylow theorems to limit the number of Sylow subgroups.",
      "If |G| = p^a m with p not dividing m, the number of Sylow p-subgroups divides m and is 1 mod p. When that leaves only 1, the subgroup is normal and the group is not simple.", "P1", [
       N("aa-sylow-options", QT, "By the Sylow theorems, how many values are possible for the number of Sylow {{kp}}-subgroups of a group of order {{kg}}?", "kans", "pm_sylow_options(kg, kp)",
         "List the divisors of the part of the order prime to p and keep those that are 1 mod p", tex="values",
         cases=[{"kg": g, "kp": p, "kans": sylow(g, p)} for g, p in [(12, 3), (12, 2), (15, 5), (20, 5), (30, 5), (24, 2), (56, 7), (60, 5)]]),
       F("aa-sylow-facts", QT, [
           ("A group of order 15 is cyclic because the Sylow theorems force:", "One Sylow 3-subgroup and one Sylow 5-subgroup, both normal", "Three Sylow 5-subgroups", "No element of order 3", "A trivial centre"),
           ("A Sylow p-subgroup is normal exactly when:", "It is the only Sylow p-subgroup", "p is the largest prime dividing |G|", "It is cyclic", "Its order is p"),
           ("The order of a Sylow 2-subgroup of S₄ (order 24) is:", "8", "2", "4", "16"),
           ("Any two Sylow p-subgroups of a finite group are:", "Conjugate", "Equal", "Disjoint", "Abelian")],
         "For order 15, the count of Sylow 5-subgroups divides 3 and is 1 mod 5, so it is 1; the count of Sylow 3-subgroups divides 5 and is 1 mod 3, so it is 1")])]),
 }),
 5: ("rings", "Rings", R("RI"), ["DIV"], {
   1: ("Units, ideals and factorisation", [
     ("A", R("RI"), "Count units, zero divisors and idempotents in Z_n.",
      "In Z_n a non-zero residue is a unit if it is coprime to n and a zero divisor otherwise. Z_n has 2^k idempotents, where k is the number of distinct primes dividing n.", "P1", [
       N("aa-zero-divisors", RG, "How many zero divisors (non-zero elements a with ab = 0 for some non-zero b) has the ring Z_{{kn}}?", "kans", "pm_zero_divisors(kn)",
         "Every non-zero residue is a unit or a zero divisor, so the count is n − 1 − φ(n)", tex="zero divisors",
         cases=[{"kn": n, "kans": n - 1 - phi(n)} for n in (6, 8, 10, 12, 15, 18, 20)]),
       N("aa-idempotents", RG, "How many elements e of Z_{{kn}} satisfy e² = e?", "kans", "pm_idempotents(kn)",
         "By the Chinese remainder theorem Z_n is a product of rings Z_(p^a), each with only the idempotents 0 and 1, so there are 2^k in all", tex="idempotents",
         cases=[{"kn": n, "kans": sum(1 for a in range(n) if a * a % n == a)} for n in (6, 8, 10, 12, 30, 15, 9)])]),
     ("B", R("RI"), "Decide whether a quotient ring is a field and count roots of a polynomial over Z_p.",
      "Z_n is a field exactly when n is prime, and F[x]/(f) is a field exactly when f is irreducible. Over a field a polynomial of degree d has at most d roots; over Z_n with n composite it can have more.", "P2", [
       Q("aa-field-or-not", RG, "The ring {{rg}} is:", pace="recall", cases=[
           {"rg": "Z₇", "kc": 0}, {"rg": "Z₉", "kc": 2}, {"rg": "the integers Z", "kc": 1}, {"rg": "Z₂[x]/(x² + x + 1)", "kc": 0}, {"rg": "R[x]/(x² + 1)", "kc": 0},
           {"rg": "R[x]/(x² − 1)", "kc": 2}, {"rg": "the Gaussian integers Z[i]", "kc": 1}, {"rg": "Z₆", "kc": 2}, {"rg": "the polynomial ring Q[x]", "kc": 1}],
         choice=["A field", "An integral domain but not a field", "Not an integral domain"], correct="kc", verify="authored",
         explain="A quotient by an irreducible polynomial is a field (R[x]/(x² + 1) is the complex numbers); a reducible one gives zero divisors, since (x − 1)(x + 1) = 0 in R[x]/(x² − 1)"),
       N("aa-roots-mod-n", RG, "How many roots has x² − 1 in Z_{{kn}}?", "kans", "pm_poly_roots_mod('-1,0,1', kn)",
         "Over a field a quadratic has at most 2 roots. Modulo a composite n the bound fails: solve modulo each prime power and combine by the Chinese remainder theorem", tex="roots",
         cases=[{"kn": n, "kans": sum(1 for x in range(n) if (x * x - 1) % n == 0)} for n in (7, 8, 12, 15, 24, 11, 21)])]),
     ("C", R("RI"), "Work with norms in the Gaussian integers and recognise failures of unique factorisation.",
      "N(a + bi) = a² + b² is multiplicative, so an element of prime norm is irreducible. Z[i] has unique factorisation; Z[√−5] does not, since 6 = 2 · 3 = (1 + √−5)(1 − √−5).", "P1", [
       N("aa-gaussian-norm", RG, "Find the norm of the product ({{ka}} + {{kb}}i)({{kc}} + {{kd}}i) in the Gaussian integers.", "(ka^2 + kb^2)*(kc^2 + kd^2)", "Abs((ka + kb*I)*(kc + kd*I))**2",
         "The norm is multiplicative, so multiply the two norms instead of the two numbers. This is also why a product of two sums of two squares is a sum of two squares", tex="N",
         given={"ka": {"pick": [1, 2, 3]}, "kb": {"pick": [1, 2, 4]}, "kc": {"pick": [2, 3, 5]}, "kd": {"pick": [1, 3]}}),
       F("aa-factorisation-facts", RG, [
           ("In Z[√−5], 6 = 2 · 3 = (1 + √−5)(1 − √−5). This shows the ring is not:", "A unique factorisation domain", "An integral domain", "Commutative", "A ring"),
           ("Eisenstein's criterion with p = 2 shows which polynomial is irreducible over Q?", "x³ + 2x + 2", "x² − 4", "x² + 2x + 1", "x³ − 8"),
           ("Every Euclidean domain is a principal ideal domain, and every principal ideal domain is:", "A unique factorisation domain", "A field", "Finite", "A polynomial ring"),
           ("The units of the Gaussian integers are:", "1, −1, i, −i", "1 and −1", "All elements of norm 2", "Only 1"),
           ("In Z[x] the ideal (2, x) is not principal, so Z[x] is:", "A unique factorisation domain that is not a principal ideal domain", "A principal ideal domain", "A field", "Not an integral domain")],
         "Irreducible and prime mean the same thing only where factorisation is unique. In Z[√−5] the number 2 is irreducible but divides a product without dividing either factor")])]),
 }),
}
ADD = [(f"{FW['code']}-{n}.{tn}.{lo[0]}", qq) for n, u in UNITS.items() for tn, (tt, los) in u[4].items() for lo in los for qq in lo[5]]
