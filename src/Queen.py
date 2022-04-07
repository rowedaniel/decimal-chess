
from Piece import Piece
from Rook import Rook
from Bishop import Bishop

class Queen(Piece):
    """
    Queen Piece

    NOTE: since queens in chess have the same movement as rooks + bishops,
    the movement for queens is not explicitly specified. Instead, Queen directly
    calls Bishop and Rook's movement methods.

    """

    def get_movement_spaces(self, board_size : int, check_piece_at) -> list:
        spaces = []
        spaces.extend(Rook.get_movement_spaces(self, board_size, check_piece_at))
        spaces.extend(Bishop.get_movement_spaces(self, board_size, check_piece_at))
        return spaces

    def get_attack_spaces(self, board_size : int, check_piece_at, check_opposing_piece_at) -> list:
        spaces = []
        spaces.extend(
                Rook.get_attack_spaces(self, board_size, check_piece_at, check_opposing_piece_at)
                )
        spaces.extend(
                Bishop.get_attack_spaces(self, board_size, check_piece_at, check_opposing_piece_at)
                )
        return spaces

    def __str__(self):
        return 'queen'
