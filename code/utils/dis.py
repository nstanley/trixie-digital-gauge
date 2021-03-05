import digitalio
import board
import re
import time

# Broadcom numbering
dis_clk_pin = board.D16
dis_data_pin = board.D20
dis_enable_pin =board.D21

class TrixieView_DIS():
    def __init__(self, clk, data, enable, numLines):

        self.clk = digitalio.DigitalInOut(clk)
        self.clk.direction = digitalio.Direction.OUTPUT
        self.data = digitalio.DigitalInOut(data)
        self.data.direction = digitalio.Direction.OUTPUT
        self.enable = digitalio.DigitalInOut(enable)
        self.enable.direction = digitalio.Direction.OUTPUT

        # Initial settings
        self.clk.value = True
        self.data.value = True
        self.enable.value = False

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
        self.enable.value = True
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
        self.enable.value = False
        self.enable.value = True
        for val in byteObj:
            for _i in range(8):
                self.clk.value = True
                if (val & 0x80):
                    self.data.value = False # inverted logic
                else:
                    self.data.value = True # inverted logic
                val <<= 1
                self.clk.value = False
        # Reset to default
        self.enable.value = False
        self.clk.value = True
        self.data.value = True


viewRadio = TrixieView_DIS(dis_clk_pin, dis_data_pin, dis_enable_pin, 2)
viewRadio.showData("Eng Load", str(6))
time.sleep(2.0)
viewRadio.showData("Cool Tmp", str(190))
time.sleep(2.0)
viewRadio.showData("S Fuel", str(-7.86))
time.sleep(2.0)
viewRadio.showData("L Fuel", str(1.21))
time.sleep(2.0)
viewRadio.showData("RPM", str(2345))
time.sleep(2.0)
viewRadio.showData("Speed", str(30))
time.sleep(2.0)
viewRadio.showData("Intake Tmp", str(86))
time.sleep(2.0)
viewRadio.showData("MAF", str(55.66))
time.sleep(2.0)
viewRadio.showData("Throttle", str(33))
time.sleep(2.0)