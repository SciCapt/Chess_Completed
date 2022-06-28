import time
import mouse
import keyboard
import numpy as np

def Get_Mouse_Pos():
    while True:
        mouse.wait(button='right')
        if mouse.is_pressed(button='right'):
            return mouse.get_position()
            break

def Select_Square():
    pos = Get_Mouse_Pos()
    for x in range(8):
        if pos[0] > 14+(111*x) and pos[0] < 125+(111*x):
            posX = x
            break
    for y in range(8):
        if pos[1] > 38+(97*y) and pos[1] < 135+(97*y):
            posY = y
            break
    selection = [y,x]
    return selection
