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
    pi = Pieces[OldY, OldX, 0]
    try:
        IsCastling = ChosenMove[4]
    except:
        IsCastling = False
    if IsCastling:
        # Apply castling move to board
        King = Pieces[NewY, NewX,0]
        if Pieces[NewY, NewX,1] == 1:
            return Pieces, True
        Rook = Pieces[OldY, OldX,0]
        kingy = ChosenMove[5]
        kingx = ChosenMove[6]
        rooky = ChosenMove[7]
        rookx = ChosenMove[8]
        # New Piece Locations
        Pieces[kingy, kingx,0] = King
        Pieces[rooky, rookx,0] = Rook
        Pieces[OldY, OldX,0] = 0
        Pieces[NewY, NewX,0] = 0
        # Set Flags
        Pieces[kingy, kingx, 1] = 1 # Castling flag
        Pieces[NewY, NewX, 1] = 0 # Castling flag
        Pieces[rooky, rookx, 1] = 1 # Castling flag
        Pieces[OldY, OldX, 1] = 0 # Castling flag
        # Update dim3 (piece movement tally)
        Pieces[kingy, kingx, 3] = Pieces[NewY, NewX, 3] + 1
        Pieces[NewY, NewX, 3] = 0
        Pieces[rooky, rookx, 3] = Pieces[OldY, OldX, 3] + 1
        Pieces[OldY, OldX, 3] = 0
        return Pieces, False

    elif not IsCastling:
        # Apply move to board
        capture = Pieces[NewY, NewX, 0]
        # Update Pieces/Flags
        Pieces[NewY, NewX,0] = Pieces[OldY, OldX,0]
        Pieces[OldY, OldX,0] = 0
        Pieces[NewY, NewX, 1] = Pieces[OldY, OldX, 1]
        Pieces[OldY, OldX, 1] = 0
        # AI Capture Memory
        Pieces[NewY, NewX, 2] = capture
        Pieces[OldY, OldX, 2] = 0
        # Update dim3 (piece movement tally)
        Pieces[NewY, NewX, 3] = Pieces[OldY, OldX, 3] + 1
        Pieces[OldY, OldX, 3] = 0
        # Check for moving king
        if Pieces[NewY, NewX, 0] == 6.1 or Pieces[NewY, NewX, 0] == 6.2: # King Movement disables castling
            Pieces[NewY, NewX, 1] = 1
            Pieces[OldY, OldX, 1] = 0
        # Check for moving rook
        if Pieces[NewY, NewX, 0] == 4.1 or Pieces[NewY, NewX, 0] == 4.2: # King Movement disables castling
            Pieces[NewY, NewX, 1] = 1
            Pieces[OldY, OldX, 1] = 0


    # Check for Pawn Promotion
    if NewY == 0 and ((pi == 1.1 and Player == "W") or (pi == 1.2 and Player == "B")):
        # Pieces[NewY, NewX, 2] = Pieces[NewY, NewX, 0] # Whoops, not needed
        # Also caused problems with pawn promotion as this same thing is done
        # effectively a few lines earlier
        Pieces[OldY, OldX, 2] = 0
        if Pieces[NewY, NewX,0] == 1.1 and Player == "W":
            Pieces[NewY, NewX,0] = rn.choice([5.1,5.1,5.1,5.1,4.1,3.1,2.1])
            Pieces[NewY, NewX,1] = 2 # Flag for pawn promotion
            Pieces[OldY, OldX,1] = 0 # Remove en potato flag
        elif Pieces[NewY, NewX,0] == 1.2 and Player == "B":
            Pieces[NewY, NewX,0] = rn.choice([5.2,5.2,5.2,5.2,4.2,3.2,2.2])
            Pieces[NewY, NewX,1] = 2 # Flag for pawn promotion
            Pieces[OldY, OldX,1] = 0 # Remove en potato flag
    return Pieces, False

