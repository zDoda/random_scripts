#!/usr/bin/env python3

import subprocess
import os

# Define the directory where your project is located.
project_dir = '/path/to/your/project'

# Define the commands for building and deploying your project.
build_command = './build.sh'  # Replace with your build command.
deploy_command = './deploy.sh'  # Replace with your deploy command.

def run_command(command, work_dir):
    """Run a shell command in a specific working directory."""
    try:
        subprocess.check_call(command, shell=True, cwd=work_dir)
        print(f"Command '{command}' executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing '{command}': {e}")

def build_project():
    """Build the project using the defined build command."""
    print("Starting the build process...")
    run_command(build_command, project_dir)

def deploy_project():
    """Deploy the project using the defined deploy command."""
    print("Starting the deployment process...")
    run_command(deploy_command, project_dir)

def main():
    # Build the project
    build_project()
    
    # Deploy the project
    deploy_project()

if __name__ == "__main__":
    main()
