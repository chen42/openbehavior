#!/usr/bin/python

# Copyright 2016 University of Tennessee Health Sciences Center
# Author: Matthew Longley <mlongle1@uthsc.edu>
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
pumppid = 99999
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

# Run the deviceinfo script
os.system("/home/pi/openbehavior/wifi-network/deviceinfo.sh")

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

# Initialize pump
pump = pumpcontrol.Pump(gpio)

# Initialize touch sensor
tsensor = touchsensor.TouchSensor()

# Initialize data logger
dlogger = datalogger.DataLogger()

# Get start time
sTime = datetime.datetime.now()

# Setup timer to shutdown program after two hours
shutDownTimer = Timer(120, stopProgram)
shutDownTimer.start()

while True:
	if gpio.input(SW1):
		pump.move(0.5)
	elif gpio.input(SW2):
		pump.move(-0.5)
	elif not gpio.input(TIR):
		i = tsensor.readPinTouched()
		if i == 1:
			blinkTouchLED(0.1)
			if not pumptimedout:
				touchcounter += 1
				if touchcounter == fixedratio:
					dlogger.logTouch("REWARD")
					touchcounter = 0
					pumptimedout = True
					pumpTimer = Timer(timeout, resetPumpTimeout)
					pumpTimer.start()
					subprocess.call('python /home/pi/openbehavior/pump-control/python/blinkenlights.py &', shell=True)
					pump.move(-0.06)
				else:
					dlogger.logTouch("ACTIVE")
			else:
				dlogger.logTouch("ACTIVE")
		elif i == 7:
			blinkTouchLED(0.1)
			dlogger.logTouch("INACTIVE")
