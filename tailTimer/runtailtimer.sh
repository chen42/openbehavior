#!/bin/bash

echo "------------------------"
echo "Please write down the data and time shown above if it is not correct!" 
echo "-----------------------------------------------------------"
python /home/pi/openbehavior/tailTimer/tailwithdrawal.py 

echo ""
echo "--------------------------------"
echo "Please plug in a usb drive, enter anything to continue"
echo "--------------------------------"
echo ""
read dummy 
sudo mount /dev/sda1 /home/pi/usbDrive
echo ""
echo ""
echo "START COPYING FILES"
sudo cp /home/pi/Pies/tailwithdrawal/* /home/pi/usbDrive/ -v
echo "FILES COPIED"
sudo umount /dev/sda1
echo "PLEASE REMOVE THE USB DRIVE"


