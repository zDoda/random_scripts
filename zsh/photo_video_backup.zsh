#!/bin/zsh

# Set the source and destination directories for photos and videos
photo_source_dir="/path/to/photos/"
video_source_dir="/path/to/videos/"
backup_dir="/path/to/backup/"

# Create backup directories if they don't exist
mkdir -p "${backup_dir}photos"
mkdir -p "${backup_dir}videos"

# Function to backup photos
backup_photos() {
  echo "Starting photo backup..."
  rsync -av --progress "${photo_source_dir}" "${backup_dir}photos"
  echo "Photo backup completed."
}

# Function to backup videos
backup_videos() {
  echo "Starting video backup..."
  rsync -av --progress "${video_source_dir}" "${backup_dir}videos"
  echo "Video backup completed."
}

# Perform the backup
backup_photos
backup_videos

# Unset variables to avoid conflict if script is sourced
unset photo_source_dir
unset video_source_dir
unset backup_dir
unset -f backup_photos
unset -f backup_videos
