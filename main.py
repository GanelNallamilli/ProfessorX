import argparse
import math
import collections 
from matplotlib import pyplot as plt 
import pandas as pd
import os
import time
import sys
from datetime import datetime
import pandas as pd
from scipy.fftpack import rfft,rfftfreq 
import numpy as np
import socket
import movement as m
import sys
import time
import RPi.GPIO as GPIO

from pythonosc import dispatcher
from pythonosc import osc_server

eegTP9Array = []
eegAF7Array = []
eegAF8Array = []
eegTP10Array = []
timeArray = []
boolean = True

forward_Back = False
turn_drive_toggle = False
limitDrive = False
left_right_toggle = True
limiter = False


sample = 256

def stoppingTime():
    print("STARTED COUNT DOWN")
    print("Current state: RIGHT")
    print("Blink to change rotation")
    print("Tilt head forward to go forward")
    print("Tilt head bakcward to go backwards")
    m.run()
    time.sleep(90)
    GPIO.cleanup()
    os._exit(0)

def dataGyro(none: float,accForBack: float,accLeftRight: float,accZ: float):
    global turn_drive_toggle,left_right_toggle,limitDrive,forward_Back
    if((accForBack > 0.5)):
        turn_drive_toggle = True
        if(forward_Back == False or limitDrive == True):
            forward_Back = True
            limitDrive = False
            limiter = True
            print("Forward")
    if((accForBack < -0.5)):
        turn_drive_toggle = True
        if(forward_Back == True or limitDrive == True):
            forward_Back = False
            limitDrive = False
            limiter = True
            print("Backward")

#method called by dispatcher to receive eeg data.
def data(eeg1: float,eeg2: float,eeg3: float,eeg4: float,eeg5: float,eeg6: float):
    global boolean
    plotData(eeg2,eeg3,eeg4,eeg6)
    if(boolean == True):
        boolean = False
        stoppingTime()

#writes 550 frames of eeg to a .csv file.
def plotData(eegTP9,eegAF7,eegAF8,eegTP10):
    global turn_drive_toggle,left_right_toggle,limitDrive,forward_Back,limiter
    global eegTP9Array,eegAF7Array,timeArray,eegAF8Array,eegTP10Array,filename,count
    limiter = False
    eegTP9Array.append(str(eegTP9))
    eegAF7Array.append(str(eegAF7))
    eegAF8Array.append(str(eegAF8))
    eegTP10Array.append(str(eegTP10))
    timeArray.append(str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]))
    if((len(eegTP9Array) or len(eegAF7Array) or len(eegAF8Array) or len(eegTP10Array)) == sample):
        npArray = []
        startTime = 0 #Variable to start the start time in seconds.
        npArray = np.array(timeArray[:sample]) # converts the timeColumn data from to a numpy array.
        
        #loops through the unformatted time array, and replaces each element with its relative time from the start time.
        for i in range (0,len(npArray)):
            #tempArray stores the components of time, by splitting the formatted time.
            #We start with "2021-02-17 15:36:15.614" then we get the last 12 characters which gives "15:36:15.614".
            #We then split "15:36:15.614" by the colon to work with the hours,minutes and seconds separetly.
            #Therefore the tempArray will store ["15","36","15.614"] for each element in the unformated time array (npArray) in example.
            tempArray = npArray[i][-12:].split(":")

            #if i is 0, then we know we are working with the first recorded time. So we have to work out the start time in seconds, and
            # we want to set the first element of the unformatted npArray to be 0, since the start time is time 0.
            if(i ==0):
                #works out the start time in seconds by multiplying the hours and minutes by 60^2 and 60 respectively
                #then will add all the time components up, essentially turning a time like 16:01:01.002 to 57661.002 seconds.
                #This means that aslong as our data does not cross over the 24 hour mark then the alorigthm will work.
                startTime = float(tempArray[0])*(60**2) + float(tempArray[1])*60 +float(tempArray[2])
                npArray[i] = 0 #sets first element to 0.
            else:
                #if we are not working with the start time, then it translates ordinary 24 hour time into seconds like 'startTime' before.
                totalTime = float(tempArray[0])*(60**2) + float(tempArray[1])*60 +float(tempArray[2])
                #We then update the unformatted element with the relative time, slowly formatting each element as the loop tends to len(npArray)
                npArray[i] = totalTime - startTime
        
        total = 0
        count = 0
        average = 0
        
        yf = rfft(eegAF7Array[:sample])
        xf = rfftfreq(len(npArray[:sample]),1/sample)
        absYF = np.abs(yf)
        power_spectrum = np.square(absYF)

        for j in range(0,len(xf)):
            if(float(xf[j]) > 48 and 52> float(xf[j])):
                power_spectrum[j] = 0
            elif (xf[j]< 5 or xf[j]>= 50) :
                power_spectrum[j] = 0
        arrayPower = findMaximumFreq(power_spectrum,xf)
        average = (arrayPower[0]+arrayPower[1]+arrayPower[2])/3

        high1000 = False
        low9000 = False
        errorVal = False
        indexRemember = -1
        count = 0
        tempEegAF7= eegAF7Array
        for i in range(0,len(eegAF7Array)):
            if(float(eegAF7Array[i]) > 1050.0):
                high1000  = True
                indexRemember = i
                break
        if(high1000 == True):
            for i in range(indexRemember,len(eegAF7Array)):
                if(float(eegAF7Array[i]) < 700.0):
                    low9000  = True
                    break
        

        if(high1000 == True and low9000 == True and limiter == False):
            turn_drive_toggle = False
            limitDrive = True
            if(left_right_toggle == True):
                left_right_toggle = False
            elif(left_right_toggle == False):
                left_right_toggle = True

            if(left_right_toggle == False):
                print("Left")
            elif(left_right_toggle == True):
                print("Right")
        
        for i in range(0, len(eegAF7Array)):
            if((float(eegAF7Array[i])>820.0 and float(eegAF7Array[i])>870.0 ) or (float(eegAF7Array[i])<750.0  and float(eegAF7Array[i])>780.0 )):
                count = count + 1
        
        if(average >= 25):

            if(turn_drive_toggle == False):
                if(left_right_toggle == False):
                    m.left(1)
                elif(left_right_toggle == True):
                    m.right(1)
            elif(turn_drive_toggle == True):
                if(forward_Back == True):
                    m.forward(1)
                elif(forward_Back == False):
                    m.reverse(1)

        
        eegTP9Array = []
        eegAF7Array = []
        eegAF8Array = []
        eegTP10Array = []
        timeArray = []
        for i in range (int(sample/2),len(eegAF7Array)):
            eegAF7Array[i-int(sample/2)] = tempEegAF7[i]
        
def findMaximumFreq(power_spectrum,xf):
    top80Array = []
    count = 0
    sortedPower_Spectrum = -np.sort(-power_spectrum)
    for i in range(0,len(sortedPower_Spectrum)):
        if (count == 3):
            break
        for j in range(0,len(power_spectrum)):
            if((power_spectrum[j] == sortedPower_Spectrum[i])):
                if(isInArray(xf[j],top80Array)):
                    top80Array.append(xf[j])
                    count += 1
                    break
    return top80Array

def isInArray(value,array):
        for i in range(0,len(array)):
            if(float(value) == float(array[i])):
                return False
        return True

#initalises the the port and ip to start receiving osc data packets.
if __name__ == "__main__":
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print("local_ip")
    time.sleep(1)
    print("Staring now!")
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
        default=local_ip, help="The ip to listen on")
    parser.add_argument("--port",
        type=int, default=5000, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/muse/acc",dataGyro)
    dispatcher.map("/muse/eeg",data)

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

