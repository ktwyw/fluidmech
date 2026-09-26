"""Example 18 - Choosing the most economical pipe diameter.

A bigger pipe costs more to buy but less to pump through. The best diameter
minimises the annualised capital cost plus the yearly energy cost.
All costs are illustrative.
"""

from fluidmech import Fluid
from fluidmech import pipe_flow as pf

water = Fluid.water(15)
Q, L = 0.060, 2000.0  # m3/s, m
eps = pf.ROUGHNESS["commercial_steel"]
pump_eff = 0.75  # overall pump + motor efficiency
hours_per_year = 6000  # operating hours per year
energy_price = 0.12  # $/kWh
interest, lifetime = 0.06, 30  # capital recovery
# capital recovery factor: capital cost -> equal annual payments
crf = interest * (1 + interest) ** lifetime / ((1 + interest) ** lifetime - 1)


def pipe_cost_per_metre(d: float) -> float:
    """Installed cost [$ / m], a typical power-law fit."""
    return 1800.0 * d**1.3


standard_sizes = [0.100, 0.125, 0.150, 0.200, 0.250, 0.300, 0.350, 0.400]  # nominal inside diameters [m]
print(f"Q = {Q * 1000:.0f} L/s over {L / 1000:.0f} km, capital recovery factor = {crf:.4f}\n")
print(
    f"{'D [mm]':>7} {'V [m/s]':>8} {'hf [m]':>8} {'P [kW]':>8} {'energy $/yr':>12} {'capital $/yr':>13} "
    f"{'total $/yr':>11}"
)
best = None
for d in standard_sizes:
    r = pf.head_loss(Q, d, L, water, eps)
    power_kw = r.pumping_power(pump_eff) / 1e3  # W -> kW
    energy = power_kw * hours_per_year * energy_price
    capital = pipe_cost_per_metre(d) * L * crf
    total = energy + capital
    if best is None or total < best[1]:
        best = (d, total)
    print(
        f"{d * 1000:>7.0f} {r.velocity:>8.2f} {r.major_head_loss:>8.1f} {power_kw:>8.1f} {energy:>12,.0f} "
        f"{capital:>13,.0f} {total:>11,.0f}"
    )

print(f"\nMost economical standard size: {best[0] * 1000:.0f} mm (V = {pf.mean_velocity(Q, best[0]):.2f} m/s)")
print("Typical economic water velocities are 1-2 m/s, consistent with this result.")
