#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import os

# Define path to your images and watermark text
image_folder_path = "/path/to/your/images/"
watermark_text = "Your Watermark Here"
output_folder_path = "/path/to/save/watermarked/images/"
font_path = "/path/to/font.ttf"  # Update this with the absolute path to your font file

# Function to add watermark to an image
def add_watermark(input_image_path, output_image_path, watermark, position):
    image = Image.open(input_image_path).convert("RGBA")
    watermark = Image.new("RGBA", image.size)
    draw = ImageDraw.Draw(watermark, "RGBA")
    width, height = image.size
    
    font_size = 100  # Adjust font size as needed
    font = ImageFont.truetype(font_path, font_size)

    text_width, text_height = draw.textsize(watermark, font)
    x = position[0]
    y = position[1]

    draw.text((x, y), watermark, font=font, fill=(255, 255, 255, 128))
    
    watermarked_image = Image.alpha_composite(image, watermark)
    watermarked_image = watermarked_image.convert("RGB") # Remove alpha for saving in jpg format
    watermarked_image.save(output_image_path)

# Iterate over all images in the folder 
for image_filename in os.listdir(image_folder_path):
    if image_filename.endswith(('.png', '.jpg', '.jpeg')):
        print(f"Processing {image_filename}")
        image_path = os.path.join(image_folder_path, image_filename)
        output_path = os.path.join(output_folder_path, image_filename)
        add_watermark(image_path, output_path, watermark_text, (30, 30))  # You can change the position as you like

print("Watermarking complete.")
