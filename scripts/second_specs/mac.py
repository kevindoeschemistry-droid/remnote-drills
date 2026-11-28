"""Macroeconomics (MAC, Nov 2026): principles of macroeconomics. Structure in UNITS (written by scripts/fw_setup.py),
two question types per objective.

Basis: the AP Macroeconomics Course and Exam Description (effective fall 2022), read through its Course at a Glance:
all six units with their weights and every topic title, so read: part (learning objectives and essential knowledge
not read). Items are the topics. Unit 1 of the AP course (scarcity, trade, supply and demand) is answered by the
Microeconomics framework and is not rebuilt. Monetary policy cards stay at the direction of each tool; the Federal
Reserve's operating framework has changed (ample reserves) and the detail should be checked before going deeper."""
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "mac-macroeconomics", "macroeconomics", "P1"
M = "Symbol('m')"
FW = dict(id="macroeconomics", title="Macroeconomics", code="MAC", domain="macro", track="business", requires=["microeconomics"], level=2,
          primary="ap-macroeconomics", also=[], subject="Business and Economics",
          note="Anchored on the AP Macroeconomics Course and Exam Description (2022), read through its topic list. AP unit 1 is left to Microeconomics. Introductory level: the Solow model, IS-LM, expectations-augmented dynamics and open-economy models belong to an intermediate course and are not built.",
          header=["The economy as a whole: how output, unemployment and prices are measured, the aggregate demand and",
                  "supply model, money and banking, what fiscal and monetary policy do in the short and long run, and",
                  "exchange rates. Each card is one identity, one multiplier or one shift."],
          source=dict(id="ap-macro-outline", title="Principles of macroeconomics by AP unit (course outline)", short="Macro outline", field="economics",
                      note=["The AP Macroeconomics units written as a source so the macro.* skills have a home.", "NOT a book: only the topic list was read. Chapter numbers are ours."]))
_T = [("1.1", "Scarcity"), ("1.2", "Opportunity cost and the production possibilities curve"), ("1.3", "Comparative advantage and gains from trade"), ("1.4", "Demand"), ("1.5", "Supply"),
      ("1.6", "Market equilibrium, disequilibrium and changes in equilibrium"),
      ("2.1", "The circular flow and GDP"), ("2.2", "Limitations of GDP"), ("2.3", "Unemployment"), ("2.4", "Price indices and inflation"), ("2.5", "Costs of inflation"),
      ("2.6", "Real versus nominal GDP"), ("2.7", "Business cycles"),
      ("3.1", "Aggregate demand"), ("3.2", "Multipliers"), ("3.3", "Short-run aggregate supply"), ("3.4", "Long-run aggregate supply"), ("3.5", "Equilibrium in the AD-AS model"),
      ("3.6", "Changes in the AD-AS model in the short run"), ("3.7", "Long-run self-adjustment"), ("3.8", "Fiscal policy"), ("3.9", "Automatic stabilisers"),
      ("4.1", "Financial assets"), ("4.2", "Nominal versus real interest rates"), ("4.3", "Definition, measurement and functions of money"), ("4.4", "Banking and the expansion of the money supply"),
      ("4.5", "The money market"), ("4.6", "Monetary policy"), ("4.7", "The loanable funds market"),
      ("5.1", "Fiscal and monetary policy actions in the short run"), ("5.2", "The Phillips curve"), ("5.3", "Money growth and inflation"), ("5.4", "Government deficits and the national debt"),
      ("5.5", "Crowding out"), ("5.6", "Economic growth"), ("5.7", "Public policy and economic growth"),
      ("6.1", "Balance of payments accounts"), ("6.2", "Exchange rates"), ("6.3", "The foreign exchange market"), ("6.4", "Effects of policies and conditions on the foreign exchange market"),
      ("6.5", "Changes in the foreign exchange market and net exports"), ("6.6", "Real interest rates and international capital flows")]
STDS = [{"id": "ap-macroeconomics", "name": "AP Macroeconomics Course and Exam Description (effective fall 2022)", "publisher": "College Board", "kind": "standard", "read": "part",
         "url": "https://apcentral.collegeboard.org/media/pdf/ap-macroeconomics-course-at-a-glance.pdf",
         "note": "Read Nov 2026 through an extraction of the Course at a Glance: the six units, their exam weights and all 42 topic titles. Learning objectives and essential knowledge were not read, so read: part. Items are the topics, titled in our words. Unit 1's topics are answered in the Microeconomics framework and are not cited from Macroeconomics.",
         "items": [{"code": c, "title": t} for c, t in _T]}]
SKILLS = [("indicators", "GDP, unemployment, price indices, real and nominal values, the business cycle", "Economic indicators", []),
          ("adas", "Aggregate demand and supply, multipliers, gaps, self-adjustment and fiscal policy", "National income and the price level", ["macro.indicators"]),
          ("finance", "Financial assets, interest rates, money, banking, the money market, monetary policy and loanable funds", "The financial sector", ["macro.adas"]),
          ("longrun", "Policy mixes, the Phillips curve, money growth, deficits and debt, crowding out and growth", "Long-run consequences", ["macro.finance"]),
          ("open", "The balance of payments, exchange rates and capital flows", "The open economy", ["macro.finance"])]
IDEAS = [("MEASURE", "Measure before you model", "GDP, the unemployment rate and the price level are defined by identities; getting the definition right settles most disputes about the numbers."),
         ("SHIFT", "Find the curve that moves", "Almost every question is: which curve shifts, which way, and what happens to the two things on the axes."),
         ("RUNS", "Short run and long run differ", "Policy can move output in the short run; in the long run output returns to potential and what remains is the price level, the interest rate or the debt.")]
