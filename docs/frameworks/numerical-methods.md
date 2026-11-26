# Numerical Methods — curriculum framework (draft 1)

Generated from `drills/frameworks/numerical-methods.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**17 learning objectives** in 5 units (17 core): 17 drilled, 0 partly, 0 with no drills. Core: 17 / 17 drilled.

## Big ideas

- **ERR · Every method has an error that scales.** A step size h, a number of panels or an iteration count sets the error as a power of h or a factor per step. Knowing the power is knowing how much refinement buys.
- **STAB · Stable before accurate.** An iteration or a time step that amplifies errors is useless however accurate each step is. Check the contraction factor or the stability limit first.

## Practices

- **P1 · Step by hand.** Carry one step or one iteration of a method to a number, the way you check code.
- **P2 · Judge convergence.** Decide whether and how fast a method converges from the problem's structure.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Roots of equations | core | — | 4 | 4 | 0 | 0 |
| 2 · Iterative linear solvers | core | — | 3 | 3 | 0 | 0 |
| 3 · Interpolation and numerical integration | core | — | 5 | 5 | 0 | 0 |
| 4 · Ordinary differential equations | core | — | 4 | 4 | 0 | 0 |
| 5 · Numerical differentiation | core | — | 1 | 1 | 0 | 0 |

## Unit 1 · Roots of equations

Big ideas: ERR, STAB

### 1.1 Bracketing and open methods



- ● **NM-1.1.A** (fe-chemical:1.D) Count the bisection steps needed for a tolerance.
  - EK: n ≥ log₂(L/ε): about 3.3 steps per digit.
  - P1 · drills: nm-bisection-steps, nm-bisection-error-bound
- ● **NM-1.1.B** (webwork-opl:CA3.17) Take a Newton step.
  - EK: x₁ = x₀ − f(x₀)/f′(x₀); quadratic convergence near a simple root.
  - P1 · drills: nm-newton-step, nm-newton-reciprocal
- ● **NM-1.1.C** (fe-chemical:1.D) Take a secant step.
  - EK: The derivative is replaced by the slope through the last two points.
  - P1 · drills: nm-secant-step, nm-false-position
- ● **NM-1.1.D** (fe-chemical:1.D) Decide whether fixed-point iteration converges.
  - EK: Converges when |g′(r)| < 1.
  - P2 · drills: nm-fixed-point, nm-fixed-point-iterations

## Unit 2 · Iterative linear solvers

Big ideas: ERR, STAB

### 2.1 Jacobi and Gauss–Seidel



- ● **NM-2.1.A** (fe-chemical:1.E) Take a Jacobi step.
  - EK: Each unknown from its own equation, old values only.
  - P1 · drills: nm-jacobi-step, nm-jacobi-spectral
- ● **NM-2.1.B** (fe-chemical:1.E) Take a Gauss–Seidel sweep.
  - EK: Use each new value as soon as it is computed.
  - P1 · drills: nm-gauss-seidel-step, nm-gauss-seidel-spectral
- ● **NM-2.1.C** (fe-chemical:1.E) Test for strict diagonal dominance.
  - EK: |a_ii| > Σ|a_ij| on every row guarantees convergence.
  - P2 · drills: nm-diagonal-dominance, nm-dominance-threshold

## Unit 3 · Interpolation and numerical integration

Big ideas: ERR, STAB

### 3.1 Interpolation



- ● **NM-3.1.A** (fe-chemical:1.D) Evaluate the interpolating quadratic through three points.
  - EK: Lagrange form: Σ yᵢLᵢ(x).
  - P1 · drills: nm-lagrange-quadratic, nm-divided-difference

### 3.2 Quadrature



- ● **NM-3.2.A** (webwork-opl:CA5.13) Apply Simpson's rule.
  - EK: (h/3)(f₀ + 4f₁ + f₂); exact for cubics.
  - P1 · drills: nm-simpson, nm-simpson-error
- ● **NM-3.2.B** (webwork-opl:CA5.13) Predict how the trapezoid error falls with refinement.
  - EK: Error ∝ h²; Simpson ∝ h⁴.
  - P2 · drills: nm-trapezoid-scaling, nm-trapezoid-panels
- ● **NM-3.2.C** (fe-chemical:1.D, webwork-opl:CA5.13) Improve two trapezoid estimates by Richardson extrapolation.
  - EK: (4T(h/2) − T(h))/3.
  - P1 · drills: nm-richardson, nm-richardson-cubic
- ● **NM-3.2.D** (fe-chemical:1.D, webwork-opl:CA5.13) Apply two-point Gauss–Legendre quadrature.
  - EK: Nodes ±1/√3, weights 1; exact for cubics.
  - P1 · drills: nm-gauss-two-point, nm-gauss-three-point

## Unit 4 · Ordinary differential equations

Big ideas: ERR, STAB

### 4.1 One-step methods



- ● **NM-4.1.A** (webwork-opl:DE6.2) Take a Heun (improved Euler) step.
  - EK: Predict with Euler, correct with the average slope.
  - P1 · drills: nm-heun-step, nm-midpoint-step
- ● **NM-4.1.B** (webwork-opl:DE6.2) Take a classical RK4 step.
  - EK: For y′ = λy the step multiplies by the Taylor series of e^(λh) through order 4.
  - P1 · drills: nm-rk4-step, nm-rk4-stability
- ● **NM-4.1.C** (webwork-opl:DE6.1) Find the explicit Euler stability limit.
  - EK: h ≤ 2/λ for y′ = −λy.
  - P2 · drills: nm-euler-stability, nm-backward-euler
- ● **NM-4.1.D** (webwork-opl:DE6.3) Take an Euler step for a system.
  - EK: y₁ = (I + hA)y₀.
  - P1 · drills: nm-euler-system, nm-stiffness-ratio

## Unit 5 · Numerical differentiation

Big ideas: ERR, STAB

### 5.1 Finite differences



- ● **NM-5.1.A** (fe-chemical:1.D) Find the error of a central-difference derivative.
  - EK: Error = (h²/6) f‴: second order.
  - P1 · drills: nm-central-difference-error, nm-forward-difference-error

## Drills not yet placed on the map

- gc-condition-digits (nm.linear-iter)
- gc-residual-vs-error (nm.linear-iter)
- gc-stiff-step (nm.ode)
- gc-stiffness-ratio (nm.ode)
- gc-optimal-step (nm.diff)
- gc-observed-order (nm.diff)
