"""Materials Science and Engineering (MSE, Nov 2026): crystal structure, defects and dislocations, deformation and
strengthening, diffusion, phase diagrams and transformations, failure, and the material classes. Structure in UNITS
(written by scripts/fw_setup.py), two question types per objective.

Basis: the Engineers Canada Materials Engineering examination syllabus (2021), exams 21-Mat-A3, A4, A5, B6, B8 and
B11, read to the topics each description names through an extraction of the syllabus page, so read: part; and the
NCEES FE Mechanical specification section 9, read to its lettered lines. Neither names a Burgers vector or a Miller
index: both stop at "crystal structures" and "plastic deformation", so the objectives under those lines are ours, in
the order of an introductory text (Callister; chapter order from memory, never cited on an item).

There is no lattice figure type yet. Burgers circuits, Miller indices and slip systems are asked in words and
numbers; drawing a plane in a cell, tracing a circuit on a picture and reading a phase diagram off a plot wait on
figures. Phase-diagram cards print the compositions they need."""
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "mse-core", "materials-science", "P1"
M = "Symbol('m')"
FW = dict(id="materials-science", title="Materials Science and Engineering", code="MSE", domain="mse", track="engineering",
          requires=["chemistry", "physics", "calculus", "engineering-mechanics"], level=3,
          primary="engineers-canada-materials", also=["fe-mechanical"], subject="Materials Science",
          note="Anchored on the Engineers Canada materials syllabus (exams A3, A4, A5, B6, B8, B11) and FE Mechanical section 9, both read to their topic lines. Dislocation geometry, Miller indices and slip systems sit under lines that say only 'crystal structures' and 'plastic deformation', so those objectives are a house list in textbook order. Asked in words and numbers: no lattice or phase-diagram figure type exists yet. Polymers, colloids, selection and corrosion are in Polymers and Materials (MT); axial stress and Mohr's circle are in Engineering Mechanics.",
          header=["Why a metal bends and a ceramic snaps: atoms on a lattice, the defects in it, and how dislocations,",
                  "diffusion and phase changes set strength, toughness and conductivity. Crystal geometry first, then",
                  "defects and the Burgers vector, then what processing does to them."],
          source=dict(id="mse-outline", title="Materials science by syllabus exam (course outline)", short="MSE outline", field="materials science",
                      note=["The Engineers Canada materials exams and FE Mechanical section 9 written as a source so the mse.* skills have a home.",
                            "NOT a book: only the syllabus topic lines were read. Chapter numbers are ours."]))
_EC = [("A3.1", "Crystal structures of metals, ceramics and polymers"), ("A3.2", "Elemental and diffraction analysis (EDS, XPS, XRD)"), ("A3.3", "Optical and electron microscopy"),
       ("A3.4", "Thermal analysis (DTA, DSC, TGA)"), ("A4.1", "Elastic and plastic deformation"), ("A4.2", "Strengthening mechanisms"), ("A4.3", "Fracture mechanisms"),
       ("A4.4", "Introductory fracture mechanics"), ("A4.5", "High-temperature creep"), ("A4.6", "Cyclic stress and fatigue crack growth"), ("A4.7", "Thermal properties"),
       ("A4.8", "Electronic properties"), ("A5.1", "Binary phase diagrams"), ("A5.2", "Annealing and heat treatment"), ("A5.3", "Crystallization kinetics"), ("A5.4", "Diffusion"),
       ("A5.5", "Nucleation and growth"), ("A5.6", "Amorphous materials and the glass transition"), ("A5.7", "Time-temperature-transformation diagrams"),
       ("B6.1", "Bonding and ceramic structures"), ("B6.2", "Defects in ceramics"), ("B6.3", "Mechanical properties of ceramics"), ("B6.4", "Thermal stresses"),
       ("B8.1", "Band theory"), ("B8.2", "Semiconductors"), ("B8.3", "Magnetism and superconductivity"), ("B11.1", "Isostress and isostrain loading of composites"),
       ("B11.2", "Reinforcement type, orientation and length")]
STDS = [{"id": "engineers-canada-materials", "name": "Engineers Canada Examination Syllabus: Materials Engineering (2021)", "publisher": "Engineers Canada", "kind": "exam-spec", "read": "part",
         "url": "https://engineerscanada.ca/become-an-engineer/examination-syllabi/materials-engineering-syllabus",
         "note": "Read Nov 2026 through an extraction of the syllabus page: the exam list (A1-A7, B1-B11) and the topics named in the descriptions of A3, A4, A5, A6, A7, B6, B7, B8 and B11. Items are the topics of A3, A4, A5 and the parts of B6, B8 and B11 this framework answers, coded and titled by us. Not itemised here: A1 and A2 (thermodynamics, transport: other frameworks), A6 and A7 (selection, corrosion: Polymers and Materials unit 4), B7 (polymers: Polymers and Materials unit 1), dielectrics in B6 and B8, fabrication and failure modes in B11, and the extractive metallurgy exams B1-B5, B9, B10, which were read by title only.",
         "items": [{"code": c, "title": t} for c, t in _EC]}]
SKILLS = [("structure", "Unit cells, packing, density, Miller indices, interplanar spacing and diffraction", "Crystal structure", []),
          ("defects", "Vacancies, solid solutions, edge and screw dislocations, the Burgers circuit and vector, grain boundaries", "Defects and dislocations", ["mse.structure"]),
          ("deformation", "Slip systems, Schmid's law, strengthening mechanisms and the tensile curve", "Deformation and strengthening", ["mse.defects"]),
          ("diffusion", "Fick's laws, Arrhenius diffusivity and diffusion distance", "Diffusion in solids", ["mse.defects"]),
          ("phases", "Phase rule, lever rule, eutectics, the iron-carbon system, TTT diagrams, nucleation and heat treatment", "Phase diagrams and transformations", ["mse.diffusion"]),
          ("failure", "Fracture toughness, Griffith cracks, stress concentration, fatigue and creep", "Failure", ["mse.deformation"]),
          ("classes", "Ceramics, composites, electronic and magnetic behaviour, alloys, processing and characterisation", "Material classes and characterisation", ["mse.structure"])]
IDEAS = [("LATTICE", "Structure sets what can move", "Which planes are densest and which directions are shortest decide how a crystal slips, diffracts and packs; everything else is counted from the unit cell."),
         ("DEFECT", "Properties live in the defects", "A perfect crystal would be a thousand times stronger and far less useful: vacancies carry diffusion, dislocations carry plastic flow, and every strengthening method is a way to pin a dislocation."),
         ("PATH", "Processing chooses the microstructure", "The phase diagram says where equilibrium is; cooling rate, cold work and heat treatment decide how far the material gets there, and so which phases and grain sizes it ends with.")]
