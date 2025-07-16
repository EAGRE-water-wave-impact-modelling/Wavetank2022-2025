# Numerical Wavetank in *Firedrake*: Two Method Implementations
This repository shares the source code for a potential-flow-based numerical wavetank (NWT) built upon Luke's variational principle (VP). Two numerical models have been established and implemented in [*Firedrake*](https://www.firedrakeproject.org/): 
- **Method 1**: Weak formulations are manually derived from the space-discretised VP and explicitly formulated in the code.
- **Method 2**: Weak formulations are generated automatically from the encoded time-discretised VP, resulting in an implicit implementation.

The NWT has been verified and validated through a series of test cases (TCs). Their source codes are shared to support reproducibility and encourage further development.

## Code Files for the Test Cases 1-4
- **Method 1** (Folder [TC-SV](TC-SV)):
    - `3D_tank.py`: main script, with time variables in wavemaker-related functions replaced by *Firedrake* `Constant` objects;
    - `settings_TCx.py`: test case configuration file, where `Constant` objects are used when defining wavemaker-related functions;
    - `savings.py`: simulation output management;
    - `solvers_full.py`: explicit weak formulations for the SE and SV schemes.
- **Method 2** (Folder [TC-MMP](TC-MMP)):
    - `3D_tank_VP.py`: main script[^1];
    - `settings_TCx.py`: test case configuration file;
    - `savings.py`: simulation output management.
- The folder [202002](202002) contains experimental data for TC4, including sampled wavemaker input and probe measurements.

[^1]: Updating `t` using `Constant` unfortunately caused a `segmentation fault` (as of July 2025).

## Simulation Instructions
1. **Select a test case**
    - At the beginning of the main script, set the test case by changing: `case = 'TCx'`.
2. **Set simulation parameters**
    - Parameters for each test case are configured in `settings_TCx.py`:
      - Set the time-stepping scheme via `scheme`: `SE`/`SV` for Method 1, `MMP` for Method 2;
      - Define the output directory by modifying the `save_path`;
      - Adjust spatial resolution via `res_x`, `res_y` and `nz` in the `domain` function; set temporal resolution and output frequency via `dt` and `dt_save` in the `set_time` function; specify the wavemaker motion in the `wavemaker` function.
3. **Output files**
    - After the simulation completes, output files will be saved to the specified directory. The expected files vary by test case: 
      - TC1/TC2: `energy.csv` containing time series of energy in the fluid domain; a series of `.npy` binary files containing 1D field data named after the time step, and `readme.txt`, which is a summary of the simulation details;
      - TC3: `checkpoints.csv` containing energy, water depths at three vertices and wavemaker-related data, `readme.txt`;
      - TC4: `energy.csv`, `probes.csv` containing numerical measurements, `readme.txt`.

## Reproducing the Figures
The numerical results can be processed and visualised using the post-processing scripts provided in the folder [post-processing](post-processing). The table below summarises the scripts used to reproduce each figure.

**Note**: You may need to adjust the `data_path` in each script to match your chosen output directory.

| Test Case| Figure No. | Data Sources | Post-Processing Script(s)  |
|  :----:  |  :----:    |    :----:    |      :----:           |
|   TC1    |   Fig.3    |  `energy.csv`, `.npy` field data files | `pp_SWS_TC1VP.py` |
|   TC2    |   Fig.4    |  `.npy` field data files | Fig.4(a),(b): `pp-TC1-convergence-dx.py`<br> Fig.4(c),(d): `pp-TC1-convergence-nz.py`<br> Fig.4(e),(f): `pp-TC1-convergence-dt.py`  |
|   TC2    |   Fig.5, Fig.6    |  `.npy` field data files |  `pp-TC1-advanced-convergence.py` |
|   TC3    |   Fig.7, Fig.8 |  `checkpoints.csv` | `pp_energy_figs_TC3VP.py` |
|   TC4    |   Fig.10    |  `probes.csv`, folder `202002` | `pp_wavemaker_TC4VP.py`  |
|   TC4    |   Fig.12   |  `probes.csv`, folder `202002` | `pp_probes_TC4VP.py`  |
|   TC4    |   Fig.13   |  `probes.csv`, folder `202002` | `FFT_202002.m`  |

