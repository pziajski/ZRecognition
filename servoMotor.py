import pigpio
import time
import RPi.GPIO as GPIO #Raspberry Pi based library that acceses it's GPIOs

class MotorControl():
    rightDir = 5
    middDir = 7.5
    leftDir = 10

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(12, GPIO.OUT)
        self.p = GPIO.PWM(12,50) #pin, frequency

    def Turn(self):
        self.p.start(2.5)
        time.sleep(0.5)
        self.p.ChangeDutyCycle(5)
        time.sleep(0.5)
        self.p.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        self.p.ChangeDutyCycle(10)
        time.sleep(0.5)
        self.p.ChangeDutyCycle(12.5)
        time.sleep(0.5)
        self.p.ChangeDutyCycle(10)
        time.sleep(0.5)
        self.p.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        self.p.ChangeDutyCycle(5)
        time.sleep(0.5)
        self.p.ChangeDutyCycle(2.5)
        time.sleep(0.5)
        GPIO.cleanup()