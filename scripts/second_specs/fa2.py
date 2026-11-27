"""Second question types for the eleven Financial Accounting objectives that listed one drill (Nov 2026). US GAAP.
Classification items are authored; amounts are recomputed. Kevin teaches this material and checks it."""
FILE, FRAMEWORK = "fa-second-types", "accounting-far"
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


ST, NFP, LL, LI, TR = "acct.statements", "acct.nfp-gov", "acct.long-lived", "acct.liabilities", "acct.transactions"
L("FA-1.1.A", "fa-cash-flow-section", ST, "On a US GAAP statement of cash flows, {{q}} is reported in:", ["Operating activities", "Investing activities", "Financing activities", "A noncash disclosure, outside the three sections"], [
  ("cash paid for dividends", 2), ("cash paid for equipment", 1), ("interest paid", 0), ("land acquired by issuing shares", 3), ("cash collected from customers", 0), ("repayment of loan principal", 2),
  ("dividends received", 0), ("cash paid for another company's bonds held as an investment", 1)],
  "Operating: what runs through net income, including interest paid and received and dividends received. Investing: long-lived assets and investments. Financing: owners and lenders. No cash, no section")
N("FA-1.2.A", "fa-nfp-restricted-balance", NFP, "A not-for-profit receives {{kx}} restricted by the donor to a programme and spends {{ky}} on that programme in the same year. By how much do net assets with donor restrictions rise for the year?",
  "kx - ky", f"solve(Eq({M} + ky, kx), {M})[0]", "The gift raises net assets with donor restrictions; spending for the purpose releases that amount to net assets without donor restrictions", tex="\\Delta", final=True,
  given={"kx": {"pick": [50000, 80000, 120000]}, "ky": {"pick": [20000, 35000, 50000]}})
N("FA-1.4.A", "fa-segment-75-test", ST, "A public company's consolidated external revenue is {{kx}}. Its reportable segments must together account for at least how much external revenue?", "0.75*kx", "Rational(3, 4)*kx",
  "After the 10% tests, more segments are added until the reportable ones cover 75% of consolidated external revenue", tex="revenue", given={"kx": {"pick": [400000, 1000000, 2400000]}})
N("FA-1.4.B", "fa-cash-to-accrual-revenue", ST, "Under the cash basis a business reports {{kc}} collected from customers. Accounts receivable rose from {{ka}} to {{kb}} during the year. What is revenue on the accrual basis?",
  "kc + kb - ka", f"solve(Eq(ka + {M} - kc, kb), {M})[0]", "Roll the receivable forward: beginning + revenue − collections = ending", tex="revenue", final=True,
  cases=C("kc ka kb", [(90000, 10000, 15000), (120000, 20000, 12000), (64000, 5000, 9000), (250000, 30000, 30000)]))
N("FA-2.3.B", "fa-avoidable-interest", LL, "Weighted-average accumulated expenditures on a self-built asset were {{kw}}. A {{ks}} construction loan carries {{k1}}%, and other debt averages {{k2}}%. Actual interest for the year was higher than the result. How much interest is capitalized?",
  "ks*k1/100 + (kw - ks)*k2/100", "Rational(k1, 100)*ks + Rational(k2, 100)*(kw - ks)", "Use the specific loan's rate up to its amount and the weighted rate of other debt on the rest; the total can never exceed actual interest", tex="interest",
  cases=C("kw ks k1 k2", [(500000, 300000, 8, 6), (800000, 500000, 10, 7), (400000, 100000, 6, 9), (1000000, 600000, 5, 8)]))
N("FA-2.5.A", "fa-goodwill-after-impairment", LL, "A reporting unit carries goodwill of {{kg}}. Its total carrying amount is {{kc}} and its fair value is {{kf}}. What goodwill remains on the balance sheet after the impairment test?",
  "kg - min(kg, kc - kf)", "kg - Min(kg, kc - kf)", "The loss is the excess of carrying amount over fair value, but never more than the goodwill itself", tex="goodwill", final=True,
  cases=C("kg kc kf", [(200000, 900000, 800000), (100000, 700000, 550000), (300000, 1200000, 1150000), (150000, 400000, 320000)]))
