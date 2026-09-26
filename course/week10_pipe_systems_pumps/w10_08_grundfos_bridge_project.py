"""CHME 202 - Week 10 - Bridge project: specifying the hydraulic duty for a water-supply pump.

Implements the joint exercise proposed in the CHME 202 / Grundfos alignment statement:
given a target flow, pipe schedule, elevation and operating hours, students
  1. calculate the system head across the operating range,
  2. compare a candidate pump curve and efficiency with that system curve,
  3. estimate the energy implications of fixed-speed throttling vs. variable speed,
  4. check NPSH, and
  5. document assumptions and the checks that require supervision.

IMPORTANT: the candidate pump curve below is ILLUSTRATIVE, not a Grundfos product.
In the real exercise, enter the duty point in Grundfos Product Center, export the
proposed pump's flow-head and efficiency data, and paste them into CANDIDATE.
The script writes system_curve.csv so the system curve can be compared with
manufacturer data in a spreadsheet.
"""

import csv

from fluidmech import Fluid, PumpCurve, pumps
from fluidmech import pipe_flow as pf
from fluidmech.constants import G
from fluidmech.solvers import bisect

# ----------------------------------------------------------------------------- inputs
water = Fluid.water(10)
STATIC_HEAD = 28.0  # elevated tank level minus ground reservoir level [m]
SUCTION = {"length": 8.0, "diameter": 0.1541, "k": 0.5 + 0.3 + 0.15}  # 6" Sch 40
DISCHARGE = {"length": 850.0, "diameter": 0.1541, "k": 6 * 0.3 + 2 * 0.15 + 2.5 + 1.0}  # + check valve, exit
ROUGHNESS = pf.ROUGHNESS["commercial_steel"]
DEMAND_PROFILE = [  # (flow [m3/h], hours per year at this flow)
    (40, 1500),
    (60, 2000),
    (80, 1500),
    (100, 800),
    (110, 200),
]
ELECTRICITY_PRICE = 0.08  # $/kWh (assumption - use the site tariff)
MOTOR_EFF, DRIVE_EFF = 0.93, 0.97
SUCTION_STATIC = 1.5  # reservoir level above the pump inlet [m] (flooded suction)
NPSHR_AT_MAX = 3.5  # from the candidate pump data sheet [m] (illustrative)

# Illustrative candidate pump: flow [m3/h], head [m], efficiency [-]
CANDIDATE = {
    "flow_m3h": [0, 40, 80, 120, 140],
    "head_m": [55, 54, 50.5, 44, 39],
    "efficiency": [0, 0.60, 0.78, 0.74, 0.66],
}


# ----------------------------------------------------------------------------- 1. system head
def system_head(q: float) -> float:
    if q <= 0:
        return STATIC_HEAD
    loss = sum(
        pf.head_loss(q, s["diameter"], s["length"], water, ROUGHNESS, s["k"]).total_head_loss
        for s in (SUCTION, DISCHARGE)
    )
    return STATIC_HEAD + loss


print("1. SYSTEM HEAD ACROSS THE OPERATING RANGE")
print(f"{'Q [m3/h]':>9} {'H_sys [m]':>10} {'V [m/s]':>8}")
with open("system_curve.csv", "w", newline="") as fh:
    writer = csv.writer(fh)
    writer.writerow(["flow_m3h", "system_head_m"])
    for qh in range(0, 141, 10):  # system curve 0-140 m3/h
        h = system_head(qh / 3600)
        writer.writerow([qh, round(h, 3)])
        if qh % 20 == 0:
            print(f"{qh:>9} {h:>10.2f} {pf.mean_velocity(qh / 3600, DISCHARGE['diameter']) if qh else 0:>8.2f}")
print("   (written to system_curve.csv)")
q_max = max(q for q, _ in DEMAND_PROFILE) / 3600  # highest duty [m3/s] sets the design point
print(f"   Design duty point: {q_max * 3600:.0f} m3/h at {system_head(q_max):.1f} m\n")

