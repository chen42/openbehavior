#openbehavior

This project aims to establish a computing platform for rodent behavior research using the Raspberry Pi computer. We intend to build programs for conducting operant conditioning, as well as some infrared sensor based assays. We also intend to create an environmental sensor set that records the temperature, humidity, air pressure, ambient light, noise level, etc. 

####Data Partition
We anticipate most of our users don't use Linux. To make data accessible on Windows/Mac OS computers, we create a FAT32 partition on the SD card that the Raspberry Pi uses. We plan to save all data into this partition so that users can plug the Raspberry Pi SD card into their computers to copy the data. We will incorporate this into the disk image we will release in the future. For now, here are the steps to create that partition, using [gparted](gparted.org).  You may also need to install the [msdosfs](http://www.freebsd.org/cgi/man.cgi?query=msdosfs&sektion=5&manpath=FreeBSD+8.4-RELEASE) formats package.

```
apt-get install gparted
apt-get install msdosfs
sudo gparted
```

After creating an appropriately sized partition, you'll need to edit the file system tables to force the new partition to mount on boot.  

```
sudo [your favorite text editor] /etc/fstab
```

The fstab file should look something like this:

```
proc            /proc          proc        defaults          0    0
/dev/mmcblk0p1  /boot          vfat        defaults          0    2
/dev/mmcblk0p2  /              ext4        defaults,noatime  0    1
/dev/mmcblk0p3  /home/pi/data  vfat        defaults          0    0
```

In this case, we created a new partition on the Pi SD card alongside the operating system and manually added the /dev/mmcblk0p3 line to the file.  If you're using a different form of removable storage or number of partitions, this name may vary.  The infrared module writes to /home/pi/data, but you can change it if you prefer.  When the Pi reboots, the device will mount to /home/pi/data and the log file will be retrievable from most operating systems. 




