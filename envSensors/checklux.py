# Abigail Salinero, a summer student, contributed this code.

import RPi.GPIO as GPIO
import time

pin=11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)


def blink(pin):
	GPIO.output(pin,GPIO.HIGH)
	time.sleep(.2)
	GPIO.output(pin,GPIO.LOW)
	time.sleep(.2)
	return


sum = 0
count = 0
threshold = 5
with open('/home/pi/lux.csv') as f:
	for line in f:
		sum += float(line)
		count = count + 1
	avg = sum/count			
	print avg
	while avg <= threshold:
		blink(pin)
