# Examples

Fifty self-contained, runnable worked examples. Each script prints its
results and explains what they mean; a few also save a figure. Run one with

```bash
python examples/01_pipe_design.py
```

or run all 50 (figures go to `examples/output/`):

```bash
python examples/run_all.py
```

Scripts marked 📈 draw a figure. Those marked *(required)* need
`pip install -e ".[examples]"`; the others skip the plot if matplotlib is missing.

## Fluid properties and dimensionless numbers

| # | Script | What it shows |
|---|---|---|
| 05 | `05_property_tables.py` | Textbook-style property tables for water (0–100 °C) and air (−40–200 °C) |
| 06 | `06_property_plots.py` 📈 *(required)* | Viscosity of water and air vs. temperature |
| 07 | `07_reynolds_number_survey.py` | Reynolds numbers from honey to container ships; laminar vs. turbulent |
| 28 | `28_model_similitude.py` | Froude and Reynolds scaling for spillway, valve and ship models |
| 44 | `44_us_customary_units.py` | A pipe and pump problem entered and reported in gpm, ft, psi and hp |

## Hydrostatics

| # | Script | What it shows |
|---|---|---|
| 03 | `03_dam_gate.py` | Force and centre of pressure on vertical and inclined gates |
| 08 | `08_manometers.py` | Piezometer, U-tube and inclined manometers; choosing a gauge liquid |
| 09 | `09_layered_tank.py` | Pressure profile and wall force with oil floating on water |
| 10 | `10_barge_stability.py` | Draft, metacentric height and stability of a loaded barge |

## Bernoulli equation and momentum

| # | Script | What it shows |
|---|---|---|
| 11 | `11_tank_draining.py` | Tank draining time: exact solution vs. numerical integration |
| 12 | `12_flow_meters.py` | Venturi, orifice plate and Pitot tube (including at altitude) |
| 13 | `13_siphon.py` | Siphon flow rate and the cavitation limit at the crest |
| 31 | `31_jet_momentum.py` | Jet forces on plates and vanes, Pelton wheel, fire-hose nozzle |

## Pipe flow

| # | Script | What it shows |
|---|---|---|
| 01 | `01_pipe_design.py` | The three classic pipe problems (head loss, flow rate, diameter) |
| 02 | `02_moody_diagram.py` 📈 *(required)* | A Moody diagram generated from the Colebrook equation |
| 14 | `14_friction_factor_comparison.py` | Accuracy of Swamee–Jain and Haaland vs. Colebrook |
| 15 | `15_pump_operating_point.py` 📈 | Pump and system curves, operating point, pumps in parallel |
| 16 | `16_series_parallel_pipes.py` | Flow distribution in series and parallel pipes |
| 17 | `17_hardy_cross_network.py` | Two-loop pipe network solved with the Hardy Cross method |
| 18 | `18_economic_pipe_diameter.py` | Least-cost diameter: capital cost vs. pumping energy |
| 19 | `19_velocity_profiles.py` | Laminar vs. turbulent velocity profiles and wall shear stress |
| 20 | `20_hvac_duct.py` | Rectangular duct pressure drop using the hydraulic diameter |
| 32 | `32_energy_grade_line.py` | EGL/HGL along a pumped pipeline over a ridge |
| 45 | `45_monte_carlo_uncertainty.py` | Monte Carlo uncertainty of a head-loss calculation |
| 46 | `46_pipe_sizing_chart.py` 📈 *(required)* | Head-loss/flow design chart for standard pipe sizes |
| 49 | `49_irrigation_lateral.py` | Pressure variation along a drip-irrigation lateral with many outlets |

## Pumps

| # | Script | What it shows |
|---|---|---|
| 33 | `33_variable_speed_pump.py` | Energy saved by a variable-speed drive instead of throttling |
| 34 | `34_pumps_series_parallel.py` | When to combine pumps in series and when in parallel |
| 35 | `35_npsh_cavitation.py` | NPSH available vs. required: temperature, suction lift and altitude |
| 47 | `47_tank_filling_simulation.py` | Time simulation of a pump filling a tank as its operating point drifts |

## Pipe networks

| # | Script | What it shows |
|---|---|---|
| 36 | `36_water_distribution_network.py` | A town network with pump, storage tank and 9 nodes; pressure checks |
| 37 | `37_three_reservoir_problem.py` | The classic three-reservoir problem for different reservoir levels |
| 38 | `38_network_scenarios.py` | Average day, peak hour, fire flow and pipe-break scenarios |
| 50 | `50_fire_hydrant_flow_test.py` | Interpreting a hydrant flow test (NFPA 291 method) |

## Water hammer

| # | Script | What it shows |
|---|---|---|
| 21 | `21_water_hammer.py` | Joukowsky surge pressure for different pipe materials and closure times |
| 48 | `48_surge_protection_design.py` | Minimum valve closure time to keep surge within the pipe rating |

## Open-channel flow

| # | Script | What it shows |
|---|---|---|
| 04 | `04_open_channel.py` | Normal and critical depth in a trapezoidal canal |
| 22 | `22_channel_rating_curve.py` | Stage–discharge rating curve and power-law fit |
| 23 | `23_specific_energy.py` 📈 | Specific energy, alternate depths, flow over a hump and choking |
| 24 | `24_hydraulic_jump.py` | Hydraulic jumps: sequent depth, energy loss, jump classification |
| 25 | `25_best_hydraulic_section.py` | Most efficient trapezoidal section (the half hexagon) |
| 26 | `26_gradually_varied_flow.py` 📈 | M1 backwater curve behind a weir (direct step method) |
| 27 | `27_weirs.py` | Rectangular and V-notch weirs for flow measurement |
| 43 | `43_sluice_gate_hydraulic_jump.py` | Where a hydraulic jump forms downstream of a sluice gate |

## External flow

| # | Script | What it shows |
|---|---|---|
| 29 | `29_settling_velocity.py` | Terminal velocity of sand grains and droplets; Stokes' law limits |
| 30 | `30_drag_and_wind_loads.py` | Wind loads on structures, vehicle drag power, golf-ball drag crisis |
| 42 | `42_ship_hull_friction.py` | Skin-friction resistance of a ship; boundary-layer growth along the hull |

## Compressible flow

| # | Script | What it shows |
|---|---|---|
| 39 | `39_converging_diverging_nozzle.py` | Designing a Mach 2.5 nozzle; back-pressure operating regimes |
| 40 | `40_gas_leak_blowdown.py` | Leak rate and blowdown time of a compressed-air receiver |
| 41 | `41_supersonic_wind_tunnel.py` | Normal-shock table; Mach number from a supersonic Pitot tube |

> Numbers such as costs, pump curves and loss coefficients are representative
> values chosen for teaching; replace them with data for your own problem.
