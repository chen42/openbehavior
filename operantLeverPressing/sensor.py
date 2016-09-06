#from htu21d import HTU21D ## this is only for the I2C board from adafruit
import time
from time import gmtime, strftime
import sys
from bmp183 import bmp183

#htu21d = HTU21D()
#htu21d.reset()
bmp = bmp183()
def main(argv):
    logs = open('temperature.csv', 'a')
    logs.write("AnimalID\tTime\tTemp (C)\tHumidity \tbmp Temp \tbmp Pressure\n")
    logs.close()
    
    animalID = str(argv)
    while True:
        logs = open('temperature.csv', 'a')
        logs.write(animalID)
        logs.write(" ")
        curTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
 #       temperature = "{:.2f}".format(htu21d.get_temp())
	temperature = -1
       # humidity = "{:.2f}".format(htu21d.get_rel_humidity())
	humidity = -1
        logs.write(str(curTime))
        logs.write("\t")
        logs.write(str(temperature))
        logs.write("\t")
        logs.write(str(humidity))
        logs.write("\t")
	logs.write(str(bmp.temperature))
	logs.write("\t")
	logs.write(str(bmp.pressure))
        logs.close()
        time.sleep(120)
        
if __name__ == "__main__":
    main(sys.argv[1])

