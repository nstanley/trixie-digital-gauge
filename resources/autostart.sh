#!/bin/bash

# T
his is the GPIO pin connected to the lead on switch labeled IN
GPIOpin2=4

echo "$GPIOpin2" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio$GPIOpin2/direction
echo "1" > /sys/class/gpio/gpio$GPIOpin2/value

# Run the gauge
python3 /root/trixie-digital-gauge/code/trixie.py

# The gauge will fault/exit when it tries to read the OBD and the car is off
# so we will return to this line of the script, power off
poweroff