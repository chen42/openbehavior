import os
import time
from time import strftime, localtime
import sys
import RPi.GPIO as gpio
from random import randint
import serial
from operator import xor 
import multiprocessing


sessionLength=3600
start=time.time()
datafile='/home/pi/oss_'+ time.strftime("%Y-%m-%d_%H:%M:%S", localtime())+".csv"

green=11
red=7
sessionLed=36
pins=[green,red]

gpio.setmode(gpio.BOARD)
gpio.setup(green, gpio.OUT)
gpio.setup(red, gpio.OUT)
gpio.setup(sessionLed,gpio.OUT)
gpio.output(red,False)
gpio.output(green,False)

UART = serial.Serial("/dev/ttyAMA0", 9600) 
UART.close()
UART.open()


with open(datafile,"a") as f:
	f.write("#Session Started on " +time.strftime("%Y-%m-%d\t%H:%M:%S\t", localtime())+"\n")
	f.close()


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
	gpio.output(sessionLed,False)
	if len(pin)==3:
		print ("blink  pins alternativly "+str(pin)+" for "+str(numTimes)+" times at "+str(speed) + " speed") 
		for i in range(0,numTimes):
			time.sleep(speed)
			gpio.output(pin[0],True)
			time.sleep(speed)
			gpio.output(pin[0],False)
			gpio.output(pin[1],True)
			time.sleep(speed)
			gpio.output(pin[1],False)
	elif len(pin)==2:
		print ("blink both pins "+str(pin)+" for "+str(numTimes)+" times at "+str(speed) + " speed") 
		for i in range(0,numTimes):
			time.sleep(speed)
			gpio.output(pin[1],True)
			gpio.output(pin[0],True)
			time.sleep(speed)
			gpio.output(pin[0],False)
			gpio.output(pin[1],False)
	else:
		print ("blink pin "+str(pin)+" for "+str(numTimes)+" times at "+str(speed) + " speed") 
		for i in range(0,numTimes):
			time.sleep(speed)
			gpio.output(pin[0],True)
			time.sleep(speed)
			gpio.output(pin[0],False)
	gpio.output(sessionLed,True)
	return {'pins':pin, 'times':numTimes, 'speed':speed}

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
		lapsed=time.time()-start
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
			print ("RFID detected: ", ID, " lapsed ", lapsed)
			para=blink(pins)
			with open(datafile,"a") as f:
					f.write("active\t"+time.strftime("%Y-%m-%d\t%H:%M:%S\t", localtime())+"\t"+str(lapsed)+"\t"+ID+"\t"+str(para['pins'])+"\t"+str(para['times'])+"\t"+str(para['speed'])+"\n")
			f.close()
			UART.flushInput()
			time.sleep(5)


if __name__ == '__main__':
	p=multiprocessing.Process(target=activerfid, name="Active")
	gpio.output(sessionLed,True)
	p.start()

	time.sleep(sessionLength)
	gpio.output(sessionLed,False)
	p.terminate()
	p.join()


