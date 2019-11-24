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
        self.Reset()

    def TurnLeft(self):
        self.p.start(self.leftDir)
        time.sleep(3)
        self.p.stop()
        GPIO.cleanup()
    
    def TurnRight(self):
        self.p.start(self.rightDir)
        time.sleep(3)
        self.p.stop()
        GPIO.cleanup()

    def Reset(self):
        self.p.start(self.middDir)
        time.sleep(3)
        self.p.stop()
        GPIO.cleanup()

    def ChangeSpeed(self, dutyCycle):
        self.p.ChangeDutyCycle(dutyCycle)