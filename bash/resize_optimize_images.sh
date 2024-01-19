#!/bin/bash

# Check for the required command line tool 'convert' from ImageMagick
if ! command -v convert &> /dev/null; then
    echo "ImageMagick convert command could not be found"
    exit 1
fi

# Check if at least one argument is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Input directory where images are stored
input_dir=$1

# Output directory for resized and optimized images
output_dir="${input_dir}/optimized"
mkdir -p "$output_dir"

# Image size to resize to
image_width=1920

# Quality for the optimized images (scale of 1-100)
quality=85

# Loop through all .jpg and .jpeg files in the input directory
find "$input_dir" -type f \( -iname "*.jpg" -o -iname "*.jpeg" \) | while read image; do
    # Get the base name of the image file
    base_name=$(basename "$image")
    # Specify the output file name
    output_file="${output_dir}/${base_name}"

    # Resize and optimize the image using ImageMagick's 'convert'
    convert "$image" -resize "${image_width}" -strip -interlace Plane -gaussian-blur 0.05 -quality "${quality}" "$output_file"

    # Output the status
    if [ $? -eq 0 ]; then
        echo "Processed: $output_file"
    else
        echo "Failed to process: $image"
    fi
done
