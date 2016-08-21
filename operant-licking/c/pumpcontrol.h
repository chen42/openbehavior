#ifndef PUMPCONTROL_H
#define PUMPCONTROL_H

/* Macro definitions */

#define DIR_PIN 0
#define STEP_PIN 2
#define SLEEP_PIN 3
#define MS3_PIN 12
#define MS2_PIN 13
#define MS1_PIN 14
#define SW1_PIN 25
#define SW2_PIN 28
/* Since raspi has four cores with one thread each, */
/* the maximum number of threads should be four */
#define MAX_NUM_THREADS 4

/* struct definitions */
typedef struct pumpControlState {
  float position;
  float pitch;
  float steps;
  float stepsPerMm;
  float mlPerS;
  float mlPerMm;
  int sw1State;
  int sw2State;
} pumpControlState;

/* motor commands are represented by an enumerated type */
typedef enum e_motor_cmd {
  FORWARD,
  REVERSE,
  IDLE,
  UNDEFINED
} motor_cmd;

/* Function declarations */
int setupPumpPins(void);
int initPumpState(pumpControlState *ps);
int move(float ml);
int gotoAbsolutePos(float ml);
int motorSleep(void);
void *querySwitches(void *p);
motor_cmd parseSwitchState(pumpControlState *ps);

#endif /* PUMPCONTROL_H */
