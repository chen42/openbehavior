#!/usr/bin/python

import Adafruit_CharLCD

# create new lcd object
lcd = Adafruit_CharLCD.Adafruit_CharLCD()
lcd.begin(16,1)

# Display some stuff
lcd.clear()
lcd.message("Scientia est\n")
lcd.message("    lux lucis")
