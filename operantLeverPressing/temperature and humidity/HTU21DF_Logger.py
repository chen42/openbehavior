'''
	Author: Ethan Willis
	Description: This program will log temperature and humidity
	to a log file with a given frequency.
	
	The log will have the following structure per entry.
	"date\ttime\ttemperature\thumidity\n"

	Usage:
		python HTU21DF_Logger.py <log filepath> <sleeptime>
'''
import time
import datetime
import HTU21DF
import sys

'''
	Writes data to the logfile located at the location specified
	by the filename variable.
'''
def write_to_log(filename, data):
	with open(filename, "a") as logfile:
		datastring = str(data[0]) + "\t" + str(data[1]) + "\t" + str(data[2]) + "\t" + str(data[3]) + "\n"
		logfile.write(datastring)
		print datastring

'''
	Collects temperature and humidity data on the time period
	specified by the sleeptime variable.
'''
def prog(filename="/home/pi/data/htu21df.log", sleeptime=3600):
	while True:
		# reset sensor and collect data for next log entry.
		HTU21DF.htu_reset
		temperature = HTU21DF.read_temperature()
		humidity = HTU21DF.read_humidity()
		cur_date = datetime.date.today()
		cur_time = time.time()
		data = [cur_date, cur_time, temperature, humidity]
	
		# save new data entry
		write_to_log(filename, data)
	
		# sleep until ready to collect next measurements.
		time.sleep(sleeptime)

prog()
