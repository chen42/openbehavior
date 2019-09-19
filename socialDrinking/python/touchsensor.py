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

import Adafruit_MPR121.MPR121 as MPR121
import sys

class TouchSensor:
	def __init__(self):
		# Initialize hardware
		self.cap = MPR121.MPR121()
		if not self.cap.begin():
			print('Error initializing MPR121.  Check your wiring!')
			sys.exit(1)
		# Get last touched
		self.lasttouched = self.cap.touched()
		self.touched = self.lasttouched
	def readPinTouched(self):
		self.lasttouched = self.touched
		self.touched = self.cap.touched()
		for i in range(3):
			pinbit = 1 << i
			if self.touched & pinbit and not self.lasttouched & pinbit:
				return i
			if not self.touched & pinbit and self.lasttouched & pinbit:
				return -i
