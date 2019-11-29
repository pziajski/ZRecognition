import pigpio
import time
import RPi.GPIO as GPIO #Raspberry Pi based library that acceses it's GPIOs

class MotorControl():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(12, GPIO.OUT)
        self.p = GPIO.PWM(12,50) #pin, frequency

    def Turn(self):
        sleepTimer = 0.15
        self.p.start(7)
        time.sleep(sleepTimer)
        self.p.ChangeDutyCycle(8)
        time.sleep(sleepTimer)
        self.p.ChangeDutyCycle(9)
        time.sleep(sleepTimer)
        self.p.ChangeDutyCycle(10.5)
        time.sleep(sleepTimer)
        self.p.ChangeDutyCycle(11.5)
        time.sleep(sleepTimer)
        self.p.ChangeDutyCycle(0)
        time.sleep(2)
        self.p.ChangeDutyCycle(10.5)
        time.sleep(sleepTimer)
        self.p.ChangeDutyCycle(9)
        time.sleep(sleepTimer)
        self.p.ChangeDutyCycle(8)
        time.sleep(sleepTimer)
        self.p.ChangeDutyCycle(7)
        time.sleep(sleepTimer)
        self.p.ChangeDutyCycle(0)