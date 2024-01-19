#!/bin/zsh

# Abort on any error
set -e

# Update the system
echo "Updating system..."
sudo apt-get update && sudo apt-get upgrade -y

# Install necessary packages
echo "Installing necessary packages for the VPN server..."
sudo apt-get install -y openvpn easy-rsa

# Set up the Easy-RSA variables
EASY_RSA="/etc/openvpn/easy-rsa"
PKI_DIR="$EASY_RSA/pki"
echo "Setting up Easy-RSA..."
sudo make-cadir "$EASY_RSA"
cd "$EASY_RSA"

# Customize the vars file
cat >vars <<EOF
set_var EASYRSA_REQ_COUNTRY    "US"
set_var EASYRSA_REQ_PROVINCE   "California"
set_var EASYRSA_REQ_CITY       "San Francisco"
set_var EASYRSA_REQ_ORG        "MyOrganization"
set_var EASYRSA_REQ_EMAIL      "admin@example.com"
set_var EASYRSA_REQ_OU         "MyOrganizationalUnit"
EOF

# Source the vars file, clean up any previous PKI and build the PKI
source vars
sudo ./easyrsa clean-all
echo "Building the PKI..."
sudo ./easyrsa build-ca nopass

# Generate server key and certificate
echo "Creating VPN server certificates..."
sudo ./easyrsa build-server-full server nopass

# Generate Diffie-Hellman parameters
echo "Generating Diffie-Hellman parameters..."
sudo ./easyrsa gen-dh

# Move the certificates and keys
sudo cp "$PKI_DIR/ca.crt" "$PKI_DIR/issued/server.crt" "$PKI_DIR/private/server.key" "$PKI_DIR/dh.pem" /etc/openvpn/

# Configure OpenVPN
echo "Configuring OpenVPN server..."
OPENVPN_DIR="/etc/openvpn/server"
sudo mkdir -p "$OPENVPN_DIR"

# Create a server config file
cat >/etc/openvpn/server.conf <<EOF
port 1194
proto udp
dev tun
ca ca.crt
cert server.crt
key server.key
dh dh.pem
server 10.8.0.0 255.255.255.0
ifconfig-pool-persist ipp.txt
push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 8.8.8.8"
push "dhcp-option DNS 8.8.4.4"
keepalive 10 120
cipher AES-256-CBC
user nobody
group nogroup
persist-key
persist-tun
status openvpn-status.log
verb 3
explicit-exit-notify 1
EOF

# Enable IP forwarding
echo "Enabling IP forwarding..."
sudo sysctl -w net.ipv4.ip_forward=1

# Make IP forwarding permanent
sudo sed -i '/net.ipv4.ip_forward=1/s/^#//g' /etc/sysctl.conf

# Start and enable OpenVPN service
echo "Starting OpenVPN server..."
sudo systemctl start openvpn@server
sudo systemctl enable openvpn@server

echo "VPN server setup completed."
