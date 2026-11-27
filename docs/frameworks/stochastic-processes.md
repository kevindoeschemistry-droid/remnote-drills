# Stochastic Processes — curriculum framework (draft 1)

Generated from `drills/frameworks/stochastic-processes.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**16 learning objectives** in 5 units (12 core): 16 drilled, 0 partly, 0 with no drills. Core: 12 / 12 drilled.

## Big ideas

- **STEP · Condition on the first step.** Hitting probabilities, expected times and invariant distributions all come from one move of the chain and a set of linear equations.
- **EQ · Equilibrium is a balance of flows.** A distribution is invariant when probability flowing into each state equals what flows out; detailed balance is the special case where it balances pair by pair.

## Practices

- **P1 · Compute.** Carry the definition or theorem to a number, a count or an example.
- **P2 · Decide.** Say whether a statement holds, which hypothesis fails, or which example breaks it.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Markov chains | core | — | 3 | 3 | 0 | 0 |
| 2 · Random walks | core | — | 2 | 2 | 0 | 0 |
| 3 · Long-run behaviour | core | — | 4 | 4 | 0 | 0 |
| 4 · Poisson processes and queues | core | — | 3 | 3 | 0 | 0 |
| 5 · Martingales and Brownian motion | extension | — | 4 | 4 | 0 | 0 |

## Unit 1 · Markov chains

Big ideas: STEP

### 1.1 Transition matrices and hitting



- ● **STO-1.1.A** (cambridge-ib-markov-chains:M1) Compute n-step transition probabilities and push a distribution forward one step.
  - EK: The n-step probabilities are the entries of Pⁿ (Chapman-Kolmogorov), and a row vector of probabilities evolves by μ ↦ μP.
  - Needs: LA-2.2.A, SS-2.1.A
  - P1 · drills: sto-two-step, sto-push-forward
- ● **STO-1.1.B** (cambridge-ib-markov-chains:M1) Find the communicating classes of a chain, say which are closed, and find the period of a state.
  - EK: States communicate when each can reach the other. A class is closed if the chain cannot leave it; a chain with one class is irreducible. The period of a state is the gcd of its possible return times.
  - Needs: STO-1.1.A
  - P1 · drills: sto-class-count, sto-period
- ● **STO-1.1.C** (cambridge-ib-markov-chains:M1) Find an absorption probability and a mean hitting time by first-step analysis.
  - EK: h(i), the probability of hitting A from i, satisfies h = 1 on A and h(i) = Σ p(i, j) h(j) elsewhere. k(i), the mean time to hit A, satisfies k = 0 on A and k(i) = 1 + Σ p(i, j) k(j).
  - Needs: STO-1.1.B
  - P1 · drills: sto-absorption, sto-hitting-time

## Unit 2 · Random walks

Big ideas: STEP

### 2.1 Ruin, recurrence and transience



- ● **STO-2.1.A** (cambridge-ib-markov-chains:M1) Solve the gambler's ruin problem for the chance of winning and the expected duration.
  - EK: On 0…N with up-probability p and q = 1 − p: from i the chance of reaching N first is i/N if p = 1/2 and (1 − (q/p)^i)/(1 − (q/p)^N) otherwise. The fair game lasts i(N − i) steps on average.
  - Needs: STO-1.1.C
  - P1 · drills: sto-ruin-biased, sto-ruin-duration
- ● **STO-2.1.B** (cambridge-ib-markov-chains:M2) Say whether a random walk is recurrent or transient and find a biased walk's return probability.
  - EK: A state is recurrent if return is certain, equivalently if Σ pⁿ(i, i) diverges. The simple symmetric walk is recurrent in one and two dimensions and transient in three (Pólya). On the integers with p ≠ 1/2 the return probability is 1 − |p − q|.
  - Needs: STO-2.1.A
  - P2 · drills: sto-return-probability, sto-recurrence-facts

## Unit 3 · Long-run behaviour

Big ideas: EQ

### 3.1 Invariant distributions and reversibility



- ● **STO-3.1.A** (cambridge-ib-markov-chains:M3) Find the invariant distribution of a small chain.
  - EK: π is invariant when πP = π with entries summing to 1. For two states with p(0, 1) = a and p(1, 0) = b, π = (b, a)/(a + b).
  - Needs: STO-1.1.B, LA-5.1.A
  - P1 · drills: sto-stationary-two, sto-stationary-three
- ● **STO-3.1.B** (cambridge-ib-markov-chains:M3) Relate the invariant distribution to mean return times and long-run proportions.
  - EK: In an irreducible positive-recurrent chain the mean return time to i is 1/π_i, and the long-run proportion of time spent in i is π_i whatever the start.
  - Needs: STO-3.1.A, STO-1.1.C
  - P1 · drills: sto-return-time, sto-long-run-count
- ● **STO-3.1.C** (cambridge-ib-markov-chains:M4) Use detailed balance, including for a random walk on a graph.
  - EK: If π_i p(i, j) = π_j p(j, i) for all pairs then π is invariant and the chain is reversible. A random walk on a graph has π_v = deg(v)/(2E).
  - Needs: STO-3.1.A
  - P1 · drills: sto-graph-walk, sto-detailed-balance-facts
- ● **STO-3.1.D** (cambridge-ib-markov-chains:M3) Say when a chain converges to equilibrium and how fast.
  - EK: An irreducible aperiodic positive-recurrent chain has pⁿ(i, j) → π_j. For two states, pⁿ(0, 0) − π₀ = π₁ λⁿ with λ = 1 − a − b, the second eigenvalue.
  - Needs: STO-3.1.B
  - P1 · drills: sto-second-eigenvalue, sto-convergence-facts

## Unit 4 · Poisson processes and queues

Big ideas: EQ

### 4.1 Continuous time



- ● **STO-4.1.A** (cambridge-ii-applied-probability:P1) Compute probabilities and waiting times for a Poisson process.
  - EK: With rate λ, the number of arrivals in time t is Poisson with mean λt, the gaps are independent exponentials of mean 1/λ, and the kth arrival comes at mean time k/λ.
  - Needs: SS-6.3.A
  - P1 · drills: sto-poisson-none, sto-poisson-count
- ● **STO-4.1.B** (cambridge-ii-applied-probability:P1) Combine and split Poisson processes.
  - EK: Independent Poisson processes of rates λ and μ superpose to rate λ + μ, and the next event is from the first with probability λ/(λ + μ). Keeping each event with probability p gives a Poisson process of rate pλ.
  - Needs: STO-4.1.A
  - P1 · drills: sto-poisson-race, sto-poisson-thinning
- ● **STO-4.1.C** (cambridge-ii-applied-probability:P1, cambridge-ii-applied-probability:P3) Find the equilibrium of a birth-death chain and of the M/M/1 queue.
  - EK: Balance across each cut: π_n λ_n = π_(n+1) μ_(n+1). For M/M/1 with ρ = λ/μ < 1, π_n = (1 − ρ)ρⁿ and the mean number in the system is ρ/(1 − ρ).
  - Needs: STO-4.1.B, STO-3.1.C
  - P1 · drills: sto-mm1-mean, sto-birth-death

## Unit 5 · Martingales and Brownian motion (extension)

Big ideas: STEP, EQ

### 5.1 Fair games in discrete and continuous time



- ● **STO-5.1.A** (cambridge-ii-stochastic-financial-models:MG) Compute a conditional expectation and decide whether a process is a martingale.
  - EK: M is a martingale when E[M_(n+1) | past] = M_n: a fair game. For a simple symmetric walk S_n, both S_n and S_n² − n are martingales; for a biased walk, (q/p)^S_n is.
  - Needs: STO-2.1.A
  - P1 · drills: sto-conditional-expectation, sto-is-martingale
- ● **STO-5.1.B** (cambridge-ii-stochastic-financial-models:MG) Use the optional stopping theorem to find exit probabilities and expected exit times.
  - EK: For a martingale and a bounded stopping time (or bounded increments and finite mean time), E[M_T] = M₀. Applied to S_n it gives P(hit b before −a) = a/(a + b); applied to S_n² − n it gives E[T] = ab.
  - Needs: STO-5.1.A
  - P1 · drills: sto-exit-probability, sto-exit-time
- ● **STO-5.1.C** (cambridge-ii-stochastic-financial-models:BM) Price a claim in the one-period binomial model by the risk-neutral probability.
  - EK: If the stock moves from S to uS or dS and the bank pays 1 + r, with d < 1 + r < u, the risk-neutral up-probability is q = (1 + r − d)/(u − d), and any claim costs its discounted q-expectation: the price of the portfolio that replicates it.
  - Needs: STO-5.1.A
  - P1 · drills: sto-risk-neutral-q, sto-binomial-call
- ● **STO-5.1.D** (cambridge-ii-stochastic-financial-models:BR) Compute variances, covariances and hitting probabilities for Brownian motion.
  - EK: B_t − B_s is normal with mean 0 and variance t − s, independent of the past, so Cov(B_s, B_t) = min(s, t). Reflection principle: P(max over [0, t] ≥ a) = 2 P(B_t ≥ a).
  - Needs: STO-5.1.B, SS-6.3.A
  - P1 · drills: sto-brownian-variance, sto-reflection
