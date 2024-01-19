#!/bin/bash

output_file="system_info_report-$(date +%Y%m%d).txt"

{
    echo "System Information Report - $(date)"
    echo "====================================="
    echo ""
    echo "Hostname:"
    hostname
    echo ""
    
    echo "System Date and Time:"
    date
    echo ""
    
    echo "Uptime:"
    uptime
    echo ""
    
    echo "Users Currently Logged In:"
    who
    echo ""
    
    echo "System Load Averages:"
    uptime | cut -d ',' -f 3-5
    echo ""
    
    echo "Memory Usage:"
    free -h
    echo ""
    
    echo "Disk Usage:"
    df -h
    echo ""
    
    echo "Top 5 Memory-Consuming Processes:"
    ps aux --sort=-%mem | head -n 6
    echo ""
    
    echo "Top 5 CPU-Consuming Processes:"
    ps aux --sort=-%cpu | head -n 6
    echo ""
    
    echo "Open TCP Ports:"
    netstat -plnt
    echo ""
    
    echo "System Kernel Version:"
    uname -r
    echo ""
    
    echo "Operating System Info:"
    cat /etc/*release
    echo ""

    echo "IP Addresses and Interfaces:"
    ip addr show
    echo ""

} > "$output_file"

echo "System information report saved to $output_file"
