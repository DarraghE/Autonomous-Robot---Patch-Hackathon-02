import sys
from machine import Pin
from time import sleep


MOTOR_INPUTS = {
    "in1": 2,
    "in2": 11,
    "in3": 10,
    "in4": 8,
}


def all_off(pins):
    for pin in pins.values():
        pin.off()


def main():
    name = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 1

    pins = {
        input_name: Pin(gpio, Pin.OUT, value=0)
        for input_name, gpio in MOTOR_INPUTS.items()
    }

    if name not in MOTOR_INPUTS:
        all_off(pins)
        print("Use one of: {}".format(", ".join(MOTOR_INPUTS)))
        return

    try:
        print("{} high on GPIO{}".format(name.upper(), MOTOR_INPUTS[name]))
        pins[name].on()
        sleep(seconds)
    finally:
        all_off(pins)
        print("all inputs low")


main()
