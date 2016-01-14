#!/usr/bin/python

import Adafruit_CharLCD

# create new lcd object
lcd = Adafruit_CharLCD.Adafruit_CharLCD()

# Display some stuff
lcd.clear()
lcd.message("Scientia est\n")
lcd.message("\tluxlucis")
