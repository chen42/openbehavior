#!/usr/bin/env python3

import time
import string

ROOT='/home/pi'
ROOT="."
DEVID_FILE = ROOT+'/deviceid'
RATID_FILE = ROOT+'/ratids'
SESSIONID_FILE = ROOT+'/sessionid'
DATAFILE_PRFX = ROOT+'/Pies/Oxycodone/Oxy_'

class LickLogger:
    def __init__(self):
        with open (DEVID_FILE) as devID:
            self.devID = str((devID.read()).strip())
            devID.close()
        with open (SESSIONID_FILE) as sessID:
            self.sessID=str(sessID.read().strip())
            sessID.close()
        with open (RATID_FILE) as ratID:
            self.ratID = str((ratID.read()).strip())
            ratID.close()
        self.startTime=time.strftime("%Y-%m-%d\t%H:%M:%S", time.localtime())

    def createDataFile(self, schedule):
        self.datafile = DATAFILE_PRFX + str(self.devID) + '_S' + self.sessID +  "_" +  str(self.ratID) + '.csv'
        print ("Data file location:\n", self.datafile)
        # open data file
        with open(self.datafile,"a") as f:
            f.write("RatID\tdate\tstart_time\tboxid\tEventType\t"+schedule+"\tseconds\n")
            f.close()

    def logEvent(self, rat, eventType, timeLapsed, ratio=0):
        # Create output string
        outputstr = rat + "\t" + time.strftime("%Y-%m-%d\t%H:%M:%S", time.localtime()) + "\t" + self.devID + "_S" + self.sessID+ "\t" + eventType + "\t" + str(ratio) + "\t"+ str(timeLapsed) + "\n"
        print (outputstr)
        with open (self.datafile, "a") as datafile:
            datafile.write(outputstr)

