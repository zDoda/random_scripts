#!/bin/zsh

# Script to monitor and report server temperature

# Configuration variables
LOG_FILE="/var/log/server_temperature.log"
THRESHOLD=75 # Temperature threshold in Celsius

# Function to get server temperature
# For illustration, we'll assume the server temperature can be
# retrieved from a sensor at /sys/class/thermal/thermal_zone0/temp
get_server_temperature() {
  local temp=$(cat /sys/class/thermal/thermal_zone0/temp)
  echo $((temp / 1000)) # Convert to Celsius
}

# Function to log temperature
log_temperature() {
  local temp=$1
  echo "$(date) - Current Temperature: ${temp}°C" | tee -a "$LOG_FILE"
}

# Function to check if temperature exceeds the threshold
check_threshold() {
  local temp=$1
  if [[ $temp -ge $THRESHOLD ]]; then
    # Log and possibly send alert/notification
    echo "$(date) - High Temperature Alert: ${temp}°C" | tee -a "$LOG_FILE"
    
    # Sending alert or email could be done here
    # Example:
    # mail -s "High Temperature Alert" admin@localhost <<< "Current server temperature: ${temp}°C"
  fi
}

# Main monitoring loop
while true; do
  temperature=$(get_server_temperature)
  log_temperature $temperature
  check_threshold $temperature
  sleep 60 # Check every minute
done
