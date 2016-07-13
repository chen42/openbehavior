#!/usr/bin/python

import RPi.GPIO as gpio
import time

# setup GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

# BEGIN CONSTANT DEFINITIONS
LED1 = int(7)
LED2 = int(9)
duration=int(1)

start=time.time()

while ( time.time()-start < 3600 ):
	gpio.output(LED1, gpio.HIGH)
	gpio.output(LED2, gpio.HIGH)
	time.sleep(duration)
	gpio.output(LED1, gpio.LOW)
	gpio.output(LED2, gpio.LOW)
	time.sleep(duration)

