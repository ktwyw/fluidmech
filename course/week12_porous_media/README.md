# Week 12 - Flow through porous media

**Syllabus:** Pressure drop in packed beds (Kozeny-Carman) and in filters and membranes (Darcy's law).

**Course learning outcomes:** CLO 2, 3, 4, 5  |  **Assessment:** HW-6

**Reading:** McCabe, Smith & Harriott: flow past immersed bodies/packed beds and fluidisation; filtration.

## Learning objectives

- Apply Darcy's law and determine permeability from test data.
- Compute packed-bed pressure drop with Kozeny-Carman, Burke-Plummer and Ergun.
- Predict minimum fluidisation velocity and the fluidised-bed pressure drop.
- Analyse cake filtration data and membrane flux with the resistance-in-series model.

## Scripts

| Script | Content | Needs |
|---|---|---|
| [`w12_01_darcy_permeameter.py`](w12_01_darcy_permeameter.py) | Darcy's law and permeability | fluidmech only |
| [`w12_02_packed_bed_pressure_drop.py`](w12_02_packed_bed_pressure_drop.py) | Pressure drop through a packed catalyst bed | fluidmech only |
| [`w12_03_fluidization.py`](w12_03_fluidization.py) | From packed bed to fluidised bed | matplotlib |
| [`w12_04_cake_filtration.py`](w12_04_cake_filtration.py) | Constant-pressure cake filtration | fluidmech only |
| [`w12_05_membrane_filtration.py`](w12_05_membrane_filtration.py) | Membranes - Darcy's law at the smallest scale | fluidmech only |
| [`w12_06_particle_size_and_sauter_mean.py`](w12_06_particle_size_and_sauter_mean.py) | Which particle diameter goes into the Ergun equation? | fluidmech only |
| [`w12_07_filter_cycle_optimisation.py`](w12_07_filter_cycle_optimisation.py) | The optimum filtration cycle | fluidmech only |
| [`w12_08_compressible_cake.py`](w12_08_compressible_cake.py) | Compressible filter cakes | fluidmech only |
| [`w12_09_well_drawdown_thiem.py`](w12_09_well_drawdown_thiem.py) | Radial Darcy flow to a well (Thiem equation) | fluidmech only |
| [`w12_10_liquid_fluidization_backwash.py`](w12_10_liquid_fluidization_backwash.py) | Expanding a sand filter bed by backwashing (liquid fluidisation) | fluidmech only |
| [`w12_11_constant_rate_filtration.py`](w12_11_constant_rate_filtration.py) | Constant-rate filtration - the pressure rises as the cake grows | fluidmech only |
| [`w12_12_sand_filter_headloss.py`](w12_12_sand_filter_headloss.py) | Clean-bed head loss of a rapid sand filter (water treatment) | fluidmech only |
| [`w12_13_concentration_polarisation.py`](w12_13_concentration_polarisation.py) | Concentration polarisation in reverse osmosis | fluidmech only |
| [`w12_14_seepage_under_a_dam.py`](w12_14_seepage_under_a_dam.py) | Seepage under a dam - Darcy flow and the Laplace equation | numpy |
| [`w12_15_cake_washing.py`](w12_15_cake_washing.py) | Washing the filter cake | fluidmech only |

Run a script from this folder, e.g. `python w12_01_darcy_permeameter.py`. Figures are saved as PNG files
in the current directory.

## Suggested student exercises

1. Measure alpha at two pressures and estimate the cake compressibility index s (alpha = alpha0 dp^s).
2. Find the particle size that halves the bed pressure drop in `w12_02` and report the surface-area penalty.
3. Size the membrane area of a brackish-water RO plant (3 g/L) with `w12_05`.
