#!/usr/bin/python

import RPi.GPIO as GPIO 
import time
import os
import grp
import pwd
#from collections import defaultdict

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

pinCount = input("Enter number of pins in use by IR sensors: ")
channels = []
pin_alloc = 0

#get pins to be used from command line 
while pin_alloc < pinCount:
	pin = input("Enter GPIO pin number: ")
	if pin in range (1,27) and not pin in [1, 2, 4, 6, 9, 14, 17, 20, 25]:
		channels.append(pin)
		pin_alloc += 1
	else:
		print "Invalid GPIO pin number (power pins are included)"
		 
#initialize counts
for c in channels:
	print str(c)
	GPIO.setup(c, GPIO.IN, pull_up_down = GPIO.PUD_UP)

fo = open("/home/pi/data/ir_log.txt", "a")
uid = pwd.getpwnam("pi").pw_uid
gid = grp.getgrnam("pi").gr_gid
path = "/home/pi/data/ir_log.txt"
os.chown(path, uid, gid)

def intervalCounting(channel): 
	fo = open("/home/pi/data/ir_log.txt", "a")
	if GPIO.input(channel):
		currentTime = int(round(time.time()*1000))
		fo.write(str(currentTime) + "\tchannel " + str(channel) + "\tblocked\n")
	else:
		currentTime = int(round(time.time()*1000))
		fo.write(str(currentTime) + "\tchannel " + str(channel) + "\topen\n")
	return

for c in channels:
	GPIO.add_event_detect(c, GPIO.RISING, callback = intervalCounting, bouncetime = 0)

try:
	while True:
		time.sleep(50)	

except KeyboardInterrupt:
	GPIO.cleanup()

GPIO.cleanup()
