## using the adxl345 to detect tremor associated with alcohol withdrawal.

from adxl345 import ADXL345
from time import localtime
import time
import RPi.GPIO as gpio
  
adxl345 = ADXL345()
    
sessionLength=480
#sessionLength=10
datafile='/home/pi/tremor' + time.strftime("%Y-%m-%d_%H:%M:%S", localtime()) + ".csv"

Led=37
gpio.setmode(gpio.BOARD)
gpio.setup(Led, gpio.OUT)

gpio.output(Led, True)
start=time.time()

lapsed= 0.00
data= 'Date\tTime\tSecondsLapsed\tx\ty\tz\n'

while  (lapsed < sessionLength) :
	lapsed= time.time()-start 
	datetime= time.strftime("%Y-%m-%d\t%H:%M:%S", localtime())
	axes = adxl345.getAxes(True)
	data = data +  datetime+ "\t"+ str(lapsed) + '\t' + str(axes['x']) + '\t' + str(axes['y']) + '\t' + str(axes['x'])  + "\n"
	time.sleep(.041667)

with  open(datafile, "a")  as f:
	f.write(data)

gpio.output(Led, False)


