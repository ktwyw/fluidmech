"""CHME 202 - Week 9 - Example 8: valve flow coefficients (Kv, Cv) and control-valve sizing.

Valve data sheets use a flow coefficient instead of K:
    Q [m3/h] = Kv sqrt(dp [bar] / SG),   Cv (US gpm, psi) = 1.156 Kv.
It converts to a loss coefficient via K = 2.59e9 A^2 / Kv^2 (A = pipe area, m2).
A control valve needs enough pressure drop ('authority') to control well.
"""

import math

from fluidmech import Fluid
from fluidmech import pipe_flow as pf

water = Fluid.water(20)
sg = water.density / 1000  # specific gravity
D = 0.0779  # 3" Sch 40
A = math.pi * D**2 / 4
print("Converting catalogue Kv to a loss coefficient in a 3-inch line:")
for name, kv in [("full-bore ball valve", 900), ("gate valve", 600), ("butterfly (open)", 250), ("globe valve", 110)]:
    print(f"  {name:<22} Kv = {kv:>4} m3/h/bar^0.5 (Cv = {1.156 * kv:6.0f}) -> K = {2.592e9 * A**2 / kv**2:6.2f}")

# Size a control valve: Q = 40 m3/h, line friction at max flow 1.2 bar, valve should take ~1/3 of the drop
Q_h = 40.0
# friction drop of the line [bar]
line_dp = pf.head_loss(Q_h / 3600, D, 150.0, water, pf.ROUGHNESS["commercial_steel"], 5.0).pressure_drop / 1e5
dp_valve = 0.5 * line_dp  # valve takes one third of the total variable drop
kv_req = Q_h / math.sqrt(dp_valve / sg)  # Kv definition: Q [m3/h] = Kv sqrt(dp [bar] / SG)
print(f"\nControl valve for {Q_h:.0f} m3/h: line friction {line_dp:.2f} bar, valve drop chosen {dp_valve:.2f} bar")
print(f"  required Kv = {kv_req:.0f}; choose a valve with Kvs ~ {1.3 * kv_req:.0f} (operate at ~70-80 % open)")
print(f"  valve authority = {dp_valve / (dp_valve + line_dp):.2f} (0.25-0.5 recommended)")
print("A valve that takes too little pressure drop cannot control; one that takes too much wastes pump energy.")
