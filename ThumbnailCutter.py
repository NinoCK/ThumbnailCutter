import os
import subprocess
import argparse

class ImageResizer:
    """
    A class that resizes images using ffmpeg and overlays the original image on top of the modified image.

    Args:
        src_file (str): The source file path of the image to be resized.
        target_file (str): The target file path where the resized image will be saved.

    Attributes:
        src_file (str): The source file path of the image to be resized.
        target_file (str): The target file path where the resized image will be saved.
    """

    def __init__(self, src_file, target_file):
        self.src_file = src_file
        self.target_file = target_file

    def resize_image(self):
        """
        Resizes the image and overlays the original image on top of the modified image.

        This method uses ffmpeg to resize the image to a resolution of 1280x720 and apply a box blur effect.
        It then overlays the original image on top of the modified image, centered.

        Raises:
            FileNotFoundError: If the source file does not exist.
            FileExistsError: If the target file already exists.

        Note:
            This method requires ffmpeg to be installed on the system and accessible from the command line.
        """
        os.makedirs(os.path.dirname(self.target_file), exist_ok=True)

        if self.src_file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # ffmpeg process
            subprocess.run(['ffmpeg','-y', '-i', self.src_file, '-vf', 'scale=1280:720,boxblur=10:10', self.target_file], check=True)
            # create a temporary file for the overlay
            temp_file = os.path.join(os.path.dirname(self.target_file), "temp_" + os.path.basename(self.src_file))
            # copy the original image to the temporary file
            subprocess.run(['cp', self.src_file, temp_file], check=True)
            # overlay the original image on top of the modified image, centered
            subprocess.run(['ffmpeg', '-y', '-i', self.target_file, '-i', temp_file, '-filter_complex', 'overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2', self.target_file], check=True)
            # remove the temporary file
            os.remove(temp_file)
def main():
    parser = argparse.ArgumentParser(description='Resize an image.')
    parser.add_argument('src_file', type=str, help='The source file path of the image to be resized.')
    parser.add_argument('target_file', type=str, help='The target file path where the resized image will be saved.')
    args = parser.parse_args()

    resizer = ImageResizer(args.src_file, args.target_file)
    resizer.resize_image()

if __name__ == "__main__":
    main()

#call the function with a path for a local image in the system disk not all images in one path
#example of flow ::
#user uploads a video to the server
#a script is generating the thumbnail of the the video
#this script is resizing the thumbnail and adding a blur effect