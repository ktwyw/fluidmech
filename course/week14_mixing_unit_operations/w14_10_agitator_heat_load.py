"""CHME 202 - Week 14 - Example 10: agitator power becomes heat - viscous batches warm up.

All shaft power is eventually dissipated by viscosity (Week 5). In low-viscosity
liquids the effect is small; in viscous batches (polymers, pastes) mixing power
can dominate the heat balance and must be removed by the jacket.
"""

from fluidmech import mixing as mx

T, D = 1.5, 0.75  # tank and (close-clearance) impeller diameter [m]
tank = mx.StirredTank(T, D, "pitched_blade_45")
rho_batch = 1100.0  # batch density [kg/m3]
mass = rho_batch * tank.volume  # batch mass [kg]
print(f"Batch of {mass / 1000:.1f} t in a {T} m tank, impeller D = {D} m\n")
print(f"{'liquid':<18} {'mu [Pa s]':>10} {'rpm':>5} {'Re':>9} {'power [kW]':>11} {'dT/dt [K/h]':>12}")
rates = []
for name, mu, cp, rpm in [
    ("water-like", 0.001, 4000, 120),
    ("syrup", 5.0, 2500, 60),
    ("polymer solution", 50.0, 2000, 40),
    ("paste", 200.0, 1800, 30),
]:
    r = tank.analyse(rpm / 60, rho_batch, mu)  # rpm -> rev/s
    dTdt = r["power_W"] / (mass * cp) * 3600  # all shaft power becomes heat; K/s -> K/h
    rates.append(dTdt)
    print(f"{name:<18} {mu:>10} {rpm:>5} {r['reynolds']:>9.3g} {r['power_W'] / 1000:>11.2f} {dTdt:>12.2f}")
print("\nIn laminar flow P = Kp mu N^2 D^3: at a given speed, power is proportional to viscosity.")
print(f"Heating rates here are up to {max(rates):.1f} K/h - over an 8-hour batch that is up to {8 * max(rates):.0f} K,")
print("which the jacket must remove for temperature-sensitive products. Note the paste heats about as fast")
print("as the water-like batch even though it is stirred four times more slowly.")
print("(Close-clearance anchors or helical ribbons are used in practice; the pitched-blade constants here")
print(" are illustrative.)")
