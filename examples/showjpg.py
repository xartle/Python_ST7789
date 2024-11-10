import sys
from time import sleep
from PIL import Image
import Adafruit_GPIO.SPI as SPI
import ST7789 as TFT
import RPi.GPIO as GPIO

# Constants
RST = 27
DC = 22
backlight = 5
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

GPIO.setwarnings(True)  # Enable warnings
GPIO.setmode(GPIO.BCM)  # or GPIO.BOARD, depending on the wiring
GPIO.setup(backlight, GPIO.OUT, initial=GPIO.HIGH)  # Set initial state to LOW

def set_gpio5_low():
    GPIO.output(backlight, GPIO.LOW)

def set_gpio5_high():
    GPIO.output(backlight, GPIO.HIGH)



# Load and display image
def display_image(file_path, display_time=5, direction='up'):
    """
    Displays a JPEG image with a scroll animation effect for a specified duration.

    :param file_path: Path to the JPEG file.
    :param display_time: Time in seconds to display the image.
    :param direction: Direction of the scroll animation ('up', 'down', 'left', 'right').
    """
    try:
        image = Image.open(file_path)
        image = image.resize((WIDTH, HEIGHT), Image.LANCZOS)
        steps = 20
        step_duration = 0.05

        # Scroll effect: move the image in the specified direction to fully on screen
        for step in range(steps):
            offset = int((HEIGHT / steps) * step) if direction in ['up', 'down'] else int((WIDTH / steps) * step)
            scrolling_image = Image.new("RGB", (WIDTH, HEIGHT), "BLACK")
            if direction == 'up':
                scrolling_image.paste(image, (0, HEIGHT - offset))
            elif direction == 'down':
                scrolling_image.paste(image, (0, -HEIGHT + offset))
            elif direction == 'left':
                scrolling_image.paste(image, (WIDTH - offset, 0))
            elif direction == 'right':
                scrolling_image.paste(image, (-WIDTH + offset, 0))
            disp.display(scrolling_image)
            sleep(step_duration)

        # Hold the image for the specified time
        sleep(display_time)

        # Scroll effect: move the image off the screen in the specified direction
        for step in range(steps):
            offset = int((HEIGHT / steps) * step) if direction in ['up', 'down'] else int((WIDTH / steps) * step)
            scrolling_image = Image.new("RGB", (WIDTH, HEIGHT), "BLACK")
            if direction == 'up':
                scrolling_image.paste(image, (0, -offset))
            elif direction == 'down':
                scrolling_image.paste(image, (0, offset - HEIGHT))
            elif direction == 'left':
                scrolling_image.paste(image, (-offset, 0))
            elif direction == 'right':
                scrolling_image.paste(image, (offset - WIDTH, 0))
            disp.display(scrolling_image)
            sleep(step_duration)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        black_image = Image.new("RGB", (WIDTH, HEIGHT), "BLACK")
        disp.display(black_image)
        set_gpio5_low()

# Main function to display the image from command line arguments
if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python script.py <image_file_path> [direction]")
    else:
        image_file_path = sys.argv[1]
        direction = sys.argv[2] if len(sys.argv) == 3 else 'up'
        display_image(image_file_path, display_time=5, direction=direction)
	
