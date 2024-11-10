# Python_ST7789
Python library for using ST7789-based IPS LCD with Raspberry Pi
(240x240 pixels, SPI interface, 7 pins without CS pin)


Code snippet for GMT130 display
```
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
GPIO.setup(backlight, GPIO.OUT, initial=GPIO.HIGH)

