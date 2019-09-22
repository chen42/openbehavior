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


def flashRewardLED(duration):
    print ("LED on")
    gpio.output(GREEN_LED_PIN, gpio.HIGH)
    time.sleep(duration)
    print ("LED off")
    gpio.output(GREEN_LED_PIN, gpio.LOW)
    time.sleep(duration)

if __name__ == "__main__":
    # Initialize GPIO
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
    gpio.setup(GREEN_LED_PIN, gpio.OUT)
    # turn LED on for 5 sec
    #flashRewardLED(5)
    while times >= 1:
        print (str(times)+ " LED flashing left")
        flashRewardLED(5)
        times-=1
