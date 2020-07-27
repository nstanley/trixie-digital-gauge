# Main program to run the OBD Gauge

import time
import subprocess
import digitalio
import board
from trixie_view import TrixieView
from trixie_model import TrixieModel_OBD, TrixieModel_Demo

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Splash Image
splashFile = "/home/pi/trixie-digital-gauge/resources/audi_128x96-big-red.png"

class TrixieController():
    def __init__(self):
        # Setup VIEW
        self.view = TrixieView(cs_pin, dc_pin, reset_pin, BAUDRATE, splashFile)

        # Setup MODEL
        self.model = TrixieModel_Demo()
        #self.model = TrixieModel_OBD()
    
        # Setup list
        self.labels = ["Eng Load",
                       "Eng Temp",
                       "Short Fuel",
                       "Long Fuel",
                       "RPM",
                       "Speed",
                       "Intake Temp",
                       "MAF",
                       "Throttle"]
        self.values = [self.model.getEngineLoad,
                       self.model.getEngineTemp,
                       self.model.getShortFuelTrim,
                       self.model.getLongFuelTrim,
                       self.model.getRPM,
                       self.model.getSpeed,
                       self.model.getIntakeTemp,
                       self.model.getMAF,
                       self.model.getThrottle]
        self.index = 0

        # Connect
        if (self.model.connect("/dev/ttyAMA0", 7)):
            while (True):
                self.view.showData(self.labels[self.index], str(self.values[self.index]()))
                time.sleep(0.2)

def main():
    print("Trixie Digital Gauge Startup!")
    gauge = TrixieController()

if __name__ == "__main__":
    main()