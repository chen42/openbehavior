#!/usr/bin/python

# Copyright 2016 University of Tennessee Health Sciences Center
# Author: Matthew Longley <mlongle1@uthsc.edu>
# Author: Hao Chen <hchen@uthsc.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or(at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# BEGIN IMPORT PRELUDE
import sys
import getopt
import time
import datetime
from threading import Timer
import subprocess32 as subprocess
import RPi.GPIO as gpio
import Adafruit_MPR121.MPR121 as MPR121
import pumpcontrol
import serial
import touchsensor
import datalogger
import os
# END IMPORT PRELUDE

# BEGIN CONSTANT DEFINITIONS
TIR = int(36)
SW1 = int(37)
SW2 = int(38)
TOUCHLED = int(32)
# END CONSTANT DEFINITIONS

# BEGIN GLOBAL VARIABLES
touchcounter = 0
fixedratio = 10
timeout = 20
pumptimedout = False
sessionLength=7200
#pumppid = 99999
# END GLOBAL VARIABLES

def stopProgram():
	os.system("/home/pi/openbehavior/wifi-network/rsync.sh")
	os.system("sudo kill -9 " + str(pumppid))

def printUsage():
	print(sys.argv[0] + ' -t <timeout> -f <fixed ratio>')
	
def resetPumpTimeout():
	global pumptimedout
	pumptimedout = False
	
def blinkTouchLED(duration):
	gpio.output(TOUCHLED, gpio.HIGH)
	time.sleep(duration)
	gpio.output(TOUCHLED, gpio.LOW)



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
		Z = 0
		Tag = 0
		ID = ""
		Z = uart.read()
		if Z == Startflag:
			for Counter in range(13):
				Z = uart.read()
				ID = ID + str(Z)
			ID = ID.replace(Endflag, "" ) 
			print "RFID  detected: "+ ID
			return (ID)

# Parse command line arguments
try:
	opts, args = getopt.getopt(sys.argv[1:], "hf:t:")
except getopt.GetoptError:
	printUsage()
	sys.exit(2)
for opt, arg in opts:
	if opt == '-f':
		fixedratio = int(arg)
	elif opt == '-t':
		timeout = int(arg)
	elif opt == '-h':
		printUsage()
		sys.exit()


# Get process ID
pumppid = os.getpid()

# Initialize GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)


# Setup switch pins
gpio.setup(SW1, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(SW2, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(TIR, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(TOUCHLED, gpio.OUT)
MOTIONLED=int(31)
gpio.setup(MOTIONLED, gpio.OUT)

# Run the deviceinfo script
os.system("/home/pi/openbehavior/wifi-network/deviceinfo.sh")
print "device info updated\n"
gpio.output(TOUCHLED, gpio.HIGH)
gpio.output(MOTIONLED, gpio.HIGH)

os.system("/home/pi/openbehavior/pump-control/python/motion.py &")
# Initialize pump
pump = pumpcontrol.Pump(gpio)

# Initialize touch sensor
tsensor = touchsensor.TouchSensor()

# Initialize data logger
dlogger = datalogger.DataLogger()

# Get start time
sTime = datetime.datetime.now()

# Setup timer to shutdown program after two hours
shutDownTimer = Timer(sessionLength, stopProgram)
shutDownTimer.start()

# wait for RFID scanner to get RatID

RatID=ReadRFID("/dev/ttyAMA0")
print RatID
with open ("/home/pi/ratid", "w") as ratid:
    ratid.write(RatID)

## creat data files, Each box has its own ID

while True:
	if gpio.input(SW1):
		pump.move(0.5)
	elif gpio.input(SW2):
		pump.move(-0.5)
	elif not gpio.input(TIR):
		i = tsensor.readPinTouched()
		if i == 1:
			if not pumptimedout:
				touchcounter += 1
				if touchcounter == fixedratio:
					lapsed= datetime.datetime.now() - sTime
					dlogger.logTouch("REWARD", lapsed)
					touchcounter = 0
					pumptimedout = True
					pumpTimer = Timer(timeout, resetPumpTimeout)
					pumpTimer.start()
					subprocess.call('python /home/pi/openbehavior/pump-control/python/blinkenlights.py &', shell=True)
					pump.move(-0.06)
				else:
					lapsed= datetime.datetime.now() - sTime
					dlogger.logTouch("ACTIVE", lapsed)
			else:
				lapsed= datetime.datetime.now() - sTime
				dlogger.logTouch("ACTIVE", lapsed)
			blinkTouchLED(0.05)
		elif i == 2:
			lapsed= datetime.datetime.now() - sTime
			dlogger.logTouch("INACTIVE", lapsed)
			blinkTouchLED(0.05)
