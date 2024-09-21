#!/bin/zsh

# Define the IP range for the VPN
VPN_SUBNET="10.8.0.0/24"

# Install necessary packages
sudo apt update -y
sudo apt install -y openvpn easy-rsa

# Make the Easy-RSA files available in an easy-to-use directory
make-cadir ~/openvpn-ca
pushd ~/openvpn-ca
source vars

# Clean previous keys and build CA
./clean-all
./build-ca --batch

# Create the server certificate, key, and encryption files
./build-key-server --batch server
./build-dh
openvpn --genkey --secret keys/ta.key

# Move the server credentials
sudo cp -r keys/{ca.crt,ca.key,server.crt,server.key,ta.key,dh2048.pem} /etc/openvpn

# Generate server configuration
cat > /etc/openvpn/server.conf <<EOF
port 1194
proto udp
dev tun
ca ca.crt
cert server.crt
key server.key
dh dh2048.pem
auth SHA512
tls-auth ta.key 0
topology subnet
server $VPN_SUBNET
ifconfig-pool-persist ipp.txt
push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 8.8.8.8"
push "dhcp-option DNS 8.8.4.4"
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
sudo sh -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'

# Make IP forwarding permanent
sudo sed -i '/net.ipv4.ip_forward=1/s/^#//g' /etc/sysctl.conf

# Configure UFW to allow traffic
VPN_PUBLIC_INTERFACE=$(ip -o -4 route show to default | awk '{print $5}')
sudo ufw allow 1194/udp
sudo ufw allow OpenSSH
sudo sed -i '1 a *nat\n:POSTROUTING ACCEPT [0:0]\n-A POSTROUTING -s '$VPN_SUBNET' -o '$VPN_PUBLIC_INTERFACE' -j MASQUERADE\nCOMMIT\n' /etc/ufw/before.rules
sudo ufw enable

# Start the VPN server
sudo systemctl start openvpn@server
sudo systemctl enable openvpn@server

popd

# Output completion message
echo "VPN server setup is complete."
