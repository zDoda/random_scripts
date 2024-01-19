#!/bin/bash

# Loop through all files in the current directory
for file in *\ *; do
    # Replace spaces with underscores in the filename
    newname=$(echo "$file" | tr ' ' '_')

    # Rename the file
    mv "$file" "$newname"
done

