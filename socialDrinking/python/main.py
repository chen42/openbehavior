#!/usr/bin/python

# Copyright 2019 University of Tennessee Health Sciences Center
# Author: Hao Chen <hchen@uthsc.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or(at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# BEGIN IMPORT PRELUDE
import pigpio
from PigpioStepperMotor import StepperMotor
import sys
import getopt
import time
from threading import Timer
import subprocess32 as subprocess
import RPi.GPIO as gpio
import Adafruit_MPR121.MPR121 as MPR121
import serial
import touchsensor
import datalogger
import os
import random
#import Adafruit_CharLCD as LCD
# END IMPORT PRELUDE


# pump code from https://www.raspberrypi.org/forums/viewtopic.php?t=220247#p1352169
# pip3 install pigpio
# git clone https://github.com/stripcode/pigpio-stepper-motor

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

## initiate pump motor
pi = pigpio.pi()
motor = StepperMotor(pi, 17, 23, 22, 24)
pwma = pigpio.pi()
pwma.write(18,1)
pwmb = pigpio.pi()
pwmb.write(12,1)
stby = pigpio.pi()
stby.write(27,0)

def pumpforward(x):
    for i in range(x):
        stby.write(27,1)
        motor.doClockwiseStep()

def printUsage():
    print(sys.argv[0] + ' -t <timeout> -f <fixed ratio>')

def resetPumpTimeout():
    global pumptimedout
    pumptimedout = False

def blinkTouchLED(duration):
    gpio.output(TOUCHLED, gpio.HIGH)
    time.sleep(duration)
    gpio.output(TOUCHLED, gpio.LOW)

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
#updateTime=0 # time since last LCD update
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

# Run the deviceinfo script
#mesg("Hurry up, Wifi!")
#os.system("/home/pi/openbehavior/wifi-network/deviceinfo.sh")

# Initialize touch sensor
tsensor = touchsensor.TouchSensor()

# device id
#dId=open("/home/pi/deviceid")
#deviceId=dId.read().strip()

# get date and time 
datetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# the default schedule is vr10 timeout20. Other reinforcemnt schedules can be started by using RFIDs.
if RatID=="1E003E3B0C17" or RatID=="2E90EDD235B4":
    schedule="pr"
    breakpoint=2.0
    timeout = 20
    nextratio=int(5*2.72**(breakpoint/5)-5)
    sessionLength=10*60 # session ends after 10 min inactivity
    ratio=""
    print("Run PR Schedule.\nPls Scan Rat")
    time.sleep(3)
    RatID=ReadRFID("/dev/ttyAMA0")
    #signal motion sensor to keep recording until this is changed
    with open ("/home/pi/prend", "w") as f:
        f.write("no")
elif RatID=="2E90EDD079FA" or RatID=="2E90EDD071F2":
    schedule="fr"
    ratio = 2
    timeout =  20
    sessionLength=60*60*1 # one hour assay
    nextratio=ratio
    print("Run FR"+str(ratio)+" Prog.\nPls Scan Rat")
    time.sleep(3)
    RatID=ReadRFID("/dev/ttyAMA0")
elif RatID=="2E90EDD20283" or RatID=="2E90EDD226A7":
    schedule="ext"
    timeout=0
    ratio=1000000
    nextratio=1000000
    sessionLength=60*60*1
    print("Run Ext"+str(ratio)+" Prog.\nPls Scan Rat")
    time.sleep(3)
    RatID=ReadRFID("/dev/ttyAMA0")
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

print(schedule+ratio+"TO"+timeout+"session Length="+sessionLength+"sec\n")
rat1=input("please scan rat1")
rat2=input("please scan rat2")

#turn lights off to indicate RFID recieved
print("Session Started")
#gpio.output(TOUCHLED, gpio.LOW)
#gpio.output(MOTIONLED, gpio.LOW)

# session id 
#with open ("/home/pi/sessionid", "r+") as f:
#    storedSessionID=f.read().strip()
#    sessionID=int(storedSessionID)+1  
#    f.seek(0)
#    f.write(str(sessionID))
#    f.close()

# start motion sensor Note: motion sensor needs to be started before session ID is incremented
# print ("staring motion sensor")
#subprocess.call("sudo python /home/pi/openbehavior/operantLicking/python/#motion.py " +  " -SessionLength " + str(sessionLength) + " -RatID " + #RatID +  " -Schedule " + schedule + " &", shell=True)

