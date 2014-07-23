#!/usr/bin/python

import RPi.GPIO as GPIO 
import time
import os
import grp
import pwd
from collections import defaultdict

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#create a two dim dict for storing the timing of ir pulses
def chan(): #channel
	return defaultdict(int)
def eve(): #timing of events
	return defaultdict(chan)
CT=defaultdict(eve)

channel0=11
channel1=12
cnt={}
cnt[channel0]=0
cnt[channel1]=0
mili={}
mili[channel0]=int(round(time.time()*1000))
mili[channel1]=int(round(time.time()*1000))
interval=200 # half second
threshould=50 # minimal counts in time interval

state={}
state[channel0]=1
state[channel1]=1
diff={}
diff[channel0]=0
diff[channel1]=0


GPIO.setup(channel0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(channel1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Give write, user, group permissions for log file
fo = open("ir_log.txt", "a")
uid = pwd.getpwnam("pi").pw_uid
gid = grp.getgrnam("pi").gr_gid
path = "/home/pi/ir_log.txt"
os.chown(path, uid, gid)

def intervalCounting(channel): 
	fo = open("ir_log.txt", "a")
	cnt[channel]+=1
	currentTime= int(round(time.time()*1000))
	if currentTime - mili[channel] > interval :
		mili[channel]=currentTime
#		print (str(channel) + "=>"+ str(cnt[channel]) + "|| " + str(state[channel]))
		if cnt[channel] < threshould and state[channel] ==1:
			fo.write(str(currentTime) + " channel " + str(channel) + " blocked\n")
			state[channel] =0 #channel blocked
		if cnt[channel] > threshould and state[channel] ==0:
			fo.write(str(currentTime) + " channel " + str(channel) + " open\n")
			state[channel] =1 #channel open 
		cnt[channel]=0
	fo.close()
	return
GPIO.add_event_detect(channel0, GPIO.FALLING, callback=intervalCounting, bouncetime=0)
GPIO.add_event_detect(channel1, GPIO.FALLING, callback=intervalCounting, bouncetime=0)

try:
	while True:
		time.sleep(50)	

except KeyboardInterrupt:
	GPIO.cleanup()

GPIO.cleanup()



