"""CHME 202 - Week 11 - Example 9: sizing a gravity settling chamber.

Gas flows horizontally at u through a chamber of height H and length L. A particle
is caught if it settles through H in the residence time L/u: U_t >= u H / L.
For smaller particles (plug flow, no mixing) the collection efficiency is U_t L / (u H).
"""

from fluidmech import Fluid
from fluidmech.drag import terminal_velocity

air = Fluid.air(80)
Q = 2.0  # m3/s of hot gas
W, H, L = 2.0, 1.5, 6.0
u = Q / (W * H)  # mean horizontal gas velocity
rho_p = 2200.0  # dust density [kg/m3]
print(f"Settling chamber {L} x {W} x {H} m, {Q} m3/s of air at 80 degC -> u = {u:.2f} m/s")
ut_needed = u * H / L
print(f"Complete capture needs U_t >= u H / L = {ut_needed * 100:.1f} cm/s\n")
print(f"{'d [um]':>7} {'U_t [cm/s]':>11} {'efficiency':>11}")
for d_um in [10, 20, 40, 60, 80, 120]:
    ut = terminal_velocity(d_um * 1e-6, rho_p, air)
    eff = min(1.0, ut * L / (u * H))  # fraction settling before the outlet (plug flow, no mixing)
    print(f"{d_um:>7} {ut * 100:>11.2f} {eff:>11.1%}")
print("\nTrays that divide the height into n shelves multiply the efficiency by n (Howard chamber).")
print("Settling chambers are cheap pre-cleaners for coarse particles; fine dust needs cyclones (Example 7).")
