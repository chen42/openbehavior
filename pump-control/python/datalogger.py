#!/usr/bin/python

# BEGIN IMPORT PRELUDE
import time
import string
# END IMPORT PRELUDE

# BEGIN CONSTANT DEFINITIONS
BOXID_FILEPATH = '/home/pi/boxid'
RATID_FILEPATH = '/home/pi/ratid'
TDATA_FILEPATH = '/home/pi/touchdata'
# END CONSTANT DEFINITIONS

class DataLogger:
	def __init__(self):
		# read box id
		boxidfile = open(BOXID_FILEPATH)
		self.boxid = int((boxidfile.read()).strip())
		boxidfile.close()
		# read rat id
		ratidfile = open(RATID_FILEPATH)
		self.ratid = int((ratidfile.read()).strip())
		ratidfile.close()
		# open data file
		self.datafile = open(TDATA_FILEPATH, "a")
	def logTouch(self, touchType):
		# Get current time in formatted string
		currtimestr = time.strftime("%Y/%m/%d\t%H:%M:%S %Z\n")
		# Create output string
		outputstr = "" + str(self.boxid) + "\t" + str(self.ratid) + "\t" + touchType + "\t" + currtimestr
		# Append to file
		(self.datafile).write(outputstr)

