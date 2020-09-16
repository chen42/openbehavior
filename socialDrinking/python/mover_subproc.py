from pump_move import PumpMove

def forward():
    mover = PumpMove()
    mover.move("forward")
    del(mover)

    

# SERVO = 2
# RECEIVER = 26

# FORWARDBUTTON = 5
# BACKWARDBUTTON = 27
# IR = 17


# sensor = InputDevice(IR, pull_up=True)


# GPIO.setmode(GPIO.BCM)
# GPIO.setup(FORWARDBUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(BACKWARDBUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)



