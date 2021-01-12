#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
import os
import glob
import serial
import sys
import datetime
import operator
from config import COMMAND_RFIDs, USER_RFIDs


## disable saving data if keys are detected as RFID
## check within rat variability before continue to next rat

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

file_dir = "/home/pi/Pies/tailwithdrawl/"
# create the directory if not already exist
if not os.path.isdir(file_dir):
   os.makedirs(file_dir) 

datafile = file_dir + "tailimmersion_" + td + ".csv"


# flags
startflag = "\x02"
endflag = "\x03"

latency={}
savedata=1 # default to save data

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

spin_speed = input("Please enter a mixing speed (1-7): ")[-4:]
user=input("TailTimer started.\nPlease enter your name:\n")[-4:]
if user in USER_RFIDs.keys():
    user = USER_RFIDs[user]

print ("\nWelcome, " + user + "\n")
targettemp=input("Please enter the target temp in C,  or scan any key for 48C.\n")
if not targettemp.isdigit():
    targettemp=48
templo=int(targettemp)-0.25
temphi=int(targettemp)+0.25

print ("\n\nProgram started, user is " + user + " target temp range: (" + str(templo) + " - " + str(temphi) + ")\n" )
print ("Data are saved in " + datafile+"\n")

print ("Please test the wire.")
ratid="00fbtest"

while True:
    time.sleep(0.01)
    tail_out= GPIO.input(Tail)
    if (tail_out==True):
        temp1=read_temp()
        if (temp1>temphi):
            print ("Temp: " + str(temp1) + " Too hot!!")
        elif (temp1<templo):
            print ("Temp: " + str(temp1) + " Too cold!!")
        elif ratid[0:4] != "00fb":
            print ("Temp: " + str(temp1) + " please test " + ratid)
        else:
            print ("Temp: " + str(temp1) + "!!! "+ ratid +" is not a rat ID. ")
    else:
        sTime=time.time()
        print ("Timer started\n")
        while (tail_out==False):
            tail_out= GPIO.input(Tail)
            time.sleep(0.02)
            elapsed=time.time()-sTime + 0.4 # calibrated at 2s and 10s  found this consistent system error        
            if  (elapsed>10):
                print ("Maximum latency of 10 s reached\n");
                tail_out=True
        elapsed=round(elapsed, 3)
        temp2=read_temp()
        temp=round((temp1+temp2)/2, 3)
        now0=datetime.datetime.now()
        now=now0.strftime("%Y-%m-%d\t%H:%M")
        line=ratid+"\t" + now + "\t"+ str(elapsed) + "\t"+ str(temp) + "\t" + str(user) + "\t" + spin_speed + "\n"
        if (ratid in latency.keys()):
            latency[ratid] += str(elapsed) + ", "
        else:
            latency[ratid] = str(elapsed) + ", "
        print ("Rat is "+ ratid+", latency = "+ latency[ratid])
        next_id=input("Choose one of the following:\n \"n\" for new rat,\n\"d\" to delete this trial,\n\"a\" to test the current rat again\n\"e\" to end the run\n")[-4:]
        ## RFID equivalants
        if next_id in COMMAND_RFIDs.keys():
            next_id = COMMAND_RFIDs[next_id]

        if (next_id =="d"):
            print ("Data deleted as requested\n")
            next_id="a" # then test the same rat again
            savedata=0
        if elapsed<1.5:
            print ("!!! latency < 1.5 sec, Data not saved");
            savedata=0
            next_id="a"
        if temp> temphi or temp<templo:
            print ("!!! temperature not in target range, Data not saved")
            next_id="a"
            savedata=0
        if ratid[0:4]=="00fb" or ratid[0:4]=="3200":
            print ("!!! RFID is not a valid rat ID, Data not saved");
            next_id="n"
            savedata=0
        if savedata:
            with open(datafile, "a") as f:
                f.write(line)
            print ("Data saved to " + datafile)  
        if (next_id=="e"):
            print ("Exit prgram\n")
            sys.exit()
        savedata=1
        print ("Please wait 10 seconds\n")
        time.sleep(10)
        if (next_id=="n"):
            ratid=input("Please enter new rat ID\n")
        else:
            print ("Please test the same rat again\n")
