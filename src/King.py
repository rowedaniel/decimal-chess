
from Piece import Piece
from PieceLocation import PieceLocation

class King(Piece):
    """
    King chess piece
    """

    def get_movement_spaces(self, board_size : int, check_piece_at) -> list:

        spaces = []

        # go over each combination of movements
        for irow in range(-1, 2):
            for icol in range(-1, 2):
                row = self.location.row + irow
                col = self.location.col + icol
                loc = PieceLocation(row, col)

                if 0 <= row < board_size and \
                   0 <= col < board_size and \
                   not check_piece_at(loc):

                    spaces.append(loc)

        return spaces

    def get_attack_spaces(self, board_size : int, check_piece_at, check_opposing_piece_at) -> list:

        spaces = []

        # go over each combination of movements
        for irow in range(-1, 2):
            for icol in range(-1, 2):
                row = self.location.row + irow
                col = self.location.col + icol
                loc = PieceLocation(row, col)

                if 0 <= row < board_size and \
                   0 <= col < board_size and \
                   check_opposing_piece_at(loc):

                    spaces.append(loc)

        return spaces
