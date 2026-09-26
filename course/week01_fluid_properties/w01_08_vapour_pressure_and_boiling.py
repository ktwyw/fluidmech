"""CHME 202 - Week 1 - Example 8: vapour pressure, boiling under vacuum and the cavitation number.

A liquid boils (or cavitates) when its local pressure falls to the vapour pressure.
This matters for vacuum distillation, pump suction lines and control valves.
Reading: White, Section 1.8.
"""

from fluidmech.properties import water_density, water_vapor_pressure
from fluidmech.solvers import bisect

print(f"{'T [degC]':>9} {'p_v [kPa]':>10}")
for t in [0, 20, 40, 60, 80, 100]:
    print(f"{t:>9} {water_vapor_pressure(t) / 1e3:>10.2f}")

print("\nBoiling point of water under vacuum (vacuum evaporators, distillation):")
for p_kpa in [101.3, 50.0, 20.0, 10.0, 5.0]:
    # boiling point: p_v(T) = p (kPa -> Pa)
    t_b = bisect(lambda t, p=p_kpa: water_vapor_pressure(t) - p * 1e3, 1.0, 100.0)
    print(f"  p = {p_kpa:>6.1f} kPa(abs): boils at {t_b:5.1f} degC")
print("Heat-sensitive products (milk, juices, pharmaceuticals) are concentrated this way.\n")

print("Cavitation number sigma = (p - p_v) / (0.5 rho V^2) in a valve throat at 150 kPa(abs):")
for t in [20, 60, 90]:
    rho = water_density(t)
    for v in [5.0, 10.0, 15.0]:
        # cavitation number, throat pressure 150 kPa(abs)
        sigma = (150e3 - water_vapor_pressure(t)) / (0.5 * rho * v**2)
        risk = "cavitation likely" if sigma < 1.0 else ("check" if sigma < 2.0 else "safe")
        print(f"  {t:>2} degC, V = {v:>4} m/s: sigma = {sigma:5.2f} -> {risk}")
print("Hot liquids and high velocities both lower sigma.")
