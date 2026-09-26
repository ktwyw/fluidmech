"""CHME 202 - Week 1 - Example 2: how viscosity depends on temperature.

Liquids become LESS viscous when heated (Andrade/Arrhenius behaviour);
gases become MORE viscous (Sutherland's law). We fit the Andrade equation
mu = A exp(B/T) to glycerol data and compare correlations for water and air.
Saves viscosity_temperature.png.

# requires: matplotlib
"""

import math

import matplotlib.pyplot as plt

from fluidmech.properties import air_dynamic_viscosity, water_dynamic_viscosity
from fluidmech.rheology import Andrade

# Glycerol viscosity [Pa s] (literature values, e.g. Segur & Oberstar 1951)
t_gly = [0, 20, 40, 60, 80, 100]
mu_gly = [12.07, 1.412, 0.284, 0.0813, 0.0319, 0.0148]  # [Pa s] at the temperatures above

fit = Andrade.fit(t_gly, mu_gly)
print(f"Andrade fit for glycerol: mu = {fit.A:.3e} exp({fit.B:.0f} / T)")
print(f"Apparent activation energy for viscous flow: {fit.activation_energy / 1000:.0f} kJ/mol\n")
print(f"{'T [degC]':>9} {'data':>9} {'Andrade':>9} {'error':>7}")
for t, m in zip(t_gly, mu_gly):
    print(f"{t:>9} {m:>9.4f} {fit.viscosity(t):>9.4f} {fit.viscosity(t) / m - 1:>+7.0%}")
print("The Arrhenius form captures the 3-decade trend but misses individual points by up to ~30 %:")
print("on a plot of ln(mu) against 1/T, glycerol's data curve instead of lying on a straight line.\n")


# Vogel-Fulcher-Tammann: ln(mu) = a + b / (T - C). For each trial C, a and b follow from a linear fit.
def vft_fit(temps, mus):
    best = None
    for c in range(0, 250):  # try every integer C [K]; keep the one with the smallest squared error
        x = [1 / (t + 273.15 - c) for t in temps]  # VFT is linear in 1/(T - C) once C is fixed
        y = [math.log(m) for m in mus]
        n = len(x)
        xm, ym = sum(x) / n, sum(y) / n
        b = sum((xi - xm) * (yi - ym) for xi, yi in zip(x, y)) / sum((xi - xm) ** 2 for xi in x)
        a = ym - b * xm
        err = sum((a + b * xi - yi) ** 2 for xi, yi in zip(x, y))
        if best is None or err < best[0]:
            best = (err, a, b, c)
    _, a, b, c = best
    return lambda t: math.exp(a + b / (t + 273.15 - c)), (a, b, c)


vft, (a_v, b_v, c_v) = vft_fit(t_gly, mu_gly)
print(f"VFT fit: ln(mu) = {a_v:.2f} + {b_v:.0f} / (T - {c_v:.0f} K)")
print(f"{'T [degC]':>9} {'data':>9} {'VFT':>9} {'error':>7}")
for t, m in zip(t_gly, mu_gly):
    print(f"{t:>9} {m:>9.4f} {vft(t):>9.4f} {vft(t) / m - 1:>+7.1%}")
print("One extra parameter brings the error down to a few percent across the whole range.\n")

water_fit = Andrade.fit([10, 30, 50, 70, 90], [water_dynamic_viscosity(t) for t in (10, 30, 50, 70, 90)])
print(
    f"Water: activation energy {water_fit.activation_energy / 1000:.1f} kJ/mol "
    f"(glycerol is {fit.activation_energy / water_fit.activation_energy:.1f}x more temperature-sensitive)"
)
print(
    f"Heating water from 20 to 80 degC cuts its viscosity by "
    f"{1 - water_dynamic_viscosity(80) / water_dynamic_viscosity(20):.0%}; air's viscosity RISES by "
    f"{air_dynamic_viscosity(80) / air_dynamic_viscosity(20) - 1:.0%}."
)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
ts = [i for i in range(0, 101, 2)]  # 0-100 degC for the plot
axes[0].semilogy(t_gly, mu_gly, "ko", label="glycerol data")
axes[0].semilogy(ts, [fit.viscosity(t) for t in ts], "k--", label="Andrade fit")
axes[0].semilogy(ts, [vft(t) for t in ts], "k:", label="VFT fit")
axes[0].semilogy(ts, [water_dynamic_viscosity(t) for t in ts], label="water")
axes[0].set(xlabel="Temperature [degC]", ylabel="mu [Pa s]", title="Liquids: viscosity falls with T")
axes[0].legend()
axes[0].grid(alpha=0.4, which="both")
ta = list(range(-40, 401, 10))
axes[1].plot(ta, [air_dynamic_viscosity(t) * 1e6 for t in ta])  # Pa s -> uPa s
axes[1].set(xlabel="Temperature [degC]", ylabel="mu [uPa s]", title="Gases: viscosity rises with T (air)")
axes[1].grid(alpha=0.4)
fig.tight_layout()
fig.savefig("viscosity_temperature.png", dpi=130)
print("\nSaved viscosity_temperature.png")
