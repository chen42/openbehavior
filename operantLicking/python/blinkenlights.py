#!/usr/bin/python

import RPi.GPIO as gpio
import time

# BEGIN CONSTANT DEFINITIONS
GREEN_LED_PIN = int(7)
# END CONSTANT DEFINITIONS

def flashRewardLED(duration):
	gpio.output(GREEN_LED_PIN, gpio.HIGH)
	time.sleep(duration)
	gpio.output(GREEN_LED_PIN, gpio.LOW)

if __name__ == "__main__":
	# Initialize GPIO
	gpio.setwarnings(False)
	gpio.setmode(gpio.BOARD)
	gpio.setup(GREEN_LED_PIN, gpio.OUT)
	# flash
	flashRewardLED(5)
