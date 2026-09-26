"""CHME 202 - Week 5 - Example 5: oscillating flows and the Stokes layer (Stokes' second problem).

A plate oscillating at frequency omega drags a layer of thickness
delta ~ sqrt(2 nu / omega) with it; beyond that the fluid hardly moves.
Relevant to oscillatory rheometers, pulsatile blood flow and acoustics.
"""

import math

from fluidmech import Fluid
from fluidmech.laminar import stokes_second_problem

fluids = [Fluid.air(20), Fluid.water(20), Fluid(1261.0, 1.41, "glycerol")]
print(
    f"{'frequency':>10} " + "".join(f"{f.name[:14]:>16}" for f in fluids) + "   (Stokes layer depth sqrt(2 nu / omega))"
)
for hz in [0.1, 1, 10, 100, 1000]:
    w = 2 * math.pi * hz  # Hz -> rad/s
    print(f"{hz:>8} Hz " + "".join(f"{math.sqrt(2 * f.kinematic_viscosity / w) * 1000:>13.3f} mm" for f in fluids))

nu = Fluid.water(20).kinematic_viscosity
w = 2 * math.pi * 1.0
delta = math.sqrt(2 * nu / w)
print(f"\nWater, 1 Hz: velocity amplitude and phase lag across the layer (delta = {delta * 1000:.2f} mm)")
for k in [0, 1, 2, 3, 4]:
    y = k * delta
    amp = math.exp(-y / delta)
    print(
        f"  y = {k} delta: amplitude {amp:6.1%}, phase lag {math.degrees(y / delta):5.0f} deg,"
        f" u at t=0: {stokes_second_problem(y, 0.0, 1.0, w, nu):+.3f}"
    )
print("The motion decays by e^-1 per delta and lags further behind the plate with distance.")
print(
    "Womersley number for the aorta (R = 12 mm, 1.2 Hz, blood): "
    f"{0.012 * math.sqrt(2 * math.pi * 1.2 / 3.3e-6):.0f} -> flat, not parabolic, pulsatile profile."
)
