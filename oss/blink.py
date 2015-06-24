import RPi.GPIO as gpio
import time
from time import strftime, localtime
from random import randint
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('-datafile',  type=str)
parser.add_argument('-start',  type=float)
args=parser.parse_args()
print ("\n")
print ("\n")
print (args.datafile)
print (args.start )
print ("\n")

idfile=open("/home/pi/boxid")
boxid=idfile.read()
boxid=boxid.strip()

# green and red Leds are for sensation seeking
greenLed=7
redLed=11
sessionLed1=33
pins=[greenLed,redLed]

gpio.setmode(gpio.BOARD)
gpio.setup(greenLed, gpio.OUT)
gpio.setup(redLed, gpio.OUT)
gpio.setup(sessionLed1, gpio.OUT)

## blinks the greenLed and/or redLed at a randomly selected frequency for a randomly selected time period, repeat 1-3 times
def blink(pins):
	whichpin=randint(0,3)
	if whichpin==0:
		pin=[pins[0]]
	elif whichpin==1:
		pin=[pins[1]]
	elif whichpin==2:
		pin=pins
	else:
		pin=[pins[0],pins[1],9] # 9 = both pins
	numTimes=randint(1,3)
	speed=randint(1,9)/float(9)
	gpio.output(sessionLed1,False)
	if len(pin)==3:
		print ("blink  pins alternativly "+str(pin)+" for "+str(numTimes)+" times at "+str(speed) + " speed") 
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
		print ("blink pin "+str(pin)+" for "+str(numTimes)+" times at "+str(speed) + " speed") 
		for i in range(0,numTimes):
			gpio.output(pin[0],True)
			time.sleep(speed)
			gpio.output(pin[0],False)
			time.sleep(speed)
#	time.sleep(5-speed*numTimes)
	gpio.output(sessionLed1,True)
	pin=str(pin)
	pin=str.replace(pin, ",",":") # comma in data file cause confusion with the csv format
	pin=str.replace(pin, "11","red") # replace pin with LED color
	pin=str.replace(pin, "7","green")
	pin=str.replace(pin, "7, 11, 9","both")
	with open(args.datafile,"a") as f:
		#lapsed=time.time()-args.start
		lapsed=time.time()
		f.write("reward\t" + time.strftime("%Y-%m-%d\t%H:%M:%S", localtime()) + "\t" + str(lapsed) + "\t" +  boxid + "\t" + str(pin) + "\t" + str(numTimes) + "\t" + str(speed) + "\n")
		f.close()

blink(pins)
