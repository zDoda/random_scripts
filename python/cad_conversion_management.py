#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

# Define the path where the CAD files are stored
cad_files_path = Path('/path/to/cad/files')
# Define the output path where the converted files will be stored
output_path = Path('/path/to/converted/files')

# Specify the conversion tool command line
conversion_tool = 'your_conversion_tool_command_line'
# Specify the file extension of the CAD files and the desired output format
cad_extension = '.dwg'
output_extension = '.pdf'

# Create the output directory if not exists
os.makedirs(output_path, exist_ok=True)

# Convert each CAD file in the directory to the desired output format
for cad_file_path in cad_files_path.glob(f'*{cad_extension}'):
    # Define output file path with the same base name but with the new extension
    output_file_path = output_path / cad_file_path.with_suffix(output_extension).name
    # Build the conversion command
    command = f'{conversion_tool} {cad_file_path} {output_file_path}'
    # Execute the command
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        # Log an error if the conversion fails
        print(f'Error converting {cad_file_path}: {result.stderr}')
    else:
        # Log success message
        print(f'Successfully converted {cad_file_path} to {output_file_path}')

# You would need to replace 'your_conversion_tool_command_line' with the actual command line of the CAD conversion tool you intend to use.
