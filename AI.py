import numpy as np
import random as rn
from PieceMovement import *
from CheckmateNerd import *

## AI Base Functions ##
def AI_Possible_Moves(Pieces, Player):
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
    return AIMoves, Pieces

def AI_Make_Move(Pieces, Player, ChosenMove):
    # Cords
    OldX = ChosenMove[3]; OldY = ChosenMove[2]
    NewX = ChosenMove[1]; NewY = ChosenMove[0]
    try:
        IsCastling = ChosenMove[4]
    except:
        IsCastling = False
    if IsCastling:
        # Apply castling move to board
        King = Pieces[NewY, NewX]
        Rook = Pieces[OldY, OldX]
        kingy = ChosenMove[5]
        kingx = ChosenMove[6]
        rooky = ChosenMove[7]
        rookx = ChosenMove[8]
        Pieces[kingy, kingx] = King
        Pieces[rooky, rookx] = Rook
        Pieces[OldY, OldX] = 0
        Pieces[NewY, NewX] = 0
        return Pieces
    elif not IsCastling:
        # Apply move to board
        Pieces[NewY, NewX] = Pieces[OldY, OldX]
        Pieces[OldY, OldX] = 0

    # Check for Pawn Promotion
    if NewY == 0:
        if Pieces[NewY, NewX] == 1.1 and Player == "W":
            Pieces[NewY, NewX] = rn.choice([5.1,5.1,5.1,4.1,3.1,2.1])
        elif Pieces[NewY, NewX] == 1.2 and Player == "B":
            Pieces[NewY, NewX] = rn.choice([5.2,5.2,5.2,4.2,3.2,2.2])
    return Pieces


## AI Personalities ##
def AI_TEMPLATE(Pieces, Player):
    # Get all possible moves for AI
    AIMoves, Pieces = AI_Possible_Moves(Pieces, Player)

    # AI ALGORITHM GOES HERE
    ChosenMove = stuff(AIMoves)

    # Finish
    Pieces = AI_Make_Move(Pieces, Player, ChosenMove)
    return Pieces

def AI_Bob_Move(Pieces, Player):
    # Get all possible moves for AI
    AIMoves, Pieces = AI_Possible_Moves(Pieces, Player)

    # Bob Stuff (Choose random move, ELO = 125)
    ChosenMove = rn.choice(AIMoves)

    # Finish
    Pieces = AI_Make_Move(Pieces, Player, ChosenMove)
    return Pieces
