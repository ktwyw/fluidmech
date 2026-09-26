"""CHME 202 - Week 12 - Example 1: Darcy's law and permeability.

Darcy (1856): u = (k / mu) dp / L, with superficial velocity u = Q / A and
permeability k [m^2] (1 darcy = 9.87e-13 m^2). The fluid actually moves faster
between the grains: interstitial velocity u / eps.
Reading: McCabe, Smith & Harriott (flow through beds of solids).
"""

from fluidmech import Fluid
from fluidmech import porous as por

water = Fluid.water(20)
# Constant-head permeameter test on a sand column
A, L = 0.0050, 0.30  # column cross-section [m2], sample length [m]
tests = [(5e3, 2.1e-6), (10e3, 4.3e-6), (20e3, 8.4e-6), (40e3, 16.9e-6)]  # (dp [Pa], Q [m3/s])
print(f"Permeameter: A = {A * 1e4:.0f} cm2, L = {L * 100:.0f} cm, water at 20 degC")
print(f"{'dp [kPa]':>9} {'Q [mL/s]':>9} {'u [mm/s]':>9} {'k [m2]':>10}")
ks = []
for dp, q in tests:
    k = por.permeability_from_test(q, A, dp, L, water.dynamic_viscosity)
    ks.append(k)
    print(f"{dp / 1e3:>9.0f} {q * 1e6:>9.2f} {q / A * 1000:>9.3f} {k:>10.3e}")
k = sum(ks) / len(ks)
print(f"Mean permeability k = {k:.2e} m2 = {k / por.DARCY:.1f} darcy")
print(f"Hydraulic conductivity K = {por.hydraulic_conductivity(k) * 100:.3f} cm/s")
print("Q proportional to dp -> Darcy's law holds (creeping flow in the pores).\n")

eps = 0.35  # aquifer porosity
u = 1.0 / (24 * 3600)  # 1 m/day superficial groundwater flux
print(f"Groundwater at a superficial velocity of 1 m/day through porosity {eps}:")
print(f"  interstitial (pore) velocity {1 / eps:.1f} m/day - this is what transports a contaminant plume")
print(f"  hydraulic gradient required: {u * water.dynamic_viscosity / k / (water.density * 9.81):.4f} m/m\n")

print("Typical permeabilities:")
for name, kk in [
    ("gravel", 1e-9),
    ("clean sand", 1e-11),
    ("sandstone oil reservoir", 1e-13),
    ("silt", 1e-14),
    ("clay", 1e-17),
    ("ultrafiltration membrane layer", 1e-18),
]:
    print(f"  {name:<32} {kk:.0e} m2 ({kk / por.DARCY:.2g} darcy)")
