import numpy as np
import random as rn
from PieceMovement import *
from CheckmateNerd import *

def AI_Template_DONT_USE(Pieces, Player):
    # Get all possible moves for AI
    AIMoves = []
    for j in range(8):
        for i in range(8):
            AIMoves = AIMoves + Legal_Moves([j,i], Pieces, Player)

    # Check Moves
    for n in range(-len(AIMoves)+1,1):
        move = AIMoves[n]
        OldX = move[3]; OldY = move[2]
        dump, Pinned = Is_Pinned([OldY, OldX], Pieces, Player)
        if Pinned:
            AIMoves.pop(n)
    AIMoves, Pieces = Check_Move_Narrower(AIMoves, Pieces, Player)

    ## BOT ALGORITHM TO CHOOSE MOVE GOES HERE ##
    ChoosenMove = stuff(AIMoves)

    # Apply move to board
    OldX = ChoosenMove[3]; OldY = ChoosenMove[2]
    NewX = ChoosenMove[1]; NewY = ChoosenMove[0]
    Pieces[NewY, NewX] = Pieces[OldY, OldX]
    Pieces[OldY, OldX] = 0

    # Finish
    return Pieces

def AI_Bob_Move(Pieces, Player):
    # Get all possible moves for AI
    AIMoves = []
    for j in range(8):
        for i in range(8):
            AIMoves = AIMoves + Legal_Moves([j,i], Pieces, Player)

    # Check Moves
    for n in range(-len(AIMoves)+1,1):
        move = AIMoves[n]
        OldX = move[3]; OldY = move[2]
        dump, Pinned = Is_Pinned([OldY, OldX], Pieces, Player)
        if Pinned:
            AIMoves.pop(n)
    AIMoves, Pieces = Check_Move_Narrower(AIMoves, Pieces, Player)

    # Bob Stuff (Choose random move, ELO = 125)
    ChoosenMove = rn.choice(AIMoves)

    # Apply move to board
    OldX = ChoosenMove[3]; OldY = ChoosenMove[2]
    NewX = ChoosenMove[1]; NewY = ChoosenMove[0]
    Pieces[NewY, NewX] = Pieces[OldY, OldX]
    Pieces[OldY, OldX] = 0

    # Finish
    return Pieces
