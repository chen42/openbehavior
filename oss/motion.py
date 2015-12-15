#!/usr/bin/env python2

import RPi.GPIO as gpio
import time
import os
import sys

sessionLength=1800
pirPin=12
motionLed=31
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(pirPin, gpio.IN)        
gpio.setup(motionLed, gpio.OUT)        

## create data files, Each box has its own ID
idfile=open("/home/pi/boxid")
boxid=idfile.read()
boxid=boxid.strip()
startTime=time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
start=time.time()
motionDataFile='/home/pi/pies/motion/mot'+ boxid + "_" + startTime + ".csv"
with open(motionDataFile,"a") as f:
	f.write("#Session Started on " +time.strftime("%Y-%m-%d\t%H:%M:%S\t", time.localtime())+"\n")
	f.write("RatID\tdate\tboxid\tseconds\n")
	f.close()

while time.time()-start < sessionLength:
	if gpio.input(pirPin):
		#print time.strftime("%Y-%m-%d\t%H:%M:%S")
		with open(motionDataFile,"a") as f:
			lapsed=time.time()-start
			f.write(time.strftime("%Y-%m-%d\t", time.localtime()) + boxid +"\t"+ str(lapsed) +"\n")
			f.close()
		gpio.output(motionLed, True)
		time.sleep(0.5)
		gpio.output(motionLed, False)
		time.sleep(0.5)

with open(motionDataFile, "a") as f:
	f.write("#session Ended at " + time.strftime("%H:%M:%S", time.localtime())+"\n")
	f.close



