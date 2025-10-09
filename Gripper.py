#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from time import sleep

# define conection
gripper = ev3.MediumMotor('outC')
ultra = ev3.UltrasonicSensor('in4')

# check connection
assert gripper.connected, "Connect a motor to port C"
assert ultra.connected, "Connect a ultrasonic sensor to port 4"

# function to open and close the gripper
def open_gripper():
    if ultra.value