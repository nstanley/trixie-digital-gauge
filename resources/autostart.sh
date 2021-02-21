#!/bin/bash

# This is the GPIO pin connected to the lead on switch labeled IN
MB_IN_PIN=4

echo "Setting Mausberry IN pin [${MB_IN_PIN}]!"
echo "${MB_IN_PIN}" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio${MB_IN_PIN}/direction
echo "1" > /sys/class/gpio/gpio${MB_IN_PIN}/value

# Run the gauge
echo "Starting Trixie's OBD-II gauge!"
python3 /root/trixie-digital-gauge/code/trixie.py

# The gauge will fault/exit when it tries to read the OBD and the car is off
# so we will return to this line of the script, power off
echo "Trixie's Gauge has exited, shutdown!"
poweroff