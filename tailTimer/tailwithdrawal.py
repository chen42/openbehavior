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
    GPIO.setmode(GPIO.BOARD)    # Numbers GPIOs by physical location
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

user=input("Please enter your last name\n")
if user =="00fb4fb3":
    user="Chen"
if user=="00a56fe6":
    user="Udell"

targettemp=48
#targettemp=input("What is that target temp in C?")
templo=int(targettemp)-0.50
temphi=int(targettemp)+0.50

print ("\n\nProgram started, user is " + user + " target temp range: (" + str(templo) + " - " + str(temphi) + ")\n" )
print ("Data are saved in " + datafile+"\n")
ratid=input("Please enter rat ID\n")

while True:
    time.sleep(0.01)
    tail_out= GPIO.input(Tail)
    if (tail_out==True):
        temp1=read_temp()
        print ("Current temp:\t" + str(temp1))
        if (temp1>temphi):
            print ("\t\t\tTemperature too high\n")
        elif (temp1<templo):
            print ("\t\t\tTemperature too low\n")
    else:
        sTime=time.time()
        print ("Timer started\n")
        while (tail_out==False):
            tail_out= GPIO.input(Tail)
        elapsed=time.time()-sTime + 0.4 # calibrated at 2s and 10s  found this consistent system error        
        elapsed=round(elapsed, 3)
        temp2=read_temp()
        temp=round((temp1+temp2)/2, 3)
        now0=datetime.datetime.now()
        now=now0.strftime("%Y-%m-%d\t%H:%M")
        line=ratid+"\t" + now + "\t"+ str(elapsed) + "\t"+ str(temp) + "\t" + str(user) + "\n"
        lineshort=ratid+"\t" + str(elapsed) + "\t"+ str(temp) + "\t" + str(user) + "\n"
        print (lineshort)
        time.sleep(1)
        next=input("Type \"n\" for new rat,\n\"d\" to delete this trial,\n\"a\" to test the current rat again\n\"e\" to end the run\n")
        ## RFID equivalants
        if next=="00fbf27e":
            next="n"
        if next=="00fc191f":
            next="d"
        if next=="00fb8874":
            next="e"
        if next=="00fb3131":
            next="a"
        ## 
        if (next =="d"):
            print ("Data deleted\n")
            next="a" # then test the same rat again
        else:
            with open(datafile, "a") as f:
                f.write(line)
                f.close()
            print ("Data saved\n")
        print ("Please wait 10 seconds\n")
        time.sleep(10)
        if (next=="n"):
            ratid=input("Please enter new rat ID\n")
        elif (next=="e"):
            print ("Exit prgram\n")
            sys.exit()
        else:
             print ("Please test the same rat again\n")
