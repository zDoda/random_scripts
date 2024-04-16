#!/bin/zsh

# Users to be created, one per line in the file userlist.txt
USERLIST="userlist.txt"

# Default password for new users
DEFAULT_PASSWORD="ChangeMe123!"

# Location for the log file
LOGFILE="user_creation.log"

# Function to create a user
create_user() {
  local username=$1
  local password=$2

  # Check if the user already exists
  if id "$username" &>/dev/null; then
    echo "User $username already exists, skipping..." | tee -a "$LOGFILE"
  else
    # Creating the user and setting the default password
    /usr/sbin/useradd $username && \
    echo "$username:$password" | chpasswd && \
    echo "User $username created successfully." | tee -a "$LOGFILE"
  fi
}

# Read the user list and create each user
while IFS= read -r username; do
  if [[ -n "$username" ]]; then
    create_user "$username" "$DEFAULT_PASSWORD"
  fi
done < "$USERLIST"

echo "Bulk user creation script completed." | tee -a "$LOGFILE"
