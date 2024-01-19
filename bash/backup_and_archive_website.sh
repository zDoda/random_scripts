#!/bin/bash

# Define website directory
WEBSITE_DIR=/var/www/html

# Define backup directory
BACKUP_DIR=/backup

# Create directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Archive the website directory
tar -cvzf $BACKUP_DIR/website_$(date +"%Y%m%d").tar.gz $WEBSITE_DIR
