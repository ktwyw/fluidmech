"""CHME 202 - Week 1 - Example 12: estimating the viscosity of a liquid mixture.

A common first estimate is the Arrhenius (Grunberg-Nissan with zero interaction)
mixing rule ln(mu_mix) = sum x_i ln(mu_i). We test it on glycerol-water, a strongly
non-ideal system, against measured data at 20 degC.
"""

import math

mu_w, mu_g = 1.002e-3, 1.412  # water, glycerol at 20 degC [Pa s]
M_w, M_g = 18.02, 92.09
# Measured viscosity of glycerol-water solutions at 20 degC (mass % glycerol -> mPa s)
data = {20: 1.76, 40: 3.72, 60: 10.8, 80: 60.1, 90: 219.0}
print(f"{'wt % glycerol':>14} {'mole frac':>10} {'measured':>9} {'mole rule':>10} {'mass rule':>10}   [mPa s]")
for wt, measured in data.items():
    w = wt / 100
    x = (w / M_g) / (w / M_g + (1 - w) / M_w)  # mass fraction -> mole fraction
    mole_rule = math.exp(x * math.log(mu_g) + (1 - x) * math.log(mu_w)) * 1000  # Pa s -> mPa s
    mass_rule = math.exp(w * math.log(mu_g) + (1 - w) * math.log(mu_w)) * 1000  # Pa s -> mPa s
    print(f"{wt:>14} {x:>10.3f} {measured:>9.2f} {mole_rule:>10.2f} {mass_rule:>10.2f}")
print("\nNeither simple rule is reliable for this hydrogen-bonded mixture: the mole-fraction rule is too low")
print("at every composition and the mass-fraction rule too high (by up to ~7x). For design, use measured data or a")
print("fitted correlation - an error of 3x in viscosity is an error of 3x in laminar pressure drop.")
