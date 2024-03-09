#!/bin/zsh
# This script creates user accounts with specified permissions.

# Function to add a user
add_user_with_permissions() {
    local username=$1
    local password=$2
    local group=$3

    # Check if the group already exists, if not create it
    if ! getent group $group > /dev/null 2>&1; then
        groupadd $group
    fi

    # Create a new user with the given username, password and add to the group
    useradd -m -g $group -p $(echo $password | openssl passwd -1 -stdin) $username

    # Assign file permissions and ownership
    chmod 0750 /home/$username
    chown $username:$group /home/$username

    echo "User $username created and permissions set."
}

# Check if the script is run with root privileges
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root."
    exit 1
fi

# Main execution
# Replace the following with actual username, password, and group
# Or pass them as parameters or read them from an input source
USERNAME="newuser"
PASSWORD="password"
GROUP="users"

add_user_with_permissions $USERNAME $PASSWORD $GROUP
