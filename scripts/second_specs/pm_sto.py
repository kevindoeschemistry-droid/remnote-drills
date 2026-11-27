"""Stochastic Processes (STO, Nov 2026): Markov chains, random walks, long-run behaviour, and the Poisson process with
simple queues. Structure in UNITS (written by scripts/pm_setup.py), two question types per objective.

Basis: the Cambridge Part IB Markov Chains schedule, with the first and third blocks of Part II Applied Probability
(both read through an extraction of the 2026-27 Schedules booklet). Answers here come from matrix formulas (powers,
the fundamental matrix, a null vector); tests/verify/pmcalc.py solves the first-step equations instead."""
import sympy as sp
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "sto-stochastic", "stochastic-processes", "P1"
FW = dict(id="stochastic-processes", title="Stochastic Processes", code="STO", domain="stoch", requires=["statistics", "linear-algebra"], level=4,
          primary="cambridge-ib-markov-chains", also=["cambridge-ii-applied-probability"],
          note="Anchored on the Cambridge Markov Chains schedule (read through an extraction), with the Poisson process and the M/M/1 queue from Applied Probability. Renewal theory, general continuous-time chains, martingales and Brownian motion are not built.",
          header=["Markov chains are what molecular simulation runs on: detailed balance, stationary distributions and mixing",
                  "are the same objects whether the states are residues or configurations. Molecular Simulation uses them;",
                  "this framework is where they are defined and computed on chains small enough to do by hand."])
SKILLS = [("chains", "Transition matrices, communicating classes, hitting probabilities and times", "Markov chains", []),
          ("walks", "Gambler's ruin, recurrence and transience of random walks", "Random walks", ["stoch.chains"]),
          ("longrun", "Invariant distributions, return times, detailed balance and convergence", "Long-run behaviour", ["stoch.chains"]),
          ("poisson", "The Poisson process, thinning and superposition, birth-death chains and the M/M/1 queue", "Poisson processes and queues", ["stoch.longrun"])]
IDEAS = [("STEP", "Condition on the first step", "Hitting probabilities, expected times and invariant distributions all come from one move of the chain and a set of linear equations."),
         ("EQ", "Equilibrium is a balance of flows", "A distribution is invariant when probability flowing into each state equals what flows out; detailed balance is the special case where it balances pair by pair.")]
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


def stat(rows, j):  # left null vector of P - I
    Pm = P(rows)
    v = (Pm.T - sp.eye(Pm.shape[0])).nullspace()[0]
    return v[j] / sum(v)


def absorb(rows, target, start):  # fundamental matrix
    Pm = P(rows)
    tr = [i for i in range(Pm.shape[0]) if Pm[i, i] != 1]
    Nf = (sp.eye(len(tr)) - Pm.extract(tr, tr)).inv()
    return (Nf * Pm.extract(tr, [target]))[tr.index(start), 0]


def hit(rows, target, start):
    Pm = P(rows)
    tr = [i for i in range(Pm.shape[0]) if i != target]
    Nf = (sp.eye(len(tr)) - Pm.extract(tr, tr)).inv()
    return sum(Nf[tr.index(start), k] for k in range(len(tr)))


def classes(rows):
    Pm = P(rows); n = Pm.shape[0]
    R = sp.eye(n) + Pm
    R = R ** n
    return len({frozenset(j for j in range(n) if R[i, j] != 0 and R[j, i] != 0) for i in range(n)})


