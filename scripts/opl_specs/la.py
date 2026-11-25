from opl_dsl import Q, L, U

FW, FILE, IDEA = "LA", "opl-la", "MAIN"

UNITS = [U(9, "abstract", "Abstract vector spaces and special matrices", [
    ("Abstract vector spaces", [
        L("A", "Decide whether a set with its operations is a vector space.", "Check the zero vector, closure under addition and under scaling; the rest of the axioms usually come free.", ["LA6.1", "LA6.5"], [
            Q("la-is-vector-space", "la.subspaces", "Is {{q}} a vector space under the usual addition and scalar multiplication?", pace="recall",
              cases=[{"q": "the polynomials of degree at most 3", "ans": 0}, {"q": "the polynomials of degree exactly 3", "ans": 1},
                     {"q": "the 2 × 2 symmetric matrices", "ans": 0}, {"q": "the invertible 2 × 2 matrices", "ans": 1},
                     {"q": "the functions on [0, 1] with f(0) = 0", "ans": 0}, {"q": "the functions on [0, 1] with f(0) = 1", "ans": 1},
                     {"q": "the solutions of y″ + y = 0", "ans": 0}, {"q": "the solutions of y″ + y = 1", "ans": 1},
                     {"q": "the 2 × 2 matrices with trace 0", "ans": 0}, {"q": "the positive real numbers", "ans": 1}],
              choice=["Yes", "No"], correct="ans", verify="authored",
              explain="Ask whether the zero element is in the set and whether sums and multiples stay in it. Degree exactly 3 fails (the sum of x³ and −x³ is 0); invertible matrices miss the zero matrix; a nonhomogeneous condition (f(0) = 1, y″ + y = 1) fails closure.")]),
        L("B", "Write a polynomial as a combination of other polynomials.", "Match coefficients of each power and solve the linear system.", ["LA6.2"], [
            Q("la-poly-combination", "la.span", "Write $p = {{a + c}} + ({{a + b}})t + ({{b + c}})t^2$ as $c_1(1 + t) + c_2(t + t^2) + c_3(1 + t^2)$. What is $c_2$?",
              given={"a": {"int": [-4, 5]}, "b": {"int": [-4, 5]}, "c": {"int": [-4, 5]}}, require=["b != 0"], value="b", tex="c_2",
              verify="(Matrix([[1, 0, 1], [1, 1, 0], [0, 1, 1]]).inv()*Matrix([a + c, a + b, b + c]))[1]",
              explain="Match constants, $t$ and $t^2$: $c_1 + c_3 = {{a + c}}$, $c_1 + c_2 = {{a + b}}$, $c_2 + c_3 = {{b + c}}$. In coordinates on $\\{1, t, t^2\\}$ this is an ordinary $3 \\times 3$ system")]),
        L("C", "Decide whether a polynomial lies in the span of others.", "In the span exactly when the coefficient system is consistent.", ["LA6.3"], [
            Q("la-poly-span", "la.span", "Is ${{a}} + ({{b}})t + ({{a + b + e}})t^2$ in the span of $1 + t^2$ and $t + t^2$?", pace="quick",
              given={"a": {"int": [-4, 5]}, "b": {"int": [-4, 5]}, "e": {"pick": [0, 0, 1, -2]}}, choice=["Yes", "No"], correct="e == 0 ? 0 : 1",
              verify="0 if Matrix([[1, 0], [0, 1], [1, 1]]).rank() == Matrix([[1, 0, a], [0, 1, b], [1, 1, a + b + e]]).rank() else 1",
              explain="$c_1(1 + t^2) + c_2(t + t^2)$ has constant $c_1$, $t$-coefficient $c_2$ and $t^2$-coefficient $c_1 + c_2$. So the $t^2$ coefficient must equal ${{a}} + ({{b}})$")]),
        L("D", "Decide when polynomials are linearly dependent.", "Dependent exactly when the matrix of their coefficient vectors is singular.", ["LA6.4"], [
            Q("la-poly-dependence", "la.independence", "For which $h$ are $1 + {{a}}t + t^2$, $t + {{b}}t^2$ and $1 + ht$ linearly dependent?",
              given={"a": {"int": [-3, 4]}, "b": {"int": [-3, 4]}}, require=["b != 0"], value="a - 1/b", tol=0.0001, tex="h",
              verify="solve(Matrix([[1, a, 1], [0, 1, b], [1, x, 0]]).det(), x)[0]",
              explain="Write each as a coefficient vector on $\\{1, t, t^2\\}$ and set the determinant to zero: $-b(h - a) - 1 = 0$, so $h = {{a}} - 1/{{b}}$")]),
        L("E", "Find the dimension of a standard space of matrices or polynomials.", "Count the free entries: symmetric n(n+1)/2, skew n(n−1)/2, trace zero n² − 1, P_n has n + 1.", ["LA6.8"], [
            Q("la-space-dimension", "la.subspaces", "What is the dimension of the space of {{q}}, with $n = {{n}}$?", pace="recall",
              given={"n": {"int": [2, 6]}},
              cases=[{"q": "n × n symmetric matrices", "kd": 0}, {"q": "n × n skew-symmetric matrices", "kd": 1},
                     {"q": "n × n matrices with trace 0", "kd": 2}, {"q": "polynomials of degree at most n", "kd": 3},
                     {"q": "n × n upper-triangular matrices", "kd": 4}],
              value="kd == 0 ? n*(n + 1)/2 : (kd == 1 ? n*(n - 1)/2 : (kd == 2 ? n^2 - 1 : (kd == 3 ? n + 1 : n*(n + 1)/2)))", tex="\\dim",
              verify="summation(Symbol('i'), (Symbol('i'), 1, n)) if kd in (0, 4) else (summation(Symbol('i') - 1, (Symbol('i'), 1, n)) if kd == 1 else (n**2 - 1 if kd == 2 else n + 1))",
              explain="Count the entries you may choose freely. A symmetric matrix is fixed by its diagonal and upper triangle; a skew one by the strict upper triangle; trace zero removes one condition from $n^2$")]),
        L("F", "Compute an inner product of functions.", "⟨f, g⟩ = ∫ f g dx is an inner product on continuous functions.", ["LA8.2"], [
            Q("la-function-inner-product", "la.orthogonality", "With $\\langle f, g\\rangle = \\int_0^1 f(t)g(t)\\,dt$, find $\\langle {{a}} + {{b}}t,\\; {{c}} + t\\rangle$.",
              given={"a": {"int": [-3, 4]}, "b": {"int": [-3, 4]}, "c": {"int": [-3, 4]}}, require=["a*c + (a + b*c)/2 + b/3 != 0"],
              value="a*c + (a + b*c)/2 + b/3", tex="\\langle f, g\\rangle", verify="integrate((a + b*x)*(c + x), (x, 0, 1))",
              explain="Multiply and integrate: $\\int_0^1 ({{a*c}} + ({{a}} + {{b*c}})t + {{b}}t^2)\\,dt$. Orthogonal functions are the ones with zero inner product, which is how Fourier series and Legendre polynomials are built")]),
    ]),
    ("Special matrices and applications", [
        L("A", "Balance a chemical equation from the null space of its composition matrix.", "Each element gives one equation; the coefficients span the null space.", ["LA1.7"], [
            Q("la-balance-combustion", "la.span", "Balance the combustion of $\\mathrm{C_{ {{n}} }H_{ {{2*n + 2}} }}$ with the smallest whole numbers. What is the coefficient of $\\mathrm{O_2}$?",
              given={"n": {"int": [1, 8]}}, value="mod(n, 2) == 1 ? (3*n + 1)/2 : 3*n + 1", final=True, tex="\\nu_{O_2}",
              verify="(Matrix([[n, 0, -1, 0], [2*n + 2, 0, 0, -2], [0, 2, -2, -1]]).nullspace()[0][1]/Matrix([[n, 0, -1, 0], [2*n + 2, 0, 0, -2], [0, 2, -2, -1]]).nullspace()[0][0]).p",
              explain="Rows are C, H and O balances on (fuel, O₂, CO₂, H₂O). The null space gives O₂/fuel = $(3n + 1)/2$; clear the fraction. Balancing equations is a homogeneous linear system")]),
        L("B", "Invert an elementary matrix.", "The inverse undoes the row operation: add −k instead of k, divide instead of multiply, swap back.", ["LA2.7"], [
            Q("la-elementary-inverse", "la.inverse", "$E$ adds ${{k}}$ times row 1 to row 3 of a $3 \\times 3$ matrix. What is the (3, 1) entry of $E^{-1}$?", pace="recall",
              given={"k": {"pick": [-5, -3, -2, 2, 3, 4, 7]}}, value="-k", tex="(E^{-1})_{31}", verify="Matrix([[1, 0, 0], [0, 1, 0], [k, 0, 1]]).inv()[2, 0]",
              explain="$E$ is the identity with ${{k}}$ in position (3, 1). Undo it by subtracting ${{k}}$ times row 1. Row reduction is a product of elementary matrices, which is where $A = LU$ comes from")]),
        L("C", "Compute with complex matrix entries.", "Arithmetic is ordinary arithmetic with i² = −1; conjugates pair up into real numbers.", ["LA2.8"], [
            Q("la-complex-det", "la.determinant", "Find $\\det\\begin{pmatrix} {{a}} + {{b}}i & {{c}} \\\\ {{d}} & {{a}} - {{b}}i \\end{pmatrix}$.",
              given={"a": {"int": [-3, 4]}, "b": {"int": [1, 4]}, "c": {"int": [-3, 3]}, "d": {"int": [-3, 3]}}, require=["a^2 + b^2 - c*d != 0"],
              value="a^2 + b^2 - c*d", tex="\\det", verify="expand(Matrix([[a + b*I, c], [d, a - b*I]]).det())",
              explain="$(a + bi)(a - bi) = a^2 + b^2$, real; subtract ${{c}}\\cdot{{d}}$. Hermitian and unitary matrices are the complex versions of symmetric and orthogonal ones")]),
        L("D", "Compute a power of a Jordan block.", "[[λ, 1], [0, λ]]ᵏ = [[λᵏ, kλᵏ⁻¹], [0, λᵏ]].", ["LA3.5"], [
            Q("la-jordan-power", "la.diagonalization", "$J = \\begin{pmatrix} {{l}} & 1 \\\\ 0 & {{l}} \\end{pmatrix}$ cannot be diagonalised. Find the (1, 2) entry of $J^{ {{k}} }$.",
              given={"l": {"pick": [-2, -1, 2, 3]}, "k": {"int": [2, 5]}}, value="k*l^(k - 1)", tex="(J^k)_{12}", verify="(Matrix([[l, 1], [0, l]])**k)[0, 1]",
              explain="Write $J = \\lambda I + N$ with $N^2 = 0$; the binomial theorem stops after two terms: $J^k = \\lambda^kI + k\\lambda^{k-1}N$. That extra factor $k$ is where $te^{\\lambda t}$ comes from in repeated-root ODEs")]),
        L("E", "Use the properties of an orthogonal matrix.", "Qᵀ Q = I, so Q⁻¹ = Qᵀ and lengths and angles are preserved.", ["LA8.6"], [
            Q("la-orthogonal-inverse", "la.orthogonality", "$Q = \\frac{1}{ {{n}} }\\begin{pmatrix} {{p}} & {{-q}} \\\\ {{q}} & {{p}} \\end{pmatrix}$ is orthogonal. What is the (1, 2) entry of $Q^{-1}$?",
              cases=[{"p": 3, "q": 4, "n": 5}, {"p": 5, "q": 12, "n": 13}, {"p": 8, "q": 6, "n": 10}, {"p": 4, "q": -3, "n": 5}, {"p": 12, "q": 5, "n": 13}],
              value="q/n", tex="(Q^{-1})_{12}", verify="(Matrix([[p, -q], [q, p]])/n).inv()[0, 1]",
              explain="For an orthogonal matrix the inverse is the transpose, so $(Q^{-1})_{12} = Q_{21}$. No determinant or row reduction needed")]),
        L("F", "Invert a linear transformation.", "T is invertible exactly when its matrix is; T⁻¹ has the inverse matrix.", ["LA9.6"], [
            Q("la-map-inverse", "la.transformations", "$T(x, y) = ({{a}}x + ({{b}})y,\\; ({{c}})x + {{d}}y)$. Find the first component of $T^{-1}({{p}}, {{q}})$.",
              given={"a": {"int": [1, 4]}, "b": {"int": [-3, 3]}, "c": {"int": [-3, 3]}, "d": {"int": [1, 4]}, "p": {"int": [-5, 6]}, "q": {"int": [-5, 6]}},
              require=["a*d - b*c != 0", "d*p - b*q != 0"], value="(d*p - b*q)/(a*d - b*c)", tex="x",
              verify="solve([Eq(a*x + b*Symbol('Y'), p), Eq(c*x + d*Symbol('Y'), q)], [x, Symbol('Y')])[x]",
              explain="Solving $T(x, y) = ({{p}}, {{q}})$ is applying $T^{-1}$: $x = \\dfrac{dp - bq}{ad - bc}$. If $ad - bc = 0$ the map squashes the plane onto a line and has no inverse")]),
    ]),
])]

