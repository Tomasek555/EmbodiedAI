#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from time import sleep

# Initialize motor on port C
motor = ev3.MediumMotor('outA')
touch = ev3.TouchSensor('in3')
assert motor.connected, "Connect a motor to port A"
assert touch.connected, "Connect a touch sensor to port 3"  
# Function to move motor to a target position
def move_motor(position):
    motor.position_sp = position
    motor.speed_sp = 200  # Speed in degrees per second
    motor.stop_action = 'brake'
    motor.run_to_abs_pos()
    motor.wait_while('running')
while True:
    # Start from position 0
    current_position = 0
    step = 1800  # degrees to move per button press

    btn = ev3.Button()

    print("Position is:", current_position)

    while True:
        if touch.value():
            new_position = current_position + step
            print("Moving forward to", new_position)
            move_motor(new_position)
            current_position = new_position
            print("New position is:", current_position)
            sleep(0.02)  # Debounce delay

        elif btn.down:
            print("Exiting...")
            motor.stop()
            break
    sleep(0.05)  # Small delay to avoid high CPU usage
