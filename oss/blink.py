#!/usr/bin/env python2

import RPi.GPIO as gpio
import time
import random
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('-datafile',  type=str)
parser.add_argument('-start',  type=float)
parser.add_argument('-RatID',  type=str)
parser.add_argument('-interval',  type=int)
args=parser.parse_args()
print ("\n")
print ("\n")
print (args.datafile)
print (args.RatID)
print (args.start )
print ("\n")

idfile=open("/home/pi/boxid")
boxid=idfile.read()
boxid=boxid.strip()

# green and red LEDs are for sensation seeking
greenLed=7
redLed=11
houseLight1=33
houseLight2=37
pins=[greenLed,redLed]

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
gpio.setup(greenLed, gpio.OUT)
gpio.setup(redLed, gpio.OUT)
gpio.setup(houseLight1, gpio.OUT)
gpio.setup(houseLight2, gpio.OUT)

## blinks the green LED and/or red LED at a randomly selected frequency for a randomly selected time period, repeat 1-3 times
def blink(pins):
	whichpin=random.randint(0,3)
	if whichpin==0:
		pin=[pins[0]]
		Pin="Red"
	elif whichpin==1:
		pin=[pins[1]]
		Pin="Green"
	elif whichpin==2:
		pin=pins
		Pin="Both"
	else:
		pin=[pins[0],pins[1],9] # 9 = blink alternatively 
		Pin="Alt."
	numTimes=random.randint(1,3)
	speed=random.randint(1,9)/float(18)
	lapsed=time.time()-args.start
	# which house light to turn off?
	hL=1
	if random.randint(0,9)< 5 :
		hL=0
		print "blink house lights"
		for i in range (0, random.randint(2,4)):
			print (str(i))
			gpio.output(houseLight1,False)
			gpio.output(houseLight2,False)
			time.sleep(random.randint(1,4)/float(8))
			gpio.output(houseLight1,True)
			gpio.output(houseLight2,True)
			time.sleep(random.randint(1,4)/float(8))
	if len(pin)==3:
		print ("blink pins alternately "+str(pin)+" for "+str(numTimes)+" times at "+str(speed) + " speed") 
		for i in range(0,numTimes):
			gpio.output(pin[0],True)
			time.sleep(speed)
			gpio.output(pin[0],False)
			gpio.output(pin[1],True)
			time.sleep(speed)
			gpio.output(pin[1],False)
			time.sleep(speed)
	elif len(pin)==2:
		print ("blink both pins "+str(pin)+" for "+str(numTimes)+" times at "+str(speed) + " speed") 
		for i in range(0,numTimes):
			gpio.output(pin[1],True)
			gpio.output(pin[0],True)
			time.sleep(speed)
			gpio.output(pin[0],False)
			gpio.output(pin[1],False)
			time.sleep(speed)
	else:
		print ("blink pin "+str(pin[0])+" for "+str(numTimes)+" times at "+str(speed) + " speed") 
		for i in range(0,numTimes):
			gpio.output(pin[0],True)
			time.sleep(speed)
			gpio.output(pin[0],False)
			time.sleep(speed)
	houseOff=random.randint(0,args.interval) ## house light off is no longer than inteval
	time.sleep(houseOff)
	gpio.output(houseLight1,True)
	gpio.output(houseLight2,True)
#	pin=str(pin)
#	pin=str.replace(pin, ",",":") # comma in data file causes confusion with the csv format
#	pin=str.replace(pin, "7: 11: 9","both")
#	pin=str.replace(pin, "11","red") # replace pin with LED color
#	pin=str.replace(pin, "7","green")
	with open(args.datafile,"a") as f:
		f.write(args.RatID+"\treward\t" + time.strftime("%Y-%m-%d\t%H:%M:%S", time.localtime()) + "\t" + str(lapsed) + "\t" +  boxid + "\t" + Pin + "\t" + str(numTimes) + "\t" + str(speed) + "\t" + str(args.interval) + "\t" + str(hL) + "\t" + str(houseOff) + "\n")
		f.close()

blink(pins)
