"""CHME 202 - Week 1 - Example 6: surface tension, capillarity and the Young-Laplace equation.

Capillary rise h = 2 sigma cos(theta) / (rho g r); pressure jump across a curved
interface dp = 2 sigma / R (drop) or 4 sigma / R (soap bubble, two surfaces).
Reading: White, Section 1.9.
"""

import math

from fluidmech.constants import G
from fluidmech.properties import water_density, water_surface_tension

sigma, rho = water_surface_tension(20), water_density(20)
print(f"Water at 20 degC: sigma = {sigma * 1000:.1f} mN/m\n")

print("Capillary rise of water in a clean glass tube (contact angle ~0):")
for d_mm in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
    r = d_mm / 2000
    h = 2 * sigma / (rho * G * r)  # capillary rise, contact angle 0 (cos = 1)
    print(f"  d = {d_mm:>5} mm: h = {h * 1000:7.1f} mm")
print("Manometer tubes should be > ~10 mm in diameter so capillary error is negligible.\n")

sigma_hg, rho_hg, theta_hg = 0.484, 13546.0, 130.0  # mercury: sigma [N/m], density [kg/m3], contact angle [deg]
# negative (cos 130 < 0): a depression; r = 0.5 mm
h_hg = 2 * sigma_hg * math.cos(math.radians(theta_hg)) / (rho_hg * G * 0.0005)
print(f"Mercury in a 1 mm tube (contact angle {theta_hg:.0f} deg): capillary DEPRESSION of {-h_hg * 1000:.1f} mm\n")

print("Pressure inside droplets and bubbles (Young-Laplace):")
for d_um in [1, 10, 100, 1000]:
    r = d_um * 1e-6 / 2
    print(
        f"  d = {d_um:>5} um: water droplet dp = {2 * sigma / r / 1000:9.2f} kPa, "
        f"soap bubble dp = {4 * 0.025 / r / 1000:9.2f} kPa"
    )
print("Tiny bubbles have very high internal pressure - one reason nucleating cavitation needs large tensions.")
