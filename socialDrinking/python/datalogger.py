#!/usr/bin/env python3

import time
import string
from ids import *

class LickLogger:
    def __init__(self, devID, sesID):
        self.devID = devID
        self.sessID= sesID
        self.startTime=time.strftime("%Y-%m-%d\t%H:%M:%S", time.localtime())

    def createDataFile(self, schedule, ratIDs):
        self.datafile = DATA_DIR + DATA_PREFIX + str(self.devID) + '_S' + str(self.sessID) +  "_" + schedule + str(ratIDs) + '.csv'
        print ("\nData file location:\n", self.datafile)
        # open data file
        with open(self.datafile,"a") as f:
            f.write("RatID\tRfidSec\tdate\tstart_time\tboxid\tEventType\t"+schedule+"\tlapsedSec\n")
            f.close()

    def logEvent(self, rat, eventSec, eventType, timeLapsed, ratio=0):
        # Create output string
        outputstr = rat + "\t" + str(eventSec) + "\t"+ time.strftime("%Y-%m-%d\t%H:%M:%S", time.localtime()) + "\t" + self.devID + "_S" + str(self.sessID) + "\t" + eventType + "\t" + str(ratio) + "\t"+ str(timeLapsed) + "\n"
        print (outputstr)
        with open (self.datafile, "a") as datafile:
            datafile.write(outputstr)

