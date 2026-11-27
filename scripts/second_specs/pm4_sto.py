"""Stochastic Processes, the intermediate steps (Nov 2026): 13 objectives between the ones draft 1 jumped across —
reading a transition matrix and following a path before n-step powers, walks by counting paths before gambler's
ruin, balance checks before solving for an invariant distribution, exponential clocks before the Poisson process.
NEEDS rewires the framework. Basis unchanged: the Cambridge Markov Chains and Applied Probability schedules."""
from math import comb
import sympy as sp
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "sto-steps", "stochastic-processes", "P1"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
CH, WK, LR, PO = "stoch.chains", "stoch.walks", "stoch.longrun", "stoch.poisson"
M = lambda *s: [f"cambridge-ib-markov-chains:{x}" for x in s]
AP = lambda *s: [f"cambridge-ii-applied-probability:{x}" for x in s]


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", final=False, **kw):
    return Q(name, skill, prompt, value=value, tex=tex, final=final, verify=verify, explain=explain, **kw)


def P(rows):
    return sp.Matrix([[sp.Rational(x) for x in r.split(",")] for r in rows.split(";")])


def show(rows):
    return " ; ".join("(" + ", ".join(r.split(",")) + ")" for r in rows.split(";"))


def fl(x):
    return float(sp.Rational(x))


def stat(rows):
    Pm = P(rows); v = (Pm.T - sp.eye(Pm.shape[0])).nullspace()[0]
    return [x / sum(v) for x in v]


R3 = ["1/2,1/2,0;1/4,1/2,1/4;0,1/2,1/2", "1/2,1/4,1/4;1/3,1/3,1/3;0,1/2,1/2", "0,1/2,1/2;1/2,0,1/2;1/2,1/2,0", "1/5,4/5,0;1/2,0,1/2;0,1/4,3/4"]
R2 = ["9/10,1/10;1/2,1/2", "4/5,1/5;2/5,3/5", "1/2,1/2;1/4,3/4", "7/10,3/10;1/10,9/10"]

