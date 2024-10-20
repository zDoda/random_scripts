#!/usr/bin/env python3
import PySpice.Logging.Logging as Logging
from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

logger = Logging.setup_logging()

libraries_path = find_libraries()
spice_library = SpiceLibrary(libraries_path)

circuit = Circuit('Resistor Bridge')

circuit.V('1', 'Vcc', circuit.gnd, 15@u_V)
circuit.R(1, 'Vcc', 'n1', 1@u_kΩ)
circuit.R(2, 'n1', 'n2', 2@u_kΩ)
circuit.R(3, 'n1', 'n3', 1@u_kΩ)
circuit.R(4, 'n3', circuit.gnd, 2@u_kΩ)
circuit.R(5, 'n3', 'n2', 1@u_kΩ)
circuit.R('Load', 'n2', circuit.gnd, 10@u_kΩ)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.operating_point()

for node in ('n1', 'n2', 'n3'):
    print('Voltage @ {}: {:.2f} V'.format(node, float(analysis[node])))

# To plot the result (if matplotlib is installed), uncomment the following line:
# plot(analysis['n1'], title="Node n1 Voltage")
