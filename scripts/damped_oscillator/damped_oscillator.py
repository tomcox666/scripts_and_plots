import numpy as np
import matplotlib.pyplot as plt
import configparser
from scipy.integrate import solve_ivp

# Read parameters from config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# General configuration
t_span_start = float(config["General"]["t_span_start"])
t_span_end = float(config["General"]["t_span_end"])
t_span = (t_span_start, t_span_end)
t_eval_points = int(config["General"]["t_eval_points"])
t_eval = np.linspace(t_span_start, t_span_end, t_eval_points)

num_oscillators = int(config["General"]["num_oscillators"])

oscillators = []

# Read each oscillator's parameters from the config file
for i in range(num_oscillators):
    section = f"Oscillator{i+1}"
    m = float(config[section]["mass"])
    k = float(config[section]["spring_constant"])
    c = float(config[section]["damping_coefficient"])
    x0 = float(config[section]["initial_displacement"])
    v0 = float(config[section]["initial_velocity"])

    osc = {
        "m": m,
        "k": k,
        "c": c,
        "x0": x0,
        "v0": v0,
        "title": f"Oscillator {i + 1}",
    }
    oscillators.append(osc)

# Function to simulate damped harmonic oscillators
def damped_oscillator(t, y, m, k, c):
    x, v = y
    dxdt = v
    dvdt = -(k / m) * x - (c / m) * v
    return [dxdt, dvdt]

# Function to plot the position, velocity, and energy of a single oscillator
def plot_oscillator(sol, m, k, title):
    x = sol.y[0]
    v = sol.y[1]
    kinetic_energy = 0.5 * m * v**2
    potential_energy = 0.5 * k * x**2
    total_energy = kinetic_energy + potential_energy

    # Create plots for position, velocity, and energy
    fig, axs = plt.subplots(2, 2, figsize=(10, 6))
    axs[0, 0].plot(sol.t, x, label='Position', color='b')
    axs[0, 0].set_title(f'Position vs. Time ({title})')
    axs[0, 0].set_xlabel('Time (s)')
    axs[0, 0].set_ylabel('Position (m)')

    axs[0, 1].plot(sol.t, v, label='Velocity', color='r')
    axs[0, 1].set_title(f'Velocity vs. Time ({title})')
    axs[0, 1].set_xlabel('Time (s)')
    axs[0, 1].set_ylabel('Velocity (m/s)')

    axs[1, 0].plot(sol.t, kinetic_energy, label='Kinetic Energy', linestyle='--', color='g')
    axs[1, 0].plot(sol.t, potential_energy, label='Potential Energy', linestyle='-.', color='y')
    axs[1, 0].plot(sol.t, total_energy, label='Total Energy', linestyle='-', color='m')
    axs[1, 0].set_title(f'Energy vs. Time ({title})')
    axs[1, 0].set_xlabel('Time (s)')
    axs[1, 0].set_ylabel('Energy (J)')
    axs[1, 0].legend()

    # Phase space diagram
    axs[1, 1].plot(x, v, color='c')
    axs[1, 1].set_title(f'Phase Space Diagram ({title})')
    axs[1, 1].set_xlabel('Position (m)')
    axs[1, 1].set_ylabel('Velocity (m/s)')

    fig.suptitle(f'Spring-Mass System - {title}')
    plt.tight_layout()
    plt.show()

# Simulate individual oscillators and plot their behavior
for osc in oscillators:
    sol = solve_ivp(
        lambda t, y: damped_oscillator(t, y, osc["m"], osc["k"], osc["c"]),
        t_span,
        [osc["x0"], osc["v0"]],
        t_eval=t_eval,
    )
    plot_oscillator(sol, osc["m"], osc["k"], osc["title"])

# Simulate coupled oscillators if more than one oscillator exists
if len(oscillators) > 1:
    # Function to simulate coupled oscillators
    def coupled_oscillator(t, y, k_coupling, c_coupling):
        x1, v1, x2, v2 = y
        m1, k1, c1 = oscillators[0]["m"], oscillators[0]["k"], oscillators[0]["c"]
        m2, k2, c2 = oscillators[1]["m"], oscillators[1]["k"], oscillators[1]["c"]

        dx1dt = v1
        dv1dt = -(k1 / m1) * x1 - (c1 / m1) * v1 - (k_coupling / m1) * (x1 - x2) - (c_coupling / m1) * (v1 - v2)
        dx2dt = v2
        dv2dt = -(k2 / m2) * x2 - (c2 / m2) * v2 - (k_coupling / m2) * (x2 - x1) - (c_coupling / m2) * (v2 - v1)

        return [dx1dt, dv1dt, dx2dt, dv2dt]

    # Read coupling parameters from the config file
    k_coupling = float(config["Coupling"]["spring_constant"])
    c_coupling = float(config["Coupling"]["damping_coefficient"])

    # Initial conditions for the coupled system
    x1_0 = oscillators[0]["x0"]
    v1_0 = oscillators[0]["v0"]
    x2_0 = oscillators[1]["x0"]
    v2_0 = oscillators[1]["v0"]

    # Solve the differential equations for the coupled system
    sol_coupled = solve_ivp(
        lambda t, y: coupled_oscillator(t, y, k_coupling, c_coupling),
        t_span,
        [x1_0, v1_0, x2_0, v2_0],
        t_eval=t_eval,
    )

    # Plot results for the coupled oscillators
    fig, axs = plt.subplots(2, 1, figsize=(10, 6))
    axs[0].plot(sol_coupled.t, sol_coupled.y[0], label='Oscillator 1 Position', color='b')
    axs[0].plot(sol_coupled.t, sol_coupled.y[2], label='Oscillator 2 Position', color='r')
    axs[0].set_title('Position of Coupled Oscillators')
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Position (m)')
    axs[0].legend(loc='best')

    axs[1].plot(sol_coupled.t, sol_coupled.y[1], label='Oscillator 1 Velocity', color='b')
    axs[1].plot(sol_coupled.t, sol_coupled.y[3], label='Oscillator 2 Velocity', color='r')
    axs[1].set_title('Velocity of Coupled Oscillators')
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Velocity (m/s)')
    axs[1].legend(loc='best')

    plt.tight_layout()
    plt.show()