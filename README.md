
# AutoCrop
AutoCrop is a Python script that crops all images in a folder. The crop can happen automatically (to cut out black borders) or manually (given height or width or both, and a fixed point).

## Usage
To use AutoCrop, run the following command in your terminal:

    python AutoCrop.py /path/to/folder [--extension EXTENSION] [--padding PADDING] [--width WIDTH] [--height HEIGHT] [--fix FIX] [--append APPEND]

The script takes the following arguments:
- `path`: Path to the folder containing the images (REQUIRED)
- `extension`: File extension for the input and output files (default: png)
- `append`: custom append for the output file name (default: _crop)
- `padding`: Padding to add to the cropped image (pixels, default: 0)
- `width`, `height`: target image final width/height (pixels)
	-  (default) if none are given, the automatic black border detection is used to crop. (Useful for movie screenshots)
	- if only one is given, the image is cropped to the given one, while keeping the other as the original.
	- if both are given, the image is cropped with those final dimensions.
	- if any given dimension is larger than the original, the original is kept

- `fix`: fixed point/side, crop the rest (only considered if at least one dimension if given)
	- (default: `center`) the default behaviour centers the cropping, so the center of the image is fixed.
	- options: center, top, bottom, left, right, topleft, topright, bottomleft, bottomright
	- if given height, you should set center/top/bottom
	- if given width, you should set center/left/right
	- if given both dimensions, you can set the corner to fix (topleft, topright, bottomleft, bottomright), or just the side (top, bottom, left, right), in this latter case the other dimension is centered

## Examples
Default behaviour: crop all PNG images in the folder `/path/to/folder` using the **automatic black border detection**, then save the cropped images with the new file name appended with `_crop.png`.

    python AutoCrop.py /path/to/folder

**Crop 1080p movie screenshots to a 18:9 format** (vertical crop): the original image is ideally 1920x1080 with a 16:9 screen (but it's not important), so the 18:9 equivalent is 1920x960, thus:

    python AutoCrop.py /path/to/folder --height 960

**Crop the top-left 500x500 square** of all PNG images to a custom width of 500 pixels, then save the cropped images with the new file name appended with `_sq.png`:

    python AutoCrop.py /path/to/folder --width 500 --height 500 --fix topleft --append _sq

**Crop the bottom-center 500x300 portion** of all JPG images:

    python AutoCrop.py /path/to/folder --width 500 --height 300 --extension jpg --fix bottom

## Credits
AutoCrop was created by me in my free time, since I like to have movie screenshots as wallpapers, but often they contain black borders. I will share my wallpapers on my [website](https://thefacc.github.io). The script is based on the Pillow library, a popular Python library used for handling and transforming image files.

