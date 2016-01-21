#!/bin/bash

# Clone the openbehavior repository to the home directory of user 'pi' and
# then run this script with root permissions to install RFID scanner

if [ ! -d "/home/pi/Sync" ]; then
	mkdir "/home/pi/Sync"
	chown pi:users "/home/pi/Sync"
fi

if [ ! -e "/home/pi/Sync/rfidreader.log" ]; then
	touch "/home/pi/Sync/rfidreader.log"
	chown pi:users "/home/pi/Sync/rfidreader.log"
fi

cp /home/pi/openbehavior/RFID/rfidscanner.service /etc/systemd/system/rfidscanner.service
systemctl enable rfidscanner.service
