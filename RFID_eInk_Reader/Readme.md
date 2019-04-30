# This is a RFID reader with an eInk hat display

## 2.7 inch e-paper hat
* From [WaveShare.com](https://www.waveshare.com/2.7inch-e-Paper-HAT.htm)
* User manual in [PDF](https://www.waveshare.com/w/upload/3/31/2.7inch_e-paper_hat_user_manual_en.pdf)

## RFID USB reader 
* https://www.amazon.com/Reader-LANMU-125khz-Contactless-Proximity/dp/B07B7H6CQ2

## Software
* Library https://github.com/waveshare/e-Paper/tree/master/2.7inch_e-paper_code/RaspberryPi/
* Steps not described in the user manual
	* enable SPI interface in the PI ```sudo raspi-config```
* For the python demo code, make sure the font is present in your system. 
* To run the python code automatically after boot, do the following
  * change the boot into command line and enable auto login with user pi by running ```sudo raspi-config```  
  * add the python program to the end of the .bashrc file for user pi



