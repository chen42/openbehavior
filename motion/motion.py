#!/usr/bin/env python2

import RPi.GPIO as gpio
import time
import os
import sys

pirPin=12
onPin=16
motionLed=40
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(pirPin, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(onPin, gpio.IN, pull_up_down=gpio.PUD_DOWN)        
gpio.setup(motionLed, gpio.OUT)        

while(True):
	if not gpio.input(onPin):
                os.system("/home/pi/openbehavior/wifi-network/killhtpd.sh &") # kills htpd in 30 sec
                os.system("/home/pi/openbehavior/wifi-network/deviceinfo.sh") # try to connect to wifi but only wait for max 20 sec.
                os.system("sudo ifconfig wlan0 down") # disconnect from the internet
                sessionLength=2.5*60
		idfile=open("/home/pi/deviceid")
		boxid=idfile.read()
                boxid=boxid.strip()
		startTime=time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
		start=time.time()
		motionDataFile='/home/pi/Pies/OCMotion/mot'+ boxid + "_" + startTime + ".csv"
                cnt=0
		with open(motionDataFile,"a") as f:
			f.write("#Session started on " + time.strftime("%Y-%m-%d\t%H:%M:%S\t", time.localtime())+"\n")
			f.write("date\tboxid\tseconds\n")
			f.close()
		print ("session starts at " + time.strftime("%Y-%m-%d\t%H:%M:%S"))
		while time.time()-start < sessionLength:
#                        time.sleep(2) # time resolution of motion data
			if gpio.input(pirPin):
                                cnt=cnt+1
#                               print ("motion cnt " + str(cnt))
				with open(motionDataFile,"a") as f:
                                    lapsed=time.time()-start
                                    f.write(time.strftime("%Y-%m-%d\t", time.localtime()) + boxid +"\t"+ str(lapsed) +"\n")
				    f.close()
				gpio.output(motionLed, True)
				time.sleep(0.2)
				gpio.output(motionLed, False)
				time.sleep(0.2)
                        if gpio.input(onPin) == 1:
                            print "session ended\n"
                            with open(motionDataFile,"a") as f:
                                f.write("#Session ended\t" + time.strftime("%H:%M:%S", time.localtime()) + "\n") 
                                f.write(boxid + "\t" + str(cnt)+"\n")
                                f.close()
                            sessionLength=0
                            os.system("sudo ifconfig wlan0 up")
                            os.system("/home/pi/openbehavior/wifi-network/rsync.sh &")
	else:
		time.sleep(1)
		gpio.output(motionLed, True)
                #print "pin 16 has no signal\n"

