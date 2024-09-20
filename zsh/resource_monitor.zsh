#!/bin/zsh

# Thresholds
CPU_THRESHOLD=90
MEM_THRESHOLD=90
DISK_THRESHOLD=90

# Get current CPU usage as a percentage
current_cpu=$(top -bn2 | grep "Cpu(s)" | tail -n 1 | awk '{print $2 + $4}')
# Get current memory usage as a percentage
current_memory=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
# Get current disk usage for the root partition as a percentage
current_disk=$(df -h / | tail -n 1 | awk '{print $5}' | tr -d '%')

# Function to check and alert if threshold is exceeded
check_usage() {
  local usage=$1
  local threshold=$2
  local resource=$3

  # If resource usage exceeds the threshold, send an alert
  if (( $(echo "$usage >= $threshold" | bc -l) )); then
    echo "Alert: $resource usage is at ${usage}%"
  fi
}

# Call the check_usage function with current usage stats and thresholds
check_usage $current_cpu $CPU_THRESHOLD "CPU"
check_usage $current_memory $MEM_THRESHOLD "Memory"
check_usage $current_disk $DISK_THRESHOLD "Disk"
