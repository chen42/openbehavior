#!/usr/bin/python

import RPi.GPIO as gpio
import time
import argparse

import board
import neopixel


pixels = neopixel.NeoPixel(board.NEOPIXEL,1)

parser=argparse.ArgumentParser()
# parser.add_argument('-times',  type=int)
parser.add_argument('-reward_happened', type=bool, default=False)
args=parser.parse_args()
# times=args.times
reward_happened = args.reward_happened
    

lights_on_hours = [21,22,23,0,1,2,3,4,5,6,7,8,9]
def house_light_on():
    for i in range(len(pixels)):
        pixels[i] = (255,255,255)

def reward_cue_light():
    for i in range(len(pixels)):
        pixels[i] = (0,0,0)
        
    time.slee(0.5)

    # if it's light on sessoin, turn back the house light
    if time.localtime().tm_hour in lights_on_hours:
        house_light_on()
        

# BEGIN CONSTANT DEFINITIONS
# GREEN_LED_PIN = int(7)
# END CONSTANT DEFINITIONS


# def flashRewardLED(duration):
#     print ("LED on")
#     gpio.output(GREEN_LED_PIN, gpio.HIGH)
#     time.sleep(duration)
#     print ("LED off")
#     gpio.output(GREEN_LED_PIN, gpio.LOW)
#     time.sleep(duration)

if __name__ == "__main__":
    house_light_on() 
    if reward_happened:
        reward_cue_light()

    # # Initialize GPIO
    # gpio.setwarnings(False)
    # gpio.setmode(gpio.BOARD)
    # gpio.setup(GREEN_LED_PIN, gpio.OUT)
    # # turn LED on for 5 sec
    # #flashRewardLED(5)
    # while times >= 1:
    #     print (str(times)+ " LED flashing left")
    #     flashRewardLED(0.5)
    #     times-=1
