#code from https://www.raspberrypi.org/forums/viewtopic.php?t=220247#p1352169
# pip3 install pigpio
# git clone https://github.com/stripcode/pigpio-stepper-motor

'''
# connection to adafruit TB6612
# motor: SY28STH32-0674A
Vcmotor --> 12V 5A power supply
VM --> floating
Vcc --> 3V3 Pin 17
GND --> GND Pin 06
PwmA --> 3V3 Pin 01
AIN2 --> Pin 15 - BCM 22
AIN1 --> Pin 11 - BCM 17
STBY --> Pin 13 - BCM 27
BIN1 --> Pin 16 - BCM 23
BIN2 --> Pin 18 - BCM 24
PwmB --> Pin 32 - BCM
MotorA --> Red (A+) and Green (A-) wires
MotorB --> Blue (B+) and Black (B-) wires
GND of Power supply --> Pin 39 (gnd) Raspberry Pi
'''

import pigpio, time
from PigpioStepperMotor import StepperMotor

pi = pigpio.pi()
motor = StepperMotor(pi, 17, 23, 22, 24)
pwma = pigpio.pi()
pwma.write(18,1)
pwmb = pigpio.pi()
pwmb.write(12,1)
stby = pigpio.pi()
stby.write(27,0)
for i in range(500):
  stby.write(27,1)
  motor.doСlockwiseStep()
