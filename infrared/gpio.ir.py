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
cnt, mili, diff = ({} for i in range(3))
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
	diff[c] = 0
	print str(c)
	GPIO.setup(c, GPIO.IN, pull_up_down = GPIO.PUD_UP)

fo = open("ir_log.txt", "a")
uid = pwd.getpwnam("pi").pw_uid
gid = grp.getgrnam("pi").gr_gid
path = "ir_log.txt"
os.chown(path, uid, gid)

def intervalCounting(channel): 
	fo = open("ir_log.txt", "a")
	cnt[channel] += 1
	currentTime = int(round(time.time()*1000))
	if GPIO.input(channel):
		currentTime = int(round(time.time()*1000))
		fo.write(str(currentTime) + "\tchannel " + str(channel) + "\tblocked\n")
	else:
		currentTime = int(round(time.time()*1000))
		fo.write(str(currentTime) + "\tchannel " + str(channel) + "\topen\b")
	return

for c in channels:
	GPIO.add_event_detect(c, GPIO.RISING, callback = intervalCounting, bouncetime = 0)

try:
	while True:
		time.sleep(50)	

except KeyboardInterrupt:
	GPIO.cleanup()

GPIO.cleanup()
