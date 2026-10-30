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
  // ── switched / impulsive forcing (ode2 + switches), systems with forcing, L{tf} ──
  [
    "y'' + 4y = u(t-π) - u(t-2π), y(0) = y'(0) = 0",
    mk({ kind: "ode2", a: 1, b: 0, c: 4, v: "t", rhs: "heaviside(t-pi) - heaviside(t-2*pi)", ic: [0, 0, 0],
      switches: [{ at: Math.PI, kick: 0 }, { at: 2 * Math.PI, kick: 0 }],
      ref: "(1/4)*(1-cos(2*(t-pi)))*heaviside(t-pi) - (1/4)*(1-cos(2*(t-2*pi)))*heaviside(t-2*pi)" }),
    [
      "y = (1/4)(1-cos(2t))(u(t-pi)-u(t-2pi))",
      "1/4(1 - cos(2(t-π)))u(t-π) - 1/4(1 - cos(2(t-2π)))u(t-2π)",
      "sin(t)^2 (H(t-pi) - H(t-2pi))/2",
      "(1-cos(2t))/4 * (u_pi(t) - u_{2pi}(t))",
      "(1/4)(1-cos(2t))(u_π(t) - u_{2π}(t))",
      "0.25(1-cos(2t))(heaviside(t-pi)-heaviside(t-2pi))",
      "\\frac{1}{4}(1 - \\cos(2t))(u(t - \\pi) - u(t - 2\\pi))",
    ],
    [
      "(1/4)(1-cos(2t))u(t-pi)",
      "(1/4)(1-cos(2t))(u(t-3)-u(t-6))",
      "(1/4)(1-cos(2t))",
      "(1/2)(1-cos(2t))(u(t-pi)-u(t-2pi))",
      "(1/4)(1-cos(t))(u(t-pi)-u(t-2pi))",
      "(1/4)(1-cos(2t))(u(t-pi)-u(t-2pi)) + (t-3.1)^2 u(t-3.1)",
    ],
  ],
  [
    "y'' + 3y' + 2y = 2u(t-1), y(0) = 1, y'(0) = 0",
    mk({ kind: "ode2", a: 1, b: 3, c: 2, v: "t", rhs: "2*heaviside(t-1)", ic: [0, 1, 0], switches: [{ at: 1, kick: 0 }],
      ref: "2*exp(-t) - exp(-2*t) + (1 - 2*exp(-(t-1)) + exp(-2*(t-1)))*heaviside(t-1)" }),
    ["2e^(-t) - e^(-2t) + (1 - 2e^(-(t-1)) + e^(-2(t-1)))u(t-1)", "y = 2e^{-t} - e^{-2t} + H(t-1)(1 - e^{-(t-1)})^2", "2exp(-t)-exp(-2t)+u_1(t)(1-2exp(1-t)+exp(2-2t))"],
    [
      "2e^(-t) - e^(-2t) + (1 - 2e^(-t) + e^(-2t))u(t-1)",
      "2e^(-t) - e^(-2t) + 1 - 2e^(-(t-1)) + e^(-2(t-1))",
      "e^(-t) + (1 - 2e^(-(t-1)) + e^(-2(t-1)))u(t-1)",
      "2e^(-t) - e^(-2t) + (1 - 2e^(-(t-1)) + e^(-2(t-1)))u(t-2)",
    ],
  ],
  [
    "y'' + 3y' + 2y = δ(t-1), y(0) = y'(0) = 0 (Kreyszig §6.4)",
    mk({ kind: "ode2", a: 1, b: 3, c: 2, v: "t", ic: [0, 0, 0], switches: [{ at: 1, kick: 1 }], ref: "(exp(-(t-1)) - exp(-2*(t-1)))*heaviside(t-1)" }),
    ["(e^(-(t-1)) - e^(-2(t-1)))u(t-1)", "H(t-1)(exp(1-t) - exp(2-2t))", "u_1(t)(e^{-(t-1)} - e^{-2(t-1)})", "y = heaviside(t-1)*(e^(1-t) - e^(2-2t))"],
    ["e^(-t) - e^(-2t)", "e^(-(t-1)) - e^(-2(t-1))", "(e^(-(t-1)) - e^(-2(t-1)))u(t-2)", "2(e^(-(t-1)) - e^(-2(t-1)))u(t-1)", "(e^(-(t-1)) - e^(-2(t-1)))u(t-1)/2"],
  ],
  [
    "impulse response of y'' + 4y = δ(t)",
    mk({ kind: "ode2", a: 1, b: 0, c: 4, v: "t", ic: [0, 0, 1], ref: "sin(2*t)/2" }),
    ["sin(2t)/2", "g(t) = (1/2)sin 2t", "1/2 sin(2t) u(t)", "sin(t)cos(t)"],
    ["sin(2t)", "cos(2t)/2", "sin(2t)/2 + 1/4"],
  ],
  [
    "forced system y1' = y2, y2' = y1 - 1, y(0) = (3, 0)",
    mk({ kind: "tuple", fields: [{ label: "y₁", tex: "y_1", ref: "", mode: "expr" }, { label: "y₂", tex: "y_2", ref: "", mode: "expr" }], system: { A: [[0, 1], [1, 0]], v: "t", ic: [0, 3, 0], g: ["0", "-1"] } }),
    [["1 + e^t + e^(-t)", "e^t - e^(-t)"], ["y1 = 1 + 2cosh(t)", "y2 = 2sinh(t)"]],
    [["3cosh(t)", "3sinh(t)"], ["1 + e^t + e^(-t)", "e^t + e^(-t)"], ["1 + C1 e^t + C2 e^(-t)", "C1 e^t - C2 e^(-t)"]],
  ],
  [
    "L^{-1}{ln((s+1)/(s-2))} by -F'(s)",
    mk({ kind: "expression", ref: "(exp(2*t) - exp(-t))/t", vars: ["t"], points: [0.23, 0.61, 0.97, 1.34, 1.71, 2.28].map((t) => ({ t })) }),
    ["(e^(2t) - e^(-t))/t", "f(t) = (e^{2t} - e^{-t})/t", "2e^(t/2)sinh(3t/2)/t"],
    ["e^(2t) - e^(-t)", "(e^(-2t) - e^(t))/t", "(e^(2t) - e^(-t))/t^2"],
  ],
];
