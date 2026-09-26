"""CHME 202 - Week 11 - Example 14: very small particles - slip correction and Brownian motion.

Below ~1 um, air no longer behaves as a continuum around the particle: the Cunningham
factor C = 1 + Kn [1.257 + 0.4 exp(-1.1 / Kn)] (Kn = 2 lambda / d, lambda = 0.066 um)
speeds up settling. Brownian diffusion (D = C k T / (3 pi mu d)) then dominates over settling.
Relevant to clean rooms, filters and nanoparticle handling.
"""

import math

from fluidmech import Fluid
from fluidmech.constants import G

air = Fluid.air(20)
# mean free path of air [m], Boltzmann constant, T [K], density
lam, kB, T, rho_p = 0.066e-6, 1.380649e-23, 293.15, 1000.0
print(f"{'d [um]':>7} {'Cunningham C':>13} {'settling [um/s]':>16} {'Brownian rms in 1 s [um]':>25}  dominant")
for d_um in [0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0]:
    d = d_um * 1e-6
    kn = 2 * lam / d  # Knudsen number
    C = 1 + kn * (1.257 + 0.4 * math.exp(-1.1 / kn))  # Cunningham slip correction
    v_s = C * rho_p * G * d**2 / (18 * air.dynamic_viscosity)
    D = C * kB * T / (3 * math.pi * air.dynamic_viscosity * d)  # Stokes-Einstein diffusivity with slip
    x_rms = math.sqrt(2 * D * 1.0)  # rms Brownian displacement in 1 s (one direction)
    dominant = "Brownian" if x_rms > v_s * 1.0 else "settling"
    print(f"{d_um:>7} {C:>13.2f} {v_s * 1e6:>16.3g} {x_rms * 1e6:>25.3g}  {dominant}")
print("\nParticles of ~0.1-1 um neither settle nor diffuse quickly - they stay airborne for days and are")
print("the hardest to filter (the 'most penetrating particle size' that HEPA filters are rated at).")
