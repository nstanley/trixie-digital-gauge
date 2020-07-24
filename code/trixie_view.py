import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357  # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331  # pylint: disable=unused-import

class TrixieView():
    def __init__(self, cs_pin, dc_pin, reset_pin, buad):
        # Setup SPI connection
        self.spi = board.SPI()
        # 1.27" SSD1351 Color OLED display
        self.disp = ssd1351.SSD1351(
            self.spi,
            height=96,
            y_offset=32,
            rotation=0,
            cs=cs_pin,
            dc=dc_pin,
            rst=reset_pin,
            baudrate=buad,
        )
        # Rotation calculation
        if self.disp.rotation % 180 == 90:
            self.height = self.disp.width  # we swap height/width to rotate it to landscape!
            self.width  = self.disp.height
        else:
            self.width  = self.disp.width  # we swap height/width to rotate it to landscape!
            self.height = self.disp.height
        
        self.image = Image.new("RGB", (self.width, self.height))
        
        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=(0, 0, 0))
        self.disp.image(self.image)

        # First define some constants to allow easy positioning of text.
        self.padding = 2
        self.x = 0

        self.fontDigits = ImageFont.truetype("/home/pi/trixie-digital-gauge/resources/SevenSegment.ttf", 64)
        self.fontLabel = ImageFont.truetype("/home/pi/trixie-digital-gauge/resources/SevenSegment.ttf", 28)

    def showData(self, label, data):
        # Clear    
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        
        # Assign values
        # Label
        self.y = self.padding
        self.draw.text(
            (self.x, self.y),
            label,
            font=self.fontLabel,
            fill="#FF0000"
        )
        # Data (centered horizontally)
        self.y += self.fontLabel.getsize(label)[1] + self.padding
        fontwidth = self.fontDigits.getsize(data)[0]
        self.draw.text(
            (self.width // 2 - fontwidth // 2, self.y),
            data,
            font=self.fontDigits,
            fill="#FF0000"
        )

        # Display
        self.disp.image(self.image)

    def showSplash(self, file):
        splash = Image.open(file)
        self.disp.image(splash)
