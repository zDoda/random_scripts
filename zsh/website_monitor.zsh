#!/bin/zsh

# Configuration
WEBSITE_URL="http://example.com"
ALERT_EMAIL="alert@example.com"
CHECK_INTERVAL=60 # In seconds

# Function to check the website status
check_website() {
    if ! curl -s --head $WEBSITE_URL | grep "200 OK" > /dev/null; then
        echo "Website $WEBSITE_URL seems to be down" | mail -s "Website Down Alert" $ALERT_EMAIL
    fi
}

# Main script loop
while true; do
    check_website
    sleep $CHECK_INTERVAL
done
