
from Piece import Piece

class King(Piece):
    """
    King chess piece
    """

    def get_movement_spaces(self, boardSize : int, check_piece_at) -> list:
        """
        returns an array of all possible locations to move to (not including attacking)
        @param {int} boardSize: the size of the board
        @param {Callable(int,int)} check_piece_at: function that checks if the space
            specified by (row, col) has a piece occupying it.
        returns: {list<tuple<int,int>>} of tuple coords
        """

        spaces = []


        # go over each combination of movements
        for irow in range(-1, 2):
            for icol in range(-1, 2):
                row = self.row + irow
                col = self.col + icol
                if 0 <= row < boardSize and \
                   0 <= col < boardSize and \
                   not check_piece_at(row, col):
                    spaces.append((row, col))

        return spaces

    def get_attack_spaces(self, boardSize : int, check_piece_at) -> list:
        """
        returns an array of all possible locations to move to (not including attacking)
        @param {int} boardSize: the size of the board
        @param {Callable(row:int,col:int,color:int)} check_piece_at: function that checks
            if the space specified by (row, col) has a piece of the opposing color occupying it.
        returns: {list<tuple<int,int>>} of tuple coords
        """

        spaces = []


        # go over each combination of movements
        for irow in range(-1, 2):
            for icol in range(-1, 2):
                row = self.row + irow
                col = self.col + icol
                if 0 <= row < boardSize and \
                   0 <= col < boardSize and \
                        check_piece_at(row, col):
                    spaces.append((row, col))

        return spaces
