#!/bin/zsh

# Define local and remote directories
local_dir="/path/to/local/dir"
remote_dir="user@remote.server:/path/to/remote/dir"
remote_backup_dir="user@remote.server:/path/to/remote/backup/dir"

# Current date for backup
current_date=$(date "+%Y-%m-%d_%H-%M-%S")

# Syncing local directory to remote server directory
rsync -avz --delete $local_dir $remote_dir

# Create a backup of the remote directory before syncing
ssh user@remote.server "cp -a $remote_dir $remote_backup_dir/backup_$current_date"

# Now, sync the local directory to remote server directory using the backup
rsync -avz --delete --backup --backup-dir=$remote_backup_dir/backup_$current_date $local_dir $remote_dir
