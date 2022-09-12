from AI import *
from Printer import *
from Definitions import *
from MousePosition import *
from PieceMovement import *
from CheckmateNerd import *
import pygetwindow as wn
from os import system
import numpy as np
import time
import random as rn
import mouse

# Setup AI
AIPlayer = input("Use AI For Player 2? (y/n): ")
# AIPlayer = 'y'
if AIPlayer in ['y', 'Y', 'yes', 'YES', 'nai', 'si', 'da', 'dak', 'wi', 'oui']:
    UseAI = True
    try:
        Difficulty = int(input("AI Difficulty (1 - 5): "))
    except:
        Difficulty = 1
else:
    UseAI = False

# Set CMD Window to Particular Size and Position
system("title " + 'Chess')
time.sleep(.05) # small time delay to allow title to update
GameWindow = wn.getWindowsWithTitle('Chess')[0]
GameWindow.resizeTo(930, 830)
GameWindow.moveTo(0, 0)

# Base Array Variables
Pieces = Starting_Board(np.zeros((8,8,4))); Player = "W"
    # dim 0 is pieces
    # dim 1 is piece flags
    # dim 2 is for ai captures
    # dim 3 is how many times a piece has moved
# if rn.random() > 0.5:
#     Pieces = Flip_Pieces(Pieces)
#     Player = "B"
MainPlayer = Player
turntable = ["W", "B"]
mistake = False
restart = False
turn = 0

# Pieces = AIPawnPromotionBoard()

# Dynamic Section
for t in range(1000):
    # Check if player is idiot and selected unmoveable piece, or if the player
    # is semi-compeitent and completed their're turn, move to the next player
    if mistake == False:
        Player = turntable[turn%2]
        turn = turn + 1
        
    else:
        mistake = False

    # Checkmate Detection
    if Player == MainPlayer:
        CMD_Print(Pieces_To_Printable(Pieces))
    if Is_Checkmate(Pieces, Player):
        break
    if Only_Kings(Pieces):
        break

    # Use AI for Player 2
    if UseAI and Player != MainPlayer:
        # Make move via ai
        if Difficulty == 1:
            Pieces = AI_Bob_Move(Pieces, Player)
        elif Difficulty == 2:
            Pieces = AI_Jeff_Move(Pieces, Player)
        elif Difficulty == 3:
            Pieces = AI_Jeff_Advanced_Move(Pieces, Player)
        elif Difficulty == 4:
            Pieces = AI_Nelson_Move(Pieces, Player)
        elif Difficulty == 5:
            Pieces = AI_Jeff_Advanced_Move(Pieces, Player, SickoMode=True)

        # Set board for other player
        if turn != 1:
            Pieces = Flip_Pieces(Pieces)
        continue

    # Print Board; Highlight king if it is in check
    if In_Check(Pieces, Player):
        if Player == "W":
            king = 6.1
        elif Player == "B":
            king = 6.2
        for j in range(8):
            for i in range(8):
                if Pieces[j,i,0] == king:
                    kingX = i
                    kingY = j
        CMD_Print(Highlight_Square([[kingY, kingX]], Pieces))
    else:
        CMD_Print(Pieces_To_Printable(Pieces))

    # Select Piece and check its a piece of the current player
    while True:
        PieceCoords = Select_Square()
        # Check if actually moving one of the player's Pieces
        if Player == 'W':
            if Piece_Is_White(PieceCoords, Pieces) == True:
                break
        elif Player == 'B':
            if Piece_Is_Black(PieceCoords, Pieces) == True:
                break

    # Calculate legal moves; Update screen with highlight
    AllowedMoves = Legal_Moves(PieceCoords, Pieces, Player)
    if len(AllowedMoves) == 0:
        mistake = True
        continue
    AllowedMoves, Pinned = Is_Pinned(PieceCoords, Pieces, Player)
    if Pinned:
        mistake = True
        continue

    # Limit moves to lgeal moves if in check
    if In_Check(Pieces, Player):
        AllowedMoves, Pieces = Check_Move_Narrower(AllowedMoves, Pieces, Player)
    if len(AllowedMoves) == 0:
        mistake = True
        continue

    CMD_Print(Highlight_Square([PieceCoords]+AllowedMoves, Pieces))

    # Select new position or unselect current position; check if legal then move
    HasntMoved = True
    while HasntMoved:
        NewCoords = Select_Square()
        # if NewCoords == PieceCoords: # Unselect piece and restart!
        #     restart = True
        #     break
        # Check if actually making a legal move
        HasntMoved = Make_Move(AllowedMoves, NewCoords, PieceCoords, Pieces)
        if HasntMoved == True: # Actually fixes a few selection problems
            restart = True     # while also making unselecting easier
            mistake = True
            break

    # Secondary break for unselecting a piece
    if restart == True:
        restart = False
        mistake = True
        continue

    # Pawn Promotion Check
    pi = Pieces[NewCoords[0], NewCoords[1],0]
    if pi == 1.1 and Player == "W" or pi == 1.2 and Player == "B":
        if NewCoords[0] == 0:
            # system('cls')
            newpiece = Pawn_Promotion(Player)
            Pieces[NewCoords[0], NewCoords[1],0] = newpiece
            Pieces[NewCoords[0], NewCoords[1],1] = 2 # Flag for pawn promotion
            Pieces[PieceCoords[0], PieceCoords[1],1] = 0 # Remove en potato flag

    # Set Board for next player
    Pieces = Flip_Pieces(Pieces)

# Print final frame if player won by pawn promotion
if Player != MainPlayer:
    Pieces = Flip_Pieces(Pieces)
    CMD_Print(Pieces_To_Printable(Pieces))

# Final Out for Detected Checkmate/Stalemate/etc.
if Only_Kings(Pieces):
    print(f'\nStalemate Detected!')
elif not In_Check(Pieces, Player):
    print(f'\nStalemate Detected!')
else:
    print(f'\nCheckmate Detected!')
    if Player == "W":
        Player = "B"
    elif Player == "B":
        Player = "W"
    print(f'Player {Player} Wins!')
