#!/bin/zsh

# Threshold for system load above which services should be stopped
# and below which services should be started
LOAD_THRESHOLD=5.0

# Array of service names to be managed
SERVICES=("httpd" "mysql" "ssh")

# Function to get the current system load
get_system_load() {
  echo $(uptime | awk -F'[a-z]:' '{ print $2 }' | cut -d ',' -f 1)
}

# Function to start the services
start_services() {
  for service in $SERVICES; do
    sudo systemctl start $service
  done
}

# Function to stop the services
stop_services() {
  for service in $SERVICES; do
    sudo systemctl stop $service
  done
}

# Main script logic
current_load=$(get_system_load)
if (( $(echo "$current_load < $LOAD_THRESHOLD" | bc -l) )); then
  # If the system load is below the threshold, start services
  start_services
else
  # If the system load is above or equal to the threshold, stop services
  stop_services
fi
