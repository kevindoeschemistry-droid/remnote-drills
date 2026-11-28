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
          primary="engineers-canada-materials", also=["pe-metmat", "fe-mechanical"], subject="Materials Science",
          note="Anchored on the Engineers Canada materials syllabus (all eighteen exams), the PE Metallurgical and Materials specification and FE Mechanical section 9, each read to its topic lines. Dislocation geometry, Miller indices and slip systems sit under lines that say only 'crystal structures' and 'plastic deformation', so those objectives are a house list in textbook order. Asked in words and numbers: no lattice or phase-diagram figure type exists yet. Polymer chemistry and colloids are in Polymers and Materials (MT); axial stress and Mohr's circle are in Engineering Mechanics.",
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
       ("B11.2", "Reinforcement type, orientation and length"),
       ("A1.1", "Phase relationships and the phase rule"), ("A1.2", "Laws of thermodynamics, enthalpy and heat balances"), ("A1.3", "Entropy, free energy and chemical equilibrium"),
       ("A1.4", "Solution models, activity and chemical potential"), ("A1.5", "Phase diagrams from thermodynamic properties"), ("A1.6", "Thermochemical analysis of materials processes"),
       ("A2.1", "Transport equations and interphase transport in materials processes"), ("A2.2", "Processing operations: mixed flow, plug flow, residence time"),
       ("A2.3", "Radiation heat transfer"), ("A2.4", "Mathematical models of transport"), ("A3.5", "Analysis of microstructure and surface morphology"),
       ("A6.1", "Selection for design criteria and constraints"), ("A6.2", "Shape and processing variables"), ("A6.3", "Material indices and selection charts"),
       ("A6.4", "Sustainable selection and design"), ("A6.5", "Life cycle assessment and end of life"),
       ("A7.1", "Degradation of metals, ceramics and polymers"), ("A7.2", "Basic corrosion theory"), ("A7.3", "Electrochemical corrosion theory"), ("A7.4", "Stress-assisted corrosion"),
       ("A7.5", "Protective coatings"), ("A7.6", "Corrosion inhibitors"), ("A7.7", "Cathodic and anodic protection"),
       ("B1.1", "Leaching processes"), ("B1.2", "Pourbaix diagrams"), ("B1.3", "Purification of leach liquors and solid-liquid separation"),
       ("B1.4", "Cementation, electrowinning and electrorefining"), ("B1.5", "Hydrometallurgy of copper, nickel, zinc, cobalt, gold and uranium"),
       ("B2.1", "Mineral processing"), ("B2.2", "Roasting, smelting, converting and refining"), ("B2.3", "Refractories"), ("B2.4", "Flow sheets with heat and mass balances"),
       ("B3.1", "Ironmaking and direct reduction"), ("B3.2", "Primary steelmaking"), ("B3.3", "Ladle metallurgy and secondary refining"), ("B3.4", "Continuous casting"),
       ("B3.5", "Fluxes, slags and refractories in steelmaking"),
       ("B4.1", "Properties and processing of non-ferrous metals"), ("B4.2", "Sulphide smelting of copper, nickel, lead and zinc"), ("B4.3", "Fused-salt electrolysis of aluminium and magnesium"),
       ("B4.4", "Refractory metals by chlorination"),
       ("B5.1", "Iron-carbon alloys and austenite transformations"), ("B5.2", "Classes of steel and cast iron"), ("B5.3", "Heat treatments of steel"), ("B5.4", "Surface hardening and modification"),
       ("B5.5", "Casting methods"), ("B5.6", "Hot working"), ("B5.7", "Bending and sheet-metal operations"), ("B5.8", "Welding"),
       ("B6.5", "Sintering and grain growth"), ("B6.6", "Dielectric properties of ceramics"), ("B6.7", "Diffusion and electrical conductivity in ceramics"),
       ("B7.1", "Chain architecture and dimensions"), ("B7.2", "Molar mass determination"), ("B7.3", "Polymer phase equilibria"), ("B7.4", "Polymer transitions and free volume"),
       ("B7.5", "Polymer crystallization"), ("B7.6", "Mechanical properties of polymers: viscoelasticity and rubber elasticity"), ("B7.7", "Polymer flow properties"),
       ("B7.8", "Polymer processing"),
       ("B8.4", "Dielectrics, polarization and optical behaviour"), ("B8.5", "Junctions and semiconductor devices"), ("B8.6", "Free electrons and Fermi-Dirac statistics"),
       ("B9.1", "Modelling and numerical analysis of materials processing"),
       ("B10.1", "Lithography"), ("B10.2", "Etching"), ("B10.3", "Physical, chemical and electrochemical deposition"), ("B10.4", "Oxidation"), ("B10.5", "Diffusion and ion implantation"),
       ("B10.6", "Yield and metrology"),
       ("B11.3", "Matrices and fillers: PMC, CMC, MMC"), ("B11.4", "Composite fabrication"), ("B11.5", "Composite failure modes"), ("B11.6", "Composite applications")]
_PE = [("1A", "Structures of metals, ceramics and polymers"), ("1B", "Diffusion and phase transformations"), ("1C", "Fractography"), ("1D", "Materials chemistry"),
       ("1E", "Microstructure and macrostructure"), ("1F", "Binary and ternary phase diagrams"), ("1G", "Non-equilibrium structures"),
       ("2A", "Environmental performance of metals"), ("2B", "Environmental performance of nonmetals"), ("2C", "Mechanical performance"), ("2D", "Thermal performance"),
       ("2E", "Wear and tribology"), ("2F", "Quality assurance"), ("2G", "Failure analysis"), ("2H", "Fitness for service and life prediction"), ("2I", "Material selection"),
       ("2J", "Lifecycle analysis"),
       ("3A", "Deformation processing"), ("3B", "Casting and molding"), ("3C", "Coating applications"), ("3D", "Cold work, stress relief and annealing"),
       ("3E", "Diffusion and thermal surface treatments"), ("3F", "Joining of metals and polymers"), ("3G", "Heat treatment and strengthening"), ("3H", "Powder processing"),
       ("3I", "Additive manufacturing"), ("3J", "Polymer and composite processing"),
       ("4A", "Structural analysis techniques"), ("4B", "Chemical analysis techniques"), ("4C", "Polymer characterization techniques"), ("4D", "Corrosion testing"),
       ("4E", "Characterization of coatings"), ("4F", "High-temperature behavior"), ("4G", "Low-temperature and cryogenic behavior"), ("4H", "Mechanical property evaluation"),
       ("4I", "Mechanical behavior of composites"), ("4J", "Physical properties")]
STDS = [{"id": "engineers-canada-materials", "name": "Engineers Canada Examination Syllabus: Materials Engineering (2021)", "publisher": "Engineers Canada", "kind": "exam-spec", "read": "part",
         "url": "https://engineerscanada.ca/become-an-engineer/examination-syllabi/materials-engineering-syllabus",
         "note": "Read Nov 2026 through an extraction of the syllabus page: all eighteen exams (A1-A7, B1-B11) with every topic their descriptions name. The page's own wording was not seen, so read: part. Items are those topics, grouped where one description runs several together, coded and titled by us. Recent-developments, emerging-technology and environmental-impact lines of B2-B4 are not itemised.",
         "items": [{"code": c, "title": t} for c, t in _EC]},
        {"id": "pe-metmat", "name": "NCEES PE Metallurgical and Materials CBT Exam Specifications (effective October 2024)", "publisher": "NCEES", "kind": "exam-spec", "read": "part",
         "url": "https://ncees.org/wp-content/uploads/2024/04/MetMat-Oct-2024.pdf",
         "note": "Read Nov 2026 through an extraction of the NCEES PDF: the four sections with their question ranges (Structure 11-17, Performance 23-35, Processing 19-29, Characterization and Properties 17-26) and all 37 lettered lines. The examples the specification may give under each line were not seen, so read: part. A professional exam: it sets breadth here, not depth.",
         "items": [{"code": c, "title": t} for c, t in _PE]}]
SKILLS = [("structure", "Unit cells, packing, density, Miller indices, interplanar spacing and diffraction", "Crystal structure", []),
          ("defects", "Vacancies, solid solutions, edge and screw dislocations, the Burgers circuit and vector, grain boundaries", "Defects and dislocations", ["mse.structure"]),
          ("deformation", "Slip systems, Schmid's law, strengthening mechanisms and the tensile curve", "Deformation and strengthening", ["mse.defects"]),
          ("diffusion", "Fick's laws, Arrhenius diffusivity and diffusion distance", "Diffusion in solids", ["mse.defects"]),
          ("phases", "Phase rule, lever rule, eutectics, the iron-carbon system, TTT diagrams, nucleation and heat treatment", "Phase diagrams and transformations", ["mse.diffusion"]),
          ("failure", "Fracture toughness, Griffith cracks, stress concentration, fatigue and creep", "Failure", ["mse.deformation"]),
          ("classes", "Ceramics, composites, electronic and magnetic behaviour, alloys, processing and characterisation", "Material classes and characterisation", ["mse.structure"]),
          ("thermo", "Heat balances, Ellingham diagrams, solution models, solidification and heat loss in processing", "Thermodynamics and transport in processing", ["mse.phases"]),
          ("service", "Material indices, life cycle, corrosion, oxidation, wear and protection", "Selection and degradation", ["mse.failure"]),
          ("polymers", "Chain dimensions, molar mass methods, transitions, crystallinity, viscoelasticity and flow", "Polymer structure and properties", ["mse.structure"]),
          ("extraction", "Mineral processing, pyrometallurgy, hydrometallurgy, electrometallurgy, iron and steelmaking", "Extraction and refining", ["mse.thermo"]),
          ("fabrication", "Steel heat treatments, surface hardening, casting, forming, welding, powder and additive routes", "Fabrication", ["mse.phases"]),
          ("functional", "Sintering, ionic conduction, dielectrics, optics, junctions, superconductors and microfabrication", "Functional materials and microfabrication", ["mse.classes"]),
          ("practice", "Composite classes, fabrication and failure, inspection, failure analysis and life prediction", "Composites and service practice", ["mse.failure"])]
IDEAS = [("LATTICE", "Structure sets what can move", "Which planes are densest and which directions are shortest decide how a crystal slips, diffracts and packs; everything else is counted from the unit cell."),
         ("DEFECT", "Properties live in the defects", "A perfect crystal would be a thousand times stronger and far less useful: vacancies carry diffusion, dislocations carry plastic flow, and every strengthening method is a way to pin a dislocation."),
         ("PATH", "Processing chooses the microstructure", "The phase diagram says where equilibrium is; cooling rate, cold work and heat treatment decide how far the material gets there, and so which phases and grain sizes it ends with.")]
PRACTICES = [("P1", "Compute", "Carry a geometric, rate or mechanical relation to a number with its unit."),
             ("P2", "Classify", "Name the structure, defect, mechanism or technique a description points to.")]
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
SK, DF, DE, DI, PH, FA, CL, TH, SV, PO, EX, FB, FN, PR = ["mse." + s[0] for s in SKILLS]
X = lambda *s: [f"engineers-canada-materials:{x}" for x in s]
E_ = lambda *s: [f"fe-mechanical:{x}" for x in s]
P_ = lambda *s: [f"pe-metmat:{x}" for x in s]
FD = "96485"
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


