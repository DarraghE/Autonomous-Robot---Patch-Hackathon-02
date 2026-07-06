from machine import Pin
from time import sleep


# These are ESP32-C6 GPIO numbers, not physical header-position numbers.
IN1_PIN = 2
IN2_PIN = 11
IN3_PIN = 10
IN4_PIN = 8


class WheelMotor:
    def __init__(self, forward_pin, backward_pin):
        self._forward = Pin(forward_pin, Pin.OUT, value=0)
        self._backward = Pin(backward_pin, Pin.OUT, value=0)
        self.stop()

    def forward(self):
        self._backward.off()
        self._forward.on()

    def backward(self):
        self._forward.off()
        self._backward.on()

    def stop(self):
        self._forward.off()
        self._backward.off()


class RobotWheels:
    """
    Wheel control for an ESP32-C6-DevKitC-1 running MicroPython.

    Pin mapping:
    - GPIO2 -> IN1
    - GPIO11 -> IN2
    - GPIO10 -> IN3
    - GPIO8 -> IN4
    """

    def __init__(self):
        self.left = WheelMotor(forward_pin=IN1_PIN, backward_pin=IN2_PIN)
        self.right = WheelMotor(forward_pin=IN3_PIN, backward_pin=IN4_PIN)
        self.stop()

    def forward(self):
        self.left.forward()
        self.right.forward()

    def backward(self):
        self.left.backward()
        self.right.backward()

    def turn_left(self):
        self.left.backward()
        self.right.forward()

    def turn_right(self):
        self.left.forward()
        self.right.backward()

    def stop(self):
        self.left.stop()
        self.right.stop()

    def run_for(self, command, seconds=1):
        try:
            getattr(self, command)()
            sleep(seconds)
        finally:
            self.stop()
