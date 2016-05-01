#!/usr/bin/env pyhon2

import RPi.GPIO as gpio
import serial
import time
#import os
#import sys
import subprocess
#import random

def ReadRFID(path_to_sensor) :
	baud_rate = 9600 
	time_out = 0.05
	uart = serial.Serial(path_to_sensor, baud_rate, timeout = time_out)
	uart.close()
	uart.open()
	uart.flushInput()
	uart.flushOutput()
	print(path_to_sensor + " initiated")
	Startflag = "\x02"
	Endflag = "\x03"
	while True:
		Zeichen = 0
		Tag = 0
		ID = ""
		Zeichen = uart.read()
		if Zeichen == Startflag:
			for Counter in range(13):
				Zeichen = uart.read()
				ID = ID + str(Zeichen)
			ID = ID.replace(Endflag, "" ) 
			print "RFID  detected: "+ ID
			return (ID)

def doneSignal():
	while True:
		motionLight=31
		gpio.output(touchLed,True)
		gpio.output(motionLight,False)
		time.sleep(1)
		gpio.output(touchLed,False)
		gpio.output(motionLight,True)
		time.sleep(1)

if __name__ == '__main__':
	sessionLength=1800
	# disable python automatic garbage collection for greater sensitivity
	# session LEDs are on when data are being recorded. These LEDs are located at the end of the head poke holes and serve to attract the attension of the rats. 
	# touchLed is on when touch sensor is activated  
	# green and red Leds are for sensation seeking
	touchLed=35 
	# setting up the various LEDs.
	gpio.setwarnings(False)
	gpio.setmode(gpio.BOARD)
	gpio.setup(touchLed,gpio.OUT)
	gpio.output(touchLed,True) ## borrow the touch LED to indicate program stared
	RatID=ReadRFID("/dev/ttyUSB0")
	gpio.output(touchLed,False)
	subprocess.call("sudo python /home/pi/openbehavior/oss/motion.py " + " -RatID " + RatID, shell=True)
        doneSignal()
	subprocess.call('/home/pi/openbehavior/wifi-network/rsync.sh')



