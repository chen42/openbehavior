# Using the Raspberry Pi single board computer to monitor the lab environment

The sensor we use include the HTU21DF for humidity,  TSL2561 for light,  and BMP180 for barometric pressure. Both the HTU21DF and BMP180 have a temperature senor. So we take the average readout of the two. These sensors are all connected to the Raspberry Pi via I2C.  We also use a I2C  real-time clock (DS1307 from either Adafruit or JBtek. JBtek is cheaper but some of the units we got were not reliable) to ensure the accuracy of the time.  

We tested the MPL3115A2  for barometer but the BMP180 is easier to use.  

Because we ran all these sensor via I2C, an extra 5V power supply is provide to the I2C bus. We use the  [Powergen Dual USB charger](http://www.amazon.com/gp/product/B0073FCPSK) for this purpose. 

The location of the device is identified in a file named locatinID located at /home/pi/. The ID stored in this file is used to name the data file. The location ID is also entered in the data file. This allows the same program to be deployed at multiple locations. The python logger program is ran once every 10 min via cron.

We use this device to monitor the environment of animal housing rooms where the light cycle is reversed. The logger program  writes the lux level during the night to a file called lux.csv. The checklux.py program, also ran via a cron job, checks the lux level during the day and flashes an LED to alert the technician if lights are off during the night.    


