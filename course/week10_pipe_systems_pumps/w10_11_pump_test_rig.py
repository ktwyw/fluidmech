"""CHME 202 - Week 10 - Example 11: measuring a pump curve on a test rig.

Pump head from gauge readings: H = (p_d - p_s)/(rho g) + (V_d^2 - V_s^2)/(2 g) + (z_d - z_s).
Efficiency from the measured shaft power: eta = rho g Q H / P_shaft. Readings are ILLUSTRATIVE.
"""

import math

from fluidmech import PumpCurve
from fluidmech.constants import G

rho = 998.0  # water [kg/m3]
d_s, d_d, dz = 0.080, 0.065, 0.30  # suction and discharge pipe diameters, gauge height difference
A_s, A_d = math.pi * d_s**2 / 4, math.pi * d_d**2 / 4
# (Q [L/s], suction gauge [kPa g], discharge gauge [kPa g], shaft power [kW])
readings = [
    (0.0, 12.0, 310.0, 1.6),
    (3.0, 11.5, 305.0, 2.35),
    (6.0, 10.0, 288.0, 3.0),
    (9.0, 7.5, 258.0, 3.6),
    (12.0, 4.0, 214.0, 3.95),
    (15.0, -0.5, 156.0, 4.15),
]
print(f"{'Q [L/s]':>8} {'H [m]':>7} {'P_hyd [kW]':>11} {'P_shaft [kW]':>13} {'eta':>6}")
qs, hs, etas = [], [], []
for q_ls, ps, pd, pw in readings:
    q = q_ls / 1000  # L/s -> m3/s
    vs, vd = q / A_s, q / A_d
    # pump head: pressure (kPa -> Pa), velocity and elevation terms
    H = (pd - ps) * 1e3 / (rho * G) + (vd**2 - vs**2) / (2 * G) + dz
    p_hyd = rho * G * q * H
    eta = p_hyd / (pw * 1000)  # shaft power kW -> W
    qs.append(q)
    hs.append(H)
    etas.append(eta)
    print(f"{q_ls:>8} {H:>7.2f} {p_hyd / 1000:>11.2f} {pw:>13.1f} {eta:>6.1%}")
curve = PumpCurve.from_points(qs, hs, etas)
bep = curve.best_efficiency_point()
print(f"\nFitted curve: H = {curve.h0:.1f} {curve.h1:+.1f} Q {curve.h2:+.0f} Q^2 (Q in m3/s)")
print(
    f"Best efficiency point: Q = {bep * 1000:.1f} L/s, H = {curve.head(bep):.1f} m, eta = {curve.efficiency(bep):.0%}"
)
print("Note the velocity-head correction (smaller discharge pipe) and the gauge height difference:")
print("ignoring them biases the head at high flow.")
