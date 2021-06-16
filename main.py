import argparse
import math
import collections 
from matplotlib import pyplot as plt 
import pandas as pd
from datetime import datetime
import os
import time
import sys
import socket

from pythonosc import dispatcher
from pythonosc import osc_server


def stoppingTime():
    print("STARTED COUNT DOWN")
    time.sleep(30)
    os._exit(0)

#method called by dispatcher to receive eeg data.
def data(none: float,accForBack: float,accLeftRight: float,accZ: float):
    text = ""
    leftRightBool = (accLeftRight < 0.2) and (accLeftRight> -0.2)
    forBackBool = (accForBack < 0.2) and (accForBack > -0.2)
    if((forBackBool==True) and (leftRightBool==True)):
        text = "none"
    elif((accForBack > 0.3) and (leftRightBool==True)):
        text = "forward"
    elif((accForBack < -0.3) and (leftRightBool==True)):
        text = "back"
    elif((accLeftRight)>0.3 and (forBackBool==True)):
        text = "right"
    elif((accLeftRight)<-0.3 and (forBackBool==True)):
        text = "left"

    if(accZ > 1.5):
        text = "Stop/start"

    print(text)




#initalises the the port and ip to start receiving osc data packets.
if __name__ == "__main__":
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
        default=local_ip, help="The ip to listen on")
    parser.add_argument("--port",
        type=int, default=5000, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/muse/acc",data)

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
