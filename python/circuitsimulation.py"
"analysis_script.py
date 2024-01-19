#!/usr/bin/env python3

import PySpice.Logging.Logging as Logging
from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

logger = Logging.setup_logging()

# Load the default libraries
libraries_path = find_libraries()
spice_library = SpiceLibrary(libraries_path)

circuit = Circuit('Resistor Divider')

circuit.V('input', 'in', circuit.gnd, 'DC 10')
circuit.R(1, 'in', 'out', 1@u_kΩ)
circuit.R(2, 'out', circuit.gnd, 2@u_kΩ)

# Perform a DC operating point simulation
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.operating_point()

# Print the output node voltage
for node in (analysis['in'], analysis['out']):
    print('Node {}: {:4.1f} V'.format(str(node), float(node)))

# Perform a DC sweep simulation
voltage_divider_simulation = simulator.dc(Vinput=slice(0, 10, 0.1))

# Plot the sweep simulation results
plot(voltage_divider_simulation['in'])
plot(voltage_divider_simulation['out'])
