#!/usr/bin/python

# BEGIN IMPORT PRELUDE
import time
import string
# END IMPORT PRELUDE

# BEGIN CONSTANT DEFINITIONS
DEVID_FILEPATH = '/home/pi/deviceid'
RATID_FILEPATH = '/home/pi/ratid'
TDATA_FILEPRFX = '/home/pi/Pies/ETOH/Lick/ETOH_'
# END CONSTANT DEFINITIONS

class DataLogger:
	def __init__(self):
		# read box id
		devidfile = open(DEVID_FILEPATH)
		self.devid = str((devidfile.read()).strip())
		devidfile.close()
		# read rat id
		ratidfile = open(RATID_FILEPATH)
		self.ratid = int((ratidfile.read()).strip())
		ratidfile.close()
		# get start time
		startTime=time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
		# construct file name
		datafilePath = TDATA_FILEPRFX + str(self.devid) + '_' + str(startTime) + '.csv'
		# open data file
		self.datafile = open(datafilePath, "a")
	def logTouch(self, touchType):
		# Get current time in formatted string
		currtimestr = time.strftime("%Y/%m/%d\t%H:%M:%S:%f %Z\n")
		# Create output string
		outputstr = "" + str(self.devid) + "\t" + str(self.ratid) + "\t" + touchType + "\t" + currtimestr
		# Append to file
		(self.datafile).write(outputstr)

