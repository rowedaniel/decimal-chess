
from Piece import Piece

class Pawn(Piece):
    def get_movement_spaces(self, boardSize : int, check_piece_at) -> list:
        """
        returns an array of all possible locations to move to (not including attacking)
        @param {int} boardSize: the size of the board
        @param {Callable(int,int)} check_piece_at: function that checks if the space specified by (row, col) has a piece occupying it.
        returns: {list<tuple<int,int>>} of tuple coords
        """
        
        spaces = []

        # bottom-right diagonal
        row = self.row + ( -1 if self.color == Piece.BLACK else 1 )
        col = self.col
        if row < boardSize and row >= 0 and not check_piece_at(row, col):
            spaces.append((row, col))

        return spaces



