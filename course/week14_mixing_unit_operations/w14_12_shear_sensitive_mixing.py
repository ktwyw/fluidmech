"""CHME 202 - Week 14 - Example 12: agitating shear-sensitive material (cells, crystals, flocs).

Damage relates to the smallest turbulent eddies: when the Kolmogorov scale approaches the
particle size, eddies act across the particle. Near the impeller the local dissipation is
much higher than the tank average. Tip speed is a common practical proxy.
Limits quoted below are indicative; they depend strongly on the specific cells or crystals.
"""

from fluidmech import mixing as mx
from fluidmech.turbulence import kolmogorov_scales

rho, mu = 1000.0, 1e-3  # culture medium ~ water
tank = mx.StirredTank(2.0, 0.8, "hydrofoil")
particle = 20e-6  # e.g. an animal cell or microcarrier-scale particle
print(f"2 m bioreactor with a hydrofoil (D = 0.8 m); particles of {particle * 1e6:.0f} um\n")
print(f"{'rpm':>5} {'tip [m/s]':>10} {'P/V [W/m3]':>11} {'eta_K mean [um]':>16} {'eta_K impeller [um]':>20}")
for rpm in [20, 40, 60, 90, 120]:
    r = tank.analyse(rpm / 60, rho, mu)  # rpm -> rev/s
    eta_mean = kolmogorov_scales(r["dissipation_W_kg"], mu / rho)[0]
    eta_imp = kolmogorov_scales(30 * r["dissipation_W_kg"], mu / rho)[0]  # impeller zone ~30x the mean dissipation
    flag = "  <- eddies comparable to particle size" if eta_imp < 1.5 * particle else ""
    print(
        f"{rpm:>5} {r['tip_speed_m_s']:>10.2f} {r['power_per_volume_W_m3']:>11.1f} {eta_mean * 1e6:>16.0f} "
        f"{eta_imp * 1e6:>20.0f}{flag}"
    )
print("\nSensitive cultures are typically run at low P/V (tens of W/m3) with large, slow axial impellers.")
print("The trade-off: enough mixing and oxygen transfer (Example 8) without damaging the product.")
