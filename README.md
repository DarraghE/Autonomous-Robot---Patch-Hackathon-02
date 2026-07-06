# Autonomous Robot - Patch Hackathon 02

MicroPython control code for a two-wheel autonomous robot using an ESP32-C6-DevKitC-1 and a GPIO-connected motor driver.

## Motor driver pins

The code uses ESP32-C6 GPIO numbers, not physical header-position numbers or board-edge position labels:

| ESP32-C6 GPIO | Motor driver input |
| --- | --- |
| GPIO2 | IN1 |
| GPIO11 | IN2 |
| GPIO10 | IN3 |
| GPIO8 | IN4 |

Forward sets IN1 / GPIO2 and IN3 / GPIO10 high, while keeping IN2 / GPIO11 and IN4 / GPIO8 low.

Note: on the ESP32-C6-DevKitC-1, GPIO8 is also associated with the boot/ROM function on the board pinout. The code supports it because it is wired to IN4 here, but if the board has trouble booting while the motor driver is connected, move IN4 to a safer free GPIO and update `IN4_PIN`.

## Setup

Install the host upload tool:

```bash
python -m pip install -r requirements.txt
```

The ESP32-C6 should be running MicroPython firmware before uploading these files.

## Upload to the ESP32-C6

With the board connected over USB:

```bash
mpremote connect auto fs cp robot_motor_controller.py :robot_motor_controller.py
mpremote connect auto fs cp main.py :main.py
```

`main.py` drives both motors forward continuously until the ESP32-C6 is reset or powered off.

Keep the robot lifted or blocked safely before plugging it in. Once this boot script is installed, plugging in or resetting the ESP32-C6 will start continuous forward movement.

## Test commands

Each command runs briefly and then stops the wheels. Upload `robot_motor_controller.py` first, then run:

```bash
mpremote connect auto run wheel_test.py forward 1
mpremote connect auto run wheel_test.py backward 1
mpremote connect auto run wheel_test.py turn_left 1
mpremote connect auto run wheel_test.py turn_right 1
mpremote connect auto run wheel_test.py stop
```

The motors are stopped automatically when the script exits.
