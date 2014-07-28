#!/usr/bin/python

import RPi.GPIO as GPIO
import time
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

camera = picamera.PiCamera()

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
        timeout = 20 #nothing will happen on button presses
        sessionT = 300  #Length of total session
        c1=0 # counter for lever one  
        c2=0 # counter for lever two
        
        try:
                opts, args = getopt.getopt(argv,"hf:it:to:st",["fr","injectTime", "timeout", "sessionT"])
        except getopt.GetoptError:
                print("sudo python3 openb.py -f <fixedRatio> -it <injectTime> -to <timeout> -st <sessionTime>")
                sys.exit(2)
        for opt, arg in opts:
                if opt == '-h':
                        print("sudo python3 openb.py -f <fixedRatio> -it <injectTime>-to <timeout> -st <sessionTime>")
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

        sensor = subprocess.Popen("python3 sensor.py", shell=True, preexec_fn=os.setsid) # start recording temp/humidity in a file evry 5 min
        totalT = time.time() + sessionT
        while True:
                input1= GPIO.input(l1)
                input2= GPIO.input(l2)
                if(input1==0):
                        c1+=1
                        time.sleep(.250)
                if(input2==0):
                        c2+=1
                        time.sleep(.250)
                if(c1>=int(fixedR)):
                        print("Lever 1 is pressed ", fixedR, "times")
                        print("No of lever 2 presses before the mouse pressed the lever 1 correct number of times: ", c2)
                        GPIO.output(pump, True)
                        print("Spinning")
                        GPIO.output(light, True)
                        
                        camera.start_recording('video.h264')
                        
                        #Start recording lever presses during injection
                        lever_during_inject = subprocess.check_output("python3 leverRecord.py " + str(injectT), shell=True)
                        c1, c2 = processNum(lever_during_inject)
                        time.sleep(float(injectT))
                        GPIO.output(pump, False)
                        GPIO.output(light, False)
                        print("Lever presses during injection: ", c1, " ", c2)

                        #Start recording lever presses during timeout period
                        lever_during_timeout = subprocess.check_output("python3 leverRecord.py " + str(timeout), shell=True)
                        time.sleep(float(timeout))
                        c1, c2 = processNum(lever_during_timeout)
                        print("Lever presses during timeout: ", c1, " ", c2)
                        
                        camera.stop_recording()
                        c1=0
                        continue
                if(time.time()>totalT):
                        os.killpg(sensor.pid, signal.SIGTERM)
                        break

def processNum(a):
        b = a.decode(encoding='UTF-8')
        c1, c2= b.split(':')
        return c1, c2

if __name__ == "__main__":
        init()
        main(sys.argv[1:])
        GPIO.cleanup()
