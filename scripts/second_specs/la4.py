"""Linear algebra on the MAA CUPM 2023 course area report (read in full, Nov 2026). EXISTING cites its essential (E)
and optional (O) core topics on the objectives outside the opl-fill block; unit 9's citations are in opl_specs/la.py."""
FILE, FRAMEWORK = "la-cupm2023", "linear-algebra"
C = lambda *x: [f"cupm-2023-la:{i}" for i in x]
ADD = []
EXISTING = {
    "LA-1.1.A": C("E1"), "LA-1.1.C": C("E1"), "LA-1.1.D": C("E1"), "LA-1.1.B": C("E2"), "LA-1.2.A": C("E3"), "LA-1.2.B": C("E5", "E1"),
    "LA-2.1.A": C("E4"), "LA-2.1.B": C("E4"), "LA-2.1.C": C("E4"), "LA-2.2.A": C("E4"), "LA-2.2.B": C("E4"),
    "LA-4.1.A": C("E5", "E9"), "LA-4.2.A": C("E5"), "LA-4.2.B": C("E9", "E5"), "LA-4.3.A": C("E9"), "LA-4.3.B": C("E9"),
    "LA-5.1.A": C("E8"), "LA-5.1.B": C("E8", "E9"), "LA-5.2.A": C("E8", "E9"), "LA-5.2.B": C("E8"), "LA-5.2.C": C("E8"),
    "LA-6.1.A": C("E10", "O2"), "LA-6.1.B": C("E11"), "LA-6.2.A": C("E10"), "LA-6.2.B": C("E10"), "LA-6.2.C": C("O2"),
    "LA-7.1.A": C("O3"), "LA-7.1.B": C("O4"), "LA-7.2.A": C("O4"), "LA-7.2.B": C("O4"), "LA-7.3.A": C("O3"), "LA-7.3.B": C("O3"), "LA-7.3.C": C("E11", "O3"),
    "LA-8.1.A": C("E6"), "LA-8.1.B": C("E6", "E4"), "LA-8.1.C": C("E6"), "LA-8.2.A": C("E6", "E7"), "LA-8.2.B": C("E6", "E9"), "LA-8.2.C": C("E6", "E7", "E8"),
}

from opl_dsl import Q
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]

OBJS = [
    ("LA-1.1.E", C("E2", "E9"), "Decide independence by counting: rank, the number of vectors and the dimension of the space.",
     "More than n vectors in Rⁿ are always dependent; n vectors in Rⁿ are independent exactly when the matrix they form has nonzero determinant (rank n)."),
    ("LA-1.2.C", C("E3", "E5"), "Describe a span geometrically and find its dimension.",
     "The span of vectors in R³ is a point, a line, a plane or all of R³, as its dimension (the rank) is 0, 1, 2 or 3."),
    ("LA-6.1.C", C("E11", "E10"), "Fit a least-squares line with the normal equations and read its residuals.",
     "Solve AᵀA c = Aᵀy for c = (b, m); the residual vector is orthogonal to every column of A, so its entries sum to zero when an intercept is fitted."),
]

ADD = [
    ("LA-1.1.E", Q("la-indep-det", "la.independence", "For which value of k are the vectors (1, 2, 0), (0, 1, {{a}}) and (k, 0, 1) linearly dependent?",
        given={"a": {"pick": [1, 2, 3, -1]}}, value="-1/(2*a)", tex="k",
        verify="solve(Matrix([[1, 0, x], [2, 1, 0], [0, a, 1]]).det(), x)[0]",
        explain="Three vectors in R³ are dependent exactly when the determinant of the matrix with them as columns is zero")),
    ("LA-1.1.E", Q("la-indep-count", "la.independence", "A set has {{m}} vectors in R^{{n}} whose matrix has rank {{r}}. How many of the vectors can be removed, at most, without shrinking the span?",
        cases=[{"m": 5, "n": 3, "r": 3}, {"m": 4, "n": 4, "r": 2}, {"m": 3, "n": 5, "r": 3}, {"m": 6, "n": 4, "r": 4}],
        value="m - r", tex="N", final=True, verify="m - Min(r, n, m)",
        explain="The span has dimension r, so r independent vectors carry it and the other m − r are redundant")),
    ("LA-1.2.C", Q("la-span-dim", "la.span", "What is the dimension of the span of (1, 2, {{a}}), (2, 4, {{b}}) and (0, 0, 1)?",
        cases=[{"a": 3, "b": 6}, {"a": 1, "b": 5}, {"a": 0, "b": 0}, {"a": 2, "b": 1}],
        value="2", tex="\\dim", final=True, verify="Matrix([[1, 2, a], [2, 4, b], [0, 0, 1]]).rank()",
        explain="The first two vectors agree in their first two entries up to the factor 2, and (0, 0, 1) fills in the third: the span is a plane")),
    ("LA-1.2.C", Q("la-span-shape", "la.span", "Vectors in R³ form a matrix of rank {{r}}. What does their span look like? (Answer 0 for a point, 1 for a line through the origin, 2 for a plane through the origin, 3 for all of R³.)",
        given={"r": {"pick": [1, 2, 3]}}, value="r", tex="\\text{shape}", final=True, verify="Integer(r)",
        explain="The span is a subspace of dimension equal to the rank: lines and planes always pass through the origin")),
    ("LA-6.1.C", Q("la-lsq-slope", "la.least-squares", "Fit y = b + mx by least squares to the points (0, {{y0}}), (1, {{y1}}), (2, {{y2}}), (3, {{y3}}). What is the slope m?",
        given={"y0": {"pick": [1, 2]}, "y1": {"pick": [2, 3, 4]}, "y2": {"pick": [4, 5]}, "y3": {"pick": [5, 7, 8]}},
        value="(3*y3 + y2 - y1 - 3*y0)/10", tex="m",
        verify="((Matrix([[1, 0], [1, 1], [1, 2], [1, 3]]).T*Matrix([[1, 0], [1, 1], [1, 2], [1, 3]])).inv()*Matrix([[1, 0], [1, 1], [1, 2], [1, 3]]).T*Matrix([y0, y1, y2, y3]))[1]",
        explain="Normal equations AᵀA c = Aᵀy; with x = 0, 1, 2, 3 the slope is Σ(x − x̄)(y − ȳ)/Σ(x − x̄)²")),
    ("LA-6.1.C", Q("la-lsq-residual-sum", "la.least-squares", "A least-squares line with an intercept is fitted to {{n}} points; the first {{k}} residuals sum to {{s}}. What is the sum of the remaining residuals?",
        given={"n": {"pick": [5, 8]}, "k": {"pick": [2, 3]}, "s": {"pick": [1.5, -2.25, 0.8]}}, value="-s", tex="\\sum e",
        verify="-nsimplify(s)", explain="The residual vector is orthogonal to the column of ones, so all residuals sum to zero")),
]
