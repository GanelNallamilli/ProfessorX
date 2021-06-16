import sys
import time
import RPi.GPIO as GPIO

ForwardLeft=26
BackwardLeft=20
ForwardRight=19
BackwardRight=16

def run():
    global ForwardLeft,BackwardLeft,ForwardRight,BackwardRight
    mode=GPIO.getmode()

    GPIO.cleanup()

    ForwardLeft=26
    BackwardLeft=20
    ForwardRight=19
    BackwardRight=16
    sleeptime=1
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ForwardLeft, GPIO.OUT)
    GPIO.setup(BackwardLeft, GPIO.OUT)
    GPIO.setup(ForwardRight, GPIO.OUT)
    GPIO.setup(BackwardRight, GPIO.OUT)

def forward(x):
    global ForwardLeft,BackwardLeft,ForwardRight,BackwardRight
    GPIO.output(ForwardRight, GPIO.HIGH)
    GPIO.output(ForwardLeft, GPIO.HIGH)
    print("Moving Forward")
    time.sleep(x)
    GPIO.output(ForwardRight, GPIO.LOW)
    GPIO.output(ForwardLeft, GPIO.LOW)

def reverse(x):
    global ForwardLeft,BackwardLeft,ForwardRight,BackwardRight
    GPIO.output(BackwardLeft, GPIO.HIGH)
    GPIO.output(BackwardRight, GPIO.HIGH)
    print("Moving Backward")
    time.sleep(x)
    GPIO.output(BackwardLeft, GPIO.LOW)
    GPIO.output(BackwardRight, GPIO.LOW)

def left(x):
    global ForwardLeft,BackwardLeft,ForwardRight,BackwardRight
    GPIO.output(ForwardRight, GPIO.HIGH)
    print("Turning Left")
    time.sleep(x)
    GPIO.output(ForwardRight, GPIO.LOW)

def right(x):
    global ForwardLeft,BackwardLeft,ForwardRight,BackwardRight
    GPIO.output(ForwardLeft, GPIO.HIGH)
    print("Turning right")
    time.sleep(x)
    GPIO.output(ForwardLeft, GPIO.LOW)
