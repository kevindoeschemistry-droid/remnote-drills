"""Managerial Accounting (MG, Nov 2026): cost and management accounting. Structure in UNITS (written by
scripts/fw_setup.py), two question types per objective.

Basis: the IMA Content Specification Outlines for the CMA examinations (effective September 2024), read through an
extraction of Part 1 sections B, C, D and Part 2 sections C, E down to their lettered lines; the Learning Outcome
Statements were not read, so read: part. Items are the numbered subtopics with our own titles. Cards compute along the
textbook formula; verify expressions solve the defining relation or sum the pieces another way."""
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "mg-managerial", "managerial-accounting", "P1"
M = "Symbol('m')"
FW = dict(id="managerial-accounting", title="Managerial Accounting", code="MG", domain="mgmt", track="business", requires=["accounting-far"], level=3,
          primary="ima-cma-cso", also=[], subject="Business and Economics",
          note="Anchored on the IMA CMA Content Specification Outlines (2024): Part 1 planning and budgeting, performance management and cost management, and Part 2 decision analysis and capital investment, read to the lettered lines of the outline. Financial reporting, internal controls, analytics, corporate finance, risk and ethics sections of the CMA are not built here.",
          header=["Accounting for the people who run the business rather than the people who invest in it: what a unit costs,",
                  "how cost moves with volume, what the budget said against what happened, and which numbers bear on a decision.",
                  "Financial reporting is in Accounting (FAR)."],
          source=dict(id="cma-outline", title="Managerial accounting by CMA outline section (course outline)", short="CMA outline", field="accounting",
                      note=["The CMA content specification sections written as a source so the mgmt.* skills have a home.", "NOT a book: only the outline was read. Chapter numbers are ours."]))
STDS = [{"id": "ima-cma-cso", "name": "CMA Content Specification Outlines (effective September 1, 2024)", "publisher": "Institute of Certified Management Accountants (IMA)", "kind": "exam-spec", "read": "part",
         "url": "https://accounting.uworld.com/wp-content/uploads/2025/05/2024-CMA-Content-Specification-Outlines-Final.pdf",
         "note": "Read Nov 2026 through an extraction of a review provider's copy of the outline: Part 1 sections B, C and D and Part 2 sections C and E, down to the lettered lines. Part 1 sections A, E, F and Part 2 sections A, B, D, F were not read, and neither were the Learning Outcome Statements, so read: part. Items are the numbered subtopics of the sections read, titled in our words. IMA says the outline is unchanged for 2026 (a provider's report, not checked with IMA).",
         "items": [{"code": c, "title": t} for c, t in [
             ("1B1", "Strategic planning"), ("1B2", "Budgeting concepts"), ("1B3", "Forecasting techniques: regression, learning curves, expected value"),
             ("1B4", "Budgeting methodologies: master, project, activity-based, zero-based, rolling, flexible"), ("1B5", "The annual profit plan and its schedules"),
             ("1B6", "Pro forma statements and cash flow projections"),
             ("1C1", "Cost and variance measures: flexible budgets and standard cost variances"), ("1C2", "Responsibility centres, transfer pricing and segment reporting"),
             ("1C3", "Performance measures: profitability, ROI, residual income, KPIs, balanced scorecard"),
             ("1D1", "Cost measurement: behaviour, actual, normal and standard costs, absorption and variable costing, joint costs"),
             ("1D2", "Costing systems: job order, activity-based, life-cycle and others"), ("1D3", "Overhead: rates, allocation bases and service departments"),
             ("1D4", "Supply chain management: lean, ERP, capacity"), ("1D5", "Business process improvement: value chain, benchmarking, cost of quality"),
             ("2C1", "Cost-volume-profit analysis"), ("2C2", "Marginal analysis: relevant costs and short-run decisions"), ("2C3", "Pricing"),
             ("2E1", "The capital budgeting process"), ("2E2", "Capital investment analysis methods")]]}]
SKILLS = [("cost-concepts", "Cost classification, cost behaviour, absorption and variable costing, joint costs", "Cost concepts", []),
          ("costing-systems", "Overhead rates, job and process costing, activity-based costing, service departments", "Costing systems", ["mgmt.cost-concepts"]),
          ("cvp", "Contribution margin, breakeven, target profit, sales mix and operating leverage", "Cost-volume-profit", ["mgmt.cost-concepts"]),
          ("budgeting", "Budget types, operating and cash budgets, learning curves and expected value", "Budgeting and forecasting", ["mgmt.cvp"]),
          ("variances", "Flexible budgets and standard cost variances", "Standard costs and variances", ["mgmt.budgeting", "mgmt.costing-systems"]),
          ("performance", "Responsibility centres, ROI, residual income, transfer pricing and the balanced scorecard", "Performance measurement", ["mgmt.variances"]),
          ("decisions", "Relevant costs, short-run decisions, pricing and capital budgeting", "Decision analysis", ["mgmt.cvp"])]
IDEAS = [("BEHAVE", "Cost behaviour comes first", "Whether a cost changes with volume decides how it enters a breakeven, a budget and a decision; the same cost can be fixed for one question and variable for another."),
         ("DIFF", "Only differences matter", "A decision turns on the costs and revenues that differ between the alternatives. Sunk costs and costs common to every choice drop out."),
         ("PLANACT", "Plan against actual", "A variance is the gap between what happened and what the plan says should have happened at the actual volume; splitting it into price and quantity says who can explain it.")]
