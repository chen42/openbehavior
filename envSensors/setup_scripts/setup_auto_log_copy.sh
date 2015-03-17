# create usb UDEV rules for running script when USB drive is plugged in.
sudo echo 'SUBSYSTEMS=="usb", KERNEL=="sd[a-h]", SYMLINK+="usbkey", RUN+="/home/pi/autocopylogs.sh" SUBSYSTEMS=="usb",KERNEL=="sd[a-h]",ACTION=="remove", RUN+="/home/pi/autocopylogs.sh"' > /etc/udev/rules.d/999-env-autologging.rules
sudo echo 'SUBSYSTEMS=="usb", KERNEL=="sd[a-h]1", SYMLINK+="usbkey", RUN+="/home/pi/autocopylogs.sh" SUBSYSTEMS=="usb",KERNEL=="sd[a-h]1",ACTION=="remove", RUN+="/home/pi/autocopylogs.sh"' >> /etc/udev/rules.d/999-env-autologging.rules


# create shell script for copying files to usb drive from /home/pi/
OUTPUTDIR=/home/pi/autocopylogs.sh
LOGFILESRC=/home/pi/behaviorRoomEnv.log
LOGFILEDEST=/mnt/usblog/behaviorRoomEnv.log
sudo echo '#!/bin/sh' > $OUTPUTDIR
sudo echo 'ACTION=$(expr "ACTION" : "\([a-zA-Z]\+\).*")' >> $OUTPUTDIR 
sudo echo 'if [ "$ACTION" = "add" ]' >> $OUTPUTDIR
sudo echo 'then' >> $OUTPUTDIR
sudo echo '	mount /mnt/usb' >> $OUTPUTDIR
sudo echo "	# Copy log files to /mnt/usb/" >> $OUTPUTDIR
sudo echo	"	cp $LOGFILESRC $LOGFILEDEST" >> $OUTPUTDIR
sudo echo "	# Blink RPi LED" >> $OUTPUTDIR
sudo echo "	# Turn off Default SD Card blinking mechanisms" >> $OUTPUTDIR
sudo echo "	echo none > /sys/class/leds/led0/trigger" >> $OUTPUTDIR
sudo echo	"	echo 1 > /sys/class/leds/led0/brightness" >> $OUTPUTDIR
sudo echo "	sleep 1" >> $OUTPUTDIR
sudo echo "	echo 0 > /sys/class/leds/led0/brightness" >> $OUTPUTDIR
sudo echo "	sleep 1" >> $OUTPUTDIR
sudo echo "	echo 1 > /sys/class/leds/led0/brightness" >> $OUTPUTDIR
sudo echo "	sleep 2" >> $OUTPUTDIR
sudo echo "	echo 0 > /sys/class/leds/led0/brightness" >> $OUTPUTDIR
sudo echo "	sleep 2" >> $OUTPUTDIR
sudo echo "	echo 1 > /sys/class/leds/led0/brightness" >> $OUTPUTDIR
sudo echo "	sleep 1" >> $OUTPUTDIR
sudo echo "	echo 0 > /sys/class/leds/led0/brightness" >> $OUTPUTDIR
sudo echo "	sleep 1" >> $OUTPUTDIR
sudo echo "	echo 1 > /sys/class/leds/led0/brightness" >> $OUTPUTDIR
sudo echo "	sleep 1" >> $OUTPUTDIR
sudo echo "	echo 0 > /sys/class/leds/led0/brightness" >> $OUTPUTDIR
sudo echo "	sleep 1" >> $OUTPUTDIR
sudo echo "	echo 1 > /sys/class/leds/led0/brightness" >> $OUTPUTDIR
sudo echo "	sleep 1" >> $OUTPUTDIR
sudo echo "	# Turn back on normal SD card trigger for LED " >> $OUTPUTDIR
sudo echo "	echo mmc0 > /sys/class/leds/led0/trigger" >> $OUTPUTDIR
sudo echo 'else' >> $OUTPUTDIR
sudo echo '	umount /mnt/usb' >> $OUTPUTDIR
sudo echo 'fi' >> $OUTPUTDIR


# Create directory for mounting usb drive
sudo mkdir /mnt/usblog

# Add entry into fstab to automount usb devices to /mnt/usblog
# TODO: Make this smarter and make it so that only one such entry exists in our fstab
echo "/dev/usbkey /mnt/usblog vfat ro,noauto,user,exec 0 0" >> /etc/fstab
