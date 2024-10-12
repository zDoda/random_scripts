#!/bin/zsh

# Configuration variables
SOURCE_DIR="/path/to/local/directory"
DEST_DIR="remoteuser@remotehost:/path/to/remote/directory"
SSH_KEY="/path/to/private/key"
RSYNC_OPTIONS="-avz --delete"

function sync_to_remote() {
    # Sync local source directory to remote destination
    rsync $RSYNC_OPTIONS -e "ssh -i $SSH_KEY" "$SOURCE_DIR" "$DEST_DIR"
}

function sync_from_remote() {
    # Sync remote source to local destination
    rsync $RSYNC_OPTIONS -e "ssh -i $SSH_KEY" "$DEST_DIR" "$SOURCE_DIR"
}

# Execute the sync functions
sync_to_remote
# sync_from_remote  # Uncomment to sync from remote to local instead
