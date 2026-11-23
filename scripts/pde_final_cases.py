"""Builds drills/problems/pde-final.yaml: the cells of the 1-D PDE grid (drills/matrices/pde-1d.yaml)
that had no item. Run: python3 scripts/pde_final_cases.py

Answers follow the route the card teaches (closed-form coefficients, the residue at each pole,
the Thomas algorithm); tests/verify/pdecalc.py checks by integration, dsolve, quadrature and linear
solves instead.
"""
from pathlib import Path

import mpmath as mp
import yaml

mp.mp.dps = 30
OUT = Path(__file__).resolve().parent.parent / "drills/problems/pde-final.yaml"
T = []


def F(v):
    return float(mp.nstr(v, 12))


def tpl(name, skill, prompt, ask, explain, cases, verify, tol=0.0001, pace="quick"):
    T.append({"template": name, "skill": skill, "pace": pace, "cases": cases, "prompt": prompt,
              "parts": [{"ask": ask, "label": "y", "value": "ans", "tol": tol, "explain": explain}],
              "verify": {"expect": {"y": verify}}})


# ── a boundary value that changes in time: shift by w = x g(t)/L ──────────────
cases = []
for gtex, g, gp0, L, k, x in [("5t", "5*t", 5, 2, 1, 1), ("3t", "3*t", 3, 1, 0.5, 0.5), ("10(1 - e^{-t})", "10*(1 - exp(-t))", 10, 4, 2, 1),
                              ("2\\sin t", "2*sin(t)", 2, 3, 1, 2), ("100 + 4t", "100 + 4*t", 4, 5, 0.1, 2.5)]:
    F_ = -mp.mpf(x) / L * gp0  # w_xx = 0 for w linear in x
    cases.append({"gtex": gtex, "g": g, "L": L, "k": k, "xp": x, "ans": F(F_)})
tpl("pde-time-bc-shift", "pde.nonhomogeneous",
    "$u_t = {{k}}\\,u_{xx}$ on $0 < x < {{L}}$ with $u(0,t) = 0$ and $u({{L}},t) = {{gtex}}$. Shift by $w = x\\,g(t)/{{L}}$, so $v = u - w$ has zero ends and obeys $v_t = {{k}}v_{xx} + F(x,t)$. What is $F$ at $x = {{xp}}$, $t = 0$?",
    "F",
    "Substitute $u = v + w$: $v_t + w_t = k(v_{xx} + w_{xx})$, and $w_{xx} = 0$, so $F = -w_t = -\\dfrac{x}{L}g'(t)$. A moving boundary becomes a source inside, which is then expanded in the eigenfunctions (next card type)",
    cases, "shift_source(g, L, k, xp)")

# ── a heat source: steady state and the forcing on each mode ────────────────
cases = []
for Q, k, L, x, kind in [(10, 1, 2, 1, 0), (6, 2, 3, 1, 0), (100, 50, 0.1, 0.05, 0), (8, 1, 2, 2, 1), (20, 4, 1, 0.5, 1)]:
    if kind == 0:
        v = mp.mpf(Q) / (2 * k) * x * (L - x)
    else:
        v = mp.mpf(Q) / k * (L * x - x**2 / 2)
    cases.append({"Q": Q, "k": k, "L": L, "xp": x, "kind": kind, "bt": ["both ends held at 0", "x = 0 held at 0 and the end at x = L insulated"][kind], "ans": F(v)})
tpl("pde-source-steady", "pde.nonhomogeneous",
    "$u_t = {{k}}\\,u_{xx} + {{Q}}$ on $0 < x < {{L}}$ with {{bt}}. What is the steady-state temperature at $x = {{xp}}$?",
    "u_s",
    "Steady state: $k u_s'' = -Q$, a parabola. Both ends zero: $u_s = \\dfrac{Q}{2k}x(L - x)$, peak $QL^2/8k$ in the middle. Insulated at $L$: $u_s = \\dfrac{Q}{k}\\left(Lx - \\dfrac{x^2}{2}\\right)$, peak at the insulated end. Then $v = u - u_s$ is the source-free problem",
    cases, "source_steady(Q, k, L, xp, kind)")

