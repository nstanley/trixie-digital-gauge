# Main program to run the OBD Gauge

import os
import time
import subprocess
import digitalio
import board
import gaugette.gpio
import gaugette.rotary_encoder
import json
import enum

from trixie_view import TrixieView_OLED, TrixieView_DIS
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
enc_A_pin = 23
enc_B_pin = 24
enc_btn_pin = 25

# Radio display pins (WiringPi numbering)
# dis_clk_pin = 27
# dis_data_pin = 28
# dis_enable_pin = 29
# Broadcom numbering
dis_clk_pin = board.D16
dis_data_pin = board.D20
dis_enable_pin =board.D21

class Mode(str, enum.Enum):
    ControlGauge = "ControlGauge"
    ControlRadio = "ControlRadio"
    ControlNone = "ControlNone"

class TrixieController():
    def __init__(self):
        # Setup VIEW
        self.viewGauge = TrixieView_OLED(cs_pin, dc_pin, reset_pin, BAUDRATE, splashFile)
        self.viewRadio = TrixieView_DIS(dis_clk_pin, dis_data_pin, dis_enable_pin)
    
        # Setup MODEL
        self.modelDemo = TrixieModel_Demo()
        self.modelOBD = TrixieModel_OBD()
        self.model = self.modelOBD

        # Connect
        if (self.model.connect("/dev/ttyUSB0", 7)):
            self.demo = False
            print("Connected!")
        else:
            self.demo = True
            self.startTime = time.perf_counter()
            print("OBD Timeout, switch to DEMO MODE!")
            self.model = self.modelDemo
            self.model.connect("/dev/ttyAMA0", 7)

        # Setup list
        self.labels = ("Eng Load",
                       "Cool Tmp",
                       "S Fuel",
                       "L Fuel",
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
        self.load()
        
        # Setup rotary encoder
        gpio = gaugette.gpio.GPIO()
        self.encoder = gaugette.rotary_encoder.RotaryEncoder(gpio, enc_A_pin, enc_B_pin, self.rotated)
        self.encoder.start()
        self.button = gaugette.gaugette.switch.Switch(gpio, enc_btn_pin)
        self.button.enable_isr(gpio.EDGE_FALLING, self.pushed)

    def run(self):
        running = True
        while (running):
            try:
                self.viewGauge.showData(self.labels[self.gaugeIndex], str(self.values[self.gaugeIndex]()))
                if (self.radioIndex >= len(self.labels)):
                    self.viewRadio.showData("", "")
                else:
                    self.viewRadio.showData(self.labels[self.radioIndex], str(self.values[self.radioIndex]()))
                time.sleep(0.2)
            except:
                running = False

            # Only run the demo for 64s
            if self.demo:
                now = time.perf_counter()
                diff = now - self.startTime
                if (diff > 64):
                    running = False
        self.save()
        exit()
    
    # ISR for rotary encoder
    def rotated(self, direction):
        if (self.modeIndex == Mode.ControlGauge):
            self.gaugeIndex += direction
            if (self.gaugeIndex >= len(self.labels)):
                self.gaugeIndex = 0
            if (self.gaugeIndex < 0):
                self.gaugeIndex = len(self.labels) - 1
        elif (self.modeIndex == Mode.ControlRadio):
            self.radioIndex += direction
            if (self.radioIndex > len(self.labels)): # additional index for off
                self.radioIndex = 0
            if (self.radioIndex < 0):
                self.radioIndex = len(self.labels)

    def pushed(self):
        if (self.modeIndex == Mode.ControlGauge):
            self.modeIndex = Mode.ControlRadio
        elif (self.modeIndex == Mode.ControlRadio):
            self.modeIndex = Mode.ControlNone
        elif (self.modeIndex == Mode.ControlNone):
            self.modeIndex = Mode.ControlGauge

    def save(self):
        data = {}
        data['save'] = []
        data['save'].append(
            {
                'gaugeIndex': self.gaugeIndex,
                'radioIndex': self.radioIndex,
                'modeIndex': self.modeIndex
            }
        )
        with open('save.json', 'w') as filePtr:
            json.dump(data, filePtr)

    def load(self):
        try:
            with open('save.json', 'r') as filePtr:
                saveData = json.load(filePtr)
                for d in saveData['save']:
                    self.gaugeIndex = d['gaugeIndex']
                    self.radioIndex = d['radioIndex']
                    self.modeIndex = d['modeIndex']
        except:
            self.gaugeIndex = 0
            self.radioIndex = 0
            self.modeIndex = Mode.ControlNone

def main():
    print("Trixie Digital Gauge Startup!")
    gauge = TrixieController()
    gauge.run()

if __name__ == "__main__":
    main()