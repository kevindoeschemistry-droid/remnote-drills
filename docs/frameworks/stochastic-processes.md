# Stochastic Processes — curriculum framework (draft 1)

Generated from `drills/frameworks/stochastic-processes.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**29 learning objectives** in 5 units (25 core): 29 drilled, 0 partly, 0 with no drills. Core: 25 / 25 drilled.

## Big ideas

- **STEP · Condition on the first step.** Hitting probabilities, expected times and invariant distributions all come from one move of the chain and a set of linear equations.
- **EQ · Equilibrium is a balance of flows.** A distribution is invariant when probability flowing into each state equals what flows out; detailed balance is the special case where it balances pair by pair.

## Practices

- **P1 · Compute.** Carry the definition or theorem to a number, a count or an example.
- **P2 · Decide.** Say whether a statement holds, which hypothesis fails, or which example breaks it.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Markov chains | core | — | 7 | 7 | 0 | 0 |
| 2 · Random walks | core | — | 5 | 5 | 0 | 0 |
| 3 · Long-run behaviour | core | — | 7 | 7 | 0 | 0 |
| 4 · Poisson processes and queues | core | — | 6 | 6 | 0 | 0 |
| 5 · Martingales and Brownian motion | extension | — | 4 | 4 | 0 | 0 |

## Unit 1 · Markov chains

Big ideas: STEP

### 1.1 Transition matrices and hitting



- ● **STO-1.1.A** (cambridge-ib-markov-chains:M1) Compute n-step transition probabilities and push a distribution forward one step.
  - EK: The n-step probabilities are the entries of Pⁿ (Chapman-Kolmogorov), and a row vector of probabilities evolves by μ ↦ μP.
  - Needs: LA-2.2.A, SS-2.1.A, STO-1.2.C
  - P1 · drills: sto-two-step, sto-push-forward
- ● **STO-1.1.B** (cambridge-ib-markov-chains:M1) Find the communicating classes of a chain, say which are closed, and find the period of a state.
  - EK: States communicate when each can reach the other. A class is closed if the chain cannot leave it; a chain with one class is irreducible. The period of a state is the gcd of its possible return times.
  - Needs: STO-1.1.A, STO-1.2.D
  - P1 · drills: sto-class-count, sto-period
- ● **STO-1.1.C** (cambridge-ib-markov-chains:M1) Find an absorption probability and a mean hitting time by first-step analysis.
  - EK: h(i), the probability of hitting A from i, satisfies h = 1 on A and h(i) = Σ p(i, j) h(j) elsewhere. k(i), the mean time to hit A, satisfies k = 0 on A and k(i) = 1 + Σ p(i, j) k(j).
  - Needs: STO-1.1.B
  - P1 · drills: sto-absorption, sto-hitting-time

### 1.2 Reading a chain



- ● **STO-1.2.A** (cambridge-ib-markov-chains:M1) Read and complete a transition matrix.
  - EK: Entry (i, j) is the probability of moving from state i to state j in one step. Every row is a probability distribution, so each row sums to 1; columns need not.
  - Needs: SS-2.1.A
  - P1 · drills: sto-missing-entry, sto-matrix-reading
- ● **STO-1.2.D** (cambridge-ib-markov-chains:M1, cambridge-ib-markov-chains:M2) Classify a state as absorbing, transient or recurrent from the diagram.
  - EK: A state is absorbing if the chain can never leave it. In a finite chain a state is recurrent if it lies in a closed class and transient if the chain can leave its class for good.
  - Needs: STO-1.2.A
  - P1 · drills: sto-classify-state, sto-class-facts
- ● **STO-1.2.B** (cambridge-ib-markov-chains:M1) Find the probability of a particular path.
  - EK: By the Markov property the probability of a path is the product of its one-step transition probabilities: the future depends on the past only through the present state.
  - Needs: STO-1.2.A
  - P1 · drills: sto-path-probability, sto-two-step-route
- ● **STO-1.2.C** (cambridge-ib-markov-chains:M1) Evolve a starting distribution for one or two steps.
  - EK: If the chain starts with distribution μ (a row vector), after n steps its distribution is μPⁿ: multiply on the left, one step at a time.
  - Needs: STO-1.2.B, LA-2.2.A
  - P1 · drills: sto-distribution-step, sto-distribution-two-steps

## Unit 2 · Random walks

Big ideas: STEP

### 2.1 Ruin, recurrence and transience



- ● **STO-2.1.A** (cambridge-ib-markov-chains:M1) Solve the gambler's ruin problem for the chance of winning and the expected duration.
  - EK: On 0…N with up-probability p and q = 1 − p: from i the chance of reaching N first is i/N if p = 1/2 and (1 − (q/p)^i)/(1 − (q/p)^N) otherwise. The fair game lasts i(N − i) steps on average.
  - Needs: STO-1.1.C, STO-2.2.A
  - P1 · drills: sto-ruin-biased, sto-ruin-duration
- ● **STO-2.1.B** (cambridge-ib-markov-chains:M2) Say whether a random walk is recurrent or transient and find a biased walk's return probability.
  - EK: A state is recurrent if return is certain, equivalently if Σ pⁿ(i, i) diverges. The simple symmetric walk is recurrent in one and two dimensions and transient in three (Pólya). On the integers with p ≠ 1/2 the return probability is 1 − |p − q|.
  - Needs: STO-2.1.A, STO-2.2.C
  - P2 · drills: sto-return-probability, sto-recurrence-facts

### 2.2 Walks by counting paths



- ● **STO-2.2.A** (cambridge-ib-markov-chains:M2) Find the distribution of a simple random walk after n steps by counting paths.
  - EK: A walk of n steps ends at k when it takes (n + k)/2 steps up, so P(S_n = k) = C(n, (n + k)/2) p^((n+k)/2) q^((n−k)/2), and zero unless n and k have the same parity.
  - Needs: STO-1.2.B
  - P1 · drills: sto-walk-position, sto-walk-position-biased
- ● **STO-2.2.B** (cambridge-ib-markov-chains:M2) Find the mean and variance of a random walk's position.
  - EK: Each step has mean p − q and variance 4pq, and steps are independent, so S_n has mean n(p − q) and variance 4npq. A symmetric walk is typically about √n from its start.
  - Needs: STO-2.2.A
  - P1 · drills: sto-walk-mean, sto-walk-sd
- ● **STO-2.2.C** (cambridge-ib-markov-chains:M2) Compute return probabilities of the symmetric walk.
  - EK: The walk is at 0 after 2n steps with probability C(2n, n)/4ⁿ, about 1/√(πn). It first returns at step 2n with probability C(2n, n)/((2n − 1)4ⁿ).
  - Needs: STO-2.2.A
  - P1 · drills: sto-return-at-2n, sto-first-return

## Unit 3 · Long-run behaviour

Big ideas: EQ

### 3.1 Invariant distributions and reversibility



- ● **STO-3.1.A** (cambridge-ib-markov-chains:M3) Find the invariant distribution of a small chain.
  - EK: π is invariant when πP = π with entries summing to 1. For two states with p(0, 1) = a and p(1, 0) = b, π = (b, a)/(a + b).
  - Needs: STO-1.1.B, LA-5.1.A, STO-3.2.A
  - P1 · drills: sto-stationary-two, sto-stationary-three
- ● **STO-3.1.B** (cambridge-ib-markov-chains:M3) Relate the invariant distribution to mean return times and long-run proportions.
  - EK: In an irreducible positive-recurrent chain the mean return time to i is 1/π_i, and the long-run proportion of time spent in i is π_i whatever the start.
  - Needs: STO-3.1.A, STO-1.1.C, STO-3.2.C
  - P1 · drills: sto-return-time, sto-long-run-count
- ● **STO-3.1.C** (cambridge-ib-markov-chains:M4) Use detailed balance, including for a random walk on a graph.
  - EK: If π_i p(i, j) = π_j p(j, i) for all pairs then π is invariant and the chain is reversible. A random walk on a graph has π_v = deg(v)/(2E).
  - Needs: STO-3.1.A, STO-3.2.B
  - P1 · drills: sto-graph-walk, sto-detailed-balance-facts
- ● **STO-3.1.D** (cambridge-ib-markov-chains:M3) Say when a chain converges to equilibrium and how fast.
  - EK: An irreducible aperiodic positive-recurrent chain has pⁿ(i, j) → π_j. For two states, pⁿ(0, 0) − π₀ = π₁ λⁿ with λ = 1 − a − b, the second eigenvalue.
  - Needs: STO-3.1.B
  - P1 · drills: sto-second-eigenvalue, sto-convergence-facts

### 3.2 Equilibrium by balance



- ● **STO-3.2.A** (cambridge-ib-markov-chains:M3) Check whether a given distribution is invariant.
  - EK: π is invariant when πP = π: for each state, the probability flowing in over one step equals the probability already there.
  - Needs: STO-1.2.C
  - P1 · drills: sto-is-invariant, sto-balance-two
- ● **STO-3.2.B** (cambridge-ib-markov-chains:M3) Use symmetry to find an invariant distribution without solving.
  - EK: If the columns of P also sum to 1 (a doubly stochastic matrix), the uniform distribution is invariant. A symmetric transition matrix is doubly stochastic.
  - Needs: STO-3.2.A
  - P1 · drills: sto-doubly-stochastic, sto-uniform-facts
- ● **STO-3.2.C** (cambridge-ib-markov-chains:M3) Compute a long-run average from the invariant distribution.
  - EK: For an irreducible positive-recurrent chain the long-run average of f(X_n) is Σ π_i f(i), whatever the starting state (the ergodic theorem).
  - Needs: STO-3.1.A
  - P1 · drills: sto-long-run-reward, sto-ergodic-facts

## Unit 4 · Poisson processes and queues

Big ideas: EQ

### 4.1 Continuous time



- ● **STO-4.1.A** (cambridge-ii-applied-probability:P1) Compute probabilities and waiting times for a Poisson process.
  - EK: With rate λ, the number of arrivals in time t is Poisson with mean λt, the gaps are independent exponentials of mean 1/λ, and the kth arrival comes at mean time k/λ.
  - Needs: SS-6.3.A, STO-4.2.A
  - P1 · drills: sto-poisson-none, sto-poisson-count
- ● **STO-4.1.B** (cambridge-ii-applied-probability:P1) Combine and split Poisson processes.
  - EK: Independent Poisson processes of rates λ and μ superpose to rate λ + μ, and the next event is from the first with probability λ/(λ + μ). Keeping each event with probability p gives a Poisson process of rate pλ.
  - Needs: STO-4.1.A, STO-4.2.B
  - P1 · drills: sto-poisson-race, sto-poisson-thinning
- ● **STO-4.1.C** (cambridge-ii-applied-probability:P1, cambridge-ii-applied-probability:P3) Find the equilibrium of a birth-death chain and of the M/M/1 queue.
  - EK: Balance across each cut: π_n λ_n = π_(n+1) μ_(n+1). For M/M/1 with ρ = λ/μ < 1, π_n = (1 − ρ)ρⁿ and the mean number in the system is ρ/(1 − ρ).
  - Needs: STO-4.1.B, STO-3.1.C
  - P1 · drills: sto-mm1-mean, sto-birth-death

### 4.2 Exponential clocks



- ● **STO-4.2.A** (cambridge-ii-applied-probability:P1) Compute with the exponential distribution and its memoryless property.
  - EK: An exponential time with rate λ has P(T > t) = e^(−λt) and mean 1/λ. Memoryless: given T > s, the remaining time is again exponential with rate λ.
  - Needs: SS-6.3.B
  - P1 · drills: sto-exponential-tail, sto-memoryless
- ● **STO-4.2.B** (cambridge-ii-applied-probability:P1) Find the time until the first of several independent exponential events.
  - EK: The minimum of independent exponentials with rates λ₁, …, λ_n is exponential with rate λ₁ + … + λ_n. With n identical clocks of rate λ the first rings after mean time 1/(nλ).
  - Needs: STO-4.2.A
  - P1 · drills: sto-first-of-n, sto-all-of-n
- ● **STO-4.2.C** (cambridge-ii-applied-probability:P3) Find the idle probability and the mean time in an M/M/1 queue.
  - EK: With ρ = λ/μ < 1 the server is idle a fraction 1 − ρ of the time, and a customer spends on average 1/(μ − λ) in the system (Little's formula L = λW).
  - Needs: STO-4.1.C
  - P1 · drills: sto-mm1-idle, sto-mm1-time

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
