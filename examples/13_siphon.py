"""Example 13 - Siphon design and the cavitation limit at the crest.

A 50 mm PVC siphon draws water over a wall from a reservoir to a lower outlet.
The pressure at the crest must stay above the vapour pressure of water.
"""

from fluidmech import Fluid
from fluidmech import pipe_flow as pf
from fluidmech.constants import P_ATM, G

water = Fluid.water(20)
p_vapour = 2.34e3  # Pa, water at 20 degC
D = 0.05
eps = pf.ROUGHNESS["pvc"]
L_up, L_down = 6.0, 12.0  # pipe length before and after the crest [m]
drop = 5.0  # outlet below reservoir surface [m]
k_in, k_bends, k_exit = 0.5, 2 * 0.3, 1.0

# Energy from reservoir surface to outlet: drop = all losses (exit K=1 = outlet velocity head)
k_total = k_in + k_bends + k_exit
q = pf.flow_rate_for_head_loss(drop, D, L_up + L_down, water, eps, k_total)
v = pf.mean_velocity(q, D)
print(f"Siphon flow: Q = {q * 1000:.2f} L/s, V = {v:.2f} m/s")


def crest_pressure_abs(crest_height: float) -> float:
    """Absolute pressure at the crest [Pa] for a crest this far above the reservoir."""
    upstream = pf.head_loss(q, D, L_up, water, eps, k_total=k_in + 0.3)
    head = -crest_height - v**2 / (2 * G) - upstream.total_head_loss
    return P_ATM + water.density * G * head


print(f"\n{'crest height [m]':>17} {'p_abs [kPa]':>12}  status")
for zc in [1, 2, 4, 6, 7, 8, 9]:
    p = crest_pressure_abs(zc)
    status = "OK" if p > p_vapour + 20e3 else ("near cavitation" if p > p_vapour else "CAVITATES / breaks")
    print(f"{zc:>17} {p / 1e3:>12.1f}  {status}")

# Maximum crest height where p = p_vapour
upstream = pf.head_loss(q, D, L_up, water, eps, k_total=k_in + 0.3).total_head_loss
z_max = (P_ATM - p_vapour) / (water.density * G) - v**2 / (2 * G) - upstream
print(f"\nTheoretical maximum crest height: {z_max:.2f} m above the reservoir")
print("Dissolved air comes out of solution well before this, so design with a margin:")
print(f"a crest no higher than about {z_max - 2.5:.1f} m keeps p_abs above ~25 kPa.")
