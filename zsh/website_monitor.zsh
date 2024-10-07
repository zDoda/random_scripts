#!/bin/zsh

# Website URL to monitor
WEBSITE_URL="https://example.com"

# Email for sending alert
ALERT_EMAIL="your-email@example.com"

# Function to check if a website is up
check_website() {
    if ! curl --silent --head --fail "$WEBSITE_URL" > /dev/null; then
        echo "$WEBSITE_URL appears to be down" | mail -s "$WEBSITE_URL DOWN!" $ALERT_EMAIL
        echo "Alert has been sent to $ALERT_EMAIL"
    else
        echo "$WEBSITE_URL is up and running."
    fi
}

# Infinite loop to keep the script running
while true; do
    check_website
    sleep 60 # Check every 60 seconds
done
