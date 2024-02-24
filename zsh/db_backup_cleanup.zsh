#!/bin/zsh

# Database credentials
user="username"
password="password"
host="localhost"
db_name="database_name"

# Backup directory
backup_path="/your/backup/directory"
date=$(date +%Y-%m-%d)

# Number of days to keep directories
days_to_keep=7

# Create a backup
mysqldump --user=$user --password=$password --host=$host $db_name | gzip > "$backup_path/db-backup-$date.sql.gz"

# Cleanup old backups
find $backup_path/* -mtime +$days_to_keep -exec rm {} \;
