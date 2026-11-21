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


def check(p, H):
    """the CS cards are problems as data, checked by data.py with the functions above"""
    return None
