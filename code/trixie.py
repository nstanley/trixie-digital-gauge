# Main program to run the OBD Gauge

import digitalio
import board
from trixie_view import TrixieView

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

class TrixieController():
    def __init__(self):
        self.view = TrixieView(cs_pin, dc_pin, reset_pin, BAUDRATE)
        self.view.showSplash("/home/pi/trixie-digital-gauge/resources/audi_128x96.png")
        #self.view.showData("Speed", 37)

def main():
    print("Trixie Digital Gauge Startup!")
    gauge = TrixieController()

if __name__ == "__main__":
    main()