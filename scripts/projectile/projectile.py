import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.animation import FuncAnimation  # For dynamic visualization
import math

# Function to generate variable wind
def wind_function(t):
    # Base wind with oscillation over time
    wind_x = 2 * np.sin(0.5 * t)
    wind_y = 1 * np.cos(0.3 * t)

    # Add random gusts
    gust = np.random.normal(0, 0.5, 2)  # Random 2D wind gusts
    wind_x += gust[0]
    wind_y += gust[1]

    return wind_x, wind_y, 0  # Assume no vertical wind

# Function for 3D projectile motion simulation with obstacles and wind
def projectile_motion_3d_with_obstacles(v0, theta, phi, g, obstacles, drag_coeff=0.5, air_density=1.2, area=0.1):
    """
    Simulates projectile motion in 3D, with optional drag and wind, and checks for collisions with obstacles.
    """
    # Convert angles to radians
    theta = np.radians(theta)
    phi = np.radians(phi)

    # Initial velocities in Cartesian coordinates
    vx = v0 * np.cos(theta) * np.cos(phi)
    vy = v0 * np.cos(theta) * np.sin(phi)
    vz = v0 * np.sin(theta)

    # Initial positions and time
    x, y, z = 0, 0, 0
    t = 0

    # Simulation step and other constants
    dt = 0.01
    mass = 1.0  # Assume mass of projectile
    time_list = []
    x_list = []
    y_list = []
    z_list = []
    wind_data = []  # Initialize wind data list

    # Calculate forces, including variable wind
    def calculate_forces(vx, vy, vz, t):
        speed = np.sqrt(vx ** 2 + vy ** 2 + vz ** 2)
        drag_magnitude = 0.5 * drag_coeff * air_density * area * speed ** 2
        drag_force = -drag_magnitude * np.array([vx, vy, vz]) / speed
        gravity_force = np.array([0, 0, -mass * g])
        wind_force = np.array(wind_function(t))

        return drag_force + gravity_force + wind_force

    # Simulation loop
    max_height = 0
    while z >= 0:
        # Calculate forces
        net_force = calculate_forces(vx, vy, vz, t)

        # Update accelerations
        ax = net_force[0] / mass
        ay = net_force[1] / mass
        az = net_force[2] / mass

        # Update velocities
        vx += ax * dt
        vy += ay * dt
        vz += az * dt

        # Update positions
        x += vx * dt
        y += vy * dt
        z += vz * dt
        t += dt

        # Update maximum height
        if z > max_height:
            max_height = z

        # Save wind data
        wind_data.append(list(wind_function(t)))

        # Store results for plotting
        time_list.append(t)
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)

        # Check for collisions with obstacles
        for obstacle in obstacles:
            ox, oy, oz, ow, oh, od = obstacle
            if (
                ox <= x <= ox + ow
                and oy <= y <= oy + oh
                and oz <= z <= oz + od
            ):
                return t, x_list, y_list, z_list, max_height, wind_data

    return t, x_list, y_list, z_list, max_height, wind_data


# Define obstacles (x, y, z, width, height, depth)
obstacles = [
    (10, 10, 10, 5, 5, 5),  # An example obstacle at (10, 10, 10) with dimensions (5, 5, 5)
    (20, 20, 5, 10, 10, 10)  # Another obstacle at (20, 20, 5) with dimensions (10, 10, 10)
]

# Input values
v0 = float(input("Enter initial velocity (m/s): "))
theta = float(input("Enter elevation angle (degrees): "))
phi = float(input("Enter azimuthal angle (degrees): "))
g = 9.81  # Gravitational acceleration

# Simulate the motion and get the results
t_final, x_list, y_list, z_list, max_height, wind_data = projectile_motion_3d_with_obstacles(v0, theta, phi, g, obstacles)

# Create the 3D plot for animation
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the trajectory and obstacles
line, = ax.plot([], [], [], 'b-', label="Projectile Trajectory")
arrows = ax.quiver(0, 0, 0, 0, 0, 0, length=0.2, normalize=True, color='g', label="Wind")

for obstacle in obstacles:
    ox, oy, oz, ow, oh, od = obstacle
    ax.bar3d(ox, oy, oz, ow, oh, od, color='red', alpha=0.5)

# Set axis labels and title
ax.set_xlabel("Distance X (m)")
ax.set_ylabel("Distance Y (m)")
ax.set_zlabel("Height Z (m)")
ax.set_title("3D Projectile Motion with Obstacles")

# Include the legend
ax.legend(loc='upper right')

# Define the animation update function
def update_animation(frame, x_list, y_list, z_list, wind_data):
    # Update the trajectory
    line.set_data(x_list[:frame], y_list[:frame])
    line.set_3d_properties(z_list[:frame])

    # Update wind arrows
    arrows.set_segments([[[x_list[frame], y_list[frame], z_list[frame]], 
                          [x_list[frame] + wind_data[frame][0], 
                           y_list[frame] + wind_data[frame][1], 
                           z_list[frame]]]])  # Line for the arrow

    return line, arrows

# Create the animation
num_frames = len(x_list)
ani = FuncAnimation(fig, update_animation, frames=num_frames, fargs=(x_list, y_list, z_list, wind_data), interval=50, blit=False)

# Display additional information
print("Total flight time:", t_final, "seconds")
print("Maximum height reached:", max_height, "meters")
print("Final wind speed:", wind_data[-1], "m/s")
print("Range in X:", x_list[-1], "m")
print("Range in Y:", y_list[-1], "m")

plt.show()