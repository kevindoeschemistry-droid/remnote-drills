"""Proof-side mathematics (discrete, number theory, algebra, analysis, topology, Markov chains), recomputed by
brute force or from the definition, never by the formula the card teaches: phi by counting coprime residues, orders
by repeated multiplication, permutations by applying them, counts by enumeration, chains by solving the linear
equations, surfaces by gluing a polygon's corners.
"""
import itertools
import math

import sympy as sp


def check(p, H_):
    return None


# ---- number theory ----
def pm_phi(n):
    n = int(n)
    return sp.Integer(sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1))


def pm_inv(a, n):
    a, n = int(a), int(n)
    return sp.Integer(next(k for k in range(1, n) if a * k % n == 1))


def pm_powmod(a, k, n):
    r = 1
    for _ in range(int(k)):
        r = r * int(a) % int(n)
    return sp.Integer(r)


def pm_crt(a1, n1, a2, n2):
    return sp.Integer(next(k for k in range(int(n1) * int(n2)) if k % int(n1) == int(a1) % int(n1) and k % int(n2) == int(a2) % int(n2)))


def pm_order(a, n):
    a, n = int(a), int(n)
    r, k = a % n, 1
    while r != 1:
        r, k = r * a % n, k + 1
    return sp.Integer(k)


def pm_legendre(a, p):
    a, p = int(a), int(p)
    return sp.Integer(1 if any(k * k % p == a % p for k in range(1, p)) else -1)


def pm_ndiv(n):
    return sp.Integer(sum(1 for k in range(1, int(n) + 1) if int(n) % k == 0))


def pm_sigma(n):
    return sp.Integer(sum(k for k in range(1, int(n) + 1) if int(n) % k == 0))


def pm_gcd_steps(a, b):
    """number of division steps Euclid's algorithm takes on (a, b), a > b > 0"""
    a, b, k = int(a), int(b), 0
    while b:
        a, b, k = b, a % b, k + 1
    return sp.Integer(k)


def pm_bezout_x(a, b):
    """the least non-negative x with a*x congruent to gcd(a, b) modulo b"""
    a, b = int(a), int(b)
    g = math.gcd(a, b)
    return sp.Integer(next(x for x in range(b) if (a * x - g) % b == 0))


