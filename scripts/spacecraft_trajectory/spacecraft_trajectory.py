import configparser
import numpy as np
import astropy.units as u
from astropy.coordinates import get_body_barycentric, CartesianRepresentation
from astropy.time import Time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the configuration file
config = configparser.ConfigParser()
config.read("config.ini")

# Read parameters from the config file
planet = config["DEFAULT"]["planet"]
mu = float(config["DEFAULT"]["mu"])
t0 = float(config["DEFAULT"]["initial_time"])  # Initial time in Unix time
tf = float(config["DEFAULT"]["final_time"])  # Final time in Unix time
dt = float(config["DEFAULT"]["delta_t"]) * u.s  # Delta t with proper units

# Initialize position and velocity
r0 = np.array([float(config["SPACECRAFT"]["initial_x"]), 
               float(config["SPACECRAFT"]["initial_y"]), 
               float(config["SPACECRAFT"]["initial_z"])]) * u.km

v0 = np.array([float(config["SPACECRAFT"]["initial_vx"]), 
               float(config["SPACECRAFT"]["initial_vy"]), 
               float(config["SPACECRAFT"]["initial_vz"])]) * u.km / u.s

# Initialize time
t = Time(t0, format="unix", scale="utc")

# Array for positions, velocities, and times
r_array = [r0.value]  # Values are extracted to avoid unit mismatches
v_array = [v0.value]  # Values are extracted to avoid unit mismatches
times = [t.unix]  # Unix time in seconds

# Function for gravitational acceleration
def gravitational_acceleration(position, mu):
    r_magnitude = np.linalg.norm(position.value)  # This must be without units
    return -mu * (position / r_magnitude**3)

# Flyby condition (altitude in km)
flyby_altitude = 1000.0 * u.km  # Properly setting units

# Simulation loop
while t.unix < tf:
    # Calculate gravitational acceleration
    a_grav = gravitational_acceleration(r0, mu)  # Output should be in km/s^2
    
    # Update position and velocity with Euler's method
    r0 = r0 + (v0 * dt)  # This should result in km
    v0 = v0 + (a_grav * dt)  # This should result in km/s
    
    # Store new position and velocity (without units)
    r_array.append(r0.value)  # Using .value to avoid unit errors
    v_array.append(v0.value)  # Using .value to avoid unit errors
    
    # Update time
    t += dt
    
    times.append(t.unix)  # Keep times in Unix seconds

# Convert to numpy arrays for plotting
r_array = np.array(r_array)
v_array = np.array(v_array)
times = np.array(times)

# Plot the trajectory
fig = plt.figure(figsize=(10, 8))
ax = plt.axes(projection="3d")

# Plot the Earth
earth_radius = 6371.0  # Earth radius in km
earth_pos = get_body_barycentric("earth", times).represent_as(CartesianRepresentation).to(u.km).value
ax.scatter(earth_pos[:, 0], earth_pos[:, 1], earth_pos[:, 2], c="k", s=earth_radius**2/100, label="Earth")

# Plot spacecraft trajectory
ax.plot(r_array[:, 0], r_array[:, 1], r_array[:, 2], c="r", label="Spacecraft Trajectory")

# Set axis labels and legend
ax.set_xlabel("X (km)")
ax.set_ylabel("Y (km)")
ax.set_zlabel("Z (km)")
ax.legend()
plt.show()
