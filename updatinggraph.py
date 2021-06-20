import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.animation as animation
import random
import threading

def graphUpdate():
    global arrayNormal,ax1,arrayNormal2,ax2,fig
    arrayNormal = []
    style.use('fivethirtyeight')
    fig = plt.figure(figsize=(12,6))
    ax1 = fig.add_subplot(1,2,1)

    arrayNormal2 = []
    ax2 = fig.add_subplot(1,2,2)
    ani = animation.FuncAnimation(fig, animate, interval=100)
    plt.show()
    print("hello")


def animate(i):
    global arrayNormal,ax1,arrayNormal2,ax2,fig
    arrayNormal.append(random.randint(0,15))
    ax1.clear()
    ax1.plot(arrayNormal[-10:])

    arrayNormal2.append(random.randint(0,30))
    ax2.clear()
    ax2.plot(arrayNormal2[-10:])



graphUpdate()
