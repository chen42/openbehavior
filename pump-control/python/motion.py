#!/usr/bin/env python2

import RPi.GPIO as GPIO
import time
import os
import sys
from threading import Timer

### BEGIN CONSTANT DEFINITIONS
# Pin numbers for GPIO
MOTIONLED = int(31)
MOTIONOUT = int(35)
# Filesystem path to where the box id is stored
DEVIDPATH = '/home/pi/deviceid'
# Prefix to filesystem path where motion data will be stored
PREFIXDAT = '/home/pi/Pies/motion/motion_'
# Number of seconds to sleep after detecting motion
SECS_TO_SLEEP_ON_MOTION = float(1.0)
### END CONSTANT DEFINITIONS

### BEGIN GLOBAL DATA SECTION
# Constructed path to file where motion data is stored
motionDataPath = ''
# Global file handler for writing the motion data
motionDataFile = None
# ID string for the box data is being collected from
devID = ''
# Start time in various formats
startLocalTime = None
startLocalTimeString = ''
startEpochTime = float()
# Variable to control whether or not the program's main thread should sleep or not.
pSleep = False
# Motion sensing process id
motionpid = 99999
### END GLOBAL DATA SECTION

# Define helper function to blink the LED when a motion event is detected
def motionBlinkenLights():
	# Turn LED on, sleep for one-tenth of a second, then turn LED off
	GPIO.output(MOTIONLED, GPIO.HIGH)
	time.sleep(0.1)
	GPIO.output(MOTIONLED, GPIO.LOW)
	# Explicit return because STRUCTURED PROGRAMMING IS THE WAY OF THE FUTURE!!!
	return None
	
# Define callback for shutting down program
def stopProgram():
	os.system("/home/pi/openbehavior/wifi-network/rsync.sh")
	os.system("sudo kill -9 " + str(motionpid))

# Define callback for writing motion data to file when appropriate GPIO interrupt is fired
def recordMotionCallback(derp):
	global devID
	global motionDataFile
	global startEpochTime
	# Get time of event
	motionEventTime = time.time()
	# Calculate elapsed time since start
	elapsedTime = time.time() - startEpochTime
	# If elapsed time is greater than two hours, end the program
	if elapsedTime >= 7200:
		sys.exit(0)
	# Write data point to file
	motionDataFile.write(time.strftime("%Y-%m-%d\t", time.localtime(motionEventTime)) + boxID + "\t" + str(elapsedTime) + "\n")
	# Blink the LED
	motionBlinkenLights()
	# Explicit return because FUCK YEAH FLOWCHARTS
	return None

# Program entry point (AKA main)
def motionMain():
	# Explicitly global variables for modification
	global motionDataPath, motionDataFile, devID, startLocalTime, startLocalTimeString, startEpochTime, pSleep
	# Open file containing the box id, read the data, strip away whitespace, save the id into a global var, and close the file
	try:
		devidfile = open(DEVIDPATH, 'r')
		devID = (boxidfile.read()).strip()
		devidfile.close()
	except IOError as (errno, strerror):
		sys.stderr.write("I/O Error({0}): {1}\n".format(errno, strerror))
		sys.exit(1)
	
	# Record the starting time
	startEpochTime = time.time()
	# Convert it into localtime (struct_time) and formatted string representations
	startLocalTime = time.localtime(startEpochTime)
	startLocalTimeStr = time.strftime("%Y-%m-%d_%H:%M:%S", startLocalTime)
	# Using the recorded time, construct the path to the file used to store motion data
	motionDataPath = PREFIXDAT + devID + '_' + startLocalTimeStr + '.csv'
	
	# Open motion data file in append mode and write a comment line to indicate the starting time
	try:
		motionDataFile = open(motionDataPath, 'a')
		motionDataFile.write("# Session started on " + time.strftime("%Y-%m-%d\t%H:%M:%S\t", startLocalTime) + "\n")
	except IOError as (errno, strerror):
		sys.stderr.write("I/O Error({0}): {1}\n".format(errno, strerror))
		sys.exit(1)
	
	# Initialize GPIO
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(MOTIONOUT, GPIO.IN)
	GPIO.setup(MOTIONLED, GPIO.OUT, initial=GPIO.LOW)
	
	# Register interrupt event for pin used for motion detection
	#GPIO.add_event_detect(MOTIONOUT, GPIO.RISING, callback=recordMotionCallback)
	
	# Setup timer to kill program after two hours
	shutDownTimer = Timer(120, stopProgram)
	shutDownTimer.start()
	
	# Main event loop
	while(True):
		# EXPLANATION:
		# 	When motion is detected, the sensor's output transitions from low to high and stays
		# 	there for about one minute before finally transitioning back to low. Since the input
		#	is guaranteed to not change during this time, the program can sleep for most of it.
		#	Recording the time and writing it to the data file should take less than a second, 
		#	but we budget 15 seconds for this just to be safe (in case the kernel's buffer 
		#	cache is being thrashed or whatever) and provide some wiggle room. The program
		#	should therefore sleep for the remaining 45 seconds.
		#
		# If motion has been detected, sleep for about 3/4ths of a minute to free up CPU time
		#if pSleep:
			#time.sleep(SECS_TO_SLEEP_ON_MOTION)
			#pSleep = False
		#	pass
		# If motion hasn't been detected, simply pass (do nothing) and continue waiting for motion
		#else:
		#	pass
		if GPIO.input(MOTIONOUT):
			# Get time of event
			motionEventTime = time.time()
			# Calculate elapsed time since start
			elapsedTime = time.time() - startEpochTime
			# Write data point to file
			motionDataFile.write(time.strftime("%Y-%m-%d\t", time.localtime(motionEventTime)) + boxID + "\t" + str(elapsedTime) + "\n")
			# Blink the LED
			motionBlinkenLights()
						
# Execute motionMain() when script is run directly 
# (Allows for possible importation by other scripts in the future)
if __name__ == '__main__':
	motionMain()
