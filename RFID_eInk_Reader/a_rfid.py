#!/usr/bin/python
# -*- coding:utf-8 -*-

#import epd2in7
import time
#from PIL import Image,ImageDraw,ImageFont
import os 


#epd = epd2in7.EPD()
#epd.init()
#epd.Clear(0xFF)

def show(text):
#    Himage = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)  # 255: clear the frame
#    draw = ImageDraw.Draw(Himage)
#    font32 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',32)
#    draw.text((10, 0), text, font = font32, fill = 0)
#    epd.display(epd.getbuffer(Himage))
    print(text)

print("Ready to scan")
line=""
cnt=0
while True:
    if (cnt == 5 ):
        cnt=0
        line=""
    cnt=cnt+1
    rfid=input("Waiting for RFID")
    #rfid=hex(int(rfid)).upper()
    l=len(rfid)
    line=line +  rfid[2:l-4] + "." + rfid[-4:] +  "\n"
    print(line)
    time.sleep(.5)

