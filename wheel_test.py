import sys
from time import sleep

from robot_motor_controller import backward, forward, stop, turn_left, turn_right


COMMANDS = {
    "forward": forward,
    "backward": backward,
    "turn_left": turn_left,
    "turn_right": turn_right,
    "stop": stop,
}


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "stop"
    seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 1

    if command not in COMMANDS:
        stop()
        print("Use one of: {}".format(", ".join(COMMANDS)))
        return

    try:
        COMMANDS[command]()
        if command != "stop":
            sleep(seconds)
    finally:
        stop()


main()
