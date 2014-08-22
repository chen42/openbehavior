import RPi.GPIO as GPIO
import time
from time import gmtime, strftime
import sys

l1=8
l2=10

def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(l1, GPIO.IN)  #for lever 1
    GPIO.setup(l2, GPIO.IN)  #for lever 2

def main(argv):
    c1=0
    c2=0
    t1, animalID = argv.split(":")
    t = float(t1)
    totalT = time.time() + t - .5 #it should end a bit early than our main program
    while True:
        input1= GPIO.input(l1)
        input2= GPIO.input(l2)
        if(input1==0):
            curTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            c1+=1
            data = open('data.csv', 'a')
            data.write(animalID + "," + str(curTime) + ",Lever 1\n")
            data.close()
            time.sleep(.200)
        if(input2==0):
            c2+=1
            curTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            data = open('data.csv', 'a')
            data.write(animalID + "," + str(curTime) + ",Lever 2\n")
            time.sleep(.200)
        if(time.time()>totalT):
            print(c1,":",c2)
            break


if __name__ == "__main__":
    init()
    main(sys.argv[1])
