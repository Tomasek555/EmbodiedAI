#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from time import sleep

# define conection
mA = ev3.LargeMotor('outC')
motor = ev3.MediumMotor('outA')
mB = ev3.LargeMotor('outB')
ultra = ev3.UltrasonicSensor('in4')
TouchSensor = ev3.TouchSensor('in3')
def move_motor(position):
    motor.position_sp = position
    motor.speed_sp = 200  # Speed in degrees per second
    motor.stop_action = 'brake'
    motor.run_to_abs_pos()
    motor.wait_while('running')

# check connection
THRESHHOLD_LEFT = 30
THRESHHOLD_RIGHT = 30

BASE_SPEED = 30
TURN_SPEED = 80

assert TouchSensor.connected, "Connect a touch sensor to port 3"
assert mA.connected, "Connect a motor to port A"
assert mB.connected, "Connect a motor to port B"
assert ultra.connected, "Connect a ultrasonic sensor to port 4"

mA.run_direct()
mB.run_direct()

while True:
    # Start from position 0
    current_position = 0
    step = -1600  # degrees to move per button press

    btn = ev3.Button()

    print("Position is:", current_position)


    while True:
        ulta_val  = ultra.value()

        print(ulta_val)
        if current_position <= -1600:
            motor.stop
        elif ultra.value() < 100:
            mA.speed_sp = 0
            mB.speed_sp = 0
            new_position = current_position + step
            print("Moving forward to", new_position)
            move_motor(new_position)
            current_position = new_position
            print("New position is:", current_position)
            sleep(0.02)  # Debounce delay
        elif ulta_val <= 2550:
            mA.speed_sp = -BASE_SPEED
            mB.speed_sp = -BASE_SPEED
        

