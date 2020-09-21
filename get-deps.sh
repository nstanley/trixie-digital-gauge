#!/bin/bash
# Installs required packages for this project

# apt packages
sudo apt-get install python3-pip
sudo apt-get install python3-pil

# pip packages
pip3 install obd
pip3 install wiringpi
pip3 install adafruit-circuitpython-mcp3xxx
pip3 install adafruit-circuitpython-rgb-display

# Seven seg font
wget -O sevensegttf.zip https://dl.dafont.com/dl/?f=seven_segment
unzip sevensegttf.zip
mv 'Seven Segment.ttf' resources/SevenSegment.ttf

# py-gaugette
cd ~
git clone git://github.com/guyc/py-gaugette.git
cd py-gaugette
sudo python setup.py install