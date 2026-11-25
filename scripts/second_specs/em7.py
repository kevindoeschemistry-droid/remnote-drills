"""Engineering Math: Green's functions, the 1-D random walk and Fourier convolution (Nov 2026, Kevin asked). A house
list on the CBE 200/605 topic lists (Green's functions and transforms for PDEs). Each key is checked along another
route: a Green's function against the jump conditions or a direct solve, an impulse response against the convolution
integral, image solutions against sine and cosine transforms, walk statistics against exact binomial sums or a
generating function, and convolutions against the defining integral."""
from opl_dsl import Q

FILE, FRAMEWORK = "em-green", "engineering-math"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
S, T, K, Z = "Symbol('s')", "Symbol('t')", "Symbol('k')", "Symbol('z')"
GR, RW, FT = "bvp.green", "pde.random-walk", "bvp.fourier-series"

TOPICS = {"9.4": "Green's functions", "11.2": "Random walks and the diffusion limit"}

OBJS = [
    ("EM-9.4.A", [], "Build the Green's function of y″ = f with y(0) = y(L) = 0 and use it to solve for a given f.",
     "G(x, s) = x(s − L)/L for x < s and s(x − L)/L for x > s: continuous at x = s, slope jumps by 1, zero at both ends; y = ∫G f ds."),
    ("EM-9.4.B", [], "Build the Green's function of y″ + k²y = f with fixed ends from the homogeneous solutions and the jump condition.",
     "G = −sin(kx_<) sin(k(L − x_>))/(k sin kL); it fails to exist exactly when kL = nπ, an eigenvalue of the homogeneous problem."),
    ("EM-9.4.C", [], "Solve a forced initial-value problem by convolving the forcing with the impulse response.",
     "For y″ + ω²y = f, g(t) = sin(ωt)/ω; for τy′ + y = f, g(t) = e^(−t/τ)/τ; y = ∫₀ᵗ g(t − u) f(u) du from rest."),
    ("EM-10.5.D", [], "Write the heat kernel as the Green's function of the diffusion equation and use images for a fixed or insulated end.",
     "G = e^(−(x−x₀)²/4κt)/√(4πκt) on the line; on x > 0 subtract the mirror image for u(0) = 0, add it for an insulated end."),
    ("EM-11.1.F", [], "Convolve functions directly and through the Fourier transform: Gaussians, pulses, and an initial profile spreading by diffusion.",
     "Gaussian widths add in quadrature (σ² = σ₁² + σ₂²); two pulses give a triangle; u(x, t) = u₀ ∗ heat kernel, so σ² grows by 2κt."),
    ("EM-11.2.A", [], "Compute end-point probabilities and moments of a 1-D random walk, with or without bias.",
     "N steps of ±a: P(m) = C(N, (N + m)/2)/2^N; ⟨x⟩ = Na(2p − 1), Var x = 4Np(1 − p)a², so ⟨x²⟩ = Na² when unbiased."),
    ("EM-11.2.B", [], "Take the diffusion limit of a random walk: D from step length and time, and the time to diffuse a distance.",
     "D = a²/(2Δt) in 1-D; ⟨x²⟩ = 2Dt, and ⟨r²⟩ = 2dDt in d dimensions; t ~ L²/(2D)."),
    ("EM-11.2.C", [], "Use the Gaussian limit of the walk to find the fraction of walkers past a distance, and add the variances of successive stages.",
     "P(x, t) = e^(−x²/4Dt)/√(4πDt); fraction beyond |x| > ℓ is erfc(ℓ/√(4Dt)); independent stages convolve, so variances add."),
]

