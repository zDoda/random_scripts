#!/usr/bin/env python3
import os
import shutil
import datetime
import subprocess

# Website details - Customize these variables as per your requirement
website_directory = '/var/www/my_website'  # Path to your website directory
backup_directory = '/backups/my_website'   # Path where you want to store your backup files
number_of_backups = 5  # Number of backup archives to keep

# Create a backup
timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
archive_name = f"website_backup_{timestamp}.tar.gz"
archive_path = os.path.join(backup_directory, archive_name)

# Ensure the backup directory exists
if not os.path.exists(backup_directory):
    os.makedirs(backup_directory)

# Generate the backup using tar
subprocess.run(['tar', '-czvf', archive_path, '-C', os.path.dirname(website_directory), os.path.basename(website_directory)])

# Prune old backups, keep the recent 'number_of_backups' files
existing_backups = sorted([os.path.join(backup_directory, f) for f in os.listdir(backup_directory) if f.startswith('website_backup_') and f.endswith('.tar.gz')], key=os.path.getmtime)

while len(existing_backups) > number_of_backups:
    os.remove(existing_backups.pop(0))  # Remove the oldest backup
