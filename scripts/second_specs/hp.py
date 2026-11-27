"""Anatomy and Physiology (HP, Nov 2026): the two-semester human A&P course. Structure in UNITS (written by
scripts/fw_setup.py), two question types per objective.

Basis: the HAPS Anatomy and Physiology Learning Outcomes (revised fall 2019), read at the level of its modules and
topic headings; the individual outcomes were not read, so read: part, and items are the modules with our own titles.
The outcomes are CC BY-NC-SA: they are a checklist, and every item here is ours. Physiology arithmetic is verified by
solving the defining relation; facts are authored at the level of a standard undergraduate text."""
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "hp-anatomy-physiology", "anatomy-physiology", "P1"
M = "Symbol('m')"
FW = dict(id="anatomy-physiology", title="Anatomy and Physiology", code="HP", domain="hap", track="health", requires=["biology", "chemistry"], level=4,
          primary="haps-ap-2019", also=[], subject="Human Biology",
          note="Anchored on the HAPS Anatomy and Physiology Learning Outcomes (2019), read through its module and topic headings only. Cell biology (module C) and heredity (module S) are left to the Biology framework. Clinical judgment is in NCLEX and INBDE; this is the normal structure and function they assume.",
          header=["The human body system by system, at the level of the two-semester undergraduate course that nursing,",
                  "dental and medical programmes require: name the structure, say what it does, and do the arithmetic",
                  "physiology runs on (cardiac output, filtration pressures, lung volumes, clearance, acid-base)."],
          source=dict(id="haps-ap-outline", title="Anatomy and physiology by HAPS module (course outline)", short="A&P outline", field="biology",
                      note=["The HAPS learning-outcome modules written as a source so the hap.* skills have a home.", "NOT a book: only the module and topic headings were read. Chapter numbers are ours."]))
STDS = [{"id": "haps-ap-2019", "name": "HAPS Anatomy and Physiology Learning Outcomes (revised fall 2019)", "publisher": "Human Anatomy and Physiology Society", "kind": "standard", "read": "part",
         "url": "https://hapsweb.org/wp-content/uploads/2024/09/AP-Learning-Outcomes-PDF.pdf",
         "note": "Read Nov 2026 at the level of the twenty modules and their topic headings; the individual learning outcomes were not read, so read: part. Items are the modules, titled in our words. The outcomes are CC BY-NC-SA and are used as a checklist only: no outcome text is copied. Modules C (chemistry and cell biology) and S (heredity) are answered in the Biology framework and are not cited here.",
         "items": [{"code": c, "title": t} for c, t in [
             ("A", "Body plan and organisation: anatomical position, planes, directional terms, cavities, organ systems"),
             ("B", "Homeostasis: feedback loops and their components"),
             ("C", "Chemistry and cell biology review"),
             ("D", "Histology: the four tissue types and membranes"),
             ("E", "Integumentary system"),
             ("F", "Skeletal system and articulations"),
             ("G", "Muscular system"),
             ("H", "Nervous system"),
             ("I", "General and special senses"),
             ("J", "Endocrine system"),
             ("K", "Cardiovascular system: blood, heart, vessels and pressure"),
             ("L", "Lymphatic system and immunity"),
             ("M", "Respiratory system"),
             ("N", "Digestive system"),
             ("O", "Nutrients and metabolism"),
             ("P", "Urinary system"),
             ("Q", "Fluid, electrolyte and acid-base balance"),
             ("R", "Reproductive system"),
             ("S", "Introduction to heredity"),
             ("T", "Embryology and development")]]}]
SKILLS = [("body-plan", "Anatomical terms, planes, cavities and homeostatic feedback", "Body plan and homeostasis", []),
          ("tissues", "The four tissue types, membranes and the skin", "Tissues and integument", ["hap.body-plan"]),
          ("skeletal", "Bone tissue, the skeleton and joints", "Skeletal system", ["hap.tissues"]),
          ("muscular", "Sarcomeres, excitation-contraction coupling, motor units and muscle actions", "Muscular system", ["hap.skeletal"]),
          ("nervous", "Membrane potentials, synapses, the central, peripheral and autonomic divisions", "Nervous system", ["hap.muscular"]),
          ("senses", "Vision, hearing, equilibrium and the general senses", "Senses", ["hap.nervous"]),
          ("endocrine", "Hormone classes, the pituitary axes and metabolic hormones", "Endocrine system", ["hap.nervous"]),
          ("cardio", "Blood, the heart, vessels, flow and pressure", "Cardiovascular system", ["hap.endocrine"]),
          ("immune", "Lymphatic organs, innate and adaptive immunity", "Lymphatic system and immunity", ["hap.cardio"]),
          ("respiratory", "Ventilation, lung volumes, gas exchange and transport", "Respiratory system", ["hap.cardio"]),
          ("digestive", "The gut tube, secretions, absorption and energy balance", "Digestion and metabolism", ["hap.tissues"]),
          ("renal", "The nephron, filtration, clearance, fluid compartments and acid-base balance", "Urinary system and fluids", ["hap.cardio", "hap.respiratory"]),
          ("repro", "Gametogenesis, the reproductive cycles and early development", "Reproduction and development", ["hap.endocrine"])]
IDEAS = [("FORM", "Structure fits function", "A thin flat cell is for exchange, a thick wall for pressure, a folded surface for area. Naming a structure is half of knowing what it does."),
         ("HOME", "Homeostasis by feedback", "A sensor, a control centre and an effector hold a variable near its set point; most loops are negative and oppose the change."),
         ("GRAD", "Flow follows gradients", "Blood, air, filtrate, ions and water move down pressure, concentration and electrical gradients, and the amount moved is the gradient over the resistance.")]
