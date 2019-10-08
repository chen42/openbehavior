#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
import os
import glob
import serial
import sys
import datetime
import operator
import subprocess

## temp probe DS18B20
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# path to data file 
idfile=open("/home/pi/deviceid")
device=idfile.read()
device=device.strip()
today=datetime.date.today()
td=str(today)
datafile="/home/pi/Pies/tailwithdrawal/tailwithdrawal"+td+".csv"

# flags
startflag = "\x02"
endflag = "\x03"


def setupGPIO():
	GPIO.setmode(GPIO.BOARD)	# Numbers GPIOs by physical location
	GPIO.setup(Tail, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.01)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

Tail=12
setupGPIO()

user=raw_input("please type your name\n")
#targettemp=raw_input("what is that target temp in C?")
targettemp=48
templo=int(targettemp)-0.50
temphi=int(targettemp)+0.50

print ("\n\nProgram started, target temp range: ("+str(templo)+" - "+str(temphi)+")\n")
print ("data are saved in " + datafile+"\n")
ratid=input("please scan rat")

while True:
	time.sleep(0.01)
	tail_out= GPIO.input(Tail)
	if (tail_out==True):
		temp1=read_temp()
		print ("current temp:\t" + str(temp1))
		if (temp1>temphi):
			print ("\t\t\tTemperature too high\n")
		elif (temp1<templo):
			print ("\t\t\tTemperature too low\n")
	else: 
		sTime=time.time()
		print "start timer\n"
		while (tail_out==False):
			tail_out= GPIO.input(Tail)
		elapsed=time.time()-sTime +0.4 # calibrated at 2s and 10s  found this consistent system error		
		elapsed=round(elapsed, 3)
		temp2=read_temp()
		temp=round((temp1+temp2)/2, 3)
		now0=datetime.datetime.now()
		now=now0.strftime("%Y-%m-%d\t%H:%M")
		line=ratid+"\t" + now + "\t"+ str(elapsed) + "\t"+ str(temp) + "\t" + str(user) + "\n" 
		print (line)
		time.sleep(5)
		next=raw_input("Type \"n\" for new rat,\n\"d\" to delete this trial,\n\"e\" to end the run, \nanythine else to continue with current rat, CTRL-C to stop\n")
		if (next !="d"):
			with open(datafile, "a") as f:
				f.write(line)
				f.close()
		if (next=="n"):
			ratid=input("please scan rat")
		if (next=="e"): 
			sys.exit()
