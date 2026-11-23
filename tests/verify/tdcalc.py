"""Thermodynamics and statistical mechanics checks for td-depth.yaml, each by a route of its own:

vdW coexistence   equal chemical potential (G) of the two phases, solved with nsolve
fugacity          ln φ = ∫₀ᴾ (Z − 1)/P dP, integrated
B₂                −2πN_A ∫ (e^(−u/kT) − 1) r² dr, integrated
Gibbs–Duhem       d ln γ₂ = −(x₁/x₂) d ln γ₁, integrated from pure 2
flash             Rachford–Rice solved with nsolve
azeotrope         y₁ = x₁ from modified Raoult, nsolve
Ising             largest eigenvalue of the 2×2 transfer matrix
Maxwell speeds    moments of the speed distribution, integrated
Flory–Huggins     the critical point from the second and third derivatives of ΔG_mix
"""
import mpmath as mp
import sympy as sp

R_ = sp.Rational("1.380649e-23") * sp.Rational("6.02214076e23")


def check(p, H):
    """helpers only: data.py calls these through verify expressions"""
    return None


def N(v):
    return sp.nsimplify(v)


def homogeneous(expr):
    """1 if S(λU, λV, λN) = λS (first-order homogeneous), else 0"""
    U, V, n, lam = sp.symbols("U V N lam", positive=True)
    S = sp.sympify(expr, locals={"U": U, "V": V, "N": n})
    return 1 if sp.simplify(S.subs({U: lam * U, V: lam * V, n: lam * n}, simultaneous=True) - lam * S) == 0 else 0


def exact(Mx, Ny):
    x, y = sp.symbols("x y")
    M, Nn = sp.sympify(Mx, locals={"x": x, "y": y}), sp.sympify(Ny, locals={"x": x, "y": y})
    return 1 if sp.simplify(sp.diff(M, y) - sp.diff(Nn, x)) == 0 else 0


def isentropic_T2(T1, P1, P2, cp):
    """ideal gas, constant cp: solve cp ln(T2/T1) − R ln(P2/P1) = 0"""
    T2 = sp.Symbol("T2", positive=True)
    return sp.nsolve(N(cp) * sp.log(T2 / N(T1)) - R_ * sp.log(N(P2) / N(P1)), T2, N(T1), prec=20)


def vdw_reduced_unstable(Tr, Vr):
    """1 if (∂P/∂V)_T > 0 in the reduced vdW equation"""
    V = sp.Symbol("V")
    P = 8 * N(Tr) / (3 * V - 1) - 3 / V**2
    return 1 if sp.diff(P, V).subs(V, N(Vr)) > 0 else 0


def vdw_psat(Tr):
    """reduced saturation pressure: equal G of liquid and vapour roots, by nsolve on (Vl, Vg)"""
    mp.mp.dps = 30
    Tr = mp.mpf(str(Tr))
    P = lambda V: 8 * Tr / (3 * V - 1) - 3 / V**2  # noqa: E731
    # molar Helmholtz energy per reduced units (up to a function of T): A = −(8/3)Tr ln(3V − 1) − 3/V
    A = lambda V: -mp.mpf(8) / 3 * Tr * mp.log(3 * V - 1) - 3 / V  # noqa: E731
    G = lambda V: A(V) + P(V) * V  # noqa: E731
    # bisect on pressure: the liquid and vapour roots of the cubic must have equal G
    sv = sorted(r.real for r in mp.polyroots([4 * Tr, -9, 6, -1]) if abs(r.imag) < 1e-20 and r.real > mp.mpf(1) / 3)
    lo, hi = max(P(sv[0]), mp.mpf("1e-12")), P(sv[1])
    for _ in range(200):
        mid = (lo + hi) / 2
        r = sorted(z.real for z in mp.polyroots([3 * mid, -(mid + 8 * Tr), 9, -3], maxsteps=200, extraprec=60) if abs(z.imag) < 1e-15)
        # below Psat the vapour root has the lower G
        lo, hi = (mid, hi) if G(r[-1]) < G(r[0]) else (lo, mid)
    return sp.Float((lo + hi) / 2, 15)


def ln_phi_virial(B, P, T):
    """B in m³/mol, P in Pa"""
    Pp = sp.Symbol("Pp", positive=True)
    Z = 1 + N(B) * Pp / (R_ * N(T))
    return sp.exp(sp.integrate((Z - 1) / Pp, (Pp, 0, N(P))))


def b2_square_well(sigma, lam, eps_over_kT):
    """B₂ (m³/mol) of a square well: σ in m, well to λσ, depth ε"""
    r = sp.Symbol("r", positive=True)
    s, l, e = N(sigma), N(lam), N(eps_over_kT)
    inner = sp.integrate((0 - 1) * r**2, (r, 0, s))
    well = sp.integrate((sp.exp(e) - 1) * r**2, (r, s, l * s))
    return sp.N(-2 * sp.pi * sp.Rational("6.02214076e23") * (inner + well), 15)


