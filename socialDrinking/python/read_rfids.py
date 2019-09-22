#!/usr/bin/env python3

## records the time each RFID is detected and sort them into active vs inactive spout
## active spout is 10 digit hex, inactive spout is 8 digit hex.

import os
import time

# get date and time
date=time.strftime("%Y-%m-%d", time.localtime())

while True:
    hms=time.strftime("%H:%M:%S", time.localtime())
    rfid=input("waiting for RFID\n")

    if (len(rfid)==10):
        with open("_inactive", "w+") as inactive:
            inactive.write(rfid+"\t"+time.time())
            inactive.close()
        with open(date+"_inactive", "a+") as inactive:
            inactive.write(hms+"\t"+rfid+"\n")
            inactive.close()

    if (len(rfid)==8):
        with open("_active", "w+") as active:
            active.write(rfid+"\t"+time.time())
            active.close()
        with open(date+"_active", "a+") as active:
            active.write(hms+"\t"+rfid+"\n")
            active.close()


