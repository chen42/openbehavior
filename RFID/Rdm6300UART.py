#!/usr/bin/python

'''
code originally obtained from raspberry pi forum: 
http://www.raspberrypi.org/forums/viewtopic.php?t=59025&p=501603
'''

import serial
import sys
import time
from operator import xor 
# UART
ID = ""
Zeichen = 0
Checksumme = 0
Tag = 0
# Flags
Startflag = "\x02"
Endflag = "\x03"
# UART oeffnen
UART = serial.Serial("/dev/ttyAMA0", 9600) 
UART.close();
UART.open()
while True:
    # Variablen loeschen
	Checksumme = 0
	Checksumme_Tag = 0
	ID = ""
	# Zeichen einlesen
	Zeichen = UART.read()
	# Uebertragungsstart signalisiert worden?
	if Zeichen == Startflag:
	    # ID zusammen setzen
		for Counter in range(13):
			Zeichen = UART.read()
			ID = ID + str(Zeichen)
		# Endflag aus dem String loeschen
		ID = ID.replace(Endflag, "" ) # Checksumme berechnen
		for I in range(0, 9, 2):
			Checksumme = Checksumme ^ (((int(ID[I], 16)) << 4) + int(ID[I+1], 16))
		Checksumme = hex(Checksumme)
		# Tag herausfiltern
		Tag = ((int(ID[1], 16)) << 8) + ((int(ID[2], 16)) << 4) + ((int(ID[3], 16)) << 0) 
                Tag = hex(Tag)
		# Ausgabe der Daten
		print "------------------------------------------"
		print "Datensatz: ", ID
		print "Tag: ", Tag
		print "ID: ", ID[4:10], " - ", int(ID[4:10], 16)
		print "Checksumme: ", Checksumme
		print "------------------------------------------"
