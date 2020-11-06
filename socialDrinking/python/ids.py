#!/usr/bin/python3 


import os
import time

ROOT='/home/pi'
DEVID_FILE = ROOT+'/deviceid'
RATID_FILE = ROOT+'/ratids'
SESSIONID_FILE = ROOT+'/sessionid'
DATA_DIR = ROOT+'/SocialDrinking'
DATA_PREFIX = "/Soc_"

COMMAND_IDS = [
    "0084cb3c",
    "002cd652",
    "002ba76f",
    "002c7365",
    "002c94ef",
    "0087739a",
    "002d54ff",
    "0084668e",

    "002cd488",
    "002cbc8f",
    "002b51b9",
    "002d558c",
    "002d3da7",
    "002c732f",
    "002b392d",
    "002cdfc3",
]

with open (ROOT+"/_active", "w") as act:
    act.write("ratUnknown\t"+str(time.time()))
    act.close()

with open (ROOT+"/_inactive", "w") as inact:
    inact.write("00ratUnknown\t"+str(time.time()))
    inact.close()

if not os.path.exists(DEVID_FILE):
    print ("please edit " + DEVID_FILE + " to assign device ID")
    with open (DEVID_FILE, 'w') as devID:
        devID.write("BOX_X")
        devID.close()
if not os.path.exists(SESSIONID_FILE):
    print ("please edit " + SESSIONID_FILE + " to assign initial session ID")
    with open (SESSIONID_FILE, 'w') as sessionID:
        sessionID.write("1")
        sessionID.close()

if not os.path.exists(DATA_DIR):
    os.system("mkdir " + DATA_DIR)

class IDS:
    def __init__(self):
        with open (DEVID_FILE) as devID:
            self.devID = str((devID.read()).strip())
            devID.close()
        with open (SESSIONID_FILE, "r") as sessID:
            self.sesID=int(sessID.read().strip())
            #newSesID=self.sesID+1
            #sessID.seek(0)
            #sessID.write(str(newSesID))
            #sessID.close()
    def sessionIncrement(self):
        with open (SESSIONID_FILE, "r+") as sessID:
            self.sesID=int(sessID.read().strip())
            newSesID=self.sesID+1
            self.sesID = newSesID
            sessID.seek(0)
            sessID.write(str(newSesID))
            

