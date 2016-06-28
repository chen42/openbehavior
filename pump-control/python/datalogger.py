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
		self.ratid = str((ratidfile.read()).strip())
		ratidfile.close()
		# get start time
		startTime=time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
		# construct file name
		self.datafilePath = TDATA_FILEPRFX + str(self.ratid) + '_' + str(startTime) + '.csv'
		# open data file
		#self.datafile = open(datafilePath, "a")
	def logTouch(self, touchType, timelapsed):
		# Create output string
		outputstr = "" + self.ratid + "\t" + self.devid + "\t" + touchType + "\t" + str(timelapsed) + "\n"
		# Append to file
		with open (self.datafilePath, "a") as datafile:
			datafile.write(outputstr)