def Is_Capture(Pieces, Player, ChosenMove):
    xMove = ChosenMove[1]; yMove = ChosenMove[0]
    if Pieces[yMove, xMove,0] != 0:
        if (Piece_Is_Black([yMove, xMove], Pieces) and Player == "W" or
            Piece_Is_White([yMove, xMove], Pieces) and Player == "B"):
            return True
    return False

def Undo_AI_Move(Pieces, Player, ChosenMove):
    # Cords (Flipped logic for undoing the move)
    OldX = ChosenMove[3]; OldY = ChosenMove[2]
    NewX = ChosenMove[1]; NewY = ChosenMove[0]

    # Check if last move was Castling
    try:
        IsCastling = ChosenMove[4]
    except:
        IsCastling = False
    if IsCastling:
        King = Pieces[NewY, NewX, 0]
        KingMoved = False
        if Pieces[NewY, NewX, 1] == 1:
            KingMoved = True
        Rook = Pieces[OldY, OldX, 0]
        kingy = ChosenMove[5]
        kingx = ChosenMove[6]
        rooky = ChosenMove[7]
        rookx = ChosenMove[8]
        # Undo Castling
        Pieces[NewY, NewX, 0] = Pieces[kingy, kingx, 0]
        Pieces[kingy, kingx, 0] = 0
        Pieces[OldX, OldY, 0] = Pieces[rooky, rookx, 0]
        Pieces[rooky, rookx, 0] = 0
        # Undo updating dim3 (piece movement tally)
        if Pieces[kingy, kingx, 3] > 0:
            Pieces[NewY, NewX, 3] = Pieces[kingy, kingx, 3] - 1
        Pieces[kingy, kingx, 3] = 0
        if Pieces[rooky, rookx, 3] > 0:
            Pieces[OldY, OldX, 3] = Pieces[rooky, rookx, 3] - 1
        Pieces[rooky, rookx, 3] = 0
        return Pieces

    # Test for pawn promotion
    if Pieces[NewY, NewX, 1] == 2:
        Pieces[NewY, NewX, 1] = 0
        Pieces[NewY, NewX, 0] = 0
        if Player == "W":
            Pieces[OldY, OldX, 0] = 1.1
            Pieces[OldY, OldX, 1] = 0
            Pieces[NewY, NewX, 0] = Pieces[NewY, NewX, 2]
            Pieces[NewY, NewX, 2] = 0
            return Pieces
        elif Player == "B":
            Pieces[OldY, OldX, 0] = 1.2
            Pieces[OldY, OldX, 1] = 0
            Pieces[NewY, NewX, 0] = Pieces[NewY, NewX, 2]
            Pieces[NewY, NewX, 2] = 0
            return Pieces

    # Default Undo Move
    Pieces[OldY, OldX, 0] = Pieces[NewY, NewX, 0]
    Pieces[NewY, NewX, 0] = 0
    Pieces[OldY, OldX, 1] = Pieces[NewY, NewX, 1]
    Pieces[NewY, NewX, 1] = 0
    Pieces[NewY, NewX, 0] = Pieces[NewY, NewX, 2]
    Pieces[NewY, NewX, 2] = 0
    # Undo Update dim3 (piece movement tally)
    if Pieces[NewY, NewX, 3] > 0:
        Pieces[OldY, OldX, 3] = Pieces[NewY, NewX, 3] - 1
    Pieces[NewY, NewX, 3] = 0
    return Pieces

def Remove_Move(ChosenMove, AIMoves):
    for move in range(len(AIMoves)):
        if ChosenMove == AIMoves[move]:
            AIMoves.pop(move)
            return AIMoves
    # Thought I would need this for some errors I was getting but I haven't
    # actually had to use it yet. Consider this function depreciated for now
        # Also, the 'False' return at the end of AI_Make_Move isn't neccessary
        # if this function isn't either.

