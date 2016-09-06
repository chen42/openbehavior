#!/usr/bin/env python2

import RPi.GPIO as gpio
import time

def touchLED():
	RFIDLed=35 
	gpio.setmode(gpio.BOARD)
	gpio.setwarnings(False)
	gpio.setup(RFIDLed,gpio.OUT)
	gpio.output(RFIDLed, True)
	time.sleep(0.2)
	gpio.output(RFIDLed, False)

touchLED()



