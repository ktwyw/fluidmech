"""CHME 202 - Week 10 - Example 15: choosing a pump on life-cycle cost, not purchase price.

Energy usually dominates a pump's life-cycle cost (LCC). We compare two candidates for
the same duty over 15 years with discounting. Prices and efficiencies are ILLUSTRATIVE.
"""

from fluidmech.constants import G

Q, H, hours = 0.05, 40.0, 6000  # duty and operating hours per year
price_kwh, years, rate = 0.08, 15, 0.08  # electricity [$/kWh], evaluation period [yr], discount rate
motor_eff = 0.94  # electric motor efficiency
p_hyd = 1000 * G * Q * H  # power delivered to the water, rho g Q H [W]
candidates = {"Pump A (cheaper)": (8000.0, 0.72, 400.0), "Pump B (high efficiency)": (12000.0, 0.81, 400.0)}
# name: (purchase + installation [$], pump efficiency at duty, maintenance [$/yr])
annuity = sum(1 / (1 + rate) ** y for y in range(1, years + 1))  # present value of 1 $/yr for `years`
print(f"Duty {Q * 1000:.0f} L/s at {H:.0f} m, {hours} h/yr, {price_kwh} $/kWh, {years} years at {rate:.0%} discount\n")
print(f"{'pump':<26} {'power [kW]':>11} {'energy $/yr':>12} {'LCC [$]':>10} {'energy share':>13}")
for name, (capex, eta, maint) in candidates.items():
    kw = p_hyd / (eta * motor_eff) / 1000  # electrical input [kW]
    energy = kw * hours * price_kwh
    lcc = capex + (energy + maint) * annuity
    print(f"{name:<26} {kw:>11.2f} {energy:>12,.0f} {lcc:>10,.0f} {energy * annuity / lcc:>13.0%}")
# Simple payback of the efficient pump, derived from the table above (edit the table, not these lines)
(capex_a, eta_a, _), (capex_b, eta_b, _) = candidates.values()
diff_capex = capex_b - capex_a  # extra purchase cost [$]
saving = (p_hyd / (eta_a * motor_eff) - p_hyd / (eta_b * motor_eff)) / 1000 * hours * price_kwh  # W -> kW, x h x $/kWh
print(
    f"\nThe efficient pump costs {diff_capex:,.0f} $ more but saves {saving:,.0f} $/yr: simple payback "
    f"{diff_capex / saving:.1f} years."
)
print("Energy is ~90 % of the LCC, so a few points of efficiency (and operating near BEP) matter most.")
