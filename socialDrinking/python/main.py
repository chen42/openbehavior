#!/usr/bin/env python3

import sys
import time
import subprocess
import os
from ids import *
from gpiozero import Button
from pump_move import PumpMove
from gpiozero import DigitalInputDevice



# get date and time 
datetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
date=time.strftime("%Y-%m-%d", time.localtime())
# get device and session ids
ids = IDS()
ids.sessionIncrement()
# file to store RFID scann times
RFIDFILE=DATA_DIR + DATA_PREFIX + date + "_" + str(ids.devID)+ "_S"+str(ids.sesID)+ "_RFID.csv"

RatID=input("please scan a command RFID\n")[-8:]

class SessionInfo():
    def init(self, schedule, timeout, nextratio, sessionLength, ratio):
        self.schedule = schedule
        self.timeout = timeout
        self.nextratio = nextratio
        self.sessionLength = sessionLength
        self.ratio = ratio
        self.nextratio = nextratio


command_ids = {
    ('3c', '88'): SessionInfo(schedule="pr", timeout=10, nextratio=int(5*2.72**(2/5)-5), sessionLength=20*60, ratio=""), # PR
    ('52', '8f'): SessionInfo(schedule="fr", timeout=10, nextratio=5, sessionLength=60*60*1, ratio=5), # FR5 1h
    ('6f', 'b9'): SessionInfo(schedule="fr", timeout=10, nextratio=5, sessionLength=60*60*16, ratio=5), # FR5 16h
    ('65', '8c'): SessionInfo(schedule="ext", timeout=0, nextratio=1000000, sessionLength=60*60*1, ratio=1000000), # extinction
    ('ef', 'a7'): SessionInfo(schedule="vr", timeout=10, nextratio=10, sessionLength=60*60*1, ratio=10), # VR10, 1h
    ('b8', '7e'): SessionInfo(schedule="vr", timeout=10, nextratio=10, sessionLength=60*60*2, ratio=10), # VR10, 2h
    ('9a', '2f'): SessionInfo(schedule="vr", timeout=10, nextratio=10, sessionLength=60*60*4, ratio=10), # VR10, 4h
    ('ff', '2d'): SessionInfo(schedule="vr", timeout=1, nextratio=5, sessionLength=60*60*4, ratio=5), # VRreinstate, 4h
    ('8e', 'c3'): SessionInfo(schedule="vr", timeout=10, nextratio=10, sessionLength=60*60*16, ratio=10), # VR10 16h
}

while RatID not in COMMAND_IDS:
    RatID = input("command ID not found, please rescan the id: ")[-8:]

for key in command_ids.keys():
    if RatID[-2:] in key:
        sess_info = command_ids[key]
    
mover = PumpMove()

sessionLength = sess_info.sessionLength
ratio = sess_info.ratio
timeout = sess_info.timeout
schedule = sess_info.schedule

h=str(int(sessionLength/3600))
print("Run " + schedule + str(ratio) + "for "  + h + "h\n")

rat1 = input("please scan rat1\n")[-8:]
time.sleep(1) # delay for time to get the next rat
rat2 = input("please scan rat2\n")[-8:]

while(rat1 == rat2):
    rat2 = input("The IDs of rat1 and rat2 are identical, please scan rat2 again\n")[-8:]

print("Session started\nSchedule:"+schedule+str(ratio)+"TO"+str(timeout)+"\nSession Length:"+str(sessionLength)+"sec\n")
# start time
sTime=time.time()
lapsed=0

# delete mover to prevent overheating
del(mover)

subprocess.call("python3 operant.py -schedule " +schedule+ " -ratio " +str(ratio)+ " -sessionLength " + str(sessionLength) + " -rat1ID " + rat1 + " -rat2ID " + rat2 + " -timeout " + str(timeout) +   " & ", shell=True)

poke_counts = {rat1:{"act": 0, "inact": 0}, rat2:{"act":0, "inact":0}}

while lapsed < sessionLength:
    lapsed=time.time()-sTime
    try:
        rfid=input("rfid waiting\n")
    except EOFError:
        break
    if (len(rfid)==10):
        temp_rfid = rfid[-8:]
        poke_counts[temp_rfid]["inact"] = poke_counts[temp_rfid]["inact"] + 1
        record=temp_rfid+"\t"+str(time.time())+ "\tinactive\t" + str(lapsed) +"\n"
        with open(ROOT + "/_inactive", "w+") as inactive:
            inactive.write(record)
            inactive.close()
        with open(RFIDFILE, "a+") as inactive:
            print ("\n    inactive spout " + temp_rfid + "\t")
            inactive.write(record)
        fname = "{}/{}_inact_count.txt".format(DATA_DIR, temp_rfid)
        with open(fname, "w+") as f:
            f.write("{}:{}".format(temp_rfid, poke_counts[temp_rfid]["inact"]))
            

    if (len(rfid)==8):
        try:
            poke_counts[rfid]["act"] = poke_counts[rfid]["act"] + 1
        except KeyError as e:
            with open(ROOT + "/error.log", "a+") as f:
                f.write("error - {}\n".format(e))
                f.write("poke_counts - {}\n".format(poke_counts))
                f.write("rfid - {}\n".format(rfid))

        record=rfid+"\t"+str(time.time())+ "\tactive\t" + str(lapsed)+ "\n"
        with open(ROOT+"/_active", "w+") as active:
            active.write(record)
            active.close()
        with open(RFIDFILE, "a+") as active:
            print ("\n      active spout " + rfid + "\t")
            active.write(record)
        fname = "{}/{}_act_count.txt".format(DATA_DIR, rfid)
        with open(fname, "w+") as f:
            f.write("{}:{}".format(rfid,poke_counts[rfid]["act"]))
