#!/bin/bash

# introduce a small random delay so that the server does not get too many requrests at the same time.
delay=`shuf -i1-3 -n1` 

# make sure wlan0 is up
ifconfig wlan0 up
while [ `sudo ifconfig wlan0 |grep broadcast |wc -l` -ne 1 ]
	do
	sleep 2
	cnt=$[$cnt+1]
	if [ $cnt -eq 30 ] # max 60 sec  
		then 
			break
	fi
done

# remove files older than 15 days
rm `find /home/pi/SocialDrinking/* -mtime +15` 

gzip -f /home/pi/SocialDrinking/*csv

rsync -auvp -e ssh /home/pi/SocialDrinking/ root@149.56.128.122:~/Dropbox/Pies/SocialDrinking/ 
sleep 1m
#sync one more time
rsync -auvp -e ssh /home/pi/SocialDrinking/ root@149.56.128.122:~/Dropbox/Pies/SocialDrinking/ 

sudo reboot

