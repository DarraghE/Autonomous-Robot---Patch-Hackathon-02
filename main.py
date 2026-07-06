from time import sleep

from robot_motor_controller import RobotWheels


BOOT_DELAY_SECONDS = 2

wheels = RobotWheels()
sleep(BOOT_DELAY_SECONDS)
wheels.forward()
