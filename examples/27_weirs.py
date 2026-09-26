"""Example 27 - Measuring open-channel flow with sharp-crested weirs.

Rectangular weir:   Q = Cd (2/3) sqrt(2g) L H^(3/2)
V-notch weir:       Q = Cd (8/15) sqrt(2g) tan(theta/2) H^(5/2)
H is the head above the crest, measured well upstream.
"""

import math

from fluidmech.constants import G
from fluidmech.open_channel import RectangularChannel


def rectangular_weir(head: float, length: float, cd: float = 0.62) -> float:
    return cd * (2 / 3) * math.sqrt(2 * G) * length * head**1.5


def v_notch_weir(head: float, angle_deg: float = 90.0, cd: float = 0.58) -> float:
    return cd * (8 / 15) * math.sqrt(2 * G) * math.tan(math.radians(angle_deg / 2)) * head**2.5


print(f"{'H [mm]':>7} {'rect. 1 m [L/s]':>16} {'90d V-notch [L/s]':>18}")
for h_mm in [20, 50, 100, 150, 200, 300, 400]:
    h = h_mm / 1000  # mm -> m
    print(f"{h_mm:>7} {rectangular_weir(h, 1.0) * 1000:>16.1f} {v_notch_weir(h) * 1000:>18.2f}")

# Resolution at small flows: compare both weirs passing the SAME flow
q_small = 0.005  # 5 L/s
h_rect = (q_small / rectangular_weir(1.0, 1.0)) ** (2 / 3)
h_v = (q_small / v_notch_weir(1.0)) ** (2 / 5)
print(f"\nFor a small flow of {q_small * 1000:.0f} L/s:")
for name, func, h in [
    ("rectangular", lambda h: rectangular_weir(h, 1.0), h_rect),
    ("V-notch", v_notch_weir, h_v),
]:
    err = (func(h + 0.001) - func(h)) / func(h)
    print(f"  {name:<12} H = {h * 1000:5.1f} mm; a 1 mm reading error -> {err:.1%} flow error")
print("The V-notch concentrates small flows into a deep, easily read head -> preferred for low flows.")

# Sizing: what weir head does a 0.5 m3/s channel flow give?
Q = 0.5
h_rect = (Q / (0.62 * (2 / 3) * math.sqrt(2 * G) * 2.0)) ** (2 / 3)
print(f"\nA 2 m wide rectangular weir passing Q = {Q} m3/s runs with H = {h_rect:.3f} m")

# Check the approach flow is slow (subcritical) so the head reading is valid
approach = RectangularChannel(2.0)
y_approach = h_rect + 0.6  # weir crest 0.6 m above the bed
print(
    f"Approach channel depth {y_approach:.2f} m, Fr = {approach.froude(y_approach, Q):.3f} (well subcritical -> good)"
)
