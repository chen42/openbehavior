#!/usr/bin/python

import RPi.GPIO as GPIO 
import time
import os
import grp
import pwd
#from collections import defaultdict

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

interval = 200 # 20 milli second 
threshould = 50 # minimal counts in time interval
pinCount = input("Enter number of pins in use by IR sensors: ")
channels = []
cnt, mili, state, diff = ({} for i in range(4))
pin_alloc = 0

#get pins in use
while pin_alloc < pinCount:
	pin = input("Enter GPIO pin number: ")
	if pin in range (1,27) and not pin in [1, 2, 4, 6, 9, 14, 17, 20, 25]:
		channels.append(pin)
		pin_alloc += 1
	else:
		print "Invalid GPIO pin number"
		 
#initialize counts
for c in channels:
	cnt[c] = 0
	mili[c] = (int(round(time.time() * 1000)))
	state[c] = 1
	diff[c] = 0
	print str(c)
	GPIO.setup(c, GPIO.IN, pull_up_down = GPIO.PUD_UP)

fo = open("/home/pi/data/ir_log.txt", "a")
uid = pwd.getpwnam("pi").pw_uid
gid = grp.getgrnam("pi").gr_gid
path = "/home/pi/data/ir_log.txt"
os.chown(path, uid, gid)

def intervalCounting(channel): 
	fo = open("/home/pi/data/ir_log.txt", "a")
	cnt[channel] += 1
	currentTime = int(round(time.time()*1000))
	if currentTime - mili[channel] > interval :
		mili[channel] = currentTime
		if cnt[channel] < threshould and state[channel] == 1:
			fo.write(str(currentTime) + "\tchannel " + str(channel) + "\tblocked\n")
			state[channel] = 0 #channel blocked
		if cnt[channel] > threshould and state[channel] == 0:
			fo.write(str(currentTime) + "\tchannel " + str(channel) + "\topen\n")
			state[channel] = 1 #channel open 
		cnt[channel] = 0
	fo.close()
	return

for c in channels:
	GPIO.add_event_detect(c, GPIO.FALLING, callback = intervalCounting, bouncetime = 0)

try:
	while True:
		time.sleep(50)	

except KeyboardInterrupt:
	GPIO.cleanup()

GPIO.cleanup()
