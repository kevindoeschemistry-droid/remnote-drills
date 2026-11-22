"""Nursing (NCLEX-RN) checks, written separately from the hand-filled answers in nr-*.yaml.

ABG interpretation and compensation by the usual rule; ABO/Rh red-cell compatibility from antigens;
GCS, APGAR and rule-of-nines scores from the descriptions on the card, through their own tables.
"""
import sympy as sp

PRIMARY = ["respiratory acidosis", "respiratory alkalosis", "metabolic acidosis", "metabolic alkalosis"]


def abg_primary(pH, co2, hco3):
    """0 resp acidosis, 1 resp alkalosis, 2 met acidosis, 3 met alkalosis; a normal pH is read by its side of 7.40"""
    acid = pH < 7.40
    if acid:
        if co2 > 45:
            return 0
        if hco3 < 22:
            return 2
    else:
        if co2 < 35:
            return 1
        if hco3 > 26:
            return 3
    raise ValueError(f"no primary disorder in {pH}, {co2}, {hco3}")


def abg_comp(pH, co2, hco3):
    """0 uncompensated, 1 partially, 2 fully compensated"""
    both = (co2 < 35 or co2 > 45) and (hco3 < 22 or hco3 > 26)
    if not both:
        return 0
    return 2 if 7.35 <= pH <= 7.45 else 1


ANTIGENS = {"O": set(), "A": {"A"}, "B": {"B"}, "AB": {"A", "B"}}


def abo_ok(rec, rrh, don, drh):
    """1 if the donor's red cells can go to the recipient: no antigen the recipient lacks, and Rh+ only to Rh+"""
    t = ["O", "A", "B", "AB"]
    ok = ANTIGENS[t[don]] <= ANTIGENS[t[rec]] and (drh == 0 or rrh == 1)
    return 0 if ok else 1  # option 0 is "Compatible"


GCS_E = {"spontaneously": 4, "to voice": 3, "to pain": 2, "not at all": 1}
GCS_V = {"oriented": 5, "confused": 4, "inappropriate words": 3, "incomprehensible sounds": 2, "no verbal response": 1}
GCS_M = {"obeys commands": 6, "localizes pain": 5, "withdraws from pain": 4, "abnormal flexion": 3, "extension": 2, "no motor response": 1}


def gcs(et, vt, mt):
    return GCS_E[et] + GCS_V[vt] + GCS_M[mt]


def apgar(hr, resp, tone, refl, color):
    s = 0 if hr == 0 else (1 if hr < 100 else 2)
    s += {"absent": 0, "slow and irregular": 1, "good cry": 2}[resp]
    s += {"limp": 0, "some flexion": 1, "active motion": 2}[tone]
    s += {"no response": 0, "grimace": 1, "cry or sneeze": 2}[refl]
    s += {"blue or pale": 0, "pink body, blue hands and feet": 1, "completely pink": 2}[color]
    return s


NINES = {"hd": 9, "ra": 9, "la": 9, "ft": 18, "bt": 18, "rl": 18, "ll": 18, "frl": 9, "fll": 9, "brl": 9, "bll": 9, "pe": 1}


def nines(codes):
    return sum(NINES[c] for c in codes.split())


def holliday(w):
    """maintenance fluid in mL/h by the 4-2-1 rule, as an explicit sum over weight bands"""
    w = sp.nsimplify(w)
    first, second, rest = sp.Min(w, 10), sp.Min(sp.Max(w - 10, 0), 10), sp.Max(w - 20, 0)
    return 4 * first + 2 * second + rest


FUNCS = {f.__name__: f for f in [abg_primary, abg_comp, abo_ok, gcs, apgar, nines, holliday]}
