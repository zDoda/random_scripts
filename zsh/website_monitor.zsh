#!/bin/zsh

# Variables
URL="http://example.com" # The URL of the website you want to monitor
ALERT_EMAIL="user@example.com" # The email address where alerts should be sent
LOGFILE="website_uptime.log" # Log file for storing the uptime status

# Function to check website status
check_website_status() {
  # Send a http request and get just the response code
  local status=$(curl -o /dev/null -s -w "%{http_code}\n" $URL)

  # Website is up
  if [ "$status" -eq 200 ]; then
    echo "$(date) $URL is UP." >> $LOGFILE
  else
    # Website is down, send an alert email
    echo "Subject: Alert! $URL is DOWN" | sendmail $ALERT_EMAIL
    echo "$(date) ERROR: $URL is DOWN." >> $LOGFILE
  fi
}

# Infinite loop to check the website status every minute
while true
do
  check_website_status
  sleep 60 # Wait for 60 seconds before the next check
done
