#!/usr/bin/env python3

import os
import subprocess
from pathlib import Path

# Configure paths to your CAD software command line utilities here
CAD_CONVERTER_PATH = "path/to/CAD/converter/executable"

def convert_cad_file(source_file, target_format):
    """
    Converts a CAD file to the given target format using command line utility.
    
    Args:
    - source_file: Path to the source CAD file.
    - target_format: Desired output format, e.g., 'DXF', 'STL', etc.
    
    Returns:
    - output_file: Path to the converted file.
    """
    source_file = Path(source_file)
    output_file = source_file.with_suffix(f'.{target_format.lower()}')

    # Setting up the conversion command
    # The command format may change based on the converter's specs
    # This is a generic example, you'll need to adjust it to match your specific CAD software's CLI
    conversion_command = [
        CAD_CONVERTER_PATH,
        "-i", str(source_file),
        "-o", str(output_file),
        "-f", target_format
    ]

    # Run the command and wait for it to finish
    subprocess.run(conversion_command, check=True)
    
    return output_file

def batch_convert_cad_files(source_dir, target_format):
    """
    Converts all CAD files in a given directory to the target format.
    
    Args:
    - source_dir: Directory containing source CAD files.
    - target_format: Desired output format.
    """
    for cad_file in Path(source_dir).glob('*'):
        if cad_file.is_file():
            try:
                output_file = convert_cad_file(cad_file, target_format)
                print(f"Converted {cad_file} to {output_file}")
            except Exception as e:
                print(f"Failed to convert {cad_file}: {e}")

def clean_up(directory, file_extension):
    """
    Deletes files with the given file extension in the specified directory.
    
    - directory: Path to the folder where files are to be deleted.
    - file_extension: Extension of files to delete.
    """
    for file in Path(directory).glob(f'*.{file_extension}'):
        try:
            file.unlink()
            print(f"Deleted {file}")
        except Exception as e:
            print(f"Failed to delete {file}: {e}")

# Example usage
if __name__ == "__main__":
    # Folder containing CAD files
    source_directory = "/path/to/cad/files"
    # Format wanted for the CAD files
    desired_format = "STL"

    # Convert all CAD files to the desired format
    batch_convert_cad_files(source_directory, desired_format)

    # Clean up old files if required
    # clean_up(source_directory, "old_extension")
