# Week 1 - Introduction to fluids and fluid properties

**Syllabus:** Development of the concept of viscosity for Newtonian and non-Newtonian fluids. Introduction to piping systems. Typical fluid parameters and their temperature dependence.

**Course learning outcomes:** CLO 1, 2

**Reading:** White, Ch. 1 (Sections 1.4-1.9). Wilkes, chapter on non-Newtonian fluids.

## Learning objectives

- Recall typical values of density and viscosity and explain the difference between dynamic and kinematic viscosity.
- Describe how liquid and gas viscosities depend on temperature and fit Andrade/VFT models.
- Analyse viscometer and rheometer data; classify fluids as Newtonian, shear-thinning, shear-thickening or yield-stress.
- Read pipe schedules and choose a line size from velocity guidelines.

## Scripts

| Script | Content | Needs |
|---|---|---|
| [`w01_01_fluid_properties_table.py`](w01_01_fluid_properties_table.py) | Typical values of fluid properties | fluidmech only |
| [`w01_02_temperature_dependence.py`](w01_02_temperature_dependence.py) | How viscosity depends on temperature | matplotlib |
| [`w01_03_viscometers.py`](w01_03_viscometers.py) | Measuring viscosity | fluidmech only |
| [`w01_04_non_newtonian_flow_curves.py`](w01_04_non_newtonian_flow_curves.py) | Non-Newtonian fluids and rheometer data | matplotlib |
| [`w01_05_piping_basics.py`](w01_05_piping_basics.py) | Introduction to piping systems | fluidmech only |
| [`w01_06_surface_tension.py`](w01_06_surface_tension.py) | Surface tension, capillarity and the Young-Laplace equation | fluidmech only |
| [`w01_07_compressibility.py`](w01_07_compressibility.py) | Compressibility - when can a fluid be treated as incompressible? | fluidmech only |
| [`w01_08_vapour_pressure_and_boiling.py`](w01_08_vapour_pressure_and_boiling.py) | Vapour pressure, boiling under vacuum and the cavitation number | fluidmech only |
| [`w01_09_viscosity_units_and_measurement.py`](w01_09_viscosity_units_and_measurement.py) | Viscosity units and kinematic viscometers | fluidmech only |
| [`w01_10_newton_law_of_viscosity_devices.py`](w01_10_newton_law_of_viscosity_devices.py) | Newton's law of viscosity in simple devices | fluidmech only |
| [`w01_11_process_gas_properties.py`](w01_11_process_gas_properties.py) | Properties of process gases at pressure | fluidmech only |
| [`w01_12_mixture_viscosity.py`](w01_12_mixture_viscosity.py) | Estimating the viscosity of a liquid mixture | fluidmech only |
| [`w01_13_shear_rates_in_equipment.py`](w01_13_shear_rates_in_equipment.py) | What shear rate does a non-Newtonian fluid 'see' in equipment? | fluidmech only |
| [`w01_14_membrane_bubble_point.py`](w01_14_membrane_bubble_point.py) | Surface tension at work - the membrane bubble-point test | fluidmech only |
| [`w01_15_temperature_and_line_losses.py`](w01_15_temperature_and_line_losses.py) | Why fluid temperature matters for a piping system | fluidmech only |

Run a script from this folder, e.g. `python w01_01_fluid_properties_table.py`. Figures are saved as PNG files
in the current directory.

## Suggested student exercises

1. Fit the Andrade equation to your own ethanol viscosity data from a handbook and report the activation energy.
2. Modify `w01_04` to add the Carreau model and discuss when a zero-shear plateau matters.
3. Size a Schedule 40 line for 60 m3/h of glycerol at 40 degC; what changes compared with water?
