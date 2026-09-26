"""CHME 202 - Week 5 - Example 9: the cubic law - leakage through thin gaps and fractures.

Plane Poiseuille flow through a gap of height h, width w and length L:
Q = w h^3 dp / (12 mu L). The h^3 dependence makes leakage extremely sensitive to
gap size: flange leaks, valve seats, rock fractures (equivalent permeability h^2/12).
"""

from fluidmech import Fluid

water = Fluid.water(20)
w, L, dp = 0.3, 0.02, 10e5  # leak path width, length, pressure difference (10 bar)
print(f"Leak path {w * 1000:.0f} mm wide, {L * 1000:.0f} mm long, dp = {dp / 1e5:.0f} bar, water\n")
print(f"{'gap [um]':>9} {'Q [mL/min]':>11} {'V [m/s]':>8} {'Re':>7}")
for h_um in [1, 5, 10, 25, 50]:
    h = h_um * 1e-6
    q = w * h**3 * dp / (12 * water.dynamic_viscosity * L)  # plane Poiseuille flow (cubic law)
    v = q / (w * h)
    re = v * 2 * h / water.kinematic_viscosity
    print(f"{h_um:>9} {q * 6e7:>11.3f} {v:>8.2f} {re:>7.1f}")
print("Doubling the gap multiplies the leak by 8 - gasket and seat finish matter enormously.")
print("(Check Re: above a few hundred the flow is no longer laminar and the law overpredicts.)\n")

print("Rock fracture of aperture h behaves like a porous layer of permeability k = h^2 / 12:")
for h_um in [10, 100, 1000]:
    k = (h_um * 1e-6) ** 2 / 12  # equivalent permeability of a slot [m2]
    print(f"  h = {h_um:>5} um: k = {k:.2e} m2 = {k / 9.869e-13:,.0f} darcy")
print("A single 0.1 mm crack is more permeable than coarse gravel (see Week 12).")
