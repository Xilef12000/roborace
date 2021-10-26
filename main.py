#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from simple_pid import PID

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

left_motor = Motor(Port.D , Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
line_sensor = ColorSensor(Port.S3)
steer_motor = Motor(Port.C)
distance_sensor = UltrasonicSensor(Port.S2)

WHEEL_DIAMETER=50
AXLE_TRACK=100

robot = DriveBase(left_motor, right_motor, WHEEL_DIAMETER, AXLE_TRACK)

wall_distance = 200

pid = PID(0.85, 0.0015 , 0, setpoint=1)
#Alte pid werte: pid = PID(1, 0.0004, 0, setpoint=1)
#Mittelalte werte sind: PID(0.85, 0.0015 , 0, setpoint=1)
# der beste d-wert war 4 ist aber schlechter als 0 bisher!
pid.sample_time = 0.01
pid.output_limits = (-40, 40) 

# Write your program here.                                                                
# ev3.speaker.say('Starting') 

grey = line_sensor.reflection()                                                            
pid.setpoint = grey                        

robot.drive(900,0)   
                
while True:
    current = line_sensor.reflection()
    if distance_sensor.distance() < 300:
      pid.tunings = (1, 0.0004, 0,)
      pid.setpoint = wall_distance
      #ev3.speaker.say('distance sensor')
      while True:
        current = distance_sensor.distance()
        turn_degree = -1 * pid(current)
        steer_motor.track_target(turn_degree)
        if distance_sensor.distance() > 300:
          pid.setpoint = grey
          #ev3.speaker.say('line sensor')
          current = line_sensor.reflection()
          pid.tunings = (1, 0.0004, 0,) 
          break

    turn_degree = 2 * pid(current)
    if turn_degree > 42:
      turn_degree = 42
    if turn_degree < -42:
      turn_degree = -42
    steer_motor.track_target(turn_degree)

