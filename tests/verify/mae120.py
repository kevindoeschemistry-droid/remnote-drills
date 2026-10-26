"""Exam-style MAE 120 drills: rebuild each answer independently.

concept          own truth table (second, independent entry)
laplace          sympy Laplacian of the field (Cartesian or cylindrical) is identically zero?
wall-compare     same q through series layers -> R ratio = ΔT ratio; R ∝ 1/k for equal L, A
series-parallel  solve the A | (B ∥ C) | D network numerically for random kA > kB > kC > kD
wall-point       dsolve T'' = 0 with the layer's face temperatures
rod-slab         Table 4.1 case 5 (restated); depth y by nsolve on the energy balance
two-spheres      two case-1 resistances in series across T1 - T2
pot              dsolve T'' = 0 with flux / convection / fixed boundary conditions
fd               symbolic energy balance on the node's cell from its faces
"""
import math
import random

import sympy as sp

TRUTH = {
    "rad-medium": False, "k-direction": False, "fin-eff-1": True, "fin-eta": False, "fin-linear": False,
    "wall-linear": True, "cyl-linear": False, "q-const-cyl": True, "flux-const-cyl": False,
    "insulation-always": False, "tau-large": True, "bi-small": True, "bi-large": False, "lc-sphere": True,
    "shape-k": True, "series-same-q": True, "biggest-drop": False, "steady-zero-storage": False,
    "laplace-cond": True, "fd-interior": True,
}


def close(a, b, rel=1e-6):
    return abs(a - b) <= rel * max(1.0, abs(b))


def check(p, H):
    meta = p.get("meta", {})
    kind = meta.get("mae")
    if kind is None:
        return None
    a = p["answer"]
    ans = a.get("correct")
    val = float(H.P(a["ref"])) if a["kind"] == "expression" else None

    if kind == "concept":
        return TRUTH[meta["id"]] == (ans == "True")

    if kind == "laplace":
        if meta["coord"] == "cart":
            x, y, z = sp.symbols("x y z")
            syms = {"x": x, "y": y, "z": z}
            T = meta["a"] * x**2 + meta["b"] * y**2 + meta["c"] * z**2
            for c, body in meta["cross"]:
                T += c * syms[body[0]] * syms[body[1]]
            lap = sp.diff(T, x, 2) + sp.diff(T, y, 2) + sp.diff(T, z, 2)
        else:
            r, z = sp.symbols("r z", positive=True)
            T = meta["A"] * r**2 + meta["B"] * z**2 + meta["C"] * r * z + meta["D"] * sp.log(r)
            lap = sp.diff(r * sp.diff(T, r), r) / r + sp.diff(T, z, 2)
        possible = sp.simplify(lap) == 0
        return possible == (ans == "Possible")

    if kind == "wall-compare":
        R1, R2 = meta["d1"], meta["d2"]  # R ∝ ΔT at equal q
        k1, k2 = 1 / R1, 1 / R2
        truth = {"R1>R2": R1 > R2, "R1<R2": R1 < R2, "k1>k2": k1 > k2, "k1<k2": k1 < k2}[meta["claim"]]
        return truth == (ans == "True")

    if kind == "series-parallel":
        rnd = random.Random(7)
        seen = set()
        for _ in range(30):
            kA, kB, kC, kD = sorted((rnd.uniform(0.1, 100) for _ in range(4)), reverse=True)
            w, h = 1.0, 1.0  # block width (x) and the half-height of B and C; A, D span 2h
            RA, RD = w / (kA * 2 * h), w / (kD * 2 * h)
            RB, RC = w / (kB * h), w / (kC * h)
            Rp = 1 / (1 / RB + 1 / RC)
            q = 1.0 / (RA + Rp + RD)
            dTp = q * Rp
            qA = qD = q
            qB, qC = dTp / RB, dTp / RC
            f = {"A": qA / (2 * h), "B": qB / h, "C": qC / h, "D": qD / (2 * h)}
            t = {
                "fA>fB": f["A"] > f["B"], "fB>fA": f["B"] > f["A"], "qB>qC": qB > qC, "qC>qB": qC > qB,
                "fC>fD": f["C"] > f["D"], "fD>fC": f["D"] > f["C"], "qA>qD": qA > qD * (1 + 1e-12),
                "qA=qD": math.isclose(qA, qD), "fB>fD": f["B"] > f["D"], "fA=fD": math.isclose(f["A"], f["D"]),
            }[meta["id"]]
            seen.add(t)
        return len(seen) == 1 and seen.pop() == (ans == "True")

    if kind == "wall-point":
        x = sp.Symbol("x")
        Tf = sp.Function("T")
        sol = sp.dsolve(Tf(x).diff(x, 2), Tf(x), ics={Tf(0): meta["Ta"], Tf(1): meta["Tb"]}).rhs
        return close(val, float(sol.subs(x, sp.nsimplify(meta["f"]))))

    if kind == "rod-slab":
        D, k = meta["D"], meta["k"]
        Rp = lambda yy: sp.log(8 * yy / (sp.pi * D)) / (2 * sp.pi * k)  # Table 4.1 case 5, per unit length
        if meta["variant"] == "R":
            return close(val, float(Rp(meta["y"])) * 1000)
        if meta["variant"] == "q":
            return close(val, meta["dT"] / float(Rp(meta["y"])))
        yy = sp.Symbol("y", positive=True)
        qgen = meta["qdot"] * sp.pi * D**2 / 4
        y_sol = sp.nsolve(meta["dT"] / Rp(yy) - qgen, yy, 0.3)
        return close(val, float(y_sol) * 1000)

    if kind == "two-spheres":
        D, z, k = meta["D"], meta["z"], meta["k"]
        S = 2 * sp.pi * D / (1 - D / (4 * z))  # Table 4.1 case 1
        R = 1 / (S * k)
        q = (meta["T1"] - meta["T2"]) / (2 * R)
        return close(val, float(q))

    if kind == "pot":
        y = sp.Symbol("y")
        C1, C2 = sp.symbols("C1 C2")
        T = C1 * y + C2  # general solution of T'' = 0
        qf, L, k, Tinf = meta["qf"], meta["L"], meta["k"], meta["Tinf"]
        eqs = [sp.Eq(-k * sp.diff(T, y).subs(y, 0), qf)]
        if meta["variant"] in ("T0fromTL", "h"):
            eqs.append(sp.Eq(T.subs(y, L), meta["TL"]))
        else:
            eqs.append(sp.Eq(-k * sp.diff(T, y).subs(y, L), meta["h"] * (T.subs(y, L) - Tinf)))
        s = sp.solve(eqs, [C1, C2])
        Ts = T.subs(s)
        if meta["variant"] == "h":
            hh = sp.Symbol("h")
            return close(val, float(sp.solve(sp.Eq(-k * sp.diff(Ts, y), hh * (meta["TL"] - Tinf)), hh)[0]))
        target = Ts.subs(y, 0) if meta["variant"] in ("T0", "T0fromTL") else Ts.subs(y, L)
        return close(val, float(target))

    if kind == "fd":
        Tn = sp.Symbol("Tn")
        total = 0
        for f in meta["faces"]:
            if f["kind"] == "cond":
                total += meta["k"] * sp.nsimplify(f["len"]) * (f["T"] - Tn) / sp.nsimplify(f["dist"])
            elif f["kind"] == "conv":
                ell = sp.nsimplify(f["len"])
                total += meta["h"] * ell * (meta["Tinf"] - Tn) + meta["hr"] * ell * (meta["Tsur"] - Tn)
        return close(val, float(sp.solve(sp.Eq(total, 0), Tn)[0]))

    return False
