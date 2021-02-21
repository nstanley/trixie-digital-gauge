# trixie-digital-gauge
A digital OBD-II gauge for my 2001 Audi TT, Trixie!

## Overview
I've wanted to do an On Board Diagnostics project for a while, just for the sake of seeing some of the data my car knows but I don't. I've deployed this to my project/fun car, a 2001 Audi TT.  
When the car is turned on, the Raspberry Pi is powered on and it runs the appropriate python script. The user can cycle through the available data via a rotary encoder. Once the car is powered off, the Raspberry Pi will shutdown automatically, waiting for the next ignition.

## Hardware
Most aftermarked car gauges come in a 52mm package, so that was my target for selecting a screen. There are probably screens that will fit in a 52mm diameter, however with the extra pins and mount points, I ended up with a 57mm sized gauge (57mm is the size of the climate control dials). 
 * For the screen, I chose Adafruit's [OLED Breakout Board - 16-bit Color 1.27" w/microSD holder](https://www.adafruit.com/product/1673), which is large enough to be easily visible and small enough to fit my 57mm gauge. 
 * For control, I chose a Raspberry Pi Zero. Running a Linux OS instead of directly on a board was just a faster way to get all my components together.
 * To interface to the car, I have a USB ELM327 
 * To cycle between PIDs, I'm using a rotary encoder
 * To power the board in the car, I'm using [Mausberry's 4AMP CAR SUPPLY / SWITCH](https://mausberry-circuits.myshopify.com/collections/frontpage/products/4amp-car-supply-switch). This is a pretty slick board that attaches to the car's 12V feeds, both constant and switched, to check if the car is on and send power accordingly

## Software
As a C/C++ guy, I chose Python for this project. Why? Primarily because there are tons of existing libraries out there to do what I need done. Those libraries primarily being [Adafruit's](https://learn.adafruit.com/adafruit-1-5-color-oled-breakout-board?view=all) to control their OLED and [python-OBD](https://python-obd.readthedocs.io/en/latest/) to interface with the ELM327 over USB.
The software is setup with a Model-View-Controller pattern. The controller `trixie.py` creates a model `trixie-model.py` to get the data from the ELM327. The controller then pipes that data to the view `trixie-view.py`, which manages the OLED to display the data. This decouples the logic so I can swap in different models or different views (see Future Work below) with ease.

## Setup
As I looked for the fastest way to boot a Raspberry Pi, I came across [DietPi](https://dietpi.com/). I'm always looking for different Linux distros, so I gave it a shot. 

### OS Setup
I used [DietPi's Raspberry Pi 32 bit image](https://dietpi.com/downloads/images/DietPi_RPi-ARMv6-Buster.7z) and [Balena's Etcher](https://www.balena.io/etcher/) software to flash an 8GB SD card. Before you install the SD card, you will need to edit the `/boot/config.txt` to enable SPI, as DietPi does not have an option to do that internally. Edit the SPI line as shown below
```
#-------SPI-------------
dtparam=spi=on
```
Once booted and logged in (I logged in as `root`), DietPi should ask you to configure your setup, which you can access via
```
dietpi-config
```
If your network wasn't setup on first boot, it will probably complain about trying to connect to the network. Use `DietPi-Config` to configure the network setup, then `Retry` so it can pull the latest updates. The setup will ask some questions, and eventually end on a page about installing additional software. You can just hit `<OK>` at the bottom, and confirm you want to start with a minimal image. Once finished, you can configure the following options for fast boot and our startup from `DietPi-Config`.
 * Advanced Options-> Time sync mode -> Custom. No need to sync the clock, the time sync requires internet to sync and we won't always have it in the car. And this will block the boot sequence
 * Network Options: Misc -> Boot Net Wait -> Disabled. 
 * AutoStart Options -> Custom. We will use a script to launch our app.

Now we just need `git` to grab the repo
```
sudo apt install git
```
We can now setup the software

### Software Setup
The first step would be to clone this repo
```
git clone https://github.com/nstanley/trixie-digital-gauge.git
cd trixie-digital-gauge
```
To get all the necessary libraries, you can use the `get-deps.sh` script
```
sudo bash get-deps.sh
```
This will install support packages used by the gauge. You should now be able to run the gauge
```
python3 code/trixie.py
```
If you don't have this wired in the car, it should attempt to connect to the car, fail 7 times, then run a simple demo. If you see `Demo: Connected!` and it is still running, then everything is installed and setup.

The final step is to setup the autostart script. I have setup a necessary script at `resources/autostart.sh`
```
cp resources/autostart.sh /var/lib/dietpi/dietpi-autostart/custom.sh
chmod 777 /var/lib/dietpi/dietpi-autostart/custom.sh
```
Final check - reboot and verify the same output as the initial test above, but from the start without any user interaction. The demo is set to run for a short time and then stop, which would send the script to the following `poweroff` command (assuming this was in a car, we shutdown once we exit the gauge).

### Hardware setup

### Future work
I came across an awesome [Hackster.io post](https://www.hackster.io/databus100/digital-speedometer-to-car-s-instrument-cluster-via-can-bus-66e273) about sending data to the existing LCD screen in the TT, as if it were the radio. The Hackster post describes a system with the "new" CAN interface, but I'm lucky enough to have the earlier interface described by the [inspiration for the post](https://github.com/derpston/Audi-radio-DIS-reader). I have parts on order to try to tap into that interface.

## Resources
 * https://en.wikipedia.org/wiki/OBD-II_PIDs
 * https://python-obd.readthedocs.io/en/latest/
 * https://github.com/guyc/py-gaugette
 * https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/spi-sensors-devices
 * https://learn.adafruit.com/adafruit-1-5-color-oled-breakout-board?view=all
 * https://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi?view=all
 * https://www.dafont.com/seven-segment.font