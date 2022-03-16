
from Piece import Piece
from PieceLocation import PieceLocation

class Knight(Piece):
    """ Knight Piece """

    def get_movement_spaces(self, board_size : int, check_piece_at) -> list:

        spaces = []

        # go over each combination of movements
        movement = [2, 1, -2, -1, 2, -1, -2, 1]
        for i in range(len(movement)):
            row = self.location.row + movement[i]
            col = self.location.col + movement[i-1]
            loc = PieceLocation(row, col)
            if 0 <= row < board_size and \
               0 <= col < board_size and \
               not check_piece_at(loc):
                spaces.append(loc)

        return spaces


    def get_attack_spaces(self, board_size : int, check_piece_at, check_opposing_piece_at) -> list:

        spaces = []

        # go over each combination of movements
        movement = [2, 1, -2, -1, 2, -1, -2, 1]
        for i in range(len(movement)):
            row = self.location.row + movement[i]
            col = self.location.col + movement[i-1]
            loc = PieceLocation(row, col)
            if row < board_size and col < board_size and \
                    check_opposing_piece_at(loc, self.color):
                spaces.append(loc)

        return spaces
