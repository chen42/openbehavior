from htu21d import HTU21D
import time
from time import gmtime, strftime

sensor = HTU21D()
sensor.reset()

logs = open('temperature.txt', 'w')

logs.write("       Time             Temp (C)  Humidity \n")
logs.close()


while True:
    logs = open('temperature.txt', 'a')
    curTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    temperature = "{:.2f}".format(sensor.get_temp())
    humidity = "{:.2f}".format(sensor.get_rel_humidity())
    logs.write(str(curTime))
    logs.write("   |  ")
    logs.write(str(temperature))
    logs.write("  |  ")
    logs.write(str(humidity))
    logs.write("   |\n")
    logs.close()
    time.sleep(300)  #sleep 5 minutes


