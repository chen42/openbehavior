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
# from pump_move import PumpMove
# from gpiozero import InputDevice
# from gpiozero import Servo
# from gpiozero import Button
import RPi.GPIO as GPIO
import mover_subproc

# import mover_subproc
# subprocess.call("python3 ./mover_subproc.py")

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

# touch sensor  mpr121
SDA
SCL
5V
GND

# Cue LED
GND

'''
print("inside operant1")


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

# motor code from https://www.raspberrypi.org/forums/viewtopic.php?t=220247#p1352169
# pip3 install pigpio
# git clone https://github.com/stripcode/pigpio-stepper-motor

## initiate pump motor
pi = pigpio.pi()
# motor = StepperMotor(pi, 17, 23, 22, 24)
# pwma = pigpio.pi()
# pwma.write(18,1)
# pwmb = pigpio.pi()
# pwmb.write(12,1)
# stby = pigpio.pi()
# stby.write(27,0)

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
datetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
date=time.strftime("%Y-%m-%d", time.localtime())

# deal with session and box ID, and data file location
ids=ids.IDS()

# Initialize data logger 
dlogger = datalogger.LickLogger(ids.devID, ids.sesID)
dlogger.createDataFile(schedule+str(ratio)+'TO'+str(timeout), rat1ID+"_"+rat2ID)

# Get start time
sTime = time.time()

# GLOBAL VARIABLES
touchcounter={rat0ID:0,rat1ID:0, rat2ID:0}
nextratio={rat0ID:0,rat1ID:ratio, rat2ID:ratio}
rew={rat0ID:0, rat1ID:0, rat2ID:0}
act={rat0ID:0, rat1ID:0, rat2ID:0}
ina={rat0ID:0, rat1ID:0, rat2ID:0}
lastActiveLick={rat0ID:float(sTime), rat1ID:float(sTime), rat2ID:float(sTime)}
lastInactiveLick={rat0ID:float(sTime), rat1ID:float(sTime), rat2ID:float(sTime)}
pumptimedout={rat0ID:False, rat1ID:False, rat2ID:False}
lapsed=0  # time since program start
updateTime=0 # time since last data print out 
vreinstate=0
minInterLickInterval=0.15 # minimal interlick interval (about 6-7 licks per second)
maxISI = 15  # max lapse between RFIC scan and first lick in a cluster 
maxILI = 2 # max inter lick interval in seconds  



def pumpforward(x=180): #x=80 is 60ul
    for i in range(x):
        stby.write(27,1)
        motor.doClockwiseStep()

def resetPumpTimeout(rat):
    pumptimedout[rat] = False

def showData(phase="progress"):
    if schedule=='pr':
        minsLeft=int((sessionLength-(time.time()-lastActiveLick[rat]))/60) ## need work, max of the two
    else:
        minsLeft=int((sessionLength-lapsed)/60)
    if phase=="final":
        print(ids.devID+  " Session_"+str(ids.sesID))
    print ("[" + str(minsLeft) + " min Left]")
    print (rat1ID+": Active=" + str(act[rat1ID])+" Inactive="+str(ina[rat1ID]) + " Reward=" +  str(rew[rat1ID]) + " Timeout: "+ str(pumptimedout[rat1ID]))
    print (rat2ID+": Active=" + str(act[rat2ID])+" Inactive="+str(ina[rat2ID]) + " Reward=" +  str(rew[rat2ID]) + " Timeout: "+ str(pumptimedout[rat2ID]) + "\n")
    print (rat0ID+": Active=" + str(act[rat0ID])+" Inactive="+str(ina[rat0ID]) + " Reward=" +  str(rew[rat0ID]) + " Timeout: "+ str(pumptimedout[rat0ID]) + "\n")
    return time.time()



#################################################################
# new pump mover code
# mover = PumpMove()

# SERVO = 2
# RECEIVER = 26

# FORWARDBUTTON = 5 #16
# BACKWARDBUTTON = 27 #12


# IR = 17
# # SERVO = 27
# sensor = InputDevice(IR, pull_up=True)
# # servo = Servo(SERVO, initial_value=None)

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(FORWARDBUTTON,GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(BACKWARDBUTTON,GPIO.IN, pull_up_down=GPIO.PUD_UP)

# while True:
#     if FORWARDBUTTON.is_pressed:
#         mover.move("forward")
#     elif BACKWARDBUTTON.is_pressed:
#         mover.move("backward")

#     if FORWARDBUTTON.is_pressed and BACKWARDBUTTON.is_pressed:
#         del(mover)
#         break
 
def forward_btn_callback(channel):
    if not GPIO.input(FORWARDBUTTON):
        mover.move('forward')
        # mover.forward()

def backward_btn_callback(channel):
    if not GPIO.input(BACKWARDBUTTON):
        mover.move('backward')
        # mover.backward()

# def signal_handler(sig, frame):
#     GPIO.cleanup()
#     sys.exit(0)


# # def ir_callback(channel):
# #     # object detected
# #     if sensor.value == 1:
# #         print("1")
# #         servo.min()
# #         sleep(.5)
# #         servo.mid()
# #         sleep(.5)
# #         servo.max()
# #         sleep(.5)

# #     # object disappeared
# #     if sensor.value == 0:
# #         print("0")
# #         servo.max()
# #         sleep(.5)
# #         servo.mid()
# #         sleep(.5)
# #         servo.min()
# #         sleep(.5)


    
#     # signal.signal(signal.SIGINT, signal_handler)
#     # signal.pause()


# GPIO.add_event_detect(FORWARDBUTTON, GPIO.FALLING)
# GPIO.add_event_callback(FORWARDBUTTON, forward_btn_callback)

# GPIO.add_event_detect(BACKWARDBUTTON, GPIO.FALLING)
# GPIO.add_event_callback(BACKWARDBUTTON, backward_btn_callback)

# # GPIO.add_event_detect(FORWARDBUTTON, GPIO.FALLING, callback=forward_btn_callback, bouncetime=100)
# # time.sleep(.5)
# # GPIO.add_event_callback(BACKWARDBUTTON, backward_btn_callback)
#################################################################


#if (vreinstate):
#    subprocess.call('python /home/pi/openbehavior/operantLicking/python/#blinkenlights.py -times 10 &', shell=True)

while lapsed < sessionLength:
    time.sleep(0.05) # allow 20 licks per sec
    ina0 = mpr121.touched_pins[0]
    act1 = mpr121.touched_pins[1]
    lapsed = time.time() - sTime
    

    if act1 == 1:
        thisActiveLick=time.time()
        try:
            f=open("/home/pi/_active", "r")
            (rat, scantime)=f.read().strip().split("\t")
            print("rat = ", rat)
            print("scantime = ", scantime)
            scantime=float(scantime)
            f.close()
        except ValueError:
            rat="ratUnknown"
            scantime=0
        if not rat:
            print("not rat")
            rat="ratUnknown"
        print (lastActiveLick)
        if thisActiveLick-lastActiveLick[rat]>maxILI and thisActiveLick-scantime>maxISI:
            print("second if statements")
            rat="ratUnknown"
        act[rat]+=1
        dlogger.logEvent(rat, time.time()-scantime, "ACTIVE", lapsed, nextratio[rat])
        lastActiveLick[rat]=thisActiveLick
        updateTime=showData()
        #blinkCueLED(0.2)
        if not pumptimedout[rat]:
            touchcounter[rat] += 1 # for issuing rewards
            if touchcounter[rat] >= nextratio[rat]  and rat !="ratUnknown":
                rew[rat]+=1
                #print("reward for "+rat+":"+str(rew[rat]))
                dlogger.logEvent(rat, time.time()-scantime, "REWARD", time.time()-sTime)
                touchcounter[rat] = 0
                pumptimedout[rat] = True
                pumpTimer = Timer(timeout, resetPumpTimeout, [rat])
                print ("timeout on " + rat)
                pumpTimer.start()
                subprocess.call('python ' + './blinkenlights.py -times 1&', shell=True)

                mover_subproc.forward()
                # subprocess.call("python3 mover_subproc.py")
                # pumpforward(180) # This is 60ul
                updateTime=showData()
                if schedule == "fr":
                    nextratio[rat]=ratio
                elif schedule == "vr":
                    nextratio[ratio]=random.randint(1,ratio*2)
                elif schedule == "pr":
                    breakpoint+=1.0
                    nextratio[rat]=int(5*2.72**(breakpoint/5)-5)
    elif ina0 == 1:
        thisInactiveLick=time.time()
        try:
            f=open("/home/pi/_inactive", "r")
            (rat, scantime)=f.read().strip().split("\t")
            scantime=float(scantime)
            rat=rat[2:]
            f.close()
        except:
            rat="ratUnknown"
            scantime=0
        if not rat:
            rat="ratUnknown"
        if thisInactiveLick-lastInactiveLick[rat]>maxILI and thisInactiveLick-scantime>maxISI:
            rat="ratUnknown"
        ina[rat]+=1
        dlogger.logEvent(rat, time.time()-scantime, "INACTIVE", lapsed)
        lastInactiveLick[rat]=thisInactiveLick
        updateTime=showData()
    # keep this here so that the PR data file will record lapse from sesion start 
    if schedule=="pr":
        lapsed = time.time() - lastActiveLick
    #show data if idle more than 5 min 
    if time.time()-updateTime > 60*5:
        updateTime=showData()


# signal the motion script to stop recording
#if schedule=='pr':
#    with open("/home/pi/prend", "w") as f:
#        f.write("yes")

dlogger.logEvent("", time.time(), "SessionEnd", time.time()-sTime)

print(ids.devID+  "Session"+ids.sesID + " Done!\n")
showData("final")


# del(pumpmover)

#subprocess.call('/home/pi/openbehavior/wifi-network/rsync.sh &', shell=True)
