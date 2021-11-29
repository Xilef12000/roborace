#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()
motorLeft = Motor(Port.C, Direction.COUNTERCLOCKWISE)
motorRight = Motor(Port.B, Direction.COUNTERCLOCKWISE)
#-> could be wrong(f.e. could be "CLOCKWISE")
colorSensor = ColorSensor(Port.S2)
#touchSensor = TouchSensor(Port.S1)
#watch = StopWatch()


#variables
lastDeviation = 0
lastDelta = 0
integral = 0
rateOChange = 0
allDelta = {}
lastTurnrate = 0
allDeviation = {}
deltaTurnrate = 0
lastDeltaTurnrate = 0

#constants
#TARGET = 42 (if taking it directly doesnt work)
TARGET = colorSensor.reflection()
SPEED = 200

WHEEL_DIAMETER = 55.5
AXLE_TRACK = 104
#-> I took the values from an example

robot = DriveBase(motorLeft, motorRight, WHEEL_DIAMETER, AXLE_TRACK)

#The PID-values that we need to determine
P = 0
I = 0
D = 0

ev3.speaker.beep()

#while not touchSensor.pressed():
#    #wait(10)
#    pass

while True:
  #measures the current values
  color = colorSensor.reflection()
  #print(color)
  deviation = TARGET - color

#if the deviation is very small(the roboter is in the middle of the track) all deviations get reset to reset the integral
  if (deviation > -0.01) and (deviation < 0.01): 
    allDeviation = {}
  
  allDeviation.append(deviation)
  integral = sum(allDeviation)
  delta = lastDeviation - deviation
  
#This is here to determine if there is a turningpoint
  turnrate = P * deviation + I * integral + D * rateOChange

  deltaTurnrate = lastTurnrate - turnrate
  
#This determines if the previos point was the turnig point if yes all deltas get reset to reset the turnrate
  if abs(deltaTurnrate) < abs(lastDeltaTurnrate):
    allDelta = {}

  allDelta.append(delta)

  lastDeltaTurnrate = deltaTurnrate
  lastDeviation = deviation
  lastTurnrate = turnrate

  rateOChange = sum(allDelta)/range(allDelta)
  
  turnrate = P * deviation + I * integral + D * rateOChange #This is the final turnrate which is actually used

  robot.drive(turnrate, SPEED)
