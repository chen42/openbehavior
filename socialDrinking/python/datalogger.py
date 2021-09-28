#!/usr/bin/env python3
import os
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
        ratids = [data_dict["ratID1"][0], data_dict["ratID2"][0]]
        poke_counts = {ratids[0]:{"act":0, "inact": 0}, ratids[1]:{"act":0, "inact":0}}
        poke_count_files = {"ACT_POKE": ["{}_act_count.txt".format(ID) for ID in ratids],
                            "INACT_POKE": ["{}_inact_count.txt".format(ID) for ID in ratids]
                           }

        with open(DATA_DIR + "/" + fname, "a+") as f:
            for ref, count_files in poke_count_files.items():
                for file in count_files:
                    try:
                        with open(DATA_DIR + "/" + file, "r") as f1:
                            (rfid,poke_count) = f1.read().split(":")
                            if ref == "ACT_POKE":
                                poke_counts[rfid]["act"] = poke_count
                            else:
                                poke_counts[rfid]["inact"] = poke_count
                        # remove file after reading
                        os.remove(DATA_DIR + "/" + file)
                    except FileNotFoundError:
                        continue

        with open(DATA_DIR+ "/" + fname, "a+") as f:
            ID1_str = (("{}\t"*13).format(*data_dict["ratID1"], poke_counts[ratids[0]]["act"], poke_counts[ratids[0]]["inact"])) + "\n"
            ID2_str = (("{}\t"*13).format(*data_dict["ratID2"], poke_counts[ratids[1]]["act"], poke_counts[ratids[1]]["inact"])) + "\n"
            ID0_str = (("{}\t"*11).format(*data_dict["ratID0"])) + "\n"
            f.write(ID1_str + ID2_str + ID0_str)
        
                

