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
speedOffset = 0.0 #corecting of the gyro values
turnSpeed = 100 #speed when turning at shooting area
target = 42
target = colorSensor.reflection()
targetCorrector = 1
speed = 500 #roboter driving speed maximum 700 (900 is the absolute maximunm)
speedCorrectorBlack = 1.2 # 1.1 to 1.5
speedCorrectorWhite = 1.3 # 1.2 to 1.7

ev3.speaker.beep()
gyroSensor.reset_angle(0)
time.sleep(0.5)
while not touchSensor.pressed():
  #wait(10)
  pass
target = colorSensor.reflection()
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
  distance = ultrasonicSensor.distance(silent=False)
  color = colorSensor.reflection()
  #angleAverage.append(gyroSensor.speed())
  #if len(angleAverage) >= 1000:
  #  print(sum(angleAverage)/len(angleAverage))

  #print(color)
  if (color < 90):
  #if (color < 90 and distance < 300):
    print("grayscale")
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
      #angle = gyroSensor.angle()
      AngleSpeed = gyroSensor.speed() - speedOffset
      timeOld = timeNow
      timeNow = time.time()
      timeDelta = timeNow - timeOld
      angleDelta = AngleSpeed * timeDelta
      angle += angleDelta
      #print(angle)
      if angle < angleTarget - angleTargetAccuracy:
        print("turning")
        motorLeft.run(turnSpeed)
        motorRight.run(-turnSpeed)
      elif angle > angleTarget + angleTargetAccuracy:
        print("turning")
        motorLeft.run(-turnSpeed)
        motorRight.run(turnSpeed)
      else:
        while(True):
          rgb = colorSensor.rgb()
          if(not(rgb[0] < 30 and rgb[1] < 40 and rgb[2] > 50)):
            print("forward")
            motorLeft.run(turnSpeed)
            motorRight.run(turnSpeed)
            #print(rgb)
          else: 
            print("blue")
            motorLeft.run(0)
            motorRight.run(0)
            motorShoot.run_angle (1000, -720, Stop.COAST, True)
            motorLeft.run(500)
            motorRight.run(500)
            time.sleep(0.2)
            break
        break
    