TOPICS = {"1.2": "Reading a chain", "2.2": "Walks by counting paths", "3.2": "Equilibrium by balance", "4.2": "Exponential clocks"}
OBJS = [
 ("STO-1.2.A", M("M1"), "Read and complete a transition matrix.", "Entry (i, j) is the probability of moving from state i to state j in one step. Every row is a probability distribution, so each row sums to 1; columns need not."),
 ("STO-1.2.B", M("M1"), "Find the probability of a particular path.", "By the Markov property the probability of a path is the product of its one-step transition probabilities: the future depends on the past only through the present state."),
 ("STO-1.2.C", M("M1"), "Evolve a starting distribution for one or two steps.", "If the chain starts with distribution μ (a row vector), after n steps its distribution is μPⁿ: multiply on the left, one step at a time."),
 ("STO-1.2.D", M("M1", "M2"), "Classify a state as absorbing, transient or recurrent from the diagram.", "A state is absorbing if the chain can never leave it. In a finite chain a state is recurrent if it lies in a closed class and transient if the chain can leave its class for good."),
 ("STO-2.2.A", M("M2"), "Find the distribution of a simple random walk after n steps by counting paths.", "A walk of n steps ends at k when it takes (n + k)/2 steps up, so P(S_n = k) = C(n, (n + k)/2) p^((n+k)/2) q^((n−k)/2), and zero unless n and k have the same parity."),
 ("STO-2.2.B", M("M2"), "Find the mean and variance of a random walk's position.", "Each step has mean p − q and variance 4pq, and steps are independent, so S_n has mean n(p − q) and variance 4npq. A symmetric walk is typically about √n from its start."),
 ("STO-2.2.C", M("M2"), "Compute return probabilities of the symmetric walk.", "The walk is at 0 after 2n steps with probability C(2n, n)/4ⁿ, about 1/√(πn). It first returns at step 2n with probability C(2n, n)/((2n − 1)4ⁿ)."),
 ("STO-3.2.A", M("M3"), "Check whether a given distribution is invariant.", "π is invariant when πP = π: for each state, the probability flowing in over one step equals the probability already there."),
 ("STO-3.2.B", M("M3"), "Use symmetry to find an invariant distribution without solving.", "If the columns of P also sum to 1 (a doubly stochastic matrix), the uniform distribution is invariant. A symmetric transition matrix is doubly stochastic."),
 ("STO-3.2.C", M("M3"), "Compute a long-run average from the invariant distribution.", "For an irreducible positive-recurrent chain the long-run average of f(X_n) is Σ π_i f(i), whatever the starting state (the ergodic theorem)."),
 ("STO-4.2.A", AP("P1"), "Compute with the exponential distribution and its memoryless property.", "An exponential time with rate λ has P(T > t) = e^(−λt) and mean 1/λ. Memoryless: given T > s, the remaining time is again exponential with rate λ."),
 ("STO-4.2.B", AP("P1"), "Find the time until the first of several independent exponential events.", "The minimum of independent exponentials with rates λ₁, …, λ_n is exponential with rate λ₁ + … + λ_n. With n identical clocks of rate λ the first rings after mean time 1/(nλ)."),
 ("STO-4.2.C", AP("P3"), "Find the idle probability and the mean time in an M/M/1 queue.", "With ρ = λ/μ < 1 the server is idle a fraction 1 − ρ of the time, and a customer spends on average 1/(μ − λ) in the system (Little's formula L = λW)."),
]
ADD = [
 ("STO-1.2.A", N("sto-missing-entry", CH, "A transition matrix has first row ({{ka}}, {{kb}}, ?). Find the missing entry.", "1 - ka - kb", "solve(Eq(nsimplify(ka) + nsimplify(kb) + Symbol('m'), 1), Symbol('m'))[0]",
    "Each row lists the probabilities of every possible next state, so it sums to 1", tex="p",
    cases=[{"ka": 0.2, "kb": 0.5}, {"ka": 0.1, "kb": 0.6}, {"ka": 0.25, "kb": 0.25}, {"ka": 0.4, "kb": 0.35}, {"ka": 0.05, "kb": 0.8}])),
 ("STO-1.2.A", F("sto-matrix-reading", CH, [
    ("In a transition matrix, the entry in row 2, column 3 is the probability of:", "Moving from state 2 to state 3", "Moving from state 3 to state 2", "Being in state 2 and state 3", "Staying in state 2"),
    ("Which must be true of every transition matrix?", "Each row sums to 1", "Each column sums to 1", "The diagonal entries are positive", "It is symmetric"),
    ("A diagonal entry equal to 1 means that state is:", "Absorbing", "Transient", "Unreachable", "Periodic"),
    ("A weather model says tomorrow depends only on today, not on earlier days. This is the:", "Markov property", "Law of large numbers", "Memoryless property of the exponential", "Detailed balance condition")],
    "Rows are 'from', columns are 'to'. Getting this backwards is the most common mistake with chains")),
 ("STO-1.2.B", N("sto-path-probability", CH, "A chain on states 0, 1, 2 has transition matrix with rows {{sh}}. Starting in state {{k0}}, find the probability that it visits {{k1}}, then {{k2}}, then {{k3}} in its next three steps.", "kans", "pm_mc_path(rows, pth)",
    "Multiply the three one-step probabilities along the path", tex="p",
    cases=[{"rows": r, "sh": show(r), "k0": a, "k1": b, "k2": c, "k3": d, "pth": f"{a},{b},{c},{d}", "kans": fl(P(r)[a, b] * P(r)[b, c] * P(r)[c, d])} for r, a, b, c, d in [
        (R3[0], 0, 1, 2, 2), (R3[0], 1, 1, 0, 1), (R3[1], 0, 1, 2, 1), (R3[2], 0, 1, 2, 0), (R3[3], 0, 1, 2, 2), (R3[1], 1, 0, 0, 2)]])),
 ("STO-1.2.B", N("sto-two-step-route", CH, "A chain on states 0 and 1 has transition matrix with rows {{sh}}. Starting in state 0, find the probability that it is in state 0 two steps later, summing over both routes.", "kans", "pm_mc_nstep(rows, 2, 0, 0)",
    "Two routes: stay then stay, or leave then come back. Add the two path probabilities", tex="p",
    cases=[{"rows": r, "sh": show(r), "kans": fl((P(r) ** 2)[0, 0])} for r in R2])),
 ("STO-1.2.C", N("sto-distribution-step", CH, "A chain on states 0, 1, 2 has transition matrix with rows {{sh}}. It starts in state 0 or state 2 with probability 1/2 each. Find the probability it is in state 1 after one step.", "kans", "pm_mc_dist(rows, '1/2,0,1/2', 1, 1)",
    "Weight each starting state's chance of moving to state 1 by the chance of starting there", tex="p",
    cases=[{"rows": r, "sh": show(r), "kans": fl((P(r)[0, 1] + P(r)[2, 1]) / 2)} for r in R3])),
 ("STO-1.2.C", N("sto-distribution-two-steps", CH, "A chain on states 0 and 1 has transition matrix with rows {{sh}}. It starts in state 0 with probability {{ka}}. Find the probability it is in state 0 after two steps.", "kans", "pm_mc_dist(rows, st, 2, 0)",
    "Apply the matrix twice: first find the distribution after one step, then use it as the start for the second", tex="p",
    cases=[{"rows": r, "sh": show(r), "ka": a, "st": f"{sp.Rational(str(a))},{1 - sp.Rational(str(a))}", "kans": fl((sp.Matrix([[sp.Rational(str(a)), 1 - sp.Rational(str(a))]]) * P(r) ** 2)[0, 0])} for r, a in zip(R2, (0.5, 0.2, 0.75, 0.4))])),
 ("STO-1.2.D", Q("sto-classify-state", CH, "In this chain, state {{ks}} is: {{ds}}", pace="recall", cases=[
    {"ds": "From 0 the chain stays at 0. From 1 it moves to 0 or 2 with probability 1/2 each. From 2 it stays at 2.", "ks": 1, "kc": 1},
    {"ds": "From 0 the chain stays at 0. From 1 it moves to 0 or 2 with probability 1/2 each. From 2 it stays at 2.", "ks": 0, "kc": 0},
    {"ds": "The chain moves 0 → 1 → 2 → 0 deterministically.", "ks": 1, "kc": 2},
    {"ds": "From 0 it moves to 1. From 1 it moves to 2. From 2 it moves to 1.", "ks": 0, "kc": 1},
    {"ds": "From 0 it moves to 1. From 1 it moves to 2. From 2 it moves to 1.", "ks": 2, "kc": 2},
    {"ds": "From 0 it stays with probability 1/2 or moves to 1. From 1 it stays for ever.", "ks": 1, "kc": 0}],
    choice=["Absorbing", "Transient", "Recurrent but not absorbing"], correct="kc", verify="authored",
    explain="Ask whether the chain, having left the state, is certain to come back. If it can escape to somewhere with no way back, the state is transient")),
 ("STO-1.2.D", F("sto-class-facts", CH, [
    ("In a finite Markov chain, at least one state must be:", "Recurrent", "Transient", "Absorbing", "Periodic"),
    ("A transient state is visited:", "Only finitely many times, with probability 1", "Infinitely often", "Exactly once", "Never"),
    ("A closed communicating class is one that:", "The chain cannot leave", "Contains an absorbing state", "Has period 1", "Contains every state"),
    ("In a finite chain, the states of a communicating class that is not closed are:", "Transient", "Recurrent", "Absorbing", "Periodic")],
    "A finite chain has to be somewhere for ever, so it cannot be transient everywhere")),
 ("STO-2.2.A", N("sto-walk-position", WK, "A simple symmetric random walk starts at 0. Find the probability that it is at {{kk}} after {{kn}} steps.", "combinations(kn, (kn + kk)/2)/2^kn", "pm_walk_prob(kn, kk, Rational(1, 2))",
    "The walk needs (n + k)/2 steps up out of n; count the orderings and divide by 2ⁿ", tex="P",
    cases=[{"kn": 4, "kk": 2}, {"kn": 4, "kk": 0}, {"kn": 6, "kk": 2}, {"kn": 5, "kk": 1}, {"kn": 6, "kk": 4}, {"kn": 8, "kk": 2}])),
 ("STO-2.2.A", N("sto-walk-position-biased", WK, "A random walk steps +1 with probability {{kp}} and −1 otherwise. Find the probability that it is at {{kk}} after {{kn}} steps.", "combinations(kn, (kn + kk)/2)*kp^((kn + kk)/2)*(1 - kp)^((kn - kk)/2)", "pm_walk_prob(kn, kk, kp)",
    "Count the paths with the right number of up-steps and multiply by the probability of any one of them", tex="P",
    cases=[{"kn": 3, "kk": 1, "kp": 0.6}, {"kn": 4, "kk": 2, "kp": 0.7}, {"kn": 4, "kk": 0, "kp": 0.6}, {"kn": 5, "kk": 3, "kp": 0.5}, {"kn": 3, "kk": -1, "kp": 0.25}])),
 ("STO-2.2.B", N("sto-walk-mean", WK, "A random walk steps +1 with probability {{kp}} and −1 otherwise. Find its expected position after {{kn}} steps.", "kn*(2*kp - 1)", "kn*(nsimplify(kp)*1 + (1 - nsimplify(kp))*(-1))",
    "Each step has mean p − q = 2p − 1, and expectations add", tex="E[S_n]",
    given={"kp": {"pick": [0.6, 0.7, 0.55, 0.9]}, "kn": {"pick": [10, 50, 100]}})),
 ("STO-2.2.B", N("sto-walk-sd", WK, "A simple symmetric random walk takes {{kn}} steps. Find the standard deviation of its final position.", "sqrt(kn)", "sqrt(kn*(Rational(1, 2)*1 + Rational(1, 2)*1 - 0))",
    "Each step has variance 1 and the steps are independent, so the variance is n and the typical distance from the start is √n", tex="\\sigma",
    given={"kn": {"pick": [16, 100, 400, 2500]}})),
 ("STO-2.2.C", N("sto-return-at-2n", WK, "Find the probability that a simple symmetric random walk is back at its starting point after {{km}} steps.", "combinations(km, km/2)/2^km", "pm_walk_prob(km, 0, Rational(1, 2))",
    "It must take exactly half its steps up: C(2n, n)/4ⁿ", tex="P",
    given={"km": {"pick": [2, 4, 6, 8, 10]}})),
 ("STO-2.2.C", N("sto-first-return", WK, "Find the probability that a simple symmetric random walk returns to its starting point for the first time at step {{km}}.", "combinations(km, km/2)/((km - 1)*2^km)", "pm_walk_first_return(km/2)",
    "First-return probability at step 2n is the return probability divided by 2n − 1", tex="P",
    given={"km": {"pick": [2, 4, 6, 8]}})),
 ("STO-3.2.A", Q("sto-is-invariant", LR, "A chain has transition matrix with rows {{sh}}. Is ({{pi}}) an invariant distribution?", pace="recall",
    cases=[{"sh": show(r), "pi": ", ".join(str(x) for x in v), "kc": 0 if [sp.Rational(x) for x in v] == stat(r) else 1} for r, v in [
        (R2[0], ("5/6", "1/6")), (R2[0], ("1/2", "1/2")), (R2[1], ("2/3", "1/3")), (R2[2], ("1/3", "2/3")), (R2[2], ("2/3", "1/3")), (R3[2], ("1/3", "1/3", "1/3")), (R3[0], ("1/3", "1/3", "1/3")), (R3[0], ("1/4", "1/2", "1/4"))]],
    choice=["Yes", "No"], correct="kc", verify="authored",
    explain="Multiply the row vector by the matrix and see whether you get it back. For two states it is enough to check that the flow from 0 to 1 equals the flow from 1 to 0")),
 ("STO-3.2.A", N("sto-balance-two", LR, "A two-state chain leaves state 0 with probability {{ka}} per step and leaves state 1 with probability {{kb}} per step. In equilibrium, what is the ratio π₀/π₁?", "kb/ka", "solve(Eq(Symbol('m')*nsimplify(ka), nsimplify(kb)), Symbol('m'))[0]",
    "Balance the flows: π₀ a = π₁ b. The chain spends longer in the state that is harder to leave", tex="\\pi_0/\\pi_1",
    cases=[{"ka": 0.1, "kb": 0.5}, {"ka": 0.2, "kb": 0.4}, {"ka": 0.5, "kb": 0.25}, {"ka": 0.3, "kb": 0.1}, {"ka": 0.05, "kb": 0.2}])),
 ("STO-3.2.B", N("sto-doubly-stochastic", LR, "A chain on {{kn}} states has a symmetric transition matrix. What is the long-run probability of each state?", "1/kn", "pm_mc_stationary(rws, 0)",
    "A symmetric matrix has columns summing to 1 as well as rows, so the uniform distribution is invariant", tex="\\pi_i",
    cases=[{"kn": 3, "rws": "0,1/2,1/2;1/2,0,1/2;1/2,1/2,0"}, {"kn": 3, "rws": "1/2,1/4,1/4;1/4,1/2,1/4;1/4,1/4,1/2"}, {"kn": 4, "rws": "0,1/2,0,1/2;1/2,0,1/2,0;0,1/2,0,1/2;1/2,0,1/2,0"}, {"kn": 2, "rws": "1/3,2/3;2/3,1/3"}])),
 ("STO-3.2.B", F("sto-uniform-facts", LR, [
    ("A random walk on a regular graph (every vertex has the same degree) has invariant distribution:", "Uniform", "Proportional to the vertex labels", "Concentrated on one vertex", "None"),
    ("A transition matrix whose columns also sum to 1 is called:", "Doubly stochastic", "Symmetric", "Reversible", "Absorbing"),
    ("Shuffling a deck by a fixed random procedure that is equally likely to do any move and its reverse has as invariant distribution:", "All orderings equally likely", "The starting ordering", "Sorted orderings only", "None"),
    ("If π is uniform and invariant on n states, the mean return time to any state is:", "n", "1", "1/n", "n²")],
    "Uniform invariance needs column sums of 1, which symmetry or regularity gives for free")),
 ("STO-3.2.C", N("sto-long-run-reward", LR, "A machine is 'up' (state 0) or 'down' (state 1) with transition matrix rows {{sh}} per day. It earns {{ku}} dollars on an up day and costs {{kd}} dollars on a down day. Find the long-run average profit per day.", "kans", "pm_mc_reward(rows, rw)",
    "Weight each day's payoff by the long-run fraction of days spent in that state", tex="profit",
    cases=[{"rows": r, "sh": show(r), "ku": u, "kd": d, "rw": f"{u},{-d}", "kans": fl(stat(r)[0] * u - stat(r)[1] * d)} for r, u, d in zip(R2, (600, 300, 900, 400), (1200, 600, 300, 800))])),
 ("STO-3.2.C", F("sto-ergodic-facts", LR, [
    ("The ergodic theorem for an irreducible positive-recurrent chain says time averages converge to:", "Averages against the invariant distribution", "The starting value", "Zero", "The maximum value"),
    ("The long-run fraction of time a chain spends in state i is:", "π_i", "1/π_i", "p(i, i)", "1/n"),
    ("The long-run average does not depend on the starting state because the chain is:", "Irreducible", "Periodic", "Reducible", "Deterministic"),
    ("In a molecular simulation, averaging an observable along a long trajectory estimates its:", "Equilibrium ensemble average", "Initial value", "Maximum", "Time derivative")],
    "This is the reason a single long run of a simulation can stand in for an average over the whole ensemble")),
 ("STO-4.2.A", N("sto-exponential-tail", PO, "A component's lifetime is exponential with mean {{km}} hours. Find the probability that it lasts more than {{kt}} hours.", "exp(-kt/km)", "1 - integrate(exp(-Y/km)/km, (Y, 0, kt))",
    "The rate is 1/mean, and the survival probability is e^(−t/mean)", tex="P",
    given={"km": {"pick": [10, 50, 100]}, "kt": {"pick": [5, 20, 100]}})),
 ("STO-4.2.A", N("sto-memoryless", PO, "A component's lifetime is exponential with mean {{km}} hours. It has already lasted {{ks}} hours. Find the probability that it lasts at least {{kt}} more.", "exp(-kt/km)", "exp(-Rational(ks + kt, km))/exp(-Rational(ks, km))",
    "Memoryless: the time already survived is irrelevant, so the answer is the same as for a new component", tex="P",
    given={"km": {"pick": [10, 50]}, "ks": {"pick": [20, 100]}, "kt": {"pick": [5, 10, 25]}})),
 ("STO-4.2.B", N("sto-first-of-n", PO, "{{kn}} independent components each fail at rate {{kl}} per year. Find the expected time in years until the first failure.", "1/(kn*kl)", "integrate(exp(-kn*nsimplify(kl)*Y), (Y, 0, oo))",
    "The minimum of n exponentials with rate λ is exponential with rate nλ, so its mean is 1/(nλ)", tex="E[T]",
    given={"kn": {"pick": [2, 5, 10]}, "kl": {"pick": [0.1, 0.5, 2]}})),
 ("STO-4.2.B", N("sto-all-of-n", PO, "{{kn}} independent components each fail at rate 1 per year. Find the expected time in years until all have failed.", "kans", "summation(1/nn, (nn, 1, kn))",
    "Wait for the first of n (mean 1/n), then by memorylessness the first of the remaining n − 1 (mean 1/(n − 1)), and so on: 1/n + 1/(n − 1) + … + 1", tex="E[T]",
    cases=[{"kn": 2, "kans": 1.5}, {"kn": 3, "kans": 1.83333333}, {"kn": 4, "kans": 2.08333333}, {"kn": 5, "kans": 2.28333333}])),
 ("STO-4.2.C", N("sto-mm1-idle", PO, "Customers arrive at a single server at rate {{kl}} per hour and are served at rate {{km}} per hour. What fraction of the time is the server idle?", "1 - kl/km", "(1 - Rational(kl, km))*Rational(kl, km)**0",
    "The equilibrium probability of an empty system is 1 − ρ with ρ = λ/μ", tex="\\pi_0",
    cases=[{"kl": 2, "km": 3}, {"kl": 3, "km": 4}, {"kl": 4, "km": 5}, {"kl": 9, "km": 10}, {"kl": 1, "km": 2}])),
 ("STO-4.2.C", N("sto-mm1-time", PO, "Customers arrive at a single server at rate {{kl}} per hour and are served at rate {{km}} per hour. Find the mean time in hours a customer spends in the system.", "1/(km - kl)", "summation(nn*(1 - Rational(kl, km))*Rational(kl, km)**nn, (nn, 1, oo))/kl",
    "Little's formula: mean number in system L = λW, and L = ρ/(1 − ρ), so W = 1/(μ − λ)", tex="W",
    cases=[{"kl": 2, "km": 3}, {"kl": 3, "km": 4}, {"kl": 4, "km": 5}, {"kl": 9, "km": 10}, {"kl": 5, "km": 8}])),
]
NEEDS = {
 "STO-1.2.A": ["SS-2.1.A"], "STO-1.2.B": ["STO-1.2.A"], "STO-1.2.C": ["STO-1.2.B", "LA-2.2.A"], "STO-1.1.A": ["STO-1.2.C"], "STO-1.2.D": ["STO-1.2.A"], "STO-1.1.B": ["STO-1.2.D"],
 "STO-2.2.A": ["STO-1.2.B"], "STO-2.2.B": ["STO-2.2.A"], "STO-2.2.C": ["STO-2.2.A"], "STO-2.1.A": ["STO-2.2.A", "STO-1.1.C"], "STO-2.1.B": ["STO-2.2.C"],
 "STO-3.2.A": ["STO-1.2.C"], "STO-3.1.A": ["STO-3.2.A"], "STO-3.2.B": ["STO-3.2.A"], "STO-3.1.C": ["STO-3.2.B"], "STO-3.2.C": ["STO-3.1.A"], "STO-3.1.B": ["STO-3.2.C"],
 "STO-4.2.A": ["SS-6.3.B"], "STO-4.2.B": ["STO-4.2.A"], "STO-4.1.A": ["STO-4.2.A"], "STO-4.1.B": ["STO-4.2.B"], "STO-4.2.C": ["STO-4.1.C"],
}
