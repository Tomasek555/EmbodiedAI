#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from time import sleep


# 43 white plane 7 for the black line


# Motors and Sensors
MLeft = ev3.LargeMotor('outC')
MRight = ev3.LargeMotor('outB')
clRight = ev3.ColorSensor('in1')
clLeft = ev3.ColorSensor('in2')
TouchSensor = ev3.TouchSensor('in3')
buttons = ev3.Button()  # Brick buttons


# Hardware check
assert MLeft.connected, "Connect a motor to port C"
assert MRight.connected, "Connect a motor to port B"
assert clRight.connected, "Connect a color sensor to port 1"
assert clLeft.connected, "Connect a color sensor to port 2"
assert TouchSensor.connected, "Connect a touch sensor to port 3"

# Base settings
BASE_SPEED = -30
MLeft.run_direct()
MRight.run_direct()
MLeft.duty_cycle_sp = BASE_SPEED
MRight.duty_cycle_sp = BASE_SPEED

clRight.mode = 'COL-REFLECT'
clLeft.mode = 'COL-REFLECT'

# PID gains
P_GAIN = 2.0
I_GAIN = 0.1
D_GAIN = 0.1

# Gain selection state
gain_names = ['P', 'I', 'D']
gain_index = 0  # Start with P selected

# PID control variables
last_error = 0
integral = 0
dt = 0.01  # 10 ms loop

# Button state for edge detection
last_up = False
last_left = False
last_right = False

# EV3 screen reference
lcd = ev3.Screen()

def show_gain():
    lcd.clear()
    # Display gain name and value on screen
    if gain_names[gain_index] == 'P':
        val = P_GAIN
    elif gain_names[gain_index] == 'I':
        val = I_GAIN
    else:
        val = D_GAIN
    lcd.draw.text((10, 20), "Gain: {}".format(gain_names[gain_index]))
    lcd.draw.text((10, 50), "{:.2f}".format(val))
    lcd.update()

# Show initial gain on screen
show_gain()

while True:
    # Exit condition
    if TouchSensor.value():
        ev3.Sound.beep().wait()
        MLeft.stop(stop_action='brake')
        MRight.stop(stop_action='brake')
        break

    # --- Button Handling ---

    # Detect rising edge for UP (cycle gain selection)
    if buttons.up and not last_up:
        gain_index = (gain_index + 1) % 3
        show_gain()

    # Detect left press (decrease current gain)
    if buttons.left and not last_left:
        if gain_names[gain_index] == 'P':
            P_GAIN = max(0, P_GAIN - 0.25)
        elif gain_names[gain_index] == 'I':
            I_GAIN = max(0, I_GAIN - 0.05)
        elif gain_names[gain_index] == 'D':
            D_GAIN = max(0, D_GAIN - 0.05)
        show_gain()

    # Detect right press (increase current gain)
    if buttons.right and not last_right:
        if gain_names[gain_index] == 'P':
            P_GAIN += 0.25
        elif gain_names[gain_index] == 'I':
            I_GAIN += 0.05
        elif gain_names[gain_index] == 'D':
            D_GAIN += 0.05
        show_gain()

    # Update button state
    last_up = buttons.up
    last_left = buttons.left
    last_right = buttons.right

    # --- PID Line Following ---

    left_val = clLeft.value()
    right_val = clRight.value()
    error = left_val - right_val

    integral += error * dt
    derivative = (error - last_error) / dt

    correction = P_GAIN * error + I_GAIN * integral + D_GAIN * derivative

    left_speed = BASE_SPEED - correction
    right_speed = BASE_SPEED + correction

    left_speed = max(min(left_speed, 100), -100)
    right_speed = max(min(right_speed, 100), -100)

    MLeft.duty_cycle_sp = int(left_speed)
    MRight.duty_cycle_sp = int(right_speed)

    last_error = error
    sleep(dt)
