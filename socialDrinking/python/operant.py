#!/usr/bin/env python3

import pigpio
from PigpioStepperMotor import StepperMotor
import sys
import argparse
import time
from threading import Timer
import RPi.GPIO as gpio
import datalogger
import subprocess
import os
import random
import board # MPR121
import busio # MPR121
import adafruit_mpr121
import ids
from pump_move import PumpMove
from gpiozero import DigitalInputDevice
import RPi.GPIO as GPIO


parser=argparse.ArgumentParser()
parser.add_argument('-schedule',  type=str, default="vr")
parser.add_argument('-ratio',  type=int, default=10)
parser.add_argument('-sessionLength',  type=int, default=3600)
parser.add_argument('-timeout',  type=int, default=20)
parser.add_argument('-rat1ID',  type=str, default="rat1")
parser.add_argument('-rat2ID',  type=str, default="rat2")
args=parser.parse_args()

# exp setting
schedule=args.schedule
ratio=args.ratio
sessionLength=args.sessionLength
timeout=args.timeout
rat1ID=args.rat1ID
rat2ID=args.rat2ID
rat0ID="ratUnknown"

## initiate pump motor
pi = pigpio.pi()

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)
# Create MPR121 object.
mpr121 = adafruit_mpr121.MPR121(i2c)

# Initialize GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

# GPIO usage 
TIR = int(16) # Pin 36
SW1 = int(26) # Pin 37
SW2 = int(20) # Pin 38
TOUCHLED = int(12) #pin 32
MOTIONLED= int(6) #pin 31

