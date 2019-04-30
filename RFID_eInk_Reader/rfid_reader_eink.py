#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd2in7
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

epd = epd2in7.EPD()
epd.init()
epd.Clear(0xFF)
    
    
def show(text):
    Himage = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)  # 255: clear the frame
    # Horizontal
    print("Drawing")
    draw = ImageDraw.Draw(Himage)
    font32 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',32)
    draw.text((10, 0), text, font = font32, fill = 0)
    epd.display(epd.getbuffer(Himage))
    time.sleep(2)
        

show("Ready to scan")
while True:
    rfid=raw_input("Waiting for RFID ")
    rfid=hex(int(rfid)).upper()
    show(rfid)
    time.sleep(2)

epd.sleep()
