#!/usr/bin/python

import RPi.GPIO as GPIO

import time
from time import gmtime, strftime, sleep
import picamera
import os
import sys
import getopt
import subprocess
import signal


## all  times are in seconds

# GPIO setup.   
pump=7 # syringe pump
l1=8 # active lever 
l2=10  # inactive lever
light=16 # cue light

def init():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(pump, GPIO.OUT)  #for syringe pump
        GPIO.setup(l1, GPIO.IN)  #for active lever (i.e., lever 1)
        GPIO.setup(l2, GPIO.IN)  #for inactive lever (i.e., lever 2)
        GPIO.setup(light, GPIO.OUT)  #for light

def main(argv):
        fixedR=5  # fixed ratio
        injectT=5  # the time for which the pump will run, based on the weight of the mouse
        timeout = 10 # nothing will happen on lever presses
        sessionT = 300 # session time will be overwritten by the parameter provided at the command line   
        c1=0 # counter for lever 1  
        c2=0 # counter for lever 2 
        i1=0 # counter for lever 1 during injection
        i2=0 # counter for lever 2 during injection
        t1=0 # counter for lever 1 during timeout
        t2=0 # counter for lever 2 during timeout
        animalID = "animal ID"
        camera = picamera.PiCamera()
        camera.resolution = (320,240)
        try:
                opts, args = getopt.getopt(sys.argv[1:],"hf:i:t:s:a:",["fr","injectTime", "timeout", "sessionT", "animalID"])
        except getopt.GetoptError:
                print("sudo python3 openb.py -f <fixedRatio> -i <injectTime> -t <timeout> -s <sessionTime> -a <animalID>")
                sys.exit(2)
        for opt, arg in opts:
                if opt == '-h':
                        print("sudo python3 openb.py -f <fixedRatio> -i <injectTime> -t <timeout> -s <sessionTime> -a <animalID>")
                        sys.exit()
                elif opt in ("-f", "--fr"):
                        fixedR = arg
                elif opt in ("-i", "--injectTime"):
                        injectT = arg
                elif opt in("-t", "--timeout"):
                        timeout = arg
                elif opt in("-s", "--sessionT"):
                        if(int(arg)>=300):
                                sessionT=arg
                elif opt in("-a", "--animalID"):
                        animalID = arg

        sensor = subprocess.Popen("python3 sensor.py " + str(animalID), shell=True, preexec_fn=os.setsid) # start recording temp/humidity in a file evry 5 min
        totalT = time.time() + float(sessionT)
        # Need to change file name to animalID-data.csv
        data = open('data.csv', 'a') # default data file format is comma seperated value, csv        
        data.write("\nAnimalID,Time,Event\n")
        data.close()
        i=0
        print("fixedR", fixedR)
        print("injectT", injectT)
        print("timeout", timeout)
        print("sessionT", sessionT)
        print("animalID", animalID)
        while True:
                input1= GPIO.input(l1)
                input2= GPIO.input(l2)
                if(input1==0):
                        curTime = strftime("%Y-%m-%d,%H:%M:%S", gmtime())
                        c1+=1
                        data = open('data.csv', 'a')
                        data.write(str(animalID) + "," + str(curTime) + ",Lever 1\n") 
                        data.close()
                        print("Lever 1 pressed at ", curTime)
                        time.sleep(.200)
                if(input2==0):
                        curTime = strftime("%Y-%m-%d,%H:%M:%S", gmtime())
                        c2+=1
                        data = open('data.csv', 'a')
                        data.write(str(animalID) + "," + str(curTime) + ",Lever 1\n") 
                        data.close()
                        print ("Lever 2 pressed at ", curTime)
                        time.sleep(.200)
                if(c1>=int(fixedR)):
                        curTime = strftime("%Y-%m-%d,%H:%M:%S", gmtime())
                        i+=1
                        GPIO.output(pump, True)
                        GPIO.output(light, True)
                        data = open('data.csv', 'a')
                        data.write(str(animalID) + "," + str(curTime) + ",Injection\n") 
                        print("Stimulus delivered at", curTime )
                        data.close()
                        camera.start_recording(str(i) + 'video.h264') # we take a short video after each reward

                        #Start recording lever presses during injection
                        lever_during_inject = subprocess.check_output("python3 leverRecord.py " + str(injectT)+":"+str(animalID), shell=True)
                        i1, i2 = processNum(lever_during_inject)
                        time.sleep(float(injectT))
                        GPIO.output(pump, False)
                        GPIO.output(light, False)
                        print("Lever presses during injection: ", i1, " ", i2)

                        #Start recording lever presses during timeout period
                        lever_during_timeout = subprocess.check_output("python3 leverRecord.py " + str(timeout)+":"+str(animalID), shell=True)
                        time.sleep(float(timeout))
                        t1, t2 = processNum(lever_during_timeout)
                        print("Lever presses during timeout: ", t1, " ", t2)
                        
                        camera.stop_recording()
                        c1=0
                        continue
                if(time.time()>totalT):
                        os.killpg(sensor.pid, signal.SIGTERM)
                        return i, animalID, timeout, sessionT, injectT, fixedR
                        break

def processNum(a):
        b = a.decode(encoding='UTF-8')
        c1, c2= b.split(':')
        return c1, c2

def processData(i, animalID, timeout, sessionT, injectT, fixedR):
        data = open('data.csv', 'r')
        c1 = 0
        c2 = 0 
        for line in data:
                if "Lever 1" in line:
                        c1+=1
                if "Lever 2" in line:
                        c2+=1
                if "Animal" in line:
                        c1=0
                        c2=0
        data = open('data.csv', 'a')
        curTime = strftime("%Y-%m-%d,%H:%M:%S", gmtime())
        data.write(str(animalID) + ","+ str(curTime) + ",Lever 1 Sum,"+str(c1)+"\n")
        data.write(str(animalID) + ","+ str(curTime) + ",Lever 2 Sum,"+str(c2)+"\n")
        data.write(str(animalID) + ","+ str(curTime) + ",Injection Sum,"+str(i)+"\n")
        data.write(str(animalID) + ","+ str(curTime) + ",Session time,"+str(sessionT)+"\n")
        data.write(str(animalID) + ","+ str(curTime) + ",Injection time,"+str(injectT)+"\n")
        data.write(str(animalID) + ","+ str(curTime) + ",Fixed ratio,"+str(fixedR)+"\n")
        data.write(str(animalID) + ","+ str(curTime) + ",Time out,"+str(timeout)+"\n")
        data.close()

if __name__ == "__main__":
        init()
        try:
                numInjection, animalID, timeout, sessionT, injectT, fixedR = main(sys.argv[1:])
        except KeyboardInterrupt:
                os.system("sudo pkill -9 -f sensor.py")
        processData(numInjection, animalID, timeout, sessionT, injectT, fixedR)
        GPIO.cleanup()
