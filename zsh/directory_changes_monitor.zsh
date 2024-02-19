#!/bin/zsh

MONITOR_DIR="$1"
LOG_FILE="$2"

if [[ -z "$MONITOR_DIR" || -z "$LOG_FILE" ]]; then
  echo "Usage: $0 [directory] [log_file]"
  exit 1
fi

if [[ ! -d "$MONITOR_DIR" ]]; then
  echo "Error: Directory $MONITOR_DIR does not exist."
  exit 1
fi

if [[ ! -f "$LOG_FILE" ]]; then
  touch "$LOG_FILE"
fi

function log_changes {
  echo "[$(date +"%Y-%m-%d %H:%M:%S")] $1" >> "$LOG_FILE"
}

autoload -Uz colors && colors
print "${fg_bold[green]}Monitoring${fg_no_bold[white]}: ${fg_bold[blue]}$MONITOR_DIR${fg_no_bold[white]}"
print "${fg_bold[green]}Logging to${fg_no_bold[white]}: ${fg_bold[blue]}$LOG_FILE${fg_no_bold[white]}"

inotifywait -m -e create -e delete -e move -e modify "$MONITOR_DIR" --format "%T %:e %f" --timefmt "%Y-%m-%d %H:%M:%S" |
while read DATE_TIME EVENT FILE; do
  log_changes "$DATE_TIME: $EVENT occurred on $FILE"
done
