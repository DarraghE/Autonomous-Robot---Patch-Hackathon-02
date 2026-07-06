# Autonomous Robot - Patch Hackathon 02

Python control code for a two-wheel autonomous robot using a GPIO-connected motor driver.

## Motor driver pins

The code uses Raspberry Pi BCM GPIO numbering:

| Raspberry Pi GPIO | Motor driver input |
| --- | --- |
| GPIO2 | IN1 |
| GPIO11 | IN2 |
| GPIO10 | IN3 |
| GPIO8 | IN4 |

Current wheel assumption:

- Left wheel: IN1 / IN2
- Right wheel: IN3 / IN4

If either wheel spins the wrong direction during testing, swap that wheel's `forward_pin` and `backward_pin` values in `robot_motor_controller.py`.

## Setup

Install dependencies on the Raspberry Pi:

```bash
python -m pip install -r requirements.txt
```

## Test commands

Each command runs briefly and then stops the wheels:

```bash
python robot_motor_controller.py forward --seconds 1
python robot_motor_controller.py backward --seconds 1
python robot_motor_controller.py turn_left --seconds 1
python robot_motor_controller.py turn_right --seconds 1
python robot_motor_controller.py stop
```

The motors are stopped automatically when the script exits.
