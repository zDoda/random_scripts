#!/bin/zsh

# Define local and remote directories
local_dir="/path/to/local/directory"
remote_dir="user@remotehost:/path/to/remote/directory"

# Define remote SSH options
ssh_options="-i /path/to/private/key"

# Path to the rsync command 
rsync_command=$(which rsync)

# Rsync options
rsync_options="-avz --delete"

# Perform sync from local to remote
$($rsync_command $rsync_options -e "ssh $ssh_options" $local_dir $remote_dir)

# Perform sync from remote to local
$($rsync_command $rsync_options -e "ssh $ssh_options" $remote_dir $local_dir)
