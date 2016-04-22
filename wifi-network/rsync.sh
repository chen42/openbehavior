#!/bin/sh
delay=`shuf -i1-10 -n1`
sleep $delay
rsync -az -e ssh /home/pi/Pies/ root@149.56.128.122:~/Dropbox/Pies/  


