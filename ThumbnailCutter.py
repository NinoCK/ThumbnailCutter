import os
import subprocess
import argparse

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
                subprocess.run(['ffmpeg','-y', '-i', self.src_file, '-vf', 'scale=1280:720,boxblur=10:10', self.target_file], check=True)
                # create a temporary file for the overlay
                temp_file = os.path.join(os.path.dirname(self.target_file), "temp_" + os.path.basename(self.src_file))
                # copy the original image to the temporary file
                subprocess.run(['cp', self.src_file, temp_file], check=True)
                # overlay the original image on top of the modified image, centered
                subprocess.run(['ffmpeg', '-y', '-i', self.target_file, '-i', temp_file, '-filter_complex', 'overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2', self.target_file], check=True)
                # remove the temporary file
                os.remove(temp_file)
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