PRACTICES = [("P1", "Compute", "Carry a geometric, rate or mechanical relation to a number with its unit."),
             ("P2", "Classify", "Name the structure, defect, mechanism or technique a description points to.")]
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
SK, DF, DE, DI, PH, FA, CL = ["mse." + s[0] for s in SKILLS]
X = lambda *s: [f"engineers-canada-materials:{x}" for x in s]
E_ = lambda *s: [f"fe-mechanical:{x}" for x in s]
KB, KBS = "8.617333e-5", "Rational('8.617333e-5')"
RG, RGS = "8.314", "Rational('8.314')"
NA, NAS = "6.022e23", "Rational('6.022e23')"


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def L(name, skill, prompt, options, rows, explain):
    return Q(name, skill, prompt, pace="recall", cases=[{"q": a, "kc": k} for a, k in rows], choice=options, correct="kc", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", **kw):
    return Q(name, skill, prompt, value=value, tex=tex, verify=verify, explain=explain, **kw)


def C(keys, rows):
    return [dict(zip(keys.split(), r)) for r in rows]


U1 = ("structure", "Crystal structure", X("A3.1", "A3.2") + E_("9A"), ["LATTICE"], {
   1: ("Unit cells", [
     ("A", X("A3.1"), "Count the atoms in a cubic unit cell and state its coordination number.",
      "A corner atom is shared by 8 cells, a face atom by 2, a body atom by 1. FCC holds 4 atoms with 12 nearest neighbours; BCC holds 2 with 8; simple cubic holds 1 with 6.", "P1", [
       F("mse-cell-facts", SK, [
         ("How many atoms belong to one FCC unit cell?", "4", "2", "1", "14"),
         ("How many atoms belong to one BCC unit cell?", "2", "4", "9", "1"),
         ("What is the coordination number in FCC?", "12", "8", "6", "4"),
         ("What is the coordination number in BCC?", "8", "12", "6", "2"),
         ("Which two metal structures are both close-packed?", "FCC and HCP", "BCC and FCC", "BCC and HCP", "Simple cubic and BCC"),
         ("FCC and HCP differ only in", "the stacking of close-packed planes: ABCABC against ABAB", "their packing fraction", "their coordination number", "the radius of the atoms")],
         "Count shared atoms: corners one-eighth, faces one-half, the body centre whole"),
       N("mse-cell-count", SK, "A cubic unit cell has atoms on {{kc}} corners, {{kf}} face centres and {{kb}} body-centre sites. How many atoms belong to the cell?", "kc/8 + kf/2 + kb",
         "(kc + 4*kf + 8*kb)/Rational(8)", "Each corner counts one-eighth, each face one-half, a body site one", tex="n",
         cases=C("kc kf kb", [(8, 0, 1), (8, 6, 0), (8, 0, 0), (8, 2, 0), (8, 6, 1)]))]),
     ("B", X("A3.1"), "Relate the cell edge to the atomic radius in FCC and BCC.",
      "Atoms touch along the face diagonal in FCC, so a√2 = 4r; along the body diagonal in BCC, so a√3 = 4r.", "P1", [
       N("mse-edge-from-radius", SK, "{{kn}} is {{ks}} with atomic radius {{kr}} nm. Find the cell edge a in nm.", "4*kr/sqrt(kd)",
         f"Max(*solve(Eq(kd*{M}**2, (4*kr)**2), {M}))", "Four radii span the diagonal along which the atoms touch: the face diagonal in FCC, the body diagonal in BCC", tex="a",
         cases=C("kn ks kd kr", [("Copper", "FCC", 2, 0.1278), ("Iron at room temperature", "BCC", 3, 0.1241), ("Aluminium", "FCC", 2, 0.1431), ("Tungsten", "BCC", 3, 0.1371), ("Nickel", "FCC", 2, 0.1246)])),
       N("mse-radius-from-edge", SK, "{{kn}} is {{ks}} with cell edge a = {{ka}} nm. Find the atomic radius in nm.", "ka*sqrt(kd)/4",
         f"solve(Eq(4*{M}, ka*sqrt(kd)), {M})[0]", "The touching diagonal (a√2 in FCC, a√3 in BCC) is four radii long", tex="r",
         cases=C("kn ks kd ka", [("Silver", "FCC", 2, 0.4086), ("Chromium", "BCC", 3, 0.2885), ("Gold", "FCC", 2, 0.4078), ("Molybdenum", "BCC", 3, 0.3147), ("Lead", "FCC", 2, 0.4950)]))]),
     ("C", X("A3.1"), "Compute an atomic packing factor.",
      "APF is the volume of the atoms in the cell over the cell volume: 0.74 for FCC and HCP, 0.68 for BCC, 0.52 for simple cubic.", "P1", [
       N("mse-apf", SK, "A cubic cell of edge {{ka}} nm holds {{kn}} atoms of radius {{kr}} nm. Find the atomic packing factor.", "kn*(4/3)*pi*kr^3/ka^3",
         "kn*integrate(4*pi*Y**2, (Y, 0, kr))/ka**3", "Sphere volume times the atoms per cell, over a³", tex="APF",
         cases=C("ka kn kr", [(0.3615, 4, 0.1278), (0.2866, 2, 0.1241), (0.4050, 4, 0.1431), (0.3165, 2, 0.1371), (0.3340, 1, 0.1670)])),
       F("mse-apf-facts", SK, [
         ("What is the packing factor of FCC?", "0.74", "0.68", "0.52", "0.34"),
         ("What is the packing factor of BCC?", "0.68", "0.74", "0.52", "0.91"),
         ("What is the packing factor of simple cubic?", "0.52", "0.68", "0.74", "0.34"),
         ("Iron changes from BCC to FCC at 912 °C on heating. Its volume", "shrinks slightly, because FCC packs more tightly", "grows, because FCC has more atoms per cell", "does not change", "doubles")],
         "0.74 is the densest packing of equal spheres; BCC leaves more open space"),
       ]),
     ("D", X("A3.1") + E_("9A"), "Compute a theoretical density from the unit cell.",
      "ρ = nA ÷ (V_cell N_A): atoms per cell times molar mass, over cell volume times Avogadro's number. With a in nm, a³ in cm³ is (a × 10⁻⁷)³.", "P1", [
       N("mse-density", SK, "{{kn}} has {{kc}} atoms per cubic cell, molar mass {{km}} g/mol and cell edge {{ka}} nm. Find its density in g/cm³.", f"kc*km/((ka*1e-7)^3*{NA})",
         f"solve(Eq({M}*(ka*Rational('1e-7'))**3*{NAS}, kc*km), {M})[0]", "Mass in one cell is n A ÷ N_A; divide by a³ in cm³", tex="\\rho",
         cases=C("kn kc km ka", [("Copper", 4, 63.55, 0.3615), ("Iron", 2, 55.85, 0.2866), ("Aluminium", 4, 26.98, 0.4050), ("Tungsten", 2, 183.84, 0.3165), ("Nickel", 4, 58.69, 0.3524)])),
       N("mse-molar-mass-from-cell", SK, "A metal has density {{kd}} g/cm³, a cubic cell of edge {{ka}} nm and {{kc}} atoms per cell. Find its molar mass in g/mol.", f"kd*(ka*1e-7)^3*{NA}/kc",
         f"solve(Eq(kd*(ka*Rational('1e-7'))**3*{NAS}, kc*{M}), {M})[0]", "Run the density formula backward: A = ρ a³ N_A ÷ n", tex="A",
         cases=C("kd ka kc", [(8.94, 0.3615, 4), (7.87, 0.2866, 2), (19.3, 0.3165, 2), (2.70, 0.4050, 4), (21.45, 0.3924, 4)]))])]),
   2: ("Directions, planes and diffraction", [
     ("A", X("A3.1"), "Write the Miller indices of a plane from its intercepts and test whether a direction lies in a plane.",
      "Take the intercepts in units of the cell edges, invert, and clear fractions; a plane parallel to an axis has index 0 for it. In a cubic crystal [uvw] lies in (hkl) when hu + kv + lw = 0.", "P2", [
       F("mse-miller-plane", SK, [
         ("A plane cuts the x and y axes at one cell edge each and is parallel to z. Its Miller indices are", "(110)", "(111)", "(100)", "(001)"),
         ("A plane cuts the axes at a/2, b and c. Its Miller indices are", "(211)", "(122)", "(112)", "(121)"),
         ("A plane cuts the x axis at a and is parallel to y and z. Its Miller indices are", "(100)", "(011)", "(111)", "(010)"),
         ("A plane cuts all three axes at one cell edge. Its Miller indices are", "(111)", "(100)", "(110)", "(011)"),
         ("A plane cuts the axes at a/3, b/2 and c. Its Miller indices are", "(321)", "(123)", "(231)", "(632)"),
         ("A plane cuts the axes at a, b and c/2. Its Miller indices are", "(112)", "(221)", "(110)", "(211)")],
         "Intercepts, then reciprocals, then clear fractions"),
       L("mse-direction-in-plane", SK, "In a cubic crystal, does the direction lie in the plane? {{q}}", ["Yes: hu + kv + lw = 0", "No: hu + kv + lw is not 0"], [
         ("[1 -1 0] and (111)", 0), ("[110] and (111)", 1), ("[0 1 -1] and (111)", 0), ("[111] and (110)", 1), ("[1 -1 1] and (110)", 0), ("[001] and (110)", 0), ("[100] and (110)", 1)],
         "A direction lies in a plane when it is perpendicular to the plane's normal, and in cubic crystals the normal to (hkl) is [hkl]")]),
     ("B", X("A3.1"), "Write a direction's indices and find the angle between two directions.",
      "A direction is the vector between two lattice points reduced to smallest integers. In a cubic crystal the angle between [u₁v₁w₁] and [u₂v₂w₂] comes from the dot product.", "P1", [
       N("mse-direction-angle", SK, "In a cubic crystal, find the angle in degrees between [{{ka}}{{kb}}{{kc}}] and [{{kd}}{{kf}}{{kg}}].", "acos((ka*kd + kb*kf + kc*kg)/(sqrt(ka^2 + kb^2 + kc^2)*sqrt(kd^2 + kf^2 + kg^2)))*180/pi",
         "atan2(sqrt((kb*kg - kc*kf)**2 + (kc*kd - ka*kg)**2 + (ka*kf - kb*kd)**2), ka*kd + kb*kf + kc*kg)*180/pi", "cos θ is the dot product over the product of the lengths", tex="\\theta",
         cases=C("ka kb kc kd kf kg", [(1, 0, 0, 1, 1, 0), (1, 1, 1, 1, 0, 0), (1, 1, 0, 1, 1, 1), (1, 1, 0, 1, 0, 1), (1, 0, 0, 0, 1, 0), (1, 1, 1, 1, 1, 0)])),
       F("mse-direction-indices", SK, [
         ("The direction from the origin to the point (1, 1/2, 0) in cell-edge units is", "[210]", "[120]", "[110]", "[1 1/2 0]"),
         ("The body diagonal of a cubic cell is the direction", "[111]", "[110]", "[100]", "[112]"),
         ("A face diagonal of a cubic cell is a direction of the type", "[110]", "[111]", "[100]", "[210]"),
         ("The direction from (1, 0, 0) to (0, 1, 0) is", "[-1 1 0]", "[110]", "[011]", "[100]"),
         ("The direction from the origin to (1/3, 2/3, 1) is", "[123]", "[321]", "[213]", "[136]")],
         "Head minus tail, then multiply through to the smallest whole numbers"),
       ]),
     ("C", X("A3.1", "A3.2"), "Compute the spacing of (hkl) planes in a cubic crystal.",
      "d = a ÷ √(h² + k² + l²). Low-index planes are the most widely spaced and the most densely packed.", "P1", [
       N("mse-d-spacing", SK, "A cubic crystal has a = {{ka}} nm. Find the spacing of its ({{kh}}{{kk}}{{kl}}) planes in nm.", "ka/sqrt(kh^2 + kk^2 + kl^2)",
         f"Max(*solve(Eq({M}**2*(kh**2 + kk**2 + kl**2), ka**2), {M}))", "Divide the cell edge by the length of the index vector", tex="d",
         cases=C("ka kh kk kl", [(0.3615, 1, 1, 1), (0.2866, 1, 1, 0), (0.4050, 2, 0, 0), (0.3165, 2, 1, 1), (0.3524, 2, 2, 0)])),
       N("mse-edge-from-spacing", SK, "The ({{kh}}{{kk}}{{kl}}) planes of a cubic crystal are {{kd}} nm apart. Find the cell edge a in nm.", "kd*sqrt(kh^2 + kk^2 + kl^2)",
         f"Max(*solve(Eq({M}**2, kd**2*(kh**2 + kk**2 + kl**2)), {M}))", "a = d √(h² + k² + l²)", tex="a",
         cases=C("kd kh kk kl", [(0.2087, 1, 1, 1), (0.2027, 1, 1, 0), (0.2025, 2, 0, 0), (0.1292, 2, 1, 1), (0.1246, 2, 2, 0)]))]),
     ("D", X("A3.2"), "Use Bragg's law.",
      "nλ = 2d sin θ. A diffractometer reports 2θ, the angle between the incident and diffracted beams.", "P1", [
       N("mse-bragg-angle", SK, "X-rays of wavelength {{kw}} nm reflect in first order from planes {{kd}} nm apart. Find the diffraction angle 2θ in degrees.", "2*asin(kw/(2*kd))*180/pi",
         "2*atan2(kw/(2*kd), sqrt(1 - (kw/(2*kd))**2))*180/pi", "sin θ = λ ÷ 2d, then double θ", tex="2\\theta",
         cases=C("kw kd", [(0.1542, 0.2087), (0.1542, 0.2027), (0.1542, 0.1433), (0.0711, 0.2338), (0.1790, 0.1170)])),
       N("mse-bragg-spacing", SK, "A first-order peak appears at 2θ = {{kt}}° with X-rays of wavelength {{kw}} nm. Find the plane spacing in nm.", "kw/(2*sin(kt*pi/360))",
         f"solve(Eq(2*{M}*sin(kt*pi/360), kw), {M})[0]", "Halve 2θ first, then d = λ ÷ 2 sin θ", tex="d",
         cases=C("kt kw", [(43.3, 0.1542), (44.7, 0.1542), (65.0, 0.1542), (38.5, 0.1542), (17.5, 0.0711)]))]),
     ("E", X("A3.2"), "Decide which reflections a cubic structure allows.",
      "BCC reflects only when h + k + l is even; FCC only when h, k and l are all odd or all even; simple cubic reflects for every plane.", "P2", [
       L("mse-reflection-allowed", SK, "Does this reflection appear in the diffraction pattern? {{q}}", ["Present", "Absent"], [
         ("BCC, (110)", 0), ("BCC, (100)", 1), ("FCC, (111)", 0), ("FCC, (110)", 1), ("BCC, (211)", 0), ("FCC, (200)", 0), ("BCC, (111)", 1), ("FCC, (210)", 1), ("FCC, (220)", 0)],
         "BCC needs an even index sum; FCC needs unmixed indices"),
       F("mse-first-peaks", SK, [
         ("A cubic metal's first three peaks index as (110), (200), (211). The structure is", "BCC", "FCC", "Simple cubic", "HCP"),
         ("A cubic metal's first three peaks index as (111), (200), (220). The structure is", "FCC", "BCC", "Simple cubic", "Diamond cubic only"),
         ("A cubic crystal's first three peaks index as (100), (110), (111). The structure is", "Simple cubic", "BCC", "FCC", "It cannot be cubic"),
         ("The first peak of an FCC metal comes from the planes", "(111)", "(100)", "(110)", "(200)"),
         ("The first peak of a BCC metal comes from the planes", "(110)", "(100)", "(111)", "(200)")],
         "Read the sequence of allowed planes: mixed indices rule out FCC, odd sums rule out BCC")]),
     ("F", X("A3.1"), "Compute a linear and a planar density.",
      "Linear density is atom centres per length along a direction; planar density is atoms per area on a plane. Slip prefers the densest directions on the densest planes.", "P1", [
       N("mse-linear-density", SK, "An FCC metal has atomic radius {{kr}} nm. Find the linear density along [110] in atoms per nm.", "1/(2*kr)",
         "2/(sqrt(2)*(2*sqrt(2)*kr))", "The face diagonal is 4r long and holds two atoms: half at each corner and one at the centre", tex="LD",
         cases=C("kr", [(0.1278,), (0.1431,), (0.1246,), (0.1445,), (0.1750,)])),
       N("mse-planar-density", SK, "An FCC metal has atomic radius {{kr}} nm. Find the planar density of (111) in atoms per nm².", "1/(2*sqrt(3)*kr^2)",
         "2/(sqrt(3)/4*(4*kr)**2)", "The (111) triangle inside the cell has sides 4r and holds two atoms: three corner sixths and three edge halves", tex="PD",
         cases=C("kr", [(0.1278,), (0.1431,), (0.1246,), (0.1445,), (0.1750,)]))])])})

U2 = ("defects", "Defects and dislocations", X("A4.1", "A4.2", "B6.2"), ["DEFECT"], {
   1: ("Point defects and solid solutions", [
     ("A", X("A4.1", "A5.4"), "Compute an equilibrium vacancy concentration.",
      "N_v ÷ N = exp(−Q_v ÷ kT), with k = 8.617 × 10⁻⁵ eV/K. Near melting about one site in ten thousand is vacant.", "P1", [
       N("mse-vacancy-fraction", DF, "A metal has a vacancy formation energy of {{kq}} eV. How many vacancies are there per million lattice sites at {{kt}} K? (k = 8.617333 × 10⁻⁵ eV/K)", f"1e6*exp(-kq/({KB}*kt))",
         f"10**6/exp(kq/({KBS}*kt))", "The Boltzmann factor gives the fraction of vacant sites; scale to a million", tex="N_v",
         cases=C("kq kt", [(0.90, 1273), (1.00, 1000), (0.75, 900), (1.10, 1300), (0.90, 1356)])),
       N("mse-vacancy-energy", DF, "At {{kt}} K a fraction {{kf}} of a metal's lattice sites is vacant. Find the vacancy formation energy in eV. (k = 8.617333 × 10⁻⁵ eV/K)", f"-{KB}*kt*log(kf)",
         f"{KBS}*kt*log(1/kf)", "Take the logarithm of the fraction: Q = −kT ln(N_v ÷ N)", tex="Q_v",
         cases=C("kt kf", [(1273, 0.00027), (1000, 0.00001), (1356, 0.00045), (900, 0.00006), (1200, 0.0001)]))]),
     ("B", X("A4.2"), "Tell substitutional from interstitial solid solutions and apply the size rule.",
      "A solute sits on host sites when its radius is within about 15% of the host's and the structures, valences and electronegativities are alike; a much smaller atom (C, N, H) sits between host atoms.", "P2", [
       F("mse-solution-type", DF, [
         ("Carbon dissolved in iron is", "an interstitial solute", "a substitutional solute", "a vacancy", "a second phase by definition"),
         ("Nickel dissolved in copper is", "a substitutional solute, soluble in all proportions", "an interstitial solute", "insoluble", "a Frenkel defect"),
         ("Zinc in copper (brass) is", "a substitutional solute with limited solubility", "an interstitial solute", "a Schottky defect", "soluble in all proportions"),
         ("Hydrogen in palladium is", "an interstitial solute", "a substitutional solute", "a dislocation", "a grain boundary phase"),
         ("Copper and nickel dissolve completely in each other because", "both are FCC with radii, valence and electronegativity close together", "nickel is much smaller than copper", "they form an intermetallic compound", "one is BCC and one is FCC")],
         "Small atoms go between host atoms; similar atoms replace them"),
       N("mse-size-mismatch", DF, "A solute atom has radius {{ka}} nm and the host {{kb}} nm. Find the size difference as a percentage of the host radius (substitution needs under about 15%).", "abs(ka - kb)/kb*100",
         "sqrt((ka - kb)**2)/kb*100", "Radius difference over the host radius", tex="\\%",
         cases=C("ka kb", [(0.1246, 0.1278), (0.1332, 0.1278), (0.1750, 0.1278), (0.1431, 0.1278), (0.0710, 0.1241)]))]),
     ("C", X("A4.2") + E_("9A"), "Convert a composition between weight percent and atom percent.",
      "Divide each weight percent by its molar mass to get moles, then normalise; multiply atom percents by molar mass and normalise to go back.", "P1", [
       N("mse-wt-to-at", DF, "An alloy is {{kw}} wt% of element 1 (molar mass {{ka}} g/mol), the rest element 2 ({{kb}} g/mol). Find the atom percent of element 1.", "(kw/ka)/(kw/ka + (100 - kw)/kb)*100",
         f"solve(Eq({M}*(kw/ka + (100 - kw)/kb), 100*kw/ka), {M})[0]", "Moles of each from 100 g of alloy, then the mole fraction", tex="at\\%",
         cases=C("kw ka kb", [(30, 65.38, 63.55), (0.76, 12.011, 55.85), (4, 63.55, 26.98), (10, 118.71, 63.55), (6, 26.98, 47.87)])),
       N("mse-at-to-wt", DF, "An alloy is {{kw}} at% of element 1 (molar mass {{ka}} g/mol), the rest element 2 ({{kb}} g/mol). Find the weight percent of element 1.", "kw*ka/(kw*ka + (100 - kw)*kb)*100",
         f"solve(Eq({M}*(kw*ka + (100 - kw)*kb), 100*kw*ka), {M})[0]", "Mass of each from 100 mol of alloy, then the mass fraction", tex="wt\\%",
         cases=C("kw ka kb", [(25, 26.98, 58.69), (50, 47.87, 26.98), (3.5, 12.011, 55.85), (10, 65.38, 63.55), (33.3, 63.55, 26.98)]))]),
     ("D", X("B6.2"), "Identify Schottky and Frenkel defects and the vacancies a dopant forces in an ionic crystal.",
      "A Schottky defect is a cation vacancy with an anion vacancy; a Frenkel defect is a cation moved to an interstitial site. Both keep the crystal neutral, and an impurity of different charge brings compensating vacancies.", "P2", [
       F("mse-ionic-defects", DF, [
         ("A missing Na⁺ paired with a missing Cl⁻ in NaCl is", "a Schottky defect", "a Frenkel defect", "an edge dislocation", "a substitutional impurity"),
         ("A silver ion moved from its site into an interstice in AgCl is", "a Frenkel defect", "a Schottky defect", "a twin", "a colour centre only"),
         ("Why do point defects in ionic crystals come in pairs or sets?", "The crystal must stay electrically neutral", "Vacancies attract each other elastically", "Single vacancies cannot diffuse", "The lattice must stay cubic"),
         ("Which defect leaves the density of the crystal unchanged?", "Frenkel: the ion is still in the crystal", "Schottky: two ions leave", "Both lower it equally", "Neither can form without melting")],
         "Schottky removes a neutral set of ions; Frenkel only relocates one"),
       L("mse-dopant-vacancy", DF, "What keeps the crystal neutral? {{q}}", ["One cation vacancy per impurity ion", "One cation vacancy per two impurity ions", "One anion vacancy per two impurity ions"], [
         ("Ca²⁺ replaces Na⁺ in NaCl", 0), ("Fe³⁺ replaces Fe²⁺ in FeO", 1), ("Al³⁺ replaces Mg²⁺ in MgO", 1), ("Mg²⁺ replaces Li⁺ in LiF", 0), ("Y³⁺ replaces Zr⁴⁺ in ZrO₂", 2), ("Sc³⁺ replaces Zr⁴⁺ in ZrO₂", 2)],
         "Balance the extra or missing charge: each extra positive charge needs cation vacancies worth the same charge, each missing one needs anion vacancies")])]),
   2: ("Dislocations and the Burgers vector", [
     ("A", X("A4.1"), "Tell edge, screw and mixed dislocations apart by the Burgers vector and the line.",
      "The Burgers vector b is the lattice displacement a dislocation carries. Edge: b perpendicular to the line (an extra half-plane). Screw: b parallel to the line (a spiral ramp). Anything between is mixed.", "P2", [
       F("mse-dislocation-facts", DF, [
         ("In an edge dislocation the Burgers vector is", "perpendicular to the dislocation line", "parallel to the dislocation line", "at 45 degrees to the line", "zero"),
         ("In a screw dislocation the Burgers vector is", "parallel to the dislocation line", "perpendicular to the dislocation line", "perpendicular to the slip plane", "zero"),
         ("An extra half-plane of atoms ending inside the crystal is", "an edge dislocation", "a screw dislocation", "a stacking fault", "a twin boundary"),
         ("Why can a screw dislocation cross-slip onto another plane while an edge cannot?", "Its Burgers vector is parallel to its line, so the two do not fix a single slip plane", "It has no strain field", "It moves by diffusion", "Its Burgers vector is larger"),
         ("Along a curved dislocation line, the Burgers vector", "stays the same everywhere, while the edge or screw character changes", "rotates to stay perpendicular to the line", "rotates to stay parallel to the line", "falls to zero at the bends"),
         ("An edge dislocation glides in the direction", "of its Burgers vector, perpendicular to its line", "of its line", "normal to the slip plane", "opposite to the applied shear only")],
         "One vector, fixed along the whole line; the angle it makes with the line names the character"),
       L("mse-dislocation-character", DF, "The Burgers vector makes this angle with the dislocation line. What is the character? {{q}}", ["Edge", "Screw", "Mixed"], [
         ("90°", 0), ("0°", 1), ("35°", 2), ("60°", 2), ("180°", 1), ("90°, and the line then turns until the angle is 0°: name the first segment", 0)],
         "Perpendicular is edge, parallel or antiparallel is screw, anything else is mixed")]),
     ("B", X("A4.1"), "Find a Burgers vector from a Burgers circuit.",
      "Walk a closed loop of lattice steps around the line, equal steps in opposite directions. In perfect crystal the loop closes; around a dislocation it does not, and the vector needed to close it is b.", "P1", [
       N("mse-burgers-circuit", DF, "In a simple cubic crystal with lattice parameter {{ka}} nm, a circuit around a dislocation line goes {{kr}} atom steps right, {{ku}} up, {{kw}} left and {{ku}} down, and ends at an atom that is not its starting atom. Find the magnitude of the net Burgers vector it encloses, in nm.", "abs(kr - kw)*ka",
         "sqrt(((kr - kw)*ka)**2 + ((ku - ku)*ka)**2)", "The up and down steps cancel; the right and left steps differ by the closure failure", tex="b",
         cases=C("ka kr ku kw", [(0.30, 5, 4, 4), (0.25, 6, 5, 5), (0.40, 4, 3, 5), (0.286, 7, 6, 5), (0.36, 3, 3, 4)])),
       F("mse-burgers-circuit-facts", DF, [
         ("A sequence of lattice steps closes in perfect crystal. Taken around a dislocation, the same sequence", "fails to close, and the closing vector is the Burgers vector", "closes, but only after twice as many steps", "closes exactly as before", "cannot be drawn"),
         ("A Burgers circuit that encloses no dislocation", "closes exactly", "fails to close by one lattice spacing", "fails to close by the grain size", "closes only in FCC"),
         ("A circuit encloses two edge dislocations of opposite sign. The closure failure is", "zero: the two Burgers vectors cancel", "twice one Burgers vector", "one Burgers vector", "undefined"),
         ("Around an edge dislocation the closure failure points", "perpendicular to the line, in the slip plane", "along the line", "normal to the slip plane", "in a random direction"),
         ("Around a screw dislocation the circuit", "ends one lattice step along the line from where it began, like one turn of a spiral ramp", "closes exactly", "ends one step perpendicular to the line", "cannot be completed"),
         ("If the circuit is made larger but still encloses the same single dislocation, the closure failure", "does not change", "grows with the circuit", "shrinks with the circuit", "changes sign")],
         "The closure failure counts the dislocation content inside the loop and nothing else")]),
     ("C", X("A4.1"), "Compute the magnitude of a Burgers vector from its indices.",
      "A perfect dislocation's b joins nearest neighbours: (a/2)⟨110⟩ in FCC, (a/2)⟨111⟩ in BCC. Its length is (a/2)√(h² + k² + l²), which equals two atomic radii.", "P1", [
       N("mse-burgers-magnitude", DF, "{{kn}} is {{ks}} with a = {{ka}} nm, and its slip dislocations have b = (a/2)[{{kh}}{{kk}}{{kl}}]. Find the magnitude of b in nm.", "ka/2*sqrt(kh^2 + kk^2 + kl^2)",
         f"Max(*solve(Eq(4*{M}**2, ka**2*(kh**2 + kk**2 + kl**2)), {M}))", "Length of the index vector times a/2", tex="b",
         cases=C("kn ks ka kh kk kl", [("Copper", "FCC", 0.3615, 1, 1, 0), ("Iron", "BCC", 0.2866, 1, 1, 1), ("Aluminium", "FCC", 0.4050, 1, 1, 0), ("Tungsten", "BCC", 0.3165, 1, 1, 1), ("Nickel", "FCC", 0.3524, 1, 0, 1)])),
       N("mse-burgers-from-radius", DF, "{{kn}} is {{ks}} with atomic radius {{kr}} nm. Its Burgers vector joins nearest neighbours. Find the magnitude of b in nm.", "2*kr",
         "(4*kr/sqrt(kd))/2*sqrt(kd)", "Nearest neighbours touch, so the shortest lattice vector is one atomic diameter", tex="b",
         cases=C("kn ks kd kr", [("Silver", "FCC", 2, 0.1445), ("Chromium", "BCC", 3, 0.1249), ("Gold", "FCC", 2, 0.1442), ("Molybdenum", "BCC", 3, 0.1363), ("Lead", "FCC", 2, 0.1750)]))]),
     ("D", X("A4.1", "A4.2"), "Use the b² rule for a dislocation's energy and for dislocation reactions.",
      "The elastic energy per length of a dislocation is about ½Gb². A reaction b₁ → b₂ + b₃ is favourable when b₁² > b₂² + b₃² (Frank's rule), which is why dislocations take the shortest lattice vector.", "P1", [
       N("mse-dislocation-energy", DF, "A metal has shear modulus {{kg}} GPa and Burgers vector {{kb}} nm. Estimate the energy per unit length of a dislocation as ½Gb², in nJ/m.", "0.5*kg*kb^2",
         "integrate(kg*Y, (Y, 0, kb))", "GPa × nm² is nJ/m, so the units fall out directly", tex="E",
         cases=C("kg kb", [(45, 0.2556), (82, 0.2482), (26, 0.2864), (160, 0.2741), (76, 0.2492)])),
       L("mse-frank-rule", DF, "By Frank's b² rule, is the reaction favourable? {{q}}", ["Favourable: the energy falls", "Unfavourable: the energy rises"], [
         ("FCC: (a/2)[110] → (a/6)[211] + (a/6)[1 2 -1], so a²/2 → a²/6 + a²/6", 0),
         ("BCC: a[100] → (a/2)[111] + (a/2)[1 -1 -1], so a² → 3a²/4 + 3a²/4", 1),
         ("BCC: (a/2)[111] + (a/2)[1 -1 -1] → a[100], so 3a²/4 + 3a²/4 → a²", 0),
         ("A dislocation of Burgers vector 2b splits into two of b, so 4b² → b² + b²", 0),
         ("Two dislocations of b on the same plane merge into one of 2b, so b² + b² → 4b²", 1)],
         "Compare the sum of b² before and after")]),
     ("E", X("A4.1"), "Work with a dislocation density.",
      "Density ρ is line length per volume, in m⁻²: about 10¹⁰ in an annealed metal, 10¹⁴ to 10¹⁶ after heavy cold work. The mean spacing between dislocations is about 1 ÷ √ρ.", "P1", [
       N("mse-dislocation-spacing", DF, "A metal has a dislocation density of {{kp}} × 10^{{kq}} m⁻². Estimate the mean spacing between dislocations in nm.", "1e9/sqrt(kp*10^kq)",
         f"Max(*solve(Eq({M}**2*kp*10**kq, 10**18), {M}))", "Spacing is one over the square root of the density; convert metres to nm", tex="l",
         cases=C("kp kq", [(1, 14), (1, 10), (4, 12), (2.5, 15), (1, 16)])),
       N("mse-dislocation-length", DF, "A metal has a dislocation density of {{kp}} × 10^{{kq}} m⁻². What total length of dislocation line, in km, is in one cubic centimetre?", "kp*10^kq*1e-9",
         "kp*10**kq/Rational(10**6)/1000", "Density times volume: 1 cm³ is 10⁻⁶ m³; then metres to km", tex="L",
         cases=C("kp kq", [(1, 10), (5, 12), (1, 14), (2, 15), (3, 11)]))])]),
   3: ("Grain boundaries and planar defects", [
     ("A", X("A3.3", "A4.2"), "Convert between ASTM grain size number and grain count.",
      "N = 2^(G − 1): N grains per square inch at 100× magnification for ASTM grain size number G. A larger G means finer grains.", "P1", [
       N("mse-astm-grains", DF, "A steel has ASTM grain size number {{kg}}. How many grains per square inch are seen at 100×?", "2^(kg - 1)",
         "exp((kg - 1)*log(2))", "Double the count for every step in G", tex="N",
         cases=C("kg", [(6,), (8,), (4,), (10,), (7,)])),
       N("mse-astm-number", DF, "A micrograph at 100× shows {{kn}} grains per square inch. Find the ASTM grain size number.", "1 + log(kn)/log(2)",
         "1 + log(kn, 2)", "Take the base-2 logarithm and add one", tex="G",
         cases=C("kn", [(32,), (128,), (8,), (512,), (45,)]))]),
     ("B", X("A4.2"), "Identify low-angle boundaries, twins and stacking faults.",
      "A low-angle tilt boundary is a wall of edge dislocations of spacing D with misorientation θ ≈ b ÷ D. A twin boundary is a mirror plane; a stacking fault is a mistake in the ABCABC sequence.", "P1", [
       N("mse-tilt-angle", DF, "A tilt boundary is a wall of edge dislocations with b = {{kb}} nm spaced {{kd}} nm apart. Find the misorientation in degrees, from tan(θ/2) = b ÷ 2D.", "2*atan(kb/(2*kd))*180/pi",
         "2*atan2(kb/2, kd)*180/pi", "For small angles this is b ÷ D in radians", tex="\\theta",
         cases=C("kb kd", [(0.2556, 15), (0.2482, 5), (0.2864, 30), (0.2556, 3), (0.2741, 10)])),
       F("mse-planar-defects", DF, [
         ("A boundary across which the lattice is a mirror image of itself is", "a twin boundary", "a stacking fault", "a low-angle tilt boundary", "an antiphase boundary only"),
         ("An FCC stacking sequence ABCABABC contains", "a stacking fault", "a twin boundary", "a screw dislocation", "a vacancy cluster"),
         ("A low-angle tilt boundary is built from", "a wall of edge dislocations", "a grid of vacancies", "a single screw dislocation", "a layer of second phase"),
         ("A low-angle twist boundary is built from", "a grid of screw dislocations", "a wall of edge dislocations", "a stack of twins", "interstitial atoms"),
         ("Compared with a low-angle boundary, a high-angle grain boundary has", "higher energy and stops slip more effectively", "lower energy", "no effect on dislocations", "a Burgers vector of its own")],
         "Tilt walls are edge dislocations, twist grids are screws, twins are mirrors, faults are stacking mistakes")])])})

U3 = ("deformation", "Deformation and strengthening", X("A4.1", "A4.2") + E_("9A", "9B"), ["DEFECT"], {
   1: ("Slip", [
     ("A", X("A4.1"), "Name the slip systems of FCC, BCC and HCP metals.",
      "Slip runs on the most densely packed planes along the closest-packed directions: (111) planes and 110-type directions in FCC (12 systems), 111-type directions in BCC, the basal plane in HCP (3 systems).", "P2", [
       F("mse-slip-systems", DE, [
         ("FCC metals slip on", "the (111)-type planes along 110-type directions", "the (110)-type planes along 111-type directions", "the (100)-type planes along 100-type directions", "the basal plane only"),
         ("BCC metals slip along", "111-type directions, the body diagonals", "110-type directions", "100-type directions", "no fixed direction"),
         ("Why are HCP metals such as magnesium hard to form cold?", "Basal slip gives only three systems, too few for a general shape change", "They have no dislocations", "Their Burgers vector is too short", "They have no close-packed plane"),
         ("Why are FCC metals ductile even at low temperature?", "Twelve close-packed slip systems are always available", "They contain no grain boundaries", "Their bonds are weaker than in BCC metals", "They deform only by twinning"),
         ("Slip prefers close-packed planes because", "they are the most widely spaced, so the resistance to shear is lowest", "they have the highest surface energy", "they contain the most vacancies", "dislocations cannot exist on other planes")],
         "Densest plane, shortest lattice vector"),
       L("mse-slip-count", DE, "How many slip systems? {{q}}", ["3", "12", "48"], [
         ("FCC: four (111)-type planes, three 110-type directions in each", 1), ("HCP with basal slip only", 0), ("BCC counting the 110, 112 and 123 plane families", 2), ("BCC on the six 110-type planes alone, two 111-type directions in each", 1)],
         "Planes times directions per plane")]),
     ("B", X("A4.1"), "Apply Schmid's law.",
      "τ_R = σ cos φ cos λ, with φ between the load axis and the slip-plane normal and λ between the load axis and the slip direction. Slip starts when τ_R reaches the critical resolved shear stress; the factor cannot exceed 0.5.", "P1", [
       N("mse-schmid-stress", DE, "A single crystal is pulled with {{kg}} MPa. The slip-plane normal is {{kp}}° from the load axis and the slip direction {{kq}}°. Find the resolved shear stress in MPa.", "kg*cos(kp*pi/180)*cos(kq*pi/180)",
         "kg*sin((90 - kp)*pi/180)*sin((90 - kq)*pi/180)", "Resolve the force onto the slip direction and the area onto the slip plane", tex="\\tau_R",
         cases=C("kg kp kq", [(50, 45, 45), (45, 54.7, 35.3), (80, 60, 35), (12, 30, 65), (100, 40, 55)])),
       N("mse-schmid-yield", DE, "A crystal's critical resolved shear stress is {{kt}} MPa. The slip-plane normal is {{kp}}° from the load axis and the slip direction {{kq}}°. Find the tensile stress at which it yields, in MPa.", "kt/(cos(kp*pi/180)*cos(kq*pi/180))",
         f"solve(Eq({M}*cos(kp*pi/180)*cos(kq*pi/180), kt), {M})[0]", "Divide the critical stress by the Schmid factor", tex="\\sigma_y",
         cases=C("kt kp kq", [(0.5, 45, 45), (20.7, 54.7, 35.3), (6.2, 60, 35), (0.48, 43.1, 47.9), (30, 70, 25)]))]),
     ("C", X("A4.1"), "Compare theoretical and observed shear strength.",
      "Shearing a whole plane at once would take about G ÷ 2π. Real crystals yield at a thousandth of that because a dislocation moves the slip one row at a time.", "P1", [
       N("mse-theoretical-strength", DE, "A metal has shear modulus {{kg}} GPa. Estimate its theoretical shear strength, G ÷ 2π, in GPa.", "kg/(2*pi)",
         f"solve(Eq(2*pi*{M}, kg), {M})[0]", "About one sixth of the shear modulus", tex="\\tau_{th}",
         cases=C("kg", [(45,), (82,), (26,), (160,), (76,)])),
       F("mse-why-weak", DE, [
         ("Real metal crystals yield far below G ÷ 2π because", "dislocations move the slip one atomic row at a time", "their bonds are weaker than calculated", "they contain vacancies", "grain boundaries slide first"),
         ("Which solid comes closest to its theoretical strength?", "A dislocation-free whisker", "An annealed single crystal", "A cold-worked sheet", "A coarse-grained casting"),
         ("Every strengthening mechanism in a metal works by", "making dislocations harder to move", "removing all dislocations", "raising the elastic modulus", "increasing the density"),
         ("After heavy cold work a metal contains more dislocations and is", "stronger, because dislocations block one another", "weaker, because there are more carriers of slip", "unchanged in strength", "more ductile")],
         "Dislocations make slip easy; obstacles to dislocations make it hard again")])]),
   2: ("Strengthening mechanisms", [
     ("A", X("A4.2"), "Use the Hall-Petch relation.",
      "σ_y = σ₀ + k_y d^(−1/2): a grain boundary stops a dislocation, so finer grains give higher yield strength.", "P1", [
       N("mse-hall-petch", DE, "A steel has σ₀ = {{ko}} MPa and k_y = {{kk}} MPa·mm^½. Find its yield strength at a grain size of {{kd}} mm, in MPa.", "ko + kk/sqrt(kd)",
         "ko + kk*kd**Rational(-1, 2)", "Add the grain-boundary term k_y ÷ √d to the friction stress", tex="\\sigma_y",
         cases=C("ko kk kd", [(70, 23.4, 0.04), (25, 12.5, 0.01), (150, 20, 0.0025), (70, 23.4, 0.0064), (100, 15, 0.09)])),
       N("mse-hall-petch-constant", DE, "A metal yields at {{ka}} MPa with {{kd}} mm grains and at {{kb}} MPa with {{kf}} mm grains. Find k_y in MPa·mm^½.", "(ka - kb)/(1/sqrt(kd) - 1/sqrt(kf))",
         f"solve([Eq(ka, Symbol('s') + {M}/sqrt(kd)), Eq(kb, Symbol('s') + {M}/sqrt(kf))], [Symbol('s'), {M}])[{M}]", "Two points on a line of σ_y against d^(−1/2): the slope is k_y", tex="k_y",
         cases=C("ka kd kb kf", [(304, 0.01, 187, 0.04), (275, 0.0025, 150, 0.01), (230, 0.0064, 135, 0.04), (400, 0.0016, 250, 0.0064), (150, 0.04, 110, 0.16)]))]),
     ("B", X("A4.2"), "Compute percent cold work and the strength from dislocation density.",
      "%CW = (A₀ − A_d) ÷ A₀ × 100. Work hardening follows τ = αGb√ρ with α about 0.5: flow stress rises as the square root of dislocation density.", "P1", [
       N("mse-cold-work", DE, "A rod is drawn from {{ko}} mm to {{kd}} mm diameter. Find the percent cold work.", "(1 - (kd/ko)^2)*100",
         "(pi*ko**2/4 - pi*kd**2/4)/(pi*ko**2/4)*100", "Areas go as diameter squared", tex="\\%CW",
         cases=C("ko kd", [(10, 8), (15.2, 12.2), (6.4, 5.1), (20, 17), (12, 6)])),
       N("mse-taylor-hardening", DE, "A metal has G = {{kg}} GPa, b = {{kb}} nm and a dislocation density of {{kp}} × 10^{{kq}} m⁻². Estimate the shear flow stress τ = 0.5 G b √ρ in MPa.", "0.5*kg*kb*sqrt(kp*10^kq)/1e6",
         "kg*kb*sqrt(kp)*10**(kq/Rational(2))/(2*10**6)", "GPa × nm is Pa·m, and √ρ is per metre, so the product is in Pa", tex="\\tau",
         cases=C("kg kb kp kq", [(45, 0.2556, 1, 14), (82, 0.2482, 1, 15), (26, 0.2864, 4, 14), (45, 0.2556, 1, 12), (76, 0.2492, 2.5, 15)]))]),
     ("C", X("A4.2"), "Explain solid-solution and precipitation strengthening and use the Orowan stress.",
      "Solute atoms strain the lattice and drag on dislocations. Fine coherent precipitates are cut; larger ones are bypassed by bowing between them at τ = Gb ÷ L, so strength peaks at an intermediate ageing time and falls on overageing.", "P1", [
       N("mse-orowan", DE, "Particles in a metal with G = {{kg}} GPa and b = {{kb}} nm are spaced {{kw}} nm apart. Find the Orowan bypass stress Gb ÷ L in MPa.", "kg*1000*kb/kw",
         f"solve(Eq({M}*kw, 1000*kg*kb), {M})[0]", "Closer particles force a tighter bow and a higher stress", tex="\\tau",
         cases=C("kg kb kw", [(26, 0.2864, 50), (26, 0.2864, 200), (45, 0.2556, 100), (82, 0.2482, 80), (76, 0.2492, 30)])),
       F("mse-precipitation-facts", DE, [
         ("In precipitation hardening, strength peaks when the precipitates are", "fine, closely spaced and still coherent with the matrix", "as large as possible", "fully dissolved", "all at the grain boundaries"),
         ("Overageing lowers strength because", "the particles coarsen and spread apart, so dislocations bow between them easily", "the particles dissolve", "the grains shrink", "dislocations disappear"),
         ("The steps of a precipitation heat treatment, in order, are", "solution treat, quench, age", "age, quench, solution treat", "quench, solution treat, age", "anneal, cold work, quench"),
         ("A solute atom strengthens a metal mainly by", "its strain field interacting with dislocations", "raising the melting point", "adding slip systems", "lowering the density"),
         ("An alloy can be precipitation hardened only if", "the solubility of the solute falls as temperature falls", "it is a pure metal", "it has no solid solubility at any temperature", "it is BCC")],
         "Many small obstacles close together beat a few large ones far apart")]),
     ("D", X("A5.2") + E_("9G"), "Order recovery, recrystallization and grain growth.",
      "On annealing a cold-worked metal: recovery rearranges dislocations and relieves stress with little change in strength; recrystallization replaces the worked grains with new strain-free ones and restores ductility; grain growth then coarsens them.", "P2", [
       L("mse-anneal-stage", DE, "Which annealing stage? {{q}}", ["Recovery", "Recrystallization", "Grain growth"], [
         ("Internal stress falls and conductivity returns, but hardness barely changes", 0), ("New strain-free grains nucleate and hardness drops sharply", 1), ("Average grain diameter increases as boundary area shrinks", 2),
         ("Dislocations climb and line up into subgrain walls", 0), ("Ductility returns to its value before cold work", 1), ("Holding long after the new grains have formed lowers the yield strength further by Hall-Petch", 2)],
         "Stress relief first, new grains second, coarser grains last"),
       F("mse-recrystallization-facts", DE, [
         ("More prior cold work makes the recrystallization temperature", "lower, because more stored energy drives it", "higher", "unchanged", "equal to the melting point"),
         ("The recrystallization temperature of a pure metal is typically about", "0.3 to 0.5 of its absolute melting temperature", "0.9 of its melting temperature", "room temperature for every metal", "its boiling point"),
         ("Deforming a metal above its recrystallization temperature is called", "hot working", "cold working", "precipitation hardening", "quenching"),
         ("Lead and tin do not work harden at room temperature because", "room temperature is above their recrystallization temperature", "they have no dislocations", "they are amorphous", "they are HCP")],
         "Stored energy of cold work drives recrystallization")])]),
   3: ("The tensile test", [
     ("A", X("A4.1") + E_("9B"), "Read ductility and plastic strain from a tensile test.",
      "Percent elongation is (l_f − l₀) ÷ l₀ × 100. On unloading, the elastic strain σ ÷ E is recovered along a line parallel to the elastic slope, leaving the plastic strain.", "P1", [
       N("mse-elongation", DE, "A tensile bar with a {{ko}} mm gauge length measures {{kf}} mm after fracture. Find the percent elongation.", "(kf - ko)/ko*100",
         f"solve(Eq(ko*(1 + {M}/100), kf), {M})[0]", "Change in length over the original length", tex="\\%EL",
         cases=C("ko kf", [(50, 62), (50.8, 67.3), (25, 26.2), (200, 246), (50, 51.5)])),
       N("mse-plastic-strain", DE, "A metal with E = {{kg}} GPa is loaded to {{kt}} MPa, where the total strain is {{kp}}%, then unloaded. Find the permanent strain in percent.", "kp - kt/(kg*10)",
         f"solve(Eq(kp, {M} + 100*kt/(kg*1000)), {M})[0]", "Subtract the recovered elastic strain σ ÷ E from the total", tex="\\varepsilon_p",
         cases=C("kg kt kp", [(200, 400, 1.2), (70, 280, 2.0), (110, 550, 3.0), (200, 600, 0.8), (45, 180, 1.5)]))]),
     ("B", X("A4.1") + E_("9B"), "Convert engineering stress and strain to true stress and strain.",
      "σ_T = σ(1 + ε) and ε_T = ln(1 + ε) = ln(l ÷ l₀), valid up to necking. True strain adds up the increments dl ÷ l.", "P1", [
       N("mse-true-stress", DE, "At an engineering stress of {{kg}} MPa the engineering strain is {{kp}}. Find the true stress in MPa.", "kg*(1 + kp)",
         f"solve(Eq({M}/(1 + kp), kg), {M})[0]", "Constant volume: the area has shrunk by the factor 1 + ε", tex="\\sigma_T",
         cases=C("kg kp", [(300, 0.10), (450, 0.20), (520, 0.05), (250, 0.35), (700, 0.08)])),
       N("mse-true-strain", DE, "A bar is stretched uniformly from {{ko}} mm to {{kf}} mm. Find the true strain.", "log(kf/ko)",
         "integrate(1/Y, (Y, ko, kf))", "Integrate dl ÷ l from the start length to the final length", tex="\\varepsilon_T",
         cases=C("ko kf", [(50, 60), (50, 55), (100, 150), (25, 27), (200, 280)]))]),
     ("C", X("A4.1") + E_("9B"), "Use the strain-hardening law.",
      "In the plastic range σ_T = K ε_T^n. The exponent n runs from about 0.1 to 0.5, and necking begins when the true strain equals n.", "P1", [
       N("mse-hardening-stress", DE, "A metal follows σ = K εⁿ with K = {{kk}} MPa and n = {{kn}}. Find the true stress at a true strain of {{kt}}, in MPa.", "kk*kt^kn",
         "kk*exp(kn*log(kt))", "Raise the strain to the power n and scale by K", tex="\\sigma_T",
         cases=C("kk kn kt", [(530, 0.26, 0.10), (1275, 0.45, 0.20), (690, 0.16, 0.05), (315, 0.54, 0.30), (895, 0.49, 0.15)])),
       N("mse-hardening-exponent", DE, "True stress is {{ka}} MPa at a true strain of {{kc}} and {{kb}} MPa at {{kd}}. Find the strain-hardening exponent n.", "log(kb/ka)/log(kd/kc)",
         "(log(kb) - log(ka))/(log(kd) - log(kc))", "On a log-log plot the law is a straight line of slope n", tex="n",
         cases=C("ka kc kb kd", [(290, 0.10, 347, 0.20), (400, 0.05, 520, 0.20), (150, 0.02, 300, 0.20), (500, 0.10, 600, 0.30), (220, 0.04, 310, 0.16)]))]),
     ("D", X("A4.1") + E_("9A", "9B"), "Compute the modulus of resilience and tell it from toughness.",
      "Resilience is the elastic energy per volume up to yield, U_r = σ_y² ÷ 2E; toughness is the whole area under the stress-strain curve to fracture.", "P1", [
       N("mse-resilience", DE, "A metal has yield strength {{ky}} MPa and modulus {{kg}} GPa. Find its modulus of resilience in kJ/m³.", "ky^2/(2*kg)",
         "integrate(kg*1000*Y, (Y, 0, ky/(kg*1000)))*1000", "The area of the elastic triangle: half of stress times strain at yield", tex="U_r",
         cases=C("ky kg", [(350, 200), (275, 69), (900, 110), (1500, 207), (60, 45)])),
       F("mse-toughness-facts", DE, [
         ("Toughness in a tensile test is", "the area under the whole stress-strain curve to fracture", "the slope of the elastic region", "the stress at 0.2% offset", "the maximum stress"),
         ("A ceramic has high strength and low toughness because", "it fractures with almost no plastic strain, so the area under its curve is small", "its modulus is low", "it has many slip systems", "it necks early"),
         ("A spring material should have a high", "modulus of resilience: high yield strength relative to modulus", "ductility", "strain-hardening exponent", "percent elongation"),
         ("Yield strength is commonly read from the curve at", "a 0.2% strain offset line parallel to the elastic slope", "the highest point", "the fracture point", "half the tensile strength")],
         "Resilience is elastic energy; toughness needs both strength and ductility")]),
     ("E", E_("9A") + X("A4.1"), "Relate hardness to strength and name the hardness tests.",
      "Hardness is resistance to local plastic indentation. For steels, tensile strength in MPa is about 3.45 times the Brinell number.", "P1", [
       N("mse-hardness-strength", DE, "A steel has a Brinell hardness of {{kh}} HB. Estimate its tensile strength in MPa, using TS = 3.45 × HB.", "3.45*kh",
         f"solve(Eq({M}/Rational('3.45'), kh), {M})[0]", "The rule holds for most steels, not for other alloys", tex="TS",
         cases=C("kh", [(150,), (200,), (320,), (480,), (95,)])),
       F("mse-hardness-tests", DE, [
         ("Which test presses a hardened steel or carbide ball and measures the indent diameter?", "Brinell", "Vickers", "Rockwell C", "Mohs"),
         ("Which test uses a diamond pyramid and measures the indent diagonals?", "Vickers", "Brinell", "Charpy", "Jominy"),
         ("Which test reads hardness from the depth of penetration under a minor then a major load?", "Rockwell", "Brinell", "Knoop", "Mohs"),
         ("Which is a scratch scale rather than an indentation test?", "Mohs", "Vickers", "Rockwell B", "Brinell"),
         ("Which test suits a thin coating or a single grain?", "Knoop or Vickers microhardness", "Brinell", "Rockwell C", "Charpy impact")],
         "Ball and diameter, pyramid and diagonal, or depth under load")])])})

U4 = ("diffusion", "Diffusion in solids", X("A5.4"), ["DEFECT"], {
   1: ("Rates of diffusion", [
     ("A", X("A5.4"), "Apply Fick's first law to steady diffusion through a plate.",
      "J = −D dC/dx: flux runs down the concentration gradient. For a linear profile J = D ΔC ÷ Δx.", "P1", [
       N("mse-fick-flux", DI, "Carbon concentrations of {{ka}} and {{kb}} kg/m³ are held on the two faces of an iron plate {{kw}} mm thick, with D = {{kd}} × 10⁻¹¹ m²/s. Find the steady flux in units of 10⁻⁸ kg/(m²·s).", "kd*(ka - kb)/kw",
         "-kd*diff(ka + (kb - ka)*Y/kw, Y)", "Diffusivity times the concentration drop over the thickness; the powers of ten combine to 10⁻⁸", tex="J",
         cases=C("ka kb kw kd", [(1.2, 0.8, 5, 3.0), (2.0, 0.5, 1, 6.0), (0.9, 0.3, 2, 1.5), (4.0, 1.0, 10, 2.5), (1.5, 1.1, 0.5, 8.0)])),
       N("mse-fick-thickness", DI, "A steady flux of {{kj}} × 10⁻⁸ kg/(m²·s) passes through a membrane with D = {{kd}} × 10⁻¹¹ m²/s and concentrations {{ka}} and {{kb}} kg/m³ on its faces. Find its thickness in mm.", "kd*(ka - kb)/kj",
         f"solve(Eq(kj*{M}, kd*(ka - kb)), {M})[0]", "Rearrange J = D ΔC ÷ Δx for the thickness", tex="\\Delta x",
         cases=C("kj kd ka kb", [(0.24, 3.0, 1.2, 0.8), (9.0, 6.0, 2.0, 0.5), (0.45, 1.5, 0.9, 0.3), (2.0, 4.0, 3.0, 1.0), (1.6, 8.0, 1.5, 1.1)]))]),
     ("B", X("A5.4"), "Use the Arrhenius law for a diffusion coefficient.",
      "D = D₀ exp(−Q_d ÷ RT). A plot of ln D against 1 ÷ T is a line of slope −Q_d ÷ R.", "P1", [
       N("mse-diffusivity", DI, "For carbon in austenite D₀ = {{kp}} × 10⁻⁵ m²/s and Q_d = {{kq}} kJ/mol. Find D at {{kt}} K in units of 10⁻¹² m²/s. (R = 8.314 J/mol·K)", f"kp*1e7*exp(-kq*1000/({RG}*kt))",
         f"kp*10**7/exp(kq*1000/({RGS}*kt))", "The exponential is tiny, so keep the powers of ten apart: 10⁻⁵ over 10⁻¹² is 10⁷", tex="D",
         cases=C("kp kq kt", [(2.3, 148, 1173), (2.3, 148, 1273), (2.3, 148, 1073), (5.0, 284, 1673), (0.62, 80, 700)])),
       N("mse-diffusion-activation", DI, "A diffusion coefficient is {{ka}} × 10⁻¹⁵ m²/s at {{kc}} K and {{kb}} × 10⁻¹⁵ m²/s at {{kd}} K. Find the activation energy in kJ/mol. (R = 8.314 J/mol·K)", f"{RG}*log(kb/ka)/(1/kc - 1/kd)/1000",
         f"solve(Eq(log(kb/ka)*{RGS}, {M}*1000*(1/kc - 1/kd)), {M})[0]", "Two points fix the slope of ln D against 1 ÷ T", tex="Q_d",
         cases=C("ka kc kb kd", [(5.5, 900, 130, 1100), (1.0, 800, 40, 1000), (2.0, 1000, 26, 1200), (0.8, 700, 9.4, 800), (3.0, 1100, 50, 1400)]))]),
     ("C", X("A5.4"), "Scale a diffusion depth with time and temperature.",
      "For a fixed surface concentration, a given composition is reached at a depth proportional to √(Dt). The same profile results whenever the product Dt is the same.", "P1", [
       N("mse-diffusion-time", DI, "Carburizing reaches a case depth of {{ka}} mm in {{kt}} h. How many hours give {{kb}} mm at the same temperature?", "kt*(kb/ka)^2",
         f"solve(Eq(ka**2/kt, kb**2/{M}), {M})[0]", "Depth goes as √t, so time goes as depth squared", tex="t",
         cases=C("ka kt kb", [(0.5, 2, 1.0), (0.4, 3, 0.6), (1.0, 10, 0.5), (0.25, 1, 0.75), (0.8, 8, 1.2)])),
       N("mse-equal-dt", DI, "A treatment takes {{kt}} h at a temperature where D = {{ka}} × 10⁻¹¹ m²/s. How many hours give the same profile where D = {{kb}} × 10⁻¹¹ m²/s?", "kt*ka/kb",
         f"solve(Eq(ka*kt, kb*{M}), {M})[0]", "Keep D t constant", tex="t",
         cases=C("kt ka kb", [(10, 0.59, 1.94), (4, 2.4, 0.8), (20, 1.0, 5.3), (1.5, 6.0, 2.0), (8, 0.3, 1.2)]))]),
     ("D", X("A5.4"), "Compare diffusion mechanisms and paths.",
      "Interstitial atoms diffuse faster than substitutional ones, which must wait for a vacancy. Grain boundaries and surfaces are faster paths than the lattice; open structures and low melting points give faster diffusion.", "P2", [
       L("mse-diffusion-faster", DI, "Which diffuses faster at the same temperature? {{q}}", ["The first", "The second"], [
         ("Carbon in BCC iron, or nickel in BCC iron", 0), ("Copper atoms in the copper lattice, or copper atoms along a copper grain boundary", 1),
         ("Carbon in FCC iron, or carbon in BCC iron", 1), ("Hydrogen in steel, or chromium in steel", 0), ("Atoms across a free surface, or through the lattice", 0), ("Self-diffusion in tungsten at 800 K, or in lead at 500 K", 1)],
         "Small interstitials, open structures, defects and low melting points all speed diffusion"),
       F("mse-diffusion-mechanism", DI, [
         ("Substitutional atoms diffuse by", "exchanging places with a neighbouring vacancy", "squeezing between host atoms", "moving only along dislocations", "tunnelling"),
         ("The activation energy for vacancy diffusion includes", "the energy to form a vacancy and the energy to move an atom into it", "only the bond energy", "only the energy to move", "the heat of fusion"),
         ("Interstitial diffusion is faster mainly because", "the atoms are small and nearly every neighbouring interstitial site is empty", "the atoms are heavier", "it needs two vacancies", "it happens only at grain boundaries"),
         ("Grain-boundary diffusion matters most at", "low temperature and fine grain size", "the melting point", "coarse grain size", "zero stress")],
         "A substitutional jump needs a vacancy next door; an interstitial jump almost never waits")])])})

PBSN = "For lead-tin: α holds up to 18.3 wt% Sn, the eutectic is at 61.9 wt% Sn and β starts at 97.8 wt% Sn (183 °C)."
FEC = "Use ferrite 0.022, eutectoid 0.76 and cementite 6.70 wt% C."
U5 = ("phases", "Phase diagrams and transformations", X("A5.1", "A5.2", "A5.3", "A5.5", "A5.6", "A5.7") + E_("9C", "9G"), ["PATH"], {
   1: ("Binary phase diagrams", [
     ("A", X("A5.1") + E_("9G"), "Apply the Gibbs phase rule at constant pressure.",
      "F = C − P + 1 when pressure is fixed. In a binary system a two-phase field has one degree of freedom and a three-phase reaction (eutectic, eutectoid, peritectic) has none: it happens at one temperature.", "P1", [
       N("mse-phase-rule", PH, "At constant pressure a system of {{kc}} components has {{kp}} phases in equilibrium. How many degrees of freedom does it have?", "kc - kp + 1",
         f"solve(Eq({M} + kp, kc + 1), {M})[0]", "Components minus phases plus one", tex="F",
         cases=C("kc kp", [(2, 1), (2, 2), (3, 2), (3, 1), (1, 1), (3, 3)])),
       L("mse-phase-rule-meaning", PH, "In a binary alloy at constant pressure: {{q}}", ["Temperature and composition can both be chosen freely", "Fixing the temperature fixes the compositions of the phases", "It happens only at one temperature and one set of compositions"], [
         ("a single-phase solid solution", 0), ("liquid in equilibrium with one solid", 1), ("liquid transforming to two solids at the eutectic", 2), ("α and β coexisting below the eutectic", 1), ("austenite transforming to ferrite and cementite", 2)],
         "Two degrees of freedom, one, or none")]),
     ("B", X("A5.1") + E_("9G"), "Use the lever rule.",
      "In a two-phase field the phase compositions are the ends of the tie line, and the fraction of one phase is the opposite lever arm over the whole tie line.", "P1", [
       N("mse-lever-rule", PH, "An alloy of overall composition {{ko}} wt% B sits in a two-phase field where α holds {{ka}} wt% B and β holds {{kb}} wt% B. Find the weight percent of α.", "(kb - ko)/(kb - ka)*100",
         f"solve(Eq({M}/100*ka + (1 - {M}/100)*kb, ko), {M})[0]", "The arm on the far side of the overall composition, over the tie-line length", tex="W_\\alpha",
         cases=C("ko ka kb", [(40, 18.3, 97.8), (35, 31.5, 42.5), (60, 20, 90), (15, 10, 55), (70, 45, 82)])),
       N("mse-lever-composition", PH, "A two-phase alloy is {{kw}} wt% α. The α holds {{ka}} wt% B and the β holds {{kb}} wt% B. Find the overall composition in wt% B.", "kw/100*ka + (1 - kw/100)*kb",
         f"solve(Eq(({M} - kb)/(ka - kb)*100, kw), {M})[0]", "A mass balance on B over the two phases", tex="C_0",
         cases=C("kw ka kb", [(73, 18.3, 97.8), (68, 31.5, 42.5), (25, 20, 90), (50, 10, 55), (40, 45, 82)]))]),
     ("C", X("A5.1"), "Split a hypoeutectic alloy into primary phase and eutectic.",
      "Just above the eutectic temperature the liquid has the eutectic composition; all of it becomes eutectic microconstituent. The primary phase fraction is a lever between the solubility limit and the eutectic point.", "P1", [
       N("mse-primary-alpha", PH, f"A lead-tin alloy holds {{{{ko}}}} wt% Sn. Find the weight percent of primary α. {PBSN}", "(61.9 - ko)/(61.9 - 18.3)*100",
         f"100 - solve(Eq((1 - {M}/100)*Rational('18.3') + {M}/100*Rational('61.9'), ko), {M})[0]", "Lever between 18.3 and 61.9 just above the eutectic temperature; the rest is eutectic", tex="W_{\\alpha'}",
         cases=C("ko", [(40,), (30,), (50,), (25,), (55,)])),
       N("mse-eutectic-alpha", PH, f"A lead-tin alloy holds {{{{ko}}}} wt% Sn. Just below the eutectic temperature, find the weight percent of the alloy that is α inside the eutectic microconstituent. {PBSN}", "(97.8 - ko)/(97.8 - 18.3)*100 - (61.9 - ko)/(61.9 - 18.3)*100",
         "(ko - Rational('18.3'))/(Rational('61.9') - Rational('18.3'))*(Rational('97.8') - Rational('61.9'))/(Rational('97.8') - Rational('18.3'))*100", "Total α minus primary α; or the eutectic fraction times the α share of the eutectic", tex="W_{\\alpha,e}",
         cases=C("ko", [(40,), (30,), (50,), (25,), (55,)]))]),
     ("D", X("A5.1") + E_("9G"), "Name the invariant reactions.",
      "On cooling: eutectic, liquid → two solids; eutectoid, one solid → two solids; peritectic, liquid + solid → a different solid.", "P2", [
       L("mse-invariant-name", PH, "Name the reaction on cooling: {{q}}", ["Eutectic", "Eutectoid", "Peritectic"], [
         ("L → α + β", 0), ("γ → α + Fe₃C", 1), ("L + δ → γ", 2), ("L (61.9 wt% Sn) → α + β at 183 °C", 0), ("austenite (0.76 wt% C) → pearlite at 727 °C", 1), ("L + α → β", 2)],
         "Count the liquids: one going to two solids is eutectic, none is eutectoid, liquid plus solid making a new solid is peritectic"),
       F("mse-diagram-facts", PH, [
         ("A eutectic alloy freezes", "at one temperature, like a pure metal", "over the widest range of any composition", "only on quenching", "into a single solid phase"),
         ("The line above which an alloy is entirely liquid is the", "liquidus", "solidus", "solvus", "tie line"),
         ("The line marking the limit of solid solubility is the", "solvus", "liquidus", "solidus", "isotherm"),
         ("A copper-nickel alloy between liquidus and solidus contains", "liquid and one solid solution of different compositions", "two solid phases", "a eutectic", "a compound"),
         ("Fast freezing of a solid-solution alloy leaves", "cored grains, richer in the higher-melting element at the centre", "a uniform composition", "a eutectic at every boundary", "martensite")],
         "Liquidus above, solidus below, solvus between solids")])]),
   2: ("Steel and heat treatment", [
     ("A", X("A5.1") + E_("9C"), "Identify the phases and landmarks of the iron-carbon diagram.",
      "Ferrite (α) is BCC and holds at most 0.022 wt% C; austenite (γ) is FCC and holds up to 2.14; cementite Fe₃C is 6.70 wt% C. The eutectoid is 0.76 wt% C at 727 °C; steels lie below 2.14 wt% C, cast irons above.", "P2", [
       F("mse-fe-c-facts", PH, [
         ("Austenite is", "FCC iron with carbon in solution", "BCC iron with carbon in solution", "the compound Fe₃C", "a mixture of ferrite and cementite"),
         ("Ferrite is", "BCC iron holding very little carbon", "FCC iron", "the compound Fe₃C", "a layered mixture"),
         ("Pearlite is", "alternating layers of ferrite and cementite", "a single phase", "carbon-saturated martensite", "FCC iron"),
         ("The eutectoid composition and temperature of plain carbon steel are about", "0.76 wt% C and 727 °C", "2.14 wt% C and 1147 °C", "4.30 wt% C and 1147 °C", "0.022 wt% C and 912 °C"),
         ("Austenite dissolves far more carbon than ferrite because", "its interstitial sites are larger, though it is more densely packed", "it is less dense", "it is hotter and nothing else", "carbon replaces iron atoms in it")],
         "α is BCC and carbon-poor, γ is FCC and carbon-rich, Fe₃C is hard and brittle"),
       L("mse-steel-class", PH, "Classify an iron-carbon alloy holding {{q}}.", ["Hypoeutectoid steel", "Hypereutectoid steel", "Cast iron"], [
         ("0.40 wt% C", 0), ("1.1 wt% C", 1), ("3.5 wt% C", 2), ("0.20 wt% C", 0), ("0.95 wt% C", 1), ("2.8 wt% C", 2)],
         "Below 0.76 is hypoeutectoid, 0.76 to 2.14 hypereutectoid, above 2.14 cast iron")]),
     ("B", X("A5.1") + E_("9C", "9G"), "Compute the microconstituents of a slowly cooled steel.",
      "In a hypoeutectoid steel the austenite left at 727 °C has 0.76 wt% C and becomes pearlite, so pearlite is a lever between 0.022 and 0.76. Total cementite is a lever between 0.022 and 6.70.", "P1", [
       N("mse-pearlite-fraction", PH, f"A slowly cooled steel holds {{{{ko}}}} wt% C. Find the weight percent of pearlite. {FEC}", "(ko - 0.022)/(0.76 - 0.022)*100",
         "100 - (Rational('0.76') - ko)/(Rational('0.76') - Rational('0.022'))*100", "Pearlite forms from the austenite present just above 727 °C", tex="W_p",
         cases=C("ko", [(0.40,), (0.20,), (0.60,), (0.30,), (0.10,)])),
       N("mse-cementite-fraction", PH, f"A slowly cooled steel holds {{{{ko}}}} wt% C. Find the total weight percent of cementite at room temperature. {FEC}", "(ko - 0.022)/(6.70 - 0.022)*100",
         f"solve(Eq((1 - {M}/100)*Rational('0.022') + {M}/100*Rational('6.70'), ko), {M})[0]", "A carbon balance over ferrite and cementite", tex="W_{Fe_3C}",
         cases=C("ko", [(0.40,), (0.76,), (1.0,), (0.20,), (1.4,)]))]),
     ("C", X("A5.7") + E_("9G"), "Predict the product of an isothermal or quench treatment from a TTT diagram.",
      "Austenite held just below 727 °C gives coarse pearlite, lower gives fine pearlite, below the nose (about 550 to 250 °C) bainite; quenched fast enough to miss the nose it shears to martensite, which is hard, brittle and not on the equilibrium diagram.", "P2", [
       L("mse-ttt-product", PH, "A eutectoid steel is austenitized, then: {{q}} What forms?", ["Coarse pearlite", "Bainite", "Martensite"], [
         ("held at 700 °C until transformation ends.", 0), ("quenched to 350 °C and held until transformation ends.", 1), ("quenched in water to room temperature.", 2),
         ("cooled very slowly in the furnace.", 0), ("quenched to 300 °C, held for a day, then cooled.", 1), ("quenched fast enough to miss the nose of the curve.", 2)],
         "High temperature gives coarse layers, below the nose gives bainite, missing the nose gives martensite"),
       F("mse-martensite-facts", PH, [
         ("Martensite forms by", "a diffusionless shear of the austenite lattice", "long-range diffusion of carbon", "nucleation and growth of cementite", "melting and refreezing"),
         ("The amount of martensite formed depends on", "the temperature reached, not the time held", "the time held only", "the grain size only", "the cooling medium's colour"),
         ("Martensite is hard because", "trapped carbon distorts the lattice to body-centred tetragonal", "it is FCC", "it contains graphite", "its grains are large"),
         ("Tempering martensite", "trades some hardness for toughness as fine carbides precipitate", "makes it harder and more brittle", "turns it back into austenite", "has no effect below 700 °C"),
         ("Fine pearlite is stronger than coarse pearlite because", "more ferrite-cementite boundaries block dislocations", "it contains more carbon", "it contains martensite", "its cementite is softer")],
         "Diffusion makes pearlite and bainite; shear makes martensite")]),
     ("D", X("A5.2") + E_("9G"), "Choose a heat treatment for steel and explain hardenability.",
      "Full annealing (furnace cool) gives the softest structure; normalizing (air cool) a finer, stronger one; quench and temper gives the best strength with toughness. Hardenability is the depth to which a steel forms martensite, measured by the Jominy end-quench test and raised by alloying.", "P2", [
       L("mse-heat-treatment", PH, "Which treatment? {{q}}", ["Full anneal", "Normalize", "Quench and temper"], [
         ("Austenitize and cool in still air to refine the grain", 1), ("Austenitize and furnace cool for the softest, most machinable state", 0), ("Austenitize, cool rapidly in oil, then reheat to 400 °C", 2),
         ("A shaft needs high strength with good toughness", 2), ("A forging must be softened as far as possible before machining", 0)],
         "Furnace cool, air cool, or quench then reheat"),
       F("mse-hardenability-facts", PH, [
         ("Hardenability is", "the depth to which a steel hardens on quenching", "the maximum hardness a steel can reach", "resistance to scratching", "the carbon content"),
         ("The Jominy test measures", "hardness against distance from a water-quenched end", "impact energy against temperature", "strain against time under load", "crack length against cycles"),
         ("Adding chromium, molybdenum or nickel to a steel", "shifts the transformation curves to longer times, so thicker sections harden", "lowers hardenability", "prevents martensite from forming", "raises the eutectoid carbon content to 2%"),
         ("The maximum hardness of martensite is set mainly by", "carbon content", "nickel content", "section size", "quench medium"),
         ("A more severe quench (water rather than oil) gives", "deeper hardening but more risk of distortion and cracking", "less martensite", "coarser pearlite", "no change")],
         "Carbon sets how hard; alloying sets how deep")]),
     ("E", X("A5.3", "A5.5"), "Use the Avrami equation for the fraction transformed.",
      "y = 1 − exp(−k tⁿ): the S-shaped curve of nucleation and growth. The rate is often quoted as 1 ÷ t at half transformation.", "P1", [
       N("mse-avrami-fraction", PH, "A transformation follows y = 1 − exp(−k tⁿ) with k = {{kk}} and n = {{kn}} (t in minutes). Find the percent transformed after {{kt}} min.", "(1 - exp(-kk*kt^kn))*100",
         "100 - 100/exp(kk*kt**kn)", "Raise the time to n first, then take the exponential", tex="y",
         cases=C("kk kn kt", [(0.0005, 2, 40), (0.01, 1.5, 20), (0.00002, 3, 30), (0.002, 2, 15), (0.05, 1, 10)])),
       N("mse-avrami-half-time", PH, "A transformation follows y = 1 − exp(−k tⁿ) with k = {{kk}} and n = {{kn}} (t in minutes). Find the time for 50% transformation, in minutes.", "(log(2)/kk)^(1/kn)",
         "exp(log(log(2)/kk)/kn)", "Set exp(−k tⁿ) to one half: tⁿ = ln 2 ÷ k", tex="t_{0.5}",
         cases=C("kk kn", [(0.0005, 2), (0.01, 1.5), (0.00002, 3), (0.002, 2), (0.05, 1)]))])]),
   3: ("Nucleation and glass", [
     ("A", X("A5.5"), "Compute a critical nucleus radius and scale the nucleation barrier.",
      "A solid nucleus gains volume free energy and pays surface energy: r* = 2γT_m ÷ (ΔH_f ΔT) and ΔG* varies as 1 ÷ ΔT². Larger undercooling means smaller nuclei and a lower barrier.", "P1", [
       N("mse-critical-radius", PH, "A metal has solid-liquid surface energy {{kg}} J/m², melting point {{kt}} K and latent heat {{kh}} × 10⁹ J/m³. Find the critical nucleus radius at an undercooling of {{kd}} K, in nm.", "2*kg*kt/(kh*kd)",
         "Max(*solve(diff(4*pi*Y**2*kg - Rational(4, 3)*pi*Y**3*kh*kd/kt, Y), Y))", "ΔG_v = ΔH_f ΔT ÷ T_m, then r* = 2γ ÷ ΔG_v; J/m² over 10⁹ J/m³ is nm", tex="r^*",
         cases=C("kg kt kh kd", [(0.132, 1337, 1.16, 230), (0.177, 1358, 1.77, 236), (0.255, 1728, 2.53, 319), (0.132, 1337, 1.16, 50), (0.204, 1811, 1.85, 295)])),
       N("mse-nucleation-barrier", PH, "The nucleation barrier ΔG* varies as 1 ÷ ΔT². Find the barrier at an undercooling of {{kb}} K as a percentage of its value at {{ka}} K.", "(ka/kb)^2*100",
         "100*(1/kb**2)/(1/ka**2)", "Ratio of the inverse squares", tex="\\%",
         cases=C("ka kb", [(50, 100), (100, 250), (200, 150), (20, 80), (120, 180)]))]),
     ("B", X("A5.6"), "Tell a glass transition from melting.",
      "A crystal melts sharply at T_m. An amorphous solid has no T_m: it softens over the glass transition T_g, where the slope of volume against temperature changes. A semicrystalline polymer shows both.", "P2", [
       L("mse-tg-or-tm", PH, "What does this material show on heating? {{q}}", ["A sharp melting point only", "A glass transition only", "Both a glass transition and a melting point"], [
         ("A pure crystalline metal", 0), ("Window (soda-lime silica) glass", 1), ("Semicrystalline polyethylene", 2), ("Atactic polystyrene, fully amorphous", 1), ("Crystalline sodium chloride", 0), ("Nylon 6,6, about half crystalline", 2)],
         "Crystals melt, glasses soften, semicrystalline polymers do both"),
       F("mse-glass-facts", PH, [
         ("A glass forms when a liquid is cooled", "too fast for crystals to nucleate and grow", "very slowly", "under high vacuum only", "below absolute zero"),
         ("At the glass transition, the specific volume against temperature shows", "a change of slope with no jump", "a sudden jump", "no change at all", "a maximum"),
         ("Below its glass transition an amorphous polymer is", "rigid and brittle", "a viscous liquid", "rubbery", "crystalline"),
         ("Metallic glasses need very high cooling rates because", "metal atoms rearrange into crystals extremely quickly", "they have no melting point", "they are polymers", "their surface energy is zero"),
         ("Compared with the crystal of the same composition, a glass has", "no long-range order and a slightly lower density", "long-range order", "a higher density", "sharp X-ray diffraction peaks")],
         "A glass is a liquid's structure frozen in")])])})

U6 = ("failure", "Failure", X("A4.3", "A4.4", "A4.5", "A4.6") + E_("9J"), ["DEFECT"], {
   1: ("Fracture, fatigue and creep", [
     ("A", X("A4.4") + E_("9J"), "Use fracture toughness to find a critical stress or flaw size.",
      "K = Yσ√(πa); fracture when K reaches K_IC. For a surface crack a is the depth, for an internal crack half the length.", "P1", [
       N("mse-critical-stress", FA, "A plate with K_IC = {{kk}} MPa·m^½ contains a surface crack {{ka}} mm deep, with Y = {{ky}}. Find the stress at which it fractures, in MPa.", "kk/(ky*sqrt(pi*ka/1000))",
         f"solve(Eq(ky*{M}*sqrt(pi*ka/1000), kk), {M})[0]", "Convert the crack to metres before taking the root", tex="\\sigma_c",
         cases=C("kk ka ky", [(54.8, 4.0, 1.0), (24, 2.0, 1.12), (98.9, 0.75, 1.0), (40, 10, 1.1), (3.0, 0.5, 1.0)])),
       N("mse-critical-flaw", FA, "A part with K_IC = {{kk}} MPa·m^½ carries {{kg}} MPa, with Y = {{ky}}. Find the largest surface crack it tolerates, in mm.", "(kk/(ky*kg))^2/pi*1000",
         f"solve(Eq(ky**2*kg**2*pi*{M}/1000, kk**2), {M})[0]", "Square K_IC ÷ Yσ and divide by π", tex="a_c",
         cases=C("kk kg ky", [(35, 250, 1.0), (54.8, 1030, 1.0), (24, 300, 1.12), (82, 500, 1.1), (4.5, 100, 1.0)]))]),
     ("B", X("A4.3", "A4.4"), "Apply the Griffith criterion and tell ductile from brittle fracture.",
      "A brittle crack grows when the elastic energy released pays for the new surface: σ_c = √(2Eγ_s ÷ πa). Ductile fracture absorbs far more energy through plastic flow (cup and cone); BCC metals turn brittle below a transition temperature.", "P1", [
       N("mse-griffith", FA, "A glass has E = {{kg}} GPa and surface energy {{kw}} J/m². Find the stress that propagates an internal crack of half-length {{ka}} µm, in MPa.", "sqrt(2*kg*1e9*kw/(pi*ka*1e-6))/1e6",
         f"Max(*solve(Eq(pi*ka*({M}*10**6)**2, 2*kg*10**9*kw*10**6), {M}))", "Work in pascals and metres, then convert", tex="\\sigma_c",
         cases=C("kg kw ka", [(69, 0.30, 2.0), (69, 0.30, 50), (393, 0.90, 5.0), (225, 1.0, 0.5), (72, 0.35, 10)])),
       F("mse-fracture-mode", FA, [
         ("A cup-and-cone fracture surface with much necking shows", "ductile fracture", "brittle cleavage", "fatigue", "creep rupture"),
         ("A flat, bright, faceted fracture with no necking shows", "brittle cleavage", "ductile fracture", "plastic collapse", "wear"),
         ("Which metals show a ductile-to-brittle transition on cooling?", "BCC metals such as low-carbon steel", "FCC metals such as aluminium and copper", "All metals equally", "None"),
         ("The ductile-to-brittle transition is measured with", "Charpy impact tests over a range of temperatures", "a Jominy end quench", "a Brinell indent", "a creep test"),
         ("A crack that follows the grain boundaries is", "intergranular", "transgranular", "cup and cone", "a slip band")],
         "Ductile fracture warns with deformation; brittle fracture does not")]),
     ("C", X("A4.4") + E_("9J"), "Compute the stress at the tip of a flaw.",
      "σ_m = 2σ₀√(a ÷ ρ_t): the maximum stress at a crack of length a and tip radius ρ_t. Sharp cracks concentrate stress; drilling a hole at the tip blunts it.", "P1", [
       N("mse-tip-stress", FA, "A plate under {{kg}} MPa has a surface crack {{ka}} mm long with a tip radius of {{kp}} mm. Find the maximum stress at the tip in MPa.", "2*kg*sqrt(ka/kp)",
         f"Max(*solve(Eq(kp*{M}**2, 4*kg**2*ka), {M}))", "Twice the applied stress times the root of length over tip radius", tex="\\sigma_m",
         cases=C("kg ka kp", [(100, 1.0, 0.01), (50, 2.5, 0.001), (200, 0.5, 0.05), (30, 4.0, 0.0025), (140, 0.25, 0.01)])),
       N("mse-tip-radius", FA, "A {{ka}} mm crack raises an applied stress of {{kg}} MPa to {{kt}} MPa at its tip. Find the tip radius in mm.", "ka*(2*kg/kt)^2",
         f"solve(Eq(kt**2*{M}, 4*kg**2*ka), {M})[0]", "Square the stress ratio", tex="\\rho_t",
         cases=C("ka kg kt", [(1.0, 100, 2000), (2.5, 50, 5000), (0.5, 200, 1265), (4.0, 30, 2400), (2.0, 80, 800)]))]),
     ("D", X("A4.6") + E_("9J"), "Describe a fatigue cycle and read an S-N curve.",
      "σ_m = (σ_max + σ_min) ÷ 2, σ_a = (σ_max − σ_min) ÷ 2, R = σ_min ÷ σ_max. Steels and titanium alloys have a fatigue limit below which life is unlimited; aluminium, copper and magnesium do not.", "P1", [
       N("mse-fatigue-amplitude", FA, "A part cycles between {{ka}} MPa and {{kb}} MPa (tension positive). Find the stress amplitude in MPa.", "(ka - kb)/2",
         f"solve(Eq((ka + kb)/Rational(2) + {M}, ka), {M})[0]", "Half the range; the mean plus the amplitude is the maximum", tex="\\sigma_a",
         cases=C("ka kb", [(300, -100), (450, 50), (200, -200), (120, 20), (500, -350)])),
       L("mse-fatigue-limit", FA, "On an S-N curve, does this alloy have a fatigue limit? {{q}}", ["Yes: below it the part lasts indefinitely", "No: quote a fatigue strength at a stated number of cycles"], [
         ("Plain carbon steel", 0), ("An aluminium alloy", 1), ("A titanium alloy", 0), ("Copper", 1), ("A magnesium alloy", 1), ("A low-alloy steel", 0)],
         "Steels and titanium level off; most nonferrous alloys keep falling")]),
     ("E", X("A4.6"), "Use the Paris law for fatigue crack growth.",
      "da/dN = A(ΔK)^m with ΔK = YΔσ√(πa) and m about 2 to 4 for metals. Life is the integral of dN from the initial to the critical crack length.", "P1", [
       N("mse-paris-ratio", FA, "A crack grows by the Paris law with m = {{km}}. By what factor does the growth rate rise if the stress range is multiplied by {{kf}} at the same crack length?", "kf^km",
         "exp(km*log(kf))", "ΔK is proportional to the stress range, and the rate goes as ΔK to the power m", tex="factor",
         cases=C("km kf", [(3, 2), (4, 1.5), (2, 3), (3, 1.2), (3.5, 2)])),
       N("mse-paris-life", FA, "A crack grows by da/dN = A(ΔK)² with A = {{kc}} × 10⁻¹¹ m/cycle per (MPa·m^½)², Y = {{ky}} and a stress range of {{kg}} MPa. How many million cycles take it from {{ko}} mm to {{kf}} mm?", "log(kf/ko)/(kc*1e-11*ky^2*kg^2*pi)/1e6",
         "integrate(1/(kc*Rational('1e-11')*ky**2*kg**2*pi*Y), (Y, ko, kf))/10**6", "With m = 2 the integral of da ÷ a is a logarithm, so the millimetres cancel", tex="N_f",
         cases=C("kc ky kg ko kf", [(1.0, 1.0, 100, 1, 10), (2.0, 1.12, 80, 0.5, 8), (0.5, 1.0, 150, 2, 20), (1.5, 1.1, 60, 1, 25), (3.0, 1.0, 120, 0.2, 5)]))]),
     ("F", X("A4.5") + E_("9J"), "Work with steady-state creep and the Larson-Miller parameter.",
      "Steady creep rate goes as σⁿ exp(−Q_c ÷ RT); creep matters above about 0.4 of the absolute melting temperature. The Larson-Miller parameter T(C + log t_r), with C about 20 and t_r in hours, trades temperature against rupture life.", "P1", [
       N("mse-larson-miller", FA, "A part runs at {{kt}} K and ruptures after {{kh}} h. Find the Larson-Miller parameter T(20 + log₁₀ t_r) in units of 10³ K·h.", "kt*(20 + log10(kh))/1000",
         "kt*(20 + log(kh, 10))/1000", "Base-ten logarithm of the life in hours", tex="LMP",
         cases=C("kt kh", [(1073, 1000), (923, 100000), (1000, 5000), (1150, 100), (873, 20000)])),
       N("mse-creep-exponent", FA, "At one temperature the steady creep rate is {{ka}} × 10⁻⁷ per hour at {{kc}} MPa and {{kb}} × 10⁻⁷ per hour at {{kd}} MPa. Find the stress exponent n.", "log(kb/ka)/log(kd/kc)",
         "(log(kb) - log(ka))/(log(kd) - log(kc))", "The slope of log rate against log stress", tex="n",
         cases=C("ka kc kb kd", [(1.0, 55, 100, 138), (2.5, 80, 240, 200), (6.6, 15, 880, 43), (0.4, 100, 13, 200), (3.0, 40, 30, 70)]))])])})

RR = "Radius-ratio ranges: 0.225 to 0.414 gives 4, 0.414 to 0.732 gives 6, 0.732 to 1.0 gives 8."
U7 = ("classes", "Material classes and characterisation", X("B6.1", "B6.3", "B6.4", "B8.1", "B8.2", "B8.3", "B11.1", "B11.2", "A3.2", "A3.3", "A3.4", "A4.7", "A4.8") + E_("9A", "9C", "9D", "9E", "9F"), ["LATTICE", "PATH"], {
   1: ("Ceramics", [
     ("A", X("B6.1"), "Predict a ceramic's coordination from the radius ratio and name the common structures.",
      "The cation takes as many anion neighbours as can touch it: r_C ÷ r_A of 0.225 to 0.414 gives tetrahedral (4), 0.414 to 0.732 octahedral (6), 0.732 to 1.0 cubic (8).", "P2", [
       L("mse-radius-ratio", CL, f"A ceramic has a cation-to-anion radius ratio of {{{{q}}}}. What coordination number is predicted? {RR}", ["4 (tetrahedral)", "6 (octahedral)", "8 (cubic)"], [
         ("0.56", 1), ("0.94", 2), ("0.40", 0), ("0.74", 2), ("0.29", 0), ("0.51", 1), ("0.69", 1)],
         "Find the band the ratio falls in"),
       F("mse-ceramic-structures", CL, [
         ("In the rock salt (NaCl) structure each ion has how many nearest neighbours of the other kind?", "6", "4", "8", "12"),
         ("In the caesium chloride structure the coordination number is", "8", "6", "4", "12"),
         ("In zinc blende (ZnS) each atom is bonded to", "4 neighbours, tetrahedrally", "6 neighbours", "8 neighbours", "12 neighbours"),
         ("Barium titanate, BaTiO₃, has the structure type", "perovskite", "rock salt", "fluorite", "zinc blende"),
         ("How many formula units are in one rock salt unit cell?", "4", "1", "2", "8"),
         ("Ceramics are brittle mainly because", "slip would bring like charges together or break directional bonds", "they have no crystal structure", "they contain too many dislocations", "their grains are too small")],
         "Size ratio sets the coordination; charge balance sets the formula"),
       ]),
     ("B", X("B6.1"), "Compute a ceramic's density and cell edge from its ions.",
      "ρ = n′(ΣA_C + ΣA_A) ÷ (V_cell N_A), with n′ formula units per cell. In rock salt the ions touch along the cell edge, so a = 2(r_C + r_A).", "P1", [
       N("mse-ceramic-density", CL, "{{kn}} has {{kc}} formula units per cubic cell of edge {{ka}} nm; the molar masses are {{km}} and {{kb}} g/mol. Find its density in g/cm³.", f"kc*(km + kb)/((ka*1e-7)^3*{NA})",
         f"solve(Eq({M}*(ka*Rational('1e-7'))**3*{NAS}, kc*km + kc*kb), {M})[0]", "Mass of the formula units in one cell over the cell volume", tex="\\rho",
         cases=C("kn kc ka km kb", [("Sodium chloride", 4, 0.5640, 22.99, 35.45), ("Magnesium oxide", 4, 0.4212, 24.31, 16.00), ("Caesium chloride", 1, 0.4123, 132.91, 35.45), ("Iron(II) oxide", 4, 0.4307, 55.85, 16.00), ("Potassium bromide", 4, 0.6600, 39.10, 79.90)])),
       N("mse-rock-salt-edge", CL, "A rock salt crystal has cation radius {{kr}} nm and anion radius {{kq}} nm. Find its cell edge in nm.", "2*(kr + kq)",
         f"Max(*solve(Eq(({M}/2 - kr)**2, kq**2), {M}))", "Along an edge: half an anion, a whole cation, half an anion, twice", tex="a",
         cases=C("kr kq", [(0.102, 0.181), (0.072, 0.140), (0.138, 0.196), (0.077, 0.140), (0.100, 0.140)]))]),
     ("C", X("B6.3") + E_("9A"), "Compute a flexural strength from a three-point bend test.",
      "Ceramics are tested in bending because they are hard to grip in tension. For a rectangular bar σ_fs = 3FL ÷ 2bd², with L the support span.", "P1", [
       N("mse-flexural-strength", CL, "A ceramic bar {{kb}} mm wide and {{kd}} mm deep breaks at {{kf}} N in three-point bending over a {{kw}} mm span. Find its flexural strength in MPa.", "3*kf*kw/(2*kb*kd^2)",
         "(kf*kw/4)*(kd/2)/(kb*kd**3/12)", "The check uses bending stress M c ÷ I with M = FL ÷ 4 at midspan", tex="\\sigma_{fs}",
         cases=C("kb kd kf kw", [(10, 5, 620, 40), (6.4, 3.2, 290, 25), (15, 7.5, 2500, 50), (8, 4, 380, 30), (12, 6, 1150, 45)])),
       N("mse-flexural-load", CL, "A ceramic with flexural strength {{kg}} MPa is made into a bar {{kb}} mm wide and {{kd}} mm deep on a {{kw}} mm span. Find the three-point load that breaks it, in N.", "2*kg*kb*kd^2/(3*kw)",
         f"solve(Eq(3*{M}*kw, 2*kg*kb*kd**2), {M})[0]", "Rearrange σ = 3FL ÷ 2bd²", tex="F",
         cases=C("kg kb kd kw", [(300, 10, 5, 40), (105, 12, 6, 50), (550, 6, 3, 25), (69, 20, 10, 80), (800, 4, 3, 20)]))]),
     ("D", X("B6.4", "A4.7"), "Compute a thermal stress and a thermal shock limit.",
      "A constrained body heated or cooled by ΔT carries σ = EαΔT. A brittle solid survives a sudden temperature change of about σ_f ÷ Eα, so low expansion and high conductivity resist thermal shock.", "P1", [
       N("mse-thermal-stress", CL, "A rod with E = {{kg}} GPa and α = {{kc}} × 10⁻⁶ per K is held rigid while its temperature changes by {{kt}} K. Find the stress magnitude in MPa.", "kg*kc*kt/1000",
         f"solve(Eq({M}/(kg*1000), kc*kt/10**6), {M})[0]", "The blocked thermal strain αΔT times the modulus", tex="\\sigma",
         cases=C("kg kc kt", [(100, 20, 80), (380, 7.6, 150), (70, 9, 200), (207, 12, 40), (310, 4.5, 500)])),
       N("mse-thermal-shock", CL, "A ceramic has fracture strength {{kf}} MPa, E = {{kg}} GPa and α = {{kc}} × 10⁻⁶ per K. Estimate the largest sudden temperature change it survives, σ_f ÷ Eα, in K.", "kf*1000/(kg*kc)",
         f"solve(Eq({M}*kg*1000*kc/10**6, kf), {M})[0]", "Set the thermal stress EαΔT equal to the strength", tex="\\Delta T",
         cases=C("kf kg kc", [(300, 380, 7.6), (70, 69, 9.0), (110, 73, 0.5), (800, 310, 3.3), (400, 430, 4.6)]))])]),
   2: ("Composites", [
     ("A", X("B11.1") + E_("9E"), "Compute a continuous-fibre composite's modulus along the fibres.",
      "Loaded along the fibres, fibre and matrix strain equally (isostrain): E_c = E_m V_m + E_f V_f, the upper bound.", "P1", [
       N("mse-isostrain-modulus", CL, "A composite is {{kv}}% by volume fibres of modulus {{kf}} GPa in a matrix of {{km}} GPa. Find its modulus along the fibres in GPa.", "kf*kv/100 + km*(1 - kv/100)",
         f"solve(Eq({M}*100, kf*kv + km*(100 - kv)), {M})[0]", "Volume-weighted average of the two moduli", tex="E_{cl}",
         cases=C("kv kf km", [(40, 69, 3.4), (60, 230, 2.4), (30, 131, 3.0), (50, 72.5, 3.5), (65, 380, 70)])),
       N("mse-fibre-fraction", CL, "Fibres of modulus {{kf}} GPa go into a matrix of {{km}} GPa. What volume percent of fibres gives a longitudinal modulus of {{kg}} GPa?", "(kg - km)/(kf - km)*100",
         f"solve(Eq(kf*{M}/100 + km*(1 - {M}/100), kg), {M})[0]", "Solve the rule of mixtures for V_f", tex="V_f",
         cases=C("kf km kg", [(230, 2.4, 100), (69, 3.4, 30), (380, 70, 200), (131, 3.0, 50), (72.5, 3.5, 45)]))]),
     ("B", X("B11.1") + E_("9E"), "Compute the transverse modulus and say which loading gives which bound.",
      "Loaded across the fibres, fibre and matrix carry equal stress (isostress): 1 ÷ E_c = V_m ÷ E_m + V_f ÷ E_f, the lower bound, dominated by the soft matrix.", "P1", [
       N("mse-isostress-modulus", CL, "A composite is {{kv}}% by volume fibres of modulus {{kf}} GPa in a matrix of {{km}} GPa. Find its modulus across the fibres in GPa.", "km*kf/((1 - kv/100)*kf + kv/100*km)",
         "1/(kv/(100*kf) + (100 - kv)/(100*km))", "Compliances add in series", tex="E_{ct}",
         cases=C("kv kf km", [(40, 69, 3.4), (60, 230, 2.4), (30, 131, 3.0), (50, 72.5, 3.5), (65, 380, 70)])),
       L("mse-composite-bound", CL, "Which loading case is this? {{q}}", ["Isostrain: the upper bound", "Isostress: the lower bound"], [
         ("Load applied along continuous aligned fibres", 0), ("Load applied across continuous aligned fibres", 1), ("Fibre and matrix stretch by the same amount", 0), ("Fibre and matrix carry the same stress", 1),
         ("The modulus is a volume-weighted average of the moduli", 0), ("The compliance is a volume-weighted average of the compliances", 1)],
         "Parallel to the fibres strains match; across them stresses match")]),
     ("C", X("B11.1", "B11.2") + E_("9E"), "Compute the load carried by the fibres and the critical fibre length.",
      "Under isostrain F_f ÷ F_m = E_f V_f ÷ E_m V_m. A fibre reaches its full strength only if it is longer than l_c = σ_f d ÷ 2τ_c, with τ_c the fibre-matrix bond strength.", "P1", [
       N("mse-fibre-load-share", CL, "A composite is {{kv}}% by volume fibres of modulus {{kf}} GPa in a matrix of {{km}} GPa, loaded along the fibres. What percent of the load do the fibres carry?", "kf*kv/(kf*kv + km*(100 - kv))*100",
         f"solve(Eq({M}/(100 - {M}), kf*kv/(km*(100 - kv))), {M})[0]", "Each phase carries load in proportion to modulus times volume fraction", tex="\\%",
         cases=C("kv kf km", [(40, 69, 3.4), (60, 230, 2.4), (30, 131, 3.0), (10, 72.5, 3.5), (65, 380, 70)])),
       N("mse-critical-length", CL, "Fibres of strength {{kg}} MPa and diameter {{kd}} µm are bonded to a matrix with shear strength {{kt}} MPa. Find the critical fibre length in mm.", "kg*kd/(2*kt)/1000",
         f"solve(Eq(2*kt*{M}*1000, kg*kd), {M})[0]", "Shear on the fibre surface over half its length must build the full tensile load", tex="l_c",
         cases=C("kg kd kt", [(3500, 10, 20), (4000, 7, 50), (2000, 15, 10), (3450, 12, 35), (1500, 100, 80)]))])]),
   3: ("Electronic and magnetic behaviour", [
     ("A", X("A4.8", "B8.1"), "Compute a conductivity from carrier density and mobility.",
      "σ = n|e|μ, with e = 1.602 × 10⁻¹⁹ C. Metals have about one free electron per atom or more; their mobility, not their carrier count, falls on heating or alloying.", "P1", [
       N("mse-conductivity", CL, "A metal has {{kp}} × 10^{{kq}} free electrons per m³ with mobility {{ku}} m²/V·s. Find its conductivity in units of 10⁶ S/m. (e = 1.602 × 10⁻¹⁹ C)", "kp*10^kq*1.602e-19*ku/1e6",
         f"solve(Eq({M}*10**6/(kp*10**kq*Rational('1.602e-19')), ku), {M})[0]", "Carriers per volume times charge times mobility", tex="\\sigma",
         cases=C("kp kq ku", [(8.5, 28, 0.0044), (5.9, 28, 0.0068), (18.1, 28, 0.0013), (2.5, 28, 0.0053), (8.5, 28, 0.0030)])),
       N("mse-mobility", CL, "A metal has conductivity {{kg}} × 10⁷ S/m and {{kp}} × 10²⁸ free electrons per m³. Find the electron mobility in units of 10⁻³ m²/V·s. (e = 1.602 × 10⁻¹⁹ C)", "kg*1e7/(kp*1e28*1.602e-19)*1000",
         f"solve(Eq(kp*10**28*Rational('1.602e-19')*{M}/1000, kg*10**7), {M})[0]", "μ = σ ÷ n e", tex="\\mu",
         cases=C("kg kp", [(6.0, 8.5), (3.8, 18.1), (6.8, 5.9), (4.3, 5.9), (1.0, 17.0)]))]),
     ("B", X("B8.1", "B8.2"), "Classify a solid by its band gap and compute an intrinsic conductivity.",
      "Metals have a partly filled band or overlapping bands; semiconductors a gap under about 2 eV; insulators a wider one. An intrinsic semiconductor has equal electrons and holes: σ = n_i|e|(μ_e + μ_h).", "P1", [
       N("mse-intrinsic-conductivity", CL, "An intrinsic semiconductor has n_i = {{kp}} × 10^{{kq}} per m³, electron mobility {{ku}} and hole mobility {{kh}} m²/V·s. Find its conductivity in S/m. (e = 1.602 × 10⁻¹⁹ C)", "kp*10^kq*1.602e-19*(ku + kh)",
         "kp*10**kq*Rational('1.602e-19')*ku + kp*10**kq*Rational('1.602e-19')*kh", "Electrons and holes both carry current; add their mobilities", tex="\\sigma",
         cases=C("kp kq ku kh", [(1.0, 16, 0.14, 0.048), (2.3, 19, 0.38, 0.18), (1.5, 16, 0.135, 0.048), (4.0, 19, 0.39, 0.19), (7.0, 12, 0.85, 0.04)])),
       L("mse-band-class", CL, "Classify the solid: {{q}}", ["Metal", "Semiconductor", "Insulator"], [
         ("band gap 1.1 eV", 1), ("valence and conduction bands overlap", 0), ("band gap 5.5 eV", 2), ("band gap 0.67 eV", 1), ("band gap 9 eV", 2), ("a half-filled band", 0), ("conductivity rises steeply on heating, gap 1.4 eV", 1)],
         "No gap, a small gap, or a large gap")]),
     ("C", X("B8.2"), "Predict the carrier type a dopant gives.",
      "In silicon or germanium a group 15 atom (P, As, Sb) donates an electron: n-type. A group 13 atom (B, Al, Ga, In) accepts one and leaves a hole: p-type.", "P2", [
       L("mse-dopant-type", CL, "What type of semiconductor results? {{q}}", ["n-type", "p-type"], [
         ("Silicon doped with arsenic", 0), ("Silicon doped with gallium", 1), ("Germanium doped with antimony", 0), ("Silicon doped with aluminium", 1), ("Silicon doped with phosphorus", 0), ("Germanium doped with indium", 1), ("Silicon doped with boron", 1)],
         "One more valence electron than the host donates; one fewer accepts"),
       F("mse-extrinsic-facts", CL, [
         ("In an n-type semiconductor the majority carriers are", "electrons", "holes", "ions", "phonons"),
         ("A donor level sits", "just below the conduction band", "just above the valence band", "in the middle of the gap", "inside the valence band"),
         ("An acceptor level sits", "just above the valence band", "just below the conduction band", "in the middle of the gap", "above the conduction band"),
         ("Heating a metal lowers its conductivity; heating an intrinsic semiconductor", "raises it, because many more carriers are excited across the gap", "lowers it for the same reason", "leaves it unchanged", "makes it a metal"),
         ("At room temperature the conductivity of doped silicon is set mainly by", "the dopant concentration", "the band gap alone", "the grain size", "the dislocation density")],
         "Donors give electrons, acceptors give holes")]),
     ("D", X("B8.3"), "Classify magnetic behaviour and state what a superconductor does.",
      "Diamagnets weakly oppose a field; paramagnets weakly align with it; ferromagnets (Fe, Co, Ni) align strongly and stay magnetised below the Curie temperature. Below T_c a superconductor has zero resistance and expels magnetic flux.", "P2", [
       L("mse-magnetic-class", CL, "Classify the magnetic behaviour: {{q}}", ["Diamagnetic", "Paramagnetic", "Ferromagnetic"], [
         ("Copper", 0), ("Aluminium", 1), ("Iron at room temperature", 2), ("Nickel at room temperature", 2), ("Iron above its Curie temperature of 768 °C", 1), ("A superconductor below its critical temperature", 0), ("Cobalt at room temperature", 2)],
         "Weakly repelled, weakly attracted, or strongly and permanently magnetised"),
       F("mse-magnet-facts", CL, [
         ("A soft magnetic material has", "a narrow hysteresis loop and low coercivity, for transformer cores", "a wide loop, for permanent magnets", "no domains", "a Curie temperature of zero"),
         ("A hard magnetic material has", "high coercivity and remanence, for permanent magnets", "a narrow loop", "no hysteresis", "high electrical resistance only"),
         ("Above the Curie temperature a ferromagnet becomes", "paramagnetic", "diamagnetic", "superconducting", "antiferromagnetic"),
         ("The expulsion of magnetic flux from a superconductor is", "the Meissner effect", "the Hall effect", "the Seebeck effect", "the skin effect"),
         ("The area inside a hysteresis loop is", "the energy lost per volume in each cycle", "the saturation magnetisation", "the permeability", "the Curie temperature")],
         "Narrow loops switch easily; wide loops hold their magnetisation")])]),
   4: ("Alloys and processing", [
     ("A", E_("9C"), "Read a steel designation and tell the classes of ferrous alloy apart.",
      "In AISI/SAE four-digit steels the last two digits are carbon in hundredths of a weight percent: 1040 is plain carbon with 0.40% C. Stainless steels need at least about 11% Cr. Gray iron has graphite flakes, ductile iron spheroids.", "P2", [
       F("mse-steel-designation", CL, [
         ("AISI 1040 steel is", "plain carbon steel with about 0.40 wt% C", "plain carbon steel with about 4.0 wt% C", "an alloy steel with 10% nickel", "a stainless steel"),
         ("AISI 4340 steel contains about", "0.40 wt% C with nickel, chromium and molybdenum", "0.43 wt% C and nothing else", "4.3 wt% C", "34 wt% chromium"),
         ("A steel is stainless when it holds at least about", "11 wt% chromium", "2 wt% chromium", "11 wt% nickel", "0.8 wt% carbon"),
         ("Type 304 stainless steel is", "austenitic and non-magnetic", "martensitic and magnetic", "ferritic and magnetic", "a tool steel"),
         ("The graphite in gray cast iron is in the form of", "flakes, which make it weak in tension but good at damping", "spheroids", "cementite plates", "martensite needles"),
         ("Ductile (nodular) iron gets its spheroidal graphite from", "small additions of magnesium or cerium", "rapid quenching", "a long anneal of white iron", "extra silicon alone")],
         "Last two digits are carbon; chromium makes stainless; graphite shape names the cast iron"),
       L("mse-carbon-class", CL, "Classify by carbon content (low under 0.25, medium 0.25 to 0.60, high 0.60 to 1.4 wt% C, cast iron above 2.14): {{q}}", ["Low-carbon steel", "Medium-carbon steel", "High-carbon steel", "Cast iron"], [
         ("AISI 1020", 0), ("AISI 1045", 1), ("AISI 1095", 2), ("3.2 wt% C with 2% Si", 3), ("AISI 4140", 1), ("AISI 1010", 0), ("AISI 1080", 2)],
         "Read the last two digits as hundredths of a percent")]),
     ("B", E_("9D"), "Identify the common nonferrous alloys and how they are strengthened.",
      "Brass is Cu-Zn, bronze Cu-Sn. Aluminium tempers: T means solution treated and aged, H strain hardened, O annealed. Titanium alloys give the best strength to weight; nickel superalloys keep strength hot.", "P2", [
       F("mse-nonferrous-facts", CL, [
         ("Brass is an alloy of copper with", "zinc", "tin", "nickel", "aluminium"),
         ("Bronze is traditionally an alloy of copper with", "tin", "zinc", "lead", "iron"),
         ("Which alloy family is chosen for turbine blades at 1000 °C?", "Nickel-based superalloys", "Aluminium alloys", "Magnesium alloys", "Brasses"),
         ("Ti-6Al-4V is valued mainly for", "high strength to weight with corrosion resistance", "low cost", "high electrical conductivity", "ease of casting"),
         ("Magnesium alloys are hard to form at room temperature because", "they are HCP with few slip systems", "they are too dense", "they are FCC", "they have no dislocations"),
         ("Aluminium 2024 and 7075 get their strength from", "precipitation hardening", "martensite", "a eutectoid reaction", "graphite flakes")],
         "Know the base metal, the main addition and the reason it is used"),
       L("mse-temper", CL, "How is this alloy strengthened? {{q}}", ["Precipitation (age) hardening", "Cold work (strain hardening)", "Neither: it is used annealed"], [
         ("Aluminium 6061-T6", 0), ("Aluminium 1100-H14", 1), ("Aluminium 2024-T4", 0), ("Aluminium 5052-H32", 1), ("Aluminium 3003-O", 2), ("Beryllium copper, solution treated and aged", 0)],
         "T is heat treated, H is strain hardened, O is annealed")]),
     ("C", E_("9F"), "Match a manufacturing process to what it does to the metal.",
      "Casting fills a mould with liquid; forging, rolling, extrusion and drawing shape the solid, hot (above recrystallization, no hardening) or cold (strain hardened, better finish); powder metallurgy presses and sinters powder; welding leaves a heat-affected zone.", "P2", [
       L("mse-hot-or-cold", CL, "Hot working or cold working? {{q}}", ["Hot working", "Cold working"], [
         ("The metal recrystallizes as it deforms, so large reductions are possible", 0), ("The product is stronger, with a bright surface and close tolerances", 1), ("The surface oxidises and dimensions are less exact", 0),
         ("Ductility falls and an anneal may be needed between passes", 1), ("Done above about half the absolute melting temperature", 0)],
         "Above the recrystallization temperature there is no strain hardening"),
       F("mse-process-facts", CL, [
         ("Pushing a billet through a die to make a long constant section is", "extrusion", "forging", "rolling", "casting"),
         ("Pulling a rod through a die to reduce its diameter is", "drawing", "extrusion", "forging", "sintering"),
         ("Pressing metal powder and heating it below melting so the particles bond is", "powder metallurgy (sintering)", "investment casting", "hot rolling", "welding"),
         ("The region next to a weld whose microstructure is changed without melting is the", "heat-affected zone", "fusion zone", "parting line", "riser"),
         ("Which process suits a complex shape in a metal too brittle to forge?", "Casting", "Wire drawing", "Cold rolling", "Deep drawing"),
         ("A casting freezes with coarse grains at the centre because", "the centre cools slowly, so few nuclei grow large", "the centre cools fastest", "the mould is a single crystal", "carbon segregates there")],
         "Liquid route, solid deformation route, powder route, or joining")])]),
   5: ("Characterisation", [
     ("A", X("A3.2"), "Choose between XRD, EDS and XPS.",
      "X-ray diffraction gives crystal structure, phases and lattice parameters. EDS in an electron microscope gives elemental composition from characteristic X-rays. XPS gives the composition and chemical state of the top few nanometres.", "P2", [
       L("mse-analysis-choice", CL, "Which technique? {{q}}", ["XRD", "EDS", "XPS"], [
         ("Identify which crystalline phases a powder contains", 0), ("Map which elements are in a precipitate while imaging it in the SEM", 1), ("Find the oxidation state of iron in the top few nanometres of a surface", 2),
         ("Measure a lattice parameter", 0), ("Check whether a thin surface film is oxide or metal", 2), ("Get a quick elemental spectrum from a fracture surface in the SEM", 1)],
         "Structure, bulk elements under the beam, or surface chemistry"),
       F("mse-analysis-facts", CL, [
         ("XRD cannot identify a phase that is", "amorphous, since it gives only a broad hump", "cubic", "metallic", "fine grained"),
         ("EDS identifies elements from", "the energies of characteristic X-rays excited by the electron beam", "diffraction angles", "the kinetic energy of photoelectrons", "mass loss on heating"),
         ("XPS is surface sensitive because", "photoelectrons escape only from the top few nanometres", "X-rays cannot enter solids", "it uses visible light", "the sample is molten"),
         ("Broader diffraction peaks indicate", "smaller crystallites or more lattice strain", "larger grains", "a higher density", "a purer sample")],
         "Diffraction sees order, EDS sees elements, XPS sees the surface and its bonding")]),
     ("B", X("A3.3"), "Choose between optical, scanning and transmission electron microscopy.",
      "Optical microscopes resolve about 0.2 µm and show grains on a polished, etched surface. SEM resolves nanometres with great depth of field on bulk samples. TEM passes electrons through a thin foil and images dislocations and lattice planes.", "P2", [
       L("mse-microscope-choice", CL, "Which microscope? {{q}}", ["Optical microscope", "SEM", "TEM"], [
         ("Measure a 50 µm grain size on a polished and etched section", 0), ("Examine the rough topography of a fracture surface", 1), ("Image individual dislocations", 2),
         ("Resolve lattice planes in a nanoparticle", 2), ("See 1 µm precipitates on a bulk sample without thinning it", 1), ("Check a weld's grain structure quickly at 100×", 0)],
         "Light for grains, SEM for surfaces, TEM for defects inside a thin foil"),
       F("mse-microscopy-facts", CL, [
         ("Etching a polished metal reveals grain boundaries because", "boundaries are attacked faster and scatter light away", "grains change colour on their own", "it removes dislocations", "it melts the surface"),
         ("A TEM sample must be", "thin enough for electrons to pass through, about 100 nm", "coated in gold and several mm thick", "polished and etched only", "a powder"),
         ("The resolution limit of an optical microscope is about", "0.2 µm, set by the wavelength of light", "0.2 nm", "20 µm", "2 mm"),
         ("SEM images of fracture surfaces look three-dimensional because of", "the large depth of field", "transmitted electrons", "polarised light", "diffraction contrast")],
         "Wavelength sets resolution; sample thickness sets which electron microscope")]),
     ("C", X("A3.4"), "Choose between DSC and TGA and read what each shows.",
      "DSC (and DTA) record heat flow against temperature: glass transitions, melting, crystallisation, heats of reaction. TGA records mass against temperature: drying, decomposition, oxidation, filler content.", "P2", [
       L("mse-thermal-choice", CL, "Which thermal analysis? {{q}}", ["DSC", "TGA"], [
         ("Find a polymer's glass transition temperature", 0), ("Measure the mass lost as a hydrate dries", 1), ("Measure a heat of fusion", 0), ("Find the filler content of a composite by burning off the resin", 1),
         ("Detect the exotherm of crystallisation on heating a glass", 0), ("Follow the weight gained as a metal oxidises", 1)],
         "Heat flow or mass"),
       F("mse-thermal-facts", CL, [
         ("On a DSC trace a glass transition appears as", "a step in the baseline", "a sharp peak", "a mass loss", "nothing"),
         ("On a DSC heating trace, melting appears as", "an endothermic peak", "an exothermic peak", "a step in mass", "a flat line"),
         ("A TGA curve that drops in two separate steps shows", "two decomposition or loss events at different temperatures", "two glass transitions", "two melting points", "an instrument fault"),
         ("DTA differs from DSC in that it records", "the temperature difference between sample and reference rather than heat flow", "mass", "length", "X-ray intensity")],
         "Steps and peaks in heat flow are transitions; steps in mass are losses or gains")])])})

UNITS = {1: U1, 2: U2, 3: U3, 4: U4, 5: U5, 6: U6, 7: U7}
ADD = [(f"{FW['code']}-{n}.{tn}.{lo[0]}", qq) for n, u in UNITS.items() for tn, (tt, los) in u[4].items() for lo in los for qq in lo[5]]
