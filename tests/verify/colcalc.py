"""Colloids and DLVO theory, recomputed along routes the cards do not use.

The Debye length comes from a list of ions (concentration and valence), not from a stated ionic
strength; sphere interactions come from integrating the flat-plate energy per area through the
Derjaguin approximation; the DLVO barrier is found by bisection on a numerical derivative scanned
from the outside in, where the generator uses Newton's method on the analytic derivative.
"""
import mpmath as mp
import sympy as sp

mp.mp.dps = 30
E = mp.mpf("1.602176634e-19")
KB = mp.mpf("1.380649e-23")
NA = mp.mpf("6.02214076e23")
EPS0 = mp.mpf("8.8541878128e-12")
EPSR = mp.mpf("78.4")
T = mp.mpf("298.15")


def check(p, H_):
    return None


def col_debye_nm(ions):
    """κ⁻¹ in nm from 'c:z,c:z' (c in mM = mol/m³): κ² = e²N_A Σ c z² / (ε kT)"""
    if not isinstance(ions, str):
        ions = f"{ions}:1,{ions}:1"
    s = 0
    for part in ions.split(","):
        c, z = part.split(":")
        s += mp.mpf(c) * mp.mpf(z) ** 2
    kappa2 = E**2 * NA * s / (EPSR * EPS0 * KB * T)
    return sp.Float(1 / mp.sqrt(kappa2) * 1e9, 25)


def _plate_vdw(A, x):
    return -A / (12 * mp.pi * x**2)


def col_vdw_spheres_kt(A, R, D):
    """two equal spheres: Derjaguin F = π R w(D) with w the plate energy per area; W = ∫_D^∞ F"""
    A, R, D = mp.mpf(A), mp.mpf(R) * 1e-9, mp.mpf(D) * 1e-9
    W = mp.quad(lambda x: mp.pi * R * _plate_vdw(A, x), [D, mp.inf])
    return sp.Float(W / (KB * T), 25)


def col_edl_spheres_kt(R, psi_mV, ions, D):
    """weak-overlap, low-potential plates: w = 2εε0κψ0² e^{−κx}; spheres through Derjaguin as above"""
    R, D = mp.mpf(R) * 1e-9, mp.mpf(D) * 1e-9
    psi = mp.mpf(psi_mV) / 1000
    kappa = 1 / (mp.mpf(col_debye_nm(ions)) * 1e-9)
    w = lambda x: 2 * EPSR * EPS0 * kappa * psi**2 * mp.e ** (-kappa * x)
    W = mp.quad(lambda x: mp.pi * R * w(x), [D, mp.inf])
    return sp.Float(W / (KB * T), 25)


def _total(R, A, psi, kappa, D):
    return 2 * mp.pi * EPSR * EPS0 * R * psi**2 * mp.e ** (-kappa * D) - A * R / (12 * D)


def col_barrier_kt(R, A, psi_mV, ions):
    """height of the DLVO maximum: scan D from 50 Debye lengths inward, bracket the sign change of
    a central-difference slope, then bisect"""
    R, A, psi = mp.mpf(R) * 1e-9, mp.mpf(A), mp.mpf(psi_mV) / 1000
    lam = mp.mpf(col_debye_nm(ions)) * 1e-9
    kappa = 1 / lam
    f = lambda D: _total(R, A, psi, kappa, D)
    slope = lambda D: (f(D * (1 + mp.mpf("1e-12"))) - f(D * (1 - mp.mpf("1e-12")))) / (2 * D * mp.mpf("1e-12"))
    D, step = 50 * lam, lam / 50
    prev = slope(D)
    while D > lam / 1000:
        Dn = D - step
        s = slope(Dn)
        if prev < 0 <= s or prev <= 0 < s:
            lo, hi = Dn, D
            for _ in range(200):
                mid = (lo + hi) / 2
                if slope(mid) >= 0:
                    lo = mid
                else:
                    hi = mid
            return sp.Float(f((lo + hi) / 2) / (KB * T), 25)
        D, prev = Dn, s
    raise ValueError("no barrier")


def col_total_kt(R, A, psi_mV, ions, Dnm):
    return col_vdw_spheres_kt(A, R, Dnm) + col_edl_spheres_kt(R, psi_mV, ions, Dnm)


def col_zeta_mV(mob):
    """Smoluchowski from the force balance on the slipping plane: εζE/η = μE"""
    eta = mp.mpf("0.00089")
    return sp.Float(mp.mpf(mob) * 1e-8 * eta / (EPSR * EPS0) * 1000, 25)


def col_grahame(psi_mV, c_mM):
    """σ = sqrt(8 ε kT n∞) sinh(eψ/2kT), with n∞ in particles/m³; returns mC/m²"""
    n = mp.mpf(c_mM) * NA
    psi = mp.mpf(psi_mV) / 1000
    return sp.Float(mp.sqrt(8 * EPSR * EPS0 * KB * T * n) * mp.sinh(E * psi / (2 * KB * T)) * 1000, 25)


def col_stokes_einstein_um2s(a_nm, eta):
    """D = kT / f with the Stokes friction f = 6πηa; µm²/s"""
    f = 6 * mp.pi * mp.mpf(eta) * mp.mpf(a_nm) * 1e-9
    return sp.Float(KB * T / f * 1e12, 25)


def col_fast_halflife(n0, eta):
    """dN/dt = −k N² with k = 4kT/3η: integrate dN/(kN²) from N0/2 to N0"""
    k = 4 * KB * T / (3 * mp.mpf(eta))
    N0 = mp.mpf(n0)
    t = mp.quad(lambda N: 1 / (k * N**2), [N0 / 2, N0])
    return sp.Float(t, 25)


FUNCS = {f.__name__: f for f in [col_debye_nm, col_vdw_spheres_kt, col_edl_spheres_kt, col_barrier_kt, col_total_kt,
                                 col_zeta_mV, col_grahame, col_stokes_einstein_um2s, col_fast_halflife]}
