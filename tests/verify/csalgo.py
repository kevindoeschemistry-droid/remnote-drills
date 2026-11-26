"""Computer science drills (drills/problems/cs-*.yaml): the verifier's own implementations of the
algorithms the cards trace. Answers on the cards are worked by hand; these recompute them.
Graphs are written as "a-b:3 b-c:1" (undirected, weight after the colon, default 1) or with ">" for
a directed edge; neighbours are always taken in alphabetical order.
"""
import heapq
import ipaddress
from itertools import combinations

import sympy as sp


def _ints(v):
    return [int(t) for t in v.split()] if isinstance(v, str) else [int(t) for t in v]


def _edges(spec):
    out = []
    for tok in spec.split():
        w = 1
        if ":" in tok:
            tok, w = tok.split(":")
            w = int(w)
        if ">" in tok:
            a, b = tok.split(">")
            out.append((a, b, w, True))
        else:
            a, b = tok.split("-")
            out.append((a, b, w, False))
    return out


def _adj(spec):
    adj = {}
    for a, b, w, directed in _edges(spec):
        adj.setdefault(a, []).append((b, w))
        adj.setdefault(b, [])
        if not directed:
            adj[b].append((a, w))
    for k in adj:
        adj[k].sort()
    return adj


def bfs_order(spec, src):
    adj, seen, q, out = _adj(spec), {src}, [src], []
    while q:
        v = q.pop(0)
        out.append(v)
        for u, _ in adj[v]:
            if u not in seen:
                seen.add(u)
                q.append(u)
    return "".join(out)


def dfs_order(spec, src):
    adj, seen, out = _adj(spec), set(), []

    def go(v):
        seen.add(v)
        out.append(v)
        for u, _ in adj[v]:
            if u not in seen:
                go(u)
    go(src)
    return "".join(out)


def topo_order(spec):
    """Kahn's algorithm, always taking the alphabetically smallest ready vertex"""
    adj = _adj(spec)
    indeg = {v: 0 for v in adj}
    for v in adj:
        for u, _ in adj[v]:
            indeg[u] += 1
    ready = sorted(v for v in adj if indeg[v] == 0)
    out = []
    while ready:
        v = ready.pop(0)
        out.append(v)
        for u, _ in adj[v]:
            indeg[u] -= 1
            if indeg[u] == 0:
                ready.append(u)
                ready.sort()
    return "".join(out)


def dijkstra(spec, src, dst):
    adj, dist, pq = _adj(spec), {src: 0}, [(0, src)]
    while pq:
        d, v = heapq.heappop(pq)
        if d > dist.get(v, 1e18):
            continue
        for u, w in adj[v]:
            if d + w < dist.get(u, 1e18):
                dist[u] = d + w
                heapq.heappush(pq, (d + w, u))
    return dist[dst]


def mst_weight(spec):
    """Kruskal with a union-find"""
    parent = {}

    def find(v):
        parent.setdefault(v, v)
        while parent[v] != v:
            v = parent[v]
        return v
    total = 0
    for a, b, w, _ in sorted(_edges(spec), key=lambda e: e[2]):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            total += w
    return total


def bst_order(keys, kind):
    """keys inserted in order into an empty BST; kind 'in', 'pre' or 'post'"""
    keys = _ints(keys)
    root = None
    for k in keys:
        node, slot = root, None
        if root is None:
            root = [k, None, None]
            continue
        while node:
            slot = 1 if k < node[0] else 2
            if node[slot] is None:
                node[slot] = [k, None, None]
                break
            node = node[slot]
    out = []

    def walk(n):
        if n is None:
            return
        if kind == "pre":
            out.append(n[0])
        walk(n[1])
        if kind == "in":
            out.append(n[0])
        walk(n[2])
        if kind == "post":
            out.append(n[0])
    walk(root)
    return " ".join(map(str, out))


