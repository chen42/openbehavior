#!/bin/sh

# introduce a small random delay so that the server does not get too much requrest at the same time.
delay=`shuf -i1-3 -n1` 

# make sure wlan0 is up
ifconfig wlan0 up
while [ `sudo ifconfig wlan0 |grep Bcast |wc -l` -ne 1 ]
	do
	sleep 2
	cnt=$[$cnt+1]
	if [ $cnt -eq 30 ] # max 60 sec  
		then 
			break
	fi
done

# remove files older than 30 days
rm `find /home/pi/Pies/* -mtime +30` 

rsync -az -e ssh /home/pi/Pies/ root@149.56.128.122:~/Dropbox/Pies/  