ADD = [
    # 9.4.A
    ("EM-9.4.A", Q("gf-string-value", GR, "For y″ = f on 0 < x < {{L}} with y(0) = y({{L}}) = 0, evaluate the Green's function G(x, s) at x = {{x0}}, s = {{s0}}.",
        cases=[{"L": 1, "x0": 0.25, "s0": 0.5}, {"L": 2, "x0": 1.5, "s0": 0.5}, {"L": 4, "x0": 1, "s0": 3}, {"L": 3, "x0": 2, "s0": 2.5}],
        value="x0 < s0 ? x0*(s0 - L)/L : s0*(x0 - L)/L", tex="G",
        verify="(Symbol('A')*nsimplify(x0) if x0 < s0 else Symbol('B')*(nsimplify(x0) - L)).subs(solve([Symbol('A')*nsimplify(s0) - Symbol('B')*(nsimplify(s0) - L), Symbol('B') - Symbol('A') - 1], [Symbol('A'), Symbol('B')]))",
        explain="G = A x left of s, B(x − L) right of s; continuity A s = B(s − L) and the unit slope jump B − A = 1 fix A and B")),
    ("EM-9.4.A", Q("gf-string-solve", GR, "Use the Green's function of y″ = f, y(0) = y({{L}}) = 0, to find y({{x0}}) when f(x) = {{c}}x.",
        cases=[{"L": 1, "x0": 0.5, "c": 6}, {"L": 2, "x0": 1, "c": 3}, {"L": 3, "x0": 1, "c": 2}, {"L": 2, "x0": 0.5, "c": -6}],
        value="c*(x0^3 - L^2*x0)/6", tex="y",
        verify=f"integrate({S}*(nsimplify(x0) - L)/L*c*{S}, ({S}, 0, nsimplify(x0))) + integrate(nsimplify(x0)*({S} - L)/L*c*{S}, ({S}, nsimplify(x0), L))",
        explain="Integrating twice directly gives y = c(x³ − L²x)/6, the same as ∫G(x, s) c s ds")),
    # 9.4.B
    ("EM-9.4.B", Q("gf-helmholtz-value", GR, "For y″ + {{k2}}y = f on 0 < x < π/2 with y(0) = y(π/2) = 0 (k = {{kk}}), evaluate G(x, s) at x = {{x0}}, s = {{s0}}.",
        cases=[{"k2": 1, "kk": 1, "x0": 0.3, "s0": 0.9}, {"k2": 9, "kk": 3, "x0": 1.2, "s0": 0.4}, {"k2": 1, "kk": 1, "x0": 1.0, "s0": 0.5}, {"k2": 9, "kk": 3, "x0": 0.2, "s0": 0.7}],
        value="-sin(kk*min(x0, s0))*sin(kk*(pi/2 - max(x0, s0)))/(kk*sin(kk*pi/2))", tex="G",
        verify="(Symbol('A')*sin(kk*nsimplify(x0)) if x0 < s0 else Symbol('B')*sin(kk*(pi/2 - nsimplify(x0)))).subs(solve([Symbol('A')*sin(kk*nsimplify(s0)) - Symbol('B')*sin(kk*(pi/2 - nsimplify(s0))), -Symbol('B')*kk*cos(kk*(pi/2 - nsimplify(s0))) - Symbol('A')*kk*cos(kk*nsimplify(s0)) - 1], [Symbol('A'), Symbol('B')]))",
        explain="Left piece A sin kx, right piece B sin k(L − x); continuity and a unit jump in G′ at x = s fix A and B")),
    ("EM-9.4.B", Q("gf-existence", GR, "{{q}}", pace="quick",
        cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in [
            ("For y″ + k²y = f, y(0) = y(L) = 0, when does the Green's function fail to exist?", "When kL is a multiple of π", "When k is negative", "When f is discontinuous", "Never"),
            ("What jump does dG/dx have at x = s for (p y′)′ + q y = f?", "1/p(s)", "1", "p(s)", "0: it is continuous"),
            ("For a self-adjoint problem, how are G(x, s) and G(s, x) related?", "They are equal (symmetry)", "G(s, x) = −G(x, s)", "G(s, x) = 1/G(x, s)", "No general relation"),
            ("What does G(x, s) represent physically for a loaded string?", "The deflection at x from a unit point load at s", "The tension at s", "The slope at x from a unit load at x", "The energy stored by the load"),
        ]], choice=MC, correct="0", verify="authored",
        explain="G solves the problem with a delta source; it exists exactly when the homogeneous problem has only the zero solution")),
    # 9.4.C
    ("EM-9.4.C", Q("gf-oscillator-step", GR, "y″ + {{w2}}y = {{F0}} for t > 0, from rest. Using y = ∫₀ᵗ g(t − u) f(u) du with g = sin(ωt)/ω, find y({{T}}).",
        cases=[{"w2": 4, "F0": 8, "T": 1}, {"w2": 1, "F0": 2, "T": 2}, {"w2": 9, "F0": 3, "T": 0.5}],
        value="F0*(1 - cos(sqrt(w2)*T))/w2", tex="y",
        verify=f"integrate(sin(sqrt(w2)*(nsimplify(T) - {S}))/sqrt(w2)*F0, ({S}, 0, nsimplify(T)))",
        explain="A step force shifts the equilibrium to F₀/ω² and the mass oscillates about it: F₀(1 − cos ωt)/ω²")),
    ("EM-9.4.C", Q("gf-lag-ramp", GR, "A first-order system τy′ + y = f has τ = {{tau}} and starts at rest. Find y({{T}}) for the ramp f(t) = t.",
        given={"tau": {"pick": [0.5, 1, 2]}, "T": {"pick": [1, 3, 5]}},
        value="T - tau*(1 - exp(-T/tau))", tex="y",
        verify=f"integrate(exp(-(T - {S})/nsimplify(tau))/nsimplify(tau)*{S}, ({S}, 0, T))",
        explain="Convolve with g = e^(−t/τ)/τ: the output lags the ramp by τ once the transient e^(−t/τ) dies")),
    # 10.5.D
    ("EM-10.5.D", Q("gf-image-fixed", GR, "Heat Q = {{Qh}} is released at x₀ = {{x0}} on a half-line x > 0 with κ = {{kap}} and u(0, t) = 0. Find u({{xx}}, {{T}}) by the method of images.",
        given={"Qh": {"pick": [1, 2]}, "x0": {"pick": [1, 2]}, "kap": {"pick": [0.5, 1]}, "xx": {"pick": [0.5, 1.5]}, "T": {"pick": [0.5, 1]}},
        value="Qh/sqrt(4*pi*kap*T)*(exp(-(xx - x0)^2/(4*kap*T)) - exp(-(xx + x0)^2/(4*kap*T)))", tex="u",
        verify=f"2/pi*Qh*integrate(sin({K}*nsimplify(xx))*sin({K}*x0)*exp(-nsimplify(kap)*{K}**2*nsimplify(T)), ({K}, 0, oo))",
        explain="A negative image at −x₀ holds u(0) = 0; checked against the Fourier sine-transform solution")),
    ("EM-10.5.D", Q("gf-image-insulated", GR, "Same release (Q = {{Qh}} at x₀ = {{x0}}, κ = {{kap}}), but the end x = 0 is insulated. Find u({{xx}}, {{T}}).",
        given={"Qh": {"pick": [1, 2]}, "x0": {"pick": [1, 2]}, "kap": {"pick": [0.5, 1]}, "xx": {"pick": [0.5, 1.5]}, "T": {"pick": [0.5, 1]}},
        value="Qh/sqrt(4*pi*kap*T)*(exp(-(xx - x0)^2/(4*kap*T)) + exp(-(xx + x0)^2/(4*kap*T)))", tex="u",
        verify=f"2/pi*Qh*integrate(cos({K}*nsimplify(xx))*cos({K}*x0)*exp(-nsimplify(kap)*{K}**2*nsimplify(T)), ({K}, 0, oo))",
        explain="A positive image makes ∂u/∂x = 0 at the wall; checked against the cosine-transform solution")),
    # 11.1.F
    ("EM-11.1.F", Q("fc-gaussians", FT, "f and g are normalised Gaussians centred at 0 with standard deviations {{s1}} and {{s2}}. Find (f ∗ g)(0).",
        given={"s1": {"pick": [1, 2]}, "s2": {"pick": [1, 3]}},
        value="1/sqrt(2*pi*(s1^2 + s2^2))", tex="(f*g)(0)",
        verify=f"integrate(exp(-{S}**2/(2*s1**2))/sqrt(2*pi*s1**2)*exp(-{S}**2/(2*s2**2))/sqrt(2*pi*s2**2), ({S}, -oo, oo))",
        explain="The transforms multiply, so the exponents add: a Gaussian with σ² = σ₁² + σ₂²")),
    ("EM-11.1.F", Q("fc-pulses", FT, "f = g = 1 on |x| < {{b}} and 0 elsewhere. Find (f ∗ g)({{x0}}).",
        cases=[{"b": 1, "x0": 0.5}, {"b": 2, "x0": 1}, {"b": 1, "x0": 1.5}, {"b": 2, "x0": 3}],
        value="max(0, 2*b - abs(x0))", tex="(f*g)",
        verify=f"integrate(1, ({S}, Max(-b, nsimplify(x0) - b), Min(b, nsimplify(x0) + b)))",
        explain="The overlap of two shifted pulses: a triangle of height 2b; its transform is the square of the sinc")),
    ("EM-11.1.F", Q("fc-heat-spread", FT, "u(x, 0) is a Gaussian of standard deviation {{s0}} holding total heat {{Qh}}. With κ = {{kap}}, find u(0, {{T}}).",
        given={"s0": {"pick": [0.5, 1]}, "Qh": {"pick": [1, 3]}, "kap": {"pick": [0.25, 0.5]}, "T": {"pick": [1, 2]}},
        value="Qh/sqrt(2*pi*(s0^2 + 2*kap*T))", tex="u",
        verify=f"integrate(Qh*exp(-{S}**2/(2*nsimplify(s0)**2))/sqrt(2*pi*nsimplify(s0)**2)*exp(-{S}**2/(4*nsimplify(kap)*T))/sqrt(4*pi*nsimplify(kap)*T), ({S}, -oo, oo))",
        explain="u = u₀ ∗ heat kernel; the kernel has variance 2κt, so σ² = σ₀² + 2κt")),
    # 11.2.A
    ("EM-11.2.A", Q("rw-endpoint", RW, "An unbiased walker takes {{N}} steps of ±1. What is the probability it ends at x = {{m}}?",
        cases=[{"N": 4, "m": 2}, {"N": 6, "m": 0}, {"N": 10, "m": 4}, {"N": 8, "m": -2}, {"N": 12, "m": 6}],
        value="combinations(N, (N + m)/2)/2^N", tex="P", final=True,
        verify=f"expand((({Z} + 1/{Z})/2)**N).coeff({Z}, m)",
        explain="(N + m)/2 steps right and the rest left: C(N, (N + m)/2) paths out of 2^N; the generating function ((z + 1/z)/2)^N agrees")),
    ("EM-11.2.A", Q("rw-biased-msd", RW, "A walker steps +{{a}} with probability {{p}} and −{{a}} otherwise, {{N}} times. Find ⟨x²⟩.",
        given={"a": {"pick": [1, 2]}, "p": {"pick": [0.5, 0.6, 0.75]}, "N": {"pick": [10, 20]}},
        value="4*N*p*(1 - p)*a^2 + (N*a*(2*p - 1))^2", tex="\\langle x^2\\rangle",
        verify=f"summation(binomial(N, {S})*nsimplify(p)**{S}*(1 - nsimplify(p))**(N - {S})*(a*(2*{S} - N))**2, ({S}, 0, N))",
        explain="⟨x²⟩ = Var x + ⟨x⟩² = 4Np(1 − p)a² + (Na(2p − 1))²; the drift grows as N², the spread as N")),
    # 11.2.B
    ("EM-11.2.B", Q("rw-diffusivity", RW, "A molecule makes a {{a}} nm jump every {{dt}} ps in a random direction along a line. What is D in cm²/s?",
        given={"a": {"pick": [0.2, 0.3, 0.5]}, "dt": {"pick": [1, 2, 5]}},
        value="(a*1e-7)^2/(2*dt*1e-12)", tex="D",
        verify="(nsimplify(a)*Rational(1, 10**7))**2/(2*nsimplify(dt)*Rational(1, 10**12))",
        explain="⟨x²⟩ = Na² = (t/Δt)a² = 2Dt, so D = a²/(2Δt); 1 nm = 10⁻⁷ cm")),
    ("EM-11.2.B", Q("rw-diffuse-time", RW, "How long does a molecule with D = {{Dv}} cm²/s take to reach an rms displacement of {{L}} µm in {{dim}} dimension(s)?",
        given={"Dv": {"pick": [1e-5, 1e-6]}, "L": {"pick": [1, 10, 100]}, "dim": {"pick": [1, 3]}},
        value="(L*1e-4)^2/(2*dim*Dv)", tex="t",
        verify="solve(Eq(2*dim*nsimplify(Dv)*Symbol('tt'), (L*Rational(1, 10**4))**2), Symbol('tt'))[0]",
        explain="⟨r²⟩ = 2dDt: ten times the distance takes a hundred times as long")),
    # 11.2.C
    ("EM-11.2.C", Q("rw-tail", RW, "Walkers start at x = 0 and diffuse with D = {{Dv}} for time {{T}}. What fraction are farther than {{ell}} from the start (either side)?",
        given={"Dv": {"pick": [0.5, 1]}, "T": {"pick": [1, 2]}, "ell": {"pick": [1, 2, 3]}},
        value="1 - erf(ell/sqrt(4*Dv*T))", tex="f",
        verify=f"2*integrate(exp(-{S}**2/(4*nsimplify(Dv)*T))/sqrt(4*pi*nsimplify(Dv)*T), ({S}, ell, oo))",
        explain="Twice the Gaussian tail: erfc(ℓ/√(4Dt))")),
    ("EM-11.2.C", Q("rw-stages", RW, "A walker takes {{N1}} steps of length {{a1}}, then {{N2}} steps of length {{a2}}, all unbiased and independent. What is its rms displacement?",
        given={"N1": {"pick": [100, 400]}, "a1": {"pick": [1, 2]}, "N2": {"pick": [100, 900]}, "a2": {"pick": [0.5, 3]}},
        value="sqrt(N1*a1^2 + N2*a2^2)", tex="x_{rms}",
        verify=f"sqrt(integrate({S}**2*exp(-{S}**2/(2*(N1*a1**2 + N2*nsimplify(a2)**2)))/sqrt(2*pi*(N1*a1**2 + N2*nsimplify(a2)**2)), ({S}, -oo, oo)))",
        explain="The distribution after both stages is the convolution of the two; convolution adds variances, not rms values")),
]
