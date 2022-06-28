import numpy as np

## Callable Pieces ##
def Piece(n):
    Base = np.ones((6,7))*0.75

    if n == 1.1:
        # Pawn Definition
        Pawn = Base
        Pawn[1:5,3] = 1
        Pawn[2,2] = 1
        Pawn[4,2] = 1
        Pawn[2,4] = 1
        Pawn[4,4] = 1
        return Pawn

    elif n == 2.1:
        # Bishop Definition
        Bishop = Base
        Bishop[:,3] = 1
        Bishop[1:3,2:5] = 1
        Bishop[4:5,2] = 1
        Bishop[4:5,4] = 1
        Bishop[5,1:2] = 1
        Bishop[5,4:5] = 1
        Bishop[5,2] = 1
        Bishop[5,5] = 1
        return Bishop

    elif n == 3.1:
        # Knight Definition
        Knight = Base
        Knight[5,1:6] = 1
        Knight[5,2:5] = 1
        Knight[4,3] = 1
        Knight[3,2:4] = 1
        Knight[2,2:6] = 1
        Knight[1,2:5] = 1
        return Knight

    elif n == 4.1:
        # Rook Definition
        Rook = Base
        Rook[2:6,1:6] = 1
        Rook[3:5,1] = 0.75
        Rook[3:5,5] = 0.75
        Rook[1,1] = 1
        Rook[1,3] = 1
        Rook[1,5] = 1
        return Rook

    elif n == 5.1:
        # Queen Definition
        Queen = Base
        Queen[3:5,1:6] = 1
        Queen[5,2:5] = 1
        Queen[1:4,1] = 1
        Queen[1:4,3] = 1
        Queen[1:4,5] = 1
        return Queen

    elif n == 6.1:
        # King Definition
        King = Base
        King[4:5,1:6] = 1
        King[4:5,2] = 0.75
        King[4:5,4] = 0.75
        King[5,2:5] = 1
        King[3,2:5] = 1
        King[0:3,3] = 1
        King[1,2:5] = 1
        return King

    elif n == 1.2:
        # Pawn Definition
        Pawn = Base
        PawnB = Base
        Pawn[1:5,3] = 1
        Pawn[2,2] = 1
        Pawn[4,2] = 1
        Pawn[2,4] = 1
        Pawn[4,4] = 1
        for j in range(6): # Black Piece Definition
            for i in range(7):
                if Pawn[j,i] == 1:
                    PawnB[j,i] = 0
                else:
                    PawnB[j,i] = 0.75
        return PawnB

    elif n == 2.2:
        # Bishop Definition
        Bishop = Base
        BishopB = Base
        Bishop[:,3] = 1
        Bishop[1:3,2:5] = 1
        Bishop[4:5,2] = 1
        Bishop[4:5,4] = 1
        Bishop[5,1:2] = 1
        Bishop[5,4:5] = 1
        Bishop[5,2] = 1
        Bishop[5,5] = 1
        for j in range(6): # Black Piece Definition
            for i in range(7):
                if Bishop[j,i] == 1:
                    BishopB[j,i] = 0
                else:
                    BishopB[j,i] = 0.75
        return BishopB

    elif n == 3.2:
        # Knight Definition
        Knight = Base
        KnightB = Base
        Knight[5,1:6] = 1
        Knight[5,2:5] = 1
        Knight[4,3] = 1
        Knight[3,2:4] = 1
        Knight[2,2:6] = 1
        Knight[1,2:5] = 1
        for j in range(6): # Black Piece Definition
            for i in range(7):
                if Knight[j,i] == 1:
                    KnightB[j,i] = 0
                else:
                    KnightB[j,i] = 0.75
        return KnightB

    elif n == 4.2:
        # Rook Definition
        Rook = Base
        RookB = Base
        Rook[2:6,1:6] = 1
        Rook[3:5,1] = 0.75
        Rook[3:5,5] = 0.75
        Rook[1,1] = 1
        Rook[1,3] = 1
        Rook[1,5] = 1
        for j in range(6): # Black Piece Definition
            for i in range(7):
                if Rook[j,i] == 1:
                    RookB[j,i] = 0
                else:
                    RookB[j,i] = 0.75
        return RookB

    elif n == 5.2:
        # Queen Definition
        Queen = Base
        QueenB = Base
        Queen[3:5,1:6] = 1
        Queen[5,2:5] = 1
        Queen[1:4,1] = 1
        Queen[1:4,3] = 1
        Queen[1:4,5] = 1
        for j in range(6): # Black Piece Definition
            for i in range(7):
                if Queen[j,i] == 1:
                    QueenB[j,i] = 0
                else:
                    QueenB[j,i] = 0.75
        return QueenB

    elif n == 6.2:
        # King Definition
        King = Base
        KingB = Base
        King[4:5,1:6] = 1
        King[4:5,2] = 0.75
        King[4:5,4] = 0.75
        King[5,2:5] = 1
        King[3,2:5] = 1
        King[0:3,3] = 1
        King[1,2:5] = 1
        for j in range(6): # Black Piece Definition
            for i in range(7):
                if King[j,i] == 1:
                    KingB[j,i] = 0
                else:
                    KingB[j,i] = 0.75
        return KingB

    elif n == 0:
        return Base

# Starting Layout
def Starting_Board(Pieces):
    # Layout of White Pieces
    Pieces[6,:] = 1.1
    Pieces[7,2] = 2.1
    Pieces[7,5] = 2.1
    Pieces[7,1] = 3.1
    Pieces[7,6] = 3.1
    Pieces[7,0] = 4.1
    Pieces[7,7] = 4.1
    Pieces[7,3] = 5.1
    Pieces[7,4] = 6.1
    # Layout of Black Pieces
    Pieces[1,:] = 1.2
    Pieces[0,2] = 2.2
    Pieces[0,5] = 2.2
    Pieces[0,1] = 3.2
    Pieces[0,6] = 3.2
    Pieces[0,0] = 4.2
    Pieces[0,7] = 4.2
    Pieces[0,3] = 5.2
    Pieces[0,4] = 6.2
    return Pieces
