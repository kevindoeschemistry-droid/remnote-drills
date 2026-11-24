"""Engineering thermodynamics gaps (OPL TH). Steam properties on the cards come from IAPWS-IF97 (the
`iapws` package, dev only), rounded as a table would print them; the verifier works only from the printed
numbers, so the property values are data and the balances are what is checked."""
import math
from iapws import IAPWS97
from opl_dsl import Q, L, U

FW, FILE, IDEA = "TD", "opl-td", "EQ"


def r(v, n=2):
    return round(float(v), n)


SAT = []  # saturated states by pressure (kPa)
for P in (10, 50, 100, 200, 500, 1000, 2000):
    f, g = IAPWS97(P=P / 1000, x=0), IAPWS97(P=P / 1000, x=1)
    SAT.append({"P": P, "Ts": r(f.T - 273.15, 1), "hf": r(f.h), "hfg": r(g.h - f.h), "sf": r(f.s, 4), "sfg": r(g.s - f.s, 4), "vg": r(g.v, 4)})

SUPER = []  # superheated pairs for interpolation
for P, T1, T2, Tq in ((1000, 250, 300, 280), (2000, 300, 350, 320), (500, 200, 250, 230), (4000, 400, 450, 420), (100, 150, 200, 175)):
    a, b = IAPWS97(P=P / 1000, T=T1 + 273.15), IAPWS97(P=P / 1000, T=T2 + 273.15)
    SUPER.append({"P": P, "T1": T1, "T2": T2, "T": Tq, "h1": r(a.h, 1), "h2": r(b.h, 1), "s1": r(a.s, 4), "s2": r(b.s, 4)})

COMP = []  # compressed liquid
for P, T in ((5000, 80), (10000, 100), (20000, 60), (15000, 150)):
    f = IAPWS97(T=T + 273.15, x=0)
    COMP.append({"P": P, "T": T, "hf": r(f.h), "vf": r(f.v, 6), "Ps": r(f.P * 1000, 2), "sf": r(f.s, 4)})

RANK = []  # simple ideal Rankine cycles: boiler P (MPa), T (°C), condenser P (kPa)
for Pb, Tb, Pc in ((3, 350, 10), (4, 400, 10), (6, 450, 20), (8, 500, 10), (10, 550, 15)):
    s1 = IAPWS97(P=Pb, T=Tb + 273.15)
    f, g = IAPWS97(P=Pc / 1000, x=0), IAPWS97(P=Pc / 1000, x=1)
    x2 = (s1.s - f.s) / (g.s - f.s)
    h2 = f.h + x2 * (g.h - f.h)
    wp = f.v * (Pb * 1000 - Pc)
    RANK.append({"Pb": Pb, "Tb": Tb, "Pc": Pc, "h1": r(s1.h, 1), "h2": r(h2, 1), "h3": r(f.h, 1), "h4": r(f.h + wp, 1)})

REGEN = []  # open feedwater heater fraction
for Pb, Tb, Pf, Pc in ((8, 500, 0.5, 10), (6, 450, 0.4, 10), (10, 550, 0.8, 15)):
    s1 = IAPWS97(P=Pb, T=Tb + 273.15)
    bled = IAPWS97(P=Pf, s=s1.s)
    pump1 = IAPWS97(P=Pc / 1000, x=0)
    h_in = pump1.h + pump1.v * (Pf * 1000 - Pc)
    sat = IAPWS97(P=Pf, x=0)
    REGEN.append({"Pb": Pb, "Tb": Tb, "Pf": Pf, "Pc": Pc, "hb": r(bled.h, 1), "hin": r(h_in, 1), "hout": r(sat.h, 1)})

SH = lambda name, sk, *a, **k: Q(name, sk, *a, **k)

