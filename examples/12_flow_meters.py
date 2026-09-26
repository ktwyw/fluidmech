"""Example 12 - Flow measurement: Venturi meter, orifice plate and Pitot tube."""

from fluidmech import Fluid
from fluidmech.bernoulli import pitot_velocity, venturi_flow_rate

water = Fluid.water(20)
d1, d2 = 0.150, 0.075  # pipe and throat/orifice diameter [m]

print(f"Water line D = {d1 * 1000:.0f} mm, throat/orifice d = {d2 * 1000:.0f} mm (beta = {d2 / d1})")
print(f"{'dp [kPa]':>9} {'Venturi Q [L/s]':>16} {'Orifice Q [L/s]':>16}")
for dp_kpa in [1, 2, 5, 10, 20, 50, 100]:
    dp = dp_kpa * 1e3  # kPa -> Pa
    q_v = venturi_flow_rate(d1, d2, dp, water.density, discharge_coefficient=0.98)
    q_o = venturi_flow_rate(d1, d2, dp, water.density, discharge_coefficient=0.61)
    print(f"{dp_kpa:>9} {q_v * 1000:>16.2f} {q_o * 1000:>16.2f}")

print("\nQ is proportional to sqrt(dp): quadrupling dp only doubles Q, so a")
print("meter sized for full flow has poor resolution at low flow (turndown).")

# Permanent pressure loss: Venturi recovers most of dp, orifice plate very little
dp_design = 20e3
print(f"\nAt dp = {dp_design / 1e3:.0f} kPa, typical unrecovered losses:")
print(f"  Venturi       ~10-15 % of dp -> ~{0.12 * dp_design / 1e3:.1f} kPa")
print(f"  Orifice plate ~60-70 % of dp -> ~{0.65 * dp_design / 1e3:.1f} kPa")

# Pitot-static tube on an aircraft at altitude
print("\nPitot-static tube airspeed")
print(f"{'altitude':>9} {'T [degC]':>9} {'p [kPa]':>8} {'rho':>7} {'V for dp=2 kPa [m/s]':>21}")
for alt, t, p in [(0, 15.0, 101.325), (3000, -4.5, 70.1), (6000, -24.0, 47.2), (10000, -50.0, 26.5)]:
    rho = Fluid.air(t, p * 1e3).density  # p in kPa -> Pa
    print(f"{alt:>8}m {t:>9.1f} {p:>8.1f} {rho:>7.3f} {pitot_velocity(2000.0, rho):>21.1f}")
print("Same dp -> higher true airspeed at altitude (why pilots fly 'indicated' airspeed).")