N("FA-2.6.A", "fa-note-principal-from-accrual", LI, "Year-end accrued interest on a {{kr}}% note signed {{km}} months before year end is {{ki}}. What is the note's principal?", "ki*1200/(kr*km)",
  f"solve(Eq({M}*Rational(kr, 100)*Rational(km, 12), ki), {M})[0]", "Interest = principal × annual rate × months/12, read backwards", tex="principal", final=True,
  cases=C("ki km kr", [(300, 3, 6), (500, 6, 5), (240, 4, 8), (750, 9, 10)]))
L("FA-3.1.A", "fa-change-treatment", TR, "{{q}} is accounted for:", ["Retrospectively, by adjusting prior periods presented", "Prospectively, in the current and future periods", "By restating prior periods as the correction of an error"], [
  ("A switch from FIFO to weighted-average inventory costing", 0), ("A revised useful life for equipment", 1), ("A change in depreciation method", 1), ("A prior-year inventory count that was added up wrong", 2),
  ("A change from an accounting method that was never acceptable to GAAP", 2), ("A revised estimate of uncollectible receivables", 1), ("A change in the entities included in the consolidated statements", 0)],
  "Principle and reporting entity: retrospective. Estimate: prospective, and a change in depreciation method is treated as a change in estimate. A mistake, including moving from non-GAAP to GAAP: restatement")
L("FA-3.1.B", "fa-contingency-amount", TR, "{{q}} The company should:", ["Accrue the low end of the range and disclose the exposure above it", "Accrue the best estimate", "Disclose only", "Neither accrue nor disclose"], [
  ("A loss is probable and estimated between two amounts, with no amount in the range more likely than another.", 0), ("A loss is probable, and one amount within the range is the best estimate.", 1),
  ("A loss is reasonably possible.", 2), ("A loss is remote (and is not a guarantee).", 3), ("A gain is probable.", 2), ("A loss is probable but cannot be reasonably estimated.", 2)],
  "Accrue only when probable and estimable; with a range and no best estimate, accrue the minimum. Gain contingencies are not recognised until realised")
N("FA-3.1.C", "fa-subsequent-event-liability", TR, "At year end a company had accrued {{ka}} for a lawsuit. Before the statements were issued, {{q}} {{kb}}. What liability does the year-end balance sheet report?",
  "ka + kt*(kb - ka)", "kt*kb + (1 - kt)*ka", "Evidence about a condition that existed at the balance sheet date adjusts the statements. A new event after year end is disclosed, not recognised", tex="liability", final=True,
  cases=[{"ka": 100000, "kb": 140000, "kt": 1, "q": "the same case was settled for"}, {"ka": 250000, "kb": 200000, "kt": 1, "q": "the same case was settled for"},
         {"ka": 100000, "kb": 60000, "kt": 0, "q": "a new, unrelated suit over an accident that happened after year end was settled for"},
         {"ka": 80000, "kb": 300000, "kt": 0, "q": "a fire after year end caused an uninsured loss of"}])
L("FA-3.4.A", "fa-valuation-approach", TR, "Measuring fair value from {{q}} uses the:", ["Market approach", "Income approach", "Cost approach"], [
  ("earnings multiples of comparable public companies", 0), ("discounted future cash flows", 1), ("current replacement cost, adjusted for obsolescence", 2), ("an option-pricing model", 1),
  ("matrix pricing of similar bonds", 0), ("prices in recent sales of similar assets", 0)],
  "Market: prices from comparable transactions. Income: future amounts converted to a present value. Cost: what it would take to replace the asset's service capacity")
assert len(ADD) == 11
