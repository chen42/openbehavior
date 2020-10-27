
from time import sleep
import RPi.GPIO as GPIO
from gpiozero import Button
from gpiozero import DigitalInputDevice

GPIO.setwarnings(False)

request = input("""
                Enter a number to start a test:
                    1 - Test left and right buttons
                    2 - Test pump forward limit
                    3 - Test Pump backward limit
                    4 - Test pump move
                """)

while True:

    if request == 1:
        left_button = Button("GPIO5")
        right_button = Button("GPIO27")

        def left_btn_press():
            while left_button.value == 1:
                print("left button pressed")

        def right_btn_press():
            while right_button.value == 1:
                print("right button pressed")

        left_button.when_pressed = left_btn_press
        right_button.when_pressed = right_btn_press

    elif request == 2:
        forward_limit = GPIO.setup("24", GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        if GPIO.input(24):
            print("forward limit pressed.")

    elif request == 3:
        backward_limit = DigitalInputDevice("GPIO23")

        if backward_limit.value == 1:
            print("backward limit pressed")
            
    elif request == 4:
        steps = 200
        rotate_dir = 1
        DIR = 26
        STEP = 6
        CW = 1
        CCW = 0
        GPIO = GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(STEP, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.output(DIR,CW)
        MODE = (17,22)
        GPIO.setup(MODE, GPIO.OUT)
        RESOLUTION = {
                            'Full': (0,0),
                            'Half': (1,0),
                            '1/8': (0,1),
                            '1/16': (1,1),
                          }
        
        step_counts = steps
        delay = .0209 / 50

        GPIO.output(STEP, GPIO.HIGH)
        GPIO.output(DIR, CW)
        for step in range(steps):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)

        
        GPIO.output(DIR, CCW)
        for step in range(steps):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)
        
        
        GPIO.cleanup(MODE)
        
        
