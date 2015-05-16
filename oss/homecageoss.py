# Author: Hao Chen, Ivan Amies
# Home cage operant sensation seeking assay using one raspberry pi to control two RDM6300 RFID readers. 
# Each of the antenna sits on top of a head poking hole. There one LED light at the end of each hole.  
# Upon the active RFID reader detects an RFID, it triggers two additional LED (one green, one red) to flash at a random fashion. 
# Upon the inactive RFID reader detects an RFID, nothing happens. 
# Data recorded include the RFID, light pattern, frequency, times, etc.


import time
import gc
import serial
import RPi.GPIO as gpio
import multiprocessing

from time import strftime, localtime
from operator import xor 
from random import randint

sessionLength=3600
start=time.time()

# Each box has its own ID
idfile=open("/home/pi/ossboxid")
boxid=idfile.read()
boxid=boxid.strip()

datafile='/home/pi/oss'+ boxid + "_" + time.strftime("%Y-%m-%d_%H:%M:%S", localtime()) + ".csv"

# session LEDs are on when data are being recorded. These LEDs are located at the end of the head poke holes and serve to attract the attension of the rats. 
sessionLed1=33
sessionLed2=37
# RFID LED is on when RFID is detected
RFIDLed=35 
# green and red Leds are for sensation seeking
greenLed=11
redLed=7
pins=[greenLed,redLed]

gpio.setmode(gpio.BOARD)
gpio.setup(greenLed, gpio.OUT)
gpio.setup(redLed, gpio.OUT)
gpio.setup(sessionLed1,gpio.OUT)
gpio.setup(sessionLed2,gpio.OUT)
gpio.setup(RFIDLed,gpio.OUT)

gpio.output(redLed,False)
gpio.output(greenLed,False)

# Flags ## DO NOT CHANGE ####
#############################
Startflag = "\x02"
Endflag = "\x03"
#############################
#############################

# intial settings for the file IO
# change as desired all except for the clock 

# initial settings for the uart device. Change as necessary, or read in as desired.#
baud_rate = 9600
# 5 second time out period after each ID is detected.
amount_to_sleep = 5 
time_out = 0.05
###

# open data file
with open(datafile,"a") as f:
	f.write("#Session Started on " +time.strftime("%Y-%m-%d\t%H:%M:%S\t", localtime())+"\n")
	f.close()

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
	gpio.output(36,False)
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
	#gpio.output(RFIDLed,True)
	pin=str(pin)
	pin=str.replace(pin, ",",":") # comma in data file cause confusion with the csv format
	pin=str.replace(pin, "7","red") # replace pin with LED color
	pin=str.replace(pin, "11","green")
	pin=str.replace(pin, "7, 11, 9","both")
	return {'pins':pin, 'times':numTimes, 'speed':speed}


def initialize_uart(path_to_sensor) :
	uart = serial.Serial(path_to_sensor, baud_rate, timeout = time_out)
	uart.close()
	uart.open()
	uart.flushInput()
	uart.flushOutput()
	print(path_to_sensor + " active")
	return uart;

def activerfid(uart):
	while True:
		Zeichen = 0
		Checksumme = 0
		Tag = 0
		ID = ""
		Zeichen = uart.read()
		lapsed=time.time()-start
		if Zeichen == Startflag:
			for Counter in range(13):
				Zeichen = uart.read()
				ID = ID + str(Zeichen)
			ID = ID.replace(Endflag, "" ) # Checksumme berechnen
			#for I in range(0, 9, 2):
			#	Checksumme = Checksumme ^ (((int(ID[I], 16)) << 4) + int(ID[I+1], 16))
			#Checksumme = hex(Checksumme)
			#Tag = ((int(ID[1], 16)) << 8) + ((int(ID[2], 16)) << 4) + ((int(ID[3], 16)) << 0) 
			#Tag = hex(Tag)
			print ("RFID 1 detected: ", ID, " lapsed ", lapsed)
			para=blink(pins)
			with open(datafile,"a") as f:
					f.write("active\t" + time.strftime("%Y-%m-%d\t%H:%M:%S\t", localtime()) + "\t" + str(lapsed) + "\t" + ID + "\t"+ boxid + "\t" + str(para['pins']) + "\t" + str(para['times']) + "\t" + str(para['speed']) + "\n")
			f.close()
			uart.flushInput()
			uart.flushOutput()
			time.sleep(5)

def inactiverfid(uart):
	while True:
		Zeichen = 0
		Checksumme = 0
		Tag = 0
		ID = ""
		Zeichen = uart2.read()
		lapsed=time.time()-start
		if Zeichen == Startflag:
			for Counter in range(13):
				Zeichen = uart.read()
				ID = ID + str(Zeichen)
			ID = ID.replace(Endflag, "" ) # Checksumme berechnen
			#for I in range(0, 9, 2):
			#	Checksumme = Checksumme ^ (((int(ID[I], 16)) << 4) + int(ID[I+1], 16))
			#Checksumme = hex(Checksumme)
			#Tag = ((int(ID[1], 16)) << 8) + ((int(ID[2], 16)) << 4) + ((int(ID[3], 16)) << 0) 
			#Tag = hex(Tag)
			print ("RFID 2 detected: ", ID, " lapsed ", lapsed)
			with open(datafile,"a") as f:
				f.write("inactive\t" + time.strftime("%Y-%m-%d\t%H:%M:%S\t", localtime()) + "\t"+str(lapsed) + "\t" + ID + "\t"+ boxid +"\t\t\t\n")
				f.close()
			time.sleep(amount_to_sleep)
			uart.flushInput()
			uart.flushOutput()
			time.sleep(5)
			gpio.output(RFIDLed,True)


if __name__ == '__main__':

	# set path to rfid sensors
	path_to_rfid_one = "/dev/ttyAMA0"
	path_to_rfid_two = "/dev/ttyUSB0"

	# disable python automatic garbage collect
	# for greater sensitivity
	gc.disable()

	# initialize uart 1 & 2
	uart1 = initialize_uart(path_to_rfid_one) 
	uart2 = initialize_uart(path_to_rfid_two) 

	p1=multiprocessing.Process(target=activerfid, args=(uart1,))
	p2=multiprocessing.Process(target=inactiverfid, args=(uart2,))
	gpio.output(sessionLed1,True)
	gpio.output(sessionLed2,True)
	gpio.output(RFIDLed,True)
	p1.start()
	p2.start()
	time.sleep(sessionLength)
	gpio.output(sessionLed1,False)
	gpio.output(sessionLed2,False)
	p1.terminate()
	p2.terminate()
	p1.join()
	p2.join()

	# reactivate automatic garbage collection
	# and clean objects so no memory leaks

	# open data file
	with open(datafile,"a") as f:
		f.write("#Session Ended on " +time.strftime("%Y-%m-%d\t%H:%M:%S\t", localtime())+"\n")
		f.close()

	gc.enable()
	gc.collect()


