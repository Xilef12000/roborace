#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time 

ev3 = EV3Brick()
motorShoot = Motor(Port.A)
motorSensor = TouchSensor(Port.S1)
#watch = StopWatch()

ev3.speaker.beep()
time.sleep(0.5)
while True:
    #wait(10)
  if motorSensor.pressed():
    motorShoot.run(500)
  else:
    motorShoot.run(0)
