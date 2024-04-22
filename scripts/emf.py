import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

# Constants
k = 8.9875517923e9  # Coulomb's constant

# Ask for the number of charges
num_charges = int(input("Enter the number of point charges: "))

charges = []
for i in range(num_charges):
    # Prompt the user for position and magnitude of each charge
    x = float(input(f"Enter x-coordinate for charge {i + 1}: "))
    y = float(input(f"Enter y-coordinate for charge {i + 1}: "))
    q = float(input(f"Enter magnitude for charge {i + 1}: "))
    charges.append((x, y, q))

# Parameters for grid and plot limits
grid_size = (100, 100)  # Number of points in the x and y directions
xlim = (0, 10)  # Plot limits
ylim = (0, 10)

# Function to calculate the electric field at each grid point
def electric_field(X, Y, charges):
    E_x = np.zeros_like(X)
    E_y = np.zeros_like(Y)
    for charge_x, charge_y, q in charges:
        dx = X - charge_x
        dy = Y - charge_y
        r = np.sqrt(dx**2 + dy**2)
        r[r < 1e-6] = 1e-6  # Prevent division by zero
        E = k * q / r**3
        E_x += E * dx
        E_y += E * dy
    return E_x, E_y

# Function to calculate electric potential
def electric_potential(X, Y, charges):
    potential = np.zeros_like(X)
    for charge_x, charge_y, q in charges:
        dx = X - charge_x
        dy = Y - charge_y
        r = np.sqrt(dx**2 + dy**2)
        r[r < 1e-6] = 1e-6  # Prevent division by zero
        potential += k * q / r
    return potential

# Create the grid for calculation
X, Y = np.meshgrid(np.linspace(xlim[0], xlim[1], grid_size[0]), 
                   np.linspace(ylim[0], ylim[1], grid_size[1]))

# Calculate the electric field at each point
E_x, E_y = electric_field(X, Y, charges)

# Calculate the field strength
field_strength = np.sqrt(E_x**2 + E_y**2)

# Plot the field strength as a colormap
fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(field_strength, extent=(xlim[0], xlim[1], ylim[0], ylim[1]), 
               origin='lower', cmap='viridis', alpha=0.7, aspect='auto')

# Plot electric field lines
ax.streamplot(X, Y, E_x, E_y, density=1.5, color='k', linewidth=1)

# Plot charges with color intensity based on their magnitude
max_charge = max(abs(charge[2]) for charge in charges)  # Find the maximum charge
for charge in charges:
    intensity = abs(charge[2]) / max_charge  # Normalize intensity
    color = 'red' if charge[2] > 0 else 'blue'
    ax.scatter(charge[0], charge[1], c=color, s=70, alpha=intensity)

# Plot equipotential lines
ax.contour(X, Y, electric_potential(X, Y, charges), levels=10, colors='gray')

# Configure plot
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_title('Electric Field Simulation with Colormap')

# Create a colorbar linked to the colormap
fig.colorbar(ScalarMappable(norm=Normalize(), cmap='viridis'), ax=ax, label='Field Strength')

# Show the plot
plt.show()
