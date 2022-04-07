
from Piece import Piece
from PieceLocation import PieceLocation

class Bishop(Piece):
    """
    Bishop piece
    """

    def get_movement_spaces(self, board_size : int, check_piece_at) -> list:

        spaces = []

        # bottom-right diagonal
        row = self.location.row + 1
        col = self.location.col + 1
        loc = PieceLocation(row, col)
        while 0 <= row < board_size and 0 <= col < board_size and not check_piece_at(loc):
            spaces.append(PieceLocation(row, col))
            row += 1
            col += 1
            loc = PieceLocation(row, col)

        # bottom-left diagonal
        row = self.location.row + 1
        col = self.location.col - 1
        loc = PieceLocation(row, col)
        while 0 <= row < board_size and 0 <= col < board_size and not check_piece_at(loc):
            spaces.append(PieceLocation(row, col))
            row += 1
            col -= 1
            loc = PieceLocation(row, col)

        # top-right diagonal
        row = self.location.row - 1
        col = self.location.col + 1
        loc = PieceLocation(row, col)
        while 0 <= row < board_size and 0 <= col < board_size and not check_piece_at(loc):
            spaces.append(PieceLocation(row, col))
            row -= 1
            col += 1
            loc = PieceLocation(row, col)

        # top-left diagonal
        row = self.location.row - 1
        col = self.location.col - 1
        loc = PieceLocation(row, col)
        while 0 <= row < board_size and 0 <= col < board_size and not check_piece_at(loc):
            spaces.append(PieceLocation(row, col))
            row -= 1
            col -= 1
            loc = PieceLocation(row, col)

        return spaces



    def get_attack_spaces(self, board_size : int, check_piece_at, check_opposing_piece_at) -> list:

        spaces = []

        # bottom-right diagonal
        row = self.location.row + 1
        col = self.location.col + 1
        while 0 <= row < board_size and 0 <= col < board_size:
            loc = PieceLocation(row, col)
            if check_piece_at(loc):
                spaces.extend(check_opposing_piece_at(loc, self.color))
                break
            row += 1
            col += 1

        # bottom-left diagonal
        row = self.location.row + 1
        col = self.location.col - 1
        while 0 <= row < board_size and col >= 0:
            loc = PieceLocation(row, col)
            if check_piece_at(loc):
                spaces.extend(check_opposing_piece_at(loc, self.color))
                break
            row += 1
            col -= 1

        # top-right diagonal
        row = self.location.row - 1
        col = self.location.col + 1
        while row >= 0 and 0 <= col < board_size:
            loc = PieceLocation(row, col)
            if check_piece_at(loc):
                spaces.extend(check_opposing_piece_at(loc, self.color))
                break
            row -= 1
            col += 1

        # top-left diagonal
        row = self.location.row - 1
        col = self.location.col - 1
        while row >= 0 and col >= 0:
            loc = PieceLocation(row, col)
            if check_piece_at(loc):
                spaces.extend(check_opposing_piece_at(loc, self.color))
                break
            row -= 1
            col -= 1

        return spaces

    def __str__(self):
        return 'bishop'
