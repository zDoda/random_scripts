#!/bin/zsh

# Script to automate the setup of a VPN server using OpenVPN

# Define variables
VPN_USER="vpnuser"
VPN_PASS="vpnpassword"
VPN_SERVER_IP=$(hostname -I | awk '{print $1}')
EASY_RSA_PATH="/etc/openvpn/easy-rsa"

# Install EPEL repo and update system
yum install -y epel-release
yum update -y

# Install OpenVPN and Easy-RSA
yum install -y openvpn easy-rsa

# Copy the Easy-RSA generation scripts
cp -R /usr/share/easy-rsa/ $EASY_RSA_PATH
cd $EASY_RSA_PATH

# Create vars file from template
cp vars.example vars

# Update vars with local information
sed -i 's/export KEY_COUNTRY.*/export KEY_COUNTRY="US"/' vars
sed -i 's/export KEY_PROVINCE.*/export KEY_PROVINCE="CA"/' vars
sed -i 's/export KEY_CITY.*/export KEY_CITY="SanFrancisco"/' vars
sed -i 's/export KEY_ORG.*/export KEY_ORG="MyOrganization"/' vars
sed -i 's/export KEY_EMAIL.*/export KEY_EMAIL="me@example.com"/' vars
sed -i 's/export KEY_OU.*/export KEY_OU="MyOrganizationalUnit"/' vars
sed -i 's/export KEY_NAME.*/export KEY_NAME="server"/' vars

# Clean up the environment and build the CA
./clean-all
source vars
./build-ca --batch

# Build the server certificate
./build-key-server --batch server

# Generate Diffie-Hellman parameters
./build-dh

# Move certificates and keys
cp pki/ca.crt pki/issued/server.crt pki/private/server.key pki/dh.pem /etc/openvpn/

# Server Configuration
cat > /etc/openvpn/server.conf <<EOF
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
group nobody
persist-key
persist-tun
status openvpn-status.log
verb 3
EOF

# Enable IP Forwarding
echo 'net.ipv4.ip_forward = 1' > /etc/sysctl.d/99-openvpn.conf
sysctl --system

# Configure firewall
firewall-cmd --add-service=openvpn --permanent
firewall-cmd --add-masquerade --permanent
systemctl restart firewalld

# Add a VPN user
useradd $VPN_USER
echo $VPN_USER:$VPN_PASS | chpasswd

# Start and enable the OpenVPN service
systemctl start openvpn@server
systemctl enable openvpn@server

echo "VPN setup is complete. Connect to $VPN_SERVER_IP with the username/password provided."
