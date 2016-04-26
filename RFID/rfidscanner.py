#!/usr/bin/python

import serial
import sys
import time
import datetime
import operator
import Adafruit_CharLCD

# CONSTANTS
# path to data file

idfile=open("/home/pi/deviceid")
device=idfile.read()
device=device.strip()
today=datetime.date.today()
td=str(today)+"\n"
year=datetime.date.today().year
month=datetime.date.today().month
datafile="/home/pi/Pies/RFIDReader/"+device+"_"+str(year)+"-"+str(month)+".log"
# flags
startflag = "\x02"
endflag = "\x03"

def printIDtoLCD(lcd, idstring):
	lcd.clear()
	lcd.message(td)
        lcd.message("Tag Found!\n")
	time.sleep(.5)
	lcd.clear()
        lcd.message(td)
        lcd.message("ID:"+ idstring)
	

def main():
	# UART data
	idstring = ""
	chardata = 0
	
	# initialize the LCD
	lcd = Adafruit_CharLCD.Adafruit_CharLCD()
	lcd.begin(16,1)
	lcd.clear()
	lcd.message("a posse ad esse\n")
	lcd.message(td)
	time.sleep(2)
	
	# open the reader through UART
	UART = serial.Serial("/dev/ttyAMA0", 9600)
	UART.close()
	UART.open()
	
	# Instruct the user that the scanner is ready to read
	lcd.clear()
	lcd.message("Ready to scan!")
	
	# Main program loop
	while True:
		time.sleep(0.25)
		# zero out the variables
		tag = 0
		idstring = ""
		# read in a character
		chardata = UART.read()
		# Is it the start flag?
		if chardata == startflag:
			# concatenate id together
			for i in range(12):
				chardata = UART.read()
				idstring = idstring + str(chardata)
			printIDtoLCD(lcd, idstring)
			with open(datafile, "a") as f:
				f.write(time.strftime("%Y-%m-%d\t%H:%M:%S\t") + idstring + "\n")
			f.close()
			UART.flushInput()

main()
