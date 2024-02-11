#!/bin/zsh

# Dashboard for Server Health and Metrics

# Define the command to fetch system metrics
SYSINFO_CMD="top -l 1"

# Define the commands for various server health checks
CPU_USAGE_CMD="ps -A -o %cpu | awk '{s+=$1} END {print s "%"}'"
MEM_USAGE_CMD="vm_stat | grep 'Pages active' | awk '{print $3}' | sed 's/.$//'"
DISK_USAGE_CMD="df -h | awk '$NF=="/"{print $(NF-1)}'"
LOAD_AVERAGE_CMD="sysctl -n vm.loadavg | awk '{print $2, $3, $4}'"
NETWORK_IO_CMD="netstat -ib | awk '/en0/ {print $7, $10}'"

clear

# Display the server metrics in a simple dashboard format
while true; do
  # Clear the previous output
  clear

  # Print the headers
  echo "---- Server Health Dashboard ----"
  echo "Updated: $(date)"
  echo

  # Fetch and print the system information
  echo "System Information:"
  $SYSINFO_CMD
  echo

  # Fetch and print the CPU usage
  echo "CPU Usage:"
  CPU_USAGE=$($CPU_USAGE_CMD)
  echo "Total CPU Usage: $CPU_USAGE"
  echo

  # Fetch and print the memory usage
  echo "Memory Usage:"
  MEM_USAGE=$($MEM_USAGE_CMD)
  echo "Active Memory Usage: $MEM_USAGE bytes"
  echo

  # Fetch and print the disk usage
  echo "Disk Usage:"
  DISK_USAGE=$($DISK_USAGE_CMD)
  echo "Root Partition Usage: $DISK_USAGE"
  echo

  # Fetch and print the load average
  echo "Load Average (1, 5, 15 min):"
  LOAD_AVERAGE=$($LOAD_AVERAGE_CMD)
  echo "$LOAD_AVERAGE"
  echo

  # Fetch and print network I/O
  echo "Network I/O (in/out bytes):"
  NETWORK_IO=$($NETWORK_IO_CMD)
  echo "$NETWORK_IO"
  echo

  # Sleep for a specified time before refreshing the dashboard
  sleep 5
done
