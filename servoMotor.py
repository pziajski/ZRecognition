import pigpio
import time


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