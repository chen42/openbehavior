#!/usr/bin/python

# BEGIN IMPORT PRELUDE
import time
import string
# END IMPORT PRELUDE

# BEGIN CONSTANT DEFINITIONS
BOXID_FILEPATH = '/home/pi/boxid'
RATID_FILEPATH = '/home/pi/ratid'
TDATA_FILEPRFX = '/home/pi/pies/pump/pump'
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
		# get start time
		startTime=time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
		# construct file name
		datafilePath = TDATA_FILEPRFX + self.boxid + '_' + str(startTime) + '.csv'
		# open data file
		self.datafile = open(datafilePath, "a")
	def logTouch(self, touchType):
		# Get current time in formatted string
		currtimestr = time.strftime("%Y/%m/%d\t%H:%M:%S:%f %Z\n")
		# Create output string
		outputstr = "" + str(self.boxid) + "\t" + str(self.ratid) + "\t" + touchType + "\t" + currtimestr
		# Append to file
		(self.datafile).write(outputstr)

