#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh

# Parameters for a hypothetical structure
num_elements = 10  # Number of elements
element_stiffness = 210e9 * (1.0e-4 / 2) / 2  # Axial stiffness of each element
element_mass = 7800 * 1.0e-4 * 2  # Mass of each element

# Generate mass and stiffness matrices for the structure
M = np.zeros((num_elements, num_elements))
K = np.zeros((num_elements, num_elements))

for i in range(num_elements):
    M[i, i] = element_mass
    K[i, i] += element_stiffness
    if i > 0:
        K[i, i - 1] -= element_stiffness
        K[i - 1, i] -= element_stiffness
        K[i - 1, i - 1] += element_stiffness

# Apply boundary conditions (fixed at both ends)
K[0, 0] *= 2
K[-1, -1] *= 2

# Perform an eigenvalue analysis
eigenvalues, eigenvectors = eigh(K, M)
natural_frequencies = np.sqrt(eigenvalues)

# Reporting
print("Natural Frequencies of the Structure:")
for i, freq in enumerate(natural_frequencies):
    print(f"Mode {i+1}: {freq:.2f} rad/s")

# Plot mode shapes
for i in range(num_elements):
    plt.figure()
    plt.plot(eigenvectors[:, i])
    plt.title(f'Mode Shape for Mode {i+1}')
    plt.xlabel('Element Number')
    plt.ylabel('Displacement')
    plt.grid(True)
    plt.show()
