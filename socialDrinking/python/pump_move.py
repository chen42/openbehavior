from time import sleep
import RPi.GPIO as GPIO
# import argparse
import signal
import sys
from gpiozero import InputDevice
from gpiozero import Servo
# from gpiozero import DigitalInputDevice
# from gpiozero import SmoothedInputDevice


# parser=argparse.ArgumentParser()
# parser.add_argument('-steps', type=int, default=100)
# parser.add_argument('-clockwise', type=int, default=1)
# args=parser.parse_args()

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
        self.RESOLUTION = {
                            'Full': (0,0),
                            'Half': (1,0),
                            '1/8': (0,1),
                            '1/16': (1,1),
                          }

        # GPIO.output(self.MODE, self.RESOLUTION['Full'])
        # GPIO.output(self.MODE, self.RESOLUTION['Half'])
        # self.GPIO.output(self.MODE, self.RESOLUTION['1/8'])
        # GPIO.output(self.MODE, self.RESOLUTION['1/16'])
        
        self.step_counts = steps
        self.delay = .0209 / 50
        self.rotate_dir = rotate_dir

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
        
    def __del__(self):
        self.GPIO.cleanup()
            
# if __name__ == '__main__':
#     mover = PumpMove()    
#     SERVO = 2
#     RECEIVER = 26

#     FORWARDBUTTON = 16
#     BACKWARDBUTTON = 12
#     IR = 17
#     SERVO = 27
#     sensor = InputDevice(IR, pull_up=True)
#     servo = Servo(SERVO, initial_value=None)
    
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(FORWARDBUTTON,GPIO.IN, pull_up_down=GPIO.PUD_UP)
#     GPIO.setup(BACKWARDBUTTON,GPIO.IN, pull_up_down=GPIO.PUD_UP)


#     def forward_btn_callback(channel):
#         if not GPIO.input(FORWARDBUTTON):
#             mover.move('forward')
#             # mover.forward()
    
#     def backward_btn_callback(channel):
#         if not GPIO.input(BACKWARDBUTTON):
#             mover.move('backward')
#             # mover.backward()

#     def signal_handler(sig, frame):
#         GPIO.cleanup()
#         sys.exit(0)

#     def ir_callback(channel):
#         # object detected
#         if sensor.value == 1:
#             print("1")
#             servo.min()
#             sleep(.5)
#             servo.mid()
#             sleep(.5)
#             servo.max()
#             sleep(.5)

#         # object disappeared
#         if sensor.value == 0:
#             print("0")
#             servo.max()
#             sleep(.5)
#             servo.mid()
#             sleep(.5)
#             servo.min()
#             sleep(.5)

#     GPIO.add_event_detect(IR, GPIO.FALLING, callback=ir_callback, bouncetime=100)


#     GPIO.add_event_detect(FORWARDBUTTON, GPIO.FALLING, callback=forward_btn_callback,bouncetime=100)
#     GPIO.add_event_detect(BACKWARDBUTTON, GPIO.FALLING, callback=backward_btn_callback,bouncetime=100)


#     signal.signal(signal.SIGINT, signal_handler)
#     signal.pause()

        
