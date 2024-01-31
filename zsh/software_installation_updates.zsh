#!/bin/zsh

# Utility function to install a package using the package manager
install_package() {
    local package="$1"
    if command -v apt-get &> /dev/null; then
        sudo apt-get install -y "$package"
    elif command -v yum &> /dev/null; then
        sudo yum install -y "$package"
    elif command -v pacman &> /dev/null; then
        sudo pacman -Syu --noconfirm "$package"
    elif command -v zypper &> /dev/null; then
        sudo zypper install -y "$package"
    else
        echo "No known package manager found."
        return 1
    fi
    return 0
}

# Utility function to update the package list and upgrade all packages
update_system() {
    if command -v apt-get &> /dev/null; then
        sudo apt-get update -y && sudo apt-get upgrade -y
    elif command -v yum &> /dev/null; then
        sudo yum update -y
    elif command -v pacman &> /dev/null; then
        sudo pacman -Syu --noconfirm
    elif command -v zypper &> /dev/null; then
        sudo zypper update -y
    else
        echo "No known package manager found."
        return 1
    fi
    return 0
}

# The list of packages you wish to install
packages=(
    "git"
    "htop"
    "curl"
    # ... add more packages here
)

# Update the system first
echo "Updating system..."
update_system

# Iterate through the list of packages and install them one by one
for pkg in "${packages[@]}"; do
    echo "Installing $pkg..."
    install_package "$pkg"
done

echo "Software installation and updates have been completed."