def pm_dioph_count(a, b, c):
    """solutions of a*x + b*y = c in non-negative integers"""
    a, b, c = int(a), int(b), int(c)
    return sp.Integer(sum(1 for x in range(c // a + 1) if (c - a * x) % b == 0))


def pm_primroots(p):
    p = int(p)
    return sp.Integer(sum(1 for a in range(1, p) if pm_order(a, p) == p - 1))


def pm_cf_term(p, q, k):
    """k-th partial quotient (from 0) of p/q"""
    p, q, out = int(p), int(q), []
    while q:
        out.append(p // q)
        p, q = q, p % q
    return sp.Integer(out[int(k)])


def pm_sum2sq(n):
    n = int(n)
    return sp.Integer(1 if any(a * a + b * b == n for a in range(n + 1) for b in range(a, n + 1) if a * a + b * b <= n) else 0)


def pm_pell_x(d):
    """least x > 1 with x^2 - d y^2 = 1 for some integer y >= 1"""
    d, y = int(d), 1
    while True:
        x = math.isqrt(d * y * y + 1)
        if x * x == d * y * y + 1:
            return sp.Integer(x)
        y += 1


# ---- permutations and groups ----
def _perm(cyc, n):
    """'123|45' on {1..n} as a dict"""
    f = {k: k for k in range(1, n + 1)}
    for c in str(cyc).split("|"):
        xs = [int(ch) for ch in c]
        for a, b in zip(xs, xs[1:] + xs[:1]):
            f[a] = b
    return f


def _deg(*cycs):
    return max(int(ch) for c in cycs for ch in str(c) if ch.isdigit())


def pm_perm_order(cyc):
    n = _deg(cyc)
    f = _perm(cyc, n)
    g, k = dict(f), 1
    while any(g[x] != x for x in g):
        g, k = {x: f[g[x]] for x in g}, k + 1
    return sp.Integer(k)


def pm_perm_sign(cyc):
    n = _deg(cyc)
    f = _perm(cyc, n)
    inv = sum(1 for a in range(1, n + 1) for b in range(a + 1, n + 1) if f[a] > f[b])
    return sp.Integer(1 if inv % 2 == 0 else -1)


def pm_perm_image(c1, c2, x):
    """(c1 then... ) the product c1 c2 read right to left: apply c2 first, then c1"""
    n = _deg(c1, c2)
    f, g = _perm(c1, n), _perm(c2, n)
    return sp.Integer(f[g[int(x)]])


def pm_zn_count_order(n, d):
    """elements of additive order d in Z_n"""
    n, d = int(n), int(d)
    def order(a):
        k, s = 1, a % n
        while s:
            s, k = (s + a) % n, k + 1
        return k
    return sp.Integer(sum(1 for a in range(n) if order(a) == d))


def pm_units_is_cyclic(n):
    n = int(n)
    units = [a for a in range(1, n) if math.gcd(a, n) == 1]
    return sp.Integer(1 if any(pm_order(a, n) == len(units) for a in units) else 0)


def pm_partitions(n):
    def count(m, largest):
        return 1 if m == 0 else sum(count(m - k, k) for k in range(1, min(m, largest) + 1))
    return sp.Integer(count(int(n), int(n)))


def pm_necklaces(n, k):
    """colourings of n beads on a rotating ring with k colours, counted up to rotation by enumeration"""
    n, k = int(n), int(k)
    seen = set()
    for w in itertools.product(range(k), repeat=n):
        seen.add(min(w[i:] + w[:i] for i in range(n)))
    return sp.Integer(len(seen))


def pm_bracelets(n, k):
    n, k = int(n), int(k)
    seen = set()
    for w in itertools.product(range(k), repeat=n):
        rots = [w[i:] + w[:i] for i in range(n)]
        seen.add(min(rots + [r[::-1] for r in rots]))
    return sp.Integer(len(seen))


def pm_sn_class_size(cyc):
    """number of permutations in S_n with the cycle type 'a,b,c' (fixed points included)"""
    t = sorted(int(x) for x in str(cyc).split(","))
    n = sum(t)
    cnt = 0
    for p in itertools.permutations(range(n)):
        seen, typ = set(), []
        for s in range(n):
            if s in seen:
                continue
            x, ln = s, 0
            while x not in seen:
                seen.add(x)
                x, ln = p[x], ln + 1
            typ.append(ln)
        cnt += sorted(typ) == t
    return sp.Integer(cnt)


def pm_hom_count(m, n):
    m, n = int(m), int(n)
    return sp.Integer(sum(1 for a in range(n) if m * a % n == 0))


def pm_sylow_options(order, p):
    order, p = int(order), int(p)
    m = order
    while m % p == 0:
        m //= p
    return sp.Integer(sum(1 for d in range(1, m + 1) if m % d == 0 and d % p == 1))


def pm_zero_divisors(n):
    n = int(n)
    return sp.Integer(sum(1 for a in range(1, n) if any(a * b % n == 0 for b in range(1, n))))


def pm_poly_roots_mod(coeffs, p):
    """roots in Z_p of the polynomial with coefficients 'c0,c1,c2,...' (constant first)"""
    cs = [int(c) for c in str(coeffs).split(",")]
    return sp.Integer(sum(1 for x in range(int(p)) if sum(c * x ** k for k, c in enumerate(cs)) % int(p) == 0))


def pm_idempotents(n):
    n = int(n)
    return sp.Integer(sum(1 for a in range(n) if a * a % n == a))


def pm_gauss_norm_factor(n):
    """1 if n = a^2 + b^2 with a, b >= 1 (so n is not irreducible in Z[i] when n is prime), else 0"""
    n = int(n)
    return sp.Integer(1 if any(a * a + b * b == n for a in range(1, n) for b in range(1, n)) else 0)


# ---- counting ----
def pm_derange(n):
    n = int(n)
    return sp.Integer(sum(1 for p in itertools.permutations(range(n)) if all(p[k] != k for k in range(n))))


def pm_surj(n, k):
    n, k = int(n), int(k)
    return sp.Integer(sum(1 for f in itertools.product(range(k), repeat=n) if len(set(f)) == k))


def pm_inj(n, k):
    n, k = int(n), int(k)
    return sp.Integer(sum(1 for f in itertools.product(range(k), repeat=n) if len(set(f)) == n))


def pm_solutions(n, k, lo):
    """solutions of x1 + ... + xk = n with every xi >= lo"""
    n, k, lo = int(n), int(k), int(lo)
    return sp.Integer(sum(1 for x in itertools.product(range(lo, n + 1), repeat=k) if sum(x) == n))


def pm_divisible_any(top, ds):
    ds = [int(d) for d in str(ds).split(",")]
    return sp.Integer(sum(1 for m in range(1, int(top) + 1) if any(m % d == 0 for d in ds)))


def pm_recur(a, b, f0, f1, n):
    """f(n) = a f(n-1) + b f(n-2)"""
    x, y = sp.Integer(f0), sp.Integer(f1)
    for _ in range(int(n) - 1):
        x, y = y, a * y + b * x
    return y if int(n) >= 1 else x


def pm_words(letters):
    return sp.Integer(len(set(itertools.permutations(str(letters)))))


def pm_tt_count(expr, nvars):
    """rows of the truth table on p, q, r (the first nvars of them) where the Python expression is true"""
    names = ["p", "q", "r"][:int(nvars)]
    return sp.Integer(sum(1 for vals in itertools.product([False, True], repeat=len(names))
                          if eval(expr, {"__builtins__": {}}, dict(zip(names, vals)))))  # noqa: S307


def pm_relations(n, kind):
    """relations on an n-set: kind 1 reflexive, 2 symmetric, 3 equivalence relations"""
    n, kind = int(n), int(kind)
    pairs = [(a, b) for a in range(n) for b in range(n)]
    cnt = 0
    for bits in itertools.product([0, 1], repeat=len(pairs)):
        r = {p for p, b in zip(pairs, bits) if b}
        refl = all((a, a) in r for a in range(n))
        sym = all((b, a) in r for a, b in r)
        tra = all((a, d) in r for a, b in r for c, d in r if b == c)
        cnt += refl if kind == 1 else sym if kind == 2 else (refl and sym and tra)
    return sp.Integer(cnt)


def pm_binom_coeff(a, b, n, k):
    """coefficient of x^k in (a x + b)^n, by expansion"""
    t = sp.Symbol("t")
    return sp.Poly(sp.expand((a * t + b) ** int(n)), t).coeff_monomial(t ** int(k))


def pm_gf_coeff(expr, k):
    """coefficient of t^k in the power series of a Python expression in t"""
    t = sp.Symbol("t")
    f = sp.sympify(eval(expr, {"__builtins__": {}}, {"t": t}))  # noqa: S307
    return sp.series(f, t, 0, int(k) + 1).removeO().coeff(t, int(k))


# ---- graphs: edges written 'a-b,b-c' ----
def _graph(edges):
    es = [tuple(e.split("-")) for e in str(edges).split(",")]
    vs = sorted({v for e in es for v in e})
    return vs, es


def pm_g_odd(edges):
    vs, es = _graph(edges)
    return sp.Integer(sum(1 for v in vs if sum(v in e for e in es) % 2 == 1))


def pm_g_spanning(edges):
    vs, es = _graph(edges)
    n = len(vs)
    L = sp.zeros(n, n)
    for a, b in es:
        i, j = vs.index(a), vs.index(b)
        L[i, i] += 1; L[j, j] += 1; L[i, j] -= 1; L[j, i] -= 1
    return L[1:, 1:].det()


def pm_g_colourings(edges, k):
    vs, es = _graph(edges)
    return sp.Integer(sum(1 for c in itertools.product(range(int(k)), repeat=len(vs))
                          if all(c[vs.index(a)] != c[vs.index(b)] for a, b in es)))


def pm_g_chromatic(edges):
    k = 1
    while pm_g_colourings(edges, k) == 0:
        k += 1
    return sp.Integer(k)


def pm_g_components(edges, nverts):
    vs, es = _graph(edges)
    par = {v: v for v in vs}
    def find(x):
        while par[x] != x:
            x = par[x]
        return x
    for a, b in es:
        par[find(a)] = find(b)
    return sp.Integer(len({find(v) for v in vs}) + int(nverts) - len(vs))


def pm_g_hamilton(edges):
    vs, es = _graph(edges)
    adj = {frozenset(e) for e in es}
    for p in itertools.permutations(vs[1:]):
        cyc = [vs[0]] + list(p)
        if all(frozenset((cyc[i], cyc[(i + 1) % len(cyc)])) in adj for i in range(len(cyc))):
            return sp.Integer(1)
    return sp.Integer(0)


# ---- analysis ----
def pm_first_n(expr, limit, eps):
    """least N with |a_n - limit| < eps for every n >= N, for a sequence monotone in |a_n - limit| (checked far out)"""
    f = lambda n: abs(eval(expr, {"__builtins__": {}}, {"n": sp.Integer(n), "sqrt": sp.sqrt, "factorial": sp.factorial, "Rational": sp.Rational}) - sp.nsimplify(limit))  # noqa: S307,E731
    e = sp.nsimplify(eps)
    n = 1
    while not f(n) < e:
        n += 1
    assert all(f(m) < e for m in range(n, n + 200))
    return sp.Integer(n)


def pm_upper_sum(expr, a, b, n):
    """upper Riemann sum of an increasing function on n equal pieces of [a, b]"""
    a, b, n = sp.nsimplify(a), sp.nsimplify(b), int(n)
    h = (b - a) / n
    f = lambda x: sp.sympify(eval(expr, {"__builtins__": {}}, {"t": x, "sqrt": sp.sqrt}))  # noqa: S307,E731
    return sum(f(a + (k + 1) * h) for k in range(n)) * h


def pm_lower_sum(expr, a, b, n):
    a, b, n = sp.nsimplify(a), sp.nsimplify(b), int(n)
    h = (b - a) / n
    f = lambda x: sp.sympify(eval(expr, {"__builtins__": {}}, {"t": x, "sqrt": sp.sqrt}))  # noqa: S307,E731
    return sum(f(a + k * h) for k in range(n)) * h


# ---- finite topologies: points are letters, open sets written 'a|ab|abc' (the empty set is '0') ----
def _opens(sets):
    return {frozenset() if s == "0" else frozenset(s) for s in str(sets).split("|")}


def pm_is_topology(points, sets):
    X, T = frozenset(str(points)), _opens(sets)
    ok = frozenset() in T and X in T and all(a | b in T and a & b in T for a in T for b in T)
    return sp.Integer(1 if ok else 0)


def pm_closure_size(points, sets, sub):
    X, T, A = frozenset(str(points)), _opens(sets), frozenset(str(sub))
    closed = [X - u for u in T]
    return sp.Integer(len(frozenset.intersection(*[c for c in closed if A <= c])))


def pm_interior_size(points, sets, sub):
    T, A = _opens(sets), frozenset(str(sub))
    return sp.Integer(len(frozenset().union(*[u for u in T if u <= A])))


def pm_top_connected(points, sets):
    X, T = frozenset(str(points)), _opens(sets)
    return sp.Integer(0 if any(u and u != X and (X - u) in T for u in T) else 1)


def pm_top_hausdorff(points, sets):
    X, T = sorted(str(points)), _opens(sets)
    ok = all(any(a in u and b in v and not (u & v) for u in T for v in T) for a in X for b in X if a < b)
    return sp.Integer(1 if ok else 0)


def pm_top_count(n):
    """topologies on an n-point set (n <= 3), by checking every family of subsets"""
    pts = "abc"[:int(n)]
    subs = [frozenset(c) for r in range(len(pts) + 1) for c in itertools.combinations(pts, r)]
    cnt = 0
    for bits in itertools.product([0, 1], repeat=len(subs)):
        T = {s for s, b in zip(subs, bits) if b}
        cnt += frozenset() in T and frozenset(pts) in T and all(a | b in T and a & b in T for a in T for b in T)
    return sp.Integer(cnt)


def pm_surface_chi(word):
    """Euler characteristic of the closed surface from a polygon word such as 'a b A B' (capital = reversed edge):
    V - E + F with V counted by gluing corners"""
    w = str(word).split()
    m = len(w)
    par = list(range(m))
    def find(x):
        while par[x] != x:
            x = par[x]
        return x
    ends = {}
    for i, s in enumerate(w):
        tail, head = (i, (i + 1) % m) if s.islower() else ((i + 1) % m, i)
        if s.lower() in ends:
            t0, h0 = ends[s.lower()]
            par[find(tail)] = find(t0); par[find(head)] = find(h0)
        else:
            ends[s.lower()] = (tail, head)
    return sp.Integer(len({find(v) for v in range(m)}) - m // 2 + 1)


def pm_surface_vertices(word):
    """number of distinct corners left after gluing the polygon's sides"""
    return pm_surface_chi(word) + len(str(word).split()) // 2 - 1


def pm_top_generated(points, sets):
    """number of open sets in the smallest topology containing the given sets"""
    X = frozenset(str(points))
    T = _opens(sets) | {frozenset(), X}
    while True:
        new = {a | b for a in T for b in T} | {a & b for a in T for b in T}
        if new <= T:
            return sp.Integer(len(T))
        T |= new


def pm_surface_orientable(word):
    w = str(word).split()
    return sp.Integer(0 if any(w.count(s) == 2 for s in set(w)) else 1)


# ---- Markov chains: rows written '0.9,0.1;0.5,0.5' ----
def _P(rows):
    return sp.Matrix([[sp.nsimplify(x, rational=True) for x in r.split(",")] for r in str(rows).split(";")])


def pm_mc_nstep(rows, n, i, j):
    return (_P(rows) ** int(n))[int(i), int(j)]


def pm_mc_stationary(rows, j):
    P = _P(rows)
    n = P.shape[0]
    xs = sp.symbols(f"x0:{n}")
    sol = sp.solve([sum(xs[i] * P[i, k] for i in range(n)) - xs[k] for k in range(n - 1)] + [sum(xs) - 1], xs, dict=True)[0]
    return sol[xs[int(j)]]


def pm_mc_hit_time(rows, target, start):
    """expected steps to reach `target` from `start`"""
    P = _P(rows)
    n, t = P.shape[0], int(target)
    ks = sp.symbols(f"k0:{n}")
    eqs = [ks[t]] + [ks[i] - 1 - sum(P[i, j] * ks[j] for j in range(n)) for i in range(n) if i != t]
    return sp.solve(eqs, ks, dict=True)[0][ks[int(start)]]


def pm_mc_absorb(rows, target, start):
    """probability of being absorbed in `target` (an absorbing state) from `start`"""
    P = _P(rows)
    n, t = P.shape[0], int(target)
    hs = sp.symbols(f"h0:{n}")
    eqs = []
    for i in range(n):
        if i == t: eqs.append(hs[i] - 1)
        elif P[i, i] == 1: eqs.append(hs[i])
        else: eqs.append(hs[i] - sum(P[i, j] * hs[j] for j in range(n)))
    return sp.solve(eqs, hs, dict=True)[0][hs[int(start)]]


def pm_ruin_win(p, i, N):
    """probability a walk on 0..N stepping +1 with probability p reaches N before 0, from i"""
    p, N = sp.nsimplify(p, rational=True), int(N)
    hs = sp.symbols(f"h0:{N + 1}")
    eqs = [hs[0], hs[N] - 1] + [hs[k] - p * hs[k + 1] - (1 - p) * hs[k - 1] for k in range(1, N)]
    return sp.solve(eqs, hs, dict=True)[0][hs[int(i)]]


def pm_ruin_time(i, N):
    """expected duration of the fair game on 0..N from i"""
    N = int(N)
    ks = sp.symbols(f"k0:{N + 1}")
    eqs = [ks[0], ks[N]] + [ks[k] - 1 - (ks[k + 1] + ks[k - 1]) / 2 for k in range(1, N)]
    return sp.solve(eqs, ks, dict=True)[0][ks[int(i)]]


def pm_mc_classes(rows):
    P = _P(rows)
    n = P.shape[0]
    reach = [[i == j or P[i, j] != 0 for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])
    return sp.Integer(len({frozenset(j for j in range(n) if reach[i][j] and reach[j][i]) for i in range(n)}))


def pm_mc_period(rows, i):
    P = _P(rows)
    i = int(i)
    g, M = 0, sp.eye(P.shape[0])
    for n in range(1, 25):
        M = M * P
        if M[i, i] != 0:
            g = math.gcd(g, n)
    return sp.Integer(g)


def pm_graph_walk_stationary(edges, v):
    vs, es = _graph(edges)
    P = sp.zeros(len(vs), len(vs))
    for a, b in es:
        P[vs.index(a), vs.index(b)] += 1; P[vs.index(b), vs.index(a)] += 1
    rows = ";".join(",".join(str(P[i, j] / sum(P[i, :])) for j in range(len(vs))) for i in range(len(vs)))
    return pm_mc_stationary(rows, vs.index(str(v)))


def pm_ctmc_stationary(rates, j):
    """stationary probability of state j for a birth-death chain with rates 'up0,up1,...;down1,down2,...'"""
    up, down = [[sp.nsimplify(x, rational=True) for x in part.split(",")] for part in str(rates).split(";")]
    w = [sp.Integer(1)]
    for u, d in zip(up, down):
        w.append(w[-1] * u / d)
    return w[int(j)] / sum(w)


# ---- second layer: fields, Jacobi, factorising, homotopy, pricing ----
def pm_minpoly_deg(expr):
    """degree over Q of the algebraic number written as a Python expression (sqrt, cbrt, I, Rational available)"""
    t = sp.Symbol("t")
    a = sp.sympify(eval(expr, {"__builtins__": {}}, {"sqrt": sp.sqrt, "cbrt": sp.cbrt, "I": sp.I, "Rational": sp.Rational, "root": sp.root, "exp": sp.exp, "pi": sp.pi, "cos": sp.cos}))  # noqa: S307
    return sp.Integer(sp.degree(sp.minimal_polynomial(a, t), t))


def pm_irreducible_count(p, d):
    """monic irreducible polynomials of degree d over F_p, by removing every product of two monic polynomials"""
    p, d = int(p), int(d)
    def mul(a, b):
        out = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                out[i + j] = (out[i + j] + x * y) % p
        return tuple(out)
    monic = lambda k: [c + (1,) for c in itertools.product(range(p), repeat=k)]  # noqa: E731
    red = {mul(a, b) for k in range(1, d // 2 + 1) for a in monic(k) for b in monic(d - k)}
    return sp.Integer(len([f for f in monic(d) if f not in red]))


def pm_jacobi(a, n):
    """Jacobi symbol as a product of Legendre symbols over the prime factors of n"""
    a, n, out, q = int(a), int(n), 1, 3
    if math.gcd(a, n) > 1:
        return sp.Integer(0)
    while n > 1:
        while n % q == 0:
            out *= int(pm_legendre(a, q))
            n //= q
        q += 2
    return sp.Integer(out)


def pm_fermat_a(n):
    """least a >= sqrt(n) with a^2 - n a perfect square"""
    n = int(n)
    a = math.isqrt(n)
    if a * a < n:
        a += 1
    while math.isqrt(a * a - n) ** 2 != a * a - n:
        a += 1
    return sp.Integer(a)


def pm_g_cycle_rank(edges):
    """rank of the fundamental group of a connected graph: edges not in a spanning tree, found by building one"""
    vs, es = _graph(edges)
    par = {v: v for v in vs}
    def find(x):
        while par[x] != x:
            x = par[x]
        return x
    extra = 0
    for a, b in es:
        if find(a) == find(b):
            extra += 1
        else:
            par[find(a)] = find(b)
    return sp.Integer(extra)


def pm_replicate_price(s0, u, d, r, pu, pd):
    """one-period binomial price by replication: hold D shares and B in the bank so both outcomes are matched"""
    s0, u, d, r, pu, pd = [sp.nsimplify(x, rational=True) for x in (s0, u, d, r, pu, pd)]
    D, B = sp.symbols("D B")
    sol = sp.solve([D * s0 * u + B * (1 + r) - pu, D * s0 * d + B * (1 + r) - pd], [D, B], dict=True)[0]
    return sol[D] * s0 + sol[B]


# ---- third layer: dihedral groups, one-line permutations, quotients, proof bridge ----
def _dihedral(n):
    """the 2n symmetries of a regular n-gon as tuples acting on corners 0..n-1"""
    rots = [tuple((i + k) % n for i in range(n)) for k in range(n)]
    refl = [tuple((k - i) % n for i in range(n)) for k in range(n)]
    return rots + refl


def _comp(f, g):
    return tuple(f[g[i]] for i in range(len(f)))


def pm_dihedral_order2(n):
    G = _dihedral(int(n)); e = G[0]
    return sp.Integer(sum(1 for g in G if g != e and _comp(g, g) == e))


def pm_dihedral_center(n):
    G = _dihedral(int(n))
    return sp.Integer(sum(1 for g in G if all(_comp(g, h) == _comp(h, g) for h in G)))


def pm_dihedral_classes(n):
    G = _dihedral(int(n))
    inv = {g: next(h for h in G if _comp(g, h) == G[0]) for g in G}
    return sp.Integer(len({frozenset(_comp(_comp(h, g), inv[h]) for h in G) for g in G}))


def pm_dihedral_srs(n, k):
    """the exponent j (0..n-1) with s r^k s = r^j, where r is a rotation and s a reflection"""
    n, k = int(n), int(k)
    G = _dihedral(n); r, s = G[1], G[n]
    rk = G[0]
    for _ in range(k):
        rk = _comp(r, rk)
    return sp.Integer(G.index(_comp(_comp(s, rk), s)))


def _oneline(s):
    xs = [int(x) for x in str(s).split()]
    return {i + 1: v for i, v in enumerate(xs)}


def _cycles(f):
    seen, out = set(), []
    for a in sorted(f):
        if a in seen:
            continue
        ln, x = 0, a
        while x not in seen:
            seen.add(x); x = f[x]; ln += 1
        out.append(ln)
    return out


def pm_oneline_order(s):
    return sp.Integer(sp.ilcm(1, *_cycles(_oneline(s))))


def pm_oneline_cycles(s):
    """number of cycles, counting fixed points"""
    return sp.Integer(len(_cycles(_oneline(s))))


def pm_perm_power_image(cyc, k, x):
    f = _perm(cyc, _deg(cyc)); x = int(x)
    for _ in range(int(k)):
        x = f[x]
    return sp.Integer(x)


def pm_perm_inverse_image(cyc, x):
    f = _perm(cyc, _deg(cyc))
    return sp.Integer(next(a for a in f if f[a] == int(x)))


def pm_perm_transpositions(cyc, n):
    """fewest transpositions whose product is the permutation, on n points: n minus the number of cycles"""
    return sp.Integer(int(n) - len(_cycles(_perm(cyc, int(n)))))


def pm_perm_orbits(cyc, n):
    return sp.Integer(len(_cycles(_perm(cyc, int(n)))))


def pm_conj_image(sigma, tau, x):
    """where tau sigma tau^-1 sends x"""
    n = _deg(sigma, tau)
    f, g = _perm(sigma, n), _perm(tau, n)
    ginv = {v: k for k, v in g.items()}
    return sp.Integer(g[f[ginv[int(x)]]])


def pm_kernel_size(k, n):
    """elements x of Z_n with k x = 0"""
    return sp.Integer(sum(1 for x in range(int(n)) if int(k) * x % int(n) == 0))


def pm_prod_count_order(m, n, d):
    """elements of order d in Z_m x Z_n"""
    m, n, d = int(m), int(n), int(d)
    def order(a, b):
        k, x, y = 1, a % m, b % n
        while x or y:
            x, y, k = (x + a) % m, (y + b) % n, k + 1
        return k
    return sp.Integer(sum(1 for a in range(m) for b in range(n) if order(a, b) == d))


def pm_quotient_order(a, d, n):
    """order of the coset a + <d> in Z_n / <d>, d dividing n"""
    a, d = int(a), int(d)
    k, x = 1, a % d
    while x:
        x, k = (x + a) % d, k + 1
    return sp.Integer(k)


def pm_frobenius_next(a, b):
    """least N such that every integer >= N is a non-negative combination of coprime a and b"""
    a, b = int(a), int(b)
    ok = lambda m: any((m - a * x) % b == 0 for x in range(m // a + 1))  # noqa: E731
    top = a * b
    bad = [m for m in range(1, top + 1) if not ok(m)]
    return sp.Integer(max(bad) + 1)


def pm_bisect_cover(a, d, x):
    """least non-negative member of the coset x + <d> in Z_n"""
    return sp.Integer(int(x) % int(d))


def pm_distinct_values(expr, upto):
    """number of distinct values a periodic sequence takes for n = 1..upto (its subsequential limits)"""
    ns = {"sin": sp.sin, "cos": sp.cos, "pi": sp.pi, "Rational": sp.Rational}
    vals = set()
    for n in range(1, int(upto) + 1):
        vals.add(sp.nsimplify(eval(expr, {"__builtins__": {}}, dict(ns, n=sp.Integer(n)))))  # noqa: S307
    return sp.Integer(len(vals))  # noqa: S307


# ---- fourth layer: intermediate steps for number theory, topology, chains and geometry ----
def pm_prime_count(lo, hi):
    """primes p with lo <= p <= hi, by trial division"""
    return sp.Integer(sum(1 for m in range(max(2, int(lo)), int(hi) + 1) if all(m % d for d in range(2, math.isqrt(m) + 1))))


def pm_trial_bound(n):
    """largest prime not exceeding the square root of n"""
    r = math.isqrt(int(n))
    return sp.Integer(max(m for m in range(2, r + 1) if all(m % d for d in range(2, m))))


def pm_vp_factorial(n, p):
    """exponent of the prime p in n!, by factorising each of 1..n"""
    n, p, e = int(n), int(p), 0
    for m in range(1, n + 1):
        while m % p == 0:
            m //= p; e += 1
    return sp.Integer(e)


def pm_cong_solutions(a, b, n):
    """residues x modulo n with a x = b"""
    a, b, n = int(a), int(b), int(n)
    return sp.Integer(sum(1 for x in range(n) if (a * x - b) % n == 0))


def pm_cong_least(a, b, n):
    a, b, n = int(a), int(b), int(n)
    return sp.Integer(next(x for x in range(n) if (a * x - b) % n == 0))


def pm_digit_mod(num, m):
    return sp.Integer(int(str(num)) % int(m))


def pm_boundary_count(pieces):
    """boundary points of a finite union of intervals and points of the real line, written '(0,1);[2,3);{5}'"""
    ends, ivs, pts = set(), [], set()
    for pc in str(pieces).split(";"):
        if pc[0] == "{":
            pts.add(sp.nsimplify(pc[1:-1]))
        else:
            a, b = [sp.nsimplify(v) for v in pc[1:-1].split(",")]
            ivs.append((a, b)); ends |= {a, b}
    inside = lambda v: any(a < v < b for a, b in ivs)  # noqa: E731
    return sp.Integer(len({v for v in ends | pts if not inside(v)}))


def pm_interval_components(pieces):
    """connected components of a finite union of intervals and points, written '(0,1);[1,2);{5}'"""
    ivs = []
    for pc in str(pieces).split(";"):
        if pc[0] == "{":
            v = sp.nsimplify(pc[1:-1]); ivs.append([v, v, True, True])
        else:
            a, b = [sp.nsimplify(v) for v in pc[1:-1].split(",")]
            ivs.append([a, b, pc[0] == "[", pc[-1] == "]"])
    ivs.sort(key=lambda t: (t[0], not t[2]))
    n, cur = 1, ivs[0][:]
    for nx in ivs[1:]:
        if nx[0] < cur[1] or (nx[0] == cur[1] and (cur[3] or nx[2])):
            if nx[1] > cur[1] or (nx[1] == cur[1] and nx[3]):
                cur[1], cur[3] = nx[1], nx[3]
        else:
            n, cur = n + 1, nx[:]
    return sp.Integer(n)


def pm_min_cover(points, sets):
    """fewest of the listed sets ('ab|bc|cd') whose union is all the points"""
    X = frozenset(str(points)); S = [frozenset(x) for x in str(sets).split("|")]
    for k in range(1, len(S) + 1):
        if any(frozenset().union(*c) == X for c in itertools.combinations(S, k)):
            return sp.Integer(k)
    return sp.Integer(0)


def pm_preimage_open(points, sets, fmap, tsets):
    """1 if the map 'a>x,b>y' between finite spaces is continuous: every open set of the target pulls back to an open set"""
    T, U = _opens(sets), _opens(tsets)
    f = dict(pr.split(">") for pr in str(fmap).split(","))
    return sp.Integer(1 if all(frozenset(a for a in f if f[a] in u) in T for u in U) else 0)


def pm_walk_prob(n, k, p):
    """P(S_n = k) for a walk of n steps of +1 (probability p) or -1, by summing over every path"""
    n, k, p = int(n), int(k), sp.nsimplify(p, rational=True)
    tot = sp.Integer(0)
    for path in itertools.product([1, -1], repeat=n):
        if sum(path) == k:
            ups = path.count(1)
            tot += p ** ups * (1 - p) ** (n - ups)
    return tot


def pm_walk_first_return(n):
    """probability that a simple symmetric walk first returns to 0 at step 2n"""
    n = int(n); cnt = 0
    for path in itertools.product([1, -1], repeat=2 * n):
        s, ok = 0, True
        for i, st in enumerate(path):
            s += st
            if s == 0 and i < 2 * n - 1:
                ok = False; break
        cnt += ok and s == 0
    return sp.Rational(cnt, 2 ** (2 * n))


def pm_mc_path(rows, path):
    """probability of following the states 'i,j,k,...' in order, given the first"""
    P = _P(rows); st = [int(x) for x in str(path).split(",")]
    out = sp.Integer(1)
    for a, b in zip(st, st[1:]):
        out *= P[a, b]
    return out


def pm_mc_dist(rows, start, n, j):
    """probability of state j after n steps from the start distribution 'a,b,...'"""
    P = _P(rows)
    mu = sp.Matrix([[sp.nsimplify(x, rational=True) for x in str(start).split(",")]])
    return (mu * P ** int(n))[0, int(j)]


def pm_mc_reward(rows, rewards):
    """long-run average reward per step: sum over states of stationary probability times reward"""
    P = _P(rows); r = [sp.nsimplify(x, rational=True) for x in str(rewards).split(",")]
    return sum(pm_mc_stationary(rows, j) * r[j] for j in range(P.shape[0]))


def pm_sphere_angle(lat1, lon1, lat2, lon2):
    """central angle in degrees between two points given by latitude and longitude in degrees, from the dot product"""
    d = sp.pi / 180
    v = lambda la, lo: sp.Matrix([sp.cos(la * d) * sp.cos(lo * d), sp.cos(la * d) * sp.sin(lo * d), sp.sin(la * d)])  # noqa: E731
    return sp.acos(v(sp.nsimplify(lat1), sp.nsimplify(lon1)).dot(v(sp.nsimplify(lat2), sp.nsimplify(lon2)))) / d


FUNCS = {k: v for k, v in globals().items() if k.startswith("pm_") and callable(v)}
