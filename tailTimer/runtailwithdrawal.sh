#!/bin/bash

echo ""
echo "------------------------"
echo "Current date and time is "
echo "------------------------"
date 

echo "Is that correct? (Y/n)? " 
read ch
if [ $ch = 'n' ] ; then 
	echo "Enter the date the following format: yyyy-mm-dd"
	read dt
	sudo date +%Y-%m-%d -s "$dt"
	echo "Enter the current time in the following format: hh:mm:ss" 
	read dt 
	sudo date --set="$dt"
fi

sudo python /home/pi/openbehavior/tailwithdrawal/tailwithdrawal.py 

echo "--------------------------------"
echo "Please plug in a usb drive, click on \"cancel\" when a window pops up, press entery to copy the data"
echo "--------------------------------"
read dummy 
sudo umount /dev/sda1
sudo mount /dev/sda1 /home/pi/usbDrive
sudo cp /home/pi/Pies/tailwithdrawal/* /home/pi/usbDrive/ -v


