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

#### PUMP and BUTTON
# start the pump after the command ID is scanned
mover = PumpMove()
forwardbtn = Button("GPIO5")
backwardbtn = Button("GPIO27")

BACKWARD_LIMIT_BTN = "GPIO23"
BACKWARD_LIMIT = DigitalInputDevice(BACKWARD_LIMIT_BTN)


RatID = ""
while RatID == "":
   if forwardbtn.value == 1 and backwardbtn.value == 1:
       print("You can now adjust the pump")
       def forward():
           while forwardbtn.value == 1:
               mover.move("forward")
        def backward():
            while BACKWARD_LIMIT.value != 1:
                mover.move("backward")
        forwardbtn.when_pressed = forward
        backwardbtn.when_pressed = backward
    RatID = input("please scan a command RFID\n")[-8:]

del(mover)

command_ids = [
    "0084cb3c",
    "002cd652",
    "002ba76f",
    "002c7365",
    "002c94ef",
    "002ceeb8",
    "0087739a",
    "002d54ff",
    "0084668e",

    "002cd488",
    "002cbc8f",
    "002b51b9",
    "002d558c",
    "002d3da7",
    "002b397e",
    "002c732f",
    "002b392d",
    "002cdfc3",
]


while RatID not in command_ids:
    RatID = input("command ID not found, please rescan the id: ")[-8:]

# the default schedule is vr10 timeout10. Other reinforcemnt schedules can be started by using RFIDs.
if RatID[-2:] == "3c" or RatID[-2:] == "88": # PR
    schedule="pr"
    breakpoint=2
    timeout = 10
    nextratio=int(5*2.72**(breakpoint/5)-5)
    sessionLength=20*60 # session ends after 20 min inactivity
    ratio=""
    #signal motion sensor to keep recording until this is changed
    with open ("ROOT/prend", "w") as f:
        f.write("no")
elif RatID[-2:] == "52" or RatID[-2:] == "8f":  #FR5 1h
    schedule="fr"
    ratio = 5
    timeout =  10
    sessionLength=60*60*1 # one hour assay
    nextratio=ratio
elif RatID[-2:] == "6f" or RatID[-2:] == "b9": # FR5, 16h 
    schedule="fr"
    ratio = 5
    timeout =  10
    sessionLength=60*60*16 # one hour assay
    nextratio=ratio
elif RatID[-2:] == "65" or RatID[-2:] == "8c": # extinction
    schedule="ext"
    timeout=0
    ratio=1000000
    nextratio=1000000
    sessionLength=60*60*1
elif RatID[-2:] == "ef" or RatID[-2:] == "a7": #VR10, 1h
    schedule="vr"
    ratio = 10
    timeout =  10
    sessionLength=60*60*1 #
    nextratio=ratio
elif RatID[-2:] == "b8" or RatID[-2:] == "7e": #VR10, 2h
    schedule="vr"
    ratio = 10
    timeout =  10
    sessionLength=60*60*2 #
    nextratio=ratio
elif RatID[-2:] == "9a" or RatID[-2:] == "2f": #VR10, 4h
    schedule="vr"
    ratio = 10
    timeout =  10
    sessionLength=60*60*4 #
    nextratio=ratio
elif RatID[-2:] == "ff" or RatID[-2:] == "2d": #VRreinstate, 4h
    vreinstate=1
    schedule="vr"
    ratio = 5
    timeout = 1
    sessionLength=60*60*4 # one hour assay
    nextratio=ratio
    RatID=ReadRFID("/dev/ttyAMA0")
elif RatID[-2:] == "8e" or RatID[-2:] == "c3": # vr10 16h
    schedule="vr"
    ratio=10
    nextratio=ratio
    timeout = 10
    sessionLength=60*60*16



h=str(int(sessionLength/3600))
print("Run " + schedule + str(ratio) + "for "  + h + "h\n")

rat1 = "rat1"
rat2 = "rat2"

print("Session started\nSchedule:"+schedule+str(ratio)+"TO"+str(timeout)+"\nSession Length:"+str(sessionLength)+"sec\n")
# start time
sTime=time.time()
lapsed=0

# delete mover to prevent overheating
# del(mover)

subprocess.call("python3 operant.py -schedule " +schedule+ " -ratio " +str(ratio)+ " -sessionLength " + str(sessionLength) + " -rat1ID " + rat1 + " -rat2ID " + rat2 + " -timeout " + str(timeout) +   " & ", shell=True)
