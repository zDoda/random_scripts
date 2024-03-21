#!/bin/zsh

LOG_FILE_PATH="/var/log/server.log"

# Check if the log file exists
if [[ ! -f $LOG_FILE_PATH ]]; then
    echo "Error: Log file does not exist at $LOG_FILE_PATH."
    exit 1
fi

# Function to analyze logs
analyze_logs() {
    local log_file=$1
    echo "Analyzing Log File: $log_file"

    # Example of what you can parse:
    # IP addresses of all clients
    echo "--- Clients IP Addresses ---"
    grep -oP '(\d{1,3}\.){3}\d{1,3}' "$log_file" | sort | uniq -c | sort -nr

    # Number of requests per endpoint
    echo "--- Requests per Endpoint ---"
    grep -oP '"GET \K[^ ]+' "$log_file" | sort | uniq -c | sort -nr

    # Response status codes
    echo "--- Response Status Codes ---"
    grep -oP 'HTTP/1.[01]" \K\d{3}' "$log_file" | sort | uniq -c | sort -nr

    # Most frequent user-agents
    echo "--- Most Frequent User-Agents ---"
    grep -oP '"\K[^"]+(?=" "Mozilla)' "$log_file" | sort | uniq -c | sort -nr
}

# Call the function with the log file path
analyze_logs $LOG_FILE_PATH
