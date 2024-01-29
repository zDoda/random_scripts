#!/usr/bin/env python3

import os
from pyautocad import Autocad, APoint

def convert_dwg_to_pdf(input_file, output_file):
    autocad = Autocad(create_if_not_exists=True)
    autocad.Application.Documents.Open(input_file)

    # Assuming the active layout is to be converted
    layout = autocad.ActiveDocument.ActiveLayout

    # Set the necessary print preferences (can be customized)
    layout.ConfigName = "DWG to PDF.pc3"
    layout.PlotWithPlotStyles = True
    layout.CanonicalMediaName = "A3"

    # Plot the layout to PDF
    layout.PlotToFile(output_file)
    autocad.ActiveDocument.Close(SaveChanges=False)

def batch_convert_directory(input_dir, output_dir):
    files = os.listdir(input_dir)
    dwg_files = [file for file in files if file.lower().endswith('.dwg')]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for dwg_file in dwg_files:
        input_file_path = os.path.join(input_dir, dwg_file)
        output_file_path = os.path.join(output_dir, dwg_file.replace('.dwg', '.pdf'))
        convert_dwg_to_pdf(input_file_path, output_file_path)
        print(f"Converted: {input_file_path} to {output_file_path}")

if __name__ == "__main__":
    input_directory = "/path/to/dwg/files"
    output_directory = "/path/to/output/pdf/files"
    batch_convert_directory(input_directory, output_directory)
