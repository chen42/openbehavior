#!/usr/bin/env python2

import RPi.GPIO as GPIO
import time
import os
import sys

### BEGIN CONSTANT DEFINITIONS
# Pin numbers for GPIO
MOTIONLED = int(31)
MOTIONOUT = int(35)
# Filesystem path to where the box id is stored
BOXIDPATH = '/home/pi/boxid'
# Prefix to filesystem path where motion data will be stored
PREFIXDAT = '/home/pi/pies/motion/mot'
# Number of seconds to sleep after detecting motion
SECS_TO_SLEEP_ON_MOTION = float(45.0)
### END CONSTANT DEFINITIONS

### BEGIN GLOBAL DATA SECTION
# Constructed path to file where motion data is stored
motionDataPath = ''
# Global file handler for writing the motion data
motionDataFile = None
# ID string for the box data is being collected from
boxID = ''
# Start time in various formats
startLocalTime = None
startLocalTimeString = ''
startEpochTime = float()
# Variable to control whether or not the program's main thread should sleep or not.
# EXPLANATION:
# 	The motion detector outputs HIGH for an entire minute after motion is detected,
# 	so the program should voluntarily release control of execution and sleep for just
# 	under a minute instead of tying up resources. This variable is asynchronously set
#	to true by recordMotionCallback which is asynchronously called whenever motion is 
#	detected and reset to false after the program finishes sleeping.
pSleep = False
### END GLOBAL DATA SECTION

# Define helper function to blink the LED when a motion event is detected
def motionBlinkenLights():
	# Turn LED on, sleep for one-tenth of a second, then turn LED off
	GPIO.output(MOTIONLED, GPIO.HIGH)
	time.sleep(0.1)
	GPIO.output(MOTIONLED, GPIO.LOW)
	# Explicit return because STRUCTURED PROGRAMMING IS THE WAY OF THE FUTURE!!!
	return None

# Define callback for writing motion data to file when appropriate GPIO interrupt is fired
def recordMotionCallback():
	global boxID
	global motionDataFile
	global startEpochTime
	# Get time of event
	motionEventTime = time.time()
	# Calculate elapsed time since start
	elapsedTime = time.time() - startEpochTime
	# Write data point to file
	motionDataFile.write(time.strftime("%Y-%m-%d\t", time.localtime(eventTime)) + boxID + "\t" + str(elapsedTime) + "\n")
	# Blink the LED
	motionBlinkenLights()
	# Explicit return because FUCK YEAH FLOWCHARTS
	return None

# Program entry point (AKA main)
def motionMain():
	# Explicitly global variables for modification
	global motionDataPath, motionDataFile, boxID, startLocalTime, startLocalTimeString, startEpochTime, pSleep
	# Open file containing the box id, read the data, strip away whitespace, save the id into a global var, and close the file
	try:
		boxidfile = open(BOXIDPATH, 'r')
		boxID = (boxidfile.read()).strip()
		boxidfile.close()
	except IOError as (errno, strerror):
		sys.stderr.write("I/O Error({0}): {1}\n".format(errno, strerror))
		sys.exit(1)
	
	# Record the starting time
	startEpochTime = time.time()
	# Convert it into localtime (struct_time) and formatted string representations
	startLocalTime = time.localtime(startEpochTime)
	startLocalTimeStr = time.strftime("%Y-%m-%d_%H:%M:%S", startLocalTime)
	# Using the recorded time, construct the path to the file used to store motion data
	motionDataPath = PREFIXDAT + boxID + '_' + startLocalTimeStr + '.csv'
	
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
	GPIO.add_event_detect(MOTIONOUT, GPIO.RISING, callback=recordMotionCallback)
	
	# Main event loop
	while(True):
		# EXPLANATION:
		# 	When motion is detected, the sensor's output transitions from low to high and stays
		# 	high for about one minute before finally transitioning back to low. Since the input
		#	is guaranteed to not change during this time, the program can sleep for most of it.
		#	Recording the time and writing it to the data file should take less than a second, 
		#	but we budget 15 seconds for this just to be safe (in case the kernel's buffer 
		#	cache is being thrashed or whatever) and to provide some wiggle room. The program
		#	should therefore sleep for the remaining 45 seconds
		#
		# If motion has been detected, sleep for about 3/4ths of a minute to free up CPU time
		if pSleep:
			time.sleep(SECS_TO_SLEEP_ON_MOTION)
			pSleep = False
		# If motion hasn't been detected, simply pass (do nothing) and continue waiting for motion
		else:
			pass
			
# Execute motionMain() when script is run directly 
# (Allows for possible importation by other scripts in the future)
if __name__ == '__main__':
	motionMain()
