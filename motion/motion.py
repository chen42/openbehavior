#!/usr/bin/env python2

import RPi.GPIO as gpio
import time
import os
import sys

pirPin=12
offPin=16
motionLed=40
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(pirPin, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(offPin, gpio.IN, pull_up_down=gpio.PUD_DOWN)        
gpio.setup(motionLed, gpio.OUT)        

while(True):
	if not gpio.input(offPin):
                os.system("/home/pi/openbehavior/wifi-network/killhtpd.sh &") # kills htpd in 30 sec
                os.system("/home/pi/openbehavior/wifi-network/deviceinfo.sh") # try to connect to wifi but only wait for max 20 sec.
                os.system("sudo ifconfig wlan0 down") # disconnect from the internet
		boxid=open("/home/pi/deviceid").read().strip()
                # session id 
                with open ("/home/pi/sessionid", "r+") as f:
                    storedSessionID=f.read().strip()
                    sessionID=int(storedSessionID)+1  
                    f.seek(0)
                    f.write(str(sessionID))
                    f.close()
		startTime=time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
		motionDataFile='/home/pi/Pies/OCMotion/'+ boxid + "_s" + str(sessionID) + "_" + startTime + ".csv"
		with open(motionDataFile,"a") as f:
			f.write("#Session started at " + startTime +"\n")
			f.write("date\tboxid\tseconds\n")
			f.close()
		print ("session starts at " + startTime)
                cnt=0
		start=time.time()

		while gpio.input(offPin)==0:
#                        time.sleep(0.1) # time resolution of motion data
			if gpio.input(pirPin):
                                cnt=cnt+1
                                print ("motion cnt " + str(cnt))
				with open(motionDataFile,"a") as f:
                                    lapsed=time.time()-start
                                    f.write(time.strftime("%Y-%m-%d\t", time.localtime()) + boxid +"\t"+ str(lapsed) +"\n")
				    f.close()
				gpio.output(motionLed, True)
				time.sleep(0.2)
				gpio.output(motionLed, False)
				time.sleep(0.2)
#               print "session ended\n"
                with open(motionDataFile,"a") as f:
                    f.write("#Session ended at \t" + time.strftime("%H:%M:%S", time.localtime()) + "\n") 
                    f.write(boxid + "\t" + str(cnt)+"\n")
                    f.close()
                os.system("sudo ifconfig wlan0 up")
                os.system("/home/pi/openbehavior/wifi-network/rsync.sh &")
        else:
		time.sleep(1)
		gpio.output(motionLed, True)
                #print "pin 16 has no signal\n"