PRACTICES = [("P1", "Compute", "Carry a macroeconomic identity or multiplier to a number."),
             ("P2", "Predict", "Say which curve shifts and which way an outcome moves, or classify a case.")]
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
IN, AD, FN, LR, OP = ["macro." + s[0] for s in SKILLS]
A = lambda *s: [f"ap-macroeconomics:{x}" for x in s]


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def L(name, skill, prompt, options, rows, explain):
    return Q(name, skill, prompt, pace="recall", cases=[{"q": a, "kc": k} for a, k in rows], choice=options, correct="kc", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", **kw):
    return Q(name, skill, prompt, value=value, tex=tex, verify=verify, explain=explain, **kw)


def C(keys, rows):
    return [dict(zip(keys.split(), r)) for r in rows]


UP, DN = "It rises", "It falls"
UNITS = {
 1: ("indicators", "Economic indicators and the business cycle", A("2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7"), ["MEASURE"], {
   1: ("Measuring the economy", [
     ("A", A("2.1", "2.2"), "Compute GDP by expenditure and decide what counts.",
      "GDP is the market value of final goods and services produced within a country in a period: C + I + G + (X − M). It leaves out intermediate goods, used goods, purely financial transactions, transfer payments and unpaid household work.", "P1", [
       N("mac-gdp-expenditure", IN, "Consumption is {{ka}}, investment {{kb}}, government purchases {{kg}}, exports {{kx}} and imports {{km}}, all in billions of dollars. Find GDP.", "ka + kb + kg + kx - km",
         f"solve(Eq({M} + km, ka + kb + kg + kx), {M})[0]", "C + I + G + net exports; imports are subtracted because they are in the other terms but were not produced here", tex="GDP", final=True,
         cases=C("ka kb kg kx km", [(700, 150, 200, 80, 100), (1400, 300, 350, 250, 200), (500, 90, 120, 60, 95), (9000, 2100, 2400, 1500, 2000)])),
       L("mac-gdp-counts", IN, "Is this counted in this year's GDP? {{q}}", ["Counted", "Not counted"], [
           ("A new car built and sold this year", 0), ("The sale of a ten-year-old house (the price itself)", 1), ("A Social Security payment", 1), ("Flour bought by a bakery to make bread it sells", 1),
           ("A haircut", 0), ("Shares of stock bought on an exchange", 1), ("A new factory built by a firm", 0), ("Housework done by a family for itself", 1), ("The estate agent's commission on a used house", 0)],
         "Final, newly produced, sold in a market: all three")]),
     ("B", A("2.3"), "Compute the unemployment rate and classify unemployment.",
      "The labour force is the employed plus the unemployed (without work and looking). Unemployment rate = unemployed ÷ labour force. Frictional unemployment is between jobs, structural is a mismatch of skills or place, cyclical comes from recessions; the natural rate is frictional plus structural.", "P1", [
       N("mac-unemployment-rate", IN, "A country has {{ka}} million employed, {{kb}} million unemployed and looking, and {{kd}} million adults not in the labour force. Find the unemployment rate in percent.", "100*kb/(ka + kb)",
         f"solve(Eq({M}/100*(ka + kb), kb), {M})[0]", "Unemployed over the labour force; people not looking are in neither part", tex="u",
         cases=C("ka kb kd", [(95, 5, 50), (138, 12, 60), (46, 4, 25), (27, 3, 20), (184, 16, 100)])),
       L("mac-unemployment-type", IN, "Which type of unemployment? {{q}}", ["Frictional", "Structural", "Cyclical"], [
           ("A graduate spends two months searching for a first job", 0), ("Coal miners lose jobs as power plants switch to gas", 1), ("A car plant lays off workers during a recession", 2),
           ("A nurse quits to move to another city and looks for work there", 0), ("Bank tellers are replaced by machines and their skills do not transfer", 1), ("Builders are idle because demand has fallen across the economy", 2)],
         "Between jobs, wrong skills, or not enough demand")]),
     ("C", A("2.4"), "Compute a price index and the inflation rate.",
      "CPI = cost of the market basket this year ÷ cost in the base year × 100. The inflation rate is the percentage change in the index from one year to the next.", "P1", [
       N("mac-cpi", IN, "A market basket cost {{kb}} dollars in the base year and costs {{ka}} dollars this year. Find this year's CPI.", "100*ka/kb", f"solve(Eq({M}*kb/100, ka), {M})[0]",
         "The base year's index is 100 by construction", tex="CPI",
         cases=C("kb ka", [(200, 230), (500, 540), (80, 100), (1200, 1500), (400, 390)])),
       N("mac-inflation-rate", IN, "The CPI rose from {{ka}} to {{kb}}. Find the inflation rate in percent.", "100*(kb - ka)/ka", f"solve(Eq(ka*(1 + {M}/100), kb), {M})[0]",
         "Percentage change in the index, measured from the earlier year", tex="\\pi",
         cases=C("ka kb", [(200, 210), (120, 126), (250, 245), (100, 108), (180, 189)]))]),
     ("D", A("2.5", "2.6"), "Convert nominal to real values and say who unexpected inflation helps.",
      "Real GDP = nominal GDP ÷ GDP deflator × 100. Real values strip out price changes. Unexpected inflation moves wealth from lenders and people on fixed incomes to borrowers, because debts are repaid in cheaper dollars.", "P1", [
       N("mac-real-gdp", IN, "Nominal GDP is {{kn}} billion dollars and the GDP deflator is {{kd}}. Find real GDP in billions of base-year dollars.", "100*kn/kd", f"solve(Eq({M}*kd/100, kn), {M})[0]",
         "Divide out the price level", tex="Y",
         cases=C("kn kd", [(2200, 110), (1500, 125), (900, 90), (18000, 120), (640, 160)])),
       L("mac-inflation-winners", IN, "Inflation turns out higher than expected. Is this party helped or hurt? {{q}}", ["Helped", "Hurt"], [
           ("A homeowner with a fixed-rate mortgage", 0), ("A bank that lent at a fixed rate", 1), ("A retiree on a fixed pension", 1), ("A government with a large fixed-rate debt", 0),
           ("A saver holding cash", 1), ("A firm that borrowed at a fixed rate to build a plant", 0)],
         "Whoever owes fixed dollars gains; whoever is owed them loses")]),
     ("E", A("2.7"), "Read the business cycle and the output gap.",
      "Output moves through expansion, peak, contraction and trough around potential output. The output gap is actual minus potential real GDP: negative (recessionary) when unemployment is above the natural rate, positive (inflationary) when it is below.", "P1", [
       N("mac-output-gap", IN, "Actual real GDP is {{ka}} billion dollars and potential real GDP is {{kb}} billion. Find the output gap as a percentage of potential.", "100*(ka - kb)/kb",
         f"solve(Eq(kb*(1 + {M}/100), ka), {M})[0]", "Negative means the economy is below potential", tex="gap",
         cases=C("ka kb", [(1900, 2000), (2100, 2000), (4750, 5000), (840, 800), (980, 1000)])),
       L("mac-cycle-phase", IN, "Which describes the economy? {{q}}", ["Recessionary gap", "Inflationary gap", "At potential output"], [
           ("Unemployment is 8% and the natural rate is 5%", 0), ("Unemployment is 3% and the natural rate is 5%", 1), ("Unemployment equals the natural rate", 2),
           ("Real GDP is below potential GDP", 0), ("Real GDP is above potential GDP and prices are accelerating", 1)],
         "Compare actual with potential, or unemployment with the natural rate")])]),
 }),
 2: ("adas", "National income and price determination", A("3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8", "3.9"), ["SHIFT", "RUNS"], {
   1: ("Aggregate demand and supply", [
     ("A", A("3.1"), "Explain the slope of aggregate demand and predict its shifts.",
      "AD slopes down through the real wealth, interest rate and exchange rate effects. It shifts with changes in consumption, investment, government purchases and net exports that are not caused by the price level.", "P2", [
       L("mac-ad-shift", AD, "What happens to aggregate demand? {{q}}", ["AD shifts right", "AD shifts left", "Movement along AD only"], [
           ("Consumer confidence rises", 0), ("The government cuts its purchases", 1), ("The price level falls", 2), ("Income taxes are cut", 0), ("Trading partners fall into recession", 1),
           ("Interest rates fall because the central bank eases", 0), ("Stock prices crash and households feel poorer", 1)],
         "A change in the price level is a movement along the curve; anything else that changes spending shifts it"),
       F("mac-ad-slope", AD, [
           ("A lower price level raises the purchasing power of money balances, so people spend more. Which effect is this?", "the real wealth effect", "the interest rate effect", "the exchange rate effect", "the multiplier effect"),
           ("A lower price level reduces the demand for money, lowering interest rates and raising investment. Which effect is this?", "the interest rate effect", "the real wealth effect", "the exchange rate effect", "crowding out"),
           ("A lower domestic price level makes exports cheaper abroad. Which effect is this?", "the exchange rate (net export) effect", "the real wealth effect", "the interest rate effect", "the substitution effect of micro demand"),
           ("Which is NOT a component of aggregate demand?", "the money supply", "consumption", "investment", "net exports")],
         "Three reasons the economy-wide curve slopes down, none of them the micro reason")]),
     ("B", A("3.2"), "Compute spending and tax multipliers.",
      "Spending multiplier = 1 ÷ (1 − MPC) = 1 ÷ MPS. Tax multiplier = −MPC ÷ (1 − MPC), smaller in size because part of a tax cut is saved. A balanced-budget change has a multiplier of 1.", "P1", [
       N("mac-spending-multiplier", AD, "The marginal propensity to consume is {{kc0}}. Government purchases rise by {{kg}} billion dollars. Find the maximum change in real GDP.", "kg/(1 - kc0)",
         f"solve(Eq({M}, kg + kc0*{M}), {M})[0]", "Each round of spending is the MPC times the last; the sum is 1/(1 − MPC)", tex="\\Delta Y",
         cases=C("kc0 kg", [(0.8, 50), (0.75, 100), (0.9, 20), (0.6, 40), (0.5, 30)])),
       N("mac-tax-multiplier", AD, "The marginal propensity to consume is {{kc0}}. Taxes are cut by {{kt}} billion dollars. Find the maximum change in real GDP.", "kc0*kt/(1 - kc0)",
         f"solve(Eq({M}, kc0*kt + kc0*{M}), {M})[0]", "The first round is only the part of the tax cut that is spent", tex="\\Delta Y",
         cases=C("kc0 kt", [(0.8, 50), (0.75, 100), (0.9, 20), (0.6, 40), (0.5, 30)]))]),
     ("C", A("3.3", "3.4"), "Predict shifts of short-run and long-run aggregate supply.",
      "SRAS slopes up because wages and some prices are sticky; it shifts with input prices, expected inflation and productivity. LRAS is vertical at potential output and shifts only with resources, technology and institutions.", "P2", [
       L("mac-as-shift", AD, "Which aggregate supply curve shifts, and which way? {{q}}", ["SRAS shifts left only", "SRAS shifts right only", "Both SRAS and LRAS shift right", "Both SRAS and LRAS shift left"], [
           ("Oil prices rise sharply for a few months", 0), ("Nominal wages fall", 1), ("A new technology raises productivity permanently", 2), ("A war destroys much of the capital stock", 3),
           ("Workers come to expect higher inflation", 0), ("The labour force grows through immigration", 2)],
         "Costs move the short-run curve; capacity moves both"),
       F("mac-as-slope", AD, [
           ("Why does short-run aggregate supply slope upward?", "wages and some input prices are slow to adjust, so higher prices raise profit per unit", "firms always produce at capacity", "money is neutral", "potential output rises with the price level"),
           ("Why is long-run aggregate supply vertical?", "in the long run all prices and wages adjust, so output depends only on resources and technology", "prices are fixed in the long run", "aggregate demand is vertical", "the central bank fixes output"),
           ("At what level of output does the long-run aggregate supply curve stand?", "potential (full-employment) output", "zero unemployment output", "the output of the last peak", "whatever aggregate demand sets"),
           ("Which change shifts long-run aggregate supply?", "a larger stock of capital", "a higher price level", "a cut in the money supply", "higher consumer confidence")],
         "Sticky in the short run, flexible in the long run")]),
     ("D", A("3.5", "3.6"), "Predict short-run effects of demand and supply shocks.",
      "A rise in AD raises both the price level and real output; a fall lowers both. A leftward shift of SRAS raises the price level and lowers output (stagflation); a rightward shift does the opposite.", "P2", [
       L("mac-shock-effect", AD, "In the short run, what happens to the price level and real output? {{q}}", ["Price level up, output up", "Price level down, output down", "Price level up, output down", "Price level down, output up"], [
           ("Aggregate demand increases", 0), ("Aggregate demand decreases", 1), ("Short-run aggregate supply decreases", 2), ("Short-run aggregate supply increases", 3),
           ("An oil price shock", 2), ("A collapse in business investment", 1), ("A surge in exports", 0)],
         "Demand shocks move price and output together; supply shocks move them apart"),
       L("mac-shock-unemployment", AD, "In the short run, what happens to unemployment? {{q}}", [UP, DN], [
           ("Aggregate demand decreases", 0), ("Aggregate demand increases", 1), ("Short-run aggregate supply decreases", 0), ("Short-run aggregate supply increases", 1), ("Government purchases rise", 1)],
         "Unemployment moves opposite to real output")]),
     ("E", A("3.7"), "Describe long-run self-adjustment.",
      "In a recessionary gap unemployment pushes nominal wages down over time, SRAS shifts right and output returns to potential at a lower price level. In an inflationary gap wages rise, SRAS shifts left and output returns to potential at a higher price level.", "P2", [
       L("mac-self-adjust", AD, "With no policy response, how does the economy return to potential? {{q}}", ["Wages fall and SRAS shifts right", "Wages rise and SRAS shifts left"], [
           ("The economy is in a recessionary gap", 0), ("The economy is in an inflationary gap", 1), ("Unemployment is above the natural rate", 0), ("Real GDP is above potential", 1)],
         "The labour market does the adjusting, through SRAS"),
       F("mac-long-run-result", AD, [
           ("Aggregate demand rises permanently from long-run equilibrium. After full adjustment, what has changed?", "the price level is higher and output is back at potential", "output is permanently higher", "the price level is unchanged", "unemployment is permanently lower"),
           ("Aggregate demand falls permanently from long-run equilibrium. After full adjustment, what has changed?", "the price level is lower and output is back at potential", "output is permanently lower", "the price level is higher", "potential output has fallen"),
           ("Why may policymakers not wait for self-adjustment in a recession?", "wages fall slowly, so the adjustment can take a long time", "it never happens", "it raises the price level", "it shifts long-run aggregate supply left"),
           ("In the long run, what determines real output?", "resources, technology and institutions", "aggregate demand", "the money supply", "the price level")],
         "Demand changes the price level in the long run, not output")]),
     ("F", A("3.8", "3.9"), "Choose a fiscal policy and size it with the multiplier.",
      "Expansionary fiscal policy (more spending, lower taxes) closes a recessionary gap; contractionary policy closes an inflationary gap. The spending change needed is the gap divided by the multiplier. Automatic stabilisers (income taxes, unemployment benefits) act without new legislation.", "P1", [
       N("mac-close-gap", AD, "Real GDP is {{kg}} billion dollars below potential and the marginal propensity to consume is {{kc0}}. By how much must government purchases rise to close the gap?", "kg*(1 - kc0)",
         f"solve(Eq({M}/(1 - kc0), kg), {M})[0]", "Divide the gap by the spending multiplier", tex="\\Delta G",
         cases=C("kg kc0", [(200, 0.8), (300, 0.75), (100, 0.9), (120, 0.6), (500, 0.5)])),
       L("mac-fiscal-kind", AD, "How would you classify this? {{q}}", ["Discretionary expansionary policy", "Discretionary contractionary policy", "Automatic stabiliser"], [
           ("Congress passes a one-time tax rebate in a recession", 0), ("Unemployment benefit payments rise as a recession deepens", 2), ("Parliament raises tax rates to cool inflation", 1),
           ("Income tax receipts fall as incomes fall", 2), ("A new public works programme is voted to fight a slump", 0), ("Government purchases are cut to reduce demand", 1)],
         "Automatic means built into existing law; discretionary means a new decision")])]),
 }),
 3: ("finance", "The financial sector", A("4.1", "4.2", "4.3", "4.4", "4.5", "4.6", "4.7"), ["SHIFT"], {
   1: ("Money, banks and interest", [
     ("A", A("4.1"), "Relate bond prices to interest rates and compare assets by liquidity.",
      "Bond prices and interest rates move in opposite directions: a bond paying a fixed coupon is worth less when new bonds pay more. Liquidity is how easily an asset becomes spendable without loss: cash, then deposits, then bonds and stocks.", "P1", [
       N("mac-perpetuity-price", FN, "A bond pays {{kp}} dollars a year forever. Find its price when the market interest rate is {{kr}}%.", "kp/(kr/100)", f"solve(Eq({M}*kr/100, kp), {M})[0]",
         "Price = payment over the rate, so doubling the rate halves the price", tex="P",
         cases=C("kp kr", [(50, 5), (50, 10), (30, 4), (80, 2), (60, 8)])),
       L("mac-bond-rate", FN, "What happens to the prices of previously issued bonds? {{q}}", ["They rise", "They fall"], [
           ("Market interest rates rise", 1), ("Market interest rates fall", 0), ("The central bank buys bonds in the open market", 0), ("The demand for bonds falls", 1)],
         "Old bonds must compete with the yield on new ones")]),
     ("B", A("4.2"), "Convert between nominal and real interest rates.",
      "Real interest rate ≈ nominal rate − inflation. Lenders set the nominal rate from the real return they want plus the inflation they expect (the Fisher relation), so the realised real rate depends on what inflation turns out to be.", "P1", [
       N("mac-real-rate", FN, "A loan carries a nominal interest rate of {{kn}}% and inflation is {{kp}}%. Find the real interest rate in percent (use the approximation).", "kn - kp",
         f"solve(Eq({M} + kp, kn), {M})[0]", "What the lender gains in purchasing power", tex="r", final=True,
         cases=C("kn kp", [(7, 3), (5, 6), (10, 2.5), (4, 1), (2, 5)])),
       N("mac-nominal-rate", FN, "Lenders want a real return of {{kr}}% and expect inflation of {{kp}}%. What nominal interest rate will they charge (use the approximation)?", "kr + kp",
         f"solve(Eq({M} - kp, kr), {M})[0]", "The Fisher relation: nominal = real + expected inflation", tex="i", final=True,
         cases=C("kr kp", [(3, 2), (2, 5), (4, 1.5), (1, 8), (2.5, 2.5)]))]),
     ("C", A("4.3"), "Define money by its functions and its measures.",
      "Money is a medium of exchange, a unit of account and a store of value. M1 is currency in circulation plus liquid deposits; M2 adds less liquid near-monies such as small time deposits and retail money market funds. Credit cards and stocks are not money.", "P2", [
       L("mac-money-function", FN, "Which function of money? {{q}}", ["Medium of exchange", "Unit of account", "Store of value"], [
           ("Paying for groceries with cash", 0), ("A shop lists prices in dollars", 1), ("Keeping savings in a bank account for next year", 2), ("Comparing the cost of two cars by their dollar prices", 1),
           ("Accepting wages in money and not in goods", 0), ("Holding banknotes in a safe", 2)],
         "Buy with it, count in it, keep it"),
       F("mac-money-measures", FN, [
           ("Which of these is part of M1?", "currency in circulation", "a share of stock", "a credit card limit", "a 10-year government bond"),
           ("Which of these is in M2 but is less liquid than currency?", "a small time deposit (certificate of deposit)", "a corporate bond", "gold jewellery", "a house"),
           ("Why is a credit card not money?", "it is a loan that must be repaid with money", "it is not accepted in shops", "it earns interest", "it is issued by a bank"),
           ("What backs fiat money?", "government decree and public acceptance, not a commodity", "gold reserves", "silver reserves", "the stock market")],
         "Money is defined by liquidity: how directly it can be spent")]),
     ("D", A("4.4"), "Compute bank reserves and the money multiplier.",
      "Required reserves = reserve ratio × deposits; excess reserves are what a bank may lend. With no leakages the banking system can expand deposits by the money multiplier, 1 ÷ reserve ratio, times the initial excess reserves.", "P1", [
       N("mac-excess-reserves", FN, "A bank has {{kd}} million dollars of deposits and {{kr}} million of reserves. The reserve requirement is {{kq}}%. Find its excess reserves in millions.", "kr - kq/100*kd",
         f"solve(Eq({M} + kq*kd/100, kr), {M})[0]", "Reserves held less reserves required", tex="ER",
         cases=C("kd kr kq", [(100, 25, 10), (500, 80, 10), (200, 50, 20), (80, 12, 5), (1000, 300, 25)])),
       N("mac-money-multiplier", FN, "The reserve requirement is {{kq}}% and banks hold no excess reserves. A new deposit creates {{ke}} million dollars of excess reserves. Find the maximum increase in the money supply from lending, in millions.", "ke/(kq/100)",
         f"solve(Eq({M}*kq/100, ke), {M})[0]", "Money multiplier 1/rr times the initial excess reserves", tex="\\Delta M",
         cases=C("kq ke", [(10, 90), (20, 40), (25, 30), (5, 19), (12.5, 70)]))]),
     ("E", A("4.5"), "Use the money market to find the direction of the nominal interest rate.",
      "The demand for money falls as the nominal interest rate rises; the supply is set by the central bank. An increase in the money supply lowers the nominal interest rate; an increase in money demand (higher price level or real income) raises it.", "P2", [
       L("mac-money-market", FN, "What happens to the nominal interest rate? {{q}}", [UP, DN], [
           ("The money supply increases", 1), ("The money supply decreases", 0), ("The price level rises, increasing money demand", 0), ("Real GDP falls, reducing money demand", 1), ("The central bank sells bonds", 0)],
         "More money relative to the demand for it means a lower price of holding it"),
       F("mac-money-demand", FN, [
           ("Why does the quantity of money demanded fall when the nominal interest rate rises?", "the opportunity cost of holding money rises", "people become poorer", "banks refuse deposits", "prices fall"),
           ("What is the opportunity cost of holding money?", "the interest forgone on other assets", "inflation only", "zero", "the price level"),
           ("Which change shifts the money demand curve to the right?", "a rise in the price level", "a rise in the interest rate", "a fall in real GDP", "a rise in the money supply"),
           ("In the simple money-market model, what shape is the money supply curve?", "vertical", "horizontal", "upward sloping", "downward sloping")],
         "The interest rate is the price of liquidity")]),
     ("F", A("4.6"), "Classify monetary policy actions and trace their effects.",
      "Expansionary monetary policy lowers interest rates to raise investment, aggregate demand and output; contractionary policy does the opposite. Buying bonds, lowering the rates the central bank administers or lowering reserve requirements are expansionary; the reverse actions are contractionary.", "P2", [
       L("mac-monetary-kind", FN, "Expansionary or contractionary? {{q}}", ["Expansionary", "Contractionary"], [
           ("The central bank buys government bonds", 0), ("The central bank raises its policy interest rate", 1), ("The central bank sells government bonds", 1), ("The reserve requirement is lowered", 0),
           ("The central bank lowers the interest rate it pays on reserves", 0), ("The discount rate is raised", 1)],
         "Anything that lowers market interest rates is expansionary"),
       L("mac-monetary-chain", FN, "The central bank adopts an expansionary policy. In the short run, what happens to {{q}}?", [UP, DN], [
           ("the nominal interest rate", 1), ("investment spending", 0), ("aggregate demand", 0), ("real output", 0), ("unemployment", 1), ("the price level", 0)],
         "Rates down, investment up, AD right, output and prices up")]),
     ("G", A("4.7"), "Use the loanable funds market to find the direction of the real interest rate.",
      "Savers supply loanable funds and borrowers demand them; the price is the real interest rate. Government borrowing raises demand (or reduces supply) and raises the real rate; more saving lowers it.", "P2", [
       L("mac-loanable-funds", FN, "What happens to the real interest rate? {{q}}", [UP, DN], [
           ("The government runs a larger budget deficit", 0), ("Households save a larger share of income", 1), ("Firms become more optimistic and want to invest more", 0), ("Foreign savers send more funds into the country", 1),
           ("The government moves from deficit to surplus", 1)],
         "More borrowing raises the price of funds; more saving lowers it"),
       F("mac-two-markets", FN, [
           ("Which interest rate is determined in the loanable funds market?", "the real interest rate", "the nominal interest rate", "the discount rate", "the exchange rate"),
           ("Which interest rate is determined in the money market?", "the nominal interest rate", "the real interest rate", "the tax rate", "the reserve ratio"),
           ("Who supplies loanable funds?", "savers", "borrowing firms", "the central bank only", "importers"),
           ("An investment tax credit is introduced. What happens in the loanable funds market?", "demand for loanable funds increases", "supply of loanable funds increases", "demand decreases", "nothing changes")],
         "Money market for the nominal rate, loanable funds for the real rate")])]),
 }),
 4: ("longrun", "Long-run consequences of stabilisation policy", A("5.1", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7"), ["RUNS"], {
   1: ("After the short run", [
     ("A", A("5.1"), "Combine fiscal and monetary policy.",
      "Expansionary fiscal and expansionary monetary policy both raise output and the price level but push interest rates in opposite directions: fiscal expansion raises them, monetary expansion lowers them. So the mix decides the interest rate when both are used.", "P2", [
       L("mac-policy-mix", LR, "What happens to interest rates? {{q}}", [UP, DN, "The direction is ambiguous"], [
           ("Expansionary fiscal policy alone", 0), ("Expansionary monetary policy alone", 1), ("Expansionary fiscal policy with expansionary monetary policy", 2),
           ("Contractionary fiscal policy with expansionary monetary policy", 1), ("Expansionary fiscal policy with contractionary monetary policy", 0)],
         "Fiscal expansion borrows, raising rates; monetary expansion supplies money, lowering them"),
       L("mac-policy-output", LR, "What happens to real output in the short run? {{q}}", [UP, DN, "The direction is ambiguous"], [
           ("Expansionary fiscal policy with expansionary monetary policy", 0), ("Contractionary fiscal policy with contractionary monetary policy", 1),
           ("Expansionary fiscal policy with contractionary monetary policy", 2), ("Contractionary fiscal policy with expansionary monetary policy", 2)],
         "When the two pull the same way on demand the output effect is clear; when they oppose it depends on size")]),
     ("B", A("5.2"), "Read the Phillips curve.",
      "The short-run Phillips curve slopes down: lower unemployment comes with higher inflation. Demand shocks move the economy along it; supply shocks and changes in expected inflation shift it. The long-run curve is vertical at the natural rate of unemployment.", "P2", [
       L("mac-phillips", LR, "What happens on the Phillips curve diagram? {{q}}", ["Movement up along the short-run curve", "Movement down along the short-run curve", "The short-run curve shifts right (up)", "The short-run curve shifts left (down)"], [
           ("Aggregate demand increases", 0), ("Aggregate demand decreases", 1), ("An oil price shock reduces short-run aggregate supply", 2), ("Expected inflation rises", 2),
           ("A productivity gain increases short-run aggregate supply", 3), ("Expected inflation falls", 3)],
         "Demand moves along the curve; supply and expectations move the curve"),
       F("mac-phillips-long-run", LR, [
           ("What shape is the long-run Phillips curve?", "vertical at the natural rate of unemployment", "downward sloping", "horizontal", "upward sloping"),
           ("In the long run, what can expansionary monetary policy change?", "the inflation rate, not the unemployment rate", "the unemployment rate, not inflation", "both permanently", "neither"),
           ("Stagflation appears on the Phillips curve diagram as what?", "a rightward shift of the short-run curve", "a movement down along the curve", "a movement up along the curve", "a leftward shift of the long-run curve"),
           ("A point to the left of the long-run Phillips curve corresponds to which gap?", "an inflationary gap", "a recessionary gap", "no gap", "a trade gap")],
         "The trade-off between inflation and unemployment is a short-run one")]),
     ("C", A("5.3"), "Apply the quantity theory of money.",
      "The equation of exchange is M × V = P × Y. With velocity and real output fixed, the price level moves in proportion to the money supply; in growth rates, inflation ≈ money growth + velocity growth − real output growth.", "P1", [
       N("mac-equation-of-exchange", LR, "The money supply is {{km}} billion dollars, velocity is {{kv}} and real output is {{ky}} billion units. Find the price level.", "km*kv/ky",
         f"solve(Eq(km*kv, {M}*ky), {M})[0]", "MV = PY", tex="P",
         cases=C("km kv ky", [(500, 4, 1000), (200, 5, 400), (800, 2, 2000), (300, 6, 900), (1000, 3, 1500)])),
       N("mac-money-growth-inflation", LR, "The money supply grows by {{km}}% a year, real output grows by {{ky}}% and velocity is constant. Find the long-run inflation rate in percent.", "km - ky",
         f"solve(Eq(km + 0, {M} + ky), {M})[0]", "Money growth beyond the growth of output shows up as inflation", tex="\\pi", final=True,
         cases=C("km ky", [(7, 3), (10, 2), (5, 2.5), (2, 3), (12, 4)]))]),
     ("D", A("5.4", "5.5"), "Compute deficits and debt ratios and explain crowding out.",
      "A deficit is one year's spending minus revenue; the debt is the accumulated total. The debt-to-GDP ratio measures the burden. Government borrowing raises the real interest rate and crowds out private investment, which slows capital accumulation and growth.", "P1", [
       N("mac-debt-ratio", LR, "Government debt was {{kd}} billion dollars. This year spending is {{ks}} billion and revenue {{kr}} billion, and GDP is {{kg}} billion. Find the debt-to-GDP ratio at the end of the year, in percent.", "100*(kd + ks - kr)/kg",
         f"solve(Eq({M}*kg/100 - kd, ks - kr), {M})[0]", "This year's deficit adds to the debt; then compare with GDP", tex="ratio",
         cases=C("kd ks kr kg", [(800, 300, 250, 1000), (1500, 600, 500, 2000), (400, 120, 130, 500), (9000, 2400, 1900, 10000)])),
       L("mac-crowding-out", LR, "The government increases deficit-financed spending. What happens to {{q}}?", [UP, DN], [
           ("the demand for loanable funds", 0), ("the real interest rate", 0), ("private investment", 1), ("the long-run growth of the capital stock", 1)],
         "Public borrowing competes with private borrowers for the same savings")]),
     ("E", A("5.6", "5.7"), "Measure growth and name its sources.",
      "Growth is the rise in real GDP per person, driven by physical capital, human capital and technology, and shown as an outward shift of the PPC and a rightward shift of LRAS. A quantity growing at g% a year doubles in about 70 ÷ g years.", "P1", [
       N("mac-rule-of-70", LR, "Real GDP per person grows at {{kg}}% a year. About how many years does it take to double, by the rule of 70?", "70/kg", f"solve(Eq({M}*kg, 70), {M})[0]",
         "Seventy over the growth rate in percent", tex="years",
         cases=C("kg", [(2,), (3.5,), (7,), (1,), (5,), (1.4,)])),
       L("mac-growth-policy", LR, "Does this raise long-run economic growth? {{q}}", ["Yes: it raises productive capacity", "No: it changes demand only"], [
           ("Public investment in education", 0), ("A one-time tax rebate that households spend", 1), ("Tax incentives for research and development", 0), ("An increase in the money supply", 1),
           ("Building ports and roads", 0), ("Policies that raise the saving and investment rate", 0)],
         "Growth policy moves long-run aggregate supply; stabilisation policy moves aggregate demand")])]),
 }),
 5: ("open", "The open economy", A("6.1", "6.2", "6.3", "6.4", "6.5", "6.6"), ["SHIFT"], {
   1: ("Trade and finance", [
     ("A", A("6.1"), "Place transactions in the balance of payments.",
      "The current account records trade in goods and services, income from abroad and transfers. The capital and financial account records purchases and sales of assets. Apart from measurement error the two sum to zero: a current account deficit is matched by a financial account surplus.", "P1", [
       N("mac-current-account", OP, "Exports are {{kx}}, imports {{km}}, net income from abroad {{kn}} and net transfers {{kt}}, all in billions of dollars. Find the current account balance.", "kx - km + kn + kt",
         f"solve(Eq({M} + km, kx + kn + kt), {M})[0]", "Trade balance plus net income plus net transfers", tex="CA", final=True,
         cases=C("kx km kn kt", [(500, 620, 40, -30), (900, 800, -20, -10), (250, 300, 15, 5), (1200, 1500, 100, -60)])),
       L("mac-bop-account", OP, "Current account or financial account? {{q}}", ["Current account", "Financial account"], [
           ("A country exports wheat", 0), ("A foreign firm buys a domestic factory", 1), ("Residents receive dividends from foreign shares", 0), ("A resident buys a foreign government bond", 1),
           ("Workers send money to family abroad", 0), ("Tourists from abroad spend on hotels", 0), ("A foreign investor buys domestic stock", 1)],
         "Goods, services, income and gifts in one; assets in the other")]),
     ("B", A("6.2"), "Convert currencies and measure appreciation.",
      "An exchange rate is the price of one currency in terms of another. A currency appreciates when it buys more of the other currency, which makes that country's exports dearer abroad and its imports cheaper.", "P1", [
       N("mac-convert-currency", OP, "One dollar buys {{kr}} units of a foreign currency. How many dollars does an item priced at {{kp}} units of that currency cost?", "kp/kr",
         f"solve(Eq({M}*kr, kp), {M})[0]", "Divide the foreign price by the units each dollar buys", tex="USD",
         cases=C("kr kp", [(0.9, 450), (150, 12000), (20, 500), (1.3, 65), (7, 2100)])),
       N("mac-appreciation", OP, "A dollar bought {{ka}} units of a foreign currency last year and buys {{kb}} units now. By what percentage has the dollar appreciated (negative means depreciated)?", "100*(kb - ka)/ka",
         f"solve(Eq(ka*(1 + {M}/100), kb), {M})[0]", "The dollar is stronger when it buys more foreign currency", tex="pct",
         cases=C("ka kb", [(100, 110), (0.8, 0.92), (20, 18), (150, 135), (1.25, 1.5)]))]),
     ("C", A("6.3", "6.4"), "Predict movements in the foreign exchange market.",
      "The demand for a currency comes from foreigners buying that country's goods and assets; the supply from residents buying foreign goods and assets. Higher domestic real interest rates, lower domestic prices or stronger foreign demand for exports make the currency appreciate.", "P2", [
       L("mac-forex", OP, "What happens to the value of the domestic currency? {{q}}", ["It appreciates", "It depreciates"], [
           ("Domestic real interest rates rise relative to those abroad", 0), ("Domestic inflation runs above inflation abroad", 1), ("Foreign demand for the country's exports rises", 0),
           ("Residents' incomes rise and they import more", 1), ("The central bank cuts interest rates", 1), ("Foreign investors want more of the country's assets", 0)],
         "Ask whether the event raises the demand for the currency or its supply"),
       F("mac-forex-market", OP, [
           ("In the market for dollars, who demands dollars?", "foreigners who want to buy US goods, services and assets", "US residents buying imports", "US tourists abroad", "the US Treasury only"),
           ("In the market for dollars, who supplies dollars?", "US residents who want foreign goods, services and assets", "foreigners buying US exports", "foreign tourists in the US", "foreign buyers of US bonds"),
           ("Under a floating exchange rate, what sets the rate?", "supply and demand in the foreign exchange market", "the central bank by decree", "an international treaty", "the price of gold"),
           ("The dollar appreciates against the euro. What has happened to the euro against the dollar?", "it has depreciated", "it has appreciated", "it is unchanged", "it cannot be determined")],
         "Every purchase of one currency is a sale of another")]),
     ("D", A("6.5", "6.6"), "Link exchange rates and interest rates to net exports and capital flows.",
      "An appreciation makes exports dearer and imports cheaper, reducing net exports and aggregate demand; a depreciation raises them. A higher domestic real interest rate attracts a financial capital inflow, which appreciates the currency.", "P2", [
       L("mac-net-exports", OP, "What happens to the country's net exports? {{q}}", [UP, DN], [
           ("Its currency depreciates", 0), ("Its currency appreciates", 1), ("Its trading partners grow faster", 0), ("Its own price level rises faster than prices abroad", 1), ("Its own income rises, with nothing else changed", 1)],
         "A cheaper currency sells more abroad and buys less from abroad"),
       L("mac-capital-flow", OP, "A country's real interest rate rises relative to the rest of the world. What happens to {{q}}?", [UP, DN], [
           ("financial capital inflow", 0), ("the demand for its currency", 0), ("the value of its currency", 0), ("its net exports", 1)],
         "Funds chase the higher return, bidding up the currency and squeezing exports")])]),
 }),
}
ADD = [(f"{FW['code']}-{n}.{tn}.{lo[0]}", qq) for n, u in UNITS.items() for tn, (tt, los) in u[4].items() for lo in los for qq in lo[5]]