# Setup switch pins
gpio.setup(SW1, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(SW2, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(TIR, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(TOUCHLED, gpio.OUT)

# get date and time 
datetime=time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
session_start_time = time.strftime("%H:%M:%S", time.localtime())
date=time.strftime("%Y-%m-%d", time.localtime())

# deal with session and box ID, and data file location
ids=ids.IDS()

# Initialize data logger 
dlogger = datalogger.LickLogger(ids.devID, ids.sesID)
dlogger.createDataFile(schedule+str(ratio)+'TO'+str(timeout), rat1ID+"_"+rat2ID)

# Get start time
sTime = time.time()

# GLOBAL VARIABLES
FORWARD_LIMIT_BTN = 24
FORWARD_LIMIT_REACHED = False
# BACKWARD_LIMIT_BTN = 23
FORWARD_COUNTER = 0
touchcounter={rat0ID:0,rat1ID:0, rat2ID:0}
nextratio={rat0ID:0,rat1ID:ratio, rat2ID:ratio}
rew={rat0ID:0, rat1ID:0, rat2ID:0}
act={rat0ID:0, rat1ID:0, rat2ID:0}
ina={rat0ID:0, rat1ID:0, rat2ID:0}
act_licks_when_empty = {rat1ID:0, rat2ID: 0, rat0ID:0}

# lastActiveLick={rat0ID:float(sTime), rat1ID:float(sTime), rat2ID:float(sTime)}
# lastInactiveLick={rat0ID:float(sTime), rat1ID:float(sTime), rat2ID:float(sTime)}
lastActiveLick={rat0ID:{"time":float(sTime), "scantime": 0}, rat1ID:{"time":float(sTime), "scantime":0}, rat2ID:{"time":float(sTime), "scantime":0}}
lastInactiveLick={rat0ID:{"time":float(sTime), "scantime": 0}, rat1ID:{"time":float(sTime), "scantime":0}, rat2ID:{"time":float(sTime), "scantime":0}}


# FORWARD_LIMIT = DigitalInputDevice(18)
FORWARD_LIMIT = GPIO.setup(FORWARD_LIMIT_BTN, GPIO.IN, pull_up_down= GPIO.PUD_DOWN)

# BACKWARD_LIMIT = DigitalInputDevice(BACKWARD_LIMIT_BTN)


pumptimedout={rat0ID:False, rat1ID:False, rat2ID:False}
lapsed=0  # time since program start
updateTime=0 # time since last data print out 
vreinstate=0
minInterLickInterval=0.15 # minimal interlick interval (about 6-7 licks per second)
maxISI = 15  # max lapse between RFID scan and first lick in a cluster 
maxILI = 3 # max interval between licks used to turn an RFID into unknown.   


first_time_empty = False

def resetPumpTimeout(rat):
    pumptimedout[rat] = False

def colored_print(ratID, act_count, inact_count, reward_count, timeout):
    print (ratID+ \
           "\x1b[0;32;40m" + \
           ": Active=" + str(act_count)+ \
           "\x1b[0m" + \
           "\x1b[0;33;40m" + \
           " Inactive="+str(inact_count) + \
           "\x1b[0m" + \
           "\x1b[0;32;40m" + \
           " Reward=" +  str(reward_count) + \
           "\x1b[0m" + \
           "\x1b[0;35;40m" + \
           " Timeout: "+ str(timeout) + \
           "\x1b[0m"
          )

def showData(phase="progress"):
    if schedule=='pr':
        minsLeft=int((sessionLength-(time.time()-lastActiveLick[rat]))/60) ## need work, max of the two
    else:
        minsLeft=int((sessionLength-lapsed)/60)
    if phase=="final":
        print(ids.devID+  " Session_"+str(ids.sesID))
    print ("\x1b[0;31;40m" + \
           "[" + str(minsLeft) + " min Left]" + \
           "\x1b[0m")
    colored_print(rat1ID, act[rat1ID], ina[rat1ID], rew[rat1ID], pumptimedout[rat1ID])
    colored_print(rat2ID, act[rat2ID], ina[rat2ID], rew[rat2ID], pumptimedout[rat2ID])
    colored_print(rat0ID, act[rat0ID], ina[rat0ID], rew[rat0ID], pumptimedout[rat0ID])
    return time.time()

#if (vreinstate):
#    subprocess.call('python /home/pi/openbehavior/operantLicking/python/#blinkenlights.py -times 10 &', shell=True)

def set_empty_syringe_licks():
    for rat in act_licks_when_empty.keys():
        act_licks_when_empty[rat] = act[rat]


def get_rat_scantime(fname, thislick, lastlick):
    # lastlick can be either lastInactiveLick or lastActiveLick
    try:
        with open(fname, "r") as f:
            (rat, scantime, dummy1, dummy2) = f.read().strip().split("\t")
            scantime = float(scantime)
    except:
        rat="ratUnknown"
        scantime=0

    try:
        if rat is None or (thislick - lastlick[rat]["time"] > maxILI and thislick - scantime > maxISI):
            rat = "ratUnknown"
    except KeyError:
        print("\nrat={}\t thislick={}\t lastlick={}\t".format(rat, thislick, lastlick))
        
    return rat, scantime
house_light_on = False

while lapsed < sessionLength:
    if time.localtime().tm_hour >= 21 and house_light_on is False:
        # turn house light
        subprocess.call('sudo python ' + './blinkenlights.py &', shell=True)
        house_light_on = True # to void keep execute the subprocess
        

    time.sleep(0.05) # allow 20 licks per sec
    ina0 = mpr121.touched_pins[0]
    act1 = mpr121.touched_pins[1]
    lapsed = time.time() - sTime

    if GPIO.input(FORWARD_LIMIT_BTN):
        FORWARD_LIMIT_REACHED = True
        # dlogger.logEvent(rat, time.time(), "syringe empty", time.time()-sTime)
    if act1 == 1:
        thisActiveLick=time.time()
        (rat, scantime)= get_rat_scantime(fname="/home/pi/_active", thislick=thisActiveLick, lastlick=lastActiveLick)
        if(thisActiveLick - lastActiveLick[rat]["time"] > 1):
            lastActiveLick[rat]["time"] = thisActiveLick
            lastActiveLick[rat]["scantime"] = scantime
        else:
            act[rat]+=1
            if FORWARD_LIMIT_REACHED:
                if first_time_empty is False:
                    set_empty_syringe_licks()
                    first_time_empty = True

                dlogger.logEvent(rat, time.time(), "syringe empty", time.time()-sTime)
            else:
                dlogger.logEvent(rat,time.time() - lastActiveLick[rat]["scantime"], "ACTIVE", lapsed, nextratio[rat])
            lastActiveLick[rat]["time"]=thisActiveLick
            lastActiveLick[rat]["scantime"]=scantime

            updateTime=showData()
        #blinkCueLED(0.2)
        if not pumptimedout[rat]:
            touchcounter[rat] += 1 # for issuing rewards
            if touchcounter[rat] >= nextratio[rat]  and rat !="ratUnknown":
                rew[rat]+=1
                #print("reward for "+rat+":"+str(rew[rat]))
                touchcounter[rat] = 0
                pumptimedout[rat] = True
                pumpTimer = Timer(timeout, resetPumpTimeout, [rat])
                print ("timeout on " + rat)
                pumpTimer.start()
                # subprocess.call('python ' + './blinkenlights.py -times 1&', shell=True)
                
                subprocess.call('sudo python ' + './blinkenlights.py -reward_happened True&', shell=True)

                # if(not FORWARD_LIMIT.value):
                if FORWARD_LIMIT_REACHED:
                    dlogger.logEvent(rat, time.time(), "syringe empty", time.time()-sTime)
                else:
                    dlogger.logEvent(rat, time.time()-scantime, "REWARD", time.time()-sTime)
                    mover = PumpMove()
                    if(float(sessionLength) / 3600  == 16.0):
                        mover.move("forward", 130) # 20ML syringe 60µL solution
                    else:
                        mover.move("forward", 150) # 10ML syringe 60µL solution
                    del(mover)
                updateTime=showData()
                if schedule == "fr":
                    nextratio[rat]=ratio
                elif schedule == "vr":
                    nextratio[rat]=random.randint(1,ratio*2)
                elif schedule == "pr":
                    breakpoint+=1.0
                    nextratio[rat]=int(5*2.72**(breakpoint/5)-5)
    elif ina0 == 1:
        thisInactiveLick=time.time()
        (rat, scantime)= get_rat_scantime(fname="/home/pi/_inactive", thislick=thisInactiveLick, lastlick=lastInactiveLick)
        if(thisInactiveLick - lastInactiveLick[rat]["time"] > 1):
            lastInactiveLick[rat]["time"] = thisInactiveLick
            lastInactiveLick[rat]["scantime"] = scantime
        else:
            ina[rat]+=1
#            if FORWARD_LIMIT_REACHED:
#                dlogger.logEvent(rat, time.time(), "syringe empty", time.time()-sTime)
#            else:
            dlogger.logEvent(rat,time.time() - lastInactiveLick[rat]["scantime"], "INACTIVE", lapsed)
            lastInactiveLick[rat]["time"]=thisInactiveLick
            lastInactiveLick[rat]["scantime"]=scantime
            updateTime=showData()

    # keep this here so that the PR data file will record lapse from sesion start 
    if schedule=="pr":
        lapsed = time.time() - lastActiveLick
    #show data if idle more than 1 min 
    if time.time()-updateTime > 60*1:
        updateTime=showData()

# signal the motion script to stop recording
#if schedule=='pr':
#    with open("/home/pi/prend", "w") as f:
#        f.write("yes")

dlogger.logEvent("", time.time(), "SessionEnd", time.time()-sTime)

formatted_schedule = schedule+str(ratio)+'TO'+str(timeout)+"_"+ rat1ID+"_"+rat2ID
schedule_to = schedule+str(ratio)+'TO'+str(timeout)
finallog_fname = "Soc_{}_{}_S{}_{}_summary.tab".format(datetime,ids.devID,ids.sesID,formatted_schedule)
data_dict = {
            "ratID1":[rat1ID, date, session_start_time, ids.devID, ids.sesID, schedule_to, sessionLength, act[rat1ID], ina[rat1ID], rew[rat1ID], act_licks_when_empty[rat1ID]],
            "ratID2":[rat2ID, date, session_start_time, ids.devID, ids.sesID, schedule_to, sessionLength, act[rat2ID], ina[rat2ID], rew[rat2ID], act_licks_when_empty[rat2ID]],
            "ratID0":[rat0ID, date, session_start_time, ids.devID, ids.sesID, schedule_to, sessionLength, act[rat0ID], ina[rat0ID], rew[rat0ID], act_licks_when_empty[rat0ID]]
            }
datalogger.LickLogger.finalLog(finallog_fname, data_dict)


print(str(ids.devID) +  "Session" + str(ids.sesID) + " Done!\n")
showData("final")
subprocess.call('/home/pi/openbehavior/wifi-network/rsync.sh &', shell=True)
print(ids.devID+  "Session"+ids.sesID + " Done!\n")
showData("final")


