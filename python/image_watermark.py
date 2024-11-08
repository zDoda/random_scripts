#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

def add_watermark(input_image_path, output_image_path, watermark_text, position=(0, 0)):
    # Open the original image
    original_image = Image.open(input_image_path)

    # Create a drawable image
    watermark_image = Image.new('RGBA', original_image.size)
    # Create a drawing context
    draw = ImageDraw.Draw(watermark_image)

    # Specify a font and size for the watermark
    font = ImageFont.truetype('arial.ttf', 36)

    # Get text size
    text_width, text_height = draw.textsize(watermark_text, font)

    # Calculate the position of the watermark
    if position == 'center':
        x = (watermark_image.size[0] - text_width) // 2
        y = (watermark_image.size[1] - text_height) // 2
        position = (x, y)
    elif position == 'bottom_right':
        x = watermark_image.size[0] - text_width - 10
        y = watermark_image.size[1] - text_height - 10
        position = (x, y)

    # Position the text at the bottom right
    draw.text(position, watermark_text, (255, 255, 255), font=font)

    # Combine the original image with the watermark
    watermarked_image = Image.alpha_composite(original_image.convert('RGBA'), watermark_image)

    # Save the watermarked image
    watermarked_image.save(output_image_path, 'PNG')

# Example usage:
# add_watermark('input.jpg', 'watermarked.png', '© YourName', 'bottom_right')

# If you want to process all images in a directory and add watermarks to them
def batch_watermark_images(input_dir, output_dir, watermark_text, position='bottom_right'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_image_path = os.path.join(input_dir, filename)
            output_image_path = os.path.join(output_dir, 'watermarked_' + filename)

            add_watermark(input_image_path, output_image_path, watermark_text, position)

# Example batch processing:
# batch_watermark_images('path_to_input_images', 'path_to_output_images', '© YourName', 'bottom_right')
