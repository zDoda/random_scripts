#!/usr/bin/env python3
import os
from PIL import Image

def add_watermark(input_image_path, output_image_path, watermark_image_path, position):
    base_image = Image.open(input_image_path)
    watermark = Image.open(watermark_image_path)
    # Assuming the watermark is transparent and its size is appropriate for the base image
    # You may need to resize or modify the watermark image to better fit your use case
    
    # calculate the position
    if position == 'bottom-right':
        x = base_image.width - watermark.width
        y = base_image.height - watermark.height
    elif position == 'bottom-left':
        x = 0
        y = base_image.height - watermark.height
    elif position == 'top-right':
        x = base_image.width - watermark.width
        y = 0
    elif position == 'top-left':
        x = 0
        y = 0
    else:
        x = (base_image.width - watermark.width) // 2
        y = (base_image.height - watermark.height) // 2

    # Applying the watermark
    transparent = Image.new('RGBA', base_image.size)
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, (x, y), mask=watermark)
    
    # If base image is not 'RGBA', convert it back to the original mode
    if base_image.mode != 'RGBA':
        transparent = transparent.convert(base_image.mode)
    
    # Save watermarked image
    transparent.save(output_image_path)

if __name__ == "__main__":
    # Example usage
    input_path = "input.jpg"
    output_path = "watermarked.jpg"
    watermark_path = "watermark.png"
    watermark_position = "bottom-right"  # Options: 'center', 'top-left', 'top-right', 'bottom-left', 'bottom-right'
    add_watermark(input_path, output_path, watermark_path, watermark_position)
