CC = gcc
CFLAGS = -Wall -g
LIBS = -lwiringPi -lpthread
EXEFILE = pumpcontrol
OBJFILE = pumpcontrol.o

all: pumpcontrol.c
	gcc -o $(EXEFILE) $(LIBS)

pumpcontrol.c:
	$(CC) -c pumpcontrol.c $(CFLAGS)

clean:
	rm -f $(EXENAME) $(OBJFILE)
