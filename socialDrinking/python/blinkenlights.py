#!/usr/bin/python

import RPi.GPIO as gpio
import time
import argparse


parser=argparse.ArgumentParser()
parser.add_argument('-times',  type=int)
args=parser.parse_args()
times=args.times


# BEGIN CONSTANT DEFINITIONS
GREEN_LED_PIN = int(7)
# END CONSTANT DEFINITIONS

print (str(times))

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
        while times > 1:
            time.sleep(10)
            flashRewardLED(5)
            times-=1
