#!/bin/zsh

# Network range to scan
network_range="192.168.1.0/24"

# Scan network and list IP addresses of all devices
nmap -sn $network_range | grep 'Nmap scan report for' | awk '{ print $5 }'
