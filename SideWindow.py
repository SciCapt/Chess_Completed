import pygetwindow as wn
from Printer import *
from os import system
import random as rn
import numpy as np
from AI import *
import time

# Set CMD Window to Particular Size and Position
system("title " + 'Position')
time.sleep(.05) # small time delay to allow title to update
GameWindow = wn.getWindowsWithTitle('Position')[0]
GameWindow.resizeTo(55, 830)
GameWindow.moveTo(915, 0)

# Printer data
pix1 = '||'
pix2 = '██'
posBar = 24*pix1 + 24*pix2

# Running loop
time.sleep(1)
MainPlayer = np.load("Player.npy")
while True:
    # Get current board data
    try:
        Pieces = np.load("Board.npy", allow_pickle=True)
    except:
        pass

    # Update position bar
    posVal = SF_Position(Pieces)[0]
    # posVal = (rn.random() - 0.5)*48

    # Relative pix count from posVal
    posVal = int(posVal)
    if abs(posVal) > 24:
        if posVal < 0:
            posVal = -24
        elif posVal > 0:
            posVal = 24
        # posVal ranges from -24 to 24

    # Build position bar
    if MainPlayer == "W":
        posBar = pix1*(24-posVal) + pix2*(24+posVal)
        print(posBar)

    elif MainPlayer == "B":
        posBar = pix2*(24+posVal) + pix1*(24-posVal)
        print(posBar)

    # Refresh Rate (in seconds)
    time.sleep(1/2)
