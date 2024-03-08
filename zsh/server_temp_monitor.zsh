#!/bin/zsh

# Define the threshold temperature
THRESHOLD=70 # Degrees Celsius, adjust as necessary

# Define log file
LOG_FILE="/var/log/server_temp.log"

# Function to get server temperature
get_server_temp() {
    # Command to get the CPU temperature.
    # This might vary based on your hardware and sensors available.
    # Make sure to replace it with the appropriate command for your system.
    typeset temp=$(sensors | grep 'Package id 0:' | awk '{print $4}' | sed 's/[^0-9.]//g')
    echo $temp
}

# Function to write to log file
write_log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Server Temperature: $1°C" >> $LOG_FILE
}

# Main logic
while true; do
    # Retrieve the current server temperature
    typeset current_temp=$(get_server_temp)
    
    # Check if the temperature exceeds the threshold
    if [[ "$current_temp" > "$THRESHOLD" ]]; then
        # Log to file if the current temperature exceeds the threshold
        write_log "$current_temp"
        # Send alert (this could be an email, SNMP trap, etc. - implement as necessary)
    fi
    
    # Wait for a minute before the next check.
    sleep 60
done
