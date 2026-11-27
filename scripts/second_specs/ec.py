"""Microeconomics (EC, Nov 2026): principles of microeconomics. Structure in UNITS (written by scripts/fw_setup.py),
two question types per objective.

Basis: the AP Microeconomics Course and Exam Description (effective fall 2022). The unit and topic list was read
(topic 6.5's title did not come through and is taken as "Inequality"); learning-objective codes were read for units 1
and 2 only, and the essential-knowledge statements not at all, so read: part and items are the topics. Linear models
are solved on the card by the usual shortcut and verified by solving the equilibrium or first-order condition, or by
integrating under the curve."""
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "ec-microeconomics", "microeconomics", "P1"
M = "Symbol('m')"
FW = dict(id="microeconomics", title="Microeconomics", code="EC", domain="econ", track="business", requires=["math-hs"], level=2,
          primary="ap-microeconomics", also=[], subject="Business and Economics",
          note="Anchored on the AP Microeconomics Course and Exam Description (2022), read through its unit and topic list. Introductory level with linear curves. Indifference curves, isoquants, Cournot and Bertrand models and general equilibrium belong to an intermediate course and are not built; macroeconomics has no framework yet.",
          header=["How households and firms choose, and what markets do with those choices: opportunity cost, supply and",
                  "demand, costs and market structure, factor markets and market failure. Every model here is linear, so",
                  "each answer is a line crossing, a triangle or a marginal comparison."],
          source=dict(id="ap-micro-outline", title="Principles of microeconomics by AP unit (course outline)", short="Micro outline", field="economics",
                      note=["The AP Microeconomics units written as a source so the econ.* skills have a home.", "NOT a book: only the topic list was read. Chapter numbers are ours."]))
_T = [("1.1", "Scarcity"), ("1.2", "Resource allocation and economic systems"), ("1.3", "Production possibilities curve"), ("1.4", "Comparative advantage and trade"),
      ("1.5", "Cost-benefit analysis"), ("1.6", "Marginal analysis and consumer choice"),
      ("2.1", "Demand"), ("2.2", "Supply"), ("2.3", "Price elasticity of demand"), ("2.4", "Price elasticity of supply"), ("2.5", "Other elasticities"),
      ("2.6", "Market equilibrium and consumer and producer surplus"), ("2.7", "Market disequilibrium and changes in equilibrium"),
      ("2.8", "Effects of government intervention in markets"), ("2.9", "International trade and public policy"),
      ("3.1", "The production function"), ("3.2", "Short-run production costs"), ("3.3", "Long-run production costs"), ("3.4", "Types of profit"), ("3.5", "Profit maximisation"),
      ("3.6", "Short-run decisions to produce and long-run decisions to enter or exit"), ("3.7", "Perfect competition"),
      ("4.1", "Introduction to imperfectly competitive markets"), ("4.2", "Monopoly"), ("4.3", "Price discrimination"), ("4.4", "Monopolistic competition"), ("4.5", "Oligopoly and game theory"),
      ("5.1", "Introduction to factor markets"), ("5.2", "Changes in factor demand and factor supply"), ("5.3", "Profit-maximising behaviour in perfectly competitive factor markets"), ("5.4", "Monopsonistic markets"),
      ("6.1", "Socially efficient and inefficient market outcomes"), ("6.2", "Externalities"), ("6.3", "Public and private goods"),
      ("6.4", "Effects of government intervention in different market structures"), ("6.5", "Inequality")]
STDS = [{"id": "ap-microeconomics", "name": "AP Microeconomics Course and Exam Description (effective fall 2022)", "publisher": "College Board", "kind": "standard", "read": "part",
         "url": "https://apcentral.collegeboard.org/media/pdf/ap-microeconomics-course-and-exam-description.pdf",
         "note": "Read Nov 2026 through an extraction of the first part of the PDF: the six units with their exam weights and the topic list. Learning-objective codes came through for units 1 and 2 only and the essential knowledge not at all, so read: part. Topic 6.5's title was cut off in the extraction and is entered as Inequality from general knowledge of the course; check it. Items are the topics, titled in our words.",
         "items": [{"code": c, "title": t} for c, t in _T]}]
SKILLS = [("basics", "Scarcity, opportunity cost, the production possibilities curve, comparative advantage and marginal analysis", "Basic concepts", []),
          ("markets", "Demand, supply, equilibrium, elasticity, surplus, price controls, taxes and trade", "Supply and demand", ["econ.basics"]),
          ("firm", "Production, short- and long-run costs, profit and the perfectly competitive firm", "Costs and perfect competition", ["econ.markets"]),
          ("imperfect", "Monopoly, price discrimination, monopolistic competition and oligopoly", "Imperfect competition", ["econ.firm"]),
          ("factors", "Derived demand, marginal revenue product, hiring rules and monopsony", "Factor markets", ["econ.firm"]),
          ("failure", "Externalities, public goods, regulation and inequality", "Market failure", ["econ.imperfect"])]
IDEAS = [("MARGIN", "Decisions are made at the margin", "The best quantity is where the benefit of one more equals its cost: MB = MC for a consumer, MR = MC for a firm, MRP = MFC for an employer, MSB = MSC for society."),
         ("OPP", "Every choice has an opportunity cost", "The cost of anything is the next best thing given up, which is why trade pays even for the party who is better at everything."),
         ("SURPLUS", "Markets are judged by surplus", "Competitive equilibrium maximises consumer plus producer surplus; taxes, controls, market power and externalities are measured by the triangle of surplus they destroy.")]
