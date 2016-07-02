#!/bin/sh

# introduce a small random delay so that the server does not get too much requrest at the same time.
delay=`shuf -i1-10 -n1` 
sleep $delay

# remove files older than 30 days
rm `find /home/pi/Pies/* -mtime +30` 

rsync -az -e ssh /home/pi/Pies/ root@149.56.128.122:~/Dropbox/Pies/  


