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

sessionLed=36
gpio.setmode(gpio.BOARD)
gpio.setup(sessionLed,gpio.OUT)

UART = serial.Serial("/dev/ttyAMA0", 9600) 
UART.close();
UART.open()

with open(datafile,"a") as f:
	f.write("#session started on "+time.strftime("%Y-%m-%d\t%H:%M:%S\t", localtime())+"\n")
	f.close()

def inactiverfid():
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
			gpio.output(sessionLed,False)
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
			with open(datafile,"a") as f:
					f.write("inactive\t"+time.strftime("%Y-%m-%d\t%H:%M:%S\t", localtime())+"\t"+str(lapsed)+"\t"+ID+"\n")
			f.close()
			UART.flushInput()
			time.sleep(5)
			gpio.output(sessionLed,True)



if __name__ == '__main__':
	p=multiprocessing.Process(target=inactiverfid, name="Inactive")
	gpio.output(sessionLed,True)
	p.start()
	time.sleep(sessionLength)
	gpio.output(sessionLed,False)
	p.terminate()
	p.join()


