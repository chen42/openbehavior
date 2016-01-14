#!/usr/bin/python

import serial
import sys
import time
import operator

# path to data file
datafile = "/home/pi/Sync/rfidreader.log"

# UART data
idstring = ""
chardata = 0
checksum = 0
tag = 0

# flags
startflag = "\x02"
endflag = "\x03"

# open the reader through UART
UART = serial.Serial("/dev/ttyAMA0", 9600)
UART.close()
UART.open()

# Main program loop
while True:
	# zero out the variables
	checksum = 0
	tag = 0
	idstring = ""
	# read in a character
	chardata = UART.read()
	# Is it the start flag?
	if chardata == startflag:
		# concatenate id together
		for i in range(13):
			chardata = UART.read()
			idstring = idstring + str(chardata)
		# remove end flag from the string
		idstring = idstring.replace(endflag, "")
		# calculate checksum
		for i in range(0, 9, 2):
			checksum = checksum ^ (((int(idstring[i], 16)) << 4) + int(idstring[i+1], 16))
		checksum = hex(checksum)
		# filter tag
		tag = ((int(idstring[1], 16) << 8) + ((int(idstring[2], 16)) << 4) + ((int(idstring[3], 16)) << 0)
		tag = hex(tag)
		print "ID: ", idstring
		with open(datafile, "a") as f:
			f.write(time.strftime("%Y-%m-%d\t%H:%M:%S\t") + idstring + "\n")
		f.close()
		UART.flushInput()
