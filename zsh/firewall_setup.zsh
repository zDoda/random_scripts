#!/bin/zsh

# Ensure the script is run as root
if (( $EUID != 0 )); then
   echo "Please run this script as root."
   exit 1
fi

# Set default policies to deny all incoming traffic and allow all outgoing
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow all traffic on the loopback interface
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established and related incoming connections
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Add additional rules below this line
# e.g., to open port 22 for SSH, you would use:
# iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Saving the rules so they persist on reboot.
iptables-save > /etc/iptables/rules.v4

# Repeat similar steps for IPv6 if necessary
ip6tables -P INPUT DROP
ip6tables -P FORWARD DROP
ip6tables -P OUTPUT ACCEPT

# Allow all traffic on the loopback interface for IPv6
ip6tables -A INPUT -i lo -j ACCEPT
ip6tables -A OUTPUT -o lo -j ACCEPT

# Allow established and related incoming IPv6 connections
ip6tables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Save the ip6tables rules
ip6tables-save > /etc/iptables/rules.v6

# Ensure iptables rules are reloaded on boot
cat > /etc/systemd/system/iptables-persistent.service <<EOS
[Unit]
Description=Packet Filtering Framework
Before=network-pre.target
Wants=network-pre.target

[Service]
Type=oneshot
ExecStart=/sbin/iptables-restore /etc/iptables/rules.v4
ExecStart=/sbin/ip6tables-restore /etc/iptables/rules.v6
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOS

# Enable iptables persistent service
systemctl enable iptables-persistent.service

# Start iptables & ip6tables services
systemctl start iptables-persistent.service

echo "Firewall setup complete."
