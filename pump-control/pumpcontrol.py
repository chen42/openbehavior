#!/usr/bin/python

# Copyright 2013 Michigan Technological University
# Author: Bas Wijnen <bwijnen@mtu.edu>
# This design was developed as part of a project with
# the Michigan Tech Open Sustainability Technology Research Group
# http://www.appropedia.org/Category:MOST
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
import sys
import time
try:
	import RPi.GPIO as gpio
	gpio.setwarnings(False)
	gpio.setmode(gpio.BOARD)
except:
	sys.stderr.write('Warning: using emulation because RPi.GPIO could not be used\n')
	class gpio:
		LOW = 0
		HIGH = 1
		IN = 0
		OUT = 1
		@classmethod
		def output(cls, pin, state):
			pass
		@classmethod
		def setup(cls, pin, type, initial):
			pass
# END IMPORT PRELUDE

# BEGIN Pin configuration
DIR = int(11) #int(config['dir-pin'])
STEP = int(13) #int(config['step-pin'])
SLEEP = int(15) #int(config['sleep-pin'])
MS3 = int(19) #int(config['ms3-pin'])
MS2 = int(21) #int(config['ms2-pin'])
MS1 = int(23) #int(config['ms1-pin'])
SW1 = int(37)
gpio.setup(SLEEP, gpio.OUT, initial = gpio.HIGH)
gpio.setup(STEP, gpio.OUT, initial = gpio.HIGH)
gpio.setup(DIR, gpio.OUT, initial = gpio.HIGH)
gpio.setup(MS1, gpio.OUT, initial = gpio.HIGH)
gpio.setup(MS2, gpio.OUT, initial = gpio.HIGH)
gpio.setup(MS3, gpio.OUT, initial = gpio.HIGH)
gpio.setup(SW1, gpio.IN, pull_up_down=gpio.PUD_DOWN)
# END Pin configuration

# BEGIN CLASS Pump
class Pump:
    # BEGIN Constructor method
	def __init__(self):
		self.position = 0.
		self.pitch = float(0.8)
		self.steps = float(3200)
		self.steps_per_mm = self.steps / self.pitch
		self.ml_per_s = float(0.7)
		self.ml_per_mm = float(0.1635531002398778)
    # END Constructor method
    # BEGIN Setter and getter methods
	def getPosition(self):
		return self.position
	def setPosition(self, position):
		self.position = position
	def getPitch(self):
		return self.pitch
	def setPitch(self, pitch):
		self.pitch = pitch
	def getSteps(self):
		return self.steps
	def setSteps(self, steps):
		self.steps = steps
	def getStepsPerMm(self):
		return self.steps_per_mm
	def setStepsPerMm(self, steps_per_mm):
		self.steps_per_mm = steps_per_mm
	def getMlPerS(self):
		return self.ml_per_s
	def setMlPerS(self, ml_per_s):
		self.ml_per_s = ml_per_s
	def getMlPerMm(self):
		return self.ml_per_mm
	def setMlPerMm(self, ml_per_mm):
		self.ml_per_mm = ml_per_mm
    # END Setter and getter methods
	def goto(self, ml):
		self.move(ml - self.position)
	def move(self, ml):
		gpio.output(SLEEP, gpio.HIGH)
		gpio.output(DIR, gpio.HIGH if ml < 0 else gpio.LOW)
		s_per_half_step = self.ml_per_mm / self.steps_per_mm / self.ml_per_s / 2
		self.steps = int(ml / self.ml_per_mm * self.steps_per_mm + .5)
		target = time.time()
		for t in range(abs(self.steps)):
			gpio.output(STEP, gpio.HIGH)
			target += s_per_half_step
			while time.time() < target:
				# Yes, this is a busy wait.
				pass
			gpio.output(STEP, gpio.LOW)
			target += s_per_half_step
			while time.time() < target:
				# Yes, this is a busy wait.
				pass
		self.position += ml
	def speed(self, ml_per_s):
		self.ml_per_s = ml_per_s
	def sleep(self):
		gpio.output(SLEEP, gpio.LOW)
# END CLASS Pump

if __name__ == "__main__":
	p = Pump()
	p.setSteps(10)
	while(True):
		if(gpio.input(SW1)):
			p.move(10)
		
