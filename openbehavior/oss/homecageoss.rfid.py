import RPi.GPIO as gpio
import time
from random import randint
import os

import sys
import time
import Adafruit_MPR121.MPR121 as MPR121




import serial
from operator import xor 



start=time.time()

green=11
red=7
pins=[green,red]

gpio.setmode(gpio.BOARD)
gpio.setup(green, gpio.OUT)
gpio.setup(red, gpio.OUT)
gpio.output(red,False)
gpio.output(green,False)

def blink(pins):
	whichpin=randint(0,3)
	if whichpin==0:
		pin=[pins[0]]
	elif whichpin==1:
		pin=[pins[1]]
	elif whichpin==2:
		pin=pins
	else:
		pin=[pins[0],pins[1],9]

	numTimes=randint(1,3)
	speed=randint(1,9)/float(9)

	if len(pin)==3:
		print ("blink  pins alternativly "+str(pin)+" for "+str(numTimes)+" times at "+str(speed) + "speed") 
		for i in range(0,numTimes):
			time.sleep(speed)
			gpio.output(pin[0],True)
			time.sleep(speed)
			gpio.output(pin[0],False)
			gpio.output(pin[1],True)
			time.sleep(speed)
			gpio.output(pin[1],False)
	elif len(pin)==2:
		print ("blink both pins "+str(pin)+" for "+str(numTimes)+" times at "+str(speed) + "speed") 
		for i in range(0,numTimes):
			time.sleep(speed)
			gpio.output(pin[1],True)
			gpio.output(pin[0],True)
			time.sleep(speed)
			gpio.output(pin[0],False)
			gpio.output(pin[1],False)
	else:
		print ("blink pin "+str(pin)+" for "+str(numTimes)+" times at "+str(speed) + "speed") 
		for i in range(0,numTimes):
			time.sleep(speed)
			gpio.output(pin[0],True)
			time.sleep(speed)
			gpio.output(pin[0],False)
	return {'pins':pin, 'times':numTimes, 'speed':speed}


cap = MPR121.MPR121()
if not cap.begin():
    print 'Error initializing MPR121.  Check your wiring!'
    sys.exit(1)



def active():
#last_touched = cap.touched()
	while True:
	#	current_touched = cap.touched()
		# Check each pin's last and current state to see if it was pressed or released.
		if cap.is_touched(1):
			lapsed=time.time()-start
			para=blink(pins)
			print (lapsed,para['pins'],para['times'],para['speed'])
			with open("oss.data.csv","a") as f:
				f.write("active"+"\t"+str(lapsed)+"\t"+str(para['pins'])+"\t"+str(para['times'])+"\t"+str(para['speed'])+"\n")
			time.sleep(0.02)

UART = serial.Serial("/dev/ttyAMA0", 9600) 
UART.close();
UART.open()
def activerfid():
	while True:
		# UART
		ID = ""
		Zeichen = 0
		Checksumme = 0
		Tag = 0
		# Flags
		Startflag = "\x02"
		Endflag = "\x03"
		# UART oeffnen

		Zeichen = UART.read()
		if Zeichen == Startflag:
			for Counter in range(13):
				Zeichen = UART.read()
				ID = ID + str(Zeichen)
			ID = ID.replace(Endflag, "" ) # Checksumme berechnen
			for I in range(0, 9, 2):
				Checksumme = Checksumme ^ (((int(ID[I], 16)) << 4) + int(ID[I+1], 16))
			Checksumme = hex(Checksumme)
			Tag = ((int(ID[1], 16)) << 8) + ((int(ID[2], 16)) << 4) + ((int(ID[3], 16)) << 0) 
			Tag = hex(Tag)
			print "RFID detected: ", ID
			lapsed=time.time()-start
			para=blink(pins)
			time.sleep(1)
			UART.flushInput()
			print (lapsed,para['pins'],para['times'],para['speed'])
			with open("oss.data.csv","a") as f:
				f.write("rfidactive"+"\t"+str(lapsed)+"\t"+str(para['pins'])+"\t"+str(para['times'])+"\t"+str(para['speed'])+"\n")


			#print "Tag: ", Tag
			#print "ID: ", ID[4:10], " - ", int(ID[4:10], 16)
			#print "Checksumme: ", Checksumme
			#print "------------------------------------------"


def inactive():
	while True:
		if cap.is_touched(0):
			lapsed=time.time()-start
			with open("oss.data.csv","a") as f:
				f.write("inactive"+"\t"+str(lapsed)+"\n")
			time.sleep(0.02)

pid=os.fork()

while True:
	if pid >0:
		activerfid()
		#active()
	else:
		inactive()
