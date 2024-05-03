#!/usr/bin/env python3

import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

class Circuit:
    def __init__(self):
        # Initialize empty lists to keep track of components and nodes
        self.components = []
        self.nodes = set()

    def add_resistor(self, name, n1, n2, value):
        self.components.append(('resistor', name, n1, n2, value))
        self.nodes.update([n1, n2])

    def add_capacitor(self, name, n1, n2, value):
        self.components.append(('capacitor', name, n1, n2, value))
        self.nodes.update([n1, n2])

    def add_inductor(self, name, n1, n2, value):
        self.components.append(('inductor', name, n1, n2, value))
        self.nodes.update([n1, n2])

    def add_voltage_source(self, name, n1, n2, amplitude, frequency, phase):
        self.components.append(('vsource', name, n1, n2, amplitude, frequency, phase))
        self.nodes.update([n1, n2])

    def solve(self):
        # Number of voltage sources and nodes
        V = sum(1 for c in self.components if c[0] == 'vsource')
        N = len(self.nodes) - 1  # GND node (assumed to be named '0') is excluded
        M = V + N 

        # Initializing the system of equations
        A = np.zeros((M, M))
        z = np.zeros(M)

        # Maps node names to matrix indices
        node_to_index = {node: i for i, node in enumerate(self.nodes if node != '0')}

        for component in self.components:
            comp_type, name, n1, n2, value = component[:5]
            i = node_to_index.get(n1, -1)
            j = node_to_index.get(n2, -1)

            # Resistors contribute to the conductance matrix
            if comp_type == 'resistor':
                g = 1.0 / value
                if i >= 0: A[i,i] += g
                if j >= 0: A[j,j] += g
                if i >= 0 and j >= 0:
                    A[i,j] -= g
                    A[j,i] -= g
            # Voltage sources contribute to the right-hand side
            elif comp_type == 'vsource':
                index = N + component[5]  # Index for this voltage source in A matrix
                v = value
                if i >= 0:
                    A[index, i] = 1
                    A[i, index] = 1
                if j >= 0:
                    A[index, j] = -1
                    A[j, index] = -1
                z[index] = v

        # Solve the system of equations
        x = np.linalg.solve(A, z)
        voltages = {node: (x[i] if node != '0' else 0.0) for node, i in node_to_index.items()}
        voltages['0'] = 0.0
        return voltages

# Example usage of the Circuit class:
if __name__ == '__main__':
    # Create a circuit
    circuit = Circuit()

    # Add components
    circuit.add_resistor('R1', '1', '0', 1000)  # Resistor R1 between node 1 and GND with 1k ohm
    circuit.add_resistor('R2', '1', '2', 2000)  # Resistor R2 between node 1 and 2 with 2k ohm
    circuit.add_voltage_source('V1', '0', '1', 5, 0, 0)  # 5V DC source between GND and node 1

    # Solve the circuit
    voltages = circuit.solve()

    # Print the results
    for node, voltage in voltages.items():
        print(f"Voltage at node {node}: {voltage:.2f} V"