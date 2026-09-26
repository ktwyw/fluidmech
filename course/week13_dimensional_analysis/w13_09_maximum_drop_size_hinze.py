"""CHME 202 - Week 13 - Example 9: dimensional reasoning for drop break-up (Kolmogorov-Hinze).

A drop breaks when the turbulent stress rho u'^2 across it overcomes surface tension
sigma/d: a critical Weber number. With u'^2 ~ (eps d)^(2/3) in the inertial range this
gives d_max = C (sigma / rho)^(3/5) eps^(-2/5), with C ~ 0.725 (Hinze, 1955).
Used for emulsification, liquid-liquid extraction and dispersing gas.
"""

from fluidmech import mixing as mx
from fluidmech.turbulence import kolmogorov_scales

rho_c, mu_c = 1000.0, 1e-3  # continuous phase (water)
sigma = 0.030  # oil-water interfacial tension [N/m]
tank = mx.StirredTank(0.5, 0.5 / 3)
print("Oil drops dispersed in water by a Rushton turbine in a 0.5 m tank:\n")
print(f"{'rpm':>5} {'P/V [W/m3]':>11} {'eps [W/kg]':>11} {'d_max [um]':>11} {'Kolmogorov eta [um]':>20}")
for rpm in [150, 300, 450, 600]:
    r = tank.analyse(rpm / 60, rho_c, mu_c)  # rpm -> rev/s
    # break-up happens in the impeller zone (~10x mean)
    eps_local = 10 * r["dissipation_W_kg"]  # break-up happens in the impeller zone (~10x mean)
    d_max = 0.725 * (sigma / rho_c) ** 0.6 * eps_local ** (-0.4)  # Hinze (1955)
    eta = kolmogorov_scales(eps_local, mu_c / rho_c)[0]
    print(f"{rpm:>5} {r['power_per_volume_W_m3']:>11.0f} {eps_local:>11.2f} {d_max * 1e6:>11.0f} {eta * 1e6:>20.1f}")
print("\nd_max ~ eps^-0.4 ~ N^-1.2: doubling the speed shrinks drops by ~2.3x. The drops are larger than the")
print("Kolmogorov scale, as the inertial-range argument assumes. Adding surfactant lowers sigma and")
print("the drop size - the principle of emulsifiers.")
