**Damped Harmonic Oscillator Simulation**

**Overview**
This project simulates damped harmonic oscillators, with optional coupling between multiple oscillators. The script uses the SciPy library to solve differential equations, and matplotlib to visualize the results. You can configure the oscillators and their coupling parameters using a `config.ini` file.

**Installation**
To run this script, ensure you have Python 3.x installed, along with the following packages:

NumPy
SciPy
Matplotlib
ConfigParser (usually included in Python)
You can install the required packages using pip

**Configuration**
Create a `config.ini` file in the same directory as your script. This file contains the parameters for the oscillators and the coupling between them.

**Explanation of Configuration Sections**
* [General]: Defines general simulation parameters:
* `num_oscillators`: Number of oscillators to simulate.
* `t_span_start` and t_span_end: Defines the start and end times for the simulation.
* `t_eval_points`: Number of points at which to evaluate the solution.
* [OscillatorX]: Each section (e.g., Oscillator1, Oscillator2) defines the parameters for a specific oscillator:
* `mass`: Mass of the oscillator in kilograms.
* `spring_constant`: Spring constant in newtons per meter.
* `damping_coefficient`: Damping coefficient in newton-seconds per meter.
* `initial_displacement`: Initial displacement in meters.
* `initial_velocity`: Initial velocity in meters per second.
* [Coupling]: Parameters for coupling between oscillators:
* `spring_constant`: Spring constant for coupling in newtons per meter.
* `damping_coefficient`: Damping coefficient for coupling in newton-seconds per meter.

**Usage**
Create or update your `config.ini` file with the desired parameters.
Run the Python script. It will read the configuration and simulate the oscillators accordingly.
The script will plot the position, velocity, and energy of the oscillators over time, as well as the phase space diagram.
To run the script, use the following command:

`python damped_oscillator.py`

**Notes**
Ensure that your `config.ini` file is in the same directory as your script.
If you add more oscillators, update the num_oscillators field in the [General] section accordingly, and add additional sections for each new oscillator.
This script is intended for educational and illustrative purposes, demonstrating the simulation of damped harmonic oscillators with coupling.