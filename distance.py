import RPi.GPIO as GPIO
import time
def getDistance():
    GPIO.setmode(GPIO.BCM)
    TRIG = 4
    ECHO = 18

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == False:
        start = time.time()

    while GPIO.input(ECHO) == True:
        end = time.time()

    sig_time = end-start

    #CM:
    distance = sig_time / 0.000058
    GPIO.cleanup()
    #inches:
    #distance = sig_time / 0.000148
    return distance



