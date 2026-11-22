"""Dental (INBDE) checks, kept separate from the hand-filled answers in dn-*.yaml.

Tooth notation is rebuilt from an explicit list of teeth in Universal order, not from the
arithmetic the generator uses; periodontal staging and diagnostic-test statistics by their
definitions.
"""
import sympy as sp

# Universal 1..32: maxillary right third molar round to mandibular right third molar
_ARCH = ["third molar", "second molar", "first molar", "second premolar", "first premolar", "canine", "lateral incisor", "central incisor"]
_UNIVERSAL = ([("UR", n) for n in _ARCH] + [("UL", n) for n in reversed(_ARCH)]
              + [("LL", n) for n in _ARCH] + [("LR", n) for n in reversed(_ARCH)])
_QUAD = {"UR": 1, "UL": 2, "LL": 3, "LR": 4}
_POS = {n: 8 - i for i, n in enumerate(_ARCH)}  # central incisor 1 ... third molar 8


def fdi(u):
    q, name = _UNIVERSAL[int(u) - 1]
    return 10 * _QUAD[q] + _POS[name]


_P_ARCH = ["second molar", "first molar", "canine", "lateral incisor", "central incisor"]
_PRIMARY = ([("UR", n) for n in _P_ARCH] + [("UL", n) for n in reversed(_P_ARCH)]
            + [("LL", n) for n in _P_ARCH] + [("LR", n) for n in reversed(_P_ARCH)])  # A..T
_PQUAD = {"UR": 5, "UL": 6, "LL": 7, "LR": 8}
_PPOS = {n: 5 - i for i, n in enumerate(_P_ARCH)}


def fdi_primary(k):
    """k = 0 for A ... 19 for T"""
    q, name = _PRIMARY[int(k)]
    return 10 * _PQUAD[q] + _PPOS[name]


def perio_stage(cal):
    """2017 AAP/EFP staging by worst interdental CAL: 0 stage I (1-2 mm), 1 stage II (3-4), 2 stage III or IV (5+)"""
    return 0 if cal <= 2 else (1 if cal <= 4 else 2)


def test_stat(tp, fp, fn, tn, k):
    """0 sensitivity, 1 specificity, 2 PPV, 3 NPV, as fractions"""
    return [sp.Rational(tp, tp + fn), sp.Rational(tn, tn + fp), sp.Rational(tp, tp + fp), sp.Rational(tn, tn + fn)][int(k)]


FUNCS = {f.__name__: f for f in [fdi, fdi_primary, perio_stage, test_stat]}
