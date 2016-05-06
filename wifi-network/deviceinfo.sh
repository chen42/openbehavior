#!/bin/bash

year=`date |cut -d " " -f 7 ` 
if [ "$year" -lt "2016" ] 
	then
		date -s "Fri May 6 1:01:01 CDT 2016"
		htpdate -s www.freebsd.org www.linux.org www.google.com	
		hwclock -w
fi

date >>/home/pi/Pies/DeviceInfo/`cat /home/pi/deviceid`.info
cat /home/pi/deviceid >>/home/pi/Pies/DeviceInfo/`cat /home/pi/deviceid`.info
ifconfig wlan0 >>/home/pi/Pies/DeviceInfo/`cat /home/pi/deviceid`.info
ifconfig eth0 >>/home/pi/Pies/DeviceInfo/`cat /home/pi/deviceid`.info
echo "_______________________________" >>/home/pi/Pies/DeviceInfo/`cat /home/pi/deviceid`.info


