"""Example 35 - Will the pump cavitate? NPSH available vs. NPSH required.

NPSHa = (p_atm - p_vapour)/(rho g) + z_s - h_L,suction must exceed NPSHr
(from the pump data sheet) by a safety margin, typically 0.5-1 m or 10-30 %.
"""

from fluidmech import Fluid, pumps
from fluidmech import pipe_flow as pf
from fluidmech.constants import G
from fluidmech.properties import water_vapor_pressure


def npsh_required(q: float) -> float:
    """Manufacturer's NPSHr curve (rises steeply at high flow)."""
    return 2.0 + 900.0 * q**2  # illustrative NPSHr curve [m], q in m3/s


q = 0.06  # pump flow [m3/s]
d_suction, l_suction, k_suction = 0.20, 8.0, 0.5 + 0.3 + 0.2  # entrance, elbow, strainer
print(f"Pump at Q = {q * 1000:.0f} L/s, NPSHr = {npsh_required(q):.2f} m\n")
print(f"{'water T':>8} {'p_v [kPa]':>10} " + "".join(f"{f'z_s={z:+d} m':>10}" for z in (-6, -4, -2, 0, 2)))
for temp in [10, 30, 50, 70, 90]:
    water = Fluid.water(temp)
    loss = pf.head_loss(q, d_suction, l_suction, water, pf.ROUGHNESS["commercial_steel"], k_suction)
    row = []
    for z in (-6, -4, -2, 0, 2):
        a = pumps.npsh_available(z, loss.total_head_loss, fluid_temperature=temp)
        margin = a - npsh_required(q)
        row.append(f"{a:>6.1f}{'  ' if margin > 1.0 else ' !' if margin > 0 else ' X'}  ")
    print(f"{temp:>6} C {water_vapor_pressure(temp) / 1e3:>10.2f} " + "".join(row))
print("\nTable values are NPSHa [m]. z_s < 0: suction lift (pump above the water); z_s > 0: flooded suction")
print("'!' = margin under 1 m, 'X' = cavitation expected\n")

# Maximum suction lift for cold water at sea level and at altitude
water = Fluid.water(20)
loss = pf.head_loss(q, d_suction, l_suction, water, pf.ROUGHNESS["commercial_steel"], k_suction)
for place, p_atm in [("sea level", 101.3e3), ("1500 m altitude", 84.6e3), ("3000 m altitude", 70.1e3)]:
    z_max = -((p_atm - water_vapor_pressure(20)) / (water.density * G) - loss.total_head_loss - npsh_required(q) - 1.0)
    print(f"Max suction lift at {place:<16}: {-z_max:5.2f} m (with 1 m margin)")
print("Hot water and high altitude both erode NPSH -> put the pump below the tank.")
