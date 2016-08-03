#!/usr/bin/python

# BEGIN IMPORT PRELUDE
import time
import string
# END IMPORT PRELUDE

# BEGIN CONSTANT DEFINITIONS
DEVID_FILEPATH = '/home/pi/deviceid'
RATID_FILEPATH = '/home/pi/ratid'
TDATA_FILEPRFX = '/home/pi/Pies/ETOH/ETOH_'
SESSIONID='/home/pi/sessionid'
# END CONSTANT DEFINITIONS

class LickLogger:
	def __init__(self):
		# read box id
		self.datatype="lick"
	def createDataFile(self):
		devidfile = open(DEVID_FILEPATH)
		self.devid = str((devidfile.read()).strip())
		devidfile.close()
		# read rat id
		ratidfile = open(RATID_FILEPATH)
		self.ratid = str((ratidfile.read()).strip())
		ratidfile.close()
                # read sessin id
                sessionid=open(SESSIONID)
                self.sessid=str(sessionid.read().strip())
		# get start time
		startTime=time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
		# construct file name
                self.datafile = TDATA_FILEPRFX + self.datatype + "_" + str(self.ratid) + "_" + str(self.devid)[5:] + '_S' + self.sessid + '.csv'
		# open data file
		with open(self.datafile,"a") as f:
			f.write("RatID\tdate\tboxid\tEventType\tratio\tseconds\n")
			f.close()
	def logEvent(self, EventType, timelapsed, ratio=0):
		# Create output string
		outputstr = self.ratid + "\t" + time.strftime("%Y-%m-%d", time.localtime()) + "\t" + self.devid + "_S" + self.sessid+ "\t" + EventType + "\t" + str(ratio) + "\t"+ str(timelapsed) + "\n"
		# Append to file
		with open (self.datafile, "a") as datafile:
			datafile.write(outputstr)


class MotionLogger (LickLogger):
	def __init__ (self):
		self.datatype="motion"
