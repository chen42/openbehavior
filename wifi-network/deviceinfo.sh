#!/bin/bash

date >>/home/pi/Pies/DeviceInfo/`cat /home/pi/deviceid`.info
cat /home/pi/deviceid >>/home/pi/Pies/DeviceInfo/`cat /home/pi/deviceid`.info
ifconfig wlan0 >>/home/pi/Pies/DeviceInfo/`cat /home/pi/deviceid`.info
ifconfig eth0 >>/home/pi/Pies/DeviceInfo/`cat /home/pi/deviceid`.info
echo "_______________________________" >>/home/pi/Pies/DeviceInfo/`cat /home/pi/deviceid`.info


