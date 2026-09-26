"""CHME 202 - Week 11 - Example 3: terminal velocities of drops and bubbles.

Fluid spheres differ from solid ones: internal circulation reduces drag
(Hadamard-Rybczynski), but surfactants immobilise the interface so small bubbles
in real (contaminated) water behave like rigid spheres. Larger bubbles deform;
their rise speed is set by surface tension and buoyancy (Mendelson).
Relevant to bubble columns, aeration tanks and liquid-liquid extraction.
"""

from fluidmech import Fluid
from fluidmech.drag import (
    eotvos_number,
    hadamard_rybczynski_velocity,
    mendelson_bubble_velocity,
    morton_number,
    terminal_velocity,
)
from fluidmech.properties import water_surface_tension

water = Fluid.water(20)
sigma = water_surface_tension(20)
rho_air, mu_air = 1.2, 1.8e-5  # gas inside the bubble
print(f"Air bubbles rising in water at 20 degC (Mo = {morton_number(water, water.density, sigma):.2e})")
print(f"{'d [mm]':>7} {'Eo':>6} {'clean (H-R)':>12} {'contaminated':>13} {'Mendelson':>10}   [m/s]")
for d_mm in [0.1, 0.3, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0]:
    d = d_mm / 1000  # mm -> m
    eo = eotvos_number(d, water.density, sigma)
    # sign flipped: bubbles rise (negative settling velocity)
    hr = -hadamard_rybczynski_velocity(d, rho_air, mu_air, water)
    rigid = -terminal_velocity(d, rho_air, water)
    mend = mendelson_bubble_velocity(d, sigma, water)
    re_hr = water.density * hr * d / water.dynamic_viscosity  # creeping-flow formula valid only for Re < 1
    hr_txt = f"{hr:>12.3f}" if re_hr < 1 else f"{'(Re > 1)':>12}"
    rigid_txt = f"{rigid:>13.3f}" if d_mm <= 2.0 else f"{'(deformed)':>13}"
    mend_txt = f"{mend:>10.3f}" if d_mm >= 1.5 else f"{'-':>10}"
    print(f"{d_mm:>7} {eo:>6.2f} {hr_txt} {rigid_txt} {mend_txt}")
print("Each estimate is shown only inside its range of validity.")
print("Small bubbles (Eo << 1) stay spherical; above ~1.5 mm they wobble and rise at ~0.2-0.3 m/s")
print("almost regardless of size. Real rise velocities lie between the clean and contaminated values.\n")

print("Liquid drops falling through air (rigid-sphere estimate, valid until drops deform above ~1 mm):")
air = Fluid.air(20)
for d_mm in [0.05, 0.1, 0.5, 1.0]:
    print(f"  d = {d_mm} mm: U_t = {terminal_velocity(d_mm / 1000, 998.0, air):.3f} m/s")
print("\nOrganic drops in water (liquid-liquid extraction): toluene, d = 1 mm, mu_d = 0.59 mPa s")
toluene_rise = -hadamard_rybczynski_velocity(1e-3, 867.0, 0.59e-3, water)
print(
    f"  creeping-flow (Hadamard-Rybczynski) estimate: {toluene_rise * 1000:.1f} mm/s upward; check Re = "
    f"{water.density * toluene_rise * 1e-3 / water.dynamic_viscosity:.0f} (above 1, so only indicative)"
)
