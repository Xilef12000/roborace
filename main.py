#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()
motorLeft = Motor(Port.C)
motorRight = Motor(Port.B)
colorSensor = ColorSensor(Port.S2)
gyroSensor = GyroSensor(Port.S4)
#touchSensor = TouchSensor(Port.S1)
#watch = StopWatch()

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

while True:
  color = colorSensor.reflection()
  angle = gyroSensor.angle()
  print(angle)
  #print(color)
  #motorLeft.run(int(((speed * (color / target) ** targetCorrector) ** speedCorrector)))
  #motorRight.run(int((speed * ((target - color + target) / target) ** targetCorrector) ** speedCorrector))
  #if (color / target > 1):
  #  color = color * 1.4
  #  motorLeft.run((speed * (color / target) * speedCorrectorWhite))
  #  motorRight.run((speed * ((target - color + target) / target) / speedCorrectorWhite))
  #elif (color / target < 1):
  #  motorLeft.run((speed * (color / target) / speedCorrectorBlack))
  #  motorRight.run((speed * ((target - color + target) / target) * speedCorrectorBlack))
  #else:
  #  motorLeft.run((speed * (color / target)))
  #  motorRight.run((speed * ((target - color + target) / target)))