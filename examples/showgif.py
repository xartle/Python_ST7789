import sys
from time import sleep
from PIL import Image, ImageSequence
import Adafruit_GPIO.SPI as SPI
import ST7789 as TFT

# Constants
RST = 27
DC = 22
SPI_PORT = 0
SPI_DEVICE = 0
SPI_MODE = 0b11
SPI_SPEED_HZ = 40000000
WIDTH = 240
HEIGHT = 240

# Configure Display
disp = TFT.ST7789(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=SPI_SPEED_HZ),
                  mode=SPI_MODE, rst=RST, dc=DC)
disp.begin()
disp.clear()

# Load and display animated GIF
def display_animated_gif(file_path):
    """
    Displays an animated GIF on the ST7789 display.

    :param file_path: Path to the GIF file.
    """
    try:
        gif = Image.open(file_path)
        if gif.format != "GIF":
            raise ValueError("The provided file is not a GIF.")

        # Resize each frame to match display dimensions
        frames = [frame.copy().resize((WIDTH, HEIGHT), Image.LANCZOS) for frame in ImageSequence.Iterator(gif)]

        while True:
            for frame in frames:
                disp.display(frame)
                sleep(gif.info.get('duration', 100) / 1000.0)  # Duration in milliseconds, default to 100ms if not provided

    except Exception as e:
        print(f"Error: {e}")
    finally:
        disp.clear()

# Main function to display the GIF from command line arguments
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <gif_file_path>")
    else:
        gif_file_path = sys.argv[1]
        display_animated_gif(gif_file_path)

