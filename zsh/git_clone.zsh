#!/bin/zsh

# Array of git repositories to clone
repositories=(
    "git@github.com:user/repo1.git"
    "git@github.com:user/repo2.git"
    "https://github.com/user/repo3.git"
)

# Directory to clone the repositories into
clone_dir="${HOME}/cloned_repos"

# Create the directory if it doesn't exist
mkdir -p "${clone_dir}"

# Function to clone a repository
clone_repository() {
    local repo_url=$1
    local repo_name=${repo_url##*/}
    repo_name=${repo_name%%.git}

    # Check if the repository already exists
    if [[ -d "${clone_dir}/${repo_name}" ]]; then
        echo "Repository ${repo_name} already exists, skipping clone."
    else
        echo "Cloning ${repo_name} into ${clone_dir}..."
        git clone "${repo_url}" "${clone_dir}/${repo_name}"
    fi
}

# Iterate over the list of repositories and clone them
for repo in "${repositories[@]}"; do
    clone_repository "${repo}"
done

