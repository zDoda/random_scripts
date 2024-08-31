#!/bin/zsh

# Define cleanup function
function cleanup() {
    # List of directories to clean
    local dirs_to_clean=("/tmp/*" "$HOME/.cache/*" "/var/tmp/*")

    # Loop through directories and remove files and directories
    for dir in $dirs_to_clean; do
        if [[ -d $dir ]]; then
            # Use rm -rf to force remove files and directories recursively
            rm -rf "$dir"
        else
            echo "Directory $dir does not exist or cannot be cleaned."
        fi
    done

    echo "Cleanup of temporary files and cache has been completed."
}

# Call the cleanup function
cleanup
