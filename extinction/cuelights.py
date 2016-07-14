#!/usr/bin/python

import RPi.GPIO as gpio
import time

# BEGIN CONSTANT DEFINITIONS
LED1 = int(33)
LED2 = int(29)
duration=int(1)

# setup GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(LED1, gpio.OUT)
gpio.setup(LED2, gpio.OUT)

start=time.time()

while ( time.time()-start < 3600 ):
	gpio.output(LED1, gpio.HIGH)
	gpio.output(LED2, gpio.HIGH)
	time.sleep(duration)
	gpio.output(LED1, gpio.LOW)
	gpio.output(LED2, gpio.LOW)
	time.sleep(duration)

