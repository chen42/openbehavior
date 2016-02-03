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
import RPi.GPIO as gpio

# Helper function to clear the screen and reset the cursor
def clearScreen():
	print(chr(27) + "[2J")
	print(chr(27) + "[H")

# BEGIN CLASS PumpInterface
class PumpInterface:
	def __init__(self, pumpToInterface):
		self.pump = pumpToInterface
		self.steps = 0
		gpio.setwarnings(False)
		gpio.setmode(GPIO.BOARD)
		gpio.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	# BEGIN Main Menu Display Method
	def dispMenu(self):
		print("----------------------------------------------------")
		print("| Pump Control | Ver. 0.01 | Edit parameters below |")
		print("----------------------------------------------------")
		print("1) Steps: " + str(self.steps))
		print("2) Speed: " + str((self.pump).getMlPerS()) + " ml/s")
		print("3) Pitch: " + str((self.pump).getPitch()))
		print("4) ml per mm: " + str((self.pump).getMlPerMm()))
		print("5) Begin stepping")
		print("6) Exit program")
		print("----------------------------------------------------")
		print("POSITION: " + str((self.pump).getPosition()) + " mm")
		print("STEPS PER MM: " + str((self.pump).getStepsPerMm()))
		print("----------------------------------------------------")
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
		clearScreen()
		while(True):
			if(gpio.input(37)):
				self.steps = 10
				self.startMovement()
			self.useropt = 'derp'
			self.dispMenu()
			self.useropt = str(input())
			if self.useropt == '1':
				self.readSteps()
			elif self.useropt == '2':
				self.readSpeed()
			elif self.useropt == '3':
				self.readPitch()
			elif self.useropt == '4':
				self.readMlPerMm()
			elif self.useropt == '5':
				self.startMovement()
			elif self.useropt == '6':
				raise SystemExit
			else:
				print("Invalid choice. Please enter again.")
			clearScreen()
	# END Program Main Loop
# END CLASS PumpInterface

if __name__ == "__main__":
	p = pumpcontrol.Pump()
	pi = PumpInterface(p)
	pi.mainLoop()
