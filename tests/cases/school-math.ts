// Student-style answers for the K–12 mathematics drills (run by tests/run.ts).
// Each case is built with the same answer helpers the generators use (src/drills/school.ts).
import type { Answer, Problem } from "../../src/drills/types";
import { Q } from "../../src/drills/rational";
import { approx, exact, tuple } from "../../src/drills/school";

const mk = (answer: Answer): Problem => ({ skill: "t", template: "t", level: 1, prompt: "", answerTex: "", steps: [], answer });

export const SCHOOL_MATH_CASES: [string, Problem, (string | string[])[], (string | string[])[]][] = [
  [
    "exact fraction 7/3 (any equivalent form, but not a rounded decimal or a spaced mixed number)",
    mk(exact(new Q(7, 3))),
    ["7/3", "14/6", "2 + 1/3", "2.3333333333", "(7)/(3)", "x = 7/3"],
    ["2.33", "7/4", "2 1/3", "3/7"],
  ],
  [
    "large exact integer: off by 0.01 is wrong",
    mk(exact(154883)),
    ["154883", "154883.0", "150000 + 4883"],
    ["154883.01", "154882", "15488.3"],
  ],
  [
    "exact decimal from money arithmetic",
    mk(exact(new Q(5969, 1000))),
    ["5.969", "5969/1000"],
    ["5.97", "5.96", "59.69"],
  ],
  [
    "answer in terms of π, or rounded to 2 decimals",
    mk(approx("25*pi", Math.max(5e-4, 0.0051 / (25 * Math.PI)))),
    ["25pi", "25π", "25*pi", "78.54", "78.5398"],
    ["78.5", "50pi", "25", "-25pi"],
  ],
  [
    "tolerance answers typed with a root or a log keep it (not stripped as a unit)",
    mk(approx("sqrt(20)", 0.002)),
    ["2sqrt(5)", "sqrt(20)", "2√5", "4.472", "4.47 cm"],
    ["2", "4.4", "sqrt(5)"],
  ],
  [
    "small π answer to 2 decimals (rounding allowed)",
    mk(approx("pi/3", Math.max(5e-4, 0.0051 / (Math.PI / 3)))),
    ["pi/3", "1.05", "1.0472", "π/3"],
    ["1.1", "1", "pi/6"],
  ],
  [
    "scientific notation",
    mk(approx(0.000362, 1e-6)),
    ["3.62e-4", "3.62 x 10^-4", "3.62*10^(-4)", "0.000362", "362 × 10^-6"],
    ["3.62e-5", "3.6e-4", "-3.62e-4"],
  ],
  [
    "exact trig value -√3/2",
    mk({ kind: "expression", ref: "-(sqrt(3)/2)", vars: [], label: "cos", tol: 1e-9 }),
    ["-sqrt(3)/2", "-√3/2", "-(3^(1/2))/2", "-0.8660254038"],
    ["sqrt(3)/2", "-1/2", "-0.866"],
  ],
  [
    "radians in terms of π",
    mk({ kind: "expression", ref: "3/4*pi", vars: [], label: "radians", tol: 1e-9 }),
    ["3pi/4", "3π/4", "0.75pi", "(3/4)*pi"],
    ["3/4", "135", "pi/4"],
  ],
  [
    "rearranged formula P = 2l + 2w for w",
    mk({ kind: "expression", ref: "(P - 2*l)/2", vars: ["P", "l"], label: "w" }),
    ["(P - 2l)/2", "P/2 - l", "w = (P-2*l)/2", "0.5P - l"],
    ["P - 2l", "(P - l)/2", "(P - 2w)/2"],
  ],
  [
    "explicit formula for 5, 8, 11, … at integer n",
    mk({ kind: "expression", ref: "5 + (n-1)*(3)", vars: ["n"], label: "a_n", points: [1, 2, 3, 4, 5, 6, 7].map((n) => ({ n })) }),
    ["3n + 2", "a_n = 3n+2", "5 + 3(n - 1)"],
    ["3n + 5", "5 + 3n", "3^n + 2"],
  ],
  [
    "geometric explicit formula 3, 6, 12, …",
    mk({ kind: "expression", ref: "3*(2)^(n-1)", vars: ["n"], label: "a_n", points: [1, 2, 3, 4, 5, 6, 7].map((n) => ({ n })) }),
    ["3*2^(n-1)", "1.5*2^n", "a_n = 3(2)^(n - 1)"],
    ["3*2^n", "6^(n-1)", "3 + 3(n-1)"],
  ],
  [
    "transformed function g(x) = 2(x − 3)² − 3",
    mk({ kind: "expression", ref: "2*((x - 3))^2 + -3", vars: ["x"], label: "g(x)" }),
    ["2(x-3)^2 - 3", "g(x) = 2x^2 - 12x + 15", "2(3 - x)^2 - 3"],
    ["2(x+3)^2 - 3", "(x-3)^2 - 3", "2(x-3)^2 + 3"],
  ],
  [
    "inverse with a cube root",
    mk({ kind: "expression", ref: "cbrt((x - (-4))/2)", vars: ["x"], label: "f^{-1}(x)" }),
    ["cbrt((x+4)/2)", "((x + 4)/2)^(1/3)", "f^-1(x) = cbrt(x/2 + 2)"],
    ["cbrt(x/2) + 4", "((x - 4)/2)^(1/3)", "(x+4)/2"],
  ],
  [
    "log identity in u = log_b 2, v = log_b 3",
    mk({ kind: "expression", ref: "2*u + 1*v + 1", vars: ["u", "v"], label: "log" }),
    ["2u + v + 1", "u + u + v + 1", "1 + v + 2*u"],
    ["2u + v", "u^2 + v + 1", "2u + 3v + 1"],
  ],
  [
    "polynomial division: quotient as an expression, remainder as a number",
    mk(tuple([{ label: "q(x)", tex: "q(x)", ref: "(-3)*x^2 + (3)*x^1 + (6)*x^0" }, { label: "r", tex: "r", ref: 5 }], ["x"])),
    [["-3x^2 + 3x + 6", "5"], ["q(x) = -3(x^2 - x - 2)", "r = 5"]],
    [["-3x^2 + 3x + 6", "-5"], ["-3x^2 + 3x", "5"], ["-3x^2 + 3x + 6 + 5/(x+1)", "5"]],
  ],
  [
    "quadratic-formula roots, any order, exact",
    mk({ kind: "roots", ref: [(7 + Math.sqrt(61)) / 2, (7 - Math.sqrt(61)) / 2], label: "x" }),
    ["(7 + sqrt(61))/2, (7 - sqrt(61))/2", "x = (7 - √61)/2 and x = (7 + √61)/2", "3.5 + sqrt(61)/2, 3.5 - sqrt(61)/2"],
    ["(7 + sqrt(61))/2", "7.405, -0.405", "(-7 + sqrt(61))/2, (-7 - sqrt(61))/2"],
  ],
  [
    "trig equation: inverse-sine answers typed exactly",
    mk({ kind: "roots", ref: [Math.asin(0.4), Math.PI - Math.asin(0.4)], label: "x" }),
    ["asin(0.4), pi - asin(0.4)", "arcsin(0.4), π - arcsin(0.4)"],
    ["asin(0.4)", "asin(0.4), 2pi - asin(0.4)", "0.41, 2.73"],
  ],
  [
    "vector sum: magnitude and direction to 2 decimals",
    mk(tuple([{ label: "magnitude", tex: "m", ref: 19.659649062935802, mode: "number" }, { label: "direction°", tex: "\\theta", ref: 75, mode: "number" }])),
    [["19.66", "75"], ["19.6596", "75.00"]],
    [["19.66", "255"], ["19.5", "75"], ["24", "75"]],
  ],
  [
    "tens and ones",
    mk(tuple([{ label: "tens", tex: "t", ref: 6 }, { label: "ones", tex: "o", ref: 3 }])),
    [["6", "3"]],
    [["3", "6"], ["60", "3"]],
  ],
];
