#!/usr/bin/env python3

import sys
import time
import subprocess
import os
from ids import *
from gpiozero import Button
from pump_move import PumpMove
from gpiozero import DigitalInputDevice

# start the pump  
mover = PumpMove()
forwardbtn = Button("GPIO5")
backwardbtn = Button("GPIO27")

BACKWARD_LIMIT_BTN = "GPIO23"
BACKWARD_LIMIT = DigitalInputDevice(BACKWARD_LIMIT_BTN)

# ************************************************************************************************
# BUTTON MOVE setting

# ************************************************************************************************
# BUTTON MOVE setting

def forward():
    while forwardbtn.value == 1:
        mover.move("forward")

def backward():
    while BACKWARD_LIMIT.value != 1:
        mover.move("backward")

forwardbtn.when_pressed = forward
backwardbtn.when_pressed = backward


# get date and time 
datetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
date=time.strftime("%Y-%m-%d", time.localtime())

RatID=input("please scan a command RFID\n")

# the default schedule is vr10 timeout20. Other reinforcemnt schedules can be started by using RFIDs.
if RatID[-1:]=="F": # PR
    schedule="pr"
    breakpoint=2
    timeout = 20
    nextratio=int(5*2.72**(breakpoint/5)-5)
    sessionLength=20*60 # session ends after 20 min inactivity
    ratio=""
    #signal motion sensor to keep recording until this is changed
    with open ("/home/pi/prend", "w") as f:
        f.write("no")
elif RatID[-1:] == "A":  #FR5 1h
    schedule="fr"
    ratio = 5
    timeout =  20
    sessionLength=60*60*1 # one hour assay
    nextratio=ratio
elif RatID[-1:]=="B": # FR5, 16h 
    schedule="fr"
    ratio = 5
    timeout =  20
    sessionLength=60*60*16 # one hour assay
    nextratio=ratio
elif RatID[-1:]=="C": # extinction
    schedule="ext"
    timeout=0
    ratio=1000000
    nextratio=1000000
    sessionLength=60*60*1
elif RatID[-1:]=="1": #VR10, 1h
    schedule="vr"
    ratio = 10
    timeout =  20
    sessionLength=60*60*1 #
    nextratio=ratio
elif RatID[-1:]=="4": #VR10, 4h
    schedule="vr"
    ratio = 10
    timeout =  20
    sessionLength=60*60*4 #
    nextratio=ratio
elif RatID[-1:]=="D": #VRreinstate, 4h
    vreinstate=1
    schedule="vr"
    ratio = 5
    timeout = 1
    sessionLength=60*60*4 # one hour assay
    nextratio=ratio
    RatID=ReadRFID("/dev/ttyAMA0")
else: # vr10 16h
    schedule="vr"
    ratio=10
    nextratio=ratio
    timeout = 20
    sessionLength=60*60*16

h=str(int(sessionLength/3600))
print("Run " + schedule + str(ratio) + "for "  + h + "h\n")

time.sleep(3)
rat1 = input("please scan rat1\n")[-8:]
rat2 = input("please scan rat2\n")[-8:]

while(rat1[-8:] == rat2[-8:]):
    rat2 = input("The IDs of rat1 and rat2 are identical, please scan rat2 again\n")


print("Session started\nSchedule:"+schedule+str(ratio)+"TO"+str(timeout)+"\nSession Length:"+str(sessionLength)+"sec\n")
time.sleep(1) # time to put the rat in the chamber
sTime=time.time()
lapsed=0

# delete mover to prevent overheating
del(mover)

subprocess.call("python3 operant1.py -schedule " +schedule+ " -ratio " +str(ratio)+ " -sessionLength " + str(sessionLength) + " -rat1ID " + rat1 + " -rat2ID " + rat2 + " -timeout " + str(timeout) +   " & ", shell=True)

while lapsed < sessionLength:
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
            print ("\n    inactive spout " + rfid + "\t")
            inactive.write(record)
            inactive.close()

    if (len(rfid)==8):
        record=rfid+"\t"+str(time.time())+"\n"
        with open(ROOT+"/_active", "w+") as active:
            active.write(record)
            active.close()
        with open(ROOT+"/"+date+"_active", "a+") as active:
            print ("\n      active spout " + rfid + "\t")
            active.write(record)
            active.close()

