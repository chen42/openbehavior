#!/bin/sh

# introduce a small random delay so that the server does not get too much requrest at the same time.
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

# remove files older than 30 days
rm `find /home/pi/Pies/* -mtime +30` 

gzip /home/pi/SocialDrinking/*csv
rsync -auvp -e ssh /home/pi/SocialDrinking/ root@149.56.128.122:~/Dropbox/Pies/SocialDriking/ 
for i in {1..5}; do
	echo "sleep $i min"
	sleep ${i}s
	rsync -auvp -e ssh /home/pi/SocialDrinking/ root@149.56.128.122:~/Dropbox/Pies/SocialDriking/ 
done



