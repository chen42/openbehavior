from time import sleep
import RPi.GPIO as GPIO
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('-steps', type=int, default=3000)
parser.add_argument('-clockwise', type=int, default=1)
args=parser.parse_args()

steps=args.steps
rotate_dir=args.clockwise

GPIO.setwarnings(False)
#DIR = 20
#STEP = 21
#CW = 1
#CCW = 0
#SPR = 200 #120

class PumpMove:
    def __init__(self):
        self.DIR = 20
        self.STEP = 21
        self.CW = 1
        self.CCW = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.STEP, GPIO.OUT)
        GPIO.output(self.DIR,self.CW)
        #self.step_count = stp_cnt
        #self.delay = delay
        self.MODE = (14,15)
        GPIO.setup(self.MODE, GPIO.OUT)
        self.RESOLUTION = {
                            'Full': (0,0),
                            'Half': (1,0),
                            '1/8': (0,1),
                            '1/16': (1,1),
                          }

        GPIO.output(self.MODE, self.RESOLUTION['Full'])
        
        self.step_counts = steps
        self.delay = .0209 / 50
        self.rotate_dir = rotate_dir
    def move(self):
        if(not self.rotate_dir):
            GPIO.output(self.DIR, self.CCW)

        for step in range(self.step_counts):
            GPIO.output(self.STEP, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(self.STEP, GPIO.LOW)
            sleep(self.delay)

    def __del__(self):
        GPIO.cleanup()
            


if __name__ == '__main__':
    mover = PumpMove()
    mover.move()
    
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(DIR, GPIO.OUT)
#GPIO.setup(STEP, GPIO.OUT)
##GPIO.output(DIR,CW)
#GPIO.output(DIR,rotate_dir)
#
#step_count = SPR
#delay = .0208
#
#
#MODE = (14,15)
#GPIO.setup(MODE,GPIO.OUT)
#
#RESOLUTION = {
#        'Full': (0,0),
#        'Half': (1,0),
#        '1/8': (0,1),
#        '1/16': (1,1),
#        }
#
#GPIO.output(MODE, RESOLUTION['Full'])
#
#step_count = steps #10000 #SPR * 50
#delay = .0209 / 50#50


#GPIO.output(DIR,CCW)
#for x in range(step_count):
#    GPIO.output(STEP,GPIO.HIGH)
#    sleep(delay)
#    GPIO.output(STEP, GPIO.LOW)
#    sleep(delay)


#GPIO.cleanup()


