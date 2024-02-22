#!/bin/zsh

# Define the network to scan (e.g. "192.168.1.")
network_prefix="192.168.1."

# Use arp-scan to scan the network and grep to parse out IP addresses
for i in {1..254}; do
  ping -c 1 "$network_prefix$i" &>/dev/null && arp -n | grep "$network_prefix$i" | awk '{print $1}'
done
