#!/bin/zsh

# This script will create user accounts from a provided list (users.txt)

# Function to create a user and set permissions
create_user_with_permissions() {
  local username=$1
  
  # Add the user (assume the use of /bin/bash as default shell)
  # -m to create the home directory if it doesn't exist
  # -s to set the default user shell
  useradd -m -s /bin/bash $username
  
  # Set permissions for the user's home directory
  # Assume the requirement is to set it to 700 (rwx only for the user)
  chmod 700 /home/$username
  
  # (Optional) Set the password for the user
  # In a real-world scenario, it would be better to use an encrypted password or prompt for password
  # For the purpose of this example, we set a default password 'defaultPassword'
  echo $username:defaultPassword | chpasswd

  # Provide feedback that the user was created
  echo "User $username created with default permissions set."
}

# Check if the script is being run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root." >&2
   exit 1
fi

# Input file with the list of users to be created
USER_FILE="users.txt"

# Check if the users file exists
if [[ -e $USER_FILE ]]; then
  while read username; do
    # Check if the user already exists
    if id "$username" &>/dev/null; then
      echo "User $username already exists. Skipping."
    else
      create_user_with_permissions $username
    fi
  done <$USER_FILE
else
  echo "File $USER_FILE not found. Please create the file with a list of usernames, one per line."
  exit 1
fi

