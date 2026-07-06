from __future__ import annotations

import argparse
import time
from dataclasses import dataclass

from gpiozero import OutputDevice


@dataclass(frozen=True)
class MotorPins:
    forward_pin: int
    backward_pin: int


class WheelMotor:
    def __init__(self, pins: MotorPins) -> None:
        self._forward = OutputDevice(pins.forward_pin, active_high=True, initial_value=False)
        self._backward = OutputDevice(pins.backward_pin, active_high=True, initial_value=False)

    def forward(self) -> None:
        self._backward.off()
        self._forward.on()

    def backward(self) -> None:
        self._forward.off()
        self._backward.on()

    def stop(self) -> None:
        self._forward.off()
        self._backward.off()

    def close(self) -> None:
        self.stop()
        self._forward.close()
        self._backward.close()


class RobotWheels:
    """
    Controls a two-wheel robot through an H-bridge style motor driver.

    Pin numbering uses Raspberry Pi BCM GPIO numbers.
    """

    def __init__(self) -> None:
        self.left = WheelMotor(MotorPins(forward_pin=2, backward_pin=11))  # IN1 / IN2
        self.right = WheelMotor(MotorPins(forward_pin=10, backward_pin=8))  # IN3 / IN4
        self.stop()

    def forward(self) -> None:
        self.left.forward()
        self.right.forward()

    def backward(self) -> None:
        self.left.backward()
        self.right.backward()

    def turn_left(self) -> None:
        self.left.backward()
        self.right.forward()

    def turn_right(self) -> None:
        self.left.forward()
        self.right.backward()

    def stop(self) -> None:
        self.left.stop()
        self.right.stop()

    def close(self) -> None:
        self.stop()
        self.left.close()
        self.right.close()

    def __enter__(self) -> "RobotWheels":
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()


def run_command(command: str, seconds: float) -> None:
    with RobotWheels() as wheels:
        action = getattr(wheels, command)
        action()
        time.sleep(seconds)
        wheels.stop()


def main() -> None:
    parser = argparse.ArgumentParser(description="Control the autonomous robot wheel motors.")
    parser.add_argument(
        "command",
        choices=["forward", "backward", "turn_left", "turn_right", "stop"],
        help="Wheel command to run.",
    )
    parser.add_argument(
        "--seconds",
        type=float,
        default=1.0,
        help="How long to run the command before stopping. Defaults to 1 second.",
    )
    args = parser.parse_args()

    if args.command == "stop":
        with RobotWheels() as wheels:
            wheels.stop()
        return

    run_command(args.command, args.seconds)


if __name__ == "__main__":
    main()
