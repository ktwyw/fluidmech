"""CHME 202 - Week 3 - Example 6: transferring liquid by pressurising a vessel.

In chemical plants, liquids are often moved without a pump by pressurising the
headspace of a vessel with nitrogen ("blowing over"). Bernoulli (with a
discharge coefficient for losses) gives the transfer rate.
"""

import math

from fluidmech.constants import G

rho = 870.0  # toluene-like solvent [kg/m3]
d_out, cd = 0.025, 0.70  # outlet diameter, overall discharge coefficient (pipe + valve losses)
a_out = math.pi * d_out**2 / 4
z_rise = 6.0  # the receiving vessel inlet is 6 m ABOVE the liquid surface in the source vessel
volume = 2.0  # m3 to transfer
print(f"Solvent (rho = {rho} kg/m3) lifted {z_rise} m through a {d_out * 1000:.0f} mm line, Cd = {cd}\n")
print(f"{'N2 overpressure [bar]':>22} {'net head [m]':>13} {'Q [L/s]':>8} {'time for 2 m3':>14}")
for bar in [0.3, 0.5, 1.0, 2.0, 3.0]:
    head = bar * 1e5 / (rho * G) - z_rise  # bar -> Pa -> m of liquid, minus the lift
    if head <= 0:
        print(f"{bar:>22.1f} {head:>13.2f}    no flow: pressure cannot lift the liquid {z_rise} m")
        continue
    q = cd * a_out * math.sqrt(2 * G * head)
    print(f"{bar:>22.1f} {head:>13.2f} {q * 1000:>8.2f} {volume / q / 60:>11.1f} min")
p_min = rho * G * z_rise / 1e5  # Pa -> bar
print(f"\nMinimum overpressure just to lift the liquid: {p_min:.2f} bar(g)")
print("Safety: the source vessel must be rated for the blanketing pressure, with a relief valve.")
