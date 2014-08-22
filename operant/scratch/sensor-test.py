import os
import scratch

s = scratch.Scratch()

message = s.receive()

#print(type(message))
#print(message)

sensor="measure temp and humidity"

for key, value in message.iteritems():
    print(value)
    if sensor in value:
        os.system("sudo python3 /home/pi/OpenB/htu21d.py")