cases = []
for Q, L, n, ftex, f in [(10, 1, 1, "10", "10"), (10, 1, 2, "10", "10"), (10, 1, 3, "10", "10"), (6, 2, 1, "6", "6"), (5, 3, 1, "5x", "5*x"), (5, 3, 2, "5x", "5*x")]:
    if f.isdigit():
        b = 2 * mp.mpf(Q) * (1 - (-1) ** n) / (n * mp.pi)
    else:
        b = 2 * 5 * L * (-1) ** (n + 1) / (n * mp.pi)
    if b == 0:
        continue
    cases.append({"Q": Q, "L": L, "n": n, "ftex": ftex, "f": f, "ans": F(b)})
tpl("pde-source-mode", "pde.nonhomogeneous",
    "$u_t = u_{xx} + q(x)$ on $0 < x < {{L}}$, ends at 0, with $q(x) = {{ftex}}$. Expanding $u = \\sum T_n(t)\\sin(n\\pi x/{{L}})$ gives $T_n' + (n\\pi/{{L}})^2 T_n = q_n$. What is $q_{ {{n}} }$?",
    "q_n",
    "Expand the source in the same eigenfunctions: $q_n = \\dfrac{2}{L}\\int_0^L q(x)\\sin\\dfrac{n\\pi x}{L}dx$. A constant source has only odd modes, $4Q/n\\pi$. Each $T_n$ then solves a first-order ODE: $T_n \\to q_n/(n\\pi/L)^2$ in the long run",
    cases, "sine_coef(f, L, n)")

# ── cylinder with a nonzero wall: shift by the wall temperature ─────────────
cases = []
for Ti, Tw, a, k, what in [(100, 20, 0.05, 1e-5, 0), (25, 200, 0.02, 4e-6, 0), (300, 50, 0.1, 1.2e-5, 1), (80, 0, 0.01, 1e-6, 1), (60, 10, 0.03, 2e-5, 0)]:
    al = mp.besseljzero(0, 1)
    if what == 0:
        v = 2 * mp.mpf(Ti - Tw) / (al * mp.besselj(1, al))
    else:
        v = mp.mpf(k) * (al / a) ** 2
    cases.append({"Ti": Ti, "Tw": Tw, "a": a, "a_mm": a * 1000, "k": k, "w": what,
                  "wt": ["the coefficient A₁ of J₀(α₁r/a) in the shifted solution", "the decay rate (s⁻¹) of the slowest mode"][what], "ans": F(v)})
T.append({"template": "pde-cylinder-wall", "skill": "pde.review-4", "pace": "quick", "cases": cases,
          "prompt": "A long cylinder of radius {{a_mm}} mm ($\\alpha = {{k}}$ m²/s) starts at ${{Ti}}$ °C and its wall is suddenly held at ${{Tw}}$ °C. With $u = T - T_w$ (zero at the wall), find {{wt}}. ($\\alpha_1 = 2.4048$, $J_1(\\alpha_1) = 0.5191$)",
          "parts": [{"ask": "Value", "label": "y", "value": "ans", "tol": 0.0001,
                     "explain": "Shift by the wall temperature so the wall condition is zero; the initial value becomes $T_i - T_w$. Then $u = \\sum A_n J_0(\\alpha_n r/a)e^{-\\alpha(\\alpha_n/a)^2t}$, and for a uniform start $A_n = \\dfrac{2(T_i - T_w)}{\\alpha_nJ_1(\\alpha_n)}$ (weight $r$ in the orthogonality integral). The slowest mode decays at $\\alpha(\\alpha_1/a)^2$"}],
          "verify": {"expect": {"y": "[bessel_coef(Ti - Tw, a), bessel_rate(k, a)][w]"}}})

