import pigpio
import time
import RPi.GPIO as GPIO #Raspberry Pi based library that acceses it's GPIOs

class MotorControl():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(12, GPIO.OUT)
        self.p = GPIO.PWM(12,50) #pin, frequency

    def Start(self):
        self.p.start(7.5)
    
    def Stop(self):
        self.p.stop()
        GPIO.cleanup()

    def ChangeSpeed(self, dutyCycle):
        self.p.ChangeDutyCycle(dutyCycle)