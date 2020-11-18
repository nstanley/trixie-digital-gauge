# Main program to run the OBD Gauge

import os
import time
import subprocess
import digitalio
import board
import gaugette.gpio
import gaugette.rotary_encoder

from trixie_view import TrixieView
from trixie_model import TrixieModel, TrixieModel_OBD, TrixieModel_Demo

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Splash Image
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
splashFile = BASE_DIR + "/resources/audi_128x96-big-red.png"

# Rotary encoder pins (WiringPi numbering)
enc_A_pin = 25
enc_B_pin = 24

class TrixieController():
    def __init__(self):
        # Setup VIEW
        self.view = TrixieView(cs_pin, dc_pin, reset_pin, BAUDRATE, splashFile)

        # Setup MODEL
        self.modelDemo = TrixieModel_Demo()
        self.modelOBD = TrixieModel_OBD()
        self.model = self.modelOBD

        # Connect
        if (self.model.connect("/dev/ttyAMA0", 7)):
            print("Connected!")
        else:
            print("OBD Timeout, switch to DEMO MODE!")
            self.model = self.modelDemo
            self.model.connect("/dev/ttyAMA0", 7)

        # Setup list
        self.labels = ("Eng Load",
                       "Cool Tmp",
                       "Short Fuel",
                       "Long Fuel",
                       "RPM",
                       "Speed",
                       "Intake Tmp",
                       "MAF",
                       "Throttle")
        self.values = (self.model.getEngineLoad,
                       self.model.getEngineTemp,
                       self.model.getShortFuelTrim,
                       self.model.getLongFuelTrim,
                       self.model.getRPM,
                       self.model.getSpeed,
                       self.model.getIntakeTemp,
                       self.model.getMAF,
                       self.model.getThrottle)
        self.index = 0
        
        # Setup rotary encoder
        gpio = gaugette.gpio.GPIO()
        self.encoder = gaugette.rotary_encoder.RotaryEncoder(gpio, enc_A_pin, enc_B_pin, self.rotated)
        self.encoder.start()

    def run(self):
        while (True):
            self.view.showData(self.labels[self.index], str(self.values[self.index]()))
            time.sleep(0.2)
    
    # ISR for rotary encoder
    def rotated(self, direction):
        self.index += direction
        if (self.index >= len(self.labels)):
            self.index = 0
        if (self.index < 0):
            self.index = len(self.labels) - 1

def main():
    print("Trixie Digital Gauge Startup!")
    gauge = TrixieController()
    gauge.run()

if __name__ == "__main__":
    main()