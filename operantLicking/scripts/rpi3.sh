#!/bin/bash

# Associative array storing revisions
declare -A revisions
revisions["0002"]=1
revisions["0003"]=1
revisions["0004"]=1
revisions["0005"]=1
revisions["0006"]=1
revisions["0007"]=1
revisions["0008"]=1
revisions["0009"]=1
revisions["000d"]=1
revisions["000e"]=1
revisions["000f"]=1
revisions["0010"]=1
revisions["0013"]=1
revisions["0011"]=1
revisions["0012"]=1
revisions["a01041"]=2
revisions["a21041"]=2
revisions["900092"]=0
revisions["a02082"]=3
revisions["a22082"]=3

function getRaspberryPiVersion {
	REVISION="$(cat /proc/cpuinfo | grep Revision | cut -f 2 | tr -d ": " | head -n 1)"
	return ${revisions[$REVISION]}	
}

getRaspberryPiVersion

if [ "$?" == "3" ] ; then
	# Update the boot config
	echo "bluetooth disabled; please reboot."
	echo "dtoverlay=pi3-disable-bt" >>/boot/config.txt
	systemctl disable hciuart
else
	echo "Not RPi 3, nothing is done."
fi

