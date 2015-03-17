#!/bin/sh

## This script is meant to be run once in order to setup a connected ds1307 adafruit RTC module.

# Step 1: Add the RTC-DS1307 to our list of modules
echo "rtc-ds1307" >> /etc/modules

# Step 2: Create our ds-1307 as a device on Raspberry Pi boot
echo "echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device" >> /etc/rc.local
echo "sudo hwclock -s" >> /etc/rc.local
