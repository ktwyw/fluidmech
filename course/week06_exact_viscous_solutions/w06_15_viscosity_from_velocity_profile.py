"""CHME 202 - Week 6 - Example 15: measuring viscosity from a velocity profile (inverse problem).

Velocity measurements across a pipe (e.g. from PIV or an ultrasonic profiler) are fitted with
the Hagen-Poiseuille parabola u = u0 (1 - r^2/R^2); with the measured pressure gradient G,
mu = G R^2 / (4 u0). The 'measurements' here carry 3 % random error.
"""

import random

random.seed(4)
R, G, mu_true = 0.01, 800.0, 0.25  # tube radius [m], -dp/dx [Pa/m], viscosity used to make the data
u0_true = G * R**2 / (4 * mu_true)
rs = [R * i / 10 for i in range(-9, 10)]
data = [(r, u0_true * (1 - (r / R) ** 2) * (1 + random.gauss(0, 0.03))) for r in rs]
# least squares for u = u0 * s with s = 1 - (r/R)^2 (line through the origin)
s = [1 - (r / R) ** 2 for r, _ in data]
u0_fit = sum(si * ui for si, (_, ui) in zip(s, data)) / sum(si * si for si in s)  # least-squares slope of u against s
mu_fit = G * R**2 / (4 * u0_fit)
resid = [ui - u0_fit * si for si, (_, ui) in zip(s, data)]
print(f"{len(data)} velocity measurements across a {2 * R * 1000:.0f} mm tube, G = {G} Pa/m")
print(f"Fitted centreline velocity u0 = {u0_fit * 1000:.2f} mm/s")
print(f"Viscosity mu = G R^2 / (4 u0) = {mu_fit:.4f} Pa s (true {mu_true}, error {mu_fit / mu_true - 1:+.1%})")
print(f"RMS residual {(sum(e * e for e in resid) / len(resid)) ** 0.5 * 1000:.3f} mm/s")
print("\nA parabolic fit with small, random residuals confirms laminar Newtonian flow; a blunt profile")
print("would reveal shear-thinning (Week 6, Example 6) or turbulence. Check Re before trusting the fit:")
print(f"Re = {1000 * u0_fit / 2 * 2 * R / mu_fit:.2f}")