U1 = ("structure", "Crystal structure", X("A3.1", "A3.2") + E_("9A") + P_("1A", "4A"), ["LATTICE"], {
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

U2 = ("defects", "Defects and dislocations", X("A4.1", "A4.2", "B6.2") + P_("1A", "1E"), ["DEFECT"], {
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

U3 = ("deformation", "Deformation and strengthening", X("A4.1", "A4.2") + E_("9A", "9B") + P_("2C", "3D", "4H"), ["DEFECT"], {
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

U4 = ("diffusion", "Diffusion in solids", X("A5.4") + P_("1B"), ["DEFECT"], {
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
U5 = ("phases", "Phase diagrams and transformations", X("A1.1", "A5.1", "A5.2", "A5.3", "A5.5", "A5.6", "A5.7", "B5.1") + E_("9C", "9G") + P_("1B", "1F", "1G", "3G"), ["PATH"], {
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

U6 = ("failure", "Failure", X("A4.3", "A4.4", "A4.5", "A4.6") + E_("9J") + P_("1C", "2C", "4F", "4G"), ["DEFECT"], {
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
U7 = ("classes", "Material classes and characterisation", X("B6.1", "B6.3", "B6.4", "B8.1", "B8.2", "B8.3", "B11.1", "B11.2", "A3.2", "A3.3", "A3.4", "A3.5", "A4.7", "A4.8", "B4.1", "B5.2") + E_("9A", "9C", "9D", "9E", "9F") + P_("1D", "2D", "4A", "4B", "4I", "4J"), ["LATTICE", "PATH"], {
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


U8 = ("processing-thermo", "Thermodynamics and transport in processing", X("A1.2", "A1.3", "A1.4", "A1.5", "A1.6", "A2.1", "A2.2", "A2.3", "A2.4", "B9.1"), ["PATH"], {
   1: ("Thermochemistry of processes", [
     ("A", X("A1.2", "A1.6"), "Run a heat balance for heating and melting a charge.",
      "Q = m[c_p(T_m − T₀) + L_f]: sensible heat to the melting point plus latent heat. Furnace energy is this divided by the thermal efficiency.", "P1", [
       N("mse-melt-heat", TH, "A {{km}} kg charge with mean c_p = {{kc}} kJ/kg·K is heated from {{ko}} K to its melting point of {{kt}} K and melted (latent heat {{kl}} kJ/kg). Find the heat required in MJ.", "km*(kc*(kt - ko) + kl)/1000",
         "(km*integrate(kc, (Y, ko, kt)) + km*kl)/1000", "Sensible heat plus latent heat, then kJ to MJ", tex="Q",
         cases=C("km kc ko kt kl", [(1000, 0.90, 298, 933, 397), (500, 0.70, 298, 1811, 247), (200, 0.44, 298, 1358, 205), (50, 0.13, 298, 600, 23), (1000, 0.55, 298, 1728, 297)])),
       N("mse-melt-energy", TH, "A furnace melts a metal with mean c_p = {{kc}} kJ/kg·K from {{ko}} K at its melting point of {{kt}} K (latent heat {{kl}} kJ/kg) at {{kf}}% thermal efficiency. Find the electricity used in kWh per tonne.", "(kc*(kt - ko) + kl)*1000/3600/(kf/100)",
         f"solve(Eq({M}*kf/100*3600, (kc*(kt - ko) + kl)*1000), {M})[0]", "Heat per tonne in kJ, divided by 3600 for kWh and by the efficiency", tex="E",
         cases=C("kc ko kt kl kf", [(0.90, 298, 933, 397, 60), (0.70, 298, 1811, 247, 70), (0.44, 298, 1358, 205, 55), (0.90, 298, 933, 397, 85), (0.55, 298, 1728, 297, 65)]))]),
     ("B", X("A1.3"), "Compute a standard free energy of oxidation and where it changes sign.",
      "ΔG° = ΔH° − TΔS°. On an Ellingham diagram this is a line of slope −ΔS°; an oxide decomposes on heating above the temperature where its line crosses zero.", "P1", [
       N("mse-ellingham-dg", TH, "An oxidation, per mole of O₂, has ΔH° = {{kh}} kJ and ΔS° = {{ks}} J/K. Find ΔG° at {{kt}} K in kJ.", "kh - kt*ks/1000",
         "kh - integrate(ks/1000, (Y, 0, kt))", "Convert the entropy term to kJ before subtracting", tex="\\Delta G^\\circ",
         cases=C("kh ks kt", [(-529, -129, 1273), (-906, -176, 1500), (-223, 175, 1273), (-1117, -209, 1000), (-311, -138, 800)])),
       N("mse-ellingham-zero", TH, "An oxide forms, per mole of O₂, with ΔH° = {{kh}} kJ and ΔS° = {{ks}} J/K. Above what temperature in K does it decompose in oxygen at 1 atm?", "kh/ks*1000",
         f"solve(Eq(kh - {M}*ks/1000, 0), {M})[0]", "Set ΔG° to zero: T = ΔH° ÷ ΔS°", tex="T",
         cases=C("kh ks", [(-62, -133), (-182, -216), (-230, -200), (-290, -180), (-520, -195)]))]),
     ("C", X("A1.3", "A1.6"), "Decide from free energies of formation whether one metal reduces another's oxide.",
      "Compare the oxides per mole of O₂: the element whose oxide has the more negative ΔG° takes the oxygen. Carbon's line to CO slopes downward, so carbon reduces more oxides the hotter it gets.", "P1", [
       N("mse-reduction-dg", TH, "Per mole of O₂, metal A's oxide forms with ΔG° = {{ka}} kJ and metal B's with {{kb}} kJ. Find ΔG° for A reducing B's oxide, in kJ per mole of O₂.", "ka - kb",
         f"solve(Eq({M} + kb, ka), {M})[0]", "Form A's oxide and undo B's", tex="\\Delta G^\\circ",
         cases=C("ka kb", [(-850, -540), (-360, -850), (-450, -360), (-940, -700), (-355, -940)])),
       L("mse-reduction-feasible", TH, "Can the first reduce the second's oxide? Free energies of oxide formation are in kJ per mole of O₂. {{q}}", ["Yes: its oxide line lies lower", "No: its oxide line lies higher"], [
         ("Aluminium (−850) and chromium oxide (−540)", 0), ("Iron (−360) and alumina (−850)", 1), ("Carbon to CO at 1273 K (−450) and iron oxide (−360)", 0),
         ("Carbon to CO at 1273 K (−450) and alumina (−850)", 1), ("Magnesium (−940) and titanium dioxide (−700)", 0), ("Hydrogen to water (−355) and magnesia (−940)", 1)],
         "The lower line on the Ellingham diagram wins the oxygen")]),
     ("D", X("A1.4"), "Compute the entropy and enthalpy of mixing of a binary solution.",
      "Ideal mixing: ΔS = −R(x ln x + (1 − x) ln(1 − x)), largest at x = 0.5. A regular solution adds ΔH = Ωx(1 − x): positive Ω means like atoms prefer each other.", "P1", [
       N("mse-mixing-entropy", TH, "Find the ideal molar entropy of mixing of a binary solution with mole fraction {{kx}} of one component, in J/mol·K. (R = 8.314)", f"-{RG}*(kx*log(kx) + (1 - kx)*log(1 - kx))",
         f"{RGS}*(kx*log(1/kx) + (1 - kx)*log(1/(1 - kx)))", "Both logarithms are negative, so the entropy is positive", tex="\\Delta S",
         cases=C("kx", [(0.5,), (0.2,), (0.1,), (0.35,), (0.02,)])),
       N("mse-regular-enthalpy", TH, "A regular solution has interaction parameter Ω = {{ko}} kJ/mol. Find its molar enthalpy of mixing at a mole fraction of {{kx}}, in kJ/mol.", "ko*kx*(1 - kx)",
         "ko*kx - ko*kx**2", "Ω times the product of the two mole fractions", tex="\\Delta H",
         cases=C("ko kx", [(20, 0.5), (12, 0.3), (-15, 0.5), (25, 0.1), (8, 0.4)]))]),
     ("E", X("A1.4", "A1.5"), "Link a solution model to the shape of the phase diagram.",
      "Phases in equilibrium share a common tangent to their free-energy curves. A regular solution with Ω > 2RT has a double-welled curve and separates into two phases; the miscibility gap closes at T_c = Ω ÷ 2R.", "P1", [
       N("mse-miscibility-tc", TH, "A regular solution has Ω = {{ko}} J/mol. Find the temperature at the top of its miscibility gap, in K. (R = 8.314)", f"ko/(2*{RG})",
         f"solve(Eq(2*{RGS}*{M}, ko), {M})[0]", "T_c = Ω ÷ 2R", tex="T_c",
         cases=C("ko", [(20000,), (12500,), (30000,), (8000,), (16600,)])),
       L("mse-miscibility-gap", TH, "What does the regular-solution model predict? {{q}}", ["One solution at every composition", "A miscibility gap: two phases at middle compositions"], [
         ("Ω = 10 kJ/mol at 1000 K, where 2RT = 16.6 kJ/mol", 0), ("Ω = 25 kJ/mol at 1000 K, where 2RT = 16.6 kJ/mol", 1), ("Ω = 0, an ideal solution", 0),
         ("Ω = 20 kJ/mol at 600 K, where 2RT = 10.0 kJ/mol", 1), ("Ω = −15 kJ/mol: unlike atoms attract", 0)],
         "Compare Ω with 2RT")])]),
   2: ("Heat and flow in processing", [
     ("A", X("A2.1") + P_("3B"), "Estimate a casting's solidification time with Chvorinov's rule.",
      "t = B(V ÷ A)²: freezing time goes as the square of the volume-to-surface ratio (the casting modulus). A riser must have a larger modulus than the section it feeds.", "P1", [
       N("mse-chvorinov", TH, "A casting has volume {{kv}} cm³ and surface area {{ka}} cm², and the mould constant is {{kb}} min/cm². Find its solidification time in minutes.", "kb*(kv/ka)^2",
         "kb*exp(2*log(kv/ka))", "Square the modulus V ÷ A and scale by the mould constant", tex="t",
         cases=C("kv ka kb", [(1000, 600, 2.0), (8000, 2400, 3.0), (500, 550, 2.5), (2700, 1260, 4.0), (125, 150, 2.0)])),
       N("mse-chvorinov-ratio", TH, "A riser has a modulus of {{ka}} cm and the casting {{kb}} cm. Find the riser's freezing time as a percentage of the casting's.", "(ka/kb)^2*100",
         "100*ka**2/kb**2", "Times go as the square of the modulus; above 100% the riser stays liquid longer", tex="\\%",
         cases=C("ka kb", [(2.4, 2.0), (1.5, 1.8), (3.0, 2.5), (1.0, 2.0), (2.2, 2.0)]))]),
     ("B", X("A2.3"), "Compute radiant heat loss from a hot surface.",
      "q = εσA(T⁴ − T_s⁴), with σ = 5.670 × 10⁻⁸ W/m²·K⁴. Because of the fourth power, radiation dominates the heat loss of hot metal.", "P1", [
       N("mse-radiation-loss", TH, "A billet at {{kt}} K with emissivity {{kf}} and surface area {{ka}} m² faces surroundings at {{ks}} K. Find its net radiant heat loss in kW. (σ = 5.670374 × 10⁻⁸ W/m²·K⁴)", "kf*5.670374e-8*ka*(kt^4 - ks^4)/1000",
         "kf*Rational('5.670374e-8')*ka*(kt**2 - ks**2)*(kt**2 + ks**2)/1000", "Use absolute temperatures to the fourth power", tex="q",
         cases=C("kt kf ka ks", [(1400, 0.8, 2.0, 300), (1200, 0.6, 0.5, 300), (900, 0.3, 4.0, 320), (1600, 0.85, 1.2, 350), (700, 0.9, 3.0, 295)])),
       N("mse-radiation-ratio", TH, "A furnace wall radiates as a grey body. By what factor does its emitted power rise when its temperature goes from {{ka}} K to {{kb}} K?", "(kb/ka)^4",
         "exp(4*log(kb/ka))", "Emitted power goes as the fourth power of absolute temperature", tex="factor",
         cases=C("ka kb", [(1000, 1200), (800, 1600), (1500, 1650), (600, 900), (1273, 1473)]))]),
     ("C", X("A2.2", "B9.1"), "Use residence time for a ladle or tundish.",
      "Mean residence time τ = V ÷ Q. In a well-mixed vessel a step change washes out as exp(−t ÷ τ); plug flow would deliver it all at once after τ.", "P1", [
       N("mse-residence-time", TH, "A tundish holds {{kv}} m³ of steel and passes {{kq}} m³/min. Find the mean residence time in minutes.", "kv/kq",
         f"solve(Eq({M}*kq, kv), {M})[0]", "Volume over volumetric flow", tex="\\tau",
         cases=C("kv kq", [(4.0, 0.5), (6.3, 0.9), (2.5, 0.4), (8.0, 1.6), (3.3, 0.6)])),
       N("mse-washout", TH, "A well-mixed vessel has a mean residence time of {{kw}} min. What percent of the old grade is still in it {{kt}} min after the feed is switched?", "100*exp(-kt/kw)",
         "100/exp(kt/kw)", "A mixed vessel loses the old material exponentially", tex="\\%",
         cases=C("kw kt", [(8, 8), (7, 21), (5, 2), (10, 30), (6, 9)]))]),
     ("D", X("A2.1", "A2.4", "B9.1"), "Use the Biot number to choose a quench model.",
      "Bi = hL_c ÷ k compares surface convection with conduction inside. Below about 0.1 the part is nearly uniform and a lumped model works; above it, the inside lags and a conduction solution is needed.", "P1", [
       N("mse-biot", TH, "A part with characteristic length {{kl}} mm and conductivity {{kk}} W/m·K is quenched with h = {{kh}} W/m²·K. Find the Biot number.", "kh*kl/1000/kk",
         f"solve(Eq({M}*kk, kh*kl/1000), {M})[0]", "Convert the length to metres", tex="Bi",
         cases=C("kl kk kh", [(5, 200, 500), (25, 40, 2000), (2, 15, 800), (50, 50, 5000), (10, 400, 300)])),
       L("mse-lumped-valid", TH, "Is a lumped (uniform temperature) model acceptable? {{q}}", ["Yes: the part stays nearly uniform", "No: steep gradients form inside"], [
         ("Bi = 0.02", 0), ("Bi = 5", 1), ("A thin aluminium sheet in oil, Bi = 0.005", 0), ("A thick ceramic block in water, Bi = 40", 1), ("Bi = 0.09", 0), ("Bi = 0.6", 1)],
         "The usual limit is Bi under 0.1")])])})

U9 = ("service", "Selection and degradation", X("A6.1", "A6.2", "A6.3", "A6.4", "A6.5", "A7.1", "A7.2", "A7.3", "A7.4", "A7.5", "A7.6", "A7.7") + E_("9H", "9I") + P_("2A", "2B", "2E", "2I", "2J", "3C", "4D", "4E"), ["PATH"], {
   1: ("Selecting a material", [
     ("A", X("A6.1", "A6.3") + E_("9H") + P_("2I"), "Choose and compute a material index for a light, stiff or strong part.",
      "Translate the design: function, constraint, objective, free variable. A light stiff tie maximises E ÷ ρ, a beam E^½ ÷ ρ, a panel E^⅓ ÷ ρ; a light strong tie σ_y ÷ ρ.", "P1", [
       N("mse-beam-index", SV, "A material has E = {{kg}} GPa and density {{kd}} Mg/m³. Compute the light-stiff-beam index E^½ ÷ ρ.", "sqrt(kg)/kd",
         "exp(log(kg)/2)/kd", "Square root of the modulus, over the density", tex="M",
         cases=C("kg kd", [(210, 7.85), (70, 2.70), (110, 4.43), (150, 1.60), (12, 0.60)])),
       L("mse-index-choice", SV, "Which index should be made as large as possible? {{q}}", ["E over rho", "square root of E, over rho", "cube root of E, over rho", "yield strength over rho"], [
         ("A light, stiff tie rod in tension", 0), ("A light, stiff beam in bending", 1), ("A light, stiff flat panel in bending", 2), ("A light tie rod that must not yield", 3), ("A bicycle frame tube sized for bending stiffness", 1)],
         "Tension uses the property directly; bending rewards low density more, a panel most of all")]),
     ("B", X("A6.3") + P_("2I"), "Compare two materials by index and read a selection chart.",
      "For a tie of fixed stiffness the mass goes as ρ ÷ E. On a log-log property chart, materials on a line of slope set by the index perform equally; those above it are better.", "P1", [
       N("mse-tie-mass-ratio", SV, "A tie rod of fixed length and stiffness is made first of a material with E = {{ka}} GPa and ρ = {{kb}} Mg/m³, then of one with E = {{kc}} GPa and ρ = {{kd}} Mg/m³. Find the second rod's mass as a percentage of the first.", "(kd/kc)/(kb/ka)*100",
         "100*kd*ka/(kc*kb)", "Mass goes as ρ ÷ E for equal stiffness", tex="\\%",
         cases=C("ka kb kc kd", [(210, 7.85, 70, 2.70), (210, 7.85, 150, 1.60), (70, 2.70, 110, 4.43), (70, 2.70, 45, 1.74), (210, 7.85, 400, 15.6)])),
       F("mse-chart-facts", SV, [
         ("On a modulus-density chart with log axes, materials that give equally light stiff ties lie", "on a straight line of slope 1", "on a horizontal line", "on a vertical line", "on a circle"),
         ("On a modulus-density chart, the best candidates for light stiff parts are toward the", "upper left: high modulus, low density", "lower right", "lower left", "upper right only"),
         ("Steel, aluminium and titanium alloys have nearly the same E ÷ ρ, so for light stiff ties", "none of them beats the others, and composites or shape must do the work", "steel is always lightest", "aluminium is three times better", "titanium is useless"),
         ("In a selection, a property that must be met but is not optimised is", "a constraint", "an objective", "a free variable", "an index")],
         "Lines of equal index, then move toward the corner that raises it")]),
     ("C", X("A6.2"), "Compute a shape factor and say what limits it.",
      "Shape puts material far from the neutral axis. The elastic bending shape factor φ = 4πI ÷ A² is 1 for a solid round bar; for a tube it is (r_o² + r_i²) ÷ (r_o² − r_i²).", "P1", [
       N("mse-shape-factor", SV, "A tube has outer radius {{ko}} mm and inner radius {{kq}} mm. Find its bending shape factor φ = 4πI ÷ A².", "(ko^2 + kq^2)/(ko^2 - kq^2)",
         "4*pi*(pi*(ko**4 - kq**4)/4)/(pi*(ko**2 - kq**2))**2", "I = π(r_o⁴ − r_i⁴) ÷ 4 and A = π(r_o² − r_i²)", tex="\\varphi",
         cases=C("ko kq", [(20, 18), (25, 20), (10, 9), (50, 48), (30, 15)])),
       F("mse-shape-facts", SV, [
         ("A thin-walled tube is stiffer in bending than a solid bar of the same mass because", "its material sits farther from the neutral axis", "its modulus is higher", "it has more material", "it is longer"),
         ("What finally limits how thin a tube or I-beam wall can be made?", "Local buckling and what the process can form", "The modulus falls", "The density rises", "Nothing"),
         ("Wood and bamboo compete with metals in bending because", "low density and a natural tubular or cellular shape give a high index", "their modulus is higher than steel's", "they do not creep", "they are isotropic"),
         ("A material that cannot be extruded or rolled into thin sections", "cannot reach high shape factors, whatever its properties", "is always the best choice", "has an infinite shape factor", "must be cast as a solid sphere")],
         "Shape multiplies the material index, up to the limit of buckling and processing")]),
     ("D", X("A6.4", "A6.5") + P_("2J"), "Compute an embodied energy and name the stages of a life cycle assessment.",
      "Embodied energy is mass times the energy to make a kilogram, less with recycled content. An LCA sets a functional unit, then counts material production, manufacture, use and end of life.", "P1", [
       N("mse-embodied-energy", SV, "A {{km}} kg part is {{kp}}% recycled metal ({{kq}} MJ/kg) and the rest virgin ({{kv}} MJ/kg). Find its embodied energy in MJ.", "km*((1 - kp/100)*kv + kp/100*kq)",
         "km*kv - km*(kp/100)*(kv - kq)", "Weight the two energies by their mass fractions", tex="E",
         cases=C("km kp kq kv", [(10, 40, 25, 210), (2.5, 0, 25, 210), (100, 60, 9, 32), (5, 30, 250, 600), (20, 90, 25, 210)])),
       F("mse-lca-facts", SV, [
         ("An LCA compares products on the basis of", "a functional unit: the same service delivered", "one kilogram of each", "their purchase price", "their colour"),
         ("For a car, the largest share of life-cycle energy is usually", "the use phase, so saving mass pays back", "making the materials", "final disposal", "transport to the dealer"),
         ("Recycling aluminium rather than smelting it saves roughly", "nine tenths of the energy", "one tenth of the energy", "nothing", "half the mass"),
         ("Which material class is hardest to recycle back into the same grade?", "Thermoset composites", "Aluminium", "Steel", "Copper"),
         ("Cradle-to-gate differs from cradle-to-grave in leaving out", "use and end of life", "mining", "smelting", "all transport")],
         "Fix the function first; then count every stage")])]),
   2: ("Degradation and protection", [
     ("A", X("A7.2", "A7.3") + E_("9I") + P_("2A"), "Find the cell voltage of a galvanic couple and which metal corrodes.",
      "The metal with the lower (more negative) potential is the anode and corrodes; the emf is E_cathode − E_anode. A small anode joined to a large cathode corrodes fastest.", "P1", [
       N("mse-galvanic-emf", SV, "Two metals with standard potentials {{kc}} V and {{ka}} V are coupled in an electrolyte. Find the standard cell emf in volts.", "kc - ka",
         f"solve(Eq(ka + {M}, kc), {M})[0]", "Cathode potential minus anode potential", tex="E",
         cases=C("kc ka", [(0.34, -0.76), (0.34, -0.44), (0.80, -0.25), (-0.44, -0.76), (0.34, -1.66)])),
       L("mse-galvanic-anode", SV, "Which one corrodes? {{q}}", ["The first", "The second"], [
         ("A steel bolt in a copper plate, in seawater", 0), ("The zinc coating and the steel under a scratch", 0), ("A copper pipe joined to an aluminium fitting", 1),
         ("A passive stainless fastener in an aluminium hull", 1), ("A magnesium block wired to a buried steel tank", 0), ("A tin coating and the steel under a scratch, in aerated water", 1)],
         "The more active metal of the pair is the anode")]),
     ("B", X("A7.3"), "Apply the Nernst equation to a metal electrode.",
      "E = E° + (0.0592 ÷ n) log[Mⁿ⁺] at 25 °C: a metal in a dilute solution of its ions is more active, which is what drives a concentration cell.", "P1", [
       N("mse-nernst-metal", SV, "A metal with E° = {{ko}} V and n = {{kn}} sits in a {{kc}} M solution of its ions at 25 °C. Find its electrode potential in volts.", "ko + 0.0592/kn*log10(kc)",
         "ko + Rational('0.0592')/kn*log(kc, 10)", "The logarithm is negative for a dilute solution, so the potential drops", tex="E",
         cases=C("ko kn kc", [(0.34, 2, 0.01), (-0.44, 2, 0.001), (-0.76, 2, 0.1), (0.80, 1, 0.005), (-0.25, 2, 0.0001)])),
       N("mse-nernst-concentration", SV, "A metal with E° = {{ko}} V and n = {{kn}} shows an electrode potential of {{kv}} V at 25 °C. Find the concentration of its ions in mol/L.", "10^((kv - ko)*kn/0.0592)",
         "exp(log(10)*(kv - ko)*kn/Rational('0.0592'))", "Solve the Nernst equation for the logarithm, then raise ten to it", tex="[M]",
         cases=C("ko kn kv", [(0.34, 2, 0.281), (-0.44, 2, -0.529), (-0.76, 2, -0.790), (0.80, 1, 0.682), (-0.25, 2, -0.309)]))]),
     ("C", X("A7.3") + P_("4D"), "Compute a corrosion rate from weight loss and from current density.",
      "Penetration in mm/yr = 87.6W ÷ (ρAt), with W in mg, ρ in g/cm³, A in cm², t in hours. By Faraday's law a corrosion current density i removes iM ÷ (nFρ) of depth per second.", "P1", [
       N("mse-corrosion-weight-loss", SV, "A coupon of density {{kd}} g/cm³ and area {{ka}} cm² loses {{kw}} mg in {{kt}} h. Find the corrosion rate in mm/yr.", "87.6*kw/(kd*ka*kt)",
         "(kw/1000/kd/ka*10)/(kt/Rational(8760))", "Volume lost over area gives depth; scale the exposure to a year", tex="CPR",
         cases=C("kd ka kw kt", [(7.87, 25, 120, 720), (2.70, 40, 15, 2000), (8.94, 10, 6, 500), (7.9, 65, 485, 8760), (7.14, 30, 300, 1000)])),
       N("mse-corrosion-current", SV, "A metal (M = {{km}} g/mol, n = {{kn}}, ρ = {{kd}} g/cm³) corrodes at a current density of {{kj}} µA/cm². Find the penetration rate in mm/yr. (F = 96485 C/mol)", f"kj*1e-6*km/(kn*{FD}*kd)*10*31536000",
         f"solve(Eq({M}*kn*{FD}*kd, kj*km*Rational('1e-6')*10*31536000), {M})[0]", "Moles per area per second from Faraday, to depth, to a year", tex="r",
         cases=C("km kn kd kj", [(55.85, 2, 7.87, 10), (65.38, 2, 7.14, 50), (26.98, 3, 2.70, 2), (63.55, 2, 8.94, 100), (58.69, 2, 8.90, 1)]))]),
     ("D", X("A7.3", "A7.2"), "Read the active, passive and transpassive regions of a polarization curve.",
      "A passive metal (stainless steel, aluminium, titanium) forms a thin oxide film and its corrosion current falls by orders of magnitude as the potential rises; at higher potential still the film breaks down. Chlorides break the film locally and cause pitting.", "P2", [
       L("mse-passivity-region", SV, "Which region of the polarization curve? {{q}}", ["Active", "Passive", "Transpassive"], [
         ("Current density rises steadily with potential and bare metal dissolves", 0), ("Current density is very low and nearly constant over a wide range of potential", 1),
         ("At high potential the current rises again as the film breaks down", 2), ("Stainless steel in aerated dilute nitric acid, covered by its film", 1), ("Stainless steel in a reducing acid with no oxidiser", 0)],
         "Dissolving, protected by a film, or film breaking down"),
       F("mse-passivity-facts", SV, [
         ("Stainless steel resists corrosion because of", "a thin, self-healing chromium oxide film", "its high carbon content", "a thick iron oxide scale", "its nickel alone"),
         ("Chloride ions attack passive alloys mainly by", "breaking the film locally, giving pits", "thickening the film", "uniform dissolution only", "raising the pH"),
         ("Crevice corrosion starts because the liquid inside a crevice", "runs out of oxygen and turns acidic", "is richer in oxygen", "is flowing fast", "is colder"),
         ("Weld decay in austenitic stainless steel comes from", "chromium carbides at grain boundaries leaving the neighbouring metal short of chromium", "too much nickel", "martensite", "graphite flakes"),
         ("Concentration polarization sets a limiting current because", "the reacting species cannot reach the surface any faster", "the metal runs out", "the film is too thick", "the temperature is too high")],
         "A film a few nanometres thick is the whole defence")]),
     ("E", X("A7.1") + P_("2A", "4F"), "Compute a Pilling-Bedworth ratio and judge the oxide scale.",
      "P-B ratio = volume of oxide formed ÷ volume of metal consumed = (M_oxide ρ_metal) ÷ (n M_metal ρ_oxide). Under 1 the scale is porous; 1 to 2 protective; well above 2 it cracks and spalls. A protective scale grows parabolically.", "P1", [
       N("mse-pilling-bedworth", SV, "An oxide of molar mass {{km}} g/mol and density {{kp}} g/cm³ contains {{kn}} metal atoms per formula; the metal has molar mass {{ka}} g/mol and density {{kd}} g/cm³. Find the Pilling-Bedworth ratio.", "km*kd/(kn*ka*kp)",
         "(km/kp)/(kn*ka/kd)", "Molar volume of oxide over the molar volume of the metal it used", tex="PB",
         cases=C("km kp kn ka kd", [(101.96, 3.97, 2, 26.98, 2.70), (40.30, 3.58, 1, 24.31, 1.74), (71.85, 5.70, 1, 55.85, 7.87), (151.99, 5.22, 2, 52.00, 7.19), (74.69, 6.67, 1, 58.69, 8.90)])),
       L("mse-scale-protective", SV, "How does an oxide scale with this Pilling-Bedworth ratio behave? {{q}}", ["Porous and unprotective", "Protective", "Likely to crack and spall"], [
         ("0.81 (magnesium)", 0), ("1.28 (aluminium)", 1), ("3.3 (tungsten)", 2), ("1.70 (nickel)", 1), ("0.45 (potassium)", 0), ("2.5 (niobium)", 2), ("2.0 (chromium)", 1)],
         "Too little oxide leaves gaps; too much builds stress")]),
     ("F", X("A7.4") + P_("2A"), "Tell stress-corrosion cracking, hydrogen embrittlement and corrosion fatigue apart.",
      "SCC needs a tensile stress, a susceptible alloy and a specific environment together. Hydrogen embrittlement comes from atomic hydrogen entering high-strength steel. Corrosion fatigue removes the fatigue limit.", "P2", [
       L("mse-stress-corrosion-type", SV, "Which failure mode? {{q}}", ["Stress-corrosion cracking", "Hydrogen embrittlement", "Corrosion fatigue"], [
         ("Cold-worked brass cracks in an ammonia atmosphere under residual stress", 0), ("A high-strength steel bolt fails days after electroplating, with no load cycling", 1),
         ("A ship's propeller shaft cracks in seawater under cyclic bending below its fatigue limit in air", 2), ("Austenitic stainless steel cracks in hot chloride solution under steady tension", 0),
         ("A welded high-strength steel cracks hours after welding with damp electrodes", 1), ("An aircraft skin in a salt environment cracks from pits under pressure cycles", 2)],
         "Steady stress with a specific environment, hydrogen from a process, or cycles in a corrosive medium"),
       F("mse-stress-corrosion-facts", SV, [
         ("Stress-corrosion cracking requires", "tensile stress, a susceptible alloy and a specific environment together", "only a corrosive environment", "only a high stress", "cyclic loading"),
         ("Baking a plated high-strength steel part at about 200 °C serves to", "drive out hydrogen before it causes cracking", "harden the plating", "temper the steel", "remove chloride"),
         ("In a corrosive environment the S-N curve of steel", "loses its fatigue limit", "rises", "is unchanged", "becomes vertical"),
         ("Which reduces the risk of stress-corrosion cracking?", "Stress relief or shot peening to remove surface tension", "Increasing the residual tensile stress", "Using a higher-strength temper", "Adding chloride")],
         "Remove any one of stress, susceptible alloy or environment and SCC stops")]),
     ("G", X("A7.5", "A7.6", "A7.7") + P_("3C", "4E"), "Choose a protection method and size a sacrificial anode.",
      "Cathodic protection makes the structure the cathode, by a sacrificial anode (Zn, Mg, Al) or an impressed current. Anodic protection holds a passivating alloy in its passive range. Coatings are barriers; inhibitors slow the anodic or cathodic reaction. Anode mass consumed is ItM ÷ nF.", "P1", [
       N("mse-anode-mass", SV, "A sacrificial anode (M = {{km}} g/mol, n = {{kn}}) supplies {{kj}} A for {{ky}} years. Find the mass consumed in kg, assuming all its current is useful. (F = 96485 C/mol)", f"kj*ky*31536000*km/(kn*{FD})/1000",
         f"solve(Eq({M}*1000*kn*{FD}, kj*ky*31536000*km), {M})[0]", "Charge passed, to moles by Faraday, to mass", tex="m",
         cases=C("km kn kj ky", [(65.38, 2, 0.5, 10), (24.31, 2, 0.2, 5), (26.98, 3, 2.0, 15), (65.38, 2, 0.05, 20), (24.31, 2, 1.0, 3)])),
       L("mse-protection-method", SV, "Which protection method is this? {{q}}", ["Sacrificial anode", "Impressed current", "Barrier coating", "Inhibitor"], [
         ("Zinc blocks bolted to a ship's hull", 0), ("A rectifier drives current from inert anodes to a buried pipeline", 1), ("Epoxy paint on structural steel", 2),
         ("Chromate or phosphate added to cooling water", 3), ("Galvanized steel after the zinc layer is scratched through", 0), ("A vapour-phase chemical in the packaging of machined parts", 3)],
         "Make it the cathode, cover it, or slow the reaction")]),
     ("H", X("A7.1") + P_("2B"), "Describe how polymers and ceramics degrade.",
      "Polymers swell or dissolve in chemically similar liquids, and their chains are cut by UV, heat, oxygen and hydrolysis. Ceramics are already oxides and resist corrosion, but dissolve in molten slags and, for silicates, in hydrofluoric acid and strong alkali.", "P2", [
       L("mse-nonmetal-degradation", SV, "Which mechanism? {{q}}", ["Swelling or dissolution", "Chain scission", "Chemical attack on a ceramic"], [
         ("A rubber seal softens and grows in size in petrol", 0), ("A polypropylene chair turns chalky and brittle after years in sunlight", 1), ("A furnace lining is eaten away by basic slag", 2),
         ("A polyester loses strength in hot water as its ester links hydrolyse", 1), ("A glass bottle is etched by hydrofluoric acid", 2), ("Polystyrene dissolves in acetone", 0)],
         "Liquid entering between chains, chains being cut, or a ceramic reacting"),
       F("mse-nonmetal-degradation-facts", SV, [
         ("Carbon black is added to rubber and polyethylene partly to", "absorb ultraviolet light and slow chain scission", "raise the melting point", "make it conduct heat", "lower the density"),
         ("A polymer is most likely to swell in a liquid that is", "chemically similar to it", "water, always", "a strong acid, always", "more dense than it"),
         ("Ozone attacks rubber by", "breaking the double bonds in the chain, giving cracks under tension", "dissolving the filler", "raising the glass transition", "crystallising it"),
         ("An acid refractory such as silica brick must not be used against", "a basic slag", "an acid slag", "air", "nitrogen")],
         "Like dissolves like; light and heat break chains; acid and base ceramics react")]),
     ("I", P_("2E"), "Compute wear volume with Archard's law and name the wear modes.",
      "V = KFs ÷ H: wear volume grows with load and sliding distance and falls with hardness; K is a dimensionless wear coefficient found by test.", "P1", [
       N("mse-archard", SV, "A pin of hardness {{kh}} MPa slides {{kd}} m under {{kf}} N with a wear coefficient of {{kk}} × 10⁻⁴. Find the wear volume in mm³.", "kk*1e-4*kf*kd*1000/kh",
         f"solve(Eq({M}*kh, kk*kf*kd/10), {M})[0]", "N·m over MPa is 10⁻⁶ m³, which is 1000 mm³", tex="V",
         cases=C("kh kd kf kk", [(1500, 1000, 50, 1.0), (800, 5000, 20, 5.0), (6000, 2000, 100, 0.2), (2500, 300, 200, 10), (1200, 10000, 5, 2.0)])),
       F("mse-wear-modes", SV, [
         ("Hard particles ploughing grooves in a softer surface is", "abrasive wear", "adhesive wear", "fretting", "cavitation erosion"),
         ("Surfaces welding at asperities and tearing material across is", "adhesive wear (galling)", "abrasive wear", "erosion", "corrosion"),
         ("Damage from tiny oscillating slip between clamped parts is", "fretting", "abrasion", "erosion", "creep"),
         ("Damage from collapsing vapour bubbles on a pump impeller is", "cavitation erosion", "fretting", "galling", "abrasion"),
         ("By Archard's law, doubling the surface hardness", "halves the wear volume", "doubles the wear volume", "has no effect", "quarters the wear volume")],
         "Ploughing, welding and tearing, micro-slip, or bubbles")])])})

U10 = ("polymers", "Polymer structure and properties", X("B7.1", "B7.2", "B7.3", "B7.4", "B7.5", "B7.6", "B7.7", "B7.8") + P_("1A", "3J", "4C"), ["LATTICE", "PATH"], {
   1: ("Chains, transitions and flow", [
     ("A", X("B7.1"), "Compute the size of a random-coil chain.",
      "A freely jointed chain of n links of length l has root-mean-square end-to-end distance l√n, far shorter than its contour length nl. That gap is why rubber can stretch several hundred percent.", "P1", [
       N("mse-chain-rms", PO, "A freely jointed chain has {{kn}} links, each {{kl}} nm long. Find its root-mean-square end-to-end distance in nm.", "kl*sqrt(kn)",
         f"Max(*solve(Eq({M}**2, kn*kl**2), {M}))", "A random walk: the mean square distance is n l²", tex="R",
         cases=C("kn kl", [(10000, 0.154), (2500, 0.154), (400, 0.5), (40000, 0.154), (900, 0.3)])),
       N("mse-chain-extension", PO, "A freely jointed chain has {{kn}} links, each {{kl}} nm long. How many times longer is its fully extended length than its root-mean-square end-to-end distance?", "sqrt(kn)",
         "(kn*kl)/(kl*sqrt(kn))", "Contour length n l over l√n", tex="ratio",
         cases=C("kn kl", [(10000, 0.154), (2500, 0.154), (400, 0.5), (40000, 0.154), (900, 0.3)]))]),
     ("B", X("B7.2") + P_("4C"), "Match a molar-mass method to the average it gives and use the Mark-Houwink relation.",
      "Colligative methods (osmometry, end-group analysis) count molecules and give M_n; light scattering weights by size and gives M_w; viscometry gives M_v through [η] = K Mᵃ; gel permeation chromatography gives the whole distribution.", "P1", [
       L("mse-molar-mass-method", PO, "What does this method measure? {{q}}", ["Number-average molar mass", "Weight-average molar mass", "Viscosity-average molar mass", "The whole distribution"], [
         ("Membrane osmometry", 0), ("Static light scattering", 1), ("Capillary viscometry", 2), ("Gel permeation (size-exclusion) chromatography", 3), ("End-group titration", 0)],
         "Counting molecules gives the number average; scattering favours the big ones"),
       N("mse-mark-houwink", PO, "A polymer in solution obeys [η] = K Mᵃ with K = {{kk}} × 10⁻⁴ dL/g and a = {{ka}}. Its intrinsic viscosity is {{kh}} dL/g. Find its viscosity-average molar mass in g/mol.", "(kh/(kk*1e-4))^(1/ka)",
         "exp(log(kh/(kk*Rational('1e-4')))/ka)", "Divide by K, then take the 1 ÷ a power", tex="M_v",
         cases=C("kk ka kh", [(1.1, 0.725, 0.80), (3.8, 0.63, 0.50), (0.9, 0.74, 1.50), (1.2, 0.71, 0.30), (5.0, 0.60, 1.00)]))]),
     ("C", X("B7.3"), "Use the Flory-Huggins parameter to judge solvent quality.",
      "χ measures polymer-solvent contact energy. Below 0.5 the solvent is good and coils swell; at 0.5 (the theta condition) they are ideal; above it the polymer separates. For a chain of N segments the critical value is ½(1 + 1 ÷ √N)².", "P1", [
       N("mse-flory-critical", PO, "A polymer has {{kn}} segments per chain. Find the critical Flory-Huggins parameter χ_c = ½(1 + 1 ÷ √N)².", "0.5*(1 + 1/sqrt(kn))^2",
         "Rational(1, 2)*(1 + 2/sqrt(kn) + 1/kn)", "Longer chains bring χ_c down toward one half, so they separate more easily", tex="\\chi_c",
         cases=C("kn", [(100,), (1000,), (25,), (10000,), (400,)])),
       L("mse-solvent-quality", PO, "For a long polymer chain, what is the solvent? {{q}}", ["A good solvent: coils swell", "A theta solvent: coils are ideal", "A poor solvent: the polymer separates"], [
         ("χ = 0.30", 0), ("χ = 0.50", 1), ("χ = 0.80", 2), ("χ = 0.45", 0), ("χ = 1.2", 2), ("The temperature at which the second virial coefficient is zero", 1)],
         "One half is the dividing line")]),
     ("D", X("B7.4"), "Estimate a glass transition temperature and say what moves it.",
      "For a miscible blend or random copolymer the Fox equation gives 1 ÷ T_g = w₁ ÷ T_g1 + w₂ ÷ T_g2 (kelvin). T_g rises with chain stiffness, bulky or polar side groups and crosslinking, and falls with plasticizer and free volume.", "P1", [
       N("mse-fox-tg", PO, "A miscible blend is {{kw}} weight fraction of a polymer with T_g = {{ka}} K, the rest one with T_g = {{kb}} K. Estimate the blend's T_g in K with the Fox equation.", "1/(kw/ka + (1 - kw)/kb)",
         f"solve(Eq({M}*(kw/ka + (1 - kw)/kb), 1), {M})[0]", "Add the weighted reciprocals, then invert", tex="T_g",
         cases=C("kw ka kb", [(0.5, 373, 233), (0.3, 378, 263), (0.8, 354, 188), (0.25, 423, 373), (0.6, 300, 200)])),
       F("mse-tg-facts", PO, [
         ("Adding a plasticizer to PVC", "lowers its glass transition by adding free volume between chains", "raises its glass transition", "crosslinks it", "makes it crystalline"),
         ("Which change raises a polymer's glass transition temperature?", "A stiffer backbone or bulky side groups", "More plasticizer", "Shorter chains", "More chain ends"),
         ("Polystyrene has a much higher T_g than polyethylene because", "its bulky phenyl side groups hinder rotation", "its chains are shorter", "it is more crystalline", "it has no side groups"),
         ("Light crosslinking of a rubber", "raises T_g slightly and stops the chains flowing", "lowers T_g sharply", "makes it melt at lower temperature", "has no effect"),
         ("The free-volume picture says that at T_g", "the unoccupied volume has fallen too low for chain segments to move", "the chains break", "the polymer crystallises", "the density jumps")],
         "Anything that makes segments harder to move raises T_g")]),
     ("E", X("B7.5") + P_("1A"), "Compute percent crystallinity from density.",
      "% crystallinity = ρ_c(ρ_s − ρ_a) ÷ [ρ_s(ρ_c − ρ_a)] × 100, a mass fraction from the specimen, fully crystalline and fully amorphous densities. Regular, linear chains cooled slowly crystallise most.", "P1", [
       N("mse-crystallinity", PO, "A polymer specimen has density {{ks}} g/cm³; the fully crystalline and fully amorphous densities are {{kc}} and {{ka}} g/cm³. Find the percent crystallinity by mass.", "kc*(ks - ka)/(ks*(kc - ka))*100",
         f"solve(Eq(1/ks, {M}/100/kc + (1 - {M}/100)/ka), {M})[0]", "Specific volumes add by mass fraction", tex="\\%",
         cases=C("ks kc ka", [(0.925, 0.998, 0.870), (0.955, 0.998, 0.870), (1.400, 1.450, 1.335), (0.904, 0.946, 0.853), (1.152, 1.242, 1.091)])),
       F("mse-crystallinity-facts", PO, [
         ("Which polymer crystallises most readily?", "Linear polyethylene", "Atactic polystyrene", "A heavily crosslinked epoxy", "A random copolymer"),
         ("Branching in polyethylene", "lowers crystallinity and density", "raises crystallinity", "has no effect on density", "makes it a thermoset"),
         ("Polymer crystals grow as", "chain-folded lamellae that gather into spherulites", "single extended chains only", "cubic grains with dislocations", "martensite plates"),
         ("Compared with the amorphous form, a more crystalline polymer is", "denser, stiffer and less transparent", "less dense", "more rubbery", "more soluble"),
         ("Quenching a crystallisable polymer from the melt gives", "lower crystallinity than slow cooling", "higher crystallinity", "a single crystal", "a crosslinked network")],
         "Regular chains with time to fold crystallise")]),
     ("F", X("B7.6"), "Use the Maxwell model and tell creep from stress relaxation.",
      "A Maxwell element (spring and dashpot in series) held at fixed strain relaxes as σ = σ₀ exp(−t ÷ τ), with relaxation time τ = η ÷ E. Creep is strain growing under constant stress; stress relaxation is stress falling at constant strain.", "P1", [
       N("mse-maxwell-relaxation", PO, "A Maxwell element with E = {{kg}} GPa and η = {{kv}} GPa·s is stretched until the stress is {{ko}} MPa and held. Find the stress after {{kt}} s, in MPa.", "ko*exp(-kt*kg/kv)",
         "ko/exp(kt/(kv/kg))", "The relaxation time is η ÷ E", tex="\\sigma",
         cases=C("kg kv ko kt", [(2, 100, 10, 25), (1, 500, 5, 500), (3, 60, 20, 10), (0.5, 200, 2, 1000), (2, 40, 8, 60)])),
       L("mse-viscoelastic-test", PO, "Which viscoelastic response is described? {{q}}", ["Stress relaxation", "Creep", "Elastic recovery"], [
         ("A gasket is clamped to a fixed thickness and its sealing force falls over months", 0), ("A plastic shelf sags more each year under the same books", 1),
         ("A stretched strip springs back when released", 2), ("A guitar string of nylon goes flat although its length is fixed", 0), ("A pipe under constant pressure slowly grows in diameter", 1)],
         "Fixed strain and falling stress, or fixed stress and growing strain")]),
     ("G", X("B7.6"), "Compute a rubber's modulus and a time-temperature shift.",
      "Rubber elasticity is entropic: G = ρRT ÷ M_c, rising with temperature and crosslink density. The WLF equation log a_T = −17.44(T − T_g) ÷ (51.6 + T − T_g) shifts a relaxation time from T_g to T.", "P1", [
       N("mse-rubber-modulus", PO, "A rubber of density {{kp}} kg/m³ has {{km}} g/mol between crosslinks. Find its shear modulus at {{kt}} K in MPa. (R = 8.314)", f"kp*{RG}*kt/(km/1000)/1e6",
         f"solve(Eq({M}*10**6*km/1000, kp*{RGS}*kt), {M})[0]", "Convert M_c to kg/mol; the result is in pascals", tex="G",
         cases=C("kp km kt", [(920, 5000, 298), (950, 10000, 300), (1100, 2500, 350), (900, 8000, 273), (1200, 4000, 320)])),
       N("mse-wlf", PO, "A polymer has T_g = {{kg}} K. Find the WLF shift factor log₁₀ a_T at {{kt}} K, using log a_T = −17.44(T − T_g) ÷ (51.6 + T − T_g).", "-17.44*(kt - kg)/(51.6 + kt - kg)",
         "-Rational('17.44')/(Rational('51.6')/(kt - kg) + 1)", "A negative value: relaxation is faster above T_g", tex="\\log a_T",
         cases=C("kg kt", [(373, 393), (200, 250), (378, 428), (233, 298), (350, 360)]))]),
     ("H", X("B7.7"), "Use the power law for a polymer melt's viscosity.",
      "Polymer melts shear thin: η = K γ̇ⁿ⁻¹ with n below 1, because chains disentangle and align. n = 1 is Newtonian.", "P1", [
       N("mse-power-law-viscosity", PO, "A melt follows η = K γ̇ⁿ⁻¹ with K = {{kk}} Pa·sⁿ and n = {{kn}}. Find its viscosity at a shear rate of {{kr}} per second, in Pa·s.", "kk*kr^(kn - 1)",
         "kk*exp((kn - 1)*log(kr))", "The exponent n − 1 is negative for a shear-thinning melt", tex="\\eta",
         cases=C("kk kn kr", [(10000, 0.4, 100), (5000, 0.6, 1000), (20000, 0.3, 10), (800, 0.8, 500), (15000, 0.5, 2500)])),
       L("mse-flow-class", PO, "Classify the fluid by its power-law index: {{q}}", ["Shear thinning", "Newtonian", "Shear thickening"], [
         ("n = 0.4, a polyethylene melt", 0), ("n = 1.0, water", 1), ("n = 1.5, a dense cornstarch suspension", 2), ("n = 0.7", 0), ("viscosity independent of shear rate", 1), ("viscosity rises as it is stirred faster", 2)],
         "Below one thins, one is Newtonian, above one thickens")]),
     ("I", X("B7.8") + P_("3J"), "Match a polymer part to its process.",
      "Injection moulding makes complex solid parts in a closed mould; extrusion makes continuous sections; blow moulding makes hollow containers from a tube of melt; compression moulding and casting suit thermosets, which cannot be remelted.", "P2", [
       L("mse-polymer-process", PO, "Which process makes this? {{q}}", ["Injection moulding", "Extrusion", "Blow moulding", "Compression moulding"], [
         ("A drinks bottle", 2), ("PVC pipe by the kilometre", 1), ("A phone case with snap fits", 0), ("A thermoset electrical socket", 3), ("Insulation coated onto a wire", 1), ("A gear with fine teeth in nylon", 0)],
         "Closed mould, continuous die, inflated tube, or pressed charge"),
       F("mse-polymer-process-facts", PO, [
         ("A thermoset cannot be recycled by remelting because", "its chains are permanently crosslinked", "it has no carbon", "it is too crystalline", "its T_g is below room temperature"),
         ("Thermoplastics are processed", "above their melting or glass transition temperature, then cooled", "by sintering powder only", "by quenching to form martensite", "only by machining"),
         ("Drawing a polymer fibre or film raises its strength along the draw direction because", "the chains align", "the chains break", "it becomes amorphous", "crosslinks form"),
         ("Vulcanising rubber with sulphur", "crosslinks the chains so it recovers its shape", "plasticises it", "makes it a thermoplastic", "raises its crystallinity to 100%")],
         "Thermoplastics flow when hot; thermosets set once")])])})

U11 = ("extraction", "Extraction and refining", X("B1.1", "B1.2", "B1.3", "B1.4", "B1.5", "B2.1", "B2.2", "B2.3", "B2.4", "B3.1", "B3.2", "B3.3", "B3.4", "B3.5", "B4.2", "B4.3", "B4.4", "A1.6"), ["PATH"], {
   1: ("From ore to metal", [
     ("A", X("B2.1"), "Compute grinding energy with Bond's law and order the mineral-processing steps.",
      "W = 10 W_i (1 ÷ √P₈₀ − 1 ÷ √F₈₀) kWh per tonne, with sizes in micrometres. Ore is crushed and ground to free the mineral, classified, concentrated (often by flotation), then dewatered.", "P1", [
       N("mse-bond-energy", EX, "An ore with Bond work index {{kw}} kWh/t is ground from an 80%-passing size of {{kf}} µm to {{kp}} µm. Find the energy needed in kWh per tonne.", "10*kw*(1/sqrt(kp) - 1/sqrt(kf))",
         "kw*(10/kp**Rational(1, 2) - 10/kf**Rational(1, 2))", "Finer product means a much larger first term", tex="W",
         cases=C("kw kf kp", [(13, 10000, 100), (15, 2500, 64), (11, 6400, 144), (18, 12100, 81), (9, 900, 49)])),
       F("mse-mineral-processing-facts", EX, [
         ("The purpose of grinding an ore is to", "liberate the valuable mineral grains from the gangue", "reduce the metal chemically", "melt the ore", "remove sulphur"),
         ("In froth flotation the valuable sulphide particles are collected because", "a collector makes them water-repellent, so they attach to air bubbles", "they are magnetic", "they are the densest particles", "they dissolve"),
         ("Which order is right?", "Crush, grind, classify, concentrate, dewater", "Concentrate, crush, dewater, grind, classify", "Dewater, grind, crush, classify, concentrate", "Grind, crush, concentrate, classify, dewater"),
         ("Grinding is the most energy-hungry step of mineral processing because", "energy per tonne rises steeply as the product gets finer", "the ore must be melted", "it uses reagents", "it runs dry"),
         ("Magnetite ore is most simply concentrated by", "magnetic separation", "cyanide leaching", "flotation with xanthate only", "electrowinning")],
         "Free the mineral first, then separate it by a property the gangue lacks")]),
     ("B", X("B2.1", "B2.4"), "Compute recovery and concentration ratio from assays.",
      "A two-product balance on feed f, concentrate c and tailing t (assays in %): C ÷ F = (f − t) ÷ (c − t), and recovery = c(f − t) ÷ [f(c − t)] × 100.", "P1", [
       N("mse-flotation-recovery", EX, "A flotation plant treats feed at {{kf}}% metal, making concentrate at {{kc}}% and tailing at {{kt}}%. Find the metal recovery in percent.", "kc*(kf - kt)/(kf*(kc - kt))*100",
         f"solve([Eq(100, {M} + Symbol('s')), Eq(100*kf, {M}*kc + Symbol('s')*kt)], [{M}, Symbol('s')])[{M}]*kc/kf", "Balance total mass and metal over 100 units of feed, then metal in concentrate over metal in feed", tex="R",
         cases=C("kf kc kt", [(1.0, 25, 0.10), (0.6, 28, 0.08), (5.0, 55, 0.5), (2.2, 30, 0.25), (0.8, 20, 0.15)])),
       N("mse-concentration-ratio", EX, "A concentrator treats feed at {{kf}}% metal, making concentrate at {{kc}}% and tailing at {{kt}}%. How many tonnes of feed make one tonne of concentrate?", "(kc - kt)/(kf - kt)",
         f"100/solve([Eq(100, {M} + Symbol('s')), Eq(100*kf, {M}*kc + Symbol('s')*kt)], [{M}, Symbol('s')])[{M}]", "The inverse of the mass fraction reporting to concentrate", tex="K",
         cases=C("kf kc kt", [(1.0, 25, 0.10), (0.6, 28, 0.08), (5.0, 55, 0.5), (2.2, 30, 0.25), (0.8, 20, 0.15)]))]),
     ("C", X("B2.2", "B4.2"), "Name the pyrometallurgical steps for a sulphide ore.",
      "Roasting burns sulphur to SO₂ and makes oxide. Smelting melts the charge into a sulphide matte under a slag. Converting blows air through matte to oxidise iron and sulphur, leaving blister metal. Refining removes the last impurities, often electrolytically.", "P2", [
       L("mse-pyro-step", EX, "Which pyrometallurgical step? {{q}}", ["Roasting", "Smelting", "Converting", "Refining"], [
         ("Zinc sulphide concentrate is burned in air to zinc oxide below its melting point", 0), ("Copper concentrate is melted with flux into a matte and a slag", 1),
         ("Air is blown through molten matte until blister copper remains", 2), ("Blister copper is cast as anodes and plated onto pure cathodes", 3), ("A flash furnace burns dry concentrate in oxygen and collects molten matte", 1)],
         "Burn off sulphur, melt and separate, blow to metal, purify"),
       F("mse-pyro-facts", EX, [
         ("Matte is", "a molten mixture of metal sulphides", "a silicate waste", "pure metal", "an oxide scale"),
         ("Slag is", "a molten oxide and silicate layer that carries off gangue and iron", "the valuable sulphide", "a gas", "unreacted coke"),
         ("Silica flux is added in copper smelting to", "combine with iron oxide into a fluid slag", "reduce copper oxide", "raise the sulphur content", "cool the furnace"),
         ("Flash smelting needs little added fuel because", "burning the concentrate's own sulphur and iron supplies the heat", "it runs cold", "it uses electricity only", "no reaction occurs"),
         ("The sulphur dioxide from roasting and converting is usually", "captured and made into sulphuric acid", "vented as the main product", "reduced to sulphur in the slag", "dissolved in the matte")],
         "Sulphur leaves as gas, iron as slag, the metal stays")]),
     ("D", X("B2.4", "A1.6"), "Do the stoichiometry of a roast.",
      "ZnS + 1.5 O₂ → ZnO + SO₂: each mole of sulphide gives one of SO₂, which can become one of H₂SO₄. Use ZnS 97.44, SO₂ 64.06, H₂SO₄ 98.08 g/mol.", "P1", [
       N("mse-roast-so2", EX, "An ore concentrate is {{kg}}% ZnS by mass and is roasted completely. How many kg of SO₂ come from one tonne? (ZnS 97.44, SO₂ 64.06 g/mol)", "1000*kg/100*64.06/97.44",
         "(1000*kg/100/Rational('97.44'))*Rational('64.06')", "Mass of sulphide, to moles, to mass of SO₂", tex="m",
         cases=C("kg", [(80,), (55,), (92,), (70,), (48,)])),
       N("mse-roast-acid", EX, "An ore concentrate is {{kg}}% ZnS by mass. If all its sulphur is recovered, how many kg of H₂SO₄ can one tonne make? (ZnS 97.44, H₂SO₄ 98.08 g/mol)", "1000*kg/100*98.08/97.44",
         "(1000*kg/100/Rational('97.44'))*Rational('98.08')", "One mole of acid per mole of sulphide", tex="m",
         cases=C("kg", [(80,), (55,), (92,), (70,), (48,)]))]),
     ("E", X("B1.1", "B1.3", "B1.5"), "Name the hydrometallurgical operations and where each is used.",
      "Leaching dissolves the metal (acid for copper oxide and zinc calcine, alkaline for bauxite, cyanide for gold, pressure acid for laterites). The liquor is purified by solvent extraction, ion exchange or precipitation, and the metal is recovered by cementation or electrowinning.", "P2", [
       L("mse-hydro-step", EX, "Which hydrometallurgical operation? {{q}}", ["Leaching", "Solvent extraction", "Ion exchange", "Cementation", "Electrowinning"], [
         ("Dilute sulphuric acid trickles through a heap of oxide copper ore", 0), ("An organic reagent in kerosene pulls copper out of the leach liquor, then gives it up to strong acid", 1),
         ("Uranium is loaded onto resin beads from a dilute liquor", 2), ("Zinc dust is added to a gold cyanide solution and gold drops out", 3), ("Copper is plated from purified sulphate solution onto cathodes using inert anodes", 4),
         ("Scrap iron is put in a copper sulphate stream and copper coats it", 3)],
         "Dissolve, purify and concentrate, then recover"),
       F("mse-hydro-facts", EX, [
         ("Gold is leached from ore with", "dilute aerated cyanide solution", "sulphuric acid", "caustic soda", "water alone"),
         ("The Bayer process extracts alumina from bauxite by", "hot caustic soda leaching under pressure", "cyanide leaching", "roasting to SO₂", "flotation"),
         ("Nickel laterites are commonly treated by", "high-pressure acid leaching", "froth flotation alone", "simple roasting", "magnetic separation"),
         ("Cementation works because", "a more active metal displaces a more noble one from solution", "the solution is boiled dry", "current is applied", "the pH is raised"),
         ("Thickeners and filters in a leach plant are for", "solid-liquid separation", "grinding", "smelting", "electrolysis")],
         "Each metal has a lixiviant that dissolves it and leaves the gangue")]),
     ("F", X("B1.2"), "Read the regions and lines of a Pourbaix diagram.",
      "A potential-pH diagram maps where the metal (immunity), a dissolved ion (corrosion) or a solid oxide or hydroxide (passivation) is stable. Horizontal lines are electron transfer alone, vertical lines acid-base alone; water is stable between the hydrogen and oxygen lines.", "P2", [
       L("mse-pourbaix-region", EX, "Which region of a Pourbaix diagram? {{q}}", ["Immunity", "Corrosion", "Passivation"], [
         ("The metal itself is the stable form", 0), ("A dissolved ion is the stable form", 1), ("A solid oxide or hydroxide is the stable form", 2),
         ("Iron at low potential, below the Fe/Fe²⁺ line", 0), ("Iron at pH 2 and moderate potential, as Fe²⁺", 1), ("Iron at pH 10 and moderate potential, as an oxide film", 2), ("Where a leach must operate to dissolve the metal", 1)],
         "Metal, ion or solid compound"),
       F("mse-pourbaix-facts", EX, [
         ("A horizontal line on a Pourbaix diagram is a reaction that involves", "electrons but no hydrogen ions", "hydrogen ions but no electrons", "neither", "only gases"),
         ("A vertical line on a Pourbaix diagram is a reaction that involves", "hydrogen ions but no electrons", "electrons but no hydrogen ions", "both in equal number", "only solids"),
         ("Below the hydrogen line of the diagram, water", "is reduced to hydrogen gas", "is oxidised to oxygen", "is stable", "freezes"),
         ("A Pourbaix diagram cannot tell you", "how fast the corrosion or leaching goes", "which species is stable", "the effect of pH", "the effect of potential"),
         ("Gold's region of immunity covers the whole range of water stability, which is why", "gold does not corrode in water, and needs a complexing agent such as cyanide to leach", "gold dissolves in rain", "gold passivates", "gold is active")],
         "Thermodynamics only: what is stable, never how fast")]),
     ("G", X("B1.4"), "Compute metal deposited and energy used in electrowinning.",
      "Faraday: m = ItMη ÷ nF, with η the current efficiency. The energy per kilogram is VnF ÷ (Mη), so high cell voltage and low efficiency both cost power.", "P1", [
       N("mse-electrowin-mass", EX, "A tankhouse cell runs at {{kj}} kA for {{kt}} h at {{kf}}% current efficiency, plating a metal with M = {{km}} g/mol and n = {{kn}}. Find the mass deposited in kg. (F = 96485 C/mol)", f"kj*1000*kt*3600*km*kf/100/(kn*{FD})/1000",
         f"solve(Eq({M}*1000*kn*{FD}, kj*1000*kt*3600*km*kf/100), {M})[0]", "Charge passed, times efficiency, to moles, to mass", tex="m",
         cases=C("kj kt kf km kn", [(30, 24, 92, 63.55, 2), (50, 24, 90, 65.38, 2), (20, 12, 95, 58.69, 2), (100, 24, 94, 63.55, 2), (5, 8, 85, 58.93, 2)])),
       N("mse-electrowin-energy", EX, "A metal with M = {{km}} g/mol and n = {{kn}} is electrowon at {{kv}} V and {{kf}}% current efficiency. Find the energy used in kWh per kg. (F = 96485 C/mol)", f"kv*kn*{FD}/(3600*km*kf/100)",
         f"solve(Eq({M}*3600000*(km/1000)*kf/100, kv*kn*{FD}), {M})[0]", "Joules per mole over kilograms per mole, corrected for efficiency, then to kWh", tex="E",
         cases=C("km kn kv kf", [(63.55, 2, 2.0, 92), (65.38, 2, 3.3, 90), (58.69, 2, 3.6, 95), (63.55, 2, 0.3, 96), (26.98, 3, 4.2, 94)]))]),
     ("H", X("B3.1"), "Describe ironmaking and do its stoichiometry.",
      "In a blast furnace, coke burns to CO, which reduces iron oxide as the charge descends; limestone fluxes the gangue into slag; the hot metal holds about 4% carbon. Direct reduction uses reformed natural gas or hydrogen and leaves solid sponge iron.", "P1", [
       N("mse-iron-from-ore", EX, "An iron ore is {{kg}}% Fe₂O₃ by mass. How many kg of iron can one tonne yield? (Fe 55.845, Fe₂O₃ 159.69 g/mol)", "1000*kg/100*2*55.845/159.69",
         "(1000*kg/100/Rational('159.69'))*2*Rational('55.845')", "Two moles of iron per mole of hematite", tex="m",
         cases=C("kg", [(90,), (65,), (82,), (95,), (57,)])),
       F("mse-ironmaking-facts", EX, [
         ("In a blast furnace most of the iron oxide is reduced by", "carbon monoxide rising through the charge", "solid limestone", "nitrogen", "molten slag"),
         ("Coke in a blast furnace serves as", "fuel, source of reducing gas and a strong permeable bed", "a flux only", "the source of iron", "a refractory lining"),
         ("Limestone is charged to a blast furnace to", "flux silica and alumina into a fluid slag", "supply carbon", "cool the hearth", "oxidise the iron"),
         ("Blast-furnace hot metal contains about", "4% carbon, so it must be refined into steel", "0.04% carbon", "no carbon", "20% carbon"),
         ("Direct reduced iron differs from blast-furnace iron in being", "reduced in the solid state by gas, without melting", "higher in carbon", "made from scrap", "refined by blowing oxygen")],
         "CO does the reducing; coke and limestone make it possible")]),
     ("I", X("B3.2", "B3.3", "B3.4"), "Place a steelmaking operation and compute a deoxidation addition.",
      "The basic oxygen furnace blows oxygen through hot metal to burn out carbon; the electric arc furnace melts scrap. Ladle treatment adjusts composition, deoxidises (2Al + 3O → Al₂O₃), desulphurises and degasses; the continuous caster freezes the steel into slabs or billets.", "P1", [
       L("mse-steelmaking-step", EX, "Where does this happen? {{q}}", ["Basic oxygen furnace", "Electric arc furnace", "Ladle treatment", "Continuous caster"], [
         ("Oxygen is blown onto hot metal and scrap to cut carbon from 4% to under 0.1%", 0), ("A charge of scrap is melted by graphite electrodes", 1), ("Aluminium is added to tie up dissolved oxygen, and argon is bubbled to float out inclusions", 2),
         ("Steel is poured through a tundish into a water-cooled copper mould and withdrawn as a strand", 3), ("Vacuum degassing lowers hydrogen before casting", 2), ("Direct reduced iron and scrap are melted with electricity", 1)],
         "Refine hot metal, melt scrap, trim the chemistry, then freeze it"),
       N("mse-deoxidation", EX, "Liquid steel holds {{kp}} ppm of dissolved oxygen by mass. How many kg of aluminium per tonne of steel would tie it all up as Al₂O₃? (Al 26.98, O 16.00 g/mol)", "kp/1000*(2*26.98)/(3*16.00)",
         f"solve(Eq({M}*3*16/(2*Rational('26.98')), kp/1000), {M})[0]", "ppm of a tonne is grams; two aluminium atoms take three oxygen atoms", tex="m",
         cases=C("kp", [(600,), (400,), (250,), (800,), (100,)]))]),
     ("J", X("B4.3", "B4.4"), "Describe fused-salt electrolysis and the Kroll process.",
      "Aluminium is too reactive for carbon reduction, so alumina dissolved in molten cryolite is electrolysed (Hall-Héroult); the carbon anode burns away: 2Al₂O₃ + 3C → 4Al + 3CO₂. Titanium is made by chlorinating the oxide and reducing TiCl₄ with magnesium (Kroll).", "P1", [
       N("mse-anode-carbon", EX, "By 2Al₂O₃ + 3C → 4Al + 3CO₂, how many kg of anode carbon are consumed in making {{kt}} tonnes of aluminium? (Al 26.98, C 12.011 g/mol)", "kt*1000*3*12.011/(4*26.98)",
         "(kt*10**6/Rational('26.98'))*Rational(3, 4)*Rational('12.011')/1000", "Three moles of carbon for every four of aluminium", tex="m",
         cases=C("kt", [(1,), (2.5,), (10,), (0.4,), (6,)])),
       F("mse-fused-salt-facts", EX, [
         ("In the Hall-Héroult cell, alumina is dissolved in", "molten cryolite at about 960 °C", "water", "sulphuric acid", "molten iron"),
         ("Aluminium cannot be won from water solution because", "hydrogen would be discharged at the cathode instead", "alumina dissolves too well", "it is too noble", "it has no ions"),
         ("In the Kroll process titanium tetrachloride is reduced by", "molten magnesium under an inert atmosphere", "carbon monoxide", "hydrogen at room temperature", "electrolysis in water"),
         ("Titanium is not made by carbon reduction of its oxide because", "it forms a carbide and dissolves oxygen and nitrogen", "the oxide will not melt", "carbon is too expensive", "the reaction is too fast"),
         ("Magnesium metal is produced mainly by", "electrolysis of molten magnesium chloride or thermal reduction with ferrosilicon", "leaching with cyanide", "blowing air through matte", "flotation")],
         "Metals more reactive than carbon can handle need electrolysis or a more reactive metal")]),
     ("K", X("B2.3", "B3.5"), "Classify refractories and compute a slag basicity.",
      "Acid refractories (silica, fireclay) resist acid slags; basic ones (magnesia, dolomite) resist basic slags; chromite, carbon and high alumina are close to neutral. Slag basicity is commonly %CaO ÷ %SiO₂; steelmaking slags run basic to hold phosphorus and sulphur.", "P1", [
       N("mse-slag-basicity", EX, "A slag analyses {{ka}}% CaO, {{kb}}% MgO, {{kc}}% SiO₂ and {{kd}}% Al₂O₃. Find the basicity (CaO + MgO) ÷ (SiO₂ + Al₂O₃).", "(ka + kb)/(kc + kd)",
         f"solve(Eq({M}*(kc + kd), ka + kb), {M})[0]", "Basic oxides over acid oxides", tex="B",
         cases=C("ka kb kc kd", [(45, 8, 15, 2), (38, 10, 35, 12), (50, 6, 14, 1), (30, 5, 40, 15), (42, 9, 20, 5)])),
       L("mse-refractory-class", EX, "Classify the refractory: {{q}}", ["Acid", "Basic", "Neutral"], [
         ("Silica brick", 0), ("Magnesia brick", 1), ("Dolomite", 1), ("Chromite", 2), ("Fireclay", 0), ("Carbon block", 2)],
         "Match the lining to the slag: acid with acid, basic with basic")])])})

U12 = ("fabrication", "Fabrication", X("B5.3", "B5.4", "B5.5", "B5.6", "B5.7", "B5.8") + P_("3A", "3B", "3E", "3F", "3G", "3H", "3I"), ["PATH"], {
   1: ("Heat treating, shaping and joining", [
     ("A", X("B5.3") + P_("3G"), "Tell the special heat treatments of steel apart.",
      "Austempering holds below the nose until bainite forms, with no temper needed. Martempering holds just above M_s to even out the temperature, then cools to martensite with less distortion. Process annealing softens cold-worked low-carbon steel below 727 °C; spheroidizing gives the softest high-carbon steel.", "P2", [
       L("mse-special-heat-treatment", FB, "Which heat treatment? {{q}}", ["Austempering", "Martempering", "Process anneal", "Spheroidizing"], [
         ("Quench into a salt bath at 350 °C and hold until the transformation to bainite ends", 0), ("Quench to just above the martensite start, hold until uniform, then air cool and temper", 1),
         ("Heat cold-rolled low-carbon sheet to 650 °C between forming passes", 2), ("Hold a high-carbon tool steel just below 727 °C for many hours before machining", 3),
         ("Chosen for a thin spring clip that must be tough without quench cracks or a separate temper", 0)],
         "Bainite by holding, martensite with less distortion, softening below the eutectoid, or balling up the carbide"),
       F("mse-special-treatment-facts", FB, [
         ("The purpose of the hold in martempering is to", "let the surface and centre reach the same temperature before martensite forms", "form bainite", "form pearlite", "dissolve carbides"),
         ("Spheroidite is the softest state of a steel because", "the carbide is in coarse globules with little boundary to block slip", "it contains martensite", "it has no carbon", "its grains are finest"),
         ("A process anneal differs from a full anneal in", "staying below the eutectoid temperature, so no austenite forms", "being hotter", "ending with a quench", "forming martensite"),
         ("Austempering is limited to thin sections because", "the whole part must cool past the nose of the curve before transforming", "bainite cannot form in steel", "it needs vacuum", "it requires tempering twice")],
         "The path on the TTT diagram decides the product")]),
     ("B", X("B5.4") + P_("3E"), "Choose a surface-hardening method and estimate a case depth.",
      "Carburizing diffuses carbon into low-carbon steel, then quenches for a hard case on a tough core. Nitriding forms hard nitrides at about 500 °C with no quench. Induction and flame hardening heat only the surface of a medium-carbon steel. Depth goes as √(Dt).", "P1", [
       L("mse-surface-hardening", FB, "Which surface treatment? {{q}}", ["Carburizing", "Nitriding", "Induction hardening", "Shot peening"], [
         ("A low-carbon gear is held in a carbon-rich gas at 925 °C, then quenched", 0), ("An alloy steel crankshaft is held in ammonia at 510 °C, with no quench", 1),
         ("A coil heats only the skin of a medium-carbon shaft, which is then sprayed with water", 2), ("Small steel balls are fired at a spring to leave compressive stress", 3), ("Chosen when distortion must be smallest and the steel contains Al or Cr", 1)],
         "Add carbon, add nitrogen, heat the skin, or cold work it"),
       N("mse-case-depth", FB, "Carbon diffuses into steel with D = {{kd}} × 10⁻¹¹ m²/s. Estimate the case depth √(Dt) after {{kt}} h, in mm.", "sqrt(kd*1e-11*kt*3600)*1000",
         f"Max(*solve(Eq(({M}/1000)**2, kd*Rational('1e-11')*kt*3600), {M}))", "Hours to seconds, then metres to mm", tex="x",
         cases=C("kd kt", [(1.6, 8), (1.6, 2), (3.0, 4), (0.8, 16), (5.3, 6)]))]),
     ("C", X("B5.5") + P_("3B"), "Choose a casting method and size a pattern.",
      "Sand casting suits large or one-off parts; die casting forces low-melting alloys into steel dies for high volume; investment (lost-wax) casting gives fine detail in any alloy; continuous casting makes slab and billet. A pattern is made oversize by the solid shrinkage.", "P1", [
       L("mse-casting-method", FB, "Which casting method? {{q}}", ["Sand casting", "Die casting", "Investment casting", "Continuous casting"], [
         ("A two-tonne cast iron machine base, three off", 0), ("A million zinc door handles a year", 1), ("A nickel superalloy turbine blade with internal cooling passages", 2),
         ("Steel slab for a rolling mill", 3), ("A thin-walled aluminium gearbox housing in high volume", 1), ("A stainless steel surgical implant with fine detail", 2)],
         "Size and number of parts, detail needed, and the alloy's melting point decide"),
       N("mse-pattern-size", FB, "A casting must be {{kl}} mm long and the alloy shrinks {{ks}}% linearly as it cools from the solidus. Find the pattern length in mm.", "kl*(1 + ks/100)",
         f"solve(Eq({M}/(1 + ks/100), kl), {M})[0]", "Make the pattern oversize by the shrinkage allowance", tex="L",
         cases=C("kl ks", [(200, 1.3), (500, 2.0), (120, 1.0), (850, 1.6), (64, 2.6)]))]),
     ("D", X("B5.6") + P_("3A"), "Compute the limits and strain of a rolling pass.",
      "The rolls bite only if the draft is under μ²R. The true strain of a pass is ln(h₀ ÷ h_f).", "P1", [
       N("mse-rolling-draft", FB, "Rolls of radius {{kr}} mm have a friction coefficient of {{km}} with the strip. Find the largest draft they can take in one pass, in mm.", "km^2*kr",
         "kr*exp(2*log(km))", "Maximum draft is μ²R", tex="d",
         cases=C("kr km", [(300, 0.10), (250, 0.40), (150, 0.07), (400, 0.30), (500, 0.12)])),
       N("mse-rolling-strain", FB, "A strip is rolled from {{ko}} mm to {{kf}} mm thick. Find the true strain.", "log(ko/kf)",
         "integrate(1/Y, (Y, kf, ko))", "Integrate dh ÷ h over the reduction", tex="\\varepsilon",
         cases=C("ko kf", [(25, 20), (10, 6), (3.0, 2.4), (50, 30), (2.0, 0.5)]))]),
     ("E", X("B5.6") + P_("3A"), "Estimate an extrusion pressure and name a bulk-forming process.",
      "Ideal extrusion pressure is p = Y ln(A₀ ÷ A_f), with Y the mean flow stress; friction and redundant work raise it. Rolling passes stock between rolls, forging squeezes it between dies, extrusion pushes it and drawing pulls it through a die.", "P1", [
       N("mse-extrusion-pressure", FB, "A billet {{ko}} mm in diameter is extruded to {{kf}} mm; the mean flow stress is {{ky}} MPa. Find the ideal extrusion pressure in MPa.", "ky*log((ko/kf)^2)",
         "2*ky*integrate(1/Y, (Y, kf, ko))", "The area ratio is the diameter ratio squared", tex="p",
         cases=C("ko kf ky", [(150, 50, 100), (100, 25, 60), (200, 80, 250), (75, 15, 40), (120, 60, 180)])),
       L("mse-forming-process", FB, "Which bulk-forming process? {{q}}", ["Rolling", "Forging", "Extrusion", "Wire drawing"], [
         ("Plate is reduced between two rotating cylinders", 0), ("A hot billet is hammered between shaped dies into a crankshaft", 1), ("An aluminium window-frame section is pushed out of a die", 2),
         ("Copper rod is pulled through a series of dies to a fine diameter", 3), ("Blooms are turned into I-beams between grooved cylinders", 0), ("A bolt head is upset on the end of a rod", 1)],
         "Between rolls, between dies, pushed through, or pulled through")]),
     ("F", X("B5.7") + P_("3A"), "Compute a blanking force and name a sheet-metal operation.",
      "The force to shear a blank is the shear strength times the cut area, perimeter × thickness. Deep drawing pulls a blank into a cup; stretch forming thins it over a form; hydroforming shapes it with fluid pressure.", "P1", [
       N("mse-blanking-force", FB, "A round blank {{kd}} mm in diameter is punched from sheet {{kh}} mm thick with a shear strength of {{kt}} MPa. Find the punch force in kN.", "kt*pi*kd*kh/1000",
         f"solve(Eq({M}*1000/(pi*kd*kh), kt), {M})[0]", "Shear strength times circumference times thickness", tex="F",
         cases=C("kd kh kt", [(50, 2.0, 300), (20, 1.0, 150), (100, 3.0, 400), (12, 0.8, 250), (75, 1.5, 200)])),
       L("mse-sheet-operation", FB, "Which sheet-metal operation? {{q}}", ["Shearing", "Deep drawing", "Stretch forming", "Hydroforming"], [
         ("A punch and die cut blanks from coil", 0), ("A flat blank is pulled into a seamless drinks can body", 1), ("A sheet gripped at its edges is pulled over a form to make an aircraft skin panel", 2),
         ("Fluid pressure expands a tube into a die to make a bicycle frame member", 3), ("A sink bowl is formed from a flat disc with a punch and blank holder", 1)],
         "Cut, pull into a cup, stretch over a form, or shape with fluid")]),
     ("G", X("B5.8") + P_("3F"), "Compute a weld's heat input and choose a joining process.",
      "Heat input per length is ηVI ÷ v. High heat input widens the heat-affected zone and coarsens grains. Arc welding melts with an electric arc; laser welding gives a narrow deep weld; friction stir welding joins in the solid state; brazing melts only a filler.", "P1", [
       N("mse-weld-heat-input", FB, "An arc weld runs at {{kv}} V and {{kj}} A, travelling {{ks}} mm/s with {{kf}}% arc efficiency. Find the heat input in kJ/mm.", "kf/100*kv*kj/(ks*1000)",
         f"solve(Eq({M}*ks*1000, kf/100*kv*kj), {M})[0]", "Arc power times efficiency, over travel speed", tex="H",
         cases=C("kv kj ks kf", [(25, 200, 5, 80), (30, 300, 8, 85), (12, 100, 2, 60), (28, 250, 4, 80), (20, 150, 10, 75)])),
       L("mse-joining-process", FB, "Which joining process? {{q}}", ["Arc welding", "Friction stir welding", "Laser welding", "Brazing or soldering"], [
         ("A rotating pin stirs two aluminium plates together without melting them", 1), ("A consumable electrode and shielding gas join structural steel", 0), ("A focused beam makes a deep, narrow weld with a very small heat-affected zone", 2),
         ("A copper-zinc filler flows into a steel joint by capillary action, and the steel does not melt", 3), ("Chosen for 7xxx aluminium, which cracks when fusion welded", 1), ("Electronic components are attached to a board with a tin alloy", 3)],
         "Melt both, stir in the solid, melt a thin line, or melt only a filler")]),
     ("H", X("B5.8") + P_("3F"), "Compute a carbon equivalent and judge weldability.",
      "CE = C + Mn÷6 + (Cr + Mo + V)÷5 + (Ni + Cu)÷15, the IIW formula in weight percent. A high CE means a hard, crack-prone heat-affected zone: usual guidance is no preheat under about 0.40, preheat from 0.40 to 0.60, and preheat with low-hydrogen practice and post-heat above.", "P1", [
       N("mse-carbon-equivalent", FB, "A steel holds {{kc}}% C, {{km}}% Mn, {{kr}}% Cr, {{ko}}% Mo, {{kn}}% Ni and {{ku}}% Cu, with no vanadium. Find its IIW carbon equivalent, C + Mn÷6 + (Cr + Mo + V)÷5 + (Ni + Cu)÷15.", "kc + km/6 + (kr + ko)/5 + (kn + ku)/15",
         "(30*kc + 5*km + 6*(kr + ko) + 2*(kn + ku))/Rational(30)", "Each alloy group is weighted by how strongly it hardens the heat-affected zone", tex="CE",
         cases=C("kc km kr ko kn ku", [(0.20, 1.20, 0.10, 0.02, 0.10, 0.20), (0.40, 0.80, 1.00, 0.20, 0.10, 0.10), (0.12, 0.60, 0.05, 0.01, 0.05, 0.10), (0.30, 1.50, 0.50, 0.25, 1.80, 0.15), (0.16, 1.40, 0.02, 0.01, 0.02, 0.02)])),
       L("mse-weldability", FB, "By the usual carbon-equivalent bands (under 0.40, 0.40 to 0.60, above 0.60), how weldable is the steel? {{q}}", ["Readily weldable, no preheat", "Weldable with preheat", "Difficult: preheat, low-hydrogen practice and post-heat"], [
         ("CE = 0.32", 0), ("CE = 0.48", 1), ("CE = 0.78", 2), ("CE = 0.39", 0), ("CE = 0.55", 1), ("CE = 0.66", 2)],
         "Higher carbon equivalent, harder heat-affected zone, more care")]),
     ("I", P_("3H"), "Compute porosity and sintering shrinkage of a powder compact.",
      "Porosity = (1 − ρ ÷ ρ_theoretical) × 100. Mass is conserved on sintering, so linear shrinkage is 1 − (ρ_green ÷ ρ_sintered)^⅓.", "P1", [
       N("mse-powder-porosity", FB, "A sintered part has density {{kd}} g/cm³; the fully dense alloy is {{kt}} g/cm³. Find the porosity in percent.", "(1 - kd/kt)*100",
         f"solve(Eq(kd, kt*(1 - {M}/100)), {M})[0]", "One minus the relative density", tex="P",
         cases=C("kd kt", [(6.8, 7.87), (7.4, 7.87), (2.5, 2.70), (15.9, 19.3), (4.1, 4.51)])),
       N("mse-sinter-shrinkage", FB, "A green compact of density {{kg}} g/cm³ sinters to {{ks}} g/cm³. Find the linear shrinkage in percent.", "(1 - (kg/ks)^(1/3))*100",
         "100 - 100*exp(log(kg/ks)/3)", "Volume ratio is the inverse density ratio; take its cube root", tex="\\%",
         cases=C("kg ks", [(6.0, 7.4), (2.3, 3.9), (9.5, 18.0), (5.5, 6.8), (3.2, 5.9)]))]),
     ("J", P_("3I"), "Name the additive-manufacturing routes and compute an energy density.",
      "Powder bed fusion melts thin layers of powder with a laser or electron beam; directed energy deposition feeds powder or wire into a melt pool; binder jetting glues powder for later sintering; material extrusion lays down a filament. Volumetric energy density is P ÷ (v h t).", "P1", [
       L("mse-additive-route", FB, "Which additive process? {{q}}", ["Powder bed fusion", "Directed energy deposition", "Binder jetting", "Material extrusion"], [
         ("A laser scans each spread layer of titanium powder", 0), ("Wire is fed into a melt pool to rebuild a worn turbine shaft", 1), ("A print head deposits glue on powder, and the part is sintered afterward", 2),
         ("A heated nozzle lays down a thermoplastic filament", 3), ("An electron beam melts powder layer by layer in vacuum", 0), ("Powder is blown through a nozzle into a laser spot on an existing part", 1)],
         "Fuse a spread layer, feed a melt pool, glue then sinter, or squeeze out a bead"),
       N("mse-energy-density", FB, "A laser powder bed machine runs at {{kp}} W, {{kv}} mm/s scan speed, {{kh}} mm hatch spacing and {{kt}} mm layer thickness. Find the volumetric energy density in J/mm³.", "kp/(kv*kh*kt)",
         f"solve(Eq({M}*kv*kh*kt, kp), {M})[0]", "Power over the volume swept per second", tex="E",
         cases=C("kp kv kh kt", [(200, 1000, 0.10, 0.03), (370, 1300, 0.12, 0.03), (175, 700, 0.08, 0.04), (300, 1200, 0.14, 0.05), (95, 500, 0.07, 0.025)]))])])})

U13 = ("functional", "Functional materials and microfabrication", X("B6.5", "B6.6", "B6.7", "B8.3", "B8.4", "B8.5", "B8.6", "B10.1", "B10.2", "B10.3", "B10.4", "B10.5", "B10.6") + P_("3H", "4J"), ["LATTICE", "DEFECT"], {
   1: ("Ceramics and dielectrics in use", [
     ("A", X("B6.5") + P_("3H"), "Compute grain growth and explain sintering.",
      "Sintering bonds powder below melting, driven by the fall in surface energy; finer powder sinters faster. Afterward grains coarsen by d² − d₀² = Kt.", "P1", [
       N("mse-grain-growth", FN, "Grains start at {{ko}} µm and grow by d² − d₀² = Kt with K = {{kk}} µm²/h. Find the grain size after {{kt}} h, in µm.", "sqrt(ko^2 + kk*kt)",
         f"Max(*solve(Eq({M}**2 - ko**2, kk*kt), {M}))", "Add Kt to the square of the starting size", tex="d",
         cases=C("ko kk kt", [(2, 5, 4), (10, 50, 6), (0.5, 0.3, 10), (5, 12, 2), (1, 8, 3)])),
       F("mse-sintering-facts", FN, [
         ("The driving force for sintering is", "the reduction of total surface energy", "an applied voltage", "gravity", "the heat of fusion"),
         ("A finer starting powder sinters", "faster and at lower temperature", "more slowly", "only with a liquid phase", "not at all"),
         ("In the first stage of sintering", "necks grow between touching particles", "all pores vanish", "the grains melt", "the compact expands"),
         ("Liquid-phase sintering speeds densification because", "a small amount of liquid pulls particles together and carries material quickly", "it cools the compact", "it removes the powder", "it stops grain growth"),
         ("Pores trapped inside grains during rapid grain growth are", "very hard to remove, which limits the final density", "removed first", "filled with metal", "helpful for strength")],
         "Surface energy drives it, diffusion carries it, grain growth can spoil it")]),
     ("B", X("B6.7"), "Compute an ionic conductivity from a diffusion coefficient.",
      "The Nernst-Einstein relation ties the two: σ = n(ze)²D ÷ kT. Ceramics such as stabilised zirconia conduct by oxygen vacancies, and their conductivity rises with temperature.", "P1", [
       N("mse-nernst-einstein", FN, "A ceramic has {{kp}} × 10²⁸ mobile ions per m³, each of charge {{kz}}e, with D = {{kd}} × 10⁻¹³ m²/s at {{kt}} K. Find its ionic conductivity in S/m. (e = 1.602 × 10⁻¹⁹ C, k = 1.380649 × 10⁻²³ J/K)", "kp*1e28*(kz*1.602e-19)^2*kd*1e-13/(1.380649e-23*kt)",
         f"solve(Eq({M}*Rational('1.380649e-23')*kt, kp*10**28*(kz*Rational('1.602e-19'))**2*kd*Rational('1e-13')), {M})[0]", "Carrier density times charge squared times D, over kT", tex="\\sigma",
         cases=C("kp kz kd kt", [(1.0, 2, 1.0, 1273), (0.5, 2, 20, 1073), (2.0, 1, 0.5, 600), (0.3, 2, 100, 1273), (4.0, 1, 3.0, 800)])),
       F("mse-ionic-conduction-facts", FN, [
         ("Yttria-stabilised zirconia conducts electricity at high temperature by", "oxygen ions hopping through oxygen vacancies", "free electrons", "holes in the valence band", "protons only"),
         ("Adding yttria to zirconia raises its ionic conductivity because", "each pair of Y³⁺ ions brings an oxygen vacancy", "it removes all vacancies", "it adds free electrons", "it melts the zirconia"),
         ("Ionic conductivity in a ceramic changes with temperature", "upward, following an Arrhenius law like diffusion", "downward, like a metal", "not at all", "only at the melting point"),
         ("A solid oxide fuel cell or oxygen sensor needs an electrolyte that conducts", "ions but not electrons", "electrons but not ions", "both equally", "neither")],
         "Charge is carried by moving ions, so conductivity follows the diffusion coefficient")]),
     ("C", X("B6.6", "B8.4"), "Compute a capacitance and a breakdown voltage.",
      "C = ε₀ε_r A ÷ d, with ε₀ = 8.854 × 10⁻¹² F/m. The dielectric fails when the field reaches its dielectric strength, so V_max = strength × thickness.", "P1", [
       N("mse-capacitance", FN, "A capacitor has plates of {{ka}} cm², a dielectric {{kd}} µm thick and relative permittivity {{kf}}. Find its capacitance in nF. (ε₀ = 8.8541878 × 10⁻¹² F/m)", "8.8541878e-12*kf*ka*1e-4/(kd*1e-6)*1e9",
         f"solve(Eq({M}*kd*Rational('1e-6'), Rational('8.8541878e-12')*kf*ka*Rational('1e-4')*10**9), {M})[0]", "Convert cm² and µm to SI, then farads to nF", tex="C",
         cases=C("ka kd kf", [(1.0, 10, 6.0), (0.5, 2, 3000), (4.0, 25, 3.2), (0.1, 1, 9.0), (2.0, 50, 2.1)])),
       N("mse-breakdown-voltage", FN, "A dielectric film {{kd}} µm thick has a dielectric strength of {{ks}} kV/mm. Find the voltage at which it breaks down, in volts.", "ks*kd",
         "ks*1000*(kd/1000)", "kV/mm times µm is volts", tex="V",
         cases=C("kd ks", [(10, 20), (2, 300), (25, 150), (0.5, 1000), (100, 12)]))]),
     ("D", X("B8.4"), "Tell piezoelectric, pyroelectric and ferroelectric behaviour apart.",
      "Piezoelectric crystals polarise under stress (and strain under a field). Pyroelectrics have a spontaneous polarisation that changes with temperature. Ferroelectrics have a spontaneous polarisation that an applied field can reverse; they lose it above the Curie temperature. Every ferroelectric is pyroelectric and piezoelectric.", "P2", [
       L("mse-polar-class", FN, "Which property is being used? {{q}}", ["Piezoelectric", "Pyroelectric", "Ferroelectric"], [
         ("A quartz crystal produces a voltage when squeezed", 0), ("An infrared sensor gives a signal when its temperature changes", 1), ("A memory cell stores a bit as a polarisation direction that a field can flip", 2),
         ("An ultrasound transducer vibrates when a voltage is applied", 0), ("A hysteresis loop of polarisation against field", 2), ("A gas lighter makes a spark when a crystal is struck", 0)],
         "Stress, temperature change, or a switchable polarisation"),
       F("mse-polar-facts", FN, [
         ("Above its Curie temperature barium titanate", "becomes cubic and loses its spontaneous polarisation", "becomes a metal", "melts", "becomes ferromagnetic"),
         ("Quartz is piezoelectric but not ferroelectric because", "it has no spontaneous polarisation to switch", "it is amorphous", "it is a metal", "it has a centre of symmetry"),
         ("A crystal can be piezoelectric only if its structure", "lacks a centre of symmetry", "is cubic close-packed", "is amorphous", "contains free electrons"),
         ("A piezoelectric ceramic such as PZT is poled in order to", "align the domains so the grains' effects add up", "anneal it", "sinter it", "remove its polarisation")],
         "All ferroelectrics are pyroelectric, all pyroelectrics are piezoelectric, never the reverse")]),
     ("E", X("B8.4") + P_("4J"), "Compute a surface reflectivity and a critical angle.",
      "At normal incidence from air, R = [(n − 1) ÷ (n + 1)]². Light inside a material of index n is totally reflected beyond the critical angle, sin θ_c = 1 ÷ n, which is how an optical fibre guides light.", "P1", [
       N("mse-reflectivity", FN, "Light strikes a transparent solid of refractive index {{kn}} from air at normal incidence. What percent is reflected at the surface?", "((kn - 1)/(kn + 1))^2*100",
         "100 - 400*kn/(kn + 1)**2", "The check uses the transmitted fraction 4n ÷ (n + 1)²", tex="R",
         cases=C("kn", [(1.50,), (2.42,), (1.33,), (3.50,), (1.76,)])),
       N("mse-critical-angle", FN, "A transparent solid has refractive index {{kn}}. Find the critical angle for total internal reflection against air, in degrees.", "asin(1/kn)*180/pi",
         "atan2(1, sqrt(kn**2 - 1))*180/pi", "sin θ_c = 1 ÷ n", tex="\\theta_c",
         cases=C("kn", [(1.50,), (2.42,), (1.33,), (3.50,), (1.76,)]))])]),
   2: ("Electrons, junctions and superconductors", [
     ("A", X("B8.6"), "Use the Fermi-Dirac distribution.",
      "f(E) = 1 ÷ [exp((E − E_F) ÷ kT) + 1]: one half at the Fermi level, falling to zero a few kT above it. Only electrons within a few kT of E_F take part in conduction.", "P1", [
       N("mse-fermi-dirac", FN, "Find the percent probability that a state {{kd}} eV from the Fermi level (positive is above) is occupied at {{kt}} K. (k = 8.617333 × 10⁻⁵ eV/K)", f"100/(exp(kd/({KB}*kt)) + 1)",
         f"100 - 100/(1 + exp(-kd/({KBS}*kt)))", "The check uses the probability that the state is empty", tex="f",
         cases=C("kd kt", [(0.05, 300), (-0.05, 300), (0.10, 600), (0.02, 300), (-0.10, 400)])),
       F("mse-fermi-facts", FN, [
         ("At the Fermi level the occupation probability is", "one half at any temperature above zero", "one", "zero", "equal to kT"),
         ("At absolute zero the Fermi-Dirac distribution is", "a step: full below the Fermi level, empty above", "a straight line", "flat at one half", "a Gaussian"),
         ("In an intrinsic semiconductor the Fermi level lies", "near the middle of the band gap", "in the conduction band", "in the valence band", "at the vacuum level"),
         ("Doping silicon n-type moves the Fermi level", "toward the conduction band", "toward the valence band", "to mid-gap", "nowhere"),
         ("An electron's effective mass in a crystal describes", "how the band's curvature makes it respond to a force", "its rest mass changing", "the mass of the nucleus", "its charge")],
         "Half filled at E_F; the spread around it is a few kT")]),
     ("B", X("B8.5"), "Compute a junction's built-in potential and say what bias does.",
      "V_bi = (kT ÷ q) ln(N_A N_D ÷ n_i²). Forward bias lowers the barrier and current rises exponentially; reverse bias raises it and only a small leakage flows. A solar cell is a junction that separates carriers made by light.", "P1", [
       N("mse-built-in-potential", FN, "A silicon junction at 300 K has N_A = {{ka}} × 10^{{kp}} and N_D = {{kb}} × 10^{{kq}} per cm³, with n_i = 1.5 × 10¹⁰ per cm³. Find the built-in potential in volts. (k = 8.617333 × 10⁻⁵ eV/K)", f"{KB}*300*log(ka*10^kp*kb*10^kq/(1.5e10)^2)",
         f"{KBS}*300*(log(ka*10**kp) + log(kb*10**kq) - 2*log(Rational('1.5e10')))", "kT in eV is the thermal voltage in volts", tex="V_{bi}",
         cases=C("ka kp kb kq", [(1, 16, 1, 16), (5, 17, 1, 15), (1, 18, 1, 17), (2, 15, 2, 15), (1, 19, 5, 16)])),
       L("mse-junction-bias", FN, "Forward or reverse bias? {{q}}", ["Forward bias", "Reverse bias"], [
         ("The positive terminal is on the p side and current rises steeply with voltage", 0), ("The depletion region widens and only a tiny leakage current flows", 1), ("A light-emitting diode is glowing", 0),
         ("A photodiode is waiting to detect light with a wide depletion region", 1), ("The energy barrier at the junction is lowered", 0)],
         "Forward lowers the barrier; reverse raises it and widens the depletion region")]),
     ("C", X("B8.3"), "Compute a superconductor's critical field and tell type I from type II.",
      "H_c(T) = H_c(0)[1 − (T ÷ T_c)²]. Superconductivity needs temperature, field and current density all below their critical values. Type I expels flux completely up to H_c; type II lets flux in as vortices between H_c1 and a much higher H_c2, which is why magnets use it.", "P1", [
       N("mse-critical-field", FN, "A superconductor has T_c = {{kc}} K and a critical field of {{ko}} mT at absolute zero. Find its critical field at {{kt}} K, in mT.", "ko*(1 - (kt/kc)^2)",
         "ko*(kc - kt)*(kc + kt)/kc**2", "The field falls parabolically to zero at T_c", tex="H_c",
         cases=C("kc ko kt", [(7.2, 80, 4.2), (9.2, 200, 4.2), (3.7, 30, 2.0), (4.15, 41, 1.0), (7.2, 80, 6.0)])),
       F("mse-superconductor-facts", FN, [
         ("BCS theory explains superconductivity by", "electrons pairing through lattice vibrations", "ions becoming mobile", "a band gap opening to 5 eV", "electrons losing their charge"),
         ("Which kind of superconductor is used to wind high-field magnets?", "Type II, such as niobium-titanium", "Type I, such as lead", "Any metal below 77 K", "Copper"),
         ("Between its lower and upper critical fields a type II superconductor", "lets magnetic flux through as quantised vortices", "is a normal metal", "expels all flux", "becomes ferromagnetic"),
         ("Besides temperature, superconductivity is destroyed by", "too high a magnetic field or current density", "too low a current", "light", "pressure only"),
         ("Cuprate superconductors matter because their critical temperatures", "exceed the boiling point of liquid nitrogen, 77 K", "are above room temperature", "are below 1 K", "do not exist")],
         "Three limits at once: temperature, field and current density")])]),
   3: ("Microfabrication", [
     ("A", X("B10.1"), "Compute lithographic resolution and depth of focus.",
      "Rayleigh: the smallest printable feature is k₁λ ÷ NA and the depth of focus k₂λ ÷ NA². A larger numerical aperture sharpens the image but shrinks the focus range.", "P1", [
       N("mse-litho-resolution", FN, "A lithography tool has wavelength {{kw}} nm, numerical aperture {{kn}} and process factor k₁ = {{kk}}. Find the smallest feature it prints, in nm.", "kk*kw/kn",
         f"solve(Eq({M}*kn, kk*kw), {M})[0]", "k₁ λ ÷ NA", tex="R",
         cases=C("kw kn kk", [(193, 1.35, 0.30), (248, 0.80, 0.40), (13.5, 0.33, 0.35), (365, 0.60, 0.60), (193, 0.93, 0.35)])),
       N("mse-litho-focus", FN, "A lithography tool has wavelength {{kw}} nm and numerical aperture {{kn}}, with k₂ = {{kk}}. Find its depth of focus in nm.", "kk*kw/kn^2",
         f"solve(Eq({M}*kn**2, kk*kw), {M})[0]", "k₂ λ ÷ NA²", tex="DOF",
         cases=C("kw kn kk", [(193, 1.35, 0.5), (248, 0.80, 0.5), (13.5, 0.33, 1.0), (365, 0.60, 0.8), (193, 0.93, 0.5)]))]),
     ("B", X("B10.2"), "Tell isotropic from anisotropic etching and use selectivity.",
      "Wet chemical etches usually attack equally in all directions and undercut the mask; plasma (dry) etches can cut straight down. Selectivity is the etch rate of the film over that of the mask or the layer beneath.", "P1", [
       L("mse-etch-profile", FN, "Which kind of etch? {{q}}", ["Isotropic, typical of a wet etch", "Anisotropic, typical of a plasma etch"], [
         ("The film is removed sideways under the mask as far as it is removed downward", 0), ("Vertical sidewalls are cut with almost no undercut", 1), ("Buffered hydrofluoric acid removes silicon dioxide", 0),
         ("Reactive ions are accelerated straight down onto the wafer", 1), ("Needed for a trench much deeper than it is wide", 1)],
         "Equal in all directions, or straight down"),
       N("mse-etch-selectivity", FN, "A film must be etched {{kd}} nm deep with an etch whose selectivity to the mask is {{ks}} to 1. Find the least mask thickness that survives, in nm.", "kd/ks",
         f"solve(Eq({M}*ks, kd), {M})[0]", "The mask erodes 1 nm for every S nm of film", tex="t",
         cases=C("kd ks", [(500, 10), (1200, 30), (200, 4), (3000, 50), (80, 2.5)]))]),
     ("C", X("B10.3"), "Choose a deposition method and count ALD cycles.",
      "Sputtering and evaporation are physical: atoms travel in a line from a source. CVD reacts gases at the surface and coats more evenly. ALD alternates two self-limiting gas pulses and grows a fixed fraction of a monolayer per cycle. Electrodeposition plates metal from solution.", "P1", [
       L("mse-deposition-method", FN, "Which deposition method? {{q}}", ["Sputtering", "Chemical vapour deposition", "Atomic layer deposition", "Electrodeposition"], [
         ("Argon ions knock atoms off a metal target onto the wafer", 0), ("Silane decomposes on a hot wafer to grow polysilicon", 1), ("Two precursors are pulsed in turn to coat a deep trench with exactly 5 nm of oxide", 2),
         ("Copper is plated from solution into trenches for interconnects", 3), ("Chosen when thickness must be controlled to a single atomic layer", 2), ("A plasma lets a nitride film grow from gases at low temperature", 1)],
         "Knocked off a target, reacted from gas, pulsed one layer at a time, or plated"),
       N("mse-ald-cycles", FN, "An ALD process grows {{kg}} Å per cycle. How many cycles give a {{kt}} nm film?", "kt*10/kg",
         f"solve(Eq({M}*kg/10, kt), {M})[0]", "Convert nm to Å, then divide by the growth per cycle", tex="N",
         cases=C("kg kt", [(1.0, 5), (0.8, 20), (1.2, 3), (0.5, 10), (1.1, 44)]))]),
     ("D", X("B10.4"), "Compute an oxide thickness with the Deal-Grove model and the silicon it consumes.",
      "x² + Ax = Bt: growth is linear in time while the surface reaction limits it, parabolic once diffusion through the oxide does. The oxide takes silicon from the wafer: Si occupies 12.06 cm³/mol and SiO₂ 27.3, so 44% of the oxide thickness was silicon.", "P1", [
       N("mse-deal-grove", FN, "Silicon oxidises by x² + Ax = Bt with A = {{ka}} µm and B = {{kb}} µm²/h. Find the oxide thickness after {{kt}} h, in µm.", "(-ka + sqrt(ka^2 + 4*kb*kt))/2",
         f"Max(*solve(Eq({M}**2 + ka*{M}, kb*kt), {M}))", "Take the positive root of the quadratic", tex="x",
         cases=C("ka kb kt", [(0.165, 0.027, 2), (0.226, 0.287, 1), (0.05, 0.72, 0.5), (0.165, 0.027, 10), (0.50, 0.203, 4)])),
       N("mse-silicon-consumed", FN, "An oxide {{kx}} nm thick is grown on silicon. How many nm of silicon were consumed? (Molar volumes: Si 12.06, SiO₂ 27.3 cm³/mol)", "kx*12.06/27.3",
         f"solve(Eq({M}/Rational('12.06'), kx/Rational('27.3')), {M})[0]", "One mole of silicon makes one mole of oxide, on the same area", tex="t",
         cases=C("kx", [(100,), (25,), (500,), (8,), (1000,)]))]),
     ("E", X("B10.5"), "Estimate a dopant's diffusion length and compare diffusion with implantation.",
      "A dopant spreads about √(Dt) in a thermal step. Ion implantation fires ions at a set energy and dose: depth is set by energy, the amount by dose, at low temperature, but the crystal damage must then be annealed.", "P1", [
       N("mse-dopant-length", FN, "A dopant in silicon has D = {{kd}} × 10⁻¹⁴ cm²/s. Find its diffusion length √(Dt) after {{kt}} min, in nm.", "sqrt(kd*1e-14*kt*60)*1e7",
         f"Max(*solve(Eq(({M}/10**7)**2, kd*Rational('1e-14')*kt*60), {M}))", "Minutes to seconds, then cm to nm", tex="L",
         cases=C("kd kt", [(1.0, 30), (30, 60), (0.2, 10), (5.0, 120), (100, 20)])),
       L("mse-doping-method", FN, "Thermal diffusion or ion implantation? {{q}}", ["Thermal diffusion", "Ion implantation"], [
         ("The dose is set by counting the beam charge", 1), ("The peak concentration lies below the surface, at a depth set by the beam energy", 1), ("The wafer sits in a dopant gas at 1000 °C", 0),
         ("A photoresist mask can be used because the wafer stays cool", 1), ("The profile is highest at the surface and falls off with depth", 0), ("An anneal is needed afterward to repair lattice damage and activate the dopant", 1)],
         "Heat and a gas source, or a beam of ions")]),
     ("F", X("B10.6"), "Compute die yield and dies per wafer.",
      "The Poisson model gives yield Y = exp(−D₀A) for defect density D₀ and die area A: large dies suffer most. Gross dies per wafer ≈ π(d÷2)² ÷ A − πd ÷ √(2A), the second term allowing for the edge.", "P1", [
       N("mse-die-yield", FN, "A process has {{kd}} killer defects per cm² and the die area is {{ka}} cm². Find the Poisson yield in percent.", "100*exp(-kd*ka)",
         "100/exp(kd*ka)", "Probability of zero defects on a die", tex="Y",
         cases=C("kd ka", [(0.5, 1.0), (0.1, 4.0), (1.0, 0.25), (0.2, 6.0), (0.05, 1.5)])),
       N("mse-dies-per-wafer", FN, "Estimate the gross dies on a {{kd}} mm wafer for a die area of {{ka}} mm², from π(d÷2)² ÷ A − πd ÷ √(2A). Do not round.", "pi*(kd/2)^2/ka - pi*kd/sqrt(2*ka)",
         "pi*kd**2/(4*ka) - pi*kd/(2*ka)**Rational(1, 2)", "Wafer area over die area, less the partial dies at the edge", tex="N",
         cases=C("kd ka", [(300, 100), (200, 50), (300, 400), (150, 25), (300, 64)]))])])})

U14 = ("practice", "Composites and service practice", X("B11.2", "B11.3", "B11.4", "B11.5", "B11.6") + P_("1C", "2F", "2G", "2H", "3J", "4E", "4I"), ["PATH"], {
   1: ("Composites in practice", [
     ("A", X("B11.3", "B11.6"), "Classify a composite by its matrix and say why it is used.",
      "Polymer-matrix composites give the best strength and stiffness per weight near room temperature. Metal-matrix composites add stiffness, wear resistance and temperature capability to a metal. Ceramic-matrix composites add toughness to a ceramic, by fibres bridging and pulling out of cracks.", "P2", [
       L("mse-composite-class", PR, "Which class of composite? {{q}}", ["Polymer-matrix (PMC)", "Metal-matrix (MMC)", "Ceramic-matrix (CMC)"], [
         ("Carbon fibre in epoxy for an aircraft wing skin", 0), ("Silicon carbide particles in aluminium for a brake rotor", 1), ("Silicon carbide fibres in silicon carbide for a turbine shroud", 2),
         ("Glass fibre in polyester for a boat hull", 0), ("Tungsten carbide in cobalt for a cutting tool", 1), ("Carbon fibres in carbon for an aircraft brake disc", 2)],
         "Name the continuous phase"),
       F("mse-composite-class-facts", PR, [
         ("Fibres are added to a ceramic matrix mainly to raise its", "toughness, by bridging and pulling out of cracks", "density", "melting point", "electrical conductivity"),
         ("In a ceramic-matrix composite the fibre-matrix bond is kept deliberately", "weak, so cracks deflect along the fibres", "as strong as possible", "metallic", "absent"),
         ("Polymer-matrix composites are limited mainly by", "the temperature the resin can stand", "low specific strength", "high density", "poor corrosion resistance"),
         ("Concrete reinforced with steel bar is a composite in which the steel carries", "the tension that concrete cannot", "the compression", "no load", "the heat"),
         ("A sandwich panel puts stiff skins on a light core in order to", "raise bending stiffness for very little mass", "raise the density", "carry tension only", "conduct heat")],
         "Each matrix has a weakness the reinforcement is there to cover")]),
     ("B", X("B11.4") + P_("3J"), "Choose a composite fabrication route and convert fibre weight fraction to volume fraction.",
      "Hand lay-up suits large one-off shapes; filament winding makes tubes and pressure vessels; pultrusion pulls constant sections through a heated die; prepreg cured in an autoclave gives the highest quality. V_f = (w_f ÷ ρ_f) ÷ (w_f ÷ ρ_f + w_m ÷ ρ_m).", "P1", [
       L("mse-composite-fabrication", PR, "Which fabrication route? {{q}}", ["Hand lay-up", "Filament winding", "Pultrusion", "Prepreg and autoclave"], [
         ("A rocket motor case is built by wrapping resin-wetted tow around a rotating mandrel", 1), ("Glass mat and resin are rolled into an open mould for a small boat", 0), ("Ladder rails of constant section are pulled continuously through a heated die", 2),
         ("Pre-impregnated carbon plies are stacked, bagged and cured under heat and pressure for a wing spar", 3), ("A pressure pipe with fibres at ±55 degrees", 1)],
         "Open mould, wound on a mandrel, pulled through a die, or stacked plies under pressure"),
       N("mse-fibre-volume-fraction", PR, "A composite is {{kw}}% fibre by weight; the fibre density is {{kf}} and the matrix {{km}} g/cm³. Find the fibre volume percent.", "(kw/kf)/(kw/kf + (100 - kw)/km)*100",
         f"solve(Eq({M}*(kw/kf + (100 - kw)/km), 100*kw/kf), {M})[0]", "Volumes from 100 g of composite, then the fibre share", tex="V_f",
         cases=C("kw kf km", [(60, 1.80, 1.20), (70, 2.54, 1.15), (50, 1.44, 1.25), (65, 1.80, 1.30), (30, 2.54, 0.90)]))]),
     ("C", X("B11.5") + P_("4I"), "Compute a longitudinal strength and name a composite failure mode.",
      "When the fibres fail first, σ_c = σ_f V_f + σ′_m(1 − V_f), with σ′_m the matrix stress at the fibre failure strain. Across the fibres or between plies the weak matrix and interface decide: matrix cracking, debonding, delamination.", "P1", [
       N("mse-composite-strength", PR, "A composite is {{kv}}% by volume fibres of strength {{ks}} MPa; the matrix carries {{km}} MPa when the fibres break. Find the longitudinal tensile strength in MPa.", "ks*kv/100 + km*(1 - kv/100)",
         f"solve(Eq({M}*100, ks*kv + km*(100 - kv)), {M})[0]", "Rule of mixtures on stress at the fibre failure strain", tex="\\sigma_c",
         cases=C("kv ks km", [(60, 3500, 30), (40, 2400, 45), (55, 4900, 25), (30, 1500, 10), (65, 3100, 60)])),
       L("mse-composite-failure", PR, "Which failure mode? {{q}}", ["Fibre fracture", "Matrix cracking", "Delamination", "Fibre pull-out"], [
         ("Plies separate from one another after an impact", 2), ("Loaded along the fibres, the laminate breaks cleanly across them", 0), ("Loaded across the fibres, cracks run through the resin between them", 1),
         ("Broken fibres slide out of the matrix on the fracture surface, absorbing energy", 3), ("A crack runs between layers at a free edge under bending", 2)],
         "Fibres break, resin cracks, plies part, or fibres slide out")]),
     ("D", X("B11.2") + P_("4I"), "Allow for fibre orientation with an efficiency factor.",
      "E_c = K E_f V_f + E_m V_m, with K = 1 for aligned fibres loaded along their length, 3/8 for fibres random in a plane and 1/5 for fibres random in three dimensions.", "P1", [
       N("mse-orientation-modulus", PR, "A composite is {{kv}}% by volume fibres of modulus {{kf}} GPa in a matrix of {{km}} GPa, with a fibre efficiency factor of {{kk}}. Find its modulus in GPa.", "kk*kf*kv/100 + km*(1 - kv/100)",
         f"solve(Eq({M}*100, kk*kf*kv + km*(100 - kv)), {M})[0]", "Scale the fibre term by the efficiency factor", tex="E_c",
         cases=C("kv kf km kk", [(30, 72.5, 3.5, 0.375), (40, 230, 2.4, 1), (20, 72.5, 2.8, 0.2), (50, 131, 3.0, 0.375), (25, 380, 70, 0.2)])),
       F("mse-orientation-facts", PR, [
         ("A sheet moulding compound with chopped fibres random in the plane is", "equally stiff in every in-plane direction, at about three eighths of the aligned fibre contribution", "stiff in one direction only", "as stiff as an aligned laminate", "stiffest through its thickness"),
         ("A unidirectional ply loaded at 90 degrees to its fibres is", "little stiffer than the matrix alone", "as stiff as along the fibres", "twice as stiff", "rigid"),
         ("Laminates stack plies at 0, +45, −45 and 90 degrees in order to", "carry loads from several directions", "save resin", "raise the density", "make the part thicker only"),
         ("Short fibres reinforce less than continuous ones because", "the ends carry little load, so the average fibre stress is lower", "they are weaker", "they are thicker", "they melt")],
         "Fibres only help along their own length")])]),
   2: ("Inspection, failure analysis and life", [
     ("A", P_("2F", "4E"), "Choose a non-destructive test.",
      "Dye penetrant shows cracks open to the surface. Magnetic particle shows surface and near-surface flaws in ferromagnetic parts. Eddy current finds surface flaws and measures coating thickness on conductors. Ultrasound finds internal flaws and measures thickness. Radiography images internal voids and inclusions.", "P2", [
       L("mse-ndt-choice", PR, "Which non-destructive test? {{q}}", ["Dye penetrant", "Magnetic particle", "Eddy current", "Ultrasonic testing", "Radiography"], [
         ("Find a fine surface crack in an aluminium casting, cheaply", 0), ("Find a crack just under the surface of a steel crankshaft", 1), ("Measure the remaining wall thickness of a pipe from outside", 3),
         ("Image porosity inside a weld on film", 4), ("Scan aircraft skin for cracks at rivet holes without removing paint", 2), ("Find delamination inside a composite panel", 3)],
         "Open to the surface, magnetic, conductive, internal by sound, or internal by image"),
       F("mse-ndt-facts", PR, [
         ("Dye penetrant inspection cannot find", "flaws that do not break the surface", "surface cracks", "pinholes", "laps"),
         ("Magnetic particle inspection works only on", "ferromagnetic materials", "aluminium", "austenitic stainless steel", "polymers"),
         ("Radiography shows a crack poorly when the crack is", "perpendicular to the beam, so the path length barely changes", "parallel to the beam", "filled with tungsten", "very wide"),
         ("An ultrasonic pulse reflects from a flaw because", "the acoustic impedance changes there", "the flaw is magnetic", "the flaw emits sound", "the metal melts"),
         ("A certified material test report lets the buyer check", "that the heat's chemistry and properties meet the specification", "the price", "the delivery date", "the colour")],
         "Each method needs its own kind of contrast")]),
     ("B", P_("1C", "2G"), "Read a fracture surface and order a failure analysis.",
      "Beach marks and striations mean fatigue; dimples mean ductile overload; flat facets with river patterns mean cleavage; a rock-candy surface means intergranular fracture. Chevron marks point back to the origin. Preserve and document first, test non-destructively, and cut samples last.", "P2", [
       L("mse-fractography", PR, "What does this fracture feature indicate? {{q}}", ["Fatigue", "Ductile overload", "Brittle cleavage", "Intergranular fracture"], [
         ("Curved beach marks spreading from one point, with a small rough final zone", 0), ("Cup-like dimples seen in the SEM", 1), ("Flat shiny facets with river patterns", 2),
         ("A rock-candy surface that follows the grain boundaries", 3), ("Fine parallel striations, one per load cycle", 0), ("A dull fibrous surface with heavy necking", 1)],
         "Beach marks, dimples, facets or grain faces"),
       F("mse-failure-analysis-facts", PR, [
         ("The first step in a failure analysis is to", "preserve and record the evidence before anything is cleaned or cut", "section the fracture", "repeat the service loading", "replace the part"),
         ("Chevron marks on a brittle fracture surface", "point back toward the origin of the crack", "point toward the final fracture", "show the grain size", "mean fatigue"),
         ("Why should two fracture halves never be fitted back together?", "Touching them destroys the fine surface features", "They will weld", "They are magnetic", "It changes the chemistry"),
         ("A large final-fracture zone on a fatigue surface suggests", "the part was highly stressed", "the stress was very low", "there was no stress concentration", "corrosion was the cause"),
         ("Destructive tests such as sectioning for metallography are done", "last, after all non-destructive examination", "first", "instead of visual examination", "only on undamaged parts")],
         "Look before you cut")]),
     ("C", P_("2H"), "Sum fatigue damage with Miner's rule.",
      "Damage from n cycles at a level where life is N is n ÷ N; failure is predicted when the fractions sum to 1.", "P1", [
       N("mse-miner-damage", PR, "A part sees {{ka}} cycles at a stress where its life is {{kb}} cycles, and {{kc}} cycles at a stress where its life is {{kd}} cycles. Find the accumulated damage fraction.", "ka/kb + kc/kd",
         "(ka*kd + kc*kb)/(kb*kd)", "Add the life fractions used at each level", tex="D",
         cases=C("ka kb kc kd", [(20000, 100000, 300000, 1000000), (5000, 20000, 40000, 200000), (1000, 8000, 100000, 500000), (60000, 150000, 10000, 40000), (250, 1000, 9000, 60000)])),
       N("mse-miner-remaining", PR, "A part has used {{ka}} cycles at a stress where its life is {{kb}} cycles. How many cycles can it still take at a stress where its life is {{kd}} cycles?", "kd*(1 - ka/kb)",
         f"solve(Eq(ka/kb + {M}/kd, 1), {M})[0]", "Spend the remaining life fraction at the new level", tex="n",
         cases=C("ka kb kd", [(20000, 100000, 1000000), (5000, 20000, 200000), (1000, 8000, 500000), (60000, 150000, 40000), (250, 1000, 60000)]))])])})

UNITS = {1: U1, 2: U2, 3: U3, 4: U4, 5: U5, 6: U6, 7: U7, 8: U8, 9: U9, 10: U10, 11: U11, 12: U12, 13: U13, 14: U14}
ADD = [(f"{FW['code']}-{n}.{tn}.{lo[0]}", qq) for n, u in UNITS.items() for tn, (tt, los) in u[4].items() for lo in los for qq in lo[5]]
