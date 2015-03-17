'''
    bmp183 - Adafruit BMP183 SPI interface for Raspberry Pi  
    Copyright (C) 2014 Przemo Firszt @ https://github.com/PrzemoF/bmp183

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from bmp183 import bmp183

bmp = bmp183()
bmp.measure_pressure()
print "Temperature: ", bmp.temperature, "deg C"
print "Pressure: ", bmp.pressure/100.0, " hPa"
quit()

#TODO: Log temp/pressure to data file
