#!/bin/zsh

# Array of network device IPs or hostnames
network_devices=("192.168.1.10" "192.168.1.11" "192.168.1.12")

# Function to sync time on a network device
sync_time() {
  local device_ip=$1
  # Replace with the actual command to synchronize time on your network device
  # For example, using ssh to execute the `ntpdate` command on the remote device:
  ssh admin@$device_ip "sudo ntpdate pool.ntp.org"
}

# Iterate over the list of network devices and sync time
for device in $network_devices; do
  echo "Synchronizing time for device $device"
  sync_time $device
done
