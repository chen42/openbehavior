#!/bin/bash


# wait for wifi connection before run htpdate (because ntp is blocked on my network
# then set hwclock

## make sure wlan0 is up
sudo ifconfig wlan0 up

while [ `sudo ifconfig wlan0 |grep Bcast |wc -l` -ne 1 ]
	do
	sleep 2
	cnt=$[$cnt+1]
	echo "waiting $cnt"
	if [ $cnt -eq 10 ] # max 20 sec  
		then 
			sudo ifconfig wlan0 down # disconnect wifi if not connected
			echo "Give up on wifi"
			break
	fi
done

echo "Sync time with the internet"
sudo htpdate  -t -s www.ntp.org www.uthsc.edu www.freebsd.org > /home/pi/htpdateout 	
if grep -v -q ExtBox /home/pi/deviceid ; then 
	if grep -q "Setting.*seconds" /home/pi/htpdateout ; then 
		cat /home/pi/htpdateout
		echo "update hw clock"
		sudo hwclock -w
	else 
		sudo hwclock -s
	fi
fi

date >>/home/pi/Pies/DeviceInfo/`cat /home/pi/deviceid`.info
cat /home/pi/deviceid >>/home/pi/Pies/DeviceInfo/`cat /home/pi/deviceid`.info
ifconfig wlan0 >>/home/pi/Pies/DeviceInfo/`cat /home/pi/deviceid`.info
ifconfig eth0 >>/home/pi/Pies/DeviceInfo/`cat /home/pi/deviceid`.info
echo "_______________________________" >>/home/pi/Pies/DeviceInfo/`cat /home/pi/deviceid`.info

rsync -az -e ssh /home/pi/Pies/ root@149.56.128.122:~/Dropbox/Pies/  


