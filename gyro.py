#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time

ev3 = EV3Brick()
motorLeft = Motor(Port.C)
motorRight = Motor(Port.B)
motorShoot = Motor(Port.A)
colorSensor = ColorSensor(Port.S2)
gyroSensor = GyroSensor(Port.S4)
#watch = StopWatch()

angleTarget = 120
angleTargetAccuracy = 1
speedOffset = 79.436
speedOffset = 0
turnSpeed = 100
target = 42
target = colorSensor.reflection()
targetCorrector = 1
speed = 700
speed = 200
speedCorrectorBlack = 1.3
speedCorrectorWhite = 1.5

ev3.speaker.beep()
gyroSensor.reset_angle(0)
time.sleep(0.5)
timeNow = time.time()
angle = 0
angleAverage = []
while True:
  #angle = gyroSensor.angle()
  AngleSpeed = gyroSensor.speed() - speedOffset
  timeOld = timeNow
  timeNow = time.time()
  timeDelta = timeNow - timeOld
  angleDelta = AngleSpeed * timeDelta
  angle += angleDelta
  #print(angle)
  color = colorSensor.reflection()
  angleAverage.append(gyroSensor.speed())
  if len(angleAverage) >= 1000:
    print(sum(angleAverage)/len(angleAverage))