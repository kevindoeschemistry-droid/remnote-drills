# Computer Science — curriculum framework (draft 1)

Generated from `drills/frameworks/computer-science.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**140 learning objectives** in 19 units (128 core): 0 drilled, 0 partly, 140 with no drills. Core: 0 / 128 drilled.

## Big ideas

- **ABS · Abstraction and layering.** Every system is a stack of interfaces — gates, ISA, OS, language, library, service. Working at one layer means trusting the contract of the one below and knowing when it leaks.
- **COST · Resources are finite and costs scale.** Time, space, bandwidth, energy and money grow with input size; asymptotic analysis and measurement say which design survives growth, and the bottleneck sets the whole.
- **REP · Representation decides what is cheap.** The same information as an array, a tree, a hash table, a relation, a bit pattern or a vector makes different operations fast, slow or impossible.
- **CORR · Correctness is argued, not hoped for.** Specifications, invariants, types, proofs and tests are how a program is shown to do what it should — including on the boundary inputs.
- **CONC · Concurrency and distribution change the rules.** Once work overlaps in time or space, ordering, shared state, partial failure and coordination dominate; single-threaded intuition breaks.
- **ADV · Assume an adversary.** Security means reasoning about an attacker who chooses the worst input, timing and path; trust boundaries and least privilege, not obscurity, contain them.
- **HUM · Computing serves people.** Systems are used, misused and governed by people; usability, accessibility, fairness, privacy and law are design constraints, not afterthoughts.

## Practices

- **P1 · Model the problem.** Turn a described task into a precise specification — inputs, outputs, constraints, the abstraction (graph, relation, automaton, state machine) it really is.
- **P2 · Analyse cost.** Derive time, space, I/O, latency or throughput — asymptotically or numerically — and identify the dominant term or bottleneck.
- **P3 · Trace execution.** Simulate a structure, algorithm, protocol or machine step by step and state its exact state after k steps.
- **P4 · Choose and design.** Select the structure, algorithm, schema, protocol or architecture that fits a described workload and justify the trade-off.
- **P5 · Implement.** Write the code, query, configuration or expression that realises the design.
- **P6 · Verify.** Prove, test, type-check or find the counterexample; check boundary cases and failure modes.
- **P7 · Evaluate impact.** Judge security, usability, ethical, legal and social consequences of a design choice.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Discrete and probabilistic foundations | core | — | 8 | 0 | 0 | 8 |
| 2 · Algorithm analysis | core | — | 8 | 0 | 0 | 8 |
| 3 · Data structures | core | — | 10 | 0 | 0 | 10 |
| 4 · Algorithm design and graph algorithms | core | — | 11 | 0 | 0 | 11 |
| 5 · Models of computation and complexity classes | core | — | 6 | 0 | 0 | 6 |
| 6 · Software engineering | core | — | 8 | 0 | 0 | 8 |
| 7 · Databases and data management | core | — | 13 | 0 | 0 | 13 |
| 8 · Computer architecture and systems performance | core | — | 9 | 0 | 0 | 9 |
| 9 · Operating systems and systems programming | core | — | 11 | 0 | 0 | 11 |
| 10 · Networking | core | — | 9 | 0 | 0 | 9 |
| 11 · Security | core | — | 9 | 0 | 0 | 9 |
| 12 · Programming languages | core | — | 7 | 0 | 0 | 7 |
| 13 · Artificial intelligence and machine learning | core | — | 7 | 0 | 0 | 7 |
| 14 · Parallel and distributed computing | core | — | 4 | 0 | 0 | 4 |
| 15 · Human–computer interaction | core | — | 4 | 0 | 0 | 4 |
| 16 · Society, ethics and the profession | core | — | 4 | 0 | 0 | 4 |
| 17 · Advanced algorithms | extension | — | 4 | 0 | 0 | 4 |
| 18 · Distributed systems and cloud | extension | — | 5 | 0 | 0 | 5 |
| 19 · Machine learning in depth | extension | — | 3 | 0 | 0 | 3 |

## Unit 1 · Discrete and probabilistic foundations

Big ideas: CORR, REP

### 1.1 Logic and proof

Book: cs2023 §MSF-Discrete

- ○ **CS-1.1.A** Decide whether two propositional formulas are equivalent, by truth table or by algebraic laws.
  - EK: Equivalent ⇔ same truth value on every assignment; p → q ≡ ¬p ∨ q; De Morgan swaps ∧ and ∨ under negation.
  - P3 · P6
- ○ **CS-1.1.B** Prove a claim about a recursive definition or a loop by induction, naming base case, hypothesis and step.
  - EK: Weak induction assumes P(k) to show P(k+1); strong induction assumes all P(j ≤ k); structural induction follows the recursive definition.
  - P6

### 1.2 Counting, sums and recurrences

Book: cs2023 §MSF-Discrete

- ○ **CS-1.2.A** Count arrangements or selections with the product rule, permutations, combinations and inclusion–exclusion, giving a number.
  - EK: Order matters ⇒ P(n,k) = n!/(n−k)!; order ignored ⇒ C(n,k); |A ∪ B| = |A| + |B| − |A ∩ B|.
  - P1 · P2
- ○ **CS-1.2.B** Evaluate a summation or simple linear recurrence in closed form (e.g. T(n) = T(n−1) + n).
  - EK: Σ i = n(n+1)/2; Σ 2^i = 2^(n+1) − 1; geometric series with ratio < 1 is bounded by its first term.
  - P2

### 1.3 Relations and graphs

Book: cs2023 §MSF-Discrete

- ○ **CS-1.3.A** Compute degrees, connectivity, and whether a small graph is bipartite, acyclic or a tree.
  - EK: Σ deg = 2|E|; a tree on n vertices has n − 1 edges; bipartite ⇔ no odd cycle.
  - P3

### 1.4 Probability and statistics for computing

Book: cs2023 §MSF-Probability, §MSF-Statistics

- ○ **CS-1.4.A** Compute an expected count (collisions, comparisons, hits) using linearity of expectation over indicator variables.
  - EK: E[ΣX_i] = ΣE[X_i] even when the X_i are dependent; E[indicator] = P(event).
  - P2
- ○ **CS-1.4.B** Apply Bayes' rule to a detector or classifier scenario and find the probability an alert is real.
  - EK: P(A|B) = P(B|A)P(A)/P(B); a low base rate makes most positives false even for an accurate test.
  - P2 · P7
- ○ **CS-1.4.C** Compute the mean, standard deviation and a confidence interval from repeated benchmark runs, and decide whether two configurations differ.
  - EK: CI ≈ x̄ ± t·s/√n; overlapping intervals do not prove no difference; report variance, not one run.
  - P2 · P6

## Unit 2 · Algorithm analysis

Big ideas: COST, CORR

### 2.1 Asymptotic notation

Book: cs2023 §AL-Foundational, §AL-Complexity

- ○ **CS-2.1.A** Rank a set of functions by growth rate (constant, log, polylog, polynomial, exponential, factorial).
  - EK: log n ≪ n^ε ≪ n^k ≪ c^n ≪ n!; bases of logs differ by a constant factor.
  - P2
- ○ **CS-2.1.B** Compute the Big-O of described or shown code — nested loops, dependent bounds, index doubling or halving — as an auto-checked answer.
  - EK: Nested independent loops multiply; i *= 2 runs log n times; Σ_{i=1..n} i = Θ(n²); sequential blocks add, the largest wins.
  - Needs: CS-1.2.B
  - P2

### 2.2 Recurrences and divide-and-conquer cost

Book: cs2023 §AL-Foundational, §AL-Strategies

- ○ **CS-2.2.A** Write the running-time recurrence of a recursive function from its code.
  - EK: T(n) = a·T(n/b) + f(n): a recursive calls on size n/b plus non-recursive work f(n).
  - P1 · P2
- ○ **CS-2.2.B** Solve a divide-and-conquer recurrence with the master theorem or a recursion tree, naming the case that applies.
  - EK: Compare f(n) with n^(log_b a): smaller ⇒ Θ(n^(log_b a)); equal ⇒ ×log n; larger (regular) ⇒ Θ(f(n)).
  - Needs: CS-2.2.A
  - P2

### 2.3 Cases and amortization

Book: cs2023 §AL-Foundational, §AL-Complexity

- ○ **CS-2.3.A** Identify the best-, worst- and average-case inputs of an algorithm and their costs (e.g. quicksort on sorted input).
  - EK: Worst case is a guarantee over all inputs of size n; average case needs an input distribution.
  - P2 · P6
- ○ **CS-2.3.B** Compute the amortized cost per operation of a sequence (dynamic-array doubling, binary counter) by the aggregate or accounting method.
  - EK: Doubling capacity costs n total copies over n appends ⇒ O(1) amortized; growing by a constant is O(n) amortized.
  - P2

### 2.4 Correctness arguments

Book: cs2023 §AL-Foundational, §SDF-Algorithms

- ○ **CS-2.4.A** State a loop invariant for an iterative algorithm and use initialization, maintenance and termination to prove it correct.
  - EK: An invariant holds before each iteration; at exit, invariant + negated loop condition ⇒ postcondition.
  - Needs: CS-1.1.B
  - P6
- ○ **CS-2.4.B** Find the boundary input on which a given binary-search or loop variant fails (off-by-one, infinite loop, overflow in mid).
  - EK: Check empty, one-element and target-at-ends inputs; lo + (hi − lo)/2 avoids overflow; the interval must shrink every step.
  - P3 · P6

## Unit 3 · Data structures

Big ideas: REP, COST

### 3.1 Sequences, stacks and queues

Book: cs2023 §SDF-Data-Structures, §AL-Foundational

- ○ **CS-3.1.A** State the cost of access, insert-at-front, append and delete for arrays, dynamic arrays, singly and doubly linked lists and deques.
  - EK: Arrays: O(1) index, O(n) front insert; linked lists: O(1) splice given the node, O(n) index; contiguous memory is cache-friendly.
  - P2

### 3.2 Hash tables

Book: cs2023 §AL-Foundational, §SDF-Data-Structures

- ○ **CS-3.2.A** Trace insertions into a hash table under chaining, linear probing or double hashing for a given hash function, giving the final table.
  - EK: Linear probing tries h, h+1, h+2 … mod m; deletion under open addressing needs tombstones.
  - P3
- ○ **CS-3.2.B** Compute the load factor and expected probes for a hash table and decide when it must resize.
  - EK: α = n/m; chaining: expected chain length α; linear probing degrades sharply above α ≈ 0.7.
  - Needs: CS-1.4.A
  - P2

### 3.3 Search trees

Book: cs2023 §AL-Foundational, §SDF-Data-Structures

- ○ **CS-3.3.A** Trace BST insertion and deletion and produce the in-, pre- and post-order traversals of the result.
  - EK: In-order of a BST is sorted; deleting a two-child node swaps in its successor; height ranges from log n to n.
  - P3
- ○ **CS-3.3.B** Trace the rotations an AVL or red-black tree performs after an insertion.
  - EK: AVL keeps |balance| ≤ 1 via single or double rotations; both guarantee O(log n) height.
  - Needs: CS-3.3.A
  - P3
- ○ **CS-3.3.C** Compute the height of a B-tree or B+-tree of order m holding n keys and explain why databases use it.
  - EK: Height ≈ log_m n; high fanout makes each level one disk page, so a lookup costs a few I/Os.
  - P2 · P4

### 3.4 Heaps and priority queues

Book: cs2023 §AL-Foundational, §SDF-Data-Structures

- ○ **CS-3.4.A** Trace a binary heap's array after insert, extract-min and bottom-up heapify.
  - EK: Children of i at 2i+1, 2i+2; sift-up/down are O(log n); bottom-up build is O(n).
  - P3

### 3.5 Graph representations and disjoint sets

Book: cs2023 §AL-Foundational

- ○ **CS-3.5.A** Choose an adjacency list or matrix for a graph's density and operations and give its space and edge-query cost.
  - EK: List: Θ(V + E) space, O(deg) edge test; matrix: Θ(V²) space, O(1) edge test; sparse graphs favour lists.
  - Needs: CS-1.3.A
  - P2 · P4
- ○ **CS-3.5.B** Trace union-find with union by rank and path compression and give the resulting parent array.
  - EK: Both heuristics together give O(α(n)) amortized per operation — effectively constant.
  - P3

### 3.6 Choosing a structure

Book: cs2023 §SDF-Data-Structures, §AL-Strategies

- ○ **CS-3.6.A** Pick the data structure for a described access pattern (LRU cache, top-k of a stream, prefix search, range queries, membership with false positives allowed) — auto-checked choice.
  - EK: LRU = hash map + doubly linked list; top-k = size-k min-heap; prefixes = trie; ranges = balanced BST/B-tree; approximate membership = Bloom filter.
  - Needs: CS-3.1.A, CS-3.2.A, CS-3.4.A
  - P4

## Unit 4 · Algorithm design and graph algorithms

Big ideas: COST, CORR, REP

### 4.1 Sorting

Book: cs2023 §AL-Foundational, §SDF-Algorithms

- ○ **CS-4.1.A** Trace the array after k passes of insertion, selection or bubble sort, a quicksort partition, or a merge step.
  - EK: Insertion sort keeps a sorted prefix; selection places the k-th smallest at pass k; Lomuto/Hoare partitions differ in pivot placement.
  - P3
- ○ **CS-4.1.B** Pick a sort for a scenario by worst-case time, stability, extra space and adaptivity, and explain when counting or radix sort beats Ω(n log n).
  - EK: Comparison sorts need Ω(n log n) comparisons; merge sort is stable, heapsort in-place, quicksort fast on average; radix sort is O(d(n + k)).
  - Needs: CS-2.3.A
  - P2 · P4

### 4.2 Greedy algorithms

Book: cs2023 §AL-Strategies

- ○ **CS-4.2.A** Apply a greedy rule (interval scheduling by earliest finish, Huffman coding) and give its output; for coin change with non-canonical coins, produce the counterexample.
  - EK: Greedy is correct only with the greedy-choice property and optimal substructure, shown by an exchange argument.
  - P3 · P6
- ○ **CS-4.2.B** Build a Huffman code for given symbol frequencies and compute the encoded length in bits.
  - EK: Repeatedly merge the two least-frequent nodes; total bits = Σ freq × depth.
  - P3 · P2

### 4.3 Dynamic programming

Book: cs2023 §AL-Strategies

- ○ **CS-4.3.A** Fill a DP table (LCS, edit distance, 0/1 knapsack, coin-change count) and read off the optimum and one optimal solution.
  - EK: Each cell is a subproblem combined from already-filled cells; traceback through choices recovers the solution.
  - P3
- ○ **CS-4.3.B** Write the state, recurrence and base cases for a described optimisation problem and give its time and space.
  - EK: Time ≈ (# states) × (work per state); overlapping subproblems + optimal substructure ⇒ DP.
  - P1 · P2

### 4.4 Graph traversal

Book: cs2023 §AL-Foundational

- ○ **CS-4.4.A** Trace BFS or DFS from a source (neighbours in given order) and give the visit order, BFS distances or DFS discovery/finish times.
  - EK: BFS finds fewest-edge paths using a queue; DFS uses a stack/recursion; both are O(V + E).
  - Needs: CS-3.5.A
  - P3
- ○ **CS-4.4.B** Produce a topological order of a DAG, or report the cycle that prevents one.
  - EK: Kahn: repeatedly remove in-degree-0 vertices; DFS: reverse finish order; a back edge means a cycle.
  - P3 · P6

### 4.5 Shortest paths and spanning trees

Book: cs2023 §AL-Foundational

- ○ **CS-4.5.A** Trace Dijkstra's distance array and settled set after k extractions.
  - EK: Greedily settle the closest unsettled vertex and relax its edges; O((V + E) log V) with a binary heap.
  - Needs: CS-3.4.A
  - P3
- ○ **CS-4.5.B** Run Bellman–Ford to find distances or detect a negative cycle, and explain why Dijkstra fails with negative edges.
  - EK: V − 1 rounds of relaxing every edge; an improvement in round V means a negative cycle.
  - P3 · P6
- ○ **CS-4.5.C** Compute an MST's weight with Kruskal or Prim and give the order in which edges are chosen.
  - EK: Cut property: the lightest edge crossing any cut is safe; Kruskal uses union-find.
  - Needs: CS-3.5.B
  - P3

## Unit 5 · Models of computation and complexity classes

Big ideas: CORR, COST

### 5.1 Automata and languages

Book: cs2023 §AL-Models

- ○ **CS-5.1.A** Trace a DFA or NFA on an input string and decide whether it accepts.
  - EK: A DFA has exactly one transition per symbol; an NFA accepts if any path does; every NFA has an equivalent DFA.
  - P3
- ○ **CS-5.1.B** Write a regular expression or DFA for a described language, or argue it is not regular.
  - EK: Regular languages cannot count unboundedly (e.g. aⁿbⁿ); pumping lemma gives the contradiction.
  - P1 · P5
- ○ **CS-5.1.C** Derive a string from a context-free grammar and show the grammar is ambiguous by giving two parse trees.
  - EK: CFGs capture nesting (balanced brackets) that regular expressions cannot; ambiguity = two leftmost derivations.
  - P3

### 5.2 Computability and NP-completeness

Book: cs2023 §AL-Models, §AL-Complexity

- ○ **CS-5.2.A** Show a described problem is undecidable by reducing the halting problem to it.
  - EK: If a decider for X would yield a decider for HALT, X is undecidable; Rice's theorem covers non-trivial semantic properties.
  - P6
- ○ **CS-5.2.B** Classify a described problem as in P, NP-complete, or undecidable, and verify a given certificate in polynomial time.
  - EK: NP = polynomially verifiable; NP-complete = in NP and every NP problem reduces to it; P = NP is open.
  - P4 · P6
- ○ **CS-5.2.C** State the direction of a polynomial reduction needed to prove a new problem NP-hard, and carry out a small one (3-SAT → independent set, vertex cover ↔ independent set).
  - EK: Reduce a known NP-hard problem TO the new one; S is a vertex cover ⇔ V∖S is an independent set.
  - Needs: CS-5.2.B
  - P6

## Unit 6 · Software engineering

Big ideas: CORR, ABS, HUM

### 6.1 Process and requirements

Book: cs2023 §SE-Teamwork, §SE-Requirements

- ○ **CS-6.1.A** Rewrite a vague requirement as a testable functional or non-functional requirement with an acceptance criterion.
  - EK: Testable = measurable outcome and condition ('p95 latency < 200 ms at 500 rps'); NFRs cover performance, security, usability, reliability.
  - P1 · P6

### 6.2 Design principles and patterns

Book: cs2023 §SE-Design, §FPL-OOP

- ○ **CS-6.2.A** Identify which SOLID principle a code snippet violates and the refactoring that fixes it.
  - EK: SRP one reason to change; OCP extend without editing; LSP subtypes substitutable; ISP small interfaces; DIP depend on abstractions.
  - P6
- ○ **CS-6.2.B** Name the design pattern a snippet implements or needs (strategy, observer, factory, adapter, decorator, singleton, repository).
  - EK: Patterns are named solutions to recurring forces: vary an algorithm ⇒ strategy; notify dependents ⇒ observer; wrap an incompatible API ⇒ adapter.
  - P4

### 6.3 Tools and construction

Book: cs2023 §SE-Tools, §SE-Construction

- ○ **CS-6.3.A** Predict the commit graph after a git merge, rebase, cherry-pick, revert or reset on a described history.
  - EK: Merge adds a two-parent commit; rebase replays commits with new hashes; revert adds an inverse commit; reset moves the branch pointer.
  - P3

### 6.4 Testing and validation

Book: cs2023 §SE-Validation

- ○ **CS-6.4.A** Design test inputs for a specification by equivalence partitioning and boundary-value analysis.
  - EK: One input per partition plus each boundary and its neighbours; invalid partitions need tests too.
  - P6
- ○ **CS-6.4.B** Compute statement and branch coverage of a test suite on a given snippet, and add the test that raises it.
  - EK: Branch coverage counts each decision outcome; 100% statement coverage can miss a false branch.
  - P2 · P6

### 6.5 Reliability and specification

Book: cs2023 §SE-Reliability, §SE-Formal, §SF-Reliability

- ○ **CS-6.5.A** Compute availability from MTBF and MTTR, and for components in series or redundant parallel; convert nines to downtime per year.
  - EK: A = MTBF/(MTBF + MTTR); series multiply A; parallel 1 − Π(1 − A_i); 99.9% ≈ 8.8 h/yr down.
  - P2
- ○ **CS-6.5.B** Write pre- and postconditions for a function and decide whether a given Hoare triple holds.
  - EK: {P} S {Q}: if P holds before S and S terminates, Q holds after; assignment rule substitutes backward.
  - Needs: CS-2.4.A
  - P6

## Unit 7 · Databases and data management

Big ideas: REP, CORR, CONC

### 7.1 Modelling and the relational model

Book: cs2023 §DM-Modeling, §DM-Relational

- ○ **CS-7.1.A** Build an ER model with cardinalities for a scenario and map it to relational tables with primary and foreign keys.
  - EK: 1:N ⇒ FK on the N side; M:N ⇒ junction table with composite key; weak entities borrow the owner's key.
  - P1 · P5
- ○ **CS-7.1.B** Evaluate a relational-algebra expression (σ, π, ⋈, ∪, −, ρ) on small tables and give the result.
  - EK: Selection filters rows, projection columns (removing duplicates); natural join matches equal-named attributes.
  - P3

### 7.2 SQL

Book: cs2023 §DM-Querying

- ○ **CS-7.2.A** Write a SQL query with joins, GROUP BY and HAVING for a described question — auto-checked by comparing result sets.
  - EK: WHERE filters rows before grouping, HAVING filters groups after; every non-aggregated SELECT column must be grouped.
  - Needs: CS-7.1.B
  - P5
- ○ **CS-7.2.B** Predict the result of an outer join, a comparison with NULL, or an aggregate over a column containing NULLs.
  - EK: NULL = NULL is unknown, not true; COUNT(*) counts rows, COUNT(col) skips NULLs; LEFT JOIN keeps unmatched left rows with NULLs.
  - P3
- ○ **CS-7.2.C** Write a query using a correlated subquery, CTE or window function (rank, running total, top-n per group).
  - EK: Window functions compute over a PARTITION BY … ORDER BY frame without collapsing rows.
  - Needs: CS-7.2.A
  - P5

### 7.3 Functional dependencies and normal forms

Book: cs2023 §DM-Relational, §DM-Modeling

- ○ **CS-7.3.A** Compute an attribute closure from a set of FDs and find all candidate keys.
  - EK: X⁺ = everything X determines by repeatedly applying FDs; X is a superkey iff X⁺ = all attributes.
  - P3
- ○ **CS-7.3.B** Determine the highest normal form (1NF–BCNF) a relation satisfies under given FDs.
  - EK: 2NF: no partial dependency on a key; 3NF: every non-trivial FD has a superkey LHS or prime RHS; BCNF: superkey LHS always.
  - Needs: CS-7.3.A
  - P6
- ○ **CS-7.3.C** Decompose a relation into BCNF or 3NF and check the decomposition is lossless and dependency-preserving.
  - EK: Binary split R1, R2 is lossless iff R1 ∩ R2 → R1 or → R2; 3NF synthesis always preserves dependencies, BCNF may not.
  - Needs: CS-7.3.B
  - P5 · P6

### 7.4 Transactions and concurrency control

Book: cs2023 §DM-Processing, §DM-Internals

- ○ **CS-7.4.A** Name the anomaly (dirty read, non-repeatable read, phantom, lost update, write skew) in a described interleaving and the weakest isolation level that prevents it.
  - EK: READ COMMITTED stops dirty reads; REPEATABLE READ stops non-repeatable reads; SERIALIZABLE stops phantoms and write skew.
  - P3 · P6
- ○ **CS-7.4.B** Decide whether a schedule is conflict-serializable by drawing its precedence graph, and give an equivalent serial order.
  - EK: Conflicts: two ops on the same item, different transactions, at least one write; acyclic precedence graph ⇔ conflict-serializable.
  - Needs: CS-4.4.B
  - P3 · P6

### 7.5 Storage, indexing and query processing

Book: cs2023 §DM-Internals, §DM-Processing

- ○ **CS-7.5.A** Estimate the page I/Os of a lookup or range query with no index, a B+-tree index and a hash index, and pick the index for a workload.
  - EK: Scan = all pages; B+-tree = height + matching leaf pages (+ row fetches if unclustered); hash = ~1–2 I/Os for equality only.
  - Needs: CS-3.3.C
  - P2 · P4

### 7.6 NoSQL and distributed data

Book: cs2023 §DM-NoSQL, §DM-Distributed

- ○ **CS-7.6.A** Choose a data model (relational, document, key-value, wide-column, graph) for a described access pattern and consistency need.
  - EK: Model data around queries in NoSQL; joins and multi-row transactions favour relational; deep traversals favour graph.
  - P4
- ○ **CS-7.6.B** Apply CAP and PACELC to say what a described system gives up during a network partition and in normal operation.
  - EK: During a partition choose consistency or availability; else trade latency against consistency.
  - P4 · P6

## Unit 8 · Computer architecture and systems performance

Big ideas: REP, COST, ABS

### 8.1 Data representation

Book: cs2023 §AR-Representation

- ○ **CS-8.1.A** Convert integers between binary, hex and decimal, including n-bit two's complement, and detect overflow.
  - EK: Two's complement range −2^(n−1) … 2^(n−1) − 1; negate = invert + 1; overflow iff same-sign operands give opposite-sign result.
  - P3
- ○ **CS-8.1.B** Decode an IEEE 754 single-precision bit pattern and explain why 0.1 + 0.2 ≠ 0.3 in binary floating point.
  - EK: (−1)^s × 1.f × 2^(e−127); most decimal fractions have no finite binary expansion, so they round.
  - P3

### 8.2 Instruction execution

Book: cs2023 §AR-Assembly, §AR-Organization

- ○ **CS-8.2.A** Trace register and memory contents through a short RISC-V or x86 instruction sequence.
  - EK: Loads/stores move data between memory and registers; branches compare and set the PC; the stack grows downward.
  - P3

### 8.3 Memory hierarchy

Book: cs2023 §AR-Memory, §SF-Performance

- ○ **CS-8.3.A** Split an address into tag, index and offset bits for a given cache size, block size and associativity.
  - EK: offset = log₂(block bytes); sets = size/(block × ways); index = log₂(sets); tag = rest.
  - Needs: CS-8.1.A
  - P2
- ○ **CS-8.3.B** Simulate a direct-mapped or set-associative LRU cache on an address trace and compute the hit rate — auto-checked.
  - EK: Compulsory, capacity and conflict misses; higher associativity removes conflict misses only.
  - Needs: CS-8.3.A
  - P3
- ○ **CS-8.3.C** Compute average memory access time for a multi-level hierarchy.
  - EK: AMAT = hit time + miss rate × miss penalty, applied recursively per level.
  - P2

### 8.4 Performance laws

Book: cs2023 §AR-Performance-Energy, §SF-Performance, §SF-Evaluation

- ○ **CS-8.4.A** Compute CPU time from instruction count, CPI and clock rate, and compare two designs.
  - EK: CPU time = IC × CPI / f; the 'iron law' — no single factor alone measures speed.
  - P2
- ○ **CS-8.4.B** Apply Amdahl's law to compute overall speedup, or the fraction that must be sped up to hit a target.
  - EK: S = 1 / ((1 − p) + p/s); the serial fraction caps speedup at 1/(1 − p).
  - P2
- ○ **CS-8.4.C** Apply Little's law and utilisation to relate throughput, latency and queue length in a service.
  - EK: L = λW; utilisation ρ = λ/μ; queueing delay explodes as ρ → 1.
  - P2

## Unit 9 · Operating systems and systems programming

Big ideas: ABS, CONC, COST

### 9.1 Processes and system calls

Book: cs2023 §OS-Purpose, §OS-Process, §OS-Principles

- ○ **CS-9.1.A** Predict the output and number of processes created by code that calls fork(), exec() and wait().
  - EK: fork returns 0 in the child and the child PID in the parent; n sequential forks make 2ⁿ processes; exec replaces the image.
  - P3

### 9.2 CPU scheduling

Book: cs2023 §OS-Scheduling

- ○ **CS-9.2.A** Compute the schedule (Gantt order), average waiting and turnaround time under FCFS, SJF, SRTF, round-robin with quantum q, or priority — auto-checked.
  - EK: Turnaround = completion − arrival; waiting = turnaround − burst; SJF minimises average waiting time; RR trades it for response time.
  - P3 · P2

### 9.3 Concurrency and synchronization

Book: cs2023 §OS-Concurrency, §PDC-Coordination

- ○ **CS-9.3.A** Identify the race condition in a shared-memory snippet and give an interleaving that produces a wrong result.
  - EK: count++ is load–add–store; two threads interleaving those steps lose an update.
  - P3 · P6
- ○ **CS-9.3.B** Fix a race with a mutex, semaphore or condition variable and trace the semaphore values through a schedule.
  - EK: wait/P decrements and blocks below zero; signal/V increments and wakes one; check condition variables in a while loop.
  - Needs: CS-9.3.A
  - P5 · P3
- ○ **CS-9.3.C** Detect deadlock in a resource-allocation or wait-for graph, and run the banker's algorithm to decide whether a state is safe.
  - EK: Deadlock needs mutual exclusion, hold-and-wait, no preemption and circular wait; safe ⇔ some order lets every process finish.
  - P3 · P6

### 9.4 Memory management

Book: cs2023 §OS-Memory

- ○ **CS-9.4.A** Translate a virtual address to a physical one by walking a one- or two-level page table, counting memory accesses — auto-checked.
  - EK: VPN = high bits, offset = low log₂(page size) bits; each level indexes one table; PA = frame × page size + offset.
  - Needs: CS-8.1.A
  - P3
- ○ **CS-9.4.B** Compute page-table size and effective access time with a TLB of given hit rate.
  - EK: Entries = 2^(VA bits − offset bits); EAT = h·(t_TLB + t_mem) + (1 − h)·(t_TLB + (levels + 1)·t_mem).
  - Needs: CS-9.4.A
  - P2
- ○ **CS-9.4.C** Simulate FIFO, LRU and optimal page replacement on a reference string and count page faults.
  - EK: OPT evicts the page used farthest in future; LRU approximates it; FIFO can suffer Belady's anomaly.
  - P3

### 9.5 Files, storage and protection

Book: cs2023 §OS-Files, §OS-Devices, §OS-Protection

- ○ **CS-9.5.A** Compute the maximum file size for an inode with given direct, single-, double- and triple-indirect pointers.
  - EK: Pointers per block = block size / pointer size; max = (direct + p + p² + p³) × block size.
  - P2
- ○ **CS-9.5.B** Decide whether a user can read, write or execute a file from its Unix permission bits, owner and group (e.g. chmod 754).
  - EK: Three octal digits for owner/group/other; r = 4, w = 2, x = 1; the first matching class applies.
  - P3

### 9.6 Virtualization

Book: cs2023 §OS-Virtualization

- ○ **CS-9.6.A** Compare a VM and a container for a described deployment by isolation boundary, startup cost and overhead.
  - EK: VMs virtualise hardware with a guest kernel; containers share the host kernel, isolated by namespaces and limited by cgroups.
  - P4

## Unit 10 · Networking

Big ideas: ABS, COST, CONC

### 10.1 Layers and performance

Book: cs2023 §NC-Fundamentals

- ○ **CS-10.1.A** Compute transmission, propagation and total delay of a transfer, and the bandwidth–delay product of a link.
  - EK: d_trans = L/R; d_prop = distance/speed; BDP = R × RTT is the data in flight needed to fill the pipe.
  - P2

### 10.2 Application layer

Book: cs2023 §NC-Applications, §SPD-Web

- ○ **CS-10.2.A** Trace a DNS resolution and an HTTP request, and predict the status code and caching behaviour from given headers.
  - EK: Recursive resolver walks root → TLD → authoritative, caching by TTL; Cache-Control/ETag decide 200 vs 304.
  - P3

### 10.3 Reliable transport

Book: cs2023 §NC-Reliability

- ○ **CS-10.3.A** Trace sequence and acknowledgement numbers through a TCP handshake and data exchange.
  - EK: SYN and FIN each consume one sequence number; ACK = next byte expected.
  - P3
- ○ **CS-10.3.B** Compute link utilisation and throughput for stop-and-wait and sliding-window protocols.
  - EK: U = (W · L/R) / (RTT + L/R), capped at 1; window ≥ BDP keeps the link busy.
  - Needs: CS-10.1.A
  - P2
- ○ **CS-10.3.C** Trace TCP's congestion window across RTTs through slow start, congestion avoidance, a timeout and a triple duplicate ACK.
  - EK: Slow start doubles cwnd per RTT until ssthresh; AIMD adds 1 MSS per RTT; loss halves ssthresh (Reno fast recovery) or resets cwnd (timeout).
  - P3

### 10.4 Addressing and routing

Book: cs2023 §NC-Routing

- ○ **CS-10.4.A** Compute the network address, broadcast address, usable host range and host count for an IPv4 CIDR block, or subnet it into k pieces — auto-checked.
  - EK: Mask = prefix ones; network = IP AND mask; hosts = 2^(32 − prefix) − 2; borrowing b bits makes 2^b subnets.
  - Needs: CS-8.1.A
  - P2
- ○ **CS-10.4.B** Forward a packet by longest-prefix match against a routing table.
  - EK: Among matching prefixes, the longest (most specific) wins; 0.0.0.0/0 is the default route.
  - Needs: CS-10.4.A
  - P3
- ○ **CS-10.4.C** Compute a router's table after one round of distance-vector updates, or by link-state Dijkstra.
  - EK: DV: D_x(y) = min_v (c(x,v) + D_v(y)); link-state floods topology then runs Dijkstra locally.
  - Needs: CS-4.5.A
  - P3

### 10.5 Network security

Book: cs2023 §NC-Security

- ○ **CS-10.5.A** Evaluate an ordered firewall rule set against a list of packets and say which are allowed.
  - EK: First match wins; end with default deny; stateful firewalls allow return traffic of established connections.
  - P3 · P7

## Unit 11 · Security

Big ideas: ADV, CORR

### 11.1 Foundations and threat modelling

Book: cs2023 §SEC-Foundations, §SEC-Engineering

- ○ **CS-11.1.A** Classify a described incident by the CIA property violated and separate threat, vulnerability and risk.
  - EK: Confidentiality, integrity, availability; risk = likelihood × impact of a threat exploiting a vulnerability.
  - P7
- ○ **CS-11.1.B** Apply STRIDE to a data-flow diagram and list one threat and one mitigation per crossed trust boundary.
  - EK: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege; threats concentrate at trust boundaries.
  - P1 · P7

### 11.2 Secure coding

Book: cs2023 §SEC-Coding, §DM-Security

- ○ **CS-11.2.A** Identify the vulnerability class in a code snippet — SQL injection, XSS, CSRF, buffer overflow, path traversal, IDOR, TOCTOU race, insecure deserialization — and its CWE — auto-checked.
  - EK: Most classes are untrusted input reaching an interpreter or memory without validation; IDOR is a missing authorization check, not an input bug.
  - P6 · P7
- ○ **CS-11.2.B** Give the specific fix for an identified vulnerability (parameterised query, context-aware output encoding, CSRF token/SameSite, bounds check, server-side authorization).
  - EK: Fix the sink, not the symptom: blocklists fail; parameterisation separates code from data.
  - Needs: CS-11.2.A
  - P5

### 11.3 Cryptography in use

Book: cs2023 §SEC-Crypto

- ○ **CS-11.3.A** Pick the primitive for a goal — confidentiality, integrity, authentication, non-repudiation — among symmetric cipher, hash, MAC, signature and key exchange.
  - EK: Hashes give integrity only against accidents; MACs need a shared key; signatures give non-repudiation; use AEAD for confidentiality + integrity.
  - P4
- ○ **CS-11.3.B** Encrypt and decrypt with toy RSA (small primes): compute n, φ(n), d and c = m^e mod n.
  - EK: d = e⁻¹ mod φ(n); modular exponentiation by repeated squaring; security rests on factoring n.
  - Needs: CS-1.2.A
  - P3
- ○ **CS-11.3.C** Compute password entropy and brute-force time at a given guess rate, and state how passwords must be stored.
  - EK: Entropy = L·log₂(alphabet); time = 2^H / rate; store with a unique salt and a slow hash (bcrypt, scrypt, Argon2).
  - P2 · P7

### 11.4 Authentication, authorization and risk

Book: cs2023 §SEC-Engineering, §SEC-Governance

- ○ **CS-11.4.A** Trace an OAuth 2.0 authorization-code flow with PKCE and identify the token mishandling in a described implementation.
  - EK: Authentication says who; authorization says what; access tokens are bearer credentials; the ID token (OIDC) identifies the user.
  - P3 · P7
- ○ **CS-11.4.B** Compute annualised loss expectancy for a risk and decide whether a control is worth its cost.
  - EK: SLE = asset value × exposure factor; ALE = SLE × ARO; a control is justified if ΔALE > its annual cost.
  - P2 · P4

## Unit 12 · Programming languages

Big ideas: ABS, REP, CORR

### 12.1 Paradigms

Book: cs2023 §FPL-OOP, §FPL-Functional

- ○ **CS-12.1.A** Predict the output of a snippet that mixes overriding, overloading and dynamic dispatch.
  - EK: Overloads resolve at compile time on static types; overrides dispatch at run time on the object's dynamic type.
  - P3
- ○ **CS-12.1.B** Rewrite a loop with map, filter and reduce, and evaluate an expression built from higher-order functions and closures.
  - EK: A closure captures its defining environment; reduce folds with an accumulator from an initial value.
  - P5 · P3

### 12.2 Types

Book: cs2023 §FPL-Types

- ○ **CS-12.2.A** Decide whether an expression type-checks and infer the type of a polymorphic function.
  - EK: Hindley–Milner unifies constraints to the most general type, e.g. map : (a → b) → [a] → [b].
  - P6
- ○ **CS-12.2.B** Identify the variance error in a generic subtyping snippet (arrays, List<T>, function parameters).
  - EK: Producers are covariant, consumers contravariant; mutable containers must be invariant; functions are contravariant in arguments.
  - Needs: CS-12.2.A
  - P6

### 12.3 Binding, evaluation and run time

Book: cs2023 §FPL-Constructs, §FPL-Run-Time, §FPL-Semantics

- ○ **CS-12.3.A** Predict a program's output under lexical versus dynamic scope, and under pass-by-value, -reference and -sharing.
  - EK: Lexical scope resolves names where code is written; pass-by-sharing copies the reference, so mutation is visible but rebinding is not.
  - P3
- ○ **CS-12.3.B** Predict the output order of async JavaScript mixing synchronous code, promises, await and setTimeout.
  - EK: Run the call stack to empty, then all microtasks (promise callbacks), then one macrotask (timers, I/O).
  - P3

### 12.4 Translation

Book: cs2023 §FPL-Translation, §FPL-Syntax

- ○ **CS-12.4.A** Parse an expression under a grammar's precedence and associativity into an AST and evaluate it.
  - EK: Lower-precedence operators sit nearer the root; left-associative ⇒ left-leaning tree.
  - Needs: CS-5.1.C
  - P3

## Unit 13 · Artificial intelligence and machine learning

Big ideas: REP, COST, HUM

### 13.1 Search

Book: cs2023 §AI-Search

- ○ **CS-13.1.A** Trace uniform-cost or A* search — frontier and expansion order — and check whether a heuristic is admissible and consistent.
  - EK: A* expands lowest f = g + h; admissible h never overestimates ⇒ optimal tree search; consistent ⇒ optimal graph search.
  - Needs: CS-4.5.A
  - P3 · P6

### 13.2 Supervised learning

Book: cs2023 §AI-ML

- ○ **CS-13.2.A** Compute accuracy, precision, recall and F1 from a confusion matrix and pick the metric a scenario needs.
  - EK: Precision = TP/(TP + FP); recall = TP/(TP + FN); imbalanced classes make accuracy misleading.
  - P2 · P4
- ○ **CS-13.2.B** Diagnose under- or overfitting from training and validation curves and choose a remedy.
  - EK: High train and val error ⇒ bias; low train, high val ⇒ variance; regularise, add data or simplify for variance.
  - P6
- ○ **CS-13.2.C** Compute one gradient-descent update for linear or logistic regression on a tiny dataset.
  - EK: w ← w − η∇L; for MSE ∇_w = (2/n)Xᵀ(Xw − y); too large η diverges.
  - Needs: CS-1.4.A
  - P3
- ○ **CS-13.2.D** Classify a point by k-NN, or compute the information gain or Gini decrease of a decision-tree split.
  - EK: Entropy H = −Σ p log₂ p; gain = H(parent) − weighted H(children); Gini = 1 − Σ p².
  - P3 · P2

### 13.3 Language models

Book: cs2023 §AI-NLP

- ○ **CS-13.3.A** Compute cosine similarity between embedding vectors and the softmax attention weights for a tiny query–key set.
  - EK: cos = a·b/(|a||b|); attention = softmax(QKᵀ/√d)V; cost grows as n² in sequence length.
  - P3 · P2

### 13.4 AI and society

Book: cs2023 §AI-SEP

- ○ **CS-13.4.A** Compute demographic parity and equal-opportunity gaps for a classifier from per-group counts, and name the harm.
  - EK: Parity compares positive rates; equal opportunity compares true-positive rates; the two generally cannot both hold when base rates differ.
  - Needs: CS-13.2.A
  - P2 · P7

## Unit 14 · Parallel and distributed computing

Big ideas: CONC, COST

### 14.1 Parallel performance

Book: cs2023 §PDC-Programs, §PDC-Evaluation

- ○ **CS-14.1.A** Compute work, span and parallelism of a task DAG and bound the runtime on p processors.
  - EK: T₁ = work, T∞ = span; parallelism = T₁/T∞; greedy scheduling gives T_p ≤ T₁/p + T∞.
  - Needs: CS-8.4.B
  - P2
- ○ **CS-14.1.B** Compute strong- and weak-scaling efficiency from timings and explain the gap with Amdahl and Gustafson.
  - EK: Efficiency = S/p; Gustafson: scaled speedup = p − α(p − 1) when the problem grows with p.
  - P2

### 14.2 Ordering and coordination

Book: cs2023 §PDC-Communication, §PDC-Coordination

- ○ **CS-14.2.A** Assign Lamport timestamps or vector clocks to events in a message diagram and decide whether two events are causally ordered or concurrent.
  - EK: Lamport: L = max(local, received) + 1, consistent with but not implying causality; vector clocks capture happened-before exactly.
  - P3
- ○ **CS-14.2.B** Decide whether quorum settings R, W, N guarantee read-your-latest-write, and place keys on a consistent-hash ring.
  - EK: R + W > N ⇒ read and write quorums overlap; consistent hashing moves ~1/n of keys when a node joins.
  - P2 · P4

## Unit 15 · Human–computer interaction

Big ideas: HUM

### 15.1 Design and evaluation

Book: cs2023 §HCI-User, §HCI-Design, §HCI-Evaluation

- ○ **CS-15.1.A** Identify which of Nielsen's usability heuristics a described interface violates.
  - EK: Visibility of status, match with the real world, user control, consistency, error prevention, recognition over recall, …
  - P7
- ○ **CS-15.1.B** Use Fitts's law to compare the movement time for two target layouts.
  - EK: MT = a + b·log₂(1 + D/W); bigger, closer targets are faster; screen edges act as infinitely deep targets.
  - P2
- ○ **CS-15.1.C** Choose an evaluation method (usability test, heuristic review, A/B test, survey) for a question, and decide whether an A/B result is significant.
  - EK: Formative tests find problems with ~5 users; A/B tests measure effects and need a pre-set sample size and two-proportion z-test.
  - Needs: CS-1.4.C
  - P4 · P6

### 15.2 Accessibility

Book: cs2023 §HCI-Accessibility

- ○ **CS-15.2.A** Compute a colour-contrast ratio and identify the WCAG 2.x failure in a markup snippet (alt text, labels, focus, contrast).
  - EK: Ratio = (L₁ + 0.05)/(L₂ + 0.05); AA needs ≥ 4.5:1 for body text, 3:1 for large text; every control needs an accessible name.
  - P2 · P7

## Unit 16 · Society, ethics and the profession

Big ideas: HUM, ADV

### 16.1 Ethics, IP and privacy

Book: cs2023 §SEP-Ethical-Analysis, §SEP-Professional-Ethics, §SEP-IP, §SEP-Privacy

- ○ **CS-16.1.A** Identify the ACM Code of Ethics principle at stake in a scenario and the action it requires.
  - EK: Avoid harm (1.2) and the public good outrank employer instructions; honesty and competence obligations follow.
  - P7
- ○ **CS-16.1.B** State the obligations a reuse scenario triggers under MIT, Apache-2.0, GPL-3.0 or AGPL-3.0.
  - EK: Permissive: keep notice; Apache adds a patent grant; GPL: distribute derived source; AGPL: network use counts as distribution.
  - P7
- ○ **CS-16.1.C** Check whether a released table is k-anonymous for given quasi-identifiers and name the re-identification risk.
  - EK: Each quasi-identifier combination must appear ≥ k times; k-anonymity does not stop attribute disclosure (l-diversity).
  - P3 · P7

### 16.2 Sustainability

Book: cs2023 §SEP-Sustainability

- ○ **CS-16.2.A** Estimate the energy and carbon of a compute job from hardware power, utilisation, PUE and grid intensity.
  - EK: kWh = W × h × PUE / 1000; CO₂e = kWh × grid intensity (g/kWh); location and time shift matter.
  - P2 · P7

## Unit 17 · Advanced algorithms (extension)

Big ideas: COST, CORR

### 17.1 Network flow

Book: cs2023 §AL-Strategies

- ○ **CS-17.1.A** Compute a maximum flow and minimum cut with Ford–Fulkerson/Edmonds–Karp, tracing augmenting paths in the residual graph.
  - EK: Max-flow value = min-cut capacity; Edmonds–Karp's BFS paths give O(VE²).
  - Needs: CS-4.4.A
  - P3
- ○ **CS-17.1.B** Model a bipartite matching or assignment problem as a flow network and read the matching from the flow.
  - EK: Unit capacities source → left → right → sink; integral flow ⇒ a matching of the same size.
  - Needs: CS-17.1.A
  - P1

### 17.2 Randomised, approximation and string algorithms

Book: cs2023 §AL-Strategies, §AL-Complexity

- ○ **CS-17.2.A** Compute the approximation ratio of a greedy algorithm (e.g. maximal-matching vertex cover) on an instance and argue its bound.
  - EK: Ratio = ALG/OPT; taking both endpoints of a maximal matching gives a 2-approximation.
  - Needs: CS-5.2.C
  - P2 · P6
- ○ **CS-17.2.B** Compute the KMP failure function for a pattern, or a Rabin–Karp rolling hash across a text window.
  - EK: Failure[i] = length of the longest proper prefix that is also a suffix of pattern[0..i]; rolling hash updates in O(1).
  - P3

## Unit 18 · Distributed systems and cloud (extension)

Big ideas: CONC, COST, ABS

### 18.1 Consensus and replication

Book: cs2023 §PDC-Algorithms, §PDC-Coordination, §DM-Distributed

- ○ **CS-18.1.A** Trace Raft leader election and log replication through a described sequence of timeouts, votes and crashes.
  - EK: A candidate needs a majority in its term; an entry commits once replicated on a majority; n = 2f + 1 tolerates f crashes.
  - Needs: CS-14.2.A
  - P3
- ○ **CS-18.1.B** Identify where two-phase commit blocks when the coordinator fails, and what consensus-based commit changes.
  - EK: Participants that voted yes cannot decide alone; replicating the coordinator's decision with consensus removes the block.
  - P6

### 18.2 Cloud architecture

Book: cs2023 §PDC-Evaluation, §SF-Design

- ○ **CS-18.2.A** Compute the monthly cost of a workload under on-demand, reserved and serverless pricing and pick the cheapest model for its load shape.
  - EK: Serverless bills per request × duration and wins at low or spiky load; reserved wins at steady high utilisation.
  - P2 · P4
- ○ **CS-18.2.B** Compute the instances an autoscaler needs for a target load and utilisation, and the origin load left after a cache or CDN with a given hit rate.
  - EK: Instances = ⌈load / (per-instance capacity × target utilisation)⌉; origin load = (1 − hit rate) × requests.
  - Needs: CS-8.4.C
  - P2
- ○ **CS-18.2.C** Choose a shard key for a described dataset and query mix and predict hot-spotting.
  - EK: High-cardinality, evenly-accessed keys spread load; monotonic keys (timestamps) send all writes to one shard.
  - P4

## Unit 19 · Machine learning in depth (extension)

Big ideas: REP, COST

### 19.1 Neural networks

Book: cs2023 §AI-ML

- ○ **CS-19.1.A** Compute a forward pass of a small MLP and the backpropagated gradient for one weight.
  - EK: Chain rule layer by layer: ∂L/∂w = δ_out · a_in; ReLU passes gradient only where its input > 0.
  - Needs: CS-13.2.C
  - P3
- ○ **CS-19.1.B** Count the parameters and output shape of a convolutional or fully-connected layer.
  - EK: Conv params = (k_h·k_w·C_in + 1)·C_out; output = ⌊(n + 2p − k)/s⌋ + 1.
  - P2

### 19.2 Unsupervised learning

Book: cs2023 §AI-ML

- ○ **CS-19.2.A** Trace one k-means iteration (assign, recompute centroids), or compute variance explained by the top PCA components from eigenvalues.
  - EK: k-means minimises within-cluster squared distance and converges to a local optimum; variance explained = λ_i / Σλ.
  - P3 · P2
