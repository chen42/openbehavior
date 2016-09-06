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
	def createDataFile(self, RatID, schedule):
		devidfile = open(DEVID_FILEPATH)
		self.devid = str((devidfile.read()).strip())
		devidfile.close()

		# read rat id
		self.ratid = RatID 

                # read sessin id
                sessionid=open(SESSIONID)
                self.sessid=str(sessionid.read().strip())
                #print ("sessionid ", self.sessid, "\n") 

		# get start time
		startTime=time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())

		# construct file name
                self.datafile = TDATA_FILEPRFX + self.datatype + "_" +  str(self.devid)[5:] + '_S' + self.sessid +  "_" +  str(self.ratid) + '.csv'

		# open data file
		with open(self.datafile,"a") as f:
			f.write("RatID\tdate\tboxid\tEventType\t"+schedule+"\tseconds\n")
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
