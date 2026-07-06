from machine import Pin


IN1 = Pin(2, Pin.OUT, value=0)
IN2 = Pin(11, Pin.OUT, value=0)
IN3 = Pin(10, Pin.OUT, value=0)
IN4 = Pin(8, Pin.OUT, value=0)


def stop():
    IN1.off()
    IN2.off()
    IN3.off()
    IN4.off()


def forward():
    IN2.off()
    IN4.off()
    IN1.on()
    IN3.on()


def backward():
    IN1.off()
    IN3.off()
    IN2.on()
    IN4.on()


def turn_left():
    IN1.off()
    IN4.off()
    IN2.on()
    IN3.on()


def turn_right():
    IN2.off()
    IN3.off()
    IN1.on()
    IN4.on()
