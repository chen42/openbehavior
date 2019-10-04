#!/usr/bin/env python3

import sys
import time
import subprocess
import os
from ids import *


# Run the deviceinfo script
# pring("Hurry up, Wifi!")
# os.system("/home/pi/openbehavior/wifi-network/deviceinfo.sh")

# get date and time 
datetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
date=time.strftime("%Y-%m-%d", time.localtime())

RatID=input("please scan a command RFID\n")

# the default schedule is vr10 timeout20. Other reinforcemnt schedules can be started by using RFIDs.
if RatID[-1:]=="E":
    schedule="pr"
    breakpoint=2.0
    timeout = 20
    nextratio=int(5*2.72**(breakpoint/5)-5)
    sessionLength=10*60 # session ends after 10 min inactivity
    ratio=""
    #signal motion sensor to keep recording until this is changed
    with open ("/home/pi/prend", "w") as f:
        f.write("no")
elif RatID[-1:]=="F":
    schedule="fr"
    ratio = 2
    timeout =  20
    sessionLength=60*60*1 # one hour assay
    nextratio=ratio
elif RatID=="2E90EDD20283" or RatID=="2E90EDD226A7":
    schedule="ext"
    timeout=0
    ratio=1000000
    nextratio=1000000
    sessionLength=60*60*1
    print("Run Ext"+str(ratio)+" Prog.\nPls Scan Rat")
elif RatID=="2E90EDD21796":
    schedule="vr"
    ratio = 10
    timeout =  20
    sessionLength=60*60*22 # twenty two hour assay
    nextratio=ratio
    print("Run VR"+str(ratio)+"22h\nPls Scan Rat")
    time.sleep(3)
    RatID=ReadRFID("/dev/ttyAMA0")
elif RatID=="0400F16C5DC4":
    vreinstate=1
    schedule="vr"
    ratio = 5 
    timeout = 1 
    sessionLength=60*60*1 # one hour assay
    nextratio=ratio
    print("Run VREINST\n"+"Pls Scan Rat")
    time.sleep(3)
    RatID=ReadRFID("/dev/ttyAMA0")
else: # vr
    schedule="vr"
    ratio=10
    nextratio=ratio
    timeout = 20
    sessionLength=60*60*1 # one hour assay


rat1=input("please scan rat1\n")
time.sleep(5)
rat2=input("please scan rat2\n")

print("Session started\nSchedule:"+schedule+str(ratio)+"TO"+str(timeout)+"\nSession Length:"+str(sessionLength)+"sec\n")
time.sleep(1) # time to put the rat in the chamber
sTime=time.time()
lapsed=0

subprocess.call("python ./operant.py -schedule " +schedule+ " -ratio " +str(ratio)+ " -sessionLength " + str(sessionLength) + " -rat1ID " + rat1 + " -rat2ID " + rat2 + " -timeout " + str(timeout) +   " & ", shell=True)

while lapsed < sessionLength:
    #hms=time.strftime("%H:%M:%S", time.localtime())
    lapsed=time.time()-sTime
    try:
        rfid=input("rfid waiting")
    except EOFError:
        break
    if (len(rfid)==10):
        record=rfid+"\t"+str(time.time())+"\n"
        with open(ROOT + "/_inactive", "w+") as inactive:
            inactive.write(record)
            inactive.close()
        with open(ROOT + "/"+date+"_inactive", "a+") as inactive:
            print ("\n====inactive====")
            print ("|| "+rfid )
            print ("================\n")
            inactive.write(record)
            inactive.close()

    if (len(rfid)==8):
        record=rfid+"\t"+str(time.time())+"\n"
        with open(ROOT+"/_active", "w+") as active:
            active.write(record)
            active.close()
        with open(ROOT+"/"+date+"_active", "a+") as active:
            print ("\n====active====")
            print ("|| "+rfid )
            print ("==============\n")
            active.write(record)
            active.close()

#subprocess.call('/home/pi/openbehavior/wifi-network/rsync.sh &', shell=True)