PRACTICES = [("P1", "Compute", "Carry a physiological relation to a number with its unit."),
             ("P2", "Identify", "Name the structure, the step or the cause from a description.")]
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
BP, TI, SK, MU, NE, SE, EN, CV, IM, RS, DG, RN, RP = ["hap." + s[0] for s in SKILLS]
H = lambda *s: [f"haps-ap-2019:{x}" for x in s]


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def L(name, skill, prompt, options, rows, explain):
    return Q(name, skill, prompt, pace="recall", cases=[{"q": a, "kc": k} for a, k in rows], choice=options, correct="kc", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", **kw):
    return Q(name, skill, prompt, value=value, tex=tex, verify=verify, explain=explain, **kw)


def C(keys, rows):
    return [dict(zip(keys.split(), r)) for r in rows]


UNITS = {
 1: ("body-plan", "Body plan and homeostasis", H("A", "B"), ["FORM", "HOME"], {
   1: ("Anatomical language", [
     ("A", H("A"), "Use directional terms and the anatomical planes.",
      "In anatomical position the body stands facing forward with palms forward. Superior/inferior, anterior/posterior, medial/lateral and proximal/distal are relative terms; sagittal, frontal and transverse planes cut the body into left-right, front-back and top-bottom parts.", "P2", [
       F("hp-directional-terms", BP, [
           ("The wrist is ____ to the elbow.", "distal", "proximal", "medial", "superior"),
           ("The nose is ____ to the ears.", "medial", "lateral", "posterior", "distal"),
           ("The sternum is ____ to the vertebral column.", "anterior", "posterior", "lateral", "inferior"),
           ("The knee is ____ to the ankle.", "proximal", "distal", "lateral", "anterior"),
           ("The skin is ____ to the skeletal muscles.", "superficial", "deep", "medial", "proximal")],
         "Proximal and distal are measured along a limb from its attachment; medial and lateral from the midline"),
       F("hp-planes", BP, [
           ("Which plane divides the body into equal left and right halves?", "midsagittal", "frontal", "transverse", "oblique"),
           ("Which plane divides the body into anterior and posterior parts?", "frontal (coronal)", "sagittal", "transverse", "midsagittal"),
           ("Which plane divides the body into superior and inferior parts?", "transverse", "frontal", "sagittal", "parasagittal"),
           ("A cut parallel to the midline but off-centre is which plane?", "parasagittal", "midsagittal", "frontal", "transverse")],
         "Sagittal separates left from right, frontal separates front from back, transverse separates top from bottom")]),
     ("B", H("A"), "Place organs in body cavities and name their serous membranes.",
      "The dorsal cavity holds the brain and spinal cord. The ventral cavity is split by the diaphragm into the thoracic cavity (pleural cavities, mediastinum with the pericardial cavity) and the abdominopelvic cavity. Serous membranes have a parietal layer on the wall and a visceral layer on the organ.", "P2", [
       F("hp-cavities", BP, [
           ("In which cavity does the heart lie?", "pericardial cavity, within the mediastinum", "pleural cavity", "abdominal cavity", "vertebral canal"),
           ("Which structure separates the thoracic from the abdominopelvic cavity?", "the diaphragm", "the mediastinum", "the peritoneum", "the pelvic brim"),
           ("In which cavity does the spinal cord lie?", "vertebral canal", "cranial cavity", "mediastinum", "pelvic cavity"),
           ("Which organ lies in the pelvic cavity?", "urinary bladder", "stomach", "spleen", "liver")],
         "Thoracic above the diaphragm, abdominopelvic below; the mediastinum is the central block between the lungs"),
       F("hp-serous-membranes", BP, [
           ("Which membrane lies directly on the surface of the lung?", "visceral pleura", "parietal pleura", "visceral pericardium", "parietal peritoneum"),
           ("Which membrane lines the inside of the abdominal wall?", "parietal peritoneum", "visceral peritoneum", "parietal pleura", "mesentery"),
           ("Which membrane forms the outer surface of the heart itself?", "visceral pericardium (epicardium)", "parietal pericardium", "endocardium", "visceral pleura"),
           ("What does the serous fluid between the two layers do?", "reduces friction as organs move", "carries oxygen to the organ", "holds the organ rigid", "forms scar tissue")],
         "Parietal lines the wall, visceral covers the organ; pleura for lungs, pericardium for heart, peritoneum for abdominal organs")])]),
   2: ("Homeostasis", [
     ("A", H("B"), "Name the parts of a feedback loop and tell negative from positive feedback.",
      "A receptor senses the variable, a control centre compares it with a set point, and an effector acts. Negative feedback reverses the change (temperature, glucose, blood pressure); positive feedback amplifies it to an end point (labour, clotting, the upstroke of an action potential).", "P2", [
       L("hp-feedback-sign", BP, "Negative or positive feedback? {{q}}", ["Negative feedback", "Positive feedback"], [
           ("Sweating when body temperature rises", 0), ("Oxytocin strengthening contractions during labour", 1),
           ("Insulin release after a meal lowering blood glucose", 0), ("Platelets recruiting more platelets at a wound", 1),
           ("Heart rate falling when blood pressure rises", 0), ("Sodium entry opening more sodium channels at threshold", 1)],
         "Ask whether the response opposes the change or pushes it further"),
       F("hp-feedback-parts", BP, [
           ("In the baroreceptor reflex, what is the control centre?", "the medulla oblongata", "the carotid sinus", "the heart", "the arterioles"),
           ("When blood glucose rises, which cells are both sensor and control centre?", "pancreatic beta cells", "liver cells", "skeletal muscle fibres", "alpha cells"),
           ("In thermoregulation, which is an effector?", "sweat glands", "skin thermoreceptors", "the hypothalamus", "the set point"),
           ("What is the role of a receptor in a feedback loop?", "detect the change in the variable", "set the target value", "carry out the response", "amplify the stimulus")],
         "Receptor detects, control centre decides, effector acts")])]),
 }),
 2: ("tissues", "Tissues and the integument", H("D", "E"), ["FORM"], {
   1: ("Histology", [
     ("A", H("D"), "Match an epithelium to its location and function.",
      "Epithelia are named by layers (simple, stratified, pseudostratified) and cell shape (squamous, cuboidal, columnar). Thin simple squamous allows exchange; stratified squamous resists abrasion; columnar cells secrete and absorb; transitional epithelium stretches.", "P2", [
       F("hp-epithelium-location", TI, [
           ("Which epithelium lines the alveoli and capillaries?", "simple squamous", "stratified squamous", "simple columnar", "transitional"),
           ("Which epithelium lines the urinary bladder?", "transitional", "simple squamous", "pseudostratified columnar", "simple cuboidal"),
           ("Which epithelium lines the trachea?", "pseudostratified ciliated columnar", "stratified squamous", "simple cuboidal", "transitional"),
           ("Which epithelium lines the small intestine?", "simple columnar with microvilli", "stratified squamous", "simple squamous", "transitional"),
           ("Which epithelium forms the epidermis?", "keratinised stratified squamous", "simple columnar", "transitional", "simple cuboidal")],
         "One thin layer where things cross, many layers where things rub"),
       F("hp-epithelium-function", TI, [
           ("A single layer of flat cells is best suited to what?", "diffusion and filtration", "protection from abrasion", "stretching", "contraction"),
           ("Many layers of cells with flat surface cells are best suited to what?", "protection from abrasion", "rapid diffusion", "absorption", "secretion of mucus"),
           ("What do goblet cells secrete?", "mucus", "keratin", "collagen", "sebum"),
           ("Which feature do all epithelia share?", "they are avascular and rest on a basement membrane", "they contain many blood vessels", "they have abundant extracellular matrix", "they conduct impulses")],
         "Epithelia cover and line; they have a free surface, a basement membrane and no blood vessels of their own")]),
     ("B", H("D"), "Tell the connective, muscle and nervous tissues apart.",
      "Connective tissue is cells scattered in a matrix of fibres and ground substance (loose, dense, cartilage, bone, blood). Skeletal muscle is striated and voluntary, cardiac is striated with intercalated discs, smooth is unstriated. Nervous tissue is neurons and glia.", "P2", [
       F("hp-connective-tissue", TI, [
           ("Which tissue makes up tendons?", "dense regular connective tissue", "hyaline cartilage", "areolar tissue", "elastic cartilage"),
           ("Which cartilage covers the ends of long bones?", "hyaline cartilage", "fibrocartilage", "elastic cartilage", "dense irregular tissue"),
           ("Which cartilage forms the intervertebral discs?", "fibrocartilage", "hyaline cartilage", "elastic cartilage", "compact bone"),
           ("Which cell makes the fibres of connective tissue proper?", "fibroblast", "osteoclast", "mast cell", "macrophage"),
           ("Which connective tissue has a fluid matrix?", "blood", "bone", "adipose", "cartilage")],
         "Regular collagen for pull in one direction; fibrocartilage where compression meets tension"),
       F("hp-muscle-tissue-types", TI, [
           ("Which muscle tissue has intercalated discs?", "cardiac", "skeletal", "smooth", "none of them"),
           ("Which muscle tissue is striated, multinucleate and voluntary?", "skeletal", "cardiac", "smooth", "all three"),
           ("Which muscle tissue has no striations?", "smooth", "skeletal", "cardiac", "all are striated"),
           ("Which cells support and insulate neurons?", "glial cells", "fibroblasts", "chondrocytes", "myocytes")],
         "Striations mean sarcomeres; intercalated discs join cardiac cells electrically and mechanically")])]),
   2: ("Skin", [
     ("A", H("E"), "Name the layers of the skin and what each cell type does.",
      "The epidermis runs from the stratum basale (dividing cells, melanocytes) up through spinosum, granulosum, lucidum (thick skin only) to the dead corneum. The dermis has a papillary and a reticular layer with vessels, nerves, glands and follicles; the hypodermis is fat and loose tissue beneath.", "P2", [
       F("hp-skin-layers", TI, [
           ("In which epidermal layer do keratinocytes divide?", "stratum basale", "stratum corneum", "stratum granulosum", "stratum lucidum"),
           ("Which epidermal layer is found only in thick skin?", "stratum lucidum", "stratum basale", "stratum spinosum", "stratum corneum"),
           ("Which layer of the skin holds the blood vessels, hair follicles and glands?", "dermis", "epidermis", "stratum corneum", "stratum basale"),
           ("Which is the most superficial layer of the epidermis?", "stratum corneum", "stratum basale", "stratum spinosum", "papillary layer")],
         "Basale at the bottom divides; corneum at the top is dead keratin; the dermis carries the supply lines"),
       F("hp-skin-cells", TI, [
           ("Which cell makes the pigment that shields DNA from ultraviolet light?", "melanocyte", "keratinocyte", "tactile (Merkel) cell", "fibroblast"),
           ("Which gland is the main one for cooling the body?", "eccrine sweat gland", "sebaceous gland", "apocrine sweat gland", "ceruminous gland"),
           ("Which vitamin does skin begin to make in sunlight?", "vitamin D", "vitamin C", "vitamin K", "vitamin A"),
           ("When the body is cold, what do dermal blood vessels do?", "constrict, keeping heat in the core", "dilate, losing heat", "leak plasma", "nothing")],
         "Skin protects, regulates temperature, senses and starts vitamin D synthesis")])]),
 }),
 3: ("skeletal", "Skeletal system", H("F"), ["FORM"], {
   1: ("Bone", [
     ("A", H("F"), "Name the cells and structures of bone tissue.",
      "Osteoblasts build matrix, osteocytes maintain it from lacunae, osteoclasts resorb it. Compact bone is built of osteons around central canals; spongy bone is trabeculae holding red marrow. Long bones grow in length at the epiphyseal plate.", "P2", [
       F("hp-bone-cells", SK, [
           ("Which cell breaks down bone matrix?", "osteoclast", "osteoblast", "osteocyte", "chondrocyte"),
           ("Which cell lays down new bone matrix?", "osteoblast", "osteoclast", "osteocyte", "fibroblast"),
           ("Which mature cell sits in a lacuna and maintains the matrix?", "osteocyte", "osteoblast", "osteoclast", "osteogenic cell"),
           ("What is the structural unit of compact bone?", "the osteon", "the trabecula", "the epiphysis", "the lacuna")],
         "Blasts build, clasts cut, cytes keep"),
       F("hp-long-bone", SK, [
           ("Where does a long bone grow in length?", "the epiphyseal plate", "the periosteum", "the medullary cavity", "the articular cartilage"),
           ("What is the shaft of a long bone called?", "diaphysis", "epiphysis", "metaphysis", "periosteum"),
           ("What fills the spaces of spongy bone in the adult hip and sternum?", "red marrow", "yellow marrow", "hyaline cartilage", "synovial fluid"),
           ("Which membrane covers the outer surface of a bone?", "periosteum", "endosteum", "perichondrium", "synovial membrane")],
         "Epiphyses at the ends, diaphysis between, growth plate where they meet")]),
     ("B", H("F", "J"), "Predict how hormones move calcium between bone and blood.",
      "Parathyroid hormone raises blood calcium by stimulating osteoclast activity, renal reabsorption and activation of vitamin D. Calcitonin lowers it weakly by inhibiting osteoclasts. Calcitriol raises intestinal absorption.", "P2", [
       F("hp-calcium-hormones", SK, [
           ("Blood calcium falls. Which hormone is released in response?", "parathyroid hormone", "calcitonin", "thyroxine", "insulin"),
           ("Which hormone inhibits osteoclasts and lowers blood calcium?", "calcitonin", "parathyroid hormone", "calcitriol", "cortisol"),
           ("Which hormone increases calcium absorption from the gut?", "calcitriol (active vitamin D)", "calcitonin", "aldosterone", "glucagon"),
           ("What does parathyroid hormone do to osteoclast activity?", "increases it, releasing calcium", "decreases it", "has no effect on it", "converts osteoclasts to osteoblasts")],
         "PTH pulls calcium into blood from bone, kidney and, through vitamin D, the gut"),
       L("hp-calcium-direction", SK, "What happens to blood calcium? {{q}}", ["It rises", "It falls"], [
           ("Parathyroid hormone secretion increases", 0), ("Osteoclast activity is inhibited", 1), ("Calcitriol production increases", 0),
           ("Osteoblasts deposit matrix faster than osteoclasts remove it", 1), ("The parathyroid glands are removed", 1)],
         "Resorption and absorption raise blood calcium; deposition lowers it")])]),
   2: ("Skeleton and joints", [
     ("A", H("F"), "Classify bones as axial or appendicular and count the vertebrae.",
      "The axial skeleton is the skull, vertebral column, ribs and sternum; the appendicular skeleton is the limbs and their girdles. The column has 7 cervical, 12 thoracic and 5 lumbar vertebrae, then the sacrum and coccyx; there are 12 pairs of ribs, 7 of them true.", "P2", [
       L("hp-axial-appendicular", SK, "Axial or appendicular skeleton? {{q}}", ["Axial", "Appendicular"], [
           ("Sternum", 0), ("Scapula", 1), ("Clavicle", 1), ("Sacrum", 0), ("Hip bone (os coxae)", 1), ("Mandible", 0), ("Patella", 1), ("Hyoid", 0)],
         "Girdles belong with the limbs they carry"),
       F("hp-vertebra-count", SK, [
           ("How many cervical vertebrae are there?", "7", "5", "8", "12"),
           ("How many thoracic vertebrae are there?", "12", "7", "10", "5"),
           ("How many lumbar vertebrae are there?", "5", "7", "4", "12"),
           ("How many pairs of ribs attach directly to the sternum by their own cartilage?", "7", "12", "5", "10"),
           ("How many pairs of floating ribs are there?", "2", "5", "3", "7")],
         "Breakfast at 7, lunch at 12, dinner at 5; 7 true, 3 false and 2 floating pairs of ribs")]),
     ("B", H("F"), "Classify joints and name the movements at synovial joints.",
      "Fibrous and cartilaginous joints allow little or no movement; synovial joints have a cavity, capsule, synovial membrane and articular cartilage. Hinge joints flex and extend; ball-and-socket joints move in all planes; pivot joints rotate.", "P2", [
       F("hp-joint-types", SK, [
           ("What type of synovial joint is the elbow (humerus with ulna)?", "hinge", "ball-and-socket", "pivot", "saddle"),
           ("What type of synovial joint is the hip?", "ball-and-socket", "hinge", "condylar", "plane"),
           ("What type of joint is a skull suture?", "fibrous", "synovial", "cartilaginous (symphysis)", "pivot"),
           ("What type of joint is the atlas on the dens of the axis?", "pivot", "hinge", "saddle", "plane"),
           ("What type of joint is the pubic symphysis?", "cartilaginous", "fibrous", "synovial hinge", "synovial plane")],
         "Shape of the surfaces sets the axes of movement"),
       F("hp-joint-movements", SK, [
           ("Moving the arm away from the midline in the frontal plane is called what?", "abduction", "adduction", "flexion", "pronation"),
           ("Bending the elbow decreases the joint angle. What is this movement?", "flexion", "extension", "abduction", "rotation"),
           ("Turning the palm from anterior to posterior is called what?", "pronation", "supination", "inversion", "eversion"),
           ("Pointing the toes downward is called what?", "plantar flexion", "dorsiflexion", "inversion", "extension")],
         "Flexion closes the angle, abduction leaves the midline, supination holds the soup")])]),
 }),
 4: ("muscular", "Muscular system", H("G"), ["FORM", "GRAD"], {
   1: ("Contraction", [
     ("A", H("G"), "Describe the sarcomere and what changes when it shortens.",
      "A sarcomere runs from Z disc to Z disc. Thin (actin) filaments slide past thick (myosin) filaments: the I band and H zone narrow and the Z discs approach, while the A band keeps its length because no filament shortens.", "P2", [
       L("hp-sarcomere-bands", MU, "During contraction, what happens to the {{q}}?", ["It shortens", "It stays the same length"], [
           ("I band", 0), ("A band", 1), ("H zone", 0), ("distance between Z discs", 0), ("thick filament", 1), ("thin filament", 1)],
         "Filaments slide; they do not shorten. The A band is the length of the thick filament"),
       F("hp-sarcomere-parts", MU, [
           ("Which protein forms the thick filament?", "myosin", "actin", "troponin", "titin"),
           ("Which protein covers the myosin-binding sites on actin at rest?", "tropomyosin", "troponin", "myosin", "dystrophin"),
           ("To which protein does calcium bind to start contraction in skeletal muscle?", "troponin", "tropomyosin", "calmodulin", "myosin"),
           ("What marks the boundary of a sarcomere?", "the Z disc", "the M line", "the H zone", "the A band")],
         "Calcium binds troponin, troponin moves tropomyosin, myosin heads reach actin")]),
     ("B", H("G"), "Order the steps from a motor neuron's action potential to cross-bridge cycling.",
      "Acetylcholine released at the neuromuscular junction opens ligand-gated channels on the motor end plate; the action potential runs down the T tubules and opens the sarcoplasmic reticulum's calcium channels. ATP is needed to detach the myosin head and to pump calcium back.", "P2", [
       F("hp-nmj", MU, [
           ("Which neurotransmitter is released at the neuromuscular junction?", "acetylcholine", "norepinephrine", "dopamine", "glutamate"),
           ("Which enzyme ends the signal at the neuromuscular junction?", "acetylcholinesterase", "monoamine oxidase", "ATP synthase", "creatine kinase"),
           ("What carries the action potential deep into the muscle fibre?", "T tubules", "the sarcoplasmic reticulum", "myofibrils", "gap junctions"),
           ("From where is calcium released to start contraction in skeletal muscle?", "the sarcoplasmic reticulum", "the T tubule lumen", "mitochondria", "the nucleus")],
         "Neuron, acetylcholine, end plate, T tubule, sarcoplasmic reticulum, calcium, troponin"),
       F("hp-crossbridge-atp", MU, [
           ("What does binding of a new ATP do to a myosin head attached to actin?", "detaches it from actin", "causes the power stroke", "releases calcium", "moves tropomyosin"),
           ("Why do muscles stiffen in rigor mortis?", "no ATP is left to detach the cross-bridges", "calcium is absent", "actin is destroyed", "acetylcholine accumulates"),
           ("What does ATP hydrolysis by the myosin head accomplish?", "cocks the head into its high-energy position", "binds calcium to troponin", "opens the end-plate channels", "shortens the thick filament"),
           ("How does the fibre relax after stimulation ends?", "calcium is pumped back into the sarcoplasmic reticulum", "ATP runs out", "myosin is broken down", "sodium leaves the T tubules")],
         "ATP is spent three ways: cocking the head, releasing it, and pumping calcium")]),
     ("C", H("G"), "Relate motor units, summation and fibre types to force and fatigue.",
      "A motor unit is one motor neuron and the fibres it supplies. Force rises by recruiting more units and by stimulating faster (wave summation up to tetanus). Slow oxidative fibres resist fatigue; fast glycolytic fibres are powerful and tire quickly.", "P2", [
       F("hp-motor-units", MU, [
           ("What is a motor unit?", "one motor neuron and all the fibres it supplies", "one sarcomere", "one fascicle", "all neurons to one muscle"),
           ("Which muscles have the smallest motor units?", "those needing fine control, such as eye muscles", "postural muscles of the back", "the quadriceps", "the gluteals"),
           ("How does a muscle increase force without changing stimulation frequency?", "by recruiting more motor units", "by lengthening the sarcomeres", "by reducing calcium", "by lowering ATP use"),
           ("What is a sustained, smooth maximal contraction from rapid stimulation called?", "fused tetanus", "a twitch", "treppe", "the latent period")],
         "Recruitment and frequency are the two controls on force"),
       L("hp-fibre-types", MU, "Slow oxidative or fast glycolytic fibres? {{q}}", ["Slow oxidative (type I)", "Fast glycolytic (type IIx)"], [
           ("Many mitochondria and much myoglobin", 0), ("Large glycogen stores, pale colour", 1), ("Fatigue quickly", 1),
           ("Dominant in postural muscles", 0), ("Largest diameter and greatest power", 1), ("Dense capillary supply", 0)],
         "Red, small and tireless against white, large and brief")])]),
   2: ("Muscles in action", [
     ("A", H("G"), "Name the prime mover for a movement and the role of its antagonist.",
      "The agonist (prime mover) produces the movement, the antagonist opposes it, synergists assist. A muscle pulls its insertion toward its origin and can only pull.", "P2", [
       F("hp-prime-movers", MU, [
           ("Which muscle is the prime mover of elbow extension?", "triceps brachii", "biceps brachii", "brachialis", "deltoid"),
           ("Which muscle group extends the knee?", "quadriceps femoris", "hamstrings", "gastrocnemius", "adductors"),
           ("Which muscle is the prime mover of arm abduction?", "deltoid", "pectoralis major", "latissimus dorsi", "trapezius"),
           ("Which muscle is the main muscle of quiet inspiration?", "diaphragm", "rectus abdominis", "internal intercostals", "pectoralis minor"),
           ("Which muscle plantar flexes the ankle?", "gastrocnemius", "tibialis anterior", "quadriceps femoris", "iliopsoas")],
         "Find the joint crossed and the side of it the muscle lies on"),
       F("hp-muscle-roles", MU, [
           ("During elbow flexion, what is the role of the triceps brachii?", "antagonist", "agonist", "synergist", "fixator"),
           ("What is the less movable attachment of a muscle called?", "origin", "insertion", "belly", "aponeurosis"),
           ("During knee extension, which group is the antagonist?", "hamstrings", "quadriceps", "gluteus maximus", "gastrocnemius alone"),
           ("What is a muscle that stabilises a joint so another can act called?", "fixator", "antagonist", "prime mover", "insertion")],
         "Muscles work in opposed pairs because each can only pull")])]),
 }),
}
UNITS.update({
 5: ("nervous", "Nervous system", H("H"), ["GRAD", "HOME"], {
   1: ("Signals", [
     ("A", H("H"), "Explain the resting potential and compute an equilibrium potential.",
      "The resting membrane is most permeable to potassium, so it sits near the potassium equilibrium potential, about −70 mV; the sodium-potassium pump maintains the gradients. At 37 °C the Nernst potential for a monovalent cation is 61.5 mV × log10(outside/inside).", "P1", [
       N("hp-nernst", NE, "At 37 °C an ion with charge +1 has an outside concentration of {{ko}} mM and an inside concentration of {{ki}} mM. Find its equilibrium potential in mV, using 61.5 mV per tenfold ratio.", "61.5*log10(ko/ki)",
         "Rational(123, 2)*(log(ko) - log(ki))/log(10)", "E = 61.5 log10(out/in). More outside gives a positive potential (sodium), more inside a negative one (potassium)", tex="E", tol=0.01,
         cases=C("ko ki", [(145, 15), (5, 150), (4, 140), (150, 12), (5, 100)])),
       F("hp-resting-potential", NE, [
           ("To which ion is the resting membrane most permeable?", "potassium", "sodium", "calcium", "magnesium"),
           ("What does the sodium-potassium pump move per ATP?", "3 sodium out and 2 potassium in", "2 sodium out and 3 potassium in", "3 sodium in and 2 potassium out", "1 sodium out and 1 potassium in"),
           ("If extracellular potassium rises, what happens to the resting potential?", "it becomes less negative (depolarises)", "it becomes more negative", "it does not change", "it reverses to +60 mV"),
           ("Which ion is far more concentrated outside the cell than inside?", "sodium", "potassium", "phosphate", "protein anions")],
         "The membrane rests near the equilibrium potential of the ion it lets through most easily")]),
     ("B", H("H"), "Follow the phases of an action potential and its conduction.",
      "At threshold voltage-gated sodium channels open (depolarisation), then inactivate while potassium channels open (repolarisation, then hyperpolarisation). The absolute refractory period makes conduction one-way. Myelin and large diameter raise speed; myelinated conduction is saltatory.", "P1", [
       F("hp-action-potential", NE, [
           ("What causes the rising phase of an action potential?", "sodium entering through voltage-gated channels", "potassium leaving the cell", "chloride entering the cell", "the sodium-potassium pump"),
           ("What causes repolarisation?", "potassium leaving through voltage-gated channels", "sodium entering the cell", "calcium leaving the cell", "the pump alone"),
           ("Why can a second action potential not start during the absolute refractory period?", "sodium channels are open or inactivated", "potassium channels are closed", "the membrane is hyperpolarised", "ATP is exhausted"),
           ("Where are action potentials regenerated along a myelinated axon?", "at the nodes of Ranvier", "under the myelin", "only at the axon terminal", "at the dendrites")],
         "Sodium in, then potassium out; inactivation gives the refractory period"),
       N("hp-conduction-time", NE, "A nerve impulse travels {{kd}} m along an axon conducting at {{kv}} m/s. How long does it take, in milliseconds?", "1000*kd/kv", f"solve(Eq({M}*kv/1000, kd), {M})[0]",
         "Time is distance over speed. Large myelinated fibres run near 100 m/s, small unmyelinated fibres near 1 m/s", tex="t",
         cases=C("kd kv", [(1, 50), (0.8, 100), (1.2, 2), (0.5, 20), (1, 80)]))]),
     ("C", H("H"), "Describe a chemical synapse and tell excitatory from inhibitory effects.",
      "An action potential opens voltage-gated calcium channels in the terminal; vesicles release transmitter, which binds postsynaptic receptors. Opening cation channels gives an EPSP; opening chloride or potassium channels gives an IPSP. Potentials sum in time and space at the axon hillock.", "P2", [
       F("hp-synapse-steps", NE, [
           ("Which ion's entry into the axon terminal triggers transmitter release?", "calcium", "sodium", "potassium", "chloride"),
           ("What is the main inhibitory transmitter of the brain?", "GABA", "glutamate", "acetylcholine", "norepinephrine"),
           ("What is the main excitatory transmitter of the brain?", "glutamate", "GABA", "glycine", "serotonin"),
           ("Two EPSPs from different synapses arriving together add. What is this called?", "spatial summation", "temporal summation", "saltatory conduction", "the refractory period")],
         "Calcium in, vesicles out; the receptor, not the transmitter, decides the sign"),
       L("hp-epsp-ipsp", NE, "EPSP or IPSP? {{q}}", ["EPSP (toward threshold)", "IPSP (away from threshold)"], [
           ("Ligand-gated channels open and sodium enters", 0), ("Chloride channels open and chloride enters", 1), ("Potassium channels open and potassium leaves", 1),
           ("The membrane moves from −70 mV to −62 mV", 0), ("The membrane moves from −70 mV to −76 mV", 1)],
         "Depolarising is excitatory; hyperpolarising is inhibitory")])]),
   2: ("Central and peripheral divisions", [
     ("A", H("H"), "Match brain regions to their functions.",
      "Frontal lobe: motor cortex and planning; parietal: somatosensory; occipital: vision; temporal: hearing and memory. The cerebellum coordinates movement, the hypothalamus runs homeostasis and the pituitary, the thalamus relays sensation, the medulla holds cardiac and respiratory centres.", "P2", [
       F("hp-brain-regions", NE, [
           ("Which region coordinates balance and the timing of movement?", "cerebellum", "thalamus", "medulla oblongata", "hypothalamus"),
           ("Which region holds the cardiovascular and respiratory centres?", "medulla oblongata", "cerebellum", "thalamus", "hippocampus"),
           ("Which region controls body temperature, hunger and the pituitary?", "hypothalamus", "thalamus", "pons", "cerebellum"),
           ("Which region relays most sensory input to the cortex?", "thalamus", "hypothalamus", "medulla oblongata", "corpus callosum")],
         "Medulla for vital reflexes, hypothalamus for set points, thalamus for relay, cerebellum for coordination"),
       F("hp-cortex-lobes", NE, [
           ("In which lobe is the primary motor cortex?", "frontal", "parietal", "occipital", "temporal"),
           ("In which lobe is the primary somatosensory cortex?", "parietal", "frontal", "temporal", "occipital"),
           ("In which lobe is the primary visual cortex?", "occipital", "parietal", "frontal", "temporal"),
           ("In which lobe is the primary auditory cortex?", "temporal", "occipital", "frontal", "parietal")],
         "Motor in front of the central sulcus, sensory behind it")]),
     ("B", H("H"), "Trace a spinal reflex and the main spinal pathways.",
      "A reflex arc runs receptor, sensory neuron (dorsal root), integration centre, motor neuron (ventral root), effector. The stretch reflex is monosynaptic. Dorsal columns carry fine touch and proprioception, the spinothalamic tract pain and temperature, the corticospinal tract voluntary movement.", "P2", [
       F("hp-reflex-arc", NE, [
           ("Through which root do sensory fibres enter the spinal cord?", "dorsal root", "ventral root", "ventral ramus", "white ramus"),
           ("How many synapses are there in the knee-jerk (stretch) reflex arc within the cord?", "one", "two", "three", "none"),
           ("Which receptor starts the stretch reflex?", "muscle spindle", "Golgi tendon organ", "free nerve ending", "lamellar corpuscle"),
           ("Where are the cell bodies of sensory neurons found?", "dorsal root ganglia", "ventral horn", "lateral horn", "ventral root")],
         "Sensory in the back, motor out the front"),
       F("hp-spinal-tracts", NE, [
           ("Which pathway carries pain and temperature?", "spinothalamic tract", "dorsal columns", "corticospinal tract", "spinocerebellar tract"),
           ("Which pathway carries fine touch and conscious proprioception?", "dorsal column-medial lemniscus", "spinothalamic tract", "corticospinal tract", "reticulospinal tract"),
           ("Which pathway carries voluntary motor commands?", "corticospinal tract", "spinothalamic tract", "dorsal columns", "spinocerebellar tract"),
           ("Where do most corticospinal fibres cross the midline?", "the pyramids of the medulla", "the thalamus", "the spinal segment where they end", "the corpus callosum")],
         "Ascending tracts are named from cord to target, descending tracts from origin to cord")]),
     ("C", H("H"), "Name the cranial nerves by number and main function.",
      "Twelve pairs: I olfactory, II optic, III oculomotor, IV trochlear, V trigeminal, VI abducens, VII facial, VIII vestibulocochlear, IX glossopharyngeal, X vagus, XI accessory, XII hypoglossal.", "P2", [
       F("hp-cranial-nerve-names", NE, [
           ("Which cranial nerve is number V?", "trigeminal", "facial", "abducens", "trochlear"),
           ("Which cranial nerve is number VII?", "facial", "trigeminal", "vestibulocochlear", "glossopharyngeal"),
           ("Which cranial nerve is number X?", "vagus", "accessory", "hypoglossal", "glossopharyngeal"),
           ("Which cranial nerve is number III?", "oculomotor", "optic", "trochlear", "olfactory"),
           ("Which cranial nerve is number XII?", "hypoglossal", "accessory", "vagus", "glossopharyngeal")],
         "Olfactory, optic, oculomotor, trochlear, trigeminal, abducens, facial, vestibulocochlear, glossopharyngeal, vagus, accessory, hypoglossal"),
       F("hp-cranial-nerve-functions", NE, [
           ("Which nerve carries sensation from the face and moves the muscles of mastication?", "trigeminal (V)", "facial (VII)", "glossopharyngeal (IX)", "hypoglossal (XII)"),
           ("Which nerve moves the muscles of facial expression?", "facial (VII)", "trigeminal (V)", "accessory (XI)", "vagus (X)"),
           ("Which nerve carries parasympathetic fibres to the heart, lungs and gut?", "vagus (X)", "glossopharyngeal (IX)", "accessory (XI)", "facial (VII)"),
           ("Which nerve moves the tongue?", "hypoglossal (XII)", "glossopharyngeal (IX)", "trigeminal (V)", "vagus (X)"),
           ("Which nerve carries hearing and balance?", "vestibulocochlear (VIII)", "facial (VII)", "trigeminal (V)", "abducens (VI)")],
         "V feels the face, VII moves it; X wanders to the viscera")])]),
   3: ("Autonomic division", [
     ("A", H("H"), "Contrast the sympathetic and parasympathetic divisions.",
      "Sympathetic outflow is thoracolumbar with short preganglionic fibres and norepinephrine at most targets; parasympathetic outflow is craniosacral with long preganglionic fibres and acetylcholine on muscarinic receptors. All preganglionic neurons release acetylcholine onto nicotinic receptors.", "P2", [
       L("hp-autonomic-effect", NE, "Sympathetic or parasympathetic? {{q}}", ["Sympathetic", "Parasympathetic"], [
           ("Pupils dilate", 0), ("Heart rate slows", 1), ("Bronchioles dilate", 0), ("Gut motility and secretion increase", 1),
           ("Sweating increases", 0), ("The bladder wall contracts to void", 1), ("Blood flow shifts to skeletal muscle", 0)],
         "Fight or flight against rest and digest"),
       F("hp-autonomic-wiring", NE, [
           ("From which regions does sympathetic outflow leave the central nervous system?", "thoracic and lumbar cord", "brainstem and sacral cord", "cervical cord only", "the cerebellum"),
           ("Which transmitter do all autonomic preganglionic neurons release?", "acetylcholine", "norepinephrine", "epinephrine", "dopamine"),
           ("Which transmitter do most sympathetic postganglionic neurons release?", "norepinephrine", "acetylcholine", "GABA", "serotonin"),
           ("Which receptor does acetylcholine act on at parasympathetic target organs?", "muscarinic", "nicotinic", "alpha-adrenergic", "beta-adrenergic")],
         "Two neurons in series; acetylcholine at every ganglion, the divisions differ at the target")])]),
 }),
 6: ("senses", "Senses", H("I"), ["FORM"], {
   1: ("Special senses", [
     ("A", H("I"), "Trace light through the eye and find the power of a lens.",
      "Light passes the cornea (most of the refraction), aqueous humour, pupil, lens (adjustable focus), vitreous humour and reaches the retina. Rods serve dim light, cones colour and acuity at the fovea. Lens power in diopters is 1 over the focal length in metres.", "P1", [
       F("hp-eye-structures", SE, [
           ("Which structure does most of the bending of light entering the eye?", "cornea", "lens", "vitreous humour", "retina"),
           ("Which photoreceptors give colour vision and sharp detail?", "cones", "rods", "bipolar cells", "ganglion cells"),
           ("Where is visual acuity highest?", "fovea centralis", "optic disc", "peripheral retina", "ciliary body"),
           ("Why is the optic disc a blind spot?", "it has no photoreceptors", "it has only rods", "the lens shades it", "it lies behind the iris"),
           ("To focus on a near object, what does the lens do?", "becomes rounder as the ciliary muscle contracts", "flattens as the ciliary muscle contracts", "moves backward", "stays fixed while the cornea changes")],
         "The cornea does the fixed bending, the lens the fine adjustment"),
       N("hp-lens-power", SE, "A lens brings parallel light to a focus {{kf}} cm behind it. Find its power in diopters.", "100/kf", f"solve(Eq({M}*kf, 100), {M})[0]",
         "Power in diopters is 1 over focal length in metres. The relaxed eye is about 60 D", tex="P",
         cases=C("kf", [(2,), (2.5,), (5,), (10,), (25,), (50,)]))]),
     ("B", H("I"), "Trace sound through the ear and separate hearing from equilibrium.",
      "Sound moves the tympanic membrane, the ossicles (malleus, incus, stapes) and the oval window; hair cells of the spiral organ in the cochlea transduce it, high pitch near the base. The semicircular canals sense rotation, the utricle and saccule linear acceleration and head tilt.", "P2", [
       F("hp-ear-pathway", SE, [
           ("Which ossicle presses on the oval window?", "stapes", "malleus", "incus", "the tympanic membrane itself"),
           ("Where are the receptor cells for hearing?", "the spiral organ in the cochlea", "the semicircular canals", "the tympanic membrane", "the auditory tube"),
           ("Which part of the basilar membrane responds to high-pitched sound?", "the base, near the oval window", "the apex", "all parts equally", "the round window"),
           ("What does the auditory (pharyngotympanic) tube do?", "equalises pressure across the eardrum", "amplifies sound", "senses rotation", "drains endolymph")],
         "Air, bone, fluid, hair cell"),
       L("hp-hearing-equilibrium", SE, "Which structure senses this? {{q}}", ["Cochlea", "Semicircular canals", "Utricle and saccule"], [
           ("The pitch of a tone", 0), ("Turning the head to say no", 1), ("An elevator starting upward", 2), ("The tilt of the head relative to gravity", 2),
           ("Spinning on a chair", 1), ("The loudness of a sound", 0)],
         "Canals for rotation, otolith organs for linear acceleration and gravity")])]),
 }),
 7: ("endocrine", "Endocrine system", H("J"), ["HOME"], {
   1: ("Hormones", [
     ("A", H("J"), "Classify hormones by solubility and predict where their receptors are.",
      "Peptides and catecholamines are water soluble, bind membrane receptors and act through second messengers within seconds to minutes. Steroids and thyroid hormones are lipid soluble, travel on carrier proteins, bind intracellular receptors and change gene transcription.", "P2", [
       L("hp-hormone-solubility", EN, "Where is the receptor for {{q}}?", ["On the cell membrane", "Inside the cell"], [
           ("insulin", 0), ("cortisol", 1), ("epinephrine", 0), ("thyroxine", 1), ("oestradiol", 1), ("glucagon", 0), ("aldosterone", 1), ("antidiuretic hormone", 0)],
         "Steroids and thyroid hormones cross the membrane; peptides and catecholamines do not"),
       F("hp-hormone-mechanisms", EN, [
           ("Which is a common second messenger for peptide hormones?", "cyclic AMP", "ATP synthase", "messenger RNA", "cholesterol"),
           ("How do steroid hormones mainly produce their effects?", "by changing gene transcription", "by opening ion channels directly", "by activating adenylyl cyclase", "by binding haemoglobin"),
           ("Why do steroid hormones last longer in blood than peptides?", "they travel bound to carrier proteins", "they are larger", "they are stored in vesicles", "the kidney cannot filter water"),
           ("From what molecule are steroid hormones made?", "cholesterol", "tyrosine", "glucose", "arachidonic acid")],
         "Solubility decides the receptor's location and the speed of the response")]),
     ("B", H("J"), "Follow a hypothalamic-pituitary axis and predict levels when one gland fails.",
      "The hypothalamus releases hormones into the portal system to the anterior pituitary (TSH, ACTH, FSH, LH, GH, prolactin); the posterior pituitary releases ADH and oxytocin made in the hypothalamus. Target hormones feed back negatively, so a failing target gland gives a high tropic hormone.", "P2", [
       F("hp-pituitary-hormones", EN, [
           ("Which pituitary hormone stimulates the adrenal cortex?", "ACTH", "TSH", "LH", "ADH"),
           ("Which hormones are released from the posterior pituitary?", "ADH and oxytocin", "GH and prolactin", "TSH and ACTH", "FSH and LH"),
           ("Which hypothalamic hormone stimulates TSH release?", "TRH", "CRH", "GnRH", "dopamine"),
           ("How do hypothalamic releasing hormones reach the anterior pituitary?", "through the hypophyseal portal vessels", "down axons", "through the general circulation only", "through cerebrospinal fluid")],
         "Releasing hormone, tropic hormone, target hormone, with feedback at each level"),
       F("hp-axis-feedback", EN, [
           ("The thyroid gland itself fails. What happens to TSH?", "it rises, because feedback is lost", "it falls", "it is unchanged", "it disappears"),
           ("The anterior pituitary fails. What happens to cortisol and ACTH?", "both are low", "cortisol low, ACTH high", "both are high", "cortisol high, ACTH low"),
           ("A person takes large doses of a cortisol-like drug. What happens to their own ACTH?", "it falls", "it rises", "it is unchanged", "it doubles"),
           ("The adrenal cortex fails. What happens to ACTH?", "it rises", "it falls", "it is unchanged", "it falls to zero")],
         "Low target hormone with high tropic hormone points at the target gland; both low points upstream")]),
     ("C", H("J"), "Predict the hormonal response to a change in blood glucose.",
      "Insulin from beta cells lowers glucose by moving it into muscle and fat and storing it as glycogen and fat. Glucagon from alpha cells raises it by glycogenolysis and gluconeogenesis in the liver; epinephrine, cortisol and growth hormone also raise it.", "P2", [
       L("hp-glucose-hormone", EN, "Does {{q}} raise or lower blood glucose?", ["Raises it", "Lowers it"], [
           ("glucagon", 0), ("insulin", 1), ("cortisol", 0), ("epinephrine", 0), ("growth hormone", 0)],
         "One hormone lowers glucose; several raise it"),
       F("hp-glucose-actions", EN, [
           ("Which pancreatic cells secrete insulin?", "beta cells", "alpha cells", "delta cells", "acinar cells"),
           ("What is glucagon's main target organ?", "liver", "skeletal muscle", "brain", "kidney"),
           ("What does insulin do in skeletal muscle?", "moves glucose transporters to the membrane", "breaks down glycogen", "starts gluconeogenesis", "releases fatty acids"),
           ("During an overnight fast, which process in the liver first maintains blood glucose?", "glycogenolysis", "glycogenesis", "lipogenesis", "glycolysis")],
         "Fed state stores under insulin; fasted state releases under glucagon")])]),
 }),
 8: ("cardio", "Cardiovascular system", H("K"), ["GRAD", "HOME"], {
   1: ("Blood", [
     ("A", H("K"), "Describe the composition of blood and find the haematocrit.",
      "Blood is about 55% plasma and 45% formed elements. Haematocrit is the fraction of blood volume that is red cells. Erythrocytes carry gases, neutrophils are the commonest leukocyte, platelets are fragments of megakaryocytes.", "P1", [
       N("hp-haematocrit", CV, "A centrifuged blood sample has a total column height of {{kt}} mm and a packed red cell column of {{kr}} mm. Find the haematocrit in percent.", "100*kr/kt", f"solve(Eq({M}*kt/100, kr), {M})[0]",
         "Haematocrit is red cell volume over total volume. The usual adult range is roughly 37 to 52%", tex="Hct",
         cases=C("kt kr", [(60, 27), (50, 21), (80, 34), (60, 18), (50, 26)])),
       F("hp-formed-elements", CV, [
           ("Which is the most abundant leukocyte?", "neutrophil", "lymphocyte", "eosinophil", "basophil"),
           ("From which cell do platelets form?", "megakaryocyte", "erythroblast", "monocyte", "lymphoblast"),
           ("Which hormone stimulates red cell production, and from which organ?", "erythropoietin from the kidney", "thrombopoietin from the spleen", "erythropoietin from the liver only", "renin from the kidney"),
           ("Which is the most abundant plasma protein?", "albumin", "fibrinogen", "immunoglobulin G", "transferrin"),
           ("Which leukocyte leaves the blood to become a macrophage?", "monocyte", "neutrophil", "basophil", "lymphocyte")],
         "Never Let Monkeys Eat Bananas orders leukocytes from most to least common")]),
     ("B", H("K"), "Order the steps of haemostasis.",
      "Vascular spasm, then a platelet plug on exposed collagen (with von Willebrand factor), then coagulation: the intrinsic and extrinsic pathways meet at factor X, prothrombin becomes thrombin and thrombin turns fibrinogen into fibrin. Plasmin later dissolves the clot.", "P2", [
       F("hp-haemostasis-steps", CV, [
           ("What is the first response of a cut vessel?", "vascular spasm", "fibrin formation", "fibrinolysis", "platelet plug retraction"),
           ("What converts fibrinogen to fibrin?", "thrombin", "plasmin", "factor XII", "heparin"),
           ("At which factor do the intrinsic and extrinsic pathways join?", "factor X", "factor VIII", "factor XII", "factor VII"),
           ("Which enzyme dissolves a clot?", "plasmin", "thrombin", "prothrombinase", "tissue factor")],
         "Spasm, plug, clot, then repair and fibrinolysis"),
       F("hp-clotting-needs", CV, [
           ("Which vitamin is needed to make several clotting factors?", "vitamin K", "vitamin C", "vitamin D", "vitamin B12"),
           ("Which ion is required at several steps of coagulation?", "calcium", "sodium", "potassium", "chloride"),
           ("Which organ makes most clotting factors?", "liver", "spleen", "kidney", "bone marrow"),
           ("What starts the extrinsic pathway?", "tissue factor from damaged tissue", "contact with glass", "plasmin", "antithrombin")],
         "Liver, vitamin K and calcium are the three supplies clotting cannot do without")])]),
   2: ("Heart", [
     ("A", H("K"), "Trace blood through the heart and name the valves and sounds.",
      "Right atrium, tricuspid valve, right ventricle, pulmonary valve, lungs, left atrium, mitral valve, left ventricle, aortic valve, body. The first heart sound is the atrioventricular valves closing, the second the semilunar valves closing.", "P2", [
       F("hp-heart-path", CV, [
           ("Blood leaving the right ventricle passes through which valve?", "pulmonary valve", "tricuspid valve", "mitral valve", "aortic valve"),
           ("Which chamber receives oxygenated blood from the lungs?", "left atrium", "right atrium", "left ventricle", "right ventricle"),
           ("Which valve lies between the left atrium and left ventricle?", "mitral (bicuspid) valve", "tricuspid valve", "aortic valve", "pulmonary valve"),
           ("Which vessels carry oxygenated blood toward the heart?", "pulmonary veins", "pulmonary arteries", "venae cavae", "coronary sinus"),
           ("Which chamber has the thickest wall?", "left ventricle", "right ventricle", "left atrium", "right atrium")],
         "Right side to the lungs, left side to the body; arteries leave, veins return"),
       F("hp-heart-sounds", CV, [
           ("What produces the first heart sound?", "closure of the atrioventricular valves", "closure of the semilunar valves", "opening of the aortic valve", "atrial contraction"),
           ("What produces the second heart sound?", "closure of the semilunar valves", "closure of the atrioventricular valves", "ventricular filling", "opening of the mitral valve"),
           ("What prevents the atrioventricular valves from everting into the atria?", "chordae tendineae and papillary muscles", "the semilunar cusps", "the fibrous pericardium", "the interatrial septum"),
           ("During ventricular ejection, which valves are open?", "the semilunar valves", "the atrioventricular valves", "all four", "none")],
         "Valves open and close on pressure differences alone")]),
     ("B", H("K"), "Follow the conduction system and read the waves of an ECG.",
      "SA node, atria, AV node (delay), AV bundle, bundle branches, Purkinje fibres. The P wave is atrial depolarisation, the QRS complex ventricular depolarisation, the T wave ventricular repolarisation. Heart rate in beats per minute is 60 over the R-R interval in seconds.", "P1", [
       F("hp-ecg-waves", CV, [
           ("What does the P wave represent?", "atrial depolarisation", "ventricular depolarisation", "ventricular repolarisation", "atrial repolarisation"),
           ("What does the QRS complex represent?", "ventricular depolarisation", "atrial depolarisation", "ventricular repolarisation", "AV node delay"),
           ("What does the T wave represent?", "ventricular repolarisation", "atrial repolarisation", "ventricular depolarisation", "SA node firing"),
           ("Where does the heartbeat normally begin?", "the SA node", "the AV node", "the Purkinje fibres", "the AV bundle"),
           ("What is the purpose of the delay at the AV node?", "to let the ventricles fill before they contract", "to stop the atria contracting", "to speed conduction", "to repolarise the atria")],
         "P for atria, QRS for ventricles firing, T for ventricles recovering"),
       N("hp-rate-from-rr", CV, "On an ECG the R-R interval is {{kr}} s. Find the heart rate in beats per minute.", "60/kr", f"solve(Eq({M}*kr, 60), {M})[0]",
         "Rate is 60 divided by the seconds per beat", tex="HR",
         cases=C("kr", [(0.8,), (1,), (0.6,), (1.2,), (0.5,), (0.75,)]))]),
     ("C", H("K"), "Compute cardiac output, stroke volume and ejection fraction.",
      "Stroke volume is end-diastolic minus end-systolic volume; cardiac output is heart rate times stroke volume; ejection fraction is stroke volume over end-diastolic volume. Preload, contractility and afterload set stroke volume.", "P1", [
       N("hp-cardiac-output", CV, "A heart beats {{kh}} times per minute with a stroke volume of {{ks}} mL. Find the cardiac output in L/min.", "kh*ks/1000", f"solve(Eq({M}*1000/kh, ks), {M})[0]",
         "CO = HR × SV. About 5 L/min at rest", tex="CO",
         cases=C("kh ks", [(70, 70), (60, 85), (150, 110), (90, 60), (75, 80)])),
       N("hp-ejection-fraction", CV, "A ventricle holds {{ka}} mL at the end of diastole and {{kb}} mL at the end of systole. Find the ejection fraction in percent.", "100*(ka - kb)/ka", f"solve(Eq(ka*(1 - {M}/100), kb), {M})[0]",
         "EF = (EDV − ESV)/EDV. A healthy ventricle ejects a little over half of what it holds", tex="EF",
         cases=C("ka kb", [(120, 50), (130, 60), (150, 100), (140, 56), (110, 44)]))])]),
   3: ("Vessels and pressure", [
     ("A", H("K"), "Relate flow, pressure and resistance, and the effect of vessel radius.",
      "Flow equals the pressure difference over resistance, so mean arterial pressure is about cardiac output times total peripheral resistance. Resistance varies with the inverse fourth power of radius, which is why arterioles control flow.", "P1", [
       N("hp-map-from-co", CV, "Cardiac output is {{kq}} L/min and total peripheral resistance is {{kr}} mmHg·min/L. Taking venous pressure as negligible, find the mean arterial pressure in mmHg.", "kq*kr", f"solve(Eq({M}/kr, kq), {M})[0]",
         "Pressure difference = flow × resistance", tex="MAP",
         cases=C("kq kr", [(5, 18), (6, 15), (4, 25), (5, 20), (8, 11)])),
       N("hp-radius-flow", CV, "An arteriole's radius changes to {{kf}} times its original value while the pressure difference stays the same. By what factor does the flow through it change?", "kf^4", "(pi*(kf*Y)**4/8)/(pi*Y**4/8)",
         "Poiseuille: flow goes as radius to the fourth power, so small changes in calibre move flow a great deal", tex="factor",
         cases=C("kf", [(2,), (0.5,), (1.5,), (0.8,), (1.2,)]))]),
     ("B", H("K"), "Find the net filtration pressure across a capillary wall.",
      "Net filtration pressure = (capillary hydrostatic − interstitial hydrostatic) − (plasma colloid osmotic − interstitial colloid osmotic). Positive values filter fluid out, negative values draw it in; the lymphatics return the excess.", "P1", [
       N("hp-capillary-nfp", CV, "At one point in a capillary the hydrostatic pressure is {{ka}} mmHg inside and {{kb}} mmHg in the interstitium; the colloid osmotic pressure is {{kp}} mmHg in plasma and {{kq}} mmHg in the interstitium. Find the net filtration pressure in mmHg (positive outward).", "(ka - kb) - (kp - kq)",
         f"solve(Eq(ka - kb - {M}, kp - kq), {M})[0]", "Hydrostatic difference pushes out, colloid osmotic difference pulls in", tex="NFP",
         cases=C("ka kb kp kq", [(35, 0, 26, 1), (17, 0, 26, 1), (30, 2, 25, 3), (40, 1, 28, 2), (15, 1, 25, 2)])),
       F("hp-oedema-causes", CV, [
           ("Plasma albumin falls. Why does oedema follow?", "plasma colloid osmotic pressure falls", "capillary hydrostatic pressure falls", "lymph flow stops", "capillaries become impermeable"),
           ("Venous pressure rises in the legs. Why does oedema follow?", "capillary hydrostatic pressure rises", "plasma proteins rise", "arterioles constrict", "interstitial pressure falls to zero"),
           ("Lymph nodes are removed from the armpit. Why may the arm swell?", "filtered fluid and protein are not returned", "arterial pressure rises", "albumin synthesis falls", "capillaries rupture"),
           ("At the arterial end of a typical capillary, which way does fluid move?", "out, by net filtration", "in, by net reabsorption", "no net movement", "into the lymphatics directly")],
         "Each cause of oedema moves one of the four Starling pressures or blocks lymph")]),
     ("C", H("K"), "Predict the reflex and hormonal responses to a change in blood pressure.",
      "Baroreceptors in the carotid sinus and aortic arch report to the medulla: a fall in pressure raises sympathetic output (heart rate, contractility, vasoconstriction). Over hours the kidney's renin starts the angiotensin-aldosterone system, and ADH retains water.", "P2", [
       F("hp-baroreflex", CV, [
           ("Blood pressure falls on standing. What does the baroreflex do?", "raises heart rate and constricts arterioles", "slows the heart and dilates arterioles", "releases atrial natriuretic peptide", "nothing for several hours"),
           ("Where are the main arterial baroreceptors?", "the carotid sinuses and aortic arch", "the right atrium only", "the renal arteries", "the medulla"),
           ("Blood pressure rises suddenly. What happens to parasympathetic output to the heart?", "it increases", "it decreases", "it is unchanged", "it stops"),
           ("Which hormone is released by the atria when they are stretched?", "atrial natriuretic peptide", "aldosterone", "renin", "ADH")],
         "The baroreflex is a negative feedback loop acting within a heartbeat or two"),
       F("hp-raas", CV, [
           ("Which organ releases renin?", "kidney", "liver", "lung", "adrenal cortex"),
           ("What does angiotensin-converting enzyme produce?", "angiotensin II", "angiotensin I", "renin", "aldosterone"),
           ("What does aldosterone do in the kidney?", "increases sodium reabsorption and potassium secretion", "increases water permeability of the collecting duct", "decreases sodium reabsorption", "dilates the afferent arteriole"),
           ("What is the direct effect of angiotensin II on arterioles?", "vasoconstriction", "vasodilation", "no effect", "increased permeability")],
         "Renin, angiotensin I, angiotensin II, aldosterone: salt and water kept, vessels narrowed")])]),
 }),
})
UNITS.update({
 9: ("immune", "Lymphatic system and immunity", H("L"), ["HOME"], {
   1: ("Defence", [
     ("A", H("L"), "Trace lymph back to the blood and name the lymphoid organs.",
      "Lymphatic capillaries collect excess interstitial fluid; lymph passes through nodes to the thoracic duct (most of the body) or the right lymphatic duct, which empty into the subclavian veins. Bone marrow and thymus are primary lymphoid organs; nodes, spleen and tonsils are secondary.", "P2", [
       F("hp-lymph-flow", IM, [
           ("Into which vessels does lymph finally drain?", "the subclavian veins", "the aorta", "the hepatic portal vein", "the pulmonary veins"),
           ("Which duct drains the lower body and the left upper body?", "thoracic duct", "right lymphatic duct", "cisterna chyli only", "the lacteals"),
           ("What moves lymph along its vessels?", "muscle and breathing movements with one-way valves", "the heart's pumping", "gravity alone", "cilia"),
           ("What do the lacteals of the small intestine absorb?", "dietary fats as chylomicrons", "glucose", "amino acids", "water only")],
         "Lymph is filtered plasma on its way back to the veins"),
       F("hp-lymphoid-organs", IM, [
           ("Where do T lymphocytes mature?", "thymus", "bone marrow", "spleen", "lymph nodes"),
           ("Where do B lymphocytes mature?", "bone marrow", "thymus", "tonsils", "liver"),
           ("Which organ filters blood and removes old red cells?", "spleen", "thymus", "lymph node", "appendix"),
           ("Which structures filter lymph?", "lymph nodes", "the spleen", "the thymus", "red marrow")],
         "Primary organs make and train lymphocytes; secondary organs are where they meet antigen")]),
     ("B", H("L"), "Name the innate defences and the signs of inflammation.",
      "Barriers (skin, mucus, acid), phagocytes (neutrophils, macrophages), natural killer cells, complement, interferons, fever and inflammation act without prior exposure. Inflammation shows redness, heat, swelling and pain from vasodilation and increased permeability.", "P2", [
       F("hp-innate-cells", IM, [
           ("Which cell arrives first in large numbers at a bacterial infection?", "neutrophil", "plasma cell", "cytotoxic T cell", "memory B cell"),
           ("Which innate lymphocyte kills virus-infected cells without prior sensitisation?", "natural killer cell", "helper T cell", "plasma cell", "mast cell"),
           ("Which proteins do virus-infected cells release to protect their neighbours?", "interferons", "antibodies", "complement", "histamine"),
           ("What does the membrane attack complex of complement do?", "punches pores in a target cell's membrane", "presents antigen", "produces antibodies", "raises body temperature")],
         "Innate defences are fast, the same every time and keep no memory"),
       F("hp-inflammation", IM, [
           ("Which chemical released by mast cells causes vasodilation and leaky capillaries?", "histamine", "interferon", "perforin", "immunoglobulin G"),
           ("Why is an inflamed area red and warm?", "increased blood flow from vasodilation", "reduced blood flow", "bacterial pigments", "nerve damage"),
           ("Why does an inflamed area swell?", "plasma leaks from more permeable capillaries", "lymph vessels dilate", "cells divide rapidly", "blood clots in the arteries"),
           ("What is the movement of leukocytes toward chemical signals called?", "chemotaxis", "opsonisation", "diapedesis", "agglutination")],
         "Vasodilation gives redness and heat; permeability gives swelling")]),
     ("C", H("L"), "Assign roles to the cells and antibodies of adaptive immunity.",
      "B cells become plasma cells that secrete antibody (humoral immunity). Helper T cells (CD4) read antigen on MHC II and direct the response; cytotoxic T cells (CD8) read MHC I and kill infected cells. IgM comes first, IgG is most abundant and crosses the placenta, IgA is in secretions, IgE drives allergy.", "P2", [
       F("hp-adaptive-cells", IM, [
           ("Which cell secretes antibodies?", "plasma cell", "helper T cell", "cytotoxic T cell", "macrophage"),
           ("Which cell kills virus-infected body cells by recognising antigen on MHC I?", "cytotoxic T cell (CD8)", "helper T cell (CD4)", "plasma cell", "B cell"),
           ("Which cell activates both B cells and cytotoxic T cells with cytokines?", "helper T cell (CD4)", "natural killer cell", "neutrophil", "plasma cell"),
           ("On which molecule do dendritic cells show antigen to helper T cells?", "MHC class II", "MHC class I", "immunoglobulin M", "complement C3")],
         "CD4 reads MHC II and helps; CD8 reads MHC I and kills (4 × 2 = 8 = 8 × 1)"),
       F("hp-antibody-classes", IM, [
           ("Which antibody class crosses the placenta?", "IgG", "IgM", "IgA", "IgE"),
           ("Which antibody class is made first in a primary response?", "IgM", "IgG", "IgA", "IgD"),
           ("Which antibody class is found in tears, saliva and breast milk?", "IgA", "IgG", "IgE", "IgM"),
           ("Which antibody class binds mast cells and triggers allergic reactions?", "IgE", "IgA", "IgG", "IgM")],
         "M first, G most and through the placenta, A in secretions, E in allergy")]),
     ("D", H("L"), "Tell primary from secondary responses and active from passive immunity.",
      "A first exposure gives a slow, small, mostly IgM response and leaves memory cells; a second gives a fast, large, mostly IgG response. Active immunity is made by one's own cells (infection, vaccine) and lasts; passive immunity is borrowed antibody (placenta, milk, antiserum) and fades.", "P2", [
       L("hp-active-passive", IM, "Which kind of immunity? {{q}}", ["Natural active", "Artificial active", "Natural passive", "Artificial passive"], [
           ("Recovering from chickenpox", 0), ("Receiving a measles vaccine", 1), ("Antibodies crossing the placenta", 2), ("An injection of antivenom", 3),
           ("IgA in breast milk", 2), ("A tetanus toxoid booster", 1), ("Immune globulin given after a rabies exposure", 3)],
         "Active means your own lymphocytes responded; artificial means it was given on purpose"),
       F("hp-primary-secondary", IM, [
           ("Compared with the primary response, how does the secondary antibody response differ?", "faster, larger and mainly IgG", "slower and mainly IgM", "the same size but shorter", "smaller because antigen is cleared"),
           ("Which cells make the secondary response faster?", "memory cells", "neutrophils", "plasma cells from the first exposure", "natural killer cells"),
           ("Why does passive immunity fade within weeks to months?", "the borrowed antibodies are broken down and no memory cells exist", "memory cells die", "the antigen mutates", "the thymus shrinks"),
           ("What is the lag before antibody appears in a primary response?", "several days", "a few minutes", "several months", "there is none")],
         "Memory is the whole point of a vaccine")])]),
 }),
 10: ("respiratory", "Respiratory system", H("M"), ["GRAD"], {
   1: ("Breathing and gas exchange", [
     ("A", H("M"), "Explain ventilation with Boyle's law.",
      "Contracting the diaphragm and external intercostals enlarges the thorax; alveolar pressure falls below atmospheric and air flows in. Quiet expiration is passive recoil. At constant temperature, pressure times volume is constant.", "P1", [
       N("hp-boyle-lung", RS, "A sealed sample of gas at {{kp}} mmHg expands from {{ka}} mL to {{kb}} mL at constant temperature. Find its new pressure in mmHg.", "kp*ka/kb", f"solve(Eq({M}*kb, kp*ka), {M})[0]",
         "P1V1 = P2V2: a larger volume means a lower pressure, which is what draws air in", tex="P_2",
         cases=C("kp ka kb", [(760, 2400, 2500), (760, 500, 400), (760, 3000, 3040), (750, 2000, 2500), (760, 1000, 950)])),
       F("hp-ventilation-mechanics", RS, [
           ("During quiet inspiration, what does the diaphragm do?", "contracts and flattens", "relaxes and domes upward", "does not move", "is pulled up by the lungs"),
           ("What drives quiet expiration?", "elastic recoil of the lungs and chest wall", "contraction of the diaphragm", "contraction of the external intercostals", "positive pressure from the heart"),
           ("Which substance lowers surface tension in the alveoli?", "surfactant", "mucus", "pleural fluid", "elastin"),
           ("Why does the lung stay expanded against the chest wall?", "intrapleural pressure is below alveolar pressure", "the pleural cavity is filled with air", "the bronchi are rigid", "surfactant glues it there")],
         "Volume changes first; pressure and flow follow")]),
     ("B", H("M"), "Combine lung volumes and find alveolar ventilation.",
      "Vital capacity = tidal + inspiratory reserve + expiratory reserve volume; total lung capacity adds the residual volume. Minute ventilation is tidal volume times rate; alveolar ventilation subtracts the anatomical dead space (about 150 mL) from each breath.", "P1", [
       N("hp-vital-capacity", RS, "A person has a tidal volume of {{ka}} mL, an inspiratory reserve volume of {{kb}} mL, an expiratory reserve volume of {{kd}} mL and a residual volume of {{kr}} mL. Find the vital capacity in mL.", "ka + kb + kd",
         f"solve(Eq({M} + kr, ka + kb + kd + kr), {M})[0]", "Vital capacity is everything that can be moved; the residual volume cannot be exhaled", tex="VC",
         cases=C("ka kb kd kr", [(500, 3100, 1200, 1200), (500, 1900, 700, 1100), (600, 3000, 1100, 1200), (450, 2500, 1000, 1150)])),
       N("hp-alveolar-ventilation", RS, "A person breathes {{kf}} times per minute with a tidal volume of {{ka}} mL and a dead space of {{kd}} mL. Find the alveolar ventilation in mL/min.", "kf*(ka - kd)",
         f"solve(Eq({M} + kf*kd, kf*ka), {M})[0]", "Only the air beyond the dead space reaches the alveoli, so deep slow breathing ventilates better than shallow fast breathing", tex="V_A",
         cases=C("kf ka kd", [(12, 500, 150), (20, 300, 150), (10, 600, 150), (30, 200, 150), (15, 450, 150)]))]),
     ("C", H("M"), "Find partial pressures and predict shifts of the oxygen dissociation curve.",
      "A gas's partial pressure is its fraction times the total pressure of dry gas; inspired air is humidified, so subtract water vapour (47 mmHg at 37 °C). Raised carbon dioxide, acidity, temperature and 2,3-BPG shift the haemoglobin curve right, releasing more oxygen to tissue.", "P1", [
       N("hp-inspired-po2", RS, "Barometric pressure is {{kp}} mmHg and the inspired oxygen fraction is {{kf}}. Find the partial pressure of oxygen in humidified tracheal air, taking water vapour as 47 mmHg.", "kf*(kp - 47)",
         f"solve(Eq({M}/kf + 47, kp), {M})[0]", "Subtract water vapour first, then take the oxygen fraction: about 150 mmHg at sea level on room air", tex="P_{O_2}",
         cases=C("kp kf", [(760, 0.21), (760, 0.4), (523, 0.21), (760, 1), (630, 0.21)])),
       L("hp-o2-curve-shift", RS, "Which way does the oxygen-haemoglobin curve shift? {{q}}", ["Right (oxygen released more easily)", "Left (oxygen held more tightly)"], [
           ("Blood pH falls", 0), ("Temperature rises in working muscle", 0), ("Carbon dioxide partial pressure falls", 1),
           ("2,3-BPG rises at altitude", 0), ("Fetal haemoglobin replaces adult haemoglobin", 1), ("Blood becomes more alkaline", 1)],
         "Working tissue is hot, acidic and full of carbon dioxide, and all three push the curve right")]),
     ("D", H("M"), "Describe how carbon dioxide is carried and how breathing is controlled.",
      "Most carbon dioxide travels as bicarbonate made in red cells by carbonic anhydrase, some on haemoglobin, a little dissolved. Central chemoreceptors in the medulla respond to carbon dioxide through the pH of cerebrospinal fluid and set the normal drive; peripheral chemoreceptors respond to low oxygen.", "P2", [
       F("hp-co2-transport", RS, [
           ("In what form is most carbon dioxide carried in blood?", "bicarbonate ion", "dissolved gas", "carbaminohaemoglobin", "carbonic acid"),
           ("Which enzyme speeds the reaction of carbon dioxide with water in red cells?", "carbonic anhydrase", "catalase", "haemoglobin reductase", "ATP synthase"),
           ("Which ion enters the red cell as bicarbonate leaves?", "chloride", "sodium", "potassium", "calcium"),
           ("What happens to blood pH if carbon dioxide is retained?", "it falls", "it rises", "it is unchanged", "it rises then falls")],
         "CO2 + H2O gives H+ and bicarbonate; retaining one side of that equation makes acid"),
       F("hp-breathing-control", RS, [
           ("What is the main stimulus to breathe in a healthy person at rest?", "rising arterial carbon dioxide", "falling arterial oxygen", "rising arterial oxygen", "falling blood glucose"),
           ("Where are the central chemoreceptors?", "the medulla oblongata", "the carotid bodies", "the lungs", "the cerebral cortex"),
           ("What do the peripheral chemoreceptors of the carotid bodies mainly sense?", "a large fall in arterial oxygen", "blood pressure", "blood glucose", "lung stretch"),
           ("A person hyperventilates. What happens to arterial carbon dioxide and pH?", "carbon dioxide falls and pH rises", "carbon dioxide rises and pH falls", "both fall", "both rise")],
         "Carbon dioxide, not oxygen, sets the breath-to-breath drive")])]),
 }),
 11: ("digestive", "Digestion and metabolism", H("N", "O"), ["FORM", "GRAD"], {
   1: ("Digestive system", [
     ("A", H("N"), "Name the layers of the gut wall and the types of motility.",
      "From the lumen out: mucosa, submucosa, muscularis externa (inner circular, outer longitudinal), serosa. The submucosal and myenteric plexuses form the enteric nervous system. Peristalsis propels; segmentation mixes.", "P2", [
       F("hp-gut-layers", DG, [
           ("Which layer of the gut wall touches the lumen?", "mucosa", "serosa", "submucosa", "muscularis externa"),
           ("Which plexus mainly controls gut motility?", "myenteric plexus", "submucosal plexus", "brachial plexus", "coeliac ganglion alone"),
           ("Which layer carries the larger blood vessels and the glands of the duodenum?", "submucosa", "mucosa", "serosa", "muscularis externa"),
           ("How is the stomach's muscularis different from the rest of the tract?", "it has a third, oblique layer", "it has no circular layer", "it is skeletal muscle", "it lacks a plexus")],
         "Mucosa, submucosa, muscularis, serosa, from inside out"),
       F("hp-gut-motility", DG, [
           ("Which movement propels food along the tract?", "peristalsis", "segmentation", "mastication", "haustral churning only"),
           ("Which movement mainly mixes chyme with secretions in the small intestine?", "segmentation", "peristalsis", "deglutition", "mass movement"),
           ("Which sphincter controls emptying of the stomach?", "pyloric sphincter", "lower oesophageal sphincter", "ileocaecal valve", "hepatopancreatic sphincter"),
           ("What effect does parasympathetic activity have on the gut?", "increases motility and secretion", "decreases motility and secretion", "none", "closes all sphincters")],
         "Peristalsis moves, segmentation mixes")]),
     ("B", H("N"), "Match secretions and enzymes to what they digest.",
      "Salivary and pancreatic amylase digest starch; pepsin (from chief cells' pepsinogen, activated by parietal cells' acid) starts protein digestion; pancreatic trypsin, lipase and brush-border enzymes finish; bile salts emulsify fat.", "P2", [
       F("hp-enzymes", DG, [
           ("Which enzyme begins starch digestion in the mouth?", "salivary amylase", "pepsin", "lipase", "lactase"),
           ("Which enzyme begins protein digestion in the stomach?", "pepsin", "trypsin", "amylase", "enteropeptidase"),
           ("Which organ supplies most of the lipase that digests triglycerides?", "pancreas", "liver", "stomach", "gallbladder"),
           ("Where is lactase found?", "the brush border of the small intestine", "pancreatic juice", "saliva", "gastric juice"),
           ("What do bile salts do to dietary fat?", "emulsify it into small droplets", "hydrolyse it to fatty acids", "absorb it", "convert it to glucose")],
         "Bile is a detergent, not an enzyme"),
       F("hp-gastric-cells", DG, [
           ("Which gastric cell secretes hydrochloric acid and intrinsic factor?", "parietal cell", "chief cell", "G cell", "mucous neck cell"),
           ("Which gastric cell secretes pepsinogen?", "chief cell", "parietal cell", "G cell", "enteroendocrine D cell"),
           ("Which hormone from G cells stimulates acid secretion?", "gastrin", "secretin", "cholecystokinin", "somatostatin"),
           ("Intrinsic factor is needed to absorb which vitamin?", "vitamin B12", "vitamin C", "vitamin K", "folate")],
         "Parietal cells make acid, chief cells make the enzyme precursor")]),
     ("C", H("N"), "Describe absorption and the roles of the liver, gallbladder and pancreas.",
      "Villi and microvilli give the small intestine its area; sugars and amino acids enter capillaries to the hepatic portal vein, fats enter lacteals as chylomicrons. Secretin calls for pancreatic bicarbonate; cholecystokinin calls for enzymes and gallbladder contraction.", "P2", [
       F("hp-absorption", DG, [
           ("Where does most nutrient absorption take place?", "small intestine", "stomach", "large intestine", "oesophagus"),
           ("Absorbed glucose and amino acids travel first to which organ?", "liver, through the hepatic portal vein", "heart, through the thoracic duct", "kidney", "spleen"),
           ("What does the large intestine mainly absorb?", "water and electrolytes", "proteins", "triglycerides", "starch"),
           ("In what form do most absorbed fats leave the intestinal cell?", "chylomicrons entering lacteals", "free fatty acids entering capillaries", "bile salts", "glycogen")],
         "Water-soluble products go to the liver by the portal vein; fat goes by lymph"),
       F("hp-gi-hormones", DG, [
           ("Which hormone makes the gallbladder contract?", "cholecystokinin", "secretin", "gastrin", "insulin"),
           ("Which hormone calls for bicarbonate-rich pancreatic juice when acid enters the duodenum?", "secretin", "gastrin", "cholecystokinin", "ghrelin"),
           ("Which organ makes bile?", "liver", "gallbladder", "pancreas", "duodenum"),
           ("What is the function of pancreatic bicarbonate?", "neutralise stomach acid in the duodenum", "digest protein", "emulsify fat", "activate pepsin")],
         "Secretin answers acid, cholecystokinin answers fat and protein")])]),
   2: ("Nutrients and energy", [
     ("A", H("O"), "Count the energy in a meal and say which hormone governs each metabolic state.",
      "Carbohydrate and protein give about 4 kcal per gram, fat about 9. In the absorptive state insulin stores glucose as glycogen and fat; in the postabsorptive state glucagon releases glucose from glycogen and by gluconeogenesis, and fat is mobilised.", "P1", [
       N("hp-meal-energy", DG, "A meal has {{ka}} g of carbohydrate, {{kb}} g of protein and {{kf}} g of fat. Using 4, 4 and 9 kcal per gram, find its energy in kcal.", "4*ka + 4*kb + 9*kf",
         f"solve(Eq(({M} - 9*kf)/4, ka + kb), {M})[0]", "Fat carries more than twice the energy per gram of carbohydrate or protein", tex="E", final=True,
         cases=C("ka kb kf", [(60, 25, 20), (45, 30, 15), (80, 20, 10), (30, 40, 30), (100, 15, 5)])),
       L("hp-metabolic-state", DG, "Absorptive (fed) or postabsorptive (fasting) state? {{q}}", ["Absorptive", "Postabsorptive"], [
           ("Glycogen is being built in the liver", 0), ("Glucagon is the dominant hormone", 1), ("Fatty acids are released from adipose tissue", 1),
           ("Insulin is the dominant hormone", 0), ("The liver is making glucose from amino acids", 1), ("Triglycerides are being stored in adipose tissue", 0)],
         "Fed stores, fasting releases")])]),
 }),
 12: ("renal", "Urinary system and fluid balance", H("P", "Q"), ["GRAD", "HOME"], {
   1: ("Kidney", [
     ("A", H("P"), "Order the parts of the nephron and name its three processes.",
      "Glomerulus and capsule, proximal convoluted tubule, nephron loop, distal convoluted tubule, collecting duct. Filtration moves plasma into the capsule, reabsorption returns most of it to blood (about two-thirds in the proximal tubule), secretion adds to the tubule.", "P2", [
       F("hp-nephron-order", RN, [
           ("Which segment follows the proximal convoluted tubule?", "nephron loop", "distal convoluted tubule", "collecting duct", "glomerular capsule"),
           ("Where does filtration take place?", "the glomerulus", "the proximal tubule", "the nephron loop", "the collecting duct"),
           ("Which vessel carries blood into the glomerulus?", "afferent arteriole", "efferent arteriole", "peritubular capillary", "renal vein"),
           ("Where is most filtered water and sodium reabsorbed?", "proximal convoluted tubule", "distal convoluted tubule", "collecting duct", "nephron loop's thin limb only")],
         "Capsule, proximal tubule, loop, distal tubule, collecting duct"),
       L("hp-renal-process", RN, "Filtration, reabsorption or secretion? {{q}}", ["Filtration", "Reabsorption", "Secretion"], [
           ("Glucose moving from the proximal tubule back into blood", 1), ("Plasma water entering the glomerular capsule", 0),
           ("Hydrogen ions moved from peritubular blood into the tubule", 2), ("Water leaving the collecting duct under ADH", 1),
           ("Potassium added to the distal tubule under aldosterone", 2)],
         "Name the direction: blood to capsule, tubule to blood, or blood to tubule")]),
     ("B", H("P"), "Find the glomerular net filtration pressure and a renal clearance.",
      "Net filtration pressure = glomerular hydrostatic − capsular hydrostatic − glomerular colloid osmotic pressure. Clearance of a substance = urine concentration × urine flow ÷ plasma concentration; for inulin or creatinine it estimates GFR.", "P1", [
       N("hp-glomerular-nfp", RN, "Glomerular capillary hydrostatic pressure is {{ka}} mmHg, capsular hydrostatic pressure {{kb}} mmHg and glomerular colloid osmotic pressure {{kp}} mmHg. Find the net filtration pressure in mmHg.", "ka - kb - kp",
         f"solve(Eq(ka - {M}, kb + kp), {M})[0]", "One pressure pushes out, two oppose it; about 10 mmHg is normal", tex="NFP",
         cases=C("ka kb kp", [(55, 15, 30), (60, 18, 32), (50, 15, 30), (55, 25, 28), (45, 15, 26)])),
       N("hp-clearance", RN, "A substance has a urine concentration of {{ku}} mg/mL and a plasma concentration of {{kp}} mg/mL while urine flows at {{kv}} mL/min. Find its clearance in mL/min.", "ku*kv/kp",
         f"solve(Eq({M}*kp, ku*kv), {M})[0]", "C = UV/P: the volume of plasma that would have to be emptied of the substance each minute", tex="C",
         cases=C("ku kp kv", [(30, 0.25, 1), (1.2, 0.01, 1), (12, 0.2, 2), (0.9, 0.012, 1.5), (60, 0.1, 1)]))]),
     ("C", H("P"), "Compute filtered load and filtration fraction, and place the actions of ADH and aldosterone.",
      "Filtered load = GFR × plasma concentration; filtration fraction = GFR ÷ renal plasma flow, about 20%. ADH inserts aquaporins in the collecting duct to retain water; aldosterone raises sodium reabsorption and potassium secretion in the distal nephron.", "P1", [
       N("hp-filtered-load", RN, "GFR is {{kg}} mL/min and plasma glucose is {{kp}} mg/mL. Find the filtered load of glucose in mg/min.", "kg*kp", f"solve(Eq({M}/kp, kg), {M})[0]",
         "Filtered load is what enters the tubule each minute; when it exceeds the transport maximum (about 375 mg/min for glucose) the excess is excreted", tex="load",
         cases=C("kg kp", [(125, 1), (125, 0.9), (100, 2), (120, 4), (125, 3)])),
       N("hp-filtration-fraction", RN, "GFR is {{kg}} mL/min and renal plasma flow is {{kr}} mL/min. Find the filtration fraction in percent.", "100*kg/kr", f"solve(Eq({M}*kr/100, kg), {M})[0]",
         "About a fifth of the plasma entering the glomerulus is filtered", tex="FF",
         cases=C("kg kr", [(125, 625), (120, 600), (100, 650), (90, 600), (130, 520)]))])]),
   2: ("Fluids and acid-base", [
     ("A", H("Q"), "Divide body water into compartments and estimate plasma osmolarity.",
      "Total body water is about 60% of body mass; two-thirds is intracellular and one-third extracellular, and about a quarter of the extracellular fluid is plasma. Plasma osmolarity ≈ 2 × sodium + glucose/18 + urea nitrogen/2.8 (mEq/L, mg/dL, mg/dL).", "P1", [
       N("hp-icf-volume", RN, "A {{kw}} kg adult has total body water equal to 60% of body mass. Find the intracellular fluid volume in litres, taking 1 kg of water as 1 L.", "kw*0.6*2/3",
         "kw*Rational(3, 5) - kw*Rational(3, 5)/3", "60% is water, two-thirds of that is inside cells: the 60-40-20 rule", tex="ICF",
         cases=C("kw", [(70,), (60,), (80,), (50,), (90,)])),
       N("hp-plasma-osmolarity", RN, "Plasma sodium is {{kn}} mEq/L, glucose {{kg}} mg/dL and urea nitrogen {{kb}} mg/dL. Estimate the plasma osmolarity in mOsm/L.", "2*kn + kg/18 + kb/2.8",
         "2*kn + kg/Rational(18) + kb/Rational(14, 5)", "Sodium and its anions dominate; glucose and urea add a few units each unless they are very high", tex="osm", tol=0.01,
         cases=C("kn kg kb", [(140, 90, 14), (130, 180, 28), (145, 360, 14), (150, 90, 56), (135, 720, 28)]))]),
     ("B", H("Q"), "Compute blood pH from the bicarbonate buffer and the anion gap.",
      "pH = 6.1 + log10(bicarbonate ÷ (0.03 × carbon dioxide partial pressure)); the lungs set carbon dioxide and the kidneys set bicarbonate. Anion gap = sodium − chloride − bicarbonate, normally about 8 to 12 mEq/L.", "P1", [
       N("hp-henderson-hasselbalch", RN, "Arterial bicarbonate is {{kb}} mEq/L and carbon dioxide partial pressure is {{kp}} mmHg. Find the pH from pH = 6.1 + log10(HCO3 / (0.03 × PCO2)).", "6.1 + log10(kb/(0.03*kp))",
         "Rational(61, 10) + (log(kb) - log(Rational(3, 100)*kp))/log(10)", "A 20 to 1 ratio of bicarbonate to dissolved carbon dioxide gives pH 7.4", tex="pH", tol=0.002,
         cases=C("kb kp", [(24, 40), (12, 25), (24, 60), (36, 48), (24, 20), (15, 40)])),
       N("hp-anion-gap", RN, "Sodium is {{kn}} mEq/L, chloride {{kl}} mEq/L and bicarbonate {{kb}} mEq/L. Find the anion gap in mEq/L.", "kn - kl - kb", f"solve(Eq({M} + kl + kb, kn), {M})[0]",
         "The gap is the unmeasured anions; it widens when an acid other than hydrochloric adds its anion", tex="AG", final=True,
         cases=C("kn kl kb", [(140, 104, 24), (138, 100, 12), (142, 112, 18), (135, 95, 10), (140, 100, 28)]))])]),
 }),
 13: ("repro", "Reproduction and development", H("R", "T"), ["HOME", "FORM"], {
   1: ("Reproduction", [
     ("A", H("R"), "Follow gametogenesis and the path of sperm.",
      "Spermatogenesis in the seminiferous tubules yields four sperm per primary spermatocyte, supported by sustentacular cells; interstitial cells make testosterone under LH. Oogenesis yields one ovum and polar bodies and pauses in prophase I until puberty and in metaphase II until fertilisation.", "P2", [
       F("hp-gametogenesis", RP, [
           ("How many functional gametes come from one primary oocyte?", "one", "two", "four", "eight"),
           ("How many sperm come from one primary spermatocyte?", "four", "one", "two", "eight"),
           ("At which stage is a secondary oocyte arrested when it is ovulated?", "metaphase II", "prophase I", "anaphase I", "it has finished meiosis"),
           ("Which cells secrete testosterone?", "interstitial (Leydig) cells", "sustentacular (Sertoli) cells", "spermatogonia", "cells of the prostate")],
         "Unequal division keeps one large egg; equal division gives four small sperm"),
       F("hp-sperm-path", RP, [
           ("Where are sperm produced?", "seminiferous tubules", "epididymis", "seminal glands", "prostate"),
           ("Where do sperm mature and gain motility?", "epididymis", "ductus deferens", "urethra", "seminiferous tubules"),
           ("Which gland contributes the largest share of semen volume?", "seminal glands (vesicles)", "prostate", "bulbourethral glands", "testes"),
           ("Which pituitary hormone stimulates sustentacular cells to support spermatogenesis?", "FSH", "LH", "prolactin", "oxytocin")],
         "Tubules, epididymis, ductus deferens, ejaculatory duct, urethra")]),
     ("B", H("R"), "Time the events and hormones of the ovarian and uterine cycles.",
      "FSH grows follicles, which secrete oestrogen (proliferative phase). An LH surge near day 14 triggers ovulation. The corpus luteum secretes progesterone (secretory phase); without pregnancy it regresses, hormones fall and menstruation begins. hCG from an embryo rescues the corpus luteum.", "P2", [
       F("hp-ovarian-cycle", RP, [
           ("Which hormone surge triggers ovulation?", "LH", "FSH", "progesterone", "hCG"),
           ("Which structure secretes most of the progesterone after ovulation?", "corpus luteum", "dominant follicle", "endometrium", "anterior pituitary"),
           ("Which hormone dominates the proliferative phase of the uterine cycle?", "oestrogen", "progesterone", "LH", "prolactin"),
           ("What causes menstruation to begin?", "the fall in progesterone and oestrogen as the corpus luteum regresses", "the LH surge", "rising FSH", "rising hCG")],
         "Follicle and oestrogen before ovulation, corpus luteum and progesterone after"),
       F("hp-pregnancy-hormones", RP, [
           ("Which hormone, made by the early embryo, maintains the corpus luteum?", "hCG", "LH", "FSH", "oxytocin"),
           ("Which hormone causes milk ejection during nursing?", "oxytocin", "prolactin", "oestrogen", "progesterone"),
           ("Which hormone stimulates milk production?", "prolactin", "oxytocin", "hCG", "relaxin"),
           ("Where does fertilisation usually occur?", "the ampulla of the uterine tube", "the uterine cavity", "the ovary", "the cervix")],
         "hCG is the signal a pregnancy test reads")]),
     ("C", H("T"), "Order early development and assign tissues to germ layers.",
      "Zygote, cleavage, morula, blastocyst (implants about a week after fertilisation), then gastrulation forms ectoderm (nervous system, epidermis), mesoderm (muscle, bone, blood, heart, kidney) and endoderm (lining of gut and airways, liver, pancreas).", "P2", [
       L("hp-germ-layers", RP, "From which germ layer does this arise? {{q}}", ["Ectoderm", "Mesoderm", "Endoderm"], [
           ("Brain and spinal cord", 0), ("Skeletal muscle", 1), ("Lining of the small intestine", 2), ("Epidermis", 0), ("Heart", 1),
           ("Liver", 2), ("Bone", 1), ("Lining of the lungs", 2), ("Kidney", 1)],
         "Outside and nerves from ectoderm, lining tubes from endoderm, everything between from mesoderm"),
       F("hp-early-development", RP, [
           ("Which stage implants in the uterine wall?", "blastocyst", "zygote", "morula", "gastrula"),
           ("What process forms the three germ layers?", "gastrulation", "cleavage", "implantation", "neurulation"),
           ("Which part of the blastocyst becomes the embryo itself?", "inner cell mass", "trophoblast", "blastocoel", "zona pellucida"),
           ("Which fetal shunt carries blood from the pulmonary trunk to the aorta?", "ductus arteriosus", "foramen ovale", "ductus venosus", "umbilical vein")],
         "Cleavage, morula, blastocyst, implantation, gastrulation")])]),
 }),
})
ADD = [(f"{FW['code']}-{n}.{tn}.{lo[0]}", qq) for n, u in UNITS.items() for tn, (tt, los) in u[4].items() for lo in los for qq in lo[5]]
