from opl_dsl import Q, L, U

FW, FILE, IDEA = "MB", "opl-mb", "CONSERVE"

UNITS = [
U(6, "multiunit", "Multiunit balances and degrees of freedom", [
    ("Flowsheets", [
        L("A", "Solve a two-unit separation train.", "Balance each unit in turn; a component's recovery multiplies through units in series.", ["MB2.3"], [
            Q("mb-two-column", "meb.nonreactive", "A feed of {{F}} mol/h with {{z}} mole fraction A goes to column 1, which sends {{r1}} of the A to its top product; the bottoms go to column 2, which recovers {{r2}} of the A it receives overhead. How much A leaves in the two top products together, in mol/h?",
              given={"F": {"pick": [100, 200, 500]}, "z": {"pick": [0.3, 0.4, 0.5]}, "r1": {"pick": [0.8, 0.9]}, "r2": {"pick": [0.7, 0.85]}},
              value="F*z*(r1 + (1 - r1)*r2)", tex="\\dot n_A", tol=0.0001,
              verify="solve(Eq(x + nsimplify(F)*nsimplify(z)*(1 - nsimplify(r1))*(1 - nsimplify(r2)), nsimplify(F)*nsimplify(z)), x)[0]",
              explain="Column 1 takes $r_1$ of the A; column 2 takes $r_2$ of what is left. Check against the overall balance: what escapes both is $(1 - r_1)(1 - r_2)$ of the feed")]),
        L("B", "Count degrees of freedom for an energy balance.", "DOF = unknowns − independent equations; the energy balance adds one equation and usually one unknown (Q or a temperature).", ["MB4.1"], [
            Q("mb-energy-dof", "meb.energy", "A heat exchanger problem has {{u}} unknown stream variables plus an unknown duty Q. You can write {{e}} independent material balances and relations, plus one energy balance. How many more specifications are needed?",
              given={"u": {"int": [4, 8]}, "e": {"int": [2, 5]}}, require=["u + 1 - e - 1 > 0"], value="u + 1 - e - 1", tex="DOF", final=True,
              verify="(u + 1) - (e + 1)", explain="Count every unknown, including Q, and every independent equation, including the energy balance. Zero means the problem is specified")]),
    ]),
]),
]
