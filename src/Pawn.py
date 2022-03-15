
from Piece import Piece

class Pawn(Piece):
    """ Pawn Chess piece """
    def get_movement_spaces(self, boardSize : int, check_piece_at) -> list:
        """
        returns an array of all possible locations to move to (not including attacking)
        @param {int} boardSize: the size of the board
        @param {Callable(int,int)} check_piece_at: function that checks if the space
            specified by (row, col) has a piece occupying it.
        returns: {list<tuple<int,int>>} of tuple coords
        """
        spaces = []

        # bottom-right diagonal
        row = self.row + ( -1 if self.color == Piece.BLACK else 1 )
        col = self.col
        if 0 <= row < boardSize and not check_piece_at(row, col):
            spaces.append((row, col))

        return spaces

    def get_attack_spaces(self, boardSize : int, check_piece_at) -> list:
        """
        returns an array of all possible locations to attack
        @param {int} boardSize: the size of the board
        @param {Callable(int,int,int)} check_piece_at: function that checks if the space
            specified by (row, col) has an opposing piece occupying it.
        returns: {list<tuple<int,int>>} of tuple coords
        """
        spaces = []

        # bottom-right diagonal
        row = self.row + ( -1 if self.color == Piece.BLACK else 1 )
        for col in (self.col-1, self.col+1):
            if 0 <= row < boardSize and check_piece_at(row, col, self.color):
                spaces.append((row, col))

        return spaces
