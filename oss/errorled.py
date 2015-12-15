import RPi.GPIO as gpio
import time

ErrorLed=35 
gpio.setmode(gpio.BOARD)
gpio.setup(ErrorLed,gpio.OUT)

while True:
	gpio.output(ErrorLed, True)
	time.sleep(0.5)
	gpio.output(ErrorLed, False)
	time.sleep(0.5)