TWO = ["9/10,1/10;1/2,1/2", "4/5,1/5;2/5,3/5", "1/2,1/2;1/4,3/4", "7/10,3/10;1/10,9/10", "2/3,1/3;1/6,5/6"]
THREE = ["1/2,1/2,0;1/4,1/2,1/4;0,1/2,1/2", "0,1,0;1/2,0,1/2;0,1,0", "1/2,1/4,1/4;1/3,1/3,1/3;0,1/2,1/2", "0,1/2,1/2;1/2,0,1/2;1/2,1/2,0"]
ABS = ["1,0,0,0;1/2,0,1/2,0;0,1/2,0,1/2;0,0,0,1", "1,0,0,0;1/3,1/3,1/3,0;0,1/4,1/4,1/2;0,0,0,1", "1,0,0,0;1/4,1/2,1/4,0;0,1/3,1/3,1/3;0,0,0,1"]
CLS = [("1/2,1/2,0;1/2,1/2,0;0,0,1", None), ("1,0,0;1/2,0,1/2;0,0,1", None), ("0,1,0;0,0,1;1,0,0", None), ("1/2,1/2,0,0;1/2,1/2,0,0;0,1/3,1/3,1/3;0,0,0,1", None),
       ("0,1,0,0;1,0,0,0;0,0,0,1;0,0,1,0", None)]
GRAPHS = [("a-b,b-c,c-a,c-d", "c"), ("a-b,b-c,c-a,c-d", "d"), ("a-b,b-c,c-d", "b"), ("a-b,a-c,a-d,b-c", "a"), ("a-b,b-c,c-d,d-a,a-c", "a"), ("a-b,a-c,a-d,a-e", "a")]


def gstat(edges, v):
    es = [e.split("-") for e in edges.split(",")]
    return sp.Rational(sum(v in e for e in es), 2 * len(es))


