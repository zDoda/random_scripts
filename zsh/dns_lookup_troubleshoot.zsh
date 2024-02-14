#!/bin/zsh

# Function to perform DNS lookup and troubleshooting
function dns_lookup_and_troubleshoot() {
  local domain=$1

  if [[ -z "$domain" ]]; then
    echo "Usage: dns_lookup_and_troubleshoot <domain>"
    return 1
  fi

  # Perform a DNS lookup
  echo "Resolving DNS for $domain..."
  if ! host $domain; then
    echo "DNS resolution failed for $domain."
    return 2
  fi

  # Check for common IP addresses
  echo "Checking for common IP addresses..."
  local ip_addresses=$(dig +short $domain)
  for ip in ${ip_addresses}; do
    if [[ ${ip} == "127.0.0.1" || ${ip} == "::1" ]]; then
      echo "Warning: $domain resolves to a loopback address ($ip)."
    fi
  done

  # Check reverse DNS
  echo "Performing reverse DNS checks..."
  for ip in ${ip_addresses}; do
    if ! host $ip; then
      echo "Reverse DNS lookup failed for $ip."
    fi
  done

  # Perform traceroute to diagnose network path
  echo "Tracing network path to $domain..."
  traceroute $domain

  # Check for DNS propagation using Google's and Cloudflare's public DNS servers
  echo "Checking DNS propagation with public DNS servers..."
  for ns in 8.8.8.8 8.8.4.4 1.1.1.1; do
    echo "Querying $ns for $domain..."
    dig @$ns $domain +short
  done

  echo "DNS lookup and troubleshooting for $domain completed."
}

# Call the function with a domain provided as the first script argument
dns_lookup_and_troubleshoot "$1"
