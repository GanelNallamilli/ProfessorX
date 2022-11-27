import RPi.GPIO as GPIO
import time

'''Scripted used to test if the ultrasonic sensor works'''

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIG1 = 4
ECHO1 = 17

TRIG2 = 29
ECHO2 = 31

GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)

GPIO.output(TRIG1, True)
time.sleep(0.0001)
GPIO.output(TRIG1, False)

while GPIO.input(ECHO1) == False:
    start_time = time.time()
    
while GPIO.input(ECHO1) == True:
    end_time = time.time()
 
sig_time = start_time-end_time

distance = sig_time / 0.000058
print(start_time)
print(end_time)
print(sig_time)
print(distance)

GPIO.cleanup()