PRACTICES = [("P1", "Compute", "Carry a costing, budgeting or decision rule to a number."),
             ("P2", "Classify", "Name the cost type, the method or the responsible party from a description.")]
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
CC, CS, CV, BU, VA, PE, DE = ["mgmt." + s[0] for s in SKILLS]
I = lambda *s: [f"ima-cma-cso:{x}" for x in s]


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
 1: ("cost-concepts", "Cost concepts", I("1D1"), ["BEHAVE"], {
   1: ("What a cost is", [
     ("A", I("1D1"), "Classify a cost as product or period, direct or indirect, fixed or variable.",
      "Product costs (direct materials, direct labour, manufacturing overhead) attach to inventory and are expensed when the goods are sold; period costs (selling and administrative) are expensed as incurred. Variable costs change in total with volume; fixed costs do not within the relevant range.", "P2", [
       L("mg-product-period", CC, "Product cost or period cost? {{q}}", ["Product cost", "Period cost"], [
           ("Wood used in furniture a factory makes", 0), ("Sales commissions", 1), ("Depreciation on factory equipment", 0), ("The chief executive's salary", 1),
           ("Factory supervisor's salary", 0), ("Advertising", 1), ("Depreciation on the delivery trucks for finished goods", 1), ("Wages of assembly-line workers", 0)],
         "If it happens inside the factory it goes into inventory; everything else is expensed in the period"),
       L("mg-fixed-variable", CC, "Within the relevant range, how does this cost behave in total as output rises? {{q}}", ["Variable", "Fixed", "Mixed"], [
           ("Direct materials", 0), ("Factory rent", 1), ("A phone plan with a flat fee plus a charge per minute", 2), ("Straight-line depreciation", 1),
           ("Sales commissions paid per unit", 0), ("A salesperson's base salary plus commission", 2)],
         "Variable in total means constant per unit; fixed in total means falling per unit")]),
     ("B", I("1D1"), "Split a mixed cost with the high-low method.",
      "Variable cost per unit = change in cost ÷ change in activity between the highest and lowest activity levels; fixed cost = total cost at either point minus the variable part.", "P1", [
       N("mg-high-low-rate", CC, "Maintenance cost was {{ka}} dollars at {{kp}} machine hours (the lowest month) and {{kb}} dollars at {{kq}} machine hours (the highest month). Find the variable cost per machine hour.", "(kb - ka)/(kq - kp)",
         f"solve(Eq(ka + {M}*(kq - kp), kb), {M})[0]", "Rise over run between the two extreme activity levels", tex="v",
         cases=C("ka kp kb kq", [(4200, 1000, 6600, 2200), (9000, 3000, 12600, 5400), (2500, 500, 4000, 1500), (15000, 4000, 21000, 8000)])),
       N("mg-high-low-fixed", CC, "Utility cost was {{ka}} dollars at {{kp}} units and {{kb}} dollars at {{kq}} units, the lowest and highest months. Find the fixed cost per month.", "ka - (kb - ka)/(kq - kp)*kp",
         f"solve(Eq(({M} - ka)/(0 - kp), (kb - ka)/(kq - kp)), {M})[0]", "Find the slope first, then back out the intercept from either point", tex="F",
         cases=C("ka kp kb kq", [(4200, 1000, 6600, 2200), (9000, 3000, 12600, 5400), (2500, 500, 4000, 1500), (15000, 4000, 21000, 8000)]))]),
     ("C", I("1D1"), "Compare income under absorption and variable costing.",
      "Absorption costing puts fixed manufacturing overhead into unit cost; variable costing expenses it in the period. When production exceeds sales, absorption income is higher by the fixed overhead per unit times the increase in inventory.", "P1", [
       N("mg-absorption-unit-cost", CC, "A unit takes {{ka}} dollars of direct materials, {{kb}} of direct labour and {{kv}} of variable overhead. Fixed manufacturing overhead is {{kf}} dollars for the {{kn}} units produced. Find the unit product cost under absorption costing.", "ka + kb + kv + kf/kn",
         f"solve(Eq(({M} - ka - kb - kv)*kn, kf), {M})[0]", "Absorption costing adds a share of fixed overhead; variable costing would stop at the first three", tex="c",
         cases=C("ka kb kv kf kn", [(10, 6, 4, 50000, 10000), (20, 12, 8, 120000, 8000), (5, 3, 2, 30000, 15000), (14, 9, 2, 60000, 12000)])),
       N("mg-absorption-variable-gap", CC, "Fixed manufacturing overhead is {{kf}} dollars per unit. The company produced {{kp}} units and sold {{ks}}. By how many dollars does absorption costing income exceed variable costing income?", "kf*(kp - ks)",
         f"solve(Eq({M}/kf + ks, kp), {M})[0]", "The gap is the fixed overhead parked in the units added to inventory", tex="gap",
         cases=C("kf kp ks", [(5, 10000, 8000), (15, 8000, 7000), (2, 15000, 12500), (8, 6000, 5200)]))]),
     ("D", I("1D1"), "Allocate a joint cost.",
      "Joint costs up to the split-off point are allocated by relative sales value at split-off, by net realisable value (final sales value minus separable costs) or by physical units. The allocation is for inventory costing; it is irrelevant to the decision to process further.", "P1", [
       N("mg-joint-sales-value", CC, "A joint process costing {{kj}} dollars yields product A with a sales value at split-off of {{ka}} dollars and product B with {{kb}} dollars. How much joint cost is allocated to A by relative sales value?", "kj*ka/(ka + kb)",
         f"solve(Eq({M}*(ka + kb), kj*ka), {M})[0]", "Each product carries joint cost in proportion to its share of total sales value", tex="A",
         cases=C("kj ka kb", [(60000, 80000, 40000), (90000, 100000, 50000), (48000, 30000, 90000), (100000, 150000, 100000)])),
       N("mg-joint-nrv", CC, "Product A sells for {{ka}} dollars after {{kp}} dollars of separable processing; product B sells for {{kb}} dollars after {{kq}} dollars of separable processing. The joint cost is {{kj}} dollars. How much joint cost goes to A by the net realisable value method?", "kj*(ka - kp)/(ka - kp + kb - kq)",
         f"solve(Eq({M}*((ka - kp) + (kb - kq)), kj*(ka - kp)), {M})[0]", "Net realisable value is final sales value less the costs incurred after split-off", tex="A",
         cases=C("kj ka kp kb kq", [(60000, 100000, 20000, 50000, 10000), (90000, 140000, 20000, 70000, 10000), (40000, 60000, 10000, 40000, 10000)]))])]),
 }),
 2: ("costing-systems", "Costing systems and overhead", I("1D2", "1D3"), ["BEHAVE"], {
   1: ("Attaching cost to output", [
     ("A", I("1D3"), "Set a predetermined overhead rate and find over- or underapplied overhead.",
      "Predetermined rate = budgeted overhead ÷ budgeted activity. Applied overhead = rate × actual activity. If actual overhead exceeds applied, overhead is underapplied.", "P1", [
       N("mg-overhead-rate", CS, "Budgeted manufacturing overhead is {{ko}} dollars and budgeted activity is {{kh}} direct labour hours. A job used {{kj}} hours. How much overhead is applied to the job?", "ko/kh*kj",
         f"solve(Eq({M}*kh, ko*kj), {M})[0]", "Rate first (dollars per hour), then rate times the job's hours", tex="OH",
         cases=C("ko kh kj", [(300000, 20000, 150), (480000, 40000, 85), (90000, 6000, 40), (750000, 50000, 320)])),
       N("mg-underapplied", CS, "The predetermined rate is {{kr}} dollars per machine hour. Actual machine hours were {{kh}} and actual overhead was {{ka}} dollars. Find the underapplied overhead (a negative answer means overapplied).", "ka - kr*kh",
         f"solve(Eq(kr*kh + {M}, ka), {M})[0]", "Underapplied means less was applied to jobs than was actually spent", tex="U",
         cases=C("kr kh ka", [(12, 21000, 260000), (15, 19000, 280000), (6, 14000, 87000), (20, 9800, 190000)]))]),
     ("B", I("1D2"), "Cost a job and choose between job-order and process costing.",
      "Job cost = direct materials + direct labour + applied overhead. Job-order costing suits distinct, custom jobs; process costing suits a continuous flow of identical units.", "P1", [
       N("mg-job-cost", CS, "A job used {{ka}} dollars of direct materials and {{kh}} direct labour hours at {{kw}} dollars per hour. Overhead is applied at {{kr}} dollars per direct labour hour. Find the total cost of the job.", "ka + kh*kw + kh*kr",
         f"solve(Eq(({M} - ka)/kh, kw + kr), {M})[0]", "Materials, labour and applied overhead; actual overhead never goes to a job directly", tex="cost", final=True,
         cases=C("ka kh kw kr", [(1200, 40, 25, 15), (3500, 120, 30, 20), (800, 16, 22, 18), (5000, 200, 28, 12)])),
       L("mg-job-or-process", CS, "Job-order or process costing? {{q}}", ["Job-order costing", "Process costing"], [
           ("A custom home builder", 0), ("An oil refinery", 1), ("A law firm billing by engagement", 0), ("A soft drink bottler", 1), ("A print shop making wedding invitations", 0), ("A cement plant", 1)],
         "Distinct jobs against a stream of identical units")]),
     ("C", I("1D2"), "Find equivalent units and cost per equivalent unit by the weighted-average method.",
      "Equivalent units = units completed and transferred out + ending work in process × its percentage of completion. Cost per equivalent unit = (beginning WIP cost + costs added) ÷ equivalent units.", "P1", [
       N("mg-equivalent-units", CS, "A department completed and transferred out {{kt}} units and has {{kw}} units in ending work in process that are {{kp}}% complete as to conversion. Find the equivalent units for conversion by the weighted-average method.", "kt + kw*kp/100",
         f"solve(Eq(({M} - kt)*100, kw*kp), {M})[0]", "Finished units count whole; unfinished units count for the fraction done", tex="EU",
         cases=C("kt kw kp", [(8000, 2000, 40), (15000, 5000, 60), (4500, 1500, 20), (20000, 4000, 75)])),
       N("mg-cost-per-eu", CS, "Beginning work in process carried {{kb}} dollars of conversion cost and {{ka}} dollars were added in the period. Equivalent units for conversion are {{ku}}. Find the conversion cost per equivalent unit (weighted average).", "(kb + ka)/ku",
         f"solve(Eq({M}*ku - ka, kb), {M})[0]", "Weighted average pools beginning and current costs", tex="c",
         cases=C("kb ka ku", [(4000, 40000, 8800), (9000, 81000, 18000), (1500, 22500, 4800), (10000, 105000, 23000)]))]),
     ("D", I("1D2"), "Assign overhead with activity-based costing.",
      "Each activity pool has its own rate = pool cost ÷ total driver volume; a product is charged rate × the driver units it uses. ABC shifts overhead toward low-volume, complex products compared with a single volume-based rate.", "P1", [
       N("mg-abc-assign", CS, "Setups cost {{ks}} dollars for {{kn}} setups in total, and inspections cost {{kq}} dollars for {{km}} inspections in total. A product line uses {{ka}} setups and {{kb}} inspections. How much overhead does ABC assign to it?", "ks/kn*ka + kq/km*kb",
         f"solve(Eq({M} - ks*ka/kn, kq*kb/km), {M})[0]", "One rate per activity, then charge by use", tex="OH",
         cases=C("ks kn kq km ka kb", [(60000, 200, 40000, 800, 30, 100), (90000, 300, 50000, 1000, 120, 250), (24000, 60, 36000, 900, 10, 300)])),
       F("mg-abc-concepts", CS, [
           ("Compared with one plant-wide rate based on labour hours, what does ABC usually do to the cost of a low-volume, complex product?", "raises it", "lowers it", "leaves it unchanged", "sets it to its direct cost"),
           ("What is a cost driver?", "a measure of activity that causes a cost pool to change", "the manager responsible for a cost", "a fixed cost", "the product with the highest cost"),
           ("Machine setups are which level of activity?", "batch level", "unit level", "product-sustaining level", "facility level"),
           ("Plant security is which level of activity?", "facility level", "unit level", "batch level", "product-sustaining level")],
         "Volume-based rates undercharge products that use many batches and much support for few units")]),
     ("E", I("1D3"), "Allocate service department costs.",
      "The direct method allocates each service department's cost only to production departments. The step-down method allocates in sequence and recognises some service-to-service use; the reciprocal method recognises all of it with simultaneous equations.", "P1", [
       N("mg-direct-method", CS, "A maintenance department costing {{kc}} dollars serves Machining for {{ka}} hours, Assembly for {{kb}} hours and the cafeteria (another service department) for {{ks}} hours. How much goes to Machining under the direct method?", "kc*ka/(ka + kb)",
         f"solve(Eq({M}*(ka + kb), kc*ka), {M})[0]", "The direct method ignores service given to other service departments", tex="alloc",
         cases=C("kc ka kb ks", [(120000, 6000, 4000, 2000), (90000, 3000, 6000, 1000), (200000, 12000, 8000, 5000), (45000, 2000, 1000, 500)])),
       L("mg-allocation-method", CS, "Which allocation method? {{q}}", ["Direct method", "Step-down method", "Reciprocal method"], [
           ("Ignores all services that service departments give each other", 0), ("Uses simultaneous equations to recognise all mutual services", 2),
           ("Allocates departments one after another, never back to one already closed", 1), ("The simplest and the least accurate of the three", 0), ("The most accurate in theory", 2)],
         "The methods differ only in how much service-to-service use they recognise")])]),
 }),
 3: ("cvp", "Cost-volume-profit", I("2C1"), ["BEHAVE"], {
   1: ("Breakeven and beyond", [
     ("A", I("2C1"), "Find contribution margin and the breakeven point.",
      "Contribution margin per unit = price − variable cost per unit. Breakeven units = fixed costs ÷ unit contribution margin; breakeven sales = fixed costs ÷ contribution margin ratio.", "P1", [
       N("mg-breakeven-units", CV, "A product sells for {{kp}} dollars with a variable cost of {{kv}} dollars per unit. Fixed costs are {{kf}} dollars. Find the breakeven point in units.", "kf/(kp - kv)",
         f"solve(Eq(kp*{M} - kv*{M} - kf, 0), {M})[0]", "Each unit contributes price minus variable cost toward the fixed costs", tex="Q",
         cases=C("kp kv kf", [(50, 30, 80000), (120, 72, 240000), (25, 10, 45000), (80, 60, 150000), (15, 9, 36000)])),
       N("mg-breakeven-dollars", CV, "Variable costs are {{kv}}% of sales and fixed costs are {{kf}} dollars. Find breakeven sales in dollars.", "kf/(1 - kv/100)",
         f"solve(Eq({M} - {M}*kv/100, kf), {M})[0]", "Divide fixed costs by the contribution margin ratio", tex="sales",
         cases=C("kv kf", [(60, 80000), (75, 150000), (40, 90000), (80, 36000), (55, 180000)]))]),
     ("B", I("2C1"), "Find the volume for a target profit and the margin of safety.",
      "Units for a target profit = (fixed costs + target profit) ÷ unit contribution margin. Margin of safety = actual or budgeted sales − breakeven sales.", "P1", [
       N("mg-target-profit-units", CV, "Price is {{kp}} dollars, variable cost {{kv}} dollars per unit, fixed costs {{kf}} dollars. How many units give a pre-tax profit of {{kt}} dollars?", "(kf + kt)/(kp - kv)",
         f"solve(Eq((kp - kv)*{M} - kf, kt), {M})[0]", "Treat the target profit as one more fixed amount to cover", tex="Q",
         cases=C("kp kv kf kt", [(50, 30, 80000, 40000), (120, 72, 240000, 96000), (25, 10, 45000, 30000), (80, 60, 150000, 50000)])),
       N("mg-margin-of-safety", CV, "Sales are {{ks}} dollars, the contribution margin ratio is {{kr}}% and fixed costs are {{kf}} dollars. Find the margin of safety as a percentage of sales.", "100*(ks - kf/(kr/100))/ks",
         f"solve(Eq(ks*(1 - {M}/100)*kr/100, kf), {M})[0]", "How far sales can fall before the company reaches breakeven", tex="MOS",
         cases=C("ks kr kf", [(500000, 40, 160000), (800000, 25, 150000), (300000, 60, 90000), (1000000, 20, 180000)]))]),
     ("C", I("2C1"), "Handle a sales mix and measure operating leverage.",
      "With several products, breakeven uses the weighted-average contribution margin at the given mix. Degree of operating leverage = contribution margin ÷ operating income; it multiplies a percentage change in sales into a percentage change in income.", "P1", [
       N("mg-mix-breakeven", CV, "A company sells {{ka}} units of A (unit contribution margin {{kp}} dollars) for every {{kb}} units of B (unit contribution margin {{kq}} dollars). Fixed costs are {{kf}} dollars. Find the breakeven point in total units.", "kf/((ka*kp + kb*kq)/(ka + kb))",
         f"solve(Eq({M}*ka/(ka + kb)*kp + {M}*kb/(ka + kb)*kq, kf), {M})[0]", "Average the contribution margins by the mix, then proceed as for one product", tex="Q",
         cases=C("ka kp kb kq kf", [(3, 10, 1, 30, 90000), (2, 20, 3, 10, 140000), (1, 40, 1, 20, 120000), (4, 5, 1, 25, 54000)])),
       N("mg-operating-leverage", CV, "Contribution margin is {{kc}} dollars and fixed costs are {{kf}} dollars. If sales rise by {{kg}}%, by what percentage does operating income rise?", "kc/(kc - kf)*kg",
         f"solve(Eq((kc*(1 + kg/100) - kf), (kc - kf)*(1 + {M}/100)), {M})[0]", "Degree of operating leverage times the percentage change in sales", tex="pct",
         cases=C("kc kf kg", [(200000, 150000, 10), (400000, 300000, 5), (120000, 60000, 20), (500000, 450000, 4)]))])]),
 }),
 4: ("budgeting", "Budgeting and forecasting", I("1B2", "1B3", "1B4", "1B5", "1B6"), ["PLANACT"], {
   1: ("The plan", [
     ("A", I("1B2", "1B4"), "Name the budgeting approach and order the master budget.",
      "The master budget starts from the sales budget, then production, materials, labour, overhead, selling and administrative, then the cash budget and pro forma statements. Zero-based budgets justify every item from nothing; rolling budgets add a period as one ends; flexible budgets adjust to actual volume; activity-based budgets build from activities and drivers.", "P2", [
       L("mg-budget-type", BU, "Which kind of budget? {{q}}", ["Zero-based", "Rolling (continuous)", "Flexible", "Activity-based", "Static"], [
           ("Every expense must be justified from scratch each period", 0), ("A new month is added as each month ends, so twelve months are always planned", 1),
           ("Costs are restated for the actual level of output", 2), ("Built from the cost of the activities needed and their drivers", 3), ("Prepared for one planned level of output and never adjusted", 4)],
         "Each approach answers a different weakness of last year plus a percentage"),
       F("mg-master-budget-order", BU, [
           ("Which budget is prepared first in the master budget?", "sales budget", "cash budget", "production budget", "budgeted balance sheet"),
           ("Which budget must be finished before the direct materials purchases budget?", "production budget", "cash budget", "budgeted income statement", "capital budget"),
           ("Which of these is a financial budget, not an operating budget?", "cash budget", "sales budget", "direct labour budget", "production budget"),
           ("What is budgetary slack?", "deliberately understating revenue or overstating cost to make targets easier", "the cash left at year end", "the difference between actual and standard cost", "unused plant capacity")],
         "Sales drive production, production drives the cost budgets, and everything meets in cash")]),
     ("B", I("1B5"), "Prepare production and purchases budgets.",
      "Production = budgeted sales + desired ending finished goods − beginning finished goods. Materials to purchase = production needs + desired ending materials − beginning materials.", "P1", [
       N("mg-production-budget", BU, "Budgeted sales are {{ks}} units. Beginning finished goods are {{kb}} units and the desired ending inventory is {{kn}} units. How many units must be produced?", "ks + kn - kb",
         f"solve(Eq(kb + {M} - ks, kn), {M})[0]", "Beginning plus production less sales leaves the ending inventory wanted", tex="units", final=True,
         cases=C("ks kb kn", [(10000, 1200, 1500), (25000, 3000, 2000), (8000, 500, 900), (40000, 6000, 4500)])),
       N("mg-purchases-budget", BU, "Production of {{kp}} units needs {{kr}} kg of material per unit. Beginning materials are {{kb}} kg and desired ending materials are {{kn}} kg. Material costs {{kc}} dollars per kg. Find the budgeted purchases in dollars.", "(kp*kr + kn - kb)*kc",
         f"solve(Eq(kb + {M}/kc - kp*kr, kn), {M})[0]", "The same inventory identity, one level down", tex="cost", final=True,
         cases=C("kp kr kb kn kc", [(5000, 2, 800, 1000, 3), (12000, 3, 4000, 2500, 2), (2000, 5, 600, 1100, 4), (9000, 4, 3000, 3600, 5)]))]),
     ("C", I("1B6"), "Build cash collections and a cash budget.",
      "Collections follow the credit pattern (so much in the month of sale, so much the next). Ending cash = beginning cash + receipts − disbursements; a shortfall against the minimum balance is borrowed.", "P1", [
       N("mg-cash-collections", BU, "Credit sales were {{ka}} dollars in May and {{kb}} dollars in June. The company collects {{kp}}% in the month of sale and the rest in the following month. Find June cash collections.", "kb*kp/100 + ka*(100 - kp)/100",
         f"solve(Eq({M} - kb*kp/100, ka - ka*kp/100), {M})[0]", "This month's share of this month's sales plus the remainder of last month's", tex="cash", final=True,
         cases=C("ka kb kp", [(200000, 240000, 60), (150000, 180000, 30), (90000, 120000, 75), (400000, 350000, 40)])),
       N("mg-cash-borrowing", BU, "Beginning cash is {{kb}} dollars, receipts are {{kr}} dollars and disbursements are {{kd}} dollars. The company keeps a minimum balance of {{km}} dollars. How much must it borrow?", "km - (kb + kr - kd)",
         f"solve(Eq(kb + kr - kd + {M}, km), {M})[0]", "Borrow the gap between the balance before financing and the minimum", tex="borrow", final=True,
         cases=C("kb kr kd km", [(20000, 150000, 165000, 15000), (8000, 90000, 110000, 10000), (50000, 300000, 335000, 25000), (12000, 60000, 71000, 5000)]))]),
     ("D", I("1B3"), "Forecast with a learning curve and an expected value.",
      "On a cumulative-average learning curve, each doubling of cumulative output multiplies the cumulative average time per unit by the learning rate. Expected value is the probability-weighted average of the outcomes.", "P1", [
       N("mg-learning-curve", BU, "The first unit takes {{kt}} hours and an {{kl}}% cumulative-average learning curve applies. Find the total hours for the first {{kn}} units.", "kn*kt*(kl/100)^log2(kn)",
         "kn*kt*exp(log(kn)/log(2)*log(Rational(kl, 100)))", "Each doubling multiplies the average time per unit by the learning rate; total is average times units", tex="hours",
         cases=C("kt kl kn", [(100, 80, 4), (200, 90, 2), (50, 80, 8), (1000, 70, 4), (40, 90, 8)])),
       N("mg-expected-value", BU, "Sales next year will be {{ka}} dollars with probability {{kp}}, {{kb}} dollars with probability {{kq}}, and {{kd}} dollars otherwise. Find the expected sales.", "ka*kp + kb*kq + kd*(1 - kp - kq)",
         f"solve(Eq(({M} - ka*kp - kb*kq)/(1 - kp - kq), kd), {M})[0]", "Weight each outcome by its probability and add", tex="EV",
         cases=C("ka kp kb kq kd", [(500000, 0.2, 400000, 0.5, 300000), (1000000, 0.3, 800000, 0.4, 500000), (120000, 0.25, 100000, 0.5, 60000), (90000, 0.1, 70000, 0.6, 40000)]))])]),
 }),
 5: ("variances", "Standard costs and variances", I("1C1"), ["PLANACT"], {
   1: ("Actual against standard", [
     ("A", I("1C1"), "Build a flexible budget and separate volume from spending.",
      "A flexible budget restates the budget at the actual volume: variable cost per unit × actual units + fixed cost. Flexible-budget variance = actual − flexible budget; sales-volume variance = flexible budget − static budget.", "P1", [
       N("mg-flexible-budget", VA, "The static budget for {{ks}} units shows {{kv}} dollars of variable cost and {{kf}} dollars of fixed cost. Actual output was {{ka}} units. Find the total flexible budget cost.", "kv/ks*ka + kf",
         f"solve(Eq(({M} - kf)*ks, kv*ka), {M})[0]", "Scale the variable part to actual volume; leave the fixed part alone", tex="FB", final=True,
         cases=C("ks kv kf ka", [(10000, 80000, 50000, 12000), (5000, 150000, 90000, 4500), (20000, 100000, 60000, 23000), (8000, 96000, 40000, 7000)])),
       N("mg-flexible-budget-variance", VA, "The flexible budget allows {{kb}} dollars of variable cost per unit plus {{kf}} dollars fixed. Actual output was {{ka}} units and actual total cost was {{kt}} dollars. Find the flexible-budget cost variance in dollars (positive means unfavourable).", "kt - (kb*ka + kf)",
         f"solve(Eq(kb*ka + kf + {M}, kt), {M})[0]", "Compare actual cost with what the cost should have been at the actual volume, not the planned volume", tex="var", final=True,
         cases=C("kb kf ka kt", [(8, 50000, 12000, 150000), (30, 90000, 4500, 221000), (5, 60000, 23000, 172000), (12, 40000, 7000, 127500)]))]),
     ("B", I("1C1"), "Compute direct materials price and quantity variances.",
      "Price variance = (actual price − standard price) × actual quantity. Quantity variance = (actual quantity − standard quantity allowed for actual output) × standard price. Positive is unfavourable.", "P1", [
       N("mg-materials-price-variance", VA, "A company bought and used {{kq}} kg at {{ka}} dollars per kg; the standard price is {{ks}} dollars per kg. Find the materials price variance (positive means unfavourable).", "(ka - ks)*kq",
         f"solve(Eq(ks*kq + {M}, ka*kq), {M})[0]", "Hold quantity at actual and price the difference", tex="var",
         cases=C("kq ka ks", [(5000, 4.2, 4), (12000, 2.9, 3), (800, 15.5, 15), (20000, 1.1, 1.25)])),
       N("mg-materials-quantity-variance", VA, "Production of {{ku}} units has a standard of {{kr}} kg per unit at {{ks}} dollars per kg. Actual usage was {{kq}} kg. Find the materials quantity variance (positive means unfavourable).", "(kq - ku*kr)*ks",
         f"solve(Eq(ku*kr*ks + {M}, kq*ks), {M})[0]", "Standard quantity is for the output actually made; value the difference at the standard price", tex="var",
         cases=C("ku kr ks kq", [(1000, 5, 4, 5200), (4000, 3, 3, 11700), (250, 3, 15, 800), (8000, 2.5, 1.25, 20600)]))]),
     ("C", I("1C1"), "Compute direct labour rate and efficiency variances.",
      "Rate variance = (actual rate − standard rate) × actual hours. Efficiency variance = (actual hours − standard hours allowed) × standard rate.", "P1", [
       N("mg-labour-rate-variance", VA, "Workers were paid {{kp}} dollars in total for {{kh}} hours; the standard rate is {{ks}} dollars per hour. Find the labour rate variance (positive means unfavourable).", "kp - ks*kh",
         f"solve(Eq(({M} + ks*kh)/kh, kp/kh), {M})[0]", "Actual pay less what those hours should have cost", tex="var",
         cases=C("kp kh ks", [(84000, 4000, 20), (51300, 2700, 20), (126000, 6000, 22), (30400, 1900, 15)])),
       N("mg-labour-efficiency-variance", VA, "{{ku}} units were made; the standard is {{kr}} hours per unit at {{ks}} dollars per hour. Actual hours were {{kh}}. Find the labour efficiency variance (positive means unfavourable).", "(kh - ku*kr)*ks",
         f"solve(Eq({M}/ks + ku*kr, kh), {M})[0]", "Hours over or under standard, valued at the standard rate", tex="var",
         cases=C("ku kr ks kh", [(2000, 2, 20, 4100), (900, 3, 20, 2600), (1500, 4, 22, 6250), (1000, 2, 15, 1900)]))]),
     ("D", I("1C1"), "Compute overhead variances and say who can explain a variance.",
      "Variable overhead spending = actual − actual hours × standard rate; efficiency = (actual hours − standard hours) × standard rate. Fixed overhead budget variance = actual − budgeted; volume variance = budgeted − applied, unfavourable when production is below the denominator level.", "P1", [
       N("mg-fixed-volume-variance", VA, "Budgeted fixed overhead is {{kb}} dollars on a denominator of {{kd}} machine hours. Standard hours allowed for actual output were {{kh}}. Find the fixed overhead volume variance (positive means unfavourable).", "kb - kb/kd*kh",
         f"solve(Eq(({M} - kb)*kd, -kb*kh), {M})[0]", "Budgeted less applied: producing below the planned level leaves fixed overhead unabsorbed", tex="var",
         cases=C("kb kd kh", [(200000, 10000, 9000), (360000, 24000, 25000), (90000, 6000, 5400), (500000, 20000, 21500)])),
       L("mg-variance-owner", VA, "Who is usually best placed to explain this variance? {{q}}", ["Purchasing", "Production", "Sales or planning"], [
           ("An unfavourable materials price variance", 0), ("An unfavourable labour efficiency variance", 1), ("An unfavourable materials quantity variance from careless handling", 1),
           ("An unfavourable fixed overhead volume variance because orders fell", 2), ("A favourable materials price variance from buying a cheaper grade", 0)],
         "A variance is a question for the manager who controls that input; cheap material bought by purchasing can cause waste in production")])]),
 }),
 6: ("performance", "Performance measurement", I("1C2", "1C3"), ["PLANACT"], {
   1: ("Measuring managers and segments", [
     ("A", I("1C2"), "Classify responsibility centres.",
      "A cost centre manager controls costs; a revenue centre, revenues; a profit centre, both; an investment centre, profit and the assets used to earn it. Managers should be judged on what they can control.", "P2", [
       L("mg-responsibility-centre", PE, "Which kind of responsibility centre? {{q}}", ["Cost centre", "Revenue centre", "Profit centre", "Investment centre"], [
           ("A factory maintenance department", 0), ("A regional sales office that sets no prices and controls only selling effort", 1), ("A restaurant in a chain whose manager controls prices and costs but not new investment", 2),
           ("A division whose head decides on plant and equipment purchases", 3), ("The accounting department", 0)],
         "Ask what the manager can decide: costs, revenues, both, or assets as well"),
       F("mg-controllability", PE, [
           ("Which measure fits an investment centre and not a profit centre?", "return on investment", "total revenue", "cost variance", "units produced"),
           ("Allocated corporate headquarters cost in a division manager's evaluation is an example of what?", "an uncontrollable cost", "a controllable cost", "a variable cost", "an opportunity cost"),
           ("What is management by exception?", "investigating only the variances that are significant", "investigating every variance", "ignoring unfavourable variances", "budgeting from zero"),
           ("Which centre is a production department that is evaluated only on meeting standard cost?", "cost centre", "profit centre", "investment centre", "revenue centre")],
         "Responsibility accounting holds managers to account for what they control")]),
     ("B", I("1C3"), "Compute return on investment and residual income.",
      "ROI = operating income ÷ average operating assets = margin × turnover. Residual income = operating income − required rate × operating assets. ROI can lead a manager to reject a project that earns more than the cost of capital but less than the division's current ROI; residual income does not.", "P1", [
       N("mg-roi", PE, "A division has sales of {{ks}} dollars, operating income of {{kn}} dollars and average operating assets of {{ka}} dollars. Find its ROI in percent.", "100*kn/ka",
         f"solve(Eq((kn/ks)*(ks/ka)*100, {M}), {M})[0]", "Margin times turnover collapses to income over assets", tex="ROI",
         cases=C("ks kn ka", [(2000000, 240000, 1200000), (5000000, 400000, 2500000), (800000, 100000, 400000), (3000000, 450000, 3000000)])),
       N("mg-residual-income", PE, "A division earns {{kn}} dollars of operating income on {{ka}} dollars of operating assets. The required rate of return is {{kr}}%. Find its residual income.", "kn - kr/100*ka",
         f"solve(Eq(({M} - kn)*100, -kr*ka), {M})[0]", "Income above the minimum the assets must earn", tex="RI", final=True,
         cases=C("kn ka kr", [(240000, 1200000, 12), (400000, 2500000, 10), (100000, 400000, 15), (450000, 3000000, 18)]))]),
     ("C", I("1C2"), "Set a transfer price.",
      "The selling division's minimum transfer price is its variable cost per unit plus the contribution margin it gives up on outside sales (zero with idle capacity). The buying division's maximum is the outside market price.", "P1", [
       N("mg-transfer-minimum", PE, "A division makes a part at a variable cost of {{kv}} dollars and sells it outside for {{kp}} dollars. It is at full capacity. What is the minimum transfer price it should accept for an internal sale?", "kv + (kp - kv)",
         f"solve(Eq({M} - kv, kp - kv), {M})[0]", "At capacity every internal unit displaces an outside sale, so the floor is the market price", tex="TP", final=True,
         cases=C("kv kp", [(30, 50), (12, 20), (75, 110), (8, 15)])),
       F("mg-transfer-concepts", PE, [
           ("With idle capacity, what is the selling division's minimum acceptable transfer price?", "its variable cost per unit", "the market price", "full cost plus a markup", "zero"),
           ("What is the most the buying division should pay internally?", "the outside market price", "the seller's variable cost", "the seller's full cost", "any price the seller names"),
           ("What is the main risk of a transfer price set too high?", "the buyer purchases outside even though making inside is cheaper for the company", "the seller refuses outside orders", "fixed costs rise", "taxes fall to zero"),
           ("Which transfer price tends to preserve divisional autonomy when a competitive outside market exists?", "market price", "variable cost", "full cost", "a price dictated by headquarters")],
         "The range runs from the seller's opportunity cost up to the buyer's outside price")]),
     ("D", I("1C2", "1C3"), "Read a balanced scorecard and a segment margin.",
      "The balanced scorecard has four perspectives: financial, customer, internal business process, learning and growth. Segment margin = contribution margin − traceable fixed costs; common fixed costs are not allocated to segments.", "P1", [
       L("mg-scorecard-perspective", PE, "Which balanced scorecard perspective? {{q}}", ["Financial", "Customer", "Internal business process", "Learning and growth"], [
           ("Return on investment", 0), ("Percentage of repeat customers", 1), ("Defect rate", 2), ("Hours of employee training", 3), ("On-time delivery, as customers experience it", 1),
           ("Manufacturing cycle time", 2), ("Employee turnover", 3)],
         "Learning drives processes, processes drive customers, customers drive financial results"),
       N("mg-segment-margin", PE, "A segment has sales of {{ks}} dollars, variable costs of {{kv}} dollars and traceable fixed costs of {{kt}} dollars. Common fixed costs allocated to it are {{ka}} dollars. Find the segment margin.", "ks - kv - kt",
         f"solve(Eq({M} + kt + kv, ks), {M})[0]", "Stop before common costs: they would remain if the segment were dropped", tex="margin", final=True,
         cases=C("ks kv kt ka", [(500000, 300000, 120000, 50000), (900000, 540000, 200000, 90000), (250000, 100000, 110000, 60000), (1200000, 840000, 150000, 100000)]))])]),
 }),
 7: ("decisions", "Decision analysis", I("2C2", "2C3", "2E1", "2E2"), ["DIFF"], {
   1: ("Choosing", [
     ("A", I("2C2"), "Tell relevant costs from irrelevant ones.",
      "A relevant cost is a future cost that differs between alternatives. Sunk costs are irrelevant. An opportunity cost (the benefit given up) is relevant although it is never recorded.", "P2", [
       L("mg-relevant", DE, "Relevant or irrelevant to the decision? {{q}}", ["Relevant", "Irrelevant"], [
           ("The price paid three years ago for a machine that may be replaced", 1), ("The resale value today of that old machine", 0), ("Rent that continues whichever product is made", 1),
           ("Contribution lost on regular sales displaced by a special order", 0), ("Direct materials needed only if the order is accepted", 0), ("Book value of obsolete inventory", 1)],
         "Future and different: both must hold"),
       F("mg-cost-terms", DE, [
           ("What is a sunk cost?", "a cost already incurred that no decision can change", "a cost that varies with output", "the benefit given up by choosing an alternative", "a cost that will be paid next year"),
           ("What is an opportunity cost?", "the benefit forgone by choosing one alternative over the next best", "a cost recorded in the ledger", "a past cost", "a cost that is the same under every alternative"),
           ("A cost that could be eliminated by dropping a product line is called what?", "avoidable", "sunk", "common", "committed"),
           ("Which unit cost is most dangerous to use in a short-run decision?", "full unit cost including allocated fixed overhead", "variable cost per unit", "incremental cost", "outside purchase price")],
         "Unitised fixed cost looks variable and is not")]),
     ("B", I("2C2"), "Decide a special order and a make-or-buy question.",
      "Accept a special order if its incremental revenue exceeds its incremental cost, including any contribution lost on displaced sales. Make rather than buy if the avoidable cost of making is below the purchase price plus any opportunity cost of the capacity.", "P1", [
       N("mg-special-order", DE, "A customer offers {{kp}} dollars per unit for {{kn}} units. Variable cost is {{kv}} dollars per unit, the order needs a one-time tool costing {{kt}} dollars, and there is idle capacity. Find the change in operating income if the order is accepted.", "(kp - kv)*kn - kt",
         f"solve(Eq(({M} + kt)/kn + kv, kp), {M})[0]", "Fixed costs already being paid do not change, so only contribution and the special tool count", tex="change", final=True,
         cases=C("kp kn kv kt", [(18, 5000, 14, 6000), (40, 2000, 31, 8000), (9, 10000, 7.5, 5000), (65, 800, 50, 4000)])),
       N("mg-make-or-buy", DE, "A company makes {{kn}} parts a year at a variable cost of {{kv}} dollars each, with {{ka}} dollars of fixed cost that would be avoided if it stopped. A supplier offers the part at {{kp}} dollars. Find the annual advantage of making over buying (negative means buying is better).", "kp*kn - (kv*kn + ka)",
         f"solve(Eq(kv*kn + ka + {M}, kp*kn), {M})[0]", "Compare the purchase cost with only the costs that making would add", tex="adv", final=True,
         cases=C("kn kv ka kp", [(10000, 12, 30000, 16), (5000, 20, 15000, 22), (20000, 7, 50000, 10), (8000, 45, 40000, 49)]))]),
     ("C", I("2C2"), "Decide to process further, drop a segment, or ration a scarce resource.",
      "Process further if incremental revenue exceeds incremental cost; joint costs are sunk. Drop a segment only if the avoidable fixed costs exceed the contribution margin lost. With one constraint, rank products by contribution margin per unit of the scarce resource.", "P1", [
       N("mg-process-further", DE, "A product can be sold at split-off for {{ka}} dollars or processed further at a cost of {{kc}} dollars and sold for {{kb}} dollars. Allocated joint cost is {{kj}} dollars. Find the gain from processing further (negative means sell at split-off).", "kb - ka - kc",
         f"solve(Eq(ka + kc + {M}, kb), {M})[0]", "The joint cost is the same either way and drops out", tex="gain", final=True,
         cases=C("ka kc kb kj", [(40000, 15000, 60000, 30000), (25000, 12000, 35000, 20000), (90000, 20000, 125000, 70000), (10000, 9000, 18000, 6000)])),
       N("mg-constraint-cm", DE, "A product sells for {{kp}} dollars, has a variable cost of {{kv}} dollars and needs {{kh}} machine hours per unit. Machine hours are the scarce resource. Find its contribution margin per machine hour.", "(kp - kv)/kh",
         f"solve(Eq({M}*kh + kv, kp), {M})[0]", "Rank by contribution per unit of the bottleneck, not per unit of product", tex="cm",
         cases=C("kp kv kh", [(100, 60, 4), (50, 35, 0.5), (240, 150, 6), (80, 44, 3)]))]),
     ("D", I("2C3"), "Price by cost-plus and by target costing.",
      "Cost-plus price = cost × (1 + markup). Target cost = the price the market will bear − the required profit: the price comes first and the cost must be engineered to fit.", "P1", [
       N("mg-cost-plus", DE, "A product's full cost is {{kc}} dollars per unit and the company prices at a {{km}}% markup on cost. Find the selling price.", "kc*(1 + km/100)",
         f"solve(Eq(({M} - kc)/kc*100, km), {M})[0]", "Markup is a percentage of cost, not of price", tex="P",
         cases=C("kc km", [(40, 25), (120, 50), (8, 60), (250, 20)])),
       N("mg-target-cost", DE, "The market price for a product is {{kp}} dollars and the company requires a profit of {{kr}}% of the selling price. Find the target cost per unit.", "kp*(1 - kr/100)",
         f"solve(Eq((kp - {M})/kp*100, kr), {M})[0]", "Start from the price and take the profit out; what is left is all the product may cost", tex="cost",
         cases=C("kp kr", [(200, 15), (50, 20), (1200, 25), (80, 10)]))]),
     ("E", I("2E1", "2E2"), "Evaluate an investment by payback and net present value.",
      "Payback = investment ÷ annual net cash inflow when inflows are even; it ignores the time value of money and everything after payback. NPV = present value of the cash flows at the required rate − the investment; accept when positive. IRR is the rate at which NPV is zero.", "P1", [
       N("mg-payback", DE, "A machine costs {{kc}} dollars and saves {{ks}} dollars of cash each year. Find the payback period in years.", "kc/ks", f"solve(Eq({M}*ks, kc), {M})[0]",
         "How long until the cash is back; not a measure of profitability", tex="years",
         cases=C("kc ks", [(120000, 30000), (500000, 125000), (45000, 18000), (84000, 24000)])),
       N("mg-npv-three-years", DE, "A project costs {{kc}} dollars now and returns {{ka}} dollars at the end of each of three years. The required rate is {{kr}}%. Find its net present value.", "ka/(1 + kr/100) + ka/(1 + kr/100)^2 + ka/(1 + kr/100)^3 - kc",
         "ka*(1 - (1 + Rational(kr, 100))**(-3))/Rational(kr, 100) - kc", "Discount each year's cash flow and subtract the outlay; the card sums three terms, the check uses the annuity factor", tex="NPV", tol=0.005,
         cases=C("kc ka kr", [(100000, 45000, 10), (250000, 100000, 8), (60000, 25000, 12), (40000, 15000, 5)]))])]),
 }),
}
ADD = [(f"{FW['code']}-{n}.{tn}.{lo[0]}", qq) for n, u in UNITS.items() for tn, (tt, los) in u[4].items() for lo in los for qq in lo[5]]
