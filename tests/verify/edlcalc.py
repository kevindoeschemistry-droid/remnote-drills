"""Independent checks for drills/problems/el-edl.yaml (framework electric-double-layers, EL; Petsev, van Swol
and Frink 2021). The cards use closed forms; these go back to the integral or the equation they come from."""
import mpmath as mp
import sympy as sp


def check(p, H):
    return None


def edl_gc_psi(psis, kz):
    """Gouy-Chapman: reduced potential at reduced distance kz, by inverting kz = int_psi^psis dpsi/(2 sinh(psi/2))"""
    with mp.workdps(40):
        s, k = mp.mpf(str(psis)), mp.mpf(str(kz))
        z = lambda p: mp.quad(lambda q: 1 / (2 * mp.sinh(q / 2)), [p, s])
        lo, hi = mp.mpf("1e-30"), s
        for _ in range(200):
            m = (lo + hi) / 2
            if z(m) > k:
                lo = m
            else:
                hi = m
        return sp.Float(str((lo + hi) / 2), 30)


def edl_mf_m(t):
    """mean-field Ising: positive root of m = tanh(m/t) for t = T/Tc < 1, by bisection"""
    with mp.workdps(40):
        t = mp.mpf(str(t))
        lo, hi = mp.mpf("1e-12"), mp.mpf(1)
        for _ in range(300):
            m = (lo + hi) / 2
            if mp.tanh(m / t) - m > 0:
                lo = m
            else:
                hi = m
        return sp.Float(str((lo + hi) / 2), 30)


FUNCS = {f.__name__: f for f in [edl_gc_psi, edl_mf_m]}
