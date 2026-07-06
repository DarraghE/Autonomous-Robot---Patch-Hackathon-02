import sys

from robot_motor_controller import RobotWheels


COMMANDS = ("forward", "backward", "turn_left", "turn_right", "stop")


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "stop"
    seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 1

    if command not in COMMANDS:
        print("Use one of: {}".format(", ".join(COMMANDS)))
        return

    wheels = RobotWheels()
    if command == "stop":
        wheels.stop()
    else:
        wheels.run_for(command, seconds)


main()
