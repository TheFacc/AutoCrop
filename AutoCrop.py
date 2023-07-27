import argparse
from PIL import Image
import sys
import glob
from PIL import ImageOps
import numpy as np
import os

# Crop all images with black background in a folder
# Usage "python AutoCrop.py /path/to/folder [-h] [--extension EXTENSION] [--padding PADDING]
#                                         [--width WIDTH] [--height HEIGHT] [--fix FIXED] [--append APPEND]""

parser = argparse.ArgumentParser(description='Crop all images with black background in a folder')
parser.add_argument('path', type=str, help='Path to the folder containing images')
parser.add_argument('--extension', type=str, default='png', help='File extension for the input and output files (default: png)')
parser.add_argument('--padding', type=int, default=0, help='Padding to add to the cropped image (pixels, default 0)')
parser.add_argument('--width', type=int, help='Width to crop the image to (pixels)')
parser.add_argument('--height', type=int, help='Height to crop the image to (pixels)')
parser.add_argument('--fix', type=str, default='center', help='Fixed point, crop the rest: center (default), top, bottom, left, right, topleft, topright, bottomleft, bottomright')
parser.add_argument('--append', type=str, default='_crop', help='Custom append for the output file name (default: _crop)')
args = parser.parse_args()

path = args.path
padding = args.padding
width = args.width
height = args.height
append = args.append
extension = args.extension
fix = args.fix

filePaths = glob.glob(path + f"/*.{extension}") # search for all images in the folder

print(f"Cropping '.{extension}' files in folder.")
if width is not None and height is not None:
    if fix in ['top', 'bottom', 'left', 'right']:
        print(f"Cropping method: Custom size ({width}x{height})")
        print(f"Cropping from: {fix} (centered in the other direction)")
    else:
        print(f"Cropping method: Custom size ({width}x{height})")
        print(f"Cropping from: {fix}")
elif width is not None:
    if fix in ['left', 'right']:
        print(f"Cropping method: Custom width ({width}x(original height))")
        print(f"Cropping from: {fix} (centered vertically)")
    else:
        print(f"Cropping method: Custom width ({width}x(original height))")
        print(f"Cropping from: {fix}")
elif height is not None:
    if fix in ['top', 'bottom']:
        print(f"Cropping method: Custom height ((original width)x{height})")
        print(f"Cropping from: {fix} (centered horizontally)")
    else:
        print(f"Cropping method: Custom height ((original width)x{height})")
        print(f"Cropping from: {fix}")
else:
    print(f"Cropping method: Automatic (imageBox)")
    print(f"Saving as: '.{extension.upper()}' files with '{append}' appended to the original file name.")
    print(f"Cropping from: {fix}")
print(f"Saving as: '.{extension.upper()}' files with '{append}' appended to the original file name.")

print()

for index, filePath in enumerate(filePaths):
    image=Image.open(filePath)
    image.load()
    imageSize = image.size

    # Check if the image is smaller than the given dimension
    if (width is not None and imageSize[0] < width) or (height is not None and imageSize[1] < height):
        print(f"({index+1}/{len(filePaths)})", filePath, "Size:", imageSize, "New Size: unchanged (already smaller than given dimensions)")
        cropped = image
    else:
        # Create box conditionally
        if width is not None and height is not None:
            if fix == 'topleft':
                imageBox = (0, 0, width, height)
            elif fix == 'topright':
                imageBox = (imageSize[0]-width, 0, imageSize[0], height)
            elif fix == 'bottomleft':
                imageBox = (0, imageSize[1]-height, width, imageSize[1])
            elif fix == 'bottomright':
                imageBox = (imageSize[0]-width, imageSize[1]-height, imageSize[0], imageSize[1])
            elif fix == 'top':
                imageBox = ((imageSize[0]-width)//2, 0, (imageSize[0]+width)//2, height)
            elif fix == 'bottom':
                imageBox = ((imageSize[0]-width)//2, imageSize[1]-height, (imageSize[0]+width)//2, imageSize[1])
            elif fix == 'left':
                imageBox = (0, (imageSize[1]-height)//2, width, (imageSize[1]+height)//2)
            elif fix == 'right':
                imageBox = (imageSize[0]-width, (imageSize[1]-height)//2, imageSize[0], (imageSize[1]+height)//2)
            else: # center
                imageBox = ((imageSize[0]-width)//2, (imageSize[1]-height)//2, (imageSize[0]+width)//2, (imageSize[1]+height)//2)
        elif width is not None:
            if fix == 'left':
                imageBox = (0, 0, width, imageSize[1])
            elif fix == 'right':
                imageBox = (imageSize[0]-width, 0, imageSize[0], imageSize[1])
            else: # center
                imageBox = ((imageSize[0]-width)//2, 0, (imageSize[0]+width)//2, imageSize[1])
        elif height is not None:
            if fix == 'top':
                imageBox = (0, 0, imageSize[0], height)
            elif fix == 'bottom':
                imageBox = (0, imageSize[1]-height, imageSize[0], imageSize[1])
            else: # center
                imageBox = (0, (imageSize[1]-height)//2, imageSize[0], (imageSize[1]+height)//2)
        else:
            invert_im = image.convert("RGB") # remove alpha channel
            #invert_im = ImageOps.invert(invert_im) # invert if you want to remove white instead of black
            imageBox = invert_im.getbbox()
            imageBox = tuple(np.asarray(imageBox)+padding)
        # Crop based on the box
        print(f"({index+1}/{len(filePaths)})", filePath, "Size:", imageSize, "New Size:", imageBox)
        cropped=image.crop(imageBox)

    # Save
    file_name = os.path.splitext(os.path.basename(filePath))[0]
    output_file_name = file_name + append + '.' + extension
    cropped.save(os.path.join(path, output_file_name))

print("\nDone!")
