#!/usr/bin/env python3
import subprocess
import os

# Define build and deploy functions
def build():
    print("Starting build process...")
    # Add your build commands here, for example:
    # subprocess.run(["npm", "install"], check=True)
    # subprocess.run(["npm", "run", "build"], check=True)
    print("Build process completed.")

def deploy():
    print("Starting deployment process...")
    # Add your deployment commands here, for example:
    # subprocess.run(["scp", "-r", "build/", "user@server:/path/to/deploy"], check=True)
    print("Deployment process completed.")

def main():
    try:
        # First, we build the project
        build()
        
        # Then, if build succeeds, we deploy the project
        deploy()
    
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
