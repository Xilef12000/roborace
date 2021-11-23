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
#touchSensor = TouchSensor(Port.S1)
#watch = StopWatch()

angleTarget = 0
angleTargetAccuracy = 5
speedOffset = 79.436
turnSpeed = 10
target = 42
target = colorSensor.reflection()
targetCorrector = 1
speed = 700
speedCorrectorBlack = 1.3
speedCorrectorWhite = 1.5

ev3.speaker.beep()
gyroSensor.reset_angle(0)
#while not touchSensor.pressed():
#    #wait(10)
#    pass

timeNow = time.time()
angle = 0
#angleAverage = []
while True:
  color = colorSensor.reflection()
  #angle = gyroSensor.angle()
  speed = gyroSensor.speed() - speedOffset
  timeOld = timeNow
  timeNow = time.time()
  timeDelta = timeNow - timeOld
  angleDelta = speed * timeDelta
  angle += angleDelta
  print(angle)

  #angleAverage.append(gyroSensor.speed())
  #if len(angleAverage) >= 1000:
  #  print(sum(angleAverage)/len(angleAverage))

  print(color)
  if (color < 70):
    #motorLeft.run(int(((speed * (color / target) ** targetCorrector) ** speedCorrector)))
    #motorRight.run(int((speed * ((target - color + target) / target) ** targetCorrector) ** speedCorrector))
    if (color / target > 1):
      color = color * 1.4
      motorLeft.run((speed * (color / target) * speedCorrectorWhite))
      motorRight.run((speed * ((target - color + target) / target) / speedCorrectorWhite))
    elif (color / target < 1):
      motorLeft.run((speed * (color / target) / speedCorrectorBlack))
      motorRight.run((speed * ((target - color + target) / target) * speedCorrectorBlack))
    else:
      motorLeft.run((speed * (color / target)))
      motorRight.run((speed * ((target - color + target) / target)))
  else:
    while True:
      if angle < angleTarget - angleTargetAccuracy:
        motorLeft.run(turnSpeed)
        motorRight.run(-turnSpeed)
      elif angle > angleTarget + angleTargetAccuracy:
        motorLeft.run(-turnSpeed)
        motorRight.run(turnSpeed)
      else:
        motorLeft.run(0)
        motorRight.run(0)
        motorShoot.run(0)
        break
