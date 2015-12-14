#!/usr/bin/python

# Copyright 2015 University of Tennessee Health Sciences Center
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

import pumpcontrol

# BEGIN CLASS PumpInterface
class PumpInterface:
	def __init__(self, pumpToInterface):
		self.pump = pumpToInterface
		self.steps = 0
	# BEGIN Main Menu Display Method
	def dispMenu():
		print("--------------------------------------------------------------------------------")
		print("| Pump Control | Ver. 0.01 | Edit parameters below |")
		print("--------------------------------------------------------------------------------")
		print("1) Steps: " + self.movement)
		print("2) Speed: " + (self.pump).getMlPerS() + " ml/s")
		print("3) Pitch: " + (self.pump).getPitch())
		print("4) ml per mm: " + (self.pump).getMlPerMm())
		print("M) Begin stepping")
		print("X) Exit program")
	# END Main Menu Display Method
	# BEGIN User Input Section
	def readSteps(self):
		print("Enter amount to step: ")
		self.steps = int(input())
	def readSpeed(self):
		print("Enter speed (in ml/s): ")
		(self.pump).setMlPerS(float(input()))
	def readPitch(self):
		print("Enter pitch: ")
		(self.pump).setPitch(float(input()))
	def readMlPerMm(self):
		print("Enter ml per mm: ")
		(self.pump).setMlPerMm(float(input()))
	# END User Input Section
	def startMovement(self):
		(self.pump).move(self.steps)
	# BEGIN Program Main Loop
	def mainLoop(self):
		while(True):
			self.useropt = 'derp'
			self.dispMenu()
			self.useropt = input()
			while self.useropt != 'M':
				if self.useropt == '1':
					self.readSteps()
				elif self.useropt == '2':
					self.readSpeed()
				elif self.useropt == '3':
					self.readPitch()
				elif self.useropt == '4':
					self.readMlPerMm()
				elif self.useropt == 'M':
					self.startMovement()
				elif self.useropt == 'X':
					raise SystemExit
				else
					print("Invalid choice. Please enter again.")
	# END Program Main Loop
# END CLASS PumpInterface
