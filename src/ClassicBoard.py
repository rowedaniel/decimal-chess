
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
    def __init__(self, base_piece_health : int, piece_attack : dict, game_id : int):
        """
        Builds the board (pieces included)
        @param {int} base_piece_health: the base health for each piece (the same for all)
        @param {map<Piece, int} piece_attack: dictionary of attack stats for each piece
        """

        self.base_piece_health= base_piece_health
        self.piece_attack = piece_attack

        super().__init__(8, game_id)

        self.reset_board()



    def reset_board(self):
        super().reset_board()
        # place all the pieces
        layout = (
                (Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook),
                tuple(Pawn for i in range(self.size))
                )

        for cindex in (0,1):
            color = (Piece.WHITE, Piece.BLACK)[cindex]

            rows = []
            if cindex:
                rows.append(self.size-1)
                rows.append(self.size-2)
            else:
                rows.append(0)
                rows.append(1)
            for rindex in range(2):
                row = rows[rindex]
                for column in range(self.size):
                    piece = layout[rindex][column]
                    loc = PieceLocation(row, column)

                    self.place_piece(loc,
                            piece(self.base_piece_health,
                                self.base_piece_health,
                                self.piece_attack[piece],
                                loc,
                                color)
                            )
