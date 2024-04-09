"""
ThumbnailCutter.py
Author: Konstantinos Konis

This program modifies an image by resizing it and adding a blurred background with a black banner at the bottom.
The program uses ffmpeg to resize the image and add the blurred background and banner.
Use it by calling the program from the command line with the source image file path and the target image file path as arguments.
"""

import os
import subprocess
import argparse
from PIL import Image, ImageDraw

class ImageResizer:
    """
    A class that resizes images using ffmpeg.

    Args:
        src_file (str): The path to the source image file.
        target_file (str): The path to the target image file.

    Attributes:
        src_file (str): The path to the source image file.
        target_file (str): The path to the target image file.
    """

    def __init__(self, src_file, target_file):
        self.src_file = src_file
        self.target_file = target_file

    def round_corners(self, radius=20):
        """
        Rounds the corners of the target image.

        Args:
            radius (int, optional): The radius of the rounded corners. Default is 30.
        """
        # Open the image file
        img = Image.open(self.target_file)
        # Create a mask
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        # Draw rounded corners
        # draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=255)  # Top-left corner
        # draw.pieslice((img.size[0] - radius * 2, 0, img.size[0], radius * 2), -90, 0, fill=255)  # Top-right corner
        # draw.pieslice((0, img.size[1] - radius * 2, radius * 2, img.size[1]), 90, 180, fill=255)  # Bottom-left corner
        # draw.pieslice((img.size[0] - radius * 2, img.size[1] - radius * 2, img.size[0], img.size[1]), 0, 90, fill=255)  # Bottom-right corner
        # draw.rectangle((radius, 0, img.size[0] - radius, img.size[1]), fill=255)  # Top and bottom rectangles
        # draw.rectangle((0, radius, img.size[0], img.size[1] - radius), fill=255)  # Left and right rectangles
        draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=255)  # Top-left corner
        draw.pieslice((img.size[0] - radius * 2, 0, img.size[0], radius * 2), -90, 0, fill=255)  # Top-right corner
        draw.rectangle((radius, 0, img.size[0] - radius, radius), fill=255)  # Top rectangle
        draw.rectangle((0, radius, img.size[0], img.size[1]), fill=255)  # Left and right rectangles
        # Apply the mask to the image
        img.putalpha(mask)
        # Save the image
        img.save(self.target_file)

    def resize_image(self):
        """
        Resizes the image using ffmpeg.

        Note:
            This method requires ffmpeg to be installed on the system and accessible from the command line.
        """
        try:
            # Check if source file exists
            if not os.path.isfile(self.src_file):
                raise FileNotFoundError(f"Source file {self.src_file} does not exist")

            os.makedirs(os.path.dirname(self.target_file), exist_ok=True)

            if self.src_file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                # ffmpeg process
                subprocess.run(['ffmpeg','-y', '-i', self.src_file, '-vf', 'scale=636:422,boxblur=10:10', self.target_file], check=True)

                # create a temporary file for the overlay
                temp_file = os.path.join(os.path.dirname(self.target_file), "temp_" + os.path.basename(self.src_file))
                # copy the original image to the temporary file
                subprocess.run(['cp', self.src_file, temp_file], check=True)

                # resize the original image to 720 height and proportional width
                resized_file = os.path.join(os.path.dirname(self.target_file), "resized_" + os.path.basename(self.src_file))
                subprocess.run(['ffmpeg', '-y', '-i', temp_file, '-vf', 'scale=-1:422', resized_file], check=True)

                # overlay the original image on top of the blurred image, centered in the frame
                overlay_file = os.path.join(os.path.dirname(self.target_file), "overlay_" + os.path.basename(self.src_file))
                subprocess.run(['ffmpeg', '-y', '-i', self.target_file, '-i', resized_file, '-filter_complex', 'overlay=(W-w)/2:(H-h)/2', overlay_file], check=True)

                # draw the box
                banner_file = os.path.join(os.path.dirname(self.target_file), "final_" + os.path.basename(self.src_file))
                subprocess.run(['ffmpeg', '-y', '-i', overlay_file, '-vf', 'drawbox=y=ih-h:w=iw:h=140:color=black@0.7:t=fill', banner_file], check=True)
                # rounds the corners of the image
                # move the final file to the target file
                os.rename(banner_file, self.target_file)
                self.round_corners()

                # remove the temporary file
                os.remove(temp_file)
                os.remove(resized_file)
                os.remove(overlay_file)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while executing a subprocess: {str(e)}")
        except FileNotFoundError as e:
            print(str(e))
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Resize an image.')
    parser.add_argument('src_file', type=str, help='The source file path of the image to be resized.')
    parser.add_argument('target_file', type=str, help='The target file path where the resized image will be saved.')
    args = parser.parse_args()

    resizer = ImageResizer(args.src_file, args.target_file)
    resizer.resize_image()

if __name__ == "__main__":
    main()