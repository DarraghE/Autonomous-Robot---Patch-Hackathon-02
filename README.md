# Autonomous Robot - Patch Hackathon 02

MicroPython control code for a two-wheel autonomous robot using an ESP32-C6-DevKitC-1 and a GPIO-connected motor driver.

## Motor driver pins

The code uses ESP32-C6 GPIO numbers:

| ESP32-C6 GPIO | Motor driver input |
| --- | --- |
| GPIO2 | IN1 |
| GPIO11 | IN2 |
| GPIO10 | IN3 |
| GPIO8 | IN4 |

Current wheel assumption:

- Left wheel: IN1 / IN2
- Right wheel: IN3 / IN4

The board header position numbered `1` on the supplied ESP32-C6-DevKitC-1 pinout corresponds to `GPIO2`.

If either wheel spins the wrong direction during testing, swap that wheel's `forward_pin` and `backward_pin` values in `robot_motor_controller.py`.

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

`main.py` waits 2 seconds after boot, then drives both wheels forward until the board is reset or powered off.

Keep the robot lifted or blocked safely before plugging it in. Once this boot script is installed, plugging in the ESP32-C6 will start the wheels automatically.

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

## Pin diagnostic

To verify wiring one motor-driver input at a time:

```bash
mpremote connect auto run pin_diagnostic.py in1 1
mpremote connect auto run pin_diagnostic.py in2 1
mpremote connect auto run pin_diagnostic.py in3 1
mpremote connect auto run pin_diagnostic.py in4 1
```

If the driver inputs toggle but the motors do not move, check that the motor driver has motor power, ESP32 ground and driver ground are connected together, and any enable pins or jumpers on the motor driver are enabled.