# ── sphere: v = r u turns it into a rod ─────────────────────────────────────
cases = []
for U0, a, k, t, what, n in [(100, 1, 1, 0.1, 0, 1), (100, 1, 1, 0.1, 0, 2), (50, 2, 0.5, 0, 0, 1), (100, 1, 1, 0.05, 1, 0), (80, 0.5, 0.1, 0.2, 1, 0), (100, 1, 1, 0.0, 2, 0)]:
    if what == 0:
        v = 2 * a * mp.mpf(U0) * (-1) ** (n + 1) / (n * mp.pi)
    elif what == 1:
        v = sum(2 * a * mp.mpf(U0) * (-1) ** (m + 1) / (m * mp.pi) * (m * mp.pi / a) * mp.exp(-k * (m * mp.pi / a) ** 2 * t) for m in range(1, 60))
    else:
        v = mp.mpf(k) * (mp.pi / a) ** 2
    if what == 2:
        t = 0
    cases.append({"U0": U0, "a": a, "k": k, "t": t, "w": what, "n": n,
                  "wt": [f"the coefficient B_{n} in r·u = Σ Bₙ sin(nπr/a)e^(−k(nπ/a)²t)", "the centre temperature u(0, t) (sum the series)", "the decay rate of the slowest mode"][what], "ans": F(v)})
T.append({"template": "pde-sphere", "skill": "pde.review-4", "pace": "quick", "cases": cases,
          "prompt": "$u_t = {{k}}\\left(u_{rr} + \\tfrac{2}{r}u_r\\right)$ in a sphere of radius ${{a}}$, surface held at 0, initially ${{U0}}$ everywhere. At $t = {{t}}$, find {{wt}}.",
          "parts": [{"ask": "Value", "label": "y", "value": "ans", "tol": 0.0005,
                     "explain": "Put $v = ru$: the equation becomes $v_t = kv_{rr}$, a rod with $v(0) = 0$ (u finite) and $v(a) = 0$. So $v = \\sum B_n\\sin(n\\pi r/a)e^{-k(n\\pi/a)^2t}$ with $B_n = \\dfrac{2}{a}\\int_0^a rU_0\\sin\\dfrac{n\\pi r}{a}dr = \\dfrac{2aU_0(-1)^{n+1}}{n\\pi}$, and $u = v/r$; at the centre $\\sin(\\lambda r)/r \\to \\lambda$"}],
          "verify": {"expect": {"y": "[sphere_coef(U0, a, n), sphere_centre(U0, a, k, t), k*(pi/nsimplify(a))**2][w]"}}})

# ── Laplace transform: invert with infinitely many poles (residues) ─────────
cases = []
for L, x, n in [(1, 0.5, 1), (1, 0.25, 1), (2, 1, 1), (1, 0.5, 3), (2, 0.5, 2), (3, 1, 1)]:
    c = 2 * (-1) ** n / (n * mp.pi) * mp.sin(n * mp.pi * x / L)
    if abs(c) < 1e-12:
        continue
    cases.append({"L": L, "xp": x, "n": n, "ans": F(c)})
tpl("pde-lt-residues", "pde.laplace-transform",
    "$u_t = u_{xx}$, $u(0,t) = 0$, $u({{L}},t) = 1$, $u(x,0) = 0$ gives $U(x,s) = \\dfrac{\\sinh(\\sqrt s\\,x)}{s\\sinh(\\sqrt s\\,{{L}})}$. Invert by residues. At $x = {{xp}}$, what is the coefficient of $e^{-({{n}}\\pi/{{L}})^2 t}$?",
    "Coefficient",
    "Poles: $s = 0$ (residue $x/L$, the steady state) and $\\sqrt s = in\\pi/L$, i.e. $s_n = -(n\\pi/L)^2$, where $\\sinh(\\sqrt sL) = 0$. Each residue is $\\dfrac{2(-1)^n}{n\\pi}\\sin\\dfrac{n\\pi x}{L}e^{s_nt}$. Summing all residues rebuilds the separation-of-variables series: the poles are the eigenvalues",
    cases, "ramp_series_coef(L, xp, n)")