# ----------------------------------------------------------------------------- 2. pump vs system
pump = PumpCurve.from_points([q / 3600 for q in CANDIDATE["flow_m3h"]], CANDIDATE["head_m"], CANDIDATE["efficiency"])
op = pumps.operating_point(pump, system_head, water.density)
bep = pump.best_efficiency_point()
print("2. CANDIDATE PUMP (illustrative data)")
print(
    f"   full-speed operating point {op.flow_rate * 3600:.1f} m3/h at {op.head:.1f} m, efficiency {op.efficiency:.0%}"
)
print(f"   BEP {bep * 3600:.0f} m3/h; design duty is at {q_max / bep:.0%} of BEP")
margin = pump.head(q_max) - system_head(q_max)
print(
    f"   head margin at design flow: {margin:+.1f} m"
    + ("" if margin >= 0 else "  <- PUMP TOO SMALL: choose a larger pump or impeller")
)
print()

# ----------------------------------------------------------------------------- 3. energy
print("3. ANNUAL ENERGY: fixed speed + throttling valve vs variable-speed drive")
print(f"{'Q [m3/h]':>9} {'hours':>6} | {'throttled kW':>12} | {'speed':>6} {'VFD kW':>7}")
e_throttle = e_vfd = 0.0
for qh, hours in DEMAND_PROFILE:
    q = qh / 3600
    if pump.head(q) < system_head(q):
        print(f"{qh:>9} {hours:>6} | cannot deliver this flow at full speed - duty not met")
        continue
    p_thr = water.density * G * q * pump.head(q) / pump.efficiency(q) / MOTOR_EFF
    h_need = system_head(q)
    # speed at which the pump exactly meets the system head
    ratio = bisect(lambda r, q=q, h=h_need: pump.scaled(speed_ratio=r).head(q) - h, 0.3, 1.0)
    slow = pump.scaled(speed_ratio=ratio)
    p_vfd = water.density * G * q * h_need / slow.efficiency(q) / (MOTOR_EFF * DRIVE_EFF)
    e_throttle += p_thr * hours / 1000  # W x h -> kWh
    e_vfd += p_vfd * hours / 1000  # W x h -> kWh
    print(f"{qh:>9} {hours:>6} | {p_thr / 1000:>12.1f} | {ratio:>6.1%} {p_vfd / 1000:>7.1f}")
hours_total = sum(h for _, h in DEMAND_PROFILE)
print(f"   annual energy, throttled: {e_throttle:,.0f} kWh  ({e_throttle * ELECTRICITY_PRICE:,.0f} $)")
print(f"   annual energy, VFD:       {e_vfd:,.0f} kWh  ({e_vfd * ELECTRICITY_PRICE:,.0f} $)")
print(f"   saving {1 - e_vfd / e_throttle:.0%} over {hours_total} operating hours\n")

# ----------------------------------------------------------------------------- 4. NPSH
suction_loss = pf.head_loss(
    q_max, SUCTION["diameter"], SUCTION["length"], water, ROUGHNESS, SUCTION["k"]
).total_head_loss
npsha = pumps.npsh_available(SUCTION_STATIC, suction_loss, fluid_temperature=10)
print("4. NPSH CHECK at maximum flow")
print(
    f"   NPSHa = {npsha:.2f} m, NPSHr = {NPSHR_AT_MAX:.2f} m, margin {npsha - NPSHR_AT_MAX:+.2f} m "
    f"-> {'acceptable' if npsha - NPSHR_AT_MAX > 1.0 else 'REVIEW'}\n"
)

# ----------------------------------------------------------------------------- 5. documentation
print("5. ASSUMPTIONS AND CHECKS REQUIRING SUPERVISION")
for line in [
    "Water at 10 degC; new commercial-steel pipe (roughness will increase with age).",
    "Fitting K values are typical textbook values, not supplier data.",
    "Demand profile and electricity price are assumptions - obtain site data.",
    "Candidate pump data are illustrative; replace with the proposed product's curves.",
    "Motor and drive efficiencies assumed constant; real values fall at part load.",
    "Not covered: materials and seals, minimum-flow protection, surge on pump trip (fluidmech.transients),",
    "  controls, electrical integration and installation safety - these need product training.",
]:
    print(f"   {'' if line.startswith('  ') else '- '}{line}")
