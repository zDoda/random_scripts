#!/bin/zsh

# Pattern to match the files to be renamed
pattern="oldpattern*"

# Prefix to add to the renamed files
prefix="new"

# Loop through files matching the pattern
for file in $pattern; do
  # Extract the base name without the pattern
  base_name=${file#$pattern}
  # Construct new file name with the prefix and the base name
  new_name="${prefix}${base_name}"
  # Rename the file
  mv -- "$file" "$new_name"
done
