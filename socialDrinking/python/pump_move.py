from time import sleep
import RPi.GPIO as GPIO
# import argparse
import signal
import sys
from gpiozero import InputDevice
from gpiozero import Servo
from gpiozero import Button
from gpiozero import DigitalInputDevice
import pigpio
# from gpiozero import DigitalInputDevice
# from gpiozero import SmoothedInputDevice


steps=150
rotate_dir=1



GPIO.setwarnings(False)


class PumpMove:
    def __init__(self):
        self.DIR = 26
        self.STEP = 6
        self.CW = 1
        self.CCW = 0
        # self.BUTTON = 16
        # self.STOP_BUTTON = 12

        self.GPIO = GPIO
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setup(self.DIR, self.GPIO.OUT, initial=self.GPIO.HIGH)
        self.GPIO.setup(self.STEP, self.GPIO.OUT, initial=self.GPIO.HIGH)
        # self.GPIO.setup(self.BUTTON, self.GPIO.IN, pull_up_down=self.GPIO.PUD_DOWN)
        # self.GPIO.setup(self.STOP_BUTTON, self.GPIO.IN, pull_up_down=self.GPIO.PUD_DOWN)
        self.GPIO.output(self.DIR,self.CW)
        #self.step_count = stp_cnt
        #self.delay = delay
        self.MODE = (17,22)
        self.GPIO.setup(self.MODE, self.GPIO.OUT)
        # self.GPIO.setup(23, GPIO.IN, pull_up_down=)
        self.RESOLUTION = {
                            'Full': (0,0),
                            'Half': (1,0),
                            '1/8': (0,1),
                            '1/16': (1,1),
                          }
        
        self.step_counts = steps
        self.delay = .0209 / 50
        self.rotate_dir = rotate_dir
        
        self.BACKWARD_LIMIT = DigitalInputDevice("GPIO23")
        
        self.FORWARDBTN = Button("GPIO5")
        self.BACKWARDBTN = Button("GPIO27")
        self.FORWARDBTN.when_pressed = self.forward
        self.BACKWARDBTN.when_pressed = self.backward


    def move(self, direction, steps=150):
        direction_dict = {"forward": self.CW, "backward": self.CCW}

        try:
            self.GPIO.output(self.MODE, self.RESOLUTION['Full'])
            self.GPIO.output(self.DIR, direction_dict[direction])

            for step in range(steps):
                self.GPIO.output(self.STEP, self.GPIO.HIGH)
                sleep(self.delay)
                self.GPIO.output(self.STEP, self.GPIO.LOW)
                sleep(self.delay)

            self.GPIO.output(self.STEP, self.GPIO.HIGH)
        except KeyError:
            print("please enter a correct direction")
        # if direction == "forward":
        #     pass
        # elif direction == "backward":
    
    def forward(self):
        while self.FORWARDBTN.value == 1:
            self.move("forward")
    
    def backward(self):
        while self.BACKWARD_LIMIT.value != 1:
            self.move("backward")
        
        
    def __del__(self):
        self.GPIO.cleanup(self.MODE)


#     GPIO.add_event_detect(IR, GPIO.FALLING, callback=ir_callback, bouncetime=100)


#     GPIO.add_event_detect(FORWARDBUTTON, GPIO.FALLING, callback=forward_btn_callback,bouncetime=100)
#     GPIO.add_event_detect(BACKWARDBUTTON, GPIO.FALLING, callback=backward_btn_callback,bouncetime=100)


#     signal.signal(signal.SIGINT, signal_handler)
#     signal.pause()

        
