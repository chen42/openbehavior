from htu21d import HTU21D
import time
from time import gmtime, strftime
import sys

sensor = HTU21D()
sensor.reset()


def main(argv):
    logs = open('temperature.txt', 'a')

    logs.write("AnimalID             Time        Temp (C)   Humidity \n")
    logs.close()

    animalID = str(argv)
    while True:
        logs = open('temperature.txt', 'a')
        logs.write(animalID)
        logs.write("    ")
        curTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        temperature = "{:.2f}".format(sensor.get_temp())
        humidity = "{:.2f}".format(sensor.get_rel_humidity())
        logs.write(str(curTime))
        logs.write("    ")
        logs.write(str(temperature))
        logs.write("    ")
        logs.write(str(humidity))
        logs.write("\n")
        logs.close()
        time.sleep(3)
        
if __name__ == "__main__":
    main(sys.argv[1])

