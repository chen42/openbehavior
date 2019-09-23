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

parser=argparse.ArgumentParser()
parser.add_argument('-schedule',  type=str, default="vr")
parser.add_argument('-ratio',  type=int, default=10)
parser.add_argument('-sessionLength',  type=int, default=3600)
parser.add_argument('-timeout',  type=int, default=20)
parser.add_argument('-rat1ID',  type=str, default="rat1")
parser.add_argument('-rat2ID',  type=str, default="rat2")
args=parser.parse_args()

schedule=args.schedule
ratio=args.ratio
sessionLength=args.sessionLength
timeout=args.timeout
rat1ID=args.rat1ID
rat2ID=args.rat2ID
nextratio=ratio

minInterLickInterval=0.15 # minimal ILI (about 6-7 licks per second)


'''
# connection to adafruit TB6612
# motor: SY28STH32-0674A
Vcmotor --> 12V 5A power supply
VM --> floating
Vcc --> 3V3 Pin 17
GND --> GND Pin 06
PwmA --> 3V3 Pin 01
AIN2 --> Pin 15 - BCM 22
AIN1 --> Pin 11 - BCM 17
STBY --> Pin 13 - BCM 27
BIN1 --> Pin 16 - BCM 23
BIN2 --> Pin 18 - BCM 24
PwmB --> Pin 32 - BCM
MotorA --> Red (A+) and Green (A-) wires
MotorB --> Blue (B+) and Black (B-) wires
GND of Power supply --> Pin 39 (gnd) Raspberry Pi
'''
# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)
# Create MPR121 object.
mpr121 = adafruit_mpr121.MPR121(i2c)
 
# motor code from https://www.raspberrypi.org/forums/viewtopic.php?t=220247#p1352169
# pip3 install pigpio
# git clone https://github.com/stripcode/pigpio-stepper-motor

## initiate pump motor
pi = pigpio.pi()
motor = StepperMotor(pi, 17, 23, 22, 24)
pwma = pigpio.pi()
pwma.write(18,1)
pwmb = pigpio.pi()
pwmb.write(12,1)
stby = pigpio.pi()
stby.write(27,0)

def pumpforward(x=80): #x=80 is 60ul
    for i in range(x):
        stby.write(27,1)
        motor.doClockwiseStep()

def resetPumpTimeout():
    global pumptimedout
    pumptimedout = False

# BEGIN CONSTANT DEFINITIONS
TIR = int(16) # Pin 36
SW1 = int(26) # Pin 37
SW2 = int(20) # Pin 38
TOUCHLED = int(12) #pin 32
MOTIONLED= int(6) #pin 31
# END CONSTANT DEFINITIONS

# BEGIN GLOBAL VARIABLES
interLickInterval=1 # second
logged={}
touchcounter = 0
pumptimedout = False
act=0 # number of licks on the active spout
ina=0 # number of licks on the inactive spout
rew=0 # number of reward
lapsed=0  # time since program start
updateTime=0 # time since last LCD update
vreinstate=0
# ENG GLOBAL VARIABLES

# Initialize GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

# Setup switch pins
gpio.setup(SW1, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(SW2, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(TIR, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(TOUCHLED, gpio.OUT)

# get date and time 
datetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
date=time.strftime("%Y-%m-%d", time.localtime())

ids=ids.IDS() ## read in session id, boxid, etc.
 
#RatIDs=rat1ID+"_"+rat2ID

# Initialize data logger 
dlogger = datalogger.LickLogger(ids.devID, ids.sesID)
dlogger.createDataFile(schedule+str(ratio)+'TO'+str(timeout), rat1ID+"_"+rat2ID)

# Get start time
sTime = time.time()
lastActiveLick=sTime
lastInactiveLick=sTime
lastInactiveLick=sTime

def showData():
    if schedule=='pr':
        minsLeft=int((sessionLength-(time.time()-lastActiveLick))/60)
    else:
        minsLeft=int((sessionLength-lapsed)/60)
    print(ids.devID+  " Session_"+str(ids.sesID) + " "+ str(schedule) + str(nextratio) + " [" + str(minsLeft) + " min Left]\n"+ "Active: " + str(act)+" Inactive: "+str(ina) + " Reward: " +  str(rew) + "\n")
    return time.time()



#if (vreinstate):
#    subprocess.call('python /home/pi/openbehavior/operantLicking/python/#blinkenlights.py -times 10 &', shell=True)

while lapsed < sessionLength:
    #time.sleep(0.05) # set delay to adjust sensitivity of the sensor.
    ina0 = mpr121.touched_pins[0]
    act1 = mpr121.touched_pins[1]
    lapsed = time.time() - sTime
    #show data if idle more than 1 min 
    if time.time()-updateTime > 60:
        updateTime=showData()
    if act1 == 1:
        f=open("/home/pi/_active", "r")
        rat=f.read().strip()
        f.close()
        thisActiveLick=time.time() 
        if thisActiveLick-lastActiveLick > minInterLickInterval: # rat licks in rapid sucsession
            act+=1
            dlogger.logEvent(rat, time.time(), "ACTIVE", lapsed, nextratio)
            lastActiveLick=thisActiveLick
            updateTime=showData()
            #blinkCueLED(0.2)
            if not pumptimedout:
                touchcounter += 1 # for issuing rewards
                if touchcounter >= nextratio:
                    rew+=1
                    dlogger.logEvent(rat, time.time(), "REWARD", time.time()-sTime, nextratio)
                    touchcounter = 0
                    pumptimedout = True
                    pumpTimer = Timer(timeout, resetPumpTimeout)
                    pumpTimer.start()
                    subprocess.call('python ' + './blinkenlights.py -times 1&', shell=True)
                    pumpforward() # This is 60ul
                    updateTime=showData()
                    if schedule == "fr":
                        nextratio=ratio
                    elif schedule == "vr":
                        nextratio=random.randint(1,ratio*2)
                    elif schedule == "pr":
                        breakpoint+=1.0
                        nextratio=int(5*2.72**(breakpoint/5)-5)
        #logged[thisActiveLick]=1
        #lastActiveLick=thisActiveLick
    elif ina0 == 1:
        thisInactiveLick=time.time() 
        # only count licks that are within interlick interval to exclude noise
        # need to deal with not skipping the first lick in a series
        #if thisInactiveLick-lastInactiveLick < interLickInterval: # rat licks in rapid sucsession
            ##if (lastInactiveLick not in logged): 
            #    ina+=1
            #    dlogger.logEvent(str(time.time()),"INACTIVE", lastInactiveLick-sTime)
        if thisInactiveLick-lastInactiveLick > minInterLickInterval: 
            f=open("/home/pi/_inactive", "r")
            rat=f.read().strip()
            f.close()
            ina+=1
            dlogger.logEvent(rat, time.time(), "INACTIVE", lapsed)
            lastInactiveLick=thisInactiveLick
            updateTime=showData()
    # keep this here so that the PR data file will record lapse from sesion start 
    if schedule=="pr":
        lapsed = time.time() - lastActiveLick 
# signal the motion script to stop recording
#if schedule=='pr':
#    with open("/home/pi/prend", "w") as f:
#        f.write("yes")

dlogger.logEvent("", time.time(), "SessionEnd", time.time()-sTime)

print("Box" + ids.devID+  "Session"+ids.sesID + " " + ids.ratID + " Done!\n" + "a" + str(act)+"i"+str(ina) + "r" +  str(rew)) 

#subprocess.call('/home/pi/openbehavior/wifi-network/rsync.sh &', shell=True)
