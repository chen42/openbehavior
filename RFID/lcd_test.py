#!/usr/bin/python

import pylcdlib
lcd = pylcdlib.lcd(0x21, 0)
lcd.lcd_puts("Scientia est", 1)
lcd.lcd_puts("       lux lucis", 2)
