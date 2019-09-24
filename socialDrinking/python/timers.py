#!/usr/bin/env python3

from threading import Timer
import time

def resetPumpTimeout(rat):
#    global pumptimedout
    print (rat + " timeout reset")
    pumptimedout[rat] = False

rat1ID="rat...1"
rat2ID="rat...2"

pumptimedout={rat1ID:False, rat2ID:False}
#pumptimedout=False
touchcounter={rat1ID:0, rat2ID:0}
nextratio={rat1ID:5, rat1ID:5}
rew={rat1ID:0,rat2ID:0}
timeout=5
print(touchcounter[rat1ID])

#resetPumpTimeout(rat1ID)
while True: 
    rat=rat1ID
    time.sleep(1)
    print ("timedout"+str(pumptimedout))
    if not pumptimedout[rat] :
        touchcounter[rat] += 1 # for issuing rewards
        print ("touchcount="+str(touchcounter[rat]))
        if touchcounter[rat] >= nextratio[rat]:
            rew[rat]+=1
            print ("reward"+str(rew[rat]))
            touchcounter[rat] = 0
            pumptimedout[rat] = True
            pumpTimer = Timer(timeout, resetPumpTimeout, [rat])
            pumpTimer.start()