RatID=rat1+"_"+rat2
# Initialize data logger 
dlogger = datalogger.LickLogger()
dlogger.createDataFile(RatID, schedule+str(ratio)+'TO'+str(timeout))

# Get start time
sTime = time.time()
lastActiveLick=sTime
lastInactiveLick=sTime

def showdata():
    if schedule=='pr':
        minsLeft=int((sessionLength-(time.time()-lastActiveLick))/60)
    else:
        minsLeft=int((sessionLength-lapsed)/60)
    print("B" + deviceId[-2:]+  "S"+str(sessionID) + " " + RatID[-4:] + " " + str(minsLeft) + "Left\n"+ "a" + str(act)+"i"+str(ina) + "r" +  str(rew) + schedule + str(nextratio))
    return time.time()


#if (vreinstate):
#    subprocess.call('python /home/pi/openbehavior/operantLicking/python/#blinkenlights.py -times 10 &', shell=True)

while lapsed < sessionLength:
    time.sleep(0.05) # set delay to adjust sensitivity of the sensor.
    lapsed = time.time() - sTime
    i = tsensor.readPinTouched()
    if i == 1:
        thisActiveLick=time.time() 
        print ("act=" + str(act) +  " rew= "+str(rew)+" nextratio=" + str(nextratio)+" counter="+str(touchcounter))
        # only count licks that are within interlick interval to exclude noise
        # need to deal with not skipping the first lick in a series
        if thisActiveLick-lastActiveLick < interLickInterval: # rat licks in rapid sucsession
            #print ("this one counts, timeout?", str(pumptimedout))
            if (lastActiveLick not in logged): 
                act+=1
                dlogger.logEvent("ACTIVE", lastActiveLick-sTime)
            act+=1
            dlogger.logEvent("ACTIVE", lapsed)
            blinkTouchLED(0.02)
            if not pumptimedout:
                touchcounter += 1
                if (lastActiveLick not in logged):
                    touchcounter += 1
                if touchcounter >= nextratio:
                    rew+=1
                    updateTime=showdata()
                    dlogger.logEvent("REWARD", lapsed, nextratio)
                    touchcounter = 0
                    pumptimedout = True
                    pumpTimer = Timer(timeout, resetPumpTimeout)
                    pumpTimer.start()
                    subprocess.call('python /home/pi/openbehavior/operantLicking/python/blinkenlights.py &', shell=True)
                    pumpforward(0.08) # This is 60ul
                    if schedule == "fr":
                        nextratio=ratio
                    elif schedule == "vr":
                        nextratio=random.randint(1,ratio*2)
                    elif schedule == "pr":
                        breakpoint+=1.0
                        nextratio=int(5*2.72**(breakpoint/5)-5)
                else:
                    updateTime=showdata()
#           logged[lastActiveLick]=1
            logged[thisActiveLick]=1
        lastActiveLick=thisActiveLick
    elif i == 2:
        thisInactiveLick=time.time() 
        # only count licks that are within interlick interval to exclude noise
        # need to deal with not skipping the first lick in a series
        if thisInactiveLick-lastInactiveLick < interLickInterval: # rat licks in rapid sucsession
            if (lastInactiveLick not in logged): 
                ina+=1
                dlogger.logEvent("INACTIVE", lastInactiveLick-sTime)
            ina+=1
            dlogger.logEvent("INACTIVE", lapsed)
            blinkTouchLED(0.02)
            logged[thisInactiveLick]=1
        lastInactiveLick=thisInactiveLick
        blinkTouchLED(0.05)
        updateTime=showdata()
#    elif i == 0:
#        wat+=1
#        dlogger.logEvent("WATER", lapsed)
#        blinkTouchLED(0.05)
#        updateTime=showdata()
    elif time.time() - updateTime > 60:
        updateTime=showdata()
    # keep this here so that the PR data file will record lapse from sesion start 
    if schedule=="pr":
        lapsed = time.time() - lastActiveLick 
#        print ("prlaps", lapsed)
 
# signal the motion script to stop recording
#if schedule=='pr':
#    with open("/home/pi/prend", "w") as f:
#        f.write("yes")

dlogger.logEvent("SessionEnd", time.time()-sTime)

print("Box" + deviceId[-2:]+  "Session"+str(sessionID) + " " + RatID[-4:] + " Done!\n" + "a" + str(act)+"i"+str(ina) + "r" +  str(rew)) 

subprocess.call('/home/pi/openbehavior/wifi-network/rsync.sh &', shell=True)
