"""CHME 202 - Week 10 - Example 14: how quickly does the flow build up when a pump starts?

Treating the water in the pipe as a rigid column of length L and area A:
(L / (g A)) dQ/dt = H_pump(Q) - H_system(Q).
The flow approaches the operating point with a time constant set by the inertia of the column.
Pump data are ILLUSTRATIVE.
"""

import math

from fluidmech import Fluid, PumpCurve, pumps
from fluidmech.constants import G

water = Fluid.water(20)
pump = PumpCurve.from_points([0, 0.02, 0.04, 0.06], [45, 43, 37, 27])
for L in [100.0, 1000.0, 5000.0]:
    D = 0.2  # pipe diameter [m]
    A = math.pi * D**2 / 4
    system = pumps.system_curve(20.0, D, L, water, 0.1e-3, 5.0)
    op = pumps.operating_point(pump, system)
    q, t, dt = 0.0, 0.0, 0.01  # start from rest; time step [s]
    t95 = None
    while t < 600:  # rigid-column model, explicit time stepping
        q += dt * G * A / L * (pump.head(q) - system(q))  # (L / g A) dQ/dt = H_pump - H_system
        t += dt
        if t95 is None and q >= 0.95 * op.flow_rate:
            t95 = t
            break
    print(f"L = {L:>5.0f} m: steady flow {op.flow_rate * 1000:5.1f} L/s, reaches 95 % after {t95:6.1f} s")
print("\nLong pipelines take much longer to accelerate (the time scales with L). The same inertia makes")
print("sudden STOPS dangerous: stopping the column quickly causes water hammer (fluidmech.transients).")
