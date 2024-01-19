```python
#!/bin/bash

# Set threshold values
cpu_threshold=80
memory_threshold=80

while true; do
    # Get the current CPU and memory usage
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d '.' -f 1)
    memory_usage=$(free | awk 'FNR == 2 {print $3/$2 * 100}')

    # Check if the thresholds are exceeded
    if [ $cpu_usage -gt $cpu_threshold ]; then
        echo "CPU usage is above the threshold: $cpu_usage%"
        # Add alert or action here
    fi

    if [ $memory_usage -gt $memory_threshold ]; then
        echo "Memory usage is above the threshold: $memory_usage%"
        # Add alert or action here
    fi
    
    # Wait for some time before checking again
    sleep 30
done
