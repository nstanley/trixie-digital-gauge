#!/bin/bash
# Installs required packages for this project

# apt packages
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo apt-get install wiringpi

# pip packages
pip3 install obd
pip3 install wiringpi
pip3 install adafruit-circuitpython-mcp3xxx
pip3 install adafruit-circuitpython-rgb-display

# Seven seg font original source
# wget -O sevensegttf.zip https://dl.dafont.com/dl/?f=seven_segment
# unzip sevensegttf.zip

# py-gaugette
cd ~
git clone git://github.com/guyc/py-gaugette.git
cd py-gaugette
sudo python3 setup.py install