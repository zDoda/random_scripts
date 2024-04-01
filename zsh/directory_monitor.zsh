#!/bin/zsh
MONITORED_DIR="/path/to/your/directory"
LOGFILE="/path/to/your/logfile.log"

# Check if the directory exists
if [[ ! -d "$MONITORED_DIR" ]]; then
  echo "Error: Monitored directory does not exist."
  exit 1
fi

# Function to write to log with timestamp
write_log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S'): $1" >> "$LOGFILE"
}

# Initial scan of directory
declare -A file_list
for file in "$MONITORED_DIR"/*(DN); do
  file_list[$file]=$(md5sum "$file" | cut -d ' ' -f1)
done

write_log "Monitoring started on directory: $MONITORED_DIR"

# Monitoring loop
while true; do
  for file in "$MONITORED_DIR"/*(DN); do
    if [[ ! ${file_list[$file]} ]]; then
      # New file detected
      file_list[$file]=$(md5sum "$file" | cut -d ' ' -f1)
      write_log "File added: $file"
    else
      # Check if file has been modified
      current_md5=$(md5sum "$file" | cut -d ' ' -f1)
      if [[ ${file_list[$file]} != $current_md5 ]]; then
        file_list[$file]=$current_md5
        write_log "File modified: $file"
      fi
    fi
  done

  # Check for deleted files
  for file in "${(@k)file_list}"; do
    if [[ ! -a $file ]]; then
      unset file_list[$file]
      write_log "File deleted: $file"
    fi
  done

  # Wait before rechecking
  sleep 5
done
