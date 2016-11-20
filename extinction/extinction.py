#!/usr/bin/python

import RPi.GPIO as gpio
import time
import os
import sys
import Adafruit_MPR121.MPR121 as MPR121
import Adafruit_CharLCD as LCD

def initLCD():
	# Raspberry Pi pin configuration:
	lcd_rs        = 25
	lcd_en        = 24
	lcd_d4        = 23
	lcd_d5        = 17
	lcd_d6        = 21
	lcd_d7        = 22
	lcd_backlight = 4
	# Define LCD column and row size for 16x2 LCD.
	lcd_columns = 16
	lcd_rows    = 2
	# Initialize the LCD using the pins above.
	lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
	lcd.clear()
	sysTime= time.strftime("%H:%M:%S", time.localtime())
	lcd.message("Hurry up, Wifi!\n" + deviceid + "Sess."+ sessionid)
	return lcd 

def initTouch():
	cap = MPR121.MPR121()
	if not cap.begin():
		print ("Error initializing MPR121.  Check your wiring!") 
		lcd.clean()
		lcd.message("Touch Sensor \nConnection Error")
		sys.exit(1)
	print ("Touch Sensor Started\n")
	return cap

def updatelcd(active, inactive, seconds):
	minutes=str(int(seconds/60))
	lcd.clear()
        lcd.message("A:" + str(active) + " I:" + str(inactive) + "\n" + "Min:" + str(minutes) + " "+ deviceid[3:] + "S" +sessionid )

def recordLicks(sessionLength):
	active=0
	inactive=0
	start=time.time()
        updateTime=start
        print ("session started\n")
	while time.time() - start < sessionLength:
		time.sleep(0.07) # sets time resolution
		lapsed = time.time() - start
		if cap.is_touched(1):
			active+=1
			updatelcd(active, inactive, lapsed)
                        updateTime=time.time()
			print(active, inactive, lapsed)
			with open(lickDataFile,"a") as f:
				f.write(str(deviceid) + "\t" + "ratID\t"+today +"\t" + startTime + "\t" + "active\t" +  str(lapsed) + "\n")
				f.close()
		elif cap.is_touched(0):
			inactive+=1
			lapsed=time.time()-start
			updatelcd(active, inactive, lapsed)
                        updateTime=time.time()
			print (active, inactive, lapsed)
			with open(lickDataFile,"a") as f:
				f.write(str(deviceid) + "\t" + "ratID\t"+today +"\t" + startTime + "\t" + "inactive\t" +  str(lapsed) + "\n")
				f.close()
                if time.time() - updateTime > 60 : # update LCD every 60 sec 
			updatelcd(active, inactive, lapsed)
                        updateTime=time.time()
	# finishing the data files
	updatelcd(active, inactive, lapsed)
	print (active, inactive, lapsed)

if __name__ == '__main__':
	idfile=open('/home/pi/deviceid')
	deviceid=idfile.read()
	deviceid=deviceid.strip()
        with open ("/home/pi/sessionid", "r+") as f:
            sessionid=f.read()
            sessionid=sessionid.strip()
            nextSession=int(sessionid)+1  
            f.seek(0)
            f.write(str(nextSession))
            f.close()
	lcd=initLCD()
        time.sleep(1)
	os.system("bash /home/pi/openbehavior/wifi-network/deviceinfo.sh")
        os.system("bash /home/pi/openbehavior/wifi-network/wlan0down.sh")
	os.system("python /home/pi/openbehavior/extinction/cuelights.py &")
	today= time.strftime("%Y-%m-%d", time.localtime())
	startTime= time.strftime("%H:%M:%S", time.localtime())
        lcd.clear()
        lcd.message("Session started\n" + startTime)
	cap=initTouch()
	currentTime=today + "_" + startTime
	lickDataFile="/home/pi/Pies/Extinction/" + deviceid + "S"+ sessionid + "_" + today + ".csv"
	with open(lickDataFile,"a") as f:
		f.write("#Session Started on " + currentTime + "\n")
		f.write("device\tRatID\tDate\tStartTime\tSpout\tlapsed\n")
		f.close()
	recordLicks(3600) # session length in seconds
	with open(lickDataFile,"a") as f:
		f.write("#Session Ended on " +time.strftime("%Y-%m-%d\t%H:%M:%S\t", time.localtime())+"\n")
		f.close()
	os.system('/home/pi/openbehavior/wifi-network/rsync.sh &')