# ── finite differences: flux boundary by a ghost node; implicit and Crank–Nicolson ─
cases = []
for u0, u1, r, h, g in [(50, 60, 0.25, 0.1, 0), (50, 60, 0.4, 0.1, -20), (20, 18, 0.5, 0.05, 40), (100, 90, 0.3, 0.2, 10), (0, 5, 0.25, 0.1, -50)]:
    v = u0 + r * (2 * u1 - 2 * u0 - 2 * h * g)
    cases.append({"u0": u0, "u1": u1, "r": r, "h": h, "g": g, "ans": F(mp.mpf(v))})
tpl("pde-fd-ghost", "pde.review-5",
    "Explicit scheme for $u_t = u_{xx}$, $r = k/h^2 = {{r}}$, $h = {{h}}$, with the flux condition $u_x(0,t) = {{g}}$. Now $u_0 = {{u0}}$ and $u_1 = {{u1}}$. Using a ghost node, what is $u_0$ one step later?",
    "u₀ next",
    "Central difference at the boundary: $(u_1 - u_{-1})/2h = g$, so the ghost value is $u_{-1} = u_1 - 2hg$. Put it in the usual update: $u_0^{new} = u_0 + r(2u_1 - 2u_0 - 2hg)$. Insulated ($g = 0$) mirrors the first interior node",
    cases, "ghost_step(u0, u1, r, h, g)")

cases = []
for a, b, c, r, th in [(0, 100, 0, 1, 1), (50, 100, 50, 0.5, 1), (20, 40, 60, 1, 1), (0, 100, 0, 1, 0.5), (50, 100, 50, 2, 0.5), (10, 30, 10, 0.5, 0.5)]:
    rr, tt = mp.mpf(r), mp.mpf(th)
    old = [0, a, b, c, 0]
    rhs = [old[i] + rr * (1 - tt) * (old[i - 1] - 2 * old[i] + old[i + 1]) for i in (1, 2, 3)]
    lo, di, up = -rr * tt, 1 + 2 * rr * tt, -rr * tt  # Thomas algorithm
    cp, dp = [0] * 3, [0] * 3
    cp[0], dp[0] = up / di, rhs[0] / di
    for i in (1, 2):
        m = di - lo * cp[i - 1]
        cp[i] = up / m
        dp[i] = (rhs[i] - lo * dp[i - 1]) / m
    x3 = dp[2]
    x2 = dp[1] - cp[1] * x3
    cases.append({"a": a, "b": b, "c": c, "r": r, "th": th, "nm": ["", "", ""][0], "sch": "backward Euler (fully implicit)" if th == 1 else "Crank–Nicolson", "ans": F(x2)})
tpl("pde-fd-implicit", "pde.review-5",
    "$u_t = u_{xx}$ with ends held at 0 and three interior nodes at ${{a}}, {{b}}, {{c}}$. Take one {{sch}} step with $r = {{r}}$. What is the new middle value?",
    "Middle node",
    "Implicit: $-r\\theta u_{i-1}^{new} + (1 + 2r\\theta)u_i^{new} - r\\theta u_{i+1}^{new} = u_i + r(1 - \\theta)(u_{i-1} - 2u_i + u_{i+1})$, with θ = 1 (backward Euler) or ½ (Crank–Nicolson). That is a tridiagonal system, solved by elimination (Thomas). Both are stable for any r; explicit needs r ≤ ½",
    cases, "implicit_mid(a, b, c, r, th)")


def dump():
    for t in T:
        for c in t["cases"]:
            c.pop("nm", None)
    head = "# " + "\n# ".join(__doc__.strip().splitlines()) + "\n# GENERATED: edit scripts/pde_final_cases.py, not this file.\n\n"
    OUT.write_text(head + yaml.dump(T, allow_unicode=True, sort_keys=False, width=1000, default_flow_style=None))
    print(f"{len(T)} templates, {sum(len(t['cases']) for t in T)} cases -> {OUT}")


if __name__ == "__main__":
    dump()
