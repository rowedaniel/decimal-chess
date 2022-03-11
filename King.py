
from Piece import Piece

class King(Piece):
    def get_movement_spaces(self, boardSize : int, check_piece_at) -> list:
        """
        returns an array of all possible locations to move to (not including attacking)
        @param {int} boardSize: the size of the board
        @param {Callable(int,int)} check_piece_at: function that checks if the space specified by (row, col) has a piece occupying it.
        returns: {list<tuple<int,int>>} of tuple coords
        """
        
        spaces = []


        # go over each combination of movements
        for r in range(-1, 2):
            for c in range(-1, 2):
                row = self.row + r
                col = self.col + c
                if row < boardSize and col < boardSize and not check_piece_at(row, col):
                    spaces.append((row, col))

        return spaces

    def get_attack_spaces(self, boardSize : int, check_piece_at, check_piece_color_at) -> list:
        """
        returns an array of all possible locations to move to (not including attacking)
        @param {int} boardSize: the size of the board
        @param {Callable(int,int)} check_piece_at: function that checks if the space specified by (row, col) has a piece occupying it.
        @param {Callable(int,int)} check_piece_color_at: function that returns the color of the piece at specified (row, col) coords
        returns: {list<tuple<int,int>>} of tuple coords
        """

        spaces = []


        # go over each combination of movements
        for r in range(-1, 2):
            for c in range(-1, 2):
                row = self.row + r
                col = self.col + c
                if row < boardSize and col < boardSize and \
                   check_piece_at(row, col) and check_piece_color_at(row, col) != self.color:
                    spaces.append((row, col))

        return spaces


