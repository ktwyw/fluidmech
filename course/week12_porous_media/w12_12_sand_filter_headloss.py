"""CHME 202 - Week 12 - Example 12: clean-bed head loss of a rapid sand filter (water treatment).

Filtration rates of 5-15 m/h through ~0.5 mm sand are in the laminar (Kozeny-Carman) regime.
Head loss is proportional to velocity and to viscosity - so the same filter loses more head
in winter when the water is cold.
"""

from fluidmech import Fluid
from fluidmech import porous as por
from fluidmech.constants import G

d, eps, phi, L = 0.5e-3, 0.42, 0.85, 0.8  # sand size, voidage, sphericity, bed depth
print(f"Sand d = {d * 1000} mm, voidage {eps}, sphericity {phi}, depth {L} m\n")
print(f"{'rate [m/h]':>11} {'Re_p':>6} " + "".join(f"{f'h_L at {t} degC':>16}" for t in (4, 15, 25)))
for rate in [5, 8, 10, 12, 15]:
    u = rate / 3600  # filtration rate m/h -> m/s
    cells = []
    for T in (4, 15, 25):
        w = Fluid.water(T)
        dp = por.ergun_pressure_gradient(u, d, eps, w.dynamic_viscosity, w.density, phi) * L
        cells.append(f"{dp / (w.density * G) * 100:13.1f} cm")
    re = por.bed_reynolds(u, d, eps, Fluid.water(15).dynamic_viscosity, 1000.0, phi)
    print(f"{rate:>11} {re:>6.2f} " + "".join(f"{c:>16}" for c in cells))
print("\nRe_p << 10: the viscous term dominates, h_L ~ mu u. Water at 4 degC is ~1.7x as viscous as at")
print("25 degC, so a filter that is fine in summer may need backwashing sooner in winter. As the bed")
print("clogs with dirt, the head loss grows until it reaches ~2-3 m, which triggers a backwash (Example 10).")
