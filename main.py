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
touchSensor = TouchSensor(Port.S1)
ultrasonicSensor = UltrasonicSensor(Port.S3)
#watch = StopWatch()

angleTarget = -240  #angle of the shooting area relative to the start point
angleTargetAccuracy = 1
speedOffset = 0.0 #correcting of the gyro values
turnSpeed = 100 #speed when turning at shooting area
target = 42
target = colorSensor.reflection()
targetCorrector = 1
speed = 500 #robot driving speed maximum 700 (900 is the absolute maximum)
speedCorrectorBlack = 1.2 # 1.1 to 1.5
speedCorrectorWhite = 1.3 # 1.2 to 1.7

ev3.speaker.beep()
gyroSensor.reset_angle(0)
time.sleep(0.5)
while not touchSensor.pressed(): #wait for start button to get pressed
  pass
target = colorSensor.reflection()
timeNow = time.time()
angle = 0
angleAverage = []
while True:
  AngleSpeed = gyroSensor.speed() - speedOffset # |get corrected gyro angle
  timeOld = timeNow                             # |
  timeNow = time.time()                         # |
  timeDelta = timeNow - timeOld                 # |
  angleDelta = AngleSpeed * timeDelta           # |
  angle += angleDelta                           # |
  distance = ultrasonicSensor.distance(silent=False) #get distance
  color = colorSensor.reflection() #get reflection

  if (color < 90):                      # |driving or shooting
  #if (color < 90 and distance < 300):  # |
    print("grayscale")
    if (color / target > 1): #drive in white areas
      color = color * 1.4
      motorLeft.run((speed * (color / target) * speedCorrectorWhite))
      motorRight.run((speed * ((target - color + target) / target) / speedCorrectorWhite))
    elif (color / target < 1): #drive in black areas
      motorLeft.run((speed * (color / target) / speedCorrectorBlack))
      motorRight.run((speed * ((target - color + target) / target) * speedCorrectorBlack))
    else: #drive in optimum
      motorLeft.run((speed * (color / target)))
      motorRight.run((speed * ((target - color + target) / target)))
  else: #shoot modi
    while True:
      AngleSpeed = gyroSensor.speed() - speedOffset # |get corrected gyro angle
      timeOld = timeNow                             # |
      timeNow = time.time()                         # |
      timeDelta = timeNow - timeOld                 # |
      angleDelta = AngleSpeed * timeDelta           # |
      angle += angleDelta                           # |
      if angle < angleTarget - angleTargetAccuracy: #turn right
        print("turning")
        motorLeft.run(turnSpeed)
        motorRight.run(-turnSpeed)
      elif angle > angleTarget + angleTargetAccuracy: #turn left
        print("turning")
        motorLeft.run(-turnSpeed)
        motorRight.run(turnSpeed)
      else:
        while(True):
          rgb = colorSensor.rgb()
          if(not(rgb[0] < 30 and rgb[1] < 40 and rgb[2] > 50)): #drive forward until blue stripe
            print("forward")
            motorLeft.run(turnSpeed) #drive
            motorRight.run(turnSpeed)
          else: #shoot on blue stripe
            print("blue")
            motorLeft.run(0) #stop
            motorRight.run(0)
            motorShoot.run_angle (1000, -720, Stop.COAST, True) #shoot
            motorLeft.run(500) #drive
            motorRight.run(500)
            time.sleep(0.2)
            break
        break
    
