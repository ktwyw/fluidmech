"""CHME 202 - Week 6 - Example 3: capillary viscometry with the Rabinowitsch-Mooney correction.

Hagen-Poiseuille lets us measure viscosity from Q and dp in a thin tube.
For a Newtonian fluid the wall shear rate is 4Q/(pi R^3). For non-Newtonian
fluids the true wall shear rate is (3n' + 1)/(4n') times that, where
n' = d ln(tau_w) / d ln(4Q / pi R^3).
Reading: Wilkes, Fluid Mechanics for Chemical Engineers (capillary viscometry).
"""

import math

from fluidmech.laminar import pipe_flow_rate, power_law_pipe_flow_rate

R, L = 0.5e-3, 0.10  # capillary radius and length [m]

# Part 1: Newtonian calibration oil - viscosity from a single measurement
dp, Q = 50e3, 0.50e-6
mu = math.pi * dp * R**4 / (8 * Q * L)
print(f"Capillary R = {R * 1000} mm, L = {L * 1000:.0f} mm")
print(f"(1) Newtonian oil: dp = {dp / 1e3:.0f} kPa gives Q = {Q * 1e6:.2f} mL/s -> mu = {mu * 1000:.1f} mPa s")
print(f"    check: Hagen-Poiseuille with this mu gives Q = {pipe_flow_rate(dp / L, R, mu) * 1e6:.2f} mL/s")
re = 900 * (Q / (math.pi * R**2)) * 2 * R / mu  # Re with oil density 900 kg/m3
print(f"    Reynolds number {re:.0f} -> laminar, so Hagen-Poiseuille applies\n")

# Part 2: polymer melt data (generated here from a power-law fluid K = 800, n = 0.4 with 2 % scatter)
K_true, n_true = 800.0, 0.4
dps = [2e6, 4e6, 8e6, 16e6]  # applied pressure drops [Pa]
noise = [1.02, 0.99, 1.01, 0.98]  # +/-2 % 'measurement' scatter
Qs = [power_law_pipe_flow_rate(p / L, R, K_true, n_true) * e for p, e in zip(dps, noise)]
tau_w = [p * R / (2 * L) for p in dps]  # wall shear stress from a force balance (any fluid)
gamma_app = [4 * q / (math.pi * R**3) for q in Qs]  # apparent (Newtonian) wall shear rate
x = [math.log(g) for g in gamma_app]
y = [math.log(t) for t in tau_w]
m = len(x)
xm, ym = sum(x) / m, sum(y) / m
n_prime = sum((a - xm) * (b - ym) for a, b in zip(x, y)) / sum((a - xm) ** 2 for a in x)
print(f"(2) Polymer melt, n' = d ln(tau_w)/d ln(4Q/pi R^3) = {n_prime:.3f}")
print(
    f"{'dp [MPa]':>9} {'tau_w [kPa]':>12} {'apparent rate':>14} {'true rate':>10} {'mu_app [Pa s]':>14} {'true mu':>9}"
)
for p, t, g in zip(dps, tau_w, gamma_app):
    g_true = g * (3 * n_prime + 1) / (4 * n_prime)
    print(f"{p / 1e6:>9.0f} {t / 1e3:>12.1f} {g:>12.1f}/s {g_true:>8.1f}/s {t / g:>14.1f} {t / g_true:>9.1f}")
print(f"\nThe correction factor (3n'+1)/(4n') = {(3 * n_prime + 1) / (4 * n_prime):.3f}: ignoring it overestimates the")
print("viscosity of this shear-thinning melt by that same factor. Recovered K and n:")
K_fit = math.exp(ym - n_prime * xm) / ((3 * n_prime + 1) / (4 * n_prime)) ** n_prime
print(f"  n = {n_prime:.3f} (true {n_true}), K = {K_fit:.0f} Pa s^n (true {K_true:.0f})")
