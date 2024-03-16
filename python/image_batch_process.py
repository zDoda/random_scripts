#!/usr/bin/env python3

import os
from PIL import Image

def batch_process_images(input_dir, output_dir, size=(800, 600), fmt='JPEG'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif')):
                img_path = os.path.join(root, file)
                img = Image.open(img_path)
                
                # Resize the image
                img.thumbnail(size, Image.ANTIALIAS)
                
                # Convert the format
                file_basename, file_ext = os.path.splitext(file)
                new_filename = file_basename + '.' + fmt.lower()
                new_path = os.path.join(output_dir, new_filename)
                
                img.save(new_path, fmt)

if __name__ == "__main__":
    import argparse

    # Set up argument parser
    parser = argparse.ArgumentParser(description='Batch resize and convert images')
    parser.add_argument('input_dir', help='Input directory where images are located')
    parser.add_argument('output_dir', help='Output directory where processed images will be saved')
    parser.add_argument('--size', nargs=2, type=int, default=(800, 600), help='Size to which images will be resized (width height)')
    parser.add_argument('--format', type=str, default='JPEG', choices=['JPEG', 'PNG', 'GIF', 'BMP', 'TIFF'], help='Format to convert images to')

    # Parse arguments
    args = parser.parse_args()
    
    # Calling the batch process function
    batch_process_images(args.input_dir, args.output_dir, tuple(args.size), args.format)
