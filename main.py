from time import sleep

from robot_motor_controller import forward, stop


stop()
sleep(5)
forward()
sleep(5)
stop()
