CC = gcc
CFLAGS = -Wall -g
LIBS = -lwiringPi -lpthread
EXEFILE = pumpcontrol
OBJFILE = pumpcontrol.o

all: pumpcontrol.c

pumpcontrol.c:
	$(CC) -o $(EXEFILE) $(LIBS) $(CFLAGS) pumpcontrol.c

clean:
	rm -f $(EXENAME) $(OBJFILE)
