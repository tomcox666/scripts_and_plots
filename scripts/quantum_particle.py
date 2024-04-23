import numpy as np
import matplotlib.pyplot as plt

# Constants
hbar = 1.05457e-34  # Reduced Planck constant (J*s)
m = 9.10938e-31     # Electron mass (kg)
Lx = 1e-9            # Box length X-direction (m)
Ly = 1e-9            # Box length Y-direction (m)


# Helper Function for Wavefunction
def psi_n(x, n, Lx):
    """Calculates the wavefunction of the particle in a box for energy level n.

    Args:
        x: Position (or array of positions) 
        n: Energy level (integer, starting from 1)
        Lx: Length of the box

    Returns:
        The value (or array of values) of the wavefunction
    """
    return np.sqrt(2/Lx) * np.sin(n * np.pi * x / Lx)

def psi_2d(x, y, nx, ny, Lx, Ly):
    """Calculates the wavefunction of the particle in a 2D box.

    Args:
        x, y: Positions (or arrays of positions)
        nx, ny: Energy levels in x and y directions (integers, starting from 1)
        Lx, Ly: Length of the box in x and y directions

    Returns:
        The value (or array of values) of the wavefunction
    """
    return np.sqrt(4/(Lx * Ly)) * np.sin(nx * np.pi * x / Lx) * np.sin(ny * np.pi * y / Ly)

# Energy Levels
def energy(n):
    """Calculates the energy of the particle in the box for energy level n.

    Args:
        n: Energy level (integer, starting from 1)

    Returns:
        The energy of the particle
    """
    return (n**2 * hbar**2 * np.pi**2) / (2 * m * Lx**2)

def energy_2d(nx, ny, Lx, Ly):
    """Calculates the energy of the particle in a 2D box.

    Args:
        nx, ny: Energy levels in x and y directions (integers, starting from 1)
        Lx, Ly: Length of the box in x and y directions

    Returns:
        The energy of the particle
    """
    return (hbar**2 * np.pi**2) / (2 * m) * ((nx/Lx)**2 + (ny/Ly)**2)

# Finding Degeneracies
def find_degeneracies(max_energy):
    """Finds and groups degenerate energy states up to a given maximum energy.

    Args:
        max_energy: The maximum energy to consider (in Joules)

    Returns:
        A list of lists, where each inner list contains the (nx, ny) quantum
        number combinations that yield the same degenerate energy level.
    """
    degeneracies = []
    max_n = int(np.sqrt(2 * m * max_energy * max(Lx, Ly)**2 / (hbar**2 * np.pi**2)))  # Estimate max nx, ny values

    for nx in range(1, max_n + 1):
        for ny in range(1, max_n + 1):
            energy = energy_2d(nx, ny, Lx, Ly)
            if energy <= max_energy:
                for group in degeneracies:
                    if abs(energy - energy_2d(group[0][0], group[0][1], Lx, Ly)) < 1e-8:  # Check if already recorded
                        group.append((nx, ny))  
                        break  
                else: 
                    degeneracies.append([(nx, ny)])  # New degeneracy group

    return degeneracies

def calculate_energy_difference(n):
    """Calculates the energy difference between energy level n and n-1.

    Args:
        n: Energy level (integer, starting from 2)

    Returns:
        The energy difference.
    """
    if n <= 1:
        raise ValueError("Energy difference calculation starts from the second energy level.")
    return energy(n) - energy(n - 1)

def expected_position(n, Lx):
    """Calculates the expected value of the particle's position for a given energy level.

    Args:
        n: Energy level (integer, starting from 1)
        Lx: Length of the box

    Returns:
        The expected value of the particle's position.
    """
    x = np.linspace(0, Lx, 1000)  # Array of positions for integration
    psi = psi_n(x, n, Lx)
    probability_density = np.abs(psi)**2
    return np.trapz(x * probability_density, x)  # Integration for expected value

