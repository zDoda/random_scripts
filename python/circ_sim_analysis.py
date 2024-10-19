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

circuit = Circuit('Resistor Divider')

circuit.V('input', 'in', circuit.gnd, 'DC 10')
circuit.R(1, 'in', 'out', 1@u_kΩ)
circuit.R(2, 'out', circuit.gnd, 2@u_kΩ)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.operating_point()

for node in analysis.nodes.values():
    print('Node {}: {:4.1f} V'.format(str(node), float(node)))

v_out = float(analysis.nodes['out'])
print("V_out = {:.2f} V".format(v_out))
```

Make sure you have PySpice, matplotlib, and scipy installed in your environment to be able to simulate and plot circuits. You can install them using pip:
```
pip install PySpice matplotlib scipy
