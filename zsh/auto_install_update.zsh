#!/bin/zsh

# Define an array of software to install (replace with your actual software packages)
declare -a software_packages=("package1" "package2" "package3")

# Update system
echo "Updating system..."
sudo apt-get update -y
sudo apt-get upgrade -y

# Install software
for package in "${software_packages[@]}"; do
    echo "Installing $package..."
    sudo apt-get install -y $package
done

# Clean up
echo "Cleaning up..."
sudo apt-get autoremove -y
sudo apt-get autoclean -y

echo "Software installation and updates completed!"
