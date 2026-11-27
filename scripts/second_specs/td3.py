"""Second question types for the three Thermodynamics objectives that listed one drill (Nov 2026)."""
FILE, FRAMEWORK = "td-second-types-3", "thermodynamics"
from opl_dsl import Q

M = "Symbol('m')"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
ADD = []


def N(code, name, skill, prompt, value, verify, explain, tex="answer", **kw):
    ADD.append((code, Q(name, skill, prompt, value=value, tex=tex, verify=verify, explain=explain, **kw)))


def L(code, name, skill, prompt, options, rows, explain):
    ADD.append((code, Q(name, skill, prompt, pace="recall", cases=[{"q": a, "kc": k} for a, k in rows], choice=options, correct="kc", verify="authored", explain=explain)))


def F(code, name, skill, rows, explain):
    ADD.append((code, Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows], choice=MC, correct="0", verify="authored", explain=explain)))


def C(keys, rows):
    return [dict(zip(keys.split(), r)) for r in rows]


FE = "thermo.fundamental-equation"
N("TD-2.2.B", "td-thermal-contact-temperature", FE, "Two bodies with constant heat capacities {{k1}} and {{k2}} J/K start at {{ka}} K and {{kb}} K and exchange energy only with each other. At what common temperature is the total entropy largest?",
  "(k1*ka + k2*kb)/(k1 + k2)", f"solve(Eq(k1*({M} - ka) + k2*({M} - kb), 0), {M})[0]", "dS = (1/T₁ − 1/T₂)dU₁ vanishes when the temperatures are equal, and energy conservation fixes which temperature", tex="T",
  cases=C("k1 k2 ka kb", [(100, 100, 300, 400), (200, 100, 300, 360), (50, 150, 500, 300), (400, 100, 280, 380)]))
L("TD-2.2.C", "td-extremum-principle", FE, "For a system held at fixed {{q}}, equilibrium is where:", ["Entropy is a maximum", "Internal energy is a minimum", "Helmholtz energy is a minimum", "Gibbs energy is a minimum"], [
  ("U, V and N", 0), ("S, V and N", 1), ("T, V and N", 2), ("T, P and N", 3)],
  "Each potential is the Legendre transform that swaps the held variables: maximum S at fixed U is the same statement as minimum U at fixed S, and so on down the list")
N("TD-2.3.C", "td-extensive-exponent", FE, "A proposed fundamental equation is S = a·U^{{ka}}·V^{{kb}}·N^γ. What must γ be for S to be extensive?", "1 - ka - kb",
  f"solve(Eq(nsimplify(ka) + nsimplify(kb) + {M}, 1), {M})[0]", "Scaling U, V and N by λ must scale S by λ, so the exponents add to 1", tex="\\gamma",
  cases=C("ka kb", [(0.5, 0.25), (0.25, 0.25), (0.4, 0.4), (0.75, 0.5), (0.2, 0.3)]))
assert len(ADD) == 3
