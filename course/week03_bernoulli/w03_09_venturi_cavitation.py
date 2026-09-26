"""CHME 202 - Week 3 - Example 9: throat pressure and cavitation in a Venturi.

Accelerating a liquid through a throat lowers its pressure (Bernoulli). If the
throat pressure reaches the vapour pressure the liquid flashes - the principle of
cavitation reactors, but a fault in flow meters and control valves.
"""

import math

from fluidmech.properties import water_density, water_vapor_pressure

d1, d2 = 0.05, 0.02  # inlet and throat diameters [m]
p1 = 200e3  # upstream absolute pressure [Pa]
beta4 = (d2 / d1) ** 4
for T in (20, 70):
    rho, pv = water_density(T), water_vapor_pressure(T)
    print(f"Water at {T} degC (p_v = {pv / 1e3:.1f} kPa), inlet {p1 / 1e3:.0f} kPa(abs), throat {d2 * 1000:.0f} mm")
    print(f"{'Q [L/s]':>8} {'V throat':>9} {'p throat [kPa]':>15}")
    for q_ls in [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]:
        q = q_ls / 1000  # L/s -> m3/s
        v2 = q / (math.pi * d2**2 / 4)
        p2 = p1 - 0.5 * rho * v2**2 * (1 - beta4)  # Bernoulli + continuity between inlet and throat
        flag = "  <- CAVITATES" if p2 <= pv else ""
        print(f"{q_ls:>8} {v2:>9.2f} {max(p2, pv) / 1e3:>15.1f}{flag}")
    v_crit = math.sqrt(2 * (p1 - pv) / (rho * (1 - beta4)))  # throat velocity at which p2 falls to p_v
    print(f"  cavitation starts at Q = {v_crit * math.pi * d2**2 / 4 * 1000:.2f} L/s\n")
print("Downstream the diffuser recovers most of the pressure, so the line itself may be well above p_v:")
print("cavitation is a LOCAL phenomenon at the point of highest velocity.")
