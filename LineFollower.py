#!/usr/bin/env python3
import ev3dev.ev3 as ev3

from  time import sleep

import signal


MLeft = ev3.LargeMotor('outC') # Left motor
MRight = ev3.LargeMotor('outB') # Right motor

BASE_SPEED = -30

clRight = ev3.ColorSensor('in1')
clLeft = ev3.ColorSensor('in2')
TouchSensor = ev3.TouchSensor('in3')

assert MLeft.connected, "Connect a motor to port C"
assert MRight.connected, "Connect a motor to port B"
assert clRight.connected, "Connect a color sensor to port 1"
assert clLeft.connected, "Connect a color sensor to port 2"
assert TouchSensor.connected, "Connect a touch sensor to port 3"

MLeft.run_direct()
MRight.run_direct()

MLeft.duty_cycle_sp = BASE_SPEED
MRight.duty_cycle_sp = BASE_SPEED
tou_val = TouchSensor.value()

clRight.mode = 'COL-REFLECT'
clLeft.mode = 'COL-REFLECT'

P_GAIN = 2  # Proportional gain, adjust as necessary
I_GAIN = 0.1 # Integral gain, adjust as necessary
D_GAIN = 0.1 # Derivative gain, adjust as necessary

# PID variables
last_error = 0
integral = 0

# Loop timing
dt = 0.01  # 10ms loop time

while True:
    # Stop if touch sensor is pressed
    if TouchSensor.value():
        ev3.Sound.beep().wait()
        MLeft.stop(stop_action='brake')
        MRight.stop(stop_action='brake')
        break

    # Read sensor values
    left_val = clLeft.value()
    right_val = clRight.value()

    # Calculate error: the difference between left and right
    error = left_val - right_val  # or vice versa depending on behavior
    
    # Update integral
    integral += error * dt

    # Calculate derivative
    derivative = (error - last_error) / dt

    # Apply P controller
    correction = P_GAIN * error + I_GAIN*integral + D_GAIN * derivative

    # Calculate motor speeds
    left_speed = BASE_SPEED - correction
    right_speed = BASE_SPEED + correction

    # Limit speeds to range [-100, 100]
    left_speed = max(min(left_speed, 100), -100)
    right_speed = max(min(right_speed, 100), -100)

    # Apply speeds
    MLeft.run_direct()
    MRight.run_direct()
    MLeft.duty_cycle_sp = int(left_speed)
    MRight.duty_cycle_sp = int(right_speed)

    last_error = error
    sleep(0.01)  # Small delay to prevent excessive CPU usage