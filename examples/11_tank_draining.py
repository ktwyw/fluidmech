"""Example 11 - Draining a tank through a bottom orifice.

Compares the closed-form draining time with a step-by-step numerical
integration of the quasi-steady Bernoulli equation dh/dt = -Cd a sqrt(2 g h) / A.
"""

import math

from fluidmech.bernoulli import orifice_flow_rate, tank_drain_time

D_tank, d_orifice = 2.0, 0.05  # m
A_tank = math.pi * D_tank**2 / 4
a_orifice = math.pi * d_orifice**2 / 4
h0 = 3.0  # initial liquid depth [m]
cd = 0.61  # discharge coefficient of a sharp-edged orifice

t_exact = tank_drain_time(A_tank, a_orifice, h0, 0.0, cd)
print(f"Cylindrical tank D = {D_tank} m, orifice d = {d_orifice * 1000:.0f} mm, Cd = {cd}")
print(f"Analytical time to empty from h = {h0} m: {t_exact:.0f} s ({t_exact / 60:.1f} min)\n")

# Explicit (forward Euler) integration
dt, t, h = 1.0, 0.0, h0
table_times = {int(t_exact * f) for f in (0.0, 0.1, 0.25, 0.5, 0.75, 0.9)}
print(f"{'t [s]':>7} {'h numeric [m]':>14} {'h exact [m]':>12} {'Q [L/s]':>9}")
while h > 0.0:  # explicit (forward Euler) time stepping of dh/dt = -Cd a sqrt(2 g h) / A
    if int(t) in table_times:
        # exact solution: sqrt(h) = sqrt(h0) - (Cd a sqrt(2g) / (2A)) t
        h_exact = (math.sqrt(h0) - cd * a_orifice * math.sqrt(2 * 9.80665) / (2 * A_tank) * t) ** 2
        q = orifice_flow_rate(a_orifice, h, cd) * 1000  # m3/s -> L/s for printing
        print(f"{t:>7.0f} {h:>14.4f} {h_exact:>12.4f} {q:>9.2f}")
    h -= orifice_flow_rate(a_orifice, h, cd) / A_tank * dt
    t += dt
print(f"\nNumerical time to empty: {t:.0f} s (error {abs(t - t_exact) / t_exact:.2%})")

print("\nHalf the head does NOT mean half the time:")
t_half = tank_drain_time(A_tank, a_orifice, h0, h0 / 2, cd)
print(f"  top half drains in {t_half:.0f} s, bottom half in {t_exact - t_half:.0f} s")

print("\nEffect of the orifice discharge coefficient:")
for name, c in [("sharp-edged", 0.61), ("short tube", 0.82), ("rounded nozzle", 0.97)]:
    print(f"  {name:<15} Cd = {c:.2f} -> {tank_drain_time(A_tank, a_orifice, h0, 0, c) / 60:5.1f} min")
