# Week 3 - Elementary fluid dynamics: the Bernoulli equation

**Syllabus:** Development of Bernoulli's law and its application for frictionless inviscid fluids.

**Course learning outcomes:** CLO 1, 2, 3, 4  |  **Assessment:** Lab Assignment #1

**Reading:** White, Sections 3.5-3.7 (Bernoulli equation, energy and hydraulic grade lines).

## Learning objectives

- Apply Bernoulli's equation along a streamline, including stagnation and Pitot measurements.
- Draw energy and hydraulic grade lines and identify sub-atmospheric regions and cavitation risk.
- Calibrate a flow meter and interpret discharge coefficients.
- State and quantify the limits of Bernoulli's equation (friction, compressibility, unsteadiness).

## Scripts

| Script | Content | Needs |
|---|---|---|
| [`w03_01_pitot_traverse.py`](w03_01_pitot_traverse.py) | Stagnation pressure and a Pitot-tube traverse | fluidmech only |
| [`w03_02_nozzle_and_free_jet.py`](w03_02_nozzle_and_free_jet.py) | Jets from tanks and nozzles | fluidmech only |
| [`w03_03_lab1_venturi_calibration.py`](w03_03_lab1_venturi_calibration.py) | Calibrating a Venturi meter | matplotlib |
| [`w03_04_egl_hgl_ideal_system.py`](w03_04_egl_hgl_ideal_system.py) | Energy and hydraulic grade lines for frictionless flow | matplotlib |
| [`w03_05_limits_of_bernoulli.py`](w03_05_limits_of_bernoulli.py) | When does Bernoulli's equation fail? | fluidmech only |
| [`w03_06_pressurized_vessel_transfer.py`](w03_06_pressurized_vessel_transfer.py) | Transferring liquid by pressurising a vessel | fluidmech only |
| [`w03_07_energy_equation_with_pump.py`](w03_07_energy_equation_with_pump.py) | The steady-flow energy equation - Bernoulli plus pumps and losses | fluidmech only |
| [`w03_08_spray_nozzles.py`](w03_08_spray_nozzles.py) | Spray nozzles - flow rate versus pressure | fluidmech only |
| [`w03_09_venturi_cavitation.py`](w03_09_venturi_cavitation.py) | Throat pressure and cavitation in a Venturi | fluidmech only |
| [`w03_10_diffuser_pressure_recovery.py`](w03_10_diffuser_pressure_recovery.py) | Diffusers - turning velocity back into pressure | fluidmech only |
| [`w03_11_flow_under_sluice_gate.py`](w03_11_flow_under_sluice_gate.py) | Bernoulli with a free surface - flow under a sluice gate | fluidmech only |
| [`w03_12_rotameter.py`](w03_12_rotameter.py) | The rotameter (variable-area flow meter) | fluidmech only |
| [`w03_13_manometer_oscillation.py`](w03_13_manometer_oscillation.py) | Unsteady Bernoulli - oscillation of liquid in a U-tube | fluidmech only |
| [`w03_14_aspirator_suction.py`](w03_14_aspirator_suction.py) | Using Bernoulli suction - aspirators and sprayers | fluidmech only |
| [`w03_15_draining_a_spherical_tank.py`](w03_15_draining_a_spherical_tank.py) | Draining a tank whose cross-section varies with height | fluidmech only |
| [`w03_16_pitot_in_hot_flue_gas.py`](w03_16_pitot_in_hot_flue_gas.py) | Measuring stack-gas velocity - use the density of the ACTUAL gas | fluidmech only |

Run a script from this folder, e.g. `python w03_01_pitot_traverse.py`. Figures are saved as PNG files
in the current directory.

## Suggested student exercises

1. Replace the Lab 1 data in `w03_03` with your measurements and report Cd with uncertainty.
2. Use equal-area radial positions in `w03_01` and compare the flow rate with the trapezoidal result.
3. Find the maximum hump height in `w03_04` if the water is at 80 degC.
