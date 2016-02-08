CC = gcc
CFLAGS = -Wall -g
LIBS = -lwiringPi -lpthread
EXEFILE = pumpcontrol
OBJFILE = pumpcontrol.o

all: pumpcontrol.c

pumpcontrol.c:
	$(CC) -o $(EXEFILE) pumpcontrol.c $(LIBS) $(CFLAGS)

clean:
	rm -f $(EXENAME) $(OBJFILE)
