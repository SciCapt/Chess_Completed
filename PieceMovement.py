import numpy as np
from Printer import *

def Piece_Is_White(PieceCoords, Pieces):
    piece = Pieces[PieceCoords[0], PieceCoords[1]]
    if piece == 0:
        return False
    if int(round(piece-piece//1, 2)*10) == 1:
        return True
    else:
        return False

def Piece_Is_Black(PieceCoords, Pieces):
    piece = Pieces[PieceCoords[0], PieceCoords[1]]
    if piece == 0:
        return False
    if int(round(piece-piece//1, 2)*10) == 2:
        return True
    else:
        return False

def Make_Move(AllowedMoves, NewCoords, PieceCoords, Pieces):
    NewX = NewCoords[1]; NewY = NewCoords[0]
    for n in range(len(AllowedMoves)):
        OldX = AllowedMoves[n][3]; OldY = AllowedMoves[n][2]
        ChkX = AllowedMoves[n][1]; ChkY = AllowedMoves[n][0]
        if OldX == PieceCoords[1] and OldY == PieceCoords[0]:
            if NewX == ChkX and NewY == ChkY:
                Pieces[NewY, NewX] = Pieces[PieceCoords[0], PieceCoords[1]]
                Pieces[PieceCoords[0], PieceCoords[1]] = 0
                CMD_Print(Pieces_To_Printable(Pieces))
                return False
    return True

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

def Legal_Moves_FOR_KING(PieceCoords, Pieces, Player):
    piece = Pieces[PieceCoords[0], PieceCoords[1]]
    legal = []
    # Pawn #
    if (piece == 1.1 and Player == 'W') or (piece == 1.2 and Player == 'B'):
        # Allow double move on first move
        if PieceCoords[0] == 6:
            if Pieces[PieceCoords[0]-1, PieceCoords[1]] == 0:
                if Pieces[PieceCoords[0]-2, PieceCoords[1]] == 0:
                    Pieces[PieceCoords[0], PieceCoords[1]] = Pieces[PieceCoords[0], PieceCoords[1]]
                    legal.append([PieceCoords[0]-2, PieceCoords[1], PieceCoords[0], PieceCoords[1]])
                        # format is [(ynew, xnew), (yold, xold)]

        # Typical one move up
        if Pieces[PieceCoords[0]-1, PieceCoords[1]] == 0:
            legal.append([PieceCoords[0]-1, PieceCoords[1], PieceCoords[0], PieceCoords[1]])

        # Taking a piece to the diagonal
        try:
            diag1 = Pieces[PieceCoords[0]-1, PieceCoords[1]-1]
        except:
            diag1 = 0
        try:
            diag2 = Pieces[PieceCoords[0]-1, PieceCoords[1]+1]
        except:
            diag2 = 0
        if diag1 != 0:
            if Player == 'B' and (Piece_Is_White([PieceCoords[0]-1, PieceCoords[1]-1], Pieces)) or Player == 'W' and (Piece_Is_Black([PieceCoords[0]-1, PieceCoords[1]-1], Pieces)):
                legal.append([PieceCoords[0]-1, PieceCoords[1]-1, PieceCoords[0], PieceCoords[1]])
        if diag2 != 0:
            if Player == 'B' and (Piece_Is_White([PieceCoords[0]-1, PieceCoords[1]+1], Pieces)) or Player == 'W' and (Piece_Is_Black([PieceCoords[0]-1, PieceCoords[1]+1], Pieces)):
                legal.append([PieceCoords[0]-1, PieceCoords[1]+1, PieceCoords[0], PieceCoords[1]])

        # # En` Patato - effects too many things (printer, piece values, removing 'en potatabilty' later, etc.)
        # try:
        #     if piece == 1.1:
        #         if Pieces[PieceCoords[0], PieceCoords[1]+1] == 1.21:
        #             legal.append([PieceCoords[0], PieceCoords[1]+1, PieceCoords[0], PieceCoords[1], True])
        #         elif Pieces[PieceCoords[0], PieceCoords[1]-1] == 1.21:
        #             legal.append([PieceCoords[0], PieceCoords[1]-1, PieceCoords[0], PieceCoords[1], True])
        # except:
        #     pass
        # try:
        #     if piece == 1.2:
        #         if Pieces[PieceCoords[0], PieceCoords[1]+1] == 1.11:
        #             legal.append([PieceCoords[0], PieceCoords[1]+1, PieceCoords[0], PieceCoords[1], True])
        #         elif Pieces[PieceCoords[0], PieceCoords[1]-1] == 1.11:
        #             legal.append([PieceCoords[0], PieceCoords[1]-1, PieceCoords[0], PieceCoords[1], True])
        # except:
        #     pass

    # Bishop #
    if (piece == 2.1 and Player == 'W') or (piece == 2.2 and Player == 'B'):
        Bx = PieceCoords[1]; By = PieceCoords[0]
        # Diagonal 1
        for j in range(1,8):
            i = j
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Diagonal 2
        for j in range(1,8):
            i = -j
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Diagonal 3
        for j in range(-1,-8,-1):
            i = j
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Diagonal 4
        for j in range(-1,-8,-1):
            i = -j
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break

        # # Diagonal 1 - Alternate Form
        # for j in range(1,8):
        #     if done == True:
        #         done = False
        #         break
        #     for i in range(1,8):
        #         if abs(j) == abs(i) and max(j+By, i+Bx) < 8 and min(j+By, i+Bx) >= 0:
        #             if Player == "B" and Piece_Is_Black([j+By, i+Bx], Pieces) or Player == "W" and Piece_Is_White([j+By, i+Bx], Pieces):
        #                 done = True
        #                 break
        #             elif Pieces[j+By, i+Bx] == 0:
        #                 legal.append([j+By, i+Bx, By, Bx])
        #             elif Player == "W" and Piece_Is_Black([j+By, i+Bx], Pieces) or Player == "B" and Piece_Is_White([j+By, i+Bx], Pieces):
        #                 legal.append([j+By, i+Bx, By, Bx])
        #                 done = True
        #                 break

    # Knight #
    if (piece == 3.1 and Player == 'W') or (piece == 3.2 and Player == 'B'):
        Kx = PieceCoords[1]; Ky = PieceCoords[0]
        for j in range(-2,3):
            for i in range(-2,3):
                if (abs(j) == 2 or abs(j) == 1) and (abs(i) == 2 or abs(i) == 1):
                    if Ky+j >= 0 and Ky+j <= 7 and Kx+i >= 0 and Kx+i <= 7 and abs(j) != abs(i):
                        if Player == 'W' and (Piece_Is_Black([Ky+j, Kx+i], Pieces) or Pieces[Ky+j, Kx+i] == 0):
                            legal.append([Ky+j, Kx+i, Ky, Kx])
                        if Player == 'B' and (Piece_Is_White([Ky+j, Kx+i], Pieces) or Pieces[Ky+j, Kx+i] == 0):
                            legal.append([Ky+j, Kx+i, Ky, Kx])

    # Rook #
    if (piece == 4.1 and Player == 'W') or (piece == 4.2 and Player == 'B'):
        # Definitley didn't just repurpose the bishop code what do ya mean xD
        By = PieceCoords[0]; Bx = PieceCoords[1]
        # Straight 1
        for j in range(-1,-8,-1):
            i = 0
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Straight 2
        for j in range(1,8):
            i = 0
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Straight 3
        for i in range(-1,-8,-1):
            j = 0
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Straight 4
        for i in range(1,8):
            j = 0
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break

    # Queen #
    if (piece == 5.1 and Player == 'W') or (piece == 5.2 and Player == 'B'):
        # OK YES I just used the bishop's and "rook's" code =)
        By = PieceCoords[0]; Bx = PieceCoords[1]
        # Straight 1
        for j in range(-1,-8,-1):
            i = 0
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Straight 2
        for j in range(1,8):
            i = 0
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Straight 3
        for i in range(-1,-8,-1):
            j = 0
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Straight 4
        for i in range(1,8):
            j = 0
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Diagonal 1
        for j in range(1,8):
            i = j
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Diagonal 2
        for j in range(1,8):
            i = -j
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Diagonal 3
        for j in range(-1,-8,-1):
            i = j
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Diagonal 4
        for j in range(-1,-8,-1):
            i = -j
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break

    return legal

def Legal_Moves(PieceCoords, Pieces, Player):
    piece = Pieces[PieceCoords[0], PieceCoords[1]]
    legal = []
    # Pawn #
    if (piece == 1.1 and Player == 'W') or (piece == 1.2 and Player == 'B'):
        # Allow double move on first move
        if PieceCoords[0] == 6:
            if Pieces[PieceCoords[0]-1, PieceCoords[1]] == 0:
                if Pieces[PieceCoords[0]-2, PieceCoords[1]] == 0:
                    Pieces[PieceCoords[0], PieceCoords[1]] = Pieces[PieceCoords[0], PieceCoords[1]]
                    legal.append([PieceCoords[0]-2, PieceCoords[1], PieceCoords[0], PieceCoords[1]])
                        # format is [(ynew, xnew), (yold, xold)]

        # Typical one move up
        if Pieces[PieceCoords[0]-1, PieceCoords[1]] == 0:
            legal.append([PieceCoords[0]-1, PieceCoords[1], PieceCoords[0], PieceCoords[1]])

        # Taking a piece to the diagonal
        try:
            diag1 = Pieces[PieceCoords[0]-1, PieceCoords[1]-1]
        except:
            diag1 = 0
        try:
            diag2 = Pieces[PieceCoords[0]-1, PieceCoords[1]+1]
        except:
            diag2 = 0
        if diag1 != 0:
            if Player == 'B' and (Piece_Is_White([PieceCoords[0]-1, PieceCoords[1]-1], Pieces)) or Player == 'W' and (Piece_Is_Black([PieceCoords[0]-1, PieceCoords[1]-1], Pieces)):
                legal.append([PieceCoords[0]-1, PieceCoords[1]-1, PieceCoords[0], PieceCoords[1]])
        if diag2 != 0:
            if Player == 'B' and (Piece_Is_White([PieceCoords[0]-1, PieceCoords[1]+1], Pieces)) or Player == 'W' and (Piece_Is_Black([PieceCoords[0]-1, PieceCoords[1]+1], Pieces)):
                legal.append([PieceCoords[0]-1, PieceCoords[1]+1, PieceCoords[0], PieceCoords[1]])

    # Bishop #
    if (piece == 2.1 and Player == 'W') or (piece == 2.2 and Player == 'B'):
        Bx = PieceCoords[1]; By = PieceCoords[0]
        # Diagonal 1
        for j in range(1,8):
            i = j
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Diagonal 2
        for j in range(1,8):
            i = -j
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Diagonal 3
        for j in range(-1,-8,-1):
            i = j
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Diagonal 4
        for j in range(-1,-8,-1):
            i = -j
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break

    # Knight #
    if (piece == 3.1 and Player == 'W') or (piece == 3.2 and Player == 'B'):
        Kx = PieceCoords[1]; Ky = PieceCoords[0]
        for j in range(-2,3):
            for i in range(-2,3):
                if (abs(j) == 2 or abs(j) == 1) and (abs(i) == 2 or abs(i) == 1):
                    if Ky+j >= 0 and Ky+j <= 7 and Kx+i >= 0 and Kx+i <= 7 and abs(j) != abs(i):
                        if Player == 'W' and (Piece_Is_Black([Ky+j, Kx+i], Pieces) or Pieces[Ky+j, Kx+i] == 0):
                            legal.append([Ky+j, Kx+i, Ky, Kx])
                        if Player == 'B' and (Piece_Is_White([Ky+j, Kx+i], Pieces) or Pieces[Ky+j, Kx+i] == 0):
                            legal.append([Ky+j, Kx+i, Ky, Kx])

    # Rook #
    if (piece == 4.1 and Player == 'W') or (piece == 4.2 and Player == 'B'):
        # Definitley didn't just repurpose the bishop code what do ya mean xD
        By = PieceCoords[0]; Bx = PieceCoords[1]
        # Straight 1
        for j in range(-1,-8,-1):
            i = 0
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Straight 2
        for j in range(1,8):
            i = 0
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Straight 3
        for i in range(-1,-8,-1):
            j = 0
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Straight 4
        for i in range(1,8):
            j = 0
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break

    # Queen #
    if (piece == 5.1 and Player == 'W') or (piece == 5.2 and Player == 'B'):
        # OK YES I just used the bishop's and "rook's" code =)
        By = PieceCoords[0]; Bx = PieceCoords[1]
        # Straight 1
        for j in range(-1,-8,-1):
            i = 0
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Straight 2
        for j in range(1,8):
            i = 0
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Straight 3
        for i in range(-1,-8,-1):
            j = 0
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Straight 4
        for i in range(1,8):
            j = 0
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Diagonal 1
        for j in range(1,8):
            i = j
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Diagonal 2
        for j in range(1,8):
            i = -j
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Diagonal 3
        for j in range(-1,-8,-1):
            i = j
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break
        # Diagonal 4
        for j in range(-1,-8,-1):
            i = -j
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break

    # King #
    if (piece == 6.1 and Player == 'W') or (piece == 6.2 and Player == 'B'):
        Kx = PieceCoords[1]; Ky = PieceCoords[0]
        # Default King Moves
        if Ky+1 < 8:
            legal.append([Ky+1, Kx, Ky, Kx])
            if Kx+1 < 8:
                legal.append([Ky+1, Kx+1, Ky, Kx])
            if Kx-1 >= 0:
                legal.append([Ky+1, Kx-1, Ky, Kx])
        if Ky-1 >= 0:
            legal.append([Ky-1, Kx, Ky, Kx])
            if Kx+1 < 8:
                legal.append([Ky-1, Kx+1, Ky, Kx])
            if Kx-1 >= 0:
                legal.append([Ky-1, Kx-1, Ky, Kx])
        if Kx+1 < 8:
            legal.append([Ky, Kx+1, Ky, Kx])
        if Kx-1 >= 0:
            legal.append([Ky, Kx-1, Ky, Kx])

        # Get moves of other player
        allMovesOther = []
        if Player == "W":
            Player2 = "B"
        else:
            Player2 = "W"
        for j in range(8):
            for i in range(8):
                newMove = Legal_Moves_FOR_KING([j,i], Flip_Pieces(Pieces), Player2)
                if len(newMove) != 0:
                    allMovesOther = allMovesOther + newMove
        allMovesOther = Flip_Moves(allMovesOther)

        # Check if any of other player moves block king's moves
        for n in range(len(allMovesOther)):
            for nn in range(-len(legal)+1,1):
                kmvX = legal[nn][1]; kmvY = legal[nn][0]
                chkX = allMovesOther[n][1]; chkY = allMovesOther[n][0]
                if chkX == kmvX and chkY == kmvY:
                    legal.pop(nn)

        # Check if any of player's pieces are in the way
        for j in range(8):
            for i in range(8):
                for n in range(-len(legal)+1,1):
                    kmvX = legal[n][1]; kmvY = legal[n][0]
                    if kmvX == i and kmvY == j:
                        if Player=="B" and Piece_Is_Black([j,i],Pieces) or Player=="W" and Piece_Is_White([j,i],Pieces):
                            legal.pop(n)

    # Finish
    return legal
