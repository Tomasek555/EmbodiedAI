#!/usr/bin/env python3

import ev3dev.ev3 as ev3

from  time import sleep

import signal

btn = ev3.Button()

mA = ev3.LargeMotor('outC')
mB = ev3.LargeMotor('outB')

THRESHHOLD_LEFT = 30
THRESHHOLD_RIGHT = 30

BASE_SPEED = 30
TURN_SPEED = 80

TouchSensor = ev3.TouchSensor('in3')

assert TouchSensor.connected, "Connect a touch sensor to port 3"
assert mA.connected, "Connect a motor to port A"
assert mB.connected, "Connect a motor to port B"

mA.run_direct()
mB.run_direct()

while True:
    mA.duty_cycle_sp = BASE_SPEED
    mB.duty_cycle_sp = BASE_SPEED
    tou_val = TouchSensor.value()

    if tou_val:
        ev3.Sound.beep().wait()
        mA.duty_cycle_sp = 0
        mB.duty_cycle_sp = 0
        exit()
    else:
        print("Touch sensor value: ", tou_val)