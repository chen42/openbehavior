#!/usr/bin/python

# Copyright 2016 University of Tennessee Health Sciences Center
# Author: Matthew Longley <mlongle1@uthsc.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or(at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# BEGIN IMPORT PRELUDE
import RPi.GPIO as gpio
import Adafruit_MPR121.MPR121 as MPR121
import pumpcontrol
# END IMPORT PRELUDE

# BEGIN CONSTANT DEFINITIONS
SW1 = int(37)
SW2 = int(38)
# END CONSTANT DEFINITIONS

# Initialize GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

# Initialize pump
pump = pumpcontrol.Pump(gpio)

# Move pump
pump.move(10)

