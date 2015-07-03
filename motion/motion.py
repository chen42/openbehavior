import time
from time import strftime, localtime
import RPi.GPIO as io
io.setmode(io.BOARD)

pir_pin = 12 
led_pin =37

io.setup(pir_pin, io.IN)        # activate input
io.setup(led_pin, io.OUT)       # activate input
start=time.time()

# Each box has its own ID
idfile=open("/home/pi/boxid")
boxid=idfile.read()
boxid=boxid.strip()
datafile='/home/pi/motion'+ boxid + "_" + time.strftime("%Y-%m-%d_%H:%M:%S", localtime()) + ".csv"

#sessionLength=3600
sessionLength=10.0

# open data file
with open(datafile,"a") as f:
	f.write("#Session Started on " +time.strftime("%Y-%m-%d\t%H:%M:%S\t", localtime())+"\n")
	f.write("boxid\tseconds\n")
	f.close()
time.sleep(2)


def motion(pir_pin, start, sessionLength):
	cnt=0
	while time.time()-start < sessionLength:
		if io.input(pir_pin):
			print time.strftime("%Y-%m-%d\t%H:%M:%S")
			with open(datafile,"a") as f:
				lapsed=time.time()-start
				f.write(boxid +"\t"+ str(lapsed) +"\n")
				f.close()
			io.output(led_pin, True)
			time.sleep(0.05)
			io.output(led_pin, False)
			time.sleep(0.05)
			cnt=cnt+1
	return cnt


if __name__== '__main__':
	CNT=motion(pir_pin, start, sessionLength)
	with open(datafile, "a") as f:
		f.write("Total Activity:\t"+str(CNT)+"\n")
		f.write("#session Ended at " + time.strftime("%H:%M:%S", localtime())+"\n")

