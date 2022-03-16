
from Piece import Piece
from PieceLocation import PieceLocation

class Rook(Piece):
    """ rook piece """
    def get_movement_spaces(self, board_size : int, check_piece_at) -> list:

        spaces = []

        # right line
        row = self.location.row + 1
        col = self.location.col
        while row < board_size:
            loc = PieceLocation(row, col)
            if check_piece_at(loc):
                break
            spaces.append(loc)
            row += 1

        # bottom line
        row = self.location.row
        col = self.location.col + 1
        while col < board_size:
            loc = PieceLocation(row, col)
            if check_piece_at(loc):
                break
            spaces.append(loc)
            col += 1

        # left line
        row = self.location.row - 1
        col = self.location.col
        while row >= 0:
            loc = PieceLocation(row, col)
            if check_piece_at(loc):
                break
            spaces.append(loc)
            row -= 1

        # left line
        row = self.location.row
        col = self.location.col - 1
        while col >= 0:
            loc = PieceLocation(row, col)
            if check_piece_at(loc):
                break
            spaces.append(loc)
            col -= 1

        return spaces


    def get_attack_spaces(self, board_size : int, check_piece_at, check_opposing_piece_at) -> list:

        spaces = []

        # right line
        row = self.location.row + 1
        col = self.location.col
        while row < board_size:
            loc = PieceLocation(row, col)
            if check_piece_at(loc):
                if check_opposing_piece_at(loc, self.color):
                    spaces.append(loc)
                break
            row += 1

        # bottom line
        row = self.location.row
        col = self.location.col + 1
        while col < board_size:
            loc = PieceLocation(row, col)
            if check_piece_at(loc):
                if check_opposing_piece_at(loc, self.color):
                    spaces.append(loc)
                break
            col += 1

        # left line
        row = self.location.row - 1
        col = self.location.col
        while row >= 0:
            loc = PieceLocation(row, col)
            if check_piece_at(loc):
                if check_opposing_piece_at(loc, self.color):
                    spaces.append(loc)
                break
            row -= 1

        # left line
        row = self.location.row
        col = self.location.col - 1
        while col >= 0:
            loc = PieceLocation(row, col)
            if check_piece_at(loc):
                if check_opposing_piece_at(loc, self.color):
                    spaces.append(loc)
                break
            col -= 1

        return spaces
