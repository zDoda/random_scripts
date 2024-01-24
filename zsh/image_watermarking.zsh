#!/bin/zsh

# Dependencies: ImageMagick must be installed to use the convert command

# Configuration
WATERMARK_IMAGE="/path/to/watermark.png"   # Path to the watermark image
IMAGE_DIRECTORY="/path/to/images"          # Directory containing images to watermark
OUTPUT_DIRECTORY="/path/to/output"         # Directory to save watermarked images
POSITION="southeast"                       # Watermark position: northeast, northwest, southeast, southwest, center, etc.
PADDING="10x10"                            # Optional offset (e.g. "10x10" will add a 10 pixel offset to x and y)

# Create output directory if it doesn't exist
mkdir -p $OUTPUT_DIRECTORY

# Loop through all images in the directory
for IMAGE in $IMAGE_DIRECTORY/*.{jpg,jpeg,png,gif}; do
  if [ -f "$IMAGE" ]; then
    BASENAME=$(basename $IMAGE)
    # Create the watermarked version
    convert "$IMAGE" -gravity $POSITION -geometry +$PADDING -composite $WATERMARK_IMAGE "$OUTPUT_DIRECTORY/$BASENAME"
  fi
done

echo "Watermarking complete. Check output in $OUTPUT_DIRECTORY"
