import RPi.GPIO as GPIO
import time
import picamera
from htu21d import HTU21D
import sys
import getopt


pump=7
l1=8
l2=10
light=16

fr=5  # fixed ratio
t=5  #the time for which the pump will run, based on the weight of the mouse
c1=0 # counter for lever one
c2=0 # counter for lever two

sensor = HTU21D()

camera = picamera.PiCamera()

def init():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(pump, GPIO.OUT)  #for syringe pump
        GPIO.setup(l1, GPIO.IN)  #for lever 1
        GPIO.setup(l2, GPIO.IN)  #for lever 2
        GPIO.setup(light, GPIO.OUT)  #for light

def main(argv):
        c1=0
        try:
                opts, args = getopt.getopt(argv,"hf:t:",["fr","time"])
        except getopt.GetoptError:
                print("test.py -f <fixedratio> -t <exptime>")
                sys.exit(2)
        for opt, arg in opts:
                if opt == '-h':
                        print("test.py -f <fixedratio> -t <exptime>")
                        sys.exit()
                elif opt in ("-f", "--fr"):
                        fr = arg
                elif opt in ("-t", "--time"):
                        t = arg
        while True:
                input1= GPIO.input(l1)
                input2= GPIO.input(l2)
                if(input1==0):
                        print("Button Pressed ", c1)
                        c1+=1
                        time.sleep(.300)
                if(input2==0):
                        c2+=1
                        time.sleep(.300)
                if(c1>=int(fr)):
                        GPIO.output(pump, True)
                        sensor.reset()
                        print(time.time(), sensor.get_temp(), sensor.get_rel_humidity())
                        print("Spinning")
                        GPIO.output(light, True)
                        camera.capture('image.jpg')
                        time.sleep(float(t))
                        GPIO.output(pump, False)
                        GPIO.output(light, False)
                        c1=0
                        
if __name__ == "__main__":
   init()
   main(sys.argv[1:])
   GPIO.cleanup()
