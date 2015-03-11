#!/bin/sh
ACTION=$(expr "ACTION" : "\([a-zA-Z]\+\).*")
if [ "$ACTION" = "add" ]
then
	mount /mnt/usb
	# Copy log files to /mnt/usb/
	cp /home/pi/behaviorRoomEnv.log /mnt/usblog/behaviorRoomEnv.log
	# Blink RPi LED
	echo none > /sys/class/leds/led0/trigger
	echo 1 > /sys/class/leds/led0/brightness
	sleep 1
	echo 0 > /sys/class/leds/led0/brightness
	sleep 1
	echo 1 > /sys/class/leds/led0/brightness
	sleep 2
	echo 0 > /sys/class/leds/led0/brightness
	sleep 2
	echo 1 > /sys/class/leds/led0/brightness
	sleep 1
	echo 0 > /sys/class/leds/led0/brightness
	sleep 1
	echo 1 > /sys/class/leds/led0/brightness
	sleep 1
	echo 0 > /sys/class/leds/led0/brightness
	sleep 1
	echo 1 > /sys/class/leds/led0/brightness
	sleep 1
	# Turn back on normal SD card trigger for LED 
	echo mmc0 > /sys/class/leds/led0/trigger
else
	umount /mnt/usb
fi
