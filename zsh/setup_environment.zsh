#!/bin/zsh

# Update package lists
echo "Updating package lists..."
sudo apt-get update -y

# Upgrade installed packages
echo "Upgrading installed packages..."
sudo apt-get upgrade -y

# Install development tools
echo "Installing development tools..."
sudo apt-get install -y build-essential git curl

# Install code editors (VSCode as an example)
echo "Installing Visual Studio Code..."
wget -q https://go.microsoft.com/fwlink/?LinkID=760868 -O vscode.deb
sudo dpkg -i vscode.deb
sudo apt-get install -y -f # Fix any dependency issues
rm vscode.deb

# Install Node.js and npm
echo "Installing Node.js and npm..."
curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Docker
echo "Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Add the current user to the docker group
sudo usermod -aG docker $USER

# Install docker-compose
echo "Installing docker-compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone sample repositories (example)
echo "Cloning sample repositories..."
git clone https://github.com/your-repo/your-project.git

# Set up SSH keys (if applicable)
echo "Setting up SSH keys..."
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

echo "Development environment setup complete!"
