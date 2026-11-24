"""Second question types for Material and Energy Balances (MB), hand-written units 2-5."""
from opl_dsl import Q

FILE, FRAMEWORK = "mb-second-types", "material-balances"
ADD = [
    ("MB-2.1.B", Q("mb-dof-mixer", "meb.nonreactive", "Two streams of a {{nc}}-component mixture merge into one. Of the {{tot}} stream variables (three flows and their compositions) {{known}} are given. How many degrees of freedom remain? (Negative means over-specified.)",
        given={"nc": {"pick": [2, 3]}, "known": {"int": [3, 8]}}, let={"tot": "3*nc"}, require=["known <= 3*nc"], value="3*nc - known - nc", tex="DOF", final=True,
        verify="(3 + 3*(nc - 1)) - known - nc", explain="Unknowns minus independent equations: a non-reactive unit gives one balance per component. Zero means the problem can be solved")),
    ("MB-3.1.C", Q("mb-selectivity-from-yield", "meb.reactive", "In parallel reactions A → D (desired) and A → U, conversion of A is {{X}} and the fractional yield of D (moles D per mole A fed) is {{Yd}}. What is the selectivity, moles D per mole U?",
        given={"X": {"pick": [0.6, 0.8, 0.9]}, "f": {"pick": [0.5, 0.7, 0.85]}}, let={"Yd": "X*f"}, value="Yd/(X - Yd)", tex="S_{D/U}",
        verify="solve(Eq(nsimplify(X)*nsimplify(f), x*(nsimplify(X) - nsimplify(X)*nsimplify(f))), x)[0]",
        explain="A consumed = D + U formed (one to one here); yield counts D against A fed, selectivity against U")),
    ("MB-3.1.D", Q("mb-recycle-flow", "meb.recycle", "A reactor converts {{Xs}} of its feed per pass; unreacted A is separated completely and recycled, so overall conversion is 100%. For {{F}} mol/h of fresh A, what is the recycle flow, in mol/h?",
        given={"Xs": {"pick": [0.2, 0.25, 0.5, 0.8]}, "F": {"pick": [100, 250]}}, value="F*(1 - Xs)/Xs", tex="R",
        verify="solve(Eq((F + x)*nsimplify(Xs), F), x)[0]", explain="Everything fed must eventually react: (F + R)X_sp = F. Low single-pass conversion means a large recycle and a big separator")),
    ("MB-4.1.B", Q("mb-mixer-flow-needed", "meb.energy", "Water at {{Th}} °C is mixed adiabatically with {{mc}} kg/s of water at {{Tc}} °C. What flow of the hot water, in kg/s, gives a mixture at {{Tm}} °C? (Constant c_p.)",
        given={"Th": {"pick": [80, 90]}, "mc": {"pick": [1, 2.5]}, "Tc": {"pick": [10, 15]}, "Tm": {"pick": [30, 40, 50]}}, value="mc*(Tm - Tc)/(Th - Tm)", tex="\\dot m_h",
        verify="solve(Eq(x*(Th - Tm), nsimplify(mc)*(Tm - Tc)), x)[0]", explain="Heat lost by the hot stream equals heat gained by the cold one: the lever rule on temperature")),
    ("MB-4.2.A", Q("mb-heat-of-reaction-T", "meb.energy", "A reaction has ΔH°(298 K) = {{dH}} kJ/mol and ΔC_p = {{dCp}} J/(mol·K), constant. What is ΔH at {{T}} K, in kJ/mol?",
        given={"dH": {"pick": [-92.2, -41.2, 180.5]}, "dCp": {"pick": [-45, -10, 20]}, "T": {"pick": [500, 700, 900]}}, value="dH + dCp*(T - 298)/1000", tex="\\Delta H(T)",
        verify="nsimplify(dH) + integrate(nsimplify(dCp)/1000, (Symbol('TT'), 298, T))", explain="Kirchhoff's law: carry reactants down to 298 K, react, carry products back up")),
    ("MB-5.1.A", Q("mb-drain-time", "meb.unsteady", "A tank of cross-section {{A}} m² drains through an orifice of {{a}} cm² (discharge coefficient 0.6). How long, in s, for the level to fall from {{h1}} m to {{h2}} m? (g = 9.81 m/s²)",
        given={"A": {"pick": [1, 2]}, "a": {"pick": [5, 10, 20]}, "h1": {"pick": [2, 3]}, "h2": {"pick": [0.5, 1]}}, value="2*A/(0.6*a/10000*sqrt(2*9.81))*(sqrt(h1) - sqrt(h2))", tex="t",
        verify="integrate(A/(Rational(6, 10)*Rational(a, 10000)*sqrt(2*Rational(981, 100)*Symbol('hh'))), (Symbol('hh'), nsimplify(h2), h1))",
        explain="Outflow ∝ √h (Torricelli), so draining slows as the level drops; the last bit takes longest")),
    ("MB-5.2.A", Q("mb-heating-coil-time", "meb.unsteady", "A stirred batch ({{m}} kg, c_p = 4.18 kJ/(kg·K)) at {{T0}} °C is heated by steam at {{Ts}} °C through a coil with UA = {{UA}} W/K. How long, in min, to reach {{T}} °C?",
        given={"m": {"pick": [500, 1000]}, "T0": {"pick": [20]}, "Ts": {"pick": [120, 150]}, "T": {"pick": [60, 80, 100]}, "UA": {"pick": [1000, 2500]}},
        value="m*4180/UA*log((Ts - T0)/(Ts - T))/60", tex="t",
        verify="integrate(m*4180/(UA*(Ts - Symbol('TT'))), (Symbol('TT'), T0, T))/60",
        explain="The driving force shrinks as the batch warms, so the approach is exponential with time constant mc_p/UA")),
]
