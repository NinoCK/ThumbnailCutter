import os
import subprocess

class ImageResizer:
    """
    A class that resizes images using ffmpeg and overlays the original image on top of the modified image.

    Args:
        src_dir (str): The source directory containing the images to be resized.
        target_dir (str): The target directory where the resized images will be saved.

    Attributes:
        src_dir (str): The source directory containing the images to be resized.
        target_dir (str): The target directory where the resized images will be saved.
    """

    def __init__(self, src_dir, target_dir):
        self.src_dir = src_dir
        self.target_dir = target_dir

    def resize_images(self):
        """
        Resizes the images in the source directory and overlays the original image on top of the modified image.

        This method uses ffmpeg to resize the images to a resolution of 1280x720 and apply a box blur effect.
        It then overlays the original image on top of the modified image, centered.

        Raises:
            FileNotFoundError: If the source directory does not exist.
            FileExistsError: If the target directory already exists.

        Note:
            This method requires ffmpeg to be installed on the system and accessible from the command line.
        """
        os.makedirs(self.target_dir, exist_ok=True)

        for filename in os.listdir(self.src_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                src_file = os.path.join(self.src_dir, filename)
                target_file = os.path.join(self.target_dir, filename)
                # ffmpeg process
                subprocess.run(['ffmpeg','-y', '-i', src_file, '-vf', 'scale=1280:720,boxblur=10:10', target_file], check=True)
                # create a temporary file for the overlay
                temp_file = os.path.join(self.target_dir, "temp_" + filename)
                # copy the original image to the temporary file
                subprocess.run(['cp', src_file, temp_file], check=True)
                # overlay the original image on top of the modified image, centered
                subprocess.run(['ffmpeg', '-y', '-i', target_file, '-i', temp_file, '-filter_complex', 'overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2', target_file], check=True)
                # remove the temporary file
                os.remove(temp_file)
# usage
resizer = ImageResizer('/home/ninokonis/Downloads/ThubnailCutter', '/home/ninokonis/Downloads/ThubnailCutter/results')
resizer.resize_images()

#call the function with a path for a local image in the system disk not all images in one path
#example of flow ::
#user uploads a video to the server
#a script is generating the thumbnail of the the video
#this script is resizing the thumbnail and adding a blur effect