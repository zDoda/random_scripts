#!/bin/zsh

# Variables
website_directory="/path/to/your/website" # replace with the path to your website
backup_directory="/path/to/backup/directory" # replace with where you want your backups to go
date_format="$(date +%Y%m%d_%H%M%S)"
backup_filename="website_backup_${date_format}.tar.gz"

# Ensure the backup directory exists
mkdir -p $backup_directory

# Backup and compress the website directory
tar -czf $backup_directory/$backup_filename -C $website_directory .

# If you want to delete backups older than 30 days, uncomment the following line
# find $backup_directory -type f -name 'website_backup_*.tar.gz' -mtime +30 -delete
