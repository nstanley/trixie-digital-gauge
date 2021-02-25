import digitalio
import board
import re

# Radio display pins (WiringPi numbering)
# dis_clk_pin = 27
# dis_data_pin = 28
# dis_enable_pin = 29
# Broadcom numbering
dis_clk_pin = board.D16
dis_data_pin = board.D20
dis_enable_pin =board.D21

class TrixieView_DIS():
    def __init__(self, clk, data, enable):
        # self.clk = clk
        # self.data = data
        # self.enable = enable
        # wiringpi.wiringPiSetup()
        # wiringpi.pinMode(self.clk, 1)
        # wiringpi.pinMode(self.data, 1)
        # wiringpi.pinMode(self.enable, 1)

        self.clk = digitalio.DigitalInOut(clk)
        self.clk.direction = digitalio.Direction.OUTPUT
        self.data = digitalio.DigitalInOut(data)
        self.data.direction = digitalio.Direction.OUTPUT
        self.enable = digitalio.DigitalInOut(enable)
        self.enable.direction = digitalio.Direction.OUTPUT

        self.showData("Welcome", "")

    # thanks https://stackoverflow.com/a/21582376
    def anti_vowel(self, msg):
        result = re.sub(r'[aeiou]', '', msg)
        return result

    def showData(self, label, data):
        if (len(label) > 8):
            label = self.anti_vowel(label)
        label = label[:8].center(8)
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

        self.enable.value = True
        # wiringpi.digitalWrite(self.enable, 1)
        for val in byteObj:
            for i in range(8):
                if (val & 0x80):
                    self.data.value = True
                    # wiringpi.digitalWrite(self.data, 1)
                else:
                    self.data.value = False
                    # wiringpi.digitalWrite(self.data, 0)
                val <<= 1
            self.clk.value = False
            self.clk.value = True
            # wiringpi.digitalWrite(self.clk, 0)
            # wiringpi.digitalWrite(self.clk, 1)
        self.enable.value = False
        # wiringpi.digitalWrite(self.enable, 0)


viewRadio = TrixieView_DIS(dis_clk_pin, dis_data_pin, dis_enable_pin)
viewRadio.showData("Speed", 30)