UNITS = [
U(18, "properties", "Properties of pure substances and simple processes", [
    ("Work and property tables", [
        L("A", "Compute spring and electrical work.", "Spring: W = ½k(x₂² − x₁²); electrical: W = VIt.", ["TH1.14", "TH1.15"], [
            Q("td-spring-work", "thermo.first-law", "A spring with $k = {{k}}$ kN/m is compressed from {{x1}} cm to {{x2}} cm. How much work goes in, in J?",
              given={"k": {"pick": [50, 100, 200]}, "x1": {"pick": [0, 2, 5]}, "x2": {"pick": [8, 10, 15]}}, value="0.5*k*1000*((x2/100)^2 - (x1/100)^2)", tex="W",
              verify="integrate(k*1000*x, (x, nsimplify(x1)/100, nsimplify(x2)/100))", explain="The force grows linearly with stretch, so the work is the area of a trapezoid under $F = kx$: $\\tfrac12k(x_2^2 - x_1^2)$"),
            Q("td-electrical-work", "thermo.first-law", "A {{V}} V heater draws {{I}} A for {{t}} min inside a closed tank. How much electrical work enters, in kJ?",
              given={"V": {"pick": [110, 120, 230]}, "I": {"pick": [2, 5, 8]}, "t": {"pick": [5, 10, 30]}}, value="V*I*t*60/1000", tex="W_e",
              verify="integrate(V*I, (x, 0, t*60))/1000", explain="Electrical power is $VI$; multiply by the time in seconds. In a closed-system first law it enters as work, not heat"),
        ]),
        L("B", "Read a compressed-liquid state.", "h ≈ h_f(T) + v_f (P − P_sat(T)); otherwise treat it as saturated liquid at T.", ["TH2.4", "TH7.3"], [
            Q("td-compressed-liquid", "thermo.first-law", "Water at {{P}} kPa and {{T}} °C. From the saturated table at {{T}} °C: $h_f = {{hf}}$ kJ/kg, $v_f = {{vf}}$ m³/kg, $P_{sat} = {{Ps}}$ kPa. Estimate $h$ with the pressure correction.",
              cases=COMP, value="hf + vf*(P - Ps)", tex="h", tol=0.0001, verify="nsimplify(hf) + nsimplify(vf)*(P - nsimplify(Ps))",
              explain="A compressed liquid is nearly the saturated liquid at the same temperature; the $v\\,\\Delta P$ term corrects $h$ by a few kJ/kg. Entropy needs no correction: $s \\approx s_f(T)$")]),
        L("C", "Use saturated-liquid and saturated-vapour properties.", "At saturation, h_g = h_f + h_fg; the mass in a tank is V/v_g.", ["TH2.5", "TH2.7"], [
            Q("td-saturated-mass", "thermo.first-law", "A {{V}} m³ tank holds saturated water vapour at {{P}} kPa ($v_g = {{vg}}$ m³/kg). What mass of vapour is in it, in kg?",
              cases=SAT, given={"V": {"pick": [0.5, 1, 2]}}, value="V/vg", tex="m", tol=0.0001, verify="nsimplify(V)/nsimplify(vg)",
              explain="Specific volume is volume per mass. At low pressure $v_g$ is large (tens of m³/kg at 10 kPa), so a big tank holds little vapour")]),
        L("D", "Find the quality and enthalpy of a two-phase mixture.", "x = (h − h_f)/h_fg; h = h_f + x h_fg.", ["TH2.6", "TH2.9"], [
            Q("td-quality", "thermo.first-law", "Water at {{P}} kPa ($T_{sat} = {{Ts}}$ °C) has $h = {{hf + xq*hfg}}$ kJ/kg. With $h_f = {{hf}}$ and $h_{fg} = {{hfg}}$ kJ/kg, what is the quality?",
              cases=SAT, given={"xq": {"pick": [0.2, 0.5, 0.75, 0.9]}}, value="xq", tex="x", tol=0.0001,
              verify="solve(Eq(nsimplify(hf) + x*nsimplify(hfg), nsimplify(hf) + nsimplify(xq)*nsimplify(hfg)), x)[0]",
              explain="Quality is the vapour mass fraction; any specific property interpolates linearly between $f$ and $g$ with weight $x$")]),
        L("E", "Interpolate in the superheated table.", "Linear interpolation between neighbouring entries.", ["TH2.8", "TH7.7"], [
            Q("td-superheated-interp", "thermo.first-law", "Superheated steam at {{P}} kPa: $h = {{h1}}$ kJ/kg at {{T1}} °C and ${{h2}}$ kJ/kg at {{T2}} °C. Estimate $h$ at {{T}} °C.",
              cases=SUPER, value="h1 + (T - T1)/(T2 - T1)*(h2 - h1)", tex="h", tol=0.0001,
              verify="solve(Eq((x - nsimplify(h1))/(T - T1), (nsimplify(h2) - nsimplify(h1))/(T2 - T1)), x)[0]",
              explain="Between table rows a property is close to linear in $T$; the same interpolation gives $s$ and $v$")]),
        L("F", "Find the heat to melt or boil a substance.", "Q = m(c ΔT + latent heat).", ["TH2.3", "TH2.9"], [
            Q("td-ice-melt", "thermo.first-law", "{{m}} kg of ice at {{T}} °C is warmed to 0 °C and melted ($c_{ice} = 2.09$ kJ/kg·K, $h_{if} = 333.7$ kJ/kg). How much heat, in kJ?",
              given={"m": {"pick": [1, 2, 5]}, "T": {"pick": [-20, -10, -5]}}, value="m*(2.09*(0 - T) + 333.7)", tex="Q",
              verify="m*(integrate(Rational(209, 100), (x, T, 0)) + Rational(3337, 10))", explain="Warm the solid first, then supply the latent heat at constant temperature; melting dominates")]),
        L("G", "Find the work of a polytropic process.", "PVⁿ = const; W = (P₂V₂ − P₁V₁)/(1 − n) for n ≠ 1.", ["TH2.16"], [
            Q("td-polytropic-work", "thermo.first-law", "A gas expands polytropically ($n = {{n}}$) from {{P1}} kPa and {{V1}} m³ to {{V2}} m³. What boundary work does it do, in kJ?",
              given={"n": {"pick": [1.2, 1.3, 1.4]}, "P1": {"pick": [400, 800, 1000]}, "V1": {"pick": [0.1, 0.2]}, "V2": {"pick": [0.4, 0.5, 0.8]}},
              value="(P1*(V1/V2)^n*V2 - P1*V1)/(1 - n)", tex="W", tol=0.0001,
              verify="integrate(P1*nsimplify(V1)**nsimplify(n)/x**nsimplify(n), (x, nsimplify(V1), nsimplify(V2)))",
              explain="$P_2 = P_1(V_1/V_2)^n$; integrating $P\\,dV$ gives $(P_2V_2 - P_1V_1)/(1 - n)$. $n = 1$ is isothermal for an ideal gas, $n = k$ is isentropic")]),
        L("H", "Handle incompressible substances.", "Δu = cΔT; Δh = cΔT + vΔP; Δs = c ln(T₂/T₁).", ["TH2.17", "TH2.18", "TH7.11"], [
            Q("td-pump-enthalpy", "thermo.first-law", "Liquid water ($v = 0.001$ m³/kg) is pumped from {{P1}} kPa to {{P2}} kPa with no temperature change. What is $\\Delta h$, in kJ/kg?",
              given={"P1": {"pick": [10, 50, 100]}, "P2": {"pick": [2000, 5000, 10000]}}, value="0.001*(P2 - P1)", tex="\\Delta h",
              verify="integrate(Rational(1, 1000), (x, P1, P2))", explain="For an incompressible liquid $\\Delta u = c\\Delta T = 0$ here and $\\Delta h = v\\Delta P$. That small number is why pump work is tiny next to turbine work"),
            Q("td-incompressible-entropy", "thermo.first-law", "{{m}} kg of iron ($c = 0.45$ kJ/kg·K) cools from {{T1}} °C to {{T2}} °C. What is its entropy change, in kJ/K?",
              given={"m": {"pick": [1, 2, 5]}, "T1": {"pick": [300, 400, 500]}, "T2": {"pick": [25, 50, 100]}}, value="m*0.45*log((T2 + 273.15)/(T1 + 273.15))", tex="\\Delta S",
              verify="m*integrate(Rational(45, 100)/x, (x, nsimplify(T1) + Rational(27315, 100), nsimplify(T2) + Rational(27315, 100)))",
              explain="$dS = mc\\,dT/T$ for an incompressible solid; use kelvin. It is negative, but the surroundings gain more"),
        ]),
    ]),
    ("Entropy of pure substances", [
        L("A", "Read entropy on a T–s diagram.", "Area under a reversible path is the heat; an isentropic process is a vertical line.", ["TH7.1"], [
            Q("td-ts-diagram", "thermo.first-law", "On a T–s diagram, {{q}}", pace="recall",
              cases=[{"q": "what does the area under a reversible process curve represent?", "ans": 0}, {"q": "what does a reversible adiabatic process look like?", "ans": 1},
                     {"q": "what does an isothermal process look like?", "ans": 2}, {"q": "what does the area enclosed by a reversible cycle represent?", "ans": 3}],
              choice=["The heat transferred per unit mass", "A vertical line", "A horizontal line", "The net work of the cycle"], correct="ans", verify="authored",
              explain="$\\delta q_{rev} = T\\,ds$, so area means heat; no heat and no irreversibility means constant $s$")]),
        L("B", "Find the entropy of a saturated or two-phase state.", "s = s_f + x s_fg; the entropy of vaporisation is h_fg/T_sat.", ["TH7.4", "TH7.5", "TH7.6", "TH7.8"], [
            Q("td-two-phase-entropy", "thermo.first-law", "Water at {{P}} kPa has quality {{xq}}. With $s_f = {{sf}}$ and $s_{fg} = {{sfg}}$ kJ/kg·K, find $s$.",
              cases=SAT, given={"xq": {"pick": [0.1, 0.4, 0.8, 0.95]}}, value="sf + xq*sfg", tex="s", tol=0.0001,
              verify="nsimplify(sf)*(1 - nsimplify(xq)) + (nsimplify(sf) + nsimplify(sfg))*nsimplify(xq)", explain="Mix the saturated-liquid and saturated-vapour values in the ratio $1 - x : x$"),
            Q("td-boiling-entropy", "thermo.first-law", "{{m}} kg of saturated liquid water is fully vaporised at {{P}} kPa ($T_{sat} = {{Ts}}$ °C, $h_{fg} = {{hfg}}$ kJ/kg). What is the entropy change, in kJ/K?",
              cases=SAT, given={"m": {"pick": [1, 2, 3]}}, value="m*hfg/(Ts + 273.15)", tex="\\Delta S", tol=0.0001,
              verify="m*nsimplify(hfg)/(nsimplify(Ts) + Rational(27315, 100))", explain="At constant $T$ and $P$, $\\Delta s = h_{fg}/T_{sat}$ in kelvin: the table's $s_{fg}$ is exactly this"),
        ]),
        L("C", "Find the entropy change of heating a solid.", "Δs = c ln(T₂/T₁) for a solid with constant c.", ["TH7.2"], [
            Q("td-ice-entropy", "thermo.first-law", "{{m}} kg of ice ($c = 2.09$ kJ/kg·K) warms from {{T}} °C to 0 °C. What is its entropy change, in kJ/K?",
              given={"m": {"pick": [1, 2, 5]}, "T": {"pick": [-30, -20, -10]}}, value="m*2.09*log(273.15/(T + 273.15))", tex="\\Delta S", tol=0.0001,
              verify="m*integrate(Rational(209, 100)/x, (x, nsimplify(T) + Rational(27315, 100), Rational(27315, 100)))", explain="Integrate $mc\\,dT/T$; solids and liquids behave alike here")]),
    ]),
]),
U(19, "control-volumes", "Control volumes, the second law and exergy", [
    ("Flow work and devices", [
        L("A", "Compute flow work.", "Flow work per unit mass = Pv.", ["TH5.1"], [
            Q("td-flow-work", "thermo.first-law", "Steam enters a turbine at {{P}} kPa with $v = {{v}}$ m³/kg. What is the flow work per kilogram, in kJ/kg?",
              given={"P": {"pick": [500, 1000, 3000]}, "v": {"pick": [0.08, 0.2, 0.4]}}, value="P*v", tex="Pv", verify="P*nsimplify(v)",
              explain="Pushing a kilogram into the control volume against pressure $P$ takes $Pv$; it is why open systems use $h = u + Pv$")]),
        L("B", "Analyse several devices together.", "Write the balance for each device and add the powers.", ["TH5.10"], [
            Q("td-net-power", "thermo.first-law", "Steam ({{m}} kg/s) runs through a turbine from $h = {{h1}}$ to ${{h2}}$ kJ/kg; a pump raises the same water from ${{h3}}$ to ${{h4}}$ kJ/kg. What is the net power, in kW?",
              cases=RANK, given={"m": {"pick": [5, 10, 20]}}, value="m*((h1 - h2) - (h4 - h3))", tex="\\dot W_{net}", tol=0.0001,
              verify="m*(nsimplify(h1) - nsimplify(h2)) + m*(nsimplify(h3) - nsimplify(h4))", explain="Each adiabatic device gives $\\dot W = \\dot m(h_{in} - h_{out})$; the pump's is negative")]),
        L("C", "Account for isentropic efficiency.", "Turbine: η = (h₁ − h₂)/(h₁ − h₂ₛ); compressor: η = (h₂ₛ − h₁)/(h₂ − h₁).", ["TH7.17"], [
            Q("td-compressor-efficiency", "thermo.first-law", "Air ($k = 1.4$, $c_p = 1.005$ kJ/kg·K) is compressed from {{T1}} K and 100 kPa to {{rp*100}} kPa by a compressor with isentropic efficiency {{eta}}. Find the actual exit temperature, in K.",
              given={"T1": {"pick": [290, 300]}, "rp": {"pick": [4, 6, 8, 10]}, "eta": {"pick": [0.8, 0.85, 0.9]}}, value="T1 + (T1*rp^(0.4/1.4) - T1)/eta", tex="T_2", tol=0.0001,
              verify="solve(Eq(nsimplify(eta), (T1*rp**Rational(2, 7) - T1)/(x - T1)), x)[0]", explain="Find the isentropic outlet $T_{2s} = T_1 r_p^{(k-1)/k}$, then divide the ideal temperature rise by $\\eta$: real compressors run hotter")]),
    ]),
    ("The second law", [
        L("A", "Recognise the Kelvin–Planck and Clausius statements.", "No cycle turns heat from one reservoir entirely into work; none moves heat from cold to hot with no work.", ["TH6.2", "TH6.3"], [
            Q("td-second-law-statements", "thermo.first-law", "{{q}}", pace="recall",
              cases=[{"q": "An engine takes 100 kJ from a hot reservoir and delivers 100 kJ of work, rejecting nothing. Possible?", "ans": 1},
                     {"q": "A refrigerator moves 50 kJ from a cold space to a warm room with no work input. Possible?", "ans": 1},
                     {"q": "An engine takes 100 kJ from a 600 K reservoir, rejects 60 kJ to a 300 K one and delivers 40 kJ. Possible?", "ans": 0},
                     {"q": "A heat pump delivers 50 kJ to a house while taking 40 kJ from outside and 10 kJ of work. Possible?", "ans": 0}],
              choice=["Yes", "No, it violates the second law"], correct="ans", verify="authored",
              explain="Kelvin–Planck forbids a cycle that rejects no heat; Clausius forbids heat climbing a temperature without work. An engine is also capped by Carnot: here $1 - 300/600 = 0.5 \\ge 0.4$, so the third case is fine")]),
        L("B", "Use the thermodynamic temperature scale.", "For a reversible engine Q_H/Q_L = T_H/T_L.", ["TH6.8"], [
            Q("td-kelvin-scale", "thermo.first-law", "A reversible engine takes {{QH}} kJ from a reservoir at {{TH}} K and rejects {{QL}} kJ. What is the cold reservoir's temperature, in K?",
              given={"QH": {"pick": [500, 1000]}, "TH": {"pick": [600, 800, 1000]}, "QL": {"pick": [200, 300, 400]}}, value="TH*QL/QH", tex="T_L",
              verify="solve(Eq(Rational(QH, QL), TH/x), x)[0]", explain="Kelvin defined temperature this way: the ratio of heats in a reversible cycle, independent of any substance")]),
    ]),
    ("Exergy", [
        L("A", "Find the exergy of a hot body.", "X = m c[(T − T₀) − T₀ ln(T/T₀)].", ["TH8.1"], [
            Q("td-exergy-block", "thermo.first-law", "{{m}} kg of iron ($c = 0.45$ kJ/kg·K) is at {{T}} K; the surroundings are at 300 K. What is its exergy, in kJ?",
              given={"m": {"pick": [1, 5, 10]}, "T": {"pick": [400, 500, 700]}}, value="m*0.45*((T - 300) - 300*log(T/300))", tex="X", tol=0.0001,
              verify="integrate(m*Rational(45, 100)*(1 - 300/x), (x, 300, T))", explain="Run a reversible engine off the block as it cools: each $\\delta Q$ yields $(1 - T_0/T)\\delta Q$")]),
        L("B", "Find the exergy carried by heat.", "X_Q = Q(1 − T₀/T).", ["TH8.2"], [
            Q("td-heat-exergy", "thermo.first-law", "{{Q}} kJ of heat is delivered at {{T}} K with surroundings at 298 K. How much of it is exergy, in kJ?",
              given={"Q": {"pick": [100, 500, 1000]}, "T": {"pick": [350, 500, 800, 1200]}}, value="Q*(1 - 298/T)", tex="X_Q", tol=0.0001,
              verify="solve(Eq(x/Q, 1 - Rational(298, T)), x)[0]", explain="Heat is worth only its Carnot fraction; heat near ambient temperature is nearly worthless")]),
        L("C", "Find the exergy destroyed in a process.", "X_destroyed = T₀ S_gen.", ["TH8.3"], [
            Q("td-exergy-destroyed", "thermo.first-law", "{{Q}} kJ of heat leaks from a {{TH}} K reservoir straight to a {{TL}} K reservoir. With $T_0 = {{TL}}$ K, how much exergy is destroyed, in kJ?",
              given={"Q": {"pick": [100, 200, 500]}, "TH": {"pick": [500, 800, 1000]}, "TL": {"pick": [290, 300]}}, value="TL*Q*(1/TL - 1/TH)", tex="X_d", tol=0.0001,
              verify="Q*(1 - nsimplify(TL)/TH) - Q*(1 - nsimplify(TL)/TL)", explain="Gouy–Stodola: $X_d = T_0S_{gen}$ with $S_{gen} = Q/T_L - Q/T_H$. It equals the exergy the heat carried in minus what it carries out")]),
        L("D", "Compute flow exergy.", "ψ = (h − h₀) − T₀(s − s₀) (ignoring kinetic and potential terms).", ["TH8.4"], [
            Q("td-flow-exergy", "thermo.first-law", "A stream has $h - h_0 = {{dh}}$ kJ/kg and $s - s_0 = {{ds}}$ kJ/kg·K; $T_0 = 298$ K. What is its flow exergy, in kJ/kg?",
              given={"dh": {"pick": [500, 1000, 2500]}, "ds": {"pick": [0.8, 1.5, 4]}}, value="dh - 298*ds", tex="\\psi", tol=0.0001,
              verify="nsimplify(dh) - 298*nsimplify(ds)", explain="Enthalpy above the dead state, less what must be rejected as heat to reach it")]),
        L("E", "Compute a second-law efficiency.", "η_II = W_actual/W_reversible (or actual/maximum COP).", ["TH8.5"], [
            Q("td-second-law-efficiency", "thermo.first-law", "An engine between {{TH}} K and 300 K has thermal efficiency {{eta}}. What is its second-law efficiency?",
              given={"TH": {"pick": [600, 800, 1000]}, "eta": {"pick": [0.25, 0.3, 0.35]}}, value="eta/(1 - 300/TH)", tex="\\eta_{II}", tol=0.0001,
              verify="nsimplify(eta)/(1 - Rational(300, TH))", explain="Compare with the best possible engine between the same reservoirs, the Carnot efficiency")]),
        L("F", "Put a price on exergy destruction.", "Cost rate = (exergy destroyed per second) × (price of energy).", ["TH8.6"], [
            Q("td-thermoeconomics", "thermo.first-law", "A throttle destroys exergy at {{X}} kW, around the clock. At {{c}} cents per kWh, what does that cost per year, in dollars?",
              given={"X": {"pick": [10, 50, 200]}, "c": {"pick": [8, 12, 15]}}, value="X*8760*c/100", tex="C",
              verify="integrate(X*Rational(c, 100), (x, 0, 8760))", explain="Exergy destroyed is work that could have been had; thermoeconomics prices it to decide which losses are worth a capital fix")]),
    ]),
]),
U(20, "cycles", "Power and refrigeration cycles", [
    ("Vapour power cycles", [
        L("A", "Find the efficiency of a Rankine cycle.", "η = (w_turbine − w_pump)/q_in with q_in = h₁ − h₄.", ["TH9.1", "TH9.2"], [
            Q("td-rankine", "thermo.first-law", "A Rankine cycle ({{Pb}} MPa, {{Tb}} °C, condenser {{Pc}} kPa) has $h_1 = {{h1}}$ (turbine inlet), $h_2 = {{h2}}$, $h_3 = {{h3}}$ (pump inlet), $h_4 = {{h4}}$ kJ/kg. Find its thermal efficiency.",
              cases=RANK, value="((h1 - h2) - (h4 - h3))/(h1 - h4)", tex="\\eta", tol=0.0001,
              verify="1 - (nsimplify(h2) - nsimplify(h3))/(nsimplify(h1) - nsimplify(h4))",
              explain="Net work over heat in, which is also $1 - q_{out}/q_{in}$. Superheating and reheating raise $h_1$ and keep the turbine exhaust dry; higher boiler pressure raises the mean temperature of heat addition")]),
        L("B", "Find the bleed fraction of an open feedwater heater.", "y h_bleed + (1 − y) h_in = h_out (saturated liquid).", ["TH9.3"], [
            Q("td-feedwater-heater", "thermo.first-law", "An open feedwater heater at {{Pf}} MPa takes bled steam ($h = {{hb}}$ kJ/kg) and pumped condensate ($h = {{hin}}$ kJ/kg), and delivers saturated liquid ($h = {{hout}}$ kJ/kg). What fraction of the turbine flow is bled?",
              cases=REGEN, value="(hout - hin)/(hb - hin)", tex="y", tol=0.0001,
              verify="solve(Eq(x*nsimplify(hb) + (1 - x)*nsimplify(hin), nsimplify(hout)), x)[0]",
              explain="An energy balance on the mixing heater. Regeneration raises the temperature at which the boiler receives water, which lifts the cycle's efficiency")]),
    ]),
    ("Gas power cycles", [
        L("A", "Find the air-standard Otto efficiency.", "η = 1 − r^(1−k).", ["TH10.1"], [
            Q("td-otto", "thermo.first-law", "An air-standard Otto cycle ($k = 1.4$) has compression ratio {{rc}}. Find its thermal efficiency.",
              given={"rc": {"pick": [6, 8, 9, 10, 12]}}, value="1 - rc^(-0.4)", tex="\\eta", tol=0.0001,
              verify="1 - (2 - 1)/(2*rc**Rational(2, 5) - rc**Rational(2, 5))",
              explain="Both heat transfers are at constant volume, and the isentropic legs give $T_2/T_1 = r^{k-1}$; everything cancels but the compression ratio")]),
        L("B", "Find the air-standard Diesel efficiency.", "η = 1 − r^(1−k)(r_c^k − 1)/(k(r_c − 1)).", ["TH10.2"], [
            Q("td-diesel", "thermo.first-law", "An air-standard Diesel cycle ($k = 1.4$) has compression ratio {{r}} and cutoff ratio {{c}}. Find its efficiency.",
              given={"r": {"pick": [16, 18, 20]}, "c": {"pick": [1.5, 2, 2.5]}}, value="1 - r^(-0.4)*(c^1.4 - 1)/(1.4*(c - 1))", tex="\\eta", tol=0.0001,
              verify="1 - (nsimplify(c)**Rational(7, 5) - 1)/(Rational(7, 5)*(r**Rational(2, 5)*nsimplify(c) - r**Rational(2, 5)))",
              explain="Track temperatures with $T_1 = 1$: $T_2 = r^{k-1}$, $T_3 = r_cT_2$, $T_4 = r_c^k$. Heat in at constant pressure is $c_p(T_3 - T_2)$, heat out $c_v(T_4 - T_1)$")]),
        L("C", "Find the air-standard dual-cycle efficiency.", "Heat is added partly at constant volume (pressure ratio r_p), partly at constant pressure (cutoff r_c).", ["TH10.3"], [
            Q("td-dual", "thermo.first-law", "An air-standard dual cycle ($k = 1.4$) has compression ratio {{r}}, pressure ratio {{rp}} and cutoff ratio {{c}}. Find its efficiency.",
              given={"r": {"pick": [14, 16, 18]}, "rp": {"pick": [1.5, 2]}, "c": {"pick": [1.2, 1.5]}},
              value="1 - (rp*c^1.4 - 1)/(r^0.4*((rp - 1) + 1.4*rp*(c - 1)))", tex="\\eta", tol=0.0001,
              verify="1 - (nsimplify(rp)*nsimplify(c)**Rational(7, 5) - 1)/((r**Rational(2, 5)*nsimplify(rp) - r**Rational(2, 5)) + Rational(7, 5)*(r**Rational(2, 5)*nsimplify(rp)*nsimplify(c) - r**Rational(2, 5)*nsimplify(rp)))",
              explain="With $T_1 = 1$: $T_2 = r^{k-1}$, $T_x = r_pT_2$, $T_3 = r_cT_x$, $T_4 = r_pr_c^k$. Heat in is $c_v(T_x - T_2) + c_p(T_3 - T_x)$. It falls between Otto and Diesel")]),
        L("D", "Find the efficiency of a regenerated Stirling or Ericsson cycle.", "With perfect regeneration both reach the Carnot efficiency.", ["TH10.4"], [
            Q("td-stirling-regenerated", "thermo.first-law", "An ideal Stirling engine with a perfect regenerator runs between {{TH}} K and {{TL}} K. Find its efficiency.",
              given={"TH": {"pick": [600, 800, 1000]}, "TL": {"pick": [300, 350]}}, value="1 - TL/TH", tex="\\eta", tol=0.0001,
              verify="(Symbol('R')*TH*log(2) - Symbol('R')*TL*log(2))/(Symbol('R')*TH*log(2))",
              explain="Heat enters and leaves isothermally; the regenerator recycles the constant-volume heats internally. Work $= R(T_H - T_L)\\ln(V_2/V_1)$ over $RT_H\\ln(V_2/V_1)$")]),
        L("E", "Find the Brayton cycle efficiency.", "η = 1 − r_p^((1−k)/k).", ["TH10.5"], [
            Q("td-brayton", "thermo.first-law", "An ideal Brayton cycle ($k = 1.4$) has pressure ratio {{rp}}. Find its thermal efficiency.",
              given={"rp": {"pick": [6, 8, 10, 12, 16]}}, value="1 - rp^(-0.4/1.4)", tex="\\eta", tol=0.0001,
              verify="1 - (Symbol('T')*rp**Rational(2, 7) - Symbol('T'))/(Symbol('T')*rp**Rational(4, 7) - Symbol('T')*rp**Rational(2, 7))",
              explain="Heat in and out at constant pressure; the isentropic legs make $T_2/T_1 = T_3/T_4 = r_p^{(k-1)/k}$. Gas turbines live here")]),
        L("F", "Find the efficiency of a Brayton cycle with ideal regeneration.", "η = 1 − (T₁/T₃) r_p^((k−1)/k).", ["TH10.6"], [
            Q("td-brayton-regen", "thermo.first-law", "An ideal Brayton cycle ($k = 1.4$) with a perfect regenerator has $r_p = {{rp}}$, $T_1 = 300$ K and $T_3 = {{T3}}$ K. Find its efficiency.",
              given={"rp": {"pick": [4, 6, 8]}, "T3": {"pick": [1000, 1200, 1400]}}, value="1 - 300/T3*rp^(0.4/1.4)", tex="\\eta", tol=0.0001,
              verify="1 - (300*rp**Rational(2, 7) - 300)/(T3 - T3/rp**Rational(2, 7))",
              explain="The regenerator preheats compressed air with turbine exhaust, so heat in is $c_p(T_3 - T_4)$ and heat out $c_p(T_2 - T_1)$. Regeneration helps most at low pressure ratios")]),
        L("G", "Choose the intercooling pressure for minimum compressor work.", "Two stages with intercooling to T₁: P_x = √(P₁P₂).", ["TH10.7"], [
            Q("td-intercooling", "thermo.first-law", "Air is compressed in two stages from {{P1}} kPa to {{P2}} kPa with perfect intercooling. What intermediate pressure minimises the work, in kPa?",
              given={"P1": {"pick": [100, 200]}, "P2": {"pick": [900, 1600, 2500]}}, value="sqrt(P1*P2)", tex="P_x", tol=0.0001,
              verify="Max(*solve(diff((x/P1)**Rational(2, 7) + (P2/x)**Rational(2, 7), x), x))", explain="Equal pressure ratios across both stages split the work equally and minimise it")]),
        L("H", "Combine the efficiencies of a gas–steam cycle.", "η = η_gas + η_steam − η_gas η_steam when the steam cycle runs on the gas cycle's rejected heat.", ["TH10.8"], [
            Q("td-combined-cycle", "thermo.first-law", "A gas turbine with efficiency {{a}} rejects all its heat to a steam cycle of efficiency {{b}}. What is the combined efficiency?",
              given={"a": {"pick": [0.3, 0.35, 0.4]}, "b": {"pick": [0.3, 0.35, 0.4]}}, value="a + b - a*b", tex="\\eta", tol=0.0001,
              verify="(nsimplify(a) + nsimplify(b)*(1 - nsimplify(a)))", explain="Per unit of heat in, the gas turbine makes $\\eta_g$ and passes on $1 - \\eta_g$, of which the steam cycle converts $\\eta_s$")]),
        L("I", "Find the thrust of a turbojet.", "F = ṁ(V_exit − V_inlet).", ["TH10.9"], [
            Q("td-turbojet-thrust", "thermo.first-law", "A turbojet moves {{m}} kg/s of air, flying at {{V1}} m/s and exhausting at {{V2}} m/s relative to the engine. What is the thrust, in kN?",
              given={"m": {"pick": [50, 80, 120]}, "V1": {"pick": [200, 250]}, "V2": {"pick": [500, 600, 800]}}, value="m*(V2 - V1)/1000", tex="F", tol=0.0001,
              verify="solve(Eq(x*1000, m*V2 - m*V1), x)[0]", explain="Thrust is the momentum the engine adds to the air each second (ignoring fuel mass and pressure thrust)")]),
    ]),
    ("Refrigeration", [
        L("A", "Find the COP of a vapour-compression refrigerator.", "COP_R = (h₁ − h₄)/(h₂ − h₁).", ["TH11.1"], [
            Q("td-refrigeration-cop", "thermo.first-law", "A refrigerant leaves the evaporator at $h_1 = {{h1}}$ kJ/kg and the compressor at $h_2 = {{h2}}$ kJ/kg; it enters the evaporator at $h_4 = {{h4}}$ kJ/kg. Find the COP.",
              given={"h1": {"pick": [240, 245, 250]}, "h2": {"pick": [275, 280, 290]}, "h4": {"pick": [90, 100, 110]}}, value="(h1 - h4)/(h2 - h1)", tex="COP_R", tol=0.0001,
              verify="solve(Eq(x*(h2 - h1), h1 - h4), x)[0]", explain="Refrigeration effect over compressor work. The throttle makes $h_4 = h_3$, which is why it has no work term")]),
        L("B", "Find the COP of a gas (reversed Brayton) refrigeration cycle.", "COP = 1/(r_p^((k−1)/k) − 1).", ["TH11.2"], [
            Q("td-gas-refrigeration", "thermo.first-law", "An ideal reversed Brayton cycle ($k = 1.4$) has pressure ratio {{rp}}. Find its COP.",
              given={"rp": {"pick": [3, 4, 5, 6]}}, value="1/(rp^(0.4/1.4) - 1)", tex="COP", tol=0.0001,
              verify="(Symbol('T') - Symbol('T')/rp**Rational(2, 7))/((Symbol('T')*rp**Rational(2, 7) - Symbol('T')) - (Symbol('T') - Symbol('T')/rp**Rational(2, 7)))",
              explain="Gas cycles have low COPs but cool to very low temperatures and fly well (aircraft cabins)")]),
    ]),
]),
U(21, "psychrometrics", "Moist air and air conditioning", [
    ("Moist-air properties", [
        L("A", "Find the humidity ratio from an adiabatic-saturation (wet-bulb) reading.", "ω₁ = [c_p(T₂ − T₁) + ω₂h_fg₂]/(h_g₁ − h_f₂).", ["TH12.4"], [
            Q("td-wet-bulb", "thermo.first-law", "Air at {{T1}} °C passes through an adiabatic saturator and leaves saturated at {{T2}} °C with $\\omega_2 = {{w2}}$. With $c_p = 1.005$, $h_{fg2} = {{hfg2}}$, $h_{g1} = {{hg1}}$, $h_{f2} = {{hf2}}$ kJ/kg, find $\\omega_1$.",
              cases=[{"T1": 30, "T2": 20, "w2": 0.0147, "hfg2": 2453.5, "hg1": 2555.6, "hf2": 83.9}, {"T1": 35, "T2": 25, "w2": 0.0201, "hfg2": 2441.7, "hg1": 2564.6, "hf2": 104.8},
                     {"T1": 25, "T2": 15, "w2": 0.0107, "hfg2": 2465.4, "hg1": 2546.5, "hf2": 63.0}],
              value="(1.005*(T2 - T1) + w2*hfg2)/(hg1 - hf2)", tex="\\omega_1", tol=0.0001,
              verify="solve(Eq(Rational(1005, 1000)*T1 + x*nsimplify(hg1) + (nsimplify(w2) - x)*nsimplify(hf2), Rational(1005, 1000)*T2 + nsimplify(w2)*(nsimplify(hf2) + nsimplify(hfg2))), x)[0]",
              explain="An energy balance on the saturator: the air cools and the evaporated water carries the latent heat. The exit temperature is (very nearly) the wet-bulb temperature")]),
        L("B", "Find a dew point.", "T_dp is the saturation temperature at the vapour's partial pressure.", ["TH12.6"], [
            Q("td-dew-point", "thermo.first-law", "Air at {{T}} °C has relative humidity {{phi}}. Using the Magnus approximation $P_{sat}(T) = 0.6112\\,e^{17.62T/(243.12 + T)}$ kPa, find the dew point, in °C.",
              given={"T": {"pick": [20, 25, 30, 35]}, "phi": {"pick": [0.3, 0.5, 0.7, 0.9]}}, value="243.12*(log(phi) + 17.62*T/(243.12 + T))/(17.62 - (log(phi) + 17.62*T/(243.12 + T)))", tex="T_{dp}", tol=0.0001,
              verify="solve(Eq(Rational(1762, 100)*x/(Rational(24312, 100) + x), log(nsimplify(phi)) + Rational(1762, 100)*T/(Rational(24312, 100) + T)), x)[0]",
              explain="$P_v = \\phi P_{sat}(T)$; cool at constant $P_v$ until $P_{sat}(T_{dp}) = P_v$. Surfaces colder than this collect condensate")]),
        L("C", "Find the enthalpy of moist air.", "h = 1.005T + ω(2501 + 1.82T) kJ per kg dry air, T in °C.", ["TH12.7"], [
            Q("td-moist-enthalpy", "thermo.first-law", "Air at {{T}} °C has humidity ratio {{w}} kg/kg dry air. What is its enthalpy, in kJ per kg dry air?",
              given={"T": {"pick": [15, 25, 30, 35]}, "w": {"pick": [0.005, 0.01, 0.015, 0.02]}}, value="1.005*T + w*(2501 + 1.82*T)", tex="h", tol=0.0001,
              verify="integrate(Rational(1005, 1000), (x, 0, T)) + nsimplify(w)*(2501 + integrate(Rational(182, 100), (x, 0, T)))",
              explain="Dry air's sensible heat plus the water vapour's enthalpy (latent heat at 0 °C plus vapour sensible heat). The psychrometric chart tabulates exactly this")]),
    ]),
    ("Air-conditioning processes", [
        L("A", "Balance an air-conditioning process.", "Dry air is conserved; water and energy balances fix the heat and the condensate.", ["TH12.8", "TH12.10"], [
            Q("td-dehumidify-water", "thermo.first-law", "{{ma}} kg/s of dry air is cooled from $\\omega = {{w1}}$ to $\\omega = {{w2}}$. How much water condenses, in kg/min?",
              given={"ma": {"pick": [0.5, 1, 2]}, "w1": {"pick": [0.018, 0.02, 0.022]}, "w2": {"pick": [0.008, 0.01, 0.012]}}, value="ma*(w1 - w2)*60", tex="\\dot m_w", tol=0.0001,
              verify="solve(Eq(nsimplify(ma)*nsimplify(w1), nsimplify(ma)*nsimplify(w2) + x/60), x)[0]", explain="Water in = water out + condensate. Air is cooled below its dew point, then usually reheated"),
            Q("td-ac-heat", "thermo.first-law", "{{ma}} kg/s of dry air goes from $h = {{h1}}$ to $h = {{h2}}$ kJ/kg dry air, and {{mw}} kg/s of condensate leaves at $h_w = 42$ kJ/kg. What cooling load is needed, in kW?",
              given={"ma": {"pick": [1, 2, 3]}, "h1": {"pick": [70, 80, 90]}, "h2": {"pick": [30, 35, 40]}, "mw": {"pick": [0.005, 0.01, 0.02]}}, value="ma*(h1 - h2) - mw*42", tex="\\dot Q", tol=0.0001,
              verify="solve(Eq(nsimplify(ma)*h1, nsimplify(ma)*h2 + nsimplify(mw)*42 + x), x)[0]", explain="Energy in with the air equals energy out with the air, the condensate and the coil load"),
        ]),
        L("B", "Heat moist air at constant composition.", "Simple heating: ω constant, Q = ṁ_a c_p,moist ΔT.", ["TH12.9"], [
            Q("td-simple-heating", "thermo.first-law", "{{ma}} kg/s of dry air with $\\omega = {{w}}$ is heated from {{T1}} °C to {{T2}} °C. Find the heat input, in kW (use $h = 1.005T + \\omega(2501 + 1.82T)$).",
              given={"ma": {"pick": [0.5, 1, 2]}, "w": {"pick": [0.004, 0.006, 0.008]}, "T1": {"pick": [5, 10]}, "T2": {"pick": [22, 25, 30]}}, value="ma*(1.005 + 1.82*w)*(T2 - T1)", tex="\\dot Q", tol=0.0001,
              verify="nsimplify(ma)*((Rational(1005, 1000)*T2 + nsimplify(w)*(2501 + Rational(182, 100)*T2)) - (Rational(1005, 1000)*T1 + nsimplify(w)*(2501 + Rational(182, 100)*T1)))",
              explain="Nothing is added or removed, so the latent part cancels; relative humidity falls as the air warms")]),
        L("C", "Humidify air.", "Water added = ṁ_a(ω₂ − ω₁).", ["TH12.11", "TH12.14"], [
            Q("td-humidify", "thermo.first-law", "{{ma}} kg/s of dry air passes a humidifier (or a cooling tower) and its humidity ratio rises from {{w1}} to {{w2}}. How much water must be supplied, in kg/h?",
              given={"ma": {"pick": [1, 2, 5]}, "w1": {"pick": [0.004, 0.006, 0.01]}, "w2": {"pick": [0.012, 0.018, 0.024]}}, value="ma*(w2 - w1)*3600", tex="\\dot m_w", tol=0.0001,
              verify="solve(Eq(nsimplify(ma)*nsimplify(w1) + x/3600, nsimplify(ma)*nsimplify(w2)), x)[0]",
              explain="Every kilogram of water picked up by the air must be made up. In a cooling tower this evaporation is what cools the remaining water")]),
        L("D", "Find the outlet temperature of an evaporative cooler.", "The process is nearly at constant enthalpy (constant wet-bulb).", ["TH12.12"], [
            Q("td-evaporative-cooling", "thermo.first-law", "Hot dry air at {{T1}} °C with $\\omega = {{w1}}$ passes an evaporative cooler and leaves with $\\omega = {{w2}}$, at constant enthalpy. What is the exit temperature, in °C?",
              given={"T1": {"pick": [35, 40, 45]}, "w1": {"pick": [0.004, 0.006]}, "w2": {"pick": [0.01, 0.012, 0.014]}},
              value="(1.005*T1 + w1*(2501 + 1.82*T1) - w2*2501)/(1.005 + 1.82*w2)", tex="T_2", tol=0.0001,
              verify="solve(Eq(Rational(1005, 1000)*x + nsimplify(w2)*(2501 + Rational(182, 100)*x), Rational(1005, 1000)*T1 + nsimplify(w1)*(2501 + Rational(182, 100)*T1)), x)[0]",
              explain="The latent heat for evaporation comes out of the air's sensible heat. It works well only in dry climates")]),
        L("E", "Mix two moist air streams.", "ω₃ = (ṁ₁ω₁ + ṁ₂ω₂)/(ṁ₁ + ṁ₂); h₃ likewise.", ["TH12.13"], [
            Q("td-adiabatic-mixing", "thermo.first-law", "{{m1}} kg/s of air with $\\omega = {{w1}}$ mixes adiabatically with {{m2}} kg/s with $\\omega = {{w2}}$ (dry-air flows). Find $\\omega$ of the mixture.",
              given={"m1": {"pick": [1, 2, 3]}, "w1": {"pick": [0.005, 0.008]}, "m2": {"pick": [1, 2, 4]}, "w2": {"pick": [0.012, 0.016, 0.02]}}, value="(m1*w1 + m2*w2)/(m1 + m2)", tex="\\omega_3", tol=0.0001,
              verify="solve(Eq((m1 + m2)*x, m1*nsimplify(w1) + m2*nsimplify(w2)), x)[0]", explain="Mass-weighted averages of $\\omega$ and $h$: the mixture lies on the straight line between the two states on the chart")]),
    ]),
]),
U(22, "reacting", "Combustion, reacting systems and liquid-phase fugacity", [
    ("Combustion and reacting systems", [
        L("A", "Estimate an adiabatic flame temperature.", "Heat released heats the products: Σnᵢc_p,ᵢ(T − T₀) = LHV.", ["TH13.7"], [
            Q("td-flame-temperature", "thermo.first-law", "Methane burns in {{ex}}% theoretical air from 298 K. Take the products per mol fuel as 1 CO₂, 2 H₂O, {{7.52*ex/100}} N₂ and {{2*(ex/100 - 1)}} O₂ with mean $c_p$ = 54, 43, 33 and 35 J/mol·K, and LHV = 802 kJ/mol. Find the flame temperature, in K.",
              given={"ex": {"pick": [100, 120, 150, 200]}}, value="298 + 802000/(54 + 2*43 + 7.52*ex/100*33 + 2*(ex/100 - 1)*35)", tex="T_{ad}", tol=0.0001,
              verify="solve(Eq((54 + 86 + Rational(752, 100)*ex/100*33 + 2*(Rational(ex, 100) - 1)*35)*(x - 298), 802000), x)[0]",
              explain="All the heat stays in the products. Excess air adds mass to heat, so the flame is cooler; real flames are lower still from dissociation")]),
        L("B", "Find a mixture's lower flammability limit.", "Le Chatelier: LFL_mix = 1/Σ(yᵢ/LFLᵢ) with yᵢ the fuel-only fractions.", ["TH13.8"], [
            Q("td-le-chatelier", "thermo.first-law", "A fuel gas is {{y}}% methane (LFL 5.0%) and the rest propane (LFL 2.1%). Estimate the mixture's LFL, in vol%.",
              given={"y": {"pick": [20, 50, 70, 90]}}, value="1/(y/100/5 + (1 - y/100)/2.1)", tex="LFL", tol=0.0001,
              verify="1/(Rational(y, 100)/5 + (1 - Rational(y, 100))/Rational(21, 10))", explain="Each fuel contributes its share of 'distance to its own limit'. It is an estimate, best for similar fuels")]),
        L("C", "Find the temperature rise of an adiabatic batch reactor.", "ΔT_ad = (−ΔH_r) C₀ X / (ρ c_p).", ["TH13.10"], [
            Q("td-batch-adiabatic-rise", "thermo.first-law", "An adiabatic batch reactor holds a liquid ($\\rho c_p = {{rc}}$ kJ/m³·K) with {{C0}} mol/m³ of reactant; $\\Delta H_r = -{{dH}}$ kJ/mol. What is the temperature rise at full conversion, in K?",
              given={"rc": {"pick": [3500, 4000, 4180]}, "C0": {"pick": [500, 1000, 2000]}, "dH": {"pick": [50, 80, 150]}}, value="dH*C0/rc", tex="\\Delta T_{ad}", tol=0.0001,
              verify="solve(Eq(rc*x, dH*C0), x)[0]", explain="Energy released by reaction goes into the reactor contents. This number decides whether a runaway is credible")]),
        L("D", "Combine a reaction equilibrium with a phase equilibrium.", "Over pure liquid A, p_A = P_sat; then p_B = K p_A for A(g) ⇌ B(g).", ["TH13.11"], [
            Q("td-reaction-phase", "thermo.chemical-equilibrium", "Pure liquid A sits in a closed vessel; its vapour isomerises, A(g) ⇌ B(g), with $K = {{K}}$. $P_{sat,A} = {{Ps}}$ kPa. What is the partial pressure of B at equilibrium, in kPa?",
              given={"K": {"pick": [0.2, 0.5, 2, 4]}, "Ps": {"pick": [10, 20, 50]}}, value="K*Ps", tex="p_B", tol=0.0001,
              verify="solve(Eq(x/Ps, nsimplify(K)), x)[0]", explain="The liquid pins $p_A$ at its vapour pressure, so the gas-phase equilibrium sets $p_B$ directly")]),
        L("E", "Find the chemical exergy of a gas from its dilution.", "Per mole, RT₀ ln(1/y_env) for a gas present at mole fraction y_env in the environment.", ["TH13.13"], [
            Q("td-chemical-exergy", "thermo.first-law", "Pure CO₂ is compared with the atmosphere, where its mole fraction is {{y}}. At 298 K, what is its chemical exergy, in kJ/mol?",
              given={"y": {"pick": [0.0004, 0.0003, 0.01]}}, value="8.314*298*log(1/y)/1000", tex="x_{ch}", tol=0.0001,
              verify="integrate(Rational(8314, 1000)*298/x, (x, nsimplify(y), 1))/1000",
              explain="It is the work an ideal isothermal compressor could recover letting the pure gas expand to its partial pressure in air")]),
    ]),
    ("Liquids and solids at high pressure", [
        L("A", "Estimate a saturated-liquid volume with the Rackett equation.", "V_sat = V_c Z_c^((1 − T_r)^(2/7)).", ["TH15.7"], [
            Q("td-rackett", "thermo.phase-equilibrium", "A liquid has $V_c = {{Vc}}$ cm³/mol and $Z_c = {{Zc}}$. Estimate its saturated-liquid volume at $T_r = {{Tr}}$, in cm³/mol.",
              given={"Vc": {"pick": [150, 200, 250]}, "Zc": {"pick": [0.26, 0.27, 0.29]}, "Tr": {"pick": [0.5, 0.6, 0.7]}}, value="Vc*Zc^((1 - Tr)^(2/7))", tex="V_{sat}", tol=0.0001,
              verify="Vc*exp(log(nsimplify(Zc))*(1 - nsimplify(Tr))**Rational(2, 7))", explain="A generalised correlation for liquids: only critical properties go in")]),
        L("B", "Find the fugacity of a compressed liquid with the Poynting factor.", "f = φ_sat P_sat exp[V_L(P − P_sat)/RT].", ["TH15.12"], [
            Q("td-poynting-liquid", "thermo.phase-equilibrium", "A liquid ($V_L = {{V}}$ cm³/mol) has $P_{sat} = {{Ps}}$ bar at {{T}} K, and $\\phi_{sat} \\approx 1$. What is its fugacity at {{P}} bar, in bar?",
              given={"V": {"pick": [18, 50, 100]}, "Ps": {"pick": [0.5, 1, 2]}, "T": {"pick": [300, 350, 400]}, "P": {"pick": [50, 100, 300]}}, value="Ps*exp(V*(P - Ps)/(83.14*T))", tex="f", tol=0.0001,
              verify="nsimplify(Ps)*exp(integrate(V/(Rational(8314, 100)*T), (x, nsimplify(Ps), P)))", explain="From saturation, integrate $(\\partial\\ln f/\\partial P)_T = V/RT$ through the liquid. The correction is small unless the pressure is very high")]),
        L("C", "Find the Poynting factor for a solid.", "Same integral with the solid's molar volume and the sublimation pressure.", ["TH15.13"], [
            Q("td-poynting-solid", "thermo.phase-equilibrium", "A solid with molar volume {{V}} cm³/mol is pressurised from its tiny sublimation pressure to {{P}} bar at {{T}} K. By what factor does its fugacity rise?",
              given={"V": {"pick": [100, 150, 200]}, "P": {"pick": [100, 200, 300]}, "T": {"pick": [300, 320, 350]}}, value="exp(V*P/(83.14*T))", tex="PF", tol=0.0001,
              verify="exp(integrate(V/(Rational(8314, 100)*T), (x, 0, P)))", explain="Pressure raises a condensed phase's fugacity exponentially in $VP/RT$; this enhances solid solubility in supercritical fluids")]),
    ]),
    ("Multicomponent equilibrium", [
        L("A", "Find the boiling pressure of two immiscible liquids.", "Each liquid exerts its own vapour pressure: P = P₁sat + P₂sat.", ["TH16.5"], [
            Q("td-immiscible-liquids", "thermo.solutions", "Water ($P_{sat} = {{p1}}$ kPa) and an immiscible oil ($P_{sat} = {{p2}}$ kPa) share a vessel at the same temperature. What is the vapour's mole fraction of oil?",
              given={"p1": {"pick": [20, 47, 70]}, "p2": {"pick": [2, 5, 10]}}, value="p2/(p1 + p2)", tex="y_{oil}", tol=0.0001,
              verify="solve(Eq(x*(p1 + p2), p2), x)[0]", explain="With two liquid phases both pure, the total pressure is the sum and boils lower than either alone: the basis of steam distillation")]),
        L("B", "Find an ideal solid solubility.", "ln x = −(ΔH_fus/R)(1/T − 1/T_m).", ["TH16.7"], [
            Q("td-ideal-solubility", "thermo.solutions", "A solid melts at {{Tm}} K with $\\Delta H_{fus} = {{dH}}$ kJ/mol. What is its ideal mole-fraction solubility at {{T}} K?",
              given={"Tm": {"pick": [350, 400, 450]}, "dH": {"pick": [15, 20, 25]}, "T": {"pick": [298, 310]}}, value="exp(-dH*1000/8.314*(1/T - 1/Tm))", tex="x", tol=0.0001,
              verify="solve(Eq(log(x), -dH*1000/Rational(8314, 1000)*(Rational(1, T) - Rational(1, Tm))), x)[0]",
              explain="It depends only on the solute: melting point and heat of fusion. Higher-melting solids are less soluble in every ideal solvent")]),
        L("C", "Apply van der Waals mixing rules.", "a_mix = (Σyᵢ√aᵢ)², b_mix = Σyᵢbᵢ.", ["TH16.9"], [
            Q("td-mixing-rule", "thermo.phase-equilibrium", "A mixture is {{y}} mole fraction gas 1 ($a = {{a1}}$) and the rest gas 2 ($a = {{a2}}$), in the same units. Find $a_{mix}$ with $a_{12} = \\sqrt{a_1a_2}$.",
              given={"y": {"pick": [0.2, 0.5, 0.7]}, "a1": {"pick": [1.4, 2.3, 3.6]}, "a2": {"pick": [0.14, 0.5, 5.5]}}, value="(y*sqrt(a1) + (1 - y)*sqrt(a2))^2", tex="a_{mix}", tol=0.0001,
              verify="nsimplify(y)**2*nsimplify(a1) + 2*nsimplify(y)*(1 - nsimplify(y))*sqrt(nsimplify(a1)*nsimplify(a2)) + (1 - nsimplify(y))**2*nsimplify(a2)",
              explain="$a$ is quadratic in composition (pair interactions); the geometric-mean cross term is the classical combining rule")]),
        L("D", "Find a fugacity coefficient from the virial equation.", "ln φ = BP/RT.", ["TH16.10"], [
            Q("td-virial-fugacity", "thermo.phase-equilibrium", "A gas has $B = {{B}}$ cm³/mol at {{T}} K. What is its fugacity coefficient at {{P}} bar?",
              given={"B": {"pick": [-300, -150, -50, 20]}, "T": {"pick": [300, 350, 400]}, "P": {"pick": [5, 10, 20]}}, value="exp(B*P/(83.14*T))", tex="\\phi", tol=0.0001,
              verify="exp(integrate(B/(Rational(8314, 100)*T), (x, 0, P)))", explain="Integrate $(Z - 1)/P$ with $Z = 1 + BP/RT$. Negative $B$ (attraction) gives $\\phi < 1$")]),
    ]),
    ("Activity models", [
        L("A", "Use the van Laar model.", "ln γ₁ = A₁₂(A₂₁x₂/(A₁₂x₁ + A₂₁x₂))².", ["TH17.4"], [
            Q("td-van-laar", "thermo.solutions", "With van Laar parameters $A_{12} = {{a}}$, $A_{21} = {{b}}$, find $\\ln\\gamma_1$ at $x_1 = {{x1}}$.",
              given={"a": {"pick": [0.5, 1, 1.5]}, "b": {"pick": [0.8, 1.2, 2]}, "x1": {"pick": [0.2, 0.5, 0.8]}}, value="a*(b*(1 - x1)/(a*x1 + b*(1 - x1)))^2", tex="\\ln\\gamma_1", tol=0.0001,
              verify="diff((Symbol('n1') + Symbol('n2'))*nsimplify(a)*nsimplify(b)*(Symbol('n1')/(Symbol('n1') + Symbol('n2')))*(Symbol('n2')/(Symbol('n1') + Symbol('n2')))/(nsimplify(a)*Symbol('n1')/(Symbol('n1') + Symbol('n2')) + nsimplify(b)*Symbol('n2')/(Symbol('n1') + Symbol('n2'))), Symbol('n1')).subs({Symbol('n1'): nsimplify(x1), Symbol('n2'): 1 - nsimplify(x1)})",
              explain="$\\ln\\gamma_1$ is the partial molar derivative of $nG^E/RT = n A_{12}A_{21}x_1x_2/(A_{12}x_1 + A_{21}x_2)$; at infinite dilution it tends to $A_{12}$")]),
        L("B", "Use regular-solution (Scatchard–Hildebrand) theory.", "ln γ₁ = V₁Φ₂²(δ₁ − δ₂)²/RT.", ["TH17.5"], [
            Q("td-scatchard-hildebrand", "thermo.solutions", "A solute ($V_1 = {{V}}$ cm³/mol, $\\delta_1 = {{d1}}$ (J/cm³)$^{1/2}$) in a solvent with $\\delta_2 = {{d2}}$ has solvent volume fraction $\\Phi_2 = {{F}}$ at {{T}} K. Find $\\ln\\gamma_1$.",
              given={"V": {"pick": [90, 120, 150]}, "d1": {"pick": [18, 20, 24]}, "d2": {"pick": [14, 16, 29]}, "F": {"pick": [0.5, 0.8, 0.95]}, "T": {"pick": [298, 320]}},
              value="V*F^2*(d1 - d2)^2/(8.314*T)", tex="\\ln\\gamma_1", tol=0.0001, verify="V*nsimplify(F)**2*(d1 - d2)**2/(Rational(8314, 1000)*T)",
              explain="Like dissolves like: the closer the solubility parameters, the nearer γ is to 1. The theory only predicts positive deviations")]),
        L("C", "Use Wilson's equation.", "ln γ₁ = −ln(x₁ + Λ₁₂x₂) + x₂[Λ₁₂/(x₁ + Λ₁₂x₂) − Λ₂₁/(x₂ + Λ₂₁x₁)].", ["TH17.9"], [
            Q("td-wilson", "thermo.solutions", "With Wilson parameters $\\Lambda_{12} = {{L12}}$, $\\Lambda_{21} = {{L21}}$, find $\\ln\\gamma_1$ at $x_1 = {{x1}}$.",
              given={"L12": {"pick": [0.3, 0.6, 1.2]}, "L21": {"pick": [0.4, 0.8, 1.5]}, "x1": {"pick": [0.2, 0.5, 0.8]}},
              value="-log(x1 + L12*(1 - x1)) + (1 - x1)*(L12/(x1 + L12*(1 - x1)) - L21/((1 - x1) + L21*x1))", tex="\\ln\\gamma_1", tol=0.0001,
              verify="diff(-Symbol('n1')*log(Symbol('n1')/(Symbol('n1') + Symbol('n2')) + nsimplify(L12)*Symbol('n2')/(Symbol('n1') + Symbol('n2'))) - Symbol('n2')*log(Symbol('n2')/(Symbol('n1') + Symbol('n2')) + nsimplify(L21)*Symbol('n1')/(Symbol('n1') + Symbol('n2'))), Symbol('n1')).subs({Symbol('n1'): nsimplify(x1), Symbol('n2'): 1 - nsimplify(x1)})",
              explain="Wilson's local-composition model differentiates $nG^E/RT = -n_1\\ln(x_1 + \\Lambda_{12}x_2) - n_2\\ln(x_2 + \\Lambda_{21}x_1)$. It cannot show liquid–liquid splitting")]),
        L("D", "Use the NRTL model at infinite dilution.", "ln γ₁^∞ = τ₂₁ + τ₁₂ exp(−ατ₁₂).", ["TH17.10"], [
            Q("td-nrtl-infinite", "thermo.solutions", "NRTL parameters are $\\tau_{12} = {{t12}}$, $\\tau_{21} = {{t21}}$, $\\alpha = {{al}}$. Find $\\ln\\gamma_1^\\infty$.",
              given={"t12": {"pick": [0.5, 1, 1.5]}, "t21": {"pick": [0.3, 0.8, 2]}, "al": {"pick": [0.2, 0.3, 0.47]}}, value="t21 + t12*exp(-al*t12)", tex="\\ln\\gamma_1^\\infty", tol=0.0001,
              verify="limit(diff((Symbol('n1') + Symbol('n2'))*(Symbol('n1')/(Symbol('n1') + Symbol('n2')))*(Symbol('n2')/(Symbol('n1') + Symbol('n2')))*(nsimplify(t21)*exp(-nsimplify(al)*nsimplify(t21))/(Symbol('n1')/(Symbol('n1') + Symbol('n2')) + Symbol('n2')/(Symbol('n1') + Symbol('n2'))*exp(-nsimplify(al)*nsimplify(t21))) + nsimplify(t12)*exp(-nsimplify(al)*nsimplify(t12))/(Symbol('n2')/(Symbol('n1') + Symbol('n2')) + Symbol('n1')/(Symbol('n1') + Symbol('n2'))*exp(-nsimplify(al)*nsimplify(t12)))), Symbol('n1')).subs(Symbol('n2'), 1), Symbol('n1'), 0)",
              explain="Take NRTL's $G^E/RT = x_1x_2[\\tau_{21}G_{21}/(x_1 + x_2G_{21}) + \\tau_{12}G_{12}/(x_2 + x_1G_{12})]$, $G_{ij} = e^{-\\alpha\\tau_{ij}}$, differentiate and let $x_1 \\to 0$")]),
        L("E", "Know what group-contribution and other activity models need.", "UNIFAC: group volumes, areas and group interaction parameters; UNIQUAC: r and q plus binary energies; MOSCED: dispersion, polarity, induction and hydrogen-bond parameters.", ["TH17.7", "TH17.8", "TH17.11"], [
            Q("td-activity-models", "thermo.solutions", "{{q}}", pace="recall",
              cases=[{"q": "Which model predicts activity coefficients with no binary data for the pair, from functional groups alone?", "ans": 0},
                     {"q": "Which model splits ln γ into a combinatorial part from molecular size and shape (r, q) and a residual part from binary interaction energies?", "ans": 1},
                     {"q": "Which model predicts infinite-dilution activity coefficients from dispersion, polarity, induction and hydrogen-bond acidity and basicity parameters?", "ans": 2}],
              choice=["UNIFAC", "UNIQUAC", "MOSCED"], correct="ans", verify="authored",
              explain="UNIFAC is UNIQUAC built from groups instead of molecules, so it predicts unmeasured pairs. MOSCED extends regular-solution theory with polar and hydrogen-bonding terms")]),
    ]),
]),
]