def visualize_particle(num_levels, plot_differences=False, plot_expected_pos=False):
    """
    Simulates the particle in a box and visualizes the probability distributions.

    Args:
        num_levels (int): Number of energy levels to visualize (must be greater than 0)
    """
    if num_levels <= 0:
        print("Error: Please enter a number of energy levels greater than 0.")
        return

    N = 1000
    x = np.linspace(0, Lx, N)

    fig, axes = plt.subplots(1, num_levels, figsize=(12, 5))  
    for n in range(1, num_levels + 1):
        psi = psi_n(x, n, Lx)
        prob_density = np.abs(psi)**2
        axes[n - 1].plot(x, prob_density, label=f'Energy Level {n}, Energy: {energy(n):.3e} J')

        if plot_expected_pos:
            expected_pos = expected_position(n, Lx)
            axes[n - 1].axvline(expected_pos, color='r', linestyle='dashed', label=f'Expected Position: {expected_pos:.2e} m')

        # Set the legend to appear below the x-axis
        axes[n - 1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.2))  # Legend below the plot area
        axes[n - 1].set_xlabel("Position (m)")
        axes[n - 1].set_ylabel("Probability Density")
        axes[n - 1].set_title(f"Energy Level {n}")

    plt.tight_layout()  # Adjust the layout for proper spacing
    plt.show()

    diff = calculate_energy_difference(n)
    print(f"Energy difference between level {n} and {n - 1}: {diff:.3e} J")
    if plot_differences:
        differences = [calculate_energy_difference(n) for n in range(2, num_levels + 1)]

        # Choose between a bar graph and line plot:
        plt.figure()  # New figure for the difference plot

        # Option 1: Bar Graph
        plt.bar(range(2, num_levels + 1), differences) 

        # Option 2: Line Plot
        #plt.plot(range(2, num_levels + 1), differences)

        plt.xlabel("Energy Level (n)")
        plt.ylabel("Energy Difference (J)")
        plt.title("Energy Differences between Consecutive Levels")
        plt.grid(True)
        plt.show()

# Visualization
def visualize_2d(nx, ny, Lx, Ly):
    """Visualizes the probability density for a particle in a 2D box 

    Args:
        nx: Energy level in x-direction (integer, starting from 1)
        ny: Energy level in y-direction (integer, starting from 1)
        Lx: Length of the box in x-direction
        Ly: Length of the box in y-direction
    """
    x = np.linspace(0, Lx, 200)
    y = np.linspace(0, Ly, 200)
    X, Y = np.meshgrid(x, y)  # Create coordinate grid

    Z = psi_2d(X, Y, nx, ny, Lx, Ly)**2  # Calculate probability density

    plt.figure(figsize=(8, 6))
    plt.contourf(X, Y, Z, levels=20, cmap='viridis') 
    plt.colorbar(label='Probability Density')
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title(f"Particle in a 2D Box - Energy Level (nx={nx}, ny={ny}), Energy: {energy_2d(nx, ny, Lx, Ly):.3e} J")
    plt.show()

def plot_degeneracies(degeneracies):
    """Plots a diagram representing the degeneracies.

    Args:
        degeneracies: A list of lists, where each inner list represents a degenerate group.
    """
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta']  # Colors for different groups
    max_degeneracy = max(len(group) for group in degeneracies)

    plt.figure(figsize=(6, 5))

    for i, group in enumerate(degeneracies):
        for j, (nx, ny) in enumerate(group):
            x_offset = (j - len(group) / 2 + 0.5) / max_degeneracy 
            plt.scatter(energy_2d(nx, ny, Lx, Ly), i + x_offset, color=colors[i % len(colors)], s=80)
            plt.text(energy_2d(nx, ny, Lx, Ly), i + x_offset, f"({nx}, {ny})", fontsize=8, ha='center')

    plt.xlabel("Energy (J)")
    plt.ylabel("Degeneracy Level")
    plt.title("Degenerate Energy Levels in a 2D Box")
    plt.show()
    
# User Input
num_levels = int(input("Enter the number of energy levels to visualize (positive integer): "))
visualize_particle(num_levels, plot_differences=True,  plot_expected_pos=True) 

nx = int(input("Enter the energy level in the x-dimension (positive integer): "))
ny = int(input("Enter the energy level in the y-dimension (positive integer): "))
visualize_2d(nx, ny, Lx, Ly)

max_search_energy = 20 * (hbar**2 * np.pi**2) / (2 * m * Lx**2)  # Search for some energy states
degeneracy_groups = find_degeneracies(max_search_energy)
plot_degeneracies(degeneracy_groups)

# Explanation (printed to the console)
print("\nExplanation:")
print("The graphs show the probability density of finding the particle at a specific position within the box.")
print("Higher probability density indicates a greater chance of finding the particle in that region.")
print("As the energy level increases, the wavefunction becomes more complex with additional nodes (points where the probability is zero).")
print("This reflects the quantization of energy in quantum mechanics, where particles can only exist in certain discrete energy states.")