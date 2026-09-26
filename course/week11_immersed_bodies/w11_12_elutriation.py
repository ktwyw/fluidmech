"""CHME 202 - Week 11 - Example 12: elutriation - which particles are blown out of a fluidised bed?

Particles whose terminal velocity is below the gas velocity are carried out of the bed
(elutriated) and must be caught by cyclones. The cut size solves U_t(d) = u_gas.
"""

from fluidmech import Fluid
from fluidmech.drag import terminal_velocity
from fluidmech.solvers import bisect

gas = Fluid.air(400)  # hot fluidising gas
rho_p = 1500.0  # catalyst particles
print(f"Fluidising gas: air at 400 degC (mu = {gas.dynamic_viscosity * 1e6:.1f} uPa s, rho = {gas.density:.3f} kg/m3)")
print(f"Catalyst density {rho_p:.0f} kg/m3\n")
print(f"{'gas velocity [m/s]':>19} {'largest particle carried out [um]':>34}")
for u in [0.1, 0.3, 0.5, 1.0, 2.0]:
    # particle whose terminal velocity equals the gas velocity
    d_cut = bisect(lambda d, u=u: terminal_velocity(d, rho_p, gas) - u, 1e-7, 0.01)
    print(f"{u:>19} {d_cut * 1e6:>34.0f}")
print("\nRaising the gas velocity improves mixing and throughput but blows out more fines; fluid catalytic")
print("cracking units run at high velocity and recover the catalyst with internal cyclones (Example 7).")
print("The hot gas is MORE viscous than cold air, so it carries larger particles at the same velocity.")
