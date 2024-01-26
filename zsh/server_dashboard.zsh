```zsh
#!/usr/bin/env zsh

# Set the refresh rate in seconds
REFRESH_RATE=5

# Clear the screen and display the dashboard on repeat
while true; do
  clear
  echo "Server Health and Metrics Dashboard"
  echo "=================================="
  echo "Timestamp: $(date)"
  echo ""

  # CPU Load
  echo "CPU Load:"
  uptime
  echo ""

  # Memory Usage
  echo "Memory Usage (free -m):"
  free -m
  echo ""

  # Disk Usage
  echo "Disk Usage (df -h):"
  df -h
  echo ""

  # Network Activity
  echo "Network Activity (netstat -tunap):"
  netstat -tunap
  echo ""

  # Top Processes
  echo "Top processes by CPU and Memory (top -b -n 1):"
  top -b -n 1 | head -15
  echo ""

  # Waiting for the next refresh
  sleep $REFRESH_RATE
done