def SF_Position(Pieces):
    # Single-Frame based Position Algorithm
    # Give the net (simple) position value of the current board
    # Doesn't account for things like discovered checks/attacks
    BlackPos = 0
    WhitePos = 0

    # Step 1 - Development
    ## Give points for having moved Pieces and Pawns
    ## Only matters if a piece has moved, not if it has moved
    ## multiple times. Give a fraction of a set maximum points based on
    ## the fraction of pieces/pawns that have moved
    MaxPoints = 3
    BlackPieceCount = 0
    BlackTally = 0
    WhitePieceCount = 0
    WhiteTally = 0
    for i in range(8):
        for j in range(8):
            pi = Pieces[i,j,0]
            tally = Pieces[i,j,3]
            # See if piece has moved, and who owns it
            if tally > 0:
                if pi-(pi//1) == 0.1:
                    WhiteTally += 1
                elif pi-(pi//1) == 0.2:
                    BlackTally += 1
            # Total up pieces/pawns of each side
            if pi-(pi//1) == 0.1:
                WhitePieceCount += 1
            elif pi-(pi//1) == 0.2:
                BlackPieceCount += 1
    # Calculate points to give based on development
    WhitePos += MaxPoints*(WhiteTally/WhitePieceCount)
    BlackPos += MaxPoints*(BlackTally/BlackPieceCount)

def It_Position(Pieces):
    # Iterated Position ('smart') Algorithm
    # First uses SF_Position to check the immediate position, then checks for
    # discovered checks/attacks by making all the current moves avalible for both
    # players. This can then also be used to check for an M1 position.
        # The Hard AIs will likely do some depth analysis taking full advantage
        # of this algorithm to check for any M# positions possible. This allows
        # for a few personalities to test for this later on
    print('void')

## Troubleshooting AI ##
def AI_Tester_Move(Pieces, Player):
    # Get all possible moves for AI
    AIMoves, OriginalBoard = AI_Possible_Moves(Pieces, Player)

    ## Jeff Stuff ##
    if Player == "W":
        PlayerTest = "B"
    elif Player == "B":
        PlayerTest = "W"
    FavoredMoves = []

    # Favored move
    for move in range(len(AIMoves)):
        ChosenMove = AIMoves[move]
        try:
            castling = ChosenMove[4]
        except:
            castling = False

        if castling == True:
            FavoredMoves.append(ChosenMove)

    for move in range(len(FavoredMoves)):
        for i in range(100): # x100 check move likelyhood
            AIMoves.append(FavoredMoves[move])

    # Select Move from Optimized List
    ChosenMove = rn.choice(AIMoves)

    # Finish
    Pieces = AI_Make_Move(Pieces, Player, ChosenMove)[0]
    return Pieces

## Group I AIs ##
def AI_Bob_Move(Pieces, Player):
    # Get all possible moves for AI
    AIMoves, Pieces = AI_Possible_Moves(Pieces, Player)

    # Bob Stuff (Choose random move, ELO = 125)
    ChosenMove = rn.choice(AIMoves)

    # Finish
    Pieces, Pop = AI_Make_Move(Pieces, Player, ChosenMove)
    return Pieces

def AI_Jeff_Move(Pieces, Player):
    # Get all possible moves for AI
    AIMoves, OriginalBoard = AI_Possible_Moves(Pieces, Player)

    ## Jeff Stuff ##
    if Player == "W":
        PlayerTest = "B"
    elif Player == "B":
        PlayerTest = "W"
    CheckMoves = []
    CaptureMoves = []

    # Favor Checks (x4 Likelyhood)
    for move in range(len(AIMoves)):
        ChosenMove = AIMoves[move]
        Pieces = AI_Make_Move(Pieces, Player, ChosenMove)[0]
        if In_Check(Flip_Pieces(Pieces), PlayerTest):
            CheckMoves.append(ChosenMove)
        Pieces = Undo_AI_Move(Pieces, Player, ChosenMove)

    # Favor Captures (x3 Likelyhood)
    for move in range(len(AIMoves)):
        ChosenMove = AIMoves[move]
        if Is_Capture(Pieces, Player, ChosenMove):
            CaptureMoves.append(ChosenMove)

    # Add Favored Moves to main move list
    for move in range(len(CheckMoves)):
        for i in range(4): # x4 check move likelyhood
            AIMoves.append(CheckMoves[move])

    for move in range(len(CaptureMoves)):
        for i in range(3): # x3 check move likelyhood
            AIMoves.append(CaptureMoves[move])

    # Select Move from Optimized List
    ChosenMove = rn.choice(AIMoves)

    # Finish
    Pieces = AI_Make_Move(Pieces, Player, ChosenMove)[0]
    return Pieces

def AI_Jeff_Advanced_Move(Pieces, Player, SickoMode=False):
    # Get all possible moves for AI
    AIMoves, OriginalBoard = AI_Possible_Moves(Pieces, Player)

    ## Jeff Stuff ##
    if Player == "W":
        PlayerTest = "B"
    elif Player == "B":
        PlayerTest = "W"
    CheckMoves = []
    CaptureMoves = []

    # Favor Checks (x10 Likelyhood)
    for move in range(len(AIMoves)):
        ChosenMove = AIMoves[move]
        ToCoords = [ChosenMove[0], ChosenMove[1]]
        Pieces = AI_Make_Move(Pieces, Player, ChosenMove)[0]
        if In_Check(Flip_Pieces(Pieces), PlayerTest):
            if not Is_Under_Attack(ToCoords, Pieces, Player):
                CheckMoves.append(ChosenMove)
        Pieces = Undo_AI_Move(Pieces, Player, ChosenMove)

    # Favor Captures (x10 Likelyhood)
    for move in range(len(AIMoves)):
        ChosenMove = AIMoves[move]
        ToCoords = [ChosenMove[0], ChosenMove[1]]
        if Is_Capture(Pieces, Player, ChosenMove):
            if not Is_Under_Attack(ToCoords, Pieces, Player):
                CaptureMoves.append(ChosenMove)

    # Add Favored Moves to main move list
    if SickoMode == True:
        Aggressiveness = 20
    else:
        Aggressiveness = 10

    for move in range(len(CheckMoves)):
        for i in range(Aggressiveness): # x10 check move likelyhood
            AIMoves.append(CheckMoves[move])

    for move in range(len(CaptureMoves)):
        for i in range(Aggressiveness): # x10 check move likelyhood
            AIMoves.append(CaptureMoves[move])

    # Select Move from Optimized List
    ChosenMove = rn.choice(AIMoves)

    # Finish
    Pieces = AI_Make_Move(Pieces, Player, ChosenMove)[0]
    return Pieces

def AI_Nelson_Move(Pieces, Player):
    # Get all possible moves for AI
    AIMoves, Pieces = AI_Possible_Moves(Pieces, Player)

    # Define Nelson's Queen
    if Player == "W":
        queen = 5.1
    elif Player == "B":
        queen = 5.2

    # Nelson Stuff (favor queen moves)
    FavoredMoves = []
    for n in range(len(AIMoves)):
        move = AIMoves[n]
        if Pieces[move[2], move[3], 0] == queen:
            PieceCoords = [move[0], move[1]]
            if not Is_Under_Attack(PieceCoords, Pieces, Player):
                FavoredMoves.append(move)
            # elif rn.random() > 0.9: # 10% of the time, add queen move even if
            #                        # it can be taken with a certain move
            #     FavoredMoves.append(move)

    # Add queen move multiple times to AIMoves to make a queen move a
    # configureable amount of the time dictated by QueenMoveRatio
    QueenMoveRatio = 1 # 1:1 ratio of normal moves to extra favored quene moves
    QueenMoveLen = len(AIMoves)*QueenMoveRatio//1
    QueenMove = 0
    if len(FavoredMoves) != 0:
        for n in range(QueenMoveLen):
            if QueenMove >= len(FavoredMoves):
                QueenMove = 0
            AIMoves.append(FavoredMoves[QueenMove])
            QueenMove += 1

    # Select Move from Optimized List
    ChosenMove = rn.choice(AIMoves)

    # Finish
    Pieces, Pop_DEPRECIATED_I_THINK = AI_Make_Move(Pieces, Player, ChosenMove)
    return Pieces

## Group II AIs ##
