#!/bin/bash


while [ `sudo ifconfig wlan0 |grep Bcast |wc -l` -eq 1 ]
	do
	sleep 1
		echo "turnning off wlan0"
		ifconfig wlan0 down
done

