"""CHME 202 - Week 5 - Example 13: capillary filling (Washburn equation).

A liquid wicking into a horizontal capillary of radius r is pulled by surface tension
(2 sigma cos(theta) / r) and resisted by Poiseuille friction over the wetted length L:
L^2 = sigma r cos(theta) t / (2 mu). Governs wicking in paper, textiles, porous catalyst
supports and passive microfluidic devices.
"""

import math

sigma, theta = 0.072, 0.0  # water surface tension [N/m], contact angle [rad]
print(f"{'liquid':<10} {'r [um]':>7} " + "".join(f"{f'L after {t}s':>14}" for t in (1, 10, 60)))
for name, mu, s in [("water", 1.0e-3, 0.072), ("ethanol", 1.2e-3, 0.022), ("glycerol", 1.41, 0.063)]:
    for r_um in (10, 100):
        r = r_um * 1e-6
        Ls = [math.sqrt(s * r * math.cos(theta) * t / (2 * mu)) for t in (1, 10, 60)]
        print(f"{name:<10} {r_um:>7} " + "".join(f"{L * 1000:>11.1f} mm" for L in Ls))
print("\nL ~ sqrt(t): wicking slows down as the wetted length (and friction) grows. Wider capillaries fill")
print("faster horizontally but rise LESS high vertically (Week 1, capillary rise ~ 1/r) - a trade-off")
print("designers of wicks and paper-based diagnostics must balance.")
