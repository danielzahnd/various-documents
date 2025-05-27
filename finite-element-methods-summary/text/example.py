import numpy as np
import matplotlib.pyplot as plt

# --- Parameters ---
L = 1.0           # Length of the domain (in meters)
n_elements = 6    # Number of finite elements
T = 0.3           # Final time (in seconds)
dt = 0.001        # Time step (in seconds)
k = 1.0           # Thermal conductivity (W/m K)
T_0 = 1.0         # Initial temperature (K)

# Derived quantities
n_nodes = n_elements + 1  # Number of nodes (one more than elements)
dx = L / n_elements      # Element size (length of each finite element)
n_steps = int(T / dt)    # Number of time steps based on final time and time step size

# --- Shape function derivatives for linear elements ---
# For a 2-node element on [0, dx], the derivatives of the shape functions are constant
dN_dx = np.array([[-1/dx, 1/dx]])

# --- Element Matrices (constant for uniform mesh) ---
# Element stiffness matrix (Ke) for linear elements
Ke = k * (dN_dx.T @ dN_dx) * dx  # Element stiffness matrix (2x2)

# Element mass matrix (Me) using analytical integration for linear elements
Me = (dx / 6) * np.array([[2, 1],  # Element mass matrix (2x2)
                          [1, 2]])

# --- Assembly of Global Matrices ---
# Initialize global stiffness and mass matrices with zeros
K = np.zeros((n_nodes, n_nodes))  # Global stiffness matrix
M = np.zeros((n_nodes, n_nodes))  # Global mass matrix

# Assemble the global stiffness and mass matrices
for e in range(n_elements):
    # Local-to-global mapping for each element
    idx = [e, e + 1]

    # Assemble K and M by adding the contributions from each element
    for i in range(2):
        for j in range(2):
            K[idx[i], idx[j]] += Ke[i, j]  # Add element stiffness to global K
            M[idx[i], idx[j]] += Me[i, j]  # Add element mass to global M

# --- Initial condition: u(x, 0) = sin(pi*x) ---
# Initialize the node positions (x) and the initial temperature distribution
x = np.linspace(0, L, n_nodes)  # Position of each node
q = T_0 * np.sin(np.pi * x)           # Initial temperature profile 

# Apply Dirichlet boundary conditions: u=0 at both ends (x=0 and x=L)
q[0] = 0
q[-1] = 0

# --- Time integration using Explicit Euler ---
q_all = [q.copy()]  # List to store the solution at all time steps

# Precompute M inverse (or lumped inverse for efficiency/stability)
# Lumped mass matrix: diagonal with row-sums of M
M_lumped_inv = 1 / M.sum(axis=1)

# Time-stepping loop (Explicit Euler method)
for step in range(n_steps):
    # Compute the right-hand side for the time update: r^j = -K @ q^j
    rhs = -K @ q

    # Explicit Euler update: q^{j+1} = q^j + dt * M^{-1} * (-K q^j)
    q_new = q + dt * (M_lumped_inv * rhs)

    # Enforce boundary conditions (u=0 at both ends)
    q_new[0] = 0
    q_new[-1] = 0

    # Update the solution and store it
    q = q_new
    q_all.append(q.copy())  # Append the solution at the current time step

# --- Plotting ---
from matplotlib import cm

q_all = np.array(q_all)  # Convert the list of solutions into a numpy array

# Sample 5 time indices evenly spaced through the time steps
time_indices = np.linspace(0, n_steps, 5, dtype=int)  # Choose 5 time indices
time_values = np.linspace(0, T, n_steps + 1)[time_indices]  # Corresponding time values

# Plot the temperature profile at each selected time step
plt.figure(figsize=(8, 4))  # Set the figure size

for idx, t_idx in enumerate(time_indices):
    plt.plot(x, q_all[t_idx], label=f"$t$ = {time_values[idx]:.3f} s")  # Plot each time step

# Label the axes
plt.xlabel("Distance $x$ [m]")
plt.ylabel("Temperature $T(x,t)$ [K]")

# Highlight the nodes with red markers
plt.scatter(x, np.zeros_like(x), color='red', zorder=5, label='Nodes')

# Add legend and grid
plt.legend()
plt.grid(True)

# Adjust layout and display the plot
plt.tight_layout()
plt.savefig('resultexampletimeint.pdf')
plt.show()