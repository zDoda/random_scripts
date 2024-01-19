#!/usr/bin/env python3
import subprocess
import shutil
import os

# Configuration
repo_url = 'https://github.com/your-repo/your-project.git'
clone_folder = 'repo'
build_script = './build.sh'
deploy_script = './deploy.sh'
branch_to_deploy = 'main'

def clone_repo(url, branch, destination_folder):
    subprocess.run(['git', 'clone', '-b', branch, url, destination_folder], check=True)

def pull_latest_code(repo_folder, branch):
    subprocess.run(['git', 'checkout', branch], cwd=repo_folder, check=True)
    subprocess.run(['git', 'pull', 'origin', branch], cwd=repo_folder, check=True)

def run_script(script_path):
    subprocess.run([script_path], check=True)

def clean_up(folder):
    if os.path.isdir(folder):
        shutil.rmtree(folder)

def main():
    # Cleanup the old repo folder if exists
    clean_up(clone_folder)
    
    # Clone the repository
    print(f"Cloning the repository from {repo_url}...")
    clone_repo(repo_url, branch_to_deploy, clone_folder)
    
    # Pull the latest code
    print(f"Pulling the latest code from the {branch_to_deploy} branch...")
    pull_latest_code(clone_folder, branch_to_deploy)
    
    # Running build script
    print("Running build script...")
    run_script(os.path.join(clone_folder, build_script))
    
    # Running deployment script
    print("Running deployment script...")
    run_script(os.path.join(clone_folder, deploy_script))
    
    # Clean up cloned repo
    print("Cleaning up...")
    clean_up(clone_folder)

    print("Build and deployment processes are completed!")

if __name__ == '__main__':
    main()