UNITS = {
 1: ("chains", "Markov chains", M("M1"), ["STEP"], {
   1: ("Transition matrices and hitting", [
     ("A", M("M1"), "Compute n-step transition probabilities and push a distribution forward one step.",
      "The n-step probabilities are the entries of Pⁿ (Chapman-Kolmogorov), and a row vector of probabilities evolves by μ ↦ μP.", "P1", [
       N("sto-two-step", CH, "A chain on states 0 and 1 has transition matrix with rows {{sh}}. Find the probability of being in state {{kj}} after {{kn}} steps, starting from state {{ks}}.", "kans", "pm_mc_nstep(rows, kn, ks, kj)",
         "Sum over the intermediate states: for two steps, p(i, 0)p(0, j) + p(i, 1)p(1, j). That is the (i, j) entry of the matrix power", tex="p",
         cases=[{"rows": r, "sh": show(r), "ks": s, "kj": j, "kn": n, "kans": fl((P(r) ** n)[s, j])} for r, s, j, n in [
             (TWO[0], 1, 1, 2), (TWO[1], 1, 1, 2), (TWO[2], 1, 1, 2), (TWO[3], 1, 1, 3), (TWO[4], 1, 1, 2), (TWO[0], 1, 1, 3)]]),
       N("sto-push-forward", CH, "A chain has transition matrix with rows {{sh}}. It starts in state 0 with probability {{ka}} and in state 1 otherwise. Find the probability it is in state 1 after one step.", "ka*kp + (1 - ka)*kq", "ka*pm_mc_nstep(rows, 1, 0, 1) + (1 - ka)*pm_mc_nstep(rows, 1, 1, 1)",
         "Multiply the row vector of starting probabilities by the matrix: each start state contributes its probability times its chance of moving to 1", tex="p",
         cases=[{"rows": r, "sh": show(r), "ka": a, "kp": fl(P(r)[0, 1]), "kq": fl(P(r)[1, 1])} for r, a in [(TWO[0], 0.5), (TWO[1], 0.25), (TWO[2], 0.8), (TWO[3], 0.4), (TWO[4], 0.1)]])]),
     ("B", M("M1"), "Find the communicating classes of a chain, say which are closed, and find the period of a state.",
      "States communicate when each can reach the other. A class is closed if the chain cannot leave it; a chain with one class is irreducible. The period of a state is the gcd of its possible return times.", "P1", [
       N("sto-class-count", CH, "A chain has transition matrix with rows {{sh}}. How many communicating classes does it have?", "kans", "pm_mc_classes(rows)", final=True,
         explain="Draw an arrow for each non-zero entry and group the states that can reach each other in both directions", tex="classes",
         cases=[{"rows": r, "sh": show(r), "kans": classes(r)} for r, _ in CLS]),
       N("sto-period", CH, "{{ds}} What is the period of state 0?", "kans", "pm_mc_period(rows, 0)", final=True,
         explain="List the step counts at which a return to the state is possible and take their greatest common divisor", tex="period",
         cases=[{"ds": "A walk on a cycle of 4 states moves to either neighbour with probability 1/2.", "rows": "0,1/2,0,1/2;1/2,0,1/2,0;0,1/2,0,1/2;1/2,0,1/2,0", "kans": 2},
                {"ds": "A chain cycles deterministically 0 → 1 → 2 → 0.", "rows": "0,1,0;0,0,1;1,0,0", "kans": 3},
                {"ds": "A walk on a triangle moves to either other vertex with probability 1/2.", "rows": "0,1/2,1/2;1/2,0,1/2;1/2,1/2,0", "kans": 1},
                {"ds": "A walk on a cycle of 4 states moves to either neighbour with probability 1/4 each and stays put with probability 1/2.", "rows": "1/2,1/4,0,1/4;1/4,1/2,1/4,0;0,1/4,1/2,1/4;1/4,0,1/4,1/2", "kans": 1},
                {"ds": "A walk on a cycle of 6 states moves to either neighbour with probability 1/2.", "rows": "0,1/2,0,0,0,1/2;1/2,0,1/2,0,0,0;0,1/2,0,1/2,0,0;0,0,1/2,0,1/2,0;0,0,0,1/2,0,1/2;1/2,0,0,0,1/2,0", "kans": 2}])]),
     ("C", M("M1"), "Find an absorption probability and a mean hitting time by first-step analysis.",
      "h(i), the probability of hitting A from i, satisfies h = 1 on A and h(i) = Σ p(i, j) h(j) elsewhere. k(i), the mean time to hit A, satisfies k = 0 on A and k(i) = 1 + Σ p(i, j) k(j).", "P1", [
       N("sto-absorption", CH, "A chain on states 0, 1, 2, 3 has transition matrix with rows {{sh}}; states 0 and 3 are absorbing. Starting from state {{ks}}, find the probability of being absorbed at 3.", "kans", "pm_mc_absorb(rows, 3, ks)",
         "Write h(1) and h(2) each as an average of the h values one step away, with h(0) = 0 and h(3) = 1, and solve the two equations", tex="h",
         cases=[{"rows": r, "sh": show(r), "ks": s, "kans": fl(absorb(r, 3, s))} for r in ABS for s in (1, 2)]),
       N("sto-hitting-time", CH, "A chain has transition matrix with rows {{sh}}. Find the expected number of steps to reach state {{kt}} starting from state {{ks}}.", "kans", "pm_mc_hit_time(rows, kt, ks)",
         "Set k(target) = 0 and k(i) = 1 + Σ p(i, j) k(j) for the other states, then solve", tex="k",
         cases=[{"rows": r, "sh": show(r), "kt": t, "ks": s, "kans": fl(hit(r, t, s))} for r, t, s in [
             (TWO[0], 1, 0), (TWO[1], 1, 0), (THREE[0], 2, 0), (THREE[1], 2, 0), (THREE[3], 2, 0), (THREE[0], 2, 1)]])])]),
 }),
 2: ("walks", "Random walks", M("M1", "M2"), ["STEP"], {
   1: ("Ruin, recurrence and transience", [
     ("A", M("M1"), "Solve the gambler's ruin problem for the chance of winning and the expected duration.",
      "On 0…N with up-probability p and q = 1 − p: from i the chance of reaching N first is i/N if p = 1/2 and (1 − (q/p)^i)/(1 − (q/p)^N) otherwise. The fair game lasts i(N − i) steps on average.", "P1", [
       N("sto-ruin-biased", WK, "A gambler with {{ki}} units bets 1 unit at a time, winning each bet with probability {{kp}}, and stops at 0 or {{kn}}. Find the probability of reaching {{kn}}.", "(1 - ((1 - kp)/kp)^ki)/(1 - ((1 - kp)/kp)^kn)", "pm_ruin_win(kp, ki, kn)",
         "With r = q/p the answer is (1 − r^i)/(1 − r^N). A small edge against you is ruinous over a long game", tex="P",
         cases=[{"ki": 2, "kn": 4, "kp": 0.4}, {"ki": 3, "kn": 6, "kp": 0.6}, {"ki": 5, "kn": 10, "kp": 0.45}, {"ki": 1, "kn": 5, "kp": 0.6}, {"ki": 4, "kn": 8, "kp": 0.25}]),
       N("sto-ruin-duration", WK, "In a fair game with unit bets, a gambler starts with {{ki}} units and stops at 0 or {{kn}}. Find the expected number of bets.", "ki*(kn - ki)", "pm_ruin_time(ki, kn)", final=True,
         explain="k(i) = 1 + (k(i − 1) + k(i + 1))/2 with k(0) = k(N) = 0 has the solution i(N − i)", tex="bets",
         cases=[{"ki": 2, "kn": 5}, {"ki": 3, "kn": 10}, {"ki": 5, "kn": 10}, {"ki": 1, "kn": 8}, {"ki": 4, "kn": 12}])]),
     ("B", M("M2"), "Say whether a random walk is recurrent or transient and find a biased walk's return probability.",
      "A state is recurrent if return is certain, equivalently if Σ pⁿ(i, i) diverges. The simple symmetric walk is recurrent in one and two dimensions and transient in three (Pólya). On the integers with p ≠ 1/2 the return probability is 1 − |p − q|.", "P2", [
       N("sto-return-probability", WK, "A walk on the integers steps +1 with probability {{kp}} and −1 otherwise. Find the probability that it ever returns to its starting point.", "2*min(kp, 1 - kp)", "1 - Abs(2*nsimplify(kp) - 1)",
         "The walk returns for certain after a step against the drift and with probability q/p (for p > q) after a step with it, giving 1 − |p − q| = 2 min(p, q)", tex="P",
         given={"kp": {"pick": [0.6, 0.7, 0.25, 0.9, 0.45]}}),
       F("sto-recurrence-facts", WK, [
           ("The simple symmetric random walk is recurrent in which dimensions?", "One and two only", "One only", "All dimensions", "One, two and three"),
           ("A state i is transient exactly when the sum over n of pⁿ(i, i) is:", "Finite", "Infinite", "Equal to 1", "Zero"),
           ("In a finite irreducible chain, every state is:", "Positive recurrent", "Transient", "Null recurrent", "Absorbing"),
           ("The simple symmetric walk on the integers returns to 0 with probability 1, and its expected return time is:", "Infinite", "2", "Finite but large", "1"),
           ("Recurrence and transience are class properties, meaning:", "All states in a communicating class share them", "They depend on the starting distribution", "They hold only for closed classes", "They change with time")],
         "The return probabilities of the symmetric walk decay like n^(−d/2), which is summable only for d ≥ 3. In one dimension return is certain but takes infinitely long on average: null recurrence")])]),
 }),
 3: ("longrun", "Long-run behaviour", M("M3", "M4"), ["EQ"], {
   1: ("Invariant distributions and reversibility", [
     ("A", M("M3"), "Find the invariant distribution of a small chain.",
      "π is invariant when πP = π with entries summing to 1. For two states with p(0, 1) = a and p(1, 0) = b, π = (b, a)/(a + b).", "P1", [
       N("sto-stationary-two", LR, "A chain on states 0 and 1 has transition matrix with rows {{sh}}. Find the long-run probability of state 0.", "kb/(ka + kb)", "pm_mc_stationary(rows, 0)",
         "Balance the flow between the two states: π₀ a = π₁ b, so π₀ = b/(a + b), where a and b are the two switching probabilities", tex="\\pi_0",
         cases=[{"rows": r, "sh": show(r), "ka": fl(P(r)[0, 1]), "kb": fl(P(r)[1, 0])} for r in TWO]),
       N("sto-stationary-three", LR, "A chain on states 0, 1, 2 has transition matrix with rows {{sh}}. Find the invariant probability of state {{kj}}.", "kans", "pm_mc_stationary(rows, kj)",
         "Solve πP = π together with π₀ + π₁ + π₂ = 1; one of the three balance equations is redundant", tex="\\pi",
         cases=[{"rows": r, "sh": show(r), "kj": j, "kans": fl(stat(r, j))} for r, j in [(THREE[0], 1), (THREE[0], 0), (THREE[1], 1), (THREE[2], 2), (THREE[2], 0), (THREE[3], 0)]])]),
     ("B", M("M3"), "Relate the invariant distribution to mean return times and long-run proportions.",
      "In an irreducible positive-recurrent chain the mean return time to i is 1/π_i, and the long-run proportion of time spent in i is π_i whatever the start.", "P1", [
       N("sto-return-time", LR, "A chain on states 0 and 1 has transition matrix with rows {{sh}}. Starting in state 1, find the expected number of steps until it is next in state 1.", "(ka + kb)/ka", "1/pm_mc_stationary(rows, 1)",
         "The mean return time is the reciprocal of the invariant probability: π₁ = a/(a + b)", tex="m_1",
         cases=[{"rows": r, "sh": show(r), "ka": fl(P(r)[0, 1]), "kb": fl(P(r)[1, 0])} for r in TWO]),
       N("sto-long-run-count", LR, "A machine is 'up' (state 0) or 'down' (state 1), with transition matrix rows {{sh}} per day. Over {{kd}} days, about how many days is it down?", "kd*ka/(ka + kb)", "kd*pm_mc_stationary(rows, 1)",
         "The long-run fraction of time in a state is its invariant probability, whatever the starting state", tex="days",
         cases=[{"rows": r, "sh": show(r), "ka": fl(P(r)[0, 1]), "kb": fl(P(r)[1, 0]), "kd": d} for r, d in zip(TWO, (360, 300, 600, 1000, 900))])]),
     ("C", M("M4"), "Use detailed balance, including for a random walk on a graph.",
      "If π_i p(i, j) = π_j p(j, i) for all pairs then π is invariant and the chain is reversible. A random walk on a graph has π_v = deg(v)/(2E).", "P1", [
       N("sto-graph-walk", LR, "A random walk on the graph with edges {{ge}} moves to a uniformly chosen neighbour at each step. Find the long-run probability of vertex {{gv}}.", "kans", "pm_graph_walk_stationary(ge, gv)",
         "Detailed balance holds with π proportional to degree, so π_v = deg(v)/(2 × number of edges)", tex="\\pi_v",
         cases=[{"ge": g, "gv": v, "kans": fl(gstat(g, v))} for g, v in GRAPHS]),
       F("sto-detailed-balance-facts", LR, [
           ("Detailed balance π_i p(i, j) = π_j p(j, i) for all i and j implies that π is:", "Invariant", "Uniform", "Unique", "Zero off the diagonal"),
           ("The Metropolis algorithm is built so that its target distribution satisfies:", "Detailed balance", "The strong Markov property", "Transience", "Periodicity"),
           ("A chain that cycles deterministically 0 → 1 → 2 → 0 has a uniform invariant distribution but is not reversible because:", "Flow goes one way round the cycle", "It has no invariant distribution", "It is not irreducible", "It is aperiodic"),
           ("A chain with a symmetric transition matrix on a finite state space has invariant distribution:", "Uniform", "Proportional to the diagonal", "Concentrated on one state", "None"),
           ("Run backwards in time at equilibrium, a reversible chain looks like:", "The same chain", "A deterministic chain", "A transient chain", "A chain with transposed, unnormalised matrix")],
         "Detailed balance is sufficient for invariance, not necessary: the three-cycle balances globally but not pair by pair")]),
     ("D", M("M3"), "Say when a chain converges to equilibrium and how fast.",
      "An irreducible aperiodic positive-recurrent chain has pⁿ(i, j) → π_j. For two states, pⁿ(0, 0) − π₀ = π₁ λⁿ with λ = 1 − a − b, the second eigenvalue.", "P1", [
       N("sto-second-eigenvalue", LR, "A chain on states 0 and 1 has transition matrix with rows {{sh}}. Find pⁿ(0, 0) − π₀ for n = {{kn}}, using π₁λⁿ with λ = 1 − a − b.", "ka/(ka + kb)*(1 - ka - kb)^kn", "pm_mc_nstep(rows, kn, 0, 0) - pm_mc_stationary(rows, 0)",
         "The gap to equilibrium shrinks by the factor λ = 1 − a − b each step: the closer the two rows of the matrix, the faster the chain forgets its start", tex="gap", tol=0.01,
         cases=[{"rows": r, "sh": show(r), "ka": fl(P(r)[0, 1]), "kb": fl(P(r)[1, 0]), "kn": n} for r, n in zip(TWO, (2, 3, 2, 4, 3))]),
       F("sto-convergence-facts", LR, [
           ("The chain that alternates 0 → 1 → 0 → … has invariant distribution (1/2, 1/2), but pⁿ(0, 0) does not converge because the chain is:", "Periodic", "Transient", "Reducible", "Null recurrent"),
           ("For pⁿ(i, j) → π_j from every start, a finite chain needs to be:", "Irreducible and aperiodic", "Irreducible only", "Reversible", "Symmetric"),
           ("An irreducible chain with at least one state that can stay put (p(i, i) > 0) is:", "Aperiodic", "Periodic with period 2", "Reducible", "Transient"),
           ("A chain with two closed communicating classes has:", "More than one invariant distribution", "No invariant distribution", "Exactly one invariant distribution", "Period 2"),
           ("The rate of convergence of a finite reversible chain is governed by:", "The second-largest eigenvalue modulus", "The largest eigenvalue", "The trace", "The determinant")],
         "Irreducibility gives uniqueness of π, aperiodicity gives convergence to it, and the spectral gap gives the speed")])]),
 }),
 4: ("poisson", "Poisson processes and queues", AP("P1", "P3"), ["EQ"], {
   1: ("Continuous time", [
     ("A", AP("P1"), "Compute probabilities and waiting times for a Poisson process.",
      "With rate λ, the number of arrivals in time t is Poisson with mean λt, the gaps are independent exponentials of mean 1/λ, and the kth arrival comes at mean time k/λ.", "P1", [
       N("sto-poisson-none", PO, "Events occur as a Poisson process at rate {{kl}} per hour. Find the probability of no events in {{kt}} hours.", "exp(-kl*kt)", "1 - integrate(kl*exp(-kl*Y), (Y, 0, nsimplify(kt)))",
         "No arrivals by time t means the first gap exceeds t, and an exponential gap survives with probability e^(−λt)", tex="P",
         given={"kl": {"pick": [2, 3, 4]}, "kt": {"pick": [0.25, 0.5, 1]}}),
       N("sto-poisson-count", PO, "Events occur as a Poisson process at rate {{kl}} per minute. Find the probability of exactly {{kk}} events in {{kt}} minutes.", "exp(-kl*kt)*(kl*kt)^kk/factorial(kk)", "diff(exp(kl*kt*(Y - 1)), Y, kk).subs(Y, 0)/factorial(kk)",
         "The count is Poisson with mean λt: e^(−λt)(λt)^k/k!", tex="P",
         given={"kl": {"pick": [1, 2, 3]}, "kt": {"pick": [1, 2]}, "kk": {"pick": [1, 2, 3]}})]),
     ("B", AP("P1"), "Combine and split Poisson processes.",
      "Independent Poisson processes of rates λ and μ superpose to rate λ + μ, and the next event is from the first with probability λ/(λ + μ). Keeping each event with probability p gives a Poisson process of rate pλ.", "P1", [
       N("sto-poisson-race", PO, "Two independent Poisson processes have rates {{kl}} and {{km}} per second. Find the probability that the next event comes from the first.", "kl/(kl + km)", "integrate(kl*exp(-kl*Y)*exp(-km*Y), (Y, 0, oo))",
         "The first process wins the race if its exponential clock rings first: integrate its density against the other's survival", tex="P",
         given={"kl": {"pick": [1, 2, 3, 5]}, "km": {"pick": [1, 4, 6]}}),
       N("sto-poisson-thinning", PO, "Particles arrive at a detector as a Poisson process at {{kl}} per second, and each is recorded independently with probability {{kp}}. Find the probability that none is recorded in {{kt}} seconds.", "exp(-kl*kp*kt)", "exp(-nsimplify(kp)*kl*kt)",
         "Thinning gives a Poisson process of rate pλ, so the recorded count in time t has mean pλt", tex="P",
         given={"kl": {"pick": [5, 10, 20]}, "kp": {"pick": [0.1, 0.2, 0.5]}, "kt": {"pick": [0.5, 1, 2]}})]),
     ("C", AP("P1", "P3"), "Find the equilibrium of a birth-death chain and of the M/M/1 queue.",
      "Balance across each cut: π_n λ_n = π_(n+1) μ_(n+1). For M/M/1 with ρ = λ/μ < 1, π_n = (1 − ρ)ρⁿ and the mean number in the system is ρ/(1 − ρ).", "P1", [
       N("sto-mm1-mean", PO, "Customers arrive at a single server at rate {{kl}} per hour and are served at rate {{km}} per hour (M/M/1). Find the mean number in the system at equilibrium.", "kl/(km - kl)", "summation(nn*(1 - Rational(kl, km))*Rational(kl, km)**nn, (nn, 1, oo))",
         "ρ = λ/μ and the mean of the geometric equilibrium distribution is ρ/(1 − ρ) = λ/(μ − λ), which blows up as the arrival rate approaches the service rate", tex="L",
         cases=[{"kl": 2, "km": 3}, {"kl": 3, "km": 4}, {"kl": 4, "km": 5}, {"kl": 9, "km": 10}, {"kl": 1, "km": 2}, {"kl": 5, "km": 8}]),
       N("sto-birth-death", PO, "A system has states 0, 1, 2. It moves up from 0 at rate {{u0}} and from 1 at rate {{u1}}, and down from 1 at rate {{d1}} and from 2 at rate {{d2}}. Find the equilibrium probability of state 2.", "(u0/d1)*(u1/d2)/(1 + u0/d1 + (u0/d1)*(u1/d2))", "pm_ctmc_stationary(rts, 2)",
         "Balance across each cut: π₁ = π₀ u₀/d₁ and π₂ = π₁ u₁/d₂, then normalise", tex="\\pi_2",
         cases=[{"u0": a, "u1": b, "d1": c, "d2": d, "rts": f"{a},{b};{c},{d}"} for a, b, c, d in [(2, 1, 1, 2), (1, 1, 2, 2), (3, 2, 1, 1), (2, 2, 3, 1), (1, 2, 1, 4)]])])]),
 }),
}
ADD = [(f"{FW['code']}-{n}.{tn}.{lo[0]}", qq) for n, u in UNITS.items() for tn, (tt, los) in u[4].items() for lo in los for qq in lo[5]]
