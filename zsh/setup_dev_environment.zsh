#!/bin/zsh

# This script will set up a new development environment by installing various tools and packages.

# Define the list of packages to be installed
packages=(
    "git"
    "vim"
    "curl"
    "htop"
    "nodejs"
    "npm"
    "python3"
    "python3-pip"
    "docker"
    "docker-compose"
)

# Update system and install packages
echo "Updating system and installing necessary packages..."
if type apt > /dev/null; then
    sudo apt update -y && sudo apt upgrade -y
    sudo apt install -y $packages
elif type brew > /dev/null; then
    brew update
    brew install $packages
elif type pacman > /dev/null; then
    sudo pacman -Syu --noconfirm
    sudo pacman -S --noconfirm $packages
else
    echo "Package manager not found. Please install packages manually."
    exit 1
fi

# Set up Git
echo "Configuring Git..."
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set up Vim
echo "Setting up Vim..."
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

# Set up Node.js environment
echo "Setting up Node.js environment..."

# Using Node Version Manager (NVM)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | zsh
source ~/.zshrc
nvm install node
nvm use node

# Set up Python environment
echo "Setting up Python environment..."
pip3 install --upgrade pip setuptools wheel

# Install Docker and start the service
echo "Setting up Docker..."
if type apt > /dev/null; then
    sudo apt remove docker docker-engine docker.io containerd runc
    sudo apt install -y apt-transport-https ca-certificates gnupg lsb-release
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io
elif type pacman > /dev/null; then
    sudo pacman -S --noconfirm docker
fi
sudo systemctl start docker
sudo systemctl enable docker

# Done
echo "Development environment setup is complete!"
