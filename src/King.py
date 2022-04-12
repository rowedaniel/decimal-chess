
from Piece import Piece
from PieceLocation import PieceLocation

class King(Piece):
    """
    King chess piece
    """

    def get_tiles(self, board_size : int):
        """
        gets all the tiles that the king can attack
        """
        for irow in range(-1,2):
            for icol in range(-1,2):
                if irow == 0 and icol == 0:
                    continue
                row = self.location.row + irow
                col = self.location.col + icol

                if 0 <= row < board_size and \
                   0 <= col < board_size:
                    yield PieceLocation(row,col)

    def get_movement_spaces(self, board_size : int, check_piece_at) -> list:

        spaces = []

        for loc in self.get_tiles(board_size):
            if not check_piece_at(loc):
                spaces.append(loc)

        return spaces

    def get_attack_spaces(self, board_size : int, check_piece_at, check_opposing_piece_at) -> list:

        spaces = []

        for loc in self.get_tiles(board_size):
            spaces.extend(check_opposing_piece_at(loc, self.color))

        return spaces

    def __str__(self):
        return 'king'
