#!/usr/bin/env python3

import sys
from Bio.PDB import MMCIFParser, PDBParser
from Bio.PDB.DSSP import DSSP
from Bio.PDB.Polypeptide import PPBuilder
import numpy as np

def analyze_structure(file_path):
    # Determine file format (assume .cif or .pdb)
    file_format = 'cif' if file_path.lower().endswith('.cif') else 'pdb'
    
    # Parse structure
    parser = MMCIFParser() if file_format == 'cif' else PDBParser()
    try:
        structure = parser.get_structure("structure", file_path)
    except Exception as e:
        print(f"An error occurred while parsing the structure: {e}")
        return

    # Run DSSP to get secondary structure (assumes DSSP is installed and in PATH)
    model = structure[0]  # Since structures often contain a single model, we'll just use the first
    try:
        dssp = DSSP(model, file_path)
    except Exception as e:
        print(f"An error occurred while running DSSP: {e}")
        return

    # Generate Secondary Structure Summary
    dssp_dict = dict(dssp)
    sec_struct_count = {
        'H': 0,  # Alpha helix
        'B': 0,  # Isolated beta-bridge residue
        'E': 0,  # Strand
        'G': 0,  # 3-10 helix
        'I': 0,  # Pi helix
        'T': 0,  # Turn
        'S': 0,  # Bend
        '-': 0,  # None
    }

    for key in dssp_dict:
        sec_struct_count[dssp_dict[key][2]] += 1

    # Calculate Amino Acid Composition
    ppb = PPBuilder()

    amino_acid_composition = {}
    for pp in ppb.build_peptides(structure):
        seq = str(pp.get_sequence())
        for residue in seq:
            amino_acid_composition[residue] = amino_acid_composition.get(residue, 0) + 1

    # Print report
    print(f"Structure Analysis Report for {file_path}")
    print("Secondary Structure Composition:")
    for k, v in sec_struct_count.items():
        print(f"  {k}: {v}")

    print("Amino Acid Composition:")
    for k, v in sorted(amino_acid_composition.items()):
        print(f"  {k}: {v}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyze_structure.py <structure_file>")
        sys.exit(1)

    analyze_structure(sys.argv[1])