# LACSG 2.0 citations (read through the AMS Notices survey, 2022): objective id within each topic -> items
_LACSG = {("Abstract vector spaces", "A"): ["lacsg-2:S1", "cupm-2023-la:E7"], ("Abstract vector spaces", "B"): ["cupm-2023-la:E7"],
          ("Abstract vector spaces", "C"): ["cupm-2023-la:E7", "cupm-2023-la:E3"], ("Abstract vector spaces", "D"): ["cupm-2023-la:E7", "cupm-2023-la:E2"],
          ("Abstract vector spaces", "E"): ["cupm-2023-la:E7", "cupm-2023-la:E9"], ("Abstract vector spaces", "F"): ["lacsg-2:S3", "cupm-2023-la:O1"],
          ("Special matrices and applications", "A"): ["cupm-2023-la:E5"], ("Special matrices and applications", "B"): ["cupm-2023-la:E4"],
          ("Special matrices and applications", "D"): ["lacsg-2:S7"], ("Special matrices and applications", "E"): ["cupm-2023-la:O4"],
          ("Special matrices and applications", "F"): ["lacsg-2:F2", "cupm-2023-la:E6"]}
for _u in UNITS:
    for _t, _los in _u.topics:
        for _lo in _los:
            _lo.std = list(_lo.std) + [s for s in _LACSG.get((_t, _lo.id), []) if s not in _lo.std]
UNITS[0].std = ["webwork-opl:LA1.7", "webwork-opl:LA2.7", "webwork-opl:LA2.8"]  # keep the unit citation as before
