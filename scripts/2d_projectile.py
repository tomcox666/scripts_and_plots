import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

g = 9.81
rho = 1.225

def drag_force(v, C_d, A):
    return 0.5 * C_d * rho * A * v**2

def projectile_motion(v0, theta, phi, h0, C_d, mass):

    theta_rad = np.radians(theta)
    phi_rad = np.radians(phi)
    v0x = v0 * np.sin(theta_rad) * np.cos(phi_rad)
    v0y = v0 * np.sin(theta_rad) * np.sin(phi_rad)
    v0z = v0 * np.cos(theta_rad)

    dt = 0.01
    t = 0
    max_time = 100
    x, y, z = [], [], []

    pos = np.array([0, 0, h0])
    vel = np.array([v0x, v0y, v0z])
    
    while pos[2] >= 0 and t <= max_time:
        speed = np.linalg.norm(vel)
        F_drag = drag_force(speed, C_d, mass)

        drag_direction = -vel / speed
        acceleration = np.array([0, 0, -g]) + F_drag * drag_direction / mass

        vel += acceleration * dt
        pos += vel * dt

        x.append(pos[0])
        y.append(pos[1])
        z.append(pos[2])

        print(f"Time={t:.5f}: (x={x[-1]:.2f}, y={y[-1]:.2f}, z={z[-1]:.2f}), (velocity={vel[-1]:.2f})")

        t += dt

    return np.array(x), np.array(y), np.array(z)

def animate_trajectory(x, y, z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("Projectile Motion with Air Resistance")
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_xlim([min(x) - 5, max(x) + 5])
    ax.set_ylim([min(y) - 5, max(y) + 5])
    ax.set_zlim([0, max(z) + 5])

    line, = ax.plot([], [], [], lw=2)

    def update(num):
        line.set_data(x[:num], y[:num])
        line.set_3d_properties(z[:num])
        return line,

    ani = FuncAnimation(fig, update, frames=len(x), blit=True, interval=50)
    plt.show()

def main():
    print("Projectile Motion Simulation")
    v0 = float(input("Enter initial velocity (m/s, v > 0): "))
    theta = float(input("Enter launch angle (degrees, 0-90 degrees): "))
    phi = float(input("Enter azimuth angle (degrees, 0-360 degrees): "))
    h0 = float(input("Enter initial altitude (m, h >= 0): "))
    C_d = float(input("Enter drag coefficient (0.0 - 1.0): "))
    mass = float(input("Enter projectile mass (kg, m > 0): "))

    global A
    A = 0.01

    x, y, z = projectile_motion(v0, theta, phi, h0, C_d, mass)

    print(f"Final position: (x={x[-1]:.2f}, y={y[-1]:.2f}, z={z[-1]:.2f})")
    print(f"Total time of flight: {len(x) * 0.01:.2f} seconds")

    animate_trajectory(x, y, z)

if __name__ == "__main__":
    main()