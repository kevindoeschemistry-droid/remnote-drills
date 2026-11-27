"""Stochastic Processes unit 5 (Nov 2026): martingales, optional stopping, the binomial pricing model and Brownian
motion, on the Cambridge Part II Stochastic Financial Models schedule (read through an extraction of the 2026-27
Schedules). Pricing is asked as mathematics: a risk-neutral expectation, checked by replication."""
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "sto-martingales", "stochastic-processes", "P1"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
MG = "stoch.martingales"
B = ["cambridge-ii-stochastic-financial-models:MG", "cambridge-ii-stochastic-financial-models:BM", "cambridge-ii-stochastic-financial-models:BR"]
M, BN, BR = ([x] for x in B)


def F(name, rows, explain):
    return Q(name, MG, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def N(name, prompt, value, verify, explain, tex="answer", final=False, **kw):
    return Q(name, MG, prompt, value=value, tex=tex, final=final, verify=verify, explain=explain, **kw)


UNITS = {"5": ("martingales", "Martingales and Brownian motion", ["STEP", "EQ"], B)}
TOPICS = {"5.1": "Fair games in discrete and continuous time"}
OBJS = [
 ("STO-5.1.A", M, "Compute a conditional expectation and decide whether a process is a martingale.",
  "M is a martingale when E[M_(n+1) | past] = M_n: a fair game. For a simple symmetric walk S_n, both S_n and S_n² − n are martingales; for a biased walk, (q/p)^S_n is."),
 ("STO-5.1.B", M, "Use the optional stopping theorem to find exit probabilities and expected exit times.",
  "For a martingale and a bounded stopping time (or bounded increments and finite mean time), E[M_T] = M₀. Applied to S_n it gives P(hit b before −a) = a/(a + b); applied to S_n² − n it gives E[T] = ab."),
 ("STO-5.1.C", BN, "Price a claim in the one-period binomial model by the risk-neutral probability.",
  "If the stock moves from S to uS or dS and the bank pays 1 + r, with d < 1 + r < u, the risk-neutral up-probability is q = (1 + r − d)/(u − d), and any claim costs its discounted q-expectation: the price of the portfolio that replicates it."),
 ("STO-5.1.D", BR, "Compute variances, covariances and hitting probabilities for Brownian motion.",
  "B_t − B_s is normal with mean 0 and variance t − s, independent of the past, so Cov(B_s, B_t) = min(s, t). Reflection principle: P(max over [0, t] ≥ a) = 2 P(B_t ≥ a)."),
]
ADD = [
 ("STO-5.1.A", N("sto-conditional-expectation", "Two fair dice are rolled and the first shows {{kk}}. Given that, find the expected value of the product of the two dice.", "kk*3.5", "kk*Rational(1 + 2 + 3 + 4 + 5 + 6, 6)",
    "Conditioning fixes the first die; the second is independent with mean 3.5, so the product has conditional mean k × 3.5 (and the total k + 3.5)", tex="E[XY|X]",
    given={"kk": {"pick": [2, 3, 4, 6]}})),
 ("STO-5.1.A", Q("sto-is-martingale", MG, "S_n is a simple symmetric random walk started at 0. Is {{pr}} a martingale?", pace="recall", cases=[
    {"pr": "S_n", "kc": 0}, {"pr": "S_n²", "kc": 1}, {"pr": "S_n² − n", "kc": 0}, {"pr": "S_n + n", "kc": 1}, {"pr": "S_n³ − 3nS_n", "kc": 0}, {"pr": "|S_n|", "kc": 1}, {"pr": "2^(S_n)", "kc": 1}, {"pr": "(−1)ⁿ S_n", "kc": 1}],
    choice=["Yes", "No"], correct="kc", verify="authored",
    explain="Average the two possible next values and compare with the current one: (s + 1)² and (s − 1)² average to s² + 1, so S_n² drifts up by 1 each step and S_n² − n is the fair version. A convex function of a martingale is a submartingale")),
 ("STO-5.1.B", N("sto-exit-probability", "A simple symmetric random walk starts at 0. Find the probability that it reaches +{{kb}} before −{{ka}}.", "ka/(ka + kb)", "pm_ruin_win(Rational(1, 2), ka, ka + kb)",
    "Optional stopping on S_n: 0 = E[S_T] = b·p − a·(1 − p), so p = a/(a + b). The nearer barrier is the likelier one", tex="P",
    given={"ka": {"pick": [1, 2, 3, 5]}, "kb": {"pick": [2, 4, 7]}})),
 ("STO-5.1.B", N("sto-exit-time", "A simple symmetric random walk starts at 0 and stops when it first reaches +{{kb}} or −{{ka}}. Find the expected number of steps.", "ka*kb", "pm_ruin_time(ka, ka + kb)", final=True,
    explain="Optional stopping on S_n² − n: E[T] = E[S_T²] = b² · a/(a + b) + a² · b/(a + b) = ab", tex="E[T]",
    given={"ka": {"pick": [1, 2, 3, 5]}, "kb": {"pick": [2, 4, 7]}})),
 ("STO-5.1.C", N("sto-risk-neutral-q", "A stock moves from 100 to {{su}} or {{sd}} over one period, and the bank pays interest {{kr}} per period. Find the risk-neutral probability of the up move.", "(100*(1 + kr) - sd)/(su - sd)", "solve(Eq(Symbol('m')*su + (1 - Symbol('m'))*sd, 100*(1 + nsimplify(kr))), Symbol('m'))[0]",
    "Under q the stock must earn the bank rate on average: q·uS + (1 − q)·dS = (1 + r)S", tex="q",
    cases=[{"su": 120, "sd": 80, "kr": 0.05}, {"su": 110, "sd": 95, "kr": 0.02}, {"su": 130, "sd": 90, "kr": 0.1}, {"su": 125, "sd": 80, "kr": 0}, {"su": 115, "sd": 85, "kr": 0.04}])),
 ("STO-5.1.C", N("sto-binomial-call", "A stock moves from 100 to {{su}} or {{sd}} over one period; the bank pays {{kr}} per period. Find the price of a call option with strike {{kx}} (it pays {{pu}} after an up move and nothing after a down move).", "((100*(1 + kr) - sd)/(su - sd))*pu/(1 + kr)", "pm_replicate_price(100, Rational(su, 100), Rational(sd, 100), kr, pu, 0)",
    "Price = discounted risk-neutral expectation, q × payoff/(1 + r). The same number is the cost of the stock-plus-borrowing portfolio that reproduces the payoff in both outcomes, which is why the real-world probability never appears", tex="price",
    cases=[{"su": 120, "sd": 80, "kr": 0.05, "kx": 100, "pu": 20}, {"su": 110, "sd": 95, "kr": 0.02, "kx": 100, "pu": 10}, {"su": 130, "sd": 90, "kr": 0.1, "kx": 110, "pu": 20},
           {"su": 125, "sd": 80, "kr": 0, "kx": 105, "pu": 20}, {"su": 115, "sd": 85, "kr": 0.04, "kx": 100, "pu": 15}])),
 ("STO-5.1.D", N("sto-brownian-variance", "B is a standard Brownian motion. Find the variance of B_{{ks}} + B_{{kt}}.", "ks + kt + 2*min(ks, kt)", "ks + kt + 2*Min(ks, kt)",
    "Var(X + Y) = Var X + Var Y + 2 Cov(X, Y), with Var B_t = t and Cov(B_s, B_t) = min(s, t): the two share the path up to the earlier time", tex="\\mathrm{Var}", final=True,
    cases=[{"ks": 1, "kt": 3}, {"ks": 2, "kt": 5}, {"ks": 4, "kt": 9}, {"ks": 3, "kt": 3}, {"ks": 1, "kt": 10}])),
 ("STO-5.1.D", N("sto-reflection", "B is a standard Brownian motion. Find the probability that it reaches the level {{ka}} at some time up to t = {{kt}}.", "1 - erf(ka/sqrt(2*kt))", "2*(1 - (1 + erf(ka/sqrt(2*kt)))/2)",
    "Reflection principle: paths that reach a are equally likely to end above or below it, so P(max ≥ a) = 2 P(B_t ≥ a) = 2(1 − Φ(a/√t))", tex="P", tol=0.01,
    cases=[{"ka": 1, "kt": 1}, {"ka": 1, "kt": 4}, {"ka": 2, "kt": 4}, {"ka": 3, "kt": 9}, {"ka": 2, "kt": 1}])),
]
