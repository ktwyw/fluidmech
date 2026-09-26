"""CHME 202 - Week 2 - Example 12: measuring liquid level with pressure.

A differential-pressure (DP) transmitter reads dp = rho g h. It converts to level only
if the density is known: a density change looks like a level change. Two DP readings
locate the interface between two immiscible liquids.
"""

from fluidmech.constants import G

# 1. DP level transmitter calibrated for water at 20 degC
rho_cal = 998.0
h_true = 3.0  # actual liquid level [m]
print(f"DP transmitter calibrated with rho = {rho_cal} kg/m3; true level {h_true} m")
for liquid, rho in [("water, 20 degC", 998.0), ("water, 80 degC", 972.0), ("brine", 1180.0), ("light oil", 850.0)]:
    reading = rho * G * h_true / (rho_cal * G)
    print(f"  {liquid:<15} indicated level {reading:5.2f} m (error {reading - h_true:+.2f} m)")

# 2. Interface level in a separator: oil (top) over water, total height known from a second reading
rho_o, rho_w = 850.0, 1000.0
p_bottom = 30.2e3  # gauge pressure at the bottom tapping [Pa]
H_total = 3.3  # total liquid height (from a radar gauge) [m]
# p = rho_w g h_w + rho_o g (H - h_w)  ->  h_w
h_w = (p_bottom / G - rho_o * H_total) / (rho_w - rho_o)  # from p = g [rho_w h_w + rho_o (H - h_w)]
print(f"\nSeparator: bottom pressure {p_bottom / 1e3:.1f} kPa, total liquid {H_total} m")
print(f"  water layer {h_w:.2f} m, oil layer {H_total - h_w:.2f} m")
print(f"  a 1 kPa error in pressure shifts the interface by {1e3 / (G * (rho_w - rho_o)):.2f} m -")
print("  interface measurement is sensitive when the densities are close.")
