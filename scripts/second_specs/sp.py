"""Second question types for Separations (SP; code shared with Speaking, so FRAMEWORK names the file)."""
from opl_dsl import Q

FILE, FRAMEWORK = "sp-second-types", "separations"
ADD = [
    ("SP-1.1.A", Q("sp-alpha-from-data", "sep.vle", "A sample of liquid with light-key mole fraction {{xl}} is in equilibrium with vapour at {{yv}}. What relative volatility does that give?",
        given={"xl": {"pick": [0.2, 0.4, 0.5]}, "al": {"pick": [1.5, 2.4, 4]}}, let={"yv": "al*xl/(1 + (al - 1)*xl)"},
        value="yv*(1 - xl)/(xl*(1 - yv))", tex="\\alpha", verify="nsimplify(al)",
        explain="α = (y/x)/((1 − y)/(1 − x)): the ratio of the two components' K-values, nearly constant for similar molecules")),
    ("SP-1.1.B", Q("sp-fenske-reverse", "sep.distillation", "A column has the equivalent of {{n}} ideal stages at total reflux, α = {{al}}, and bottoms at $x_B$ = {{xb}}. What distillate purity $x_D$ can it reach?",
        given={"n": {"int": [5, 15]}, "al": {"pick": [1.5, 2, 2.5]}, "xb": {"pick": [0.02, 0.05, 0.1]}},
        value="1/(1 + ((1 - xb)/xb)/al^n)", tex="x_D", verify="solve(Eq((x/(1 - x))*((1 - nsimplify(xb))/nsimplify(xb)), nsimplify(al)**n), x)[0]",
        explain="At total reflux each stage multiplies the separation ratio by α, so purity climbs steeply with stages once α is well above 1")),
    ("SP-1.1.C", Q("sp-rmin-vapour-feed", "sep.distillation", "A saturated-vapour feed (z = {{z}}) enters a column with α = {{al}} and $x_D$ = {{xd}}. What is the minimum reflux ratio? (The pinch is where the horizontal q-line y = z meets the equilibrium curve.)",
        given={"z": {"pick": [0.4, 0.5, 0.6]}, "al": {"pick": [2, 2.5, 3]}, "xd": {"pick": [0.9, 0.95]}},
        value="(xd - z)/(z - z/(al - (al - 1)*z))", tex="R_{min}",
        verify="(nsimplify(xd) - nsimplify(z))/(nsimplify(z) - solve(Eq(nsimplify(al)*x/(1 + (nsimplify(al) - 1)*x), nsimplify(z)), x)[0])",
        explain="Slope of the pinched rectifying line R/(R + 1) = (x_D − y*)/(x_D − x*); a vapour feed needs more reflux than a liquid feed for the same job")),
    ("SP-1.2.A", Q("sp-kremser-fraction", "sep.absorption", "An absorber has {{n}} ideal stages and absorption factor A = {{Af}}, with solute-free liquid. What fraction of the solute is absorbed?",
        given={"n": {"int": [2, 8]}, "Af": {"pick": [0.8, 1.2, 1.5, 2]}}, value="(Af^(n + 1) - Af)/(Af^(n + 1) - 1)", tex="f",
        verify="summation(nsimplify(Af)**Symbol('k'), (Symbol('k'), 1, n))/summation(nsimplify(Af)**Symbol('k'), (Symbol('k'), 0, n))",
        explain="With A < 1 even infinite stages cannot absorb everything (the limit is A); with A > 1 complete absorption is possible in principle")),
    ("SP-2.1.A", Q("sp-rh-from-humidity", "sep.humidification", "Air at {{P}} kPa total has absolute humidity {{H}} kg water/kg dry air; the vapour pressure of water at its temperature is {{ps}} kPa. What is the relative humidity, in %?",
        given={"P": {"pick": [101.3]}, "H": {"pick": [0.005, 0.01, 0.015]}, "ps": {"pick": [3.17, 4.25]}}, require=["H*101.3/(0.622 + H)/ps < 1"],
        value="H*P/(0.622 + H)/ps*100", tex="RH", verify="solve(Eq(nsimplify(H), Rational(622, 1000)*(x/100*nsimplify(ps))/(nsimplify(P) - x/100*nsimplify(ps))), x)[0]",
        explain="Back out the water partial pressure from H = 0.622 p/(P − p), then divide by the saturation pressure")),
    ("SP-2.1.B", Q("sp-evaporator-steam", "sep.humidification", "A single-effect evaporator concentrates {{F}} kg/h of feed from {{x1}}% to {{x2}}% solids, fed at its boiling point. Latent heat of the vapour is {{lv}} kJ/kg and of the steam {{ls}} kJ/kg. How much steam, in kg/h?",
        given={"F": {"pick": [1000, 2500]}, "x1": {"pick": [5, 10]}, "x2": {"pick": [30, 50]}, "lv": {"pick": [2260, 2300]}, "ls": {"pick": [2150, 2200]}},
        value="F*(1 - x1/x2)*lv/ls", tex="\\dot m_s",
        verify="solve(Eq(x*ls, (F - solve(Eq(F*Rational(x1, 100), Symbol('pp')*Rational(x2, 100)), Symbol('pp'))[0])*lv), x)[0]",
        explain="Solids balance gives the water evaporated; with no sensible heating and no boiling-point rise, roughly one kg of steam per kg of water (economy about 1). Multiple effects reuse the vapour")),
]
