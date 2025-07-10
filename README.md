# Numerical Wavetank in *Firedrake*: Two Method Implementations
This repository shares the source code for a potential-flow-based numerical wavetank (NWT) built upon Luke's variational principle (VP). Two numerical models have been established and implemented in [*Firedrake*](https://www.firedrakeproject.org/): 
- **Method 1**: Weak formulations are manually derived from the space-discretised VP and explicitly formulated in the code.
- **Method 2**: Weak formulations are generated automatically from the encoded time-discretised VP, resulting in an implicit implementation.

The NWT has been verified and validated through a series of test cases (TCs). Their source codes are shared to support reproducibility and encourage further development.

## Code Files for the Test Cases 1-4
- Main script:
    - Method 1: `3D_tank.py`
    - Method 2: `3D_tank_VP.py`
- Shared modules:
    - Test case configurations: `settings_TCx.py`
    - Simulation output management: `savings.py`
- Specific to Method 1:
    - Explicit weak formulations for SE and SV schemes: `solvers_full.py`
 
## Simulation Instructions
1. **Select a test case**
    - At the beginning of the main script, set the test case by changing: `case = 'TCx'`.
2. **Set simulation parameters**
    - Parameters for each test case are configured in `settings_TCx.py`:
      - Define the output directory by modifying the `save_path`;
      - Adjust spatial resolution via `res_x`, `res_y` and `nz` in the `domain` function; set temporal resolution and output frequency via `dt` and `dt_save` in the `set_time` function; specify the wavemaker motion in the `wavemaker` function.
3. **Output files**
    - After the simulation completes, output files will be saved to the specified directory. The expected files vary by test case: 
      - TC1/TC2: `energy.csv` containing time series of energy in the fluid domain; a series of `.npy` binary files containing 1D field data named after the time step, and `readme.txt`, which is a summary of the simulation details;
      - TC3: `checkpoints.csv` containing energy, water depths at three vertices and wavemaker-related data, `readme.txt`;
      - TC4: `energy.csv`, `probes.csv` containing numerical measurements, `readme.txt`.

## Reproduce the Figures
The numerical results can be processed and visualised with the post-processing codes provided in the folder [post-processing](post-processing).