def gamma2_from_margules(A, x1):
    """integrate Gibbs–Duhem from x1 = 0 for ln γ1 = A x2²"""
    t = sp.Symbol("t")
    lng1 = N(A) * (1 - t) ** 2
    integrand = -(t / (1 - t)) * sp.diff(lng1, t)
    return sp.N(sp.exp(sp.integrate(integrand, (t, 0, N(x1)))), 15)


def flash_vf(z1, K1, K2):
    """binary Rachford–Rice: Σ z_i(K_i − 1)/(1 + ψ(K_i − 1)) = 0"""
    psi = sp.Symbol("psi")
    z1, K1, K2 = N(z1), N(K1), N(K2)
    f = z1 * (K1 - 1) / (1 + psi * (K1 - 1)) + (1 - z1) * (K2 - 1) / (1 + psi * (K2 - 1))
    return sp.nsolve(f, psi, sp.Rational(1, 2), prec=20)


def azeotrope_x1(A, P1, P2):
    """one-parameter Margules: x1 where γ1P1 = γ2P2"""
    x = sp.Symbol("xa")
    A, P1, P2 = N(A), N(P1), N(P2)
    return sp.nsolve(A * (1 - x) ** 2 + sp.log(P1) - A * x**2 - sp.log(P2), x, sp.Rational(1, 2), prec=20)


def ising_ln_lambda(bJ, bh):
    beta_J, beta_h = N(bJ), N(bh)
    Tm = sp.Matrix([[sp.exp(beta_J + beta_h), sp.exp(-beta_J)], [sp.exp(-beta_J), sp.exp(beta_J - beta_h)]])
    return sp.N(sp.log(max(sp.N(e) for e in Tm.eigenvals())), 15)


def maxwell_speed(M, T, which):
    """which 0 most probable, 1 mean, 2 rms; M in kg/mol"""
    v = sp.Symbol("v", positive=True)
    m, Tt = N(M), N(T)
    a = m / (2 * R_ * Tt)
    f = 4 * sp.pi * (a / sp.pi) ** sp.Rational(3, 2) * v**2 * sp.exp(-a * v**2)
    if which == 0:
        return sp.N(sp.solve(sp.diff(f, v), v)[0], 15)
    if which == 1:
        return sp.N(sp.integrate(v * f, (v, 0, sp.oo)), 15)
    return sp.N(sp.sqrt(sp.integrate(v**2 * f, (v, 0, sp.oo))), 15)


def ho_classical_q(kT_over_hbar_omega):
    """∫∫ e^(−βH) dx dp / h for H = p²/2m + mω²x²/2, in units where ħω/kT is given"""
    x, p = sp.symbols("x p", real=True)
    b = 1 / N(kT_over_hbar_omega)  # βħω; take m = ω = ħ = 1 so h = 2π
    return sp.N(sp.integrate(sp.exp(-b * (p**2 / 2 + x**2 / 2)), (x, -sp.oo, sp.oo), (p, -sp.oo, sp.oo)) / (2 * sp.pi), 15)


def fh_chi_c(Nn):
    """Flory–Huggins critical χ for chain length N, from f'' = f''' = 0"""
    phi, chi = sp.symbols("phi chi", positive=True)
    Nn = N(Nn)
    f = phi / Nn * sp.log(phi) + (1 - phi) * sp.log(1 - phi) + chi * phi * (1 - phi)
    sol = sp.nsolve([sp.diff(f, phi, 2), sp.diff(f, phi, 3)], [phi, chi], [sp.N(1 / (1 + sp.sqrt(Nn))), 0.5], prec=20)
    return sol[1]


def ionic_strength(cs, zs):
    return sp.Rational(1, 2) * sum(N(c) * z**2 for c, z in zip(cs, zs))


FUNCS = {f.__name__: f for f in [homogeneous, exact, isentropic_T2, vdw_reduced_unstable, vdw_psat, ln_phi_virial, b2_square_well,
                                 gamma2_from_margules, flash_vf, azeotrope_x1, ising_ln_lambda, maxwell_speed, ho_classical_q, fh_chi_c,
                                 ionic_strength]}
FUNCS.update({"zip": zip, "loggamma": sp.loggamma})


def wsum(ws, xs, power=1):
    """Σ wᵢ xᵢ^power, weights and values given as lists (no comprehension, so eval scoping is moot)"""
    tot = 0
    for i in range(len(ws)):
        tot += sp.nsimplify(ws[i]) * sp.nsimplify(xs[i]) ** power
    return tot


def gibbs_S(ps):
    """−Σ p ln p over the listed probabilities"""
    tot = 0
    for q in ps:
        q = sp.nsimplify(q)
        tot -= q * sp.log(q)
    return tot


FUNCS.update({"wsum": wsum, "gibbs_S": gibbs_S})
