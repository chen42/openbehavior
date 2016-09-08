
import time
import Adafruit_BMP.BMP085 as BMP085


barometer = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)
while 1:
	pressure=barometer.read_pressure()
	temp=barometer.read_temperature()
	print (str(temp), str(pressure))
	time.sleep(2)

