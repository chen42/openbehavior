#!/usr/bin/python

import RPi.GPIO as GPIO
import time
from time import gmtime, strftime
import picamera
import os
import sys
import getopt
import subprocess
import signal

pump=7
l1=8
l2=10 
light=16

def init():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(pump, GPIO.OUT)  #for syringe pump
        GPIO.setup(l1, GPIO.IN)  #for lever 1
        GPIO.setup(l2, GPIO.IN)  #for lever 2
        GPIO.setup(light, GPIO.OUT)  #for light

def main(argv):
        fixedR=5  # fixed ratio
        injectT=5  #the time for which the pump will run, based on the weight of the mouse
        timeout = 10 #nothing will happen on button presses
        sessionT = 40 #300
        c1=0 # counter for lever one  
        c2=0 # counter for lever two
        i1=0 # counter for lever 1 during injection
        i2=0 # counter for lever 2 during injection
        t1=0 # counter for lever 1 during timeout
        t2=0 # counter for lever 2 during timeout
        animalID = 100000
        camera = picamera.PiCamera()
        camera.resolution = (320,240)
        try:
                opts, args = getopt.getopt(argv,"hf:it:to:st:aid",["fr","injectTime", "timeout", "sessionT", "animalID"])
        except getopt.GetoptError:
                print("sudo python3 openb.py -f <fixedRatio> -it <injectTime> -to <timeout> -st <sessionTime> -aid<animalID>")
                sys.exit(2)
        for opt, arg in opts:
                if opt == '-h':
                        print("sudo python3 openb.py -f <fixedRatio> -it <injectTime>-to <timeout> -st <sessionTime> -aid<animalID>")
                        sys.exit()
                elif opt in ("-f", "--fr"):
                        fixedR = arg
                elif opt in ("-it", "--injectTime"):
                        injectT = arg
                elif opt in("-to", "--timeout"):
                        timeout = arg
                elif opt in("-st", "--sessionT"):
                        if(arg>=300):
                                sessionT=arg
                elif opt in("-aid", "--animalID"):
                        animalID = arg 

        sensor = subprocess.Popen("python3 sensor.py " + str(animalID), shell=True, preexec_fn=os.setsid) # start recording temp/humidity in a file evry 5 min
        totalT = time.time() + sessionT
        # Need to change file name to animalID-data.txt
        data = open('data.txt', 'a')        
        data.write("\nAnimalID        Time              Event\n")
        data.close()
        i=0
        while True:
                input1= GPIO.input(l1)
                input2= GPIO.input(l2)
                if(input1==0):
                        c1+=1
                        data = open('data.txt', 'a')
                        data.write(str(animalID))
                        data.write("    ")
                        curTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                        data.write(str(curTime))                        
                        data.write("    Lever 1    ")
                        data.write("\n")
                        data.close()
                        time.sleep(.200)
                if(input2==0):
                        c2+=1
                        data = open('data.txt', 'a')
                        data.write(str(animalID))
                        data.write("    ")
                        curTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                        data.write(str(curTime))                        
                        data.write("    Lever 2    ")
                        data.write("\n")
                        data.close()
                        time.sleep(.200)
                if(c1>=int(fixedR)):
                        i+=1
                        GPIO.output(pump, True)
                        print("Spinning")
                        GPIO.output(light, True)
                        data = open('data.txt', 'a')
                        data.write(str(animalID))
                        data.write("    ")
                        curTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                        data.write(str(curTime))
                        data.write("    Inject    ")
                        data.write("\n")
                        data.close()
                        
                        camera.start_recording(str(i) + 'video.h264')
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
                        return i, animalID
                        break

def processNum(a):
        b = a.decode(encoding='UTF-8')
        c1, c2= b.split(':')
        return c1, c2

def processData(i, animalID):
        data = open('data.txt', 'r')
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
        data = open('data.txt', 'a')
        data.write(str(animalID))
        data.write("    ")
        curTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        data.write(str(curTime))
        data.write("    Lever 1    ")
        data.write("Sum    ")
        data.write(str(c1))
        data.write("\n")
        data.write(str(animalID))
        data.write("    ")
        curTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        data.write(str(curTime))
        data.write("    Lever 2    ")
        data.write("Sum    ")
        data.write(str(c2))
        data.write("\n")
        data.write(str(animalID))
        data.write("    ")
        curTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        data.write(str(curTime))
        data.write("    Inject    ")
        data.write("Sum    ")
        data.write(str(i))
        data.close()

if __name__ == "__main__":
        init()
        numInjection, animalID = main(sys.argv[1:])
        processData(numInjection, animalID)
        GPIO.cleanup()
