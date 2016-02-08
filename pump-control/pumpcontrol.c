#include <wiringPi.h>
#include <time.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <stdbool.h>
#include "pumpcontrol.h"

// Static global variable to store pump controller state
static pumpControlState pcstate;
// Mutexes to control execution of switch polling thread
static bool pollingEnabled = true;

int setupPumpPins(void) {
  // initialize the wiringPi library
  wiringPiSetup();
  // set mode for the output pins
  pinMode(DIR_PIN, OUTPUT);
  pinMode(STEP_PIN, OUTPUT);
  pinMode(SLEEP_PIN, OUTPUT);
  pinMode(MS3_PIN, OUTPUT);
  pinMode(MS2_PIN, OUTPUT);
  pinMode(MS1_PIN, OUTPUT);
  // set mode for the input pins
  pinMode(SW1_PIN, INPUT);
  pinMode(SW2_PIN, INPUT);
  // enable pull-down resistor for switch pins
  pullUpDnControl(SW1_PIN, PUD_DOWN);
  pullUpDnControl(SW2_PIN, PUD_DOWN);
  // return 0 for no errors
  return 0;
}

int initPumpState(pumpControlState *ps) {
  ps->position = 0.0f;
  ps->pitch = 0.8f;
  ps->steps = 3200.0f;
  ps->stepsPerMm = (ps->steps) / (ps->pitch);
  ps->mlPerS = 0.7f;
  ps->mlPerMm = 0.1635531002398778f;
  ps->sw1State = 0;
  ps->sw2State = 0;
  return 0;
}

int move(float ml) {
  digitalWrite(SLEEP_PIN, LOW);
  digitalWrite(DIR_PIN, ((ml < 0) ? HIGH : LOW));
  float sPerHalfStep = ((pcstate.mlPerMm) / (pcstate.stepsPerMm) / (pcstate.mlPerS) / 2.0);
  pcstate.steps = ml / pcstate.mlPerMm * pcstate.stepsPerMm + 0.5f;
  int target = time(NULL);
  for(int i = 0; i < abs(pcstate.steps); ++i) {
    digitalWrite(STEP_PIN, HIGH);
    target += sPerHalfStep;
    while(time(NULL) < target) {
      sleep(0);
    }
    digitalWrite(STEP_PIN, LOW);
    target += sPerHalfStep;
    while(time(NULL) < target) {
      sleep(0);
    }
    pcstate.position += ml;
  }
  return 0;
}

int gotoAbsolutePos(float ml) {
  move(ml - pcstate.position);
  return 0;
}

int motorSleep(void) {
  digitalWrite(SLEEP_PIN, LOW);
  return 0;
}

motor_cmd parseSwitchState(pumpControlState *ps) {
  if(ps->sw1State ^ ps->sw2State) {
    return IDLE;
  } else if (ps->sw1State) {
    return REVERSE;
  } else if (ps->sw2State) {
    return FORWARD;
  } else {
    return UNDEFINED;
  }
}

void *querySwitches(void *p) {
  while(pollingEnabled) {
    pumpControlState *ps = (pumpControlState *) p;
    int switchOne = digitalRead(SW1_PIN);
    int switchTwo = digitalRead(SW2_PIN);
    ps->sw1State = switchOne;
    ps->sw2State = switchTwo;
  }
  return;
}

int main(void) {
  // array to track threads being used by the program
  pthread_t threads[MAX_NUM_THREADS];
  // integer identifier for the thread that polls the switches
  int pollThread;
  // stores the current command for the motor
  motor_cmd currCmd = IDLE;
  // Initialize the pump controller state
  initPumpState(&pcstate);
  // Setup the pins
  setupPumpPins();
  // create new thread to continuously poll the switches
  pollThread = pthread_create(&threads[0], NULL, querySwitches, (void *) &pcstate);
  while(1) {
    // halt polling temporarily to get consistent switch state
    pollingEnabled = false;
    // parse the switch state to determine command for motor
    currCmd = parseSwitchState(&pcstate);
    // resume polling
    pollingEnabled = true;
    // perform action indicated by currCmd
    switch(currCmd) {
    	case FORWARD:
	  move(1);
	  break;
    	case REVERSE:
	  move(-1);
	  break;
    	case IDLE:
	  move(0);
	  break;
    	default:
	  break;
    }
  }
  // Clean up threads
  pthread_exit(NULL);
  return 0;
}
