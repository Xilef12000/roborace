#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

target = 42
targetCorrector = 1
speed = 200
speedCorrector = 1


ev3 = EV3Brick()
motorLeft = Motor(Port.C)
motorRight = Motor(Port.B)
colorSensor = ColorSensor(Port.S2)
#touchSensor = TouchSensor(Port.S1)
watch = StopWatch()

ev3.speaker.beep()

#while not touchSensor.pressed():
#    #wait(10)
#    pass

while True:
  color = colorSensor.reflection()
  print(color)
  motorLeft.run(((speed * (color / target) ** targetCorrector) ** speedCorrector))
  motorRight.run(((speed * ((target - color + target) / target) ** targetCorrector) ** speedCorrector))