def heap_after(keys, extracts=0):
    """min-heap array after inserting keys one by one (sift up), then extract-min `extracts` times"""
    h = []
    for k in _ints(keys):
        h.append(k)
        i = len(h) - 1
        while i > 0 and h[(i - 1) // 2] > h[i]:
            h[(i - 1) // 2], h[i] = h[i], h[(i - 1) // 2]
            i = (i - 1) // 2
    for _ in range(int(extracts)):
        h[0] = h[-1]
        h.pop()
        i = 0
        while True:
            l, r, m = 2 * i + 1, 2 * i + 2, i
            if l < len(h) and h[l] < h[m]:
                m = l
            if r < len(h) and h[r] < h[m]:
                m = r
            if m == i:
                break
            h[i], h[m] = h[m], h[i]
            i = m
    return " ".join(map(str, h))


def probe_table(keys, m, mode):
    """slot of each key: h(k) = k mod m; mode 'linear' or 'double' with h2(k) = 7 - (k mod 7);
    returns the table as m entries, '-' for empty"""
    t = ["-"] * int(m)
    m = int(m)
    for k in _ints(keys):
        step = 1 if mode == "linear" else 7 - (k % 7)
        i = k % m
        while t[i] != "-":
            i = (i + step) % m
        t[i] = str(k)
    return " ".join(t)


def huffman_bits(freqs):
    """total encoded bits = sum over merges of the merged weight"""
    h = _ints(freqs)
    heapq.heapify(h)
    total = 0
    while len(h) > 1:
        a, b = heapq.heappop(h), heapq.heappop(h)
        total += a + b
        heapq.heappush(h, a + b)
    return total


def lcs(a, b):
    best = 0
    for k in range(min(len(a), len(b)), 0, -1):
        for idx in combinations(range(len(a)), k):
            sub = "".join(a[i] for i in idx)
            it = iter(b)
            if all(c in it for c in sub):
                return k
    return best


def edit_distance(a, b):
    @__import__("functools").lru_cache(None)
    def d(i, j):
        if i == 0 or j == 0:
            return i + j
        return min(d(i - 1, j) + 1, d(i, j - 1) + 1, d(i - 1, j - 1) + (a[i - 1] != b[j - 1]))
    return d(len(a), len(b))


def knapsack(items, cap):
    """items 'w:v w:v …'; brute force over subsets"""
    its = [tuple(map(int, t.split(":"))) for t in items.split()]
    best = 0
    for r in range(len(its) + 1):
        for c in combinations(its, r):
            if sum(w for w, _ in c) <= int(cap):
                best = max(best, sum(v for _, v in c))
    return best


def coin_ways(coins, n):
    """number of multisets of coins summing to n, by enumeration"""
    cs = sorted(_ints(coins))
    n = int(n)

    def ways(i, left):
        if left == 0:
            return 1
        if i == len(cs):
            return 0
        return sum(ways(i + 1, left - k * cs[i]) for k in range(left // cs[i] + 1))
    return ways(0, n)


def page_faults(refs, frames, alg):
    """refs as a string of digits; alg 'fifo', 'lru' or 'opt'"""
    mem, faults, frames = [], 0, int(frames)
    for t, r in enumerate(refs):
        if r in mem:
            if alg == "lru":
                mem.remove(r)
                mem.append(r)
            continue
        faults += 1
        if len(mem) < frames:
            mem.append(r)
            continue
        if alg in ("fifo", "lru"):
            mem.pop(0)
        else:
            future = refs[t + 1:]
            victim = max(mem, key=lambda p: future.index(p) if p in future else 10 ** 9)
            mem.remove(victim)
        mem.append(r)
    return faults


def avg_wait(procs, alg, q=2):
    """procs 'arrival:burst …' named P1, P2 …; alg 'fcfs', 'sjf' (non-preemptive), 'srtf' or 'rr'
    (quantum q); simulated one time unit at a time. Returns the average waiting time."""
    ps = [tuple(map(int, p.split(":"))) for p in procs.split()]
    n, left, done, t = len(ps), [b for _, b in ps], [None] * len(ps), 0
    queue, running, slice_left, order_seen = [], None, 0, set()
    while None in done:
        for i, (a, _) in enumerate(ps):
            if a == t and i not in order_seen:
                order_seen.add(i)
                queue.append(i)
        if alg == "rr" and running is not None and slice_left == 0:
            queue.append(running)
            running = None
        if running is None or alg == "srtf":
            cand = queue + ([running] if running is not None else [])
            if cand:
                if alg in ("fcfs", "rr"):
                    pick = running if running is not None else queue[0]
                else:
                    pick = min(cand, key=lambda i: (left[i], ps[i][0], i))
                if running is not None and pick != running:
                    queue.append(running)
                if pick in queue:
                    queue.remove(pick)
                if pick != running:
                    slice_left = q
                running = pick
        if running is not None:
            left[running] -= 1
            slice_left -= 1
            if left[running] == 0:
                done[running] = t + 1
                running = None
        t += 1
    return sp.Rational(sum(done[i] - ps[i][0] - ps[i][1] for i in range(n)), n)


def kmp_table(p):
    """the failure function: longest proper prefix that is also a suffix, for each prefix"""
    return " ".join(str(max([k for k in range(i + 1) if p[:k] == p[i + 1 - k:i + 1] and k <= i] or [0])) for i in range(len(p)))


def cidr_hosts(net):
    n = ipaddress.ip_network(net, strict=False)
    return max(n.num_addresses - 2, 0)


def lpm(table, ip):
    """table 'prefix=port …'; the port of the longest matching prefix"""
    addr = ipaddress.ip_address(ip)
    best = None
    for tok in table.split():
        p, port = tok.split("=")
        net = ipaddress.ip_network(p)
        if addr in net and (best is None or net.prefixlen > best[0]):
            best = (net.prefixlen, port)
    return best[1]


def closure(attrs, fds):
    """fds 'AB>C C>D …'"""
    got = set(attrs)
    rules = [tuple(f.split(">")) for f in fds.split()]
    changed = True
    while changed:
        changed = False
        for l, r in rules:
            if set(l) <= got and not set(r) <= got:
                got |= set(r)
                changed = True
    return "".join(sorted(got))


def candidate_keys(rel, fds):
    keys = []
    for r in range(1, len(rel) + 1):
        for c in combinations(sorted(rel), r):
            if closure(c, fds) == "".join(sorted(rel)) and not any(set(k) <= set(c) for k in keys):
                keys.append("".join(c))
    return " ".join(keys)


def powmod(b, e, m):
    return sp.Integer(pow(int(b), int(e), int(m)))


def pick(value, options):
    hits = [i for i, o in enumerate(options) if str(o) == str(value)]
    if len(hits) != 1:
        raise ValueError(f"value {value!r} not uniquely among {options}")
    return hits[0]


FUNCS = {f.__name__: f for f in [bfs_order, dfs_order, topo_order, dijkstra, mst_weight, bst_order, heap_after,
                                  probe_table, huffman_bits, lcs, edit_distance, knapsack, coin_ways, page_faults,
                                  avg_wait, kmp_table, cidr_hosts, lpm, closure, candidate_keys, pick, powmod]}
FUNCS.update({"binomial": sp.binomial, "factorial": sp.factorial, "floor": sp.floor, "sympify": sp.sympify, "mod_inverse": sp.mod_inverse})


# ── CS depth (Nov 2026): each recomputes a card's trace by brute force or direct simulation ──────────────────────
def cs_equiv(f, g, names="p q r"):
    """1 when two Python boolean formulas (and/or/not, '<=' for implication on bools) agree on every row"""
    vs = names.split()
    from itertools import product as _prod
    return int(all(bool(eval(f, {}, dict(zip(vs, row)))) == bool(eval(g, {}, dict(zip(vs, row))))
                   for row in _prod([False, True], repeat=len(vs))))


def cs_graph_kind(spec):
    """0 tree, 1 bipartite with a cycle, 2 not bipartite (odd cycle); undirected, connected"""
    adj = _adj(spec)
    n, m = len(adj), len(_edges(spec))
    colour, stack = {}, []
    for s0 in sorted(adj):
        if s0 in colour: continue
        colour[s0] = 0; stack = [s0]
        while stack:
            v = stack.pop()
            for u, _ in adj[v]:
                if u not in colour:
                    colour[u] = 1 - colour[v]; stack.append(u)
                elif colour[u] == colour[v]:
                    return 2
    return 0 if m == n - 1 else 1


def cs_uf(n, unions):
    """parent array after 'a-b c-d …' with union by rank (ties: second root under first) and path compression on find"""
    par, rank = list(range(int(n))), [0] * int(n)

    def find(x):
        root = x
        while par[root] != root: root = par[root]
        while par[x] != root: par[x], x = root, par[x]
        return root
    for tok in unions.split():
        a, b = (int(t) for t in tok.split("-"))
        ra, rb = find(a), find(b)
        if ra == rb: continue
        if rank[ra] < rank[rb]: par[ra] = rb
        elif rank[ra] > rank[rb]: par[rb] = ra
        else: par[rb] = ra; rank[ra] += 1
    return " ".join(str(v) for v in par)


def cs_bellman(spec, src, dst):
    """shortest distance on a directed weighted graph, or 'neg' if a negative cycle is reachable"""
    E = [(a, b, w) for a, b, w, d in _edges(spec)] + [(b, a, w) for a, b, w, d in _edges(spec) if not d]
    V = {x for e in E for x in e[:2]}
    dist = {v: float("inf") for v in V}; dist[src] = 0
    for _ in range(len(V) - 1):
        for a, b, w in E:
            if dist[a] + w < dist[b]: dist[b] = dist[a] + w
    if any(dist[a] + w < dist[b] for a, b, w in E): return "neg"
    return sp.Integer(dist[dst])


def cs_interval(ivs):
    """most non-overlapping intervals 's-e …' by brute force over subsets"""
    I = [tuple(int(t) for t in tok.split("-")) for tok in ivs.split()]
    best = 0
    for r in range(len(I) + 1):
        for c in combinations(I, r):
            c = sorted(c)
            if all(c[k][1] <= c[k + 1][0] for k in range(len(c) - 1)): best = max(best, r)
    return sp.Integer(best)


def cs_min_coins(coins, n):
    INF = 10 ** 9
    best = [0] + [INF] * int(n)
    for v in range(1, int(n) + 1):
        best[v] = min([best[v - c] + 1 for c in _ints(coins) if c <= v] + [INF])
    return sp.Integer(best[int(n)])


def cs_greedy_coins(coins, n):
    k, left = 0, int(n)
    for c in sorted(_ints(coins), reverse=True):
        k += left // c; left %= c
    return sp.Integer(k)


def cs_maxflow(spec, s, t):
    """max flow by brute-force augmenting on a capacity matrix (DFS paths), directed edges 'a>b:c'"""
    cap = {}
    for a, b, w, d in _edges(spec):
        cap[(a, b)] = cap.get((a, b), 0) + w; cap.setdefault((b, a), 0)
    V = sorted({x for e in cap for x in e})
    flow = 0
    while True:
        prev, q = {s: None}, [s]
        while q and t not in prev:
            v = q.pop(0)
            for u in V:
                if u not in prev and cap.get((v, u), 0) > 0:
                    prev[u] = v; q.append(u)
        if t not in prev: return sp.Integer(flow)
        path, v = [], t
        while prev[v] is not None: path.append((prev[v], v)); v = prev[v]
        f = min(cap[e] for e in path)
        for a, b in path: cap[(a, b)] -= f; cap[(b, a)] += f
        flow += f


def cs_serial(sched):
    """1 when a schedule 'r1(A) w2(A) …' is conflict-serializable (precedence graph acyclic)"""
    ops = [(int(tok[1]), tok[0], tok[3]) for tok in sched.split()]
    E = set()
    for i, (t1, a1, x1) in enumerate(ops):
        for t2, a2, x2 in ops[i + 1:]:
            if t1 != t2 and x1 == x2 and "w" in (a1, a2): E.add((t1, t2))
    T = sorted({o[0] for o in ops})
    from itertools import permutations
    return int(any(all(order.index(a) < order.index(b) for a, b in E) for order in permutations(T)))


def cs_nf(rel, fds):
    """highest normal form among 2 (2NF), 3 (3NF), 4 (BCNF); 1 when not even 2NF. FDs 'AB>C …', single-letter attributes"""
    keys = candidate_keys(rel, fds).split()
    prime = set("".join(keys))
    full = "".join(sorted(rel))
    rules = [tuple(f.split(">")) for f in fds.split()]
    nontriv = [(l, a) for l, r in rules for a in r if a not in l]
    if all(closure(l, fds) == full for l, a in nontriv): return sp.Integer(4)
    if all(closure(l, fds) == full or a in prime for l, a in nontriv): return sp.Integer(3)
    partial = any(a not in prime and any(set(l) < set(k) for k in keys) for l, a in nontriv)
    return sp.Integer(1 if partial else 2)


def cs_cache_hits(addrs, block, sets, ways):
    """hits of an LRU set-associative cache on byte addresses"""
    S = [[] for _ in range(int(sets))]
    hits = 0
    for a in _ints(addrs):
        blk = a // int(block); s = S[blk % int(sets)]
        if blk in s: hits += 1; s.remove(blk)
        elif len(s) == int(ways): s.pop(0)
        s.append(blk)
    return sp.Integer(hits)


def cs_banker(avail, mx, alloc):
    """1 when the state is safe; vectors space-separated, processes separated by '|'"""
    av = _ints(avail)
    M = [_ints(r) for r in mx.split("|")]; A = [_ints(r) for r in alloc.split("|")]
    from itertools import permutations
    for order in permutations(range(len(M))):
        w, ok = av[:], True
        for i in order:
            if any(M[i][k] - A[i][k] > w[k] for k in range(len(w))): ok = False; break
            w = [w[k] + A[i][k] for k in range(len(w))]
        if ok: return 1
    return 0


def cs_perm(mode, cls, op):
    """1 when a user of class 0 owner / 1 group / 2 other may do op 0 read / 1 write / 2 execute under octal mode"""
    digit = int(str(mode)[int(cls)])
    return int(bool(digit & (4 >> int(op))))


def cs_cwnd(events, ssthresh):
    """TCP Reno cwnd (in MSS) after per-RTT events: 'a' a round of ACKs (doubling below ssthresh, capped at it; +1 at
    or above), 't' timeout (ssthresh = cwnd/2, cwnd = 1), 'd' triple duplicate ACK (ssthresh = cwnd/2, cwnd = ssthresh)"""
    cw, th = 1, int(ssthresh)
    for e in events.split():
        if e == "a":
            cw = min(2 * cw, th) if cw < th else cw + 1
        elif e == "t": th = max(cw // 2, 2); cw = 1
        elif e == "d": th = max(cw // 2, 2); cw = th
    return sp.Integer(cw)


def cs_firewall(rules, pkt):
    """first matching rule's action; rules 'allow:tcp:80 deny:tcp:* allow:udp:53 …', packet 'tcp:443'; default deny"""
    proto, port = pkt.split(":")
    for r in rules.split():
        act, p, q = r.split(":")
        if p in (proto, "*") and q in (port, "*"): return int(act == "allow")
    return 0


def cs_kanon(rows, cols):
    """k of a table given rows 'a,b,c;…' and the indices of the quasi-identifier columns '0 1'"""
    from collections import Counter
    R = [r.split(",") for r in rows.split(";")]
    ix = _ints(cols)
    return sp.Integer(min(Counter(tuple(r[i] for i in ix) for r in R).values()))


def cs_lamport(procs, target):
    """Lamport clock of an event. procs 'a1 s:m1 a2|r:m1 b1' per process, events: plain name, send 's:msg', receive 'r:msg'.
    target is an event name or 's:msg'/'r:msg'. Simulated until stable."""
    P = [p.split() for p in procs.split("|")]
    sent, clock = {}, {}
    pos, c = [0] * len(P), [0] * len(P)
    progress = True
    while progress:
        progress = False
        for i, evs in enumerate(P):
            while pos[i] < len(evs):
                e = evs[pos[i]]
                if e.startswith("r:"):
                    if e[2:] not in sent: break
                    c[i] = max(c[i], sent[e[2:]]) + 1
                else:
                    c[i] += 1
                    if e.startswith("s:"): sent[e[2:]] = c[i]
                clock[e] = c[i]; pos[i] += 1; progress = True
    return sp.Integer(clock[target])


def cs_admissible(spec, h, goal):
    """1 when heuristic 'a=3 b=2 …' never exceeds the true distance to goal on the undirected graph"""
    hs = {k: int(v) for k, v in (t.split("=") for t in h.split())}
    return int(all(hs[v] <= dijkstra(spec, v, goal) for v in hs))


def cs_failure(p):
    """KMP failure function by brute force over every border, written apart from kmp_table"""
    out = []
    for i in range(1, len(p) + 1):
        s = p[:i]
        out.append(max(k for k in range(i) if s[:k] == s[i - k:]))
    return " ".join(str(v) for v in out)


FUNCS.update({f.__name__: f for f in [cs_equiv, cs_graph_kind, cs_uf, cs_bellman, cs_interval, cs_min_coins, cs_greedy_coins,
                                      cs_maxflow, cs_serial, cs_nf, cs_cache_hits, cs_banker, cs_perm, cs_cwnd, cs_firewall,
                                      cs_kanon, cs_lamport, cs_admissible, cs_failure]})


def cs_count_div(N, a, b):
    return sp.Integer(sum(1 for k in range(1, int(N) + 1) if k % int(a) == 0 or k % int(b) == 0))


def cs_avl_root(keys):
    """root key after inserting keys into an AVL tree (recursive insert, rebalance on the way up)"""
    def h(t): return t[3] if t else 0
    def mk(k, l, r): return (k, l, r, 1 + max(h(l), h(r)))
    def rot_r(t):
        k, l, r, _ = t; return mk(l[0], l[1], mk(k, l[2], r))
    def rot_l(t):
        k, l, r, _ = t; return mk(r[0], mk(k, l, r[1]), r[2])
    def ins(t, x):
        if not t: return mk(x, None, None)
        k, l, r, _ = t
        t = mk(k, ins(l, x), r) if x < k else mk(k, l, ins(r, x))
        k, l, r, _ = t
        bal = h(l) - h(r)
        if bal > 1:
            if x > l[0]: t = mk(k, rot_l(l), r)
            return rot_r(t)
        if bal < -1:
            if x < r[0]: t = mk(k, l, rot_r(r))
            return rot_l(t)
        return t
    t = None
    for x in _ints(keys): t = ins(t, x)
    return sp.Integer(t[0])


def cs_uf_sets(n, unions):
    roots = set()
    par = list(range(int(n)))
    def f(x):
        while par[x] != x: x = par[x]
        return x
    for tok in unions.split():
        a, b = (int(t) for t in tok.split("-"))
        ra, rb = f(a), f(b)
        if ra != rb: par[rb] = ra
    return sp.Integer(len({f(x) for x in range(int(n))}))


def cs_inversions(xs):
    v = _ints(xs)
    return sp.Integer(sum(1 for i in range(len(v)) for j in range(i + 1, len(v)) if v[i] > v[j]))


def cs_topo_count(spec):
    from itertools import permutations
    adj = _adj(spec)
    E = [(a, b) for a in adj for b, _ in adj[a]]
    return sp.Integer(sum(1 for o in permutations(sorted(adj)) if all(o.index(a) < o.index(b) for a, b in E)))


def cs_dijkstra_order(spec, src):
    """settle order by brute force: repeatedly take the unsettled vertex with the smallest true distance (ties alphabetical)"""
    V = sorted(_adj(spec))
    d = {v: dijkstra(spec, src, v) for v in V}
    return "".join(sorted(V, key=lambda v: (d[v], v)))


def _rows(t): return [r.split(",") for r in t.split(";")]


def cs_join(R, S):
    """natural join size, R's last column against S's first"""
    return sp.Integer(sum(1 for r in _rows(R) for s in _rows(S) if r[-1] == s[0]))


def cs_proj_count(R, col):
    return sp.Integer(len({r[int(col)] for r in _rows(R)}))


def cs_lossless(r1, r2, fds):
    common = "".join(sorted(set(r1) & set(r2)))
    c = set(closure(common, fds)) if common else set()
    return int(set(r1) <= c or set(r2) <= c)


def cs_rv(prog, reg):
    """value of register after a tiny RISC-V program 'addi x1,x0,5; slli x2,x1,2; …' (64-bit signed)"""
    R = [0] * 32
    for ins in prog.split(";"):
        ins = ins.strip()
        if not ins: continue
        op, args = ins.split(None, 1)
        a = [t.strip() for t in args.split(",")]
        d = int(a[0][1:])
        x = R[int(a[1][1:])]
        y = int(a[2]) if op.endswith("i") else R[int(a[2][1:])]
        if op.startswith("add"): v = x + y
        elif op == "sub": v = x - y
        elif op.startswith("sll"): v = x << y
        elif op.startswith("srl"): v = (x % (1 << 64)) >> y
        elif op.startswith("and"): v = x & y
        elif op.startswith("or"): v = x | y
        elif op.startswith("xor"): v = x ^ y
        else: raise ValueError(op)
        if d: R[d] = ((v + (1 << 63)) % (1 << 64)) - (1 << 63)
    return sp.Integer(R[int(str(reg).lstrip("x"))])


def cs_interleave(sched):
    """shared counter from 0; steps 'L1 L2 A1 S1 …' (load to a private register, add one, store back)"""
    mem, reg = 0, {}
    for st in sched.split():
        k, t = st[0], st[1:]
        if k == "L": reg[t] = mem
        elif k == "A": reg[t] += 1
        elif k == "S": mem = reg[t]
    return sp.Integer(mem)


def cs_sem(init, ops):
    """counting semaphore value after 'P P V …' where P decrements (negative = number waiting) and V increments"""
    return sp.Integer(int(init) - ops.split().count("P") + ops.split().count("V"))


def cs_has_cycle(spec):
    adj = _adj(spec)
    return int(len(topo_order(spec)) < len(adj))


def cs_chmod(sym):
    """'u=rwx,g=rx,o=' to its octal digits"""
    out = {"u": 0, "g": 0, "o": 0}
    for part in sym.split(","):
        who, perms = part.split("=")
        out[who] = sum({"r": 4, "w": 2, "x": 1}[c] for c in perms)
    return sp.Integer(100 * out["u"] + 10 * out["g"] + out["o"])


FUNCS.update({f.__name__: f for f in [cs_count_div, cs_avl_root, cs_uf_sets, cs_inversions, cs_topo_count, cs_dijkstra_order,
                                      cs_join, cs_proj_count, cs_lossless, cs_rv, cs_interleave, cs_sem, cs_has_cycle, cs_chmod]})


def cs_vc_rel(a, b):
    """0 when vector clock a happened before b, 1 when b before a, 2 when concurrent"""
    A, B = _ints(a), _ints(b)
    if all(x <= y for x, y in zip(A, B)) and A != B: return 0
    if all(y <= x for x, y in zip(A, B)) and A != B: return 1
    return 2


def cs_ring(nodes, h):
    """consistent hashing: the first node position at or after h on a ring of node positions (wrapping)"""
    ps = sorted(_ints(nodes))
    for p in ps:
        if p >= int(h): return sp.Integer(p)
    return sp.Integer(ps[0])


def cs_kmeans1d(pts, c1, c2):
    """new first centroid after one assignment step (ties go to the first centroid)"""
    P = [sp.nsimplify(t) for t in pts.split()]
    a, b = sp.nsimplify(c1), sp.nsimplify(c2)
    mine = [p for p in P if abs(p - a) <= abs(p - b)]
    return sum(mine) / len(mine)


FUNCS.update({f.__name__: f for f in [cs_vc_rel, cs_ring, cs_kmeans1d]})


def check(p, H):
    """the CS cards are problems as data, checked by data.py with the functions above"""
    return None
