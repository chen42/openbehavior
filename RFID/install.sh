#!/bin/bash

# Clone the openbehavior repository to the home directory of user 'pi' and
# then run this script with root permissions to install RFID scanner

if [ ! -d "/home/pi/Pies" ]; then
	mkdir "/home/pi/Pies"
	chown pi:users "/home/pi/Pies"
fi

if [ ! -d "/home/pi/Pies/RFIDReader" ]; then
	mkdir "/home/pi/Pies/RFIDReader"
	chown pi:users "/home/pi/Pies/RFIDReader"
fi

cp /home/pi/openbehavior/RFID/rfidscanner.service /etc/systemd/system/rfidscanner.service
systemctl enable rfidscanner.service

