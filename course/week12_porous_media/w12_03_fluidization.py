"""CHME 202 - Week 12 - Example 3: from packed bed to fluidised bed.

As gas velocity rises, the bed pressure drop follows Ergun until it equals the
bed's buoyant weight per unit area; above u_mf the bed fluidises and dp stays
constant. Above the particle terminal velocity, particles are blown out.
Saves fluidization.png.

# requires: matplotlib
"""

import matplotlib.pyplot as plt

from fluidmech import Fluid
from fluidmech import porous as por
from fluidmech.drag import terminal_velocity

air = Fluid.air(20)
d_p, rho_p = 300e-6, 2600.0  # sand
eps_mf, bed_height_mf = 0.44, 0.5  # voidage and bed height at minimum fluidisation
dp_bed = por.fluidized_bed_pressure_drop(bed_height_mf, eps_mf, rho_p, air.density)
u_mf = por.minimum_fluidization_velocity(d_p, rho_p, air.density, air.dynamic_viscosity, voidage_mf=eps_mf)
u_wy = por.minimum_fluidization_velocity(d_p, rho_p, air.density, air.dynamic_viscosity)
u_t = terminal_velocity(d_p, rho_p, air)
ar = por.archimedes_number(d_p, rho_p, air.density, air.dynamic_viscosity)
print(f"Sand d = {d_p * 1e6:.0f} um, rho_p = {rho_p} kg/m3 in air; Ar = {ar:.0f}")
print(f"  bed weight per area (fluidised dp) = {dp_bed / 1e3:.2f} kPa")
print(f"  u_mf (Ergun, eps_mf = {eps_mf}) = {u_mf * 100:.1f} cm/s; Wen & Yu correlation = {u_wy * 100:.1f} cm/s")
for e in (0.40, 0.42, 0.46):
    u_e = por.minimum_fluidization_velocity(d_p, rho_p, air.density, air.dynamic_viscosity, voidage_mf=e)
    print(f"     sensitivity: eps_mf = {e:.2f} -> u_mf = {u_e * 100:.1f} cm/s")
print("  Ergun's u_mf depends strongly on the (uncertain) voidage at minimum fluidisation; Wen & Yu is an")
print("  empirical fit to many beds. Measure u_mf in the lab when it matters.")
print(f"  terminal velocity u_t = {u_t:.2f} m/s -> operating window u_t / u_mf = {u_t / u_mf:.0f}")

us = [u_mf * 0.02 * i for i in range(1, 200)]  # 0 to ~4 u_mf
# fixed bed (Ergun) until dp reaches the bed weight, then constant
dps = [
    min(por.ergun_pressure_gradient(u, d_p, eps_mf, air.dynamic_viscosity, air.density) * bed_height_mf, dp_bed)
    for u in us
]
fig, ax = plt.subplots(figsize=(6.5, 4.2))
ax.plot([u * 100 for u in us], [p / 1e3 for p in dps])
ax.axvline(u_mf * 100, ls="--", color="grey")
ax.text(u_mf * 100 * 1.05, dp_bed / 1e3 * 0.5, "u_mf")
ax.set(xlabel="superficial velocity [cm/s]", ylabel="bed pressure drop [kPa]", title="Fluidisation curve (idealised)")
fig.tight_layout()
fig.savefig("fluidization.png", dpi=130)
print("Saved fluidization.png")
print("\nReal beds show a small overshoot at u_mf (breaking interparticle contacts) and hysteresis.")
