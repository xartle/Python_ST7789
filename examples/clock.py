import datetime
import numpy as np
from time import sleep
from PIL import Image, ImageDraw, ImageFont
import Adafruit_GPIO.SPI as SPI
import ST7789 as TFT

# Constants
RST = 27
DC = 22
LED = 5
SPI_PORT = 0
SPI_DEVICE = 0
SPI_MODE = 0b11
SPI_SPEED_HZ = 40000000
WIDTH = 240
HEIGHT = 240
CLOCK_RADIUS = 90
PI = 3.14159265358979

# Configure Display
disp = TFT.ST7789(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=SPI_SPEED_HZ),
                  mode=SPI_MODE, rst=RST, dc=DC, led=LED)
disp.begin()
disp.clear()

# Helper Functions
def expand_to_square(pil_img, background_color):
    """
    Expands a PIL image to a square with the given background color.
    """
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), background_color)
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result

def draw_rotated_text(image, text, position, angle, font, fill):
    """
    Draw text at an angle on an image.
    """
    text_image = Image.new('RGBA', (font.getsize(text)[0], font.getsize(text)[1]), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_image)
    draw.text((0, 0), text, font=font, fill=fill)
    rotated = text_image.rotate(angle, expand=1)
    image.paste(rotated, position, rotated)

def draw_analog_clock(draw, center_x, center_y, radius, time_obj):
    """
    Draws an analog clock on the given image.
    """
    second_hand_length = radius - 2
    minute_hand_length = radius - 8
    hour_hand_length = minute_hand_length - 16

    hour = time_obj.hour
    minute = time_obj.minute
    second = time_obj.second

    # Draw clock circle
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), outline=(255, 255, 255), fill=(0, 0, 0))

    # Draw second hand
    end_x = center_x + second_hand_length * np.sin(PI * (second / 30.0))
    end_y = center_y - second_hand_length * np.cos(PI * (second / 30.0))
    draw.line((center_x, center_y, end_x, end_y), fill=(255, 0, 0))

    # Draw minute hand
    end_x = center_x + minute_hand_length * np.sin(PI * ((minute / 30.0) + (second / 1800.0)))
    end_y = center_y - minute_hand_length * np.cos(PI * ((minute / 30.0) + (second / 1800.0)))
    draw.line((center_x, center_y, end_x, end_y), fill=(255, 255, 0))

    # Draw hour hand
    end_x = center_x + hour_hand_length * np.sin(PI * ((hour / 6.0) + (minute / 360.0) + (second / 21600.0)))
    end_y = center_y - hour_hand_length * np.cos(PI * ((hour / 6.0) + (minute / 360.0) + (second / 21600.0)))
    draw.line((center_x, center_y, end_x, end_y), fill=(63, 255, 63))

def display_clock():
    """
    Main loop to display the analog clock.
    """
    try:
        last_time = ""
        while True:
            current_time = datetime.datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")
            
            if formatted_time != last_time:
                last_time = formatted_time
                image = Image.new("RGB", (WIDTH, HEIGHT), "BLACK")
                draw = ImageDraw.Draw(image)
                
                # Draw analog clock
                draw_analog_clock(draw, WIDTH // 2, HEIGHT // 2, CLOCK_RADIUS, current_time)
                
                # Display image
                disp.display(image)
            
            sleep(0.1)
    except KeyboardInterrupt:
        disp.clear()
        image = Image.new("RGB", (WIDTH, HEIGHT), "BLACK")
        disp.display(image)
        sleep(1)
        disp.clear()

# Run the clock display function
display_clock()

