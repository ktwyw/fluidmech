"""CHME 202 - Week 1 - Example 11: properties of process gases at pressure.

Gas density follows the ideal-gas law rho = p / (R T) (below ~20 bar for most gases),
while dynamic viscosity hardly depends on pressure. So kinematic viscosity falls as
pressure rises - but for a fixed MASS flow the pipe Reynolds number 4 m_dot / (pi D mu)
does not change at all.
"""

import math

from fluidmech.constants import KELVIN_OFFSET

gases = {  # specific gas constant [J/(kg K)], viscosity at 20 degC [Pa s]
    "air": (287.05, 1.81e-5),
    "nitrogen": (296.8, 1.76e-5),
    "carbon dioxide": (188.9, 1.47e-5),
    "methane": (518.3, 1.10e-5),
    "hydrogen": (4124.0, 0.88e-5),
}
T = 20.0  # gas temperature [degC]
print(
    f"{'gas':<15} " + "".join(f"{f'rho @ {p} bar':>13}" for p in (1, 10, 50)) + f"{'nu @ 1 bar':>12}{'nu @ 50 bar':>12}"
)
for name, (R, mu) in gases.items():
    rhos = [p * 1e5 / (R * (T + KELVIN_OFFSET)) for p in (1, 10, 50)]  # ideal gas; bar -> Pa
    print(f"{name:<15} " + "".join(f"{r:>13.3f}" for r in rhos) + f"{mu / rhos[0]:>12.2e}{mu / rhos[2]:>12.2e}")

m_dot, D = 0.5, 0.1  # kg/s of nitrogen in a 100 mm line
R, mu = gases["nitrogen"]
print(f"\nNitrogen, {m_dot} kg/s in a {D * 1000:.0f} mm pipe:")
for p in (1.5, 10, 50):
    rho = p * 1e5 / (R * (T + KELVIN_OFFSET))  # ideal gas; bar -> Pa
    V = m_dot / (rho * math.pi * D**2 / 4)
    print(f"  {p:>4} bar: rho = {rho:6.2f} kg/m3, V = {V:6.1f} m/s, Re = {rho * V * D / mu:.3e}")
print("Same Re at every pressure, but the velocity (and friction loss per metre) falls ~1/p:")
print("gas lines are sized for velocity (10-30 m/s), which is why high-pressure lines can be small.")
