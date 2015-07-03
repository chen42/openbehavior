import time
import serial
import RPi.GPIO as gpio
from operator import xor 

### This is the USB version
### The RDM6300 is connected to a CP2102 serial to USB breakout board
### http://forum.arduino.cc/index.php?topic=138611.0
### http://www.amazon.com/gp/product/B009T2ZR6W
### modified from code written by Ivan Amies.


# Flags ## DO NOT CHANGE ####
#############################
Startflag = "\x02"
Endflag = "\x03"
#############################

# initial settings for the uart device. Change as necessary, or read in as desired.#
baud_rate = 9600
time_out = 0.05
###

def initialize_uart(path_to_sensor) :
	uart = serial.Serial(path_to_sensor, baud_rate, timeout = time_out)
	uart.close()
	uart.open()
	uart.flushInput()
	uart.flushOutput()
	print(path_to_sensor + " initiated")
	return uart;

def readrfid(uart):
	while True:
		Zeichen = 0
		Tag = 0
		ID = ""
		Zeichen = uart.read()
		if Zeichen == Startflag:
			for Counter in range(13):
				Zeichen = uart.read()
				ID = ID + str(Zeichen)
			ID = ID.replace(Endflag, "" ) 
			print "RFID  detected: "+ ID

usb = "/dev/ttyUSB0"
uart = initialize_uart(usb) 
readrfid(uart)


