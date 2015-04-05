#!/bin/sh

## NOTE: pigpoid can be found here: wget abyz.co.uk/rpi/pigpio/pigpio.zip
## need to install the following:
## enable I2C: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
## install Adafruit library for the MCP9808 https://learn.adafruit.com/mcp9808-temperature-sensor-python-library/software

## The following commands need to be run before the env log file

sudo chmod 666   /sys/module/i2c_bcm2708/parameters/combined
sudo echo -n 1 > /sys/module/i2c_bcm2708/parameters/combined
sudo pigpiod

## Setup our DS1307 Clock
./setup_ds1307.sh
