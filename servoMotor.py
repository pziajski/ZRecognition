import pigpio
import time
# import RPi.GPIO as GPIO -- Raspberry Pi based library that acceses it's GPIOs


def servoMotor():
    pi = pigpio.pi()
    pi.set_mode(18, pigpio.OUTPUT)


    pi.set_PWM_frequency(17,50)

    time.sleep(1)

    print(pi.get_PWM_frequency(17))
    pi.set_PWM_frequency(17,32)

    time.sleep(1)

    pi.set_PWM_frequency(17,0)
    time.sleep(1)

    pi.stop()

#https://github.com/joan2937/pigpio/issues/67


# **** CODE BELOW WORKS FINE ON PI ****
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(12, GPIO.OUT)
# p = GPIO.PWM(12,50)
# p.start(7.5)
# try:
#     while True:
#         p.ChangeDutyCycle(7.5)
#         time.sleep(1)
#         p.ChangeDutyCycle(2.5)
#         time.sleep(1)
#         p.ChangeDutyCycle(12.5)
#         time.sleep(1)
# except KeyboardInterrupt:
#     p.stop()
#     GPIO.cleanup()
# https://rpi.science.uoit.ca/lab/servo/