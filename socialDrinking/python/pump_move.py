from time import sleep
import RPi.GPIO as GPIO
import argparse
import signal
import sys


parser=argparse.ArgumentParser()
parser.add_argument('-steps', type=int, default=3000)
parser.add_argument('-clockwise', type=int, default=1)
args=parser.parse_args()

steps=args.steps
rotate_dir=args.clockwise

GPIO.setwarnings(False)


class PumpMove:
    def __init__(self):
        self.DIR = 20
        self.STEP = 21
        self.CW = 1
        self.CCW = 0
        self.BUTTON = 16
        self.STOP_BUTTON = 12

        self.GPIO = GPIO
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setup(self.DIR, self.GPIO.OUT, initial=self.GPIO.HIGH)
        self.GPIO.setup(self.STEP, self.GPIO.OUT, initial=self.GPIO.HIGH)
        self.GPIO.setup(self.BUTTON, self.GPIO.IN, pull_up_down=self.GPIO.PUD_DOWN)
        self.GPIO.setup(self.STOP_BUTTON, self.GPIO.IN, pull_up_down=self.GPIO.PUD_DOWN)
        self.GPIO.output(self.DIR,self.CW)
        #self.step_count = stp_cnt
        #self.delay = delay
        self.MODE = (14,15)
        self.GPIO.setup(self.MODE, self.GPIO.OUT)
        self.RESOLUTION = {
                            'Full': (0,0),
                            'Half': (1,0),
                            '1/8': (0,1),
                            '1/16': (1,1),
                          }

        # GPIO.output(self.MODE, self.RESOLUTION['Full'])
        # GPIO.output(self.MODE, self.RESOLUTION['Half'])
        self.GPIO.output(self.MODE, self.RESOLUTION['1/8'])
        # GPIO.output(self.MODE, self.RESOLUTION['1/16'])
        
        self.step_counts = steps
        self.delay = .0209 / 50
        self.rotate_dir = rotate_dir

    def move(self, flag):
        if flag:
            self.GPIO.output(self.MODE, self.RESOLUTION['Full'])
            self.GPIO.output(self.DIR, self.CCW)

        for step in range(self.step_counts):
            print("step = ", step)
            self.GPIO.output(self.STEP, self.GPIO.HIGH)
            sleep(self.delay)
            self.GPIO.output(self.STEP, self.GPIO.LOW)
            sleep(self.delay)

    def forward(self):
        # if self.GPIO.input(self.BUTTON) == self.GPIO.HIGH:
        self.GPIO.output(self.MODE, self.RESOLUTION['Full'])
        self.GPIO.output(self.DIR,self.CW)
        for step in range(self.step_counts):
            print("step = ", step)
            self.GPIO.output(self.STEP, self.GPIO.HIGH)
            sleep(self.delay)
            self.GPIO.output(self.STEP, self.GPIO.LOW)
            sleep(self.delay)
        
        self.GPIO.output(self.STEP, self.GPIO.HIGH)

    def backward(self):
        self.GPIO.output(self.MODE, self.RESOLUTION['Full'])
        self.GPIO.output(self.DIR, self.CCW)
        for step in range(self.step_counts):
            print("step = ", step)
            self.GPIO.output(self.STEP, self.GPIO.HIGH)
            sleep(self.delay)
            self.GPIO.output(self.STEP, self.GPIO.LOW)
            sleep(self.delay)
        self.GPIO.output(self.STEP, self.GPIO.HIGH)
        


    def __del__(self):
        self.GPIO.cleanup()
            
mover = PumpMove()    
if __name__ == '__main__':

    FORWARDBUTTON = 16
    BACKWARDBUTTON = 12
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FORWARDBUTTON,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BACKWARDBUTTON,GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def forward_btn_callback(channel):
        if not GPIO.input(FORWARDBUTTON):
            mover.forward()
    
    def backward_btn_callback(channel):
        if not GPIO.input(BACKWARDBUTTON):
            mover.backward()

    def signal_handler(sig, frame):
        GPIO.cleanup()
        sys.exit(0)

    # mover = PumpMove()

    GPIO.add_event_detect(FORWARDBUTTON, GPIO.FALLING, callback=forward_btn_callback,bouncetime=100)
    GPIO.add_event_detect(BACKWARDBUTTON, GPIO.FALLING, callback=backward_btn_callback,bouncetime=100)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()

        
