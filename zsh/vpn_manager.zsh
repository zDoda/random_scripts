#!/bin/zsh

VPN_CONFIG_DIR="$HOME/.vpn-configs"
VPN_CONNECTIONS_DIR="/etc/NetworkManager/system-connections"

function list_vpn() {
  echo "Available VPN configurations:"
  ls "${VPN_CONFIG_DIR}"
}

function add_vpn() {
  local config_name="$1"
  if [[ -z "$config_name" || ! -f "${VPN_CONFIG_DIR}/${config_name}" ]]; then
    echo "Usage: $0 add <config-name>"
    return 1
  fi
  sudo cp "${VPN_CONFIG_DIR}/${config_name}" "${VPN_CONNECTIONS_DIR}/${config_name}"
  chmod 600 "${VPN_CONNECTIONS_DIR}/${config_name}"
  sudo nmcli connection reload
  echo "Added VPN configuration: $config_name"
}

function delete_vpn() {
  local config_name="$1"
  if [[ -z "$config_name" ]]; then
    echo "Usage: $0 delete <config-name>"
    return 1
  fi
  if [[ ! -f "${VPN_CONNECTIONS_DIR}/${config_name}" ]]; then
    echo "VPN configuration not found: $config_name"
    return 1
  fi
  sudo rm -f "${VPN_CONNECTIONS_DIR}/${config_name}"
  sudo nmcli connection reload
  echo "Deleted VPN configuration: $config_name"
}

function connect_vpn() {
  local config_name="$1"
  if [[ -z "$config_name" ]]; then
    echo "Usage: $0 connect <config-name>"
    return 1
  fi
  sudo nmcli connection up "$config_name"
  echo "Connected to VPN: $config_name"
}

function disconnect_vpn() {
  local config_name="$1"
  if [[ -z "$config_name" ]]; then
    echo "Usage: $0 disconnect <config-name>"
    return 1
  fi
  sudo nmcli connection down "$config_name"
  echo "Disconnected from VPN: $config_name"
}

case "$1" in
  list)
    list_vpn
    ;;
  add)
    add_vpn "$2"
    ;;
  delete)
    delete_vpn "$2"
    ;;
  connect)
    connect_vpn "$2"
    ;;
  disconnect)
    disconnect_vpn "$2"
    ;;
  *)
    echo "Usage: $0 {list|add|delete|connect|disconnect} [config-name]"
    exit 1
    ;;
esac
