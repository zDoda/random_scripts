#!/bin/zsh

# This script is designed to back up photos and videos from a specified
# source directory to a destination backup directory.

# Please change SOURCE_DIR and BACKUP_DIR to the paths of your source
# and backup directories.

SOURCE_DIR="/path/to/source/folder"
BACKUP_DIR="/path/to/backup/folder"
PHOTO_EXTENSIONS="(jpg|jpeg|png|gif)"
VIDEO_EXTENSIONS="(mov|mp4|avi|m4v)"

# Function to perform backup of photos and videos
backup_media() {
    # Create backup directory if it doesn't exist
    mkdir -p "$BACKUP_DIR"

    # Find and copy photos
    find "$SOURCE_DIR" -type f -iregex ".*\.$PHOTO_EXTENSIONS" -exec cp {} "$BACKUP_DIR" \; 

    # Find and copy videos
    find "$SOURCE_DIR" -type f -iregex ".*\.$VIDEO_EXTENSIONS" -exec cp {} "$BACKUP_DIR" \;
    
    echo "Backup of photos and videos completed."
}

# Start the backup process
backup_media
