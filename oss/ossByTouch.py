import RPi.GPIO as gpio
import serial
import time
import os
import gc
import sys
import Adafruit_MPR121.MPR121 as MPR121
import multiprocessing
import subprocess
from time import strftime, localtime
from operator import xor 
from random import randint

def initUART(path_to_sensor) :
	baud_rate = 9600 
	time_out = 0.05
	uart = serial.Serial(path_to_sensor, baud_rate, timeout = time_out)
	uart.close()
	uart.open()
	uart.flushInput()
	uart.flushOutput()
	print(path_to_sensor + " initiated")
	return uart;

def readRFID(uart):
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

def createDataFiles():
	# open touch data file
	with open(touchDataFile,"a") as f:
		f.write("#Session Started on " +time.strftime("%Y-%m-%d\t%H:%M:%S\t", localtime())+"\n")
		f.write("RatID\thole\tdate\ttime\tlapsed\tboxid\tleds\ttimes\tspeed\n")
		f.close()
	# open motion data file
	with open(motionDataFile,"a") as f:
		f.write("#Session Started on " +time.strftime("%Y-%m-%d\t%H:%M:%S\t", localtime())+"\n")
		f.write("RatID\tboxid\tseconds\n")
		f.close()

### initiate touch sensor
def initTouch():
	cap = MPR121.MPR121()
	if not cap.begin():
		print 'Error initializing MPR121.  Check your wiring!'
		subprocess.call("sudo python /home/pi/oss/errorled.py &")
		sys.exit(1)
	return cap


def active():
	timeout=5
	rewardtime=start-timeout #to ensoure the first touch of the session triggers the reward immediately
	while True:
		if cap.is_touched(1):
			subprocess.call("sudo python /home/pi/oss/touchled.py &", shell=True)
			if (time.time()-rewardtime>timeout):
				rewardtime=time.time()
				subprocess.call("sudo python /home/pi/oss/blink.py " + " -datafile "+  touchDataFile + " -RatID " + RatID +  " -start " + str(start)  + " &", shell=True)
			else:
				with open(touchDataFile,"a") as f:
					lapsed=time.time()-start
					f.write(RatID + "\tactive\t" + time.strftime("%Y-%m-%d\t%H:%M:%S", localtime()) + "\t" + str(lapsed) + "\t" + boxid + "\t\t\t\n")
					f.close()
			time.sleep(0.5)

def inactive():
	while True:
		if cap.is_touched(0):
			subprocess.call("sudo python /home/pi/oss/touchled.py &", shell=True)
			with open(touchDataFile,"a") as f:
				lapsed=time.time()-start
				f.write(RatID+"\tinactive\t" + time.strftime("%Y-%m-%d\t%H:%M:%S", localtime()) + "\t" + str(lapsed) + "\t" + boxid + "\t\t\t\n")
				f.close()
			time.sleep(0.5)

def motion():
	cnt=0
	#while time.time()-start < sessionLength:
	while True:
		if gpio.input(pirPin):
			#print time.strftime("%Y-%m-%d\t%H:%M:%S")
			with open(motionDataFile,"a") as f:
				lapsed=time.time()-start
				f.write(RatID+"\t"+boxid +"\t"+ str(lapsed) +"\n")
				f.close()
			gpio.output(motionLed, True)
			time.sleep(0.5)
			gpio.output(motionLed, False)
			time.sleep(0.5)
			cnt=cnt+1
			#return cnt


if __name__ == '__main__':
	sessionLength=3600
	# disable python automatic garbage collect for greater sensitivity
	gc.disable()

	# session LEDs are on when data are being recorded. These LEDs are located at the end of the head poke holes and serve to attract the attension of the rats. 
	# touchLed is on when touch sensor is activated  
	# green and red Leds are for sensation seeking
	motionLed=31
	sessionLed1=33
	touchLed=35 
	sessionLed2=37
	greenLed=11
	redLed=7
	pins=[greenLed,redLed]
	pirPin = 12 
	# setting up the various LEDs.
	gpio.setwarnings(False)
	gpio.setmode(gpio.BOARD)
	gpio.setup(greenLed, gpio.OUT)
	gpio.setup(redLed, gpio.OUT)
	gpio.setup(sessionLed1,gpio.OUT)
	gpio.setup(sessionLed2,gpio.OUT)
	gpio.setup(touchLed,gpio.OUT)
	gpio.setup(pirPin, gpio.IN)        
	gpio.setup(motionLed, gpio.OUT)       
	## Initial LED status
	gpio.output(redLed,False)
	gpio.output(greenLed,False)
	gpio.output(touchLed,False)
	gpio.output(sessionLed1,True)
	gpio.output(sessionLed2,True)
	# initiate the touch sensor
	cap=initTouch()
	## session starts when the RFID is detected
	path = "/dev/ttyUSB0"
	uart = initUART(path) 
	RatID = readRFID(uart)
	print RatID
	## creat data files, Each box has its own ID
	idfile=open("/home/pi/boxid")
	boxid=idfile.read()
	boxid=boxid.strip()
	# data file names
	startTime=str(time.strftime("%Y-%m-%d_%H:%M:%S", localtime()))
	touchDataFile='/home/pi/oss'+ boxid + "_" + startTime + ".csv"
	motionDataFile='/home/pi/motion'+ boxid + "_" + startTime + ".csv"
	createDataFiles()
	## blink both the touchLed and motionLed to indicate the RFID is detected
	gpio.output(touchLed, True)
	gpio.output(motionLed, True)
	time.sleep(2)
	gpio.output(touchLed, False)
	gpio.output(motionLed, False)
	start=time.time()
	##
	p1=multiprocessing.Process(target=active)
	p2=multiprocessing.Process(target=inactive)
	p3=multiprocessing.Process(target=motion)
	p1.start()
	p2.start()
	p3.start()
	time.sleep(sessionLength)
	gpio.output(sessionLed1,False)
	gpio.output(sessionLed2,False)
	p1.terminate()
	p2.terminate()
	p3.terminate()
	p1.join()
	p2.join()
	p3.join()
	## finishing the data files
	with open(motionDataFile, "a") as f:
	#f.write("Total Activity:\t"+str(CNT)+"\n")
		f.write("#session Ended at " + time.strftime("%H:%M:%S", localtime())+"\n")
		f.close
	# open data file
	with open(touchDataFile,"a") as f:
		f.write("#Session Ended on " +time.strftime("%Y-%m-%d\t%H:%M:%S\t", localtime())+"\n")
		f.close()
	# reactivate automatic garbage collection and clean objects so no memory leaks
	gc.enable()
	gc.collect()