PRACTICES = [("P1", "Compute", "Solve a linear model for a price, a quantity, an area or a marginal value."),
             ("P2", "Predict", "Say which way a curve shifts or an outcome moves, or classify a case.")]
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
BA, MK, FI, IP, FA, FL = ["econ." + s[0] for s in SKILLS]
A = lambda *s: [f"ap-microeconomics:{x}" for x in s]


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
 1: ("basics", "Basic economic concepts", A("1.1", "1.2", "1.3", "1.4", "1.5", "1.6"), ["OPP", "MARGIN"], {
   1: ("Scarcity and choice", [
     ("A", A("1.1", "1.5"), "Identify scarcity and compute an opportunity cost.",
      "Resources are limited and wants are not, so every choice gives something up. Opportunity cost is the value of the next best alternative, including implicit costs such as forgone wages.", "P1", [
       N("ec-opportunity-cost", BA, "A year of college costs {{kt}} dollars in tuition and books. The student gives up a job paying {{kw}} dollars a year. Room and board would cost {{kr}} dollars either way. Find the opportunity cost of the year of college.", "kt + kw",
         f"solve(Eq({M} + kr - kw, kt + kr), {M})[0]", "Count what is paid and what is given up; leave out costs that would be incurred anyway", tex="cost", final=True,
         cases=C("kt kw kr", [(15000, 30000, 12000), (40000, 35000, 14000), (9000, 28000, 10000), (22000, 42000, 15000)])),
       F("ec-scarcity", BA, [
           ("What is the basic economic problem?", "limited resources against unlimited wants", "too little money in circulation", "unequal incomes", "government regulation"),
           ("Which is a factor of production?", "capital", "money in a bank account", "a share of stock", "profit"),
           ("In economics, what does 'capital' mean?", "tools, machines and buildings used to produce", "money available to spend", "a firm's stock price", "natural resources"),
           ("How are goods mainly allocated in a market economy?", "by prices set through supply and demand", "by central planners", "by tradition", "by lottery")],
         "Scarcity forces choice, and choice has a cost")]),
     ("B", A("1.3"), "Read a production possibilities curve.",
      "Points on the curve are efficient, points inside are inefficient (unemployed or misallocated resources), points outside are unattainable now. A bowed-out curve shows increasing opportunity cost; growth shifts the curve outward.", "P1", [
       L("ec-ppc-point", BA, "On a production possibilities diagram, {{q}}", ["a point on the curve", "a point inside the curve", "the curve shifts outward", "the curve shifts inward"], [
           ("a recession leaves workers unemployed. This is shown as", 1), ("all resources are fully and efficiently used. This is shown as", 0), ("a new technology raises productivity in both goods:", 2),
           ("a natural disaster destroys factories:", 3), ("the labour force grows through immigration:", 2)],
         "Use of existing resources moves the point; a change in resources or technology moves the curve"),
       N("ec-ppc-opportunity-cost", BA, "With all its resources a country can make {{ka}} cars or {{kb}} tonnes of wheat, and its production possibilities curve is a straight line. Find the opportunity cost of one car in tonnes of wheat.", "kb/ka",
         f"solve(Eq({M}*ka, kb), {M})[0]", "On a straight-line curve the trade-off is constant: what you give up over what you gain", tex="cost",
         cases=C("ka kb", [(100, 400), (50, 20), (200, 300), (80, 40), (30, 120)]))]),
     ("C", A("1.4"), "Find comparative advantage and acceptable terms of trade.",
      "A producer has the comparative advantage in the good it makes at the lower opportunity cost. Both sides gain when each specialises that way and they trade at a price between their two opportunity costs.", "P2", [
       F("ec-comparative-advantage", BA, [
           ("In a day Ana makes 10 shirts or 5 hats; Ben makes 6 shirts or 2 hats. Who has the comparative advantage in hats?", "Ana (a hat costs her 2 shirts; it costs Ben 3)", "Ben (a hat costs him 3 shirts)", "neither", "both"),
           ("In a day Ana makes 10 shirts or 5 hats; Ben makes 6 shirts or 2 hats. Who has the comparative advantage in shirts?", "Ben (a shirt costs him 1/3 hat; it costs Ana 1/2)", "Ana (she makes more shirts)", "neither", "both"),
           ("Country X makes 8 cars or 4 planes; country Y makes 6 cars or 1 plane. Which should specialise in cars?", "Y (a car costs it 1/6 plane; it costs X 1/2)", "X (it makes more cars)", "neither", "both equally"),
           ("Can one party have the comparative advantage in both goods?", "no: a lower opportunity cost in one good means a higher one in the other", "yes, if it is more productive in both", "yes, if it is larger", "only with tariffs")],
         "Absolute advantage is about who makes more; comparative advantage is about who gives up less"),
       F("ec-terms-of-trade", BA, [
           ("A hat costs Ana 2 shirts and costs Ben 3 shirts. Which price for one hat benefits both?", "2.5 shirts", "1.5 shirts", "3.5 shirts", "4 shirts"),
           ("A car costs X half a plane and costs Y one sixth of a plane. Which price for one car benefits both?", "one third of a plane", "one tenth of a plane", "three quarters of a plane", "one plane"),
           ("Where must mutually beneficial terms of trade lie?", "between the two parties' opportunity costs", "below both opportunity costs", "above both opportunity costs", "at the richer party's cost"),
           ("What do specialisation and trade allow a country to do?", "consume beyond its own production possibilities curve", "produce beyond its production possibilities curve without new resources", "eliminate scarcity", "avoid all opportunity costs")],
         "A price between the two opportunity costs leaves each side better off than making the good itself")]),
     ("D", A("1.6"), "Choose a quantity by marginal analysis and apply the utility-maximising rule.",
      "Do more of an activity while marginal benefit exceeds marginal cost; stop where they are equal. A consumer maximises utility by equalising marginal utility per dollar across goods, within the budget.", "P1", [
       N("ec-mb-equals-mc", BA, "The marginal benefit of the q-th unit is {{ka}} − {{kb}}q dollars and each unit costs {{kc}} dollars. What quantity maximises net benefit?", "(ka - kc)/kb",
         f"solve(diff(ka*{M} - kb*{M}**2/2 - kc*{M}, {M}), {M})[0]", "Keep going until the marginal benefit has fallen to the marginal cost", tex="q",
         cases=C("ka kb kc", [(50, 2, 10), (100, 5, 40), (24, 3, 6), (80, 4, 20)])),
       N("ec-mu-per-dollar", BA, "At her current purchases the marginal utility of a taco is {{ka}} and tacos cost {{kp}} dollars. Drinks cost {{kq}} dollars. What marginal utility of a drink would put her at the utility-maximising combination?", "ka/kp*kq",
         f"solve(Eq({M}/kq, ka/kp), {M})[0]", "Marginal utility per dollar must be equal across goods", tex="MU",
         cases=C("ka kp kq", [(30, 3, 2), (24, 4, 1.5), (18, 2, 5), (40, 5, 3)]))])]),
 }),
 2: ("markets", "Supply and demand", A("2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8", "2.9"), ["SURPLUS", "MARGIN"], {
   1: ("Markets", [
     ("A", A("2.1", "2.2"), "Tell a shift of a curve from a movement along it.",
      "A change in the good's own price moves along the curve (a change in quantity demanded or supplied). Demand shifts with income, tastes, prices of related goods, expectations and the number of buyers; supply shifts with input prices, technology, taxes and subsidies, expectations and the number of sellers.", "P2", [
       L("ec-shift-or-move", MK, "In the market for coffee, what happens? {{q}}", ["Demand shifts right", "Demand shifts left", "Supply shifts right", "Supply shifts left", "Movement along the curves only"], [
           ("The price of tea, a substitute, rises", 0), ("A frost destroys part of the coffee crop", 3), ("A new harvesting machine cuts costs", 2), ("A study says coffee is unhealthy", 1),
           ("The price of coffee falls because of a sale", 4), ("Consumer incomes rise and coffee is a normal good", 0), ("The wage of coffee pickers rises", 3)],
         "Ask whether buyers or sellers are affected, and whether it is the good's own price that changed"),
       F("ec-demand-supply-laws", MK, [
           ("What does the law of demand say?", "quantity demanded falls as price rises, other things equal", "demand rises as income rises", "price rises as demand rises", "quantity supplied rises with price"),
           ("The price of cream, a complement to coffee, rises. What happens to the demand for coffee?", "it decreases", "it increases", "it does not change", "quantity demanded rises along the curve"),
           ("Income rises and demand for instant noodles falls. What kind of good are they?", "inferior", "normal", "luxury", "complementary"),
           ("Sellers expect the price to be higher next month. What happens to supply today?", "it decreases", "it increases", "it does not change", "demand decreases")],
         "Other things equal is doing the work in both laws")]),
     ("B", A("2.6"), "Solve for a linear market equilibrium.",
      "Equilibrium is where quantity demanded equals quantity supplied. With Qd = a − bP and Qs = c + dP, set them equal and solve for P, then substitute for Q.", "P1", [
       N("ec-equilibrium-price", MK, "Demand is Qd = {{ka}} − {{kb}}P and supply is Qs = {{kc}} + {{kd}}P. Find the equilibrium price.", "(ka - kc)/(kb + kd)",
         f"solve(Eq(ka - kb*{M}, kc + kd*{M}), {M})[0]", "Set quantity demanded equal to quantity supplied", tex="P",
         cases=C("ka kb kc kd", [(100, 2, 10, 4), (60, 3, 0, 2), (200, 5, 20, 10), (90, 1, 30, 2), (150, 4, 30, 2)])),
       N("ec-equilibrium-quantity", MK, "Demand is Qd = {{ka}} − {{kb}}P and supply is Qs = {{kc}} + {{kd}}P. Find the equilibrium quantity.", "ka - kb*(ka - kc)/(kb + kd)",
         f"solve(Eq((ka - {M})/kb, ({M} - kc)/kd), {M})[0]", "Find the price first, then put it into either equation", tex="Q",
         cases=C("ka kb kc kd", [(100, 2, 10, 4), (60, 3, 0, 2), (200, 5, 20, 10), (90, 1, 30, 2), (150, 4, 30, 2)]))]),
     ("C", A("2.7"), "Predict how equilibrium price and quantity change when a curve shifts.",
      "Demand up: price and quantity both rise. Supply up: price falls, quantity rises. When both curves shift, one of price or quantity is determined and the other is ambiguous.", "P2", [
       L("ec-equilibrium-change", MK, "What happens to equilibrium price and quantity? {{q}}", ["Price up, quantity up", "Price down, quantity down", "Price up, quantity down", "Price down, quantity up"], [
           ("Demand increases", 0), ("Demand decreases", 1), ("Supply decreases", 2), ("Supply increases", 3), ("Incomes fall, for a normal good", 1), ("An input becomes cheaper", 3)],
         "Draw it: demand shifts move price and quantity together, supply shifts move them apart"),
       L("ec-double-shift", MK, "Both curves shift. What can be said? {{q}}", ["Quantity rises; price is ambiguous", "Quantity falls; price is ambiguous", "Price rises; quantity is ambiguous", "Price falls; quantity is ambiguous"], [
           ("Demand increases and supply increases", 0), ("Demand decreases and supply decreases", 1), ("Demand increases and supply decreases", 2), ("Demand decreases and supply increases", 3)],
         "The two shifts agree on one variable and pull against each other on the other")]),
     ("D", A("2.3", "2.4"), "Compute price elasticity by the midpoint method and link it to revenue.",
      "Elasticity = percentage change in quantity ÷ percentage change in price, with each percentage taken on the midpoint. Above 1 in size is elastic, below 1 inelastic. When demand is elastic a price cut raises total revenue; when inelastic it lowers it.", "P1", [
       N("ec-midpoint-elasticity", MK, "When price rises from {{kp}} to {{kq}} dollars, quantity demanded falls from {{ka}} to {{kb}} units. Find the price elasticity of demand by the midpoint method, as a positive number.", "((ka - kb)/((ka + kb)/2))/((kq - kp)/((kp + kq)/2))",
         f"solve(Eq({M}*(kq - kp)*(ka + kb), (ka - kb)*(kp + kq)), {M})[0]", "Percentage changes on the average of the two points, so the answer is the same in both directions", tex="E_d",
         cases=C("kp kq ka kb", [(4, 6, 120, 80), (10, 12, 55, 45), (2, 3, 100, 90), (8, 10, 30, 10), (5, 7, 70, 50)])),
       L("ec-elasticity-revenue", MK, "What happens to total revenue? {{q}}", ["It rises", "It falls", "It is unchanged"], [
           ("Price rises and demand is inelastic", 0), ("Price rises and demand is elastic", 1), ("Price falls and demand is elastic", 0), ("Price falls and demand is inelastic", 1), ("Price changes and demand is unit elastic", 2)],
         "With elastic demand quantity moves more than price, so revenue follows quantity")]),
     ("E", A("2.5"), "Use income and cross-price elasticities to classify goods.",
      "Income elasticity is positive for normal goods and negative for inferior goods. Cross-price elasticity is positive for substitutes and negative for complements.", "P1", [
       N("ec-cross-elasticity", MK, "The price of good B rises by {{kp}}% and the quantity of good A demanded changes by {{kq}}%. Find the cross-price elasticity of demand for A with respect to B.", "kq/kp", f"solve(Eq({M}*kp, kq), {M})[0]",
         "Percentage change in A's quantity over percentage change in B's price; the sign carries the meaning", tex="E_{AB}",
         cases=C("kp kq", [(10, 5), (20, -8), (5, 4), (8, -12), (25, 10)])),
       L("ec-elasticity-sign", MK, "What does this elasticity tell you? {{q}}", ["The goods are substitutes", "The goods are complements", "The good is normal", "The good is inferior"], [
           ("Cross-price elasticity of +0.8", 0), ("Cross-price elasticity of −1.5", 1), ("Income elasticity of +1.2", 2), ("Income elasticity of −0.4", 3), ("Cross-price elasticity of +2.0", 0)],
         "Income elasticity sorts normal from inferior; cross-price elasticity sorts substitutes from complements")]),
     ("F", A("2.6"), "Measure consumer and producer surplus.",
      "Consumer surplus is the area under the demand curve above the price; producer surplus is the area above the supply curve below the price. With straight lines each is a triangle: half base times height.", "P1", [
       N("ec-consumer-surplus", MK, "Inverse demand is P = {{ka}} − {{kb}}Q and the market price is {{kp}} dollars. Find the consumer surplus.", "(ka - kp)^2/(2*kb)",
         "integrate(ka - kb*Y - kp, (Y, 0, (ka - kp)/Rational(kb)))", "A triangle: height from the price up to the demand intercept, base the quantity bought", tex="CS",
         cases=C("ka kb kp", [(100, 2, 40), (50, 1, 20), (80, 4, 20), (60, 3, 30), (120, 2, 60)])),
       N("ec-producer-surplus", MK, "Inverse supply is P = {{ka}} + {{kb}}Q and the market price is {{kp}} dollars. Find the producer surplus.", "(kp - ka)^2/(2*kb)",
         "integrate(kp - ka - kb*Y, (Y, 0, (kp - ka)/Rational(kb)))", "A triangle: height from the supply intercept up to the price, base the quantity sold", tex="PS",
         cases=C("ka kb kp", [(10, 2, 40), (5, 1, 25), (20, 4, 60), (0, 3, 30), (12, 2, 60)]))]),
     ("G", A("2.8"), "Analyse price controls and a per-unit tax.",
      "A ceiling below equilibrium causes a shortage; a floor above it causes a surplus; a control on the wrong side of equilibrium is not binding. A per-unit tax drives a wedge between the buyers' and sellers' prices, lowers quantity and creates a deadweight loss of half the tax times the fall in quantity.", "P1", [
       L("ec-price-control", MK, "Equilibrium price is 10 dollars. What results? {{q}}", ["A shortage", "A surplus", "No effect (not binding)"], [
           ("A price ceiling of 8 dollars", 0), ("A price floor of 12 dollars", 1), ("A price ceiling of 12 dollars", 2), ("A price floor of 8 dollars", 2), ("A minimum price of 15 dollars", 1), ("A maximum price of 6 dollars", 0)],
         "A ceiling binds only below equilibrium, a floor only above"),
       N("ec-tax-deadweight", MK, "Demand is Qd = {{ka}} − {{kb}}P and supply is Qs = {{kd}}P. A tax of {{kt}} dollars per unit is placed on sellers. Find the deadweight loss.", "kt^2*kb*kd/(2*(kb + kd))",
         f"(kt/Rational(2))*(kd*solve(Eq(ka - kb*{M}, kd*{M}), {M})[0] - (ka - kb*solve(Eq(ka - kb*{M}, kd*({M} - kt)), {M})[0]))", "Half the tax times the fall in quantity; the check solves the taxed equilibrium directly", tex="DWL",
         cases=C("ka kb kd kt", [(100, 2, 2, 10), (120, 3, 1, 8), (60, 1, 2, 6), (200, 4, 4, 5)]))]),
     ("H", A("2.9"), "Find imports at a world price and the effect of a tariff.",
      "If the world price is below the domestic equilibrium the country imports the gap between quantity demanded and domestic quantity supplied. A tariff raises the domestic price, shrinks imports and raises revenue equal to the tariff times the imports that remain.", "P1", [
       N("ec-imports", MK, "Domestic demand is Qd = {{ka}} − {{kb}}P and domestic supply is Qs = {{kd}}P. The world price is {{kw}} dollars. Find the quantity imported.", "ka - kb*kw - kd*kw",
         f"solve(Eq(kd*kw + {M}, ka - kb*kw), {M})[0]", "Imports fill the gap between what buyers want and what home producers supply at the world price", tex="imports",
         cases=C("ka kb kd kw", [(100, 2, 2, 10), (120, 3, 1, 20), (60, 1, 2, 10), (200, 4, 4, 15)])),
       N("ec-tariff-revenue", MK, "Domestic demand is Qd = {{ka}} − {{kb}}P and domestic supply is Qs = {{kd}}P. The world price is {{kw}} dollars and a tariff of {{kt}} dollars per unit is imposed. Find the tariff revenue.", "kt*(ka - (kb + kd)*(kw + kt))",
         f"kt*solve(Eq(kd*(kw + kt) + {M}, ka - kb*(kw + kt)), {M})[0]", "The tariff raises the home price to world price plus tariff; revenue is the tariff on the imports that remain", tex="rev",
         cases=C("ka kb kd kw kt", [(100, 2, 2, 10, 5), (120, 3, 1, 20, 5), (60, 1, 2, 10, 4), (200, 4, 4, 15, 5)]))])]),
 }),
 3: ("firm", "Production, cost and perfect competition", A("3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7"), ["MARGIN"], {
   1: ("The firm", [
     ("A", A("3.1"), "Compute marginal product and recognise diminishing returns.",
      "Marginal product is the extra output from one more unit of a variable input. With a fixed input it eventually falls (diminishing marginal returns); total product still rises while marginal product is positive.", "P1", [
       N("ec-marginal-product", FI, "Output rises from {{ka}} to {{kb}} units when the number of workers rises from {{kp}} to {{kq}}. Find the marginal product of labour over this range, per worker.", "(kb - ka)/(kq - kp)",
         f"solve(Eq(ka + {M}*(kq - kp), kb), {M})[0]", "Change in output over change in the input", tex="MP",
         cases=C("ka kb kp kq", [(40, 70, 2, 3), (100, 124, 5, 7), (0, 15, 0, 1), (200, 215, 9, 10)])),
       L("ec-returns-stage", FI, "Total output with 1, 2, 3 and 4 workers is {{q}}. With which worker do diminishing marginal returns set in?", ["The second worker", "The third worker", "The fourth worker"], [
           ("10, 18, 24, 28", 0), ("10, 25, 35, 40", 1), ("5, 15, 30, 40", 2), ("8, 20, 30, 36", 1), ("12, 20, 26, 30", 0)],
         "Take differences to get marginal products and find the first one smaller than the one before")]),
     ("B", A("3.2"), "Compute short-run cost measures.",
      "Total cost = fixed + variable. ATC = TC/Q = AFC + AVC. Marginal cost is the change in total cost per extra unit; it cuts AVC and ATC at their minimum points.", "P1", [
       N("ec-average-total-cost", FI, "A firm has fixed costs of {{kf}} dollars and variable costs of {{kv}} dollars when it makes {{kn}} units. Find its average total cost.", "(kf + kv)/kn",
         f"solve(Eq({M}*kn - kv, kf), {M})[0]", "Average fixed cost plus average variable cost", tex="ATC",
         cases=C("kf kv kn", [(1000, 3000, 200), (500, 700, 100), (2400, 3600, 300), (800, 1200, 50)])),
       N("ec-marginal-cost", FI, "Total cost is {{ka}} dollars at {{kp}} units and {{kb}} dollars at {{kq}} units. Find the marginal cost per unit over this range.", "(kb - ka)/(kq - kp)",
         f"solve(Eq(ka + {M}*(kq - kp), kb), {M})[0]", "Fixed cost does not change, so marginal cost is the change in variable cost too", tex="MC",
         cases=C("ka kp kb kq", [(4000, 200, 4300, 220), (1200, 100, 1245, 105), (6000, 300, 6800, 350), (2000, 50, 2030, 51)]))]),
     ("C", A("3.3", "3.4"), "Separate economic from accounting profit and read the long-run average cost curve.",
      "Economic profit subtracts implicit (opportunity) costs as well as explicit ones; zero economic profit is a normal profit. Falling long-run average cost is economies of scale, rising is diseconomies, flat is constant returns to scale.", "P1", [
       N("ec-economic-profit", FI, "A business has revenue of {{kr}} dollars and explicit costs of {{kx}} dollars. The owner gave up a salary of {{ks}} dollars and {{kn}} dollars of interest on the savings invested. Find the economic profit.", "kr - kx - ks - kn",
         f"solve(Eq({M} + ks + kn, kr - kx), {M})[0]", "Accounting profit less the implicit costs; a negative answer means the owner would do better elsewhere", tex="profit", final=True,
         cases=C("kr kx ks kn", [(300000, 180000, 70000, 10000), (150000, 90000, 65000, 5000), (500000, 350000, 90000, 20000), (220000, 150000, 50000, 8000)])),
       L("ec-scale", FI, "Economies of scale, constant returns or diseconomies of scale? {{q}}", ["Economies of scale", "Constant returns to scale", "Diseconomies of scale"], [
           ("Long-run average cost falls as output expands", 0), ("Doubling all inputs more than doubles output", 0), ("Layers of management slow decisions and raise unit cost as the firm grows", 2),
           ("Long-run average cost is flat over a range of output", 1), ("Doubling all inputs less than doubles output", 2), ("Bulk purchasing and specialised machines lower unit cost", 0)],
         "Scale is about the long run, when every input can change")]),
     ("D", A("3.5", "3.6"), "Find a competitive firm's profit and decide whether it produces, shuts down or exits.",
      "A firm maximises profit where MR = MC; for a price taker MR is the price. Profit = (P − ATC) × Q. In the short run it produces if P ≥ AVC and shuts down otherwise; in the long run it exits if P < ATC.", "P1", [
       N("ec-competitive-profit", FI, "A price-taking firm faces a price of {{kp}} dollars and, at the output where price equals marginal cost, makes {{kn}} units at an average total cost of {{ka}} dollars. Find its profit (negative for a loss).", "(kp - ka)*kn",
         f"solve(Eq({M}/kn + ka, kp), {M})[0]", "Profit per unit times units", tex="profit", final=True,
         cases=C("kp kn ka", [(20, 500, 16), (12, 1000, 14), (50, 200, 42), (8, 3000, 9)])),
       L("ec-shutdown", FI, "A competitive firm's price, average variable cost and average total cost at its best output are given. What should it do? {{q}}", ["Produce at a profit", "Produce at a loss in the short run", "Shut down in the short run"], [
           ("P = 20, AVC = 12, ATC = 16", 0), ("P = 14, AVC = 12, ATC = 16", 1), ("P = 10, AVC = 12, ATC = 16", 2), ("P = 30, AVC = 25, ATC = 34", 1), ("P = 8, AVC = 9, ATC = 11", 2), ("P = 45, AVC = 30, ATC = 40", 0)],
         "Above ATC is profit; between AVC and ATC covers some fixed cost; below AVC, stop")]),
     ("E", A("3.7"), "Describe long-run equilibrium in perfect competition.",
      "Entry and exit drive economic profit to zero: price settles at the minimum of average total cost, where P = MC = minimum ATC, which is both allocatively and productively efficient.", "P1", [
       N("ec-long-run-price", FI, "Every firm in a competitive industry has total cost TC = {{ka}} + {{kb}}q + {{kc}}q². Find the long-run equilibrium price.", "kb + 2*sqrt(ka*kc)",
         "(ka + kb*Max(*solve(diff((ka + kb*Y + kc*Y**2)/Y, Y), Y)) + kc*Max(*solve(diff((ka + kb*Y + kc*Y**2)/Y, Y), Y))**2)/Max(*solve(diff((ka + kb*Y + kc*Y**2)/Y, Y), Y))",
         "Price falls to minimum average total cost, which is where q = sqrt(a/c)", tex="P",
         cases=C("ka kb kc", [(100, 4, 1), (64, 10, 4), (200, 5, 2), (36, 2, 1), (400, 20, 1)])),
       F("ec-pc-long-run", FI, [
           ("Firms in a competitive industry are earning economic profit. What happens in the long run?", "firms enter, supply rises and price falls until profit is zero", "firms exit and price rises", "nothing changes", "each firm raises its price"),
           ("In long-run competitive equilibrium, price equals what?", "marginal cost and minimum average total cost", "average variable cost only", "average fixed cost", "marginal revenue plus a markup"),
           ("Why is a perfectly competitive firm a price taker?", "it sells an identical product and is small relative to the market", "the government sets its price", "it has no costs", "its demand curve slopes down steeply"),
           ("What does P = MC mean for society?", "allocative efficiency: the last unit is worth what it costs", "the firm earns the largest possible profit margin", "consumers get no surplus", "output is too low")],
         "Free entry is what delivers zero profit and minimum cost")])]),
 }),
 4: ("imperfect", "Imperfect competition", A("4.1", "4.2", "4.3", "4.4", "4.5"), ["MARGIN", "SURPLUS"], {
   1: ("Market power", [
     ("A", A("4.1", "4.2"), "Solve a linear monopoly and its deadweight loss.",
      "With P = a − bQ, marginal revenue is MR = a − 2bQ. The monopolist sets MR = MC, then charges the price on the demand curve at that quantity. Output is below the competitive level, and the deadweight loss is the triangle between demand and marginal cost over the lost units.", "P1", [
       N("ec-monopoly-price", IP, "A monopolist faces P = {{ka}} − {{kb}}Q and has a constant marginal cost of {{kc}} dollars. Find the profit-maximising price.", "(ka + kc)/2",
         "ka - kb*solve(diff((ka - kb*Y)*Y - kc*Y, Y), Y)[0]", "Set MR = MC for the quantity, then go up to the demand curve for the price", tex="P",
         cases=C("ka kb kc", [(100, 2, 20), (60, 1, 10), (80, 4, 16), (120, 3, 30), (50, 0.5, 10)])),
       N("ec-monopoly-dwl", IP, "A monopolist faces P = {{ka}} − {{kb}}Q with constant marginal cost {{kc}} dollars. Find the deadweight loss compared with the competitive outcome.", "(ka - kc)^2/(8*kb)",
         "integrate(ka - kb*Y - kc, (Y, solve(diff((ka - kb*Y)*Y - kc*Y, Y), Y)[0], (ka - kc)/Rational(kb)))", "The monopolist sells half the competitive quantity; the lost triangle has that base and the markup as height", tex="DWL",
         cases=C("ka kb kc", [(100, 2, 20), (60, 1, 10), (80, 4, 16), (120, 3, 30)]))]),
     ("B", A("4.3"), "Explain price discrimination and its effect on output and surplus.",
      "Price discrimination charges different prices for the same good for reasons other than cost; it needs market power, a way to sort buyers and no resale. Under perfect discrimination the firm sells the competitive quantity, takes all the consumer surplus and leaves no deadweight loss.", "P1", [
       N("ec-perfect-pd-profit", IP, "A monopolist facing P = {{ka}} − {{kb}}Q with constant marginal cost {{kc}} dollars and no fixed cost can charge each buyer exactly their willingness to pay. Find its profit.", "(ka - kc)^2/(2*kb)",
         "integrate(ka - kb*Y - kc, (Y, 0, (ka - kc)/Rational(kb)))", "It captures the whole triangle between demand and marginal cost", tex="profit",
         cases=C("ka kb kc", [(100, 2, 20), (60, 1, 10), (80, 4, 16), (120, 3, 30)])),
       F("ec-price-discrimination", IP, [
           ("Which condition is needed for price discrimination to work?", "buyers cannot resell to one another", "the product is identical across many sellers", "marginal cost is zero", "demand is perfectly elastic"),
           ("Under perfect price discrimination, how much consumer surplus is left?", "none", "all of it", "half of it", "the same as in competition"),
           ("Compared with a single-price monopoly, what does perfect price discrimination do to output?", "raises it to the competitive quantity", "lowers it", "leaves it unchanged", "reduces it to zero"),
           ("A cinema charges students less than other adults. Which group must have the more elastic demand?", "students", "other adults", "neither", "both equally")],
         "The group that responds more to price gets the lower price")]),
     ("C", A("4.4"), "Describe monopolistic competition in the short and long run.",
      "Many firms sell differentiated products with free entry. Each faces a downward-sloping demand curve and sets MR = MC; entry shifts each firm's demand left until price equals average total cost and economic profit is zero, with price above marginal cost and excess capacity.", "P2", [
       L("ec-market-structure", IP, "Which market structure? {{q}}", ["Perfect competition", "Monopolistic competition", "Oligopoly", "Monopoly"], [
           ("Many sellers of an identical product, free entry", 0), ("Many sellers of differentiated products, free entry", 1), ("A few large interdependent sellers behind entry barriers", 2),
           ("One seller of a product with no close substitutes", 3), ("Restaurants in a large city", 1), ("Wheat farming", 0), ("Commercial aircraft manufacturing", 2)],
         "Count the sellers, then ask whether the product is differentiated and whether entry is free"),
       F("ec-monopolistic-long-run", IP, [
           ("In long-run equilibrium, what economic profit does a monopolistically competitive firm earn?", "zero", "positive", "negative", "the monopoly profit"),
           ("In that long-run equilibrium, how does price compare with marginal cost?", "price is above marginal cost", "price equals marginal cost", "price is below marginal cost", "price equals average fixed cost"),
           ("What is excess capacity in monopolistic competition?", "producing less than the output that minimises average total cost", "holding unsold inventory", "having too many workers", "producing more than the efficient scale"),
           ("Firms in the industry are making losses. What happens to a surviving firm's demand curve as others exit?", "it shifts right", "it shifts left", "it becomes horizontal", "it does not move")],
         "Zero profit like competition, markup over marginal cost like monopoly")]),
     ("D", A("4.5"), "Find dominant strategies and the Nash equilibrium of a two-firm game.",
      "A dominant strategy is best whatever the rival does. A Nash equilibrium is a pair of strategies from which neither player gains by changing alone. In a prisoners' dilemma both have a dominant strategy and the equilibrium leaves both worse off than cooperation would.", "P2", [
       F("ec-nash", IP, [
           ("Payoffs (A, B): both price High (10, 10); A High, B Low (2, 14); A Low, B High (14, 2); both Low (5, 5). What is the Nash equilibrium?", "both price Low", "both price High", "A High, B Low", "A Low, B High"),
           ("Payoffs (A, B): both Advertise (6, 6); A Advertises, B does not (12, 3); A does not, B Advertises (3, 12); neither (9, 9). What is A's dominant strategy?", "Advertise", "Do not advertise", "A has none", "copy B"),
           ("Payoffs (A, B): both Enter (−2, −2); A Enters, B stays out (8, 0); A stays out, B Enters (0, 8); both stay out (0, 0). Does A have a dominant strategy?", "no: A's best choice depends on what B does", "yes: Enter", "yes: stay out", "yes: whichever B chooses"),
           ("Payoffs (A, B): both High (10, 10); A High, B Low (2, 14); A Low, B High (14, 2); both Low (5, 5). Why do the firms not both price High?", "each gains by cutting price whatever the other does", "High prices are illegal", "they do not know the payoffs", "High is each firm's dominant strategy")],
         "Check each player's best reply to each of the other's choices"),
       F("ec-oligopoly", IP, [
           ("What is the defining feature of an oligopoly?", "a few firms whose decisions affect one another", "many firms with identical products", "one firm", "free entry and zero profit"),
           ("What is a cartel?", "a group of firms that agree to restrict output and raise price", "a firm with a patent", "a government price floor", "a market with free entry"),
           ("Why do cartels tend to break down?", "each member can gain by secretly producing more than its quota", "demand becomes perfectly elastic", "members have identical costs", "price falls below marginal cost"),
           ("In a prisoners' dilemma, how does the Nash equilibrium compare with the cooperative outcome?", "both players are worse off", "both are better off", "one is better off and one worse", "it is the same")],
         "Interdependence is what makes strategy matter")])]),
 }),
 5: ("factors", "Factor markets", A("5.1", "5.2", "5.3", "5.4"), ["MARGIN"], {
   1: ("Hiring", [
     ("A", A("5.1", "5.3"), "Compute marginal revenue product and decide how many workers to hire.",
      "Demand for a factor is derived from demand for what it makes. For a price-taking firm, marginal revenue product = marginal product × output price; hire as long as MRP is at least the wage.", "P1", [
       N("ec-mrp", FA, "Hiring one more worker raises output by {{km}} units, and each unit sells for {{kp}} dollars in a competitive market. Find the worker's marginal revenue product.", "km*kp", f"solve(Eq({M}/kp, km), {M})[0]",
         "What the extra worker adds to revenue", tex="MRP", final=True,
         cases=C("km kp", [(12, 5), (8, 20), (30, 2.5), (5, 40)])),
       L("ec-hire-count", FA, "The marginal products of the first five workers are 10, 8, 6, 4 and 2 units per day. {{q}} How many workers should the firm hire?", ["1", "2", "3", "4", "5"], [
           ("Output sells for 10 dollars and the wage is 60 dollars a day.", 2), ("Output sells for 10 dollars and the wage is 80 dollars a day.", 1), ("Output sells for 10 dollars and the wage is 40 dollars a day.", 3),
           ("Output sells for 20 dollars and the wage is 40 dollars a day.", 4), ("Output sells for 5 dollars and the wage is 50 dollars a day.", 0)],
         "Hire every worker whose marginal revenue product is at least the wage")]),
     ("B", A("5.2"), "Predict shifts in factor demand and supply.",
      "Factor demand rises with the output price, with the factor's productivity, and with the price of a substitute input; factor supply shifts with population, preferences for work and alternative opportunities.", "P2", [
       L("ec-labour-shift", FA, "In the market for carpenters, what happens? {{q}}", ["Labour demand increases", "Labour demand decreases", "Labour supply increases", "Labour supply decreases"], [
           ("The price of new houses rises", 0), ("Better tools raise each carpenter's output", 0), ("A housing slump cuts the price of houses", 1), ("More people complete carpentry training", 2),
           ("Wages in other trades rise sharply", 3), ("Immigration adds skilled carpenters", 2)],
         "Demand for a factor follows the value of what it produces"),
       F("ec-derived-demand", FA, [
           ("Why is the demand for labour called a derived demand?", "it depends on the demand for the product labour makes", "it is set by the government", "it is derived from workers' preferences", "it slopes upward"),
           ("Why does the marginal revenue product curve slope down for a competitive firm?", "diminishing marginal product", "the output price falls as the firm sells more", "wages rise with employment", "fixed costs rise"),
           ("In a competitive labour market, the wage a single firm pays is determined by what?", "market supply and demand for that labour", "the firm's own choice", "the firm's fixed costs", "the firm's average product"),
           ("Equilibrium wage rises and employment rises. Which shift caused it?", "an increase in labour demand", "an increase in labour supply", "a decrease in labour demand", "a decrease in labour supply")],
         "Factor markets are supply and demand again, with the firms as buyers")]),
     ("C", A("5.3"), "Apply the least-cost rule for combining inputs.",
      "Cost is minimised when the marginal product per dollar is equal across inputs: MP of labour ÷ wage = MP of capital ÷ rental rate. If labour's ratio is higher, use more labour and less capital.", "P1", [
       N("ec-least-cost", FA, "The marginal product of labour is {{ka}} and the wage is {{kw}} dollars. Capital rents for {{kr}} dollars. At what marginal product of capital is the firm's input mix cost-minimising?", "ka/kw*kr",
         f"solve(Eq({M}/kr, ka/kw), {M})[0]", "Equal marginal product per dollar", tex="MP_K",
         cases=C("ka kw kr", [(20, 10, 40), (12, 15, 50), (30, 20, 30), (8, 16, 100)])),
       L("ec-input-switch", FA, "To lower cost at the same output, what should the firm do? {{q}}", ["Use more labour and less capital", "Use more capital and less labour", "Change nothing"], [
           ("MP of labour 20, wage 10; MP of capital 60, rent 40", 0), ("MP of labour 12, wage 12; MP of capital 50, rent 25", 1), ("MP of labour 30, wage 15; MP of capital 80, rent 40", 2),
           ("MP of labour 8, wage 16; MP of capital 20, rent 50", 0), ("MP of labour 9, wage 18; MP of capital 45, rent 60", 1)],
         "Shift spending toward the input that gives more output per dollar")]),
     ("D", A("5.4"), "Solve a monopsony and compare it with a competitive labour market.",
      "A monopsonist faces the upward-sloping market supply curve, so its marginal factor cost lies above the wage. It hires where MRP = MFC and pays the wage on the supply curve at that quantity: fewer workers at a lower wage than competition.", "P1", [
       N("ec-monopsony-employment", FA, "A monopsonist faces labour supply w = {{ka}} + {{kb}}L and has marginal revenue product MRP = {{kc}} − {{kd}}L. Find the number of workers it hires.", "(kc - ka)/(2*kb + kd)",
         f"solve(Eq(diff((ka + kb*{M})*{M}, {M}), kc - kd*{M}), {M})[0]", "Marginal factor cost is a + 2bL; set it equal to MRP", tex="L",
         cases=C("ka kb kc kd", [(10, 1, 70, 1), (4, 2, 60, 3), (20, 1, 100, 2), (5, 0.5, 45, 1)])),
       F("ec-monopsony", FA, [
           ("Compared with a competitive labour market, a monopsonist hires how many workers and pays what wage?", "fewer workers at a lower wage", "more workers at a lower wage", "fewer workers at a higher wage", "the same number at a lower wage"),
           ("Why is a monopsonist's marginal factor cost above the wage?", "to hire one more worker it must raise the wage for all workers", "it pays a hiring tax", "its workers are less productive", "it sells in a competitive market"),
           ("What is a monopsony?", "a market with a single buyer", "a market with a single seller", "a market with a few sellers", "a market with many buyers"),
           ("A minimum wage set between the monopsony wage and the competitive wage does what to employment in a monopsony?", "can raise it", "must lower it", "leaves it unchanged in every case", "reduces it to zero")],
         "Monopsony is monopoly turned around: power on the buying side")])]),
 }),
 6: ("failure", "Market failure and the role of government", A("6.1", "6.2", "6.3", "6.4", "6.5"), ["SURPLUS", "MARGIN"], {
   1: ("When markets miss", [
     ("A", A("6.1", "6.2"), "Find the socially optimal quantity and the corrective tax.",
      "The efficient quantity is where marginal social benefit equals marginal social cost. With a constant external cost per unit, marginal social cost = marginal private cost + the external cost, and a per-unit tax equal to the external cost moves the market to the efficient quantity.", "P1", [
       N("ec-social-optimum", FL, "Demand (marginal benefit) is P = {{ka}} − {{kb}}Q, private marginal cost is P = {{kc}} + {{kd}}Q, and each unit causes {{kx}} dollars of external cost. Find the socially optimal quantity.", "(ka - kc - kx)/(kb + kd)",
         f"solve(Eq(ka - kb*{M}, kc + kd*{M} + kx), {M})[0]", "Add the external cost to the supply curve and find the new crossing", tex="Q",
         cases=C("ka kb kc kd kx", [(100, 2, 10, 1, 15), (80, 1, 20, 1, 10), (60, 2, 0, 2, 12), (120, 3, 20, 2, 25)])),
       N("ec-overproduction", FL, "Demand is P = {{ka}} − {{kb}}Q, private marginal cost is P = {{kc}} + {{kd}}Q, and each unit causes {{kx}} dollars of external cost. By how many units does the unregulated market overproduce?", "kx/(kb + kd)",
         f"solve(Eq(ka - kb*{M}, kc + kd*{M}), {M})[0] - solve(Eq(ka - kb*{M}, kc + kd*{M} + kx), {M})[0]", "Market quantity ignores the external cost; the gap closes with a tax equal to that cost", tex="gap",
         cases=C("ka kb kc kd kx", [(100, 2, 10, 1, 15), (80, 1, 20, 1, 10), (60, 2, 0, 2, 12), (120, 3, 20, 2, 25)]))]),
     ("B", A("6.2"), "Classify externalities and their remedies.",
      "A negative externality (pollution) makes the market produce too much; a positive one (vaccination, education) too little. Taxes and subsidies equal to the external effect, or tradable permits, bring private incentives into line.", "P2", [
       L("ec-externality", FL, "Compared with the efficient quantity, the market produces {{q}}", ["too much", "too little", "the efficient amount"], [
           ("steel from a mill that pollutes a river:", 0), ("flu vaccinations:", 1), ("a good with no external costs or benefits in a competitive market:", 2),
           ("education that benefits others as well as the student:", 1), ("loud late-night concerts in a residential street:", 0)],
         "External cost means too much; external benefit means too little"),
       F("ec-externality-remedy", FL, [
           ("Which policy corrects a negative externality?", "a per-unit tax equal to the marginal external cost", "a per-unit subsidy to producers", "a price ceiling", "removing property rights"),
           ("Which policy corrects a positive externality?", "a per-unit subsidy equal to the marginal external benefit", "a per-unit tax", "a quota below the market quantity", "a price floor"),
           ("What does the Coase theorem say?", "with clear property rights and low bargaining costs, private parties can reach the efficient outcome", "governments must always tax polluters", "externalities cannot be corrected", "markets never fail"),
           ("With a negative externality, how does marginal social cost compare with marginal private cost?", "it is higher", "it is lower", "it is equal", "it is zero")],
         "Make the decision-maker face the full cost or receive the full benefit")]),
     ("C", A("6.3"), "Classify goods by rivalry and excludability.",
      "Private goods are rival and excludable; public goods are neither, so free riders make private provision too small; common resources are rival but not excludable and are overused; club (artificially scarce) goods are excludable but not rival.", "P2", [
       L("ec-good-type", FL, "What type of good? {{q}}", ["Private good", "Public good", "Common resource", "Club good"], [
           ("A sandwich", 0), ("National defence", 1), ("Fish in the open ocean", 2), ("A streaming video subscription", 3), ("A lighthouse beam", 1),
           ("A congested toll-free road", 2), ("A pair of shoes", 0), ("A cable television channel", 3)],
         "Two questions: does my use reduce yours, and can non-payers be kept out?"),
       F("ec-free-rider", FL, [
           ("Why do private markets underprovide public goods?", "people can benefit without paying, so few pay", "they cost nothing to produce", "they are rival", "governments forbid it"),
           ("What is the tragedy of the commons?", "overuse of a resource that is rival but not excludable", "underuse of a public good", "monopoly pricing of a club good", "a shortage caused by a price ceiling"),
           ("How is the efficient quantity of a public good found?", "where the sum of everyone's marginal benefits equals marginal cost", "where one person's marginal benefit equals marginal cost", "where price equals average cost", "by maximising tax revenue"),
           ("Which change turns a common resource into something closer to a private good?", "assigning enforceable property rights", "removing all fees", "raising demand", "banning sales")],
         "Non-excludable means a free-rider problem; rival means crowding")]),
     ("D", A("6.4"), "Predict how taxes and regulation affect a monopolist.",
      "A lump-sum tax changes neither marginal cost nor marginal revenue, so output and price stay the same and only profit falls. A per-unit tax raises marginal cost and lowers output. Regulating price at marginal cost is efficient but may cause a loss for a natural monopoly; price at average total cost gives zero economic profit.", "P2", [
       L("ec-monopoly-tax", FL, "What happens to a monopolist's output? {{q}}", ["It falls", "It rises", "It does not change"], [
           ("A lump-sum tax is imposed", 2), ("A per-unit tax is imposed", 0), ("A per-unit subsidy is given", 1), ("A lump-sum subsidy is given", 2),
           ("A price ceiling is set at the level where demand crosses marginal cost", 1)],
         "Only what changes marginal cost or marginal revenue changes the quantity"),
       F("ec-natural-monopoly", FL, [
           ("What makes an industry a natural monopoly?", "average total cost falls over the whole range of market demand", "the firm owns a patent", "the government bans entry", "demand is perfectly inelastic"),
           ("A natural monopoly is required to price at marginal cost. What is the likely problem?", "price is below average total cost, so it makes a loss", "it earns excessive profit", "output is too low", "there is a deadweight loss"),
           ("Regulators set price equal to average total cost. What economic profit does the firm earn?", "zero", "positive", "negative", "the monopoly profit"),
           ("What is the aim of antitrust policy?", "to keep markets competitive by limiting mergers and collusion", "to raise prices", "to protect monopolies", "to set wages")],
         "Marginal-cost pricing is efficient; average-cost pricing is the fair-return compromise")]),
     ("E", A("6.5"), "Measure inequality and classify taxes.",
      "The Lorenz curve plots cumulative income share against cumulative population share; the Gini coefficient is the area between it and the line of equality divided by the whole area under that line (0 is perfect equality, 1 perfect inequality). A tax is progressive if its average rate rises with income, regressive if it falls.", "P1", [
       N("ec-gini", FL, "The area between the line of equality and the Lorenz curve is {{ka}}, measured with the whole square as 1. Find the Gini coefficient.", "ka/0.5", f"solve(Eq({M}/2, ka), {M})[0]",
         "The triangle under the line of equality has area one half, so the Gini is twice the gap area", tex="G",
         cases=C("ka", [(0.2,), (0.15,), (0.3,), (0.24,), (0.125,)])),
       L("ec-tax-type", FL, "Progressive, proportional or regressive? {{q}}", ["Progressive", "Proportional", "Regressive"], [
           ("Tax of 1,000 dollars on an income of 10,000 and 20,000 on an income of 100,000", 0), ("Tax of 2,000 dollars on an income of 20,000 and 5,000 on an income of 100,000", 2),
           ("Tax of 1,500 dollars on an income of 15,000 and 9,000 on an income of 90,000", 1), ("A fixed fee of 500 dollars per person whatever the income", 2), ("A flat 15% of all income", 1)],
         "Compare average tax rates, tax over income, at the two incomes")])]),
 }),
}
ADD = [(f"{FW['code']}-{n}.{tn}.{lo[0]}", qq) for n, u in UNITS.items() for tn, (tt, los) in u[4].items() for lo in los for qq in lo[5]]
