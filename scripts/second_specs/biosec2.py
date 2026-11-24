"""Biosecurity foundations (BS, Nov 2026): applied epidemiology on CDC's Principles of Epidemiology (SS1978), national
capacities on the WHO JEE tool (3rd ed.), decontamination kinetics, Poisson detection, ASHRAE 241 clean air per person
and vaccination impact. Two types per objective. Policy, public-health and defence level only."""
from opl_dsl import Q

FILE, FRAMEWORK = "bs-foundations", "biosecurity"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
n = lambda v: f"nsimplify({v})"


def facts(name, skill, rows, explain, pace="recall"):
    return Q(name, skill, "{{q}}", pace=pace, cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


EPI, PREV, BIO, DET, WITH, COMB = "biosec.epidemiology", "biosec.prevent", "biosec.biosafety", "biosec.detect", "biosec.withstand", "biosec.combat"

ADD = [
    # ── 2.3.C decontamination ────────────────────────────────────────────
    ("BS-2.3.C", Q("bs-autoclave-time", BIO, "A load carries 10^{{k}} resistant spores. The D-value at 121 °C is {{Dv}} min. How many minutes reduce it to one in a million (10⁻⁶) chance of a survivor?",
        given={"k": {"pick": [4, 6, 8]}, "Dv": {"pick": [0.5, 1.5, 2]}}, value="(k + 6)*Dv", tex="t",
        verify=f"solve(Eq(k - x/{n('Dv')}, -6), x)[0]", explain="Each D-value is one log; from 10^k down to 10⁻⁶ is k + 6 logs")),
    ("BS-2.3.C", Q("bs-log-reduction", BIO, "A disinfectant brings {{N0}} organisms down to {{N}} in its contact time. What log reduction is that?",
        cases=[{"N0": "10⁷", "a": 7, "N": "100", "b": 2}, {"N0": "10⁶", "a": 6, "N": "10", "b": 1}, {"N0": "10⁸", "a": 8, "N": "1000", "b": 3}, {"N0": "10⁵", "a": 5, "N": "1", "b": 0}],
        value="a - b", tex="\\log_{10}", final=True, verify="log(Integer(10)**a/Integer(10)**b, 10)", explain="Log reduction = log₁₀(N₀/N): a 5-log kill leaves 1 in 100 000")),
    # ── 2.4.A JEE ────────────────────────────────────────────────────────
    ("BS-2.4.A", facts("bs-jee-area", PREV, [
        ("A country trains laboratory staff in biorisk management and inventories dangerous pathogens. Which JEE technical area?", "P7 Biosafety and biosecurity (Prevent)", "D1 National laboratory system (Detect)", "R4 Infection prevention and control (Respond)", "P5 Zoonotic disease (Prevent)"),
        ("Police and public-health officials hold joint exercises for a suspected deliberate event. Which area?", "R2 Linking public health and security authorities", "P1 Legal instruments", "D2 Surveillance", "R5 Risk communication"),
        ("A country sets up event-based reporting from clinics within 24 hours. Which area?", "D2 Surveillance", "P3 IHR coordination", "R1 Health emergency management", "D3 Human resources"),
        ("Animal-health and human-health agencies share outbreak data under a One Health plan. Which area?", "P5 Zoonotic disease", "P6 Food safety", "P4 Antimicrobial resistance", "PoE Points of entry"),
    ], "The JEE scores 19 technical areas in Prevent, Detect and Respond, plus points of entry, chemical and radiation events")),
    ("BS-2.4.A", facts("bs-jee-pillar", PREV, [
        ("Which pillar contains immunization in the JEE tool?", "Prevent", "Detect", "Respond", "Other hazards"),
        ("Which pillar contains the national laboratory system?", "Detect", "Prevent", "Respond", "Other hazards"),
        ("Which pillar contains risk communication and community engagement?", "Respond", "Prevent", "Detect", "Other hazards"),
        ("What does a JEE produce?", "Consensus scores on a five-level scale per indicator, with priority actions", "A binding sanction", "A ranking of countries by GDP", "A vaccine stockpile"),
    ], "The JEE is voluntary, external and multisectoral; it measures IHR core capacities")),
    # ── 3.1.D Poisson detection ──────────────────────────────────────────
    ("BS-3.1.D", Q("bs-detect-prob", DET, "Sequencing a sample is expected to yield {{lam}} target reads on average (Poisson). What is the probability of seeing at least one, in %?",
        given={"lam": {"pick": [0.1, 0.5, 1, 2, 3]}}, value="100*(1 - exp(-lam))", tex="P", verify=f"100*(1 - exp(-{n('lam')}))",
        explain="P(0) = e^{−λ}, so at λ = 1 a single sample misses the target 37% of the time")),
    ("BS-3.1.D", Q("bs-depth-for-confidence", DET, "How many target reads must be expected (Poisson mean) to see at least one with {{pc}}% probability?",
        given={"pc": {"pick": [90, 95, 99]}}, value="-log(1 - pc/100)", tex="\\lambda", verify="solve(Eq(exp(-x), 1 - Rational(pc, 100)), x)[0]",
        explain="λ = −ln(1 − P): about 2.3 for 90%, 3.0 for 95%, 4.6 for 99%")),
    # ── 4.1.C ASHRAE 241 ─────────────────────────────────────────────────
    ("BS-4.1.C", Q("bs-eca-per-person", WITH, "A room with {{occ}} people gets {{oa}} cfm of outdoor air, recirculates {{rec}} cfm through a filter that removes {{eff}}% of infectious particles, and has a portable cleaner with a clean air delivery rate of {{cadr}} cfm. What is the equivalent clean airflow per person, in cfm?",
        given={"occ": {"pick": [10, 20, 30]}, "oa": {"pick": [150, 300]}, "rec": {"pick": [600, 1000]}, "eff": {"pick": [50, 75, 90]}, "cadr": {"pick": [0, 250, 400]}},
        value="(oa + rec*eff/100 + cadr)/occ", tex="ECA", verify=f"solve(Eq(x*occ, oa + rec*Rational(eff, 100) + cadr), x)[0]",
        explain="Clean air adds: outdoor air counts in full, filtered air at the filter's efficiency, a cleaner at its CADR; ASHRAE 241 sets the per-person target by space type")),
    ("BS-4.1.C", Q("bs-occupancy-limit", WITH, "A space delivers {{tot}} cfm of equivalent clean air. In infection-risk mode the target is {{eci}} cfm per person. How many people can it hold?",
        given={"tot": {"pick": [900, 1500, 2400]}, "eci": {"pick": [30, 40, 50]}}, value="floor(tot/eci)", tex="N", final=True,
        verify=f"floor(Rational(tot, eci))", explain="Occupancy limit = clean air ÷ per-person target, rounded down; more clean air or fewer people both work")),
    # ── 5.1.D NNV ────────────────────────────────────────────────────────
    ("BS-5.1.D", Q("bs-nnv", COMB, "Without vaccination {{ar}}% of a group would become cases this season. A vaccine is {{VE}}% efficacious. How many people must be vaccinated to prevent one case?",
        given={"ar": {"pick": [1, 5, 10, 20]}, "VE": {"pick": [50, 60, 80, 90]}}, value="1/(ar/100*VE/100)", tex="NNV",
        verify="1/(Rational(ar, 100) - Rational(ar, 100)*(1 - Rational(VE, 100)))", explain="NNV = 1 / absolute risk reduction = 1/(AR × VE): low attack rates need many vaccinations per case averted")),
    ("BS-5.1.D", Q("bs-cases-averted", COMB, "{{nv}} people are vaccinated with a {{VE}}% efficacious vaccine where the unvaccinated attack rate is {{ar}}%. How many cases are averted?",
        given={"nv": {"pick": [10000, 100000]}, "VE": {"pick": [50, 70, 90]}, "ar": {"pick": [2, 5, 10]}}, value="nv*ar/100*VE/100", tex="N",
        verify="nv*Rational(ar, 100) - nv*Rational(ar, 100)*(1 - Rational(VE, 100))", explain="Expected cases without minus with vaccination")),
    # ── 7.1 disease occurrence ───────────────────────────────────────────
    ("BS-7.1.A", facts("bs-chain-link", EPI, [
        ("Handwashing mainly breaks which link in the chain of infection?", "Mode of transmission", "Reservoir", "Susceptible host", "Portal of exit"),
        ("Vaccination breaks which link?", "Susceptibility of the host", "Reservoir", "Mode of transmission", "Portal of entry"),
        ("Culling infected poultry targets which link?", "The reservoir", "The susceptible host", "Portal of entry", "Mode of transmission"),
        ("A respirator on a healthy worker protects mainly at which link?", "Portal of entry", "Reservoir", "Portal of exit", "Susceptible host's immunity"),
    ], "Agent in a reservoir → portal of exit → transmission → portal of entry → susceptible host; break any link")),
    ("BS-7.1.A", facts("bs-natural-history", EPI, [
        ("What is the incubation period?", "Time from infection to the onset of symptoms", "Time from infection to becoming infectious", "Time a person stays infectious", "Time from symptoms to recovery"),
        ("If the latent period is shorter than the incubation period, what follows?", "People can transmit before they have symptoms", "People never transmit", "Symptoms always come first", "Isolation of symptomatic cases stops spread"),
        ("What is the serial interval?", "Time between symptom onset in a case and in the person they infected", "Time from exposure to symptoms", "Time from symptoms to death", "Time between two tests"),
    ], "Presymptomatic spread happens whenever the latent period is shorter than the incubation period")),
    ("BS-7.1.B", Q("bs-exposure-from-peak", EPI, "A point-source outbreak's cases peak on day {{peak}} (counting from the first of the month). The illness's median incubation period is {{inc}} days. On about what day was the exposure?",
        given={"peak": {"pick": [10, 14, 18, 22]}, "inc": {"pick": [1, 2, 3, 4, 7]}}, value="peak - inc", tex="d", final=True, verify="solve(Eq(x + inc, peak), x)[0]",
        explain="For a single shared exposure, the peak falls about one median incubation period after it")),
    ("BS-7.1.B", facts("bs-epicurve-shape", EPI, [
        ("Cases rise sharply to one peak and fall within about one incubation period. Which pattern?", "Point source", "Propagated (person to person)", "Continuous common source", "Endemic"),
        ("Several peaks spaced about one incubation period apart. Which pattern?", "Propagated", "Point source", "Continuous common source", "Seasonal"),
        ("Cases rise and then plateau for weeks before a contaminated supply is fixed. Which pattern?", "Continuous common source", "Point source", "Propagated", "Sporadic"),
    ], "The shape of the curve says how people were exposed")),
    # ── 7.2 measures of risk ─────────────────────────────────────────────
    ("BS-7.2.A", Q("bs-attack-rate", EPI, "{{c}} of {{nn}} people at a banquet became ill. What is the attack rate, in %?",
        given={"c": {"pick": [12, 30, 45, 72]}, "nn": {"pick": [80, 120, 150]}}, value="100*c/nn", tex="AR", verify="100*Rational(c, nn)",
        explain="Attack rate = new cases ÷ population at risk during the outbreak")),
    ("BS-7.2.A", Q("bs-secondary-attack", EPI, "{{p}} primary cases live in households with {{hh}} other members in total. {{s}} of those members later fall ill. What is the secondary attack rate, in %?",
        given={"p": {"pick": [5, 10]}, "hh": {"pick": [20, 32, 40]}, "s": {"pick": [4, 6, 9]}}, value="100*s/hh", tex="SAR", verify="100*Rational(s, hh)",
        explain="Divide by susceptible contacts only: the primary cases are not in the denominator")),
    ("BS-7.2.B", Q("bs-prevalence-from-incidence", EPI, "A condition arises at {{inc}} new cases per 1000 people per year and lasts on average {{dur}} years. About what is its prevalence, per 1000?",
        given={"inc": {"pick": [2, 5, 10]}, "dur": {"pick": [0.5, 2, 4]}}, value="inc*dur", tex="P", verify=f"solve(Eq(x/{n('dur')}, inc), x)[0]",
        explain="In a steady state, prevalence ≈ incidence × duration: a cure lowers prevalence without changing incidence")),
    ("BS-7.2.B", facts("bs-incidence-or-prevalence", EPI, [
        ("A new treatment keeps patients alive longer without curing them. What happens to prevalence?", "It rises", "It falls", "It stays the same", "It becomes zero"),
        ("Which measure is right for tracking how fast new infections are occurring?", "Incidence", "Point prevalence", "Period prevalence", "Case fatality ratio"),
        ("A one-day serosurvey finds 12% with antibodies. What is that?", "A point prevalence of past infection", "An incidence rate", "An attack rate", "A case fatality ratio"),
    ], "Incidence counts new cases over time; prevalence counts all current cases at a time")),
    ("BS-7.2.C", Q("bs-risk-ratio", EPI, "In a cohort, {{a}} of {{n1}} who ate the salad became ill, and {{c}} of {{n0}} who did not. What is the risk ratio?",
        given={"a": {"pick": [30, 40, 45]}, "n1": {"pick": [50, 60]}, "c": {"pick": [5, 8, 10]}, "n0": {"pick": [50, 80]}}, value="(a/n1)/(c/n0)", tex="RR",
        verify="Rational(a, n1)*Rational(n0, c)", explain="RR = risk in exposed ÷ risk in unexposed: far above 1 points at the salad")),
    ("BS-7.2.C", Q("bs-odds-ratio", EPI, "In a case-control study, {{a}} of {{ca}} cases and {{b}} of {{co}} controls were exposed. What is the odds ratio?",
        given={"a": {"pick": [20, 30, 36]}, "ca": {"pick": [40, 50]}, "b": {"pick": [10, 15, 20]}, "co": {"pick": [60, 80]}}, value="(a*(co - b))/((ca - a)*b)", tex="OR",
        verify="(Rational(a, ca - a))/(Rational(b, co - b))", explain="OR = ad/bc; case-control studies sample on outcome, so they give odds ratios, not risks")),
    ("BS-7.2.D", Q("bs-attributable-fraction-exposed", EPI, "Among the exposed, risk is {{rr}} times that of the unexposed. What percentage of the exposed group's cases is attributable to the exposure?",
        given={"rr": {"pick": [1.5, 2, 4, 10]}}, value="100*(rr - 1)/rr", tex="AF_e", verify=f"100*(1 - 1/{n('rr')})", explain="AF among exposed = (RR − 1)/RR")),
    ("BS-7.2.D", Q("bs-paf", EPI, "{{pe}}% of a population is exposed, and the exposure has a risk ratio of {{rr}}. What is the population attributable fraction, in %?",
        given={"pe": {"pick": [10, 25, 50]}, "rr": {"pick": [2, 3, 5]}}, value="100*(pe/100*(rr - 1))/(1 + pe/100*(rr - 1))", tex="PAF",
        verify=f"100*(({n('pe')}/100*{n('rr')} + 1 - {n('pe')}/100) - 1)/({n('pe')}/100*{n('rr')} + 1 - {n('pe')}/100)",
        explain="PAF = (total risk − unexposed risk) ÷ total risk: how much disease would vanish if the exposure did")),
    # ── 7.3 surveillance and investigation ───────────────────────────────
    ("BS-7.3.A", facts("bs-investigation-steps", EPI, [
        ("Which step comes first in an outbreak investigation once the team is prepared?", "Confirm that an outbreak exists", "Implement control measures", "Write the report", "Test hypotheses with a case-control study"),
        ("When should control measures start?", "As soon as a likely source is known, even before the study is finished", "Only after the final report", "Only after laboratory confirmation of every case", "Never during the investigation"),
        ("What does 'describe by time, place and person' produce?", "An epidemic curve, a map of cases and a profile of who is affected", "A vaccine", "A legal case", "A press release"),
    ], "Prepare → confirm the outbreak → verify the diagnosis → define and find cases → describe → hypothesise → test → control → communicate")),
    ("BS-7.3.A", facts("bs-case-definition", EPI, [
        ("Early in an investigation, why use a loose case definition (including probable and possible cases)?", "To find as many potential cases as possible (high sensitivity)", "To make the study smaller", "To avoid laboratory testing", "It is required by law"),
        ("For an analytic study testing a hypothesis, which definition is better?", "A strict one (confirmed cases) to avoid misclassification", "The loosest possible", "Any symptom at all", "None"),
        ("What must a case definition include?", "Clinical criteria with limits of time, place and person", "The suspected cause", "The treatment", "The name of the index case"),
    ], "Case definitions trade sensitivity against specificity, and change as the investigation moves")),
    ("BS-7.3.B", Q("bs-surveillance-sensitivity", DET, "A capture-recapture audit estimates {{tc}} true cases in a district. The surveillance system reported {{rep}} cases, of which {{tp}} were real. What is the system's sensitivity, in %?",
        given={"tc": {"pick": [200, 250, 400]}, "rep": {"pick": [150, 180]}, "tp": {"pick": [120, 140]}}, value="100*tp/tc", tex="Se", verify="100*Rational(tp, tc)",
        explain="Sensitivity = true cases detected ÷ all true cases; under-reporting is normal")),
    ("BS-7.3.B", Q("bs-surveillance-pvp", DET, "A surveillance system reported {{rep}} cases; investigation confirmed {{tp}} of them. What is its predictive value positive, in %?",
        given={"rep": {"pick": [150, 180, 240]}, "tp": {"pick": [90, 120, 135]}}, value="100*tp/rep", tex="PVP", verify="100*Rational(tp, rep)",
        explain="PVP = true cases ÷ reported cases: low PVP wastes investigation effort")),
    # ── 7.4 transmission dynamics ────────────────────────────────────────
    ("BS-7.4.A", Q("bs-final-size", EPI, "In a well-mixed population with no interventions and R₀ = {{R0}}, what fraction is eventually infected, in %? (Solve z = 1 − e^{−R₀z}.)",
        cases=[{"R0": 1.5, "z": 0.582811643866}, {"R0": 2, "z": 0.79681213002}, {"R0": 2.5, "z": 0.892644753609}, {"R0": 3, "z": 0.940479790707}, {"R0": 4, "z": 0.980172598718}], value="100*z", tex="z", tol=0.002,
        verify=f"100*bs_final_size({n('R0')})", explain="Overshoot: the final size exceeds the herd-immunity threshold 1 − 1/R₀")),
    ("BS-7.4.A", Q("bs-reff-susceptibles", EPI, "R₀ = {{R0}} and {{im}}% of the population is already immune. What is R_eff?",
        given={"R0": {"pick": [1.5, 2.5, 4, 6]}, "im": {"pick": [20, 40, 60, 80]}}, value="R0*(1 - im/100)", tex="R_{eff}", verify=f"{n('R0')}*(1 - Rational(im, 100))",
        explain="R_eff = R₀ × susceptible fraction; growth stops when it falls below 1")),
    ("BS-7.4.B", Q("bs-zero-offspring", EPI, "Offspring per case follow a negative binomial with mean R = {{R}} and dispersion k = {{kk}}. What fraction of cases infect no one, in %?",
        given={"R": {"pick": [1.5, 2.5, 3]}, "kk": {"pick": [0.1, 0.5, 1, 10]}}, value="100*(1 + R/kk)^(-kk)", tex="P_0", verify=f"100*(1 + {n('R')}/{n('kk')})**(-{n('kk')})",
        explain="Small k (overdispersion) means most cases infect no one and a few infect many: target settings, not just people")),
    ("BS-7.4.B", facts("bs-superspreading", EPI, [
        ("With strong overdispersion (k ≈ 0.1), what share of cases typically causes about 80% of transmission?", "About 10–20%", "About 80%", "All cases equally", "About 50%"),
        ("Why does overdispersion make some introductions fizzle out?", "Most cases infect no one, so a chain often ends early", "R is below 1 for all pathogens", "Tests are better", "It does not"),
        ("Which control does overdispersion favour?", "Backward tracing and limiting crowded, poorly ventilated gatherings", "Only symptom checks", "Isolating everyone equally", "Nothing changes"),
    ], "Overdispersion is about heterogeneity: settings and behaviour concentrate transmission")),
]
