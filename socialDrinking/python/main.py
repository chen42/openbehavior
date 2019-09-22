#!/usr/bin/env python3

import pigpio
from PigpioStepperMotor import StepperMotor
import sys
import getopt
import time
from threading import Timer
import subprocess
import RPi.GPIO as gpio
import serial
import datalogger
import os
import random
import board # MPR121
import busio # MPR121
import adafruit_mpr121
from ids import IDS

ROOT="."

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

def printUsage():
    print(sys.argv[0] + ' -t <timeout> -f <fixed ratio>')

def resetPumpTimeout():
    global pumptimedout
    pumptimedout = False

#def blinkTouchLED(duration):
#    gpio.output(TOUCHLED, gpio.HIGH)
#    time.sleep(duration)
#    gpio.output(TOUCHLED, gpio.LOW)

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

# Run the deviceinfo script
#mesg("Hurry up, Wifi!")
#os.system("/home/pi/openbehavior/wifi-network/deviceinfo.sh")


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

print("Session started\nSchedule:"+schedule+str(ratio)+"TO"+str(timeout)+"\nSession Length:"+str(sessionLength)+"sec\n")

rat1=input("please scan rat1\n")
rat2=input("please scan rat2\n")
with open ("ratids", "w+") as ratids:
    ratids.write(rat1+"_"+rat2)
    ratids.close()

ids=IDS() ## read in session id, ratid, boxid, etc.
 
#turn lights off to indicate RFID recieved
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
dlogger.createDataFile(schedule+str(ratio)+'TO'+str(timeout))

# Get start time
sTime = time.time()
lastActiveLick=sTime
lastInactiveLick=sTime

def showdata():
    if schedule=='pr':
        minsLeft=int((sessionLength-(time.time()-lastActiveLick))/60)
    else:
        minsLeft=int((sessionLength-lapsed)/60)
    print("B" + ids.devID+  "S"+ids.sesID + " " + ids.ratID+ " " + str(minsLeft) + "Left\n"+ "a" + str(act)+"i"+str(ina) + "r" +  str(rew) + schedule + str(nextratio))
    return time.time()


#if (vreinstate):
#    subprocess.call('python /home/pi/openbehavior/operantLicking/python/#blinkenlights.py -times 10 &', shell=True)

while lapsed < sessionLength:
    time.sleep(0.05) # set delay to adjust sensitivity of the sensor.
    ina0 = mpr121.touched_pins[0]
    act1 = mpr121.touched_pins[1]
    lapsed = time.time() - sTime
    if act1 == 1:
        #thisActiveLick=time.time() 
        #print ("act=" + str(act) +  " rew= "+str(rew)+" nextratio=" + str(nextratio)+" counter="+str(touchcounter))
        #only count licks that are within interlick interval to exclude noise
        # need to deal with not skipping the first lick in a series
        #if thisActiveLick-lastActiveLick < interLickInterval: # rat licks in rapid sucsession
        #if thisActiveLick-lastActiveLick < 1: # rat licks in rapid sucsession
            #print ("this one counts, timeout?", str(pumptimedout))
        #if (lastActiveLick not in logged): 
        act+=1
        dlogger.logEvent(str(time.time()), "ACTIVE", lapsed, nextratio)
        #blinkTouchLED(0.2)
        #act+=1
        #dlogger.logEvent("ACTIVE", lapsed)
        if not pumptimedout:
            touchcounter += 1 # for issuing rewards
        #    if (lastActiveLick not in logged):
        #        touchcounter += 1
            if touchcounter >= nextratio:
                rew+=1
        #       updateTime=showdata()
                dlogger.logEvent(str(time.time()), "REWARD", time.time()-sTime, nextratio)
                touchcounter = 0
                pumptimedout = True
                pumpTimer = Timer(timeout, resetPumpTimeout)
                pumpTimer.start()
                subprocess.call('python ' + ROOT + '/blinkenlights.py -times 1&', shell=True)
                pumpforward() # This is 60ul
                if schedule == "fr":
                    nextratio=ratio
                elif schedule == "vr":
                    nextratio=random.randint(1,ratio*2)
                elif schedule == "pr":
                    breakpoint+=1.0
                    nextratio=int(5*2.72**(breakpoint/5)-5)
            #else:
            #    updateTime=showdata()
        #logged[thisActiveLick]=1
        #lastActiveLick=thisActiveLick
    elif ina0 == 1:
        #thisInactiveLick=time.time() 
        # only count licks that are within interlick interval to exclude noise
        # need to deal with not skipping the first lick in a series
        #if thisInactiveLick-lastInactiveLick < interLickInterval: # rat licks in rapid sucsession
            ##if (lastInactiveLick not in logged): 
            #    ina+=1
            #    dlogger.logEvent(str(time.time()),"INACTIVE", lastInactiveLick-sTime)
        ina+=1
        dlogger.logEvent(str(time.time()), "INACTIVE", lapsed)
        #blinkTouchLED(0.02)
        #logged[thisInactiveLick]=1
        #lastInactiveLick=thisInactiveLick
        #blinkTouchLED(0.05)
        #updateTime=showdata()
    #elif time.time() - updateTime > 60:
    #    updateTime=showdata()
    # keep this here so that the PR data file will record lapse from sesion start 
    if schedule=="pr":
        lapsed = time.time() - lastActiveLick 
#        print ("prlaps", lapsed)
# signal the motion script to stop recording
#if schedule=='pr':
#    with open("/home/pi/prend", "w") as f:
#        f.write("yes")

dlogger.logEvent("", "SessionEnd", time.time()-sTime)

print("Box" + ids.devID+  "Session"+ids.sesID + " " + ids.ratID + " Done!\n" + "a" + str(act)+"i"+str(ina) + "r" +  str(rew)) 

#subprocess.call('/home/pi/openbehavior/wifi-network/rsync.sh &', shell=True)
