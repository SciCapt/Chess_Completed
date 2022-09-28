import numpy as np
from Printer import *

def Piece_Is_White(PieceCoords, Pieces):
    piece = Pieces[PieceCoords[0], PieceCoords[1], 0]
    if piece == 0:
        return False
    if int(round(piece-piece//1, 2)*10) == 1:
        return True
    else:
        return False

def Piece_Is_Black(PieceCoords, Pieces):
    piece = Pieces[PieceCoords[0], PieceCoords[1], 0]
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

        try:
            IsCastling = AllowedMoves[n][4]
        except:
            IsCastling = False
        if IsCastling:
            King = Pieces[NewY, NewX, 0]
            KingMoved = False
            if Pieces[NewY, NewX, 1] == 1:
                KingMoved = True
            Rook = Pieces[OldY, OldX, 0]
            kingy = AllowedMoves[n][5]
            kingx = AllowedMoves[n][6]
            rooky = AllowedMoves[n][7]
            rookx = AllowedMoves[n][8]

        if OldX == PieceCoords[1] and OldY == PieceCoords[0]:
            if NewX == ChkX and NewY == ChkY:

                if not IsCastling:
                    # Move Piece
                    Pieces[NewY, NewX, 0] = Pieces[PieceCoords[0], PieceCoords[1], 0]
                    Pieces[PieceCoords[0], PieceCoords[1], 0] = 0
                    # Move Flags
                    Pieces[NewY, NewX, 1] = Pieces[OldY, OldX, 1]
                    Pieces[OldY, OldX, 1] = 0
                    # Update dim3 (piece movement tally)
                    Pieces[NewY, NewX, 3] = Pieces[OldY, OldX, 3] + 1
                    Pieces[OldY, OldX, 3] = 0
                    # If moving king, set king flag to 1
                    if Pieces[NewY, NewX, 0] == 6.1 or Pieces[NewY, NewX, 0] == 6.2: # King Movement disables castling
                        Pieces[NewY, NewX, 1] = 1
                        Pieces[OldY, OldX, 1] = 0
                    # if moving a rook, set anti-castling flag for that rook
                    if Pieces[NewY, NewX, 0] == 4.1 or Pieces[NewY, NewX, 0] == 4.2:
                        Pieces[NewY, NewX, 1] = 1
                        Pieces[OldY, OldX, 1] = 0

                elif IsCastling:
                    if KingMoved: # King Movement disables castling
                        return True
                    # New king/rook positions
                    Pieces[kingy, kingx, 0] = King
                    Pieces[kingy, kingx, 1] = 1 # Castling flag
                    Pieces[rooky, rookx, 0] = Rook
                    Pieces[rooky, rookx, 1] = 1 # Castling flag
                    # Removing pieces/flags from previous locations
                    Pieces[OldY, OldX, 0] = 0
                    Pieces[NewY, NewX, 0] = 0
                    Pieces[NewY, NewX, 1] = 0 # Castling flag
                    Pieces[OldY, OldX, 1] = 0 # Castling flag
                    # Update dim3 (piece movement tally)
                    Pieces[kingy, kingx, 3] = Pieces[NewY, NewX, 3] + 1
                    Pieces[NewY, NewX, 3] = 0
                    Pieces[rooky, rookx, 3] = Pieces[OldY, OldX, 3] + 1
                    Pieces[OldY, OldX, 3] = 0
                CMD_Print(Pieces_To_Printable(Pieces))
                return False
    return True

def Undo_Move(Pieces, Player, ChosenMove):
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

def Only_Kings(Pieces):
    # Remove kings from board
    for j in range(8):
        for i in range(8):
            if Pieces[j,i,0] == 6.1:
                Pieces[j,i,0] = 0
                king1 = [j,i]
            elif Pieces[j,i,0] == 6.2:
                Pieces[j,i,0] = 0
                king2 = [j,i]

    # Test if no other pieces are on the board
    same = True
    for j in range(8):
        if same == False:
            break
        for i in range(8):
            if Pieces[j,i,0] != 0:
                same = False
                break

    # Restore board
    Pieces[king1[0], king1[1],0] = 6.1
    Pieces[king2[0], king2[1],0] = 6.2
    return same

def Legal_Moves_FOR_KING(PieceCoords, Pieces, Player):
    piece = Pieces[PieceCoords[0], PieceCoords[1], 0]
    legal = []
    # Pawn #
    if (piece == 1.1 and Player == 'W') or (piece == 1.2 and Player == 'B'):
        # Allow double move on first move
        if PieceCoords[0] == 6:
            if Pieces[PieceCoords[0]-1, PieceCoords[1],0] == 0:
                if Pieces[PieceCoords[0]-2, PieceCoords[1],0] == 0:
                    Pieces[PieceCoords[0], PieceCoords[1],0] = Pieces[PieceCoords[0], PieceCoords[1],0]
                    legal.append([PieceCoords[0]-2, PieceCoords[1], PieceCoords[0], PieceCoords[1]])
                        # format is [(ynew, xnew), (yold, xold)]

        # Typical one move up
        if PieceCoords[0]-1 >= 0 and PieceCoords[0]-1 < 8:
            if Pieces[PieceCoords[0]-1, PieceCoords[1],0] == 0:
                legal.append([PieceCoords[0]-1, PieceCoords[1], PieceCoords[0], PieceCoords[1]])

        # Taking a piece to the diagonal
        if PieceCoords[0]-1 >= 0 and PieceCoords[0]-1 < 8:
            if PieceCoords[1]-1 >= 0 and PieceCoords[1]-1 < 8:
                try:
                    diag1 = Pieces[PieceCoords[0]-1, PieceCoords[1]-1,0]
                except:
                    diag1 = 0
            if PieceCoords[1]+1 >= 0 and PieceCoords[1]+1 < 8:
                try:
                    diag2 = Pieces[PieceCoords[0]-1, PieceCoords[1]+1,0]
                except:
                    diag2 = 0
        try:
            if diag1 != 0:
                if Player == 'B' and (Piece_Is_White([PieceCoords[0]-1, PieceCoords[1]-1], Pieces)) or Player == 'W' and (Piece_Is_Black([PieceCoords[0]-1, PieceCoords[1]-1], Pieces)):
                    legal.append([PieceCoords[0]-1, PieceCoords[1]-1, PieceCoords[0], PieceCoords[1]])
            if diag2 != 0:
                if Player == 'B' and (Piece_Is_White([PieceCoords[0]-1, PieceCoords[1]+1], Pieces)) or Player == 'W' and (Piece_Is_Black([PieceCoords[0]-1, PieceCoords[1]+1], Pieces)):
                    legal.append([PieceCoords[0]-1, PieceCoords[1]+1, PieceCoords[0], PieceCoords[1]])
        except:
            pass

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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                        if Player == 'W' and (Piece_Is_Black([Ky+j, Kx+i], Pieces) or Pieces[Ky+j, Kx+i,0] == 0):
                            legal.append([Ky+j, Kx+i, Ky, Kx])
                        if Player == 'B' and (Piece_Is_White([Ky+j, Kx+i], Pieces) or Pieces[Ky+j, Kx+i,0] == 0):
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
                    legal.append([By+j,Bx+i, By, Bx])
                elif Player=="B" and Piece_Is_White([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_Black([By+j,Bx+i],Pieces):
                    legal.append([By+j,Bx+i, By, Bx])
                    break

    return legal

def IUA_FOR_KING(CordsList, Pieces, Player):
    # List of True/Falses
    Booleans = []

    for n in range(len(CordsList)):
        # Get Piece Coords player is testing if is under attack
        PieceCoords = CordsList[n]
        Pix = PieceCoords[1]; Piy = PieceCoords[0]

        # Find all possible moves for the other player
        if Player == "W":
            otherPlayer = "B"
        else:
            otherPlayer = "W"
        allLegalMoves = []
        for j in range(8):
            for i in range(8):
                allLegalMoves = allLegalMoves + Legal_Moves_FOR_KING([j,i], Flip_Pieces(Pieces), otherPlayer)

        # Flip Moves
        allLegalMoves = Flip_Moves(allLegalMoves)

        # Delete Straight Pawn Moves (Can't capture)
        for n in range(len(allLegalMoves)-1, -1, -1):
            move = allLegalMoves[n]
            if Pieces[move[2], move[3], 0]//1 == 1: # is the piece a pawn
                if move[1] == move[3]: # Same x row
                    if move[0] == move[2]+1 or move[0] == move[2]+2: # 1 or 2 square pawn move
                        # If all true, then it is a non-capturing pawn move
                        # so it shouldn't be factored as an attack
                        allLegalMoves.pop(n)


        # Test if other player has move to capture test piece
        for n in range(len(allLegalMoves)):
            move = allLegalMoves[n]
            moveX = move[1]; moveY = move[0]
            if moveX == Pix and moveY == Piy:
                Booleans.append(True)
        Booleans.append(False)

    return Booleans

def Legal_Moves(PieceCoords, Pieces, Player):
    piece = Pieces[PieceCoords[0], PieceCoords[1], 0]
    legal = []
    # Pawn #
    if (piece == 1.1 and Player == 'W') or (piece == 1.2 and Player == 'B'):
        # Allow double move on first move
        if PieceCoords[0] == 6:
            if Pieces[PieceCoords[0]-1, PieceCoords[1],0] == 0:
                if Pieces[PieceCoords[0]-2, PieceCoords[1],0] == 0:
                    Pieces[PieceCoords[0], PieceCoords[1],0] = Pieces[PieceCoords[0], PieceCoords[1],0]
                    legal.append([PieceCoords[0]-2, PieceCoords[1], PieceCoords[0], PieceCoords[1]])
                        # format is [(ynew, xnew), (yold, xold)]

        # Typical one move up
        if PieceCoords[0]-1 >= 0 and PieceCoords[0]-1 < 8:
            if Pieces[PieceCoords[0]-1, PieceCoords[1],0] == 0:
                legal.append([PieceCoords[0]-1, PieceCoords[1], PieceCoords[0], PieceCoords[1]])

        # Taking a piece to the diagonal
        if PieceCoords[0]-1 >= 0 and PieceCoords[0]-1 < 8:
            if PieceCoords[1]-1 >= 0 and PieceCoords[1]-1 < 8:
                try:
                    diag1 = Pieces[PieceCoords[0]-1, PieceCoords[1]-1,0]
                except:
                    diag1 = 0
            if PieceCoords[1]+1 >= 0 and PieceCoords[1]+1 < 8:
                try:
                    diag2 = Pieces[PieceCoords[0]-1, PieceCoords[1]+1,0]
                except:
                    diag2 = 0
        try:
            if diag1 != 0:
                if Player == 'B' and (Piece_Is_White([PieceCoords[0]-1, PieceCoords[1]-1], Pieces)) or Player == 'W' and (Piece_Is_Black([PieceCoords[0]-1, PieceCoords[1]-1], Pieces)):
                    legal.append([PieceCoords[0]-1, PieceCoords[1]-1, PieceCoords[0], PieceCoords[1]])
        except:
            pass
        try:
            if diag2 != 0:
                if Player == 'B' and (Piece_Is_White([PieceCoords[0]-1, PieceCoords[1]+1], Pieces)) or Player == 'W' and (Piece_Is_Black([PieceCoords[0]-1, PieceCoords[1]+1], Pieces)):
                    legal.append([PieceCoords[0]-1, PieceCoords[1]+1, PieceCoords[0], PieceCoords[1]])
        except:
            pass

    # Bishop #
    if (piece == 2.1 and Player == 'W') or (piece == 2.2 and Player == 'B'):
        Bx = PieceCoords[1]; By = PieceCoords[0]
        # Diagonal 1
        for j in range(1,8):
            i = j
            if 0 <= By+j < 8 and 0 <= Bx+i < 8:
                if Player=="B" and Piece_Is_Black([By+j,Bx+i],Pieces) or Player=="W" and Piece_Is_White([By+j,Bx+i],Pieces):
                    break
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                        if Player == 'W' and (Piece_Is_Black([Ky+j, Kx+i], Pieces) or Pieces[Ky+j, Kx+i,0] == 0):
                            legal.append([Ky+j, Kx+i, Ky, Kx])
                        if Player == 'B' and (Piece_Is_White([Ky+j, Kx+i], Pieces) or Pieces[Ky+j, Kx+i,0] == 0):
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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
                elif Pieces[By+j,Bx+i,0] == 0:
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

        # Castling #
        Ry = Ky; Rx = Kx

        # Check if king moved or already castled
        if Player == "W":
            checkFor = 6.1
            rookNum = 4.1
        else:
            checkFor = 6.2
            rookNum = 4.2
        for j in range(8):
            for i in range(8):
                rookX = []; rookY = []
                if Pieces[j,i,0] == checkFor:
                    kingX = i
                    kingY = j
                if Pieces[j,i,0] == rookNum:
                    rookX.append(i)
                    rookY.append(j)
        if Pieces[kingY,kingX,1] == 1:
            return legal

        # Castling for black
        if True not in IUA_FOR_KING([[7,3]], Pieces, "B"): # If king not in check
            if Pieces[7,3,0] == 6.2 and True not in IUA_FOR_KING([[7,1], [7,2]], Pieces, "B"): # if king in right pos and the in-between squares aren't under attack
                if Pieces[7, 1,0] == 0 and Pieces[7,2,0] == 0 and Pieces[7,0,0] == 4.2 and Player == "B": # if the rook and opsn squares are in the right pos
                    if Pieces[7,0,1] != 1: # if the rook doesn't have an anti-casling flag
                        legal.append([7, 0, 7, 3, True, 7, 1, 7, 2])
                        # format of [newy, newx, oldy, oldx, IsCastling, kingy, kingx, rooky, rookx]
            if Pieces[7,3,0] == 6.2 and True not in IUA_FOR_KING([[7,4], [7,5], [7,6]], Pieces, "B"):
                if Pieces[7, 4,0] == 0 and Pieces[7,5,0] == 0 and Pieces[7,6,0] == 0 and Pieces[7,7,0] == 4.2 and Player == "B":
                    if Pieces[7,7,1] != 1:
                        legal.append([7, 7, 7, 3, True, 7, 5, 7, 4])
        if True not in IUA_FOR_KING([[0,4]], Pieces, "B"):
            if Pieces[0,4,0] == 6.2 and True not in IUA_FOR_KING([[0,1], [0,2], [0,3]], Pieces, "B"):
                if Pieces[0, 1,0] == 0 and Pieces[0,2,0] == 0 and Pieces[0,3,0] == 0 and Pieces[0,0,0] == 4.2 and Player == "B":
                    if Pieces[0,0,1] != 1:
                        legal.append([0, 0, 0, 4, True, 0, 2, 0, 3])
            if Pieces[0,4,0] == 6.2 and True not in IUA_FOR_KING([[0,6], [0,5]], Pieces, "B"):
                if Pieces[0, 6,0] == 0 and Pieces[0,5,0] == 0 and Pieces[0,7,0] == 4.2 and Player == "B":
                    if Pieces[0,7,1] != 1:
                        legal.append([0, 7, 0, 4, True, 0, 6, 0, 5])

        # Casling for white
        if True not in IUA_FOR_KING([[7,4]], Pieces, "W"):
            if Pieces[7,4,0] == 6.1 and True not in IUA_FOR_KING([[7,1], [7,2], [7,3]], Pieces, "W"):
                if Pieces[7, 1,0] == 0 and Pieces[7,2,0] == 0 and Pieces[7,3,0] == 0 and Pieces[7,0,0] == 4.1 and Player == "W":
                    if Pieces[7,0,1] != 1:
                        legal.append([7, 0, 7, 4, True, 7, 2, 7, 3])
            if Pieces[7,4,0] == 6.1 and True not in IUA_FOR_KING([[7,6], [7,5]], Pieces, "W"):
                if Pieces[7, 6,0] == 0 and Pieces[7,5,0] == 0 and Pieces[7,7,0] == 4.1 and Player == "W":
                    if Pieces[7,7,1] != 1:
                        legal.append([7, 7, 7, 4, True, 7, 6, 7, 5])
        if True not in IUA_FOR_KING([[0,3]], Pieces, "W"):
            if Pieces[0,3,0] == 6.1 and True not in IUA_FOR_KING([[0,1], [0,2]], Pieces, "W"):
                if Pieces[0, 1,0] == 0 and Pieces[0,2,0] == 0 and Pieces[0,0,0] == 4.1 and Player == "W":
                    if Pieces[0,0,1] != 1:
                        legal.append([0, 0, 0, 3, True, 0, 1, 0, 2])
            if Pieces[0,3,0] == 6.1 and True not in IUA_FOR_KING([[0,6], [0,5], [0,4]], Pieces, "W"):
                if Pieces[0, 6,0] == 0 and Pieces[0,5,0] == 0 and Pieces[0,4,0] == 0 and Pieces[0,7,0] == 4.1 and Player == "W":
                    if Pieces[0,7,1] != 1:
                        legal.append([0, 7, 0, 3, True, 0, 5, 0, 4])

    # Finish
    return legal
