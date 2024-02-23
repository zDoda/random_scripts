#!/bin/zsh

# Set the pattern and prefix variables
pattern="*.jpg"
prefix="photo_"

# Loop through all the files matching the pattern
for file in $pattern; do
    # Extract the basename without the extension
    base=${file%.*}
    # Rename the file with the new prefix and original extension
    mv -- "$file" "${prefix}${base}.jpg"
done
