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
timesIntegral = 1
timesROC = 0
rateOChange = 0

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
  
  delta = lastDeviation - deviation
  
  #Multiplies the measured values with the fitting Corrector and than adds them to get the turnrate
  turnrate = P * deviation + I * integral + D * rateOChange 

  robot.drive(turnrate, SPEED)
  integral = (integral * timesIntegral) + deviation
  rateOChange = (timesROC * rateOChange) + delta

  timesIntegral +=1
  timesROC += 1
  
  rateOChange /= timesROC
  integral /= timesIntegral