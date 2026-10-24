// Student-style answers for the Laplace / Fourier / PDE drills (run by tests/run.ts).
import type { Answer, Problem } from "../../src/drills/types";

const mk = (answer: Answer): Problem => ({ skill: "t", template: "t", level: 1, prompt: "", answerTex: "", steps: [], answer });
const around = (a: number) => [-0.6, -0.25, 0.15, 0.45, 0.8, 1.3, 1.9].map((d) => ({ t: a + d }));

export const LAPLACE_FOURIER_CASES: [string, Problem, (string | string[])[], (string | string[])[]][] = [
  [
    "unit step spellings, 3(t-2)u(t-2)",
    mk({ kind: "expression", ref: "3*(t-2)*heaviside(t-2)", vars: ["t"], points: around(2) }),
    ["3(t-2)u(t-2)", "3(t-2)H(t-2)", "3(t - 2) u_2(t)", "3(t-2)u_{2}(t)", "3(t-2)heaviside(t-2)", "3(t-2)·u(t-2)", "f(t) = 3tu(t-2) - 6u(t-2)"],
    ["3(t-2)", "3(t-2)u(t-3)", "3t u(t-2)", "3(t-2)u(t-1)", "3(t-2)u(t)"],
  ],
  [
    "shifted exponential e^{t-1}u(t-1)",
    mk({ kind: "expression", ref: "exp(t-1)*heaviside(t-1)", vars: ["t"], points: around(1) }),
    ["e^(t-1)u(t-1)", "e^{t-1} u_1(t)", "exp(t-1)H(t-1)"],
    ["e^t u(t-1)", "e^(t-1)", "e^(t-1)u(t-2)"],
  ],
  [
    "transform in s, any equivalent form",
    mk({ kind: "expression", ref: "1/s + 4/s^2 - 4/(s-1)", vars: ["s"] }),
    ["1/s + 4/s^2 - 4/(s-1)", "(-3s^2+3s-4)/(s^2(s-1))", "F(s) = 1/s+4/s²-4/(s-1)"],
    ["1/s + 4/s^2 - 4/(s+1)", "1/s + 4/s - 4/(s-1)", "1/s + 4/s^2"],
  ],
  [
    "delay factor e^{-2s}",
    mk({ kind: "expression", ref: "exp(-2*s)/s^2", vars: ["s"] }),
    ["e^(-2s)/s^2", "e^{-2s}/s^2", "exp(-2s)/s^2"],
    ["e^(2s)/s^2", "e^(-s)/s^2", "1/s^2"],
  ],
  [
    "Fourier coefficients at integer n (Kreyszig a_0 = mean)",
    mk({ kind: "tuple", fields: [{ label: "a_0", tex: "a_0", ref: "3/2", mode: "expr" }, { label: "a_n", tex: "a_n", ref: "0", mode: "expr" }, { label: "b_n", tex: "b_n", ref: "3*(1-(-1)^n)/(n*pi)", mode: "expr" }], vars: ["n"], points: [1, 2, 3, 4, 5, 6, 7].map((n) => ({ n })) }),
    [["3/2", "0", "3(1-(-1)^n)/(n pi)"], ["1.5", "0", "3(1 - cos(n pi))/(n π)"], ["3/2", "0", "-3((-1)^n - 1)/(nπ)"]],
    [["3/2", "0", "3/(n pi)"], ["3", "0", "3(1-(-1)^n)/(n pi)"], ["3/2", "0", "6/(n pi)"], ["3/2", "0", "3(1+(-1)^n)/(n pi)"]],
  ],
  [
    "heat equation u(x,t)",
    mk({ kind: "expression", ref: "sin(x)*exp(-t) + 2*sin(3*x)*exp(-9*t)", vars: ["x", "t"], points: [0.05, 0.15, 0.3, 0.5, 0.8, 1.1, 1.5].map((tau, i) => ({ x: 0.4 + 0.35 * i, t: tau / 9 })) }),
    ["e^(-t) sin x + 2 e^(-9t) sin 3x", "u = sin(x)e^{-t} + 2sin(3x)e^{-9t}"],
    ["sin(x)e^(-t) + 2 sin(3x) e^(-3t)", "sin(x) + 2 sin(3x)", "sin(x)e^(-t) + 2 sin(3x) e^(-9t) + x/100"],
  ],
];
