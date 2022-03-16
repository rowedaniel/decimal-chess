
from Board import Board

from PieceLocation import PieceLocation
from Piece import Piece

from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Queen import Queen
from King import King
from Pawn import Pawn





class ClassicBoard(Board):
    """
    Standard 8x8 Chess board, with default piece layout.
    """
    def __init__(self, base_piece_health : int, piece_attack : dict):
        """
        Builds the board (pieces included)
        @param {int} base_piece_health: the base health for each piece (the same for all)
        @param {map<Piece, int} piece_attack: dictionary of attack stats for each piece
        """
        super().__init__(8)


        # place all the pieces
        backrow_layout = (Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook)
        frontrow_layout = tuple(Pawn for i in range(self.size))

        for cindex in (0,1):
            color = (Piece.WHITE, Piece.BLACK)[cindex]

            # back row
            row = cindex * 7
            for column in range(self.size):
                piece = backrow_layout[column]
                loc = PieceLocation(row, column)

                self.place_piece(loc,
                        piece(base_piece_health, piece_attack[piece], loc, color)
                        )

            # front row
            row += 1 - 2 * cindex
            for column in range(self.size):
                piece = frontrow_layout[column]
                loc = PieceLocation(row, column)

                self.place_piece(loc,
                        piece(base_piece_health, piece_attack[piece], loc, color)
                        )
