#!/bin/zsh

# Constants
VPN_CONFIG_DIR="$HOME/vpn_configs"
OPENVPN_CMD="openvpn"

# Functions
function list_vpns() {
    echo "Available VPN configurations:"
    ls "$VPN_CONFIG_DIR"
}

function connect_vpn() {
    local config_file=$1
    sudo $OPENVPN_CMD --config "${VPN_CONFIG_DIR}/${config_file}"
}

function disconnect_vpn() {
    sudo killall openvpn
}

function print_usage() {
    echo "Usage: $0 {list|connect|disconnect} [config-file]"
}

# Check VPN configuration directory
if [[ ! -d $VPN_CONFIG_DIR ]]; then
    echo "VPN configuration directory does not exist: $VPN_CONFIG_DIR"
    exit 1
fi

# Main Program
case $1 in
    list)
        list_vpns
        ;;
    connect)
        if [[ -z $2 ]]; then
            echo "Error: No configuration file specified."
            print_usage
            exit 1
        fi
        connect_vpn $2
        ;;
    disconnect)
        disconnect_vpn
        ;;
    *)
        print_usage
        exit 1
        ;;
esac
