#!/usr/bin/env python3

import os
from PIL import Image, ImageDraw, ImageFont

def add_watermark(input_image_path, output_image_path, watermark_text, position, opacity=255, font_size=30):
    # Open the original image
    base_image = Image.open(input_image_path).convert("RGBA")
    
    # Make a blank image for the watermark with an alpha layer (RGBA)
    txt = Image.new('RGBA', base_image.size, (255,255,255,0))
    
    # Choose a font and size for the watermark
    font = ImageFont.truetype("arial.ttf", font_size)
    
    # Get drawing context from the blank watermark image
    d = ImageDraw.Draw(txt)
    
    # Identify the size of the drawn text
    text_size = d.textsize(watermark_text, font=font)
    
    # Calculate the position for the watermark
    if position == "bottom_right":
        text_position = (base_image.size[0] - text_size[0] - 10, base_image.size[1] - text_size[1] - 10)
    elif position == "top_right":
        text_position = (base_image.size[0] - text_size[0] - 10, 10)
    elif position == "top_left":
        text_position = (10, 10)
    elif position == "bottom_left":
        text_position = (10, base_image.size[1] - text_size[1] - 10)
    elif position == "center":
        text_position = ((base_image.size[0] - text_size[0]) / 2, (base_image.size[1] - text_size[1]) / 2)
    else:
        raise ValueError("Invalid position for watermark. Use 'center', 'top_left', 'top_right', 'bottom_left', or 'bottom_right'.")

    # Add the text to the watermark image
    d.text(text_position, watermark_text, fill=(255,255,255,opacity), font=font)
    
    # Combine the watermark image with the base image
    watermarked = Image.alpha_composite(base_image, txt)
    
    # Convert to RGB and save final image
    watermarked.convert('RGB').save(output_image_path, "JPEG")

# Example usage: Add a watermark to an image
input_image = 'path/to/input/image.jpg'
output_image = 'path/to/output/image_with_watermark.jpg'
watermark = 'Watermark Text Here'
add_watermark(input_image, output_image, watermark, 'bottom_right', opacity=128, font_size=50)
