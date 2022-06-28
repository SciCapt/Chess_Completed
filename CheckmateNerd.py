import numpy as np
from PieceMovement import *
from Printer import *

def Flip_Moves(Moves): # translate one player's legal moves to the other player's perspective
    for n in range(len(Moves)):
        for nn in range(4):
            num = Moves[n][nn]
            if num == 0:
                num = 7
            elif num == 1:
                num = 6
            elif num == 2:
                num = 5
            elif num == 3:
                num = 4
            elif num == 4:
                num = 3
            elif num == 5:
                num = 2
            elif num == 6:
                num = 1
            elif num == 7:
                num = 0
            Moves[n][nn] = num
    return Moves

def In_Check(Pieces, Player):
    # Get legal moves of other player
    if Player == "W":
        Player = "B"
        king = 6.1
    elif Player == "B":
        Player = "W"
        king = 6.2
    allLegalMoves = []
    for j in range(8):
        for i in range(8):
            allLegalMoves = allLegalMoves + Legal_Moves([j,i], Flip_Pieces(Pieces), Player)
            if Pieces[j,i] == king:
                kingX = i
                kingY = j

    # Flip Moves=
    allLegalMoves = Flip_Moves(allLegalMoves)

    # Check if current player's king can get stomped on
    for n in range(len(allLegalMoves)):
        NewX = allLegalMoves[n][1]
        NewY = allLegalMoves[n][0]
        try:
            if kingX == NewX and kingY == NewY:
                return True
        except UnboundLocalError:
            if n <= 0:
                a = 1
                # print("my dude where is your king????")
                ## This goes off more than it should             ##
                ## just figured thats worth noting to future me  ##
    return False

def Check_Move_Narrower(AllowedMoves, Pieces, Player):
    for n in range(len(AllowedMoves)-1,-1,-1):
        move = AllowedMoves[n]
        NewX = move[1]; NewY = move[0]
        OldX = move[3]; OldY = move[2]
        prev = Pieces[NewY, NewX]
        Pieces[NewY, NewX] = Pieces[OldY, OldX]
        Pieces[OldY, OldX] = 0
        if In_Check(Pieces, Player):
            AllowedMoves.pop(n)
        Pieces[OldY, OldX] = Pieces[NewY, NewX]
        Pieces[NewY, NewX] = prev
    return AllowedMoves, Pieces

def Is_Pinned(PieceCoords, Pieces, Player): # find if you cant move a piece

    # Check if already in check
    selected = Pieces[PieceCoords[0], PieceCoords[1]]
    alreadyInCheck = In_Check(Pieces, Player)

    # Check if removing the piece matters
    Pieces[PieceCoords[0], PieceCoords[1]] = 0
    isPinned = In_Check(Pieces, Player)
    Pieces[PieceCoords[0], PieceCoords[1]] = selected

    # Run through moves for the piece to see if it can counterattack
    Moves = Legal_Moves([PieceCoords[0], PieceCoords[1]], Pieces, Player)
    Moves, Pieces = Check_Move_Narrower(Moves, Pieces, Player)
    if len(Moves) != 0:
        isPinned = False

    if isPinned == True and alreadyInCheck == False:
        return Moves, True
    else:
        return Moves, False

def Is_Checkmate(Pieces, Player):
    # Find all possible moves for the current player
    allLegalMoves = []
    for j in range(8):
        for i in range(8):
            allLegalMoves = allLegalMoves + Legal_Moves([j,i], Pieces, Player)

    # Check if any of them can prevent checkmate
    allLegalMoves, dump = Check_Move_Narrower(allLegalMoves, Pieces, Player)
    if len(allLegalMoves) == 0:
        return True
    else:
        return False
