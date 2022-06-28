import numpy as np
from Definitions import *

# Printable Array Stuff
blackBlock  = '  ' # 0.75
whiteBlock  = '██' # 1
hollowBlock = '[]' # 0
lightSquare = '- ' # 2
highlight1  = '==' # 3
highlight2  = '||' # 4

# Conversion Array Stuff
xWidth = 56
yWidth = 48
conversionArray = np.ones((yWidth, xWidth))*0.75

def Flip_Pieces(array):
        array = np.flipud(np.fliplr(array))
        return array

def Pieces_To_Printable(array):     # main graphics translator
    # Draw Checkerboard
    for j in range(0,8):
        for i in range(0,8):
            if (j+i)%2 == 0:
                for JJ in range(6*j, 6*(j+1)):
                    for II in range(7*i, 7*(i+1)):
                        conversionArray[JJ,II] = 2
            else:
                for JJ in range(6*j, 6*(j+1)):
                    for II in range(7*i, 7*(i+1)):
                        conversionArray[JJ,II] = 0.75

    # Draw Pieces
    for j in range(8):
        for i in range(8):
            num = array[j,i]
            toDraw = Piece(num)
            for JJ in range(6*j, 6*(j+1)):
                for II in range(7*i, 7*(i+1)):
                    new = toDraw[JJ-6*j, II-7*i]
                    if new == 1 or new == 0:
                        conversionArray[JJ,II] = toDraw[JJ-6*j, II-7*i]

    return conversionArray

def CMD_Print(conversionArray):     # graphics printer
    printableArray = blackBlock*xWidth
    # Graphical Builder
    for j in range(yWidth):
        for i in range(xWidth):
            try:
                if conversionArray[j,i] == 1:
                    printableArray = printableArray + whiteBlock
                elif conversionArray[j,i] == 0:
                    printableArray = printableArray + hollowBlock
                elif conversionArray[j,i] == 0.75:
                    printableArray = printableArray + blackBlock
                elif conversionArray[j,i] == 2:
                    printableArray = printableArray + lightSquare
                elif conversionArray[j,i] == 3:
                    printableArray = printableArray + highlight1
                elif conversionArray[j,i] == 4:
                    printableArray = printableArray + highlight2
            except:
                printableArray = printableArray + blackBlock
    # Out
    print(printableArray)

def Highlight_Square(coords_list, Pieces):       # highlighting graphics translator
    conversionArray = Pieces_To_Printable(Pieces)
    for n in range(len(coords_list)):
        coords = coords_list[n]
        X = coords[1]
        Y = coords[0]
        # conversionArray[Y*6, X*7:(X+1)*7] = 3
        # conversionArray[(Y+1)*6-1, X*7:(X+1)*7] = 3
        try:
            conversionArray[Y*6:(Y+1)*6, X*7] = 4
        except:
            continue
        try:
            conversionArray[Y*6:(Y+1)*6, (X+1)*7-1] = 4
        except:
            continue
    return conversionArray
