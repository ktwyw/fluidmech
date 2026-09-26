"""CHME 202 - Week 1 - Example 14: surface tension at work - the membrane bubble-point test.

A wetted pore holds liquid by capillarity until the gas pressure exceeds the
capillary (Young-Laplace) pressure dp = 4 sigma cos(theta) / d. The pressure at which
gas first bubbles through (the bubble point) indicates the largest pore - an integrity
test for sterile filters.
"""

sigma_water, sigma_ipa = 0.072, 0.022  # water, isopropanol [N/m]
print("Ideal capillary bubble point for cylindrical pores (theta = 0):")
print(f"{'pore d [um]':>12} {'water [bar]':>12} {'isopropanol [bar]':>18}")
for d_um in [0.1, 0.2, 0.45, 1.0, 5.0]:
    d = d_um * 1e-6
    print(f"{d_um:>12} {4 * sigma_water / d / 1e5:>12.2f} {4 * sigma_ipa / d / 1e5:>18.2f}")
print("\nReal membrane pores are tortuous, not cylindrical, so measured bubble points are lower (about")
print("a quarter of these ideal values); manufacturers publish the calibrated minimum bubble point.")
print("The test is still decisive: a torn membrane or leaking seal bubbles far below the specification.")
print("Low-surface-tension wetting liquids (alcohols) lower the test pressure proportionally.")
