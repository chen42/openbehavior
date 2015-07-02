import time
import RPi.GPIO as io
io.setmode(io.BCM)

pir_pin = 18 # board=12

io.setup(pir_pin, io.IN)         # activate input

while True:
	if io.input(pir_pin):
		print time.strftime("%Y-%m-%d\t%H:%M:%S")
	time.sleep(0.5)

