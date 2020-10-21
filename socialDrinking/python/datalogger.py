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
        date=time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
        self.datafile = DATA_DIR + DATA_PREFIX + date + "_" + str(self.devID) + '_S' + str(self.sessID) +  "_" + schedule + "_" + str(ratIDs) + '.csv'
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

    @staticmethod
    def finalLog(fname,data_dict):
        print(data_dict)
        print(data_dict["ratID1"])
        with open(DATA_DIR+ "/" + fname, "a+") as f:
            ID1_str = (("{}\t"*9).format(*data_dict["ratID1"])) + "\n"
            ID2_str = (("{}\t"*9).format(*data_dict["ratID2"])) + "\n"
            ID0_str = (("{}\t"*9).format(*data_dict["ratID0"])) + "\n"
            f.write(ID1_str + ID2_str + ID0_str)
        
        poke_count_files = {"ACT_POKE":"act_count.txt","INACT_POKE":"inact_count.txt"}
        with open(DATA_DIR + "/" + fname, "a+") as f:
            for ref, count_file in poke_count_files.items():
                with open(DATA_DIR + "/" + count_file, "r") as f1:
                    f.write("{}:{}\n".format(ref, f1.read()))
                

