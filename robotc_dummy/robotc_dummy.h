 /**
 * This C header file provides dummy definitions for types and functions
 * specific to the Lego Mindstorms EV3 ROBOTC version of C.
 * Including this file allows a file written in ROBOTC to be successfully
 * compiled and run (likely with incomprehensible or illogical results).
 *
 */

#pragma once

#ifdef NOTROBOTC

#include <stdarg.h>
#include <stdio.h>

// Types
typedef int task;

typedef enum {
  false,
  true
} bool;

typedef enum {
  soundBlip,
  soundBeepBeep,
  soundDownwardTones,
  soundLowBuzz,
  soundFastUpwardTones,
  soundShortBlip,
  soundException,
  soundLowBuzzShort
} TSounds;

// Display
void displayTextLine(const int nLineNumber, char* sFormatString, ...);
void displayTextLine(const int nLineNumber, char* sFormatString, ...) {
  va_list args;
  va_start(args, sFormatString);
  vprintf(sFormatString, args);
  va_end(args);
  printf("\n");
}

void displayCenteredTextLine(const int nLineNumber, char* sFormatString, ...);
void displayCenteredTextLine(const int nLineNumber, char* sFormatString, ...) {
  va_list args;
  va_start(args, sFormatString);
  vprintf(sFormatString, args);
  va_end(args);
  printf("\n");
}

void displayCenteredBigTextLine(
  const int nLineNumber,
  char* sFormatString, ...
);
void displayCenteredBigTextLine(
  const int nLineNumber,
  char* sFormatString, ...) {
  va_list args;
  va_start(args, sFormatString);
  vprintf(sFormatString, args);
  va_end(args);
  printf("\n");
}

void drawCircle(const int centerX, const int centerY, const int radius);
void drawCircle(const int centerX, const int centerY, const int radius) {}

void drawRect(
  const int left, const int top,
  const int right, const int bottom
);
void drawRect(
  const int left, const int top,
  const int right, const int bottom
) {}

void eraseDisplay();
void eraseDisplay(){}

// Datalog
bool datalogOpen(long nDatalogIndex, long nColumns, bool bAppend);
bool datalogOpen(long nDatalogIndex, long nColumns, bool bAppend) {
  return true;
}

bool datalogAddShort(long nIndex, short data);
bool datalogAddShort(long nIndex, short data) {
  return true;
}

bool datalogAddChar(long nIndex, char data);
bool datalogAddChar(long nIndex, char data) {
  return true;
}

void datalogFlush();
void datalogFlush(){}

void datalogClose();
void datalogClose(){}

// Sensors (buttons)
typedef enum
{
  buttonAny,
  buttonLeft,
  buttonRight
} buttonTypes;
bool getButtonPress(int button);
bool getButtonPress(int button) {
  return true;
}

// Sensors
short getColorReflected(int sensor);
short getColorReflected(int sensor) {
  return 0;
}

float getUSDistance(int nDeviceIndex);
float getUSDistance(int nDeviceIndex) {
  return 0;
}

int getMotorSpeed(int nMotorIndex);
int getMotorSpeed(int nMotorIndex) {
  return 0;
}

int getTouchValue(int nMotorIndex);
int getTouchValue(int nMotorIndex) {
  return 1;
}

// Actuators
void setMotorSpeed(int motor, int speed);
void setMotorSpeed(int motor, int speed) {}

void resetMotorEncoder(int nMotorIndex);
void resetMotorEncoder(int nMotorIndex) {}

int getMotorEncoder(int nMotorIndex);
int getMotorEncoder(int nMotorIndex) {
  return 1;
}

void setMotorTarget(int nMotorIndex, float nPosition, int nspeed);
void setMotorTarget(int nMotorIndex, float nPosition, int nspeed) {}

void waitUntilMotorStop(int nMotorIndex);
void waitUntilMotorStop(int nMotorIndex){}

void playTone(int frequency, int durationIn10MsecTicks);
void playTone(int frequency, int durationIn10MsecTicks) {}

void playSound(TSounds sound);
void playSound(TSounds sound){}

// Other functions
void sleep();
void sleep(){}

int random();
int random() {
  return 1;
}

void stringDelete(char* str, const int nIndex, const int nSize);
void stringDelete(char* str, const int nIndex, const int nSize){}

#endif
