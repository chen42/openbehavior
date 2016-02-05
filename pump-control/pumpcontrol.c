#include <wiringPi.h>
#include "pumpcontrol.h"

static double pump_pos = 0.0;
static double pump_pitch = 0.8;
static double pump_steps = 3200;
static double pump_steps_per_mm = pump_steps / pump_pitch;
static double pump_ml_per_s = 0.7;
static double pump_ml_per_mm = 0.1635531002398778;

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
  // set mode for the input pin
  pinMode(SW1_PIN, INPUT);
  // enable pull-down resistor for switch pin
  pullUpDnControl(SW1_PIN, PUD_DOWN);
  // return 0 for no errors
  return 0;
}

int main(void) {
  // Setup the pins
  setupPumpPins();
  return 0;
}
