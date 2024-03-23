```zsh
#!/usr/bin/env zsh

# Batch Image Watermarking Script
# Requires ImageMagick to be installed

WATERMARK_IMAGE="watermark.png"  # Path to the watermark image
OUTPUT_DIR="watermarked_images"  # Output directory for watermarked images

if [[ ! -f $WATERMARK_IMAGE ]]; then
    echo "Watermark image does not exist."
    exit 1
fi

if [[ ! -d $OUTPUT_DIR ]]; then
    mkdir -p $OUTPUT_DIR
fi

for img in *.jpg *.jpeg *.png; do
    if [[ -f $img ]]; then
        output_file="${OUTPUT_DIR}/${img}"
        composite -gravity southeast -geometry +10+10 "$WATERMARK_IMAGE" "$img" "$output_file"
        echo "Watermarked image saved as $output_file"
    fi
done
