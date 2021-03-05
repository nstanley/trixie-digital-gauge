import os
import re
import time
import subprocess
import digitalio
import board
import wiringpi
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357  # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331  # pylint: disable=unused-import

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TrixieView_OLED():
    def __init__(self, cs_pin, dc_pin, reset_pin, buad, splashFile):
        # Setup SPI connection
        print("   Connecting to OLED via SPI...")
        self.spi = board.SPI()
        # 1.27" SSD1351 Color OLED display
        print("   Configuring OLED...")
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
        print("   Setup drawing...")
        self.draw = ImageDraw.Draw(self.image)

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=(0, 0, 0))
        self.disp.image(self.image)

        # Show the splash screen
        print("   Display splash screen...")
        self.showSplash(splashFile)

        # First define some constants to allow easy positioning of text.
        self.padding = 2
        self.x = 0
        self.fontDigits = ImageFont.truetype(BASE_DIR + "/resources/SevenSegment.ttf", 64)
        self.fontLabel = ImageFont.truetype(BASE_DIR + "/resources/SevenSegment.ttf", 28)
        print("   ... Done!")

    def showData(self, label, data):
        # Clear    
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        
        # Assign values
        # Label
        self.y = self.padding
        lblwidth = self.fontLabel.getsize(label)[0]
        self.draw.text(
            (self.width // 2 - lblwidth // 2, self.y),
            label,
            font=self.fontLabel,
            fill="#FF0000"
        )
        # Data (centered horizontally)
        self.y += self.fontLabel.getsize(label)[1] + self.padding
        datawidth = self.fontDigits.getsize(data)[0]
        self.draw.text(
            (self.width // 2 - datawidth // 2, self.y),
            data,
            font=self.fontDigits,
            fill="#FF0000"
        )

        # Display
        self.disp.image(self.image)

    def showSplash(self, file):
        splash = Image.open(file)
        self.disp.image(splash)

class TrixieView_DIS():
    def __init__(self, clk, data, enable, numLines):
        self.clk = clk
        self.data = data
        self.enable = enable
        wiringpi.wiringPiSetup()
        wiringpi.pinMode(self.clk, 1)
        wiringpi.pinMode(self.data, 1)
        wiringpi.pinMode(self.enable, 1)

        # Initial settings
        wiringpi.digitalWrite(self.enable, 0)
        wiringpi.digitalWrite(self.clk, 1)
        wiringpi.digitalWrite(self.data, 1)

        if (numLines <= 1):
            self.numLines = 1
            self.showData("", "HI!")
        else:
            self.numLines = 2
            self.showData("Welcome", "")

    # thanks https://stackoverflow.com/a/21582376
    def anti_vowel(self, msg):
        result = re.sub(r'[aeiou]', '', msg)
        return result

    def showData(self, label, data):
        # self.enable.value = True
        wiringpi.digitalWrite(self.enable, 1)
        if (self.numLines == 1):
            label = self.anti_vowel(label)
            label = label[:3].upper()
            if (len(data) >= 4):
                if (data[3] == '.'):
                    data = data[:3]
            data = data[:4].rjust(4)
            message = label + " " + data + "       "
        else: # numLines == 2
            if (len(label) > 8):
                label = self.anti_vowel(label)
            label = label[:8].center(8).upper() # Audi requires uppercase
            data = data[:7].center(7)
            message = label + data
        print(": " + message + " :")
        msgArr = bytearray(message, "ascii")
        header = 0xF0
        command = 0x1C

        byteArr = bytearray()
        byteArr.append(header)
        byteArr = byteArr + msgArr
        byteArr.append(command)
        byteObj = bytes(byteArr)

        checksum = 0
        for val in byteObj:
            checksum += val
        checksum &= 0xFF
        checksum ^= 0xFF
        byteArr.append(checksum)
        byteObj = bytes(byteArr)

        # blip the enable because derpston did...
        wiringpi.digitalWrite(self.enable, 0)
        wiringpi.digitalWrite(self.enable, 1)
        for val in byteObj:
            for _i in range(8):
                wiringpi.digitalWrite(self.clk, 1)
                if (val & 0x80):
                    wiringpi.digitalWrite(self.data, 0) # active low
                else:
                    wiringpi.digitalWrite(self.data, 1)
                val <<= 1
                wiringpi.digitalWrite(self.clk, 0)
        # Reset to default
        wiringpi.digitalWrite(self.enable, 0)
        wiringpi.digitalWrite(self.clk, 1)
        wiringpi.digitalWrite(self.data, 1)