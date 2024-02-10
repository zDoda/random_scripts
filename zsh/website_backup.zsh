#!/bin/zsh

# Variables
backup_dir="/path/to/backup/dir"
website_dir="/path/to/website/dir"
timestamp=$(date +"%Y%m%d%H%M%S")
archive_name="website_backup_$timestamp.tar.gz"
temp_backup_file="website_temp_backup_$timestamp"

# Create backup directory if it doesn't exist
mkdir -p $backup_dir

# Create a temporary backup file with a list of files to be archived
find $website_dir -type f > $temp_backup_file

# Archive and compress the website files listed in the temporary backup file
tar -czf $backup_dir/$archive_name -T $temp_backup_file

# Remove temporary backup file
rm $temp_backup_file

# Printing the backup file path
echo "Backup archived as $backup_dir/$archive_name"
