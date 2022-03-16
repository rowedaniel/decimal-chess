
from Piece import Piece
from PieceLocation import PieceLocation

class Pawn(Piece):
    """ Pawn Chess piece """

    def get_movement_spaces(self, board_size : int, check_piece_at) -> list:
        spaces = []

        # bottom-right diagonal
        for i in range(2 - self.has_moved):
            row = self.location.row + ( -1 if self.color == Piece.BLACK else 1 ) * (i+1)
            col = self.location.col
            loc = PieceLocation(row, col)
            if 0 <= row < board_size and not check_piece_at(loc):
                spaces.append(loc)

        return spaces

    def get_attack_spaces(self, board_size : int, check_piece_at, check_opposing_piece_at) -> list:
        spaces = []

        # bottom-right diagonal
        row = self.location.row + ( -1 if self.color == Piece.BLACK else 1 )
        for col in (self.location.col-1, self.location.col+1):
            loc = PieceLocation(row, col)
            if 0 <= row < board_size and check_opposing_piece_at(loc, self.color):
                spaces.append(loc)

        return spaces
